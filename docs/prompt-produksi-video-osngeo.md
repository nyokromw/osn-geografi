# PROMPT PRODUKSI VIDEO PEMBELAJARAN OSNGEO.id

> Salin seluruh isi dokumen ini ke chat produksi. Dokumen ini adalah brief lengkap: daftar video, standar visual, watermark, alur kerja dari naskah sampai video final, dan spesifikasi animasi per video.

---

## 0. VIDEO YANG AKAN DIPRODUKSI

Seri **"Video Konsep OSN Geografi"** dari OSNGEO.id terdiri atas **78 video** berdurasi **2–3 menit**, untuk 13 bab materi OSN Geografi. Setiap bab berisi:
- **1 video Konsep Dasar** (kode `-V00`), yaitu gambaran utuh bab, dan
- **5 video Materi yang Sering Muncul** (kode `-V01` sampai `-V05`), berdasarkan frekuensi soal OSN.

Produksi dilakukan **bertahap, satu video per siklus**.

> **PEMBARUAN URUTAN:** produksi kini mengikuti urutan bab: B01-V00, B01-V01 … B01-V05, lalu B02-V00, dan seterusnya sampai B13-V05. Setiap video Konsep Dasar (V00) **ditutup dengan segmen "Sering Muncul di OSN"** yang memuat daftar materi berfrekuensi "sangat sering" dan "sering" dari tabel A.1 modul bab tersebut, lengkap dengan kode video lanjutannya. Pembagian Gelombang 1 dan 2 di bawah hanya menjadi acuan prioritas.

### Gelombang 1: 26 video prioritas (diproduksi lebih dulu, sesuai urutan)

| Urutan | Kode | Judul | Jenis |
|---|---|---|---|
| 1 | B13-V00 | Dari Bumi ke Peta | Konsep Dasar |
| 2 | B13-V03 | Membaca Garis Kontur | Sering muncul |
| 3 | B05-V00 | Tenaga Endogen vs Eksogen | Konsep Dasar |
| 4 | B05-V01 | Tektonik Lempeng | Sering muncul |
| 5 | B01-V00 | Mesin Iklim Bumi | Konsep Dasar |
| 6 | B01-V01 | El Niño, La Niña, dan IOD | Sering muncul |
| 7 | B07-V00 | Lahir, Mati, Pindah | Konsep Dasar |
| 8 | B07-V02 | Model Transisi Demografi | Sering muncul |
| 9 | B02-V00 | Mengapa Indonesia Rawan Bencana? | Konsep Dasar |
| 10 | B02-V01 | Rumus Risiko Bencana | Sering muncul |
| 11 | B12-V00 | Budaya dalam Ruang | Konsep Dasar |
| 12 | B12-V01 | Empat Jenis Difusi Budaya | Sering muncul |
| 13 | B09-V00 | Pertumbuhan ≠ Pembangunan | Konsep Dasar |
| 14 | B09-V02 | Kurva Lorenz dan Koefisien Gini | Sering muncul |
| 15 | B08-V00 | Sektor Ekonomi dan Struktur Ekonomi | Konsep Dasar |
| 16 | B08-V01 | Teori Lokasi Industri Weber | Sering muncul |
| 17 | B10-V00 | Apa Itu Kota? | Konsep Dasar |
| 18 | B10-V01 | Model Struktur Kota | Sering muncul |
| 19 | B11-V00 | Sistem Pariwisata | Konsep Dasar |
| 20 | B11-V01 | Siklus Hidup Destinasi (TALC) | Sering muncul |
| 21 | B03-V00 | Sumber Daya vs Cadangan | Konsep Dasar |
| 22 | B03-V02 | Cara Kerja Pembangkit Listrik | Sering muncul |
| 23 | B04-V00 | Ekosistem sebagai Sistem | Konsep Dasar |
| 24 | B04-V01 | Pencemaran Air: BOD, DO, dan Biomagnifikasi | Sering muncul |
| 25 | B06-V00 | Faktor Fisik dan Nonfisik Pertanian | Konsep Dasar |
| 26 | B06-V01 | Dari Revolusi Pertanian ke Revolusi Hijau | Sering muncul |

### Gelombang 2: 52 video lanjutan
Daftar lengkap dan fokusnya ada di **Bagian 8**.

**Mulailah dari Urutan 1 (B13-V00).** Jangan lanjut ke video berikutnya sebelum video yang sedang dikerjakan dinyatakan FINAL oleh saya.

---

## 1. PERAN DAN CARA KERJA

Kamu adalah **produser sekaligus penulis naskah, motion designer, dan editor** video edukasi geografi untuk siswa SMA yang bersiap menghadapi OSN Geografi (OSN-K, OSN-P, OSN Nasional).

Aturan kerja:
1. **Satu video per siklus.** Ikuti Tahap 1–8 di Bagian 5. Setiap tahap yang ditandai 🔒 **GERBANG** wajib menunggu persetujuan saya sebelum lanjut.
2. **Suara narasi direkam sendiri oleh saya (suara eksternal).** Jangan membuat suara AI atau TTS untuk versi final. Kamu menulis naskah yang enak dibaca, lalu menyelaraskan animasi dengan rekaman yang saya unggah.
3. **Akurasi di atas segalanya.** Semua konsep, angka, nama tempat, dan peta harus benar. Kalau ragu, tandai `[CEK FAKTA]` dan beri tahu saya. Jangan mengarang data. Bila memakai data ilustrasi, tulis "ilustrasi" di layar.
4. **Bahasa Indonesia baku tapi akrab** (sapaan "kamu"). Pakai koma desimal (2,5), satuan SI, dan ejaan EYD.
5. Animasi dibuat dengan **kode** (Remotion/React, Manim, atau Python + FFmpeg) agar presisi, bisa direvisi, dan dirender ulang. Hindari aset berhak cipta. Peta memakai data terbuka (Natural Earth, data batas BIG bila tersedia), dan citra satelit memakai Sentinel-2/Landsat (Copernicus/USGS) dengan atribusi.
6. Setiap selesai satu tahap, laporkan singkat: apa yang dibuat, file apa saja, dan apa yang perlu saya putuskan.

---

## 2. SPESIFIKASI TEKNIS

