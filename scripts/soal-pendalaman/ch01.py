from figlib import *

# ============================ figures ============================

def f_atmos(path):
    fig, ax = new(7, 5.2)
    z = [0, 12, 50, 85, 110]
    T = [15, -56, -2, -90, 60]
    ax.plot(T, z, color=C["red"], lw=2.5)
    for zz in [12, 50, 85]:
        ax.axhline(zz, color="#A0AEC0", ls="--", lw=1)
    for name, y in [("P", 6), ("Q", 31), ("R", 67), ("S", 98)]:
        ax.text(-120, y, name, fontsize=18, fontweight="bold", color=C["blue"], va="center")
    ax.set_xlim(-130, 80); ax.set_ylim(0, 110)
    ax.set_xlabel("Suhu (°C)"); ax.set_ylabel("Ketinggian (km)")
    ax.set_title("Profil suhu vertikal atmosfer standar")
    save(fig, path)


def f_albedo(path):
    cats = ["Hutan tropis", "Sawah tergenang", "Atap seng terang", "Aspal", "Beton"]
    alb = [12, 8, 35, 6, 25]
    bars(cats, {"Albedo (%)": alb}, path, title="Albedo beberapa permukaan (radiasi datang 800 W/m²)",
         ylabel="Albedo (%)", values=True, ylim=(0, 45), w=8.5, rot=15)


def f_isobar_speed(path):
    centers = [(0.18, 0.55, -18, 0.20, "R"), (0.85, 0.45, 14, 0.28, "T")]
    pts = {"P": (0.38, 0.55), "Q": (0.62, 0.85), "S": (0.83, 0.15), "U": (0.12, 0.15)}
    Z = iso_map(path + ".tmp.png", centers, points=pts)
    # verify P has steepest gradient
    gy, gx = np.gradient(Z)
    g = np.hypot(gx, gy)
    def at(p):
        return g[int(p[1] * 219), int(p[0] * 299)]
    vals = {k: at(v) for k, v in pts.items()}
    assert max(vals, key=vals.get) == "P", vals
    os.replace(path + ".tmp.png", path)


def f_pola3(path):
    X = [310, 290, 230, 140, 90, 60, 40, 35, 60, 120, 210, 300]
    Y = [210, 220, 290, 270, 180, 130, 120, 140, 180, 280, 300, 240]
    Z = [120, 110, 140, 180, 270, 330, 320, 240, 160, 110, 90, 100]
    fig, axs = plt.subplots(1, 3, figsize=(10, 3.6), sharey=True)
    for a, d, n in zip(axs, [X, Y, Z], ["Stasiun X", "Stasiun Y", "Stasiun Z"]):
        a.bar(range(12), d, color=C["lblue"], edgecolor=C["blue"])
        a.set_xticks(range(12)); a.set_xticklabels(BULAN)
        a.set_title(n); a.grid(axis="y", color="#E2E8F0"); a.set_axisbelow(True)
    axs[0].set_ylabel("Curah hujan (mm)")
    save(fig, path)


def f_fohn(path):
    fig, ax = blank(9, 4.6, (0, 100), (0, 52))
    xs = [0, 10, 50, 85, 100]; ys = [4, 6, 44, 10, 9]
    ax.fill_between([0, 10, 50, 85, 100], 0, [4, 6, 44, 10, 9], color="#C6A77B")
    ax.plot([0, 100], [4, 4], color="none")
    ax.text(2, 1.5, "Laut", color=C["blue"], fontsize=11)
    ax.add_patch(Rectangle((0, 0), 10, 4, fc=C["lblue"], ec="none"))
    ax.annotate("", xy=(42, 40), xytext=(4, 8), arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["blue"]))
    ax.annotate("", xy=(84, 14), xytext=(56, 44), arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["red"]))
    ax.plot([14, 50], [17, 17], ls="--", color=C["gray"])
    ax.text(5, 18, "dasar awan\n800 m", fontsize=10, ha="center")
    ax.add_patch(Ellipse((36, 26), 26, 14, fc="#E2E8F0", ec="#A0AEC0"))
    ax.text(3, 10, "28 °C\n0 m", fontsize=11, fontweight="bold")
    ax.text(50, 47.5, "Puncak 2.400 m", ha="center", fontsize=11, fontweight="bold")
    ax.text(88, 15, "Kota K\n400 m\nT = ?", fontsize=11, fontweight="bold")
    ax.text(50, 2, "Laju adiabatik kering 1 °C/100 m · laju jenuh 0,6 °C/100 m", ha="center", fontsize=10)
    save(fig, path)


P_AM = [420, 380, 300, 210, 120, 70, 40, 45, 80, 140, 250, 345]  # sum = 2400
T_AM = [26.2, 26.3, 26.8, 27.3, 27.5, 27.0, 26.5, 26.9, 27.4, 27.8, 27.2, 26.5]


def f_klim_am(path):
    assert sum(P_AM) == 2400
    climograph(T_AM, P_AM, path, title="Klimograf Stasiun M (total hujan 2.400 mm/tahun)", ylimT=(20, 30), ylimP=(0, 450))


# ---- paket 1
def f_neraca(path):
    fig, ax = blank(9.5, 5.4, (0, 100), (0, 62))
    ax.add_patch(Rectangle((0, 0), 100, 8, fc="#C6A77B", ec="none"))
    ax.text(50, 3.5, "Permukaan Bumi", ha="center", fontsize=11)
    ax.add_patch(Rectangle((0, 8), 100, 30, fc="#EBF8FF", ec="none"))
    ax.text(98, 35.5, "Atmosfer", ha="right", fontsize=10, color=C["gray"])
    ax.text(50, 59, "Puncak atmosfer", ha="center", fontsize=10, color=C["gray"])
    ax.plot([0, 100], [57, 57], color="#A0AEC0", ls="--", lw=1)
    arrow(ax, 8, 56, 8, 40, color=C["orange"], lw=3); ax.text(8, 47, "100\nsatuan\nmasuk", ha="center", fontsize=10, bbox=dict(fc="white", ec="none"))
    arrow(ax, 26, 38, 26, 56, color=C["orange"], lw=3); ax.text(26, 47, "P = 22", ha="center", fontsize=11, fontweight="bold", bbox=dict(fc="white", ec="none"))
    ax.text(26, 41, "dipantulkan\nawan & udara", ha="center", fontsize=9)
    arrow(ax, 46, 9, 46, 56, color=C["orange"], lw=3); ax.text(46, 47, "Q = 8", ha="center", fontsize=11, fontweight="bold", bbox=dict(fc="white", ec="none"))
    ax.text(46, 20, "dipantulkan\npermukaan", ha="center", fontsize=9, bbox=dict(fc="white", ec="none"))
    arrow(ax, 66, 56, 66, 24, color=C["orange"], lw=3); ax.text(66, 47, "R = 20", ha="center", fontsize=11, fontweight="bold", bbox=dict(fc="white", ec="none"))
    ax.text(66, 20, "diserap\natmosfer", ha="center", fontsize=9)
    arrow(ax, 86, 56, 86, 9, color=C["orange"], lw=3); ax.text(86, 47, "S = 50", ha="center", fontsize=11, fontweight="bold", bbox=dict(fc="white", ec="none"))
    ax.text(86, 20, "diserap\npermukaan", ha="center", fontsize=9, bbox=dict(fc="white", ec="none"))
    ax.set_title("Neraca radiasi gelombang pendek rata-rata global (satuan relatif, disederhanakan)")
    save(fig, path)


def f_diurnal(path):
    h = np.arange(0, 25, 1)
    A = 27 + 3 * np.sin((h - 9) / 24 * 2 * np.pi)
    B = 25 + 7 * np.sin((h - 9) / 24 * 2 * np.pi)
    lines(h, {"Stasiun A": A, "Stasiun B": B}, path, title="Suhu udara per jam pada hari cerah yang sama",
          xlabel="Jam (waktu setempat)", ylabel="Suhu (°C)", xticks=range(0, 25, 3), markers=False)


def f_inversi(path):
    fig, ax = new(6.5, 5)
    z = [0, 100, 200, 300, 400, 500, 600, 700, 800, 1000, 1200]
    T = [22.0, 21.4, 20.8, 20.2, 21.8, 23.2, 24.0, 23.2, 22.5, 21.0, 19.6]
    ax.plot(T, z, marker="o", color=C["red"], lw=2.2)
    ax.axhspan(300, 600, color="#FEFCBF", alpha=0.8)
    ax.text(18.6, 450, "Lapisan\nK", fontsize=13, fontweight="bold", va="center")
    ax.set_xlabel("Suhu (°C)"); ax.set_ylabel("Ketinggian (m)")
    ax.set_xlim(18, 25.5)
    ax.set_title("Hasil radiosonde pukul 06.00 di kota lembah")
    ax.grid(color="#EDF2F7")
    save(fig, path)


def f_uhi(path):
    xs = np.arange(9)
    T = [24.1, 24.6, 25.9, 27.4, 28.6, 26.1, 28.8, 25.6, 24.3]
    fig, ax = new(9, 4.4)
    ax.plot(xs, T, marker="o", lw=2.4, color=C["red"])
    names = ["Sawah", "Desa", "Pinggiran", "Permukiman\npadat", "Pusat\nbisnis", "Taman\nkota P", "Kawasan\nindustri",
             "Pinggiran", "Kebun"]
    ax.set_xticks(xs); ax.set_xticklabels(names, fontsize=9.5)
    ax.set_ylabel("Suhu udara 21.00 (°C)"); ax.grid(axis="y", color="#E2E8F0")
    ax.set_title("Transek suhu malam hari melintasi sebuah kota")
    ax.annotate("P", (5, 26.1), xytext=(5, 27.6), fontsize=14, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->"))
    save(fig, path)


def f_darat_laut(path):
    fig, ax = blank(9, 4, (0, 100), (0, 40))
    ax.add_patch(Rectangle((0, 0), 50, 10, fc="#C6A77B", ec="none"))
    ax.add_patch(Rectangle((50, 0), 50, 8, fc=C["lblue"], ec="none"))
    ax.text(25, 4.5, "Daratan: 22 °C", ha="center", fontsize=12, fontweight="bold")
    ax.text(75, 3.5, "Laut: 27 °C", ha="center", fontsize=12, fontweight="bold")
    ax.text(50, 36, "Pukul 02.00 dini hari, langit cerah, angin regional lemah", ha="center", fontsize=11)
    ax.text(25, 22, "Tekanan permukaan: ?", ha="center", fontsize=11)
    ax.text(75, 22, "Tekanan permukaan: ?", ha="center", fontsize=11)
    ax.text(50, 14, "← arah angin permukaan = ? →", ha="center", fontsize=11, color=C["gray"])
    save(fig, path)


def f_gradien(path):
    fig, ax = blank(8, 4.4, (0, 100), (0, 48))
    yy = np.linspace(3, 42, 100)
    for x, p in [(12, 1014), (32, 1010), (52, 1006), (72, 1002)]:
        ax.plot(x + 3 * np.sin(yy / 7), yy, color="#2D3748", lw=1.4)
        ax.text(x + 3 * np.sin(42 / 7) - 2, 44, f"{p} mb", fontsize=10)
    ax.plot(12 + 3 * np.sin(25 / 7), 25, "o", color="black"); ax.text(8.5, 27, "A", fontsize=15, fontweight="bold")
    ax.plot(72 + 3 * np.sin(25 / 7), 25, "o", color="black"); ax.text(73, 27, "B", fontsize=15, fontweight="bold")
    ax.annotate("", xy=(70.8, 21), xytext=(11.5, 21), arrowprops=dict(arrowstyle="<->", lw=1.3))
    ax.text(41, 17.5, "jarak A–B = 333 km", ha="center", fontsize=11, bbox=dict(fc="white", ec="none"))
    ax.set_title("Peta isobar (interval 4 mb)")
    save(fig, path)


# ---- paket 2
def f_tricell(path):
    fig, ax = blank(8.5, 5.6, (0, 100), (0, 70))
    lats = [0, 30, 60, 90]
    ys = [5, 25, 45, 65]
    ax.plot([20, 20], [5, 65], color="#2D3748", lw=2)
    for lab, y, lat in zip("KLMN", ys, lats):
        ax.plot([18, 22], [y, y], color="#2D3748", lw=2)
        ax.text(14, y, f"{lat}°", ha="right", va="center", fontsize=12)
        ax.text(25, y, lab, fontsize=16, fontweight="bold", color=C["blue"], va="center")
    # surface winds
    arrow(ax, 45, 21, 38, 9, color=C["teal"]); ax.text(48, 14, "pasat timur laut", fontsize=10)
    arrow(ax, 38, 29, 45, 41, color=C["teal"]); ax.text(48, 35, "angin baratan", fontsize=10)
    arrow(ax, 45, 61, 38, 49, color=C["teal"]); ax.text(48, 55, "angin timuran kutub", fontsize=10)
    # cells
    for (y0, y1, n) in [(5, 25, "sel Hadley"), (25, 45, "sel Ferrel"), (45, 65, "sel Polar")]:
        ax.add_patch(Ellipse((80, (y0 + y1) / 2), 22, (y1 - y0) * 0.85, fc="none", ec=C["gray"], lw=1.4, ls="--"))
        ax.text(80, (y0 + y1) / 2, n, ha="center", va="center", fontsize=10)
    ax.set_title("Model sirkulasi tiga sel (Belahan Bumi Utara)")
    save(fig, path)


def f_monsun(path):
    fig, ax = indonesia_map(extent=(92, 142, -14, 12), w=10, h=5.2)
    for (x, y) in [(108, 9), (112, 7), (104, 4), (100, 1)]:
        ax.annotate("", xy=(x - 2.5, y - 4), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["blue"]))
    for (x, y) in [(104, -3), (108, -5), (114, -4.5), (120, -6.8), (126, -8)]:
        ax.annotate("", xy=(x + 4, y - 1.3), xytext=(x, y), arrowprops=dict(arrowstyle="-|>", lw=2.2, color=C["blue"]))
    ax.text(100, 10.3, "Tekanan tinggi", fontsize=10, fontweight="bold", color=C["blue"])
    ax.text(127, -12.8, "Tekanan rendah", fontsize=10, fontweight="bold", color=C["red"])
    ax.set_title("Pola angin permukaan rata-rata pada bulan tertentu")
    save(fig, path)


