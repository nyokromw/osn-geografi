import sys, json, os
from PIL import Image
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SVG = open(f"{V}/b01v00/assets/logo.svg").read().replace("\n", " ")
CFG = {
 "b01v03": dict(no=2, osn=["ATMOSFER", "BUMI"], hl="5 lapisan + tekanan udara", badge="11 ISTILAH ASING OSN", osnsub="troposphere · lapse rate · ionosphere · aurora",
   formal="Atmosfer Bumi: Komposisi, Lapisan, dan Tekanan Udara", desc="Komposisi udara dan aerosol, profil suhu troposfer sampai termosfer, lapisan ozon, ionosfer, aurora, serta penurunan tekanan terhadap ketinggian.",
   q=["KENAPA SESAK NAPAS", "DI PUNCAK GUNUNG?"], tag="padahal udaranya bersih",
   a=("t176.000.png", (110, 290, 1000, 905)), f=("t176.000.png", (100, 290, 1830, 905)), u=("t24.000.png", (110, 220, 630, 640))),
 "b01v04": dict(no=3, osn=["RADIASI", "MATAHARI"], hl="Wien · Stefan–Boltzmann", badge="10 ISTILAH ASING OSN", osnsub="shortwave · longwave · solar constant · axial tilt",
   formal="Radiasi Matahari dan Insolasi", desc="Hukum Wien, hukum Stefan–Boltzmann, konstanta matahari, empat faktor insolasi, serta mengapa kutub utara menerima energi harian terbesar pada 21 Juni.",
   q=["KUTUB UTARA DAPAT", "MATAHARI TERBANYAK?"], tag="pada 21 Juni, lebih dari ekuator",
   a=("t68.000.png", (100, 290, 1200, 910)), f=("t68.000.png", (100, 290, 1830, 910)), u=("t176.000.png", (110, 290, 1110, 900))),
 "b01v05": dict(no=4, osn=["ALBEDO &", "NERACA ENERGI"], hl="100 masuk = 30 + 20 + 50", badge="8 ISTILAH ASING OSN", osnsub="energy budget · latent heat · urban heat island",
   formal="Albedo dan Neraca Energi Bumi", desc="Albedo berbagai permukaan, aliran energi 100 satuan, panas sensibel dan laten, keseimbangan radiasi, serta pulau bahang kota dan cara mendinginkannya.",
   q=["KENAPA KOTA", "LEBIH PANAS?"], tag="rahasianya ada di albedo",
   a=("t118.000.png", (110, 295, 1810, 885)), f=("t118.000.png", (110, 295, 1810, 885)), u=("t156.000.png", (100, 280, 1120, 900))),
 "b01v06": dict(no=5, osn=["SUHU", "UDARA"], hl="0,6 °C per 100 m", badge="14 ISTILAH ASING OSN", osnsub="lapse rate · temperature inversion · isotherm",
   formal="Suhu Udara: Amplitudo, Ketinggian, dan Inversi", desc="Pengaruh darat dan laut, amplitudo suhu, rumus Braak, zona Junghuhn, inversi suhu, embun upas Dieng, serta isoterm dan ekuator termal.",
   q=["KENAPA PUNCAK", "GUNUNG DINGIN?"], tag="padahal lebih dekat ke matahari",
   a=("t154.000.png", (100, 290, 1830, 900)), f=("t154.000.png", (100, 290, 1830, 900)), u=("t112.000.png", (110, 290, 990, 900))),
 "b01n06": dict(no=6, osn=["TEKANAN", "& ANGIN"], hl="isobar · gradien barometrik", badge="6 ISTILAH ASING OSN", osnsub="pressure gradient · thermal low · Siberian High",
   formal="Tekanan Udara dan Lahirnya Angin", desc="Perbedaan pemanasan, tekanan rendah dan tinggi, isobar, gradien barometrik dalam mb per 111 km, gaya gradien tekanan, serta pola tekanan Januari dan Juli di Asia–Australia.",
   q=["KENAPA ANGIN", "BISA BERTIUP?"], tag="jawabannya ada di peta isobar",
   a=("t158.000.png", (300, 200, 1100, 1000)), f=("t118.000.png", (100, 230, 1820, 930)), u=("t158.000.png", (180, 140, 1220, 1000))),
 "b01n07": dict(no=7, osn=["GAYA", "CORIOLIS"], hl="kanan di BBU, kiri di BBS", badge="8 ISTILAH ASING OSN", osnsub="geostrophic wind · Buys Ballot's law · cyclone",
   formal="Gaya Coriolis, Gesekan, dan Hukum Buys Ballot", desc="Mengapa angin dibelokkan rotasi bumi, angin geostropik, peran gesekan, hukum Buys Ballot, serta siklon dan antisiklon di kedua belahan bumi.",
   q=["KENAPA BADAI", "SELALU BERPUTAR?"], tag="karena bumi berputar",
   a=("t9.000.png", (540, 170, 1380, 1010)), f=("t173.000.png", (60, 380, 1860, 960)), u=("t9.000.png", (360, 90, 1560, 1090))),
 "b01n08": dict(no=8, osn=["ANGIN", "LOKAL"], hl="laut · darat · lembah · fohn", badge="7 ISTILAH ASING OSN", osnsub="sea breeze · katabatic wind · foehn wind",
   formal="Angin Lokal: Angin Laut, Darat, Lembah, Gunung, dan Fohn", desc="Angin laut dan darat, angin lembah dan gunung (anabatik–katabatik), angin fohn beserta nama-nama lokalnya di Indonesia, dan angin bora.",
   q=["KENAPA NELAYAN", "BERANGKAT DINI HARI?"], tag="jawabannya: angin darat",
   a=("t132.000.png", (100, 230, 1820, 930)), f=("t63.000.png", (0, 330, 1920, 940)), u=("t63.000.png", (0, 300, 1920, 940))),
 "b01n09": dict(no=9, osn=["SIRKULASI", "TIGA SEL"], hl="Hadley · Ferrel · kutub", badge="11 ISTILAH ASING OSN", osnsub="Hadley cell · trade winds · westerlies · ITCZ",
   formal="Sirkulasi Tiga Sel dan Angin Pasat", desc="Sel Hadley, Ferrel, dan kutub; ITCZ dan doldrums, antipasat, tekanan tinggi subtropis dan gurun dunia, angin pasat, baratan, timuran kutub, serta front kutub.",
   q=["KENAPA GURUN BERJAJAR", "DI LINTANG 30°?"], tag="jawabannya: sel Hadley",
   a=("t120.000.png", (280, 300, 1100, 990)), f=("t120.000.png", (250, 260, 1880, 960)), u=("t22.000.png", (0, 0, 1920, 940))),
 "b01n10": dict(no=10, osn=["ITCZ &", "MONSUN"], hl="barat · timur · pancaroba", badge="5 ISTILAH ASING OSN", osnsub="ITCZ · west monsoon · east monsoon",
   formal="ITCZ dan Monsun di Indonesia", desc="Pergeseran ITCZ mengikuti matahari, monsun barat yang basah, monsun timur yang kering, pancaroba, serta wilayah yang tidak mengikuti pola monsun seperti Pontianak dan Ambon.",
   q=["KENAPA AMBON HUJAN", "SAAT JAWA KEMARAU?"], tag="jawabannya: monsun timur",
   a=("t48.000.png", (240, 200, 1040, 1000)), f=("t110.000.png", (100, 225, 1270, 935)), u=("t185.000.png", (100, 225, 1270, 935))),
 "b01n11": dict(no=11, osn=["SIRKULASI", "WALKER"], hl="naik Indonesia · turun Peru", badge="6 ISTILAH ASING OSN", osnsub="Walker circulation · warm pool · upwelling",
   formal="Sirkulasi Walker di Ekuator Pasifik", desc="Sirkulasi meridional dan zonal, kolam air hangat Indonesia, upwelling Peru, loop udara naik dan turun di sepanjang ekuator, pemantauan Tahiti–Darwin, dan kaitannya dengan El Niño, La Niña, serta MJO.",
   q=["KENAPA LAUT INDONESIA", "HANGAT, PERU DINGIN?"], tag="jawabannya: sirkulasi Walker",
   a=("t123.000.png", (60, 380, 1230, 960)), f=("t123.000.png", (60, 380, 1230, 960)), u=("t18.000.png", (0, 0, 1920, 940))),
}
ONLY = sys.argv[1:]
for film, c in CFG.items():
    if ONLY and film not in ONLY: continue
    B = f"{V}/{film}"
    for k in "afu":
        fn, box = c[k]; Image.open(f"{V}/out/{film}/stills/{fn}").crop(box).save(f"{B}/thumb_{k}.png")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:UI;src:url(fonts/ui.woff2);font-weight:100 900}}
