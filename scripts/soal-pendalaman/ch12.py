from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)


def tag(ax, x, y, t, fs=13, c="#C53030"):
    ax.text(x, y, t, fontsize=fs, fontweight="bold", color=c, ha="center", va="center", bbox=dict(fc="white", ec=c, boxstyle="round,pad=0.25"))

# ============================ figures: paket 1 ============================

def f_hier(path):
    fig, ax = blank(9.5, 5.4, (0, 100), (0, 62))
    ax.add_patch(Circle((50, 50), 6, fc=C["red"], ec="black")); ax.text(50, 50, "Jakarta\n2017", ha="center", va="center", fontsize=8.5, color="white", fontweight="bold")
    mids = [(20, 30, "Medan"), (50, 30, "Surabaya"), (80, 30, "Makassar")]
    for x, y, n in mids:
        ax.add_patch(Circle((x, y), 4.5, fc=C["orange"], ec="black")); ax.text(x, y, f"{n}\n2018", ha="center", va="center", fontsize=7.5, fontweight="bold")
        arrow(ax, 50 + (x - 50) * 0.12, 44, x, y + 5, color=C["gray"])
        for dx in (-9, 0, 9):
            ax.add_patch(Circle((x + dx, 10), 2.6, fc=C["yellow"], ec="black")); arrow(ax, x + dx * 0.3, y - 4.6, x + dx, 13, color="#A0AEC0", lw=1.4, ms=10)
        ax.text(x, 4, "kota kabupaten (2019)", ha="center", fontsize=8)
    for (x, y) in [(66, 54), (68, 46), (34, 54)]:
        ax.add_patch(Circle((x, y), 1.6, fc="#E2E8F0", ec="black"))
    ax.text(73, 50.5, "desa di pinggiran Jakarta\n(baru 2020)", fontsize=8.5)
    ax.set_title("Persebaran tren kedai kopi susu kekinian")
    save(fig, path)


def f_ikl1(path):
    table([["Bahasa A", "25.000", "50%"], ["Bahasa B", "15.000", "30%"], ["Bahasa C", "10.000", "20%"], ["Jumlah", "50.000", "100%"]],
          ["Bahasa ibu", "Penutur", "Proporsi"], path, title="Komposisi bahasa ibu penduduk Kabupaten K", col_w=[0.4, 0.3, 0.3])


SHAPES = [("P", "CHL", (-76, -66, -56, -17)), ("Q", "POL", (13.5, 24.5, 48.5, 55)), ("R", "THA", (97, 106, 5, 21)), ("S", "PHL", (116, 127, 4.5, 21)),
          ("T", "ZAF", (16, 33.5, -35, -22))]


def f_bentuk(path):
    fig, axs = plt.subplots(1, 5, figsize=(12, 4.6), gridspec_kw=dict(width_ratios=[0.6, 1.1, 0.8, 0.8, 1.3]))
    feats = world_features()
    for ax, (lab, code, ext) in zip(axs, SHAPES):
        ax.set_facecolor("white")
        draw_geo(ax, [f for f in feats if f["properties"]["ADM0_A3"] == code], fc="#68A063", ec="#2F4F2F", lw=0.6)
        if code == "ZAF":
            draw_geo(ax, [f for f in feats if f["properties"]["ADM0_A3"] in ("LSO",)], fc="white", ec="#2F4F2F", lw=0.6)
        ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3]); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(lab, fontsize=16, fontweight="bold")
    fig.suptitle("Siluet lima negara (skala tidak sama)", fontsize=13, fontweight="bold")
    save(fig, path)


def f_shift(path):
    bars(["60+ th", "40–59 th", "25–39 th", "15–24 th", "5–14 th"], {"Bahasa daerah": [85, 72, 55, 38, 25], "Bahasa Indonesia": [15, 28, 45, 62, 75]}, path,
         title="Bahasa ibu penduduk Kota X menurut kelompok umur (%)", ylabel="%", stacked=True, values=True, ylim=(0, 140), colors=[C["green"], C["red"]],
         w=8.5, legend_loc="upper center")


def f_papua(path):
    fig, ax = world_map(extent=(128, 152, -11.5, 1), colors={"IDN": "#F6E7B0", "PNG": "#C6F6D5"}, w=10, h=5.2)
    ax.text(136.5, -4.5, "INDONESIA", fontsize=11, fontweight="bold"); ax.text(144.5, -6.2, "PAPUA NUGINI", fontsize=11, fontweight="bold")
    tag(ax, 141, -2.3, "X"); arrow(ax, 141.5, -2.6, 141.05, -3.4, color=C["red"], lw=1.5, ms=10)
    tag(ax, 139.6, -7.6, "Y"); arrow(ax, 140.1, -7.6, 140.95, -7.0, color=C["red"], lw=1.5, ms=10)
    ax.set_title("Batas darat Indonesia–Papua Nugini")
    ax.set_xticks([130, 135, 140, 145, 150]); ax.set_xticklabels([f"{v}°BT" for v in [130, 135, 140, 145, 150]], fontsize=8)
    save(fig, path)


def f_seg1(path):
    table([["Distrik 1", "600", "100"], ["Distrik 2", "300", "300"], ["Distrik 3", "100", "600"], ["Jumlah", "1.000", "1.000"]],
          ["Distrik", "Kelompok A", "Kelompok B"], path, title="Sebaran dua kelompok etnis di Kota S", col_w=[0.34, 0.33, 0.33])

# ============================ figures: paket 2 ============================

