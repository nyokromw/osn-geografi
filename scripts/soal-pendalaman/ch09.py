from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def lorenz_ax(ax):
    ax.plot([0, 1], [0, 1], color="black", lw=1.2, label="Garis pemerataan sempurna")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
    ax.set_xlabel("Persentase kumulatif penduduk"); ax.set_ylabel("Persentase kumulatif pendapatan")
    ax.set_xticks([0, .2, .4, .6, .8, 1]); ax.set_xticklabels(["0", "20", "40", "60", "80", "100"])
    ax.set_yticks([0, .2, .4, .6, .8, 1]); ax.set_yticklabels(["0", "20", "40", "60", "80", "100"])


def f_lorenz2(path):
    x = np.linspace(0, 1, 100)
    fig, ax = new(6, 6); lorenz_ax(ax)
    ax.plot(x, x ** 1.6, color=C["blue"], lw=2.4, label="Wilayah P"); ax.plot(x, x ** 3.2, color=C["red"], lw=2.4, label="Wilayah Q")
    ax.legend(frameon=False, loc="upper left"); ax.set_title("Kurva Lorenz dua wilayah")
    save(fig, path)


def f_lorenzAB(path):
    x = np.linspace(0, 1, 100); y = x ** 2.33
    fig, ax = new(6, 6); lorenz_ax(ax)
    ax.plot(x, y, color=C["blue"], lw=2.4)
    ax.fill_between(x, y, x, color="#FED7D7"); ax.fill_between(x, 0, y, color="#BEE3F8")
    ax.text(0.55, 0.42, "A", fontsize=20, fontweight="bold"); ax.text(0.78, 0.25, "B\n(luas 0,30)", fontsize=12, fontweight="bold", ha="center")
    ax.set_title("Kurva Lorenz Kabupaten L")
    save(fig, path)


def f_desil(path):
    sh = [2, 3, 4, 5, 6, 7, 9, 12, 22, 30]
    bars([f"D{i}" for i in range(1, 11)], {"Porsi pendapatan (%)": sh}, path, title="Porsi pendapatan menurut desil penduduk Negara P (D1 = 10% termiskin)",
         ylabel="% dari total pendapatan", values=True, ylim=(0, 35), colors=[C["teal"]], w=9)


IPMCOL = {"Jakarta Raya": "#2F855A", "Yogyakarta": "#2F855A", "Kalimantan Timur": "#2F855A", "Kepulauan Riau": "#2F855A", "Bali": "#68D391", "Riau": "#68D391",
          "Sulawesi Utara": "#68D391", "Banten": "#68D391", "Jawa Barat": "#68D391", "Jawa Tengah": "#68D391", "Jawa Timur": "#68D391", "Aceh": "#68D391",
          "Sumatera Barat": "#68D391", "Sumatera Utara": "#68D391", "Kalimantan Utara": "#68D391", "Sulawesi Selatan": "#68D391", "Bangka-Belitung": "#68D391",
          "Jambi": "#68D391", "Bengkulu": "#68D391", "Sumatera Selatan": "#68D391", "Lampung": "#68D391", "Kalimantan Selatan": "#68D391", "Kalimantan Tengah": "#68D391",
          "Maluku": "#68D391", "Sulawesi Tenggara": "#68D391", "Sulawesi Tengah": "#68D391", "Gorontalo": "#F6E05E", "Sulawesi Barat": "#F6E05E",
          "Maluku Utara": "#F6E05E", "Kalimantan Barat": "#F6E05E", "Nusa Tenggara Barat": "#F6E05E", "Nusa Tenggara Timur": "#F6E05E", "Papua Barat": "#F6E05E", "Papua": "#E53E3E"}


def f_ipmmap(path):
    fig, ax = indonesia_map(colors=IPMCOL, w=10, h=4.6)
    legend_patches(ax, [("Sangat tinggi (≥ 80)", "#2F855A"), ("Tinggi (70–80)", "#68D391"), ("Sedang (60–70)", "#F6E05E"), ("Rendah (< 60)", "#E53E3E")],
                   title="IPM", loc="lower left", fs=8)
    ax.set_title("Kategori IPM provinsi (disederhanakan)")
    save(fig, path)


def f_corep(path):
    fig, ax = blank(9, 5, (0, 100), (0, 56))
    ax.add_patch(Circle((50, 28), 12, fc="#F6AD55", ec="black")); ax.text(50, 28, "PUSAT\n(kota inti)", ha="center", va="center", fontsize=10, fontweight="bold")
    for (x, y) in [(12, 46), (88, 46), (12, 10), (88, 10)]:
        ax.add_patch(Circle((x, y), 7, fc="#C6F6D5", ec="black")); ax.text(x, y, "pinggiran", ha="center", va="center", fontsize=8.5)
    arrow(ax, 18, 42, 40, 32, color=C["red"], lw=2.2); ax.text(22, 33, "X", fontsize=14, fontweight="bold", color=C["red"])
    arrow(ax, 60, 32, 82, 42, color=C["blue"], lw=2.2); ax.text(73, 33, "Y", fontsize=14, fontweight="bold", color=C["blue"])
    ax.text(2, 1, "X: tenaga kerja terdidik, modal, dan bahan mentah mengalir ke pusat   ·   Y: inovasi, investasi, dan permintaan menyebar ke pinggiran", fontsize=8)
    ax.set_title("Hubungan pusat dan pinggiran")
    save(fig, path)


def f_kuznetsg(path):
    pts = [("A", 1.0, 0.33), ("B", 3.0, 0.42), ("C", 6.0, 0.46), ("D", 12, 0.44), ("E", 25, 0.37), ("F", 45, 0.30)]
    fig, ax = new(8.5, 4.6)
    ax.scatter([p[1] for p in pts], [p[2] for p in pts], s=60, color=C["blue"])
    for n, x, y in pts:
        ax.annotate(n, (x, y), xytext=(4, 5), textcoords="offset points", fontweight="bold")
    xx = np.linspace(0.8, 50, 200); ax.plot(xx, 0.46 - 0.035 * (np.log(xx) - np.log(7)) ** 2, "--", color=C["gray"])
    ax.set_xscale("log"); ax.set_xlabel("PDB per kapita (ribu USD, skala log)"); ax.set_ylabel("Koefisien Gini"); ax.grid(color="#EDF2F7")
    ax.set_title("Pendapatan per kapita dan ketimpangan beberapa negara (ilustrasi)")
    save(fig, path)


# ---- paket 1
def f_ipmtab(path):
    table([["Indeks kesehatan", "0,80"], ["Indeks pendidikan", "0,65"], ["Indeks pengeluaran", "0,75"]], ["Komponen", "Nilai"], path,
          title="Indeks komponen IPM Kabupaten H", col_w=[0.6, 0.4])


def f_miskin(path):
    table([["Jawa Timur", "9,8%", "4,0 juta"], ["Jawa Barat", "7,6%", "3,9 juta"], ["NTT", "19,5%", "1,1 juta"], ["Papua", "26,0%", "0,9 juta"],
           ["DKI Jakarta", "4,4%", "0,5 juta"]], ["Provinsi", "Persentase miskin", "Jumlah miskin"], path,
          title="Kemiskinan di beberapa provinsi (ilustrasi)", col_w=[0.3, 0.38, 0.32])


def f_fgt(path):
    table([["1", "300"], ["2", "400"], ["3", "450"], ["4", "600"], ["5", "800"]], ["Rumah tangga", "Pengeluaran per kapita (ribu Rp/bulan)"], path,
          title="Pengeluaran lima rumah tangga (garis kemiskinan z = 500 ribu Rp)", col_w=[0.35, 0.65])


def f_ipm_miskin(path):
    pts = [("A", 62, 26), ("B", 66, 20), ("C", 69, 14), ("D", 71, 11), ("E", 73, 9), ("F", 76, 7), ("G", 80, 5), ("H", 82, 4)]
    scatter(pts, path, title="IPM dan persentase penduduk miskin beberapa provinsi (ilustrasi)", xlabel="IPM", ylabel="Penduduk miskin (%)", fit=True)


def f_kotadesa(path):
    lines([2014, 2016, 2018, 2020, 2022, 2024], {"Perdesaan": [14.2, 14.1, 13.2, 13.2, 12.4, 11.3], "Perkotaan": [8.2, 7.7, 6.9, 7.9, 7.5, 7.1]}, path,
          title="Persentase penduduk miskin perkotaan dan perdesaan (ilustrasi)", xlabel="Tahun", ylabel="%", w=8.5)


# ---- paket 2
def f_ginitab(path):
    table([["Kuintil 1 (20% termiskin)", "5"], ["Kuintil 2", "10"], ["Kuintil 3", "15"], ["Kuintil 4", "25"], ["Kuintil 5 (20% terkaya)", "45"]],
          ["Kelompok penduduk", "Porsi pendapatan (%)"], path, title="Distribusi pendapatan Negara G menurut kuintil", col_w=[0.6, 0.4])


def f_gini_id(path):
    lines([2000, 2005, 2008, 2011, 2014, 2017, 2020, 2023], {"Koefisien Gini": [0.30, 0.34, 0.35, 0.41, 0.41, 0.39, 0.38, 0.388]}, path,
          title="Koefisien Gini pengeluaran Indonesia (disederhanakan)", xlabel="Tahun", ylabel="Gini", ylim=(0.25, 0.45), w=8.5)


def f_will(path):
    table([["A", "20", "50"], ["B", "40", "50"]], ["Wilayah", "PDRB per kapita (juta Rp)", "Porsi penduduk (%)"], path,
          title="Data dua wilayah dalam satu provinsi", col_w=[0.24, 0.4, 0.36])


def f_pdrbkap(path):
    bars(["DKI Jakarta", "Kalimantan Timur", "Riau", "Jawa Barat", "Sulawesi Selatan", "NTT"], {"PDRB per kapita (juta Rp)": [320, 200, 160, 55, 70, 25]}, path,
         title="PDRB per kapita beberapa provinsi (ilustrasi)", ylabel="juta Rp per orang", values=True, ylim=(0, 360), colors=[C["blue"]], rot=12, w=8.5)


def f_porsiwil(path):
    bars(["Sumatra", "Jawa", "Kalimantan", "Sulawesi", "Bali–Nusa Tenggara", "Maluku–Papua"], {"Porsi penduduk (%)": [22, 56, 6, 7, 6, 3], "Porsi PDB (%)": [22, 57, 8, 7, 3, 3]},
         path, title="Porsi penduduk dan porsi PDB menurut wilayah (ilustrasi)", ylabel="%", values=True, ylim=(0, 65), w=9.5, rot=10)


# ---- paket 3
def f_rostow(path):
    fig, ax = blank(9.5, 4.8, (0, 100), (0, 50))
    names = ["Masyarakat\ntradisional", "Prasyarat\nlepas landas", "Lepas\nlandas", "Menuju\nkedewasaan", "Konsumsi\nmassa tinggi"]
    for i, n in enumerate(names):
        x, y = 2 + i * 19.5, 3 + i * 8.5
        ax.add_patch(Rectangle((x, 0), 18, y + 6, fc=["#E2E8F0", "#BEE3F8", "#90CDF4", "#63B3ED", "#3182CE"][i], ec="black"))
        ax.text(x + 9, y + 2.5, str(i + 1), ha="center", fontsize=15, fontweight="bold")
        ax.text(x + 9, (y + 6) / 2 - 1, n, ha="center", va="center", fontsize=8.5)
    ax.set_title("Tahap-tahap pertumbuhan ekonomi Rostow")
    save(fig, path)


CORE = ["USA", "CAN", "GBR", "FRA", "DEU", "JPN", "AUS", "NZL", "ITA", "ESP", "NLD", "BEL", "CHE", "AUT", "SWE", "NOR", "DNK", "FIN", "IRL", "KOR"]
SEMI = ["CHN", "BRA", "IND", "IDN", "MEX", "RUS", "ZAF", "TUR", "ARG", "MYS", "THA", "SAU", "IRN", "POL", "CHL", "COL", "EGY", "VNM", "PHL"]


def f_sistemdunia(path):
    col = {**{c: "#2B6CB0" for c in CORE}, **{c: "#90CDF4" for c in SEMI}}
    fig, ax = world_map(colors=col, fc="#FBD38D", w=10, h=5)
    legend_patches(ax, [("Kelompok K", "#2B6CB0"), ("Kelompok L", "#90CDF4"), ("Kelompok M", "#FBD38D")], loc="lower left")
    ax.set_title("Pengelompokan negara menurut teori sistem dunia (disederhanakan)")
    save(fig, path)


