from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_talc(path):
    t = np.linspace(0, 10, 300)
    v = 100 / (1 + np.exp(-(t - 4.5) * 1.4))
    fig, ax = new(9, 4.8)
    ax.plot(t, v, color=C["blue"], lw=2.6)
    ax.plot(t[t > 8], v[t > 8][0] + 12 * (t[t > 8] - 8) / 2, "--", color=C["green"]); ax.text(9.6, 112, "peremajaan", fontsize=9, color=C["green"])
    ax.plot(t[t > 8], v[t > 8][0] - 30 * (t[t > 8] - 8) / 2, "--", color=C["red"]); ax.text(9.6, 68, "penurunan", fontsize=9, color=C["red"])
    for b in [1.5, 3.0, 5.5, 6.8, 8.0]:
        ax.axvline(b, color="#CBD5E0", ls=":")
    for lab, x in [("P", 0.75), ("Q", 2.25), ("R", 4.25), ("S", 6.15), ("T", 7.4)]:
        ax.text(x, 122, lab, ha="center", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 132); ax.set_xticks([]); ax.set_xlabel("Waktu →"); ax.set_ylabel("Jumlah wisatawan")
    ax.set_title("Model siklus hidup destinasi wisata (Butler)")
    save(fig, path)


KUNJ = [800, 600, 700, 750, 900, 1100, 1500, 1400, 900, 800, 850, 1800]


def f_musim(path):
    bars(BULAN3, {"Kunjungan (ribu orang)": KUNJ}, path, title="Kunjungan wisatawan bulanan ke Destinasi D (total 12.100 ribu)", ylabel="ribu orang",
         values=True, ylim=(0, 2000), colors=[C["teal"]], w=9.5)


def f_kebocoran(path):
    table([["Jumlah wisatawan per tahun", "200.000 orang"], ["Rata-rata pengeluaran per wisatawan", "Rp2.000.000"], ["Kebocoran (impor, keuntungan ke luar daerah)", "40%"]],
          ["Komponen", "Nilai"], path, title="Data ekonomi pariwisata Pulau P", col_w=[0.62, 0.38])


def f_plog(path):
    x = np.linspace(-3.5, 3.5, 300); y = np.exp(-x ** 2 / 2)
    fig, ax = new(9, 4.4)
    ax.fill_between(x, 0, y, color="#EBF8FF"); ax.plot(x, y, color=C["blue"], lw=2.4)
    for b in [-2, -0.7, 0.7, 2]:
        ax.axvline(b, color="#A0AEC0", ls="--")
    for lab, xx in [("P", -2.75), ("Q", -1.35), ("R", 0), ("S", 1.35), ("T", 2.75)]:
        ax.text(xx, 1.05, lab, ha="center", fontsize=14, fontweight="bold")
    ax.text(-3.4, -0.12, "menyukai yang akrab dan aman", fontsize=9); ax.text(3.4, -0.12, "menyukai petualangan dan hal baru", fontsize=9, ha="right")
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(-0.18, 1.15); ax.set_ylabel("proporsi wisatawan")
    ax.set_title("Sebaran tipe kepribadian wisatawan menurut Plog")
    save(fig, path)


def f_pcc(path):
    table([["Panjang jalur trekking", "1.200 m"], ["Ruang yang dibutuhkan satu pengunjung", "2 m"], ["Jam buka per hari", "8 jam"], ["Lama satu kunjungan", "2 jam"],
           ["Faktor koreksi curah hujan (Cf₁)", "0,8"], ["Faktor koreksi kerentanan tanah (Cf₂)", "0,6"]], ["Parameter", "Nilai"], path,
          title="Data daya dukung jalur trekking Taman Nasional T", col_w=[0.66, 0.34])


DPSP = {"P": (98.9, 2.6), "Q": (110.2, -7.6), "R": (116.3, -8.9), "S": (119.9, -8.5), "T": (125.1, 1.6)}


