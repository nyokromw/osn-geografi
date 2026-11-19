from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

AG = ["0–4", "5–9", "10–14", "15–19", "20–24", "25–29", "30–34", "35–39", "40–44", "45–49", "50–54", "55–59", "60–64", "65–69", "70–74", "75+"]

# ============================ figures ============================

def f_pyr_eks(path):
    m = [8.6, 7.8, 7.0, 6.2, 5.3, 4.5, 3.8, 3.1, 2.5, 2.0, 1.6, 1.2, 0.9, 0.6, 0.4, 0.3]
    pyramid(AG, m, [x * 0.97 for x in m], path, title="Piramida penduduk Negara X", xmax=10)


def f_dtm(path):
    x = np.linspace(0, 100, 300)
    cbr = np.where(x < 35, 40, np.where(x < 70, 40 - (x - 35) / 35 * 26, np.where(x < 85, 14, 14 - (x - 85) / 15 * 5)))
    cdr = np.where(x < 15, 38, np.where(x < 50, 38 - (x - 15) / 35 * 28, np.where(x < 85, 10, 10 + (x - 85) / 15 * 2)))
    fig, ax = new(9.5, 4.6)
    ax.plot(x, cbr, color=C["blue"], lw=2.6, label="Angka kelahiran kasar (CBR)")
    ax.plot(x, cdr, color=C["red"], lw=2.6, label="Angka kematian kasar (CDR)")
    for b in [15, 50, 70, 85]:
        ax.axvline(b, color="#A0AEC0", ls="--")
    for i, (a, b) in enumerate([(0, 15), (15, 50), (50, 70), (70, 85), (85, 100)]):
        ax.text((a + b) / 2, 44, ["P", "Q", "R", "S", "T"][i], ha="center", fontsize=15, fontweight="bold")
    ax.set_ylim(0, 48); ax.set_xticks([]); ax.set_xlabel("Waktu →"); ax.set_ylabel("per 1.000 penduduk"); ax.legend(loc="lower left", frameon=False)
    ax.set_title("Model transisi demografi")
    save(fig, path)


def f_pyr_kon(path):
    m = [3.6, 3.8, 4.0, 4.3, 4.6, 5.0, 5.4, 6.0, 6.8, 7.4, 7.0, 6.6, 6.5, 6.8, 5.9, 8.2]
    f = [3.4, 3.6, 3.8, 4.1, 4.4, 4.8, 5.2, 5.8, 6.6, 7.3, 7.0, 6.8, 6.9, 7.5, 7.1, 12.5]
    pyramid(AG, [x * 0.5 for x in m], [x * 0.5 for x in f], path, title="Piramida penduduk Negara Y", xmax=7, legend_loc="lower right")


CITIES = {"A": ((20, 30), 1), "B": ((80, 30), 4), "C": ((30, 75), 2)}


def f_gravitasi(path):
    fig, ax = blank(8, 6, (0, 100), (0, 90))
    for (n1, n2, d) in [("A", "B", "100 km"), ("A", "C", "50 km"), ("B", "C", "200 km")]:
        (x1, y1), (x2, y2) = CITIES[n1][0], CITIES[n2][0]
        ax.plot([x1, x2], [y1, y2], color="#A0AEC0", lw=2); ax.text((x1 + x2) / 2 + 1.5, (y1 + y2) / 2 + 1.5, d, fontsize=11, bbox=dict(fc="white", ec="none"))
    for n, ((x, y), p) in CITIES.items():
        ax.add_patch(Circle((x, y), 4 + p * 1.6, fc=C["orange"], ec="black")); ax.text(x, y, n, ha="center", va="center", fontsize=14, fontweight="bold")
        ax.text(x, y - 7 - p * 1.6, f"{p} juta jiwa", ha="center", fontsize=10)
    ax.set_title("Jumlah penduduk dan jarak antarkota")
    save(fig, path)


def f_padat(path):
    table([["P", "4.000.000", "8.000", "2.000", "800.000"], ["Q", "1.500.000", "20.000", "2.500", "900.000"], ["R", "9.000.000", "3.000", "1.000", "450.000"]],
          ["Provinsi", "Penduduk", "Luas (km²)", "Lahan tani (km²)", "Petani"], path, title="Data kependudukan dan lahan tiga provinsi",
          col_w=[0.14, 0.22, 0.18, 0.26, 0.2])


def f_urban(path):
    lines([1971, 1980, 1990, 2000, 2010, 2020], {"Penduduk perkotaan (%)": [17.3, 22.4, 30.9, 42.0, 49.8, 56.7]}, path,
          title="Persentase penduduk perkotaan Indonesia", xlabel="Tahun", ylabel="%", w=8,
          annotate=lambda ax: [ax.text(x, y + 1.5, f"{y:.1f}".replace(".", ","), ha="center", fontsize=10) for x, y in
                               [(1971, 17.3), (1980, 22.4), (1990, 30.9), (2000, 42.0), (2010, 49.8), (2020, 56.7)]])


# ---- paket 1
ASFR = [30, 120, 140, 100, 60, 20, 5]


def f_asfr(path):
    bars(["15–19", "20–24", "25–29", "30–34", "35–39", "40–44", "45–49"], {"ASFR (per 1.000 perempuan)": ASFR}, path,
         title="Angka fertilitas menurut kelompok umur (ASFR) Kabupaten F", ylabel="kelahiran per 1.000 perempuan", xlabel="Kelompok umur ibu",
         values=True, ylim=(0, 165), colors=[C["purple"]], w=8.5)


def f_imr(path):
    bars(["DKI Jakarta", "DI Yogyakarta", "Jawa Timur", "NTB", "NTT", "Papua"], {"AKB (per 1.000 kelahiran hidup)": [10, 12, 16, 24, 26, 38]}, path,
         title="Angka kematian bayi beberapa provinsi (ilustrasi)", ylabel="per 1.000 kelahiran hidup", values=True, ylim=(0, 45), colors=[C["red"]], rot=12, w=8.5)


def f_preston(path):
    pts = [("A", 1.2, 58), ("B", 2.5, 64), ("C", 4.5, 69), ("D", 8, 72), ("E", 15, 76), ("F", 30, 80), ("G", 50, 82), ("H", 70, 83)]
    fig, ax = new(8, 4.8)
    xs = [p[1] for p in pts]; ys = [p[2] for p in pts]
    ax.scatter(xs, ys, s=60, color=C["blue"]); [ax.annotate(n, (x, y), xytext=(4, 4), textcoords="offset points", fontweight="bold") for n, x, y in pts]
    xx = np.linspace(1, 72, 200); ax.plot(xx, 84 - 28 * np.exp(-xx / 9), "--", color=C["gray"])
    ax.set_xlabel("PDB per kapita (ribu USD)"); ax.set_ylabel("Angka harapan hidup (tahun)"); ax.grid(color="#EDF2F7")
    ax.set_title("PDB per kapita dan angka harapan hidup beberapa negara (ilustrasi)")
    save(fig, path)


def f_epid(path):
    bars(["1980", "1995", "2010", "2023"], {"Penyakit menular, ibu & bayi, gizi": [55, 42, 28, 18], "Penyakit tidak menular": [35, 48, 63, 74],
                                             "Cedera": [10, 10, 9, 8]}, path, title="Penyebab kematian di Indonesia (persen; ilustrasi)",
         ylabel="%", stacked=True, values=True, ylim=(0, 145), colors=[C["orange"], C["purple"], C["gray"]], w=8.5, legend_loc="upper center")


def f_tfr(path):
    lines([1971, 1980, 1991, 2002, 2012, 2017, 2020], {"TFR": [5.6, 4.7, 3.0, 2.6, 2.6, 2.4, 2.2]}, path, title="Angka fertilitas total (TFR) Indonesia",
          xlabel="Tahun", ylabel="anak per perempuan", hline=2.1, w=8.5,
          annotate=lambda ax: ax.text(1972, 2.25, "tingkat penggantian ±2,1", fontsize=9, color=C["gray"]))


# ---- paket 2
def f_berimbang(path):
    table([["Penduduk awal tahun (P₀)", "500.000"], ["Kelahiran (L)", "9.000"], ["Kematian (M)", "3.000"], ["Migrasi masuk (I)", "4.000"],
           ["Migrasi keluar (E)", "6.000"]], ["Komponen selama satu tahun", "Jiwa"], path, title="Data kependudukan Kota K", col_w=[0.6, 0.4])


def f_pyr3(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 4.2))
    shapes = {"X": [9, 8, 7, 6, 5, 4.2, 3.4, 2.7, 2.1, 1.6, 1.2, 0.8, 0.5, 0.3],
              "Y": [6, 6, 6, 5.9, 5.8, 5.7, 5.6, 5.4, 5.1, 4.8, 4.3, 3.6, 2.8, 2],
              "Z": [3.5, 3.8, 4.1, 4.5, 5.0, 5.6, 6.2, 6.8, 7.2, 7.4, 7.0, 6.4, 5.6, 5.0]}
    for a, (n, v) in zip(axs, shapes.items()):
        y = np.arange(len(v)); a.barh(y, [-x for x in v], color=C["blue"]); a.barh(y, v, color=C["red"], alpha=0.85)
        a.set_xlim(-10, 10); a.set_yticks([]); a.set_xticks([]); a.set_title(f"Piramida {n}", fontsize=13, fontweight="bold"); a.axvline(0, color="black", lw=0.6)
    fig.suptitle("Tiga bentuk piramida penduduk (biru = laki-laki, merah = perempuan; umur muda di bawah)", fontweight="bold")
    save(fig, path)


def f_sexratio(path):
    lines(["0–9", "10–19", "20–29", "30–39", "40–49", "50–59", "60+"], {"Rasio jenis kelamin": [105, 104, 78, 82, 95, 98, 88]}, path,
          title="Rasio jenis kelamin menurut umur di Kabupaten M", ylabel="laki-laki per 100 perempuan", xlabel="Kelompok umur", hline=100, w=8.5)


def f_rk(path):
    yr = [1970, 1980, 1990, 2000, 2010, 2020, 2030, 2040, 2050]
    lines(yr, {"Rasio ketergantungan": [86, 79, 68, 55, 51, 47, 46, 49, 53]}, path, title="Rasio ketergantungan Indonesia (proyeksi setelah 2020; ilustrasi)",
          xlabel="Tahun", ylabel="per 100 penduduk usia produktif", hline=50, w=8.5)


def f_dtm_tab(path):
    table([["A", "45", "40"], ["B", "40", "15"], ["C", "20", "8"], ["D", "9", "11"]],
          ["Negara", "CBR (per 1.000)", "CDR (per 1.000)"], path, title="Angka kelahiran dan kematian kasar empat negara", col_w=[0.25, 0.375, 0.375])


# ---- paket 3
def f_densmap(path):
    dense = {"Jakarta Raya": "#7B341E", "Jawa Barat": "#C05621", "Banten": "#C05621", "Jawa Tengah": "#C05621", "Yogyakarta": "#C05621", "Jawa Timur": "#DD6B20",
             "Bali": "#DD6B20", "Nusa Tenggara Barat": "#ED8936", "Lampung": "#F6AD55", "Sumatera Utara": "#F6AD55", "Sulawesi Selatan": "#F6AD55",
             "Kepulauan Riau": "#F6AD55", "Sumatera Barat": "#FBD38D", "Sulawesi Utara": "#FBD38D", "Aceh": "#FBD38D", "Bangka-Belitung": "#FBD38D",
             "Bengkulu": "#FBD38D", "Sumatera Selatan": "#FBD38D", "Jambi": "#FEEBC8", "Riau": "#FEEBC8", "Nusa Tenggara Timur": "#FBD38D",
             "Gorontalo": "#FBD38D", "Sulawesi Tenggara": "#FEEBC8", "Sulawesi Barat": "#FEEBC8", "Sulawesi Tengah": "#FEEBC8", "Kalimantan Selatan": "#FBD38D",
             "Kalimantan Barat": "#FEEBC8", "Kalimantan Timur": "#FFFAF0", "Kalimantan Tengah": "#FFFAF0", "Maluku": "#FEEBC8", "Maluku Utara": "#FEEBC8",
             "Papua": "#FFFAF0", "Papua Barat": "#FFFAF0"}
    fig, ax = indonesia_map(colors=dense, neighbors=True, w=10, h=4.6)
    legend_patches(ax, [("> 1.000", "#C05621"), ("250–1.000", "#ED8936"), ("100–250", "#F6AD55"), ("50–100", "#FBD38D"), ("20–50", "#FEEBC8"), ("< 20", "#FFFAF0")],
                   title="jiwa/km²", loc="lower left", fs=8)
    ax.set_title("Kepadatan penduduk per provinsi (disederhanakan)")
    save(fig, path)


