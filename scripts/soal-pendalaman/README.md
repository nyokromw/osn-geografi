# Generator Soal Pendalaman Materi

Skrip untuk membangun 6 paket × 10 soal per bab (13 bab) beserta gambar.

- `figlib.py` — helper grafik/peta (matplotlib). Peta memakai GeoJSON Natural Earth di folder `geo/`
  (`countries50.geojson`, `idn_prov.geojson`; unduh dari github.com/nvkelso/natural-earth-vector).
- `chNN.py` — isi soal bab NN (`PAKETS` = [Gratis, 01..05]); opsi pertama selalu kunci.
- `build.py NN [--upload] [--push]` — render gambar, acak posisi kunci (tiap huruf A–E tepat 2× per paket),
  cek panjang opsi, unggah gambar ke bucket `soal-images/pendalaman/v2/`, dan perbarui tabel `soal_pendalaman`.
- `sheet.py` — lembar kontak untuk memeriksa gambar.

Butuh: `pip install matplotlib numpy pillow`. Update DB butuh kredensial yang berhak menulis.
