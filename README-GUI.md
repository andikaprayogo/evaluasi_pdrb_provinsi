# GUI Sistem Evaluasi PDRB Provinsi

GUI berbasis Streamlit untuk `main.ipynb`. Seluruh sel kode notebook dijalankan apa adanya
(tanpa menulis ulang aturan evaluasi); hanya lokasi file, nama sheet, dan periode yang diganti
pada salinan di memori. `main.ipynb` asli tidak diubah.

## Struktur

```text
evaluasi_pdrb_provinsi/
├── main.ipynb
├── app.py                 # tampilan Streamlit
├── engine.py              # penjalan notebook
├── requirements-gui.txt
└── data/output/
```

## Instalasi & menjalankan

```bash
python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate
pip install -r requirements-gui.txt
python -m streamlit run app.py
```

## Alur penggunaan

1. Unggah file Excel sumber (sheet 205, 209, 210, 211, 212, 213, 218, 219).
2. Periode dibaca otomatis dari header tabel; pilih periode yang dievaluasi (default: terbaru).
3. Klik **Jalankan Evaluasi**.
4. Telaah ringkasan/detail temuan, lalu unduh Excel hasil. Salinan juga ada di `data/output/`.

## Catatan

- Tidak memerlukan Jupyter/ipykernel; notebook dieksekusi langsung di proses Python aplikasi.
- Perubahan aturan/threshold tetap dilakukan di `main.ipynb`; GUI otomatis memakai versi terbaru.
- Jika sel notebook gagal, nomor sel dan pesan error ditampilkan di layar.