def f_christaller(path):
    fig, ax = blank(7, 6.3, (-5, 5), (-4.6, 4.6))
    from matplotlib.patches import RegularPolygon
    ax.add_patch(RegularPolygon((0, 0), 6, radius=4.2, orientation=0, fc="#FEFCBF", ec=C["orange"], lw=2))
    for k in range(6):
        a = np.radians(60 * k + 30); x, y = 2.45 * np.cos(a), 2.45 * np.sin(a)
        ax.add_patch(RegularPolygon((x, y), 6, radius=1.4, orientation=0, fc="none", ec=C["blue"], lw=1.2))
        ax.plot(x, y, "o", ms=10, color=C["blue"])
    for k in range(6):
        a = np.radians(60 * k); ax.plot(4.2 * np.cos(a) * 0.98, 4.2 * np.sin(a) * 0.98, "o", ms=6, color=C["green"])
    ax.plot(0, 0, "s", ms=18, color=C["red"])
    legend_patches(ax, [("Pusat orde tinggi (K)", C["red"]), ("Pusat orde menengah (L)", C["blue"]), ("Pusat orde rendah (M)", C["green"])], loc="lower left", fs=8)
    ax.set_title("Hierarki tempat sentral Christaller")
    save(fig, path)


def f_ambang(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    for a, (rr, rt, t) in zip(axs, [(4, 2.5, "Layanan P"), (2, 3.5, "Layanan Q")]):
        a.set_xlim(-5, 5); a.set_ylim(-5, 5); a.set_aspect("equal"); a.axis("off")
        a.add_patch(Circle((0, 0), rr, fc="#C6F6D5", ec=C["green"], lw=2, label="jangkauan (range)"))
        a.add_patch(Circle((0, 0), rt, fc="none", ec=C["red"], lw=2, ls="--", label="ambang (threshold)"))
        a.plot(0, 0, "s", ms=10, color="black"); a.set_title(t, fontsize=13, fontweight="bold")
    axs[0].legend(loc="lower left", fontsize=9)
    fig.suptitle("Ambang (merah putus-putus) dan jangkauan (hijau) dua jenis layanan", fontweight="bold")
    save(fig, path)


def f_klassen(path):
    pts = [("A", 3.5, 60), ("B", 7.2, 75), ("C", 7.8, 22), ("D", 4.0, 28), ("E", 6.5, 58)]
    fig, ax = new(8, 5.2)
    ax.axvline(5.2, color="#718096"); ax.axhline(45, color="#718096")
    for n, x, y in pts:
        ax.plot(x, y, "o", ms=9, color=C["blue"]); ax.text(x + 0.1, y + 2, n, fontsize=13, fontweight="bold")
    ax.text(5.3, 85, "rata-rata provinsi", fontsize=9, color=C["gray"]); ax.text(2.6, 46, "rata-rata provinsi", fontsize=9, color=C["gray"])
    ax.set_xlim(2.5, 9); ax.set_ylim(10, 90); ax.set_xlabel("Laju pertumbuhan ekonomi (%)"); ax.set_ylabel("PDRB per kapita (juta Rp)")
    ax.set_title("Tipologi Klassen kabupaten di Provinsi K")
    save(fig, path)


# ---- paket 4
def f_gniregion(path):
    bars(["Afrika\nSub-Sahara", "Asia Selatan", "Asia Timur\n& Pasifik", "Eropa\n& Asia Tengah", "Amerika Utara"], {"GNI per kapita (USD)": [1700, 2300, 13000, 38000, 75000]},
         path, title="GNI per kapita menurut kawasan (ilustrasi)", ylabel="USD per orang", values=True, ylim=(0, 85000), colors=[C["purple"]], w=9)


def f_ipmgap(path):
    lines([2010, 2013, 2016, 2019, 2022, 2024], {"DKI Jakarta": [76.3, 78.1, 79.6, 80.8, 81.6, 83.0], "Papua": [54.5, 56.3, 58.1, 60.8, 61.4, 63.0]}, path,
          title="IPM DKI Jakarta dan Papua (ilustrasi)", xlabel="Tahun", ylabel="IPM", w=8.5)


def f_tertinggal(path):
    col = {"Papua": "#C53030", "Papua Barat": "#E53E3E", "Nusa Tenggara Timur": "#E53E3E", "Maluku": "#FC8181", "Sulawesi Tengah": "#FEB2B2",
           "Nusa Tenggara Barat": "#FEB2B2", "Sumatera Utara": "#FED7D7", "Sumatera Barat": "#FED7D7", "Maluku Utara": "#FEB2B2", "Lampung": "#FED7D7",
           "Sulawesi Barat": "#FEB2B2", "Kalimantan Barat": "#FED7D7", "Gorontalo": "#FED7D7"}
    fig, ax = indonesia_map(colors=col, fc="#F7FAFC", w=10, h=4.6)
    legend_patches(ax, [("Sangat banyak", "#C53030"), ("Banyak", "#E53E3E"), ("Sedang", "#FC8181"), ("Sedikit", "#FEB2B2"), ("Sangat sedikit", "#FED7D7"), ("Tidak ada", "#F7FAFC")],
                   title="Kabupaten tertinggal", loc="lower left", fs=8)
    ax.set_title("Sebaran kabupaten daerah tertinggal (ilustrasi)")
    save(fig, path)


def f_jalan(path):
    pts = [("A", 0.08, 28), ("B", 0.15, 21), ("C", 0.30, 16), ("D", 0.45, 12), ("E", 0.70, 9), ("F", 1.10, 7), ("G", 1.60, 5)]
    scatter(pts, path, title="Kerapatan jalan dan kemiskinan beberapa kabupaten (ilustrasi)", xlabel="Kerapatan jalan (km per km²)", ylabel="Penduduk miskin (%)", fit=False)


def f_ginikd(path):
    lines([2015, 2017, 2019, 2021, 2023], {"Perkotaan": [0.428, 0.404, 0.392, 0.398, 0.409], "Perdesaan": [0.334, 0.320, 0.317, 0.314, 0.313]}, path,
          title="Koefisien Gini perkotaan dan perdesaan (ilustrasi)", xlabel="Tahun", ylabel="Gini", ylim=(0.28, 0.45), w=8.5)


# ---- paket 5
def f_danadesa(path):
    bars(["2015", "2016", "2017", "2018", "2019", "2023"], {"Dana desa (triliun Rp)": [20.8, 47.0, 60.0, 60.0, 70.0, 70.0]}, path,
         title="Alokasi dana desa nasional", ylabel="triliun Rp", values=True, ylim=(0, 82), colors=[C["green"]], w=8)


def f_kek(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    kek = {"Sei Mangkei": (99.3, 3.2), "Galang Batang": (104.6, 1.0), "Tanjung Api-Api": (104.9, -2.2), "Mandalika": (116.3, -8.9), "Likupang": (125.1, 1.6),
           "Palu": (119.8, -0.8), "Morotai": (128.3, 2.3), "Sorong": (131.2, -0.9), "Maloy": (117.6, 0.9), "Arun": (97.1, 5.2)}
    for n, (x, y) in kek.items():
        ax.plot(x, y, "D", ms=8, color=C["purple"], mec="white")
    ax.set_title("Sebaran Kawasan Ekonomi Khusus (KEK), sebagian (ilustrasi)")
    save(fig, path)


def f_gic(path):
    p = np.arange(5, 100, 10)
    lines(p, {"Negara X": 6.5 - 0.045 * p, "Negara Y": 1.5 + 0.045 * p}, path, title="Kurva insiden pertumbuhan (growth incidence curve)",
          xlabel="Persentil pengeluaran penduduk (5 = termiskin)", ylabel="Pertumbuhan pengeluaran per tahun (%)", w=8.5)


def f_targeting(path):
    table([["Menerima bantuan", "8 juta (P)", "2 juta (Q)"], ["Tidak menerima bantuan", "3 juta (R)", "37 juta (S)"]],
          ["Status bantuan", "RT miskin", "RT tidak miskin"], path, title="Hasil evaluasi penyaluran sebuah program bantuan sosial",
          col_w=[0.34, 0.33, 0.33])


def f_transfer(path):
    bars(["Jawa", "Sumatra", "Kalimantan", "Sulawesi", "Bali–NT", "Maluku–Papua"], {"Transfer ke daerah per kapita (juta Rp)": [2.1, 3.3, 5.2, 4.1, 3.8, 9.6]}, path,
         title="Transfer pusat ke daerah per kapita menurut wilayah (ilustrasi)", ylabel="juta Rp per orang", values=True, ylim=(0, 11), colors=[C["orange"]], w=8.5)


# ============================ questions ============================
P0 = [
    Q("Perhatikan kurva Lorenz dua wilayah berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Wilayah Q lebih timpang karena kurvanya lebih jauh dari garis pemerataan", "Wilayah P lebih timpang karena kurvanya lebih dekat ke garis pemerataan",
       "Kedua wilayah sama timpangnya karena kurvanya bermula dari titik yang sama", "Wilayah Q lebih merata karena kurvanya lebih melengkung",
       "Kurva Lorenz tidak dapat dipakai membandingkan ketimpangan"],
      "Kurva Lorenz menggambarkan persentase kumulatif pendapatan yang diterima persentase kumulatif penduduk. Garis diagonal adalah pemerataan sempurna. Semakin jauh kurva dari diagonal (semakin melengkung ke bawah), semakin besar ketimpangan karena sebagian besar pendapatan dinikmati sedikit penduduk. Kurva Wilayah Q lebih jauh dari diagonal daripada Wilayah P; misalnya 60% penduduk termiskin di Q hanya menerima sekitar 20% pendapatan, sedangkan di P sekitar 44%. Jadi Q lebih timpang dan koefisien Gini-nya lebih besar.\n\nPengecoh: kurva yang dekat diagonal justru lebih merata. Semua kurva Lorenz bermula di (0,0) dan berakhir di (100,100), sehingga titik awal tidak menentukan. Kurva lebih melengkung berarti lebih timpang. Kurva Lorenz justru alat utama membandingkan ketimpangan.",
      f_lorenz2),
    Q("PDB suatu negara sebesar 1.200 miliar USD. Pendapatan faktor yang diterima warganya dari luar negeri 50 miliar USD, sedangkan pendapatan faktor yang dibayarkan ke luar negeri (misalnya laba investor asing) 150 miliar USD. GNI negara tersebut adalah …",
      ["1.100 miliar USD", "1.300 miliar USD", "1.400 miliar USD", "1.000 miliar USD", "1.250 miliar USD"],
      "GNI = PDB + pendapatan faktor dari luar negeri − pendapatan faktor yang dibayarkan ke luar negeri\n= 1.200 + 50 − 150 = 1.100 miliar USD.\nPDB mengukur nilai produksi di dalam wilayah negara, siapa pun pemilik faktor produksinya. GNI mengukur pendapatan yang diterima warga negara, di mana pun mereka berproduksi. Negara yang banyak menerima investasi asing (misalnya tambang dan smelter milik asing) cenderung memiliki GNI lebih kecil daripada PDB karena sebagian laba mengalir ke luar negeri.\n\nPengecoh: 1.300 membalik tanda pendapatan faktor. 1.400 menambahkan keduanya. 1.000 mengurangkan keduanya. 1.250 hanya menambahkan pendapatan dari luar negeri.",
      None),
    Q("Perhatikan kurva Lorenz Kabupaten L berikut. Luas daerah B (di bawah kurva Lorenz) adalah 0,30, sedangkan luas segitiga di bawah garis pemerataan adalah 0,5.\n\nKoefisien Gini Kabupaten L adalah …",
      ["0,40", "0,30", "0,60", "0,20", "0,70"],
      "Koefisien Gini = A ÷ (A + B), dengan A adalah luas antara garis pemerataan dan kurva Lorenz, serta A + B = 0,5 (luas segitiga di bawah diagonal).\nA = 0,5 − 0,30 = 0,20.\nGini = 0,20 ÷ 0,5 = 0,40.\nCara lain: Gini = 1 − 2B = 1 − 2 × 0,30 = 0,40.\nNilai 0,40 tergolong ketimpangan sedang (0,3–0,5).\n\nPengecoh: 0,30 adalah luas B. 0,60 adalah 2 × B. 0,20 adalah luas A, belum dibagi 0,5. 0,70 adalah 1 − B.",
      f_lorenzAB),
    Q("Angka harapan hidup sebuah provinsi adalah 72 tahun. Dengan rumus indeks kesehatan IPM = (AHH − 20) ÷ (85 − 20), nilai indeks kesehatan provinsi tersebut adalah …",
      ["0,80", "0,85", "0,72", "1,11", "0,65"],
      "Indeks kesehatan = (AHH − nilai minimum) ÷ (nilai maksimum − nilai minimum) = (72 − 20) ÷ (85 − 20) = 52 ÷ 65 = 0,80.\nIndeks ini menormalkan angka harapan hidup ke skala 0–1, dengan batas minimum 20 tahun dan maksimum 85 tahun sesuai metode UNDP. Indeks kesehatan kemudian digabungkan dengan indeks pendidikan dan pengeluaran melalui rata-rata geometrik untuk menghasilkan IPM.\n\nPengecoh: 0,85 membagi 72 dengan 85 tanpa mengurangi nilai minimum. 0,72 menganggap AHH langsung dibagi 100. 1,11 membagi 72 dengan 65. 0,65 adalah selisih batas maksimum dan minimum dibagi 100.",
      None),
    Q("Perhatikan grafik porsi pendapatan menurut desil penduduk Negara P berikut. Rasio Palma = porsi 10% teratas ÷ porsi 40% terbawah.\n\nRasio Palma Negara P adalah …",
      ["Sekitar 2,1", "Sekitar 0,5", "Sekitar 15", "Sekitar 1,5", "Sekitar 7,5"],
      "Porsi 10% teratas (D10) = 30%.\nPorsi 40% terbawah (D1–D4) = 2 + 3 + 4 + 5 = 14%.\nRasio Palma = 30 ÷ 14 ≈ 2,1.\nArtinya 10% penduduk terkaya menerima sekitar dua kali lipat pendapatan yang diterima 40% penduduk termiskin. Rasio Palma berfokus pada kedua ujung distribusi karena porsi kelompok menengah (D5–D9) cenderung stabil, sehingga perubahan ketimpangan lebih banyak terjadi di ujung atas dan bawah.\n\nPengecoh: 0,5 membalik pembagian. 15 membagi D10 dengan D1 (30 ÷ 2). 1,5 dan 7,5 berasal dari salah menjumlahkan desil (misalnya 30 ÷ 20 atau 30 ÷ 4).",
      f_desil),
    Q("Sebuah negara memiliki rasio tabungan (investasi) terhadap PDB 30% dan ICOR sebesar 6. Menurut model Harrod–Domar g = s ÷ ICOR, laju pertumbuhan ekonomi yang dapat dicapai adalah …",
      ["5%", "180%", "36%", "20%", "0,5%"],
      "Model Harrod–Domar: g = s ÷ ICOR = 30% ÷ 6 = 5% per tahun.\nICOR (incremental capital-output ratio) menunjukkan berapa unit tambahan modal yang diperlukan untuk menghasilkan satu unit tambahan output. ICOR 6 berarti investasi kurang efisien; bila ICOR turun menjadi 4 (investasi lebih produktif), dengan tabungan yang sama pertumbuhan dapat naik menjadi 7,5%. Model ini menekankan pentingnya tabungan, investasi, dan efisiensi investasi bagi pertumbuhan.\n\nPengecoh: 180% mengalikan s dengan ICOR. 36% menjumlahkan keduanya. 20% dan 0,5% berasal dari salah membagi.",
      None),
    Q("Perhatikan peta kategori IPM provinsi berikut.\n\nPola spasial pembangunan manusia yang paling tepat berdasarkan peta adalah …",
      ["IPM rendah–sedang terkonsentrasi di Indonesia timur", "IPM sangat tinggi tersebar merata di seluruh Indonesia timur",
       "Seluruh provinsi di Jawa memiliki IPM rendah", "IPM tidak memiliki pola spasial karena tersebar acak", "Papua memiliki IPM tertinggi di Indonesia"],
      "Peta menunjukkan provinsi dengan IPM sangat tinggi berada di DKI Jakarta, DI Yogyakarta, Kalimantan Timur, dan Kepulauan Riau, sedangkan IPM sedang dan rendah terkonsentrasi di Indonesia timur, terutama Papua (rendah), Papua Barat, NTT, NTB, Maluku Utara, Sulawesi Barat, dan Gorontalo. Pola ini mencerminkan ketimpangan pembangunan kawasan barat dan timur Indonesia akibat perbedaan aksesibilitas, infrastruktur pendidikan dan kesehatan, kondisi geografis kepulauan dan pegunungan, serta sejarah pembangunan yang berpusat di Jawa.\n\nPengecoh: IPM sangat tinggi tidak tersebar di timur. Provinsi di Jawa umumnya tinggi. Pola jelas tidak acak. Papua justru terendah.",
      f_ipmmap),
    Q("Dalam teori Rostow, tahap ketika tingkat investasi naik tajam (lebih dari 10% pendapatan nasional), muncul sektor industri pemimpin, dan pertumbuhan ekonomi berlangsung terus-menerus disebut tahap …",
      ["Lepas landas (take-off)", "Masyarakat tradisional", "Prasyarat lepas landas", "Menuju kedewasaan", "Konsumsi massa tinggi"],
      "Walt Rostow (1960) membagi pertumbuhan ekonomi menjadi lima tahap:\n1) Masyarakat tradisional: pertanian subsisten dan teknologi terbatas.\n2) Prasyarat lepas landas: mulai ada pendidikan, perbankan, infrastruktur, dan kewirausahaan.\n3) Lepas landas: investasi naik tajam, muncul sektor industri pemimpin (leading sectors), dan pertumbuhan menjadi berkelanjutan.\n4) Menuju kedewasaan: teknologi menyebar ke seluruh sektor ekonomi dan ekonomi makin beragam.\n5) Konsumsi massa tinggi: produksi barang konsumsi tahan lama dan jasa mendominasi.\nTeori ini dikritik karena menganggap semua negara mengikuti jalur linear yang sama seperti negara Barat dan mengabaikan faktor eksternal seperti kolonialisme.\n\nPengecoh: tahap lain tidak dicirikan lonjakan investasi dan munculnya sektor pemimpin.",
      None),
    Q("Perhatikan diagram hubungan pusat dan pinggiran berikut.\n\nAliran yang menurut Gunnar Myrdal disebut efek balik (backwash effect) dan cenderung memperlebar ketimpangan adalah …",
      ["X, aliran tenaga kerja terdidik, modal, dan bahan mentah ke pusat", "Y, penyebaran inovasi dan investasi ke wilayah pinggiran",
       "Y, karena aliran dari pusat selalu merugikan wilayah pinggiran", "X dan Y, karena keduanya sama-sama memperkecil ketimpangan",
       "Tidak ada, karena pusat dan pinggiran tidak saling berhubungan"],
      "Teori penyebab kumulatif Myrdal menjelaskan bahwa pertumbuhan di wilayah pusat menimbulkan dua efek:\n• Efek balik (backwash effect): wilayah pusat menarik tenaga kerja terdidik, modal, dan bahan mentah dari pinggiran (aliran X). Akibatnya pinggiran kehilangan sumber daya terbaiknya sehingga ketimpangan makin lebar.\n• Efek sebar (spread effect): pertumbuhan pusat meningkatkan permintaan produk pinggiran serta menyebarkan inovasi dan investasi ke pinggiran (aliran Y), sehingga ketimpangan dapat berkurang.\nMenurut Myrdal, tanpa intervensi pemerintah, efek balik biasanya lebih kuat sehingga ketimpangan cenderung bertambah (sebab-akibat kumulatif). Konsep serupa disebut polarisasi dan tetesan ke bawah oleh Hirschman.\n\nPengecoh: Y adalah efek sebar. Kedua aliran tidak sama-sama memperkecil ketimpangan. Pusat dan pinggiran jelas saling berhubungan.",
      f_corep),
    Q("Perhatikan diagram pencar pendapatan per kapita dan koefisien Gini beberapa negara berikut.\n\nInterpretasi yang paling sesuai dengan hipotesis Kuznets adalah …",
      ["Ketimpangan naik di tahap awal, memuncak, lalu turun", "Ketimpangan selalu turun sejak awal seiring kenaikan pendapatan",
       "Ketimpangan selalu naik tanpa batas seiring kenaikan pendapatan", "Negara A memiliki ketimpangan tertinggi karena pendapatannya terendah",
       "Pendapatan per kapita tidak berhubungan dengan ketimpangan"],
      "Grafik membentuk pola U terbalik: negara berpendapatan rendah (A, Gini ±0,33) relatif merata, ketimpangan meningkat pada negara berpendapatan menengah (B dan C, Gini ±0,42–0,46), lalu menurun pada negara berpendapatan tinggi (E dan F, Gini ±0,37 dan 0,30). Simon Kuznets menjelaskan bahwa pada awal industrialisasi, sebagian kecil penduduk di sektor modern menikmati pendapatan tinggi sementara sebagian besar masih di sektor tradisional, sehingga ketimpangan naik. Setelah tenaga kerja berpindah ke sektor modern dan kebijakan redistribusi berkembang, ketimpangan menurun.\nPerlu diingat bahwa banyak negara tidak mengikuti pola ini secara tepat; kebijakan pemerintah sangat berpengaruh.\n\nPengecoh: ketimpangan tidak selalu turun atau naik. Negara A justru relatif merata. Grafik menunjukkan ada hubungan.",
      f_kuznetsg),
]

P1 = [
    Q("Perhatikan indeks komponen IPM Kabupaten H berikut. IPM dihitung sebagai rata-rata geometrik ketiga indeks lalu dikalikan 100.\n\nIPM Kabupaten H adalah sekitar …",
      ["73,1", "73,3", "39,0", "80,0", "65,0"],
      "IPM = (I_kesehatan × I_pendidikan × I_pengeluaran)^(1/3) × 100\n= (0,80 × 0,65 × 0,75)^(1/3) × 100 = (0,39)^(1/3) × 100.\nKarena 0,73³ ≈ 0,389, akar pangkat tiga dari 0,39 ≈ 0,731, sehingga IPM ≈ 73,1 (kategori tinggi, 70–80).\nRata-rata geometrik dipakai agar capaian rendah di satu dimensi tidak dapat ditutupi sepenuhnya oleh capaian tinggi di dimensi lain.\n\nPengecoh: 73,3 adalah rata-rata aritmetika ((0,80 + 0,65 + 0,75) ÷ 3). 39,0 adalah hasil perkalian tanpa akar pangkat tiga. 80,0 dan 65,0 hanya memakai satu indeks.",
      f_ipmtab),
    Q("Sebuah kabupaten memiliki rata-rata lama sekolah (RLS) 9 tahun dan harapan lama sekolah (HLS) 13,5 tahun. Dengan indeks pendidikan = (RLS/15 + HLS/18) ÷ 2, nilai indeks pendidikannya adalah …",
      ["0,675", "0,600", "0,750", "1,350", "0,450"],
      "• Indeks RLS = 9 ÷ 15 = 0,60.\n• Indeks HLS = 13,5 ÷ 18 = 0,75.\n• Indeks pendidikan = (0,60 + 0,75) ÷ 2 = 0,675.\nRLS mengukur capaian pendidikan penduduk dewasa (25 tahun ke atas), sedangkan HLS mengukur peluang pendidikan anak usia 7 tahun di masa depan. Nilai maksimum yang dipakai adalah 15 tahun untuk RLS dan 18 tahun untuk HLS.\n\nPengecoh: 0,600 dan 0,750 hanya memakai salah satu komponen. 1,350 lupa membagi dua. 0,450 berasal dari salah perhitungan.",
      None),
    Q("Perhatikan data kemiskinan di beberapa provinsi berikut.\n\nPernyataan yang paling tepat untuk perencanaan program pengentasan kemiskinan adalah …",
      ["Persentase tertinggi di Papua, jumlah terbanyak di Jawa Timur", "Papua memiliki jumlah penduduk miskin terbanyak di Indonesia",
       "DKI Jakarta memiliki persentase kemiskinan tertinggi karena penduduknya padat", "Jawa Timur memiliki persentase kemiskinan tertinggi di antara provinsi tersebut",
       "Persentase dan jumlah penduduk miskin selalu menunjukkan urutan yang sama"],
      "Tabel menunjukkan Papua memiliki persentase penduduk miskin tertinggi (±26%) dan NTT (±19,5%), tetapi jumlah penduduk miskinnya relatif kecil (±0,9 dan ±1,1 juta) karena total penduduknya sedikit. Sebaliknya Jawa Timur dan Jawa Barat memiliki persentase lebih rendah (±9,8% dan ±7,6%), tetapi jumlah penduduk miskinnya terbanyak (±4,0 dan ±3,9 juta) karena penduduknya sangat banyak.\nImplikasinya, program pengentasan kemiskinan perlu mempertimbangkan keduanya: intensitas kemiskinan (persentase) menunjukkan wilayah yang paling tertinggal, sedangkan jumlah absolut menunjukkan besarnya sasaran program dan anggaran.\n\nPengecoh: jumlah penduduk miskin Papua bukan yang terbanyak. Jakarta memiliki persentase terendah. Jawa Timur tidak memiliki persentase tertinggi. Kedua ukuran tidak menghasilkan urutan yang sama.",
      f_miskin),
    Q("Indeks Kemiskinan Multidimensi (MPI) dihitung dengan MPI = H × A. Jika 30% penduduk tergolong miskin multidimensi (H = 0,30) dan rata-rata intensitas deprivasi mereka 45% (A = 0,45), nilai MPI adalah …",
      ["0,135", "0,75", "0,15", "1,35", "0,667"],
      "MPI = H × A = 0,30 × 0,45 = 0,135.\nH (headcount) adalah proporsi penduduk yang miskin multidimensi, sedangkan A (intensity) adalah rata-rata proporsi indikator yang tidak terpenuhi oleh penduduk miskin. Indikatornya mencakup tiga dimensi: kesehatan (gizi, kematian anak), pendidikan (lama sekolah, partisipasi sekolah), dan standar hidup (listrik, air minum, sanitasi, bahan bakar memasak, lantai rumah, aset).\nMPI melengkapi ukuran kemiskinan moneter karena menggambarkan kekurangan nonpendapatan.\n\nPengecoh: 0,75 menjumlahkan H dan A. 0,15 adalah selisih. 1,35 adalah kesalahan desimal. 0,667 membagi H dengan A.",
      None),
    Q("Perhatikan data pengeluaran lima rumah tangga berikut. Indeks kedalaman kemiskinan P1 = (1/n) Σ[(z − yᵢ)/z] untuk rumah tangga miskin (yᵢ < z).\n\nNilai P0 (persentase miskin) dan P1 adalah …",
      ["P0 = 60% dan P1 = 0,14", "P0 = 40% dan P1 = 0,14", "P0 = 60% dan P1 = 0,70", "P0 = 60% dan P1 = 0,23", "P0 = 80% dan P1 = 0,14"],
      "Garis kemiskinan z = 500. Rumah tangga dengan pengeluaran di bawah 500 adalah RT 1 (300), RT 2 (400), dan RT 3 (450). Jadi P0 = 3 ÷ 5 = 60%.\nKesenjangan relatif (z − y)/z:\n• RT 1: (500 − 300)/500 = 0,40.\n• RT 2: (500 − 400)/500 = 0,20.\n• RT 3: (500 − 450)/500 = 0,10.\nP1 = (0,40 + 0,20 + 0,10) ÷ 5 = 0,70 ÷ 5 = 0,14.\nP1 mengukur rata-rata jarak pengeluaran penduduk miskin terhadap garis kemiskinan; semakin besar, semakin dalam kemiskinannya.\n\nPengecoh: P0 40% dan 80% salah menghitung jumlah RT miskin. P1 0,70 lupa membagi dengan n. P1 0,23 membagi dengan jumlah RT miskin (3), padahal penyebutnya seluruh penduduk.",
      f_fgt),
    Q("PDB per kapita Negara A dalam dolar AS nominal lebih rendah daripada Negara B, tetapi dalam paritas daya beli (PPP) justru lebih tinggi. Penjelasan yang paling tepat adalah …",
      ["Harga di Negara A lebih murah sehingga daya beli riil lebih besar", "Negara A memiliki jumlah penduduk lebih banyak daripada Negara B",
       "PPP hanya menghitung ekspor dan impor kedua negara", "Nilai tukar mata uang Negara A selalu sama dengan dolar AS",
       "PDB nominal sudah memperhitungkan perbedaan harga antarnegara"],
      "PDB per kapita nominal mengonversi pendapatan ke dolar AS dengan kurs pasar, sehingga tidak memperhitungkan perbedaan tingkat harga antarnegara. Paritas daya beli (PPP) menyesuaikan pendapatan dengan harga barang dan jasa setempat. Bila harga di Negara A jauh lebih murah (misalnya makanan, transportasi, jasa), jumlah barang yang dapat dibeli dengan pendapatan yang sama menjadi lebih banyak. Itulah sebabnya PDB per kapita PPP negara berkembang biasanya jauh lebih tinggi daripada nilai nominalnya, dan perbandingan kesejahteraan antarnegara lebih tepat memakai PPP.\n\nPengecoh: jumlah penduduk sudah dimasukkan dalam nilai per kapita. PPP tidak hanya menghitung ekspor-impor. Kurs Negara A tidak sama dengan dolar. PDB nominal belum memperhitungkan perbedaan harga.",
      None),
    Q("Perhatikan diagram pencar IPM dan persentase penduduk miskin beberapa provinsi berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["IPM lebih tinggi cenderung disertai kemiskinan lebih rendah", "Provinsi dengan IPM lebih tinggi selalu memiliki penduduk miskin lebih banyak",
       "IPM dan kemiskinan tidak berhubungan sama sekali", "Provinsi A memiliki IPM tertinggi dan kemiskinan terendah",
       "Kenaikan IPM satu poin pasti menurunkan kemiskinan tepat satu persen"],
      "Titik-titik menunjukkan pola menurun: provinsi A (IPM ±62) memiliki penduduk miskin ±26%, sedangkan provinsi H (IPM ±82) hanya ±4%. Hubungan negatif ini menunjukkan bahwa pembangunan manusia (kesehatan, pendidikan, dan daya beli) berkaitan erat dengan rendahnya kemiskinan. Namun korelasi ini tidak membuktikan hubungan sebab-akibat langsung dan besarnya penurunan tidak tetap; penurunan kemiskinan per poin IPM lebih besar pada IPM rendah dan mengecil pada IPM tinggi (pola melengkung).\n\nPengecoh: hubungan bukan positif. Ada hubungan yang jelas. Provinsi A justru memiliki IPM terendah dan kemiskinan tertinggi. Besar penurunan tidak tetap satu persen per poin.",
      f_ipm_miskin),
    Q("Beberapa negara penghasil minyak di Timur Tengah memiliki GNI per kapita sangat tinggi, tetapi peringkat IPM-nya relatif lebih rendah daripada peringkat GNI-nya. Penjelasan yang paling tepat adalah …",
      ["Capaian pendidikan dan kesehatan belum sebanding pendapatan", "IPM hanya menghitung pendapatan sehingga seharusnya sama dengan GNI",
       "Negara tersebut tidak memiliki penduduk usia sekolah", "Harapan hidup di negara tersebut selalu di atas 85 tahun",
       "GNI per kapita tidak termasuk komponen IPM sama sekali"],
      "IPM menggabungkan tiga dimensi: kesehatan, pendidikan, dan standar hidup (pendapatan). Negara dengan pendapatan tinggi dari ekspor minyak dapat memiliki indeks pendapatan sangat tinggi, tetapi bila capaian pendidikan (misalnya rata-rata lama sekolah, terutama perempuan) dan kesehatan belum setinggi negara lain dengan pendapatan sejenis, nilai IPM-nya relatif lebih rendah. Selisih peringkat GNI dan IPM menunjukkan seberapa efektif kekayaan ekonomi diubah menjadi pembangunan manusia.\n\nPengecoh: IPM tidak hanya menghitung pendapatan. Negara tersebut memiliki penduduk usia sekolah. Harapan hidup di atas 85 tahun justru akan menaikkan IPM. GNI per kapita PPP adalah salah satu komponen IPM.",
      None),
    Q("Perhatikan grafik persentase penduduk miskin perkotaan dan perdesaan berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Kemiskinan desa selalu lebih tinggi, selisihnya menyempit", "Kemiskinan perkotaan selalu lebih tinggi daripada perdesaan",
       "Kemiskinan perdesaan naik terus sejak 2014", "Kemiskinan perkotaan dan perdesaan selalu sama besar",
       "Kemiskinan perkotaan turun sangat tajam pada 2020"],
      "Grafik menunjukkan persentase penduduk miskin perdesaan selalu lebih tinggi (±14,2% pada 2014 menjadi ±11,3% pada 2024) daripada perkotaan (±8,2% menjadi ±7,1%). Selisihnya menyempit dari ±6,0 poin (2014) menjadi ±4,2 poin (2024), karena kemiskinan perdesaan turun lebih cepat, antara lain berkat dana desa dan bantuan sosial. Pada 2020, kemiskinan perkotaan justru naik (dari ±6,9% menjadi ±7,9%) akibat pandemi COVID-19 yang memukul sektor informal dan jasa di kota.\n\nPengecoh: perkotaan tidak lebih tinggi. Kemiskinan perdesaan menurun, bukan naik. Keduanya tidak sama. Kemiskinan perkotaan pada 2020 justru naik.",
      f_kotadesa),
    Q("BPS menghitung garis kemiskinan dengan pendekatan kebutuhan dasar. Komponen garis kemiskinan tersebut adalah …",
      ["Garis kemiskinan makanan (2.100 kkal) ditambah nonmakanan",
       "Pendapatan 1 dolar AS per hari untuk setiap rumah tangga tanpa memperhatikan jumlah anggota",
       "Upah minimum provinsi dibagi jumlah anggota rumah tangga",
       "Nilai PDRB per kapita dibagi 12 bulan",
       "Kepemilikan kendaraan bermotor dan telepon pintar"],
      "BPS memakai pendekatan kebutuhan dasar (basic needs approach). Garis kemiskinan (GK) terdiri atas: (1) garis kemiskinan makanan, yaitu nilai pengeluaran untuk memenuhi kebutuhan minimum makanan setara 2.100 kilokalori per kapita per hari; dan (2) garis kemiskinan nonmakanan, yaitu kebutuhan minimum untuk perumahan, sandang, pendidikan, kesehatan, dan kebutuhan dasar lain. Penduduk dengan rata-rata pengeluaran per kapita per bulan di bawah GK digolongkan miskin. GK dihitung terpisah untuk perkotaan dan perdesaan di setiap provinsi karena tingkat harga berbeda.\n\nPengecoh: ukuran dolar per hari dipakai Bank Dunia untuk perbandingan internasional (dengan PPP), bukan dasar GK BPS. Upah minimum, PDRB per kapita, dan kepemilikan barang bukan dasar GK.",
      None),
]

