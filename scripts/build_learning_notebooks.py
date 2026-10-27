"""Membuat materi belajar mandiri untuk dibaca di VSCode.

Jalankan dari root proyek:
    python scripts/build_learning_notebooks.py

Sumber konten: src/learning_content.py
Hasil: folder "notebooks pembelajaran" (9 notebook modul + panduan).
"""

from __future__ import annotations

import re
import sys
import textwrap
import unicodedata
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.learning_content import MODULES  # noqa: E402

MATERIAL_DIR = ROOT / "notebooks pembelajaran"
GUIDE_NAME = "00_Panduan_Belajar.ipynb"


def clean(text: str) -> str:
    """Rapikan indentasi triple-quoted string dari learning_content."""
    return textwrap.dedent(text).strip()


def render(template: str, **values: str) -> str:
    """Dedent template dulu, baru masukkan nilai multiline.

    Ini penting agar isi pelajaran tidak membawa indentasi dari source code
    generator ke dalam Markdown notebook.
    """
    return textwrap.dedent(template).format(**values).strip()


def quote(text: str) -> str:
    """Ubah teks menjadi blockquote Markdown."""
    lines = clean(text).splitlines()
    return "\n".join("> " + line if line.strip() else ">" for line in lines)


def extract_code(text: str) -> str:
    """Ambil isi blok ```python ...``` dari field python."""
    match = re.search(r"```python\s*\n(.*?)```", text, flags=re.DOTALL)
    if match:
        return textwrap.dedent(match.group(1)).strip()
    return clean(text)


