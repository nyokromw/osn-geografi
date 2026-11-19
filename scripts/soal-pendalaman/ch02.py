from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_risk3(path):
    bars(["Desa X", "Desa Y", "Desa Z"], {"Bahaya (H)": [0.8, 0.6, 0.9], "Kerentanan (V)": [0.6, 0.8, 0.5],
                                          "Kapasitas (C)": [0.4, 0.8, 0.5]}, path,
         title="Nilai komponen risiko tiga desa (skala 0–1)", ylabel="Nilai", values=True, ylim=(0, 1.25), w=8.5, legend_loc="upper left")


def f_seismo(path):
    t = np.linspace(0, 400, 4000)
    rnd = np.random.RandomState(1)
    y = 0.05 * rnd.randn(len(t))
    tp, ts = 60, 255
    y += (t > tp) * 0.6 * np.exp(-(t - tp) / 60) * np.sin(2 * np.pi * (t - tp) / 2.2) * (t < 400)
    y += (t > ts) * 1.6 * np.exp(-(t - ts) / 50) * np.sin(2 * np.pi * (t - ts) / 4) * (t < 400)
    fig, ax = new(9.5, 3.8)
    ax.plot(t, y, color="#2D3748", lw=0.7)
    for x, n in [(tp, "P tiba\n08:14:20"), (ts, "S tiba\n08:17:35")]:
        ax.axvline(x, color=C["red"], ls="--", lw=1.2)
        ax.text(x + 3, -1.75, n, fontsize=10, color=C["red"], va="bottom")
    ax.set_yticks([]); ax.set_xlabel("Waktu (detik sejak 08:13:20)")
    ax.set_title("Seismogram di Stasiun Q")
    save(fig, path)


def f_krb(path):
    fig, ax = blank(7.5, 6.3, (0, 100), (0, 84))
    ax.add_patch(Circle((50, 45), 34, fc="#FEFCBF", ec="#B7791F"))
    ax.add_patch(Circle((50, 45), 20, fc="#FBD38D", ec="#C05621"))
    ax.add_patch(Circle((50, 45), 9, fc="#FC8181", ec="#C53030"))
    for xs, ys in [([50, 44, 36, 26, 14, 4], [45, 30, 18, 10, 4, 1]), ([50, 62, 72, 84, 96], [45, 32, 22, 14, 7])]:
        ax.plot(xs, ys, color=C["blue"], lw=2)
        ax.fill_between(xs, np.array(ys) - 2.2, np.array(ys) + 2.2, color="#FEFCBF", ec="#B7791F", lw=0.6, zorder=0.5)
    ax.plot(50, 45, "^", ms=16, color="#742A2A")
    ax.text(50, 49.5, "KRB III", ha="center", fontsize=10, fontweight="bold")
    ax.text(50, 59, "KRB II", ha="center", fontsize=10, fontweight="bold")
    ax.text(50, 73, "KRB I", ha="center", fontsize=10, fontweight="bold")
    ax.text(6, 7, "Sungai\nX", fontsize=10, color=C["blue"])
    ax.text(90, 11, "Sungai\nY", fontsize=10, color=C["blue"])
    ax.set_title("Peta Kawasan Rawan Bencana (KRB) gunung api G (disederhanakan)")
    save(fig, path)


def f_hidro(path):
    t = np.arange(0, 25, 0.5)
    def h(tp, qp, k):
        return 15 + qp * (t / tp) ** k * np.exp(k * (1 - t / tp))
    lines(t, {"Tahun 2000 (hutan 70%)": h(10, 85, 3), "Tahun 2023 (hutan 25%, permukiman meluas)": h(6, 190, 3)}, path,
          title="Hidrograf sungai X untuk hujan yang sama", xlabel="Jam sejak hujan mulai", ylabel="Debit (m³/s)",
          markers=False, w=9)


def f_tektonik(path):
    fig, ax = indonesia_map(extent=(93, 142, -13, 8), w=10, h=5)
    tr = [(94.5, 6), (96.5, 2), (99.5, -2.5), (103, -6.3), (106, -8.6), (112, -10.3), (118, -11.2), (122, -11.3)]
    ax.plot(*zip(*tr), color=C["red"], lw=2.5)
    for i in range(0, len(tr) - 1):
        (x0, y0), (x1, y1) = tr[i], tr[i + 1]
        for f_ in np.linspace(0.2, 0.8, 3):
            x, y = x0 + f_ * (x1 - x0), y0 + f_ * (y1 - y0)
            dx, dy = x1 - x0, y1 - y0; nrm = np.hypot(dx, dy)
            ax.plot([x, x - 0.5 * dy / nrm], [y, y + 0.5 * dx / nrm], color=C["red"], lw=2)
    sf = [(95.5, 5.3), (97.5, 3.0), (99.5, 0.5), (101.5, -2.0), (103.5, -4.0), (105.0, -5.6)]
    ax.plot(*zip(*sf), color=C["purple"], lw=2.2, ls="--")
    so = [(124.5, 0.2), (128, -1.2), (131.5, -1.0), (134, -1.6)]
    ax.plot(*zip(*so), color=C["purple"], lw=2.2, ls="--")
    fl = [(115.5, -7.4), (119, -7.6), (122.5, -7.6), (125.5, -7.4)]
    ax.plot(*zip(*fl), color=C["orange"], lw=2.5)
    for t, (x, y) in {"P": (106.5, -10.3), "R": (99.3, 1.4), "S": (120.5, -6.6), "T": (129.5, 0.2)}.items():
        ax.text(x, y, t, fontsize=15, fontweight="bold", ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="#2D3748"))
    ax.set_title("Beberapa struktur tektonik utama di Indonesia (disederhanakan)")
    save(fig, path)


def f_rob2(path):
    bars(["Amblesan tanah", "Kenaikan muka laut"], {"Laju (mm/tahun)": [75, 3]}, path,
         title="Laju rata-rata dua proses di pesisir Kota J", ylabel="mm per tahun", values=True, ylim=(0, 90),
         colors=[C["brown"]], w=7)


# ---- paket 1
STA = {"A": (18, 70), "B": (84, 72), "C": (52, 12)}
EPI = (44, 52)


def f_triang(path):
    fig, ax = blank(7.5, 6.5, (0, 100), (0, 90))
    for n, (x, y) in STA.items():
        r = np.hypot(x - EPI[0], y - EPI[1])
        ax.add_patch(Circle((x, y), r, fc="none", ec=C["blue"], lw=1.4, ls="--"))
        ax.plot(x, y, "^", ms=12, color=C["blue"]); ax.text(x + 2, y + 2, f"Stasiun {n}", fontsize=11, fontweight="bold", color=C["blue"])
    cand = {"P": (30, 38), "Q": (60, 50), "R": EPI, "S": (40, 70), "T": (66, 30)}
    for n, (x, y) in cand.items():
        ax.plot(x, y, "o", ms=7, color=C["red"]); ax.text(x + 1.5, y - 4, n, fontsize=13, fontweight="bold", color=C["red"])
    ax.set_xlim(-10, 110); ax.set_ylim(-15, 95)
    ax.set_title("Lingkaran jarak episentrum dari tiga stasiun")
    save(fig, path)


def f_benioff(path):
    rnd = np.random.RandomState(4)
    x = rnd.uniform(0, 400, 120)
    depth = 0.55 * x + rnd.normal(0, 12, 120)
    depth = np.clip(depth, 5, None)
    shallow = rnd.uniform(0, 400, 25); sd = rnd.uniform(5, 30, 25)
    fig, ax = new(9, 4.8)
    ax.scatter(x, depth, s=16, color=C["red"], alpha=0.8)
    ax.scatter(shallow, sd, s=16, color=C["red"], alpha=0.8)
    ax.invert_yaxis(); ax.set_xlabel("Jarak dari palung ke arah utara (km)"); ax.set_ylabel("Kedalaman hiposentrum (km)")
    ax.text(5, 245, "SELATAN\n(Samudra Hindia)", fontsize=10); ax.text(320, 245, "UTARA\n(Pulau Jawa)", fontsize=10)
    ax.set_ylim(260, 0); ax.grid(color="#EDF2F7")
    ax.set_title("Sebaran hiposentrum gempa pada penampang selatan–utara Jawa")
    save(fig, path)


def f_tide(path):
    t = np.arange(0, 60, 0.5)
    y = 0.3 * np.sin(2 * np.pi * t / 600)
    y = y - 1.2 * np.exp(-((t - 22) / 4) ** 2) + 3.0 * np.exp(-((t - 31) / 3.2) ** 2)
    fig, ax = new(9, 4)
    ax.plot(t, y, color=C["blue"], lw=2.2)
    ax.axvline(8, color=C["red"], ls="--"); ax.text(8.5, 2.8, "gempa\n(menit 8)", fontsize=10, color=C["red"])
    ax.axhline(0, color="#A0AEC0", lw=1)
    ax.set_xlabel("Menit"); ax.set_ylabel("Tinggi muka laut (m)"); ax.grid(color="#EDF2F7")
    ax.set_title("Rekaman tide gauge di sebuah pelabuhan")
    save(fig, path)


HOUSES = {"K": 400, "L": 650, "M": 850, "N": 1050, "O": 1300}


def f_evak(path):
    fig, ax = blank(9.5, 4.6, (0, 140), (0, 60))
    ax.add_patch(Rectangle((0, 0), 22, 60, fc=C["lblue"], ec="none")); ax.text(11, 30, "Laut", ha="center", fontsize=12, rotation=90)
    ax.add_patch(Polygon([(118, 0), (140, 0), (140, 60), (118, 60), (124, 30)], fc="#9AE6B4", ec="#2F855A"))
    ax.text(131, 30, "Bukit\naman\n(+30 m)", ha="center", fontsize=10)
    ax.plot([22, 122], [30, 30], color="#718096", lw=6, solid_capstyle="butt")
    ax.text(40, 33.5, "Jalan evakuasi", ha="center", fontsize=9, color=C["gray"])
    for i, (n, d) in enumerate(HOUSES.items()):
        x = 122 - d / 1500 * 100
        y = 42 if i % 2 == 0 else 16
        ax.add_patch(Rectangle((x - 3, y - 3), 6, 6, fc=C["orange"], ec="black"))
        ax.text(x, y + 6, n, ha="center", fontsize=13, fontweight="bold")
        ax.text(x, y - 7.5, f"{d} m", ha="center", fontsize=10)
        ax.plot([x, x], [y + (-3 if y > 30 else 3), 30], color="#A0AEC0", lw=1)
    ax.set_title("Jarak tempuh rumah ke bukit aman melalui jalan")
    save(fig, path)


def f_bor(path):
    fig, axs = plt.subplots(1, 3, figsize=(9, 4.8), sharey=True)
    logs = {"Lokasi K": [(0, 1, "#C6A77B", "tanah urug"), (1, 9, "#F6E05E", "pasir lepas\nhalus")],
            "Lokasi L": [(0, 2, "#C6A77B", "tanah urug"), (2, 9, "#A0522D", "lempung\npadat")],
            "Lokasi M": [(0, 3, "#C6A77B", "tanah urug"), (3, 9, "#D69E2E", "pasir padat\n& kerikil")]}
    mat = {"Lokasi K": 1.0, "Lokasi L": 1.5, "Lokasi M": 8.0}
    for a, (n, ls) in zip(axs, logs.items()):
        for z0, z1, c, lab in ls:
            a.add_patch(Rectangle((0, z0), 1, z1 - z0, fc=c, ec="black"))
            a.text(0.5, (z0 + z1) / 2, lab, ha="center", va="center", fontsize=10)
        a.axhline(mat[n], color=C["blue"], lw=2.5, ls="--")
        a.text(1.02, mat[n], "▼ MAT", color=C["blue"], fontsize=9, va="center")
        a.set_xlim(0, 1.35); a.set_xticks([]); a.set_title(n)
        for s in ["top", "right", "bottom"]:
            a.spines[s].set_visible(False)
    axs[0].set_ylim(9, 0); axs[0].set_ylabel("Kedalaman (m)")
    fig.suptitle("Log bor tiga lokasi (MAT = muka air tanah)", fontweight="bold")
    save(fig, path)


# ---- paket 2
def f_volc3(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 6); a.axis("off")
    axs[0].add_patch(Polygon([(0, 0.5), (5, 1.6), (10, 0.5)], fc="#6B4226")); axs[0].set_title("X")
    axs[0].text(5, 0.2, "lereng sangat landai, lava encer", ha="center", fontsize=9)
    axs[1].add_patch(Polygon([(0.5, 0.5), (4.3, 5.2), (5.7, 5.2), (9.5, 0.5)], fc="#8B5A2B"))
    for y in [1.5, 2.6, 3.7]:
        axs[1].plot([5 - (5.2 - y) * 0.8 - 0.3, 5 + (5.2 - y) * 0.8 + 0.3], [y, y], color="#F6E05E", lw=1.5)
    axs[1].set_title("Y"); axs[1].text(5, 0.05, "lereng curam, berlapis lava–piroklastik", ha="center", fontsize=9)
    axs[2].add_patch(Polygon([(0, 0.5), (2.5, 3.2), (3.5, 3.2), (4, 1.3), (6, 1.3), (6.5, 3.2), (7.5, 3.2), (10, 0.5)], fc="#8B5A2B"))
    axs[2].add_patch(Polygon([(4, 1.3), (6, 1.3), (5.8, 1.9), (4.2, 1.9)], fc=C["lblue"]))
    axs[2].set_title("Z"); axs[2].text(5, 0.05, "cekungan sangat lebar di puncak", ha="center", fontsize=9)
    save(fig, path)


def f_prekursor(path):
    d = np.arange(1, 31)
    vt = np.array([3, 2, 4, 3, 5, 4, 6, 5, 8, 9, 12, 11, 15, 18, 22, 25, 31, 38, 45, 52, 60, 66, 75, 88, 96, 110, 118, 130, 142, 150])
    edm = 4200 - np.cumsum(np.r_[0, np.clip((d[1:] - 10) * 0.12, 0, None)])
    fig, ax = new(9, 4.4)
    ax.bar(d, vt, color=C["orange"], label="Gempa vulkanik dalam (kejadian/hari)")
    ax.set_ylabel("Gempa vulkanik/hari"); ax.set_xlabel("Hari ke-")
    ax2 = ax.twinx(); ax2.plot(d, edm, color=C["blue"], lw=2.2, label="Jarak EDM pos–puncak (m)")
    ax2.set_ylabel("Jarak EDM (m)", color=C["blue"]); ax2.spines["top"].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center left", frameon=False, fontsize=10)
    ax.set_title("Data pemantauan gunung api G selama 30 hari")
    save(fig, path)


