// B01-16 · Pola Hujan Indonesia · OSNGEO.id — pure function of time (seconds). New style.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { tag, bigNum, gumpal } from './lib/gumpal.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 223.9;
const u = (i) => U_(i).v0;
let IND = null, MAL = null;
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(k); ctx.restore(); };

const DATA = { U: [320, 290, 250, 180, 120, 80, 50, 40, 60, 120, 210, 300], M: [230, 190, 290, 260, 200, 150, 140, 170, 220, 330, 350, 280], N: [130, 130, 140, 280, 520, 630, 600, 410, 250, 150, 110, 140] };
const COL = { U: C.blue, M: C.forestL, N: C.clay };
const REG = {
  U: [[105, 115, -9, -5.8], [114.4, 125, -11, -7.8], [101.5, 106.5, -6, -2.2], [110, 117, -4.3, -1.6], [118.8, 123, -6, -3.2]],
  M: [[95, 104.5, -2.2, 6], [108.5, 117.5, -1.6, 4.5]],
  N: [[125.5, 131, -4.6, -2.4], [121.5, 124.2, -2.6, 0.6], [134, 141, -3, -0.8]],
};
// bar chart with optional morph into a letter
function letterPts(L, x, y, w, h, n = 48) {
  const pts = []; const r = w / 2, L1 = h - r, tot = 2 * L1 + Math.PI * r;
  for (let i = 0; i < n; i++) { const f = i / (n - 1); let px, py;
    if (L === 'M') { const s = f * 4, k = Math.floor(Math.min(3.999, s)), q = s - k; const P = [[0, h], [0.22, 0], [0.5, h * 0.62], [0.78, 0], [1, h]]; px = x + w * lerp(P[k][0], P[k + 1][0], q); py = y + lerp(P[k][1], P[k + 1][1], q); }
    else { const d = f * tot; if (d < L1) { px = x; py = y + d; } else if (d < L1 + Math.PI * r) { const a = Math.PI - (d - L1) / r; px = x + r + Math.cos(a) * r; py = y + L1 + Math.sin(a) * r; } else { px = x + w; py = y + L1 - (d - L1 - Math.PI * r); }
      if (L === 'N') py = y + h - (py - y); }
    pts.push([px, py]); }
  return pts;
}
function chart(ctx, t, x, y, w, h, key, grow, morph) {
  const d = DATA[key], col = COL[key], bw = w / 12;
  ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h); ctx.lineTo(x + w, y + h); ctx.stroke();
  d.forEach((v, i) => { const bh = h * v / 650 * clamp(grow * 1.5 - i * 0.04); ctx.save(); ctx.globalAlpha *= 1 - morph * 0.75; rrect(ctx, x + i * bw + 6, y + h - bh, bw - 12, bh, 8); ctx.fillStyle = col; ctx.fill(); ctx.restore(); text(ctx, 'JFMAMJJASOND'[i], x + (i + 0.5) * bw, y + h + 34, fU(24, 800), C.gray, 'center'); });
  if (morph > 0) {
    const n = 48, src = []; for (let i = 0; i < n; i++) { const f = i / (n - 1) * 11; const k = Math.floor(Math.min(10.999, f)), r = f - k; const v = lerp(d[k], d[k + 1], (1 - Math.cos(r * Math.PI)) / 2); src.push([x + (f + 0.5) * bw, y + h - h * v / 650]); }
    const dst = letterPts(key, x + w * 0.3, y + h * 0.05, w * 0.4, h * 0.9, n); const k = E.inOutCubic(clamp(morph));
    ctx.strokeStyle = col; ctx.lineWidth = lerp(8, 34, k); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.beginPath(); src.forEach((p, i) => { const q = [lerp(p[0], dst[i][0], k), lerp(p[1], dst[i][1], k)]; i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.stroke();
  }
}
function indoMap(ctx, t, box, ext, regs, k, col) {
  const pr = G.mapProj(box, ext); G.drawMap(ctx, IND, pr, { t, depth: 8 });
  if (k > 0) { ctx.save(); ctx.beginPath(); for (const r of IND) { r.forEach(([lo, la], i) => { const [xx, yy] = pr(lo, la); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }); ctx.closePath(); } ctx.clip(); regs.forEach(([a, b, c, d], i) => { const kk = clamp(k * 1.5 - i * 0.15); if (kk <= 0) return; const p = pr(a, d), q = pr(b, c); ctx.globalAlpha = 0.75 * kk; ctx.fillStyle = col; ctx.fillRect(p[0], p[1], q[0] - p[0], q[1] - p[1]); }); ctx.restore(); }
  return pr;
}
const MAPBOX = { x: 960, y: 250, w: 900, h: 560 }, MAPEXT = [94, 142, -11.5, -11.5 + 48 * 560 / 900];

// ---------------------------------------------------------------- hook: mystery graph
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#f2efe8', () => {
    ctx.save(); ctx.globalAlpha *= 0.35; G.drawMap(ctx, IND, G.mapProj({ x: 0, y: 0, w: W, h: H }, [93, 143, -18, 13]), { t, waves: false }); ctx.restore();
    const k = sp(t, u(0), SPRING.gentle); ctx.save(); ctx.translate(W / 2, 560 + (1 - k) * 200); ctx.rotate(Math.sin(t * 0.8) * 0.03); card(ctx, -420, -300, 840, 560, { r: 30 }); chart(ctx, t, -340, -230, 680, 380, 'M', ap(t, u(0) + 0.5, 2), 0); ctx.restore();
    const q = sp(t, tw('ada', u(0)), SPRING.bouncy); if (q > 0) { ctx.save(); ctx.translate(W / 2 + 470, 300); ctx.scale(q, q); text(ctx, '?', 0, 60, fD(200), C.clay, 'center'); ctx.restore(); }
    show_(ctx, t, u(2), 1e9, () => { ['U', 'M', '∩'].forEach((s, i) => { const kk = sp(t, u(2) + 0.6 + i * 0.4, SPRING.bouncy); ctx.save(); ctx.translate(560 + i * 400, 150); ctx.scale(kk, kk); circle(ctx, 0, 0, 70); ctx.fillStyle = [C.blue, C.forestL, C.clay][i]; ctx.fill(); if (s === '∩') { ctx.rotate(Math.PI); text(ctx, 'U', 0, 30, fU(84, 800), C.cream, 'center'); } else text(ctx, s, 0, 30, fU(84, 800), C.cream, 'center'); ctx.restore(); }); });
  });
}
// ---------------------------------------------------------------- one scene per pattern
function sMons(ctx, t) {
  scene(ctx, t, 'mons', '#f2efe8', () => {
    const map = t >= u(8) - 0.5;
    chart(ctx, t, map ? 120 : 360, 300, map ? 700 : 1200, map ? 420 : 520, 'U', ap(t, u(3) + 0.3, 2.5), ap(t, u(5), 1.6));
    show_(ctx, t, u(4), u(5), () => { tag(ctx, 380, 230, 'puncak Des–Jan', '', 1, C.blue); tag(ctx, 1300, 230, 'kemarau Jun–Agu', '', 1, C.clay); });
    show_(ctx, t, u(5), 1e9, () => tag(ctx, map ? 470 : 960, 210, 'pola monsunal', 'monsoonal pattern', 1, C.blue));
    show_(ctx, t, u(6), u(8) - 0.3, () => { const x = 1560, y = 420; cloud(ctx, x - 90, y, 1.2, '#c3ccd4'); rain(ctx, x - 90, y + 30, 120, t, 6); text(ctx, 'monsun barat', x - 90, y + 160, fU(28, 800), C.blue, 'center'); sun(ctx, x + 130, y, 40, t); text(ctx, 'monsun timur', x + 130, y + 160, fU(28, 800), C.clayD, 'center'); });
    if (map) { indoMap(ctx, t, MAPBOX, MAPEXT, REG.U, ap(t, u(8), 3), C.blue); }
    show_(ctx, t, u(9), 1e9, () => { const x = 470, y = 880; rrect(ctx, x - 300, y - 60, 600, 120, 24); ctx.fillStyle = C.forest; ctx.fill(); const lv = 30 + 20 * Math.sin(t * 2); ctx.fillStyle = 'rgba(90,168,224,0.8)'; ctx.fillRect(x - 280, y + 40 - lv * 0.6, 120, lv * 0.6); text(ctx, 'banjir Jan–Feb', x + 60, y + 14, fU(38, 800), C.cream, 'center'); });
  });
}
function sEkua(ctx, t) {
  scene(ctx, t, 'ekua', '#f2efe8', () => {
    const phase = t < u(13) ? 0 : t < u(16) ? 1 : 2;
    if (phase !== 1) chart(ctx, t, phase === 2 ? 120 : 360, 300, phase === 2 ? 700 : 1200, phase === 2 ? 420 : 520, 'M', ap(t, u(10) + 0.3, 2.5), ap(t, u(12), 1.6));
    show_(ctx, t, u(11), u(12), () => { tag(ctx, 600, 230, 'puncak Maret', '', 1, C.forestL); tag(ctx, 1380, 230, 'puncak Okt–Nov', '', 1, C.forestL); });
    show_(ctx, t, u(12), u(13), () => tag(ctx, 960, 210, 'pola ekuatorial', 'equatorial pattern', 1, C.forestL));
    if (phase === 1) {
      // sun's apparent path across the year
      const x0 = 260, x1 = 1660, yE = 560, A = 230; const X = (m) => lerp(x0, x1, m / 12), Y = (m) => yE - A * Math.sin((m - 2.7) / 12 * Math.PI * 2);
      ctx.fillStyle = 'rgba(242,177,58,0.12)'; ctx.fillRect(x0, yE - A, x1 - x0, 2 * A);
      [[yE - A, '23,5° LU'], [yE, 'ekuator'], [yE + A, '23,5° LS']].forEach(([y, s], i) => { ctx.setLineDash(i === 1 ? [] : [12, 10]); ctx.strokeStyle = i === 1 ? C.clayD : C.gray; ctx.lineWidth = i === 1 ? 5 : 3; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y); ctx.stroke(); ctx.setLineDash([]); text(ctx, s, x0 - 20, y + 9, fU(24, 800), i === 1 ? C.clayD : C.gray, 'right'); });
      const p = ap(t, u(14), 4.5, E.linear); ctx.strokeStyle = C.amber; ctx.lineWidth = 6; ctx.beginPath(); for (let m = 0; m <= 12 * p; m += 0.1) m ? ctx.lineTo(X(m), Y(m)) : ctx.moveTo(X(m), Y(m)); ctx.stroke();
      const m = 12 * p; sun(ctx, X(m), Y(m), 36, t);
      'JFMAMJJASOND'.split('').forEach((s, i) => text(ctx, s, X(i + 0.5), yE + A + 60, fU(24, 800), C.gray, 'center'));
      [2.7, 8.7].forEach((mm, i) => show_(ctx, t, u(14) + (mm / 12) * 4.5, 1e9, () => { circle(ctx, X(mm), yE, 22); ctx.fillStyle = C.clayD; ctx.fill(); cloud(ctx, X(mm), yE - 110, 1.1, '#c3ccd4'); rain(ctx, X(mm), yE - 80, 90, t + i, 6); text(ctx, i ? 'September' : 'Maret', X(mm), yE + 60, fU(28, 800), C.clayD, 'center'); }));
      show_(ctx, t, u(15), 1e9, () => tag(ctx, 960, 200, 'ITCZ melintas dua kali', '', 1, C.forestL));
    }
    if (phase === 2) { const pr = indoMap(ctx, t, MAPBOX, MAPEXT, REG.M, ap(t, u(16), 3), C.forestL); show_(ctx, t, u(17), 1e9, () => { [['Pontianak', 109.3, 0], ['Padang', 100.4, -0.95]].forEach(([n, lo, la]) => { const p = pr(lo, la); circle(ctx, p[0], p[1], 12); ctx.fillStyle = C.ink; ctx.fill(); pill(ctx, n, p[0], p[1] - 34, fU(24, 800), C.forest, C.cream, 14, 44, 'center'); }); }); show_(ctx, t, u(16), 1e9, () => tag(ctx, 470, 210, 'pola ekuatorial', 'equatorial pattern', 1, C.forestL)); }
  });
}
function sLokal(ctx, t) {
  scene(ctx, t, 'lokal', '#f2efe8', () => {
    const phase = t < u(22) ? 0 : t < u(25) ? 1 : 2;
    if (phase === 0) { chart(ctx, t, 360, 300, 1200, 520, 'N', ap(t, u(18) + 0.3, 2.5), ap(t, u(20), 1.6)); show_(ctx, t, u(19), u(20), () => tag(ctx, 960, 230, 'puncak Juni–Juli', '', 1, C.clay)); show_(ctx, t, u(20), 1e9, () => tag(ctx, 960, 210, 'pola lokal', 'local pattern', 1, C.clay)); }
    if (phase === 1) {
      const pr = G.mapProj({ x: 0, y: 0, w: W, h: H }, [122.3, 134.7, -8.2, -8.2 + 12.4 * H / W]); G.drawMap(ctx, MAL, pr, { t, depth: 10 });
      const sea = pr(128, -6); text(ctx, 'Laut Banda', sea[0], sea[1], fU(40, 800), '#4a7da0', 'center');
      for (let i = 0; i < 8; i++) { const ph = (t * 0.35 + i / 8) % 1; const a = pr(lerp(133.5, 129.4, ph) + (i % 3) * 0.4, lerp(-8.3, -3.9, ph) + (i % 2) * 0.3), b = pr(lerp(133.5, 129.4, ph) + (i % 3) * 0.4 - 0.6, lerp(-8.3, -3.9, ph) + (i % 2) * 0.3 + 0.7); ctx.globalAlpha = Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], mix(C.clay, C.blue, ph), 12, 34); ctx.globalAlpha = 1; }
      show_(ctx, t, u(22), 1e9, () => { const p = pr(132.6, -8.2); pill(ctx, 'dari Australia: kering', p[0], p[1], fU(28, 800), C.clay, C.cream, 18, 52, 'center'); });
      show_(ctx, t, u(23), 1e9, () => { const s = pr(129.4, -3.05); ctx.fillStyle = '#8a7350'; poly(ctx, [[s[0] - 120, s[1] + 30], [s[0] - 20, s[1] - 90], [s[0] + 90, s[1] + 30]]); ctx.fill(); cloud(ctx, s[0] - 20, s[1] - 140, 1.6, '#c3ccd4'); rain(ctx, s[0] - 20, s[1] - 100, 140, t, 8); pill(ctx, 'Seram', s[0], s[1] + 70, fU(26, 800), C.forest, C.cream, 14, 46, 'center'); const a = pr(128.2, -3.7); circle(ctx, a[0], a[1], 12); ctx.fillStyle = C.ink; ctx.fill(); pill(ctx, 'Ambon', a[0] - 40, a[1] + 40, fU(26, 800), C.forest, C.cream, 14, 46, 'center'); });
      show_(ctx, t, u(24), 1e9, () => tag(ctx, W / 2, 180, 'hujan orografis', 'orographic rain', 1, C.blue));
    }
    if (phase === 2) { chart(ctx, t, 120, 300, 700, 420, 'N', 1, 1); indoMap(ctx, t, MAPBOX, MAPEXT, REG.N, ap(t, u(25), 3), C.clay); tag(ctx, 470, 210, 'pola lokal', 'local pattern', 1, C.clay); }
  });
}
function sHafal(ctx, t) {
  scene(ctx, t, 'hafal', C.forestD, () => {
    const L = [['U', 'monsunal', C.blue, tw('monsunal', u(27))], ['M', 'ekuatorial', C.forestL, tw('ekuatorial', u(27))], ['∩', 'lokal', C.clay, tw('lokal', u(27))]];
    L.forEach(([s, n, col, t0], i) => { const k = sp(t, t0 - 0.2, SPRING.bouncy); if (k <= 0) return; ctx.save(); ctx.translate(480 + i * 480, 520); ctx.scale(k, k); circle(ctx, 0, 0, 190); ctx.fillStyle = col; ctx.fill(); if (s === '∩') { ctx.save(); ctx.rotate(Math.PI); text(ctx, 'U', 0, 90, fU(260, 800), C.cream, 'center'); ctx.restore(); } else text(ctx, s, 0, 90, fU(260, 800), C.cream, 'center'); text(ctx, n, 0, 290, fU(48, 800), C.cream, 'center'); ctx.restore(); });
  });
}
function sJumlah(ctx, t) {
  scene(ctx, t, 'jumlah', '#e9eef1', () => {
    const pr = G.mapProj({ x: 0, y: 40, w: W, h: H }, [93, 143, -16, -16 + 50 * H / W]); G.drawMap(ctx, IND, pr, { t, depth: 10 });
    const pillar = (lo, la, mm, col, lab, t0) => { const k = ap(t, t0, 1.5, E.outCubic); if (k <= 0) return; const p = pr(lo, la), h = mm / 4000 * 330 * k, w = 46; ctx.fillStyle = mix(col, '#000', 0.25); poly(ctx, [[p[0] + w / 2, p[1]], [p[0] + w / 2 + 18, p[1] - 12], [p[0] + w / 2 + 18, p[1] - 12 - h], [p[0] + w / 2, p[1] - h]]); ctx.fill(); ctx.fillStyle = col; ctx.fillRect(p[0] - w / 2, p[1] - h, w, h); ctx.fillStyle = mix(col, '#fff', 0.3); poly(ctx, [[p[0] - w / 2, p[1] - h], [p[0] + w / 2, p[1] - h], [p[0] + w / 2 + 18, p[1] - h - 12], [p[0] - w / 2 + 18, p[1] - h - 12]]); ctx.fill(); if (k > 0.6) { text(ctx, `${Math.round(mm * k).toLocaleString('id-ID')} mm`, p[0], p[1] - h - 30, fU(26, 800), C.ink, 'center'); text(ctx, lab, p[0], p[1] + 34, fU(24, 800), C.ink, 'center'); } };
    pillar(119.87, -0.9, 650, C.clay, 'Palu', u(29));
    pillar(100.5, -1.2, 4000, C.blue, 'Bukit Barisan', tw('Bukit', u(30)));
    pillar(138.5, -4.0, 4000, C.blue, 'Papua (pegunungan)', tw('Papua', u(30)));
    show_(ctx, t, u(31), 1e9, () => { const p = pr(123.6, -10.2); sun(ctx, p[0], p[1] - 60, 40, t); pill(ctx, 'NTT: kemarau terpanjang', p[0], p[1] + 40, fU(26, 800), C.clayD, C.cream, 16, 48, 'center'); });
    show_(ctx, t, u(28), u(29), () => tag(ctx, W / 2, 160, 'jumlah hujan per tahun', '', 1, C.forest));
  });
}

