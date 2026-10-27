"""Halaman paper trading dan jurnal investasi virtual."""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.cached_data import get_prices
from src.config import INITIAL_CAPITAL, LOT_SIZE, ticker_label, ticker_name
from src.data_loader import DataNotFoundError, latest_close_prices
from src.pages.common import format_ticker_option, stock_options
from src.portfolio import (
    append_trade,
    delete_last_trade,
    load_trades,
    simulate_portfolio,
)
from src.ui import (
    date_label,
    empty_state,
    page_header,
    pct,
    rupiah,
    section_heading,
    stat_cards,
)


def _format_holdings(holdings: pd.DataFrame) -> pd.DataFrame:
    display = holdings.copy()
    if display.empty:
        return display
    display["Ticker"] = display["Ticker"].map(ticker_label)
    for column in ["Harga Rata-rata", "Harga Terakhir", "Nilai Pasar", "Laba/Rugi Belum Terealisasi"]:
        display[column] = display[column].map(rupiah)
    display["Return (%)"] = display["Return (%)"].map(lambda value: f"{value:+.2f}%".replace(".", ","))
    display.columns = [
        "Ticker",
        "Saham",
        "Lot",
        "Harga Rata-rata",
        "Harga Terakhir",
        "Nilai Pasar",
        "Laba/Rugi Belum Terealisasi",
        "Return",
    ]
    return display


def _format_ledger(ledger: pd.DataFrame) -> pd.DataFrame:
    display = ledger.copy()
    if display.empty:
        return display
    display["Tanggal"] = display["Tanggal"].map(date_label)
    display["Ticker"] = display["Ticker"].map(ticker_label)
    for column in ["Harga", "Nilai Bruto", "Biaya", "Arus Kas", "Kas Setelah", "Laba/Rugi Terealisasi"]:
        display[column] = display[column].map(rupiah)
    display.columns = [
        "Tanggal",
        "Ticker",
        "Aksi",
        "Lot",
        "Saham",
        "Harga",
        "Nilai Bruto",
        "Biaya",
        "Arus Kas",
        "Kas Setelah",
        "Laba/Rugi Terealisasi",
    ]
    return display


def _format_journal(trades: pd.DataFrame) -> pd.DataFrame:
    display = trades.copy()
    if display.empty:
        return display
    display["date"] = display["date"].map(date_label)
    display["ticker"] = display["ticker"].map(ticker_label)
    display["price"] = display["price"].map(rupiah)
    display["lots"] = display["lots"].map(lambda value: f"{int(value)} lot")
    display["fee_pct"] = display["fee_pct"].map(lambda value: f"{value:.2f}%".replace(".", ","))
    display["tax_pct"] = display["tax_pct"].map(lambda value: f"{value:.2f}%".replace(".", ","))
    display = display[["date", "ticker", "side", "price", "lots", "fee_pct", "tax_pct", "reason", "note"]]
    display.columns = ["Tanggal", "Ticker", "Aksi", "Harga", "Jumlah", "Komisi", "Pajak", "Alasan", "Catatan Evaluasi"]
    return display


