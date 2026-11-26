// B01-17 · Klasifikasi Iklim · OSNGEO.id — pure function of time (seconds). New style.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, rain, check } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { tag, bigNum } from './lib/gumpal.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 244.2;
const u = (i) => U_(i).v0;
let W110 = null;
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(k); ctx.restore(); };

// ---------------------------------------------------------------- people
function person(ctx, x, y, s, kind, t, k = 1) {
  if (k <= 0) return; ctx.save(); ctx.globalAlpha *= clamp(k); ctx.translate(x, y + Math.sin(t * 2 + x) * 3); ctx.scale(s, s);
  const shirt = { petani: '#3f8a52', rimbawan: '#8a6a44', ilmuwan: '#2b6cb0' }[kind];
  rrect(ctx, -60, -40, 120, 170, 40); ctx.fillStyle = shirt; ctx.fill();
  circle(ctx, 0, -95, 52); ctx.fillStyle = '#e6b98f'; ctx.fill();
  [-1, 1].forEach((d) => { circle(ctx, d * 18, -100, 6); ctx.fillStyle = '#1b322b'; ctx.fill(); }); ctx.strokeStyle = '#1b322b'; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(0, -82, 14, 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke();
  if (kind === 'petani') { ctx.fillStyle = '#d9b46a'; poly(ctx, [[-90, -125], [0, -185], [90, -125]]); ctx.fill(); ctx.strokeStyle = '#3f8a52'; ctx.lineWidth = 6; for (let i = 0; i < 4; i++) { ctx.beginPath(); ctx.moveTo(80 + i * 8, 120); ctx.quadraticCurveTo(90 + i * 8, 40, 120 + i * 10, 10 + Math.sin(t * 2 + i) * 5); ctx.stroke(); } }
  if (kind === 'rimbawan') { ctx.fillStyle = '#e0a12a'; ctx.beginPath(); ctx.ellipse(0, -138, 62, 30, 0, Math.PI, 0); ctx.fill(); ctx.fillRect(-72, -140, 144, 10); ctx.fillStyle = '#6b4a2b'; ctx.fillRect(108, 20, 16, 110); circle(ctx, 116, 0, 48); ctx.fillStyle = '#2f7d4a'; ctx.fill(); }
  if (kind === 'ilmuwan') { ctx.fillStyle = '#2b2b2b'; ctx.fillRect(-36, -108, 30, 14); ctx.fillRect(6, -108, 30, 14); circle(ctx, 120, 20, 50); ctx.fillStyle = '#7fb3d5'; ctx.fill(); ctx.fillStyle = '#9dcf7e'; ctx.beginPath(); ctx.ellipse(110, 10, 22, 14, 0.3, 0, Math.PI * 2); ctx.fill(); ctx.beginPath(); ctx.ellipse(135, 40, 14, 18, 0.3, 0, Math.PI * 2); ctx.fill(); }
  ctx.restore();
}
const PEOPLE = [['petani', 'petani padi', 460], ['rimbawan', 'ahli kehutanan', 960], ['ilmuwan', 'ahli iklim dunia', 1460]];
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#f2efe8', () => {
    ctx.fillStyle = '#e8dcc6'; ctx.fillRect(0, 820, W, 260);
    const order = [1, 0, 2];
    PEOPLE.forEach(([k, lab, x], i) => { const t0 = u(0) + order[i] * 0.9; person(ctx, x, 700, 1.2, k, t, sp(t, t0, SPRING.bouncy)); show_(ctx, t, t0 + 0.4, 1e9, () => text(ctx, lab, x, 930, fU(34, 800), C.ink, 'center')); show_(ctx, t, u(1), 1e9, () => { const bob = Math.sin(t * 1.5 + i) * 6; card(ctx, x - 110, 260 + bob, 220, 150, { r: 18 }); ctx.fillStyle = ['#9dcf7e', '#5f9a5c', '#7fb3d5'][i]; rrect(ctx, x - 92, 278 + bob, 184, 114, 12); ctx.fill(); [[-50, 0], [10, -20], [50, 20]].forEach(([a, b], j) => { circle(ctx, x + a, 335 + b + bob, 16); ctx.fillStyle = ['#e9c46a', '#f4a261', '#2a9d8f'][(i + j) % 3]; ctx.fill(); }); }); });
    show_(ctx, t, u(3), 1e9, () => { ['Koppen', 'Schmidt-Ferguson', 'Oldeman'].forEach((s, i) => { const k = sp(t, tw(i === 0 ? 'Koppen' : i === 1 ? 'Schmidt' : 'Oldeman', u(3)) - 0.1, SPRING.bouncy); ctx.save(); ctx.translate(560 + i * 400, 150); ctx.scale(k, k); pill(ctx, s, 0, 0, fU(34, 800), C.forest, C.cream, 24, 64, 'center'); ctx.restore(); }); });
  });
}

