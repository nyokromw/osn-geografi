from figlib import *


def Q(t, o, e, f=None):
    return dict(t=t, o=o, e=e, f=f)

# ============================ figures ============================

def f_thunen(path):
    fig, ax = blank(6.5, 6.5, (-50, 50), (-50, 50))
    cols = ["#FBD38D", "#68D391", "#F6E05E", "#C6F6D5", "#E2E8F0"]
    for r, c in zip([45, 36, 27, 18, 9][::-1], cols[::-1]):
        pass
    for r, c in zip([45, 36, 27, 18], ["#E2E8F0", "#FAF089", "#68D391", "#FBD38D"]):
        ax.add_patch(Circle((0, 0), r, fc=c, ec="#555"))
    ax.add_patch(Circle((0, 0), 5, fc="#2D3748")); ax.text(0, 0, "Kota", ha="center", va="center", color="white", fontsize=9)
    for i, r in enumerate([11.5, 22.5, 31.5, 40.5]):
        ax.text(0, r, str(i + 1), ha="center", va="center", fontsize=15, fontweight="bold")
    ax.set_title("Model cincin penggunaan lahan von Thünen")
    save(fig, path)


def f_bidrent(path):
    d = np.linspace(0, 100, 200)
    sayur = np.clip(3000 - 120 * d, 0, None); gandum = np.clip(1000 - 10 * d, 0, None)
    fig, ax = new(8.5, 4.6)
    ax.plot(d, sayur, color=C["green"], lw=2.4, label="Sayur: R = 3.000 − 120d")
    ax.plot(d, gandum, color=C["yellow"], lw=2.4, label="Gandum: R = 1.000 − 10d")
    ax.set_xlabel("Jarak dari pasar, d (km)"); ax.set_ylabel("Sewa lokasi (ribu Rp/ha)")
    ax.legend(frameon=False); ax.grid(color="#EDF2F7"); ax.set_xlim(0, 100); ax.set_ylim(0, 3200)
    ax.set_title("Kurva sewa lokasi dua komoditas")
    save(fig, path)


def f_produktivitas(path):
    table([["A", "50.000", "280.000"], ["B", "30.000", "186.000"], ["C", "70.000", "343.000"]],
          ["Kabupaten", "Luas panen padi (ha)", "Produksi gabah (ton)"], path, title="Data padi tiga kabupaten", col_w=[0.24, 0.38, 0.38])


def f_ntp(path):
    table([["Tanaman pangan", "118", "120"], ["Hortikultura", "125", "118"], ["Perkebunan rakyat", "112", "119"]],
          ["Subsektor", "Harga diterima (It)", "Harga dibayar (Ib)"], path,
          title="Indeks harga petani di Provinsi P", col_w=[0.3, 0.35, 0.35])


def f_kedelai(path):
    bars(["Produksi", "Impor", "Ekspor"], {"Juta ton": [0.6, 2.4, 0.0]}, path, title="Neraca kedelai Indonesia dalam satu tahun (disederhanakan)",
         ylabel="juta ton", values=True, ylim=(0, 3), colors=[C["green"]], w=7)


def f_kc(path):
    days = [0, 20, 20, 50, 50, 90, 90, 110]
    kc = [1.05, 1.05, 1.05, 1.20, 1.20, 1.20, 1.20, 0.90]
    fig, ax = new(8.5, 4.2)
    ax.plot([0, 20, 50, 90, 110], [1.05, 1.05, 1.20, 1.20, 0.90], color=C["green"], lw=2.6, marker="o")
    for x0, x1, n in [(0, 20, "awal"), (20, 50, "pertumbuhan"), (50, 90, "pertengahan"), (90, 110, "akhir")]:
        ax.axvspan(x0, x1, color="#EDF2F7" if n in ("awal", "pertengahan") else "white"); ax.text((x0 + x1) / 2, 1.27, n, ha="center", fontsize=10)
    ax.set_ylim(0.8, 1.32); ax.set_xlabel("Hari setelah tanam"); ax.set_ylabel("Koefisien tanaman (Kc)")
    ax.set_title("Nilai Kc padi sawah menurut fase pertumbuhan")
    save(fig, path)


# ---- paket 1
def f_sistem(path):
    table([["K", "lahan sangat luas, mesin besar, tenaga kerja sedikit, hasil dijual"], ["L", "lahan sempit, tenaga kerja sangat banyak, padi sawah, hasil dikonsumsi sendiri"],
           ["M", "membuka hutan dengan tebas-bakar, ditanam 2–3 tahun lalu ditinggalkan"], ["N", "satu jenis tanaman tahunan dalam skala besar untuk ekspor"]],
          ["Sistem", "Ciri utama"], path, title="Ciri empat sistem pertanian", col_w=[0.13, 0.87], fs=11)


def f_komoditas(path):
    cmap = {}
    for p in ["Riau", "Kalimantan Tengah", "Kalimantan Barat", "Sumatera Utara", "Jambi"]: cmap[p] = "#F6AD55"
    for p in ["Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara", "Sulawesi Barat"]: cmap[p] = "#9F7AEA"
    for p in ["Lampung", "Sumatera Selatan", "Bengkulu"]: cmap[p] = "#8B5A2B"
    for p in ["Maluku", "Maluku Utara"]: cmap[p] = "#F687B3"
    fig, ax = indonesia_map(colors=cmap, w=10, h=4.8)
    legend_patches(ax, [("Komoditas K", "#F6AD55"), ("Komoditas L", "#9F7AEA"), ("Komoditas M", "#8B5A2B"), ("Komoditas N", "#F687B3")], loc="lower left")
    ax.set_title("Provinsi sentra empat komoditas perkebunan (disederhanakan)")
    save(fig, path)


def f_poltanam(path):
    P = [330, 300, 270, 200, 120, 70, 40, 35, 60, 130, 230, 310]
    fig, ax = new(9.5, 4.6)
    ax.bar(range(12), P, color=C["lblue"], edgecolor=C["blue"]); ax.set_xticks(range(12)); ax.set_xticklabels(BULAN3)
    ax.set_ylabel("Curah hujan (mm)"); ax.set_ylim(0, 420)
    for x0, x1, n, c in [(-0.5, 3.0, "Padi MT-I", "#68D391"), (3.0, 6.5, "Padi MT-II", "#38A169"), (6.5, 9.5, "Palawija", "#F6E05E"), (9.5, 11.5, "Olah tanah\n& semai", "#E2E8F0")]:
        ax.add_patch(Rectangle((x0, 365), x1 - x0, 40, fc=c, ec="black")); ax.text((x0 + x1) / 2, 385, n, ha="center", va="center", fontsize=9)
    ax.set_title("Curah hujan dan pola tanam di Kabupaten J")
    save(fig, path)


def f_gurem(path):
    bars(["< 0,5 ha", "0,5–1 ha", "1–2 ha", "> 2 ha"], {"Rumah tangga petani (%)": [60, 20, 12, 8]}, path,
         title="Rumah tangga petani menurut luas garapan di Jawa (ilustrasi)", ylabel="%", values=True, ylim=(0, 70),
         colors=[C["brown"]], w=8)


def f_enso_padi(path):
    pts = [("1997", 1.9, -6.5), ("2015", 2.4, -5.0), ("2023", 1.9, -4.2), ("2019", 0.6, -1.5), ("2004", 0.7, -0.8), ("2014", 0.4, 0.5),
           ("2010", -1.4, 3.8), ("2021", -1.0, 2.0), ("2016", -0.6, 1.6), ("2008", -0.8, 2.6)]
    scatter(pts, path, title="ONI kemarau dan anomali produksi padi gadu (ilustrasi)", xlabel="ONI Juni–September (°C)",
            ylabel="Anomali produksi padi (%)", fit=True)


# ---- paket 2
def f_ayakan(path):
    table([["Berat contoh tanah kering", "80 g"], ["Fraksi pasir", "32 g"], ["Fraksi debu", "28 g"], ["Fraksi liat", "sisanya"]],
          ["Hasil analisis tekstur", "Nilai"], path, title="Analisis tekstur contoh tanah sawah", col_w=[0.6, 0.4])


def f_sesuai(path):
    table([["Suhu rata-rata", "26 °C", "S1"], ["Curah hujan tahunan", "1.400 mm", "S2"], ["Drainase tanah", "sangat cepat", "S3"],
           ["pH tanah", "6,2", "S1"], ["Kedalaman efektif", "60 cm", "S2"]],
          ["Karakteristik lahan", "Nilai", "Kelas per faktor"], path, title="Evaluasi kesesuaian lahan untuk padi sawah di lokasi T",
          col_w=[0.42, 0.3, 0.28])


def f_efisiensi(path):
    bars(["Irigasi genangan", "Irigasi curah (sprinkler)", "Irigasi tetes"], {"Efisiensi (%)": [40, 75, 90]}, path,
         title="Efisiensi pemberian air beberapa metode irigasi", ylabel="%", values=True, ylim=(0, 100), colors=[C["blue"]], w=8)


def f_panas(path):
    t = [29, 30, 31, 32, 33, 34, 35, 36, 37]
    f = [90, 90, 89, 87, 82, 70, 55, 38, 22]
    lines(t, {"Persentase gabah bernas (%)": f}, path, title="Suhu saat pembungaan dan gabah bernas (ilustrasi)",
          xlabel="Suhu maksimum harian saat pembungaan (°C)", ylabel="%", w=8.5)


def f_ph_tanah(path):
    bars(["Petak A", "Petak B", "Petak C", "Petak D"], {"pH tanah": [6.4, 4.4, 7.1, 5.9]}, path, title="pH tanah empat petak sawah", ylabel="pH",
         values=True, ylim=(0, 9), colors=[C["teal"]], w=7.5, hline=5.5)


# ---- paket 3
def f_konservasi(path):
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4))
    for a in axs:
        a.set_xlim(0, 10); a.set_ylim(0, 7); a.axis("off")
    xs, ys = [0], [0.5]
    for i in range(5):
        xs += [xs[-1] + 1.6, xs[-1] + 1.6 + 0.2]; ys += [ys[-1], ys[-1] + 1.1]
    axs[0].fill_between(xs, 0, ys, color="#C6A77B", step=None); axs[0].set_title("1")
    axs[1].fill_between([0, 10], [0, 0], [0.5, 6], color="#C6A77B")
    for x in np.arange(1, 10, 1.6):
        axs[1].add_patch(Ellipse((x, 0.5 + 0.55 * x + 0.2), 0.9, 0.5, fc="#68D391"))
    axs[1].set_title("2")
    axs[2].fill_between([0, 10], [0, 0], [0.5, 6], color="#C6A77B")
    for x0 in [0.5, 3.5, 6.5]:
        axs[2].fill_between([x0, x0 + 1.5], [0.5 + 0.55 * x0, 0.5 + 0.55 * (x0 + 1.5)], [0.9 + 0.55 * x0, 0.9 + 0.55 * (x0 + 1.5)], color="#38A169")
    axs[2].set_title("3")
    fig.suptitle("Tiga teknik konservasi tanah pada lahan miring (penampang)", fontweight="bold")
    save(fig, path)


def f_erosi(path):
    bars(["Tanpa konservasi", "Guludan searah kontur", "Teras bangku", "Agroforestri + teras"], {"Erosi (ton/ha/tahun)": [120, 70, 18, 12]}, path,
         title="Hasil petak percobaan erosi pada lereng 25%", ylabel="ton/ha/tahun", values=True, ylim=(0, 140), colors=[C["brown"]], rot=10, w=8.5)


def f_ikan(path):
    yr = [2000, 2004, 2008, 2012, 2016, 2020, 2024]
    lines(yr, {"Perikanan tangkap": [4.1, 4.7, 5.0, 5.4, 6.6, 7.0, 7.3], "Perikanan budi daya": [1.0, 1.5, 3.9, 9.7, 16.0, 15.4, 17.0]}, path,
          title="Produksi perikanan Indonesia (juta ton, termasuk rumput laut; ilustrasi)", ylabel="juta ton", xlabel="Tahun", w=9)


def f_fcr(path):
    bars(["Sapi potong", "Babi", "Ayam pedaging", "Ikan nila"], {"kg pakan per kg pertambahan bobot": [8, 4, 1.8, 1.5]}, path,
         title="Rasio konversi pakan beberapa ternak dan ikan (ilustrasi)", ylabel="kg pakan / kg bobot", values=True, ylim=(0, 9.5),
         colors=[C["orange"]], w=8)


