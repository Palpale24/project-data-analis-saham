"""Pembersihan dan validasi data snapshot IDX serta data historis."""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

SNAPSHOT_COLUMN_MAP = {
    "No": "no",
    "Kode Saham": "ticker",
    "Nama Perusahaan": "company_name",
    "Remarks": "remarks",
    "Sebelumnya": "previous_close",
    "Open Price": "open",
    "Tanggal Perdagangan Terakhir": "last_trade_date",
    "First Trade": "first_trade",
    "Tertinggi": "high",
    "Terendah": "low",
    "Penutupan": "close",
    "Selisih": "change",
    "Volume": "volume",
    "Nilai": "value",
    "Frekuensi": "frequency",
    "Index Individual": "index_individual",
    "Offer": "offer",
    "Offer Volume": "offer_volume",
    "Bid": "bid",
    "Bid Volume": "bid_volume",
    "Listed Shares": "listed_shares",
    "Tradeble Shares": "tradeable_shares",
    "Weight For Index": "weight_for_index",
    "Foreign Sell": "foreign_sell",
    "Foreign Buy": "foreign_buy",
    "Non Regular Volume": "non_regular_volume",
    "Non Regular Value": "non_regular_value",
    "Non Regular Frequency": "non_regular_frequency",
}

SNAPSHOT_REQUIRED = set(SNAPSHOT_COLUMN_MAP)
SNAPSHOT_NUMERIC = [
    "no",
    "previous_close",
    "open",
    "first_trade",
    "high",
    "low",
    "close",
    "change",
    "volume",
    "value",
    "frequency",
    "index_individual",
    "offer",
    "offer_volume",
    "bid",
    "bid_volume",
    "listed_shares",
    "tradeable_shares",
    "weight_for_index",
    "foreign_sell",
    "foreign_buy",
    "non_regular_volume",
    "non_regular_value",
    "non_regular_frequency",
]

MONTHS_ID = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "mei": 5,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "agu": 8,
    "agt": 8,
    "aug": 8,
    "sep": 9,
    "okt": 10,
    "oct": 10,
    "nov": 11,
    "des": 12,
    "dec": 12,
}


def parse_indonesian_date(value: Any) -> pd.Timestamp:
    """Ubah tanggal Indonesia seperti '23 Okt 2026' menjadi Timestamp.

    Mengembalikan pd.NaT jika format tidak dikenali, bukan menebak tanggal.
    """
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return pd.NaT
    if isinstance(value, pd.Timestamp):
        return value.normalize()
    text = str(value).strip()
    if not text:
        return pd.NaT

    # Format ISO dan format angka umum ditangani pandas.
    try:
        return pd.Timestamp(text).normalize()
    except (ValueError, TypeError):
        pass

    match = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})", text)
    if not match:
        return pd.NaT
    day, month_text, year = match.groups()
    month = MONTHS_ID.get(month_text.lower()[:3])
    if month is None:
        return pd.NaT
    try:
        return pd.Timestamp(year=int(year), month=month, day=int(day))
    except ValueError:
        return pd.NaT


def validate_ohlc(frame: pd.DataFrame) -> pd.Series:
    """Tandai baris dengan harga tidak konsisten (True = valid).

    Nilai 0 pada saham yang tidak diperdagangkan bukan otomatis dianggap error.
    Snapshot IDX juga dapat mencatat Open Price = 0 untuk saham yang tetap
    diperdagangkan; dalam kasus itu open dianggap tidak tersedia, bukan harga nol.
    """
    traded = frame.get("volume", pd.Series(0, index=frame.index)).fillna(0) > 0
    prices = frame[["open", "high", "low", "close"]].apply(pd.to_numeric, errors="coerce")
    open_available = prices["open"].fillna(0) > 0
    basic = (
        (prices["high"] >= prices["low"])
        & (prices["high"] > 0)
        & (prices["low"] > 0)
        & (prices["close"] > 0)
        & (prices["high"] + 0.01 >= prices["close"])
        & (prices["low"] - 0.01 <= prices["close"])
    )
    upper_ok = (~open_available) | (prices["high"] + 0.01 >= prices["open"])
    lower_ok = (~open_available) | (prices["low"] - 0.01 <= prices["open"])
    return (~traded) | (basic & upper_ok & lower_ok)


