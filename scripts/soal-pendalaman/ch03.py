from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_rp(path):
    table([["Batu bara", "31,7 miliar ton", "0,775 miliar ton"], ["Minyak bumi", "2,4 miliar barel", "0,22 miliar barel"],
           ["Gas bumi", "41 TSCF", "2,4 TSCF"]],
          ["Komoditas", "Cadangan terbukti", "Produksi per tahun"], path,
          title="Cadangan dan produksi energi fosil Negara N (data ilustrasi)", col_w=[0.28, 0.36, 0.36])


def f_hubbert(path):
    yr = [1970, 1977, 1985, 1990, 1995, 2000, 2004, 2010, 2015, 2020]
    prod = [0.85, 1.68, 1.30, 1.45, 1.60, 1.40, 1.10, 0.95, 0.80, 0.70]
    cons = [0.15, 0.25, 0.50, 0.65, 0.90, 1.15, 1.25, 1.40, 1.55, 1.50]
    lines(yr, {"Produksi minyak": prod, "Konsumsi minyak": cons}, path,
          title="Produksi dan konsumsi minyak bumi Indonesia (juta barel/hari, disederhanakan)", ylabel="juta barel/hari",
          xlabel="Tahun", w=9)


GEOT = [(99.0, 1.9), (98.5, 3.2), (104.6, -5.3), (107.8, -7.1), (107.6, -7.2), (106.7, -6.7), (109.9, -7.2), (124.8, 1.3),
        (120.4, -8.7), (121.0, -8.8), (99.5, 0.7), (101.1, -1.5), (107.4, -7.25), (103.6, -4.2), (114.2, -8.0), (121.9, -8.7),
        (102.3, -3.3), (95.6, 5.4), (127.6, 1.2), (128.2, -3.6), (100.4, -0.6), (112.6, -7.9), (116.4, -8.4)]


def f_geotermal(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    xs, ys = zip(*GEOT)
    ax.plot(xs, ys, "o", ms=7, color=C["red"], mec="white", mew=0.8, label="Wilayah kerja panas bumi")
    ax.legend(loc="lower left", fontsize=9)
    ax.set_title("Sebaran wilayah kerja panas bumi di Indonesia (disederhanakan)")
    save(fig, path)


def f_falken(path):
    reg = ["Papua", "Kalimantan", "Sumatra", "Sulawesi", "Bali–Nusa Tenggara", "Jawa"]
    val = [300000, 110000, 25000, 22000, 4000, 1200]
    fig, ax = new(9, 4.4)
    ax.barh(reg, val, color=C["blue"]); ax.invert_yaxis(); ax.set_xscale("log")
    for i, v in enumerate(val):
        ax.text(v * 1.1, i, f"{v:,}".replace(",", "."), va="center", fontsize=10)
    for t, l in [(1700, "1.700"), (1000, "1.000"), (500, "500")]:
        ax.axvline(t, color=C["red"], ls="--", lw=1); ax.text(t, 5.45, l, color=C["red"], fontsize=9, ha="center", va="top", rotation=90, bbox=dict(fc="white", ec="none", pad=1))
    ax.set_xlim(200, 2e6); ax.set_xlabel("m³ per kapita per tahun (skala logaritmik)")
    ax.set_title("Ketersediaan air per kapita per pulau (data ilustrasi)")
    save(fig, path)


def f_hutan(path):
    yr = [2000, 2005, 2010, 2015, 2020]; v = [30.0, 28.9, 27.4, 25.8, 24.6]
    fig, ax = new(8, 4.2)
    ax.plot(yr, v, marker="o", lw=2.4, color=C["green"])
    for x, y in zip(yr, v):
        ax.text(x, y + 0.25, f"{y:.1f}".replace(".", ","), ha="center", fontsize=10)
    ax.set_ylim(22, 31.5); ax.set_xticks(yr); ax.set_ylabel("Luas tutupan hutan (juta ha)")
    ax.set_title("Luas tutupan hutan Pulau X"); ax.grid(axis="y", color="#E2E8F0")
    save(fig, path)


def f_laterit(path):
    fig, axs = plt.subplots(1, 2, figsize=(9, 5), gridspec_kw=dict(width_ratios=[1, 1.4]), sharey=True)
    a = axs[0]
    for z0, z1, c, n in [(0, 2, "#8B4513", "Tanah penutup"), (2, 10, "#C0392B", "Lapisan P"), (10, 22, "#D4AC0D", "Lapisan Q"),
                         (22, 30, "#4D5656", "Lapisan R")]:
        a.add_patch(Rectangle((0, z0), 1, z1 - z0, fc=c, ec="black")); a.text(0.5, (z0 + z1) / 2, n, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    a.set_xlim(0, 1); a.set_xticks([]); a.set_ylim(30, 0); a.set_ylabel("Kedalaman (m)")
    depth = [1, 4, 8, 12, 16, 20, 24, 28]; ni = [0.6, 1.0, 1.3, 1.9, 2.4, 2.1, 0.4, 0.3]
    axs[1].plot(ni, depth, marker="o", color=C["green"], lw=2.2); axs[1].set_xlabel("Kadar nikel (%)")
    axs[1].grid(color="#EDF2F7")
    fig.suptitle("Profil endapan nikel laterit di Sulawesi Tenggara (ilustrasi)", fontweight="bold")
    save(fig, path)


# ---- paket 1
def f_coal(path):
    rk = ["Gambut", "Lignit", "Sub-\nbituminus", "Bituminus", "Antrasit"]
    bars(rk, {"Kandungan karbon (%)": [55, 65, 73, 84, 93], "Kandungan air (%)": [75, 40, 25, 8, 3]}, path,
         title="Perubahan sifat bahan dalam proses pembatubaraan (nilai rata-rata ilustrasi)", ylabel="%", values=True,
         ylim=(0, 105), w=9.5)


def f_antiklin(path):
    fig, ax = blank(9.5, 4.8, (0, 100), (0, 50))
    x = np.linspace(0, 100, 300)
    def lay(off):
        return off + 14 * np.exp(-((x - 50) / 22) ** 2)
    ax.fill_between(x, 0, lay(10), color="#A0AEC0")
    ax.fill_between(x, lay(10), lay(18), color="#F6E05E")
    ax.fill_between(x, lay(18), lay(26), color="#B794F4")
    ax.fill_between(x, lay(26), 50, color="#E2E8F0")
    # fluids inside reservoir
    top = lay(18); g = (x > 36) & (x < 64)
    ax.fill_between(x[g], np.maximum(lay(10)[g], 28.5), top[g], color="#FC8181", alpha=0.85)
    o = (x > 28) & (x < 72)
    ax.fill_between(x[o], np.maximum(lay(10)[o], 24), np.minimum(top[o], 28.5), color="#1A202C", alpha=1)
    ax.text(8, 5, "serpih", fontsize=10); ax.text(8, 13.5, "batu pasir berpori", fontsize=10)
    ax.text(8, 21.5, "serpih kedap (batuan penutup)", fontsize=10)
    for n, (px, py) in {"K": (50, 30), "L": (36, 25.5), "M": (80, 14), "N": (50, 6)}.items():
        ax.plot(px, py, "o", ms=8, color=C["blue"], mec="white"); ax.text(px + 1.5, py + 1, n, fontsize=14, fontweight="bold", color=C["blue"], bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Penampang struktur antiklin (warna merah = gas, hitam = minyak)")
    save(fig, path)


def f_bauran(path):
    fig, ax = plt.subplots(figsize=(7, 5))
    d = [40, 30, 17, 13]; lab = ["Batu bara", "Minyak bumi", "Gas bumi", "EBT"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=["#4A5568", "#DD6B20", "#3182CE", "#38A169"], startangle=90,
           wedgeprops=dict(ec="white"), textprops=dict(fontsize=11))
    ax.set_title("Bauran energi primer Indonesia tahun T (disederhanakan)")
    save(fig, path)


def f_beban(path):
    h = np.arange(0, 25)
    load = 28 + 3 * np.sin((h - 9) / 24 * 2 * np.pi) + 9 * np.exp(-((h - 19.5) / 2.0) ** 2)
    fig, ax = new(9, 4.4)
    ax.fill_between(h, 0, 25, color="#CBD5E0", label="beban dasar")
    ax.fill_between(h, 25, load, color="#FBD38D", label="beban menengah–puncak")
    ax.plot(h, load, color=C["red"], lw=2.2)
    ax.set_xticks(range(0, 25, 2)); ax.set_xlabel("Jam"); ax.set_ylabel("Beban (GW)"); ax.set_ylim(0, 42)
    ax.legend(loc="upper left", frameon=False)
    ax.set_title("Kurva beban harian sistem kelistrikan Jawa–Bali (ilustrasi)")
    save(fig, path)


def f_lpg(path):
    bars(["Produksi dalam negeri", "Konsumsi nasional"], {"Juta ton": [1.9, 8.6]}, path, title="LPG Indonesia dalam satu tahun",
         ylabel="juta ton", values=True, ylim=(0, 10), colors=[C["orange"]], w=7)


def f_emisi(path):
    bars(["PLTU batu bara", "PLTGU gas", "PLTP panas bumi", "PLTS surya"], {"g CO₂/kWh": [1000, 400, 50, 40]}, path,
         title="Faktor emisi rata-rata per kWh listrik (ilustrasi)", ylabel="gram CO₂ per kWh", values=True, ylim=(0, 1150),
         colors=[C["gray"]], w=8.5)


# ---- paket 2
def f_debit(path):
    bars(BULAN3, {"Tahun normal": [80, 85, 82, 70, 60, 52, 48, 46, 45, 55, 68, 78],
                   "Tahun El Niño": [78, 80, 75, 60, 45, 35, 28, 22, 20, 24, 40, 62]}, path,
         title="Debit masuk turbin PLTA (m³/s); tinggi jatuh 100 m", ylabel="m³/s", w=9.5)


def f_irr(path):
    bars(["NTT", "NTB", "Jawa Timur", "Kalimantan Barat", "Sumatra Barat", "Papua (pegunungan)"],
         {"kWh/m²/hari": [5.8, 5.5, 4.9, 4.6, 4.5, 4.2]}, path, title="Rata-rata radiasi Matahari harian (ilustrasi)",
         ylabel="kWh/m²/hari", values=True, ylim=(0, 7), colors=[C["yellow"]], rot=15, w=9)


def f_payback(path):
    table([["Biaya pemasangan PLTS atap 2 kWp", "Rp15.000.000"], ["Tagihan listrik per bulan sebelum PLTS", "Rp800.000"],
           ["Tagihan listrik per bulan sesudah PLTS", "Rp550.000"], ["Biaya perawatan", "diabaikan"]],
          ["Komponen", "Nilai"], path, title="Data rumah tangga yang memasang PLTS atap", col_w=[0.62, 0.38])


def f_otec(path):
    z = np.array([0, 20, 40, 60, 100, 200, 400, 600, 800, 1000])
    tA = [29.5, 29.3, 29.0, 28.6]
    tB = [29.0, 28.8, 28.0, 27.0, 24.0, 15.0, 9.0, 7.0, 5.8, 5.0]
    fig, ax = new(7, 5.2)
    ax.plot(tA, z[:4], marker="s", lw=2.4, color=C["orange"], label="Lokasi A (dasar laut 60 m)")
    ax.plot(tB, z, marker="o", lw=2.4, color=C["blue"], label="Lokasi B (dasar laut > 1.500 m)")
    ax.invert_yaxis(); ax.set_xlabel("Suhu air laut (°C)"); ax.set_ylabel("Kedalaman (m)"); ax.legend(frameon=False, loc="lower right")
    ax.grid(color="#EDF2F7"); ax.set_title("Profil suhu laut dua lokasi pesisir")
    save(fig, path)


def f_cf(path):
    bars(["PLTS", "PLTB (angin)", "PLTA", "PLTU", "PLTP"], {"Faktor kapasitas (%)": [18, 30, 45, 70, 90]}, path,
         title="Faktor kapasitas rata-rata jenis pembangkit (ilustrasi)", ylabel="%", values=True, ylim=(0, 100),
         colors=[C["teal"]], w=8)


# ---- paket 3
def f_airbumi(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.6))
    axs[0].pie([97.5, 2.5], labels=["Air asin\n97,5%", "Air tawar\n2,5%"], colors=[C["blue"], C["lblue"]], startangle=90,
               wedgeprops=dict(ec="white"))
    axs[0].set_title("Seluruh air di Bumi")
    axs[1].pie([68.7, 30.1, 1.2], labels=["K\n68,7%", "L\n30,1%", "M\n1,2%"], colors=["#E2E8F0", "#B7791F", "#63B3ED"],
               startangle=90, wedgeprops=dict(ec="white"))
    axs[1].set_title("Komposisi air tawar")
    save(fig, path)


def f_akuifer(path):
    fig, ax = blank(10, 5, (0, 100), (0, 56))
    x = np.linspace(0, 100, 200)
    surf = 40 + 12 * np.exp(-((x - 5) / 18) ** 2)
    ax.fill_between(x, 0, 8, color="#4A5568")
    ax.fill_between(x, 8, 16 + 10 * np.exp(-((x - 5) / 20) ** 2), color="#90CDF4")
    lay2 = 16 + 10 * np.exp(-((x - 5) / 20) ** 2)
    ax.fill_between(x, lay2, lay2 + 6, color="#8B5A2B")
    ax.fill_between(x, lay2 + 6, surf, color="#F6E05E")
    ax.text(70, 11, "akuifer tertekan (pasir)", fontsize=10); ax.text(70, 21.5, "lapisan kedap (lempung)", fontsize=10, color="white")
    ax.text(70, 30, "akuifer bebas", fontsize=10)
    ax.text(3, 54, "daerah resapan\n(pegunungan)", fontsize=9)
    for n, xx, d, c in [("W1", 60, 31, C["gray"]), ("W2", 80, 9, C["blue"])]:
        top = 40 + 12 * np.exp(-((xx - 5) / 18) ** 2)
        ax.plot([xx, xx], [d, top + 2], color="black", lw=3); ax.text(xx + 1, top + 2.5, n, fontsize=13, fontweight="bold")
    ax.annotate("", xy=(84, 49), xytext=(80, 42.5), arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=2))
    ax.text(85, 49, "air memancar sendiri", fontsize=9, color=C["blue"])
    ax.plot(x, 36 + 10 * np.exp(-((x - 5) / 18) ** 2), color=C["blue"], ls=":", lw=1.5)
    ax.text(40, 37.5, "muka air tanah bebas", fontsize=8.5, color=C["blue"])
    ax.set_title("Penampang hidrogeologi sebuah cekungan air tanah")
    save(fig, path)


def f_aral(path):
    yr = [1960, 1970, 1980, 1990, 2000, 2010]
    lines(yr, {"Luas permukaan (ribu km²)": [68, 60, 51, 37, 24, 14]}, path, title="Luas permukaan Laut Aral",
          ylabel="ribu km²", xlabel="Tahun", w=8)


def f_prov(path):
    table([["K", "12", "10"], ["L", "30", "8"], ["M", "4", "9"]],
          ["Provinsi", "Air terbarukan (km³/tahun)", "Penduduk (juta jiwa)"], path,
          title="Ketersediaan air dan penduduk tiga provinsi", col_w=[0.2, 0.45, 0.35])


def f_intrusi(path):
    yr = np.arange(2010, 2025)
    mat = -2 - 0.9 * (yr - 2010)
    cl = 120 + 18 * (yr - 2010) ** 1.3
    fig, ax = new(9, 4.4)
    ax.plot(yr, mat, color=C["blue"], marker="o", lw=2, label="Muka air tanah (m dpl)")
    ax.set_ylabel("Muka air tanah (m dpl)", color=C["blue"]); ax.axhline(0, color="#A0AEC0", lw=1)
    ax2 = ax.twinx(); ax2.plot(yr, cl, color=C["red"], marker="s", lw=2, label="Kadar klorida (mg/L)")
    ax2.set_ylabel("Klorida (mg/L)", color=C["red"]); ax2.spines["top"].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="lower left", frameon=False)
    ax.set_title("Sumur pantau 1 km dari pantai Kota S")
    save(fig, path)


