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
- Video: `OSNGEO_{c['code']}_{c['slug']}_FINAL.mp4` (1920×1080, 30 fps, ±{int(dur//60)}:{int(dur%60):02d}, −14 LUFS, subtitle tertempel)
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