def f_td(path):
    h = np.arange(0, 24)
    T = 28 + 4 * np.sin((h - 8) / 24 * 2 * np.pi)
    Td = 23.5 + 0.5 * np.sin((h - 8) / 24 * 2 * np.pi)
    fig, ax = new(8, 4.2)
    ax.plot(h, T, color=C["red"], lw=2.2, label="Suhu udara")
    ax.plot(h, Td, color=C["blue"], lw=2.2, ls="--", label="Titik embun")
    ax.plot(14, 32, "o", color=C["red"]); ax.text(14.3, 32.4, "32 °C", fontsize=10)
    ax.plot(14, 24, "o", color=C["blue"]); ax.text(14.3, 22.8, "24 °C", fontsize=10)
    ax.set_xticks(range(0, 24, 2)); ax.set_xlabel("Jam"); ax.set_ylabel("°C"); ax.set_ylim(20, 34)
    ax.legend(frameon=False); ax.grid(color="#EDF2F7")
    ax.set_title("Suhu udara dan titik embun di sebuah stasiun")
    save(fig, path)


def f_hujan4(path):
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.2))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 8); a.axis("off")
    a = axs[0]
    a.add_patch(Rectangle((0, 0), 10, 1, fc="#C6A77B")); a.add_patch(Circle((8.5, 7), 0.7, fc="#F6E05E"))
    arrow(a, 5, 1.3, 5, 5, color=C["red"]); a.add_patch(Ellipse((5, 5.8), 4, 1.6, fc="#E2E8F0", ec="#718096"))
    a = axs[1]
    a.add_patch(Polygon([(0, 0), (6, 6), (10, 0)], fc="#C6A77B")); arrow(a, 0.3, 1.5, 4.5, 5.8, color=C["blue"])
    a.add_patch(Ellipse((3.5, 6.5), 3.5, 1.4, fc="#E2E8F0", ec="#718096"))
    a = axs[2]
    a.add_patch(Polygon([(0, 0), (10, 0), (10, 4.5)], fc="#BEE3F8", ec=C["blue"])); a.text(7.8, 1.2, "dingin", fontsize=9)
    arrow(a, 1, 0.8, 8.5, 5.5, color=C["red"]); a.text(1, 4.5, "hangat", fontsize=9)
    a.add_patch(Ellipse((8, 6.6), 3.5, 1.4, fc="#E2E8F0", ec="#718096"))
    a = axs[3]
    a.add_patch(Rectangle((0, 0), 10, 1, fc=C["lblue"]))
    arrow(a, 0.5, 1.8, 4.3, 1.8, color=C["teal"]); arrow(a, 9.5, 1.8, 5.7, 1.8, color=C["teal"])
    arrow(a, 5, 2.2, 5, 5.5, color=C["red"]); a.add_patch(Ellipse((5, 6.3), 4, 1.4, fc="#E2E8F0", ec="#718096"))
    for i, a in enumerate(axs):
        a.set_title(f"Gambar {i+1}")
    save(fig, path)


AMBON = [130, 120, 140, 290, 520, 640, 600, 400, 240, 160, 110, 130]
JKT = [390, 340, 210, 150, 120, 95, 70, 55, 70, 110, 150, 230]


def f_ambon(path):
    bars(BULAN3, {"Stasiun J": JKT, "Stasiun K": AMBON}, path, title="Rata-rata curah hujan bulanan dua stasiun",
         ylabel="Curah hujan (mm)", w=9)


def f_walker(path):
    fig, ax = blank(10, 4.4, (0, 100), (0, 44))
    ax.add_patch(Rectangle((0, 0), 100, 8, fc=C["lblue"], ec="none"))
    ax.add_patch(Rectangle((0, 0), 12, 9, fc="#C6A77B")); ax.text(6, 4, "Indonesia", ha="center", fontsize=9)
    ax.add_patch(Rectangle((90, 0), 10, 9, fc="#C6A77B")); ax.text(95, 4, "Peru", ha="center", fontsize=9)
    ax.text(50, 4, "Samudra Pasifik ekuator", ha="center", fontsize=10)
    arrow(ax, 16, 12, 16, 34, color=C["red"], lw=3); ax.text(18, 23, "P", fontsize=16, fontweight="bold")
    arrow(ax, 20, 38, 80, 38, color=C["gray"], lw=3); ax.text(50, 40, "Q", fontsize=16, fontweight="bold")
    arrow(ax, 85, 34, 85, 12, color=C["blue"], lw=3); ax.text(87, 23, "R", fontsize=16, fontweight="bold")
    arrow(ax, 80, 11, 20, 11, color=C["teal"], lw=3); ax.text(50, 13, "S", fontsize=16, fontweight="bold")
    ax.add_patch(Ellipse((14, 38), 12, 5, fc="#E2E8F0", ec="#718096"))
    ax.set_title("Sirkulasi Walker pada kondisi normal")
    save(fig, path)


# ---- paket 3
P_AW = [280, 250, 210, 120, 60, 25, 10, 15, 30, 90, 180, 230]  # 1500
T_AW = [26.5, 26.6, 27.0, 27.4, 27.0, 26.0, 25.0, 25.3, 26.4, 27.6, 27.8, 27.0]


def f_klim_aw(path):
    assert sum(P_AW) == 1500
    climograph(T_AW, P_AW, path, title="Klimograf Stasiun W (total hujan 1.500 mm/tahun)", ylimT=(20, 30), ylimP=(0, 320))


def f_sf_table(path):
    table([[2019, 4, 6], [2020, 5, 5], [2021, 3, 7], [2022, 6, 4], [2023, 2, 8]],
          ["Tahun", "Jumlah bulan kering (< 60 mm)", "Jumlah bulan basah (> 100 mm)"], path,
          title="Rekap bulan kering dan basah Stasiun H", col_w=[0.18, 0.41, 0.41])


def f_pola_map(path):
    A = ["Riau", "Sumatera Barat", "Jambi", "Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Timur", "Sumatera Utara", "Kepulauan Riau", "Bengkulu"]
    B = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "Yogyakarta", "Banten", "Jakarta Raya", "Bali", "Nusa Tenggara Barat",
         "Nusa Tenggara Timur", "Lampung", "Sumatera Selatan", "Kalimantan Selatan", "Sulawesi Selatan", "Bangka-Belitung"]
    Cc = ["Maluku"]
    col = {**{p: "#F6AD55" for p in A}, **{p: "#68D391" for p in B}, **{p: "#B794F4" for p in Cc}}
    fig, ax = indonesia_map(colors=col, w=10, h=4.6)
    for t, (x, y) in {"A": (101.5, 0.5), "B": (110.5, -7.2), "C": (129.5, -3.3)}.items():
        ax.text(x, y, t, fontsize=17, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="#2D3748"))
    ax.set_title("Pembagian wilayah pola curah hujan (disederhanakan)")
    save(fig, path)


DAS = [("Okt I", 22), ("Okt II", 58), ("Okt III", 41), ("Nov I", 52), ("Nov II", 67), ("Nov III", 49),
       ("Des I", 80), ("Des II", 95), ("Des III", 110)]


def f_dasarian(path):
    bars([d[0] for d in DAS], {"Curah hujan (mm)": [d[1] for d in DAS]}, path,
         title="Curah hujan dasarian ZOM X", ylabel="mm per dasarian", values=True, hline=50, ylim=(0, 125), w=9)


def f_junghuhn(path):
    fig, ax = blank(9, 5, (0, 100), (0, 60))
    ax.fill_between([0, 50, 100], [0, 0, 0], [0, 56, 0], color="#C6A77B")
    for y, lab in [(0, ""), (11.8, "700 m"), (25.2, "1.500 m"), (42, "2.500 m")]:
        if lab:
            ax.plot([0, 100], [y, y], ls="--", color="#4A5568", lw=1)
            ax.text(1, y + 0.8, lab, fontsize=10)
    for t, y in [("K", 6), ("L", 18.5), ("M", 33.5), ("N", 49)]:
        ax.text(80, y, t, fontsize=16, fontweight="bold", color=C["blue"], va="center")
    ax.text(50, 58, "Puncak ± 3.300 m", ha="center", fontsize=10)
    ax.set_title("Zona suhu menurut ketinggian (Junghuhn)")
    save(fig, path)


OLD = [320, 290, 260, 210, 150, 90, 60, 40, 70, 140, 230, 300]


def f_oldeman(path):
    bars(BULAN3, {"Curah hujan (mm)": OLD}, path, title="Rata-rata curah hujan bulanan Stasiun O", ylabel="mm",
         values=True, ylim=(0, 360), w=9)


# ---- paket 4
YR = np.arange(2014, 2025, 1 / 24)


def oni():
    pts = {2014: 0.0, 2014.75: 0.5, 2015.9: 2.6, 2016.5: 0.0, 2017.0: -0.6, 2017.6: -0.1, 2017.95: -0.9,
           2018.4: -0.2, 2018.9: 0.8, 2019.5: 0.3, 2020.0: 0.5, 2020.4: -0.4, 2020.9: -1.3, 2021.4: -0.5,
           2021.9: -1.0, 2022.4: -0.9, 2022.9: -0.9, 2023.2: -0.2, 2023.5: 1.0, 2023.95: 2.0, 2024.4: 0.6, 2024.95: -0.3}
    xs = np.array(list(pts)); ys = np.array(list(pts.values()))
    return YR, np.interp(YR, xs, ys)


def f_oni(path):
    x, y = oni()
    fig, ax = new(9.5, 4.2)
    ax.fill_between(x, 0, y, where=y >= 0.5, color=C["red"], alpha=0.6, interpolate=True)
    ax.fill_between(x, 0, y, where=y <= -0.5, color=C["blue"], alpha=0.6, interpolate=True)
    ax.plot(x, y, color="#2D3748", lw=1.5)
    for t in [0.5, -0.5]:
        ax.axhline(t, ls="--", color="#718096", lw=1)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(range(2014, 2025)); ax.set_ylabel("ONI (°C)")
    ax.set_title("Oceanic Niño Index (ONI) 2014–2024 (disederhanakan)")
    save(fig, path)


def f_iod(path):
    fig, ax = world_map(extent=(38, 125, -22, 18), w=9.5, h=4.6)
    ax.add_patch(Ellipse((60, -2), 26, 16, fc=C["red"], alpha=0.45, ec="none"))
    ax.add_patch(Ellipse((98, -6), 18, 10, fc=C["blue"], alpha=0.5, ec="none"))
    ax.text(60, -2, "+1,0 °C", ha="center", fontsize=13, fontweight="bold")
    ax.text(98, -6, "−0,8 °C", ha="center", fontsize=13, fontweight="bold")
    ax.set_title("Anomali suhu muka laut Samudra Hindia, September")
    save(fig, path)


ANOM = {"P": (300, 180), "Q": (250, 200), "R": (400, 270), "S": (150, 160)}


def f_anom(path):
    cats = list(ANOM)
    bars([f"Stasiun {c}" for c in cats], {"Normal": [ANOM[c][0] for c in cats], "Tahun El Niño": [ANOM[c][1] for c in cats]},
         path, title="Curah hujan September–November (mm)", ylabel="mm", values=True, ylim=(0, 450), w=8.5)


def f_arlindo(path):
    fig, ax = indonesia_map(extent=(105, 135, -12.5, 8), w=9, h=6.2)
    path_pts = [[(128, 7), (124, 4), (119, 1.5), (118.2, -3), (117.5, -6.5), (116, -9.5), (115, -11.8)],
                [(117.5, -6.5), (121, -8.0), (124, -9.0), (125, -10.5)],
                [(131, 2), (128, -1), (127, -4.5), (127, -7.5), (126, -10.5), (124, -12)]]
    for pp in path_pts:
        xs, ys = zip(*pp)
        ax.plot(xs, ys, color=C["red"], lw=2.4)
        ax.annotate("", xy=pp[-1], xytext=pp[-2], arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=2.4))
    ax.text(129, 6, "Samudra\nPasifik", fontsize=10, ha="center")
    ax.text(110, -11, "Samudra Hindia", fontsize=10)
    ax.set_title("Lintasan utama sebuah arus laut di perairan Indonesia")
    save(fig, path)


def f_tracks(path):
    fig, ax = world_map(extent=(90, 160, -25, 25), w=9.5, h=6.5)
    ax.axhspan(-5, 5, color="#FEFCBF", alpha=0.7)
    ax.text(150, 0, "5°LU–5°LS", fontsize=9, ha="center")
    rnd = np.random.RandomState(3)
    for i in range(7):
        x0 = 140 + rnd.rand() * 15; y0 = 8 + rnd.rand() * 6
        xs = x0 - np.linspace(0, 25, 12); ys = y0 + np.linspace(0, 9, 12) ** 1.15
        ax.plot(xs, ys, color=C["red"], lw=1.4)
    for i in range(6):
        x0 = 112 + rnd.rand() * 35; y0 = -9 - rnd.rand() * 5
        xs = x0 - np.linspace(0, 10, 12) + np.linspace(0, 12, 12) ** 1.1 * 0.3; ys = y0 - np.linspace(0, 10, 12)
        ax.plot(xs, ys, color=C["red"], lw=1.4)
    ax.set_title("Lintasan siklon tropis di sekitar Indonesia (ilustrasi)")
    save(fig, path)


# ---- paket 5
def f_keeling(path):
    t = np.arange(2014, 2024, 1 / 12)
    co2 = 397 + 2.4 * (t - 2014) + 3.2 * np.sin(2 * np.pi * (t - 2014 - 0.05) + 0.9)
    lines(t, {"CO₂": co2}, path, title="Konsentrasi CO₂ bulanan di Mauna Loa (ilustrasi)", xlabel="Tahun",
          ylabel="CO₂ (ppm)", markers=False, w=9)