def f_skor(path):
    table([["Kemiringan lereng", "0,30", "4"], ["Curah hujan tahunan", "0,25", "5"], ["Jenis tanah/batuan", "0,20", "3"],
           ["Tutupan lahan", "0,15", "4"], ["Jarak dari sesar", "0,10", "2"]],
          ["Parameter", "Bobot", "Skor lereng S (1–5)"], path, title="Parameter kerawanan longsor lereng S",
          col_w=[0.46, 0.2, 0.34])


def f_creep(path):
    fig, ax = blank(9, 4.6, (0, 100), (0, 50))
    xs = np.array([0, 100]); ax.fill_between([0, 100], [0, 0], [44, 6], color="#C6A77B")
    for i, x in enumerate([15, 32, 50, 68, 85]):
        y = 44 - 0.38 * x
        ang = np.radians(18)
        if i % 2 == 0:
            ax.plot([x, x + 9 * np.sin(ang)], [y, y + 9 * np.cos(ang)], color="#4A5568", lw=3)
        else:
            ax.plot([x, x + 6 * np.sin(ang)], [y, y + 6 * np.cos(ang)], color="#2F855A", lw=3)
            ax.add_patch(Circle((x + 7 * np.sin(ang), y + 8 * np.cos(ang)), 3, fc="#68D391", ec="#2F855A"))
    for x in [25, 60]:
        y = 44 - 0.38 * x
        ax.plot([x - 3, x + 4], [y - 0.5, y - 3.5], color="#2D3748", lw=1)
    ax.text(70, 40, "Tiang listrik dan batang pohon\nmiring searah lereng;\npagar bergeser perlahan\ndalam beberapa tahun", fontsize=10)
    ax.set_title("Kondisi sebuah lereng hasil pengamatan lapangan")
    save(fig, path)


RAIN = [5, 12, 30, 48, 55, 41, 22, 35]


def f_rain_longsor(path):
    days = [f"H-{7-i}" if i < 7 else "H" for i in range(8)]
    cum = np.cumsum(RAIN)
    fig, ax = new(9, 4.2)
    ax.bar(days, RAIN, color=C["lblue"], edgecolor=C["blue"], label="Hujan harian (mm)")
    for i, v in enumerate(RAIN):
        ax.text(i, v + 2, str(v), ha="center", fontsize=10)
    ax.set_ylabel("Hujan harian (mm)")
    ax2 = ax.twinx(); ax2.plot(days, cum, color=C["red"], marker="o", lw=2, label="Hujan kumulatif (mm)")
    ax2.set_ylabel("Kumulatif (mm)", color=C["red"]); ax2.spines["top"].set_visible(False)
    ax.set_title("Curah hujan sebelum longsor (H = hari longsor terjadi)")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=10)
    save(fig, path)


def f_kontur_lereng(path):
    X, Y, Z = terrain(peaks=((0.55, 0.6, 900, 0.17), (0.2, 0.25, 300, 0.12)), base=100)
    pts = {"P": (0.68, 0.62), "Q": (0.35, 0.85), "R": (0.18, 0.22), "S": (0.85, 0.15), "T": (0.92, 0.88)}
    gy, gx = np.gradient(Z)
    g = np.hypot(gx, gy)
    vals = {k: g[int(v[1] * 199), int(v[0] * 199)] for k, v in pts.items()}
    assert max(vals, key=vals.get) == "P", vals
    contour_map(X, Y, Z, path, interval=50, index_every=4, points=pts, title="Peta kontur (interval 50 m)")


# ---- paket 3
def f_rasional(path):
    table([["Hutan", "40", "0,20"], ["Sawah", "30", "0,40"], ["Permukiman", "30", "0,80"]],
          ["Penggunaan lahan", "Luas (%)", "Koefisien limpasan C"], path,
          title="Penggunaan lahan DAS Y (luas 25 km²)", col_w=[0.4, 0.25, 0.35])


AMB = {"A": (1.2, 100), "B": (0.6, 30), "C": (0.9, 80), "D": (0.4, 10)}


def f_amblesan(path):
    table([[k, f"{v[0]:.1f}".replace(".", ","), str(v[1])] for k, v in AMB.items()],
          ["Kawasan", "Elevasi di atas pasang (m)", "Laju amblesan (mm/tahun)"], path,
          title="Empat kawasan pesisir (kenaikan muka laut 4 mm/tahun)", col_w=[0.2, 0.4, 0.4])


def f_hotspot(path):
    bars(BULAN3, {"Tahun normal": [5, 4, 8, 10, 15, 30, 60, 120, 150, 90, 20, 8],
                   "Tahun El Niño": [6, 5, 9, 14, 25, 60, 180, 520, 1250, 980, 140, 12]}, path,
         title="Jumlah titik panas (hotspot) bulanan di Kalimantan Tengah", ylabel="Jumlah titik panas", w=9.5)


def f_karst(path):
    fig, ax = blank(9.5, 4.8, (0, 100), (0, 52))
    xs = np.linspace(0, 100, 200); top = 38 + 4 * np.abs(np.sin(xs / 6))
    ax.fill_between(xs, 0, top, color="#E2E8F0", ec="#718096")
    for x in [18, 46, 74]:
        ax.add_patch(Polygon([(x - 5, 42), (x + 5, 42), (x + 1, 34), (x - 1, 34)], fc="white", ec="#718096"))
        ax.plot([x, x], [34, 16], color=C["blue"], lw=1.5, ls=":")
    ax.plot(np.linspace(5, 95, 50), 14 + 2 * np.sin(np.linspace(0, 6, 50)), color=C["blue"], lw=5)
    ax.text(50, 9, "sungai bawah tanah", ha="center", fontsize=10, color=C["blue"])
    for x in range(10, 96, 6):
        ax.plot([x, x - 1.2], [51, 47.5], color=C["blue"], lw=1)
    ax.text(97, 49, "hujan", fontsize=9, color=C["blue"], ha="right")
    ax.text(18, 44.5, "doline", ha="center", fontsize=9)
    ax.text(95, 26, "batu gamping\nberongga", ha="right", fontsize=9)
    ax.set_title("Penampang kawasan karst Gunung Sewu")
    save(fig, path)


HTH = {"Kab. A": 14, "Kab. B": 27, "Kab. C": 45, "Kab. D": 68, "Kab. E": 8}


def f_hth(path):
    bars(list(HTH), {"Hari tanpa hujan berturut-turut": list(HTH.values())}, path,
         title="Hari Tanpa Hujan (HTH) berturut-turut per 31 Agustus", ylabel="hari", values=True, ylim=(0, 80),
         colors=[C["orange"]], w=8)


def f_lahan_das(path):
    fig, axs = plt.subplots(1, 2, figsize=(9, 4.2))
    lab = ["Hutan", "Kebun campur", "Pertanian semusim", "Permukiman"]
    cols = [C["green"], C["lgreen"], C["yellow"], C["red"]]
    for a, d, t in zip(axs, [[62, 18, 15, 5], [24, 14, 40, 22]], ["Hulu DAS Z, 2003", "Hulu DAS Z, 2023"]):
        a.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=cols, startangle=90,
              wedgeprops=dict(ec="white"), textprops=dict(fontsize=9))
        a.set_title(t)
    save(fig, path)


# ---- paket 4
def f_siklus(path):
    fig, ax = blank(7.5, 6.3, (-50, 50), (-46, 46))
    names = [("P", "Pencegahan\n& mitigasi"), ("Q", "Kesiapsiagaan"), ("R", "Tanggap\ndarurat"), ("S", "Rehabilitasi"), ("T", "Rekonstruksi")]
    for i, (k, n) in enumerate(names):
        a = np.radians(90 - i * 72)
        x, y = 30 * np.cos(a), 30 * np.sin(a)
        ax.add_patch(Circle((x, y), 11.5, fc="#EBF8FF", ec=C["blue"], lw=1.6))
        ax.text(x, y + 3.5, k, ha="center", fontsize=15, fontweight="bold", color=C["blue"])
        ax.text(x, y - 3, n, ha="center", va="center", fontsize=8.5)
        a2 = np.radians(90 - i * 72 - 36)
        ax.annotate("", xy=(33 * np.cos(a2 - 0.25), 33 * np.sin(a2 - 0.25)), xytext=(33 * np.cos(a2 + 0.25), 33 * np.sin(a2 + 0.25)),
                    arrowprops=dict(arrowstyle="-|>", lw=1.8, color=C["gray"]))
    ax.text(0, 0, "★\nBencana", ha="center", va="center", fontsize=11, color=C["red"], fontweight="bold")
    ax.set_title("Siklus penanggulangan bencana")
    save(fig, path)


def f_ews(path):
    fig, ax = blank(10, 3, (0, 100), (0, 24))
    items = ["Pengetahuan\nrisiko", "Pemantauan &\nlayanan peringatan", "?", "Kemampuan\nrespons masyarakat"]
    for i, t in enumerate(items):
        box(ax, 2 + i * 25, 6, 20, 12, t, fc="#FEFCBF" if t == "?" else "#EBF8FF", fs=11 if t != "?" else 22, bold=(t == "?"))
        if i < 3:
            arrow(ax, 22.8 + i * 25, 12, 26.6 + i * 25, 12)
    ax.set_title("Empat unsur sistem peringatan dini yang berpusat pada masyarakat")
    save(fig, path)


def f_bnpb(path):
    cats = ["Banjir", "Cuaca\nekstrem", "Tanah\nlongsor", "Karhutla", "Kekeringan", "Gempa\nbumi", "Erupsi"]
    freq = [1250, 1260, 590, 530, 170, 30, 5]
    death = [98, 21, 63, 2, 0, 330, 2]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
    axs[0].barh(cats, freq, color=C["blue"]); axs[0].invert_yaxis(); axs[0].set_title("Jumlah kejadian")
    axs[1].barh(cats, death, color=C["red"]); axs[1].invert_yaxis(); axs[1].set_title("Korban meninggal")
    for a, d in zip(axs, [freq, death]):
        for i, v in enumerate(d):
            a.text(v, i, f" {v}", va="center", fontsize=9)
        a.set_xlim(0, max(d) * 1.2)
    fig.suptitle("Kejadian bencana di Indonesia dalam satu tahun (data ilustrasi)", fontweight="bold")
    save(fig, path)


def f_puting(path):
    fig, ax = blank(7, 5.2, (0, 100), (0, 80))
    ax.add_patch(Ellipse((50, 66), 80, 16, fc="#A0AEC0", ec="#4A5568"))
    ax.add_patch(Polygon([(18, 66), (82, 66), (90, 74), (10, 74)], fc="#CBD5E0", ec="#4A5568"))
    ax.add_patch(Polygon([(44, 58), (56, 58), (52, 8), (49, 8)], fc="#718096", alpha=0.85))
    ax.add_patch(Rectangle((0, 0), 100, 8, fc="#C6A77B"))
    for y in [45, 30, 18]:
        ax.add_patch(Ellipse((51, y), 14, 3.5, fc="none", ec="white", lw=1.4))
    ax.text(50, 72, "awan cumulonimbus", ha="center", fontsize=10)
    ax.text(75, 30, "pusaran angin\nberdiameter puluhan–\nratusan meter,\nberlangsung < 10 menit", fontsize=9)
    ax.set_title("Fenomena cuaca ekstrem lokal")
    save(fig, path)


def f_abrasi(path):
    fig, ax = blank(9, 4.8, (0, 100), (0, 52))
    ax.add_patch(Rectangle((0, 0), 100, 52, fc=C["lblue"]))
    x = np.linspace(0, 100, 100)
    l2005 = 30 + 2 * np.sin(x / 9); l2020 = l2005 + 12 * np.exp(-((x - 50) / 22) ** 2)
    ax.fill_between(x, l2020, 52, color=C["land"])
    ax.plot(x, l2005, color=C["green"], lw=2.2, ls="--", label="Garis pantai 2005 (bermangrove)")
    ax.plot(x, l2020, color=C["red"], lw=2.2, label="Garis pantai 2020 (mangrove ditebang untuk tambak)")
    ax.annotate("", xy=(50, l2020[50]), xytext=(50, l2005[50]), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(52, (l2005[50] + l2020[50]) / 2, "?", fontsize=14, fontweight="bold")
    scalebar(ax, 6, 4, 24, "0 ——— 240 m", h=1.2)
    ax.text(10, 10, "Laut", fontsize=11)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.9)
    ax.set_title("Perubahan garis pantai Desa M")
    save(fig, path)


# ---- paket 5
GH = np.array([[0.9, 0.8, 0.4], [0.7, 0.6, 0.3], [0.5, 0.4, 0.2]])
GV = np.array([[0.3, 0.7, 0.8], [0.5, 0.9, 0.6], [0.8, 0.6, 0.4]])
GC = np.array([[0.6, 0.4, 0.5], [0.3, 0.5, 0.6], [0.8, 0.4, 0.5]])


def f_overlay(path):
    R = GH * GV / GC
    assert np.unravel_index(R.argmax(), R.shape) == (0, 1), R
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.8))
    for a, G, t, cm in zip(axs, [GH, GV, GC], ["Bahaya (H)", "Kerentanan (V)", "Kapasitas (C)"], ["Reds", "Oranges", "Greens"]):
        a.imshow(G, cmap=cm, vmin=0, vmax=1.3)
        for i in range(3):
            for j in range(3):
                a.text(j, i, f"{G[i, j]:.1f}".replace(".", ","), ha="center", va="center", fontsize=12, fontweight="bold")
        a.set_xticks(range(3)); a.set_xticklabels(["1", "2", "3"]); a.set_yticks(range(3)); a.set_yticklabels(["a", "b", "c"])
        a.set_title(t)
    fig.suptitle("Tiga lapisan raster (sel diberi kode baris–kolom, misalnya a1)", fontweight="bold")
    save(fig, path)


BLD_IN = [(14, 5), (22, -8), (30, 9), (41, -3), (50, 7), (58, -9), (67, 4), (78, -6), (90, 8)]
BLD_OUT = [(18, 20), (35, -17), (46, 22), (62, -19), (72, 18), (85, -16), (94, -20)]
BLD = [(x, 38 + 6 * np.sin(x / 12) + d) for x, d in BLD_IN + BLD_OUT]