def f_salin(path):
    d = [0.5, 1, 2, 3, 5, 8]
    fig, ax = new(8.5, 4.4)
    ax.plot(d, [12, 9, 5, 3, 1.5, 0.8], color=C["red"], marker="o", lw=2.2, label="Salinitas air irigasi (‰)")
    ax.set_ylabel("Salinitas (‰)", color=C["red"]); ax.set_xlabel("Jarak dari garis pantai (km)")
    ax2 = ax.twinx(); ax2.plot(d, [1.2, 2.4, 4.1, 5.2, 5.8, 6.0], color=C["green"], marker="s", lw=2.2, label="Produktivitas padi (ton/ha)")
    ax2.set_ylabel("ton/ha", color=C["green"]); ax2.spines["top"].set_visible(False)
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="center right", frameon=False)
    ax.set_title("Salinitas dan produktivitas padi di pesisir Kabupaten D")
    save(fig, path)


# ---- paket 4
def f_engel(path):
    bars(["Kuintil 1\n(termiskin)", "Kuintil 2", "Kuintil 3", "Kuintil 4", "Kuintil 5\n(terkaya)"], {"Porsi pengeluaran pangan (%)": [65, 59, 53, 46, 35]}, path,
         title="Porsi pengeluaran untuk pangan menurut kelompok pendapatan", ylabel="% dari total pengeluaran", values=True, ylim=(0, 75),
         colors=[C["orange"]], w=8.5)


def f_dayadukung(path):
    table([["A", "3.000", "50.000", "0,08"], ["B", "8.000", "40.000", "0,10"], ["C", "5.000", "62.500", "0,08"]],
          ["Wilayah", "Lp (ha)", "Pd (jiwa)", "KFM (ha/orang)"], path,
          title="Data daya dukung lahan pertanian tiga wilayah", col_w=[0.16, 0.32, 0.26, 0.26])


def f_neraca(path):
    table([["Produksi beras", "2.500.000 ton"], ["Impor", "300.000 ton"], ["Ekspor", "100.000 ton"], ["Susut dan tercecer", "10% dari pasokan"],
           ["Penggunaan nonpangan (benih, industri, pakan)", "200.000 ton"], ["Jumlah penduduk", "20 juta jiwa"]],
          ["Komponen neraca", "Nilai"], path, title="Neraca beras Provinsi R dalam satu tahun", col_w=[0.6, 0.4])


def f_fao(path):
    yr = np.arange(2000, 2025)
    idx = np.interp(yr, [2000, 2005, 2007, 2008, 2009, 2011, 2014, 2016, 2019, 2020, 2021, 2022, 2023, 2024],
                    [53, 66, 94, 118, 92, 131, 115, 92, 95, 98, 125, 144, 124, 122])
    lines(yr, {"Indeks harga pangan": idx}, path, title="Indeks harga pangan dunia (2014–2016 = 100; disederhanakan)", xlabel="Tahun",
          ylabel="indeks", w=9, annotate=lambda ax: [ax.annotate(t, (x, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=10, fontweight="bold")
                                                      for t, x, y in [("P", 2008, 118), ("Q", 2011, 131), ("R", 2022, 144)]])


def f_swasembada(path):
    yr = np.arange(2012, 2025)
    prod = 31 + 0.15 * (yr - 2012) - 0.02 * (yr - 2012) ** 2
    cons = 28.5 + 0.45 * (yr - 2012)
    lines(yr, {"Produksi beras domestik": prod, "Konsumsi beras": cons}, path, title="Produksi dan konsumsi beras Negara N (juta ton; ilustrasi)",
          xlabel="Tahun", ylabel="juta ton", w=9)


# ---- paket 5
def f_sawah(path):
    lines([2013, 2015, 2017, 2019], {"Luas baku sawah (juta ha)": [8.13, 7.92, 7.70, 7.46]}, path, title="Luas baku sawah Indonesia (disederhanakan)",
          xlabel="Tahun", ylabel="juta ha", w=8)


def f_loss(path):
    bars(["Panen", "Pascapanen\n& penyimpanan", "Pengolahan\n& distribusi", "Ritel", "Konsumen\n(rumah tangga)"], {"Persentase hilang/terbuang": [3, 5, 4, 2, 11]}, path,
         title="Kehilangan dan pemborosan pangan sepanjang rantai pasok (ilustrasi)", ylabel="% dari produksi", values=True, ylim=(0, 13),
         colors=[C["red"]], w=9)


def f_emisi_pangan(path):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    d = [31, 27, 24, 18]; lab = ["Peternakan & perikanan", "Produksi tanaman", "Perubahan penggunaan lahan", "Rantai pasok\n(olah, kemas, angkut, ritel)"]
    ax.pie(d, labels=[f"{l}\n{v}%" for l, v in zip(lab, d)], colors=[C["red"], C["yellow"], C["green"], C["gray"]], startangle=90, wedgeprops=dict(ec="white"),
           textprops=dict(fontsize=10))
    ax.set_title("Emisi GRK sistem pangan global (ilustrasi)")
    save(fig, path)


def f_harga(path):
    bars(["Jawa Timur", "Sulawesi Selatan", "DKI Jakarta", "NTT", "Papua Pegunungan"], {"Rp/kg": [12500, 12300, 14200, 14800, 19500]}, path,
         title="Harga rata-rata beras medium di beberapa provinsi (ilustrasi)", ylabel="Rp per kg", values=True, ylim=(0, 22000), colors=[C["teal"]], rot=10, w=9)


NDVI = np.array([[0.78, 0.80, 0.81, 0.79, 0.77], [0.79, 0.52, 0.48, 0.80, 0.78], [0.80, 0.50, 0.46, 0.79, 0.81], [0.77, 0.79, 0.80, 0.78, 0.30],
                 [0.79, 0.81, 0.80, 0.29, 0.28]])


def f_ndvi_grid(path):
    fig, ax = new(6.5, 6)
    im = ax.imshow(NDVI, cmap="RdYlGn", vmin=0, vmax=1)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, f"{NDVI[i, j]:.2f}".replace(".", ","), ha="center", va="center", fontsize=10, fontweight="bold")
    ax.set_xticks(range(5)); ax.set_xticklabels(list("12345")); ax.set_yticks(range(5)); ax.set_yticklabels(list("ABCDE"))
    plt.colorbar(im, ax=ax, fraction=0.046, label="NDVI")
    ax.set_title("Peta NDVI hasil drone di sebidang sawah\n(umur 60 hari, varietas dan pemupukan seragam)")
    save(fig, path)


# ============================ questions ============================
P0 = [
    Q("Perhatikan model cincin penggunaan lahan von Thünen berikut.\n\nDalam model klasik von Thünen, cincin yang dimanfaatkan untuk hutan penghasil kayu bakar dan kayu bangunan adalah nomor …",
      ["2", "1", "3", "4", "1 dan 4"],
      "Model klasik von Thünen (1826) menyusun penggunaan lahan pertanian dalam cincin konsentris di sekitar kota pasar:\n1) Hortikultura dan peternakan susu: produk mudah rusak sehingga harus dekat pasar.\n2) Hutan untuk kayu bakar dan kayu bangunan: kayu berat dan dibutuhkan dalam jumlah besar, sehingga biaya angkutnya tinggi.\n3) Tanaman pangan biji-bijian dengan rotasi (gandum).\n4) Peternakan ekstensif (ranch) yang membutuhkan lahan luas tetapi biaya angkut per nilai produk rendah.\nPenempatan hutan di cincin kedua mengejutkan banyak orang, tetapi masuk akal pada masa itu karena kayu adalah sumber energi utama dan berat diangkut.\n\nPengecoh: cincin 1 untuk produk mudah rusak, cincin 3 untuk biji-bijian, dan cincin 4 untuk peternakan ekstensif.",
      f_thunen),
    Q("Sebuah komoditas menghasilkan Y = 10 ton/ha dengan harga pasar p = Rp500 ribu/ton, biaya produksi c = Rp300 ribu/ton, dan biaya angkut f = Rp5 ribu/ton/km. Dengan R = Y(p − c) − Yfd, sewa lokasi pada jarak 20 km dan batas jarak terjauh budi dayanya adalah …",
      ["Rp1 juta/ha dan 40 km", "Rp2 juta/ha dan 40 km", "Rp1 juta/ha dan 20 km", "Rp3 juta/ha dan 60 km", "Rp1 juta/ha dan 100 km"],
      "1) R = Y(p − c) − Yfd = 10 × (500 − 300) − 10 × 5 × 20 = 2.000 − 1.000 = 1.000 ribu = Rp1 juta per ha.\n2) Batas budi daya terjauh tercapai ketika R = 0: d = (p − c) ÷ f = 200 ÷ 5 = 40 km.\nDi luar 40 km, biaya angkut melebihi keuntungan produksi sehingga komoditas tersebut tidak lagi menguntungkan.\n\nPengecoh: Rp2 juta/ha adalah keuntungan sebelum dikurangi biaya angkut. 20 km adalah jarak yang ditanyakan, bukan batas. 60 km dan 100 km berasal dari salah membagi (misalnya 300 ÷ 5 atau 500 ÷ 5).",
      None),
    Q("Perhatikan kurva sewa lokasi dua komoditas berikut.\n\nBatas penggunaan lahan antara sayur dan gandum terletak pada jarak sekitar …",
      ["18 km dari pasar", "25 km dari pasar", "100 km dari pasar", "9 km dari pasar", "50 km dari pasar"],
      "Petani memilih komoditas yang memberikan sewa lokasi (keuntungan per hektare) tertinggi. Batas kedua penggunaan lahan berada pada titik potong kedua garis:\n3.000 − 120d = 1.000 − 10d → 2.000 = 110d → d ≈ 18,2 km.\nDi dekat pasar (< 18 km), sayur lebih menguntungkan karena hasil per hektare tinggi walaupun biaya angkutnya besar dan mudah rusak. Di luar 18 km hingga 100 km, gandum lebih menguntungkan.\n\nPengecoh: 25 km adalah batas terjauh sayur (R sayur = 0). 100 km adalah batas terjauh gandum. 9 km dan 50 km tidak sesuai perhitungan. Model ini menjelaskan mengapa sentra sayur sering berada di pinggiran kota besar.",
      f_bidrent),
    Q("Revolusi Hijau berhasil meningkatkan produksi padi Indonesia hingga swasembada beras pada 1984, tetapi juga menimbulkan dampak negatif. Dampak negatif yang paling tepat adalah …",
      ["Ketergantungan pada pupuk kimia dan pestisida serta hilangnya varietas lokal", "Produksi padi turun drastis karena varietas unggul tidak cocok di Indonesia",
       "Petani beralih seluruhnya ke tanaman perkebunan untuk ekspor", "Kebutuhan air irigasi berkurang sehingga waduk tidak lagi diperlukan",
       "Lahan sawah bertambah luas karena hutan otomatis berubah menjadi sawah"],
      "Revolusi Hijau memperkenalkan paket teknologi (Panca Usaha Tani): bibit unggul, pemupukan, pemberantasan hama, irigasi, dan cara bercocok tanam yang baik. Produksi padi melonjak, tetapi dampak negatifnya antara lain: (1) ketergantungan pada pupuk kimia dan pestisida yang mahal; (2) penurunan kesuburan dan kerusakan struktur tanah; (3) ledakan hama seperti wereng cokelat akibat resistensi; (4) hilangnya ribuan varietas padi lokal (erosi genetik); dan (5) kesenjangan antara petani kaya dan gurem.\n\nPengecoh: produksi justru naik pesat. Petani tetap menanam padi. Varietas unggul memerlukan air irigasi lebih banyak, bukan lebih sedikit. Perluasan sawah tidak terjadi secara otomatis.",
      None),
    Q("Perhatikan data padi tiga kabupaten berikut.\n\nKabupaten dengan produktivitas tertinggi beserta nilainya adalah …",
      ["B, sekitar 6,2 ton/ha", "C, sekitar 4,9 ton/ha", "A, sekitar 5,6 ton/ha", "C, sekitar 343 ton/ha", "B, sekitar 0,16 ton/ha"],
      "Produktivitas = produksi ÷ luas panen.\n• A: 280.000 ÷ 50.000 = 5,6 ton/ha.\n• B: 186.000 ÷ 30.000 = 6,2 ton/ha.\n• C: 343.000 ÷ 70.000 = 4,9 ton/ha.\nKabupaten B memiliki produktivitas tertinggi walaupun produksi totalnya paling kecil. Kabupaten C memiliki produksi terbesar karena luas panennya terbesar, tetapi produktivitasnya terendah.\n\nPengecoh: C dipilih bila hanya melihat produksi total. 343 ton/ha adalah salah membaca angka. 0,16 ton/ha muncul bila pembagian dibalik (luas ÷ produksi). Ingat juga perbedaan luas panen dan luas baku sawah: satu hektare sawah yang ditanam dua kali setahun dihitung sebagai dua hektare luas panen.",
      f_produktivitas),
    Q("Sebuah kabupaten memiliki luas baku sawah 2.000 ha dengan indeks pertanaman (IP) 250 dan produktivitas 5,5 ton/ha. Produksi gabah tahunan kabupaten tersebut adalah …",
      ["27.500 ton", "11.000 ton", "2.750.000 ton", "13.750 ton", "55.000 ton"],
      "Produksi tahunan = luas baku × IP × produktivitas.\nIP 250 berarti rata-rata lahan ditanami 2,5 kali dalam setahun (misalnya sebagian lahan tiga kali, sebagian dua kali).\nProduksi = 2.000 × 2,5 × 5,5 = 27.500 ton gabah.\n\nPengecoh: 11.000 ton mengabaikan IP (hanya satu kali tanam). 2.750.000 ton memakai IP 250 sebagai angka 250, bukan 2,5. 13.750 ton memakai IP 1,25. 55.000 ton memakai IP 5. Peningkatan IP melalui irigasi dan varietas berumur pendek adalah strategi menaikkan produksi tanpa menambah luas sawah.",
      None),
    Q("Perhatikan tabel indeks harga petani di Provinsi P berikut. Nilai Tukar Petani NTP = (It ÷ Ib) × 100.\n\nSubsektor yang petaninya mengalami surplus (daya beli meningkat) adalah …",
      ["Hortikultura, dengan NTP sekitar 105,9", "Tanaman pangan, dengan NTP sekitar 98,3", "Perkebunan rakyat, dengan NTP sekitar 94,1",
       "Tanaman pangan, dengan NTP sekitar 101,7", "Semua subsektor karena It selalu di atas 100"],
      "Hitung NTP:\n• Tanaman pangan: 118 ÷ 120 × 100 ≈ 98,3.\n• Hortikultura: 125 ÷ 118 × 100 ≈ 105,9.\n• Perkebunan rakyat: 112 ÷ 119 × 100 ≈ 94,1.\nNTP > 100 berarti kenaikan harga yang diterima petani lebih cepat daripada kenaikan harga yang dibayar petani (untuk konsumsi dan biaya produksi), sehingga petani mengalami surplus. Hanya hortikultura yang memenuhi syarat ini.\n\nPengecoh: tanaman pangan dan perkebunan memiliki NTP di bawah 100 (defisit). Nilai 101,7 muncul bila pembagian dibalik (120 ÷ 118). It di atas 100 tidak cukup karena harus dibandingkan dengan Ib.",
      f_ntp),
    Q("Seorang balita di daerah lumbung beras tetap mengalami stunting walaupun beras tersedia melimpah dan harganya terjangkau. Pilar ketahanan pangan yang paling bermasalah adalah …",
      ["Pemanfaatan pangan, yaitu asupan gizi seimbang, sanitasi, dan pola asuh", "Ketersediaan pangan, yaitu jumlah produksi pangan di wilayah tersebut",
       "Akses pangan, yaitu kemampuan ekonomi rumah tangga untuk membeli pangan", "Stabilitas pangan, yaitu fluktuasi harga pangan antarmusim",
       "Ketersediaan dan akses pangan secara bersamaan"],
      "Ketahanan pangan memiliki empat pilar: (1) ketersediaan (produksi, cadangan, impor); (2) akses (kemampuan fisik dan ekonomi memperoleh pangan); (3) pemanfaatan (cara pangan diolah, dikonsumsi, dan diserap tubuh, termasuk keragaman gizi, air bersih, sanitasi, kesehatan, dan pola asuh); serta (4) stabilitas (ketiga pilar terjaga sepanjang waktu).\nPada kasus ini beras tersedia dan terjangkau, sehingga ketersediaan dan akses tidak bermasalah. Stunting terjadi karena asupan gizi tidak seimbang (kekurangan protein dan mikronutrien), infeksi berulang akibat sanitasi buruk, atau pola asuh yang kurang tepat. Itu masalah pilar pemanfaatan.\n\nPengecoh: ketersediaan, akses, dan stabilitas tidak menjadi persoalan utama dalam kasus ini.",
      None),
    Q("Perhatikan grafik neraca kedelai Indonesia berikut. Rasio swasembada = produksi ÷ (produksi + impor − ekspor) × 100%.\n\nRasio swasembada kedelai adalah …",
      ["20%", "25%", "80%", "400%", "300%"],
      "Konsumsi nasional (penggunaan domestik) ≈ produksi + impor − ekspor = 0,6 + 2,4 − 0 = 3,0 juta ton.\nRasio swasembada = 0,6 ÷ 3,0 × 100% = 20%.\nArtinya hanya seperlima kebutuhan kedelai (bahan tahu dan tempe) yang dipenuhi produksi dalam negeri. Penyebabnya antara lain kedelai adalah tanaman subtropis yang produktivitasnya rendah di iklim tropis basah, harganya kalah bersaing dengan kedelai impor, dan petani lebih memilih menanam padi atau jagung.\n\nPengecoh: 25% membagi produksi dengan impor (0,6 ÷ 2,4). 80% adalah porsi impor. 400% dan 300% berasal dari pembagian terbalik.",
      f_kedelai),
    Q("Perhatikan grafik nilai Kc padi sawah menurut fase pertumbuhan berikut. Jika evapotranspirasi acuan ET₀ = 5 mm/hari, kebutuhan air tanaman per hari untuk 100 ha sawah pada fase pertengahan adalah …",
      ["6.000 m³", "5.000 m³", "600 m³", "60.000 m³", "5.250 m³"],
      "1) Pada fase pertengahan, Kc = 1,20.\n2) ETc = Kc × ET₀ = 1,20 × 5 = 6 mm/hari.\n3) Ingat konversi: 1 mm air pada lahan 1 ha = 10 m³. Jadi 6 mm × 10 m³ = 60 m³ per ha per hari.\n4) Untuk 100 ha: 60 × 100 = 6.000 m³ per hari.\nKebutuhan air tertinggi terjadi pada fase pertengahan (pembentukan malai dan pembungaan), sehingga kekurangan air pada fase ini paling merugikan hasil.\n\nPengecoh: 5.000 m³ mengabaikan Kc (hanya ET₀). 600 m³ dan 60.000 m³ adalah kesalahan konversi satuan. 5.250 m³ memakai Kc fase awal (1,05).",
      f_kc),
]

