"""Align the VO script to the audio using detected pauses, then write ASS subtitles + scene timings."""
import json, re, subprocess, sys

AUDIO, OUT = sys.argv[1], sys.argv[2]
SCRIPT = open(sys.argv[3]).read().strip()

dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', AUDIO]))
log = subprocess.run(['ffmpeg', '-hide_banner', '-i', AUDIO, '-af', 'silencedetect=n=-35dB:d=0.18', '-f', 'null', '-'], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
sil = list(zip(st, en))
lead = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
tail = sil[-1][0] if sil and sil[-1][1] > dur - 0.05 else dur
sil = [s for s in sil if s[0] > lead + 0.05 and s[1] < tail - 0.05]

# phrases split at punctuation
phrases = [p.strip() for p in re.split(r'(?<=[.,:?!])\s+', SCRIPT.replace('\n', ' ')) if p.strip()]
w = [len(re.sub(r'[^\w]', '', p)) + 3 for p in phrases]  # chars + small per-phrase cost
speech = (tail - lead) - sum(e - s for s, e in sil)
# Map phrase boundaries to silences with monotonic DP.
cum = [0]
for x in w: cum.append(cum[-1] + x)
total = cum[-1]
n, m = len(phrases) - 1, len(sil)  # boundaries, silences
# predicted time of boundary k given s silences already used before it: lead + speech*frac + used silence
INF = 1e9
dp = [[INF] * (m + 1) for _ in range(n + 1)]
bk = [[None] * (m + 1) for _ in range(n + 1)]
dp[0][0] = 0
# state (k boundaries processed, j silences consumed)
for k in range(n + 1):
    for j in range(m + 1):
        c = dp[k][j]
        if c >= INF: continue
        # skip silence j (pause inside a phrase)
        if j < m and c + 1.2 < dp[k][j + 1]:
            dp[k][j + 1] = c + 1.2; bk[k][j + 1] = ('s', k, j)
        if k < n:
            frac = cum[k + 1] / total
            used = sum(e - s for s, e in sil[:j])
            pred = lead + speech * frac + used
            # boundary k matched to silence j
            if j < m:
                mid = sil[j][0]
                cost = c + abs(pred - mid) * 2 - (0.4 if phrases[k].endswith(('.', '?', ':')) else 0.1)
                if cost < dp[k + 1][j + 1]:
                    dp[k + 1][j + 1] = cost; bk[k + 1][j + 1] = ('m', k, j)
            # boundary without pause
            if c + 0.6 < dp[k + 1][j]:
                dp[k + 1][j] = c + 0.6; bk[k + 1][j] = ('n', k, j)
# backtrack
k, j = n, m
match = {}
while (k, j) != (0, 0):
    t, pk, pj = bk[k][j]
    if t == 'm': match[pk] = pj
    k, j = pk, pj
# anchors: boundary index -> (end of phrase time, start of next phrase time)
anchors = [(0, lead, lead)]
for b in sorted(match):
    s, e = sil[match[b]]
    anchors.append((b + 1, s, e))
anchors.append((len(phrases), tail, tail))
times = [None] * len(phrases)
for (a, _, a_start), (b, b_end, _) in zip(anchors, anchors[1:]):
    seg = phrases[a:b]; ws = w[a:b]; T = b_end - a_start; t = a_start
    inner = [x for x in sil if x[0] > a_start and x[1] < b_end]
    pause = sum(e - s for s, e in inner)
    for i, p in enumerate(seg):
        d = (T - pause) * ws[i] / sum(ws)
        times[a + i] = [t, t + d + (pause * ws[i] / sum(ws))]
        t = times[a + i][1]

# subtitle chunks (<= 5 words, no orphan single words)
def chunks(text):
    words = text.split()
    if len(words) <= 5: return [words]
    k = -(-len(words) // 5)
    size = -(-len(words) // k)
    return [words[i:i + size] for i in range(0, len(words), size)]

def ts(x):
    h = int(x // 3600); m_ = int(x % 3600 // 60); s = x % 60
    return f'{h}:{m_:02d}:{s:05.2f}'

ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1080', 'PlayResY: 1920', 'WrapStyle: 0', '',
       '[V4+ Styles]',
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       'Style: Sub,OSN Sub,70,&H00FAFEFF,&H00FAFEFF,&H00231916,&H96231916,0,0,0,0,100,100,-1,0,1,7,0,2,90,90,420,1', '',
       '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
KEY = re.compile(r'(?i)\b(video animasi|tiga belas topik|seratus video|gratis|puluhan paket tryout|pembahasan|grafik kemajuan|OSN-GEO dot ID|OSNGEO dot ID|abstrak|Ujung Kulon|puluhan ekor|satu bencana|tsunami|wabah penyakit|kawin sedarah|keragaman genetik|populasi kedua|kajian ilmiah|habitat utama|Alas Purwo|Baluran|menolak|stres|mati|pakan|sumber air|berkubang|daya dukung|habitat|fauna Asiatis|garis Wallace|OSN Geografi|OSN|dipindahkan|langka)\b')
for p, (a, b) in zip(phrases, times):
    cs = chunks(p); tot = sum(len(' '.join(c)) for c in cs); t = a
    for c in cs:
        d = (b - a) * len(' '.join(c)) / tot
        txt = ' '.join(c).rstrip(',')
        txt = KEY.sub(lambda mm: '{\\c&H4F79E0&}' + mm.group(0) + '{\\c&H00FAFEFF&}', txt)
        ass.append(f'Dialogue: 0,{ts(t)},{ts(min(t + d + 0.05, b))},Sub,,0,0,0,,{{\\fad(60,40)}}{txt}')
        t += d
open(f'{OUT}/subtitles.ass', 'w').write('\n'.join(ass) + '\n')

# scene cues: first phrase containing the cue text
cues = [('hook','Pernah'),('globe','Bumi berputar'),('indo','Indonesia membentang'),('zona','Makanya'),('quiz','Sekarang'),('cta','Soal hitungan')]
scene = []
for name, cue in cues:
    i = next(i for i, p in enumerate(phrases) if p.startswith(cue))
    scene.append([name, round(times[i][0] - (0.15 if i else times[i][0]), 3)])
json.dump({'duration': dur, 'scenes': scene, 'phrases': [[p, round(a, 2), round(b, 2)] for p, (a, b) in zip(phrases, times)]}, open(f'{OUT}/timing.json', 'w'), indent=1, ensure_ascii=False)
for p, (a, b) in zip(phrases, times): print(f'{a:6.2f}-{b:6.2f}  {p}')
print(scene)
