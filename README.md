# SahamLab — Belajar Saham Indonesia

Proyek belajar **data analyst + saham Indonesia** untuk pemula. Isinya: data historis nyata,
analisis Python yang bisa dipakai ulang, dashboard Streamlit lokal, 9 modul pembelajaran,
simulasi modal **Rp700.000**, paper trading, pengujian, notebook, dan laporan.

> **Bukan rekomendasi investasi.** Proyek ini tidak terhubung ke broker, tidak mengirim order,
> tidak memakai API key, dan tidak menjanjikan keuntungan. Harga bisa turun; modal bisa berkurang.
> Jangan memakai utang, margin, atau uang kebutuhan untuk berinvestasi.

---

## 1. Apa yang bisa dilakukan?

| Bagian | Fungsi |
| --- | --- |
| Beranda & Belajar | 9 modul × 2 pelajaran, kuis 3 soal, progres tersimpan lokal |
| Data Overview | Audit snapshot IDX satu hari + kualitas data historis |
| Performa Saham | Harga ternormalisasi, return, CAGR, moving average, IHSG |
| Analisis Risiko | Volatilitas, drawdown, VaR historis, distribusi return |
| Korelasi Saham | Heatmap korelasi return harian |
| Fundamental | Latihan membaca laporan keuangan dengan perusahaan **fiktif** |
| Simulasi Rp700.000 | Lot, fraksi harga, komisi, pajak, laba/rugi bersih |
| Paper Trading | Jurnal transaksi virtual + perhitungan portofolio |
| Riset Saham | Tabel metrik historis dengan filter transparan, tanpa skor “pasti bagus” |

Semua transaksi di aplikasi **virtual**. Tidak ada koneksi ke sekuritas/broker.

---

## 2. Data yang dipakai

### Snapshot IDX

- File asli: `Ringkasan Saham-20261023.csv` (di root proyek, **tidak diubah**).
- Salinan mentah: `data/raw/idx_daily_summary_20261023.csv`.
- Isi: **963 saham**, **28 kolom**, **1 tanggal** (23 Oktober 2026).
- Ini **potret satu hari**, bukan data historis. Tidak dipakai untuk tren, return, atau risiko.

### Data historis

- Sumber: Yahoo Finance melalui `yfinance`, `auto_adjust=False`.
- File: `data/processed/historical_prices.csv`.
- Isi: **12 saham + IHSG**, **23.856 baris**, **1 Januari 2019 – 26 Oktober 2026**.
- `Adj Close` dipakai untuk return/risiko jangka panjang; `Close` dipakai untuk valuasi harga.
- Sumber pihak ketiga, bukan pengganti laporan resmi BEI/perusahaan.

Daftar saham: BBCA, BBRI, BMRI, TLKM, ASII, ANTM, ADRO, AKRA, ICBP, UNVR, SMGR, GOTO,
ditambah IHSG (`^JKSE`). Ini **bukan daftar rekomendasi**.

### Data fundamental

Data fundamental perusahaan nyata **belum tersedia** dan tidak dibuat-buat. Halaman Fundamental
memakai **PT Bakso Nusantara (fiktif)** di `data/sample/contoh_laporan_keuangan_fiktif.csv`.

---

## 3. Cara menjalankan (Windows)

Prasyarat: Python 3.13 (proyek diuji dengan Python 3.13.15) dan koneksi internet untuk mengambil data.

Buka **PowerShell** di folder proyek:

```powershell
cd "C:\Users\53\Documents\data sains\project saham"

# Opsional tetapi disarankan: virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Ambil/segarkan data historis (butuh internet)
python scripts\fetch_data.py

# Jalankan dashboard
python -m streamlit run app.py
```

Browser biasanya terbuka otomatis di `http://localhost:8501`. Jika belum, buka alamat tersebut manual.
Hentikan server dengan `Ctrl+C`.

Jika PowerShell menolak aktivasi venv, jalankan sekali:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Alternatif tanpa venv: langsung `python -m pip install -r requirements.txt`, lalu
`python -m streamlit run app.py`.

---

## 4. Alur belajar yang disarankan

1. Buka **Beranda & Belajar**.
2. Baca Modul 1 Pelajaran 1: “Apa itu saham?”.
3. Jawab 3 pertanyaan. Minimal **2 benar** untuk membuka pelajaran berikutnya.
4. Lanjut satu pelajaran per sesi; jangan mengejar semua materi sekaligus.
5. Setelah beberapa modul, buka halaman analisis dan simulator.
6. Catat keputusan virtual di Paper Trading **beserta alasannya**.
7. Evaluasi proses, bukan hanya hasil.