def f_buffer(path):
    fig, ax = blank(9, 5.4, (0, 100), (0, 75))
    xs = np.linspace(0, 100, 200); ys = 38 + 6 * np.sin(xs / 12)
    ax.fill_between(xs, ys - 12, ys + 12, color="#FED7D7", alpha=0.8, label="Sempadan 100 m")
    ax.plot(xs, ys, color=C["blue"], lw=3, label="Sungai")
    inside = 0
    for (x, y) in BLD:
        yr = 38 + 6 * np.sin(x / 12)
        ins = abs(y - yr) <= 12
        inside += ins
        ax.add_patch(Rectangle((x - 1.6, y - 1.6), 3.2, 3.2, fc="#2D3748"))
    assert inside == 9, inside
    scalebar(ax, 70, 3, 24, "0 ———— 200 m", h=1.2)
    ax.legend(loc="upper left", fontsize=9)
    ax.set_title("Hasil analisis penyangga (buffer) sungai dan sebaran bangunan (■)")
    save(fig, path)


def f_gender(path):
    groups = ["0–9", "10–19", "20–29", "30–39", "40–49", "50–59", "60+"]
    bars(groups, {"Laki-laki": [18, 12, 9, 10, 12, 16, 24], "Perempuan": [27, 20, 22, 25, 26, 30, 38]}, path,
         title="Persentase penduduk yang meninggal di desa terdampak tsunami (ilustrasi)", ylabel="% dari kelompok",
         xlabel="Kelompok umur (tahun)", w=9)


RM = {"Banjir": (5, 3), "Longsor": (4, 4), "Gempa": (2, 5), "Kekeringan": (3, 2), "Erupsi": (1, 4)}


def f_matrix(path):
    fig, ax = new(7, 6)
    cm = np.add.outer(np.arange(1, 6), np.arange(1, 6))
    ax.imshow(cm, origin="lower", cmap="RdYlGn_r", extent=(0.5, 5.5, 0.5, 5.5), alpha=0.6)
    for n, (l, i) in RM.items():
        ax.plot(l, i, "o", ms=11, color="black"); ax.text(l + 0.12, i + 0.15, n, fontsize=11, fontweight="bold")
    ax.set_xlabel("Kemungkinan terjadi (1 = sangat jarang, 5 = sangat sering)")
    ax.set_ylabel("Dampak (1 = sangat kecil, 5 = sangat besar)")
    ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
    ax.set_title("Matriks risiko Kabupaten Q")
    save(fig, path)


def f_capacity(path):
    pts = [("A", 0.35, 82), ("B", 0.42, 70), ("C", 0.55, 48), ("D", 0.61, 40), ("E", 0.70, 25), ("F", 0.78, 18), ("G", 0.85, 9)]
    scatter(pts, path, title="Kapasitas daerah dan korban jiwa",
            xlabel="Indeks kapasitas daerah (0–1)", ylabel="Korban jiwa per 100 ribu terdampak", fit=True)


# ============================ questions ============================
P0 = [
    Q("Perhatikan grafik nilai komponen risiko tiga desa berikut. Diketahui risiko R = (H × V) ÷ C, dengan keterpaparan dianggap sama.\n\nUrutan risiko dari yang tertinggi ke terendah adalah …",
      ["X, Z, Y", "Z, X, Y", "X, Y, Z", "Z, Y, X", "Y, X, Z"],
      "Hitung risiko tiap desa:\n• Desa X: (0,8 × 0,6) ÷ 0,4 = 0,48 ÷ 0,4 = 1,20.\n• Desa Y: (0,6 × 0,8) ÷ 0,8 = 0,48 ÷ 0,8 = 0,60.\n• Desa Z: (0,9 × 0,5) ÷ 0,5 = 0,45 ÷ 0,5 = 0,90.\nUrutan: X (1,20) > Z (0,90) > Y (0,60).\n\nPengecoh: Z memiliki bahaya tertinggi (0,9), sehingga orang tergoda menganggapnya paling berisiko. Padahal risiko tidak hanya ditentukan oleh bahaya; kapasitas X yang rendah (0,4) membuat risikonya paling besar. Desa Y, meskipun kerentanannya tinggi, memiliki kapasitas tinggi (0,8) sehingga risikonya paling rendah. Pesan kebijakannya: meningkatkan kapasitas (pelatihan, sistem peringatan, jalur evakuasi) adalah cara efektif menurunkan risiko walaupun bahaya tidak dapat diubah.",
      f_risk3),
    Q("Gempa A bermagnitudo 7,2 dan gempa B bermagnitudo 5,2. Jika setiap kenaikan 1 magnitudo setara dengan energi sekitar 32 kali, energi gempa A kira-kira … energi gempa B.",
      ["1.000 kali", "64 kali", "100 kali", "20 kali", "2 kali"],
      "Selisih magnitudo = 7,2 − 5,2 = 2. Energi berbanding sekitar 32 × 32 ≈ 1.024, atau tepatnya 10^(1,5 × 2) = 10³ = 1.000 kali.\n\nPengecoh: 100 kali adalah perbandingan amplitudo gelombang (10² untuk selisih 2 magnitudo), bukan energi. 64 kali muncul bila 32 dikalikan 2, padahal hubungannya eksponensial. 20 kali dan 2 kali menganggap skala magnitudo linear. Pemahaman ini penting: gempa M 7 tidak \"sedikit lebih besar\" dari M 5, tetapi melepaskan energi ribuan kali lipat.",
      None),
    Q("Perhatikan seismogram di Stasiun Q berikut. Dengan rumus Laska, Δ = [(S − P) − 1] × 1.000 km dengan (S − P) dalam menit, jarak episentrum dari Stasiun Q adalah …",
      ["2.250 km", "3.250 km", "2.000 km", "2.150 km", "195 km"],
      "Waktu tiba gelombang P = 08:14:20 dan gelombang S = 08:17:35. Selisih S − P = 3 menit 15 detik = 3,25 menit.\nΔ = (3,25 − 1) × 1.000 = 2,25 × 1.000 = 2.250 km.\n\nPengecoh: 3.250 km lupa mengurangkan 1. 2.000 km muncul bila detik diabaikan (3 − 1 = 2). 2.150 km muncul jika 3 menit 15 detik keliru ditulis sebagai 3,15 menit. 195 km muncul bila selisih dinyatakan dalam detik (195 detik) lalu dibagi 1.000 tanpa memakai rumus. Selalu ubah detik menjadi pecahan menit (15 detik = 0,25 menit).",
      f_seismo),
    Q("Gempa bawah laut terjadi 300 km dari sebuah kota pantai. Kedalaman laut rata-rata di antara keduanya 4.000 m. Dengan v = √(g × d) dan g = 9,8 m/s², gelombang tsunami diperkirakan tiba di kota tersebut sekitar …",
      ["25 menit setelah gempa", "42 menit setelah gempa", "13 menit setelah gempa", "75 menit setelah gempa", "4 menit setelah gempa"],
      "1) v = √(9,8 × 4.000) = √39.200 ≈ 198 m/s.\n2) Ubah ke km/jam: 198 × 3,6 ≈ 713 km/jam.\n3) t = jarak ÷ v = 300 ÷ 713 ≈ 0,42 jam ≈ 25 menit.\n\nPengecoh: 42 menit muncul bila 0,42 jam dibaca langsung sebagai menit. 13 menit dan 75 menit berasal dari kesalahan satuan (misalnya km dan m/s dicampur). 4 menit tidak masuk akal untuk jarak 300 km. Interpretasi: waktu 25 menit harus dikurangi waktu reaksi warga; karena itu warga pesisir perlu evakuasi mandiri begitu merasakan gempa kuat, tanpa menunggu sirene.",
      None),
    Q("Perhatikan peta Kawasan Rawan Bencana (KRB) gunung api G berikut.\n\nKRB I memanjang jauh ke arah hilir mengikuti Sungai X dan Sungai Y. Penjelasan yang paling tepat adalah …",
      ["Sungai berhulu di puncak menjadi jalur aliran lahar yang bisa mencapai jarak jauh",
       "Awan panas selalu bergerak lurus menjauhi kawah tanpa dipengaruhi bentuk lembah",
       "Lontaran batu pijar paling jauh jatuh di sepanjang aliran sungai yang lebih rendah",
       "Gas beracun lebih berat daripada udara sehingga hanya menyebar di sepanjang sungai",
       "Lava encer gunung tipe strato selalu mengalir puluhan kilometer mengikuti sungai"],
      "KRB III adalah kawasan yang sangat sering terlanda awan panas, lontaran batu, dan gas beracun (dekat kawah). KRB II berpotensi terlanda awan panas, lava, dan lontaran. KRB I adalah kawasan yang berpotensi terlanda lahar dan banjir, serta kemungkinan perluasan awan panas.\nLahar adalah aliran material vulkanik bercampur air yang bergerak mengikuti lembah sungai. Karena material dapat terbawa hujan berbulan-bulan setelah erupsi dan mengalir puluhan kilometer, kawasan di sepanjang sungai yang berhulu di puncak dimasukkan ke dalam KRB I. Contohnya Kali Gendol dan Kali Putih di Merapi.\n\nPengecoh: awan panas justru sering mengikuti lembah, bukan bergerak lurus. Lontaran batu tidak mengikuti sungai. Gas beracun bersifat lokal di sekitar kawah atau lembah tertutup. Gunung strato umumnya mengeluarkan lava kental yang tidak mengalir puluhan kilometer.",
      f_krb),
    Q("Sebuah kabupaten melakukan kegiatan berikut: (1) memasang sirene dan menggelar simulasi evakuasi tsunami; (2) membangun tanggul penahan ombak; (3) menyusun Perda tata ruang berbasis risiko; (4) menyiapkan tas siaga di setiap rumah. Pasangan kegiatan yang tergolong kesiapsiagaan adalah …",
      ["(1) dan (4)", "(2) dan (3)", "(1) dan (2)", "(3) dan (4)", "(2) dan (4)"],
      "Mitigasi adalah upaya mengurangi risiko melalui pembangunan fisik (struktural) atau penyadaran dan pengaturan (nonstruktural), misalnya tanggul (2) dan Perda tata ruang berbasis risiko (3).\nKesiapsiagaan adalah upaya mengantisipasi bencana melalui pengorganisasian dan langkah yang tepat guna agar siap merespons saat bencana terjadi, misalnya sistem peringatan dini, simulasi evakuasi (1), dan tas siaga keluarga (4).\n\nPengecoh: pasangan yang memuat (2) atau (3) mencampur kegiatan mitigasi ke dalam kesiapsiagaan. Kedua tahap ini sama-sama berada pada fase prabencana, sehingga sering tertukar dalam soal OSN.",
      None),
    Q("Perhatikan hidrograf Sungai X untuk hujan yang sama pada dua periode berikut.\n\nPerubahan yang paling tepat menggambarkan dampak alih fungsi lahan di DAS tersebut adalah …",
      ["Debit puncak naik lebih dari dua kali dan waktu menuju puncak lebih cepat",
       "Debit puncak turun karena air hujan lebih banyak terserap ke dalam tanah",
       "Waktu menuju puncak lebih lama karena permukiman menahan aliran permukaan",
       "Debit puncak hampir sama, tetapi aliran dasar meningkat menjadi dua kali lipat",
       "Hidrograf tidak berubah karena besar hujan pada kedua periode tersebut sama"],
      "Pada tahun 2000 (hutan 70%), debit puncak ±100 m³/s tercapai sekitar jam ke-10. Pada tahun 2023 (hutan 25%), debit puncak ±205 m³/s tercapai sekitar jam ke-6. Artinya debit puncak naik lebih dari dua kali dan waktu menuju puncak (time to peak) lebih pendek.\nPenyebabnya: berkurangnya hutan dan meluasnya permukaan kedap air menurunkan infiltrasi dan intersepsi, sehingga koefisien limpasan meningkat. Air hujan lebih banyak dan lebih cepat mengalir di permukaan menuju sungai. Akibatnya risiko banjir meningkat walaupun hujannya sama.\n\nPengecoh: opsi yang menyebut debit turun atau waktu puncak lebih lama membalik arah perubahan. Aliran dasar justru cenderung berkurang karena pengisian air tanah menurun. Hidrograf jelas berubah walaupun hujan sama.",
      f_hidro),
    Q("Perhatikan peta struktur tektonik utama Indonesia berikut.\n\nStruktur yang berupa sesar mendatar yang membelah Pulau Sumatra di sepanjang Bukit Barisan ditunjukkan oleh label …",
      ["R", "P", "S", "T", "P dan R"],
      "• P (garis bergerigi merah di selatan Sumatra–Jawa–Nusa Tenggara) adalah zona subduksi atau palung Sunda, tempat Lempeng Indo-Australia menunjam ke bawah Lempeng Eurasia; sumber gempa megathrust dan tsunami.\n• R (garis putus-putus di sepanjang Sumatra) adalah Sesar Besar Sumatra (Semangko), sesar mendatar menganan sepanjang ±1.900 km yang terbentuk akibat tumbukan miring (oblique) di zona subduksi.\n• S (di utara Nusa Tenggara) adalah sesar naik belakang busur Flores (back-arc thrust), sumber gempa Lombok 2018.\n• T (Papua bagian utara) adalah Sesar Sorong, juga sesar mendatar, tetapi tidak membelah Sumatra.\nPengecoh \"P dan R\" keliru karena P bukan sesar mendatar.",
      f_tektonik),
    Q("Pada gempa Palu 2018, kawasan Petobo dan Balaroa mengalami likuifaksi yang menenggelamkan ribuan rumah. Kombinasi kondisi yang paling memungkinkan likuifaksi terjadi adalah …",
      ["Pasir halus lepas, jenuh air, dan guncangan gempa kuat yang cukup lama",
       "Lempung padat, kering, dan guncangan gempa lemah dalam waktu singkat",
       "Batuan beku keras, muka air tanah dalam, dan guncangan gempa kuat",
       "Kerikil padat, kering, dan lereng curam di atas zona sesar mendatar",
       "Pasir padat, muka air tanah dalam, dan hujan deras setelah gempa"],
      "Likuifaksi terjadi ketika endapan pasir halus yang lepas dan jenuh air diguncang kuat. Guncangan membuat butir pasir ingin memadat, tetapi air di pori-pori tidak sempat keluar sehingga tekanan air pori meningkat. Tegangan efektif antarbutir turun mendekati nol dan tanah berperilaku seperti cairan; bangunan tenggelam atau terseret aliran tanah. Di Palu, kondisi ini diperparah oleh lereng landai dan saluran irigasi yang menjenuhkan tanah.\n\nPengecoh: lempung padat bersifat kohesif dan sulit mencair. Batuan beku keras dan kerikil padat tidak mengalami likuifaksi. Muka air tanah dalam berarti tanah tidak jenuh. Hujan setelah gempa tidak menjadi syarat utama likuifaksi.",
      None),
    Q("Perhatikan grafik laju dua proses di pesisir Kota J berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Laju amblesan sekitar 25 kali kenaikan muka laut sehingga menjadi penyebab utama rob",
       "Kenaikan muka laut menjadi penyebab utama rob karena terjadi di seluruh dunia",
       "Laju amblesan sekitar 2,5 kali kenaikan muka laut sehingga keduanya sama pentingnya",
       "Amblesan tanah hanya berpengaruh terhadap bangunan, bukan terhadap genangan rob",
       "Rob dapat dihentikan sepenuhnya cukup dengan memperbanyak tanggul pantai saja"],
      "Laju amblesan 75 mm/tahun, sedangkan kenaikan muka laut 3 mm/tahun. Rasionya 75 ÷ 3 = 25 kali. Artinya penurunan muka tanah jauh lebih dominan menyebabkan genangan rob dibanding kenaikan muka laut global. Amblesan di kota pesisir seperti Jakarta Utara dan Semarang terutama dipicu pengambilan air tanah berlebihan, beban bangunan, dan pemadatan endapan aluvial muda.\n\nPengecoh: 2,5 kali muncul dari kesalahan satuan (7,5 cm dibandingkan 3 mm tanpa konversi). Kenaikan muka laut memang terjadi global, tetapi dalam kasus ini kontribusinya kecil. Amblesan jelas memperluas genangan. Tanggul hanya solusi sementara; tanpa menghentikan pengambilan air tanah, amblesan berlanjut dan tanggul harus terus ditinggikan.",
      f_rob2),
]

