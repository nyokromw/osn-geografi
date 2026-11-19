from satfig import show

def s_batur(p): show("batur", p, title="Citra Sentinel-2 warna asli kawasan Kintamani, Bali", labels=[("P", .75, .45), ("Q", .33, .5), ("R", .62, .82), ("S", .5, .1)])
def s_batur_n(p): show("batur", p, kind="ndvi", title="Citra NDVI kawasan Kintamani, Bali", labels=[("P", .75, .45), ("Q", .33, .5), ("R", .62, .82), ("S", .5, .1)])
def s_bromo(p): show("bromo", p, title="Citra Sentinel-2 warna asli kawasan Tengger, Jawa Timur", labels=[("P", .68, .5), ("Q", .41, .555)])
def s_jakarta(p): show("jakarta", p, title="Citra Sentinel-2 warna asli pusat Kota Jakarta", labels=[("P", .38, .72), ("Q", .2, .23)])
def s_krakatau(p): show("krakatau", p, title="Citra Sentinel-2 warna asli Selat Sunda", labels=[("P", .5, .5), ("Q", .12, .78), ("R", .9, .5)])
def s_lapindo(p): show("lapindo", p, title="Citra Sentinel-2 warna asli Kabupaten Sidoarjo", labels=[("P", .5, .5)])
def s_mahakam(p): show("mahakam", p, title="Citra Sentinel-2 warna asli pesisir Kalimantan Timur")
def s_pari(p): show("pari", p, title="Citra Sentinel-2 warna asli Kepulauan Seribu", labels=[("P", .32, .6), ("Q", .2, .4), ("R", .7, .15)])
def s_batang(p): show("batanghari", p, title="Citra Sentinel-2 warna asli Kota Jambi", labels=[("P", .3, .9), ("Q", .7, .5)])
def s_segara(p): show("segara", p, title="Citra Sentinel-2 warna asli pesisir selatan Jawa Tengah", labels=[("P", .42, .45)])
def s_soetta(p): show("soetta", p, title="Citra Sentinel-2 warna asli Kabupaten Tangerang", labels=[("P", .5, .62)])
def s_karawang(p): show("karawang", p, kind="false", title="Citra Sentinel-2 komposit warna semu (NIR-merah-hijau) Karawang")
