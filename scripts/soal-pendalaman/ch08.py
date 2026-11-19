from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_weber(path):
    fig, ax = blank(8, 5.6, (0, 100), (0, 70))
    pts = {"M₁ (bijih)": (12, 12), "M₂ (batu bara)": (88, 12), "P (pasar)": (50, 62)}
    xs = [p[0] for p in pts.values()] + [12]; ys = [p[1] for p in pts.values()] + [12]
    ax.plot(xs, ys, color="#A0AEC0", lw=1.5, ls="--")
    for n, (x, y) in pts.items():
        ax.plot(x, y, "s", ms=14, color=C["orange"] if "M" in n else C["blue"]); ax.text(x, y - 6 if y < 30 else y + 4, n, ha="center", fontsize=11, fontweight="bold")
    ax.text(12, 2, "4 ton per ton produk", ha="center", fontsize=9); ax.text(88, 2, "2 ton per ton produk", ha="center", fontsize=9)
    ax.text(50, 54, "produk akhir: 1 ton", ha="center", fontsize=9)
    ax.set_title("Segitiga lokasi Weber untuk industri baja (disederhanakan)")
    save(fig, path)


def f_lq(path):
    table([["Pertanian", "40.000", "30%"], ["Industri pengolahan", "20.000", "25%"], ["Perdagangan & jasa", "40.000", "45%"], ["Total", "100.000", "100%"]],
          ["Sektor", "Tenaga kerja Kab. K", "Porsi nasional"], path, title="Struktur tenaga kerja Kabupaten K dan nasional",
          col_w=[0.36, 0.32, 0.32])


def f_isodapan(path):
    fig, ax = blank(8, 6, (-50, 50), (-42, 42))
    for r, c in [(12, "10"), (24, "20"), (36, "30"), (46, "40")]:
        ax.add_patch(Circle((0, 0), r, fc="none", ec=C["red"] if c == "30" else "#A0AEC0", lw=2.2 if c == "30" else 1.2, ls="-" if c == "30" else "--"))
        ax.text(r * 0.72, r * 0.72, f"+{c}", fontsize=10, color=C["red"] if c == "30" else C["gray"])
    ax.plot(0, 0, "*", ms=18, color="black"); ax.text(2, -4, "O (lokasi biaya angkut minimum)", fontsize=9)
    for n, (x, y) in {"L₁": (-17, 10), "L₂": (28, -26)}.items():
        ax.plot(x, y, "o", ms=10, color=C["blue"]); ax.text(x + 2, y + 2, n, fontsize=13, fontweight="bold", color=C["blue"])
    ax.text(-48, -40, "Angka = tambahan biaya angkut per unit (ribu Rp) bila pabrik pindah dari O", fontsize=9)
    ax.set_title("Isodapan di sekitar lokasi optimum O")
    save(fig, path)


def f_neraca(path):
    yr = [2019, 2020, 2021, 2022, 2023, 2024]
    bars([str(y) for y in yr], {"Ekspor": [168, 163, 231, 292, 259, 264], "Impor": [171, 141, 196, 237, 222, 233]}, path,
         title="Ekspor dan impor barang Negara N (miliar USD; ilustrasi)", ylabel="miliar USD", values=True, ylim=(0, 330), w=9)


CHOKE = {"P": (101, 2.5), "Q": (56.5, 26.5), "R": (32.5, 30.5), "S": (-79.7, 9.1), "T": (43.4, 12.6)}


