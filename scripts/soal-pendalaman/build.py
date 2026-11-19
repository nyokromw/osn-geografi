"""Build a chapter: render figures, balance keys, lint options, upload images, update Supabase rows.

usage: python3 build.py NN [--upload] [--push]
Chapter module chNN.py must define PAKETS: list of 6 lists x 10 dicts {t, o:[correct, d1..d4], e, f?}.
Order of PAKETS = [Gratis, 01, 02, 03, 04, 05].
"""
import sys, os, json, random, importlib, subprocess, statistics, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BASE = "https://lhzlcaxlemlmjhfmichz.supabase.co"
KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_QFpgNTMxHxMmGoD-MU8KWw_pwZftVMX")
# chapter -> paket ids in order [Gratis, 01..05]
PAKET_IDS = {1: [3, 16, 17, 18, 19, 20], 2: [6, 21, 22, 23, 24, 25], 3: [7, 26, 27, 28, 29, 30],
             4: [8, 31, 32, 33, 34, 35], 5: [5, 36, 37, 38, 39, 40], 6: [9, 41, 42, 43, 44, 45],
             7: [10, 46, 47, 48, 49, 50], 8: [11, 51, 52, 53, 54, 55], 9: [12, 56, 57, 58, 59, 60],
             10: [13, 61, 62, 63, 64, 65], 11: [14, 66, 67, 68, 69, 70], 12: [15, 71, 72, 73, 74, 75],
             13: [4, 76, 77, 78, 79, 80]}
L = "ABCDE"
VERSION = "v2"


def balanced_keys(seed):
    rnd = random.Random(seed)
    while True:
        k = list("AABBCCDDEE")
        rnd.shuffle(k)
        if all(not (k[i] == k[i + 1] == k[i + 2]) for i in range(8)) and all(k[i] != k[i + 1] for i in range(9)):
            return k


def lint(ch, pi, qi, q):
    warn = []
    o = q["o"]
    if len(o) != 5 or len(set(o)) != 5:
        warn.append("options not 5 unique")
    lens = [len(x) for x in o]
    others = lens[1:]
    med = statistics.median(others)
    if med >= 12:
        if lens[0] > max(others) and lens[0] > 1.25 * med:
            warn.append(f"correct LONGEST {lens}")
        if lens[0] < min(others) and lens[0] < 0.7 * med:
            warn.append(f"correct SHORTEST {lens}")
    if len(q["e"]) < 250:
        warn.append(f"short explanation {len(q['e'])}")
    for w in warn:
        print(f"  ch{ch} p{pi} q{qi+1}: {w} :: {q['t'][:60]}")
    return warn


def rest(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"apikey": KEY, "Content-Type": "application/json", "Prefer": "return=minimal"})
    with urllib.request.urlopen(req) as r:
        return r.read().decode()


def upload(local, remote):
    url = f"{BASE}/storage/v1/object/soal-images/{remote}"
    out = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", "x-upsert: true", "-H", "Content-Type: image/png",
                          "--data-binary", f"@{local}"], capture_output=True, text=True)
    if '"Key"' not in out.stdout:
        raise RuntimeError(out.stdout + out.stderr)
    return f"{BASE}/storage/v1/object/public/soal-images/{remote}"


def main():
    ch = int(sys.argv[1]); do_upload = "--upload" in sys.argv; do_push = "--push" in sys.argv
    mod = importlib.import_module(f"ch{ch:02d}")
    P = mod.PAKETS
    assert len(P) == 6, len(P)
    outdir = os.path.join(HERE, "out", f"ch{ch:02d}"); os.makedirs(outdir, exist_ok=True)
    rows = []; nwarn = 0
    for pi, pk in enumerate(P):
        assert len(pk) == 10, (pi, len(pk))
        keys = balanced_keys(ch * 100 + pi)
        nimg = 0
        for qi, q in enumerate(pk):
            nwarn += len(lint(ch, pi, qi, q))
            img = None
            if q.get("f"):
                nimg += 1
                img = os.path.join(outdir, f"p{pi}_q{qi+1:02d}.png")
                q["f"](img)
            k = keys[qi]; idx = L.index(k)
            d = q["o"][1:]
            opts = d[:idx] + [q["o"][0]] + d[idx:]
            rows.append(dict(pi=pi, qi=qi, pertanyaan=q["t"].strip(), img=img, opts=opts, key=k,
                             pembahasan=f"Jawaban: {k}. {q['o'][0]}\n\n" + q["e"].strip()))
        print(f"paket {pi}: {nimg} gambar, kunci {''.join(keys)}")
        if nimg < 5:
            print(f"  !! paket {pi} has only {nimg} images"); nwarn += 1
    print("warnings:", nwarn)
    json.dump([{k: v for k, v in r.items()} for r in rows], open(os.path.join(outdir, "rows.json"), "w"), ensure_ascii=False, indent=1)
    if not do_upload:
        return
    for r in rows:
        if r["img"]:
            r["url"] = upload(r["img"], f"pendalaman/{VERSION}/bab{ch:02d}/p{r['pi']}_q{r['qi']+1:02d}.png")
    if not do_push:
        return
    for pi, pid in enumerate(PAKET_IDS[ch]):
        ids = [x["id"] for x in json.loads(rest("GET", f"/rest/v1/soal_pendalaman?select=id&paket_id=eq.{pid}&order=id"))]
        prow = [r for r in rows if r["pi"] == pi]
        assert len(ids) == len(prow) == 10, (pid, len(ids))
        for sid, r in zip(ids, prow):
            body = dict(pertanyaan=r["pertanyaan"], gambar_url=r.get("url"), jawaban_benar=r["key"],
                        pembahasan=r["pembahasan"], **{f"pilihan_{L[i].lower()}": r["opts"][i] for i in range(5)})
            rest("PATCH", f"/rest/v1/soal_pendalaman?id=eq.{sid}", body)
        print(f"pushed paket {pid}")


if __name__ == "__main__":
    main()