def f_jejak(path):
    bars(["Daging sapi", "Daging ayam", "Beras", "Gandum", "Sayuran"], {"Liter per kg": [15400, 4300, 2500, 1800, 300]}, path,
         title="Jejak air rata-rata beberapa bahan pangan", ylabel="liter per kg", values=True, ylim=(0, 17500),
         colors=[C["blue"]], w=8.5)


# ---- paket 4
def f_hutan2(path):
    bars(["Kabupaten P", "Kabupaten Q"], {"2010": [800, 300], "2020": [680, 240]}, path,
         title="Luas tutupan hutan (ribu ha)", ylabel="ribu ha", values=True, ylim=(0, 900), w=7.5)


def f_msy(path):
    B = np.linspace(0, 1, 200); G = 4 * B * (1 - B)
    fig, ax = new(8, 4.6)
    ax.plot(B, G, color=C["blue"], lw=2.5)
    for n, b in {"A": 0.15, "B": 0.32, "C": 0.5, "D": 0.75, "E": 0.95}.items():
        ax.plot(b, 4 * b * (1 - b), "o", ms=9, color=C["red"]); ax.text(b, 4 * b * (1 - b) + 0.06, n, ha="center", fontsize=13, fontweight="bold")
    ax.set_xticks([0, 0.5, 1]); ax.set_xticklabels(["0", "K/2", "K"]); ax.set_yticks([])
    ax.set_xlabel("Biomassa stok ikan"); ax.set_ylabel("Pertumbuhan stok per tahun"); ax.set_ylim(0, 1.18)
    ax.set_title("Model surplus produksi stok ikan")
    save(fig, path)


WPP = {"WPP 711": 1.2, "WPP 712": 1.4, "WPP 713": 0.9, "WPP 714": 0.6, "WPP 715": 0.7, "WPP 718": 1.1}


def f_wpp(path):
    fig, ax = new(8.5, 4.4)
    vals = list(WPP.values())
    ax.bar(list(WPP), vals, color=[C["red"] if v >= 1 else (C["yellow"] if v >= 0.5 else C["green"]) for v in vals])
    for i, v in enumerate(vals):
        ax.text(i, v + 0.03, f"{v:.1f}".replace(".", ","), ha="center", fontsize=10)
    ax.axhline(1, color="black", ls="--", lw=1); ax.axhline(0.5, color="#718096", ls=":", lw=1)
    ax.set_ylabel("Tingkat pemanfaatan (E)"); ax.set_ylim(0, 1.6)
    ax.set_title("Tingkat pemanfaatan ikan demersal per WPP (ilustrasi)")
    save(fig, path)


def f_unclos(path):
    fig, ax = blank(10, 4.2, (0, 100), (0, 40))
    ax.add_patch(Rectangle((0, 0), 12, 40, fc=C["land"], ec="#8D7B5A")); ax.text(6, 20, "Daratan", ha="center", rotation=90)
    ax.add_patch(Rectangle((12, 0), 88, 40, fc=C["sea"]))
    ax.plot([12, 12], [0, 40], color="black", lw=2); ax.text(12.5, 37, "garis pangkal", fontsize=9)
    for x, lab in [(20, "12 mil laut"), (28, "24 mil laut"), (92, "200 mil laut")]:
        ax.plot([x, x], [0, 34], color="#2D3748", ls="--", lw=1.4); ax.text(x, 35, lab, ha="center", fontsize=9)
    for t, x0, x1 in [("P", 12, 20), ("Q", 20, 28), ("R", 28, 92)]:
        ax.annotate("", xy=(x1, 16), xytext=(x0, 16), arrowprops=dict(arrowstyle="<->", lw=1.4))
        ax.text((x0 + x1) / 2, 19, t, ha="center", fontsize=15, fontweight="bold", color=C["blue"])
    ax.set_title("Zona-zona laut menurut UNCLOS 1982")
    save(fig, path)


def f_cpue(path):
    yr = np.arange(2010, 2024)
    eff = 1000 + 120 * (yr - 2010)
    catch = 50000 + 2500 * (yr - 2010) - 260 * (yr - 2010) ** 2
    cpue = catch / eff
    fig, ax = new(9, 4.4)
    ax.bar(yr, eff, color="#CBD5E0", label="Upaya tangkap (trip kapal)")
    ax.set_ylabel("Upaya (trip)")
    ax2 = ax.twinx(); ax2.plot(yr, cpue, color=C["red"], marker="o", lw=2.2, label="Hasil tangkapan per upaya (ton/trip)")
    ax2.set_ylabel("CPUE (ton/trip)", color=C["red"]); ax2.spines["top"].set_visible(False); ax2.set_ylim(0, 60)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False)
    ax.set_title("Upaya tangkap dan CPUE ikan kakap di sebuah WPP (ilustrasi)")
    save(fig, path)


# ---- paket 5
def f_nikel(path):
    bars(["2014\n(ekspor bijih)", "2017", "2020", "2022\n(produk olahan)"], {"Nilai ekspor (miliar USD)": [1.0, 4.5, 11.0, 33.0]},
         path, title="Nilai ekspor komoditas berbasis nikel (ilustrasi)", ylabel="miliar USD", values=True, ylim=(0, 38),
         colors=[C["teal"]], w=8)


def f_tev(path):
    comps = ["Kayu & bahan bangunan", "Perikanan", "Pelindung pantai", "Penyerapan karbon", "Nilai keberadaan"]
    vals = [2, 8, 15, 5, 2]
    cols = ["#8B5A2B", "#3182CE", "#2C7A7B", "#38A169", "#805AD5"]
    fig, ax = new(9, 3.6)
    left = 0
    for c, v, col in zip(comps, vals, cols):
        ax.barh([0], [v], left=left, color=col, ec="white"); ax.text(left + v / 2, 0, f"{v}", ha="center", va="center", color="white", fontsize=12, fontweight="bold")
        left += v
    ax.set_yticks([]); ax.set_xlabel("juta rupiah per hektare per tahun"); ax.set_xlim(0, 33)
    legend_patches(ax, list(zip(comps, cols)), loc="upper center", ncol=3, fs=9)
    ax.set_ylim(-0.6, 1.4)
    ax.set_title("Komponen nilai ekonomi ekosistem mangrove Desa B")
    save(fig, path)


def f_pltsskor(path):
    table([["Radiasi Matahari", "0,40", "5", "4", "5"], ["Kemiringan lahan", "0,20", "4", "5", "3"],
           ["Jarak ke jaringan listrik", "0,25", "3", "5", "4"], ["Tutupan lahan", "0,15", "4", "3", "5"]],
          ["Kriteria", "Bobot", "Lokasi A", "Lokasi B", "Lokasi C"], path,
          title="Skor kesesuaian lokasi PLTS (1 = buruk, 5 = sangat baik)", col_w=[0.36, 0.13, 0.17, 0.17, 0.17])


def f_nexus(path):
    fig, ax = blank(8, 5.6, (0, 100), (0, 80))
    pos = {"AIR": (50, 70), "ENERGI": (15, 12), "PANGAN": (85, 12)}
    for n, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 10, fc="#EBF8FF", ec=C["blue"], lw=1.8)); ax.text(x, y, n, ha="center", va="center", fontsize=12, fontweight="bold")
    arrow(ax, 22, 21, 43, 61, color=C["gray"]); ax.text(25, 44, "1", fontsize=15, fontweight="bold", color=C["red"])
    arrow(ax, 57, 61, 78, 21, color=C["gray"]); ax.text(73, 44, "2", fontsize=15, fontweight="bold", color=C["red"])
    arrow(ax, 75, 10, 25, 10, color=C["gray"]); ax.text(50, 4, "3", fontsize=15, fontweight="bold", color=C["red"])
    ax.text(50, 30, "1: energi → air\n2: air → pangan\n3: pangan → energi", ha="center", fontsize=10, color=C["gray"])
    ax.set_title("Keterkaitan nexus air–energi–pangan")
    save(fig, path)


def f_curse(path):
    pts = [("A", 8, 4.2), ("B", 12, 3.8), ("C", 18, 3.5), ("D", 25, 2.6), ("E", 33, 2.0), ("F", 41, 1.4), ("G", 52, 0.8), ("H", 60, 0.5)]
    scatter(pts, path, title="Ketergantungan ekspor SDA dan pertumbuhan ekonomi (ilustrasi)",
            xlabel="Porsi ekspor SDA mentah terhadap PDB (%)", ylabel="Pertumbuhan PDB per kapita (%/tahun)", fit=True)


