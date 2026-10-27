"""Halaman riset saham: tabel metrik historis dan detail per saham.

Halaman ini sengaja tidak memberi skor gabungan atau label "pasti bagus".
Semua angka berasal dari data yang tersedia dan filter bersifat transparan.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import get_prices, get_snapshot, get_tickers
from src.config import BENCHMARK_TICKER, ticker_label, ticker_name
from src.data_loader import DataNotFoundError
from src.pages.common import (
    date_range_caption,
    format_ticker_option,
    render_period_controls,
)
from src.screening import build_research_table
from src.stock_analysis import (
    get_price_series,
    prepare_comparison,
    summary_metrics,
)
from src.ui import (
    badge,
    date_label,
    decimal_pct,
    number,
    page_header,
    plotly_style,
    pct,
    rupiah,
    section_heading,
    stat_cards,
)

SORT_OPTIONS = {
    "Return periode (tertinggi)": ("Return Periode", False),
    "CAGR (tertinggi)": ("CAGR", False),
    "Volatilitas (terendah)": ("Volatilitas Tahunan", True),
    "Max drawdown (paling dangkal)": ("Max Drawdown", False),
    "Nilai transaksi 20H (terbesar)": ("Nilai Transaksi 20H", False),
    "Nama perusahaan (A–Z)": ("Nama", True),
    "Kode saham (A–Z)": ("Ticker", True),
}


def _format_table(frame: pd.DataFrame) -> pd.DataFrame:
    display = frame[
        [
            "Ticker",
            "Nama",
            "Sektor",
            "Harga Terakhir",
            "Return 1 Tahun",
            "Return Periode",
            "CAGR",
            "Volatilitas Tahunan",
            "Max Drawdown",
            "Nilai Transaksi 20H",
            "Kapitalisasi (Perkiraan)",
            "Tradeable/Listed (%)",
        ]
    ].copy()
    display["Harga Terakhir"] = display["Harga Terakhir"].map(rupiah)
    for column in ["Return 1 Tahun", "Return Periode", "CAGR", "Max Drawdown"]:
        display[column] = display[column].map(lambda value: pct(value, signed=True))
    display["Volatilitas Tahunan"] = display["Volatilitas Tahunan"].map(pct)
    display["Nilai Transaksi 20H"] = display["Nilai Transaksi 20H"].map(
        lambda value: rupiah(value, compact=True)
    )
    display["Kapitalisasi (Perkiraan)"] = display["Kapitalisasi (Perkiraan)"].map(
        lambda value: rupiah(value, compact=True)
    )
    display["Tradeable/Listed (%)"] = display["Tradeable/Listed (%)"].map(decimal_pct)
    display.columns = [
        "Kode",
        "Nama",
        "Sektor",
        "Harga Terakhir",
        "Return 1 Thn",
        "Return Periode",
        "CAGR",
        "Volatilitas",
        "Max Drawdown",
        "Likuiditas 20H",
        "Kapitalisasi",
        "Tradeable/Listed",
    ]
    return display


def _detail_chart(prices: pd.DataFrame, ticker: str, start, end) -> None:
    tickers = [ticker]
    if ticker != BENCHMARK_TICKER:
        tickers.append(BENCHMARK_TICKER)
    comparison = prepare_comparison(prices, tickers, start=start, end=end)
    if comparison.empty:
        st.info("Data historis belum cukup untuk menggambar perbandingan pada periode ini.")
        return

    fig = go.Figure()
    for index, column in enumerate(comparison.columns):
        fig.add_trace(
            go.Scatter(
                x=comparison.index,
                y=comparison[column],
                mode="lines",
                name=f"{ticker_label(column)} — {ticker_name(column)}",
                line=dict(width=2.2 if column == ticker else 1.5, color=["#0F766E", "#94A3B8", "#2563EB"][index % 3]),
                hovertemplate=f"{ticker_label(column)}<br>%{{x|%d %b %Y}}<br>Indeks: %{{y:.1f}}<extra></extra>",
            )
        )
    fig.add_hline(y=100, line_dash="dot", line_color="#94A3B8", annotation_text="Awal = 100")
    plotly_style(
        fig,
        f"Perjalanan {ticker_label(ticker)} vs IHSG (awal = 100)",
        "Tanggal",
        "Indeks (awal = 100)",
        height=430,
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption(date_range_caption(comparison.index.min(), comparison.index.max()))


def _detail_view(prices: pd.DataFrame, table: pd.DataFrame, snapshot: pd.DataFrame | None, start, end) -> None:
    options = list(table["Kode Lengkap"])
    if not options:
        return
    selected = st.selectbox(
        "Pilih saham untuk dilihat lebih dekat",
        options,
        format_func=format_ticker_option,
        key="research_detail_ticker",
    )
    metrics = summary_metrics(get_price_series(prices, selected, start=start, end=end))
    row = table.loc[table["Kode Lengkap"] == selected].iloc[0]

    stat_cards(
        [
            {
                "label": "Harga terakhir",
                "value": rupiah(row["Harga Terakhir"]),
                "note": "Harga penutupan biasa dari dataset",
                "tone": "blue",
            },
            {
                "label": "Total return periode",
                "value": pct(metrics["total_return"], signed=True),
                "note": "Harga adjusted, bukan prediksi",
                "tone": "good" if (metrics["total_return"] or 0) >= 0 else "bad",
            },
            {
                "label": "CAGR",
                "value": pct(metrics["cagr"], signed=True),
                "note": "Pertumbuhan tahunan majemuk",
                "tone": "blue",
            },
            {
                "label": "Volatilitas tahunan",
                "value": pct(metrics["annualized_volatility"]),
                "note": "Semakin tinggi, semakin liar",
                "tone": "warn",
            },
        ]
    )
    stat_cards(
        [
            {
                "label": "Maximum drawdown",
                "value": pct(metrics["max_drawdown"], signed=True),
                "note": f"Puncak {date_label(metrics.get('peak_date'))} → dasar {date_label(metrics.get('trough_date'))}",
                "tone": "bad",
            },
            {
                "label": "Hari negatif",
                "value": pct(1 - metrics["positive_day_pct"])
                if pd.notna(metrics["positive_day_pct"])
                else "—",
                "note": f"Dari {number(metrics['observations'])} hari return",
                "tone": "amber",
            },
            {
                "label": "Hari terburuk",
                "value": pct(metrics["worst_day"], signed=True),
                "note": f"Hari terbaik {pct(metrics['best_day'], signed=True)}",
                "tone": "bad",
            },
            {
                "label": "Observasi",
                "value": number(metrics["observations"]),
                "note": "Jumlah harga yang dipakai",
                "tone": "",
            },
        ]
    )
    _detail_chart(prices, selected, start, end)

    if snapshot is not None and not snapshot.empty:
        code = selected.replace(".JK", "")
        snap = snapshot.loc[snapshot["ticker"].astype(str).str.upper() == code]
        if not snap.empty:
            snap = snap.iloc[0]
            section_heading(
                "Potret snapshot IDX",
                "Hanya satu hari. Jangan memakai baris ini untuk menghitung tren atau risiko.",
            )
            st.markdown(
                f"""
                - **Nama:** {snap.get('company_name', '—')}
                - **Penutupan snapshot:** {rupiah(snap.get('close'))} · **Selisih:** {rupiah(snap.get('change'))}
                - **Volume:** {number(snap.get('volume'))} lembar · **Nilai:** {rupiah(snap.get('value'), compact=True)}
                - **Kapitalisasi pasar:** {rupiah(snap.get('market_cap'), compact=True)}
                - **Saham dapat diperdagangkan / saham tercatat:** {decimal_pct(snap.get('tradeable_pct'))}
                  (field `Tradeble Shares` di snapshot; **bukan** free float sebenarnya)
                - **Arus asing net:** {rupiah(snap.get('foreign_net'), compact=True)}
                - **Ada transaksi:** {'Ya' if bool(snap.get('traded')) else 'Tidak'}
                """
            )
        else:
            st.info(
                "Saham ini tidak ada di snapshot IDX satu hari yang tersedia. Metrik historis tetap bisa dipakai."
            )
    st.caption(
        "Return dan risiko memakai **Adj Close** agar perbandingan jangka panjang tidak terdistorsi dividen/split. "
        "Harga terakhir dan kapitalisasi memakai harga penutupan biasa."
    )


def _reading_view() -> None:
    st.markdown(
        """
        ### Cara membaca tabel ini dengan jujur

        - **Return 1 Tahun** dan **Return Periode** dihitung dari harga adjusted pada periode filter.
          Angka besar di masa lalu tidak berarti akan berulang.
        - **CAGR** adalah return tahunan majemuk. Cocok untuk membandingkan periode yang panjang,
          tetapi bisa menyesatkan bila periode sangat pendek.
        - **Volatilitas** mengukur naik-turun return harian yang disetahunkan. Volatilitas tinggi bukan
          otomatis buruk, tetapi biasanya berarti perjalanan lebih sulit ditahan.
        - **Max drawdown** adalah penurunan terdalam dari puncak sebelumnya. Ini bukan batas kerugian
          maksimum di masa depan.
        - **Likuiditas 20H** adalah rata-rata nilai transaksi harian selama 20 hari terakhir pada data.
          Semakin kecil, semakin besar risiko sulit keluar masuk tanpa menggerakkan harga.
        - **Kapitalisasi** dihitung dari harga terakhir dataset × jumlah saham tercatat di snapshot.
          Ini perkiraan kasar, bukan angka resmi real-time.
        - **Tradeable/Listed** adalah rasio `Tradeble Shares` ÷ `Listed Shares` dari snapshot. Pada file ini
          nilainya hampir selalu 100%, jadi **bukan** ukuran free float sebenarnya. Jangan memakainya untuk
          menyimpulkan likuiditas atau kepemilikan publik.

        ### Yang tidak dilakukan halaman ini

        - Tidak memberi skor “saham terbaik” atau rekomendasi beli.
        - Tidak memprediksi harga.
        - Tidak memakai data fundamental perusahaan nyata karena belum tersedia dan belum diverifikasi.
        - Tidak menghapus saham yang pernah merugi dari tabel (tidak ada survivorship selection di sini).

        Filter hanya membantu mempersempit pertanyaan riset. Keputusan tetap membutuhkan pemahaman bisnis,
        laporan keuangan, valuasi, dan toleransi risiko masing-masing.
        """
    )


def render() -> None:
    page_header(
        "Riset Saham",
        "Menyaring 12 saham belajar dengan kriteria yang terlihat jelas. Tidak ada skor ajaib dan tidak ada rekomendasi beli.",
        "Langkah 9 · riset",
    )
    st.warning(
        "**Ini bukan screener rekomendasi.** Tabel hanya merangkum metrik historis dari dataset kecil "
        "12 saham. Jangan membeli saham hanya karena peringkatnya bagus di sini.",
        icon="🔎",
    )

    try:
        prices = get_prices()
        tickers = get_tickers()
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Data historis belum siap: {exc}")
        st.info("Jalankan `python scripts/fetch_data.py`, lalu muat ulang halaman.")
        return

    try:
        snapshot = get_snapshot()
    except (DataNotFoundError, ValueError):
        snapshot = None
        st.caption("Snapshot IDX tidak tersedia; kolom kapitalisasi dan tradeable/listed akan kosong.")

    start, end, period_label = render_period_controls(prices, "research", "3 tahun")
    st.caption(
        f"Periode: **{period_label}**. Metrik dihitung ulang setiap kali periode atau filter berubah."
    )

    with st.spinner("Menghitung metrik historis..."):
        table = build_research_table(
            prices,
            tickers,
            snapshot=snapshot,
            start=start,
            end=end,
            min_observations=60,
        )

    if table.empty:
        st.warning("Belum ada saham dengan data cukup pada periode ini. Coba periode lebih panjang.")
        return

    section_heading("Filter riset", "Filter ini hanya menyaring baris; bukan penilaian otomatis.")
    filter_left, filter_mid, filter_right = st.columns([1.3, 1.4, 1.2])
    with filter_left:
        sectors = sorted(table["Sektor"].dropna().astype(str).unique())
        chosen_sectors = st.multiselect(
            "Sektor",
            sectors,
            default=[],
            help="Kosongkan untuk menampilkan semua sektor.",
        )
        search = st.text_input(
            "Cari kode atau nama",
            placeholder="Contoh: BBCA atau Bank",
        )
    with filter_mid:
        min_liquidity_juta = st.number_input(
            "Likuiditas 20H minimum (Rp juta)",
            min_value=0,
            max_value=1_000_000,
            value=0,
            step=500,
            help="0 berarti tanpa batas minimum. Angka ini rata-rata nilai transaksi harian, bukan jaminan mudah dijual.",
        )
        max_volatility_pct = st.slider(
            "Volatilitas tahunan maksimum (%)",
            min_value=0,
            max_value=100,
            value=100,
            step=5,
            help="100% berarti tanpa batas. Volatilitas dihitung dari return harian.",
        )
    with filter_right:
        sort_label = st.selectbox("Urutkan", list(SORT_OPTIONS), index=0)
        only_snapshot = st.checkbox(
            "Hanya yang ada di snapshot IDX",
            value=False,
            help="Saham tanpa data snapshot tetap punya metrik historis, tetapi kapitalisasi dan tradeable/listed kosong.",
        )

    filtered = table.copy()
    if chosen_sectors:
        filtered = filtered.loc[filtered["Sektor"].isin(chosen_sectors)]
    if search.strip():
        query = search.strip().lower()
        filtered = filtered.loc[
            filtered["Ticker"].str.lower().str.contains(query, na=False)
            | filtered["Nama"].str.lower().str.contains(query, na=False)
            | filtered["Kode Lengkap"].str.lower().str.contains(query, na=False)
        ]
    if min_liquidity_juta > 0:
        filtered = filtered.loc[filtered["Nilai Transaksi 20H"] >= min_liquidity_juta * 1_000_000]
    if max_volatility_pct < 100:
        filtered = filtered.loc[filtered["Volatilitas Tahunan"] <= max_volatility_pct / 100]
    if only_snapshot:
        filtered = filtered.loc[filtered["Kapitalisasi (Perkiraan)"].notna()]

    sort_column, ascending = SORT_OPTIONS[sort_label]
    filtered = filtered.sort_values(sort_column, ascending=ascending, na_position="last")

    st.markdown(
        f"{badge(f'{len(filtered)} dari {len(table)} saham', 'teal')} "
        f"{badge('Tanpa rekomendasi beli', 'amber')} "
        f"{badge('Harga adjusted untuk return', 'blue')}",
        unsafe_allow_html=True,
    )
    st.caption(
        "Jika filter terlalu ketat, tabel bisa kosong. Longgarkan filter sebelum menyimpulkan bahwa "
        "'tidak ada saham bagus'."
    )

    tab_table, tab_detail, tab_reading = st.tabs(["Tabel Riset", "Detail Saham", "Cara Membaca"])

    with tab_table:
        if filtered.empty:
            st.info("Tidak ada saham yang lolos filter. Coba longgarkan likuiditas atau volatilitas.")
        else:
            st.dataframe(_format_table(filtered), width="stretch", hide_index=True, height=450)
            st.download_button(
                "Unduh tabel riset (CSV)",
                data=filtered.to_csv(index=False).encode("utf-8"),
                file_name="riset_saham.csv",
                mime="text/csv",
            )
            st.caption(
                "Tabel diurutkan sesuai pilihanmu. Perubahan periode dapat mengubah urutan; itu normal "
                "karena kondisi pasar berbeda. Jangan menganggap satu periode sebagai bukti permanen."
            )

    with tab_detail:
        _detail_view(prices, filtered, snapshot, start, end)

    with tab_reading:
        _reading_view()

    st.warning(
        "Dataset hanya berisi 12 saham dan IHSG, bukan seluruh bursa. Hasil filter tidak boleh dianggap "
        "mewakili seluruh pasar Indonesia.",
        icon="⚠️",
    )
