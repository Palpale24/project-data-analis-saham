"""Pengujian pembersihan data snapshot dan historis."""

from __future__ import annotations

import pandas as pd
import pytest

from src.data_cleaning import (
    clean_historical,
    clean_snapshot,
    historical_quality_report,
    parse_indonesian_date,
    snapshot_quality_report,
    validate_ohlc,
)
from tests.conftest import make_snapshot_row


def test_parse_indonesian_date_berbagai_format():
    assert parse_indonesian_date("23 Okt 2026") == pd.Timestamp("2026-10-23")
    assert parse_indonesian_date("1 Mei 2024") == pd.Timestamp("2024-05-01")
    assert parse_indonesian_date("2026-10-23") == pd.Timestamp("2026-10-23")
    assert pd.isna(parse_indonesian_date("tanggal tidak jelas"))
    assert pd.isna(parse_indonesian_date(None))


def test_validate_ohlc_menerima_open_nol_jika_tidak_tersedia():
    frame = pd.DataFrame(
        {
            "open": [0, 100, 100, 100],
            "high": [110, 110, 110, 90],
            "low": [90, 90, 120, 80],
            "close": [100, 100, 100, 100],
            "volume": [1_000, 1_000, 1_000, 0],
        }
    )
    result = validate_ohlc(frame)
    assert bool(result.iloc[0]) is True  # open tidak tersedia
    assert bool(result.iloc[1]) is True
    assert bool(result.iloc[2]) is False  # high < low
    assert bool(result.iloc[3]) is True  # tidak diperdagangkan, tidak dipaksa valid


def test_clean_snapshot_menghapus_duplikat_dan_menghitung_kolom_turunan(snapshot_raw):
    duplicate = pd.concat([snapshot_raw, snapshot_raw.iloc[[0]]], ignore_index=True)
    clean = clean_snapshot(duplicate)

    assert len(clean) == 2
    assert clean["ticker"].tolist() == ["AAA", "BBB"]
    row = clean.loc[clean["ticker"] == "AAA"].iloc[0]
    assert row["last_trade_date"] == pd.Timestamp("2026-10-23")
    assert row["market_cap"] == 1_000 * 1_000_000_000
    assert row["foreign_net"] == 5_000_000
    assert row["tradeable_pct"] == pytest.approx(40.0)
    assert bool(row["traded"]) is True


def test_clean_snapshot_menolak_kolom_hilang():
    with pytest.raises(ValueError, match="Kolom snapshot tidak lengkap"):
        clean_snapshot(pd.DataFrame({"Kode Saham": ["AAA"]}))


def test_snapshot_quality_report(snapshot_raw):
    raw = snapshot_raw.copy()
    raw.loc[0, "Open Price"] = 0
    raw.loc[1, "Volume"] = 0
    clean = clean_snapshot(raw)
    report = snapshot_quality_report(raw, clean)

    assert report["rows"] == 2
    assert report["unique_tickers"] == 2
    assert report["date_count"] == 1
    assert report["single_date"] is True
    assert report["no_trade_rows"] == 1
    assert report["zero_open_traded_rows"] == 1
    assert report["invalid_ohlc_rows"] == 0
    assert report["missing_values"] == 0
    assert any("satu tanggal" in warning for warning in report["warnings"])


def test_clean_historical_menghapus_harga_tidak_valid_dan_duplikat(sample_prices):
    frame = sample_prices.copy()
    frame.loc[0, "close"] = 0
    frame = pd.concat([frame, sample_prices.iloc[[1]]], ignore_index=True)
    clean = clean_historical(frame)

    assert (clean["close"] > 0).all()
    assert (clean["adj_close"] > 0).all()
    assert not clean.duplicated(subset=["ticker", "date"]).any()
    assert clean["date"].dtype.kind == "M"
    assert set(clean.columns) >= {"ohlc_valid"}


def test_historical_quality_report(sample_prices):
    frame = clean_historical(sample_prices)
    report = historical_quality_report(frame)

    assert report["rows"] == len(frame)
    assert report["tickers"] == 3
    assert report["missing_values"] == 0
    assert report["duplicate_rows"] == 0
    assert report["invalid_ohlc_rows"] == 0
    assert report["date_min"] <= report["date_max"]
    per_ticker = report["per_ticker"]
    assert set(per_ticker["Ticker"]) == {"AAA.JK", "BBB.JK", "^JKSE"}
    assert per_ticker["Kelengkapan (%)"].max() == pytest.approx(100.0)


def test_historical_quality_report_kosong():
    report = historical_quality_report(pd.DataFrame())
    assert report["rows"] == 0
    assert report["tickers"] == 0
    assert report["per_ticker"].empty


def test_make_snapshot_row_valid():
    row = make_snapshot_row()
    clean = clean_snapshot(pd.DataFrame([row]))
    assert clean.iloc[0]["ohlc_valid"] is True or bool(clean.iloc[0]["ohlc_valid"]) is True