def f_migtab(path):
    table([["K", "4.000.000", "120.000", "40.000"], ["L", "2.000.000", "30.000", "70.000"], ["M", "5.000.000", "60.000", "55.000"]],
          ["Provinsi", "Penduduk", "Migrasi masuk (I)", "Migrasi keluar (E)"], path, title="Data migrasi risen tiga provinsi dalam satu tahun",
          col_w=[0.16, 0.26, 0.29, 0.29])


def f_lee(path):
    fig, ax = blank(10, 4.2, (0, 100), (0, 42))
    for x, n in [(15, "Daerah asal"), (85, "Daerah tujuan")]:
        ax.add_patch(Ellipse((x, 21), 26, 30, fc="#EBF8FF", ec=C["blue"], lw=1.6)); ax.text(x, 39, n, ha="center", fontsize=11, fontweight="bold")
        for i, s in enumerate(["+", "−", "0", "+", "−", "0", "+", "−"]):
            ax.text(x - 8 + (i % 4) * 5.5, 26 - (i // 4) * 8, s, fontsize=14, ha="center", color=C["green"] if s == "+" else (C["red"] if s == "−" else C["gray"]))
    arrow(ax, 29, 21, 71, 21, lw=3)
    for x in [42, 50, 58]:
        ax.add_patch(Rectangle((x - 1.5, 15), 3, 12, fc=C["gray"]))
    ax.text(50, 9, "K", ha="center", fontsize=15, fontweight="bold", color=C["red"])
    ax.text(50, 33, "migrasi", ha="center", fontsize=10)
    ax.set_title("Model migrasi Everett Lee")
    save(fig, path)


def f_decay(path):
    d = [50, 100, 200, 400, 800, 1600]
    lines(d, {"Jumlah migran ke Kota J (ribu jiwa)": [180, 95, 48, 22, 11, 5]}, path, title="Migran ke Kota J menurut jarak daerah asal (ilustrasi)",
          xlabel="Jarak daerah asal ke Kota J (km)", ylabel="ribu jiwa", w=8.5)


def f_komuter(path):
    bars(["Kab./Kota Bekasi", "Kab./Kota Bogor", "Kab./Kota Tangerang", "Kota Depok", "Tangerang Selatan"], {"Komuter ke Jakarta (ribu orang/hari)": [520, 400, 360, 330, 290]}, path,
         title="Komuter harian dari Bodetabek ke Jakarta (ilustrasi)", ylabel="ribu orang per hari", values=True, ylim=(0, 600), colors=[C["teal"]], rot=12, w=9)


# ---- paket 4
def f_urbprov(path):
    bars(["DKI Jakarta", "Banten", "Jawa Barat", "Kalimantan Timur", "Aceh", "NTT"], {"Penduduk perkotaan (%)": [100, 69, 72, 67, 32, 25]}, path,
         title="Persentase penduduk perkotaan beberapa provinsi (ilustrasi)", ylabel="%", values=True, ylim=(0, 115), colors=[C["gray"]], rot=12, w=8.5)


def f_ranksize(path):
    table([["1", "Kota A", "10.500.000"], ["2", "Kota B", "2.900.000"], ["3", "Kota C", "2.400.000"], ["4", "Kota D", "1.700.000"], ["5", "Kota E", "1.500.000"]],
          ["Peringkat", "Kota", "Penduduk"], path, title="Lima kota terbesar Negara N", col_w=[0.25, 0.35, 0.4])


def f_ipm(path):
    bars(["Indeks kesehatan", "Indeks pendidikan", "Indeks pengeluaran"], {"DI Yogyakarta": [0.86, 0.80, 0.78], "Jawa Timur": [0.83, 0.67, 0.75], "Papua": [0.72, 0.48, 0.62]},
         path, title="Indeks komponen IPM tiga provinsi (ilustrasi)", ylabel="indeks (0–1)", values=True, ylim=(0, 1.05), w=9, fmt="{:.2f}")


def f_tpt(path):
    table([["Penduduk usia kerja", "800.000", "500.000"], ["Angkatan kerja", "560.000", "300.000"], ["Bekerja", "520.000", "288.000"]],
          ["Indikator", "Kabupaten X", "Kabupaten Y"], path, title="Data ketenagakerjaan dua kabupaten", col_w=[0.4, 0.3, 0.3])


def f_didik(path):
    bars(["25–34", "35–44", "45–54", "55–64", "65+"], {"≤ SD": [18, 30, 45, 62, 80], "SMP–SMA": [57, 52, 42, 30, 16], "Perguruan tinggi": [25, 18, 13, 8, 4]}, path,
         title="Pendidikan tertinggi menurut kelompok umur (%; ilustrasi)", ylabel="%", stacked=True, values=True, ylim=(0, 145), xlabel="Kelompok umur",
         colors=[C["lgray"], C["lblue"], C["blue"]], w=8.5, legend_loc="upper center")


# ---- paket 5
def f_proyeksi(path):
    bars(["2020", "2030", "2040", "2050"], {"0–14 tahun": [24, 21, 19, 17], "15–64 tahun": [70, 69, 67, 64], "65+ tahun": [6, 10, 14, 19]}, path,
         title="Proyeksi struktur umur penduduk Indonesia (%; ilustrasi)", ylabel="%", stacked=True, values=True, ylim=(0, 145), colors=[C["green"], C["blue"], C["orange"]],
         w=8.5, legend_loc="upper center")


def f_tfr_edu(path):
    pts = [("A", 6.5, 3.4), ("B", 7.4, 3.0), ("C", 8.0, 2.7), ("D", 8.6, 2.4), ("E", 9.2, 2.2), ("F", 10.1, 2.0), ("G", 11.0, 1.8)]
    scatter(pts, path, title="Lama sekolah perempuan dan TFR (ilustrasi)", xlabel="Rata-rata lama sekolah perempuan (tahun)",
            ylabel="TFR (anak per perempuan)", fit=True)


def f_srb(path):
    lines([1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020], {"Rasio jenis kelamin saat lahir": [107, 109, 111, 115, 117, 118, 118, 116, 112]}, path,
          title="Rasio jenis kelamin saat lahir di Negara C (laki-laki per 100 perempuan)", xlabel="Tahun", ylabel="rasio", hline=105, w=8.5)


def f_pyr_tambang(path):
    m = [3.2, 3.0, 2.8, 2.6, 7.5, 9.8, 9.0, 7.2, 5.0, 2.8, 1.5, 0.8, 0.4, 0.2, 0.1, 0.1]
    f = [3.1, 2.9, 2.7, 2.4, 3.2, 3.6, 3.3, 2.6, 1.8, 1.1, 0.7, 0.5, 0.3, 0.2, 0.1, 0.1]
    pyramid(AG, m, f, path, title="Piramida penduduk Kecamatan W", xmax=11)


def f_oadr(path):
    yr = [2000, 2010, 2020, 2030, 2040, 2050]
    lines(yr, {"Jepang": [25, 36, 48, 54, 66, 74], "Korea Selatan": [10, 15, 22, 38, 59, 78], "Indonesia": [7, 8, 10, 14, 19, 26]}, path,
          title="Rasio ketergantungan lansia (65+ per 100 penduduk 15–64; proyeksi, ilustrasi)", xlabel="Tahun", ylabel="rasio", w=9)


# ============================ questions ============================
P0 = [
    Q("Perhatikan piramida penduduk Negara X berikut.\n\nPernyataan yang paling tepat tentang Negara X adalah …",
      ["Piramida ekspansif; angka kelahiran tinggi dan proporsi penduduk muda besar", "Piramida konstruktif; angka kelahiran rendah dan penduduk menua",
       "Piramida stasioner; kelahiran dan kematian sama-sama rendah dan seimbang", "Piramida ekspansif; proporsi lansia jauh lebih besar daripada anak-anak",
       "Piramida konstruktif; jumlah penduduk usia 0–4 tahun paling sedikit"],
      "Piramida Negara X berbentuk segitiga dengan alas lebar: kelompok umur 0–4 tahun paling besar (±8,6% laki-laki) dan proporsi terus mengecil ke kelompok umur tua. Bentuk ini disebut piramida ekspansif, yang menunjukkan angka kelahiran tinggi, angka kematian (terutama bayi dan anak) relatif tinggi, harapan hidup relatif rendah, dan proporsi penduduk muda besar. Negara dengan piramida seperti ini menghadapi tantangan penyediaan sekolah, layanan kesehatan anak, dan lapangan kerja di masa depan. Contohnya negara-negara Afrika sub-Sahara dan Indonesia pada 1970-an.\n\nPengecoh: piramida konstruktif memiliki alas sempit. Piramida stasioner berbentuk hampir tegak lurus. Proporsi lansia pada Negara X justru sangat kecil.",
      f_pyr_eks),
    Q("Pada tahun 2024, sebuah kabupaten berpenduduk 240.000 jiwa (pertengahan tahun) mencatat 4.800 kelahiran hidup. Angka kelahiran kasar (CBR) kabupaten tersebut adalah …",
      ["20 per 1.000 penduduk", "2 per 1.000 penduduk", "50 per 1.000 penduduk", "200 per 1.000 penduduk", "0,02 per 1.000 penduduk"],
      "CBR = (jumlah kelahiran hidup ÷ jumlah penduduk pertengahan tahun) × 1.000\n= (4.800 ÷ 240.000) × 1.000 = 0,02 × 1.000 = 20 per 1.000 penduduk.\nArtinya setiap 1.000 penduduk terdapat 20 kelahiran dalam satu tahun. Nilai ini tergolong sedang (kriteria umum: < 20 rendah, 20–30 sedang, > 30 tinggi).\nCBR disebut \"kasar\" karena penyebutnya seluruh penduduk, termasuk laki-laki, anak-anak, dan lansia yang tidak melahirkan, sehingga dipengaruhi struktur umur.\n\nPengecoh: 2 dan 200 adalah kesalahan faktor sepuluh. 50 per 1.000 membalik pembagian dan salah konstanta. 0,02 belum dikalikan 1.000.",
      None),
    Q("Perhatikan model transisi demografi berikut.\n\nTahap yang ditandai pertumbuhan penduduk paling cepat karena angka kematian turun tajam sementara angka kelahiran masih tinggi adalah …",
      ["Q", "P", "R", "S", "T"],
      "Tahap-tahap model transisi demografi:\n• P: kelahiran dan kematian sama-sama tinggi; pertumbuhan sangat lambat (masyarakat praindustri).\n• Q: kematian turun tajam berkat perbaikan pangan, sanitasi, dan kesehatan, sementara kelahiran masih tinggi; jarak antara CBR dan CDR paling lebar sehingga pertumbuhan penduduk paling cepat (ledakan penduduk).\n• R: kelahiran mulai turun karena urbanisasi, pendidikan perempuan, dan keluarga berencana; pertumbuhan melambat.\n• S: kelahiran dan kematian sama-sama rendah; pertumbuhan sangat lambat atau stabil.\n• T: kelahiran lebih rendah daripada kematian sehingga penduduk dapat menurun, misalnya Jepang.\n\nPengecoh: tahap lain memiliki selisih CBR dan CDR yang lebih kecil.",
      f_dtm),
    Q("Suatu negara memiliki penduduk usia 0–14 tahun 70 juta jiwa, usia 15–64 tahun 190 juta jiwa, dan usia 65 tahun ke atas 15 juta jiwa. Rasio ketergantungan dan maknanya adalah …",
      ["Sekitar 44,7; negara berada pada masa bonus demografi", "Sekitar 36,8; negara mengalami penuaan penduduk ekstrem",
       "Sekitar 223,5; beban penduduk produktif sangat berat", "Sekitar 44,7; negara belum memasuki bonus demografi",
       "Sekitar 7,9; hampir tidak ada penduduk usia nonproduktif"],
      "Rasio ketergantungan (RK) = (penduduk 0–14 + penduduk 65+) ÷ penduduk 15–64 × 100\n= (70 + 15) ÷ 190 × 100 = 85 ÷ 190 × 100 ≈ 44,7.\nArtinya setiap 100 penduduk usia produktif menanggung sekitar 45 penduduk usia nonproduktif. RK di bawah 50 menandakan negara berada pada masa bonus demografi, yaitu ketika proporsi penduduk usia produktif sangat besar sehingga berpotensi mempercepat pertumbuhan ekonomi bila tersedia lapangan kerja dan SDM berkualitas.\n\nPengecoh: 36,8 hanya menghitung anak (70 ÷ 190). 223,5 membalik pembagian. 7,9 hanya menghitung lansia. RK 44,7 justru berarti negara sudah berada pada bonus demografi.",
      None),
    Q("Perhatikan piramida penduduk Negara Y berikut.\n\nTantangan kependudukan utama yang dihadapi Negara Y adalah …",
      ["Penuaan penduduk dan menyusutnya angkatan kerja muda", "Ledakan kelahiran sehingga sekolah dasar kekurangan ruang kelas",
       "Tingginya angka kematian bayi akibat layanan kesehatan buruk", "Kelebihan penduduk usia muda yang belum memperoleh pekerjaan",
       "Rasio jenis kelamin sangat timpang akibat migrasi laki-laki"],
      "Piramida Negara Y memiliki alas sempit (kelompok 0–14 tahun kecil) dan bagian atas yang lebar, termasuk kelompok 75+ yang besar terutama perempuan. Bentuk ini disebut piramida konstruktif (kontraktif), khas negara dengan angka kelahiran sangat rendah dan harapan hidup tinggi, seperti Jepang, Italia, atau Korea Selatan.\nTantangannya: penuaan penduduk, jumlah angkatan kerja yang menyusut, beban pensiun dan layanan kesehatan lansia yang meningkat, serta kemungkinan penurunan jumlah penduduk. Kebijakan yang ditempuh antara lain insentif kelahiran, perpanjangan usia pensiun, otomatisasi, dan penerimaan pekerja migran.\n\nPengecoh: ledakan kelahiran, kematian bayi tinggi, dan kelebihan penduduk muda adalah ciri piramida ekspansif. Rasio jenis kelamin pada piramida ini tidak menunjukkan ketimpangan akibat migrasi laki-laki.",
      f_pyr_kon),
    Q("Penduduk sebuah kota tahun 2020 berjumlah 2.000.000 jiwa dengan laju pertumbuhan geometrik 2% per tahun. Dengan Pt = P₀(1 + r)ᵗ, jumlah penduduk kota tersebut pada tahun 2030 adalah sekitar …",
      ["2.438.000 jiwa", "2.400.000 jiwa", "2.040.000 jiwa", "4.000.000 jiwa", "2.200.000 jiwa"],
      "Pt = 2.000.000 × (1 + 0,02)¹⁰ = 2.000.000 × 1,02¹⁰.\n1,02¹⁰ ≈ 1,219, sehingga Pt ≈ 2.000.000 × 1,219 ≈ 2.438.000 jiwa.\nModel geometrik mengasumsikan pertumbuhan terjadi bertahap setiap tahun dan bunga majemuk, sehingga hasilnya lebih besar daripada pertumbuhan linear.\n\nPengecoh: 2.400.000 jiwa memakai pertumbuhan linear (2% × 10 = 20%). 2.040.000 jiwa hanya menghitung satu tahun. 4.000.000 jiwa adalah waktu penggandaan yang memerlukan sekitar 35 tahun (70 ÷ 2). 2.200.000 jiwa memakai 1% per tahun.",
      None),
    Q("Perhatikan jumlah penduduk dan jarak antarkota berikut. Dengan model gravitasi I = k × P₁ × P₂ ÷ d², pasangan kota yang diperkirakan memiliki interaksi (arus perjalanan) terbesar adalah …",
      ["A dan C", "A dan B", "B dan C", "Ketiganya sama besar", "B dan C karena penduduknya paling banyak"],
      "Hitung nilai relatif P₁ × P₂ ÷ d² (P dalam juta jiwa, d dalam km):\n• A–B: (1 × 4) ÷ 100² = 4 ÷ 10.000 = 0,0004.\n• A–C: (1 × 2) ÷ 50² = 2 ÷ 2.500 = 0,0008.\n• B–C: (4 × 2) ÷ 200² = 8 ÷ 40.000 = 0,0002.\nInteraksi terbesar terjadi antara A dan C, walaupun jumlah penduduk keduanya tidak terbesar, karena jaraknya paling dekat dan jarak dalam model dikuadratkan.\n\nPengecoh: pasangan B–C memiliki perkalian penduduk terbesar (8), tetapi jaraknya paling jauh sehingga interaksinya paling kecil. A–B berada di urutan kedua. Interaksi ketiganya tidak sama. Model ini menunjukkan peran jarak (friction of distance) dalam interaksi keruangan.",
      f_gravitasi),
    Q("Menurut teori Everett Lee, keputusan seseorang untuk bermigrasi dipengaruhi empat kelompok faktor. Yang dimaksud dengan rintangan antara (intervening obstacles) adalah …",
      ["Hambatan di antara asal dan tujuan, seperti jarak dan biaya", "Faktor positif di daerah tujuan, seperti upah tinggi dan fasilitas lengkap",
       "Faktor negatif di daerah asal, seperti kemiskinan dan bencana", "Faktor pribadi, seperti usia, pendidikan, dan kepribadian calon migran",
       "Faktor netral yang tidak memengaruhi siapa pun"],
      "Everett Lee (1966) menjelaskan bahwa migrasi dipengaruhi oleh: (1) faktor di daerah asal (positif, negatif, dan netral); (2) faktor di daerah tujuan; (3) rintangan antara, yaitu hambatan yang terletak di antara daerah asal dan tujuan, seperti jarak, biaya transportasi, topografi, perbedaan bahasa, dan peraturan imigrasi atau perbatasan; serta (4) faktor pribadi, seperti usia, pendidikan, kesehatan, dan persepsi individu.\nMigrasi terjadi bila daya tarik dan dorongan cukup kuat untuk mengatasi rintangan antara. Perbaikan transportasi dan informasi memperkecil rintangan sehingga mobilitas meningkat.\n\nPengecoh: opsi lain menggambarkan faktor daerah tujuan, daerah asal, dan faktor pribadi, bukan rintangan antara.",
      None),
    Q("Perhatikan data kependudukan dan lahan tiga provinsi berikut.\n\nProvinsi dengan kepadatan penduduk agraris tertinggi adalah …",
      ["R, sekitar 450 petani per km² lahan pertanian", "P, sekitar 500 jiwa per km² luas wilayah", "Q, sekitar 360 petani per km² lahan pertanian",
       "R, sekitar 3.000 jiwa per km² luas wilayah", "P, sekitar 2.000 jiwa per km² lahan pertanian"],
      "Kepadatan agraris = jumlah petani ÷ luas lahan pertanian.\n• P: 800.000 ÷ 2.000 = 400 petani/km².\n• Q: 900.000 ÷ 2.500 = 360 petani/km².\n• R: 450.000 ÷ 1.000 = 450 petani/km².\nKepadatan agraris tertinggi ada di R, artinya tekanan petani terhadap lahan pertanian paling besar dan rata-rata luas garapan per petani paling sempit.\nBandingkan dengan kepadatan aritmatik (penduduk ÷ luas wilayah): P = 500, Q = 75, R = 3.000 jiwa/km²; dan kepadatan fisiologis (penduduk ÷ lahan pertanian): P = 2.000, Q = 600, R = 9.000 jiwa/km².\n\nPengecoh: opsi lain memakai jenis kepadatan yang berbeda (aritmatik atau fisiologis) atau angka yang salah.",
      f_padat),
    Q("Perhatikan grafik persentase penduduk perkotaan Indonesia berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Sejak 2010-an lebih dari separuh penduduk tinggal di kota", "Persentase penduduk perkotaan menurun sejak 1990",
       "Penduduk perkotaan bertambah tepat 10 poin persen setiap dekade", "Pada 1971 sudah lebih dari separuh penduduk tinggal di kota",
       "Peningkatan tercepat terjadi pada dekade 2010–2020"],
      "Grafik menunjukkan persentase penduduk perkotaan naik dari 17,3% (1971) menjadi 49,8% (2010) dan 56,7% (2020). Artinya sejak sekitar awal 2010-an, lebih dari separuh penduduk Indonesia tinggal di wilayah perkotaan.\nKenaikan per dekade: 1971–1980 ±5,1 poin; 1980–1990 ±8,5 poin; 1990–2000 ±11,1 poin (tercepat); 2000–2010 ±7,8 poin; 2010–2020 ±6,9 poin. Kenaikan disebabkan oleh migrasi desa–kota, pertumbuhan alami penduduk kota, dan reklasifikasi desa menjadi kawasan perkotaan.\n\nPengecoh: persentase tidak pernah menurun. Kenaikan per dekade tidak tetap. Pada 1971 baru 17,3%. Kenaikan tercepat terjadi pada 1990–2000, bukan 2010–2020.",
      f_urban),
]

P1 = [
    Q("Perhatikan grafik ASFR Kabupaten F berikut. Dengan TFR = 5 × ΣASFR ÷ 1.000, angka fertilitas total kabupaten tersebut adalah sekitar …",
      ["2,4 anak per perempuan", "0,5 anak per perempuan", "4,8 anak per perempuan", "23,8 anak per perempuan", "1,4 anak per perempuan"],
      "Jumlahkan ASFR seluruh kelompok umur: 30 + 120 + 140 + 100 + 60 + 20 + 5 = 475 kelahiran per 1.000 perempuan.\nKarena setiap kelompok umur mencakup 5 tahun, TFR = 5 × 475 ÷ 1.000 = 2,375 ≈ 2,4 anak per perempuan.\nArtinya rata-rata seorang perempuan akan melahirkan sekitar 2,4 anak selama masa reproduksinya bila pola fertilitas tetap. Nilai ini sedikit di atas tingkat penggantian (±2,1).\n\nPengecoh: 0,5 lupa mengalikan 5. 4,8 mengalikan dengan 10. 23,8 tidak membagi dengan 1.000 secara tepat. 1,4 berasal dari salah menjumlah. Grafik juga menunjukkan puncak fertilitas pada umur 25–29 tahun.",
      f_asfr),
    Q("Sebuah kota memiliki 6.000 kelahiran hidup dalam satu tahun dan 120.000 perempuan usia 15–49 tahun. Angka fertilitas umum (GFR) kota tersebut adalah …",
      ["50 per 1.000 perempuan usia subur", "5 per 1.000 perempuan usia subur", "20 per 1.000 perempuan usia subur", "500 per 1.000 perempuan usia subur",
       "0,05 per 1.000 perempuan usia subur"],
      "GFR = (jumlah kelahiran hidup ÷ jumlah perempuan usia 15–49 tahun) × 1.000 = (6.000 ÷ 120.000) × 1.000 = 0,05 × 1.000 = 50.\nArtinya setiap 1.000 perempuan usia subur melahirkan 50 bayi dalam setahun. GFR lebih baik daripada CBR karena penyebutnya hanya perempuan yang berisiko melahirkan, tetapi belum memperhitungkan perbedaan fertilitas antar kelompok umur seperti ASFR dan TFR.\n\nPengecoh: 5 dan 500 adalah kesalahan faktor sepuluh. 20 membalik perhitungan secara keliru. 0,05 belum dikalikan 1.000.",
      None),
    Q("Perhatikan grafik angka kematian bayi (AKB) beberapa provinsi berikut.\n\nPenjelasan yang paling tepat untuk tingginya AKB di Papua dibandingkan DKI Jakarta adalah …",
      ["Akses layanan kesehatan, gizi, dan sanitasi terbatas", "Jumlah penduduk Papua jauh lebih banyak daripada Jakarta",
       "Iklim Papua yang dingin membuat bayi tidak dapat bertahan hidup", "AKB dihitung dari seluruh penduduk sehingga provinsi luas selalu tinggi",
       "Bayi di Jakarta tidak pernah sakit karena tinggal di kota besar"],
      "AKB Papua (±38 per 1.000 kelahiran hidup) hampir empat kali AKB DKI Jakarta (±10). AKB adalah indikator sensitif terhadap kondisi sosial-ekonomi dan layanan kesehatan. Di wilayah terpencil Papua, banyak kampung yang hanya dapat dijangkau dengan pesawat atau berjalan kaki berhari-hari, sehingga akses ke puskesmas, bidan, imunisasi, dan rujukan persalinan sangat terbatas. Ditambah gizi ibu dan bayi yang kurang serta sanitasi dan air bersih yang buruk, risiko kematian bayi meningkat.\n\nPengecoh: jumlah penduduk Papua lebih kecil dan tidak menentukan angka per 1.000 kelahiran. Sebagian besar wilayah Papua beriklim tropis, bukan dingin. AKB dihitung per kelahiran hidup, bukan per penduduk. Bayi di kota tetap dapat sakit.",
      f_imr),
    Q("Di sebuah kabupaten tercatat 15.000 kelahiran hidup dan 360 kematian bayi berumur di bawah satu tahun dalam setahun. Angka kematian bayi (AKB) kabupaten tersebut adalah …",
      ["24 per 1.000 kelahiran hidup", "2,4 per 1.000 kelahiran hidup", "240 per 1.000 kelahiran hidup", "36 per 1.000 kelahiran hidup",
       "41,7 per 1.000 kelahiran hidup"],
      "AKB (IMR) = (kematian bayi < 1 tahun ÷ jumlah kelahiran hidup) × 1.000 = (360 ÷ 15.000) × 1.000 = 0,024 × 1.000 = 24 per 1.000 kelahiran hidup.\nPenyebutnya adalah kelahiran hidup pada tahun yang sama, bukan jumlah penduduk. AKB sering dipakai sebagai indikator kualitas layanan kesehatan dan kesejahteraan suatu wilayah.\n\nPengecoh: 2,4 dan 240 adalah kesalahan faktor sepuluh. 36 salah membaca jumlah kematian. 41,7 membalik pembagian (15.000 ÷ 360).",
      None),
    Q("Perhatikan diagram pencar PDB per kapita dan angka harapan hidup berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Harapan hidup naik pesat pada pendapatan rendah, lalu melambat",
       "Harapan hidup naik secara linear dan tidak terbatas seiring kenaikan pendapatan",
       "Harapan hidup menurun ketika pendapatan per kapita meningkat",
       "Pendapatan tidak berhubungan dengan harapan hidup sama sekali",
       "Negara dengan pendapatan tertinggi pasti memiliki harapan hidup di atas 100 tahun"],
      "Grafik menunjukkan pola cekung (kurva Preston): pada pendapatan rendah (1–8 ribu USD), kenaikan kecil pendapatan diikuti kenaikan besar harapan hidup (dari ±58 menjadi ±72 tahun), karena tambahan pendapatan dipakai untuk kebutuhan dasar seperti gizi, air bersih, sanitasi, dan imunisasi. Pada pendapatan tinggi (30–70 ribu USD), kenaikan harapan hidup sangat kecil (±80–83 tahun) karena mendekati batas biologis dan dipengaruhi faktor lain seperti gaya hidup.\nImplikasinya, investasi kesehatan dasar di negara berpendapatan rendah memberikan dampak terbesar.\n\nPengecoh: hubungan tidak linear dan tidak tanpa batas. Harapan hidup tidak menurun. Hubungan keduanya jelas. Tidak ada negara dengan harapan hidup rata-rata di atas 100 tahun.",
      f_preston),
    Q("Di sebuah provinsi tercatat 18 kematian ibu akibat kehamilan dan persalinan dari 12.000 kelahiran hidup dalam setahun. Angka kematian ibu (AKI) provinsi tersebut adalah …",
      ["150 per 100.000 kelahiran hidup", "1,5 per 1.000 kelahiran hidup", "15 per 100.000 kelahiran hidup", "1.500 per 100.000 kelahiran hidup",
       "667 per 100.000 kelahiran hidup"],
      "AKI (MMR) = (jumlah kematian ibu ÷ jumlah kelahiran hidup) × 100.000 = (18 ÷ 12.000) × 100.000 = 0,0015 × 100.000 = 150 per 100.000 kelahiran hidup.\nKonstanta 100.000 dipakai karena kematian ibu relatif jarang. Penurunan AKI menjadi salah satu target SDGs (di bawah 70 per 100.000 kelahiran hidup pada 2030) dan sangat ditentukan oleh persalinan yang ditolong tenaga kesehatan di fasilitas kesehatan.\n\nPengecoh: 1,5 per 1.000 secara matematis setara, tetapi bukan satuan baku AKI. 15 dan 1.500 adalah kesalahan faktor sepuluh. 667 membalik pembagian.",
      None),
    Q("Perhatikan grafik penyebab kematian di Indonesia berikut.\n\nGejala yang ditunjukkan grafik disebut …",
      ["Transisi epidemiologi dari penyakit menular ke tidak menular", "Transisi demografi tahap pertama dengan kematian sangat tinggi",
       "Ledakan penyakit menular akibat urbanisasi yang sangat cepat", "Penurunan penyakit tidak menular karena gaya hidup makin sehat",
       "Stagnasi kesehatan karena porsi penyebab kematian tidak berubah"],
      "Grafik menunjukkan porsi kematian akibat penyakit menular, gangguan ibu dan bayi, serta gizi turun dari ±55% (1980) menjadi ±18% (2023), sedangkan porsi penyakit tidak menular (jantung, stroke, diabetes, kanker) naik dari ±35% menjadi ±74%. Pergeseran pola penyakit ini disebut transisi epidemiologi. Penyebabnya: keberhasilan imunisasi, sanitasi, dan pengobatan penyakit infeksi; meningkatnya harapan hidup sehingga lebih banyak orang mencapai usia rawan penyakit kronis; serta perubahan gaya hidup (pola makan, rokok, kurang aktivitas fisik).\n\nPengecoh: kematian sangat tinggi adalah tahap awal transisi demografi, bukan pola grafik. Penyakit menular justru menurun. Penyakit tidak menular meningkat. Porsi penyebab kematian jelas berubah.",
      f_epid),
    Q("Angka kematian kasar (CDR) Jepang sekitar 12 per 1.000, lebih tinggi daripada Indonesia yang sekitar 7 per 1.000, walaupun layanan kesehatan Jepang jauh lebih maju. Penjelasan yang paling tepat adalah …",
      ["Proporsi lansia di Jepang jauh lebih besar sehingga kematian lebih banyak",
       "Layanan kesehatan Jepang sebenarnya lebih buruk daripada Indonesia",
       "Angka kematian bayi di Jepang jauh lebih tinggi daripada Indonesia",
       "Jepang sering mengalami wabah penyakit menular setiap tahun",
       "CDR dihitung dengan rumus yang berbeda di setiap negara"],
      "CDR disebut \"kasar\" karena tidak memperhitungkan struktur umur penduduk. Jepang memiliki penduduk sangat menua (sekitar 29% berusia 65 tahun ke atas), dan secara alami risiko kematian meningkat pada usia lanjut. Karena itu, walaupun harapan hidup Jepang termasuk tertinggi di dunia (±84 tahun), jumlah kematian per 1.000 penduduk tetap tinggi. Indonesia memiliki struktur penduduk yang lebih muda sehingga CDR-nya lebih rendah.\nUntuk membandingkan tingkat kematian antarnegara secara adil, digunakan angka kematian menurut umur (ASDR), angka kematian yang distandarkan umur, atau angka harapan hidup.\n\nPengecoh: layanan kesehatan Jepang lebih baik. AKB Jepang sangat rendah (±2 per 1.000). Jepang tidak mengalami wabah tahunan besar. Rumus CDR sama di setiap negara.",
      None),
    Q("Perhatikan grafik TFR Indonesia berikut.\n\nPernyataan yang paling tepat adalah …",
      ["TFR turun tajam sejak 1971 dan pada 2020 mendekati tingkat penggantian", "TFR naik terus sehingga Indonesia mengalami ledakan kelahiran baru",
       "TFR sudah jauh di bawah tingkat penggantian seperti Jepang", "TFR tidak berubah sejak 1971 meskipun program KB dijalankan",
       "TFR pada 2020 berarti setiap keluarga pasti memiliki tepat dua anak"],
      "Grafik menunjukkan TFR Indonesia turun dari 5,6 anak per perempuan (1971) menjadi 2,2 (2020), sedikit di atas tingkat penggantian (±2,1). Penurunan tajam terjadi pada 1970–1990-an berkat program Keluarga Berencana, peningkatan pendidikan perempuan, urbanisasi, dan turunnya kematian bayi. Antara 2002 dan 2012, TFR sempat stagnan di 2,6.\nTingkat penggantian adalah TFR yang membuat setiap generasi menggantikan dirinya sendiri dalam jangka panjang (sekitar 2,1, lebih dari 2 karena memperhitungkan kematian sebelum usia reproduksi dan rasio jenis kelamin saat lahir).\n\nPengecoh: TFR tidak naik. Indonesia belum jauh di bawah tingkat penggantian. TFR jelas berubah. TFR adalah angka rata-rata, bukan jumlah anak pasti setiap keluarga.",
      f_tfr),
    Q("Faktor yang paling konsisten berhubungan dengan penurunan fertilitas di banyak negara berkembang adalah …",
      ["Meningkatnya pendidikan dan partisipasi kerja perempuan", "Menurunnya usia kawin pertama perempuan di perdesaan",
       "Meningkatnya angka kematian bayi sehingga keluarga menambah anak", "Bertambahnya nilai ekonomi anak sebagai tenaga kerja di sawah",
       "Menurunnya akses terhadap alat kontrasepsi modern"],
      "Pendidikan perempuan memengaruhi fertilitas melalui banyak jalur: perempuan berpendidikan cenderung menunda usia kawin pertama, memiliki pengetahuan dan akses lebih baik terhadap kontrasepsi, lebih banyak bekerja di sektor formal sehingga biaya peluang memiliki banyak anak meningkat, serta lebih memperhatikan kualitas pendidikan dan kesehatan anak. Akibatnya jumlah anak yang diinginkan menurun.\n\nPengecoh: usia kawin yang lebih muda justru memperpanjang masa reproduksi dan meningkatkan fertilitas. Kematian bayi yang tinggi mendorong keluarga memiliki lebih banyak anak (efek penggantian). Nilai ekonomi anak yang tinggi juga mendorong fertilitas. Turunnya akses kontrasepsi meningkatkan fertilitas.",
      None),
]

