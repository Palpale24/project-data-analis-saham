"""Halaman fundamental: status data nyata dan latihan dengan perusahaan fiktif."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import get_prices
from src.data_loader import DataNotFoundError
from src.fundamental import (
    SAMPLE_FUNDAMENTAL_FILE,
    calculate_fundamental_metrics,
    load_sample_financials,
    metrics_table,
)
from src.ui import (
    badge,
    decimal_pct,
    number,
    page_header,
    plotly_style,
    rupiah,
    section_heading,
    stat_cards,
)


def _format_sample_table(frame: pd.DataFrame) -> pd.DataFrame:
    display = frame.copy()
    for column in [
        "pendapatan",
        "beban_pokok",
        "laba_operasi",
        "laba_bersih",
        "arus_kas_operasi",
        "total_aset",
        "total_liabilitas",
        "ekuitas",
        "dividen_dibagikan",
    ]:
        display[column] = display[column].map(lambda value: rupiah(value, compact=True))
    display["jumlah_saham"] = display["jumlah_saham"].map(lambda value: number(value))
    display["harga_saham"] = display["harga_saham"].map(rupiah)
    display.columns = [
        "Tahun",
        "Pendapatan",
        "Beban Pokok",
        "Laba Operasi",
        "Laba Bersih",
        "Arus Kas Operasi",
        "Total Aset",
        "Liabilitas",
        "Ekuitas",
        "Jumlah Saham",
        "Harga Saham",
        "Dividen",
    ]
    return display


def _format_metrics(frame: pd.DataFrame) -> pd.DataFrame:
    display = frame.copy()
    for column in ["EPS (Rp)", "BVPS (Rp)", "DPS (Rp)"]:
        display[column] = display[column].map(rupiah)
    for column in ["PER (×)", "PBV (×)", "DER (×)"]:
        display[column] = display[column].map(lambda value: f"{value:.2f}×" if pd.notna(value) else "—")
    for column in ["ROE (%)", "Margin Laba (%)", "Dividend Yield (%)", "Payout Ratio (%)"]:
        display[column] = display[column].map(lambda value: decimal_pct(value) if pd.notna(value) else "—")
    display["Arus Kas Operasi / Laba"] = display["Arus Kas Operasi / Laba"].map(
        lambda value: f"{value:.2f}×" if pd.notna(value) else "—"
    )
    display.columns = [
        "Tahun",
        "EPS",
        "PER",
        "Nilai Buku/Lembar",
        "PBV",
        "ROE",
        "Margin Laba",
        "DER",
        "DPS",
        "Dividend Yield",
        "Payout Ratio",
        "Arus Kas Operasi / Laba",
    ]
    return display


def _status_tab(sample: pd.DataFrame) -> None:
    st.warning(
        "Data fundamental perusahaan nyata **belum tersedia** di proyek ini. Halaman ini tidak menampilkan "
        "PER/PBV perusahaan nyata karena angka tersebut belum diverifikasi. Yang tersedia adalah latihan "
        "dengan perusahaan fiktif dan kalkulator manual.",
        icon="🧾",
    )
    stat_cards(
        [
            {"label": "Data fundamental nyata", "value": "Belum ada", "note": "Tidak dibuat-buat", "tone": "bad"},
            {"label": "Perusahaan latihan", "value": "Fiktif", "note": "PT Bakso Nusantara", "tone": "amber"},
            {"label": "Periode contoh", "value": "3 tahun", "note": "2023–2025", "tone": "blue"},
            {"label": "Sumber", "value": "File lokal", "note": "data/sample", "tone": ""},
        ]
    )
    st.markdown(
        """
        Untuk menganalisis perusahaan nyata, kamu perlu mengumpulkan:

        - laporan laba rugi dan neraca dari laporan tahunan/triwulan resmi;
        - laporan arus kas;
        - jumlah saham beredar (dan riwayat dilusi);
        - harga saham pada tanggal analisis;
        - dividen yang dibagikan;
        - catatan kaki tentang utang, goodwill, dan pos sekali.

        Sumber utama: situs Investor Relations perusahaan, keterbukaan informasi BEI, dan laporan tahunan.
        Jangan mengisi kolom kosong dengan angka perkiraan lalu menganggapnya fakta.
        """
    )
    st.download_button(
        "Unduh data contoh fiktif (CSV)",
        data=sample.to_csv(index=False).encode("utf-8"),
        file_name="contoh_laporan_keuangan_fiktif.csv",
        mime="text/csv",
    )
    st.caption(f"Lokasi file contoh: `{SAMPLE_FUNDAMENTAL_FILE.relative_to(SAMPLE_FUNDAMENTAL_FILE.parents[2])}`")


def _practice_tab(sample: pd.DataFrame, ratios: pd.DataFrame) -> None:
    st.info(
        "**PT Bakso Nusantara adalah perusahaan fiktif.** Angka di bawah hanya untuk belajar rumus, bukan "
        "data perusahaan nyata dan bukan rekomendasi.",
        icon="🏷️",
    )
    section_heading("Laporan keuangan fiktif", "Tiga tahun sederhana: pendapatan, laba, arus kas, aset, utang, ekuitas, dan dividen.")
    st.dataframe(_format_sample_table(sample), width="stretch", hide_index=True)

    latest = sample.iloc[-1]
    fig = go.Figure()
    categories = ["Pendapatan", "Laba bersih", "Arus kas operasi"]
    values = [
        latest["pendapatan"] / 1e9,
        latest["laba_bersih"] / 1e9,
        latest["arus_kas_operasi"] / 1e9,
    ]
    colors = ["#0F766E", "#D97706", "#2563EB"]
    fig.add_trace(
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"Rp{v:.2f} M" for v in values],
            textposition="outside",
            hovertemplate="%{x}<br>Rp%{y:.2f} miliar<extra></extra>",
        )
    )
    plotly_style(fig, "PT Bakso Nusantara 2025 (fiktif) — skala miliar rupiah", "", "Rp miliar", height=360, show_legend=False)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption("Laba bersih lebih besar dari arus kas operasi. Ini mengingatkan bahwa laba akuntansi tidak selalu sama dengan kas.")

    section_heading("Rasio dari data fiktif", "Perhatikan bagaimana setiap rasio berasal dari angka yang sama.")
    st.dataframe(_format_metrics(ratios), width="stretch", hide_index=True)

    latest_ratio = ratios.iloc[-1]
    stat_cards(
        [
            {"label": "EPS", "value": rupiah(latest_ratio["EPS (Rp)"]), "note": "Laba per lembar", "tone": "good"},
            {"label": "PER", "value": f"{latest_ratio['PER (×)']:.1f}×", "note": "Harga ÷ EPS", "tone": "blue"},
            {"label": "PBV", "value": f"{latest_ratio['PBV (×)']:.1f}×", "note": "Harga ÷ nilai buku", "tone": "amber"},
            {"label": "ROE", "value": decimal_pct(latest_ratio["ROE (%)"]), "note": "Laba ÷ ekuitas", "tone": ""},
        ]
    )
    st.warning(
        "PER 12,5× dan PBV 2,5× tidak otomatis berarti mahal atau murah. Kita belum membandingkan dengan "
        "perusahaan sejenis, pertumbuhan, utang, dan kualitas arus kas.",
        icon="🔍",
    )


def _calculator_tab(sample: pd.DataFrame) -> None:
    st.info(
        "Kalkulator ini memakai input manual. Masukkan angka dari laporan resmi; jangan menganggap hasilnya "
        "sebagai rekomendasi. Semua input bisa diubah.",
        icon="🧮",
    )
    latest = sample.iloc[-1]
    left, right = st.columns(2)
    with left:
        pendapatan = st.number_input("Pendapatan (Rp)", min_value=1.0, value=float(latest["pendapatan"]), step=10_000_000.0, format="%.0f")
        laba_bersih = st.number_input("Laba bersih (Rp)", value=float(latest["laba_bersih"]), step=1_000_000.0, format="%.0f")
        ekuitas = st.number_input("Ekuitas (Rp)", min_value=1.0, value=float(latest["ekuitas"]), step=10_000_000.0, format="%.0f")
        liabilitas = st.number_input("Total liabilitas (Rp)", min_value=0.0, value=float(latest["total_liabilitas"]), step=10_000_000.0, format="%.0f")
    with right:
        saham = st.number_input("Jumlah saham beredar (lembar)", min_value=1.0, value=float(latest["jumlah_saham"]), step=100_000.0, format="%.0f")
        harga = st.number_input("Harga saham (Rp/lembar)", min_value=1.0, value=float(latest["harga_saham"]), step=50.0, format="%.0f")
        dividen = st.number_input("Total dividen dibagikan (Rp)", min_value=0.0, value=float(latest["dividen_dibagikan"]), step=1_000_000.0, format="%.0f")

    if laba_bersih <= 0:
        st.warning("Laba bersih ≤ 0: PER dan payout ratio tidak dapat dihitung secara bermakna.")
    metrics = calculate_fundamental_metrics(
        pendapatan=pendapatan,
        laba_bersih=laba_bersih,
        ekuitas=ekuitas,
        jumlah_saham=saham,
        harga_saham=harga,
        dividen_dibagikan=dividen,
        total_liabilitas=liabilitas,
    )
    stat_cards(
        [
            {"label": "EPS", "value": rupiah(metrics["eps"]), "note": "Laba ÷ saham", "tone": "good"},
            {"label": "PER", "value": f"{metrics['per']:.2f}×" if metrics["per"] else "Tidak dapat dihitung", "note": "Harga ÷ EPS", "tone": "blue"},
            {"label": "PBV", "value": f"{metrics['pbv']:.2f}×" if metrics["pbv"] else "Tidak dapat dihitung", "note": "Harga ÷ nilai buku", "tone": "amber"},
            {"label": "ROE", "value": decimal_pct(metrics["roe"] * 100) if metrics["roe"] is not None else "—", "note": "Laba ÷ ekuitas", "tone": ""},
            {"label": "DER", "value": f"{metrics['der']:.2f}×" if metrics["der"] is not None else "—", "note": "Utang ÷ ekuitas", "tone": "warn"},
            {"label": "Dividend yield", "value": decimal_pct(metrics["dividend_yield"] * 100) if metrics["dividend_yield"] is not None else "—", "note": "DPS ÷ harga", "tone": ""},
            {"label": "Payout ratio", "value": decimal_pct(metrics["payout_ratio"] * 100) if metrics["payout_ratio"] is not None else "—", "note": "Dividen ÷ laba", "tone": ""},
            {"label": "Margin laba", "value": decimal_pct(metrics["net_margin"] * 100) if metrics["net_margin"] is not None else "—", "note": "Laba ÷ pendapatan", "tone": ""},
        ]
    )
    st.caption("Nilai PER/PBV yang tampil hanya berlaku untuk harga dan laba yang kamu masukkan. Ganti harga, hasilnya berubah.")


def _reading_tab() -> None:
    st.markdown(
        """
        ### Rumus yang dipakai

        - **EPS** = laba bersih ÷ jumlah saham beredar.
        - **PER** = harga per lembar ÷ EPS.
        - **Nilai buku per saham (BVPS)** = ekuitas ÷ jumlah saham.
        - **PBV** = harga per lembar ÷ BVPS.
        - **ROE** = laba bersih ÷ ekuitas.
        - **DER** = total liabilitas ÷ ekuitas.
        - **DPS** = total dividen ÷ jumlah saham.
        - **Dividend yield** = DPS ÷ harga per lembar.
        - **Payout ratio** = total dividen ÷ laba bersih.
        - **Margin laba** = laba bersih ÷ pendapatan.

        ### Cara membaca yang jujur

        - Bandingkan rasio dengan **perusahaan sejenis** dan **tahun sebelumnya**, bukan angka absolut.
        - PER rendah bisa berarti murah, bisa juga karena pasar meragukan laba masa depan.
        - PBV rendah bisa berarti aset murah, tetapi goodwill dan aset tidak produktif bisa menipu.
        - ROE tinggi bisa berasal dari utang besar, bukan efisiensi.
        - Dividend yield tinggi bisa muncul karena harga jatuh.
        - Laba sekali (penjualan aset, revaluasi) bisa membuat EPS dan PER terlihat bagus sementara.

        **Jangan menyimpulkan perusahaan bagus atau buruk dari satu rasio.** Baca arus kas, utang,
        catatan kaki, prospek industri, dan risiko bisnis.
        """
    )
    st.warning(
        "Data fundamental nyata belum tersedia. Jangan mengisi angka contoh ke dalam analisis perusahaan "
        "nyata tanpa memeriksa laporan resminya.",
        icon="⚠️",
    )


def render() -> None:
    page_header(
        "Analisis Fundamental",
        "Membaca laporan keuangan dan rasio dengan hati-hati. Data nyata belum tersedia; latihan memakai perusahaan fiktif.",
        "Langkah 6 · fundamental",
    )
    try:
        sample = load_sample_financials()
        ratios = metrics_table(sample)
    except (FileNotFoundError, ValueError) as exc:
        st.error(f"Data contoh fundamental tidak dapat dibaca: {exc}")
        return

    st.markdown(
        f"{badge('Data fundamental nyata: belum tersedia', 'amber')} "
        f"{badge('Contoh fiktif untuk latihan', 'blue')} "
        f"{badge('Tidak ada angka perusahaan nyata yang dikarang', 'teal')}",
        unsafe_allow_html=True,
    )
    st.write("")
    tab_status, tab_practice, tab_calculator, tab_reading = st.tabs(
        ["Status Data", "Latihan Fiktif", "Kalkulator Rasio", "Cara Membaca"]
    )
    with tab_status:
        _status_tab(sample)
    with tab_practice:
        _practice_tab(sample, ratios)
    with tab_calculator:
        _calculator_tab(sample)
    with tab_reading:
        _reading_tab()
