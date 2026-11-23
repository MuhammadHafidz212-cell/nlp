# Preprocessing Teks Ulasan Produk E-Commerce (Bahasa Indonesia)

Repositori tugas mata kuliah **Pengolahan Bahasa Alami (NLP)** yang membangun pipeline
*preprocessing* teks ulasan produk e-commerce berbahasa Indonesia secara bertahap dan
terdokumentasi.

- **Nama:** Muhammad Hafidz
- **NIM:** 24146028
- **Repo GitHub:** https://github.com/MuhammadHafidz212-cell/nlp
- **Dataset:** [dipawidia/ecommerce-product-reviews-sentiment](https://huggingface.co/datasets/dipawidia/ecommerce-product-reviews-sentiment)

## Dataset

| Item | Keterangan |
|---|---|
| Sumber | Hugging Face: `dipawidia/ecommerce-product-reviews-sentiment` |
| Split | `train` |
| Jumlah data | 11.606 ulasan |
| Kolom | `review` (teks ulasan), `translate` (terjemahan), `sentimen` (label) |
| Label | `0` = negatif, `1` = positif |
| Distribusi label | negatif 5.803 (50,00%), positif 5.803 (50,00%) |
| Missing value | 0 pada semua kolom |
| Baris duplikat | 4 |

## Tujuan

1. Mengambil dan memeriksa dataset ulasan e-commerce secara langsung dari Hugging Face.
2. Melakukan *preprocessing* teks berbahasa Indonesia: case folding, cleaning, tokenisasi,
   stopword removal, dan stemming.
3. Menyimpan hasil tiap tahap sehingga proses dapat diaudit dan direproduksi.
4. Mengukur dampak preprocessing terhadap panjang teks, ukuran vocabulary, dan jumlah teks kosong.
5. Menyusun laporan PDF yang memuat identitas, dataset, metode, hasil, pembahasan, dan kesimpulan.

## Tahapan Preprocessing

1. **Case folding** - mengubah teks menjadi huruf kecil.
2. **Cleaning** - menghapus URL, tag HTML, angka, tanda baca, karakter khusus/emoji, serta merapikan spasi.
3. **Tokenisasi** - memecah teks menjadi token kata (NLTK, dengan fallback `split()`).
4. **Stopword removal** - membuang kata umum bahasa Indonesia memakai daftar stopword Sastrawi.
5. **Stemming** - mengubah kata berimbuhan menjadi kata dasar memakai Sastrawi (PySastrawi),
   dengan cache per kata unik.

Setiap tahap disimpan pada kolom tersendiri di `data/hasil_preprocessing.csv`:
`review`, `case_folding`, `cleaning`, `tokenisasi`, `stopword_removal`, `stemming`.

## Hasil Singkat

| Metrik | Sebelum | Sesudah |
|---|---|---|
| Rata-rata panjang karakter | 103,57 | 65,76 |
| Rata-rata panjang kata | 15,74 | 10,82 |
| Ukuran vocabulary (kata unik) | 12.558 | 10.036 |

- Penurunan vocabulary: **2.522 kata (20,08%)**.
- Teks kosong setelah preprocessing: **20 dari 11.606 (0,17%)**.
- Grafik distribusi label: `figures/distribusi_label.png`.

## Struktur Folder

```
preprocessing-ulasan-ecommerce-id/
├── preprocessing_ulasan.ipynb     # notebook utama (sudah dieksekusi, output tersimpan)
├── README.md
├── requirements.txt
├── laporan.pdf                    # laporan akhir
├── scripts/
│   └── buat_laporan.py            # generator laporan PDF dari statistik.json + CSV
├── data/
│   ├── hasil_preprocessing.csv    # hasil semua tahap preprocessing
│   └── statistik.json             # angka statistik & contoh (sumber tunggal laporan)
└── figures/
    └── distribusi_label.png       # bar chart distribusi label
```

## Cara Menjalankan

```bash
git clone https://github.com/MuhammadHafidz212-cell/nlp.git
cd nlp

python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
jupyter notebook
```

Buka `preprocessing_ulasan.ipynb` lalu jalankan semua sel dari atas ke bawah.
Alternatif non-interaktif:

```bash
jupyter nbconvert --to notebook --execute --inplace preprocessing_ulasan.ipynb
python scripts/buat_laporan.py
```

Catatan: notebook mengunduh dataset dari Hugging Face sehingga membutuhkan koneksi internet
saat pertama kali dijalankan. Paket **PySastrawi** digunakan karena API-nya kompatibel dengan
`Sastrawi` (`import Sastrawi`) tetapi jauh lebih cepat pada Python 3.13.

## Output

- `data/hasil_preprocessing.csv` - seluruh data dengan kolom hasil setiap tahap.
- `data/statistik.json` - jumlah data, tipe kolom, distribusi label, 10 contoh, dan statistik dampak.
- `figures/distribusi_label.png` - visualisasi distribusi label sentimen.
- `laporan.pdf` - laporan bahasa Indonesia yang dibangun dari `statistik.json` dan CSV di atas.

---

Muhammad Hafidz - 24146028