P1 = [
    Q("Perhatikan ciri empat sistem pertanian berikut.\n\nPasangan sistem dan namanya menurut klasifikasi Whittlesey yang tepat adalah …",
      ["L – pertanian subsisten intensif padi; N – perkebunan", "K – ladang berpindah; M – pertanian komersial ekstensif",
       "L – perkebunan; N – pertanian subsisten intensif padi", "M – perkebunan; K – peternakan nomaden", "N – ladang berpindah; L – pertanian komersial ekstensif"],
      "Identifikasi berdasarkan ciri:\n• K: lahan sangat luas, mesin besar, tenaga kerja sedikit, hasil dijual → pertanian biji-bijian komersial ekstensif (misalnya gandum di Amerika Utara dan Australia).\n• L: lahan sempit, tenaga kerja sangat banyak, padi sawah, hasil sebagian besar dikonsumsi sendiri → pertanian subsisten intensif padi, khas Asia Monsun termasuk Jawa.\n• M: membuka hutan dengan tebas-bakar lalu ditinggalkan → ladang berpindah (perladangan berpindah).\n• N: satu jenis tanaman tahunan skala besar untuk ekspor → perkebunan (plantation), misalnya sawit dan karet.\nPasangan yang benar adalah L dan N.\n\nPengecoh: opsi lain menukar sistem dengan namanya.",
      f_sistem),
    Q("Perladangan berpindah dengan masa bera 15–20 tahun dapat lestari, tetapi menjadi merusak ketika masa beranya dipersingkat menjadi 2–3 tahun. Penjelasan yang paling tepat adalah …",
      ["Masa bera singkat tidak cukup untuk memulihkan hara dan vegetasi sehingga lahan terdegradasi",
       "Masa bera singkat membuat hutan tumbuh terlalu lebat sehingga sulit dibuka kembali",
       "Perladangan berpindah selalu merusak berapa pun lama masa beranya",
       "Masa bera singkat meningkatkan kesuburan karena abu pembakaran lebih sering diberikan",
       "Lahan bera hanya dapat ditanami kembali setelah 50 tahun pada semua kondisi"],
      "Pada perladangan berpindah, hara tanah tropis yang miskin terutama berasal dari abu pembakaran biomassa. Setelah 2–3 tahun ditanami, hara habis dan gulma meningkat, sehingga lahan ditinggalkan (bera). Masa bera yang panjang (15–20 tahun) memberi kesempatan hutan sekunder tumbuh kembali dan mengakumulasi hara di biomassa. Ketika tekanan penduduk memaksa masa bera dipersingkat, vegetasi dan hara belum pulih; tanah makin miskin, erosi meningkat, dan lahan dapat berubah menjadi padang alang-alang yang kritis.\n\nPengecoh: masa bera singkat justru menghasilkan vegetasi tipis. Perladangan berpindah dengan bera panjang dan penduduk jarang dapat lestari. Abu yang sering tetapi sedikit tidak memulihkan kesuburan. Lama bera bergantung kondisi lokal, bukan selalu 50 tahun.",
      None),
    Q("Perhatikan peta provinsi sentra empat komoditas perkebunan berikut.\n\nKomoditas L yang sentranya terkonsentrasi di Pulau Sulawesi paling mungkin adalah …",
      ["Kakao", "Kelapa sawit", "Kopi robusta", "Cengkih", "Karet"],
      "Sebaran komoditas pada peta:\n• K (oranye) di Riau, Sumatera Utara, Jambi, Kalimantan Barat, dan Kalimantan Tengah → kelapa sawit.\n• L (ungu) di Sulawesi Tengah, Selatan, Tenggara, dan Barat → kakao. Sulawesi adalah sentra kakao nasional karena iklim, tanah, dan sejarah pengembangan perkebunan rakyat sejak 1980-an.\n• M (cokelat) di Lampung, Sumatera Selatan, dan Bengkulu → kopi robusta.\n• N (merah muda) di Maluku dan Maluku Utara → cengkih dan pala (rempah).\nKaret juga banyak di Sumatra dan Kalimantan, bukan Sulawesi.\n\nPengecoh: kelapa sawit, kopi robusta, dan cengkih sesuai dengan warna lain pada peta.",
      f_komoditas),
    Q("Sebagian besar petani di Jawa tergolong petani gurem. Masalah utama yang ditimbulkan oleh kondisi ini adalah …",
      ["Lahan garapan sangat sempit sehingga pendapatan rendah dan sulit menerapkan mekanisasi", "Lahan garapan terlalu luas sehingga petani kekurangan tenaga kerja",
       "Produktivitas per hektare selalu lebih rendah daripada perkebunan besar", "Petani gurem tidak menanam tanaman pangan sehingga Jawa kekurangan beras",
       "Petani gurem hanya terdapat di kota besar sehingga tidak memengaruhi pertanian"],
      "Petani gurem adalah petani yang menguasai lahan kurang dari 0,5 ha. Pewarisan lahan yang terus membagi lahan (fragmentasi) dan alih fungsi sawah membuat jumlahnya meningkat. Dengan lahan sesempit itu, pendapatan dari usaha tani tidak mencukupi kebutuhan keluarga, skala usaha tidak ekonomis untuk mekanisasi, akses kredit sulit, dan banyak anak muda enggan menjadi petani. Akibatnya terjadi urbanisasi dan pekerjaan sampingan di luar pertanian.\n\nPengecoh: masalahnya justru lahan terlalu sempit. Produktivitas per hektare sawah petani kecil di Jawa sebenarnya bisa tinggi. Petani gurem banyak menanam padi. Petani gurem terutama berada di perdesaan.",
      None),
    Q("Perhatikan grafik curah hujan dan pola tanam di Kabupaten J berikut.\n\nAlasan utama palawija ditanam pada Juli–September adalah …",
      ["Curah hujan rendah sehingga air tidak cukup untuk padi, sedangkan palawija lebih hemat air",
       "Curah hujan sangat tinggi sehingga palawija lebih tahan genangan daripada padi",
       "Palawija hanya dapat tumbuh pada suhu dingin yang terjadi pada Juli–September",
       "Harga palawija selalu paling tinggi pada musim hujan sehingga petani menunda panen",
       "Padi tidak boleh ditanam pada Juli–September karena peraturan daerah"],
      "Grafik menunjukkan curah hujan tinggi pada November–April (musim hujan) dan sangat rendah pada Juni–September (puncak kemarau, < 70 mm). Pola tanam padi–padi–palawija memanfaatkan ketersediaan air: padi musim tanam I dan II ditanam saat air melimpah, sedangkan palawija (jagung, kedelai, kacang hijau) ditanam saat kemarau karena kebutuhan airnya jauh lebih kecil daripada padi sawah. Rotasi dengan palawija juga memutus siklus hama padi dan, untuk kacang-kacangan, menambah nitrogen tanah.\n\nPengecoh: Juli–September justru kering. Suhu di Indonesia relatif stabil sepanjang tahun. Harga dan peraturan daerah bukan alasan utama pola tanam ini.",
      f_poltanam),
    Q("Program reforma agraria bertujuan antara lain meredistribusi tanah dan memberikan kepastian hukum atas tanah petani. Masalah struktural yang ingin diatasi program ini adalah …",
      ["Ketimpangan penguasaan tanah", "Kekurangan curah hujan di daerah pertanian", "Rendahnya harga pupuk bersubsidi",
       "Tingginya produktivitas padi di Jawa", "Terlalu banyaknya varietas padi lokal"],
      "Reforma agraria adalah penataan kembali struktur penguasaan, pemilikan, penggunaan, dan pemanfaatan tanah agar lebih adil. Di Indonesia, sebagian besar tanah dikuasai oleh sedikit pihak (misalnya konsesi perkebunan dan kehutanan skala besar), sementara jutaan petani gurem atau tunakisma tidak memiliki tanah cukup. Ketimpangan ini memicu kemiskinan perdesaan dan konflik agraria. Program reforma agraria mencakup legalisasi aset (sertifikasi), redistribusi tanah dari Tanah Objek Reforma Agraria (TORA), dan perhutanan sosial.\n\nPengecoh: curah hujan, harga pupuk, produktivitas padi, dan keragaman varietas bukan masalah struktural penguasaan tanah.",
      None),
    Q("Perhatikan grafik sebaran rumah tangga petani menurut luas lahan garapan berikut.\n\nKebijakan yang paling relevan untuk mengatasi masalah yang tergambar adalah …",
      ["Konsolidasi usaha tani melalui korporasi petani dan nilai tambah", "Membagi lahan petani besar menjadi petak-petak yang lebih kecil lagi",
       "Menghapus seluruh program irigasi karena lahan petani terlalu sempit", "Mewajibkan semua petani menanam tanaman perkebunan untuk ekspor",
       "Melarang anak petani bekerja di luar sektor pertanian"],
      "Grafik menunjukkan 60% rumah tangga petani menggarap lahan kurang dari 0,5 ha (petani gurem) dan 80% kurang dari 1 ha. Usaha tani pada lahan sesempit ini sulit mencapai skala ekonomi. Kebijakan yang relevan antara lain konsolidasi usaha (korporasi petani atau koperasi yang mengelola lahan secara kolektif sehingga mekanisasi dan pemasaran lebih efisien), pengembangan komoditas bernilai tinggi (hortikultura), pengolahan hasil pertanian, serta penciptaan lapangan kerja nonpertanian di perdesaan.\n\nPengecoh: membagi lahan memperparah fragmentasi. Irigasi tetap penting. Mewajibkan komoditas tertentu mengabaikan kesesuaian lahan dan pasar. Melarang anak petani bekerja di luar pertanian tidak realistis dan tidak menyelesaikan masalah.",
      f_gurem),
    Q("Sekitar 40% luas perkebunan kelapa sawit di Indonesia dikelola petani rakyat (smallholder). Tantangan utama perkebunan sawit rakyat dibandingkan perkebunan besar adalah …",
      ["Produktivitas rendah akibat bibit, pemupukan, dan legalitas lahan", "Produktivitas selalu lebih tinggi sehingga harga sawit dunia turun",
       "Perkebunan rakyat tidak menghasilkan tandan buah segar sama sekali", "Perkebunan rakyat hanya terdapat di Pulau Jawa yang tidak cocok untuk sawit",
       "Petani rakyat tidak boleh menjual hasil panennya ke pabrik kelapa sawit"],
      "Perkebunan sawit rakyat umumnya memiliki produktivitas lebih rendah (sekitar 2–3 ton CPO/ha) dibandingkan perkebunan besar (4–5 ton CPO/ha). Penyebabnya antara lain bibit tidak bersertifikat, pemupukan kurang karena keterbatasan modal, tanaman yang sudah tua, akses ke pabrik yang terbatas, dan status lahan yang belum legal sehingga sulit memperoleh sertifikasi keberlanjutan (ISPO/RSPO) dan kredit. Program peremajaan sawit rakyat (PSR) ditujukan untuk mengatasi masalah ini.\n\nPengecoh: produktivitas rakyat justru lebih rendah. Perkebunan rakyat menghasilkan TBS. Sebagian besar sawit rakyat berada di Sumatra dan Kalimantan. Petani rakyat dapat menjual TBS ke pabrik.",
      None),
    Q("Perhatikan diagram pencar ONI musim kemarau dan anomali produksi padi musim gadu berikut.\n\nKesimpulan yang paling tepat adalah …",
      ["Semakin positif ONI (El Niño), produksi padi musim gadu cenderung turun", "Semakin positif ONI, produksi padi musim gadu cenderung naik",
       "ONI tidak berhubungan dengan produksi padi karena titik tersebar acak", "La Niña selalu menurunkan produksi padi musim gadu secara drastis",
       "Produksi padi hanya dipengaruhi harga pupuk, bukan iklim"],
      "Titik-titik membentuk pola menurun: tahun El Niño kuat (1997, 2015, 2023 dengan ONI ±1,9–2,4) memiliki anomali produksi negatif besar (−4% hingga −6,5%), sedangkan tahun La Niña (2010, 2008, 2021 dengan ONI negatif) memiliki anomali positif. Hubungan negatif ini terjadi karena El Niño mengurangi hujan musim kemarau sehingga air irigasi untuk musim tanam gadu (kemarau) berkurang, waktu tanam mundur, dan sebagian lahan puso.\nInformasi ini dipakai untuk peringatan dini pertanian, misalnya penyesuaian kalender tanam dan cadangan beras.\n\nPengecoh: arah hubungan bukan positif. Titik tidak acak. La Niña pada grafik justru cenderung menaikkan produksi musim gadu. Iklim jelas berpengaruh selain faktor harga pupuk.",
      f_enso_padi),
    Q("Wilayah sekitar Laut Tengah terkenal dengan pertanian zaitun, anggur, dan jeruk. Ciri iklim yang mendukung sistem pertanian ini adalah …",
      ["Musim panas kering dan musim dingin basah yang sejuk", "Hujan merata sepanjang tahun dengan suhu selalu tinggi",
       "Musim dingin sangat panjang dengan tanah membeku hampir sepanjang tahun", "Musim hujan pada musim panas akibat angin monsun",
       "Curah hujan kurang dari 100 mm per tahun sepanjang tahun"],
      "Iklim Mediterania (Köppen Cs) dicirikan musim panas yang panas dan kering serta musim dingin yang sejuk dan basah. Tanaman khas seperti zaitun, anggur, dan jeruk telah beradaptasi terhadap kekeringan musim panas: akarnya dalam, daunnya tebal atau berlapis lilin untuk mengurangi penguapan. Gandum ditanam pada musim dingin yang basah. Wilayah dengan iklim serupa juga ditemukan di California, Chile tengah, Afrika Selatan bagian barat daya, dan Australia selatan.\n\nPengecoh: hujan merata dan suhu tinggi adalah iklim tropis basah (Af). Musim dingin panjang dan tanah membeku adalah iklim kutub/subarktik. Hujan pada musim panas akibat monsun khas Asia. Curah hujan < 100 mm adalah iklim gurun.",
      None),
]