def f_temp(path):
    years = np.arange(1880, 2021, 10)
    an = np.array([-0.2, -0.3, -0.3, -0.3, -0.25, -0.1, 0.0, -0.05, -0.2, -0.05, 0.2, 0.4, 0.6, 0.8, 1.0])
    fig, ax = new(9, 4.4)
    ax.bar(years, an, width=7, color=[C["red"] if v > 0 else C["blue"] for v in an])
    for y, v in [(1960, -0.2), (2020, 1.0)]:
        ax.annotate(f"{v:+.1f} °C".replace(".", ",").replace("-", "−"), (y, v), xytext=(0, 8 if v > 0 else -16), textcoords="offset points",
                    ha="center", fontsize=10, fontweight="bold")
    ax.axhline(0, color="black", lw=0.8); ax.set_ylabel("Anomali suhu global (°C)")
    ax.set_title("Anomali suhu permukaan global per dekade (rata-rata disederhanakan)")
    save(fig, path)


PWB = [300, 280, 250, 180, 110, 70, 40, 30, 50, 120, 220, 290]
EWB = [120, 115, 125, 125, 130, 125, 135, 145, 150, 145, 130, 120]


def f_neraca_air(path):
    fig, ax = new(9, 4.4)
    ax.bar(range(12), PWB, color=C["lblue"], edgecolor=C["blue"], label="Curah hujan (P)")
    ax.plot(range(12), EWB, color=C["red"], marker="o", lw=2.2, label="Evapotranspirasi acuan (ET₀)")
    ax.set_xticks(range(12)); ax.set_xticklabels(BULAN3); ax.set_ylabel("mm/bulan")
    ax.legend(frameon=False); ax.grid(axis="y", color="#E2E8F0"); ax.set_axisbelow(True)
    ax.set_title("Neraca air klimatologis sebuah kabupaten")
    save(fig, path)


def f_milank(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    for a in axs:
        a.set_xlim(-5, 5); a.set_ylim(-4, 4); a.set_aspect("equal"); a.axis("off")
    a = axs[0]
    a.add_patch(Ellipse((0, 0), 8, 5, fc="none", ec="#2D3748", lw=1.5)); a.add_patch(Ellipse((0, 0), 7, 6.3, fc="none", ec="#A0AEC0", ls="--"))
    a.add_patch(Circle((1.2, 0), 0.45, fc="#F6E05E")); a.set_title("P: bentuk orbit\nlonjong ↔ hampir bulat", fontsize=11)
    a = axs[1]
    a.add_patch(Circle((0, 0), 2, fc=C["lblue"], ec=C["blue"]))
    a.plot([0, 0], [-3.3, 3.3], ls="--", color="#A0AEC0")
    ang = np.radians(23.5); a.plot([-3 * np.sin(ang), 3 * np.sin(ang)], [-3 * np.cos(ang), 3 * np.cos(ang)], color=C["red"], lw=2)
    a.text(1.4, 3.2, "22,1°–24,5°", fontsize=10); a.set_title("Q: kemiringan sumbu\nrotasi Bumi", fontsize=11)
    a = axs[2]
    a.add_patch(Circle((0, -0.6), 1.6, fc=C["lblue"], ec=C["blue"]))
    a.plot([0, 1.2], [-0.6, 2.6], color=C["red"], lw=2)
    a.add_patch(Ellipse((0.95, 2.1), 2.4, 0.8, fc="none", ec=C["gray"], lw=1.4))
    arrow(a, 2.1, 2.3, 1.6, 2.55, ms=10, lw=1.2)
    a.set_title("R: goyangan arah\nsumbu rotasi", fontsize=11)
    save(fig, path)


MON = BULAN3
RES_N = [92, 93, 93, 92, 90, 88, 86, 84, 83, 85, 88, 91]
RES_E = [91, 91, 90, 88, 85, 82, 79, 74, 72, 71, 74, 79]


def f_waduk(path):
    lines(MON, {"Tahun normal": RES_N, "Tahun El Niño": RES_E}, path,
          title="Tinggi muka air waduk PLTA (m di atas muka laut)", ylabel="m dpl", hline=75,
          annotate=lambda ax: ax.text(0.2, 75.4, "batas minimum operasi turbin = 75 m", fontsize=10, color=C["gray"]),
          ylim=(70, 95), w=9)


# ============================ questions ============================
def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)


P0 = [
    Q("Perhatikan profil suhu vertikal atmosfer berikut.\n\nLapisan tempat ozon menyerap radiasi ultraviolet sehingga suhu justru meningkat seiring bertambahnya ketinggian ditunjukkan oleh label …",
      ["Q, yaitu stratosfer", "P, yaitu troposfer", "R, yaitu mesosfer", "S, yaitu termosfer", "Batas P–Q, yaitu tropopause"],
      "Pada grafik, suhu turun dari permukaan sampai ±12 km (lapisan P), lalu naik dari ±12 km sampai ±50 km (lapisan Q). Kenaikan suhu di Q terjadi karena molekul ozon (O₃) menyerap radiasi ultraviolet Matahari dan melepaskan energinya sebagai panas. Itulah sebabnya lapisan Q adalah stratosfer.\n\nPengecoh: P (troposfer) justru mendingin dengan ketinggian karena dipanasi dari bawah oleh permukaan Bumi. R (mesosfer) kembali mendingin karena ozon sudah sangat tipis. S (termosfer) memang memanas, tetapi penyebabnya penyerapan radiasi berenergi sangat tinggi (sinar-X dan UV ekstrem) oleh oksigen dan nitrogen, bukan ozon. Tropopause hanyalah batas lapisan, bukan lapisan penyerap UV.",
      f_atmos),
    Q("Perhatikan grafik albedo berikut. Sebidang hutan tropis dikonversi menjadi kawasan berumah atap seng terang. Jika radiasi yang datang tetap 800 W/m², perubahan energi radiasi yang diserap permukaan adalah …",
      ["Berkurang 184 W/m²", "Berkurang 280 W/m²", "Berkurang 96 W/m²", "Bertambah 184 W/m²", "Berkurang 520 W/m²"],
      "Energi yang diserap = I × (1 − α).\n• Hutan (α = 0,12): 800 × 0,88 = 704 W/m².\n• Atap seng terang (α = 0,35): 800 × 0,65 = 520 W/m².\nSelisihnya 704 − 520 = 184 W/m², artinya energi yang diserap berkurang.\n\nPengecoh: 280 W/m² adalah energi yang dipantulkan atap seng (800 × 0,35), bukan perubahan serapan. 96 W/m² adalah energi yang dipantulkan hutan. 520 W/m² adalah serapan akhir, bukan perubahannya. \"Bertambah\" membalik arah perubahan.\n\nCatatan analisis: walaupun serapan radiasi turun, kawasan permukiman tetap bisa terasa lebih panas karena hilangnya pendinginan oleh evapotranspirasi dan adanya panas buangan aktivitas manusia.",
      f_albedo),
    Q("Sebuah kota berada pada ketinggian 1.200 m dpl. Menurut rumus Braak, T = 26,3 − 0,6h (h dalam ratusan meter), suhu rata-rata tahunan kota tersebut adalah …",
      ["19,1 °C", "25,6 °C", "18,5 °C", "20,3 °C", "7,2 °C"],
      "Pada rumus Braak, h dinyatakan dalam ratusan meter, sehingga 1.200 m → h = 12.\nT = 26,3 − 0,6 × 12 = 26,3 − 7,2 = 19,1 °C.\n\nPengecoh khas:\n• 25,6 °C muncul jika h dimasukkan dalam ribuan meter (0,6 × 1,2 = 0,72), kesalahan satuan.\n• 7,2 °C hanyalah besar penurunan suhu, belum dikurangkan dari 26,3 °C.\n• 18,5 °C dan 20,3 °C berasal dari salah memakai laju penurunan (misalnya 0,65 atau 0,5 per 100 m).\nKota pada ketinggian ini (mis. dataran tinggi seperti Wonosobo) memang beriklim sejuk sehingga cocok untuk sayuran dataran tinggi.",
      None),
    Q("Perhatikan peta isobar (dalam mb) di Belahan Bumi Utara berikut. R adalah pusat tekanan rendah dan T pusat tekanan tinggi.\n\nTitik yang kemungkinan besar memiliki kecepatan angin permukaan paling tinggi adalah …",
      ["Titik P", "Titik Q", "Titik S", "Titik U", "Pusat T karena tekanannya tertinggi"],
      "Kecepatan angin ditentukan oleh gradien barometrik, yaitu besarnya perbedaan tekanan per satuan jarak. Pada peta isobar, gradien besar ditandai oleh isobar yang rapat. Titik P berada di antara pusat R dan pusat T, tempat isobar paling rapat, sehingga gaya gradien tekanan di P paling besar dan angin paling kencang.\n\nTitik Q, S, dan U berada pada daerah dengan isobar yang lebih renggang. Pusat T memang bertekanan tertinggi, tetapi yang menggerakkan angin adalah perbedaan tekanan, bukan besar tekanannya; di pusat antisiklon isobar justru renggang dan angin cenderung tenang.",
      f_isobar_speed),
    Q("Perhatikan diagram curah hujan bulanan tiga stasiun berikut.\n\nPasangan pola curah hujan yang tepat untuk stasiun X, Y, dan Z berturut-turut adalah …",
      ["Monsunal, ekuatorial, lokal", "Ekuatorial, monsunal, lokal", "Lokal, ekuatorial, monsunal", "Monsunal, lokal, ekuatorial", "Ekuatorial, lokal, monsunal"],
      "Cara membaca: hitung jumlah puncak dan tentukan bulan puncaknya.\n• X: satu puncak pada Desember–Februari dan satu lembah pada Juni–Agustus (bentuk huruf U) → pola monsunal, khas Jawa, Bali, Nusa Tenggara.\n• Y: dua puncak, yaitu sekitar Maret–April dan Oktober–November → pola ekuatorial, karena Matahari dua kali melintasi khatulistiwa (ekuinoks) sehingga konveksi maksimum terjadi dua kali.\n• Z: satu puncak pada Mei–Juli, berkebalikan dengan monsunal (bentuk ∩) → pola lokal, misalnya Ambon dan sebagian Maluku.\nOpsi lain menukar karakter grafik tersebut.",
      f_pola3),
    Q("El Niño sering dikaitkan dengan kemarau panjang di sebagian besar Indonesia. Rantai sebab-akibat yang paling tepat adalah …",
      ["Pasat melemah, kolam air hangat bergeser ke Pasifik tengah-timur, udara di atas Indonesia cenderung turun",
       "Pasat menguat, air hangat menumpuk di barat Pasifik, sehingga uap air di atas Indonesia ikut berkurang",
       "Suhu muka laut di sekitar Indonesia meningkat, penguapan naik, sehingga awan justru sulit tumbuh",
       "Monsun Asia menguat, uap air dari Laut Cina Selatan ditahan di utara, sehingga tidak sampai Indonesia",
       "Upwelling di pantai Peru menguat, air dingin menyebar ke barat, sehingga suhu laut Indonesia naik"],
      "Pada kondisi normal, pasat timur mendorong air hangat ke Pasifik barat sehingga udara naik dan banyak awan terbentuk di atas Indonesia (cabang naik sirkulasi Walker). Saat El Niño, pasat melemah sehingga kolam air hangat bergeser ke Pasifik tengah-timur. Pusat konveksi ikut berpindah ke timur, sedangkan di atas Indonesia udara cenderung turun (subsidensi). Akibatnya pembentukan awan berkurang dan musim kemarau lebih panjang/kering.\n\nPengecoh: \"pasat menguat\" dan \"air hangat menumpuk di barat\" adalah ciri La Niña. Suhu laut Indonesia saat El Niño umumnya lebih dingin dari normal, bukan lebih hangat. Upwelling Peru justru melemah saat El Niño. Monsun Asia tidak menjadi mekanisme utama ENSO.",
      None),
    Q("Perhatikan gambar penampang pegunungan berikut. Udara lembap dari laut bergerak naik melewati pegunungan, lalu turun ke Kota K di lereng bawah angin.\n\nSuhu udara yang tiba di Kota K adalah …",
      ["30,4 °C", "24,0 °C", "22,4 °C", "28,0 °C", "10,4 °C"],
      "Kerjakan bertahap:\n1) Naik kering 0 → 800 m: turun 8 × 1 °C = 8 °C → 28 − 8 = 20 °C (dasar awan).\n2) Naik jenuh 800 → 2.400 m (1.600 m): turun 16 × 0,6 °C = 9,6 °C → 10,4 °C di puncak.\n3) Turun ke Kota K 2.400 → 400 m (2.000 m) memakai laju kering karena uap air sudah jatuh sebagai hujan di lereng hadap angin: naik 20 × 1 °C = 20 °C → 30,4 °C.\n\nPengecoh: 10,4 °C berhenti di puncak (hitungan setengah jalan). 22,4 °C muncul jika saat turun memakai laju jenuh. 24,0 °C muncul jika seluruh pendakian dianggap kering. 28,0 °C mengira suhu kembali seperti semula. Inilah efek fohn: udara di lereng bawah angin lebih panas dan kering, misalnya angin Gending di Probolinggo.",
      f_fohn),
    Q("Sebuah TPA melepaskan 500 ton metana (GWP 28) dan sebuah lahan pertanian melepaskan 20 ton dinitrogen oksida (GWP 265) per tahun. Total emisi kedua sumber dalam CO₂-ekuivalen adalah …",
      ["19.300 ton CO₂-e", "14.000 ton CO₂-e", "5.300 ton CO₂-e", "520 ton CO₂-e", "133.060 ton CO₂-e"],
      "CO₂-ekuivalen = massa gas × GWP.\n• Metana: 500 × 28 = 14.000 ton CO₂-e.\n• N₂O: 20 × 265 = 5.300 ton CO₂-e.\nTotal = 19.300 ton CO₂-e.\n\nPengecoh: 14.000 dan 5.300 hanya menghitung salah satu sumber. 520 ton hanya menjumlahkan massa tanpa mengalikan GWP. 133.060 muncul bila GWP kedua gas tertukar (500 × 265 + 20 × 28). Pelajaran: walaupun massanya kecil, N₂O menyumbang porsi besar karena GWP-nya sangat tinggi.",
      None),
    Q("Perhatikan klimograf Stasiun M berikut. Gunakan kriteria Köppen: suhu bulan terdingin ≥ 18 °C → kelompok A; Af jika hujan bulan terkering ≥ 60 mm; jika < 60 mm, Am bila hujan bulan terkering ≥ 100 − (P/25), selain itu Aw.\n\nTipe iklim Stasiun M adalah …",
      ["Am (monsun tropis)", "Af (hutan hujan tropis)", "Aw (sabana tropis)", "Cwa (subtropis musim dingin kering)", "BSh (stepa panas)"],
      "Langkah:\n1) Suhu bulan terdingin ±26,2 °C ≥ 18 °C → kelompok A.\n2) Hujan bulan terkering (Juli) 40 mm < 60 mm → bukan Af.\n3) Ambang Am = 100 − 2.400/25 = 100 − 96 = 4 mm. Karena 40 mm ≥ 4 mm, tipe iklimnya Am.\n\nPengecoh: Af dipilih jika lupa memeriksa bulan terkering. Aw dipilih jika ambang dihitung keliru (misalnya 100 − 24 = 76 mm). Kelompok C tidak mungkin karena suhu terdingin jauh di atas 18 °C. Kelompok B (kering) tidak sesuai dengan hujan tahunan 2.400 mm. Am menggambarkan wilayah yang sangat basah tetapi memiliki musim kering singkat, khas sebagian Sumatra dan Kalimantan bagian selatan.",
      f_klim_am),
    Q("Rata-rata sebuah stasiun memiliki 3,6 bulan kering (< 60 mm) dan 7,2 bulan basah (> 100 mm) per tahun. Berdasarkan klasifikasi Schmidt-Ferguson (A: Q < 14,3%; B: 14,3–33,3%; C: 33,3–60%; D: 60–100%; E: 100–167%), tipe iklim stasiun tersebut adalah …",
      ["Tipe C, Q = 50%", "Tipe B, Q = 30%", "Tipe D, Q = 72%", "Tipe F, Q = 200%", "Tipe E, Q = 136%"],
      "Rumus Schmidt-Ferguson: Q = (rata-rata bulan kering ÷ rata-rata bulan basah) × 100%.\nQ = 3,6 ÷ 7,2 × 100% = 50%. Nilai 50% berada pada rentang 33,3–60% → tipe C (agak basah).\n\nPengecoh: Q = 200% (tipe F) muncul bila pembilang dan penyebut tertukar (7,2 ÷ 3,6). Nilai 72% dan 136% tidak memiliki dasar hitungan yang benar. Tipe B memerlukan Q jauh lebih kecil, misalnya bulan kering hanya ±2 bulan dengan 8 bulan basah.",
      None),
]

