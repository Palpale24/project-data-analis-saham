"""Perhitungan performa saham yang dapat dipakai ulang oleh dashboard dan notebook."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from src.config import TRADING_DAYS
from src.data_loader import get_ticker_prices


def get_price_series(
    prices: pd.DataFrame,
    ticker: str,
    start=None,
    end=None,
    price_col: str = "adj_close",
) -> pd.Series:
    """Ambil seri harga satu ticker dan potong sesuai periode."""
    series = get_ticker_prices(prices, ticker, price_col=price_col)
    if start is not None:
        series = series.loc[series.index >= pd.Timestamp(start)]
    if end is not None:
        series = series.loc[series.index <= pd.Timestamp(end)]
    return series.dropna().sort_index()


def calculate_daily_returns(series: pd.Series) -> pd.Series:
    if series.empty:
        return pd.Series(dtype=float, name="return")
    result = series.pct_change(fill_method=None).dropna()
    result.name = "return"
    return result


def cumulative_return(series: pd.Series) -> float:
    series = series.dropna()
    if len(series) < 2 or series.iloc[0] == 0:
        return float("nan")
    return float(series.iloc[-1] / series.iloc[0] - 1)


def cagr(series: pd.Series) -> float:
    """Compound Annual Growth Rate berdasarkan jumlah tahun kalender."""
    series = series.dropna()
    if len(series) < 2 or series.iloc[0] <= 0:
        return float("nan")
    days = (series.index[-1] - series.index[0]).days
    if days <= 0:
        return float("nan")
    years = days / 365.25
    return float((series.iloc[-1] / series.iloc[0]) ** (1 / years) - 1)


def annualized_volatility(returns: pd.Series, periods: int = TRADING_DAYS) -> float:
    returns = returns.dropna()
    if len(returns) < 2:
        return float("nan")
    return float(returns.std(ddof=1) * np.sqrt(periods))


def drawdown_series(series: pd.Series) -> pd.Series:
    series = series.dropna()
    if series.empty:
        return pd.Series(dtype=float, name="drawdown")
    result = series / series.cummax() - 1
    result.name = "drawdown"
    return result


def max_drawdown(series: pd.Series) -> float:
    drawdown = drawdown_series(series)
    if drawdown.empty:
        return float("nan")
    return float(drawdown.min())


def drawdown_details(series: pd.Series) -> dict:
    """Cari puncak, dasar, dan kedalaman drawdown terbesar."""
    series = series.dropna()
    if len(series) < 2:
        return {
            "max_drawdown": float("nan"),
            "peak_date": None,
            "trough_date": None,
            "recovery_date": None,
            "duration_days": None,
        }

    running_max = series.cummax()
    drawdown = series / running_max - 1
    trough_date = drawdown.idxmin()
    peak_date = series.loc[:trough_date].idxmax()
    peak_value = series.loc[peak_date]
    after_trough = series.loc[trough_date:]
    recovered = after_trough[after_trough >= peak_value]
    recovery_date = recovered.index[0] if not recovered.empty else None
    duration = (trough_date - peak_date).days

    return {
        "max_drawdown": float(drawdown.min()),
        "peak_date": peak_date,
        "trough_date": trough_date,
        "recovery_date": recovery_date,
        "duration_days": int(duration),
    }


def moving_average(series: pd.Series, window: int) -> pd.Series:
    if window <= 0:
        raise ValueError("Window moving average harus lebih dari 0")
    return series.rolling(window=window, min_periods=window).mean()


def normalize_to_100(series: pd.Series) -> pd.Series:
    series = series.dropna()
    if series.empty or series.iloc[0] == 0:
        return pd.Series(dtype=float)
    return series / series.iloc[0] * 100


def summary_metrics(series: pd.Series) -> dict:
    """Ringkasan performa dan risiko untuk satu seri harga yang sudah disesuaikan."""
    series = series.dropna().sort_index()
    if len(series) < 2:
        return {
            "observations": int(len(series)),
            "start_date": series.index.min() if len(series) else None,
            "end_date": series.index.max() if len(series) else None,
            "start_price": float(series.iloc[0]) if len(series) else None,
            "end_price": float(series.iloc[-1]) if len(series) else None,
            "total_return": float("nan"),
            "cagr": float("nan"),
            "annualized_volatility": float("nan"),
            "max_drawdown": float("nan"),
            "best_day": float("nan"),
            "worst_day": float("nan"),
            "positive_day_pct": float("nan"),
            "average_daily_return": float("nan"),
        }

    returns = calculate_daily_returns(series)
    details = drawdown_details(series)
    return {
        "observations": int(len(series)),
        "start_date": series.index.min(),
        "end_date": series.index.max(),
        "start_price": float(series.iloc[0]),
        "end_price": float(series.iloc[-1]),
        "total_return": cumulative_return(series),
        "cagr": cagr(series),
        "annualized_volatility": annualized_volatility(returns),
        "max_drawdown": max_drawdown(series),
        "peak_date": details["peak_date"],
        "trough_date": details["trough_date"],
        "recovery_date": details["recovery_date"],
        "best_day": float(returns.max()) if not returns.empty else float("nan"),
        "worst_day": float(returns.min()) if not returns.empty else float("nan"),
        "positive_day_pct": float((returns > 0).mean()) if not returns.empty else float("nan"),
        "average_daily_return": float(returns.mean()) if not returns.empty else float("nan"),
    }


def prepare_comparison(
    prices: pd.DataFrame,
    tickers: Iterable[str],
    start=None,
    end=None,
    price_col: str = "adj_close",
) -> pd.DataFrame:
    """Tabel harga ternormalisasi (100 di awal periode) untuk perbandingan adil.

    Tanggal awal disamakan ke tanggal pertama ketika semua ticker sudah memiliki
    data, sehingga saham yang baru IPO tidak membuat perbandingan tampak lebih
    baik atau lebih buruk karena periode yang berbeda.
    """
    tickers = [t for t in tickers if t]
    if not tickers:
        return pd.DataFrame()

    series_map: dict[str, pd.Series] = {}
    for ticker in tickers:
        series = get_price_series(prices, ticker, start=start, end=end, price_col=price_col)
        if len(series) >= 2:
            series_map[ticker] = series
    if not series_map:
        return pd.DataFrame()

    common_start = max(series.index.min() for series in series_map.values())
    common_end = min(series.index.max() for series in series_map.values())
    if common_start > common_end:
        return pd.DataFrame()

    result = pd.DataFrame(
        {ticker: series.loc[common_start:common_end] for ticker, series in series_map.items()}
    ).sort_index()
    result = result.dropna(how="all")
    last_valid = result.ffill().iloc[-1]
    result = result.loc[:, last_valid.notna()]
    for column in result.columns:
        first_valid = result[column].first_valid_index()
        if first_valid is None:
            continue
        result[column] = result[column] / result.loc[first_valid, column] * 100
    return result


def performance_table(
    prices: pd.DataFrame,
    tickers: Iterable[str],
    start=None,
    end=None,
) -> pd.DataFrame:
    rows = []
    for ticker in tickers:
        series = get_price_series(prices, ticker, start=start, end=end)
        metrics = summary_metrics(series)
        rows.append(
            {
                "Ticker": ticker,
                "Observasi": metrics["observations"],
                "Awal": metrics["start_date"],
                "Akhir": metrics["end_date"],
                "Total Return": metrics["total_return"],
                "CAGR": metrics["cagr"],
                "Volatilitas Tahunan": metrics["annualized_volatility"],
                "Max Drawdown": metrics["max_drawdown"],
            }
        )
    return pd.DataFrame(rows)


def returns_matrix(
    prices: pd.DataFrame,
    tickers: Iterable[str],
    start=None,
    end=None,
) -> pd.DataFrame:
    """Matriks return harian; hanya memakai harga yang benar-benar tersedia."""
    series_map = {}
    for ticker in tickers:
        series = get_price_series(prices, ticker, start=start, end=end)
        if len(series) >= 2:
            series_map[ticker] = series
    if not series_map:
        return pd.DataFrame()
    wide = pd.DataFrame(series_map).sort_index()
    returns = wide.pct_change(fill_method=None)
    return returns.dropna(how="all")


def correlation_matrix(returns: pd.DataFrame, min_periods: int = 30) -> pd.DataFrame:
    """Korelasi Pearson dengan syarat jumlah pasangan observasi minimum."""
    if returns.empty or returns.shape[1] < 2:
        return pd.DataFrame()
    return returns.corr(method="pearson", min_periods=min_periods)
