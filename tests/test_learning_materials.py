"""Validasi materi belajar yang dibaca di VSCode."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

from src.learning_content import MODULES

ROOT = Path(__file__).resolve().parents[1]
MATERIAL_DIR = ROOT / "notebooks pembelajaran"


def test_notebook_materi_lengkap_dan_valid():
    files = sorted(MATERIAL_DIR.glob("*.ipynb"))
    assert len(files) == len(MODULES) + 1, "Harus ada 1 panduan + 9 notebook modul"

    for path in files:
        notebook = nbf.read(path, as_version=4)
        nbf.validate(notebook)
        assert notebook.cells, f"{path.name} tidak memiliki sel"


def test_semua_pelajaran_dan_kuis_ada_di_materi():
    text = "\n".join(
        "".join(cell.source)
        for path in MATERIAL_DIR.glob("*.ipynb")
        for cell in nbf.read(path, as_version=4).cells
    )

    for module in MODULES:
        assert module["title"] in text, f"Judul modul hilang: {module['title']}"
        for lesson in module["lessons"]:
            assert lesson["title"] in text, f"Pelajaran hilang: {lesson['title']}"
            for quiz in lesson["quiz"]:
                assert quiz["q"] in text, f"Soal hilang: {quiz['q']}"
