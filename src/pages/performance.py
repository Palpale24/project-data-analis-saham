"""Halaman performa saham dan perbandingan dengan IHSG."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import get_metadata, get_prices
from src.config import BENCHMARK_TICKER, ticker_label, ticker_name
from src.data_loader import DataNotFoundError
from src.pages.common import (
    date_range_caption,
    format_ticker_option,
    render_period_controls,
    stock_options,
)
from src.stock_analysis import (
    get_price_series,
    moving_average,
    performance_table,
    prepare_comparison,
    returns_matrix,
    summary_metrics,
)
from src.ui import (
    COLORWAY,
    TEAL,
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


def _metrics_display(table: pd.DataFrame, benchmark_return: float | None = None) -> pd.DataFrame:
    display = table.copy()
    display["Ticker"] = display["Ticker"].map(ticker_label)
    display["Awal"] = display["Awal"].map(date_label)
    display["Akhir"] = display["Akhir"].map(date_label)
    for column in ["Total Return", "CAGR", "Volatilitas Tahunan", "Max Drawdown"]:
        display[column] = display[column].map(lambda value: pct(value, signed=column in {"Total Return", "CAGR", "Max Drawdown"}))
    if benchmark_return is not None:
        display["Return Relatif vs IHSG"] = table["Total Return"].map(
            lambda value: pct(value - benchmark_return, signed=True) if pd.notna(value) else "—"
        )
    display.columns = [
        "Ticker",
        "Observasi",
        "Awal",
        "Akhir",
        "Total Return",
        "CAGR",
        "Volatilitas Tahunan",
        "Max Drawdown",
    ] + (["Return Relatif vs IHSG"] if benchmark_return is not None else [])
    return display


def _price_detail(prices: pd.DataFrame, ticker: str, start, end) -> None:
    series = get_price_series(prices, ticker, start=start, end=end)
    if len(series) < 2:
        st.warning("Data untuk saham ini belum cukup pada periode yang dipilih.")
        return
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series.values,
            mode="lines",
            name=f"{ticker_label(ticker)} (Adj Close)",
            line=dict(color=TEAL, width=2),
            hovertemplate="%{x|%d %b %Y}<br>Harga: Rp%{y:,.0f}<extra></extra>",
        )
    )
    windows = [20, 50, 200]
    for window, color in zip(windows, ["#D97706", "#2563EB", "#7C3AED"]):
        if len(series) >= window:
            ma = moving_average(series, window)
            fig.add_trace(
                go.Scatter(
                    x=ma.index,
                    y=ma.values,
                    mode="lines",
                    name=f"MA {window}",
                    line=dict(color=color, width=1.3),
                    hovertemplate=f"MA {window}: Rp%{{y:,.0f}}<extra></extra>",
                )
            )
    plotly_style(
        fig,
        f"Harga {ticker_label(ticker)} — {ticker_name(ticker)}",
        "Tanggal",
        "Harga adjusted (Rp)",
        height=460,
    )
    fig.update_yaxes(tickprefix="Rp", tickformat=",.0f")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    st.caption(
        "Garis harga memakai **Adj Close**. Moving average hanya digambar jika jumlah data mencukupi. "
        "MA adalah rata-rata masa lalu, bukan sinyal pasti."
    )


def render() -> None:
    page_header(
        "Analisis Performa Saham",
        "Bandingkan perjalanan harga, return, CAGR, dan moving average pada periode yang sama.",
        "Langkah 3 · performa",
    )
    try:
        prices = get_prices()
        metadata = get_metadata()
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Data historis belum siap: {exc}")
        st.info("Jalankan `python scripts/fetch_data.py` dari folder proyek, lalu muat ulang.")
        return

    options = stock_options(prices)
    defaults = [t for t in ["BBCA.JK", "TLKM.JK", "ANTM.JK"] if t in options]
    left, middle, right = st.columns([2.2, 1.2, 1.0])
    with left:
        selected = st.multiselect(
            "Saham yang dibandingkan",
            options,
            default=defaults,
            format_func=format_ticker_option,
            help="Pilih beberapa saham. Perbandingan dimulai pada tanggal yang sama agar adil.",
        )
    with middle:
        start, end, period_label = render_period_controls(prices, "performance", "3 tahun")
    with right:
        include_benchmark = st.checkbox("Sertakan IHSG", value=True, help="IHSG dipakai sebagai pembanding pasar.")
        st.caption("Benchmark: IHSG")

    if not selected:
        st.info("Pilih minimal satu saham untuk mulai.")
        return

    tickers = list(selected)
    if include_benchmark and BENCHMARK_TICKER not in tickers:
        tickers.append(BENCHMARK_TICKER)

    comparison = prepare_comparison(prices, tickers, start=start, end=end)
    if comparison.empty:
        st.warning("Tidak ada tanggal yang bisa dibandingkan pada periode ini. Coba periode lebih panjang.")
        return
    common_start, common_end = comparison.index.min(), comparison.index.max()
    st.caption(
        f"Periode data: **{date_range_caption(common_start, common_end)}** · "
        f"Grafik dan tabel memakai tanggal awal yang sama agar perbandingan tidak bias."
    )

    table = performance_table(prices, tickers, start=common_start, end=common_end)
    if table.empty:
        st.warning("Tabel metrik belum dapat dihitung.")
        return
    benchmark_row = table.loc[table["Ticker"] == BENCHMARK_TICKER]
    benchmark_return = (
        float(benchmark_row["Total Return"].iloc[0])
        if include_benchmark and not benchmark_row.empty
        else None
    )

    first_ticker = selected[0]
    first_metrics = summary_metrics(get_price_series(prices, first_ticker, start=common_start, end=common_end))
    stat_cards(
        [
            {
                "label": f"Total return {ticker_label(first_ticker)}",
                "value": pct(first_metrics["total_return"], signed=True),
                "note": "Perubahan harga adjusted, bukan prediksi",
                "tone": "good" if (first_metrics["total_return"] or 0) >= 0 else "bad",
            },
            {
                "label": "CAGR",
                "value": pct(first_metrics["cagr"], signed=True),
                "note": "Pertumbuhan tahunan majemuk",
                "tone": "blue",
            },
            {
                "label": "Volatilitas tahunan",
                "value": pct(first_metrics["annualized_volatility"]),
                "note": "Semakin tinggi, semakin liar",
                "tone": "warn",
            },
            {
                "label": "Maximum drawdown",
                "value": pct(first_metrics["max_drawdown"], signed=True),
                "note": "Penurunan terdalam dari puncak",
                "tone": "bad",
            },
        ]
    )
    st.caption(
        f"Kartu di atas memakai **{ticker_label(first_ticker)}** sebagai contoh. "
        "Angka historis tidak menjamin hasil masa depan."
    )

    tab_compare, tab_detail, tab_returns, tab_table = st.tabs(
        ["Perbandingan", "Detail Saham", "Return Harian", "Tabel Metrik"]
    )

    with tab_compare:
        fig = go.Figure()
        for index, ticker in enumerate(comparison.columns):
            name = f"{ticker_label(ticker)} — {ticker_name(ticker)}"
            fig.add_trace(
                go.Scatter(
                    x=comparison.index,
                    y=comparison[ticker],
                    mode="lines",
                    name=name,
                    line=dict(width=2.4 if ticker == BENCHMARK_TICKER else 1.8, color=COLORWAY[index % len(COLORWAY)]),
                    hovertemplate=f"{name}<br>%{{x|%d %b %Y}}<br>Indeks: %{{y:.1f}}<extra></extra>",
                )
            )
        fig.add_hline(y=100, line_dash="dot", line_color="#94A3B8", annotation_text="Awal = 100")
        plotly_style(
            fig,
            "Perbandingan Harga Ternormalisasi (awal = 100)",
            "Tanggal",
            "Indeks (awal = 100)",
            height=470,
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption(
            "Semua saham dimulai dari nilai 100 pada tanggal yang sama. Garis yang lebih tinggi berarti "
            "naik lebih besar, bukan otomatis perusahaan yang lebih baik. IHSG adalah pembanding pasar."
        )

    with tab_detail:
        detail_ticker = st.selectbox(
            "Saham untuk grafik detail",
            selected,
            format_func=format_ticker_option,
            key="performance_detail_ticker",
        )
        _price_detail(prices, detail_ticker, common_start, common_end)

    with tab_returns:
        returns = returns_matrix(prices, tickers, start=common_start, end=common_end)
        if returns.empty:
            st.info("Return harian belum cukup untuk ditampilkan.")
        else:
            fig = go.Figure()
            for index, column in enumerate(returns.columns):
                fig.add_trace(
                    go.Scatter(
                        x=returns.index,
                        y=returns[column],
                        mode="lines",
                        name=ticker_label(column),
                        line=dict(width=1.2, color=COLORWAY[index % len(COLORWAY)]),
                        hovertemplate=f"{ticker_label(column)}<br>%{{x|%d %b %Y}}<br>Return: %{{y:.2%}}<extra></extra>",
                    )
                )
            fig.add_hline(y=0, line_dash="dot", line_color="#94A3B8")
            plotly_style(fig, "Return Harian", "Tanggal", "Return harian", height=420, percent_y=True)
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
            st.caption(
                "Return harian = (harga hari ini ÷ harga kemarin) − 1. Garis harian bisa terlihat berisik; "
                "gunakan tabel dan periode lebih panjang untuk melihat pola."
            )

    with tab_table:
        display = _metrics_display(table, benchmark_return)
        section_heading("Ringkasan metrik", "Persentase dihitung dari harga adjusted pada periode yang sama.")
        st.dataframe(display, width="stretch", hide_index=True)
        if benchmark_return is not None:
            st.caption(
                "Kolom **Return Relatif vs IHSG** = total return saham − total return IHSG pada periode ini. "
                "Positif berarti mengungguli IHSG secara historis, bukan jaminan masa depan."
            )
        st.download_button(
            "Unduh metrik (CSV)",
            data=table.to_csv(index=False).encode("utf-8"),
            file_name="performance_metrics.csv",
            mime="text/csv",
        )

    st.markdown(
        f"**Periode kontrol:** {period_label}. Dataset historis sampai "
        f"{metadata.get('date_max', date_label(prices['date'].max()))}. "
        "Sumber: Yahoo Finance, harga adjusted. Bukan rekomendasi."
    )
