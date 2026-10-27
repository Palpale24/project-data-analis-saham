"""Pembungkus cache Streamlit agar file besar tidak dibaca berulang kali."""

from __future__ import annotations

import streamlit as st

from src.data_cleaning import (
    clean_historical,
    clean_snapshot,
    historical_quality_report,
    snapshot_quality_report,
)
from src.data_loader import (
    load_historical_prices,
    load_metadata,
    load_snapshot,
    load_tickers,
)


@st.cache_data(show_spinner=False, ttl=600)
def get_snapshot_raw():
    return load_snapshot()


@st.cache_data(show_spinner=False, ttl=600)
def get_snapshot():
    return clean_snapshot(load_snapshot())


@st.cache_data(show_spinner=False, ttl=600)
def get_snapshot_quality():
    raw = load_snapshot()
    clean = clean_snapshot(raw)
    return snapshot_quality_report(raw, clean)


@st.cache_data(show_spinner=False, ttl=600)
def get_prices():
    return clean_historical(load_historical_prices())


@st.cache_data(show_spinner=False, ttl=600)
def get_historical_quality():
    return historical_quality_report(clean_historical(load_historical_prices()))


@st.cache_data(show_spinner=False, ttl=600)
def get_metadata():
    return load_metadata()


@st.cache_data(show_spinner=False, ttl=600)
def get_tickers():
    return load_tickers()


@st.cache_data(show_spinner=False, ttl=600)
def get_available_stocks():
    prices = clean_historical(load_historical_prices())
    return sorted(t for t in prices["ticker"].unique() if not str(t).startswith("^"))


@st.cache_data(show_spinner=False, ttl=600)
def get_benchmark_prices():
    prices = clean_historical(load_historical_prices())
    return prices.loc[prices["ticker"] == "^JKSE"].copy()