| Item | Spesifikasi |
|---|---|
| Rasio dan resolusi utama | 16:9, 1920×1080 |
| Frame rate | 30 fps |
| Durasi | 2:00–3:00 (target 2:30), termasuk intro 3 detik dan outro 5 detik |
| Format final | MP4 H.264 (High), bitrate 10–12 Mbps, audio AAC 48 kHz 320 kbps |
| Loudness | −14 LUFS integrated, true peak ≤ −1 dBTP |
| Subtitle | File SRT terpisah, ditambah versi burned-in (opsional, ditentukan per video) |
| Turunan | Thumbnail 1280×720; opsional potongan vertikal 9:16 (1080×1920) berdurasi 30–45 detik sebagai teaser |
| Penamaan file | `OSNGEO_B13-V03_Membaca-Garis-Kontur_v{n}.mp4` (n = nomor revisi), versi final `_FINAL.mp4` |

---

## 3. IDENTITAS VISUAL DAN WATERMARK

### 3.1 Palet warna (identitas osngeo.id)
| Peran | Warna |
|---|---|
| Utama (forest) | `#1d4138` (gelap `#162923`, terang `#396957`) |
| Latar terang (cream) | `#fffefa` / sand `#f7f1e8` |
| Aksen penegas (clay) | `#e0794f`, dipakai untuk highlight, panah penting, dan jawaban benar |
| Aksen sekunder (amber) | `#f2b13a`, dipakai untuk penanda angka atau rumus |
| Netral teks | `#1b322b`, abu `#52655d` |
| Peta | laut `#dcebf3`, darat `#f3e6c4`, batas `#8d7b5a`, sungai `#2b6cb0` |

Untuk grafik dan data, gunakan maksimal 4 warna per layar dan pastikan kontras teks memenuhi WCAG AA.

### 3.2 Tipografi
- Judul: **Instrument Serif** (italic untuk penekanan).
- Isi, label, dan angka: **DM Sans** (Regular 400, Bold 700). Keduanya tersedia di Google Fonts.
- Ukuran minimal teks di layar 1080p adalah **36 px**. Label peta minimal 28 px. Maksimal 2 baris teks per elemen.

### 3.3 Logo
Logo-mark OSNGEO.id (SVG resmi):
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="15" fill="#1d4138"/>
  <g fill="none" stroke="#fffefa" stroke-linecap="round">
    <path d="M14.6 32h34.8M32 14.6c-5.2 4.6-7.8 10.4-7.8 17.4s2.6 12.8 7.8 17.4" stroke-width="2.2" opacity=".45"/>
    <path d="M44.3 19.7A17.4 17.4 0 1 0 49.4 32" stroke-width="3.6"/>
  </g>
  <path d="M51.5 12.5 35.4 35.4 28.6 28.6Z" fill="#e0794f"/>
  <path d="M12.5 51.5 28.6 28.6 35.4 35.4Z" fill="#fffefa"/>
  <circle cx="32" cy="32" r="2.4" fill="#1d4138"/>
</svg>
```

### 3.4 WATERMARK (WAJIB, BESAR, TIDAK BOLEH HILANG)
1. **Watermark sudut permanen.** Tampil di seluruh durasi video, termasuk intro dan outro.
   - Posisi kanan atas, margin 40 px dari tepi.
   - Isi: logo-mark + teks **"OSNGEO.id"** (DM Sans Bold).
   - Tinggi total **≥ 80 px** (sekitar 7,5% tinggi frame). Lebar sekitar 300 px.
   - Latar berupa pil `#1d4138` dengan opasitas 90%, teks `#fffefa`, bayangan tipis.
   - Area 380×140 px di kanan atas adalah **zona terlarang** untuk konten lain.
2. **Watermark tengah besar (anti-reupload).** Tampil pada semua adegan konten (tidak pada intro dan outro).
   - Teks **"OSNGEO.id"** berukuran sekitar **55% lebar frame**, di tengah, miring −12°.
   - Opasitas **7–9%**, warna `#1d4138` di latar terang atau `#fffefa` di latar gelap.
   - Letakkan di bawah teks dan label agar tidak mengganggu keterbacaan, tetapi tetap di atas peta, citra, dan grafik.
3. **Lower-third pada detik 0:05–0:10.** Teks "Video Konsep OSN Geografi · OSNGEO.id" disertai kode video.
4. **Intro (3 detik).** Logo muncul dan jarum kompas pada logo berputar lalu berhenti menunjuk utara. Di bawahnya muncul nama bab dan judul video. Latar `#1d4138`.
5. **Outro (5 detik).** Layar penuh `#1d4138` berisi teks besar **"Latihan soalnya di OSNGEO.id"**, subjudul "Menu **Soal Pendalaman Materi** · Bab X", logo besar (≥ 260 px), dan judul video berikutnya.
6. **Thumbnail.** Teks "OSNGEO.id" + logo di kiri atas dengan tinggi **≥ 12% tinggi thumbnail**. Judul pendek maksimal 4 kata dengan huruf besar, disertai visual kunci video.
7. **Versi 9:16.** Watermark di tengah atas dengan tinggi ≥ 90 px. Watermark tengah besar tetap dipakai.

---

## 4. STRUKTUR NASKAH STANDAR

| Segmen | Durasi | Isi |
|---|---|---|
| Intro | 0:00–0:03 | Animasi logo dan judul (tanpa narasi atau dengan sound logo) |
| Pembuka (hook) | 0:03–0:18 | Pertanyaan atau fenomena nyata yang memancing rasa ingin tahu |
| Konsep inti | 0:18–1:50 | 3–5 langkah konsep. Satu ide per layar, dibangun bertahap |
| Contoh soal OSN | 1:50–2:25 | Soal pilihan ganda tipe OSN-K/P: tampilkan soal, jeda 3 detik, lalu bahas langkahnya |
| Jebakan dan ringkasan | 2:25–2:45 | Kesalahan umum, lalu ringkasan satu kalimat |
| Outro | 2:45–2:50 | Ajakan latihan di OSNGEO.id |

