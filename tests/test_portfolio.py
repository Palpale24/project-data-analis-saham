"""Pengujian jurnal paper trading dan perhitungan portofolio virtual."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import pytest

from src.portfolio import (
    append_trade,
    delete_last_trade,
    empty_trades,
    load_trades,
    simulate_portfolio,
    validate_new_trade,
)

TODAY = date.today()


def buy_trade(**overrides) -> dict:
    trade = {
        "date": TODAY,
        "ticker": "AAA.JK",
        "side": "BELI",
        "price": 2_500,
        "lots": 1,
        "fee_pct": 0.15,
        "tax_pct": 0.10,
        "reason": "latihan mencatat transaksi",
        "note": "",
    }
    trade.update(overrides)
    return trade


def sell_trade(**overrides) -> dict:
    trade = buy_trade(side="JUAL")
    trade.update(overrides)
    return trade


def test_load_trades_file_tidak_ada(tmp_path):
    frame = load_trades(tmp_path / "belum_ada.csv")
    assert frame.empty
    assert list(frame.columns) == list(empty_trades().columns)


def test_append_dan_load_trade(tmp_path):
    path = tmp_path / "trades.csv"
    updated = append_trade(buy_trade(), path=path)
    assert len(updated) == 1
    loaded = load_trades(path)
    assert len(loaded) == 1
    assert loaded.iloc[0]["ticker"] == "AAA.JK"
    assert loaded.iloc[0]["side"] == "BELI"
    assert loaded.iloc[0]["lots"] == 1


def test_validasi_menolak_input_tidak_lengkap():
    with pytest.raises(ValueError, match="Kolom wajib"):
        validate_new_trade({"date": TODAY}, empty_trades())


def test_validasi_menolak_alasan_pendek():
    with pytest.raises(ValueError, match="Alasan"):
        validate_new_trade(buy_trade(reason="ok"), empty_trades())


def test_validasi_tanggal_masa_depan():
    with pytest.raises(ValueError, match="masa depan"):
        validate_new_trade(buy_trade(date=TODAY + timedelta(days=1)), empty_trades())


def test_validasi_lot_dan_harga():
    with pytest.raises(ValueError, match="bilangan bulat"):
        validate_new_trade(buy_trade(lots=1.5), empty_trades())
    with pytest.raises(ValueError, match="Harga"):
        validate_new_trade(buy_trade(price=0), empty_trades())
    with pytest.raises(ValueError, match="Jenis transaksi"):
        validate_new_trade(buy_trade(side="HOLD"), empty_trades())


def test_validasi_kas_tidak_cukup():
    with pytest.raises(ValueError, match="kas virtual tidak cukup"):
        validate_new_trade(buy_trade(lots=10), empty_trades())


def test_simulate_portofolio_beli_dan_jual(tmp_path):
    path = tmp_path / "trades.csv"
    append_trade(buy_trade(), path=path)
    result = simulate_portfolio(load_trades(path), {"AAA.JK": 2_500})
    assert result.cash == pytest.approx(449_625)
    assert result.holdings_value == pytest.approx(250_000)
    assert result.equity == pytest.approx(699_625)
    assert result.unrealized_pnl == pytest.approx(-375)
    assert result.total_pnl == pytest.approx(-375)
    assert result.return_pct == pytest.approx(-375 / 700_000 * 100)
    assert len(result.holdings) == 1

    updated = append_trade(sell_trade(price=3_000), path=path)
    result = simulate_portfolio(updated, {"AAA.JK": 3_000})
    assert result.cash == pytest.approx(748_875)
    assert result.holdings_value == pytest.approx(0)
    assert result.equity == pytest.approx(748_875)
    assert result.realized_pnl == pytest.approx(48_875)
    assert result.total_pnl == pytest.approx(48_875)
    assert result.holdings.empty


def test_simulate_portofolio_menolak_jual_melebihi_kepemilikan(tmp_path):
    path = tmp_path / "trades.csv"
    append_trade(buy_trade(), path=path)
    with pytest.raises(ValueError, match="tidak bisa menjual"):
        append_trade(sell_trade(lots=2), path=path)


def test_delete_last_trade(tmp_path):
    path = tmp_path / "trades.csv"
    append_trade(buy_trade(), path=path)
    append_trade(buy_trade(price=2_600, lots=1), path=path)
    remaining = delete_last_trade(path)
    assert len(remaining) == 1
    assert load_trades(path).iloc[0]["price"] == pytest.approx(2_500)


def test_simulate_portofolio_kosong():
    result = simulate_portfolio(empty_trades(), {})
    assert result.cash == pytest.approx(700_000)
    assert result.equity == pytest.approx(700_000)
    assert result.total_pnl == pytest.approx(0)
    assert result.holdings.empty
    assert result.warnings


def test_harga_terakhir_hilang_memakai_harga_transaksi(tmp_path):
    path = tmp_path / "trades.csv"
    append_trade(buy_trade(), path=path)
    result = simulate_portfolio(load_trades(path), {})
    assert result.holdings.iloc[0]["Harga Terakhir"] == pytest.approx(2_500)
    assert result.warnings
