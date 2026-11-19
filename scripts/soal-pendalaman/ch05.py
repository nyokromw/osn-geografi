from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_bumi(path):
    fig, ax = blank(7, 7, (-60, 60), (-60, 60))
    for r, c, n in [(50, "#C6A77B", ""), (46, "#E9A857", ""), (27, "#F6AD55", ""), (12, "#FC8181", "")]:
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#555"))
    ax.text(0, 38, "mantel", ha="center", fontsize=10); ax.text(0, 18, "lapisan X", ha="center", fontsize=11, fontweight="bold")
    ax.text(0, 0, "lapisan Y", ha="center", fontsize=10, fontweight="bold"); ax.text(0, 48, "kerak", ha="center", fontsize=8)
    ax.plot(0, 50, "*", ms=18, color="black"); ax.text(3, 52, "pusat gempa", fontsize=10)
    for a in np.radians([90 - 104, 90 + 104]):
        ax.plot([0, 50 * np.cos(a)], [50, 50 * np.sin(a)], color=C["red"], ls="--", lw=1)
    th = np.linspace(np.radians(-14), np.radians(-166), 60)
    ax.plot(55 * np.cos(th), 55 * np.sin(th), color=C["red"], lw=5, alpha=0.6)
    ax.text(0, -58, "zona tidak menerima gelombang S langsung (104°–180°)", ha="center", fontsize=10, color=C["red"])
    ax.set_title("Penampang Bumi dan zona bayangan gelombang S")
    save(fig, path)


def f_magnet(path):
    fig, ax = blank(10, 4.2, (-110, 110), (0, 50))
    edges = [0, 15, 30, 55, 75, 100]
    for i in range(len(edges) - 1):
        col = "#2D3748" if i % 2 == 0 else "white"
        for s in [1, -1]:
            x0, x1 = s * edges[i], s * edges[i + 1]
            ax.add_patch(Rectangle((min(x0, x1), 10), abs(x1 - x0), 28, fc=col, ec="#2D3748", lw=0.8))
    ax.plot([0, 0], [6, 44], color=C["red"], lw=2.5); ax.text(0, 46, "punggungan tengah samudra", ha="center", fontsize=10, color=C["red"])
    for x, t in [(55, "3 juta th"), (100, "5 juta th"), (-100, "5 juta th")]:
        ax.annotate(t, (x, 10), xytext=(x, 3), ha="center", fontsize=9, arrowprops=dict(arrowstyle="-", lw=0.8))
    ax.annotate("", xy=(100, 41), xytext=(0, 41), arrowprops=dict(arrowstyle="<->", lw=1.2)); ax.text(50, 42.5, "100 km", ha="center", fontsize=10)
    ax.text(-105, 30, "hitam = polaritas normal\nputih = polaritas terbalik", fontsize=8.5)
    ax.set_title("Pola anomali magnetik dasar samudra dan umur batuan")
    save(fig, path)


def f_siklus_batuan(path):
    fig, ax = blank(8.5, 6, (0, 100), (0, 70))
    pos = {"Magma": (50, 60), "Batuan beku": (15, 35), "Sedimen lepas": (85, 35), "Batuan sedimen": (70, 8), "Batuan metamorf": (30, 8)}
    for n, (x, y) in pos.items():
        box(ax, x - 11, y - 4, 22, 8, n, fc="#EBF8FF", fs=10)
    for (a, b, lab, off) in [("Magma", "Batuan beku", "1", (-3, 2)), ("Batuan beku", "Sedimen lepas", "2", (0, 3)),
                              ("Sedimen lepas", "Batuan sedimen", "3", (4, 0)), ("Batuan sedimen", "Batuan metamorf", "4", (0, -4)),
                              ("Batuan metamorf", "Magma", "5", (-3, 0))]:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        arrow(ax, x0 + (x1 - x0) * 0.25, y0 + (y1 - y0) * 0.25, x0 + (x1 - x0) * 0.72, y0 + (y1 - y0) * 0.72, color=C["gray"])
        ax.text((x0 + x1) / 2 + off[0], (y0 + y1) / 2 + off[1], lab, fontsize=14, fontweight="bold", color=C["red"])
    ax.set_title("Siklus batuan (disederhanakan)")
    save(fig, path)


def f_strati(path):
    fig, ax = blank(8.5, 5.4, (0, 100), (0, 60))
    cols = ["#D69E2E", "#A0AEC0", "#F6E05E", "#9C4221"]
    for i, c in enumerate(cols):
        ax.add_patch(Rectangle((0, i * 10), 100, 10, fc=c, ec="black"))
        ax.text(3, i * 10 + 5, ["L1", "L2", "L3", "L4"][i], fontsize=12, fontweight="bold", va="center")
    ax.add_patch(Polygon([(55, 0), (63, 0), (60, 40), (53, 40)], fc="#E53E3E", ec="black")); ax.text(66, 20, "K (intrusi\nbatuan beku)", fontsize=10)
    ax.plot([0, 100], [40, 40], color="black", lw=2.5)
    xs = np.linspace(0, 100, 50); top = 40 + 1.5 * np.sin(xs / 7)
    ax.fill_between(xs, 40, 50, color="#68D391", ec="black"); ax.text(3, 45, "L5", fontsize=12, fontweight="bold", va="center")
    ax.text(70, 41.5, "bidang erosi", fontsize=9)
    ax.set_title("Penampang stratigrafi sebuah tebing")
    save(fig, path)


def f_sesar(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.6))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 8); a.axis("off"); a.set_aspect("equal")
    # X normal: hanging wall down
    for a, dy, title in [(axs[0], -1.2, "X"), (axs[1], 1.2, "Y")]:
        a.add_patch(Polygon([(0, 0), (4, 0), (6, 5), (0, 5)], fc="#F6E05E", ec="black"))
        a.add_patch(Polygon([(4, 0 + dy), (10, 0 + dy), (10, 5 + dy), (6, 5 + dy)], fc="#ED8936", ec="black"))
        a.plot([3.5, 6.5], [-0.5, 6.5], color=C["red"], lw=2)
        arrow(a, 1.5, 6.6, 0.3, 6.6, ms=12) if dy < 0 else arrow(a, 0.3, 6.6, 1.5, 6.6, ms=12)
        arrow(a, 8.5, 6.6 + dy, 9.7, 6.6 + dy, ms=12) if dy < 0 else arrow(a, 9.7, 6.6 + dy, 8.5, 6.6 + dy, ms=12)
        a.set_title(title, fontsize=14, fontweight="bold")
    a = axs[2]
    a.add_patch(Rectangle((0.5, 1), 4.3, 6, fc="#F6E05E", ec="black")); a.add_patch(Rectangle((5.2, 1), 4.3, 6, fc="#ED8936", ec="black"))
    a.plot([5, 5], [0.5, 7.5], color=C["red"], lw=2)
    arrow(a, 2.6, 2, 2.6, 6, ms=12); arrow(a, 7.4, 6, 7.4, 2, ms=12)
    a.set_title("Z (tampak atas)", fontsize=14, fontweight="bold")
    fig.suptitle("Tiga jenis sesar (panah = arah gaya / gerak blok)", fontweight="bold")
    save(fig, path)


def f_hjul(path):
    d = np.array([0.001, 0.01, 0.1, 0.5, 1, 10, 100])
    ero = np.array([150, 60, 25, 20, 25, 90, 300])
    dep = np.array([0.02, 0.15, 1.2, 5, 9, 60, 200])
    fig, ax = new(8.5, 5)
    ax.plot(d, ero, color=C["red"], lw=2.4, label="kecepatan mulai erosi")
    ax.plot(d, dep, color=C["blue"], lw=2.4, label="kecepatan mulai pengendapan")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.text(0.003, 400, "EROSI", fontsize=12, fontweight="bold", color=C["red"])
    ax.text(0.003, 3, "TRANSPORTASI", fontsize=12, fontweight="bold", color=C["gray"])
    ax.text(5, 1, "PENGENDAPAN", fontsize=12, fontweight="bold", color=C["blue"])
    for n, x in [("lempung", 0.002), ("pasir", 0.5), ("kerikil", 20)]:
        ax.axvline(x, color="#A0AEC0", ls=":"); ax.text(x, 0.012, n, ha="center", fontsize=9, rotation=90, va="bottom")
    ax.set_xlabel("Ukuran butir (mm, skala log)"); ax.set_ylabel("Kecepatan arus (cm/s, skala log)")
    ax.set_ylim(0.01, 1000); ax.legend(loc="lower right", frameon=False)
    ax.set_title("Kurva Hjulström (disederhanakan)")
    save(fig, path)


