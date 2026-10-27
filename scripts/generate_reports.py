"""Menghasilkan laporan dan grafik dari data proyek yang sebenarnya.

Jalankan dari root proyek:
    python scripts/generate_reports.py
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CHART_DIR, REPORT_DIR, ticker_label  # noqa: E402
from src.data_cleaning import (  # noqa: E402
    clean_historical,
    clean_snapshot,
    historical_quality_report,
    snapshot_quality_report,
)
from src.data_loader import load_historical_prices, load_metadata, load_snapshot, load_tickers  # noqa: E402
from src.risk_analysis import risk_table  # noqa: E402
from src.screening import build_research_table  # noqa: E402
from src.simulation import simulate_trade  # noqa: E402
from src.stock_analysis import (  # noqa: E402
    correlation_matrix,
    drawdown_series,
    get_price_series,
    performance_table,
    prepare_comparison,
    returns_matrix,
)

WIB = ZoneInfo("Asia/Jakarta")
TEAL = "#0F766E"
AMBER = "#D97706"
RED = "#B91C1C"
NAVY = "#0B1F33"
MUTED = "#64748B"
COLORS = ["#0F766E", "#D97706", "#2563EB", "#7C3AED", "#DB2777", "#0891B2"]
MONTHS_ID = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun", 7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des"}


def rupiah(value: float, compact: bool = False) -> str:
    if value is None or pd.isna(value):
        return "—"
    if compact:
        if abs(value) >= 1_000_000_000_000:
            return f"Rp{value / 1_000_000_000_000:,.2f} T".replace(",", ".")
        if abs(value) >= 1_000_000_000:
            return f"Rp{value / 1_000_000_000:,.1f} M".replace(",", ".")
        if abs(value) >= 1_000_000:
            return f"Rp{value / 1_000_000:,.1f} juta".replace(",", ".")
    return f"Rp{value:,.0f}".replace(",", ".")


def id_date(value) -> str:
    value = pd.Timestamp(value)
    return f"{value.day:02d} {MONTHS_ID[value.month]} {value.year}"


def pct(value: float, signed: bool = False, decimals: int = 1) -> str:
    if value is None or pd.isna(value):
        return "—"
    text = f"{value * 100:+.{decimals}f}%" if signed else f"{value * 100:.{decimals}f}%"
    return text.replace(".", ",")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return "\n".join(lines)


def setup_plot_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": "#CBD5E1",
            "axes.labelcolor": "#334155",
            "axes.titlecolor": NAVY,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": "#E2E8F0",
            "font.family": "DejaVu Sans",
            "legend.frameon": False,
        }
    )


def save(fig: plt.Figure, name: str) -> Path:
    path = CHART_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("Grafik:", path)
    return path


def normalized_chart(prices: pd.DataFrame, start, end) -> None:
    tickers = ["BBCA.JK", "TLKM.JK", "ANTM.JK", "GOTO.JK", "^JKSE"]
    comparison = prepare_comparison(prices, tickers, start=start, end=end)
    if comparison.empty:
        return
    fig, ax = plt.subplots(figsize=(11, 5.2))
    for index, column in enumerate(comparison.columns):
        ax.plot(
            comparison.index,
            comparison[column],
            label="IHSG" if column == "^JKSE" else ticker_label(column),
            color=COLORS[index % len(COLORS)],
            linewidth=1.8 if column != "^JKSE" else 2.4,
        )
    ax.axhline(100, color="#94A3B8", linestyle=":", linewidth=1)
    ax.set_title("Perjalanan harga ternormalisasi (awal = 100)")
    ax.set_ylabel("Indeks (awal = 100)")
    ax.set_xlabel("Tanggal")
    ax.legend(ncol=5, fontsize=8)
    ax.grid(axis="y", alpha=0.55)
    save(fig, "normalized_performance.png")


def drawdown_chart(prices: pd.DataFrame, start, end) -> None:
    fig, ax = plt.subplots(figsize=(11, 4.8))
    for index, ticker in enumerate(["BBCA.JK", "TLKM.JK", "ANTM.JK", "GOTO.JK", "^JKSE"]):
        series = get_price_series(prices, ticker, start=start, end=end)
        if series.empty:
            continue
        drawdown = drawdown_series(series)
        ax.plot(drawdown.index, drawdown * 100, label=ticker_label(ticker), color=COLORS[index], linewidth=1.5)
    ax.axhline(0, color="#94A3B8", linestyle=":", linewidth=1)
    ax.set_title("Drawdown dari puncak sebelumnya")
    ax.set_ylabel("Drawdown (%)")
    ax.set_xlabel("Tanggal")
    ax.legend(ncol=5, fontsize=8)
    ax.grid(axis="y", alpha=0.55)
    save(fig, "drawdown.png")


def risk_scatter(perf: pd.DataFrame) -> None:
    data = perf.loc[perf["Ticker"] != "^JKSE"].copy()
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.scatter(
        data["Volatilitas Tahunan"] * 100,
        data["Total Return"] * 100,
        s=70,
        color=TEAL,
        alpha=0.8,
        edgecolor="white",
        linewidth=1,
    )
    for _, row in data.iterrows():
        ax.annotate(
            ticker_label(row["Ticker"]),
            (row["Volatilitas Tahunan"] * 100, row["Total Return"] * 100),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=8,
            color=NAVY,
        )
    benchmark = perf.loc[perf["Ticker"] == "^JKSE"]
    if not benchmark.empty:
        row = benchmark.iloc[0]
        ax.scatter(
            row["Volatilitas Tahunan"] * 100,
            row["Total Return"] * 100,
            s=90,
            marker="D",
            color=AMBER,
            label="IHSG",
            zorder=3,
        )
        ax.legend()
    ax.axhline(0, color="#94A3B8", linestyle=":", linewidth=1)
    ax.set_xlabel("Volatilitas tahunan (%)")
    ax.set_ylabel("Total return periode (%)")
    ax.set_title("Return vs volatilitas — bukan rekomendasi")
    ax.grid(alpha=0.5)
    save(fig, "risk_scatter.png")


def correlation_chart(corr: pd.DataFrame) -> None:
    labels = [ticker_label(t) for t in corr.index]
    fig, ax = plt.subplots(figsize=(9.2, 7.4))
    image = ax.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr.values[i, j]
            if pd.notna(value):
                ax.text(j, i, f"{value:.2f}", ha="center", va="center", fontsize=7.5, color=NAVY)
    ax.set_title("Korelasi return harian")
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04, label="r")
    save(fig, "correlation_heatmap.png")


def snapshot_chart(snapshot: pd.DataFrame) -> None:
    top = snapshot.nlargest(10, "value").sort_values("value")
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    ax.barh(top["ticker"], top["value"] / 1e9, color=TEAL)
    ax.set_xlabel("Nilai transaksi (Rp miliar)")
    ax.set_title("10 saham dengan nilai transaksi terbesar — snapshot 23 Okt 2026")
    ax.grid(axis="x", alpha=0.45)
    save(fig, "snapshot_top_value.png")


def simulation_chart(result) -> None:
    labels = ["Nilai beli", "Perubahan harga", "Komisi beli", "Komisi jual", "Pajak jual", "Laba bersih"]
    values = [
        -result.buy_gross,
        result.gross_profit,
        -result.buy_fee,
        -result.sell_fee,
        -result.tax,
        result.net_profit,
    ]
    colors = [NAVY if value < 0 else TEAL for value in values]
    fig, ax = plt.subplots(figsize=(9.4, 4.8))
    ax.bar(labels, values, color=colors)
    ax.axhline(0, color="#94A3B8", linewidth=1)
    ax.set_ylabel("Rupiah")
    ax.set_title("Simulasi 1 lot: dari nilai beli ke laba/rugi bersih")
    for index, value in enumerate(values):
        ax.text(index, value, f"{rupiah(value, compact=True)}", ha="center", va="bottom" if value >= 0 else "top", fontsize=8)
    plt.xticks(rotation=15)
    ax.grid(axis="y", alpha=0.5)
    save(fig, "simulation_waterfall.png")


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    setup_plot_style()

    snapshot_raw = load_snapshot()
    snapshot = clean_snapshot(snapshot_raw)
    snapshot_report = snapshot_quality_report(snapshot_raw, snapshot)

    prices = clean_historical(load_historical_prices())
    historical_quality = historical_quality_report(prices)
    metadata = load_metadata()
    tickers = load_tickers()

    stocks = sorted(t for t in prices["ticker"].unique() if not t.startswith("^"))
    start = prices["date"].min()
    end = prices["date"].max()

    perf = performance_table(prices, stocks + ["^JKSE"], start=start, end=end)
    risk, skipped = risk_table(prices, stocks, start=start, end=end, min_observations=60)
    research = build_research_table(prices, tickers, snapshot=snapshot, start=start, end=end, min_observations=60)
    returns = returns_matrix(prices, stocks, start=start, end=end)
    corr = correlation_matrix(returns, min_periods=30)
    simulation = simulate_trade()

    # CSV keluaran
    snapshot_report_frame = pd.DataFrame(
        [
            {
                "baris": snapshot_report["rows"],
                "kolom": snapshot_report["columns"],
                "ticker_unik": snapshot_report["unique_tickers"],
                "tanggal": ", ".join(snapshot_report["dates"]),
                "missing": snapshot_report["missing_values"],
                "duplikat_baris": snapshot_report["duplicate_rows"],
                "tanpa_transaksi": snapshot_report["no_trade_rows"],
                "open_nol_diperdagangkan": snapshot_report["zero_open_traded_rows"],
                "ohlc_tidak_wajar": snapshot_report["invalid_ohlc_rows"],
                "total_nilai": snapshot_report["total_value"],
            }
        ]
    )
    snapshot_report_frame.to_csv(REPORT_DIR / "quality_snapshot.csv", index=False)
    historical_quality["per_ticker"].to_csv(REPORT_DIR / "quality_historical.csv", index=False)
    perf.to_csv(REPORT_DIR / "performance_metrics.csv", index=False)
    risk.to_csv(REPORT_DIR / "risk_metrics.csv", index=False)
    corr.to_csv(REPORT_DIR / "correlation_matrix.csv")
    research.to_csv(REPORT_DIR / "research_table.csv", index=False)

    # Grafik
    normalized_chart(prices, start, end)
    drawdown_chart(prices, start, end)
    risk_scatter(perf)
    correlation_chart(corr)
    snapshot_chart(snapshot)
    simulation_chart(simulation)

    # Tabel Markdown
    perf_rows = []
    for _, row in perf.sort_values("Total Return", ascending=False).iterrows():
        perf_rows.append(
            [
                ticker_label(row["Ticker"]),
                f"{int(row['Observasi']):,}".replace(",", "."),
                pct(row["Total Return"], signed=True),
                pct(row["CAGR"], signed=True),
                pct(row["Volatilitas Tahunan"]),
                pct(row["Max Drawdown"], signed=True),
            ]
        )
    perf_table_md = markdown_table(
        ["Ticker", "Observasi", "Total return", "CAGR", "Volatilitas", "Max drawdown"],
        perf_rows,
    )

    risk_rows = []
    for _, row in risk.sort_values("Volatilitas Tahunan").iterrows():
        risk_rows.append(
            [
                ticker_label(row["Ticker"]),
                pct(row["Volatilitas Tahunan"]),
                pct(row["Downside Deviation"]),
                pct(row["Max Drawdown"], signed=True),
                pct(row["VaR 95% Harian"]),
                pct(row["Hari Negatif"]),
            ]
        )
    risk_table_md = markdown_table(
        ["Ticker", "Volatilitas", "Downside dev.", "Max drawdown", "VaR 95% harian", "Hari negatif"],
        risk_rows,
    )

    research_rows = []
    for _, row in research.sort_values("Return Periode", ascending=False).iterrows():
        research_rows.append(
            [
                row["Ticker"],
                row["Sektor"],
                rupiah(row["Harga Terakhir"]),
                pct(row["Return Periode"], signed=True),
                pct(row["Volatilitas Tahunan"]),
                pct(row["Max Drawdown"], signed=True),
                rupiah(row["Nilai Transaksi 20H"], compact=True),
            ]
        )
    research_md = markdown_table(
        ["Ticker", "Sektor", "Harga terakhir", "Return periode", "Volatilitas", "Max DD", "Likuiditas 20H"],
        research_rows,
    )

    # Pasangan korelasi ekstrem
    pairs = []
    columns = list(corr.columns)
    for i, left in enumerate(columns):
        for right in columns[i + 1 :]:
            value = corr.loc[left, right]
            if pd.notna(value):
                pairs.append((ticker_label(left), ticker_label(right), float(value)))
    strongest = max(pairs, key=lambda item: item[2]) if pairs else None
    weakest = min(pairs, key=lambda item: item[2]) if pairs else None
    strongest_text = ""
    weakest_text = ""
    if strongest:
        arah = "searah" if strongest[2] >= 0 else "berlawanan"
        strongest_text = f"Korelasi tertinggi: **{strongest[0]} vs {strongest[1]} = {strongest[2]:.2f}** ({arah})."
    if weakest:
        arah = "searah" if weakest[2] >= 0 else "berlawanan"
        weakest_text = f"Korelasi terendah: **{weakest[0]} vs {weakest[1]} = {weakest[2]:.2f}** ({arah})."

    best = perf.loc[perf["Ticker"] != "^JKSE"].sort_values("Total Return", ascending=False).iloc[0]
    worst = perf.loc[perf["Ticker"] != "^JKSE"].sort_values("Total Return").iloc[0]
    benchmark = perf.loc[perf["Ticker"] == "^JKSE"].iloc[0]
    riskiest = risk.sort_values("Max Drawdown").iloc[0]

    now = datetime.now(WIB)
    generated = f"{now.day:02d} {MONTHS_ID[now.month]} {now.year}, {now.strftime('%H:%M')} WIB"
    source_note = (
        f"Yahoo Finance melalui `yfinance`, diambil {metadata.get('retrieved_at_wib', '—')}"
        if metadata
        else "metadata pengambilan tidak tersedia"
    )

    report = f"""# Laporan Analisis Saham Indonesia

