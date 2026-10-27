# 📚 Materi Belajar SahamLab

Materi bacaan lengkap **9 modul**, **18 pelajaran**, dan
**54 soal pilihan ganda**. Total waktu baca sekitar
**4 jam 8 menit**.

Folder ini cocok dibuka langsung di VSCode. Setiap modul punya satu notebook berisi
dua pelajaran, kuis, kunci jawaban, dan checklist.

> **Bukan rekomendasi investasi.** Materi ini untuk belajar. Tidak ada keuntungan
> yang dijamin, dan modal bisa berkurang.

## Mulai dari sini

1. Buka folder proyek `project saham` di VSCode.
2. Pasang ekstensi **Python** dan **Jupyter**.
3. Buka [`00_Panduan_Belajar.ipynb`](00_Panduan_Belajar.ipynb).
4. Pilih satu modul di bawah dan baca satu pelajaran per sesi.

Untuk membaca materi, notebook tidak perlu dijalankan. Pilih kernel Python hanya
jika ingin menjalankan sel kode opsional.

## Daftar modul

| # | Modul | Estimasi | Notebook |
|---:|---|---:|---|
| 1 | 🌱 Memahami Saham dari Nol | 26 menit | [Buka](Modul_01_Memahami_Saham_dari_Nol.ipynb) |
| 2 | 🧺 Mengelola Modal Rp700.000 | 27 menit | [Buka](Modul_02_Mengelola_Modal_Rp700_000.ipynb) |
| 3 | 🛡️ Memahami Risiko Investasi | 27 menit | [Buka](Modul_03_Memahami_Risiko_Investasi.ipynb) |
| 4 | 🔍 Mengenal Aplikasi dan Sumber Data | 26 menit | [Buka](Modul_04_Mengenal_Aplikasi_dan_Sumber_Data.ipynb) |
| 5 | 🧾 Membaca Laporan Keuangan | 31 menit | [Buka](Modul_05_Membaca_Laporan_Keuangan.ipynb) |
| 6 | 🐍 Analisis Saham dengan Python | 32 menit | [Buka](Modul_06_Analisis_Saham_dengan_Python.ipynb) |
| 7 | 📝 Simulasi dan Paper Trading | 27 menit | [Buka](Modul_07_Simulasi_dan_Paper_Trading.ipynb) |
| 8 | 🚦 Persiapan Pembelian Saham Pertama | 27 menit | [Buka](Modul_08_Persiapan_Pembelian_Saham_Pertama.ipynb) |
| 9 | 🌳 Membangun Kebiasaan Investor | 25 menit | [Buka](Modul_09_Membangun_Kebiasaan_Investor.ipynb) |

## Alur belajar

1. Baca satu pelajaran sampai selesai.
2. Jawab tiga soal tanpa membuka kunci.
3. Buka kunci dan pelajari pembahasannya.
4. Lanjut jika minimal **2 dari 3** jawaban benar.
5. Tulis catatan dengan kata sendiri.
6. Setelah beberapa modul, buka dashboard untuk simulasi dan paper trading.

## Bedanya dengan folder `notebooks/`

| Folder | Isi | Cara pakai |
|---|---|---|
| `notebooks pembelajaran/` | Materi bacaan, kuis, kunci jawaban | Dibaca di VSCode; tidak perlu dijalankan |
| `notebooks/` | Lab Python dengan output nyata | Dijalankan dengan kernel Python dan data proyek |

## Membuat ulang materi

Dari root proyek:

```powershell
python scripts\build_learning_notebooks.py
```

Generator membaca `src/learning_content.py` dan menimpa notebook dengan nama yang
sama. Simpan catatan pribadi di file terpisah agar tidak hilang.

## Menjalankan dashboard

```powershell
python -m streamlit run app.py
```

Progres kuis otomatis, simulasi Rp700.000, dan paper trading tersedia di dashboard.
Folder materi ini tidak mengubah progres dashboard.

## Pengingat

- Gunakan uang yang siap menghadapi risiko.
- Jangan memakai utang, margin, atau uang kebutuhan.
- Harga saham bisa turun dan modal bisa berkurang.
- Materi ini bukan nasihat keuangan, pajak, atau hukum.