P2 = [
    Q("Perhatikan data kependudukan Kota K selama satu tahun berikut. Dengan persamaan berimbang Pt = P₀ + (L − M) + (I − E), jumlah penduduk Kota K pada akhir tahun adalah …",
      ["504.000 jiwa", "508.000 jiwa", "506.000 jiwa", "522.000 jiwa", "498.000 jiwa"],
      "Pertumbuhan alami = L − M = 9.000 − 3.000 = 6.000 jiwa.\nMigrasi neto = I − E = 4.000 − 6.000 = −2.000 jiwa (lebih banyak yang keluar).\nPt = 500.000 + 6.000 + (−2.000) = 504.000 jiwa.\nKota K bertambah 4.000 jiwa karena pertumbuhan alaminya positif walaupun mengalami migrasi neto negatif.\n\nPengecoh: 508.000 jiwa membalik tanda migrasi neto (+2.000). 506.000 jiwa mengabaikan migrasi. 522.000 jiwa menjumlahkan semua komponen. 498.000 jiwa salah menjumlahkan tanda pertumbuhan alami.",
      f_berimbang),
    Q("Laju pertumbuhan penduduk sebuah negara adalah 1,4% per tahun. Dengan pendekatan aturan 70, waktu yang diperlukan agar penduduk negara itu menjadi dua kali lipat adalah sekitar …",
      ["50 tahun", "70 tahun", "98 tahun", "14 tahun", "140 tahun"],
      "Aturan 70: waktu penggandaan (Td) ≈ 70 ÷ r(%) = 70 ÷ 1,4 = 50 tahun.\nPendekatan ini berasal dari rumus eksak Td = ln 2 ÷ ln(1 + r) ≈ 0,693 ÷ r, sehingga dalam persen menjadi ±70 ÷ r. Dengan laju 1,4% per tahun, penduduk negara itu akan berlipat dua dalam sekitar setengah abad bila laju pertumbuhan tetap.\n\nPengecoh: 70 tahun belum dibagi laju pertumbuhan. 98 tahun mengalikan 70 dengan 1,4. 14 tahun dan 140 tahun berasal dari kesalahan desimal.",
      None),
    Q("Perhatikan tiga bentuk piramida penduduk berikut.\n\nPasangan piramida dan contoh negara yang paling tepat adalah …",
      ["X – Niger; Z – Jepang", "X – Jepang; Y – Niger", "Y – Niger; Z – Indonesia tahun 1970", "Z – Niger; X – Swedia", "Y – Jepang; X – Swedia"],
      "• Piramida X (alas sangat lebar dan meruncing ke atas) adalah piramida ekspansif: kelahiran sangat tinggi dan penduduk muda dominan, misalnya Niger yang memiliki TFR sekitar 6–7.\n• Piramida Y (hampir tegak dengan sisi relatif lurus) adalah piramida stasioner: kelahiran dan kematian sama-sama rendah dan stabil, misalnya Swedia atau beberapa negara Eropa Barat.\n• Piramida Z (alas menyempit dan bagian tengah-atas lebih lebar) adalah piramida konstruktif: kelahiran sangat rendah dan penduduk menua, misalnya Jepang.\nPasangan yang tepat adalah X – Niger dan Z – Jepang.\n\nPengecoh: opsi lain menukar bentuk piramida dengan negara. Indonesia tahun 1970 justru berbentuk ekspansif.",
      f_pyr3),
    Q("Penduduk sebuah kabupaten bertambah dari 1.000.000 jiwa menjadi 1.210.000 jiwa dalam 10 tahun. Dengan model geometrik r = (Pt ÷ P₀)^(1/t) − 1, laju pertumbuhan rata-rata per tahun adalah sekitar …",
      ["1,9% per tahun", "2,1% per tahun", "21% per tahun", "1,1% per tahun", "0,21% per tahun"],
      "Pt ÷ P₀ = 1.210.000 ÷ 1.000.000 = 1,21.\nr = 1,21^(1/10) − 1. Karena 1,019¹⁰ ≈ 1,207 dan 1,0192¹⁰ ≈ 1,21, maka r ≈ 0,0192 ≈ 1,9% per tahun.\nModel geometrik menghasilkan laju lebih kecil daripada perhitungan linear karena pertumbuhan setiap tahun ikut bertumbuh (majemuk).\n\nPengecoh: 2,1% adalah laju linear (21% ÷ 10). 21% adalah pertumbuhan total 10 tahun. 1,1% dan 0,21% berasal dari kesalahan perhitungan atau desimal.",
      None),
    Q("Perhatikan grafik rasio jenis kelamin menurut umur di Kabupaten M berikut.\n\nPenjelasan yang paling mungkin untuk rendahnya rasio jenis kelamin pada kelompok umur 20–39 tahun adalah …",
      ["Banyak laki-laki usia produktif merantau keluar daerah untuk bekerja", "Lebih banyak bayi perempuan dilahirkan dibandingkan bayi laki-laki",
       "Harapan hidup laki-laki pada usia 20–39 tahun jauh lebih tinggi daripada perempuan", "Banyak perempuan usia produktif bermigrasi keluar daerah",
       "Rasio jenis kelamin selalu di bawah 100 pada semua kelompok umur"],
      "Rasio jenis kelamin (RJK) = jumlah laki-laki ÷ jumlah perempuan × 100. Pada kelompok umur 0–19 tahun RJK sekitar 104–105, sesuai pola alami saat lahir. Namun pada umur 20–39 tahun RJK turun tajam menjadi 78–82, artinya jauh lebih sedikit laki-laki daripada perempuan. Pola ini khas daerah asal migran yang banyak laki-laki usia produktifnya merantau (misalnya ke kota, perkebunan, atau luar negeri). RJK kembali naik pada umur 40–59 tahun ketika sebagian perantau pulang, dan turun lagi pada umur 60+ karena harapan hidup perempuan lebih tinggi.\n\nPengecoh: kelahiran justru lebih banyak bayi laki-laki. Kematian laki-laki muda biasanya sedikit lebih tinggi, bukan sebaliknya. Migrasi perempuan keluar akan menaikkan RJK. RJK tidak selalu di bawah 100.",
      f_sexratio),
    Q("Sebuah provinsi memiliki 12 juta penduduk berusia 65 tahun ke atas dan 60 juta penduduk berusia 0–14 tahun. Indeks penuaan (aging index) provinsi tersebut adalah …",
      ["20", "500", "5", "72", "0,2"],
      "Indeks penuaan = (penduduk 65+ ÷ penduduk 0–14) × 100 = (12 ÷ 60) × 100 = 20.\nArtinya terdapat 20 lansia untuk setiap 100 anak. Indeks penuaan di atas 100 berarti jumlah lansia melebihi jumlah anak, seperti di Jepang dan Italia. Indeks yang terus naik menandakan proses penuaan penduduk.\n\nPengecoh: 500 membalik pembagian (60 ÷ 12 × 100). 5 adalah rasio anak terhadap lansia tanpa dikali 100 secara tepat. 72 menjumlahkan kedua kelompok. 0,2 belum dikalikan 100.",
      None),
    Q("Perhatikan grafik rasio ketergantungan Indonesia berikut. Bonus demografi terjadi ketika rasio ketergantungan berada di bawah 50.\n\nPeriode bonus demografi Indonesia berdasarkan grafik adalah sekitar …",
      ["2012 hingga 2040", "1970 hingga 2000", "2000 hingga 2010", "Setelah tahun 2050", "1980 hingga 2050"],
      "Grafik menunjukkan rasio ketergantungan turun dari 86 (1970) menjadi 51 (2010), lalu berada di bawah garis 50 sekitar 2012 hingga ±2040 (titik terendah ±46 pada 2030), kemudian naik kembali menjadi 53 pada 2050 karena bertambahnya penduduk lansia. Periode di bawah 50 inilah jendela bonus demografi, ketika proporsi penduduk usia produktif sangat besar.\nBonus demografi hanya menjadi keuntungan bila penduduk usia produktif sehat, terdidik, dan memperoleh pekerjaan layak; bila tidak, justru dapat menjadi beban (pengangguran).\n\nPengecoh: 1970–2000 rasio masih di atas 50. 2000–2010 belum di bawah 50. Setelah 2050 rasio naik di atas 50. Periode 1980–2050 terlalu panjang.",
      f_rk),
    Q("Agar bonus demografi benar-benar menjadi keuntungan ekonomi, syarat yang paling penting adalah …",
      ["Tersedianya lapangan kerja produktif dan SDM yang sehat serta terampil", "Meningkatkan angka kelahiran setinggi mungkin agar penduduk muda bertambah",
       "Mengurangi anggaran pendidikan agar dana dialihkan ke pembangunan jalan", "Melarang perempuan bekerja agar fokus mengurus rumah tangga",
       "Menunggu bonus demografi berlalu tanpa kebijakan khusus"],
      "Bonus demografi adalah peluang ketika proporsi penduduk usia produktif tinggi. Peluang ini hanya menghasilkan pertumbuhan ekonomi bila penduduk usia kerja benar-benar bekerja secara produktif. Syaratnya antara lain: pendidikan dan pelatihan yang berkualitas, kesehatan dan gizi yang baik sejak dini, penciptaan lapangan kerja yang luas, partisipasi perempuan dalam angkatan kerja, serta tabungan dan investasi yang meningkat. Tanpa itu, bonus demografi dapat berubah menjadi beban berupa pengangguran dan ketimpangan.\n\nPengecoh: menaikkan kelahiran justru menambah beban anak dan memperpendek jendela bonus. Mengurangi anggaran pendidikan menurunkan kualitas SDM. Melarang perempuan bekerja mengurangi angkatan kerja. Tanpa kebijakan, peluang akan terlewat.",
      None),
    Q("Perhatikan tabel angka kelahiran dan kematian kasar empat negara berikut.\n\nNegara yang berada pada tahap kedua transisi demografi (ledakan penduduk) adalah …",
      ["Negara B", "Negara A", "Negara C", "Negara D", "Negara A dan B"],
      "Tentukan tahap berdasarkan pola CBR dan CDR:\n• A (45 dan 40): kelahiran dan kematian sama-sama tinggi, pertumbuhan alami ±0,5% → tahap 1.\n• B (40 dan 15): kelahiran masih tinggi, kematian sudah turun tajam, pertumbuhan alami (40 − 15) ÷ 10 = 2,5% per tahun → tahap 2 (ledakan penduduk).\n• C (20 dan 8): kelahiran sudah turun, pertumbuhan ±1,2% → tahap 3–4.\n• D (9 dan 11): kelahiran lebih rendah daripada kematian, pertumbuhan alami negatif → tahap 5.\n\nPengecoh: A berada pada tahap 1 karena kematiannya masih tinggi. C dan D berada pada tahap lanjut. Pertumbuhan tercepat terjadi pada tahap 2 karena selisih CBR dan CDR paling lebar.",
      f_dtm_tab),
    Q("Jepang menghadapi penuaan penduduk yang sangat cepat. Kebijakan berikut yang paling tepat untuk mengatasi berkurangnya tenaga kerja adalah …",
      ["Otomatisasi, usia pensiun lebih panjang, dan pekerja migran", "Menurunkan harapan hidup dengan mengurangi layanan kesehatan lansia",
       "Melarang perempuan bekerja agar angka kelahiran naik dengan sendirinya", "Menutup seluruh industri agar kebutuhan tenaga kerja berkurang",
       "Mengirim seluruh penduduk lansia untuk tinggal di negara lain"],
      "Penuaan penduduk menyebabkan jumlah penduduk usia kerja menyusut sementara beban pensiun dan kesehatan meningkat. Kebijakan yang realistis antara lain: (1) otomatisasi dan robotika untuk menggantikan sebagian tenaga kerja, termasuk perawatan lansia; (2) memperpanjang usia pensiun dan mendorong lansia sehat tetap bekerja; (3) meningkatkan partisipasi perempuan di pasar kerja dengan dukungan penitipan anak; (4) menerima pekerja migran, misalnya melalui program pekerja terampil spesifik, termasuk dari Indonesia; serta (5) insentif kelahiran.\n\nPengecoh: mengurangi layanan kesehatan lansia tidak etis. Melarang perempuan bekerja justru mengurangi tenaga kerja dan tidak terbukti menaikkan kelahiran. Menutup industri merusak ekonomi. Memindahkan lansia ke negara lain tidak realistis.",
      None),
]

