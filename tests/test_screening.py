"""Pengujian tabel riset dan penggabungan snapshot IDX."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_cleaning import clean_historical, clean_snapshot
from src.data_loader import load_historical_prices
from src.screening import build_research_table


def test_build_research_table_menggabungkan_snapshot(sample_prices, sample_tickers, snapshot_raw):
    prices = clean_historical(sample_prices)
    snapshot = clean_snapshot(snapshot_raw)
    table = build_research_table(
        prices,
        sample_tickers,
        snapshot=snapshot,
        start=prices["date"].min(),
        end=prices["date"].max(),
        min_observations=60,
    )

    assert len(table) == 2
    assert "AAA" in set(table["Ticker"])
    row = table.loc[table["Ticker"] == "AAA"].iloc[0]
    latest_close = (
        prices.loc[prices["ticker"] == "AAA.JK"].sort_values("date").iloc[-1]["close"]
    )
    assert row["Harga Terakhir"] == pytest.approx(latest_close)
    assert row["Kapitalisasi (Perkiraan)"] == pytest.approx(latest_close * 1_000_000_000)
    assert row["Tradeable/Listed (%)"] == pytest.approx(40.0)
    assert row["Nama"] == "Alpha Andalan Tbk."
    assert row["Sektor"] == "Keuangan"


def test_build_research_table_tanpa_snapshot(sample_prices, sample_tickers):
    prices = clean_historical(sample_prices)
    table = build_research_table(prices, sample_tickers, snapshot=None, min_observations=60)
    assert len(table) == 2
    assert table["Kapitalisasi (Perkiraan)"].isna().all()
    assert table["Tradeable/Listed (%)"].isna().all()


def test_build_research_table_menghormati_min_observasi(sample_prices, sample_tickers):
    prices = clean_historical(sample_prices)
    table = build_research_table(prices, sample_tickers, min_observations=1_000)
    assert table.empty


def test_build_research_table_data_kosong(sample_tickers):
    table = build_research_table(pd.DataFrame(), sample_tickers)
    assert table.empty


def test_build_research_table_pakai_data_asli():
    """Uji integrasi ringan dengan dataset proyek bila tersedia."""
    try:
        prices = clean_historical(load_historical_prices())
    except FileNotFoundError:
        pytest.skip("Dataset historis belum tersedia")
    tickers = pd.read_csv("data/processed/tickers.csv")
    table = build_research_table(prices, tickers, min_observations=60)
    assert len(table) == 12
    assert table["Harga Terakhir"].notna().all()
    assert table["Volatilitas Tahunan"].notna().all()
    assert "GOTO" in set(table["Ticker"])