P2 = [
    Q("Perhatikan hasil analisis tekstur contoh tanah sawah berikut.\n\nPersentase fraksi liat contoh tanah tersebut adalah …",
      ["25%", "20%", "40%", "35%", "50%"],
      "Fraksi liat = berat total − (pasir + debu) = 80 − (32 + 28) = 20 g.\nPersentase = berat fraksi ÷ berat total × 100%.\n• Pasir: 32 ÷ 80 × 100% = 40%.\n• Debu: 28 ÷ 80 × 100% = 35%.\n• Liat: 20 ÷ 80 × 100% = 25%.\nKomposisi 40% pasir, 35% debu, dan 25% liat termasuk kelas tekstur lempung (loam), tekstur yang cukup ideal untuk pertanian karena seimbang antara kemampuan menahan air dan drainase.\n\nPengecoh: 20% adalah berat liat dalam gram, belum dikonversi ke persen. 40% dan 35% adalah persentase pasir dan debu. 50% tidak sesuai perhitungan.",
      f_ayakan),
    Q("Lahan pasang surut di Kalimantan Selatan yang dibuka untuk sawah sering menghadapi masalah tanah sulfat masam. Masalah ini muncul ketika …",
      ["Pirit teroksidasi akibat drainase berlebihan sehingga tanah masam", "Tanah terlalu basa akibat kandungan kapur yang sangat tinggi",
       "Tanah terlalu banyak mengandung bahan organik sehingga sangat subur", "Air pasang membawa pupuk alami yang menaikkan pH tanah",
       "Tanah berpasir kuarsa sehingga tidak dapat menahan air"],
      "Tanah sulfat masam mengandung mineral pirit (FeS₂) yang terbentuk di lingkungan payau tergenang. Selama tergenang, pirit stabil. Ketika lahan dikeringkan secara berlebihan melalui saluran drainase, pirit terpapar oksigen dan teroksidasi menghasilkan asam sulfat. pH tanah dapat turun di bawah 3,5, aluminium dan besi menjadi beracun, dan tanaman padi gagal tumbuh. Pengelolaannya adalah menjaga muka air tetap tinggi, pencucian asam, pemberian kapur, dan pemilihan varietas toleran.\n\nPengecoh: tanah sulfat masam justru sangat masam, bukan basa. Kandungan bahan organik tinggi adalah ciri gambut, dan masalahnya bukan kesuburan berlebih. Air pasang tidak menaikkan pH secara berarti. Tanah pasir kuarsa adalah masalah lain.",
      None),
    Q("Perhatikan hasil evaluasi kesesuaian lahan untuk padi sawah di lokasi T berikut.\n\nKelas kesesuaian lahan aktual lokasi T dan faktor pembatas utamanya adalah …",
      ["S3, dengan faktor pembatas drainase tanah", "S1, karena sebagian besar faktor tergolong S1", "S2, dengan faktor pembatas curah hujan",
       "S2, karena rata-rata kelas semua faktor adalah S2", "N, karena terdapat faktor yang tergolong S2"],
      "Evaluasi kesesuaian lahan menggunakan prinsip faktor pembatas terberat (hukum minimum): kelas kesesuaian ditentukan oleh faktor dengan kelas paling rendah, bukan rata-rata.\nPada lokasi T, drainase tanah yang sangat cepat tergolong S3 (sesuai marginal), sedangkan faktor lain S1 atau S2. Jadi kelas kesesuaian aktual adalah S3 dengan pembatas drainase. Untuk padi sawah, drainase yang terlalu cepat membuat air sulit tergenang.\nBila pembatas dapat diperbaiki (misalnya dengan pelumpuran dan pembuatan lapisan tapak bajak), kelas kesesuaian potensial dapat naik.\n\nPengecoh: kelas tidak ditentukan oleh mayoritas atau rata-rata. Curah hujan bukan pembatas terberat. Kelas N berarti tidak sesuai, sedangkan tidak ada faktor yang tergolong N.",
      f_sesuai),
    Q("Sebuah saluran irigasi mengalirkan air 1,5 liter/detik untuk setiap hektare sawah. Volume air yang dialirkan untuk 100 ha sawah dalam satu hari adalah sekitar …",
      ["12.960 m³", "129.600 m³", "1.296 m³", "150 m³", "8.640 m³"],
      "Konversi: 1 liter/detik selama 1 hari = 86.400 liter = 86,4 m³.\n• Per hektare: 1,5 × 86,4 = 129,6 m³ per hari.\n• Untuk 100 ha: 129,6 × 100 = 12.960 m³ per hari.\nNilai 1,5 L/detik/ha setara tinggi air ±13 mm/hari, cukup untuk memenuhi kebutuhan tanaman padi ditambah perkolasi dan rembesan.\n\nPengecoh: 129.600 dan 1.296 m³ adalah kesalahan faktor sepuluh. 150 m³ mengalikan 1,5 dengan 100 tanpa konversi waktu. 8.640 m³ memakai 1 L/detik, bukan 1,5.",
      None),
    Q("Perhatikan grafik efisiensi beberapa metode irigasi berikut. Kebutuhan air bersih tanaman di sebuah kebun adalah 9.000 m³ per musim. Penghematan air yang diperoleh jika metode irigasi genangan diganti dengan irigasi tetes adalah …",
      ["12.500 m³", "10.000 m³", "22.500 m³", "4.500 m³", "5.000 m³"],
      "Pengambilan air kotor = kebutuhan bersih ÷ efisiensi.\n• Irigasi genangan (40%): 9.000 ÷ 0,40 = 22.500 m³.\n• Irigasi tetes (90%): 9.000 ÷ 0,90 = 10.000 m³.\n• Penghematan = 22.500 − 10.000 = 12.500 m³ per musim.\nIrigasi tetes memberikan air langsung ke zona akar sehingga kehilangan akibat penguapan, limpasan, dan perkolasi sangat kecil. Metode ini cocok untuk hortikultura bernilai tinggi di daerah kering, misalnya NTT dan NTB.\n\nPengecoh: 10.000 dan 22.500 m³ adalah pengambilan air masing-masing metode, bukan penghematannya. 4.500 m³ dan 5.000 m³ berasal dari mengalikan, bukan membagi, dengan efisiensi.",
      f_efisiensi),
    Q("Pada tahun El Niño, petani di daerah tadah hujan sering mengalami gagal tanam pertama. Strategi adaptasi yang paling tepat berdasarkan informasi prakiraan iklim adalah …",
      ["Menyesuaikan waktu tanam dengan prakiraan musim dan varietas tahan kering",
       "Menanam padi lebih awal sebelum hujan turun agar panen lebih cepat",
       "Menambah dosis pupuk urea dua kali lipat untuk mengganti kekurangan air",
       "Mengganti seluruh sawah tadah hujan menjadi kolam ikan permanen",
       "Mengabaikan prakiraan iklim karena El Niño tidak berpengaruh di daerah tadah hujan"],
      "El Niño cenderung memundurkan awal musim hujan dan mengurangi curah hujan. Di sawah tadah hujan yang tidak memiliki irigasi teknis, menanam terlalu awal berisiko gagal karena hujan belum stabil. Adaptasi yang tepat adalah memanfaatkan prakiraan awal musim (misalnya dari BMKG dan Kalender Tanam Terpadu), menunda atau menyesuaikan waktu tanam, memilih varietas umur pendek dan tahan kekeringan, menyiapkan embung atau sumur dangkal, serta mengalihkan sebagian lahan ke palawija.\n\nPengecoh: menanam sebelum hujan stabil meningkatkan risiko gagal tanam. Pupuk tidak dapat menggantikan air. Mengubah seluruh sawah menjadi kolam tidak realistis tanpa sumber air. El Niño justru sangat berpengaruh di daerah tadah hujan.",
      None),
    Q("Perhatikan grafik pengaruh suhu maksimum saat pembungaan terhadap persentase gabah bernas berikut.\n\nInterpretasi yang paling tepat terkait perubahan iklim adalah …",
      ["Suhu di atas ±33 °C saat pembungaan menurunkan gabah bernas", "Kenaikan suhu selalu meningkatkan persentase gabah bernas",
       "Persentase gabah bernas tidak berubah pada kisaran suhu 29–37 °C", "Padi paling produktif pada suhu maksimum di atas 36 °C",
       "Suhu hanya memengaruhi tinggi tanaman, bukan pengisian gabah"],
      "Grafik menunjukkan persentase gabah bernas relatif stabil (±87–90%) hingga suhu maksimum ±32 °C, lalu turun tajam: 82% pada 33 °C, 55% pada 35 °C, dan hanya 22% pada 37 °C. Suhu tinggi saat pembungaan mengganggu viabilitas serbuk sari dan penyerbukan, sehingga banyak gabah hampa. Dengan pemanasan global, frekuensi hari panas meningkat sehingga risiko penurunan hasil padi bertambah. Adaptasinya antara lain varietas toleran panas dan pengaturan waktu tanam agar pembungaan tidak jatuh pada periode terpanas.\n\nPengecoh: kenaikan suhu justru menurunkan gabah bernas setelah ambang tertentu. Persentase berubah nyata. Suhu di atas 36 °C bukan kondisi paling produktif. Suhu jelas memengaruhi pengisian gabah.",
      f_panas),
    Q("Lahan gambut sering dibuka untuk pertanian, tetapi banyak menghadapi kegagalan. Kendala utama pertanian di lahan gambut adalah …",
      ["Sangat masam, miskin hara, mudah ambles, dan rawan terbakar", "Tanah terlalu keras sehingga akar tanaman tidak dapat menembusnya",
       "Kandungan kapur sangat tinggi sehingga pH tanah lebih dari 9", "Lahan gambut terletak di pegunungan tinggi dengan suhu sangat dingin",
       "Gambut mengandung pasir kuarsa sehingga tidak dapat menahan air sama sekali"],
      "Gambut adalah tanah organik yang terbentuk dari timbunan sisa tumbuhan di rawa. Kendala pertaniannya: (1) sangat masam (pH 3–4) dan miskin hara terutama unsur mikro (Cu, Zn); (2) daya tumpu rendah sehingga tanaman mudah roboh; (3) ketika dikeringkan, gambut mengalami subsiden (ambles) karena pemadatan dan oksidasi; (4) gambut kering bersifat irreversible (tidak dapat menyerap air kembali) dan mudah terbakar; serta (5) gambut tebal di atas lapisan pirit berisiko menimbulkan masalah sulfat masam. Pengalaman Proyek Lahan Gambut Sejuta Hektare (PLG) di Kalimantan Tengah menunjukkan kegagalan bila karakteristik ini diabaikan.\n\nPengecoh: gambut justru lunak, masam (bukan berkapur), berada di dataran rendah, dan mampu menyimpan air sangat banyak saat basah.",
      None),
    Q("Perhatikan grafik pH tanah empat petak sawah berikut. Garis putus-putus menunjukkan batas pH 5,5.\n\nPetak yang paling memerlukan pengapuran beserta alasannya adalah …",
      ["Petak B, karena pH 4,4 sangat masam dan Al beracun", "Petak C, karena pH 7,1 terlalu masam untuk tanaman padi",
       "Petak A, karena pH 6,4 adalah yang paling masam di antara keempatnya", "Petak D, karena pH 5,9 berada di bawah batas 5,5",
       "Semua petak karena pH tanah di Indonesia selalu terlalu basa"],
      "pH tanah memengaruhi ketersediaan hara. Pada pH sangat masam (< 5,5), unsur fosfor terikat oleh aluminium dan besi sehingga sulit diserap tanaman, sedangkan aluminium terlarut dapat meracuni akar. Pengapuran (pemberian kapur pertanian atau dolomit) menaikkan pH dan memperbaiki ketersediaan hara.\nPetak B dengan pH 4,4 adalah satu-satunya petak yang jauh di bawah batas 5,5, sehingga paling memerlukan pengapuran.\n\nPengecoh: pH 7,1 (petak C) mendekati netral, bukan masam. Petak A (6,4) dan D (5,9) berada di atas batas 5,5 dan relatif sesuai untuk banyak tanaman. Tanah di Indonesia yang beriklim tropis basah justru cenderung masam akibat pencucian basa oleh hujan.",
      f_ph_tanah),
    Q("Kebutuhan air bersih tanaman di suatu daerah irigasi adalah 8.000 m³ per hari, sedangkan efisiensi irigasi jaringan tersebut 64%. Volume air yang harus diambil dari sumber (pengambilan kotor) per hari adalah …",
      ["12.500 m³", "5.120 m³", "8.640 m³", "13.120 m³", "2.880 m³"],
      "Pengambilan air kotor = kebutuhan bersih ÷ efisiensi = 8.000 ÷ 0,64 = 12.500 m³ per hari.\nArtinya 4.500 m³ air hilang di saluran (rembesan, penguapan, kebocoran, dan operasi pintu air) sebelum mencapai tanaman. Memperbaiki saluran (misalnya lining saluran tersier) dan pengelolaan oleh perkumpulan petani pemakai air dapat menaikkan efisiensi sehingga kebutuhan pengambilan berkurang.\n\nPengecoh: 5.120 m³ adalah hasil 8.000 × 0,64 (dikalikan, bukan dibagi). 8.640 m³ dan 13.120 m³ tidak sesuai perhitungan. 2.880 m³ adalah 8.000 × 0,36, yaitu bagian yang hilang bila salah konsep.",
      None),
]