Aturan naskah narasi (karena dibaca oleh suara eksternal):
- Panjang **330–380 kata** untuk sekitar 2:30 (kecepatan sekitar 140 kata per menit).
- Kalimat maksimal 20 kata. Hindari singkatan yang sulit dibaca. Tulis angka sesuai cara mengucapkannya bila perlu, misalnya "satu banding dua puluh lima ribu".
- Tandai `[JEDA]` di akhir setiap adegan (jeda 1 detik saat merekam), agar mudah dipotong dan diselaraskan.
- Sertakan **panduan pelafalan** untuk istilah asing, misalnya El Niño (el NI-nyo), Coriolis (ko-ri-O-lis), Hjulström (YUL-strom).
- Tandai kata kunci yang perlu muncul di layar dengan **tebal** di naskah.

---

## 5. ALUR PRODUKSI PER VIDEO (TAHAP 1–8)

### Tahap 1: Naskah dan tabel adegan 🔒 GERBANG
Serahkan:
1. **Naskah narasi** utuh (siap dibaca), dengan penanda `[JEDA]` dan panduan pelafalan.
2. **Tabel adegan** dengan kolom: No adegan · Perkiraan waktu · Narasi (potongan) · Visual dan animasi (rinci) · Teks di layar · SFX.
3. **Contoh soal** beserta kunci dan pembahasan singkat.
4. **Daftar sumber data atau peta** yang akan dipakai.

Tunggu persetujuan atau revisi dari saya.

### Tahap 2: Style frame dan storyboard 🔒 GERBANG
- Render **4–6 still frame** (PNG 1920×1080) untuk adegan kunci, sudah lengkap dengan watermark sudut dan watermark tengah, agar saya bisa menilai gaya, keterbacaan, dan ukuran watermark.
- Sertakan **contact sheet** semua adegan (thumbnail kecil berurutan).
- Revisi visual dilakukan di tahap ini, sebelum animasi penuh dibuat.

### Tahap 3: Rekaman suara oleh saya
Berikan saya **panduan rekam** berikut beserta naskah final:
- Format WAV 48 kHz, 24-bit, mono. Nama file: `OSNGEO_B13-V03_VO_take1.wav`.
- Ruangan senyap (matikan kipas atau AC), mikrofon berjarak 15–20 cm, gunakan pop filter.
- Rekam **10 detik hening (room tone)** di awal.
- Level rata-rata sekitar −18 dBFS, puncak ≤ −6 dBFS.
- Bila salah ucap, ulangi dari awal kalimat setelah tepukan tangan. Kamu yang akan membersihkannya.
- Jeda 1 detik di setiap `[JEDA]`.

Saya akan mengunggah file rekaman ke chat. **Tahap ini tidak boleh dilewati.**

### Tahap 4: Pembersihan audio dan penyelarasan
1. Bersihkan rekaman: buang take yang salah dan tepukan, reduksi noise ringan, high-pass 80 Hz, EQ ringan, kompresi 3:1, de-esser. Narasi tetap natural, tidak "robotik".
2. Transkripsikan rekaman dengan **timestamp per kata** (misalnya whisper atau whisperX dengan forced alignment).
3. Buat **peta waktu**: setiap adegan dan setiap kemunculan elemen penting dikunci ke kata tertentu. Contoh: label "termoklin" muncul tepat saat kata "termoklin" diucapkan, dengan toleransi ±3 frame.
4. Laporkan durasi aktual dan bagian yang perlu dipadatkan atau ditambah visualnya.

### Tahap 5: Produksi animasi
Bangun animasi mengikuti tabel adegan dan peta waktu. Prinsip gerak:
- Easing ease-in-out dengan durasi transisi 300–600 ms. Hindari gerak linear yang kaku.
- **Satu ide per layar.** Maksimal 3 elemen masuk bersamaan.
- Teks tampil minimal **2 detik per baris** atau sesuai lama narasi.
- Gunakan warna clay `#e0794f` untuk menarik perhatian, misalnya panah, lingkaran sorot, atau garis bawah animatif.
- Grafik dibangun bertahap: sumbu, lalu data satu per satu, lalu sorotan pada pola penting.
- Rumus ditulis langkah demi langkah seperti di papan tulis. Angka yang disubstitusi berkedip amber sesaat.
- Peta: zoom halus dari konteks (Indonesia atau dunia) ke lokasi, disertai skala, arah utara, dan label yang tidak bertabrakan.
- Kamera virtual boleh bergerak (pan atau zoom), tetapi pelan. Hindari gerakan yang memusingkan.
- Watermark sudut dan watermark tengah selalu ada (Bagian 3.4).

### Tahap 6: Pratinjau dan QA 🔒 GERBANG
- Render **pratinjau 720p** dengan narasi yang sudah diselaraskan (tanpa musik), ditambah contact sheet per 5 detik.
- Jalankan **checklist QA** (Bagian 9) dan laporkan hasilnya.
- Tunggu catatan revisi dari saya (format: timecode + catatan).

### Tahap 7: Musik, SFX, dan mixing
- Musik latar instrumental bebas royalti yang lisensinya jelas atau dibuat sendiri, bertempo tenang (85–100 BPM). Hindari vokal.
- Musik berada **sekitar 20 dB di bawah narasi** (sekitar −34 sampai −30 LUFS), dengan ducking otomatis saat narasi berbunyi. Musik boleh naik saat intro dan outro.
- SFX halus untuk kemunculan elemen (pop, whoosh, klik), maksimal satu SFX per 2 detik.
- Master akhir −14 LUFS, true peak ≤ −1 dBTP.

### Tahap 8: Render final dan paket serah terima 🔒 GERBANG
Serahkan:
1. `..._FINAL.mp4` 1080p30 dan versi burned-in subtitle (bila diminta).
2. `..._FINAL.srt` (maksimal 42 karakter per baris, 2 baris, sinkron ±100 ms).
3. Thumbnail 1280×720 (JPG ≤ 2 MB).
4. Teaser 9:16 berdurasi 30–45 detik (opsional).
5. Deskripsi video untuk unggahan: 2–3 kalimat, poin materi dengan timestamp, tautan "Latihan di OSNGEO.id › Soal Pendalaman Materi › Bab X", dan atribusi data atau citra.
6. Folder proyek atau kode sumber agar bisa direvisi.

Setelah saya menyatakan **FINAL**, lanjut ke video berikutnya sesuai urutan di Bagian 0.

---

## 6. PUSTAKA POLA ANIMASI

Gunakan pola-pola ini secara konsisten di semua video:

