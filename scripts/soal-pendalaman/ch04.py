from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_piramida(path):
    fig, ax = blank(8, 5, (0, 100), (0, 60))
    levels = [("Produsen (fitoplankton)", "100.000 kJ", 90), ("Konsumen I (zooplankton)", "?", 66),
              ("Konsumen II (ikan kecil)", "?", 44), ("Konsumen III (ikan besar)", "? ", 24)]
    for i, (n, v, w) in enumerate(levels):
        y = 4 + i * 13
        ax.add_patch(Rectangle((50 - w / 2, y), w, 11, fc=[C["green"], C["lgreen"], C["yellow"], C["orange"]][i], ec="black"))
        ax.text(50, y + 5.5, f"{n}: {v}", ha="center", va="center", fontsize=11, fontweight="bold")
    ax.set_title("Piramida energi ekosistem perairan (efisiensi transfer 10%)")
    save(fig, path)


def f_garis(path):
    fig, ax = indonesia_map(extent=(105, 142, -11.5, 8), w=9.5, h=5.4)
    W = [(115.7, -10), (115.9, -8.2), (117.8, -4.0), (118.9, 1.0), (120.3, 4.5), (121.3, 6.2)]
    Wb = [(126.5, -10), (127.0, -6.5), (128.6, -3.8), (127.7, -0.5), (127.2, 3.0)]
    Ly = [(130.5, -10.5), (132.8, -6.5), (131.0, -3.4), (130.3, -1.0), (130.0, 1.5)]
    for line, lab, col in [(W, "X", C["red"]), (Wb, "Y", C["purple"]), (Ly, "Z", C["blue"])]:
        ax.plot(*zip(*line), color=col, lw=2.4, ls="--")
        ax.text(line[-1][0] + 0.4, line[-1][1] + 0.4, lab, fontsize=15, fontweight="bold", color=col,
                bbox=dict(boxstyle="circle,pad=0.15", fc="white", ec=col))
    ax.set_title("Tiga garis batas persebaran fauna di Indonesia")
    save(fig, path)