def f_kontur_ab(path):
    fig, ax = blank(8.5, 4.6, (0, 100), (0, 50))
    for i, h in enumerate([500, 562.5, 625, 687.5, 750]):
        x = 15 + i * 17.5
        ax.plot([x - 3, x + 2, x - 2, x + 3], [46, 32, 18, 4], color="#8B5A2B", lw=1.6 if h in (500, 750) else 0.9)
        ax.text(x - 1, 47.5, f"{h:g}".replace(".", ","), fontsize=9, ha="center")
    ax.plot(16, 25, "o", color=C["red"]); ax.text(10, 26, "A", fontsize=14, fontweight="bold")
    ax.plot(86, 25, "o", color=C["red"]); ax.text(88, 26, "B", fontsize=14, fontweight="bold")
    ax.annotate("", xy=(85.5, 21), xytext=(16.5, 21), arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.text(51, 17.5, "jarak di peta A–B = 4 cm", ha="center", fontsize=10, bbox=dict(fc="white", ec="none"))
    ax.text(50, 2, "Skala 1 : 25.000 · interval kontur 62,5 m (garis tebal setiap 250 m)", ha="center", fontsize=9)
    ax.set_title("Potongan peta topografi")
    save(fig, path)


# ---- paket 1
def f_batas3(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 6); a.axis("off")
    a = axs[0]
    a.add_patch(Rectangle((0, 2.5), 4.7, 1.2, fc="#4A5568")); a.add_patch(Rectangle((5.3, 2.5), 4.7, 1.2, fc="#4A5568"))
    arrow(a, 4, 4.4, 1.5, 4.4, ms=12); arrow(a, 6, 4.4, 8.5, 4.4, ms=12)
    a.add_patch(Polygon([(4.7, 2.5), (5.3, 2.5), (5.5, 0.5), (4.5, 0.5)], fc="#FC8181")); a.set_title("Penampang 1")
    a = axs[1]
    a.add_patch(Polygon([(0, 3.4), (5.5, 3.4), (8.5, 0.6), (8, 0.3), (5.2, 2.6), (0, 2.6)], fc="#4A5568"))
    a.add_patch(Polygon([(5.3, 3.4), (10, 3.4), (10, 4.8), (6.5, 4.8)], fc="#C6A77B"))
    a.add_patch(Polygon([(7.3, 4.8), (7.8, 5.8), (8.3, 4.8)], fc="#9C4221"))
    arrow(a, 1, 4.1, 3.5, 4.1, ms=12); a.set_title("Penampang 2")
    a = axs[2]
    a.add_patch(Rectangle((0.5, 0.5), 4.3, 5, fc="#A0AEC0", ec="black")); a.add_patch(Rectangle((5.2, 0.5), 4.3, 5, fc="#CBD5E0", ec="black"))
    arrow(a, 2.6, 1.5, 2.6, 4.5, ms=12); arrow(a, 7.4, 4.5, 7.4, 1.5, ms=12); a.set_title("Penampang 3 (tampak atas)")
    save(fig, path)


HAW = [("Hawaii", 0, 0.4), ("Maui", 200, 1.3), ("Oahu", 340, 3.0), ("Kauai", 520, 5.1), ("Nihoa", 780, 7.3)]


def f_hawaii(path):
    fig, ax = new(9, 3.8)
    for n, d, a in HAW:
        ax.plot(d, 0, "o", ms=14, color=C["brown"]); ax.text(d, 0.25, f"{n}\n{a:g} juta th".replace(".", ","), ha="center", fontsize=10)
    ax.annotate("", xy=(850, -0.35), xytext=(-20, -0.35), arrowprops=dict(arrowstyle="-|>", lw=1.2))
    ax.text(420, -0.55, "jarak dari titik panas di bawah Pulau Hawaii (km) → arah barat laut", ha="center", fontsize=10)
    ax.set_ylim(-0.8, 0.8); ax.set_yticks([]); ax.set_xlim(-60, 880); ax.set_xlabel("km")
    ax.set_title("Rangkaian pulau gunung api Hawaii dan umur batuannya")
    save(fig, path)


def f_silika(path):
    fig, ax = new(8.5, 4.4)
    m = ["Basal", "Andesit", "Dasit", "Riolit"]; si = [50, 60, 66, 72]
    ax.bar(m, si, color=["#2D3748", "#718096", "#A0AEC0", "#E2E8F0"], ec="black")
    for i, v in enumerate(si):
        ax.text(i, v + 1, f"{v}%", ha="center", fontsize=11, fontweight="bold")
    ax.set_ylim(40, 80); ax.set_ylabel("Kandungan SiO₂ (%)")
    ax.annotate("", xy=(3.4, 78), xytext=(-0.4, 78), arrowprops=dict(arrowstyle="-|>", lw=1.5))
    ax.text(1.5, 78.6, "viskositas dan kandungan gas meningkat", ha="center", fontsize=10)
    ax.set_title("Jenis magma menurut kandungan silika")
    save(fig, path)


def f_lipatan(path):
    fig, ax = blank(9.5, 4.6, (0, 100), (0, 50))
    x = np.linspace(0, 100, 300)
    cols = ["#9C4221", "#D69E2E", "#F6E05E", "#68D391"]
    for i in range(4):
        y0 = 4 + i * 7 + 9 * np.sin(x / 100 * 2 * np.pi * 1.5)
        ax.fill_between(x, y0, y0 + 7, color=cols[i], ec="black", lw=0.5)
    ax.text(16.5, 44, "P", fontsize=15, fontweight="bold"); ax.text(50, 21, "Q", fontsize=15, fontweight="bold", color="white")
    ax.text(97, 40, "lapisan 4 (termuda)", ha="right", fontsize=9); ax.text(97, 2, "lapisan 1 (tertua)", ha="right", fontsize=9)
    arrow(ax, 2, 25, 10, 25, color=C["red"]); arrow(ax, 98, 25, 90, 25, color=C["red"])
    ax.set_title("Penampang struktur lipatan (panah = arah gaya tekan)")
    save(fig, path)


def f_lempeng(path):
    fig, ax = indonesia_map(extent=(90, 145, -18, 12), w=10, h=5.4)
    arrow(ax, 105, -15, 107, -10.5, color=C["red"], lw=3, ms=20); ax.text(102, -16.5, "Lempeng P · ±7 cm/th", fontsize=10, fontweight="bold")
    arrow(ax, 143, 6, 136, 8, color=C["red"], lw=3, ms=20); ax.text(133, 10.5, "Lempeng Q · ±10 cm/th", fontsize=10, fontweight="bold")
    ax.text(100, 9, "Lempeng R (relatif stabil)", fontsize=10, fontweight="bold")
    ax.set_title("Gerak relatif lempeng di sekitar Indonesia")
    save(fig, path)


# ---- paket 2
def f_mohs(path):
    table([[1, "Talk"], [2, "Gipsum"], [3, "Kalsit"], [4, "Fluorit"], [5, "Apatit"], [6, "Ortoklas"], [7, "Kuarsa"],
           [8, "Topaz"], [9, "Korundum"], [10, "Intan"]], ["Kekerasan Mohs", "Mineral"], path,
          title="Skala kekerasan Mohs (kaca ±5,5; kuku ±2,5; paku baja ±6,5)", col_w=[0.4, 0.6], row_h=0.36)


def f_batuan(path):
    table([["P", "kristal besar terlihat mata, kuarsa dan feldspar"], ["Q", "berlapis, bereaksi dengan HCl, ada fosil kerang"],
           ["R", "berfoliasi, membelah menjadi lembaran tipis"], ["S", "berongga banyak, sangat ringan, mengapung di air"]],
          ["Sampel", "Ciri-ciri hasil pengamatan"], path, title="Hasil pengamatan empat sampel batuan", col_w=[0.18, 0.82])


def f_paruh(path):
    n = np.linspace(0, 4, 200)
    fig, ax = new(8.5, 4.4)
    ax.plot(n * 1.3, 100 * 0.5 ** n, color=C["blue"], lw=2.4)
    for k in range(1, 4):
        ax.plot(k * 1.3, 100 * 0.5 ** k, "o", color=C["red"]); ax.text(k * 1.3 + 0.05, 100 * 0.5 ** k + 3, f"{100 * 0.5 ** k:g}%".replace(".", ","), fontsize=10)
    ax.set_xlabel("Waktu (miliar tahun)"); ax.set_ylabel("Isotop induk tersisa (%)")
    ax.set_title("Peluruhan isotop K-40 (waktu paruh ±1,3 miliar tahun)"); ax.grid(color="#EDF2F7")
    save(fig, path)


def f_waktu(path):
    seg = [("Kambrium–Perm\n(Paleozoikum)", 541, 252, "#90CDF4"), ("Trias", 252, 201, "#B794F4"), ("Jura", 201, 145, "#9F7AEA"),
           ("Kapur", 145, 66, "#68D391"), ("Paleogen", 66, 23, "#F6AD55"), ("Neogen", 23, 2.6, "#F6E05E"), ("Kuarter", 2.6, 0, "#FEFCBF")]
    fig, ax = new(10, 3)
    for n, a, b, c in seg:
        ax.barh(0, a - b, left=-a, color=c, ec="black")
        ax.text(-(a + b) / 2, 0, n, ha="center", va="center", fontsize=8.5 if a - b > 40 else 7.5, rotation=0 if a - b > 40 else 90)
    for t in [252, 66]:
        ax.axvline(-t, color=C["red"], lw=2); ax.text(-t, 0.55, f"{t} juta th", ha="center", fontsize=9, color=C["red"])
    ax.set_yticks([]); ax.set_xlim(-560, 5); ax.set_ylim(-0.6, 0.8)
    ax.set_xticks([-500, -400, -300, -200, -100, 0]); ax.set_xticklabels(["500", "400", "300", "200", "100", "0"])
    ax.set_xlabel("juta tahun yang lalu")
    ax.set_title("Skala waktu geologi (disederhanakan)")
    save(fig, path)


def f_tekstur(path):
    bars(["Tanah K", "Tanah L", "Tanah M"], {"Pasir": [75, 30, 10], "Debu": [15, 45, 30], "Liat": [10, 25, 60]}, path,
         title="Komposisi ukuran butir tiga sampel tanah (%)", ylabel="%", stacked=True, values=True, ylim=(0, 135), legend_loc="upper center",
         colors=[C["sand"], C["yellow"], C["brown"]], w=8)


# ---- paket 3
def f_profil(path):
    x = np.linspace(0, 100, 200); y = 1200 * np.exp(-x / 25)
    fig, ax = new(9, 4.2)
    ax.plot(x, y, color=C["blue"], lw=2.6)
    for t, xx in [("K", 8), ("L", 45), ("M", 88)]:
        ax.text(xx, 1200 * np.exp(-xx / 25) + 80, t, fontsize=15, fontweight="bold", ha="center")
    ax.set_xlabel("Jarak dari mata air (km)"); ax.set_ylabel("Elevasi dasar sungai (m)")
    ax.set_title("Profil memanjang sebuah sungai")
    save(fig, path)


def f_pola(path):
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.2))
    for a in axs:
        a.set_xlim(-5, 5); a.set_ylim(-5, 5); a.set_aspect("equal"); a.axis("off")
    rnd = np.random.RandomState(1)
    def tree(a, x, y, ang, l, d):
        if d == 0: return
        x2, y2 = x + l * np.cos(ang), y + l * np.sin(ang)
        a.plot([x, x2], [y, y2], color=C["blue"], lw=d * 0.8)
        for s in [-0.5, 0.5]:
            tree(a, x2, y2, ang + s + rnd.uniform(-0.2, 0.2), l * 0.62, d - 1)
    tree(axs[0], 0, -4.5, np.pi / 2, 3.2, 5); axs[0].set_title("1")
    for i in range(12):
        t = i / 12 * 2 * np.pi; axs[1].plot([0.8 * np.cos(t), 4.6 * np.cos(t)], [0.8 * np.sin(t), 4.6 * np.sin(t)], color=C["blue"])
    axs[1].add_patch(Circle((0, 0), 0.6, fc=C["brown"])); axs[1].set_title("2")
    axs[2].plot([0, 0], [-4.8, 4.8], color=C["blue"], lw=3)
    for y in np.arange(-4, 4.5, 1.2):
        axs[2].plot([0, 3], [y, y + 0.2], color=C["blue"], lw=1.5); axs[2].plot([0, -3], [y + 0.6, y + 0.8], color=C["blue"], lw=1.5)
    axs[2].set_title("3")
    for r in [1.5, 3, 4.4]:
        axs[3].add_patch(Circle((0, 0), r, fc="none", ec=C["blue"], lw=1.5))
    for t in [0.3, 2.2, 4.1]:
        axs[3].plot([1.5 * np.cos(t), 4.4 * np.cos(t)], [1.5 * np.sin(t), 4.4 * np.sin(t)], color=C["blue"])
    axs[3].set_title("4")
    fig.suptitle("Empat pola aliran sungai", fontweight="bold")
    save(fig, path)


def f_meander(path):
    fig, ax = blank(9, 5, (0, 100), (0, 56))
    t = np.linspace(0, 1, 400); x = 100 * t; y = 28 + 16 * np.sin(t * 2 * np.pi * 1.5)
    ax.fill_between(x, y - 2.5, y + 2.5, color=C["lblue"])
    ax.plot(x, y, color=C["blue"], lw=1)
    ax.text(16, 48, "P", fontsize=14, fontweight="bold"); ax.text(16, 32, "Q", fontsize=14, fontweight="bold")
    ax.add_patch(Ellipse((16.5, 36), 9, 6, fc=C["sand"], ec="none", zorder=0.5))
    ax.text(50, 18.5, "R", fontsize=14, fontweight="bold")
    ax.add_patch(Ellipse((50, 20), 9, 6, fc=C["sand"], ec="none", zorder=0.5))
    arrow(ax, 2, 30, 8, 37, color=C["gray"], lw=1.2); ax.text(1, 24, "arah aliran", fontsize=9)
    ax.set_title("Kenampakan sebuah sungai bermeander (tampak atas)")
    save(fig, path)


def f_karst2(path):
    fig, ax = blank(10, 5, (0, 100), (0, 54))
    xs = np.linspace(0, 100, 400)
    top = 34 + 9 * np.clip(np.sin(xs / 4.5), 0, None)
    top = np.where((xs > 22) & (xs < 30), 32 - 5 * np.sin((xs - 22) / 8 * np.pi), top)
    ax.fill_between(xs, 0, top, color="#E2E8F0", ec="#718096")
    ax.add_patch(Ellipse((70, 18), 26, 9, fc="white", ec="#718096"))
    for xx in np.arange(60, 81, 3):
        ax.add_patch(Polygon([(xx, 22.3), (xx + 0.8, 22.3), (xx + 0.4, 19.5)], fc="#A0AEC0"))
    ax.plot([45, 45], [top[180], 18], color="#2D3748", lw=3)
    for t, (x, y) in {"K": (26, 33), "L": (47, 30), "M": (70, 13), "N": (86, 48)}.items():
        ax.text(x, y, t, fontsize=14, fontweight="bold", color=C["red"])
    ax.set_title("Penampang bentang lahan karst")
    save(fig, path)


def f_dd(path):
    table([["X", "300", "450"], ["Y", "300", "180"], ["Z", "300", "900"]],
          ["DAS", "Luas (km²)", "Panjang total sungai (km)"], path, title="Data morfometri tiga DAS", col_w=[0.2, 0.35, 0.45])


# ---- paket 4
def f_pantai(path):
    fig, ax = blank(9, 5.4, (0, 100), (0, 60))
    ax.add_patch(Rectangle((0, 0), 100, 60, fc=C["sea"]))
    ax.add_patch(Polygon([(0, 0), (0, 60), (30, 60), (34, 40), (30, 22), (36, 0)], fc=C["land"], ec="#8D7B5A"))
    ax.add_patch(Polygon([(33, 44), (60, 50), (62, 48.5), (34, 41)], fc=C["sand"], ec="#B7791F"))
    ax.add_patch(Circle((78, 18), 7, fc=C["land"], ec="#8D7B5A"))
    ax.add_patch(Polygon([(33, 17), (72, 16), (72, 20), (32, 21)], fc=C["sand"], ec="#B7791F"))
    for t, (x, y) in {"P": (62, 53), "Q": (52, 23.5), "R": (78, 29), "S": (20, 6)}.items():
        ax.text(x, y, t, fontsize=14, fontweight="bold", color=C["red"])
    arrow(ax, 20, 56, 32, 53, color=C["blue"]); ax.text(10, 57, "arus sejajar pantai", fontsize=9, color=C["blue"])
    ax.set_title("Bentuk lahan hasil pengendapan marin")
    save(fig, path)


def f_geomap(path):
    fig, ax = blank(8.5, 4.8, (0, 100), (0, 56))
    bands = [("Ta", "#90CDF4", 0, 20), ("Tb", "#F6E05E", 20, 38), ("Tc", "#68D391", 38, 62), ("Tb", "#F6E05E", 62, 80), ("Ta", "#90CDF4", 80, 100)]
    for n, c, a, b in bands:
        ax.add_patch(Rectangle((a, 6), b - a, 44, fc=c, ec="black")); ax.text((a + b) / 2, 28, n, ha="center", fontsize=14, fontweight="bold")
    for x, s in [(15, "⟵ 30°"), (30, "⟵ 25°"), (70, "25° ⟶"), (85, "30° ⟶")]:
        pass
    for x, d in [(14, -1), (29, -1), (71, 1), (86, 1)]:
        ax.plot([x, x], [40, 46], color="black", lw=2); ax.plot([x, x - 3 * d], [43, 43], color="black", lw=2)
    ax.text(50, 2, "Keterangan umur: Ta = Eosen (tertua), Tb = Oligosen, Tc = Miosen (termuda). Simbol ⊤ menunjukkan arah kemiringan lapisan.", ha="center", fontsize=8.5)
    ax.set_title("Peta geologi sederhana sebuah daerah")
    save(fig, path)


def f_barchan(path):
    fig, ax = blank(8, 5, (0, 100), (0, 60))
    ax.add_patch(Rectangle((0, 0), 100, 60, fc="#FEFCBF"))
    th = np.linspace(-np.pi / 2, np.pi / 2, 100)
    outer = np.c_[50 - 22 * np.cos(th) * 0.9 + 25 * (np.abs(np.sin(th)) ** 3), 30 + 22 * np.sin(th)]
    inner = np.c_[50 - 12 * np.cos(th) + 25 * (np.abs(np.sin(th)) ** 3) + 8, 30 + 18 * np.sin(th)]
    poly = np.r_[outer, inner[::-1]]
    ax.add_patch(Polygon(poly, fc="#D69E2E", ec="#975A16"))
    ax.text(30, 30, "lereng landai", fontsize=9, ha="center"); ax.text(66, 30, "lereng curam\n(slip face)", fontsize=9, ha="center")
    ax.text(80, 50, "tanduk", fontsize=9); ax.text(80, 9, "tanduk", fontsize=9)
    north_arrow(ax, 0.93, 0.9)
    ax.set_title("Bentuk sebuah gumuk pasir (tampak atas)")
    save(fig, path)


def f_kontur4(path):
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.2))
    for a in axs:
        a.set_xlim(-5, 5); a.set_ylim(-5, 5); a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
    for r, h in zip([4, 2.8, 1.6, 0.6], [100, 200, 300, 400]):
        axs[0].add_patch(Circle((0, 0), r, fc="none", ec=C["brown"])); axs[0].text(r - 0.3, 0, str(h), fontsize=7)
    for i, h in enumerate([100, 200, 300, 400]):
        k = -1.5 + i * 2
        axs[1].plot([-4.5, 0, 4.5], [k - 3, k, k - 3], color=C["brown"]); axs[1].text(3.6, k - 2.6, str(h), fontsize=7)
    axs[1].plot([0, 0], [-5, 5], color=C["blue"], lw=1)
    for i, h in enumerate([400, 300, 200, 100]):
        k = 1.5 - i * 2
        axs[2].plot([-4.5, 0, 4.5], [k + 3, k, k + 3], color=C["brown"]); axs[2].text(3.6, k + 2.6, str(h), fontsize=7)
    for r in [4, 2.8, 1.6]:
        axs[3].add_patch(Circle((0, 0), r, fc="none", ec=C["brown"]))
        for t in np.linspace(0, 2 * np.pi, 14, endpoint=False):
            axs[3].plot([r * np.cos(t), (r - 0.35) * np.cos(t)], [r * np.sin(t), (r - 0.35) * np.sin(t)], color=C["brown"], lw=0.8)
    for i, a in enumerate(axs):
        a.set_title(str(i + 1))
    fig.suptitle("Empat pola garis kontur (angka = elevasi, m)", fontweight="bold")
    save(fig, path)