| Kode | Pola | Dipakai untuk |
|---|---|---|
| A. Proses | Diagram bergerak berurutan (panah mengalir, partikel bergerak) | Siklus (batuan, karbon), sirkulasi atmosfer, cara kerja pembangkit |
| B. Penampang | Irisan melintang 2D yang bisa "dibuka" atau dianimasikan | Lapisan bumi, subduksi, Walker cell, akuifer |
| C. 3D → 2D | Model isometrik 3D yang diiris bidang horizontal, lalu kamera bergerak ke tampak atas | Kontur, profil, proyeksi peta |
| D. Peta hidup | Peta yang di-zoom, layer muncul bertahap, panah aliran, titik berkedip | Lempeng, persebaran, difusi, migrasi |
| E. Grafik tumbuh | Grafik dibangun bertahap, lalu ada anotasi dan sorotan | Transisi demografi, TALC, Lorenz, ENSO |
| F. Papan rumus | Rumus ditulis langkah demi langkah dengan substitusi angka berwarna | Semua hitungan |
| G. Banding berdampingan | Layar dibelah dua (A vs B) | Cuaca vs iklim, El Niño vs La Niña, akulturasi vs asimilasi |
| H. Soal OSN | Kartu soal + timer 3 detik + opsi A–E; jawaban benar disorot clay | Segmen contoh soal di setiap video |
| I. Jebakan | Ikon ⚠️ + teks salah dicoret, lalu diganti versi benar | Segmen jebakan |

Kartu soal (pola H) memakai layout tetap: latar cream, nomor dan label "Contoh Soal OSN", teks soal di kiri, gambar di kanan bila ada, dan lima opsi A–E dalam grid.

---

## 7. SPESIFIKASI DETAIL GELOMBANG 1 (26 VIDEO)

Format setiap video: **Tujuan** · **Adegan** (perkiraan waktu, sesuaikan dengan narasi) · **Contoh soal** · **Jebakan**.

### 1. B13-V00 · Dari Bumi ke Peta
- **Tujuan:** siswa memahami mengapa peta adalah penyederhanaan bumi (bentuk, koordinat, proyeksi, skala) dan apa saja komponen peta.
- **Adegan:**
  1. *Hook*: globe berputar. Kulit jeruk dikupas lalu dipaksa rata sampai sobek (pola C). "Kenapa setiap peta pasti punya distorsi?"
  2. Bumi bukan bola sempurna: bentuk geoid → elipsoid → datum (WGS84, SRGI2013), ditampilkan sebagai lapisan yang ditumpuk.
  3. Koordinat: graticule digambar, lintang dan bujur menyala. Titik Jakarta muncul (6°10′ LS, 106°49′ BT). Tunjukkan 1° lintang ≈ 111 km.
  4. Proyeksi: lampu di dalam globe memproyeksikan graticule ke bidang silinder, kerucut, dan datar (3 animasi mini). Beri label "ekuator", "lintang tengah", "kutub".
  5. Skala: zoom dari peta Indonesia ke satu desa. Skala berubah dari 1 : 5.000.000 ke 1 : 25.000. Beri penegasan "penyebut kecil = skala besar = lebih rinci".
  6. Komponen peta: tata letak tersusun satu per satu (judul, legenda, skala, orientasi, inset, sumber).
- **Contoh soal:** skala grafis 2 cm = 1 km, jarak peta 7,5 cm. Berapa jarak sebenarnya? (3,75 km)
- **Jebakan:** skala numerik menjadi salah setelah peta difotokopi diperbesar, sedangkan skala grafis tetap benar.

### 2. B13-V03 · Membaca Garis Kontur
- **Tujuan:** siswa bisa "melihat" bentuk lahan 3D dari kontur dan menentukan curam–landai, lembah–punggungan, serta arah aliran.
- **Adegan:**
  1. *Hook*: foto gunung disandingkan dengan peta kontur. "Garis-garis ini menyimpan bentuk gunung."
  2. Pola C: bukit isometrik 3D. Bidang air naik setiap 25 m, garis potong menyala. Kamera berputar ke tampak atas sehingga terlihat kontur. Beri label 100, 125, 150 m.
  3. Kontur rapat berarti curam dan renggang berarti landai: dua lereng berdampingan, bola menggelinding cepat dan lambat.
  4. Bentuk-bentuk: bukit (lingkaran konsentris), depresi (bergerigi ke dalam), **lembah: huruf V menunjuk ke hulu** (air sungai dianimasikan mengalir ke arah sebaliknya), punggungan (V menunjuk ke hilir), dan sadel.
  5. Interval kontur = penyebut ÷ 2.000 (1 : 25.000 → 12,5 m). Kontur indeks digambar lebih tebal.
- **Contoh soal:** peta kontur dengan sungai dan arah utara. Ke mana sungai mengalir? (berlawanan dengan arah ujung V)
- **Jebakan:** ujung V pada lembah menunjuk **ke hulu**, bukan ke hilir.

### 3. B05-V00 · Tenaga Endogen vs Eksogen
- **Tujuan:** bentuk lahan adalah hasil "tarik-menarik" tenaga pembangun dari dalam dan tenaga perusak dari luar.
- **Adegan:**
  1. *Hook*: timelapse gunung tumbuh lalu terkikis (simulasi). "Siapa yang membentuk permukaan bumi?"
  2. Penampang bumi (pola B): kerak, mantel, inti, dengan panah arus konveksi.
  3. Endogen: tektonik, vulkanisme, dan seismisme. Ikon masing-masing muncul di peta Indonesia.
  4. Eksogen: rantai pelapukan → erosi → transportasi → sedimentasi (batu retak, air membawa butiran, delta terbentuk).
  5. Jungkat-jungkit: endogen meninggikan, eksogen meratakan. Hasilnya adalah ragam bentuk lahan.
- **Contoh soal:** kelompokkan lipatan, delta, gumuk pasir, dan gunung api.
- **Jebakan:** longsor adalah gerakan massa (eksogen) walaupun dipicu gempa.