P2 = [
    Q("Perhatikan distribusi pendapatan Negara G menurut kuintil berikut. Dengan Gini = 1 − Σ(Xₖ − Xₖ₋₁)(Yₖ + Yₖ₋₁), X dan Y kumulatif dalam desimal.\n\nKoefisien Gini Negara G adalah …",
      ["0,38", "0,62", "0,45", "0,40", "0,31"],
      "Persentase kumulatif penduduk (X): 0,2; 0,4; 0,6; 0,8; 1,0 (setiap selisih 0,2).\nPersentase kumulatif pendapatan (Y): 0,05; 0,15; 0,30; 0,55; 1,00.\nΣ(ΔX)(Yₖ + Yₖ₋₁) = 0,2 × [(0,05 + 0) + (0,15 + 0,05) + (0,30 + 0,15) + (0,55 + 0,30) + (1,00 + 0,55)]\n= 0,2 × (0,05 + 0,20 + 0,45 + 0,85 + 1,55) = 0,2 × 3,10 = 0,62.\nGini = 1 − 0,62 = 0,38 (ketimpangan sedang).\n\nPengecoh: 0,62 adalah hasil penjumlahan sebelum dikurangkan dari 1. 0,45 adalah porsi kuintil teratas. 0,40 dan 0,31 berasal dari salah menghitung kumulatif.",
      f_ginitab),
    Q("Di suatu negara, 20% penduduk terkaya menerima 45% pendapatan, sedangkan 20% penduduk termiskin menerima 5% pendapatan. Rasio S80/S20 negara tersebut adalah …",
      ["9", "0,11", "40", "2,25", "50"],
      "Rasio S80/S20 = porsi pendapatan 20% teratas ÷ porsi pendapatan 20% terbawah = 45 ÷ 5 = 9.\nArtinya 20% penduduk terkaya menerima pendapatan sembilan kali lipat 20% penduduk termiskin. Rasio kuintil ini mudah dipahami dan sering dipakai bersama koefisien Gini dan rasio Palma untuk menggambarkan ketimpangan.\n\nPengecoh: 0,11 membalik pembagian. 40 adalah selisih porsi. 2,25 dan 50 berasal dari pembagian atau perkalian yang keliru.",
      None),
    Q("Perhatikan grafik koefisien Gini pengeluaran Indonesia berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Naik pada 2000-an, memuncak 2011–2014, lalu sedikit turun", "Ketimpangan terus menurun sejak tahun 2000",
       "Ketimpangan tidak pernah berubah sejak tahun 2000", "Gini 0,41 menunjukkan ketimpangan sangat tinggi di atas 0,6",
       "Ketimpangan tertinggi terjadi pada tahun 2000"],
      "Grafik menunjukkan Gini pengeluaran Indonesia naik dari ±0,30 (2000) menjadi ±0,41 (2011–2014), lalu turun perlahan menjadi ±0,38–0,39 (2017–2023). Kenaikan pada 2000-an dikaitkan dengan ledakan harga komoditas yang lebih banyak dinikmati kelompok kaya dan wilayah tertentu, sedangkan penurunan setelah 2014 dikaitkan dengan program bantuan sosial, dana desa, dan pembangunan infrastruktur. Nilai Gini sekitar 0,38–0,41 tergolong ketimpangan sedang.\n\nPengecoh: ketimpangan tidak terus menurun dan jelas berubah. Gini 0,41 bukan di atas 0,6. Gini tahun 2000 justru terendah dalam grafik.",
      f_gini_id),
    Q("Indeks Williamson berbeda dari koefisien Gini dalam mengukur ketimpangan. Indeks Williamson lebih tepat dipakai untuk mengukur …",
      ["Ketimpangan PDRB per kapita antarwilayah", "Ketimpangan pendapatan antarindividu dalam satu rumah tangga",
       "Persentase penduduk yang hidup di bawah garis kemiskinan", "Kedalaman kemiskinan rumah tangga miskin", "Ketimpangan gender dalam pendidikan"],
      "Indeks Williamson (indeks ketimpangan regional) mengukur variasi PDRB per kapita antarwilayah (misalnya antarkabupaten dalam satu provinsi atau antarprovinsi dalam satu negara), yang ditimbang dengan porsi penduduk tiap wilayah, lalu dibagi rata-rata PDRB per kapita. Nilainya mendekati 0 berarti antarwilayah relatif merata; makin besar berarti makin timpang.\nKoefisien Gini umumnya mengukur ketimpangan pendapatan atau pengeluaran antarindividu atau rumah tangga.\n\nPengecoh: ketimpangan dalam rumah tangga tidak diukur Williamson. Persentase miskin adalah P0. Kedalaman kemiskinan adalah P1. Ketimpangan gender diukur dengan indeks lain seperti IKG.",
      None),
    Q("Perhatikan data dua wilayah dalam satu provinsi berikut. Indeks Williamson Iw = √[Σ(yᵢ − ȳ)² × fᵢ/n] ÷ ȳ, dengan ȳ adalah rata-rata tertimbang penduduk.\n\nNilai indeks Williamson provinsi tersebut adalah sekitar …",
      ["0,33", "0,50", "0,10", "3,00", "0,67"],
      "1) Rata-rata tertimbang: ȳ = (20 × 0,5) + (40 × 0,5) = 30 juta Rp.\n2) Σ(yᵢ − ȳ)² × fᵢ/n = (20 − 30)² × 0,5 + (40 − 30)² × 0,5 = 100 × 0,5 + 100 × 0,5 = 100.\n3) Akar = √100 = 10.\n4) Iw = 10 ÷ 30 ≈ 0,33.\nNilai 0,33 menunjukkan ketimpangan antarwilayah tingkat sedang. Bila PDRB per kapita wilayah A meningkat mendekati B, nilai Iw akan turun.\n\nPengecoh: 0,50 dan 0,67 berasal dari salah memilih penyebut (20 atau 15). 0,10 tidak membagi dengan rata-rata secara tepat. 3,00 membalik pembagian (30 ÷ 10).",
      f_will),
    Q("Rasio Palma sering dianggap lebih mudah dipahami daripada koefisien Gini. Kelebihan utama rasio Palma adalah …",
      ["Langsung menunjukkan perbandingan porsi kelompok terkaya dan termiskin", "Selalu bernilai antara 0 dan 1 seperti koefisien Gini",
       "Menghitung seluruh kelompok pendapatan secara rinci tanpa pengecualian", "Mengukur ketimpangan antarwilayah, bukan antarpenduduk",
       "Tidak memerlukan data pendapatan atau pengeluaran sama sekali"],
      "Rasio Palma membandingkan porsi pendapatan 10% penduduk terkaya dengan 40% penduduk termiskin. Gabriel Palma menemukan bahwa porsi kelompok menengah (desil 5–9) relatif stabil di banyak negara, sekitar setengah pendapatan nasional, sehingga perbedaan ketimpangan antarnegara terutama berasal dari kedua ujung distribusi. Rasio ini mudah dipahami (misalnya \"10% terkaya menerima dua kali pendapatan 40% termiskin\") dan peka terhadap perubahan di kedua ujung.\n\nPengecoh: rasio Palma tidak dibatasi 0–1; nilainya bisa lebih dari 1. Palma justru tidak memakai kelompok menengah. Palma mengukur ketimpangan antarpenduduk, bukan antarwilayah. Palma tetap memerlukan data pendapatan atau pengeluaran.",
      None),
    Q("Perhatikan grafik PDRB per kapita beberapa provinsi berikut.\n\nPenjelasan yang paling tepat untuk tingginya PDRB per kapita Kalimantan Timur dan Riau adalah …",
      ["Sektor tambang dan migas besar, penduduk relatif sedikit", "Jumlah penduduk kedua provinsi adalah yang terbanyak di Indonesia",
       "Kedua provinsi memiliki sektor pertanian padi terbesar di Indonesia", "PDRB per kapita tinggi berarti tidak ada penduduk miskin di kedua provinsi",
       "Kedua provinsi adalah pusat pemerintahan nasional"],
      "Kalimantan Timur (batu bara, migas) dan Riau (minyak bumi, kelapa sawit) memiliki PDRB besar dari sektor pertambangan dan perkebunan, sementara jumlah penduduknya relatif kecil dibandingkan provinsi di Jawa. Akibatnya PDRB per kapita sangat tinggi. Namun PDRB per kapita tidak selalu mencerminkan kesejahteraan penduduk karena sebagian nilai tambah dimiliki perusahaan dari luar daerah atau luar negeri, bersifat padat modal, dan sebagian keuntungan mengalir keluar. Kemiskinan tetap ada di kedua provinsi.\n\nPengecoh: penduduk terbanyak berada di Jawa. Sektor padi terbesar bukan di kedua provinsi. PDRB per kapita tinggi tidak menjamin tidak ada kemiskinan. Pusat pemerintahan nasional adalah Jakarta (dan kelak IKN).",
      f_pdrbkap),
    Q("Hubungan Gini dan PDB per kapita (x, dalam ribu USD) di suatu kawasan dimodelkan G = 0,20 + 0,08x − 0,004x². Menurut model Kuznets kuadrat tersebut, ketimpangan mencapai puncak pada PDB per kapita sebesar …",
      ["10 ribu USD", "20 ribu USD", "5 ribu USD", "40 ribu USD", "0,4 ribu USD"],
      "Fungsi kuadrat G = a + bx − cx² mencapai puncak pada x* = b ÷ (2c).\nx* = 0,08 ÷ (2 × 0,004) = 0,08 ÷ 0,008 = 10 ribu USD.\nGini puncak = 0,20 + 0,08 × 10 − 0,004 × 100 = 0,20 + 0,80 − 0,40 = 0,60.\nSebelum PDB per kapita 10 ribu USD, ketimpangan cenderung naik; setelahnya cenderung turun, sesuai hipotesis U terbalik Kuznets.\n\nPengecoh: 20 ribu USD adalah b ÷ c (lupa membagi 2). 5 ribu USD membagi dengan 4c. 40 ribu USD dan 0,4 ribu USD berasal dari kesalahan aljabar.",
      None),
    Q("Perhatikan grafik porsi penduduk dan porsi PDB menurut wilayah berikut.\n\nWilayah dengan PDB per kapita relatif paling rendah dibandingkan rata-rata nasional adalah …",
      ["Bali–Nusa Tenggara", "Kalimantan", "Jawa", "Sumatra", "Maluku–Papua"],
      "PDB per kapita relatif suatu wilayah dapat dilihat dari perbandingan porsi PDB dengan porsi penduduk:\n• Sumatra: 22 ÷ 22 = 1,0.\n• Jawa: 57 ÷ 56 ≈ 1,02.\n• Kalimantan: 8 ÷ 6 ≈ 1,33 (di atas rata-rata, karena tambang dan perkebunan).\n• Sulawesi: 7 ÷ 7 = 1,0.\n• Bali–Nusa Tenggara: 3 ÷ 6 = 0,5 (paling rendah).\n• Maluku–Papua: 3 ÷ 3 = 1,0.\nBali–Nusa Tenggara memiliki porsi penduduk dua kali porsi PDB, sehingga PDB per kapitanya sekitar separuh rata-rata nasional, terutama karena NTB dan NTT memiliki ekonomi yang didominasi pertanian lahan kering.\n\nPengecoh: Kalimantan justru di atas rata-rata. Jawa, Sumatra, dan Maluku–Papua sekitar rata-rata pada data ilustrasi ini.",
      f_porsiwil),
    Q("Koefisien Gini suatu provinsi adalah 0,52. Kategori ketimpangan provinsi tersebut adalah …",
      ["Ketimpangan tinggi", "Ketimpangan rendah", "Ketimpangan sedang", "Pemerataan sempurna", "Ketimpangan mutlak"],
      "Koefisien Gini bernilai 0 (pemerataan sempurna, semua penduduk menerima pendapatan sama) hingga 1 (ketimpangan mutlak, satu orang menerima seluruh pendapatan). Klasifikasi yang umum dipakai: Gini < 0,3 ketimpangan rendah; 0,3–0,5 ketimpangan sedang; > 0,5 ketimpangan tinggi.\nNilai 0,52 berada di atas 0,5 sehingga tergolong ketimpangan tinggi. Sebagai pembanding, Gini pengeluaran Indonesia sekitar 0,38–0,39 (sedang), sedangkan beberapa negara di Afrika bagian selatan dan Amerika Latin memiliki Gini pendapatan di atas 0,5.\n\nPengecoh: 0,52 bukan rendah atau sedang. Pemerataan sempurna bernilai 0, dan ketimpangan mutlak bernilai 1.",
      None),
]