# ============================ questions ============================
P0 = [
    Q("Perhatikan tabel cadangan dan produksi energi fosil Negara N berikut. Dengan rasio cadangan terhadap produksi (R/P), komoditas yang paling cepat habis dan perkiraan umurnya adalah …",
      ["Minyak bumi, sekitar 11 tahun", "Gas bumi, sekitar 17 tahun", "Batu bara, sekitar 41 tahun", "Minyak bumi, sekitar 0,09 tahun",
       "Gas bumi, sekitar 6 tahun"],
      "Umur cadangan (rasio R/P) = cadangan ÷ produksi per tahun.\n• Batu bara: 31,7 ÷ 0,775 ≈ 40,9 tahun.\n• Minyak bumi: 2,4 ÷ 0,22 ≈ 10,9 tahun.\n• Gas bumi: 41 ÷ 2,4 ≈ 17,1 tahun.\nMinyak bumi paling cepat habis (±11 tahun).\n\nPengecoh: 0,09 tahun muncul bila produksi dibagi cadangan (terbalik). Gas bumi bukan yang tercepat. Ingat pula bahwa rasio R/P bukan ramalan pasti: angka ini berubah bila ditemukan cadangan baru, teknologi meningkatkan perolehan, atau tingkat produksi berubah.",
      f_rp),
    Q("Sebuah danau dimanfaatkan bebas oleh banyak nelayan tanpa aturan kuota. Setiap nelayan menambah alat tangkap karena keuntungannya dinikmati sendiri, sedangkan kerugian akibat stok ikan turun ditanggung bersama. Akhirnya stok ikan runtuh. Konsep yang menjelaskan peristiwa ini adalah …",
      ["Tragedi kepemilikan bersama (commons)", "Kutukan sumber daya (resource curse)", "Kurva puncak produksi Hubbert",
       "Peningkatan daya dukung lingkungan", "Hilirisasi sumber daya perikanan"],
      "Tragedy of the commons (Garrett Hardin, 1968) menggambarkan sumber daya milik bersama yang terbuka bagi semua orang. Setiap pengguna terdorong memaksimalkan keuntungan pribadinya, sedangkan biaya kerusakan dibagi kepada semua pihak. Akumulasi perilaku rasional individu itu justru merusak sumber daya. Solusinya antara lain aturan akses dan kuota, hak kelola komunitas (misalnya sasi di Maluku dan awig-awig di Lombok), atau pengelolaan bersama oleh pemerintah dan masyarakat.\n\nPengecoh: kutukan sumber daya berkaitan dengan ketergantungan ekonomi negara pada ekspor SDA. Kurva Hubbert menjelaskan puncak produksi sumber daya tak terbarukan. Daya dukung justru menurun. Hilirisasi adalah pengolahan bahan mentah menjadi produk bernilai tambah.",
      None),
    Q("Perhatikan grafik produksi dan konsumsi minyak bumi Indonesia berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Indonesia menjadi pengimpor bersih minyak sejak awal 2000-an karena produksi menurun dan konsumsi naik",
       "Indonesia menjadi pengimpor bersih minyak sejak akhir 1970-an karena puncak produksi sudah lewat",
       "Indonesia tetap pengekspor bersih minyak karena produksi selalu di atas konsumsi hingga 2020",
       "Produksi minyak terus naik setelah tahun 1995 sehingga impor hanya terjadi pada tahun 2010-an",
       "Konsumsi minyak menurun sejak tahun 2000 sehingga kebutuhan impor semakin kecil"],
      "Grafik menunjukkan produksi memuncak sekitar 1977 (±1,7 juta barel/hari) dan sekitar 1995, lalu terus menurun. Sebaliknya konsumsi naik terus seiring pertumbuhan penduduk dan ekonomi. Kedua garis berpotongan di awal 2000-an (antara 2000 dan 2004); sejak itu konsumsi melebihi produksi sehingga Indonesia menjadi pengimpor bersih minyak (net oil importer) dan keluar dari OPEC pada 2008.\nPola produksi yang naik, memuncak, lalu turun ini sesuai dengan model kurva Hubbert untuk sumber daya tak terbarukan.\n\nPengecoh: pada akhir 1970-an produksi masih jauh di atas konsumsi. Produksi setelah 1995 menurun, bukan naik. Konsumsi tidak menurun sejak 2000.",
      f_hubbert),
    Q("Sebuah PLTA memiliki debit 50 m³/s, tinggi jatuh air 80 m, dan efisiensi 85%. Dengan P = ρ × g × Q × H × η (ρ = 1.000 kg/m³, g = 9,8 m/s²), daya listrik yang dihasilkan adalah sekitar …",
      ["33,3 MW", "39,2 MW", "3,3 MW", "333 MW", "28,9 MW"],
      "P = 1.000 × 9,8 × 50 × 80 × 0,85\n  = 9.800 × 4.000 × 0,85\n  = 39.200.000 × 0,85 = 33.320.000 W ≈ 33,3 MW.\n\nPengecoh: 39,2 MW adalah daya sebelum dikalikan efisiensi. 3,3 MW dan 333 MW adalah kesalahan konversi watt ke megawatt (1 MW = 1.000.000 W). 28,9 MW tidak sesuai perhitungan (misalnya memakai efisiensi 0,85 dua kali sebagian). Rumus ini menunjukkan bahwa daya PLTA sebanding dengan debit dan tinggi jatuh; karena itu lokasi ideal PLTA adalah sungai berdebit besar dengan beda tinggi besar, misalnya di wilayah pegunungan.",
      None),
    Q("Perhatikan peta sebaran wilayah kerja panas bumi di Indonesia berikut.\n\nAlasan Pulau Kalimantan hampir tidak memiliki wilayah kerja panas bumi adalah …",
      ["Kalimantan tidak berada pada jalur busur gunung api hasil subduksi", "Curah hujan di Kalimantan terlalu tinggi sehingga panas bumi padam",
       "Kalimantan tertutup hutan lebat sehingga panas bumi tidak dapat dipetakan", "Batuan di Kalimantan terlalu muda untuk menyimpan panas",
       "Kalimantan terletak tepat di khatulistiwa sehingga panas Matahari dominan"],
      "Sumber panas bumi berasal dari magma dangkal di bawah gunung api. Di Indonesia, gunung api terbentuk pada busur vulkanik akibat subduksi Lempeng Indo-Australia dan lempeng di Pasifik barat. Busur ini melintasi Sumatra, Jawa, Bali, Nusa Tenggara, Sulawesi Utara, dan Maluku, sehingga titik-titik wilayah kerja panas bumi berderet di sepanjang pulau-pulau tersebut. Kalimantan berada di bagian stabil Lempeng Eurasia (Paparan Sunda) dan tidak memiliki gunung api aktif, sehingga potensinya sangat kecil.\n\nPengecoh: curah hujan tidak memadamkan panas bumi; justru air hujan mengisi reservoir. Hutan tidak menghalangi survei geologi. Batuan Kalimantan umumnya tua, dan usia batuan bukan faktor utama. Panas Matahari tidak terkait dengan energi panas bumi.",
      f_geotermal),
    Q("Sebuah PLTS berkapasitas 10 MW menghasilkan 15.768 MWh listrik dalam setahun. Faktor kapasitas PLTS tersebut adalah …",
      ["18%", "1,8%", "55%", "64%", "180%"],
      "Faktor kapasitas = produksi aktual ÷ produksi maksimum teoretis.\nProduksi maksimum = kapasitas × 8.760 jam = 10 MW × 8.760 = 87.600 MWh.\nFaktor kapasitas = 15.768 ÷ 87.600 = 0,18 = 18%.\n\nNilai ini wajar untuk PLTS karena hanya menghasilkan listrik pada siang hari dan intensitasnya dipengaruhi awan. Bandingkan dengan PLTP yang dapat beroperasi hampir terus-menerus (faktor kapasitas ±80–90%).\n\nPengecoh: 1,8% dan 180% adalah kesalahan desimal. 55% dan 64% berasal dari salah memakai jumlah jam (misalnya 24 jam × 365 hari dihitung keliru atau hanya jam siang).",
      None),
    Q("Perhatikan grafik ketersediaan air per kapita per pulau berikut. Indeks Falkenmark: > 1.700 m³ aman; 1.000–1.700 m³ stres air; 500–1.000 m³ kelangkaan air; < 500 m³ kelangkaan absolut.\n\nKondisi Pulau Jawa adalah …",
      ["Stres air, karena ketersediaannya di antara 1.000 dan 1.700 m³", "Aman, karena seluruh pulau di Indonesia beriklim tropis basah",
       "Kelangkaan absolut, karena ketersediaannya di bawah 500 m³", "Kelangkaan air, karena ketersediaannya di antara 500 dan 1.000 m³",
       "Aman, karena curah hujan tahunan Jawa lebih dari 2.000 mm"],
      "Ketersediaan air per kapita Jawa ±1.200 m³/tahun, berada di antara garis 1.000 dan 1.700, sehingga tergolong stres air. Penyebabnya bukan curah hujan yang kecil, melainkan jumlah penduduk yang sangat besar (lebih dari separuh penduduk Indonesia) dibandingkan luas pulau dan volume air terbarukan. Sebaliknya Papua dan Kalimantan memiliki ketersediaan sangat besar karena penduduknya sedikit.\n\nPengecoh: iklim tropis basah dan curah hujan tinggi tidak otomatis menjamin kecukupan air per kapita. Nilai Jawa tidak berada di bawah 1.000 m³ maupun 500 m³. Perhatikan juga bahwa grafik memakai skala logaritmik, sehingga panjang batang tidak sebanding linear dengan nilainya.",
      f_falken),
    Q("Sebuah stok ikan memiliki laju pertumbuhan intrinsik r = 0,6 per tahun dan daya dukung K = 2.000.000 ton. Dengan MSY = r × K ÷ 4 dan Jumlah Tangkapan yang Diperbolehkan (JTB) sebesar 80% dari MSY, besar JTB adalah …",
      ["240.000 ton per tahun", "300.000 ton per tahun", "1.200.000 ton per tahun", "960.000 ton per tahun", "1.600.000 ton per tahun"],
      "1) MSY = 0,6 × 2.000.000 ÷ 4 = 1.200.000 ÷ 4 = 300.000 ton per tahun.\n2) JTB = 80% × 300.000 = 240.000 ton per tahun.\nMSY dicapai ketika biomassa stok sekitar setengah daya dukung (K/2), karena saat itu pertumbuhan stok paling cepat. JTB ditetapkan lebih rendah dari MSY sebagai prinsip kehati-hatian untuk mengantisipasi ketidakpastian data dan variasi lingkungan.\n\nPengecoh: 300.000 adalah MSY, belum dikalikan 80%. 1.200.000 adalah r × K tanpa dibagi 4. 960.000 adalah 80% dari r × K. 1.600.000 adalah 80% dari K.",
      None),
    Q("Perhatikan grafik luas tutupan hutan Pulau X berikut.\n\nLaju rata-rata kehilangan hutan per tahun pada periode 2000–2020 adalah …",
      ["270.000 ha per tahun", "1.080.000 ha per tahun", "216.000 ha per tahun", "18% per tahun", "540.000 ha per tahun"],
      "Kehilangan hutan = 30,0 − 24,6 = 5,4 juta ha dalam 20 tahun (2000–2020 adalah 20 selang tahun).\nLaju rata-rata = 5,4 juta ÷ 20 = 0,27 juta ha = 270.000 ha per tahun.\nSecara persentase, total kehilangan 5,4 ÷ 30,0 × 100% = 18% dalam 20 tahun, atau rata-rata ±0,9% per tahun.\n\nPengecoh: 1.080.000 ha membagi dengan 5 (jumlah titik data, bukan selang tahun). 216.000 ha membagi dengan 25. 18% adalah total perubahan 20 tahun, bukan per tahun. 540.000 ha membagi dengan 10. Ingat rumus: rata-rata kenaikan/penurunan tahunan = selisih ÷ jumlah selang tahun.",
      f_hutan),
    Q("Perhatikan profil endapan nikel laterit dan grafik kadar nikel berikut.\n\nLapisan yang menjadi sasaran utama penambangan bijih nikel kadar tinggi beserta penjelasannya adalah …",
      ["Lapisan Q (saprolit), tempat nikel terlindi dari atas mengendap kembali", "Lapisan P (limonit), karena paling dekat permukaan sehingga kadarnya tertinggi",
       "Lapisan R (batuan dasar ultrabasa), karena merupakan sumber asli nikel", "Tanah penutup, karena mengandung bahan organik yang mengikat nikel",
       "Lapisan P dan R, karena keduanya mengandung besi dalam jumlah besar"],
      "Nikel laterit terbentuk dari pelapukan kimia batuan ultrabasa (peridotit) di iklim tropis lembap, seperti di Sulawesi dan Halmahera. Air hujan melarutkan unsur mudah larut (Mg, Si) dan juga nikel dari bagian atas. Nikel terbawa ke bawah dan mengendap kembali di zona saprolit. Grafik menunjukkan kadar Ni tertinggi (±2,1–2,4%) pada kedalaman 12–20 m, yaitu lapisan Q (saprolit). Lapisan limonit di atasnya (P) kaya besi tetapi kadar nikelnya lebih rendah (±1–1,3%) dan biasanya diolah dengan teknologi HPAL untuk bahan baterai.\n\nPengecoh: kedekatan dengan permukaan tidak menentukan kadar. Batuan dasar segar memiliki kadar nikel rendah (±0,3%). Tanah penutup tidak menjadi sasaran utama.",
      f_laterit),
]