def f_tebing(path):
    lines([1990, 2000, 2010, 2020], {"Posisi tebing (m dari patok 1990)": [0, -18, -40, -66]}, path,
          title="Mundurnya tebing pantai di Tanjung T", xlabel="Tahun", ylabel="m (negatif = mundur ke darat)", w=8)


# ---- paket 5
def f_kelas(path):
    table([["I", "0–3%", "tanpa hambatan berarti"], ["II", "3–8%", "hambatan ringan"], ["III", "8–15%", "hambatan sedang"],
           ["IV", "15–30%", "hambatan berat; tanaman semusim terbatas"], ["VI", "30–45%", "tidak sesuai tanaman semusim; padang rumput, hutan produksi"],
           ["VII", "45–65%", "hambatan sangat berat; hutan produksi terbatas"], ["VIII", "> 65%", "kawasan lindung/cagar alam"]],
          ["Kelas", "Lereng", "Keterangan utama"], path, title="Kelas kemampuan lahan berdasarkan kemiringan lereng (disederhanakan)",
          col_w=[0.12, 0.15, 0.73], fs=10.5, w=9)


def f_matriks(path):
    table([["Hutan", "8.200", "1.300", "300", "200"], ["Kebun campur", "0", "4.100", "500", "400"],
           ["Sawah", "0", "200", "5.600", "1.200"], ["Permukiman", "0", "0", "0", "3.000"]],
          ["2010 \\ 2020", "Hutan", "Kebun campur", "Sawah", "Permukiman"], path,
          title="Matriks perubahan penggunaan lahan Kabupaten L, 2010–2020 (ha)", col_w=[0.24, 0.19, 0.19, 0.19, 0.19])


def f_pie2(path):
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    lab = ["Sawah", "Permukiman", "Hutan", "Lainnya"]; cols = [C["yellow"], C["red"], C["green"], C["lgray"]]
    for a, d, t in zip(axs, [[40, 15, 30, 15], [28, 30, 27, 15]], ["2005", "2025"]):
        a.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=cols, startangle=90, wedgeprops=dict(ec="white"))
        a.set_title(f"Kabupaten B, {t} (luas 1.000 km²)")
    save(fig, path)


def f_lereng(path):
    fig, ax = blank(8, 4.2, (0, 100), (0, 46))
    for i, h in enumerate([300, 312.5, 325, 337.5, 350]):
        x = 20 + i * 15
        ax.plot([x, x + 3, x - 1, x + 2], [42, 30, 16, 4], color="#8B5A2B", lw=1.2)
        ax.text(x, 43.5, f"{h:g}".replace(".", ","), ha="center", fontsize=9)
    ax.annotate("", xy=(51, 24), xytext=(36, 24), arrowprops=dict(arrowstyle="<->", lw=1.2))
    ax.text(43.5, 26, "3 mm", ha="center", fontsize=10, bbox=dict(fc="white", ec="none"))
    ax.text(50, 1, "Skala peta 1 : 25.000 · interval kontur 12,5 m · jarak rata-rata antarkontur 3 mm", ha="center", fontsize=9)
    ax.set_title("Potongan peta kontur lereng S")
    save(fig, path)


def f_ndvi(path):
    t = np.arange(2015, 2025, 0.25)
    v = np.where(t < 2019, 0.82, np.where(t < 2019.5, 0.15, 0.15 + 0.08 * (t - 2019.5)))
    lines(t, {"NDVI": v}, path, title="NDVI rata-rata sebuah petak lahan dari citra satelit", xlabel="Tahun", ylabel="NDVI",
          markers=False, ylim=(-0.1, 1.0), w=9)


# ============================ questions ============================
P0 = [
    Q("Perhatikan penampang Bumi dan zona bayangan gelombang S berikut.\n\nGelombang S tidak diterima secara langsung oleh stasiun pada jarak 104°–180° dari pusat gempa. Kesimpulan yang paling tepat adalah …",
      ["Lapisan X (inti luar) berwujud cair karena gelombang S tidak merambat di zat cair",
       "Lapisan X (inti luar) berwujud padat karena gelombang S dipantulkan seluruhnya",
       "Mantel berwujud cair sehingga gelombang S terserap sebelum mencapai inti",
       "Lapisan Y (inti dalam) berwujud gas sehingga semua gelombang seismik berhenti",
       "Kerak bumi terlalu tipis sehingga gelombang S tidak dapat dicatat seismograf"],
      "Gelombang S (gelombang sekunder/transversal) hanya dapat merambat melalui zat padat karena zat cair tidak memiliki kekuatan geser. Zona bayangan gelombang S yang sangat luas (104°–180°) menunjukkan bahwa gelombang S terhenti ketika mencapai lapisan X, yaitu inti luar. Inilah bukti utama bahwa inti luar Bumi berwujud cair (besi-nikel cair). Aliran besi cair di inti luar juga menjadi sumber medan magnet Bumi (efek dinamo).\n\nPengecoh: inti luar bukan padat. Mantel bersifat padat plastis, sehingga gelombang S masih dapat melewatinya. Inti dalam (Y) justru padat karena tekanan sangat tinggi, bukan gas. Ketebalan kerak tidak menjelaskan zona bayangan yang luas.",
      f_bumi),
    Q("Perhatikan pola anomali magnetik dasar samudra berikut. Batuan berumur 5 juta tahun ditemukan 100 km di kedua sisi punggungan.\n\nLaju pemekaran total dasar samudra di punggungan tersebut adalah …",
      ["4 cm per tahun", "2 cm per tahun", "20 cm per tahun", "0,2 cm per tahun", "10 cm per tahun"],
      "Laju pada satu sisi = jarak ÷ umur = 100 km ÷ 5 juta tahun = 20 km per juta tahun.\nUbah satuan: 20 km = 2.000.000 cm, sehingga 2.000.000 cm ÷ 1.000.000 tahun = 2 cm per tahun.\nKarena batuan seumur ditemukan di kedua sisi, laju pemekaran total (kedua lempeng saling menjauh) = 2 × 2 = 4 cm per tahun.\nPola garis magnet yang simetris terhadap punggungan adalah bukti teori pemekaran dasar samudra: magma naik di punggungan, membeku merekam arah medan magnet saat itu, lalu terdorong menjauh.\n\nPengecoh: 2 cm/tahun adalah laju satu sisi. 20 cm dan 0,2 cm/tahun adalah kesalahan konversi satuan. 10 cm/tahun tidak sesuai perhitungan.",
      f_magnet),
    Q("Pasangan kenampakan dan jenis batas lempeng yang tepat adalah …",
      ["Laut Merah – divergen; Pegunungan Himalaya – konvergen benua–benua", "Laut Merah – konvergen; Sesar San Andreas – divergen",
       "Pegunungan Himalaya – transform; Palung Mariana – divergen", "Sesar San Andreas – konvergen; Laut Merah – transform",
       "Palung Jawa – divergen; Pegunungan Himalaya – transform"],
      "Jenis batas lempeng:\n• Divergen (saling menjauh): membentuk punggungan tengah samudra dan lembah retakan, misalnya Laut Merah dan Lembah Retakan Afrika Timur.\n• Konvergen (saling mendekat): samudra–benua membentuk palung dan busur gunung api (Palung Jawa); samudra–samudra membentuk palung dan busur kepulauan (Palung Mariana); benua–benua membentuk pegunungan lipatan tinggi tanpa subduksi berarti (Himalaya, akibat tumbukan India dan Eurasia).\n• Transform (bergeser sejajar): membentuk sesar mendatar besar, misalnya Sesar San Andreas.\nHanya opsi pertama yang seluruhnya tepat.\n\nPengecoh: opsi lain menukar jenis batas lempeng.",
      None),
    Q("Perhatikan diagram siklus batuan berikut.\n\nProses yang ditunjukkan oleh panah nomor 4 adalah …",
      ["Metamorfisme akibat tekanan dan suhu tinggi", "Pelapukan dan erosi di permukaan Bumi", "Kompaksi dan sementasi (litifikasi)",
       "Peleburan menjadi magma di kedalaman", "Pendinginan dan pembekuan magma"],
      "Panah pada siklus batuan:\n1 = pendinginan dan pembekuan magma menjadi batuan beku.\n2 = pelapukan, erosi, dan transportasi batuan beku menjadi sedimen lepas.\n3 = kompaksi dan sementasi (litifikasi) sedimen menjadi batuan sedimen.\n4 = metamorfisme, yaitu perubahan batuan sedimen akibat tekanan dan suhu tinggi tanpa melebur, menjadi batuan metamorf (misalnya batu gamping menjadi marmer, batu lempung menjadi sabak).\n5 = peleburan batuan metamorf di kedalaman menjadi magma.\n\nPengecoh: opsi lain adalah proses pada panah 1, 2, 3, dan 5. Siklus batuan menunjukkan bahwa setiap jenis batuan dapat berubah menjadi jenis lain dalam rentang waktu geologi.",
      f_siklus_batuan),
    Q("Menurut deret reaksi Bowen, mineral yang pertama kali mengkristal ketika magma basa mendingin dari suhu sangat tinggi adalah …",
      ["Olivin", "Kuarsa", "Muskovit", "Ortoklas", "Biotit"],
      "Deret reaksi Bowen menggambarkan urutan kristalisasi mineral saat magma mendingin.\n• Deret tak menerus (kiri): olivin → piroksen → amfibol → biotit.\n• Deret menerus (kanan): plagioklas kaya Ca → plagioklas kaya Na.\n• Pada suhu paling rendah: ortoklas → muskovit → kuarsa.\nOlivin mengkristal pertama pada suhu ±1.200 °C dan khas batuan ultrabasa–basa (peridotit, basal). Kuarsa mengkristal paling akhir sehingga banyak ditemukan pada batuan asam seperti granit.\nKonsekuensinya: mineral yang terbentuk pada suhu tinggi (olivin) paling mudah lapuk di permukaan, sedangkan kuarsa paling tahan pelapukan, sehingga pasir pantai umumnya didominasi kuarsa.\n\nPengecoh: kuarsa, muskovit, ortoklas, dan biotit mengkristal pada suhu yang lebih rendah.",
      None),
    Q("Perhatikan penampang stratigrafi sebuah tebing berikut.\n\nUrutan kejadian dari yang paling tua ke paling muda adalah …",
      ["L1–L4 diendapkan → intrusi K → erosi → L5 diendapkan", "Intrusi K → L1–L4 diendapkan → erosi → L5 diendapkan",
       "L1–L4 diendapkan → erosi → L5 diendapkan → intrusi K", "L5 diendapkan → erosi → L1–L4 diendapkan → intrusi K",
       "L1–L4 diendapkan → L5 diendapkan → intrusi K → erosi"],
      "Gunakan prinsip stratigrafi:\n• Superposisi: pada lapisan yang belum terganggu, lapisan bawah lebih tua (L1 tertua, lalu L2, L3, L4).\n• Hubungan potong-memotong: batuan yang memotong lebih muda daripada yang dipotong. Intrusi K memotong L1–L4, sehingga K lebih muda dari L4.\n• K terpancung oleh bidang erosi dan tidak menembus L5, sehingga K lebih tua dari bidang erosi dan L5.\nUrutannya: L1–L4 diendapkan → intrusi K → erosi (ketidakselarasan) → L5 diendapkan.\n\nPengecoh: K tidak mungkin lebih tua dari L1–L4 karena memotongnya. K juga tidak mungkin lebih muda dari L5 karena tidak menembusnya. L5 berada paling atas sehingga paling muda.",
      f_strati),
    Q("Sebuah fosil kayu mengandung C-14 tinggal 25% dari jumlah awalnya. Jika waktu paruh C-14 sekitar 5.730 tahun, umur fosil tersebut adalah sekitar …",
      ["11.460 tahun", "5.730 tahun", "17.190 tahun", "1.433 tahun", "22.920 tahun"],
      "Setiap satu waktu paruh, jumlah isotop induk tinggal setengahnya: 100% → 50% (1 waktu paruh) → 25% (2 waktu paruh).\nSisa 25% berarti telah berlalu 2 waktu paruh: 2 × 5.730 = 11.460 tahun.\nPenanggalan C-14 dipakai untuk bahan organik berumur hingga ±50.000 tahun, misalnya arang, tulang, dan kayu di situs arkeologi. Untuk batuan berumur jutaan tahun digunakan isotop dengan waktu paruh panjang seperti K-40 atau U-238.\n\nPengecoh: 5.730 tahun berlaku bila sisa 50%. 17.190 tahun berlaku bila sisa 12,5% (3 waktu paruh). 22.920 tahun berlaku bila sisa 6,25%. 1.433 tahun muncul bila 5.730 dibagi 4, kesalahan operasi.",
      None),
    Q("Perhatikan tiga jenis sesar berikut.\n\nSesar yang terbentuk akibat gaya tarik (tensional) dan dapat membentuk struktur graben–horst adalah …",
      ["X, sesar normal", "Y, sesar naik", "Z, sesar mendatar", "Y, sesar normal", "X, sesar naik"],
      "• Sesar X: kedua blok ditarik saling menjauh, dan blok di atas bidang sesar (hanging wall) turun relatif terhadap blok di bawahnya. Inilah sesar normal (sesar turun) akibat gaya tarik. Kombinasi beberapa sesar normal membentuk graben (blok turun, misalnya Danau Toba bagian tertentu, Lembah Rift) dan horst (blok naik).\n• Sesar Y: kedua blok saling ditekan, dan hanging wall naik. Inilah sesar naik akibat gaya tekan, misalnya sesar naik belakang busur Flores.\n• Sesar Z: blok bergeser mendatar sejajar bidang sesar, misalnya Sesar Sumatra dan Palu-Koro.\n\nPengecoh: sesar naik dan sesar mendatar tidak terbentuk oleh gaya tarik. Opsi \"Y, sesar normal\" dan \"X, sesar naik\" salah menamai sesar.",
      f_sesar),
    Q("Perhatikan kurva Hjulström berikut.\n\nPenjelasan yang paling tepat mengapa butir lempung memerlukan kecepatan arus lebih tinggi untuk mulai tererosi dibandingkan butir pasir adalah …",
      ["Butir lempung bersifat kohesif sehingga saling melekat dan sulit diangkat arus", "Butir lempung lebih berat daripada pasir sehingga memerlukan energi lebih besar",
       "Butir lempung selalu terendap di dasar sungai karena tidak dapat diangkut arus", "Butir lempung hanya dapat diangkut oleh angin, bukan oleh aliran air",
       "Kurva menunjukkan lempung lebih mudah tererosi daripada pasir pada arus lemah"],
      "Pada kurva Hjulström, kecepatan minimum untuk mengerosi pasir (±0,5 mm) sekitar 20 cm/s, sedangkan lempung (±0,002 mm) memerlukan lebih dari 100 cm/s. Partikel lempung sangat halus dan bermuatan listrik sehingga saling melekat (kohesif), dan permukaan dasar berlempung juga lebih halus. Akibatnya diperlukan arus kuat untuk melepaskannya. Namun setelah terangkat, lempung dapat terbawa sebagai suspensi pada arus sangat lemah karena kecepatan pengendapannya sangat kecil.\n\nPengecoh: lempung lebih ringan, bukan lebih berat. Lempung dapat diangkut air dalam jumlah besar (penyebab air sungai keruh). Kurva menunjukkan lempung lebih sulit, bukan lebih mudah, tererosi.",
      f_hjul),
    Q("Perhatikan potongan peta topografi berikut. Kemiringan lereng antara titik A dan B adalah …",
      ["25%", "6,25%", "2,5%", "250%", "12,5%"],
      "1) Beda tinggi: A berada pada kontur 500 m dan B pada kontur 750 m, sehingga Δh = 250 m.\n2) Jarak horizontal sebenarnya = jarak peta × penyebut skala = 4 cm × 25.000 = 100.000 cm = 1.000 m.\n3) Kemiringan lereng = (Δh ÷ jarak horizontal) × 100% = (250 ÷ 1.000) × 100% = 25%.\n\nPengecoh: 6,25% memakai satu interval kontur (62,5 m) sebagai beda tinggi. 2,5% dan 250% adalah kesalahan konversi satuan (cm ke m). 12,5% memakai setengah beda tinggi. Lereng 25% (±14°) tergolong agak curam hingga curam dan perlu konservasi tanah bila diolah.",
      f_kontur_ab),
]

