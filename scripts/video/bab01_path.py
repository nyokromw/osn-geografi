"""Jalur belajar Bab 1 Iklim: 27 video berurutan menurut prasyarat."""
T1, T2, T3, T4, T5, T6, T7 = ("Tahap 1 · Fondasi atmosfer dan energi", "Tahap 2 · Udara bergerak", "Tahap 3 · Air di atmosfer",
                              "Tahap 4 · Iklim wilayah", "Tahap 5 · Interaksi laut–atmosfer", "Tahap 6 · Perubahan iklim", "Tahap 7 · Terapan dan data")
PATH = [
 (1, T1, "Konsep Dasar: Mesin Iklim Bumi", "Cuaca vs iklim, unsur dan pengendali iklim, pemanasan matahari yang tidak merata, rumus Braak.", "Dasar", []),
 (2, T1, "Atmosfer Bumi", "Komposisi udara, lima lapisan atmosfer, dan tekanan udara yang turun terhadap ketinggian.", "Dasar", [1]),
 (3, T1, "Radiasi Matahari dan Insolasi", "Gelombang pendek dan panjang, sudut datang sinar, lama penyinaran, dan sebaran insolasi menurut lintang.", "Dasar", [1]),
 (4, T1, "Albedo dan Neraca Energi", "Albedo berbagai permukaan, neraca 100 satuan energi, dan pulau bahang kota.", "Dasar–Menengah", [3]),
 (5, T1, "Suhu Udara", "Faktor suhu, rumus Braak, zona Junghuhn, isoterm, amplitudo, dan inversi suhu.", "Dasar–Menengah", [2, 4]),
 (6, T2, "Tekanan Udara dan Lahirnya Angin", "Gradien tekanan, isobar, dan mengapa udara bergerak dari tekanan tinggi ke rendah.", "Dasar", [5]),
 (7, T2, "Gaya Coriolis dan Gesekan", "Pembelokan angin, hukum Buys Ballot, siklon dan antisiklon di dua belahan bumi.", "Menengah", [6]),
 (8, T2, "Angin Lokal", "Angin darat–laut, lembah–gunung, dan angin jatuh di Indonesia.", "Dasar", [6]),
 (9, T2, "Sirkulasi Tiga Sel dan Angin Pasat", "Sel Hadley, Ferrel, Polar, sabuk tekanan, dan angin pasat.", "Menengah", [7]),
 (10, T2, "ITCZ dan Monsun Asia–Australia", "Pergeseran ITCZ, monsun barat dan timur, serta musim di Indonesia.", "Menengah", [9]),
 (11, T2, "Sirkulasi Walker", "Sel sirkulasi barat–timur di atas Pasifik ekuator.", "Menengah", [9]),
 (12, T3, "Kelembapan Udara", "Kelembapan absolut, relatif, spesifik, dan titik embun.", "Dasar–Menengah", [5]),
 (13, T3, "Proses Adiabatik dan Stabilitas Atmosfer", "Laju adiabatik kering dan basah, udara stabil dan labil.", "Lanjut", [5, 12]),
 (14, T3, "Efek Föhn", "Hitungan parsel udara yang naik dan turun melewati gunung.", "Lanjut", [8, 13]),
 (15, T3, "Awan dan Hujan", "Jenis awan, empat mekanisme hujan, hujan es, kabut, dan hujan asam.", "Menengah", [13]),
 (16, T4, "Pola Hujan Indonesia", "Pola monsunal, ekuatorial, dan lokal beserta wilayahnya.", "Menengah", [10, 15]),
 (17, T4, "Klasifikasi Iklim", "Köppen, Schmidt–Ferguson (nilai Q), Oldeman, dan membaca klimograf.", "Menengah", [16]),
 (18, T5, "Arus Laut dan Upwelling", "Gyre, arus hangat dan dingin, gurun pesisir, transpor Ekman, dan upwelling.", "Menengah", [7, 9]),
 (19, T5, "Sirkulasi Termohalin dan ARLINDO", "Sabuk konveyor global, AMOC, dan Arus Lintas Indonesia.", "Menengah", [18]),
 (20, T5, "El Niño, La Niña, dan IOD (+MJO)", "Mekanisme ENSO, IOD, dan MJO, indeks ONI–SOI–DMI, dampak bagi Indonesia, dan 18 istilah.", "Menengah–Lanjut", [11, 18]),
 (21, T5, "Siklon Tropis dan Cuaca Ekstrem", "Syarat terbentuknya siklon, siklon dan Indonesia, serta cuaca ekstrem lain.", "Menengah", [7, 13, 18]),
 (22, T6, "Efek Rumah Kaca dan Pemanasan Global", "Neraca energi, gas rumah kaca dan GWP, bukti, umpan balik, dampak, mitigasi dan adaptasi, dan 18 istilah.", "Menengah–Lanjut", [4]),
 (23, T6, "Kebijakan Iklim", "IPCC, Protokol Kyoto, Persetujuan Paris, NDC Indonesia, dan nilai ekonomi karbon.", "Menengah", [22]),
 (24, T6, "Paleoklimat dan Siklus Milankovitch", "Data inti es, siklus orbit, zaman es, dan Paparan Sunda–Sahul.", "Lanjut", [3, 22]),
 (25, T7, "Evapotranspirasi dan Neraca Air", "Evapotranspirasi, metode Thornthwaite dan Blaney–Criddle, surplus dan defisit air.", "Lanjut", [5, 16]),
 (26, T7, "Nexus Pangan–Air–Energi", "Keterkaitan iklim, irigasi, PLTA, dan kalender tanam.", "Lanjut", [20, 25]),
 (27, T7, "Membaca Data Iklim BMKG", "Zona Musim, sifat hujan, hari tanpa hujan, indeks kekeringan, anomali dan tren.", "Lanjut", [16, 20]),
]
def kode(n): return f"B01-{n:02d}"
def rows():
    return [dict(topik_id=1, kode=kode(n), judul=j, deskripsi=d, tahap=t, level=l, prasyarat=", ".join(kode(p) for p in pre) or None, urutan=100 + n) for n, t, j, d, l, pre in PATH]
if __name__ == "__main__":
    import json; print(json.dumps(rows(), ensure_ascii=False))