P1 = [
    Q("Perhatikan grafik perubahan sifat bahan dalam proses pembatubaraan berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Semakin tinggi peringkat batu bara, kadar karbon naik dan kadar air turun", "Lignit memiliki nilai kalori tertinggi karena kadar airnya paling besar",
       "Antrasit terbentuk paling cepat karena berada paling dekat permukaan tanah", "Kadar karbon dan kadar air naik bersamaan seiring bertambahnya tekanan",
       "Gambut adalah batu bara peringkat tertinggi karena masih banyak air"],
      "Pembatubaraan (coalification) adalah perubahan sisa tumbuhan menjadi batu bara akibat penimbunan, tekanan, dan panas selama jutaan tahun. Urutannya gambut → lignit → sub-bituminus → bituminus → antrasit. Grafik menunjukkan kadar karbon naik dari ±55% menjadi ±93%, sedangkan kadar air turun dari ±75% menjadi ±3%. Semakin tinggi peringkatnya, semakin tinggi nilai kalorinya.\nBatu bara Indonesia (terutama Kalimantan dan Sumatra Selatan) didominasi lignit–sub-bituminus berumur Tersier yang relatif muda, sehingga kadar airnya tinggi dan kalorinya sedang–rendah.\n\nPengecoh: kadar air tinggi justru menurunkan nilai kalori. Antrasit terbentuk paling lama pada kondisi panas dan tekanan tinggi. Kadar air turun, bukan naik. Gambut belum tergolong batu bara.",
      f_coal),
    Q("Perhatikan penampang struktur antiklin berikut.\n\nTitik pengeboran yang paling tepat untuk memperoleh gas bumi adalah …",
      ["K, di puncak antiklin tepat di bawah batuan penutup", "L, di sayap antiklin pada zona minyak bumi",
       "M, di sayap jauh tempat batu pasir terisi air", "N, di lapisan serpih di bawah batu pasir reservoir",
       "L dan M, karena keduanya berada di batu pasir berpori"],
      "Minyak dan gas bumi bermigrasi dari batuan induk melalui batuan berpori (reservoir), lalu terperangkap di bawah batuan penutup kedap. Pada perangkap antiklin, fluida tersusun menurut berat jenisnya: gas di bagian paling atas (puncak lipatan), minyak di bawahnya, dan air di bagian paling bawah. Titik K berada di puncak antiklin pada zona gas, tepat di bawah serpih penutup.\n\nPengecoh: L berada pada zona minyak, bukan gas. M berada pada sayap lipatan yang terisi air. N berada di lapisan serpih di bawah reservoir, bukan di reservoir. Kombinasi L dan M tidak sesuai dengan zona gas.",
      f_antiklin),
    Q("Perhatikan diagram bauran energi primer Indonesia tahun T berikut. Jika target porsi EBT tahun T adalah 23%, kondisi capaian EBT adalah …",
      ["Kurang 10 poin persen dari target", "Kurang 23 poin persen dari target", "Kurang 13 poin persen dari target",
       "Sudah melampaui target 23%", "Kurang 3 poin persen dari target"],
      "Porsi EBT pada diagram adalah 13%. Target 23%. Selisihnya 23 − 13 = 10 poin persen.\nArtinya pemanfaatan EBT masih jauh dari target, sementara bauran energi masih didominasi batu bara (40%) dan minyak bumi (30%). Penyebabnya antara lain biaya awal EBT yang tinggi, keterbatasan jaringan transmisi, dan dominasi PLTU yang sudah terbangun.\n\nPengecoh: 13 poin persen adalah capaian EBT itu sendiri, bukan selisihnya. 23 poin persen adalah targetnya. \"Sudah melampaui target\" bertentangan dengan data. 3 poin persen salah menghitung selisih. Perhatikan perbedaan \"poin persen\" (selisih dua persentase) dan \"persen\" (perubahan relatif).",
      f_bauran),
    Q("Di sebuah kabupaten terdapat 1.050.000 rumah tangga, dan 980.000 di antaranya sudah menikmati listrik. Rasio elektrifikasi kabupaten tersebut adalah sekitar …",
      ["93,3%", "107,1%", "6,7%", "98,0%", "70,0%"],
      "Rasio elektrifikasi = rumah tangga berlistrik ÷ total rumah tangga × 100%.\n= 980.000 ÷ 1.050.000 × 100% ≈ 93,3%.\nArtinya masih ada ±70.000 rumah tangga (6,7%) yang belum berlistrik. Daerah seperti ini biasanya berada di wilayah terpencil atau kepulauan, sehingga solusi yang cocok adalah pembangkit tersebar seperti PLTS komunal atau mikrohidro.\n\nPengecoh: 107,1% muncul bila pembagian dibalik. 6,7% adalah persentase rumah tangga yang belum berlistrik. 98,0% dan 70,0% muncul bila salah membaca angka (98 dari 100, atau 70.000 dibaca 70%).",
      None),
    Q("Perhatikan kurva beban harian sistem kelistrikan Jawa–Bali berikut.\n\nJenis pembangkit yang paling tepat untuk melayani beban puncak sekitar pukul 18.00–22.00 adalah …",
      ["PLTG atau PLTA waduk yang dapat dinyalakan dan dinaikkan dayanya dengan cepat", "PLTU batu bara yang membutuhkan waktu berjam-jam untuk dinyalakan",
       "PLTP panas bumi yang paling efisien bila beroperasi stabil sepanjang hari", "PLTS tanpa baterai karena produksi listriknya tertinggi pada malam hari",
       "PLTU mulut tambang karena biaya bahan bakarnya paling murah"],
      "Kurva menunjukkan beban dasar ±25 GW yang selalu ada sepanjang hari, serta lonjakan beban puncak hingga ±39 GW pada pukul 18.00–22.00 ketika rumah tangga menyalakan lampu dan peralatan listrik.\n• Beban dasar dilayani pembangkit yang murah dan stabil tetapi lambat diubah dayanya: PLTU batu bara dan PLTP.\n• Beban puncak memerlukan pembangkit yang cepat dinyalakan dan dinaikkan dayanya (fleksibel): PLTG (turbin gas), PLTA waduk, atau PLTA pumped storage.\n\nPengecoh: PLTU dan PLTU mulut tambang cocok untuk beban dasar, bukan puncak. PLTP efisien untuk beban dasar. PLTS tidak menghasilkan listrik pada malam hari tanpa penyimpanan energi.",
      f_beban),
    Q("Gas bumi sering disebut energi transisi dalam peralihan dari batu bara menuju energi terbarukan. Alasan yang paling tepat adalah …",
      ["Emisi CO₂ per kWh dari gas lebih rendah dan pembangkitnya fleksibel mengimbangi EBT", "Gas bumi adalah energi terbarukan sehingga tidak menghasilkan emisi sama sekali",
       "Cadangan gas bumi tidak terbatas sehingga dapat dipakai untuk selamanya", "Pembakaran gas bumi menghasilkan emisi lebih tinggi daripada batu bara",
       "Gas bumi hanya dapat dipakai untuk memasak sehingga tidak bersaing dengan EBT"],
      "Gas bumi tetap energi fosil, tetapi pembakarannya menghasilkan emisi CO₂ per kWh sekitar 40–60% dari PLTU batu bara, serta sangat sedikit SO₂ dan partikulat. Pembangkit gas (PLTG/PLTGU) juga fleksibel karena cepat dinyalakan dan dinaikkan dayanya, sehingga dapat mengimbangi pasokan PLTS dan PLTB yang berfluktuasi. Karena itu gas dipandang sebagai jembatan selama kapasitas EBT dan penyimpanan energi dibangun.\n\nPengecoh: gas bukan energi terbarukan. Cadangannya terbatas. Emisinya lebih rendah, bukan lebih tinggi, daripada batu bara. Gas juga dipakai untuk pembangkit listrik, industri, dan bahan baku pupuk. Catatan: kebocoran metana pada rantai pasok gas dapat mengurangi manfaat iklimnya.",
      None),
    Q("Perhatikan grafik produksi dan konsumsi LPG Indonesia dalam satu tahun berikut.\n\nPersentase kebutuhan LPG yang harus dipenuhi dari impor adalah sekitar …",
      ["78%", "22%", "353%", "67%", "128%"],
      "Impor = konsumsi − produksi = 8,6 − 1,9 = 6,7 juta ton.\nPorsi impor = 6,7 ÷ 8,6 × 100% ≈ 77,9% ≈ 78%.\nKetergantungan impor yang tinggi ini terjadi setelah program konversi minyak tanah ke LPG (2007), sementara produksi LPG domestik terbatas. Implikasinya: ketahanan energi rentan terhadap gejolak harga dan kurs, serta beban subsidi besar. Alternatif yang dikembangkan antara lain jaringan gas kota, kompor listrik, dan DME dari batu bara.\n\nPengecoh: 22% adalah porsi produksi dalam negeri (1,9 ÷ 8,6). 353% membagi konsumsi dengan produksi. 67% muncul jika 6,7 dibaca sebagai persen. 128% tidak memiliki dasar perhitungan yang benar.",
      f_lpg),
    Q("Subsidi harga BBM dan listrik yang diberikan secara merata kepada semua konsumen sering dikritik. Alasan kritik yang paling tepat adalah …",
      ["Kelompok mampu yang konsumsi energinya besar justru menikmati subsidi terbanyak", "Subsidi membuat harga energi menjadi lebih mahal bagi masyarakat miskin",
       "Subsidi mendorong masyarakat menghemat energi secara berlebihan", "Subsidi menurunkan konsumsi energi sehingga pertumbuhan ekonomi terhenti",
       "Subsidi hanya dinikmati oleh masyarakat di daerah terpencil"],
      "Subsidi harga yang tidak tepat sasaran bersifat regresif: semakin banyak energi yang dikonsumsi, semakin besar subsidi yang dinikmati. Rumah tangga mampu yang memiliki mobil, banyak peralatan listrik, dan rumah besar menerima porsi subsidi jauh lebih besar daripada rumah tangga miskin. Selain itu harga energi yang murah mendorong konsumsi berlebih dan menghambat transisi energi. Karena itu kebijakan diarahkan pada subsidi tepat sasaran, misalnya berbasis data penerima.\n\nPengecoh: subsidi menurunkan, bukan menaikkan, harga. Subsidi justru mendorong pemborosan, bukan penghematan. Subsidi tidak menghentikan pertumbuhan ekonomi. Penerima subsidi terbesar justru di perkotaan.",
      None),
    Q("Coal bed methane (CBM) termasuk sumber energi fosil nonkonvensional. Pernyataan yang tepat tentang CBM adalah …",
      ["Gas metana pada lapisan batu bara yang dilepas dengan menurunkan tekanan air", "Minyak bumi yang terbentuk dari ganggang laut di dalam batu gamping karst",
       "Gas hasil fermentasi kotoran ternak di dalam biodigester skala rumah tangga", "Gas yang terbentuk dari pembakaran batu bara di dalam PLTU mulut tambang",
       "Energi terbarukan karena metana pada batu bara selalu terbentuk kembali dengan cepat"],
      "Coal bed methane (CBM) adalah gas metana yang teradsorpsi pada pori-pori dan rekahan lapisan batu bara. Gas ini diproduksi dengan memompa air dari lapisan batu bara sehingga tekanan turun dan metana terlepas. Indonesia memiliki potensi CBM besar di cekungan batu bara Sumatra Selatan dan Kalimantan Timur. Tantangannya adalah biaya tinggi dan pengelolaan air terproduksi yang banyak.\n\nPengecoh: minyak dari ganggang di batu gamping adalah minyak konvensional dengan reservoir karbonat. Gas dari kotoran ternak adalah biogas (bioenergi terbarukan). Gas hasil pembakaran adalah emisi, bukan sumber energi. CBM bukan energi terbarukan karena pembentukannya memerlukan waktu geologi.",
      None),
    Q("Perhatikan grafik faktor emisi per kWh berbagai pembangkit berikut. Jika 100 GWh listrik per tahun yang semula dari PLTU batu bara digantikan oleh PLTGU gas, pengurangan emisi CO₂ per tahun adalah …",
      ["60.000 ton", "40.000 ton", "100.000 ton", "6.000 ton", "600.000 ton"],
      "100 GWh = 100.000.000 kWh.\n• Emisi PLTU = 100.000.000 × 1.000 g = 1 × 10¹¹ g = 100.000 ton CO₂.\n• Emisi PLTGU = 100.000.000 × 400 g = 4 × 10¹⁰ g = 40.000 ton CO₂.\nPengurangan = 100.000 − 40.000 = 60.000 ton CO₂ per tahun.\nJika diganti PLTS (40 g/kWh), pengurangannya jauh lebih besar, yaitu 96.000 ton.\n\nPengecoh: 40.000 ton adalah emisi PLTGU, bukan pengurangannya. 100.000 ton adalah emisi PLTU. 6.000 dan 600.000 ton adalah kesalahan konversi satuan (1 ton = 1.000.000 g; 1 GWh = 1.000.000 kWh).",
      f_emisi),
]