P3 = [
    Q("Perhatikan diagram tahap-tahap pertumbuhan ekonomi Rostow berikut.\n\nTahap ketika teknologi modern telah menyebar ke hampir semua sektor ekonomi dan ekonomi makin beragam ditunjukkan oleh nomor …",
      ["4", "1", "2", "3", "5"],
      "Tahapan Rostow pada diagram:\n1) Masyarakat tradisional: pertanian subsisten, teknologi terbatas.\n2) Prasyarat lepas landas: mulai terbentuk pendidikan, perbankan, infrastruktur, dan wirausaha.\n3) Lepas landas: investasi meningkat tajam dan muncul sektor industri pemimpin.\n4) Menuju kedewasaan: teknologi modern menyebar ke seluruh sektor ekonomi, ekonomi makin beragam, dan ketergantungan pada satu sektor berkurang.\n5) Konsumsi massa tinggi: ekonomi didominasi produksi barang konsumsi tahan lama dan jasa, serta pendapatan tinggi.\nCiri pada soal sesuai dengan tahap 4.\n\nPengecoh: tahap 3 masih bertumpu pada beberapa sektor pemimpin. Tahap 5 dicirikan konsumsi massal. Tahap 1 dan 2 belum memiliki teknologi modern yang menyebar.",
      f_rostow),
    Q("Teori ketergantungan (dependency theory) menjelaskan keterbelakangan negara berkembang terutama karena …",
      ["Hubungan ekonomi timpang dengan negara maju sejak kolonial", "Negara berkembang tidak memiliki sumber daya alam sama sekali",
       "Penduduk negara berkembang malas bekerja", "Iklim tropis selalu menghambat pertumbuhan ekonomi", "Negara berkembang terlalu cepat melakukan industrialisasi"],
      "Teori ketergantungan (misalnya Andre Gunder Frank dan Raúl Prebisch) berpendapat bahwa keterbelakangan negara berkembang bukan karena faktor internal semata, melainkan akibat posisi mereka dalam sistem ekonomi global. Sejak masa kolonial, negara berkembang ditempatkan sebagai pemasok bahan mentah murah dan pasar barang jadi dari negara maju. Nilai tukar perdagangan yang memburuk, aliran keuntungan ke negara maju, dan dominasi perusahaan asing membuat negara berkembang terus bergantung. Solusi yang diusulkan antara lain industrialisasi substitusi impor dan penguatan kemandirian ekonomi.\n\nPengecoh: negara berkembang justru kaya sumber daya alam. Penjelasan berbasis stereotip seperti \"malas\" tidak ilmiah. Determinisme iklim telah lama ditolak. Teori ini justru mendorong industrialisasi mandiri.",
      None),
    Q("Perhatikan peta pengelompokan negara menurut teori sistem dunia Wallerstein berikut.\n\nIndonesia, Brasil, dan Tiongkok tergolong kelompok …",
      ["L, semi-pinggiran", "K, inti (core)", "M, pinggiran (periphery)", "K dan M sekaligus", "Tidak termasuk kelompok mana pun"],
      "Immanuel Wallerstein membagi negara dalam sistem ekonomi dunia menjadi:\n• Inti (core) – kelompok K: negara maju berteknologi tinggi yang menguasai modal, industri bernilai tambah tinggi, dan keuangan, misalnya Amerika Serikat, Eropa Barat, dan Jepang.\n• Semi-pinggiran (semi-periphery) – kelompok L: negara dengan ciri campuran, sudah memiliki industri dan menjadi pusat bagi negara di sekitarnya, tetapi masih bergantung pada negara inti, misalnya Tiongkok, India, Brasil, Meksiko, dan Indonesia.\n• Pinggiran (periphery) – kelompok M: negara yang terutama memasok bahan mentah dan tenaga kerja murah.\nPosisi negara dapat berubah; Korea Selatan, misalnya, bergerak dari semi-pinggiran menjadi inti.\n\nPengecoh: Indonesia, Brasil, dan Tiongkok berwarna biru muda (L), bukan K atau M.",
      f_sistemdunia),
    Q("Amartya Sen memandang pembangunan sebagai \"kebebasan\" (development as freedom). Inti pendekatan kapabilitas tersebut adalah …",
      ["Memperluas kemampuan dan pilihan nyata setiap orang", "Memaksimalkan PDB tanpa memperhatikan kesejahteraan manusia",
       "Mengurangi jumlah penduduk agar pendapatan per kapita naik", "Mengutamakan pembangunan fisik gedung tinggi di kota besar",
       "Menyerahkan seluruh pembangunan kepada mekanisme pasar bebas"],
      "Amartya Sen berpendapat bahwa pembangunan bukan sekadar pertumbuhan pendapatan, tetapi perluasan kapabilitas, yaitu kemampuan nyata seseorang untuk melakukan dan menjadi sesuatu yang mereka hargai, seperti hidup sehat, berpendidikan, berpartisipasi dalam masyarakat, dan bebas dari diskriminasi. Pendapatan hanyalah salah satu sarana. Gagasan ini menjadi dasar konsep pembangunan manusia dan Indeks Pembangunan Manusia (IPM) yang dikembangkan UNDP bersama Mahbub ul Haq.\n\nPengecoh: memaksimalkan PDB tanpa kesejahteraan bertentangan dengan pendekatan Sen. Mengurangi penduduk, mengutamakan gedung tinggi, atau menyerahkan sepenuhnya pada pasar bukan inti pendekatan kapabilitas.",
      None),
    Q("Perhatikan diagram hierarki tempat sentral Christaller berikut.\n\nLayanan yang paling sesuai berada di pusat orde tinggi (K) adalah …",
      ["Rumah sakit rujukan dan universitas", "Warung kebutuhan sehari-hari", "Sekolah dasar di setiap desa",
       "Pos pelayanan terpadu (posyandu)", "Kios pulsa dan bahan bakar eceran"],
      "Teori tempat sentral Christaller menyatakan bahwa pusat permukiman membentuk hierarki. Pusat orde rendah (M) jumlahnya banyak, berjarak dekat, dan menyediakan barang atau jasa yang sering dibutuhkan dengan ambang penduduk kecil, misalnya warung, SD, dan posyandu. Pusat orde tinggi (K) jumlahnya sedikit, melayani wilayah luas, dan menyediakan layanan khusus yang jarang dibutuhkan tetapi memerlukan ambang penduduk besar, misalnya rumah sakit rujukan dengan dokter spesialis, universitas, pusat perbelanjaan besar, dan kantor pemerintahan tingkat tinggi. Pusat orde tinggi juga menyediakan semua layanan orde di bawahnya.\n\nPengecoh: opsi lain adalah layanan orde rendah dengan ambang kecil dan jangkauan pendek.",
      f_christaller),
    Q("Menurut teori penyebab kumulatif Myrdal, tanpa campur tangan pemerintah ketimpangan antara wilayah maju dan tertinggal cenderung …",
      ["Makin lebar karena efek balik lebih kuat daripada efek sebar", "Menghilang dengan sendirinya dalam waktu singkat",
       "Tidak berubah karena kedua wilayah tidak saling memengaruhi", "Berbalik sehingga wilayah tertinggal menjadi lebih maju",
       "Bergantung sepenuhnya pada jumlah curah hujan"],
      "Gunnar Myrdal menyatakan bahwa keunggulan awal suatu wilayah akan menarik modal, tenaga kerja terampil, dan kegiatan ekonomi, sehingga wilayah itu makin maju (sebab-akibat kumulatif yang melingkar). Sebaliknya wilayah tertinggal kehilangan sumber daya terbaiknya (efek balik/backwash). Walaupun ada efek sebar (spread) berupa permintaan dan inovasi yang mengalir ke pinggiran, dalam mekanisme pasar bebas efek balik biasanya lebih kuat, sehingga ketimpangan makin lebar. Karena itu Myrdal mendorong intervensi pemerintah, seperti investasi infrastruktur, pendidikan, dan insentif di wilayah tertinggal.\n\nPengecoh: ketimpangan tidak hilang dengan sendirinya. Kedua wilayah saling memengaruhi. Pembalikan tidak terjadi otomatis. Curah hujan bukan faktor dalam teori ini.",
      None),
    Q("Perhatikan diagram ambang dan jangkauan dua jenis layanan berikut.\n\nPernyataan yang paling tepat berdasarkan teori tempat sentral adalah …",
      ["Layanan P layak berdiri karena jangkauannya lebih luas daripada ambangnya", "Layanan Q layak berdiri karena ambangnya lebih luas daripada jangkauannya",
       "Kedua layanan tidak layak karena berada di pusat yang sama", "Layanan P tidak layak karena jangkauannya terlalu luas",
       "Ambang dan jangkauan tidak memengaruhi kelayakan suatu layanan"],
      "Ambang (threshold) adalah jumlah penduduk minimum yang diperlukan agar suatu layanan dapat bertahan, digambarkan sebagai lingkaran wilayah yang memuat penduduk sebanyak itu. Jangkauan (range) adalah jarak maksimum yang bersedia ditempuh konsumen untuk memperoleh layanan tersebut.\nSuatu layanan layak berdiri bila jangkauannya lebih luas daripada ambangnya, karena konsumen yang terjangkau cukup banyak. Pada Layanan P, lingkaran jangkauan (hijau) lebih besar daripada ambang (merah) → layak. Pada Layanan Q, ambang lebih luas daripada jangkauan → pelanggan yang terjangkau tidak cukup sehingga layanan tidak layak, kecuali bersifat keliling atau periodik (misalnya pasar mingguan).\n\nPengecoh: opsi lain membalik konsep ambang dan jangkauan atau mengabaikannya.",
      f_ambang),
    Q("Albert Hirschman memperkenalkan istilah trickling-down effect dan polarization effect. Yang dimaksud trickling-down effect adalah …",
      ["Manfaat pertumbuhan wilayah maju menetes ke wilayah tertinggal", "Wilayah tertinggal menyerap seluruh tenaga kerja dari wilayah maju",
       "Ketimpangan makin besar karena modal mengalir ke wilayah maju", "Pemerintah menghapus seluruh investasi di wilayah maju", "Hujan dari wilayah maju mengalir ke wilayah tertinggal"],
      "Hirschman (1958) mengemukakan bahwa pertumbuhan tidak terjadi merata, tetapi berawal di beberapa pusat (pertumbuhan tidak seimbang). Dari pusat tersebut muncul dua efek:\n• Efek tetesan ke bawah (trickling-down): pertumbuhan di wilayah maju meningkatkan permintaan terhadap produk wilayah tertinggal, menyerap tenaga kerja, dan mendorong investasi ke wilayah tertinggal, sehingga manfaat pertumbuhan menyebar.\n• Efek polarisasi (polarization): wilayah maju menarik modal dan tenaga kerja terbaik dari wilayah tertinggal sehingga ketimpangan bertambah.\nHirschman lebih optimis daripada Myrdal: dalam jangka panjang efek tetesan dapat lebih kuat, terutama bila didukung kebijakan.\n\nPengecoh: opsi ketiga adalah efek polarisasi. Opsi lain tidak sesuai konsep.",
      None),
    Q("Perhatikan diagram tipologi Klassen kabupaten di Provinsi K berikut.\n\nKabupaten yang tergolong \"daerah berkembang cepat\" (pertumbuhan tinggi tetapi PDRB per kapita rendah) adalah …",
      ["C", "B", "A", "D", "E"],
      "Tipologi Klassen membagi daerah menjadi empat kuadran berdasarkan laju pertumbuhan dan PDRB per kapita dibandingkan rata-rata provinsi:\n• Kuadran I (pertumbuhan tinggi, per kapita tinggi): daerah maju dan tumbuh cepat → B dan E.\n• Kuadran II (pertumbuhan rendah, per kapita tinggi): daerah maju tetapi tertekan → A.\n• Kuadran III (pertumbuhan tinggi, per kapita rendah): daerah berkembang cepat → C.\n• Kuadran IV (pertumbuhan rendah, per kapita rendah): daerah relatif tertinggal → D.\nHanya kabupaten C yang berada di kuadran III.\n\nPengecoh: B dan E maju serta tumbuh cepat. A maju tetapi tertekan. D tertinggal.",
      f_klassen),
    Q("Teori modernisasi dikritik oleh banyak ahli geografi pembangunan. Kritik utama terhadap teori tersebut adalah …",
      ["Menganggap semua negara harus meniru jalur Barat", "Terlalu memperhatikan sejarah kolonial negara berkembang",
       "Menolak peran investasi dan industrialisasi dalam pembangunan", "Hanya berlaku untuk negara di kawasan kutub", "Menganggap pertanian tradisional sebagai tahap akhir pembangunan"],
      "Teori modernisasi (misalnya Rostow) memandang pembangunan sebagai proses linear dari masyarakat tradisional menuju masyarakat modern seperti negara Barat, dengan menekankan faktor internal seperti nilai budaya, tabungan, investasi, dan teknologi. Kritik utamanya: (1) bersifat Eurosentris karena menganggap jalur Barat sebagai satu-satunya model; (2) mengabaikan faktor eksternal seperti kolonialisme, perdagangan yang timpang, dan dominasi negara maju; (3) kurang memperhatikan ketimpangan dan keberlanjutan lingkungan; serta (4) menganggap budaya tradisional sebagai penghambat.\n\nPengecoh: teori modernisasi justru kurang memperhatikan sejarah kolonial. Teori ini mendukung investasi dan industrialisasi. Teori ini tidak terbatas pada kawasan kutub. Pertanian tradisional dianggap tahap awal, bukan akhir.",
      None),
]