def f_choke(path):
    fig, ax = world_map(extent=(-110, 150, -20, 50), w=10.5, h=4.4)
    for n, (x, y) in CHOKE.items():
        ax.plot(x, y, "o", ms=10, color=C["red"], mec="white"); ax.text(x + 2.5, y + 2.5, n, fontsize=14, fontweight="bold", color=C["red"],
                                                                          bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Lima titik sempit (chokepoint) jalur pelayaran dunia")
    save(fig, path)


def f_smile(path):
    st = ["Riset &\npengembangan", "Desain", "Komponen\nutama", "Perakitan", "Distribusi", "Pemasaran &\nmerek", "Layanan\npurnajual"]
    v = [9, 8, 5, 1.5, 4.5, 8.5, 7.5]
    fig, ax = new(9.5, 4.6)
    xs = np.arange(len(st)); xx = np.linspace(0, len(st) - 1, 200)
    ax.plot(xx, np.interp(xx, xs, v), color=C["blue"], lw=2.6); ax.plot(xs, v, "o", color=C["blue"])
    for i, l in enumerate("KLMNOPQ"):
        ax.text(i, v[i] + 0.5, l, ha="center", fontsize=13, fontweight="bold", color=C["red"])
    ax.set_xticks(xs); ax.set_xticklabels(st, fontsize=9); ax.set_ylabel("Nilai tambah relatif"); ax.set_yticks([]); ax.set_ylim(0, 11)
    ax.set_title("Kurva senyum (smile curve) rantai nilai produk elektronik")
    save(fig, path)


# ---- paket 1
def f_hexagon(path):
    fig, ax = blank(7, 6, (-5, 5), (-4.5, 4.5))
    from matplotlib.patches import RegularPolygon
    for q in range(-3, 4):
        for r in range(-3, 4):
            x = 1.5 * q; y = np.sqrt(3) * (r + q / 2)
            if abs(x) < 5 and abs(y) < 4.6:
                ax.add_patch(RegularPolygon((x, y), 6, radius=1, orientation=np.pi / 6, fc="#EBF8FF", ec=C["blue"]))
                ax.plot(x, y, "o", ms=4, color=C["red"])
    ax.set_title("Pola wilayah pasar menurut Lösch (titik = pusat penjualan)")
    save(fig, path)


def f_market(path):
    x = np.linspace(0, 50, 100)
    fig, ax = new(8.5, 4.4)
    ax.plot(x, 100 + 2 * x, color=C["blue"], lw=2.4, label="Harga sampai di konsumen dari pabrik A (p = 100)")
    ax.plot(x, 120 + 2 * (50 - x), color=C["orange"], lw=2.4, label="Harga sampai di konsumen dari pabrik B (p = 120)")
    ax.set_xlabel("Jarak dari pabrik A (km); pabrik B berada di km 50"); ax.set_ylabel("Harga sampai di konsumen (ribu Rp)")
    ax.legend(frameon=False, fontsize=9, loc="upper center"); ax.set_ylim(90, 250); ax.grid(color="#EDF2F7")
    ax.set_title("Harga sampai dua pabrik semen (ongkos angkut 2 ribu Rp/km)")
    save(fig, path)


def f_klaster(path):
    fig, ax = indonesia_map(w=10, h=4.6)
    pts = {"P": (107.3, -6.3), "Q": (112.6, -7.2), "R": (104.0, 1.1), "S": (122.0, -2.8), "T": (117.2, -0.5)}
    for n, (x, y) in pts.items():
        ax.plot(x, y, "o", ms=10, color=C["red"], mec="white"); ax.text(x + 0.6, y + 0.6, n, fontsize=13, fontweight="bold", color=C["red"],
                                                                         bbox=dict(fc="white", ec="none", pad=1))
    ax.set_title("Beberapa klaster industri di Indonesia")
    save(fig, path)


def f_smith(path):
    x = np.linspace(0, 100, 200)
    cost = 60 + 0.012 * (x - 45) ** 2
    fig, ax = new(8.5, 4.4)
    ax.plot(x, cost, color=C["red"], lw=2.4, label="Biaya rata-rata per unit")
    ax.axhline(75, color=C["blue"], lw=2.4, label="Pendapatan rata-rata per unit")
    xm = [45 - np.sqrt(15 / 0.012), 45 + np.sqrt(15 / 0.012)]
    for m in xm:
        ax.axvline(m, color=C["gray"], ls="--")
    ax.fill_between(x, cost, 75, where=cost < 75, color="#C6F6D5")
    for n, xx in {"K": 5, "L": 30, "M": 45, "N": 70, "O": 95}.items():
        ax.plot(xx, 60 + 0.012 * (xx - 45) ** 2, "o", color="black"); ax.text(xx, 60 + 0.012 * (xx - 45) ** 2 - 4.5, n, ha="center", fontsize=12, fontweight="bold")
    ax.set_xlabel("Lokasi sepanjang suatu garis wilayah"); ax.set_ylabel("Rupiah per unit"); ax.set_ylim(50, 100)
    ax.legend(frameon=False, loc="upper center"); ax.set_title("Model batas spasial keuntungan (spatial margin)")
    save(fig, path)


def f_im(path):
    table([["Semen", "1,6 ton batu kapur + tanah liat", "1 ton semen", "1,6"], ["Roti", "0,6 ton tepung + bahan lain", "1 ton roti*", "0,6"],
           ["Gula tebu", "8 ton tebu", "1 ton gula", "8,0"]], ["Industri", "Bahan baku terlokalisasi", "Produk", "Indeks material"], path,
          title="Indeks material tiga industri (*sebagian berat roti dari air)", col_w=[0.16, 0.42, 0.2, 0.22], fs=10.5)


# ---- paket 2
def f_struktur(path):
    bars(["1970", "1990", "2010", "2023"], {"Pertanian": [45, 22, 14, 12], "Industri pengolahan": [10, 21, 22, 19], "Pertambangan & lainnya": [10, 17, 22, 24],
                                             "Jasa & perdagangan": [35, 40, 42, 45]}, path, title="Struktur PDB Indonesia menurut sektor (%; disederhanakan)",
         ylabel="%", stacked=True, values=True, ylim=(0, 165), colors=[C["green"], C["blue"], C["gray"], C["orange"]], w=8.5, legend_loc="upper center")


def f_shift(path):
    table([["Tenaga kerja sektor elektronik Kabupaten E tahun awal", "1.000 orang"], ["Pertumbuhan tenaga kerja nasional (semua sektor), g", "5%"],
           ["Pertumbuhan sektor elektronik nasional, gᵢ", "8%"], ["Pertumbuhan sektor elektronik Kabupaten E, gᵢⱼ", "12%"]],
          ["Data", "Nilai"], path, title="Data analisis shift-share sektor elektronik", col_w=[0.72, 0.28], fs=10.5)


def f_pdrb(path):
    table([["A", "300", "15"], ["B", "120", "3"], ["C", "900", "50"]], ["Provinsi", "PDRB (triliun Rp)", "Penduduk (juta jiwa)"], path,
          title="PDRB dan penduduk tiga provinsi", col_w=[0.24, 0.38, 0.38])


LQS = {"Pertanian": 0.6, "Pertambangan": 2.4, "Industri": 1.3, "Konstruksi": 0.9, "Perdagangan": 0.8, "Pariwisata": 1.1}


def f_lqbar(path):
    bars(list(LQS), {"LQ": list(LQS.values())}, path, title="Location Quotient sektor-sektor Kabupaten T", ylabel="LQ", values=True, ylim=(0, 2.8),
         hline=1, colors=[C["teal"]], rot=12, w=8.5)


def f_ekspor(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [18, 11, 10, 8, 6, 47]; lab = ["Batu bara", "Minyak sawit", "Besi & baja", "Produk nikel", "Elektronik", "Lainnya"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=["#2D3748", "#DD6B20", "#718096", "#2C7A7B", "#3182CE", "#CBD5E0"], startangle=90,
           wedgeprops=dict(ec="white"), textprops=dict(fontsize=10))
    ax.set_title("Komposisi nilai ekspor barang Indonesia (ilustrasi)")
    save(fig, path)


# ---- paket 3
def f_komparatif(path):
    table([["Negara A", "2 jam", "4 jam"], ["Negara B", "6 jam", "6 jam"]], ["Negara", "1 unit kain", "1 unit beras"], path,
          title="Jam kerja yang diperlukan untuk menghasilkan satu unit barang", col_w=[0.24, 0.38, 0.38])


def f_xm(path):
    yr = ["2020", "2021", "2022", "2023"]
    bars(yr, {"Ekspor": [163, 231, 292, 259], "Impor": [141, 196, 237, 222]}, path, title="Ekspor dan impor Negara M (miliar USD; ilustrasi)",
         ylabel="miliar USD", values=True, ylim=(0, 330), w=8)


def f_diversion(path):
    table([["Negara X (bukan anggota FTA)", "90", "20%", "108"], ["Negara Y (anggota FTA)", "100", "0%", "100"]],
          ["Pemasok", "Harga asal", "Tarif di Z", "Harga di Z"], path,
          title="Harga barang di Negara Z setelah FTA dengan Negara Y", col_w=[0.34, 0.22, 0.22, 0.22], fs=10.5)


def f_tot(path):
    yr = [2016, 2018, 2020, 2022, 2024]
    fig, ax = new(8.5, 4.4)
    pe = [100, 112, 98, 150, 125]; pi = [100, 108, 104, 120, 122]
    ax.plot(yr, pe, marker="o", lw=2.2, color=C["blue"], label="Indeks harga ekspor")
    ax.plot(yr, pi, marker="s", lw=2.2, color=C["orange"], label="Indeks harga impor")
    ax.set_xticks(yr); ax.legend(frameon=False); ax.grid(color="#EDF2F7"); ax.set_ylabel("indeks (2016 = 100)")
    ax.set_title("Indeks harga ekspor dan impor Negara R")
    save(fig, path)


RCEP = ["CHN", "JPN", "KOR", "AUS", "NZL", "IDN", "MYS", "SGP", "THA", "PHL", "VNM", "BRN", "KHM", "LAO", "MMR"]


def f_rcep(path):
    col = {c: "#68D391" for c in RCEP}
    fig, ax = world_map(extent=(70, 180, -50, 55), colors=col, w=8.5, h=6.5)
    ax.set_title("Negara-negara anggota sebuah perjanjian perdagangan regional (hijau)")
    save(fig, path)


# ---- paket 4
def f_fdi(path):
    bars(["Logam dasar\n& smelter", "Pertambangan", "Kimia &\nfarmasi", "Transportasi\n& gudang", "Perumahan &\nkawasan industri"], {"Realisasi PMA (miliar USD)": [11.0, 5.2, 4.1, 3.8, 3.1]},
         path, title="Realisasi penanaman modal asing menurut sektor (ilustrasi)", ylabel="miliar USD", values=True, ylim=(0, 13), colors=[C["purple"]], w=9)


def f_ponsel(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [58, 14, 10, 5, 2, 11]; lab = ["Keuntungan pemilik merek\n& desain (AS)", "Komponen\n(Korea Selatan)", "Komponen\n(Jepang & Taiwan)", "Bahan mentah",
                                       "Perakitan\n(Tiongkok)", "Distribusi & lainnya"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=["#2B6CB0", "#63B3ED", "#90CDF4", "#A0AEC0", "#E53E3E", "#CBD5E0"], startangle=90,
           wedgeprops=dict(ec="white"), textprops=dict(fontsize=9))
    ax.set_title("Pembagian nilai satu unit telepon pintar (ilustrasi)")
    save(fig, path)


def f_rantai(path):
    fig, ax = blank(10, 4.6, (0, 100), (0, 46))
    sup = [("Jepang:\nmesin & transmisi", 4, 34), ("Thailand:\nsuku cadang", 4, 20), ("Taiwan:\ncip semikonduktor", 4, 6)]
    for t, x, y in sup:
        box(ax, x, y, 24, 9, t, fc="#EBF8FF", fs=9)
        arrow(ax, 29, y + 4.5, 43, 23, color=C["gray"])
    box(ax, 44, 17, 22, 12, "Perakitan mobil\ndi Karawang", fc="#FEFCBF", fs=10, bold=True)
    arrow(ax, 67, 23, 78, 23, color=C["gray"])
    box(ax, 79, 17, 19, 12, "Pasar domestik\n& ekspor", fc="#C6F6D5", fs=10)
    ax.text(16.5, 2, "pemasok cip tunggal", ha="center", fontsize=9, color=C["red"])
    ax.set_title("Rantai pasok sebuah pabrik perakitan mobil")
    save(fig, path)


def f_pelabuhan(path):
    bars(["Shanghai", "Singapura", "Ningbo", "Busan", "Rotterdam", "Tanjung Priok"], {"Juta TEU per tahun": [47, 39, 35, 23, 14, 7]}, path,
         title="Arus peti kemas beberapa pelabuhan (ilustrasi)", ylabel="juta TEU", values=True, ylim=(0, 55), colors=[C["blue"]], rot=10, w=8.5)


def f_investasi(path):
    lines([2015, 2017, 2019, 2021, 2023], {"Jawa": [54, 51, 47, 46, 44], "Luar Jawa": [46, 49, 53, 54, 56]}, path,
          title="Porsi realisasi investasi menurut lokasi (%; ilustrasi)", xlabel="Tahun", ylabel="% dari total investasi", w=8.5)


# ---- paket 5
def f_porsi(path):
    lines([2017, 2018, 2019, 2020, 2021, 2022, 2023], {"Tiongkok": [21.6, 21.2, 18.1, 18.6, 17.9, 16.5, 13.9], "Meksiko": [13.4, 13.6, 14.3, 13.9, 13.6, 14.0, 15.4],
                                                       "Vietnam": [2.0, 2.0, 2.7, 3.4, 3.6, 3.8, 3.6]}, path,
          title="Porsi impor barang Amerika Serikat menurut asal (%; disederhanakan)", xlabel="Tahun", ylabel="%", w=9)


def f_minyak(path):
    bars(["Selat Hormuz", "Selat Malaka", "Terusan Suez &\nSUMED", "Bab el-Mandeb", "Terusan Panama"], {"Juta barel per hari": [21, 16, 9, 6, 1]}, path,
         title="Aliran minyak melalui titik sempit maritim (ilustrasi)", ylabel="juta barel per hari", values=True, ylim=(0, 25), colors=[C["gray"]], w=9)


def f_gmv(path):
    bars(["2019", "2020", "2021", "2022", "2023"], {"Nilai transaksi (miliar USD)": [40, 47, 70, 77, 82]}, path,
         title="Nilai transaksi ekonomi digital sebuah negara (ilustrasi)", ylabel="miliar USD", values=True, ylim=(0, 95), colors=[C["purple"]], w=8)


def f_nilaitambah(path):
    table([["Bijih nikel (kadar ±1,8%)", "±40"], ["Nickel pig iron (NPI)", "±1.500"], ["Baja nirkarat (stainless steel)", "±2.500"],
           ["Prekursor/katode baterai", "±25.000"]], ["Tahap produk", "Nilai per ton (USD; ilustrasi)"], path,
          title="Nilai produk pada beberapa tahap hilirisasi nikel", col_w=[0.6, 0.4])


def f_smelter(path):
    fig, ax = indonesia_map(extent=(115, 132, -7, 3.5), w=9, h=5.6)
    for n, (x, y) in {"Morowali": (122.0, -2.8), "Weda Bay": (127.9, 0.45), "Konawe": (122.3, -3.9), "Pomalaa": (121.6, -4.2), "Obi": (127.6, -1.5)}.items():
        ax.plot(x, y, "^", ms=12, color=C["red"], mec="black"); ax.text(x + 0.25, y + 0.25, n, fontsize=10, fontweight="bold")
    ax.set_title("Lokasi utama kawasan smelter nikel")
    save(fig, path)


# ============================ questions ============================
P0 = [
    Q("Perhatikan segitiga lokasi Weber untuk industri baja berikut. Setiap ton baja memerlukan 4 ton bijih dan 2 ton batu bara, keduanya bahan baku terlokalisasi.\n\nIndeks material dan kecenderungan lokasi industri tersebut adalah …",
      ["IM = 6; berorientasi bahan baku", "IM = 6; berorientasi pasar", "IM = 0,17; berorientasi pasar", "IM = 2; berorientasi tenaga kerja",
       "IM = 1; lokasi bebas di mana saja"],
      "Indeks material (IM) = berat bahan baku terlokalisasi ÷ berat produk = (4 + 2) ÷ 1 = 6.\nKarena IM > 1, proses produksi mengurangi berat (weight-losing). Mengangkut bahan baku jauh lebih mahal daripada mengangkut produk, sehingga lokasi optimum cenderung mendekati sumber bahan baku, terutama bahan yang paling berat (bijih). Itulah sebabnya pabrik baja dan smelter sering dibangun dekat tambang atau pelabuhan bahan baku.\n\nPengecoh: IM 6 tidak berorientasi pasar; orientasi pasar terjadi bila IM < 1 (weight-gaining). 0,17 membalik pembagian. IM 2 dan IM 1 berasal dari perhitungan keliru. Orientasi tenaga kerja dalam teori Weber adalah penyimpangan dari lokasi biaya angkut minimum, bukan ditentukan oleh IM.",
      f_weber),
    Q("Sebuah perusahaan konsultan perangkat lunak yang menjual jasa analisis data dan riset pasar tergolong dalam sektor ekonomi …",
      ["Kuarter", "Primer", "Sekunder", "Tersier sederhana", "Primer dan sekunder"],
      "Klasifikasi sektor ekonomi:\n• Primer: mengambil langsung dari alam, misalnya pertanian, perikanan, kehutanan, dan pertambangan.\n• Sekunder: mengolah bahan mentah menjadi barang jadi, misalnya industri manufaktur dan konstruksi.\n• Tersier: menyediakan jasa, misalnya perdagangan, transportasi, dan pariwisata.\n• Kuarter: jasa berbasis pengetahuan dan informasi, misalnya riset, teknologi informasi, konsultansi, dan pengembangan perangkat lunak (sering ditambah kuiner untuk pengambil keputusan tingkat tinggi).\nPerusahaan konsultan perangkat lunak dan riset data termasuk sektor kuarter.\n\nPengecoh: kegiatan tersebut tidak mengambil dari alam atau mengolah bahan mentah, dan bukan jasa sederhana seperti perdagangan eceran.",
      None),
    Q("Perhatikan struktur tenaga kerja Kabupaten K dan nasional berikut. Dengan LQ = (sᵢ ÷ s) ÷ (Sᵢ ÷ S), sektor basis Kabupaten K adalah …",
      ["Pertanian, dengan LQ sekitar 1,33", "Industri pengolahan, dengan LQ sekitar 0,80", "Perdagangan & jasa, dengan LQ sekitar 0,89",
       "Pertanian, dengan LQ sekitar 0,75", "Semua sektor karena porsinya di atas 20%"],
      "Hitung LQ tiap sektor (porsi kabupaten ÷ porsi nasional):\n• Pertanian: (40.000 ÷ 100.000) ÷ 30% = 0,40 ÷ 0,30 ≈ 1,33.\n• Industri: 0,20 ÷ 0,25 = 0,80.\n• Perdagangan & jasa: 0,40 ÷ 0,45 ≈ 0,89.\nLQ > 1 berarti sektor tersebut lebih terkonsentrasi di kabupaten daripada rata-rata nasional, sehingga dianggap sektor basis yang menghasilkan barang atau jasa untuk \"diekspor\" ke luar wilayah dan mendatangkan pendapatan. Sektor basis Kabupaten K adalah pertanian.\n\nPengecoh: industri dan jasa memiliki LQ < 1. LQ 0,75 membalik pembagian. Porsi besar dalam ekonomi lokal tidak otomatis menjadi basis; yang dibandingkan adalah porsi relatif terhadap nasional.",
      f_lq),
    Q("Dua penjual es krim di sepanjang pantai lurus awalnya berada di seperempat dan tiga perempat panjang pantai. Menurut model Hotelling, dalam persaingan bebas keduanya cenderung …",
      ["Berpindah mendekat ke tengah pantai hingga berdampingan", "Berpindah ke kedua ujung pantai agar saling menjauh",
       "Tetap di posisi semula karena sudah membagi pasar sama besar", "Berpindah ke luar pantai karena pasar sudah jenuh",
       "Bergabung menjadi satu perusahaan untuk menghindari persaingan"],
      "Model Hotelling (1929) mengasumsikan konsumen tersebar merata dan memilih penjual terdekat. Bila salah satu penjual bergeser sedikit ke tengah, ia merebut pelanggan di antara kedua penjual tanpa kehilangan pelanggan di sisinya sendiri. Penjual lainnya akan membalas dengan bergeser juga. Proses ini berlanjut hingga keduanya berdampingan di tengah pantai.\nModel ini menjelaskan mengapa toko sejenis, SPBU, atau minimarket sering berlokasi berdekatan, serta mengapa partai politik cenderung mendekati posisi tengah (pemilih median). Secara sosial, posisi ini kurang efisien karena konsumen di ujung pantai harus berjalan lebih jauh.\n\nPengecoh: saling menjauh tidak stabil dalam model ini. Posisi awal yang efisien secara sosial tidak bertahan dalam persaingan. Model tidak menyatakan keluar pasar atau merger.",
      None),
    Q("Perhatikan isodapan di sekitar lokasi optimum O berikut. Di lokasi L₁ dan L₂ terdapat tenaga kerja murah yang menghemat biaya upah sebesar 30 ribu Rp per unit produk.\n\nKeputusan relokasi yang paling menguntungkan adalah …",
      ["Pindah ke L₁, karena tambahan biaya angkut kurang dari penghematan upah", "Pindah ke L₂, karena penghematan upah selalu lebih penting daripada biaya angkut",
       "Pindah ke L₁ atau L₂ sama saja karena penghematan upahnya sama", "Tetap di O karena biaya angkut selalu menentukan lokasi",
       "Pindah ke L₂, karena tambahan biaya angkutnya paling kecil"],
      "Dalam teori Weber, pabrik akan menyimpang dari lokasi biaya angkut minimum (O) ke lokasi tenaga kerja murah bila penghematan upah lebih besar daripada tambahan biaya angkut. Isodapan adalah garis yang menghubungkan titik-titik dengan tambahan biaya angkut yang sama. Isodapan kritis adalah isodapan yang nilainya sama dengan penghematan upah, yaitu +30.\n• L₁ berada di dalam isodapan +20 (tambahan biaya ±20 < 30) → relokasi menguntungkan.\n• L₂ berada di antara isodapan +30 dan +40 (tambahan biaya > 30) → tidak menguntungkan.\nJadi pabrik sebaiknya pindah ke L₁.\n\nPengecoh: penghematan upah tidak selalu mengalahkan biaya angkut. L₁ dan L₂ tidak sama karena tambahan biaya angkutnya berbeda. Tetap di O merugikan karena L₁ lebih hemat. Tambahan biaya angkut L₂ justru lebih besar.",
      f_isodapan),
    Q("Negara A memerlukan 2 jam kerja untuk 1 unit kain dan 4 jam untuk 1 unit beras, sedangkan Negara B memerlukan 6 jam untuk kain dan 6 jam untuk beras. Menurut teori keunggulan komparatif, spesialisasi yang tepat adalah …",
      ["A berspesialisasi kain dan B berspesialisasi beras", "A berspesialisasi beras dan B berspesialisasi kain", "A memproduksi keduanya, B tidak memproduksi apa pun",
       "B berspesialisasi kain karena waktunya sama dengan beras", "Tidak ada perdagangan karena A unggul mutlak pada kedua barang"],
      "Negara A unggul mutlak pada kedua barang (lebih sedikit jam kerja). Namun spesialisasi ditentukan oleh keunggulan komparatif, yaitu biaya peluang terendah.\n• Biaya peluang 1 unit kain: A = 2 ÷ 4 = 0,5 unit beras; B = 6 ÷ 6 = 1 unit beras → A lebih murah membuat kain.\n• Biaya peluang 1 unit beras: A = 4 ÷ 2 = 2 unit kain; B = 6 ÷ 6 = 1 unit kain → B lebih murah membuat beras.\nJadi A berspesialisasi kain dan B berspesialisasi beras, lalu keduanya berdagang sehingga total produksi dan kesejahteraan meningkat (teori David Ricardo).\n\nPengecoh: opsi kedua membalik spesialisasi. Keunggulan mutlak tidak menghalangi perdagangan yang saling menguntungkan.",
      None),
    Q("Perhatikan grafik ekspor dan impor barang Negara N berikut.\n\nTahun ketika Negara N mengalami defisit neraca perdagangan adalah …",
      ["2019", "2020", "2022", "2023", "2024"],
      "Neraca perdagangan = ekspor − impor.\n• 2019: 168 − 171 = −3 miliar USD (defisit).\n• 2020: 163 − 141 = +22 (surplus).\n• 2021: 231 − 196 = +35 (surplus).\n• 2022: 292 − 237 = +55 (surplus terbesar).\n• 2023: 259 − 222 = +37 (surplus).\n• 2024: 264 − 233 = +31 (surplus).\nHanya tahun 2019 yang defisit. Surplus besar pada 2021–2022 banyak dipengaruhi lonjakan harga komoditas ekspor seperti batu bara dan minyak sawit.\n\nPengecoh: tahun-tahun lainnya surplus karena ekspor lebih besar daripada impor. Perhatikan bahwa nilai ekspor yang turun (misalnya 2020) tidak otomatis berarti defisit; yang menentukan adalah selisihnya dengan impor.",
      f_neraca),
    Q("Indeks harga ekspor sebuah negara naik menjadi 120, sedangkan indeks harga impornya naik menjadi 150 (tahun dasar = 100). Nilai terms of trade dan interpretasinya adalah …",
      ["80; posisi dagang memburuk", "125; posisi dagang membaik", "80; posisi dagang membaik",
       "270; volume perdagangan meningkat tajam", "30; selisih harga impor dan ekspor"],
      "Terms of trade (ToT) = indeks harga ekspor ÷ indeks harga impor × 100 = 120 ÷ 150 × 100 = 80.\nNilai di bawah 100 berarti harga impor naik lebih cepat daripada harga ekspor, sehingga untuk membeli jumlah impor yang sama, negara harus mengekspor lebih banyak barang. Posisi dagang negara tersebut memburuk. Hal ini sering dialami negara pengekspor komoditas mentah ketika harga barang manufaktur impor naik lebih cepat.\n\nPengecoh: 125 membalik pembagian. Nilai di bawah 100 menandakan memburuk, bukan membaik. 270 menjumlahkan indeks. 30 hanya selisih, bukan ToT.",
      None),
    Q("Perhatikan peta lima titik sempit (chokepoint) jalur pelayaran dunia berikut.\n\nTitik sempit yang menghubungkan Samudra Hindia dengan Laut Cina Selatan dan menjadi jalur utama perdagangan Asia Timur–Timur Tengah adalah …",
      ["P, Selat Malaka", "Q, Selat Hormuz", "R, Terusan Suez", "S, Terusan Panama", "T, Bab el-Mandeb"],
      "Titik-titik pada peta:\n• P: Selat Malaka, antara Semenanjung Malaya dan Sumatra, menghubungkan Samudra Hindia dengan Laut Cina Selatan; dilalui puluhan ribu kapal per tahun, termasuk pasokan minyak ke Tiongkok, Jepang, dan Korea Selatan.\n• Q: Selat Hormuz, pintu keluar Teluk Persia.\n• R: Terusan Suez, menghubungkan Laut Merah dengan Laut Tengah.\n• S: Terusan Panama, menghubungkan Samudra Atlantik dan Pasifik.\n• T: Bab el-Mandeb, antara Yaman dan Tanduk Afrika, menghubungkan Laut Merah dengan Teluk Aden.\nLetak Indonesia di sekitar Selat Malaka, Selat Sunda, dan Selat Lombok memberi nilai geostrategis yang tinggi.\n\nPengecoh: opsi lain menukar lokasi titik sempit.",
      f_choke),
    Q("Perhatikan kurva senyum rantai nilai produk elektronik berikut.\n\nTahap dengan nilai tambah terendah yang sering ditempatkan di negara berupah rendah adalah …",
      ["N, perakitan", "K, riset dan pengembangan", "P, pemasaran dan merek", "L, desain", "Q, layanan purnajual"],
      "Kurva senyum (smile curve) menggambarkan bahwa nilai tambah terbesar dalam rantai nilai global berada di kedua ujung rantai, yaitu kegiatan pra-produksi (riset, pengembangan, desain) dan pasca-produksi (pemasaran, merek, layanan). Tahap tengah, terutama perakitan (N), memiliki nilai tambah paling rendah karena bersifat padat karya, mudah ditiru, dan bersaing ketat. Karena itu perakitan sering dipindahkan ke negara berupah rendah, sedangkan riset dan merek tetap dikuasai negara maju.\nImplikasinya, negara berkembang perlu naik kelas (upgrading) ke tahap bernilai tambah tinggi agar tidak terjebak sebagai perakit saja.\n\nPengecoh: K, L, P, dan Q berada di ujung kurva dengan nilai tambah tinggi.",
      f_smile),
]

P1 = [
    Q("Perhatikan pola wilayah pasar menurut Lösch berikut.\n\nAlasan wilayah pasar digambarkan berbentuk segi enam (heksagon) adalah …",
      ["Heksagon menutup seluruh ruang tanpa celah dan paling mendekati lingkaran", "Heksagon adalah bentuk wilayah administrasi kabupaten di Jerman",
       "Lingkaran lebih efisien tetapi tidak dapat digambar di peta", "Heksagon membuat setiap konsumen dilayani oleh dua penjual sekaligus",
       "Bentuk heksagon terjadi karena jalan raya selalu bersudut 60°"],
      "Dalam model Lösch, setiap penjual melayani wilayah pasar di sekitarnya hingga jarak tertentu (batas ketika biaya angkut membuat harga terlalu mahal). Wilayah pasar ideal berbentuk lingkaran, tetapi susunan lingkaran meninggalkan celah (wilayah tidak terlayani) atau tumpang tindih. Heksagon adalah bentuk yang dapat menutup bidang tanpa celah dan tanpa tumpang tindih sekaligus paling mendekati lingkaran, sehingga jarak rata-rata konsumen ke penjual paling kecil. Gagasan serupa dipakai Christaller dalam teori tempat sentral.\n\nPengecoh: bentuk heksagon bukan berasal dari batas administrasi atau sudut jalan. Lingkaran meninggalkan celah sehingga bukan yang paling efisien untuk menutup ruang. Dalam heksagon, setiap konsumen dilayani satu penjual terdekat.",
      f_hexagon),
    Q("Industri garmen dan alas kaki banyak berlokasi di kabupaten dengan upah minimum rendah, seperti di Jawa Tengah. Industri seperti ini tergolong …",
      ["Industri padat karya yang berorientasi tenaga kerja", "Industri padat modal yang berorientasi pasar", "Industri berorientasi bahan baku karena bahan bakunya berat",
       "Industri footloose yang tidak terikat faktor lokasi apa pun", "Industri ekstraktif yang mengambil bahan langsung dari alam"],
      "Industri garmen dan alas kaki membutuhkan banyak tenaga kerja dengan keterampilan sedang, sedangkan bahan bakunya relatif ringan dan mudah diangkut. Biaya upah menjadi komponen biaya terbesar, sehingga industri ini disebut padat karya dan cenderung berlokasi di daerah dengan upah rendah dan tenaga kerja melimpah. Kenaikan upah minimum di Jabodetabek mendorong relokasi pabrik garmen ke Jawa Tengah seperti Jepara, Kendal, dan Boyolali.\n\nPengecoh: padat modal memerlukan mesin dan modal besar (misalnya petrokimia). Bahan baku garmen tidak berat. Industri footloose relatif bebas memilih lokasi karena biaya angkut dan tenaga kerja tidak dominan, misalnya perangkat lunak. Industri ekstraktif adalah pertambangan atau kehutanan.",
      None),
    Q("Perhatikan grafik harga sampai di konsumen dari dua pabrik semen berikut. Pabrik A menjual pada harga 100 ribu Rp dan pabrik B 120 ribu Rp, dengan ongkos angkut 2 ribu Rp/km, dan jarak kedua pabrik 50 km.\n\nBatas wilayah pasar kedua pabrik terletak pada jarak … dari pabrik A.",
      ["30 km", "25 km", "20 km", "35 km", "10 km"],
      "Batas wilayah pasar berada pada titik ketika harga sampai dari kedua pabrik sama:\n100 + 2x = 120 + 2(50 − x)\n100 + 2x = 220 − 2x\n4x = 120 → x = 30 km dari pabrik A.\nKonsumen yang berjarak kurang dari 30 km dari A membeli dari A, sedangkan konsumen di luar itu (lebih dekat ke B) membeli dari B. Karena harga di pabrik A lebih murah, wilayah pasarnya lebih luas.\n\nPengecoh: 25 km adalah titik tengah, berlaku bila kedua harga pabrik sama. 20 km adalah jarak dari pabrik B. 35 km dan 10 km tidak sesuai perhitungan.",
      f_market),
    Q("Pemerintah menetapkan Kawasan Ekonomi Khusus (KEK) di beberapa daerah dengan berbagai insentif. Tujuan utama kebijakan KEK adalah …",
      ["Menarik investasi dan menumbuhkan pusat pertumbuhan baru", "Menutup daerah tersebut dari perdagangan internasional",
       "Melarang perusahaan asing berinvestasi di Indonesia", "Memindahkan seluruh industri dari Jawa ke kawasan tersebut tanpa insentif",
       "Menghapus pajak di seluruh wilayah Indonesia"],
      "Kawasan Ekonomi Khusus adalah kawasan dengan batas tertentu yang diberi fasilitas dan insentif khusus, seperti keringanan pajak dan bea masuk, kemudahan perizinan, serta infrastruktur terpadu (pelabuhan, energi, air). Tujuannya menarik investasi domestik maupun asing, mendorong industri dan pariwisata, menciptakan lapangan kerja, dan memeratakan pembangunan dengan menumbuhkan pusat pertumbuhan baru di luar Jawa, misalnya KEK Sei Mangkei (Sumatera Utara), KEK Mandalika (NTB), dan KEK Galang Batang (Kepulauan Riau).\n\nPengecoh: KEK justru membuka diri terhadap perdagangan dan investasi asing. Relokasi industri tidak dipaksakan. Insentif pajak hanya berlaku di dalam kawasan.",
      None),
    Q("Perhatikan peta beberapa klaster industri di Indonesia berikut.\n\nKlaster S yang berkembang pesat sejak akhir 2010-an didorong terutama oleh …",
      ["Ketersediaan bijih nikel sebagai bahan baku smelter dan baja nirkarat", "Kedekatan dengan pasar konsumen terbesar di Jabodetabek",
       "Status kawasan perdagangan bebas yang berbatasan langsung dengan Singapura", "Upah buruh paling rendah di seluruh Indonesia untuk industri garmen",
       "Jaringan jalan tol terpanjang di Indonesia"],
      "Klaster pada peta: P = Jabodetabek–Karawang (otomotif, elektronik; dekat pasar terbesar), Q = Gresik–Surabaya (petrokimia, semen), R = Batam (elektronik dan galangan kapal; kawasan perdagangan bebas dekat Singapura), S = Morowali (Sulawesi Tengah), dan T = Kalimantan Timur (energi dan petrokimia).\nKlaster Morowali tumbuh pesat setelah kebijakan larangan ekspor bijih nikel, karena di sekitarnya terdapat cadangan nikel laterit yang besar. Smelter, pabrik baja nirkarat, dan bahan baterai dibangun dekat sumber bijih karena bahan baku sangat berat (berorientasi bahan baku).\n\nPengecoh: pasar terbesar adalah ciri P. Kawasan perdagangan bebas dekat Singapura adalah R. Morowali bukan sentra garmen. Faktor jalan tol tidak menjadi pendorong utama.",
      f_klaster),
    Q("Pabrik di Kota X membayar upah Rp300 ribu per hari dengan produktivitas 10 unit per pekerja per hari, sedangkan di Kota Y upah Rp450 ribu per hari dengan produktivitas 20 unit. Pernyataan yang tepat adalah …",
      ["Biaya per unit Y lebih murah: Rp22.500 dibanding Rp30.000", "Biaya tenaga kerja per unit di X lebih murah karena upahnya lebih rendah",
       "Biaya tenaga kerja per unit di kedua kota sama, yaitu Rp30.000", "Biaya tenaga kerja per unit di Y adalah Rp9.000.000",
       "Produktivitas tidak memengaruhi biaya tenaga kerja per unit"],
      "Biaya tenaga kerja per unit = upah ÷ produktivitas.\n• Kota X: 300.000 ÷ 10 = Rp30.000 per unit.\n• Kota Y: 450.000 ÷ 20 = Rp22.500 per unit.\nWalaupun upah di Y lebih tinggi, produktivitasnya dua kali lipat sehingga biaya per unit justru lebih rendah. Inilah alasan upah rendah saja tidak menjamin daya saing; investor juga memperhatikan keterampilan, teknologi, dan produktivitas tenaga kerja.\n\nPengecoh: upah rendah tidak berarti biaya per unit rendah. Biaya kedua kota tidak sama. Rp9.000.000 adalah perkalian upah dan produktivitas. Produktivitas jelas memengaruhi biaya per unit.",
      None),
    Q("Perhatikan model batas spasial keuntungan berikut.\n\nLokasi yang memberikan keuntungan bagi perusahaan adalah …",
      ["L, M, dan N", "K dan O", "M saja", "Semua lokasi K sampai O", "K, L, N, dan O"],
      "Model batas spasial keuntungan (D. M. Smith) membandingkan pendapatan dan biaya per unit di berbagai lokasi. Perusahaan untung bila pendapatan rata-rata lebih besar daripada biaya rata-rata. Pada grafik, garis pendapatan (75) berada di atas kurva biaya di antara dua garis putus-putus (batas spasial keuntungan), yaitu daerah hijau. Lokasi L, M, dan N berada di dalam batas tersebut sehingga menguntungkan; M adalah lokasi optimum karena biaya terendah. Lokasi K dan O berada di luar batas sehingga merugi.\nModel ini menunjukkan bahwa perusahaan tidak harus berada di titik optimum; cukup berada di dalam batas keuntungan, sehingga faktor pribadi atau perilaku dapat memengaruhi pilihan lokasi.\n\nPengecoh: K dan O merugi. M bukan satu-satunya lokasi untung. Tidak semua lokasi untung.",
      f_smith),
    Q("Perusahaan pengembang aplikasi digital dapat berlokasi di Bandung, Yogyakarta, atau Bali tanpa perbedaan biaya produksi yang berarti. Industri seperti ini disebut …",
      ["Footloose industry", "Industri berorientasi bahan baku", "Industri berat", "Industri ekstraktif", "Industri berorientasi pelabuhan"],
      "Footloose industry adalah industri yang relatif bebas memilih lokasi karena biaya angkut bahan baku dan produk tidak berarti dan tidak bergantung pada sumber daya alam tertentu. Produk digital dapat dikirim melalui internet. Faktor lokasi yang lebih menentukan adalah ketersediaan tenaga kerja terampil, kualitas internet, kualitas hidup, ekosistem startup, dan kedekatan dengan kampus. Karena itu kota pendidikan dan kota dengan suasana menyenangkan seperti Yogyakarta, Bandung, dan Bali menarik bagi pekerja teknologi.\n\nPengecoh: industri berorientasi bahan baku terikat pada sumber bahan berat. Industri berat memerlukan bahan dan mesin berat. Industri ekstraktif mengambil langsung dari alam. Industri berorientasi pelabuhan bergantung pada ekspor-impor curah.",
      None),
    Q("Perhatikan tabel indeks material tiga industri berikut.\n\nIndustri yang paling cenderung berlokasi dekat pasar (konsumen) adalah …",
      ["Roti, karena indeks materialnya kurang dari 1", "Gula tebu, karena indeks materialnya paling besar", "Semen, karena bahan bakunya tersedia di mana-mana",
       "Gula tebu, karena produk gula mudah rusak", "Ketiganya sama karena semuanya industri pengolahan"],
      "Indeks material (IM) = berat bahan baku terlokalisasi ÷ berat produk.\n• Semen (1,6) dan gula tebu (8,0): IM > 1, proses produksi mengurangi berat, sehingga cenderung dekat bahan baku. Pabrik gula selalu berada di dekat kebun tebu karena tebu sangat berat dan cepat rusak setelah ditebang.\n• Roti (0,6): IM < 1 karena sebagian berat produk berasal dari air, bahan yang tersedia di mana-mana (ubiquitous). Produk lebih berat daripada bahan baku terlokalisasi dan juga mudah basi, sehingga pabrik roti cenderung dekat pasar.\n\nPengecoh: IM besar justru menandakan orientasi bahan baku. Bahan baku semen (batu kapur) tidak tersedia di mana-mana. Gula bukan produk yang mudah rusak. Ketiganya memiliki IM berbeda sehingga orientasinya berbeda.",
      f_im),
    Q("Ketika sebuah kawasan industri tumbuh terlalu padat, perusahaan mulai menghadapi kemacetan, harga lahan mahal, kenaikan upah, dan polusi. Gejala ini disebut …",
      ["Disekonomi aglomerasi", "Ekonomi aglomerasi", "Efek tetesan ke bawah", "Keunggulan komparatif", "Integrasi vertikal"],
      "Aglomerasi (pengelompokan kegiatan ekonomi di satu lokasi) memberikan keuntungan berupa ekonomi aglomerasi: berbagi tenaga kerja terampil, pemasok, infrastruktur, dan pertukaran pengetahuan. Namun bila konsentrasi terlalu tinggi, muncul biaya tambahan seperti kemacetan, harga lahan dan sewa yang mahal, kenaikan upah, kelangkaan air, dan polusi. Kondisi ini disebut disekonomi aglomerasi, yang mendorong sebagian perusahaan pindah ke daerah pinggiran atau kota lain, misalnya relokasi pabrik dari Jabodetabek ke Jawa Tengah.\n\nPengecoh: ekonomi aglomerasi adalah keuntungan, bukan biaya. Efek tetesan ke bawah adalah penyebaran manfaat pertumbuhan. Keunggulan komparatif terkait perdagangan. Integrasi vertikal adalah penggabungan tahap produksi dalam satu perusahaan.",
      None),
]

P2 = [
    Q("Perhatikan grafik struktur PDB Indonesia menurut sektor berikut.\n\nGejala yang ditunjukkan grafik disebut …",
      ["Transformasi struktural dari ekonomi pertanian ke industri dan jasa", "Deindustrialisasi dini karena industri menurun sejak 1970",
       "Ruralisasi ekonomi karena pertanian semakin dominan", "Stagnasi ekonomi karena porsi semua sektor tetap",
       "Revolusi Hijau yang membuat pertanian menjadi sektor terbesar"],
      "Grafik menunjukkan porsi pertanian dalam PDB turun dari ±45% (1970) menjadi ±12% (2023), sedangkan industri pengolahan naik dari ±10% menjadi ±19–22% dan jasa serta perdagangan naik dari ±35% menjadi ±45%. Perubahan komposisi ekonomi dari dominasi sektor primer ke sekunder dan tersier ini disebut transformasi struktural, ciri umum negara yang sedang berkembang.\nCatatan analisis: porsi industri sedikit turun setelah 2010 (22% menjadi 19%), yang oleh sebagian ekonom disebut gejala deindustrialisasi dini, tetapi pola utama sejak 1970 tetap transformasi struktural.\n\nPengecoh: industri justru naik sejak 1970. Pertanian semakin kecil, bukan dominan. Porsi sektor jelas berubah. Revolusi Hijau tidak membuat pertanian menjadi sektor terbesar pada periode ini.",
      f_struktur),
    Q("Di sebuah kota, kegiatan ekonomi basis mempekerjakan 40.000 orang dan total tenaga kerja 120.000 orang. Jika sebuah pabrik ekspor baru menambah 5.000 pekerjaan basis, perkiraan tambahan total lapangan kerja di kota tersebut adalah …",
      ["15.000 orang", "5.000 orang", "10.000 orang", "3.000 orang", "40.000 orang"],
      "Pengganda basis = total kegiatan ÷ kegiatan basis = 120.000 ÷ 40.000 = 3.\nArtinya setiap 1 pekerjaan basis (yang menjual ke luar wilayah) menghasilkan total 3 pekerjaan: 1 pekerjaan basis ditambah 2 pekerjaan nonbasis (perdagangan, jasa, transportasi lokal) yang melayani pekerja dan perusahaan basis.\nTambahan 5.000 pekerjaan basis → tambahan total = 5.000 × 3 = 15.000 pekerjaan (5.000 basis + 10.000 nonbasis).\n\nPengecoh: 5.000 hanya menghitung pekerjaan basis. 10.000 hanya menghitung tambahan pekerjaan nonbasis. 3.000 dan 40.000 tidak sesuai perhitungan.",
      None),
    Q("Perhatikan data analisis shift-share sektor elektronik berikut. Komponen keunggulan kompetitif = E × (gᵢⱼ − gᵢ).\n\nBesar komponen keunggulan kompetitif sektor elektronik Kabupaten E adalah …",
      ["40 orang", "50 orang", "30 orang", "120 orang", "70 orang"],
      "Analisis shift-share membagi pertumbuhan tenaga kerja sektor di daerah menjadi tiga komponen:\n• Pertumbuhan nasional (national share): E × g = 1.000 × 5% = 50 orang.\n• Bauran industri (industry mix): E × (gᵢ − g) = 1.000 × (8% − 5%) = 30 orang.\n• Keunggulan kompetitif (competitive/regional share): E × (gᵢⱼ − gᵢ) = 1.000 × (12% − 8%) = 40 orang.\nTotal pertumbuhan = 50 + 30 + 40 = 120 orang (sama dengan 1.000 × 12%).\nKomponen kompetitif positif berarti sektor elektronik di Kabupaten E tumbuh lebih cepat daripada sektor yang sama secara nasional, menandakan daya saing lokal.\n\nPengecoh: 50 adalah komponen pertumbuhan nasional. 30 adalah bauran industri. 120 adalah total pertumbuhan. 70 menjumlahkan dua komponen yang salah.",
      f_shift),
    Q("PDRB atas dasar harga konstan (ADHK) sebuah provinsi naik dari Rp500 triliun menjadi Rp530 triliun dalam setahun. Laju pertumbuhan ekonomi riil provinsi tersebut adalah …",
      ["6,0%", "5,7%", "30%", "106%", "3,0%"],
      "Pertumbuhan ekonomi riil = (PDRB ADHK tahun t − PDRB ADHK tahun t−1) ÷ PDRB ADHK tahun t−1 × 100%\n= (530 − 500) ÷ 500 × 100% = 30 ÷ 500 × 100% = 6,0%.\nPDRB harga konstan dipakai karena telah menghilangkan pengaruh kenaikan harga (inflasi), sehingga mencerminkan pertambahan volume barang dan jasa yang sebenarnya. PDRB harga berlaku (ADHB) dipakai untuk melihat struktur ekonomi dan besaran nominal.\n\nPengecoh: 5,7% membagi dengan nilai akhir (30 ÷ 530). 30% salah membaca selisih 30 triliun sebagai persen. 106% adalah rasio nilai akhir terhadap awal. 3,0% tidak sesuai perhitungan.",
      None),
    Q("Perhatikan data PDRB dan penduduk tiga provinsi berikut.\n\nPernyataan yang tepat adalah …",
      ["B memiliki PDRB per kapita tertinggi, sekitar Rp40 juta per orang", "C memiliki PDRB per kapita tertinggi karena PDRB totalnya terbesar",
       "A memiliki PDRB per kapita tertinggi, sekitar Rp20 juta per orang", "Ketiga provinsi memiliki PDRB per kapita yang sama", "B memiliki PDRB per kapita terendah karena PDRB totalnya terkecil"],
      "PDRB per kapita = PDRB ÷ jumlah penduduk.\n• A: 300 triliun ÷ 15 juta = Rp20 juta per orang.\n• B: 120 triliun ÷ 3 juta = Rp40 juta per orang.\n• C: 900 triliun ÷ 50 juta = Rp18 juta per orang.\nProvinsi B memiliki PDRB total terkecil, tetapi PDRB per kapitanya tertinggi karena penduduknya sedikit. Provinsi seperti ini sering merupakan daerah tambang atau migas (misalnya Kalimantan Timur atau Riau). PDRB per kapita adalah ukuran rata-rata dan belum menggambarkan pemerataan pendapatan.\n\nPengecoh: C memiliki PDRB total terbesar, tetapi per kapitanya terendah. A berada di urutan kedua. Ketiganya tidak sama.",
      f_pdrb),
    Q("Usaha mikro, kecil, dan menengah (UMKM) menyerap sekitar 97% tenaga kerja Indonesia, tetapi sumbangannya terhadap ekspor relatif kecil. Tantangan utama UMKM untuk naik kelas adalah …",
      ["Keterbatasan akses modal, teknologi, standar mutu, dan pasar", "UMKM tidak membutuhkan tenaga kerja sehingga sulit berkembang",
       "UMKM hanya beroperasi di sektor pertambangan skala besar", "UMKM dilarang menjual produknya ke luar negeri", "UMKM sudah menguasai seluruh pasar ekspor Indonesia"],
      "UMKM menjadi tulang punggung penyerapan tenaga kerja dan penyumbang sekitar 60% PDB, tetapi produktivitas dan kontribusi ekspornya relatif rendah. Penyebabnya antara lain keterbatasan modal dan akses kredit, teknologi produksi yang sederhana, kesulitan memenuhi standar mutu dan sertifikasi (misalnya halal, keamanan pangan), keterbatasan pemasaran dan jaringan distribusi, serta banyak yang belum berbadan hukum (informal). Program digitalisasi, pendampingan, kemitraan dengan usaha besar, dan pembiayaan seperti KUR ditujukan untuk membantu UMKM naik kelas.\n\nPengecoh: UMKM justru padat karya. UMKM tersebar di berbagai sektor, terutama perdagangan, kuliner, dan kerajinan, bukan pertambangan skala besar. UMKM boleh mengekspor. UMKM belum menguasai pasar ekspor.",
      None),
    Q("Perhatikan grafik Location Quotient sektor-sektor Kabupaten T berikut.\n\nSektor basis Kabupaten T adalah …",
      ["Pertambangan, industri, dan pariwisata", "Pertanian dan perdagangan", "Pertambangan saja", "Konstruksi, perdagangan, dan pertanian", "Semua sektor"],
      "Sektor basis adalah sektor dengan LQ > 1, artinya porsinya di kabupaten lebih besar daripada porsi rata-rata di tingkat acuan (provinsi atau nasional), sehingga diperkirakan menghasilkan surplus yang dijual ke luar wilayah.\nPada grafik, sektor dengan LQ di atas garis 1 adalah pertambangan (2,4), industri (1,3), dan pariwisata (1,1). Sektor pertanian (0,6), konstruksi (0,9), dan perdagangan (0,8) berada di bawah 1 sehingga merupakan sektor nonbasis yang terutama melayani kebutuhan lokal.\n\nPengecoh: \"pertambangan saja\" mengabaikan industri dan pariwisata yang juga di atas 1. Pertanian, konstruksi, dan perdagangan bukan sektor basis. Tidak semua sektor memiliki LQ di atas 1.",
      f_lqbar),
    Q("Dalam statistik PDB, tersedia PDB atas dasar harga berlaku (ADHB) dan atas dasar harga konstan (ADHK). Penggunaan yang tepat adalah …",
      ["ADHK untuk pertumbuhan riil; ADHB untuk struktur dan nilai nominal", "ADHB untuk mengukur pertumbuhan riil karena sudah bebas dari inflasi",
       "ADHK selalu lebih besar daripada ADHB di setiap tahun", "Keduanya sama persis sehingga dapat dipakai bergantian", "ADHK hanya dipakai untuk menghitung jumlah penduduk"],
      "PDB ADHB menilai barang dan jasa dengan harga pada tahun berjalan, sehingga dipengaruhi inflasi. ADHB cocok untuk melihat besaran nominal ekonomi dan struktur ekonomi (porsi tiap sektor) pada tahun tersebut.\nPDB ADHK menilai barang dan jasa dengan harga pada tahun dasar tertentu (misalnya 2010), sehingga pengaruh perubahan harga dihilangkan. ADHK dipakai untuk menghitung pertumbuhan ekonomi riil.\nSetelah tahun dasar, ADHB biasanya lebih besar daripada ADHK karena harga cenderung naik.\n\nPengecoh: ADHB belum bebas inflasi. ADHK tidak selalu lebih besar; justru biasanya lebih kecil setelah tahun dasar. Keduanya berbeda. ADHK tidak terkait penghitungan penduduk.",
      None),
    Q("Perhatikan diagram komposisi nilai ekspor barang Indonesia berikut.\n\nRisiko ekonomi yang paling mungkin dari komposisi ekspor tersebut adalah …",
      ["Penerimaan ekspor sangat dipengaruhi naik-turunnya harga komoditas global", "Ekspor tidak terpengaruh harga dunia karena didominasi barang elektronik",
       "Ekspor akan selalu surplus karena produk nikel bernilai tinggi", "Penerimaan ekspor stabil karena tidak ada komoditas yang dominan",
       "Indonesia tidak memerlukan pasar luar negeri untuk komoditasnya"],
      "Diagram menunjukkan ekspor Indonesia banyak bertumpu pada komoditas berbasis sumber daya alam seperti batu bara (18%), minyak sawit (11%), besi dan baja (10%), dan produk nikel (8%), sedangkan elektronik hanya sekitar 6%. Harga komoditas sangat berfluktuasi mengikuti permintaan global dan siklus ekonomi. Ketika harga batu bara dan sawit melonjak (misalnya 2021–2022), ekspor naik tajam; ketika harga jatuh, penerimaan ekspor dan pendapatan negara ikut turun. Karena itu diversifikasi ekspor dan hilirisasi penting untuk mengurangi kerentanan.\n\nPengecoh: elektronik justru porsi kecil. Surplus tidak terjamin. Komoditas dominan jelas ada. Komoditas ekspor justru bergantung pada pasar luar negeri.",
      f_ekspor),
    Q("Penanaman Modal Dalam Negeri (PMDN) dan Penanaman Modal Asing (PMA) sama-sama penting bagi pembangunan. Perbedaan utama keduanya adalah …",
      ["Asal pemilik modal: domestik atau asing", "PMDN hanya untuk pertanian, PMA hanya untuk pertambangan",
       "PMA tidak boleh menyerap tenaga kerja Indonesia", "PMDN wajib dilakukan di luar negeri", "PMA selalu lebih kecil nilainya daripada PMDN"],
      "Penanaman modal dibedakan berdasarkan asal pemilik modal. PMDN adalah investasi oleh penanam modal dalam negeri (perorangan atau badan usaha Indonesia), sedangkan PMA adalah investasi oleh penanam modal asing, baik sepenuhnya maupun patungan dengan pihak domestik, yang diatur dalam UU Penanaman Modal. Keduanya dapat bergerak di berbagai sektor, menyerap tenaga kerja Indonesia, dan menghasilkan alih teknologi. Pemerintah mengatur bidang usaha yang terbuka, terbatas, atau tertutup bagi investasi.\n\nPengecoh: tidak ada pembatasan sektor seperti pada opsi kedua. PMA justru menyerap tenaga kerja lokal. PMDN dilakukan di dalam negeri. Nilai PMA dan PMDN berfluktuasi; dalam beberapa tahun PMA lebih besar.",
      None),
]

P3 = [
    Q("Perhatikan tabel jam kerja untuk menghasilkan satu unit barang di dua negara berikut.\n\nPernyataan yang tepat adalah …",
      ["A unggul mutlak pada keduanya, tetapi komparatif hanya kain", "A unggul komparatif pada beras karena waktunya 4 jam",
       "B unggul mutlak pada kain dan beras", "Perdagangan tidak menguntungkan karena A unggul mutlak", "B unggul komparatif pada kain karena biaya peluangnya 1 unit beras"],
      "Keunggulan mutlak: A memerlukan jam kerja lebih sedikit untuk kain (2 < 6) dan beras (4 < 6), sehingga unggul mutlak pada keduanya.\nKeunggulan komparatif ditentukan dari biaya peluang:\n• Kain: A = 2/4 = 0,5 beras; B = 6/6 = 1 beras → A lebih rendah, unggul komparatif kain.\n• Beras: A = 4/2 = 2 kain; B = 6/6 = 1 kain → B lebih rendah, unggul komparatif beras.\nMenurut Ricardo, kedua negara tetap untung bila A berspesialisasi kain dan B berspesialisasi beras lalu berdagang.\n\nPengecoh: A tidak unggul komparatif pada beras. B tidak unggul mutlak. Perdagangan tetap menguntungkan. Biaya peluang kain B (1 beras) lebih tinggi daripada A (0,5), sehingga B tidak unggul komparatif pada kain.",
      f_komparatif),
    Q("Menurut teori Heckscher–Ohlin, negara dengan tenaga kerja melimpah dan modal terbatas seperti Bangladesh atau Vietnam cenderung mengekspor …",
      ["Barang padat karya seperti pakaian dan alas kaki", "Barang padat modal seperti pesawat terbang dan mesin presisi", "Barang yang memerlukan teknologi nuklir",
       "Jasa keuangan internasional berskala besar", "Barang yang tidak menggunakan tenaga kerja sama sekali"],
      "Teori Heckscher–Ohlin (proporsi faktor) menyatakan bahwa suatu negara akan mengekspor barang yang produksinya intensif menggunakan faktor produksi yang melimpah dan murah di negara itu, serta mengimpor barang yang intensif menggunakan faktor yang langka. Negara dengan tenaga kerja melimpah dan upah rendah memiliki keunggulan pada barang padat karya seperti pakaian, alas kaki, dan perakitan elektronik sederhana. Negara kaya modal dan teknologi seperti Jerman atau Jepang mengekspor barang padat modal.\n\nPengecoh: pesawat dan mesin presisi padat modal dan teknologi. Teknologi nuklir dan jasa keuangan internasional memerlukan modal dan keahlian tinggi. Tidak ada barang yang sama sekali tidak memerlukan tenaga kerja.",
      None),
    Q("Perhatikan grafik ekspor dan impor Negara M berikut.\n\nPersentase kenaikan nilai ekspor dari 2021 ke 2022 adalah sekitar …",
      ["26%", "21%", "61%", "126%", "35%"],
      "Persentase perubahan = (nilai akhir − nilai awal) ÷ nilai awal × 100%\n= (292 − 231) ÷ 231 × 100% = 61 ÷ 231 × 100% ≈ 26,4%.\nKenaikan sebesar ini pada 2022 banyak dipengaruhi lonjakan harga komoditas ekspor setelah pemulihan pandemi dan gangguan pasokan global.\n\nPengecoh: 21% membagi dengan nilai akhir (61 ÷ 292). 61% salah menuliskan selisih 61 miliar USD sebagai persen. 126% adalah rasio nilai akhir terhadap awal. 35% adalah nilai surplus perdagangan 2021 (231 − 196), bukan persentase kenaikan ekspor.",
      f_xm),
    Q("Harga sebuah barang impor di negara asalnya 100 USD dan dikenakan tarif impor 25%. Harga barang sejenis buatan dalam negeri 120 USD. Dampak tarif tersebut adalah …",
      ["Harga impor menjadi 125 USD sehingga produk dalam negeri lebih bersaing", "Harga impor menjadi 75 USD sehingga barang impor makin murah",
       "Harga impor tetap 100 USD karena tarif dibayar negara pengekspor", "Harga impor menjadi 145 USD sehingga barang impor tidak laku",
       "Tarif tidak berpengaruh terhadap persaingan harga di pasar domestik"],
      "Harga setelah tarif = harga impor × (1 + tarif) = 100 × (1 + 0,25) = 125 USD.\nSebelum tarif, barang impor (100 USD) lebih murah daripada produk dalam negeri (120 USD). Setelah tarif, barang impor menjadi 125 USD, lebih mahal daripada produk dalam negeri, sehingga konsumen beralih ke produk lokal. Inilah fungsi tarif sebagai instrumen proteksi industri dalam negeri, walaupun konsumen harus membayar harga lebih mahal daripada sebelumnya.\n\nPengecoh: tarif menaikkan, bukan menurunkan, harga impor. Tarif dibayar importir dan pada akhirnya konsumen domestik. 145 USD menambahkan 25 dan 20 secara keliru. Tarif jelas memengaruhi persaingan harga.",
      None),
    Q("Perhatikan tabel harga satu unit barang di Negara Z setelah membentuk perjanjian perdagangan bebas (FTA) dengan Negara Y berikut.\n\nGejala yang terjadi ketika Negara Z beralih membeli dari Negara Y adalah …",
      ["Trade diversion; impor beralih ke anggota FTA yang kurang efisien", "Trade creation; impor beralih ke pemasok paling efisien di dunia",
       "Dumping; Negara Y menjual di bawah biaya produksi", "Kuota impor; jumlah barang dari X dibatasi secara fisik",
       "Swasembada; Negara Z berhenti mengimpor barang tersebut"],
      "Negara X adalah produsen paling efisien (harga 90), tetapi karena bukan anggota FTA, barangnya dikenai tarif 20% sehingga harganya di Negara Z menjadi 108. Barang dari Negara Y (anggota FTA) dibebaskan tarif sehingga harganya 100. Konsumen di Z beralih membeli dari Y karena lebih murah di pasar Z, padahal biaya produksi Y lebih tinggi daripada X. Peralihan impor dari pemasok luar yang efisien ke anggota FTA yang kurang efisien disebut trade diversion (pengalihan perdagangan), dan negara Z juga kehilangan penerimaan tarif.\nTrade creation terjadi bila FTA mengganti produksi domestik yang mahal dengan impor yang lebih murah dari anggota.\n\nPengecoh: Y bukan pemasok paling efisien. Tidak ada indikasi dumping atau kuota. Negara Z tetap mengimpor.",
      f_diversion),
    Q("Sebuah perusahaan asing menjual baja di pasar Indonesia dengan harga jauh di bawah harga di negaranya sendiri dan di bawah biaya produksinya untuk merebut pasar. Praktik ini disebut … dan dapat dibalas dengan …",
      ["Dumping; bea masuk antidumping", "Subsidi ekspor; kuota ekspor", "Embargo; tarif nol persen", "Kuota impor; pembebasan pajak", "Proteksi; perdagangan bebas penuh"],
      "Dumping adalah praktik menjual produk di pasar ekspor dengan harga lebih rendah daripada harga normal di negara asal (atau di bawah biaya produksi). Tujuannya menguasai pasar dan menyingkirkan pesaing lokal. Dumping dapat merugikan industri dalam negeri negara pengimpor. Berdasarkan aturan WTO, negara yang dirugikan boleh mengenakan bea masuk antidumping (BMAD) setelah penyelidikan membuktikan adanya dumping dan kerugian industri dalam negeri. Indonesia pernah mengenakan BMAD pada produk baja tertentu.\n\nPengecoh: subsidi ekspor adalah bantuan pemerintah kepada eksportir, dan kuota ekspor membatasi jumlah ekspor. Embargo adalah larangan perdagangan. Kuota impor membatasi jumlah. Proteksi adalah istilah umum, bukan nama praktik pada soal.",
      None),
    Q("Perhatikan grafik indeks harga ekspor dan impor Negara R berikut.\n\nTahun ketika terms of trade Negara R paling menguntungkan adalah …",
      ["2022", "2016", "2018", "2020", "2024"],
      "Terms of trade (ToT) = indeks harga ekspor ÷ indeks harga impor × 100.\n• 2016: 100 ÷ 100 × 100 = 100.\n• 2018: 112 ÷ 108 × 100 ≈ 103,7.\n• 2020: 98 ÷ 104 × 100 ≈ 94,2.\n• 2022: 150 ÷ 120 × 100 = 125.\n• 2024: 125 ÷ 122 × 100 ≈ 102,5.\nToT tertinggi (paling menguntungkan) terjadi pada 2022, saat harga ekspor melonjak jauh lebih cepat daripada harga impor. Pada tahun itu, setiap unit ekspor dapat \"membeli\" lebih banyak barang impor.\n\nPengecoh: 2016 adalah tahun dasar. 2018 dan 2024 hanya sedikit di atas 100. 2020 justru di bawah 100 (memburuk).",
      f_tot),
    Q("Tingkat integrasi ekonomi yang menghapus hambatan perdagangan antaranggota dan menetapkan tarif eksternal bersama terhadap negara nonanggota, tetapi belum membebaskan pergerakan tenaga kerja dan modal, disebut …",
      ["Kesatuan pabean (customs union)", "Kawasan perdagangan bebas (FTA)", "Pasar bersama (common market)", "Kesatuan ekonomi (economic union)",
       "Perjanjian perdagangan preferensial"],
      "Tahapan integrasi ekonomi (Balassa):\n1) Perjanjian perdagangan preferensial: penurunan tarif untuk sebagian barang.\n2) Kawasan perdagangan bebas (FTA): tarif antaranggota dihapus, tetapi setiap negara bebas menetapkan tarif terhadap nonanggota (contoh: AFTA).\n3) Kesatuan pabean: FTA ditambah tarif eksternal bersama terhadap nonanggota.\n4) Pasar bersama: kesatuan pabean ditambah kebebasan pergerakan tenaga kerja dan modal.\n5) Kesatuan ekonomi: pasar bersama ditambah koordinasi kebijakan ekonomi, bahkan mata uang bersama (contoh: Uni Eropa dengan euro).\nCiri pada soal sesuai dengan kesatuan pabean.\n\nPengecoh: FTA tidak memiliki tarif eksternal bersama. Pasar bersama dan kesatuan ekonomi sudah membebaskan tenaga kerja dan modal.",
      None),
    Q("Perhatikan peta negara-negara anggota sebuah perjanjian perdagangan regional berikut.\n\nPerjanjian yang dimaksud adalah …",
      ["Regional Comprehensive Economic Partnership", "Asia-Pacific Economic Cooperation (APEC)", "ASEAN Free Trade Area (AFTA)",
       "Uni Eropa (European Union)", "North American Free Trade Agreement (NAFTA)"],
      "Negara yang diwarnai hijau adalah sepuluh negara ASEAN ditambah Tiongkok, Jepang, Korea Selatan, Australia, dan Selandia Baru. Kelima belas negara ini adalah anggota Regional Comprehensive Economic Partnership (RCEP), perjanjian perdagangan bebas terbesar di dunia berdasarkan jumlah penduduk dan PDB, yang ditandatangani pada 2020 dan berlaku sejak 2022.\n\nPengecoh: AFTA hanya beranggotakan negara ASEAN. APEC juga mencakup Amerika Serikat, Kanada, Meksiko, Rusia, Chili, dan Peru, serta merupakan forum kerja sama, bukan FTA. Uni Eropa dan NAFTA (kini USMCA) berada di kawasan lain.",
      f_rcep),
    Q("Organisasi Perdagangan Dunia (WTO) memiliki beberapa fungsi utama. Salah satu fungsi WTO adalah …",
      ["Menyelesaikan sengketa perdagangan antarnegara anggota", "Mencetak mata uang tunggal bagi seluruh negara anggota", "Memberikan pinjaman darurat untuk krisis neraca pembayaran",
       "Menetapkan harga minyak dunia setiap bulan", "Mengatur kerja sama militer antarnegara anggota"],
      "WTO (berdiri 1995 menggantikan GATT) berfungsi: (1) merundingkan dan mengelola aturan perdagangan internasional yang disepakati; (2) menyelesaikan sengketa perdagangan antaranggota melalui badan penyelesaian sengketa; (3) memantau kebijakan perdagangan negara anggota; serta (4) membantu kapasitas perdagangan negara berkembang. Indonesia pernah bersengketa di WTO, misalnya terkait larangan ekspor bijih nikel yang digugat Uni Eropa.\n\nPengecoh: WTO tidak mencetak mata uang. Pinjaman darurat neraca pembayaran adalah fungsi IMF. Harga minyak ditentukan pasar dan dipengaruhi OPEC+. Kerja sama militer bukan fungsi WTO.",
      None),
]

P4 = [
    Q("Perhatikan grafik realisasi penanaman modal asing menurut sektor berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["PMA terbesar mengalir ke logam dasar dan smelter", "PMA terbesar mengalir ke sektor perumahan untuk penduduk perkotaan",
       "Investasi asing di sektor pertambangan lebih besar daripada logam dasar", "PMA sudah tidak masuk ke sektor industri pengolahan",
       "Semua sektor menerima investasi asing dengan nilai yang sama"],
      "Grafik menunjukkan realisasi PMA terbesar berada di sektor logam dasar dan smelter (±11 miliar USD), jauh di atas pertambangan (±5,2), kimia dan farmasi (±4,1), transportasi dan gudang (±3,8), serta perumahan dan kawasan industri (±3,1). Pola ini terkait kebijakan larangan ekspor bijih mineral dan hilirisasi, yang mendorong investor asing (terutama dari Tiongkok) membangun smelter nikel dan industri baja nirkarat di Sulawesi dan Maluku Utara.\n\nPengecoh: perumahan justru terkecil. Pertambangan lebih kecil daripada logam dasar. Industri pengolahan logam dasar justru menerima PMA terbesar. Nilai antarsektor jelas berbeda.",
      f_fdi),
    Q("Perusahaan transnasional (TNC) dapat membawa dampak positif dan negatif bagi negara tuan rumah. Dampak negatif yang paling sering dikritik adalah …",
      ["Laba dibawa ke negara asal dan ekonomi bergantung kantor pusat", "TNC tidak pernah menyerap tenaga kerja lokal sama sekali",
       "TNC selalu menurunkan ekspor negara tuan rumah", "TNC dilarang membayar pajak di negara tuan rumah", "TNC selalu memindahkan seluruh teknologinya kepada pesaing lokal"],
      "Perusahaan transnasional beroperasi di banyak negara dengan kantor pusat di satu negara. Dampak positifnya antara lain investasi, lapangan kerja, alih teknologi, dan akses pasar ekspor. Dampak negatif yang sering dikritik: keuntungan (repatriasi laba) dibawa ke negara asal; keputusan strategis seperti menutup pabrik ditentukan kantor pusat sehingga ekonomi lokal rentan; praktik penghindaran pajak melalui transfer pricing; persaingan yang menekan usaha lokal; serta potensi eksploitasi tenaga kerja dan kerusakan lingkungan.\n\nPengecoh: TNC umumnya menyerap tenaga kerja lokal. TNC sering justru meningkatkan ekspor. TNC wajib membayar pajak. TNC biasanya menjaga teknologi intinya, bukan memberikannya kepada pesaing.",
      None),
    Q("Perhatikan diagram pembagian nilai satu unit telepon pintar berikut.\n\nKesimpulan yang paling tepat tentang rantai nilai global produk tersebut adalah …",
      ["Negara perakit memperoleh porsi nilai paling kecil, pemilik merek dan desain terbesar", "Negara perakit memperoleh porsi nilai paling besar karena melakukan produksi fisik",
       "Bahan mentah menyumbang porsi nilai terbesar dalam rantai nilai ponsel", "Semua negara yang terlibat memperoleh porsi nilai yang sama besar",
       "Komponen dari Korea Selatan bernilai lebih besar daripada keuntungan pemilik merek"],
      "Diagram menunjukkan keuntungan pemilik merek dan desain (Amerika Serikat) mencapai ±58% nilai produk, komponen dari Korea Selatan ±14%, Jepang dan Taiwan ±10%, bahan mentah ±5%, distribusi dan lainnya ±11%, sedangkan perakitan di Tiongkok hanya ±2%. Walaupun produk dirakit di Tiongkok, sebagian besar nilai tambah dinikmati negara yang menguasai desain, teknologi, merek, dan komponen bernilai tinggi. Hal ini sesuai dengan kurva senyum rantai nilai global.\n\nPengecoh: negara perakit justru memperoleh porsi terkecil. Bahan mentah porsinya kecil. Porsi nilai sangat tidak merata. Komponen Korea Selatan (14%) jauh lebih kecil daripada keuntungan pemilik merek (58%).",
      f_ponsel),
    Q("Sebuah perusahaan Indonesia menyerahkan layanan pusat panggilan (call center)-nya kepada perusahaan lain di Filipina. Praktik ini paling tepat disebut …",
      ["Offshore outsourcing, yaitu alih daya ke pihak di luar negeri", "Insourcing, yaitu menarik kembali kegiatan ke dalam perusahaan",
       "Onshoring, yaitu memindahkan kegiatan ke kota lain di dalam negeri", "Integrasi vertikal, yaitu membeli perusahaan pemasok bahan baku",
       "Merger horizontal, yaitu bergabung dengan pesaing sejenis"],
      "Outsourcing (alih daya) adalah menyerahkan sebagian kegiatan perusahaan kepada pihak lain. Offshoring adalah memindahkan kegiatan ke negara lain, baik melalui anak perusahaan sendiri maupun pihak lain. Kombinasi keduanya, yaitu menyerahkan kegiatan kepada perusahaan lain di luar negeri, disebut offshore outsourcing. Filipina menjadi tujuan utama layanan call center (business process outsourcing) karena tenaga kerja berbahasa Inggris dengan biaya relatif rendah.\n\nPengecoh: insourcing adalah kebalikan outsourcing. Onshoring berlangsung di dalam negeri. Integrasi vertikal dan merger horizontal adalah strategi penggabungan usaha, bukan alih daya layanan.",
      None),
    Q("Perhatikan diagram rantai pasok sebuah pabrik perakitan mobil berikut.\n\nRisiko utama yang tergambar pada rantai pasok tersebut adalah …",
      ["Ketergantungan pada pemasok cip tunggal di Taiwan", "Pabrik tidak memerlukan komponen impor sama sekali",
       "Pasar domestik terlalu kecil sehingga mobil tidak dapat dijual", "Pemasok dari Jepang dan Thailand selalu memasok cip semikonduktor",
       "Perakitan mobil di Karawang tidak terhubung dengan pasar ekspor"],
      "Diagram menunjukkan pabrik di Karawang bergantung pada komponen impor dari beberapa negara, dan cip semikonduktor hanya berasal dari satu pemasok di Taiwan. Rantai pasok global yang efisien tetapi terkonsentrasi rentan terhadap gangguan: bencana, pandemi, konflik geopolitik, atau kekurangan produksi di satu titik dapat menghentikan seluruh perakitan. Kekurangan cip global pada 2021–2022 menyebabkan banyak pabrik mobil di dunia menghentikan produksi. Strategi mitigasinya antara lain diversifikasi pemasok, menambah stok penyangga, dan mengembangkan industri komponen dalam negeri.\n\nPengecoh: pabrik jelas memakai komponen impor. Diagram menunjukkan pasar domestik dan ekspor. Cip hanya dari Taiwan. Pabrik terhubung ke pasar ekspor.",
      f_rantai),
    Q("Restoran cepat saji global di Indonesia menjual menu nasi dan ayam berbumbu lokal serta memiliki sertifikasi halal. Strategi ini disebut …",
      ["Glokalisasi produk", "Homogenisasi budaya", "Deglobalisasi", "Proteksionisme", "Nasionalisasi aset"],
      "Glokalisasi (glocalization) adalah strategi perusahaan global menyesuaikan produk, layanan, atau pemasarannya dengan budaya, selera, dan aturan setempat. Contohnya menu nasi, sambal, dan ayam berbumbu, serta sertifikasi halal di Indonesia; atau menu tanpa daging sapi di India. Glokalisasi menunjukkan bahwa globalisasi tidak selalu menyeragamkan budaya, tetapi berinteraksi dengan budaya lokal.\n\nPengecoh: homogenisasi budaya adalah penyeragaman budaya akibat globalisasi, kebalikan dari penyesuaian lokal. Deglobalisasi adalah melemahnya integrasi ekonomi global. Proteksionisme adalah kebijakan negara melindungi industri dalam negeri. Nasionalisasi adalah pengambilalihan aset asing oleh negara.",
      None),
    Q("Perhatikan grafik arus peti kemas beberapa pelabuhan berikut.\n\nFaktor utama yang menjadikan Singapura pelabuhan peti kemas terbesar kedua walaupun pasar domestiknya kecil adalah …",
      ["Lokasi strategis di Selat Malaka sebagai pelabuhan transshipment kawasan", "Jumlah penduduk Singapura yang terbesar di Asia Tenggara",
       "Singapura memproduksi seluruh barang yang diekspor melalui pelabuhannya", "Singapura berada di tengah Samudra Pasifik",
       "Pelabuhan Tanjung Priok mengirim seluruh barang ke Singapura tanpa biaya"],
      "Singapura berada di ujung selatan Selat Malaka, salah satu jalur pelayaran tersibuk di dunia yang menghubungkan Asia Timur dengan Asia Selatan, Timur Tengah, dan Eropa. Sebagian besar peti kemas di Singapura tidak ditujukan untuk pasar domestik, tetapi dipindahkan dari satu kapal ke kapal lain (transshipment) menuju tujuan akhir di kawasan, termasuk Indonesia. Keunggulan lokasi didukung efisiensi pelabuhan, kedalaman perairan, teknologi, dan jaringan pelayaran yang luas.\n\nPengecoh: penduduk Singapura kecil. Sebagian besar barang tidak diproduksi di Singapura. Singapura berada di Asia Tenggara, bukan Pasifik. Pengiriman tidak tanpa biaya.",
      f_pelabuhan),
    Q("Negara-negara berlomba menurunkan standar upah, pajak, dan perlindungan lingkungan agar menarik investasi asing. Gejala ini disebut …",
      ["Race to the bottom", "Trickle-down effect", "Brain gain", "Dutch disease", "Economies of scale"],
      "Race to the bottom adalah persaingan antarnegara atau antardaerah untuk menarik investasi dengan menurunkan standar, misalnya upah minimum, pajak perusahaan, perlindungan tenaga kerja, dan regulasi lingkungan. Dalam jangka pendek investasi mungkin meningkat, tetapi dalam jangka panjang dapat merugikan kesejahteraan pekerja, penerimaan negara, dan kualitas lingkungan. Upaya mengatasinya antara lain kesepakatan pajak minimum global dan standar ketenagakerjaan internasional.\n\nPengecoh: trickle-down effect adalah anggapan bahwa manfaat pertumbuhan akan menetes ke kelompok bawah. Brain gain adalah masuknya tenaga ahli. Dutch disease adalah melemahnya sektor lain akibat booming sumber daya alam. Economies of scale adalah penurunan biaya per unit karena skala produksi besar.",
      None),
    Q("Perhatikan grafik porsi realisasi investasi menurut lokasi berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Porsi investasi luar Jawa melampaui Jawa sejak sekitar 2018", "Investasi semakin terpusat di Jawa sejak 2015",
       "Porsi investasi Jawa dan luar Jawa tidak pernah berubah", "Investasi luar Jawa menurun tajam setelah tahun 2019", "Seluruh investasi pada 2023 berada di Pulau Jawa"],
      "Grafik menunjukkan porsi investasi di Jawa turun dari ±54% (2015) menjadi ±44% (2023), sedangkan luar Jawa naik dari ±46% menjadi ±56%. Kedua garis berpotongan sekitar 2018, dan sejak itu luar Jawa menerima porsi lebih besar. Pergeseran ini terkait investasi smelter dan hilirisasi mineral di Sulawesi dan Maluku Utara, proyek energi, kawasan industri di luar Jawa, serta pembangunan infrastruktur. Bagi pemerataan, tren ini positif, tetapi perlu diimbangi pengelolaan lingkungan dan peningkatan keterampilan tenaga kerja lokal.\n\nPengecoh: investasi justru makin menyebar ke luar Jawa. Porsi keduanya berubah. Investasi luar Jawa naik, bukan turun. Porsi Jawa pada 2023 sekitar 44%, bukan 100%.",
      f_investasi),
    Q("Konsep pembagian kerja internasional baru (new international division of labour) menjelaskan bahwa sejak 1970-an …",
      ["Pabrik padat karya pindah ke negara berkembang, riset di negara maju", "Negara berkembang hanya mengekspor bahan mentah seperti pada masa kolonial",
       "Seluruh industri berpindah dari Asia ke Eropa Barat", "Negara maju berhenti melakukan kegiatan ekonomi apa pun", "Perdagangan internasional dihapus sepenuhnya"],
      "Pada masa kolonial, pembagian kerja internasional lama menempatkan negara jajahan sebagai pemasok bahan mentah dan negara industri sebagai produsen barang jadi. Sejak 1970-an, perusahaan transnasional memindahkan kegiatan manufaktur padat karya (tekstil, elektronik, perakitan) ke negara berkembang di Asia Timur dan Tenggara yang menawarkan upah rendah, sementara kegiatan bernilai tambah tinggi seperti riset, desain, keuangan, dan manajemen tetap di negara maju. Pola inilah yang disebut pembagian kerja internasional baru, dan memicu industrialisasi negara seperti Korea Selatan, Taiwan, Malaysia, dan kemudian Tiongkok serta Vietnam.\n\nPengecoh: opsi kedua menggambarkan pola lama. Industri justru bergeser ke Asia. Negara maju tetap berkegiatan ekonomi. Perdagangan justru makin intensif.",
      None),
]

P5 = [
    Q("Perhatikan grafik porsi impor barang Amerika Serikat menurut asal berikut.\n\nInterpretasi yang paling tepat terkait perang dagang AS–Tiongkok sejak 2018 adalah …",
      ["Porsi Tiongkok turun, sedangkan Meksiko dan Vietnam naik", "Porsi Tiongkok naik tajam karena tarif AS dihapus",
       "Porsi ketiga negara tidak berubah sejak 2017", "Vietnam menggantikan Tiongkok sebagai pemasok terbesar AS", "Meksiko berhenti mengekspor ke AS sejak 2019"],
      "Grafik menunjukkan porsi Tiongkok dalam impor AS turun dari ±21,6% (2017) menjadi ±13,9% (2023), sedangkan Meksiko naik dari ±13,4% menjadi ±15,4% (melampaui Tiongkok) dan Vietnam naik dari ±2% menjadi ±3,6–3,8%. Setelah AS mengenakan tarif tinggi pada banyak produk Tiongkok sejak 2018, sebagian perusahaan memindahkan produksi atau sumber pasokan ke negara lain (trade diversion dan relokasi rantai pasok, sering disebut \"China plus one\"). Negara di Asia Tenggara, termasuk Indonesia, berpeluang menarik relokasi ini.\n\nPengecoh: porsi Tiongkok turun, bukan naik. Porsi ketiga negara berubah. Vietnam belum menggantikan Tiongkok sebagai pemasok terbesar. Meksiko justru naik.",
      f_porsi),
    Q("Selat Malaka disebut sebagai \"dilema Malaka\" bagi Tiongkok. Pengertian yang paling tepat adalah …",
      ["Impor energi Tiongkok sangat bergantung pada Selat Malaka yang rawan terganggu", "Tiongkok menguasai penuh Selat Malaka sehingga negara lain tidak dapat melintas",
       "Selat Malaka terlalu dangkal sehingga tidak dapat dilalui kapal tanker", "Selat Malaka terletak di Samudra Atlantik sehingga jauh dari Tiongkok",
       "Tiongkok tidak mengimpor minyak sehingga Selat Malaka tidak penting"],
      "Sebagian besar impor minyak dan gas Tiongkok dari Timur Tengah dan Afrika diangkut melalui Selat Malaka. Ketergantungan pada satu titik sempit ini membuat pasokan energi Tiongkok rentan bila selat tersebut terganggu, misalnya karena konflik, blokade, atau perompakan. Kekhawatiran ini disebut dilema Malaka. Untuk mengurangi ketergantungan, Tiongkok membangun jalur alternatif seperti pipa melalui Myanmar dan Pakistan, pelabuhan di Samudra Hindia, serta jalur darat melalui inisiatif Sabuk dan Jalan.\n\nPengecoh: Selat Malaka adalah perairan internasional yang dikelola negara-negara pantai (Indonesia, Malaysia, Singapura), bukan dikuasai Tiongkok. Selat ini dilalui kapal tanker besar meskipun ada batas sarat. Selat Malaka berada di Asia Tenggara. Tiongkok adalah importir minyak terbesar dunia.",
      None),
    Q("Perhatikan grafik aliran minyak melalui titik sempit maritim berikut.\n\nTitik sempit yang bila tertutup paling besar mengganggu pasokan minyak dunia adalah …",
      ["Selat Hormuz", "Selat Malaka", "Terusan Suez", "Bab el-Mandeb", "Terusan Panama"],
      "Grafik menunjukkan aliran minyak terbesar melewati Selat Hormuz (±21 juta barel per hari, sekitar seperlima konsumsi minyak dunia), disusul Selat Malaka (±16), Terusan Suez dan pipa SUMED (±9), Bab el-Mandeb (±6), dan Terusan Panama (±1). Selat Hormuz adalah satu-satunya jalur laut keluar dari Teluk Persia, tempat negara-negara produsen besar seperti Arab Saudi, Irak, Kuwait, Uni Emirat Arab, Qatar, dan Iran. Ketegangan di kawasan ini sering langsung menaikkan harga minyak dunia.\n\nPengecoh: Selat Malaka juga sangat penting, tetapi alirannya lebih kecil daripada Hormuz pada grafik. Suez, Bab el-Mandeb, dan Panama memiliki aliran minyak lebih kecil.",
      f_minyak),
    Q("Industri 4.0 ditandai oleh penerapan beberapa teknologi berikut, KECUALI …",
      ["Mesin uap sebagai tenaga utama", "Internet of Things (IoT)", "Kecerdasan buatan (artificial intelligence)", "Analisis data besar (big data)",
       "Robotika dan otomatisasi berbasis sensor"],
      "Revolusi industri terdiri atas beberapa tahap:\n• Industri 1.0 (akhir abad ke-18): mekanisasi dengan tenaga uap.\n• Industri 2.0 (akhir abad ke-19): listrik dan produksi massal di jalur perakitan.\n• Industri 3.0 (1970-an): komputer, elektronik, dan otomatisasi.\n• Industri 4.0 (sejak 2010-an): sistem siber-fisik yang menghubungkan mesin, data, dan manusia melalui IoT, kecerdasan buatan, big data, komputasi awan, robotika cerdas, dan pencetakan 3D.\nMesin uap adalah ciri revolusi industri pertama, bukan Industri 4.0. Kata kunci KECUALI menuntut kita memilih pernyataan yang tidak sesuai.\n\nOpsi lainnya adalah teknologi khas Industri 4.0.",
      None),
    Q("Perhatikan grafik nilai transaksi ekonomi digital sebuah negara berikut.\n\nPersentase kenaikan nilai transaksi dari 2020 ke 2021 adalah sekitar …",
      ["49%", "23%", "70%", "33%", "149%"],
      "Persentase perubahan = (70 − 47) ÷ 47 × 100% = 23 ÷ 47 × 100% ≈ 48,9% ≈ 49%.\nLonjakan pada 2021 banyak dipengaruhi pembatasan aktivitas selama pandemi COVID-19, yang mendorong masyarakat beralih ke belanja daring, layanan pesan antar, dan pembayaran digital. Setelah itu pertumbuhan melambat (2021–2022 hanya ±10%) karena aktivitas luring kembali normal.\n\nPengecoh: 23% salah menuliskan selisih 23 miliar USD sebagai persen. 70% adalah nilai 2021, bukan persentase. 33% membagi dengan nilai akhir (23 ÷ 70). 149% adalah rasio nilai akhir terhadap awal.",
      f_gmv),
    Q("Kesenjangan digital (digital divide) di Indonesia paling tepat digambarkan oleh kondisi …",
      ["Beda akses dan kemampuan internet antara kota dan daerah 3T", "Semua daerah memiliki kecepatan internet yang sama",
       "Penduduk perdesaan lebih banyak memakai internet daripada penduduk kota", "Kesenjangan digital hanya terjadi di negara maju",
       "Kesenjangan digital hanya berkaitan dengan harga telepon pintar"],
      "Kesenjangan digital adalah perbedaan akses terhadap teknologi informasi dan komunikasi, kemampuan menggunakannya (literasi digital), serta manfaat yang diperoleh, antara kelompok atau wilayah. Di Indonesia, kota besar di Jawa memiliki jaringan internet cepat dan penetrasi tinggi, sedangkan banyak desa di daerah tertinggal, terdepan, dan terluar (3T) seperti di Papua dan Maluku belum memiliki sinyal memadai. Selain infrastruktur, faktor pendapatan, pendidikan, usia, dan keterampilan juga berpengaruh. Program pembangunan BTS dan satelit seperti SATRIA ditujukan untuk mengurangi kesenjangan ini.\n\nPengecoh: kecepatan internet tidak sama. Penduduk kota justru lebih banyak memakai internet. Kesenjangan digital juga terjadi di negara berkembang. Harga perangkat hanya salah satu faktor.",
      None),
    Q("Perhatikan tabel nilai produk pada beberapa tahap hilirisasi nikel berikut.\n\nNilai produk prekursor/katode baterai dibandingkan bijih nikel per ton adalah sekitar …",
      ["625 kali lebih tinggi", "17 kali lebih tinggi", "62 kali lebih tinggi", "10 kali lebih tinggi", "24.960 kali lebih tinggi"],
      "Rasio nilai = nilai produk baterai ÷ nilai bijih = 25.000 ÷ 40 = 625 kali.\nAngka ini menunjukkan potensi nilai tambah hilirisasi: semakin jauh bahan mentah diolah ke produk akhir, semakin besar nilai yang tercipta di dalam negeri. Namun perlu dicatat bahwa satu ton produk akhir memerlukan banyak ton bijih, energi, bahan kimia, dan modal besar, sehingga nilai tambah bersih lebih kecil daripada rasio harga per ton.\n\nPengecoh: 17 kali membandingkan baterai dengan baja nirkarat secara keliru (25.000 ÷ 1.500). 62 kali dan 10 kali adalah kesalahan perhitungan. 24.960 adalah selisih nilai, bukan rasio.",
      f_nilaitambah),
    Q("Pengemudi ojek daring dan pekerja lepas desain grafis yang mendapat pekerjaan melalui aplikasi merupakan bagian dari ekonomi … dengan tantangan utama …",
      ["Gig; perlindungan sosial yang terbatas", "Agraris; kekurangan lahan pertanian", "Ekstraktif; penipisan cadangan mineral",
       "Subsisten; hasil kerja dikonsumsi sendiri", "Gig; upah selalu jauh lebih tinggi daripada pegawai tetap"],
      "Ekonomi gig adalah sistem kerja berbasis tugas atau proyek jangka pendek yang sering diperantarai platform digital, misalnya ojek dan kurir daring, pekerja lepas desain, penulis, atau pengembang aplikasi. Kelebihannya adalah fleksibilitas waktu dan kemudahan memperoleh pekerjaan. Tantangannya antara lain pendapatan tidak pasti, status \"mitra\" yang tidak memberikan hak sebagai pekerja (cuti, pesangon, upah minimum), perlindungan sosial terbatas (jaminan kesehatan dan ketenagakerjaan), serta ketergantungan pada algoritma platform.\n\nPengecoh: ekonomi agraris, ekstraktif, dan subsisten tidak menggambarkan kerja berbasis aplikasi. Upah pekerja gig tidak selalu lebih tinggi; sering justru lebih rendah dan tidak stabil.",
      None),
    Q("Perhatikan peta lokasi utama kawasan smelter nikel berikut.\n\nImplikasi geografis yang paling tepat dari sebaran kawasan tersebut adalah …",
      ["Pusat pertumbuhan baru di Sulawesi dan Maluku Utara", "Seluruh industri nikel berada di Pulau Jawa dekat pasar konsumen",
       "Kawasan smelter berada jauh dari sumber bijih nikel", "Kawasan smelter tidak memerlukan energi listrik dalam jumlah besar", "Sebaran smelter tidak berdampak pada migrasi tenaga kerja"],
      "Peta menunjukkan kawasan smelter nikel terkonsentrasi di Sulawesi Tengah (Morowali), Sulawesi Tenggara (Konawe dan Pomalaa), serta Maluku Utara (Weda Bay dan Obi), yaitu dekat cadangan nikel laterit. Implikasinya: tumbuh pusat ekonomi baru di luar Jawa, migrasi besar tenaga kerja dari berbagai daerah, pembangunan pelabuhan dan PLTU captive, serta kenaikan PDRB yang pesat. Di sisi lain muncul tekanan lingkungan seperti deforestasi, sedimentasi dan pencemaran pesisir, emisi dari PLTU batu bara, serta isu keselamatan kerja dan sosial.\n\nPengecoh: smelter tidak berada di Jawa. Smelter justru dekat sumber bijih (berorientasi bahan baku). Smelter sangat boros energi listrik. Sebaran smelter jelas mendorong migrasi tenaga kerja.",
      f_smelter),
    Q("Indonesia menargetkan menjadi negara berpendapatan tinggi pada 2045. Risiko \"jebakan pendapatan menengah\" (middle income trap) yang perlu dihindari adalah …",
      ["Pertumbuhan melambat karena upah naik tanpa kenaikan produktivitas", "Penduduk berhenti bertambah sehingga ekonomi langsung menjadi berpendapatan tinggi",
       "Negara otomatis menjadi berpendapatan tinggi setelah bonus demografi", "Ekonomi tumbuh terlalu cepat sehingga melampaui negara maju",
       "Negara berpendapatan menengah dilarang berdagang dengan negara maju"],
      "Jebakan pendapatan menengah terjadi ketika suatu negara berhasil keluar dari kemiskinan berkat upah murah dan sumber daya alam, tetapi kemudian pertumbuhannya melambat sebelum mencapai pendapatan tinggi. Penyebabnya: upah mulai naik sehingga tidak lagi bersaing dengan negara berupah rendah, sementara produktivitas, teknologi, inovasi, dan kualitas SDM belum cukup untuk bersaing dengan negara maju. Contoh negara yang berhasil keluar adalah Korea Selatan dan Taiwan melalui investasi besar di pendidikan, riset, dan industri bernilai tambah tinggi.\n\nPengecoh: berhentinya pertambahan penduduk tidak otomatis menaikkan pendapatan. Bonus demografi tidak otomatis menghasilkan pendapatan tinggi. Jebakan justru berupa perlambatan. Tidak ada larangan berdagang.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