def f_austro(path):
    fig, ax = world_map(extent=(35, 185, -32, 32), w=11, h=4.8)
    pts = [("Taiwan\n±3000 SM", 121, 23.7), ("Filipina", 122, 13), ("Kalimantan–Sulawesi", 117, 0), ("Jawa–Nusa Tenggara", 115, -9),
           ("Pasifik barat\n±1200 SM", 160, -8), ("Madagaskar\n±500 M", 47, -19)]
    route = [(121, 23), (122, 14), (118, 2), (113, -6)]
    for (a, b), (c, d) in zip(route[:-1], route[1:]):
        arrow(ax, a, b, c, d, color=C["red"], lw=2.2)
    arrow(ax, 125, 0, 158, -7, color=C["red"], lw=2.2)
    arrow(ax, 108, -6, 50, -17, color=C["red"], lw=2.2, ls="--")
    for t, x, y in pts:
        ax.text(x + 1.2, y + 1.2, t, fontsize=8.5, fontweight="bold", bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ax.set_title("Persebaran penutur rumpun bahasa Austronesia (disederhanakan)")
    save(fig, path)


def f_sekuen(path):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, ttl in zip(axs, ["Tahap I (±1800)", "Tahap II (±1900)", "Tahap III (±2010)"]):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([]); ax.set_facecolor("#F0FFF4"); ax.set_title(ttl, fontsize=11, fontweight="bold")
        ax.plot([0, 10], [2.2, 2.6], color=C["blue"], lw=4)
    rng = np.random.default_rng(3)
    for x, y in rng.uniform(0.5, 9.5, (40, 2)):
        if y > 3: axs[0].plot(x, y, "^", color="#2F855A", ms=10)
    for x in (4, 4.8, 5.6):
        axs[0].add_patch(Rectangle((x, 3.3), 0.6, 0.6, fc="#C05621"))
    axs[0].text(5, 0.8, "hutan, kampung adat, ladang", ha="center", fontsize=9)
    for r in range(4):
        for c in range(9):
            axs[1].plot(0.8 + c, 4 + r * 1.4, "o", color="#38A169", ms=7)
    axs[1].add_patch(Rectangle((6.8, 8.5), 2.2, 1, fc="#A0AEC0")); axs[1].text(7.9, 9.0, "pabrik teh", ha="center", fontsize=7.5)
    axs[1].plot([0, 10], [3.4, 3.4], color="#4A5568", lw=2.5, ls="--"); axs[1].text(5, 0.8, "perkebunan kolonial, rel lori", ha="center", fontsize=9)
    for i in range(16):
        axs[2].add_patch(Rectangle((0.6 + (i % 8) * 1.15, 3.6 + (i // 8) * 2.4), 0.9, 1.6 + (i % 3) * 0.6, fc="#718096"))
    axs[2].plot([0, 10], [3.2, 3.2], color="#2D3748", lw=4); axs[2].text(5, 0.8, "permukiman kota, jalan raya, ruko", ha="center", fontsize=9)
    fig.suptitle("Perubahan lanskap sebuah kawasan di Jawa Barat", fontsize=13, fontweight="bold")
    save(fig, path)


def f_rumpun(path):
    bars(["Mandarin", "Spanyol", "Inggris", "Hindi", "Bengali", "Portugis", "Rusia", "Jepang"], {"Penutur bahasa ibu (juta)": [940, 485, 380, 345, 237, 236, 148, 123]}, path,
         title="Delapan bahasa dengan penutur bahasa ibu terbanyak (perkiraan)", ylabel="juta penutur", values=True, ylim=(0, 1080), colors=[C["purple"]], w=9.5)


def f_rumah(path):
    fig, ax = blank(8, 6, (0, 100), (0, 80))
    ax.add_patch(Rectangle((0, 0), 100, 8, fc="#C6F6D5"))
    ax.add_patch(Rectangle((0, 0), 100, 4, fc=C["lblue"], alpha=0.7)); ax.text(88, 1.2, "genangan banjir", fontsize=8)
    for x in (22, 38, 54, 70):
        ax.add_patch(Rectangle((x, 4), 2.2, 24, fc="#8B5A2B"))
    ax.add_patch(Rectangle((18, 28), 58, 22, fc="#D69E2E", ec="#5F370E", lw=1.5))
    for x in range(22, 74, 6):
        ax.plot([x, x], [30, 48], color="#5F370E", lw=1)
    ax.add_patch(Polygon([(10, 50), (47, 76), (84, 50)], fc="#744210", ec="black"))
    label(ax, 88, 64, "1", bg="white"); arrow(ax, 86, 64, 70, 60, color=C["red"], lw=1.4, ms=10); ax.text(90, 60, "atap curam\nlebar", fontsize=8)
    label(ax, 92, 38, "2", bg="white"); arrow(ax, 90, 38, 77, 38, color=C["red"], lw=1.4, ms=10); ax.text(86, 32, "dinding anyaman\nberongga", fontsize=8)
    label(ax, 8, 18, "3", bg="white"); arrow(ax, 10, 18, 21, 18, color=C["red"], lw=1.4, ms=10); ax.text(2, 10.5, "tiang tinggi\n(kolong)", fontsize=8)
    ax.set_title("Sketsa rumah tradisional di dataran rendah pesisir Sumatra")
    save(fig, path)


def f_ikl2(path):
    bars(["Bahasa 1", "Bahasa 2", "Bahasa 3", "Bahasa 4"], {"Kabupaten M": [25, 25, 25, 25], "Kabupaten N": [70, 10, 10, 10]}, path,
         title="Proporsi penutur bahasa ibu di dua kabupaten (%)", ylabel="%", values=True, ylim=(0, 85), colors=[C["teal"], C["orange"]], w=8)


def f_topo(path):
    table([["1", "Kuala Tungkal", "Jambi"], ["2", "Muara Enim", "Sumatera Selatan"], ["3", "Tanjung Priok", "DKI Jakarta"], ["4", "Teluk Betung", "Lampung"],
           ["5", "Gunung Sitoli", "Sumatera Utara"]], ["No", "Nama tempat", "Provinsi"], path, title="Beberapa toponim di Indonesia", col_w=[0.12, 0.44, 0.44])

# ============================ figures: paket 3 ============================

def f_agama(path):
    fig, ax = plt.subplots(figsize=(8, 5))
    d = [87.1, 7.4, 3.1, 1.7, 0.7]; lab = ["Islam", "Kristen", "Katolik", "Hindu", "Buddha & lainnya"]
    ws, _ = ax.pie(d, colors=[C["green"], C["blue"], C["purple"], C["orange"], C["gray"]], startangle=90, wedgeprops=dict(ec="white"))
    ax.legend(ws, [f"{l}: {_p(v)}%" for l, v in zip(lab, d)], loc="center left", bbox_to_anchor=(1, 0.5), frameon=False, fontsize=11)
    ax.set_title("Komposisi penduduk Indonesia menurut agama (perkiraan)")
    save(fig, path)


def _p(v):
    return f"{v:g}".replace(".", ",")


BALKAN = {"HRV": ("P", "#FBD38D"), "SRB": ("Q", "#BEE3F8"), "BIH": ("R", "#E9D8FD"), "ALB": ("S", "#9AE6B4"), "GRC": ("T", "#FED7E2")}


def f_balkan(path):
    cols = {k: v[1] for k, v in BALKAN.items()}
    fig, ax = world_map(extent=(13, 29, 35, 47.5), colors=cols, w=7.5, h=6.2)
    pos = {"HRV": (15.6, 45.3), "SRB": (20.8, 44.0), "BIH": (17.8, 44.2), "ALB": (20.0, 41.0), "GRC": (22.0, 39.3)}
    for k, (x, y) in pos.items():
        tag(ax, x, y, BALKAN[k][0])
    ax.set_title("Beberapa negara di Semenanjung Balkan")
    save(fig, path)


def f_menular(path):
    fig, ax = blank(7.5, 6.4, (-45, 45), (-45, 45))
    for r, c, t in [(40, "#FFF5F5", "10%"), (20, "#FED7D7", "30%"), (10, "#FC8181", "60%"), (5, "#C53030", "90%")]:
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#742A2A"))
        ax.text(r * 0.72, r * 0.72, t, fontsize=10, fontweight="bold")
    ax.text(0, 0, "Desa\nasal", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    for r in (5, 10, 20, 40):
        ax.text(0, -r - 2.5, f"{r} km", ha="center", fontsize=8)
    ax.set_title("Persentase petani yang memakai teknik budidaya baru\n(10 tahun setelah diperkenalkan)", fontsize=11)
    save(fig, path)


def f_haji(path):
    bars(["Indonesia", "Pakistan", "India", "Bangladesh", "Nigeria"], {"Kuota haji (ribu orang)": [221, 179, 175, 127, 95]}, path,
         title="Kuota haji beberapa negara (perkiraan)", ylabel="ribu orang", values=True, ylim=(0, 260), colors=[C["green"]], w=8)


def f_matri(path):
    fig, ax = blank(10, 6, (0, 100), (0, 64))
    def person(x, y, t, female, fill):
        if female:
            ax.add_patch(Circle((x, y), 3.2, fc=fill, ec="black", lw=1.4))
        else:
            ax.add_patch(Rectangle((x - 3, y - 3), 6, 6, fc=fill, ec="black", lw=1.4))
        ax.text(x, y - 6.2, t, ha="center", fontsize=9)
    G = "white"; W = "white"
    person(30, 56, "Nenek", True, G)
    ax.plot([30, 30], [52.8, 47], color="black"); ax.plot([18, 52], [47, 47], color="black")
    ax.plot([18, 18], [47, 41], color="black"); ax.plot([52, 52], [47, 41], color="black")
    person(18, 38, "Ibu", True, G); person(52, 38, "Mamak", False, G)
    person(6, 38, "Ayah", False, W); ax.plot([9, 14.8], [38, 38], color="black", lw=2)
    person(66, 38, "Istri mamak", True, W); ax.plot([55, 62.8], [38, 38], color="black", lw=2)
    ax.plot([12, 12], [38, 26], color="black"); ax.plot([6, 20], [26, 26], color="black")
    ax.plot([6, 6], [26, 20], color="black"); ax.plot([20, 20], [26, 20], color="black")
    person(6, 17, "Ego", False, G); person(20, 17, "Adik ego", True, G)
    ax.plot([59, 59], [38, 26], color="black"); ax.plot([52, 66], [26, 26], color="black")
    ax.plot([52, 52], [26, 20], color="black"); ax.plot([66, 66], [26, 20], color="black")
    person(52, 17, "Anak mamak 1", False, W); person(66, 17, "Anak mamak 2", True, W)
    ax.text(76, 54, "○ perempuan\n□ laki-laki\n═ hubungan perkawinan\n│ garis keturunan", fontsize=9, va="top")
    ax.set_title("Diagram kekerabatan sebuah keluarga Minangkabau")
    save(fig, path)


def f_hallyu(path):
    lines([2012, 2014, 2016, 2018, 2020, 2022], {"Indeks minat terhadap K-pop dan drama Korea": [22, 30, 41, 63, 92, 88]}, path,
          title="Minat warganet Indonesia terhadap budaya pop Korea (ilustrasi, maks = 100)", xlabel="Tahun", ylabel="indeks", ylim=(0, 105), w=8.5)

# ============================ figures: paket 4 ============================

def f_kurdi(path):
    fig, ax = world_map(extent=(26, 62, 24, 44), w=9, h=5.2)
    ax.add_patch(Polygon([(37, 37.2), (38.5, 39.5), (42, 40.3), (44.5, 39.6), (46.5, 37.5), (47.5, 35), (46, 33.6), (44.2, 34.4), (43, 35.8), (41, 36.6), (39, 36.2)],
                         fc=C["red"], alpha=0.45, ec=C["red"], lw=2, hatch="//"))
    tag(ax, 42.4, 37.9, "X")
    for t, x, y in [("TURKI", 33, 39), ("SURIAH", 38.2, 34.6), ("IRAK", 43.2, 32.5), ("IRAN", 53, 32.5)]:
        ax.text(x, y, t, fontsize=10, fontweight="bold", color="#4A5568")
    ax.set_title("Wilayah persebaran sebuah kelompok etnis (X)")
    save(fig, path)


def f_etnis(path):
    bars(["Jawa", "Bugis", "Banjar", "Dayak"], {"Proporsi penduduk (%)": [40, 25, 20, 15]}, path, title="Komposisi etnis penduduk Provinsi E (ilustrasi)", ylabel="%",
         values=True, ylim=(0, 50), colors=[C["blue"]], w=7)


def f_faktor(path):
    table([["1", "Bahasa nasional yang dipakai bersama"], ["2", "Kesenjangan ekonomi antarwilayah yang lebar"], ["3", "Ideologi dan simbol negara yang diterima bersama"],
           ["4", "Gerakan separatis bersenjata"], ["5", "Sistem pendidikan nasional"], ["6", "Politisasi identitas kesukuan dalam pemilu"]],
          ["No", "Faktor"], path, title="Faktor-faktor yang memengaruhi keutuhan negara", col_w=[0.12, 0.88])


def f_batas(path):
    table([["P", "Ditarik sebelum wilayah dihuni padat oleh penduduk"], ["Q", "Ditarik setelah permukiman dan batas budaya terbentuk, mengikutinya"],
           ["R", "Dipaksakan kekuatan luar dan memotong wilayah suatu suku"], ["S", "Tidak lagi berfungsi, tetapi jejaknya masih terlihat di lanskap"]],
          ["Batas", "Ciri"], path, title="Klasifikasi genetik batas negara", col_w=[0.12, 0.88], fs=11)


def f_kompak(path):
    table([["Negara A", "250.000", "2.000"], ["Negara B", "160.000", "5.000"], ["Negara C", "360.000", "3.000"]],
          ["Negara", "Luas (km²)", "Panjang batas (km)"], path, title="Luas dan panjang batas tiga negara (ilustrasi)", col_w=[0.3, 0.33, 0.37])


def f_timor(path):
    fig, ax = world_map(extent=(123, 127.6, -10.6, -8.1), colors={"TLS": "#9AE6B4", "IDN": "#F6E7B0"}, w=10, h=5.4)
    ax.text(126.0, -8.95, "TIMOR-LESTE", fontsize=11, fontweight="bold")
    ax.text(124.0, -9.9, "NUSA TENGGARA TIMUR\n(INDONESIA)", fontsize=10, fontweight="bold", ha="center")
    tag(ax, 124.3, -8.85, "X")
    ax.set_title("Pulau Timor")
    save(fig, path)

# ============================ figures: paket 5 ============================

def f_kota(path):
    fig, ax = blank(7.5, 6.6, (0, 100), (0, 100))
    ax.add_patch(Rectangle((35, 38), 30, 26, fc="#C6F6D5", ec="#2F855A", lw=2)); ax.text(50, 51, "Alun-alun\nutara", ha="center", va="center", fontsize=11, fontweight="bold")
    for (x, y, w, h, t) in [(10, 40, 18, 22, "P"), (38, 72, 24, 16, "Q"), (72, 40, 18, 22, "R"), (32, 6, 36, 24, "S")]:
        ax.add_patch(Rectangle((x, y), w, h, fc="#EDF2F7", ec="#4A5568", lw=1.5)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=16, fontweight="bold")
    ax.text(50, 4, "S = keraton", ha="center", fontsize=9)
    north_arrow(ax, 0.92, 0.85)
    ax.set_title("Pola tata ruang inti kota kerajaan Islam di Jawa")
    save(fig, path)


def f_aksara(path):
    fig, ax = blank(10, 5.6, (0, 100), (0, 62))
    box(ax, 40, 52, 20, 7, "Brahmi (India)", fc="#FEEBC8", fs=10, bold=True)
    box(ax, 40, 38, 20, 7, "Pallawa", fc="#FEEBC8", fs=10, bold=True)
    box(ax, 40, 24, 20, 7, "Kawi (Jawa Kuno)", fc="#FEEBC8", fs=10, bold=True)
    arrow(ax, 50, 52, 50, 45.2); arrow(ax, 50, 38, 50, 31.2)
    leaves = [(8, "Jawa"), (23, "Bali"), (38, "Sunda"), (58, "Batak"), (74, "Lontara\n(Bugis)"), (90, "Rencong")]
    for x, t in leaves:
        box(ax, x - 6, 4, 13, 8, t, fc="#E6FFFA", fs=9)
    for x, t in leaves[:3]:
        arrow(ax, 50, 24, x + 0.5, 12.2, lw=1.4, ms=10)
    for x, t in leaves[3:]:
        arrow(ax, 60, 38, x + 0.5, 12.2, lw=1.4, ms=10, ls="--")
    ax.text(70, 30, "garis putus: jalur turunan\nyang masih diperdebatkan", fontsize=8.5, color=C["gray"])
    ax.set_title("Silsilah beberapa aksara Nusantara (disederhanakan)")
    save(fig, path)


def f_ikl3(path):
    table([["Papua (sebelum pemekaran)", "0,95"], ["Nusa Tenggara Timur", "0,90"], ["Sulawesi Tengah", "0,84"], ["Jawa Tengah", "0,06"], ["Yogyakarta", "0,08"]],
          ["Provinsi", "IKL"], path, title="Indeks keragaman linguistik beberapa provinsi (ilustrasi)", col_w=[0.7, 0.3])


def f_tpak(path):
    bars(["Laki-laki", "Perempuan"], {"TPAK (%)": [84, 54]}, path, title="TPAK menurut jenis kelamin (ilustrasi)",
         ylabel="%", values=True, ylim=(0, 100), colors=[C["teal"]], w=7)


def f_vernak(path):
    table([["P", "Bulat, dinding rapat tanpa jendela, pintu rendah, perapian di tengah"], ["Q", "Panggung tinggi, dinding anyaman berventilasi, atap curam"],
           ["R", "Atap melengkung bergonjong, panggung, berukir"], ["S", "Rumah sangat panjang dihuni banyak keluarga di tepi sungai"]],
          ["Rumah", "Ciri bangunan"], path, title="Ciri beberapa rumah tradisional Indonesia", col_w=[0.14, 0.86], fs=11)


PANGAN = {"Papua": "#38A169", "Papua Barat": "#38A169", "Maluku": "#38A169", "Maluku Utara": "#38A169", "Nusa Tenggara Timur": "#ECC94B", "Gorontalo": "#ECC94B"}


def f_pangan(path):
    fig, ax = indonesia_map(colors=PANGAN, fc="#FBD38D", w=10, h=4.6)
    legend_patches(ax, [("padi (beras)", "#FBD38D"), ("jagung", "#ECC94B"), ("sagu & umbi", "#38A169")], title="Pangan pokok tradisional dominan")
    ax.set_title("Pangan pokok tradisional dominan menurut provinsi (disederhanakan)")
    save(fig, path)

# ============================ figures: paket 6 ============================

UNESCO = [("Wayang", 2008), ("Keris", 2008), ("Batik", 2009), ("Angklung", 2010), ("Tari Saman*", 2011), ("Noken*", 2012), ("Tari Bali", 2015), ("Pinisi", 2017),
          ("Pencak silat", 2019), ("Pantun", 2020), ("Gamelan", 2021), ("Jamu", 2023), ("Reog", 2024), ("Kebaya", 2024)]


def f_unesco(path):
    fig, ax = new(9, 6)
    n = len(UNESCO)
    for i, (nm, y) in enumerate(UNESCO):
        c = C["red"] if "*" in nm else C["blue"]
        yy = n - i
        ax.plot([2007, y], [yy, yy], color="#E2E8F0", lw=1)
        ax.plot(y, yy, "o", ms=11, color=c)
        ax.text(y + 0.35, yy, nm, va="center", fontsize=10, color=c, fontweight="bold" if "*" in nm else None)
    ax.set_yticks([]); ax.set_xticks(range(2008, 2025, 2)); ax.set_xlim(2007, 2026.5); ax.set_ylim(0, n + 1.6); ax.spines["left"].set_visible(False)
    ax.set_xlabel("Tahun pengakuan")
    ax.text(2007.2, n + 0.9, "* daftar warisan yang memerlukan perlindungan mendesak", fontsize=9.5, color=C["red"])
    ax.set_title("Beberapa warisan budaya takbenda Indonesia yang diakui UNESCO")
    save(fig, path)


def f_seg2(path):
    fig, ax = blank(8, 6.2, (0, 100), (0, 84))
    data = [("Distrik 1", 400, 20), ("Distrik 2", 300, 80), ("Distrik 3", 200, 300), ("Distrik 4", 100, 600)]
    for i, (n, a, b) in enumerate(data):
        x = 6 + (i % 2) * 46; y = 42 - (i // 2) * 38
        ax.add_patch(Rectangle((x, y), 42, 34, fc="#F7FAFC", ec="#2D3748", lw=1.5))
        ax.text(x + 21, y + 28, n, ha="center", fontsize=11, fontweight="bold")
        ax.text(x + 21, y + 17, f"Kelompok A: {a}", ha="center", fontsize=10.5, color=C["blue"])
        ax.text(x + 21, y + 8, f"Kelompok B: {b}", ha="center", fontsize=10.5, color=C["orange"])
    ax.set_title("Sebaran dua kelompok etnis di Kota R (orang)")
    save(fig, path)


def f_vital(path):
    bars(["60+ th", "40–59 th", "20–39 th", "10–19 th", "0–9 th"], {"Penutur aktif bahasa L (%)": [95, 80, 35, 8, 2]}, path,
         title="Penutur aktif bahasa L menurut kelompok umur di komunitasnya", ylabel="% dari kelompok umur", values=True, ylim=(0, 110), colors=[C["purple"]], w=8)


def f_wilayah(path):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.4))
    for ax, t in zip(axs, "PQR"):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t, fontsize=16, fontweight="bold")
    axs[0].add_patch(Polygon([(1, 1), (9, 1.5), (8.5, 9), (1.5, 8.5)], fc="#68D391", ec="black")); axs[0].text(5, 0.2, "seluruhnya berbahasa Sunda", ha="center", fontsize=9)
    axs[1].plot(5, 5, "o", ms=18, color=C["red"])
    rng = np.random.default_rng(5)
    for x, y in rng.uniform(0.8, 9.2, (14, 2)):
        axs[1].plot([x, 5], [y, 5], color="#A0AEC0", lw=1); axs[1].plot(x, y, "o", ms=5, color="#4A5568")
    axs[1].text(5, 0.2, "daerah jangkauan siaran radio dari kota", ha="center", fontsize=9)
    for a, r in [(0.15, 4.2), (0.25, 3.2), (0.4, 2.2)]:
        axs[2].add_patch(Ellipse((5, 5), 2 * r * 1.1, 2 * r * 0.9, fc="#F6AD55", alpha=a, ec="none"))
    axs[2].text(5, 5, "Tapal Kuda", ha="center", va="center", fontsize=11, fontweight="bold")
    axs[2].text(5, 0.2, "batas kabur, menurut persepsi warga", ha="center", fontsize=9)
    fig.suptitle("Tiga jenis wilayah budaya", fontsize=13, fontweight="bold")
    save(fig, path)


def f_transmig(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    src = (110.5, -7.3)
    for (x, y, t) in [(105.2, -4.8, "Lampung"), (103.8, -3.2, "Sumsel"), (113.5, -1.8, "Kalteng"), (121.8, -1.5, "Sulteng"), (140.2, -8.0, "Merauke")]:
        arrow(ax, src[0], src[1], x, y, color=C["red"], lw=1.8, ms=12)
        ax.text(x, y + 0.6, t, fontsize=8.5, fontweight="bold", ha="center", bbox=dict(fc="white", ec="none", pad=0.8))
    ax.text(110.5, -9.6, "Jawa Tengah", fontsize=8.5, fontweight="bold", ha="center")
    ax.set_title("Arah perpindahan penduduk program transmigrasi dari Jawa")
    save(fig, path)


def f_internet(path):
    bars(["Inggris", "Spanyol", "Jerman", "Jepang", "Prancis", "Indonesia"], {"Porsi konten situs web (%)": [49, 6, 5.6, 5, 4.4, 0.9]}, path,
         title="Bahasa konten situs web dunia (perkiraan)", ylabel="% situs web", values=True, ylim=(0, 58), colors=[C["blue"]], w=8.5, fmt="{:g}")

# ============================ questions ============================
P0 = [
    Q("Perhatikan diagram persebaran tren kedai kopi susu kekinian berikut.\n\nJenis difusi yang paling tepat menggambarkan pola tersebut adalah …",
      ["Difusi hierarki", "Difusi menular", "Difusi relokasi", "Difusi stimulus", "Difusi balik (reverse)"],
      "Diagram menunjukkan tren muncul di Jakarta (2017), lalu melompat ke kota besar lain seperti Medan, Surabaya, dan Makassar (2018), kemudian ke kota kabupaten (2019). Desa di pinggiran Jakarta yang jaraknya dekat justru baru mengadopsi pada 2020. Artinya penyebaran mengikuti urutan ukuran dan kepentingan kota, bukan kedekatan jarak. Pola ini adalah difusi hierarki (hierarchical diffusion), yang umum untuk tren mode, teknologi, dan gaya hidup karena kota besar terhubung erat oleh media, modal, dan jaringan usaha.\n\nPengecoh: difusi menular menyebar ke tempat terdekat lebih dulu. Difusi relokasi terjadi karena pembawa budaya berpindah tempat. Difusi stimulus mengubah bentuk unsur budaya. Difusi balik berarti tren dari kota kecil naik ke kota besar.",
      f_hier),
    Q("Perhatikan komposisi bahasa ibu penduduk Kabupaten K berikut. IKL = 1 − Σpᵢ².\n\nNilai indeks keragaman linguistik (IKL) Kabupaten K adalah …",
      ["0,62", "0,38", "0,67", "0,50", "0,80"],
      "1) Ubah ke proporsi desimal: pA = 0,5; pB = 0,3; pC = 0,2.\n2) Σpᵢ² = 0,25 + 0,09 + 0,04 = 0,38.\n3) IKL = 1 − 0,38 = 0,62.\nArtinya peluang dua penduduk yang dipilih acak memiliki bahasa ibu berbeda adalah 62%. Sebagai pembanding, IKL maksimum untuk tiga bahasa adalah 1 − 1/3 ≈ 0,67, yang tercapai bila ketiga bahasa berproporsi sama. Jadi Kabupaten K cukup beragam, tetapi masih didominasi bahasa A.\n\nPengecoh: 0,38 adalah indeks dominasi (Σpᵢ²). 0,67 adalah IKL maksimum. 0,50 hanya proporsi bahasa A. 0,80 adalah 1 − 0,2 (salah konsep).",
      f_ikl1),
    Q("Perhatikan siluet lima negara berikut.\n\nNegara berbentuk menjorok (protruded) dan negara berbentuk berlubang (perforated) berturut-turut ditunjukkan oleh …",
      ["R dan T", "P dan S", "Q dan R", "S dan T", "P dan Q"],
      "Identifikasi bentuk negara:\n• P (Chili): memanjang (elongated), panjang lebih dari 4.000 km tetapi sempit.\n• Q (Polandia): kompak (compact), jarak pusat ke batas relatif sama.\n• R (Thailand): menjorok (protruded/prorupted), memiliki bagian sempit yang menjulur ke selatan di Semenanjung Malaya.\n• S (Filipina): terpecah (fragmented), terdiri atas banyak pulau.\n• T (Afrika Selatan): berlubang (perforated), karena di dalamnya terdapat negara lain, yaitu Lesotho (bagian putih).\nBentuk negara memengaruhi pertahanan, transportasi, dan integrasi nasional. Misalnya bagian menjorok sering sulit dikendalikan dan rawan konflik.\n\nPengecoh: P memanjang, Q kompak, dan S terpecah.",
      f_bentuk),
    Q("Menara Masjid Kudus dibangun dari bata merah dengan bentuk menyerupai candi Hindu-Jawa, tetapi berfungsi sebagai menara masjid. Proses budaya yang tercermin adalah …",
      ["Akulturasi", "Asimilasi", "Amalgamasi", "Segregasi", "Etnosentrisme"],
      "Akulturasi adalah proses ketika dua budaya bertemu dan unsur budaya asing diterima serta diolah ke dalam budaya sendiri tanpa menghilangkan kepribadian budaya asal. Pada Menara Kudus, bentuk arsitektur candi Hindu-Jawa tetap dipertahankan, tetapi fungsinya menjadi bagian dari bangunan masjid. Kedua unsur budaya masih dapat dikenali.\nAsimilasi terjadi bila budaya-budaya melebur menjadi budaya baru dan ciri budaya asal hilang. Amalgamasi adalah perkawinan campuran antarkelompok. Segregasi adalah pemisahan kelompok dalam ruang. Etnosentrisme adalah sikap menilai budaya lain berdasarkan ukuran budaya sendiri.\n\nPengecoh: ciri budaya asal pada Menara Kudus masih jelas, sehingga bukan asimilasi.",
      None),
    Q("Perhatikan grafik bahasa ibu penduduk Kota X menurut kelompok umur berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Terjadi pergeseran bahasa antargenerasi ke bahasa Indonesia", "Bahasa daerah makin kuat pada generasi muda",
       "Penduduk usia tua lebih banyak berbahasa ibu Indonesia", "Proporsi bahasa ibu tidak berubah antarkelompok umur", "Bahasa Indonesia mulai ditinggalkan generasi muda"],
      "Grafik menunjukkan proporsi penduduk berbahasa ibu bahasa daerah turun dari 85% (usia 60+) menjadi hanya 25% (usia 5–14 tahun), sedangkan bahasa Indonesia sebagai bahasa ibu naik dari 15% menjadi 75%. Karena kelompok umur mewakili generasi berbeda, pola ini menunjukkan pergeseran bahasa (language shift) antargenerasi: orang tua makin jarang mewariskan bahasa daerah kepada anak. Penyebabnya antara lain urbanisasi, perkawinan antarsuku, pendidikan, media, dan anggapan bahwa bahasa Indonesia lebih bergengsi. Bila tren berlanjut, bahasa daerah dapat terancam punah.\n\nPengecoh: bahasa daerah justru melemah pada generasi muda. Penduduk tua lebih banyak berbahasa daerah. Proporsi jelas berubah. Bahasa Indonesia justru menguat.",
      f_shift),
    Q("Bahasa Melayu dapat berkembang menjadi dasar bahasa Indonesia terutama karena sejak lama …",
      ["Berfungsi sebagai lingua franca perdagangan di Nusantara", "Dituturkan sebagai bahasa ibu oleh mayoritas penduduk Jawa",
       "Menjadi satu-satunya bahasa resmi kerajaan Majapahit", "Diwajibkan oleh pemerintah kolonial Belanda di seluruh sekolah", "Tidak memiliki dialek dan ragam daerah"],
      "Bahasa Melayu sudah lama berfungsi sebagai lingua franca, yaitu bahasa penghubung antarpenutur bahasa yang berbeda, terutama di pelabuhan dan jalur perdagangan Nusantara sejak masa Sriwijaya. Strukturnya relatif sederhana, tidak mengenal tingkatan bahasa yang rumit seperti bahasa Jawa, dan tidak terikat pada satu suku mayoritas, sehingga lebih mudah diterima semua kelompok. Pada Sumpah Pemuda 1928, bahasa ini dikukuhkan sebagai bahasa persatuan dengan nama bahasa Indonesia.\n\nPengecoh: mayoritas penduduk Jawa berbahasa ibu Jawa. Bahasa resmi Majapahit adalah Jawa Kuno. Belanda tidak mewajibkannya di seluruh sekolah. Bahasa Melayu memiliki banyak dialek.",
      None),
    Q("Perhatikan peta batas darat Indonesia–Papua Nugini berikut.\n\nSegmen X mengikuti garis 141° BT, sedangkan segmen Y berbelok mengikuti Sungai Fly. Klasifikasi segmen X yang paling tepat adalah …",
      ["Batas geometrik yang superimposed oleh kolonial", "Batas alam yang mengikuti punggung pegunungan",
       "Batas budaya yang mengikuti wilayah satu suku", "Batas subsekuen yang mengikuti permukiman padat", "Batas relik yang sudah tidak berfungsi lagi"],
      "Segmen X berupa garis lurus yang mengikuti garis bujur 141° BT, sehingga secara morfologi termasuk batas geometrik (buatan). Secara genetik, batas ini ditetapkan oleh kekuatan kolonial (Belanda, Inggris, dan Jerman pada abad ke-19) tanpa memperhatikan persebaran suku di Pulau Nugini, sehingga termasuk batas superimposed. Akibatnya beberapa kelompok etnis yang berkerabat terpisah oleh batas negara, dan terdapat lintas batas tradisional yang diatur khusus. Segmen Y mengikuti alur Sungai Fly sehingga merupakan batas alam.\n\nPengecoh: X tidak mengikuti punggung pegunungan, wilayah suku, atau permukiman. Batas ini masih berfungsi, sehingga bukan batas relik.",
      f_papua),
    Q("Perhatikan sebaran dua kelompok etnis di Kota S berikut. Indeks disimilaritas D = ½ × Σ|aᵢ/A − bᵢ/B|.\n\nNilai indeks segregasi Kota S adalah …",
      ["0,50", "1,00", "0,25", "0,70", "0,35"],
      "1) Proporsi tiap distrik terhadap total kelompok (A = 1.000; B = 1.000):\n• Distrik 1: 0,6 dan 0,1 → selisih 0,5.\n• Distrik 2: 0,3 dan 0,3 → selisih 0.\n• Distrik 3: 0,1 dan 0,6 → selisih 0,5.\n2) Σ selisih mutlak = 1,0.\n3) D = ½ × 1,0 = 0,50.\nArtinya 50% anggota salah satu kelompok harus pindah distrik agar sebaran kedua kelompok merata. Nilai 0 berarti tidak ada segregasi, 1 berarti terpisah total. Nilai 0,5 menunjukkan segregasi sedang.\n\nPengecoh: 1,00 lupa mengalikan ½. 0,25 dan 0,35 salah hitung. 0,70 adalah jawaban contoh kasus lain.",
      f_seg1),
    Q("Kawasan baru di banyak kota dibangun dengan mal, waralaba, dan perumahan bergaya seragam sehingga hampir tidak bisa dibedakan dari kota lain. Konsep yang menggambarkan gejala ini adalah …",
      ["Ketiadaan tempat (placelessness)", "Rasa tempat (sense of place)", "Topofilia (cinta pada tempat)", "Determinisme lingkungan alam", "Wilayah budaya formal seragam"],
      "Edward Relph memperkenalkan istilah placelessness (ketiadaan tempat) untuk lanskap yang kehilangan keunikan lokal karena standardisasi, misalnya deretan waralaba, mal, bandara, dan perumahan bergaya sama yang ditemukan di mana saja. Gejala ini dipercepat oleh globalisasi dan kapitalisme. Kebalikannya adalah sense of place, yaitu ikatan emosional dan makna khas yang melekat pada suatu tempat. Topofilia (Yi-Fu Tuan) adalah rasa cinta terhadap tempat.\n\nPengecoh: rasa tempat dan topofilia justru menekankan keunikan. Determinisme lingkungan menyatakan alam menentukan budaya. Wilayah formal adalah wilayah dengan ciri seragam yang ditetapkan, bukan konsep hilangnya keunikan.",
      None),
    Q("Pernyataan berikut yang termasuk kekuatan sentrifugal bagi suatu negara adalah …",
      ["Kesenjangan pembangunan yang lebar antarwilayah", "Bahasa nasional yang digunakan bersama", "Sistem transportasi yang menghubungkan pulau",
       "Lambang negara yang dihormati semua kelompok", "Sejarah perjuangan kemerdekaan bersama"],
      "Kekuatan sentrifugal adalah faktor yang cenderung memecah atau melemahkan persatuan negara, misalnya kesenjangan ekonomi antarwilayah, perbedaan agama dan etnis yang dipolitisasi, gerakan separatis, ketidakadilan pembagian sumber daya, dan medan geografis yang memisahkan. Kesenjangan pembangunan dapat memicu rasa ketidakadilan dan tuntutan pemisahan diri.\nSebaliknya, kekuatan sentripetal menyatukan negara, misalnya bahasa nasional, transportasi dan komunikasi yang menghubungkan wilayah, simbol negara, ideologi bersama, dan sejarah perjuangan bersama.\n\nPengecoh: keempat opsi lainnya adalah kekuatan sentripetal.",
      None),
]

P1 = [
    Q("Perhatikan peta persebaran penutur rumpun bahasa Austronesia berikut.\n\nJenis difusi dan bukti yang paling tepat adalah …",
      ["Relokasi; bahasa Malagasi serumpun dengan Ma'anyan", "Hierarki; bahasa menyebar dari kota besar ke desa",
       "Menular; bahasa menyebar lewat media massa modern", "Stimulus; hanya gagasan menulis yang diterima", "Hierarki; penyebaran dipimpin kerajaan kolonial"],
      "Peta menunjukkan penutur Austronesia menyebar dari Taiwan (±3000 SM) ke Filipina, Indonesia, Pasifik, hingga Madagaskar (±500 M). Penyebaran ini terjadi karena penuturnya sendiri berpindah tempat dengan perahu bercadik, sehingga termasuk difusi relokasi (relocation diffusion). Buktinya antara lain bahasa Malagasi di Madagaskar, yang jauh di dekat Afrika, berkerabat paling dekat dengan bahasa Ma'anyan di Kalimantan Selatan–Tengah. Rumpun Austronesia pernah menjadi rumpun bahasa dengan sebaran geografis terluas sebelum ekspansi bangsa Eropa.\n\nPengecoh: tidak ada kota besar, media massa, atau kolonialisme pada masa itu. Difusi stimulus hanya mengambil gagasan, bukan memindahkan bahasa beserta penuturnya.",
      f_austro),
    Q("Sequoyah, tokoh suku Cherokee, melihat orang Eropa menulis lalu menciptakan aksara suku kata sendiri untuk bahasa Cherokee yang bentuknya berbeda dari alfabet Latin. Proses ini adalah contoh difusi …",
      ["Stimulus", "Relokasi", "Hierarki", "Menular", "Ekspansi"],
      "Difusi stimulus terjadi ketika gagasan atau prinsip dasar suatu unsur budaya menyebar dan diterima, tetapi bentuk aslinya ditolak atau diubah sesuai budaya penerima. Sequoyah mengambil gagasan bahwa bahasa dapat ditulis, tetapi menciptakan sistem aksara silabis sendiri yang berbeda dari alfabet Latin. Contoh lain adalah restoran cepat saji yang menyesuaikan menu dengan selera dan aturan lokal.\n\nPengecoh: relokasi memerlukan perpindahan pembawa budaya. Hierarki menyebar menurut ukuran kota. Menular menyebar ke tempat terdekat. Ekspansi adalah istilah umum untuk penyebaran yang memperluas wilayah tanpa pembawanya pindah; yang paling spesifik di sini adalah stimulus.",
      None),
    Q("Perhatikan gambar perubahan lanskap sebuah kawasan di Jawa Barat berikut.\n\nKonsep yang paling tepat menggambarkan rangkaian perubahan tersebut adalah …",
      ["Sekuen okupansi Whittlesey", "Determinisme lingkungan", "Difusi stimulus antarbudaya", "Ketiadaan tempat (placelessness)", "Batas budaya superimposed"],
      "Sekuen okupansi (Derwent Whittlesey, 1929) adalah konsep bahwa suatu tempat dihuni berturut-turut oleh kelompok atau sistem budaya yang berbeda, dan masing-masing meninggalkan jejak pada lanskap budaya. Gambar menunjukkan tiga lapisan: hutan dan kampung adat (±1800), perkebunan teh kolonial dengan rel lori (±1900), lalu permukiman kota, jalan raya, dan ruko (±2010). Jejak tahap sebelumnya, misalnya pola jalan bekas rel atau nama tempat, sering masih terlihat seperti palimpsest.\n\nPengecoh: determinisme menyatakan alam menentukan budaya. Difusi stimulus berkaitan dengan penyebaran gagasan. Placelessness adalah hilangnya keunikan tempat. Batas superimposed adalah konsep batas negara.",
      f_sekuen),
    Q("Perhatikan grafik delapan bahasa dengan penutur bahasa ibu terbanyak berikut.\n\nBanyaknya bahasa pada grafik yang termasuk rumpun Indo-Eropa adalah …",
      ["6 bahasa", "4 bahasa", "5 bahasa", "7 bahasa", "3 bahasa"],
      "Klasifikasi rumpun bahasa:\n• Indo-Eropa: Spanyol, Inggris, Portugis (cabang Roman/Jermanik), Hindi dan Bengali (cabang Indo-Arya), serta Rusia (cabang Slavia) → 6 bahasa.\n• Sino-Tibet: Mandarin.\n• Japonik: Jepang.\nRumpun Indo-Eropa memiliki penutur terbanyak di dunia karena persebaran awalnya dari sekitar Laut Hitam ke Eropa dan Asia Selatan, kemudian diperluas oleh kolonialisme Eropa ke Amerika, Afrika, dan Oseania.\n\nPengecoh: Hindi dan Bengali sering terlupa sebagai Indo-Eropa, sedangkan Jepang dan Mandarin bukan Indo-Eropa.",
      f_rumpun),
    Q("Tok Pisin di Papua Nugini berawal dari bahasa campuran sederhana untuk berdagang, kemudian dipelajari anak-anak sebagai bahasa ibu dan tata bahasanya menjadi lengkap. Saat ini Tok Pisin termasuk …",
      ["Bahasa kreol", "Bahasa pijin", "Bahasa isolat", "Dialek lokal", "Bahasa mati"],
      "Pijin (pidgin) adalah bahasa campuran sederhana yang muncul dari kontak antarkelompok berbeda bahasa, misalnya untuk berdagang. Pijin tidak memiliki penutur asli dan tata bahasanya terbatas. Ketika pijin dipelajari generasi berikutnya sebagai bahasa ibu, kosakata dan tata bahasanya berkembang lengkap, sehingga menjadi bahasa kreol. Tok Pisin kini dituturkan sebagai bahasa ibu oleh banyak warga perkotaan Papua Nugini dan menjadi salah satu bahasa resminya.\n\nPengecoh: pijin belum memiliki penutur asli. Bahasa isolat tidak berkerabat dengan bahasa lain. Dialek adalah variasi satu bahasa. Bahasa mati tidak lagi dituturkan.",
      None),
    Q("Perhatikan sketsa rumah tradisional berikut.\n\nFungsi ciri 1, 2, dan 3 sebagai bentuk adaptasi lingkungan berturut-turut adalah …",
      ["Mengalirkan hujan, sirkulasi udara, menghindari banjir", "Menahan panas, menahan angin, mempercepat banjir",
       "Menampung salju, mencegah cahaya, menahan gempa", "Menyimpan air, menahan debu, mengundang satwa", "Mengurangi hujan, menutup udara, menahan pasang"],
      "Rumah panggung tradisional di dataran rendah pesisir Sumatra beradaptasi dengan iklim tropis basah:\n1) Atap curam dan lebar: mempercepat aliran air hujan yang deras dan melindungi dinding dari tempias serta panas matahari.\n2) Dinding anyaman berongga: memungkinkan sirkulasi udara sehingga rumah tetap sejuk di udara panas dan lembap.\n3) Tiang tinggi (kolong): melindungi dari banjir atau pasang, kelembapan tanah, dan binatang buas; kolong juga dipakai untuk menyimpan barang atau ternak.\nArsitektur vernakular seperti ini menunjukkan hubungan erat antara budaya material dan lingkungan, sesuai pandangan posibilisme.\n\nPengecoh: opsi lain bertentangan dengan fungsi ciri-ciri tersebut di iklim tropis basah.",
      f_rumah),
    Q("Perhatikan proporsi penutur bahasa ibu di dua kabupaten berikut. IKL = 1 − Σpᵢ².\n\nPernyataan yang tepat adalah …",
      ["IKL M = 0,75 lebih tinggi daripada IKL N = 0,48", "IKL M = 0,25 lebih rendah daripada IKL N = 0,52", "IKL kedua kabupaten sama karena ada empat bahasa",
       "IKL N = 0,75 lebih tinggi daripada IKL M = 0,48", "IKL M = 1,00 karena semua bahasa sama besar"],
      "• Kabupaten M: Σp² = 4 × 0,25² = 4 × 0,0625 = 0,25 → IKL = 1 − 0,25 = 0,75.\n• Kabupaten N: Σp² = 0,7² + 3 × 0,1² = 0,49 + 0,03 = 0,52 → IKL = 1 − 0,52 = 0,48.\nKabupaten M mencapai IKL maksimum untuk empat bahasa (1 − 1/4 = 0,75) karena proporsinya sama besar. Kabupaten N didominasi satu bahasa (70%), sehingga keragamannya lebih rendah walaupun jumlah bahasanya sama. Jadi keragaman tidak hanya bergantung pada jumlah bahasa, tetapi juga pemerataan proporsinya.\n\nPengecoh: 0,25 dan 0,52 adalah indeks dominasi. IKL kedua kabupaten berbeda. Nilai M dan N tertukar pada salah satu opsi. IKL tidak mungkin 1 untuk jumlah bahasa terbatas.",
      f_ikl2),
    Q("Pegunungan Tengah Papua memiliki ratusan bahasa yang berbeda dalam wilayah relatif sempit. Penjelasan geografis yang paling tepat adalah …",
      ["Medan terjal mengisolasi kelompok dalam waktu lama", "Penduduknya baru datang pada abad ke-20 dari Eropa",
       "Wilayah tersebut merupakan pusat perdagangan internasional", "Semua kelompok memakai satu bahasa resmi sejak lama", "Iklimnya kering sehingga penduduk sering berpindah jauh"],
      "Papua (termasuk Papua Nugini) adalah wilayah dengan keragaman bahasa tertinggi di dunia. Pegunungan tinggi, lembah dalam, sungai deras, dan hutan lebat menyulitkan perjalanan, sehingga kelompok-kelompok penduduk hidup relatif terisolasi selama ribuan tahun. Isolasi geografis menyebabkan bahasa berkembang terpisah dan berbeda-beda. Pertanian ubi jalar yang memadai di lembah juga memungkinkan kelompok hidup mandiri tanpa perlu banyak berinteraksi. Wilayah seperti ini sering disebut daerah perlindungan (refuge area) bagi bahasa.\n\nPengecoh: penduduk Papua sudah ada puluhan ribu tahun. Wilayah ini bukan pusat perdagangan internasional. Banyaknya bahasa justru menunjukkan tidak ada satu bahasa bersama. Iklimnya basah, bukan kering.",
      None),
    Q("Perhatikan beberapa toponim di Indonesia berikut.\n\nPasangan toponim yang unsur namanya sama-sama menunjukkan tempat pertemuan sungai dengan sungai lain atau laut adalah …",
      ["1 dan 2", "3 dan 4", "1 dan 3", "2 dan 5", "4 dan 5"],
      "Toponimi (ilmu tentang nama tempat) sering mencerminkan kondisi geografis dan bahasa penghuni awal:\n• Kuala: muara sungai atau pertemuan sungai (Melayu) → Kuala Tungkal.\n• Muara: tempat sungai bermuara ke sungai lain atau laut → Muara Enim, tempat Sungai Enim bertemu Sungai Lematang.\n• Tanjung: daratan yang menjorok ke laut.\n• Teluk: laut yang menjorok ke daratan.\n• Gunung: bentuk lahan tinggi (Gunung Sitoli di Pulau Nias).\nJadi unsur yang sama-sama menunjukkan pertemuan sungai adalah kuala (1) dan muara (2).\n\nPengecoh: tanjung, teluk, dan gunung menunjukkan bentuk lahan pesisir atau tinggi, bukan pertemuan sungai.",
      f_topo),
    Q("Restoran cepat saji asal Amerika Serikat di Indonesia menjual paket nasi dengan ayam berbumbu lokal dan memakai sertifikat halal. Gejala ini disebut …",
      ["Glokalisasi", "Asimilasi", "Placelessness", "Segregasi", "Iredentisme"],
      "Glokalisasi (glocalization) adalah penyesuaian produk atau budaya global dengan selera, nilai, dan aturan lokal agar diterima masyarakat setempat. Restoran waralaba global menambahkan menu nasi, sambal, dan bumbu lokal serta memastikan kehalalan bagi konsumen Muslim. Gejala ini menunjukkan bahwa globalisasi tidak selalu menyeragamkan budaya, karena budaya lokal ikut membentuk produk global.\n\nPengecoh: asimilasi adalah peleburan budaya hingga ciri asal hilang. Placelessness adalah hilangnya keunikan tempat. Segregasi adalah pemisahan kelompok. Iredentisme adalah tuntutan wilayah berdasarkan kesamaan etnis.",
      None),
]

P2 = [
    Q("Perhatikan diagram komposisi penduduk Indonesia menurut agama berikut. Jika jumlah penduduk 280 juta jiwa, jumlah penganut Hindu sekitar …",
      ["4,8 juta jiwa", "1,7 juta jiwa", "8,7 juta jiwa", "2,8 juta jiwa", "47,6 juta jiwa"],
      "Jumlah penganut Hindu = 1,7% × 280 juta = 0,017 × 280 juta ≈ 4,76 juta ≈ 4,8 juta jiwa.\nSebagian besar penganut Hindu terkonsentrasi di Bali, dan sisanya di Lampung, NTB (Lombok), Sulawesi Tengah, serta daerah transmigrasi asal Bali. Persebaran ini menunjukkan agama dapat terkonsentrasi secara regional, misalnya mayoritas Kristen di NTT, Papua, dan Sulawesi Utara, serta mayoritas Islam di sebagian besar Sumatra dan Jawa.\n\nPengecoh: 1,7 juta salah membaca persen sebagai juta. 8,7 juta, 2,8 juta, dan 47,6 juta adalah kesalahan perhitungan desimal.",
      f_agama),
    Q("Perhatikan peta beberapa negara di Semenanjung Balkan berikut.\n\nNegara yang mayoritas penduduknya beragama Katolik dan negara yang mayoritas penduduknya Kristen Ortodoks Serbia berturut-turut adalah …",
      ["P dan Q", "Q dan P", "R dan S", "S dan T", "P dan R"],
      "Negara pada peta:\n• P – Kroasia: mayoritas Katolik Roma, beraksara Latin.\n• Q – Serbia: mayoritas Kristen Ortodoks Serbia, beraksara Sirilik dan Latin.\n• R – Bosnia dan Herzegovina: campuran, yaitu Bosniak (Islam), Serbia (Ortodoks), dan Kroasia (Katolik).\n• S – Albania: mayoritas Islam, bahasanya bukan Slavia.\n• T – Yunani: mayoritas Ortodoks Yunani.\nBalkan disebut shatter belt karena keragaman agama, bahasa, dan etnis yang dipengaruhi Kekaisaran Romawi Barat dan Timur serta Kesultanan Utsmaniyah. Perbedaan identitas ini menjadi salah satu faktor pecahnya Yugoslavia dan konflik 1990-an (balkanisasi).\n\nPengecoh: urutan Q–P tertukar. R campuran. S mayoritas Islam. T Ortodoks Yunani.",
      f_balkan),
    Q("Kelompok agama yang semuanya termasuk agama etnis (bukan agama universal) adalah …",
      ["Hindu, Yahudi, dan Shinto", "Islam, Kristen, dan Buddha", "Kristen, Hindu, dan Islam", "Buddha, Shinto, dan Islam", "Yahudi, Kristen, dan Buddha"],
      "Agama universal (universalizing) berusaha menyebarkan ajarannya kepada semua manusia tanpa memandang suku atau tempat, misalnya Islam, Kristen, dan Buddha. Persebarannya sangat luas karena dakwah dan misi.\nAgama etnis (ethnic) terkait erat dengan satu kelompok etnis atau wilayah tertentu, umumnya tidak aktif mencari penganut baru, dan ajarannya sering berkaitan dengan lanskap fisik setempat. Contohnya Hindu (terutama di India, Nepal, dan Bali), Yahudi, dan Shinto (Jepang).\n\nPengecoh: setiap opsi lain mengandung setidaknya satu agama universal.",
      None),
    Q("Perhatikan peta persentase petani yang memakai teknik budidaya baru berikut.\n\nPola tersebut paling tepat dijelaskan oleh …",
      ["Difusi menular dengan peluruhan jarak", "Difusi hierarki dari kota besar", "Difusi relokasi oleh petani pendatang",
       "Difusi stimulus dengan bentuk yang diubah", "Persebaran acak tanpa pengaruh jarak"],
      "Peta menunjukkan adopsi tertinggi (90%) di sekitar desa asal, lalu menurun teratur menjadi 60%, 30%, dan 10% seiring bertambahnya jarak. Pola ini adalah difusi menular (contagious diffusion), yaitu penyebaran dari orang ke orang melalui kontak langsung, sehingga tempat terdekat mengadopsi lebih dulu dan lebih banyak. Penurunan adopsi dengan jarak disebut peluruhan jarak (distance decay). Torsten Hägerstrand memodelkan proses ini untuk penyebaran inovasi pertanian di Swedia.\n\nPengecoh: tidak ada lompatan ke kota besar (hierarki). Penyebar tidak berpindah tempat (relokasi). Bentuk inovasi tidak diubah (stimulus). Pola jelas dipengaruhi jarak.",
      f_menular),
    Q("Perhatikan grafik kuota haji beberapa negara berikut. Kuota haji ditetapkan sekitar 1 orang per 1.000 penduduk Muslim. Perkiraan jumlah penduduk Muslim Pakistan adalah …",
      ["179 juta jiwa", "17,9 juta jiwa", "1,79 miliar jiwa", "221 juta jiwa", "179 ribu jiwa"],
      "Kuota = penduduk Muslim ÷ 1.000, sehingga penduduk Muslim = kuota × 1.000.\nPakistan: 179 ribu × 1.000 = 179.000.000 ≈ 179 juta jiwa.\nGrafik juga menunjukkan Indonesia memperoleh kuota terbesar karena merupakan negara dengan penduduk Muslim terbanyak di dunia. Ibadah haji adalah contoh sirkulasi religius (ziarah) berskala global yang menghubungkan Makkah dengan dunia Muslim, berdampak pada transportasi, ekonomi, dan pertukaran budaya.\n\nPengecoh: 17,9 juta dan 179 ribu salah mengalikan. 1,79 miliar terlalu besar. 221 juta adalah perkiraan untuk Indonesia.",
      f_haji),
    Q("Perhatikan diagram kekerabatan sebuah keluarga Minangkabau berikut.\n\nDalam sistem matrilineal, individu yang sesuku dengan Nenek adalah …",
      ["Ibu, mamak, ego, dan adik ego", "Ayah, ego, dan anak-anak mamak", "Hanya ego dan adik perempuannya", "Mamak dan anak-anak mamak saja",
       "Semua orang yang ada di diagram"],
      "Dalam sistem kekerabatan matrilineal Minangkabau, keanggotaan suku diturunkan melalui garis ibu. Karena itu:\n• Ibu dan mamak (saudara laki-laki ibu) sesuku dengan nenek karena keduanya anak nenek.\n• Ego dan adik ego sesuku dengan nenek karena mengikuti suku ibunya.\n• Ayah dan istri mamak berasal dari suku lain karena perkawinan harus dengan suku berbeda (eksogami).\n• Anak-anak mamak mengikuti suku ibu mereka (istri mamak), sehingga tidak sesuku dengan nenek.\nMamak tetap berperan penting membimbing kemenakan (anak saudara perempuannya). Harta pusaka tinggi seperti rumah gadang dan sawah diwariskan kepada perempuan sesuku.\n\nPengecoh: ayah dan anak-anak mamak berasal dari suku lain.",
      f_matri),
    Q("Di Bali, tata ruang pekarangan dan desa mengikuti arah kaja (ke arah gunung) yang dianggap suci dan kelod (ke arah laut) yang dianggap kurang suci. Konsep geografi budaya yang tercermin adalah …",
      ["Lanskap religius dan ruang suci", "Difusi hierarki dari budaya kota", "Sekuen okupansi masa kolonial", "Batas negara yang superimposed", "Bahasa kreol masyarakat pesisir"],
      "Lanskap religius adalah jejak keyakinan agama pada ruang dan lanskap. Dalam budaya Hindu Bali, gunung, terutama Gunung Agung, dipandang sebagai tempat bersemayam para dewa sehingga arah kaja dianggap suci. Pura keluarga (sanggah atau merajan) diletakkan di sisi kaja, sedangkan dapur, kandang, dan tempat pembuangan di sisi kelod. Desa juga ditata dengan pura desa di hulu dan pura dalem serta kuburan di hilir. Konsep ini sejalan dengan filosofi Tri Hita Karana, yaitu keharmonisan manusia dengan Tuhan, sesama, dan alam.\n\nPengecoh: difusi hierarki, sekuen okupansi, batas negara, dan bahasa kreol tidak terkait dengan orientasi ruang suci.",
      None),
    Q("Tradisi yang memadukan unsur kepercayaan lokal, Hindu-Buddha, dan Islam menjadi satu sistem keyakinan dan ritual baru, seperti kejawen, disebut …",
      ["Sinkretisme", "Asimilasi", "Akulturasi", "Segregasi", "Amalgamasi"],
      "Sinkretisme adalah percampuran unsur-unsur dari berbagai sistem kepercayaan atau agama menjadi satu sistem keyakinan dan praktik ritual baru. Kejawen memadukan kepercayaan Jawa asli, unsur Hindu-Buddha, dan tasawuf Islam. Sinkretisme berbeda dari akulturasi, yang lebih menekankan penerimaan unsur budaya asing tanpa menghilangkan kepribadian budaya sendiri, umumnya pada aspek seni, arsitektur, atau tradisi. Sinkretisme khusus menyangkut perpaduan sistem keyakinan.\n\nPengecoh: asimilasi adalah peleburan budaya kelompok. Akulturasi tidak menekankan perpaduan sistem keyakinan. Segregasi adalah pemisahan. Amalgamasi adalah perkawinan campur.",
      None),
    Q("Perhatikan grafik minat warganet Indonesia terhadap budaya pop Korea berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Minat melonjak hingga 2020, wujud difusi budaya global", "Minat menurun terus sejak 2012", "Minat tidak berubah selama sepuluh tahun",
       "Minat naik karena perpindahan penduduk Korea ke Indonesia", "Minat tertinggi terjadi pada 2012"],
      "Grafik menunjukkan indeks minat naik dari 22 (2012) menjadi 92 (2020), lalu sedikit turun menjadi 88 (2022). Lonjakan ini menggambarkan gelombang Korea (hallyu), yaitu penyebaran budaya populer Korea Selatan seperti musik K-pop, drama, kuliner, dan kosmetik ke seluruh dunia. Penyebarannya didorong media digital, platform streaming, dan media sosial, sehingga tidak memerlukan perpindahan penduduk. Pemerintah Korea juga memanfaatkannya sebagai soft power dan diplomasi budaya. Lonjakan tertinggi pada 2020 bertepatan dengan masa pandemi ketika konsumsi hiburan daring meningkat.\n\nPengecoh: minat naik, bukan turun atau tetap. Penyebaran tidak memerlukan migrasi penduduk Korea. Nilai 2012 justru terendah.",
      f_hallyu),
    Q("Program pemerintah yang mempromosikan rendang, gamelan, dan batik ke mancanegara untuk meningkatkan citra dan pengaruh Indonesia merupakan contoh …",
      ["Diplomasi budaya", "Iredentisme wilayah", "Devolusi kekuasaan", "Segregasi kelompok etnis", "Balkanisasi negara"],
      "Diplomasi budaya adalah pemanfaatan unsur budaya seperti kuliner, seni, bahasa, dan warisan budaya untuk membangun citra positif dan pengaruh suatu negara di dunia internasional. Pengaruh yang diperoleh melalui daya tarik budaya disebut soft power (Joseph Nye), berbeda dari hard power yang bertumpu pada kekuatan militer dan ekonomi. Contoh di Indonesia adalah gastrodiplomasi rendang, pengajaran bahasa Indonesia bagi penutur asing (BIPA), serta beasiswa seni budaya.\n\nPengecoh: iredentisme adalah tuntutan wilayah. Devolusi adalah penyerahan kewenangan. Segregasi adalah pemisahan kelompok. Balkanisasi adalah pecahnya negara menjadi negara kecil.",
      None),
]

P3 = [
    Q("Perhatikan peta wilayah persebaran kelompok etnis X yang tersebar di Turki, Suriah, Irak, dan Iran berikut. Kelompok X memiliki bahasa dan identitas bersama, tetapi tidak memiliki negara sendiri.\n\nKelompok X merupakan contoh …",
      ["Bangsa tanpa negara (stateless)", "Negara-bangsa (nation-state)", "Negara multinasional yang merdeka", "Enklave milik negara Turki", "Wilayah vernakular perkotaan"],
      "Kelompok X adalah bangsa Kurdi, dengan populasi sekitar 30–40 juta jiwa yang tersebar di wilayah pegunungan perbatasan Turki, Irak, Iran, dan Suriah. Mereka memiliki bahasa, budaya, dan kesadaran sebagai satu bangsa, tetapi tidak memiliki negara berdaulat sendiri, sehingga disebut bangsa tanpa negara. Wilayah mereka terbagi oleh batas negara yang ditetapkan setelah Perang Dunia I (Perjanjian Sykes–Picot dan Lausanne). Kondisi ini memicu tuntutan otonomi dan konflik. Irak memberikan otonomi khusus kepada Kurdistan Irak.\n\nPengecoh: negara-bangsa adalah negara yang wilayahnya sesuai dengan satu bangsa. Kurdi tidak memiliki negara multinasional sendiri. Wilayah X bukan enklave atau wilayah vernakular kota.",
      f_kurdi),
    Q("Jepang dan Islandia sering dijadikan contoh negara yang penduduknya sangat didominasi satu kelompok etnis dan bahasa yang sama. Negara seperti ini disebut …",
      ["Negara-bangsa (nation-state)", "Negara multinasional besar", "Bangsa tanpa negara sendiri", "Negara berbentuk menjorok", "Negara terkurung daratan"],
      "Negara-bangsa (nation-state) adalah negara yang batas wilayahnya kurang lebih sesuai dengan persebaran satu bangsa yang memiliki bahasa, budaya, dan identitas bersama. Jepang, Islandia, dan Korea Selatan sering dijadikan contoh mendekati negara-bangsa ideal. Sebaliknya, negara multinasional seperti Indonesia, India, dan Rusia memiliki banyak kelompok bangsa atau etnis dalam satu negara, sehingga memerlukan kekuatan sentripetal kuat untuk menjaga persatuan.\n\nPengecoh: negara multinasional memiliki banyak bangsa. Bangsa tanpa negara tidak memiliki negara. Bentuk menjorok dan terkurung daratan berkaitan dengan bentuk dan letak negara, bukan komposisi etnis. Jepang dan Islandia juga berupa kepulauan, bukan daratan tertutup.",
      None),
    Q("Perhatikan komposisi etnis penduduk Provinsi E berikut. Indeks fraksionalisasi F = 1 − Σsᵢ².\n\nNilai indeks fraksionalisasi etnis Provinsi E adalah …",
      ["0,72", "0,28", "0,75", "0,60", "0,85"],
      "1) Proporsi: 0,40; 0,25; 0,20; 0,15.\n2) Σs² = 0,16 + 0,0625 + 0,04 + 0,0225 = 0,285.\n3) F = 1 − 0,285 = 0,715 ≈ 0,72.\nArtinya peluang dua penduduk acak berasal dari etnis berbeda sekitar 72%. Nilai maksimum untuk empat kelompok adalah 1 − 1/4 = 0,75. Jadi Provinsi E sangat beragam. Indeks ini sering dikaitkan dengan tantangan tata kelola, karena keragaman tinggi memerlukan kebijakan yang adil dan inklusif agar tidak memicu konflik.\n\nPengecoh: 0,28 adalah Σs² (indeks dominasi). 0,75 adalah nilai maksimum. 0,60 adalah 1 − 0,40. 0,85 adalah 1 − 0,15 (salah konsep).",
      f_etnis),
    Q("Perhatikan faktor-faktor yang memengaruhi keutuhan negara berikut.\n\nFaktor yang termasuk kekuatan sentrifugal adalah …",
      ["2, 4, dan 6", "1, 3, dan 5", "1, 2, dan 3", "4, 5, dan 6", "2, 3, dan 4"],
      "Kekuatan sentrifugal melemahkan atau memecah negara, sedangkan kekuatan sentripetal mempersatukan.\n• Sentrifugal: (2) kesenjangan ekonomi antarwilayah yang lebar memicu rasa tidak adil; (4) gerakan separatis bersenjata secara langsung mengancam keutuhan wilayah; (6) politisasi identitas kesukuan memperuncing perbedaan antarkelompok.\n• Sentripetal: (1) bahasa nasional bersama; (3) ideologi dan simbol negara yang diterima bersama, misalnya Pancasila dan Garuda; (5) sistem pendidikan nasional yang menanamkan identitas bersama.\nKeutuhan negara bergantung pada keseimbangan kedua kekuatan tersebut.\n\nPengecoh: opsi lain mencampur faktor sentripetal dan sentrifugal.",
      f_faktor),
    Q("Pemerintah pusat memberikan kewenangan lebih luas kepada Aceh dan Papua melalui otonomi khusus tanpa melepaskan wilayah tersebut dari negara. Proses ini disebut …",
      ["Devolusi", "Secesi", "Iredentisme", "Aneksasi", "Balkanisasi"],
      "Devolusi adalah pengalihan sebagian kewenangan dari pemerintah pusat kepada pemerintah daerah atau regional, sementara wilayah tersebut tetap menjadi bagian negara. Devolusi sering dipakai untuk meredam tuntutan separatis dengan mengakomodasi identitas regional, misalnya otonomi khusus Aceh (termasuk penerapan syariat Islam dan partai lokal), Papua, keistimewaan Yogyakarta, serta parlemen Skotlandia di Inggris.\n\nPengecoh: secesi adalah pemisahan diri menjadi negara baru, misalnya Timor-Leste dan Sudan Selatan. Iredentisme adalah tuntutan bergabungnya wilayah berpenduduk sebangsa. Aneksasi adalah pencaplokan wilayah. Balkanisasi adalah pecahnya negara menjadi negara-negara kecil yang saling bermusuhan.",
      None),
    Q("Perhatikan klasifikasi genetik batas negara berikut.\n\nBatas antara Provinsi NTT dan Timor-Leste di Pulau Timor ditetapkan melalui perjanjian Portugis–Belanda dan memotong wilayah suku Tetun serta Atoni. Batas tersebut termasuk jenis …",
      ["R, superimposed", "P, anteseden", "Q, subsekuen", "S, relik", "P dan S sekaligus"],
      "Klasifikasi genetik (asal-usul) batas negara:\n• P – anteseden: ditarik sebelum wilayah dihuni padat, misalnya batas AS–Kanada di 49° LU bagian barat.\n• Q – subsekuen (atau konsekuen): ditarik setelah permukiman berkembang dan mengikuti batas budaya.\n• R – superimposed: dipaksakan kekuatan luar, biasanya kolonial, tanpa memperhatikan persebaran budaya penduduk.\n• S – relik: batas yang sudah tidak berfungsi tetapi jejaknya masih terlihat, misalnya bekas Tembok Berlin.\nBatas di Pulau Timor ditetapkan oleh Portugis dan Belanda (perjanjian 1859 dan 1914) dan memotong wilayah suku Tetun dan Atoni, sehingga termasuk superimposed. Batas ini kemudian menjadi batas Indonesia–Timor-Leste.\n\nPengecoh: wilayah Timor sudah dihuni (bukan anteseden), batasnya tidak mengikuti budaya (bukan subsekuen), dan masih berfungsi (bukan relik).",
      f_batas),
    Q("Pada akhir abad ke-20, sebagian kelompok di negara tetangga menuntut agar wilayah yang dihuni kelompok sebangsa di negara lain digabungkan ke negaranya. Gerakan seperti ini disebut …",
      ["Iredentisme", "Devolusi", "Glokalisasi", "Akulturasi", "Desentralisasi"],
      "Iredentisme adalah gerakan atau tuntutan untuk menggabungkan wilayah di negara lain yang dihuni oleh kelompok etnis sebangsa dengan negaranya. Istilah ini berasal dari gerakan Italia irredenta (Italia yang belum dibebaskan) pada abad ke-19. Contohnya tuntutan sebagian kelompok Serbia atas wilayah berpenduduk Serbia di Bosnia dan Kroasia pada 1990-an. Iredentisme sering menjadi sumber konflik antarnegara.\n\nPengecoh: devolusi dan desentralisasi adalah penyerahan kewenangan dalam negara. Glokalisasi adalah penyesuaian budaya global dengan budaya lokal. Akulturasi adalah percampuran budaya.",
      None),
    Q("Perhatikan data luas dan panjang batas tiga negara berikut. Panjang batas relatif = panjang batas ÷ √luas.\n\nNegara dengan bentuk paling tidak kompak beserta nilainya adalah …",
      ["Negara B, sekitar 12,5", "Negara A, sekitar 4,0", "Negara C, sekitar 5,0", "Negara B, sekitar 31,3", "Negara C, sekitar 8,3"],
      "Hitung panjang batas relatif:\n• A: 2.000 ÷ √250.000 = 2.000 ÷ 500 = 4,0.\n• B: 5.000 ÷ √160.000 = 5.000 ÷ 400 = 12,5.\n• C: 3.000 ÷ √360.000 = 3.000 ÷ 600 = 5,0.\nSemakin besar nilainya, semakin panjang batas dibandingkan luas wilayah, sehingga bentuk negara semakin tidak kompak, misalnya memanjang, menjorok, atau berbatas berkelok. Negara B paling tidak kompak, sedangkan A paling kompak. Negara kompak lebih mudah dipertahankan dan dihubungkan dengan transportasi.\n\nPengecoh: A dan C lebih kompak. 31,3 membagi panjang batas dengan luas lalu dikali seribu. 8,3 adalah salah hitung.",
      f_kompak),
    Q("Peristiwa Sumpah Pemuda 1928 yang menyatakan satu tanah air, satu bangsa, dan menjunjung bahasa persatuan Indonesia berperan sebagai …",
      ["Kekuatan sentripetal pembentuk nasionalisme", "Kekuatan sentrifugal yang memecah wilayah", "Contoh secesi wilayah dari Hindia Belanda",
       "Contoh devolusi kewenangan kepada daerah", "Contoh iredentisme terhadap negara tetangga"],
      "Sumpah Pemuda mempersatukan pemuda dari berbagai organisasi kedaerahan, seperti Jong Java, Jong Sumatranen Bond, Jong Celebes, dan Jong Ambon, dalam satu identitas kebangsaan Indonesia. Pengakuan satu tanah air, satu bangsa, dan bahasa persatuan menjadi kekuatan sentripetal yang menumbuhkan nasionalisme, yaitu kesadaran sebagai satu bangsa yang melampaui identitas suku, agama, dan daerah. Nasionalisme ini menjadi dasar terbentuknya negara Indonesia pada 1945.\n\nPengecoh: Sumpah Pemuda justru mempersatukan, bukan memecah. Peristiwa ini bukan pemisahan wilayah, penyerahan kewenangan, atau tuntutan atas wilayah negara lain.",
      None),
    Q("Perhatikan peta Pulau Timor berikut.\n\nWilayah X (Oecusse) adalah bagian Timor-Leste yang seluruhnya dikelilingi wilayah Indonesia dan laut. Bagi Timor-Leste, wilayah X disebut …",
      ["Eksklave", "Enklave", "Negara berlubang", "Zona penyangga", "Batas relik"],
      "Eksklave adalah bagian wilayah suatu negara yang terpisah dari wilayah utamanya dan dikelilingi wilayah negara lain (atau negara lain dan laut). Oecusse adalah eksklave Timor-Leste di dalam wilayah NTT, Indonesia. Dari sudut pandang Indonesia, Oecusse adalah enklave, yaitu wilayah negara lain yang berada di dalam wilayahnya. Pembedaannya bergantung pada sudut pandang negara. Keberadaan eksklave menimbulkan tantangan seperti akses transportasi, perlintasan batas, dan pelayanan publik.\n\nPengecoh: enklave adalah sudut pandang Indonesia, bukan Timor-Leste. Negara berlubang adalah negara yang dikelilingi negara lain, misalnya Lesotho di Afrika Selatan. Zona penyangga dan batas relik adalah konsep lain.",
      f_timor),
]

P4 = [
    Q("Perhatikan pola tata ruang inti kota kerajaan Islam di Jawa berikut.\n\nMasjid agung pada pola ini umumnya terletak di posisi …",
      ["P, sisi barat alun-alun", "Q, sisi utara alun-alun", "R, sisi timur alun-alun", "S, di dalam keraton", "Di tengah alun-alun"],
      "Kota-kota kerajaan Islam di Jawa, seperti Yogyakarta, Surakarta, dan Cirebon, umumnya mengikuti pola catur gatra tunggal: keraton (pusat pemerintahan) di selatan, alun-alun sebagai ruang publik di depannya, masjid agung di sisi barat alun-alun, dan pasar di sisi utara atau timur laut. Letak masjid di barat berkaitan dengan arah kiblat dan simbol kesatuan kekuasaan raja dengan agama. Pola ini adalah contoh lanskap budaya yang mencerminkan sistem kepercayaan dan politik, sekaligus akulturasi tata ruang Hindu-Jawa dengan Islam.\n\nPengecoh: utara dan timur biasanya untuk pasar atau bangunan pemerintahan. Masjid agung berada di luar keraton dan tidak di tengah alun-alun.",
      f_kota),
    Q("Perhatikan silsilah beberapa aksara Nusantara berikut.\n\nBerdasarkan asal-usulnya dari aksara Brahmi, aksara-aksara tersebut termasuk tipe sistem tulisan …",
      ["Abugida", "Abjad", "Alfabet", "Logogram", "Piktogram"],
      "Aksara turunan Brahmi, termasuk Pallawa, Kawi, Jawa, Bali, Sunda, Batak, dan Lontara, termasuk abugida (aksara silabis turunan India). Setiap huruf dasar melambangkan konsonan dengan vokal bawaan /a/, misalnya ha, na, ca, ra, ka, dan vokal lain ditulis dengan tanda diakritik (sandhangan) yang melekat pada huruf dasar.\nBandingkan dengan abjad (Arab, Ibrani) yang hanya menulis konsonan, alfabet (Latin, Yunani, Sirilik) yang menulis konsonan dan vokal sebagai huruf terpisah, serta logogram (aksara Han/Tionghoa) yang tiap tandanya mewakili kata atau morfem.\n\nPengecoh: aksara Nusantara turunan Brahmi bukan abjad, alfabet, logogram, atau piktogram.",
      f_aksara),
    Q("Aksara Arab yang disesuaikan untuk menulis bahasa Melayu (Jawi) dan bahasa Jawa (Pegon) pada dasarnya termasuk tipe sistem tulisan …",
      ["Abjad", "Abugida", "Alfabet", "Logogram", "Silabari"],
      "Aksara Arab adalah abjad, yaitu sistem tulisan yang lambang dasarnya mewakili konsonan, sedangkan vokal ditulis dengan tanda baris (harakat) yang sering dihilangkan. Ketika diadaptasi menjadi Jawi untuk bahasa Melayu dan Pegon untuk bahasa Jawa dan Sunda, ditambahkan beberapa huruf untuk bunyi yang tidak ada dalam bahasa Arab, misalnya ca, nga, pa, ga, dan nya. Persebaran aksara Jawi dan Pegon mengikuti persebaran Islam di Nusantara melalui perdagangan dan pesantren, sehingga menjadi contoh difusi budaya yang menyertai agama.\n\nPengecoh: abugida adalah aksara turunan India. Alfabet menulis vokal sebagai huruf penuh. Logogram mewakili kata. Silabari murni mewakili suku kata utuh seperti kana Jepang.",
      None),
    Q("Perhatikan indeks keragaman linguistik beberapa provinsi berikut.\n\nInterpretasi yang paling tepat untuk nilai IKL Papua adalah …",
      ["Peluang dua penduduk acak berbeda bahasa ibu sekitar 95%", "Sebanyak 95% penduduk Papua berbahasa ibu sama", "Papua hanya memiliki 95 bahasa daerah",
       "Keragaman bahasa Papua lebih rendah daripada Jawa Tengah", "Sebanyak 0,95% penduduk Papua berbahasa daerah"],
      "IKL (indeks Greenberg) = 1 − Σpᵢ² menyatakan peluang dua orang yang dipilih acak memiliki bahasa ibu berbeda. IKL Papua 0,95 berarti peluangnya sekitar 95%, sehingga keragaman bahasanya sangat tinggi karena terdapat ratusan bahasa dengan jumlah penutur masing-masing relatif kecil. Sebaliknya, IKL Jawa Tengah dan Yogyakarta sangat rendah (0,06–0,08) karena hampir seluruh penduduk berbahasa ibu Jawa. Keragaman tinggi di Papua, NTT, dan Sulawesi Tengah berkaitan dengan isolasi geografis oleh pegunungan dan pulau-pulau.\n\nPengecoh: IKL tinggi berarti beragam, bukan seragam. IKL bukan jumlah bahasa atau persentase penutur. Papua jauh lebih beragam daripada Jawa Tengah.",
      f_ikl3),
    Q("Perhatikan grafik tingkat partisipasi angkatan kerja (TPAK) menurut jenis kelamin berikut.\n\nSelisih TPAK laki-laki dan perempuan dinyatakan dengan tepat sebagai …",
      ["30 poin persen", "30 persen", "56 persen", "64 poin persen", "1,56 poin persen"],
      "Selisih dua persentase dinyatakan dalam poin persen: 84% − 54% = 30 poin persen.\nJika dinyatakan sebagai perubahan relatif, TPAK laki-laki (84 ÷ 54 − 1) × 100% ≈ 56% lebih tinggi daripada perempuan. Kedua cara memiliki arti berbeda, sehingga tidak boleh tertukar.\nKesenjangan TPAK berkaitan dengan geografi gender: norma budaya yang membagi ruang publik (bekerja di luar rumah) dan ruang domestik, beban pengasuhan anak, akses pendidikan, serta ketersediaan transportasi dan fasilitas penitipan anak.\n\nPengecoh: 30 persen keliru karena selisih persentase dinyatakan dalam poin persen. 56 persen adalah perbedaan relatif, bukan selisih. 64 dan 1,56 adalah salah hitung.",
      f_tpak),
    Q("Dalam banyak masyarakat tradisional, perempuan lebih banyak berada di ruang domestik, sedangkan laki-laki di ruang publik seperti pasar dan balai desa. Konsep geografi yang mengkaji gejala ini adalah …",
      ["Geografi gender dan ruang", "Geografi bahasa dan dialek", "Difusi relokasi budaya", "Bentuk dan batas negara", "Sekuen okupansi lanskap"],
      "Geografi gender mengkaji bagaimana peran gender membentuk dan dibentuk oleh ruang, misalnya pembagian ruang domestik (rumah, dapur) dan ruang publik (pasar, kantor, balai desa), perbedaan mobilitas laki-laki dan perempuan, akses terhadap lahan dan transportasi, serta rasa aman di ruang publik. Pembagian ruang tersebut tidak bersifat alami, melainkan dibentuk oleh norma budaya, sehingga dapat berubah. Misalnya di Minangkabau perempuan memegang harta pusaka, dan dalam masyarakat modern makin banyak perempuan bekerja di ruang publik.\n\nPengecoh: geografi bahasa, difusi relokasi, batas negara, dan sekuen okupansi tidak mengkaji pembagian ruang menurut gender.",
      None),
    Q("Perhatikan ciri beberapa rumah tradisional Indonesia berikut.\n\nRumah yang paling sesuai dengan lingkungan pegunungan tinggi yang dingin beserta namanya adalah …",
      ["P, honai di Pegunungan Tengah Papua", "Q, rumah panggung pesisir Sumatra", "R, rumah gadang di Sumatera Barat",
       "S, rumah lamin di Kalimantan Timur", "Q, honai di Pegunungan Tengah Papua"],
      "Honai (P) adalah rumah tradisional suku-suku di Pegunungan Tengah Papua, seperti Dani dan Lani, pada ketinggian ±1.500–2.500 m dengan udara dingin pada malam hari. Bentuknya bulat dengan dinding rapat tanpa jendela, pintu rendah, atap jerami tebal, dan perapian di tengah. Semua ciri tersebut berfungsi menahan panas di dalam rumah.\nQ sesuai dengan rumah panggung dataran rendah tropis basah. R adalah rumah gadang Minangkabau dengan atap bergonjong. S adalah rumah panjang (lamin atau betang) suku Dayak di tepi sungai.\nArsitektur vernakular menunjukkan adaptasi budaya material terhadap lingkungan.\n\nPengecoh: ciri Q justru cocok untuk daerah panas dan lembap.",
      f_vernak),
    Q("Mesopotamia, Lembah Sungai Indus, dan Lembah Sungai Kuning dikenal sebagai tempat lahirnya peradaban dan inovasi awal seperti pertanian, tulisan, dan kota. Dalam geografi budaya, wilayah seperti ini disebut …",
      ["Pusat budaya (hearth)", "Wilayah vernakular", "Daerah perlindungan bahasa", "Bangsa tanpa negara", "Wilayah enklave"],
      "Pusat budaya (cultural hearth) adalah wilayah tempat lahirnya inovasi budaya penting yang kemudian menyebar ke wilayah lain melalui difusi. Pusat budaya awal umumnya berada di lembah sungai besar yang subur, seperti Mesopotamia (Tigris–Eufrat), Mesir (Nil), Indus, Lembah Sungai Kuning (Huang He), serta Mesoamerika dan Andes. Kondisi tersebut mendukung surplus pertanian, pertumbuhan penduduk, kota, dan spesialisasi pekerjaan.\n\nPengecoh: wilayah vernakular adalah wilayah menurut persepsi warga. Daerah perlindungan adalah wilayah terisolasi tempat bahasa minoritas bertahan. Bangsa tanpa negara dan enklave adalah konsep geografi politik.",
      None),
    Q("Perhatikan peta pangan pokok tradisional dominan menurut provinsi berikut.\n\nPenjelasan yang paling tepat untuk pola sagu di bagian timur Indonesia adalah …",
      ["Rawa sagu alami melimpah dan menjadi tradisi pangan lokal", "Padi tidak pernah dapat tumbuh di seluruh wilayah timur",
       "Sagu dibawa pemerintah kolonial dari Eropa", "Penduduk timur menolak semua jenis pangan lain", "Iklim timur paling kering sehingga hanya sagu yang hidup"],
      "Sagu (Metroxylon sagu) tumbuh alami di rawa dan lahan basah dataran rendah Papua dan Maluku. Sejak lama masyarakat memanfaatkannya karena satu batang dapat menghasilkan ratusan kilogram pati dengan tenaga kerja relatif kecil. Sagu kemudian menjadi bagian identitas budaya, misalnya papeda. Di NTT dan sebagian Gorontalo, jagung menjadi pangan pokok tradisional karena iklim lebih kering yang kurang cocok untuk padi sawah. Pola ini menunjukkan hubungan ekologi dan budaya pangan. Kini konsumsi beras meningkat di seluruh wilayah, sehingga muncul upaya diversifikasi pangan lokal.\n\nPengecoh: padi dapat tumbuh di sebagian wilayah timur. Sagu adalah tanaman asli. Penduduk tidak menolak semua pangan lain. Iklim terkering justru di NTT, tempat jagung dominan.",
      f_pangan),
    Q("Masyarakat Bali mengembangkan subak dan terasering untuk mengolah lereng gunung menjadi sawah. Pandangan yang menyatakan manusia memilih dan mengolah berbagai kemungkinan yang disediakan alam disebut …",
      ["Posibilisme", "Determinisme", "Etnosentrisme", "Iredentisme", "Fatalisme"],
      "Posibilisme (Vidal de la Blache) menyatakan bahwa alam menyediakan berbagai kemungkinan, sedangkan manusia dengan budaya dan teknologinya memilih dan mengolah kemungkinan tersebut. Subak dan terasering menunjukkan bahwa lereng gunung yang curam dapat diubah menjadi sawah produktif melalui pengetahuan dan kerja sama masyarakat. Sistem subak diakui UNESCO sebagai warisan dunia (lanskap budaya) pada 2012.\nDeterminisme lingkungan menyatakan alam menentukan budaya dan perilaku manusia.\n\nPengecoh: determinisme bertentangan dengan peran aktif manusia. Etnosentrisme, iredentisme, dan fatalisme bukan teori hubungan manusia–lingkungan dalam konteks ini.",
      None),
]

P5 = [
    Q("Perhatikan beberapa warisan budaya takbenda Indonesia yang diakui UNESCO berikut.\n\nDaerah asal dua unsur yang masuk daftar perlindungan mendesak adalah …",
      ["Aceh dan Papua", "Jawa dan Bali", "Sulawesi dan Jawa", "Sumatera Barat dan Bali", "Jawa Barat dan Jawa Timur"],
      "Dua unsur bertanda bintang adalah Tari Saman (2011) dan Noken (2012). Tari Saman berasal dari suku Gayo di Aceh, sedangkan noken adalah tas anyaman atau rajutan serat kayu khas Papua. Keduanya masuk daftar warisan budaya takbenda yang memerlukan perlindungan mendesak karena jumlah pelaku dan pewarisnya menurun, misalnya akibat berkurangnya bahan baku dan minat generasi muda. Unsur lain seperti wayang, keris, batik, angklung, gamelan, dan pencak silat masuk daftar representatif.\n\nPengecoh: Jawa, Bali, Sulawesi, dan Jawa Barat adalah asal unsur warisan lain pada grafik, bukan unsur yang memerlukan perlindungan mendesak.",
      f_unesco),
    Q("Perhatikan sebaran dua kelompok etnis di Kota R berikut. Indeks disimilaritas D = ½ × Σ|aᵢ/A − bᵢ/B|.\n\nNilai indeks segregasi Kota R adalah …",
      ["0,60", "1,20", "0,30", "0,50", "0,40"],
      "1) Total A = 400 + 300 + 200 + 100 = 1.000; total B = 20 + 80 + 300 + 600 = 1.000.\n2) Selisih proporsi tiap distrik:\n• Distrik 1: |0,40 − 0,02| = 0,38.\n• Distrik 2: |0,30 − 0,08| = 0,22.\n• Distrik 3: |0,20 − 0,30| = 0,10.\n• Distrik 4: |0,10 − 0,60| = 0,50.\n3) Σ = 1,20 → D = ½ × 1,20 = 0,60.\nArtinya 60% anggota salah satu kelompok harus pindah agar sebaran merata, sehingga segregasi tergolong cukup tinggi. Segregasi permukiman dapat disebabkan pilihan sukarela (kedekatan budaya), diskriminasi, perbedaan ekonomi, atau sejarah kebijakan, seperti kampung-kampung etnis pada masa kolonial.\n\nPengecoh: 1,20 lupa dikalikan ½. 0,30, 0,50, dan 0,40 adalah salah hitung.",
      f_seg2),
    Q("Seseorang yang menilai budaya kelompok lain aneh dan lebih rendah semata-mata karena berbeda dengan budayanya sendiri menunjukkan sikap …",
      ["Etnosentrisme", "Relativisme budaya", "Multikulturalisme", "Akulturasi", "Toleransi budaya"],
      "Etnosentrisme adalah sikap menilai budaya lain dengan ukuran budaya sendiri dan menganggap budaya sendiri paling benar atau unggul. Sikap ini dapat memicu prasangka, diskriminasi, dan konflik antarkelompok, terutama di negara yang sangat beragam seperti Indonesia.\nSebaliknya, relativisme budaya memahami setiap budaya menurut konteksnya sendiri. Multikulturalisme dan toleransi menghargai keberagaman. Akulturasi adalah percampuran budaya.\n\nPengecoh: keempat opsi lain bersifat menghargai atau netral terhadap perbedaan budaya.",
      None),
    Q("Perhatikan grafik penutur aktif bahasa L menurut kelompok umur berikut.\n\nUpaya yang paling tepat untuk mencegah kepunahan bahasa L adalah …",
      ["Mendorong pewarisan di keluarga dan muatan lokal sekolah", "Membiarkan bahasa L berkembang tanpa campur tangan",
       "Melarang generasi muda mempelajari bahasa Indonesia", "Hanya mendokumentasikan bahasa L dalam museum", "Mengganti bahasa L dengan bahasa asing populer"],
      "Grafik menunjukkan penutur aktif masih tinggi pada usia 60+ (95%) dan 40–59 tahun (80%), tetapi anjlok pada usia 20–39 tahun (35%) dan hampir habis pada anak-anak (2–8%). Menurut kriteria vitalitas bahasa UNESCO, bahasa yang tidak lagi diwariskan kepada anak di rumah tergolong terancam. Upaya revitalisasi yang efektif adalah memulihkan pewarisan antargenerasi di keluarga dan komunitas, memasukkan bahasa L dalam muatan lokal sekolah, membuat bahan bacaan dan konten digital, serta mendokumentasikannya sebagai pendukung.\n\nPengecoh: membiarkan tanpa intervensi mempercepat kepunahan. Melarang bahasa Indonesia tidak realistis dan merugikan. Dokumentasi saja tidak menghidupkan bahasa. Mengganti dengan bahasa asing justru mempercepat pergeseran bahasa.",
      f_vital),
    Q("Perhatikan gambar tiga jenis wilayah budaya berikut.\n\nPasangan jenis wilayah yang tepat adalah …",
      ["P formal, Q fungsional, R vernakular", "P fungsional, Q formal, R vernakular", "P vernakular, Q formal, R fungsional",
       "P formal, Q vernakular, R fungsional", "P fungsional, Q vernakular, R formal"],
      "• P – wilayah formal (seragam): wilayah dengan ciri budaya yang sama di seluruh bagiannya, misalnya wilayah yang seluruh penduduknya berbahasa Sunda.\n• Q – wilayah fungsional (nodal): wilayah yang diorganisasi di sekitar satu pusat dan dihubungkan oleh interaksi, misalnya jangkauan siaran radio atau daerah pelayanan sebuah kota.\n• R – wilayah vernakular (perseptual): wilayah yang dibentuk oleh persepsi masyarakat, dengan batas kabur, misalnya Tapal Kuda di Jawa Timur yang dikenal sebagai daerah berbudaya Pandalungan (perpaduan Jawa dan Madura).\n\nPengecoh: opsi lain menukar jenis wilayah.",
      f_wilayah),
    Q("Sebagai negara kepulauan yang terdiri atas belasan ribu pulau, Indonesia menghadapi tantangan integrasi. Konsep yang dikembangkan untuk memandang darat dan laut sebagai satu kesatuan wilayah adalah …",
      ["Wawasan Nusantara", "Iredentisme Nusantara", "Devolusi kepulauan", "Balkanisasi wilayah", "Determinisme maritim"],
      "Indonesia termasuk negara berbentuk terpecah (fragmented), sehingga laut dapat dipandang sebagai pemisah. Wawasan Nusantara adalah cara pandang bangsa Indonesia yang memandang darat, laut, dan udara sebagai satu kesatuan politik, ekonomi, sosial budaya, dan pertahanan keamanan. Konsep ini berakar pada Deklarasi Djuanda (1957) dan diakui melalui UNCLOS 1982 sebagai negara kepulauan, sehingga perairan di antara pulau menjadi perairan kepulauan Indonesia. Wawasan Nusantara berfungsi sebagai kekuatan sentripetal.\n\nPengecoh: iredentisme, devolusi, dan balkanisasi adalah konsep geografi politik lain. Determinisme maritim bukan konsep kebangsaan Indonesia.",
      None),
    Q("Perhatikan peta arah perpindahan penduduk program transmigrasi dari Jawa berikut.\n\nPenyebaran kesenian kuda lumping dan wayang ke Lampung melalui program tersebut merupakan contoh …",
      ["Difusi relokasi", "Difusi hierarki", "Difusi stimulus", "Difusi menular", "Asimilasi budaya"],
      "Program transmigrasi memindahkan penduduk dari Jawa, Bali, dan Madura ke Sumatra, Kalimantan, Sulawesi, dan Papua. Para transmigran membawa bahasa, kesenian (kuda lumping, wayang, reog), pola permukiman, dan tradisi pertanian mereka ke daerah tujuan. Karena budaya menyebar bersama perpindahan para pembawanya, prosesnya adalah difusi relokasi. Akibatnya terbentuk kantong-kantong budaya Jawa di luar Jawa, misalnya di Lampung, yang kemudian berinteraksi dengan budaya lokal dan dapat memicu akulturasi maupun gesekan sosial.\n\nPengecoh: difusi hierarki, stimulus, dan menular tidak melibatkan perpindahan pembawa budaya. Asimilasi adalah peleburan budaya, bukan penyebaran.",
      f_transmig),
    Q("Pemberian status keistimewaan kepada Daerah Istimewa Yogyakarta, termasuk penetapan gubernur dari Sultan yang bertakhta, terutama didasarkan pada …",
      ["Sejarah dan identitas budaya yang khas", "Jumlah penduduk terbanyak di Indonesia", "Wilayah provinsi terluas di Pulau Jawa",
       "Tuntutan pemisahan diri dari Indonesia", "Penolakan masyarakat terhadap budaya Jawa"],
      "Keistimewaan DIY diatur dalam UU No. 13 Tahun 2012 berdasarkan sejarah dan asal-usulnya. Kesultanan Yogyakarta dan Kadipaten Pakualaman segera menyatakan bergabung dengan Republik Indonesia pada 1945 dan berperan besar dalam perjuangan kemerdekaan, termasuk ketika Yogyakarta menjadi ibu kota RI. Keistimewaan mencakup penetapan gubernur dan wakil gubernur, kelembagaan, kebudayaan, pertanahan, dan tata ruang. Ini adalah contoh pengakuan identitas regional dalam kerangka negara kesatuan.\n\nPengecoh: DIY bukan provinsi berpenduduk terbanyak atau terluas. Keistimewaan tidak didasarkan pada tuntutan pemisahan diri. DIY justru menjadi pusat budaya Jawa.",
      None),
    Q("Perhatikan grafik bahasa konten situs web dunia berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Konten bahasa Inggris jauh melebihi porsi penuturnya", "Konten berbahasa Indonesia mendominasi internet dunia",
       "Semua bahasa memiliki porsi konten yang sebanding", "Bahasa Spanyol memiliki porsi konten terbesar", "Porsi konten sama persis dengan jumlah penutur bahasa ibu"],
      "Grafik menunjukkan sekitar 49% situs web berbahasa Inggris, padahal penutur bahasa ibu Inggris hanya sekitar 5% penduduk dunia. Dominasi ini terjadi karena bahasa Inggris menjadi lingua franca global dalam sains, bisnis, teknologi, dan internet, serta banyak penutur bahasa kedua. Sebaliknya, bahasa Indonesia dengan ratusan juta penutur hanya sekitar 0,9% konten. Ketimpangan ini menunjukkan globalisasi bahasa dapat menekan bahasa lain di ruang digital, sehingga diperlukan pengembangan konten lokal.\n\nPengecoh: konten berbahasa Indonesia kecil. Porsi antarbahasa sangat timpang. Spanyol hanya 6%. Porsi konten tidak sebanding dengan jumlah penutur.",
      f_internet),
    Q("Batik diakui UNESCO sebagai warisan budaya takbenda, sedangkan Candi Borobudur diakui sebagai warisan dunia. Perbedaan utama keduanya adalah …",
      ["Batik berupa pengetahuan dan keterampilan, Borobudur benda fisik", "Batik berasal dari luar negeri, Borobudur dari Indonesia",
       "Batik tidak perlu dilestarikan, Borobudur perlu dilestarikan", "Batik hanya dibuat di Bali, Borobudur di Jawa Timur", "Batik adalah warisan alam, Borobudur warisan campuran"],
      "UNESCO membedakan dua jenis pengakuan:\n• Warisan budaya takbenda (intangible cultural heritage, Konvensi 2003): tradisi, pengetahuan, keterampilan, seni pertunjukan, dan praktik sosial yang diwariskan antargenerasi. Batik diakui karena teknik, simbol, dan budaya membatik, bukan karena kainnya semata.\n• Warisan dunia (world heritage, Konvensi 1972): situs fisik budaya atau alam yang bernilai universal luar biasa, seperti Candi Borobudur, Candi Prambanan, dan Taman Nasional Komodo.\nKeduanya memerlukan pelestarian, tetapi caranya berbeda. Warisan takbenda dilestarikan melalui pewarisan kepada generasi muda, sedangkan situs fisik melalui konservasi bangunan dan pengelolaan kawasan.\n\nPengecoh: batik berasal dari Indonesia, perlu dilestarikan, dibuat di banyak daerah, dan bukan warisan alam. Borobudur berada di Jawa Tengah.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