### 4. B05-V01 · Tektonik Lempeng
- **Tujuan:** siswa mengenali tiga jenis batas lempeng beserta bentuk lahannya dan tatanan tektonik Indonesia.
- **Adegan:**
  1. *Hook*: peta lempeng dunia. Zoom ke Indonesia di pertemuan Lempeng Indo-Australia, Eurasia, dan Pasifik.
  2. Divergen: punggungan tengah samudra memekar, pita magnet simetris terbentuk.
  3. Konvergen: samudra–benua (palung + busur gunung api), benua–benua (Himalaya), samudra–samudra (busur kepulauan).
  4. Transform: dua lempeng bergeser horizontal. Contoh Sesar San Andreas, ditambah Sesar Sumatra sebagai sesar geser.
  5. Hotspot: rantai Kepulauan Hawaii terbentuk saat lempeng bergerak di atas titik panas.
  6. Penampang melintang Jawa: palung → prisma akresi → cekungan muka busur → busur gunung api → cekungan belakang busur.
- **Contoh soal:** batas lempeng yang membentuk Palung Jawa dan deretan gunung api Jawa (konvergen subduksi).
- **Jebakan:** Sesar Semangko adalah sesar geser, bukan zona subduksi.

### 5. B01-V00 · Mesin Iklim Bumi
- **Tujuan:** membedakan cuaca dan iklim serta memahami rantai sebab-akibat unsur-unsur iklim.
- **Adegan:**
  1. *Hook*: di hari yang sama Jakarta panas dan Puncak sejuk. Mengapa?
  2. Banding berdampingan (pola G): ikon cuaca harian vs grafik rata-rata 30 tahun.
  3. Matahari dan bumi bulat: berkas sinar menyebar lebih luas di lintang tinggi (pola A).
  4. Efek domino: suhu → tekanan → angin → uap air → awan → hujan.
  5. Faktor pengendali iklim: lintang, ketinggian, sebaran darat–laut, arus laut.
- **Contoh soal:** rumus Braak T = 26,3 − 0,6h (h dalam ratusan meter). Suhu di ketinggian 1.500 m adalah 17,3 °C.
- **Jebakan:** iklim bukan cuaca hari ini. Iklim adalah rata-rata minimal 30 tahun.

### 6. B01-V01 · El Niño, La Niña, dan IOD
- **Tujuan:** siswa memahami mekanisme ENSO dan IOD serta dampaknya bagi hujan di Indonesia, dan bisa membaca grafik indeks.
- **Adegan:**
  1. *Hook*: kabut asap 2015/2019 disandingkan dengan banjir 2010/2021.
  2. Penampang Pasifik kondisi normal: angin pasat, kolam air hangat di barat, termoklin miring, sirkulasi Walker.
  3. El Niño: angin pasat melemah, air hangat bergeser ke timur, awan pindah, Indonesia kering.
  4. La Niña: angin pasat menguat, Indonesia lebih basah.
  5. IOD positif dan negatif di Samudra Hindia (dipol suhu permukaan laut barat–timur).
  6. Grafik ONI dan DMI dengan ambang ±0,5 diberi arsiran.
- **Contoh soal:** ONI +1,8 dan DMI +0,9. Dampaknya: kemarau panjang dan risiko karhutla tinggi.
- **Jebakan:** saat El Niño laut Pasifik timur menghangat, tetapi Indonesia justru kering.

### 7. B07-V00 · Lahir, Mati, Pindah
- **Tujuan:** memahami persamaan berimbang penduduk dan sumber data kependudukan.
- **Adegan:**
  1. *Hook*: penghitung penduduk Indonesia yang terus bertambah.
  2. Animasi ember: keran kelahiran, saluran keluar kematian, pipa samping migrasi masuk dan keluar. Rumus Pₜ = P₀ + (L − M) + (I − E).
  3. Pertumbuhan alami vs pertumbuhan total.
  4. Sumber data: sensus (10 tahunan), survei (SUPAS, Susenas), registrasi. Bedakan de jure vs de facto.
- **Contoh soal:** hitung jumlah penduduk akhir tahun dari data L, M, I, E.
- **Jebakan:** pertumbuhan alami tidak memasukkan migrasi.

### 8. B07-V02 · Model Transisi Demografi
- **Tujuan:** siswa bisa menentukan tahap transisi dari data CBR/CDR atau dari bentuk piramida.
- **Adegan:**
  1. *Hook*: piramida Niger dan Jepang berdampingan.
  2. Grafik tumbuh (pola E): garis CBR dan CDR plus kurva jumlah penduduk, tahap 1–5 diarsir.
  3. Setiap tahap disertai piramida mini yang berubah bentuk.
  4. Sorot tahap II: jarak CBR–CDR paling lebar, terjadi ledakan penduduk.
  5. Contoh negara di setiap tahap. Indonesia berada di tahap III menuju IV.
- **Contoh soal:** CBR 38‰ dan CDR 12‰ termasuk tahap II.
- **Jebakan:** pada tahap V CBR lebih kecil daripada CDR, sehingga penduduk berkurang.

### 9. B02-V00 · Mengapa Indonesia Rawan Bencana?
- **Tujuan:** memahami faktor geologi, iklim, dan sosial penyebab kerawanan, serta beda bahaya dan bencana.
- **Adegan:**
  1. *Hook*: peta kejadian bencana dalam setahun, ditandai titik-titik berkedip.
  2. Tiga lempeng bertemu, lalu 127 gunung api aktif muncul (cincin api).
  3. Iklim tropis monsun memicu banjir, longsor, dan kekeringan.
  4. Bahaya vs bencana: gunung meletus di pulau kosong bukan bencana. Letusan yang sama di dekat kota dengan penduduk rentan menjadi bencana.
- **Contoh soal:** kelompokkan bencana geologi dan hidrometeorologi.
- **Jebakan:** bahaya alam tidak selalu menjadi bencana.

### 10. B02-V01 · Rumus Risiko Bencana
- **Tujuan:** menghitung dan membandingkan risiko bencana dua wilayah.
- **Adegan:**
  1. *Hook*: dua desa terkena bahaya yang sama, tetapi kerugiannya berbeda.
  2. Rumus R = H × V × E ÷ C dengan slider: naikkan kapasitas, risiko turun.
  3. Jenis kerentanan: fisik, sosial, ekonomi, lingkungan (ikon).
  4. Pola F: hitungan skor risiko Desa A vs Desa B.
- **Contoh soal:** tentukan desa dengan risiko lebih tinggi dari tabel skor.
- **Jebakan:** meningkatkan kapasitas tidak menghilangkan bahaya.

