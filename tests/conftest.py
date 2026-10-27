"""Fixture data sintetis untuk pengujian tanpa menyentuh data asli."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.data_cleaning import SNAPSHOT_COLUMN_MAP


@pytest.fixture
def sample_prices() -> pd.DataFrame:
    dates = pd.bdate_range("2022-01-03", periods=320)
    rows = []
    for ticker, start, drift, wave in [
        ("AAA.JK", 1_000.0, 0.0008, 0.015),
        ("BBB.JK", 2_000.0, 0.0002, 0.025),
        ("^JKSE", 6_000.0, 0.0003, 0.010),
    ]:
        for index, day in enumerate(dates):
            close = start * (1 + drift) ** index * (1 + wave * np.sin(index / 9))
            adj = close * 0.8
            rows.append(
                {
                    "date": day,
                    "ticker": ticker,
                    "open": close * 0.997,
                    "high": close * 1.015,
                    "low": close * 0.985,
                    "close": close,
                    "adj_close": adj,
                    "volume": 1_000_000 + index * 100,
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture
def sample_tickers() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"ticker": "AAA.JK", "name": "Alpha Andalan", "sector": "Keuangan", "is_benchmark": False},
            {"ticker": "BBB.JK", "name": "Beta Baja", "sector": "Barang Baku", "is_benchmark": False},
            {"ticker": "^JKSE", "name": "IHSG", "sector": "Benchmark", "is_benchmark": True},
        ]
    )


def make_snapshot_row(**overrides) -> dict:
    """Satu baris snapshot dengan seluruh kolom wajib, siap dibersihkan."""
    row = {original: 0 for original in SNAPSHOT_COLUMN_MAP}
    row.update(
        {
            "No": 1,
            "Kode Saham": "AAA",
            "Nama Perusahaan": "Alpha Andalan Tbk.",
            "Remarks": "",
            "Sebelumnya": 990,
            "Open Price": 1_000,
            "Tanggal Perdagangan Terakhir": "23 Okt 2026",
            "First Trade": 1_000,
            "Tertinggi": 1_020,
            "Terendah": 980,
            "Penutupan": 1_000,
            "Selisih": 10,
            "Volume": 1_000_000,
            "Nilai": 1_000_000_000,
            "Frekuensi": 5_000,
            "Index Individual": 100,
            "Offer": 1_005,
            "Offer Volume": 10_000,
            "Bid": 1_000,
            "Bid Volume": 20_000,
            "Listed Shares": 1_000_000_000,
            "Tradeble Shares": 400_000_000,
            "Weight For Index": 1.2,
            "Foreign Sell": 10_000_000,
            "Foreign Buy": 15_000_000,
            "Non Regular Volume": 0,
            "Non Regular Value": 0,
            "Non Regular Frequency": 0,
        }
    )
    row.update(overrides)
    return row


@pytest.fixture
def snapshot_raw() -> pd.DataFrame:
    return pd.DataFrame(
        [
            make_snapshot_row(),
            make_snapshot_row(**{"Kode Saham": "BBB", "Nama Perusahaan": "Beta Baja Tbk."}),
        ]
    )