Versi bacaan lengkap dari 9 modul tersedia di `notebooks pembelajaran/`. Folder itu
berisi notebook yang bisa dibuka langsung di VSCode, lengkap dengan kuis dan kunci
jawaban. Dashboard tetap dipakai untuk progres otomatis, simulasi, dan paper trading.

Progres belajar disimpan di `data/user/learning_progress.json`; paper trading di
`data/user/paper_trades.csv`. Keduanya file lokal dan tidak dikirim ke mana pun.

### 9 modul

1. Memahami Saham dari Nol
2. Mengelola Modal Rp700.000
3. Memahami Risiko Investasi
4. Mengenal Aplikasi dan Sumber Data
5. Membaca Laporan Keuangan
6. Analisis Saham dengan Python
7. Simulasi dan Paper Trading
8. Persiapan Pembelian Saham Pertama
9. Membangun Kebiasaan Investor

---

## 5. Struktur proyek

```text
project saham/
├── app.py                       # navigasi utama Streamlit
├── src/
│   ├── config.py                # path, ticker, modal, aturan lot
│   ├── data_loader.py           # membaca dataset
│   ├── data_cleaning.py         # validasi & pembersihan
│   ├── feature_engineering.py   # return, MA, drawdown, fitur harian
│   ├── stock_analysis.py        # performa, CAGR, volatilitas, korelasi
│   ├── risk_analysis.py         # VaR, downside deviation, tabel risiko
│   ├── simulation.py            # simulasi lot/biaya/pajak
│   ├── portfolio.py             # paper trading & valuasi portofolio
│   ├── screening.py             # tabel riset 12 saham
│   ├── learning_content.py      # 9 modul, 18 pelajaran, 54 kuis
│   ├── progress.py              # progres belajar lokal
│   ├── fundamental.py           # rasio dari laporan fiktif
│   ├── cached_data.py           # cache Streamlit
│   ├── ui.py                    # CSS, kartu, format angka, grafik
│   └── pages/                   # halaman dashboard
├── data/
│   ├── raw/                     # file mentah (jangan diubah)
│   ├── processed/               # data bersih + fitur
│   ├── sample/                  # contoh fundamental fiktif
│   └── user/                    # progres & paper trading (lokal)
├── scripts/
│   ├── fetch_data.py            # unduh data Yahoo Finance
│   ├── build_notebooks.py       # buat + jalankan notebook lab
│   ├── build_learning_notebooks.py  # buat materi belajar .ipynb
│   └── generate_reports.py      # buat laporan + grafik
├── notebooks/                   # 01–04, sudah dieksekusi
├── notebooks pembelajaran/      # materi baca 9 modul + kuis (VSCode)
├── outputs/
│   ├── charts/                  # grafik PNG
│   └── reports/                 # laporan & CSV metrik
├── tests/                       # pytest
├── requirements.txt
└── README.md
```

---

## 6. Pengujian

```powershell
python -m pytest -q
```

Yang diuji antara lain: pembersihan snapshot/historis, aturan fraksi harga & lot, perhitungan
biaya/pajak, return/CAGR/drawdown/korelasi, validasi paper trading (kas kurang, jual melebihi
kepemilikan, tanggal masa depan), progres kuis, penggabungan snapshot, validitas notebook
materi belajar, dan smoke test seluruh halaman Streamlit.

Pengujian memakai data sintetis untuk logika inti dan dataset asli untuk integrasi ringan.
Tidak ada hasil uji yang dikarang.

---

## 7. Notebook dan laporan

### Materi belajar untuk VSCode

Folder `notebooks pembelajaran/` berisi versi bacaan dari seluruh kurikulum:

- `00_Panduan_Belajar.ipynb` — cara membuka di VSCode dan peta 9 modul.
- `Modul_01_...ipynb` s/d `Modul_09_...ipynb` — dua pelajaran per modul, kuis,
  kunci jawaban, dan checklist.
- `README.md` — ringkasan isi dan alur belajar.

Materi ini fokus membaca dan menguji pemahaman; notebook tidak perlu dijalankan.
Untuk praktik Python dengan data proyek, gunakan folder `notebooks/`.

Membuat ulang materi belajar:

```powershell
python scripts\build_learning_notebooks.py
```

### Notebook lab

Notebook di folder `notebooks/` sudah berisi output eksekusi nyata:

- `notebooks/01_data_understanding.ipynb` — mengenali snapshot vs historis.
- `notebooks/02_data_cleaning.ipynb` — pembersihan dan validasi.
- `notebooks/03_feature_engineering.ipynb` — return, MA, drawdown, volatilitas.
- `notebooks/04_eda.ipynb` — performa, risiko, korelasi, riset, simulasi.

Membuat ulang notebook lab:

```powershell
python scripts\build_notebooks.py
```

Membuat ulang laporan dan grafik:

```powershell
python scripts\generate_reports.py
```

Hasil utama:

