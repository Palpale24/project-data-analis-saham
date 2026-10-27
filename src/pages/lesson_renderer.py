"""Renderer satu pelajaran dan kuisnya."""

from __future__ import annotations

import html

import streamlit as st

from src.learning_content import get_lesson, lesson_number, ordered_lesson_ids
from src.progress import PASSING_SCORE, record_quiz_result
from src.ui import badge, clean_md


def _go_to_lesson(lesson_id: str) -> None:
    st.session_state["lesson_select"] = lesson_id
    st.session_state["selected_lesson_id"] = lesson_id


def render_lesson(lesson: dict, module: dict, progress: dict) -> None:
    lesson_id = lesson["id"]
    completed = lesson_id in progress.get("completed_lessons", [])
    score_info = progress.get("quiz_scores", {}).get(lesson_id, {})
    best_score = score_info.get("score") if isinstance(score_info, dict) else None

    st.markdown(
        f"""
        <div class="lesson-meta">
            {badge(f"Modul {module['number']}", 'teal')}
            {badge(f"Pelajaran {lesson_number(lesson_id)} dari {len(ordered_lesson_ids())}", 'gray')}
            {badge(f"± {lesson['minutes']} menit", 'blue')}
            {badge('Selesai' if completed else 'Belum selesai', 'teal' if completed else 'amber')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"## {lesson['title']}")
    st.markdown(f"**Tujuan sesi ini:** {lesson['goal']}")

    if best_score is not None:
        st.caption(
            f"Skor kuis terbaik: **{best_score}/3**. "
            f"Ambang lulus {PASSING_SCORE}/3. Kamu boleh mengulang kapan saja."
        )

    st.markdown("### 1. Materi hari ini")
    for section in lesson["sections"]:
        st.markdown(f"#### {section['heading']}")
        st.markdown(clean_md(section["body"]))

    st.markdown("### 2. Analogi kehidupan sehari-hari")
    st.info(clean_md(lesson["analogy"]), icon="🌏")

    st.markdown("### 3. Contoh angka")
    st.markdown(clean_md(lesson["example"]))

    st.markdown("### 4. Penerapan dalam investasi saham")
    st.markdown(clean_md(lesson["application"]))

    if lesson.get("python"):
        st.markdown("### 5. Praktik Python (opsional)")
        st.markdown(clean_md(lesson["python"]))
        st.caption(
            "Jalankan kode di notebook atau terminal Python. Jangan menyalin kode yang tidak dipahami; "
            "ubah satu angka dan lihat apa yang terjadi."
        )

    st.markdown("### 6. Kesalahan yang sering dilakukan pemula")
    for mistake in lesson["mistakes"]:
        st.markdown(f"- {mistake}")

    st.markdown("### 7. Rangkuman")
    for item in lesson["summary"]:
        st.markdown(f"- {item}")

    st.markdown("### 8. Tiga pertanyaan latihan")
    st.caption("Jawab ketiganya. Minimal 2 benar untuk membuka pelajaran berikutnya. Tidak ada penalti untuk mencoba lagi.")

    feedback_key = f"quiz_feedback_{lesson_id}"
    feedback = st.session_state.get(feedback_key)

    with st.form(key=f"quiz_form_{lesson_id}"):
        answers: list[int | None] = []
        for index, question in enumerate(lesson["quiz"], start=1):
            options = [f"{chr(64 + i)}. {option}" for i, option in enumerate(question["options"], start=1)]
            choice = st.radio(
                f"{index}. {question['q']}",
                options,
                index=None,
                key=f"quiz_{lesson_id}_{index}",
            )
            answers.append(options.index(choice) if choice in options else None)
        submitted = st.form_submit_button("Periksa jawaban", type="primary", width="stretch")

    if submitted:
        if any(answer is None for answer in answers):
            st.warning("Masih ada pertanyaan yang belum dijawab. Isi ketiganya dulu, ya.")
        else:
            score = sum(
                1 for answer, question in zip(answers, lesson["quiz"]) if answer == question["answer"]
            )
            passed = score >= PASSING_SCORE
            record_quiz_result(lesson_id, score=score, total=len(lesson["quiz"]))
            st.session_state[feedback_key] = {
                "score": score,
                "passed": passed,
                "answers": answers,
            }
            st.rerun()

    if feedback:
        score = int(feedback["score"])
        passed = bool(feedback["passed"])
        if passed:
            st.success(
                f"Benar **{score} dari 3**. Kamu lulus dan pelajaran berikutnya sudah terbuka.",
                icon="✅",
            )
        else:
            st.error(
                f"Benar **{score} dari 3**. Belum lulus; baca ulang bagian yang belum jelas lalu coba lagi. "
                "Ini latihan, bukan ujian yang harus sempurna.",
                icon="📚",
            )

        for index, (answer, question) in enumerate(zip(feedback["answers"], lesson["quiz"]), start=1):
            correct_text = question["options"][question["answer"]]
            is_correct = answer == question["answer"]
            with st.expander(
                f"{'✅' if is_correct else '❌'} Pertanyaan {index} — "
                f"{'benar' if is_correct else 'belum tepat'}",
                expanded=not is_correct,
            ):
                st.markdown(f"**Pertanyaan:** {question['q']}")
                if answer is not None:
                    st.markdown(f"**Jawabanmu:** {question['options'][answer]}")
                st.markdown(f"**Jawaban benar:** {correct_text}")
                st.markdown(f"**Penjelasan:** {question['why']}")

        if passed:
            ids = ordered_lesson_ids()
            current_index = ids.index(lesson_id)
            if current_index + 1 < len(ids):
                next_id = ids[current_index + 1]
                next_lesson = get_lesson(next_id)
                st.button(
                    f"Lanjut ke: {next_lesson['title']} →",
                    type="primary",
                    on_click=_go_to_lesson,
                    args=(next_id,),
                    key=f"next_{lesson_id}",
                )
            else:
                st.balloons()
                st.success(
                    "Kamu sudah menyelesaikan seluruh 18 pelajaran. Ini baru awal: lanjutkan dengan "
                    "membaca laporan perusahaan nyata dan mengisi jurnal paper trading.",
                    icon="🎓",
                )

    st.markdown("### 9. Syarat melanjutkan")
    if completed:
        st.markdown(
            "Pelajaran ini **sudah selesai**. Pelajaran berikutnya terbuka. Kamu tetap bisa mengulang "
            "materi ini kapan saja."
        )
    else:
        st.markdown(
            "Dapatkan minimal **2 dari 3** jawaban benar. Setelah lulus, tombol menuju pelajaran "
            "berikutnya akan muncul. Progres disimpan otomatis di komputer ini."
        )

    st.caption(
        "Catatan: materi ini edukasi, bukan rekomendasi saham. Jika ada istilah atau angka yang belum jelas, "
        "tanyakan sebelum melanjutkan."
    )
