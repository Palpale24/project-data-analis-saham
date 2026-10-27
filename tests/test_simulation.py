"""Pengujian aturan lot, fraksi harga, biaya, dan skenario simulasi."""

from __future__ import annotations

import pytest

from src.simulation import (
    is_price_on_tick,
    max_affordable_lots,
    scenario_table,
    simulate_trade,
    tick_size,
)


@pytest.mark.parametrize(
    "price,expected",
    [(1, 1), (199, 1), (200, 2), (499, 2), (500, 5), (1_999, 5), (2_000, 10), (4_999, 10), (5_000, 25)],
)
def test_tick_size(price, expected):
    assert tick_size(price) == expected


def test_tick_size_harga_tidak_valid():
    with pytest.raises(ValueError):
        tick_size(0)


def test_harga_sesuai_fraksi():
    assert is_price_on_tick(250) is True
    assert is_price_on_tick(2_500) is True
    assert is_price_on_tick(2_505) is False
    assert is_price_on_tick(5_025) is True
    assert is_price_on_tick(5_010) is False


def test_max_lots_memperhitungkan_biaya_beli():
    assert max_affordable_lots(280_000, 2_500, 0.15) == 1
    assert max_affordable_lots(250_000, 2_500, 0.15) == 0
    assert max_affordable_lots(500_750, 2_500, 0.15) == 2
    assert max_affordable_lots(0, 2_500, 0.15) == 0
    assert max_affordable_lots(280_000, 0, 0.15) == 0


def test_simulasi_default_rp700000():
    result = simulate_trade()
    assert result.lots == 1
    assert result.shares == 100
    assert result.buy_gross == pytest.approx(250_000)
    assert result.buy_fee == pytest.approx(375)
    assert result.total_buy == pytest.approx(250_375)
    assert result.sell_price == pytest.approx(2_625)
    assert result.sell_gross == pytest.approx(262_500)
    assert result.sell_fee == pytest.approx(393.75)
    assert result.tax == pytest.approx(262.5)
    assert result.net_proceeds == pytest.approx(261_843.75)
    assert result.net_profit == pytest.approx(11_468.75)
    assert result.return_on_investment_pct == pytest.approx(4.580629, abs=1e-5)
    assert result.return_on_total_capital_pct == pytest.approx(1.638393, abs=1e-5)
    assert result.ending_capital == pytest.approx(711_468.75)
    assert result.unallocated_cash == pytest.approx(420_000)
    assert result.allocation_leftover == pytest.approx(29_625)
    assert result.max_lots == 1


def test_simulasi_tanpa_perubahan_harga_tetap_rugi_biaya():
    result = simulate_trade(change_pct=0)
    assert result.gross_profit == pytest.approx(0)
    assert result.net_profit < 0
    assert result.net_profit == pytest.approx(-result.total_buy + result.net_proceeds)


def test_simulasi_menolak_alokasi_kurang():
    with pytest.raises(ValueError, match="Alokasi kurang"):
        simulate_trade(allocation=250_000, lots=1)


def test_simulasi_menolak_input_tidak_valid():
    with pytest.raises(ValueError, match="Alokasi investasi"):
        simulate_trade(modal=100_000, allocation=200_000)
    with pytest.raises(ValueError, match="Harga saham"):
        simulate_trade(price=0)
    with pytest.raises(ValueError, match="bulat"):
        simulate_trade(lots=1.5)
    with pytest.raises(ValueError, match="Perubahan harga"):
        simulate_trade(change_pct=-100)
    with pytest.raises(ValueError, match="Biaya beli"):
        simulate_trade(buy_fee_pct=-1)


def test_scenario_table():
    rows = scenario_table(
        modal=700_000,
        allocation=280_000,
        price=2_500,
        lots=1,
        buy_fee_pct=0.15,
        sell_fee_pct=0.15,
        tax_pct=0.10,
    )
    assert len(rows) == 7
    assert [row["Perubahan Harga"] for row in rows] == [-30, -10, -5, 0, 5, 10, 20]
    assert all(row["Modal Akhir"] < 700_000 for row in rows[:4])
    assert rows[-1]["Modal Akhir"] > 700_000
