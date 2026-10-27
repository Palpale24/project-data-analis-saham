"""Halaman analisis risiko historis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import get_prices
from src.config import ticker_label, ticker_name
from src.data_loader import DataNotFoundError
from src.pages.common import format_ticker_option, render_period_controls, stock_options
from src.risk_analysis import historical_var, risk_metrics, risk_table
from src.stock_analysis import calculate_daily_returns, drawdown_details, drawdown_series, get_price_series
from src.ui import (
    COLORWAY,
    date_label,
    decimal_pct,
    page_header,
    plotly_style,
    pct,
    section_heading,
    stat_cards,
)


def _risk_display(table: pd.DataFrame) -> pd.DataFrame:
    display = table.copy()
    display["Ticker"] = display["Ticker"].map(ticker_label)
    display["Puncak Drawdown"] = display["Puncak Drawdown"].map(date_label)
    display["Dasar Drawdown"] = display["Dasar Drawdown"].map(date_label)
    for column in [
        "Volatilitas Tahunan",
        "Downside Deviation",
        "Max Drawdown",
        "VaR 95% Harian",
        "Hari Negatif",
        "Hari Terburuk",
        "Hari Terbaik",
    ]:
        display[column] = display[column].map(lambda value: pct(value, signed=column in {"Max Drawdown", "Hari Terburuk", "Hari Terbaik"}))
    display.columns = [
        "Ticker",
        "Observasi",
        "Volatilitas Tahunan",
        "Downside Deviation",
        "Max Drawdown",
        "VaR 95% Harian",
        "Hari Negatif",
        "Hari Terburuk",
        "Hari Terbaik",
        "Puncak Drawdown",
        "Dasar Drawdown",
    ]
    return display


def render() -> None:
    page_header(
        "Analisis Risiko",
        "Melihat seberapa liar perjalanan harga dan seberapa dalam penurunan yang pernah terjadi.",
        "Langkah 4 · risiko",
    )
    try:
        prices = get_prices()
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Data historis belum siap: {exc}")
        return

    options = stock_options(prices)
    defaults = [t for t in ["BBCA.JK", "ANTM.JK", "GOTO.JK"] if t in options]
    left, right = st.columns([2.2, 1.3])
    with left:
        selected = st.multiselect(
            "Saham yang dianalisis",
            options,
            default=defaults,
            format_func=format_ticker_option,
            help="Pilih 2–6 saham agar perbandingan mudah dibaca.",
        )
    with right:
        start, end, period_label = render_period_controls(prices, "risk", "3 tahun")

    if not selected:
        st.info("Pilih minimal satu saham.")
        return

    st.caption(
        f"Periode: **{period_label}**. Metrik hanya dihitung jika tersedia minimal **60 hari** data; "
        "angka historis bukan prediksi."
    )
    table, skipped = risk_table(prices, selected, start=start, end=end, min_observations=60)
    for item in skipped:
        st.warning(f"{ticker_label(item['ticker'])}: {item['reason']}")
    if table.empty:
        st.warning("Belum ada saham dengan data cukup pada periode ini.")
        return

    first = selected[0]
    first_series = get_price_series(prices, first, start=start, end=end)
    first_metrics = risk_metrics(first_series)
    stat_cards(
        [
            {
                "label": f"Volatilitas {ticker_label(first)}",
                "value": pct(first_metrics["annualized_volatility"]),
                "note": "Disetahunkan dari return harian",
                "tone": "warn",
            },
            {
                "label": "Maximum drawdown",
                "value": pct(first_metrics["max_drawdown"], signed=True),
                "note": "Penurunan terdalam dari puncak",
                "tone": "bad",
            },
            {
                "label": "VaR 95% harian",
                "value": pct(first_metrics["var_95_daily"] / 100),
                "note": "Ambang kerugian 5% hari terburuk historis",
                "tone": "amber",
            },
            {
                "label": "Hari negatif",
                "value": pct(first_metrics["negative_day_pct"]),
                "note": f"Dari {first_metrics['observations']:,} hari data".replace(",", "."),
                "tone": "blue",
            },
        ]
    )
    st.caption(
        "Kartu memakai saham pertama yang dipilih. Drawdown negatif berarti harga pernah turun dari puncaknya."
    )

    tab_summary, tab_drawdown, tab_distribution, tab_table = st.tabs(
        ["Ringkasan", "Drawdown", "Distribusi Return", "Tabel Metrik"]
    )

    with tab_summary:
        labels = [ticker_label(t) for t in table["Ticker"]]
        left, right = st.columns(2)
        with left:
            fig = go.Figure(
                go.Bar(
                    x=labels,
                    y=table["Volatilitas Tahunan"],
                    marker_color="#D97706",
                    hovertemplate="%{x}<br>Volatilitas: %{y:.1%}<extra></extra>",
                )
            )
            plotly_style(fig, "Volatilitas Tahunan", "", "Volatilitas", height=360, percent_y=True, show_legend=False)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            st.caption("Semakin tinggi batang, semakin besar naik-turun return historis. Bukan batas kerugian maksimum.")
        with right:
            fig = go.Figure(
                go.Bar(
                    x=labels,
                    y=table["Max Drawdown"],
                    marker_color="#B91C1C",
                    hovertemplate="%{x}<br>Max drawdown: %{y:.1%}<extra></extra>",
                )
            )
            plotly_style(fig, "Maximum Drawdown", "", "Drawdown", height=360, percent_y=True, show_legend=False)
            fig.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            st.caption("Semakin negatif, semakin dalam penurunan terburuk dari puncak pada periode ini.")
        st.info(
            "Saham dengan return tinggi tetapi drawdown sangat dalam bisa lebih sulit ditahan secara emosional. "
            "Risiko bukan hanya angka akhir, tetapi juga perjalanan menuju angka itu.",
            icon="🧭",
        )

    with tab_drawdown:
        fig = go.Figure()
        for index, ticker in enumerate(selected):
            series = get_price_series(prices, ticker, start=start, end=end)
            if len(series) < 60:
                continue
            drawdown = drawdown_series(series)
            fig.add_trace(
                go.Scatter(
                    x=drawdown.index,
                    y=drawdown.values,
                    mode="lines",
                    name=ticker_label(ticker),
                    line=dict(width=1.6, color=COLORWAY[index % len(COLORWAY)]),
                    hovertemplate=f"{ticker_label(ticker)}<br>%{{x|%d %b %Y}}<br>Drawdown: %{{y:.1%}}<extra></extra>",
                )
            )
        if fig.data:
            fig.add_hline(y=0, line_dash="dot", line_color="#94A3B8")
            plotly_style(fig, "Drawdown Sepanjang Periode", "Tanggal", "Drawdown dari puncak", height=440, percent_y=True)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            st.caption(
                "Drawdown 0% berarti harga berada di puncak baru. Garis yang turun ke bawah menunjukkan "
                "jarak dari puncak sebelumnya, bukan prediksi penurunan berikutnya."
            )

        detail = st.selectbox(
            "Detail drawdown untuk",
            selected,
            format_func=format_ticker_option,
            key="risk_drawdown_ticker",
        )
        series = get_price_series(prices, detail, start=start, end=end)
        details = drawdown_details(series)
        st.markdown(
            f"""
            **{ticker_label(detail)} — {ticker_name(detail)}**  
            Puncak: {date_label(details['peak_date'])} · Dasar: {date_label(details['trough_date'])} · 
            Kedalaman: **{pct(details['max_drawdown'], signed=True)}** · 
            Pemulihan: {date_label(details['recovery_date']) if details['recovery_date'] is not None else 'belum kembali ke puncak'}
            """
        )

    with tab_distribution:
        detail = st.selectbox(
            "Saham untuk distribusi return",
            selected,
            format_func=format_ticker_option,
            key="risk_distribution_ticker",
        )
        series = get_price_series(prices, detail, start=start, end=end)
        returns = calculate_daily_returns(series)
        if len(returns) < 60:
            st.info("Data return belum cukup untuk histogram yang bermakna.")
        else:
            var_value = historical_var(returns, 0.95) / 100
            fig = go.Figure(
                go.Histogram(
                    x=returns,
                    nbinsx=60,
                    marker_color="#0F766E",
                    opacity=0.82,
                    histnorm="probability",
                    hovertemplate="Return: %{x:.1%}<br>Proporsi: %{y:.2%}<extra></extra>",
                )
            )
            fig.add_vline(x=0, line_dash="dot", line_color="#94A3B8", annotation_text="0%")
            if not np.isnan(var_value):
                fig.add_vline(
                    x=-var_value,
                    line_dash="dash",
                    line_color="#B91C1C",
                    annotation_text=f"VaR 95% ≈ -{var_value:.1%}",
                    annotation_position="top left",
                )
            plotly_style(
                fig,
                f"Distribusi Return Harian {ticker_label(detail)}",
                "Return harian",
                "Proporsi hari",
                height=430,
                percent_x=True,
                percent_y=True,
                show_legend=False,
            )
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            st.caption(
                f"VaR 95% historis sekitar **{var_value:.1%}** per hari. Artinya, pada 5% hari terburuk "
                "dalam periode ini, kerugian harian setidaknya sebesar itu. VaR bukan batas kerugian maksimum."
            )
            st.markdown(
                f"- Hari terbaik: **{pct(returns.max(), signed=True)}**  \n"
                f"- Hari terburuk: **{pct(returns.min(), signed=True)}**  \n"
                f"- Rata-rata return harian: **{pct(returns.mean(), signed=True)}**  \n"
                f"- Proporsi hari negatif: **{pct((returns < 0).mean())}**"
            )

    with tab_table:
        section_heading("Perbandingan metrik risiko", "Semakin tinggi volatilitas/drawdown, semakin besar fluktuasi historis.")
        st.dataframe(_risk_display(table), width="stretch", hide_index=True)
        st.download_button(
            "Unduh metrik risiko (CSV)",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="risk_metrics.csv",
            mime="text/csv",
        )
        st.warning(
            "Metrik dihitung dari periode yang dipilih. Mengganti periode dapat mengubah peringkat. "
            "Jangan memilih saham hanya karena drawdown historisnya paling kecil.",
            icon="⚠️",
        )
