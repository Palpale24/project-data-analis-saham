"""Smoke test aplikasi Streamlit untuk semua halaman."""

from __future__ import annotations

from pathlib import Path

import pytest

streamlit = pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    "🏠 Beranda & Belajar",
    "📊 Data Overview",
    "📈 Performa Saham",
    "🛡️ Analisis Risiko",
    "🔗 Korelasi Saham",
    "🧾 Fundamental",
    "🧮 Simulasi Rp700.000",
    "📝 Paper Trading",
    "🔎 Riset Saham",
]


@pytest.fixture
def app() -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=90)
    at.run()
    return at


def _go(app: AppTest, page: str) -> AppTest:
    nav = next(item for item in app.radio if item.label == "Menu")
    nav.set_value(page).run()
    return app


def test_beranda_tanpa_error(app):
    assert not app.exception
    assert any("SahamLab" in str(markdown.value) for markdown in app.markdown)


def test_semua_halaman_tanpa_error(app):
    for page in PAGES:
        _go(app, page)
        errors = [str(item.value) for item in app.exception]
        assert not errors, f"{page} menghasilkan error: {errors}"
        nav = next(item for item in app.radio if item.label == "Menu")
        assert nav.value == page


def test_halaman_simulasi_menampilkan_hasil_default(app):
    _go(app, "🧮 Simulasi Rp700.000")
    assert not app.exception
    text = " ".join(str(item.value) for item in app.markdown)
    assert "Rp700.000" in text or "Rp 700.000" in text or "Simulasi" in text
    assert len(app.dataframe) >= 1


def test_halaman_riset_menampilkan_tabel(app):
    _go(app, "🔎 Riset Saham")
    assert not app.exception
    assert len(app.dataframe) >= 1
    frame = app.dataframe[0].value
    assert not frame.empty
    assert "Nama" in frame.columns
