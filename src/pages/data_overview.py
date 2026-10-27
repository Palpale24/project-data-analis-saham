"""Halaman Data Overview: audit snapshot IDX dan data historis."""

from __future__ import annotations

import json

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.cached_data import (
    get_historical_quality,
    get_metadata,
    get_prices,
    get_snapshot,
    get_snapshot_quality,
    get_snapshot_raw,
    get_tickers,
)
from src.config import BENCHMARK_TICKER, ticker_label
from src.data_loader import DataNotFoundError
from src.ui import (
    badge,
    date_label,
    decimal_pct,
    dataframe_with_format,
    number,
    page_header,
    plotly_style,
    pct,
    rupiah,
    section_heading,
    stat_cards,
)


def _snapshot_tab(clean: pd.DataFrame, report: dict) -> None:
    st.info(
        "Snapshot ini adalah **potret satu hari** (23 Oktober 2026), bukan data historis. "
        "Jangan menghitung tren, return, atau risiko dari tabel ini.",
        icon="📌",
    )
    for warning in report.get("warnings", []):
        st.warning(warning)

    stat_cards(
        [
            {
                "label": "Saham tercatat",
                "value": number(report.get("unique_tickers")),
                "note": f"{number(report.get('rows'))} baris · {number(report.get('columns'))} kolom",
                "tone": "blue",
            },
            {
                "label": "Tanggal data",
                "value": "23 Okt 2026",
                "note": f"{report.get('date_count', 0)} tanggal unik",
                "tone": "warn",
            },
            {
                "label": "Saham diperdagangkan",
                "value": number(report.get("traded_rows")),
                "note": f"{number(report.get('no_trade_rows'))} tanpa volume",
                "tone": "good",
            },
            {
                "label": "Total nilai transaksi",
                "value": rupiah(report.get("total_value"), compact=True),
                "note": "Seluruh saham pada snapshot",
                "tone": "",
            },
        ]
    )
    st.caption(
        f"Missing values: **{number(report.get('missing_values'))}** · "
        f"Duplikat baris: **{number(report.get('duplicate_rows'))}** · "
        f"Open Price 0 pada saham yang tetap diperdagangkan: "
        f"**{number(report.get('zero_open_traded_rows'))}**."
    )

    section_heading("Aktivitas perdagangan terbesar", "Berdasarkan nilai dan volume transaksi pada satu hari tersebut.")
    top_value = clean.nlargest(10, "value").iloc[::-1]
    top_volume = clean.nlargest(10, "volume").iloc[::-1]

    left, right = st.columns(2)
    with left:
        fig = go.Figure(
            go.Bar(
                x=top_value["value"],
                y=[ticker_label(t) for t in top_value["ticker"]],
                orientation="h",
                marker_color="#0F766E",
                customdata=top_value[["company_name"]].values,
                hovertemplate="%{y}<br>%{customdata[0]}<br>Nilai: Rp%{x:,.0f}<extra></extra>",
            )
        )
        plotly_style(fig, "10 Saham dengan Nilai Transaksi Terbesar", "Nilai transaksi (Rp)", "", height=380, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption("Nilai transaksi = harga × volume pada snapshot. Ini bukan ukuran kualitas perusahaan.")
    with right:
        fig = go.Figure(
            go.Bar(
                x=top_volume["volume"],
                y=[ticker_label(t) for t in top_volume["ticker"]],
                orientation="h",
                marker_color="#2563EB",
                customdata=top_volume[["company_name"]].values,
                hovertemplate="%{y}<br>%{customdata[0]}<br>Volume: %{x:,.0f} lembar<extra></extra>",
            )
        )
        plotly_style(fig, "10 Saham dengan Volume Transaksi Terbesar", "Volume (lembar)", "", height=380, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption("Volume tinggi menunjukkan banyak lembar berpindah tangan, bukan jaminan harga akan naik.")

    section_heading("Jelajahi snapshot", "Cari kode atau nama perusahaan. Unduh data lengkap untuk diolah sendiri.")
    search = st.text_input("Cari kode atau nama perusahaan", placeholder="Contoh: BBCA atau Bank")
    filtered = clean.copy()
    if search.strip():
        query = search.strip().lower()
        filtered = filtered[
            filtered["ticker"].str.lower().str.contains(query, na=False)
            | filtered["company_name"].str.lower().str.contains(query, na=False)
        ]

    display = filtered[
        [
            "ticker",
            "company_name",
            "close",
            "change",
            "volume",
            "value",
            "frequency",
            "bid",
            "offer",
            "market_cap",
            "tradeable_pct",
            "foreign_net",
            "traded",
        ]
    ].copy()
    display["ticker"] = display["ticker"].map(ticker_label)
    display["close"] = display["close"].map(lambda v: rupiah(v))
    display["change"] = display["change"].map(lambda v: f"{v:+,.0f}".replace(",", ".") if pd.notna(v) else "—")
    display["volume"] = display["volume"].map(lambda v: number(v))
    display["value"] = display["value"].map(lambda v: rupiah(v, compact=True))
    display["frequency"] = display["frequency"].map(lambda v: number(v))
    display["bid"] = display["bid"].map(lambda v: rupiah(v))
    display["offer"] = display["offer"].map(lambda v: rupiah(v))
    display["market_cap"] = display["market_cap"].map(lambda v: rupiah(v, compact=True))
    display["tradeable_pct"] = display["tradeable_pct"].map(lambda v: decimal_pct(v))
    display["foreign_net"] = display["foreign_net"].map(lambda v: rupiah(v, compact=True))
    display["traded"] = display["traded"].map({True: "Ya", False: "Tidak"})
    display.columns = [
        "Kode",
        "Perusahaan",
        "Penutupan",
        "Selisih",
        "Volume",
        "Nilai",
        "Frekuensi",
        "Bid",
        "Offer",
        "Kapitalisasi",
        "Tradeable/Listed",
        "Asing Net",
        "Ada Transaksi",
    ]
    st.caption(f"Menampilkan {len(display):,} baris.".replace(",", "."))
    dataframe_with_format(display, height=430)

    st.download_button(
        "Unduh snapshot bersih (CSV)",
        data=clean.to_csv(index=False).encode("utf-8"),
        file_name="idx_snapshot_clean.csv",
        mime="text/csv",
        help="File hasil pembersihan; file mentah tetap tersimpan di data/raw.",
    )


def _historical_tab(prices: pd.DataFrame, quality: dict, metadata: dict) -> None:
    st.info(
        "Data historis ini dipakai untuk grafik performa, risiko, korelasi, dan paper trading. "
        "Harga analisis memakai **Adj Close** (disesuaikan untuk split/dividen).",
        icon="📈",
    )
    stat_cards(
        [
            {
                "label": "Ticker historis",
                "value": number(quality.get("tickers")),
                "note": "12 saham + IHSG",
                "tone": "blue",
            },
            {
                "label": "Total baris",
                "value": number(quality.get("rows")),
                "note": f"{number(quality.get('missing_values'))} missing",
                "tone": "good",
            },
            {
                "label": "Periode data",
                "value": "2019–2026",
                "note": f"{date_label(quality.get('date_min'))} – {date_label(quality.get('date_max'))}",
                "tone": "",
            },
            {
                "label": "Duplikat",
                "value": number(quality.get("duplicate_rows")),
                "note": "Berdasarkan tanggal + ticker",
                "tone": "good",
            },
        ]
    )
    st.caption(
        f"Baris volume nol: **{number(quality.get('zero_volume_rows'))}** · "
        f"OHLC tidak wajar: **{number(quality.get('invalid_ohlc_rows'))}**. "
        "Volume nol tidak otomatis dihapus karena bisa berarti saham tidak diperdagangkan."
    )

    per_ticker = quality.get("per_ticker", pd.DataFrame()).copy()
    if not per_ticker.empty:
        per_ticker["Awal"] = per_ticker["Awal"].map(date_label)
        per_ticker["Akhir"] = per_ticker["Akhir"].map(date_label)
        per_ticker["Kelengkapan (%)"] = per_ticker["Kelengkapan (%)"].map(lambda v: decimal_pct(v))
        per_ticker["Harga Disesuaikan Berbeda (%)"] = per_ticker["Harga Disesuaikan Berbeda (%)"].map(
            lambda v: decimal_pct(v)
        )
        section_heading("Kualitas per ticker", "Kelengkapan dihitung terhadap jumlah tanggal unik dalam dataset.")
        dataframe_with_format(per_ticker, height=440)

        fig = go.Figure(
            go.Bar(
                x=per_ticker["Ticker"],
                y=per_ticker["Baris"],
                marker_color="#0F766E",
                hovertemplate="%{x}<br>%{y:,} baris<extra></extra>",
            )
        )
        plotly_style(fig, "Jumlah Baris per Ticker", "Ticker", "Jumlah baris", height=340, show_legend=False)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        st.caption(
            "GOTO memiliki riwayat lebih pendek karena baru tercatat pada 2022. Perbandingan performa "
            "di halaman lain akan dimulai pada tanggal yang sama agar adil."
        )

    st.download_button(
        "Unduh ringkasan kualitas (CSV)",
        data=per_ticker.to_csv(index=False).encode("utf-8") if not per_ticker.empty else b"",
        file_name="historical_quality_per_ticker.csv",
        mime="text/csv",
    )


def _source_tab(metadata: dict, quality: dict) -> None:
    st.markdown(
        """
        **Sumber snapshot:** file `Ringkasan Saham-20261023.csv` yang disalin ke
        `data/raw/idx_daily_summary_20261023.csv`. File asli di root proyek tidak diubah.

        **Sumber historis:** Yahoo Finance melalui library `yfinance`, dengan `auto_adjust=False`.
        Kolom `Adj Close` dipakai untuk analisis return jangka panjang. Ini sumber pihak ketiga,
        bukan pengganti laporan resmi BEI atau perusahaan.
        """
    )
    if metadata:
        details = {
            "Sumber": metadata.get("source"),
            "URL sumber": metadata.get("source_url"),
            "Diambil (WIB)": metadata.get("retrieved_at_wib"),
            "Mulai diminta": metadata.get("requested_start"),
            "Akhir eksklusif": metadata.get("requested_end_exclusive"),
            "Baris": metadata.get("total_rows"),
            "Ticker": metadata.get("total_tickers"),
            "Rentang aktual": f"{metadata.get('date_min')} s/d {metadata.get('date_max')}",
            "Gagal": len(metadata.get("failures", [])),
        }
        st.dataframe(pd.DataFrame([details]), width="stretch", hide_index=True)
        with st.expander("Catatan sumber data"):
            for note in metadata.get("notes", []):
                st.markdown(f"- {note}")
        with st.expander("Metadata lengkap (JSON)"):
            st.code(json.dumps(metadata, indent=2, ensure_ascii=False), language="json")
    else:
        st.warning("Metadata historis tidak ditemukan. Jalankan ulang `scripts/fetch_data.py`.")

    section_heading("Keterbatasan yang harus diingat")
    st.markdown(
        """
        - Yahoo Finance dapat terlambat, tidak lengkap, atau mengubah data tanpa pemberitahuan.
        - Harga adjusted mengikuti metode vendor; tidak selalu identik dengan perhitungan resmi.
        - Snapshot IDX hanya satu hari, sehingga tidak bisa dipakai untuk tren atau risiko.
        - Dataset tidak mencakup seluruh saham BEI dan bisa memiliki **survivorship bias**
          jika dipakai untuk menguji strategi jangka panjang.
        - Korelasi dan backtest dihitung dari periode historis; hasilnya bukan ramalan.
        - Data fundamental perusahaan nyata belum tersedia di proyek ini.
        """
    )
    st.download_button(
        "Unduh metadata (JSON)",
        data=json.dumps(metadata, indent=2, ensure_ascii=False).encode("utf-8") if metadata else b"{}",
        file_name="historical_metadata.json",
        mime="application/json",
    )


def _reading_tab() -> None:
    st.markdown(
        """
        ### Istilah pada snapshot IDX

        - **Kode Saham**: singkatan perusahaan di bursa, misalnya BBCA.
        - **Sebelumnya**: harga penutupan hari sebelumnya.
        - **Open Price**: harga pembukaan. Nilai 0 pada snapshot ini diperlakukan sebagai tidak tersedia.
        - **Tertinggi / Terendah**: harga tertinggi dan terendah pada hari itu.
        - **Penutupan**: harga terakhir yang tercatat.
        - **Volume**: jumlah lembar yang diperdagangkan.
        - **Nilai**: nilai transaksi dalam rupiah.
        - **Frekuensi**: jumlah transaksi.
        - **Bid / Offer**: harga permintaan beli dan penawaran jual terbaik.
        - **Foreign Sell / Foreign Buy**: transaksi asing menurut catatan sumber.
        - **Listed Shares**: jumlah saham tercatat.
        - **Tradeble Shares / Tradeable Shares**: jumlah saham yang tercatat dapat diperdagangkan menurut snapshot. Pada file ini nilainya hampir selalu sama dengan saham tercatat, sehingga **bukan free float sebenarnya**.

        ### Istilah pada data historis

        - **Close**: harga penutupan biasa.
        - **Adj Close**: harga yang disesuaikan untuk split dan dividen; dipakai untuk return.
        - **Volume**: jumlah lembar; volume 0 tidak selalu berarti data hilang.
        - **Missing**: nilai kosong. Jangan diisi dengan tebakan tanpa alasan.
        - **Duplikat**: kombinasi tanggal dan ticker yang muncul lebih dari sekali.

        ### Mengapa satu hari tidak cukup

        Return membutuhkan minimal dua harga. Volatilitas membutuhkan banyak return harian.
        Maximum drawdown membutuhkan rangkaian harga dari puncak ke lembah. Snapshot satu hari
        tidak memiliki informasi itu, sehingga aplikasi **tidak** membuat grafik tren dari snapshot.
        """
    )


def render() -> None:
    page_header(
        "Data Overview",
        "Audit data sebelum percaya pada angka. Halaman ini memisahkan snapshot satu hari dari data historis.",
        "Langkah 1 · kenali data",
    )
    try:
        raw = get_snapshot_raw()
        clean = get_snapshot()
        report = get_snapshot_quality()
    except (DataNotFoundError, ValueError) as exc:
        st.error(f"Snapshot IDX tidak dapat dibaca: {exc}")
        return

    st.markdown(
        f"File mentah: `data/raw/idx_daily_summary_20261023.csv` · "
        f"{number(report.get('rows'))} baris · {number(report.get('columns'))} kolom · "
        f"{badge('Snapshot satu hari', 'amber')} {badge('File asli dipertahankan', 'teal')}",
        unsafe_allow_html=True,
    )

    try:
        prices = get_prices()
        historical_quality = get_historical_quality()
        metadata = get_metadata()
        tickers = get_tickers()
    except (DataNotFoundError, ValueError) as exc:
        st.warning(f"Data historis belum siap: {exc}")
        prices = pd.DataFrame()
        historical_quality = {}
        metadata = {}
        tickers = pd.DataFrame()

    tab_snapshot, tab_historical, tab_source, tab_reading = st.tabs(
        ["Snapshot IDX", "Data Historis", "Sumber & Kualitas", "Cara Membaca"]
    )
    with tab_snapshot:
        _snapshot_tab(clean, report)
    with tab_historical:
        if prices.empty:
            st.info("Data historis belum tersedia. Jalankan `python scripts/fetch_data.py`.")
        else:
            _historical_tab(prices, historical_quality, metadata)
    with tab_source:
        _source_tab(metadata, historical_quality)
    with tab_reading:
        _reading_tab()