P3 = [
    Q("Perhatikan tiga teknik konservasi tanah pada lahan miring berikut.\n\nTeknik yang paling efektif untuk lahan pertanian tanaman semusim dengan kemiringan sekitar 25% adalah …",
      ["Teknik 1, teras bangku yang membuat bidang datar", "Teknik 2, penanaman searah lereng tanpa teras",
       "Teknik 3, strip rumput yang hanya cocok untuk lahan datar", "Teknik 2, karena tanaman tumbuh rapat sehingga erosi nol",
       "Semua teknik sama efektifnya tanpa memperhatikan kemiringan"],
      "• Teknik 1: teras bangku, yaitu lereng diubah menjadi bidang-bidang datar bertingkat dengan tampingan. Panjang dan kemiringan lereng efektif berkurang sehingga aliran permukaan melambat dan erosi berkurang drastis. Cocok untuk tanaman semusim pada lereng 10–30% dengan solum tanah cukup dalam, misalnya di dataran tinggi Dieng.\n• Teknik 2: tanaman ditanam di lereng tanpa teras; bila barisannya searah lereng, erosi justru meningkat.\n• Teknik 3: strip tanaman (rumput atau tanaman penguat) searah kontur yang menahan aliran permukaan; efektif pada lereng landai–sedang dan dapat dikombinasikan dengan teras.\n\nPengecoh: penanaman searah lereng memperbesar erosi. Strip rumput tidak hanya untuk lahan datar. Tidak ada teknik yang menghasilkan erosi nol. Efektivitas teknik konservasi bergantung kemiringan.",
      f_konservasi),
    Q("Pertanian organik dinilai lebih berkelanjutan dibandingkan pertanian konvensional intensif. Alasan yang paling tepat adalah …",
      ["Memperbaiki bahan organik dan kehidupan tanah serta mengurangi residu kimia", "Selalu menghasilkan produksi per hektare dua kali lipat pertanian konvensional",
       "Tidak memerlukan tenaga kerja sama sekali karena tanaman tumbuh sendiri", "Menggunakan pestisida sintetis lebih banyak agar hama cepat musnah",
       "Hanya dapat dilakukan di negara beriklim subtropis"],
      "Pertanian organik menghindari pupuk kimia sintetis dan pestisida sintetis, serta mengandalkan pupuk organik, kompos, rotasi tanaman, tanaman penutup tanah, dan pengendalian hama hayati. Manfaatnya: kandungan bahan organik dan kehidupan mikroba tanah meningkat sehingga struktur dan kesuburan tanah membaik, residu kimia pada produk dan lingkungan berkurang, serta keanekaragaman hayati lebih terjaga.\nKelemahannya, produktivitas pada tahun-tahun awal konversi sering lebih rendah dan tenaga kerja yang diperlukan lebih banyak.\n\nPengecoh: produksi organik tidak selalu lebih tinggi. Tenaga kerja tetap diperlukan, bahkan lebih banyak. Pertanian organik tidak memakai pestisida sintetis. Pertanian organik dapat diterapkan di daerah tropis, termasuk Indonesia.",
      None),
    Q("Perhatikan hasil petak percobaan erosi pada lereng 25% berikut.\n\nPersentase penurunan erosi bila lahan tanpa konservasi diubah menjadi teras bangku adalah …",
      ["85%", "15%", "102%", "42%", "90%"],
      "Penurunan erosi = (erosi awal − erosi akhir) ÷ erosi awal × 100%\n= (120 − 18) ÷ 120 × 100% = 102 ÷ 120 × 100% = 85%.\nTeras bangku mengubah lereng menjadi bidang datar sehingga aliran permukaan melambat dan lebih banyak air meresap. Kombinasi agroforestri dan teras menurunkan erosi lebih besar lagi, yaitu (120 − 12) ÷ 120 = 90%.\n\nPengecoh: 15% adalah erosi tersisa (18 ÷ 120). 102% muncul bila selisih 102 ton dibaca sebagai persen. 42% adalah penurunan oleh guludan searah kontur ((120 − 70) ÷ 120 ≈ 42%). 90% adalah penurunan oleh kombinasi agroforestri dan teras.",
      f_erosi),
    Q("NTT dan NTB merupakan sentra peternakan sapi potong di Indonesia. Faktor geografis yang paling mendukung hal tersebut adalah …",
      ["Padang sabana yang luas sebagai sumber pakan dan iklim yang relatif kering", "Curah hujan sangat tinggi sehingga rumput tumbuh di hutan hujan yang lebat",
       "Lahan sawah beririgasi yang sangat luas sehingga jerami melimpah sepanjang tahun", "Suhu udara yang sangat dingin sehingga sapi tidak mudah terserang penyakit",
       "Kepadatan penduduk sangat tinggi sehingga permintaan daging lokal paling besar"],
      "NTT dan NTB beriklim tropis kering (Aw) dengan musim kemarau panjang. Kondisi ini membentuk padang sabana dan stepa yang luas, sehingga cocok untuk penggembalaan ternak seperti sapi Bali, sapi Ongole, dan kerbau. Iklim kering juga mengurangi beberapa penyakit ternak yang berkembang di daerah lembap. Sapi dari NTT dan NTB banyak dikirim ke Jawa dan daerah lain.\nTantangannya adalah kekurangan pakan dan air pada puncak kemarau, sehingga diperlukan lumbung pakan dan embung.\n\nPengecoh: curah hujan di NTT dan NTB rendah, bukan sangat tinggi. Lahan sawah beririgasi tidak seluas di Jawa. Suhu di dataran rendah NTT dan NTB tidak dingin. Kepadatan penduduk relatif rendah.",
      None),
    Q("Perhatikan grafik produksi perikanan Indonesia berikut.\n\nInterpretasi yang paling tepat adalah …",
      ["Budi daya melampaui perikanan tangkap sejak sekitar 2010-an",
       "Perikanan tangkap tumbuh paling cepat dan selalu lebih besar daripada budi daya",
       "Produksi budi daya menurun tajam sejak 2008 karena kekurangan benih",
       "Kedua jenis perikanan tumbuh dengan laju yang sama sepanjang periode",
       "Perikanan tangkap berhenti total setelah tahun 2016"],
      "Grafik menunjukkan perikanan tangkap tumbuh perlahan (±4 menjadi ±7 juta ton), sedangkan perikanan budi daya melonjak dari ±1 juta ton menjadi ±17 juta ton, dan melampaui perikanan tangkap sekitar tahun 2010–2012. Lonjakan ini sebagian besar didorong rumput laut, udang, nila, dan bandeng. Perikanan tangkap dibatasi oleh daya dukung stok ikan di laut (MSY), sehingga peningkatan produksi lebih banyak diharapkan dari budi daya.\nTantangannya: konversi mangrove untuk tambak, pencemaran perairan, dan ketergantungan pada pakan.\n\nPengecoh: perikanan tangkap tumbuh lebih lambat. Budi daya tidak menurun tajam setelah 2008. Laju kedua jenis jelas berbeda. Perikanan tangkap tetap berlangsung.",
      f_ikan),
    Q("Sistem mina padi, yaitu memelihara ikan di petak sawah bersamaan dengan tanaman padi, memberikan manfaat ganda. Manfaat ekologis yang paling tepat adalah …",
      ["Ikan memakan hama dan gulma serta kotorannya menambah hara sawah", "Ikan memakan seluruh tanaman padi sehingga lahan cepat kosong untuk tanam ulang",
       "Sistem mina padi memerlukan pestisida lebih banyak agar ikan tumbuh besar", "Ikan membuat air sawah kering sehingga padi lebih tahan kekeringan",
       "Mina padi meningkatkan emisi karena ikan menghasilkan karbon dioksida"],
      "Mina padi adalah bentuk pertanian terpadu. Ikan (misalnya nila, mas, atau lele) memakan serangga hama, keong, dan gulma air, sehingga kebutuhan pestisida berkurang. Gerakan ikan menggemburkan lumpur dan kotorannya menjadi pupuk bagi padi. Petani memperoleh dua sumber pendapatan dan protein dari lahan yang sama. Sistem ini sudah lama dipraktikkan di beberapa daerah, misalnya di Sleman dan Jawa Barat.\n\nPengecoh: ikan tidak memakan seluruh tanaman padi. Mina padi justru menuntut pengurangan pestisida karena pestisida meracuni ikan. Mina padi memerlukan air tergenang, bukan kering. Respirasi ikan bukan masalah emisi yang berarti.",
      None),
    Q("Perhatikan grafik rasio konversi pakan beberapa ternak dan ikan berikut.\n\nKesimpulan yang paling tepat untuk ketahanan pangan berbasis protein hewani adalah …",
      ["Ikan nila dan ayam paling efisien mengubah pakan menjadi daging", "Sapi potong paling efisien karena membutuhkan pakan paling banyak",
       "Babi membutuhkan pakan dua kali lipat sapi untuk setiap kilogram daging", "Semua jenis ternak memiliki efisiensi pakan yang sama",
       "Ikan nila membutuhkan pakan paling banyak sehingga paling boros"],
      "Rasio konversi pakan (feed conversion ratio, FCR) adalah jumlah pakan yang diperlukan untuk menghasilkan 1 kg pertambahan bobot. Semakin kecil FCR, semakin efisien. Grafik menunjukkan ikan nila (±1,5) dan ayam pedaging (±1,8) paling efisien, sedangkan sapi potong (±8) paling boros. Ikan efisien karena berdarah dingin (tidak memakai energi untuk menjaga suhu tubuh) dan didukung oleh air sehingga energi untuk menopang tubuh kecil.\nImplikasinya, pengembangan budi daya ikan dan unggas dapat menyediakan protein hewani dengan kebutuhan lahan dan pakan yang lebih kecil.\n\nPengecoh: FCR besar berarti boros, bukan efisien. Babi (±4) membutuhkan pakan setengah dari sapi. Efisiensi jelas berbeda. Ikan nila justru paling efisien.",
      f_fcr),
    Q("Pembukaan hutan mangrove secara besar-besaran untuk tambak udang di pantai utara Jawa pada 1980–1990-an menimbulkan dampak jangka panjang. Dampak yang paling tepat adalah …",
      ["Abrasi meningkat dan perikanan pesisir menurun", "Garis pantai maju ke laut karena sedimen bertambah",
       "Produksi udang terus meningkat tanpa batas sehingga harga udang turun", "Intrusi air laut berkurang karena tambak menahan air asin",
       "Keanekaragaman hayati pesisir meningkat karena tambak menyediakan habitat baru"],
      "Mangrove melindungi pantai dari gelombang, menahan sedimen, menjadi tempat pemijahan dan asuhan ikan serta udang liar, dan menyaring limbah. Konversi mangrove menjadi tambak menyebabkan: (1) abrasi dan mundurnya garis pantai (misalnya di Demak dan Brebes); (2) penurunan hasil perikanan tangkap pesisir karena habitat pemijahan hilang; (3) kualitas air tambak memburuk sehingga udang mudah terserang penyakit, lalu banyak tambak ditinggalkan (terbengkalai); serta (4) intrusi air laut ke daratan meningkat.\nKarena itu kini dikembangkan silvofishery (tambak dengan mangrove) dan rehabilitasi mangrove.\n\nPengecoh: garis pantai justru mundur. Produksi tambak tidak meningkat tanpa batas. Intrusi meningkat. Keanekaragaman hayati menurun.",
      None),
    Q("Perhatikan grafik salinitas air irigasi dan produktivitas padi di pesisir Kabupaten D berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Semakin dekat ke pantai, salinitas naik dan produktivitas padi turun tajam", "Semakin dekat ke pantai, salinitas turun dan produktivitas padi naik",
       "Salinitas tidak berpengaruh karena padi sangat toleran garam", "Produktivitas tertinggi berada pada jarak 0,5 km dari pantai",
       "Salinitas dan produktivitas sama-sama meningkat menjauhi pantai"],
      "Grafik menunjukkan salinitas air irigasi tinggi di dekat pantai (±12‰ pada 0,5 km) dan turun menjauhi pantai (±0,8‰ pada 8 km). Sebaliknya produktivitas padi rendah di dekat pantai (±1,2 ton/ha) dan naik hingga ±6 ton/ha menjauhi pantai. Padi tergolong tanaman yang cukup peka terhadap garam: salinitas tinggi menyebabkan stres osmotik dan keracunan ion sehingga pertumbuhan dan hasil turun. Intrusi air laut ke sawah pesisir dapat diperparah kenaikan muka laut, amblesan tanah, dan berkurangnya debit sungai saat kemarau.\nAdaptasinya antara lain varietas toleran salin (misalnya Inpari Unsoed 79 Agritan), pintu air pengendali, dan alih komoditas.\n\nPengecoh: arah hubungan dibalik. Salinitas jelas berpengaruh. Produktivitas terendah ada di dekat pantai. Salinitas menurun menjauhi pantai.",
      f_salin),
    Q("Sistem pertanian terpadu (integrated farming) yang memadukan tanaman, ternak, dan ikan dinilai lebih efisien. Prinsip utama sistem ini adalah …",
      ["Limbah satu komponen menjadi masukan komponen lain", "Setiap komponen dikelola terpisah agar tidak saling memengaruhi",
       "Hanya satu jenis tanaman ditanam dalam skala besar untuk ekspor", "Ternak dan ikan dipelihara tanpa pakan karena memakan tanaman pangan utama",
       "Penggunaan pupuk kimia dan pestisida dimaksimalkan untuk semua komponen"],
      "Pertanian terpadu menerapkan prinsip daur ulang (siklus tertutup). Contohnya: jerami dan sisa tanaman menjadi pakan ternak; kotoran ternak diolah menjadi kompos atau biogas; kompos menyuburkan tanaman; air kolam ikan yang kaya hara dipakai untuk menyiram tanaman; dan sisa sayuran menjadi pakan ikan. Dengan demikian biaya masukan luar (pupuk, pakan, energi) berkurang, limbah hampir nol, risiko gagal panen tersebar, dan pendapatan petani lebih beragam.\n\nPengecoh: komponen tidak dikelola terpisah. Monokultur ekspor adalah perkebunan. Ternak dan ikan tetap memerlukan pakan, tetapi sebagian berasal dari limbah. Pertanian terpadu justru mengurangi pupuk kimia dan pestisida.",
      None),
]