Dibuat: **{generated}**  
Proyek: **SahamLab — belajar saham, analisis data, dan simulasi lokal**

> Laporan ini adalah alat belajar dan eksplorasi data, **bukan rekomendasi beli/jual**.
> Angka historis tidak menjamin hasil masa depan. Harga bisa turun dan modal bisa berkurang.

## 1. Ringkasan data

| Komponen | Nilai |
| --- | --- |
| Snapshot IDX | {snapshot_report['rows']} saham, {snapshot_report['date_count']} tanggal ({', '.join(snapshot_report['dates'])}) |
| Data historis | {historical_quality['rows']:,} baris, {historical_quality['tickers']} ticker |
| Rentang historis | {id_date(historical_quality['date_min'])} – {id_date(historical_quality['date_max'])} |
| Sumber historis | {source_note} |
| Saham dalam dataset | {len(stocks)} saham + IHSG |
| Harga untuk return | `Adj Close` |
| Harga untuk valuasi | `Close` |

Snapshot dan data historis **tidak boleh dicampur**. Snapshot hanya potret satu hari.
Analisis tren, return, risiko, dan korelasi memakai data historis.

## 2. Kualitas data

### Snapshot

- Missing value: **{snapshot_report['missing_values']}**
- Duplikat baris: **{snapshot_report['duplicate_rows']}**
- Duplikat ticker: **{snapshot_report['duplicate_tickers']}**
- Saham tanpa transaksi: **{snapshot_report['no_trade_rows']}**
- Saham diperdagangkan dengan `Open Price = 0`: **{snapshot_report['zero_open_traded_rows']}** (diperlakukan sebagai tidak tersedia)
- OHLC tidak wajar: **{snapshot_report['invalid_ohlc_rows']}**
- Total nilai transaksi snapshot: **{rupiah(snapshot_report['total_value'], compact=True)}**