P1 = [
    Q("Perhatikan lingkaran jarak episentrum dari tiga stasiun seismik berikut.\n\nLokasi episentrum gempa yang paling tepat adalah titik …",
      ["R", "P", "Q", "S", "T"],
      "Setiap stasiun hanya dapat mengetahui jarak episentrum, bukan arahnya. Karena itu dari setiap stasiun digambar lingkaran dengan jari-jari sama dengan jarak episentrum. Satu lingkaran memberi kemungkinan tak terhingga, dua lingkaran memberi dua titik potong, dan tiga lingkaran berpotongan pada satu titik, yaitu episentrum. Metode ini disebut triangulasi (atau trilaterasi).\nPada gambar, ketiga lingkaran putus-putus berpotongan di titik R.\n\nTitik P, Q, S, dan T hanya terletak di dekat salah satu atau dua lingkaran, tidak pada ketiganya sekaligus. Inilah alasan BMKG memerlukan minimal tiga stasiun untuk menentukan episentrum.",
      f_triang),
    Q("Gempa bermagnitudo 6,5 dirasakan dengan intensitas VIII MMI di Kota A, tetapi hanya IV MMI di Kota B. Penjelasan yang paling tepat adalah …",
      ["Intensitas bergantung pada jarak, kedalaman sumber, dan kondisi tanah di lokasi",
       "Kota A mengalami magnitudo yang lebih besar karena berada lebih dekat episentrum",
       "Magnitudo dan intensitas sama-sama tetap sehingga perbedaan itu kesalahan alat",
       "Kota B pasti berdiri di atas endapan pasir lunak yang meredam guncangan gempa",
       "Intensitas hanya ditentukan oleh jumlah penduduk dan banyaknya bangunan di kota"],
      "Magnitudo adalah ukuran energi di sumber gempa sehingga satu gempa hanya memiliki satu nilai magnitudo (6,5). Intensitas (skala MMI) adalah ukuran guncangan dan dampak yang dirasakan di suatu lokasi, sehingga nilainya berbeda-beda. Intensitas dipengaruhi jarak dari sumber, kedalaman hiposentrum, kondisi tanah setempat (tanah lunak memperkuat guncangan), dan kualitas bangunan.\n\nPengecoh: magnitudo tidak berubah menurut lokasi. Perbedaan intensitas bukan kesalahan alat. Endapan lunak justru memperbesar (amplifikasi), bukan meredam guncangan. Jumlah penduduk memengaruhi dampak, tetapi intensitas terutama ditentukan faktor fisik guncangan.",
      None),
    Q("Perhatikan sebaran hiposentrum gempa pada penampang selatan–utara Jawa berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Lempeng samudra menunjam ke utara sehingga gempa makin dalam ke arah Pulau Jawa",
       "Lempeng benua menunjam ke selatan sehingga gempa makin dangkal ke arah Pulau Jawa",
       "Kedua lempeng bergerak saling menjauh sehingga gempa dalam terjadi di tengah laut",
       "Gempa dalam di bawah Jawa disebabkan aktivitas sesar lokal yang sangat dangkal",
       "Pola kedalaman ini menunjukkan batas lempeng transform tanpa proses penunjaman"],
      "Hiposentrum dangkal terdapat di dekat palung (sebelah selatan), lalu semakin dalam ke arah utara hingga ±200–250 km di bawah Pulau Jawa. Bidang miring kumpulan hiposentrum ini disebut zona Wadati–Benioff. Pola ini menandakan Lempeng Indo-Australia (samudra) menunjam ke utara di bawah Lempeng Eurasia. Gempa terjadi di sepanjang lempeng yang menunjam karena batuan yang dingin dan rapuh mengalami tekanan.\n\nPengecoh: lempeng benua tidak menunjam ke bawah lempeng samudra. Pemisahan lempeng (divergen) menghasilkan gempa dangkal di punggungan tengah samudra. Sesar lokal dangkal tidak dapat menghasilkan gempa sedalam 200 km. Batas transform tidak membentuk pola hiposentrum yang makin dalam.",
      f_benioff),
    Q("Gempa bawah laut terjadi 180 km dari pantai dengan kedalaman laut rata-rata 2.500 m (v = √(g × d), g = 9,8 m/s²). Warga Desa W mulai mengungsi 6 menit setelah gempa dan perlu menempuh 900 m ke bukit dengan kecepatan 1 m/s. Kesimpulan yang tepat adalah …",
      ["Tidak cukup; tsunami tiba ±19 menit, warga tiba di bukit pada menit ke-21",
       "Cukup; tsunami tiba ±32 menit, warga tiba di bukit pada menit ke-21",
       "Cukup; tsunami tiba ±19 menit, warga tiba di bukit pada menit ke-15",
       "Tidak cukup; tsunami tiba ±6 menit, warga belum sempat mulai mengungsi",
       "Cukup; tsunami tiba ±25 menit, warga tiba di bukit pada menit ke-16"],
      "1) v = √(9,8 × 2.500) = √24.500 ≈ 156,5 m/s ≈ 563 km/jam.\n2) Waktu tiba = 180 ÷ 563 ≈ 0,32 jam ≈ 19,2 menit.\n3) Waktu tempuh warga = 900 m ÷ 1 m/s = 900 detik = 15 menit. Karena mulai pada menit ke-6, warga tiba pada menit ke-21.\nWarga tiba setelah tsunami (21 > 19), sehingga waktunya tidak cukup. Solusinya: evakuasi mandiri segera setelah guncangan, membangun tempat evakuasi sementara (TES) vertikal yang lebih dekat, atau memperpendek jalur.\n\nPengecoh: menit ke-15 lupa menambahkan waktu mulai 6 menit. 32 menit dan 25 menit adalah kesalahan hitung kecepatan atau satuan. 6 menit adalah waktu mulai mengungsi, bukan waktu tiba tsunami.",
      None),
    Q("Perhatikan rekaman tide gauge di sebuah pelabuhan berikut.\n\nInterpretasi dan tindakan yang paling tepat adalah …",
      ["Surutnya laut sekitar menit 22 adalah tanda awal tsunami; warga harus segera ke tempat tinggi",
       "Surutnya laut sekitar menit 22 adalah pasang surut biasa sehingga warga dapat menunggu",
       "Gelombang setinggi 3 m adalah ombak badai sehingga cukup menjauh beberapa meter",
       "Tsunami datang tepat saat gempa sehingga rekaman muka laut tidak lagi berguna",
       "Surutnya laut menandakan tsunami tidak akan datang karena energi gempa telah habis"],
      "Rekaman menunjukkan muka laut surut tajam sekitar 1,2 m pada menit ke-22, kemudian naik tajam hingga ±3 m pada menit ke-31. Surut mendadak ini adalah lembah gelombang tsunami yang tiba lebih dulu (leading depression wave). Jeda antara surut dan puncak gelombang hanya ±9 menit, sehingga orang yang turun ke pantai untuk melihat atau mengambil ikan sangat berisiko.\nTindakan yang tepat adalah segera menjauhi pantai menuju tempat tinggi atau TES tanpa menunggu.\n\nPengecoh: pasang surut berlangsung berjam-jam, bukan menit. Ombak badai tidak didahului surut tajam semacam ini. Tsunami tidak datang bersamaan dengan gempa, melainkan beberapa menit hingga jam kemudian. Surut justru tanda tsunami akan datang.",
      f_tide),
    Q("Perhatikan peta jarak rumah ke bukit aman berikut. Tsunami diperkirakan tiba 20 menit setelah gempa, warga mulai bergerak 5 menit setelah gempa, dan kecepatan berjalan 1 m/s.\n\nRumah yang penghuninya memerlukan tempat evakuasi vertikal adalah …",
      ["N dan O", "M, N, dan O", "O saja", "K dan L", "L, M, N, dan O"],
      "Waktu tersedia untuk berjalan = 20 − 5 = 15 menit = 900 detik. Dengan kecepatan 1 m/s, jarak maksimum yang dapat ditempuh = 900 m.\n• K (400 m), L (650 m), dan M (850 m) dapat mencapai bukit sebelum tsunami tiba.\n• N (1.050 m) dan O (1.300 m) melebihi 900 m sehingga tidak sempat. Penghuni kedua rumah ini memerlukan TES vertikal, misalnya gedung tinggi yang kuat.\n\nPengecoh: memasukkan M (850 m) berarti salah menghitung batas, misalnya memakai 20 menit penuh tanpa dikurangi waktu mulai. \"O saja\" mengabaikan N. Opsi K dan L membalik logika jarak. Pada praktiknya, margin keselamatan perlu ditambahkan karena lansia, anak-anak, dan penyandang disabilitas berjalan lebih lambat.",
      f_evak),
    Q("Perhatikan log bor tiga lokasi berikut.\n\nLokasi yang paling rentan mengalami likuifaksi saat gempa kuat beserta alasannya adalah …",
      ["K, karena pasir halus lepas dengan muka air tanah dangkal", "L, karena lempung padat mudah menjadi cair saat diguncang",
       "M, karena pasir padat dan kerikil menyimpan banyak air", "K dan M, karena keduanya tersusun atas material berbutir pasir",
       "L, karena muka air tanahnya paling dangkal di antara ketiganya"],
      "Syarat utama likuifaksi: endapan berbutir pasir halus, lepas (tidak padat), dan jenuh air, lalu diguncang kuat.\n• Lokasi K: pasir lepas halus dengan muka air tanah 1 m sehingga sebagian besar lapisan pasir jenuh air → paling rentan.\n• Lokasi L: lempung padat bersifat kohesif sehingga sulit mencair.\n• Lokasi M: pasir padat dan kerikil dengan muka air tanah dalam (8 m), sehingga sebagian besar lapisannya tidak jenuh dan butirannya sudah rapat.\n\nPengecoh: \"K dan M\" mengabaikan perbedaan kepadatan dan muka air tanah. Muka air tanah L (1,5 m) tidak lebih dangkal daripada K (1 m), dan lempung bukan material yang rentan likuifaksi.",
      f_bor),
    Q("Energi gempa bermagnitudo 8,0 dibandingkan gempa bermagnitudo 6,0 adalah sekitar …",
      ["1.000 kali lebih besar", "100 kali lebih besar", "2 kali lebih besar", "64 kali lebih besar", "10.000 kali lebih besar"],
      "Energi gempa sebanding dengan 10^(1,5M). Selisih magnitudo 2 → 10^(1,5 × 2) = 10³ = 1.000 kali. Cara cepatnya: setiap kenaikan 1 magnitudo ≈ 32 kali energi, sehingga 2 magnitudo ≈ 32 × 32 ≈ 1.000 kali.\n\nPengecoh: 100 kali adalah perbandingan amplitudo gelombang pada seismogram (10 kali per magnitudo). 64 kali menjumlahkan 32 + 32 atau mengalikan 32 dengan 2, padahal hubungannya eksponensial. 10.000 kali berlaku untuk selisih ±2,7 magnitudo. 2 kali menganggap skala magnitudo linear seperti skala biasa.",
      None),
    Q("Data korban gempa di Indonesia menunjukkan bahwa sebagian besar korban jiwa disebabkan oleh tertimpa bangunan, bukan oleh guncangan itu sendiri. Upaya mitigasi yang paling efektif berdasarkan fakta tersebut adalah …",
      ["Menerapkan standar bangunan tahan gempa dengan kolom, balok, dan ring balok terikat",
       "Memindahkan seluruh penduduk dari wilayah yang pernah mengalami gempa bumi",
       "Memasang sirene tsunami di semua kecamatan, termasuk yang jauh dari pantai",
       "Membangun rumah dengan dinding bata tebal tanpa tulangan agar lebih berat",
       "Menunggu teknologi prediksi waktu gempa yang akurat sebelum membangun rumah"],
      "Gempa sendiri jarang membunuh secara langsung; korban terutama jatuh karena runtuhnya bangunan yang tidak dirancang menahan beban gempa. Karena itu mitigasi struktural yang paling efektif adalah membangun rumah tahan gempa: fondasi menerus, sloof, kolom, dan ring balok yang saling terikat dengan tulangan memadai, serta atap ringan. Pengalaman gempa Yogyakarta 2006 dan Lombok 2018 menunjukkan rumah bata tanpa tulangan paling banyak runtuh.\n\nPengecoh: relokasi seluruh penduduk tidak realistis karena hampir seluruh Indonesia rawan gempa. Sirene tsunami tidak relevan bagi wilayah jauh dari pantai. Dinding bata tebal tanpa tulangan justru lebih berbahaya karena berat dan getas. Gempa belum dapat diprediksi waktunya secara akurat.",
      None),
    Q("Pada tsunami Palu 2018, gelombang tiba hanya beberapa menit setelah gempa dan banyak warga di pantai tidak menerima peringatan. Dalam kerangka empat unsur sistem peringatan dini, kelemahan yang paling menonjol adalah …",
      ["Diseminasi peringatan dan kemampuan respons masyarakat untuk evakuasi mandiri",
       "Pengetahuan risiko, karena tsunami di teluk sempit tidak pernah tercatat sebelumnya",
       "Pemantauan, karena gempa Palu tidak terekam sama sekali oleh jaringan seismograf",
       "Kemampuan respons, karena warga Palu tidak pernah mengalami gempa sebelumnya",
       "Diseminasi saja, sebab peringatan sudah tepat waktu dan warga sudah siap siaga"],
      "Empat unsur sistem peringatan dini: (1) pengetahuan risiko, (2) pemantauan dan layanan peringatan, (3) diseminasi dan komunikasi, serta (4) kemampuan respons. Pada kasus Palu, gempa terekam dan peringatan dikeluarkan, tetapi peringatan tidak sampai ke banyak warga (gangguan komunikasi, sirene tidak berfungsi). Di sisi lain, waktu tiba yang sangat singkat (tsunami lokal yang dipicu longsoran bawah laut di teluk) menuntut warga melakukan evakuasi mandiri begitu merasakan guncangan kuat. Karena itu kelemahan utamanya ada pada diseminasi dan kemampuan respons.\n\nPengecoh: gempa Palu terekam baik oleh jaringan BMKG. Sejarah tsunami di Teluk Palu sebenarnya tercatat (misalnya 1927 dan 1968). Opsi \"diseminasi saja\" keliru karena mengabaikan aspek respons warga.",
      None),
]

