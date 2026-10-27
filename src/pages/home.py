"""Halaman Beranda dan Pusat Belajar."""

from __future__ import annotations

import html

import streamlit as st

from src.config import INITIAL_CAPITAL, ticker_label
from src.cached_data import get_metadata
from src.learning_content import (
    MODULES,
    all_lessons,
    get_lesson,
    get_module,
    ordered_lesson_ids,
    total_lessons,
)
from src.pages.lesson_renderer import _go_to_lesson, render_lesson
from src.progress import (
    load_progress,
    next_lesson,
    progress_percent,
    unlocked_lessons,
)
from src.ui import badge, hero, page_header, section_heading, stat_cards


def _sync_selected() -> None:
    st.session_state["selected_lesson_id"] = st.session_state["lesson_select"]


def _render_progress() -> None:
    progress = load_progress()
    ids = ordered_lesson_ids()
    completed = progress.get("completed_lessons", [])
    percent = progress_percent(ids, completed)
    st.markdown("### Perjalanan belajarmu")
    st.progress(min(100, int(percent)), text=f"{len(completed)} dari {len(ids)} pelajaran selesai ({percent:.0f}%)")
    st.caption(
        "Progres disimpan di `data/user/learning_progress.json`. Pelajaran berikutnya terbuka setelah "
        "kamu lulus kuis minimal 2 dari 3."
    )


def _render_learning_tab() -> None:
    progress = load_progress()
    ids = ordered_lesson_ids()
    completed = progress.get("completed_lessons", [])
    unlocked = unlocked_lessons(ids, completed)
    default_id = progress.get("last_lesson") if progress.get("last_lesson") in unlocked else next_lesson(ids, completed)
    if default_id not in ids:
        default_id = ids[0]

    _render_progress()

    if "lesson_select" not in st.session_state:
        st.session_state["lesson_select"] = default_id
    if st.session_state.get("lesson_select") not in ids:
        st.session_state["lesson_select"] = default_id

    labels = {}
    for lesson in all_lessons():
        module = get_module(lesson["id"][:2])
        status = "✅" if lesson["id"] in completed else ("🔓" if lesson["id"] in unlocked else "🔒")
        labels[lesson["id"]] = f"{status} Modul {module['number']} · {lesson['title']}"

    selected_id = st.selectbox(
        "Pilih pelajaran",
        ids,
        format_func=lambda lesson_id: labels.get(lesson_id, lesson_id),
        key="lesson_select",
        on_change=_sync_selected,
        help="Pelajaran terkunci akan terbuka setelah pelajaran sebelumnya lulus.",
    )
    st.session_state["selected_lesson_id"] = selected_id
    selected = get_lesson(selected_id)
    module = get_module(selected_id[:2])

    st.divider()
    if selected_id not in unlocked:
        index = ids.index(selected_id)
        previous_id = ids[index - 1] if index > 0 else ids[0]
        previous = get_lesson(previous_id)
        st.warning(
            f"Pelajaran **{selected['title']}** masih terkunci. Selesaikan dulu "
            f"**{previous['title']}** dengan minimal 2 dari 3 jawaban benar.",
            icon="🔒",
        )
        if st.button(
            f"Buka pelajaran sebelumnya: {previous['title']}",
            type="primary",
            on_click=_go_to_lesson,
            args=(previous_id,),
        ):
            pass
        return

    render_lesson(selected, module, progress)


