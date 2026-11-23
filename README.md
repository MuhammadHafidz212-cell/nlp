# Preprocessing Teks Ulasan E-Commerce Bahasa Indonesia

**Nama:** Muhammad Hafidz
**NIM:** 24146028

## Deskripsi Project

Project ini melakukan preprocessing teks pada dataset ulasan produk e-commerce berbahasa Indonesia untuk analisis sentimen. Tujuannya adalah membersihkan dan menormalkan teks mentah agar siap dipakai pada tahap pemodelan NLP berikutnya.

**Dataset:** [dipawidia/ecommerce-product-reviews-sentiment](https://huggingface.co/datasets/dipawidia/ecommerce-product-reviews-sentiment) (Hugging Face)

## Tahapan yang Dilakukan

1. **Eksplorasi dataset**: jumlah data, nama kolom, dan distribusi label sentimen.
2. **Preprocessing teks**:
   - Case folding: mengubah teks menjadi huruf kecil.
   - Cleaning: menghapus URL, angka, tanda baca, dan karakter khusus.
   - Tokenisasi: memisahkan teks menjadi kata.
   - Stopword removal: menghapus kata yang tidak penting.
   - Stemming: mengubah kata menjadi bentuk dasar (Sastrawi).
3. **Perbandingan**: 10 contoh teks sebelum dan sesudah preprocessing.
4. **Analisis dampak**: pengaruh preprocessing terhadap kualitas data teks.

## Struktur Folder

```
preprocessing-ulasan-ecommerce-id/
├── preprocessing_ulasan.ipynb   # Notebook utama
├── data/
│   └── hasil_preprocessing.csv  # Hasil preprocessing
├── figures/                     # Grafik (jika ada)
├── laporan.pdf                  # Laporan (jika ada)
├── requirements.txt             # Daftar library
└── README.md
```

## Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/MuhammadHafidz212-cell/nlp.git
cd nlp
```

### 2. Buat virtual environment (disarankan)

Windows (Git Bash / CMD):

```bash
python -m venv venv
source venv/Scripts/activate      # Git Bash
# venv\Scripts\activate           # CMD / PowerShell
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependensi

```bash
pip install -r requirements.txt
```

Jika `requirements.txt` belum ada, install manual:

```bash
pip install datasets pandas matplotlib nltk Sastrawi jupyter
```

### 4. Jalankan notebook

```bash
jupyter notebook preprocessing_ulasan.ipynb
```

Lalu pilih **Kernel → Restart & Run All** agar seluruh sel dieksekusi berurutan.

> Catatan: proses stemming dengan Sastrawi cukup lambat pada data yang besar. Notebook ini memakai cache per kata unik untuk mempercepatnya.

## Library yang Digunakan

- `datasets` (Hugging Face): memuat dataset
- `pandas`: manipulasi data
- `matplotlib`: visualisasi
- `nltk`: tokenisasi dan stopword
- `Sastrawi`: stemming dan stopword bahasa Indonesia
- `jupyter`: menjalankan notebook

## Link

- Repository: https://github.com/MuhammadHafidz212-cell/nlp
- Dataset: https://huggingface.co/datasets/dipawidia/ecommerce-product-reviews-sentiment