P2 = [
    Q("Perhatikan penampang tiga bentuk gunung api berikut.\n\nBentuk yang paling sesuai dengan gunung Merapi dan sebagian besar gunung api di Jawa, beserta alasannya, adalah …",
      ["Y; magma andesitik kental sehingga erupsinya eksplosif dan membangun kerucut berlapis",
       "X; magma basaltik encer sehingga lava mengalir jauh dan membentuk lereng landai",
       "Z; dapur magma telah runtuh sehingga terbentuk kaldera berisi danau di puncak",
       "X; magma kental tertahan lama lalu keluar perlahan membentuk perisai yang luas",
       "Y; magma basaltik encer sehingga erupsinya selalu efusif dan tidak berbahaya"],
      "X adalah gunung api perisai (shield) dengan lereng sangat landai dari lava basaltik yang encer, misalnya Mauna Loa di Hawaii. Y adalah gunung api strato (kerucut berlapis) dengan lereng curam yang tersusun atas lapisan lava dan piroklastik bergantian. Z adalah kaldera, cekungan besar akibat runtuhnya puncak setelah erupsi dahsyat, misalnya Tengger atau Toba.\nGunung api di busur Sunda, termasuk Merapi, terbentuk dari magma andesitik hasil subduksi. Magma ini kental dan kaya gas sehingga erupsinya cenderung eksplosif dan menghasilkan endapan piroklastik yang berselang-seling dengan lava, membentuk tipe Y.\n\nPengecoh: basalt encer membentuk tipe X, bukan Y, dan erupsinya efusif. Merapi bukan kaldera. Magma kental tidak membentuk gunung perisai.",
      f_volc3),
    Q("PVMBG menaikkan status gunung api G dari Waspada (Level II) menjadi Siaga (Level III). Makna status Siaga yang paling tepat adalah …",
      ["Terjadi peningkatan aktivitas yang semakin nyata dan erupsi berpeluang terjadi", "Gunung api dalam kondisi aktif normal tanpa gejala peningkatan apa pun",
       "Erupsi sudah dimulai atau akan terjadi dalam hitungan jam sehingga semua mengungsi", "Status dinaikkan hanya karena musim hujan meningkatkan ancaman lahar dingin",
       "Peningkatan aktivitas sangat kecil dan hanya perlu dipantau setiap bulan sekali"],
      "Tingkat aktivitas gunung api di Indonesia:\n• Level I (Normal): tidak ada gejala peningkatan aktivitas.\n• Level II (Waspada): ada peningkatan aktivitas di atas normal.\n• Level III (Siaga): peningkatan aktivitas semakin nyata (gempa vulkanik, deformasi, gas) dan erupsi berpeluang terjadi; radius bahaya diperluas dan masyarakat di zona tertentu mulai dievakuasi.\n• Level IV (Awas): erupsi sedang berlangsung atau akan segera terjadi; evakuasi menyeluruh di zona bahaya.\n\nPengecoh: opsi lain menggambarkan Level I, Level IV, atau Level II. Status tidak dinaikkan hanya karena musim hujan; ancaman lahar ditangani lewat peringatan tersendiri.",
      None),
    Q("Perhatikan data pemantauan gunung api G selama 30 hari berikut. EDM mengukur jarak antara pos pengamatan dan reflektor di puncak.\n\nInterpretasi yang paling tepat adalah …",
      ["Magma bergerak naik; gempa vulkanik meningkat dan tubuh gunung menggembung",
       "Aktivitas menurun; gempa vulkanik meningkat karena magma mendingin dan mengerut",
       "Tubuh gunung mengempis karena jarak EDM memendek, sehingga erupsi tidak mungkin",
       "Peningkatan gempa disebabkan gempa tektonik jauh sehingga tidak perlu ditindaklanjuti",
       "Data EDM dan gempa tidak saling berkaitan sehingga status cukup ditentukan satu data"],
      "Jumlah gempa vulkanik dalam (VA) meningkat tajam dari ±3 menjadi ±150 kejadian per hari, menandakan rekahan batuan oleh desakan magma yang bergerak naik. Bersamaan dengan itu, jarak EDM antara pos pengamatan dan puncak memendek mulai hari ke-10. Pemendekan jarak berarti tubuh gunung menggembung (inflasi) ke arah pos pengamatan akibat tekanan magma. Kombinasi kedua prekursor ini adalah dasar PVMBG untuk menaikkan status aktivitas.\n\nPengecoh: magma yang mendingin tidak menghasilkan peningkatan gempa sebesar itu. Jarak EDM yang memendek justru menunjukkan penggembungan, bukan pengempisan. Gempa tektonik jauh tidak meningkat secara konsisten selama berminggu-minggu. Status ditentukan dari gabungan berbagai data pemantauan.",
      f_prekursor),
    Q("Berikut ini yang tergolong bahaya sekunder letusan gunung api adalah …",
      ["Lahar hujan yang terjadi berbulan-bulan setelah erupsi", "Awan panas guguran yang meluncur dari kubah lava",
       "Lontaran batu pijar di sekitar kawah saat erupsi", "Aliran lava pijar yang keluar dari kawah",
       "Hujan abu tebal yang jatuh pada saat erupsi berlangsung"],
      "Bahaya primer terjadi langsung saat erupsi: aliran lava, awan panas (aliran piroklastik), lontaran material pijar, hujan abu, dan gas beracun.\nBahaya sekunder terjadi setelah erupsi, biasanya dipicu proses lain. Lahar hujan (lahar dingin) terjadi ketika material piroklastik di lereng terbawa hujan deras menjadi aliran lumpur pekat yang menerjang lembah sungai, bahkan berbulan-bulan hingga bertahun-tahun setelah erupsi, seperti setelah erupsi Merapi 2010 dan Semeru 2021.\n\nSemua opsi lain adalah bahaya primer karena terjadi saat erupsi berlangsung. Pemahaman ini penting karena ancaman lahar menuntut sistem peringatan dini tersendiri di sepanjang sungai.",
      None),
    Q("Perhatikan tabel parameter kerawanan longsor lereng S berikut. Nilai kerawanan N = Σ(bobot × skor), dengan kelas: < 2,0 rendah; 2,0–2,9 sedang; 3,0–3,9 tinggi; ≥ 4,0 sangat tinggi.\n\nNilai dan kelas kerawanan lereng S adalah …",
      ["3,85; tinggi", "3,60; tinggi", "4,15; sangat tinggi", "18,0; sangat tinggi", "2,85; sedang"],
      "N = (0,30 × 4) + (0,25 × 5) + (0,20 × 3) + (0,15 × 4) + (0,10 × 2)\n  = 1,20 + 1,25 + 0,60 + 0,60 + 0,20 = 3,85 → kelas tinggi.\n\nPengecoh: 18,0 adalah jumlah skor tanpa dikalikan bobot. 3,60 adalah rata-rata skor sederhana (18 ÷ 5) yang mengabaikan bobot. 4,15 dan 2,85 berasal dari kesalahan perkalian satu atau dua parameter. Pada metode skoring berbobot, parameter yang paling berpengaruh (kemiringan lereng dan curah hujan) diberi bobot lebih besar, sehingga hasilnya berbeda dari rata-rata biasa.",
      f_skor),
    Q("Perhatikan gambar kondisi lereng hasil pengamatan lapangan berikut.\n\nJenis gerakan massa yang paling sesuai dengan ciri-ciri tersebut adalah …",
      ["Rayapan tanah (soil creep)", "Longsoran rotasi (slump)", "Jatuhan batuan (rock fall)",
       "Aliran bahan rombakan (debris flow)", "Longsoran translasi cepat"],
      "Ciri pada gambar: tiang listrik dan batang pohon miring searah lereng, serta pagar bergeser perlahan selama beberapa tahun. Gerakan tanah yang sangat lambat (milimeter–sentimeter per tahun) dan hampir tidak terasa ini disebut rayapan tanah (soil creep). Pohon yang terus tumbuh tegak ke atas sambil pangkalnya terdorong sering membentuk batang melengkung (pistol butt).\n\nPengecoh: longsoran rotasi ditandai bidang gelincir cekung dan mahkota longsor yang jelas. Jatuhan batuan terjadi pada tebing terjal dan berlangsung cepat. Aliran bahan rombakan bergerak cepat seperti lumpur di alur lembah. Longsoran translasi cepat bergerak di bidang gelincir datar dalam waktu singkat. Rayapan tetap perlu diwaspadai karena dapat berkembang menjadi longsoran yang lebih cepat bila tanah jenuh air.",
      f_creep),
    Q("Longsor di lereng bertanah tebal paling sering terjadi saat musim hujan. Mekanisme yang paling tepat menjelaskan hal tersebut adalah …",
      ["Air meresap menambah berat tanah dan tekanan air pori sehingga kuat geser menurun",
       "Air hujan membuat tanah lebih padat sehingga kuat geser meningkat lalu tanah retak",
       "Air hujan menurunkan suhu tanah sehingga tanah mengerut dan bergerak menuruni lereng",
       "Hujan menghilangkan vegetasi secara langsung sehingga akar tidak lagi mengikat tanah",
       "Hujan menyebabkan gempa kecil yang menggetarkan lereng hingga bidang gelincir patah"],
      "Stabilitas lereng ditentukan oleh perbandingan gaya penahan (kuat geser tanah) dan gaya pendorong (komponen berat tanah searah lereng). Saat hujan, air meresap ke dalam tanah sehingga: (1) berat massa tanah bertambah, memperbesar gaya pendorong; dan (2) tekanan air pori meningkat, terutama di atas lapisan kedap air seperti lempung atau batuan, sehingga tegangan efektif dan kuat geser menurun. Bila gaya pendorong melebihi gaya penahan, tanah bergerak di sepanjang bidang gelincir.\n\nPengecoh: air tidak memadatkan tanah sehingga kuat geser naik. Penurunan suhu bukan mekanisme utama. Hujan tidak secara langsung menghilangkan vegetasi. Hujan tidak memicu gempa yang menyebabkan longsor.",
      None),
    Q("Perhatikan grafik curah hujan sebelum terjadinya longsor berikut.\n\nPada hari H hujan hanya 35 mm, lebih kecil daripada beberapa hari sebelumnya, tetapi longsor tetap terjadi. Penjelasan yang paling tepat adalah …",
      ["Hujan kumulatif beberapa hari sebelumnya telah menjenuhkan tanah sehingga hujan sedang pun memicu longsor",
       "Longsor hanya ditentukan oleh hujan harian sehingga kejadian pada hari H pasti dipicu faktor lain",
       "Hujan 35 mm termasuk hujan ekstrem yang selalu memicu longsor di semua lereng",
       "Hujan pada H-3 hingga H-1 justru mengeringkan tanah sehingga lereng retak pada hari H",
       "Grafik menunjukkan curah hujan menurun sehingga risiko longsor seharusnya ikut menurun"],
      "Hujan kumulatif sejak H-7 hingga H mencapai 248 mm, dengan hujan cukup lebat pada H-4 (48 mm) dan H-3 (55 mm). Hujan beruntun ini (hujan anteseden) membuat tanah jenuh air dan tekanan air pori tinggi. Dalam kondisi demikian, tambahan hujan sedang (35 mm) cukup untuk melampaui ambang stabilitas lereng. Karena itu sistem peringatan dini longsor tidak hanya memakai hujan harian, tetapi juga hujan kumulatif 3–7 hari.\n\nPengecoh: menganggap longsor hanya ditentukan hujan harian mengabaikan kejenuhan tanah. Hujan 35 mm/hari tergolong sedang–lebat, bukan ekstrem. Hujan tidak mengeringkan tanah. Penurunan hujan harian tidak otomatis menurunkan risiko bila tanah sudah jenuh.",
      f_rain_longsor),
    Q("Upaya mitigasi longsor berikut yang tergolong mitigasi vegetatif adalah …",
      ["Menanam vetiver dan pohon berakar dalam pada lereng", "Membangun dinding penahan tanah (retaining wall)",
       "Membuat saluran drainase untuk mengalirkan air permukaan", "Memasang ekstensometer sebagai alat peringatan dini",
       "Membuat terasering beton dengan lapisan kedap air"],
      "Mitigasi longsor dapat dikelompokkan menjadi: (1) mekanis/struktural, misalnya dinding penahan, bronjong, terasering, dan drainase; (2) vegetatif, yaitu penanaman tumbuhan yang akarnya mengikat tanah dan menyerap air, misalnya rumput vetiver yang akarnya dapat mencapai 3–4 m serta pohon berakar dalam seperti mahoni dan sonokeling; dan (3) nonstruktural, misalnya peringatan dini, penyuluhan, dan tata ruang.\nRumput vetiver banyak dipakai di lereng jalan dan tebing di Indonesia karena murah dan efektif.\n\nPengecoh: dinding penahan, drainase, dan terasering beton adalah mitigasi struktural. Ekstensometer adalah alat pemantau pergerakan tanah untuk peringatan dini (nonstruktural).",
      None),
    Q("Perhatikan peta kontur berikut.\n\nJika jenis tanah dan curah hujan di semua titik dianggap sama, titik yang paling rawan longsor berdasarkan kemiringan lerengnya adalah …",
      ["P", "Q", "R", "S", "T"],
      "Kemiringan lereng dapat dibaca dari kerapatan garis kontur: semakin rapat kontur, semakin besar beda tinggi per satuan jarak dan semakin curam lerengnya. Titik P terletak di sisi gunung utama dengan kontur paling rapat, sehingga lerengnya paling curam dan paling rawan longsor bila faktor lain sama.\nTitik Q dan T berada di kaki gunung dengan kontur renggang. Titik R berada di dekat puncak bukit kecil yang relatif datar. Titik S berada di dataran rendah dengan kontur sangat renggang.\n\nKemiringan lereng adalah parameter dengan bobot terbesar dalam banyak model kerawanan longsor, sehingga keterampilan membaca kerapatan kontur sangat penting.",
      f_kontur_lereng),
]

