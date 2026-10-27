"""Mengunduh data harga historis dari Yahoo Finance.

Contoh pemakaian dari folder proyek:

    python scripts/fetch_data.py
    python scripts/fetch_data.py --start 2020-01-01

Data mentah per saham disimpan di data/raw/historical/ dan gabungannya di
data/processed/historical_prices.csv. Sumber pihak ketiga dapat berubah,
terlambat, atau memiliki data yang tidak lengkap. Selalu cek ulang untuk
keputusan penting.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import (  # noqa: E402
    BENCHMARK_TICKER,
    DEFAULT_START_DATE,
    HISTORICAL_FILE,
    HISTORICAL_METADATA_FILE,
    HISTORICAL_RAW_DIR,
    PROCESSED_DIR,
    TICKERS_FILE,
    TICKER_META,
    ensure_directories,
)

WIB = ZoneInfo("Asia/Jakarta")


def download_one(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Unduh satu ticker. end bersifat eksklusif di Yahoo Finance."""
    import yfinance as yf

    frame = yf.Ticker(ticker).history(
        start=start,
        end=end,
        auto_adjust=False,
        actions=False,
        timeout=30,
    )
    if frame.empty:
        raise ValueError("Yahoo Finance mengembalikan data kosong")

    frame = frame.reset_index()
    frame.columns = [str(c).lower().replace(" ", "_") for c in frame.columns]
    if "date" not in frame.columns:
        raise ValueError(f"Kolom tanggal tidak ditemukan: {frame.columns.tolist()}")

    # Yahoo mengembalikan tanggal dengan zona waktu bursa (mis. +07:00).
    # Jangan konversi ke UTC karena tanggal lokal bisa bergeser satu hari.
    dates = pd.to_datetime(frame["date"], errors="coerce")
    if getattr(dates.dt, "tz", None) is not None:
        dates = dates.dt.tz_localize(None)
    frame["date"] = dates.dt.normalize()
    frame = frame.dropna(subset=["date"]).copy()

    required = ["open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in frame.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak lengkap: {missing}")

    if "adj_close" not in frame.columns:
        # Jika versi library tidak menyediakan adj_close, close dipakai dan
        # dicatat sebagai keterbatasan, bukan dianggap sudah disesuaikan.
        frame["adj_close"] = frame["close"]

    for col in ["open", "high", "low", "close", "adj_close", "volume"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")

    frame = frame[["date", "open", "high", "low", "close", "adj_close", "volume"]]
    frame = frame.drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
    frame = frame[(frame["close"] > 0) & (frame["adj_close"] > 0)]
    if frame.empty:
        raise ValueError("Semua baris tidak valid setelah pembersihan awal")
    frame["ticker"] = ticker
    return frame


def main() -> int:
    parser = argparse.ArgumentParser(description="Unduh data historis saham Indonesia")
    parser.add_argument("--start", default=DEFAULT_START_DATE, help="Tanggal mulai YYYY-MM-DD")
    parser.add_argument(
        "--end",
        default=date.today().isoformat(),
        help="Tanggal akhir eksklusif YYYY-MM-DD (default: hari ini, agar bar hari ini yang belum selesai tidak ikut)",
    )
    parser.add_argument(
        "--tickers",
        nargs="*",
        default=None,
        help="Daftar ticker opsional, misalnya BBCA.JK TLKM.JK",
    )
    args = parser.parse_args()

    ensure_directories()
    tickers = args.tickers or list(TICKER_META.keys())
    started = datetime.now(WIB)
    frames: list[pd.DataFrame] = []
    success: list[dict] = []
    failures: list[dict] = []

    print(f"Mengunduh {len(tickers)} ticker dari {args.start} sampai {args.end} (eksklusif)...")
    for ticker in tickers:
        try:
            frame = download_one(ticker, args.start, args.end)
            raw_path = HISTORICAL_RAW_DIR / f"{ticker.replace('^', 'INDEX_').replace('.', '_')}.csv"
            frame.to_csv(raw_path, index=False)
            frames.append(frame)
            info = {
                "ticker": ticker,
                "name": TICKER_META.get(ticker, {}).get("name", ticker),
                "rows": int(len(frame)),
                "first_date": frame["date"].min().date().isoformat(),
                "last_date": frame["date"].max().date().isoformat(),
                "raw_file": raw_path.relative_to(ROOT).as_posix(),
            }
            success.append(info)
            print(f"  OK  {ticker:<9} {len(frame):>5} baris  {info['first_date']} s/d {info['last_date']}")
        except Exception as exc:  # noqa: BLE001 - setiap ticker dicatat, tidak menghentikan proses
            message = f"{type(exc).__name__}: {exc}"
            failures.append({"ticker": ticker, "error": message[:500]})
            print(f"  GAGAL {ticker}: {message[:200]}")

    if not frames:
        print("Tidak ada data yang berhasil diunduh. File lama tidak diubah.")
        return 1

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]]
    downloaded_tickers = set(combined["ticker"].unique())

    # Jangan menghapus ticker lain dari dataset lama ketika pengguna hanya
    # mengunduh sebagian ticker atau ketika sebagian unduhan gagal.
    preserved_rows = 0
    if HISTORICAL_FILE.exists():
        try:
            existing = pd.read_csv(HISTORICAL_FILE)
            existing_columns = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
            if set(existing_columns).issubset(existing.columns):
                existing = existing[existing_columns].copy()
                existing["date"] = pd.to_datetime(existing["date"], errors="coerce")
                existing["ticker"] = existing["ticker"].astype(str).str.upper().str.strip()
                existing = existing.dropna(subset=["date", "ticker"])
                preserved = existing.loc[~existing["ticker"].isin(downloaded_tickers)].copy()
                preserved_rows = int(len(preserved))
                if not preserved.empty:
                    combined = pd.concat([preserved, combined], ignore_index=True)
                    combined = combined.drop_duplicates(subset=["ticker", "date"], keep="last")
        except (OSError, pd.errors.ParserError, ValueError):
            preserved_rows = 0

    combined = combined.sort_values(["ticker", "date"]).reset_index(drop=True)

    # Tulis atomik supaya file lama tidak rusak jika proses berhenti di tengah.
    tmp_file = HISTORICAL_FILE.with_suffix(".tmp.csv")
    combined.to_csv(tmp_file, index=False)
    tmp_file.replace(HISTORICAL_FILE)

    latest_by_ticker = (
        combined.groupby("ticker", as_index=False)
        .agg(first_date=("date", "min"), last_date=("date", "max"), rows=("date", "size"))
    )
    latest_by_ticker["first_date"] = latest_by_ticker["first_date"].dt.date.astype(str)
    latest_by_ticker["last_date"] = latest_by_ticker["last_date"].dt.date.astype(str)

    meta = {
        "source": "Yahoo Finance via yfinance",
        "source_url": "https://finance.yahoo.com",
        "retrieved_at_wib": started.isoformat(timespec="seconds"),
        "requested_start": args.start,
        "requested_end_exclusive": args.end,
        "price_columns": {
            "close": "Harga penutupan biasa (belum disesuaikan)",
            "adj_close": "Harga penutupan disesuaikan untuk split dan dividen menurut Yahoo Finance",
        },
        "notes": [
            "Yahoo Finance adalah sumber pihak ketiga, bukan sumber resmi BEI.",
            "Data dapat terlambat, tidak lengkap, atau berubah tanpa pemberitahuan.",
            "Baris tanggal hari ini tidak diunduh agar harga yang belum final tidak dipakai.",
            "Untuk keputusan penting, cocokkan dengan laporan resmi perusahaan dan data BEI.",
        ],
        "benchmark_ticker": BENCHMARK_TICKER,
        "total_rows": int(len(combined)),
        "total_tickers": int(combined["ticker"].nunique()),
        "preserved_rows_from_previous_dataset": preserved_rows,
        "date_min": combined["date"].min().date().isoformat(),
        "date_max": combined["date"].max().date().isoformat(),
        "success": success,
        "failures": failures,
    }
    HISTORICAL_METADATA_FILE.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    tickers_table = pd.DataFrame(
        [
            {
                "ticker": ticker,
                "name": TICKER_META.get(ticker, {}).get("name", ticker),
                "sector": TICKER_META.get(ticker, {}).get("sector", "Lainnya"),
                "is_benchmark": bool(TICKER_META.get(ticker, {}).get("benchmark", False)),
            }
            for ticker in combined["ticker"].unique()
        ]
    )
    tickers_table.to_csv(TICKERS_FILE, index=False)

    print(f"\nSelesai: {len(success)} berhasil, {len(failures)} gagal.")
    print(f"Data gabungan: {HISTORICAL_FILE.relative_to(ROOT)} ({len(combined):,} baris)")
    print(f"Metadata     : {HISTORICAL_METADATA_FILE.relative_to(ROOT)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