// ---------------------------------------------------------------- Köppen world bands
const KG = [['A', 'tropis', '#3f9a5c', 7], ['B', 'kering', '#e0b462', 8], ['C', 'sedang', '#a7d38a', 9], ['D', 'dingin', '#7fa9d6', 10], ['E', 'kutub', '#e9f2f7', 11]];
function sKoppen(ctx, t) {
  scene(ctx, t, 'koppen', '#dfeaf2', () => {
    const box = { x: 60, y: 160, w: 1800, h: 820 }; const pr = G.mapProj(box, [-170, 190, -60, 82]);
    G.drawMap(ctx, W110, pr, { t, sea: '#cfe3ef', land: '#efe6d2', depth: 6 });
    ctx.save(); ctx.beginPath(); for (const r of W110) { r.forEach(([lo, la], i) => { const [x, y] = pr(lo, la); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); } ctx.clip();
    const band = (la0, la1, col, k) => { if (k <= 0) return; const a = pr(-180, la1), b = pr(190, la0); ctx.save(); ctx.globalAlpha *= k; ctx.fillStyle = col; ctx.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]); ctx.restore(); };
    const k = (i) => ap(t, U_(KG[i][3]).v0 - 0.2, 0.8);
    band(-20, 20, KG[0][2], k(0));
    band(30, 50, KG[2][2], k(2)); band(-45, -28, KG[2][2], k(2));
    band(50, 68, KG[3][2], k(3));
    band(68, 90, KG[4][2], k(4)); band(-90, -60, KG[4][2], k(4));
    if (k(1) > 0) { ctx.save(); ctx.globalAlpha *= k(1); ctx.fillStyle = KG[1][2]; [[10, 23, 30, 9], [45, 24, 14, 7], [134, -25, 14, 8], [-112, 32, 8, 6], [65, 40, 18, 6], [20, -24, 7, 6], [-70, -30, 3, 10]].forEach(([lo, la, a, b]) => { const p = pr(lo, la); ctx.beginPath(); ctx.ellipse(p[0], p[1], a * pr.k, b * pr.k * 1.3, 0, 0, Math.PI * 2); ctx.fill(); }); ctx.restore(); }
    ctx.restore();
    // legend letters
    KG.forEach(([L, n, col, ui], i) => { const kk = sp(t, U_(ui).v0 - 0.1, SPRING.bouncy); if (kk <= 0) return; const x = 260 + i * 330, y = 1000; ctx.save(); ctx.translate(x, y); ctx.scale(kk, kk); rrect(ctx, -140, -40, 280, 80, 40); ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = 'rgba(0,0,0,0.15)'; ctx.lineWidth = 2; ctx.stroke(); text(ctx, `${L} · ${n}`, 0, 14, fU(36, 800), C.ink, 'center'); ctx.restore(); });
    show_(ctx, t, tw('delapan', u(7)) - 0.2, u(8), () => tag(ctx, W / 2, 110, 'bulan terdingin ≥ 18 °C', '', 1, C.forestL));
    show_(ctx, t, tw('sepuluh', u(11)) - 0.2, 1e9, () => tag(ctx, W / 2, 110, 'bulan terpanas < 10 °C', '', 1, C.blue));
    show_(ctx, t, u(5), u(7), () => { ['suhu', 'hujan', 'tumbuhan'].forEach((s, i) => tag(ctx, 560 + i * 400, 110, s, '', ap(t, u(5) + i * 0.6, 0.4), C.forest)); });
  });
}