P3 = [
    Q("Perhatikan peta kepadatan penduduk per provinsi berikut.\n\nFaktor yang paling menjelaskan tingginya kepadatan penduduk di Pulau Jawa dibandingkan Papua adalah …",
      ["Tanah vulkanik subur, sejarah pusat pemerintahan, dan infrastruktur",
       "Jawa memiliki luas daratan terbesar di Indonesia sehingga mampu menampung banyak penduduk",
       "Papua memiliki iklim gurun yang sangat kering sehingga tidak dapat dihuni",
       "Jawa jauh dari gunung api sehingga aman dari bencana alam",
       "Penduduk Papua seluruhnya bermigrasi ke Jawa sejak abad ke-19"],
      "Peta menunjukkan Jawa (terutama DKI Jakarta, Jawa Barat, Banten, Jawa Tengah, dan DIY) memiliki kepadatan di atas 1.000 jiwa/km², sedangkan Papua di bawah 20 jiwa/km². Faktor pendorong kepadatan Jawa: tanah vulkanik yang subur untuk pertanian padi sejak ribuan tahun, dataran rendah dan lembah yang luas, sejarah sebagai pusat kerajaan dan pemerintahan kolonial, serta konsentrasi industri, jasa, dan infrastruktur. Papua memiliki medan pegunungan terjal, hutan lebat, rawa luas, aksesibilitas rendah, dan tanah yang umumnya kurang subur.\n\nPengecoh: luas Jawa justru jauh lebih kecil daripada Kalimantan, Sumatra, dan Papua. Papua beriklim tropis basah, bukan gurun. Jawa justru memiliki banyak gunung api. Tidak ada migrasi massal seluruh penduduk Papua ke Jawa.",
      f_densmap),
    Q("Salah satu hukum migrasi Ravenstein menyatakan bahwa sebagian besar migran berpindah dalam jarak dekat dan jumlahnya berkurang seiring bertambahnya jarak. Prinsip ini sesuai dengan konsep …",
      ["Peluruhan jarak", "Kepadatan agraris", "Transisi epidemiologi", "Bonus demografi", "Kota primat"],
      "Ernst Georg Ravenstein (1885) merumuskan hukum migrasi berdasarkan data sensus Inggris, antara lain: sebagian besar migran berpindah dalam jarak dekat; migran jarak jauh cenderung menuju pusat perdagangan atau industri besar; setiap arus migrasi menimbulkan arus balik; penduduk desa lebih banyak bermigrasi daripada penduduk kota; dan perempuan lebih banyak bermigrasi jarak dekat.\nPrinsip berkurangnya interaksi seiring bertambahnya jarak disebut peluruhan jarak (distance decay), yang juga menjadi dasar model gravitasi.\n\nPengecoh: kepadatan agraris, transisi epidemiologi, bonus demografi, dan kota primat adalah konsep kependudukan lain yang tidak menjelaskan hubungan migrasi dengan jarak.",
      None),
    Q("Perhatikan data migrasi risen tiga provinsi berikut. Angka migrasi neto = (I − E) ÷ P × 1.000 dan efektivitas migrasi = (I − E) ÷ (I + E) × 100.\n\nPernyataan yang tepat adalah …",
      ["Provinsi K: migrasi neto +20 per 1.000 dan efektivitas 50", "Provinsi L: migrasi neto +20 per 1.000 dan efektivitas 40",
       "Provinsi M: migrasi neto +5 per 1.000 dan efektivitas 50", "Provinsi K: migrasi neto +80 per 1.000 dan efektivitas 75",
       "Provinsi L: migrasi neto −40 per 1.000 dan efektivitas −20"],
      "• K: migrasi neto = (120.000 − 40.000) ÷ 4.000.000 × 1.000 = 80.000 ÷ 4.000.000 × 1.000 = 20 per 1.000. Efektivitas = 80.000 ÷ 160.000 × 100 = 50.\n• L: (30.000 − 70.000) ÷ 2.000.000 × 1.000 = −20 per 1.000; efektivitas = −40.000 ÷ 100.000 × 100 = −40.\n• M: (60.000 − 55.000) ÷ 5.000.000 × 1.000 = 1 per 1.000; efektivitas = 5.000 ÷ 115.000 × 100 ≈ 4,3.\nProvinsi K adalah daerah penerima migran dengan arus yang cukup searah. Provinsi M memiliki arus masuk dan keluar hampir seimbang sehingga efektivitasnya rendah.\n\nPengecoh: opsi lain salah tanda atau salah perhitungan.",
      f_migtab),
    Q("Program transmigrasi pada masa Orde Baru memindahkan jutaan penduduk dari Jawa, Bali, dan Madura ke Sumatra, Kalimantan, Sulawesi, dan Papua. Tujuan utama program tersebut adalah …",
      ["Meratakan penduduk dan membuka pusat pertumbuhan di luar Jawa", "Mengurangi jumlah penduduk Indonesia secara keseluruhan",
       "Memindahkan ibu kota negara dari Jakarta ke luar Jawa", "Menghentikan kegiatan pertanian di Pulau Jawa sepenuhnya",
       "Mengirim tenaga kerja ke luar negeri untuk menambah devisa"],
      "Transmigrasi bertujuan meratakan persebaran penduduk yang sangat terkonsentrasi di Jawa, meningkatkan kesejahteraan transmigran melalui kepemilikan lahan, membuka lahan pertanian dan perkebunan baru, serta menumbuhkan pusat-pusat ekonomi dan permukiman di luar Jawa. Banyak kota sekarang, seperti di Lampung dan Kalimantan, berkembang dari permukiman transmigrasi.\nProgram ini juga menimbulkan masalah, misalnya konflik lahan dengan masyarakat lokal dan adat, kerusakan hutan dan gambut, serta lahan yang tidak sesuai untuk pertanian.\n\nPengecoh: transmigrasi tidak mengurangi jumlah penduduk nasional. Transmigrasi bukan pemindahan ibu kota. Pertanian di Jawa tidak dihentikan. Pengiriman tenaga kerja ke luar negeri adalah migrasi internasional, bukan transmigrasi.",
      None),
    Q("Perhatikan model migrasi Everett Lee berikut.\n\nUnsur yang ditunjukkan oleh label K adalah …",
      ["Rintangan antara (jarak, biaya)", "Faktor pendorong di daerah asal", "Faktor penarik di daerah tujuan",
       "Faktor pribadi calon migran", "Arus balik migran ke daerah asal"],
      "Model Everett Lee menggambarkan daerah asal dan daerah tujuan yang masing-masing memiliki faktor positif (+, menarik orang untuk tinggal atau datang), negatif (−, mendorong orang pergi), dan netral (0). Di antara keduanya terdapat rintangan antara (intervening obstacles), digambarkan sebagai penghalang pada panah migrasi (label K). Contohnya jarak yang jauh, biaya transportasi, topografi, perbedaan bahasa dan budaya, serta aturan imigrasi. Selain itu, faktor pribadi seperti usia, pendidikan, dan persepsi memengaruhi cara seseorang menilai semua faktor tersebut.\n\nPengecoh: faktor pendorong dan penarik digambarkan sebagai tanda + dan − di dalam daerah asal dan tujuan. Faktor pribadi tidak digambarkan sebagai penghalang di jalur migrasi. Arus balik tidak ditunjukkan pada gambar.",
      f_lee),
    Q("Setiap hari ratusan ribu orang dari Bekasi, Depok, dan Tangerang bekerja di Jakarta lalu pulang pada sore atau malam hari. Bentuk mobilitas penduduk ini disebut …",
      ["Mobilitas ulang-alik", "Migrasi permanen", "Transmigrasi", "Migrasi internasional", "Ruralisasi"],
      "Mobilitas penduduk dibedakan menjadi mobilitas permanen (migrasi, berpindah tempat tinggal untuk menetap) dan nonpermanen (sirkuler). Mobilitas nonpermanen yang dilakukan setiap hari dengan berangkat dan pulang pada hari yang sama disebut mobilitas ulang-alik atau komuter (nglaju). Gejala ini terjadi di kawasan metropolitan seperti Jabodetabek karena perbedaan harga perumahan di kota inti dan pinggiran, serta konsentrasi lapangan kerja di pusat kota.\nKomuter menimbulkan kemacetan dan tingginya kebutuhan transportasi massal (KRL, MRT, bus).\n\nPengecoh: migrasi permanen berarti menetap. Transmigrasi adalah perpindahan antarpulau yang diatur pemerintah. Migrasi internasional melintasi batas negara. Ruralisasi adalah perpindahan dari kota ke desa.",
      None),
    Q("Perhatikan grafik komuter harian dari Bodetabek ke Jakarta berikut.\n\nKebijakan yang paling efektif untuk mengurangi kemacetan akibat arus komuter tersebut adalah …",
      ["Transportasi massal terpadu dan pusat kerja di pinggiran", "Melarang warga Bodetabek bekerja di Jakarta",
       "Menambah jalan tol baru menuju pusat Jakarta tanpa transportasi umum", "Memindahkan semua perumahan ke pusat kota Jakarta",
       "Menghapus layanan kereta komuter agar warga beralih ke kendaraan pribadi"],
      "Grafik menunjukkan ratusan ribu komuter bergerak dari setiap wilayah penyangga setiap hari, terbesar dari Bekasi (±520 ribu). Mengatasi kemacetan memerlukan pendekatan dari dua sisi: (1) sisi penawaran transportasi: memperluas dan mengintegrasikan transportasi massal (KRL, MRT, LRT, bus) sehingga lebih banyak komuter beralih dari kendaraan pribadi; dan (2) sisi tata ruang: mengembangkan pusat-pusat kerja dan layanan di kota pinggiran (polisentris) serta hunian terjangkau dekat simpul transportasi (TOD), sehingga jarak dan kebutuhan perjalanan berkurang.\n\nPengecoh: melarang bekerja di Jakarta tidak realistis. Menambah jalan tol tanpa transportasi umum cenderung memicu lebih banyak kendaraan (induced demand). Memindahkan semua perumahan ke pusat kota tidak mungkin. Menghapus kereta komuter memperparah kemacetan.",
      f_komuter),
    Q("Remitansi yang dikirim pekerja migran Indonesia di luar negeri berdampak besar bagi daerah asal seperti NTB, NTT, dan Jawa Timur. Dampak positif yang paling tepat adalah …",
      ["Menambah pendapatan keluarga serta biaya sekolah dan usaha", "Mengurangi jumlah penduduk Indonesia secara signifikan setiap tahun",
       "Menghilangkan seluruh masalah sosial keluarga yang ditinggalkan", "Membuat daerah asal tidak lagi memerlukan pembangunan infrastruktur",
       "Menurunkan devisa negara karena uang dikirim ke luar negeri"],
      "Remitansi adalah kiriman uang atau barang dari migran kepada keluarga di daerah asal. Dampak positifnya: meningkatkan pendapatan dan konsumsi rumah tangga, membiayai pendidikan anak, membangun atau memperbaiki rumah, modal usaha, serta menjadi sumber devisa negara yang besar. Beberapa desa di NTB dan Jawa Timur mengalami perubahan fisik dan ekonomi yang nyata karena remitansi.\nNamun migrasi tenaga kerja juga menimbulkan masalah, seperti anak yang ditinggal orang tua, risiko eksploitasi pekerja migran, dan konsumsi yang tidak produktif.\n\nPengecoh: jumlah pekerja migran tidak mengurangi penduduk secara signifikan. Masalah sosial justru dapat muncul. Daerah asal tetap memerlukan infrastruktur. Remitansi justru menambah devisa karena uang mengalir masuk ke Indonesia.",
      None),
    Q("Perhatikan grafik jumlah migran ke Kota J menurut jarak daerah asal berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Jumlah migran berkurang tajam seiring bertambahnya jarak daerah asal", "Jumlah migran bertambah seiring bertambahnya jarak daerah asal",
       "Jarak tidak berpengaruh karena jumlah migran dari semua jarak sama", "Migran paling banyak berasal dari daerah sejauh 1.600 km",
       "Setiap penggandaan jarak menambah jumlah migran menjadi dua kali lipat"],
      "Grafik menunjukkan jumlah migran terbanyak berasal dari daerah dekat (±180 ribu dari jarak 50 km), lalu turun drastis seiring bertambahnya jarak: ±95 ribu (100 km), ±48 ribu (200 km), hingga hanya ±5 ribu (1.600 km). Pola penurunan ini disebut peluruhan jarak (distance decay): semakin jauh jarak, semakin besar biaya, waktu, dan hambatan sosial-budaya, serta semakin sedikit informasi dan jaringan kerabat di tempat tujuan. Pola ini sesuai dengan hukum migrasi Ravenstein dan model gravitasi.\nPada data ini, setiap kali jarak berlipat dua, jumlah migran kira-kira berkurang setengahnya.\n\nPengecoh: jumlah migran tidak bertambah dengan jarak. Jarak jelas berpengaruh. Migran dari jarak 1.600 km paling sedikit. Penggandaan jarak justru mengurangi migran.",
      f_decay),
    Q("Banyak dokter dan insinyur dari negara berkembang bekerja di negara maju karena gaji dan fasilitas yang lebih baik. Fenomena ini disebut … dan dampaknya bagi negara asal adalah …",
      ["Brain drain; negara asal kehilangan tenaga ahli yang telah dididik dengan biaya besar", "Brain gain; negara asal memperoleh tambahan tenaga ahli dari luar negeri",
       "Urbanisasi; penduduk desa pindah ke kota sehingga desa kekurangan petani", "Ruralisasi; tenaga ahli kembali ke desa untuk membangun pertanian",
       "Transmigrasi; tenaga ahli dipindahkan ke pulau lain oleh pemerintah"],
      "Brain drain (kebocoran otak) adalah perpindahan tenaga terdidik dan terampil dari negara asal ke negara lain yang menawarkan pendapatan, fasilitas penelitian, dan kualitas hidup lebih baik. Negara asal dirugikan karena kehilangan tenaga ahli yang pendidikannya dibiayai negara dan masyarakat, sehingga layanan kesehatan, teknologi, dan inovasi di dalam negeri terhambat. Namun ada juga dampak positif seperti remitansi, jaringan diaspora, dan kemungkinan pulangnya tenaga ahli (brain circulation) yang membawa pengetahuan baru.\n\nPengecoh: brain gain dialami negara penerima. Urbanisasi, ruralisasi, dan transmigrasi adalah bentuk mobilitas lain yang tidak menggambarkan perpindahan tenaga ahli antarnegara.",
      None),
]