def slug(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", normalized).strip("_")
    return normalized or "materi"


def module_filename(module: dict) -> str:
    return f"Modul_{module['number']:02d}_{slug(module['title'])}.ipynb"


def module_link(module: dict) -> str:
    return module_filename(module)


def markdown(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(clean(source))


def code(source: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(clean(source))


def make_notebook(cells: list[nbf.NotebookNode], notebook_id: str) -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.13.15"}
    nb.metadata["sahamlab"] = {
        "generated_from": "src/learning_content.py",
        "audience": "pemula",
        "language": "id",
    }
    nb.cells = cells
    for index, cell in enumerate(nb.cells, start=1):
        cell["id"] = f"{notebook_id}-{index:02d}"
    nbf.validate(nb)
    return nb


def lesson_cells(module: dict, lesson: dict, number: int) -> list[nbf.NotebookNode]:
    cells: list[nbf.NotebookNode] = [
        markdown(
            render(
                """
                ---

                ## Pelajaran {number}: {title}

                **Estimasi:** {minutes} menit

                **Tujuan pembelajaran:** {goal}
                """,
                number=str(number),
                title=lesson["title"],
                minutes=str(lesson["minutes"]),
                goal=lesson["goal"],
            )
        )
    ]

    for section in lesson["sections"]:
        cells.append(
            markdown(
                render(
                    """
                    ### {heading}

                    {body}
                    """,
                    heading=section["heading"],
                    body=clean(section["body"]),
                )
            )
        )

    cells.append(markdown(f"### Analogi\n\n{quote(lesson['analogy'])}"))
    cells.append(markdown(f"### Contoh\n\n{clean(lesson['example'])}"))
    cells.append(markdown(f"### Penerapan\n\n{clean(lesson['application'])}"))

    if lesson.get("python"):
        kode = extract_code(lesson["python"])
        cells.append(
            markdown(
                """
                ### Contoh kode Python

                Contoh berikut untuk dibaca dan dicoba. Untuk praktik yang benar-benar
                dijalankan dengan data proyek, gunakan notebook di folder `notebooks/`.
                """
            )
        )
        cells.append(markdown(f"```python\n{kode}\n```"))

    mistakes = "\n".join(f"- {item}" for item in lesson["mistakes"])
    cells.append(markdown(f"### Kesalahan yang perlu dihindari\n\n{mistakes}"))

    summary = "\n".join(f"- {item}" for item in lesson["summary"])
    cells.append(markdown(f"### Ringkasan\n\n{summary}"))

    quiz_lines = []
    answer_lines = []
    for index, item in enumerate(lesson["quiz"], start=1):
        quiz_lines.append(f"**{index}. {item['q']}**\n")
        for option_index, option in enumerate(item["options"]):
            quiz_lines.append(f"- {chr(65 + option_index)}. {option}")
        quiz_lines.append("")

        correct = chr(65 + int(item["answer"]))
        answer_lines.append(f"- **{index}. {correct}** — {item['why']}")

    cells.append(
        markdown(
            render(
                """
                ### Kuis — 3 soal

                Jawab dulu tanpa membuka kunci di bawah. Nilai **minimal 2 dari 3 benar**
                untuk dianggap lulus pelajaran ini.

                {quiz}
                """,
                quiz="\n".join(quiz_lines).strip(),
            )
        )
    )

    cells.append(
        markdown(
            render(
                """
                <details>
                <summary>Kunci jawaban dan pembahasan</summary>

                {answers}

                </details>
                """,
                answers="\n".join(answer_lines),
            )
        )
    )

    return cells


def module_cells(module: dict) -> list[nbf.NotebookNode]:
    total_minutes = sum(lesson["minutes"] for lesson in module["lessons"])
    total_quiz = sum(len(lesson["quiz"]) for lesson in module["lessons"])

    daftar = "\n".join(
        f"{index}. **{lesson['title']}** — {lesson['minutes']} menit"
        for index, lesson in enumerate(module["lessons"], start=1)
    )

    cells: list[nbf.NotebookNode] = [
        markdown(
            render(
                """
                # {icon} Modul {number} — {title}

                > {description}

                **Estimasi:** {total_minutes} menit · **Pelajaran:** {lesson_count} ·
                **Soal kuis:** {total_quiz}

                [← Kembali ke panduan belajar]({guide})

                ## Cara memakai notebook ini

                1. Baca satu pelajaran sampai selesai.
                2. Jawab tiga soal tanpa membuka kunci jawaban.
                3. Buka kunci, lalu jelaskan ulang bagian yang salah dengan kata sendiri.
                4. Lanjut ke pelajaran berikutnya jika sudah memahami intinya.

                Materi ini untuk dibaca. Untuk latihan Python yang dijalankan dengan data
                proyek, buka folder `notebooks/`.

                ## Daftar pelajaran

                {daftar}
                """,
                icon=module["icon"],
                number=f"{module['number']:02d}",
                title=module["title"],
                description=module["description"],
                total_minutes=str(total_minutes),
                lesson_count=str(len(module["lessons"])),
                total_quiz=str(total_quiz),
                guide=GUIDE_NAME,
                daftar=daftar,
            )
        )
    ]

    for number, lesson in enumerate(module["lessons"], start=1):
        cells.extend(lesson_cells(module, lesson, number))

    index = MODULES.index(module)
    if index + 1 < len(MODULES):
        next_module = MODULES[index + 1]
        next_line = (
            f"**Modul berikutnya:** [{next_module['icon']} Modul {next_module['number']:02d} — "
            f"{next_module['title']}]({module_link(next_module)})"
        )
    else:
        next_line = f"**Selesai:** kembali ke [{GUIDE_NAME}]({GUIDE_NAME})"

    cells.append(
        markdown(
            render(
                """
                ---

                ## Checklist modul

                - [ ] Saya membaca kedua pelajaran sampai selesai.
                - [ ] Saya menjawab enam soal tanpa membuka kunci lebih dulu.
                - [ ] Saya bisa menjelaskan inti modul dengan kata sendiri.
                - [ ] Saya mencatat bagian yang masih belum jelas.

                {next_line}

                > **Pengingat:** materi ini bukan rekomendasi investasi dan tidak menjanjikan
                > keuntungan. Jangan memakai utang, margin, atau uang kebutuhan untuk berinvestasi.
                """,
                next_line=next_line,
            )
        )
    )

    return cells


def guide_cells() -> list[nbf.NotebookNode]:
    rows = "\n".join(
        f"| {module['number']} | {module['icon']} {module['title']} | "
        f"{sum(lesson['minutes'] for lesson in module['lessons'])} menit | "
        f"[Buka]({module_link(module)}) |"
        for module in MODULES
    )
    total_minutes = sum(lesson["minutes"] for module in MODULES for lesson in module["lessons"])
    total_lessons = sum(len(module["lessons"]) for module in MODULES)
    total_quiz = sum(len(lesson["quiz"]) for module in MODULES for lesson in module["lessons"])

    return [
        markdown(
            render(
                """
                # 📚 Panduan Belajar SahamLab

                Folder ini berisi materi bacaan lengkap untuk **{module_count} modul**,
                **{total_lessons} pelajaran**, dan **{total_quiz} soal pilihan ganda**.
                Total waktu baca sekitar **{hours} jam {minutes} menit**.

                Materi ini disusun untuk pemula yang ingin memahami saham dengan tenang,
                bukan mengejar keuntungan cepat. Setiap pelajaran punya tiga soal dan kunci
                jawaban yang bisa dibuka setelah menjawab.

                ## Cara membuka di VSCode

                1. Buka **folder proyek** `project saham`, bukan hanya folder notebook.
                2. Pasang ekstensi **Python** dan **Jupyter** di VSCode.
                3. Buka `notebooks pembelajaran/00_Panduan_Belajar.ipynb`.
                4. Pilih kernel Python 3.13.15 hanya jika ingin menjalankan sel kode opsional.
                5. Untuk membaca materi, notebook tidak perlu dijalankan.

                > **Tips:** gunakan panel **Outline** di VSCode untuk berpindah antar-pelajaran,
                > atau buka file modul langsung dari daftar di bawah.

                ## Peta modul

                | # | Modul | Estimasi | Notebook |
                |---:|---|---:|---|
                {rows}

                ## Aturan belajar

                - Satu pelajaran per sesi. Jangan mengejar semua materi sekaligus.
                - Jawab tiga soal sebelum membuka kunci jawaban.
                - Minimal **2 dari 3 benar** sebelum lanjut ke pelajaran berikutnya.
                - Tulis ulang konsep dengan kata sendiri; hafalan saja tidak cukup.
                - Catat bagian yang belum jelas, lalu cek dashboard atau data proyek.
                - Gunakan uang yang siap menghadapi risiko. Jangan memakai utang atau margin.

                ## Cek lingkungan proyek

                Sel berikut opsional dan hanya memeriksa apakah folder proyek serta data
                historis bisa ditemukan. Tidak mengubah file apa pun.
                """,
                module_count=str(len(MODULES)),
                total_lessons=str(total_lessons),
                total_quiz=str(total_quiz),
                hours=str(total_minutes // 60),
                minutes=str(total_minutes % 60),
                rows=rows,
            )
        ),
        code(
            """
            from pathlib import Path

            root = Path.cwd()
            while root != root.parent and not (root / "app.py").exists():
                root = root.parent

            print("Root proyek:", root)
            print("app.py ditemukan:", (root / "app.py").exists())
            print(
                "Data historis ditemukan:",
                (root / "data/processed/historical_prices.csv").exists(),
            )
            """
        ),
        markdown(
            """
            ## Bedanya dengan folder `notebooks/`

            | Folder | Isi | Cara pakai |
            |---|---|---|
            | `notebooks pembelajaran/` | Materi bacaan, kuis, kunci jawaban | Dibaca di VSCode; tidak perlu dijalankan |
            | `notebooks/` | Lab Python dengan output nyata | Dijalankan dengan kernel Python dan data proyek |

            Jika ingin melihat perhitungan return, risiko, atau eksplorasi data, buka
            `../notebooks/01_data_understanding.ipynb` dan lanjutkan ke notebook berikutnya.

            ## Menjalankan dashboard

            Dari root proyek:

            ```powershell
            python -m streamlit run app.py
            ```

            Dashboard dipakai untuk progres kuis otomatis, simulasi Rp700.000, dan paper
            trading. Folder materi ini tidak mengubah progres di dashboard.

            ## Membuat ulang materi

            ```powershell
            python scripts\\build_learning_notebooks.py
            ```

            Generator membaca `src/learning_content.py` dan menimpa notebook dengan nama
            yang sama. Simpan catatan pribadi di file terpisah agar tidak hilang.

            ## Pengingat

            Materi ini bersifat edukasi, bukan rekomendasi membeli atau menjual saham.
            Tidak ada keuntungan yang dijamin. Harga bisa turun dan modal bisa berkurang.
            """
        ),
    ]


def build_readme() -> str:
    rows = "\n".join(
        f"| {module['number']} | {module['icon']} {module['title']} | "
        f"{sum(lesson['minutes'] for lesson in module['lessons'])} menit | "
        f"[Buka]({module_link(module)}) |"
        for module in MODULES
    )
    total_minutes = sum(lesson["minutes"] for module in MODULES for lesson in module["lessons"])
    total_lessons = sum(len(module["lessons"]) for module in MODULES)
    total_quiz = sum(len(lesson["quiz"]) for module in MODULES for lesson in module["lessons"])

    return f"""# 📚 Materi Belajar SahamLab

Materi bacaan lengkap **{len(MODULES)} modul**, **{total_lessons} pelajaran**, dan
**{total_quiz} soal pilihan ganda**. Total waktu baca sekitar
**{total_minutes // 60} jam {total_minutes % 60} menit**.

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
{rows}

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
python scripts\\build_learning_notebooks.py
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
"""


def main() -> int:
    MATERIAL_DIR.mkdir(exist_ok=True)

    guide = make_notebook(guide_cells(), "panduan")
    guide_path = MATERIAL_DIR / GUIDE_NAME
    with guide_path.open("w", encoding="utf-8") as handle:
        nbf.write(guide, handle)

    for module in MODULES:
        notebook = make_notebook(module_cells(module), module["id"])
        path = MATERIAL_DIR / module_filename(module)
        with path.open("w", encoding="utf-8") as handle:
            nbf.write(notebook, handle)
        print(f"OK  {path.relative_to(ROOT)}")

    readme_path = MATERIAL_DIR / "README.md"
    readme_path.write_text(build_readme(), encoding="utf-8")
    print(f"OK  {readme_path.relative_to(ROOT)}")
    print(f"\nSelesai: {len(MODULES)} modul + panduan di {MATERIAL_DIR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