// ---------------------------------------------------------------- decision tree with rolling ball
function treeIcon(ctx, x, y, kind, t) {
  if (kind === 'Af') { for (let i = 0; i < 5; i++) { ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 70 + i * 34, y - 30, 6, 40); circle(ctx, x - 67 + i * 34, y - 44 + Math.sin(t + i) * 2, 22); ctx.fillStyle = '#2f7d4a'; ctx.fill(); } rain(ctx, x, y - 90, 140, t, 6); }
  if (kind === 'Am') { for (let i = 0; i < 4; i++) { ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 60 + i * 40, y - 30, 6, 40); circle(ctx, x - 57 + i * 40, y - 44, 18); ctx.fillStyle = '#7aa64a'; ctx.fill(); } }
  if (kind === 'Aw') { ctx.fillStyle = '#d9c28f'; ctx.fillRect(x - 90, y, 180, 12); ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 4, y - 50, 8, 52); ctx.fillStyle = '#6a8f3a'; ctx.beginPath(); ctx.ellipse(x, y - 56, 54, 16, 0, 0, Math.PI * 2); ctx.fill(); sun(ctx, x + 70, y - 90, 18, t); }
}
function sPohon(ctx, t) {
  scene(ctx, t, 'pohon', '#f2efe8', () => {
    const N1 = [960, 300], N2 = [1300, 560], L = { Af: [560, 560], Am: [1060, 830], Aw: [1560, 830] };
    const node = (p, s, k, col = C.forest) => { if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; ctx.font = fU(30, 800); const w = ctx.measureText(s).width + 70; rrect(ctx, p[0] - w / 2, p[1] - 42, w, 84, 24); ctx.fillStyle = col; ctx.fill(); text(ctx, s, p[0], p[1] + 11, fU(30, 800), C.cream, 'center'); ctx.restore(); };
    const edge = (a, b, s, k) => { if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; ctx.strokeStyle = C.gray; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(a[0], a[1] + 42); ctx.lineTo(b[0], b[1] - 42); ctx.stroke(); text(ctx, s, (a[0] + b[0]) / 2 + (b[0] < a[0] ? -30 : 30), (a[1] + b[1]) / 2, fU(26, 800), C.gray, 'center'); ctx.restore(); };
    show_(ctx, t, u(12), u(13), () => tag(ctx, W / 2, 160, 'Indonesia: hampir semua A', '', 1, C.forestL));
    const k1 = ap(t, u(13), 0.5), k2 = ap(t, u(15), 0.5);
    node(N1, 'bulan terkering ≥ 60 mm?', k1);
    edge(N1, L.Af, 'ya', ap(t, u(14), 0.4)); edge(N1, N2, 'tidak', k2);
    node(N2, 'bulan terkering ≥ 100 − P/25 ?', ap(t, u(16), 0.5), C.clayD);
    edge(N2, L.Am, 'ya', ap(t, u(17), 0.4)); edge(N2, L.Aw, 'tidak', ap(t, u(18), 0.4));
    [['Af', 'hutan hujan tropis', u(14)], ['Am', 'monsun tropis', u(17)], ['Aw', 'sabana', u(18)]].forEach(([s, d, t0]) => { const k = sp(t, t0 + 0.6, SPRING.bouncy); if (k <= 0) return; const [x, y] = L[s]; ctx.save(); ctx.translate(x, y); ctx.scale(k, k); circle(ctx, 0, 0, 62); ctx.fillStyle = C.amber; ctx.fill(); text(ctx, s, 0, 16, fU(46, 800), C.ink, 'center'); text(ctx, d, 0, 100, fU(26, 800), C.ink, 'center'); ctx.restore(); treeIcon(ctx, x, y - 90, s, t); });
    // example ball
    if (t > u(20)) {
      const p = [[600, 160], N1, N2, L.Am]; const tt = [u(20) + 1, u(21), u(22), u(24)];
      let pos = p[0]; for (let i = 0; i < 3; i++) { const f = ap(t, tt[i], 1.2, E.inOutCubic); if (f > 0) pos = [lerp(p[i][0], p[i + 1][0], f), lerp(p[i][1], p[i + 1][1], f) - Math.sin(f * Math.PI) * 60]; }
      circle(ctx, pos[0] - 120, pos[1] - 60, 44); ctx.fillStyle = C.blue; ctx.fill(); text(ctx, 'kota X', pos[0] - 120, pos[1] - 52, fU(20, 800), C.cream, 'center');
      show_(ctx, t, u(20), u(22), () => { card(ctx, 1380, 200, 460, 140, { r: 22, bg: C.blue }); text(ctx, 'P = 2.200 mm', 1410, 258, fU(34, 800), C.cream); text(ctx, 'terkering = 45 mm', 1410, 308, fU(34, 800), C.cream); });
      show_(ctx, t, u(22), 1e9, () => { card(ctx, 1380, 200, 460, 140, { r: 22, bg: C.clayD }); text(ctx, '100 − 2.200/25', 1410, 258, fU(34, 800), C.cream); text(ctx, `= ${t > tw('dua', u(22), 3) ? 12 : '…'}  ·  45 > 12`, 1410, 308, fU(34, 800), C.amber); });
    }
    show_(ctx, t, u(24), 1e9, () => { const [x, y] = L.Am; ctx.strokeStyle = C.forest; ctx.lineWidth = 8; circle(ctx, x, y, 82 + Math.sin(t * 4) * 4); ctx.stroke(); });
  });
}