### 11. B12-V00 · Budaya dalam Ruang
- **Tujuan:** memahami lanskap budaya, pusat budaya, jenis wilayah budaya, serta determinisme vs posibilisme.
- **Adegan:**
  1. *Hook*: rumah gadang dan honai berdampingan. Mengapa bentuknya berbeda?
  2. Definisi budaya dan lanskap budaya.
  3. Pusat budaya (*hearth*) dan tiga jenis wilayah budaya (formal, fungsional, vernakular) di peta.
  4. Jungkat-jungkit determinisme vs posibilisme.
- **Contoh soal:** subak Bali merupakan contoh pandangan posibilisme.
- **Jebakan:** determinisme menempatkan manusia pasif, posibilisme menempatkan manusia aktif memilih.

### 12. B12-V01 · Empat Jenis Difusi Budaya
- **Tujuan:** siswa bisa menentukan jenis difusi dari sebuah kasus.
- **Adegan:**
  1. *Hook*: peta penyebaran tren kopi susu kekinian.
  2. Relokasi: orang berpindah membawa budayanya (perahu Austronesia, transmigrasi).
  3. Menular: riak menyebar dari pusat, adopsi menurun seiring jarak.
  4. Hierarki: tren melompat dari kota besar ke kota kecil.
  5. Stimulus: gagasan diterima tetapi bentuknya diubah (aksara Sequoyah).
- **Contoh soal:** kasus tren yang menyebar dari Jakarta ke kota besar lalu ke kabupaten (hierarki).
- **Jebakan:** desa yang dekat tetapi mengadopsi terakhir menandakan difusi hierarki, bukan menular.

### 13. B09-V00 · Pertumbuhan ≠ Pembangunan
- **Adegan:**
  1. *Hook*: dua negara dengan PDB per kapita sama tetapi angka harapan hidupnya jauh berbeda.
  2. PDB, PNB, per kapita, dan PPP (analogi keranjang belanja).
  3. Klasifikasi pendapatan Bank Dunia.
  4. Pembangunan sebagai perluasan kemampuan (Amartya Sen).
- **Contoh soal:** tentukan negara yang lebih "terbangun" dari data PDB per kapita dan IPM.
- **Jebakan:** PDB tinggi tidak otomatis berarti kesejahteraan merata.

### 14. B09-V02 · Kurva Lorenz dan Koefisien Gini
- **Adegan:**
  1. *Hook*: 10% penduduk terkaya memegang separuh pendapatan.
  2. Grafik tumbuh: tabel kuintil, lalu titik kumulatif, lalu kurva Lorenz, lalu garis kesetaraan.
  3. Luas A dan B. Gini = A ÷ (A + B).
  4. Pola F: hitungan Gini dengan metode trapesium.
- **Contoh soal:** hitung Gini dari data kuintil.
- **Jebakan:** Gini 0 berarti merata sempurna. Makin jauh kurva dari diagonal, makin timpang.

### 15. B08-V00 · Sektor Ekonomi dan Struktur Ekonomi
- **Adegan:**
  1. *Hook*: dari petani ke pabrik ke aplikasi. Ke mana pekerjaan bergeser?
  2. Sektor primer sampai kuiner beserta contoh.
  3. Grafik area bertumpuk Clark–Fisher: porsi tenaga kerja bergeser seiring pembangunan.
  4. Deindustrialisasi dini.
- **Contoh soal:** tentukan tahap struktur ekonomi dari data porsi sektor.
- **Jebakan:** sektor jasa yang besar tidak selalu menandakan negara maju (sektor informal).

### 16. B08-V01 · Teori Lokasi Industri Weber
- **Adegan:**
  1. *Hook*: mengapa pabrik semen dekat tambang kapur, sedangkan pabrik minuman dekat kota?
  2. Segitiga lokasi: dua sumber bahan baku dan pasar. Titik biaya transport minimum ditemukan.
  3. Indeks material = berat bahan lokal ÷ berat produk. Jika > 1, industri berorientasi bahan baku. Jika < 1, berorientasi pasar.
  4. Isodapan dan daya tarik tenaga kerja murah.
- **Contoh soal:** hitung indeks material lalu tentukan orientasi lokasinya.
- **Jebakan:** bahan baku ubikuitas (ada di mana-mana) tidak menarik lokasi.

### 17. B10-V00 · Apa Itu Kota?
- **Adegan:**
  1. *Hook*: kapan desa "naik kelas" menjadi kota?
  2. Kriteria perkotaan BPS: kepadatan, porsi rumah tangga pertanian, fasilitas.
  3. Fungsi kota dan zona pinggiran (*rural–urban fringe*).
- **Contoh soal:** klasifikasi desa atau kota dari data skor.
- **Jebakan:** jumlah penduduk besar saja tidak cukup untuk disebut kota.

### 18. B10-V01 · Model Struktur Kota
- **Adegan:**
  1. *Hook*: peta guna lahan Jakarta. Pola apa yang terlihat?
  2. Burgess: lingkaran konsentris tumbuh satu per satu.
  3. Hoyt: sektor memanjang mengikuti jalur transportasi.
  4. Harris–Ullman: banyak inti.
  5. Perbandingan ketiganya dan kasus kota di Indonesia.
- **Contoh soal:** tentukan model dari sebuah peta zona kota.
- **Jebakan:** Hoyt dicirikan sektor, bukan lingkaran.

### 19. B11-V00 · Sistem Pariwisata
- **Adegan:**
  1. *Hook*: apa bedanya wisatawan dan pelancong?
  2. Model Leiper: daerah asal, rute transit, destinasi.
  3. Komponen destinasi 4A (atraksi, aksesibilitas, amenitas, ansilari) tersusun.
- **Contoh soal:** kelompokkan contoh ke dalam komponen 4A.
- **Jebakan:** hotel termasuk amenitas, bukan atraksi.

### 20. B11-V01 · Siklus Hidup Destinasi (TALC)
- **Adegan:**
  1. *Hook*: mengapa destinasi yang dulu viral bisa sepi?
  2. Grafik tumbuh: kurva S Butler dengan tahap eksplorasi sampai stagnasi, lalu dua cabang (peremajaan dan penurunan).
  3. Ciri setiap tahap beserta tipe wisatawan Plog.