P3 = [
    Q("Perhatikan tabel penggunaan lahan DAS Y berikut. Dengan metode rasional Q = 0,278 × C × I × A (Q dalam m³/s, I dalam mm/jam, A dalam km²) dan intensitas hujan 60 mm/jam, debit puncak DAS Y adalah sekitar …",
      ["183 m³/s", "417 m³/s", "334 m³/s", "167 m³/s", "660 m³/s"],
      "1) Hitung koefisien limpasan gabungan (rata-rata tertimbang luas):\nC = (0,40 × 0,20) + (0,30 × 0,40) + (0,30 × 0,80) = 0,08 + 0,12 + 0,24 = 0,44.\n2) Q = 0,278 × 0,44 × 60 × 25 = 0,278 × 660 ≈ 183,5 m³/s.\n\nPengecoh: 417 m³/s muncul bila C dianggap 1 (0,278 × 60 × 25). 334 m³/s memakai C permukiman (0,8) untuk seluruh DAS. 167 m³/s memakai C = 0,40 (rata-rata sederhana tiga nilai C tanpa bobot luas, dibulatkan). 660 adalah hasil C × I × A tanpa faktor 0,278. Interpretasi: jika permukiman bertambah, C gabungan naik dan debit puncak meningkat walaupun hujannya sama.",
      f_rasional),
    Q("Banjir rob di pesisir utara Jawa semakin meluas dalam dua dekade terakhir. Faktor yang paling dominan memperparah rob di Semarang dan Jakarta Utara adalah …",
      ["Amblesan tanah akibat pengambilan air tanah berlebih dan pemadatan endapan aluvial",
       "Kenaikan muka laut global yang mencapai beberapa sentimeter setiap tahunnya",
       "Meningkatnya curah hujan di daerah hulu yang memperbesar debit sungai ke pantai",
       "Gelombang tsunami kecil yang terjadi berulang kali di sepanjang pantai utara Jawa",
       "Pasang surut yang makin kuat karena gaya gravitasi Bulan meningkat setiap tahun"],
      "Banjir rob terjadi ketika air pasang menggenangi daratan pesisir yang elevasinya lebih rendah daripada muka air pasang. Di Semarang dan Jakarta Utara, laju amblesan tanah dapat mencapai 5–15 cm per tahun, jauh lebih besar daripada kenaikan muka laut global (±3–4 mm per tahun). Amblesan dipicu oleh pengambilan air tanah berlebihan, beban bangunan, dan pemadatan alami endapan aluvial muda yang lunak.\n\nPengecoh: kenaikan muka laut global hanya beberapa milimeter, bukan sentimeter, per tahun. Hujan di hulu menyebabkan banjir kiriman, bukan rob. Tsunami tidak terjadi berulang di pantai utara Jawa. Gaya gravitasi Bulan tidak meningkat setiap tahun.",
      None),
    Q("Perhatikan data empat kawasan pesisir berikut. Kawasan dianggap mulai tergenang permanen saat pasang ketika elevasinya mencapai 0 m. Dengan asumsi laju tetap, kawasan yang paling cepat tergenang adalah …",
      ["C, sekitar 10,7 tahun", "B, sekitar 17,6 tahun", "A, sekitar 11,5 tahun", "D, sekitar 28,6 tahun", "B, sekitar 15,0 tahun"],
      "Laju penurunan relatif = laju amblesan + kenaikan muka laut (4 mm/tahun = 0,004 m/tahun).\n• A: 1,2 ÷ (0,100 + 0,004) = 1,2 ÷ 0,104 ≈ 11,5 tahun.\n• B: 0,6 ÷ (0,030 + 0,004) = 0,6 ÷ 0,034 ≈ 17,6 tahun.\n• C: 0,9 ÷ (0,080 + 0,004) = 0,9 ÷ 0,084 ≈ 10,7 tahun.\n• D: 0,4 ÷ (0,010 + 0,004) = 0,4 ÷ 0,014 ≈ 28,6 tahun.\nKawasan C paling cepat tergenang.\n\nPengecoh: B dan D memiliki elevasi terendah, tetapi laju amblesannya kecil. A memiliki laju amblesan tertinggi, tetapi elevasinya paling tinggi. Opsi \"B, 15,0 tahun\" lupa menambahkan kenaikan muka laut (0,6 ÷ 0,04). Soal seperti ini melatih kita menggabungkan dua variabel, bukan hanya melihat satu kolom.",
      f_amblesan),
    Q("Urutan jenis kekeringan yang umumnya terjadi saat kemarau panjang berlangsung adalah …",
      ["Meteorologis → pertanian → hidrologis → sosial-ekonomi", "Hidrologis → meteorologis → pertanian → sosial-ekonomi",
       "Pertanian → meteorologis → sosial-ekonomi → hidrologis", "Sosial-ekonomi → hidrologis → pertanian → meteorologis",
       "Meteorologis → hidrologis → sosial-ekonomi → pertanian"],
      "Kekeringan berkembang secara berantai:\n1) Meteorologis: curah hujan berada di bawah normal dalam periode tertentu (paling awal).\n2) Pertanian: lengas tanah tidak lagi mencukupi kebutuhan tanaman sehingga tanaman layu dan gagal panen.\n3) Hidrologis: debit sungai, muka air waduk, danau, dan air tanah turun; terjadi lebih lambat karena cadangan air tersimpan lebih lama.\n4) Sosial-ekonomi: kekurangan air dan pangan berdampak pada harga, pendapatan, dan kesehatan masyarakat.\n\nPengecoh: opsi lain menempatkan kekeringan hidrologis atau sosial-ekonomi sebagai pemicu, padahal keduanya adalah tahap lanjutan. Urutan ini penting untuk merancang peringatan dini dan respons yang bertahap.",
      None),
    Q("Perhatikan grafik jumlah titik panas bulanan di Kalimantan Tengah berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Pada tahun El Niño, titik panas melonjak dan memuncak pada September–Oktober saat kemarau paling kering",
       "Pada kedua tahun, titik panas memuncak pada Januari–Februari karena suhu udara paling tinggi",
       "Pada tahun El Niño, titik panas lebih sedikit karena hujan meningkat di Kalimantan Tengah",
       "Jumlah titik panas tidak terkait iklim sehingga perbedaan kedua tahun hanya kebetulan",
       "Pada tahun El Niño, titik panas memuncak pada Juni karena awal musim kemarau"],
      "Pada tahun normal, jumlah titik panas tertinggi hanya ±150 (September). Pada tahun El Niño, titik panas melonjak hingga ±1.250 pada September dan ±980 pada Oktober, sekitar delapan kali lipat. El Niño memperpanjang dan memperkering kemarau sehingga lahan, terutama gambut yang dikeringkan, mudah terbakar. Puncaknya terjadi pada akhir kemarau (September–Oktober) ketika muka air gambut paling rendah, sebelum hujan kembali turun pada November.\n\nPengecoh: Januari–Februari adalah musim hujan dengan titik panas sangat sedikit. El Niño mengurangi, bukan menambah, hujan. Lonjakan ini konsisten dengan kejadian karhutla 1997, 2015, 2019, dan 2023. Juni baru tahap awal peningkatan.",
      f_hotspot),
    Q("Kebakaran di lahan gambut jauh lebih sulit dipadamkan dibandingkan kebakaran hutan di tanah mineral. Penyebab utamanya adalah …",
      ["Api membara di bawah permukaan gambut kering dan dapat menjalar tanpa terlihat",
       "Gambut mengandung minyak bumi sehingga api terus menyala seperti sumur minyak",
       "Lahan gambut selalu berada di pegunungan sehingga sulit dijangkau tim pemadam",
       "Gambut tidak dapat menyerap air sehingga pemadaman dengan air tidak berguna",
       "Asap kebakaran gambut lebih tipis sehingga lokasi api sulit dideteksi satelit"],
      "Gambut adalah timbunan bahan organik yang belum terurai sempurna. Ketika dikeringkan (misalnya melalui kanal drainase), gambut menjadi bahan bakar yang sangat mudah terbakar. Api dapat membara (smoldering) di bawah permukaan hingga kedalaman beberapa meter, menjalar secara horizontal tanpa nyala yang terlihat, dan muncul kembali di tempat lain. Pemadaman memerlukan pembasahan dalam volume sangat besar, sehingga pencegahan melalui pembasahan kembali (rewetting) dengan sekat kanal jauh lebih efektif.\n\nPengecoh: gambut bukan minyak bumi. Lahan gambut di Indonesia umumnya berada di dataran rendah pesisir, bukan pegunungan. Gambut basah justru mampu menyimpan air sangat banyak. Asap kebakaran gambut sangat pekat dan menjadi sumber kabut asap lintas negara.",
      None),
    Q("Perhatikan penampang kawasan karst Gunung Sewu berikut.\n\nKawasan ini menerima curah hujan lebih dari 1.800 mm per tahun, tetapi sering mengalami kekeringan pada musim kemarau. Penyebab utamanya adalah …",
      ["Air hujan cepat meresap melalui rekahan dan doline lalu mengalir sebagai sungai bawah tanah",
       "Batu gamping kedap air sehingga air hujan seluruhnya menguap sebelum mencapai tanah",
       "Curah hujan sebesar itu terlalu kecil untuk memenuhi kebutuhan air penduduk",
       "Sungai permukaan di kawasan karst selalu mengalir sepanjang tahun ke laut",
       "Kawasan karst memiliki tanah sangat tebal sehingga air tertahan di lapisan atas"],
      "Batu gamping mudah larut oleh air hujan yang sedikit asam (pelarutan/karstifikasi), sehingga terbentuk rekahan, doline (cekungan), luweng, dan gua. Air hujan cepat meresap ke bawah melalui rongga-rongga ini dan mengalir sebagai sungai bawah tanah, misalnya Sungai Bribin di Gunungkidul. Akibatnya di permukaan hampir tidak ada sungai atau air yang tersimpan, sehingga kekeringan terjadi pada kemarau walaupun hujan tahunannya cukup tinggi. Solusinya antara lain pengangkatan air sungai bawah tanah dan pembuatan penampung air hujan (PAH).\n\nPengecoh: batu gamping justru bersifat porous karena berongga, bukan kedap air. Hujan 1.800 mm/tahun sebenarnya cukup besar. Sungai permukaan di karst umumnya kering (lembah kering). Tanah di kawasan karst justru tipis.",
      f_karst),
    Q("Perhatikan grafik Hari Tanpa Hujan (HTH) per kabupaten berikut. Kategori HTH BMKG: 1–5 sangat pendek; 6–10 pendek; 11–20 menengah; 21–30 panjang; 31–60 sangat panjang; > 60 ekstrem.\n\nPasangan kabupaten dan kategori yang tepat adalah …",
      ["Kab. D – ekstrem dan Kab. C – sangat panjang", "Kab. C – ekstrem dan Kab. D – sangat panjang",
       "Kab. B – sangat panjang dan Kab. A – panjang", "Kab. E – menengah dan Kab. A – pendek",
       "Kab. D – sangat panjang dan Kab. B – menengah"],
      "Baca nilai pada grafik lalu cocokkan dengan kategori:\n• Kab. A = 14 hari → menengah (11–20).\n• Kab. B = 27 hari → panjang (21–30).\n• Kab. C = 45 hari → sangat panjang (31–60).\n• Kab. D = 68 hari → ekstrem (> 60).\n• Kab. E = 8 hari → pendek (6–10).\nPasangan yang tepat adalah Kab. D – ekstrem dan Kab. C – sangat panjang.\n\nPengecoh: opsi lain menukar kategori C dan D, atau salah menempatkan B, A, dan E. Data HTH dipakai BMKG untuk peringatan dini kekeringan meteorologis yang menjadi dasar kesiapsiagaan air bersih dan pertanian.",
      f_hth),
    Q("Banjir bandang di Garut (2016) dan Sentani (2019) menimbulkan korban jiwa yang besar dibandingkan banjir genangan biasa. Ciri banjir bandang yang membedakannya adalah …",
      ["Datang tiba-tiba dengan arus deras membawa lumpur, batu, dan kayu dari hulu",
       "Air naik perlahan selama berhari-hari dan menggenang lama di dataran rendah",
       "Terjadi akibat air pasang laut yang menggenangi permukiman di pesisir",
       "Hanya terjadi di kota besar karena saluran drainase tidak mampu menampung air",
       "Selalu didahului peringatan beberapa hari sehingga warga sempat mengungsi"],
      "Banjir bandang (flash flood) terjadi tiba-tiba, biasanya dalam hitungan menit hingga beberapa jam setelah hujan sangat lebat di hulu yang sempit dan curam. Alirannya deras dan membawa material rombakan seperti lumpur, batu, dan batang kayu, sehingga daya rusaknya besar. Kerap dipicu pembendungan alami oleh longsoran di alur sungai yang kemudian jebol, serta kerusakan hutan di hulu, seperti pada kasus Sentani di lereng Pegunungan Cycloop.\n\nPengecoh: genangan yang naik perlahan adalah banjir genangan. Air pasang laut adalah banjir rob. Banjir akibat drainase adalah banjir perkotaan. Banjir bandang justru sulit diperingatkan karena waktu tibanya singkat.",
      None),
    Q("Perhatikan diagram penggunaan lahan hulu DAS Z pada tahun 2003 dan 2023 berikut.\n\nDampak hidrologis yang paling mungkin terjadi di DAS Z adalah …",
      ["Debit puncak banjir naik dan debit musim kemarau turun", "Debit puncak banjir turun dan debit musim kemarau naik",
       "Debit puncak dan debit kemarau sama-sama meningkat", "Tidak ada perubahan karena luas DAS tetap sama",
       "Erosi menurun karena lahan pertanian semusim lebih rapat"],
      "Dalam 20 tahun, hutan berkurang dari 62% menjadi 24%, sedangkan pertanian semusim naik dari 15% menjadi 40% dan permukiman dari 5% menjadi 22%. Berkurangnya hutan dan bertambahnya permukaan kedap air menurunkan intersepsi dan infiltrasi. Akibatnya:\n• Pada musim hujan, lebih banyak air menjadi limpasan permukaan → debit puncak banjir naik.\n• Karena pengisian air tanah berkurang, aliran dasar sungai pada musim kemarau menurun → debit kemarau turun.\nRasio debit maksimum terhadap minimum (Qmaks/Qmin) yang membesar adalah indikator DAS yang kritis.\n\nPengecoh: debit puncak tidak turun ketika hutan berkurang. Luas DAS yang sama tidak menjamin respons hidrologis tetap. Lahan pertanian semusim justru meningkatkan erosi karena tanah sering terbuka.",
      f_lahan_das),
]