P4 = [
    Q("Perhatikan grafik GNI per kapita menurut kawasan berikut.\n\nGNI per kapita Amerika Utara kira-kira … kali Afrika Sub-Sahara.",
      ["44", "73", "4,4", "0,02", "22"],
      "Rasio = 75.000 ÷ 1.700 ≈ 44 kali.\nKesenjangan yang sangat besar ini menggambarkan ketimpangan spasial global antara negara maju di belahan Bumi utara dan negara berkembang di belahan selatan (sering digambarkan dengan Garis Brandt). Faktor penyebabnya antara lain sejarah kolonialisme, perbedaan modal dan teknologi, kualitas institusi, konflik, kondisi geografis seperti akses laut dan penyakit tropis, serta posisi dalam perdagangan global.\n\nPengecoh: 73 adalah selisih dalam ribuan (75 − 1,7 dibulatkan). 4,4 adalah kesalahan desimal. 0,02 membalik pembagian. 22 membandingkan Amerika Utara dengan Eropa atau membagi dua secara keliru.",
      f_gniregion),
    Q("Garis Brandt yang dikemukakan pada 1980 membagi dunia menjadi …",
      ["Utara yang relatif kaya dan Selatan yang relatif miskin", "Timur yang komunis dan Barat yang kapitalis", "Belahan Bumi bertekanan tinggi dan rendah",
       "Negara beriklim tropis dan beriklim sedang secara tepat", "Negara berpenduduk banyak dan sedikit"],
      "Garis Brandt diperkenalkan dalam Laporan Brandt (Komisi Independen Masalah Pembangunan Internasional yang dipimpin Willy Brandt, 1980). Garis ini memisahkan negara-negara Utara yang relatif kaya (Amerika Utara, Eropa, Rusia, Jepang, serta Australia dan Selandia Baru yang dimasukkan ke Utara meski berada di selatan) dari negara-negara Selatan yang relatif miskin (sebagian besar Amerika Latin, Afrika, dan Asia). Laporan tersebut menyerukan kerja sama Utara–Selatan untuk mengurangi kesenjangan.\nSaat ini garis tersebut dianggap terlalu menyederhanakan karena banyak negara Selatan, seperti Korea Selatan, Singapura, dan negara Teluk, telah berpendapatan tinggi.\n\nPengecoh: pembagian Timur–Barat merujuk pada Perang Dingin. Garis Brandt tidak membagi berdasarkan tekanan udara, iklim secara tepat, atau jumlah penduduk.",
      None),
    Q("Perhatikan grafik IPM DKI Jakarta dan Papua berikut.\n\nPernyataan yang paling tepat adalah …",
      ["IPM Papua naik lebih cepat sehingga selisih menyempit", "IPM Papua turun sejak 2010 sehingga selisih makin lebar",
       "Selisih IPM keduanya tetap sama persis setiap tahun", "IPM Papua sudah melampaui DKI Jakarta pada 2024", "IPM DKI Jakarta menurun sejak 2016"],
      "Grafik menunjukkan IPM DKI Jakarta naik dari ±76,3 (2010) menjadi ±83,0 (2024), naik ±6,7 poin. IPM Papua naik dari ±54,5 menjadi ±63,0, naik ±8,5 poin. Karena kenaikan Papua lebih besar, selisih IPM menyempit dari ±21,8 poin menjadi ±20,0 poin. Namun kesenjangan tetap sangat besar, menunjukkan perlunya percepatan pembangunan pendidikan, kesehatan, dan ekonomi di Papua.\n\nPengecoh: IPM Papua tidak turun. Selisihnya tidak tetap. Papua belum melampaui Jakarta. IPM Jakarta terus naik.",
      f_ipmgap),
    Q("Kementerian Desa mengklasifikasikan desa berdasarkan Indeks Desa Membangun (IDM). Urutan status desa dari yang paling maju adalah …",
      ["Mandiri → maju → berkembang → tertinggal → sangat tertinggal", "Sangat tertinggal → tertinggal → berkembang → maju → mandiri",
       "Maju → mandiri → berkembang → sangat tertinggal → tertinggal", "Berkembang → mandiri → maju → tertinggal → sangat tertinggal",
       "Tertinggal → berkembang → sangat tertinggal → maju → mandiri"],
      "Indeks Desa Membangun (IDM) disusun dari tiga indeks: ketahanan sosial, ketahanan ekonomi, dan ketahanan ekologi/lingkungan. Berdasarkan nilainya, desa diklasifikasikan menjadi lima status, dari yang paling maju: desa mandiri, desa maju, desa berkembang, desa tertinggal, dan desa sangat tertinggal. Status ini dipakai untuk menentukan prioritas pembangunan desa dan penggunaan dana desa.\n\nPengecoh: opsi kedua adalah urutan dari yang paling tertinggal (terbalik dengan yang ditanyakan). Opsi lain mengacak urutannya.",
      None),
    Q("Perhatikan peta sebaran kabupaten daerah tertinggal berikut.\n\nFaktor geografis yang paling menjelaskan konsentrasi daerah tertinggal di Papua dan Nusa Tenggara Timur adalah …",
      ["Aksesibilitas rendah akibat pegunungan dan kepulauan", "Kepadatan penduduk yang sangat tinggi seperti di Jawa",
       "Lokasi yang terlalu dekat dengan pusat pemerintahan nasional", "Curah hujan merata sepanjang tahun yang terlalu tinggi di NTT",
       "Tidak adanya garis pantai di kedua provinsi tersebut"],
      "Peta menunjukkan konsentrasi kabupaten tertinggal di Papua, Papua Barat, NTT, dan Maluku. Faktor geografisnya antara lain: (1) aksesibilitas rendah karena medan pegunungan terjal di Papua dan wilayah kepulauan yang tersebar di NTT dan Maluku, sehingga biaya transportasi dan logistik sangat tinggi; (2) NTT beriklim semi-kering dengan musim kemarau panjang dan lahan kering yang kurang subur; (3) keterbatasan infrastruktur dasar seperti jalan, listrik, air bersih, sekolah, dan fasilitas kesehatan; serta (4) jarak yang jauh dari pusat pertumbuhan ekonomi nasional di Jawa.\n\nPengecoh: kepadatan penduduk di kedua wilayah justru rendah. Keduanya jauh dari pusat pemerintahan. NTT justru kering, bukan hujan merata. Kedua provinsi memiliki garis pantai panjang.",
      f_tertinggal),
    Q("Ketimpangan antara Kawasan Barat Indonesia (KBI) dan Kawasan Timur Indonesia (KTI) sudah berlangsung lama. Penyebab historis yang paling tepat adalah …",
      ["Pembangunan sejak masa kolonial terpusat di Jawa", "KTI tidak memiliki sumber daya alam sama sekali",
       "Penduduk KTI tidak pernah bermigrasi ke wilayah lain", "KTI selalu menjadi pusat industri nasional sejak abad ke-19",
       "KBI tidak memiliki pelabuhan sehingga perdagangan berpusat di KTI"],
      "Sejak masa kolonial, pembangunan infrastruktur (jalan, rel kereta, pelabuhan, irigasi), perkebunan, pendidikan, dan pemerintahan dipusatkan di Jawa dan sebagian Sumatra. Setelah kemerdekaan, industrialisasi juga berkembang terutama di Jawa karena pasar, tenaga kerja, dan infrastruktur sudah tersedia (efek kumulatif). Akibatnya KTI tertinggal walaupun kaya sumber daya alam seperti tambang, hutan, dan perikanan. Kebijakan seperti percepatan pembangunan KTI, otonomi khusus Papua, tol laut, dan KEK di luar Jawa ditujukan untuk mengurangi ketimpangan ini.\n\nPengecoh: KTI kaya sumber daya alam. Penduduk KTI juga bermigrasi. KTI bukan pusat industri nasional. KBI memiliki banyak pelabuhan besar.",
      None),
    Q("Perhatikan diagram pencar kerapatan jalan dan persentase penduduk miskin beberapa kabupaten berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Jalan lebih rapat cenderung disertai kemiskinan lebih rendah", "Kerapatan jalan yang tinggi selalu menyebabkan kemiskinan meningkat",
       "Tidak ada hubungan antara kerapatan jalan dan kemiskinan", "Kabupaten A memiliki jaringan jalan paling rapat",
       "Setiap penambahan jalan 0,1 km/km² pasti menurunkan kemiskinan tepat 5%"],
      "Titik-titik menunjukkan pola menurun: kabupaten A dengan kerapatan jalan ±0,08 km/km² memiliki penduduk miskin ±28%, sedangkan kabupaten G dengan ±1,6 km/km² hanya ±5%. Jalan meningkatkan aksesibilitas ke pasar, sekolah, dan fasilitas kesehatan, menurunkan biaya transportasi, dan membuka peluang usaha, sehingga berkaitan dengan kemiskinan yang lebih rendah. Penurunan kemiskinan paling besar terjadi pada tambahan jalan di wilayah yang awalnya sangat minim jalan.\nNamun hubungan ini korelasional; faktor lain seperti pendidikan dan kesuburan lahan juga berpengaruh.\n\nPengecoh: arah hubungan bukan positif. Hubungan jelas ada. Kabupaten A justru paling jarang jalannya. Penurunan kemiskinan tidak tetap sebesar 5% per 0,1 km/km².",
      f_jalan),
    Q("Program BBM Satu Harga yang membuat harga bensin di Papua sama dengan di Jawa paling tepat dipandang sebagai kebijakan untuk …",
      ["Mengurangi ketimpangan biaya hidup di wilayah terpencil", "Menaikkan harga BBM di Pulau Jawa agar sama dengan Papua",
       "Menghentikan penggunaan BBM di wilayah terpencil", "Mengurangi jumlah penduduk di Papua", "Menghapus subsidi energi di seluruh Indonesia"],
      "Sebelum program BBM Satu Harga (sejak 2016), harga bensin di daerah pegunungan Papua dapat mencapai puluhan ribu rupiah per liter karena BBM harus diangkut dengan pesawat atau kapal kecil. Harga BBM yang tinggi menaikkan biaya transportasi dan harga barang lain, sehingga memperbesar ketimpangan biaya hidup. Program ini menyubsidi biaya distribusi agar harga di wilayah 3T sama dengan harga nasional, sehingga mengurangi ketimpangan spasial dan meningkatkan keadilan akses energi.\nKritiknya, biaya program tinggi dan pasokan di beberapa lokasi belum selalu stabil.\n\nPengecoh: harga di Jawa tidak dinaikkan. BBM tetap dipakai. Program tidak berkaitan dengan jumlah penduduk. Program justru memerlukan subsidi.",
      None),
    Q("Perhatikan grafik koefisien Gini perkotaan dan perdesaan berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Ketimpangan di perkotaan selalu lebih tinggi daripada di perdesaan", "Ketimpangan di perdesaan selalu lebih tinggi daripada di perkotaan",
       "Ketimpangan perkotaan dan perdesaan sama besar setiap tahun", "Gini perdesaan naik tajam setelah 2019", "Gini perkotaan turun terus tanpa pernah naik"],
      "Grafik menunjukkan Gini perkotaan (±0,39–0,43) selalu lebih tinggi daripada Gini perdesaan (±0,31–0,33). Di perkotaan, variasi pendapatan sangat lebar: ada pekerja berpenghasilan sangat tinggi di sektor keuangan, teknologi, dan profesional, sekaligus pekerja informal berpenghasilan rendah. Di perdesaan, sebagian besar penduduk bekerja di sektor pertanian dengan pendapatan yang relatif mirip, sehingga ketimpangannya lebih rendah.\nGini perkotaan sempat turun hingga 2019, lalu naik kembali pada 2021–2023, antara lain akibat dampak pandemi.\n\nPengecoh: perdesaan tidak lebih timpang. Keduanya tidak sama. Gini perdesaan justru turun perlahan. Gini perkotaan naik kembali setelah 2019.",
      f_ginikd),
    Q("Dana desa yang disalurkan pemerintah pusat sejak 2015 terutama ditujukan untuk …",
      ["Membangun infrastruktur dan memberdayakan ekonomi desa", "Membiayai pembangunan gedung pencakar langit di ibu kota provinsi",
       "Menggantikan seluruh gaji pegawai negeri di kabupaten", "Membeli lahan pertanian desa untuk dijadikan kawasan industri asing", "Membayar utang luar negeri pemerintah pusat"],
      "Dana desa adalah dana APBN yang ditransfer langsung ke desa berdasarkan UU No. 6 Tahun 2014 tentang Desa. Prioritas penggunaannya antara lain pembangunan infrastruktur dasar desa (jalan desa, jembatan, irigasi, air bersih, sanitasi), pemberdayaan ekonomi seperti BUMDes dan padat karya tunai, peningkatan layanan dasar (posyandu, PAUD), serta penanganan kemiskinan dan stunting. Tujuannya mengurangi kesenjangan desa–kota dan memperkuat kemandirian desa. Tantangannya meliputi kapasitas perencanaan, transparansi, dan risiko penyalahgunaan.\n\nPengecoh: dana desa tidak untuk gedung di ibu kota provinsi, gaji pegawai kabupaten, pembelian lahan industri asing, atau pembayaran utang luar negeri.",
      None),
]