P2 = [
    Q("Perhatikan grafik debit masuk turbin PLTA berikut. Tinggi jatuh 100 m dan efisiensi 90% (P = ρ × g × Q × H × η; ρ = 1.000 kg/m³; g = 9,8 m/s²).\n\nPenurunan daya PLTA pada bulan September tahun El Niño dibandingkan tahun normal adalah sekitar …",
      ["22,1 MW", "24,5 MW", "17,6 MW", "39,7 MW", "2,2 MW"],
      "Baca grafik bulan September: debit tahun normal 45 m³/s dan tahun El Niño 20 m³/s.\n• P normal = 1.000 × 9,8 × 45 × 100 × 0,9 = 39.690.000 W ≈ 39,7 MW.\n• P El Niño = 1.000 × 9,8 × 20 × 100 × 0,9 = 17.640.000 W ≈ 17,6 MW.\n• Penurunan = 39,7 − 17,6 ≈ 22,1 MW (turun ±56%).\n\nPengecoh: 24,5 MW adalah penurunan tanpa efisiensi (9,8 × 25 × 100 = 24.500 kW). 17,6 MW dan 39,7 MW adalah daya masing-masing tahun, bukan selisihnya. 2,2 MW adalah kesalahan satuan. Kasus ini menunjukkan nexus iklim–energi: kemarau panjang akibat El Niño menurunkan produksi PLTA sehingga sistem harus mengandalkan pembangkit fosil.",
      f_debit),
    Q("PLTP (panas bumi) di Indonesia umumnya dibangun dekat lokasi sumur dan tidak dapat \"diekspor\" seperti batu bara, tetapi memiliki faktor kapasitas sangat tinggi. Penjelasan yang paling tepat adalah …",
      ["Uap panas bumi tidak dapat diangkut jauh, tetapi tersedia stabil siang–malam tanpa bergantung cuaca",
       "Uap panas bumi mudah dicairkan dan dikapalkan, tetapi pasokannya bergantung pada musim hujan",
       "PLTP hanya beroperasi pada siang hari ketika suhu permukaan tanah paling panas",
       "Faktor kapasitas tinggi karena PLTP memakai batu bara sebagai bahan bakar cadangan",
       "Panas bumi bersifat tidak terbarukan sehingga harus dihabiskan secepatnya"],
      "Energi panas bumi berupa uap atau air panas bertekanan dari reservoir di bawah tanah. Fluida ini kehilangan panas dan tekanan bila dialirkan jauh, sehingga pembangkit harus dibangun di dekat sumur; energinya dikirim dalam bentuk listrik melalui jaringan transmisi. Sebaliknya, pasokan panas dari reservoir relatif stabil dan tidak bergantung pada cuaca atau waktu, sehingga PLTP dapat beroperasi hampir sepanjang waktu dengan faktor kapasitas ±80–90%; cocok sebagai pembangkit beban dasar.\n\nPengecoh: uap tidak dikapalkan. PLTP tidak bergantung pada siang hari atau suhu permukaan. PLTP tidak memakai batu bara. Panas bumi tergolong terbarukan bila laju pengambilan diimbangi injeksi kembali (reinjeksi) fluida.",
      None),
    Q("Perhatikan grafik rata-rata radiasi Matahari harian berikut.\n\nWilayah yang paling sesuai untuk PLTS skala besar beserta alasannya adalah …",
      ["NTT, karena iklimnya lebih kering sehingga tutupan awan lebih sedikit", "Papua pegunungan, karena lebih dekat ke Matahari akibat elevasinya tinggi",
       "Sumatra Barat, karena curah hujan tinggi membersihkan panel surya", "Kalimantan Barat, karena tepat di khatulistiwa sehingga radiasi tertinggi",
       "Jawa Timur, karena radiasi Matahari di Jawa selalu yang tertinggi di Indonesia"],
      "Grafik menunjukkan NTT memiliki radiasi rata-rata tertinggi (±5,8 kWh/m²/hari), disusul NTB. Wilayah ini beriklim lebih kering dengan musim kemarau panjang, sehingga hari cerah lebih banyak dan tutupan awan lebih sedikit. Itulah sebabnya NTT dan NTB menjadi lokasi prioritas PLTS.\n\nPengecoh: perbedaan elevasi beberapa kilometer tidak berarti \"lebih dekat ke Matahari\"; justru pegunungan Papua sering berawan sehingga radiasinya terendah (4,2). Hujan memang membersihkan panel, tetapi awan hujan mengurangi radiasi. Kalimantan Barat dekat khatulistiwa, tetapi tutupan awan konvektifnya tinggi. Jawa Timur tidak tertinggi pada grafik.",
      f_irr),
    Q("Daya turbin angin sebanding dengan pangkat tiga kecepatan angin (P ∝ v³). Jika kecepatan angin di lokasi B 6 m/s dan di lokasi A 4 m/s, daya turbin di B kira-kira … daya di A.",
      ["3,4 kali", "1,5 kali", "2,25 kali", "6,75 kali", "8 kali"],
      "Rasio daya = (vB ÷ vA)³ = (6 ÷ 4)³ = 1,5³ = 3,375 ≈ 3,4 kali.\nKarena hubungannya pangkat tiga, sedikit perbedaan kecepatan angin menghasilkan perbedaan daya yang besar. Inilah sebabnya pemilihan lokasi PLTB sangat sensitif terhadap data kecepatan angin, misalnya PLTB Sidrap dan Jeneponto di Sulawesi Selatan yang memiliki angin kencang dan stabil.\n\nPengecoh: 1,5 kali adalah rasio kecepatan, bukan daya. 2,25 kali memakai pangkat dua. 6,75 kali dan 8 kali berasal dari perhitungan yang keliru (8 adalah rasio bila kecepatan dua kali lipat).",
      None),
    Q("Perhatikan data rumah tangga yang memasang PLTS atap berikut.\n\nWaktu balik modal (payback period) pemasangan PLTS atap tersebut adalah …",
      ["5 tahun", "1,6 tahun", "2,3 tahun", "60 tahun", "3,1 tahun"],
      "Penghematan per bulan = 800.000 − 550.000 = Rp250.000.\nPenghematan per tahun = 250.000 × 12 = Rp3.000.000.\nWaktu balik modal = biaya ÷ penghematan = 15.000.000 ÷ 3.000.000 = 5 tahun (atau 60 bulan).\n\nPengecoh: 1,6 tahun membagi biaya dengan seluruh tagihan sebelum PLTS per tahun (15 ÷ 9,6), seolah-olah tagihan menjadi nol. 2,3 tahun membagi dengan tagihan sesudah PLTS (15 ÷ 6,6). 60 tahun keliru menafsirkan 60 bulan sebagai tahun. 3,1 tahun tidak sesuai perhitungan. Setelah 5 tahun, penghematan menjadi keuntungan bersih karena umur panel surya umumnya 20–25 tahun.",
      f_payback),
    Q("Program biodiesel B35 memakai minyak sawit sebagai campuran solar. Kritik geografis yang paling relevan terhadap perluasan program ini adalah …",
      ["Kebutuhan sawit naik sehingga berisiko mendorong pembukaan hutan dan bersaing dengan pangan",
       "Biodiesel menghasilkan emisi lebih tinggi daripada solar murni dalam semua kondisi",
       "Sawit hanya dapat tumbuh di wilayah beriklim subtropis sehingga bahan baku harus diimpor",
       "Biodiesel tidak dapat dipakai pada mesin diesel sehingga seluruh kendaraan harus diganti",
       "Program B35 menurunkan pendapatan petani sawit karena harga tandan buah segar jatuh"],
      "Bioenergi dapat mengurangi impor solar dan emisi bila bahan bakunya berkelanjutan. Namun peningkatan campuran biodiesel menaikkan permintaan minyak sawit. Jika dipenuhi dengan perluasan kebun, risiko deforestasi dan pengeringan gambut meningkat, yang justru melepaskan emisi besar. Selain itu sawit juga bahan baku minyak goreng, sehingga terjadi persaingan pangan–energi (food vs fuel) yang dapat memengaruhi harga.\n\nPengecoh: emisi biodiesel tidak selalu lebih tinggi; hal itu bergantung pada asal bahan baku. Sawit tumbuh di iklim tropis basah. Biodiesel campuran dapat dipakai pada mesin diesel. Program B35 justru menambah permintaan sawit sehingga cenderung menopang harga.",
      None),
    Q("Perhatikan profil suhu laut dua lokasi pesisir berikut. Pembangkit listrik tenaga panas laut (OTEC) memerlukan beda suhu air permukaan dan air dalam minimal sekitar 20 °C.\n\nLokasi yang sesuai untuk OTEC adalah …",
      ["Lokasi B, karena beda suhu permukaan dan kedalaman 1.000 m sekitar 24 °C", "Lokasi A, karena suhu permukaannya paling tinggi di antara keduanya",
       "Lokasi A, karena laut dangkal memudahkan pemasangan pipa air dingin", "Kedua lokasi sesuai karena sama-sama berada di laut tropis",
       "Tidak ada yang sesuai karena beda suhu di kedua lokasi kurang dari 5 °C"],
      "OTEC (Ocean Thermal Energy Conversion) memanfaatkan beda suhu air laut hangat di permukaan dan air dingin di kedalaman ±800–1.000 m untuk menggerakkan siklus fluida kerja. Di lokasi B, suhu permukaan ±29 °C dan suhu pada 1.000 m ±5 °C, sehingga beda suhunya ±24 °C (memenuhi syarat). Lokasi A hanya sedalam 60 m dengan suhu hampir seragam (beda ±1 °C), sehingga tidak ada sumber air dingin.\nIndonesia memiliki banyak lokasi laut dalam yang dekat pantai, misalnya utara Bali dan Laut Banda, sehingga potensinya besar.\n\nPengecoh: suhu permukaan tinggi saja tidak cukup; yang diperlukan adalah beda suhu. Laut dangkal tidak menyediakan air dingin. Tidak semua laut tropis sesuai. Lokasi B memiliki beda suhu jauh lebih dari 5 °C.",
      f_otec),
    Q("Rencana pembangunan PLTN pertama di Indonesia sering diarahkan ke Kalimantan Barat atau Bangka Belitung, bukan Jawa. Alasan geografis yang paling kuat adalah …",
      ["Kedua wilayah relatif stabil secara tektonik sehingga risiko gempa dan tsunami lebih rendah",
       "Kedua wilayah memiliki gunung api aktif yang dapat dimanfaatkan sebagai pendingin reaktor",
       "Penduduk kedua wilayah lebih banyak sehingga kebutuhan listriknya paling besar di Indonesia",
       "Kedua wilayah merupakan penghasil batu bara terbesar sehingga cocok untuk bahan bakar nuklir",
       "Curah hujan di kedua wilayah paling rendah sehingga reaktor tidak memerlukan air"],
      "Keselamatan PLTN sangat bergantung pada kestabilan geologi lokasi. Jawa berada dekat zona subduksi dan banyak sesar aktif serta gunung api, sehingga risiko gempa, tsunami, dan erupsi tinggi. Kalimantan Barat dan Bangka Belitung berada di bagian stabil Paparan Sunda, jauh dari zona subduksi dan gunung api aktif, sehingga dinilai lebih aman. Bangka Belitung juga memiliki mineral monasit yang mengandung torium.\n\nPengecoh: gunung api aktif justru ancaman, bukan keuntungan. Penduduk dan kebutuhan listrik terbesar ada di Jawa. Batu bara bukan bahan bakar nuklir. PLTN memerlukan banyak air pendingin, biasanya dari laut.",
      None),
    Q("Perhatikan grafik faktor kapasitas berbagai pembangkit berikut. Jika PLTP dan PLTS masing-masing berkapasitas 100 MW, produksi listrik tahunan PLTP kira-kira … produksi PLTS.",
      ["5 kali", "sama dengan", "0,2 kali", "72 kali", "2,5 kali"],
      "Produksi tahunan = kapasitas × 8.760 jam × faktor kapasitas.\n• PLTP: 100 × 8.760 × 0,90 = 788.400 MWh.\n• PLTS: 100 × 8.760 × 0,18 = 157.680 MWh.\nRasio = 788.400 ÷ 157.680 = 5 kali.\nArtinya kapasitas terpasang yang sama tidak berarti produksi listrik yang sama. Untuk menghasilkan energi setara satu PLTP 100 MW, diperlukan PLTS sekitar 500 MW beserta penyimpanan energi agar pasokannya stabil.\n\nPengecoh: \"sama dengan\" mengabaikan faktor kapasitas. 0,2 kali membalik perbandingan. 72 kali adalah selisih persentase (90 − 18). 2,5 kali tidak sesuai perhitungan.",
      f_cf),
    Q("Hidrogen hijau dipandang sebagai salah satu pilar transisi energi. Hidrogen disebut \"hijau\" apabila …",
      ["Diproduksi melalui elektrolisis air menggunakan listrik dari energi terbarukan", "Diproduksi dari gas bumi tanpa penangkapan karbon (steam reforming)",
       "Diproduksi dari gasifikasi batu bara di sekitar wilayah tambang", "Disimpan dalam tangki berwarna hijau agar mudah dibedakan",
       "Diproduksi dari gas bumi dengan menangkap dan menyimpan karbonnya"],
      "Hidrogen diklasifikasikan berdasarkan sumber energi dan emisi proses produksinya:\n• Hidrogen abu-abu: dari gas bumi melalui steam methane reforming, CO₂ dilepas ke atmosfer.\n• Hidrogen cokelat/hitam: dari gasifikasi batu bara.\n• Hidrogen biru: dari gas bumi, tetapi CO₂-nya ditangkap dan disimpan (CCS).\n• Hidrogen hijau: dari elektrolisis air memakai listrik energi terbarukan (PLTS, PLTB, PLTA, PLTP), hampir tanpa emisi.\nIndonesia berpotensi memproduksi hidrogen hijau dari panas bumi dan PLTA.\n\nPengecoh: opsi lain menggambarkan hidrogen abu-abu, cokelat, dan biru. Warna tangki tidak terkait dengan klasifikasi.",
      None),
]