def f_ddt(path):
    cats = ["Air", "Zooplankton", "Ikan kecil", "Ikan besar", "Burung pemakan ikan"]
    vals = [0.00005, 0.04, 0.5, 2.0, 25.0]
    fig, ax = new(9, 4.4)
    ax.bar(cats, vals, color=[C["lblue"], C["teal"], C["blue"], C["purple"], C["red"]])
    ax.set_yscale("log"); ax.set_ylabel("Konsentrasi DDT (ppm, skala log)")
    for i, v in enumerate(vals):
        ax.text(i, v * 1.4, ("0,00005" if v < 0.001 else f"{v:g}".replace(".", ",")), ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(1e-5, 200)
    ax.set_title("Konsentrasi DDT pada rantai makanan sebuah estuari")
    save(fig, path)


ISPU = [85, 112, 156, 210, 98, 134, 72]


def f_ispu(path):
    days = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
    fig, ax = new(9, 4.4)
    for lo, hi, c, n in [(0, 50, "#C6F6D5", "Baik"), (50, 100, "#BEE3F8", "Sedang"), (100, 200, "#FEFCBF", "Tidak sehat"),
                         (200, 300, "#FED7D7", "Sangat tidak sehat")]:
        ax.axhspan(lo, hi, color=c); ax.text(6.45, (lo + hi) / 2, n, fontsize=9, va="center", ha="right")
    ax.bar(days, ISPU, color=C["gray"], width=0.5)
    for i, v in enumerate(ISPU):
        ax.text(i, v + 4, str(v), ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 260); ax.set_ylabel("ISPU PM2,5")
    ax.set_title("ISPU harian Kota K selama satu minggu")
    save(fig, path)


def f_do(path):
    h = np.arange(0, 25)
    do = 7 + 4.2 * np.sin((h - 9) / 24 * 2 * np.pi)
    lines(h, {"Oksigen terlarut (mg/L)": do}, path, title="Oksigen terlarut di permukaan danau yang mengalami eutrofikasi",
          xlabel="Jam", ylabel="DO (mg/L)", hline=3, xticks=range(0, 25, 3), markers=False,
          annotate=lambda ax: ax.text(0.3, 3.2, "batas kritis bagi ikan ±3 mg/L", fontsize=9, color=C["gray"]))


def f_kuznets(path):
    x = np.linspace(500, 60000, 200)
    y = 80 * np.exp(-((np.log(x) - np.log(9000)) / 1.0) ** 2) + 8
    pts = {"K": 1200, "L": 9000, "M": 45000}
    fig, ax = new(8.5, 4.6)
    ax.plot(x, y, color=C["blue"], lw=2.4); ax.set_xscale("log")
    for n, v in pts.items():
        yy = 80 * np.exp(-((np.log(v) - np.log(9000)) / 1.0) ** 2) + 8
        ax.plot(v, yy, "o", ms=9, color=C["red"]); ax.text(v * 1.08, yy + 3, n, fontsize=13, fontweight="bold")
    ax.set_xlabel("Pendapatan per kapita (USD, skala log)"); ax.set_ylabel("Tingkat pencemaran udara (indeks)")
    ax.set_title("Kurva Kuznets lingkungan (ilustrasi)")
    save(fig, path)


def f_ozon(path):
    yr = np.arange(1980, 2025, 2)
    cfc = np.interp(yr, [1980, 1994, 2000, 2024], [1.0, 3.2, 3.1, 2.6])
    hole = np.interp(yr, [1980, 1990, 2000, 2006, 2015, 2024], [1, 18, 25, 26, 22, 20])
    fig, ax = new(9, 4.4)
    ax.plot(yr, cfc, color=C["red"], lw=2.2, label="Klorin efektif di stratosfer (ppb)")
    ax.set_ylabel("Klorin (ppb)", color=C["red"])
    ax2 = ax.twinx(); ax2.bar(yr, hole, color=C["lblue"], alpha=0.7, width=1.5, label="Luas lubang ozon (juta km²)")
    ax2.set_ylabel("juta km²", color=C["blue"]); ax2.spines["top"].set_visible(False)
    ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
    ax.axvline(1987, color="#718096", ls="--"); ax.text(1988, 2.75, "Protokol\nMontreal", fontsize=9)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower right", frameon=False, fontsize=9)
    ax.set_title("Klorin stratosfer dan luas lubang ozon Antartika (disederhanakan)")
    save(fig, path)


# ---- paket 1
def f_whittaker(path):
    pts = [("P", 27, 3000), ("Q", 25, 1000), ("R", 22, 150), ("S", 8, 900), ("T", -8, 250)]
    scatter(pts, path, title="Rata-rata suhu dan curah hujan tahunan lima lokasi", xlabel="Suhu rata-rata tahunan (°C)",
            ylabel="Curah hujan tahunan (mm)")


def f_karbon(path):
    fig, ax = blank(9.5, 5.2, (0, 100), (0, 60))
    box(ax, 38, 47, 24, 9, "ATMOSFER\n±870 GtC", fc="#EBF8FF")
    box(ax, 4, 22, 24, 9, "Vegetasi & tanah\n±2.000 GtC", fc="#C6F6D5")
    box(ax, 72, 22, 24, 9, "Laut\n±38.000 GtC", fc="#BEE3F8")
    box(ax, 38, 3, 24, 9, "Bahan bakar fosil\n±1.000 GtC", fc="#E2E8F0")
    arrow(ax, 22, 32, 39, 47, color=C["green"]); ax.text(22, 40, "P", fontsize=14, fontweight="bold")
    arrow(ax, 42, 46, 25, 32, color=C["orange"]); ax.text(35, 36, "Q", fontsize=14, fontweight="bold")
    arrow(ax, 50, 13, 50, 46, color=C["red"]); ax.text(52, 28, "R", fontsize=14, fontweight="bold")
    arrow(ax, 61, 47, 78, 32, color=C["blue"]); arrow(ax, 82, 32, 64, 50, color=C["blue"]); ax.text(76, 42, "S", fontsize=14, fontweight="bold")
    ax.set_title("Siklus karbon global (cadangan dalam gigaton karbon)")
    save(fig, path)


def f_peltier(path):
    fig, ax = new(8, 5)
    ax.add_patch(Rectangle((18, 1500), 12, 2500, fc="#FBD38D", alpha=0.7)); ax.text(24, 3000, "pelapukan kimia\nkuat", ha="center", fontsize=10)
    ax.add_patch(Rectangle((-15, 300), 20, 1200, fc="#BEE3F8", alpha=0.7)); ax.text(-5, 1100, "pelapukan mekanis\n(beku-cair) kuat", ha="center", fontsize=10)
    ax.add_patch(Rectangle((5, 0), 25, 250, fc="#E2E8F0", alpha=0.9)); ax.text(17, 120, "pelapukan sangat lemah", ha="center", fontsize=9)
    for n, t, p in [("X", 26, 2500), ("Y", -5, 600), ("Z", 25, 150), ("W", 12, 1200)]:
        ax.plot(t, p, "o", ms=9, color=C["red"]); ax.text(t + 0.6, p + 80, n, fontsize=13, fontweight="bold")
    ax.set_xlim(-15, 30); ax.set_ylim(0, 4000); ax.set_xlabel("Suhu rata-rata tahunan (°C)"); ax.set_ylabel("Curah hujan tahunan (mm)")
    ax.set_title("Diagram Peltier (disederhanakan)")
    save(fig, path)


def f_horizon(path):
    fig, ax = blank(6.5, 6, (0, 60), (0, 70))
    hs = [("K", 64, 70, "#3E2723", "serasah & humus"), ("L", 54, 64, "#6D4C41", "mineral kaya bahan organik"),
          ("M", 46, 54, "#D7CCC8", "zona pencucian (eluviasi)"), ("N", 30, 46, "#A1887F", "zona penimbunan lempung, Fe, Al"),
          ("O", 14, 30, "#BCAAA4", "bahan induk lapuk"), ("P", 0, 14, "#757575", "batuan dasar")]
    for n, y0, y1, c, d in hs:
        ax.add_patch(Rectangle((5, y0), 22, y1 - y0, fc=c, ec="black"))
        ax.text(2.5, (y0 + y1) / 2, n, fontsize=14, fontweight="bold", va="center")
        ax.text(30, (y0 + y1) / 2, d, fontsize=10, va="center")
    ax.set_title("Profil tanah lengkap")
    save(fig, path)


def f_suksesi(path):
    fig, ax = blank(10, 3.6, (0, 100), (0, 34))
    st = ["Lumut kerak\n(liken)", "Rumput &\nherba", "Semak", "Pohon\npionir", "Hutan\nklimaks"]
    for i, s in enumerate(st):
        box(ax, 2 + i * 20, 10, 15, 14, s, fc=["#E2E8F0", "#C6F6D5", "#9AE6B4", "#68D391", "#2F855A"][i], fs=10,
            tc="white" if i == 4 else "#1A202C")
        ax.text(9.5 + i * 20, 27, str(i + 1), ha="center", fontsize=14, fontweight="bold", color=C["blue"])
        if i < 4:
            arrow(ax, 17.5 + i * 20, 17, 21.5 + i * 20, 17)
    ax.text(50, 3, "waktu (ratusan tahun) →", ha="center", fontsize=10)
    ax.set_title("Tahapan suksesi di lahan batuan lava yang baru membeku")
    save(fig, path)


# ---- paket 2
def f_endemik(path):
    bars(["Sulawesi", "Papua", "Jawa", "Kalimantan", "Sumatra"], {"Mamalia endemik (%)": [62, 58, 12, 18, 10]}, path,
         title="Persentase spesies mamalia darat yang endemik di tiap pulau (ilustrasi)", ylabel="%", values=True,
         ylim=(0, 75), colors=[C["green"]], w=8)


def f_iucn(path):
    table([["A", "85%", "10 tahun"], ["B", "55%", "10 tahun"], ["C", "35%", "10 tahun"], ["D", "10%", "10 tahun"]],
          ["Spesies", "Penurunan populasi", "Periode (≈ 3 generasi)"], path,
          title="Penurunan populasi empat spesies (kriteria A IUCN)", col_w=[0.2, 0.4, 0.4])


def f_fragmen(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    rnd = np.random.RandomState(2)
    for a in axs:
        a.set_xlim(0, 100); a.set_ylim(0, 100); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
        a.add_patch(Rectangle((0, 0), 100, 100, fc="#F6E05E", alpha=0.35))
    axs[0].add_patch(Rectangle((8, 8), 84, 84, fc=C["green"])); axs[0].set_title("Tahun 1990: hutan utuh")
    for (x, y, w, h) in [(5, 60, 22, 30), (40, 70, 15, 12), (70, 55, 24, 35), (12, 10, 30, 25), (60, 8, 14, 14), (45, 35, 10, 10)]:
        axs[1].add_patch(Rectangle((x, y), w, h, fc=C["green"]))
    axs[1].plot([0, 100], [48, 48], color="#4A5568", lw=4); axs[1].text(2, 50, "jalan", fontsize=9)
    axs[1].set_title("Tahun 2020: hutan terfragmentasi")
    fig.suptitle("Perubahan bentang hutan (hijau) di antara lahan pertanian (kuning)", fontweight="bold")
    save(fig, path)


def f_lintang(path):
    lat = [0, 10, 20, 30, 40, 50, 60, 70]
    lines(lat, {"Jumlah spesies burung per 10.000 km²": [600, 520, 400, 300, 220, 150, 90, 40]}, path,
          title="Kekayaan spesies burung menurut lintang (ilustrasi)", xlabel="Lintang (derajat dari ekuator)",
          ylabel="jumlah spesies", w=8)


def f_badak(path):
    bars(["1967", "1980", "1993", "2000", "2013", "2023"], {"Individu": [25, 60, 47, 50, 58, 76]}, path,
         title="Perkiraan populasi badak jawa di Taman Nasional Ujung Kulon", ylabel="individu", values=True, ylim=(0, 90),
         colors=[C["gray"]], w=8)


# ---- paket 3
def f_sag(path):
    km = [0, 2, 4, 6, 8, 10, 15, 20]
    do = [7.8, 5.2, 3.6, 2.4, 3.1, 4.4, 6.2, 7.3]
    fig, ax = new(9, 4.4)
    ax.plot(km, do, marker="o", lw=2.4, color=C["blue"])
    for n, k, d in [("A", 2, 5.2), ("B", 4, 3.6), ("C", 6, 2.4), ("D", 10, 4.4), ("E", 20, 7.3)]:
        ax.text(k, d + 0.35, n, ha="center", fontsize=13, fontweight="bold")
    ax.axvline(0, color=C["red"], ls="--"); ax.text(0.2, 8.4, "titik pembuangan limbah organik", fontsize=9, color=C["red"])
    ax.axhline(4, color="#718096", ls=":", lw=1); ax.text(15.5, 3.6, "baku mutu DO 4 mg/L", fontsize=9)
    ax.set_xlabel("Jarak ke hilir (km)"); ax.set_ylabel("Oksigen terlarut (mg/L)"); ax.set_ylim(0, 9.2)
    ax.set_title("Profil oksigen terlarut Sungai S")
    save(fig, path)


def f_ph(path):
    bars(["Sampel K", "Sampel L", "Sampel M", "Sampel N"], {"pH": [4.2, 6.8, 7.5, 5.8]}, path,
         title="pH air hujan di empat lokasi pengamatan", ylabel="pH", values=True, ylim=(0, 9), hline=5.6,
         colors=[C["teal"]], w=7.5)


def f_ispu3(path):
    table([["Kota X", "165", "90", "60", "40"], ["Kota Y", "95", "120", "45", "30"], ["Kota Z", "48", "40", "35", "20"]],
          ["Kota", "PM2,5", "PM10", "O₃", "CO"], path, title="Nilai subindeks ISPU tiap parameter pada hari yang sama",
          col_w=[0.24, 0.19, 0.19, 0.19, 0.19])


def f_plume(path):
    fig, ax = blank(9, 5, (0, 100), (0, 60))
    ax.add_patch(Rectangle((0, 0), 100, 60, fc="#FFF5E1"))
    ax.add_patch(Ellipse((52, 30), 44, 16, fc="#FED7D7", ec=C["red"], alpha=0.8))
    ax.add_patch(Rectangle((28, 27), 6, 6, fc="#744210")); ax.text(31, 36, "tangki septik", ha="center", fontsize=10)
    for i in range(4):
        arrow(ax, 8, 50 - i * 12, 22, 50 - i * 12, color=C["blue"], lw=1.6)
    ax.text(3, 56, "arah aliran air tanah →", fontsize=10, color=C["blue"])
    for n, (x, y) in {"W1": (14, 30), "W2": (50, 30), "W3": (90, 30), "W4": (50, 52)}.items():
        ax.plot(x, y, "o", ms=10, color="#2D3748"); ax.text(x + 1.5, y + 2, n, fontsize=12, fontweight="bold")
    ax.set_title("Denah permukiman dan sebaran rembesan limbah (merah)")
    save(fig, path)


def f_pm(path):
    bars(["Kendaraan bermotor", "Industri & pembangkit", "Debu jalan & konstruksi", "Pembakaran terbuka", "Lain-lain"],
         {"Kontribusi (%)": [46, 22, 13, 9, 10]}, path, title="Sumber PM2,5 di Kota M (ilustrasi)", ylabel="%", values=True,
         ylim=(0, 55), colors=[C["gray"]], rot=15, w=9)


# ---- paket 4
def f_sampah(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [40, 18, 11, 8, 6, 17]; lab = ["Sisa makanan & organik", "Plastik", "Kertas", "Kayu & ranting", "Logam & kaca", "Lainnya"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=[C["green"], C["red"], C["yellow"], C["brown"], C["gray"], C["lgray"]],
           startangle=90, wedgeprops=dict(ec="white"), textprops=dict(fontsize=10))
    ax.set_title("Komposisi sampah Kota R")
    save(fig, path)


def f_gyre(path):
    fig, ax = world_map(w=10, h=5)
    for (cx, cy, rx, ry, cw) in [(-150, 30, 40, 13, True), (-40, 30, 22, 11, True), (-110, -30, 40, 13, False), (-15, -28, 18, 10, False), (80, -28, 25, 11, False)]:
        t = np.linspace(0, 2 * np.pi, 60) * (-1 if cw else 1)
        ax.plot(cx + rx * np.cos(t), cy + ry * np.sin(t), color=C["blue"], lw=1.6)
        ax.annotate("", xy=(cx + rx * np.cos(t[12]), cy + ry * np.sin(t[12])), xytext=(cx + rx * np.cos(t[10]), cy + ry * np.sin(t[10])),
                    arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.6))
    for n, (x, y) in {"P": (-145, 31), "Q": (-150, 2), "R": (100, -5), "S": (-60, -58), "T": (170, 72)}.items():
        ax.plot(x, y, "o", ms=8, color=C["red"]); ax.text(x + 3, y + 3, n, fontsize=13, fontweight="bold", color=C["red"])
    ax.set_title("Arus permukaan berputar (gyre) di samudra dunia")
    save(fig, path)


def f_pesisir(path):
    fig, ax = blank(10, 4, (0, 100), (0, 36))
    x = np.linspace(0, 100, 200); bed = 22 - 0.15 * x + 3 * np.exp(-((x - 80) / 6) ** 2)
    ax.fill_between(x, 0, bed, color="#E9D8A6"); ax.fill_between(x, bed, 22, where=x > 20, color=C["lblue"], alpha=0.8)
    for xx in np.arange(4, 20, 3):
        ax.plot([xx, xx], [22, 30], color="#5D4037", lw=2); ax.add_patch(Circle((xx, 31), 2.2, fc="#2F855A"))
    for xx in np.arange(40, 66, 2):
        ax.plot([xx, xx + 0.5], [22 - 0.15 * xx, 24 - 0.15 * xx + 1.5], color="#38A169", lw=1.5)
    for xx in np.arange(76, 86, 2.5):
        ax.add_patch(Circle((xx, 22 - 0.15 * xx + 4), 1.3, fc="#F687B3"))
    for t, xx in [("X", 11), ("Y", 52), ("Z", 81)]:
        ax.text(xx, 34.5, t, fontsize=15, fontweight="bold", ha="center", color=C["blue"])
    ax.text(97, 23, "laut lepas →", ha="right", fontsize=9)
    ax.set_title("Penampang zonasi ekosistem pesisir tropis")
    save(fig, path)


def f_dhw(path):
    w = np.arange(1, 27)
    dhw = np.clip(np.interp(w, [1, 6, 10, 14, 17, 20, 23, 26], [0, 0.5, 2.5, 5.5, 9.0, 8.0, 3.0, 0.5]), 0, None)
    fig, ax = new(9, 4.2)
    ax.axhspan(4, 8, color="#FEFCBF"); ax.axhspan(8, 12, color="#FED7D7")
    ax.plot(w, dhw, color=C["red"], lw=2.4, marker="o", ms=4)
    ax.text(1, 5.7, "≥ 4: pemutihan karang signifikan", fontsize=9); ax.text(1, 9.7, "≥ 8: pemutihan luas & kematian karang", fontsize=9)
    ax.set_xlabel("Minggu ke-"); ax.set_ylabel("Degree Heating Weeks (°C-minggu)"); ax.set_ylim(0, 12)
    ax.set_title("Akumulasi tekanan panas di terumbu karang Perairan T")
    save(fig, path)


def f_limpasan(path):
    table([["Luas kawasan", "50 ha"], ["Hujan rencana", "100 mm"], ["C sebelum (kebun & sawah)", "0,30"], ["C sesudah (perumahan)", "0,80"]],
          ["Parameter", "Nilai"], path, title="Rencana alih fungsi lahan menjadi perumahan", col_w=[0.6, 0.4])


# ---- paket 5
PB = {"Perubahan iklim": 1.7, "Integritas biosfer": 10, "Aliran nitrogen–fosfor": 2.5, "Perubahan sistem lahan": 1.3,
      "Air tawar": 1.1, "Penipisan ozon stratosfer": 0.5}


def f_planet(path):
    fig, ax = new(9, 4.6)
    v = list(PB.values())
    ax.barh(list(PB), v, color=[C["red"] if x > 1 else C["green"] for x in v]); ax.invert_yaxis()
    ax.axvline(1, color="black", ls="--"); ax.text(1.05, 5.45, "batas aman", fontsize=9)
    ax.set_xscale("log"); ax.set_xlabel("Status terhadap batas aman (1 = tepat di batas, skala log)")
    ax.set_title("Status beberapa batas planet (ilustrasi)")
    save(fig, path)


def f_malthus(path):
    t = np.arange(0, 9)
    lines([f"{25 * i}" for i in t], {"Garis X": [2 ** i for i in t], "Garis Y": [1 + i for i in t]}, path,
          title="Model pertumbuhan menurut Malthus", xlabel="Tahun ke-", ylabel="Indeks (awal = 1)", w=8)


def f_jejak_eko(path):
    bars(["Negara A", "Negara B", "Negara C", "Negara D"], {"Jejak ekologis": [4.5, 6.0, 1.7, 2.5], "Biokapasitas": [10.0, 2.0, 1.1, 2.5]},
         path, title="Jejak ekologis dan biokapasitas per kapita (gha/orang)", ylabel="gha per orang", values=True, ylim=(0, 11.5), w=8.5)


def f_akselerasi(path):
    yr = np.arange(1850, 2021, 10)
    pop = np.interp(yr, [1850, 1900, 1950, 2000, 2020], [1.2, 1.6, 2.5, 6.1, 7.8]) / 7.8 * 100
    co2 = np.interp(yr, [1850, 1900, 1950, 2000, 2020], [285, 296, 311, 370, 413]); co2 = (co2 - 280) / (413 - 280) * 100
    fert = np.interp(yr, [1850, 1900, 1950, 1970, 2000, 2020], [0, 0.5, 4, 35, 75, 100])
    lines(yr, {"Penduduk": pop, "CO₂ atmosfer": co2, "Pemakaian pupuk": fert}, path, title="Beberapa indikator aktivitas manusia (indeks, 2020 = 100)",
          xlabel="Tahun", ylabel="indeks", markers=False, w=9,
          annotate=lambda ax: ax.axvline(1950, color="#718096", ls="--"))


def f_amdal(path):
    fig, ax = blank(10, 3, (0, 100), (0, 24))
    items = ["Penapisan\n(wajib AMDAL?)", "Kerangka\nAcuan (KA)", "ANDAL", "?", "Persetujuan\nLingkungan"]
    for i, t in enumerate(items):
        box(ax, 1 + i * 20, 6, 16, 12, t, fc="#FEFCBF" if t == "?" else "#EBF8FF", fs=10 if t != "?" else 22, bold=t == "?")
        if i < 4:
            arrow(ax, 17.6 + i * 20, 12, 20.6 + i * 20, 12)
    ax.set_title("Alur penyusunan dokumen AMDAL")
    save(fig, path)


# ============================ questions ============================
P0 = [
    Q("Perhatikan piramida energi ekosistem perairan berikut. Jika efisiensi transfer energi antartingkat trofik 10%, energi yang tersedia bagi konsumen III adalah …",
      ["100 kJ", "1.000 kJ", "10.000 kJ", "10 kJ", "30.000 kJ"],
      "Menurut aturan 10% Lindeman, hanya sekitar 10% energi pada satu tingkat trofik yang berpindah ke tingkat berikutnya; sisanya hilang sebagai panas respirasi, tidak dimakan, atau tidak tercerna.\n• Produsen: 100.000 kJ.\n• Konsumen I: 10% × 100.000 = 10.000 kJ.\n• Konsumen II: 10% × 10.000 = 1.000 kJ.\n• Konsumen III: 10% × 1.000 = 100 kJ.\nAtau langsung 100.000 × 0,1³ = 100 kJ.\n\nPengecoh: 10.000 dan 1.000 kJ adalah energi konsumen I dan II. 10 kJ adalah energi konsumen IV. 30.000 kJ keliru menjumlahkan 10% tiga kali dari produsen. Inilah alasan rantai makanan jarang lebih dari 4–5 tingkat dan konsumen puncak jumlahnya sedikit.",
      f_piramida),
    Q("Perhatikan peta tiga garis batas persebaran fauna berikut.\n\nGaris yang memisahkan fauna tipe Asia (Oriental) dari fauna peralihan di Sulawesi dan Nusa Tenggara adalah …",
      ["X, garis Wallace", "Y, garis Weber", "Z, garis Lydekker", "X, garis Lydekker", "Y, garis Wallace"],
      "Garis X yang melintasi Selat Lombok (antara Bali dan Lombok) dan Selat Makassar (antara Kalimantan dan Sulawesi) adalah garis Wallace. Di sebelah baratnya terdapat fauna tipe Asia, misalnya harimau, gajah, orang utan, dan badak. Paparan Sunda di barat pernah menyatu dengan Asia saat muka laut rendah, sedangkan Selat Lombok dan Selat Makassar tetap dalam sehingga menjadi penghalang.\nGaris Y (Weber) adalah garis keseimbangan antara fauna Asia dan Australia, sedangkan garis Z (Lydekker) membatasi tepi Paparan Sahul, tempat fauna tipe Australia seperti kanguru pohon dan cendrawasih. Wilayah antara garis Wallace dan Lydekker disebut Wallacea (fauna peralihan, misalnya anoa, babirusa, komodo).\n\nPengecoh: opsi lain menukar nama garis.",
      f_garis),
    Q("Menurut persamaan IPAT (I = P × A × T), jika jumlah penduduk (P) menjadi dua kali lipat dan konsumsi per kapita (A) naik 1,5 kali, faktor teknologi (T) harus berubah agar dampak lingkungan (I) tetap. Besar perubahan T adalah …",
      ["Turun sekitar 67%", "Turun sekitar 33%", "Turun sekitar 50%", "Naik sekitar 300%", "Turun sekitar 75%"],
      "Agar I tetap, perkalian P × A × T harus sama dengan semula.\nP baru × A baru = 2 × 1,5 = 3 kali semula, sehingga T baru = 1/3 dari T semula ≈ 0,333.\nPenurunan T = 1 − 0,333 = 0,667 ≈ 67%.\nArtinya teknologi harus tiga kali lebih bersih atau efisien (dampak per unit konsumsi tinggal sepertiga) agar dampak total tidak bertambah.\n\nPengecoh: 33% adalah nilai T yang tersisa, bukan penurunannya. 50% hanya mengimbangi kenaikan penduduk. 300% salah arah. 75% tidak sesuai perhitungan. Persamaan IPAT menunjukkan bahwa dampak lingkungan dipengaruhi bersama oleh jumlah penduduk, tingkat konsumsi, dan teknologi.",
      None),
    Q("Perhatikan grafik konsentrasi DDT pada rantai makanan sebuah estuari berikut.\n\nFaktor biomagnifikasi dari ikan kecil ke burung pemakan ikan adalah …",
      ["50 kali", "12,5 kali", "625 kali", "25 kali", "500.000 kali"],
      "Faktor biomagnifikasi = konsentrasi pada tingkat trofik atas ÷ konsentrasi pada tingkat trofik bawah.\nIkan kecil = 0,5 ppm; burung = 25 ppm. Faktor = 25 ÷ 0,5 = 50 kali.\nBiomagnifikasi terjadi karena DDT larut dalam lemak, tidak mudah terurai, dan tidak mudah dikeluarkan tubuh. Setiap tingkat trofik memakan banyak individu mangsa, sehingga zat menumpuk semakin tinggi. Pada burung, DDT menyebabkan cangkang telur tipis dan populasi menurun.\n\nPengecoh: 12,5 kali adalah faktor ikan besar ke burung (25 ÷ 2). 625 kali adalah faktor zooplankton ke burung (25 ÷ 0,04). 25 kali menganggap nilai burung sebagai faktornya. 500.000 kali adalah faktor dari air ke burung.",
      f_ddt),
    Q("Setelah letusan dahsyat tahun 1883, Pulau Rakata (Krakatau) tertutup endapan piroklastik panas yang mematikan seluruh kehidupan. Kehidupan kemudian kembali secara bertahap. Proses ini merupakan …",
      ["Suksesi primer, karena dimulai pada substrat baru tanpa tanah dan kehidupan sebelumnya",
       "Suksesi sekunder, karena tanah dan bank biji di pulau tersebut masih tersisa utuh",
       "Suksesi sekunder, karena kehidupan kembali dengan cepat dalam beberapa bulan",
       "Suksesi primer, karena pulau tersebut berada di daerah beriklim subtropis",
       "Bukan suksesi, karena tumbuhan baru berasal dari pulau lain di sekitarnya"],
      "Suksesi primer terjadi pada substrat baru yang belum pernah ditumbuhi kehidupan atau seluruh tanah dan kehidupannya hilang, misalnya lava yang membeku, endapan piroklastik tebal, atau gumuk pasir baru. Pada Rakata, organisme pionier seperti lumut kerak, alga biru-hijau, dan paku-pakuan datang dari luar pulau (terbawa angin, laut, dan burung), lalu secara bertahap diikuti rumput, semak, dan hutan.\nSuksesi sekunder terjadi pada lahan yang terganggu tetapi tanah dan sebagian kehidupannya masih tersisa, misalnya bekas ladang atau hutan terbakar.\n\nPengecoh: tanah dan bank biji Rakata hilang tertutup piroklastik. Suksesi di Rakata berlangsung puluhan tahun, bukan beberapa bulan. Rakata beriklim tropis. Kedatangan organisme dari pulau lain justru bagian dari proses suksesi primer.",
      None),
    Q("Perhatikan grafik ISPU PM2,5 harian Kota K berikut. Kategori: 0–50 baik; 51–100 sedang; 101–200 tidak sehat; 201–300 sangat tidak sehat.\n\nJumlah hari dengan kualitas udara minimal \"tidak sehat\" adalah …",
      ["4 hari", "3 hari", "1 hari", "5 hari", "2 hari"],
      "Baca nilai ISPU: Senin 85 (sedang), Selasa 112 (tidak sehat), Rabu 156 (tidak sehat), Kamis 210 (sangat tidak sehat), Jumat 98 (sedang), Sabtu 134 (tidak sehat), Minggu 72 (sedang).\nHari dengan kategori minimal tidak sehat (ISPU ≥ 101): Selasa, Rabu, Kamis, dan Sabtu = 4 hari.\n\nPengecoh: 3 hari tidak menghitung Kamis karena kategorinya \"sangat tidak sehat\", padahal soal meminta \"minimal tidak sehat\" (termasuk kategori yang lebih buruk). 1 hari hanya menghitung Kamis. 5 hari keliru memasukkan Jumat (98). Pada hari tidak sehat, kelompok sensitif seperti anak-anak, lansia, dan penderita asma disarankan mengurangi aktivitas di luar ruangan.",
      f_ispu),
    Q("Perhatikan grafik oksigen terlarut (DO) di permukaan danau yang mengalami eutrofikasi berikut.\n\nWaktu ketika risiko kematian massal ikan paling tinggi beserta penyebabnya adalah …",
      ["Menjelang pagi, karena semalaman alga dan bakteri hanya berespirasi tanpa fotosintesis",
       "Siang hari, karena fotosintesis alga menghabiskan seluruh oksigen di dalam air",
       "Sore hari, karena suhu air paling tinggi sehingga oksigen bertambah banyak",
       "Tengah malam, karena fotosintesis alga mencapai puncaknya pada saat gelap",
       "Sepanjang hari sama saja, karena DO di danau tidak berubah menurut waktu"],
      "Eutrofikasi adalah pengayaan nutrien (nitrogen dan fosfor dari pupuk, limbah, atau pakan keramba) yang memicu ledakan alga. Pada siang hari, alga berfotosintesis sehingga DO naik (puncak ±11 mg/L sekitar pukul 15.00). Pada malam hari, alga, bakteri pengurai, dan ikan hanya berespirasi, sehingga DO terus turun dan mencapai minimum menjelang pagi (±2,8 mg/L sekitar pukul 03.00), di bawah batas kritis ±3 mg/L. Itulah sebabnya kematian massal ikan keramba di Danau Toba atau Maninjau sering ditemukan pada pagi hari.\n\nPengecoh: fotosintesis menghasilkan, bukan menghabiskan, oksigen. Suhu tinggi justru menurunkan kelarutan oksigen. Fotosintesis tidak terjadi dalam gelap. Grafik jelas menunjukkan DO berubah menurut waktu.",
      f_do),
    Q("Sebuah kota seluas 120 km² memiliki RTH publik 14 km² dan RTH privat 9 km². Menurut ketentuan RTH minimal 30% (20% publik dan 10% privat), kekurangan RTH publik kota tersebut adalah …",
      ["10 km²", "13 km²", "24 km²", "3 km²", "36 km²"],
      "Kebutuhan RTH publik = 20% × 120 km² = 24 km². RTH publik yang tersedia 14 km², sehingga kekurangannya 24 − 14 = 10 km².\nSebagai pembanding, kebutuhan RTH privat = 10% × 120 = 12 km², tersedia 9 km² (kurang 3 km²). Total RTH = 23 km² atau ±19,2%, masih di bawah 30%.\n\nPengecoh: 13 km² adalah kekurangan total RTH (36 − 23). 24 km² adalah kebutuhan RTH publik, bukan kekurangannya. 3 km² adalah kekurangan RTH privat. 36 km² adalah kebutuhan RTH total. RTH berperan menurunkan suhu kota, meresapkan air hujan, dan menyerap polutan.",
      None),
    Q("Perhatikan kurva Kuznets lingkungan berikut.\n\nPernyataan yang paling tepat tentang negara L berdasarkan kurva tersebut adalah …",
      ["Berada di puncak kurva; pencemaran tertinggi saat industrialisasi pesat", "Berada di tahap awal; pencemaran rendah karena ekonomi masih agraris",
       "Berada di tahap akhir; pencemaran menurun karena teknologi bersih", "Tidak akan pernah mengalami penurunan pencemaran sama sekali",
       "Memiliki pendapatan tertinggi sehingga pencemarannya paling rendah"],
      "Kurva Kuznets lingkungan berbentuk U terbalik. Pada tahap awal pembangunan (K), pencemaran rendah karena ekonomi masih agraris. Saat industrialisasi pesat (L, di puncak kurva), pencemaran mencapai titik tertinggi karena pertumbuhan diutamakan dan teknologi belum bersih. Pada tahap lanjut (M), pendapatan tinggi mendorong tuntutan lingkungan bersih, regulasi ketat, teknologi bersih, dan pergeseran ke ekonomi jasa, sehingga pencemaran menurun.\n\nPengecoh: tahap awal adalah K dan tahap akhir adalah M. Kurva justru memprediksi penurunan setelah puncak. Negara L bukan yang berpendapatan tertinggi. Kritik terhadap kurva ini: beberapa pencemar (misalnya CO₂) tidak selalu menurun, dan negara maju dapat \"memindahkan\" industri kotor ke negara berkembang.",
      f_kuznets),
    Q("Perhatikan grafik klorin efektif di stratosfer dan luas lubang ozon Antartika berikut.\n\nPenjelasan yang paling tepat mengenai luas lubang ozon yang belum kembali ke kondisi 1980 walaupun Protokol Montreal telah berlaku sejak 1987 adalah …",
      ["CFC berumur panjang di atmosfer sehingga klorin di stratosfer turun sangat lambat", "Protokol Montreal gagal karena produksi CFC dunia terus meningkat hingga kini",
       "Lubang ozon disebabkan karbon dioksida sehingga CFC tidak berpengaruh", "Lubang ozon semakin luas setiap tahun karena klorin terus bertambah",
       "Lubang ozon hanya dipengaruhi letusan gunung api, bukan aktivitas manusia"],
      "Grafik menunjukkan klorin efektif di stratosfer memuncak sekitar pertengahan 1990-an, lalu turun perlahan setelah produksi CFC dihentikan melalui Protokol Montreal. Namun CFC memiliki umur atmosfer puluhan hingga lebih dari seratus tahun, sehingga klorin yang sudah terlepas masih merusak ozon selama bertahun-tahun. Luas lubang ozon pun stabil lalu mulai mengecil secara perlahan, dan diperkirakan pulih ke kondisi 1980 sekitar pertengahan abad ke-21.\n\nPengecoh: Protokol Montreal justru dianggap perjanjian lingkungan paling berhasil; produksi CFC turun drastis. CO₂ bukan penyebab utama lubang ozon. Klorin turun, bukan bertambah. Aerosol letusan gunung api dapat memengaruhi sementara, tetapi penyebab utamanya CFC buatan manusia.",
      f_ozon),
]

P1 = [
    Q("Perhatikan grafik suhu dan curah hujan tahunan lima lokasi berikut.\n\nLokasi yang paling mungkin memiliki bioma sabana adalah …",
      ["Q", "P", "R", "S", "T"],
      "Bioma terutama dikendalikan oleh suhu dan curah hujan (diagram Whittaker):\n• P (27 °C, 3.000 mm): hutan hujan tropis.\n• Q (25 °C, 1.000 mm): sabana tropis; suhu tinggi dengan hujan sedang dan musim kering nyata, sehingga didominasi rumput dengan pohon tersebar, misalnya di NTT.\n• R (22 °C, 150 mm): gurun panas.\n• S (8 °C, 900 mm): hutan gugur beriklim sedang.\n• T (−8 °C, 250 mm): tundra.\nJadi lokasi sabana adalah Q.\n\nPengecoh: P terlalu basah untuk sabana. R terlalu kering. S dan T terlalu dingin.",
      f_whittaker),
    Q("Sebuah ekosistem padang rumput memiliki produktivitas produsen 2.000.000 kkal. Dengan efisiensi transfer 10%, energi yang dapat dimanfaatkan konsumen III (karnivora puncak) adalah …",
      ["2.000 kkal", "20.000 kkal", "200.000 kkal", "200 kkal", "600.000 kkal"],
      "Konsumen III berada tiga tingkat di atas produsen.\nEnergi = 2.000.000 × 0,1 × 0,1 × 0,1 = 2.000.000 × 0,001 = 2.000 kkal.\nUrutannya: produsen 2.000.000 → konsumen I (herbivora) 200.000 → konsumen II 20.000 → konsumen III 2.000 kkal.\n\nPengecoh: 200.000 dan 20.000 kkal adalah energi konsumen I dan II. 200 kkal adalah konsumen IV. 600.000 kkal keliru menjumlahkan tiga kali 10%. Konsekuensi geografisnya: pola makan berbasis tumbuhan dapat memberi makan lebih banyak orang dari luas lahan yang sama dibandingkan pola makan berbasis daging.",
      None),
    Q("Perhatikan diagram siklus karbon global berikut.\n\nAliran karbon yang merupakan tambahan akibat aktivitas manusia dan menjadi penyebab utama kenaikan CO₂ atmosfer adalah …",
      ["R, pembakaran bahan bakar fosil", "P, fotosintesis vegetasi daratan", "Q, respirasi dan dekomposisi",
       "S, pertukaran CO₂ antara laut dan atmosfer", "P dan Q yang saling mengimbangi"],
      "Pada diagram: P adalah penyerapan CO₂ oleh fotosintesis, Q adalah pelepasan CO₂ melalui respirasi dan dekomposisi, S adalah pertukaran dua arah antara laut dan atmosfer, dan R adalah pelepasan karbon dari cadangan bahan bakar fosil ke atmosfer.\nBahan bakar fosil adalah karbon yang tersimpan jutaan tahun. Pembakarannya memindahkan karbon \"lama\" ke atmosfer dalam waktu singkat, sedangkan aliran alami P, Q, dan S relatif seimbang dalam jangka panjang. Itulah penyebab utama CO₂ naik dari ±280 ppm (praindustri) menjadi lebih dari 420 ppm.\n\nPengecoh: P justru mengurangi CO₂. Q dan S adalah bagian siklus alami. Laut memang menyerap sebagian CO₂ tambahan, tetapi bukan sumber tambahannya.",
      f_karbon),
    Q("Petani menanam kacang tanah atau kedelai secara bergiliran dengan padi untuk menjaga kesuburan tanah. Proses dalam siklus nitrogen yang dimanfaatkan dalam praktik ini adalah …",
      ["Fiksasi nitrogen oleh bakteri Rhizobium pada bintil akar tanaman legum", "Denitrifikasi yang melepaskan nitrogen dari tanah ke atmosfer",
       "Amonifikasi yang mengubah nitrat menjadi gas nitrogen bebas", "Pelapukan batuan yang melepaskan fosfat ke dalam tanah",
       "Penguapan amonia dari pupuk urea yang ditabur di permukaan"],
      "Tanaman tidak dapat langsung memanfaatkan gas nitrogen (N₂) di atmosfer. Bakteri Rhizobium yang bersimbiosis di bintil akar tanaman legum (kacang-kacangan) mampu mengikat N₂ dan mengubahnya menjadi amonia yang dapat dipakai tumbuhan. Setelah panen, sisa akar dan biomassa legum menambah nitrogen tanah sehingga kebutuhan pupuk nitrogen untuk tanaman berikutnya berkurang. Inilah dasar rotasi tanaman dan tumpang sari legum.\n\nPengecoh: denitrifikasi justru mengurangi nitrogen tanah. Amonifikasi mengubah bahan organik menjadi amonia, bukan nitrat menjadi N₂. Fosfat termasuk siklus fosfor. Penguapan amonia adalah kehilangan nitrogen dari pupuk.",
      None),
    Q("Perhatikan diagram Peltier berikut.\n\nLokasi yang mengalami pelapukan kimia paling kuat, beserta contoh wilayahnya, adalah …",
      ["X, wilayah tropis panas dan basah seperti Kalimantan", "Y, wilayah dingin dengan siklus beku-cair seperti Siberia",
       "Z, wilayah gurun panas seperti Sahara", "W, wilayah beriklim sedang seperti Eropa Barat", "Y dan Z, wilayah dengan curah hujan rendah"],
      "Pelapukan kimia memerlukan air sebagai pelarut dan suhu tinggi yang mempercepat reaksi kimia (hidrolisis, oksidasi, karbonasi). Titik X (26 °C, 2.500 mm) berada di zona pelapukan kimia kuat, khas wilayah tropis basah seperti Indonesia. Itulah sebabnya tanah di Indonesia umumnya tebal dan sangat lapuk, misalnya tanah laterit dan latosol.\n\nPengecoh: Y (−5 °C, 600 mm) berada di zona pelapukan mekanis beku-cair; air yang membeku di celah batuan memuai dan memecahkan batuan. Z (25 °C, 150 mm) sangat kering sehingga pelapukan kimia lemah, walaupun pelapukan mekanis akibat perubahan suhu harian tetap terjadi. W berada pada kondisi sedang. Opsi Y dan Z mengabaikan peran air.",
      f_peltier),
    Q("Dalam model siklus hara Gersmehl, hutan hujan tropis memiliki ciri penyimpanan hara yang khas. Ciri tersebut adalah …",
      ["Sebagian besar hara tersimpan di biomassa, sedangkan tanah relatif miskin hara",
       "Sebagian besar hara tersimpan di tanah sehingga lahan tetap subur setelah ditebang",
       "Sebagian besar hara tersimpan di serasah karena dekomposisi berjalan sangat lambat",
       "Hara tersebar merata di biomassa, serasah, dan tanah dalam jumlah yang sama",
       "Hara hampir tidak ada karena hujan lebat melarutkan seluruh unsur hara"],
      "Model Gersmehl menggambarkan tiga tempat penyimpanan hara: biomassa, serasah, dan tanah. Pada hutan hujan tropis, suhu dan kelembapan tinggi membuat dekomposisi serasah sangat cepat, dan hara segera diserap kembali oleh akar. Hujan lebat juga mencuci hara dari tanah. Akibatnya sebagian besar hara tersimpan di biomassa (pohon), sedangkan serasah tipis dan tanahnya relatif miskin hara.\nImplikasinya: ketika hutan ditebang dan biomassa diangkut atau dibakar, hara ikut hilang sehingga kesuburan lahan cepat menurun dalam beberapa musim tanam. Inilah alasan ladang berpindah dahulu memerlukan masa bera yang panjang.\n\nPengecoh: tanah tropis justru miskin hara. Serasah tipis karena dekomposisi cepat. Hara tidak merata. Hara tetap ada, terutama di biomassa.",
      None),
    Q("Perhatikan profil tanah lengkap berikut.\n\nHorizon tempat menumpuknya lempung, besi, dan aluminium yang tercuci dari horizon di atasnya (iluviasi) ditunjukkan oleh label …",
      ["N, horizon B", "M, horizon E", "L, horizon A", "O, horizon C", "K, horizon O"],
      "Urutan horizon tanah dari atas: O (serasah dan humus), A (tanah mineral bercampur bahan organik, berwarna gelap), E (zona eluviasi atau pencucian, berwarna pucat), B (zona iluviasi atau penimbunan lempung, Fe, dan Al), C (bahan induk yang melapuk sebagian), dan R (batuan dasar).\nPada gambar, K = O, L = A, M = E, N = B, O = C, dan P = R. Horizon tempat penimbunan bahan tercuci adalah N (horizon B).\n\nPengecoh: M (horizon E) adalah zona tempat bahan tercuci keluar, kebalikan dari B. L adalah horizon A. O adalah horizon C. K adalah horizon O (organik). Memahami horizon membantu menilai kesuburan dan potensi erosi tanah.",
      f_horizon),
    Q("Sebidang lahan miring memiliki R = 1.500, K = 0,3, LS = 2, C = 0,5, dan P = 1. Dengan rumus USLE A = R × K × LS × C × P (ton/ha/tahun), jika lahan diubah menjadi agroforestri sehingga C turun menjadi 0,1, besar penurunan erosi adalah …",
      ["360 ton/ha/tahun (80%)", "450 ton/ha/tahun (100%)", "90 ton/ha/tahun (20%)", "400 ton/ha/tahun (89%)", "36 ton/ha/tahun (8%)"],
      "1) Erosi awal: A = 1.500 × 0,3 × 2 × 0,5 × 1 = 450 ton/ha/tahun.\n2) Erosi setelah agroforestri: A = 1.500 × 0,3 × 2 × 0,1 × 1 = 90 ton/ha/tahun.\n3) Penurunan = 450 − 90 = 360 ton/ha/tahun, atau 360 ÷ 450 × 100% = 80%.\nFaktor C (tutupan dan pengelolaan tanaman) sangat berpengaruh: tajuk berlapis dan serasah agroforestri melindungi tanah dari pukulan air hujan dan memperlambat limpasan.\n\nPengecoh: 450 ton adalah erosi awal. 90 ton adalah erosi akhir. 400 dan 36 ton berasal dari salah perkalian. Faktor P (konservasi seperti terasering) juga dapat diturunkan untuk mengurangi erosi lebih lanjut.",
      None),
    Q("Perhatikan diagram tahapan suksesi di lahan lava yang baru membeku berikut.\n\nPeran utama komunitas pada tahap 1 adalah …",
      ["Melapukkan batuan dan membentuk lapisan tanah tipis bagi tumbuhan berikutnya", "Membentuk tajuk rapat yang menaungi tanah sehingga suhu tanah stabil",
       "Menjadi komunitas akhir yang stabil dan tidak akan digantikan lagi", "Menghasilkan kayu keras yang menjadi habitat satwa besar",
       "Mencegah tumbuhan lain tumbuh sehingga suksesi berhenti di tahap ini"],
      "Tahap 1 pada suksesi primer adalah komunitas pionir berupa lumut kerak (liken), simbiosis jamur dan alga. Liken mampu hidup di batuan gundul. Asam organik yang dikeluarkannya melapukkan batuan secara kimia, dan sisa tubuhnya yang mati bercampur dengan butiran batuan membentuk tanah tipis. Tanah ini memungkinkan tumbuhan berikutnya (rumput, herba) tumbuh, lalu secara bertahap semak, pohon pionir, hingga hutan klimaks (tahap 5).\n\nPengecoh: tajuk rapat dan kayu keras adalah ciri tahap akhir (hutan). Komunitas akhir yang stabil adalah hutan klimaks, bukan liken. Liken justru membuka jalan bagi tumbuhan lain.",
      f_suksesi),
    Q("Hujan asam dapat merusak tanaman, bangunan, dan ekosistem danau. Pernyataan yang paling tepat tentang hujan asam adalah …",
      ["Terbentuk dari SO₂ dan NOₓ yang bereaksi dengan uap air sehingga pH hujan di bawah 5,6",
       "Terbentuk dari CO₂ yang membuat pH hujan naik di atas 8 sehingga bersifat basa",
       "Terbentuk dari ozon stratosfer yang turun bersama hujan ke permukaan Bumi",
       "Terbentuk dari uap air laut yang mengandung garam sehingga pH hujan menjadi 7",
       "Hanya terjadi di sekitar gunung api dan tidak berkaitan dengan aktivitas manusia"],
      "Air hujan alami sedikit asam (pH ±5,6) karena CO₂ terlarut membentuk asam karbonat lemah. Hujan asam terjadi ketika sulfur dioksida (SO₂) dan nitrogen oksida (NOₓ) dari pembakaran batu bara, minyak, dan kendaraan bermotor bereaksi dengan uap air di atmosfer membentuk asam sulfat dan asam nitrat, sehingga pH hujan turun di bawah 5,6. Dampaknya: daun dan tanaman rusak, unsur hara tanah tercuci, danau menjadi asam, dan bangunan dari batu kapur atau logam terkikis.\n\nPengecoh: CO₂ membuat hujan sedikit asam, bukan basa. Ozon stratosfer tidak turun bersama hujan. Garam laut tidak menyebabkan hujan asam. Gunung api memang dapat melepaskan SO₂, tetapi aktivitas manusia adalah sumber utama di kawasan industri.",
      None),
]

P2 = [
    Q("Perhatikan grafik persentase mamalia darat endemik di tiap pulau berikut.\n\nPenjelasan yang paling tepat mengapa Sulawesi memiliki tingkat endemisme tertinggi adalah …",
      ["Sulawesi berada di Wallacea dan tidak pernah menyatu dengan Asia maupun Australia", "Sulawesi pernah menyatu dengan Asia sehingga fauna Asia berkembang sangat pesat",
       "Sulawesi memiliki luas daratan terbesar sehingga spesies yang hidup paling banyak", "Sulawesi berada tepat di Paparan Sahul sehingga faunanya seluruhnya tipe Australia",
       "Sulawesi memiliki penduduk paling sedikit sehingga tidak ada spesies yang punah"],
      "Endemisme tinggi terjadi pada wilayah yang terisolasi dalam waktu lama, sehingga spesies berevolusi secara terpisah (spesiasi). Sulawesi berada di zona Wallacea, di antara garis Wallace dan Lydekker, yang dikelilingi laut dalam. Saat muka laut turun pada zaman es, Sulawesi tetap tidak tersambung dengan Paparan Sunda maupun Sahul. Akibatnya banyak fauna khas yang hanya ada di sana, misalnya anoa, babirusa, tarsius, dan maleo.\nPapua juga tinggi karena isolasi dari Asia, sedangkan Jawa, Sumatra, dan Kalimantan rendah karena pernah menyatu dengan Asia (Sundaland) sehingga berbagi banyak spesies.\n\nPengecoh: menyatu dengan Asia justru menurunkan endemisme. Kalimantan dan Papua lebih luas dari Sulawesi. Sulawesi tidak berada di Paparan Sahul. Jumlah penduduk tidak menjelaskan endemisme.",
      f_endemik),
    Q("Dalam konsep HIPPO, penyebab utama kepunahan spesies saat ini di Indonesia adalah …",
      ["Hilangnya dan rusaknya habitat", "Spesies invasif yang masuk dari luar negeri", "Pencemaran udara di perkotaan",
       "Pertumbuhan penduduk di negara maju", "Perburuan oleh predator alami di hutan"],
      "HIPPO adalah singkatan lima penyebab utama hilangnya keanekaragaman hayati: Habitat loss (kehilangan habitat), Invasive species (spesies invasif), Pollution (pencemaran), Population (pertumbuhan penduduk manusia), dan Overharvesting (eksploitasi berlebihan, termasuk perburuan dan perdagangan satwa).\nUrutan huruf dalam akronim juga mencerminkan tingkat pengaruhnya, dan kehilangan habitat adalah penyebab terbesar. Di Indonesia, konversi hutan menjadi perkebunan, tambang, dan permukiman, serta kebakaran hutan dan lahan, telah memfragmentasi habitat orang utan, harimau sumatra, dan gajah.\n\nPengecoh: spesies invasif, pencemaran, dan pertumbuhan penduduk memang penyebab, tetapi bukan yang utama. Predator alami adalah bagian dari keseimbangan ekosistem, bukan penyebab kepunahan modern.",
      None),
    Q("Perhatikan tabel penurunan populasi empat spesies berikut. Menurut kriteria A IUCN: penurunan ≥ 80% → Kritis (CR); ≥ 50% → Genting (EN); ≥ 30% → Rentan (VU).\n\nPasangan spesies dan status yang tepat adalah …",
      ["A – Kritis (CR); C – Rentan (VU)", "A – Genting (EN); B – Kritis (CR)", "B – Rentan (VU); C – Genting (EN)",
       "C – Kritis (CR); D – Rentan (VU)", "D – Genting (EN); A – Rentan (VU)"],
      "Cocokkan persentase penurunan populasi dalam 10 tahun (setara tiga generasi) dengan ambang kriteria A:\n• A: 85% ≥ 80% → Kritis (Critically Endangered, CR).\n• B: 55% ≥ 50% → Genting (Endangered, EN).\n• C: 35% ≥ 30% → Rentan (Vulnerable, VU).\n• D: 10% < 30% → belum memenuhi kategori terancam berdasarkan kriteria A (mungkin Hampir Terancam atau Risiko Rendah).\nPasangan yang tepat adalah A – CR dan C – VU.\n\nPengecoh: opsi lain menukar status atau memberi status terancam pada spesies D. Contoh spesies Indonesia berstatus CR antara lain badak jawa, badak sumatra, harimau sumatra, dan orang utan tapanuli.",
      f_iucn),
    Q("Penangkaran jalak bali di kebun binatang dan pelestarian anoa di Taman Nasional Lore Lindu masing-masing merupakan contoh konservasi …",
      ["Ex situ dan in situ", "In situ dan ex situ", "Keduanya in situ", "Keduanya ex situ", "Ex situ dan restorasi ekosistem"],
      "Konservasi in situ adalah pelestarian spesies di habitat aslinya, misalnya taman nasional, cagar alam, dan suaka margasatwa. Konservasi ex situ adalah pelestarian di luar habitat aslinya, misalnya kebun binatang, kebun raya, pusat penangkaran, dan bank benih.\nPenangkaran jalak bali di kebun binatang berlangsung di luar habitat alaminya (ex situ), sedangkan pelestarian anoa di taman nasional di Sulawesi berlangsung di habitat aslinya (in situ). Kedua cara saling melengkapi: penangkaran dapat menghasilkan individu untuk dilepasliarkan kembali ke habitat alami.\n\nPengecoh: opsi lain menukar atau menyamakan jenis konservasinya. Restorasi ekosistem adalah pemulihan habitat yang rusak, bukan penangkaran.",
      None),
    Q("Perhatikan perubahan bentang hutan tahun 1990 dan 2020 berikut.\n\nDampak ekologis yang paling mungkin dari perubahan tersebut adalah …",
      ["Populasi satwa terisolasi di petak kecil dan efek tepi meningkat", "Keanekaragaman hayati pasti meningkat karena habitat menjadi lebih beragam",
       "Satwa besar lebih mudah bergerak karena jarak antarhabitat makin pendek", "Iklim mikro di dalam petak hutan menjadi lebih sejuk dan lembap",
       "Tidak ada dampak karena luas total hutan masih lebih dari separuh"],
      "Gambar menunjukkan hutan yang semula utuh terpecah menjadi enam petak kecil yang dipisahkan lahan pertanian dan jalan (fragmentasi habitat). Dampaknya: (1) populasi satwa terisolasi dalam petak kecil sehingga mudah mengalami perkawinan sekerabat dan kepunahan lokal; (2) efek tepi meningkat karena perbandingan keliling terhadap luas petak besar, sehingga bagian dalam hutan terpapar angin, cahaya, suhu lebih tinggi, spesies invasif, dan perburuan; (3) satwa berdaya jelajah luas seperti gajah dan harimau kesulitan bergerak dan sering berkonflik dengan manusia.\n\nPengecoh: keanekaragaman spesies hutan cenderung menurun. Jarak antarhabitat justru bertambah dan terputus. Iklim mikro menjadi lebih panas dan kering. Luas total hutan pada 2020 jauh berkurang. Solusinya adalah koridor satwa yang menghubungkan petak-petak hutan.",
      f_fragmen),
    Q("Hutan mangrove melindungi pantai dari abrasi, menyediakan kayu bakar, menjadi tempat pemijahan ikan, dan menjadi lokasi wisata edukasi. Jasa \"melindungi pantai dari abrasi\" termasuk kategori jasa ekosistem …",
      ["Pengaturan (regulating)", "Penyediaan (provisioning)", "Budaya (cultural)", "Pendukung (supporting)", "Penyediaan dan budaya sekaligus"],
      "Jasa ekosistem dibagi menjadi empat kategori:\n• Penyediaan (provisioning): produk yang langsung diperoleh, misalnya kayu bakar, ikan, dan obat-obatan.\n• Pengaturan (regulating): manfaat dari pengaturan proses alam, misalnya perlindungan pantai dari abrasi dan gelombang, pengendalian banjir, penyerapan karbon, dan penjernihan air.\n• Budaya (cultural): manfaat nonmaterial, misalnya wisata, pendidikan, dan nilai spiritual.\n• Pendukung (supporting): proses dasar yang menopang jasa lain, misalnya siklus hara, pembentukan tanah, dan habitat pemijahan.\nPerlindungan pantai dari abrasi adalah jasa pengaturan.\n\nPengecoh: kayu bakar adalah jasa penyediaan, wisata adalah jasa budaya, dan tempat pemijahan sering digolongkan jasa pendukung (habitat).",
      None),
    Q("Perhatikan grafik kekayaan spesies burung menurut lintang berikut.\n\nPenjelasan yang paling tepat untuk pola tersebut adalah …",
      ["Wilayah tropis menerima energi tinggi, iklim stabil, dan sejarah evolusi panjang", "Wilayah kutub memiliki lebih banyak habitat sehingga spesiesnya paling beragam",
       "Kekayaan spesies meningkat ke arah kutub karena predator semakin sedikit", "Wilayah tropis memiliki musim dingin panjang yang memicu migrasi banyak spesies",
       "Pola tersebut kebetulan karena penelitian hanya dilakukan di wilayah tropis"],
      "Grafik memperlihatkan gradien keanekaragaman menurut lintang: jumlah spesies tertinggi di sekitar ekuator (±600) dan menurun ke arah kutub (±40 pada 70°). Penjelasan utamanya: wilayah tropis menerima energi Matahari tinggi sehingga produktivitas primer besar; iklimnya relatif stabil sepanjang tahun dan sepanjang sejarah geologi (tidak tertutup es pada zaman glasial), sehingga spesies punya waktu panjang untuk berevolusi dan berdiversifikasi; serta struktur habitat (misalnya hutan berlapis) sangat kompleks.\nIndonesia yang terletak di khatulistiwa dan memiliki ribuan pulau termasuk negara megabiodiversitas.\n\nPengecoh: kutub justru miskin spesies. Grafik menunjukkan penurunan, bukan kenaikan, ke arah kutub. Wilayah tropis tidak memiliki musim dingin. Pola ini telah dibuktikan dari banyak penelitian di berbagai lintang.",
      f_lintang),
    Q("Pasangan spesies endemik dan wilayah asalnya yang tepat adalah …",
      ["Anoa – Sulawesi; cendrawasih – Papua", "Komodo – Sumatra; orang utan – Sulawesi", "Badak jawa – Kalimantan; maleo – Jawa",
       "Tarsius – Papua; jalak bali – Nusa Tenggara Timur", "Harimau sumatra – Sulawesi; babirusa – Kalimantan"],
      "Beberapa spesies endemik Indonesia dan wilayahnya:\n• Anoa, babirusa, tarsius, dan maleo – Sulawesi (Wallacea).\n• Cendrawasih dan kanguru pohon – Papua (tipe Australia).\n• Komodo – Pulau Komodo, Rinca, dan Flores (Nusa Tenggara Timur).\n• Orang utan – Sumatra dan Kalimantan.\n• Badak jawa – Ujung Kulon, Jawa Barat (Banten).\n• Jalak bali – Bali.\n• Harimau sumatra – Sumatra.\nHanya pasangan anoa–Sulawesi dan cendrawasih–Papua yang keduanya benar.\n\nPengecoh: opsi lain menukar wilayah asal spesies. Memahami persebaran ini membantu menjelaskan pembagian fauna berdasarkan garis Wallace dan Lydekker.",
      None),
    Q("Perhatikan grafik perkiraan populasi badak jawa di Taman Nasional Ujung Kulon berikut.\n\nWalaupun populasinya meningkat sejak 1967, badak jawa tetap berstatus Kritis (CR). Alasan yang paling tepat adalah …",
      ["Seluruh populasi terkonsentrasi di satu lokasi yang rawan tsunami dan wabah penyakit", "Populasinya terus menurun tajam sehingga diperkirakan punah dalam lima tahun",
       "Badak jawa juga tersebar luas di Kalimantan dan Sumatra dalam jumlah besar", "Status IUCN tidak pernah berubah meskipun jumlah populasi bertambah",
       "Badak jawa adalah spesies invasif sehingga perlu dikendalikan populasinya"],
      "Grafik menunjukkan populasi naik dari ±25 individu (1967) menjadi ±76 individu (2023). Namun jumlah ini sangat kecil dan seluruhnya berada di satu lokasi, yaitu Semenanjung Ujung Kulon. Populasi kecil dan tunggal sangat rentan terhadap: bencana (tsunami dari Selat Sunda atau Gunung Anak Krakatau), wabah penyakit, kawin sekerabat yang menurunkan keragaman genetik, serta persaingan dengan tumbuhan invasif langkap yang mengurangi pakan. Karena itu konservasi diarahkan pada pembentukan populasi kedua di habitat lain.\n\nPengecoh: populasi pada grafik tidak menurun tajam. Badak jawa tidak lagi tersebar di Kalimantan dan Sumatra. Status IUCN dapat berubah bila kriteria terpenuhi. Badak jawa adalah spesies asli, bukan invasif.",
      f_badak),
    Q("Dalam valuasi ekonomi, sejumlah warga kota bersedia membayar iuran tahunan agar terumbu karang di Raja Ampat tetap lestari walaupun mereka tidak pernah berencana mengunjunginya. Nilai yang ditunjukkan adalah …",
      ["Nilai keberadaan (existence value)", "Nilai guna langsung (direct use value)", "Nilai guna tidak langsung (indirect use value)",
       "Nilai pilihan (option value)", "Nilai produksi pasar (market value)"],
      "Nilai ekonomi total terdiri atas:\n• Nilai guna langsung: manfaat yang langsung dimanfaatkan, misalnya ikan dan wisata selam.\n• Nilai guna tidak langsung: fungsi ekologis, misalnya terumbu sebagai pemecah gelombang dan habitat ikan.\n• Nilai pilihan: kesediaan membayar agar sumber daya tetap tersedia untuk dimanfaatkan di masa depan oleh diri sendiri.\n• Nilai keberadaan: kepuasan mengetahui suatu ekosistem atau spesies tetap ada, walaupun tidak pernah dimanfaatkan atau dikunjungi.\nKesediaan membayar oleh warga yang tidak berencana berkunjung menunjukkan nilai keberadaan. Nilai ini biasanya diukur dengan metode survei kesediaan membayar (contingent valuation).\n\nPengecoh: nilai guna langsung dan tidak langsung memerlukan pemanfaatan. Nilai pilihan berkaitan dengan rencana pemanfaatan di masa depan. Nilai pasar tidak mencakup manfaat nonpasar ini.",
      None),
]

P3 = [
    Q("Perhatikan profil oksigen terlarut Sungai S di hilir titik pembuangan limbah organik berikut.\n\nStasiun dengan kondisi paling buruk dan penjelasannya adalah …",
      ["C, karena dekomposisi oleh bakteri paling intensif menghabiskan oksigen", "A, karena paling dekat dengan titik pembuangan limbah organik",
       "E, karena kandungan oksigennya paling tinggi sehingga bakteri tidak bekerja", "D, karena sudah berada di atas baku mutu DO 4 mg/L",
       "B, karena limbah organik langsung mengendap di dasar sungai"],
      "Setelah limbah organik masuk ke sungai, bakteri pengurai menguraikannya sambil memakai oksigen terlarut. Penurunan DO tidak langsung maksimum di titik pembuangan; konsumsi oksigen paling tinggi terjadi agak ke hilir ketika bakteri berkembang pesat. Pada grafik, DO minimum (±2,4 mg/L) terdapat di Stasiun C (6 km), jauh di bawah baku mutu 4 mg/L. Setelah itu DO pulih secara bertahap (D dan E) karena bahan organik berkurang dan oksigen dari udara masuk kembali (reaerasi). Proses ini disebut kurva sag oksigen dan menggambarkan swapurifikasi sungai.\n\nPengecoh: A dekat titik pembuangan tetapi DO-nya masih 5,2 mg/L. E kondisinya paling baik. D (4,4 mg/L) sudah pulih. B (3,6 mg/L) buruk, tetapi bukan yang terburuk.",
      f_sag),
    Q("Hasil uji laboratorium menunjukkan air limbah industri memiliki COD 400 mg/L dan BOD 80 mg/L. Interpretasi yang paling tepat adalah …",
      ["Banyak bahan pencemar sulit diurai bakteri karena COD jauh lebih besar dari BOD", "Seluruh pencemar mudah diurai bakteri karena nilai BOD lebih rendah dari COD",
       "Air limbah tersebut bersih karena BOD di bawah 100 mg/L", "Kadar oksigen terlarut dalam air limbah mencapai 400 mg/L",
       "BOD dan COD mengukur hal yang sama sehingga perbedaan tersebut kesalahan alat"],
      "BOD (Biochemical Oxygen Demand) mengukur oksigen yang diperlukan bakteri untuk menguraikan bahan organik yang mudah terurai secara biologis. COD (Chemical Oxygen Demand) mengukur oksigen yang diperlukan untuk mengoksidasi seluruh bahan organik secara kimia, termasuk yang sulit terurai bakteri. Nilai COD selalu lebih besar atau sama dengan BOD.\nRasio BOD/COD = 80/400 = 0,2. Rasio yang rendah (< 0,3) menunjukkan sebagian besar pencemar sulit diurai secara biologis, misalnya pewarna tekstil atau senyawa kimia sintetis, sehingga diperlukan pengolahan kimia-fisika tambahan.\n\nPengecoh: BOD lebih rendah dari COD bukan berarti semua mudah terurai. BOD 80 mg/L tergolong tinggi (baku mutu umumnya 30–50 mg/L). BOD dan COD bukan kadar oksigen terlarut. Keduanya mengukur hal berbeda.",
      None),
    Q("Perhatikan grafik pH air hujan di empat lokasi berikut. Garis putus-putus menunjukkan pH air hujan alami (5,6).\n\nLokasi yang mengalami hujan asam dan penyebab yang paling mungkin adalah …",
      ["K, karena dekat kawasan PLTU batu bara yang melepaskan SO₂", "L, karena dekat pantai sehingga uap air laut bersifat basa",
       "M, karena pH di atas 7 menunjukkan konsentrasi SO₂ tinggi", "N, karena pH-nya sedikit di atas 5,6 akibat CO₂ alami",
       "Semua lokasi karena seluruh pH di bawah 8"],
      "Hujan disebut hujan asam bila pH-nya lebih rendah dari pH hujan alami (±5,6). Pada grafik, hanya sampel K (pH 4,2) yang berada di bawah garis 5,6. pH 4,2 berarti keasaman sekitar 25 kali lebih tinggi dari hujan alami (selisih 1,4 satuan pH dalam skala logaritmik). Penyebab paling mungkin adalah emisi SO₂ dan NOₓ dari pembakaran batu bara, misalnya PLTU atau industri, yang membentuk asam sulfat dan nitrat di atmosfer.\n\nPengecoh: L (6,8) dan M (7,5) bukan hujan asam. Uap air laut tidak menjelaskan sifat basa. pH di atas 7 justru basa, bukan tanda SO₂ tinggi. N (5,8) masih di atas 5,6. Batas hujan asam bukan pH 8.",
      f_ph),
    Q("Kabut asap akibat karhutla di Sumatra dan Kalimantan sering semakin pekat pada pagi hari. Faktor meteorologis yang paling menjelaskan hal tersebut adalah …",
      ["Inversi suhu dan angin lemah pada pagi hari menahan asap dekat permukaan", "Pemanasan permukaan yang kuat pada pagi hari mendorong asap naik ke atas",
       "Hujan lebat pada pagi hari membawa partikel asap jatuh ke permukaan", "Angin laut yang kencang pada pagi hari mengumpulkan asap di daratan",
       "Radiasi Matahari pagi yang kuat menciptakan asap baru dari permukaan tanah"],
      "Pada malam hingga pagi hari, permukaan tanah mendingin cepat sehingga udara di dekat permukaan lebih dingin daripada udara di atasnya (inversi suhu). Lapisan inversi bersifat sangat stabil dan menghambat gerak vertikal. Ditambah angin lemah pada pagi hari, asap dan partikel PM2,5 tertahan dan terakumulasi di dekat permukaan sehingga kabut asap paling pekat dan jarak pandang paling pendek. Menjelang siang, pemanasan permukaan memecah inversi sehingga asap sedikit tersebar ke atas.\n\nPengecoh: pemanasan kuat justru terjadi siang hari dan menyebarkan asap. Hujan membersihkan, bukan mempekat, asap. Angin laut bertiup siang hari. Radiasi Matahari tidak menciptakan asap.",
      None),
    Q("Perhatikan tabel subindeks ISPU tiap parameter di tiga kota berikut. Nilai ISPU harian suatu kota ditentukan oleh subindeks tertinggi. Kategori: 0–50 baik; 51–100 sedang; 101–200 tidak sehat.\n\nPernyataan yang tepat adalah …",
      ["Kota X: ISPU 165 tidak sehat dengan parameter dominan PM2,5", "Kota X: ISPU 89 sedang, yaitu rata-rata seluruh parameter",
       "Kota Y: ISPU 95 sedang dengan parameter dominan PM2,5", "Kota Z: ISPU 143 tidak sehat, yaitu jumlah semua subindeks",
       "Kota Y: ISPU 290 sangat tidak sehat, yaitu jumlah semua subindeks"],
      "ISPU harian dilaporkan dari subindeks parameter tertinggi, sedangkan parameter tersebut disebut parameter dominan (kritis).\n• Kota X: subindeks tertinggi PM2,5 = 165 → tidak sehat, dominan PM2,5.\n• Kota Y: tertinggi PM10 = 120 → tidak sehat, dominan PM10.\n• Kota Z: tertinggi PM2,5 = 48 → baik.\n\nPengecoh: ISPU tidak dihitung dari rata-rata maupun jumlah subindeks; pendekatan rata-rata akan menyembunyikan bahaya parameter yang paling tinggi. Kota Y dominan PM10, bukan PM2,5. Kota Z tergolong baik.",
      f_ispu3),
    Q("Penambangan emas tanpa izin (PETI) di beberapa daerah Indonesia sering menggunakan merkuri untuk mengikat emas. Bahaya utama merkuri bagi masyarakat di hilir adalah …",
      ["Merkuri menjadi metilmerkuri yang terakumulasi dan berbiomagnifikasi pada ikan konsumsi", "Merkuri mudah terurai bakteri sehingga hanya berbahaya selama beberapa hari",
       "Merkuri membuat air sungai menjadi basa sehingga tanaman padi tumbuh lebih cepat", "Merkuri hanya berbahaya bagi penambang dan tidak memengaruhi penduduk hilir",
       "Merkuri meningkatkan oksigen terlarut sehingga ikan berkembang biak berlebihan"],
      "Merkuri yang terbuang ke sungai dapat diubah bakteri di sedimen menjadi metilmerkuri, bentuk organik yang sangat beracun dan mudah diserap makhluk hidup. Metilmerkuri terakumulasi di jaringan tubuh (bioakumulasi) dan meningkat konsentrasinya pada tingkat trofik lebih tinggi (biomagnifikasi), sehingga ikan predator mengandung kadar tinggi. Penduduk hilir yang mengonsumsi ikan tersebut berisiko mengalami kerusakan saraf, gangguan perkembangan janin, dan kecacatan, seperti tragedi Minamata di Jepang. Indonesia telah meratifikasi Konvensi Minamata (UU No. 11 Tahun 2017).\n\nPengecoh: merkuri tidak mudah terurai dan bertahan lama di lingkungan. Merkuri tidak menyuburkan tanaman. Dampaknya meluas ke hilir melalui air dan rantai makanan. Merkuri tidak menambah oksigen terlarut.",
      None),
    Q("Perhatikan denah permukiman dan sebaran rembesan limbah dari tangki septik berikut.\n\nSumur yang paling berisiko tercemar bakteri E. coli dari tangki septik adalah …",
      ["W2, karena berada di hilir aliran air tanah dan di dalam sebaran rembesan", "W1, karena berada di hulu aliran sehingga limbah mengalir ke arahnya",
       "W3, karena paling jauh dari tangki septik sehingga paling banyak tercemar", "W4, karena berada tegak lurus terhadap arah aliran di luar sebaran rembesan",
       "Semua sumur sama berisikonya karena air tanah tidak bergerak"],
      "Pencemar dari tangki septik terbawa aliran air tanah ke arah hilir dan membentuk sebaran rembesan (plume) memanjang searah aliran. Pada gambar, air tanah mengalir dari kiri ke kanan. Sumur W2 berada di hilir tangki septik dan di dalam area rembesan, sehingga paling berisiko tercemar. W3 juga di hilir tetapi berada di luar ujung rembesan, dan konsentrasi pencemar berkurang seiring jarak. W1 berada di hulu, sedangkan W4 berada di samping di luar rembesan.\nKarena itu jarak minimal sumur dan tangki septik (umumnya ±10 m) serta posisinya terhadap arah aliran air tanah perlu diperhatikan.\n\nPengecoh: pencemar tidak mengalir ke hulu. Jarak terjauh justru paling kecil risikonya. Air tanah bergerak walaupun lambat.",
      f_plume),
    Q("Pemulihan tanah tercemar logam berat bekas tambang dengan menanam tumbuhan yang mampu menyerap dan menimbun logam di jaringannya disebut …",
      ["Fitoremediasi", "Bioremediasi dengan bakteri", "Insinerasi", "Landfill sanitasi", "Pengomposan aerob"],
      "Remediasi adalah upaya memulihkan lingkungan yang tercemar. Fitoremediasi memanfaatkan tumbuhan untuk menyerap, menimbun, menstabilkan, atau menguraikan pencemar. Beberapa tumbuhan hiperakumulator mampu menimbun logam berat dalam jumlah besar di jaringan, lalu dipanen dan diolah dengan aman. Metode ini murah dan ramah lingkungan, tetapi memerlukan waktu lama.\n\nPengecoh: bioremediasi memakai mikroorganisme seperti bakteri untuk menguraikan pencemar organik (misalnya tumpahan minyak). Insinerasi adalah pembakaran limbah pada suhu tinggi. Landfill sanitasi adalah penimbunan sampah terkendali. Pengomposan aerob mengolah sampah organik, bukan memulihkan tanah tercemar logam berat.",
      None),
    Q("Perhatikan grafik sumber PM2,5 di Kota M berikut.\n\nKebijakan yang paling efektif menurunkan konsentrasi PM2,5 di kota tersebut adalah …",
      ["Memperluas transportasi umum dan memperketat uji emisi kendaraan bermotor", "Melarang pembakaran sampah terbuka sebagai satu-satunya kebijakan",
       "Menyiram jalan setiap hari untuk mengurangi debu dari konstruksi", "Menambah jumlah PLTU di dalam kota agar listrik lebih murah",
       "Mengganti seluruh pohon kota dengan taman rumput agar sirkulasi udara lancar"],
      "Grafik menunjukkan kendaraan bermotor adalah sumber terbesar PM2,5 (46%), disusul industri dan pembangkit (22%). Kebijakan paling efektif adalah yang menyasar sumber terbesar, misalnya memperluas transportasi umum massal, membatasi kendaraan pribadi, memperketat uji emisi, dan mendorong kendaraan listrik serta bahan bakar bersih.\n\nPengecoh: pelarangan pembakaran terbuka dan penyiraman jalan bermanfaat, tetapi hanya menyasar sumber kecil (9% dan sebagian dari 13%), sehingga dampaknya terbatas bila dijadikan satu-satunya kebijakan. Menambah PLTU di dalam kota justru menambah emisi. Pohon kota membantu menyaring partikel, sehingga menggantinya dengan rumput merugikan.",
      f_pm),
    Q("Konsentrasi suatu pestisida pada fitoplankton adalah 0,02 ppm. Jika faktor biomagnifikasi setiap tingkat trofik adalah 10 kali, konsentrasi pestisida pada konsumen III adalah …",
      ["20 ppm", "2 ppm", "0,6 ppm", "200 ppm", "0,2 ppm"],
      "Fitoplankton adalah produsen. Konsumen III berada tiga tingkat di atasnya, sehingga faktor biomagnifikasi dikalikan tiga kali:\n0,02 × 10 × 10 × 10 = 0,02 × 1.000 = 20 ppm.\nUrutannya: produsen 0,02 → konsumen I 0,2 → konsumen II 2 → konsumen III 20 ppm.\n\nPengecoh: 0,2 dan 2 ppm adalah konsentrasi konsumen I dan II. 0,6 ppm muncul bila faktor dijumlahkan (0,02 × 30). 200 ppm adalah konsentrasi konsumen IV. Perhatikan bahwa pada biomagnifikasi faktor dikalikan, bukan dijumlahkan, sehingga konsentrasinya melonjak pada predator puncak, termasuk manusia.",
      None),
]

P4 = [
    Q("Perhatikan diagram komposisi sampah Kota R berikut.\n\nStrategi yang paling efektif mengurangi volume sampah yang dikirim ke TPA adalah …",
      ["Memilah dan mengompos sampah organik sejak dari rumah tangga", "Membakar seluruh sampah plastik secara terbuka di tiap kelurahan",
       "Menambah truk pengangkut agar sampah lebih cepat sampai di TPA", "Mendaur ulang logam dan kaca sebagai prioritas utama pengelolaan",
       "Membuang sampah organik ke sungai karena mudah terurai secara alami"],
      "Diagram menunjukkan sisa makanan dan sampah organik merupakan komponen terbesar (40%), ditambah kayu dan ranting (8%). Sampah organik dapat dikompos, diolah menjadi biogas, atau dijadikan pakan maggot (larva BSF). Pemilahan sejak dari sumber (rumah tangga) membuat sampah organik tidak tercampur dengan anorganik, sehingga lebih mudah diolah dan nilai daur ulang plastik serta kertas tetap terjaga. Dengan cara ini, hampir separuh volume sampah tidak perlu dikirim ke TPA dan emisi metana dari TPA berkurang.\n\nPengecoh: pembakaran terbuka menghasilkan polusi udara dan dioksin. Menambah truk tidak mengurangi volume sampah. Logam dan kaca hanya 6%. Membuang sampah ke sungai mencemari air dan memicu banjir.",
      f_sampah),
    Q("Konsentrasi sampah plastik yang sangat tinggi ditemukan di Samudra Pasifik Utara bagian tengah (Great Pacific Garbage Patch). Penyebab utama penumpukan di lokasi tersebut adalah …",
      ["Arus berputar (gyre) subtropis mengumpulkan sampah mengapung ke bagian tengahnya", "Arus upwelling mengangkat plastik dari dasar laut ke permukaan Pasifik",
       "Angin pasat meniup plastik langsung dari daratan Asia ke tengah samudra dalam sehari", "Plastik dari kapal tenggelam yang semuanya karam di wilayah tersebut",
       "Suhu air yang sangat dingin membuat plastik mengapung dan tidak bergerak"],
      "Di setiap cekungan samudra besar terdapat gyre subtropis, yaitu sistem arus permukaan yang berputar mengelilingi pusat tekanan tinggi subtropis (searah jarum jam di BBU). Pengaruh transport Ekman membuat air permukaan dan benda mengapung cenderung bergerak ke pusat gyre (konvergen) dan terperangkap di sana karena arus di pusatnya lemah. Sampah plastik dari daratan dan kapal yang terbawa arus selama bertahun-tahun akhirnya terkumpul di pusat gyre Pasifik Utara.\n\nPengecoh: upwelling tidak terjadi di pusat gyre dan tidak mengangkat plastik dari dasar. Proses penumpukan berlangsung bertahun-tahun, bukan sehari. Penyebabnya bukan kapal karam. Perairan di sana subtropis, tidak sangat dingin.",
      None),
    Q("Perhatikan peta arus berputar (gyre) di samudra dunia berikut.\n\nLokasi yang paling mungkin menjadi tempat penumpukan sampah plastik terapung terbesar adalah …",
      ["P", "Q", "R", "S", "T"],
      "Titik P berada di pusat gyre subtropis Pasifik Utara. Arus permukaan berputar di sekelilingnya, dan transport Ekman mengarahkan benda mengapung menuju pusat gyre sehingga sampah plastik terkonsentrasi di lokasi ini.\n• Q terletak di sekitar ekuator Pasifik, zona arus ekuatorial yang divergen (menyebar), sehingga bukan zona penumpukan.\n• R terletak di dekat pesisir Indonesia; memang menerima banyak sampah dari daratan, tetapi arusnya terus membawa sampah pergi.\n• S berada di Samudra Selatan dengan Arus Lingkar Antartika yang kuat.\n• T berada di Arktik, jauh dari pusat gyre subtropis.\nCatatan: lima gyre subtropis (Pasifik Utara, Pasifik Selatan, Atlantik Utara, Atlantik Selatan, dan Hindia) semuanya menjadi lokasi penumpukan plastik.",
      f_gyre),
    Q("Dalam hierarki pengelolaan sampah ekonomi sirkular, urutan prioritas dari yang paling diutamakan adalah …",
      ["Kurangi → guna ulang → daur ulang → pemulihan energi → pembuangan akhir", "Daur ulang → kurangi → guna ulang → pembuangan akhir → pemulihan energi",
       "Pembuangan akhir → pemulihan energi → daur ulang → guna ulang → kurangi", "Pemulihan energi → daur ulang → kurangi → guna ulang → pembuangan akhir",
       "Guna ulang → pembuangan akhir → kurangi → daur ulang → pemulihan energi"],
      "Hierarki pengelolaan sampah menempatkan pencegahan sebagai prioritas tertinggi karena sampah yang tidak dihasilkan tidak perlu diolah sama sekali:\n1) Kurangi (reduce), misalnya membawa tas belanja sendiri.\n2) Guna ulang (reuse), misalnya botol isi ulang.\n3) Daur ulang (recycle), mengolah material menjadi produk baru.\n4) Pemulihan energi (recovery), misalnya insinerator penghasil listrik atau RDF.\n5) Pembuangan akhir di TPA, pilihan terakhir.\nEkonomi sirkular menjaga material tetap dalam siklus pemakaian selama mungkin, berbeda dari ekonomi linear (ambil–buat–buang).\n\nPengecoh: opsi lain mengacak atau membalik urutan, misalnya menjadikan daur ulang sebagai prioritas pertama, padahal daur ulang tetap memerlukan energi dan menurunkan kualitas material.",
      None),
    Q("Perhatikan penampang zonasi ekosistem pesisir tropis berikut.\n\nFungsi utama ekosistem Y terhadap ekosistem Z adalah …",
      ["Menangkap sedimen dan menyaring air sehingga perairan tetap jernih bagi karang", "Menyediakan kayu bakar dan bahan bangunan bagi masyarakat pesisir",
       "Menahan gelombang badai di garis pantai daratan sebelum mencapai permukiman", "Menurunkan suhu air laut sehingga karang tidak pernah memutih",
       "Menghasilkan pasir putih yang menimbun karang di dasar laut"],
      "Gambar menunjukkan zonasi dari darat ke laut: X = hutan mangrove di garis pantai, Y = padang lamun di perairan dangkal, dan Z = terumbu karang di dekat tubir.\nKetiga ekosistem saling terkait. Padang lamun (Y) memperlambat arus, menangkap sedimen, dan menyerap nutrien berlebih dari daratan, sehingga air yang mencapai terumbu karang tetap jernih. Karang (Z) memerlukan air jernih agar alga simbionnya (zooxanthellae) dapat berfotosintesis. Lamun juga menjadi tempat mencari makan dan asuhan ikan muda serta dugong.\n\nPengecoh: kayu bakar dan penahan gelombang di garis pantai adalah fungsi mangrove (X). Lamun tidak dapat mencegah pemutihan karang akibat kenaikan suhu laut global. Lamun tidak menghasilkan pasir yang menimbun karang.",
      f_pesisir),
    Q("Pemutihan karang (coral bleaching) massal di perairan Indonesia pada tahun 2016 dan 2024 terutama dipicu oleh …",
      ["Suhu laut di atas normal dalam waktu lama sehingga zooxanthellae keluar",
       "Penurunan suhu muka laut yang membuat karang membeku di perairan dangkal",
       "Penangkapan ikan dengan bom yang memutihkan karang karena ledakan",
       "Hujan asam yang turun langsung di atas terumbu karang setiap hari",
       "Peningkatan kadar oksigen terlarut akibat fotosintesis lamun yang berlebihan"],
      "Karang hidup bersimbiosis dengan alga zooxanthellae yang memberi warna dan sebagian besar makanan melalui fotosintesis. Ketika suhu muka laut naik sekitar 1 °C di atas rata-rata maksimum musim panas selama beberapa minggu, karang mengalami stres dan mengeluarkan zooxanthellae. Jaringan karang menjadi transparan sehingga kerangka kapur putihnya terlihat (memutih). Bila kondisi berlangsung lama, karang mati. Peristiwa 2016 dan 2023–2024 berkaitan dengan El Niño kuat yang diperparah pemanasan global.\n\nPengecoh: perairan tropis tidak membeku. Bom ikan menghancurkan, bukan memutihkan, karang. Hujan asam bukan penyebab utama. Oksigen dari lamun tidak memicu pemutihan.",
      None),
    Q("Perhatikan grafik akumulasi tekanan panas (Degree Heating Weeks, DHW) di terumbu karang Perairan T berikut.\n\nPeriode ketika pemutihan luas dan kematian karang paling mungkin terjadi adalah …",
      ["Sekitar minggu ke-16 sampai ke-20", "Sekitar minggu ke-1 sampai ke-6", "Sekitar minggu ke-10 sampai ke-13",
       "Sekitar minggu ke-23 sampai ke-26", "Sepanjang 26 minggu dengan intensitas sama"],
      "DHW mengukur akumulasi tekanan panas: berapa derajat dan berapa lama suhu muka laut melebihi ambang pemutihan dalam 12 minggu terakhir. Pada grafik, DHW mencapai ≥ 8 °C-minggu (zona merah) sekitar minggu ke-16 sampai ke-20, dengan puncak ±9 pada minggu ke-17. Kondisi ini dikaitkan dengan pemutihan luas dan kematian karang.\nMinggu ke-10 sampai ke-13 berada pada DHW 2,5–5 (pemutihan mulai terjadi). Minggu ke-1 sampai ke-6 hampir tanpa tekanan panas, dan setelah minggu ke-23 DHW turun di bawah 4.\n\nPengecoh: intensitas tekanan panas jelas berubah setiap minggu. Data seperti ini dipakai lembaga pemantau untuk mengeluarkan peringatan dini pemutihan karang.",
      f_dhw),
    Q("Reklamasi pantai untuk kawasan komersial di sebuah teluk sering ditolak nelayan setempat. Dampak lingkungan yang paling sering menjadi alasan penolakan tersebut adalah …",
      ["Hilangnya wilayah tangkap, rusaknya ekosistem pesisir, dan berubahnya pola arus", "Bertambahnya luas mangrove sehingga ikan berpindah ke tempat lain",
       "Meningkatnya kualitas air teluk sehingga ikan menjadi terlalu banyak", "Menurunnya muka laut di teluk sehingga perahu nelayan kandas",
       "Berkurangnya sedimentasi di muara sungai sehingga air menjadi terlalu jernih"],
      "Reklamasi menimbun perairan pesisir menjadi daratan baru. Dampaknya antara lain: (1) hilangnya wilayah tangkap dan akses nelayan ke laut; (2) rusaknya terumbu karang, lamun, dan mangrove akibat penimbunan dan kekeruhan; (3) berubahnya pola arus dan gelombang sehingga sedimentasi atau abrasi berpindah ke pantai lain; (4) terganggunya aliran sungai ke laut yang dapat memperparah banjir di daratan; serta (5) pengambilan pasir urug yang merusak lokasi tambang pasir.\n\nPengecoh: reklamasi justru mengurangi mangrove. Kualitas air cenderung menurun. Reklamasi tidak menurunkan muka laut. Sedimentasi di muara cenderung meningkat karena aliran terhambat.",
      None),
    Q("Perhatikan data rencana alih fungsi lahan menjadi perumahan berikut. Dengan rumus V = C × curah hujan × luas (hujan dalam meter, luas dalam m²), tambahan volume limpasan akibat alih fungsi lahan tersebut adalah …",
      ["25.000 m³", "40.000 m³", "15.000 m³", "2.500 m³", "250.000 m³"],
      "Ubah satuan: hujan 100 mm = 0,1 m; luas 50 ha = 500.000 m².\n• Sebelum: V = 0,30 × 0,1 × 500.000 = 15.000 m³.\n• Sesudah: V = 0,80 × 0,1 × 500.000 = 40.000 m³.\n• Tambahan limpasan = 40.000 − 15.000 = 25.000 m³ (naik ±167%).\nTambahan limpasan ini berpotensi menimbulkan banjir di hilir bila tidak ditampung, sehingga pengembang perlu membangun kolam retensi, sumur resapan, atau taman hujan dengan kapasitas setara.\n\nPengecoh: 40.000 dan 15.000 m³ adalah volume sesudah dan sebelum, bukan tambahannya. 2.500 dan 250.000 m³ adalah kesalahan konversi satuan (1 ha = 10.000 m²; 1 mm = 0,001 m).",
      f_limpasan),
    Q("Kolam retensi dan taman hujan (rain garden) semakin banyak dibangun di kawasan perkotaan. Fungsi utamanya dalam pengelolaan air hujan adalah …",
      ["Menampung dan meresapkan limpasan untuk menurunkan debit puncak banjir", "Mempercepat air hujan dibuang ke laut melalui saluran beton",
       "Menyediakan air minum siap konsumsi tanpa pengolahan untuk warga", "Menambah luas permukaan kedap air agar jalan tidak becek",
       "Menggantikan seluruh fungsi sungai sebagai saluran drainase utama kota"],
      "Pendekatan pengelolaan air hujan berkelanjutan (misalnya konsep kota spons) berusaha menahan air hujan selama mungkin di lokasi turunnya. Kolam retensi menampung limpasan sementara saat hujan lebat lalu melepaskannya perlahan, sedangkan taman hujan dan sumur resapan meresapkan air ke dalam tanah. Keduanya menurunkan debit puncak banjir, mengisi air tanah, menyaring polutan, dan menambah ruang hijau kota.\n\nPengecoh: mempercepat pembuangan air justru memindahkan banjir ke hilir dan mengurangi imbuhan air tanah. Air kolam retensi tidak siap minum. Kolam retensi mengurangi, bukan menambah, permukaan kedap. Sungai tetap diperlukan sebagai saluran utama.",
      None),
]

P5 = [
    Q("Perhatikan grafik status beberapa batas planet berikut.\n\nBatas planet yang masih berada dalam ruang aman berdasarkan grafik adalah …",
      ["Penipisan ozon stratosfer", "Integritas biosfer", "Aliran nitrogen–fosfor", "Perubahan iklim global", "Pemakaian air tawar"],
      "Konsep batas-batas planet (planetary boundaries) menetapkan ambang aman bagi sistem Bumi agar tetap stabil. Pada grafik, nilai 1 berarti tepat di batas aman; nilai > 1 berarti batas telah terlampaui.\n• Integritas biosfer (±10), aliran nitrogen–fosfor (±2,5), perubahan iklim (±1,7), perubahan sistem lahan (±1,3), dan air tawar (±1,1) sudah melampaui batas.\n• Penipisan ozon stratosfer (±0,5) masih di dalam ruang aman, berkat keberhasilan Protokol Montreal mengurangi CFC.\n\nPengecoh: semua opsi lain berada di sebelah kanan garis batas aman. Integritas biosfer, yang berkaitan dengan laju kepunahan spesies, adalah yang paling jauh terlampaui.",
      f_planet),
    Q("Pandangan yang menyatakan bahwa tekanan penduduk justru mendorong petani menemukan teknik intensifikasi pertanian sehingga produksi pangan meningkat dikemukakan oleh …",
      ["Ester Boserup", "Thomas Robert Malthus", "Paul Ehrlich", "Club of Rome", "Garrett Hardin"],
      "Ester Boserup (1965) berpandangan optimis: kepadatan penduduk yang meningkat mendorong masyarakat berinovasi, misalnya irigasi, terasering, pupuk, rotasi tanaman, dan masa bera yang lebih singkat, sehingga produksi pangan dapat mengikuti pertumbuhan penduduk. \"Kebutuhan adalah ibu dari penemuan.\"\nSebaliknya, Thomas Robert Malthus (1798) berpandangan pesimis: penduduk tumbuh menurut deret ukur sedangkan pangan menurut deret hitung, sehingga kelaparan tak terhindarkan. Paul Ehrlich (The Population Bomb) dan Club of Rome (The Limits to Growth) termasuk kelompok neo-Malthusian. Garrett Hardin dikenal dengan konsep tragedi kepemilikan bersama.\n\nRevolusi Hijau sering dipakai sebagai contoh yang mendukung pandangan Boserup, walaupun menimbulkan masalah lingkungan baru.",
      None),
    Q("Perhatikan grafik model pertumbuhan menurut Malthus berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Garis X menggambarkan penduduk yang tumbuh menurut deret ukur", "Garis X menggambarkan pangan yang tumbuh menurut deret ukur",
       "Garis Y menggambarkan penduduk yang tumbuh menurut deret hitung", "Kedua garis tumbuh dengan laju yang sama sehingga tidak ada krisis",
       "Garis Y menggambarkan pangan yang tumbuh menurut deret ukur"],
      "Malthus menyatakan bahwa penduduk cenderung tumbuh menurut deret ukur (geometris): 1, 2, 4, 8, 16, …, sedangkan produksi pangan tumbuh menurut deret hitung (aritmetika): 1, 2, 3, 4, 5, …\nPada grafik, garis X naik makin curam (1 → 256 dalam 8 periode) sehingga menggambarkan penduduk. Garis Y naik secara linear (1 → 9) sehingga menggambarkan pangan. Kesenjangan yang makin lebar menurut Malthus akan memicu kelaparan, wabah, dan perang (positive checks), kecuali ada pengendalian kelahiran (preventive checks).\n\nPengecoh: opsi lain menukar penduduk dengan pangan atau jenis deretnya. Kedua garis jelas tumbuh dengan laju berbeda.",
      f_malthus),
    Q("Jejak ekologis rata-rata penduduk dunia sekitar 2,6 hektare global (gha) per orang, sedangkan biokapasitas Bumi sekitar 1,6 gha per orang. Jumlah Bumi yang diperlukan untuk menopang gaya hidup rata-rata tersebut adalah …",
      ["Sekitar 1,6 Bumi", "Sekitar 1,0 Bumi", "Sekitar 0,6 Bumi", "Sekitar 2,6 Bumi", "Sekitar 4,2 Bumi"],
      "Jumlah Bumi = jejak ekologis per kapita ÷ biokapasitas per kapita = 2,6 ÷ 1,6 ≈ 1,63 Bumi.\nArtinya umat manusia memakai sumber daya dan menghasilkan limbah (termasuk CO₂) sekitar 1,6 kali lebih cepat daripada kemampuan Bumi meregenerasinya. Kondisi ini disebut overshoot ekologis, dan tanggal ketika konsumsi tahunan melampaui kemampuan regenerasi Bumi disebut Earth Overshoot Day.\n\nPengecoh: 1,0 Bumi menganggap konsumsi seimbang. 0,6 Bumi adalah kebalikan perhitungan (1,6 ÷ 2,6). 2,6 Bumi hanya membaca jejak ekologis. 4,2 Bumi menjumlahkan kedua angka.",
      None),
    Q("Perhatikan grafik jejak ekologis dan biokapasitas per kapita empat negara berikut.\n\nNegara yang tergolong kreditor ekologis (cadangan ekologis positif) adalah …",
      ["Negara A", "Negara B", "Negara C", "Negara D", "Negara B dan C"],
      "Cadangan ekologis = biokapasitas − jejak ekologis.\n• A: 10,0 − 4,5 = +5,5 gha (kreditor ekologis).\n• B: 2,0 − 6,0 = −4,0 gha (debitor ekologis).\n• C: 1,1 − 1,7 = −0,6 gha (debitor ekologis).\n• D: 2,5 − 2,5 = 0 (seimbang).\nNegara A memiliki biokapasitas jauh lebih besar daripada konsumsinya, misalnya negara dengan hutan atau lahan luas dan penduduk relatif sedikit.\n\nPengecoh: B memiliki jejak ekologis terbesar sehingga defisitnya paling besar; negara seperti ini bergantung pada impor sumber daya dan penyerapan karbon global. C memiliki jejak kecil, tetapi biokapasitasnya lebih kecil lagi. D seimbang, belum kreditor.",
      f_jejak_eko),
    Q("Sebuah program merehabilitasi mangrove untuk melindungi pesisir dari abrasi, menyerap karbon biru, dan memulihkan habitat ikan. Program ini paling langsung mendukung SDGs nomor …",
      ["13 (Penanganan Perubahan Iklim) dan 14 (Ekosistem Lautan)", "4 (Pendidikan Berkualitas) dan 5 (Kesetaraan Gender)",
       "7 (Energi Bersih) dan 9 (Industri dan Inovasi)", "3 (Kehidupan Sehat) dan 16 (Perdamaian dan Keadilan)",
       "8 (Pekerjaan Layak) dan 10 (Berkurangnya Kesenjangan)"],
      "Rehabilitasi mangrove berkaitan langsung dengan:\n• SDG 13 (Penanganan Perubahan Iklim): mangrove menyerap dan menyimpan karbon biru dalam jumlah besar (mitigasi) serta melindungi pesisir dari kenaikan muka laut, gelombang, dan abrasi (adaptasi).\n• SDG 14 (Ekosistem Lautan): mangrove adalah ekosistem pesisir yang menjadi tempat pemijahan dan asuhan ikan serta menjaga kualitas perairan.\nProgram ini juga dapat mendukung SDG lain secara tidak langsung, misalnya SDG 1 dan 8 melalui ekowisata dan perikanan, tetapi yang paling langsung adalah 13 dan 14.\n\nPengecoh: SDG 4, 5, 7, 9, 3, 16, dan 10 tidak menjadi sasaran utama program rehabilitasi mangrove.",
      None),
    Q("Perhatikan grafik beberapa indikator aktivitas manusia berikut.\n\nGrafik tersebut paling tepat digunakan untuk mendukung gagasan …",
      ["Antroposen, dengan percepatan besar aktivitas manusia sejak sekitar 1950", "Zaman es baru yang dimulai akibat penurunan CO₂ sejak tahun 1900",
       "Revolusi Hijau yang menghentikan pertumbuhan penduduk dunia sejak 1950", "Kurva Kuznets yang menunjukkan penurunan pemakaian pupuk setelah 2000",
       "Teori Malthus bahwa penduduk tumbuh lebih lambat daripada pangan"],
      "Grafik menunjukkan tiga indikator, yaitu penduduk, CO₂ atmosfer, dan pemakaian pupuk, yang naik perlahan sebelum 1950 lalu melonjak tajam setelahnya. Fenomena ini dikenal sebagai Great Acceleration dan menjadi salah satu dasar gagasan Antroposen: zaman ketika aktivitas manusia menjadi kekuatan geologis utama yang mengubah sistem Bumi, misalnya iklim, siklus nitrogen, dan keanekaragaman hayati. Pertengahan abad ke-20 sering diusulkan sebagai awal Antroposen.\n\nPengecoh: CO₂ justru naik, bukan turun. Penduduk tidak berhenti tumbuh. Pemakaian pupuk tidak menurun pada grafik. Grafik tidak menunjukkan penduduk tumbuh lebih lambat daripada pangan.",
      f_akselerasi),
    Q("Pasangan perjanjian lingkungan internasional dan fokus pengaturannya yang tepat adalah …",
      ["Konvensi Basel – perpindahan limbah B3 lintas batas negara", "Konvensi Ramsar – perdagangan satwa dan tumbuhan liar",
       "CITES – perlindungan lahan basah penting internasional", "Protokol Montreal – pengurangan emisi gas rumah kaca negara maju",
       "Konvensi Minamata – perlindungan lapisan ozon dari CFC"],
      "Beberapa perjanjian lingkungan internasional:\n• Konvensi Basel (1989): mengatur perpindahan lintas batas limbah berbahaya (B3) dan pembuangannya.\n• Konvensi Ramsar (1971): perlindungan lahan basah penting internasional, misalnya Taman Nasional Berbak dan Sembilang.\n• CITES (1973): perdagangan internasional satwa dan tumbuhan liar yang terancam punah.\n• Protokol Montreal (1987): penghapusan bahan perusak ozon seperti CFC.\n• Protokol Kyoto (1997): pengurangan emisi gas rumah kaca negara maju.\n• Konvensi Minamata (2013): pengendalian merkuri.\nHanya pasangan Basel – limbah B3 lintas batas yang tepat.\n\nPengecoh: opsi lain menukar fokus Ramsar dan CITES, Montreal dan Kyoto, serta Minamata dan Montreal.",
      None),
    Q("Perhatikan alur penyusunan dokumen AMDAL berikut.\n\nDokumen yang seharusnya mengisi tanda tanya dan berisi rencana pengelolaan serta pemantauan dampak adalah …",
      ["RKL-RPL", "UKL-UPL", "SPPL", "KLHS", "RTRW"],
      "Alur AMDAL: penapisan (menentukan apakah rencana usaha wajib AMDAL) → Kerangka Acuan (KA, ruang lingkup kajian) → ANDAL (analisis dampak penting) → RKL-RPL (Rencana Pengelolaan Lingkungan dan Rencana Pemantauan Lingkungan) → penilaian dan persetujuan lingkungan.\nRKL-RPL berisi langkah-langkah untuk mengelola dampak (misalnya membangun IPAL) dan memantau kualitas lingkungan (misalnya mengukur kualitas air secara berkala).\n\nPengecoh: UKL-UPL adalah dokumen untuk usaha yang tidak wajib AMDAL tetapi berdampak. SPPL (Surat Pernyataan Kesanggupan Pengelolaan dan Pemantauan Lingkungan) untuk usaha berdampak kecil. KLHS (Kajian Lingkungan Hidup Strategis) dibuat untuk kebijakan, rencana, dan program pemerintah. RTRW adalah rencana tata ruang wilayah.",
      f_amdal),
    Q("Menurut UU No. 32 Tahun 2009, perusahaan yang usahanya menggunakan atau menghasilkan limbah B3 dan menimbulkan ancaman serius terhadap lingkungan bertanggung jawab mutlak atas kerugian yang terjadi. Asas ini disebut …",
      ["Tanggung jawab mutlak (strict liability) tanpa pembuktian kesalahan", "Praduga tak bersalah sehingga korban harus membuktikan kesalahan perusahaan",
       "Kehati-hatian yang hanya berlaku bagi proyek pemerintah", "Partisipasi masyarakat dalam penyusunan dokumen tata ruang",
       "Otonomi daerah dalam pengelolaan pajak lingkungan"],
      "UU No. 32 Tahun 2009 tentang Perlindungan dan Pengelolaan Lingkungan Hidup (Pasal 88) mengatur bahwa setiap orang yang tindakan, usaha, atau kegiatannya menggunakan B3, menghasilkan dan/atau mengelola limbah B3, dan/atau menimbulkan ancaman serius terhadap lingkungan hidup bertanggung jawab mutlak atas kerugian yang terjadi tanpa perlu pembuktian unsur kesalahan (strict liability). Asas ini memudahkan pemulihan lingkungan dan ganti rugi, misalnya dalam gugatan kebakaran lahan konsesi.\n\nPengecoh: asas praduga tak bersalah adalah prinsip hukum pidana dan bukan inti pasal ini. Asas kehati-hatian berlaku luas, tidak hanya untuk proyek pemerintah. Partisipasi masyarakat dan otonomi daerah adalah asas lain yang tidak menjelaskan tanggung jawab tanpa pembuktian kesalahan.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
