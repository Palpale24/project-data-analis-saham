"""Pengujian perhitungan performa, risiko, dan perbandingan."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.risk_analysis import downside_deviation, historical_var, risk_metrics, risk_table
from src.stock_analysis import (
    annualized_volatility,
    calculate_daily_returns,
    cagr,
    correlation_matrix,
    cumulative_return,
    drawdown_details,
    drawdown_series,
    max_drawdown,
    moving_average,
    normalize_to_100,
    performance_table,
    prepare_comparison,
    returns_matrix,
    summary_metrics,
)


def test_return_dan_cagr():
    series = pd.Series([100.0, 110.0, 121.0], index=pd.bdate_range("2023-01-02", periods=3))
    returns = calculate_daily_returns(series)
    assert returns.tolist() == pytest.approx([0.10, 0.10])
    assert cumulative_return(series) == pytest.approx(0.21)

    long_series = pd.Series(
        [100.0, 121.0],
        index=pd.to_datetime(["2020-01-01", "2022-01-01"]),
    )
    days = (long_series.index[1] - long_series.index[0]).days
    expected = (1.21) ** (365.25 / days) - 1
    assert cagr(long_series) == pytest.approx(expected)


def test_cagr_dan_return_kosong():
    assert np.isnan(cumulative_return(pd.Series(dtype=float)))
    assert np.isnan(cagr(pd.Series([100.0])))
    assert np.isnan(cagr(pd.Series([0.0, 100.0])))


def test_volatilitas_return_konstan_nol():
    series = pd.Series([100.0, 101.0, 102.01, 103.0301])
    returns = calculate_daily_returns(series)
    assert annualized_volatility(returns) == pytest.approx(0.0, abs=1e-12)
    assert np.isnan(annualized_volatility(pd.Series(dtype=float)))


def test_drawdown_dan_detail():
    series = pd.Series(
        [100.0, 120.0, 60.0, 90.0, 121.0],
        index=pd.bdate_range("2023-01-02", periods=5),
    )
    drawdown = drawdown_series(series)
    assert drawdown.min() == pytest.approx(-0.5)
    assert max_drawdown(series) == pytest.approx(-0.5)

    details = drawdown_details(series)
    assert details["max_drawdown"] == pytest.approx(-0.5)
    assert details["peak_date"] == series.index[1]
    assert details["trough_date"] == series.index[2]
    assert details["recovery_date"] == series.index[4]


def test_moving_average_dan_normalisasi():
    series = pd.Series([1.0, 2.0, 3.0, 4.0])
    ma = moving_average(series, 2)
    assert np.isnan(ma.iloc[0])
    assert ma.iloc[1] == pytest.approx(1.5)
    assert ma.iloc[3] == pytest.approx(3.5)
    with pytest.raises(ValueError):
        moving_average(series, 0)

    normalized = normalize_to_100(pd.Series([50.0, 100.0]))
    assert normalized.tolist() == pytest.approx([100.0, 200.0])


def test_prepare_comparison_memakai_tanggal_awal_sama(sample_prices):
    comparison = prepare_comparison(sample_prices, ["AAA.JK", "BBB.JK"])
    assert not comparison.empty
    assert comparison.index.min() == max(
        sample_prices.loc[sample_prices["ticker"] == "AAA.JK", "date"].min(),
        sample_prices.loc[sample_prices["ticker"] == "BBB.JK", "date"].min(),
    )
    assert comparison.iloc[0].tolist() == pytest.approx([100.0, 100.0])
    assert comparison.index.is_monotonic_increasing


def test_returns_matrix_dan_korelasi(sample_prices):
    returns = returns_matrix(sample_prices, ["AAA.JK", "BBB.JK", "^JKSE"])
    assert not returns.empty
    assert returns.shape[1] == 3
    assert returns.isna().all().sum() == 0

    corr = correlation_matrix(returns, min_periods=30)
    assert corr.shape == (3, 3)
    assert np.allclose(np.diag(corr), 1.0)
    assert ((corr >= -1) & (corr <= 1)).all().all()
    assert np.allclose(corr, corr.T)


def test_summary_metrics_dan_performance_table(sample_prices):
    series = sample_prices.loc[sample_prices["ticker"] == "AAA.JK"].set_index("date")["adj_close"]
    metrics = summary_metrics(series)
    assert metrics["observations"] == len(series)
    assert metrics["total_return"] == pytest.approx(series.iloc[-1] / series.iloc[0] - 1)
    assert metrics["annualized_volatility"] > 0
    assert metrics["max_drawdown"] <= 0

    table = performance_table(sample_prices, ["AAA.JK", "BBB.JK"])
    assert len(table) == 2
    assert set(table["Ticker"]) == {"AAA.JK", "BBB.JK"}
    assert table["Observasi"].min() == len(series)


def test_risk_metrics_dan_var():
    values = [100.0, 102.0, 99.0, 101.0, 97.0, 98.0] * 5
    series = pd.Series(values, index=pd.bdate_range("2023-01-02", periods=len(values)))
    metrics = risk_metrics(series)
    assert metrics["observations"] == len(values)
    assert metrics["var_95_daily"] >= 0
    assert 0 <= metrics["negative_day_pct"] <= 1
    assert downside_deviation(calculate_daily_returns(series)) >= 0
    assert np.isnan(historical_var(pd.Series([0.01] * 5)))
    with pytest.raises(ValueError):
        historical_var(pd.Series([0.01] * 30), confidence=1.0)


def test_risk_table_melewati_saham_dengan_data_pendek(sample_prices):
    table, skipped = risk_table(
        sample_prices,
        ["AAA.JK", "BBB.JK"],
        min_observations=400,
    )
    assert table.empty
    assert len(skipped) == 2
    assert all("Butuh minimal" in item["reason"] for item in skipped)