P1 = [
    Q("Perhatikan diagram neraca radiasi gelombang pendek berikut.\n\nBerdasarkan diagram tersebut, albedo planet Bumi adalah …",
      ["30%", "22%", "8%", "50%", "70%"],
      "Albedo planet = bagian radiasi Matahari yang dipantulkan kembali ke angkasa ÷ radiasi yang datang.\nRadiasi yang dipantulkan terdiri atas P (oleh awan dan udara) = 22 satuan dan Q (oleh permukaan) = 8 satuan, sehingga totalnya 30 satuan dari 100 satuan → albedo 30%.\n\nPengecoh: 22% dan 8% hanya menghitung salah satu jalur pantulan. 50% adalah radiasi yang diserap permukaan (S). 70% adalah total yang diserap sistem Bumi–atmosfer (R + S = 20 + 50), yaitu kebalikan albedo. Energi yang diserap inilah yang kemudian dipancarkan kembali sebagai radiasi gelombang panjang.",
      f_neraca),
    Q("Menurut hukum Wien, λmaks = 2.898/T (λ dalam µm, T dalam kelvin). Jika suhu rata-rata permukaan Bumi 288 K, puncak pancaran radiasi Bumi berada pada panjang gelombang sekitar …",
      ["10 µm, inframerah termal", "0,5 µm, cahaya tampak", "1 µm, inframerah dekat", "0,1 µm, ultraviolet", "100 µm, gelombang mikro"],
      "λmaks = 2.898 ÷ 288 ≈ 10,06 µm. Panjang gelombang ini termasuk inframerah termal (gelombang panjang).\n\nBandingkan dengan Matahari (±5.800 K): λmaks = 2.898 ÷ 5.800 ≈ 0,5 µm (cahaya tampak). Perbedaan ini menjadi dasar efek rumah kaca: atmosfer relatif tembus terhadap radiasi gelombang pendek dari Matahari, tetapi gas rumah kaca (H₂O, CO₂, CH₄) menyerap radiasi gelombang panjang yang dipancarkan Bumi.\n\nPengecoh 0,5 µm adalah puncak radiasi Matahari, bukan Bumi. 1 µm, 0,1 µm, dan 100 µm tidak sesuai dengan hasil hitungan.",
      None),
    Q("Perhatikan grafik suhu per jam dua stasiun pada hari cerah yang sama berikut.\n\nPernyataan yang paling tepat berdasarkan grafik adalah …",
      ["Stasiun A di tepi pantai karena kapasitas panas air yang besar meredam amplitudo suhu",
       "Stasiun A di pedalaman karena suhu maksimumnya tercapai lebih lambat dari stasiun B",
       "Stasiun B di tepi pantai karena angin laut membuat suhu siangnya naik lebih tinggi",
       "Stasiun B di pegunungan tinggi karena suhu rata-rata hariannya lebih tinggi dari A",
       "Kedua stasiun beriklim sama karena puncak suhu keduanya terjadi pada jam yang sama"],
      "Grafik menunjukkan amplitudo harian Stasiun A sekitar 6 °C (24–30 °C), sedangkan Stasiun B sekitar 14 °C (18–32 °C). Air laut memiliki kapasitas panas jenis besar, menyerap panas ke lapisan lebih dalam, dan menggunakan sebagian energi untuk penguapan. Akibatnya suhu udara di tepi pantai berubah lebih lambat dan amplitudonya kecil. Stasiun A cocok sebagai stasiun pantai, sedangkan B sebagai stasiun pedalaman (kontinental).\n\nPengecoh: angin laut justru menurunkan suhu siang di pantai. Suhu rata-rata B (25 °C) lebih rendah daripada A (27 °C), dan pegunungan tinggi tidak bisa disimpulkan hanya dari amplitudo. Waktu puncak yang sama tidak berarti iklimnya sama.",
      f_diurnal),
    Q("Perhatikan hasil pengukuran radiosonde pada pagi hari di sebuah kota lembah berikut.\n\nKondisi pada lapisan K dan dampaknya terhadap kualitas udara kota adalah …",
      ["Inversi suhu; udara stabil sehingga polutan terperangkap dekat permukaan",
       "Lapse rate normal; udara labil sehingga polutan cepat menyebar ke atas",
       "Inversi suhu; udara labil sehingga awan konvektif cepat terbentuk di atas kota",
       "Lapisan isotermal; tidak ada pengaruh terhadap penyebaran polutan di kota",
       "Lapse rate superadiabatik; polutan tertahan karena udara bergerak mendatar"],
      "Pada lapisan K (300–600 m), suhu naik dari ±20,2 °C menjadi ±24 °C seiring bertambahnya ketinggian. Kondisi suhu yang meningkat terhadap ketinggian disebut inversi suhu. Udara dingin dan berat berada di bawah udara hangat, sehingga gerak vertikal tertekan (sangat stabil). Asap kendaraan dan industri tidak dapat naik menembus lapisan inversi dan terkumpul di dekat permukaan, apalagi di kota lembah yang dikelilingi perbukitan.\n\nPengecoh: lapse rate normal adalah suhu turun terhadap ketinggian (lapisan di bawah 300 m). Inversi tidak membuat udara labil. Lapisan isotermal berarti suhu tetap, bukan meningkat. Superadiabatik adalah kebalikan inversi, yaitu sangat labil.",
      f_inversi),
    Q("Perhatikan transek suhu malam hari yang melintasi sebuah kota berikut.\n\nPenyebab utama penurunan suhu di titik P dibandingkan kawasan di kiri-kanannya adalah …",
      ["Vegetasi dan tanah terbuka menambah pendinginan evapotranspirasi serta menyimpan sedikit panas",
       "Kawasan P memiliki albedo lebih rendah sehingga menyerap radiasi lebih banyak pada siang hari",
       "Gedung di kawasan P lebih tinggi sehingga radiasi gelombang panjang terperangkap di antaranya",
       "Kawasan P menerima panas buangan kendaraan lebih besar dari kawasan industri di sebelahnya",
       "Kawasan P terletak pada ketinggian lebih besar sehingga suhunya turun mengikuti lapse rate"],
      "Grafik memperlihatkan pola pulau bahang kota (urban heat island): suhu naik dari sawah ke pusat bisnis, lalu turun tajam di taman kota P, dan naik lagi di kawasan industri. Di taman, vegetasi dan tanah lembap menyerap energi untuk evapotranspirasi (panas laten), tajuk pohon memberi naungan pada siang hari, dan material alami menyimpan panas jauh lebih sedikit daripada beton dan aspal. Pada malam hari, taman pun lebih cepat mendingin.\n\nPengecoh: albedo rendah dan gedung tinggi (efek ngarai kota) justru menaikkan suhu malam. Panas buangan tertinggi berada di kawasan industri dan pusat bisnis. Tidak ada informasi bahwa taman berada di tempat lebih tinggi; selisih ketinggian kecil pun tidak bisa menjelaskan selisih ±2,5 °C.",
      f_uhi),
    Q("Sebuah perkebunan berada pada ketinggian ±1.800 m dpl. Menurut pembagian zona suhu Junghuhn, perkebunan tersebut berada pada zona … dengan komoditas yang paling sesuai, yaitu …",
      ["Sejuk; teh, kina, dan sayuran dataran tinggi", "Sedang; kopi, tembakau, dan padi gogo",
       "Panas; kelapa, tebu, dan padi sawah", "Dingin; lumut dan rumput pegunungan",
       "Sejuk; kelapa sawit, karet, dan kakao"],
      "Junghuhn membagi zona suhu di Jawa sebagai berikut: zona panas 0–700 m (padi, jagung, tebu, kelapa), zona sedang 700–1.500 m (kopi, tembakau, teh, sayuran), zona sejuk 1.500–2.500 m (teh, kina, kopi, sayuran dataran tinggi), dan zona dingin > 2.500 m (lumut, rumput, hampir tanpa budidaya).\nKetinggian 1.800 m berada di zona sejuk dengan suhu rata-rata ±15–16 °C (Braak: 26,3 − 0,6 × 18 = 15,5 °C). Komoditas yang sesuai adalah teh, kina, dan sayuran dataran tinggi.\n\nPengecoh: kelapa sawit, karet, dan kakao adalah tanaman dataran rendah tropis yang membutuhkan suhu tinggi. Zona sedang dan zona panas tidak sesuai dengan ketinggian 1.800 m.",
      None),
    Q("Stasiun A pada ketinggian 300 m mencatat suhu 25,0 °C. Dengan laju penurunan normal 0,6 °C per 100 m, suhu di puncak B (1.700 m) pada saat yang sama diperkirakan …",
      ["16,6 °C", "14,8 °C", "16,1 °C", "8,4 °C", "33,4 °C"],
      "Selisih ketinggian = 1.700 − 300 = 1.400 m = 14 ratus meter.\nPenurunan suhu = 14 × 0,6 = 8,4 °C.\nSuhu di B = 25,0 − 8,4 = 16,6 °C.\n\nPengecoh: 14,8 °C muncul jika memakai ketinggian B secara penuh (17 × 0,6 = 10,2 °C) tanpa mengurangkan ketinggian A. 16,1 °C muncul bila langsung memakai rumus Braak untuk 1.700 m (26,3 − 10,2) sehingga data aktual Stasiun A diabaikan; padahal soal meminta suhu pada saat yang sama berdasarkan pengukuran A. 8,4 °C hanyalah besar penurunan suhu. 33,4 °C muncul jika penurunan malah ditambahkan.",
      None),
    Q("Perhatikan kondisi suhu daratan dan laut pada dini hari berikut.\n\nAngin yang terbentuk pada kondisi tersebut adalah …",
      ["Angin darat, bertiup dari daratan bertekanan tinggi ke laut bertekanan rendah",
       "Angin laut, bertiup dari laut bertekanan tinggi ke daratan bertekanan rendah",
       "Angin darat, bertiup dari laut bertekanan rendah ke daratan bertekanan tinggi",
       "Angin laut, bertiup dari daratan bertekanan rendah ke laut bertekanan tinggi",
       "Angin fohn, bertiup menuruni lereng dari daratan yang lebih dingin ke laut"],
      "Pada malam hari daratan melepaskan panas lebih cepat sehingga lebih dingin (22 °C) daripada laut (27 °C). Udara di atas daratan yang dingin lebih rapat dan bertekanan relatif tinggi, sedangkan udara di atas laut yang lebih hangat memuai dan bertekanan relatif rendah. Angin permukaan selalu bergerak dari tekanan tinggi ke rendah, yaitu dari darat ke laut. Angin ini disebut angin darat dan dimanfaatkan nelayan tradisional untuk berangkat melaut pada dini hari.\n\nPengecoh: angin laut terjadi pada siang hari ketika kondisinya terbalik. Opsi yang menyebut angin bergerak dari tekanan rendah ke tinggi melanggar prinsip dasar gradien tekanan. Angin fohn adalah angin turun gunung yang kering dan panas, tidak terkait dengan selisih suhu darat-laut.",
      f_darat_laut),
    Q("Pasangan nama angin fohn lokal dan wilayah kemunculannya yang tepat adalah …",
      ["Angin Gending – Pasuruan dan Probolinggo", "Angin Kumbang – Deli dan Langkat, Sumatra Utara",
       "Angin Bohorok – Cirebon dan Brebes", "Angin Brubu – Biak dan Supiori, Papua", "Angin Wambraw – Makassar, Sulawesi Selatan"],
      "Beberapa angin fohn lokal di Indonesia:\n• Gending: Pasuruan–Probolinggo (Jawa Timur), turun dari kompleks Tengger–Bromo dan Argopuro.\n• Kumbang: Cirebon, Brebes, dan Tegal.\n• Bohorok: Deli, Sumatra Utara, sering merusak tanaman tembakau.\n• Brubu: Makassar, Sulawesi Selatan.\n• Wambraw: Biak, Papua.\nSemua opsi selain Gending menukar nama angin dengan wilayahnya. Ciri umum angin fohn adalah panas dan kering karena udara yang turun di lereng bawah angin memanas dengan laju adiabatik kering, setelah uap airnya dijatuhkan sebagai hujan di lereng hadap angin.",
      None),
    Q("Perhatikan peta isobar berikut. Jarak titik A ke titik B adalah 333 km.\n\nBesar gradien barometrik antara A dan B (dinyatakan dalam mb per 111 km) adalah …",
      ["4 mb per 111 km", "12 mb per 111 km", "3 mb per 111 km", "1,3 mb per 111 km", "36 mb per 111 km"],
      "Tekanan di A berada pada isobar 1.014 mb dan B pada isobar 1.002 mb, sehingga selisih tekanannya 12 mb.\nJarak 333 km = 333 ÷ 111 = 3 satuan (1 satuan = 111 km, setara 1° lintang).\nGradien barometrik = 12 ÷ 3 = 4 mb per 111 km.\n\nPengecoh: 12 mb adalah selisih tekanan total tanpa dibagi jarak. 3 adalah jumlah satuan jaraknya. 1,3 muncul bila pembagian dibalik (4 ÷ 3). 36 muncul bila selisih tekanan dikalikan dengan jarak. Semakin besar gradien barometrik, semakin kencang angin; angin bergerak dari A (tekanan tinggi) ke arah B.",
      f_gradien),
]