P4 = [
    Q("Perhatikan diagram siklus penanggulangan bencana berikut.\n\nKegiatan membangun kembali hunian tetap, sekolah, dan jembatan dengan standar yang lebih aman (build back better) termasuk tahap …",
      ["T", "S", "R", "P", "Q"],
      "Tahap pada diagram: P = pencegahan dan mitigasi; Q = kesiapsiagaan (keduanya prabencana); R = tanggap darurat (saat bencana); S = rehabilitasi; T = rekonstruksi (keduanya pascabencana).\nRehabilitasi (S) adalah perbaikan dan pemulihan pelayanan publik sampai tingkat memadai, misalnya perbaikan prasarana dasar, pemulihan psikososial, dan pelayanan kesehatan. Rekonstruksi (T) adalah pembangunan kembali sarana dan prasarana, termasuk hunian tetap, sekolah, dan jembatan, dengan prinsip membangun kembali lebih baik dan lebih aman.\n\nPengecoh: S sering tertukar dengan T karena sama-sama pascabencana. R adalah fase penyelamatan dan pemenuhan kebutuhan dasar. P dan Q dilakukan sebelum bencana.",
      f_siklus),
    Q("Contoh mitigasi nonstruktural untuk mengurangi risiko banjir di sebuah kota adalah …",
      ["Menetapkan zonasi sempadan sungai dan larangan membangun di bantaran", "Membangun tanggul dan normalisasi alur sungai sepanjang 10 km",
       "Membuat waduk pengendali banjir di bagian hulu sungai", "Memasang pompa banjir dan pintu air di muara sungai",
       "Membangun sumur resapan dan kolam retensi di setiap kelurahan"],
      "Mitigasi struktural berupa pembangunan fisik atau rekayasa teknis, misalnya tanggul, normalisasi sungai, waduk, pompa, pintu air, sumur resapan, dan kolam retensi.\nMitigasi nonstruktural berupa kebijakan, peraturan, perencanaan, dan peningkatan pengetahuan, misalnya penetapan zonasi sempadan sungai, larangan membangun di dataran banjir, peta rawan bencana, asuransi, dan edukasi masyarakat.\n\nSemua opsi selain zonasi dan larangan membangun adalah bangunan fisik sehingga tergolong struktural. Dalam jangka panjang, mitigasi nonstruktural sering lebih murah dan berkelanjutan karena mencegah pertambahan elemen yang terpapar.",
      None),
    Q("Perhatikan rantai empat unsur sistem peringatan dini berikut.\n\nUnsur yang seharusnya mengisi tanda tanya adalah …",
      ["Diseminasi dan komunikasi peringatan", "Rehabilitasi dan rekonstruksi wilayah", "Penyusunan peta kawasan rawan bencana",
       "Pemasangan sensor dan seismograf baru", "Penggalangan dana bantuan darurat"],
      "Empat unsur sistem peringatan dini yang berpusat pada masyarakat (people-centred early warning system) menurut kerangka PBB:\n1) Pengetahuan risiko: mengetahui bahaya dan kerentanan.\n2) Pemantauan dan layanan peringatan: mengamati gejala dan mengeluarkan peringatan.\n3) Diseminasi dan komunikasi: memastikan peringatan sampai kepada semua orang yang berisiko secara cepat, jelas, dan dapat dipahami.\n4) Kemampuan respons: masyarakat tahu apa yang harus dilakukan dan mampu bertindak.\nUnsur yang hilang adalah diseminasi dan komunikasi.\n\nPengecoh: peta kawasan rawan bencana termasuk unsur 1; pemasangan sensor termasuk unsur 2; rehabilitasi-rekonstruksi dan penggalangan dana adalah kegiatan pascabencana atau tanggap darurat.",
      f_ews),
    Q("Sendai Framework for Disaster Risk Reduction 2015–2030 memiliki empat prioritas aksi. Program sekolah yang memetakan bahaya di sekitar sekolah dan mengajarkan siswa membaca peta risiko paling sesuai dengan prioritas …",
      ["Memahami risiko bencana", "Memperkuat tata kelola risiko", "Berinvestasi untuk ketangguhan",
       "Meningkatkan kesiapsiagaan respons", "Membangun kembali lebih baik"],
      "Empat prioritas Sendai Framework: (1) memahami risiko bencana; (2) memperkuat tata kelola risiko bencana; (3) berinvestasi dalam pengurangan risiko bencana untuk ketangguhan; dan (4) meningkatkan kesiapsiagaan untuk respons yang efektif serta \"membangun kembali lebih baik\" dalam pemulihan, rehabilitasi, dan rekonstruksi.\nPemetaan bahaya dan edukasi tentang peta risiko adalah upaya meningkatkan pengetahuan tentang bahaya, kerentanan, dan keterpaparan, sehingga sesuai prioritas pertama.\n\nPengecoh: tata kelola menyangkut kelembagaan dan regulasi. Investasi menyangkut pendanaan dan pembangunan fisik tangguh. Kesiapsiagaan menyangkut rencana kontinjensi dan latihan respons. Build back better berlaku pada tahap pemulihan.",
      None),
    Q("Perhatikan grafik kejadian bencana dan korban meninggal di Indonesia dalam satu tahun berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Bencana hidrometeorologi paling sering terjadi, tetapi korban jiwa terbanyak berasal dari gempa bumi",
       "Bencana geologi paling sering terjadi sekaligus menimbulkan korban paling banyak setiap tahun",
       "Jumlah korban berbanding lurus dengan jumlah kejadian pada semua jenis bencana",
       "Karhutla menimbulkan korban jiwa terbanyak karena jumlah kejadiannya lebih dari 500",
       "Banjir dan cuaca ekstrem tidak perlu diprioritaskan karena korbannya relatif sedikit"],
      "Grafik kiri menunjukkan banjir (1.250), cuaca ekstrem (1.260), longsor (590), karhutla (530), dan kekeringan (170) mendominasi jumlah kejadian. Kelimanya adalah bencana hidrometeorologi. Sebaliknya, grafik kanan menunjukkan korban meninggal terbanyak berasal dari gempa bumi (330), walaupun kejadiannya hanya 30. Artinya bencana geologi jarang terjadi tetapi berdampak sangat mematikan per kejadian (low frequency – high impact), sedangkan bencana hidrometeorologi sering terjadi dengan dampak per kejadian lebih kecil tetapi kerugian ekonominya terakumulasi besar.\n\nPengecoh: bencana geologi tidak paling sering terjadi. Korban tidak berbanding lurus dengan jumlah kejadian. Karhutla menimbulkan dampak kesehatan dan ekonomi luas, tetapi korban jiwa langsungnya kecil. Banjir tetap prioritas karena frekuensi dan kerugiannya besar.",
      f_bnpb),
    Q("Teknologi Modifikasi Cuaca (TMC) sering dilakukan untuk mengurangi kebakaran lahan atau mengisi waduk. Pernyataan yang paling tepat tentang TMC adalah …",
      ["TMC hanya dapat mempercepat hujan dari awan potensial yang sudah ada dengan menyemai bahan higroskopis",
       "TMC dapat menciptakan hujan dari langit cerah tanpa awan dengan menyemai garam dalam jumlah besar",
       "TMC bekerja dengan memanaskan awan agar uap air menguap kembali dan berpindah ke wilayah lain",
       "TMC dapat menghentikan El Niño sehingga musim kemarau panjang tidak lagi terjadi",
       "TMC tidak memerlukan informasi cuaca karena penyemaian dapat dilakukan kapan saja"],
      "TMC (sering disebut hujan buatan) bekerja dengan menyemai bahan higroskopis seperti garam (NaCl) ke dalam awan yang berpotensi hujan, terutama awan cumulus yang sedang tumbuh. Bahan ini menjadi inti kondensasi yang mempercepat penggabungan butir air sehingga hujan turun lebih cepat atau lebih banyak di lokasi sasaran. Karena itu TMC memerlukan prakiraan cuaca dan keberadaan awan potensial; TMC tidak dapat menciptakan awan dari langit cerah.\nTMC juga dapat dipakai untuk mengurangi hujan di suatu lokasi dengan menurunkannya lebih awal sebelum awan mencapai lokasi tersebut.\n\nPengecoh: menciptakan hujan dari langit cerah tidak mungkin. TMC tidak bekerja dengan memanaskan awan. TMC tidak dapat menghentikan fenomena skala samudra seperti El Niño.",
      None),
    Q("Perhatikan gambar fenomena cuaca ekstrem lokal berikut.\n\nWaktu kejadian yang paling sering untuk fenomena tersebut di Indonesia adalah …",
      ["Siang–sore hari pada masa peralihan musim saat awan konvektif tumbuh kuat", "Dini hari pada puncak musim kemarau saat udara sangat stabil",
       "Pagi hari pada puncak musim hujan saat langit tertutup awan stratus", "Malam hari saat angin darat bertiup kuat dari daratan ke laut",
       "Sepanjang hari saat siklon tropis berada tepat di atas khatulistiwa"],
      "Gambar menunjukkan puting beliung: pusaran angin kencang berdiameter puluhan hingga ratusan meter yang keluar dari dasar awan cumulonimbus dan biasanya berlangsung kurang dari 10 menit. Puting beliung terbentuk ketika udara sangat labil dan pemanasan permukaan kuat, sehingga awan cumulonimbus tumbuh menjulang. Kondisi ini paling sering terjadi pada siang–sore hari di masa peralihan musim (pancaroba), misalnya Maret–April dan Oktober–November.\n\nPengecoh: puncak kemarau dan dini hari cenderung stabil. Awan stratus tidak menghasilkan puting beliung. Angin darat terlalu lemah. Siklon tropis tidak terbentuk di khatulistiwa, dan puting beliung bukan siklon tropis.",
      f_puting),
    Q("Menurut UU No. 24 Tahun 2007, bencana dibedakan menjadi bencana alam, nonalam, dan sosial. Pasangan contoh yang tepat adalah …",
      ["Epidemi penyakit – nonalam; konflik antarkelompok – sosial", "Gagal teknologi – sosial; teror – nonalam",
       "Banjir – nonalam; wabah penyakit – alam", "Kebakaran gedung akibat korsleting – alam; tanah longsor – sosial",
       "Gempa bumi – sosial; konflik antarkelompok – nonalam"],
      "UU No. 24 Tahun 2007 membedakan:\n• Bencana alam: gempa bumi, tsunami, gunung meletus, banjir, kekeringan, angin topan, dan tanah longsor.\n• Bencana nonalam: gagal teknologi, gagal modernisasi, epidemi, dan wabah penyakit (misalnya pandemi COVID-19).\n• Bencana sosial: konflik sosial antarkelompok atau antarkomunitas dan teror.\nPasangan yang tepat adalah epidemi – nonalam dan konflik antarkelompok – sosial.\n\nPengecoh: gagal teknologi adalah bencana nonalam, sedangkan teror adalah bencana sosial. Banjir dan longsor adalah bencana alam. Kebakaran gedung akibat korsleting termasuk gagal teknologi (nonalam).",
      None),
    Q("Perhatikan peta perubahan garis pantai Desa M berikut. Pada bagian tengah, jarak mundurnya garis pantai (tanda ?) sama dengan setengah panjang batang skala.\n\nLaju abrasi rata-rata di bagian tengah dan penyebab utamanya adalah …",
      ["Sekitar 8 m/tahun; hilangnya mangrove yang meredam gelombang dan menahan sedimen",
       "Sekitar 4 m/tahun; kenaikan muka laut global yang mencapai beberapa meter per tahun",
       "Sekitar 120 m/tahun; gempa tektonik yang mengangkat dasar laut di depan pantai",
       "Sekitar 8 m/tahun; sedimentasi sungai yang menumpuk sehingga garis pantai maju",
       "Sekitar 2 m/tahun; pengaruh pasang surut harian yang selalu menggerus pantai"],
      "Panjang batang skala 240 m, sehingga setengah batang = 120 m. Pantai mundur 120 m dalam 15 tahun (2005–2020). Laju abrasi = 120 ÷ 15 = 8 m/tahun.\nPerubahan terbesar terjadi di bagian tengah, tempat mangrove ditebang untuk tambak. Mangrove meredam energi gelombang dengan akar dan batangnya, serta menangkap sedimen. Tanpa mangrove, gelombang langsung menggerus pantai lumpur sehingga abrasi meningkat tajam, seperti yang terjadi di pesisir Demak (Sayung).\n\nPengecoh: 120 m adalah jarak total, bukan laju per tahun. Kenaikan muka laut global hanya beberapa milimeter per tahun. Sedimentasi justru memajukan garis pantai. Pasang surut harian tidak menjelaskan perbedaan tajam di bagian tengah.",
      f_abrasi),
    Q("Pada 72 jam pertama setelah gempa besar yang meruntuhkan banyak bangunan, prioritas utama operasi tanggap darurat adalah …",
      ["Pencarian dan penyelamatan korban yang tertimbun reruntuhan", "Pembangunan hunian tetap bagi warga yang rumahnya rusak berat",
       "Penyusunan rencana tata ruang baru berbasis risiko bencana", "Rekonstruksi sekolah dan fasilitas umum dengan standar tahan gempa",
       "Pendataan nilai kerugian ekonomi untuk keperluan asuransi"],
      "Periode 72 jam pertama sering disebut golden time. Peluang korban tertimbun untuk bertahan hidup menurun tajam setelah periode ini karena cedera, kekurangan air, dan kondisi lingkungan. Karena itu prioritas tanggap darurat adalah pencarian dan penyelamatan (SAR), pertolongan medis, serta pemenuhan kebutuhan dasar seperti air, pangan, dan tempat berlindung sementara.\n\nPengecoh: hunian tetap dan rekonstruksi fasilitas umum termasuk tahap rekonstruksi pascabencana. Penyusunan tata ruang baru termasuk mitigasi atau pemulihan jangka panjang. Pendataan kerugian ekonomi penting, tetapi bukan prioritas penyelamatan jiwa pada 72 jam pertama.",
      None),
]