### Historis

- Missing value: **{historical_quality['missing_values']}**
- Duplikat (ticker + tanggal): **{historical_quality['duplicate_rows']}**
- OHLC tidak wajar: **{historical_quality['invalid_ohlc_rows']}**
- Baris volume nol: **{historical_quality['zero_volume_rows']}**
- GOTO memiliki riwayat lebih pendek karena baru tercatat pada 2022.

## 3. Performa historis

Periode: **{id_date(start)} – {id_date(end)}**.
Return dan risiko dihitung dari `Adj Close`, bukan dari snapshot satu hari.

{perf_table_md}

**Catatan penting:** GOTO tidak memiliki data sebelum April 2022. Angka GOTO di atas dihitung
dari tanggal yang tersedia, sehingga tidak sepenuhnya sebanding dengan saham yang datanya
dimulai 2019. Perbandingan visual memakai tanggal awal yang sama.

## 4. Risiko historis

{risk_table_md}

VaR 95% historis adalah ambang kerugian harian pada 5% hari terburuk dalam periode ini.
VaR **bukan** batas kerugian maksimum. Volatilitas dan drawdown juga berubah bila periode diubah.

## 5. Korelasi return harian

{strongest_text}
{weakest_text}

Korelasi dihitung dari return harian pada tanggal yang tersedia untuk semua saham terpilih.
Korelasi bukan sebab-akibat dan tidak stabil sepanjang waktu.

