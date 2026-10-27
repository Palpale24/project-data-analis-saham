"""Metrik risiko historis: volatilitas, drawdown, VaR sederhana, dan distribusi return."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from src.config import TRADING_DAYS
from src.stock_analysis import (
    annualized_volatility,
    calculate_daily_returns,
    drawdown_details,
    get_price_series,
    max_drawdown,
)


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """VaR historis satu hari, dinyatakan sebagai potensi kerugian positif (%).

    Contoh: hasil 2,5 berarti 5% hari terburuk historis mengalami kerugian
    minimal sekitar 2,5% dalam satu hari. Ini bukan jaminan masa depan.
    """
    returns = returns.dropna()
    if len(returns) < 20:
        return float("nan")
    if not 0 < confidence < 1:
        raise ValueError("Confidence harus di antara 0 dan 1")
    quantile = returns.quantile(1 - confidence)
    return float(max(0.0, -quantile * 100))


def downside_deviation(returns: pd.Series, periods: int = TRADING_DAYS) -> float:
    returns = returns.dropna()
    if len(returns) < 2:
        return float("nan")
    downside = np.minimum(returns, 0)
    return float(np.sqrt(np.mean(np.square(downside))) * np.sqrt(periods))


def risk_metrics(series: pd.Series) -> dict:
    series = series.dropna().sort_index()
    returns = calculate_daily_returns(series)
    details = drawdown_details(series)
    return {
        "observations": int(len(series)),
        "annualized_volatility": annualized_volatility(returns),
        "downside_deviation": downside_deviation(returns),
        "max_drawdown": max_drawdown(series),
        "max_drawdown_peak": details["peak_date"],
        "max_drawdown_trough": details["trough_date"],
        "max_drawdown_recovery": details["recovery_date"],
        "var_95_daily": historical_var(returns, 0.95),
        "worst_day": float(returns.min()) if not returns.empty else float("nan"),
        "best_day": float(returns.max()) if not returns.empty else float("nan"),
        "negative_day_pct": float((returns < 0).mean()) if not returns.empty else float("nan"),
        "positive_day_pct": float((returns > 0).mean()) if not returns.empty else float("nan"),
        "average_daily_return": float(returns.mean()) if not returns.empty else float("nan"),
    }


def risk_table(
    prices: pd.DataFrame,
    tickers: Iterable[str],
    start=None,
    end=None,
    min_observations: int = 60,
) -> tuple[pd.DataFrame, list[dict]]:
    """Tabel risiko dan daftar ticker yang datanya belum cukup.

    Metrik tidak dihitung jika observasi kurang dari batas agar angka tidak
    terlihat meyakinkan padahal dasarnya tipis.
    """
    rows: list[dict] = []
    skipped: list[dict] = []
    for ticker in tickers:
        series = get_price_series(prices, ticker, start=start, end=end)
        if len(series) < min_observations:
            skipped.append(
                {
                    "ticker": ticker,
                    "observations": int(len(series)),
                    "reason": f"Butuh minimal {min_observations} hari data, tersedia {len(series)}.",
                }
            )
            continue
        metrics = risk_metrics(series)
        rows.append(
            {
                "Ticker": ticker,
                "Observasi": metrics["observations"],
                "Volatilitas Tahunan": metrics["annualized_volatility"],
                "Downside Deviation": metrics["downside_deviation"],
                "Max Drawdown": metrics["max_drawdown"],
                "VaR 95% Harian": metrics["var_95_daily"] / 100,
                "Hari Negatif": metrics["negative_day_pct"],
                "Hari Terburuk": metrics["worst_day"],
                "Hari Terbaik": metrics["best_day"],
                "Puncak Drawdown": metrics["max_drawdown_peak"],
                "Dasar Drawdown": metrics["max_drawdown_trough"],
            }
        )
    return pd.DataFrame(rows), skipped