- `outputs/reports/laporan_analisis.md`
- `outputs/reports/performance_metrics.csv`
- `outputs/reports/risk_metrics.csv`
- `outputs/reports/correlation_matrix.csv`
- `outputs/reports/research_table.csv`
- `outputs/reports/quality_snapshot.csv`
- `outputs/reports/quality_historical.csv`
- `outputs/charts/*.png`

Laporan memakai angka aktual dari dataset. Angka bisa berubah jika data diambil ulang.

![Perbandingan ternormalisasi](outputs/charts/normalized_performance.png)

---

## 8. Aturan transaksi yang dimodelkan

- **1 lot = 100 lembar** (aturan BEI; periksa kembali sumber resmi jika berubah).
- Fraksi harga: `<Rp200 = Rp1`, `<Rp500 = Rp2`, `<Rp2.000 = Rp5`, `<Rp5.000 = Rp10`,
  `≥Rp5.000 = Rp25`.
- Komisi beli/jual default **0,15%** dan bisa diubah (tarif berbeda tiap sekuritas).
- Pajak penjualan default **0,1%** untuk saham individu.
- Laba bersih = hasil jual bersih − total biaya beli.
- Simulasi **belum** memasukkan slippage, spread, likuiditas, dividen, stock split, perubahan
  fraksi, auto-reject, dan biaya lain.

Contoh default: 1 lot @ Rp2.500, alokasi Rp280.000, naik 5% → total beli Rp250.375,
hasil jual bersih Rp261.844, laba bersih **Rp11.469**, return investasi **4,58%**,
return terhadap modal **1,64%**. Pada perubahan harga 0%, hasilnya sudah negatif karena biaya.

Sumber acuan yang perlu diverifikasi ulang:

- [IDX — satuan lot](https://rdis.idx.co.id/id/events/mengenai-satuan-lot-apa-itu-lot)
- [IDX — perpajakan](https://www.idx.co.id/id/investhub/perpajakan/)
- [IDX — fraksi harga](https://www.idx.co.id/en/news/press-release/518)

---

## 9. Keterbatasan penting

1. Dataset hanya **12 saham + IHSG**, bukan seluruh bursa; tidak mewakili pasar Indonesia.
2. Yahoo Finance adalah sumber pihak ketiga: bisa terlambat, tidak lengkap, atau berubah.
3. Snapshot IDX hanya satu hari; jangan menghitung tren/return dari snapshot.
4. Tidak ada data fundamental nyata yang terverifikasi; halaman Fundamental memakai perusahaan fiktif.
5. Tidak ada integrasi broker, data intraday, bid/ask real-time, atau order nyata.
6. Dataset bisa mengandung **survivorship bias** dan **look-ahead bias** jika dipakai untuk
   menyimpulkan strategi tanpa desain backtest yang benar.
7. Return, volatilitas, drawdown, dan korelasi sangat bergantung pada periode dan kualitas data.
8. `Tradeble Shares` di snapshot hampir selalu sama dengan `Listed Shares`; rasio yang ditampilkan
   **bukan free float sebenarnya**.
9. Hasil simulasi/paper trading bukan bukti kemampuan berinvestasi nyata.
10. Proyek ini bukan nasihat keuangan, pajak, atau hukum.

---

## 10. Troubleshooting

**`File data tidak ditemukan`**  
Jalankan `python scripts\fetch_data.py`. Pastikan koneksi internet aktif.

**Dashboard tidak terbuka**  
Periksa terminal; buka `http://localhost:8501` manual. Jika port dipakai, jalankan
`python -m streamlit run app.py --server.port 8502`.

**`ModuleNotFoundError`**  
Aktifkan venv lalu `python -m pip install -r requirements.txt`.

**Data terlihat berbeda setelah diambil ulang**  
Yahoo Finance dapat merevisi data. Catat tanggal pengambilan di
`data/raw/historical/metadata.json`; jangan membandingkan laporan lama dan baru tanpa menyebut
tanggalnya.

**Ingin menghapus progres/paper trading?**  
Hapus `data/user/learning_progress.json` dan/atau `data/user/paper_trades.csv`. File mentah dan
data pasar tidak terpengaruh.

---

## 11. Keamanan dan privasi

- Tidak ada kredensial, API key, nomor rekening, atau koneksi broker.
- Jangan menaruh password/API key di file proyek.
- File `data/user/*` bersifat lokal; `.gitignore` sudah mengecualikannya dari Git.
- Jangan mengunggah data pribadi ke layanan pihak ketiga tanpa izin.

---

**Pengingat terakhir:** belajar itu tentang membangun proses yang jujur. Kalau hasilnya buruk,
jangan mengubah data atau modal virtual agar terlihat bagus. Catat, evaluasi, lalu perbaiki
keputusan berikutnya.
