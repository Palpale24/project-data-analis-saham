"""Simulasi transaksi saham dengan aturan lot dan biaya yang transparan."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from src.config import LOT_SIZE, INITIAL_CAPITAL


def tick_size(price: float) -> int:
    """Fraksi harga BEI yang umum berlaku (Rp).

    Aturan fraksi dapat berubah. Nilai ini dipakai untuk memberi peringatan,
    bukan untuk mengubah harga transaksi pengguna secara diam-diam.
    """
    if price <= 0:
        raise ValueError("Harga harus lebih dari 0")
    if price < 200:
        return 1
    if price < 500:
        return 2
    if price < 2_000:
        return 5
    if price < 5_000:
        return 10
    return 25


def is_price_on_tick(price: float) -> bool:
    tick = tick_size(price)
    return abs(price / tick - round(price / tick)) < 1e-9


def max_affordable_lots(allocation: float, price: float, buy_fee_pct: float) -> int:
    """Jumlah lot maksimum yang muat dalam alokasi, termasuk biaya beli."""
    if allocation < 0 or price <= 0:
        return 0
    cost_per_lot = price * LOT_SIZE * (1 + buy_fee_pct / 100)
    if cost_per_lot <= 0:
        return 0
    return int(allocation // cost_per_lot)


@dataclass(frozen=True)
class TradeSimulation:
    modal: float
    allocation: float
    unallocated_cash: float
    price: float
    lots: int
    shares: int
    buy_gross: float
    buy_fee_pct: float
    buy_fee: float
    total_buy: float
    allocation_leftover: float
    change_pct: float
    sell_price: float
    sell_gross: float
    sell_fee_pct: float
    sell_fee: float
    tax_pct: float
    tax: float
    total_sell_cost: float
    net_proceeds: float
    gross_profit: float
    net_profit: float
    return_on_investment_pct: float
    return_on_total_capital_pct: float
    ending_capital: float
    max_lots: int

    def to_dict(self) -> dict:
        return asdict(self)


def simulate_trade(
    modal: float = INITIAL_CAPITAL,
    allocation: float = 280_000,
    price: float = 2_500,
    lots: int = 1,
    change_pct: float = 5.0,
    buy_fee_pct: float = 0.15,
    sell_fee_pct: float = 0.15,
    tax_pct: float = 0.10,
) -> TradeSimulation:
    """Hitung hasil satu transaksi beli lalu jual secara simulasi.

    Biaya jual total = komisi jual + pajak penjualan. Pajak penjualan saham
    individu di BEI adalah 0,1% dari nilai bruto penjualan (dapat berubah;
    cek sumber resmi).
    """
    if modal < 0:
        raise ValueError("Modal tidak boleh negatif")
    if allocation < 0:
        raise ValueError("Alokasi tidak boleh negatif")
    if allocation > modal + 0.01:
        raise ValueError("Alokasi investasi tidak boleh melebihi modal")
    if price <= 0:
        raise ValueError("Harga saham harus lebih dari 0")
    if lots < 0 or int(lots) != lots:
        raise ValueError("Jumlah lot harus bilangan bulat dan tidak negatif")
    if change_pct <= -100:
        raise ValueError("Perubahan harga harus lebih besar dari -100%")
    for label, fee in [
        ("Biaya beli", buy_fee_pct),
        ("Biaya jual", sell_fee_pct),
        ("Pajak jual", tax_pct),
    ]:
        if not 0 <= fee <= 100:
            raise ValueError(f"{label} harus di antara 0% dan 100%")

    lots = int(lots)
    shares = lots * LOT_SIZE
    buy_gross = shares * price
    buy_fee = buy_gross * buy_fee_pct / 100
    total_buy = buy_gross + buy_fee
    if total_buy > allocation + 0.01:
        shortfall = total_buy - allocation
        raise ValueError(
            f"Alokasi kurang Rp{shortfall:,.0f}. Kecilkan jumlah lot atau tambah alokasi."
        )

    sell_price = price * (1 + change_pct / 100)
    sell_gross = shares * sell_price
    sell_fee = sell_gross * sell_fee_pct / 100
    tax = sell_gross * tax_pct / 100
    total_sell_cost = sell_fee + tax
    net_proceeds = sell_gross - total_sell_cost
    gross_profit = sell_gross - buy_gross
    net_profit = net_proceeds - total_buy
    return_on_investment = net_profit / total_buy * 100 if total_buy > 0 else 0.0
    return_on_capital = net_profit / modal * 100 if modal > 0 else 0.0
    unallocated_cash = modal - allocation
    allocation_leftover = allocation - total_buy

    return TradeSimulation(
        modal=float(modal),
        allocation=float(allocation),
        unallocated_cash=float(unallocated_cash),
        price=float(price),
        lots=lots,
        shares=int(shares),
        buy_gross=float(buy_gross),
        buy_fee_pct=float(buy_fee_pct),
        buy_fee=float(buy_fee),
        total_buy=float(total_buy),
        allocation_leftover=float(allocation_leftover),
        change_pct=float(change_pct),
        sell_price=float(sell_price),
        sell_gross=float(sell_gross),
        sell_fee_pct=float(sell_fee_pct),
        sell_fee=float(sell_fee),
        tax_pct=float(tax_pct),
        tax=float(tax),
        total_sell_cost=float(total_sell_cost),
        net_proceeds=float(net_proceeds),
        gross_profit=float(gross_profit),
        net_profit=float(net_profit),
        return_on_investment_pct=float(return_on_investment),
        return_on_total_capital_pct=float(return_on_capital),
        ending_capital=float(modal + net_profit),
        max_lots=max_affordable_lots(allocation, price, buy_fee_pct),
    )


def scenario_table(
    modal: float,
    allocation: float,
    price: float,
    lots: int,
    buy_fee_pct: float,
    sell_fee_pct: float,
    tax_pct: float,
    changes: tuple[float, ...] = (-30, -10, -5, 0, 5, 10, 20),
) -> list[dict]:
    rows = []
    for change in changes:
        result = simulate_trade(
            modal=modal,
            allocation=allocation,
            price=price,
            lots=lots,
            change_pct=change,
            buy_fee_pct=buy_fee_pct,
            sell_fee_pct=sell_fee_pct,
            tax_pct=tax_pct,
        )
        rows.append(
            {
                "Perubahan Harga": change,
                "Harga Jual": result.sell_price,
                "Nilai Jual Bruto": result.sell_gross,
                "Biaya Jual + Pajak": result.total_sell_cost,
                "Laba/Rugi Bersih": result.net_profit,
                "Modal Akhir": result.ending_capital,
                "Return Investasi": result.return_on_investment_pct,
            }
        )
    return rows
