"""Halaman simulasi modal Rp700.000 dengan aturan lot dan biaya."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import INITIAL_CAPITAL, LOT_SIZE
from src.simulation import (
    is_price_on_tick,
    max_affordable_lots,
    scenario_table,
    simulate_trade,
    tick_size,
)
from src.ui import (
    decimal_pct,
    number,
    page_header,
    plotly_style,
    pct,
    rupiah,
    section_heading,
    stat_cards,
)


def _set_lots(value: int) -> None:
    st.session_state["sim_lots"] = int(value)


def render() -> None:
    page_header(
        "Simulasi Modal Rp700.000",
        "Menguji angka sebelum memakai uang nyata. Ini kalkulator, bukan transaksi dan bukan rekomendasi.",
        "Langkah 7 · simulasi",
    )
    st.warning(
        "**Simulasi virtual.** Tidak ada order yang dikirim ke broker. Hasil di sini belum memasukkan "
        "slippage, likuiditas, perubahan aturan, dividen, atau pajak lain. Jangan memakai utang.",
        icon="🧪",
    )

    top_left, top_right = st.columns([2.2, 1.4])
    with top_left:
        modal = st.number_input(
            "Modal awal (Rp)",
            min_value=100_000,
            max_value=1_000_000_000,
            value=INITIAL_CAPITAL,
            step=50_000,
            format="%d",
            help="Nilai awal Rp700.000. Kamu boleh mengubahnya untuk latihan.",
        )
        allocation = st.number_input(
            "Jumlah uang yang dialokasikan ke investasi (Rp)",
            min_value=0,
            max_value=1_000_000_000,
            value=280_000,
            step=10_000,
            format="%d",
            help="Tidak harus seluruh modal. Sisakan dana cadangan.",
        )
        if allocation > modal:
            st.error("Alokasi investasi tidak boleh melebihi modal. Kurangi alokasi terlebih dahulu.")
            return
        st.caption(
            f"Alokasi = **{allocation / modal * 100:.0f}%** dari modal. "
            f"Sisa yang tidak dialokasikan: **{rupiah(modal - allocation)}**."
        )

        with st.expander("Atur estimasi biaya transaksi", expanded=False):
            fee_left, fee_mid, fee_right = st.columns(3)
            with fee_left:
                buy_fee_pct = st.number_input(
                    "Komisi beli (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=0.15,
                    step=0.01,
                    format="%.2f",
                    help="Bervariasi antar sekuritas. Contoh, bukan tarif semua broker.",
                )
            with fee_mid:
                sell_fee_pct = st.number_input(
                    "Komisi jual (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=0.15,
                    step=0.01,
                    format="%.2f",
                    help="Komisi broker saat menjual, sebelum pajak penjualan.",
                )
            with fee_right:
                tax_pct = st.number_input(
                    "Pajak penjualan (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=0.10,
                    step=0.01,
                    format="%.2f",
                    help="Pajak penjualan saham individu umumnya 0,1%. Cek aturan terbaru.",
                )
            st.caption(
                f"Total biaya jual yang dimodelkan: **{sell_fee_pct + tax_pct:.2f}%** "
                f"(komisi {sell_fee_pct:.2f}% + pajak {tax_pct:.2f}%)."
            )

        price = st.number_input(
            "Harga saham simulasi (Rp/lembar)",
            min_value=50,
            max_value=1_000_000,
            value=2_500,
            step=25,
            format="%d",
            help="Harga fiktif untuk latihan. Harga nyata berbeda dan bergerak setiap saat.",
        )
        max_lots = max_affordable_lots(allocation, price, buy_fee_pct)
        lots = st.number_input(
            "Jumlah lot",
            min_value=0,
            max_value=100_000,
            value=1,
            step=1,
            key="sim_lots",
            help=f"1 lot = {LOT_SIZE} lembar. Dengan alokasi saat ini, maksimum sekitar {max_lots} lot.",
        )
        if max_lots > 0 and lots > max_lots:
            st.warning(
                f"Alokasi hanya cukup untuk sekitar **{max_lots} lot**. Kamu memilih {lots} lot; "
                "kurangi lot atau tambah alokasi."
            )
            st.button(
                f"Gunakan {max_lots} lot (maksimum)",
                on_click=_set_lots,
                args=(max_lots,),
            )
        elif max_lots == 0:
            st.warning("Alokasi belum cukup untuk 1 lot pada harga ini.")

        change_pct = st.slider(
            "Perubahan harga saat dijual (%)",
            min_value=-50,
            max_value=50,
            value=5,
            step=1,
            help="Skenario sederhana. Harga nyata bisa bergerak lebih ekstrem.",
        )
    with top_right:
        st.markdown(
            f"""
            <div class="soft-card">
                <div class="stat-label">Ringkasan input</div>
                <div class="stat-value">{lots} lot</div>
                <p>{number(lots * LOT_SIZE)} lembar · harga {rupiah(price)}</p>
                <hr style="border-color:#E2E8F0;">
                <p><strong>Maksimum lot:</strong> {max_lots}</p>
                <p><strong>Nilai 1 lot:</strong> {rupiah(price * LOT_SIZE)}</p>
                <p><strong>Fraksi harga:</strong> Rp{tick_size(price):,.0f}</p>
                <p><strong>Status harga:</strong> {'Sesuai fraksi' if is_price_on_tick(price) else 'Tidak sesuai fraksi'}</p>
            </div>
            """.replace(",", "."),
            unsafe_allow_html=True,
        )
        if not is_price_on_tick(price):
            st.warning(
                "Harga simulasi tidak berada pada fraksi harga BEI yang umum. Simulasi tetap menghitung, "
                "tetapi transaksi nyata harus mengikuti fraksi yang berlaku.",
                icon="⚠️",
            )

    if max_lots == 0 or lots == 0:
        st.info("Isi lot minimal 1 dan pastikan alokasi cukup untuk melihat hasil simulasi.")
        return

    try:
        result = simulate_trade(
            modal=modal,
            allocation=allocation,
            price=price,
            lots=lots,
            change_pct=change_pct,
            buy_fee_pct=buy_fee_pct,
            sell_fee_pct=sell_fee_pct,
            tax_pct=tax_pct,
        )
    except ValueError as exc:
        st.error(str(exc))
        return

    profit_tone = "good" if result.net_profit >= 0 else "bad"
    st.write("")
    stat_cards(
        [
            {
                "label": "Total uang keluar untuk beli",
                "value": rupiah(result.total_buy),
                "note": f"Nilai saham + komisi {buy_fee_pct:.2f}%",
                "tone": "blue",
            },
            {
                "label": "Hasil jual bersih",
                "value": rupiah(result.net_proceeds),
                "note": f"Setelah komisi jual + pajak {sell_fee_pct + tax_pct:.2f}%",
                "tone": "blue",
            },
            {
                "label": "Laba/rugi bersih",
                "value": rupiah(result.net_profit, compact=False),
                "note": f"Return investasi {pct(result.return_on_investment_pct / 100, signed=True)}",
                "tone": profit_tone,
            },
            {
                "label": "Modal akhir",
                "value": rupiah(result.ending_capital),
                "note": f"Return terhadap modal {pct(result.return_on_total_capital_pct / 100, signed=True)}",
                "tone": profit_tone,
            },
        ]
    )
    stat_cards(
        [
            {
                "label": "Uang tidak diinvestasikan",
                "value": rupiah(result.unallocated_cash),
                "note": "Sengaja tidak dipakai membeli saham",
                "tone": "good",
            },
            {
                "label": "Sisa dari alokasi",
                "value": rupiah(result.allocation_leftover),
                "note": "Tidak terpakai setelah biaya beli",
                "tone": "good",
            },
            {
                "label": "Harga jual simulasi",
                "value": rupiah(result.sell_price),
                "note": f"Dari {rupiah(price)} × (1 {change_pct:+.0f}%)",
                "tone": "amber",
            },
            {
                "label": "Total biaya transaksi",
                "value": rupiah(result.buy_fee + result.total_sell_cost),
                "note": "Komisi beli + komisi jual + pajak",
                "tone": "warn",
            },
        ]
    )

    tab_detail, tab_scenario, tab_how = st.tabs(["Rincian", "Skenario Harga", "Cara Kerja"])

    with tab_detail:
        left, right = st.columns(2)
        with left:
            st.markdown(
                f"""
                **Pembelian**
                - Jumlah lot: **{result.lots}** ({number(result.shares)} lembar)
                - Harga beli: **{rupiah(result.price)}**
                - Nilai saham: **{rupiah(result.buy_gross)}**
                - Komisi beli {buy_fee_pct:.2f}%: **{rupiah(result.buy_fee)}**
                - Total beli: **{rupiah(result.total_buy)}**
                """
            )
        with right:
            st.markdown(
                f"""
                **Penjualan**
                - Harga jual: **{rupiah(result.sell_price)}**
                - Nilai jual kotor: **{rupiah(result.sell_gross)}**
                - Komisi jual {sell_fee_pct:.2f}%: **{rupiah(result.sell_fee)}**
                - Pajak jual {tax_pct:.2f}%: **{rupiah(result.tax)}**
                - Hasil bersih: **{rupiah(result.net_proceeds)}**
                """
            )
        st.markdown(
            f"""
            **Laba/rugi**
            - Laba kotor (sebelum biaya): **{rupiah(result.gross_profit)}**
            - Laba/rugi bersih: **{rupiah(result.net_profit)}**
            - Return investasi: **{pct(result.return_on_investment_pct / 100, signed=True)}**
            - Return terhadap total modal: **{pct(result.return_on_total_capital_pct / 100, signed=True)}**
            """
        )

        fig = go.Figure(
            go.Waterfall(
                name="Simulasi",
                orientation="v",
                measure=["relative", "relative", "relative", "relative", "relative", "total"],
                x=["Nilai beli", "Perubahan harga", "Komisi beli", "Komisi jual", "Pajak jual", "Laba/rugi bersih"],
                y=[
                    -result.buy_gross,
                    result.gross_profit,
                    -result.buy_fee,
                    -result.sell_fee,
                    -result.tax,
                    result.net_profit,
                ],
                text=[
                    rupiah(-result.buy_gross, compact=True),
                    rupiah(result.gross_profit, compact=True),
                    rupiah(-result.buy_fee, compact=True),
                    rupiah(-result.sell_fee, compact=True),
                    rupiah(-result.tax, compact=True),
                    rupiah(result.net_profit, compact=True),
                ],
                textposition="outside",
                connector=dict(line=dict(color="#94A3B8")),
                decreasing=dict(marker=dict(color="#B91C1C")),
                increasing=dict(marker=dict(color="#0F766E")),
                totals=dict(marker=dict(color="#0B1F33")),
                hovertemplate="%{x}<br>%{text}<extra></extra>",
            )
        )
        plotly_style(fig, "Dari Nilai Beli ke Laba/Rugi Bersih", "", "Rupiah", height=420, show_legend=False)
        fig.update_yaxes(tickprefix="Rp", tickformat=",.0f")
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption(
            "Waterfall memecah laba/rugi bersih. Perubahan harga bisa positif atau negatif; komisi dan pajak selalu mengurangi hasil."
        )

    with tab_scenario:
        section_heading("Skenario perubahan harga", "Semua baris memakai lot, harga, dan biaya yang sama; hanya harga jual yang berubah.")
        rows = scenario_table(
            modal=modal,
            allocation=allocation,
            price=price,
            lots=lots,
            buy_fee_pct=buy_fee_pct,
            sell_fee_pct=sell_fee_pct,
            tax_pct=tax_pct,
        )
        display = pd.DataFrame(rows)
        display["Perubahan Harga"] = display["Perubahan Harga"].map(lambda v: f"{v:+.0f}%")
        display["Harga Jual"] = display["Harga Jual"].map(rupiah)
        display["Nilai Jual Bruto"] = display["Nilai Jual Bruto"].map(rupiah)
        display["Biaya Jual + Pajak"] = display["Biaya Jual + Pajak"].map(rupiah)
        display["Laba/Rugi Bersih"] = display["Laba/Rugi Bersih"].map(rupiah)
        display["Modal Akhir"] = display["Modal Akhir"].map(rupiah)
        display["Return Investasi"] = display["Return Investasi"].map(lambda v: decimal_pct(v, signed=True))
        display.columns = [
            "Perubahan Harga",
            "Harga Jual",
            "Nilai Jual Bruto",
            "Biaya Jual + Pajak",
            "Laba/Rugi Bersih",
            "Modal Akhir",
            "Return Investasi",
        ]
        st.dataframe(display, width="stretch", hide_index=True)
        st.caption(
            "Skenario ini tidak memasukkan slippage, perubahan spread, atau kesulitan likuiditas. "
            "Angka ekstrem seperti -50% bisa terjadi pada saham berisiko tinggi."
        )

    with tab_how:
        st.markdown(
            f"""
            ### Aturan yang dipakai

            - **1 lot = {LOT_SIZE} lembar.** Ini aturan BEI yang berlaku saat proyek dibuat; periksa kembali
              sumber resmi jika ada perubahan.
            - **Fraksi harga** pada harga {rupiah(price)} adalah Rp{tick_size(price):,.0f}. Harga transaksi
              nyata harus berada pada fraksi yang berlaku. Aplikasi tidak membulatkan harga secara diam-diam.
            - **Komisi beli** = nilai saham × persentase komisi beli.
            - **Komisi jual** = nilai jual × persentase komisi jual.
            - **Pajak jual** = nilai jual × persentase pajak (umumnya 0,1% untuk saham individu).
            - **Laba bersih** = hasil jual bersih − total beli.

            ### Yang tidak dimodelkan

            - slippage (harga berubah saat order dieksekusi);
            - spread bid-ask dan antrean order;
            - likuiditas dan partial fill;
            - dividen, stock split, dan pajak dividen;
            - batas auto-reject, perubahan fraksi, dan biaya broker lain;
            - kondisi pasar yang ekstrem.

            ### Kenapa tidak seluruh Rp700.000?

            Karena saham bisa turun dan uang cadangan melindungi kebutuhan. Simulasi ini sengaja memisahkan
            **uang yang diinvestasikan**, **sisa alokasi**, dan **uang yang tidak dialokasikan**. Kehilangan
            100% pada saham hanya menghabiskan bagian yang diinvestasikan, bukan seluruh modal.

            Sumber acuan: [IDX RDIS tentang lot](https://rdis.idx.co.id/id/events/mengenai-satuan-lot-apa-itu-lot),
            [IDX Perpajakan](https://www.idx.co.id/id/investhub/perpajakan/),
            [pengumuman fraksi harga IDX](https://www.idx.co.id/en/news/press-release/518).
            Periksa kembali aturan terbaru sebelum bertransaksi.
            """
        )
