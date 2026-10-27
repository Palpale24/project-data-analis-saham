"""Konfigurasi pusat proyek.

Semua modul memakai path yang berasal dari lokasi file ini, sehingga proyek
tetap berjalan baik ketika dibuka dari VS Code, PowerShell, maupun terminal lain.
"""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
EXTERNAL_DIR = DATA_DIR / "external"
SAMPLE_DIR = DATA_DIR / "sample"
USER_DIR = DATA_DIR / "user"

OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_DIR = OUTPUT_DIR / "reports"
CHART_DIR = OUTPUT_DIR / "charts"

SNAPSHOT_FILE = RAW_DIR / "idx_daily_summary_20261023.csv"
HISTORICAL_RAW_DIR = RAW_DIR / "historical"
HISTORICAL_FILE = PROCESSED_DIR / "historical_prices.csv"
HISTORICAL_METADATA_FILE = RAW_DIR / "historical" / "metadata.json"
TICKERS_FILE = PROCESSED_DIR / "tickers.csv"
SNAPSHOT_CLEAN_FILE = PROCESSED_DIR / "idx_snapshot_clean.csv"
FEATURES_FILE = PROCESSED_DIR / "daily_features.csv"
PROGRESS_FILE = USER_DIR / "learning_progress.json"
PAPER_TRADES_FILE = USER_DIR / "paper_trades.csv"

INITIAL_CAPITAL = 700_000
LOT_SIZE = 100
TRADING_DAYS = 252
BENCHMARK_TICKER = "^JKSE"

# Saham yang diunduh untuk belajar. Bukan daftar rekomendasi beli.
TICKER_META = {
    "BBCA.JK": {"name": "Bank Central Asia", "sector": "Keuangan", "benchmark": False},
    "BBRI.JK": {"name": "Bank Rakyat Indonesia", "sector": "Keuangan", "benchmark": False},
    "BMRI.JK": {"name": "Bank Mandiri", "sector": "Keuangan", "benchmark": False},
    "TLKM.JK": {"name": "Telkom Indonesia", "sector": "Telekomunikasi", "benchmark": False},
    "ASII.JK": {"name": "Astra International", "sector": "Industri", "benchmark": False},
    "ANTM.JK": {"name": "Aneka Tambang", "sector": "Barang Baku", "benchmark": False},
    "ADRO.JK": {"name": "Alamtri Resources", "sector": "Energi", "benchmark": False},
    "AKRA.JK": {"name": "AKR Corporindo", "sector": "Energi", "benchmark": False},
    "ICBP.JK": {"name": "Indofood CBP", "sector": "Konsumen Primer", "benchmark": False},
    "UNVR.JK": {"name": "Unilever Indonesia", "sector": "Konsumen Primer", "benchmark": False},
    "SMGR.JK": {"name": "Semen Indonesia", "sector": "Barang Baku", "benchmark": False},
    "GOTO.JK": {"name": "GoTo Gojek Tokopedia", "sector": "Teknologi", "benchmark": False},
    "^JKSE": {"name": "IHSG (Indeks Harga Saham Gabungan)", "sector": "Benchmark", "benchmark": True},
}

DEFAULT_START_DATE = "2019-01-01"


def ticker_label(ticker: str) -> str:
    """Nama pendek yang ramah untuk ditampilkan di layar."""
    if ticker == BENCHMARK_TICKER:
        return "IHSG"
    return ticker.replace(".JK", "")


def ticker_name(ticker: str) -> str:
    return TICKER_META.get(ticker, {}).get("name", ticker_label(ticker))


def ensure_directories() -> None:
    for folder in [
        RAW_DIR,
        PROCESSED_DIR,
        EXTERNAL_DIR,
        SAMPLE_DIR,
        USER_DIR,
        HISTORICAL_RAW_DIR,
        REPORT_DIR,
        CHART_DIR,
    ]:
        folder.mkdir(parents=True, exist_ok=True)