P1 = [
    Q("Perhatikan tiga penampang batas lempeng berikut.\n\nPenampang yang menggambarkan batas lempeng di selatan Sumatra dan Jawa beserta kenampakannya adalah …",
      ["Penampang 2; subduksi samudra–benua yang membentuk palung dan gunung api", "Penampang 1; divergen yang membentuk punggungan tengah samudra",
       "Penampang 3; transform yang membentuk sesar mendatar di dasar samudra", "Penampang 1; konvergen benua–benua yang membentuk pegunungan lipatan",
       "Penampang 2; divergen yang membentuk lembah retakan di daratan"],
      "• Penampang 1: dua lempeng bergerak saling menjauh dan magma naik di tengahnya (divergen), membentuk punggungan tengah samudra.\n• Penampang 2: lempeng samudra (gelap, lebih rapat) menunjam di bawah lempeng benua, dan di atasnya terbentuk gunung api (konvergen subduksi samudra–benua).\n• Penampang 3: dua lempeng bergeser sejajar (transform).\nDi selatan Sumatra dan Jawa, Lempeng Indo-Australia (samudra) menunjam di bawah Lempeng Eurasia (benua), membentuk Palung Sunda, busur gunung api (Bukit Barisan, gunung api Jawa), dan zona gempa megathrust. Jadi penampang 2 yang tepat.\n\nPengecoh: penampang 1 dan 3 bukan subduksi. Penampang 2 bukan divergen. Konvergen benua–benua tidak sesuai dengan kondisi Sumatra–Jawa.",
      f_batas3),
    Q("Rangkaian Kepulauan Hawaii terbentuk di atas titik panas (hotspot). Umur pulau-pulaunya semakin tua ke arah barat laut. Kesimpulan yang tepat adalah …",
      ["Lempeng Pasifik bergerak ke barat laut di atas titik panas yang relatif diam", "Titik panas bergerak ke barat laut sedangkan lempeng Pasifik diam",
       "Lempeng Pasifik bergerak ke tenggara sehingga pulau tertua berada di tenggara", "Pulau-pulau terbentuk di batas lempeng konvergen yang bergerak ke barat",
       "Umur pulau tidak berhubungan dengan gerak lempeng karena semua erupsi serentak"],
      "Titik panas adalah gumpalan material mantel panas (mantle plume) yang relatif diam terhadap lempeng di atasnya. Ketika lempeng bergerak, gunung api yang terbentuk di atas titik panas terbawa menjauh dan menjadi tidak aktif, sedangkan gunung api baru terbentuk di atas titik panas. Hasilnya adalah rangkaian pulau yang umurnya semakin tua menjauhi titik panas. Karena pulau tertua berada di barat laut dan pulau termuda (Pulau Hawaii, masih aktif) di tenggara, Lempeng Pasifik bergerak ke arah barat laut.\n\nPengecoh: titik panas relatif diam, bukan lempeng. Pulau tertua di barat laut, bukan tenggara. Hawaii berada di tengah lempeng, bukan di batas lempeng. Umur yang berbeda menunjukkan erupsi tidak serentak.",
      None),
    Q("Perhatikan rangkaian pulau gunung api Hawaii dan umur batuannya berikut.\n\nBerdasarkan data Pulau Kauai, laju gerak Lempeng Pasifik di atas titik panas adalah sekitar …",
      ["10 cm per tahun", "1 cm per tahun", "100 cm per tahun", "5 cm per tahun", "0,1 cm per tahun"],
      "Pulau Kauai berjarak ±520 km dari titik panas dan berumur ±5,1 juta tahun.\nLaju = 520 km ÷ 5,1 juta tahun ≈ 102 km per juta tahun.\nUbah satuan: 1 km per juta tahun = 100.000 cm ÷ 1.000.000 tahun = 0,1 cm per tahun. Jadi 102 km per juta tahun ≈ 10 cm per tahun.\nPerhitungan dengan pulau lain menghasilkan nilai serupa (misalnya Nihoa: 780 ÷ 7,3 ≈ 107 km per juta tahun ≈ 10,7 cm/tahun), sehingga Lempeng Pasifik termasuk lempeng yang bergerak relatif cepat.\n\nPengecoh: 1 cm, 100 cm, dan 0,1 cm per tahun adalah kesalahan konversi satuan. 5 cm per tahun muncul bila jarak dibagi dua.",
      f_hawaii),
    Q("Setelah lapisan es tebal yang menutupi Skandinavia mencair sejak akhir zaman es, daratan di wilayah itu terus terangkat hingga sekarang. Konsep yang menjelaskan gejala tersebut adalah …",
      ["Isostasi, yaitu penyesuaian keseimbangan kerak di atas mantel", "Subduksi, yaitu penunjaman lempeng samudra ke bawah lempeng benua",
       "Pemekaran dasar samudra di bawah daratan Skandinavia", "Sedimentasi yang menambah ketebalan daratan setiap tahun",
       "Gempa vulkanik yang mengangkat kerak secara tiba-tiba"],
      "Isostasi adalah keadaan keseimbangan ketika kerak bumi yang lebih ringan \"mengapung\" di atas mantel yang lebih rapat dan bersifat plastis, mirip balok kayu di atas air. Saat zaman es, beban lapisan es setebal 2–3 km menekan kerak Skandinavia sehingga turun. Setelah es mencair, beban hilang dan kerak perlahan terangkat kembali (pantulan pascaglasial) hingga beberapa milimeter per tahun, dan proses ini masih berlangsung.\n\nPengecoh: subduksi dan pemekaran dasar samudra adalah proses tektonik lempeng di batas lempeng, bukan respons terhadap hilangnya beban es. Sedimentasi justru menambah beban. Pengangkatan ini berlangsung perlahan, bukan tiba-tiba akibat gempa vulkanik.",
      None),
    Q("Perhatikan grafik jenis magma menurut kandungan silika berikut.\n\nJenis magma yang paling mungkin menghasilkan erupsi sangat eksplosif seperti letusan Toba sekitar 74.000 tahun lalu adalah …",
      ["Riolit, karena kandungan silika dan gas tinggi membuat magma sangat kental", "Basal, karena kandungan silika rendah membuat magma encer dan meledak",
       "Andesit, karena kandungan silikanya paling rendah di antara keempatnya", "Basal, karena gas mudah terperangkap di dalam magma yang encer",
       "Dasit, karena kandungan silikanya paling tinggi di antara keempatnya"],
      "Kandungan silika (SiO₂) menentukan kekentalan (viskositas) magma: semakin tinggi silika, semakin kental magma. Magma kental menahan gas terlarut sehingga tekanan menumpuk, lalu dilepaskan secara tiba-tiba dalam letusan eksplosif. Grafik menunjukkan riolit memiliki silika tertinggi (±72%). Letusan supervolcano Toba menghasilkan endapan tuf riolitik dalam volume sangat besar dan membentuk kaldera Danau Toba.\n\nPengecoh: basal (±50%) encer sehingga gas mudah lepas dan erupsinya cenderung efusif (lelehan lava), seperti di Hawaii. Andesit tidak memiliki silika terendah. Dasit bukan yang tertinggi pada grafik.",
      f_silika),
    Q("Peristiwa tahun 1979 di Dieng, ketika ratusan warga meninggal akibat gas yang terkumpul di lembah sekitar kawah, disebabkan oleh gejala pascavulkanik berupa …",
      ["Mofet, yaitu semburan gas CO₂ yang lebih berat dari udara", "Solfatara, yaitu semburan gas belerang yang berbau tajam",
       "Fumarol, yaitu semburan uap air panas dari celah batuan", "Geiser, yaitu semburan air panas yang muncul secara berkala",
       "Sumber air panas yang mengandung belerang untuk pengobatan"],
      "Gejala pascavulkanik meliputi:\n• Fumarol: semburan uap air panas.\n• Solfatara: semburan gas belerang (H₂S, SO₂) yang berbau tajam.\n• Mofet: semburan gas karbon dioksida (CO₂) dan gas lain. CO₂ tidak berbau dan lebih berat daripada udara, sehingga dapat terkumpul di lembah atau cekungan dan menggantikan oksigen. Orang yang memasukinya dapat kehilangan kesadaran dan meninggal karena sesak napas.\n• Geiser: semburan air panas berkala.\nPada tragedi Kawah Sinila–Timbang di Dieng tahun 1979, gas CO₂ yang keluar bersama letusan freatik mengalir ke lembah dan menewaskan sekitar 149 orang.\n\nPengecoh: solfatara dan fumarol tidak menjelaskan gas tak berbau yang menumpuk di lembah. Geiser dan sumber air panas tidak menyebabkan korban massal semacam ini.",
      None),
    Q("Perhatikan penampang struktur lipatan berikut.\n\nPernyataan yang tepat mengenai bagian Q adalah …",
      ["Q adalah sinklin; lapisan termuda berada di bagian intinya", "Q adalah antiklin; lapisan tertua berada di bagian intinya",
       "Q adalah sinklin; lapisan tertua berada di bagian intinya", "Q adalah sesar naik akibat gaya tarik dari dua arah",
       "Q adalah antiklin; terbentuk karena gaya tarik yang menjauhkan lapisan"],
      "Lipatan terbentuk akibat gaya tekan (kompresi) dari samping yang melengkungkan lapisan batuan.\n• Bagian P (puncak lipatan yang melengkung ke atas) disebut antiklin; pada antiklin yang tererosi, lapisan tertua tersingkap di intinya.\n• Bagian Q (lembah lipatan yang melengkung ke bawah) disebut sinklin; lapisan termuda berada di bagian intinya.\nDi Indonesia, perbukitan lipatan banyak ditemukan di zona Kendeng dan Rembang (Jawa) serta cekungan minyak di Sumatra dan Kalimantan.\n\nPengecoh: Q bukan antiklin. Inti sinklin berisi lapisan termuda, bukan tertua. Gambar menunjukkan lipatan, bukan sesar. Lipatan terbentuk oleh gaya tekan, bukan gaya tarik.",
      f_lipatan),
    Q("Gempa Palu 2018 dipicu oleh pergerakan Sesar Palu-Koro yang membelah Kota Palu dari utara ke selatan. Jenis sesar tersebut adalah …",
      ["Sesar mendatar, karena blok bergeser sejajar bidang sesar secara horizontal", "Sesar naik, karena salah satu blok terdorong naik di atas blok lain",
       "Sesar normal, karena kedua blok ditarik menjauh dan membentuk graben", "Zona subduksi, karena lempeng samudra menunjam di bawah Kota Palu",
       "Batas divergen, karena magma naik di sepanjang Lembah Palu"],
      "Sesar Palu-Koro adalah sesar mendatar (strike-slip) mengiri dengan laju geser sekitar 3–4 cm per tahun, salah satu sesar paling aktif di Indonesia. Pada gempa M 7,4 tahun 2018, blok di kedua sisi sesar bergeser secara horizontal beberapa meter. Guncangan kuat ini memicu likuifaksi di Petobo dan Balaroa, serta longsoran bawah laut yang membangkitkan tsunami di Teluk Palu. Lembah Palu sendiri berupa cekungan tarik (pull-apart) di sepanjang sesar mendatar ini.\n\nPengecoh: sesar naik dan sesar normal melibatkan gerak vertikal yang dominan. Tidak ada zona subduksi di bawah Palu. Lembah Palu bukan batas divergen dengan magma naik.",
      None),
    Q("Perhatikan peta gerak relatif lempeng di sekitar Indonesia berikut.\n\nLempeng P, Q, dan R berturut-turut adalah …",
      ["Indo-Australia, Pasifik, dan Eurasia", "Eurasia, Indo-Australia, dan Pasifik", "Pasifik, Eurasia, dan Indo-Australia",
       "Indo-Australia, Eurasia, dan Pasifik", "Pasifik, Indo-Australia, dan Eurasia"],
      "• Lempeng P bergerak ke utara–timur laut dengan laju ±7 cm/tahun dari Samudra Hindia dan menunjam di selatan Sumatra–Jawa–Nusa Tenggara: Lempeng Indo-Australia.\n• Lempeng Q bergerak ke barat–barat laut dengan laju ±10 cm/tahun dari Samudra Pasifik ke arah Papua dan Maluku: Lempeng Pasifik (bersama Lempeng Laut Filipina).\n• Lempeng R relatif stabil dan menjadi tempat Paparan Sunda (Sumatra, Jawa, Kalimantan): Lempeng Eurasia.\nPertemuan ketiga lempeng besar ini menjadikan Indonesia sangat aktif secara tektonik: banyak gunung api, gempa bumi, dan pegunungan muda.\n\nPengecoh: opsi lain menukar posisi ketiga lempeng.",
      f_lempeng),
    Q("Laut Merah dipandang sebagai contoh samudra yang masih sangat muda. Dalam siklus Wilson, Laut Merah berada pada tahap …",
      ["Pembukaan samudra muda setelah tahap retakan benua", "Samudra matang yang sangat luas seperti Samudra Atlantik",
       "Samudra yang menyempit karena subduksi di kedua sisinya", "Tumbukan benua–benua yang membentuk pegunungan lipatan",
       "Superbenua yang belum mengalami retakan sama sekali"],
      "Siklus Wilson menggambarkan pembukaan dan penutupan cekungan samudra: (1) retakan benua (misalnya Lembah Retakan Afrika Timur); (2) samudra muda yang sempit mulai terbentuk dengan dasar samudra baru (Laut Merah); (3) samudra matang yang luas dengan tepi benua pasif (Atlantik); (4) samudra menyempit karena subduksi (Pasifik); (5) samudra tertutup dan benua bertumbukan membentuk pegunungan (Himalaya); lalu terbentuk superbenua yang kemudian retak kembali.\nLaut Merah terbentuk karena Jazirah Arab memisah dari Afrika, sehingga berada pada tahap samudra muda.\n\nPengecoh: Atlantik adalah samudra matang. Pasifik adalah samudra yang menyempit. Himalaya adalah tahap tumbukan. Laut Merah bukan superbenua.",
      None),
]