P2 = [
    Q("Perhatikan model sirkulasi atmosfer tiga sel di Belahan Bumi Utara berikut.\n\nGurun-gurun besar dunia seperti Sahara dan Arab umumnya terletak di sekitar sabuk … karena …",
      ["L; udara turun dari sel Hadley memanas dan kering", "K; udara naik kuat sehingga hujan sering turun",
       "M; udara naik di front kutub sehingga awan menipis", "N; udara turun yang sangat dingin menghambat hujan",
       "L; angin pasat dan angin baratan bertemu lalu naik"],
      "Sabuk L berada pada lintang ±30°. Di sini cabang udara turun dari sel Hadley (dan sel Ferrel) membentuk sabuk tekanan tinggi subtropis. Udara yang turun memanas secara adiabatik sehingga kelembapan relatifnya rendah; awan sulit terbentuk dan curah hujan sangat sedikit. Itulah sebabnya gurun panas besar (Sahara, Arab, Thar, Gurun Australia) terletak di sekitar 20°–30° lintang.\n\nPengecoh: K (0°, ITCZ) adalah daerah udara naik dan hujan tinggi. M (60°) adalah front kutub, daerah udara naik dengan banyak hujan frontal. N (90°) memang kering, tetapi gurun kutub bukan contoh yang ditanyakan. Pasat dan angin baratan justru menyebar (divergen) dari sabuk L, tidak bertemu di situ.",
      f_tricell),
    Q("Perhatikan peta pola angin permukaan rata-rata berikut.\n\nPola angin tersebut paling sesuai dengan kondisi …",
      ["Desember–Februari; monsun barat yang membawa banyak uap air ke Jawa",
       "Juni–Agustus; monsun timur yang kering dari Australia menuju Asia",
       "Maret–April; masa peralihan dengan angin lemah dan arah tidak menentu",
       "Juni–Agustus; monsun barat yang kering karena melewati gurun Australia",
       "Desember–Februari; angin pasat tenggara yang menembus ekuator ke utara"],
      "Peta menunjukkan tekanan tinggi di daratan Asia dan tekanan rendah di Australia. Kondisi ini terjadi saat Matahari berada di Belahan Bumi Selatan (Desember–Februari): Asia dingin (tekanan tinggi), Australia panas (tekanan rendah). Angin bertiup dari timur laut di Laut Cina Selatan, lalu setelah melintasi ekuator dibelokkan gaya Coriolis ke kiri sehingga di atas Laut Jawa datang dari barat laut–barat. Angin ini melewati samudra luas sehingga lembap dan membawa musim hujan di Jawa (monsun barat).\n\nPengecoh: monsun timur (Juni–Agustus) arahnya berlawanan dan bersifat kering. Masa peralihan tidak memiliki pola arah yang tegas. Pasat tenggara tidak menembus ekuator ke utara pada Desember–Februari.",
      f_monsun),
    Q("Pada bulan Juli, ITCZ berada di sekitar 10°–15° LU. Dampak posisi ITCZ tersebut terhadap wilayah Nusa Tenggara Timur adalah …",
      ["Mengalami puncak kemarau karena jauh dari zona konvergensi",
       "Mengalami puncak hujan karena berada tepat di bawah ITCZ",
       "Mengalami hujan merata karena ITCZ selalu di khatulistiwa",
       "Mengalami angin baratan kuat yang membawa uap air dari Samudra Hindia",
       "Mengalami badai siklon karena ITCZ melintas di atasnya"],
      "ITCZ (Inter-Tropical Convergence Zone) adalah zona pertemuan pasat dari kedua belahan Bumi; udara naik kuat dan membentuk awan hujan. Posisinya mengikuti gerak semu tahunan Matahari dengan sedikit keterlambatan. Pada Juli, ITCZ berada di BBU (10°–15° LU), sehingga wilayah Indonesia bagian selatan seperti NTT (±8°–11° LS) berada jauh dari zona konvergensi. Pada saat yang sama, angin muson timur yang kering dari Australia bertiup sehingga NTT mengalami puncak kemarau.\n\nPengecoh: NTT tidak berada di bawah ITCZ pada Juli. ITCZ tidak selalu di khatulistiwa. Angin baratan dari Samudra Hindia bertiup sekitar Desember–Februari. Siklon tidak terbentuk di ITCZ dekat ekuator karena gaya Coriolis sangat lemah.",
      None),
    Q("Perhatikan grafik suhu udara dan titik embun di sebuah stasiun berikut. Gunakan pendekatan tinggi dasar awan h ≈ 125 × (T − Td) meter.\n\nPerkiraan tinggi dasar awan konvektif pada pukul 14.00 adalah …",
      ["1.000 m", "800 m", "3.000 m", "4.000 m", "1.250 m"],
      "Pukul 14.00 suhu udara T = 32 °C dan titik embun Td = 24 °C, sehingga selisihnya (T − Td) = 8 °C.\nh ≈ 125 × 8 = 1.000 m.\n\nPengecoh: 800 m muncul bila koefisien 100 dipakai. 3.000 m muncul bila hanya Td (24) yang dikalikan 125. 4.000 m muncul bila hanya T (32) yang dikalikan. 1.250 m muncul bila selisih dibaca 10 °C.\n\nPerhatikan pula bahwa selisih T − Td paling kecil terjadi menjelang pagi (suhu terendah), sehingga kelembapan relatif tertinggi juga terjadi pada saat itu dan berpeluang membentuk embun atau kabut.",
      f_td),
    Q("Udara bersuhu 30 °C memiliki tekanan uap aktual 21 hPa dan tekanan uap jenuh 42 hPa. Pada malam hari suhu turun menjadi 20 °C (tekanan uap jenuh 23 hPa), sedangkan kandungan uap airnya tetap. Kelembapan relatif pada malam hari menjadi sekitar …",
      ["91%", "50%", "100%", "55%", "110%"],
      "Kelembapan relatif RH = e ÷ es × 100%.\n• Siang (30 °C): RH = 21 ÷ 42 × 100% = 50%.\n• Malam (20 °C): kandungan uap air tetap (e = 21 hPa), tetapi es turun menjadi 23 hPa. RH = 21 ÷ 23 × 100% ≈ 91%.\n\nPendinginan tanpa penambahan uap air menaikkan RH karena kapasitas udara menampung uap air berkurang. Udara belum jenuh (RH < 100%) karena e masih lebih kecil daripada es; titik embun belum tercapai.\n\nPengecoh: 50% adalah RH siang hari. 100% dianggap jenuh, padahal e < es. 110% tidak mungkin terjadi pada udara bebas dalam kondisi normal. 55% berasal dari pembagian yang keliru (23 ÷ 42).",
      None),
    Q("Perhatikan empat gambar mekanisme pembentukan hujan berikut.\n\nMekanisme yang paling dominan menghasilkan hujan di sekitar lintang 60° adalah …",
      ["Gambar 3, hujan frontal", "Gambar 1, hujan konvektif", "Gambar 2, hujan orografis",
       "Gambar 4, hujan konvergensi", "Gambar 1 dan 4 secara bersamaan"],
      "Keempat gambar menunjukkan: (1) hujan konvektif, udara naik karena pemanasan permukaan; (2) hujan orografis, udara dipaksa naik oleh lereng gunung; (3) hujan frontal, udara hangat naik di atas baji udara dingin; dan (4) hujan konvergensi, dua aliran udara bertemu lalu naik.\nLintang ±60° adalah lokasi front kutub, tempat udara kutub yang dingin bertemu angin baratan yang lebih hangat. Udara hangat terangkat di sepanjang bidang front sehingga hujan frontal mendominasi, misalnya di Eropa Barat Laut.\n\nPengecoh: hujan konvektif dan konvergensi dominan di wilayah tropis dekat ekuator. Hujan orografis bersifat lokal dan bergantung pada keberadaan pegunungan, bukan pada lintang.",
      f_hujan4),
    Q("Hujan es (hail) yang sesekali terjadi di Indonesia, misalnya di Bandung atau Yogyakarta, paling mungkin terbentuk dari …",
      ["Awan cumulonimbus dengan arus udara naik yang sangat kuat", "Awan stratus rendah yang menutupi kota sepanjang pagi",
       "Awan cirrus tinggi yang tersusun seluruhnya dari kristal es", "Kabut radiasi yang membeku di permukaan saat malam cerah",
       "Awan altostratus pada sistem front hangat yang luas"],
      "Hujan es terbentuk di awan cumulonimbus yang menjulang hingga di atas ketinggian beku (±4,5–5 km di tropis). Arus udara naik (updraft) yang sangat kuat membawa butir air dan es naik-turun berkali-kali di dalam awan sehingga lapisan es bertambah tebal. Ketika butir es terlalu berat untuk ditahan updraft, butir itu jatuh ke permukaan sebelum sempat mencair seluruhnya. Peristiwa ini biasanya terjadi pada siang–sore hari di masa peralihan musim, saat pemanasan permukaan kuat.\n\nPengecoh: stratus dan altostratus berlapis tipis dengan gerak vertikal lemah. Cirrus memang tersusun atas kristal es, tetapi terlalu tinggi dan tipis untuk menghasilkan presipitasi yang mencapai tanah. Kabut tidak menghasilkan butiran es.",
      None),
    Q("Perhatikan grafik rata-rata curah hujan bulanan Stasiun J dan Stasiun K berikut.\n\nPenjelasan yang paling tepat untuk pola curah hujan Stasiun K adalah …",
      ["Pola lokal; puncak saat monsun timur menyerap uap air laut lalu terangkat orografis",
       "Pola monsunal; puncak hujan saat monsun barat yang lembap dari Samudra Pasifik",
       "Pola ekuatorial; puncak hujan saat Matahari tepat di atas khatulistiwa",
       "Pola lokal; puncak hujan saat ITCZ berada tepat di atas wilayah tersebut",
       "Pola monsunal; puncak hujan saat El Niño membuat suhu muka laut menghangat"],
      "Stasiun J (puncak Desember–Februari, lembah Juli–Agustus) adalah pola monsunal. Stasiun K justru memuncak pada Mei–Juli, berlawanan dengan J; inilah pola lokal yang khas di Ambon dan sebagian Maluku. Pada Mei–Agustus, monsun timur bertiup dari Australia. Saat melintasi Laut Banda dan Laut Arafura yang luas, angin ini menyerap banyak uap air. Ketika menabrak pegunungan Pulau Ambon dan Seram, udara terangkat sehingga terjadi hujan orografis yang lebat.\n\nPengecoh: pola monsunal memuncak pada Desember–Februari. Pola ekuatorial memiliki dua puncak (Maret dan Oktober). ITCZ pada Juni–Juli berada di BBU, jauh dari Maluku. El Niño justru menurunkan hujan di Indonesia bagian timur.",
      f_ambon),
    Q("Laju penurunan suhu lingkungan (environmental lapse rate) di suatu lokasi adalah 0,8 °C/100 m. Jika laju adiabatik kering 1,0 °C/100 m dan laju adiabatik jenuh 0,6 °C/100 m, kondisi stabilitas atmosfer di lokasi tersebut adalah …",
      ["Labil bersyarat; labil bagi udara jenuh tetapi stabil bagi udara tidak jenuh",
       "Labil mutlak; parsel udara kering maupun jenuh akan terus naik dengan sendirinya",
       "Stabil mutlak; parsel udara kering maupun jenuh akan kembali ke posisi awal",
       "Labil bersyarat; labil bagi udara tidak jenuh tetapi stabil bagi udara jenuh",
       "Netral; parsel udara selalu bersuhu sama dengan lingkungan di setiap ketinggian"],
      "Bandingkan laju lingkungan (ELR) dengan laju parsel:\n• Parsel tidak jenuh mendingin 1,0 °C/100 m, lebih cepat dari lingkungan (0,8). Parsel menjadi lebih dingin daripada sekitarnya sehingga cenderung turun kembali → stabil.\n• Parsel jenuh mendingin 0,6 °C/100 m, lebih lambat dari lingkungan (0,8). Parsel tetap lebih hangat daripada sekitarnya sehingga terus naik → labil.\nKarena 0,6 < ELR < 1,0, kondisinya labil bersyarat: kelabilan bergantung pada apakah parsel sudah jenuh. Kondisi ini umum di atmosfer tropis dan menjelaskan mengapa awan cumulus bisa tumbuh menjadi cumulonimbus setelah mencapai dasar awan.\n\nPengecoh: labil mutlak membutuhkan ELR > 1,0; stabil mutlak membutuhkan ELR < 0,6. Opsi labil bersyarat yang lain membalik syaratnya.",
      None),
    Q("Perhatikan diagram sirkulasi Walker pada kondisi normal berikut.\n\nSaat terjadi El Niño, komponen sirkulasi yang melemah paling nyata sehingga memicu pergeseran kolam air hangat ke timur adalah …",
      ["S, angin pasat timur di permukaan", "P, udara naik di atas Indonesia", "Q, aliran udara ke timur di lapisan atas",
       "R, udara turun di atas Peru", "Semua komponen menguat secara bersamaan"],
      "Sirkulasi Walker normal: udara naik di atas Indonesia (P), mengalir ke timur di lapisan atas (Q), turun di atas Pasifik timur dekat Peru (R), dan kembali ke barat sebagai angin pasat timur di permukaan (S).\nEl Niño diawali dengan melemahnya pasat timur (S). Karena tidak lagi didorong kuat ke barat, air hangat di Pasifik barat mengalir kembali ke timur, termoklin di timur menjadi lebih dalam, dan upwelling di Peru melemah. Akibatnya pusat konveksi berpindah ke Pasifik tengah-timur.\n\nPengecoh: P (udara naik di atas Indonesia) memang melemah, tetapi sebagai akibat, bukan pemicu pergeseran air hangat. Q dan R ikut berubah sebagai bagian dari sirkulasi yang bergeser. \"Semua menguat\" adalah ciri La Niña.",
      f_walker),
]

