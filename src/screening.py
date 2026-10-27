"""Tabel riset saham berbasis metrik yang tersedia.

Tidak ada skor 'pasti bagus' atau rekomendasi beli. Tabel hanya merangkum
metrik historis dan data snapshot agar pengguna bisa menyaring sendiri.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import ticker_label
from src.stock_analysis import get_price_series, summary_metrics


def build_research_table(
    prices: pd.DataFrame,
    tickers: pd.DataFrame,
    snapshot: pd.DataFrame | None = None,
    start=None,
    end=None,
    min_observations: int = 120,
) -> pd.DataFrame:
    if prices.empty:
        return pd.DataFrame()

    if tickers is None or tickers.empty:
        universe = [
            {"ticker": t, "name": t, "sector": "Lainnya"}
            for t in sorted(prices["ticker"].unique())
            if t != "^JKSE"
        ]
        tickers = pd.DataFrame(universe)

    tickers = tickers.loc[~tickers["ticker"].astype(str).str.startswith("^")].copy()
    snapshot_index = None
    if snapshot is not None and not snapshot.empty:
        snapshot_view = snapshot.drop_duplicates("ticker").copy()
        snapshot_codes = snapshot_view["ticker"].astype(str).str.upper().str.strip()
        # Snapshot IDX memakai kode tanpa sufiks .JK; samakan dengan ticker historis.
        snapshot_view["ticker_full"] = snapshot_codes.where(
            snapshot_codes.str.endswith(".JK"), snapshot_codes + ".JK"
        )
        snapshot_index = snapshot_view.set_index("ticker_full")
    all_dates = prices["date"].nunique()

    rows = []
    for _, info in tickers.iterrows():
        ticker = str(info["ticker"])
        series = get_price_series(prices, ticker, start=start, end=end)
        if len(series) < min_observations:
            continue
        metrics = summary_metrics(series)
        last_12m = series.loc[series.index >= series.index.max() - pd.Timedelta(days=365)]
        return_1y = (
            float(last_12m.iloc[-1] / last_12m.iloc[0] - 1) if len(last_12m) >= 2 else np.nan
        )
        raw = prices.loc[(prices["ticker"] == ticker) & (prices["date"] >= series.index.min())].copy()
        raw = raw.loc[raw["date"] <= series.index.max()].sort_values("date")
        last_20 = raw.tail(20)
        liquidity = float((last_20["close"] * last_20["volume"]).mean()) if not last_20.empty else np.nan
        # Harga terakhir dan kapitalisasi memakai harga biasa (bukan adjusted),
        # karena harga adjusted bukan harga yang tertera di papan bursa saat ini.
        latest_close = float(raw["close"].iloc[-1]) if not raw.empty else float(series.iloc[-1])

        company_name = str(info.get("name", ticker))
        sector = str(info.get("sector", "Lainnya"))
        listed_shares = np.nan
        tradeable_pct = np.nan
        if snapshot_index is not None and ticker in snapshot_index.index:
            snap = snapshot_index.loc[ticker]
            company_name = str(snap.get("company_name", company_name))
            listed_shares = float(snap.get("listed_shares", np.nan))
            tradeable_pct = float(snap.get("tradeable_pct", np.nan))
        market_cap = float(latest_close * listed_shares) if pd.notna(listed_shares) else np.nan

        rows.append(
            {
                "Ticker": ticker_label(ticker),
                "Kode Lengkap": ticker,
                "Nama": company_name,
                "Sektor": sector,
                "Harga Terakhir": latest_close,
                "Return 1 Tahun": return_1y,
                "Return Periode": metrics["total_return"],
                "CAGR": metrics["cagr"],
                "Volatilitas Tahunan": metrics["annualized_volatility"],
                "Max Drawdown": metrics["max_drawdown"],
                "Nilai Transaksi 20H": liquidity,
                "Kapitalisasi (Perkiraan)": market_cap,
                "Tradeable/Listed (%)": tradeable_pct,
                "Observasi": metrics["observations"],
                "Kelengkapan (%)": round(metrics["observations"] / all_dates * 100, 1)
                if all_dates
                else np.nan,
            }
        )
    return pd.DataFrame(rows)