P2 = [
    Q("Perhatikan skala kekerasan Mohs berikut. Sebuah mineral dapat menggores kaca, tetapi dapat digores oleh paku baja. Mineral tersebut kemungkinan besar adalah …",
      ["Ortoklas", "Apatit", "Topaz", "Kalsit", "Korundum"],
      "Analisis kekerasan:\n• Dapat menggores kaca (±5,5) → kekerasannya lebih dari 5,5.\n• Dapat digores paku baja (±6,5) → kekerasannya kurang dari 6,5.\nMineral pada skala Mohs dengan kekerasan di antara 5,5 dan 6,5 adalah ortoklas (6), salah satu feldspar pembentuk granit.\n\nPengecoh: apatit (5) dan kalsit (3) lebih lunak dari kaca sehingga tidak dapat menggoresnya. Topaz (8) dan korundum (9) lebih keras daripada paku baja sehingga tidak dapat digores olehnya. Uji kekerasan relatif seperti ini adalah cara cepat mengenali mineral di lapangan.",
      f_mohs),
    Q("Granit tersusun atas kristal-kristal besar yang terlihat dengan mata, sedangkan basal berbutir sangat halus. Perbedaan tekstur ini terutama disebabkan oleh …",
      ["Kecepatan pendinginan magma: granit membeku lambat di kedalaman, basal membeku cepat di permukaan",
       "Umur batuan: granit selalu lebih muda daripada basal sehingga kristalnya belum mengecil",
       "Jenis pelapukan: granit mengalami pelapukan kimia, basal mengalami pelapukan mekanis",
       "Tekanan metamorfisme: granit terbentuk dari basal yang mengalami tekanan tinggi",
       "Proses sedimentasi: granit tersusun dari butiran pasir besar yang tersemen kuat"],
      "Ukuran kristal batuan beku ditentukan terutama oleh kecepatan pendinginan magma. Granit adalah batuan beku dalam (intrusif/plutonik) yang membeku perlahan di kedalaman selama ribuan hingga jutaan tahun, sehingga atom sempat menyusun kristal besar (tekstur faneritik). Basal adalah batuan beku luar (ekstrusif/vulkanik) dari lava yang membeku cepat di permukaan, sehingga kristalnya sangat halus (afanitik) atau bahkan berbentuk gelas.\nGranit tersingkap di permukaan setelah batuan di atasnya tererosi, misalnya di Bangka Belitung.\n\nPengecoh: umur tidak menentukan ukuran kristal. Pelapukan terjadi setelah batuan terbentuk. Granit bukan hasil metamorfisme basal. Granit adalah batuan beku, bukan batuan sedimen.",
      None),
    Q("Perhatikan hasil pengamatan empat sampel batuan berikut.\n\nPasangan sampel dan nama batuan yang tepat adalah …",
      ["P – granit; Q – batu gamping", "P – basal; R – batu apung", "Q – batu pasir; S – sabak", "R – marmer; S – granit",
       "S – obsidian; Q – sekis"],
      "Identifikasi berdasarkan ciri:\n• P: kristal besar terlihat mata dengan kuarsa dan feldspar → granit (batuan beku dalam, asam).\n• Q: berlapis, bereaksi (berbuih) dengan HCl, mengandung fosil kerang → batu gamping (batuan sedimen karbonat). Reaksi dengan HCl menunjukkan kandungan kalsium karbonat.\n• R: berfoliasi dan membelah menjadi lembaran tipis → sabak (batuan metamorf dari batu lempung).\n• S: berongga banyak, sangat ringan, dapat mengapung → batu apung (batuan beku luar hasil pendinginan cepat lava kaya gas).\nPasangan yang benar adalah P – granit dan Q – batu gamping.\n\nPengecoh: basal berbutir halus, bukan berkristal besar. Batu apung adalah S, bukan R. Sabak adalah R. Marmer tidak berfoliasi lembaran tipis. Obsidian berupa gelas padat tanpa rongga.",
      f_batuan),
    Q("Batu gamping yang mengalami panas dan tekanan tinggi di dekat intrusi magma akan berubah menjadi …",
      ["Marmer", "Kuarsit", "Sabak", "Gneis", "Batu apung"],
      "Batuan metamorf terbentuk dari batuan asal (protolit) yang mengalami perubahan mineral dan tekstur akibat panas, tekanan, dan cairan kimia aktif tanpa melebur.\n• Batu gamping → marmer: kristal kalsit tumbuh membesar dan saling mengunci. Marmer banyak ditambang di Tulungagung (Jawa Timur).\n• Batu pasir kuarsa → kuarsit.\n• Batu lempung/serpih → sabak → filit → sekis (meningkat derajat metamorfismenya).\n• Granit atau batuan sedimen tertentu → gneis (berfoliasi kasar berjalur).\nMetamorfisme di dekat intrusi magma disebut metamorfisme kontak (termal).\n\nPengecoh: kuarsit berasal dari batu pasir. Sabak dari batu lempung. Gneis dari batuan dengan derajat metamorfisme sangat tinggi. Batu apung adalah batuan beku, bukan metamorf.",
      None),
    Q("Perhatikan grafik peluruhan isotop K-40 berikut. Sebuah sampel batuan beku mengandung isotop induk K-40 tinggal 12,5% dari jumlah awalnya. Umur batuan tersebut adalah sekitar …",
      ["3,9 miliar tahun", "1,3 miliar tahun", "2,6 miliar tahun", "5,2 miliar tahun", "0,16 miliar tahun"],
      "Isotop induk tersisa 12,5%: 100% → 50% → 25% → 12,5%, berarti telah berlalu 3 waktu paruh.\nUmur = 3 × 1,3 miliar tahun = 3,9 miliar tahun.\nGrafik juga memperlihatkan titik 12,5% berada pada waktu ±3,9 miliar tahun. Batuan seumur ini termasuk batuan tertua di Bumi, misalnya di perisai benua Kanada dan Australia.\n\nPengecoh: 1,3 dan 2,6 miliar tahun berlaku bila tersisa 50% dan 25%. 5,2 miliar tahun berlaku bila tersisa 6,25% dan bahkan lebih tua dari umur Bumi (±4,6 miliar tahun). 0,16 miliar tahun muncul bila 1,3 dikalikan 0,125, kesalahan konsep.",
      f_paruh),
    Q("Pada sebuah singkapan ditemukan fragmen batuan granit yang terbungkus di dalam lapisan batu pasir. Kesimpulan yang tepat berdasarkan prinsip stratigrafi adalah …",
      ["Granit lebih tua karena fragmennya terbawa saat batu pasir diendapkan",
       "Batu pasir lebih tua daripada granit karena granit menerobos ke dalamnya",
       "Granit dan batu pasir pasti terbentuk pada waktu yang bersamaan",
       "Umur relatif tidak dapat ditentukan tanpa penanggalan radiometrik",
       "Batu pasir terbentuk dari peleburan granit di dalam lapisan tersebut"],
      "Prinsip inklusi (fragmen) menyatakan bahwa fragmen batuan yang terkandung di dalam batuan lain selalu lebih tua daripada batuan yang membungkusnya. Fragmen granit harus sudah ada, kemudian tererosi dan terangkut, lalu terendapkan bersama butiran pasir yang kemudian membatu menjadi batu pasir. Jadi granit lebih tua.\nBedakan dengan kasus intrusi: jika granit menerobos batu pasir (memotong lapisan dan memanggangnya di kontak), maka granit lebih muda.\n\nPengecoh: opsi kedua menggambarkan kasus intrusi, bukan inklusi. Keduanya tidak terbentuk bersamaan. Umur relatif dapat ditentukan dengan prinsip stratigrafi tanpa penanggalan radiometrik. Batu pasir terbentuk dari sedimentasi, bukan peleburan.",
      None),
    Q("Perhatikan skala waktu geologi berikut.\n\nBatas yang ditandai dengan kepunahan massal dinosaurus non-unggas sekitar 66 juta tahun lalu adalah batas antara …",
      ["Kapur dan Paleogen", "Perm dan Trias", "Jura dan Kapur", "Neogen dan Kuarter", "Trias dan Jura"],
      "Pada skala waktu, garis merah 66 juta tahun memisahkan periode Kapur (akhir Mesozoikum) dan Paleogen (awal Kenozoikum). Peristiwa kepunahan massal Kapur–Paleogen (K-Pg) dikaitkan dengan tumbukan asteroid di Chicxulub (Meksiko) dan aktivitas vulkanik besar, yang memusnahkan sekitar 75% spesies termasuk dinosaurus non-unggas.\nBatas 252 juta tahun (Perm–Trias) adalah kepunahan massal terbesar dalam sejarah Bumi.\nBanyak batu bara dan minyak bumi di Indonesia terbentuk pada era Tersier (Paleogen–Neogen), setelah batas ini.\n\nPengecoh: Perm–Trias berumur 252 juta tahun. Jura–Kapur ±145 juta tahun. Neogen–Kuarter ±2,6 juta tahun. Trias–Jura ±201 juta tahun.",
      f_waktu),
    Q("Pasangan jenis tanah dan ciri atau lokasi sebarannya yang tepat adalah …",
      ["Andosol – berasal dari abu vulkanik dan subur di lereng gunung api", "Organosol – berasal dari pelapukan batu gamping di kawasan karst",
       "Grumusol – tanah gambut tebal di rawa pesisir Kalimantan", "Aluvial – terbentuk dari pelapukan batuan beku di puncak gunung",
       "Latosol – tanah pasir pantai yang sangat muda dan tidak berstruktur"],
      "Beberapa jenis tanah di Indonesia:\n• Andosol: berkembang dari abu vulkanik, gembur, kaya bahan organik, dan subur; banyak di lereng gunung api di Jawa dan Sumatra (lahan teh, sayuran).\n• Organosol (gambut): terbentuk dari timbunan bahan organik di rawa, misalnya di pesisir Kalimantan dan Sumatra.\n• Grumusol (vertisol): kaya lempung yang mengembang saat basah dan merekah saat kering; banyak di daerah beriklim kering seperti Jawa Timur dan NTT.\n• Aluvial: endapan sungai di dataran rendah dan delta.\n• Latosol: tanah tua yang sangat tercuci di daerah tropis basah, berwarna merah–kuning.\n• Regosol: tanah pasir muda, misalnya pasir pantai.\nHanya pasangan andosol yang tepat.",
      None),
    Q("Perhatikan grafik komposisi ukuran butir tiga sampel tanah berikut.\n\nTanah yang memiliki laju infiltrasi tertinggi dan paling cepat kehilangan air saat kemarau adalah …",
      ["Tanah K, karena didominasi pasir dengan pori makro yang besar", "Tanah M, karena kandungan liat tinggi menyerap air dengan cepat",
       "Tanah L, karena kandungan debu tertinggi membuat air cepat meresap", "Tanah M, karena liat membentuk pori besar yang mudah dilewati air",
       "Ketiga tanah memiliki laju infiltrasi sama karena jumlah persentasenya 100%"],
      "Tanah K tersusun atas 75% pasir. Butiran pasir berukuran besar sehingga ruang pori di antaranya besar (pori makro). Air meresap dan mengalir ke bawah dengan cepat (infiltrasi dan permeabilitas tinggi), tetapi tanah juga cepat kering karena kemampuannya menahan air rendah. Tanah pasir kurang mampu menyimpan air dan hara bagi tanaman.\nTanah M (60% liat) memiliki pori sangat halus sehingga infiltrasinya lambat, mudah tergenang, tetapi mampu menahan air lebih lama. Tanah L (lempung berdebu) berada di antara keduanya dan umumnya paling ideal untuk pertanian.\n\nPengecoh: liat justru memperlambat infiltrasi dan membentuk pori halus. Debu tidak membuat air paling cepat meresap. Jumlah persentase yang sama tidak berarti sifat fisiknya sama.",
      f_tekstur),
    Q("Permukaan batu gamping di kawasan karst tampak berlekuk-lekuk tajam (lapies/karren) akibat air hujan. Jenis pelapukan yang dominan dalam proses ini adalah …",
      ["Pelapukan kimia melalui pelarutan (karbonasi)", "Pelapukan mekanis akibat pembekuan air di celah batuan",
       "Pelapukan biologis akibat akar tumbuhan yang membesar", "Pelapukan mekanis akibat pemuaian dan penyusutan suhu",
       "Pelapukan mekanis akibat pelepasan tekanan (eksfoliasi)"],
      "Air hujan melarutkan CO₂ dari udara dan tanah sehingga membentuk asam karbonat lemah (H₂CO₃). Asam ini bereaksi dengan kalsium karbonat (CaCO₃) pada batu gamping membentuk kalsium bikarbonat yang larut dan terbawa air. Proses pelarutan ini disebut karbonasi, salah satu bentuk pelapukan kimia. Pelarutan berlangsung lebih intensif di sepanjang retakan dan bidang lapisan, sehingga terbentuk lapies, dolina, gua, dan sungai bawah tanah.\nIklim tropis basah di Indonesia mempercepat proses ini karena curah hujan tinggi dan CO₂ tanah melimpah.\n\nPengecoh: pembekuan air tidak terjadi di dataran rendah tropis. Akar tumbuhan memang dapat memecah batuan, tetapi tidak membentuk lapies. Pemuaian-penyusutan dan eksfoliasi adalah pelapukan mekanis yang khas di daerah kering.",
      None),
]

