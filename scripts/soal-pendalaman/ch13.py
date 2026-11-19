from figlib import *
import heapq
from satq import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)


def P(ax, x, y, t, c="#C53030", fs=13, dx=0.02, dy=0.02):
    ax.plot(x, y, "o", ms=8, color=c, mec="white", mew=1.2, zorder=6)
    ax.text(x + dx, y + dy, t, fontsize=fs, fontweight="bold", zorder=7, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# ============================ paket 1 ============================

def f_skalabar(path):
    fig, ax = blank(9, 3.4, (0, 100), (0, 34))
    for i in range(3):
        ax.add_patch(Rectangle((15 + i * 22, 16), 22, 5, fc="black" if i % 2 == 0 else "white", ec="black", lw=1.5))
        ax.text(15 + i * 22, 24, str(i), ha="center", fontsize=13)
    ax.text(81, 24, "3 km", ha="center", fontsize=13)
    ax.annotate("", xy=(15, 11), xytext=(37, 11), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.6))
    ax.text(26, 5, "2 cm pada peta asli", ha="center", fontsize=11, color=C["red"])
    ax.set_title("Skala grafis pada sebuah peta")
    save(fig, path)


def f_interp(path):
    fig, ax = blank(7.5, 5.8, (0, 100), (0, 80))
    xs = np.linspace(2, 98, 200)
    for y0, v in [(10, 100), (35, 125), (60, 150)]:
        ys = y0 + 2.5 * np.sin(xs / 14)
        ax.plot(xs, ys, color="#8B5A2B", lw=1.6); ax.text(90, y0 + 3.5, f"{v} m", fontsize=11, color="#6B3E12", fontweight="bold")
    x0 = 45
    yb = 10 + 2.5 * np.sin(x0 / 14); yt = 35 + 2.5 * np.sin(x0 / 14)
    yp = yb + 0.4 * (yt - yb)
    ax.plot([x0, x0], [yb, yt], color=C["gray"], ls="--")
    ax.plot(x0, yp, "o", ms=9, color=C["red"]); ax.text(x0 + 2, yp, "P", fontsize=14, fontweight="bold", color=C["red"])
    ax.annotate("", xy=(x0 - 4, yb), xytext=(x0 - 4, yt), arrowprops=dict(arrowstyle="<->", color=C["blue"]))
    ax.text(x0 - 6, (yb + yt) / 2, "2,5 cm", ha="right", fontsize=11, color=C["blue"])
    ax.annotate("", xy=(x0 + 9, yb), xytext=(x0 + 9, yp), arrowprops=dict(arrowstyle="<->", color=C["green"]))
    ax.text(x0 + 11, (yb + yp) / 2, "1 cm", fontsize=11, color=C["green"])
    ax.set_title("Posisi titik P di antara garis kontur")
    save(fig, path)


def f_lereng(path):
    fig, ax = blank(8.5, 4.4, (0, 100), (0, 50))
    ax.plot(15, 30, "^", ms=14, color=C["red"]); ax.text(15, 36, "A (450 m)", ha="center", fontsize=12, fontweight="bold")
    ax.plot(85, 30, "o", ms=11, color=C["blue"]); ax.text(85, 36, "B (250 m)", ha="center", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(15, 20), xytext=(85, 20), arrowprops=dict(arrowstyle="<->", lw=1.6))
    ax.text(50, 13, "jarak di peta = 4 cm", ha="center", fontsize=12)
    ax.text(50, 4, "Skala peta 1 : 25.000", ha="center", fontsize=11, color=C["gray"])
    ax.set_title("Dua titik pada peta topografi")
    save(fig, path)


def f_proyeksi(path):
    fig, axs = plt.subplots(1, 3, figsize=(12, 4.4))
    ax = axs[0]
    for lon in np.arange(-180, 181, 30):
        ax.plot([lon, lon], [-2.0, 2.0], color="#4A5568", lw=0.8)
    for lat in [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]:
        y = np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
        ax.plot([-180, 180], [y, y], color="#4A5568", lw=0.8)
    ax.set_xlim(-185, 185); ax.set_ylim(-2.1, 2.1)
    ax = axs[1]
    th = np.radians(np.linspace(-60, 60, 100))
    for r in np.arange(3, 9, 1):
        ax.plot(r * np.sin(th), -r * np.cos(th), color="#4A5568", lw=0.8)
    for a in np.radians(np.arange(-60, 61, 15)):
        ax.plot([3 * np.sin(a), 8 * np.sin(a)], [-3 * np.cos(a), -8 * np.cos(a)], color="#4A5568", lw=0.8)
    ax.set_xlim(-7.5, 7.5); ax.set_ylim(-8.5, -1.5)
    ax = axs[2]
    t = np.linspace(0, 2 * np.pi, 200)
    for r in range(1, 6):
        ax.plot(r * np.cos(t), r * np.sin(t), color="#4A5568", lw=0.8)
    for a in np.radians(np.arange(0, 360, 30)):
        ax.plot([0, 5 * np.cos(a)], [0, 5 * np.sin(a)], color="#4A5568", lw=0.8)
    ax.set_xlim(-5.5, 5.5); ax.set_ylim(-5.5, 5.5)
    for ax, t in zip(axs, "PQR"):
        ax.set_aspect("equal" if t != "P" else "auto"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(t, fontsize=16, fontweight="bold")
    fig.suptitle("Jaring-jaring (graticule) tiga jenis proyeksi peta", fontsize=13, fontweight="bold")
    save(fig, path)


def f_azimut(path):
    fig, ax = new(7, 6)
    for e in range(499000, 505001, 1000):
        ax.axvline(e, color="#CBD5E0", lw=0.8)
    for n in range(9199000, 9205001, 1000):
        ax.axhline(n, color="#CBD5E0", lw=0.8)
    ax.plot(500000, 9200000, "o", ms=9, color=C["red"]); ax.text(500150, 9199650, "A", fontsize=14, fontweight="bold")
    ax.plot(503000, 9204000, "o", ms=9, color=C["blue"]); ax.text(503150, 9204100, "B", fontsize=14, fontweight="bold")
    ax.set_xlim(499000, 505000); ax.set_ylim(9199000, 9205000)
    ax.set_xticks(range(499000, 505001, 1000)); ax.set_yticks(range(9199000, 9205001, 1000))
    ax.ticklabel_format(useOffset=False, style="plain")
    ax.set_xticklabels([f"{v // 1000}" for v in range(499000, 505001, 1000)], fontsize=9)
    ax.set_yticklabels([f"{v // 1000}" for v in range(9199000, 9205001, 1000)], fontsize=9)
    ax.set_xlabel("Easting (km)"); ax.set_ylabel("Northing (km)")
    ax.set_title("Posisi titik A dan B pada grid UTM")
    save(fig, path)


def f_ndvi(path):
    table([["P", "0,40", "0,08"], ["Q", "0,30", "0,20"], ["R", "0,03", "0,06"], ["S", "0,25", "0,22"]], ["Piksel", "Pantulan NIR", "Pantulan merah"], path,
          title="Nilai pantulan empat piksel citra satelit", col_w=[0.26, 0.37, 0.37])


def f_tematik(path):
    fig, axs = plt.subplots(1, 4, figsize=(12.5, 3.8))
    rng = np.random.default_rng(2)
    shapes = [[(0, 0), (5, 0), (5, 4), (0, 5)], [(5, 0), (10, 0), (10, 5), (5, 4)], [(0, 5), (5, 4), (5, 10), (0, 10)], [(5, 4), (10, 5), (10, 10), (5, 10)]]
    cols = ["#FEEBC8", "#F6AD55", "#C05621", "#7B341E"]
    for i, ax in enumerate(axs):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_xticks([]); ax.set_yticks([]); ax.set_title("PQRS"[i], fontsize=16, fontweight="bold")
        for j, sh in enumerate(shapes):
            ax.add_patch(Polygon(sh, fc=cols[j] if i == 0 else "#F7FAFC", ec="#4A5568"))
    for (x, y) in rng.uniform(0.3, 9.7, (90, 2)):
        axs[1].plot(x, y, ".", color="black", ms=4)
    for (x, y, s) in [(2.5, 2.2, 400), (7.5, 2.2, 1300), (2.5, 7.5, 250), (7.5, 7.5, 800)]:
        axs[2].scatter(x, y, s=s, color=C["blue"], alpha=0.6, ec="black")
    X, Y = np.meshgrid(np.linspace(0, 10, 100), np.linspace(0, 10, 100))
    Z = np.exp(-((X - 7) ** 2 + (Y - 3) ** 2) / 12) * 30 + 20
    cs = axs[3].contour(X, Y, Z, levels=[22, 26, 30, 34, 38, 42, 46], colors=C["red"], linewidths=1)
    axs[3].clabel(cs, fmt="%d", fontsize=7)
    fig.suptitle("Empat teknik penyajian peta tematik", fontsize=13, fontweight="bold")
    save(fig, path)

# ============================ paket 2 ============================

def f_skala2(path):
    table([["Peta I", "1 : 50.000", "6 cm"], ["Peta II", "?", "15 cm"]], ["Peta", "Skala", "Jarak kota A–B di peta"], path,
          title="Jarak dua kota yang sama pada dua peta", col_w=[0.25, 0.3, 0.45])


def f_bentukkontur(path):
    fig, axs = plt.subplots(1, 5, figsize=(13, 3.8))
    t = np.linspace(0, 2 * np.pi, 200)
    for r, v in zip([4, 3, 2, 1], [100, 150, 200, 250]):
        axs[0].plot(r * np.cos(t), r * np.sin(t), color="#8B5A2B"); axs[0].text(r * 0.72, r * 0.72, str(v), fontsize=7)
    for r, v in zip([4, 3, 2, 1], [250, 200, 150, 100]):
        axs[1].plot(r * np.cos(t), r * np.sin(t), color="#8B5A2B"); axs[1].text(r * 0.72, r * 0.72, str(v), fontsize=7)
        for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
            axs[1].plot([r * np.cos(a), (r - 0.25) * np.cos(a)], [r * np.sin(a), (r - 0.25) * np.sin(a)], color="#8B5A2B", lw=0.8)
    x = np.linspace(-4.5, 4.5, 100)
    for k, v in enumerate([100, 150, 200, 250]):
        y0 = -3 + 2 * k
        axs[2].plot(x, y0 + 2.2 * np.clip(1 - np.abs(x) / 2.5, 0, 1), color="#8B5A2B"); axs[2].text(3.4, y0 + 0.2, str(v), fontsize=7)
        axs[3].plot(x, y0 - 2.2 * np.clip(1 - np.abs(x) / 2.5, 0, 1), color="#8B5A2B"); axs[3].text(3.4, y0 + 0.2, str(v), fontsize=7)
    for k, v in enumerate([100, 150, 200, 250]):
        axs[4].plot(x, -3.5 + 0.35 * k + 0.0 * x, color="#8B5A2B"); axs[4].text(3.4, -3.5 + 0.35 * k + 0.05, str(v), fontsize=6)
    for k, v in enumerate([300, 350]):
        axs[4].plot(x, 1.5 + 2.2 * k + 0.0 * x, color="#8B5A2B"); axs[4].text(3.4, 1.7 + 2.2 * k, str(v), fontsize=7)
    for ax, lab in zip(axs, "PQRST"):
        ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.6, 4.6); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(lab, fontsize=15, fontweight="bold")
    fig.suptitle("Pola garis kontur (angka = ketinggian dalam meter, utara ke atas)", fontsize=12, fontweight="bold")
    save(fig, path)


def f_foto(path):
    fig, ax = blank(8, 6, (0, 100), (0, 80))
    ax.add_patch(Rectangle((0, 0), 100, 12, fc="#C6F6D5")); ax.text(78, 4, "medan (500 m dpl)", fontsize=10)
    ax.plot([0, 100], [0, 0], color="black")
    ax.add_patch(Polygon([(42, 70), (58, 70), (54, 74), (46, 74)], fc="#4A5568"))
    ax.text(61, 71, "pesawat: 3.540 m dpl", fontsize=10)
    ax.plot([50, 22], [70, 12], color=C["gray"], ls="--"); ax.plot([50, 78], [70, 12], color=C["gray"], ls="--")
    ax.annotate("", xy=(12, 12), xytext=(12, 70), arrowprops=dict(arrowstyle="<->", color=C["red"], lw=1.6))
    ax.text(14, 42, "H = ?", fontsize=12, color=C["red"])
    ax.text(30, 58, "panjang fokus kamera\nf = 152 mm", fontsize=10, ha="center")
    ax.set_title("Pemotretan udara tegak")
    save(fig, path)


def f_spektral(path):
    wl = np.linspace(0.4, 2.5, 300)
    veg = 0.05 + 0.07 * np.exp(-((wl - 0.55) / 0.04) ** 2) + 0.45 / (1 + np.exp(-(wl - 0.72) / 0.015)) - 0.22 / (1 + np.exp(-(wl - 1.3) / 0.05))
    veg -= 0.15 * np.exp(-((wl - 1.45) / 0.05) ** 2) + 0.18 * np.exp(-((wl - 1.95) / 0.06) ** 2)
    veg = np.clip(veg, 0.02, None)
    soil = 0.08 + 0.16 * (wl - 0.4) / 2.1 + 0.1 * (1 - np.exp(-(wl - 0.4) * 3))
    water = 0.09 * np.exp(-(wl - 0.4) * 4.5)
    lines(list(wl), {"P": list(soil), "Q": list(veg), "R": list(water)}, path, title="Kurva pantulan spektral tiga objek", xlabel="Panjang gelombang (μm)",
          ylabel="Pantulan (0–1)", markers=False, ylim=(0, 0.62), w=9, legend_loc="upper right")


OV_S = ["11122", "11222", "11122", "11222", "11112"]
OV_T = ["AALLG", "AALLG", "AAALG", "LAAGG", "LLAGG"]


