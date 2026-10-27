"""Feature engineering untuk data harga saham."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.config import FEATURES_FILE, TRADING_DAYS


def pivot_adjusted_close(prices: pd.DataFrame, price_col: str = "adj_close") -> pd.DataFrame:
    """Ubah data panjang menjadi tabel lebar: baris tanggal, kolom ticker."""
    required = {"date", "ticker", price_col}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Kolom tidak lengkap untuk pivot: {sorted(missing)}")

    frame = prices[["date", "ticker", price_col]].dropna().copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    frame = frame.dropna(subset=["date"]).drop_duplicates(subset=["date", "ticker"], keep="last")
    wide = frame.pivot(index="date", columns="ticker", values=price_col).sort_index()
    return wide.astype(float)


def calculate_daily_returns(wide_prices: pd.DataFrame) -> pd.DataFrame:
    """Return harian sederhana: P_t / P_(t-1) - 1.

    Harga yang hilang tidak diisi otomatis. Perubahan harga lintas hari libur
    tetap dihitung sebagai satu return pada hari perdagangan berikutnya.
    """
    if wide_prices.empty:
        return wide_prices.copy()
    return wide_prices.pct_change(fill_method=None)


def add_moving_average(series: pd.Series, window: int) -> pd.Series:
    """Rata-rata bergerak sederhana; NaN sampai jumlah data mencukupi."""
    if window <= 0:
        raise ValueError("Window moving average harus lebih dari 0")
    return series.rolling(window=window, min_periods=window).mean()


def build_daily_features(prices: pd.DataFrame) -> pd.DataFrame:
    """Buat fitur harian per saham: return, cumulative return, drawdown, MA, volatilitas."""
    required = {"date", "ticker", "adj_close", "close", "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Kolom tidak lengkap untuk fitur: {sorted(missing)}")

    frame = prices.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    frame = frame.dropna(subset=["date", "ticker", "adj_close"]).sort_values(["ticker", "date"])

    outputs: list[pd.DataFrame] = []
    for ticker, group in frame.groupby("ticker", sort=True):
        group = group.drop_duplicates(subset=["date"], keep="last").copy()
        group["daily_return"] = group["adj_close"].pct_change(fill_method=None)
        group["cumulative_return"] = group["adj_close"] / group["adj_close"].iloc[0] - 1
        group["drawdown"] = group["adj_close"] / group["adj_close"].cummax() - 1
        for window in (20, 50, 200):
            group[f"ma_{window}"] = add_moving_average(group["adj_close"], window)
        group["rolling_vol_20"] = (
            group["daily_return"].rolling(20, min_periods=20).std() * np.sqrt(TRADING_DAYS)
        )
        group["ticker"] = ticker
        outputs.append(group)

    if not outputs:
        return pd.DataFrame(
            columns=[
                "date",
                "ticker",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
                "daily_return",
                "cumulative_return",
                "drawdown",
                "ma_20",
                "ma_50",
                "ma_200",
                "rolling_vol_20",
            ]
        )
    return pd.concat(outputs, ignore_index=True)


def save_daily_features(prices: pd.DataFrame, path=FEATURES_FILE) -> pd.DataFrame:
    features = build_daily_features(prices)
    path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(path, index=False)
    return features