P3 = [
    Q("Perhatikan klimograf Stasiun W berikut. Gunakan kriteria Köppen: A jika suhu bulan terdingin ≥ 18 °C; Af jika hujan bulan terkering ≥ 60 mm; jika tidak, Am bila hujan bulan terkering ≥ 100 − (P/25), selain itu Aw.\n\nTipe iklim Stasiun W adalah …",
      ["Aw, karena hujan bulan terkering di bawah ambang Am", "Am, karena hujan tahunan lebih dari 1.000 mm",
       "Af, karena suhu semua bulan di atas 18 °C", "BSh, karena memiliki musim kemarau yang panjang",
       "Cw, karena musim keringnya terjadi pada pertengahan tahun"],
      "Langkah:\n1) Suhu bulan terdingin ±25 °C ≥ 18 °C → kelompok A.\n2) Hujan bulan terkering (Juli) = 10 mm < 60 mm → bukan Af.\n3) Ambang Am = 100 − 1.500/25 = 100 − 60 = 40 mm. Karena 10 mm < 40 mm, tipe iklim Stasiun W adalah Aw (sabana tropis).\n\nPengecoh: Am salah karena hujan bulan terkering berada di bawah ambang 40 mm; jumlah hujan tahunan saja tidak cukup. Af keliru karena hanya memeriksa suhu. BSh membutuhkan hujan tahunan di bawah ambang kering (sekitar < 500–700 mm di tropis). Cw membutuhkan suhu bulan terdingin < 18 °C. Iklim Aw khas wilayah NTT dan sebagian Jawa Timur.",
      f_klim_aw),
    Q("Perhatikan tabel rekap bulan kering dan bulan basah Stasiun H berikut.\n\nBerdasarkan klasifikasi Schmidt-Ferguson (C: 33,3–60%; D: 60–100%; E: 100–167%), tipe iklim Stasiun H adalah …",
      ["D, dengan Q ≈ 66,7%", "C, dengan Q ≈ 50,0%", "E, dengan Q ≈ 150%", "C, dengan Q ≈ 40,0%", "D, dengan Q ≈ 80,0%"],
      "Schmidt-Ferguson memakai nilai rata-rata selama periode pengamatan.\n• Rata-rata bulan kering = (4 + 5 + 3 + 6 + 2) ÷ 5 = 20 ÷ 5 = 4,0.\n• Rata-rata bulan basah = (6 + 5 + 7 + 4 + 8) ÷ 5 = 30 ÷ 5 = 6,0.\n• Q = 4,0 ÷ 6,0 × 100% ≈ 66,7% → tipe D (sedang).\n\nPengecoh: Q = 150% muncul bila pembilang dan penyebut tertukar (6 ÷ 4). Q = 50% dan 40% berasal dari salah menjumlah atau hanya memakai satu tahun tertentu (misalnya 2019: 4/6 = 66,7% tetap D; 2021: 3/7 ≈ 43%). Q = 80% tidak sesuai dengan data. Nilai Q dihitung dari rata-rata, bukan rata-rata Q per tahun.",
      f_sf_table),
    Q("Klasifikasi Oldeman memakai jumlah bulan basah berurutan (> 200 mm) untuk zona utama (A > 9; B 7–9; C 5–6; D 3–4; E < 3) dan bulan kering berurutan (< 100 mm) untuk subzona (1: < 2; 2: 2–3; 3: 4–6; 4: > 6). Suatu daerah memiliki 6 bulan basah berurutan dan 3 bulan kering berurutan. Tipe agroklimatnya adalah …",
      ["C2", "C3", "B2", "D2", "C1"],
      "Zona utama ditentukan oleh bulan basah berurutan: 6 bulan berada pada rentang 5–6 → zona C. Subzona ditentukan oleh bulan kering berurutan: 3 bulan berada pada rentang 2–3 → subzona 2. Jadi tipe agroklimatnya C2.\nInterpretasi Oldeman untuk C2: padi dapat ditanam satu kali, sedangkan palawija dapat ditanam dua kali dalam setahun; satu kali palawija harus jatuh pada musim kering.\n\nPengecoh: C3 memerlukan 4–6 bulan kering berurutan. B2 memerlukan 7–9 bulan basah berurutan. D2 memerlukan 3–4 bulan basah. C1 memerlukan bulan kering kurang dari 2.",
      None),
    Q("Perhatikan peta pembagian pola curah hujan Indonesia berikut.\n\nWilayah yang grafik curah hujannya memiliki dua puncak, yaitu sekitar Maret dan Oktober–November, ditunjukkan oleh huruf …",
      ["A, karena dekat khatulistiwa sehingga dilintasi Matahari dua kali", "B, karena dipengaruhi angin monsun yang berganti arah dua kali",
       "C, karena dipengaruhi kondisi lokal Laut Banda dan pegunungan", "A, karena dipengaruhi angin monsun barat yang sangat kuat",
       "B dan C, karena keduanya berada di Belahan Bumi Selatan"],
      "Dua puncak hujan (bimodal) adalah ciri pola ekuatorial. Wilayah yang dekat khatulistiwa, seperti Sumatra bagian tengah dan Kalimantan bagian barat-tengah (A), dilintasi Matahari secara tegak lurus dua kali setahun, sekitar ekuinoks Maret dan September. Saat itu pemanasan dan konveksi maksimum sehingga muncul dua puncak hujan dengan sedikit keterlambatan (Maret–April dan Oktober–November).\n\nPengecoh: B (Jawa–Nusa Tenggara) berpola monsunal dengan satu puncak Desember–Februari; pergantian arah monsun tidak menghasilkan dua puncak. C (Maluku) berpola lokal dengan puncak Juni–Juli. Monsun barat tidak menjadi penyebab utama pola dua puncak di A.",
      f_pola_map),
    Q("Sebuah stasiun di dataran tinggi pada ketinggian ±2.000 m memiliki suhu bulan terdingin 13,5 °C dan suhu bulan terpanas 15,5 °C. Semua bulan menerima hujan lebih dari 60 mm. Menurut Köppen, tipe iklimnya adalah …",
      ["Cfb", "Af", "Cwb", "ET", "Am"],
      "Langkah:\n1) Suhu bulan terdingin 13,5 °C berada di antara −3 °C dan 18 °C → kelompok C (sedang/mesotermal), bukan A.\n2) Tidak ada bulan kering yang nyata (semua bulan > 60 mm) → huruf kedua f (lembap sepanjang tahun).\n3) Suhu bulan terpanas 15,5 °C < 22 °C, dan ada ≥ 4 bulan bersuhu ≥ 10 °C → huruf ketiga b.\nJadi tipe iklimnya Cfb. Inilah sebabnya dataran tinggi tropis seperti Dieng atau Pegunungan Tengah Papua dapat memiliki tipe iklim C walaupun berada dekat khatulistiwa.\n\nPengecoh: Af dan Am mensyaratkan suhu bulan terdingin ≥ 18 °C. Cwb memerlukan musim dingin yang kering. ET (tundra) mensyaratkan suhu bulan terpanas < 10 °C.",
      None),
    Q("Perhatikan grafik curah hujan dasarian ZOM X berikut. Kriteria awal musim hujan: curah hujan satu dasarian ≥ 50 mm dan diikuti oleh dua dasarian berikutnya yang juga ≥ 50 mm.\n\nAwal musim hujan ZOM X jatuh pada …",
      ["Desember dasarian I", "Oktober dasarian II", "November dasarian I", "November dasarian II", "Desember dasarian II"],
      "Periksa setiap dasarian yang ≥ 50 mm beserta dua dasarian berikutnya:\n• Okt II (58) → Okt III (41) gagal.\n• Nov I (52) → Nov II (67) lolos, tetapi Nov III (49) gagal.\n• Nov II (67) → Nov III (49) gagal.\n• Des I (80) → Des II (95) dan Des III (110) lolos.\nJadi awal musim hujan adalah Desember dasarian I.\n\nPengecoh: Oktober II adalah dasarian pertama yang ≥ 50 mm, tetapi tidak berlanjut. November I dan II gagal karena November III hanya 49 mm (di bawah ambang, walau tipis). Desember II tidak tepat karena syarat sudah terpenuhi sejak Desember I. Informasi awal musim seperti ini penting bagi petani untuk menentukan waktu tanam.",
      f_dasarian),
    Q("Normal curah hujan bulan Februari di sebuah stasiun adalah 250 mm. Pada Februari tahun ini tercatat 205 mm. Jika sifat hujan Atas Normal > 115%, Normal 85–115%, dan Bawah Normal < 85%, sifat hujan bulan tersebut adalah …",
      ["Bawah Normal, sekitar 82% dari normal", "Normal, sekitar 82% dari normal", "Bawah Normal, sekitar 18% dari normal",
       "Normal, sekitar 122% dari normal", "Atas Normal, sekitar 122% dari normal"],
      "Sifat hujan = (curah hujan aktual ÷ normalnya) × 100%.\n205 ÷ 250 × 100% = 82%. Nilai 82% < 85% → Bawah Normal.\n\nPengecoh: 18% adalah besar kekurangannya (100% − 82%), bukan persentase terhadap normal. 122% muncul bila pembagian dibalik (250 ÷ 205). \"Normal 82%\" salah menempatkan nilai pada kategori. Sifat hujan dinilai relatif terhadap normal setempat; 205 mm bisa Bawah Normal di satu stasiun tetapi Atas Normal di stasiun lain yang lebih kering.",
      None),
    Q("Perhatikan penampang zona suhu Junghuhn berikut.\n\nKomoditas kelapa, tebu, dan padi sawah paling sesuai dikembangkan pada zona …",
      ["K, zona panas", "L, zona sedang", "M, zona sejuk", "N, zona dingin", "L dan M, zona peralihan"],
      "Pada penampang, K berada di bawah 700 m (zona panas, suhu rata-rata ±22–26,3 °C), L pada 700–1.500 m (zona sedang), M pada 1.500–2.500 m (zona sejuk), dan N di atas 2.500 m (zona dingin).\nKelapa, tebu, dan padi sawah memerlukan suhu tinggi dan umumnya dikembangkan di dataran rendah, sehingga zona K adalah jawaban yang tepat.\n\nPengecoh: zona L cocok untuk kopi, tembakau, dan sayuran; zona M untuk teh, kina, dan sayuran dataran tinggi; zona N hampir tanpa budidaya karena terlalu dingin. Tidak ada zona peralihan L–M dalam pembagian Junghuhn.",
      f_junghuhn),
    Q("Perhatikan grafik rata-rata curah hujan bulanan Stasiun O berikut. Kriteria Oldeman: bulan basah > 200 mm, bulan kering < 100 mm; zona C = 5–6 bulan basah berurutan, D = 3–4; subzona 3 = 4–6 bulan kering berurutan.\n\nTipe agroklimat Oldeman Stasiun O adalah …",
      ["C3", "D3", "C2", "B3", "D2"],
      "Bulan basah (> 200 mm): Nov (230), Des (300), Jan (320), Feb (290), Mar (260), Apr (210). Karena tahun bersifat siklis, rangkaian Nov–Apr berurutan → 6 bulan basah → zona C.\nBulan kering (< 100 mm): Jun (90), Jul (60), Agu (40), Sep (70) → 4 bulan kering berurutan → subzona 3.\nTipe agroklimatnya C3.\n\nPengecoh: D3 muncul jika bulan basah hanya dihitung dari Januari (Jan–Apr = 4 bulan), sehingga November dan Desember tidak disambung. Mei (150 mm) bukan bulan basah maupun kering. C2 muncul bila bulan kering hanya dihitung 3. B3 memerlukan 7–9 bulan basah.",
      f_oldeman),
    Q("Pernyataan yang paling tepat mengenai faktor pengendali iklim Indonesia adalah …",
      ["Letak di antara dua benua dan dua samudra membuat Indonesia dipengaruhi monsun Asia–Australia",
       "Letak di khatulistiwa membuat seluruh wilayah Indonesia memiliki pola hujan dua puncak yang sama",
       "Bentuk kepulauan membuat suhu Indonesia sangat bervariasi antara musim panas dan musim dingin",
       "Ketinggian tempat hanya memengaruhi curah hujan, tetapi tidak memengaruhi suhu rata-rata udara",
       "Arus laut di sekitar Indonesia tidak berpengaruh karena perairan Indonesia adalah laut dangkal"],
      "Letak Indonesia di antara Benua Asia dan Australia serta Samudra Pasifik dan Hindia membuat wilayah ini dilewati angin monsun yang berganti arah setiap setengah tahun. Monsun inilah yang menghasilkan musim hujan dan kemarau di sebagian besar Indonesia.\n\nPengecoh: tidak semua wilayah berpola ekuatorial; ada pola monsunal dan lokal. Indonesia beriklim maritim tropis dengan amplitudo suhu tahunan kecil, tanpa musim panas–dingin. Ketinggian justru sangat memengaruhi suhu (rumus Braak). Arus laut, termasuk ARLINDO dan upwelling Laut Banda, berpengaruh terhadap suhu muka laut dan curah hujan; banyak perairan Indonesia pun sangat dalam (misalnya Laut Banda > 7.000 m).",
      None),
]