- **Contoh soal:** tentukan tahap destinasi dari data pertumbuhan tahunan.
- **Jebakan:** pertumbuhan melambat tetapi jumlah tinggi menandakan konsolidasi atau stagnasi, bukan pembangunan.

### 21. B03-V00 · Sumber Daya vs Cadangan
- **Adegan:**
  1. *Hook*: mengapa batu bara tidak terbarukan padahal masih terbentuk?
  2. Klasifikasi sumber daya: terbarukan, tidak terbarukan, dan tak habis.
  3. Kotak McKelvey: sumber daya (diketahui, belum diketahui) vs cadangan (ekonomis).
- **Contoh soal:** hitung umur cadangan = cadangan ÷ produksi per tahun.
- **Jebakan:** cadangan bisa bertambah karena teknologi atau harga, tanpa penemuan baru.

### 22. B03-V02 · Cara Kerja Pembangkit Listrik
- **Adegan:**
  1. *Hook*: dari mana listrik di rumahmu?
  2. Prinsip turbin–generator (pola A).
  3. PLTU, PLTA, PLTP, PLTS: alur energi masing-masing, syarat lokasi, dan dampaknya.
- **Contoh soal:** hitung daya PLTA, P = ρ g Q h η.
- **Jebakan:** PLTS tidak memakai turbin.

### 23. B04-V00 · Ekosistem sebagai Sistem
- **Adegan:**
  1. *Hook*: apa yang terjadi bila elang punah?
  2. Komponen biotik dan abiotik.
  3. Aliran energi satu arah vs siklus materi berputar (dua panah berbeda warna).
- **Contoh soal:** energi di trofik ke-3 bila produsen 10.000 kkal (aturan 10%).
- **Jebakan:** energi tidak didaur ulang, hanya materi yang didaur ulang.

### 24. B04-V01 · Pencemaran Air: BOD, DO, dan Biomagnifikasi
- **Adegan:**
  1. *Hook*: ikan mati di hilir pabrik.
  2. DO dan BOD: kurva oxygen sag di sepanjang sungai.
  3. Satuan ppm dan baku mutu.
  4. Biomagnifikasi merkuri naik sepanjang rantai makanan.
- **Contoh soal:** baca grafik DO dan tentukan titik paling tercemar.
- **Jebakan:** BOD tinggi berarti tercemar, bukan bersih.

### 25. B06-V00 · Faktor Fisik dan Nonfisik Pertanian
- **Adegan:**
  1. *Hook*: mengapa kopi di dataran tinggi dan padi di dataran rendah?
  2. Faktor fisik (iklim, tanah, relief, air) dan nonfisik (pasar, modal, teknologi, kebijakan) sebagai lapisan peta.
- **Contoh soal:** faktor dominan pada sebuah kasus pertanian.
- **Jebakan:** faktor pasar bisa mengalahkan kesesuaian fisik lahan.

### 26. B06-V01 · Dari Revolusi Pertanian ke Revolusi Hijau
- **Adegan:**
  1. *Hook*: dari ladang di Mesopotamia ke drone pertanian.
  2. Garis waktu: revolusi pertanian pertama, kedua, Revolusi Hijau, pertanian 4.0.
  3. Revolusi Hijau: bibit unggul, pupuk, irigasi, pestisida, beserta untung dan ruginya.
- **Contoh soal:** dampak negatif Revolusi Hijau.
- **Jebakan:** Revolusi Hijau meningkatkan produksi tetapi menurunkan keragaman hayati dan kesuburan jangka panjang.

---

## 8. DAFTAR GELOMBANG 2 (52 VIDEO)

Buat tabel adegan rinci untuk video-video ini saat gilirannya tiba, dengan mengikuti pola Bagian 6 dan struktur Bagian 4.

