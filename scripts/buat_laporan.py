"""Membangun laporan.pdf dari data/statistik.json dan data/hasil_preprocessing.csv.

Jalankan dari root project:
    python scripts/buat_laporan.py
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).resolve().parent.parent
JSON_PATH = BASE / "data" / "statistik.json"
CSV_PATH = BASE / "data" / "hasil_preprocessing.csv"
CHART_PATH = BASE / "figures" / "distribusi_label.png"
OUT_PATH = BASE / "laporan.pdf"

if not JSON_PATH.exists():
    raise FileNotFoundError(
        f"{JSON_PATH} belum ada. Jalankan preprocessing_ulasan.ipynb terlebih dahulu."
    )

stat = json.loads(JSON_PATH.read_text(encoding="utf-8"))
csv_df = pd.read_csv(CSV_PATH)

ds = stat["dataset"]
st = stat["statistik"]
GITHUB = stat["github"]
NAMA = stat["nama"]
NIM = stat["nim"]
TANGGAL = stat["tanggal"]

DARK = colors.HexColor("#1f3a5f")
ACCENT = colors.HexColor("#2e86c1")
GRID = colors.HexColor("#bdc3c7")
LIGHT = colors.HexColor("#f4f6f7")


def safe(text):
    """Buang karakter non-ASCII agar aman pada font standar PDF."""
    return str(text).encode("ascii", "ignore").decode("ascii")


def clip(text, n=175):
    s = " ".join(safe(text).split())
    return s if len(s) <= n else s[:n].rstrip() + "..."


def esc(text):
    return escape(safe(text))


styles = {
    "title": ParagraphStyle(
        "title", fontName="Helvetica-Bold", fontSize=21, leading=26,
        alignment=TA_CENTER, textColor=DARK, spaceAfter=6,
    ),
    "subtitle": ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=13, leading=18,
        alignment=TA_CENTER, textColor=colors.HexColor("#4d5656"),
    ),
    "identity": ParagraphStyle(
        "identity", fontName="Helvetica", fontSize=12, leading=18,
        alignment=TA_CENTER,
    ),
    "h1": ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=14, leading=18,
        textColor=DARK, spaceBefore=10, spaceAfter=6,
    ),
    "h2": ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=11, leading=14,
        textColor=ACCENT, spaceBefore=8, spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "body", fontName="Helvetica", fontSize=9.8, leading=14.5,
        alignment=TA_JUSTIFY, spaceAfter=6,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=9.8, leading=14.5,
        alignment=TA_JUSTIFY, leftIndent=14, bulletIndent=4, spaceAfter=4,
    ),
    "caption": ParagraphStyle(
        "caption", fontName="Helvetica-Oblique", fontSize=8.2, leading=11,
        alignment=TA_CENTER, textColor=colors.HexColor("#566573"), spaceAfter=8,
    ),
    "link": ParagraphStyle(
        "link", fontName="Helvetica", fontSize=11, leading=16,
        alignment=TA_CENTER,
    ),
    "code": ParagraphStyle(
        "code", fontName="Courier", fontSize=7.4, leading=9.6,
        textColor=colors.HexColor("#1b2631"), backColor=colors.HexColor("#eef2f5"),
        borderPadding=(4, 5, 4, 5), leftIndent=4, spaceBefore=2, spaceAfter=8,
    ),
    "cell": ParagraphStyle(
        "cell", fontName="Helvetica", fontSize=7.6, leading=9.6,
        alignment=TA_LEFT, wordWrap="CJK",
    ),
    "cell_small": ParagraphStyle(
        "cell_small", fontName="Helvetica", fontSize=7.2, leading=9.0,
        alignment=TA_LEFT, wordWrap="CJK",
    ),
    "cell_head": ParagraphStyle(
        "cell_head", fontName="Helvetica-Bold", fontSize=7.8, leading=10,
        alignment=TA_CENTER, textColor=colors.white,
    ),
    "cell_center": ParagraphStyle(
        "cell_center", fontName="Helvetica", fontSize=8.4, leading=10.5,
        alignment=TA_CENTER,
    ),
}


def P(text, style="body"):
    return Paragraph(text, styles[style])


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.8)
    canvas.setFillColor(colors.HexColor("#7f8c8d"))
    canvas.drawString(2 * cm, 1.15 * cm, "Muhammad Hafidz - 24146028 - Preprocessing Ulasan E-Commerce")
    canvas.drawRightString(A4[0] - 2 * cm, 1.15 * cm, f"Halaman {doc.page}")
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.4)
    canvas.line(2 * cm, 1.55 * cm, A4[0] - 2 * cm, 1.55 * cm)
    canvas.restoreState()


def base_table_style(header_rows=1):
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, header_rows - 1), DARK),
        ("TEXTCOLOR", (0, 0), (-1, header_rows - 1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, header_rows), (-1, -1), [colors.white, LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ])


story = []

# ------------------------- Halaman judul -------------------------
story.append(Spacer(1, 3.2 * cm))
story.append(P("LAPORAN TUGAS", "subtitle"))
story.append(Spacer(1, 0.2 * cm))
story.append(P("Preprocessing Teks Ulasan Produk<br/>E-Commerce Berbahasa Indonesia", "title"))
story.append(Spacer(1, 0.35 * cm))
story.append(P("Case Folding, Cleaning, Tokenisasi, Stopword Removal, dan Stemming", "subtitle"))
story.append(Spacer(1, 2.2 * cm))
story.append(P(f"<b>Nama:</b> {esc(NAMA)}", "identity"))
story.append(P(f"<b>NIM:</b> {esc(NIM)}", "identity"))
story.append(P("Mata Kuliah: Pengolahan Bahasa Alami (NLP)", "identity"))
story.append(Spacer(1, 2.0 * cm))
story.append(P("Repositori GitHub:", "identity"))
story.append(P(
    f'<link href="{GITHUB}" color="#1a5276">{esc(GITHUB)}</link>',
    "link",
))
story.append(Spacer(1, 1.6 * cm))
story.append(P(f"Tanggal: {esc(TANGGAL)}", "identity"))
story.append(PageBreak())

# ------------------------- 1. Dataset -------------------------
story.append(P("1. Dataset", "h1"))
story.append(P(
    "Penelitian ini menggunakan dataset publik <b>ecommerce-product-reviews-sentiment</b> "
    "yang tersedia di Hugging Face. Dataset berisi ulasan produk e-commerce berbahasa "
    "Indonesia beserta terjemahan dan label sentimen. Data dimuat langsung dari repositori "
    f'dataset menggunakan pustaka <font face="Courier">datasets</font>, dengan metode pemuatan: '
    f"{esc(ds['metode_load'])}."
))
story.append(P(
    f'Sumber dataset: <link href="{esc(ds["sumber"])}" color="#1a5276">'
    f'{esc(ds["sumber"])}</link>',
    "body",
))

info_rows = [
    [P("Item", "cell_head"), P("Keterangan", "cell_head")],
    [P("Nama dataset", "cell"), P(esc(ds["nama"]), "cell")],
    [P("Jumlah data", "cell"), P(f"{int(ds['jumlah_data']):,}".replace(",", "."), "cell")],
    [P("Kolom", "cell"), P(", ".join(f"<font face='Courier'>{esc(k)}</font>" for k in ds["kolom"]), "cell")],
    [P("Baris duplikat", "cell"), P(str(ds["duplikat"]), "cell")],
    [P("Missing value", "cell"), P(
        ", ".join(f"{esc(k)}={v}" for k, v in ds["missing"].items()), "cell")],
]
info_table = Table(info_rows, colWidths=[4.0 * cm, 12.0 * cm], repeatRows=1)
info_table.setStyle(base_table_style())
story.append(info_table)
story.append(Spacer(1, 0.35 * cm))

story.append(P("Kolom dan Tipe Data", "h2"))
kolom_rows = [[P("Kolom", "cell_head"), P("Tipe data", "cell_head"), P("Missing", "cell_head")]]
for kolom in ds["kolom"]:
    kolom_rows.append([
        P(f"<font face='Courier'>{esc(kolom)}</font>", "cell"),
        P(esc(ds["tipe_data"].get(kolom, "-")), "cell_center"),
        P(str(ds["missing"].get(kolom, 0)), "cell_center"),
    ])
kolom_table = Table(kolom_rows, colWidths=[6.0 * cm, 5.0 * cm, 5.0 * cm], repeatRows=1)
kolom_table.setStyle(base_table_style())
story.append(kolom_table)
story.append(Spacer(1, 0.35 * cm))

story.append(P("Distribusi Label Sentimen", "h2"))
story.append(P(
    "Label mengikuti dokumentasi dataset: <b>0 = negatif</b> dan <b>1 = positif</b>. "
    "Distribusi dihitung langsung dari kolom <font face='Courier'>sentimen</font>."
))
dist_rows = [[P("Label", "cell_head"), P("Keterangan", "cell_head"),
              P("Jumlah", "cell_head"), P("Persentase", "cell_head")]]
for label in sorted(ds["distribusi_label"].keys(), key=lambda x: int(x)):
    item = ds["distribusi_label"][label]
    dist_rows.append([
        P(label, "cell_center"),
        P(esc(item["keterangan"]), "cell_center"),
        P(f"{int(item['jumlah']):,}".replace(",", "."), "cell_center"),
        P(f"{item['persentase']:.2f}%".replace(".", ","), "cell_center"),
    ])
dist_table = Table(dist_rows, colWidths=[2.2 * cm, 4.0 * cm, 3.6 * cm, 3.6 * cm], repeatRows=1)
dist_table.setStyle(base_table_style())
story.append(dist_table)
story.append(Spacer(1, 0.3 * cm))

if CHART_PATH.exists():
    story.append(Image(str(CHART_PATH), width=10.4 * cm, height=10.4 * cm * 4 / 6))
    story.append(P("Gambar 1. Distribusi label sentimen pada dataset.", "caption"))

# ------------------------- 2. Metode -------------------------
story.append(PageBreak())
story.append(P("2. Metode Preprocessing", "h1"))
story.append(P(
    "Preprocessing dilakukan secara bertahap. Setiap tahap disimpan pada kolom tersendiri "
    "agar perubahan teks dapat ditelusuri. Urutan tahapan adalah case folding, cleaning, "
    "tokenisasi, stopword removal, dan stemming."
))

stages = [
    ("2.1 Case Folding",
     "Mengubah seluruh teks menjadi huruf kecil sehingga variasi kapitalisasi seperti "
     "\"Bagus\", \"bagus\", dan \"BAGUS\" diperlakukan sama.",
     "def case_folding(text):\n    return str(text).lower()"),
    ("2.2 Cleaning",
     "Menghapus URL, tag HTML, angka, tanda baca, karakter khusus/emoji, lalu merapikan "
     "spasi berlebih. Pola <font face='Courier'>[^a-z\\s]</font> menyisakan huruf dan spasi.",
     "text = URL_RE.sub(\" \", text)\ntext = HTML_RE.sub(\" \", text)\n"
     "text = NON_LETTER_RE.sub(\" \", text)  # angka, tanda baca, emoji\ntext = WS_RE.sub(\" \", text).strip()"),
    ("2.3 Tokenisasi",
     "Memecah teks bersih menjadi daftar token kata menggunakan NLTK, dengan fallback "
     "<font face='Courier'>split()</font> bila resource tokenizer tidak tersedia.",
     "try:\n    tokens = nltk.word_tokenize(text)\nexcept Exception:\n    tokens = text.split()"),
    ("2.4 Stopword Removal",
     "Membuang kata umum bahasa Indonesia memakai daftar stopword Sastrawi "
     f"({int(st['jumlah_stopword_sastrawi'])} kata).",
     "STOPWORDS = set(StopWordRemoverFactory().get_stop_words())\n"
     "tokens = [t for t in tokens if t and t not in STOPWORDS]"),
    ("2.5 Stemming",
     "Mengubah kata berimbuhan menjadi kata dasar memakai Sastrawi. Cache per kata unik "
     "mencegah perhitungan berulang sehingga proses lebih cepat.",
     "stemmer = StemmerFactory().create_stemmer()\ncache = {}\n"
     "def stem_token(t):\n    if t not in cache:\n        cache[t] = stemmer.stem(t)\n"
     "    return cache[t]\ntokens = [stem_token(t) for t in tokens]"),
]
for title, desc, code in stages:
    story.append(P(title, "h2"))
    story.append(P(desc))
    story.append(Preformatted(code, styles["code"]))

# ------------------------- 3. Hasil -------------------------
story.append(PageBreak())
story.append(P("3. Hasil dan Contoh", "h1"))
story.append(P(
    "Tabel berikut merangkum dampak preprocessing terhadap seluruh dataset. Angka diambil "
    "langsung dari <font face='Courier'>data/statistik.json</font> yang dihasilkan notebook."
))

def fmt_num(v):
    if isinstance(v, float):
        return f"{v:.2f}".replace(".", ",")
    return f"{int(v):,}".replace(",", ".")

def pct_change(before, after):
    if before == 0:
        return "-"
    val = (after - before) / before * 100
    return f"{val:+.2f}%".replace(".", ",")

stat_rows = [
    [P("Metrik", "cell_head"), P("Sebelum", "cell_head"),
     P("Sesudah", "cell_head"), P("Perubahan", "cell_head")],
    [P("Rata-rata panjang karakter", "cell"),
     P(fmt_num(st["rata_panjang_karakter_sebelum"]), "cell_center"),
     P(fmt_num(st["rata_panjang_karakter_sesudah"]), "cell_center"),
     P(pct_change(st["rata_panjang_karakter_sebelum"], st["rata_panjang_karakter_sesudah"]), "cell_center")],
    [P("Rata-rata panjang kata", "cell"),
     P(fmt_num(st["rata_panjang_kata_sebelum"]), "cell_center"),
     P(fmt_num(st["rata_panjang_kata_sesudah"]), "cell_center"),
     P(pct_change(st["rata_panjang_kata_sebelum"], st["rata_panjang_kata_sesudah"]), "cell_center")],
    [P("Total kata", "cell"),
     P(fmt_num(st["total_kata_sebelum"]), "cell_center"),
     P(fmt_num(st["total_kata_sesudah"]), "cell_center"),
     P(pct_change(st["total_kata_sebelum"], st["total_kata_sesudah"]), "cell_center")],
    [P("Ukuran vocabulary (kata unik)", "cell"),
     P(fmt_num(st["vocabulary_sebelum"]), "cell_center"),
     P(fmt_num(st["vocabulary_sesudah"]), "cell_center"),
     P(f"-{st['penurunan_vocabulary_persen']:.2f}%".replace(".", ","), "cell_center")],
]
stat_table = Table(stat_rows, colWidths=[6.2 * cm, 3.3 * cm, 3.3 * cm, 3.2 * cm], repeatRows=1)
stat_table.setStyle(base_table_style())
story.append(stat_table)
story.append(Spacer(1, 0.25 * cm))
story.append(P(
    f"Setelah preprocessing, rata-rata teks menyusut dari "
    f"{fmt_num(st['rata_panjang_karakter_sebelum'])} menjadi "
    f"{fmt_num(st['rata_panjang_karakter_sesudah'])} karakter dan dari "
    f"{fmt_num(st['rata_panjang_kata_sebelum'])} menjadi "
    f"{fmt_num(st['rata_panjang_kata_sesudah'])} kata. Vocabulary menurun "
    f"{fmt_num(st['penurunan_vocabulary'])} kata ({fmt_num(st['penurunan_vocabulary_persen'])}%). "
    f"Terdapat {st['jumlah_teks_kosong']} teks kosong setelah preprocessing "
    f"({fmt_num(st['persentase_teks_kosong'])}%)."
))
story.append(Spacer(1, 0.2 * cm))

story.append(P("3.1 Sepuluh Contoh Sebelum dan Sesudah Preprocessing", "h2"))
story.append(P(
    "Sepuluh contoh diambil acak dengan <font face='Courier'>random_state=42</font>. "
    "Teks asli dan hasil akhir dibaca dari <font face='Courier'>data/hasil_preprocessing.csv</font> "
    "pada indeks yang tercatat di <font face='Courier'>statistik.json</font>."
))

fallback = {int(c["index_asli"]): c for c in stat["contoh"]}
contoh_rows = [[P("No", "cell_head"), P("Teks Asli (review)", "cell_head"),
                P("Hasil Preprocessing (stemming)", "cell_head")]]
for i, idx in enumerate(stat["contoh_indeks"], start=1):
    if 0 <= idx < len(csv_df):
        review = csv_df.iloc[idx]["review"]
        processed = csv_df.iloc[idx]["stemming"]
    else:
        review = fallback[idx]["review"]
        processed = fallback[idx]["stemming"]
    contoh_rows.append([
        P(str(i), "cell_center"),
        P(esc(clip(review, 185)), "cell_small"),
        P(esc(clip(processed, 185)), "cell_small"),
    ])
contoh_table = Table(
    contoh_rows,
    colWidths=[1.0 * cm, 7.4 * cm, 7.4 * cm],
    repeatRows=1,
)
contoh_table.setStyle(base_table_style())
story.append(contoh_table)
story.append(P(
    "Teks panjang dipotong agar tabel tetap berada di dalam halaman. "
    "Data lengkap tersedia pada berkas CSV.",
    "caption",
))

# ------------------------- 4. Pembahasan -------------------------
story.append(P("4. Pembahasan", "h1"))
story.append(P(
    f"Preprocessing menurunkan noise secara signifikan. Rata-rata panjang teks turun "
    f"{fmt_num(abs(st['rata_panjang_karakter_sebelum'] - st['rata_panjang_karakter_sesudah']))} "
    f"karakter dan {fmt_num(abs(st['rata_panjang_kata_sebelum'] - st['rata_panjang_kata_sesudah']))} "
    f"kata. Cleaning membuang URL, angka, tanda baca, dan emoji yang tidak relevan, sedangkan "
    f"stopword removal membuang kata umum yang tidak membawa makna penting. Akibatnya teks "
    f"menjadi lebih padat dan fokus pada kata bermakna."
))
story.append(P(
    f"Case folding dan stemming menormalkan bentuk kata. Kata berimbuhan seperti "
    f"\"pengirimannya\" dan \"berbelanja\" berubah menjadi kata dasar \"kirim\" dan \"belanja\", "
    f"sehingga bentuk yang berbeda tidak dihitung sebagai fitur terpisah. Dampaknya, ukuran "
    f"vocabulary turun dari {fmt_num(st['vocabulary_sebelum'])} menjadi "
    f"{fmt_num(st['vocabulary_sesudah'])} kata, atau turun "
    f"{fmt_num(st['penurunan_vocabulary_persen'])}%. Vocabulary yang lebih kecil membantu "
    f"model analisis teks menjadi lebih efisien dan mengurangi sparsity."
))
story.append(P(
    f"Meskipun demikian, terdapat risiko yang perlu diperhatikan. Stopword Sastrawi memuat "
    f"kata negasi seperti \"tidak\", sehingga kalimat \"remote control tidak peka\" berubah "
    f"menjadi \"remote control peka\" setelah stopword removal. Perubahan ini dapat membalik "
    f"polaritas sentimen. Selain itu, stemming dapat keliru pada kata tidak baku atau "
    f"singkatan; pada contoh data, \"ditangan\" menjadi \"tang\" dan \"pelanggan\" menjadi "
    f"\"langgan\". Oleh karena itu, untuk tugas analisis sentimen, kata negasi sebaiknya "
    f"dipertahankan dan hasil stemming perlu divalidasi."
))
story.append(P(
    f"Terdapat pula {st['jumlah_teks_kosong']} ulasan "
    f"({fmt_num(st['persentase_teks_kosong'])}%) yang menjadi kosong setelah preprocessing, "
    f"umumnya karena isinya hanya emoji, angka, atau kata umum. Baris seperti ini perlu "
    f"ditangani pada tahap pemodelan, misalnya dengan menghapusnya atau memberi label khusus."
))

# ------------------------- 5. Kesimpulan -------------------------
story.append(P("5. Kesimpulan", "h1"))
conclusions = [
    "Dataset berhasil dimuat langsung dari Hugging Face dengan jumlah 11.606 ulasan dan tiga "
    "kolom utama: review, translate, dan sentimen. Distribusi label seimbang, yaitu 5.803 "
    "ulasan negatif dan 5.803 ulasan positif.",
    "Pipeline preprocessing berhasil dijalankan melalui lima tahap: case folding, cleaning, "
    "tokenisasi, stopword removal, dan stemming. Setiap tahap disimpan pada kolom tersendiri.",
    f"Preprocessing menurunkan rata-rata panjang teks dari "
    f"{fmt_num(st['rata_panjang_karakter_sebelum'])} menjadi "
    f"{fmt_num(st['rata_panjang_karakter_sesudah'])} karakter, serta mengecilkan vocabulary "
    f"sebesar {fmt_num(st['penurunan_vocabulary_persen'])}%.",
    "Preprocessing meningkatkan kerapian dan konsistensi teks, tetapi berisiko menghilangkan "
    "negasi dan menimbulkan kesalahan stemming. Untuk analisis sentimen, kata negasi perlu "
    "dipertahankan dan hasil stemming perlu diperiksa.",
]
for i, item in enumerate(conclusions, start=1):
    story.append(P(f"{i}. {item}", "bullet"))

story.append(Spacer(1, 0.5 * cm))
story.append(P(
    f"Kode, notebook, data hasil, dan laporan ini tersedia di "
    f'<link href="{GITHUB}" color="#1a5276">{esc(GITHUB)}</link>.',
    "body",
))

doc = SimpleDocTemplate(
    str(OUT_PATH),
    pagesize=A4,
    leftMargin=2 * cm,
    rightMargin=2 * cm,
    topMargin=1.9 * cm,
    bottomMargin=2 * cm,
    title="Laporan Preprocessing Ulasan E-Commerce",
    author=f"{NAMA} ({NIM})",
    subject="Tugas NLP - Preprocessing Teks Ulasan E-Commerce",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print("Laporan dibuat:", OUT_PATH)
print("Jumlah halaman dicek pada verifikasi.")
