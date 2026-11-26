import json, re, sys, os, shutil
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "/home/user/osn-geografi"
REPL = [(r'O S N Geo titik I D', 'OSNGEO.id')]
P = {
 "b01v03": dict(code="B01-02", slug="Atmosfer-Bumi", no=2, name="Atmosfer Bumi", prev="#1 · B01-01 · Mesin Iklim Bumi", next="#3 · B01-03 · Radiasi Matahari dan Insolasi",
   ch=[("Pembuka: Rinjani, pesawat jet, aurora", 2), ("Komposisi udara", 7), ("Aerosol dan inti kondensasi", 11), ("Lapisan atmosfer: troposfer, lapse rate, tropopause", 15), ("Stratosfer dan lapisan ozon", 24), ("Mesosfer", 27), ("Termosfer, ionosfer, aurora", 30), ("Tekanan udara", 35), ("Contoh soal OSN", 42), ("Dua jebakan", 47), ("Ringkasan dan glosarium", 51)],
   titles=["Atmosfer Bumi: Komposisi, Lapisan, dan Tekanan Udara", "Lapisan Atmosfer dan Istilah Asingnya", "Kenapa Sesak Napas di Puncak Gunung?"],
   desc="Kenapa pendaki sesak napas di puncak Rinjani, kenapa pesawat jet terbang di ketinggian sepuluh kilometer, dan dari mana cahaya aurora? Di video ini kamu belajar komposisi udara, aerosol sebagai inti kondensasi, lima lapisan atmosfer beserta profil suhunya, lapisan ozon, ionosfer, aurora, dan cara tekanan udara turun terhadap ketinggian.",
   sum=["Udara kering: N2 ±78%, O2 ±21%, Ar 0,93%, CO2 ±0,04%; uap air 0–4%.", "Aerosol = inti kondensasi (condensation nuclei) tempat titik awan terbentuk.", "Troposfer 0–12 km (ekuator ±17, kutub ±8 km): cuaca, suhu turun 0,6 °C/100 m (lapse rate).", "Stratosfer 12–50 km: ozon menyerap UV, suhu naik. Mesosfer 50–85 km: terdingin, meteor terbakar.", "Termosfer: ionosfer memantulkan radio, aurora borealis/australis.", "Tekanan ±1.013 mb di permukaan laut, separuhnya di 5,5 km; ±1 mb per 10 m di lapisan bawah."],
   tags="atmosfer bumi, lapisan atmosfer, troposfer, stratosfer, mesosfer, termosfer, ionosfer, lapisan ozon, aurora, lapse rate, tropopause, tekanan udara, aerosol, komposisi udara"),
 "b01v04": dict(code="B01-03", slug="Radiasi-Matahari-dan-Insolasi", no=3, name="Radiasi Matahari dan Insolasi", prev="#2 · B01-02 · Atmosfer Bumi", next="#4 · B01-04 · Albedo dan Neraca Energi",
   ch=[("Pembuka: kutub utara 21 Juni", 2), ("Hukum Wien", 6), ("Gelombang pendek dan gelombang panjang", 10), ("Hukum Stefan–Boltzmann", 14), ("Insolasi dan konstanta matahari", 17), ("Empat faktor insolasi", 21), ("Perihelion dan aphelion", 25), ("Kenapa kutub utara menang?", 29), ("Contoh soal OSN", 33), ("Dua jebakan", 38), ("Ringkasan dan glosarium", 42)],
   titles=["Radiasi Matahari dan Insolasi: Hukum Wien dan Stefan–Boltzmann", "Kutub Utara Dapat Energi Matahari Lebih Banyak dari Ekuator?", "Gelombang Pendek vs Gelombang Panjang"],
   desc="Pada 21 Juni, kutub utara menerima energi matahari harian lebih banyak daripada ekuator. Kok bisa? Video ini membahas hukum Wien, hukum Stefan–Boltzmann, radiasi gelombang pendek dan panjang, konstanta matahari, empat faktor insolasi (sudut datang, lama penyinaran, jarak, atmosfer), perihelion–aphelion, dan penyebab musim yang sebenarnya.",
   sum=["Hukum Wien: panjang gelombang puncak = 2.898 ÷ T (µm). Matahari ±0,5 µm, bumi ±10 µm.", "Matahari = gelombang pendek (shortwave), bumi = gelombang panjang/inframerah (longwave).", "Stefan–Boltzmann: energi sebanding T pangkat 4; suhu ×2 → energi ×16.", "Konstanta matahari ±1.361 W/m²; rata-rata seluruh permukaan ±340 W/m² (÷4).", "Faktor insolasi: sudut datang, lama penyinaran, jarak (perihelion 3 Jan, aphelion 4 Jul), atmosfer.", "Musim disebabkan kemiringan sumbu bumi 23,5° (axial tilt), bukan jarak."],
   tags="radiasi matahari, insolasi, hukum wien, stefan boltzmann, konstanta matahari, gelombang pendek, gelombang panjang, inframerah, perihelion, aphelion, sudut datang sinar, penyebab musim, axial tilt"),
 "b01v05": dict(code="B01-04", slug="Albedo-dan-Neraca-Energi", no=4, name="Albedo dan Neraca Energi", prev="#3 · B01-03 · Radiasi Matahari dan Insolasi", next="#5 · B01-05 · Suhu Udara",
   ch=[("Pembuka: kaus hitam vs putih", 2), ("Albedo berbagai permukaan", 7), ("Neraca energi 100 satuan", 15), ("Panas sensibel dan panas laten", 19), ("Keseimbangan radiasi", 23), ("Pulau bahang kota (UHI)", 25), ("Cara mendinginkan kota", 33), ("Contoh soal OSN", 34), ("Jebakan", 40), ("Ringkasan dan glosarium", 43)],
   titles=["Albedo dan Neraca Energi Bumi: Sensible, Latent, Urban Heat Island", "Kenapa Kota Lebih Panas dari Desa?", "Albedo Dijelaskan: Salju, Hutan, Aspal, dan Awan"],
   desc="Kenapa kaus hitam lebih panas, dan kenapa pusat kota bisa 2–4 °C lebih hangat dari pinggirannya? Video ini membahas albedo berbagai permukaan, neraca energi bumi dari 100 satuan radiasi, panas sensibel dan panas laten, keseimbangan radiasi, pulau bahang kota (urban heat island), serta cara mendinginkan kota.",
   sum=["Albedo = radiasi dipantulkan ÷ diterima. Salju 80–90%, awan 60–90%, hutan 10–15%, laut/aspal 5–10%; bumi ±30%.", "Dari 100 satuan: 30 dipantulkan, 20 diserap atmosfer, 50 diserap permukaan.", "Permukaan melepas energi lewat inframerah, panas sensibel, dan panas laten.", "Jangka panjang: energi masuk = keluar (radiative equilibrium).", "UHI: beton/aspal menyimpan panas, vegetasi sedikit, panas buangan, gedung rapat.", "Energi diserap = radiasi × (1 − albedo); hati-hati faktor lain di soal OSN."],
   tags="albedo, neraca energi, energy budget, panas sensibel, panas laten, sensible heat, latent heat, urban heat island, pulau bahang kota, cool roof, green roof, ruang terbuka hijau"),
 "b01v06": dict(code="B01-05", slug="Suhu-Udara", no=5, name="Suhu Udara", prev="#4 · B01-04 · Albedo dan Neraca Energi", next="#6 · B01-06 · Tekanan Udara dan Lahirnya Angin",
   ch=[("Pembuka: Siberia, Jakarta, Dieng", 2), ("Enam faktor suhu", 6), ("Darat vs laut dan amplitudo", 8), ("Iklim maritim vs kontinental", 12), ("Ketinggian dan rumus Braak", 16), ("Zona Junghuhn", 23), ("Inversi suhu", 28), ("Embun upas Dieng", 35), ("Isoterm dan ekuator termal", 36), ("Contoh soal OSN", 39), ("Jebakan dan ringkasan", 45)],
   titles=["Suhu Udara: Amplitudo, Rumus Braak, Zona Junghuhn, Inversi", "Kenapa Puncak Gunung Dingin padahal Dekat Matahari?", "Inversi Suhu dan Embun Upas Dieng"],
   desc="Siberia berayun dari −40 °C sampai +25 °C, Jakarta hampir sama sepanjang tahun, dan di Dieng embun bisa membeku. Video ini membahas faktor pengendali suhu, darat vs laut, amplitudo suhu, iklim maritim dan kontinental, rumus Braak, zona Junghuhn, inversi suhu, embun upas, isoterm, ekuator termal, dan Arus Teluk.",
   sum=["Laut lambat panas dan lambat dingin: iklim maritim beramplitudo kecil; pedalaman benua kontinental.", "Lapse rate ±0,6 °C per 100 m. Braak: T = 26,3 − 0,6h (h dalam ratusan m).", "Jika suhu titik awal diketahui: T baru = T lama − 0,6 × selisih h.", "Junghuhn: panas 0–700 m, sedang 700–1.500 m, sejuk 1.500–2.500 m, dingin >2.500 m.", "Inversi suhu (radiation inversion, cold air drainage) memerangkap polutan; embun upas = frost.", "Isoterm membelok di batas darat–laut dan arus hangat (Gulf Stream)."],
   tags="suhu udara, amplitudo suhu, iklim maritim, iklim kontinental, rumus braak, zona junghuhn, inversi suhu, temperature inversion, embun upas, dieng, isoterm, ekuator termal, gulf stream, lapse rate"),
 "b01n06": dict(code="B01-06", slug="Tekanan-Udara-dan-Angin", no=6, name="Tekanan Udara dan Lahirnya Angin", prev="#5 · B01-05 · Suhu Udara", next="#7 · B01-07 · Gaya Coriolis dan Gesekan",
   ch=[("Angin: pemanasan dan tekanan", 3), ("Barometer, isobar, dan pusat H/L", 15), ("Gradien barometrik", 21), ("Gaya gradien tekanan", 29), ("Pola tekanan Januari dan Juli", 34), ("Contoh soal OSN", 39), ("Dua jebakan", 45), ("Ringkasan dan glosarium", 49)],
   titles=["Tekanan Udara dan Lahirnya Angin: Isobar dan Gradien Barometrik", "Kenapa Angin Bisa Bertiup? Cara Membaca Peta Isobar", "Gradien Barometrik: Cara Menghitung dan Membaca Isobar"],
   desc="Garis melengkung dan huruf H dan L di peta cuaca adalah kunci untuk menebak arah dan kekuatan angin. Video ini membahas bagaimana perbedaan pemanasan melahirkan tekanan rendah dan tinggi, barometer dan satuan milibar, isobar, gradien barometrik dalam mb per 111 km, gaya gradien tekanan, serta pola tekanan Januari dan Juli di Asia–Australia yang menjadi cikal bakal monsun.",
   sum=["Udara dipanaskan mengembang dan naik: tekanan rendah (thermal low); udara dingin turun: tekanan tinggi.", "Angin bertiup dari tekanan tinggi ke tekanan rendah.", "1 mb = 1 hPa. Isobar menghubungkan tempat bertekanan sama; H = high, L = low (T/R di peta Indonesia).", "Gradien barometrik = selisih tekanan ÷ jarak, dinyatakan dalam mb per 111 km (1° lintang).", "Isobar rapat = angin kencang; isobar renggang = angin lemah.", "Januari: tekanan tinggi Siberia, Australia rendah; Juli berbalik (cikal bakal monsun)."],
   tags="tekanan udara, angin, isobar, gradien barometrik, pressure gradient, barometer, milibar, hektopascal, tekanan tinggi, tekanan rendah, thermal low, siberian high, peta cuaca, monsun"),
 "b01n07": dict(code="B01-07", slug="Gaya-Coriolis-dan-Gesekan", no=7, name="Gaya Coriolis dan Gesekan", prev="#6 · B01-06 · Tekanan Udara dan Lahirnya Angin", next="#8 · B01-08 · Angin Lokal",
   ch=[("Bola di atas bumi yang berputar", 5), ("Aturan gaya Coriolis", 11), ("Kenapa siklon jarang di khatulistiwa", 16), ("Angin geostropik", 18), ("Gaya gesekan", 25), ("Hukum Buys Ballot", 29), ("Siklon dan antisiklon", 33), ("Contoh soal OSN", 40), ("Dua jebakan", 44), ("Ringkasan dan glosarium", 47)],
   titles=["Gaya Coriolis, Angin Geostropik, dan Hukum Buys Ballot", "Kenapa Badai Selalu Berputar? Gaya Coriolis Dijelaskan", "Siklon vs Antisiklon: Arah Putaran di Utara dan Selatan"],
   desc="Badai di Amerika berputar berlawanan arah jarum jam, di Australia searah jarum jam, dan hampir tidak ada badai yang lahir di khatulistiwa. Video ini membahas gaya Coriolis dengan animasi bola bumi 3D, aturan pembelokan di BBU dan BBS, angin geostropik, gaya gesekan, hukum Buys Ballot, serta siklon dan antisiklon.",
   sum=["Gaya Coriolis (Coriolis effect): gaya semu akibat rotasi bumi; ke kanan di BBU, ke kiri di BBS.", "Nol di ekuator, maksimum di kutub; siklon tropis hampir tidak terbentuk di lintang 0°–5°.", "Lapisan atas: gaya gradien tekanan = Coriolis, angin sejajar isobar (geostrophic wind).", "Dekat permukaan: gesekan membuat angin memotong isobar 10°–45° menuju tekanan rendah.", "Buys Ballot: di BBU, membelakangi angin, tekanan rendah di kiri (BBS di kanan).", "Siklon: rendah, konvergen, naik, hujan. Antisiklon: tinggi, turun, divergen, cerah."],
   tags="gaya coriolis, coriolis effect, angin geostropik, geostrophic wind, gaya gesekan, hukum buys ballot, siklon, antisiklon, konvergen, divergen, siklon tropis, rotasi bumi"),
 "b01n08": dict(code="B01-08", slug="Angin-Lokal", no=8, name="Angin Lokal", prev="#7 · B01-07 · Gaya Coriolis dan Gesekan", next="#9 · B01-09 · Sirkulasi Tiga Sel dan Angin Pasat",
   ch=[("Apa itu angin lokal", 3), ("Angin laut, angin darat, dan nelayan", 4), ("Angin lembah dan angin gunung", 15), ("Angin fohn", 23), ("Angin fohn di Indonesia", 28), ("Angin bora", 34), ("Contoh soal OSN", 36), ("Dua jebakan", 40), ("Ringkasan dan glosarium", 43)],
   titles=["Angin Lokal: Angin Laut, Darat, Lembah, Gunung, dan Fohn", "Kenapa Nelayan Berangkat Dini Hari? Angin Darat dan Angin Laut", "Angin Fohn di Indonesia: Gending, Kumbang, Brubu, Bahorok, Wambraw"],
   desc="Nelayan berangkat dini hari dan pulang siang hari, sementara petani tembakau Probolinggo cemas saat angin Gending turun dari Tengger. Video ini membahas angin laut dan darat, angin lembah dan gunung (anabatik dan katabatik), angin fohn beserta nama lokalnya di Indonesia, dan angin bora.",
   sum=["Angin laut (sea breeze): siang, laut ke darat, ±09.00–16.00.", "Angin darat (land breeze): malam, darat ke laut, ±20.00–06.00; nelayan berangkat dini hari.", "Angin lembah (valley breeze, anabatic): siang naik ke lereng.", "Angin gunung (mountain breeze, katabatic): malam turun ke lembah; udara dingin menggenang di kaldera.", "Angin fohn (foehn wind): kering dan panas; Gending, Kumbang, Brubu, Bahorok, Wambraw.", "Angin bora: angin jatuh yang dingin (Adriatik)."],
   tags="angin lokal, angin laut, angin darat, sea breeze, land breeze, angin lembah, angin gunung, anabatic, katabatic, angin fohn, foehn, angin gending, angin kumbang, angin brubu, angin bahorok, angin wambraw, angin bora"),
 "b01n09": dict(code="B01-09", slug="Sirkulasi-Tiga-Sel-dan-Angin-Pasat", no=9, name="Sirkulasi Tiga Sel dan Angin Pasat", prev="#8 · B01-08 · Angin Lokal", next="#10 · B01-10 · ITCZ dan Monsun",
   ch=[("Mesin pemindah panas", 5), ("Sel Hadley dan ITCZ", 9), ("Antipasat, subtropis, gurun", 13), ("Angin pasat", 17), ("Sel Ferrel dan baratan", 22), ("Sel kutub dan front kutub", 25), ("Sabuk tekanan", 29), ("Contoh soal OSN", 31), ("Dua jebakan", 35), ("Ringkasan dan glosarium", 38)],
   titles=["Sirkulasi Tiga Sel: Hadley, Ferrel, Kutub, dan Angin Pasat", "Kenapa Gurun Dunia Berjajar di Lintang 30 Derajat?", "Angin Pasat, ITCZ, dan Westerlies Dijelaskan dengan Bola Bumi 3D"],
   desc="Kapal layar Eropa berangkat lewat rute selatan dan pulang lewat rute utara, gurun-gurun dunia berjajar di lintang 30°, dan pelaut takut terjebak di doldrums. Video ini membahas model tiga sel: sel Hadley, ITCZ, antipasat, tekanan tinggi subtropis dan gurun, angin pasat, sel Ferrel dan angin baratan, sel kutub, timuran kutub, front kutub, serta sabuk tekanan dunia.",
   sum=["Tropis surplus energi, kutub defisit; atmosfer memindahkan panas ke kutub dalam tiga sel per belahan bumi.", "Sel Hadley (0°–30°): naik di ITCZ (doldrums), antipasat di atas, turun di 30° (subtropical high, horse latitudes).", "Udara turun kering: Sahara, Arab, Kalahari, gurun Australia di sekitar 30°.", "Angin pasat (trade winds): timur laut di BBU, tenggara di BBS.", "Sel Ferrel (30°–60°): angin baratan (westerlies); diputar dua sel lain.", "Sel kutub (60°–90°): timuran kutub; front kutub di ±60°. Sabuk: L 0°, H 30°, L 60°, H 90°."],
   tags="sirkulasi atmosfer, model tiga sel, sel hadley, sel ferrel, sel kutub, itcz, doldrums, angin pasat, trade winds, antipasat, westerlies, angin baratan, polar easterlies, front kutub, horse latitudes, subtropical high, gurun"),
 "b01n10": dict(code="B01-10", slug="ITCZ-dan-Monsun", no=10, name="ITCZ dan Monsun", prev="#9 · B01-09 · Sirkulasi Tiga Sel dan Angin Pasat", next="#11 · B01-11 · Sirkulasi Walker",
   ch=[("ITCZ bergeser mengikuti matahari", 5), ("Apa itu monsun", 13), ("Monsun barat", 16), ("Monsun timur", 22), ("Pancaroba", 27), ("Pontianak, Padang, dan Ambon", 29), ("Contoh soal OSN", 32), ("Dua jebakan", 37), ("Ringkasan dan glosarium", 40)],
   titles=["ITCZ dan Monsun: Monsun Barat, Monsun Timur, dan Pancaroba", "Kenapa Ambon Hujan saat Jawa Kemarau? ITCZ dan Monsun", "Monsun Barat vs Monsun Timur di Indonesia"],
   desc="Jawa hujan pada Desember sampai Februari, NTT kemarau panjang, tetapi Ambon justru hujan pada Juni dan Juli. Video ini membahas ITCZ yang bergeser mengikuti matahari, monsun barat dan monsun timur dengan peta angin animasi, belokan Coriolis saat angin menyeberangi ekuator, pancaroba, serta wilayah yang tidak mengikuti pola monsun.",
   sum=["ITCZ (Intertropical Convergence Zone): sabuk tekanan rendah tempat pasat bertemu; bergeser ±5°–10° mengikuti matahari.", "Juli ITCZ di utara, Januari di selatan; pergeseran terjauh di atas Asia dan Australia.", "Monsun barat (Des–Feb): Asia tinggi, Australia rendah; angin timur laut berbelok jadi barat laut setelah ekuator; hujan.", "Monsun timur (Jun–Agu): Australia tinggi, Asia rendah; melintasi laut sempit; kemarau, NTT paling kering.", "Pancaroba (Apr–Mei, Okt–Nov): angin lemah, hujan lebat singkat, petir, puting beliung.", "Pengecualian: daerah ekuator dua puncak hujan; Ambon puncak Juni–Juli."],
   tags="itcz, monsun, monsun barat, monsun timur, west monsoon, east monsoon, pancaroba, musim hujan, musim kemarau, angin muson, iklim indonesia, coriolis, pola hujan, ambon"),
 "b01n11": dict(code="B01-11", slug="Sirkulasi-Walker", no=11, name="Sirkulasi Walker", prev="#10 · B01-10 · ITCZ dan Monsun", next="#12 · B01-12 · Kelembapan Udara",
   ch=[("Meridional dan zonal", 3), ("Kondisi normal: laut", 9), ("Kondisi normal: atmosfer", 17), ("Tahiti dan Darwin", 24), ("El Niño, La Niña, dan MJO", 26), ("Contoh soal OSN", 31), ("Dua jebakan", 35), ("Ringkasan dan glosarium", 39)],
   titles=["Sirkulasi Walker: Warm Pool, Upwelling, dan Sirkulasi Zonal", "Kenapa Laut Indonesia Hangat tapi Laut Peru Dingin?", "Sirkulasi Meridional vs Zonal: Kunci Memahami El Niño"],
   desc="Laut di sekitar Indonesia termasuk yang paling hangat di dunia, sementara lepas pantai Peru dingin dan kering. Video ini membahas sirkulasi meridional dan zonal, sirkulasi Walker di ekuator Pasifik dengan penampang 3D laut dan atmosfer, kolam air hangat, upwelling, pemantauan tekanan Tahiti–Darwin, serta kaitannya dengan El Niño, La Niña, dan MJO.",
   sum=["Sirkulasi meridional: utara–selatan (Hadley, Ferrel, kutub). Sirkulasi zonal: barat–timur.", "Sirkulasi Walker (Walker circulation): sirkulasi zonal di ekuator Pasifik.", "Pasat timur mendorong air hangat ke barat: kolam air hangat (warm pool) di Indonesia–Papua.", "Di Peru air dingin kaya nutrien naik (upwelling): perikanan kaya.", "Udara naik di Indonesia (tekanan rendah, hujan), turun di Peru (tekanan tinggi, kering).", "Walker melemah: Indonesia lebih kering (El Niño); menguat: lebih basah (La Niña). MJO juga fenomena zonal."],
   tags="sirkulasi walker, walker circulation, sirkulasi zonal, sirkulasi meridional, warm pool, kolam air hangat, upwelling, peru, tahiti darwin, indeks osilasi selatan, el nino, la nina, mjo, pasifik"),
 "b01n12": dict(code="B01-12", slug="Kelembapan-Udara", no=12, name="Kelembapan Udara", prev="#11 · B01-11 · Sirkulasi Walker", next="#13 · B01-13 · Adiabatik dan Stabilitas Atmosfer",
   ch=[("Uap air dan evapotranspirasi", 4), ("Udara seperti gelas", 12), ("Si Gumpal dan tiga ukuran kelembapan", 20), ("Malam: jenuh dan titik embun", 35), ("Embun, kabut, dan gelas es teh", 43), ("Contoh soal OSN", 49), ("Dua jebakan", 53), ("Ringkasan dan glosarium", 58)],
   titles=["Kelembapan Udara: Kelembapan Relatif, Jenuh, dan Titik Embun", "Kenapa Gelas Es Teh Berkeringat? Kelembapan Udara Dijelaskan", "Kelembapan Mutlak, Spesifik, dan Relatif dalam 4 Menit"],
   desc="Kenapa bagian luar gelas es teh bisa basah? Video ini membahas uap air, evapotranspirasi, dan tiga ukuran kelembapan (mutlak, spesifik, relatif) lewat analogi udara sebagai gelas yang ukurannya bergantung suhu, lalu udara jenuh, titik embun, embun, dan kabut. Disajikan bersama Si Gumpal, segumpal udara yang kita ikuti perjalanannya.",
   sum=["Uap air berasal dari evaporasi dan transpirasi (evapotranspiration).", "Kapasitas udara menampung uap air naik ±7% setiap suhu naik 1 °C.", "Kelembapan mutlak (g/m³), spesifik (g/kg, tetap saat udara mengembang), relatif (isi ÷ kapasitas × 100%).", "Udara didinginkan: RH naik sampai 100% = jenuh (saturated) pada titik embun (dew point).", "Di bawah titik embun: embun, kabut, awan. Kondensasi karena pendinginan, bukan pemanasan.", "RH tinggi tidak selalu berarti uap air banyak (udara kutub)."],
   tags="kelembapan udara, kelembapan relatif, relative humidity, kelembapan mutlak, kelembapan spesifik, titik embun, dew point, udara jenuh, evapotranspirasi, embun, kabut, kondensasi"),
 "b01n13": dict(code="B01-13", slug="Adiabatik-dan-Stabilitas", no=13, name="Adiabatik dan Stabilitas Atmosfer", prev="#12 · B01-12 · Kelembapan Udara", next="#14 · B01-14 · Efek Föhn dan Bayangan Hujan",
   ch=[("Mengembang, memampat, dan proses adiabatik", 6), ("Dasar awan (LCL)", 19), ("Laju adiabatik basah dan panas laten", 26), ("Lebih hangat naik, lebih dingin turun", 31), ("Bola di mangkuk vs di bukit", 36), ("Labil, stabil, labil bersyarat", 41), ("Contoh soal OSN", 50), ("Dua jebakan", 54), ("Ringkasan dan glosarium", 57)],
   titles=["Proses Adiabatik dan Stabilitas Atmosfer: DALR, SALR, LCL", "Kenapa Udara yang Naik Menjadi Dingin?", "Atmosfer Labil vs Stabil: Kenapa Badai Petir Terbentuk"],
   desc="Semprotan deodoran terasa dingin, pompa sepeda terasa hangat. Video ini membahas proses adiabatik, laju adiabatik kering dan basah, dasar awan (LCL) dengan rumus 125 × (T − Td), panas laten, serta atmosfer labil, stabil, dan labil bersyarat, lewat perjalanan Si Gumpal yang naik ke langit.",
   sum=["Udara naik: tekanan turun, mengembang, mendingin tanpa pertukaran panas (adiabatic process).", "Laju adiabatik kering (DALR): ±1 °C per 100 m.", "Dasar awan (LCL) ≈ 125 × (T − Td) meter.", "Laju adiabatik basah (SALR): ±0,5–0,6 °C per 100 m karena panas laten.", "Labil (unstable): udara terus naik, kumulonimbus, badai. Stabil: cerah atau berkabut.", "Labil bersyarat (conditionally unstable): stabil saat kering, labil saat jenuh."],
   tags="proses adiabatik, laju adiabatik kering, laju adiabatik basah, dalr, salr, lcl, dasar awan, panas laten, stabilitas atmosfer, atmosfer labil, atmosfer stabil, labil bersyarat, kumulonimbus"),
 "b01n14": dict(code="B01-14", slug="Efek-Fohn-dan-Bayangan-Hujan", no=14, name="Efek Föhn dan Bayangan Hujan", prev="#13 · B01-13 · Adiabatik dan Stabilitas Atmosfer", next="#15 · B01-15 · Awan dan Mekanisme Hujan",
   ch=[("Perjalanan Si Gumpal melewati gunung", 4), ("Langkah 1: naik kering", 10), ("Langkah 2: naik basah dan hujan", 14), ("Langkah 3: turun kering", 19), ("Kenapa lebih panas?", 25), ("Angin fohn Indonesia", 32), ("Bayangan hujan: Palu", 35), ("Contoh soal OSN", 38), ("Dua jebakan", 43), ("Ringkasan dan glosarium", 47)],
   titles=["Efek Föhn dan Bayangan Hujan: Hitung Langkah demi Langkah", "Satu Gunung, Dua Cuaca: Kenapa Palu Kering?", "Cara Menghitung Suhu Angin Fohn untuk OSN"],
   desc="Di satu sisi gunung hujan hampir setiap hari, di sisi lain panas dan kering. Video ini mengajak Si Gumpal melewati gunung langkah demi langkah: naik kering, naik basah sambil menurunkan hujan, lalu turun kering. Kamu akan paham kenapa lereng bawah angin lebih panas, apa itu angin fohn, dan kenapa Palu menjadi bayangan hujan.",
   sum=["Lereng hadap angin (windward): udara naik, mendingin, jenuh, hujan.", "Naik kering −1 °C/100 m sampai dasar awan, lalu naik basah −0,6 °C/100 m.", "Lereng bawah angin (leeward): turun kering +1 °C/100 m.", "Hasilnya lebih panas dan kering: angin fohn (foehn wind); Gending, Kumbang, Brubu, Bahorok, Wambraw.", "Daerah kering di balik gunung = bayangan hujan (rain shadow), contoh Palu.", "Hitung penurunan dari puncak sampai kota tujuan, bukan sampai permukaan laut."],
   tags="efek fohn, angin fohn, foehn, bayangan hujan, rain shadow, windward, leeward, lereng hadap angin, lereng bawah angin, palu, angin gending, laju adiabatik, hujan orografis"),
 "b01n15": dict(code="B01-15", slug="Awan-dan-Mekanisme-Hujan", no=15, name="Awan dan Mekanisme Hujan", prev="#14 · B01-14 · Efek Föhn dan Bayangan Hujan", next="#16 · B01-16 · Pola Hujan Indonesia",
   ch=[("Bagaimana awan terbentuk", 3), ("Empat kata dasar nama awan", 5), ("Awan rendah, menengah, tinggi", 11), ("Nimbostratus dan kumulonimbus", 17), ("Dari titik awan menjadi hujan", 22), ("Empat cara udara naik", 25), ("Orografi dan konvergensi", 31), ("Frontal", 37), ("Contoh soal OSN", 40), ("Dua jebakan", 44), ("Ringkasan dan glosarium", 47)],
   titles=["Awan dan Mekanisme Hujan: Jenis Awan dan 4 Cara Hujan Terbentuk", "Baca Cuaca dari Bentuk Awan", "Konveksi, Orografi, Konvergensi, Frontal: 4 Jenis Hujan"],
   desc="Awan tipis seperti bulu, seperti kapas, atau abu-abu menutupi langit, semuanya punya arti. Video ini membahas empat kata dasar nama awan, awan rendah, menengah, dan tinggi, kumulonimbus sang awan badai, cara titik awan menjadi butir hujan, dan empat cara udara naik: konveksi, orografi, konvergensi, dan frontal.",
   sum=["Kata dasar: cirrus (serat), stratus (lapisan), cumulus (gumpalan), nimbus (hujan).", "Rendah < 2 km: stratus, kumulus. Menengah 2–7 km: altokumulus, altostratus. Tinggi > 7 km: sirus, sirostratus (halo).", "Nimbostratus: hujan merata dan lama. Kumulonimbus: hujan lebat, petir, hujan es, puncak landasan.", "Titik awan bertabrakan dan bergabung menjadi butir hujan.", "Konveksi (Bogor), orografi (Bukit Barisan), konvergensi (ITCZ), frontal (lintang ±60°).", "Sirus tidak menghasilkan hujan; hujan sore setelah pagi terik = konveksi."],
   tags="jenis awan, awan kumulonimbus, cumulonimbus, awan sirus, stratus, kumulus, nimbostratus, mekanisme hujan, hujan konveksi, hujan orografis, hujan konvergensi, hujan frontal, halo"),
 "b01n16": dict(code="B01-16", slug="Pola-Hujan-Indonesia", no=16, name="Pola Hujan Indonesia", prev="#15 · B01-15 · Awan dan Mekanisme Hujan", next="#17 · B01-17 · Klasifikasi Iklim",
   ch=[("Pola monsunal: huruf U", 3), ("Pola ekuatorial: huruf M", 10), ("ITCZ melintas dua kali", 14), ("Pola lokal: kasus Ambon", 18), ("Mengapa Ambon hujan di bulan Juni", 22), ("Cara menghafal dan jumlah hujan tahunan", 26), ("Contoh soal OSN", 32), ("Dua jebakan", 37), ("Ringkasan dan glosarium", 43)],
   titles=["Pola Hujan Indonesia: Monsunal, Ekuatorial, dan Lokal", "Grafik Hujan Huruf U, M, atau U Terbalik? Cara Cepat Membacanya", "Kenapa Ambon Hujan Saat Jawa Kemarau? Pola Hujan Lokal"],
   desc="Satu grafik curah hujan bulanan bisa langsung memberi tahu letak sebuah wilayah. Video ini membahas tiga pola hujan Indonesia: monsunal (huruf U) yang dikendalikan monsun, ekuatorial (huruf M) karena ITCZ melintas dua kali, dan lokal (U terbalik) seperti di Ambon. Dibahas juga wilayah masing-masing pola, cara cepat menghafalnya, serta perbedaan jumlah hujan tahunan dari Palu sampai Pegunungan Papua.",
   sum=["Monsunal (monsoonal pattern): satu puncak Desember–Januari, kemarau Juni–Agustus; Jawa, Bali, Nusa Tenggara, Sumatra bagian selatan.", "Ekuatorial (equatorial pattern): dua puncak sekitar Maret dan Oktober–November karena ITCZ melintas dua kali; Sumatra bagian tengah-utara, Kalimantan bagian barat-tengah (Pontianak, Padang).", "Lokal (local pattern): puncak Juni–Juli, kebalikan monsunal; Ambon, Seram, sebagian Sulawesi dan Papua, karena angin dari Laut Banda naik di pegunungan.", "Cara menghafal: U = monsunal, M = ekuatorial, U terbalik = lokal.", "Jumlah hujan: Palu sangat kering (bayangan hujan / rain shadow), lereng barat Bukit Barisan dan Pegunungan Papua > 4.000 mm, NTT kemarau terpanjang.", "Jebakan: jangan tertukar puncak monsunal (Desember) dan lokal (Juni); ekuatorial tetap punya dua puncak, bukan merata."],
   tags="pola hujan indonesia, pola hujan monsunal, pola hujan ekuatorial, pola hujan lokal, curah hujan, grafik curah hujan, monsun, itcz, ambon, bayangan hujan, rain shadow, iklim indonesia"),
 "b01n17": dict(code="B01-17", slug="Klasifikasi-Iklim", no=17, name="Klasifikasi Iklim", prev="#16 · B01-16 · Pola Hujan Indonesia", next="#18 · B01-18 · Arus Laut dan Upwelling",
   ch=[("Kelompok iklim Köppen A–E", 4), ("Af, Am, Aw: pohon keputusan", 12), ("Contoh hitung Köppen", 19), ("Schmidt-Ferguson dan nilai Q", 25), ("Oldeman untuk padi", 34), ("Pasangan klasifikasi dan kegunaannya", 37), ("Contoh soal OSN", 41), ("Dua jebakan", 46), ("Ringkasan dan glosarium", 50)],
   titles=["Klasifikasi Iklim Köppen, Schmidt-Ferguson, dan Oldeman", "Iklim Kotamu Tipe Apa? Cara Menentukan Af, Am, Aw", "Nilai Q Schmidt-Ferguson dan Klasifikasi Oldeman untuk OSN"],
   desc="Ahli iklim dunia, ahli kehutanan, dan petani padi butuh peta iklim yang berbeda. Video ini membahas kelompok iklim Köppen A sampai E, cara menentukan Af, Am, dan Aw dengan pohon keputusan, nilai Q Schmidt-Ferguson, bulan basah berturut-turut Oldeman, serta kapan memakai masing-masing klasifikasi.",
   sum=["Köppen: A tropis (bulan terdingin ≥ 18 °C), B kering, C sedang, D dingin, E kutub (bulan terpanas < 10 °C).", "Af: bulan terkering ≥ 60 mm. Am: < 60 mm tetapi ≥ 100 − P/25. Aw: di bawah ambang itu.", "Schmidt-Ferguson: bulan basah > 100 mm, kering < 60 mm; Q = kering ÷ basah × 100%.", "Q makin kecil makin basah (A < 14,3%); makin besar makin kering (H > 700%).", "Oldeman: bulan basah > 200 mm berturut-turut, untuk padi dan palawija.", "Köppen untuk iklim dunia, Schmidt-Ferguson untuk kehutanan, Oldeman untuk tanaman pangan."],
   tags="klasifikasi iklim, koppen, köppen, schmidt ferguson, nilai q, oldeman, af am aw, iklim tropis, hutan hujan tropis, sabana, monsun tropis, agroklimat"),
}
def fmt(t):
    m = int(t % 3600 // 60); s = t % 60
    return f"{int(t//3600):02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000))%1000:03d}"
for film in sys.argv[1:]:
    c = P[film]; tm = json.load(open(f"{V}/{film}/timing.json")); O = f"{V}/out/{film}"
    caps = []
    for uu in tm["units"]:
        ws = [w for w in tm["words"] if w["u"] == uu["i"]]; ch = []
        for k, w in enumerate(ws):
            ch.append(w)
            if len(" ".join(x["w"] for x in ch)) > 70 and k < len(ws) - 1: caps.append([ch[0]["t"], ws[k+1]["t"] - 0.05, " ".join(x["w"] for x in ch)]); ch = []
        if ch: caps.append([ch[0]["t"], uu["v1"] + 0.25, " ".join(x["w"] for x in ch)])
    for i in range(len(caps) - 1): caps[i][1] = min(caps[i][1], caps[i+1][0] - 0.02)
    srt = f"{c['code']}_{c['slug']}.srt"
    with open(f"{O}/{srt}", "w") as f:
        for i, (a, b, s) in enumerate(caps, 1):
            for x, y in REPL: s = re.sub(x, y, s)
            f.write(f"{i}\n{fmt(a)} --> {fmt(b)}\n{s}\n\n")
    chap = ["0:00 Intro"] + [f"{int((tt:=max(3.0, tm['units'][ui]['v0']-0.2))//60)}:{int(tt%60):02d} {n}" for n, ui in c["ch"]]
    chap.append(f"{int((tt:=tm['units'][-1]['v0']-0.2)//60)}:{int(tt%60):02d} Penutup")
    keep = []; last = -99
    for line in chap:
        mm, ss = line.split(' ')[0].split(':'); sec = int(mm) * 60 + int(ss)
        if sec - last >= 10: keep.append(line); last = sec
        elif keep and line.endswith('Penutup'): pass
    chap = keep
    dur = json.load(open(f"{V}/{film}/film.json"))["duration"]
    T = [f"{x} | OSN Geografi 2027" for x in c["titles"]]
    md = f"""# {c['code']} · {c['name']} · Paket Unggah YouTube

Video #{c['no']} jalur belajar Bab 1 Iklim. Pola judul seri: **Judul | OSN Geografi 2027**.

## Opsi judul
""" + "\n".join(f"{i+1}. **{x}** ({len(x)} karakter){' ← rekomendasi' if i == 0 else ''}" for i, x in enumerate(T)) + f"""

## Deskripsi
```
{c['desc']}

Ini video #{c['no']} dari jalur belajar Bab 1 Iklim. Setiap istilah disebut dalam bahasa Indonesia dan istilah asingnya, karena soal OSN sering memakai istilah Inggris.

📌 Latihan soalnya di OSNGEO.id → menu Soal Pendalaman Materi → Bab 1 Iklim
https://osngeo.id

⏱️ Daftar isi
""" + "\n".join(chap) + """

🧠 Ringkasan
""" + "\n".join("• " + s for s in c["sum"]) + f"""

▶️ Sebelumnya: {c['prev']}
▶️ Berikutnya: {c['next']}

Sumber: Modul OSNGEO Bab 1 Iklim. Grafik dan peta disederhanakan.
#OSNGeografi #OSNGeografi2027 #Iklim #OSNGEO
```

## Tag
```
{c['tags']}, osn geografi, osn geografi 2027, olimpiade geografi, materi osn geografi, osngeo
```

## Thumbnail (3 opsi, tema seri seragam)
1. `OSNGEO_{c['code']}_thumb_1_osn.jpg`: untuk siswa OSN (judul besar, jumlah istilah asing).
2. `OSNGEO_{c['code']}_thumb_2_formal_web.jpg`: formal untuk halaman siswa di web.
3. `OSNGEO_{c['code']}_thumb_3_umum.jpg`: penonton umum (pertanyaan pemancing).

## Berkas
- Video: `OSNGEO_{c['code']}_{c['slug']}_FINAL.mp4` (1920×1080, 30 fps, ±{int(dur//60)}:{int(dur%60):02d}, −14 LUFS, {'tanpa subtitle tertempel; unggah file SRT sebagai CC di YouTube' if c['no'] >= 12 else 'subtitle tertempel'})
- Subtitle: `{srt}`
"""
    open(f"{R}/docs/video/{c['code']}_youtube.md", "w").write(md)
    F = f"{V}/FINAL"
    if os.path.exists(f"{O}/final.mp4"): shutil.copy(f"{O}/final.mp4", f"{F}/OSNGEO_{c['code']}_{c['slug']}_FINAL.mp4")
    from PIL import Image
    for n in ["1_osn", "2_formal_web", "3_umum"]:
        Image.open(f"{O}/thumb_{n}.png").convert("RGB").save(f"{F}/OSNGEO_{c['code']}_thumb_{n}.jpg", quality=90)
        shutil.copy(f"{F}/OSNGEO_{c['code']}_thumb_{n}.jpg", f"{R}/docs/video/")
    shutil.copy(f"{O}/{srt}", f"{F}/"); shutil.copy(f"{O}/{srt}", f"{R}/docs/video/")
    D = f"{R}/scripts/video/{film}"; os.makedirs(f"{D}/lib", exist_ok=True)
    for x in ["film.js", "film.json", "index.html", "timing.json", "thumbs.html"]: shutil.copy(f"{V}/{film}/{x}", D)
    shutil.copy(f"{V}/{film}/audio/script.txt", D); shutil.copy(f"{V}/{film}/lib/kit.js", f"{D}/lib/"); shutil.copy(f"{V}/{film}/lib/common.js", f"{D}/lib/")
    print(film, "ok", T[0], len(T[0]))
