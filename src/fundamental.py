"""Perhitungan rasio fundamental dari data laporan keuangan.

Modul ini tidak berisi data perusahaan nyata. Data contoh yang dipakai di
dashboard adalah PT Bakso Nusantara (fiktif) untuk latihan.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import SAMPLE_DIR

SAMPLE_FUNDAMENTAL_FILE = SAMPLE_DIR / "contoh_laporan_keuangan_fiktif.csv"


def load_sample_financials(path: Path | str = SAMPLE_FUNDAMENTAL_FILE) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data contoh fundamental tidak ditemukan: {path}")
    frame = pd.read_csv(path)
    numeric = [
        "tahun",
        "pendapatan",
        "beban_pokok",
        "laba_operasi",
        "laba_bersih",
        "arus_kas_operasi",
        "total_aset",
        "total_liabilitas",
        "ekuitas",
        "jumlah_saham",
        "harga_saham",
        "dividen_dibagikan",
    ]
    for column in numeric:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.sort_values("tahun").reset_index(drop=True)


def calculate_fundamental_metrics(
    pendapatan: float,
    laba_bersih: float,
    ekuitas: float,
    jumlah_saham: float,
    harga_saham: float,
    dividen_dibagikan: float = 0,
    total_liabilitas: float | None = None,
) -> dict:
    """Hitung rasio dasar dengan validasi penyebut.

    Mengembalikan None untuk rasio yang tidak dapat dihitung secara bermakna.
    """
    if jumlah_saham <= 0:
        raise ValueError("Jumlah saham harus lebih dari 0")
    if harga_saham <= 0:
        raise ValueError("Harga saham harus lebih dari 0")

    eps = laba_bersih / jumlah_saham
    bvps = ekuitas / jumlah_saham
    dps = dividen_dibagikan / jumlah_saham
    return {
        "eps": eps,
        "per": harga_saham / eps if eps > 0 else None,
        "bvps": bvps,
        "pbv": harga_saham / bvps if bvps > 0 else None,
        "roe": laba_bersih / ekuitas if ekuitas > 0 else None,
        "net_margin": laba_bersih / pendapatan if pendapatan > 0 else None,
        "der": total_liabilitas / ekuitas if total_liabilitas is not None and ekuitas > 0 else None,
        "dps": dps,
        "dividend_yield": dps / harga_saham if harga_saham > 0 else None,
        "payout_ratio": dividen_dibagikan / laba_bersih if laba_bersih > 0 else None,
    }


def metrics_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Ubah setiap baris laporan menjadi satu baris rasio."""
    rows = []
    for _, row in frame.iterrows():
        metrics = calculate_fundamental_metrics(
            pendapatan=float(row["pendapatan"]),
            laba_bersih=float(row["laba_bersih"]),
            ekuitas=float(row["ekuitas"]),
            jumlah_saham=float(row["jumlah_saham"]),
            harga_saham=float(row["harga_saham"]),
            dividen_dibagikan=float(row["dividen_dibagikan"]),
            total_liabilitas=float(row["total_liabilitas"]),
        )
        rows.append(
            {
                "Tahun": int(row["tahun"]),
                "EPS (Rp)": metrics["eps"],
                "PER (×)": metrics["per"],
                "BVPS (Rp)": metrics["bvps"],
                "PBV (×)": metrics["pbv"],
                "ROE (%)": metrics["roe"] * 100 if metrics["roe"] is not None else None,
                "Margin Laba (%)": metrics["net_margin"] * 100 if metrics["net_margin"] is not None else None,
                "DER (×)": metrics["der"],
                "DPS (Rp)": metrics["dps"],
                "Dividend Yield (%)": metrics["dividend_yield"] * 100
                if metrics["dividend_yield"] is not None
                else None,
                "Payout Ratio (%)": metrics["payout_ratio"] * 100
                if metrics["payout_ratio"] is not None
                else None,
                "Arus Kas Operasi / Laba": float(row["arus_kas_operasi"]) / float(row["laba_bersih"])
                if float(row["laba_bersih"]) > 0
                else None,
            }
        )
    return pd.DataFrame(rows)
