"""Aplikasi Streamlit: navigasi utama proyek belajar saham Indonesia."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.cached_data import get_metadata  # noqa: E402
from src.learning_content import ordered_lesson_ids, total_lessons  # noqa: E402
from src.pages import (  # noqa: E402
    correlation,
    data_overview,
    fundamental,
    home,
    paper_trading,
    performance,
    research,
    risk,
    simulation,
)
from src.progress import load_progress, progress_percent  # noqa: E402
from src.ui import disclaimer, inject_css  # noqa: E402

PAGES = {
    "🏠 Beranda & Belajar": home.render,
    "📊 Data Overview": data_overview.render,
    "📈 Performa Saham": performance.render,
    "🛡️ Analisis Risiko": risk.render,
    "🔗 Korelasi Saham": correlation.render,
    "🧾 Fundamental": fundamental.render,
    "🧮 Simulasi Rp700.000": simulation.render,
    "📝 Paper Trading": paper_trading.render,
    "🔎 Riset Saham": research.render,
}


def _sidebar() -> str:
    with st.sidebar:
        st.markdown(
            """
            <div class="side-brand">
                <div class="side-brand-mark">S</div>
                <div>
                    <div class="side-brand-name">SahamLab</div>
                    <div class="side-brand-sub">Belajar · Analisis · Simulasi</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(
            "Ruang belajar saham Indonesia dari nol. Semua data dan transaksi di sini bersifat edukasi."
        )
        st.divider()

        page = st.radio("Menu", list(PAGES), key="nav_page")

        st.divider()
        progress = load_progress()
        ids = ordered_lesson_ids()
        completed = progress.get("completed_lessons", [])
        percent = progress_percent(ids, completed)
        st.caption(f"Progres belajar: **{len(completed)}/{total_lessons()}** pelajaran")
        st.progress(min(100, int(percent)) / 100, text=f"{percent:.0f}% selesai")

        metadata = get_metadata()
        if metadata:
            st.caption(
                f"Data historis: **{metadata.get('total_tickers', '—')} ticker** "
                f"({metadata.get('date_min', '—')} s.d. {metadata.get('date_max', '—')}). "
                "Sumber: Yahoo Finance."
            )
        else:
            st.caption("Data historis belum tersedia. Jalankan `python scripts/fetch_data.py`.")

        st.divider()
        st.caption("🔒 Tidak terhubung ke broker. Tidak ada order nyata.")
        st.caption("Dibuat untuk latihan, bukan rekomendasi investasi.")
    return page


def main() -> None:
    st.set_page_config(
        page_title="SahamLab — Belajar Saham Indonesia",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()
    page = _sidebar()
    PAGES[page]()
    disclaimer()


if __name__ == "__main__":
    main()