P4 = [
    Q("Perhatikan grafik Oceanic Niño Index (ONI) berikut. Kejadian El Niño ditandai ONI ≥ +0,5 °C dan La Niña ditandai ONI ≤ −0,5 °C.\n\nPeriode yang menunjukkan La Niña berulang hingga tiga musim berturut-turut (triple-dip) adalah …",
      ["2020–2022", "2015–2016", "2017–2018", "2018–2019", "2023–2024"],
      "Pada grafik, ONI berada di bawah −0,5 °C pada akhir 2020, kembali melemah pada pertengahan 2021, turun lagi pada akhir 2021, dan tetap di bawah −0,5 °C hingga akhir 2022. Tiga musim La Niña berturut-turut ini dikenal sebagai triple-dip La Niña 2020–2022, yang membuat banyak wilayah Indonesia mengalami \"kemarau basah\".\n\nPengecoh: 2015–2016 dan 2023–2024 adalah El Niño kuat (ONI mencapai +2,6 dan +2,0). 2017–2018 hanya La Niña lemah satu musim. 2018–2019 adalah El Niño lemah (ONI ±0,8).",
      f_oni),
    Q("Perhatikan peta anomali suhu muka laut Samudra Hindia pada bulan September berikut.\n\nFenomena yang terjadi beserta dampaknya bagi Indonesia adalah …",
      ["IOD positif; hujan di Sumatra dan Jawa cenderung berkurang", "IOD negatif; hujan di Sumatra dan Jawa cenderung meningkat",
       "La Niña; hujan di Indonesia bagian timur cenderung meningkat", "IOD positif; hujan di Afrika Timur cenderung berkurang",
       "El Niño; suhu muka laut di barat Sumatra menjadi lebih hangat"],
      "Peta menunjukkan Samudra Hindia bagian barat (dekat Afrika) lebih hangat (+1,0 °C), sedangkan bagian timur di barat Sumatra lebih dingin (−0,8 °C). Pola dipol ini disebut Indian Ocean Dipole (IOD) positif. Air laut yang dingin di barat Sumatra mengurangi penguapan dan konveksi, sehingga pembentukan awan dan hujan di Sumatra dan Jawa berkurang. IOD positif yang terjadi bersama El Niño (misalnya 2015, 2019, 2023) memperparah kekeringan dan kebakaran hutan.\n\nPengecoh: IOD negatif memiliki pola sebaliknya. La Niña dan El Niño adalah fenomena Pasifik, bukan Samudra Hindia. Pada IOD positif, Afrika Timur justru cenderung lebih basah.",
      f_iod),
    Q("Pada Agustus–Oktober suatu tahun, BMKG melaporkan ONI −1,1 °C dan Dipole Mode Index (DMI) −0,7 °C. Dampak yang paling mungkin terjadi di Indonesia adalah …",
      ["Kemarau basah; hujan di atas normal pada musim yang biasanya kering",
       "Kemarau panjang; hujan jauh di bawah normal di sebagian besar wilayah",
       "Kemarau basah hanya di Papua, sedangkan Sumatra dan Jawa justru kering",
       "Cuaca normal karena pengaruh La Niña dan IOD negatif saling meniadakan",
       "Kekeringan di Sumatra karena IOD negatif mendinginkan laut barat Sumatra"],
      "ONI −1,1 °C berarti La Niña (sedang), sedangkan DMI −0,7 °C berarti IOD negatif. Keduanya sama-sama menambah hujan: La Niña memperkuat konveksi di atas Indonesia, terutama bagian tengah dan timur, sedangkan IOD negatif menghangatkan perairan barat Sumatra sehingga menambah hujan di Indonesia bagian barat. Karena terjadi pada Agustus–Oktober (biasanya kemarau), dampaknya adalah kemarau basah, misalnya seperti tahun 2010, 2016, dan 2022. Dampak lanjutannya antara lain gagal panen tembakau dan garam serta risiko banjir.\n\nPengecoh: kemarau panjang adalah dampak El Niño dan IOD positif. Kedua fenomena tidak saling meniadakan karena arah dampaknya sama. IOD negatif justru menghangatkan laut di barat Sumatra.",
      None),
    Q("Perhatikan grafik curah hujan September–November pada tahun El Niño dibandingkan normalnya di empat stasiun berikut. Sifat hujan dinilai dari persentase terhadap normal.\n\nStasiun yang mengalami sifat hujan bawah normal paling parah adalah …",
      ["Stasiun P", "Stasiun R", "Stasiun Q", "Stasiun S", "Stasiun P dan R sama parahnya"],
      "Hitung persentase terhadap normal:\n• P: 180 ÷ 300 = 60%.\n• Q: 200 ÷ 250 = 80%.\n• R: 270 ÷ 400 = 67,5%.\n• S: 160 ÷ 150 ≈ 107% (normal, bahkan sedikit di atas).\nPersentase terkecil ada di P (60%), sehingga P paling parah.\n\nPengecoh: R memiliki kekurangan absolut terbesar (130 mm, dibandingkan P yang 120 mm), tetapi sifat hujan dinilai secara relatif terhadap normal setempat. S justru di atas normal, menunjukkan bahwa respons ENSO berbeda antarlokasi karena pengaruh topografi dan sirkulasi lokal.",
      f_anom),
    Q("Madden–Julian Oscillation (MJO) berbeda dari ENSO terutama karena …",
      ["MJO adalah gangguan konveksi yang merambat ke timur dengan siklus sekitar 30–60 hari",
       "MJO adalah perubahan suhu muka laut Pasifik dengan siklus sekitar 2–7 tahun",
       "MJO adalah pergeseran ITCZ ke utara dan selatan dengan siklus sekitar satu tahun",
       "MJO adalah anomali dipol suhu muka laut Samudra Hindia yang memuncak pada September",
       "MJO adalah pemanasan global yang berlangsung secara bertahap selama ratusan tahun"],
      "MJO adalah gugusan awan konvektif dan anomali angin yang terbentuk di Samudra Hindia lalu merambat ke timur melewati Benua Maritim Indonesia hingga Pasifik, dengan periode sekitar 30–60 hari (intramusiman). Saat fase aktif MJO berada di atas Indonesia (fase 4–5), peluang hujan lebat meningkat selama 1–2 minggu; saat fase tidak aktif, cuaca cenderung lebih kering.\n\nPengecoh: siklus 2–7 tahun di Pasifik adalah ENSO. Pergeseran ITCZ tahunan adalah siklus musiman. Dipol Samudra Hindia adalah IOD. Pemanasan global adalah tren jangka panjang, bukan osilasi.",
      None),
    Q("Perhatikan peta lintasan arus laut di perairan Indonesia berikut.\n\nArus yang digambarkan dan penyebab utama alirannya adalah …",
      ["ARLINDO; muka laut Pasifik barat lebih tinggi daripada Samudra Hindia timur",
       "ARLINDO; muka laut Samudra Hindia lebih tinggi daripada Pasifik barat",
       "Arus Khatulistiwa Selatan; didorong angin baratan dari Samudra Hindia",
       "Arus monsun; selalu berbalik arah setiap kali monsun barat berganti timur",
       "Arus Kuroshio; membawa air hangat dari Laut Filipina menuju Australia"],
      "Peta memperlihatkan aliran dari Samudra Pasifik melalui Selat Makassar dan Laut Maluku–Banda, lalu keluar ke Samudra Hindia melalui Selat Lombok, Selat Ombai, dan Laut Timor. Inilah Arus Lintas Indonesia (ARLINDO / Indonesian Throughflow). Penggerak utamanya adalah perbedaan tinggi muka laut: pasat timur menumpuk air di Pasifik barat sehingga muka lautnya lebih tinggi (±15–20 cm) daripada Samudra Hindia timur.\n\nPengecoh: arah tekanan muka laut yang dibalik tidak sesuai dengan arah aliran. ARLINDO tetap mengalir ke Samudra Hindia sepanjang tahun walaupun kekuatannya berfluktuasi dengan monsun dan ENSO. Kuroshio mengalir ke utara menuju Jepang, bukan ke Australia.",
      f_arlindo),
    Q("Pada Juni–September, perairan selatan Jawa hingga Nusa Tenggara serta Laut Banda menjadi daerah penangkapan ikan yang sangat produktif. Penyebab utamanya adalah …",
      ["Upwelling akibat monsun timur yang mengangkat air dingin kaya nutrien", "Downwelling akibat monsun barat yang menumpuk air hangat di pesisir",
       "Pemanasan permukaan laut yang mempercepat pertumbuhan terumbu karang", "Masuknya air tawar dari sungai besar yang membawa sedimen pada kemarau",
       "Arus ARLINDO yang membawa ikan dari Samudra Hindia menuju Pasifik"],
      "Pada Juni–September, monsun timur bertiup dari tenggara. Angin yang sejajar pantai selatan Jawa–Nusa Tenggara, bersama transport Ekman yang dibelokkan menjauhi pantai, menyingkirkan air permukaan sehingga air dalam yang dingin dan kaya nutrien naik ke permukaan (upwelling). Nutrien memicu ledakan fitoplankton yang menjadi dasar rantai makanan, sehingga ikan pelagis seperti tuna, cakalang, dan lemuru berlimpah.\n\nPengecoh: downwelling justru menenggelamkan air permukaan dan miskin nutrien. Debit sungai kecil pada kemarau. ARLINDO mengalir dari Pasifik ke Samudra Hindia, bukan sebaliknya, dan tidak \"membawa ikan\". Terumbu karang tidak menjadi penyebab produktivitas perikanan pelagis di sini.",
      None),
    Q("Perhatikan peta lintasan siklon tropis di sekitar Indonesia berikut.\n\nAlasan utama hampir tidak ada siklon tropis yang terbentuk pada pita 5° LU–5° LS adalah …",
      ["Gaya Coriolis di sekitar khatulistiwa terlalu lemah untuk memutar pusaran", "Suhu muka laut di sekitar khatulistiwa terlalu dingin untuk penguapan",
       "Kelembapan udara di sekitar khatulistiwa terlalu rendah untuk membentuk awan", "Wilayah khatulistiwa didominasi tekanan tinggi yang menekan udara naik",
       "Angin di sekitar khatulistiwa selalu kencang sehingga awan cepat tercerai-berai"],
      "Siklon tropis memerlukan putaran (vortisitas) agar udara yang mengalir ke pusat tekanan rendah berpilin, tidak langsung mengisi pusat tersebut. Putaran ini berasal dari gaya Coriolis, yang besarnya sebanding dengan sinus lintang dan bernilai nol di khatulistiwa. Karena itu siklon umumnya terbentuk di atas lintang ±5°–20°, lalu bergerak menjauhi khatulistiwa. Sebagian besar wilayah Indonesia relatif aman dari terjangan langsung, tetapi bisa terkena dampak tidak langsung (\"ekor siklon\"), misalnya Siklon Seroja 2021 di NTT yang terbentuk di Laut Sawu (±9° LS).\n\nPengecoh: suhu muka laut di khatulistiwa justru tinggi (> 26,5 °C) dan kelembapannya tinggi. Khatulistiwa adalah zona tekanan rendah (ITCZ), bukan tekanan tinggi. Angin di sekitar ekuator cenderung lemah (doldrum).",
      f_tracks),
    Q("Berikut ini merupakan syarat pembentukan siklon tropis, KECUALI …",
      ["Berada tepat di garis khatulistiwa agar penguapan paling besar", "Suhu muka laut minimal sekitar 26,5 °C hingga kedalaman ±50 m",
       "Geseran angin vertikal (wind shear) antara lapisan bawah dan atas kecil", "Kelembapan udara tinggi di lapisan troposfer tengah",
       "Ada gangguan awal berupa daerah tekanan rendah di permukaan"],
      "Syarat utama pembentukan siklon tropis adalah: (1) lautan hangat, suhu muka laut ≥ 26,5 °C dengan lapisan hangat yang cukup dalam; (2) atmosfer lembap hingga troposfer tengah; (3) geseran angin vertikal kecil agar menara awan tidak terpotong; (4) ada gangguan awal tekanan rendah; dan (5) gaya Coriolis yang cukup, sehingga lokasinya minimal ±5° dari khatulistiwa.\nOpsi \"berada tepat di garis khatulistiwa\" bertentangan dengan syarat kelima. Di khatulistiwa gaya Coriolis nol sehingga pusaran tidak dapat terbentuk.\n\nOpsi lain adalah syarat yang benar. Kata kunci KECUALI harus dilingkari agar tidak terkecoh memilih syarat yang benar.",
      None),
    Q("Siklon tropis Seroja (April 2021) terbentuk di Laut Sawu dan menimbulkan banjir bandang serta longsor di NTT. Dari sudut pandang manajemen risiko, pelajaran yang paling tepat dari kejadian itu adalah …",
      ["Wilayah selatan Indonesia perlu memperhitungkan siklon dalam rencana kontinjensi walau jarang terjadi",
       "Siklon tropis tidak mungkin terbentuk di perairan Indonesia sehingga cukup mewaspadai siklon dari Australia",
       "Kerusakan terutama disebabkan angin kencang sehingga mitigasi cukup berupa penguatan atap rumah",
       "Pemanasan muka laut tidak berkaitan dengan siklon sehingga tren kejadiannya tidak perlu dipantau",
       "Siklon hanya berdampak di laut sehingga peringatan dini cukup ditujukan kepada para nelayan"],
      "Seroja tergolong langka karena terbentuk sangat dekat dengan daratan Indonesia (±9° LS) dan menimbulkan dampak langsung di NTT: hujan ekstrem memicu banjir bandang dan longsor, korban jiwa ratusan orang, dan kerusakan luas. Pelajarannya, wilayah di selatan Indonesia (NTT, NTB, selatan Jawa) yang berada pada lintang cukup jauh dari ekuator tetap berisiko dan perlu memasukkan skenario siklon ke dalam rencana kontinjensi, peringatan dini, dan tata ruang (misalnya larangan bermukim di bantaran sungai).\n\nPengecoh: siklon memang bisa terbentuk di perairan Indonesia bagian selatan. Kerusakan Seroja terutama berasal dari hujan ekstrem, bukan hanya angin. Laut yang lebih hangat meningkatkan energi siklon. Dampak siklon jelas mencapai daratan.",
      None),
]