// ---------------------------------------------------------------- Schmidt-Ferguson sorting machine
const MONTHS = [320, 290, 260, 180, 120, 75, 40, 30, 55, 110, 210, 300];
function sSchmidt(ctx, t) {
  scene(ctx, t, 'schmidt', '#eef2f4', () => {
    const cls = (v) => (v > 100 ? 'basah' : v >= 60 ? 'lembap' : 'kering'); const col = { basah: '#3d8ccc', lembap: '#9fc4dd', kering: '#e0b462' };
    // belt
    ctx.fillStyle = '#c9d2d8'; ctx.fillRect(100, 640, 1000, 26);
    const belt = ap(t, u(26), 6, E.linear);
    MONTHS.forEach((v, i) => { const x = 140 + i * 80 + belt * 520; const inM = x > 1060; if (inM) return; const k = ap(t, u(26) + i * 0.08, 0.3); ctx.save(); ctx.globalAlpha *= k; rrect(ctx, x - 34, 560, 68, 76, 12); ctx.fillStyle = col[cls(v)]; ctx.fill(); text(ctx, 'JFMAMJJASOND'[i], x, 610, fU(28, 800), C.cream, 'center'); ctx.restore(); });
    // machine
    ctx.save(); rrect(ctx, 1060, 420, 360, 340, 30); ctx.fillStyle = C.forest; ctx.fill(); for (let g = 0; g < 2; g++) { ctx.save(); ctx.translate(1180 + g * 120, 520); ctx.rotate(t * (g ? -1.5 : 1.5)); ctx.fillStyle = C.forestL; ctx.beginPath(); for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; const r = i % 2 ? 40 : 52; ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r); } ctx.closePath(); ctx.fill(); ctx.restore(); } text(ctx, 'Q', 1240, 700, fU(80, 800), C.amber, 'center'); ctx.restore();
    // legend
    show_(ctx, t, u(27), 1e9, () => { [['basah', '> 100 mm', u(27)], ['kering', '< 60 mm', u(28)], ['lembap', '60–100 mm', u(28) + 1]].forEach(([s, d, t0], i) => show_(ctx, t, t0, 1e9, () => { rrect(ctx, 140 + i * 330, 300, 300, 90, 20); ctx.fillStyle = col[s]; ctx.fill(); text(ctx, s, 290 + i * 330, 340, fU(32, 800), C.cream, 'center'); text(ctx, d, 290 + i * 330, 376, fU(24, 700), C.cream, 'center'); })); });
    // formula
    show_(ctx, t, u(29), 1e9, () => { card(ctx, 140, 790, 900, 130, { r: 24, bg: C.forest }); text(ctx, 'Q = bulan kering ÷ bulan basah × 100%', 590, 870, fU(38, 800), C.amber, 'center'); });
    // Q band A-H with needle
    const kq = ap(t, u(31), 0.6);
    if (kq > 0) {
      ctx.save(); ctx.globalAlpha *= kq; const bx = 1480, by = 260, bh = 640, types = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
      types.forEach((s, i) => { const y = by + i * bh / 8; rrect(ctx, bx, y + 4, 300, bh / 8 - 8, 14); ctx.fillStyle = mix('#2f7d4a', '#e0b462', i / 7); ctx.fill(); text(ctx, s, bx + 40, y + bh / 16 + 14, fU(40, 800), C.cream, 'center'); });
      text(ctx, 'basah', bx + 160, by - 14, fU(26, 800), C.forest, 'center'); text(ctx, 'kering', bx + 160, by + bh + 40, fU(26, 800), C.clayD, 'center');
      let pos = 0.5; if (t > u(32)) pos = lerp(0.5, 0.06, ap(t, u(32), 0.8)); if (t > u(33)) pos = lerp(0.06, 0.94, ap(t, u(33), 4, E.inOutCubic));
      const y = by + pos * bh; arrowLine(ctx, bx - 80, y, bx - 6, y, C.clayD, 10, 30);
      ctx.restore();
    }
    show_(ctx, t, u(25), u(26), () => tag(ctx, W / 2, 160, 'Schmidt-Ferguson', 'perkebunan · kehutanan', 1, C.forest));
  });
}

