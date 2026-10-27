"""Halaman korelasi return antar saham."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import get_prices
from src.config import ticker_label, ticker_name
from src.data_loader import DataNotFoundError
from src.pages.common import date_range_caption, format_ticker_option, render_period_controls, stock_options
from src.stock_analysis import correlation_matrix, returns_matrix
from src.ui import page_header, plotly_style, section_heading


def _pair_interpretation(corr: pd.DataFrame) -> tuple[tuple[str, str, float] | None, tuple[str, str, float] | None]:
    pairs = []
    columns = list(corr.columns)
    for i, left in enumerate(columns):
        for right in columns[i + 1 :]:
            value = corr.loc[left, right]
            if pd.notna(value):
                pairs.append((left, right, float(value)))
    if not pairs:
        return None, None
    strongest_positive = max(pairs, key=lambda item: item[2])
    strongest_negative = min(pairs, key=lambda item: item[2])
    return strongest_positive, strongest_negative


def render() -> None:
    page_header(
        "Analisis Hubungan Saham",
        "Melihat apakah return beberapa saham cenderung bergerak bersamaan. Korelasi bukan sebab-akibat.",
        "Langkah 5 · korelasi",
    )
    try:
        prices = get_prices()
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Data historis belum siap: {exc}")
        return

    options = stock_options(prices)
    defaults = [t for t in ["BBCA.JK", "BBRI.JK", "TLKM.JK", "ANTM.JK", "ICBP.JK"] if t in options]
    left, right = st.columns([2.4, 1.2])
    with left:
        selected = st.multiselect(
            "Pilih 2–8 saham",
            options,
            default=defaults,
            format_func=format_ticker_option,
            help="Semakin banyak saham, semakin ramai heatmap. Korelasi dihitung dari return harian pada tanggal yang sama.",
        )
    with right:
        start, end, period_label = render_period_controls(prices, "correlation", "3 tahun")

    if len(selected) < 2:
        st.info("Pilih minimal dua saham untuk menghitung korelasi.")
        return

    returns = returns_matrix(prices, selected, start=start, end=end)
    if returns.empty:
        st.warning("Return belum dapat dihitung pada periode ini.")
        return

    # Pakai hanya tanggal yang tersedia untuk SEMUA saham terpilih, agar
    # setiap pasangan korelasi dihitung pada periode yang sebanding.
    common_returns = returns.dropna()
    if len(common_returns) < 30:
        st.warning(
            f"Hanya tersedia {len(common_returns)} hari dengan data lengkap untuk semua saham. "
            "Butuh minimal 30 hari agar korelasi tidak menyesatkan. Pilih periode lebih panjang "
            "atau kurangi saham yang riwayatnya pendek."
        )
        return

    corr = correlation_matrix(common_returns, min_periods=30)
    if corr.empty:
        st.warning("Matriks korelasi belum dapat dihitung.")
        return

    labels = [ticker_label(t) for t in corr.columns]
    values = corr.values
    text = np.where(np.isnan(values), "—", np.round(values, 2).astype(str))
    fig = go.Figure(
        go.Heatmap(
            z=values,
            x=labels,
            y=labels,
            zmin=-1,
            zmax=1,
            colorscale=[[0, "#B91C1C"], [0.5, "#F8FAFC"], [1, "#0F766E"]],
            text=text,
            texttemplate="%{text}",
            textfont=dict(size=12),
            hovertemplate="%{y} vs %{x}<br>Korelasi: %{z:.2f}<extra></extra>",
            colorbar=dict(title="r", tickvals=[-1, -0.5, 0, 0.5, 1]),
        )
    )
    plotly_style(fig, "Heatmap Korelasi Return Harian", "", "", height=520, show_legend=False)
    fig.update_layout(hovermode="closest")
    fig.update_xaxes(side="bottom")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption(
        f"Periode efektif: **{date_range_caption(common_returns.index.min(), common_returns.index.max())}** · "
        f"{len(common_returns):,} hari dengan data lengkap untuk semua saham.".replace(",", ".")
    )

    positive, negative = _pair_interpretation(corr)
    average_corr = float(
        corr.where(~np.eye(len(corr), dtype=bool)).stack().mean()
    ) if len(corr) > 1 else np.nan

    section_heading("Cara membaca hasil", "Angka mendekati 1 berarti bergerak searah; mendekati -1 berarti berlawanan.")
    left, middle, right = st.columns(3)
    with left:
        if positive:
            label = "Korelasi positif terkuat" if positive[2] > 0 else "Korelasi tertinggi"
            arah = "cenderung bergerak searah" if positive[2] > 0 else "masih cenderung berlawanan, meski paling tinggi"
            st.markdown(
                f'<div class="soft-card"><div class="stat-label">{label}</div>'
                f'<div class="stat-value">{positive[2]:.2f}</div>'
                f'<p>{ticker_label(positive[0])} dan {ticker_label(positive[1])} {arah}.</p></div>',
                unsafe_allow_html=True,
            )
    with middle:
        if negative:
            label = "Korelasi paling negatif" if negative[2] < 0 else "Korelasi terendah"
            arah = "cenderung bergerak berlawanan" if negative[2] < 0 else "masih searah, tetapi paling lemah"
            st.markdown(
                f'<div class="soft-card"><div class="stat-label">{label}</div>'
                f'<div class="stat-value">{negative[2]:.2f}</div>'
                f'<p>{ticker_label(negative[0])} dan {ticker_label(negative[1])} {arah}.</p></div>',
                unsafe_allow_html=True,
            )
    with right:
        st.markdown(
            f'<div class="soft-card"><div class="stat-label">Rata-rata korelasi pasangan</div>'
            f'<div class="stat-value">{average_corr:.2f}</div>'
            f'<p>Nilai di luar diagonal. Semakin tinggi, semakin mirip pergerakannya.</p></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        - **Positif** berarti return cenderung bergerak ke arah yang sama. Tidak berarti selalu naik bersama.
        - **Negatif** berarti cenderung bergerak berlawanan. Bisa membantu diversifikasi, tetapi tidak menghilangkan risiko.
        - **Mendekati 0** berarti hubungan linear lemah pada periode ini, bukan berarti tidak ada risiko.
        - Korelasi **bukan hubungan sebab-akibat**. Dua saham bisa bergerak mirip karena terpengaruh kondisi pasar yang sama.

        Korelasi juga **tidak stabil**: bisa berubah saat krisis, suku bunga berubah, atau sektor tertekan.
        Diversifikasi yang didasarkan pada korelasi historis tetap bisa gagal di masa depan.
        """
    )

    section_heading("Matriks angka", "Nilai 1 pada diagonal berarti saham dibandingkan dengan dirinya sendiri.")
    matrix_display = corr.copy()
    matrix_display.index = [ticker_label(t) for t in matrix_display.index]
    matrix_display.columns = [ticker_label(t) for t in matrix_display.columns]
    st.dataframe(matrix_display.round(3), width="stretch")
    st.download_button(
        "Unduh matriks korelasi (CSV)",
        data=corr.to_csv().encode("utf-8"),
        file_name="correlation_matrix.csv",
        mime="text/csv",
    )

    st.warning(
        "Jumlah hari yang dipakai bersama bergantung pada saham dengan riwayat terpendek. "
        "Jika kamu memilih saham yang baru IPO, periode efektif bisa jauh lebih pendek. "
        f"Periode kontrol: {period_label}.",
        icon="⚠️",
    )