def clean_snapshot(raw: pd.DataFrame) -> pd.DataFrame:
    """Normalisasi snapshot harian tanpa mengubah file mentah."""
    missing = SNAPSHOT_REQUIRED.difference(raw.columns)
    if missing:
        raise ValueError(f"Kolom snapshot tidak lengkap: {sorted(missing)}")

    frame = raw.copy()
    frame = frame.rename(columns=SNAPSHOT_COLUMN_MAP)
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    frame["company_name"] = frame["company_name"].astype(str).str.strip()
    frame["last_trade_date"] = frame["last_trade_date"].map(parse_indonesian_date)

    for column in SNAPSHOT_NUMERIC:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.drop_duplicates()
    frame = frame.drop_duplicates(subset=["ticker"], keep="last")
    frame = frame.sort_values("ticker").reset_index(drop=True)

    frame["traded"] = frame["volume"].fillna(0) > 0
    frame["ohlc_valid"] = validate_ohlc(frame)
    frame["market_cap"] = frame["close"] * frame["listed_shares"]
    frame["foreign_net"] = frame["foreign_buy"].fillna(0) - frame["foreign_sell"].fillna(0)
    frame["avg_trade_price"] = np.where(
        frame["volume"].fillna(0) > 0,
        frame["value"] / frame["volume"].replace(0, np.nan),
        np.nan,
    )
    frame["tradeable_pct"] = np.where(
        frame["listed_shares"].fillna(0) > 0,
        frame["tradeable_shares"] / frame["listed_shares"] * 100,
        np.nan,
    )
    return frame


def snapshot_quality_report(raw: pd.DataFrame, clean: pd.DataFrame | None = None) -> dict[str, Any]:
    """Ringkasan kualitas data snapshot dalam bentuk yang mudah ditampilkan."""
    frame = clean if clean is not None else raw
    if "ticker" not in frame.columns:
        frame = clean_snapshot(raw)

    dates = sorted(
        {d.date().isoformat() for d in frame["last_trade_date"].dropna().unique()}
    )
    invalid_ohlc = int((~frame["ohlc_valid"]).sum()) if "ohlc_valid" in frame else 0
    no_trade = int((frame["volume"].fillna(0) <= 0).sum())
    zero_open_traded = int(
        ((frame["volume"].fillna(0) > 0) & (frame["open"].fillna(0) <= 0)).sum()
    )
    missing_by_column = {
        str(column): int(count) for column, count in raw.isna().sum().items() if count > 0
    }

    return {
        "rows": int(len(frame)),
        "columns": int(len(raw.columns)),
        "unique_tickers": int(frame["ticker"].nunique()),
        "dates": dates,
        "date_count": len(dates),
        "missing_values": int(raw.isna().sum().sum()),
        "missing_by_column": missing_by_column,
        "duplicate_rows": int(raw.duplicated().sum()),
        "duplicate_tickers": int(raw.duplicated(subset=["Kode Saham"]).sum())
        if "Kode Saham" in raw.columns
        else 0,
        "no_trade_rows": no_trade,
        "zero_open_traded_rows": zero_open_traded,
        "invalid_ohlc_rows": invalid_ohlc,
        "zero_close_rows": int((frame["close"].fillna(0) <= 0).sum()),
        "total_value": float(frame["value"].fillna(0).sum()),
        "total_volume": float(frame["volume"].fillna(0).sum()),
        "median_value": float(frame["value"].median()),
        "traded_rows": int(frame["traded"].sum()) if "traded" in frame else None,
        "single_date": len(dates) == 1,
        "warnings": _snapshot_warnings(dates, no_trade, invalid_ohlc, zero_open_traded),
    }