P3 = [
    Q("Perhatikan diagram komposisi air di Bumi berikut.\n\nJika K, L, dan M adalah komponen air tawar, sumber air tawar yang paling besar volumenya dan relatif dapat diakses manusia ditunjukkan oleh …",
      ["L, yaitu air tanah", "K, yaitu es dan gletser", "M, yaitu air permukaan", "K, yaitu air tanah", "M, yaitu uap air atmosfer"],
      "Sebaran air tawar di Bumi: ±68,7% tersimpan sebagai es dan gletser (K), ±30,1% sebagai air tanah (L), dan hanya ±1,2% sebagai air permukaan dan bentuk lain seperti danau, sungai, lengas tanah, dan uap air (M).\nEs dan gletser memang terbesar, tetapi sebagian besar berada di Antartika dan Greenland sehingga sulit dimanfaatkan. Air tanah adalah cadangan air tawar terbesar yang relatif dapat diakses melalui sumur dan mata air, sehingga menjadi sumber utama air minum banyak kota.\n\nPengecoh: K adalah es, bukan air tanah. M memang paling mudah diakses, tetapi volumenya paling kecil. Uap air hanya bagian kecil dari M.",
      f_airbumi),
    Q("Perhatikan penampang hidrogeologi sebuah cekungan air tanah berikut.\n\nAir di sumur W2 memancar sendiri tanpa dipompa karena …",
      ["W2 menembus akuifer tertekan yang daerah resapannya lebih tinggi dari mulut sumur", "W2 menyadap akuifer bebas yang muka air tanahnya selalu di atas permukaan",
       "Lapisan lempung di atas akuifer menyimpan air paling banyak sehingga tekanannya tinggi", "Sumur W2 lebih dangkal sehingga lebih dekat dengan sumber air hujan",
       "Air di akuifer tertekan dipanaskan magma sehingga memuai dan menyembur"],
      "Sumur W2 menembus lapisan kedap (lempung) dan menyadap akuifer tertekan (confined aquifer) di bawahnya. Akuifer ini terisi air dari daerah resapan di pegunungan yang lebih tinggi. Karena terkurung lapisan kedap di atas dan di bawahnya, air berada dalam kondisi bertekanan. Bila tinggi tekanan (muka piezometrik) melebihi elevasi mulut sumur, air memancar sendiri; inilah sumur artesis.\nSumur W1 hanya menyadap akuifer bebas sehingga airnya perlu ditimba atau dipompa.\n\nPengecoh: muka air tanah bebas berada di bawah permukaan. Lempung bersifat kedap, bukan penyimpan utama. W2 justru lebih dalam. Pancaran sumur artesis bukan disebabkan panas magma.",
      f_akuifer),
    Q("Indonesia mengimpor beras dalam jumlah besar dari Vietnam dan Thailand pada tahun kering. Dari sudut pandang konsep air virtual, impor tersebut berarti …",
      ["Indonesia secara tidak langsung \"mengimpor\" air yang dipakai untuk menanam padi di negara asal",
       "Indonesia mengekspor air tanah ke negara asal sebagai bayaran atas beras yang diterima",
       "Air yang terkandung secara fisik di dalam butir beras menambah cadangan air sungai Indonesia",
       "Jejak air beras impor selalu nol karena padi ditanam di negara beriklim tropis basah",
       "Impor beras menambah kebutuhan air irigasi di Indonesia pada musim kemarau"],
      "Air virtual adalah jumlah air yang dipakai untuk menghasilkan suatu produk. Satu kilogram beras membutuhkan ±2.500 liter air sepanjang proses produksinya. Ketika suatu negara mengimpor beras, negara itu secara tidak langsung memanfaatkan air negara pengekspor, sehingga tekanan terhadap sumber daya airnya sendiri berkurang. Konsep ini membantu menganalisis perdagangan pangan sebagai strategi menghadapi kelangkaan air.\n\nPengecoh: tidak ada ekspor air tanah secara fisik. Air virtual bukan air yang secara fisik terkandung dalam butir beras. Jejak air beras tidak nol. Impor beras justru mengurangi, bukan menambah, kebutuhan irigasi dalam negeri.",
      None),
    Q("Perhatikan grafik luas permukaan Laut Aral berikut.\n\nPenyebab utama penyusutan Laut Aral adalah …",
      ["Pengalihan air Amu Darya dan Syr Darya untuk irigasi kapas skala besar", "Kenaikan muka laut global yang mendorong air Aral ke Laut Kaspia",
       "Gempa tektonik yang membuat dasar Laut Aral retak dan menyerap air", "Pemanasan global yang membuat seluruh air Aral menguap dalam satu dekade",
       "Pembangunan PLTA di muara Laut Aral yang membendung aliran air keluar"],
      "Laut Aral adalah danau tertutup di Asia Tengah yang hanya diisi oleh Sungai Amu Darya dan Syr Darya. Sejak 1960-an, pemerintah Uni Soviet mengalihkan sebagian besar air kedua sungai untuk mengairi perkebunan kapas dan padi di gurun. Akibatnya aliran ke Laut Aral menurun drastis; luasnya menyusut dari ±68 ribu km² (1960) menjadi ±14 ribu km² (2010). Dampaknya: salinitas meningkat, perikanan runtuh, badai debu bergaram, dan kesehatan masyarakat memburuk.\n\nPengecoh: Laut Aral tidak terhubung dengan laut global. Tidak ada gempa yang menyebabkan penyusutan. Pemanasan global bukan penyebab utama. Laut Aral adalah danau tertutup tanpa aliran keluar sehingga tidak ada PLTA di \"muaranya\".",
      f_aral),
    Q("Pembangunan Grand Ethiopian Renaissance Dam (GERD) di hulu Sungai Nil memicu ketegangan dengan Mesir. Akar masalah konflik air lintas batas ini adalah …",
      ["Negara hulu mengendalikan aliran, sedangkan negara hilir sangat bergantung pada sungai yang sama",
       "Mesir berada di hulu sehingga dapat menghentikan seluruh aliran Sungai Nil ke Ethiopia",
       "Bendungan selalu menambah debit sungai di hilir sehingga Mesir mengalami banjir terus-menerus",
       "Sungai Nil hanya mengalir di wilayah Mesir sehingga Ethiopia tidak berhak memanfaatkannya",
       "Ketegangan terjadi karena kedua negara berebut cadangan minyak bumi di dasar sungai"],
      "Sungai Nil Biru berhulu di dataran tinggi Ethiopia dan menyumbang sebagian besar debit Nil yang mengalir ke Sudan dan Mesir. Mesir yang beriklim gurun bergantung hampir sepenuhnya pada Sungai Nil. Ketika Ethiopia (negara hulu) membangun bendungan raksasa untuk PLTA dan mengisi waduknya, Mesir (negara hilir) khawatir pasokan airnya berkurang, terutama pada tahun kering. Konflik hulu–hilir seperti ini menuntut perjanjian pembagian air dan pengelolaan bersama.\n\nPengecoh: Mesir berada di hilir, bukan hulu. Bendungan tidak menambah debit; pengisian waduk justru mengurangi aliran sementara. Sungai Nil melintasi banyak negara. Konflik ini tentang air, bukan minyak.",
      None),
    Q("Perhatikan tabel ketersediaan air dan penduduk tiga provinsi berikut. Indeks Falkenmark: > 1.700 m³/kapita aman; 1.000–1.700 stres air; 500–1.000 kelangkaan; < 500 kelangkaan absolut.\n\nPasangan yang tepat adalah …",
      ["K stres air; L aman; M kelangkaan absolut", "K aman; L stres air; M kelangkaan", "K kelangkaan; L aman; M stres air",
       "K stres air; L kelangkaan; M aman", "K kelangkaan absolut; L stres air; M aman"],
      "Ketersediaan per kapita = volume air terbarukan ÷ jumlah penduduk (ubah km³ menjadi m³: 1 km³ = 10⁹ m³).\n• K: 12 × 10⁹ ÷ 10 × 10⁶ = 1.200 m³ → stres air.\n• L: 30 × 10⁹ ÷ 8 × 10⁶ = 3.750 m³ → aman.\n• M: 4 × 10⁹ ÷ 9 × 10⁶ ≈ 444 m³ → kelangkaan absolut.\n\nPengecoh: opsi lain salah mengurutkan nilai. Kesalahan umum adalah lupa mengonversi km³ ke m³ atau juta jiwa ke jiwa, sehingga hasilnya meleset ribuan kali. Provinsi M memerlukan strategi seperti pemanenan air hujan, efisiensi irigasi, daur ulang air, dan perlindungan daerah resapan.",
      f_prov),
    Q("Upaya konservasi berikut yang secara langsung paling meningkatkan imbuhan (pengisian) air tanah di kawasan permukiman adalah …",
      ["Membuat sumur resapan dan lubang resapan biopori di halaman rumah", "Menyemen seluruh halaman agar air hujan cepat mengalir ke selokan",
       "Memperbanyak sumur bor dalam untuk memenuhi kebutuhan air rumah tangga", "Memperlebar saluran drainase agar air hujan cepat dibuang ke laut",
       "Mengganti pipa air bersih yang bocor di jaringan perpipaan kota"],
      "Imbuhan air tanah meningkat bila lebih banyak air hujan meresap ke dalam tanah. Sumur resapan menampung limpasan dari atap lalu meresapkannya ke dalam tanah, sedangkan lubang resapan biopori memperbesar pori-pori tanah melalui aktivitas organisme. Keduanya menambah infiltrasi dan sekaligus mengurangi limpasan permukaan.\n\nPengecoh: menyemen halaman dan memperlebar drainase justru mempercepat air terbuang. Sumur bor dalam menambah pengambilan, bukan pengisian, air tanah. Mengganti pipa bocor adalah upaya efisiensi distribusi air bersih yang penting, tetapi tidak secara langsung menambah imbuhan air tanah.",
      None),
    Q("Perhatikan grafik muka air tanah dan kadar klorida di sumur pantau Kota S berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Pengambilan air tanah berlebih menurunkan muka air tanah sehingga air laut menyusup ke akuifer",
       "Kenaikan curah hujan menurunkan muka air tanah sehingga kadar garam air tanah meningkat",
       "Muka air tanah naik di atas muka laut sehingga air tawar mendorong air laut menjauh",
       "Kadar klorida meningkat karena pencemaran limbah domestik tanpa kaitan dengan muka air tanah",
       "Penurunan muka air tanah dan kenaikan klorida tidak berhubungan karena keduanya diukur terpisah"],
      "Grafik menunjukkan muka air tanah terus turun dari −2 m menjadi ±−15 m di bawah muka laut, sementara kadar klorida naik tajam dari ±120 mg/L menjadi hampir 700 mg/L. Di wilayah pesisir, air tanah tawar normalnya menahan air laut di bawahnya. Ketika air tanah dipompa berlebihan dan muka air tanah turun di bawah muka laut, tekanan air tawar berkurang sehingga air laut menyusup ke akuifer (intrusi air laut). Akibatnya sumur menjadi payau atau asin.\n\nPengecoh: hujan justru menaikkan muka air tanah. Muka air tanah pada grafik turun, bukan naik. Limbah domestik meningkatkan pencemar lain, tetapi pola klorida yang naik seiring penurunan muka air tanah khas intrusi air laut. Keduanya diukur di sumur yang sama dan berkaitan erat.",
      f_intrusi),
    Q("Prinsip one river, one plan, one integrated management dalam pengelolaan DAS terpadu menekankan bahwa …",
      ["DAS dikelola sebagai satu kesatuan dari hulu sampai hilir lintas batas administrasi", "Setiap kabupaten mengelola bagian sungainya sendiri tanpa koordinasi dengan daerah lain",
       "Pengelolaan hanya difokuskan pada bagian hilir karena banjir terjadi di hilir", "Satu sungai hanya boleh dimanfaatkan untuk satu jenis kegiatan ekonomi",
       "Pengelolaan DAS diserahkan seluruhnya kepada perusahaan air minum swasta"],
      "Daerah aliran sungai (DAS) adalah satu kesatuan ekosistem yang dibatasi punggung bukit, sedangkan batas administrasi (kabupaten, provinsi) sering memotongnya. Apa yang terjadi di hulu (penebangan hutan, pertambangan) berdampak ke hilir (banjir, sedimentasi, pencemaran). Karena itu pengelolaan harus terpadu: satu rencana dan satu sistem pengelolaan dari hulu hingga hilir, melibatkan semua daerah dan pemangku kepentingan, seperti pada program pemulihan Sungai Citarum.\n\nPengecoh: pengelolaan sendiri-sendiri menimbulkan konflik hulu–hilir. Fokus hanya di hilir mengabaikan sumber masalah. Sungai dapat dimanfaatkan untuk banyak kegiatan (multiguna). Prinsip ini tidak berarti privatisasi.",
      None),
    Q("Perhatikan grafik jejak air beberapa bahan pangan berikut. Seseorang mengganti konsumsi 10 kg daging sapi per tahun dengan 10 kg daging ayam. Penghematan jejak air per tahun adalah …",
      ["111.000 liter", "154.000 liter", "43.000 liter", "11.100 liter", "197.000 liter"],
      "Jejak air daging sapi ±15.400 L/kg, sedangkan daging ayam ±4.300 L/kg.\n• 10 kg sapi = 154.000 L.\n• 10 kg ayam = 43.000 L.\n• Penghematan = 154.000 − 43.000 = 111.000 liter per tahun.\nDaging sapi memiliki jejak air sangat besar karena sapi memerlukan pakan (rumput dan biji-bijian) dalam jumlah banyak selama masa pemeliharaan yang panjang. Perubahan pola konsumsi merupakan salah satu cara mengurangi tekanan terhadap sumber daya air global.\n\nPengecoh: 154.000 L adalah jejak air sapi saja. 43.000 L adalah jejak air ayam saja. 11.100 L adalah kesalahan desimal. 197.000 L menjumlahkan keduanya.",
      f_jejak),
]