@font-face{{font-family:D;src:url(fonts/display.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{background:#000}}
.t{{width:1280px;height:720px;position:relative;overflow:hidden;font-family:UI}}
.brand{{position:absolute;display:flex;align-items:center;gap:14px;border-radius:60px;padding:10px 26px 10px 10px;z-index:3}}
.brand svg{{width:70px;height:70px}}.brand span{{font-weight:700;font-size:48px;letter-spacing:-1px}}
.no{{position:absolute;z-index:3;font-weight:800}}
#a{{background:#1d4138}}#a .brand{{left:40px;top:34px;background:#fffefa}}#a .brand span{{color:#1d4138}}
#a .no{{left:46px;top:150px;color:#f2b13a;font-size:30px;letter-spacing:4px}}
#a h1{{position:absolute;left:44px;top:196px;color:#fffefa;font-weight:900;font-size:{80 if max(len(x) for x in c['osn'])>11 else 100 if max(len(x) for x in c['osn'])>8 else 118}px;line-height:.95;letter-spacing:-3px;z-index:2}}#a h1 em{{font-style:normal;color:#f2b13a}}
#a .hl{{position:absolute;left:48px;top:440px;font-weight:800;font-size:40px;color:#fffefa;z-index:2;width:560px}}
#a .badge{{position:absolute;left:46px;top:{530}px;background:#e0794f;color:#fff;font-weight:800;font-size:34px;padding:12px 26px;border-radius:40px;z-index:2}}
#a .sub{{position:absolute;left:50px;top:626px;color:#aac6b5;font-weight:600;font-size:26px;font-style:italic;z-index:2}}
#a .art{{position:absolute;right:-30px;top:80px;width:600px;height:560px;border-radius:28px;overflow:hidden;transform:rotate(3deg);box-shadow:0 20px 60px #0008;border:8px solid #fffefa}}
#a .art img{{width:100%;height:100%;object-fit:cover}}
#b{{background:#f7f1e8}}#b .brand{{right:40px;top:34px;background:#1d4138;padding:8px 22px 8px 8px}}#b .brand svg{{width:56px;height:56px}}#b .brand span{{color:#fffefa;font-size:38px}}
#b .chip{{position:absolute;left:60px;top:58px;color:#983f29;font-weight:700;font-size:26px;letter-spacing:3px}}
#b h1{{position:absolute;left:58px;top:105px;font-family:D;font-weight:400;font-size:84px;line-height:1.02;color:#1d4138;width:1100px}}
#b p{{position:absolute;left:62px;top:345px;font-size:27px;color:#52655d;font-weight:500;width:520px;line-height:1.35}}
#b .art{{position:absolute;right:50px;bottom:40px;width:600px;height:330px;border-radius:22px;overflow:hidden;box-shadow:0 12px 40px #1d413833}}#b .art img{{width:100%;height:100%;object-fit:cover}}
#c{{background:#1d4138}}#c .bg{{position:absolute;inset:0}}#c .bg img{{width:100%;height:100%;object-fit:cover;filter:saturate(1.1)}}
#c .shade{{position:absolute;inset:0;background:linear-gradient(180deg,#0b1f19ee 0%,#0b1f1999 42%,#0b1f1900 70%)}}
#c .brand{{left:36px;bottom:30px;background:#fffefa}}#c .brand span{{color:#1d4138}}
#c h1{{position:absolute;left:0;right:0;top:40px;text-align:center;color:#fff;font-weight:900;font-size:86px;line-height:1.02;letter-spacing:-2px;text-shadow:0 6px 24px #000a;z-index:2}}#c h1 em{{font-style:normal;color:#f2b13a}}
#c .tag{{position:absolute;right:36px;bottom:40px;background:#e0794f;color:#fff;font-weight:800;font-size:36px;padding:12px 26px;border-radius:14px;z-index:2}}
</style></head><body>
<div class="t" id="a"><div class="art"><img src="thumb_a.png"></div><div class="brand">{SVG}<span>OSNGEO.id</span></div><div class="no">OSN GEOGRAFI 2027 · #{c['no']}</div>
<h1>{c['osn'][0]}<br><em>{c['osn'][1]}</em></h1><div class="hl">{c['hl']}</div><div class="badge">{c['badge']}</div><div class="sub">{c['osnsub']}</div></div>
<div class="t" id="b"><div class="chip">GEOGRAFI · IKLIM · SERI KONSEP #{c['no']}</div><div class="brand">{SVG}<span>OSNGEO.id</span></div><h1>{c['formal']}</h1><p>{c['desc']}</p><div class="art"><img src="thumb_f.png"></div></div>
<div class="t" id="c"><div class="bg"><img src="thumb_u.png"></div><div class="shade"></div><h1>{c['q'][0]}<br><em>{c['q'][1]}</em></h1><div class="brand">{SVG}<span>OSNGEO.id</span></div><div class="tag">{c['tag']}</div></div>
</body></html>"""
    open(f"{B}/thumbs.html", "w").write(html)
print("ok")
