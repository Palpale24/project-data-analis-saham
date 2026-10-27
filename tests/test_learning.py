"""Pengujian konten kurikulum, kuis, dan progres belajar."""

from __future__ import annotations

import json

import pytest

from src.learning_content import MODULES, all_lessons, get_module, ordered_lesson_ids, total_lessons
from src.progress import (
    PASSING_SCORE,
    load_progress,
    next_lesson,
    progress_percent,
    record_quiz_result,
    save_progress,
    unlocked_lessons,
)


def test_struktur_kurikulum():
    assert len(MODULES) == 9
    assert total_lessons() == 18
    ids = ordered_lesson_ids()
    assert len(ids) == 18
    assert len(set(ids)) == 18
    for module in MODULES:
        assert len(module["lessons"]) == 2
        assert module["number"] == int(module["lessons"][0]["id"][1:2])
        for lesson in module["lessons"]:
            assert lesson["title"]
            assert lesson["goal"]
            assert len(lesson["sections"]) >= 2
            assert len(lesson["quiz"]) == 3
            for question in lesson["quiz"]:
                assert len(question["options"]) == 4
                assert 0 <= question["answer"] < 4
                assert question["why"]


def test_get_module_dan_ids():
    module = get_module("m1")
    assert module["number"] == 1
    assert [lesson["id"] for lesson in module["lessons"]] == ["m1l1", "m1l2"]
    assert [lesson["id"] for module in MODULES for lesson in module["lessons"]] == ordered_lesson_ids()


def test_unlock_dan_next_lesson():
    ids = ordered_lesson_ids()
    assert unlocked_lessons(ids, []) == {ids[0]}
    assert next_lesson(ids, []) == ids[0]
    first_three = ids[:3]
    assert unlocked_lessons(ids, first_three[:2]) == set(first_three)
    assert next_lesson(ids, first_three[:2]) == ids[2]


def test_progress_awal(tmp_path):
    progress = load_progress(tmp_path / "progress.json")
    assert progress["completed_lessons"] == []
    assert progress["last_lesson"] == "m1l1"
    assert progress_percent(ordered_lesson_ids(), []) == 0


def test_record_quiz_gagal_lalu_lulus(tmp_path):
    path = tmp_path / "progress.json"
    progress, passed = record_quiz_result("m1l1", score=1, total=3, path=path)
    assert passed is False
    assert progress["completed_lessons"] == []
    assert progress["quiz_scores"]["m1l1"]["score"] == 1
    assert progress["quiz_scores"]["m1l1"]["attempts"] == 1

    progress, passed = record_quiz_result("m1l1", score=PASSING_SCORE, total=3, path=path)
    assert passed is True
    assert "m1l1" in progress["completed_lessons"]
    assert progress["quiz_scores"]["m1l1"]["score"] == PASSING_SCORE
    assert progress["quiz_scores"]["m1l1"]["attempts"] == 2
    assert progress_percent(ordered_lesson_ids(), progress["completed_lessons"]) == pytest.approx(100 / 18)


def test_skor_terbaik_tidak_turun(tmp_path):
    path = tmp_path / "progress.json"
    record_quiz_result("m1l1", score=2, path=path)
    progress, passed = record_quiz_result("m1l1", score=1, path=path)
    assert passed is True
    assert progress["quiz_scores"]["m1l1"]["score"] == 2


def test_progress_file_rusak_disimpan_sebagai_corrupt(tmp_path):
    path = tmp_path / "progress.json"
    path.write_text("{bukan json", encoding="utf-8")
    progress = load_progress(path)
    assert progress["completed_lessons"] == []
    assert (tmp_path / "progress.corrupt.json").exists()


def test_save_progress_menambahkan_timestamp(tmp_path):
    path = tmp_path / "progress.json"
    progress = load_progress(path)
    progress["completed_lessons"] = ["m1l1"]
    save_progress(progress, path)
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw["completed_lessons"] == ["m1l1"]
    assert raw["updated_at"] is not None


def test_semua_pelajaran_punya_isi_minimal():
    for lesson in all_lessons():
        assert len(lesson["summary"]) >= 2
        assert len(lesson["mistakes"]) >= 1
        assert lesson["analogy"].strip()
        assert lesson["example"].strip()
        assert lesson["application"].strip()