P3 = [
    Q("Perhatikan profil memanjang sebuah sungai berikut.\n\nBagian sungai yang ditandai lembah berbentuk V, aliran deras, dan banyak air terjun adalah …",
      ["K, bagian hulu dengan gradien curam dan erosi vertikal dominan", "L, bagian tengah dengan erosi lateral dan meander mulai terbentuk",
       "M, bagian hilir dengan gradien landai dan pengendapan dominan", "M, bagian hilir karena debit sungai paling besar",
       "L, bagian tengah karena dasar sungainya paling dalam"],
      "Profil memanjang sungai umumnya cekung ke atas: curam di hulu dan landai di hilir.\n• K (hulu): gradien curam dan energi potensial besar sehingga erosi vertikal (pendalaman) dominan, membentuk lembah V, jeram, dan air terjun.\n• L (tengah): gradien berkurang; erosi lateral (ke samping) mulai dominan, lembah melebar, dan meander mulai terbentuk.\n• M (hilir): gradien sangat landai sehingga kecepatan berkurang dan pengendapan dominan, membentuk dataran banjir, tanggul alam, dan delta.\n\nPengecoh: L dan M tidak dicirikan lembah V dan air terjun. Debit memang terbesar di hilir, tetapi gradiennya landai sehingga tidak terbentuk air terjun. Kedalaman dasar sungai bukan ciri utama yang ditanyakan.",
      f_profil),
    Q("Sebuah sungai memiliki panjang alur 18 km, sedangkan panjang lurus lembahnya 10 km. Nilai indeks sinuositas dan tipe alurnya adalah …",
      ["1,8; bermeander", "0,56; lurus", "1,8; lurus", "8,0; teranyam", "0,56; bermeander"],
      "Indeks sinuositas (SI) = panjang alur sungai ÷ panjang lurus lembah = 18 ÷ 10 = 1,8.\nKlasifikasi umum: SI < 1,05 lurus; 1,05–1,5 berkelok; SI > 1,5 bermeander. Nilai 1,8 menunjukkan sungai bermeander, yang umum dijumpai di dataran rendah dengan gradien landai, misalnya Sungai Kapuas dan Sungai Musi di bagian hilirnya.\n\nPengecoh: 0,56 muncul bila pembagian dibalik (10 ÷ 18); nilai SI tidak mungkin kurang dari 1 karena alur sungai tidak mungkin lebih pendek dari jarak lurusnya. 8,0 adalah selisih kedua panjang, bukan indeks. Sungai teranyam (braided) dicirikan oleh banyak alur bercabang dengan gosong, bukan nilai SI.",
      None),
    Q("Perhatikan empat pola aliran sungai berikut.\n\nPola aliran yang paling umum dijumpai pada kerucut gunung api seperti Gunung Merapi atau Gunung Slamet adalah …",
      ["Pola 2, radial sentrifugal", "Pola 1, dendritik", "Pola 3, trellis", "Pola 4, anular", "Pola 1 dan 3 secara bersamaan"],
      "• Pola 1 (dendritik): bercabang seperti pohon, terbentuk pada batuan yang homogen dengan lereng relatif seragam.\n• Pola 2 (radial sentrifugal): sungai-sungai mengalir menyebar dari satu puncak ke segala arah, khas kerucut gunung api atau kubah.\n• Pola 3 (trellis): sungai utama dengan anak sungai yang tegak lurus dan sejajar, khas daerah perbukitan lipatan.\n• Pola 4 (anular): melingkar mengikuti batuan lunak pada kubah yang tererosi.\nPada kerucut gunung api, air hujan mengalir menuruni lereng ke segala arah dari puncak, sehingga terbentuk pola radial sentrifugal. Pola ini juga menjelaskan mengapa lahar dapat mengalir ke banyak lembah di sekeliling gunung.\n\nPengecoh: dendritik, trellis, dan anular dikendalikan oleh kondisi batuan dan struktur yang berbeda.",
      f_pola),
    Q("Sebuah DAS memiliki 48 sungai orde 1, 12 sungai orde 2, dan 3 sungai orde 3. Rasio percabangan rata-rata (Rb) DAS tersebut dan interpretasinya adalah …",
      ["Rb = 4; tergolong normal, respons banjir tidak terlalu cepat", "Rb = 16; tergolong sangat tinggi sehingga banjir sangat cepat",
       "Rb = 0,25; tergolong rendah sehingga DAS tidak memiliki sungai", "Rb = 21; sama dengan jumlah rata-rata sungai per orde",
       "Rb = 4; tergolong sangat rendah sehingga banjir datang mendadak"],
      "Rasio percabangan Rb = jumlah sungai orde n ÷ jumlah sungai orde n+1.\n• Orde 1 ke orde 2: 48 ÷ 12 = 4.\n• Orde 2 ke orde 3: 12 ÷ 3 = 4.\nRb rata-rata = (4 + 4) ÷ 2 = 4.\nNilai Rb 3–5 tergolong normal; struktur geologi tidak terlalu mengganggu pola aliran. Nilai Rb kecil (< 3) menunjukkan DAS cenderung membulat sehingga air dari banyak anak sungai tiba hampir bersamaan dan memicu banjir cepat, sedangkan Rb besar (> 5) menunjukkan DAS memanjang dengan respons banjir lebih lambat.\n\nPengecoh: 16 adalah perkalian kedua rasio. 0,25 adalah kebalikan rasio. 21 adalah rata-rata jumlah sungai per orde. Rb = 4 tidak tergolong sangat rendah.",
      None),
    Q("Perhatikan kenampakan sungai bermeander berikut.\n\nPernyataan yang paling tepat adalah …",
      ["P mengalami erosi tebing, sedangkan Q dan R menjadi tempat pengendapan gosong",
       "P menjadi tempat pengendapan gosong, sedangkan Q dan R mengalami erosi tebing",
       "P, Q, dan R mengalami pengendapan karena kecepatan arus di seluruh kelokan sama",
       "R mengalami erosi tebing terkuat karena berada di sisi luar kelokan sungai",
       "Q mengalami erosi tebing terkuat karena aliran tercepat berada di sisi dalam"],
      "Pada kelokan sungai, arus tercepat terdorong ke sisi luar kelokan, sedangkan di sisi dalam kelokan arus melambat.\n• P berada di sisi luar kelokan atas sehingga mengalami erosi lateral yang membentuk tebing curam (cut bank).\n• Q berada di sisi dalam kelokan atas dan R di sisi dalam kelokan bawah; di kedua tempat ini arus lambat sehingga material diendapkan menjadi gosong (point bar), seperti ditunjukkan warna pasir pada gambar.\nKarena erosi di sisi luar dan pengendapan di sisi dalam berlangsung terus, kelokan makin besar dan bergeser. Bila dua kelokan akhirnya berdekatan dan lehernya terputus saat banjir, terbentuk danau tapal kuda (oxbow lake).\n\nPengecoh: opsi kedua membalik lokasi erosi dan pengendapan. Kecepatan arus tidak sama di seluruh kelokan. R berada di sisi dalam, bukan sisi luar. Aliran tercepat tidak berada di sisi dalam.",
      f_meander),
    Q("Delta Sungai Mississippi berbentuk kaki burung (bird's foot), sedangkan Delta Sungai Nil berbentuk kipas (arkuat). Faktor utama yang menyebabkan bentuk kaki burung adalah …",
      ["Suplai sedimen sungai sangat besar sedangkan energi gelombang dan pasang surut lemah",
       "Energi gelombang laut sangat kuat sehingga sedimen tersebar merata membentuk kipas",
       "Pasang surut yang sangat kuat membentuk alur-alur lebar berbentuk corong",
       "Sungai membawa sedikit sedimen sehingga hanya terbentuk beberapa alur sempit",
       "Delta terbentuk di laut dalam sehingga sedimen langsung tenggelam ke dasar"],
      "Bentuk delta ditentukan oleh perimbangan tiga proses: suplai sedimen sungai, energi gelombang, dan pasang surut.\n• Delta dominasi sungai (kaki burung): suplai sedimen sangat besar dengan gelombang dan pasang surut lemah, sehingga distributari memanjang jauh ke laut dengan tanggul alam di kiri-kanannya (Mississippi).\n• Delta dominasi gelombang (arkuat/kipas atau runcing): gelombang meratakan sedimen di sepanjang pantai (Nil, São Francisco).\n• Delta dominasi pasang surut: alur-alur lebar berbentuk corong dan pulau-pulau memanjang (Gangga–Brahmaputra, Mahakam yang juga dipengaruhi sungai).\n\nPengecoh: gelombang kuat menghasilkan delta arkuat. Pasang surut kuat menghasilkan delta berbentuk corong. Sedimen sedikit tidak membentuk delta besar. Laut dalam justru menghambat pembentukan delta.",
      None),
    Q("Perhatikan penampang bentang lahan karst berikut.\n\nKenampakan yang membentuk lanskap \"Seribu Bukit\" di Gunung Sewu ditunjukkan oleh label …",
      ["N, bukit kerucut karst", "K, dolina", "L, luweng (ponor)", "M, gua dengan stalaktit", "K dan L, cekungan pelarutan"],
      "Kenampakan karst pada gambar:\n• K: dolina, cekungan tertutup berbentuk mangkuk hasil pelarutan atau runtuhan.\n• L: luweng atau ponor, lubang vertikal tempat air permukaan masuk ke sistem bawah tanah.\n• M: gua dengan stalaktit, ruang bawah tanah hasil pelarutan; stalaktit terbentuk dari pengendapan kalsit pada tetesan air di atap gua.\n• N: bukit-bukit membulat yang tersisa di antara cekungan pelarutan, disebut bukit kerucut karst (conical hills/kegelkarst).\nLanskap Gunung Sewu (Gunungkidul–Wonogiri–Pacitan) yang terkenal dengan ribuan bukit kerucut merupakan karst tropis, kini ditetapkan sebagai UNESCO Global Geopark.\n\nPengecoh: dolina dan luweng adalah cekungan atau lubang, bukan bukit. Gua adalah kenampakan bawah tanah.",
      f_karst2),
    Q("Syarat utama terbentuknya topografi karst yang berkembang baik adalah …",
      ["Batu gamping murni dan tebal, banyak retakan, serta curah hujan tinggi", "Batuan beku basaltik yang tebal, keras, dan tidak berongga",
       "Batu gamping tipis yang tertutup lapisan lempung kedap air", "Iklim gurun kering dengan curah hujan kurang dari 250 mm",
       "Daerah dataran rendah yang selalu tergenang air laut"],
      "Topografi karst terbentuk melalui pelarutan batuan yang mudah larut, terutama batu gamping. Syarat berkembangnya karst antara lain: (1) batu gamping murni (kandungan CaCO₃ tinggi) dan tebal; (2) batuan banyak memiliki kekar atau retakan sebagai jalur air; (3) curah hujan cukup tinggi sebagai pelarut; (4) batuan terangkat di atas muka air tanah sehingga air dapat bersirkulasi ke bawah; dan (5) vegetasi yang menghasilkan CO₂ tanah.\nIndonesia memiliki kawasan karst luas, misalnya Gunung Sewu, Maros–Pangkep, Sangkulirang–Mangkalihat, dan Raja Ampat.\n\nPengecoh: batuan beku basaltik tidak mudah larut. Batu gamping tipis tertutup lempung menghambat pelarutan. Iklim gurun kekurangan air. Daerah yang selalu tergenang air laut tidak memiliki sirkulasi air tanah yang mendukung.",
      None),
    Q("Perhatikan data morfometri tiga DAS berikut. Kerapatan aliran Dd = panjang total sungai ÷ luas DAS.\n\nDAS yang paling cepat menghasilkan banjir setelah hujan lebat adalah …",
      ["DAS Z, Dd = 3,0 km/km²", "DAS X, Dd = 1,5 km/km²", "DAS Y, Dd = 0,6 km/km²", "DAS Y, Dd = 1,7 km/km²", "DAS X, Dd = 0,67 km/km²"],
      "Hitung kerapatan aliran:\n• X: 450 ÷ 300 = 1,5 km/km².\n• Y: 180 ÷ 300 = 0,6 km/km².\n• Z: 900 ÷ 300 = 3,0 km/km².\nKerapatan aliran tinggi berarti jaringan sungai rapat sehingga jarak tempuh air hujan dari lereng menuju alur sungai pendek. Air cepat terkumpul di sungai sehingga debit puncak tinggi dan cepat tercapai. DAS dengan Dd tinggi biasanya berbatuan kedap air dan bervegetasi jarang. Sebaliknya Dd rendah menunjukkan batuan permeabel (misalnya karst) dengan infiltrasi besar.\n\nPengecoh: Dd X dan Y lebih kecil. Nilai 1,7 dan 0,67 berasal dari kesalahan pembagian. Dd yang rendah justru menandakan respons banjir lebih lambat.",
      f_dd),
    Q("Permukiman tradisional di dataran banjir sungai besar seperti Bengawan Solo sering dibangun di atas tanggul alam. Alasan geografis yang paling tepat adalah …",
      ["Tanggul alam lebih tinggi dan berdrainase lebih baik daripada rawa belakang", "Tanggul alam tersusun dari lempung kedap sehingga tidak pernah dilalui air",
       "Tanggul alam terbentuk dari endapan vulkanik yang paling subur", "Tanggul alam berada jauh dari sungai sehingga aman dari erosi tebing",
       "Tanggul alam adalah bangunan buatan pemerintah kolonial untuk permukiman"],
      "Saat banjir, air meluap dari alur sungai dan kecepatannya langsung berkurang, sehingga material yang lebih kasar (pasir dan debu) diendapkan di tepi sungai membentuk tanggul alam (natural levee). Material halus (lempung) terbawa lebih jauh dan mengendap di rawa belakang (backswamp) yang lebih rendah. Akibatnya tanggul alam lebih tinggi, lebih jarang tergenang lama, dan drainasenya lebih baik, sehingga cocok untuk permukiman dan pekarangan, sedangkan rawa belakang sering dimanfaatkan untuk sawah.\n\nPengecoh: tanggul alam tersusun atas pasir–debu, bukan lempung kedap. Tanggul alam bukan endapan vulkanik. Tanggul alam justru berada tepat di tepi sungai. Tanggul alam terbentuk secara alami, bukan buatan.",
      None),
]