P4 = [
    Q("Perhatikan grafik porsi pengeluaran untuk pangan menurut kelompok pendapatan berikut.\n\nImplikasi yang paling tepat ketika harga pangan naik 20% adalah …",
      ["Rumah tangga termiskin paling terpukul karena porsi pangannya besar", "Rumah tangga terkaya paling terpukul karena porsi pangannya paling kecil",
       "Semua kelompok terpukul sama besar karena kenaikan harganya sama", "Rumah tangga termiskin diuntungkan karena porsi pangannya tinggi",
       "Kenaikan harga pangan tidak berpengaruh terhadap kesejahteraan rumah tangga"],
      "Grafik menunjukkan rumah tangga termiskin (kuintil 1) membelanjakan ±65% pengeluarannya untuk pangan, sedangkan kelompok terkaya (kuintil 5) hanya ±35%. Pola ini sesuai Hukum Engel: semakin tinggi pendapatan, semakin kecil porsi pengeluaran untuk pangan.\nKetika harga pangan naik 20%, pengeluaran total rumah tangga termiskin bertambah sekitar 0,65 × 20% = 13%, sedangkan kelompok terkaya hanya sekitar 0,35 × 20% = 7%. Akibatnya rumah tangga miskin paling rentan terhadap gejolak harga, sehingga diperlukan bantuan pangan dan stabilisasi harga.\n\nPengecoh: kelompok kaya justru paling sedikit terdampak. Dampaknya tidak sama karena porsi pengeluaran berbeda. Rumah tangga miskin dirugikan, bukan diuntungkan.",
      f_engel),
    Q("Sebuah kecamatan memiliki luas panen tanaman pangan 6.000 ha, penduduk 40.000 jiwa, dan kebutuhan fisik minimum (KFM) 0,1 ha per orang. Dengan σ = (Lp ÷ Pd) ÷ KFM, kondisi daya dukung lahan pertaniannya adalah …",
      ["σ = 1,5; surplus, mampu swasembada pangan", "σ = 0,67; defisit, belum mampu swasembada", "σ = 0,15; defisit berat",
       "σ = 15; surplus sangat besar", "σ = 1,0; tepat seimbang"],
      "σ = (Lp ÷ Pd) ÷ KFM = (6.000 ÷ 40.000) ÷ 0,1 = 0,15 ÷ 0,1 = 1,5.\nNilai σ > 1 berarti lahan pertanian mampu memenuhi kebutuhan pangan penduduk (surplus) sehingga wilayah tersebut mampu swasembada; σ = 1 berarti seimbang; σ < 1 berarti defisit.\n\nPengecoh: 0,67 muncul bila rumus dibalik. 0,15 adalah luas lahan per orang (Lp ÷ Pd) sebelum dibagi KFM. 15 muncul bila mengalikan dengan KFM sebagai pembilang atau salah desimal. 1,0 tidak sesuai perhitungan.",
      None),
    Q("Perhatikan data daya dukung lahan pertanian tiga wilayah berikut. Daya dukung σ = (Lp ÷ Pd) ÷ KFM.\n\nPasangan wilayah dan kondisinya yang tepat adalah …",
      ["A defisit (σ = 0,75); B surplus (σ = 2,0)", "A surplus (σ = 1,33); C defisit (σ = 0,8)", "B defisit (σ = 0,5); C surplus (σ = 1,25)",
       "A seimbang (σ = 1,0); B defisit (σ = 0,5)", "C surplus (σ = 2,0); A seimbang (σ = 1,0)"],
      "Hitung σ tiap wilayah:\n• A: (3.000 ÷ 50.000) ÷ 0,08 = 0,06 ÷ 0,08 = 0,75 → defisit.\n• B: (8.000 ÷ 40.000) ÷ 0,10 = 0,20 ÷ 0,10 = 2,0 → surplus.\n• C: (5.000 ÷ 62.500) ÷ 0,08 = 0,08 ÷ 0,08 = 1,0 → seimbang.\nPasangan yang tepat adalah A defisit dan B surplus.\n\nPengecoh: 1,33, 0,5, 1,25, dan 0,8 berasal dari pembagian yang dibalik. Wilayah defisit seperti A memerlukan peningkatan produktivitas, perluasan lahan, atau pasokan pangan dari wilayah surplus seperti B.",
      f_dayadukung),
    Q("Program penurunan stunting nasional tidak hanya membagikan beras, tetapi juga telur, ikan, dan edukasi gizi serta sanitasi. Pendekatan ini dipilih karena masalah stunting terutama berkaitan dengan …",
      ["Kekurangan gizi kronis (protein, zat gizi mikro) dan infeksi berulang", "Kekurangan kalori semata sehingga cukup diatasi dengan menambah beras",
       "Kelebihan konsumsi protein hewani pada anak balita", "Kurangnya produksi beras nasional yang menyebabkan kelaparan massal",
       "Faktor keturunan tinggi badan orang tua yang tidak dapat diubah"],
      "Stunting adalah kondisi gagal tumbuh pada anak akibat kekurangan gizi kronis, terutama dalam 1.000 hari pertama kehidupan, yang ditandai tinggi badan di bawah standar usianya. Penyebab langsungnya adalah asupan gizi yang tidak memadai, terutama protein hewani dan zat gizi mikro seperti zat besi, zinc, dan vitamin A, serta infeksi berulang (misalnya diare) akibat sanitasi dan air bersih yang buruk. Beras memenuhi kebutuhan energi tetapi tidak mencukupi protein dan mikronutrien. Masalah ini sering disebut kelaparan tersembunyi (hidden hunger).\n\nPengecoh: menambah beras saja tidak cukup. Kelebihan protein bukan masalahnya. Indonesia tidak mengalami kelaparan massal akibat kekurangan beras. Faktor keturunan berperan kecil dibandingkan gizi dan lingkungan.",
      None),
    Q("Perhatikan neraca beras Provinsi R dalam satu tahun berikut. Ketersediaan per kapita = (produksi + impor − ekspor − susut − nonpangan) ÷ penduduk.\n\nKetersediaan beras untuk konsumsi per kapita adalah sekitar …",
      ["111,5 kg/kapita/tahun", "135,0 kg/kapita/tahun", "125,0 kg/kapita/tahun", "121,5 kg/kapita/tahun", "100,0 kg/kapita/tahun"],
      "1) Pasokan = produksi + impor − ekspor = 2.500.000 + 300.000 − 100.000 = 2.700.000 ton.\n2) Susut 10% dari pasokan = 270.000 ton.\n3) Tersedia untuk konsumsi = 2.700.000 − 270.000 − 200.000 = 2.230.000 ton = 2.230.000.000 kg.\n4) Per kapita = 2.230.000.000 ÷ 20.000.000 = 111,5 kg/kapita/tahun.\n\nPengecoh: 135,0 kg membagi pasokan tanpa mengurangi susut dan nonpangan. 125,0 kg hanya memakai produksi (2,5 juta ÷ 20 juta). 121,5 kg mengurangi susut tetapi lupa penggunaan nonpangan. 100,0 kg tidak sesuai perhitungan. Angka ±111 kg sesuai dengan kisaran konsumsi beras per kapita Indonesia.",
      f_neraca),
    Q("Krisis harga pangan dunia tahun 2007–2008 dipicu oleh beberapa faktor sekaligus. Kombinasi faktor yang paling tepat adalah …",
      ["Harga minyak tinggi, biofuel, larangan ekspor, dan spekulasi", "Produksi pangan dunia berlebih sehingga harga pangan justru naik",
       "Penurunan jumlah penduduk dunia yang mengurangi kebutuhan pangan", "Seluruh negara berhenti mengimpor beras dan gandum secara bersamaan",
       "Penemuan varietas unggul baru yang menurunkan biaya produksi"],
      "Krisis harga pangan 2007–2008 terjadi akibat kombinasi: (1) harga minyak bumi yang sangat tinggi menaikkan biaya pupuk, pengolahan, dan transportasi; (2) peningkatan permintaan jagung dan minyak nabati untuk biofuel; (3) cadangan pangan dunia yang rendah; (4) larangan atau pembatasan ekspor oleh beberapa negara produsen (misalnya beras dari India dan Vietnam) yang memicu kepanikan pasar; (5) spekulasi di pasar komoditas; serta (6) gagal panen di beberapa negara akibat kekeringan.\n\nPengecoh: produksi berlebih akan menurunkan harga. Jumlah penduduk dunia terus bertambah. Negara pengimpor tidak berhenti mengimpor. Varietas unggul justru menurunkan, bukan menaikkan, harga.",
      None),
    Q("Perhatikan grafik indeks harga pangan dunia berikut.\n\nLonjakan R pada tahun 2022 paling berkaitan dengan …",
      ["Perang Rusia–Ukraina yang mengganggu pasokan gandum dan pupuk", "Revolusi Hijau yang menaikkan produksi beras di Asia",
       "Krisis keuangan Asia yang menurunkan permintaan pangan global", "Penghentian total produksi jagung di Amerika Serikat",
       "Penurunan harga minyak bumi yang membuat biaya produksi naik"],
      "Grafik menunjukkan tiga puncak: P (2008) dan Q (2011) terkait krisis harga pangan akibat harga energi tinggi, biofuel, dan gagal panen; sedangkan R (2022) adalah puncak tertinggi. Pada 2022, invasi Rusia ke Ukraina mengganggu ekspor gandum, jagung, dan minyak bunga matahari dari kedua negara (keduanya eksportir utama), serta menaikkan harga energi dan pupuk karena Rusia adalah eksportir besar gas dan pupuk. Pemulihan permintaan pascapandemi COVID-19 juga ikut mendorong kenaikan harga.\n\nPengecoh: Revolusi Hijau terjadi pada 1960–1980-an dan justru menurunkan harga. Krisis keuangan Asia terjadi pada 1997–1998. Produksi jagung AS tidak berhenti. Harga minyak justru naik pada 2022.",
      f_fao),
    Q("Konsep \"kelaparan tersembunyi\" (hidden hunger) dalam kajian gizi merujuk pada kondisi …",
      ["Kekurangan zat gizi mikro walaupun kebutuhan kalori sudah terpenuhi", "Kelaparan yang terjadi hanya pada malam hari ketika orang tidur",
       "Kelaparan akibat bencana alam yang tidak dilaporkan media", "Kelebihan kalori yang menyebabkan obesitas pada orang dewasa",
       "Kekurangan air minum bersih di daerah perkotaan padat"],
      "Kelaparan tersembunyi adalah kekurangan zat gizi mikro, seperti zat besi, yodium, zinc, vitamin A, dan asam folat, walaupun asupan energi (kalori) sudah cukup. Gejalanya tidak selalu terlihat, tetapi berdampak pada anemia, gangguan pertumbuhan, penurunan kecerdasan, dan daya tahan tubuh yang lemah. Penyebabnya pola makan yang monoton, misalnya didominasi nasi tanpa cukup sayur, buah, dan protein hewani. Solusinya antara lain diversifikasi pangan, fortifikasi (misalnya garam beryodium dan tepung terigu yang difortifikasi), dan biofortifikasi tanaman.\n\nPengecoh: kelaparan tersembunyi tidak terkait waktu malam atau pemberitaan media. Kelebihan kalori adalah masalah gizi lebih. Kekurangan air bersih adalah masalah sanitasi.",
      None),
    Q("Perhatikan grafik produksi dan konsumsi beras Negara N berikut.\n\nSejak sekitar tahun berapa negara tersebut mulai bergantung pada impor beras untuk memenuhi konsumsinya?",
      ["Sekitar 2018", "Sekitar 2012", "Sekitar 2015", "Sekitar 2022", "Tidak pernah, karena produksi selalu di atas konsumsi"],
      "Pada 2012, produksi (±31 juta ton) masih di atas konsumsi (±28,5 juta ton). Produksi tumbuh sangat lambat lalu menurun, sedangkan konsumsi naik ±0,45 juta ton per tahun seiring pertumbuhan penduduk. Kedua garis berpotongan sekitar tahun 2017–2018; setelah itu konsumsi melebihi produksi sehingga negara tersebut memerlukan impor atau pengurangan cadangan untuk menutup kekurangan.\nPenyebab umum kondisi seperti ini: alih fungsi sawah, stagnasi produktivitas, perubahan iklim, dan pertumbuhan penduduk.\n\nPengecoh: 2012 dan 2015 masih surplus. 2022 sudah jauh setelah garis berpotongan. Grafik jelas menunjukkan konsumsi melampaui produksi pada tahun-tahun akhir.",
      f_swasembada),
    Q("Di Papua dan Maluku, sagu adalah pangan pokok tradisional. Program diversifikasi pangan berbasis sumber daya lokal dinilai penting karena …",
      ["Mengurangi ketergantungan beras dan memakai pangan sesuai ekosistem", "Sagu dapat tumbuh di mana saja termasuk di gurun yang kering",
       "Beras harus dihapus sepenuhnya dari pola konsumsi seluruh penduduk Indonesia", "Sagu memiliki kandungan protein lebih tinggi daripada daging sapi",
       "Pangan lokal selalu lebih mahal sehingga meningkatkan pendapatan negara"],
      "Diversifikasi pangan adalah upaya menganekaragamkan sumber pangan pokok dan konsumsi gizi agar tidak bergantung pada satu komoditas (beras). Pangan lokal seperti sagu (Papua, Maluku), jagung (NTT, Madura), umbi-umbian, dan sorgum telah beradaptasi dengan kondisi iklim dan tanah setempat, sehingga lebih tahan terhadap guncangan iklim dan tidak memerlukan pencetakan sawah baru yang mahal. Hutan sagu juga dapat tumbuh di lahan rawa yang tidak cocok untuk padi. Pergeseran konsumsi dari sagu ke beras di Papua justru meningkatkan ketergantungan pasokan dari luar.\n\nPengecoh: sagu memerlukan lahan basah, bukan gurun. Diversifikasi tidak berarti menghapus beras. Sagu terutama sumber karbohidrat dengan protein rendah. Pangan lokal tidak selalu lebih mahal.",
      None),
]

