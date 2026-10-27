"""Isi kurikulum belajar saham.

Materi disimpan sebagai data Python agar mudah ditampilkan di dashboard dan
diuji. Setiap pelajaran memiliki 3 pertanyaan pilihan ganda. Pengguna harus
menjawab minimal 2 benar untuk membuka pelajaran berikutnya.
"""

from __future__ import annotations

MODULES: list[dict] = [
    {
        "id": "m1",
        "number": 1,
        "title": "Memahami Saham dari Nol",
        "icon": "🌱",
        "description": "Apa yang sebenarnya kamu beli saat membeli saham, dan dari mana untung atau rugi datang.",
        "lessons": [
            {
                "id": "m1l1",
                "title": "Apa itu saham?",
                "minutes": 12,
                "goal": "Memahami bahwa saham adalah bukti kepemilikan usaha, bukan utang, dan bukan tiket pasti untung.",
                "sections": [
                    {
                        "heading": "Saham itu surat kepemilikan",
                        "body": """
                            Bayangkan Pak Budi punya usaha bakso yang nilainya Rp10.000.000. Ia membagi usaha itu menjadi 100.000 lembar. Maka satu lembar mewakili 1/100.000 bagian dari warung bakso tersebut.

                            Kalau kamu membeli 5.000 lembar, kamu memiliki 5% dari usaha bakso itu. Kamu bukan memberi pinjaman kepada Pak Budi. Kamu ikut menjadi pemilik kecil. Karena itu, kamu ikut merasakan ketika usaha untung, dan ikut merasakan ketika usaha rugi.

                            Di bursa saham, saham adalah bukti kepemilikan atas sebagian perusahaan. Ketika membeli saham BBCA, kamu membeli sebagian kecil dari Bank Central Asia, bukan hanya sebuah kode yang bergerak di layar.
                        """,
                    },
                    {
                        "heading": "Mengapa perusahaan menjual saham?",
                        "body": """
                            Perusahaan membutuhkan uang untuk membuka cabang, membeli alat, melunasi utang, atau mengembangkan produk. Ada dua cara besar untuk mendapatkan uang: berutang atau menjual sebagian kepemilikan.

                            Menjual saham berarti pemilik lama rela memberikan sebagian kepemilikan kepada investor baru. Uangnya tidak harus dikembalikan seperti utang. Sebagai gantinya, investor ikut memiliki perusahaan dan berhak atas bagian keuntungan yang dibagikan.

                            Konsekuensinya, kepemilikan pemilik lama menjadi lebih kecil. Ini disebut dilusi. Perusahaan juga harus terbuka kepada publik, termasuk melaporkan kinerja secara berkala.
                        """,
                    },
                    {
                        "heading": "Dari mana investor mendapat untung atau rugi?",
                        "body": """
                            Ada dua sumber utama:

                            1. **Kenaikan harga saham.** Kalau perusahaan makin bernilai, harga saham bisa naik. Tetapi harga juga dipengaruhi harapan, berita, suku bunga, dan suasana pasar. Kenaikan tidak dijamin.
                            2. **Dividen.** Sebagian laba perusahaan dapat dibagikan kepada pemegang saham. Tidak semua perusahaan membagi dividen; ada yang memilih memakai laba untuk berkembang.

                            Kerugian terjadi ketika harga turun, perusahaan bangkrut, atau kamu menjual di harga yang lebih rendah. Dalam skenario terburuk, nilai saham bisa mendekati nol. Karena itu, uang yang dipakai membeli saham harus uang yang siap menghadapi risiko.
                        """,
                    },
                    {
                        "heading": "Investasi, trading, menabung, dan spekulasi",
                        "body": """
                            | Kegiatan | Tujuan utama | Jangka waktu | Risiko |
                            |---|---|---|---|
                            | Menabung | Menyimpan uang aman | Pendek | Sangat rendah, tetapi nilai beli bisa tergerus inflasi |
                            | Investasi | Ikut tumbuh bersama usaha | Panjang, bertahun-tahun | Sedang; harga bisa turun sementara |
                            | Trading | Memanfaatkan pergerakan harga | Pendek | Tinggi; butuh waktu, disiplin, dan biaya |
                            | Spekulasi | Bertaruh pada harga naik cepat | Sangat pendek | Sangat tinggi; bisa kehilangan sebagian besar modal |

                            Untuk pemula dengan modal kecil, fokus belajar sebaiknya pada investasi jangka panjang dan pemahaman risiko, bukan mengejar keuntungan harian.
                        """,
                    },
                ],
                "analogy": """
                    Saham itu seperti membeli sepotong warung bakso. Kalau warung makin ramai, nilai potonganmu bisa naik. Kalau warung sepi, nilai potonganmu bisa turun. Kamu tidak bisa menuntut Pak Budi mengembalikan uangmu seperti saat menagih utang; kamu harus mencari pembeli lain yang mau membeli bagianmu.
                """,
                "example": """
                    Warung bakso Pak Budi bernilai **Rp10.000.000** dan dibagi menjadi **100.000 lembar**. Harga satu lembar secara sederhana adalah **Rp100**.

                    Pak Budi menjual **20.000 lembar (20%)** kepada investor dan mendapatkan **Rp2.000.000** untuk membeli gerobak baru. Kamu membeli **5.000 lembar** seharga **Rp500.000**, sehingga memiliki **5%** usaha.

                    Tahun berikutnya warung untung **Rp1.000.000**. Laba per lembar (EPS) = Rp1.000.000 ÷ 100.000 = **Rp10**. Jika 30% laba dibagikan sebagai dividen, total dividen Rp300.000, atau **Rp3 per lembar**. Bagianmu: 5.000 × Rp3 = **Rp15.000**.

                    Kalau harga saham naik dari Rp100 menjadi Rp120, nilai 5.000 lembarmu menjadi Rp600.000. Tetapi kalau usaha sepi dan harga turun ke Rp70, nilainya menjadi Rp350.000. Dividen dan kenaikan harga **tidak dijamin**.
                """,
                "application": """
                    Saat melihat kode saham di aplikasi, ingat bahwa di balik kode itu ada perusahaan nyata dengan karyawan, utang, pelanggan, dan laba. Sebelum membeli, tanyakan: apa yang saya beli, bagaimana perusahaan menghasilkan uang, dan seberapa besar saya siap kehilangan?
                """,
                "python": "",
                "mistakes": [
                    "Menganggap saham sebagai utang yang pasti dikembalikan.",
                    "Menganggap harga saham murah berarti perusahaan otomatis bagus.",
                    "Membeli karena teman atau media sosial bilang akan naik.",
                    "Memakai seluruh uang yang dimiliki karena yakin tidak akan turun.",
                ],
                "summary": [
                    "Saham = bukti kepemilikan sebagian perusahaan.",
                    "Keuntungan datang dari dividen dan kenaikan harga; keduanya tidak dijamin.",
                    "Kerugian bisa terjadi, termasuk kehilangan sebagian besar modal.",
                    "Investasi jangka panjang berbeda dari trading dan spekulasi.",
                    "Pemilik saham memiliki risiko terbatas pada uang yang diinvestasikan, bukan ikut menanggung seluruh utang perusahaan.",
                ],
                "quiz": [
                    {
                        "q": "Apa arti memiliki saham sebuah perusahaan?",
                        "options": [
                            "Memberi pinjaman yang wajib dikembalikan perusahaan",
                            "Memiliki sebagian kecil kepemilikan perusahaan",
                            "Membeli produk perusahaan dengan diskon",
                            "Menjamin perusahaan tidak akan bangkrut",
                        ],
                        "answer": 1,
                        "why": "Saham adalah bukti kepemilikan. Pemegang saham ikut menikmati keuntungan dan menanggung risiko penurunan nilai, bukan memberi pinjaman.",
                    },
                    {
                        "q": "Manakah yang merupakan sumber potensi keuntungan pemegang saham?",
                        "options": [
                            "Dividen dan kenaikan harga saham",
                            "Bunga tetap yang dibayar setiap bulan",
                            "Jaminan keuntungan dari bursa",
                            "Potongan harga saat membeli saham",
                        ],
                        "answer": 0,
                        "why": "Investor dapat memperoleh dividen dan/atau kenaikan harga. Tidak ada bunga tetap atau jaminan keuntungan dalam saham.",
                    },
                    {
                        "q": "Jika perusahaan mengalami kebangkrutan, apa yang umumnya terjadi pada pemegang saham?",
                        "options": [
                            "Tetap menerima seluruh modal kembali",
                            "Hanya kehilangan uang yang diinvestasikan, karena tanggung jawabnya terbatas",
                            "Wajib membayar seluruh utang perusahaan",
                            "Otomatis mendapat saham perusahaan lain",
                        ],
                        "answer": 1,
                        "why": "Pemegang saham umumnya memiliki tanggung jawab terbatas sebesar modal yang disetor. Namun nilai saham bisa turun drastis atau menjadi nol.",
                    },
                ],
            },
            {
                "id": "m1l2",
                "title": "Pasar saham dan istilah wajib",
                "minutes": 14,
                "goal": "Mengenal BEI, IHSG, sekuritas, lot, bid, ask, dan biaya transaksi tanpa bingung.",
                "sections": [
                    {
                        "heading": "Pasar saham itu apa?",
                        "body": """
                            Pasar saham adalah tempat orang membeli dan menjual saham. Di Indonesia, tempat berlangsungnya perdagangan adalah **Bursa Efek Indonesia (BEI)**. BEI menyediakan aturan dan sistem, tetapi kamu tidak membeli langsung di gedung BEI.

                            Kamu membuka **rekening saham** melalui perusahaan sekuritas yang menjadi anggota bursa. Sekuritas meneruskan order-mu ke sistem bursa. Dana dan saham disimpan melalui lembaga penyelesaian dan kustodian, bukan dipegang fisik olehmu.
                        """,
                    },
                    {
                        "heading": "Siapa saja yang terlibat?",
                        "body": """
                            - **OJK** mengatur dan mengawasi sektor keuangan, termasuk pasar modal.
                            - **BEI** mengoperasikan bursa dan menetapkan aturan perdagangan.
                            - **KSEI** mencatat kepemilikan saham secara elektronik.
                            - **Perusahaan sekuritas** membuka rekening, menerima order, dan mengenakan biaya.
                            - **Investor** adalah kamu, yang membeli dan menjual saham.

                            Sebelum memilih sekuritas, periksa izin dan statusnya di sumber resmi OJK/BEI. Jangan hanya percaya iklan atau ajakan di media sosial.
                        """,
                    },
                    {
                        "heading": "IHSG bukan satu saham",
                        "body": """
                            **IHSG (Indeks Harga Saham Gabungan)** adalah indeks yang menggambarkan pergerakan harga saham di BEI secara umum. IHSG bukan perusahaan dan tidak bisa dibeli langsung. IHSG dipakai sebagai **benchmark**: pembanding untuk melihat apakah portofoliomu bergerak searah atau lebih baik/lebih buruk dari pasar secara umum.

                            Ada juga indeks lain untuk kelompok saham tertentu. Jangan menganggap IHSG mewakili setiap saham; saham kecil bisa bergerak sangat berbeda.
                        """,
                    },
                    {
                        "heading": "Lot, bid, ask, dan biaya",
                        "body": """
                            **Lot** adalah satuan transaksi. Berdasarkan aturan BEI yang berlaku saat proyek dibuat, **1 lot = 100 lembar**. Kalau harga saham Rp2.000 per lembar, satu lot bernilai Rp200.000 sebelum biaya. Aturan dapat berubah, jadi cek informasi resmi BEI.

                            **Bid** adalah harga tertinggi yang bersedia dibayar pembeli. **Ask/offer** adalah harga terendah yang bersedia diterima penjual. Selisih keduanya disebut **spread**. Saham yang ramai biasanya punya spread lebih tipis dan lebih mudah diperdagangkan.

                            Biaya transaksi biasanya terdiri dari komisi sekuritas saat beli, komisi saat jual, dan pajak penjualan. Besarnya berbeda antar sekuritas. Contoh yang sering dipakai: komisi beli 0,15%, komisi jual 0,15%, dan pajak jual 0,1%. Angka ini hanya contoh, bukan tarif semua broker.
                        """,
                    },
                ],
                "analogy": """
                    Pasar saham seperti pasar bakso yang sangat ramai. Ada penjual yang memasang harga (ask) dan pembeli yang menawar (bid). Kalau kamu ingin cepat membeli, kamu biasanya membayar harga penjual. Kalau ingin cepat menjual, kamu menerima harga pembeli. Selisih harga itu adalah salah satu biaya tersembunyi.
                """,
                "example": """
                    Kamu ingin membeli 1 lot saham seharga **Rp2.000** per lembar.

                    - Nilai saham: 100 × Rp2.000 = **Rp200.000**
                    - Komisi beli 0,15%: Rp300
                    - Total keluar: **Rp200.300**

                    Lalu kamu menjualnya di harga yang sama, Rp2.000:

                    - Nilai jual: Rp200.000
                    - Komisi jual 0,15%: Rp300
                    - Pajak jual 0,1%: Rp200
                    - Uang diterima: **Rp199.500**

                    Meskipun harga tidak berubah, kamu rugi **Rp800** karena biaya. Ini contoh kenapa transaksi bolak-balik terlalu sering bisa menggerus modal.
                """,
                "application": """
                    Di aplikasi sekuritas, perhatikan lot, harga bid/ask, dan rincian biaya sebelum menekan tombol beli. Gunakan order limit jika ingin menentukan harga maksimum, bukan asal menekan beli di harga berapa pun.
                """,
                "python": """
                    ```python
                    harga = 2_000
                    lot = 1
                    lembar = lot * 100
                    nilai = harga * lembar
                    biaya_beli = nilai * 0.0015
                    total = nilai + biaya_beli
                    print(f"Nilai: Rp{nilai:,.0f}, total: Rp{total:,.0f}")
                    ```
                """,
                "mistakes": [
                    "Mengira bisa membeli satu lembar; transaksi minimum di pasar reguler adalah satu lot.",
                    "Lupa menghitung komisi dan pajak sehingga merasa untung padahal rugi.",
                    "Membeli di harga ask tertinggi tanpa melihat antrean bid/ask.",
                    "Menganggap IHSG naik berarti semua saham pasti naik.",
                ],
                "summary": [
                    "BEI adalah bursa; sekuritas adalah pintu masuk investor.",
                    "IHSG adalah indeks pembanding, bukan saham yang bisa dibeli.",
                    "1 lot = 100 lembar (cek aturan terbaru).",
                    "Bid = harga pembeli, ask = harga penjual, spread = selisihnya.",
                    "Biaya transaksi mengurangi hasil bersih.",
                ],
                "quiz": [
                    {
                        "q": "Apa fungsi utama perusahaan sekuritas bagi investor?",
                        "options": [
                            "Menjamin harga saham selalu naik",
                            "Membuka rekening dan meneruskan order ke bursa",
                            "Menentukan harga penutupan semua saham",
                            "Membayar pajak penghasilan investor",
                        ],
                        "answer": 1,
                        "why": "Sekuritas adalah perantara berizin yang membuka rekening efek dan meneruskan order. Sekuritas tidak menjamin keuntungan.",
                    },
                    {
                        "q": "Jika harga saham Rp2.000 dan 1 lot = 100 lembar, berapa nilai satu lot sebelum biaya?",
                        "options": ["Rp20.000", "Rp200.000", "Rp2.000.000", "Rp200"],
                        "answer": 1,
                        "why": "1 lot = 100 lembar. 100 × Rp2.000 = Rp200.000.",
                    },
                    {
                        "q": "Apa yang dimaksud dengan spread bid-ask?",
                        "options": [
                            "Selisih harga beli tertinggi dan harga jual terendah",
                            "Jumlah saham yang dimiliki investor",
                            "Biaya pajak penjualan saham",
                            "Persentase dividen yang dibagikan",
                        ],
                        "answer": 0,
                        "why": "Bid adalah harga tertinggi yang mau dibayar pembeli; ask adalah harga terendah yang mau diterima penjual. Selisihnya disebut spread.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m2",
        "number": 2,
        "title": "Mengelola Modal Rp700.000",
        "icon": "🧺",
        "description": "Memilah uang, menjaga dana cadangan, dan menghitung hasil bersih setelah biaya.",
        "lessons": [
            {
                "id": "m2l1",
                "title": "Uang mana yang boleh diinvestasikan?",
                "minutes": 12,
                "goal": "Menentukan porsi modal yang aman diinvestasikan tanpa mengorbankan kebutuhan dan dana darurat.",
                "sections": [
                    {
                        "heading": "Tiga keranjang uang",
                        "body": """
                            Sebelum membeli saham, pisahkan uang menjadi tiga keranjang:

                            1. **Uang kebutuhan**: makan, transportasi, pulsa, buku, dan keperluan sehari-hari.
                            2. **Dana cadangan**: uang yang disimpan untuk keadaan tak terduga, misalnya sakit, laptop rusak, atau kebutuhan mendadak. Untuk orang dewasa yang punya penghasilan, target umum adalah 3–6 bulan pengeluaran. Untuk pelajar yang masih ditanggung orang tua, tetap penting punya cadangan kecil.
                            3. **Uang investasi**: uang yang jika nilainya turun 30–50% dalam beberapa tahun, hidupmu tidak langsung terganggu.

                            Hanya keranjang ketiga yang layak dipakai membeli saham.
                        """,
                    },
                    {
                        "heading": "Apakah Rp700.000 harus diinvestasikan semua?",
                        "body": """
                            Tidak. Tidak ada aturan bahwa seluruh modal harus masuk pasar. Kalau kamu masih membangun dana cadangan, prioritaskan keamanan.

                            Contoh pembagian yang konservatif:

                            - Rp300.000 tetap sebagai cadangan.
                            - Rp400.000 dijadikan batas maksimum uang belajar investasi.

                            Angka ini hanya contoh, bukan resep. Yang penting adalah kamu sudah memisahkan uang dan mengetahui batas kerugian maksimum yang bisa kamu terima. Jika kehilangan Rp400.000 membuatmu tidak bisa makan atau membayar kebutuhan penting, jangan investasikan uang itu.
                        """,
                    },
                    {
                        "heading": "Mengapa berutang untuk membeli saham berbahaya?",
                        "body": """
                            Utang memiliki bunga dan tanggal jatuh tempo. Saham tidak punya kewajiban memberi hasil pada waktu tertentu. Kalau kamu meminjam uang lalu harga saham turun, kamu tetap harus membayar utang beserta bunganya.

                            Ini bisa memaksa kamu menjual saham saat harga sedang rendah, atau menutup kerugian dengan uang kebutuhan. Hindari utang, paylater, atau margin untuk belajar saham. Gunakan hanya uang yang benar-benar milikmu.
                        """,
                    },
                ],
                "analogy": """
                    Membagi uang seperti menyiapkan bekal pendakian. Air minum tidak boleh dipakai untuk menyalakan api. Dana cadangan adalah air minummu; uang investasi adalah camilan tambahan. Kalau camilan habis, pendakian tetap aman. Jangan menukar air minum dengan harapan mendapat camilan lebih banyak.
                """,
                "example": """
                    Modal awal **Rp700.000**. Kamu memilih:

                    - Dana cadangan: **Rp350.000**
                    - Batas uang investasi: **Rp350.000**

                    Lalu kamu membeli 1 lot saham seharga Rp2.500 = Rp250.000, ditambah biaya beli 0,15% = Rp375, sehingga total **Rp250.375**. Sisa uang tunai dari modal awal: **Rp449.625**.

                    Jika harga turun 30%, nilai saham menjadi Rp175.000. Kerugian bersih setelah biaya sekitar Rp75.812, atau sekitar **21,7% dari total modal Rp700.000**. Kalau seluruh Rp700.000 diinvestasikan, kerugian rupiah bisa jauh lebih besar dan ruang belajarmu habis.
                """,
                "application": """
                    Sebelum memasukkan angka ke aplikasi, tulis dulu di catatan: total uang, kebutuhan terdekat, dana cadangan, dan batas uang investasi. Jangan pernah memakai angka modal yang membuatmu tidak bisa membeli kebutuhan dasar.
                """,
                "python": """
                    ```python
                    modal = 700_000
                    dana_cadangan = 350_000
                    batas_investasi = modal - dana_cadangan
                    persen_investasi = batas_investasi / modal * 100
                    print(f"Batas investasi: Rp{batas_investasi:,.0f} ({persen_investasi:.0f}%)")
                    ```
                """,
                "mistakes": [
                    "Menginvestasikan seluruh Rp700.000 karena merasa masih muda.",
                    "Memakai uang jajan atau uang kebutuhan untuk membeli saham.",
                    "Berutang atau memakai paylater agar bisa membeli lebih banyak.",
                    "Menganggap dana cadangan tidak perlu karena masih ditanggung orang tua.",
                ],
                "summary": [
                    "Pisahkan uang kebutuhan, dana cadangan, dan uang investasi.",
                    "Tidak semua modal harus diinvestasikan.",
                    "Batas kerugian harus diketahui sebelum membeli.",
                    "Hindari utang dan leverage untuk belajar saham.",
                    "Modal kecil bukan alasan untuk mengambil risiko yang tidak perlu.",
                ],
                "quiz": [
                    {
                        "q": "Uang seperti apa yang layak dipakai membeli saham?",
                        "options": [
                            "Uang kebutuhan bulan ini",
                            "Uang yang jika nilainya turun tidak mengganggu kebutuhan dasar",
                            "Uang pinjaman dengan bunga rendah",
                            "Uang dana cadangan satu-satunya",
                        ],
                        "answer": 1,
                        "why": "Uang investasi harus uang yang siap menghadapi penurunan nilai tanpa mengganggu kebutuhan dan dana cadangan.",
                    },
                    {
                        "q": "Mengapa berutang untuk membeli saham berisiko?",
                        "options": [
                            "Karena saham tidak pernah naik",
                            "Karena utang tetap harus dibayar meskipun harga saham turun",
                            "Karena broker melarang semua investor memakai utang",
                            "Karena dividen selalu lebih besar dari bunga",
                        ],
                        "answer": 1,
                        "why": "Kewajiban utang tetap ada. Jika saham turun, kamu bisa terpaksa menjual rugi atau memakai uang kebutuhan untuk membayar utang.",
                    },
                    {
                        "q": "Dari modal Rp700.000, kamu menyisihkan Rp350.000 sebagai cadangan. Berapa batas maksimum uang investasi pada contoh ini?",
                        "options": ["Rp700.000", "Rp350.000", "Rp1.050.000", "Rp0"],
                        "answer": 1,
                        "why": "Rp700.000 − Rp350.000 = Rp350.000. Ini hanya contoh pembagian, bukan aturan wajib.",
                    },
                ],
            },
            {
                "id": "m2l2",
                "title": "Menghitung untung bersih dan dampak kerugian",
                "minutes": 15,
                "goal": "Menghitung hasil investasi setelah biaya serta memahami efek penurunan 5%, 10%, dan 30%.",
                "sections": [
                    {
                        "heading": "Rumus dasar",
                        "body": """
                            **Nilai beli kotor** = harga per lembar × jumlah lembar.
                            **Total beli** = nilai beli kotor + komisi beli.
                            **Nilai jual kotor** = harga jual × jumlah lembar.
                            **Hasil jual bersih** = nilai jual kotor − komisi jual − pajak jual.
                            **Laba/rugi bersih** = hasil jual bersih − total beli.

                            Persentase return sebaiknya dihitung dari **total beli**, bukan hanya nilai saham, karena biaya ikut keluar dari kantongmu.
                        """,
                    },
                    {
                        "heading": "Contoh tiga skenario",
                        "body": """
                            Beli 1 lot di Rp2.500. Total beli = Rp250.000 + Rp375 = **Rp250.375**.

                            | Perubahan harga | Nilai jual kotor | Biaya jual + pajak | Hasil bersih | Laba/rugi bersih | Return |
                            |---|---|---|---|---|---|
                            | +5% | Rp262.500 | Rp656 | Rp261.844 | +Rp11.469 | +4,58% |
                            | −10% | Rp225.000 | Rp563 | Rp224.438 | −Rp25.938 | −10,36% |
                            | −30% | Rp175.000 | Rp438 | Rp174.563 | −Rp75.813 | −30,28% |

                            Perhatikan: kenaikan harga 5% tidak menghasilkan untung 5% karena ada biaya. Penurunan 30% terasa lebih menyakitkan daripada kenaikan 30%, karena modal yang tersisa harus naik lebih besar untuk kembali ke titik awal.
                        """,
                    },
                    {
                        "heading": "Ilusi kembali ke titik awal",
                        "body": """
                            Kalau nilai investasi turun 30%, dari Rp100 menjadi Rp70, maka untuk kembali ke Rp100 dibutuhkan kenaikan **42,9%** dari Rp70. Bukan 30%.

                            Rumus pemulihan = (harga awal ÷ harga sekarang) − 1.

                            Inilah alasan melindungi modal lebih penting daripada mengejar kenaikan kecil. Semakin besar kerugian, semakin besar usaha yang dibutuhkan untuk pulih.
                        """,
                    },
                    {
                        "heading": "Jangan lupa uang yang tidak diinvestasikan",
                        "body": """
                            Jika dari Rp700.000 kamu hanya menginvestasikan Rp250.375, sisa Rp449.625 tetap aman. Kerugian 30% pada saham tidak berarti kamu kehilangan 30% dari seluruh modal.

                            Hitung dua perspektif:

                            - **Return investasi** = laba/rugi ÷ uang yang benar-benar diinvestasikan.
                            - **Dampak pada modal total** = laba/rugi ÷ Rp700.000.

                            Keduanya penting. Return investasi menunjukkan performa saham; dampak modal total menunjukkan seberapa besar hidupmu terpengaruh.
                        """,
                    },
                ],
                "analogy": """
                    Membeli saham seperti menanam bibit. Biaya membeli pot dan pupuk membuat modal awal lebih besar dari harga bibit. Kalau bibit tumbuh 5%, belum tentu kamu untung setelah biaya. Kalau bibit mati, kamu kehilangan modal, bukan hanya potnya.
                """,
                "example": """
                    Modal **Rp700.000**, alokasi investasi **Rp350.000**.

                    Kamu membeli 1 lot saham Rp2.500:

                    - Nilai saham: Rp250.000
                    - Komisi beli 0,15%: Rp375
                    - Total keluar: Rp250.375
                    - Sisa alokasi: Rp99.625
                    - Sisa modal yang tidak dialokasikan: Rp350.000

                    Jika harga turun 30%, hasil jual bersih sekitar Rp174.563. Kerugian bersih Rp75.813. Itu sekitar **21,7% dari total modal Rp700.000**, bukan 30%, karena tidak semua modal masuk saham.
                """,
                "application": """
                    Gunakan halaman **Simulasi Rp700.000** di dashboard untuk mengubah harga, lot, persentase perubahan, dan biaya. Biasakan melihat angka **laba/rugi bersih** dan **persentase terhadap total modal**, bukan hanya harga saham.
                """,
                "python": """
                    ```python
                    def simulasi(modal, alokasi, harga, lot, perubahan, fee_beli=0.0015, fee_jual=0.0015, pajak=0.001):
                        lembar = lot * 100
                        beli = harga * lembar
                        total_beli = beli * (1 + fee_beli)
                        jual = harga * (1 + perubahan) * lembar
                        bersih = jual * (1 - fee_jual - pajak)
                        return bersih - total_beli, (bersih - total_beli) / modal * 100

                    print(simulasi(700_000, 350_000, 2_500, 1, -0.30))
                    ```
                """,
                "mistakes": [
                    "Menghitung untung dari selisih harga saja tanpa biaya.",
                    "Menganggap penurunan 30% cukup pulih dengan kenaikan 30%.",
                    "Membandingkan return saham dengan return seluruh modal tanpa membedakan penyebut.",
                    "Menambah posisi saat rugi tanpa alasan yang kuat, hanya agar terlihat lebih murah.",
                ],
                "summary": [
                    "Laba bersih = hasil jual bersih − total beli.",
                    "Biaya membeli dan menjual harus dimasukkan.",
                    "Kerugian 30% membutuhkan kenaikan sekitar 42,9% untuk pulih.",
                    "Pisahkan return investasi dari dampak terhadap total modal.",
                    "Simulasi membantu memahami risiko sebelum memakai uang nyata.",
                ],
                "quiz": [
                    {
                        "q": "Kamu membeli 1 lot di Rp2.500. Total beli termasuk biaya 0,15% adalah sekitar...",
                        "options": ["Rp250.000", "Rp250.375", "Rp251.500", "Rp200.000"],
                        "answer": 1,
                        "why": "1 lot = 100 lembar × Rp2.500 = Rp250.000. Biaya 0,15% = Rp375. Total Rp250.375.",
                    },
                    {
                        "q": "Jika nilai investasi turun 30%, kenaikan yang dibutuhkan untuk kembali ke nilai awal adalah sekitar...",
                        "options": ["30%", "42,9%", "70%", "100%"],
                        "answer": 1,
                        "why": "Dari 100 menjadi 70. Untuk kembali ke 100 dibutuhkan (100/70) − 1 = 42,9%.",
                    },
                    {
                        "q": "Mengapa return sebaiknya dihitung dari total beli, bukan hanya harga saham?",
                        "options": [
                            "Karena biaya transaksi ikut mengurangi uang yang keluar",
                            "Karena harga saham tidak pernah berubah",
                            "Karena pajak hanya berlaku saat membeli",
                            "Karena lot selalu berubah",
                        ],
                        "answer": 0,
                        "why": "Komisi dan pajak adalah uang nyata yang keluar/masuk. Return bersih harus memperhitungkan seluruh biaya.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m3",
        "number": 3,
        "title": "Memahami Risiko Investasi",
        "icon": "🛡️",
        "description": "Mengukur fluktuasi, drawdown, dan melindungi diri lewat diversifikasi.",
        "lessons": [
            {
                "id": "m3l1",
                "title": "Volatilitas dan maximum drawdown",
                "minutes": 14,
                "goal": "Membedakan fluktuasi harian dari kerugian besar, serta membaca dua metrik risiko utama.",
                "sections": [
                    {
                        "heading": "Mengapa harga bergerak?",
                        "body": """
                            Harga saham berubah karena pembeli dan penjual bertemu dengan harapan yang berbeda. Berita perusahaan, laporan keuangan, suku bunga, harga komoditas, kebijakan pemerintah, dan suasana pasar global bisa mengubah harapan itu.

                            Sebagian pergerakan berasal dari kinerja perusahaan. Sebagian lagi berasal dari emosi dan arus dana jangka pendek. Karena itu, harga bisa turun meskipun perusahaan tidak langsung mengalami kerusakan.
                        """,
                    },
                    {
                        "heading": "Volatilitas: seberapa naik-turun?",
                        "body": """
                            **Volatilitas** mengukur seberapa besar return harian menyimpang dari rata-ratanya. Semakin besar, semakin liar pergerakan harga.

                            Di dashboard, volatilitas historis disetahunkan dengan rumus:

                            **Volatilitas tahunan = simpangan baku return harian × √252**

                            Angka 252 adalah perkiraan jumlah hari perdagangan dalam setahun. Volatilitas 20% berarti dalam setahun harga cenderung bergerak dalam rentang yang cukup lebar; itu bukan batas maksimum kerugian.

                            Volatilitas tinggi tidak selalu buruk, tetapi biasanya membuat perjalanan lebih tidak nyaman dan risiko salah mengambil keputusan lebih besar.
                        """,
                    },
                    {
                        "heading": "Maximum drawdown: seberapa dalam turun dari puncak?",
                        "body": """
                            **Drawdown** mengukur penurunan dari titik tertinggi sebelumnya. Jika harga pernah di Rp1.000 lalu turun ke Rp700, drawdown-nya −30%.

                            **Maximum drawdown** adalah drawdown terburuk dalam periode yang diukur. Metrik ini menjawab: kalau kamu membeli di titik terburuk, seberapa besar penurunan yang pernah dialami?

                            Drawdown berbeda dari volatilitas. Saham bisa punya volatilitas harian rendah tetapi turun perlahan sangat dalam dalam beberapa tahun.
                        """,
                    },
                    {
                        "heading": "Perusahaan besar juga bisa jatuh",
                        "body": """
                            Ukuran perusahaan besar bukan jaminan harga tidak turun. Perubahan teknologi, utang yang berat, persaingan, regulasi, dan salah strategi bisa menekan nilai perusahaan bertahun-tahun.

                            Contoh historis di pasar Indonesia menunjukkan saham besar pun bisa mengalami penurunan puluhan persen. Karena itu, jangan menyimpulkan "terlalu besar untuk gagal". Selalu lihat utang, arus kas, dan prospek usaha.
                        """,
                    },
                ],
                "analogy": """
                    Volatilitas seperti naik roller coaster: naik-turunnya cepat dan membuat jantung berdebar. Maximum drawdown seperti selisih antara puncak tertinggi dan lembah terdalam. Kamu bisa selamat dari roller coaster, tetapi tetap perlu tahu seberapa dalam lembahnya sebelum membeli tiket.
                """,
                "example": """
                    Harga saham: Rp1.000 → Rp1.200 → Rp900 → Rp1.100.

                    - Puncak sementara: Rp1.200
                    - Lembah setelah puncak: Rp900
                    - Drawdown di lembah: (900 ÷ 1.200) − 1 = **−25%**
                    - Untuk kembali ke Rp1.200 dari Rp900, dibutuhkan kenaikan **33,3%**.

                    Jika modal Rp350.000 turun 25%, nilainya menjadi Rp262.500. Kerugian Rp87.500. Angka persentase terlihat kecil, tetapi rupiahnya nyata.
                """,
                "application": """
                    Buka halaman **Analisis Risiko** dan bandingkan volatilitas serta maximum drawdown beberapa saham. Jangan hanya melihat return tertinggi; lihat juga perjalanan turunnya.
                """,
                "python": """
                    ```python
                    import numpy as np
                    import pandas as pd

                    harga = pd.Series([1000, 1200, 900, 1100])
                    drawdown = harga / harga.cummax() - 1
                    print(drawdown.min())  # sekitar -0.25
                    ```
                """,
                "mistakes": [
                    "Menganggap volatilitas rendah berarti bebas risiko.",
                    "Menganggap saham besar tidak mungkin turun dalam.",
                    "Melihat return setahun terakhir tanpa melihat drawdown.",
                    "Panik menjual hanya karena satu hari merah.",
                ],
                "summary": [
                    "Harga bergerak karena perubahan harapan dan kondisi pasar.",
                    "Volatilitas mengukur naik-turun return; drawdown mengukur penurunan dari puncak.",
                    "Maximum drawdown menunjukkan kerugian terdalam secara historis.",
                    "Perusahaan besar tetap bisa mengalami penurunan besar.",
                    "Metrik historis bukan ramalan masa depan.",
                ],
                "quiz": [
                    {
                        "q": "Apa yang diukur oleh maximum drawdown?",
                        "options": [
                            "Keuntungan rata-rata per tahun",
                            "Penurunan terbesar dari titik puncak ke titik terendah",
                            "Jumlah dividen yang dibagikan",
                            "Banyaknya transaksi dalam sehari",
                        ],
                        "answer": 1,
                        "why": "Drawdown dihitung dari puncak sebelumnya. Maximum drawdown adalah yang terdalam pada periode yang diukur.",
                    },
                    {
                        "q": "Harga turun dari Rp1.200 ke Rp900. Berapa drawdown-nya?",
                        "options": ["−25%", "−30%", "−33,3%", "−20%"],
                        "answer": 0,
                        "why": "(900 ÷ 1.200) − 1 = −0,25 atau −25%. Kenaikan yang dibutuhkan untuk pulih justru 33,3%.",
                    },
                    {
                        "q": "Mengapa volatilitas historis bukan jaminan masa depan?",
                        "options": [
                            "Karena kondisi pasar dan perusahaan dapat berubah",
                            "Karena volatilitas hanya dihitung oleh broker",
                            "Karena harga saham tidak pernah bergerak",
                            "Karena dividen selalu tetap",
                        ],
                        "answer": 0,
                        "why": "Volatilitas dihitung dari data masa lalu. Perubahan bisnis, pasar, dan kebijakan bisa membuat risiko masa depan berbeda.",
                    },
                ],
            },
            {
                "id": "m3l2",
                "title": "Diversifikasi dan risiko likuiditas",
                "minutes": 13,
                "goal": "Mengurangi risiko yang tidak perlu dan mengenali saham yang sulit diperdagangkan.",
                "sections": [
                    {
                        "heading": "Diversifikasi bukan sekadar punya banyak saham",
                        "body": """
                            **Diversifikasi** berarti menyebar uang ke beberapa aset yang tidak bergerak persis sama. Punya 10 saham bank bukan diversifikasi yang baik, karena semuanya bisa turun bersamaan ketika sektor keuangan tertekan.

                            Diversifikasi yang lebih masuk akal menyebar ke sektor dan karakter bisnis yang berbeda. Untuk pemula, reksa dana indeks bisa menjadi cara sederhana mendapatkan banyak saham sekaligus, meskipun tetap ada biaya dan risiko pasar.

                            Diversifikasi mengurangi risiko spesifik perusahaan, tetapi **tidak menghilangkan risiko pasar**. Saat seluruh pasar turun, hampir semua aset bisa ikut turun.
                        """,
                    },
                    {
                        "heading": "Risiko individual vs risiko pasar",
                        "body": """
                            **Risiko individual** adalah risiko yang khas pada satu perusahaan, misalnya produk gagal, skandal, atau pabrik terbakar. Risiko ini bisa dikurangi dengan diversifikasi.

                            **Risiko pasar** adalah risiko yang menimpa hampir semua perusahaan, misalnya resesi, kenaikan suku bunga, atau kepanikan global. Diversifikasi tidak bisa menghapusnya.

                            Karena itu, portofolio tetap bisa turun meskipun sudah berisi banyak saham.
                        """,
                    },
                    {
                        "heading": "Risiko likuiditas",
                        "body": """
                            **Likuiditas** adalah kemudahan menjual atau membeli tanpa mengubah harga terlalu banyak. Saham dengan volume dan nilai transaksi kecil bisa sulit dijual, terutama saat pasar panik.

                            Tanda likuiditas rendah: nilai transaksi harian kecil, spread bid-ask lebar, dan harga mudah melonjak atau jatuh dengan sedikit order. Saham seperti ini lebih berisiko, terutama untuk pemula.

                            Di snapshot IDX, volume dan nilai transaksi bisa membantu melihat aktivitas. Tetapi satu hari data belum cukup untuk menyimpulkan likuiditas jangka panjang.
                        """,
                    },
                    {
                        "heading": "Saham murah bukan berarti aman",
                        "body": """
                            Harga Rp50 tidak otomatis lebih murah daripada Rp5.000. Yang penting adalah nilai perusahaan dibandingkan laba, aset, dan prospeknya. Saham berharga sangat rendah bisa memiliki risiko likuiditas dan manipulasi yang tinggi.

                            Hindari saham yang harganya digerakkan oleh rumor, volume tiba-tiba tanpa berita jelas, atau ajakan "pasti naik" di grup chat. Jika terdengar terlalu bagus untuk menjadi benar, biasanya memang begitu.
                        """,
                    },
                ],
                "analogy": """
                    Diversifikasi seperti membawa beberapa jenis obat di kotak darurat. Kalau hanya membawa obat sakit kepala, kamu tidak siap untuk masalah lain. Tetapi saat badai besar datang, semua orang tetap basah. Itulah risiko pasar yang tidak bisa dihilangkan hanya dengan menambah obat.
                """,
                "example": """
                    Kamu punya Rp700.000 dan ingin membeli saham. Pilihan A: seluruh uang ke satu saham teknologi. Pilihan B: Rp250.000 ke saham bank, Rp250.000 ke saham konsumen, dan Rp200.000 tetap tunai.

                    Pilihan B tidak menjamin untung, tetapi tidak bergantung pada satu perusahaan. Jika satu saham turun 50%, dampaknya pada total portofolio lebih kecil. Namun jika seluruh pasar turun, semua saham bisa ikut turun.
                """,
                "application": """
                    Di halaman **Korelasi Saham**, lihat apakah saham-saham pilihanmu bergerak mirip. Korelasi tinggi berarti diversifikasinya kurang efektif. Tetap ingat bahwa korelasi bisa berubah dan bukan hubungan sebab-akibat.
                """,
                "python": """
                    ```python
                    bobot = {"BBCA.JK": 0.4, "ICBP.JK": 0.3, "TLKM.JK": 0.3}
                    modal = 700_000
                    for ticker, porsi in bobot.items():
                        print(ticker, f"Rp{modal * porsi:,.0f}")
                    ```
                """,
                "mistakes": [
                    "Mengira punya banyak saham otomatis berarti terdiversifikasi.",
                    "Membeli saham tidak likuid karena harganya terlihat murah.",
                    "Menganggap diversifikasi menghilangkan semua risiko.",
                    "Menambah saham baru tanpa memahami bisnisnya.",
                ],
                "summary": [
                    "Diversifikasi menyebar risiko ke aset yang berbeda.",
                    "Banyak saham di satu sektor belum tentu terdiversifikasi.",
                    "Risiko pasar tidak bisa dihilangkan sepenuhnya.",
                    "Likuiditas memengaruhi kemudahan dan harga saat menjual.",
                    "Harga rendah bukan ukuran murah atau aman.",
                ],
                "quiz": [
                    {
                        "q": "Mengapa memiliki 10 saham bank belum tentu diversifikasi yang baik?",
                        "options": [
                            "Karena bank tidak pernah membagikan dividen",
                            "Karena semuanya rentan terhadap risiko yang sama di sektor keuangan",
                            "Karena saham bank tidak likuid",
                            "Karena harga bank selalu turun",
                        ],
                        "answer": 1,
                        "why": "Diversifikasi yang baik menyebar ke risiko yang berbeda. Satu sektor bisa terkena masalah yang sama secara bersamaan.",
                    },
                    {
                        "q": "Apa itu risiko likuiditas?",
                        "options": [
                            "Risiko sulit menjual/membeli tanpa mengubah harga terlalu banyak",
                            "Risiko perusahaan membagikan dividen terlalu besar",
                            "Risiko harga saham naik terlalu cepat",
                            "Risiko lupa password rekening",
                        ],
                        "answer": 0,
                        "why": "Likuiditas rendah membuat transaksi sulit dan spread lebar, sehingga harga bisa bergerak tidak menguntungkan saat kamu ingin keluar.",
                    },
                    {
                        "q": "Apakah diversifikasi menghilangkan risiko pasar?",
                        "options": [
                            "Ya, sepenuhnya",
                            "Tidak, diversifikasi hanya mengurangi risiko spesifik",
                            "Ya, jika membeli minimal 10 saham",
                            "Tidak, karena saham tidak bisa dijual",
                        ],
                        "answer": 1,
                        "why": "Saat seluruh pasar turun, hampir semua saham bisa ikut turun. Diversifikasi tidak menghapus risiko pasar.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m4",
        "number": 4,
        "title": "Mengenal Aplikasi dan Sumber Data",
        "icon": "🔍",
        "description": "Memilih sumber informasi yang bisa dipercaya dan memahami keterbatasannya.",
        "lessons": [
            {
                "id": "m4l1",
                "title": "Stockbit, TradingView, Yahoo Finance, dan sumber resmi",
                "minutes": 13,
                "goal": "Tahu fungsi, kelebihan, dan batas setiap sumber data agar tidak menelan informasi mentah-mentah.",
                "sections": [
                    {
                        "heading": "Sumber resmi dulu, aplikasi kemudian",
                        "body": """
                            Untuk informasi perusahaan, utamakan **situs resmi perusahaan** (bagian Investor Relations) dan **keterbukaan informasi BEI**. Di sana ada laporan tahunan, laporan keuangan triwulan, pengumuman aksi korporasi, dan penjelasan manajemen.

                            **OJK** menyediakan informasi regulasi dan daftar lembaga yang berizin. **KSEI** berkaitan dengan administrasi kepemilikan efek. Sumber resmi biasanya lebih lengkap dan dapat dipertanggungjawabkan, meskipun tampilannya tidak selalu semudah aplikasi.

                            Aplikasi seperti Stockbit, TradingView, dan Yahoo Finance berguna untuk menyaring informasi dan melihat grafik. Tetapi mereka adalah perantara, bukan pengganti laporan resmi.
                        """,
                    },
                    {
                        "heading": "Fungsi masing-masing alat",
                        "body": """
                            | Alat | Kegunaan utama | Kelebihan | Keterbatasan |
                            |---|---|---|---|
                            | Stockbit | Diskusi, berita, data perusahaan, screener | Banyak informasi dalam satu tempat | Konten komunitas bisa bias; fitur berbayar; verifikasi data tetap perlu |
                            | TradingView | Grafik dan indikator teknikal | Charting kuat dan fleksibel | Data bisa tertunda; tidak semua data fundamental lengkap |
                            | Yahoo Finance | Harga historis, berita, ringkasan rasio | Mudah diakses dan gratis | Data pihak ketiga bisa salah, tertunda, atau berubah; penyesuaian dividen perlu dicek |
                            | Situs BEI / perusahaan | Laporan keuangan dan pengumuman resmi | Paling otoritatif | Formatnya tidak selalu ramah pemula |
                            | Excel / Google Sheets | Mencatat dan menghitung manual | Fleksibel dan transparan | Rawan salah rumus dan tidak otomatis memperbarui |
                            | Python + Pandas | Mengolah data besar dan mengulang analisis | Reproducible dan bisa diuji | Butuh belajar; kualitas tetap bergantung sumber data |

                            Banyak layanan memiliki versi gratis dan berbayar. Harga, fitur, dan kebijakan bisa berubah, jadi periksa langsung halaman resmi masing-masing sebelum berlangganan.
                        """,
                    },
                    {
                        "heading": "Mengapa angka bisa berbeda antar aplikasi?",
                        "body": """
                            Dua aplikasi bisa menampilkan PER berbeda untuk saham yang sama karena memakai laba periode berbeda: laba setahun terakhir, proyeksi tahun depan, atau laba kuartal disetahunkan. Harga yang dipakai juga bisa harga penutupan kemarin, hari ini, atau tertunda beberapa menit.

                            Karena itu, saat membandingkan saham, pastikan:

                            - periode laporan sama;
                            - harga dan tanggal sama;
                            - definisi rasio sama;
                            - mata uang dan satuan sama.

                            Jangan mencampur PER dari satu sumber dengan PBV dari sumber lain tanpa memeriksa tanggal dan definisinya.
                        """,
                    },
                    {
                        "heading": "Data gratis tetap punya biaya tersembunyi",
                        "body": """
                            Data gratis sering memiliki keterlambatan, iklan, batas jumlah permintaan, atau cakupan yang tidak lengkap. Untuk belajar, itu biasanya cukup. Untuk keputusan besar, cek ulang ke laporan resmi.

                            Jangan memberikan password, kode OTP, atau API key pribadi kepada siapa pun. API key yang kamu buat sendiri untuk belajar juga jangan disimpan di file yang dibagikan publik.
                        """,
                    },
                ],
                "analogy": """
                    Sumber data seperti beberapa tukang cerita di pasar. Ada yang membaca langsung dari buku resmi, ada yang merangkum, ada yang menambahkan opini. Rangkuman boleh membantu, tetapi untuk keputusan penting, periksa buku aslinya.
                """,
                "example": """
                    Kamu melihat di media sosial: "PER saham X hanya 5, sangat murah!" Di laporan resmi, laba yang dipakai ternyata laba sekali dari penjualan aset, bukan laba operasional rutin. Setelah laba sekali itu dikeluarkan, PER menjadi 25.

                    Angka pertama tidak bohong secara matematis, tetapi konteksnya menyesatkan. Membaca laporan asli dan memahami sumber laba mencegah kesimpulan keliru.
                """,
                "application": """
                    Untuk setiap saham yang menarik, buka minimal dua sumber: satu aplikasi untuk gambaran cepat, satu laporan resmi untuk memastikan angka dan konteks. Catat tanggal akses di jurnal risetmu.
                """,
                "python": """
                    ```python
                    # Contoh mengambil data pihak ketiga; bukan sumber resmi.
                    import yfinance as yf

                    data = yf.download("BBCA.JK", start="2024-01-01", progress=False)
                    print(data.tail())
                    ```
                """,
                "mistakes": [
                    "Menganggap angka di aplikasi selalu real-time dan final.",
                    "Membandingkan PER dua saham dari periode laporan berbeda.",
                    "Mengikuti rekomendasi komunitas tanpa membaca laporan.",
                    "Membagikan API key atau kredensial di publik.",
                ],
                "summary": [
                    "Sumber resmi BEI dan perusahaan adalah prioritas untuk laporan keuangan.",
                    "Aplikasi membantu penyaringan, tetapi punya keterbatasan dan bias.",
                    "Angka bisa berbeda karena periode, definisi, dan waktu pembaruan.",
                    "Data gratis tidak selalu lengkap atau real-time.",
                    "Catat sumber dan tanggal akses.",
                ],
                "quiz": [
                    {
                        "q": "Sumber mana yang paling tepat untuk memeriksa laporan keuangan resmi perusahaan?",
                        "options": [
                            "Komentar di media sosial",
                            "Situs perusahaan bagian Investor Relations atau keterbukaan informasi BEI",
                            "Grup chat saham",
                            "Video motivasi investasi",
                        ],
                        "answer": 1,
                        "why": "Laporan resmi perusahaan dan pengumuman BEI adalah sumber utama untuk data keuangan dan aksi korporasi.",
                    },
                    {
                        "q": "Mengapa PER dari dua aplikasi bisa berbeda?",
                        "options": [
                            "Karena aplikasi selalu salah",
                            "Karena periode laba, harga, atau definisi yang dipakai bisa berbeda",
                            "Karena PER tidak punya rumus",
                            "Karena saham berubah nama setiap hari",
                        ],
                        "answer": 1,
                        "why": "PER bergantung pada harga dan EPS. Sumber bisa memakai laba historis, proyeksi, atau periode yang berbeda.",
                    },
                    {
                        "q": "Apa sikap yang tepat terhadap data gratis dari pihak ketiga?",
                        "options": [
                            "Langsung percaya untuk semua keputusan",
                            "Gunakan untuk belajar, lalu verifikasi ke sumber resmi bila penting",
                            "Abaikan semua data kecuali harganya",
                            "Sebarkan tanpa mencantumkan tanggal",
                        ],
                        "answer": 1,
                        "why": "Data pihak ketiga berguna, tetapi bisa tertunda atau tidak lengkap. Verifikasi ke sumber resmi penting untuk keputusan serius.",
                    },
                ],
            },
            {
                "id": "m4l2",
                "title": "Cara membaca data historis dengan benar",
                "minutes": 13,
                "goal": "Mengenali ticker, tanggal, harga adjusted, missing data, dan jebakan data yang bisa menyesatkan.",
                "sections": [
                    {
                        "heading": "Ticker dan tanggal",
                        "body": """
                            Di Yahoo Finance, saham Indonesia memakai akhiran **.JK**, misalnya `BBCA.JK`. Tanpa akhiran itu, kamu bisa mendapat perusahaan lain di negara lain. IHSG memakai ticker `^JKSE`.

                            Selalu periksa tanggal awal dan akhir data. Jangan menganggap file bernama "2026" otomatis berisi data sampai hari ini. Buka isinya, lihat tanggal maksimum, dan catat kapan data diambil.
                        """,
                    },
                    {
                        "heading": "Harga biasa vs harga adjusted",
                        "body": """
                            **Close** adalah harga penutupan apa adanya. **Adj Close** adalah harga yang disesuaikan untuk aksi korporasi seperti stock split dan dividen.

                            Contoh: harga Rp10.000 lalu stock split 1:10. Harga menjadi sekitar Rp1.000. Itu bukan kerugian 90%; jumlah lembarmu menjadi 10 kali lebih banyak. Kalau memakai harga mentah tanpa penyesuaian, grafik return akan terlihat jatuh padahal kekayaanmu tidak.

                            Untuk analisis return jangka panjang, gunakan **adj_close**. Untuk valuasi portofolio saat ini, harga pasar biasa (**close**) lebih relevan. Jelaskan pilihan ini di laporan.
                        """,
                    },
                    {
                        "heading": "Missing, duplikat, dan outlier",
                        "body": """
                            Periksa jumlah data hilang dan baris duplikat. Jangan langsung mengisi harga yang hilang dengan angka tebakan. Harga hilang bisa berarti saham tidak diperdagangkan, libur bursa, atau data sumber bermasalah.

                            **Outlier** adalah nilai yang sangat berbeda dari biasanya. Jangan otomatis menghapusnya. Bisa jadi itu hari krisis yang justru penting untuk memahami risiko. Periksa penyebabnya sebelum memutuskan.

                            Volume nol juga perlu perhatian: harga penutupan bisa merupakan harga terakhir dari hari sebelumnya, bukan transaksi baru.
                        """,
                    },
                    {
                        "heading": "Survivorship dan look-ahead bias",
                        "body": """
                            **Survivorship bias** terjadi jika kamu hanya menganalisis perusahaan yang masih ada hari ini, lalu mengabaikan perusahaan yang sudah delisting atau bangkrut. Hasilnya terlihat lebih bagus dari kenyataan.

                            **Look-ahead bias** terjadi jika analisis memakai informasi yang belum tersedia pada saat keputusan dibuat. Contoh: memakai laporan kuartal yang baru terbit bulan depan untuk mensimulasikan transaksi bulan ini.

                            Keduanya membuat backtest terlihat hebat tetapi tidak bisa diulang di dunia nyata.
                        """,
                    },
                ],
                "analogy": """
                    Data mentah seperti berita dari mulut ke mulut. Kalau kamu tidak mencatat siapa yang bicara, kapan, dan tentang periode apa, cerita bisa berubah. Harga adjusted seperti menerjemahkan cerita lama ke ukuran uang hari ini; tanpa itu, stock split terlihat seperti bencana padahal hanya pecahan yang berbeda.
                """,
                "example": """
                    Saham A melakukan stock split 1:10 pada 2024. Harga mentah turun dari Rp10.000 ke Rp1.000. Jika kamu menghitung return tanpa penyesuaian, terlihat −90%.

                    Dengan adj_close, harga historis sebelum split disesuaikan sehingga return yang dihitung mencerminkan perubahan nilai investor, bukan sekadar perubahan jumlah lembar. Tetap cek dokumentasi penyedia data karena metode penyesuaian bisa berbeda.
                """,
                "application": """
                    Sebelum menganalisis, buat checklist: ticker benar, tanggal benar, harga adjusted, missing dicek, duplikat dihapus, outlier diperiksa, dan sumber dicatat. Dashboard proyek ini memakai `adj_close` untuk analisis performa dan risiko.
                """,
                "python": """
                    ```python
                    import pandas as pd

                    df = pd.read_csv("data/processed/historical_prices.csv", parse_dates=["date"])
                    print(df.shape)
                    print(df.groupby("ticker")["date"].agg(["min", "max", "count"]))
                    print("Missing:", df.isna().sum().sum())
                    print("Duplikat:", df.duplicated(subset=["date", "ticker"]).sum())
                    ```
                """,
                "mistakes": [
                    "Memakai ticker tanpa `.JK` untuk saham Indonesia.",
                    "Menganggap harga turun setelah stock split sebagai kerugian.",
                    "Mengisi semua harga hilang dengan forward-fill tanpa batas.",
                    "Menghapus outlier krisis karena dianggap data kotor.",
                    "Memakai laporan yang belum terbit pada tanggal simulasi.",
                ],
                "summary": [
                    "Gunakan ticker yang benar dan periksa periode data.",
                    "Gunakan adj_close untuk return jangka panjang.",
                    "Jangan mengisi atau menghapus data secara sembarangan.",
                    "Waspadai survivorship dan look-ahead bias.",
                    "Catat sumber dan waktu pengambilan data.",
                ],
                "quiz": [
                    {
                        "q": "Mengapa analisis return jangka panjang sebaiknya memakai adj_close?",
                        "options": [
                            "Agar harga selalu naik",
                            "Agar pengaruh stock split dan dividen tidak membuat return menyesatkan",
                            "Karena adj_close adalah harga resmi BEI",
                            "Karena adj_close tidak pernah missing",
                        ],
                        "answer": 1,
                        "why": "Adj close menyesuaikan harga historis untuk aksi korporasi sehingga perubahan nilai investor lebih tercermin.",
                    },
                    {
                        "q": "Apa itu look-ahead bias?",
                        "options": [
                            "Memakai informasi yang belum tersedia pada saat keputusan dibuat",
                            "Melihat grafik terlalu jauh ke depan",
                            "Membeli saham sebelum jam bursa",
                            "Menggunakan terlalu banyak saham",
                        ],
                        "answer": 0,
                        "why": "Look-ahead bias membuat simulasi memakai informasi masa depan, sehingga hasilnya tidak realistis.",
                    },
                    {
                        "q": "Apa yang sebaiknya dilakukan pada outlier harga yang ekstrem?",
                        "options": [
                            "Langsung hapus semua",
                            "Periksa penyebabnya sebelum memutuskan",
                            "Ganti dengan nol",
                            "Abaikan seluruh data saham",
                        ],
                        "answer": 1,
                        "why": "Outlier bisa merupakan peristiwa nyata seperti krisis atau kesalahan data. Periksa konteks sebelum menghapus.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m5",
        "number": 5,
        "title": "Membaca Laporan Keuangan",
        "icon": "🧾",
        "description": "Membaca pendapatan, laba, arus kas, utang, ekuitas, dan rasio penting tanpa terburu-buru.",
        "lessons": [
            {
                "id": "m5l1",
                "title": "Tiga laporan yang perlu dilihat",
                "minutes": 15,
                "goal": "Memahami hubungan laba, aset, utang, ekuitas, dan arus kas.",
                "sections": [
                    {
                        "heading": "Laba rugi: apakah usaha menghasilkan laba?",
                        "body": """
                            **Laporan laba rugi** menunjukkan pendapatan dan beban dalam suatu periode.

                            - **Pendapatan** adalah uang dari penjualan barang/jasa.
                            - **Beban pokok penjualan** adalah biaya langsung untuk menghasilkan produk.
                            - **Laba kotor** = pendapatan − beban pokok.
                            - **Laba operasi** = laba setelah beban operasional, sebelum bunga dan pajak.
                            - **Laba bersih** = laba setelah bunga, pajak, dan pos lain.

                            Laba bersih bisa positif meskipun arus kas sedang bermasalah. Karena itu, laba rugi harus dibaca bersama arus kas.
                        """,
                    },
                    {
                        "heading": "Neraca: apa yang dimiliki dan apa yang menjadi kewajiban?",
                        "body": """
                            **Neraca** menunjukkan posisi pada satu tanggal.

                            **Aset** = apa yang dimiliki perusahaan, misalnya kas, piutang, persediaan, tanah, dan bangunan. **Liabilitas** = kewajiban, misalnya utang bank dan utang dagang. **Ekuitas** = hak pemilik, yaitu selisih aset dikurangi liabilitas.

                            Rumus dasar: **Aset = Liabilitas + Ekuitas**.

                            Jika liabilitas jauh lebih besar daripada ekuitas, perusahaan lebih rentan ketika penjualan turun atau suku bunga naik. Ekuitas negatif adalah tanda bahaya yang perlu ditelusuri.
                        """,
                    },
                    {
                        "heading": "Arus kas: uang sungguhan yang bergerak",
                        "body": """
                            **Laporan arus kas** membagi arus kas menjadi tiga:

                            1. **Arus kas operasi**: uang dari kegiatan usaha sehari-hari.
                            2. **Arus kas investasi**: pembelian/penjualan aset dan investasi.
                            3. **Arus kas pendanaan**: utang, pembayaran utang, dividen, dan penerbitan saham.

                            Perusahaan bisa melaporkan laba tetapi arus kas operasinya negatif karena piutang menumpuk atau persediaan tidak terjual. Ini perlu perhatian. Sebaliknya, arus kas operasi yang konsisten positif biasanya lebih sehat, meskipun tetap perlu melihat konteks industri.
                        """,
                    },
                    {
                        "heading": "Membaca dengan urutan sederhana",
                        "body": """
                            Untuk pemula, mulai dengan empat pertanyaan:

                            1. Apakah pendapatan tumbuh, datar, atau turun?
                            2. Apakah laba bersih berasal dari operasi normal atau kejadian sekali?
                            3. Apakah arus kas operasi searah dengan laba?
                            4. Apakah utang bisa dilayani dan ekuitas tetap positif?

                            Jangan menyimpulkan dari satu tahun. Bandingkan beberapa tahun dan baca penjelasan manajemen. Satu rasio atau satu laporan tidak cukup untuk menilai perusahaan.
                        """,
                    },
                ],
                "analogy": """
                    Laporan keuangan seperti rekam medis usaha. Laba rugi adalah catatan pemasukan dan pengeluaran, neraca adalah foto kondisi tubuh saat ini, dan arus kas adalah aliran darah yang benar-benar bergerak. Dokter yang baik tidak hanya melihat satu angka.
                """,
                "example": """
                    **PT Bakso Nusantara (fiktif)** memiliki:

                    - Pendapatan Rp1.200.000.000
                    - Laba bersih Rp120.000.000
                    - Arus kas operasi Rp90.000.000
                    - Total aset Rp900.000.000
                    - Liabilitas Rp300.000.000
                    - Ekuitas Rp600.000.000

                    Laba bersih 10% dari pendapatan. Arus kas operasi positif, tetapi lebih kecil dari laba, mungkin karena sebagian penjualan belum dibayar pelanggan. Utang Rp300 juta dibanding ekuitas Rp600 juta berarti liabilitas 50% dari ekuitas. Tidak otomatis buruk, tetapi perlu dibandingkan dengan arus kas dan jatuh tempo utang.
                """,
                "application": """
                    Di halaman **Fundamental**, data laporan keuangan nyata belum tersedia. Kamu bisa berlatih dengan contoh fiktif di halaman itu, lalu membandingkan pemahamanmu dengan laporan resmi perusahaan di BEI.
                """,
                "python": """
                    ```python
                    pendapatan = 1_200_000_000
                    laba_bersih = 120_000_000
                    aset = 900_000_000
                    liabilitas = 300_000_000
                    ekuitas = aset - liabilitas

                    margin = laba_bersih / pendapatan
                    rasio_utang = liabilitas / ekuitas
                    print(f"Margin laba: {margin:.1%}, utang/ekuitas: {rasio_utang:.2f}x")
                    ```
                """,
                "mistakes": [
                    "Menganggap laba bersih selalu berarti uang tunai tersedia.",
                    "Melihat satu tahun laporan lalu menyimpulkan perusahaan hebat.",
                    "Mengabaikan utang dan jatuh temponya.",
                    "Menganggap pendapatan naik otomatis berarti laba naik.",
                ],
                "summary": [
                    "Laba rugi menunjukkan kinerja selama periode.",
                    "Neraca menunjukkan aset, liabilitas, dan ekuitas.",
                    "Arus kas menunjukkan pergerakan uang nyata.",
                    "Laba dan arus kas operasi perlu dibandingkan.",
                    "Baca beberapa periode dan konteks industri.",
                ],
                "quiz": [
                    {
                        "q": "Apa rumus dasar neraca?",
                        "options": [
                            "Aset = Liabilitas + Ekuitas",
                            "Laba = Pendapatan + Beban",
                            "Kas = Laba Bersih",
                            "Ekuitas = Aset + Liabilitas",
                        ],
                        "answer": 0,
                        "why": "Neraca seimbang: aset sama dengan total liabilitas ditambah ekuitas.",
                    },
                    {
                        "q": "Mengapa laba bersih positif belum tentu berarti kas perusahaan sehat?",
                        "options": [
                            "Karena laba selalu salah",
                            "Karena penjualan bisa belum dibayar dan piutang menumpuk",
                            "Karena kas tidak pernah masuk",
                            "Karena pajak tidak pernah dibayar",
                        ],
                        "answer": 1,
                        "why": "Laba akuntansi bisa berasal dari penjualan kredit. Arus kas operasi menunjukkan apakah uang benar-benar masuk.",
                    },
                    {
                        "q": "Apa arti ekuitas negatif?",
                        "options": [
                            "Perusahaan punya kas berlebih",
                            "Liabilitas melebihi aset, sehingga posisi keuangan perlu diwaspadai",
                            "Laba perusahaan pasti naik",
                            "Saham pasti dibagikan dividen",
                        ],
                        "answer": 1,
                        "why": "Ekuitas = aset − liabilitas. Jika negatif, kewajiban melebihi aset dan risiko keuangan meningkat.",
                    },
                ],
            },
            {
                "id": "m5l2",
                "title": "EPS, PER, PBV, ROE, dan dividen",
                "minutes": 16,
                "goal": "Menghitung rasio dasar dan memahami kapan rasio tersebut menyesatkan.",
                "sections": [
                    {
                        "heading": "Lima angka yang sering dipakai",
                        "body": """
                            **EPS (Earnings per Share)** = laba bersih ÷ jumlah saham beredar. EPS menunjukkan laba per lembar, bukan jumlah dividen.

                            **PER (Price to Earnings Ratio)** = harga saham ÷ EPS. PER 12,5 berarti kamu membayar Rp12,5 untuk setiap Rp1 laba tahunan. PER rendah bisa berarti murah, tetapi bisa juga berarti pasar meragukan masa depan perusahaan.

                            **PBV (Price to Book Value)** = harga saham ÷ nilai buku per saham. Nilai buku per saham = ekuitas ÷ jumlah saham. PBV 2 berarti harga pasar dua kali nilai buku.

                            **ROE (Return on Equity)** = laba bersih ÷ ekuitas. ROE 20% berarti setiap Rp100 ekuitas menghasilkan laba Rp20 pada periode itu.

                            **Dividend yield** = dividen per saham ÷ harga saham. **Payout ratio** = dividen ÷ laba bersih.
                        """,
                    },
                    {
                        "heading": "Contoh PT Bakso Nusantara",
                        "body": """
                            Data fiktif:

                            - Laba bersih Rp120.000.000
                            - Ekuitas Rp600.000.000
                            - Jumlah saham 1.000.000 lembar
                            - Harga saham Rp1.500
                            - Dividen dibagikan Rp30.000.000

                            | Rasio | Perhitungan | Hasil |
                            |---|---|---|
                            | EPS | Rp120 juta ÷ 1 juta lembar | Rp120 |
                            | PER | Rp1.500 ÷ Rp120 | 12,5× |
                            | Nilai buku per saham | Rp600 juta ÷ 1 juta | Rp600 |
                            | PBV | Rp1.500 ÷ Rp600 | 2,5× |
                            | ROE | Rp120 juta ÷ Rp600 juta | 20% |
                            | DPS | Rp30 juta ÷ 1 juta | Rp30 |
                            | Dividend yield | Rp30 ÷ Rp1.500 | 2% |
                            | Payout ratio | Rp30 juta ÷ Rp120 juta | 25% |

                            Angka-angka ini terlihat wajar, tetapi belum cukup untuk menyimpulkan saham layak dibeli. Kita belum tahu pertumbuhan, utang, arus kas, pesaing, dan risiko bisnis.
                        """,
                    },
                    {
                        "heading": "Jebakan rasio",
                        "body": """
                            - **PER rendah** bisa karena laba sekali besar atau pasar pesimis.
                            - **PER tinggi** bisa karena ekspektasi pertumbuhan tinggi, tetapi juga bisa karena harga terlalu mahal.
                            - **PBV rendah** bisa berarti murah, tetapi aset bisa berupa goodwill yang nilainya tidak nyata.
                            - **ROE tinggi** bisa berasal dari utang besar, bukan efisiensi.
                            - **Dividend yield tinggi** bisa terjadi karena harga saham jatuh, bukan karena dividen naik.
                            - Rasio bank dan perusahaan teknologi sulit dibandingkan langsung.

                            Bandingkan dengan perusahaan sejenis, lihat tren beberapa tahun, dan baca laporan aslinya.
                        """,
                    },
                    {
                        "heading": "Cara bertanya yang lebih baik",
                        "body": """
                            Daripada bertanya "PER berapa yang bagus?", tanyakan:

                            - Apakah laba tumbuh dan berasal dari operasi normal?
                            - Apakah arus kas mendukung laba?
                            - Berapa utang dan biaya bunganya?
                            - Apakah bisnisnya punya keunggulan yang bertahan?
                            - Berapa harga yang masuk akal jika laba tidak tumbuh?

                            Rasio adalah alat menyaring, bukan mesin penjawab.
                        """,
                    },
                ],
                "analogy": """
                    Rasio keuangan seperti indeks pada kemasan makanan. Angka kalori dan gula membantu membandingkan, tetapi kamu tetap perlu tahu porsinya, bahan, dan kebutuhanmu. Sepotong kue rendah gula belum tentu makanan sehat.
                """,
                "example": """
                    Saham A punya PER 8 dan ROE 25%. Terlihat menarik. Setelah dicek, ROE tinggi karena utang sangat besar dan laba tahun ini berasal dari penjualan tanah. Arus kas operasi negatif.

                    Saham B punya PER 18 dan ROE 15%. Lebih mahal, tetapi laba tumbuh stabil dan arus kas operasi positif. Tanpa melihat kualitas laba dan utang, kamu bisa memilih A karena angkanya terlihat lebih murah.
                """,
                "application": """
                    Saat membaca screener, jangan mengurutkan hanya berdasarkan PER terendah. Tambahkan kolom ROE, pertumbuhan laba, arus kas, dan utang. Untuk latihan, hitung rasio PT Bakso Nusantara di halaman Fundamental.
                """,
                "python": """
                    ```python
                    laba = 120_000_000
                    ekuitas = 600_000_000
                    saham = 1_000_000
                    harga = 1_500
                    dividen = 30_000_000

                    eps = laba / saham
                    per = harga / eps
                    pbv = harga / (ekuitas / saham)
                    roe = laba / ekuitas
                    yield_ = (dividen / saham) / harga
                    print(eps, per, pbv, roe, yield_)
                    ```
                """,
                "mistakes": [
                    "Membeli hanya karena PER terendah.",
                    "Menganggap ROE tinggi selalu karena manajemen hebat.",
                    "Menyimpulkan dari satu rasio tanpa melihat utang dan arus kas.",
                    "Menganggap dividend yield tinggi pasti aman.",
                ],
                "summary": [
                    "EPS, PER, PBV, ROE, dan dividend yield saling melengkapi.",
                    "Rasio harus dibandingkan dengan sektor dan periode yang sama.",
                    "Laba sekali dan utang bisa membuat rasio terlihat bagus.",
                    "Dividend yield tinggi bisa berasal dari harga yang jatuh.",
                    "Rasio adalah alat bantu, bukan jawaban tunggal.",
                ],
                "quiz": [
                    {
                        "q": "Laba bersih Rp120 juta, jumlah saham 1 juta lembar. Berapa EPS?",
                        "options": ["Rp12", "Rp120", "Rp1.200", "Rp120 juta"],
                        "answer": 1,
                        "why": "EPS = laba bersih ÷ jumlah saham = Rp120.000.000 ÷ 1.000.000 = Rp120.",
                    },
                    {
                        "q": "Harga saham Rp1.500 dan EPS Rp120. Berapa PER?",
                        "options": ["8,0×", "12,5×", "18,0×", "1.500×"],
                        "answer": 1,
                        "why": "PER = harga ÷ EPS = Rp1.500 ÷ Rp120 = 12,5 kali.",
                    },
                    {
                        "q": "Mengapa ROE tinggi belum tentu bagus?",
                        "options": [
                            "Karena ROE tidak pernah dihitung dari laba",
                            "Karena bisa berasal dari utang yang besar sehingga risiko meningkat",
                            "Karena ROE hanya berlaku untuk bank",
                            "Karena ROE selalu negatif",
                        ],
                        "answer": 1,
                        "why": "ROE = laba ÷ ekuitas. Ekuitas kecil karena banyak utang bisa membuat ROE terlihat tinggi meskipun risiko keuangan besar.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m6",
        "number": 6,
        "title": "Analisis Saham dengan Python",
        "icon": "🐍",
        "description": "Dari membaca CSV sampai menghitung return, risiko, dan membandingkan dengan IHSG.",
        "lessons": [
            {
                "id": "m6l1",
                "title": "Membaca dan membersihkan data dengan Pandas",
                "minutes": 15,
                "goal": "Memeriksa bentuk, tipe, missing, duplikat, dan tanggal sebelum menghitung apa pun.",
                "sections": [
                    {
                        "heading": "Langkah pertama: kenali data",
                        "body": """
                            Sebelum menghitung return, pastikan kamu tahu isi datanya:

                            ```python
                            import pandas as pd

                            df = pd.read_csv("data/processed/historical_prices.csv")
                            print(df.shape)
                            print(df.head())
                            print(df.dtypes)
                            print(df.isna().sum())
                            print(df.duplicated(subset=["date", "ticker"]).sum())
                            ```

                            `shape` memberi jumlah baris dan kolom. `head()` melihat contoh isi. `dtypes` menunjukkan tipe data. `isna().sum()` menghitung nilai hilang. Duplikat dicek berdasarkan kombinasi tanggal dan ticker, bukan seluruh baris.
                        """,
                    },
                    {
                        "heading": "Perbaiki tipe data",
                        "body": """
                            Tanggal harus bertipe datetime, bukan teks. Harga dan volume harus angka. Jika tidak, operasi seperti `pct_change()` atau `groupby()` bisa gagal atau menghasilkan urutan yang salah.

                            ```python
                            df["date"] = pd.to_datetime(df["date"], errors="coerce")
                            kolom_angka = ["open", "high", "low", "close", "adj_close", "volume"]
                            for kolom in kolom_angka:
                                df[kolom] = pd.to_numeric(df[kolom], errors="coerce")
                            df = df.dropna(subset=["date", "ticker", "adj_close"])
                            df = df.drop_duplicates(subset=["date", "ticker"], keep="last")
                            df = df.sort_values(["ticker", "date"])
                            ```

                            Gunakan `errors="coerce"` agar nilai aneh menjadi NaN dan bisa diperiksa, bukan langsung membuat program berhenti.
                        """,
                    },
                    {
                        "heading": "Validasi logika harga",
                        "body": """
                            Periksa apakah harga masuk akal: harga penutupan positif, `high` tidak lebih rendah dari `low`, dan volume tidak negatif. Jangan otomatis menghapus semua baris yang mencurigakan; tandai dulu untuk diperiksa.

                            Pada data historis proyek ini, validasi dilakukan di `src/data_cleaning.py` dan ringkasannya ditampilkan di halaman Data Overview.
                        """,
                    },
                    {
                        "heading": "Jangan mengisi data secara asal",
                        "body": """
                            `ffill()` dapat membuat grafik terlihat mulus, tetapi juga menyembunyikan kenyataan bahwa saham tidak diperdagangkan. Untuk return, gunakan harga yang benar-benar ada dan biarkan NaN. Untuk analisis korelasi, gunakan pasangan tanggal yang tersedia.

                            Jika kamu mengisi harga berhari-hari ke depan, kamu bisa menciptakan return nol palsu dan menurunkan volatilitas secara tidak wajar.
                        """,
                    },
                ],
                "analogy": """
                    Membersihkan data seperti mencuci sayur sebelum memasak. Kamu membuang kotoran, tetapi tidak memotong semua bagian yang bentuknya aneh tanpa memeriksa apakah itu bagian yang penting. Data krisis yang ekstrem justru bisa menjadi pelajaran berharga.
                """,
                "example": """
                    File memiliki 1.000 baris, 3 tanggal duplikat, dan 40 harga `adj_close` kosong. Jika langsung dihitung, return bisa error atau menghasilkan angka aneh.

                    Setelah tanggal diubah ke datetime, duplikat dihapus, dan baris tanpa harga dibuang, tersisa 995 baris. Perubahannya dicatat di laporan kualitas data, bukan disembunyikan.
                """,
                "application": """
                    Notebook `01_data_understanding.ipynb` dan `02_data_cleaning.ipynb` menjalankan langkah ini pada data proyek. Bandingkan output notebook dengan halaman Data Overview.
                """,
                "python": """
                    ```python
                    df = df.sort_values(["ticker", "date"])
                    df["return"] = df.groupby("ticker")["adj_close"].pct_change()
                    print(df.groupby("ticker")["return"].describe())
                    ```
                """,
                "mistakes": [
                    "Membaca tanggal sebagai teks lalu mengurutkannya secara alfabet.",
                    "Menghapus semua baris dengan nilai hilang tanpa memeriksa polanya.",
                    "Mengisi harga saham berhari-hari dengan forward-fill.",
                    "Menghitung return dari harga mentah yang belum disesuaikan.",
                ],
                "summary": [
                    "Kenali bentuk, tipe, missing, dan duplikat sebelum analisis.",
                    "Ubah tanggal dan angka ke tipe yang benar.",
                    "Validasi harga dan volume secara logis.",
                    "Jangan mengisi atau menghapus data secara sembarangan.",
                    "Simpan data mentah dan hasil olahan secara terpisah.",
                ],
                "quiz": [
                    {
                        "q": "Apa fungsi `df.shape`?",
                        "options": [
                            "Menampilkan jumlah baris dan kolom",
                            "Menghapus duplikat",
                            "Mengubah tanggal menjadi angka",
                            "Menghitung return",
                        ],
                        "answer": 0,
                        "why": "`shape` mengembalikan tuple (jumlah baris, jumlah kolom).",
                    },
                    {
                        "q": "Mengapa tanggal perlu diubah dengan `pd.to_datetime`?",
                        "options": [
                            "Agar bisa diurutkan dan diolah sebagai waktu dengan benar",
                            "Agar harga saham naik",
                            "Agar file lebih kecil",
                            "Agar tidak ada missing value",
                        ],
                        "answer": 0,
                        "why": "Tipe datetime memungkinkan pengurutan, pemotongan periode, dan perhitungan selisih waktu yang benar.",
                    },
                    {
                        "q": "Apa risiko mengisi harga yang hilang dengan forward-fill tanpa batas?",
                        "options": [
                            "Membuat data terlihat lebih lengkap daripada kenyataan dan return menjadi palsu",
                            "Membuat harga selalu turun",
                            "Menghapus semua dividen",
                            "Mengubah lot menjadi 1.000",
                        ],
                        "answer": 0,
                        "why": "Forward-fill panjang menciptakan harga datar palsu, return nol, dan volatilitas yang terlalu rendah.",
                    },
                ],
            },
            {
                "id": "m6l2",
                "title": "Return, volatilitas, drawdown, dan benchmark",
                "minutes": 17,
                "goal": "Menghitung metrik inti dan menafsirkannya dengan jujur.",
                "sections": [
                    {
                        "heading": "Return harian dan cumulative return",
                        "body": """
                            **Return harian** = (harga hari ini ÷ harga kemarin) − 1.

                            **Cumulative return** = (harga akhir ÷ harga awal) − 1. Ini menunjukkan total perubahan selama periode, bukan rata-rata per tahun.

                            Contoh: Rp1.000 menjadi Rp1.200 dalam 2 tahun. Cumulative return = 20%. Tetapi CAGR (pertumbuhan tahunan majemuk) = (1.200 ÷ 1.000)^(1/2) − 1 = 9,54% per tahun, bukan 10% karena efek majemuk.
                        """,
                    },
                    {
                        "heading": "CAGR dan moving average",
                        "body": """
                            **CAGR** = (harga akhir ÷ harga awal)^(1 ÷ jumlah tahun) − 1. CAGR berguna untuk membandingkan periode berbeda, tetapi tetap berdasarkan titik awal dan akhir; perjalanan di tengah tidak terlihat.

                            **Moving average (MA)** adalah rata-rata harga selama beberapa hari terakhir. MA 20 memakai 20 hari; MA 200 memakai 200 hari. MA membantu melihat arah tren, tetapi selalu tertinggal dari harga karena memakai data masa lalu. Jangan menganggap MA sebagai ramalan pasti.
                        """,
                    },
                    {
                        "heading": "Volatilitas dan drawdown",
                        "body": """
                            **Volatilitas tahunan** = simpangan baku return harian × √252. Angka ini menggambarkan seberapa besar naik-turun return, bukan batas kerugian.

                            **Drawdown** = harga ÷ puncak tertinggi sebelumnya − 1. **Maximum drawdown** adalah nilai terendah drawdown. Jika saham turun 40% dari puncak, dibutuhkan kenaikan 66,7% untuk kembali.

                            Kedua metrik ini dihitung di `src/risk_analysis.py` dan ditampilkan di halaman Analisis Risiko.
                        """,
                    },
                    {
                        "heading": "Membandingkan dengan IHSG",
                        "body": """
                            Benchmark membuat penilaian lebih adil. Jika sahammu naik 10% tetapi IHSG naik 20% pada periode yang sama, sahammu tertinggal dari pasar.

                            Syarat perbandingan: periode sama, harga adjusted, dan mata uang sama. Untuk beberapa saham, gunakan tanggal awal yang sama. Jangan membandingkan return 3 tahun saham dengan IHSG 1 tahun.

                            **Return relatif** = return saham − return benchmark. Ini bukan jaminan masa depan, hanya konteks historis.
                        """,
                    },
                ],
                "analogy": """
                    Return seperti jarak yang ditempuh, CAGR seperti kecepatan rata-rata tahunan, volatilitas seperti seberapa sering arah berubah, dan drawdown seperti seberapa dalam kamu pernah jatuh ke lubang. Semuanya diperlukan untuk menggambarkan perjalanan, bukan hanya garis finis.
                """,
                "example": """
                    Harga awal Rp1.000, harga akhir Rp1.500 setelah 3 tahun.

                    - Cumulative return = 50%
                    - CAGR = (1.500 ÷ 1.000)^(1/3) − 1 = 14,47% per tahun
                    - Jika selama periode pernah turun ke Rp700 dari puncak Rp1.600, drawdown = (700 ÷ 1.600) − 1 = −56,25%
                    - Volatilitas tahunan 30% berarti naik-turun harian cukup besar, bukan berarti pasti rugi 30%.

                    Saham dengan return 50% tetapi drawdown 56% terasa jauh lebih menegangkan daripada angka return-nya.
                """,
                "application": """
                    Di halaman **Performa Saham**, pilih beberapa saham dan IHSG, lalu bandingkan grafik ternormalisasi dan tabel metrik. Di halaman **Risiko**, lihat drawdown dan distribusi return.
                """,
                "python": """
                    ```python
                    import numpy as np

                    harga = df.set_index("date")["adj_close"]
                    ret = harga.pct_change().dropna()
                    cumulative = harga.iloc[-1] / harga.iloc[0] - 1
                    vol = ret.std() * np.sqrt(252)
                    drawdown = (harga / harga.cummax() - 1).min()
                    print(cumulative, vol, drawdown)
                    ```
                """,
                "mistakes": [
                    "Membandingkan return periode berbeda.",
                    "Menganggap CAGR sama dengan rata-rata return tahunan sederhana.",
                    "Menganggap volatilitas tinggi berarti pasti bangkrut.",
                    "Menggunakan moving average sebagai jaminan beli/jual.",
                    "Tidak memasukkan biaya transaksi dalam evaluasi strategi.",
                ],
                "summary": [
                    "Return harian mengukur perubahan satu hari; cumulative return mengukur total periode.",
                    "CAGR mempertimbangkan efek majemuk.",
                    "Volatilitas mengukur naik-turun; drawdown mengukur penurunan dari puncak.",
                    "Bandingkan dengan benchmark pada periode yang sama.",
                    "Metrik historis tidak menjamin hasil masa depan.",
                ],
                "quiz": [
                    {
                        "q": "Harga naik dari Rp1.000 ke Rp1.210 dalam 2 tahun. Berapa CAGR?",
                        "options": ["10%", "21%", "9,54%", "5%"],
                        "answer": 0,
                        "why": "(1.210/1.000)^(1/2) − 1 = 0,10 atau 10% per tahun. Cumulative return 21% dibagi dua tahun bukan CAGR.",
                    },
                    {
                        "q": "Apa arti maximum drawdown −40%?",
                        "options": [
                            "Harga pernah turun 40% dari puncak sebelumnya",
                            "Harga pasti turun 40% tahun depan",
                            "Volatilitas harian 40%",
                            "Dividen turun 40%",
                        ],
                        "answer": 0,
                        "why": "Drawdown dihitung dari puncak ke lembah. −40% berarti penurunan terburuk sebesar 40% dari titik puncak pada periode itu.",
                    },
                    {
                        "q": "Mengapa perbandingan dengan IHSG harus memakai periode yang sama?",
                        "options": [
                            "Agar kesimpulan performa relatif adil",
                            "Agar harga saham otomatis naik",
                            "Karena IHSG tidak punya tanggal",
                            "Karena periode tidak memengaruhi return",
                        ],
                        "answer": 0,
                        "why": "Periode berbeda membuat perbandingan tidak setara; kondisi pasar bisa sangat berbeda.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m7",
        "number": 7,
        "title": "Simulasi dan Paper Trading",
        "icon": "📝",
        "description": "Menguji keputusan tanpa mempertaruhkan uang asli dan mencatat alasannya.",
        "lessons": [
            {
                "id": "m7l1",
                "title": "Membuat jurnal dan transaksi virtual",
                "minutes": 13,
                "goal": "Membangun kebiasaan mencatat transaksi, alasan, biaya, dan evaluasi.",
                "sections": [
                    {
                        "heading": "Paper trading itu apa?",
                        "body": """
                            **Paper trading** adalah mencatat keputusan beli/jual secara virtual tanpa mengirim order ke broker. Tujuannya melatih proses, bukan mencetak uang.

                            Bedakan dengan jelas:

                            - **Transaksi virtual**: dibuat di aplikasi ini, tidak memengaruhi rekening nyata.
                            - **Transaksi riil**: dilakukan melalui sekuritas berizin dan uang sungguhan.

                            Aplikasi ini **tidak terhubung ke broker** dan tidak bisa mengirim order. Jangan menganggap catatan virtual sebagai bukti kemampuan menghasilkan uang.
                        """,
                    },
                    {
                        "heading": "Isi jurnal yang berguna",
                        "body": """
                            Catat minimal:

                            - tanggal dan kode saham;
                            - aksi beli atau jual;
                            - harga simulasi dan jumlah lot;
                            - perkiraan biaya;
                            - **alasan** keputusan;
                            - kondisi saat itu (berita, laporan, sentimen);
                            - rencana keluar: kapan evaluasi, apa yang membuat tesis berubah;
                            - catatan evaluasi setelah beberapa waktu.

                            Alasan harus spesifik. "Kata teman" bukan alasan yang bisa dievaluasi. "Saya membeli karena arus kas operasi tumbuh dan utang turun, lalu akan mengecek laporan kuartal berikutnya" jauh lebih berguna.
                        """,
                    },
                    {
                        "heading": "Mengapa mencatat alasan penting?",
                        "body": """
                            Tanpa catatan, otak cenderung mengingat keputusan yang benar dan melupakan yang salah. Kamu bisa mengklaim "sudah tahu" setelah harga naik, padahal sebelumnya ragu.

                            Jurnal membuat proses terlihat. Kamu bisa menilai apakah keputusan diambil karena analisis, emosi, atau kebetulan. Ini yang membedakan belajar dari sekadar menebak.
                        """,
                    },
                    {
                        "heading": "Biaya dan dividen dalam simulasi",
                        "body": """
                            Sertakan komisi beli, komisi jual, dan pajak jual. Jika saham membagikan dividen, catat dividen sebagai arus kas terpisah dan pahami bahwa pajak dividen bisa berlaku.

                            Untuk perbandingan yang adil, hitung hasil portofolio setelah biaya dan bandingkan dengan IHSG pada periode yang sama. Jangan hanya melihat saham yang naik.
                        """,
                    },
                ],
                "analogy": """
                    Jurnal investasi seperti buku latihan penerbangan di simulator. Pilot pemula tidak langsung membawa penumpang; ia berlatih, mencatat kesalahan, dan mengulang. Simulator tidak membuatnya ahli secara otomatis, tetapi mempercepat pembelajaran jika ia jujur mencatat.
                """,
                "example": """
                    Contoh catatan (fiktif, bukan rekomendasi):

                    | Tanggal | Saham | Aksi | Harga | Lot | Alasan | Evaluasi |
                    |---|---|---|---|---|---|---|
                    | 10 Jan | BBCA | Beli | Rp9.000 | 1 | Ingin belajar memiliki bank besar; dana cadangan sudah dipisah | Akan review setelah laporan kuartal |
                    | 10 Apr | BBCA | Jual | Rp9.500 | 1 | Butuh uang untuk kursus; bukan karena analisis berubah | Proses keluar sesuai kebutuhan, bukan panik |

                    Perhatikan bahwa jual bukan selalu berarti perusahaan buruk. Bisa jadi kebutuhan pribadi berubah.
                """,
                "application": """
                    Buka halaman **Paper Trading**, tambahkan transaksi virtual, lalu isi alasan dan catatan evaluasi. Mulai dengan modal virtual Rp700.000 dan jangan mengubah aturan di tengah jalan hanya agar hasil terlihat bagus.
                """,
                "python": """
                    ```python
                    transaksi = {
                        "tanggal": "2026-01-10",
                        "saham": "BBCA",
                        "aksi": "BELI",
                        "harga": 9000,
                        "lot": 1,
                        "alasan": "Latihan diversifikasi dengan dana cadangan terpisah",
                    }
                    nilai = transaksi["harga"] * transaksi["lot"] * 100
                    print(transaksi, nilai)
                    ```
                """,
                "mistakes": [
                    "Mencatat transaksi tanpa alasan sehingga tidak bisa dievaluasi.",
                    "Menganggap paper trading sama dengan pengalaman pasar nyata.",
                    "Mengubah aturan simulasi setelah melihat hasil.",
                    "Lupa memasukkan biaya dan dividen.",
                ],
                "summary": [
                    "Paper trading melatih proses tanpa uang asli.",
                    "Jurnal harus memuat alasan dan rencana evaluasi.",
                    "Bedakan transaksi virtual dari transaksi riil.",
                    "Biaya dan dividen memengaruhi hasil bersih.",
                    "Aplikasi ini tidak terhubung ke broker.",
                ],
                "quiz": [
                    {
                        "q": "Apa perbedaan utama paper trading dengan transaksi riil?",
                        "options": [
                            "Paper trading tidak memakai uang atau order nyata",
                            "Paper trading dijamin untung",
                            "Transaksi riil tidak punya biaya",
                            "Paper trading hanya untuk bank",
                        ],
                        "answer": 0,
                        "why": "Paper trading adalah simulasi pencatatan. Tidak ada order yang dikirim ke broker dan tidak ada uang nyata yang berpindah.",
                    },
                    {
                        "q": "Mengapa alasan transaksi perlu dicatat?",
                        "options": [
                            "Agar bisa mengevaluasi proses dan mengenali keputusan emosional",
                            "Agar harga saham naik",
                            "Agar biaya transaksi hilang",
                            "Agar tidak perlu membaca laporan",
                        ],
                        "answer": 0,
                        "why": "Alasan membuat keputusan bisa dinilai ulang. Tanpa itu, kamu hanya menilai hasil dan mudah terkena bias.",
                    },
                    {
                        "q": "Apakah aplikasi ini mengirim order ke broker?",
                        "options": [
                            "Ya, secara otomatis",
                            "Tidak, semua transaksi hanya dicatat lokal",
                            "Ya, jika modal lebih dari Rp700.000",
                            "Hanya pada hari bursa",
                        ],
                        "answer": 1,
                        "why": "Aplikasi ini alat belajar. Tidak ada koneksi broker atau pengiriman order nyata.",
                    },
                ],
            },
            {
                "id": "m7l2",
                "title": "Mengevaluasi strategi tanpa menipu diri",
                "minutes": 14,
                "goal": "Mengenali bias, biaya, dan arti hasil simulasi yang jujur.",
                "sections": [
                    {
                        "heading": "Proses vs hasil",
                        "body": """
                            Keputusan bisa benar secara proses tetapi rugi karena faktor acak. Sebaliknya, keputusan sembarangan bisa untung karena keberuntungan.

                            Evaluasi yang sehat bertanya:

                            - Apakah analisisnya memadai?
                            - Apakah risiko sudah dibatasi?
                            - Apakah keputusan sesuai rencana?
                            - Apakah hasilnya dibandingkan dengan benchmark?
                            - Apakah ada informasi yang seharusnya dicek?

                            Jangan hanya memberi nilai "hebat" pada hasil untung.
                        """,
                    },
                    {
                        "heading": "Bias yang sering muncul",
                        "body": """
                            - **Look-ahead bias**: memakai informasi yang belum ada pada saat keputusan.
                            - **Survivorship bias**: hanya menguji saham yang masih ada sekarang.
                            - **Overfitting**: mengatur strategi terlalu pas dengan data lama sehingga gagal di data baru.
                            - **Hindsight bias**: merasa "sudah tahu" setelah melihat hasil.
                            - **Confirmation bias**: hanya mencari berita yang mendukung keyakinan.

                            Cara mengurangi: tentukan aturan sebelum melihat hasil, uji pada periode berbeda, catat semua keputusan, dan sertakan biaya.
                        """,
                    },
                    {
                        "heading": "Biaya, slippage, dan likuiditas",
                        "body": """
                            Backtest sering terlihat bagus karena menganggap transaksi selalu terjadi tepat di harga penutupan. Di dunia nyata, order bisa sebagian terisi, harga bergerak (slippage), dan spread membuat hasil berbeda.

                            Saham tidak likuid bisa lebih parah: saat ingin menjual, pembeli sedikit sehingga harga turun. Model sederhana tidak menangkap ini. Karena itu, hasil simulasi harus dianggap perkiraan kasar, bukan janji.
                        """,
                    },
                    {
                        "heading": "Membandingkan dengan benchmark",
                        "body": """
                            Jika strategimu menghasilkan 8% setahun sementara IHSG 12% pada periode yang sama, strategimu tertinggal meskipun nominalnya positif. Bandingkan juga risiko: hasil 8% dengan drawdown 40% mungkin tidak lebih baik daripada 8% dengan drawdown 15%.

                            Gunakan periode yang sama, biaya yang realistis, dan jelaskan asumsi. Jangan menyembunyikan periode buruk.
                        """,
                    },
                ],
                "analogy": """
                    Menilai strategi seperti menilai resep, bukan satu kali masakan. Satu kali masakan bisa kebetulan enak. Resep yang baik harus diuji berkali-kali, dengan bahan yang wajar, dan dicatat jika ada bahan yang mahal atau langka.
                """,
                "example": """
                    Strategi A membeli saham setelah naik 10% dan menjual setelah turun 5%. Pada data 2020–2023 terlihat untung. Tetapi biaya transaksi 1% per transaksi dan slippage 0,5% belum dihitung. Setelah dimasukkan, hasilnya negatif.

                    Strategi B tidak spektakuler, hanya membeli beberapa saham besar dan menahan lama. Return-nya mirip IHSG, tetapi drawdown lebih bisa ditahan. Untuk pemula, proses yang sederhana dan biaya rendah sering lebih realistis.
                """,
                "application": """
                    Di halaman Paper Trading, lihat ringkasan setelah biaya. Bandingkan hasil portofolio virtual dengan IHSG pada periode yang sama, lalu tulis evaluasi proses, bukan hanya angka untung.
                """,
                "python": """
                    ```python
                    return_strategi = 0.08
                    return_benchmark = 0.12
                    selisih = return_strategi - return_benchmark
                    print(f"Return relatif: {selisih:.2%}")
                    ```
                """,
                "mistakes": [
                    "Menguji strategi pada periode yang sama terus-menerus sampai terlihat bagus.",
                    "Mengabaikan saham yang delisting.",
                    "Menganggap satu kali untung sebagai bukti keahlian.",
                    "Membandingkan hasil dengan benchmark periode berbeda.",
                ],
                "summary": [
                    "Nilai proses, bukan hanya hasil.",
                    "Waspadai look-ahead, survivorship, overfitting, dan hindsight bias.",
                    "Sertakan biaya, slippage, dan likuiditas.",
                    "Bandingkan dengan benchmark pada periode yang sama.",
                    "Simulasi historis bukan jaminan masa depan.",
                ],
                "quiz": [
                    {
                        "q": "Apa itu overfitting?",
                        "options": [
                            "Strategi terlalu disesuaikan dengan data lama sehingga gagal pada data baru",
                            "Membeli terlalu banyak saham",
                            "Menggunakan biaya transaksi",
                            "Membandingkan dengan IHSG",
                        ],
                        "answer": 0,
                        "why": "Overfitting terjadi ketika aturan terlalu pas dengan kebetulan data historis dan tidak bertahan pada kondisi baru.",
                    },
                    {
                        "q": "Mengapa biaya dan slippage penting dalam simulasi?",
                        "options": [
                            "Karena keduanya mengurangi hasil nyata",
                            "Karena membuat harga saham selalu naik",
                            "Karena hanya berlaku untuk broker asing",
                            "Karena tidak memengaruhi return",
                        ],
                        "answer": 0,
                        "why": "Komisi, pajak, spread, dan slippage adalah pengurangan nyata dari hasil. Tanpa itu, simulasi terlalu optimistis.",
                    },
                    {
                        "q": "Strategi naik 8%, IHSG naik 12%. Apa kesimpulan yang tepat?",
                        "options": [
                            "Strategi tertinggal dari benchmark pada periode itu",
                            "Strategi pasti lebih baik karena untung",
                            "IHSG pasti turun besok",
                            "Strategi tidak punya risiko",
                        ],
                        "answer": 0,
                        "why": "Secara relatif, 8% lebih rendah dari 12% pada periode yang sama. Ini belum cukup untuk menilai masa depan.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m8",
        "number": 8,
        "title": "Persiapan Pembelian Saham Pertama",
        "icon": "🚦",
        "description": "Memilih sekuritas resmi, memahami order, dan menghindari jebakan pemula.",
        "lessons": [
            {
                "id": "m8l1",
                "title": "Memilih sekuritas yang resmi dan aman",
                "minutes": 13,
                "goal": "Memeriksa izin, biaya, dan keamanan sebelum membuka rekening saham.",
                "sections": [
                    {
                        "heading": "Mulai dari izin, bukan dari promo",
                        "body": """
                            Sebelum membuka rekening, pastikan perusahaan sekuritas adalah pihak yang berizin dan diawasi **OJK**, serta menjadi anggota bursa. Periksa informasi di situs resmi OJK dan BEI, bukan hanya dari iklan atau tautan yang dikirim orang.

                            Waspadai tawaran:

                            - keuntungan pasti atau risiko nol;
                            - titip dana ke rekening pribadi;
                            - robot trading dengan hasil tetap;
                            - permintaan password, PIN, atau OTP;
                            - ajakan mengejar bonus dengan setoran besar.

                            Rekening efek yang benar dibuka melalui proses resmi dengan verifikasi identitas (KYC). Jangan menyerahkan kendali akun kepada orang lain.
                        """,
                    },
                    {
                        "heading": "Bandingkan biaya secara total",
                        "body": """
                            Biaya tidak hanya komisi beli. Tanyakan:

                            - komisi beli dan jual;
                            - pajak penjualan;
                            - biaya administrasi bulanan (jika ada);
                            - biaya penarikan dana;
                            - biaya transfer saham;
                            - biaya layanan tambahan.

                            Broker dengan komisi sangat rendah bisa memiliki fitur atau layanan berbeda. Broker dengan aplikasi nyaman bisa lebih mahal. Tidak ada pilihan yang terbaik untuk semua orang; sesuaikan dengan kebutuhan dan pastikan tidak ada biaya tersembunyi.
                        """,
                    },
                    {
                        "heading": "Jangan terburu-buru membuka rekening",
                        "body": """
                            Memiliki rekening saham bukan perlombaan. Kamu bisa terus belajar dengan data historis, simulasi, dan paper trading sebelum menyetor uang.

                            Saat sudah siap, mulai dengan nominal kecil yang benar-benar siap kehilangan. Pahami cara setor, menarik dana, membaca portofolio, dan menghubungi layanan pelanggan jika ada masalah.
                        """,
                    },
                ],
                "analogy": """
                    Memilih sekuritas seperti memilih tempat menyimpan barang berharga. Kamu tidak hanya melihat promonya, tetapi memeriksa izin, reputasi, prosedur, dan biaya. Kunci tetap di tanganmu; jangan memberikannya kepada orang yang menjanjikan keajaiban.
                """,
                "example": """
                    Dua sekuritas menawarkan komisi beli 0,10% dan 0,18%. Yang lebih murah ternyata mengenakan biaya administrasi bulanan dan biaya penarikan. Setelah dihitung, total biaya untuk pola transaksi kecil bisa berbeda.

                    Contoh sederhana: transaksi Rp200.000. Komisi 0,10% = Rp200; komisi 0,18% = Rp360. Selisih Rp160 per transaksi. Untuk transaksi jarang, selisih ini kecil; untuk transaksi sering, bisa menumpuk. Namun kenyamanan dan keamanan tetap penting.
                """,
                "application": """
                    Buat daftar pertanyaan sebelum memilih: apakah berizin, berapa biaya total, bagaimana cara menarik dana, apakah layanan pelanggan responsif, dan apakah aplikasi memiliki edukasi risiko. Jangan memilih hanya karena bonus pendaftaran.
                """,
                "python": """
                    ```python
                    nilai = 200_000
                    for komisi in (0.0010, 0.0018):
                        print(f"Komisi {komisi:.2%}: Rp{nilai * komisi:,.0f}")
                    ```
                """,
                "mistakes": [
                    "Memilih sekuritas hanya karena bonus atau iklan.",
                    "Menyerahkan OTP atau password kepada pihak lain.",
                    "Tidak memeriksa izin di OJK/BEI.",
                    "Menyetor seluruh modal sebelum memahami cara kerja rekening.",
                ],
                "summary": [
                    "Pilih sekuritas berizin OJK dan anggota bursa.",
                    "Bandingkan biaya total, bukan hanya komisi beli.",
                    "Jangan pernah memberikan OTP atau kendali akun.",
                    "Tidak perlu buru-buru membuka rekening.",
                    "Mulai kecil setelah proses dan risikonya dipahami.",
                ],
                "quiz": [
                    {
                        "q": "Di mana sebaiknya memeriksa izin sekuritas?",
                        "options": [
                            "Sumber resmi OJK dan BEI",
                            "Komentar media sosial",
                            "Iklan di aplikasi pesan",
                            "Grup chat yang menjanjikan untung",
                        ],
                        "answer": 0,
                        "why": "Otoritas dan bursa memiliki informasi resmi tentang pihak yang berizin. Verifikasi di sana.",
                    },
                    {
                        "q": "Mengapa komisi terendah belum tentu biaya total terendah?",
                        "options": [
                            "Karena bisa ada biaya administrasi, penarikan, dan layanan lain",
                            "Karena komisi tidak pernah dihitung",
                            "Karena semua broker sama",
                            "Karena pajak hanya berlaku untuk broker mahal",
                        ],
                        "answer": 0,
                        "why": "Biaya total mencakup komisi, pajak, administrasi, dan biaya lainnya. Pola transaksi juga memengaruhi total.",
                    },
                    {
                        "q": "Apa yang harus dilakukan jika seseorang meminta OTP rekening saham?",
                        "options": [
                            "Memberikannya agar cepat diproses",
                            "Menolak dan tidak membagikannya kepada siapa pun",
                            "Mengirim hanya sebagian",
                            "Menyimpannya di grup chat",
                        ],
                        "answer": 1,
                        "why": "OTP adalah kunci keamanan. Tidak ada pihak resmi yang boleh memintanya. Jangan pernah membagikannya.",
                    },
                ],
            },
            {
                "id": "m8l2",
                "title": "Order, likuiditas, FOMO, dan manipulasi",
                "minutes": 14,
                "goal": "Memahami cara order bekerja secara konsep dan menghindari keputusan karena tekanan sosial.",
                "sections": [
                    {
                        "heading": "Order beli dan jual",
                        "body": """
                            Saat mengirim order, kamu bisa memilih harga dan jumlah. Dua jenis yang perlu dipahami:

                            - **Order pasar (market)**: meminta transaksi segera pada harga terbaik yang tersedia. Cepat, tetapi harga akhir bisa berbeda dari yang kamu lihat.
                            - **Order limit**: menetapkan harga maksimum saat membeli atau minimum saat menjual. Tidak dijamin terisi jika pasar tidak mencapai harga itu.

                            Di bursa, order bisa bertemu sebagian (partial fill). Kamu mungkin tidak mendapatkan seluruh lot sekaligus. Pahami tampilan antrean bid/ask dan status order di aplikasi sekuritasmu.
                        """,
                    },
                    {
                        "heading": "Likuiditas dan saham tidak likuid",
                        "body": """
                            Saham likuid memiliki banyak pembeli dan penjual, sehingga mudah diperdagangkan dengan spread tipis. Saham tidak likuid bisa memiliki spread lebar dan harga yang mudah bergerak dengan sedikit order.

                            Untuk pemula, hindari saham yang hanya ramai sesaat karena rumor. Periksa nilai transaksi beberapa waktu, bukan hanya satu hari. Snapshot satu hari di proyek ini tidak cukup untuk menyimpulkan likuiditas jangka panjang.
                        """,
                    },
                    {
                        "heading": "Saham gorengan dan manipulasi",
                        "body": """
                            Istilah **saham gorengan** merujuk pada saham yang harganya digerakkan secara tidak wajar, sering oleh sekelompok pihak yang ingin mengambil untung dari investor lain. Ciri yang perlu diwaspadai:

                            - harga naik sangat cepat tanpa perubahan fundamental jelas;
                            - volume melonjak lalu kering;
                            - banyak ajakan "pasti naik" dan target harga muluk;
                            - likuiditas rendah sehingga mudah dikendalikan;
                            - berita tidak jelas atau tidak bisa diverifikasi.

                            Jangan menuduh perusahaan tertentu tanpa bukti, tetapi lindungi dirimu dengan menghindari pola perdagangan yang tidak masuk akal.
                        """,
                    },
                    {
                        "heading": "FOMO dan emosi",
                        "body": """
                            **FOMO (fear of missing out)** adalah rasa takut ketinggalan ketika orang lain terlihat untung. FOMO membuat orang membeli di harga tinggi tanpa rencana.

                            Cara menahannya:

                            - tentukan aturan sebelum membeli;
                            - tunggu minimal satu malam untuk keputusan besar;
                            - tulis alasan dan risiko;
                            - jangan membandingkan hasil orang lain yang tidak kamu ketahui risikonya;
                            - ingat bahwa tidak ikut satu peluang tidak membuatmu gagal.

                            Kehilangan kesempatan lebih murah daripada kehilangan modal karena keputusan panik.
                        """,
                    },
                ],
                "analogy": """
                    FOMO seperti berebut masuk lift yang sudah penuh karena semua orang berlari ke sana. Kamu mungkin masuk, tetapi bisa terjepit. Lebih baik menunggu lift berikutnya dengan tenang daripada memaksakan diri dan kehilangan kendali.
                """,
                "example": """
                    Saham X naik dari Rp200 ke Rp500 dalam tiga hari karena ramai di media sosial. Kamu membeli di Rp490 karena takut ketinggalan. Keesokan hari harga turun ke Rp300 karena pembeli menghilang.

                    Jika kamu memakai order limit di Rp250 dan tidak terisi, kamu tidak untung, tetapi juga tidak kehilangan modal. Tidak semua peluang harus diambil.
                """,
                "application": """
                    Latih diri menulis rencana sebelum transaksi: harga beli maksimum, alasan, risiko, dan kapan evaluasi. Jika rencana tidak bisa dijelaskan dalam tiga kalimat, tunda keputusan.
                """,
                "python": """
                    ```python
                    harga_beli_maks = 250
                    harga_sekarang = 490
                    if harga_sekarang <= harga_beli_maks:
                        print("Sesuai rencana")
                    else:
                        print("Di luar rencana: jangan mengejar harga")
                    ```
                """,
                "mistakes": [
                    "Menggunakan order pasar tanpa memahami harga yang mungkin didapat.",
                    "Membeli saham tidak likuid karena melihat kenaikan sehari.",
                    "Mengejar harga karena takut ketinggalan.",
                    "Mempercayai target harga dari pihak yang tidak dikenal.",
                ],
                "summary": [
                    "Order pasar mengutamakan kecepatan; order limit mengutamakan harga.",
                    "Likuiditas memengaruhi kemudahan dan biaya transaksi.",
                    "Waspadai pola harga tidak wajar dan ajakan pasti untung.",
                    "FOMO mendorong pembelian tanpa rencana.",
                    "Tidak semua peluang harus diambil.",
                ],
                "quiz": [
                    {
                        "q": "Apa kelebihan order limit saat membeli?",
                        "options": [
                            "Menetapkan harga maksimum yang bersedia dibayar",
                            "Menjamin order selalu terisi",
                            "Menghilangkan semua biaya",
                            "Menjamin harga naik",
                        ],
                        "answer": 0,
                        "why": "Order limit menetapkan batas harga. Konsekuensinya, order bisa tidak terisi jika pasar tidak mencapai harga tersebut.",
                    },
                    {
                        "q": "Mengapa saham tidak likuid berisiko?",
                        "options": [
                            "Sulit diperdagangkan tanpa menggerakkan harga dan spread bisa lebar",
                            "Selalu membagikan dividen besar",
                            "Tidak bisa dimiliki investor",
                            "Harganya tidak pernah berubah",
                        ],
                        "answer": 0,
                        "why": "Sedikit pembeli/penjual membuat transaksi sulit dan harga mudah bergerak tidak menguntungkan.",
                    },
                    {
                        "q": "Apa respons sehat terhadap FOMO?",
                        "options": [
                            "Mengikuti pembelian tanpa rencana",
                            "Menunda keputusan dan memeriksa rencana serta risiko",
                            "Meminjam uang agar tidak ketinggalan",
                            "Membeli semua saham yang naik",
                        ],
                        "answer": 1,
                        "why": "Menunda dan mengembalikan keputusan pada rencana membantu menghindari pembelian impulsif di harga tinggi.",
                    },
                ],
            },
        ],
    },
    {
        "id": "m9",
        "number": 9,
        "title": "Membangun Kebiasaan Investor",
        "icon": "🌳",
        "description": "Menjaga konsistensi, mengelola emosi, dan mengevaluasi proses jangka panjang.",
        "lessons": [
            {
                "id": "m9l1",
                "title": "Kebiasaan kecil yang bertahan lama",
                "minutes": 12,
                "goal": "Membangun rutinitas menabung, mencatat, dan belajar tanpa mengejar hasil instan.",
                "sections": [
                    {
                        "heading": "Investasi adalah kebiasaan, bukan satu kali aksi",
                        "body": """
                            Modal Rp700.000 tidak akan berubah menjadi kekayaan dalam semalam. Yang lebih penting adalah kebiasaan:

                            - menyisihkan uang secara rutin;
                            - menjaga dana cadangan;
                            - belajar sebelum membeli;
                            - mencatat keputusan;
                            - mengevaluasi proses, bukan hanya hasil.

                            Mulai dari nominal yang kecil tetapi konsisten. Jika menabung Rp50.000 per minggu terasa berat, mulai dari Rp10.000. Konsistensi lebih penting daripada nominal besar yang tidak bertahan.
                        """,
                    },
                    {
                        "heading": "Tentukan tujuan yang jelas",
                        "body": """
                            Tujuan harus spesifik dan punya waktu. "Ingin kaya" terlalu kabur. Contoh yang lebih baik: "Dalam 5 tahun, saya ingin memiliki dana pendidikan Rp10 juta" atau "Saya ingin belajar menganalisis 5 perusahaan per tahun".

                            Tujuan membantu menentukan horizon. Uang yang dibutuhkan dalam 6 bulan sebaiknya tidak ditaruh di saham karena bisa turun saat kamu membutuhkannya.
                        """,
                    },
                    {
                        "heading": "Kendalikan emosi",
                        "body": """
                            Pasar akan naik dan turun. Berita akan membuat panik atau euforia. Kamu tidak bisa mengendalikan pasar, tetapi bisa mengendalikan:

                            - jumlah uang yang dipertaruhkan;
                            - frekuensi melihat portofolio;
                            - keputusan untuk menunda saat emosi tinggi;
                            - kualitas catatan dan analisis.

                            Jika ingin menjual karena panik, tulis dulu alasannya. Tunggu satu malam. Periksa apakah tesis investasimu benar-benar berubah atau hanya harga yang bergerak.
                        """,
                    },
                    {
                        "heading": "Rayakan proses",
                        "body": """
                            Beri penghargaan pada kebiasaan baik: menyelesaikan analisis, mencatat jurnal, atau berhasil menahan diri dari FOMO. Jangan hanya merayakan untung, karena untung bisa datang dari keberuntungan.

                            Investor yang bertahan lama biasanya bukan yang paling sering menang, tetapi yang mengelola risiko dan emosinya dengan baik.
                        """,
                    },
                ],
                "analogy": """
                    Menanam pohon tidak menghasilkan buah besok pagi. Kamu menyiram, memberi cahaya, dan menunggu. Kalau setiap hari mencabut tanaman untuk melihat akarnya, tanaman tidak akan tumbuh. Investasi juga butuh kesabaran dan perawatan rutin.
                """,
                "example": """
                    Dua orang mulai dengan Rp700.000.

                    - Orang A menyisihkan Rp50.000 per bulan, mencatat pengeluaran, dan belajar satu materi per minggu.
                    - Orang B menaruh semua uang di saham yang sedang ramai, melihat portofolio 20 kali sehari, dan panik saat turun.

                    Setelah setahun, Orang A mungkin belum kaya, tetapi punya kebiasaan dan catatan yang bisa dikembangkan. Orang B mungkin beruntung, tetapi prosesnya rapuh dan sulit diulang.
                """,
                "application": """
                    Gunakan halaman **Beranda & Belajar** untuk menyelesaikan satu pelajaran per sesi. Jangan terburu-buru menyelesaikan semua modul dalam satu hari. Setelah selesai, tulis satu kebiasaan yang akan kamu mulai minggu ini.
                """,
                "python": """
                    ```python
                    target_mingguan = 50_000
                    minggu = 52
                    print(f"Jika konsisten: Rp{target_mingguan * minggu:,.0f} per tahun")
                    ```
                """,
                "mistakes": [
                    "Menunggu punya banyak uang baru mulai belajar.",
                    "Melihat portofolio terlalu sering dan bereaksi pada setiap gerakan.",
                    "Merayakan untung tanpa mengevaluasi proses.",
                    "Mengorbankan dana cadangan untuk menambah investasi.",
                ],
                "summary": [
                    "Investasi adalah kebiasaan jangka panjang.",
                    "Tujuan harus spesifik dan sesuai horizon waktu.",
                    "Emosi dikelola dengan aturan dan jeda keputusan.",
                    "Nilai proses, bukan hanya hasil.",
                    "Konsistensi kecil lebih baik daripada aksi besar yang tidak berkelanjutan.",
                ],
                "quiz": [
                    {
                        "q": "Mengapa uang yang dibutuhkan dalam 6 bulan sebaiknya tidak ditaruh di saham?",
                        "options": [
                            "Karena saham selalu rugi",
                            "Karena harga bisa turun saat uang dibutuhkan",
                            "Karena saham tidak bisa dijual",
                            "Karena tidak ada biaya",
                        ],
                        "answer": 1,
                        "why": "Saham berfluktuasi. Jika horizon pendek, kamu berisiko menjual saat harga sedang rendah.",
                    },
                    {
                        "q": "Apa respons yang lebih baik saat panik karena harga turun?",
                        "options": [
                            "Langsung menjual semua",
                            "Menulis alasan, menunda, lalu memeriksa apakah tesis berubah",
                            "Meminjam uang untuk membeli lagi",
                            "Menghapus aplikasi dan melupakan catatan",
                        ],
                        "answer": 1,
                        "why": "Jeda membantu memisahkan reaksi emosional dari perubahan fundamental yang nyata.",
                    },
                    {
                        "q": "Apa yang sebaiknya dirayakan dalam proses belajar investasi?",
                        "options": [
                            "Hanya keuntungan besar",
                            "Kebiasaan baik dan kualitas proses, bukan hanya hasil",
                            "Jumlah transaksi terbanyak",
                            "Kecepatan membeli saham yang ramai",
                        ],
                        "answer": 1,
                        "why": "Hasil bisa dipengaruhi keberuntungan. Proses yang baik lebih mungkin bertahan dan diulang.",
                    },
                ],
            },
            {
                "id": "m9l2",
                "title": "Mengevaluasi proses dan kapan meninjau ulang",
                "minutes": 13,
                "goal": "Membuat checklist evaluasi dan memahami alasan yang sah untuk menjual.",
                "sections": [
                    {
                        "heading": "Evaluasi berkala, bukan setiap menit",
                        "body": """
                            Tentukan jadwal evaluasi, misalnya setiap tiga bulan atau setelah laporan keuangan terbit. Terlalu sering melihat portofolio bisa mendorong keputusan impulsif.

                            Saat evaluasi, periksa:

                            - apakah alasan awal masih berlaku;
                            - apakah utang atau arus kas berubah;
                            - apakah posisi terlalu besar dibandingkan toleransi risiko;
                            - apakah hasil dibandingkan dengan benchmark;
                            - apakah ada kesalahan proses yang bisa diperbaiki.
                        """,
                    },
                    {
                        "heading": "Alasan yang sah untuk menjual",
                        "body": """
                            Menjual bukan tanda gagal. Beberapa alasan yang masuk akal:

                            1. **Tesis berubah**: bisnis kehilangan keunggulan, utang melonjak, atau laporan mengecewakan secara struktural.
                            2. **Butuh uang**: kebutuhan hidup lebih penting daripada mempertahankan saham.
                            3. **Risiko terlalu besar**: porsi saham membuatmu tidak bisa tidur.
                            4. **Ada peluang yang lebih baik** setelah analisis, bukan karena ikut-ikutan.
                            5. **Aturan portofolio**: rebalancing atau batas risiko yang sudah ditentukan.

                            Harga turun saja bukan otomatis alasan menjual. Harga naik saja juga bukan otomatis alasan menjual.
                        """,
                    },
                    {
                        "heading": "Rebalancing sederhana",
                        "body": """
                            Jika satu saham tumbuh sangat besar hingga mendominasi portofolio, risikonya meningkat. **Rebalancing** berarti mengembalikan porsi ke target yang sudah ditentukan, misalnya dengan mengurangi sebagian posisi atau menambah aset lain.

                            Rebalancing bisa menimbulkan biaya dan pajak. Lakukan dengan sadar, bukan terlalu sering. Untuk portofolio kecil, rebalancing dengan setoran baru bisa lebih hemat biaya.
                        """,
                    },
                    {
                        "heading": "Checklist akhir",
                        "body": """
                            Sebelum membeli:

                            - Apakah ini uang yang boleh menghadapi risiko?
                            - Apakah saya memahami bisnisnya?
                            - Apakah saya sudah membaca laporan resmi?
                            - Berapa risiko maksimum yang saya terima?
                            - Apakah ukuran posisi sesuai?
                            - Apa rencana evaluasi saya?

                            Jika banyak jawaban "belum", tunda. Tidak ada hadiah untuk bertindak cepat.
                        """,
                    },
                ],
                "analogy": """
                    Meninjau portofolio seperti servis kendaraan berkala. Kamu tidak membongkar mesin setiap hari, tetapi juga tidak menunggu sampai mogok. Jadwal yang wajar dan catatan perawatan membuat kendaraan lebih aman.
                """,
                "example": """
                    Kamu membeli saham karena arus kas tumbuh dan utang turun. Setahun kemudian, utang naik tajam dan arus kas operasi negatif dua kuartal. Harga masih naik karena sentimen pasar.

                    Dalam situasi ini, tesis awal sudah melemah. Menjual bisa dipertimbangkan meskipun harga belum turun, karena keputusan didasarkan pada perubahan bisnis, bukan ramalan harga.
                """,
                "application": """
                    Gunakan jurnal di halaman Paper Trading untuk menulis tesis dan tanggal evaluasi. Saat meninjau, baca catatan lama sebelum melihat harga terbaru agar tidak terkena hindsight bias.
                """,
                "python": """
                    ```python
                    tesis = "Arus kas operasi tumbuh dan utang menurun"
                    kondisi_baru = "Arus kas operasi negatif dua kuartal"
                    print("Perlu tinjau ulang" if kondisi_baru != tesis else "Tesis masih relevan")
                    ```
                """,
                "mistakes": [
                    "Menjual hanya karena harga turun sehari.",
                    "Mempertahankan saham hanya karena sudah rugi (sunk cost).",
                    "Terlalu sering rebalancing sampai biaya menggerus hasil.",
                    "Membaca berita terbaru sebelum membaca catatan tesis sendiri.",
                ],
                "summary": [
                    "Evaluasi pada jadwal yang wajar, bukan setiap menit.",
                    "Jual jika tesis berubah, butuh uang, risiko berlebih, atau ada peluang lebih baik.",
                    "Harga turun/naik saja bukan alasan otomatis.",
                    "Rebalancing menjaga risiko tetap sesuai target.",
                    "Gunakan checklist sebelum membeli.",
                ],
                "quiz": [
                    {
                        "q": "Manakah alasan yang paling sehat untuk meninjau ulang keputusan menjual?",
                        "options": [
                            "Harga turun 2% hari ini",
                            "Tesis bisnis berubah, misalnya utang melonjak dan arus kas memburuk",
                            "Teman menjual sahamnya",
                            "Media sosial ramai membicarakannya",
                        ],
                        "answer": 1,
                        "why": "Perubahan fundamental yang merusak tesis adalah alasan yang bisa dianalisis. Pergerakan harga jangka pendek atau ikut-ikutan bukan analisis.",
                    },
                    {
                        "q": "Apa itu sunk cost yang perlu dihindari?",
                        "options": [
                            "Mempertahankan keputusan hanya karena sudah mengeluarkan uang/waktu",
                            "Biaya pajak penjualan",
                            "Biaya administrasi broker",
                            "Dividen yang diterima",
                        ],
                        "answer": 0,
                        "why": "Keputusan ke depan harus berdasarkan kondisi sekarang, bukan pengorbanan yang sudah tidak bisa diubah.",
                    },
                    {
                        "q": "Mengapa evaluasi portofolio tidak perlu dilakukan setiap menit?",
                        "options": [
                            "Karena bisa mendorong keputusan impulsif dan stres berlebihan",
                            "Karena harga tidak pernah berubah",
                            "Karena laporan keuangan tidak penting",
                            "Karena broker melarang melihat portofolio",
                        ],
                        "answer": 0,
                        "why": "Fluktuasi jangka pendek sering tidak berkaitan dengan perubahan fundamental. Terlalu sering memantau bisa memicu reaksi emosional.",
                    },
                ],
            },
        ],
    },
]


def all_lessons() -> list[dict]:
    """Daftar semua pelajaran sesuai urutan kurikulum."""
    return [lesson for module in MODULES for lesson in module["lessons"]]


def ordered_lesson_ids() -> list[str]:
    return [lesson["id"] for lesson in all_lessons()]


def get_lesson(lesson_id: str) -> dict | None:
    for lesson in all_lessons():
        if lesson["id"] == lesson_id:
            return lesson
    return None


def get_module(module_id: str) -> dict | None:
    for module in MODULES:
        if module["id"] == module_id:
            return module
    return None


def module_for_lesson(lesson_id: str) -> dict | None:
    for module in MODULES:
        if any(lesson["id"] == lesson_id for lesson in module["lessons"]):
            return module
    return None


def lesson_number(lesson_id: str) -> int:
    ids = ordered_lesson_ids()
    return ids.index(lesson_id) + 1 if lesson_id in ids else 0


def total_lessons() -> int:
    return len(all_lessons())