// ---------------------------------------------------------------- Oldeman: consecutive wet months & rice harvests
const OLD = [260, 240, 230, 210, 150, 90, 60, 50, 80, 150, 220, 250];
function sOldeman(ctx, t) {
  scene(ctx, t, 'oldeman', '#eaf3e4', () => {
    ctx.fillStyle = '#a9cf8a'; ctx.fillRect(0, 760, W, 320);
    for (let i = 0; i < 12; i++) { const v = OLD[i], x = 200 + i * 128, k = ap(t, u(34) + i * 0.1, 0.4); const wet = v > 200; const hh = v * 1.4 * k; rrect(ctx, x - 44, 700 - hh, 88, hh, 12); ctx.fillStyle = wet ? '#2b6cb0' : '#b8c7d1'; ctx.fill(); text(ctx, 'JFMAMJJASOND'[i], x, 740, fU(28, 800), C.ink, 'center'); }
    show_(ctx, t, u(35), 1e9, () => { const y = 700 - 200 * 1.4; ctx.setLineDash([14, 10]); ctx.strokeStyle = C.clayD; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(140, y); ctx.lineTo(1780, y); ctx.stroke(); ctx.setLineDash([]); text(ctx, '200 mm', 1790, y + 10, fU(26, 800), C.clayD); });
    show_(ctx, t, tw('berturut-turut', u(35)), 1e9, () => { ctx.strokeStyle = C.amber; ctx.lineWidth = 8; rrect(ctx, 1424, 200, 600, 560, 24); ctx.stroke(); rrect(ctx, 140, 200, 520, 560, 24); ctx.stroke(); });
    // rice plants growing
    const g = ap(t, u(36), 4, E.inOutCubic);
    for (let i = 0; i < 26; i++) { const x = 60 + i * 72, h = 30 + 90 * g; ctx.strokeStyle = '#3f8a52'; ctx.lineWidth = 5; for (let j = -1; j <= 1; j++) { ctx.beginPath(); ctx.moveTo(x, 1000); ctx.quadraticCurveTo(x + j * 10, 1000 - h * 0.6, x + j * 22 + Math.sin(t * 1.5 + i) * 4, 1000 - h); ctx.stroke(); } if (g > 0.7) { circle(ctx, x + 18, 1000 - h, 7); ctx.fillStyle = '#e0b462'; ctx.fill(); } }
    show_(ctx, t, u(36), 1e9, () => tag(ctx, W / 2, 160, 'makin banyak bulan basah berturut-turut, makin sering tanam padi', '', 1, C.forest));
    show_(ctx, t, u(34), u(36), () => tag(ctx, W / 2, 160, 'Oldeman', 'padi dan palawija', 1, C.forest));
  });
}
// ---------------------------------------------------------------- pairs
function sPasangan(ctx, t) {
  scene(ctx, t, 'pasangan', '#f2efe8', () => {
    ctx.fillStyle = '#e8dcc6'; ctx.fillRect(0, 820, W, 260);
    const pairs = [['ilmuwan', 'Koppen', 'iklim dunia', 460, u(38)], ['rimbawan', 'Schmidt-Ferguson', 'perkebunan · kehutanan', 960, u(39)], ['petani', 'Oldeman', 'padi', 1460, u(40)]];
    pairs.forEach(([k, n, d, x, t0]) => { person(ctx, x, 700, 1.1, k, t, 1); const kk = sp(t, t0, SPRING.bouncy); if (kk <= 0) return; ctx.save(); ctx.translate(x, 260); ctx.scale(kk, kk); pill(ctx, n, 0, 0, fU(40, 800), C.forest, C.cream, 26, 72, 'center'); text(ctx, d, 0, 70, fU(28, 800), C.clayD, 'center'); ctx.restore(); });
  });
}