def render() -> None:
    page_header(
        "Paper Trading & Jurnal",
        "Mencatat transaksi virtual beserta alasan dan evaluasi. Tidak ada koneksi broker, tidak ada uang nyata.",
        "Langkah 8 · paper trading",
    )
    st.warning(
        "**Semua transaksi di halaman ini virtual.** Modal awal virtual Rp700.000. Data disimpan di "
        "`data/user/paper_trades.csv` di komputer ini. Jangan menganggap hasil virtual sebagai bukti kemampuan "
        "bertransaksi nyata.",
        icon="📝",
    )

    try:
        prices = get_prices()
        latest = latest_close_prices(prices)
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Data harga historis belum siap: {exc}")
        return

    trades = load_trades()
    try:
        portfolio = simulate_portfolio(trades, latest, initial_cash=INITIAL_CAPITAL)
    except ValueError as exc:
        st.error(f"Jurnal transaksi tidak konsisten: {exc}")
        return

    if st.session_state.get("trade_success"):
        st.success(st.session_state.pop("trade_success"), icon="✅")

    section_heading("Tambah transaksi virtual", "Harga di sini adalah harga simulasi, bukan harga real-time dari broker.")
    options = stock_options(prices)
    with st.form("paper_trade_form", clear_on_submit=False):
        row1 = st.columns([1.1, 1.3, 0.8, 1.0, 0.8])
        with row1[0]:
            trade_date = st.date_input("Tanggal", value=date.today(), max_value=date.today(), key="trade_date")
        with row1[1]:
            ticker = st.selectbox("Saham", options, format_func=format_ticker_option, key="trade_ticker")
        with row1[2]:
            side = st.selectbox("Aksi", ["BELI", "JUAL"], key="trade_side")
        with row1[3]:
            price = st.number_input("Harga simulasi (Rp)", min_value=50, value=2_500, step=25, format="%d", key="trade_price")
        with row1[4]:
            lots = st.number_input("Lot", min_value=1, max_value=100_000, value=1, step=1, key="trade_lots")

        row2 = st.columns([0.8, 0.8, 2.4])
        with row2[0]:
            fee_pct = st.number_input("Komisi (%)", min_value=0.0, max_value=5.0, value=0.15, step=0.01, format="%.2f", key="trade_fee")
        with row2[1]:
            tax_pct = st.number_input("Pajak jual (%)", min_value=0.0, max_value=5.0, value=0.10, step=0.01, format="%.2f", key="trade_tax")
        with row2[2]:
            reason = st.text_input("Alasan transaksi", placeholder="Contoh: latihan diversifikasi; dana cadangan sudah dipisah", key="trade_reason")
        note = st.text_area(
            "Catatan evaluasi (opsional)",
            placeholder="Apa yang ingin dievaluasi nanti? Apa yang bisa membuat tesis berubah?",
            key="trade_note",
            height=80,
        )
        submitted = st.form_submit_button("Simpan transaksi virtual", type="primary", width="stretch")

    if submitted:
        try:
            append_trade(
                {
                    "date": trade_date,
                    "ticker": ticker,
                    "side": side,
                    "price": price,
                    "lots": lots,
                    "fee_pct": fee_pct,
                    "tax_pct": tax_pct,
                    "reason": reason,
                    "note": note,
                }
            )
            st.session_state["trade_success"] = "Transaksi virtual tersimpan di jurnal lokal."
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))

    st.caption(
        "Harga acuan terakhir dari dataset historis (bukan real-time): "
        + " · ".join(
            f"{ticker_label(t)} {rupiah(latest[t])}"
            for t in ["BBCA.JK", "TLKM.JK", "ANTM.JK"]
            if t in latest
        )
    )

    section_heading("Ringkasan portofolio virtual", "Valuasi memakai harga penutupan terakhir yang tersedia di dataset.")
    stat_cards(
        [
            {"label": "Kas virtual", "value": rupiah(portfolio.cash), "note": "Sisa uang tunai virtual", "tone": "blue"},
            {"label": "Nilai saham", "value": rupiah(portfolio.holdings_value), "note": "Harga terakhir dataset", "tone": ""},
            {"label": "Total ekuitas", "value": rupiah(portfolio.equity), "note": f"Awal {rupiah(portfolio.initial_cash)}", "tone": "good"},
            {
                "label": "Laba/rugi total",
                "value": rupiah(portfolio.total_pnl),
                "note": f"Return {pct(portfolio.return_pct / 100, signed=True)}",
                "tone": "good" if portfolio.total_pnl >= 0 else "bad",
            },
            {
                "label": "Terealisasi",
                "value": rupiah(portfolio.realized_pnl),
                "note": "Dari transaksi jual",
                "tone": "good" if portfolio.realized_pnl >= 0 else "bad",
            },
            {
                "label": "Belum terealisasi",
                "value": rupiah(portfolio.unrealized_pnl),
                "note": "Perubahan nilai saham yang masih dipegang",
                "tone": "good" if portfolio.unrealized_pnl >= 0 else "bad",
            },
        ],
        per_row=3,
    )

    if trades.empty:
        empty_state(
            "Belum ada transaksi virtual",
            "Mulai dengan satu transaksi kecil, tulis alasan yang spesifik, lalu evaluasi prosesnya. "
            "Jangan mengubah modal virtual seenaknya agar hasil terlihat bagus.",
            icon="📒",
        )
        st.markdown(
            """
            **Saran latihan pertama:** catat pembelian 1 lot saham dengan harga simulasi Rp2.500, alasan
            "latihan mencatat transaksi dan menghitung biaya", lalu tambahkan catatan evaluasi.
            """
        )
    else:
        tab_portfolio, tab_history, tab_manage = st.tabs(["Portofolio", "Riwayat & Jurnal", "Kelola Jurnal"])
        with tab_portfolio:
            if portfolio.holdings.empty:
                st.info("Tidak ada saham yang sedang dipegang. Semua posisi sudah dijual atau belum ada pembelian.")
            else:
                st.dataframe(_format_holdings(portfolio.holdings), width="stretch", hide_index=True)
            st.markdown("### Buku besar transaksi")
            if portfolio.ledger.empty:
                st.info("Belum ada transaksi.")
            else:
                st.dataframe(_format_ledger(portfolio.ledger), width="stretch", hide_index=True)
            for warning in portfolio.warnings:
                st.warning(warning)
            st.caption(
                "Metode harga rata-rata: biaya beli (termasuk komisi) dibagi jumlah lembar. "
                "Keuntungan terealisasi dihitung setelah komisi jual dan pajak."
            )

        with tab_history:
            st.dataframe(_format_journal(trades), width="stretch", hide_index=True)
            st.download_button(
                "Unduh jurnal (CSV)",
                data=trades.to_csv(index=False).encode("utf-8"),
                file_name="paper_trades.csv",
                mime="text/csv",
            )
            st.caption(
                "Jurnal memuat alasan dan catatan evaluasi. Bacalah kembali sebelum mengevaluasi hasil, "
                "agar tidak terkena hindsight bias."
            )

        with tab_manage:
            st.warning(
                "Menghapus transaksi terakhir mengubah kas dan posisi virtual. Gunakan hanya untuk memperbaiki "
                "kesalahan pencatatan. Tindakan ini tidak bisa dibatalkan dari aplikasi.",
                icon="⚠️",
            )
            confirm = st.checkbox("Saya yakin ingin menghapus transaksi terakhir", key="confirm_delete_trade")
            if st.button("Hapus transaksi terakhir", disabled=not confirm, type="secondary"):
                try:
                    delete_last_trade()
                    st.session_state["trade_success"] = "Transaksi terakhir dihapus dari jurnal virtual."
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Gagal menghapus: {exc}")