P4 = [
    Q("Perhatikan grafik luas tutupan hutan dua kabupaten berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Q kehilangan hutan relatif lebih besar (20%) meski luas yang hilang lebih kecil", "P kehilangan hutan relatif lebih besar karena luas yang hilang 120 ribu ha",
       "Kedua kabupaten kehilangan hutan dengan persentase yang sama besar", "Q kehilangan 60 ribu ha atau setara 25% dari tutupan hutan 2020",
       "P kehilangan hutan 15% sehingga laju relatifnya lebih tinggi dari Q"],
      "Hitung perubahan absolut dan relatif terhadap nilai awal (2010):\n• P: 800 − 680 = 120 ribu ha; 120 ÷ 800 × 100% = 15%.\n• Q: 300 − 240 = 60 ribu ha; 60 ÷ 300 × 100% = 20%.\nP kehilangan luas lebih besar, tetapi Q kehilangan porsi hutan yang lebih besar (20%). Untuk menilai tekanan terhadap ekosistem, persentase sering lebih bermakna karena menunjukkan seberapa besar bagian hutan yang tersisa.\n\nPengecoh: luas absolut yang besar tidak berarti laju relatif besar. Persentase keduanya berbeda. 25% muncul bila dibagi nilai akhir (60 ÷ 240), padahal persentase perubahan selalu dibagi nilai awal. P memang kehilangan 15%, tetapi itu lebih kecil dari Q.",
      f_hutan2),
    Q("Sistem Verifikasi Legalitas dan Kelestarian (SVLK) diterapkan pada produk kayu Indonesia. Tujuan utama SVLK adalah …",
      ["Memastikan kayu berasal dari sumber legal dan dikelola lestari sehingga diterima pasar global",
       "Melarang seluruh penebangan kayu di Indonesia agar hutan tidak berkurang sama sekali",
       "Menaikkan pajak ekspor kayu agar hutan lebih banyak dikonversi menjadi kebun",
       "Memberi izin penebangan bebas bagi semua perusahaan yang memiliki pabrik kayu",
       "Mengganti seluruh hutan alam dengan hutan tanaman industri yang seragam"],
      "SVLK adalah sistem pelacakan dan sertifikasi yang memastikan kayu dan produk kayu berasal dari sumber legal serta memenuhi prinsip kelestarian, mulai dari hutan hingga pabrik dan ekspor. Sistem ini membantu menekan pembalakan liar dan membuat produk kayu Indonesia diakui pasar internasional, misalnya melalui lisensi FLEGT dengan Uni Eropa.\n\nPengecoh: SVLK tidak melarang seluruh penebangan, melainkan memastikan legalitas dan kelestarian. SVLK bukan instrumen pajak dan tidak mendorong konversi hutan. SVLK justru membatasi penebangan ilegal. Mengganti hutan alam dengan HTI bukan tujuan SVLK.",
      None),
    Q("Perhatikan kurva model surplus produksi stok ikan berikut.\n\nTitik yang menunjukkan kondisi hasil tangkapan maksimum lestari (MSY) adalah …",
      ["C, saat stok sekitar setengah daya dukung", "E, saat stok hampir mencapai daya dukung", "A, saat stok paling sedikit",
       "D, saat stok tiga perempat daya dukung", "B, saat pertumbuhan stok sepertiga maksimum"],
      "Pada model surplus produksi (logistik), pertumbuhan stok per tahun kecil ketika stok sangat sedikit (A), karena jumlah induk sedikit, dan juga kecil ketika stok mendekati daya dukung (E), karena persaingan makanan dan ruang. Pertumbuhan maksimum terjadi pada stok sekitar K/2 (titik C). Jika penangkapan sama dengan pertumbuhan maksimum ini, stok dapat bertahan stabil; itulah MSY.\n\nPengecoh: E memiliki stok terbesar, tetapi pertumbuhannya kecil. A paling rentan karena stok sangat sedikit. D dan B berada di sisi kurva yang pertumbuhannya belum maksimum. Dalam pengelolaan, stok yang ditekan di bawah K/2 (sisi kiri kurva) menandakan tangkap lebih (overfishing).",
      f_msy),
    Q("Suatu stok ikan memiliki r = 0,8 per tahun dan K = 5 juta ton. Dengan MSY = r × K ÷ 4 dan JTB = 80% MSY, hasil tangkapan aktual 0,95 juta ton per tahun menunjukkan bahwa …",
      ["Tangkapan melampaui JTB (0,8 juta ton) tetapi masih di bawah MSY (1 juta ton)", "Tangkapan masih di bawah JTB sehingga upaya tangkap dapat dinaikkan",
       "Tangkapan melampaui MSY sehingga stok pasti sudah punah", "Tangkapan tepat sama dengan MSY sehingga kondisi paling ideal",
       "Tangkapan di bawah 20% potensi sehingga perikanan belum dimanfaatkan"],
      "1) MSY = 0,8 × 5 ÷ 4 = 1,0 juta ton per tahun.\n2) JTB = 80% × 1,0 = 0,8 juta ton per tahun.\nTangkapan 0,95 juta ton berada di atas JTB tetapi masih di bawah MSY. Artinya pemanfaatan sudah melewati batas kehati-hatian dan mendekati MSY, sehingga upaya tangkap perlu dikendalikan agar tidak berlanjut menjadi tangkap lebih.\n\nPengecoh: tangkapan tidak berada di bawah JTB. Tangkapan belum melampaui MSY, dan melampaui MSY pun tidak berarti stok pasti punah, melainkan stok menurun. Tangkapan tidak tepat sama dengan MSY. Nilai 0,95 juta ton adalah 95% MSY, bukan di bawah 20%.",
      None),
    Q("Perhatikan grafik tingkat pemanfaatan ikan demersal per WPP berikut. Kriteria: E < 0,5 moderat; 0,5 ≤ E < 1 terkendali penuh (fully exploited); E ≥ 1 tangkap lebih (over-exploited).\n\nWPP yang berstatus tangkap lebih adalah …",
      ["711, 712, dan 718", "712 dan 713 saja", "713, 714, dan 715", "711 dan 718 saja", "Seluruh WPP pada grafik"],
      "Baca nilai E pada grafik: WPP 711 = 1,2; 712 = 1,4; 713 = 0,9; 714 = 0,6; 715 = 0,7; 718 = 1,1.\nWPP dengan E ≥ 1 adalah 711 (Selat Karimata, Laut Natuna), 712 (Laut Jawa), dan 718 (Laut Arafura). Ketiganya berstatus tangkap lebih, sehingga upaya penangkapan perlu dikurangi dan dialihkan.\nWPP 713, 714, dan 715 berstatus terkendali penuh (0,5 ≤ E < 1); penambahan upaya tidak dianjurkan.\n\nPengecoh: 713 bernilai 0,9 (di bawah 1). \"711 dan 718 saja\" melewatkan 712 yang nilainya tertinggi. Tidak semua WPP berstatus tangkap lebih.",
      f_wpp),
    Q("Konflik antara nelayan tradisional dan kapal pukat (trawl) sering terjadi di perairan pesisir. Alasan utama alat tangkap pukat dasar dilarang di Indonesia adalah …",
      ["Pukat dasar menyapu dasar laut, merusak habitat, dan menangkap ikan kecil secara tidak selektif",
       "Pukat dasar hanya dapat menangkap ikan pelagis besar sehingga hasilnya terlalu sedikit",
       "Pukat dasar terlalu murah sehingga nelayan tradisional tidak mampu bersaing harga",
       "Pukat dasar digunakan di laut dalam sehingga tidak berdampak pada nelayan pesisir",
       "Pukat dasar menghasilkan polusi suara yang membuat ikan bermigrasi ke negara lain"],
      "Pukat dasar (bottom trawl) ditarik di sepanjang dasar laut. Alat ini merusak terumbu karang, padang lamun, dan habitat dasar, serta tidak selektif karena ikut menangkap ikan muda dan biota nontarget (tangkapan sampingan). Akibatnya stok ikan cepat menurun dan nelayan tradisional dengan alat tangkap ramah lingkungan kehilangan sumber penghidupan, sehingga sering memicu konflik horizontal antarnelayan.\n\nPengecoh: pukat dasar justru menangkap ikan demersal dalam jumlah besar. Masalahnya bukan murahnya alat. Pukat banyak beroperasi di perairan pesisir dangkal sehingga berbenturan dengan nelayan kecil. Polusi suara bukan alasan utama pelarangannya.",
      None),
    Q("Perhatikan diagram zona laut menurut UNCLOS 1982 berikut.\n\nZona tempat Indonesia memiliki hak berdaulat untuk mengeksplorasi dan mengelola sumber daya ikan, tetapi kapal asing tetap bebas berlayar, ditunjukkan oleh label …",
      ["R, Zona Ekonomi Eksklusif", "P, laut teritorial", "Q, zona tambahan", "P dan Q, laut teritorial dan zona tambahan", "R, laut lepas"],
      "Zona laut menurut UNCLOS 1982 dihitung dari garis pangkal:\n• P (0–12 mil laut): laut teritorial, wilayah kedaulatan penuh negara pantai (kapal asing hanya memiliki hak lintas damai).\n• Q (12–24 mil laut): zona tambahan, tempat negara dapat menegakkan aturan bea cukai, imigrasi, fiskal, dan kesehatan.\n• R (hingga 200 mil laut): Zona Ekonomi Eksklusif (ZEE), tempat negara pantai memiliki hak berdaulat atas sumber daya alam (ikan, minyak, gas), sedangkan kapal negara lain tetap bebas berlayar dan memasang kabel.\nKasus penangkapan kapal ikan asing di ZEE Natuna adalah contoh penegakan hak berdaulat ini.\n\nPengecoh: laut teritorial adalah kedaulatan penuh, bukan sekadar hak berdaulat. Zona tambahan tidak mengatur sumber daya ikan. Laut lepas berada di luar 200 mil laut.",
      f_unclos),
    Q("Budidaya rumput laut di NTT, Sulawesi Selatan, dan Maluku dipromosikan sebagai bagian dari ekonomi biru. Alasan yang paling tepat adalah …",
      ["Memberi pendapatan pesisir tanpa pakan tambahan sekaligus menyerap karbon dan nutrien", "Rumput laut hanya tumbuh di perairan tercemar sehingga membersihkan laut sepenuhnya",
       "Budidaya rumput laut memerlukan pembukaan hutan mangrove dalam skala besar", "Rumput laut adalah komoditas yang tidak memiliki pasar ekspor sama sekali",
       "Budidaya rumput laut memerlukan pakan ikan dalam jumlah besar setiap hari"],
      "Ekonomi biru menekankan pemanfaatan sumber daya laut yang menyejahterakan masyarakat sekaligus menjaga kesehatan ekosistem. Rumput laut tumbuh dengan memanfaatkan cahaya Matahari dan nutrien di perairan, sehingga tidak memerlukan pakan. Budidayanya relatif murah, padat karya, dan cocok untuk masyarakat pesisir. Rumput laut juga menyerap karbon dan nutrien berlebih, serta memiliki pasar ekspor besar untuk karagenan dan agar.\n\nPengecoh: rumput laut justru membutuhkan perairan jernih yang tidak tercemar. Budidaya tidak memerlukan pembukaan mangrove. Indonesia termasuk eksportir rumput laut terbesar dunia. Rumput laut tidak memerlukan pakan.",
      None),
    Q("Perhatikan grafik upaya tangkap dan hasil tangkapan per satuan upaya (CPUE) ikan kakap berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Upaya tangkap terus naik sementara CPUE turun, menandakan stok ikan menurun akibat tangkap lebih",
       "CPUE turun karena kapal semakin sedikit sehingga stok ikan pulih dengan cepat",
       "Upaya tangkap dan CPUE sama-sama naik sehingga perikanan kakap semakin sehat",
       "CPUE naik setelah 2015 karena teknologi tangkap semakin modern dan stok bertambah",
       "Tidak ada hubungan antara upaya tangkap dan CPUE sehingga stok tidak dapat dinilai"],
      "Grafik menunjukkan upaya tangkap (jumlah trip) naik terus dari ±1.000 menjadi ±2.600 trip, sedangkan CPUE turun dari ±50 menjadi ±18 ton per trip. CPUE adalah indikator kelimpahan stok: bila setiap trip menghasilkan ikan semakin sedikit walaupun upaya ditambah, berarti populasi ikan di laut menurun. Pola ini merupakan tanda klasik tangkap lebih, sehingga diperlukan pembatasan upaya, kuota, atau penutupan musim/area penangkapan.\n\nPengecoh: jumlah kapal tidak berkurang. CPUE tidak naik. Teknologi modern justru dapat menyamarkan penurunan stok karena menambah efisiensi tangkap. Hubungan keduanya jelas berlawanan arah.",
      f_cpue),
    Q("Program Perhutanan Sosial memberi akses legal kepada masyarakat untuk mengelola kawasan hutan negara. Skema berikut yang mengakui hak masyarakat hukum adat atas wilayah hutannya adalah …",
      ["Hutan Adat", "Hutan Tanaman Rakyat", "Hutan Kemasyarakatan", "Hutan Desa", "Kemitraan Kehutanan"],
      "Perhutanan Sosial memiliki beberapa skema:\n• Hutan Desa: dikelola lembaga desa.\n• Hutan Kemasyarakatan: dikelola kelompok masyarakat untuk pemberdayaan.\n• Hutan Tanaman Rakyat: hutan tanaman yang dibangun kelompok masyarakat.\n• Kemitraan Kehutanan: kerja sama masyarakat dengan pemegang izin atau pengelola hutan.\n• Hutan Adat: hutan yang berada di wilayah masyarakat hukum adat dan diakui sebagai hak mereka, bukan lagi hutan negara (pasca-Putusan MK No. 35/2012).\nHanya Hutan Adat yang secara khusus mengakui hak masyarakat hukum adat atas wilayahnya.\n\nOpsi lain adalah skema pemberian akses kelola pada hutan negara, bukan pengakuan hak adat. Pengakuan hutan adat penting karena masyarakat adat sering memiliki aturan lokal yang menjaga kelestarian hutan.",
      None),
]