run({
  DUR, no: 17, code: 'B01-17', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Klasifikasi Iklim', sub: 'Köppen, Schmidt-Ferguson, dan Oldeman',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-18 · Arus Laut dan Upwelling',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['koppen', 4], ['pohon', 12], ['schmidt', 25], ['oldeman', 34], ['pasangan', 37], ['soal', 41], ['jebakan', 46], ['ringkas', 50], ['outro', 53]],
  TERMS: [
    ['Köppen', 'Köppen climate classification', '', 4],
    ['Af · Am · Aw', 'rainforest · monsoon · savanna', '', 14],
    ['Schmidt-Ferguson', 'nilai Q', '', 29],
    ['Oldeman', 'agroclimatic zone', '', 35],
  ],
  hook: { cards: [], punch: [3, ''] },
  soal: {
    q: 'Periode 1981–2010: rata-rata 4,2 bulan kering dan 6,0 bulan basah. Periode 1991–2020: 5,4 bulan kering dan 5,1 bulan basah. Menurut Schmidt-Ferguson, perubahan tipe iklimnya adalah …',
    opts: ['tetap D', 'D (sedang) menjadi E (agak kering)', 'C menjadi D', 'E menjadi D', 'D menjadi C'], ans: 1, optFs: 28,
    ansT: () => tw('jawabannya', u(45) - 0.3),
    steps: () => [[u(42), 'Q awal = 4,2 ÷ 6,0', C.forest3, 30], [tw('tujuh', u(42)), '= 70% · tipe D', C.cream, 46], [u(43), 'Q baru = 5,4 ÷ 5,1', C.forest3, 30], [tw('seratus', u(43)), '≈ 106% · tipe E', C.cream, 46], [u(44), 'D ke E: lebih kering', C.amber, 50]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(47), 'Batas bulan basah semua sama', 'Schmidt-Ferguson 100 mm · Oldeman 200 mm', u(48)],
      [u(49), 'Q makin besar berarti makin basah', 'Q makin besar = makin KERING', tw('bukan', u(49))]],
  },
  ringkas: {
    items: () => [[tw('Koppen', u(51)), 'Köppen: suhu dan hujan, iklim dunia'], [tw('Schmidt', u(51)), 'Schmidt-Ferguson: nilai Q, kehutanan'], [tw('Oldeman', u(51)), 'Oldeman: bulan basah berturut-turut, padi']],
  },
  scenes: { hook: sHook, koppen: sKoppen, pohon: sPohon, schmidt: sSchmidt, oldeman: sOldeman, pasangan: sPasangan },
  async init() { W110 = await fetch('assets/world110.json').then((r) => r.json()); },
});