![Heatmap korelasi](../charts/correlation_heatmap.png)

## 6. Riset 12 saham

{research_md}

Kapitalisasi adalah perkiraan dari harga terakhir dataset × jumlah saham tercatat di snapshot.
Angka ini bukan kapitalisasi real-time resmi. Kolom `Tradeable/Listed` **bukan free float sebenarnya**.

## 7. Simulasi modal Rp700.000

Contoh: 1 lot (100 lembar) pada harga simulasi Rp2.500, alokasi Rp280.000, komisi beli/jual 0,15%,
pajak jual 0,1%, lalu harga naik 5%.

| Komponen | Nilai |
| --- | --- |
| Nilai saham | {rupiah(simulation.buy_gross)} |
| Komisi beli | {rupiah(simulation.buy_fee)} |
| Total uang keluar | {rupiah(simulation.total_buy)} |
| Hasil jual bersih | {rupiah(simulation.net_proceeds)} |
| Laba/rugi bersih | **{rupiah(simulation.net_profit)}** |
| Return investasi | {pct(simulation.return_on_investment_pct / 100, signed=True)} |
| Return terhadap modal | {pct(simulation.return_on_total_capital_pct / 100, signed=True)} |

Bahkan pada perubahan harga 0%, hasilnya sudah negatif karena biaya transaksi. Ini bukan
alasan untuk tidak pernah bertransaksi, tetapi alasan untuk menghitung biaya sebelum membeli.

