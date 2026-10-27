"""Membuat dan menjalankan notebook pembelajaran dari data proyek.

Jalankan dari root proyek:
    python scripts/build_notebooks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"

SETUP = """from pathlib import Path
import sys

ROOT = Path.cwd()
if (ROOT / "notebooks").exists():
    pass
elif ROOT.name == "notebooks":
    ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 140)
print("Root proyek:", ROOT)"""


def notebook(cells: list[tuple[str, str]]) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    nb.cells = [
        nbf.v4.new_markdown_cell(source) if kind == "md" else nbf.v4.new_code_cell(source)
        for kind, source in cells
    ]
    return nb


NB1 = notebook(
    [
        (
            "md",
            """# 01 — Memahami Data

Notebook ini menjawab pertanyaan paling dasar sebelum menghitung apa pun:

1. Data apa yang kita punya?
2. Apakah data itu satu hari atau banyak hari?
3. Kolom apa yang bisa dipercaya, dan apa yang tidak boleh dihitung?

**Penting:** snapshot IDX di proyek ini hanya **satu hari**. Data historis Yahoo Finance
dipakai untuk tren, return, dan risiko. Jangan mencampur keduanya tanpa menjelaskan bedanya.""",
        ),
        ("code", SETUP),
        (
            "md",
            "## 1. Snapshot harian IDX\n\nFile mentah dibaca apa adanya. Kita belum mengubah file di `data/raw`.",
        ),
        (
            "code",
            """from src.data_loader import load_snapshot

snapshot_raw = load_snapshot()
print("Ukuran:", snapshot_raw.shape)
snapshot_raw.head(3)""",
        ),
        (
            "code",
            """# Nama kolom asli dari file IDX
for i, column in enumerate(snapshot_raw.columns, start=1):
    print(f"{i:2d}. {column}")""",
        ),
        (
            "md",
            "## 2. Kualitas snapshot\n\nKita cek tanggal, missing value, duplikat, saham tanpa transaksi, dan Open Price = 0.",
        ),
        (
            "code",
            """from src.data_cleaning import clean_snapshot, snapshot_quality_report

snapshot = clean_snapshot(snapshot_raw)
report = snapshot_quality_report(snapshot_raw, snapshot)

for key in [
    "rows", "columns", "unique_tickers", "dates", "missing_values",
    "duplicate_rows", "duplicate_tickers", "no_trade_rows",
    "traded_rows", "zero_open_traded_rows", "invalid_ohlc_rows", "total_value",
]:
    print(f"{key:24s}: {report[key]}")

print("\\nPeringatan:")
for warning in report["warnings"]:
    print("-", warning)""",
        ),
        (
            "code",
            """top_value = snapshot.nlargest(10, "value").sort_values("value")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.barh(top_value["ticker"], top_value["value"] / 1e9, color="#0F766E")
ax.set_xlabel("Nilai transaksi (Rp miliar)")
ax.set_title("10 saham dengan nilai transaksi terbesar — snapshot 23 Okt 2026")
plt.tight_layout()
plt.show()""",
        ),
        (
            "md",
            """**Cara membaca:** nilai transaksi besar menunjukkan aktivitas pada hari itu, bukan kualitas
perusahaan dan bukan prediksi harga besok. Snapshot satu hari tidak punya informasi tren.""",
        ),
        (
            "md",
            "## 3. Data historis\n\nData ini memiliki banyak tanggal per saham. Kolom `adj_close` dipakai untuk return jangka panjang.",
        ),
        (
            "code",
            """from src.data_loader import load_historical_prices

prices_raw = load_historical_prices()
print("Ukuran:", prices_raw.shape)
print("Jumlah ticker:", prices_raw["ticker"].nunique())
print("Rentang:", prices_raw["date"].min().date(), "s/d", prices_raw["date"].max().date())
prices_raw.head(3)""",
        ),
        (
            "code",
            """from src.data_cleaning import clean_historical, historical_quality_report

prices = clean_historical(prices_raw)
quality = historical_quality_report(prices)
print("Baris bersih:", quality["rows"])
print("Ticker:", quality["tickers"])
print("Missing:", quality["missing_values"])
print("Duplikat:", quality["duplicate_rows"])
print("OHLC tidak wajar:", quality["invalid_ohlc_rows"])
print("Volume nol:", quality["zero_volume_rows"])
quality["per_ticker"]""",
        ),
        (
            "md",
            """## 4. Kenapa satu hari tidak cukup?

