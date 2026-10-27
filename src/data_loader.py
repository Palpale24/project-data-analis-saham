"""Fungsi untuk membaca dataset proyek."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from src.config import (
    HISTORICAL_FILE,
    HISTORICAL_METADATA_FILE,
    SNAPSHOT_FILE,
    TICKERS_FILE,
)


class DataNotFoundError(FileNotFoundError):
    """Dilempar ketika file dataset belum tersedia."""


def _require_file(path: Path) -> Path:
    if not path.exists():
        raise DataNotFoundError(
            f"File data tidak ditemukan: {path}. Jalankan langkah pada README terlebih dahulu."
        )
    return path


def load_snapshot(path: Path | str = SNAPSHOT_FILE) -> pd.DataFrame:
    """Baca snapshot ringkasan harian IDX apa adanya (nama kolom asli)."""
    path = Path(path)
    _require_file(path)
    # sep=None + engine="python" mendeteksi koma/titik koma secara otomatis.
    return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")


def load_historical_prices(path: Path | str = HISTORICAL_FILE) -> pd.DataFrame:
    """Baca data harga historis gabungan yang sudah dinormalisasi."""
    path = Path(path)
    _require_file(path)
    frame = pd.read_csv(path)
    required = {"date", "ticker", "open", "high", "low", "close", "adj_close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Kolom historis tidak lengkap: {sorted(missing)}")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["ticker"] = frame["ticker"].astype(str).str.strip().str.upper()
    for column in ["open", "high", "low", "close", "adj_close", "volume"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.sort_values(["ticker", "date"]).reset_index(drop=True)


def load_metadata(path: Path | str = HISTORICAL_METADATA_FILE) -> dict:
    path = Path(path)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_tickers(path: Path | str = TICKERS_FILE) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        return pd.DataFrame(columns=["ticker", "name", "sector", "is_benchmark"])
    return pd.read_csv(path)


def get_ticker_prices(
    prices: pd.DataFrame,
    ticker: str,
    price_col: str = "adj_close",
) -> pd.Series:
    """Ambil satu seri harga dengan index tanggal dan nama seri = ticker."""
    if price_col not in prices.columns:
        raise ValueError(f"Kolom harga '{price_col}' tidak tersedia")
    subset = prices.loc[prices["ticker"] == ticker, ["date", price_col]].copy()
    subset = subset.dropna().drop_duplicates(subset=["date"]).sort_values("date")
    series = subset.set_index("date")[price_col]
    series.name = ticker
    return series


def latest_close_prices(prices: pd.DataFrame) -> pd.Series:
    """Harga penutupan terakhir (harga biasa) per ticker untuk valuasi portofolio."""
    valid = prices.dropna(subset=["close"]).sort_values("date")
    latest = valid.groupby("ticker", as_index=True)["close"].last()
    return latest