## 8. Temuan utama (deskriptif, bukan rekomendasi)

- Return total tertinggi pada periode ini: **{ticker_label(best['Ticker'])} ({pct(best['Total Return'], signed=True)})**.
- Return total terendah pada periode ini: **{ticker_label(worst['Ticker'])} ({pct(worst['Total Return'], signed=True)})**.
- IHSG sebagai pembanding: **{pct(benchmark['Total Return'], signed=True)}** pada periode yang sama.
- Drawdown terdalam pada tabel risiko: **{ticker_label(riskiest['Ticker'])} ({pct(riskiest['Max Drawdown'], signed=True)})**.
- Angka-angka ini hanya menggambarkan masa lalu, bukan prediksi.

## 9. Grafik

### Harga ternormalisasi
![Performa ternormalisasi](../charts/normalized_performance.png)

### Drawdown
![Drawdown](../charts/drawdown.png)

### Return vs volatilitas
![Return vs volatilitas](../charts/risk_scatter.png)

### Snapshot: nilai transaksi terbesar
![Snapshot](../charts/snapshot_top_value.png)

### Simulasi biaya
![Simulasi](../charts/simulation_waterfall.png)

## 10. Keterbatasan

1. Dataset hanya **12 saham + IHSG**, bukan seluruh bursa. Tidak bisa mewakili pasar Indonesia.
2. Sumber historis adalah **Yahoo Finance**, pihak ketiga yang bisa terlambat, tidak lengkap,
   atau berubah tanpa pemberitahuan.
3. Tidak ada data fundamental perusahaan nyata yang terverifikasi di proyek ini.
4. Tidak ada data intraday, bid/ask real-time, atau integrasi broker.
5. Hasil mengandung **survivorship bias** bila dipakai untuk menyimpulkan strategi jangka panjang,
   karena daftar saham dipilih saat proyek dibuat.
6. Return dan risiko sangat bergantung pada periode, tanggal mulai, dan kualitas data.
7. Simulasi belum memasukkan slippage, likuiditas, perubahan fraksi harga, dividen, dan pajak lain.
8. Korelasi, CAGR, dan drawdown bukan jaminan kinerja masa depan.

## 11. File keluaran

- `outputs/reports/performance_metrics.csv`
- `outputs/reports/risk_metrics.csv`
- `outputs/reports/correlation_matrix.csv`
- `outputs/reports/research_table.csv`
- `outputs/reports/quality_snapshot.csv`
- `outputs/reports/quality_historical.csv`
- `outputs/charts/*.png`
- `notebooks/01_data_understanding.ipynb` sampai `notebooks/04_eda.ipynb`

---

**Pengingat:** proyek ini tidak terhubung ke broker, tidak mengirim order, dan tidak memberi
rekomendasi saham. Jangan memakai utang atau uang kebutuhan untuk berinvestasi.
"""

    report_path = REPORT_DIR / "laporan_analisis.md"
    report_path.write_text(report, encoding="utf-8")
    print("Laporan:", report_path)
    if skipped:
        print("Saham yang dilewati pada tabel risiko:", skipped)


if __name__ == "__main__":
    sys.exit(main())