P4 = [
    Q("Perhatikan grafik persentase penduduk perkotaan beberapa provinsi berikut.\n\nPenjelasan yang paling tepat untuk perbedaan tingkat urbanisasi antara DKI Jakarta dan NTT adalah …",
      ["Jakarta adalah pusat ekonomi dan jasa, sedangkan NTT masih didominasi pertanian perdesaan", "NTT memiliki penduduk lebih banyak sehingga tingkat urbanisasinya rendah",
       "Seluruh penduduk NTT tinggal di pulau-pulau tanpa kota sama sekali", "Tingkat urbanisasi ditentukan oleh luas wilayah, bukan kegiatan ekonomi",
       "Jakarta tidak memiliki kawasan perdesaan karena seluruh penduduknya petani"],
      "Tingkat urbanisasi DKI Jakarta 100% karena seluruh wilayahnya berupa kawasan perkotaan dengan dominasi kegiatan industri, perdagangan, jasa, dan pemerintahan. Sebaliknya NTT hanya sekitar 25% karena sebagian besar penduduknya tinggal di perdesaan dan bekerja di sektor pertanian, peternakan, dan perikanan, dengan kota-kota yang relatif kecil seperti Kupang. Provinsi dengan industri dan jasa yang berkembang (Jawa Barat, Banten, Kalimantan Timur) memiliki tingkat urbanisasi lebih tinggi.\n\nPengecoh: penduduk NTT jauh lebih sedikit daripada Jawa Barat. NTT memiliki kota-kota, meskipun kecil. Tingkat urbanisasi tidak ditentukan luas wilayah. Penduduk Jakarta bukan petani.",
      f_urbprov),
    Q("Menurut aturan peringkat–ukuran (rank-size rule), jika kota terbesar suatu negara berpenduduk 8 juta jiwa, kota terbesar keempat seharusnya berpenduduk sekitar …",
      ["2 juta jiwa", "4 juta jiwa", "32 juta jiwa", "6 juta jiwa", "0,5 juta jiwa"],
      "Aturan peringkat–ukuran (Zipf) menyatakan bahwa penduduk kota peringkat ke-n kira-kira sama dengan penduduk kota terbesar dibagi n: Pn = P₁ ÷ n.\nKota peringkat ke-4 = 8 juta ÷ 4 = 2 juta jiwa.\nNegara yang sistem kotanya mengikuti aturan ini dianggap memiliki hierarki kota yang seimbang. Bila kota terbesar jauh lebih besar daripada yang diperkirakan, negara tersebut memiliki kota primat (primate city).\n\nPengecoh: 4 juta jiwa berlaku untuk kota peringkat ke-2. 32 juta jiwa mengalikan dengan 4. 6 juta jiwa mengurangkan 2 juta. 0,5 juta jiwa membagi dengan 16 (kuadrat peringkat).",
      None),
    Q("Perhatikan tabel lima kota terbesar Negara N berikut. Indeks primasi = penduduk kota terbesar ÷ penduduk kota kedua.\n\nPernyataan yang paling tepat adalah …",
      ["Indeks primasi sekitar 3,6 sehingga Negara N memiliki kota primat", "Indeks primasi sekitar 2 sehingga sesuai dengan aturan peringkat–ukuran",
       "Indeks primasi sekitar 0,28 sehingga kota kedua lebih dominan", "Indeks primasi sekitar 7 karena dibagi kota terkecil",
       "Negara N tidak memiliki kota primat karena kota terbesar hanya sedikit lebih besar"],
      "Indeks primasi = 10.500.000 ÷ 2.900.000 ≈ 3,6.\nMenurut aturan peringkat–ukuran, kota terbesar seharusnya sekitar dua kali kota kedua (indeks ±2). Nilai 3,6 jauh lebih besar, artinya Kota A sangat dominan dibandingkan kota-kota lain. Kondisi ini disebut kota primat (primate city), yang biasanya menjadi pusat pemerintahan, ekonomi, dan budaya sekaligus, seperti Jakarta, Bangkok, atau Manila. Dampaknya: ketimpangan pembangunan antarwilayah dan beban berlebih pada kota utama.\n\nPengecoh: indeks 2 tidak sesuai dengan data. 0,28 membalik pembagian. 7 diperoleh bila membagi dengan kota terkecil dalam tabel (10,5 ÷ 1,5), padahal indeks primasi membandingkan kota pertama dan kedua. Kota A jauh lebih besar, bukan sedikit lebih besar.",
      f_ranksize),
    Q("Perkembangan kawasan perkotaan yang menyebar tidak terencana ke daerah pinggiran dengan kepadatan rendah, mengonversi sawah dan menimbulkan ketergantungan pada kendaraan pribadi, disebut …",
      ["Urban sprawl", "Gentrifikasi", "Kota kompak (compact city)", "Ruralisasi", "Suburbanisasi terencana dengan TOD"],
      "Urban sprawl adalah perluasan kawasan terbangun kota ke wilayah pinggiran secara menyebar, berkepadatan rendah, dan sering tidak terencana, misalnya perumahan yang muncul memanjang di sepanjang jalan (ribbon development) atau meloncat-loncat (leapfrog). Dampaknya antara lain alih fungsi lahan pertanian, biaya infrastruktur tinggi, ketergantungan pada kendaraan pribadi, kemacetan, dan emisi. Gejala ini terlihat di sekitar Jabodetabek, Surabaya, dan Medan.\n\nPengecoh: gentrifikasi adalah perubahan kawasan kota lama karena masuknya penduduk berpendapatan tinggi. Kota kompak justru kebalikan sprawl (padat, campuran, dan ramah pejalan kaki). Ruralisasi adalah perpindahan ke desa. Pembangunan berorientasi transit (TOD) adalah perkembangan terencana di sekitar simpul transportasi.",
      None),
    Q("Perhatikan grafik indeks komponen IPM tiga provinsi berikut.\n\nDimensi pembangunan manusia yang paling tertinggal di Papua dan paling perlu diprioritaskan adalah …",
      ["Pendidikan, dengan indeks sekitar 0,48", "Kesehatan, dengan indeks sekitar 0,72", "Pengeluaran, dengan indeks sekitar 0,62",
       "Kesehatan, karena indeksnya paling tinggi di antara ketiganya", "Semua dimensi sama karena IPM dihitung dari rata-rata"],
      "IPM disusun dari tiga dimensi: umur panjang dan sehat (indeks kesehatan/harapan hidup), pengetahuan (indeks pendidikan dari harapan lama sekolah dan rata-rata lama sekolah), serta standar hidup layak (indeks pengeluaran per kapita). Pada grafik, indeks pendidikan Papua (±0,48) paling rendah, jauh di bawah DIY (±0,80) dan Jawa Timur (±0,67). Kesenjangan terbesar ini menunjukkan dimensi pendidikan paling perlu diprioritaskan, misalnya pemerataan guru, sekolah, dan akses pendidikan di daerah terpencil.\n\nPengecoh: indeks kesehatan dan pengeluaran Papua lebih tinggi daripada pendidikan. Indeks kesehatan memang tertinggi, sehingga bukan yang paling tertinggal. Walaupun IPM merupakan rata-rata geometrik, nilai masing-masing dimensi tetap berbeda.",
      f_ipm),
    Q("Sebuah kabupaten memiliki 200.000 penduduk usia kerja, 140.000 di antaranya termasuk angkatan kerja, dan 7.000 orang menganggur. Tingkat partisipasi angkatan kerja (TPAK) dan tingkat pengangguran terbuka (TPT) adalah …",
      ["TPAK 70% dan TPT 5%", "TPAK 70% dan TPT 3,5%", "TPAK 143% dan TPT 5%", "TPAK 66,5% dan TPT 5,3%", "TPAK 30% dan TPT 20%"],
      "• TPAK = angkatan kerja ÷ penduduk usia kerja × 100% = 140.000 ÷ 200.000 × 100% = 70%.\n• TPT = jumlah penganggur ÷ angkatan kerja × 100% = 7.000 ÷ 140.000 × 100% = 5%.\nPenting: penyebut TPT adalah angkatan kerja, bukan penduduk usia kerja. Penduduk usia kerja yang bukan angkatan kerja, misalnya pelajar, ibu rumah tangga, dan pensiunan, tidak dihitung sebagai penganggur.\n\nPengecoh: TPT 3,5% membagi penganggur dengan penduduk usia kerja. TPAK 143% membalik pembagian. 66,5% dan 5,3% berasal dari salah mengurangkan penganggur. TPAK 30% adalah persentase bukan angkatan kerja, dan TPT 20% tidak sesuai perhitungan.",
      None),
    Q("Perhatikan data ketenagakerjaan dua kabupaten berikut.\n\nPernyataan yang tepat berdasarkan data tersebut adalah …",
      ["TPT X sekitar 7,1%, lebih tinggi daripada Y sekitar 4,0%", "TPT Kabupaten Y lebih tinggi karena jumlah penganggurnya lebih banyak",
       "TPAK kedua kabupaten sama, yaitu 70%", "TPT Kabupaten X sekitar 5,0% karena dibagi penduduk usia kerja", "Kabupaten Y memiliki 288.000 penganggur"],
      "• Kabupaten X: penganggur = 560.000 − 520.000 = 40.000; TPT = 40.000 ÷ 560.000 × 100% ≈ 7,1%; TPAK = 560.000 ÷ 800.000 = 70%.\n• Kabupaten Y: penganggur = 300.000 − 288.000 = 12.000; TPT = 12.000 ÷ 300.000 × 100% = 4,0%; TPAK = 300.000 ÷ 500.000 = 60%.\nTPT Kabupaten X lebih tinggi daripada Kabupaten Y.\n\nPengecoh: jumlah penganggur Y (12.000) justru lebih sedikit. TPAK kedua kabupaten berbeda (70% dan 60%). TPT X 5,0% muncul bila penganggur dibagi penduduk usia kerja (40.000 ÷ 800.000). 288.000 adalah jumlah yang bekerja di Kabupaten Y, bukan penganggur.",
      f_tpt),
    Q("Data di banyak negara menunjukkan bahwa semakin tinggi pendidikan perempuan, semakin rendah angka kematian bayi dan semakin baik gizi anak. Mekanisme yang paling menjelaskan hubungan ini adalah …",
      ["Ibu berpendidikan lebih memahami kesehatan, gizi, dan memanfaatkan layanan kesehatan", "Ibu berpendidikan tinggi memiliki anak lebih banyak sehingga lebih berpengalaman",
       "Pendidikan perempuan meningkatkan angka kelahiran dan memperbesar keluarga", "Pendidikan perempuan tidak berkaitan dengan kesehatan keluarga",
       "Ibu berpendidikan tinggi tidak memerlukan layanan kesehatan sama sekali"],
      "Pendidikan perempuan merupakan salah satu faktor terkuat yang memengaruhi kualitas penduduk. Ibu yang berpendidikan cenderung lebih memahami pentingnya gizi seimbang, ASI eksklusif, imunisasi, kebersihan, dan tanda bahaya penyakit; lebih mampu mengakses dan memanfaatkan layanan kesehatan; memiliki pendapatan lebih baik; serta menunda usia menikah dan mengatur jarak kelahiran. Semua faktor ini menurunkan risiko kematian bayi dan masalah gizi seperti stunting.\n\nPengecoh: ibu berpendidikan cenderung memiliki anak lebih sedikit, bukan lebih banyak. Pendidikan perempuan menurunkan, bukan meningkatkan, kelahiran. Hubungan pendidikan dan kesehatan keluarga sangat kuat. Ibu berpendidikan tetap memerlukan layanan kesehatan.",
      None),
    Q("Perhatikan grafik pendidikan tertinggi menurut kelompok umur berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Generasi muda lebih terdidik; porsi ≤ SD makin kecil", "Generasi tua lebih terdidik karena porsi perguruan tinggi lebih besar",
       "Pendidikan penduduk tidak berubah antargenerasi", "Kelompok umur 65+ memiliki porsi perguruan tinggi tertinggi",
       "Porsi pendidikan SMP–SMA paling kecil pada kelompok umur 25–34 tahun"],
      "Grafik menunjukkan porsi penduduk berpendidikan SD atau lebih rendah turun dari ±80% pada kelompok umur 65+ menjadi ±18% pada kelompok umur 25–34 tahun. Sebaliknya porsi pendidikan SMP–SMA naik dari ±16% menjadi ±57%, dan porsi perguruan tinggi naik dari ±4% menjadi ±25%. Artinya generasi muda jauh lebih terdidik, hasil perluasan akses sekolah seperti program wajib belajar dan pembangunan sekolah dasar sejak 1970-an. Perbaikan ini mendukung peningkatan kualitas sumber daya manusia untuk memanfaatkan bonus demografi.\n\nPengecoh: generasi tua justru kurang terdidik. Pendidikan jelas berubah antargenerasi. Porsi perguruan tinggi pada kelompok 65+ paling kecil. Porsi SMP–SMA pada kelompok 25–34 tahun justru terbesar.",
      f_didik),
    Q("Indeks Pembangunan Manusia (IPM) Indonesia dihitung dari tiga dimensi. Pasangan dimensi dan indikatornya yang tepat adalah …",
      ["Umur panjang dan hidup sehat – angka harapan hidup saat lahir", "Pengetahuan – angka kematian bayi dan angka kematian ibu",
       "Standar hidup layak – rata-rata lama sekolah penduduk dewasa", "Umur panjang dan hidup sehat – pengeluaran per kapita disesuaikan",
       "Pengetahuan – jumlah rumah sakit per 100.000 penduduk"],
      "IPM terdiri atas tiga dimensi dengan indikator sebagai berikut:\n• Umur panjang dan hidup sehat: angka harapan hidup saat lahir.\n• Pengetahuan: harapan lama sekolah (anak usia 7 tahun) dan rata-rata lama sekolah (penduduk 25 tahun ke atas).\n• Standar hidup layak: pengeluaran per kapita yang disesuaikan (paritas daya beli).\nNilai IPM merupakan rata-rata geometrik dari indeks ketiga dimensi tersebut.\n\nPengecoh: angka kematian bayi dan ibu tidak menjadi indikator langsung IPM. Rata-rata lama sekolah adalah indikator pengetahuan, bukan standar hidup. Pengeluaran per kapita adalah indikator standar hidup layak. Jumlah rumah sakit bukan indikator IPM.",
      None),
]