def _module_cards() -> None:
    progress = load_progress()
    completed = set(progress.get("completed_lessons", []))
    columns = st.columns(3)
    for index, module in enumerate(MODULES):
        module_lessons = module["lessons"]
        done = sum(1 for lesson in module_lessons if lesson["id"] in completed)
        status = "Selesai" if done == len(module_lessons) else ("Sedang dipelajari" if done else "Belum dimulai")
        tone = "teal" if done == len(module_lessons) else ("amber" if done else "gray")
        css_class = "done" if done == len(module_lessons) else ""
        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="module-card {css_class}">
                    <div class="module-top">
                        <span class="module-kicker">Modul {module['number']}</span>
                        <span class="module-icon">{module['icon']}</span>
                    </div>
                    <div class="module-title">{html.escape(module['title'])}</div>
                    <p class="module-desc">{html.escape(module['description'])}</p>
                    <div style="margin-top:.55rem; display:flex; gap:.35rem; flex-wrap:wrap;">
                        {badge(f"{done}/{len(module_lessons)} pelajaran", tone)}
                        {badge(status, tone)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")


def _render_map_tab() -> None:
    section_heading(
        "Peta 9 modul",
        "Kurikulum disusun bertahap. Kamu tidak perlu menyelesaikan semuanya hari ini.",
    )
    _module_cards()
    st.markdown("### Daftar pelajaran")
    progress = load_progress()
    completed = set(progress.get("completed_lessons", []))
    unlocked = unlocked_lessons(ordered_lesson_ids(), completed)
    for module in MODULES:
        with st.expander(f"Modul {module['number']} — {module['title']}", expanded=False):
            for lesson in module["lessons"]:
                if lesson["id"] in completed:
                    status = "✅ Selesai"
                elif lesson["id"] in unlocked:
                    status = "🔓 Terbuka"
                else:
                    status = "🔒 Terkunci"
                st.markdown(
                    f"**{lesson['title']}** · ±{lesson['minutes']} menit · {status}  \n"
                    f"{lesson['goal']}"
                )


def _render_about_tab() -> None:
    section_heading(
        "Apa yang bisa dilakukan aplikasi ini?",
        "Semua fitur dirancang untuk belajar, bukan untuk mengirim order nyata.",
    )
    capabilities = [
        ("📊 Data Overview", "Melihat kualitas snapshot IDX dan data historis, termasuk missing, duplikat, dan peringatan."),
        ("📈 Performa Saham", "Membandingkan harga ternormalisasi, return, CAGR, moving average, dan IHSG."),
        ("🛡️ Analisis Risiko", "Menghitung volatilitas, maximum drawdown, distribusi return, dan VaR historis sederhana."),
        ("🔗 Korelasi Saham", "Heatmap korelasi return untuk melihat saham yang bergerak mirip."),
        ("🧾 Fundamental", "Latihan membaca laporan keuangan lewat perusahaan fiktif dan kalkulator rasio."),
        ("🧮 Simulasi Rp700.000", "Menghitung lot, biaya, laba/rugi bersih, dan skenario harga turun/naik."),
        ("📝 Paper Trading", "Mencatat transaksi virtual beserta alasan dan evaluasi di CSV lokal."),
        ("🔎 Riset Saham", "Tabel metrik historis dengan kriteria transparan, tanpa label 'pasti untung'."),
    ]
    columns = st.columns(2)
    for index, (title, description) in enumerate(capabilities):
        with columns[index % 2]:
            st.markdown(
                f'<div class="soft-card" style="margin-bottom:.7rem;"><strong>{html.escape(title)}</strong>'
                f'<p>{html.escape(description)}</p></div>',
                unsafe_allow_html=True,
            )

    section_heading("Status data saat ini")
    metadata = get_metadata()
    if metadata:
        stat_cards(
            [
                {
                    "label": "Snapshot IDX",
                    "value": "963 saham",
                    "note": "Satu tanggal: 23 Okt 2026",
                    "tone": "warn",
                },
                {
                    "label": "Data historis",
                    "value": f"{metadata.get('total_tickers', '—')} ticker",
                    "note": f"{metadata.get('date_min', '—')} s/d {metadata.get('date_max', '—')}",
                    "tone": "good",
                },
                {
                    "label": "Sumber historis",
                    "value": "Yahoo Finance",
                    "note": "Pihak ketiga, perlu verifikasi",
                    "tone": "blue",
                },
                {
                    "label": "Baris historis",
                    "value": f"{metadata.get('total_rows', 0):,}".replace(",", "."),
                    "note": f"Diambil {metadata.get('retrieved_at_wib', '—')[:10]}",
                    "tone": "",
                },
            ]
        )
        st.warning(
            "Snapshot 23 Oktober 2026 hanya potret satu hari. Grafik tren dan risiko **tidak** dihitung "
            "dari snapshot tersebut; analisis historis memakai data 2019–2026 dari Yahoo Finance.",
            icon="⚠️",
        )
    else:
        st.info("Metadata data historis belum tersedia. Jalankan `python scripts/fetch_data.py`.")

    section_heading("Cara memakai proyek ini")
    st.markdown(
        """
        1. **Belajar bertahap** di tab Belajar. Selesaikan satu pelajaran, jawab tiga pertanyaan, lalu lanjut.
        2. **Buka halaman analisis** di sidebar untuk melihat data, performa, risiko, dan korelasi.
        3. **Uji keputusan tanpa uang nyata** lewat Simulasi Rp700.000 dan Paper Trading.
        4. **Baca keterbatasan** di README dan di bagian bawah setiap halaman. Data pihak ketiga bisa keliru.
        """
    )

    section_heading("Batas penting")
    st.markdown(
        """
        - Aplikasi **tidak terhubung ke broker** dan tidak mengirim order.
        - Data Yahoo Finance bukan sumber resmi BEI; bisa tertunda atau tidak lengkap.
        - Data fundamental perusahaan nyata **belum tersedia**; halaman Fundamental hanya memakai contoh fiktif.
        - Hasil simulasi dan backtest bukan jaminan hasil masa depan.
        - Proyek ini tidak memberi rekomendasi beli/jual.
        """
    )


def render() -> None:
    progress = load_progress()
    ids = ordered_lesson_ids()
    completed = progress.get("completed_lessons", [])
    percent = progress_percent(ids, completed)
    metadata = get_metadata()

    hero(
        "Stock Learning & Indonesian Market Analytics",
        "Belajar saham Indonesia dari nol, mengolah data dengan Python, dan menguji keputusan tanpa "
        "mempertaruhkan uang nyata. Mulai dari satu pertanyaan: apa yang sebenarnya saya beli?",
        "Proyek belajar · data analyst · versi lokal",
        [
            "9 modul · 18 pelajaran",
            "963 saham snapshot IDX",
            "12 saham + IHSG",
            "Modal simulasi Rp700.000",
        ],
    )

    stat_cards(
        [
            {
                "label": "Progres belajar",
                "value": f"{len(completed)}/{total_lessons()}",
                "note": f"{percent:.0f}% pelajaran selesai",
                "tone": "good",
            },
            {
                "label": "Data historis",
                "value": f"{metadata.get('total_tickers', '—')} ticker",
                "note": f"{metadata.get('date_min', '—')} s/d {metadata.get('date_max', '—')}",
                "tone": "blue",
            },
            {
                "label": "Snapshot IDX",
                "value": "963 saham",
                "note": "Satu hari: 23 Okt 2026",
                "tone": "warn",
            },
            {
                "label": "Uang nyata yang dipakai",
                "value": "Rp0",
                "note": "Semua transaksi di sini virtual",
                "tone": "",
            },
        ]
    )

    st.write("")
    tab_belajar, tab_peta, tab_tentang = st.tabs(["📖 Belajar", "🗺️ Peta Kurikulum", "ℹ️ Tentang Proyek"])
    with tab_belajar:
        _render_learning_tab()
    with tab_peta:
        _render_map_tab()
    with tab_tentang:
        _render_about_tab()
