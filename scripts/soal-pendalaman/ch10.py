from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_burgess(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    cols = ["#E2E8F0", "#C6F6D5", "#FEFCBF", "#FBD38D", "#FC8181"]
    for i, r in enumerate([46, 37, 28, 19, 9]):
        ax.add_patch(Circle((0, 0), r, fc=cols[i], ec="#555"))
    for i, r in enumerate([4.5, 14, 23.5, 32.5, 41.5]):
        ax.text(0, r, str(i + 1), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.set_title("Model zona konsentris")
    save(fig, path)


def f_bidrent(path):
    d = np.linspace(0, 25, 200)
    fig, ax = new(8.5, 4.4)
    for lab, a, b, c in [("Perdagangan: R = 1.000 − 100d", 1000, 100, C["red"]), ("Permukiman: R = 600 − 30d", 600, 30, C["orange"]),
                         ("Pertanian: R = 200 − 8d", 200, 8, C["green"])]:
        ax.plot(d, np.clip(a - b * d, 0, None), lw=2.4, color=c, label=lab)
    ax.set_xlabel("Jarak dari pusat kota, d (km)"); ax.set_ylabel("Sewa lahan (ribu Rp/m²/tahun)"); ax.legend(frameon=False)
    ax.grid(color="#EDF2F7"); ax.set_ylim(0, 1050); ax.set_title("Kurva sewa lahan tiga penggunaan lahan kota")
    save(fig, path)


def f_hoyt(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    secs = [(0, 40, "#FEFCBF", "Q"), (40, 100, "#C6F6D5", "R"), (100, 150, "#FBD38D", "S"), (150, 200, "#FEFCBF", "Q"), (200, 250, "#C6F6D5", "R"),
            (250, 300, "#FC8181", "T"), (300, 360, "#C6F6D5", "R")]
    from matplotlib.patches import Wedge
    for a0, a1, c, l in secs:
        ax.add_patch(Wedge((0, 0), 45, a0, a1, fc=c, ec="#555"))
        am = np.radians((a0 + a1) / 2); ax.text(30 * np.cos(am), 30 * np.sin(am), l, ha="center", va="center", fontsize=14, fontweight="bold")
    ax.add_patch(Circle((0, 0), 9, fc="#E53E3E", ec="#555")); ax.text(0, 0, "P", ha="center", va="center", fontsize=14, fontweight="bold", color="white")
    ax.plot([0, 45 * np.cos(np.radians(20))], [0, 45 * np.sin(np.radians(20))], color="black", lw=3)
    ax.text(30, 20, "jalan raya\nutama", fontsize=9)
    ax.set_title("Model sektor kota")
    save(fig, path)


def f_inti(path):
    fig, ax = blank(7, 6, (0, 100), (0, 86))
    ax.add_patch(Rectangle((0, 0), 100, 86, fc="#FEFCBF", ec="#555"))
    for (x, y, w, h, c, t) in [(40, 38, 16, 12, "#E53E3E", "1"), (10, 60, 18, 14, "#C6F6D5", "2"), (70, 8, 22, 16, "#A0AEC0", "3"), (72, 60, 14, 12, "#F6AD55", "4"),
                                (8, 10, 18, 14, "#90CDF4", "5"), (44, 6, 14, 10, "#F6AD55", "4")]:
        ax.add_patch(Rectangle((x, y), w, h, fc=c, ec="#555")); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=13, fontweight="bold")
    ax.text(50, 80, "1 = pusat bisnis · 2 = permukiman atas · 3 = industri berat", ha="center", fontsize=8.5)
    ax.text(50, 76, "4 = pusat bisnis sekunder · 5 = kawasan bandara/kampus", ha="center", fontsize=8.5)
    ax.set_title("Model struktur ruang sebuah kota")
    save(fig, path)


def f_densgrad(path):
    d = np.linspace(0, 30, 100)
    lines(d, {"1980": 25000 * np.exp(-d / 5), "2000": 18000 * np.exp(-d / 8) + 1500 * (1 - np.exp(-d / 2)), "2020": 12000 * np.exp(-d / 12) + 2500 * (1 - np.exp(-d / 2))}, path,
          title="Gradien kepadatan penduduk sebuah kota metropolitan (ilustrasi)", xlabel="Jarak dari pusat kota (km)", ylabel="jiwa per km²", markers=False, w=8.5)


def f_segre(path):
    table([["Kelurahan 1", "50", "10"], ["Kelurahan 2", "30", "30"], ["Kelurahan 3", "20", "60"], ["Total", "100", "100"]],
          ["Wilayah", "Kelompok A (ribu jiwa)", "Kelompok B (ribu jiwa)"], path, title="Sebaran dua kelompok penduduk di Kota S", col_w=[0.3, 0.35, 0.35])


# ---- paket 1
def f_lajukota(path):
    table([["Penduduk total", "200 juta", "1,2%"], ["Penduduk perkotaan", "110 juta", "2,8%"]], ["Kelompok", "Jumlah (2020)", "Laju per tahun"], path,
          title="Penduduk Negara U", col_w=[0.34, 0.3, 0.36])


def f_bentuk(path):
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.2))
    for a in axs:
        a.set_xlim(-5, 5); a.set_ylim(-5, 5); a.set_aspect("equal"); a.axis("off")
    axs[0].add_patch(Circle((0, 0), 3.2, fc="#FBD38D", ec="#555"))
    axs[1].add_patch(Rectangle((-4.8, -0.9), 9.6, 1.8, fc="#FBD38D", ec="#555")); axs[1].plot([-5, 5], [0, 0], color="black", lw=1.5)
    axs[2].add_patch(Circle((0, 0), 1.4, fc="#FBD38D", ec="#555"))
    for t in range(6):
        a = np.radians(60 * t + 15); axs[2].add_patch(Polygon([(1.2 * np.cos(a - 0.3), 1.2 * np.sin(a - 0.3)), (4.6 * np.cos(a), 4.6 * np.sin(a)), (1.2 * np.cos(a + 0.3), 1.2 * np.sin(a + 0.3))], fc="#FBD38D", ec="#555"))
    for (x, y, r) in [(-2.5, 2, 1.3), (2.2, 2.5, 1.0), (0, -1, 1.5), (-3, -3, 0.8), (3, -2.5, 1.1)]:
        axs[3].add_patch(Circle((x, y), r, fc="#FBD38D", ec="#555"))
    for i, a in enumerate(axs):
        a.set_title(f"Bentuk {i + 1}", fontweight="bold")
    fig.suptitle("Empat bentuk morfologi kota (kuning = kawasan terbangun)", fontweight="bold")
    save(fig, path)