P5 = [
    Q("Perhatikan tiga lapisan raster berikut. Risiko tiap sel dihitung dengan R = (H × V) ÷ C.\n\nSel dengan nilai risiko tertinggi adalah …",
      ["a2", "b1", "a1", "b2", "c1"],
      "Hitung R = (H × V) ÷ C untuk setiap sel:\n• Baris a: a1 = (0,9 × 0,3) ÷ 0,6 = 0,45; a2 = (0,8 × 0,7) ÷ 0,4 = 1,40; a3 = (0,4 × 0,8) ÷ 0,5 = 0,64.\n• Baris b: b1 = (0,7 × 0,5) ÷ 0,3 ≈ 1,17; b2 = (0,6 × 0,9) ÷ 0,5 = 1,08; b3 = (0,3 × 0,6) ÷ 0,6 = 0,30.\n• Baris c: c1 = (0,5 × 0,8) ÷ 0,8 = 0,50; c2 = (0,4 × 0,6) ÷ 0,4 = 0,60; c3 = (0,2 × 0,4) ÷ 0,5 = 0,16.\nNilai tertinggi adalah sel a2 (1,40).\n\nPengecoh: a1 memiliki bahaya tertinggi (0,9), tetapi kerentanannya rendah sehingga risikonya kecil. b1 menempati urutan kedua karena kapasitasnya paling rendah (0,3). b2 memiliki kerentanan tertinggi (0,9). Inilah prinsip overlay dalam SIG: nilai akhir merupakan hasil operasi aritmetika antarlapisan pada sel yang sama, sehingga satu lapisan saja tidak cukup untuk menentukan wilayah prioritas.",
      f_overlay),
    Q("Perhatikan hasil analisis penyangga (buffer) 100 m di kiri-kanan sungai berikut.\n\nJumlah bangunan yang berada di dalam sempadan sungai dan perlu ditata ulang adalah …",
      ["9 bangunan", "7 bangunan", "16 bangunan", "11 bangunan", "5 bangunan"],
      "Analisis penyangga (buffer) membuat zona dengan jarak tertentu dari suatu objek, dalam hal ini 100 m di kiri dan kanan sungai (area merah muda). Hitung bangunan (■) yang berada di dalam area tersebut: terdapat 9 bangunan. Tujuh bangunan sisanya berada di luar zona penyangga.\n\nPengecoh: 16 adalah jumlah seluruh bangunan. 7 adalah jumlah bangunan di luar penyangga. 11 dan 5 berasal dari salah menghitung bangunan yang berada di dekat batas zona. Dalam SIG, operasi ini biasanya dilanjutkan dengan overlay (intersect) antara layer bangunan dan layer penyangga sehingga daftar bangunan terdampak dapat dibuat otomatis.",
      f_buffer),
    Q("Pada tsunami 26 Desember 2004, korban jiwa di Pulau Simeulue sangat sedikit walaupun pulau itu sangat dekat dengan pusat gempa. Faktor utama yang menjelaskan hal ini adalah …",
      ["Pengetahuan lokal smong yang diwariskan sehingga warga segera lari ke bukit setelah gempa",
       "Pulau Simeulue terlindung terumbu karang sehingga tsunami sama sekali tidak mencapai pantai",
       "Pemerintah sudah memasang sistem sirene tsunami modern di seluruh desa pesisir Simeulue",
       "Tsunami di Simeulue datang beberapa jam setelah gempa sehingga waktu evakuasinya panjang",
       "Seluruh penduduk Simeulue sudah dipindahkan ke daratan Sumatra sebelum tahun 2004"],
      "Masyarakat Simeulue mewarisi pengetahuan lokal smong melalui syair dan cerita (nandong) sejak tsunami 1907: jika terjadi gempa kuat dan air laut surut, segera lari ke bukit. Pada 2004, tsunami tiba di Simeulue hanya sekitar 8–10 menit setelah gempa, tetapi warga langsung mengungsi tanpa menunggu peringatan resmi, sehingga korban jiwa sangat sedikit (±7 orang) dibandingkan puluhan ribu di daratan Aceh.\n\nPengecoh: tsunami tetap melanda Simeulue. Sistem peringatan dini tsunami modern (InaTEWS) baru dibangun setelah 2004. Waktu tiba tsunami justru sangat singkat karena dekat sumber gempa. Penduduk tidak dipindahkan. Contoh ini menunjukkan kearifan lokal sebagai bentuk pengetahuan risiko dan kemampuan respons.",
      None),
    Q("Saat banjir besar melanda sebuah kabupaten, langit tertutup awan tebal selama berhari-hari. Data penginderaan jauh yang paling tepat untuk memetakan luas genangan secara cepat adalah …",
      ["Citra radar (SAR) seperti Sentinel-1 yang dapat menembus awan", "Citra optis Landsat yang memerlukan langit cerah tanpa awan",
       "Foto udara pankromatik yang direkam saat malam hari", "Data titik panas MODIS yang mendeteksi suhu permukaan",
       "Citra lampu malam hari (night light) yang mengukur cahaya kota"],
      "Citra optis (misalnya Landsat dan Sentinel-2) merekam pantulan sinar Matahari sehingga terhalang awan. Citra radar (Synthetic Aperture Radar/SAR) seperti Sentinel-1 memancarkan gelombang mikro sendiri (sensor aktif) yang dapat menembus awan dan bekerja siang maupun malam. Permukaan air yang tenang memantulkan gelombang radar menjauhi sensor sehingga tampak gelap, memudahkan pemetaan genangan.\n\nPengecoh: Landsat terhalang awan. Foto udara pankromatik malam hari tidak merekam informasi yang memadai. Titik panas MODIS dipakai untuk kebakaran. Citra lampu malam dipakai untuk analisis permukiman, aktivitas ekonomi, atau pemadaman listrik, bukan pemetaan genangan.",
      None),
    Q("Perhatikan grafik persentase penduduk yang meninggal di desa terdampak tsunami berdasarkan umur dan jenis kelamin berikut.\n\nInterpretasi yang paling tepat dari sudut pandang kerentanan sosial adalah …",
      ["Perempuan, anak-anak, dan lansia lebih rentan karena faktor fisik, peran sosial, dan keterampilan",
       "Laki-laki dewasa paling rentan karena paling banyak bekerja di laut saat tsunami terjadi",
       "Kerentanan semua kelompok sama sehingga perbedaan angka hanya disebabkan oleh kebetulan",
       "Kelompok umur 20–39 tahun paling rentan pada kedua jenis kelamin di desa tersebut",
       "Perempuan lebih rentan semata-mata karena jumlah penduduk perempuan lebih banyak"],
      "Grafik menunjukkan persentase kematian perempuan lebih tinggi daripada laki-laki pada semua kelompok umur, dan kelompok anak (0–9 tahun) serta lansia (60+) memiliki persentase tertinggi. Persentase dihitung terhadap jumlah penduduk tiap kelompok, sehingga perbedaan ini bukan karena jumlah perempuan lebih banyak. Faktor penjelasnya: kekuatan fisik untuk berlari atau berenang, kemampuan memanjat, peran pengasuhan (perempuan menyelamatkan anak dan lansia), pakaian, serta akses terhadap informasi dan pelatihan. Pola serupa tercatat pada tsunami Aceh 2004.\n\nPengecoh: laki-laki dewasa justru memiliki persentase terendah. Perbedaan yang konsisten tidak dapat dianggap kebetulan. Kelompok 20–39 tahun bukan yang paling rentan. Implikasinya, pengurangan risiko harus responsif gender dan inklusif.",
      f_gender),
    Q("Pemerintah merelokasi warga dari zona merah likuifaksi ke hunian tetap yang berjarak 15 km dari lokasi lama. Setelah dua tahun, sebagian warga kembali ke lokasi lama. Penjelasan yang paling mungkin adalah …",
      ["Lokasi baru jauh dari sumber mata pencaharian dan ikatan sosial warga", "Zona merah sudah aman karena likuifaksi tidak dapat terjadi dua kali",
       "Hunian tetap selalu lebih buruk kualitasnya daripada rumah di lokasi lama", "Warga tidak memahami bahaya karena tidak pernah mengalami bencana",
       "Relokasi otomatis berhasil jika rumah baru dibangun tahan gempa"],
      "Relokasi adalah dilema tata ruang. Secara fisik, memindahkan warga dari zona sangat berbahaya mengurangi keterpaparan. Namun relokasi sering gagal bila tidak mempertimbangkan dimensi sosial-ekonomi: jarak ke lahan pertanian, laut, pasar, atau tempat kerja; ikatan sosial dan budaya; serta hak atas tanah lama. Ketika biaya hidup dan waktu tempuh meningkat, sebagian warga memilih kembali walaupun risikonya tinggi.\n\nPengecoh: likuifaksi dapat terjadi kembali pada endapan yang sama bila kondisinya mendukung. Kualitas hunian tetap tidak selalu lebih buruk. Warga dalam kasus ini justru pernah mengalami bencana. Rumah tahan gempa tidak menjamin relokasi berhasil jika kebutuhan penghidupan tidak terpenuhi. Pelajarannya, relokasi harus partisipatif dan memulihkan mata pencaharian.",
      None),
    Q("Perhatikan matriks risiko Kabupaten Q berikut. Tingkat risiko ditentukan oleh kombinasi kemungkinan dan dampak.\n\nDua jenis bencana yang paling perlu diprioritaskan dalam rencana penanggulangan bencana adalah …",
      ["Banjir dan longsor", "Gempa dan erupsi", "Kekeringan dan erupsi", "Banjir dan kekeringan", "Gempa dan kekeringan"],
      "Pada matriks risiko, prioritas ditentukan oleh posisi pada kombinasi kemungkinan × dampak (zona merah di kanan atas).\n• Banjir: kemungkinan 5, dampak 3 → skor 15.\n• Longsor: kemungkinan 4, dampak 4 → skor 16.\n• Gempa: kemungkinan 2, dampak 5 → skor 10.\n• Kekeringan: 3 × 2 = 6.\n• Erupsi: 1 × 4 = 4.\nDua skor tertinggi adalah longsor (16) dan banjir (15).\n\nPengecoh: gempa memiliki dampak terbesar, tetapi kemungkinannya rendah sehingga skornya lebih kecil. Kekeringan dan erupsi memiliki skor terendah. Matriks ini membantu daerah dengan anggaran terbatas menentukan urutan program, tanpa mengabaikan bahaya berdampak besar seperti gempa yang tetap memerlukan rencana kontinjensi.",
      f_matrix),
    Q("Pemerintah membentuk skema dana bersama (pooling fund) bencana dan mendorong asuransi barang milik negara. Tujuan utama kebijakan pembiayaan risiko bencana ini adalah …",
      ["Menyediakan dana cepat dan pasti untuk respons dan pemulihan tanpa mengganggu anggaran rutin",
       "Menghilangkan bahaya alam sehingga bencana tidak lagi terjadi di wilayah Indonesia",
       "Mengganti seluruh program mitigasi struktural yang mahal dengan premi asuransi",
       "Memindahkan seluruh tanggung jawab penanggulangan bencana kepada perusahaan asuransi",
       "Menunda pemulihan pascabencana sampai pemerintah memperoleh pinjaman luar negeri"],
      "Kerugian bencana di Indonesia mencapai puluhan triliun rupiah per tahun, sedangkan dana cadangan bencana dalam APBN terbatas. Pembiayaan risiko bencana (disaster risk financing) seperti Pooling Fund Bencana, asuransi barang milik negara, dan asuransi pertanian bertujuan menyediakan dana yang cepat, pasti, dan memadai untuk tanggap darurat serta pemulihan, sehingga anggaran pembangunan rutin tidak terganggu dan pemulihan tidak tertunda.\n\nPengecoh: pembiayaan risiko tidak menghilangkan bahaya. Asuransi melengkapi, bukan menggantikan, mitigasi; bahkan premi dapat lebih murah bila mitigasi dilakukan. Tanggung jawab tetap ada pada pemerintah dan masyarakat. Menunda pemulihan justru memperbesar kerugian.",
      None),
    Q("Perhatikan diagram pencar indeks kapasitas daerah dan korban jiwa per 100 ribu penduduk terdampak berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Semakin tinggi kapasitas daerah, korban per penduduk terdampak cenderung semakin rendah",
       "Semakin tinggi kapasitas daerah, korban per penduduk terdampak cenderung semakin tinggi",
       "Kapasitas daerah tidak berhubungan dengan jumlah korban per penduduk terdampak",
       "Daerah A memiliki kapasitas tertinggi sehingga korbannya paling sedikit",
       "Korban jiwa hanya ditentukan oleh besar bahaya, bukan kapasitas daerah"],
      "Titik-titik membentuk pola menurun dari kiri atas ke kanan bawah: daerah A (kapasitas 0,35) mencatat ±82 korban per 100 ribu terdampak, sedangkan daerah G (kapasitas 0,85) hanya ±9. Garis tren menunjukkan hubungan negatif (berbanding terbalik). Hal ini sesuai dengan konsep risiko R = (H × V × E) ÷ C: kapasitas seperti sistem peringatan dini, layanan kesehatan, jalur evakuasi, dan kesiapsiagaan masyarakat menurunkan dampak.\n\nPengecoh: hubungan positif membalik arah grafik. Pola yang konsisten menunjukkan ada hubungan. Daerah A justru berkapasitas terendah dengan korban terbanyak. Bahaya memang berperan, tetapi grafik menunjukkan kapasitas berpengaruh besar terhadap korban. Ingat pula bahwa korelasi tidak selalu berarti sebab-akibat; faktor lain seperti kemiskinan dapat ikut berpengaruh.",
      f_capacity),
    Q("Program Desa Tangguh Bencana (Destana) dinilai berhasil meningkatkan ketangguhan masyarakat. Ciri desa yang tangguh bencana adalah …",
      ["Mampu mengantisipasi, menghadapi, dan pulih cepat dari bencana secara mandiri", "Tidak pernah lagi mengalami kejadian bahaya alam setelah program berjalan",
       "Seluruh kegiatan penanggulangan bencana bergantung pada bantuan pemerintah pusat", "Memindahkan seluruh warga ke kota besar yang memiliki fasilitas lengkap",
       "Hanya membangun infrastruktur fisik tanpa melibatkan pengetahuan lokal warga"],
      "Ketangguhan (resiliensi) adalah kemampuan sistem atau komunitas yang terpapar bahaya untuk menahan, menyerap, beradaptasi, dan pulih dari dampak bencana secara tepat waktu dan efisien. Desa Tangguh Bencana memiliki peta risiko dan rencana kontinjensi, forum PRB, relawan terlatih, sistem peringatan dini berbasis masyarakat, jalur evakuasi, serta mampu bangkit kembali dengan sumber daya sendiri.\n\nPengecoh: bahaya alam tetap dapat terjadi; yang dikurangi adalah dampaknya. Ketangguhan justru menekankan kemandirian, bukan ketergantungan. Memindahkan seluruh warga ke kota tidak realistis dan bukan tujuan. Pendekatan Destana menggabungkan infrastruktur, kelembagaan, dan pengetahuan lokal.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
