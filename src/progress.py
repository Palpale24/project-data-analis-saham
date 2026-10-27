"""Menyimpan progres belajar secara lokal dalam file JSON."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

from src.config import PROGRESS_FILE

WIB = ZoneInfo("Asia/Jakarta")
PASSING_SCORE = 2  # minimal 2 dari 3 jawaban benar


def _default_progress() -> dict:
    return {
        "completed_lessons": [],
        "quiz_scores": {},
        "last_lesson": "m1l1",
        "updated_at": None,
    }


def load_progress(path: Path | str = PROGRESS_FILE) -> dict:
    path = Path(path)
    if not path.exists():
        return _default_progress()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        # Simpan file yang rusak agar tidak hilang tanpa jejak, lalu mulai bersih.
        try:
            path.replace(path.with_suffix(".corrupt.json"))
        except OSError:
            pass
        return _default_progress()

    progress = _default_progress()
    if isinstance(data, dict):
        completed = data.get("completed_lessons", [])
        progress["completed_lessons"] = [str(x) for x in completed] if isinstance(completed, list) else []
        scores = data.get("quiz_scores", {})
        progress["quiz_scores"] = scores if isinstance(scores, dict) else {}
        progress["last_lesson"] = str(data.get("last_lesson", "m1l1"))
        progress["updated_at"] = data.get("updated_at")
    return progress


def save_progress(progress: dict, path: Path | str = PROGRESS_FILE) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    progress = dict(progress)
    progress["updated_at"] = datetime.now(WIB).isoformat(timespec="seconds")
    tmp = path.with_suffix(".tmp.json")
    tmp.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def record_quiz_result(
    lesson_id: str,
    score: int,
    total: int = 3,
    passing_score: int = PASSING_SCORE,
    path: Path | str = PROGRESS_FILE,
) -> tuple[dict, bool]:
    """Simpan skor terbaik dan tandai selesai jika memenuhi syarat.

    Mengembalikan (progress, lulus). Skor rendah tetap dicatat sebagai upaya,
    tetapi tidak membuka pelajaran berikutnya.
    """
    progress = load_progress(path)
    previous = progress["quiz_scores"].get(lesson_id, {})
    previous_score = int(previous.get("score", -1)) if isinstance(previous, dict) else -1
    best_score = max(score, previous_score)
    progress["quiz_scores"][lesson_id] = {
        "score": int(best_score),
        "total": int(total),
        "attempts": int(previous.get("attempts", 0)) + 1 if isinstance(previous, dict) else 1,
    }
    passed = best_score >= passing_score
    if passed and lesson_id not in progress["completed_lessons"]:
        progress["completed_lessons"].append(lesson_id)
    progress["last_lesson"] = lesson_id
    save_progress(progress, path)
    return progress, passed


def set_last_lesson(lesson_id: str, path: Path | str = PROGRESS_FILE) -> dict:
    progress = load_progress(path)
    progress["last_lesson"] = lesson_id
    save_progress(progress, path)
    return progress


def unlocked_lessons(ordered_lesson_ids: Iterable[str], completed: Iterable[str]) -> set[str]:
    """Pelajaran pertama terbuka; pelajaran berikutnya terbuka setelah sebelumnya lulus."""
    ordered = list(ordered_lesson_ids)
    completed_set = set(completed)
    unlocked: set[str] = set()
    previous_completed = True
    for lesson_id in ordered:
        if previous_completed:
            unlocked.add(lesson_id)
        previous_completed = lesson_id in completed_set
    return unlocked


def next_lesson(ordered_lesson_ids: Iterable[str], completed: Iterable[str]) -> str | None:
    ordered = list(ordered_lesson_ids)
    completed_set = set(completed)
    for lesson_id in ordered:
        if lesson_id not in completed_set and lesson_id in unlocked_lessons(ordered, completed_set):
            return lesson_id
    return ordered[-1] if ordered else None


def progress_percent(ordered_lesson_ids: Iterable[str], completed: Iterable[str]) -> float:
    ordered = list(ordered_lesson_ids)
    if not ordered:
        return 0.0
    completed_set = set(completed)
    return len(completed_set.intersection(ordered)) / len(ordered) * 100