- **Return** butuh minimal dua harga.
- **Volatilitas** butuh banyak return harian.
- **Maximum drawdown** butuh rangkaian harga dari puncak ke lembah.
- **Korelasi** butuh pasangan return pada tanggal yang sama.

Karena itu, grafik performa dan risiko di dashboard selalu memakai data historis, bukan snapshot.""",
        ),
        (
            "code",
            """# Contoh: berapa hari data yang tersedia per ticker?
prices.groupby("ticker").agg(
    hari=("date", "nunique"),
    awal=("date", "min"),
    akhir=("date", "max"),
).sort_values("hari", ascending=False)""",
        ),
        (
            "md",
            """## Kesimpulan

- Snapshot menjawab “apa yang terjadi pada satu tanggal”.
- Data historis menjawab “bagaimana perjalanannya selama beberapa tahun”.
- Keduanya punya keterbatasan. Sumber pihak ketiga tetap perlu diverifikasi.

Lanjut ke `02_data_cleaning.ipynb` untuk melihat proses pembersihan secara lebih rinci.""",
        ),
    ]
)


NB2 = notebook(
    [
        (
            "md",
            """# 02 — Membersihkan Data

Tujuan notebook ini: membuat data yang konsisten tanpa mengarang nilai yang hilang.

Prinsip:
- file mentah tidak diubah;
- duplikat dihapus dengan aturan yang jelas;
- harga nol/tidak wajar tidak diisi dengan tebakan;
- setiap keputusan dicatat.""",
        ),
        ("code", SETUP),
        (
            "md",
            "## 1. Snapshot: dari kolom asli ke kolom analisis",
        ),
        (
            "code",
            """from src.data_loader import load_snapshot
from src.data_cleaning import clean_snapshot, snapshot_quality_report

raw = load_snapshot()
print("Sebelum:", raw.shape)

clean = clean_snapshot(raw)
print("Sesudah:", clean.shape)
new_columns = [c for c in clean.columns if c not in raw.columns]
print("Kolom turunan:", new_columns)

clean[["ticker", "company_name", "last_trade_date", "close", "volume",
       "traded", "ohlc_valid", "market_cap", "tradeable_pct", "foreign_net"]].head()""",
        ),
        (
            "md",
            """### Catatan penting tentang `Open Price = 0`

Snapshot IDX mencatat `Open Price = 0` untuk sebagian saham yang tetap diperdagangkan.
Nilai itu diperlakukan sebagai **tidak tersedia**, bukan harga nol. Validator tidak
menghukum baris seperti itu selama harga lain konsisten.""",
        ),
        (
            "code",
            """zero_open = clean[(clean["volume"] > 0) & (clean["open"].fillna(0) <= 0)]
print("Saham diperdagangkan dengan Open Price 0:", len(zero_open))
zero_open[["ticker", "company_name", "open", "high", "low", "close", "volume"]].head(10)""",
        ),
        (
            "code",
            """report = snapshot_quality_report(raw, clean)
print("Duplikat ticker setelah dibersihkan:", report["duplicate_tickers"])
print("OHLC tidak wajar:", report["invalid_ohlc_rows"])
print("Saham tanpa transaksi:", report["no_trade_rows"])
print("Total nilai transaksi (Rp):", f"{report['total_value']:,.0f}")""",
        ),
        (
            "md",
            "## 2. Data historis: duplikat, harga nol, dan kolom validasi",
        ),
        (
            "code",
            """from src.data_loader import load_historical_prices
from src.data_cleaning import clean_historical, historical_quality_report

prices_raw = load_historical_prices()
prices = clean_historical(prices_raw)

print("Sebelum:", prices_raw.shape)
print("Sesudah:", prices.shape)
print("Harga close <= 0:", int((prices["close"] <= 0).sum()))
print("Harga adj_close <= 0:", int((prices["adj_close"] <= 0).sum()))
print("Duplikat (ticker, tanggal):", int(prices.duplicated(["ticker", "date"]).sum()))

historical_quality_report(prices)["per_ticker"]""",
        ),
        (
            "md",
            """### Close vs Adj Close

`Close` adalah harga yang tertera di pasar. `Adj Close` disesuaikan untuk dividen dan
split menurut penyedia data. Untuk membandingkan return jangka panjang, gunakan `Adj Close`.
Untuk valuasi harga saat ini, gunakan `Close`.""",
        ),
        (
            "code",
            """ticker = "BBCA.JK"