P5 = [
    Q("Perhatikan grafik luas baku sawah Indonesia berikut.\n\nLaju rata-rata penyusutan luas baku sawah per tahun pada periode 2013–2019 adalah sekitar …",
      ["112 ribu ha per tahun", "670 ribu ha per tahun", "224 ribu ha per tahun", "8,2% per tahun", "11 ribu ha per tahun"],
      "Penyusutan = 8,13 − 7,46 = 0,67 juta ha selama 6 tahun (2013–2019).\nLaju rata-rata = 0,67 juta ÷ 6 ≈ 0,112 juta ha = ±112 ribu ha per tahun.\nSecara persentase, total penyusutan 0,67 ÷ 8,13 ≈ 8,2% dalam 6 tahun, atau sekitar 1,4% per tahun.\nAlih fungsi sawah menjadi permukiman, industri, dan infrastruktur adalah ancaman besar bagi produksi padi nasional, terutama di Jawa.\n\nPengecoh: 670 ribu ha adalah total penyusutan, bukan per tahun. 224 ribu ha membagi dengan 3 (jumlah selang titik data). 8,2% adalah persentase total 6 tahun, bukan per tahun. 11 ribu ha adalah kesalahan desimal.",
      f_sawah),
    Q("Beras yang tercecer saat panen dan rusak di gudang disebut susut pangan (food loss), sedangkan nasi yang dibuang dari piring disebut sisa pangan (food waste). Perbedaan utama keduanya adalah …",
      ["Loss terjadi di produksi–distribusi, waste di ritel dan konsumen", "Food loss hanya terjadi di negara maju, food waste hanya di negara berkembang",
       "Food loss adalah pangan busuk, food waste adalah pangan yang masih segar", "Keduanya sama persis dan hanya berbeda istilah dalam bahasa Inggris",
       "Food waste terjadi di sawah, food loss terjadi di meja makan"],
      "Susut pangan (food loss) adalah berkurangnya jumlah atau mutu pangan pada tahap panen, pascapanen, penyimpanan, pengolahan, dan distribusi, misalnya gabah tercecer saat perontokan atau sayur rusak saat pengangkutan. Sisa pangan (food waste) adalah pangan layak konsumsi yang dibuang pada tahap ritel, layanan makanan, dan rumah tangga, misalnya makanan sisa di piring atau produk kedaluwarsa di toko.\nIndonesia termasuk penghasil sisa pangan terbesar per kapita di dunia, sehingga pengurangan susut dan sisa pangan menjadi strategi ketahanan pangan sekaligus mitigasi emisi metana di TPA.\n\nPengecoh: keduanya terjadi di negara maju maupun berkembang. Perbedaannya bukan kondisi segar atau busuk. Keduanya bukan istilah yang sama. Opsi terakhir membalik tahapannya.",
      None),
    Q("Perhatikan grafik kehilangan dan pemborosan pangan sepanjang rantai pasok berikut.\n\nPernyataan yang paling tepat adalah …",
      ["Pemborosan terbesar terjadi di tingkat konsumen rumah tangga", "Kehilangan terbesar terjadi saat panen sehingga mesin panen paling mendesak",
       "Total kehilangan sepanjang rantai pasok kurang dari 10%", "Tahap ritel menyumbang kehilangan terbesar karena toko membuang pangan",
       "Kehilangan pascapanen lebih besar daripada di tingkat konsumen"],
      "Grafik menunjukkan pemborosan terbesar terjadi di tingkat konsumen atau rumah tangga (11%), lebih besar daripada tahap panen (3%), pascapanen dan penyimpanan (5%), pengolahan dan distribusi (4%), serta ritel (2%). Total kehilangan dan pemborosan mencapai 3 + 5 + 4 + 2 + 11 = 25% dari produksi. Karena itu, selain memperbaiki teknologi pascapanen, kampanye mengurangi sisa makanan di rumah tangga, restoran, dan acara (misalnya mengambil makanan secukupnya dan merencanakan belanja) sangat penting.\n\nPengecoh: kehilangan saat panen hanya 3%. Total kehilangan 25%, jauh di atas 10%. Ritel hanya 2%. Pascapanen (5%) lebih kecil daripada konsumen (11%).",
      f_loss),
    Q("Proyek Pengembangan Lahan Gambut (PLG) Sejuta Hektare di Kalimantan Tengah pada 1990-an gagal menjadi lumbung padi. Pelajaran utama dari kegagalan tersebut adalah …",
      ["Pengembangan pangan harus sesuai karakteristik lahan; gambut tebal tidak cocok untuk sawah", "Lahan gambut sangat cocok untuk padi sawah asalkan dikeringkan secara total",
       "Kegagalan semata-mata disebabkan kekurangan tenaga kerja transmigran", "Proyek berhasil meningkatkan produksi padi tetapi harga beras terlalu rendah",
       "Kanal-kanal drainase yang dibangun berhasil mencegah kebakaran gambut"],
      "Proyek PLG membuka lahan gambut tebal dan membangun ribuan kilometer kanal untuk mengeringkan lahan. Hasilnya: gambut mengering, ambles, dan menjadi sangat mudah terbakar; tanah sangat masam dan miskin hara; muncul masalah sulfat masam; serta padi gagal tumbuh. Proyek ini justru menjadi sumber kebakaran besar dan kabut asap (misalnya tahun 1997 dan 2015). Pelajarannya, pengembangan pangan (termasuk program food estate) harus didasarkan pada evaluasi kesesuaian lahan, kajian hidrologi, dan partisipasi masyarakat lokal.\n\nPengecoh: pengeringan gambut justru merusak. Kegagalan bukan karena kekurangan tenaga kerja. Produksi padi tidak berhasil. Kanal drainase justru memperparah kebakaran.",
      None),
    Q("Perhatikan diagram sumbangan emisi gas rumah kaca dari sistem pangan global berikut.\n\nUpaya mitigasi yang paling menyasar sumber emisi terbesar adalah …",
      ["Mengurangi konsumsi daging merah dan mengolah kotoran ternak", "Mengganti kemasan plastik dengan kemasan kertas di supermarket",
       "Memperbanyak pembangunan cold storage di seluruh pasar tradisional", "Mengangkut pangan dengan pesawat agar lebih cepat sampai ke konsumen",
       "Menambah penggunaan pupuk nitrogen agar produksi tanaman meningkat"],
      "Diagram menunjukkan peternakan dan perikanan menyumbang porsi terbesar (31%), disusul produksi tanaman (27%), perubahan penggunaan lahan (24%), dan rantai pasok (18%). Emisi peternakan berasal dari metana fermentasi pencernaan ruminansia (sapi, kambing), pengelolaan kotoran, dan pakan. Mitigasi yang menyasar sumber terbesar antara lain mengurangi konsumsi daging merah, memperbaiki kualitas pakan, mengolah kotoran menjadi biogas, dan beralih ke protein dengan jejak emisi lebih kecil.\n\nPengecoh: kemasan dan cold storage hanya menyasar bagian rantai pasok yang lebih kecil. Pengangkutan dengan pesawat menambah emisi. Pupuk nitrogen berlebih justru meningkatkan emisi N₂O.",
      f_emisi_pangan),
    Q("Sawah tergenang merupakan salah satu sumber emisi metana. Teknik budi daya padi yang dapat mengurangi emisi metana tanpa menurunkan hasil secara berarti adalah …",
      ["Pengairan berselang (alternate wetting and drying)", "Menggenangi sawah terus-menerus sedalam mungkin", "Membakar jerami di petakan setelah panen",
       "Menambah pupuk urea berlebihan di awal musim tanam", "Menanam padi di lahan gambut yang baru dikeringkan"],
      "Metana di sawah dihasilkan oleh mikroba anaerob yang menguraikan bahan organik di tanah tergenang tanpa oksigen. Pengairan berselang (alternate wetting and drying, AWD) mengeringkan sawah secara berkala selama beberapa hari sebelum digenangi kembali. Saat tanah mengering, oksigen masuk sehingga aktivitas mikroba penghasil metana tertekan. Teknik ini dapat menurunkan emisi metana sekitar 30–50% sekaligus menghemat air irigasi, dengan hasil panen yang relatif sama.\n\nPengecoh: genangan terus-menerus justru memaksimalkan emisi metana. Membakar jerami menghasilkan polusi udara dan emisi. Pupuk urea berlebihan menambah emisi N₂O. Pengeringan gambut melepaskan emisi CO₂ dalam jumlah sangat besar.",
      None),
    Q("Perhatikan grafik harga rata-rata beras medium di beberapa provinsi berikut.\n\nPenjelasan yang paling tepat untuk tingginya harga beras di Papua Pegunungan adalah …",
      ["Biaya distribusi tinggi karena wilayah terpencil yang hanya dapat dijangkau angkutan udara", "Produksi beras di Papua Pegunungan paling besar sehingga harganya naik",
       "Penduduk Papua Pegunungan paling banyak sehingga permintaan beras tertinggi di Indonesia", "Harga beras ditetapkan sama di seluruh provinsi oleh pemerintah",
       "Beras di Papua Pegunungan berkualitas premium sehingga harganya lebih mahal"],
      "Grafik menunjukkan harga beras di Papua Pegunungan (±Rp19.500/kg) jauh lebih tinggi daripada di sentra produksi seperti Jawa Timur dan Sulawesi Selatan (±Rp12.300–12.500/kg). Wilayah pegunungan tengah Papua sebagian besar tidak terhubung jalan darat dengan pelabuhan, sehingga beras diangkut dengan pesawat yang biayanya sangat mahal. Produksi beras lokal juga kecil karena kondisi topografi dan pangan pokok tradisional berbasis ubi jalar. Kesenjangan spasial ini menunjukkan pentingnya aksesibilitas dalam ketahanan pangan.\n\nPengecoh: produksi besar justru menurunkan harga. Jumlah penduduk Papua Pegunungan kecil. Harga beras tidak sama di semua provinsi meskipun ada harga eceran tertinggi. Grafik membandingkan beras medium, bukan premium.",
      f_harga),
    Q("Pemerintah menetapkan Harga Pembelian Pemerintah (HPP) gabah dan Harga Eceran Tertinggi (HET) beras, serta menyimpan Cadangan Beras Pemerintah melalui Bulog. Tujuan utama kebijakan ini adalah …",
      ["Melindungi petani saat panen raya dan melindungi konsumen saat harga melonjak", "Menaikkan harga beras setinggi mungkin agar petani kaya",
       "Menghapus peran pasar sehingga beras hanya dijual oleh pemerintah", "Mengurangi produksi beras agar Indonesia bergantung pada impor",
       "Menyimpan beras selamanya tanpa pernah disalurkan ke masyarakat"],
      "HPP adalah harga minimum pembelian gabah oleh pemerintah agar harga di tingkat petani tidak jatuh saat panen raya, ketika pasokan melimpah. HET adalah batas atas harga di tingkat konsumen agar beras tetap terjangkau. Cadangan Beras Pemerintah yang dikelola Bulog dipakai untuk operasi pasar (stabilisasi harga), bantuan pangan, dan penanganan bencana. Kebijakan ini menjaga pilar stabilitas dan akses dalam ketahanan pangan.\n\nPengecoh: tujuan kebijakan bukan menaikkan harga setinggi mungkin. Pasar tetap berperan. Kebijakan ini mendukung produksi, bukan mengurangi. Cadangan justru disalurkan saat diperlukan.",
      None),
    Q("Perhatikan peta NDVI hasil drone di sebidang sawah berikut. Varietas dan pemupukan di seluruh petak seragam.\n\nInterpretasi dan tindakan pertanian presisi yang paling tepat adalah …",
      ["Sel B2–C3 dan D5–E4 tanamannya tertekan dan ditangani secara lokal",
       "Seluruh sawah perlu dipupuk ulang dengan dosis dua kali lipat karena NDVI rata-rata rendah",
       "Sel dengan NDVI tertinggi adalah lokasi serangan hama sehingga perlu disemprot",
       "NDVI tidak dapat dipakai untuk menilai kondisi tanaman padi",
       "Sel B2–C3 adalah badan air karena NDVI-nya di bawah nol"],
      "Sebagian besar sel memiliki NDVI ±0,77–0,81, menandakan tanaman sehat dan rapat. Dua kelompok sel menyimpang: B2, B3, C2, C3 (±0,46–0,52) dan D5, E4, E5 (±0,28–0,30). Karena varietas dan pemupukan seragam, penurunan NDVI menunjukkan tanaman tertekan, misalnya akibat serangan hama, kekurangan air, genangan, atau masalah tanah setempat. Prinsip pertanian presisi adalah memeriksa lokasi tersebut di lapangan, lalu memberikan perlakuan (pupuk, air, atau pestisida) hanya pada sel yang membutuhkan, sehingga input lebih hemat dan efektif.\n\nPengecoh: NDVI rata-rata tinggi sehingga tidak perlu pemupukan ulang seluruh lahan. NDVI tinggi menandakan tanaman sehat, bukan hama. NDVI justru indikator umum kesehatan tanaman. Nilai sel B2–C3 tetap positif, bukan badan air.",
      f_ndvi_grid),
    Q("Pertanian perkotaan seperti hidroponik di atap gedung, vertikultur, dan kebun komunitas semakin berkembang di kota besar. Manfaat utamanya adalah …",
      ["Mendekatkan sumber pangan segar ke konsumen dan menambah ruang hijau kota", "Menggantikan seluruh produksi beras nasional dari sawah di perdesaan",
       "Meningkatkan kebutuhan transportasi pangan dari desa ke kota", "Mengurangi ruang terbuka hijau karena lahan kota habis untuk pertanian",
       "Hanya dapat dilakukan di lahan yang sangat luas di pinggiran kota"],
      "Pertanian perkotaan memanfaatkan lahan sempit, atap, dinding, dan pekarangan untuk menanam sayuran, buah, dan memelihara ikan. Manfaatnya: menyediakan pangan segar di dekat konsumen sehingga jarak angkut dan susut pangan berkurang; menambah ruang hijau yang membantu menurunkan suhu kota; memanfaatkan sampah organik menjadi kompos; menjadi sarana edukasi; serta menambah pendapatan dan ketahanan pangan rumah tangga.\nNamun, skala pertanian perkotaan terbatas sehingga melengkapi, bukan menggantikan, produksi pangan pokok dari perdesaan.\n\nPengecoh: pertanian perkotaan tidak dapat menggantikan produksi beras nasional. Transportasi justru berkurang. Ruang hijau bertambah. Teknik vertikultur dan hidroponik justru cocok untuk lahan sempit.",
      None),
]

PAKETS = [P0, P1, P2, P3, P4, P5]