def f_overlay(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    cs = {"1": "#C6F6D5", "2": "#FEB2B2", "A": "#BEE3F8", "L": "#FBD38D", "G": "#E9D8FD"}
    for ax, grid, ttl in [(axs[0], OV_S, "Peta lereng\n1 = < 15%   2 = ≥ 15%"), (axs[1], OV_T, "Peta tanah\nA = aluvial  L = latosol  G = grumusol")]:
        for r, row in enumerate(grid):
            for c, v in enumerate(row):
                ax.add_patch(Rectangle((c, 4 - r), 1, 1, fc=cs[v], ec="#4A5568")); ax.text(c + 0.5, 4.5 - r, v, ha="center", va="center", fontsize=13)
        ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(ttl, fontsize=11)
    fig.suptitle("Dua lapisan data raster (1 sel = 1 ha)", fontsize=13, fontweight="bold")
    save(fig, path)


OV_N = sum(1 for r in range(5) for c in range(5) if OV_S[r][c] == "1" and OV_T[r][c] == "A")
assert OV_N == 9, OV_N

# ============================ paket 3 ============================
RIVER = [(0, 300), (250, 380), (500, 330), (750, 480), (1000, 450)]
HOUSES = [(120, 410), (200, 250), (330, 420), (400, 200), (480, 400), (560, 300), (620, 520), (700, 380), (820, 600), (880, 470), (950, 330), (300, 600)]


def _dseg(p, a, b):
    p, a, b = map(np.array, (p, a, b))
    t = np.clip(np.dot(p - a, b - a) / np.dot(b - a, b - a), 0, 1)
    return np.linalg.norm(p - (a + t * (b - a)))


def _dline(p):
    return min(_dseg(p, RIVER[i], RIVER[i + 1]) for i in range(len(RIVER) - 1))


BUF_N = sum(1 for h in HOUSES if _dline(h) <= 100)


def f_buffer(path):
    from matplotlib.path import Path as MPath
    fig, ax = new(8.5, 6)
    X, Y = np.meshgrid(np.linspace(0, 1000, 400), np.linspace(0, 800, 320))
    D = np.vectorize(lambda x, y: _dline((x, y)))(X, Y)
    ax.contourf(X, Y, D, levels=[0, 100], colors=["#BEE3F8"], alpha=0.8)
    ax.contour(X, Y, D, levels=[100], colors=[C["blue"]], linestyles="--", linewidths=1)
    rx, ry = zip(*RIVER); ax.plot(rx, ry, color=C["blue"], lw=3)
    for h in HOUSES:
        ax.add_patch(Rectangle((h[0] - 12, h[1] - 12), 24, 24, fc=C["red"], ec="black"))
    ax.set_xlim(0, 1000); ax.set_ylim(0, 800); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.plot([700, 900], [60, 60], color="black", lw=3); ax.text(800, 80, "200 m", ha="center", fontsize=10)
    legend_patches(ax, [("sungai", C["blue"]), ("zona penyangga 100 m", "#BEE3F8"), ("rumah", C["red"])], loc="upper left")
    ax.set_title("Analisis buffer sempadan sungai")
    save(fig, path)


assert BUF_N == 6, BUF_N


def f_thiessen(path):
    table([["A", "1.800", "40"], ["B", "2.400", "35"], ["C", "3.000", "25"], ["Jumlah", "", "100"]], ["Stasiun", "Curah hujan (mm/tahun)", "Luas poligon (km²)"],
          path, title="Data stasiun hujan dan poligon Thiessen DAS W", col_w=[0.24, 0.4, 0.36])


def f_das(path):
    table([["DAS P", "400", "40"], ["DAS Q", "400", "20"]], ["DAS", "Luas A (km²)", "Panjang DAS Lb (km)"], path, title="Data morfometri dua DAS", col_w=[0.3, 0.33, 0.37])


def _zl(X, Y):
    return 100 + 800 * np.exp(-((X - 0.55) ** 2 / (2 * 0.12 ** 2) + (Y - 0.5) ** 2 / (2 * 0.28 ** 2)))


LPTS = {"P": (0.43, 0.5), "Q": (0.55, 0.52), "R": (0.92, 0.5), "S": (0.55, 0.12)}


def _grad(x, y, h=1e-4):
    gx = (_zl(x + h, y) - _zl(x - h, y)) / (2 * h); gy = (_zl(x, y + h) - _zl(x, y - h)) / (2 * h)
    return math.hypot(gx, gy)


assert max(LPTS, key=lambda k: _grad(*LPTS[k])) == "P", {k: _grad(*v) for k, v in LPTS.items()}


def f_curam(path):
    X, Y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    contour_map(X, Y, _zl(X, Y), path, 50, index_every=5, points=LPTS, title="Peta kontur sebuah bukit (CI = 50 m)")


def f_skor(path):
    table([["X", "4", "3", "3"], ["Y", "3", "4", "4"], ["Z", "5", "4", "1"], ["Bobot", "3", "2", "1"]], ["Unit lahan", "Kemiringan", "Jenis tanah", "Curah hujan"],
          path, title="Skor kesesuaian tiga unit lahan (skor tinggi = sesuai)", col_w=[0.25, 0.25, 0.25, 0.25])


def f_koord(path):
    fig, ax = new(7, 6)
    ax.set_xlim(110, 111); ax.set_ylim(-8, -7)
    ticks_x = [110 + i / 4 for i in range(5)]; ticks_y = [-8 + i / 4 for i in range(5)]
    ax.set_xticks(ticks_x); ax.set_yticks(ticks_y)
    ax.set_xticklabels(["110°00′", "110°15′", "110°30′", "110°45′", "111°00′"], fontsize=9)
    ax.set_yticklabels(["8°00′ LS", "7°45′ LS", "7°30′ LS", "7°15′ LS", "7°00′ LS"], fontsize=9)
    ax.grid(color="#CBD5E0")
    ax.plot(110.75, -7.5, "*", ms=18, color=C["red"], mec="black"); ax.text(110.77, -7.47, "K", fontsize=14, fontweight="bold")
    ax.plot(110.25, -7.75, "o", ms=9, color=C["blue"]); ax.text(110.27, -7.72, "M", fontsize=12, fontweight="bold")
    ax.set_xlabel("Bujur Timur"); ax.set_title("Lembar peta dengan grid geografis")
    save(fig, path)

# ============================ paket 4 ============================

def f_dekl(path):
    fig, ax = blank(6.5, 6.2, (-40, 40), (0, 80))
    arrow(ax, 0, 5, 0, 70, lw=2.4); ax.text(0, 73, "UG", ha="center", fontsize=12, fontweight="bold")
    a = math.radians(14)
    arrow(ax, 0, 5, 65 * math.sin(a), 5 + 65 * math.cos(a), color=C["red"], lw=2.4); ax.text(65 * math.sin(a) + 2, 72, "UM", fontsize=12, fontweight="bold", color=C["red"])
    ax.text(-38, 40, "Keterangan pada peta:\n• Deklinasi magnetis tahun 2015\n  = 2°30′ timur\n• Perubahan tahunan 6′\n  ke arah barat", fontsize=10, va="center")
    ax.text(6, 30, "δ", fontsize=14, color=C["red"])
    ax.set_title("Diagram deklinasi pada peta topografi")
    save(fig, path)


def _zp(X, Y):
    return 150 + 600 * np.exp(-((X - 0.3) ** 2 + (Y - 0.5) ** 2) / (2 * 0.09 ** 2)) + 350 * np.exp(-((X - 0.72) ** 2 + (Y - 0.5) ** 2) / (2 * 0.08 ** 2))


def f_profil(path):
    fig = plt.figure(figsize=(12, 5.2))
    ax = fig.add_axes([0.02, 0.08, 0.42, 0.82])
    X, Y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    Z = _zp(X, Y)
    ax.contourf(X, Y, Z, levels=np.arange(150, 801, 50), cmap="YlGn_r", alpha=0.35)
    cs = ax.contour(X, Y, Z, levels=np.arange(150, 801, 50), colors="#8B5A2B", linewidths=0.7)
    ax.clabel(cs, levels=[200, 400, 600], fmt="%d", fontsize=8)
    ax.plot([0.08, 0.92], [0.5, 0.5], color=C["red"], lw=2); ax.text(0.04, 0.5, "A", fontsize=13, fontweight="bold", va="center"); ax.text(0.94, 0.5, "B", fontsize=13, fontweight="bold", va="center")
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title("Peta kontur (CI = 50 m)")
    xs = np.linspace(0.08, 0.92, 200); zt = _zp(xs, 0.5)
    prof = {"P": zt[::-1], "Q": 150 + 600 * np.exp(-(xs - 0.5) ** 2 / (2 * 0.12 ** 2)), "R": zt, "S": 900 - zt, "T": 150 + (zt - 150) * np.where(xs < 0.5, 0.58, 1.7)}
    for i, (k, z) in enumerate(prof.items()):
        a = fig.add_axes([0.5 + (i % 3) * 0.17, 0.55 - (i // 3) * 0.45, 0.14, 0.33])
        a.fill_between(xs, 0, z, color="#E2E8F0"); a.plot(xs, z, color="#2D3748")
        a.set_ylim(0, 950); a.set_xticks([]); a.set_yticks([0, 400, 800]); a.tick_params(labelsize=7); a.set_title(k, fontsize=13, fontweight="bold")
    fig.suptitle("Penampang (profil) A–B yang mungkin", x=0.75, fontsize=12, fontweight="bold")
    save(fig, path)


def f_sawah(path):
    lines(BULAN3, {"NDVI": [0.2, 0.45, 0.75, 0.5, 0.2, 0.42, 0.72, 0.45, 0.15, 0.15, 0.18, 0.25]}, path, title="Rata-rata NDVI bulanan sebuah hamparan lahan", ylabel="NDVI",
          ylim=(0, 0.9), w=8.5)


def f_komposit(path):
    table([["Saluran 3 (hijau)", "0,53–0,59 μm", "biru"], ["Saluran 4 (merah)", "0,64–0,67 μm", "hijau"], ["Saluran 5 (inframerah dekat)", "0,85–0,88 μm", "merah"]],
          ["Saluran Landsat 8", "Panjang gelombang", "Ditampilkan sebagai"], path, title="Susunan citra komposit 543", col_w=[0.42, 0.3, 0.28])


KELAS = [("A", 150), ("B", 320), ("C", 410), ("D", 560), ("E", 690), ("F", 760), ("G", 880), ("H", 950)]


def f_kelas(path):
    table([[k, f"{v}"] for k, v in KELAS], ["Kabupaten", "Kepadatan (jiwa/km²)"], path, title="Kepadatan penduduk delapan kabupaten", col_w=[0.4, 0.6])


def f_waktu(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    for n, x, y in [("Medan (98,7° BT)", 98.7, 3.6), ("Makassar (119,4° BT)", 119.4, -5.1), ("Jayapura (140,7° BT)", 140.7, -2.5)]:
        ax.plot(x, y, "o", ms=9, color=C["red"], mec="black")
        ax.text(x, y + 0.9, n, fontsize=9, fontweight="bold", ha="center" if x < 135 else "right", bbox=dict(fc="white", ec="none", pad=1))
    for x in (112.5, 127.5):
        ax.axvline(x, color=C["purple"], ls="--", lw=1)
    ax.text(103, -10.6, "WIB (UTC+7)", fontsize=9, color=C["purple"], fontweight="bold"); ax.text(117, -10.6, "WITA (UTC+8)", fontsize=9, color=C["purple"], fontweight="bold")
    ax.text(133, -10.6, "WIT (UTC+9)", fontsize=9, color=C["purple"], fontweight="bold")
    ax.set_title("Tiga kota dan pembagian zona waktu Indonesia (batas disederhanakan)")
    save(fig, path)

# ============================ paket 5 ============================

def f_utm2(path):
    fig, ax = new(7, 6.4)
    ax.set_xlim(410000, 420000); ax.set_ylim(9170000, 9182000)
    ax.set_xticks(range(410000, 420001, 2000)); ax.set_yticks(range(9170000, 9182001, 2000))
    ax.set_xticklabels([f"{v // 1000}" for v in range(410000, 420001, 2000)], fontsize=9)
    ax.set_yticklabels([f"{v // 1000}" for v in range(9170000, 9182001, 2000)], fontsize=9)
    ax.grid(color="#CBD5E0")
    ax.plot(412000, 9180000, "o", ms=10, color=C["red"]); ax.text(412250, 9180300, "A", fontsize=14, fontweight="bold")
    ax.plot(418000, 9172000, "o", ms=10, color=C["blue"]); ax.text(418250, 9172300, "B", fontsize=14, fontweight="bold")
    ax.set_xlabel("Easting (km)"); ax.set_ylabel("Northing (km)"); ax.set_title("Titik A dan B pada grid UTM")
    save(fig, path)


def _zs(X, Y):
    return 200 + 400 * Y - 70 * np.exp(-(X - 0.5) ** 2 / (2 * 0.07 ** 2))


def f_sungai(path):
    X, Y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    contour_map(X, Y, _zs(X, Y), path, 25, index_every=4, river=([0.5, 0.5], [0.0, 1.0]), title="Peta kontur dengan sebuah sungai",
                extra=lambda ax: north_arrow(ax, 0.92, 0.82))


def f_uhi(path):
    fig, ax = new(7.5, 6)
    X, Y = np.meshgrid(np.linspace(0, 10, 200), np.linspace(0, 10, 200))
    Z = 26 + 9 * np.exp(-((X - 4.5) ** 2 + (Y - 5.5) ** 2) / 6) + 2 * np.exp(-((X - 8) ** 2 + (Y - 2) ** 2) / 1.5)
    cf = ax.contourf(X, Y, Z, levels=np.arange(26, 36, 1), cmap="YlOrRd"); fig.colorbar(cf, ax=ax, label="Suhu permukaan (°C)")
    for n, (x, y) in {"P": (4.5, 5.5), "Q": (8, 2), "R": (1, 9)}.items():
        ax.plot(x, y, "o", ms=8, color="black"); ax.text(x + 0.2, y + 0.2, n, fontsize=13, fontweight="bold")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal"); ax.set_title("Suhu permukaan hasil citra satelit siang hari")
    save(fig, path)


LAKE = [(2.2, 1.5), (5.3, 1.2), (7.6, 2.4), (7.8, 4.6), (6.3, 6.6), (3.6, 6.8), (1.6, 5.1), (1.4, 3.0)]


def _lake_counts():
    from matplotlib.path import Path as MPath
    pth = MPath(LAKE)
    full = part = 0
    for i in range(9):
        for j in range(8):
            pts = [(i + a / 10, j + b / 10) for a in range(11) for b in range(11)]
            ins = pth.contains_points(pts)
            if ins.all(): full += 1
            elif ins.any(): part += 1
    return full, part


LF, LP = _lake_counts()


def f_danau(path):
    fig, ax = new(7, 6.2)
    for v in range(10):
        ax.axvline(v, color="#A0AEC0", lw=0.8)
    for v in range(9):
        ax.axhline(v, color="#A0AEC0", lw=0.8)
    ax.add_patch(Polygon(LAKE, fc=C["lblue"], ec=C["blue"], lw=2, alpha=0.8))
    ax.set_xlim(0, 9); ax.set_ylim(0, 8); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Danau pada peta 1 : 25.000 (1 kotak = 1 cm × 1 cm)")
    save(fig, path)


def _zh(X, Y):
    return 300 + 530 * np.exp(-((X - 0.5) ** 2 + (Y - 0.5) ** 2) / (2 * 0.2 ** 2))


def f_puncak(path):
    X, Y = np.meshgrid(np.linspace(0, 1, 200), np.linspace(0, 1, 200))
    Z = _zh(X, Y)
    assert 800 < Z.max() < 850
    contour_map(X, Y, Z, path, 50, index_every=5, points={"T": (0.5, 0.5)}, title="Peta kontur sebuah bukit (CI = 50 m)")


GRAPH = {("A", "B"): 4, ("A", "C"): 2, ("B", "C"): 1, ("B", "D"): 5, ("C", "D"): 8, ("C", "E"): 10, ("D", "E"): 2, ("D", "F"): 6, ("E", "F"): 3}
NODES = {"A": (0.5, 3), "B": (3, 5), "C": (3, 1), "D": (6, 5), "E": (6, 1), "F": (8.5, 3)}


def _dijk(s, t):
    adj = {}
    for (a, b), w in GRAPH.items():
        adj.setdefault(a, []).append((b, w)); adj.setdefault(b, []).append((a, w))
    pq = [(0, s, [s])]; seen = set()
    while pq:
        d, u, p = heapq.heappop(pq)
        if u == t: return d, p
        if u in seen: continue
        seen.add(u)
        for v, w in adj[u]:
            heapq.heappush(pq, (d + w, v, p + [v]))


SP = _dijk("A", "F")
assert SP == (13, ["A", "C", "B", "D", "E", "F"]), SP


def f_jaringan(path):
    fig, ax = blank(9, 5, (0, 9), (0, 6))
    for (a, b), w in GRAPH.items():
        (x1, y1), (x2, y2) = NODES[a], NODES[b]
        ax.plot([x1, x2], [y1, y2], color="#718096", lw=2.4)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.15, str(w), fontsize=11, fontweight="bold", color=C["red"], bbox=dict(fc="white", ec="none", pad=0.5))
    for n, (x, y) in NODES.items():
        ax.add_patch(Circle((x, y), 0.32, fc=C["blue"], ec="black", zorder=5)); ax.text(x, y, n, ha="center", va="center", color="white", fontsize=12, fontweight="bold", zorder=6)
    ax.set_title("Jaringan jalan dengan waktu tempuh tiap ruas (menit)")
    save(fig, path)


def f_lokasi(path):
    table([["P", "300", "5", "tidak", "kebun campuran"], ["Q", "800", "4", "tidak", "semak"], ["R", "200", "12", "tidak", "tegalan"], ["S", "400", "6", "ya", "sawah"],
           ["T", "450", "7", "tidak", "hutan lindung"]], ["Lokasi", "Jarak ke jalan (m)", "Lereng (%)", "Rawan banjir", "Penggunaan lahan"], path,
          title="Data calon lokasi tempat pengolahan sampah terpadu", col_w=[0.14, 0.23, 0.17, 0.19, 0.27], fs=11)


def f_hutan(path):
    bars(["2015", "2023"], {"Hutan": [12000, 9600], "Perkebunan": [5000, 7000], "Permukiman": [1000, 1400]}, path, title="Luas tutupan lahan Kabupaten H hasil klasifikasi citra (ha)",
         ylabel="ha", values=True, ylim=(0, 14500), colors=[C["green"], C["orange"], C["gray"]], w=8)


def f_reseksi(path):
    fig, ax = blank(7.5, 6.2, (0, 100), (0, 84))
    ax.plot(20, 70, "^", ms=18, color="#744210"); ax.text(24, 70, "Puncak G", fontsize=11, fontweight="bold")
    ax.plot(80, 70, "s", ms=12, color=C["purple"]); ax.text(66, 75, "Menara M", fontsize=11, fontweight="bold")
    ax.plot(50, 40, "*", ms=16, color=C["red"]); ax.text(53, 36, "posisi pendaki (?)", fontsize=10, color=C["red"])
    ax.plot([50, 20], [40, 70], color=C["gray"], ls="--"); ax.plot([50, 80], [40, 70], color=C["gray"], ls="--")
    ax.text(24, 50, "azimut 315°", fontsize=10, color=C["gray"]); ax.text(66, 50, "azimut 45°", fontsize=10, color=C["gray"])
    north_arrow(ax, 0.92, 0.72)
    ax.set_title("Pendaki membidik dua objek dengan kompas")
    save(fig, path)


def f_los(path):
    fig, ax = new(9, 4.4)
    x = np.linspace(0, 4, 200)
    z = 300 + 50 * x + 150 * np.exp(-((x - 2) / 0.45) ** 2)
    ax.fill_between(x, 0, z, color="#E6D3A3"); ax.plot(x, z, color="#744210", lw=2)
    ax.plot(0, 302, "o", ms=9, color=C["red"]); ax.text(0.05, 320, "A (300 m)", fontsize=11, fontweight="bold")
    ax.plot(4, 500, "o", ms=9, color=C["blue"]); ax.text(3.3, 520, "B (500 m)", fontsize=11, fontweight="bold")
    ax.text(2, z.max() + 15, f"bukit {z.max():.0f} m", ha="center", fontsize=10)
    ax.set_ylim(200, 620); ax.set_xlim(-0.1, 4.1); ax.set_xlabel("Jarak (km)"); ax.set_ylabel("Ketinggian (m)")
    ax.set_title("Penampang medan antara titik A dan B")
    save(fig, path)


def f_layout(path):
    fig, ax = blank(9, 6.2, (0, 100), (0, 70))
    ax.add_patch(Rectangle((2, 2), 96, 66, fc="white", ec="black", lw=2))
    ax.add_patch(Rectangle((25, 60), 50, 6, fc="#EDF2F7", ec="#4A5568")); ax.text(50, 63, "PETA PENGGUNAAN LAHAN KABUPATEN X", ha="center", va="center", fontsize=9, fontweight="bold")
    ax.add_patch(Rectangle((5, 10), 62, 48, fc="#E6FFFA", ec="#4A5568"))
    ax.add_patch(Polygon([(12, 15), (40, 14), (60, 25), (55, 50), (25, 53), (10, 38)], fc="#FBD38D", ec="#744210"))
    ax.add_patch(Rectangle((71, 44), 24, 14, fc="#F7FAFC", ec="#4A5568"))
    for i, (c, t) in enumerate([("#FBD38D", "sawah"), ("#68D391", "hutan"), ("#A0AEC0", "permukiman")]):
        ax.add_patch(Rectangle((73, 53 - i * 4), 3, 2.5, fc=c, ec="black")); ax.text(77.5, 54.2 - i * 4, t, fontsize=8, va="center")
    ax.add_patch(Rectangle((71, 28), 24, 13, fc="#E2E8F0", ec="#4A5568"))
    ax.add_patch(Polygon([(73, 30), (90, 31), (92, 38), (76, 39)], fc="white", ec="#4A5568")); ax.add_patch(Rectangle((83, 33), 3, 2.5, fc=C["red"]))
    ax.add_patch(Rectangle((71, 18), 24, 7, fc="#F7FAFC", ec="#4A5568"))
    ax.plot([74, 92], [21, 21], color="black", lw=3); ax.text(74, 22.5, "0", fontsize=7); ax.text(90, 22.5, "2 km", fontsize=7)
    ax.add_patch(Rectangle((71, 5), 24, 10, fc="#F7FAFC", ec="#4A5568"))
    arrow(ax, 83, 6.5, 83, 13.5, lw=2, ms=12); ax.text(85, 12, "U", fontsize=9, fontweight="bold")
    for n, (x, y) in {"1": (21, 63), "2": (97, 55), "3": (97, 38), "4": (97, 23), "5": (97, 13)}.items():
        ax.add_patch(Circle((x, y), 1.9, fc=C["red"], ec="none", zorder=6)); ax.text(x, y, n, ha="center", va="center", color="white", fontsize=10, fontweight="bold", zorder=7)
    ax.set_title("Tata letak komponen sebuah peta")
    save(fig, path)

# ============================ questions ============================
P0 = [
    Q("Perhatikan skala grafis pada sebuah peta berikut. Pada peta asli, jarak dua kota terukur 7,5 cm.\n\nSkala numerik peta dan jarak sebenarnya kedua kota adalah …",
      ["1 : 50.000; 3,75 km", "1 : 5.000; 0,375 km", "1 : 500.000; 37,5 km", "1 : 50.000; 37,5 km", "1 : 20.000; 1,5 km"],
      "1) Satu segmen skala grafis panjangnya 2 cm dan mewakili 1 km = 100.000 cm.\n2) Skala numerik = 2 : 100.000 = 1 : 50.000.\n3) Jarak sebenarnya = 7,5 cm × 50.000 = 375.000 cm = 3,75 km.\nKelebihan skala grafis adalah tetap benar walaupun peta diperbesar atau diperkecil, karena panjang batang skala ikut berubah bersama peta. Sebaliknya, skala numerik menjadi salah bila peta difotokopi dengan ukuran berbeda.\n\nPengecoh: 1 : 5.000 dan 1 : 500.000 salah konversi satuan. 37,5 km salah memindahkan koma. 1 : 20.000 tidak sesuai skala grafis.",
      f_skalabar),
    Q("Perhatikan citra Sentinel-2 warna asli kawasan Kintamani, Bali berikut. Objek Q berona cokelat gelap, bertekstur kasar, hampir tanpa vegetasi, dan berada di dalam cekungan besar.\n\nObjek Q paling mungkin merupakan …",
      ["Aliran lava muda di dalam kaldera", "Danau kawah berair dalam", "Permukiman padat di bibir kaldera", "Hutan hujan tropis yang rapat", "Lahan sawah bertingkat (subak)"],
      "Citra menunjukkan Kaldera Batur, cekungan raksasa berdiameter lebih dari 10 km hasil letusan besar puluhan ribu tahun lalu. Unsur interpretasinya:\n• P: rona gelap, tekstur halus, bentuk memanjang mengikuti dinding kaldera → Danau Batur.\n• Q: rona cokelat gelap, tekstur kasar, tanpa vegetasi, menyebar dari kerucut Gunung Batur → aliran lava muda hasil letusan abad ke-20 (misalnya 1963–1974). Lava basaltik yang baru membeku belum melapuk menjadi tanah, sehingga tanaman belum dapat tumbuh.\n• R: rona cerah berbintik di bibir kaldera → permukiman Kintamani–Penelokan.\n• S: rona hijau tua di lereng luar → hutan dan kebun.\nAliran lava ini menjadi daya tarik Geopark Batur.\n\nPengecoh: danau ditunjukkan P, permukiman R, dan hutan S. Sawah berteras tidak tumbuh di atas lava muda.",
      s_batur),
    Q("Perhatikan posisi titik P di antara garis kontur berikut.\n\nKetinggian titik P berdasarkan interpolasi adalah …",
      ["110 m", "105 m", "115 m", "120 m", "135 m"],
      "Interpolasi linear: h = h₁ + (d₁ ÷ D) × CI.\n• h₁ = 100 m (kontur di bawah P).\n• CI = 125 − 100 = 25 m.\n• d₁ = jarak P ke kontur 100 m = 1 cm; D = jarak antarkontur = 2,5 cm.\nh = 100 + (1 ÷ 2,5) × 25 = 100 + 0,4 × 25 = 100 + 10 = 110 m.\nJarak diukur tegak lurus terhadap garis kontur. Interpolasi linear mengasumsikan lereng di antara dua kontur seragam.\n\nPengecoh: 105 m dan 115 m salah menghitung perbandingan jarak. 120 m membalik perbandingan (1,5 ÷ 2,5). 135 m melampaui kontur 125 m.",
      f_interp),
    Q("Perhatikan dua titik pada peta topografi berikut.\n\nKemiringan lereng rata-rata dari A ke B adalah …",
      ["20%", "2%", "50%", "8%", "40%"],
      "1) Beda tinggi Δh = 450 − 250 = 200 m.\n2) Jarak mendatar d = 4 cm × 25.000 = 100.000 cm = 1.000 m.\n3) Kemiringan = Δh ÷ d × 100% = 200 ÷ 1.000 × 100% = 20%.\nDalam derajat, α = arctan 0,2 ≈ 11,3°. Ingat bahwa kemiringan 100% sama dengan 45°, bukan 90°. Klasifikasi lereng sering dipakai untuk menentukan kesesuaian lahan, misalnya lereng di atas 40% umumnya diarahkan untuk kawasan lindung.\n\nPengecoh: 2% salah konversi jarak (10 km). 50% membagi Δh dengan 400 m. 8% dan 40% salah perhitungan.",
      f_lereng),
    Q("Perhatikan jaring-jaring tiga jenis proyeksi peta berikut.\n\nProyeksi yang paling sesuai untuk memetakan daerah kutub dan untuk daerah lintang tengah berturut-turut adalah …",
      ["R dan Q", "P dan Q", "Q dan R", "R dan P", "P dan R"],
      "Identifikasi proyeksi:\n• P – silinder (Mercator): meridian sejajar tegak dan jarak antarparalel makin lebar ke arah kutub. Distorsi luas besar di lintang tinggi, sehingga cocok untuk daerah ekuator dan navigasi karena garis arah tetap lurus (konform).\n• Q – kerucut: meridian memancar dari satu titik dan paralel berupa busur. Cocok untuk daerah lintang tengah yang membentang barat–timur, misalnya Amerika Serikat atau Eropa.\n• R – azimutal (bidang datar) normal: paralel berupa lingkaran konsentris dan meridian berupa garis radial dari kutub. Cocok untuk daerah kutub.\nJadi untuk kutub dipakai R dan untuk lintang tengah dipakai Q.\n\nPengecoh: P (silinder) paling sesuai untuk daerah ekuator.",
      f_proyeksi),
    Q("Kota Jakarta terletak pada bujur 106°49′ BT. Zona UTM dan meridian tengah zona tersebut adalah …",
      ["Zona 48, meridian tengah 105° BT", "Zona 47, meridian tengah 99° BT", "Zona 49, meridian tengah 111° BT", "Zona 48, meridian tengah 108° BT",
       "Zona 18, meridian tengah 105° BT"],
      "1) Zona = bulatkan ke bawah [(λ + 180) ÷ 6] + 1 = bulatkan ke bawah [(106,8 + 180) ÷ 6] + 1 = bulatkan ke bawah (47,8) + 1 = 47 + 1 = 48.\n2) Meridian tengah = 6 × zona − 183 = 6 × 48 − 183 = 288 − 183 = 105° BT.\nZona 48 membentang dari 102° BT hingga 108° BT. Wilayah Indonesia tercakup dalam zona UTM 46 sampai 54. Karena Jakarta di belahan bumi selatan, zona penuhnya ditulis 48S (atau 48M menurut sabuk lintang).\n\nPengecoh: zona 47 dan 49 salah membulatkan. Meridian tengah 108° adalah batas timur zona. Zona 18 adalah zona di belahan barat bumi.",
      None),
    Q("Perhatikan posisi titik A (E 500.000; N 9.200.000) dan B (E 503.000; N 9.204.000) pada grid UTM berikut.\n\nAzimut grid dan jarak A ke B adalah …",
      ["36,9° dan 5.000 m", "53,1° dan 5.000 m", "36,9° dan 7.000 m", "216,9° dan 5.000 m", "143,1° dan 5.000 m"],
      "1) ΔE = 503.000 − 500.000 = +3.000 m; ΔN = 9.204.000 − 9.200.000 = +4.000 m.\n2) ΔE dan ΔN positif → kuadran I (timur laut).\n3) θ = arctan |ΔE ÷ ΔN| = arctan (3.000 ÷ 4.000) = arctan 0,75 ≈ 36,9°. Di kuadran I, azimut = θ = 36,9°.\n4) Jarak = √(3.000² + 4.000²) = √25.000.000 = 5.000 m.\nAzimut diukur dari utara searah jarum jam.\n\nPengecoh: 53,1° memakai arctan (ΔN ÷ ΔE). 7.000 m menjumlahkan ΔE dan ΔN. 216,9° adalah azimut balik. 143,1° adalah azimut untuk kuadran II.",
      f_azimut),
    Q("Perhatikan nilai pantulan empat piksel citra satelit berikut. NDVI = (NIR − Merah) ÷ (NIR + Merah).\n\nPiksel yang paling mungkin merupakan vegetasi rapat beserta nilai NDVI-nya adalah …",
      ["P, sekitar 0,67", "Q, sekitar 0,20", "R, sekitar −0,33", "S, sekitar 0,06", "P, sekitar 0,40"],
      "Hitung NDVI tiap piksel:\n• P: (0,40 − 0,08) ÷ (0,40 + 0,08) = 0,32 ÷ 0,48 ≈ 0,67 → vegetasi rapat dan sehat.\n• Q: (0,30 − 0,20) ÷ 0,50 = 0,20 → vegetasi jarang.\n• R: (0,03 − 0,06) ÷ 0,09 ≈ −0,33 → air (NDVI negatif).\n• S: (0,25 − 0,22) ÷ 0,47 ≈ 0,06 → lahan terbuka atau permukiman.\nVegetasi sehat menyerap kuat cahaya merah untuk fotosintesis (klorofil) dan memantulkan kuat inframerah dekat karena struktur sel daun, sehingga NDVI-nya tinggi. NDVI berkisar −1 sampai +1.\n\nPengecoh: Q, R, dan S memiliki NDVI rendah atau negatif. 0,40 hanya nilai pantulan NIR P, bukan NDVI.",
      f_ndvi),
    Q("Perhatikan citra NDVI kawasan Kintamani berikut (lokasi P, Q, R, dan S sama dengan citra warna asli Kaldera Batur).\n\nUrutan nilai NDVI dari tertinggi ke terendah untuk objek S, Q, dan P adalah …",
      ["S, Q, P", "P, Q, S", "Q, S, P", "S, P, Q", "P, S, Q"],
      "NDVI = (NIR − Merah) ÷ (NIR + Merah) dihitung langsung dari saluran 8 dan 4 Sentinel-2.\n• S (hutan dan kebun di lereng luar): hijau tua, NDVI tinggi ±0,7–0,9 karena vegetasi rapat memantulkan kuat inframerah dekat.\n• Q (aliran lava muda): kuning muda, NDVI rendah ±0,1–0,2 karena hampir tanpa vegetasi.\n• P (Danau Batur): merah, NDVI negatif karena air menyerap kuat inframerah dekat sehingga pantulan NIR lebih kecil daripada merah.\nJadi urutannya S > Q > P. Peta NDVI dipakai untuk memantau kerapatan vegetasi, kekeringan, dan pemulihan lahan setelah letusan.\n\nPengecoh: air (P) selalu memiliki NDVI terendah, sedangkan hutan (S) tertinggi.",
      s_batur_n),
    Q("Perhatikan empat teknik penyajian peta tematik berikut.\n\nData kepadatan penduduk per provinsi paling tepat disajikan dengan teknik …",
      ["P, koroplet", "Q, titik (dot)", "R, simbol proporsional", "S, isopleth", "Q dan S sekaligus"],
      "Teknik penyajian peta tematik:\n• P – koroplet (choropleth): wilayah administrasi diwarnai dengan gradasi warna sesuai kelas nilai. Cocok untuk data rasio atau kepadatan per wilayah, seperti kepadatan penduduk dan persentase penduduk miskin.\n• Q – titik (dot map): setiap titik mewakili sejumlah objek, cocok untuk persebaran jumlah absolut.\n• R – simbol proporsional: ukuran simbol sebanding dengan jumlah absolut, misalnya jumlah penduduk kota.\n• S – isopleth atau isoline: garis yang menghubungkan nilai sama untuk fenomena kontinu, seperti suhu dan curah hujan.\nKepadatan penduduk adalah data rasio per wilayah, sehingga paling tepat menggunakan koroplet.\n\nPengecoh: titik dan simbol proporsional untuk jumlah absolut. Isopleth untuk fenomena kontinu yang tidak dibatasi wilayah administrasi.",
      f_tematik),
]

P1 = [
    Q("Perhatikan jarak dua kota yang sama pada dua peta berikut.\n\nSkala Peta II adalah …",
      ["1 : 20.000", "1 : 125.000", "1 : 2.000", "1 : 200.000", "1 : 30.000"],
      "1) Jarak sebenarnya dari Peta I = 6 cm × 50.000 = 300.000 cm (3 km).\n2) Penyebut Peta II = jarak sebenarnya ÷ jarak peta = 300.000 ÷ 15 = 20.000.\n3) Skala Peta II = 1 : 20.000.\nPeta II berskala lebih besar daripada Peta I karena penyebutnya lebih kecil, sehingga jarak yang sama tampak lebih panjang dan rinciannya lebih banyak.\n\nPengecoh: 1 : 125.000 membalik perbandingan (50.000 × 15 ÷ 6). 1 : 2.000 dan 1 : 200.000 salah satuan. 1 : 30.000 tidak sesuai perhitungan.",
      f_skala2),
    Q("Perhatikan pola garis kontur berikut.\n\nPola yang menunjukkan lembah sungai adalah …",
      ["R", "P", "Q", "S", "T"],
      "Identifikasi pola kontur (ketinggian bertambah ke utara pada R dan S):\n• P: kontur tertutup dengan nilai makin tinggi ke dalam → bukit atau puncak.\n• Q: kontur tertutup dengan nilai makin rendah ke dalam dan bergerigi ke arah dalam → depresi (cekungan).\n• R: kontur berbentuk V dengan ujung runcing menunjuk ke arah yang lebih tinggi (hulu) → lembah sungai. Di lembah, untuk mencapai ketinggian yang sama harus berjalan lebih jauh ke hulu, sehingga kontur melengkung ke arah hulu.\n• S: kontur berbentuk V atau U dengan ujung menunjuk ke arah yang lebih rendah → punggungan.\n• T: kontur sangat rapat di bagian bawah lalu renggang → lereng curam di bawah dan landai di atas.\nAturan praktis: huruf V pada lembah menunjuk ke hulu.\n\nPengecoh: P bukit, Q depresi, S punggungan, T lereng curam.",
      f_bentukkontur),
    Q("Pada pukul 08.00 waktu matahari setempat di kota yang terletak pada 105° BT, waktu matahari setempat di kota pada 135° BT adalah …",
      ["Pukul 10.00", "Pukul 06.00", "Pukul 09.00", "Pukul 10.30", "Pukul 11.00"],
      "Bumi berotasi 360° dalam 24 jam, sehingga setiap 15° bujur berselisih 1 jam (1° = 4 menit).\nSelisih bujur = 135° − 105° = 30° → selisih waktu = 30 ÷ 15 = 2 jam.\nKota di sebelah timur mengalami waktu lebih awal (matahari terbit lebih dulu), sehingga waktunya lebih maju: 08.00 + 2 jam = 10.00.\nZona waktu resmi Indonesia (WIB, WITA, WIT) disusun berdasarkan meridian 105°, 120°, dan 135° BT.\n\nPengecoh: 06.00 mengurangkan karena keliru arah. 09.00 hanya menambah satu jam. 10.30 dan 11.00 salah menghitung selisih.",
      None),
    Q("Perhatikan diagram pemotretan udara tegak berikut.\n\nSkala foto udara yang dihasilkan adalah …",
      ["1 : 20.000", "1 : 23.289", "1 : 3.289", "1 : 200.000", "1 : 2.000"],
      "Skala foto udara = f ÷ H, dengan H adalah tinggi terbang di atas medan, bukan di atas permukaan laut.\n1) H = 3.540 m − 500 m = 3.040 m.\n2) f = 152 mm = 0,152 m.\n3) Skala = 0,152 ÷ 3.040 = 1 : 20.000.\nKesalahan umum adalah memakai tinggi di atas permukaan laut: 0,152 ÷ 3.540 = 1 : 23.289. Karena tinggi medan bervariasi, skala foto udara tidak seragam; daerah yang lebih tinggi berskala lebih besar karena lebih dekat ke kamera.\n\nPengecoh: 1 : 23.289 memakai tinggi di atas permukaan laut. 1 : 3.289 memakai 500 m. 1 : 200.000 dan 1 : 2.000 salah satuan.",
      f_foto),
    Q("Perhatikan citra Sentinel-2 warna asli pesisir Kalimantan Timur berikut.\n\nBentuk lahan utama yang tampak pada citra adalah …",
      ["Delta dengan banyak saluran distributari", "Kaldera dengan danau di tengahnya", "Gumuk pasir di pantai berangin kering", "Atol dengan laguna di bagian tengah", "Lembah glasial berbentuk huruf U"],
      "Citra menunjukkan Delta Mahakam. Sungai Mahakam bercabang menjadi banyak saluran distributari berair keruh kecokelatan karena membawa sedimen tersuspensi, lalu mengalir menuju Selat Makassar. Di antara saluran terdapat pulau-pulau delta yang tertutup vegetasi hijau tua, yaitu hutan nipah dan mangrove, sebagian telah dibuka menjadi tambak. Delta terbentuk karena endapan sungai lebih cepat tertimbun daripada dipindahkan gelombang dan arus pasang surut. Delta Mahakam juga kaya minyak dan gas bumi.\nPerhatikan pula awan di sudut kanan atas citra: inilah kelemahan citra optik di daerah tropis basah, sehingga pemantauan rutin sering dilengkapi citra radar (SAR) yang dapat menembus awan.\n\nPengecoh: tidak ada kaldera, gumuk pasir, atol, atau lembah glasial pada citra.",
      s_mahakam),
    Q("Perhatikan kurva pantulan spektral tiga objek berikut.\n\nKurva vegetasi sehat dan alasan yang tepat adalah …",
      ["Q, pantulan inframerah dekatnya sangat tinggi", "P, pantulannya naik perlahan dan stabil", "R, pantulannya paling rendah di semua panjang gelombang",
       "Q, pantulan cahaya merahnya paling tinggi", "P, pantulan biru dan hijaunya paling rendah"],
      "Ciri kurva pantulan spektral:\n• Q – vegetasi sehat: pantulan rendah pada cahaya biru dan merah (diserap klorofil), puncak kecil pada hijau (±0,55 μm), lalu naik tajam pada inframerah dekat (±0,7–1,3 μm, red edge) karena struktur sel mesofil daun. Terdapat lembah serapan air pada ±1,45 dan ±1,95 μm.\n• P – tanah: pantulan naik perlahan dengan bertambahnya panjang gelombang.\n• R – air: pantulan rendah, sedikit pada cahaya biru, dan hampir nol pada inframerah karena diserap air.\nPerbedaan pantulan merah dan inframerah dekat inilah dasar perhitungan NDVI.\n\nPengecoh: kurva naik perlahan adalah tanah. Kurva paling rendah adalah air. Vegetasi justru menyerap cahaya merah.",
      f_spektral),
    Q("Interval kontur yang ideal untuk peta topografi berskala 1 : 50.000 adalah …",
      ["25 m", "50 m", "12,5 m", "2,5 m", "100 m"],
      "Rumus praktis interval kontur (CI) = penyebut skala ÷ 2.000 (dalam meter).\nCI = 50.000 ÷ 2.000 = 25 m.\nContoh lain: skala 1 : 25.000 → CI = 12,5 m, dan skala 1 : 100.000 → CI = 50 m. Rumus ini merupakan pedoman umum; interval sebenarnya juga menyesuaikan kondisi relief. Daerah datar dapat memakai interval lebih kecil, sedangkan daerah pegunungan memakai interval lebih besar agar kontur tidak terlalu rapat. Setiap kontur ke-4 atau ke-5 biasanya digambar lebih tebal sebagai kontur indeks.\n\nPengecoh: 50 m untuk 1 : 100.000. 12,5 m untuk 1 : 25.000. 2,5 m dan 100 m salah perhitungan.",
      None),
    Q("Perhatikan dua lapisan data raster berikut.\n\nLuas lahan yang memenuhi syarat lereng < 15% dan jenis tanah aluvial sekaligus adalah …",
      ["9 ha", "14 ha", "10 ha", "8 ha", "15 ha"],
      "Tumpang susun (overlay) dengan operasi irisan (AND) memilih sel yang memenuhi kedua syarat sekaligus. Bandingkan sel demi sel:\n• Baris 1: kolom 1 dan 2 → 2 sel.\n• Baris 2: kolom 1 dan 2 → 2 sel.\n• Baris 3: kolom 1, 2, dan 3 → 3 sel.\n• Baris 4: hanya kolom 2 (kolom 1 bertanah latosol, kolom 3 berlereng ≥ 15%) → 1 sel.\n• Baris 5: hanya kolom 3 (kolom 1–2 latosol, kolom 4 grumusol) → 1 sel.\nTotal = 9 sel × 1 ha = 9 ha.\nOverlay adalah analisis inti SIG untuk menentukan kesesuaian lahan, misalnya lokasi permukiman atau pertanian.\n\nPengecoh: 14 ha menghitung semua sel berlereng < 15% saja. 10 ha menghitung semua sel aluvial saja. 15 ha memakai operasi gabungan (OR) secara keliru. 8 ha terlewat satu sel.",
      f_overlay),
    Q("Perhatikan citra Sentinel-2 warna asli Kabupaten Tangerang berikut.\n\nKawasan di sekitar P paling mudah dikenali sebagai bandar udara terutama berdasarkan unsur interpretasi …",
      ["Bentuk dan pola landasan sejajar", "Rona gelap seperti tubuh air", "Tekstur kasar seperti hutan lebat", "Bayangan gedung pencakar langit", "Warna merah khas vegetasi"],
      "Kawasan P adalah Bandara Soekarno-Hatta. Objek dikenali terutama dari:\n• Bentuk: dua landasan pacu lurus panjang berwarna abu-abu terang. Dengan skala citra, panjangnya sekitar 3–3,6 km, ukuran khas landasan pesawat besar.\n• Pola: kedua landasan sejajar dan dihubungkan banyak jalur taksi (taxiway) yang teratur.\n• Asosiasi: terdapat gedung terminal besar dengan atap jingga di antara kedua landasan, area parkir pesawat (apron), dan jalan akses.\nKombinasi bentuk, ukuran, pola, dan asosiasi membuat objek ini mudah diinterpretasi walaupun resolusi citra hanya 10 m.\n\nPengecoh: landasan berona terang, bukan gelap seperti air. Teksturnya halus. Citra 10 m tidak menampilkan bayangan gedung tinggi. Warna asli vegetasi adalah hijau, bukan merah.",
      s_soetta),
    Q("Koordinat sebuah titik yang diukur dengan GPS pada datum WGS84 dapat bergeser puluhan hingga ratusan meter jika diplot pada peta lama yang memakai datum lokal. Penyebab utamanya adalah …",
      ["Datum memakai elipsoid acuan dan titik pusat berbeda", "Satelit GPS tidak beredar di atas Indonesia", "Peta lama tidak memakai sistem koordinat apa pun",
       "Garis lintang dan bujur berubah setiap tahun", "Bentuk bumi berubah menjadi bulat sempurna"],
      "Datum geodetik adalah acuan yang mendefinisikan bentuk dan ukuran bumi (elipsoid) serta posisinya terhadap bumi. Datum lokal lama, seperti Datum Batavia (Genuk) atau ID74, memakai elipsoid dan titik pusat yang disesuaikan untuk wilayah tertentu, sedangkan WGS84 adalah datum global yang berpusat di pusat massa bumi. Akibatnya koordinat titik yang sama berbeda angkanya pada datum berbeda dan dapat bergeser puluhan hingga ratusan meter. Karena itu diperlukan transformasi datum. Indonesia kini memakai Sistem Referensi Geospasial Indonesia (SRGI 2013).\n\nPengecoh: satelit GPS mencakup seluruh dunia. Peta lama tetap memakai sistem koordinat. Lintang dan bujur tidak berubah tahunan. Bumi tidak bulat sempurna.",
      None),
]

P2 = [
    Q(f"Perhatikan peta analisis buffer sempadan sungai berikut.\n\nJumlah rumah yang berada di dalam zona penyangga 100 m dari sungai adalah …",
      [f"{BUF_N} rumah", f"{len(HOUSES)} rumah", f"{len(HOUSES) - BUF_N + 2} rumah", f"{BUF_N - 2} rumah", f"{BUF_N + 3} rumah"],
      f"Analisis buffer membuat zona dengan jarak tertentu di sekitar objek (titik, garis, atau poligon). Pada peta, zona biru muda adalah wilayah dalam radius 100 m dari sungai. Rumah yang berada di dalam zona tersebut berjumlah {BUF_N}, sedangkan {len(HOUSES) - BUF_N} rumah lainnya berada di luar zona.\nBuffer sempadan sungai digunakan untuk perencanaan tata ruang, misalnya mengidentifikasi bangunan yang melanggar sempadan atau berisiko banjir dan longsor tebing, sebagai dasar relokasi atau penataan. Buffer juga dipakai untuk analisis jangkauan layanan, seperti radius sekolah atau rumah sakit.\n\nPengecoh: {len(HOUSES)} rumah adalah seluruh rumah pada peta. Angka lain salah menghitung rumah yang berada di tepi zona.",
      f_buffer),
    Q("Perhatikan data stasiun hujan dan poligon Thiessen DAS W berikut.\n\nCurah hujan wilayah DAS W menurut metode Thiessen adalah …",
      ["2.310 mm/tahun", "2.400 mm/tahun", "2.190 mm/tahun", "7.200 mm/tahun", "2.520 mm/tahun"],
      "Metode Thiessen menghitung rata-rata berbobot luas:\nP = Σ(Pᵢ × Aᵢ) ÷ ΣA\n= (1.800 × 40 + 2.400 × 35 + 3.000 × 25) ÷ 100\n= (72.000 + 84.000 + 75.000) ÷ 100\n= 231.000 ÷ 100 = 2.310 mm/tahun.\nRata-rata aritmetika biasa (1.800 + 2.400 + 3.000) ÷ 3 = 2.400 mm/tahun lebih besar karena tidak memperhitungkan bahwa stasiun A (curah hujan terendah) mewakili wilayah paling luas. Metode Thiessen lebih tepat bila sebaran stasiun tidak merata.\n\nPengecoh: 2.400 adalah rata-rata aritmetika. 7.200 adalah jumlah ketiga nilai. 2.190 dan 2.520 salah memasangkan bobot.",
      f_thiessen),
    Q("Perhatikan data morfometri dua DAS berikut. Faktor bentuk Ff = A ÷ Lb².\n\nPernyataan yang paling tepat adalah …",
      ["DAS Q (Ff = 1,0) lebih cepat mencapai puncak banjir", "DAS P (Ff = 0,25) lebih cepat mencapai puncak banjir", "Kedua DAS sama karena luasnya sama",
       "DAS Q (Ff = 0,05) berbentuk sangat memanjang", "DAS P (Ff = 10) berbentuk membulat"],
      "Hitung faktor bentuk:\n• DAS P: Ff = 400 ÷ 40² = 400 ÷ 1.600 = 0,25 → memanjang.\n• DAS Q: Ff = 400 ÷ 20² = 400 ÷ 400 = 1,0 → membulat.\nPada DAS membulat, air dari berbagai anak sungai tiba di titik keluar (outlet) dalam waktu yang hampir bersamaan, sehingga debit puncak tinggi dan tercapai cepat. Pada DAS memanjang, kedatangan air tersebar dalam waktu lebih lama, sehingga puncak banjir lebih rendah dan lebih lambat. Walaupun luasnya sama, bentuk DAS memengaruhi respons hidrologi.\n\nPengecoh: DAS P justru lebih lambat. Luas sama tidak berarti respons sama. 0,05 dan 10 adalah salah hitung.",
      f_das),
    Q("Sebuah DAS seluas 400 km² memiliki total panjang seluruh sungai 600 km. Kerapatan aliran (Dd) DAS tersebut dan maknanya adalah …",
      ["1,5 km/km², kerapatan sedang", "0,67 km/km², kerapatan rendah", "240.000 km³, kerapatan sangat tinggi", "1,5 km², luas rata-rata anak sungai",
       "200 km/km², kerapatan sangat tinggi"],
      "Kerapatan aliran Dd = ΣL ÷ A = 600 km ÷ 400 km² = 1,5 km/km².\nKerapatan aliran mencerminkan seberapa banyak alur sungai per satuan luas. Nilai tinggi umumnya terjadi pada batuan kedap air, tanah tipis, lereng curam, dan vegetasi jarang, sehingga limpasan permukaan besar dan banjir cepat terjadi. Nilai rendah terjadi pada batuan permeabel seperti karst atau pasir, karena air lebih banyak meresap. Klasifikasi umum: Dd < 0,25 rendah; 0,25–10 sedang; > 10 tinggi (km/km²).\n\nPengecoh: 0,67 membalik pembagian. 240.000 mengalikan keduanya. Dd bukan luas anak sungai. 200 adalah selisih, bukan kerapatan.",
      None),
    Q("Perhatikan peta kontur sebuah bukit berikut.\n\nTitik yang terletak pada lereng paling curam adalah …",
      ["P, karena garis konturnya paling rapat", "Q, karena berada di puncak tertinggi", "R, karena paling jauh dari puncak",
       "S, karena garis konturnya paling renggang", "Q, karena garis konturnya paling rapat"],
      "Kecuraman lereng pada peta kontur ditunjukkan oleh kerapatan garis kontur: makin rapat, makin curam, karena perubahan ketinggian yang sama terjadi pada jarak mendatar yang lebih pendek.\n• P berada di sisi barat bukit yang konturnya paling rapat → lereng paling curam.\n• Q berada di dekat puncak, yang relatif datar; kontur di puncak justru melingkar renggang.\n• R berada jauh di kaki bukit yang landai.\n• S berada di sisi selatan bukit yang bentuknya memanjang utara–selatan, sehingga konturnya lebih renggang daripada sisi barat.\n\nPengecoh: puncak bukan bagian tercuram. Jarak dari puncak tidak menentukan kecuraman. Kontur renggang menunjukkan lereng landai.",
      f_curam),
    Q("Perhatikan skor kesesuaian tiga unit lahan berikut. Nilai akhir = Σ(skor × bobot).\n\nUnit lahan yang paling sesuai beserta nilai akhirnya adalah …",
      ["Z, nilai 24", "Y, nilai 21", "X, nilai 21", "Y, nilai 11", "Z, nilai 10"],
      "Hitung nilai berbobot:\n• X: 4 × 3 + 3 × 2 + 3 × 1 = 12 + 6 + 3 = 21.\n• Y: 3 × 3 + 4 × 2 + 4 × 1 = 9 + 8 + 4 = 21.\n• Z: 5 × 3 + 4 × 2 + 1 × 1 = 15 + 8 + 1 = 24.\nUnit Z paling sesuai dengan nilai 24.\nJika bobot diabaikan, jumlah skor biasa menjadi X = 10, Y = 11, dan Z = 10, sehingga Y tampak paling sesuai. Inilah pentingnya pembobotan: kemiringan diberi bobot terbesar karena paling menentukan kesesuaian lahan, dan Z unggul pada faktor tersebut.\n\nPengecoh: Y 11 dan Z 10 adalah jumlah tanpa bobot. X dan Y bernilai 21, lebih rendah daripada Z.",
      f_skor),
    Q("Dalam SIG, data jaringan jalan biasanya disimpan sebagai garis dengan atribut nama dan kelas jalan, sedangkan data citra satelit disimpan sebagai sel-sel piksel. Kedua model data tersebut berturut-turut adalah …",
      ["Vektor dan raster", "Raster dan vektor", "Atribut dan tabel", "Vektor dan vektor", "Raster dan raster"],
      "SIG mengenal dua model data spasial utama:\n• Vektor: objek digambarkan sebagai titik (sumur, kota), garis (jalan, sungai), dan poligon (batas wilayah, danau). Batasnya tegas dan setiap objek dapat diberi atribut. Model ini cocok untuk objek diskret.\n• Raster: ruang dibagi menjadi sel atau piksel berukuran sama, dan setiap sel berisi nilai, misalnya pantulan citra, ketinggian (DEM), atau suhu. Model ini cocok untuk fenomena kontinu dan data penginderaan jauh.\nJaringan jalan disimpan sebagai vektor garis, sedangkan citra satelit adalah raster.\n\nPengecoh: urutan tertukar atau keliru menyebut atribut sebagai model data spasial.",
      None),
    Q("Perhatikan lembar peta dengan grid geografis berikut.\n\nKoordinat titik K adalah …",
      ["7°30′ LS dan 110°45′ BT", "7°30′ LU dan 110°45′ BT", "7°45′ LS dan 110°30′ BT", "110°45′ LS dan 7°30′ BT", "7°15′ LS dan 110°45′ BT"],
      "Baca koordinat dari garis grid:\n• Lintang: titik K berada pada garis 7°30′. Karena nilai lintang makin besar ke arah bawah (selatan), wilayah ini berada di lintang selatan → 7°30′ LS.\n• Bujur: titik K berada pada garis 110°45′ BT.\nJadi koordinat K adalah 7°30′ LS dan 110°45′ BT. Penulisan koordinat lazimnya lintang terlebih dahulu, lalu bujur. Titik M berada pada 7°45′ LS dan 110°15′ BT.\n\nPengecoh: LU keliru karena wilayah berada di selatan ekuator. 7°45′ LS dan 110°30′ BT salah membaca grid. Lintang dan bujur tertukar. 7°15′ LS salah membaca arah.",
      f_koord),
    Q("Perhatikan citra Sentinel-2 warna asli Kota Jambi berikut. Sungai P berona kuning kecokelatan dan berkelok-kelok kuat, sedangkan Q adalah kawasan kota.\n\nInterpretasi yang paling tepat untuk sungai P adalah …",
      ["Sungai bermeander yang sarat sedimen", "Sungai lurus di lembah V yang curam", "Kanal irigasi buatan yang airnya jernih", "Sungai bawah tanah di kawasan karst", "Jalan raya beraspal yang berkelok"],
      "Sungai P adalah Sungai Batanghari, sungai terpanjang di Sumatra. Di dataran rendah Jambi, kemiringan dasar sungai sangat kecil, sehingga aliran berkelok-kelok membentuk meander: erosi terjadi di tikungan luar dan pengendapan di tikungan dalam (point bar). Rona kuning kecokelatan menunjukkan banyak sedimen tersuspensi hasil erosi lahan di bagian hulu, karena partikel sedimen memantulkan kuat cahaya tampak. Kota Jambi (Q) tumbuh di tepi sungai karena sungai sejak lama menjadi jalur transportasi dan perdagangan.\nDari citra multiwaktu dapat dipantau perpindahan alur meander dan pembentukan danau tapal kuda (oxbow lake).\n\nPengecoh: sungai pada citra tidak lurus dan berada di dataran rendah. Kanal tidak berkelok alami. Sungai bawah tanah tidak tampak di permukaan. Jalan raya tidak selebar dan sekeruh itu.",
      s_batang),
    Q("Perhatikan citra Sentinel-2 warna asli Kepulauan Seribu berikut.\n\nPerbedaan rona Q (biru kehijauan terang) dan R (biru gelap) terutama disebabkan oleh …",
      ["Q dangkal di atas terumbu, R laut dalam", "Q laut dalam, R perairan dangkal berpasir", "Q tumpahan minyak, R air laut bersih", "Q hutan mangrove, R padang lamun", "Q awan tipis, R bayangan awan tebal"],
      "Cahaya tampak, terutama biru dan hijau, dapat menembus air laut jernih beberapa meter hingga puluhan meter. Di perairan dangkal (Q), cahaya mencapai dasar berupa pasir dan terumbu karang lalu dipantulkan kembali, sehingga rona tampak biru kehijauan terang. Di laut dalam (R), hampir semua cahaya diserap air sebelum mencapai dasar, sehingga rona tampak biru gelap. P adalah daratan pulau kecil berpenghuni dengan vegetasi dan permukiman.\nPrinsip ini dipakai untuk memetakan terumbu karang, padang lamun, dan kedalaman perairan dangkal (batimetri turunan citra). Rataan terumbu yang luas mengelilingi pulau kecil adalah ciri khas Kepulauan Seribu.\n\nPengecoh: Q justru dangkal. Tidak terlihat tumpahan minyak, mangrove luas, atau awan pada lokasi Q dan R.",
      s_pari),
]

P3 = [
    Q("Perhatikan diagram deklinasi pada peta topografi berikut.\n\nBesar deklinasi magnetis pada tahun 2025 adalah …",
      ["1°30′ timur", "3°30′ timur", "2°30′ barat", "0°30′ timur", "1°30′ barat"],
      "Deklinasi magnetis adalah sudut antara utara geografis atau grid dan utara magnetis. Nilainya berubah setiap tahun karena medan magnet bumi bergeser.\n1) Selisih tahun = 2025 − 2015 = 10 tahun.\n2) Perubahan = 10 × 6′ = 60′ = 1° ke arah barat.\n3) Deklinasi 2025 = 2°30′ timur − 1° = 1°30′ timur.\nKarena perubahan ke barat mengurangi deklinasi timur, utara magnetis bergeser mendekati utara grid. Nilai ini dipakai untuk mengubah azimut grid menjadi azimut magnetis dalam navigasi darat.\n\nPengecoh: 3°30′ timur menambahkan perubahan. 2°30′ barat dan 1°30′ barat salah arah. 0°30′ timur mengurangkan 2°.",
      f_dekl),
    Q("Seorang navigator berjalan dengan azimut 250°. Untuk kembali ke titik awal melalui jalur yang sama, ia harus berjalan dengan azimut …",
      ["70°", "110°", "160°", "340°", "430°"],
      "Azimut balik (back azimuth) = azimut ± 180°, dengan hasil dalam rentang 0°–360°.\nKarena 250° > 180°, azimut balik = 250° − 180° = 70°.\nAzimut 250° mengarah ke barat daya agak ke barat, sehingga arah kembali adalah timur laut agak ke timur (70°). Konsep ini dipakai dalam navigasi darat, reseksi, dan interseksi.\n\nPengecoh: 110° adalah 360° − 250°. 160° dan 340° tidak sesuai rumus. 430° melebihi 360° karena menambahkan 180° tanpa penyesuaian.",
      None),
    Q("Perhatikan peta kontur dan lima penampang berikut.\n\nPenampang yang sesuai dengan garis A–B adalah …",
      ["R", "P", "Q", "S", "T"],
      "Telusuri garis A–B dari barat ke timur:\n1) Dari A, ketinggian naik menuju bukit pertama yang tinggi (±750 m) di sepertiga bagian barat.\n2) Turun ke sadel di tengah.\n3) Naik ke bukit kedua yang lebih rendah (±500 m) di sebelah timur.\n4) Turun lagi menuju B.\nPenampang R menunjukkan pola tersebut: puncak tinggi di barat dan puncak lebih rendah di timur.\n• P adalah kebalikannya (dicerminkan), sehingga puncak tinggi berada di timur.\n• Q hanya memiliki satu puncak di tengah.\n• S terbalik (lembah menjadi puncak).\n• T memiliki tinggi relatif puncak yang tertukar.\nMembuat profil topografi dilakukan dengan memindahkan titik potong garis kontur ke grafik ketinggian.\n\nPengecoh: perhatikan urutan dan tinggi relatif kedua puncak dari A ke B.",
      f_profil),
    Q("Perhatikan citra Sentinel-2 warna asli pusat Kota Jakarta berikut.\n\nObjek P (lahan hijau persegi luas di tengah kota) dan Q (bangunan berbentuk oval) berturut-turut paling mungkin adalah …",
      ["Lapangan Monas dan Stadion GBK", "Danau buatan dan bandar udara", "Hutan lindung dan kolam retensi", "Sawah dan tempat pembuangan sampah", "Kebun raya dan pelabuhan peti kemas"],
      "Interpretasi memakai beberapa unsur sekaligus:\n• P: bentuk persegi sangat teratur, rona hijau (vegetasi taman), ukuran sekitar 1 km, berada di pusat kota dan dikelilingi jalan lebar serta gedung-gedung pemerintahan (situs dan asosiasi) → Lapangan Monas (Medan Merdeka).\n• Q: bentuk oval dengan lapangan di tengah, berasosiasi dengan kompleks olahraga di sekitarnya → Stadion Utama Gelora Bung Karno di Senayan.\nCitra juga memperlihatkan rona merah kecokelatan yang dominan, yaitu atap genteng permukiman padat, serta pola jalan utama dan jalan tol yang membentuk kerangka kota.\n\nPengecoh: P tidak berona gelap seperti air dan bukan sawah atau hutan lindung. Q terlalu kecil untuk bandara dan tidak berada di tepi laut seperti pelabuhan.",
      s_jakarta),
    Q("Perhatikan grafik rata-rata NDVI bulanan sebuah hamparan lahan berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Sawah dengan dua kali musim tanam padi dalam setahun", "Hutan primer dengan tajuk rapat sepanjang tahun", "Danau yang airnya kering setiap bulan",
       "Permukiman yang luasnya bertambah setiap bulan", "Sawah dengan tiga kali musim tanam padi setahun"],
      "Grafik NDVI menunjukkan dua siklus naik–turun: naik dari ±0,2 (Januari) ke puncak ±0,75 (Maret), turun ke ±0,2 (Mei), naik lagi ke ±0,72 (Juli), lalu turun ke ±0,15 (September–Oktober). Pola ini khas sawah padi: NDVI rendah saat tanah digenangi dan baru ditanam, naik saat padi tumbuh dan rimbun, lalu turun saat menguning dan dipanen. Dua puncak menunjukkan dua kali musim tanam, sedangkan September–November adalah masa bera.\nAnalisis deret waktu NDVI digunakan untuk memantau pola tanam, memperkirakan produksi, dan mendeteksi gagal panen.\n\nPengecoh: hutan primer memiliki NDVI tinggi stabil. Air memiliki NDVI negatif. Permukiman memiliki NDVI rendah stabil. Grafik hanya memperlihatkan dua puncak.",
      f_sawah),
    Q("Perhatikan susunan citra komposit 543 Landsat 8 berikut.\n\nPada citra komposit tersebut, vegetasi sehat tampak berwarna …",
      ["Merah", "Hijau", "Biru", "Hitam", "Putih"],
      "Pada komposit 543, saluran 5 (inframerah dekat) ditampilkan sebagai merah, saluran 4 (merah) sebagai hijau, dan saluran 3 (hijau) sebagai biru. Vegetasi sehat memantulkan sangat kuat gelombang inframerah dekat, sehingga nilai pada kanal merah layar paling tinggi dan vegetasi tampak merah cerah. Komposit ini disebut komposit warna semu (false color composite) standar. Semakin rapat dan sehat vegetasi, semakin merah warnanya. Sebaliknya, air tampak gelap atau hitam kebiruan, dan permukiman tampak biru kehijauan atau abu-abu.\n\nPengecoh: warna hijau muncul pada komposit warna asli (432). Biru, hitam, dan putih tidak sesuai karena pantulan tertinggi vegetasi ditampilkan sebagai merah.",
      f_komposit),
    Q("Pemerintah daerah ingin menentukan rute tercepat ambulans dari setiap desa ke rumah sakit terdekat dengan mempertimbangkan kecepatan dan arah jalan. Analisis SIG yang paling tepat adalah …",
      ["Analisis jaringan (network)", "Analisis buffer lingkaran sederhana", "Klasifikasi citra terbimbing", "Interpolasi curah hujan", "Analisis tumpang susun lereng"],
      "Analisis jaringan (network analysis) dalam SIG digunakan untuk memecahkan masalah yang berkaitan dengan jaringan garis, seperti jalan, sungai, atau pipa. Contohnya mencari rute terpendek atau tercepat, menentukan daerah layanan berdasarkan waktu tempuh, dan menentukan lokasi fasilitas optimal. Analisis ini memperhitungkan panjang ruas, kecepatan, arah satu jalur, dan hambatan. Hasilnya lebih realistis daripada buffer lingkaran yang hanya mengukur jarak garis lurus.\n\nPengecoh: buffer lingkaran mengabaikan jaringan jalan. Klasifikasi citra dan interpolasi curah hujan tidak terkait rute. Overlay lereng tidak menghitung waktu tempuh.",
      None),
    Q("Perhatikan data kepadatan penduduk delapan kabupaten berikut. Data akan dibagi menjadi 4 kelas dengan interval sama.\n\nKabupaten D termasuk kelas …",
      ["III (550–749)", "II (350–549)", "IV (750–950)", "I (150–349)", "III (500–699)"],
      "1) Lebar kelas = (nilai maksimum − nilai minimum) ÷ jumlah kelas = (950 − 150) ÷ 4 = 800 ÷ 4 = 200.\n2) Kelas:\n• I: 150–349\n• II: 350–549\n• III: 550–749\n• IV: 750–950\n3) Kabupaten D (560 jiwa/km²) termasuk kelas III.\nKlasifikasi interval sama mudah dipahami, tetapi dapat menghasilkan kelas yang anggotanya tidak seimbang bila data tidak tersebar merata. Metode lain adalah kuantil dan natural breaks (Jenks).\n\nPengecoh: kelas II, IV, dan I tidak mencakup 560. Kelas 500–699 memakai batas yang salah.",
      f_kelas),
    Q("Perhatikan peta tiga kota dan pembagian zona waktu Indonesia berikut.\n\nPesawat berangkat dari Jayapura pukul 09.00 WIT dan terbang selama 5 jam ke Medan. Pesawat tiba di Medan pukul …",
      ["12.00 WIB", "14.00 WIB", "16.00 WIB", "11.00 WIB", "13.00 WIB"],
      "1) Waktu tiba menurut jam Jayapura = 09.00 + 5 jam = 14.00 WIT.\n2) WIT = UTC+9 dan WIB = UTC+7, sehingga WIB terlambat 2 jam dari WIT.\n3) 14.00 WIT = 12.00 WIB.\nJadi pesawat tiba di Medan pukul 12.00 WIB. Perjalanan ke arah barat \"memperoleh\" waktu karena melintasi zona waktu yang lebih lambat.\n\nPengecoh: 14.00 WIB lupa mengonversi zona. 16.00 WIB menambah selisih zona. 11.00 dan 13.00 WIB salah menghitung selisih zona.",
      f_waktu),
    Q("Perhatikan citra Sentinel-2 warna asli Selat Sunda berikut. Pulau P berona cokelat gelap tanpa vegetasi dan mengeluarkan asap, sedangkan pulau Q dan R tertutup vegetasi lebat.\n\nPenjelasan yang paling tepat adalah …",
      ["P gunung api muda; Q dan R sisa kaldera lama", "P pulau karang; Q dan R gunung api aktif", "P gumuk pasir; Q dan R delta sungai", "P pulau buatan; Q dan R pulau reklamasi", "P atol; Q dan R terumbu karang tepi"],
      "P adalah Anak Krakatau, gunung api muda yang muncul dari laut pada 1927 di dalam kaldera bekas letusan dahsyat Krakatau 1883. Rona cokelat gelap tanpa vegetasi menunjukkan permukaan endapan piroklastik dan lava yang masih sering diperbarui oleh letusan, dan asap putih menunjukkan aktivitas vulkanik. Q (Pulau Sertung) dan R (Pulau Panjang), bersama Pulau Rakata di tenggara, adalah sisa tubuh gunung Krakatau purba yang membentuk dinding kaldera. Pulau-pulau tua tersebut sudah tertutup hutan karena tanahnya telah berkembang. Pada Desember 2018 longsoran lereng Anak Krakatau memicu tsunami di Selat Sunda.\n\nPengecoh: P bukan pulau karang, gumuk pasir, pulau buatan, atau atol, karena berbentuk kerucut vulkanik dan berasap.",
      s_krakatau),
]

P4 = [
    Q("Perhatikan titik A (E 412.000; N 9.180.000) dan B (E 418.000; N 9.172.000) pada grid UTM berikut.\n\nAzimut grid dari A ke B adalah …",
      ["143,1°", "36,9°", "323,1°", "216,9°", "126,9°"],
      "1) ΔE = 418.000 − 412.000 = +6.000 m; ΔN = 9.172.000 − 9.180.000 = −8.000 m.\n2) ΔE positif dan ΔN negatif → kuadran II (tenggara).\n3) θ = arctan |ΔE ÷ ΔN| = arctan (6.000 ÷ 8.000) = arctan 0,75 ≈ 36,9°.\n4) Di kuadran II, azimut = 180° − θ = 180° − 36,9° = 143,1°.\nJarak A–B = √(6.000² + 8.000²) = 10.000 m.\n\nPengecoh: 36,9° lupa menyesuaikan kuadran. 323,1° adalah azimut B ke A. 216,9° adalah azimut kuadran III. 126,9° memakai arctan (ΔN ÷ ΔE) secara keliru.",
      f_utm2),
    Q("Azimut grid dari titik A ke B adalah 143°. Deklinasi magnetis setempat 3° barat dan konvergensi grid diabaikan. Azimut magnetis yang harus dibidik dengan kompas adalah …",
      ["146°", "140°", "323°", "149°", "137°"],
      "Utara magnetis berada 3° di sebelah barat utara grid. Karena azimut diukur dari utara searah jarum jam, sudut yang diukur dari utara magnetis menjadi lebih besar sebesar deklinasi barat.\nAzimut magnetis = azimut grid + deklinasi barat = 143° + 3° = 146°.\nAturan umum: deklinasi barat ditambahkan dan deklinasi timur dikurangkan untuk mengubah azimut grid menjadi azimut magnetis. Kesalahan arah 3° pada perjalanan 10 km menimbulkan penyimpangan sekitar 520 m.\n\nPengecoh: 140° mengurangkan deklinasi barat. 323° adalah azimut balik. 149° dan 137° memakai koreksi ganda.",
      None),
    Q("Peta berskala 1 : 30.000 diperbesar dengan mesin fotokopi menjadi 150% dari ukuran semula. Skala peta baru adalah …",
      ["1 : 20.000", "1 : 45.000", "1 : 15.000", "1 : 30.000", "1 : 60.000"],
      "Saat peta diperbesar 150%, semua jarak di peta menjadi 1,5 kali, sedangkan jarak sebenarnya tetap. Akibatnya penyebut skala menjadi lebih kecil.\nPenyebut baru = penyebut lama × (panjang lama ÷ panjang baru) = 30.000 × (1 ÷ 1,5) = 20.000.\nJadi skala baru 1 : 20.000. Peta yang diperbesar menjadi berskala lebih besar, tetapi tingkat kerincian informasinya tidak bertambah karena hanya ukurannya yang membesar.\n\nPengecoh: 1 : 45.000 mengalikan dengan 1,5. 1 : 15.000 membagi dua. 1 : 30.000 mengabaikan pembesaran. 1 : 60.000 adalah hasil pengecilan setengah.",
      None),
    Q("Perhatikan peta kontur dengan sebuah sungai berikut.\n\nArah aliran sungai dan alasannya adalah …",
      ["Ke selatan, karena V kontur menunjuk ke utara (hulu)", "Ke utara, karena V kontur menunjuk ke utara (hilir)", "Ke selatan, karena V kontur menunjuk ke selatan (hulu)",
       "Ke timur, karena kontur rapat di sebelah timur", "Tidak dapat ditentukan dari garis kontur"],
      "Pada peta, nilai kontur bertambah ke arah utara (kontur indeks bagian atas bernilai lebih tinggi). Di tempat garis kontur memotong sungai, kontur membentuk huruf V yang ujungnya menunjuk ke utara, yaitu ke arah yang lebih tinggi atau hulu. Aturannya: huruf V kontur pada lembah sungai selalu menunjuk ke hulu. Karena air mengalir dari tempat tinggi ke rendah, sungai mengalir ke selatan.\nKetrampilan ini penting untuk menentukan arah aliran, batas DAS, dan lokasi aman dari banjir.\n\nPengecoh: V menunjuk ke hulu, bukan hilir. Ujung V berada di utara, bukan di selatan. Kontur tidak lebih rapat di timur. Arah aliran dapat ditentukan dari pola kontur.",
      f_sungai),
    Q("Perhatikan peta suhu permukaan hasil citra satelit siang hari berikut.\n\nFenomena yang ditunjukkan dan saluran citra yang digunakan adalah …",
      ["Pulau panas perkotaan, saluran inframerah termal", "Pulau panas perkotaan, saluran cahaya biru", "Inversi suhu, saluran gelombang mikro",
       "Efek rumah kaca, saluran ultraviolet", "Pendinginan kota, saluran inframerah dekat"],
      "Peta menunjukkan suhu permukaan tertinggi (±35°C) di titik P yang merupakan pusat kota, dan suhu menurun ke arah pinggiran hingga ±26°C di titik R. Titik Q menunjukkan pusat panas kecil, misalnya kawasan industri. Pola ini adalah pulau panas perkotaan (urban heat island), yang terjadi karena permukaan beton dan aspal menyerap panas, vegetasi dan air sedikit, serta panas dari kendaraan dan pendingin ruangan.\nSuhu permukaan diturunkan dari saluran inframerah termal (±10–12 μm), misalnya saluran 10 dan 11 Landsat 8, yang merekam energi pancaran objek.\n\nPengecoh: saluran biru, ultraviolet, dan inframerah dekat tidak mengukur suhu. Inversi suhu dan efek rumah kaca adalah fenomena atmosfer yang berbeda. Kota justru lebih panas.",
      f_uhi),
    Q("Pada peta dunia berproyeksi Mercator, Greenland tampak hampir sama luas dengan Afrika, padahal luas Afrika sekitar 14 kali Greenland. Sifat proyeksi Mercator yang menjelaskan hal ini adalah …",
      ["Konform: bentuk benar, luas terdistorsi", "Ekuivalen: luas benar, bentuk terdistorsi", "Ekuidistan: semua jarak tergambar benar",
       "Azimutal: arah benar dari titik pusat", "Bebas distorsi di seluruh wilayah"],
      "Proyeksi Mercator adalah proyeksi silinder konform: sudut dan bentuk lokal dipertahankan, sehingga garis arah tetap (loksodrom) tergambar lurus dan sangat berguna untuk navigasi laut. Sebagai konsekuensinya, skala bertambah ke arah kutub dan luas wilayah lintang tinggi tampak jauh lebih besar. Greenland yang berada di lintang tinggi tampak membesar, sedangkan Afrika yang dilalui ekuator tampak relatif sesuai. Tidak ada proyeksi yang bebas distorsi; selalu ada pilihan antara mempertahankan bentuk, luas, jarak, atau arah.\n\nPengecoh: proyeksi ekuivalen seperti Mollweide mempertahankan luas. Ekuidistan hanya mempertahankan jarak dari titik atau garis tertentu. Mercator bukan proyeksi azimutal.",
      None),
    Q(f"Perhatikan danau pada peta berikut. Luas diperkirakan dengan metode grid: kotak penuh dihitung 1 dan kotak sebagian dihitung ½.\n\nTerdapat {LF} kotak penuh dan {LP} kotak sebagian. Perkiraan luas danau sebenarnya adalah …",
      [f"{(LF + LP / 2) * 6.25:g} ha".replace(".", ","), f"{(LF + LP) * 6.25:g} ha".replace(".", ","), f"{LF * 6.25:g} ha".replace(".", ","),
       f"{(LF + LP / 2) * 0.625:g} ha".replace(".", ","), f"{(LF + LP / 2) * 62.5:g} ha".replace(".", ",")],
      f"1) Luas di peta ≈ {LF} + ({LP} × ½) = {LF + LP / 2:g} cm².\n2) Pada skala 1 : 25.000, 1 cm mewakili 250 m, sehingga 1 cm² mewakili 250 m × 250 m = 62.500 m² = 6,25 ha.\n3) Luas danau ≈ {LF + LP / 2:g} × 6,25 ha = {(LF + LP / 2) * 6.25:g} ha.\nMetode grid adalah cara sederhana mengukur luas bidang tidak beraturan pada peta. Ketelitiannya meningkat bila kotak grid diperkecil. Dalam SIG, luas poligon dihitung otomatis secara geometris.\n\nPengecoh: menghitung kotak sebagian sebagai penuh menghasilkan nilai terlalu besar. Mengabaikan kotak sebagian menghasilkan nilai terlalu kecil. Dua opsi lain salah konversi satuan (dikali 10 atau dibagi 10).".replace("6.25", "6,25"),
      f_danau),
    Q("Perhatikan citra Sentinel-2 warna asli kawasan Tengger, Jawa Timur berikut.\n\nObjek P yang berupa dataran luas, datar, berona abu-abu kecokelatan, dan tanpa vegetasi adalah …",
      ["Lautan pasir di dasar kaldera Tengger", "Danau kawah yang airnya telah kering", "Ladang sayuran berteras di lereng", "Aliran lava basal yang baru membeku", "Lapangan terbang di pegunungan"],
      "Citra menunjukkan Kaldera Tengger yang berdiameter sekitar 8–10 km. Dasar kaldera (P) tertutup pasir dan abu vulkanik halus hasil letusan berulang sehingga datar, berona abu-abu kecokelatan, dan hampir tanpa vegetasi; masyarakat menyebutnya Lautan Pasir. Di dalam kaldera tumbuh kerucut-kerucut gunung api muda: Gunung Batok (Q) yang lerengnya beralur-alur oleh erosi dan berona kehijauan, serta Gunung Bromo dengan kawah aktif berona putih keabu-abuan di sebelahnya. Dinding kaldera tampak sebagai tebing melengkung di tepi lautan pasir.\n\nPengecoh: tidak ada genangan air. Ladang berteras berada di lereng luar kaldera. Aliran lava berona lebih gelap dan bertekstur kasar. Tidak ada landasan pacu.",
      s_bromo),
    Q("Perhatikan peta kontur sebuah bukit berikut. Kontur indeks digambar lebih tebal setiap 250 m.\n\nKetinggian puncak T paling tepat dinyatakan sebagai …",
      ["Lebih dari 800 m, kurang dari 850 m", "Tepat 750 m", "Lebih dari 750 m, kurang dari 800 m", "Lebih dari 850 m, kurang dari 900 m", "Tepat 1.000 m"],
      "Dari peta, kontur indeks tebal bernilai 500 m dan 750 m. Dengan interval kontur 50 m, kontur di atas 750 m adalah 800 m. Kontur tertutup terdalam yang mengelilingi puncak T adalah kontur 800 m (satu garis tipis di dalam kontur indeks 750 m), dan tidak ada kontur 850 m. Jadi puncak T lebih tinggi daripada 800 m tetapi kurang dari 850 m. Pada peta topografi, ketinggian puncak yang pasti biasanya ditunjukkan dengan titik ketinggian (spot height) atau titik triangulasi.\n\nPengecoh: 750 m adalah kontur indeks, bukan puncak. 750–800 m mengabaikan kontur 800 m. 850–900 m memerlukan kontur 850 m yang tidak ada. 1.000 m terlalu tinggi.",
      f_puncak),
    Q("Perhatikan citra Sentinel-2 warna asli Kabupaten Sidoarjo berikut. Objek P berupa kawasan luas berona abu-abu yang dikelilingi tanggul di tengah permukiman.\n\nObjek P paling mungkin adalah …",
      ["Kolam penampungan semburan lumpur", "Danau vulkanik di kaldera tua", "Lapangan golf di tengah kota", "Waduk irigasi di lembah sungai", "Tambak garam di tepi pantai"],
      "Objek P adalah kawasan semburan Lumpur Sidoarjo (Lapindo) di Kecamatan Porong yang muncul sejak Mei 2006. Lumpur panas terus menyembur dan ditampung dalam kolam raksasa yang dibatasi tanggul. Berdasarkan skala citra, kolam berukuran sekitar 2–3 km, dengan luas terdampak sekitar 600 hektare yang menenggelamkan belasan desa, jalan tol, dan pabrik. Rona abu-abu, permukaan datar tanpa vegetasi, batas lurus bersudut (tanggul buatan), serta situs di tengah permukiman padat dan di sebelah Sungai Porong (tempat sebagian lumpur dialirkan) menjadi kunci interpretasinya.\n\nPengecoh: Sidoarjo tidak memiliki gunung api atau kaldera. Lapangan golf berwarna hijau. Waduk berada di lembah. Lokasinya tidak di tepi pantai.",
      s_lapindo),
]

P5 = [
    Q("Perhatikan jaringan jalan dengan waktu tempuh tiap ruas berikut.\n\nRute tercepat dari A ke F dan waktu tempuhnya adalah …",
      ["A–C–B–D–E–F, 13 menit", "A–B–D–F, 15 menit", "A–C–E–F, 15 menit", "A–B–D–E–F, 14 menit", "A–C–D–F, 16 menit"],
      "Hitung waktu tempuh beberapa rute:\n• A–B–D–F = 4 + 5 + 6 = 15 menit.\n• A–C–E–F = 2 + 10 + 3 = 15 menit.\n• A–B–D–E–F = 4 + 5 + 2 + 3 = 14 menit.\n• A–C–D–F = 2 + 8 + 6 = 16 menit.\n• A–C–B–D–E–F = 2 + 1 + 5 + 2 + 3 = 13 menit.\nRute tercepat adalah A–C–B–D–E–F (13 menit). Walaupun melewati lebih banyak simpul, rute ini memanfaatkan ruas-ruas cepat (A–C 2 menit dan C–B 1 menit untuk mencapai B lebih cepat daripada ruas A–B 4 menit). Prinsip ini dipakai algoritma Dijkstra dalam analisis jaringan SIG dan aplikasi navigasi.\n\nPengecoh: rute dengan simpul lebih sedikit belum tentu tercepat.",
      f_jaringan),
    Q("Perhatikan data calon lokasi tempat pengolahan sampah terpadu berikut. Syarat: jarak ke jalan ≤ 500 m, lereng < 8%, tidak rawan banjir, dan tidak di hutan lindung atau sawah.\n\nLokasi yang memenuhi semua syarat adalah …",
      ["P", "Q", "R", "S", "T"],
      "Periksa setiap lokasi:\n• P: jarak 300 m (memenuhi), lereng 5% (memenuhi), tidak rawan banjir, kebun campuran → memenuhi semua syarat.\n• Q: jarak 800 m → tidak memenuhi syarat aksesibilitas.\n• R: lereng 12% → terlalu curam.\n• S: rawan banjir dan berupa sawah → tidak memenuhi dua syarat.\n• T: hutan lindung → tidak boleh dialihfungsikan.\nPemilihan lokasi seperti ini dalam SIG dilakukan dengan analisis multikriteria melalui query dan overlay, yaitu menyaring sel atau poligon yang memenuhi semua syarat (operasi AND).\n\nPengecoh: setiap lokasi lain gagal memenuhi setidaknya satu syarat.",
      f_lokasi),
    Q("Perhatikan citra Sentinel-2 warna asli pesisir selatan Jawa Tengah berikut.\n\nObjek P yang berona hijau tua, bertekstur halus, dan diselingi banyak alur sungai pasang surut di sekitar laguna adalah …",
      ["Hutan mangrove di sekitar laguna", "Hutan pinus di daerah pegunungan", "Perkebunan teh di lereng gunung", "Padang rumput sabana yang kering", "Gumuk pasir di pantai selatan"],
      "Citra menunjukkan kawasan Segara Anakan, laguna di Kabupaten Cilacap yang terlindung dari Samudra Hindia oleh Pulau Nusakambangan. Objek P adalah hutan mangrove, salah satu yang terluas di Jawa. Ciri interpretasinya: rona hijau tua, tekstur halus dan seragam, situs di pesisir terlindung berair payau, serta asosiasi dengan alur-alur pasang surut yang berkelok. Di bagian barat tampak air keruh kecokelatan dari Sungai Citanduy yang membawa banyak sedimen. Sedimentasi ini menyebabkan laguna terus menyempit, sehingga menjadi masalah lingkungan dan mata pencaharian nelayan. Permukiman di sisi timur adalah Kota Cilacap.\n\nPengecoh: hutan pinus dan kebun teh berada di dataran tinggi. Sabana dan gumuk pasir berona cerah dan tidak berasosiasi dengan alur pasang surut.",
      s_segara),
    Q("Perhatikan luas tutupan lahan Kabupaten H hasil klasifikasi citra berikut.\n\nLaju penurunan luas hutan rata-rata per tahun (terhadap luas 2015) adalah …",
      ["2,5% per tahun", "20% per tahun", "300 ha per tahun", "25% per tahun", "3,3% per tahun"],
      "1) Penurunan luas hutan = 12.000 − 9.600 = 2.400 ha.\n2) Persentase penurunan terhadap 2015 = 2.400 ÷ 12.000 × 100% = 20% selama 8 tahun.\n3) Laju rata-rata = 20% ÷ 8 tahun = 2,5% per tahun.\nDalam satuan luas, penurunan rata-rata adalah 300 ha per tahun, tetapi soal menanyakan persentase. Grafik juga menunjukkan perkebunan bertambah 2.000 ha dan permukiman 400 ha, sehingga sebagian besar hutan yang hilang kemungkinan dikonversi menjadi perkebunan. Deteksi perubahan penggunaan lahan dari citra multiwaktu adalah aplikasi penting penginderaan jauh.\n\nPengecoh: 20% adalah total 8 tahun. 300 ha per tahun benar secara luas tetapi bukan persentase. 25% dan 3,3% salah perhitungan.",
      f_hutan),
    Q("Perhatikan gambar pendaki yang membidik dua objek dengan kompas berikut.\n\nUntuk menentukan posisinya (reseksi), pendaki menarik garis dari Puncak G dan Menara M dengan azimut berturut-turut …",
      ["135° dan 225°", "315° dan 45°", "45° dan 135°", "225° dan 315°", "135° dan 315°"],
      "Reseksi adalah menentukan posisi diri sendiri pada peta dengan membidik dua atau lebih objek yang dikenal.\nLangkahnya: bidik azimut ke objek, hitung azimut balik, lalu tarik garis dari objek pada peta dengan azimut balik tersebut. Perpotongan garis adalah posisi pendaki.\n• Azimut ke Puncak G = 315° → azimut balik = 315° − 180° = 135°.\n• Azimut ke Menara M = 45° → azimut balik = 45° + 180° = 225°.\nJadi garis ditarik dari G dengan azimut 135° dan dari M dengan azimut 225°.\nKebalikannya, interseksi adalah menentukan posisi objek yang belum diketahui dari dua titik yang diketahui.\n\nPengecoh: 315° dan 45° adalah azimut bidikan, bukan azimut balik. Opsi lain salah memasangkan atau salah menghitung.",
      f_reseksi),
    Q("Penginderaan jauh dengan wahana pesawat tanpa awak (drone) semakin banyak dipakai untuk pemetaan desa. Kelebihan utamanya dibandingkan citra satelit adalah …",
      ["Resolusi spasial sangat tinggi dan waktu fleksibel", "Selalu mencakup seluruh wilayah negara dalam satu foto", "Tidak terpengaruh cuaca dan angin sama sekali",
       "Tidak memerlukan pengolahan data setelah pemotretan", "Biayanya selalu lebih mahal daripada satelit"],
      "Drone terbang rendah (puluhan hingga ratusan meter), sehingga menghasilkan foto beresolusi spasial sangat tinggi (beberapa sentimeter per piksel). Waktu pemotretannya dapat diatur sesuai kebutuhan, misalnya saat cuaca cerah atau segera setelah bencana, dan dapat terbang di bawah awan. Hasilnya dapat diolah menjadi ortofoto dan model elevasi digital untuk peta desa, batas bidang tanah, dan perencanaan tata ruang.\nKelemahannya adalah cakupan wilayah sempit, durasi terbang terbatas oleh baterai, terpengaruh angin dan hujan, serta memerlukan izin terbang dan pengolahan fotogrametri.\n\nPengecoh: cakupan drone sempit, terpengaruh cuaca, memerlukan pengolahan data, dan untuk area kecil umumnya lebih murah.",
      None),
    Q("Perhatikan penampang medan antara titik A dan B berikut. Pengamat di A memiliki tinggi mata 2 m.\n\nPernyataan yang paling tepat tentang keterlihatan titik B dari A adalah …",
      ["B tidak terlihat karena terhalang bukit", "B terlihat karena B lebih tinggi daripada A", "B terlihat karena jaraknya hanya 4 km",
       "B tidak terlihat karena B lebih rendah daripada A", "B terlihat karena bukit lebih rendah daripada B"],
      "Analisis garis pandang (line of sight):\n1) Garis lurus dari mata pengamat di A (±302 m) ke B (500 m) naik ±49,5 m per km.\n2) Di posisi bukit (km ke-2), tinggi garis pandang ≈ 302 + 2 × 49,5 ≈ 401 m.\n3) Puncak bukit sekitar 550 m, jauh lebih tinggi daripada garis pandang.\nKarena bukit menghalangi garis pandang, B tidak terlihat dari A. Yang menentukan adalah perbandingan tinggi penghalang dengan garis pandang pada posisi penghalang, bukan sekadar perbandingan tinggi A dan B. Analisis keterlihatan (viewshed) dipakai untuk menentukan lokasi menara pemancar, pos pengamatan kebakaran, dan perencanaan pertahanan.\n\nPengecoh: B lebih tinggi daripada A tidak menjamin terlihat. Jarak bukan penentu. B tidak lebih rendah daripada A. Bukit (±550 m) justru lebih tinggi daripada B.",
      f_los),
    Q("Perhatikan citra Sentinel-2 komposit warna semu (NIR ditampilkan merah, merah sebagai hijau, hijau sebagai biru) di Karawang berikut.\n\nPetak-petak sawah tampak sebagian merah terang dan sebagian biru kehijauan. Penjelasan yang paling tepat adalah …",
      ["Merah padi rimbun; biru sawah tergenang atau bera", "Merah lahan terbakar; biru danau yang sangat dalam", "Merah permukiman padat; biru hutan lebat yang sehat",
       "Merah tanah kering; biru tanaman padi yang subur", "Merah dan biru menunjukkan jenis tanah yang berbeda"],
      "Pada komposit warna semu, saluran inframerah dekat (NIR) ditampilkan sebagai merah. Tanaman padi yang sedang tumbuh rimbun memantulkan kuat NIR sehingga tampak merah terang. Petak yang baru diolah dan digenangi, baru ditanam, atau sudah dipanen (bera) memiliki pantulan NIR rendah, sehingga tampak biru kehijauan hingga gelap. Karena petani di Karawang tidak menanam serentak, citra memperlihatkan mozaik petak dengan fase pertumbuhan berbeda. Garis-garis berbintik kehijauan yang memanjang adalah permukiman di sepanjang jalan dan saluran irigasi.\nCitra seperti ini dipakai untuk memantau fase tanam, memperkirakan waktu panen, dan menaksir produksi padi.\n\nPengecoh: tidak ada kebakaran atau danau dalam. Permukiman tidak tampak merah terang. Tanaman subur justru merah, bukan biru. Perbedaan warna mencerminkan tutupan vegetasi, bukan jenis tanah.",
      s_karawang),
    Q("Perhatikan tata letak komponen sebuah peta berikut.\n\nFungsi komponen nomor 3 adalah …",
      ["Menunjukkan letak daerah peta dalam wilayah lebih luas", "Menjelaskan arti simbol dan warna pada peta", "Menunjukkan arah utara dan orientasi peta",
       "Menyatakan perbandingan jarak peta dan jarak sebenarnya", "Menyebutkan isi dan tema peta secara singkat"],
      "Komponen nomor 3 berisi gambar wilayah yang lebih luas dengan kotak merah penanda lokasi daerah yang dipetakan, sehingga merupakan peta inset (peta sisipan). Fungsinya menunjukkan letak daerah yang dipetakan dalam wilayah yang lebih luas, misalnya letak sebuah kabupaten di dalam provinsi. Inset juga dapat dipakai untuk memperbesar bagian peta yang penting atau menampilkan pulau yang letaknya jauh.\nKomponen lain pada gambar adalah judul (1), legenda yang menjelaskan simbol dan warna (2), skala (4), dan orientasi atau arah utara (5). Peta juga sebaiknya mencantumkan sumber dan tahun pembuatan.\n\nPengecoh: opsi lain adalah fungsi legenda, orientasi, skala, dan judul.",
      f_layout),
    Q("Warga secara sukarela memetakan jalan, bangunan, dan fasilitas umum di daerahnya melalui platform OpenStreetMap, misalnya untuk tanggap bencana. Bentuk pengumpulan data ini disebut …",
      ["Informasi geografis sukarela (VGI)", "Survei terestris oleh lembaga negara", "Penginderaan jauh dengan satelit radar",
       "Interpolasi data curah hujan", "Generalisasi peta skala kecil"],
      "Volunteered Geographic Information (VGI) atau informasi geografis sukarela adalah data geospasial yang dibuat dan dibagikan oleh masyarakat secara sukarela, umumnya melalui platform daring dan perangkat bergerak. Contohnya OpenStreetMap, pelaporan banjir melalui media sosial, dan pemetaan partisipatif wilayah adat. VGI sangat berguna dalam tanggap bencana karena data dapat diperbarui cepat oleh banyak orang, misalnya pemetaan pascagempa Palu 2018. Tantangannya adalah menjaga kualitas dan ketelitian data.\n\nPengecoh: survei terestris dilakukan petugas resmi. Penginderaan jauh tidak melibatkan pemetaan sukarela. Interpolasi dan generalisasi adalah teknik pengolahan data.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