P5 = [
    Q("Perhatikan grafik konsentrasi CO₂ bulanan berikut.\n\nPola naik-turun setiap tahun yang terlihat pada kurva paling tepat dijelaskan oleh …",
      ["Fotosintesis vegetasi Belahan Bumi Utara yang menyerap CO₂ pada musim panasnya",
       "Pembakaran bahan bakar fosil yang berhenti setiap akhir tahun karena hari libur",
       "Letusan gunung api yang terjadi secara teratur setiap tahun di Pasifik",
       "Fotosintesis vegetasi Belahan Bumi Selatan yang luas daratannya lebih besar",
       "Penyerapan CO₂ oleh laut yang hanya terjadi pada musim dingin Belahan Utara"],
      "Kurva menunjukkan tren naik jangka panjang (akibat emisi bahan bakar fosil dan alih fungsi lahan) dengan gerigi musiman. Daratan dan vegetasi sebagian besar berada di Belahan Bumi Utara. Saat musim semi–panas di BBU (Mei–September), tumbuhan berfotosintesis aktif sehingga CO₂ atmosfer turun. Saat musim gugur–dingin, fotosintesis berkurang dan dekomposisi melepaskan CO₂ sehingga konsentrasinya naik lagi.\n\nPengecoh: emisi fosil tidak berhenti setiap tahun. Letusan gunung api tidak teratur dan sumbangannya kecil dibanding emisi manusia. Daratan Belahan Bumi Selatan lebih sempit. Pertukaran CO₂ laut tidak menghasilkan pola musiman sekuat vegetasi daratan.",
      f_keeling),
    Q("Mencairnya es laut Arktik membuat permukaan laut gelap lebih banyak terbuka, sehingga penyerapan radiasi meningkat dan pemanasan semakin cepat. Mekanisme ini merupakan contoh …",
      ["Umpan balik positif es–albedo", "Umpan balik negatif es–albedo", "Umpan balik negatif awan rendah",
       "Efek pendinginan aerosol vulkanik", "Umpan balik positif uap air stratosfer"],
      "Es dan salju memiliki albedo tinggi (±0,6–0,9), sedangkan laut terbuka memiliki albedo rendah (±0,06). Ketika suhu naik, es mencair → albedo turun → radiasi yang diserap bertambah → suhu makin naik → es makin banyak mencair. Karena respons ini memperkuat perubahan awal, mekanisme ini disebut umpan balik positif es–albedo. Inilah salah satu alasan Arktik memanas sekitar 3–4 kali lebih cepat daripada rata-rata global (Arctic amplification).\n\nPengecoh: umpan balik negatif justru meredam perubahan awal. Awan rendah dan aerosol vulkanik memang dapat mendinginkan, tetapi tidak sesuai dengan mekanisme pada soal. Uap air adalah umpan balik positif penting, tetapi terjadi terutama di troposfer dan bukan mekanisme yang digambarkan.",
      None),
    Q("Perhatikan grafik anomali suhu permukaan global per dekade berikut.\n\nLaju pemanasan rata-rata dari dekade 1960-an hingga dekade 2020-an adalah sekitar …",
      ["0,20 °C per dekade", "0,12 °C per dekade", "1,20 °C per dekade", "0,17 °C per dekade", "0,02 °C per dekade"],
      "Dari grafik: anomali dekade 1960 = −0,2 °C dan dekade 2020 = +1,0 °C. Kenaikan = 1,0 − (−0,2) = 1,2 °C.\nSelang waktunya 2020 − 1960 = 60 tahun = 6 dekade. Laju = 1,2 ÷ 6 = 0,20 °C per dekade.\n\nPengecoh: 1,20 adalah total kenaikan, bukan laju per dekade. 0,12 °C per dekade muncul bila dibagi 10 dekade. 0,17 muncul bila anomali awal dianggap nol (1,0 ÷ 6), yaitu mengabaikan tanda negatif pada dekade 1960. 0,02 adalah laju per tahun, bukan per dekade. Perhatikan selalu tanda negatif dan satuan waktu yang ditanyakan.",
      f_temp),
    Q("Suatu kabupaten memiliki suhu rata-rata 27 °C dan p = 0,27. Dengan rumus Blaney–Criddle ET₀ = p(0,46T + 8,13) dan koefisien tanaman padi Kc = 1,05, kebutuhan air (ETc) untuk 200 ha sawah selama 10 hari adalah sekitar …",
      ["116.500 m³", "111.000 m³", "11.650 m³", "1.165.000 m³", "58.300 m³"],
      "1) ET₀ = 0,27 × (0,46 × 27 + 8,13) = 0,27 × (12,42 + 8,13) = 0,27 × 20,55 ≈ 5,55 mm/hari.\n2) ETc = Kc × ET₀ = 1,05 × 5,55 ≈ 5,83 mm/hari = 0,00583 m/hari.\n3) Luas 200 ha = 2.000.000 m².\n4) Volume = 0,00583 × 2.000.000 × 10 ≈ 116.500 m³.\n\nPengecoh: 111.000 m³ muncul bila lupa mengalikan Kc (hanya ET₀). 11.650 dan 1.165.000 adalah kesalahan konversi satuan (mm ke m atau ha ke m²). 58.300 m³ hanya menghitung 5 hari. Ingat: 1 mm air pada lahan 1 ha setara 10 m³.",
      None),
    Q("Perhatikan grafik neraca air klimatologis sebuah kabupaten berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Defisit terjadi enam bulan (Mei–Oktober) sehingga tanaman musim kemarau perlu irigasi",
       "Defisit terjadi empat bulan (Juni–September) sehingga cukup mengandalkan hujan",
       "Surplus terjadi sepanjang tahun karena total hujan tahunan lebih besar dari ET₀",
       "Defisit terjadi enam bulan (April–September) karena hujan April di bawah 200 mm",
       "Defisit terjadi tiga bulan (Juli–September) yang hujannya di bawah 60 mm"],
      "Defisit terjadi bila curah hujan (P) lebih kecil daripada evapotranspirasi acuan (ET₀). Bandingkan per bulan:\nMei 110 < 130, Jun 70 < 125, Jul 40 < 135, Agu 30 < 145, Sep 50 < 150, Okt 120 < 145 → enam bulan defisit (Mei–Oktober). April (180 > 125) dan November (220 > 130) surplus.\nArtinya selama separuh tahun kebutuhan air tanaman tidak terpenuhi oleh hujan, sehingga pertanaman kedua dan ketiga membutuhkan irigasi atau pemanfaatan cadangan lengas tanah dan embung.\n\nPengecoh: menghitung hanya bulan yang hujannya < 100 mm atau < 60 mm bukan cara menghitung defisit. Total tahunan yang surplus tidak berarti setiap bulan surplus. April justru surplus.",
      f_neraca_air),
    Q("Pemerintah daerah pesisir merencanakan beberapa program: (1) membangun tanggul laut dan rumah panggung; (2) mengganti PLTU batu bara dengan PLTS; (3) mengembangkan varietas padi toleran salinitas; (4) merestorasi mangrove; (5) memasang biodigester di peternakan. Program yang tergolong adaptasi adalah …",
      ["(1) dan (3)", "(2) dan (5)", "(1) dan (2)", "(3) dan (5)", "(2) dan (4)"],
      "Mitigasi bertujuan mengurangi emisi atau meningkatkan serapan gas rumah kaca, sedangkan adaptasi bertujuan menyesuaikan diri agar dampak perubahan iklim berkurang.\n• (1) Tanggul laut dan rumah panggung → adaptasi terhadap kenaikan muka laut dan rob.\n• (2) PLTS menggantikan PLTU → mitigasi (mengurangi emisi).\n• (3) Padi toleran salinitas → adaptasi terhadap intrusi air laut.\n• (4) Restorasi mangrove → keduanya (menyerap karbon biru dan melindungi pantai), tetapi pasangan opsi yang hanya berisi adaptasi murni adalah (1) dan (3).\n• (5) Biodigester → mitigasi (menangkap metana).\nOpsi lain mencampur program mitigasi ke dalam kelompok adaptasi.",
      None),
    Q("Perhatikan gambar tiga parameter orbit Bumi dalam teori Milankovitch berikut.\n\nParameter yang memiliki siklus sekitar 41.000 tahun dan mengatur kontras musim antara musim panas dan musim dingin adalah …",
      ["Q, kemiringan sumbu (obliquity)", "P, eksentrisitas (kelonjongan) orbit", "R, presesi (goyangan) sumbu",
       "P dan R yang bekerja bersamaan", "Q, eksentrisitas orbit Bumi"],
      "Tiga siklus Milankovitch:\n• P – eksentrisitas (kelonjongan orbit), siklus ±100.000 dan ±400.000 tahun; mengubah jarak Bumi–Matahari.\n• Q – obliquity (kemiringan sumbu), berubah antara ±22,1° dan 24,5° dengan siklus ±41.000 tahun. Kemiringan yang lebih besar membuat musim panas lebih panas dan musim dingin lebih dingin, sehingga kontras musim meningkat.\n• R – presesi (goyangan arah sumbu), siklus ±19.000–26.000 tahun; mengubah waktu terjadinya perihelion relatif terhadap musim.\nPengecoh: opsi \"Q, eksentrisitas\" salah menamai parameter Q. Kombinasi P dan R tidak memiliki siklus 41.000 tahun.",
      f_milank),
    Q("Sekitar 20.000 tahun lalu (Last Glacial Maximum), muka laut global ±120 m lebih rendah daripada sekarang. Akibat yang paling tepat bagi geografi Indonesia saat itu adalah …",
      ["Paparan Sunda tersingkap sehingga Sumatra, Jawa, dan Kalimantan menyatu dengan Asia",
       "Paparan Sahul tenggelam sehingga Papua terpisah jauh dari daratan Australia",
       "Laut Banda mengering sehingga Sulawesi dan Maluku menyatu dengan Papua",
       "Selat Lombok tertutup sehingga fauna Asia dan Australia bercampur bebas",
       "Seluruh kepulauan Indonesia menyatu menjadi satu daratan dengan Australia"],
      "Paparan Sunda (Laut Jawa, Selat Karimata, sebagian Laut Cina Selatan) relatif dangkal, umumnya < 100 m. Ketika muka laut turun ±120 m, paparan ini tersingkap menjadi daratan luas (Sundaland) yang menghubungkan Sumatra, Jawa, Kalimantan, dan Semenanjung Malaya dengan Asia daratan. Hal yang sama terjadi pada Paparan Sahul, sehingga Papua menyatu dengan Australia.\n\nPengecoh: Paparan Sahul justru tersingkap, bukan tenggelam. Laut Banda dan Selat Lombok sangat dalam sehingga tetap menjadi laut; inilah yang membuat zona Wallacea (Sulawesi, Nusa Tenggara, Maluku) tetap terpisah dan menjadi batas sebaran fauna (Garis Wallace). Karena itu tidak pernah seluruh Indonesia menyatu dengan Australia.",
      None),
    Q("Perhatikan grafik tinggi muka air waduk PLTA pada tahun normal dan tahun El Niño berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Pada tahun El Niño, turbin tidak dapat beroperasi normal sekitar Agustus–November",
       "Pada tahun El Niño, turbin tidak dapat beroperasi normal sekitar Juni–Desember",
       "Pada tahun normal, turbin berhenti beroperasi sekitar September karena di bawah batas",
       "Pada kedua tahun, tinggi muka air sama sehingga produksi listrik tidak terpengaruh",
       "Pada tahun El Niño, muka air terendah terjadi pada bulan Agustus, yaitu 74 m"],
      "Batas minimum operasi turbin adalah 75 m. Pada tahun El Niño, muka air turun dari 91 m (Januari) menjadi 79 m (Juli), lalu berada di bawah batas pada Agustus (74 m), September (72 m), Oktober (71 m), dan November (74 m), kemudian pulih pada Desember (79 m). Jadi turbin tidak dapat beroperasi normal selama Agustus–November.\nPada tahun normal, muka air terendah 83 m, selalu di atas batas.\n\nPengecoh: Juni–Desember terlalu panjang karena Juni–Juli dan Desember masih di atas 75 m. Muka air terendah tahun El Niño ada pada Oktober (71 m), bukan Agustus. Ini contoh nexus air–energi: kekeringan iklim menurunkan pasokan listrik dan sering harus diganti pembangkit fosil yang menambah emisi.",
      f_waduk),
    Q("Pernyataan yang tepat mengenai Persetujuan Paris (2015) dibandingkan Protokol Kyoto (1997) adalah …",
      ["Semua negara menetapkan target melalui NDC, sedangkan Kyoto hanya mengikat negara maju",
       "Persetujuan Paris hanya mewajibkan negara maju, sedangkan Kyoto mengikat semua negara",
       "Persetujuan Paris menargetkan pemanasan di bawah 4 °C, lebih longgar daripada Kyoto",
       "Protokol Kyoto memakai NDC, sedangkan Paris memakai target yang ditetapkan PBB",
       "Persetujuan Paris tidak mengatur pendanaan maupun adaptasi bagi negara berkembang"],
      "Protokol Kyoto (1997) menetapkan target pengurangan emisi yang mengikat hanya untuk negara maju (Annex I), berdasarkan prinsip tanggung jawab bersama tetapi berbeda. Persetujuan Paris (2015) melibatkan semua negara: masing-masing menetapkan kontribusinya sendiri melalui Nationally Determined Contribution (NDC), dengan tujuan menahan kenaikan suhu jauh di bawah 2 °C dan berupaya mencapai 1,5 °C. Indonesia, misalnya, menaikkan target pengurangan emisinya dalam Enhanced NDC 2022 (31,89% tanpa syarat, 43,20% dengan dukungan internasional).\n\nPengecoh: opsi lain membalik ciri kedua perjanjian, menyebut target 4 °C yang keliru, atau menafikan pengaturan pendanaan dan adaptasi yang justru menjadi bagian penting Persetujuan Paris.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