P4 = [
    Q("Perhatikan bentuk lahan hasil pengendapan marin berikut.\n\nBentuk lahan yang menghubungkan daratan utama dengan sebuah pulau kecil ditunjukkan oleh label …",
      ["Q, tombolo", "P, spit", "R, pulau karang", "S, gisik", "P, tombolo"],
      "Arus sejajar pantai (longshore current) mengangkut pasir di sepanjang pantai lalu mengendapkannya ketika energinya berkurang.\n• P: endapan pasir yang memanjang ke laut dari daratan dengan ujung bebas, disebut spit (bura). Bila spit menutup teluk, terbentuk laguna.\n• Q: endapan pasir yang menghubungkan daratan utama dengan sebuah pulau, disebut tombolo. Gelombang yang terbiaskan di belakang pulau kehilangan energi sehingga pasir mengendap.\n• R: pulau yang dihubungkan oleh tombolo.\n• S: daerah pesisir daratan.\nContoh tombolo di Indonesia antara lain di Pantai Kuta Mandalika (Lombok) dan beberapa pantai di Maluku.\n\nPengecoh: spit memiliki ujung bebas. R adalah pulaunya, bukan endapan penghubung. \"P, tombolo\" salah menamai bentuk lahan P.",
      f_pantai),
    Q("Sebuah groin (krib) dibangun tegak lurus garis pantai untuk menahan abrasi. Setelah beberapa tahun, pantai di sisi hulu arus sejajar pantai bertambah lebar, tetapi pantai di sisi hilirnya justru tererosi. Penjelasan yang paling tepat adalah …",
      ["Groin menahan pasir dari arus sejajar pantai sehingga sisi hilir kekurangan sedimen",
       "Groin menambah energi gelombang di sisi hulu sehingga pasir menumpuk di sana",
       "Groin menghentikan pasang surut di sisi hilir sehingga pantai menjadi kering",
       "Pasir di sisi hilir hilang karena ditambang masyarakat untuk bahan membangun groin",
       "Arus sejajar pantai berbalik arah setelah groin dibangun"],
      "Arus sejajar pantai mengangkut pasir di sepanjang garis pantai (longshore drift). Groin yang tegak lurus pantai memotong aliran pasir ini, sehingga pasir tertahan dan menumpuk di sisi hulu arus. Sisi hilir groin kehilangan pasokan pasir, padahal gelombang tetap mengikis pantai, sehingga terjadi erosi. Inilah alasan pembangunan struktur pantai harus mempertimbangkan sistem sel sedimen secara utuh, karena melindungi satu lokasi dapat memindahkan masalah ke lokasi lain.\n\nPengecoh: groin tidak menambah energi gelombang. Groin tidak menghentikan pasang surut. Penambangan pasir bukan penjelasan dalam konteks soal. Arus sejajar pantai ditentukan oleh arah datang gelombang, bukan oleh groin.",
      None),
    Q("Perhatikan peta geologi sederhana berikut.\n\nStruktur geologi yang paling mungkin terdapat di daerah tersebut adalah …",
      ["Sinklin, karena lapisan termuda di tengah dan miring ke arah pusat", "Antiklin, karena lapisan termuda berada di tengah dan miring menjauhi pusat",
       "Sinklin, karena lapisan tertua berada di tengah dan miring menjauhi pusat", "Sesar normal, karena lapisan di kedua sisi berumur sama",
       "Antiklin, karena lapisan miring ke arah pusat lipatan"],
      "Pada peta, satuan batuan tersusun simetris: Ta (Eosen, tertua) di tepi, Tb (Oligosen) di tengah-tepi, dan Tc (Miosen, termuda) di bagian tengah. Simbol arah kemiringan menunjukkan lapisan di kiri miring ke kanan dan lapisan di kanan miring ke kiri, yaitu ke arah pusat.\nPola batuan termuda di tengah dan kemiringan lapisan ke arah pusat adalah ciri sinklin. Pada antiklin yang tererosi, polanya kebalikannya: batuan tertua di tengah dan lapisan miring menjauhi pusat.\n\nPengecoh: opsi antiklin keliru membaca umur atau arah kemiringan. Sinklin tidak memiliki batuan tertua di tengah. Pola simetris dengan perulangan lapisan bukan ciri utama sesar normal.",
      f_geomap),
    Q("Gumuk pasir di Parangtritis (Yogyakarta) merupakan bentang lahan eolin yang langka di daerah tropis basah. Faktor utama pembentukannya adalah …",
      ["Pasokan pasir vulkanik dari sungai, angin laut yang kuat, dan pantai yang luas", "Pelapukan batu gamping di Gunung Sewu yang menghasilkan pasir halus",
       "Endapan glasial yang tersisa sejak zaman es di pesisir selatan Jawa", "Abrasi tebing yang menghasilkan pasir lalu terendapkan oleh arus sungai",
       "Curah hujan sangat tinggi yang membawa pasir dari puncak gunung ke pantai"],
      "Gumuk pasir Parangtritis terbentuk dari kombinasi beberapa faktor: (1) pasokan pasir vulkanik dari Gunung Merapi yang diangkut Sungai Opak dan Progo ke laut; (2) gelombang Samudra Hindia yang kuat mengembalikan pasir ke pantai sehingga terbentuk gisik yang luas; (3) angin laut kuat dari arah selatan–barat daya, terutama saat musim kemarau, menerbangkan pasir kering ke darat; dan (4) adanya penghalang (Gunung Sewu di timur) yang memengaruhi pola angin dan pengendapan.\nGumuk pasir tipe barkhan di Parangtritis kini terancam oleh vegetasi dan pembangunan.\n\nPengecoh: pasirnya berasal dari material vulkanik, bukan batu gamping. Tidak ada endapan glasial di Jawa. Peran utama dalam pembentukan gumuk adalah angin, bukan arus sungai saja. Hujan tinggi justru menghambat pergerakan pasir.",
      None),
    Q("Perhatikan bentuk gumuk pasir (tampak atas) berikut.\n\nJenis gumuk pasir dan arah angin dominan yang membentuknya adalah …",
      ["Barkhan; angin bertiup dari barat ke timur", "Barkhan; angin bertiup dari timur ke barat",
       "Gumuk parabola; angin bertiup dari timur ke barat", "Gumuk memanjang (longitudinal); angin bertiup dari utara",
       "Barkhan; angin bertiup dari utara ke selatan"],
      "Gumuk pada gambar berbentuk bulan sabit dengan dua tanduk yang mengarah ke timur, lereng landai di sisi barat, dan lereng curam (slip face) di sisi timur. Ini adalah gumuk barkhan. Pada barkhan, angin datang dari sisi lereng landai, mendorong pasir naik, lalu pasir longsor di sisi lereng curam. Tanduk-tanduknya bergerak lebih cepat karena volume pasirnya lebih kecil, sehingga mengarah ke arah angin bertiup. Jadi angin bertiup dari barat ke timur.\n\nPengecoh: angin dari timur akan membentuk lereng landai di timur dan tanduk ke barat. Gumuk parabola memiliki tanduk yang mengarah ke hulu angin (berlawanan dengan barkhan) dan biasanya tertahan vegetasi. Gumuk memanjang sejajar arah angin, tidak berbentuk sabit.",
      f_barchan),
    Q("Di Puncak Jaya, Papua, terdapat gletser tropis yang terus menyusut. Bentuk lahan berikut yang merupakan hasil erosi gletser adalah …",
      ["Lembah berbentuk U dan sirkus", "Delta sungai dan tanggul alam", "Dolina dan uvala karst", "Tombolo dan spit pasir", "Barkhan dan gumuk parabola"],
      "Gletser adalah massa es yang bergerak perlahan menuruni lereng. Gletser mengikis batuan melalui proses plucking (mencabut bongkah batuan) dan abrasi (menggerus dasar dan dinding lembah). Hasil erosinya antara lain: lembah berbentuk U (lembah sungai berbentuk V yang dilebarkan gletser), sirkus (cekungan berbentuk mangkuk di kepala gletser), arête (punggungan tajam), dan horn (puncak runcing). Material yang diendapkan gletser membentuk moraine.\nGletser di Puncak Jaya (Carstensz) adalah salah satu dari sedikit gletser tropis di dunia dan diperkirakan akan hilang dalam beberapa tahun karena pemanasan global.\n\nPengecoh: delta dan tanggul alam adalah bentuk lahan fluvial. Dolina dan uvala adalah bentuk lahan karst. Tombolo dan spit adalah bentuk lahan marin. Barkhan dan gumuk parabola adalah bentuk lahan eolin.",
      None),
    Q("Perhatikan empat pola garis kontur berikut.\n\nPola yang menggambarkan lembah sungai adalah …",
      ["Pola 2, kontur berbentuk V yang meruncing ke arah elevasi lebih tinggi", "Pola 3, kontur berbentuk V yang meruncing ke arah elevasi lebih rendah",
       "Pola 1, kontur melingkar tertutup dengan elevasi makin tinggi ke tengah", "Pola 4, kontur melingkar tertutup dengan garis gerigi ke arah dalam",
       "Pola 1 dan 4, karena keduanya berbentuk lingkaran tertutup"],
      "Membaca pola kontur:\n• Pola 1: kontur melingkar tertutup dengan elevasi makin tinggi ke tengah (100 → 400 m) → bukit atau puncak.\n• Pola 2: kontur membentuk huruf V yang meruncing ke arah elevasi lebih tinggi, dan alur sungai melintas di ujung V → lembah sungai. Aturannya: kontur yang memotong sungai membentuk V yang menunjuk ke hulu.\n• Pola 3: kontur membentuk V yang meruncing ke arah elevasi lebih rendah → punggungan (taji).\n• Pola 4: kontur tertutup dengan garis gerigi (hachure) mengarah ke dalam → cekungan atau depresi, misalnya kawah atau dolina.\n\nPengecoh: pola 3 adalah punggungan, kebalikan lembah. Pola 1 dan 4 berbentuk tertutup sehingga bukan lembah.",
      f_kontur4),
    Q("Dalam klasifikasi satuan bentuk lahan berdasarkan asal proses (genesis), lereng tengah Gunung Merapi yang tersusun atas endapan piroklastik dan lahar termasuk satuan bentuk lahan asal …",
      ["Vulkanik", "Struktural", "Denudasional", "Fluvial", "Marin"],
      "Satuan bentuk lahan dikelompokkan menurut proses utama pembentuknya:\n• Vulkanik (V): hasil aktivitas gunung api, misalnya kerucut, lereng, kaki, dan dataran kaki gunung api, serta aliran lava dan lahar.\n• Struktural (S): hasil tenaga tektonik seperti lipatan dan sesar, misalnya perbukitan lipatan dan gawir sesar.\n• Denudasional (D): hasil pelapukan, erosi, dan gerakan massa yang dominan, misalnya perbukitan terkikis.\n• Fluvial (F): hasil kerja sungai, misalnya dataran banjir dan tanggul alam.\n• Marin (M): hasil kerja laut, misalnya gisik dan rataan pasang surut.\n• Eolin (E), karst (K), glasial (G), dan organik (O).\nLereng tengah Merapi terbentuk oleh endapan erupsi, sehingga termasuk bentuk lahan asal vulkanik.\n\nPengecoh: kelompok lain tidak sesuai dengan proses pembentuk utama lereng gunung api.",
      None),
    Q("Perhatikan grafik mundurnya tebing pantai di Tanjung T berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Laju mundur tebing meningkat; dekade 2010–2020 sekitar 2,6 m per tahun", "Laju mundur tebing tetap sekitar 1,8 m per tahun selama 30 tahun",
       "Laju mundur tebing menurun; dekade 2010–2020 sekitar 0,26 m per tahun", "Tebing maju ke laut sejauh 66 m karena pengendapan sedimen",
       "Laju mundur tebing rata-rata 66 m per tahun selama periode 1990–2020"],
      "Hitung laju mundur per dekade:\n• 1990–2000: 18 m ÷ 10 tahun = 1,8 m/tahun.\n• 2000–2010: (40 − 18) = 22 m ÷ 10 = 2,2 m/tahun.\n• 2010–2020: (66 − 40) = 26 m ÷ 10 = 2,6 m/tahun.\nLaju mundur meningkat dari waktu ke waktu. Rata-rata selama 30 tahun adalah 66 ÷ 30 = 2,2 m/tahun. Peningkatan laju dapat dipicu kenaikan muka laut, gelombang yang lebih kuat, hilangnya vegetasi pelindung, atau penambangan pasir di sekitarnya.\n\nPengecoh: laju tidak tetap. 0,26 m/tahun adalah kesalahan pembagian. Nilai negatif pada grafik menunjukkan mundur ke darat, bukan maju ke laut. 66 m adalah total jarak, bukan laju per tahun.",
      f_tebing),
    Q("Pantai timur Amerika Selatan dan pantai barat Afrika dicirikan oleh paparan benua yang lebar, sedimen tebal, serta hampir tidak ada gempa dan gunung api. Kawasan seperti ini disebut …",
      ["Tepi benua pasif, karena tidak berada di batas lempeng", "Tepi benua aktif, karena terjadi subduksi di bawah benua",
       "Batas lempeng transform, karena lempeng bergeser sejajar", "Busur kepulauan vulkanik di atas zona subduksi",
       "Punggungan tengah samudra yang sedang aktif memekar"],
      "Tepi benua pasif (passive continental margin) adalah tepi benua yang tidak berada di batas lempeng. Kawasan ini terbentuk setelah benua terpisah (rifting) dan samudra di antaranya melebar, misalnya Atlantik. Karena jauh dari batas lempeng, aktivitas tektonik sangat rendah: hampir tidak ada gempa besar dan gunung api. Paparan benuanya lebar dan menjadi tempat pengendapan sedimen tebal, sehingga sering menyimpan cadangan minyak dan gas.\nSebaliknya tepi benua aktif berada di batas lempeng konvergen atau transform, misalnya pantai barat Amerika Selatan dan selatan Jawa, dengan palung, gempa, dan gunung api.\n\nPengecoh: tepi benua aktif, transform, busur kepulauan, dan punggungan tengah samudra semuanya aktif secara tektonik.",
      None),
]

