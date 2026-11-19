import sys, os, re, json, subprocess, shutil
film, mp3, block, title = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = "/root/.claude/plugins/synced/5c6bea52-a78a-42c6-b441-08b1fdd4d4a0_7324d7bd-5b25-425a-96ab-a100ca9297cc/d92346f7-5140-4ddb-b284-a3b42995e5b0/skills/motion-reel/scripts"
B = f"{V}/{film}"; A = f"{B}/audio"
sh = lambda c: subprocess.run(c, shell=True, check=True, capture_output=True, text=True).stdout
if not os.path.exists(B):
    sh(f"cd {V} && node {S}/scaffold.mjs {film} --title '{title}' --duration 400 --formats 16x9")
os.makedirs(f"{A}/vo", exist_ok=True)
shutil.copy(mp3, f"{A}/vo/raw.mp3")
sh(f"cp {V}/b01v02/fonts/* {B}/fonts/ && cp {V}/b01v02/assets/*.json {B}/assets/ && cp {V}/b01v02/lib/common.js {B}/lib/ && sed -i 's/<html lang=\"en\">/<html lang=\"id\">/' {B}/index.html")
D = float(sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {A}/vo/raw.mp3"))
s = sh(f"ffmpeg -hide_banner -nostats -i {A}/vo/raw.mp3 -af silencedetect=noise=-33dB:d=0.14 -f null - 2>&1 || true")
v = re.findall(r"silence_(start|end): ([0-9.]+)", s); vals = [float(x[1]) for x in v]
if len(vals) % 2: vals = vals[:-1]
open(f"{A}/sil.txt", "w").write("\n".join(f"{vals[i]} {vals[i+1]}" for i in range(0, len(vals), 2)) + "\n")
md = open("/home/user/osn-geografi/docs/video/B01-02-05_naskah.md").read()
blk = re.findall(r"```\n(.*?)```", md, re.S)[block]
open(f"{A}/script.txt", "w").write(blk.strip() + "\n")
al = open(f"{V}/b01v02/audio/align.py").read().replace("max(0, j - 8)", "max(0, j - 16)"); al = re.sub(r"^DUR = .*$", f"DUR = {D}", al, flags=re.M)
open(f"{A}/align.py", "w").write(al)
al_out = sh(f"cd {A} && python3 align.py")
units = json.load(open(f"{A}/units.json"))
if os.path.exists(f"{A}/fix.json"):
    for i, t in json.load(open(f"{A}/fix.json")): units[i]["t1"] = t; units[i + 1]["t0"] = t
syl2 = lambda s: max(1.5, len(re.findall(r"[aiueoAIUEO]", s)))
rate = sum(u["t1"] - u["t0"] for u in units) / sum(syl2(u["text"]) for u in units)
for u in units:
    r = (u["t1"] - u["t0"]) / (syl2(u["text"]) * rate)
    if r > 1.6 or r < 0.6: print("CHECK", u["i"], round(r, 2), u["t0"], u["t1"], u["text"][:50])
sil = [tuple(map(float, l.split())) for l in open(f"{A}/sil.txt")]
pu = next(u for u in units if u["text"].startswith("Sekarang, coba kerjakan"))
nxt = next((s0, e0) for s0, e0 in sil if s0 >= pu["t1"] - 0.05)
PAUSE_AT, PAUSE = round((nxt[0] + nxt[1]) / 2, 2), 4.0
Vt = lambda t: t + 3.0 if t < PAUSE_AT else t + 3.0 + PAUSE
syl = lambda w: max(1, len(re.findall(r"[aiueoAIUEO]", w)))
words = []
for u in units:
    a, b = u["t0"], u["t1"]; inner = [(x, y) for x, y in sil if x > a + 0.05 and y < b - 0.05]
    toks = u["text"].split(); phrases = []; cur = []
    for w in toks:
        cur.append(w)
        if re.search(r"[,:;]$", w): phrases.append(cur); cur = []
    if cur: phrases.append(cur)
    tot = sum(syl(w) for w in toks); starts = [a]; acc = 0; cand = list(inner)
    for ph in phrases[:-1]:
        acc += sum(syl(w) for w in ph); est = a + (b - a) * acc / tot
        best = min(cand, key=lambda se: abs(se[1] - est)) if cand else None
        if best and abs(best[1] - est) < 1.2: starts.append(best[1]); cand = [c for c in cand if c[1] > best[1]]
        else: starts.append(est)
    ends = starts[1:] + [b]
    for ph, s0, e0 in zip(phrases, starts, ends):
        n = sum(syl(w) for w in ph); acc = 0
        for w in ph: words.append(dict(w=w, t=round(Vt(s0 + (e0 - s0) * acc / n), 2), u=u["i"])); acc += syl(w)
for u in units: u["v0"] = round(Vt(u["t0"]), 2); u["v1"] = round(Vt(u["t1"]), 2)
DUR = round(Vt(D) + 6.5, 1)
json.dump(dict(units=units, words=words, pause=[round(Vt(PAUSE_AT - 0.01) + 0.01, 2), round(Vt(PAUSE_AT - 0.01) + PAUSE, 2)]), open(f"{B}/timing.json", "w"), ensure_ascii=False)
sh(f"""cd {A} && ffmpeg -hide_banner -loglevel error -y -i vo/raw.mp3 -filter_complex "[0:a]aresample=48000,highpass=f=80,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120,asplit=2[a][b];[a]atrim=0:{PAUSE_AT},asetpts=N/SR/TB,adelay=3000|3000[p1];[b]atrim={PAUSE_AT},asetpts=N/SR/TB,adelay=7000|7000[p2];[p1][p2]concat=n=2:v=0:a=1,apad=whole_dur={DUR},atrim=0:{DUR}[o]" -map "[o]" -ac 1 -c:a pcm_s16le vo.wav""")
M = f"{V}/b01v00/audio/music.wav"
sh(f"""cd {A} && ffmpeg -hide_banner -loglevel error -y -i {M} -i {M} -filter_complex "[0][1]acrossfade=d=4:c1=tri:c2=tri,atrim=0:{DUR},afade=t=out:st={DUR-4.5}:d=4.5[o]" -map "[o]" music.wav""")
g = json.load(open(f"{V}/b01v00/beats.json")); g.update(offset=0, period=1.0, duration=DUR); json.dump(g, open(f"{B}/beats.json", "w"))
f = json.load(open(f"{B}/film.json")); f.update(duration=DUR, poster=40, title=title); json.dump(f, open(f"{B}/film.json", "w"), indent=1)
print("DUR", DUR, "PAUSE_AT", PAUSE_AT, "units", len(units), "musiclen", sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {M}"))