def f_fringe(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    for i, (r, c) in enumerate([(46, "#C6F6D5"), (36, "#E6FFFA"), (26, "#FEFCBF"), (14, "#FBD38D")]):
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#555"))
    for t, r in [("P", 7), ("Q", 20), ("R", 31), ("S", 41)]:
        ax.text(0, r, t, ha="center", va="center", fontsize=15, fontweight="bold")
    ax.text(0, -7, "kota inti", ha="center", fontsize=9); ax.text(0, -20, "campuran sawah\n& perumahan baru", ha="center", fontsize=8)
    ax.text(0, -31, "desa dengan sedikit\nciri kekotaan", ha="center", fontsize=8); ax.text(0, -42, "perdesaan", ha="center", fontsize=8)
    ax.set_title("Zona-zona di wilayah peralihan desa–kota")
    save(fig, path)


def f_sprawl(path):
    lines([2000, 2005, 2010, 2015, 2020], {"Luas kawasan terbangun": [100, 128, 160, 196, 240], "Jumlah penduduk": [100, 112, 124, 136, 150]}, path,
          title="Kawasan terbangun dan penduduk Kota M (indeks, 2000 = 100)", xlabel="Tahun", ylabel="indeks", w=8.5, xticks=[2000, 2005, 2010, 2015, 2020])


def f_potensi(path):
    table([["Kota A (100 ribu jiwa)", "10 km", "20 km"], ["Kota B (200 ribu jiwa)", "20 km", "10 km"], ["Kota C (50 ribu jiwa)", "5 km", "25 km"]],
          ["Pusat penduduk", "Jarak ke lokasi X", "Jarak ke lokasi Y"], path, title="Jarak dua calon lokasi pusat perbelanjaan ke tiga kota", col_w=[0.42, 0.29, 0.29])


def f_informal(path):
    fig, ax = blank(9, 5.2, (0, 100), (0, 58))
    ax.add_patch(Rectangle((0, 0), 100, 58, fc="#F7FAFC"))
    xs = np.linspace(0, 100, 100); ys = 30 + 8 * np.sin(xs / 14)
    ax.plot(xs, ys, color=C["blue"], lw=6); ax.text(85, 40, "sungai", color=C["blue"], fontsize=10)
    ax.plot([0, 100], [10, 10], color="#4A5568", lw=3, ls=(0, (6, 3))); ax.text(80, 5, "rel kereta", fontsize=10)
    rnd = np.random.RandomState(5)
    for _ in range(45):
        x = rnd.uniform(2, 98); y = 30 + 8 * np.sin(x / 14) + rnd.choice([-1, 1]) * rnd.uniform(3.5, 6)
        ax.add_patch(Rectangle((x, y), 1.8, 1.5, fc="#C05621", ec="none"))
    for _ in range(25):
        x = rnd.uniform(2, 98); ax.add_patch(Rectangle((x, 12.5 + rnd.uniform(0, 2.5)), 1.8, 1.5, fc="#C05621", ec="none"))
    for (x, y) in [(15, 48), (45, 50), (75, 49), (30, 20), (60, 22)]:
        ax.add_patch(Rectangle((x, y), 8, 6, fc="#A0AEC0", ec="#555"))
    ax.text(50, 56, "■ cokelat = permukiman informal padat · ■ abu-abu = perumahan formal", ha="center", fontsize=9)
    ax.set_title("Sebaran permukiman informal di Kota K (ilustrasi)")
    save(fig, path)


# ---- paket 2
def f_speed(path):
    h = np.arange(0, 24)
    sp = 42 - 22 * np.exp(-((h - 7.5) / 1.4) ** 2) - 24 * np.exp(-((h - 17.5) / 1.6) ** 2)
    lines(h, {"Kecepatan rata-rata (km/jam)": sp}, path, title="Kecepatan rata-rata kendaraan di jalan arteri Kota J pada hari kerja", xlabel="Jam",
          ylabel="km/jam", xticks=range(0, 24, 2), w=8.5)


def f_sampah(path):
    yr = np.arange(2018, 2031)
    prod = 7.0 * 1.035 ** (yr - 2018)
    fig, ax = new(8.5, 4.4)
    ax.plot(yr, prod, marker="o", color=C["orange"], lw=2.2, label="Sampah yang diangkut ke TPA (ribu ton/hari)")
    ax.axhline(9.0, color=C["red"], ls="--"); ax.text(2018.2, 9.1, "kapasitas maksimum TPA = 9 ribu ton/hari", fontsize=9, color=C["red"])
    ax.set_xticks(yr[::2]); ax.set_ylabel("ribu ton per hari"); ax.legend(frameon=False, loc="upper left"); ax.grid(color="#EDF2F7")
    ax.set_title("Proyeksi sampah kota dan kapasitas TPA (ilustrasi)")
    save(fig, path)


def f_pm_jam(path):
    h = np.arange(0, 24)
    pm = 35 + 30 * np.exp(-((h - 7) / 1.6) ** 2) + 25 * np.exp(-((h - 19) / 2) ** 2) - 8 * np.exp(-((h - 14) / 2.5) ** 2)
    lines(h, {"PM2,5 (µg/m³)": pm}, path, title="Rata-rata konsentrasi PM2,5 per jam di Kota J", xlabel="Jam", ylabel="µg/m³", xticks=range(0, 24, 2), w=8.5)


def f_backlog(path):
    bars(["2015", "2020", "2025"], {"Jumlah rumah tangga (ribu)": [2600, 2850, 3100], "Jumlah unit rumah layak (ribu)": [2300, 2500, 2700]}, path,
         title="Rumah tangga dan rumah layak huni di Kota B", ylabel="ribu", values=True, ylim=(0, 3500), w=8)


def f_moda(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [70, 15, 10, 5]; lab = ["Sepeda motor", "Mobil pribadi", "Angkutan umum", "Jalan kaki & sepeda"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=[C["orange"], C["red"], C["blue"], C["green"]], startangle=90, wedgeprops=dict(ec="white"))
    ax.set_title("Pembagian moda perjalanan komuter di Kota M")
    save(fig, path)


# ---- paket 3
def f_segmap(path):
    fig, ax = new(6.5, 6)
    rnd = np.random.RandomState(1)
    g = np.zeros((10, 10))
    for i in range(10):
        for j in range(10):
            g[i, j] = 1 if (i < 4 and j > 5) else (3 if (i > 6 and j < 4) else 2)
    g[1, 1] = 1; g[8, 8] = 3
    from matplotlib.colors import ListedColormap
    ax.imshow(g, cmap=ListedColormap(["#2B6CB0", "#E2E8F0", "#E53E3E"]), vmin=1, vmax=3)
    ax.set_xticks([]); ax.set_yticks([])
    legend_patches(ax, [("Perumahan mewah berpagar", "#2B6CB0"), ("Perumahan menengah", "#E2E8F0"), ("Permukiman berpenghasilan rendah", "#E53E3E")],
                   loc="lower center", fs=8)
    ax.set_title("Sebaran tipe permukiman di Kota T (sel = 1 km²)")
    save(fig, path)


def f_gentri(path):
    yr = [2010, 2013, 2016, 2019, 2022]
    fig, ax = new(8.5, 4.4)
    ax.plot(yr, [100, 120, 180, 260, 330], marker="o", color=C["red"], lw=2.2, label="Indeks harga sewa (2010 = 100)")
    ax.set_ylabel("Indeks sewa", color=C["red"])
    ax2 = ax.twinx(); ax2.plot(yr, [90, 82, 60, 42, 30], marker="s", color=C["blue"], lw=2.2, label="Penduduk asli yang bertahan (%)")
    ax2.set_ylabel("%", color=C["blue"]); ax2.spines["top"].set_visible(False)
    ax.axvline(2014, color="#A0AEC0", ls="--"); ax.text(2014.2, 300, "revitalisasi\n& kafe baru", fontsize=9)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, loc="center left")
    ax.set_title("Perubahan di kawasan kampung kota dekat pusat Kota G")
    save(fig, path)


def f_konsolidasi(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 10); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
    rnd = np.random.RandomState(3)
    for i in range(9):
        x, y = (i % 3) * 3.3, (i // 3) * 3.3
        axs[0].add_patch(Polygon([(x + rnd.uniform(0, .5), y), (x + 3.3, y + rnd.uniform(0, .6)), (x + 3.3 - rnd.uniform(0, .5), y + 3.3), (x, y + 3.3 - rnd.uniform(0, .5))],
                                 fc=plt.cm.Pastel1(i), ec="#555"))
    axs[0].set_title("Sebelum: petak tidak beraturan, tanpa jalan")
    for i in range(8):
        x = 0.3 + (i % 4) * 2.4; y = 0.4 if i < 4 else 6.0
        axs[1].add_patch(Rectangle((x, y), 2.1, 3.4, fc=plt.cm.Pastel1(i), ec="#555"))
    axs[1].add_patch(Rectangle((0, 4.0), 10, 1.6, fc="#A0AEC0")); axs[1].text(5, 4.8, "jalan & saluran", ha="center", fontsize=9)
    axs[1].add_patch(Rectangle((9.9, 0.4), 0.1, 0.1, fc="none"))
    axs[1].set_title("Sesudah: petak lebih kecil, jalan & fasilitas")
    fig.suptitle("Penataan sebuah kawasan permukiman", fontweight="bold")
    save(fig, path)


def f_dissim(path):
    table([["Kecamatan 1", "40", "5"], ["Kecamatan 2", "30", "15"], ["Kecamatan 3", "20", "30"], ["Kecamatan 4", "10", "50"], ["Total", "100", "100"]],
          ["Wilayah", "Pendapatan tinggi (ribu)", "Pendapatan rendah (ribu)"], path, title="Sebaran dua kelompok pendapatan di Kota R",
          col_w=[0.26, 0.37, 0.37], fs=10.5)


def f_kip(path):
    bars(["Akses air bersih", "Jalan lingkungan\ndiperkeras", "Sanitasi layak", "Drainase berfungsi"], {"Sebelum program": [35, 40, 30, 25], "Sesudah program": [80, 90, 72, 70]}, path,
         title="Kondisi kampung sebelum dan sesudah program (% rumah tangga)", ylabel="%", values=True, ylim=(0, 105), w=9)


# ---- paket 4
def f_garden(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    ax.add_patch(Circle((0, 0), 46, fc="#9AE6B4", ec="#2F855A")); ax.add_patch(Circle((0, 0), 30, fc="#FEFCBF", ec="#555"))
    ax.add_patch(Circle((0, 0), 10, fc="#C6F6D5", ec="#555"))
    for k in range(6):
        a = np.radians(60 * k); ax.plot([10 * np.cos(a), 30 * np.cos(a)], [10 * np.sin(a), 30 * np.sin(a)], color="#2D3748", lw=2)
    ax.text(0, 0, "taman\n& gedung\npublik", ha="center", va="center", fontsize=8); ax.text(0, 20, "permukiman, toko, sekolah", ha="center", fontsize=8)
    ax.text(0, 38, "sabuk hijau pertanian & hutan", ha="center", fontsize=8)
    ax.set_title("Sebuah konsep kota ideal (awal abad ke-20)")
    save(fig, path)


def f_tod(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    for r, c, t in [(44, "#E2E8F0", "S"), (30, "#FEFCBF", "R"), (16, "#FBD38D", "Q")]:
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#555")); ax.text(0, r - 6, t, ha="center", fontsize=14, fontweight="bold")
    ax.add_patch(Rectangle((-3, -3), 6, 6, fc="#E53E3E")); ax.text(0, -8, "P (stasiun MRT)", ha="center", fontsize=9, fontweight="bold")
    ax.plot([-50, 50], [0, 0], color="#2D3748", lw=2)
    ax.text(-48, 46, "Q: radius ±400 m · R: ±800 m · S: > 800 m", fontsize=9)
    ax.set_title("Zona di sekitar stasiun angkutan massal")
    save(fig, path)


def f_smart(path):
    dims = ["Smart\ngovernance", "Smart\neconomy", "Smart\nmobility", "Smart\nenvironment", "Smart\npeople", "Smart\nliving"]
    v = [78, 70, 42, 65, 72, 68]
    bars(dims, {"Skor (0–100)": v}, path, title="Skor enam dimensi kota cerdas Kota C", ylabel="skor", values=True, ylim=(0, 100), colors=[C["teal"]], w=9)


def f_kdb(path):
    fig, ax = blank(8, 5, (0, 100), (0, 62))
    ax.add_patch(Rectangle((5, 5), 90, 8, fc="#C6F6D5", ec="#2F855A")); ax.text(50, 9, "kaveling 1.000 m²", ha="center", fontsize=10)
    for i in range(5):
        ax.add_patch(Rectangle((25, 13 + i * 9), 50, 9, fc="#BEE3F8", ec="#2B6CB0")); ax.text(50, 17.5 + i * 9, f"lantai {i + 1}", ha="center", fontsize=9)
    ax.text(50, 60, "KDB 50% · KLB 2,5 · KDH 20%", ha="center", fontsize=12, fontweight="bold")
    ax.set_title("Ketentuan intensitas bangunan sebuah kaveling")
    save(fig, path)


def f_spons(path):
    fig, ax = blank(10, 4.6, (0, 100), (0, 46))
    ax.fill_between([0, 100], [0, 0], [10, 10], color="#C6A77B")
    items = [("atap hijau", 8, 30), ("taman hujan", 28, 13), ("perkerasan\nberpori", 47, 13), ("sumur resapan", 66, 13), ("kolam retensi", 86, 13)]
    ax.add_patch(Rectangle((2, 10), 14, 18, fc="#E2E8F0", ec="#555")); ax.add_patch(Rectangle((2, 28), 14, 3, fc="#68D391"))
    ax.add_patch(Ellipse((28, 10), 12, 4, fc="#9AE6B4", ec="#2F855A"))
    ax.add_patch(Rectangle((40, 9), 14, 2, fc="#CBD5E0", ec="#555"))
    ax.add_patch(Rectangle((64, 2), 4, 8, fc=C["lblue"], ec="#555"))
    ax.add_patch(Ellipse((86, 9), 18, 6, fc=C["lblue"], ec=C["blue"]))
    for t, x, y in items:
        ax.text(x, y + 6 if t != "atap hijau" else y + 4, t, ha="center", fontsize=9)
    for x in range(5, 100, 6):
        ax.plot([x, x - 1], [44, 40], color=C["blue"], lw=1)
    ax.set_title("Komponen pengelolaan air hujan sebuah kawasan kota")
    save(fig, path)


# ---- paket 5
def f_hierarki(path):
    fig, ax = blank(9, 4.4, (0, 100), (0, 46))
    items = ["RTRW Nasional", "RTRW Provinsi", "RTRW Kabupaten/Kota", "?"]
    for i, t in enumerate(items):
        box(ax, 20 + i * 6, 36 - i * 11, 60 - i * 12, 8, t, fc="#FEFCBF" if t == "?" else "#EBF8FF", fs=11 if t != "?" else 18, bold=t == "?")
        if i < 3:
            arrow(ax, 50, 36 - i * 11, 50, 44 - (i + 1) * 11 - 0.3)
    ax.set_title("Hierarki rencana tata ruang di Indonesia (umum → rinci)")
    save(fig, path)


def f_metro(path):
    fig, ax = indonesia_map(extent=(95, 126, -9.5, 5), w=10, h=5)
    for n, (x, y) in {"P": (106.8, -6.2), "Q": (112.7, -7.3), "R": (98.7, 3.6), "S": (110.4, -7.0), "T": (119.4, -5.1)}.items():
        ax.add_patch(Circle((x, y), 0.6, fc=C["red"], ec="white", alpha=0.85)); ax.text(x + 0.8, y + 0.6, n, fontsize=13, fontweight="bold", color=C["red"],
                                                                                         bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Lima kawasan metropolitan di Indonesia")
    save(fig, path)


def f_kontinum(path):
    cats = ["Desa\nterpencil", "Desa\ndekat kota", "Kota\nkecamatan", "Kota\nsedang", "Kota\nmetropolitan"]
    bars(cats, {"Penduduk bekerja di pertanian (%)": [85, 55, 30, 10, 2], "Rumah tangga berinternet (%)": [20, 45, 60, 78, 90]}, path,
         title="Ciri sosial-ekonomi sepanjang kontinum desa–kota (ilustrasi)", ylabel="%", values=True, ylim=(0, 100), w=9.5)


def f_pasok(path):
    fig, ax = blank(10, 4.6, (0, 100), (0, 46))
    box(ax, 40, 16, 20, 14, "Kota J\n(10 juta jiwa)", fc="#FEFCBF", fs=10, bold=True)
    for t, x, y in [("Beras: Jawa Barat,\nJawa Tengah", 3, 33), ("Sayur: dataran tinggi\nBandung & Bogor", 3, 4), ("Daging sapi: NTT,\nimpor Australia", 74, 33),
                    ("Ikan: Laut Jawa,\nSulawesi", 74, 4)]:
        box(ax, x, y, 23, 9, t, fc="#EBF8FF", fs=8.5)
        arrow(ax, x + 11.5 + (10 if x < 50 else -10), y + 4.5, 50 + (-10 if x < 50 else 10), 23, color=C["gray"])
    ax.set_title("Asal pasokan pangan sebuah kota besar")
    save(fig, path)


def f_jejakkota(path):
    bars(["Kota P", "Kota Q", "Kota R"], {"Jejak ekologis (gha/orang)": [3.2, 1.9, 1.2], "Biokapasitas wilayah kota (gha/orang)": [0.2, 0.3, 0.6]}, path,
         title="Jejak ekologis dan biokapasitas tiga kota (ilustrasi)", ylabel="gha per orang", values=True, ylim=(0, 3.8), w=8)


# ============================ questions ============================
P0 = [
    Q("Perhatikan model zona konsentris berikut.\n\nZona yang dalam model Burgess disebut zona peralihan (transisi), dicirikan bangunan tua, gudang, dan permukiman kumuh, ditunjukkan oleh nomor …",
      ["2", "1", "3", "4", "5"],
      "Model konsentris Burgess (1925), berdasarkan kota Chicago, terdiri atas lima zona:\n1) Pusat kegiatan bisnis (CBD): perdagangan, perkantoran, dan hiburan.\n2) Zona peralihan (transisi): campuran gudang, industri ringan, bangunan tua, dan permukiman kumuh yang dihuni pendatang baru berpenghasilan rendah.\n3) Zona permukiman pekerja berpenghasilan rendah.\n4) Zona permukiman kelas menengah.\n5) Zona penglaju (komuter): permukiman kelas atas di pinggiran.\nZona 2 berada tepat di sekeliling CBD, sehingga sering terkena ekspansi CBD dan mengalami kemunduran kualitas.\n\nPengecoh: zona lain tidak dicirikan campuran gudang dan permukiman kumuh.",
      f_burgess),
    Q("Sebuah provinsi berpenduduk 12 juta jiwa, dengan 7,2 juta jiwa tinggal di kawasan perkotaan. Tingkat urbanisasi provinsi tersebut adalah …",
      ["60%", "40%", "167%", "72%", "4,8%"],
      "Tingkat urbanisasi = penduduk perkotaan ÷ penduduk total × 100% = 7,2 ÷ 12 × 100% = 60%.\nArtinya 60% penduduk provinsi tinggal di kawasan perkotaan. Tingkat urbanisasi berbeda dengan laju urbanisasi, yang menunjukkan seberapa cepat porsi penduduk kota meningkat.\n\nPengecoh: 40% adalah porsi penduduk perdesaan. 167% membalik pembagian. 72% salah membaca angka 7,2. 4,8% adalah selisih penduduk total dan perkotaan (dalam juta) yang dibaca sebagai persen.",
      None),
    Q("Perhatikan kurva sewa lahan tiga penggunaan lahan kota berikut.\n\nBatas antara zona perdagangan dan permukiman terletak pada jarak sekitar … dari pusat kota.",
      ["5,7 km", "10,0 km", "20,0 km", "7,1 km", "3,3 km"],
      "Batas zona berada pada titik ketika sewa kedua penggunaan lahan sama:\n1.000 − 100d = 600 − 30d → 400 = 70d → d ≈ 5,7 km.\nDi dekat pusat kota (< 5,7 km), perdagangan mampu membayar sewa tertinggi karena sangat membutuhkan aksesibilitas, sehingga kurvanya paling curam. Di luar jarak tersebut, permukiman lebih mampu membayar sewa. Inilah dasar teori bid-rent yang menjelaskan pola penggunaan lahan konsentris.\n\nPengecoh: 10 km adalah titik ketika sewa perdagangan menjadi nol. 20 km adalah batas sewa permukiman nol. 7,1 km dan 3,3 km berasal dari kesalahan aljabar.",
      f_bidrent),
    Q("Setelah suburbanisasi berlangsung lama, sebagian kota besar di negara maju justru mengalami kembalinya penduduk muda ke pusat kota yang direvitalisasi. Tahap siklus perkotaan ini disebut …",
      ["Reurbanisasi", "Urbanisasi awal", "Suburbanisasi", "Kontraurbanisasi", "Ruralisasi total"],
      "Model siklus perkotaan (van den Berg) terdiri atas empat tahap:\n1) Urbanisasi: penduduk berpindah dari desa ke kota sehingga pusat kota tumbuh cepat.\n2) Suburbanisasi: penduduk dan kegiatan pindah dari pusat kota ke pinggiran (suburban) karena kendaraan pribadi, harga lahan, dan lingkungan yang lebih nyaman.\n3) Kontraurbanisasi (desurbanisasi): penduduk meninggalkan kawasan metropolitan menuju kota kecil atau perdesaan.\n4) Reurbanisasi: penduduk, terutama generasi muda dan profesional, kembali ke pusat kota yang telah diremajakan karena dekat dengan pekerjaan, budaya, dan transportasi umum.\n\nPengecoh: tahap lain menggambarkan arah perpindahan yang berbeda. Ruralisasi total bukan istilah tahap siklus perkotaan.",
      None),
    Q("Perhatikan model sektor kota berikut.\n\nPernyataan yang paling sesuai dengan model Hoyt adalah …",
      ["Permukiman atas (Q) memanjang mengikuti jalan utama", "Semua penggunaan lahan tersusun dalam cincin yang sama lebarnya",
       "Kota memiliki banyak pusat kegiatan yang tersebar acak", "Industri berat selalu berada tepat di tengah pusat kota",
       "Permukiman berpenghasilan rendah selalu berada paling jauh dari pusat"],
      "Model sektor Homer Hoyt (1939) menyatakan bahwa penggunaan lahan kota berkembang dalam bentuk sektor atau baji (irisan) yang memanjang dari pusat kota (P) ke arah luar, mengikuti jalur transportasi seperti jalan raya, rel kereta, atau sungai. Kawasan permukiman kelas atas cenderung berkembang di sepanjang koridor yang paling menarik, misalnya dekat jalan utama atau daerah yang lebih tinggi, sementara industri dan permukiman kelas bawah berkembang di sektor lain, misalnya di sekitar jalur rel.\n\nPengecoh: susunan cincin adalah model konsentris Burgess. Banyak pusat adalah model inti ganda Harris–Ullman. Industri berat tidak berada di pusat kota. Permukiman berpenghasilan rendah tidak selalu paling jauh.",
      f_hoyt),
    Q("Sebuah kaveling seluas 1.000 m² memiliki ketentuan KDB 60% dan KLB 3,0. Jika seluruh lantai dibangun dengan luas sama seperti lantai dasar maksimum, jumlah lantai maksimum yang dapat dibangun adalah …",
      ["5 lantai", "3 lantai", "6 lantai", "2 lantai", "18 lantai"],
      "• Luas lantai dasar maksimum = KDB × luas kaveling = 60% × 1.000 = 600 m².\n• Luas total lantai maksimum = KLB × luas kaveling = 3,0 × 1.000 = 3.000 m².\n• Jumlah lantai = 3.000 ÷ 600 = 5 lantai (atau KLB ÷ KDB = 3,0 ÷ 0,6 = 5).\nKetentuan KDB menjaga ruang terbuka dan resapan di kaveling, sedangkan KLB mengendalikan intensitas pemanfaatan ruang, misalnya kepadatan penghuni dan beban lalu lintas.\n\nPengecoh: 3 lantai hanya membaca KLB. 6 lantai salah memakai angka KDB. 2 lantai dan 18 lantai berasal dari perhitungan yang keliru.",
      None),
    Q("Perhatikan model struktur ruang sebuah kota berikut.\n\nModel tersebut paling sesuai dengan teori …",
      ["Inti ganda Harris–Ullman", "Zona konsentris Burgess", "Sektor Hoyt", "Kota taman Howard", "Tempat sentral Christaller"],
      "Gambar menunjukkan kota yang memiliki beberapa pusat kegiatan yang terpisah: pusat bisnis utama (1), pusat bisnis sekunder (4), kawasan industri berat (3), kawasan bandara atau kampus (5), dan permukiman kelas atas (2), yang tidak tersusun dalam cincin atau sektor beraturan. Model inti ganda Harris dan Ullman (1945) menjelaskan bahwa kota besar berkembang di sekitar beberapa inti, karena kegiatan tertentu membutuhkan fasilitas khusus, kegiatan sejenis cenderung berkelompok, kegiatan yang saling bertentangan saling menjauh, dan tidak semua kegiatan mampu membayar sewa di pusat kota. Model ini cocok untuk kota metropolitan modern seperti Jakarta.\n\nPengecoh: Burgess berbentuk cincin. Hoyt berbentuk sektor dari satu pusat. Kota taman adalah konsep perencanaan. Christaller menjelaskan sistem antarkota, bukan struktur internal kota.",
      f_inti),
    Q("Kota A berpenduduk 4 juta jiwa dan Kota B berpenduduk 1 juta jiwa, berjarak 100 km. Dengan rumus titik henti DB = d ÷ (1 + √(PA ÷ PB)), lokasi titik henti antara kedua kota adalah …",
      ["Sekitar 33 km dari Kota B", "Sekitar 50 km dari Kota B", "Sekitar 67 km dari Kota B", "Sekitar 20 km dari Kota B", "Sekitar 25 km dari Kota B"],
      "DB = 100 ÷ (1 + √(4 ÷ 1)) = 100 ÷ (1 + 2) = 100 ÷ 3 ≈ 33,3 km dari Kota B.\nTitik henti (breaking point) adalah batas wilayah pengaruh dua kota. Karena Kota A jauh lebih besar, wilayah pengaruhnya lebih luas sehingga titik henti lebih dekat ke Kota B, kota yang lebih kecil. Konsep ini dipakai, misalnya, untuk menentukan lokasi pasar atau fasilitas di antara dua kota.\n\nPengecoh: 50 km adalah titik tengah bila penduduk kedua kota sama. 67 km adalah jarak titik henti dari Kota A. 20 km dan 25 km berasal dari salah memakai akar atau perbandingan penduduk.",
      None),
    Q("Perhatikan grafik gradien kepadatan penduduk sebuah kota metropolitan berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Pusat kota makin renggang, pinggiran makin padat", "Penduduk semakin terkonsentrasi di pusat kota dari 1980 ke 2020",
       "Kepadatan di seluruh bagian kota tidak berubah", "Kota menyusut sehingga pinggiran menjadi kosong", "Gradien kepadatan menjadi makin curam dari waktu ke waktu"],
      "Grafik menunjukkan kepadatan di pusat kota turun dari ±25.000 jiwa/km² (1980) menjadi ±14.500 jiwa/km² (2020), sedangkan kepadatan di jarak 10–30 km dari pusat meningkat. Kurva menjadi makin landai (gradien makin datar). Pola ini menandakan suburbanisasi: penduduk berpindah dari pusat kota ke pinggiran karena harga lahan di pusat mahal, pusat kota beralih fungsi menjadi kawasan bisnis, dan pembangunan perumahan serta jalan tol di pinggiran.\n\nPengecoh: penduduk justru menyebar keluar. Kepadatan jelas berubah. Pinggiran justru makin padat. Gradien menjadi makin landai, bukan curam.",
      f_densgrad),
    Q("Perhatikan sebaran dua kelompok penduduk di Kota S berikut. Indeks disimilaritas D = ½ × Σ|aᵢ/A − bᵢ/B|.\n\nNilai indeks segregasi Kota S adalah …",
      ["0,40", "0,80", "0,20", "0,60", "1,00"],
      "Hitung porsi tiap kelompok di setiap kelurahan:\n• Kelurahan 1: |50/100 − 10/100| = |0,5 − 0,1| = 0,4.\n• Kelurahan 2: |0,3 − 0,3| = 0.\n• Kelurahan 3: |0,2 − 0,6| = 0,4.\nΣ = 0,8 → D = ½ × 0,8 = 0,40.\nArtinya sekitar 40% penduduk salah satu kelompok perlu pindah ke kelurahan lain agar kedua kelompok tersebar merata. Nilai 0 berarti merata sempurna, sedangkan 1 berarti terpisah sempurna.\n\nPengecoh: 0,80 lupa mengalikan ½. 0,20, 0,60, dan 1,00 berasal dari salah menjumlahkan atau membaca data.",
      f_segre),
]

P1 = [
    Q("Perhatikan data penduduk Negara U berikut. Laju urbanisasi = laju pertumbuhan penduduk kota − laju pertumbuhan penduduk total.\n\nLaju urbanisasi dan maknanya adalah …",
      ["1,6% per tahun; porsi penduduk kota terus meningkat", "4,0% per tahun; jumlah penduduk total naik dua kali lipat",
       "1,6% per tahun; porsi penduduk kota menurun", "2,8% per tahun; seluruh penduduk sudah tinggal di kota", "−1,6% per tahun; terjadi ruralisasi"],
      "Laju urbanisasi = 2,8% − 1,2% = 1,6% per tahun.\nNilai positif berarti penduduk perkotaan tumbuh lebih cepat daripada penduduk total, sehingga porsi (tingkat urbanisasi) penduduk kota terus meningkat. Saat ini tingkat urbanisasi Negara U = 110 ÷ 200 = 55%. Kenaikan porsi penduduk kota disebabkan migrasi desa–kota, pertumbuhan alami penduduk kota, dan perubahan status desa menjadi kawasan perkotaan.\n\nPengecoh: 4,0% menjumlahkan kedua laju. Laju positif berarti porsi kota naik, bukan turun. 2,8% adalah laju pertumbuhan penduduk kota, bukan laju urbanisasi. Nilai negatif muncul bila pengurangan dibalik.",
      f_lajukota),
    Q("Perhatikan empat bentuk morfologi kota berikut.\n\nKota yang berkembang memanjang mengikuti jalan raya utama atau garis pantai ditunjukkan oleh bentuk …",
      ["2, bentuk pita atau memanjang", "1, bentuk kompak bulat", "3, bentuk gurita atau bintang", "4, bentuk terpecah", "1 dan 3 secara bersamaan"],
      "Morfologi kota menurut bentuk kawasan terbangunnya:\n• Bentuk 1: kompak (bulat/bujur sangkar), berkembang relatif merata ke segala arah karena tidak ada hambatan fisik.\n• Bentuk 2: pita atau memanjang (ribbon), berkembang mengikuti jalur transportasi seperti jalan raya atau garis pantai, misalnya kota-kota di sepanjang jalur pantura Jawa.\n• Bentuk 3: gurita atau bintang, berkembang dari pusat ke beberapa arah mengikuti beberapa jalur jalan utama.\n• Bentuk 4: terpecah (fragmented), kawasan terbangun terpisah-pisah, misalnya karena perluasan yang melompat atau hambatan fisik.\n\nPengecoh: bentuk lain tidak memanjang mengikuti satu jalur.",
      f_bentuk),
    Q("Penduduk sebuah kota tumbuh dari 1,0 juta jiwa menjadi 1,5 juta jiwa dalam 10 tahun. Laju pertumbuhan geometrik rata-rata per tahun adalah sekitar …",
      ["4,1%", "5,0%", "50%", "15%", "1,5%"],
      "Laju geometrik r = (Pt ÷ P0)^(1/t) − 1 = (1,5)^(1/10) − 1.\nKarena 1,041¹⁰ ≈ 1,49, maka r ≈ 0,041 = 4,1% per tahun.\nModel geometrik memperhitungkan bahwa pertumbuhan tiap tahun bertumpu pada jumlah penduduk tahun sebelumnya (majemuk), sehingga lajunya lebih kecil daripada perhitungan linear.\n\nPengecoh: 5,0% adalah laju linear (50% ÷ 10). 50% adalah pertumbuhan total 10 tahun. 15% dan 1,5% berasal dari kesalahan desimal atau membaca rasio.",
      None),
    Q("Perhatikan zona-zona di wilayah peralihan desa–kota berikut.\n\nZona yang paling banyak mengalami konversi sawah menjadi perumahan baru dan memiliki penggunaan lahan campuran desa dan kota adalah …",
      ["Q, zona bingkai kota (urban fringe)", "P, kota inti", "R, zona bingkai desa (rural fringe)", "S, perdesaan murni", "P dan S secara bersamaan"],
      "Wilayah peralihan desa–kota (wilayah peri-urban) terdiri atas beberapa zona. Q adalah zona bingkai kota (urban fringe), berbatasan langsung dengan kota inti (P). Di zona ini penggunaan lahan kekotaan dan kedesaan bercampur: sawah masih ada tetapi cepat dikonversi menjadi perumahan, kawasan industri, dan pusat perdagangan baru. Harga lahan naik pesat dan banyak penduduk bekerja di kota (penglaju). Zona R (bingkai desa) masih didominasi ciri kedesaan dengan sedikit ciri kota, dan zona S adalah perdesaan.\n\nPengecoh: P sudah sepenuhnya kekotaan. R dan S masih didominasi ciri desa sehingga konversinya lebih kecil.",
      f_fringe),
    Q("Jakarta, Bogor, Depok, Tangerang, dan Bekasi telah tumbuh menyatu membentuk satu kawasan perkotaan yang saling terhubung. Gejala ini disebut …",
      ["Konurbasi kota", "Ruralisasi", "Kontraurbanisasi", "Gentrifikasi", "Deindustrialisasi"],
      "Konurbasi adalah gejala menyatunya beberapa kota yang semula terpisah menjadi satu kawasan perkotaan besar karena pertumbuhan dan perluasan kawasan terbangun masing-masing, sehingga batas fisik antarkota sulit dibedakan. Jabodetabek adalah contoh konurbasi atau kawasan metropolitan di Indonesia. Bila beberapa kawasan metropolitan menyatu dalam skala sangat besar, terbentuk megalopolis, seperti koridor Boston–Washington di Amerika Serikat.\n\nPengecoh: ruralisasi adalah perpindahan ke desa. Kontraurbanisasi adalah perpindahan keluar dari metropolitan. Gentrifikasi adalah perubahan sosial kawasan kota. Deindustrialisasi adalah menurunnya peran industri.",
      None),
    Q("Perhatikan grafik pertumbuhan kawasan terbangun dan penduduk Kota M berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Kawasan terbangun tumbuh lebih cepat dari penduduk", "Penduduk tumbuh lebih cepat daripada kawasan terbangun",
       "Kota menjadi makin padat dan kompak", "Kawasan terbangun dan penduduk tumbuh sama cepat", "Luas kawasan terbangun menurun sejak tahun 2000"],
      "Grafik menunjukkan indeks luas kawasan terbangun naik dari 100 menjadi 240 (naik 140%), sedangkan penduduk hanya naik dari 100 menjadi 150 (naik 50%) dalam periode 2000–2020. Artinya kawasan terbangun berkembang jauh lebih cepat daripada penduduk sehingga kepadatan rata-rata menurun. Gejala ini menandakan pemekaran kota yang menyebar (urban sprawl), misalnya perumahan berkepadatan rendah di pinggiran. Dampaknya: konversi lahan pertanian, biaya infrastruktur tinggi, dan ketergantungan pada kendaraan pribadi.\n\nPengecoh: penduduk tumbuh lebih lambat. Kota justru makin tidak kompak. Laju keduanya berbeda. Luas terbangun bertambah.",
      f_sprawl),
    Q("Menurut klasifikasi kota berdasarkan jumlah penduduk yang lazim dipakai di Indonesia, kota berpenduduk 750.000 jiwa tergolong …",
      ["Kota besar", "Kota kecil", "Kota sedang", "Kota metropolitan", "Kota megapolitan"],
      "Klasifikasi kota berdasarkan jumlah penduduk yang lazim dipakai: kota kecil (< 100.000 jiwa), kota sedang (100.000–500.000 jiwa), kota besar (500.000–1.000.000 jiwa), kota metropolitan (1–10 juta jiwa), dan kota megapolitan (> 10 juta jiwa).\nKota berpenduduk 750.000 jiwa berada pada rentang 500.000–1.000.000 jiwa sehingga tergolong kota besar.\n\nPengecoh: kota kecil dan sedang memiliki penduduk lebih sedikit. Kota metropolitan memerlukan lebih dari satu juta jiwa. Megapolitan lebih dari sepuluh juta jiwa.",
      None),
    Q("Perhatikan jarak dua calon lokasi pusat perbelanjaan ke tiga kota berikut. Potensi penduduk V = Σ(Pⱼ ÷ dⱼ).\n\nLokasi dengan potensi penduduk (aksesibilitas) lebih tinggi beserta nilainya adalah …",
      ["X, dengan V = 30.000", "Y, dengan V = 27.000", "X, dengan V = 25.000", "Y, dengan V = 35.000", "Keduanya sama, V = 30.000"],
      "Hitung V untuk setiap lokasi (P dalam jiwa, d dalam km):\n• Lokasi X: 100.000/10 + 200.000/20 + 50.000/5 = 10.000 + 10.000 + 10.000 = 30.000.\n• Lokasi Y: 100.000/20 + 200.000/10 + 50.000/25 = 5.000 + 20.000 + 2.000 = 27.000.\nLokasi X memiliki potensi penduduk lebih tinggi sehingga lebih mudah dijangkau oleh lebih banyak penduduk secara keseluruhan, walaupun Y lebih dekat ke kota terbesar (B).\n\nPengecoh: Y = 27.000 lebih kecil. Nilai 25.000 dan 35.000 berasal dari salah perhitungan. Keduanya tidak sama.",
      f_potensi),
    Q("Konsep desakota yang dikemukakan T.G. McGee untuk Asia Tenggara menggambarkan …",
      ["Campuran pertanian padat dan kegiatan nonpertanian di koridor kota", "Kota yang sepenuhnya dihuni petani tanpa kegiatan industri",
       "Desa terpencil yang tidak terhubung dengan kota mana pun", "Kota modern yang meniru sepenuhnya struktur kota Amerika Serikat",
       "Pemindahan seluruh penduduk kota ke desa secara paksa"],
      "McGee mengamati bahwa di Asia, terutama di wilayah berpenduduk padat dengan pertanian padi seperti Jawa, perkembangan kota tidak selalu mengikuti pola Barat. Di sepanjang koridor antara kota-kota besar, misalnya Jakarta–Bandung atau Yogyakarta–Solo, terbentuk wilayah desakota (dari bahasa Indonesia \"desa\" dan \"kota\"), yaitu kawasan perdesaan berpenduduk sangat padat dengan sawah yang bercampur industri, perdagangan, perumahan, dan jaringan transportasi. Penduduknya bekerja di sektor pertanian dan nonpertanian sekaligus.\n\nPengecoh: desakota bukan kota tanpa industri, bukan desa terpencil, bukan tiruan kota Amerika, dan bukan pemindahan penduduk secara paksa.",
      None),
    Q("Perhatikan sebaran permukiman informal di Kota K berikut.\n\nPenjelasan yang paling tepat untuk pola sebaran tersebut adalah …",
      ["Bantaran sungai dan rel adalah lahan murah dekat lapangan kerja", "Pemerintah sengaja menempatkan permukiman di bantaran sungai",
       "Lahan di tepi sungai paling aman dari banjir dan longsor", "Penduduk berpenghasilan tinggi memilih tinggal di sepanjang rel kereta",
       "Permukiman informal hanya terdapat di pinggiran kota yang jauh"],
      "Peta menunjukkan permukiman informal padat terkonsentrasi di sepanjang bantaran sungai dan jalur rel kereta, sedangkan perumahan formal berada di lokasi lain. Bantaran sungai dan sempadan rel umumnya adalah lahan negara yang tidak dimanfaatkan, sehingga pendatang berpenghasilan rendah dapat menempatinya tanpa membeli lahan. Lokasinya juga dekat dengan pusat kota dan lapangan kerja informal. Namun permukiman di lokasi ini rawan banjir, kebakaran, dan kecelakaan, serta mengurangi daya tampung sungai.\n\nPengecoh: pemerintah tidak sengaja menempatkannya di sana. Bantaran sungai justru rawan banjir. Penduduk berpenghasilan tinggi tidak memilih tinggal di sepanjang rel. Pada peta, permukiman informal justru berada dekat pusat kota.",
      f_informal),
]

P2 = [
    Q("Perhatikan grafik kecepatan rata-rata kendaraan di jalan arteri Kota J pada hari kerja berikut.\n\nPenyebab utama penurunan kecepatan sekitar pukul 07.00–08.00 dan 17.00–18.00 adalah …",
      ["Pergerakan komuter berangkat dan pulang kerja secara bersamaan", "Hujan deras yang selalu turun pada jam-jam tersebut",
       "Lampu lalu lintas hanya menyala pada jam tersebut", "Penutupan jalan untuk perbaikan setiap pagi dan sore", "Tidak ada kendaraan yang melintas pada jam tersebut"],
      "Grafik menunjukkan kecepatan rata-rata sekitar 40 km/jam pada malam hari, lalu turun tajam menjadi sekitar 20 km/jam pada pukul 07.00–08.00 dan sekitar 18 km/jam pada pukul 17.00–18.00. Kedua lembah ini adalah jam sibuk (peak hours), ketika jutaan komuter berangkat dan pulang kerja atau sekolah secara bersamaan, sehingga volume kendaraan melebihi kapasitas jalan. Solusinya antara lain transportasi massal, pengaturan jam kerja fleksibel, kerja jarak jauh, dan pembatasan kendaraan pribadi.\n\nPengecoh: hujan tidak selalu turun pada jam tersebut. Lampu lalu lintas menyala sepanjang hari. Perbaikan jalan tidak dilakukan rutin pada jam sibuk. Kecepatan rendah justru menandakan kendaraan sangat banyak.",
      f_speed),
    Q("Menurut kriteria yang umum dipakai, ciri berikut yang menunjukkan suatu kawasan tergolong permukiman kumuh adalah …",
      ["Bangunan padat tak teratur dengan sanitasi buruk", "Bangunan tinggi dengan taman luas dan fasilitas lengkap",
       "Jalan lebar, drainase lancar, dan kepadatan rendah", "Rumah bertingkat dengan sertifikat lengkap dan RTH memadai",
       "Kawasan pertanian luas dengan rumah berjauhan"],
      "Permukiman kumuh dicirikan antara lain: kepadatan bangunan sangat tinggi dan tidak teratur; kualitas bangunan rendah; jalan lingkungan sempit; drainase buruk dan sering tergenang; akses air bersih dan sanitasi tidak layak; pengelolaan sampah buruk; rawan kebakaran; dan sering berstatus lahan tidak jelas. Kriteria ini dipakai pemerintah dalam program penanganan kawasan kumuh seperti program Kota Tanpa Kumuh (KOTAKU).\n\nPengecoh: opsi lain menggambarkan kawasan permukiman yang tertata, bukan kumuh, atau kawasan perdesaan pertanian.",
      None),
    Q("Perhatikan grafik proyeksi sampah kota dan kapasitas TPA berikut.\n\nSampah yang diangkut ke TPA diperkirakan melampaui kapasitas maksimum sekitar tahun …",
      ["2026", "2020", "2023", "2029", "2030"],
      "Grafik menunjukkan sampah yang diangkut tumbuh sekitar 3,5% per tahun dari 7,0 ribu ton/hari (2018). Nilainya sekitar 8,6 ribu ton/hari pada 2024, 8,9 ribu pada 2025, dan 9,2 ribu ton/hari pada 2026, sehingga melampaui garis kapasitas maksimum 9 ribu ton/hari sekitar tahun 2026.\nSetelah melampaui kapasitas, risiko longsor sampah, pencemaran lindi, dan penumpukan sampah di kota meningkat. Solusinya antara lain pengurangan sampah dari sumber, pemilahan, pengomposan, bank sampah, daur ulang, dan pengolahan menjadi energi.\n\nPengecoh: 2020 dan 2023 masih di bawah kapasitas. 2029 dan 2030 sudah jauh melampaui kapasitas, bukan titik awal terlampaui.",
      f_sampah),
    Q("Banjir di kota besar seperti Jakarta disebabkan oleh kombinasi beberapa faktor. Faktor yang berasal dari perubahan penggunaan lahan di dalam kota adalah …",
      ["Bertambahnya permukaan kedap air di dalam kota", "Curah hujan ekstrem akibat siklon tropis di Samudra Hindia",
       "Pasang laut tinggi yang bertepatan dengan musim hujan", "Kiriman air dari hulu Sungai Ciliwung di Bogor", "Aktivitas gunung api di sekitar Jakarta"],
      "Banjir kota dipengaruhi faktor alam dan manusia. Faktor yang berasal dari perubahan penggunaan lahan di dalam kota adalah meluasnya permukaan kedap air (aspal, beton, atap) akibat pembangunan, berkurangnya RTH dan daerah resapan, serta penyempitan sungai akibat permukiman di bantaran. Akibatnya koefisien limpasan meningkat, air hujan lebih cepat mengalir ke saluran yang kapasitasnya terbatas, dan genangan terjadi. Amblesan tanah juga memperparah banjir di Jakarta Utara.\n\nPengecoh: curah hujan ekstrem dan pasang laut adalah faktor alam. Kiriman air dari hulu berasal dari luar kota. Tidak ada gunung api aktif yang menyebabkan banjir Jakarta.",
      None),
    Q("Perhatikan grafik rata-rata konsentrasi PM2,5 per jam di Kota J berikut.\n\nPenjelasan yang paling tepat untuk pola tersebut adalah …",
      ["Puncak pagi dan malam terkait lalu lintas dan udara stabil", "PM2,5 tertinggi pada siang hari karena radiasi Matahari menghasilkan debu",
       "PM2,5 sama sepanjang hari karena tidak ada kendaraan", "PM2,5 tertinggi pukul 14.00 karena udara paling dingin",
       "Pola tersebut hanya disebabkan pembakaran sampah pada tengah malam"],
      "Grafik menunjukkan PM2,5 memuncak sekitar pukul 07.00 (±65 µg/m³) dan pukul 19.00 (±60 µg/m³), lalu terendah sekitar pukul 14.00. Puncak pagi dan malam bertepatan dengan jam sibuk lalu lintas. Selain itu, pada pagi hari dan malam hari lapisan udara dekat permukaan cenderung stabil (sering terjadi inversi suhu), sehingga polutan tidak mudah menyebar ke atas. Pada siang hari, pemanasan permukaan membuat udara labil dan lapisan percampuran lebih tebal, sehingga polutan terencerkan.\n\nPengecoh: radiasi Matahari tidak menghasilkan debu, dan PM2,5 justru terendah siang hari. PM2,5 jelas berubah. Pukul 14.00 adalah waktu terpanas, bukan terdingin. Pembakaran sampah tengah malam tidak menjelaskan dua puncak.",
      f_pm_jam),
    Q("Banyak warga di kota pesisir masih mengandalkan air tanah dalam karena cakupan jaringan air perpipaan (PDAM) terbatas. Dampak jangka panjang yang paling dikhawatirkan adalah …",
      ["Amblesan tanah dan intrusi air laut", "Bertambahnya debit sungai di musim kemarau", "Naiknya muka air tanah hingga menggenangi rumah",
       "Turunnya kebutuhan air bersih penduduk", "Bertambahnya luas hutan kota"],
      "Pengambilan air tanah dalam secara berlebihan di kota pesisir seperti Jakarta dan Semarang menurunkan tekanan air di akuifer. Akibatnya lapisan tanah lunak di atasnya memadat sehingga terjadi amblesan tanah (land subsidence), yang memperparah banjir dan rob. Selain itu, berkurangnya tekanan air tawar memungkinkan air laut menyusup ke akuifer (intrusi air laut), sehingga air sumur menjadi payau. Solusinya adalah memperluas jaringan air perpipaan yang bersumber dari air permukaan dan membatasi pengambilan air tanah.\n\nPengecoh: debit sungai tidak bertambah. Muka air tanah justru turun. Kebutuhan air terus naik. Pengambilan air tanah tidak menambah hutan kota.",
      None),
    Q("Perhatikan grafik rumah tangga dan rumah layak huni di Kota B berikut.\n\nKekurangan rumah (backlog) di Kota B dan kecenderungannya adalah …",
      ["Naik dari 300 ribu (2015) menjadi 400 ribu unit (2025)", "Turun dari 400 ribu menjadi 300 ribu unit", "Tetap 300 ribu unit sejak 2015",
       "Tidak ada kekurangan karena rumah lebih banyak dari rumah tangga", "Naik dari 300 ribu menjadi 2.700 ribu unit"],
      "Backlog (kekurangan rumah) = jumlah rumah tangga − jumlah unit rumah layak.\n• 2015: 2.600 − 2.300 = 300 ribu unit.\n• 2020: 2.850 − 2.500 = 350 ribu unit.\n• 2025: 3.100 − 2.700 = 400 ribu unit.\nBacklog terus naik karena pertambahan rumah tangga lebih cepat daripada pembangunan rumah layak. Dampaknya, banyak rumah tangga menumpang, menyewa, atau tinggal di permukiman tidak layak. Solusinya antara lain rumah susun terjangkau, kredit perumahan bersubsidi, dan pembangunan dekat simpul transportasi.\n\nPengecoh: backlog tidak turun dan tidak tetap. Rumah tangga lebih banyak daripada rumah layak. 2.700 ribu adalah jumlah rumah layak 2025, bukan backlog.",
      f_backlog),
    Q("Pedagang kaki lima, ojek pangkalan, dan buruh harian di kota besar merupakan bagian dari sektor informal. Ciri utama sektor informal perkotaan adalah …",
      ["Mudah dimasuki, modal kecil, dan tanpa perlindungan kerja formal", "Selalu memerlukan izin usaha resmi dan modal besar",
       "Memberikan gaji tetap, cuti, dan jaminan pensiun bagi pekerjanya", "Hanya terdapat di negara maju dengan industri berteknologi tinggi",
       "Dikuasai oleh perusahaan multinasional berskala besar"],
      "Sektor informal adalah kegiatan ekonomi yang umumnya tidak terdaftar resmi, berskala kecil, padat karya, menggunakan teknologi sederhana, mudah dimasuki karena modal dan keterampilan yang dibutuhkan kecil, serta tidak memberikan perlindungan kerja formal seperti kontrak, upah minimum, cuti, dan jaminan sosial. Di kota negara berkembang, sektor informal menampung banyak pendatang dari desa yang belum terserap sektor formal, sekaligus menyediakan barang dan jasa murah bagi penduduk kota.\n\nPengecoh: sektor informal tidak selalu berizin dan tidak memerlukan modal besar. Pekerja informal umumnya tidak memperoleh gaji tetap dan jaminan pensiun. Sektor informal justru besar di negara berkembang. Sektor ini tidak dikuasai perusahaan multinasional.",
      None),
    Q("Perhatikan diagram pembagian moda perjalanan komuter di Kota M berikut.\n\nKebijakan yang paling tepat untuk mengurangi kemacetan dan emisi di Kota M adalah …",
      ["Angkutan umum terpadu dan pengendalian kendaraan pribadi", "Menambah lebar jalan tanpa memperbaiki angkutan umum",
       "Menghapus trotoar agar jalan lebih lebar untuk sepeda motor", "Memberikan subsidi pembelian sepeda motor bagi semua warga",
       "Menaikkan tarif angkutan umum agar penumpangnya berkurang"],
      "Diagram menunjukkan 85% perjalanan komuter memakai kendaraan pribadi (70% sepeda motor dan 15% mobil), sedangkan angkutan umum hanya 10% dan jalan kaki serta bersepeda 5%. Ketergantungan pada kendaraan pribadi menyebabkan kemacetan, polusi udara, dan emisi gas rumah kaca. Kebijakan yang efektif adalah menggabungkan dorongan (meningkatkan kualitas, jangkauan, dan integrasi angkutan umum serta fasilitas pejalan kaki dan sepeda) dengan pengendalian (pembatasan parkir, ganjil-genap, atau tarif kemacetan).\n\nPengecoh: pelebaran jalan cenderung menarik lebih banyak kendaraan (induced demand). Menghapus trotoar mengorbankan pejalan kaki. Subsidi sepeda motor menambah kendaraan pribadi. Menaikkan tarif angkutan umum justru mendorong orang beralih ke kendaraan pribadi.",
      f_moda),
    Q("Pemerintah kota menambah jalur jalan tol dalam kota untuk mengatasi kemacetan, tetapi dalam beberapa tahun jalan tersebut kembali macet. Fenomena ini dijelaskan oleh konsep …",
      ["Permintaan terinduksi", "Efek sebar (spread effect)", "Ambang penduduk (threshold)", "Ekonomi aglomerasi", "Kontraurbanisasi"],
      "Permintaan terinduksi (induced demand) adalah gejala ketika penambahan kapasitas jalan justru mendorong bertambahnya perjalanan dengan kendaraan pribadi. Jalan yang baru terasa lancar membuat orang yang sebelumnya memakai angkutan umum, bepergian pada jam lain, atau tidak bepergian beralih menggunakan kendaraan pribadi. Pembangunan perumahan baru di sepanjang jalan juga menambah lalu lintas. Akhirnya jalan kembali macet. Karena itu banyak ahli menyarankan investasi pada angkutan umum massal dan pengelolaan permintaan perjalanan.\n\nPengecoh: efek sebar berkaitan dengan penyebaran pertumbuhan wilayah. Ambang penduduk berkaitan dengan teori tempat sentral. Ekonomi aglomerasi adalah keuntungan pengelompokan kegiatan. Kontraurbanisasi adalah perpindahan penduduk keluar metropolitan.",
      None),
]

P3 = [
    Q("Perhatikan sebaran tipe permukiman di Kota T berikut.\n\nGejala yang paling tepat digambarkan oleh peta adalah …",
      ["Segregasi permukiman berdasarkan pendapatan", "Pemerataan sempurna tipe permukiman di seluruh kota", "Urbanisasi berlebih di kawasan perdesaan",
       "Kontraurbanisasi penduduk berpendapatan tinggi", "Konurbasi dua kota yang berbeda"],
      "Peta menunjukkan perumahan mewah berpagar terkonsentrasi di bagian kanan atas kota, sedangkan permukiman berpenghasilan rendah terkonsentrasi di bagian kiri bawah, dengan perumahan menengah di antaranya. Pemisahan spasial kelompok penduduk menurut pendapatan (atau etnis, agama) disebut segregasi permukiman. Segregasi dapat dipicu harga lahan, pengembangan perumahan berpagar (gated community), dan kebijakan perumahan. Dampaknya antara lain kesenjangan akses layanan publik, berkurangnya interaksi sosial antarkelompok, dan potensi kecemburuan sosial.\n\nPengecoh: sebaran jelas tidak merata. Peta menggambarkan kota, bukan perdesaan. Tidak ada informasi perpindahan keluar kota. Konurbasi adalah menyatunya beberapa kota.",
      f_segmap),
    Q("Revitalisasi sebuah kampung kota dekat pusat bisnis menarik kafe, galeri, dan penduduk berpenghasilan tinggi, sehingga harga sewa naik dan penduduk lama berpindah. Proses ini disebut …",
      ["Gentrifikasi", "Suburbanisasi", "Ruralisasi", "Segregasi alami", "Urban sprawl"],
      "Gentrifikasi adalah proses perubahan kawasan kota yang semula dihuni kelompok berpenghasilan rendah menjadi kawasan yang dihuni dan dimanfaatkan kelompok berpenghasilan lebih tinggi, biasanya setelah renovasi atau revitalisasi. Tandanya antara lain kenaikan harga lahan dan sewa, munculnya usaha baru seperti kafe dan galeri, serta perpindahan (displacement) penduduk lama yang tidak mampu membayar biaya hidup yang meningkat. Gentrifikasi dapat memperbaiki kualitas fisik kawasan, tetapi menimbulkan masalah keadilan sosial.\n\nPengecoh: suburbanisasi adalah perpindahan ke pinggiran. Ruralisasi adalah perpindahan ke desa. Segregasi adalah pemisahan kelompok, bukan proses perubahan kawasan ini. Urban sprawl adalah pemekaran kota yang menyebar.",
      None),
    Q("Perhatikan perubahan di kawasan kampung kota dekat pusat Kota G berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Gentrifikasi: sewa melonjak, penduduk asli berkurang", "Kawasan mengalami kemunduran karena harga sewa turun",
       "Penduduk asli bertambah setelah revitalisasi", "Harga sewa dan jumlah penduduk asli sama-sama meningkat", "Revitalisasi tidak berdampak terhadap kawasan"],
      "Grafik menunjukkan setelah revitalisasi dan munculnya kafe baru sekitar 2014, indeks harga sewa naik tajam dari ±120 menjadi ±330 (lebih dari tiga kali lipat dibanding 2010), sedangkan persentase penduduk asli yang bertahan turun dari ±90% menjadi ±30%. Kombinasi kenaikan biaya hidup dan tergusurnya penduduk lama adalah ciri gentrifikasi. Kebijakan untuk mengurangi dampak negatifnya antara lain pengendalian sewa, rumah terjangkau, dan pelibatan warga dalam perencanaan.\n\nPengecoh: harga sewa naik, bukan turun. Penduduk asli berkurang. Keduanya bergerak berlawanan arah. Revitalisasi jelas berdampak.",
      f_gentri),
    Q("Kawasan Kota Tua Jakarta ditata dengan mempertahankan bangunan bersejarah dan mengubah fungsinya menjadi museum, kafe, dan ruang publik. Bentuk peremajaan kota ini adalah …",
      ["Konservasi dan revitalisasi", "Redevelopment total dengan membongkar seluruh bangunan", "Urban sprawl ke pinggiran kota",
       "Relokasi seluruh kawasan ke kota lain", "Penggusuran tanpa pembangunan kembali"],
      "Peremajaan kota (urban renewal) memiliki beberapa bentuk:\n• Redevelopment: membongkar bangunan lama dan membangun yang baru dengan fungsi berbeda.\n• Rehabilitasi: memperbaiki kondisi bangunan dan lingkungan tanpa mengubah fungsi utama.\n• Konservasi (preservasi): mempertahankan bangunan dan kawasan bersejarah.\n• Revitalisasi: menghidupkan kembali kawasan yang menurun fungsinya melalui kegiatan baru.\nKota Tua Jakarta mempertahankan bangunan kolonial bersejarah (konservasi) dan menghidupkannya kembali sebagai kawasan wisata, museum, dan ruang publik (revitalisasi).\n\nPengecoh: kawasan ini tidak dibongkar total. Urban sprawl, relokasi, dan penggusuran tidak menggambarkan penataan Kota Tua.",
      None),
    Q("Perhatikan gambar penataan sebuah kawasan permukiman berikut.\n\nTeknik penataan yang digambarkan adalah …",
      ["Konsolidasi lahan oleh para pemilik lahan", "Pembebasan seluruh lahan oleh pemerintah dengan ganti rugi tunai",
       "Penggusuran warga ke luar kota tanpa pembangunan kembali", "Pembangunan jalan tol yang membelah permukiman", "Reklamasi pantai untuk perumahan baru"],
      "Gambar menunjukkan kawasan yang semula terdiri atas petak-petak tidak beraturan tanpa jalan, kemudian ditata menjadi petak yang lebih kecil dan teratur dengan jalan serta saluran. Teknik ini disebut konsolidasi lahan (land readjustment): pemilik lahan tetap memiliki tanahnya, tetapi menyumbangkan sebagian luasnya untuk jalan, saluran, dan fasilitas umum. Karena kawasan menjadi tertata dan terlayani infrastruktur, nilai lahan per meter persegi meningkat sehingga pemilik tetap diuntungkan walaupun luas petaknya berkurang. Teknik ini banyak dipakai di Jepang dan diterapkan di beberapa kota di Indonesia.\n\nPengecoh: tidak ada pembebasan seluruh lahan, penggusuran, jalan tol, atau reklamasi pada gambar.",
      f_konsolidasi),
    Q("Perumahan berpagar dengan satu gerbang berpenjaga (gated community) semakin banyak di pinggiran kota besar Indonesia. Kritik geografis utama terhadap pola ini adalah …",
      ["Memperkuat segregasi sosial dan membatasi akses ruang publik", "Menghapus seluruh kemacetan di kota", "Meningkatkan interaksi antarkelompok sosial yang berbeda",
       "Menurunkan harga lahan di sekitarnya secara drastis", "Membuat seluruh kota menjadi kawasan bebas kendaraan"],
      "Gated community menawarkan rasa aman dan lingkungan yang teratur bagi penghuninya. Namun secara spasial, pola ini memisahkan kelompok berpenghasilan tinggi dari masyarakat sekitarnya (segregasi sosial), mengubah jalan dan taman menjadi ruang privat sehingga akses publik terbatas, memutus jaringan jalan sehingga perjalanan warga sekitar menjadi lebih jauh, dan dapat menimbulkan kecemburuan sosial. Perencana kota mendorong pengembangan perumahan yang lebih terbuka dan terintegrasi dengan lingkungan sekitarnya.\n\nPengecoh: gated community tidak menghapus kemacetan; bahkan dapat menambah perjalanan memutar. Interaksi antarkelompok justru berkurang. Harga lahan sekitarnya cenderung naik. Kota tidak menjadi bebas kendaraan.",
      None),
    Q("Perhatikan sebaran dua kelompok pendapatan di Kota R berikut. Indeks disimilaritas D = ½ × Σ|aᵢ/A − bᵢ/B|.\n\nNilai indeks segregasi Kota R adalah …",
      ["0,50", "1,00", "0,25", "0,45", "0,35"],
      "Hitung selisih porsi setiap kecamatan (porsi kelompok tinggi − porsi kelompok rendah):\n• Kecamatan 1: |0,40 − 0,05| = 0,35.\n• Kecamatan 2: |0,30 − 0,15| = 0,15.\n• Kecamatan 3: |0,20 − 0,30| = 0,10.\n• Kecamatan 4: |0,10 − 0,50| = 0,40.\nΣ = 0,35 + 0,15 + 0,10 + 0,40 = 1,00 → D = ½ × 1,00 = 0,50.\nArtinya separuh penduduk salah satu kelompok perlu pindah kecamatan agar kedua kelompok tersebar merata; kelompok berpendapatan tinggi terkonsentrasi di kecamatan 1–2, sedangkan kelompok berpendapatan rendah di kecamatan 3–4.\n\nPengecoh: 1,00 lupa mengalikan ½. 0,25, 0,45, dan 0,35 berasal dari salah menghitung atau melewatkan salah satu kecamatan.",
      f_dissim),
    Q("Bekas kawasan pabrik dan gudang di tepi sungai yang terbengkalai dan tercemar diubah menjadi taman kota, perumahan, dan pusat kreatif. Lahan bekas tersebut dalam perencanaan kota disebut …",
      ["Brownfield", "Greenfield", "Greenbelt", "Urban fringe", "Central business district"],
      "Brownfield adalah lahan bekas kegiatan industri atau komersial yang terbengkalai dan sering tercemar, biasanya berada di dalam kota. Pemanfaatan kembali brownfield (setelah remediasi pencemaran) menjadi taman, perumahan, atau kawasan kreatif membantu kota tumbuh ke dalam (infill development), sehingga mengurangi tekanan konversi lahan pertanian di pinggiran.\nSebaliknya, greenfield adalah lahan yang belum pernah dibangun, misalnya sawah atau kebun di pinggiran kota. Greenbelt (sabuk hijau) adalah kawasan hijau yang membatasi perluasan kota. Urban fringe adalah zona peralihan desa–kota. CBD adalah pusat kegiatan bisnis.\n\nPengecoh: opsi lain tidak menggambarkan lahan bekas industri yang terbengkalai.",
      None),
    Q("Perhatikan kondisi kampung sebelum dan sesudah program perbaikan kampung berikut.\n\nKomponen yang mengalami peningkatan terbesar adalah …",
      ["Jalan lingkungan, naik 50 poin persen", "Akses air bersih, naik 45 poin persen", "Sanitasi layak, naik 42 poin persen",
       "Drainase berfungsi, naik 45 poin persen", "Semua komponen naik sama besar"],
      "Hitung selisih sesudah dan sebelum program:\n• Akses air bersih: 80 − 35 = 45 poin persen.\n• Jalan lingkungan diperkeras: 90 − 40 = 50 poin persen.\n• Sanitasi layak: 72 − 30 = 42 poin persen.\n• Drainase berfungsi: 70 − 25 = 45 poin persen.\nPeningkatan terbesar terjadi pada jalan lingkungan (50 poin persen). Program perbaikan kampung seperti Kampung Improvement Program (KIP) di Surabaya dan Jakarta, serta program KOTAKU, memperbaiki permukiman secara bertahap tanpa menggusur warga (in situ upgrading).\n\nPengecoh: air bersih dan drainase naik 45 poin. Sanitasi naik 42 poin. Kenaikan tidak sama besar.",
      f_kip),
    Q("Dalam kajian gentrifikasi, istilah displacement merujuk pada …",
      ["Tergusurnya penduduk lama akibat biaya hidup naik", "Bertambahnya jumlah penduduk lama di kawasan yang direvitalisasi",
       "Perpindahan pusat bisnis dari pinggiran ke pusat kota", "Pembangunan jalan baru yang memperlancar lalu lintas", "Perubahan iklim mikro di kawasan kota"],
      "Displacement adalah perpindahan atau tergusurnya penduduk lama dari suatu kawasan, baik secara langsung (misalnya penggusuran atau pengakhiran sewa) maupun tidak langsung (misalnya karena sewa, pajak, dan harga barang naik sehingga mereka tidak mampu lagi tinggal di sana). Displacement adalah dampak sosial utama gentrifikasi, yang menyebabkan hilangnya jaringan sosial, mata pencaharian, dan identitas kawasan lama.\n\nPengecoh: penduduk lama justru berkurang. Perpindahan pusat bisnis, pembangunan jalan, dan perubahan iklim mikro tidak sesuai dengan definisi displacement.",
      None),
]

P4 = [
    Q("Perhatikan gambar sebuah konsep kota ideal berikut.\n\nKonsep kota yang digambarkan adalah …",
      ["Kota taman Ebenezer Howard", "Kota kompak modern Le Corbusier", "Model zona konsentris Burgess", "Kota pintar (smart city)",
       "Model inti ganda Harris dan Ullman"],
      "Gambar menunjukkan kota berskala terbatas dengan taman dan gedung publik di pusat, kawasan permukiman, toko, dan sekolah di sekelilingnya, jalan-jalan radial, serta sabuk hijau pertanian dan hutan yang mengelilingi kota. Ini adalah konsep kota taman (garden city) yang dikemukakan Ebenezer Howard pada 1898 sebagai jawaban atas kota industri Inggris yang padat dan kotor. Konsep ini menggabungkan keunggulan kota (pekerjaan, layanan) dan desa (udara bersih, alam), serta membatasi ukuran kota dengan sabuk hijau. Konsep ini memengaruhi perencanaan banyak kota, termasuk kawasan Menteng di Jakarta.\n\nPengecoh: Le Corbusier menekankan gedung tinggi. Burgess dan Harris–Ullman adalah model deskriptif, bukan konsep ideal. Kota pintar berfokus pada teknologi.",
      f_garden),
    Q("Pembangunan berorientasi transit (transit-oriented development, TOD) menekankan …",
      ["Kawasan padat dan campuran di sekitar stasiun", "Perumahan berkepadatan rendah jauh dari stasiun angkutan umum",
       "Lahan parkir sangat luas di sekeliling stasiun", "Pemisahan tegas antara kawasan hunian dan kawasan kerja", "Jalan tol dalam kota sebagai tulang punggung transportasi"],
      "TOD adalah pendekatan perencanaan yang memusatkan pembangunan berkepadatan tinggi dengan fungsi campuran (hunian, perkantoran, perdagangan, layanan publik) dalam radius jalan kaki (sekitar 400–800 m) dari stasiun angkutan massal. Ciri lainnya adalah jalur pejalan kaki dan sepeda yang nyaman serta pembatasan parkir kendaraan pribadi. Tujuannya mendorong penggunaan angkutan umum, mengurangi kemacetan dan emisi, serta memanfaatkan lahan secara efisien. Contohnya kawasan di sekitar stasiun MRT Dukuh Atas dan Lebak Bulus di Jakarta.\n\nPengecoh: kepadatan rendah jauh dari stasiun, parkir luas, pemisahan fungsi, dan jalan tol justru mendorong ketergantungan kendaraan pribadi.",
      None),
    Q("Perhatikan zona di sekitar stasiun angkutan massal berikut.\n\nPenggunaan lahan yang paling sesuai untuk zona Q menurut prinsip TOD adalah …",
      ["Hunian vertikal, kantor, dan toko", "Lahan pertanian dan perkebunan yang luas", "Perumahan tunggal berkepadatan sangat rendah",
       "Kawasan industri berat dan gudang", "Lapangan parkir kendaraan pribadi yang sangat luas"],
      "Dalam TOD, intensitas pembangunan disusun menurun dari stasiun ke luar. Zona Q (radius ±400 m, sekitar 5 menit berjalan kaki) adalah inti TOD dengan kepadatan dan fungsi campuran tertinggi: hunian vertikal, perkantoran, pertokoan, dan fasilitas publik, sehingga sebanyak mungkin orang dapat berjalan kaki ke stasiun. Zona R (±800 m) berisi permukiman dengan kepadatan sedang dan layanan pendukung, sedangkan zona S di luarnya memiliki kepadatan lebih rendah dan dihubungkan dengan angkutan pengumpan.\n\nPengecoh: pertanian, perumahan sangat renggang, industri berat, dan parkir luas tidak sesuai dengan inti kawasan TOD.",
      f_tod),
    Q("Konsep kota kompak (compact city) dinilai lebih berkelanjutan daripada kota yang menyebar. Alasan yang paling tepat adalah …",
      ["Perjalanan lebih pendek dan angkutan umum lebih efisien", "Setiap rumah tangga memiliki lahan pekarangan yang sangat luas",
       "Kebutuhan kendaraan pribadi meningkat sehingga ekonomi tumbuh", "Kepadatan penduduk sangat rendah sehingga polusi hilang sepenuhnya",
       "Kawasan hunian dan kerja dipisahkan sejauh mungkin"],
      "Kota kompak dicirikan kepadatan relatif tinggi, penggunaan lahan campuran, dan batas perluasan kota yang jelas. Keunggulannya: jarak antara rumah, tempat kerja, dan layanan lebih pendek sehingga banyak perjalanan dapat dilakukan dengan berjalan kaki, bersepeda, atau angkutan umum; layanan angkutan umum dan infrastruktur lebih efisien karena melayani lebih banyak orang per kilometer; serta lahan pertanian dan kawasan alami di pinggiran lebih terlindungi. Tantangannya antara lain kepadatan berlebih, harga hunian tinggi, dan kebutuhan ruang hijau yang memadai.\n\nPengecoh: pekarangan sangat luas dan kepadatan sangat rendah adalah ciri kota menyebar. Kota kompak justru mengurangi kebutuhan kendaraan pribadi. Pemisahan hunian dan kerja menambah perjalanan.",
      None),
    Q("Perhatikan skor enam dimensi kota cerdas Kota C berikut.\n\nDimensi yang paling perlu diprioritaskan perbaikannya beserta contoh programnya adalah …",
      ["Smart mobility; integrasi angkutan umum", "Smart governance; layanan perizinan daring", "Smart people; pelatihan literasi digital",
       "Smart economy; pengembangan ekosistem usaha rintisan", "Smart living; peningkatan layanan kesehatan digital"],
      "Grafik menunjukkan skor terendah ada pada dimensi smart mobility (42), jauh di bawah dimensi lain yang berkisar 65–78. Dimensi ini mencakup aksesibilitas, sistem transportasi yang terintegrasi dan berkelanjutan, serta pemanfaatan teknologi informasi untuk transportasi. Program yang relevan antara lain integrasi rute dan tiket angkutan umum, sistem informasi lalu lintas dan kedatangan bus secara waktu nyata, lampu lalu lintas adaptif, serta jalur pejalan kaki dan sepeda.\n\nPengecoh: smart governance (78), smart people (72), smart economy (70), dan smart living (68) sudah relatif lebih baik, sehingga bukan prioritas utama berdasarkan data.",
      f_smart),
    Q("Konsep kota tangguh (resilient city) menekankan kemampuan kota untuk …",
      ["Bertahan, beradaptasi, dan pulih dari guncangan", "Tidak pernah mengalami bencana alam apa pun",
       "Menghindari pembangunan agar risiko bencana nol", "Memindahkan seluruh penduduk setiap kali terjadi bencana", "Menghapus semua ruang terbuka hijau"],
      "Kota tangguh adalah kota yang individu, komunitas, institusi, usaha, dan sistemnya mampu bertahan, beradaptasi, dan tumbuh kembali setelah mengalami guncangan akut (misalnya gempa, banjir, pandemi) maupun tekanan kronis (misalnya kemiskinan, kekurangan air, kemacetan). Upayanya antara lain tata ruang berbasis risiko, infrastruktur yang andal, sistem peringatan dini, perlindungan sosial, ekonomi yang beragam, dan ekosistem alami sebagai penyangga, seperti mangrove dan RTH.\n\nPengecoh: tidak ada kota yang sepenuhnya bebas bencana. Menghentikan pembangunan tidak realistis. Memindahkan seluruh penduduk bukan tujuan. RTH justru penting untuk ketangguhan.",
      None),
    Q("Perhatikan ketentuan intensitas bangunan sebuah kaveling berikut.\n\nLuas lantai dasar maksimum, jumlah lantai maksimum (dengan luas tiap lantai sama), dan luas lahan hijau minimum adalah …",
      ["500 m², 5 lantai, dan 200 m²", "500 m², 2 lantai, dan 200 m²", "250 m², 10 lantai, dan 500 m²", "500 m², 5 lantai, dan 800 m²", "2.500 m², 1 lantai, dan 200 m²"],
      "• Luas lantai dasar maksimum = KDB × luas kaveling = 50% × 1.000 = 500 m².\n• Luas total lantai maksimum = KLB × luas kaveling = 2,5 × 1.000 = 2.500 m².\n• Jumlah lantai = 2.500 ÷ 500 = 5 lantai.\n• Luas lahan hijau minimum = KDH × luas kaveling = 20% × 1.000 = 200 m².\nKDH menjamin adanya lahan resapan air dan ruang hijau di setiap kaveling.\n\nPengecoh: 2 lantai salah membaca KLB. 250 m² dan 10 lantai salah menghitung KDB. 800 m² adalah sisa lahan tanpa memperhatikan KDH. 2.500 m² adalah luas total lantai, bukan lantai dasar.",
      f_kdb),
    Q("Konsep \"kota 15 menit\" (15-minute city) yang diterapkan di Paris dan beberapa kota lain menekankan bahwa …",
      ["Kebutuhan harian terjangkau 15 menit jalan kaki atau bersepeda", "Setiap warga wajib memiliki mobil untuk mencapai pusat kota dalam 15 menit",
       "Kota hanya boleh dihuni penduduk selama 15 menit setiap hari", "Semua kantor harus berada di satu kawasan pusat bisnis", "Jalan tol harus dibangun setiap 15 kilometer"],
      "Kota 15 menit adalah konsep perencanaan yang dikembangkan Carlos Moreno, yaitu kota yang memungkinkan penduduk memenuhi sebagian besar kebutuhan sehari-hari (bekerja, belanja, sekolah, layanan kesehatan, rekreasi, dan budaya) dalam waktu 15 menit berjalan kaki atau bersepeda dari rumah. Untuk itu diperlukan lingkungan dengan penggunaan lahan campuran, kepadatan memadai, layanan yang tersebar, serta jalur pejalan kaki dan sepeda yang aman. Konsep ini mengurangi kebutuhan perjalanan jauh, kemacetan, dan emisi.\n\nPengecoh: konsep ini justru mengurangi ketergantungan mobil. Opsi lain tidak masuk akal atau bertentangan dengan prinsip penggunaan lahan campuran.",
      None),
    Q("Perhatikan komponen pengelolaan air hujan sebuah kawasan kota berikut.\n\nKonsep pengelolaan air hujan yang digambarkan adalah …",
      ["Kota spons: menahan, meresapkan, dan menampung air hujan di lokasi", "Drainase konvensional yang membuang air hujan secepat mungkin ke laut",
       "Penutupan seluruh permukaan tanah dengan beton kedap air", "Penyedotan air tanah dalam untuk mengeringkan kawasan kota", "Pembangunan tanggul laut sebagai satu-satunya solusi"],
      "Gambar menunjukkan atap hijau, taman hujan, perkerasan berpori, sumur resapan, dan kolam retensi. Semuanya adalah komponen konsep kota spons (sponge city) atau pengelolaan air hujan berkelanjutan (low impact development/sustainable urban drainage). Prinsipnya: air hujan ditahan, diresapkan, disimpan, dan dimanfaatkan sedekat mungkin dengan lokasi jatuhnya, sehingga debit puncak banjir berkurang, air tanah terisi kembali, dan kualitas air membaik.\n\nPengecoh: drainase konvensional membuang air secepatnya sehingga memindahkan banjir ke hilir. Betonisasi menambah limpasan. Penyedotan air tanah dalam menyebabkan amblesan. Tanggul laut menangani rob, bukan air hujan di kawasan.",
      f_spons),
    Q("Dokumen penataan ruang yang memuat aturan zonasi rinci untuk setiap blok, misalnya fungsi lahan, KDB, KLB, dan ketinggian bangunan, adalah …",
      ["Rencana Detail Tata Ruang (RDTR)", "Rencana Tata Ruang Wilayah Nasional", "Rencana Pembangunan Jangka Panjang Nasional", "Analisis mengenai dampak lingkungan",
       "Rencana Tata Ruang Pulau"],
      "Rencana Detail Tata Ruang (RDTR) beserta peraturan zonasinya adalah rencana rinci untuk bagian wilayah kota atau kabupaten. Isinya meliputi penetapan zona dan subzona penggunaan lahan pada tingkat blok, serta ketentuan intensitas pemanfaatan ruang seperti KDB, KLB, KDH, dan ketinggian bangunan. RDTR menjadi dasar langsung pemberian izin pemanfaatan ruang, misalnya kesesuaian kegiatan pemanfaatan ruang (KKPR) untuk pembangunan gedung.\n\nPengecoh: RTRW Nasional dan Rencana Tata Ruang Pulau bersifat umum dan berskala kecil. RPJPN adalah dokumen perencanaan pembangunan, bukan tata ruang rinci. AMDAL adalah kajian dampak lingkungan suatu rencana usaha.",
      None),
]

P5 = [
    Q("Perhatikan hierarki rencana tata ruang di Indonesia berikut.\n\nDokumen yang seharusnya mengisi tanda tanya adalah …",
      ["Rencana Detail Tata Ruang (RDTR)", "Rencana Pembangunan Jangka Menengah", "Kerangka acuan AMDAL", "Rencana strategis kementerian", "Anggaran pendapatan daerah"],
      "Rencana tata ruang di Indonesia disusun berjenjang dari yang umum ke yang rinci: RTRW Nasional → RTRW Provinsi → RTRW Kabupaten/Kota → Rencana Detail Tata Ruang (RDTR) beserta peraturan zonasi. Selain itu terdapat rencana tata ruang kawasan strategis dan rencana tata ruang pulau atau kepulauan. Setiap rencana yang lebih rinci harus mengacu pada rencana di atasnya. RDTR menjadi dasar langsung perizinan pemanfaatan ruang.\n\nPengecoh: RPJM dan rencana strategis kementerian adalah dokumen perencanaan pembangunan. Kerangka acuan AMDAL adalah dokumen lingkungan. Anggaran pendapatan daerah adalah dokumen keuangan.",
      f_hierarki),
    Q("Dalam RTRW Nasional, kota yang berfungsi melayani kegiatan berskala internasional, nasional, atau beberapa provinsi ditetapkan sebagai …",
      ["Pusat Kegiatan Nasional (PKN)", "Pusat Kegiatan Wilayah (PKW)", "Pusat Kegiatan Lokal (PKL)", "Pusat Pelayanan Lingkungan", "Kawasan perdesaan"],
      "RTRW Nasional menetapkan sistem perkotaan nasional berjenjang:\n• Pusat Kegiatan Nasional (PKN): melayani kegiatan berskala internasional, nasional, atau beberapa provinsi, misalnya Jakarta, Surabaya, Medan, dan Makassar.\n• Pusat Kegiatan Wilayah (PKW): melayani kegiatan berskala provinsi atau beberapa kabupaten/kota.\n• Pusat Kegiatan Lokal (PKL): melayani kegiatan berskala kabupaten/kota atau beberapa kecamatan.\n• Pusat Kegiatan Strategis Nasional (PKSN): kawasan perkotaan di perbatasan negara.\nPusat pelayanan lingkungan berskala lebih kecil lagi dan diatur dalam rencana daerah.\n\nPengecoh: PKW, PKL, dan pusat pelayanan lingkungan memiliki skala layanan lebih kecil. Kawasan perdesaan bukan bagian hierarki pusat kegiatan.",
      None),
    Q("Perhatikan peta lima kawasan metropolitan di Indonesia berikut.\n\nKawasan metropolitan Gerbangkertosusila ditunjukkan oleh label …",
      ["Q", "P", "R", "S", "T"],
      "Lokasi kawasan metropolitan pada peta:\n• P: Jabodetabek(punjur), berpusat di Jakarta.\n• Q: Gerbangkertosusila (Gresik, Bangkalan, Mojokerto, Surabaya, Sidoarjo, Lamongan), berpusat di Surabaya, Jawa Timur.\n• R: Mebidangro (Medan, Binjai, Deli Serdang, Karo), Sumatera Utara.\n• S: Kedungsepur (Kendal, Demak, Ungaran, Salatiga, Semarang, Purwodadi), Jawa Tengah.\n• T: Maminasata (Makassar, Maros, Sungguminasa, Takalar), Sulawesi Selatan.\nPengelolaan kawasan metropolitan memerlukan kerja sama antardaerah karena masalah transportasi, air, dan sampah melintasi batas administrasi.\n\nPengecoh: label lain menunjukkan kawasan metropolitan yang berbeda.",
      f_metro),
    Q("Menurut R. Bintarto, interaksi desa–kota dapat terjadi bila terdapat beberapa faktor. Faktor complementary region (wilayah yang saling melengkapi) berarti …",
      ["Kedua wilayah saling membutuhkan karena surplusnya berbeda", "Kedua wilayah memiliki sumber daya yang persis sama",
       "Ada wilayah lain di antara keduanya yang memenuhi kebutuhan", "Jarak kedua wilayah sangat jauh sehingga tidak dapat berhubungan", "Kedua wilayah dilarang berdagang oleh pemerintah"],
      "Edward Ullman (dan dikembangkan oleh Bintarto) menyebut tiga faktor yang memungkinkan interaksi wilayah:\n1) Wilayah yang saling melengkapi (regional complementarity): satu wilayah memiliki surplus yang dibutuhkan wilayah lain, misalnya desa menghasilkan beras dan sayur, sedangkan kota menyediakan barang industri dan jasa.\n2) Kesempatan berintervensi (intervening opportunity): adanya wilayah lain yang dapat memenuhi kebutuhan sehingga dapat melemahkan interaksi.\n3) Kemudahan perpindahan (spatial transfer ability): jarak, biaya, dan sarana transportasi yang memungkinkan pergerakan.\n\nPengecoh: sumber daya yang sama tidak menimbulkan saling membutuhkan. Opsi ketiga adalah kesempatan berintervensi. Jarak sangat jauh justru menghambat. Larangan berdagang bukan faktor interaksi.",
      None),
    Q("Perhatikan grafik ciri sosial-ekonomi sepanjang kontinum desa–kota berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Ciri desa dan kota berubah bertahap, bukan terpisah secara tegas", "Desa dan kota memiliki ciri yang sama persis",
       "Penduduk kota metropolitan lebih banyak bekerja di pertanian", "Akses internet di desa terpencil lebih tinggi daripada di kota", "Desa dekat kota tidak memiliki ciri kekotaan"],
      "Grafik menunjukkan persentase penduduk yang bekerja di pertanian turun bertahap dari desa terpencil (85%) ke desa dekat kota (55%), kota kecamatan (30%), kota sedang (10%), hingga metropolitan (2%). Sebaliknya akses internet naik bertahap dari 20% hingga 90%. Pola bertahap ini menggambarkan konsep kontinum desa–kota: tidak ada garis pemisah yang tegas antara desa dan kota, melainkan gradasi ciri sosial, ekonomi, dan fisik.\n\nPengecoh: ciri desa dan kota jelas berbeda. Penduduk metropolitan paling sedikit bekerja di pertanian. Internet di desa terpencil paling rendah. Desa dekat kota sudah memiliki sebagian ciri kekotaan.",
      f_kontinum),
    Q("Setelah pandemi, sebagian pekerja profesional pindah dari Jakarta ke kota kecil atau perdesaan di sekitar Bali dan Yogyakarta dan bekerja jarak jauh. Gejala ini paling tepat disebut …",
      ["Kontraurbanisasi", "Urbanisasi", "Gentrifikasi pusat kota", "Konurbasi", "Komuter harian"],
      "Kontraurbanisasi adalah perpindahan penduduk dari kota besar atau kawasan metropolitan ke kota kecil atau perdesaan. Pendorongnya antara lain biaya hidup tinggi, kemacetan, dan polusi di kota besar, serta penariknya adalah lingkungan yang lebih nyaman dan murah. Kemajuan teknologi informasi yang memungkinkan kerja jarak jauh membuat gejala ini semakin mungkin terjadi.\n\nPengecoh: urbanisasi adalah perpindahan ke kota. Gentrifikasi terjadi di kawasan kota yang direvitalisasi. Konurbasi adalah menyatunya beberapa kota. Komuter harian adalah perjalanan pulang-pergi setiap hari tanpa pindah tempat tinggal.",
      None),
    Q("Perhatikan diagram asal pasokan pangan sebuah kota besar berikut.\n\nPelajaran geografis yang paling tepat dari diagram tersebut adalah …",
      ["Kota bergantung pada wilayah lain untuk pangannya", "Kota besar dapat memenuhi seluruh kebutuhan pangannya sendiri",
       "Pasokan pangan kota hanya berasal dari luar negeri", "Desa tidak memiliki peran dalam memenuhi kebutuhan kota", "Jarak pasokan tidak memengaruhi harga pangan di kota"],
      "Diagram menunjukkan beras, sayur, daging, dan ikan untuk Kota J berasal dari berbagai wilayah, bahkan dari luar pulau dan luar negeri. Kota besar memiliki jejak ekologis jauh melampaui wilayah administrasinya; kota bergantung pada wilayah perdesaan dan wilayah lain untuk pangan, air, energi, dan bahan baku. Karena itu keberlanjutan kota bergantung pada kelestarian wilayah pemasok, kelancaran distribusi, dan hubungan desa–kota yang adil. Gangguan pada satu wilayah pemasok (misalnya gagal panen atau banjir) dapat menaikkan harga di kota.\n\nPengecoh: kota tidak dapat memenuhi kebutuhan pangannya sendiri. Pasokan berasal dari dalam dan luar negeri. Desa sangat berperan. Jarak memengaruhi biaya distribusi dan harga.",
      f_pasok),
    Q("Indikator berikut yang paling menunjukkan kemajuan sebuah kota menuju kota berkelanjutan (SDG 11) adalah …",
      ["Porsi angkutan umum naik dan permukiman kumuh berkurang", "Bertambahnya jumlah mobil pribadi per rumah tangga",
       "Meningkatnya volume sampah yang dibuang ke TPA terbuka", "Berkurangnya luas ruang terbuka hijau publik", "Meningkatnya pengambilan air tanah dalam"],
      "SDG 11 (Kota dan Permukiman yang Berkelanjutan) menargetkan kota yang inklusif, aman, tangguh, dan berkelanjutan. Targetnya antara lain akses perumahan layak dan pengurangan permukiman kumuh, sistem transportasi yang aman, terjangkau, dan berkelanjutan, perencanaan permukiman partisipatif, perlindungan warisan budaya, pengurangan dampak bencana, pengelolaan sampah dan kualitas udara, serta akses ruang hijau publik.\nMeningkatnya porsi perjalanan dengan angkutan umum dan berkurangnya permukiman kumuh menunjukkan kemajuan pada beberapa target sekaligus.\n\nPengecoh: bertambahnya mobil pribadi, sampah ke TPA terbuka, berkurangnya RTH, dan meningkatnya pengambilan air tanah justru menunjukkan kemunduran keberlanjutan.",
      None),
    Q("Perhatikan grafik jejak ekologis dan biokapasitas tiga kota berikut.\n\nKota dengan defisit ekologis terbesar per orang adalah …",
      ["Kota P, defisit sekitar 3,0 gha per orang", "Kota Q, defisit sekitar 1,6 gha per orang", "Kota R, defisit sekitar 0,6 gha per orang",
       "Kota R, surplus sekitar 0,6 gha per orang", "Ketiga kota memiliki defisit yang sama"],
      "Defisit ekologis = biokapasitas − jejak ekologis.\n• Kota P: 0,2 − 3,2 = −3,0 gha per orang.\n• Kota Q: 0,3 − 1,9 = −1,6 gha per orang.\n• Kota R: 0,6 − 1,2 = −0,6 gha per orang.\nKetiga kota mengalami defisit karena kota selalu membutuhkan sumber daya dari luar wilayahnya. Defisit terbesar ada di Kota P, yang memiliki konsumsi per orang tertinggi. Kebijakan yang dapat menurunkan jejak ekologis kota antara lain efisiensi energi, transportasi rendah emisi, pengurangan sampah, dan pola konsumsi berkelanjutan.\n\nPengecoh: defisit Q dan R lebih kecil. Kota R tidak surplus. Defisit ketiga kota berbeda.",
      f_jejakkota),
    Q("Ibu Kota Nusantara (IKN) dirancang dengan konsep forest city. Prinsip utama konsep tersebut adalah …",
      ["Sebagian besar wilayah tetap berupa hutan", "Seluruh hutan ditebang untuk perkantoran dan permukiman",
       "Kota dibangun tanpa jaringan transportasi umum", "Kota bergantung sepenuhnya pada energi batu bara", "Kawasan hijau hanya berupa taman kecil di atap gedung"],
      "Konsep forest city pada IKN menargetkan sebagian besar wilayah (sekitar 65–75%) dipertahankan atau dipulihkan sebagai kawasan hijau dan hutan tropis, sedangkan kawasan terbangun dibatasi. Prinsip lainnya antara lain kota yang ramah pejalan kaki dan berbasis angkutan umum, energi terbarukan, pengelolaan air berkelanjutan, dan perlindungan keanekaragaman hayati seperti habitat orang utan dan bekantan. Tantangannya adalah memastikan pembangunan benar-benar tidak merusak hutan dan menghormati hak masyarakat adat setempat.\n\nPengecoh: penebangan seluruh hutan, kota tanpa angkutan umum, dan ketergantungan pada batu bara bertentangan dengan konsep forest city. Kawasan hijau tidak hanya berupa taman atap.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