P5 = [
    Q("Perhatikan tabel kelas kemampuan lahan berdasarkan kemiringan lereng berikut. Sebidang lahan memiliki kemiringan 38% dan saat ini ditanami sayuran semusim secara intensif.\n\nPenilaian yang paling tepat adalah …",
      ["Lahan termasuk kelas VI sehingga tidak sesuai untuk tanaman semusim intensif", "Lahan termasuk kelas III sehingga sesuai untuk tanaman semusim tanpa konservasi",
       "Lahan termasuk kelas VIII sehingga wajib dijadikan cagar alam", "Lahan termasuk kelas IV sehingga paling ideal untuk tanaman semusim",
       "Lahan termasuk kelas I sehingga dapat dimanfaatkan untuk semua jenis tanaman"],
      "Kemiringan 38% berada pada rentang 30–45%, yaitu kelas VI. Lahan kelas VI memiliki hambatan berat sehingga tidak sesuai untuk tanaman semusim; pemanfaatan yang dianjurkan adalah padang rumput, hutan produksi, atau tanaman tahunan dengan konservasi ketat. Penanaman sayuran semusim secara intensif pada lereng curam, seperti di kawasan Dieng, memicu erosi tinggi, longsor, dan sedimentasi waduk di hilir.\n\nPengecoh: kelas III (8–15%) dan kelas IV (15–30%) memiliki lereng lebih landai. Kelas VIII untuk lereng di atas 65%. Kelas I untuk lereng 0–3%. Konsep kemampuan lahan menekankan bahwa penggunaan lahan harus sesuai dengan kapasitas dan hambatannya agar tidak terjadi degradasi.",
      f_kelas),
    Q("Penetapan fungsi kawasan memakai skor: kelas lereng × 20, kelas jenis tanah menurut kepekaan erosi × 15, dan kelas intensitas hujan × 10. Kawasan dengan skor ≥ 175 ditetapkan sebagai kawasan lindung. Sebuah lahan memiliki kelas lereng 4, kelas tanah 5, dan kelas hujan 3. Fungsi kawasan tersebut adalah …",
      ["Kawasan lindung, dengan skor 185", "Kawasan penyangga, dengan skor 165", "Kawasan budi daya, dengan skor 120",
       "Kawasan lindung, dengan skor 205", "Kawasan budi daya, dengan skor 12"],
      "Skor = (kelas lereng × 20) + (kelas tanah × 15) + (kelas hujan × 10)\n= (4 × 20) + (5 × 15) + (3 × 10) = 80 + 75 + 30 = 185.\nKarena 185 ≥ 175, lahan ditetapkan sebagai kawasan lindung. Kriteria ini (berdasarkan SK Menteri Pertanian No. 837/1980) menggabungkan tiga faktor utama penyebab erosi dan longsor.\n\nPengecoh: 165 dan 205 berasal dari salah mengalikan salah satu faktor. 120 muncul bila ketiga kelas dikalikan 10. 12 adalah jumlah kelas tanpa bobot. Hasil ini menunjukkan bahwa lahan yang terlihat datar pun dapat menjadi kawasan lindung bila tanahnya sangat peka erosi dan hujannya tinggi, dan sebaliknya.",
      None),
    Q("Perhatikan matriks perubahan penggunaan lahan Kabupaten L tahun 2010–2020 berikut. Baris menunjukkan penggunaan lahan 2010 dan kolom menunjukkan 2020.\n\nKonversi lahan terbesar yang terjadi selama periode tersebut adalah …",
      ["Hutan menjadi kebun campur, seluas 1.300 ha", "Sawah menjadi permukiman, seluas 1.200 ha", "Kebun campur menjadi sawah, seluas 500 ha",
       "Hutan menjadi permukiman, seluas 3.000 ha", "Sawah menjadi sawah, seluas 5.600 ha"],
      "Pada matriks perubahan, sel diagonal (hutan–hutan 8.200, kebun–kebun 4.100, sawah–sawah 5.600, permukiman–permukiman 3.000) menunjukkan lahan yang tidak berubah. Sel di luar diagonal menunjukkan konversi:\n• Hutan → kebun campur 1.300; hutan → sawah 300; hutan → permukiman 200.\n• Kebun → sawah 500; kebun → permukiman 400.\n• Sawah → kebun 200; sawah → permukiman 1.200.\nKonversi terbesar adalah hutan menjadi kebun campur (1.300 ha), disusul sawah menjadi permukiman (1.200 ha).\n\nPengecoh: 3.000 ha adalah permukiman yang tetap permukiman (bukan konversi dari hutan). 5.600 ha adalah sawah yang tidak berubah. Kebun ke sawah hanya 500 ha.",
      f_matriks),
    Q("Dalam kajian geografi, istilah penggunaan lahan (land use) dibedakan dari tutupan lahan (land cover). Contoh yang menunjukkan perbedaan keduanya adalah …",
      ["Tutupan lahan berupa rumput, tetapi penggunaannya lapangan golf atau padang penggembalaan", "Tutupan lahan dan penggunaan lahan selalu sama sehingga tidak perlu dibedakan",
       "Penggunaan lahan hanya dapat diamati langsung dari citra satelit tanpa survei lapangan", "Tutupan lahan berkaitan dengan fungsi ekonomi, penggunaan lahan dengan fisik permukaan",
       "Penggunaan lahan hanya berlaku untuk kawasan perkotaan, bukan perdesaan"],
      "Tutupan lahan (land cover) adalah kenampakan fisik yang menutupi permukaan Bumi, misalnya vegetasi, air, tanah terbuka, dan bangunan. Penggunaan lahan (land use) adalah fungsi atau aktivitas manusia pada lahan tersebut, misalnya pertanian, permukiman, rekreasi, dan konservasi.\nSatu jenis tutupan dapat memiliki penggunaan berbeda: tutupan rumput dapat dipakai sebagai lapangan golf, padang penggembalaan, atau taman kota. Sebaliknya penggunaan yang sama (misalnya kawasan hutan produksi) dapat memiliki tutupan berbeda (hutan lebat atau lahan terbuka bekas tebangan).\nCitra satelit langsung merekam tutupan lahan, sedangkan penggunaan lahan sering memerlukan interpretasi konteks dan survei lapangan.\n\nPengecoh: keduanya tidak selalu sama. Definisi pada opsi keempat terbalik. Penggunaan lahan berlaku di kota maupun desa.",
      None),
    Q("Perhatikan diagram penggunaan lahan Kabupaten B tahun 2005 dan 2025 berikut.\n\nPersentase perubahan luas sawah selama periode tersebut adalah …",
      ["Berkurang 30%", "Berkurang 12%", "Berkurang 43%", "Bertambah 30%", "Berkurang 120%"],
      "Luas kabupaten 1.000 km².\n• Sawah 2005 = 40% × 1.000 = 400 km².\n• Sawah 2025 = 28% × 1.000 = 280 km².\n• Perubahan = 280 − 400 = −120 km².\n• Persentase perubahan = (−120 ÷ 400) × 100% = −30% (berkurang 30%).\nPada periode yang sama permukiman naik dari 15% menjadi 30%, menunjukkan konversi sawah menjadi permukiman akibat urbanisasi, yang mengancam ketahanan pangan daerah.\n\nPengecoh: 12% adalah selisih poin persentase (40% − 28%), bukan persentase perubahan relatif. 43% muncul bila dibagi nilai akhir (120 ÷ 280). \"Bertambah\" salah arah. 120% adalah salah menuliskan 120 km² sebagai persen. Ingat: persentase perubahan selalu dibagi nilai awal.",
      f_pie2),
    Q("Alih fungsi sawah beririgasi teknis menjadi kawasan industri dan perumahan banyak terjadi di jalur pantai utara Jawa. Dampak jangka panjang yang paling dikhawatirkan adalah …",
      ["Hilangnya lahan pangan produktif yang sulit digantikan oleh pencetakan sawah baru", "Meningkatnya produksi padi karena lahan industri menyediakan pupuk murah",
       "Turunnya kebutuhan pangan karena penduduk pindah dari Jawa ke luar Jawa", "Bertambahnya luas hutan karena petani beralih menjadi buruh industri",
       "Meningkatnya kualitas tanah sawah di sekitar kawasan industri"],
      "Sawah beririgasi teknis di dataran aluvial Jawa adalah lahan pertanian paling produktif di Indonesia, didukung tanah subur dan infrastruktur irigasi yang dibangun selama puluhan tahun. Ketika dikonversi menjadi industri atau perumahan, perubahan ini praktis tidak dapat dikembalikan. Pencetakan sawah baru di luar Jawa sering terkendala tanah yang kurang subur, ketiadaan irigasi, dan biaya tinggi, sehingga produktivitasnya lebih rendah. Karena itu pemerintah menetapkan Lahan Pertanian Pangan Berkelanjutan (LP2B) melalui UU No. 41 Tahun 2009.\n\nPengecoh: industri tidak menaikkan produksi padi. Kebutuhan pangan terus naik seiring pertumbuhan penduduk. Konversi sawah tidak menambah hutan. Kawasan industri justru berpotensi mencemari tanah sawah di sekitarnya.",
      None),
    Q("Perhatikan potongan peta kontur lereng S berikut. Kelas kemiringan: 0–8% datar; 8–15% landai; 15–25% agak curam; 25–45% curam; > 45% sangat curam.\n\nKelas kemiringan lereng S adalah …",
      ["Agak curam, sekitar 16,7%", "Curam, sekitar 41,7%", "Landai, sekitar 12,5%", "Sangat curam, sekitar 167%", "Datar, sekitar 4,2%"],
      "1) Beda tinggi antara dua kontur berurutan = interval kontur = 12,5 m.\n2) Jarak horizontal sebenarnya = 3 mm × 25.000 = 75.000 mm = 75 m.\n3) Kemiringan = (12,5 ÷ 75) × 100% ≈ 16,7% → agak curam (15–25%).\n\nPengecoh: 41,7% muncul bila jarak peta dianggap 1,2 mm atau salah konversi. 12,5% menganggap jarak horizontal 100 m. 167% adalah kesalahan satuan (7,5 m). 4,2% muncul bila jarak dikalikan empat. Interval kontur peta skala 1:25.000 adalah 1/2.000 × 25.000 = 12,5 m.",
      f_lereng),
    Q("Indeks vegetasi NDVI dihitung dengan rumus NDVI = (NIR − Red) ÷ (NIR + Red). Sebuah piksel memiliki pantulan inframerah dekat (NIR) 0,50 dan merah (Red) 0,10. Nilai NDVI dan interpretasinya adalah …",
      ["0,67; vegetasi rapat dan sehat", "0,40; lahan terbuka tanpa vegetasi", "1,50; badan air yang dalam", "−0,67; awan tebal", "0,60; permukiman padat"],
      "NDVI = (0,50 − 0,10) ÷ (0,50 + 0,10) = 0,40 ÷ 0,60 ≈ 0,67.\nVegetasi sehat memantulkan inframerah dekat sangat kuat (struktur sel daun) dan menyerap cahaya merah untuk fotosintesis (klorofil), sehingga NDVI tinggi. Nilai sekitar 0,6–0,9 menunjukkan vegetasi rapat seperti hutan atau sawah yang subur. Lahan terbuka dan permukiman memiliki NDVI rendah (±0–0,2), sedangkan air dan awan cenderung negatif atau mendekati nol.\n\nPengecoh: 0,40 adalah selisih NIR dan Red (pembilang saja). 1,50 berasal dari pembagian yang keliru; NDVI hanya bernilai −1 sampai +1. −0,67 membalik urutan pengurangan. 0,60 adalah penyebut saja.",
      None),
    Q("Perhatikan grafik NDVI rata-rata sebuah petak lahan berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Hutan dibuka pada 2019, lalu vegetasi tumbuh kembali secara bertahap", "Vegetasi semakin rapat sejak 2015 hingga mencapai puncak pada 2024",
       "Petak lahan berubah menjadi badan air permanen sejak tahun 2019", "NDVI turun karena musim hujan sehingga daun menjadi lebih hijau",
       "Petak lahan selalu berupa permukiman padat sepanjang 2015–2024"],
      "Grafik menunjukkan NDVI stabil tinggi (±0,82) pada 2015–2018, menandakan vegetasi rapat seperti hutan. Pada awal 2019 NDVI turun tajam menjadi ±0,15, menandakan vegetasi hilang secara tiba-tiba, misalnya akibat pembukaan lahan atau kebakaran. Setelah itu NDVI naik perlahan hingga ±0,55 pada 2024, menunjukkan tumbuhnya vegetasi baru, misalnya tanaman perkebunan muda atau suksesi semak belukar.\nAnalisis deret waktu NDVI seperti ini dipakai untuk memantau deforestasi dan pemulihan lahan.\n\nPengecoh: vegetasi tidak semakin rapat sejak 2015. Badan air memiliki NDVI negatif, sedangkan nilai pada grafik tetap positif dan naik. Musim hujan justru menaikkan NDVI. Permukiman padat memiliki NDVI rendah sepanjang waktu, tidak tinggi seperti 2015–2018.",
      f_ndvi),
    Q("Kemampuan lahan (land capability) dibedakan dari kesesuaian lahan (land suitability). Pernyataan yang tepat adalah …",
      ["Kemampuan menilai potensi lahan secara umum; kesesuaian menilai kecocokan penggunaan tertentu",
       "Kemampuan lahan menilai kecocokan untuk satu jenis tanaman tertentu, seperti padi atau kopi",
       "Kesesuaian lahan hanya mempertimbangkan kemiringan lereng tanpa faktor tanah dan iklim",
       "Keduanya sama persis sehingga dapat digunakan secara bergantian tanpa perbedaan",
       "Kesesuaian lahan selalu lebih rendah kelasnya daripada kemampuan lahan di semua lokasi"],
      "Kemampuan lahan adalah penilaian potensi lahan untuk penggunaan secara umum (pertanian intensif, terbatas, padang rumput, hutan, atau lindung) berdasarkan faktor penghambat seperti lereng, erosi, kedalaman tanah, drainase, dan iklim. Hasilnya berupa kelas I–VIII.\nKesesuaian lahan adalah penilaian kecocokan lahan untuk jenis penggunaan atau komoditas tertentu, misalnya kesesuaian untuk padi sawah, kopi arabika, atau tambak, dengan kelas seperti S1 (sangat sesuai), S2, S3, dan N (tidak sesuai).\nKeduanya dipakai bersama dalam perencanaan tata ruang dan pertanian.\n\nPengecoh: opsi kedua menukar definisi. Kesesuaian lahan mempertimbangkan banyak faktor, tidak hanya lereng. Keduanya berbeda. Tidak ada aturan bahwa kesesuaian selalu lebih rendah.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