def _snapshot_warnings(
    dates: list[str], no_trade: int, invalid_ohlc: int, zero_open_traded: int = 0
) -> list[str]:
    warnings: list[str] = []
    if len(dates) == 1:
        warnings.append(
            "Data hanya mencakup satu tanggal. Grafik tren, return historis, dan risiko "
            "tidak boleh dihitung dari snapshot ini."
        )
    if len(dates) == 0:
        warnings.append("Tanggal perdagangan tidak dapat dibaca.")
    if no_trade:
        warnings.append(
            f"{no_trade} saham tidak memiliki volume transaksi pada tanggal tersebut; "
            "harga penutupan bisa merupakan harga terakhir sebelumnya."
        )
    if zero_open_traded:
        warnings.append(
            f"{zero_open_traded} saham diperdagangkan tetapi Open Price tercatat 0. "
            "Nilai tersebut diperlakukan sebagai data tidak tersedia, bukan harga nol."
        )
    if invalid_ohlc:
        warnings.append(f"{invalid_ohlc} baris memiliki hubungan harga OHLC yang tidak wajar.")
    return warnings


def clean_historical(prices: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan data historis tanpa mengisi harga yang hilang secara sembarangan."""
    required = {"date", "ticker", "open", "high", "low", "close", "adj_close", "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Kolom historis tidak lengkap: {sorted(missing)}")

    frame = prices.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    for column in ["open", "high", "low", "close", "adj_close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.dropna(subset=["date", "ticker", "close", "adj_close"])
    frame = frame[(frame["close"] > 0) & (frame["adj_close"] > 0)]
    frame = frame.drop_duplicates(subset=["ticker", "date"], keep="last")
    frame = frame.sort_values(["ticker", "date"]).reset_index(drop=True)
    frame["ohlc_valid"] = validate_ohlc(frame)
    return frame


def historical_quality_report(prices: pd.DataFrame) -> dict[str, Any]:
    """Laporan kualitas per ticker untuk data historis."""
    if prices.empty:
        return {
            "rows": 0,
            "tickers": 0,
            "date_min": None,
            "date_max": None,
            "missing_values": 0,
            "duplicate_rows": 0,
            "invalid_ohlc_rows": 0,
            "per_ticker": pd.DataFrame(),
        }

    frame = prices.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    all_dates = frame["date"].dropna().nunique()
    rows: list[dict[str, Any]] = []
    for ticker, group in frame.groupby("ticker", sort=True):
        adjusted_diff = (group["close"].round(4) != group["adj_close"].round(4)).mean() * 100
        gaps = group["date"].sort_values().diff().dt.days
        rows.append(
            {
                "Ticker": ticker,
                "Baris": int(len(group)),
                "Awal": group["date"].min().date(),
                "Akhir": group["date"].max().date(),
                "Kelengkapan (%)": round(len(group) / all_dates * 100, 1) if all_dates else 0.0,
                "Missing": int(group[["open", "high", "low", "close", "adj_close", "volume"]].isna().sum().sum()),
                "Duplikat": int(group.duplicated(subset=["date"]).sum()),
                "OHLC Tidak Wajar": int((~group["ohlc_valid"]).sum()) if "ohlc_valid" in group else 0,
                "Volume Nol": int((group["volume"].fillna(0) == 0).sum()),
                "Harga Disesuaikan Berbeda (%)": round(float(adjusted_diff), 1),
                "Jeda > 5 Hari": int((gaps > 5).sum()),
            }
        )

    per_ticker = pd.DataFrame(rows)
    return {
        "rows": int(len(frame)),
        "tickers": int(frame["ticker"].nunique()),
        "date_min": frame["date"].min(),
        "date_max": frame["date"].max(),
        "missing_values": int(
            frame[["open", "high", "low", "close", "adj_close", "volume"]].isna().sum().sum()
        ),
        "duplicate_rows": int(frame.duplicated(subset=["ticker", "date"]).sum()),
        "invalid_ohlc_rows": int((~frame["ohlc_valid"]).sum()) if "ohlc_valid" in frame else 0,
        "zero_volume_rows": int((frame["volume"].fillna(0) == 0).sum()),
        "per_ticker": per_ticker,
    }