run({
  DUR, no: 16, code: 'B01-16', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Pola Hujan Indonesia', sub: 'monsunal, ekuatorial, dan lokal',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-17 · Klasifikasi Iklim',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['mons', 3], ['ekua', 10], ['lokal', 18], ['hafal', 26], ['jumlah', 28], ['soal', 32], ['jebakan', 37], ['ringkas', 43], ['outro', 46]],
  TERMS: [
    ['Pola monsunal', 'monsoonal pattern', '', 5],
    ['Pola ekuatorial', 'equatorial pattern', '', 12],
    ['Pola lokal', 'local pattern', '', 20],
    ['Bayangan hujan', 'rain shadow', '', 29],
  ],
  hook: { cards: [], punch: [2, ''] },
  soal: {
    q: 'Sebuah grafik curah hujan bulanan menunjukkan dua puncak, yaitu sekitar Maret dan November, tanpa bulan yang benar-benar kering. Wilayah yang paling sesuai adalah …',
    opts: ['Kalimantan Barat', 'Nusa Tenggara Timur', 'Ambon', 'Jawa Timur', 'Bali'], ans: 0, optFs: 32,
    ansT: () => tw('jawabannya', u(36) - 0.3),
    steps: () => [[u(33), 'dua puncak: Maret dan Nov', C.cream, 38], [u(34), '= huruf M', C.amber, 56], [tw('ekuatorial', u(34)), 'pola ekuatorial', C.cream, 40], [u(35), 'dekat ekuator: Kalimantan Barat', C.amber, 40]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(38), 'Pola lokal dan monsunal tertukar', 'Lihat puncak: monsunal Desember, lokal Juni', u(40)],
      [u(41), 'Ekuatorial = hujan merata sepanjang tahun', 'Tetap ada DUA puncak yang jelas', u(42)]],
  },
  ringkas: {
    items: () => [[tw('monsunal', u(44)), 'Monsunal: huruf U, karena monsun'], [tw('ekuatorial', u(44)), 'Ekuatorial: huruf M, ITCZ melintas dua kali'], [tw('lokal', u(44)), 'Lokal: U terbalik, kondisi setempat (Ambon)']],
  },
  scenes: { hook: sHook, mons: sMons, ekua: sEkua, lokal: sLokal, hafal: sHafal, jumlah: sJumlah },
  async init() {
    const W50 = await fetch('assets/world50.json').then((r) => r.json());
    IND = G.subset(W50, [90, 145, -18, 12]); MAL = G.subset(W50, [118, 140, -12, 2]);
  },
});