subset = prices[prices["ticker"] == ticker].set_index("date")
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot(subset.index, subset["close"], label="Close", color="#0B1F33", linewidth=1.4)
ax.plot(subset.index, subset["adj_close"], label="Adj Close", color="#0F766E", linewidth=1.4)
ax.set_title(f"{ticker}: Close vs Adj Close")
ax.set_ylabel("Rupiah per lembar")
ax.legend()
plt.tight_layout()
plt.show()""",
        ),
        (
            "md",
            """## 3. Simpan hasil pembersihan

Kita menyimpan **hasil olahan** di `data/processed`, bukan menimpa file mentah.
Ini memudahkan audit: file asli tetap ada.""",
        ),
        (
            "code",
            """from src.config import SNAPSHOT_CLEAN_FILE, FEATURES_FILE

SNAPSHOT_CLEAN_FILE.parent.mkdir(parents=True, exist_ok=True)
clean.to_csv(SNAPSHOT_CLEAN_FILE, index=False)
print("Disimpan:", SNAPSHOT_CLEAN_FILE)

# Fitur harian dibuat di notebook berikutnya; kita cek dulu apakah file sudah ada.
print("Fitur harian ada:", FEATURES_FILE.exists())""",
        ),
        (
            "md",
            """## Kesimpulan

- File mentah tetap utuh.
- Duplikat dihapus, bukan dirata-ratakan diam-diam.
- Harga tidak valid dibuang; nilai hilang tidak diisi dengan angka karangan.
- `Open Price = 0` diperlakukan sebagai data tidak tersedia.

Lanjut ke `03_feature_engineering.ipynb`.""",
        ),
    ]
)


NB3 = notebook(
    [
        (
            "md",
            """# 03 — Feature Engineering

Fitur adalah kolom turunan yang membantu analisis, misalnya return harian, moving average,
drawdown, dan volatilitas bergulir.

Aturan penting: **jangan memakai informasi masa depan**. Moving average hari ini hanya
boleh memakai harga sampai hari ini.""",
        ),
        ("code", SETUP),
        (
            "code",
            """from src.data_loader import load_historical_prices
from src.data_cleaning import clean_historical
from src.feature_engineering import build_daily_features, save_daily_features

prices = clean_historical(load_historical_prices())
features = build_daily_features(prices)
print("Ukuran fitur:", features.shape)
features.head(3)""",
        ),
        (
            "md",
            "## 1. Kolom yang dibuat",
        ),
        (
            "code",
            """for column in [
    "daily_return", "cumulative_return", "drawdown",
    "ma_20", "ma_50", "ma_200", "rolling_vol_20",
]:
    print(f"{column:20s} | non-null: {features[column].notna().sum():6d} | contoh: {features[column].dropna().head(1).tolist()}")""",
        ),
        (
            "md",
            "## 2. Moving average: hanya melihat ke belakang",
        ),
        (
            "code",
            """ticker = "BBCA.JK"
subset = features[features["ticker"] == ticker].set_index("date")
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(subset.index, subset["adj_close"], label="Adj Close", color="#94A3B8", linewidth=1.2)
ax.plot(subset.index, subset["ma_20"], label="MA 20", color="#0F766E", linewidth=1.2)
ax.plot(subset.index, subset["ma_50"], label="MA 50", color="#D97706", linewidth=1.2)
ax.plot(subset.index, subset["ma_200"], label="MA 200", color="#7C3AED", linewidth=1.2)
ax.set_title(f"{ticker}: harga dan moving average")
ax.set_ylabel("Rupiah (adjusted)")
ax.legend()
plt.tight_layout()
plt.show()""",
        ),
        (
            "md",
            """**Cara membaca:** MA 20 lebih reaktif, MA 200 lebih halus. Perpotongan garis bukan
sinyal pasti. Moving average adalah ringkasan masa lalu, bukan ramalan.""",
        ),
        (
            "md",
            "## 3. Volatilitas bergulir dan drawdown",
        ),
        (
            "code",
            """fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
axes[0].plot(subset.index, subset["rolling_vol_20"] * 100, color="#D97706")
axes[0].set_ylabel("Volatilitas 20 hari (%)")
axes[0].set_title(f"{ticker}: volatilitas bergulir dan drawdown")
axes[1].fill_between(subset.index, subset["drawdown"] * 100, 0, color="#B91C1C", alpha=0.35)
axes[1].set_ylabel("Drawdown (%)")
axes[1].set_xlabel("Tanggal")
plt.tight_layout()
plt.show()""",
        ),
        (
            "code",
            """summary = features.groupby("ticker").agg(
    observasi=("date", "nunique"),
    return_harian_rata=("daily_return", "mean"),
    vol_harian=("daily_return", "std"),
    drawdown_terdalam=("drawdown", "min"),
).sort_values("drawdown_terdalam")
summary""",
        ),
        (
            "md",
            "## 4. Simpan fitur harian",
        ),
        (
            "code",
            """saved = save_daily_features(prices)