def f_dpsp(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    for n, (x, y) in DPSP.items():
        ax.plot(x, y, "*", ms=16, color=C["red"], mec="black"); ax.text(x + 0.6, y + 0.7, n, fontsize=13, fontweight="bold", color=C["red"],
                                                                          bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Lima destinasi pariwisata super prioritas")
    save(fig, path)


# ---- paket 1
def f_asal(path):
    bars(["Malaysia", "Australia", "Singapura", "Tiongkok", "India", "Amerika Serikat"], {"Kunjungan (ribu)": [2100, 1700, 1500, 1000, 600, 400]}, path,
         title="Kunjungan wisatawan mancanegara ke Indonesia menurut asal (ilustrasi)", ylabel="ribu kunjungan", values=True, ylim=(0, 2500), colors=[C["blue"]], rot=10, w=9)


def f_enklave(path):
    fig, ax = blank(9.5, 5, (0, 100), (0, 54))
    ax.add_patch(Rectangle((0, 0), 100, 12, fc=C["lblue"])); ax.text(50, 5, "pantai & laut", ha="center", fontsize=10)
    ax.add_patch(Rectangle((8, 12), 52, 32, fc="#FEFCBF", ec="#555", lw=2, ls="--"))
    ax.text(34, 40, "Kawasan resor terpadu (pagar & pos jaga)", ha="center", fontsize=10, fontweight="bold")
    for x, t in [(14, "hotel"), (27, "restoran"), (40, "toko"), (52, "spa")]:
        box(ax, x - 5, 22, 10, 7, t, fc="#FBD38D", fs=8)
    ax.add_patch(Rectangle((68, 14), 28, 26, fc="#E2E8F0", ec="#555")); ax.text(82, 36, "Desa nelayan lokal", ha="center", fontsize=10, fontweight="bold")
    for i in range(10):
        ax.add_patch(Rectangle((70 + (i % 5) * 5, 18 + (i // 5) * 7), 3, 3, fc="#C05621"))
    arrow(ax, 4, 50, 14, 45, color=C["gray"]); ax.text(2, 51.5, "wisatawan dari bandara (bus resor)", fontsize=9)
    ax.set_title("Tata ruang sebuah kawasan wisata pesisir")
    save(fig, path)


def f_rlm(path):
    table([["Jumlah tamu yang menginap", "1.200 orang"], ["Jumlah malam tamu", "3.000 malam"], ["Jumlah kamar", "60 kamar"], ["Kamar terpakai selama 30 hari", "1.260 kamar-malam"]],
          ["Data hotel bulan Juni", "Nilai"], path, title="Data okupansi Hotel H", col_w=[0.62, 0.38])


def f_wisnus(path):
    yr = ["2019", "2020", "2021", "2022", "2023"]
    bars(yr, {"Wisman (juta kunjungan)": [16.1, 4.1, 1.6, 5.5, 11.7]}, path, title="Kunjungan wisatawan mancanegara ke Indonesia", ylabel="juta kunjungan", values=True,
         ylim=(0, 19), colors=[C["purple"]], w=8)


def f_segmen(path):
    table([["Backpacker", "Rp3.000.000", "10 hari"], ["Wisatawan MICE (konferensi)", "Rp9.000.000", "3 hari"], ["Penumpang kapal pesiar", "Rp1.500.000", "1 hari"],
           ["Wisatawan keluarga", "Rp8.000.000", "5 hari"]], ["Segmen", "Biaya/kunjungan", "Lama tinggal"], path,
          title="Pengeluaran wisatawan beberapa segmen", col_w=[0.42, 0.33, 0.25])


# ---- paket 2
def f_tumbuh(path):
    yr = [2016, 2017, 2018, 2019, 2020, 2021]
    v = [200, 300, 420, 500, 540, 550]
    lines(yr, {"Kunjungan (ribu)": v}, path, title="Kunjungan wisatawan ke Pantai K", xlabel="Tahun", ylabel="ribu kunjungan", w=8.5,
          annotate=lambda ax: [ax.text(x, y + 15, str(y), ha="center", fontsize=10) for x, y in zip(yr, v)])


def f_devisa(path):
    bars(["Batu bara", "Minyak sawit", "Pariwisata", "Besi & baja", "Tekstil"], {"Devisa (miliar USD)": [24, 21, 16.9, 20, 12]}, path,
         title="Perkiraan devisa beberapa sektor sebelum pandemi (ilustrasi)", ylabel="miliar USD", values=True, ylim=(0, 28), colors=[C["green"]], w=8.5)


def f_kerja(path):
    bars(["Bali", "NTB", "DIY", "Jawa Timur", "Kalimantan Timur"], {"Pekerja di sektor terkait pariwisata (%)": [48, 22, 25, 12, 8]}, path,
         title="Porsi pekerja di sektor terkait pariwisata (ilustrasi)", ylabel="% dari total pekerja", values=True, ylim=(0, 58), colors=[C["orange"]], w=8.5)


def f_musim2(path):
    lines(BULAN3, {"Destinasi A": [0.8, 0.7, 0.8, 0.9, 1.0, 1.4, 1.9, 1.8, 1.0, 0.7, 0.5, 0.5], "Destinasi B": [1.0, 0.95, 1.0, 1.0, 1.0, 1.05, 1.1, 1.1, 1.0, 0.95, 0.9, 0.95]},
          path, title="Indeks musiman kunjungan dua destinasi", ylabel="indeks musiman", hline=1, w=9)


def f_tpk(path):
    lines(BULAN3, {"TPK (%)": [62, 48, 55, 58, 60, 72, 85, 83, 64, 57, 52, 80]}, path, title="Tingkat penghunian kamar hotel berbintang di Kota W", ylabel="%",
          hline=60, w=9)


# ---- paket 3
def f_rasio(path):
    table([["Destinasi P", "120.000", "4.800.000"], ["Destinasi Q", "800.000", "2.400.000"], ["Destinasi R", "50.000", "100.000"]],
          ["Destinasi", "Penduduk", "Wisatawan per tahun"], path, title="Penduduk dan wisatawan tiga destinasi", col_w=[0.3, 0.32, 0.38])


def f_air(path):
    bars(["Penduduk lokal", "Wisatawan\nhomestay", "Wisatawan hotel\nberbintang", "Wisatawan resor\n+ lapangan golf"], {"Liter per orang per hari": [120, 180, 450, 1500]},
         path, title="Rata-rata penggunaan air bersih (ilustrasi)", ylabel="liter per orang per hari", values=True, ylim=(0, 1700), colors=[C["blue"]], w=8.5)


def f_ecc(path):
    table([["Daya dukung fisik (PCC)", "5.000 kunjungan/hari"], ["Faktor koreksi kemiringan (Cf₁)", "0,7"], ["Faktor koreksi gangguan satwa (Cf₂)", "0,5"],
           ["Kapasitas pengelolaan (MC)", "0,6"]], ["Komponen", "Nilai"], path, title="Analisis daya dukung kawasan wisata alam W", col_w=[0.6, 0.4])


def f_karang(path):
    yr = [2010, 2012, 2014, 2016, 2018, 2020, 2022]
    fig, ax = new(8.5, 4.4)
    ax.bar(yr, [40, 60, 95, 130, 170, 60, 150], width=1.2, color="#CBD5E0", label="Penyelam (ribu/tahun)")
    ax.set_ylabel("ribu penyelam"); ax.set_ylim(0, 260); ax.set_xticks(yr)
    ax2 = ax.twinx(); ax2.plot(yr, [62, 60, 55, 49, 42, 45, 40], color=C["red"], marker="o", lw=2.2, label="Tutupan karang hidup (%)")
    ax2.set_ylabel("% tutupan karang", color=C["red"]); ax2.spines["top"].set_visible(False); ax2.set_ylim(0, 100)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
    ax.set_title("Penyelam dan tutupan karang di Titik Selam S")
    save(fig, path)


def f_gili(path):
    yr = [2005, 2010, 2015, 2020, 2023]
    fig, ax = new(8.5, 4.4)
    ax.plot(yr, [150, 420, 900, 300, 1100], marker="o", color=C["orange"], lw=2.2, label="Wisatawan (ribu/tahun)")
    ax.set_ylabel("ribu wisatawan")
    ax2 = ax.twinx(); ax2.plot(yr, [0.8, 1.6, 3.2, 2.8, 4.1], marker="s", color=C["blue"], lw=2.2, label="Salinitas sumur (‰)")
    ax2.set_ylabel("salinitas (‰)", color=C["blue"]); ax2.spines["top"].set_visible(False); ax.set_xticks(yr)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left")
    ax.set_title("Wisatawan dan salinitas air sumur di sebuah pulau kecil")
    save(fig, path)


# ---- paket 4
def f_jenis(path):
    table([["1", "Mengamati penyu bertelur bersama pemandu desa, sebagian tiket untuk konservasi"], ["2", "Menyusuri singkapan batuan purba dan tebing kaldera"],
           ["3", "Memetik buah dan belajar mengolah kopi di kebun petani"], ["4", "Ziarah ke makam wali dan masjid bersejarah"]],
          ["Paket", "Kegiatan utama"], path, title="Empat paket wisata di Kabupaten W", col_w=[0.12, 0.88], fs=10.5)


GEOPARK = {"P": (110.6, -8.0), "Q": (115.4, -8.25), "R": (106.4, -7.3), "S": (98.8, 2.7), "T": (116.45, -8.4)}


def f_geopark(path):
    fig, ax = indonesia_map(extent=(95, 125, -10.5, 6), w=10, h=5)
    for n, (x, y) in GEOPARK.items():
        dx, dy = {"Q": (-1.3, 0.6), "T": (0.5, -1.4)}.get(n, (0.4, 0.5))
        ax.plot(x, y, "o", ms=10, color=C["green"], mec="black"); ax.text(x + dx, y + dy, n, fontsize=13, fontweight="bold", bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Lokasi beberapa UNESCO Global Geopark di Indonesia")
    save(fig, path)


def f_desawisata(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [35, 20, 10, 10, 25]; lab = ["Pemilik homestay\n(warga)", "Pemandu & seni\n(warga)", "Kas Pokdarwis", "Kas desa (BUMDes)", "Agen perjalanan\nluar daerah"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=[C["green"], C["lgreen"], C["teal"], C["blue"], C["gray"]], startangle=90, wedgeprops=dict(ec="white"),
           textprops=dict(fontsize=9))
    ax.set_title("Pembagian pendapatan paket wisata Desa Wisata N")
    save(fig, path)


def f_kategori(path):
    table([["Rintisan", "potensi ada, belum ada pengelola dan kunjungan"], ["Berkembang", "mulai dikenal, ada kunjungan, sarana terbatas"],
           ["Maju", "dikelola Pokdarwis/BUMDes, fasilitas memadai, promosi digital"], ["Mandiri", "inovatif, standar mutu, pasar mancanegara, berkelanjutan"]],
          ["Kategori", "Ciri utama"], path, title="Klasifikasi desa wisata", col_w=[0.22, 0.78], fs=10.5)


def f_tbl(path):
    fig, ax = blank(7, 6.2, (0, 100), (0, 90))
    for (x, y, c, t) in [(35, 58, "#9AE6B4", "X"), (65, 58, "#FBD38D", "Y"), (50, 32, "#BEE3F8", "Z")]:
        ax.add_patch(Circle((x, y), 24, fc=c, ec="#555", alpha=0.65)); ax.text(x + (x - 50) * 0.5, y + (y - 49) * 0.6, t, fontsize=16, fontweight="bold")
    ax.text(50, 50, "pariwisata\nberkelanjutan", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(16, 86, "X: kelestarian lingkungan · Y: manfaat ekonomi · Z: ?", fontsize=10)
    ax.set_title("Tiga pilar pariwisata berkelanjutan")
    save(fig, path)


# ---- paket 5
def f_covid(path):
    bars(["2019", "2020", "2021", "2022", "2023", "2024"], {"Wisman ke Bali (juta)": [6.3, 1.1, 0.0, 2.2, 5.3, 6.3]}, path, title="Kunjungan wisatawan mancanegara ke Bali",
         ylabel="juta kunjungan", values=True, ylim=(0, 7.5), colors=[C["teal"]], w=8)


def f_krisis(path):
    yr = list(range(2000, 2020))
    v = [1.4, 1.36, 1.29, 0.99, 1.46, 1.39, 1.26, 1.66, 1.97, 2.23, 2.49, 2.76, 2.89, 3.28, 3.77, 4.0, 4.93, 5.7, 6.07, 6.27]
    lines(yr, {"Wisman ke Bali (juta)": v}, path, title="Kunjungan wisman ke Bali 2000–2019", xlabel="Tahun", ylabel="juta", w=9, markers=True,
          xticks=yr[::2], ylim=(0, 7),
          annotate=lambda ax: [ax.annotate(t, (x, y), xytext=(0, 40), textcoords="offset points", ha="center", fontsize=13, fontweight="bold", color=C["red"],
                                           arrowprops=dict(arrowstyle="->", color=C["red"])) for t, x, y in [("K", 2003, 0.99), ("L", 2006, 1.26)]])


def f_daring(path):
    lines([2015, 2017, 2019, 2021, 2023], {"Pemesanan akomodasi secara daring (%)": [28, 41, 55, 68, 74]}, path, title="Porsi pemesanan akomodasi secara daring (ilustrasi)",
          xlabel="Tahun", ylabel="%", w=8)


def f_zonasi(path):
    fig, ax = blank(8, 6.2, (0, 100), (0, 80))
    ax.add_patch(Polygon([(5, 5), (95, 8), (92, 75), (10, 72)], fc="#C6F6D5", ec="#2F855A", lw=2))
    ax.add_patch(Polygon([(30, 30), (70, 28), (68, 60), (35, 62)], fc="#2F855A", ec="black")); ax.text(51, 46, "K", fontsize=18, fontweight="bold", color="white")
    ax.add_patch(Polygon([(70, 10), (93, 12), (91, 30), (72, 28)], fc="#FBD38D", ec="black")); ax.text(81, 19, "M", fontsize=16, fontweight="bold")
    ax.add_patch(Polygon([(8, 50), (28, 50), (30, 70), (11, 70)], fc="#BEE3F8", ec="black")); ax.text(19, 60, "N", fontsize=16, fontweight="bold")
    ax.text(18, 15, "L", fontsize=16, fontweight="bold")
    ax.set_title("Zonasi sebuah taman nasional")
    ax.text(50, 0.5, "K = zona inti · L = zona rimba · M = zona pemanfaatan · N = zona tradisional", ha="center", fontsize=9)
    save(fig, path)


def f_pasar(path):
    bars(["Destinasi X", "Destinasi Y"], {"Pasar asal terbesar": [62, 18], "Pasar kedua": [10, 15], "Pasar ketiga": [8, 14], "Pasar lainnya": [20, 53]}, path,
         title="Komposisi asal wisatawan dua destinasi (%)", ylabel="%", stacked=True, values=True, ylim=(0, 165),
         colors=[C["red"], C["orange"], C["yellow"], C["lgray"]], w=7.5, legend_loc="upper center")


# ============================ questions ============================
P0 = [
    Q("Perhatikan model siklus hidup destinasi wisata Butler berikut.\n\nTahap yang ditandai jumlah wisatawan mencapai puncak, kapasitas terlampaui, citra mulai menurun, dan destinasi bergantung pada wisatawan ulangan adalah …",
      ["T, stagnasi", "P, eksplorasi", "Q, keterlibatan", "R, pembangunan", "S, konsolidasi"],
      "Model TALC (Tourism Area Life Cycle) Butler (1980) terdiri atas beberapa tahap:\n• P – eksplorasi: wisatawan sedikit, petualang, fasilitas minim.\n• Q – keterlibatan: warga lokal mulai menyediakan layanan, kunjungan meningkat.\n• R – pembangunan: kunjungan melonjak, investasi luar masuk, promosi gencar.\n• S – konsolidasi: pertumbuhan melambat, pariwisata dominan dalam ekonomi lokal.\n• T – stagnasi: kunjungan mencapai puncak, daya dukung terlampaui, masalah lingkungan dan sosial muncul, citra menurun, bergantung pada wisatawan ulangan.\nSetelah stagnasi, destinasi dapat mengalami penurunan atau peremajaan (rejuvenation) melalui atraksi baru atau penataan ulang.\n\nPengecoh: tahap lain belum mencapai puncak kunjungan.",
      f_talc),
    Q("Sebuah hotel memiliki 50 kamar. Selama bulan April (30 hari), jumlah kamar yang terjual 1.050 kamar-malam. Tingkat penghunian kamar (TPK) hotel tersebut adalah …",
      ["70%", "35%", "21%", "143%", "47%"],
      "TPK = kamar terpakai ÷ kamar tersedia × 100%.\nKamar tersedia = 50 kamar × 30 hari = 1.500 kamar-malam.\nTPK = 1.050 ÷ 1.500 × 100% = 70%.\nTPK adalah indikator utama kinerja akomodasi. Nilai di atas sekitar 60% biasanya dianggap sehat untuk hotel, walaupun angkanya berbeda menurut musim dan segmen pasar.\n\nPengecoh: 35% membagi dengan 3.000 (salah menghitung hari). 21% membagi 1.050 dengan 50 × 100. 143% membalik pembagian. 47% tidak sesuai perhitungan.",
      None),
    Q("Perhatikan grafik kunjungan wisatawan bulanan ke Destinasi D berikut. Indeks musiman = kunjungan bulan i ÷ rata-rata bulanan.\n\nBulan dengan indeks musiman tertinggi beserta nilainya adalah …",
      ["Desember, sekitar 1,8", "Juli, sekitar 1,5", "Desember, sekitar 0,15", "Februari, sekitar 0,6", "Juli, sekitar 1,0"],
      "Rata-rata kunjungan bulanan = 12.100 ÷ 12 ≈ 1.008 ribu.\nKunjungan Desember 1.800 ribu → indeks = 1.800 ÷ 1.008 ≈ 1,79 ≈ 1,8.\nKunjungan Juli 1.500 ribu → indeks ≈ 1,49.\nFebruari 600 ribu → indeks ≈ 0,60 (terendah).\nIndeks di atas 1 menunjukkan musim ramai (high season), misalnya liburan akhir tahun dan libur sekolah pertengahan tahun, sedangkan di bawah 1 menunjukkan musim sepi. Musiman yang tajam menimbulkan masalah seperti kepadatan dan lonjakan harga di musim ramai serta pengangguran musiman di musim sepi.\n\nPengecoh: Juli tinggi tetapi bukan tertinggi. 0,15 adalah kesalahan pembagian. Februari justru terendah.",
      f_musim),
    Q("Dalam komponen destinasi 4A (attraction, accessibility, amenity, ancillary), hotel, restoran, dan toko cendera mata termasuk komponen …",
      ["Amenitas", "Atraksi", "Aksesibilitas", "Ansilari (kelembagaan)", "Atraksi dan aksesibilitas"],
      "Komponen destinasi wisata 4A:\n• Atraksi (attraction): daya tarik yang menjadi alasan wisatawan datang, misalnya pantai, candi, festival, dan kuliner khas.\n• Aksesibilitas (accessibility): kemudahan mencapai destinasi, misalnya bandara, pelabuhan, jalan, dan transportasi lokal.\n• Amenitas (amenity): fasilitas pendukung selama berada di destinasi, misalnya akomodasi, restoran, toko cendera mata, toilet, dan ATM.\n• Ansilari (ancillary): kelembagaan dan layanan pendukung, misalnya pengelola destinasi, pusat informasi, asosiasi, dan pemandu berlisensi.\n\nPengecoh: hotel dan restoran bukan alasan utama berwisata (atraksi), bukan sarana menuju destinasi (aksesibilitas), dan bukan kelembagaan (ansilari).",
      None),
    Q("Perhatikan data ekonomi pariwisata Pulau P berikut.\n\nPendapatan pariwisata yang benar-benar tinggal dalam ekonomi lokal per tahun adalah …",
      ["Rp240 miliar", "Rp400 miliar", "Rp160 miliar", "Rp800 miliar", "Rp2,4 miliar"],
      "1) Pendapatan kotor = jumlah wisatawan × pengeluaran per wisatawan = 200.000 × Rp2.000.000 = Rp400 miliar.\n2) Kebocoran 40% berarti hanya 60% yang tinggal di ekonomi lokal.\n3) Pendapatan yang tinggal = Rp400 miliar × (1 − 0,40) = Rp240 miliar.\nKebocoran (leakage) terjadi ketika uang wisatawan mengalir keluar daerah, misalnya untuk mengimpor makanan dan minuman, membayar keuntungan pemilik hotel dari luar daerah atau luar negeri, gaji tenaga kerja dari luar, dan komisi agen perjalanan asing.\n\nPengecoh: Rp400 miliar adalah pendapatan kotor. Rp160 miliar adalah bagian yang bocor. Rp800 miliar dan Rp2,4 miliar adalah kesalahan perhitungan.",
      f_kebocoran),
    Q("Di sebuah destinasi, rata-rata 60% tambahan pendapatan warga dibelanjakan kembali untuk barang dan jasa lokal (MPC lokal = 0,6). Jika wisatawan membelanjakan Rp10 miliar, dampak total terhadap ekonomi lokal menurut efek pengganda adalah …",
      ["Rp25 miliar", "Rp16 miliar", "Rp6 miliar", "Rp60 miliar", "Rp10 miliar"],
      "Efek pengganda k = 1 ÷ (1 − MPC lokal) = 1 ÷ (1 − 0,6) = 1 ÷ 0,4 = 2,5.\nDampak total = k × belanja awal = 2,5 × Rp10 miliar = Rp25 miliar.\nUang wisatawan berputar beberapa kali: diterima pemilik homestay, dibelanjakan ke pedagang sayur, lalu dibelanjakan lagi, dan seterusnya. Semakin besar porsi belanja yang tetap di dalam ekonomi lokal (kebocoran kecil), semakin besar efek pengganda.\n\nPengecoh: Rp16 miliar menjumlahkan belanja awal dan satu putaran. Rp6 miliar hanya putaran pertama. Rp60 miliar dan Rp10 miliar tidak sesuai rumus.",
      None),
    Q("Perhatikan sebaran tipe kepribadian wisatawan menurut Plog berikut.\n\nWisatawan yang paling mungkin menjadi pengunjung pertama ke destinasi terpencil yang belum dikenal, seperti pulau-pulau terluar, berada pada kelompok …",
      ["T, alosentris", "P, psikosentris", "R, midsentris", "Q, mendekati psikosentris", "P dan T secara bersamaan"],
      "Stanley Plog membagi wisatawan menurut kepribadian dalam kurva normal:\n• Psikosentris (P): menyukai yang akrab, aman, dan nyaman; memilih destinasi populer dengan fasilitas lengkap dan sering memakai paket wisata.\n• Midsentris (R): kelompok terbesar di tengah, menyukai destinasi yang sudah cukup dikenal.\n• Alosentris (T): menyukai petualangan, hal baru, dan interaksi dengan budaya lokal; bersedia menerima fasilitas minim dan sering menjadi \"perintis\" yang menemukan destinasi baru.\nSeiring destinasi berkembang dan makin populer, jenis wisatawannya bergeser dari alosentris ke midsentris lalu psikosentris, yang berkaitan dengan siklus hidup destinasi.\n\nPengecoh: psikosentris dan midsentris tidak cenderung mencari destinasi terpencil.",
      f_plog),
    Q("Menurut tipologi Erik Cohen, wisatawan yang menghindari jalur wisata umum, hidup bersama penduduk lokal, dan tidak memakai fasilitas wisata formal disebut …",
      ["Drifter (pengembara)", "Organized mass tourist", "Individual mass tourist", "Explorer (penjelajah)", "Wisatawan bisnis (MICE)"],
      "Cohen (1972) membagi wisatawan menjadi empat tipe:\n• Organized mass tourist: membeli paket wisata lengkap dan bergerak dalam rombongan dengan jadwal ketat.\n• Individual mass tourist: memakai fasilitas wisata massal, tetapi mengatur sebagian perjalanannya sendiri.\n• Explorer: mengatur perjalanan sendiri, mencari tempat yang belum ramai, tetapi masih memakai akomodasi yang nyaman.\n• Drifter: sepenuhnya menghindari jalur dan fasilitas wisata formal, hidup bersama masyarakat lokal, dan mengikuti gaya hidup setempat.\nCiri pada soal sesuai dengan drifter. Explorer mirip, tetapi masih memakai sebagian fasilitas wisata.\n\nPengecoh: wisatawan massal memakai fasilitas formal. MICE adalah segmen perjalanan bisnis.",
      None),
    Q("Perhatikan data daya dukung jalur trekking Taman Nasional T berikut. PCC = (panjang jalur ÷ ruang per pengunjung) × (jam buka ÷ lama kunjungan) dan RCC = PCC × Cf₁ × Cf₂.\n\nNilai daya dukung riil (RCC) jalur tersebut adalah …",
      ["1.152 kunjungan per hari", "2.400 kunjungan per hari", "600 kunjungan per hari", "1.920 kunjungan per hari", "3.360 kunjungan per hari"],
      "1) Jumlah pengunjung bersamaan = 1.200 m ÷ 2 m = 600 orang.\n2) Faktor rotasi Rf = jam buka ÷ lama kunjungan = 8 ÷ 2 = 4.\n3) PCC = 600 × 4 = 2.400 kunjungan per hari.\n4) RCC = PCC × Cf₁ × Cf₂ = 2.400 × 0,8 × 0,6 = 1.152 kunjungan per hari.\nFaktor koreksi mengurangi daya dukung karena kondisi yang membatasi kunjungan, seperti hujan dan tanah yang rentan erosi. Bila dikalikan lagi dengan kapasitas pengelolaan (MC), diperoleh daya dukung efektif (ECC).\n\nPengecoh: 2.400 adalah PCC. 600 adalah jumlah pengunjung bersamaan tanpa rotasi. 1.920 hanya memakai Cf₁. 3.360 menjumlahkan faktor koreksi secara keliru.",
      f_pcc),
    Q("Perhatikan peta lima destinasi pariwisata super prioritas berikut.\n\nDestinasi Labuan Bajo, gerbang menuju Taman Nasional Komodo, ditunjukkan oleh label …",
      ["S", "P", "Q", "R", "T"],
      "Lima destinasi pariwisata super prioritas (DPSP) pada peta:\n• P: Danau Toba, Sumatera Utara.\n• Q: Borobudur dan sekitarnya, Jawa Tengah–DIY.\n• R: Mandalika, Lombok, NTB.\n• S: Labuan Bajo, ujung barat Pulau Flores, NTT, gerbang ke Taman Nasional Komodo.\n• T: Likupang, Sulawesi Utara.\nPengembangan DPSP bertujuan memeratakan pariwisata di luar Bali melalui pembangunan infrastruktur, amenitas, dan promosi. Tantangannya antara lain menjaga daya dukung lingkungan, misalnya pembatasan kunjungan di Taman Nasional Komodo, dan memastikan manfaat bagi masyarakat lokal.\n\nPengecoh: label lain menunjukkan destinasi super prioritas yang berbeda.",
      f_dpsp),
]

P1 = [
    Q("Perhatikan grafik kunjungan wisatawan mancanegara ke Indonesia menurut asal berikut.\n\nPola yang paling tepat dijelaskan oleh konsep peluruhan jarak adalah …",
      ["Negara tetangga dekat menyumbang kunjungan terbanyak", "Negara terjauh selalu menyumbang kunjungan terbanyak",
       "Jumlah penduduk negara asal tidak berpengaruh sama sekali", "Kunjungan dari semua negara sama besar", "Wisatawan Amerika paling banyak karena jaraknya terdekat"],
      "Grafik menunjukkan Malaysia, Australia, dan Singapura menyumbang kunjungan terbanyak (±1,5–2,1 juta), sedangkan Amerika Serikat yang jauh hanya ±0,4 juta. Pola ini sesuai dengan peluruhan jarak (distance decay): semakin jauh negara asal, semakin besar biaya, waktu perjalanan, dan perbedaan budaya, sehingga kunjungan cenderung lebih sedikit. Tiongkok dan India tetap menyumbang cukup banyak karena jumlah penduduk dan kelas menengahnya sangat besar, sehingga jarak bukan satu-satunya faktor (sesuai model gravitasi).\n\nPengecoh: negara terjauh justru menyumbang lebih sedikit. Jumlah penduduk tetap berpengaruh. Kunjungan tidak sama. Amerika Serikat tidak dekat dengan Indonesia.",
      f_asal),
    Q("Dalam teori motivasi perjalanan, keinginan wisatawan untuk mencari pengalaman baru, belajar budaya lain, dan mengembangkan diri termasuk motivasi …",
      ["Pengembangan dan aktualisasi diri", "Kebutuhan fisiologis dasar", "Tekanan sosial untuk bekerja", "Kebutuhan keamanan finansial", "Keharusan perjalanan dinas"],
      "Motivasi berwisata sering dijelaskan dengan faktor pendorong (push) dari dalam diri, misalnya ingin melepas penat, mencari pengalaman baru, prestise, atau pengembangan diri, dan faktor penarik (pull) dari destinasi, misalnya keindahan alam dan budaya. Model tangga karier perjalanan (travel career ladder) Pearce, yang terinspirasi hierarki kebutuhan Maslow, menyatakan bahwa motivasi wisatawan berkembang dari relaksasi dan kebutuhan dasar menuju hubungan sosial, harga diri, hingga pengembangan diri dan aktualisasi diri. Keinginan belajar budaya dan mengembangkan diri berada pada tingkat atas.\n\nPengecoh: kebutuhan fisiologis dan keamanan berada di tingkat bawah. Tekanan bekerja dan perjalanan dinas bukan motivasi wisata pengembangan diri.",
      None),
    Q("Perhatikan tata ruang sebuah kawasan wisata pesisir berikut.\n\nMasalah utama pola pariwisata yang digambarkan adalah …",
      ["Manfaat ekonomi bagi desa kecil karena wisatawan tertahan di resor", "Wisatawan terlalu sering berinteraksi dengan nelayan lokal",
       "Desa nelayan memperoleh seluruh pendapatan dari resor", "Resor tidak memiliki fasilitas sehingga wisatawan belanja di desa", "Tidak ada akses ke pantai bagi wisatawan"],
      "Gambar menunjukkan pariwisata enklave: kawasan resor terpadu berpagar dengan hotel, restoran, toko, dan spa sendiri, sementara wisatawan diangkut langsung dari bandara dengan bus resor. Desa nelayan lokal berada di luar pagar. Akibatnya interaksi dan belanja wisatawan di luar resor sangat sedikit, sehingga manfaat ekonomi bagi masyarakat lokal kecil, kebocoran pendapatan besar (terutama bila pemilik dan pemasok berasal dari luar), dan dapat muncul kesenjangan serta kecemburuan sosial. Masyarakat juga dapat kehilangan akses ke pantai yang sebelumnya menjadi ruang hidup mereka.\n\nPengecoh: interaksi justru sedikit. Desa tidak memperoleh seluruh pendapatan. Resor memiliki fasilitas lengkap. Wisatawan memiliki akses pantai di dalam kawasan resor.",
      f_enklave),
    Q("Menurut model destinasi Gunn, kawasan wisata terdiri atas atraksi, komunitas atau pusat layanan, dan koridor penghubung. Peran koridor penghubung adalah …",
      ["Menghubungkan gerbang, pusat layanan, dan atraksi", "Menjadi lokasi utama akomodasi berbintang lima",
       "Menggantikan atraksi wisata sebagai alasan utama kunjungan", "Membatasi wisatawan agar tidak keluar dari hotel", "Menjadi tempat pembuangan sampah wisata"],
      "Clare Gunn menggambarkan destinasi sebagai sistem keruangan yang terdiri atas: pintu masuk (gateway, misalnya bandara atau pelabuhan), komunitas atau pusat layanan (kota yang menyediakan akomodasi, makanan, dan layanan), kluster atraksi, serta koridor penghubung (jalan, jalur transportasi, dan jalur wisata) yang menghubungkan semua unsur tersebut. Koridor yang baik membuat perjalanan antaratraksi nyaman dan bahkan menjadi pengalaman wisata, misalnya jalur panorama.\n\nPengecoh: akomodasi berada di pusat layanan. Koridor tidak menggantikan atraksi. Koridor tidak membatasi wisatawan di hotel. Koridor bukan tempat pembuangan sampah.",
      None),
    Q("Perhatikan data okupansi Hotel H bulan Juni berikut.\n\nRata-rata lama menginap (RLM) dan TPK hotel tersebut adalah …",
      ["2,5 malam dan 70%", "0,4 malam dan 70%", "2,5 malam dan 50%", "1,05 malam dan 21%", "3,0 malam dan 70%"],
      "• RLM = jumlah malam tamu ÷ jumlah tamu = 3.000 ÷ 1.200 = 2,5 malam.\n• Kamar tersedia = 60 kamar × 30 hari = 1.800 kamar-malam.\n• TPK = 1.260 ÷ 1.800 × 100% = 70%.\nRLM yang lebih panjang umumnya menguntungkan karena pengeluaran wisatawan di destinasi bertambah tanpa biaya perjalanan tambahan. Strategi memperpanjang RLM antara lain mengembangkan paket wisata keliling dan atraksi di sekitar destinasi utama.\n\nPengecoh: 0,4 malam membalik pembagian. TPK 50% dan 21% salah menghitung kamar tersedia. 3,0 malam salah membaca data.",
      f_rlm),
    Q("Kunjungan ke sebuah destinasi naik dari 1,00 juta menjadi 1,44 juta dalam dua tahun. Laju pertumbuhan rata-rata majemuk per tahun adalah …",
      ["20%", "22%", "44%", "12%", "14,4%"],
      "Laju rata-rata majemuk r = (Vₜ ÷ V₀)^(1/t) − 1 = (1,44 ÷ 1,00)^(1/2) − 1 = √1,44 − 1 = 1,2 − 1 = 0,2 = 20% per tahun.\nPemeriksaan: 1,00 × 1,2 = 1,20 juta pada tahun pertama, lalu 1,20 × 1,2 = 1,44 juta pada tahun kedua.\n\nPengecoh: 22% adalah laju linear (44% ÷ 2). 44% adalah pertumbuhan total dua tahun. 12% dan 14,4% berasal dari kesalahan desimal.",
      None),
    Q("Perhatikan grafik kunjungan wisatawan mancanegara ke Indonesia berikut.\n\nPersentase pemulihan kunjungan pada 2023 dibandingkan 2019 adalah sekitar …",
      ["73%", "27%", "137%", "64%", "116%"],
      "Pemulihan = kunjungan 2023 ÷ kunjungan 2019 × 100% = 11,7 ÷ 16,1 × 100% ≈ 72,7% ≈ 73%.\nArtinya pada 2023 kunjungan wisman telah kembali sekitar tiga perempat dari tingkat sebelum pandemi. Grafik juga menunjukkan dampak pandemi COVID-19: kunjungan anjlok menjadi 4,1 juta (2020) dan 1,6 juta (2021) akibat pembatasan perjalanan, lalu pulih bertahap.\n\nPengecoh: 27% adalah kekurangan dibandingkan 2019. 137% membalik pembagian. 64% dan 116% tidak sesuai perhitungan.",
      f_wisnus),
    Q("Ketika harga tiket pesawat ke sebuah pulau naik tajam, kunjungan wisatawan domestik turun lebih besar daripada wisatawan mancanegara kelas atas. Penjelasan yang paling tepat adalah …",
      ["Permintaan wisatawan domestik lebih elastis terhadap harga", "Wisatawan mancanegara tidak membayar tiket pesawat",
       "Wisatawan domestik tidak pernah memakai pesawat", "Harga tiket tidak memengaruhi permintaan wisata", "Wisatawan kelas atas selalu lebih sensitif terhadap harga"],
      "Elastisitas harga permintaan menunjukkan seberapa besar perubahan jumlah permintaan ketika harga berubah. Wisatawan domestik, terutama segmen menengah, memiliki anggaran terbatas dan banyak pilihan destinasi pengganti yang lebih dekat atau murah, sehingga permintaannya lebih elastis: kenaikan harga tiket membuat mereka menunda perjalanan atau memilih destinasi lain. Wisatawan mancanegara kelas atas umumnya kurang sensitif terhadap harga (inelastis) karena tiket hanya sebagian kecil dari total anggaran dan mereka mencari pengalaman khusus.\n\nPengecoh: wisatawan mancanegara tetap membayar tiket. Wisatawan domestik juga memakai pesawat. Harga jelas memengaruhi permintaan. Wisatawan kelas atas justru kurang sensitif.",
      None),
    Q("Perhatikan data pengeluaran wisatawan beberapa segmen berikut.\n\nSegmen dengan pengeluaran per hari tertinggi adalah …",
      ["Wisatawan MICE, sekitar Rp3 juta per hari", "Wisatawan keluarga, sekitar Rp8 juta per hari", "Backpacker, sekitar Rp3 juta per hari",
       "Penumpang kapal pesiar, sekitar Rp1,5 juta per hari", "Wisatawan keluarga, sekitar Rp1,6 juta per hari"],
      "Pengeluaran per hari = pengeluaran per kunjungan ÷ lama tinggal.\n• Backpacker: 3.000.000 ÷ 10 = Rp300.000 per hari.\n• MICE: 9.000.000 ÷ 3 = Rp3.000.000 per hari.\n• Kapal pesiar: 1.500.000 ÷ 1 = Rp1.500.000 per hari.\n• Keluarga: 8.000.000 ÷ 5 = Rp1.600.000 per hari.\nWisatawan MICE (meeting, incentive, convention, exhibition) memiliki pengeluaran per hari tertinggi karena biasanya dibiayai lembaga, menginap di hotel berbintang, dan memakai banyak layanan. Backpacker berbelanja sedikit per hari, tetapi tinggal lama sehingga uangnya sering lebih banyak beredar di usaha lokal kecil.\n\nPengecoh: Rp8 juta adalah pengeluaran per kunjungan keluarga, bukan per hari. Backpacker hanya Rp300 ribu per hari. Kapal pesiar dan keluarga lebih rendah daripada MICE.",
      f_segmen),
    Q("Wisatawan yang datang khusus untuk menyelam di Raja Ampat, mendaki Gunung Rinjani, atau mengamati burung di Taman Nasional Way Kambas termasuk jenis …",
      ["Wisata minat khusus", "Wisata massal", "Wisata bisnis (MICE)", "Wisata religi", "Wisata belanja"],
      "Wisata minat khusus (special interest tourism) adalah perjalanan yang didorong oleh minat atau hobi tertentu, sehingga wisatawannya memiliki motivasi kuat, keterampilan atau pengetahuan khusus, dan kesediaan menghadapi tantangan. Contohnya menyelam, mendaki gunung, mengamati burung, arung jeram, fotografi alam, dan wisata sejarah tertentu. Segmen ini umumnya jumlahnya kecil, tetapi tinggal lebih lama, berbelanja relatif tinggi, dan lebih peduli terhadap kelestarian.\n\nPengecoh: wisata massal dilakukan dalam jumlah besar dengan paket standar. MICE adalah perjalanan bisnis. Wisata religi bertujuan ibadah atau ziarah. Wisata belanja bertujuan berbelanja.",
      None),
]

P2 = [
    Q("Perhatikan grafik kunjungan wisatawan ke Pantai K berikut.\n\nBerdasarkan pola pertumbuhannya, Pantai K paling mungkin berada pada tahap siklus hidup destinasi …",
      ["Konsolidasi menuju stagnasi", "Eksplorasi oleh perintis", "Keterlibatan awal warga", "Peremajaan setelah stagnasi", "Penurunan tajam kunjungan"],
      "Hitung pertumbuhan tahunan:\n• 2017: (300 − 200) ÷ 200 = 50%.\n• 2018: (420 − 300) ÷ 300 = 40%.\n• 2019: (500 − 420) ÷ 420 ≈ 19%.\n• 2020: (540 − 500) ÷ 500 = 8%.\n• 2021: (550 − 540) ÷ 540 ≈ 1,9%.\nPertumbuhan sangat cepat pada awal periode (tahap pembangunan), kemudian melambat tajam hingga hampir nol, sementara jumlah kunjungan sudah besar. Pola ini menunjukkan destinasi berada pada tahap konsolidasi menuju stagnasi dalam model Butler. Pengelola perlu mewaspadai kapasitas yang terlampaui dan merencanakan diversifikasi atraksi.\n\nPengecoh: eksplorasi dan keterlibatan dicirikan kunjungan kecil. Peremajaan memerlukan kenaikan baru setelah stagnasi. Kunjungan tidak menurun tajam.",
      f_tumbuh),
    Q("Faktor yang paling memperbesar kebocoran (leakage) pendapatan pariwisata di sebuah pulau kecil adalah …",
      ["Hotel milik asing dan bahan makanan diimpor", "Wisatawan menginap di homestay milik warga",
       "Restoran membeli ikan dan sayur dari nelayan dan petani setempat", "Pemandu wisata berasal dari penduduk desa", "Cendera mata dibuat oleh perajin lokal"],
      "Kebocoran pariwisata adalah bagian pengeluaran wisatawan yang keluar dari ekonomi lokal. Kebocoran besar terjadi bila hotel dan agen perjalanan dimiliki pihak luar sehingga keuntungan dikirim keluar, bahan makanan dan minuman diimpor, tenaga kerja manajerial didatangkan dari luar, serta promosi dan komisi dibayarkan kepada perusahaan asing. Pulau kecil sangat rentan karena produksi lokalnya terbatas.\nSebaliknya, homestay milik warga, pembelian bahan lokal, pemandu lokal, dan cendera mata buatan perajin setempat mengurangi kebocoran dan memperbesar efek pengganda.\n\nPengecoh: semua opsi lain justru menahan uang di ekonomi lokal.",
      None),
    Q("Perhatikan grafik perkiraan devisa beberapa sektor sebelum pandemi berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Devisa pariwisata setara sektor komoditas utama", "Pariwisata adalah penghasil devisa terbesar melebihi batu bara",
       "Pariwisata tidak menghasilkan devisa sama sekali", "Tekstil menghasilkan devisa terbesar di antara sektor tersebut", "Devisa pariwisata lebih kecil daripada tekstil"],
      "Grafik menunjukkan devisa pariwisata sekitar 16,9 miliar USD, berada di kisaran yang sama dengan sektor komoditas utama seperti besi dan baja (±20), minyak sawit (±21), dan batu bara (±24), serta lebih besar daripada tekstil (±12). Artinya pariwisata adalah salah satu penghasil devisa penting Indonesia. Pariwisata juga bersifat padat karya dan dapat menyebarkan manfaat ke banyak daerah, tetapi sangat rentan terhadap guncangan seperti pandemi, bencana, dan isu keamanan.\n\nPengecoh: pariwisata tidak melebihi batu bara. Pariwisata jelas menghasilkan devisa. Tekstil justru terendah. Devisa pariwisata lebih besar daripada tekstil.",
      f_devisa),
    Q("Pendapatan pariwisata yang tinggal di sebuah desa adalah Rp3 miliar per tahun, sedangkan biaya yang ditanggung warga (misalnya pengelolaan sampah dan kenaikan harga) Rp600 juta. Jika desa memiliki 400 KK, manfaat bersih rata-rata per KK adalah …",
      ["Rp6 juta per tahun", "Rp7,5 juta per tahun", "Rp1,5 juta per tahun", "Rp9 juta per tahun", "Rp2,4 juta per tahun"],
      "Manfaat bersih desa = pendapatan yang tinggal − biaya yang ditanggung warga = Rp3.000 juta − Rp600 juta = Rp2.400 juta.\nManfaat bersih per KK = Rp2.400 juta ÷ 400 KK = Rp6 juta per tahun.\nAnalisis manfaat bersih penting karena pariwisata juga menimbulkan biaya, seperti sampah, kemacetan, kenaikan harga lahan dan kebutuhan pokok, serta beban infrastruktur. Selain rata-rata, distribusi manfaat antarwarga juga perlu diperhatikan agar tidak hanya dinikmati sebagian kecil.\n\nPengecoh: Rp7,5 juta tidak mengurangkan biaya. Rp1,5 juta membagi biaya dengan jumlah KK. Rp9 juta menjumlahkan pendapatan dan biaya. Rp2,4 juta lupa membagi dengan jumlah KK secara tepat (salah satuan).",
      None),
    Q("Perhatikan grafik porsi pekerja di sektor terkait pariwisata berikut.\n\nRisiko utama bagi provinsi dengan porsi tertinggi adalah …",
      ["Ekonomi sangat rentan terhadap guncangan pariwisata", "Pengangguran tidak mungkin terjadi karena pariwisata selalu ramai",
       "Sektor pertanian pasti meningkat pesat saat pandemi", "Pendapatan daerah stabil sepanjang waktu", "Provinsi tidak memerlukan diversifikasi ekonomi"],
      "Grafik menunjukkan hampir separuh pekerja di Bali (±48%) bekerja di sektor terkait pariwisata, jauh lebih tinggi daripada provinsi lain. Ketergantungan yang tinggi membuat ekonomi daerah sangat rentan terhadap guncangan seperti pandemi COVID-19, letusan gunung api, terorisme, atau krisis ekonomi global. Saat pandemi, ekonomi Bali terkontraksi paling dalam di Indonesia dan banyak pekerja kehilangan pendapatan. Karena itu diversifikasi ekonomi, misalnya pertanian, ekonomi kreatif, dan ekonomi digital, penting untuk ketahanan daerah.\n\nPengecoh: pengangguran dapat melonjak saat kunjungan turun. Pertanian tidak otomatis meningkat. Pendapatan daerah justru tidak stabil. Diversifikasi justru diperlukan.",
      f_kerja),
    Q("Seorang wisatawan menginap di homestay milik warga, makan di warung lokal, dan memakai pemandu desa, dibandingkan wisatawan lain yang menginap di resor milik jaringan internasional. Pernyataan yang paling tepat adalah …",
      ["Pengeluaran wisatawan pertama lebih banyak tinggal di ekonomi lokal", "Kedua wisatawan memberikan manfaat lokal yang persis sama",
       "Resor internasional selalu memberikan manfaat lokal yang lebih besar", "Homestay meningkatkan kebocoran pendapatan ke luar negeri",
       "Warung lokal tidak termasuk dalam ekonomi pariwisata"],
      "Wisatawan pertama membelanjakan uangnya pada usaha milik warga setempat: homestay, warung, dan pemandu desa. Usaha-usaha ini cenderung membeli bahan dan jasa lokal, sehingga sebagian besar pengeluaran tetap beredar di ekonomi lokal dan efek penggandanya besar. Pada resor jaringan internasional, sebagian pengeluaran bocor keluar melalui keuntungan pemilik, biaya waralaba, impor bahan, dan gaji manajer dari luar.\nNamun resor tetap dapat memberikan manfaat lokal, misalnya lapangan kerja dan pajak daerah, terutama bila menerapkan kebijakan pengadaan lokal.\n\nPengecoh: manfaat keduanya tidak sama. Resor tidak selalu memberikan manfaat lokal lebih besar. Homestay justru mengurangi kebocoran. Warung lokal adalah bagian ekonomi pariwisata.",
      None),
    Q("Perhatikan grafik indeks musiman kunjungan dua destinasi berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Destinasi A jauh lebih bergantung musim daripada Destinasi B", "Destinasi B memiliki musim puncak yang lebih tajam daripada A",
       "Kedua destinasi memiliki pola musiman yang persis sama", "Destinasi A selalu ramai sepanjang tahun", "Indeks musiman B selalu di atas 1,5"],
      "Indeks musiman Destinasi A sangat berfluktuasi, dari 0,5 (November–Desember) hingga 1,9 (Juli). Artinya pada musim puncak kunjungan hampir dua kali rata-rata, sedangkan pada musim sepi hanya separuhnya. Destinasi B relatif stabil (0,9–1,1). Destinasi seperti A menghadapi tantangan kepadatan dan harga mahal di musim ramai, serta hotel kosong dan pengangguran musiman di musim sepi. Strateginya antara lain mengembangkan atraksi dan acara pada musim sepi serta menyasar segmen pasar yang berbeda waktu liburnya.\n\nPengecoh: B lebih stabil, bukan lebih tajam. Pola keduanya berbeda. A tidak ramai sepanjang tahun. Indeks B tidak pernah mencapai 1,5.",
      f_musim2),
    Q("Neraca Satelit Pariwisata (Tourism Satellite Account) disusun karena …",
      ["Kontribusi pariwisata tersebar di banyak sektor", "Pariwisata adalah satu sektor tunggal dalam statistik PDB",
       "Pariwisata tidak memiliki dampak terhadap perekonomian", "Pemerintah ingin menghitung jumlah satelit komunikasi", "Neraca ini hanya mencatat jumlah wisatawan mancanegara"],
      "Pariwisata bukan satu sektor tunggal dalam klasifikasi lapangan usaha, melainkan tersebar di banyak sektor seperti akomodasi, makanan dan minuman, transportasi, perdagangan, hiburan, dan jasa lainnya. Neraca Satelit Pariwisata (NESPARNAS di Indonesia) adalah kerangka statistik yang memisahkan bagian konsumsi wisatawan dari berbagai sektor tersebut, sehingga dapat diukur kontribusi pariwisata terhadap PDB, lapangan kerja, dan investasi secara konsisten dan dapat dibandingkan antarnegara.\n\nPengecoh: pariwisata bukan sektor tunggal dalam PDB. Pariwisata jelas berdampak terhadap ekonomi. Neraca satelit tidak berkaitan dengan satelit komunikasi. Neraca ini mencakup wisatawan domestik dan mancanegara serta aspek ekonominya.",
      None),
    Q("Perhatikan grafik tingkat penghunian kamar (TPK) hotel berbintang di Kota W berikut.\n\nPeriode musim sepi dengan TPK di bawah 60% adalah …",
      ["Februari–April dan Oktober–November", "Juni–Agustus dan Desember", "Juli, Agustus, dan September", "Januari–Desember tanpa kecuali", "Desember, Januari, dan Februari"],
      "Garis putus-putus menunjukkan batas 60%. TPK di bawah 60% terjadi pada Februari (48%), Maret (55%), April (58%), Oktober (57%), dan November (52%), sedangkan Mei tepat 60% (pada batas). Jadi periode sepinya adalah Februari–April dan Oktober–November. TPK tinggi terjadi pada Juni–Agustus (72–85%) dan Desember (80%) yang bertepatan dengan libur sekolah dan akhir tahun. Hotel dapat mengisi musim sepi dengan menyasar segmen MICE, menyelenggarakan acara, atau memberikan tarif promosi.\n\nPengecoh: Juni–Agustus dan Desember adalah musim ramai. TPK tidak di bawah 60% sepanjang tahun. Juli, Agustus, dan Desember justru termasuk bulan tertinggi, sedangkan Januari 62%.",
      f_tpk),
    Q("Menurut indeks iritasi (irridex) Doxey, sikap masyarakat lokal terhadap wisatawan cenderung berubah seiring berkembangnya pariwisata. Urutan tahapannya adalah …",
      ["Euforia → apati → iritasi → antagonisme", "Antagonisme → iritasi → apati → euforia", "Apati → euforia → antagonisme → iritasi",
       "Iritasi → euforia → apati → antagonisme", "Euforia → antagonisme → apati → iritasi"],
      "George Doxey (1975) mengemukakan bahwa sikap penduduk lokal terhadap wisatawan berubah bertahap:\n1) Euforia: wisatawan disambut antusias karena membawa pendapatan dan pengalaman baru.\n2) Apati: wisatawan dianggap biasa; hubungan menjadi lebih komersial.\n3) Iritasi: penduduk mulai terganggu oleh kepadatan, kenaikan harga, dan perubahan budaya.\n4) Antagonisme: penduduk menunjukkan penolakan terbuka dan menyalahkan wisatawan atas berbagai masalah.\nModel ini berkaitan dengan siklus hidup destinasi dan isu overtourism, seperti protes warga di Barcelona dan Venesia.\n\nPengecoh: opsi lain membalik atau mengacak urutannya.",
      None),
]

P3 = [
    Q("Perhatikan data penduduk dan wisatawan tiga destinasi berikut.\n\nDestinasi dengan tekanan pariwisata terhadap penduduk (rasio wisatawan per penduduk) tertinggi adalah …",
      ["Destinasi P, sekitar 40 wisatawan per penduduk", "Destinasi Q, sekitar 3 wisatawan per penduduk", "Destinasi R, sekitar 2 wisatawan per penduduk",
       "Destinasi Q, karena jumlah wisatawannya terbanyak kedua", "Ketiga destinasi memiliki rasio yang sama"],
      "Rasio wisatawan per penduduk = jumlah wisatawan per tahun ÷ jumlah penduduk.\n• P: 4.800.000 ÷ 120.000 = 40.\n• Q: 2.400.000 ÷ 800.000 = 3.\n• R: 100.000 ÷ 50.000 = 2.\nDestinasi P memiliki tekanan tertinggi: setiap penduduk \"menampung\" 40 wisatawan per tahun. Rasio tinggi sering menjadi indikator risiko overtourism, misalnya kepadatan, kenaikan harga hunian, tekanan pada air dan sampah, serta berkurangnya kenyamanan warga.\n\nPengecoh: Q memiliki wisatawan banyak tetapi penduduknya juga banyak. R memiliki rasio terkecil. Rasio ketiganya berbeda.",
      f_rasio),
    Q("Tarian sakral yang semula hanya dipentaskan dalam upacara adat kini dipendekkan dan dipertunjukkan setiap malam di hotel untuk wisatawan. Gejala ini disebut …",
      ["Komodifikasi budaya", "Akulturasi alami", "Konservasi budaya", "Revitalisasi lingkungan", "Asimilasi penduduk"],
      "Komodifikasi budaya adalah proses ketika unsur budaya, termasuk ritual dan kesenian sakral, diubah menjadi produk yang dijual kepada wisatawan. Untuk memenuhi selera dan waktu wisatawan, pertunjukan sering dipersingkat, diubah, atau dipentaskan di luar konteks aslinya, sehingga makna sakralnya dapat memudar (staged authenticity). Di sisi lain, pariwisata juga dapat memberikan pendapatan yang membantu pelestarian kesenian. Di Bali, misalnya, dibedakan antara tarian wali (sakral), bebali, dan balih-balihan (hiburan) untuk menjaga kesakralan.\n\nPengecoh: akulturasi adalah percampuran budaya. Konservasi justru menjaga keaslian. Revitalisasi lingkungan tidak terkait. Asimilasi adalah peleburan budaya kelompok.",
      None),
    Q("Perhatikan grafik rata-rata penggunaan air bersih berikut.\n\nImplikasi bagi pulau kecil yang mengembangkan resor dengan lapangan golf adalah …",
      ["Kebutuhan air melonjak dan bersaing dengan warga", "Kebutuhan air penduduk lokal otomatis berkurang",
       "Resor dengan golf menghemat air dibandingkan homestay", "Penggunaan air wisatawan selalu sama dengan penduduk", "Pulau kecil memiliki air tawar tak terbatas"],
      "Grafik menunjukkan wisatawan resor dengan lapangan golf menggunakan sekitar 1.500 liter air per orang per hari, lebih dari 12 kali penggunaan penduduk lokal (±120 liter) dan sekitar 8 kali wisatawan homestay (±180 liter). Di pulau kecil yang sumber air tawarnya terbatas (misalnya lensa air tanah tipis), pembangunan resor boros air dapat menyebabkan penurunan muka air tanah, intrusi air laut, dan konflik penggunaan air dengan penduduk dan petani. Karena itu diperlukan penghematan air, daur ulang air limbah, desalinasi, dan pembatasan pengembangan sesuai daya dukung.\n\nPengecoh: kebutuhan penduduk tidak berkurang otomatis. Resor justru paling boros. Penggunaan air berbeda jauh. Air tawar di pulau kecil sangat terbatas.",
      f_air),
    Q("Wisatawan yang datang ke desa adat menggunakan pakaian, gawai, dan gaya hidup modern, lalu sebagian pemuda desa mulai meniru pola konsumsi tersebut. Dampak sosial ini disebut …",
      ["Efek demonstrasi", "Efek pengganda", "Kebocoran ekonomi", "Daya dukung fisik", "Efek sebar wilayah"],
      "Efek demonstrasi (demonstration effect) adalah dampak sosial ketika masyarakat lokal, terutama generasi muda, meniru perilaku, gaya hidup, dan pola konsumsi wisatawan yang mereka lihat. Dampaknya dapat positif, misalnya terdorong belajar bahasa asing atau berwirausaha, tetapi juga negatif, misalnya konsumsi berlebihan, lunturnya nilai tradisional, dan kecemburuan sosial karena perbedaan kemampuan ekonomi.\n\nPengecoh: efek pengganda dan kebocoran adalah konsep ekonomi. Daya dukung fisik berkaitan dengan jumlah pengunjung maksimum. Efek sebar adalah konsep pembangunan wilayah.",
      None),
    Q("Perhatikan analisis daya dukung kawasan wisata alam W berikut. RCC = PCC × Cf₁ × Cf₂ dan ECC = RCC × MC.\n\nDaya dukung efektif (ECC) kawasan tersebut adalah …",
      ["1.050 kunjungan per hari", "1.750 kunjungan per hari", "3.000 kunjungan per hari", "2.100 kunjungan per hari", "5.000 kunjungan per hari"],
      "1) RCC = 5.000 × 0,7 × 0,5 = 1.750 kunjungan per hari.\n2) ECC = RCC × MC = 1.750 × 0,6 = 1.050 kunjungan per hari.\nDaya dukung efektif adalah jumlah kunjungan maksimum yang dapat dilayani dengan baik mengingat keterbatasan pengelolaan, misalnya jumlah petugas, fasilitas, dan anggaran. Bila kunjungan melebihi ECC, risiko kerusakan lingkungan dan penurunan kualitas pengalaman wisatawan meningkat, sehingga diperlukan pembatasan kuota, sistem reservasi, atau peningkatan kapasitas pengelolaan.\n\nPengecoh: 1.750 adalah RCC. 3.000 hanya mengalikan PCC dengan MC. 2.100 hanya memakai Cf₁ dan MC. 5.000 adalah PCC.",
      f_ecc),
    Q("Labuan Bajo dan Taman Nasional Komodo menghadapi masalah sampah plastik yang meningkat seiring lonjakan wisatawan. Strategi yang paling tepat sesuai prinsip pariwisata berkelanjutan adalah …",
      ["Mengurangi plastik sekali pakai dan memungut biaya kelola", "Membuang sampah ke laut agar terbawa arus",
       "Membakar sampah secara terbuka di pulau-pulau kecil", "Menambah kunjungan tanpa batas untuk menutup biaya", "Melarang warga lokal bekerja di sektor pariwisata"],
      "Pariwisata berkelanjutan menuntut pengelolaan dampak lingkungan sejak dari sumbernya. Strategi yang tepat antara lain: mengurangi plastik sekali pakai (larangan atau pengurangan kantong dan botol plastik), menyediakan stasiun isi ulang air minum, memilah dan mengolah sampah, memungut biaya konservasi atau pengelolaan lingkungan dari wisatawan, melibatkan masyarakat dalam bank sampah, serta membatasi kunjungan sesuai daya dukung.\n\nPengecoh: membuang sampah ke laut merusak ekosistem. Pembakaran terbuka mencemari udara. Kunjungan tanpa batas memperparah masalah. Melarang warga bekerja bertentangan dengan prinsip keberlanjutan sosial.",
      None),
    Q("Perhatikan grafik penyelam dan tutupan karang di Titik Selam S berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Tutupan karang cenderung turun seiring bertambahnya penyelam", "Tutupan karang naik seiring bertambahnya penyelam",
       "Jumlah penyelam tidak pernah berubah sejak 2010", "Tutupan karang pulih sepenuhnya saat penyelam turun pada 2020", "Penyelam selalu meningkatkan kesehatan terumbu karang"],
      "Grafik menunjukkan jumlah penyelam naik dari ±40 ribu (2010) menjadi ±170 ribu (2018), sementara tutupan karang hidup turun dari ±62% menjadi ±42%. Pada 2020 penyelam turun tajam (±60 ribu) karena pandemi dan tutupan karang naik sedikit (±45%), tetapi tidak pulih sepenuhnya, lalu turun lagi ketika penyelam kembali meningkat. Pola ini menunjukkan tekanan wisata selam, misalnya sentuhan, injakan fin, jangkar kapal, dan sedimen, berkaitan dengan penurunan kesehatan terumbu. Faktor lain seperti pemutihan karang akibat kenaikan suhu laut juga mungkin berperan.\n\nPengecoh: tutupan karang turun, bukan naik. Jumlah penyelam berubah. Pemulihan tidak sepenuhnya. Penyelam tidak selalu meningkatkan kesehatan karang.",
      f_karang),
    Q("Pendekatan Limits of Acceptable Change (LAC) dalam pengelolaan kawasan wisata menekankan …",
      ["Batas perubahan yang dapat diterima dan pemantauannya", "Penetapan satu angka jumlah pengunjung yang tidak pernah berubah",
       "Pembiaran kawasan tanpa pemantauan agar berkembang alami", "Penambahan fasilitas sebanyak mungkin tanpa batas", "Penutupan permanen seluruh kawasan wisata"],
      "Limits of Acceptable Change (LAC) tidak berfokus pada satu angka daya dukung, melainkan menanyakan \"berapa besar perubahan kondisi lingkungan dan sosial yang masih dapat diterima?\". Prosesnya meliputi penetapan indikator (misalnya tingkat erosi jalur, kepadatan pengunjung, kualitas air), standar batas yang dapat diterima, pemantauan berkala, dan tindakan pengelolaan bila standar terlampaui, misalnya pembatasan kunjungan, perbaikan jalur, atau zonasi. Pendekatan ini lebih fleksibel dan melibatkan pemangku kepentingan.\n\nPengecoh: LAC justru tidak terpaku pada satu angka tetap. LAC memerlukan pemantauan. Penambahan fasilitas tanpa batas dan penutupan permanen bukan prinsip LAC.",
      None),
    Q("Perhatikan grafik wisatawan dan salinitas air sumur di sebuah pulau kecil berikut.\n\nPenjelasan yang paling mungkin untuk kenaikan salinitas air sumur adalah …",
      ["Pengambilan air tanah berlebih memicu intrusi air laut", "Wisatawan membawa air laut ke dalam sumur warga",
       "Curah hujan meningkat sehingga air sumur menjadi asin", "Salinitas turun setiap kali wisatawan bertambah", "Salinitas tidak berkaitan dengan penggunaan air sama sekali"],
      "Grafik menunjukkan jumlah wisatawan meningkat pesat (±150 ribu pada 2005 menjadi ±1,1 juta pada 2023), diikuti kenaikan salinitas air sumur dari ±0,8‰ menjadi ±4,1‰. Pulau kecil hanya memiliki lensa air tanah tawar tipis yang mengapung di atas air laut. Pengambilan air tanah berlebih untuk hotel, kolam renang, dan layanan wisata menurunkan muka air tanah tawar sehingga air laut menyusup ke akuifer (intrusi air laut). Pada 2020, saat wisatawan turun karena pandemi, salinitas sedikit menurun. Pengelolaan yang diperlukan antara lain penghematan air, pemanenan air hujan, desalinasi, dan pembatasan pengambilan air tanah.\n\nPengecoh: wisatawan tidak membawa air laut ke sumur. Hujan justru mengencerkan. Salinitas naik, bukan turun. Hubungannya terlihat jelas.",
      f_gili),
    Q("Sebuah pantai menerapkan sistem kuota kunjungan harian dan reservasi daring setelah kerusakan lingkungan meningkat. Kebijakan ini paling tepat dikategorikan sebagai …",
      ["Manajemen pengunjung", "Promosi wisata massal", "Komodifikasi budaya", "Efek demonstrasi wisatawan", "Kebocoran ekonomi lokal"],
      "Manajemen pengunjung (visitor management) adalah upaya mengatur jumlah, waktu, lokasi, dan perilaku pengunjung agar dampak terhadap lingkungan dan masyarakat tetap dalam batas yang dapat diterima. Kuota harian dan reservasi daring membatasi kunjungan sesuai daya dukung, menyebarkan kunjungan, dan memudahkan pemantauan. Contohnya pembatasan kunjungan di Pulau Padar dan Pulau Komodo, serta pendakian Gunung Rinjani dengan sistem pemesanan.\n\nPengecoh: promosi wisata massal justru menambah kunjungan. Komodifikasi, efek demonstrasi, dan kebocoran ekonomi adalah dampak, bukan kebijakan pengelolaan.",
      None),
]

P4 = [
    Q("Perhatikan empat paket wisata di Kabupaten W berikut.\n\nPasangan paket dan jenis wisata yang tepat adalah …",
      ["1 – ekowisata; 2 – geowisata", "1 – wisata religi; 3 – geowisata", "2 – agrowisata; 4 – ekowisata", "3 – wisata religi; 1 – agrowisata",
       "4 – geowisata; 2 – wisata religi"],
      "Identifikasi berdasarkan kegiatan utama:\n• Paket 1: mengamati penyu bersama pemandu desa, sebagian tiket untuk konservasi → ekowisata, karena berbasis alam, edukatif, mendukung konservasi, dan memberi manfaat bagi masyarakat lokal.\n• Paket 2: menyusuri singkapan batuan purba dan tebing kaldera → geowisata, yang berfokus pada keragaman geologi (geodiversity).\n• Paket 3: memetik buah dan belajar mengolah kopi di kebun petani → agrowisata.\n• Paket 4: ziarah ke makam wali dan masjid bersejarah → wisata religi.\nPasangan yang tepat adalah 1 – ekowisata dan 2 – geowisata.\n\nPengecoh: opsi lain menukar jenis wisata.",
      f_jenis),
    Q("Sebuah kawasan ditetapkan sebagai UNESCO Global Geopark. Syarat utama penetapan tersebut adalah memiliki …",
      ["Warisan geologi internasional yang dikelola terpadu", "Hotel berbintang lima dalam jumlah sangat besar",
       "Tambang mineral aktif sebagai daya tarik utama", "Kota metropolitan berpenduduk lebih dari sepuluh juta jiwa", "Larangan total bagi masyarakat untuk beraktivitas"],
      "UNESCO Global Geopark adalah kawasan geografis terpadu yang memiliki situs dan bentang alam dengan nilai geologi internasional (geoheritage), dikelola dengan konsep holistik yang memadukan perlindungan, pendidikan, dan pembangunan berkelanjutan. Geopark tidak hanya mencakup keragaman geologi (geodiversity), tetapi juga keragaman hayati (biodiversity) dan budaya (cultural diversity), serta melibatkan masyarakat lokal dalam pengelolaan, misalnya melalui geowisata dan produk lokal. Indonesia memiliki beberapa UNESCO Global Geopark, seperti Batur, Gunung Sewu, Ciletuh–Palabuhanratu, Rinjani–Lombok, Kaldera Toba, dan Belitong.\n\nPengecoh: hotel mewah dan kota besar bukan syarat. Tambang aktif bukan daya tarik utama geopark. Masyarakat justru dilibatkan, bukan dilarang beraktivitas.",
      None),
    Q("Perhatikan peta lokasi beberapa UNESCO Global Geopark di Indonesia berikut.\n\nGeopark Gunung Sewu yang terkenal dengan bentang karst bukit kerucut ditunjukkan oleh label …",
      ["P", "Q", "R", "S", "T"],
      "Lokasi pada peta:\n• P: Gunung Sewu, membentang di pesisir selatan DIY (Gunungkidul), Jawa Tengah (Wonogiri), dan Jawa Timur (Pacitan), dengan ribuan bukit karst kerucut, gua, dan sungai bawah tanah.\n• Q: Batur, Bali, dengan kaldera dan danau vulkanik.\n• R: Ciletuh–Palabuhanratu, Jawa Barat, dengan amfiteater dan batuan tertua di Jawa.\n• S: Kaldera Toba, Sumatera Utara, hasil letusan supervolkano.\n• T: Rinjani–Lombok, NTB.\n\nPengecoh: label lain menunjukkan geopark yang berbeda.",
      f_geopark),
    Q("Prinsip utama pariwisata berbasis masyarakat (community-based tourism, CBT) adalah …",
      ["Masyarakat lokal merencanakan, mengelola, dan menikmati hasil", "Investor luar memiliki dan mengelola seluruh usaha wisata",
       "Masyarakat hanya menjadi penonton kegiatan wisata", "Keuntungan seluruhnya dikirim ke kantor pusat di luar negeri", "Wisatawan dilarang berinteraksi dengan warga"],
      "Pariwisata berbasis masyarakat menempatkan masyarakat lokal sebagai subjek: mereka terlibat sejak perencanaan, pengambilan keputusan, pengelolaan (misalnya melalui kelompok sadar wisata/Pokdarwis atau BUMDes), hingga pembagian manfaat. Prinsip lainnya adalah menjaga budaya dan lingkungan setempat, skala usaha kecil, serta interaksi yang saling menghargai antara wisatawan dan warga. Contohnya desa wisata Nglanggeran (DIY) dan Penglipuran (Bali).\n\nPengecoh: kepemilikan sepenuhnya oleh investor luar, masyarakat sebagai penonton, keuntungan ke luar negeri, dan larangan interaksi bertentangan dengan prinsip CBT.",
      None),
    Q("Perhatikan diagram pembagian pendapatan paket wisata Desa Wisata N berikut.\n\nPersentase pendapatan yang tetap berada di masyarakat dan lembaga desa adalah …",
      ["75%", "35%", "55%", "25%", "45%"],
      "Pendapatan yang tetap di desa = pemilik homestay (35%) + pemandu dan seni (20%) + kas Pokdarwis (10%) + kas desa/BUMDes (10%) = 75%.\nHanya 25% yang keluar kepada agen perjalanan dari luar daerah. Porsi manfaat lokal yang tinggi adalah ciri pariwisata berbasis masyarakat yang berhasil, karena pendapatan beredar di desa dan sebagian masuk kas bersama untuk membiayai fasilitas, konservasi, dan kegiatan sosial.\n\nPengecoh: 35% hanya pemilik homestay. 55% hanya warga perorangan (homestay dan pemandu). 25% adalah porsi yang keluar. 45% menjumlahkan komponen secara keliru.",
      f_desawisata),
    Q("Kriteria Global Sustainable Tourism Council (GSTC) untuk destinasi berkelanjutan mencakup empat pilar. Pilar tersebut adalah …",
      ["Tata kelola, sosial-ekonomi, budaya, lingkungan", "Hanya jumlah wisatawan dan pendapatan devisa", "Promosi, harga tiket, iklan, dan program diskon",
       "Jumlah hotel, bandara, pusat belanja, dan kasino", "Cuaca, musim, suhu udara, dan curah hujan"],
      "Kriteria GSTC untuk destinasi dan industri pariwisata mencakup empat pilar: (A) pengelolaan berkelanjutan (sustainable management), misalnya tata kelola destinasi, perencanaan, dan pemantauan; (B) keberlanjutan sosial-ekonomi, misalnya manfaat bagi masyarakat lokal dan tenaga kerja layak; (C) keberlanjutan budaya, misalnya perlindungan warisan budaya dan hak budaya masyarakat; serta (D) keberlanjutan lingkungan, misalnya konservasi, pengelolaan air, energi, dan sampah. Indonesia mengadopsinya melalui pedoman destinasi pariwisata berkelanjutan.\n\nPengecoh: opsi lain hanya menyebut aspek pemasaran, infrastruktur, atau iklim, bukan pilar keberlanjutan.",
      None),
    Q("Perhatikan klasifikasi desa wisata berikut. Sebuah desa telah dikelola BUMDes, memiliki homestay dan toilet yang memadai, serta mempromosikan paket wisata melalui media sosial, tetapi belum memiliki standar mutu dan pasar mancanegara.\n\nKategori desa wisata tersebut adalah …",
      ["Maju", "Rintisan", "Berkembang", "Mandiri", "Bukan desa wisata"],
      "Klasifikasi desa wisata:\n• Rintisan: potensi wisata ada, tetapi belum ada pengelola dan kunjungan berarti.\n• Berkembang: mulai dikenal, ada kunjungan, tetapi sarana dan pengelolaan masih terbatas.\n• Maju: dikelola kelembagaan seperti Pokdarwis atau BUMDes, fasilitas memadai, dan promosi digital berjalan.\n• Mandiri: inovatif, memiliki standar mutu, menjangkau pasar mancanegara, dan dikelola berkelanjutan.\nDesa pada soal sudah dikelola BUMDes, fasilitasnya memadai, dan promosinya digital, tetapi belum memenuhi ciri mandiri. Jadi kategorinya maju.\n\nPengecoh: rintisan dan berkembang belum memiliki pengelolaan dan fasilitas memadai. Mandiri memerlukan standar mutu dan pasar mancanegara.",
      f_kategori),
    Q("Wisata halal (ramah muslim) yang dikembangkan di Lombok dan Aceh paling tepat diartikan sebagai …",
      ["Layanan makanan halal dan sarana ibadah bagi wisatawan muslim", "Destinasi yang hanya boleh dikunjungi wisatawan muslim",
       "Larangan seluruh atraksi budaya non-Islam di destinasi", "Kewajiban semua wisatawan memakai pakaian adat", "Wisata yang hanya berupa kunjungan ke masjid"],
      "Wisata halal atau ramah muslim (muslim-friendly tourism) adalah layanan tambahan yang memudahkan wisatawan muslim memenuhi kebutuhannya selama berwisata, misalnya makanan dan minuman bersertifikat halal, tempat dan perlengkapan ibadah, informasi waktu salat, serta fasilitas yang menghormati nilai-nilai Islam. Konsep ini tidak membatasi wisatawan nonmuslim dan tidak menghapus atraksi lain. Lombok pernah memperoleh penghargaan destinasi wisata halal dunia, dan pasar wisatawan muslim dari Timur Tengah dan Malaysia menjadi segmen penting.\n\nPengecoh: destinasi tidak hanya untuk muslim. Atraksi budaya lain tidak dilarang. Wisatawan tidak diwajibkan memakai pakaian adat. Wisata halal tidak terbatas pada kunjungan masjid.",
      None),
    Q("Perhatikan diagram tiga pilar pariwisata berkelanjutan berikut.\n\nPilar yang seharusnya mengisi Z adalah …",
      ["Keadilan sosial-budaya bagi masyarakat lokal", "Jumlah wisatawan setinggi mungkin", "Pembangunan hotel sebanyak mungkin",
       "Promosi besar-besaran di media sosial", "Penurunan harga tiket masuk destinasi"],
      "Pariwisata berkelanjutan mengacu pada konsep triple bottom line: keseimbangan antara kelestarian lingkungan (X), manfaat ekonomi (Y), dan keadilan sosial-budaya (Z). Pilar sosial-budaya mencakup penghormatan terhadap budaya dan nilai lokal, distribusi manfaat yang adil, partisipasi masyarakat, serta perlindungan dari dampak negatif seperti komodifikasi dan penggusuran. Pariwisata baru dapat disebut berkelanjutan bila ketiga pilar terpenuhi sekaligus, ditunjukkan oleh irisan ketiga lingkaran.\n\nPengecoh: jumlah wisatawan, jumlah hotel, promosi, dan harga tiket bukan pilar keberlanjutan; bahkan pengejaran jumlah dapat bertentangan dengan keberlanjutan.",
      f_tbl),
    Q("Kunjungan ke Museum Tsunami Aceh dan situs Lumpur Lapindo di Sidoarjo termasuk jenis …",
      ["Wisata kelam (dark tourism)", "Wisata kuliner tradisional", "Wisata bahari dan rekreasi", "Agrowisata dan perkebunan", "Wisata belanja perkotaan"],
      "Wisata kelam (dark tourism) adalah kunjungan ke tempat yang berkaitan dengan bencana, tragedi, kematian, atau penderitaan, misalnya lokasi bencana, monumen peringatan, dan bekas penjara atau medan perang. Museum Tsunami Aceh, situs PLTD Apung, kawasan Lumpur Lapindo, dan Museum Lubang Buaya adalah contoh di Indonesia. Wisata ini memiliki nilai edukasi (pengetahuan kebencanaan dan sejarah), penghormatan kepada korban, dan pembelajaran mitigasi, tetapi pengelolaannya harus etis dan menghormati penyintas.\n\nPengecoh: wisata kuliner, bahari rekreasi, agrowisata, dan wisata belanja tidak berkaitan dengan lokasi tragedi.",
      None),
]

P5 = [
    Q("Perhatikan grafik kunjungan wisatawan mancanegara ke Bali berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Anjlok saat pandemi, pulih ke tingkat 2019 pada 2024", "Kunjungan terus meningkat setiap tahun tanpa penurunan",
       "Kunjungan 2023 sudah melampaui 2019 hampir dua kali lipat", "Pandemi tidak berdampak pada kunjungan ke Bali", "Kunjungan 2021 adalah yang tertinggi"],
      "Grafik menunjukkan kunjungan wisman ke Bali sekitar 6,3 juta pada 2019, anjlok menjadi 1,1 juta pada 2020 dan hampir nol pada 2021 karena penutupan perbatasan selama pandemi COVID-19. Setelah perbatasan dibuka, kunjungan pulih menjadi 2,2 juta (2022), 5,3 juta (2023), dan kembali sekitar 6,3 juta pada 2024. Peristiwa ini menunjukkan kerentanan ekonomi yang sangat bergantung pada pariwisata internasional sekaligus kemampuan pemulihannya.\n\nPengecoh: kunjungan tidak naik terus. Kunjungan 2023 belum melampaui 2019. Pandemi jelas berdampak besar. Kunjungan 2021 justru terendah.",
      f_covid),
    Q("Pembentukan Destination Management Organization (DMO) di sebuah destinasi bertujuan …",
      ["Mengoordinasikan pemangku kepentingan destinasi", "Mengambil alih seluruh usaha wisata milik warga",
       "Menghapus peran pemerintah daerah dalam pariwisata", "Membatasi promosi destinasi hanya kepada satu negara", "Mengganti seluruh atraksi alam dengan atraksi buatan"],
      "Destination Management Organization adalah lembaga atau forum yang mengoordinasikan berbagai pemangku kepentingan pariwisata di suatu destinasi, yaitu pemerintah, pelaku usaha, akademisi, komunitas, dan media (pendekatan pentahelix). Fungsinya antara lain perencanaan dan pengembangan produk, pemasaran destinasi secara terpadu, pengelolaan kualitas layanan dan pengalaman wisatawan, serta pemantauan dampak dan keberlanjutan. Tanpa koordinasi, pengelolaan destinasi sering terfragmentasi dan saling tumpang tindih.\n\nPengecoh: DMO tidak mengambil alih usaha warga atau menghapus peran pemerintah. DMO tidak membatasi promosi pada satu negara. DMO tidak mengganti atraksi alam.",
      None),
    Q("Perhatikan grafik kunjungan wisman ke Bali 2000–2019 berikut.\n\nPenurunan pada titik K dan L paling berkaitan dengan …",
      ["Aksi terorisme bom Bali", "Letusan Gunung Agung", "Pandemi COVID-19", "Krisis keuangan global 2008", "Tsunami Aceh dan Nias"],
      "Titik K (2003) dan L (2006) adalah penurunan setelah peristiwa bom Bali I (Oktober 2002) dan bom Bali II (Oktober 2005). Kedua serangan teror menurunkan rasa aman wisatawan dan memicu peringatan perjalanan (travel advisory) dari banyak negara, sehingga kunjungan turun pada tahun berikutnya. Setelah pemulihan keamanan dan promosi, kunjungan kembali tumbuh pesat hingga mencapai 6,27 juta pada 2019.\nLetusan Gunung Agung terjadi pada 2017 (dampaknya terlihat sebagai perlambatan, bukan penurunan besar pada grafik), pandemi pada 2020–2021, dan krisis keuangan global 2008 tidak menurunkan kunjungan ke Bali secara tajam pada grafik.\n\nPengecoh: tsunami Aceh 2004 tidak menjadi penyebab utama penurunan di Bali.",
      f_krisis),
    Q("Pemerintah memperkenalkan visa khusus bagi pekerja jarak jauh asing (digital nomad) yang tinggal di Bali. Peluang sekaligus tantangan kebijakan ini adalah …",
      ["Belanja lokal naik, tetapi biaya hidup warga ikut naik", "Tidak ada dampak ekonomi karena mereka tidak berbelanja",
       "Mengurangi seluruh kunjungan wisatawan konvensional", "Menghapus kebutuhan infrastruktur internet di Bali", "Membuat warga lokal kehilangan seluruh pekerjaan"],
      "Digital nomad adalah pekerja jarak jauh yang tinggal lebih lama di suatu destinasi sambil bekerja secara daring. Peluangnya: mereka tinggal berbulan-bulan sehingga belanja untuk sewa, makanan, ruang kerja bersama, dan jasa lokal lebih besar daripada wisatawan biasa, serta dapat mendorong ekonomi kreatif dan pertukaran pengetahuan. Tantangannya: kenaikan harga sewa dan biaya hidup yang dapat menyulitkan warga (gejala gentrifikasi wisata), persaingan usaha, isu perpajakan dan izin kerja, serta tekanan terhadap infrastruktur dan lingkungan.\n\nPengecoh: mereka justru berbelanja. Kebijakan ini tidak menghapus wisatawan konvensional. Kebutuhan internet justru meningkat. Warga tidak kehilangan seluruh pekerjaan.",
      None),
    Q("Perhatikan grafik porsi pemesanan akomodasi secara daring berikut.\n\nImplikasi yang paling tepat bagi pengelola homestay di desa wisata adalah …",
      ["Perlu hadir di platform daring dan media sosial", "Promosi daring tidak diperlukan karena porsinya terus turun",
       "Pemesanan daring hanya berlaku untuk hotel berbintang", "Wisatawan tidak lagi membaca ulasan sebelum memesan", "Homestay sebaiknya menolak pemesanan dari luar daerah"],
      "Grafik menunjukkan porsi pemesanan akomodasi secara daring naik dari ±28% (2015) menjadi ±74% (2023). Artinya sebagian besar wisatawan kini mencari, membandingkan, dan memesan akomodasi melalui platform daring dan media sosial, serta sangat dipengaruhi ulasan pengunjung sebelumnya. Pengelola homestay perlu hadir di platform pemesanan, mengelola foto dan ulasan, serta meningkatkan literasi digital agar tidak tertinggal. Namun perlu diwaspadai komisi platform yang dapat menambah kebocoran.\n\nPengecoh: porsi daring naik, bukan turun. Pemesanan daring juga berlaku untuk homestay. Ulasan justru makin penting. Menolak pemesanan dari luar daerah merugikan usaha.",
      f_daring),
    Q("Konsep smart tourism (pariwisata cerdas) memanfaatkan teknologi digital. Contoh penerapan yang paling tepat adalah …",
      ["Pemantauan pengunjung waktu nyata", "Mencetak brosur dalam jumlah sangat besar",
       "Melarang wisatawan membawa telepon genggam", "Menghapus papan informasi di destinasi", "Menutup akses internet di kawasan wisata"],
      "Smart tourism memanfaatkan teknologi informasi seperti sensor, aplikasi, big data, dan internet untuk meningkatkan pengalaman wisatawan, efisiensi pengelolaan, dan keberlanjutan destinasi. Contohnya: pemantauan jumlah pengunjung secara waktu nyata untuk menyebarkan kunjungan dan mencegah kepadatan, tiket dan reservasi daring dengan kuota, aplikasi panduan dan informasi multibahasa, serta analisis data kunjungan untuk perencanaan.\n\nPengecoh: brosur cetak besar-besaran, larangan telepon, penghapusan papan informasi, dan penutupan internet bertentangan dengan konsep pariwisata cerdas.",
      None),
    Q("Perhatikan zonasi sebuah taman nasional berikut.\n\nZona yang paling sesuai untuk pembangunan pusat informasi, jalur interpretasi, dan sarana wisata alam adalah …",
      ["M, zona pemanfaatan", "K, zona inti", "L, zona rimba", "N, zona tradisional", "K dan L secara bersamaan"],
      "Taman nasional di Indonesia dikelola dengan sistem zonasi:\n• Zona inti (K): perlindungan mutlak ekosistem; hanya untuk penelitian terbatas, tidak untuk wisata umum.\n• Zona rimba (L): penyangga zona inti; kegiatan sangat terbatas, misalnya wisata minat khusus tanpa sarana.\n• Zona pemanfaatan (M): lokasi yang diperuntukkan bagi wisata alam, pendidikan, dan sarana pendukung seperti pusat informasi, jalur interpretasi, dan penginapan terbatas.\n• Zona tradisional (N): pemanfaatan sumber daya secara tradisional oleh masyarakat setempat.\nZonasi memungkinkan pariwisata berjalan tanpa mengorbankan perlindungan ekosistem utama.\n\nPengecoh: zona inti dan rimba harus dilindungi dari pembangunan. Zona tradisional diperuntukkan bagi pemanfaatan masyarakat.",
      f_zonasi),
    Q("Kawasan Strategis Pariwisata Nasional (KSPN) ditetapkan pemerintah karena …",
      ["Berpengaruh penting bagi ekonomi, sosial, dan lingkungan", "Kawasan tersebut tidak memiliki potensi wisata",
       "Kawasan tersebut dilarang dikunjungi wisatawan", "Kawasan tersebut hanya dimiliki satu perusahaan swasta", "Kawasan tersebut berada di luar wilayah Indonesia"],
      "Kawasan Strategis Pariwisata Nasional (KSPN) adalah kawasan yang memiliki fungsi utama pariwisata atau potensi pengembangan pariwisata nasional yang berpengaruh penting dalam satu atau lebih aspek, seperti pertumbuhan ekonomi, sosial dan budaya, pemberdayaan sumber daya alam, daya dukung lingkungan hidup, serta pertahanan dan keamanan. Penetapan KSPN menjadi dasar prioritas pembangunan infrastruktur, investasi, dan promosi.\n\nPengecoh: KSPN justru berpotensi besar, terbuka bagi wisatawan, tidak dimiliki satu perusahaan, dan berada di wilayah Indonesia.",
      None),
    Q("Perhatikan komposisi asal wisatawan dua destinasi berikut.\n\nDestinasi yang lebih tangguh menghadapi krisis di satu negara asal wisatawan adalah …",
      ["Destinasi Y, karena pasar asalnya lebih beragam", "Destinasi X, karena 62% wisatawan berasal dari satu negara",
       "Keduanya sama tangguhnya karena total wisatawan sama 100%", "Destinasi X, karena memiliki pasar terbesar yang dominan", "Destinasi Y, karena tidak memiliki pasar asal terbesar"],
      "Destinasi X sangat bergantung pada satu pasar asal (62% wisatawan dari satu negara). Bila negara tersebut mengalami krisis ekonomi, pembatasan perjalanan, atau ketegangan politik, kunjungan ke X dapat anjlok tajam. Destinasi Y memiliki pasar yang lebih beragam: pasar terbesar hanya 18%, dan 53% berasal dari banyak negara lain. Diversifikasi pasar seperti ini menyebarkan risiko sehingga destinasi lebih tangguh (resilient). Strategi diversifikasi juga mencakup pengembangan pasar wisatawan domestik.\n\nPengecoh: ketergantungan pada satu pasar justru melemahkan ketangguhan. Persentase total selalu 100% sehingga tidak menunjukkan ketangguhan. Destinasi Y tetap memiliki pasar terbesar (18%), tetapi porsinya kecil.",
      f_pasar),
    Q("Konsep regenerative tourism (pariwisata regeneratif) melangkah lebih jauh daripada pariwisata berkelanjutan karena …",
      ["Wisata diharapkan memulihkan alam dan komunitas", "Pariwisata hanya bertujuan meningkatkan jumlah kunjungan",
       "Pariwisata tidak lagi memperhatikan dampak lingkungan", "Pariwisata regeneratif melarang semua kunjungan wisatawan", "Pariwisata regeneratif hanya berlaku di kota besar"],
      "Pariwisata berkelanjutan umumnya berfokus pada mengurangi dampak negatif agar sumber daya tidak rusak (do less harm). Pariwisata regeneratif melangkah lebih jauh: kegiatan wisata diharapkan memberikan dampak positif bersih, yaitu memulihkan ekosistem, memperkuat budaya, dan meningkatkan kesejahteraan komunitas (leave it better). Contohnya wisatawan ikut menanam mangrove atau transplantasi karang yang dipantau ilmiah, kontribusi untuk dana konservasi, serta paket wisata yang dirancang dan dikendalikan masyarakat setempat.\n\nPengecoh: regeneratif tidak berfokus pada jumlah kunjungan, tetap memperhatikan lingkungan, tidak melarang kunjungan, dan dapat diterapkan di berbagai destinasi termasuk desa.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