P5 = [
    Q("Perhatikan grafik alokasi dana desa nasional berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Naik lebih dari tiga kali hingga 2019, lalu stabil", "Dana desa turun terus sejak 2015", "Dana desa tidak pernah berubah sejak 2015",
       "Dana desa naik dua kali lipat setiap tahun hingga 2023", "Dana desa pada 2023 lebih kecil daripada 2015"],
      "Grafik menunjukkan alokasi dana desa naik dari ±20,8 triliun rupiah (2015) menjadi ±47 triliun (2016), ±60 triliun (2017–2018), dan ±70 triliun (2019), sehingga dari 2015 ke 2019 naik sekitar 3,4 kali (70 ÷ 20,8). Setelah itu alokasinya relatif stabil sekitar 70 triliun. Peningkatan ini menunjukkan komitmen pemerintah memperkuat pembangunan dari pinggiran (desa).\n\nPengecoh: dana desa tidak turun. Alokasinya berubah. Kenaikan tidak dua kali lipat setiap tahun. Dana 2023 jauh lebih besar daripada 2015.",
      f_danadesa),
    Q("Pemindahan ibu kota negara ke Kalimantan Timur (IKN Nusantara) antara lain dimaksudkan untuk …",
      ["Mengurangi beban Jakarta dan meratakan pembangunan", "Memindahkan seluruh penduduk Jawa ke Kalimantan",
       "Menghentikan kegiatan ekonomi di Jakarta sepenuhnya", "Menjauhkan ibu kota dari wilayah yang memiliki hutan", "Mengurangi jumlah provinsi di Indonesia"],
      "Alasan pemindahan ibu kota antara lain: (1) beban Jakarta sangat berat, misalnya kemacetan, banjir, penurunan muka tanah, dan kepadatan penduduk; (2) konsentrasi ekonomi dan penduduk di Jawa memperlebar ketimpangan wilayah; (3) lokasi di Kalimantan Timur relatif berada di tengah Indonesia dan rendah risiko gempa serta gunung api dibandingkan Jawa. IKN diharapkan menjadi pusat pertumbuhan baru di luar Jawa.\nKritik dan tantangannya meliputi biaya sangat besar, dampak terhadap hutan dan masyarakat adat, serta ketidakpastian apakah IKN benar-benar mengurangi ketimpangan.\n\nPengecoh: tidak ada rencana memindahkan seluruh penduduk Jawa. Jakarta tetap menjadi pusat ekonomi. IKN justru berada di kawasan berhutan. Pemindahan ibu kota tidak mengurangi jumlah provinsi.",
      None),
    Q("Perhatikan peta sebaran sebagian Kawasan Ekonomi Khusus (KEK) berikut.\n\nPola sebaran KEK pada peta paling sesuai dengan tujuan …",
      ["Menumbuhkan pusat pertumbuhan baru di luar Jawa", "Memusatkan seluruh industri baru di Jakarta",
       "Membatasi investasi hanya di Pulau Jawa", "Menghindari wilayah pesisir dan pelabuhan", "Menempatkan KEK hanya di Papua"],
      "Peta menunjukkan KEK tersebar di luar Jawa, misalnya di Sumatra (Arun, Sei Mangkei, Galang Batang, Tanjung Api-Api), Kalimantan (Maloy), Sulawesi (Palu, Likupang), Nusa Tenggara (Mandalika), Maluku (Morotai), dan Papua (Sorong). Sebaran ini sesuai strategi pembangunan berbasis kutub pertumbuhan (growth pole) untuk menciptakan pusat-pusat ekonomi baru di luar Jawa, memanfaatkan potensi lokal (sawit, pariwisata, mineral, perikanan), dan mengurangi ketimpangan wilayah. Banyak KEK berada di pesisir dekat pelabuhan agar mudah terhubung dengan perdagangan.\n\nPengecoh: KEK tidak dipusatkan di Jakarta atau dibatasi di Jawa. KEK justru banyak di pesisir. KEK tidak hanya di Papua.",
      f_kek),
    Q("Konsep pertumbuhan inklusif (inclusive growth) menekankan bahwa …",
      ["Manfaat pertumbuhan harus dinikmati semua kelompok", "Pertumbuhan ekonomi cukup diukur dengan kenaikan PDB nasional",
       "Hanya kelompok kaya yang perlu menikmati hasil pertumbuhan", "Pertumbuhan ekonomi harus dihentikan agar ketimpangan hilang", "Pertumbuhan hanya penting di wilayah perkotaan"],
      "Pertumbuhan inklusif adalah pertumbuhan ekonomi yang tidak hanya tinggi, tetapi juga memperluas kesempatan dan manfaatnya bagi seluruh lapisan masyarakat dan wilayah, termasuk kelompok miskin, perempuan, penyandang disabilitas, dan daerah tertinggal. Indikatornya antara lain penurunan kemiskinan dan ketimpangan, perluasan lapangan kerja layak, serta akses yang merata terhadap pendidikan, kesehatan, dan infrastruktur.\n\nPengecoh: PDB nasional saja tidak menunjukkan inklusivitas. Pertumbuhan yang hanya dinikmati kelompok kaya justru eksklusif. Menghentikan pertumbuhan tidak menyelesaikan masalah. Inklusivitas mencakup kota dan desa.",
      None),
    Q("Perhatikan kurva insiden pertumbuhan dua negara berikut.\n\nNegara yang pertumbuhannya bersifat pro-poor (berpihak pada penduduk miskin) adalah …",
      ["Negara X, karena pengeluaran kelompok termiskin tumbuh paling cepat", "Negara Y, karena pengeluaran kelompok terkaya tumbuh paling cepat",
       "Kedua negara sama-sama pro-poor karena semua kelompok tumbuh positif", "Negara Y, karena garisnya naik dari kiri ke kanan", "Tidak ada yang pro-poor karena pertumbuhan di bawah 10%"],
      "Kurva insiden pertumbuhan (growth incidence curve) menunjukkan laju pertumbuhan pengeluaran atau pendapatan untuk setiap persentil penduduk. Pada Negara X, kurva menurun: kelompok termiskin (persentil 5) tumbuh ±6,3% per tahun, sedangkan kelompok terkaya (persentil 95) hanya ±2,2%. Pertumbuhan seperti ini berpihak pada penduduk miskin (pro-poor dalam arti relatif) dan cenderung menurunkan ketimpangan. Pada Negara Y, kurva naik: kelompok kaya tumbuh lebih cepat, sehingga ketimpangan meningkat walaupun semua kelompok tetap tumbuh.\n\nPengecoh: pertumbuhan positif semua kelompok belum tentu pro-poor dalam arti relatif. Kurva yang naik ke kanan justru menguntungkan kelompok kaya. Ukuran pro-poor tidak ditentukan ambang 10%.",
      f_gic),
    Q("SDG nomor 10 \"Berkurangnya Kesenjangan\" mencakup target berikut, KECUALI …",
      ["Menaikkan pendapatan 40% teratas lebih cepat dari rata-rata", "Mendorong inklusi sosial, ekonomi, dan politik bagi semua orang",
       "Menjamin kesetaraan kesempatan dan mengurangi diskriminasi", "Memfasilitasi migrasi yang tertib, aman, dan bertanggung jawab",
       "Mengadopsi kebijakan fiskal dan perlindungan sosial untuk kesetaraan"],
      "SDG 10 bertujuan mengurangi kesenjangan di dalam dan antarnegara. Target utamanya antara lain: (10.1) secara progresif mencapai dan mempertahankan pertumbuhan pendapatan 40% penduduk terbawah dengan laju lebih tinggi daripada rata-rata nasional; (10.2) memberdayakan dan mendorong inklusi sosial, ekonomi, dan politik bagi semua; (10.3) menjamin kesetaraan kesempatan dan mengurangi diskriminasi; (10.4) mengadopsi kebijakan fiskal, upah, dan perlindungan sosial; serta (10.7) memfasilitasi migrasi yang tertib dan aman.\nOpsi pertama keliru karena targetnya adalah 40% penduduk terbawah, bukan teratas. Menaikkan pendapatan kelompok teratas lebih cepat justru memperlebar kesenjangan.\n\nOpsi lainnya adalah target SDG 10 yang benar. Perhatikan kata KECUALI.",
      None),
    Q("Perhatikan hasil evaluasi penyaluran sebuah program bantuan sosial berikut.\n\nBesar kesalahan eksklusi (exclusion error), yaitu persentase rumah tangga miskin yang tidak menerima bantuan, adalah …",
      ["Sekitar 27%", "Sekitar 20%", "Sekitar 6%", "Sekitar 8%", "Sekitar 73%"],
      "Jumlah rumah tangga miskin = P + R = 8 juta + 3 juta = 11 juta.\nRumah tangga miskin yang tidak menerima bantuan = R = 3 juta.\nKesalahan eksklusi = 3 ÷ 11 × 100% ≈ 27%.\nSebagai pembanding, kesalahan inklusi (penerima yang sebenarnya tidak miskin) = Q ÷ (P + Q) = 2 ÷ 10 = 20%. Kedua jenis kesalahan ini menunjukkan pentingnya data terpadu dan pemutakhiran data penerima agar bantuan tepat sasaran.\n\nPengecoh: 20% adalah kesalahan inklusi. 6% dan 8% membagi dengan seluruh rumah tangga (50 juta) secara keliru. 73% adalah persentase rumah tangga miskin yang menerima bantuan (cakupan).",
      f_targeting),
    Q("Visi Indonesia Emas 2045 menargetkan Indonesia menjadi negara maju. Dari sudut pandang geografi pembangunan, tantangan yang paling penting untuk diatasi adalah …",
      ["Ketimpangan wilayah, kualitas SDM, dan lingkungan", "Terlalu sedikitnya jumlah penduduk usia produktif saat ini",
       "Tidak adanya sumber daya alam di seluruh wilayah Indonesia", "Kelebihan infrastruktur di wilayah timur Indonesia", "Terlalu rendahnya tingkat urbanisasi di Pulau Jawa"],
      "Untuk menjadi negara maju pada 2045, Indonesia harus menjaga pertumbuhan ekonomi tinggi secara berkelanjutan sekaligus inklusif. Dari sudut pandang geografi pembangunan, tantangan pentingnya antara lain: (1) ketimpangan antarwilayah, terutama antara Jawa dan luar Jawa serta kota dan desa; (2) kualitas sumber daya manusia untuk memanfaatkan bonus demografi; (3) keberlanjutan lingkungan, termasuk deforestasi, perubahan iklim, dan risiko bencana; serta (4) transformasi ekonomi dari komoditas mentah ke industri dan jasa bernilai tambah tinggi.\n\nPengecoh: penduduk usia produktif justru sedang dalam porsi terbesar (bonus demografi). Indonesia kaya sumber daya alam. Infrastruktur di wilayah timur justru masih kurang. Tingkat urbanisasi di Jawa sudah tinggi.",
      None),
    Q("Perhatikan grafik transfer pusat ke daerah per kapita menurut wilayah berikut.\n\nPenjelasan yang paling tepat untuk tingginya transfer per kapita ke Maluku–Papua adalah …",
      ["Dana otonomi khusus dan biaya pembangunan yang tinggi", "Maluku–Papua memiliki jumlah penduduk terbanyak di Indonesia",
       "Maluku–Papua menyumbang pajak terbesar sehingga mendapat transfer paling banyak", "Transfer ke daerah dibagi sama rata untuk setiap provinsi tanpa kriteria",
       "Jawa tidak menerima transfer dari pemerintah pusat sama sekali"],
      "Grafik menunjukkan transfer per kapita ke Maluku–Papua (±9,6 juta rupiah per orang) jauh lebih tinggi daripada Jawa (±2,1 juta). Penyebabnya: (1) Papua dan Papua Barat menerima Dana Otonomi Khusus dan dana tambahan infrastruktur; (2) formula Dana Alokasi Umum mempertimbangkan luas wilayah, indeks kemahalan konstruksi, dan kebutuhan fiskal yang tinggi, sedangkan jumlah penduduknya sedikit; serta (3) kapasitas fiskal daerah (pendapatan asli daerah) rendah. Transfer ini merupakan instrumen pemerataan fiskal antarwilayah.\n\nPengecoh: penduduk Maluku–Papua justru sedikit. Penyumbang pajak terbesar berada di Jawa. Transfer tidak dibagi sama rata. Jawa tetap menerima transfer, tetapi per kapitanya kecil karena penduduknya banyak.",
      f_transfer),
    Q("Aceh dan Papua memiliki status otonomi khusus. Tujuan utama pemberian otonomi khusus kepada kedua daerah tersebut adalah …",
      ["Mengakomodasi kekhususan dan mempercepat kesejahteraan", "Memisahkan kedua daerah dari Negara Kesatuan Republik Indonesia",
       "Menghapus seluruh kewenangan pemerintah daerah di kedua provinsi", "Melarang investasi masuk ke kedua daerah", "Menghentikan dana transfer dari pemerintah pusat"],
      "Otonomi khusus diberikan kepada Aceh (UU No. 11 Tahun 2006) dan Papua (UU No. 21 Tahun 2001, diubah dengan UU No. 2 Tahun 2021) sebagai bentuk pengakuan atas kekhususan sejarah, konflik masa lalu, identitas sosial-budaya, serta ketertinggalan pembangunan. Bentuknya antara lain kewenangan khusus (misalnya penerapan syariat Islam di Aceh, Majelis Rakyat Papua), afirmasi bagi penduduk asli, dan dana otonomi khusus untuk pendidikan, kesehatan, ekonomi, dan infrastruktur. Tujuannya mempercepat kesejahteraan dan menjaga keutuhan NKRI.\n\nPengecoh: otonomi khusus tidak memisahkan daerah dari NKRI. Kewenangan daerah justru diperluas. Investasi tidak dilarang. Transfer justru bertambah melalui dana otonomi khusus.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
