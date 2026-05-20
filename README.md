# SISTEM EVALUASI PDRB PROVINSI

## 1. Pendahuluan

Sistem Evaluasi PDRB Provinsi merupakan aplikasi berbasis Python yang dirancang untuk mendukung proses evaluasi data Produk Domestik Regional Bruto (PDRB) pada tingkat provinsi.

Aplikasi ini bertujuan untuk:

- Membantu proses evaluasi data secara sistematis dan terstandarisasi
- Mengidentifikasi nilai yang melewati batas evaluasi (threshold)
- Menghasilkan output evaluasi yang terstruktur
- Mendukung proses monitoring dan pengendalian kualitas data PDRB

Aplikasi dikembangkan menggunakan Python 3.10.11 dan dijalankan melalui Jupyter Notebook.

---

## 2. Ruang Lingkup

Sistem ini digunakan untuk Evaluasi PDRB Triwulanan. Evaluasi dilakukan berdasarkan aturan (rule) dan batas nilai (threshold) yang dapat disesuaikan sesuai kebutuhan analisis.

---

## 3. Struktur Direktori

Struktur direktori proyek adalah sebagai berikut:

```bash
evaluasi_pdrb_provinsi/
├── main.ipynb
├── data/
│   ├── input/
│   │   └── Export Semua Tabel Resume_olah.xlsx
│   └── output/
│       └── Evaluasi PDRB provinsi_<yyyy-mm-dd_hh.mm PM/AM>.xlsx
├── requirements.txt
└── README.md
```

Penjelasan:

- `main.ipynb`  
  Digunakan untuk evaluasi triwulanan.

- Folder `data/input/`  
  Digunakan untuk menyimpan file sumber dengan nama wajib: "Export Semua Tabel Resume_olah.xlsx"

- Folder `data/output/`  
  Digunakan untuk menyimpan hasil evaluasi yang dihasilkan sistem.  
  Output akan berupa file yang dinamai berdasarkan waktu evaluasi dilakukan.

---

## 4. Mekanisme Evaluasi

Untuk evaluasi triwulanan:

- Gunakan `main.ipynb`

Parameter threshold dapat diubah pada bagian konfigurasi awal notebook.

---

## 5. Spesifikasi Teknis

### 5.1 Versi Python

Aplikasi ini menggunakan: Python 3.10.11

Disarankan menggunakan versi yang sama untuk menghindari ketidaksesuaian dependency.

---

### 5.2 Library yang Digunakan

Library utama:

- pandas
- openpyxl

Library bawaan Python:

- os
- re

---

## 6. Instalasi dan Persiapan Lingkungan

### 6.1 Membuat Virtual Environment (Direkomendasikan)

```bash
python -m venv venv
```

Aktivasi environment:

- Windows:

```bash
venv\Scripts\activate
```

- Mac/Linux:

```bash
source venv/bin/activate
```

### 6.2 Instalasi Dependency

Install seluruh dependency yang dibutuhkan:

```bash
pip install -r requirements.txt
```

---

## 7. Prosedur Penggunaan

1. Pastikan folder data/input/ dan data/output/ tersedia.
2. Letakkan file sumber dengan nama: "Export Semua Tabel Resume_olah.xlsx"
3. Buka notebook: "main.ipynb"
4. Jalankan seluruh sel (Run All Cells).
5. Hasil evaluasi akan tersimpan secara otomatis pada folder: "data/output/"

---

## 8. Kustomisasi Parameter Evaluasi

Nilai threshold dan parameter evaluasi dapat disesuaikan pada bagian awal notebook.

Perubahan parameter harus dilakukan dengan memperhatikan:

- Konsistensi metodologi evaluasi
- Standar yang berlaku
- Dokumentasi perubahan (jika digunakan dalam konteks institusi)

---

## 9. Ketentuan dan Catatan Penting

- Nama file input wajib: "Export Semua Tabel Resume_olah.xlsx"
- Struktur dan format Excel harus sesuai template yang digunakan sistem
- Folder data/input/ dan data/output/ harus tersedia sebelum proses dijalankan
- Disarankan tidak mengubah struktur logika utama tanpa pemahaman teknis yang memadai

---

## 10. Penutup

Sistem ini dikembangkan untuk meningkatkan efisiensi, konsistensi, dan akuntabilitas dalam proses evaluasi data PDRB Kabupaten/Kota.

Pengembangan lanjutan dapat mencakup:

- Otomatisasi validasi data
- Integrasi dengan sistem basis data
- Pengembangan antarmuka pengguna (GUI/Web Interface)
