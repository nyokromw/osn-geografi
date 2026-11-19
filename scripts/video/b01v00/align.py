import re, json, math
txt = open("script.txt").read().strip()
paras = [p.strip() for p in txt.split("\n\n")]
units = []  # (text, para_idx, is_para_end)
for pi, p in enumerate(paras):
    ss = re.findall(r"[^.?!:]+[.?!:]", p)
    for k, s in enumerate(ss):
        units.append((s.strip(), pi, k == len(ss) - 1))
def syl(s): return len(re.findall(r"[aiueoAIUEO]", s)) + 0.5 * s.count(",")
sil = [tuple(map(float, l.split())) for l in open("sil.txt")]
DUR = 188.70
# boundaries: speech starts after sil[i] end; candidate ends = sil starts
# treat leading silence
starts = [0.0] + [e for s, e in sil]   # possible unit start times
ends = [s for s, e in sil] + [DUR]      # possible unit end times
N = len(ends)
U = len(units)
tot_syl = sum(syl(u[0]) for u in units)
speech = DUR - sum(e - s for s, e in sil)
rate = speech / tot_syl
INF = 1e18
# dp[k][j]: unit k ends at ends[j]; unit k starts at starts[i] where i = prev end index+1
dp = [[INF] * N for _ in range(U)]; bk = [[-1] * N for _ in range(U)]
def cost(k, i, j):
    # unit k spans starts[i] .. ends[j], internal silences between subtract
    a, b = starts[i], ends[j]
    if b <= a: return INF
    inner = sum(min(e, b) - max(s, a) for s, e in sil if s >= a and e <= b)
    d = (b - a - inner)
    exp = syl(units[k][0]) * rate
    c = math.log(d / exp) ** 2 * 10
    gap = (sil[j][1] - sil[j][0]) if j < len(sil) else 1
    if units[k][2]: c -= 1.5 * min(gap, 1.0)   # paragraph ends like long pauses
    else: c -= 0.6 * min(gap, 0.7)
    return c
for j in range(N):
    dp[0][j] = cost(0, 0, j)
for k in range(1, U):
    for j in range(N):
        best = INF
        for jp in range(max(0, j - 8), j):
            if dp[k-1][jp] >= INF: continue
            c = dp[k-1][jp] + cost(k, jp + 1, j)
            if c < best: best, bk[k][j] = c, jp
        dp[k][j] = best
j = N - 1; path = []
for k in range(U - 1, -1, -1):
    path.append(j); j = bk[k][j]
path = path[::-1]
out = []
prev = -1
for k, j in enumerate(path):
    a = starts[prev + 1]; b = ends[j]; prev = j
    out.append(dict(i=k, p=units[k][1], t0=round(a, 2), t1=round(b, 2), text=units[k][0]))
    print(f"{k:2d} P{units[k][1]} {a:7.2f}-{b:7.2f}  {units[k][0][:70]}")
json.dump(out, open("units.json", "w"), indent=1, ensure_ascii=False)