| Kode | Judul | Fokus dan visual kunci |
|---|---|---|
| B01-V02 | Efek Rumah Kaca dan Pemanasan Global | Gelombang pendek masuk dan gelombang panjang tertahan (pola A); GWP; kenaikan muka laut |
| B01-V03 | Sirkulasi Atmosfer Global dan Monsun | Sel Hadley–Ferrel–Polar, Coriolis (pola A/D), pergeseran ITCZ |
| B01-V04 | Suhu, Lapse Rate, dan Efek Föhn | Penampang gunung, parsel udara naik dan turun, hitungan (pola B/F) |
| B01-V05 | Klasifikasi Iklim dan Klimograf | Membaca klimograf; nilai Q Schmidt–Ferguson; Oldeman |
| B02-V02 | Siklus Manajemen Bencana | Diagram siklus; mitigasi struktural vs nonstruktural |
| B02-V03 | Gempa Bumi dan Tsunami | Gelombang P dan S, magnitudo vs intensitas, waktu tiba tsunami |
| B02-V04 | Likuifaksi dan Gerakan Massa | Butir tanah dan air pori (pola B); Petobo–Balaroa |
| B02-V05 | Sistem Peringatan Dini | Empat unsur EWS; status gunung api; *last mile* |
| B03-V01 | Bauran dan Transisi Energi Indonesia | Grafik bauran energi bertumpuk; target EBT |
| B03-V03 | Panas Bumi dan Cincin Api | Penampang sistem panas bumi (pola B) |
| B03-V04 | Tragedi Milik Bersama dan MSY | Kurva logistik dan MSY; simulasi overfishing |
| B03-V05 | Hitungan Sumber Daya | Daya PLTA, umur cadangan, rasio elektrifikasi (pola F) |
| B04-V02 | Aliran Energi dan Aturan 10% | Piramida ekologi dibangun bertahap |
| B04-V03 | Siklus Biogeokimia | Siklus karbon, nitrogen, fosfor (pola A) |
| B04-V04 | Bioma dan Siklus Hara Gersmehl | Diagram Whittaker; lingkaran hara B-L-S |
| B04-V05 | Teori Penduduk–Lingkungan | Malthus vs Boserup; IPAT; kurva Kuznets lingkungan |
| B05-V02 | Siklus Batuan dan Deret Bowen | Siklus batuan (pola A); tekstur batuan beku |
| B05-V03 | Kerja Sungai dan Bentuk Lahan Fluvial | Kurva Hjulström; animasi meander → danau tapal kuda; delta |
| B05-V04 | Lipatan dan Sesar | Blok 3D ditekan atau ditarik (pola C); horst–graben |
| B05-V05 | Karst dan Pesisir | Pelarutan → dolina → gua; refraksi gelombang; spit dan tombolo |
| B06-V02 | Empat Pilar Ketahanan Pangan | Empat pilar sebagai fondasi bangunan; kedaulatan pangan |
| B06-V03 | Teori von Thünen | Kurva sewa lokasi → cincin guna lahan (pola E/C) |
| B06-V04 | Tanah untuk Pertanian | Segitiga tekstur USDA (cara membaca); pH dan KTK |
| B06-V05 | Penduduk dan Daya Dukung Lahan | Malthus; σ; hitungan swasembada (pola F) |
| B07-V01 | Ukuran Fertilitas dan Mortalitas | CBR, ASFR, TFR, NRR, IMR (pola F) |
| B07-V03 | Membaca Piramida Penduduk | Piramida ekspansif, stasioner, konstriktif, dan daerah migran (pola G) |
| B07-V04 | Rasio Ketergantungan dan Bonus Demografi | Hitungan rasio ketergantungan; "jendela peluang" pada grafik |
| B07-V05 | Teori dan Jenis Migrasi | Lee push–pull, Ravenstein, Todaro, model gravitasi; pengungsi vs IDP |
| B08-V02 | Globalisasi dan Perusahaan Transnasional | Peta aliran investasi dan produksi (pola D) |
| B08-V03 | Rantai Nilai Global dan Perang Dagang | Kurva senyum; peta *chokepoint* (Selat Malaka) |
| B08-V04 | LQ dan Basis Ekonomi Wilayah | Hitungan LQ (pola F) |
| B08-V05 | Keunggulan Komparatif | Ricardo: contoh dua negara dua barang (pola F) |
| B09-V01 | Menghitung IPM | Tiga dimensi IPM → rata-rata geometrik (pola F) |
| B09-V03 | Kurva Kuznets dan Indeks Williamson | U terbalik; ketimpangan antarwilayah |
| B09-V04 | Teori Pembangunan | Tangga Rostow vs inti–pinggiran (pola G) |
| B09-V05 | Teori Keruangan Pembangunan | Kutub pertumbuhan, efek balik dan efek sebar; heksagon Christaller; kuadran Klassen |
| B10-V02 | Teori Sewa Lahan Kota (Bid-Rent) | Kurva sewa → zona kota (pola E/C) |
| B10-V03 | Siklus Urbanisasi van den Berg | Grafik inti vs pinggiran per tahap |
| B10-V04 | Kota di Asia Tenggara | Model McGee, desakota, kampung kota |
| B10-V05 | Sistem Kota | *Rank-size*, kota primat, titik henti Reilly (pola F) |
| B11-V02 | Dampak Ekonomi Pariwisata | Aliran uang, kebocoran, efek pengganda (pola A/F) |
| B11-V03 | Tipologi Wisatawan | Kurva Plog; tipologi Cohen |
| B11-V04 | Daya Dukung Wisata | PCC → RCC → ECC (pola F); LAC |
| B11-V05 | Overtourism dan Indeks Doxey | Tangga euforia → antagonisme; komodifikasi |
| B12-V02 | Akulturasi, Asimilasi, Sinkretisme | Banding berdampingan dengan contoh Indonesia (pola G) |
| B12-V03 | Bentuk dan Batas Negara | Siluet negara; klasifikasi genetik batas (pola D) |
| B12-V04 | Indeks Keragaman Bahasa | IKL dan fraksionalisasi (pola F) |
| B12-V05 | Kekuatan Pemersatu dan Pemecah | Tarik tambang sentripetal vs sentrifugal; devolusi dan secesi |
| B13-V01 | Skala Peta | Jarak, luas (penyebut²), perbesaran peta (pola F) |
| B13-V02 | Azimut dan Navigasi | Kuadran, azimut balik, deklinasi (pola F/D) |
| B13-V04 | Profil dan Kemiringan Lereng | Membuat penampang dari kontur (pola C); persen lereng |
| B13-V05 | Penginderaan Jauh dan NDVI | Kurva pantulan spektral; citra asli Sentinel-2 warna asli, warna semu, dan NDVI |

---

## 9. CHECKLIST QA (WAJIB SEBELUM PRATINJAU DAN FINAL)
- [ ] Watermark sudut terlihat sepanjang video, tinggi ≥ 80 px, tidak tertutup elemen lain.
- [ ] Watermark tengah besar ada di semua adegan konten (opasitas 7–9%) dan tidak mengganggu keterbacaan.
- [ ] Intro, lower-third, dan outro "Latihan soalnya di OSNGEO.id" sudah ada.
- [ ] Semua fakta, angka, dan nama tempat sudah dicek dan konsisten dengan materi OSN. Tidak ada `[CEK FAKTA]` yang tersisa.
- [ ] Peta memiliki skala, arah utara, label yang tidak bertabrakan, dan sumber.
- [ ] Ejaan, koma desimal, dan satuan benar. Ukuran teks ≥ 36 px.
- [ ] Animasi sinkron dengan narasi (toleransi ±3 frame pada kata kunci).
- [ ] Contoh soal benar, kunci tidak ambigu, dan ada jeda berpikir 3 detik.
- [ ] Audio: tidak ada klik atau napas berlebihan; −14 LUFS; true peak ≤ −1 dBTP; musik tidak menutupi narasi.
- [ ] Subtitle sinkron dan bebas salah ketik.
- [ ] Durasi 2:00–3:00.
- [ ] Atribusi data atau citra tercantum di layar (kecil, kiri bawah) dan di deskripsi.

---

## 10. BALASAN PERTAMAMU

Setelah membaca brief ini, balas dengan:
1. Ringkasan singkat pemahamanmu: jumlah video, urutan Gelombang 1, dan aturan watermark.
2. Alat atau stack animasi yang akan kamu pakai beserta alasannya.
3. Langsung kerjakan **Tahap 1 untuk Urutan 1: B13-V00 "Dari Bumi ke Peta"**, yaitu naskah narasi, tabel adegan, contoh soal, dan sumber data. Lalu berhenti dan tunggu persetujuan saya.