print("Disimpan:", len(saved), "baris")
print(saved[["date", "ticker", "daily_return", "ma_20", "drawdown"]].tail(3))""",
        ),
        (
            "md",
            """## Kesimpulan

- Fitur dibuat dari data yang sudah dibersihkan.
- `rolling_vol_20` dan moving average memakai jendela waktu, bukan seluruh data.
- Drawdown dihitung dari puncak sebelumnya.
- File fitur disimpan di `data/processed/daily_features.csv`.

Lanjut ke `04_eda.ipynb` untuk analisis eksploratif.""",
        ),
    ]
)


NB4 = notebook(
    [
        (
            "md",
            """# 04 — Exploratory Data Analysis (EDA)

Notebook ini merangkum performa, risiko, korelasi, dan simulasi Rp700.000 dari data nyata
proyek. Semua angka berasal dari dataset lokal; tetap bukan rekomendasi investasi.""",
        ),
        ("code", SETUP),
        (
            "code",
            """from src.data_loader import load_historical_prices
from src.data_cleaning import clean_historical
from src.stock_analysis import performance_table, prepare_comparison, returns_matrix
from src.risk_analysis import risk_table

prices = clean_historical(load_historical_prices())
stocks = sorted(t for t in prices["ticker"].unique() if not t.startswith("^"))
print("Saham:", len(stocks), stocks)""",
        ),
        (
            "md",
            "## 1. Performa dan risiko sejak awal data",
        ),
        (
            "code",
            """start = prices["date"].min()
end = prices["date"].max()
perf = performance_table(prices, stocks + ["^JKSE"], start=start, end=end)
perf["Total Return (%)"] = perf["Total Return"] * 100
perf["CAGR (%)"] = perf["CAGR"] * 100
perf["Volatilitas (%)"] = perf["Volatilitas Tahunan"] * 100
perf["Max Drawdown (%)"] = perf["Max Drawdown"] * 100
perf[["Ticker", "Observasi", "Total Return (%)", "CAGR (%)", "Volatilitas (%)", "Max Drawdown (%)"]].sort_values("Total Return (%)", ascending=False)""",
        ),
        (
            "code",
            """risk, skipped = risk_table(prices, stocks, start=start, end=end, min_observations=60)
risk["Volatilitas (%)"] = risk["Volatilitas Tahunan"] * 100
risk["Max Drawdown (%)"] = risk["Max Drawdown"] * 100
risk["VaR 95% Harian (%)"] = risk["VaR 95% Harian"] * 100
risk[["Ticker", "Volatilitas (%)", "Max Drawdown (%)", "VaR 95% Harian (%)", "Hari Negatif"]].sort_values("Volatilitas (%)")""",
        ),
        (
            "md",
            """**Peringatan:** periode yang berbeda bisa mengubah peringkat. GOTO baru tercatat
pada 2022, jadi perbandingan harus dimulai pada tanggal yang sama.""",
        ),
        (
            "md",
            "## 2. Perbandingan harga ternormalisasi (awal = 100)",
        ),
        (
            "code",
            """selected = ["BBCA.JK", "TLKM.JK", "ANTM.JK", "GOTO.JK", "^JKSE"]
comparison = prepare_comparison(prices, selected, start=start, end=end)

fig, ax = plt.subplots(figsize=(11, 5))
for column in comparison.columns:
    ax.plot(comparison.index, comparison[column], label=column.replace(".JK", ""), linewidth=1.5)
ax.axhline(100, color="#94A3B8", linestyle=":", linewidth=1)
ax.set_title("Perjalanan harga ternormalisasi (awal = 100)")
ax.set_ylabel("Indeks")
ax.legend(ncol=5, fontsize=8)
plt.tight_layout()
plt.show()

comparison.tail(3)""",
        ),
        (
            "code",
            """print("Periode efektif:", comparison.index.min().date(), "s/d", comparison.index.max().date())
for column in comparison.columns:
    total = comparison[column].iloc[-1] / 100 - 1
    print(f"{column:10s}: {total:+.1%}")""",
        ),
        (
            "md",
            "## 3. Drawdown",
        ),
        (
            "code",
            """from src.stock_analysis import drawdown_series