P5 = [
    Q("Perhatikan grafik proyeksi struktur umur penduduk Indonesia berikut.\n\nImplikasi kebijakan yang paling tepat berdasarkan proyeksi tersebut adalah …",
      ["Menyiapkan jaminan sosial dan layanan kesehatan lansia", "Membangun lebih banyak sekolah dasar karena porsi anak naik tajam",
       "Mengurangi layanan kesehatan karena penduduk usia produktif meningkat", "Tidak perlu kebijakan karena struktur umur tetap sama hingga 2050",
       "Mendorong ledakan kelahiran agar porsi lansia tidak bertambah sama sekali"],
      "Proyeksi menunjukkan porsi penduduk 65 tahun ke atas naik dari ±6% (2020) menjadi ±19% (2050), atau sekitar tiga kali lipat, sedangkan porsi anak 0–14 tahun turun dari ±24% menjadi ±17% dan porsi usia produktif turun perlahan. Indonesia sedang menuju penduduk menua (aging population). Implikasinya: perlu memperkuat sistem jaminan pensiun dan sosial, layanan kesehatan untuk penyakit tidak menular dan geriatri, infrastruktur ramah lansia, serta memanfaatkan sisa bonus demografi untuk menabung dan berinvestasi.\n\nPengecoh: porsi anak justru menurun. Kebutuhan layanan kesehatan meningkat, bukan berkurang. Struktur umur jelas berubah. Mendorong ledakan kelahiran tidak menghentikan penuaan dan menambah beban baru.",
      f_proyeksi),
    Q("Program Keluarga Berencana (KB) di Indonesia sejak 1970-an dinilai berhasil. Dampak demografis paling nyata dari keberhasilan program tersebut adalah …",
      ["TFR turun dan laju pertumbuhan penduduk melambat", "Kenaikan angka kematian bayi karena jumlah anak berkurang",
       "Bertambahnya proporsi penduduk usia 0–14 tahun secara drastis", "Hilangnya seluruh migrasi desa–kota di Indonesia",
       "Kenaikan angka kelahiran kasar menjadi lebih dari 40 per 1.000"],
      "Program KB mendorong penggunaan kontrasepsi, menunda usia kawin, dan mengampanyekan norma keluarga kecil. Hasilnya, TFR Indonesia turun dari ±5,6 (1971) menjadi ±2,2 (2020), dan laju pertumbuhan penduduk melambat dari ±2,3% per tahun (1970-an) menjadi sekitar 1,2% per tahun. Penurunan fertilitas ini juga membuka jendela bonus demografi karena proporsi anak menurun sementara proporsi penduduk usia produktif meningkat.\n\nPengecoh: kematian bayi justru menurun berkat jarak kelahiran yang lebih baik. Proporsi anak menurun, bukan bertambah. KB tidak berhubungan langsung dengan hilangnya migrasi. CBR justru turun.",
      None),
    Q("Perhatikan diagram pencar rata-rata lama sekolah perempuan dan TFR beberapa provinsi berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Lama sekolah perempuan tinggi cenderung disertai TFR rendah", "Lama sekolah perempuan yang lebih tinggi selalu menaikkan TFR",
       "Tidak ada hubungan antara pendidikan perempuan dan TFR", "Provinsi G memiliki TFR tertinggi karena lama sekolahnya tertinggi",
       "Setiap tambahan satu tahun sekolah pasti menurunkan TFR tepat satu anak"],
      "Titik-titik menunjukkan pola menurun: provinsi A dengan rata-rata lama sekolah perempuan ±6,5 tahun memiliki TFR ±3,4, sedangkan provinsi G dengan ±11 tahun memiliki TFR ±1,8. Artinya terdapat hubungan negatif antara pendidikan perempuan dan fertilitas. Mekanismenya antara lain penundaan usia kawin, akses dan pengetahuan kontrasepsi, partisipasi kerja, dan perubahan preferensi jumlah anak.\nHubungan ini adalah korelasi; faktor lain seperti pendapatan, urbanisasi, dan budaya juga berpengaruh, sehingga tidak dapat disimpulkan bahwa setiap tambahan satu tahun sekolah menurunkan TFR tepat satu anak (pada grafik penurunannya sekitar 0,35 anak per tahun sekolah).\n\nPengecoh: hubungan bukan positif. Hubungan jelas ada. Provinsi G memiliki TFR terendah. Besaran penurunan tidak tepat satu anak.",
      f_tfr_edu),
    Q("Singapura dan Korea Selatan memberikan insentif uang tunai, cuti melahirkan panjang, dan subsidi penitipan anak bagi keluarga yang memiliki anak. Kebijakan ini tergolong …",
      ["Kebijakan pronatalis untuk menaikkan angka kelahiran yang sangat rendah", "Kebijakan antinatalis untuk menurunkan angka kelahiran yang tinggi",
       "Kebijakan transmigrasi untuk meratakan persebaran penduduk", "Kebijakan urbanisasi untuk memindahkan penduduk desa ke kota",
       "Kebijakan imigrasi untuk menolak semua pekerja asing"],
      "Kebijakan pronatalis bertujuan menaikkan angka kelahiran. Kebijakan ini diterapkan oleh negara-negara dengan TFR sangat rendah, misalnya Korea Selatan (TFR sekitar 0,7–0,8, terendah di dunia) dan Singapura (sekitar 1,0). Fertilitas yang sangat rendah menyebabkan penuaan cepat, menyusutnya tenaga kerja, dan bahkan penurunan jumlah penduduk. Insentif finansial, cuti orang tua, layanan penitipan anak, dan dukungan perumahan diberikan untuk mengurangi biaya membesarkan anak.\nSebaliknya, kebijakan antinatalis bertujuan menurunkan kelahiran, misalnya program KB Indonesia dan kebijakan satu anak di Tiongkok (1980–2015).\n\nPengecoh: kebijakan pada soal bukan antinatalis, transmigrasi, urbanisasi, atau penolakan imigrasi.",
      None),
    Q("Perhatikan grafik rasio jenis kelamin saat lahir di Negara C berikut.\n\nPenjelasan yang paling mungkin untuk kenaikan rasio hingga ±118 pada 2000-an adalah …",
      ["Preferensi anak laki-laki ditambah kebijakan pembatasan jumlah anak", "Bayi perempuan secara biologis lebih jarang dilahirkan di semua negara",
       "Kenaikan angka kematian ibu menyebabkan bayi laki-laki lebih banyak", "Banyak laki-laki bermigrasi masuk ke Negara C setiap tahun",
       "Rasio di atas 105 adalah kondisi alami yang terjadi di seluruh dunia"],
      "Secara alami, rasio jenis kelamin saat lahir sekitar 105 laki-laki per 100 perempuan. Grafik menunjukkan Negara C mencapai ±118 pada 2005–2010, jauh di atas nilai alami. Pola ini dikenal di beberapa negara Asia, misalnya Tiongkok, ketika kebijakan pembatasan jumlah anak bertemu dengan preferensi budaya yang kuat terhadap anak laki-laki, sehingga terjadi seleksi jenis kelamin sebelum kelahiran. Dampak jangka panjangnya adalah kelebihan laki-laki dewasa yang sulit mencari pasangan dan masalah sosial lainnya. Rasio menurun setelah kebijakan dilonggarkan dan seleksi jenis kelamin dilarang.\n\nPengecoh: rasio alami ±105 tidak menjelaskan nilai 118. Kematian ibu tidak memengaruhi rasio saat lahir. Migrasi tidak memengaruhi rasio saat lahir. Nilai 118 bukan kondisi alami.",
      f_srb),
    Q("Tingkat fertilitas penggantian (replacement level fertility) sekitar 2,1 anak per perempuan. Angka ini sedikit di atas 2 karena …",
      ["Ada kematian anak dan bayi laki-laki sedikit lebih banyak", "Setiap keluarga wajib memiliki minimal dua anak menurut hukum",
       "Perempuan selalu melahirkan anak kembar pada kelahiran pertama", "Angka harapan hidup laki-laki lebih tinggi daripada perempuan",
       "Migrasi masuk selalu menambah 0,1 anak per perempuan di semua negara"],
      "Agar setiap generasi tepat menggantikan generasi sebelumnya, rata-rata setiap perempuan perlu digantikan oleh satu anak perempuan yang bertahan hidup hingga usia reproduksi. Karena: (1) rasio jenis kelamin saat lahir sekitar 105 laki-laki per 100 perempuan, sehingga perlu lebih dari 2 kelahiran untuk memperoleh satu anak perempuan; dan (2) sebagian anak meninggal sebelum mencapai usia reproduksi, maka TFR penggantian di negara dengan kematian rendah sekitar 2,1. Di negara dengan kematian anak tinggi, angka penggantian bisa lebih dari 2,5.\n\nPengecoh: tidak ada hukum yang mewajibkan dua anak. Kelahiran kembar tidak terjadi selalu. Harapan hidup perempuan umumnya lebih tinggi. Migrasi tidak termasuk dalam definisi fertilitas penggantian.",
      None),
    Q("Perhatikan piramida penduduk Kecamatan W berikut.\n\nJenis wilayah yang paling sesuai dengan bentuk piramida tersebut adalah …",
      ["Kawasan tambang yang menarik pekerja laki-laki produktif", "Desa asal perantau yang ditinggalkan laki-laki usia produktif",
       "Kawasan permukiman pensiunan yang didominasi penduduk lanjut usia", "Desa dengan angka kelahiran sangat tinggi dan kematian tinggi",
       "Kota yang mengalami penurunan jumlah penduduk laki-laki"],
      "Piramida Kecamatan W memperlihatkan tonjolan sangat besar pada penduduk laki-laki usia 20–44 tahun (hingga ±9,8%), jauh lebih besar daripada perempuan pada kelompok umur yang sama (±3,6%). Kelompok anak dan lansia relatif kecil. Pola ini khas wilayah yang menarik migran pekerja laki-laki usia produktif, misalnya kawasan pertambangan (seperti di Morowali, Mimika, atau Kalimantan Timur), perkebunan baru, atau proyek industri, ketika banyak pekerja datang tanpa membawa keluarga.\n\nPengecoh: desa asal perantau justru kekurangan laki-laki usia produktif. Permukiman pensiunan didominasi lansia. Desa dengan kelahiran tinggi akan berbentuk ekspansif dengan alas lebar. Piramida ini menunjukkan kelebihan, bukan kekurangan, laki-laki.",
      f_pyr_tambang),
    Q("Sumber data kependudukan yang mencacah seluruh penduduk di suatu wilayah pada waktu tertentu dan dilaksanakan setiap sepuluh tahun di Indonesia adalah …",
      ["Sensus penduduk lengkap", "Survei Sosial Ekonomi Nasional", "Registrasi penduduk", "Survei Angkatan Kerja Nasional",
       "Survei Penduduk Antar Sensus"],
      "Sumber data kependudukan utama:\n• Sensus penduduk: pencacahan lengkap seluruh penduduk pada waktu tertentu, dilaksanakan BPS setiap sepuluh tahun (tahun berakhiran 0, misalnya SP2020).\n• Survei: pengumpulan data dari sampel penduduk, misalnya Susenas (sosial-ekonomi), Sakernas (ketenagakerjaan), dan SUPAS (dilaksanakan di antara dua sensus, tahun berakhiran 5).\n• Registrasi: pencatatan peristiwa vital secara terus-menerus, seperti kelahiran, kematian, perkawinan, dan perpindahan, oleh dinas kependudukan dan pencatatan sipil.\nSensus 2020 untuk pertama kalinya memadukan data registrasi (administrasi kependudukan) dengan pencacahan lapangan dan daring.\n\nPengecoh: Susenas, Sakernas, dan SUPAS adalah survei berbasis sampel. Registrasi dilakukan terus-menerus, bukan setiap sepuluh tahun.",
      None),
    Q("Perhatikan grafik rasio ketergantungan lansia tiga negara berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Korea Selatan mengalami peningkatan tercepat dan pada 2050 melampaui Jepang", "Indonesia memiliki rasio tertinggi sepanjang periode 2000–2050",
       "Rasio ketiga negara tidak berubah dari tahun 2000 hingga 2050", "Jepang mengalami penurunan rasio ketergantungan lansia sejak 2000",
       "Rasio Indonesia pada 2050 lebih tinggi daripada Jepang pada 2020"],
      "Grafik menunjukkan rasio ketergantungan lansia (penduduk 65+ per 100 penduduk 15–64) Jepang naik dari 25 menjadi 74, Korea Selatan dari 10 menjadi 78, dan Indonesia dari 7 menjadi 26. Korea Selatan mengalami peningkatan paling cepat (hampir delapan kali lipat) dan pada 2050 melampaui Jepang, akibat TFR yang sangat rendah dan harapan hidup yang tinggi. Indonesia juga menua, tetapi lebih lambat.\n\nPengecoh: rasio Indonesia justru terendah. Rasio ketiga negara jelas meningkat. Jepang tidak mengalami penurunan. Rasio Indonesia pada 2050 (26) jauh lebih rendah daripada Jepang pada 2020 (48).",
      f_oadr),
    Q("Diaspora Indonesia di berbagai negara semakin dipandang sebagai aset pembangunan. Kontribusi diaspora yang paling tepat bagi negara asal adalah …",
      ["Remitansi, investasi, transfer pengetahuan, dan jejaring", "Mengurangi jumlah penduduk Indonesia hingga separuhnya",
       "Menggantikan seluruh tenaga kerja dalam negeri dengan tenaga asing", "Menghapus kewajiban pemerintah memberi perlindungan warga di luar negeri",
       "Menghentikan seluruh migrasi internasional dari Indonesia"],
      "Diaspora adalah komunitas warga negara atau keturunan suatu bangsa yang tinggal di luar negeri. Diaspora dapat berkontribusi bagi negara asal melalui remitansi, investasi dan pendirian usaha, transfer pengetahuan dan teknologi, jejaring perdagangan dan pariwisata, serta diplomasi budaya. Banyak negara, seperti India, Tiongkok, dan Filipina, memanfaatkan diaspora sebagai jembatan ke ekonomi global.\nKarena itu, negara perlu menjaga hubungan dengan diaspora, misalnya melalui kemudahan administrasi, kanal investasi, dan perlindungan warga di luar negeri.\n\nPengecoh: diaspora tidak mengurangi penduduk secara drastis. Diaspora tidak menggantikan tenaga kerja dalam negeri. Pemerintah tetap wajib melindungi warganya di luar negeri. Diaspora bukan cara menghentikan migrasi internasional.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
