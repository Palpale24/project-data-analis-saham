"""Kontrol periode dan pilihan ticker yang dipakai beberapa halaman."""

from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.config import ticker_label, ticker_name
from src.ui import date_label

PERIOD_OPTIONS = ["1 tahun", "3 tahun", "5 tahun", "Sejak awal", "Custom"]
PERIOD_YEARS = {"1 tahun": 1, "3 tahun": 3, "5 tahun": 5}


def format_ticker_option(ticker: str) -> str:
    return f"{ticker_label(ticker)} — {ticker_name(ticker)}"


def stock_options(prices: pd.DataFrame) -> list[str]:
    return sorted(t for t in prices["ticker"].unique() if not str(t).startswith("^"))


def render_period_controls(
    prices: pd.DataFrame,
    key_prefix: str,
    default: str = "3 tahun",
) -> tuple[pd.Timestamp, pd.Timestamp, str]:
    """Tampilkan pilihan periode dan kembalikan (start, end, label)."""
    data_min = pd.Timestamp(prices["date"].min()).normalize()
    data_max = pd.Timestamp(prices["date"].max()).normalize()
    preset = st.selectbox(
        "Periode analisis",
        PERIOD_OPTIONS,
        index=PERIOD_OPTIONS.index(default),
        key=f"{key_prefix}_period",
        help="Periode yang lebih panjang memberi konteks lebih banyak, tetapi kondisi pasar bisa berbeda.",
    )
    if preset == "Custom":
        selected = st.date_input(
            "Rentang tanggal",
            value=(max(data_min.date(), (data_max - pd.DateOffset(years=2)).date()), data_max.date()),
            min_value=data_min.date(),
            max_value=data_max.date(),
            key=f"{key_prefix}_custom_dates",
        )
        if isinstance(selected, (tuple, list)) and len(selected) == 2:
            start, end = pd.Timestamp(selected[0]), pd.Timestamp(selected[1])
        elif isinstance(selected, (tuple, list)) and len(selected) == 1:
            start = pd.Timestamp(selected[0])
            end = data_max
        else:
            start, end = data_max - pd.DateOffset(years=3), data_max
        label = f"{date_label(start)} – {date_label(end)}"
    elif preset == "Sejak awal":
        start, end = data_min, data_max
        label = f"Sejak {date_label(data_min)}"
    else:
        end = data_max
        start = max(data_min, end - pd.DateOffset(years=PERIOD_YEARS[preset]))
        label = preset

    if start > end:
        st.error("Tanggal awal melewati tanggal akhir. Menggunakan seluruh periode data.")
        start, end = data_min, data_max
    return start.normalize(), end.normalize(), label


def date_range_caption(start: pd.Timestamp, end: pd.Timestamp) -> str:
    return f"{date_label(start)} sampai {date_label(end)}"


def today() -> date:
    return date.today()
