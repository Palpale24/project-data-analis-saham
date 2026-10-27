"""Paper trading: jurnal transaksi virtual dan perhitungan portofolio.

Tidak ada koneksi ke broker. Semua transaksi hanya dicatat di file CSV lokal.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from src.config import INITIAL_CAPITAL, LOT_SIZE, PAPER_TRADES_FILE

WIB = ZoneInfo("Asia/Jakarta")

TRADE_COLUMNS = [
    "id",
    "date",
    "ticker",
    "side",
    "price",
    "lots",
    "fee_pct",
    "tax_pct",
    "reason",
    "note",
    "created_at",
]


@dataclass
class PortfolioResult:
    initial_cash: float
    cash: float
    holdings_value: float
    equity: float
    realized_pnl: float
    unrealized_pnl: float
    total_pnl: float
    return_pct: float
    holdings: pd.DataFrame = field(default_factory=pd.DataFrame)
    ledger: pd.DataFrame = field(default_factory=pd.DataFrame)
    warnings: list[str] = field(default_factory=list)


def empty_trades() -> pd.DataFrame:
    return pd.DataFrame(columns=TRADE_COLUMNS)


def load_trades(path: Path | str = PAPER_TRADES_FILE) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return empty_trades()
    try:
        frame = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        return empty_trades()
    for column in TRADE_COLUMNS:
        if column not in frame.columns:
            frame[column] = ""
    frame = frame[TRADE_COLUMNS].copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["created_at"] = pd.to_datetime(frame["created_at"], errors="coerce")
    frame["ticker"] = frame["ticker"].astype(str).str.upper().str.strip()
    frame["side"] = frame["side"].astype(str).str.upper().str.strip()
    for column in ["price", "lots", "fee_pct", "tax_pct"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=["date", "ticker", "side", "price", "lots"])
    return frame.sort_values(["date", "created_at"], na_position="last").reset_index(drop=True)


def _atomic_write(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp.csv")
    frame.to_csv(tmp, index=False)
    tmp.replace(path)


def _replay_validate(trades: pd.DataFrame, initial_cash: float) -> None:
    cash = float(initial_cash)
    positions: dict[str, int] = {}
    for index, row in trades.sort_values(["date", "created_at"], na_position="last").iterrows():
        ticker = str(row["ticker"]).upper()
        lots = int(row["lots"])
        shares = lots * LOT_SIZE
        price = float(row["price"])
        fee = price * shares * float(row["fee_pct"]) / 100
        if row["side"] == "BELI":
            total = price * shares + fee
            if total > cash + 0.01:
                raise ValueError(
                    f"Transaksi baris {index + 1} ({ticker}, {row['date'].date()}): "
                    f"kas virtual tidak cukup. Butuh Rp{total:,.0f}, tersedia Rp{cash:,.0f}."
                )
            cash -= total
            positions[ticker] = positions.get(ticker, 0) + shares
        elif row["side"] == "JUAL":
            held = positions.get(ticker, 0)
            if shares > held:
                raise ValueError(
                    f"Transaksi baris {index + 1} ({ticker}, {row['date'].date()}): "
                    f"hanya memiliki {held:,} lembar, tidak bisa menjual {shares:,} lembar."
                )
            tax = price * shares * float(row["tax_pct"]) / 100
            cash += price * shares - fee - tax
            positions[ticker] = held - shares
        else:
            raise ValueError(f"Jenis transaksi tidak dikenal: {row['side']}")


def validate_new_trade(trade: dict, existing: pd.DataFrame, initial_cash: float = INITIAL_CAPITAL) -> dict:
    required = ["date", "ticker", "side", "price", "lots", "fee_pct", "tax_pct", "reason"]
    missing = [key for key in required if key not in trade or str(trade[key]).strip() == ""]
    if missing:
        raise ValueError(f"Kolom wajib belum lengkap: {', '.join(missing)}")

    parsed_date = pd.to_datetime(trade["date"], errors="coerce")
    if pd.isna(parsed_date):
        raise ValueError("Tanggal transaksi tidak valid")
    if parsed_date.date() > date.today():
        raise ValueError("Tanggal transaksi tidak boleh di masa depan")
    ticker = str(trade["ticker"]).upper().strip()
    if not ticker:
        raise ValueError("Kode saham wajib diisi")
    side = str(trade["side"]).upper().strip()
    if side not in {"BELI", "JUAL"}:
        raise ValueError("Jenis transaksi harus BELI atau JUAL")
    try:
        price = float(trade["price"])
        lots = float(trade["lots"])
        fee_pct = float(trade["fee_pct"])
        tax_pct = float(trade["tax_pct"])
    except (TypeError, ValueError) as exc:
        raise ValueError("Harga, lot, dan persentase biaya harus berupa angka") from exc
    if price <= 0:
        raise ValueError("Harga simulasi harus lebih dari 0")
    if lots <= 0 or int(lots) != lots:
        raise ValueError("Jumlah lot harus bilangan bulat positif")
    if not 0 <= fee_pct <= 100 or not 0 <= tax_pct <= 100:
        raise ValueError("Persentase biaya harus di antara 0% dan 100%")
    if len(str(trade["reason"]).strip()) < 3:
        raise ValueError("Alasan transaksi minimal 3 karakter agar jurnal bermakna")

    row = {
        "id": uuid.uuid4().hex[:12],
        "date": parsed_date.normalize(),
        "ticker": ticker,
        "side": side,
        "price": price,
        "lots": int(lots),
        "fee_pct": fee_pct,
        "tax_pct": tax_pct,
        "reason": str(trade["reason"]).strip(),
        "note": str(trade.get("note", "")).strip(),
        "created_at": datetime.now(WIB).replace(tzinfo=None),
    }
    candidate = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    _replay_validate(candidate, initial_cash)
    return row


def append_trade(
    trade: dict,
    path: Path | str = PAPER_TRADES_FILE,
    initial_cash: float = INITIAL_CAPITAL,
) -> pd.DataFrame:
    path = Path(path)
    existing = load_trades(path)
    row = validate_new_trade(trade, existing, initial_cash=initial_cash)
    updated = pd.concat([existing, pd.DataFrame([row])], ignore_index=True)
    updated = updated.sort_values(["date", "created_at"], na_position="last").reset_index(drop=True)
    _atomic_write(updated, path)
    return updated


def delete_last_trade(path: Path | str = PAPER_TRADES_FILE) -> pd.DataFrame:
    path = Path(path)
    existing = load_trades(path)
    if existing.empty:
        return existing
    last_index = existing["created_at"].idxmax() if existing["created_at"].notna().any() else existing.index[-1]
    updated = existing.drop(index=last_index).reset_index(drop=True)
    _atomic_write(updated, path)
    return updated


def simulate_portfolio(
    trades: pd.DataFrame,
    latest_prices: pd.Series | dict,
    initial_cash: float = INITIAL_CAPITAL,
) -> PortfolioResult:
    """Hitung kas, posisi, dan laba/rugi dengan metode harga rata-rata."""
    latest = dict(latest_prices) if not isinstance(latest_prices, dict) else latest_prices
    if trades.empty:
        return PortfolioResult(
            initial_cash=initial_cash,
            cash=initial_cash,
            holdings_value=0.0,
            equity=initial_cash,
            realized_pnl=0.0,
            unrealized_pnl=0.0,
            total_pnl=0.0,
            return_pct=0.0,
            holdings=pd.DataFrame(
                columns=[
                    "Ticker",
                    "Saham",
                    "Lot",
                    "Harga Rata-rata",
                    "Harga Terakhir",
                    "Nilai Pasar",
                    "Laba/Rugi Belum Terealisasi",
                    "Return (%)",
                ]
            ),
            ledger=pd.DataFrame(),
            warnings=["Belum ada transaksi virtual."],
        )

    _replay_validate(trades, initial_cash)
    cash = float(initial_cash)
    positions: dict[str, dict[str, float]] = {}
    realized = 0.0
    ledger_rows: list[dict] = []
    warnings: list[str] = []

    ordered = trades.sort_values(["date", "created_at"], na_position="last")
    for _, row in ordered.iterrows():
        ticker = str(row["ticker"]).upper()
        shares = int(row["lots"]) * LOT_SIZE
        price = float(row["price"])
        gross = price * shares
        fee = gross * float(row["fee_pct"]) / 100
        tax = 0.0
        row_realized = 0.0

        if ticker not in latest:
            warnings.append(f"Harga terakhir {ticker} tidak tersedia; harga transaksi terakhir dipakai.")
            latest[ticker] = price

        if row["side"] == "BELI":
            total = gross + fee
            cash -= total
            position = positions.setdefault(ticker, {"shares": 0, "cost_basis": 0.0})
            position["shares"] += shares
            position["cost_basis"] += total
            cash_flow = -total
        else:
            tax = gross * float(row["tax_pct"]) / 100
            net_proceeds = gross - fee - tax
            cash += net_proceeds
            position = positions[ticker]
            average_cost = position["cost_basis"] / position["shares"]
            cost_removed = average_cost * shares
            row_realized = net_proceeds - cost_removed
            realized += row_realized
            position["shares"] -= shares
            position["cost_basis"] -= cost_removed
            if position["shares"] <= 0:
                positions.pop(ticker, None)
            cash_flow = net_proceeds

        ledger_rows.append(
            {
                "Tanggal": row["date"],
                "Ticker": ticker,
                "Aksi": row["side"],
                "Lot": int(row["lots"]),
                "Saham": shares,
                "Harga": price,
                "Nilai Bruto": gross,
                "Biaya": fee + tax,
                "Arus Kas": cash_flow,
                "Kas Setelah": cash,
                "Laba/Rugi Terealisasi": row_realized,
            }
        )

    holding_rows = []
    holdings_value = 0.0
    unrealized = 0.0
    for ticker, position in positions.items():
        shares = int(position["shares"])
        average_cost = position["cost_basis"] / shares if shares else 0.0
        last_price = float(latest.get(ticker, average_cost))
        market_value = shares * last_price
        pnl = market_value - position["cost_basis"]
        holdings_value += market_value
        unrealized += pnl
        holding_rows.append(
            {
                "Ticker": ticker,
                "Saham": shares,
                "Lot": shares // LOT_SIZE,
                "Harga Rata-rata": average_cost,
                "Harga Terakhir": last_price,
                "Nilai Pasar": market_value,
                "Laba/Rugi Belum Terealisasi": pnl,
                "Return (%)": pnl / position["cost_basis"] * 100
                if position["cost_basis"]
                else 0.0,
            }
        )

    holdings = pd.DataFrame(holding_rows).sort_values("Ticker").reset_index(drop=True) if holding_rows else pd.DataFrame(
        columns=[
            "Ticker",
            "Saham",
            "Lot",
            "Harga Rata-rata",
            "Harga Terakhir",
            "Nilai Pasar",
            "Laba/Rugi Belum Terealisasi",
            "Return (%)",
        ]
    )
    equity = cash + holdings_value
    return PortfolioResult(
        initial_cash=initial_cash,
        cash=cash,
        holdings_value=holdings_value,
        equity=equity,
        realized_pnl=realized,
        unrealized_pnl=unrealized,
        total_pnl=equity - initial_cash,
        return_pct=(equity / initial_cash - 1) * 100 if initial_cash else 0.0,
        holdings=holdings,
        ledger=pd.DataFrame(ledger_rows),
        warnings=warnings,
    )