fig, ax = plt.subplots(figsize=(11, 4.8))
for column in ["BBCA.JK", "TLKM.JK", "GOTO.JK", "^JKSE"]:
    series = prices[prices["ticker"] == column].set_index("date")["adj_close"].sort_index()
    dd = drawdown_series(series)
    ax.plot(dd.index, dd * 100, label=column.replace(".JK", ""), linewidth=1.3)
ax.axhline(0, color="#94A3B8", linestyle=":", linewidth=1)
ax.set_title("Drawdown dari puncak sebelumnya")
ax.set_ylabel("Drawdown (%)")
ax.legend()
plt.tight_layout()
plt.show()""",
        ),
        (
            "md",
            "## 4. Korelasi return harian",
        ),
        (
            "code",
            """import seaborn as sns
from src.stock_analysis import correlation_matrix

returns = returns_matrix(prices, stocks, start=start, end=end)
corr = correlation_matrix(returns, min_periods=30)
corr.index = [t.replace(".JK", "") for t in corr.index]
corr.columns = [t.replace(".JK", "") for t in corr.columns]

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", vmin=-1, vmax=1, ax=ax, cbar_kws={"label": "r"})
ax.set_title("Korelasi return harian")
plt.tight_layout()
plt.show()""",
        ),
        (
            "md",
            """Korelasi tinggi berarti return cenderung bergerak searah, bukan berarti penyebabnya sama.
Korelasi juga tidak stabil sepanjang waktu.""",
        ),
        (
            "md",
            "## 5. Riset saham dan simulasi modal Rp700.000",
        ),
        (
            "code",
            """from src.data_loader import load_snapshot, load_tickers
from src.data_cleaning import clean_snapshot
from src.screening import build_research_table

snapshot = clean_snapshot(load_snapshot())
tickers = load_tickers()
research = build_research_table(prices, tickers, snapshot=snapshot, start=start, end=end, min_observations=60)
research["Return (%)"] = research["Return Periode"] * 100
research["Volatilitas (%)"] = research["Volatilitas Tahunan"] * 100
research["Max Drawdown (%)"] = research["Max Drawdown"] * 100
research[["Ticker", "Sektor", "Harga Terakhir", "Return (%)", "Volatilitas (%)", "Max Drawdown (%)", "Nilai Transaksi 20H"]].sort_values("Return (%)", ascending=False)""",
        ),
        (
            "code",
            """from src.simulation import simulate_trade

result = simulate_trade(
    modal=700_000,
    allocation=280_000,
    price=2_500,
    lots=1,
    change_pct=5,
    buy_fee_pct=0.15,
    sell_fee_pct=0.15,
    tax_pct=0.10,
)
print(f"Total beli      : Rp{result.total_buy:,.0f}")
print(f"Hasil jual bersih: Rp{result.net_proceeds:,.0f}")
print(f"Laba/rugi bersih : Rp{result.net_profit:,.0f}")
print(f"Return investasi : {result.return_on_investment_pct:.2f}%")
print(f"Return modal     : {result.return_on_total_capital_pct:.2f}%")""",
        ),
        (
            "md",
            """## Kesimpulan

- Return tinggi di masa lalu tidak menjamin masa depan.
- Volatilitas dan drawdown menunjukkan betapa sulitnya perjalanan, bukan hanya hasil akhir.
- Korelasi membantu memahami kemiripan pergerakan, bukan menghilangkan risiko.
- Simulasi memperlihatkan bahwa biaya transaksi dan pajak mengurangi hasil.
- Semua ini alat belajar. Keputusan nyata membutuhkan riset, disiplin, dan dana darurat.""",
        ),
    ]
)


def main() -> None:
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    targets = {
        "01_data_understanding.ipynb": NB1,
        "02_data_cleaning.ipynb": NB2,
        "03_feature_engineering.ipynb": NB3,
        "04_eda.ipynb": NB4,
    }
    for filename, nb in targets.items():
        path = NOTEBOOK_DIR / filename
        nbf.write(nb, path)
        print("Menjalankan", filename)
        client = NotebookClient(
            nb,
            timeout=180,
            kernel_name="python3",
            resources={"metadata": {"path": str(NOTEBOOK_DIR)}},
        )
        client.execute()
        nbf.write(nb, path)
        print("Selesai:", path)


if __name__ == "__main__":
    sys.exit(main())