P5 = [
    Q("Perhatikan grafik nilai ekspor komoditas berbasis nikel berikut.\n\nPenjelasan yang paling tepat tentang perubahan nilai ekspor setelah kebijakan larangan ekspor bijih nikel adalah …",
      ["Nilai ekspor naik karena bijih diolah di dalam negeri menjadi produk bernilai tambah lebih tinggi",
       "Nilai ekspor naik karena volume bijih mentah yang diekspor meningkat lebih dari 30 kali",
       "Nilai ekspor turun karena larangan ekspor menghentikan seluruh kegiatan tambang nikel",
       "Kenaikan nilai ekspor terjadi tanpa biaya lingkungan dan sosial apa pun di daerah tambang",
       "Kenaikan disebabkan harga nikel dunia naik 33 kali, bukan karena pengolahan dalam negeri"],
      "Sejak bijih nikel dilarang diekspor (mulai 2014 dan diperketat 2020), bijih diolah di smelter dalam negeri menjadi feronikel, nickel pig iron, stainless steel, hingga bahan baku baterai. Grafik menunjukkan nilai ekspor naik dari ±1 miliar USD menjadi ±33 miliar USD. Kenaikan terutama berasal dari nilai tambah pengolahan (hilirisasi), bukan dari bertambahnya ekspor bijih mentah.\nNamun hilirisasi juga membawa biaya: deforestasi di area tambang, pencemaran pesisir, emisi PLTU captive yang memasok smelter, serta isu keselamatan kerja. Karena itu analisis harus seimbang.\n\nPengecoh: ekspor bijih justru dilarang. Kegiatan tambang tidak berhenti, malah meningkat. Biaya lingkungan dan sosial nyata. Harga nikel dunia berfluktuasi, tetapi tidak naik 33 kali.",
      f_nikel),
    Q("Timah di Bangka Belitung banyak ditambang dari endapan aluvial di darat dan dasar laut dangkal. Proses pembentukan endapan timah jenis ini adalah …",
      ["Mineral kasiterit dari granit lapuk terangkut air lalu terkonsentrasi sebagai endapan plaser", "Timah terbentuk dari sisa tumbuhan rawa yang terkubur dan mengalami pembatubaraan",
       "Timah berasal dari pelapukan batuan ultrabasa yang membentuk laterit di bukit-bukit", "Timah terbentuk dari endapan karbonat terumbu karang di laut dangkal",
       "Timah terbentuk dari letusan gunung api muda yang menyebarkan abu ke dasar laut"],
      "Bangka Belitung termasuk sabuk timah Asia Tenggara yang tersusun atas batuan granit. Mineral kasiterit (SnO₂) terbentuk di dalam granit, lalu granit melapuk dan kasiterit yang berat serta tahan pelapukan terangkut aliran air. Karena berat jenisnya tinggi, kasiterit mengendap dan terkonsentrasi di lembah sungai purba dan dasar laut dangkal sebagai endapan plaser (aluvial). Penambangannya di darat meninggalkan banyak kolong (lubang bekas tambang) dan di laut memicu konflik dengan nelayan serta merusak terumbu karang.\n\nPengecoh: pembatubaraan membentuk batu bara. Laterit dari batuan ultrabasa membentuk nikel. Endapan karbonat membentuk batu gamping. Abu vulkanik tidak membentuk endapan timah.",
      None),
    Q("Perhatikan diagram komponen nilai ekonomi ekosistem mangrove Desa B berikut.\n\nPorsi nilai guna tidak langsung (jasa pelindung pantai dan penyerapan karbon) terhadap nilai ekonomi total adalah sekitar …",
      ["62,5%", "31,3%", "46,9%", "6,3%", "78,1%"],
      "Nilai ekonomi total = 2 + 8 + 15 + 5 + 2 = 32 juta rupiah per hektare per tahun.\n• Nilai guna langsung: kayu (2) + perikanan (8) = 10.\n• Nilai guna tidak langsung: pelindung pantai (15) + penyerapan karbon (5) = 20.\n• Nilai bukan guna: nilai keberadaan (2).\nPorsi nilai guna tidak langsung = 20 ÷ 32 × 100% = 62,5%.\nArtinya sebagian besar nilai mangrove tidak tampak di pasar. Bila hanya kayu dan ikan yang dihitung, mangrove tampak \"murah\" sehingga mudah dikonversi menjadi tambak, padahal kerugian jasa lingkungannya besar.\n\nPengecoh: 31,3% adalah porsi nilai guna langsung. 46,9% hanya menghitung pelindung pantai. 6,3% adalah porsi nilai keberadaan atau kayu. 78,1% menjumlahkan komponen yang salah.",
      f_tev),
    Q("Sebuah pabrik membuang limbah ke sungai sehingga petambak di hilir merugi, tetapi kerugian itu tidak dihitung dalam biaya produksi pabrik. Instrumen ekonomi yang paling tepat untuk menginternalisasi dampak tersebut adalah …",
      ["Pajak atau pungutan pencemaran sebesar biaya kerusakan yang ditimbulkan", "Subsidi bahan baku agar pabrik dapat berproduksi lebih banyak",
       "Pembebasan pajak bagi pabrik yang berlokasi di dekat sungai", "Menaikkan harga ikan dari tambak agar petambak memperoleh untung",
       "Memindahkan petambak ke lokasi lain tanpa mengubah perilaku pabrik"],
      "Kerugian petambak adalah eksternalitas negatif: biaya yang ditanggung pihak lain di luar transaksi pasar pabrik. Karena tidak masuk biaya produksi, pabrik cenderung mencemari secara berlebihan. Pajak Pigou atau pungutan pencemaran membuat pabrik menanggung biaya kerusakan tersebut (prinsip pencemar membayar), sehingga terdorong mengurangi limbah atau mengolahnya. Contoh sejenis adalah pajak karbon untuk emisi gas rumah kaca.\n\nPengecoh: subsidi bahan baku justru menambah produksi dan pencemaran. Pembebasan pajak tidak mengubah perilaku pencemar. Menaikkan harga ikan tidak mengatasi sumber masalah. Memindahkan petambak hanya memindahkan korban tanpa menghentikan pencemaran.",
      None),
    Q("Perhatikan tabel skor kesesuaian lokasi PLTS berikut. Nilai kesesuaian N = Σ(bobot × skor).\n\nLokasi yang paling sesuai beserta nilainya adalah …",
      ["Lokasi C, dengan nilai 4,35", "Lokasi A, dengan nilai 4,15", "Lokasi B, dengan nilai 4,30", "Lokasi A, dengan nilai 4,50",
       "Lokasi B, dengan nilai 4,25"],
      "Hitung nilai tiap lokasi:\n• A = (0,40 × 5) + (0,20 × 4) + (0,25 × 3) + (0,15 × 4) = 2,00 + 0,80 + 0,75 + 0,60 = 4,15.\n• B = (0,40 × 4) + (0,20 × 5) + (0,25 × 5) + (0,15 × 3) = 1,60 + 1,00 + 1,25 + 0,45 = 4,30.\n• C = (0,40 × 5) + (0,20 × 3) + (0,25 × 4) + (0,15 × 5) = 2,00 + 0,60 + 1,00 + 0,75 = 4,35.\nLokasi C paling sesuai.\n\nPengecoh: A memiliki radiasi tertinggi bersama C, tetapi jaraknya ke jaringan buruk sehingga nilainya terendah. B unggul pada dua kriteria, tetapi radiasinya lebih rendah. Nilai 4,50 dan 4,25 berasal dari salah mengalikan bobot. Analisis multikriteria seperti ini lazim dipakai dalam SIG untuk pemilihan lokasi.",
      f_pltsskor),
    Q("Konflik antara masyarakat adat dan perusahaan tambang yang mendapat izin dari pemerintah di wilayah yang diklaim sebagai tanah ulayat termasuk tipe konflik …",
      ["Vertikal, karena melibatkan masyarakat dengan negara dan korporasi", "Horizontal, karena terjadi antara dua kelompok masyarakat yang setara",
       "Internal, karena hanya terjadi di dalam satu kelompok masyarakat adat", "Lintas batas negara, karena melibatkan dua negara bertetangga",
       "Antargenerasi, karena hanya melibatkan generasi tua dan generasi muda"],
      "Konflik sumber daya dapat dikelompokkan berdasarkan pihak yang terlibat:\n• Konflik vertikal: antara masyarakat dengan pihak yang memiliki kekuasaan lebih besar, yaitu negara atau korporasi pemegang izin. Contohnya konflik tanah ulayat dengan konsesi tambang atau perkebunan.\n• Konflik horizontal: antarkelompok masyarakat yang relatif setara, misalnya antarnelayan atau antardesa berebut lahan.\nKasus pada soal melibatkan masyarakat adat dengan perusahaan dan izin pemerintah, sehingga tergolong vertikal. Penyelesaiannya memerlukan pengakuan hak, prinsip persetujuan atas dasar informasi di awal tanpa paksaan (FPIC), dan mekanisme pembagian manfaat.\n\nPengecoh: tidak ada dua kelompok masyarakat setara, bukan konflik internal, tidak lintas negara, dan bukan konflik antargenerasi.",
      None),
    Q("Perhatikan diagram keterkaitan nexus air–energi–pangan berikut.\n\nPersaingan penggunaan minyak sawit untuk biodiesel dengan kebutuhan minyak goreng paling tepat digambarkan oleh panah …",
      ["3", "1", "2", "1 dan 2", "Tidak ada panah yang sesuai"],
      "Panah pada diagram: (1) energi → air, misalnya listrik untuk memompa air irigasi dan mengolah air bersih; (2) air → pangan, misalnya air irigasi untuk sawah; (3) pangan → energi, misalnya tanaman pangan atau minyak nabati yang dipakai sebagai bahan bioenergi.\nPemakaian minyak sawit untuk biodiesel berarti komoditas pangan dialihkan menjadi energi, sehingga berada pada panah 3. Ketika permintaan biodiesel meningkat, pasokan minyak goreng dapat tertekan dan harganya naik (persaingan food vs fuel).\n\nPengecoh: panah 1 dan 2 tidak melibatkan pengalihan pangan menjadi energi. Pendekatan nexus mengajarkan bahwa kebijakan di satu sektor (misalnya energi) dapat berdampak pada sektor lain (pangan dan air), sehingga perlu dikelola terpadu.",
      f_nexus),
    Q("Dana Bagi Hasil (DBH) sumber daya alam dalam sistem desentralisasi fiskal Indonesia dimaksudkan untuk …",
      ["Memberi bagian penerimaan negara dari SDA kepada daerah penghasil dan daerah sekitarnya", "Menyerahkan seluruh hasil tambang kepada perusahaan swasta di daerah penghasil",
       "Menghapus pajak bagi perusahaan tambang yang beroperasi di daerah terpencil", "Memindahkan seluruh penerimaan SDA ke pemerintah pusat tanpa pembagian",
       "Membiayai impor energi bagi daerah yang tidak memiliki sumber daya alam"],
      "DBH SDA adalah bagian penerimaan negara dari minyak bumi, gas bumi, pertambangan mineral dan batu bara, kehutanan, perikanan, dan panas bumi yang dialokasikan kepada daerah berdasarkan persentase tertentu. Daerah penghasil memperoleh porsi lebih besar, sedangkan daerah lain dalam provinsi yang sama juga mendapat bagian. Tujuannya mengurangi ketimpangan fiskal dan memberi kompensasi atas dampak eksploitasi di daerah penghasil.\nTantangannya, DBH yang besar dapat menimbulkan ketergantungan fiskal dan rawan salah kelola, mirip gejala kutukan sumber daya di tingkat daerah.\n\nPengecoh: DBH bukan penyerahan hasil tambang ke swasta, bukan penghapusan pajak, bukan sentralisasi penuh, dan bukan dana impor energi.",
      None),
    Q("Perhatikan diagram pencar ketergantungan ekspor SDA mentah dan pertumbuhan ekonomi beberapa negara berikut.\n\nGejala yang ditunjukkan grafik dan penjelasannya adalah …",
      ["Kutukan sumber daya; ketergantungan ekspor SDA mentah diikuti pertumbuhan rendah",
       "Tragedi kepemilikan bersama; semakin banyak SDA, semakin cepat pertumbuhan ekonomi negara",
       "Kurva Hubbert; pertumbuhan ekonomi naik bersamaan dengan porsi ekspor SDA mentah",
       "Kutukan sumber daya; negara tanpa SDA pasti mengalami pertumbuhan paling rendah",
       "Hilirisasi; negara dengan porsi ekspor SDA mentah tinggi selalu lebih makmur"],
      "Grafik menunjukkan hubungan negatif: negara dengan porsi ekspor SDA mentah tinggi (misalnya G dan H, 52–60% PDB) memiliki pertumbuhan PDB per kapita rendah (±0,5–0,8%/tahun), sedangkan negara dengan porsi kecil (A dan B) tumbuh lebih cepat (±4%). Gejala ini disebut kutukan sumber daya (resource curse). Penjelasannya antara lain: penyakit Belanda (Dutch disease) yang melemahkan sektor industri dan pertanian, volatilitas harga komoditas, korupsi dan pencarian rente, serta lemahnya investasi pada sumber daya manusia.\n\nPengecoh: tragedi kepemilikan bersama tidak terkait pertumbuhan negara. Kurva Hubbert menjelaskan produksi SDA. Grafik tidak menyatakan negara tanpa SDA pasti tumbuh paling rendah. Hilirisasi justru upaya keluar dari ketergantungan ekspor mentah.",
      f_curse),
    Q("Ekonomi sirkular dalam pengelolaan sumber daya mineral untuk baterai kendaraan listrik paling tepat diwujudkan melalui …",
      ["Daur ulang baterai bekas untuk memperoleh kembali nikel, kobalt, dan litium", "Membuang baterai bekas ke TPA agar bahan bakunya kembali ke alam",
       "Menambah izin tambang baru setiap kali permintaan baterai meningkat", "Mengekspor seluruh baterai bekas tanpa pengolahan ke negara lain",
       "Membakar baterai bekas untuk menghasilkan listrik di PLTU"],
      "Ekonomi sirkular berupaya mempertahankan nilai material selama mungkin melalui prinsip reduce, reuse, recycle, dan pemulihan bahan. Untuk baterai kendaraan listrik, baterai bekas dapat dipakai ulang (second life) sebagai penyimpan energi stasioner, lalu didaur ulang untuk memperoleh kembali logam bernilai seperti nikel, kobalt, mangan, dan litium. Cara ini mengurangi kebutuhan tambang baru, limbah berbahaya, dan ketergantungan pada impor bahan baku.\n\nPengecoh: membuang baterai ke TPA mencemari tanah dan air. Menambah tambang baru adalah pola ekonomi linear. Ekspor baterai bekas tanpa pengolahan memindahkan masalah dan kehilangan nilai material. Membakar baterai berbahaya dan bukan pemulihan material.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
