// B01-V02 · Efek Rumah Kaca dan Pemanasan Global · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import {
  C, fD, fU, T, tw, U_, sp, ap, poly, circle, card, arrowLine, check, cross, wrap, riseText, pill, warnIcon,
  sun, cloud, rain, fish, mapProj, drawRings, cornerMark, centerMark, lowerThird, buildCaps, captions, intro, outro,
} from './lib/common.js';
const { W, H, E, prog, lerp, clamp, spring, SPRING, text, fill, rrect, bump, hash01, mix } = M;

let IND = null;
const HITS = [];
const hit = (t, label, sfx, o = {}) => HITS.push([t, label, sfx, { gain: 0.55, ...o }]);
const DUR = 632.5;

// chemical formula with subscripts: "CO2", "CH4", "N2O"
function chem(ctx, s, x, y, size, weight, color, align = 'left') {
  const parts = []; let i = 0;
  while (i < s.length) { const m = /^[A-Za-z]\d+/.exec(s.slice(i)); if (m) { parts.push([m[0][0], false]); parts.push([m[0].slice(1), true]); i += m[0].length; } else { parts.push([s[i], false]); i++; } }
  ctx.font = fU(size, weight); const sub = fU(size * 0.62, weight);
  const wOf = ([p, isSub]) => { ctx.font = isSub ? sub : fU(size, weight); return ctx.measureText(p).width; };
  const total = parts.reduce((a, p) => a + wOf(p), 0);
  let cx = align === 'center' ? x - total / 2 : align === 'right' ? x - total : x;
  for (const p of parts) { ctx.font = p[1] ? sub : fU(size, weight); ctx.fillStyle = color; ctx.textAlign = 'left'; ctx.fillText(p[0], cx, y + (p[1] ? size * 0.22 : 0)); cx += wOf(p); }
  return total;
}

// ---------------------------------------------------------------- scenes keyed to first VO unit
const SCN = [['hook', 0], ['peta', 5], ['gelombang', 9], ['albedo', 16], ['neraca', 22], ['erk', 30], ['alami', 36], ['tambahan', 39], ['keeling', 44],
  ['imbalance', 47], ['gwp', 51], ['co2e', 57], ['bukti', 61], ['umpan', 67], ['laut', 73], ['karang', 78], ['dampak', 81], ['rob', 83],
  ['mitadapt', 87], ['mangrove', 92], ['paris', 97], ['soal', 101], ['jebakan', 109], ['kamus', 115], ['outro', 135]];
const SC = {};
function buildScenes() {
  SC.intro = [0, 3.0];
  SCN.forEach(([n, u], i) => { SC[n] = [i === 0 ? 3.0 : U_(u).v0 - 0.2, i < SCN.length - 1 ? U_(SCN[i + 1][1]).v0 - 0.2 : DUR]; });
}
const exitP = (t, n, d = 0.35) => E.inCubic(prog(t, SC[n][1] - d, SC[n][1]));
const title = (ctx, t, n, s, col = C.forest) => { let fs = 76; ctx.font = fD(fs); while (ctx.measureText(s).width > 1060 && fs > 50) { fs -= 2; ctx.font = fD(fs); } riseText(ctx, s, 110, 165, fD(fs), col, ap(t, SC[n][0] + 0.1, 0.55, E.outQuint)); };
const show = (ctx, t, t0, fn, d = 0.45) => { const p = ap(t, t0, d); if (p <= 0) return; ctx.save(); ctx.globalAlpha *= p; fn(p); ctx.restore(); };

// ---------------------------------------------------------------- 18 terms
const TERMS = [
  ['Radiasi gelombang pendek', 'Pancaran matahari, puncak ±0,5 µm (cahaya tampak)', 12],
  ['Radiasi gelombang panjang', 'Pancaran bumi berupa inframerah, puncak ±10 µm', 13],
  ['Albedo', 'Persentase radiasi yang dipantulkan; rata-rata bumi ±30%', 18],
  ['Neraca energi', 'Dalam jangka panjang: energi masuk = energi keluar', 29],
  ['Gas rumah kaca', 'Gas penyerap inframerah: uap air, CO2, metana, N2O, gas-F', 30],
  ['Radiasi balik', 'Inframerah yang dipancarkan kembali ke permukaan', 33],
  ['Efek rumah kaca', 'Panas tertahan dekat permukaan; tanpa ini bumi −18 °C', 35],
  ['Efek rumah kaca tambahan', 'Penguatan efek rumah kaca akibat emisi manusia', 40],
  ['ppm', 'Bagian per sejuta; CO2 dari 280 ppm menjadi lebih dari 420 ppm', 42],
  ['Kurva Keeling', 'Grafik CO2 Mauna Loa sejak 1958: terus naik, bergelombang', 45],
  ['GWP', 'Kekuatan gas memerangkap panas dibanding CO2 (100 tahun)', 52],
  ['CO2-ekuivalen', 'Satuan emisi gabungan: massa gas × GWP', 57],
  ['Ekspansi termal', 'Air laut memuai saat memanas sehingga muka laut naik', 66],
  ['Umpan balik positif', 'Proses yang memperkuat pemanasan, mis. es–albedo', 68],
  ['Pengasaman laut', 'Laut menyerap CO2, pH turun ±0,1 sejak praindustri', 75],
  ['Pemutihan karang', 'Karang melepas alga simbion saat laut terlalu hangat', 80],
  ['Amblesan tanah', 'Permukaan tanah turun akibat penyedotan air tanah', 85],
  ['Mitigasi dan adaptasi', 'Mengurangi emisi vs menyesuaikan diri terhadap dampak', 88],
];
function termCard(ctx, t) {
  for (let i = 0; i < TERMS.length; i++) {
    const [term, def, ui] = TERMS[i];
    const t0 = U_(ui).v0, nxt = i < TERMS.length - 1 ? U_(TERMS[i + 1][2]).v0 : 1e9;
    const t1 = Math.min(t0 + 8, nxt - 0.1, SC.soal[0]);
    if (t < t0 || t > t1 + 0.4) continue;
    const p = sp(t, t0, SPRING.snappy), q = E.inCubic(prog(t, t1, t1 + 0.4));
    const x = 1212 + (1 - p) * 80 + q * 80, y = 128, w = 668, h = 120;
    ctx.save(); ctx.globalAlpha = clamp(p * 1.4) * (1 - q);
    card(ctx, x, y, w, h, { r: 24, bg: C.cream });
    rrect(ctx, x, y, 12, h, 6); ctx.fillStyle = C.clay; ctx.fill();
    text(ctx, `ISTILAH ${i + 1}/18`, x + 34, y + 34, fU(22, 700), C.clay);
    chem(ctx, term, x + 34, y + 74, term.length > 18 ? 32 : 38, 700, C.ink);
    chem(ctx, wrap(ctx, def, fU(22, 500), w - 60)[0], x + 34, y + 104, 22, 500, C.gray);
    ctx.restore();
  }
}

// ---------------------------------------------------------------- props
function earthDisc(ctx, x, y, r, t, warm = 0) {
  const g = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  g.addColorStop(0, mix('#8fc1e3', '#f1a77a', warm)); g.addColorStop(1, mix('#2f6f9e', '#b5532e', warm));
  circle(ctx, x, y, r); ctx.fillStyle = g; ctx.fill();
  ctx.save(); circle(ctx, x, y, r); ctx.clip(); ctx.fillStyle = 'rgba(120,170,90,0.85)';
  [[-0.3, -0.2, 0.35, 0.22], [0.25, 0.1, 0.3, 0.35], [-0.1, 0.45, 0.25, 0.15]].forEach(([a, b, c, d]) => { ctx.beginPath(); ctx.ellipse(x + a * r, y + b * r, c * r, d * r, 0.4, 0, Math.PI * 2); ctx.fill(); });
  ctx.restore();
}
function thermo(ctx, x, y, h, frac, color, label) {
  rrect(ctx, x - 22, y - h, 44, h, 22); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.stroke();
  circle(ctx, x, y + 18, 40); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); circle(ctx, x, y + 18, 28); ctx.fillStyle = color; ctx.fill();
  const fh = (h - 30) * clamp(frac); rrect(ctx, x - 11, y - fh - 5, 22, fh + 20, 11); ctx.fillStyle = color; ctx.fill();
  if (label) text(ctx, label, x + 60, y - h * 0.5, fU(72, 700), color);
}
function waveArrow(ctx, x1, y1, x2, y2, color, amp = 10, n = 5, w = 5) {
  const L = Math.hypot(x2 - x1, y2 - y1), a = Math.atan2(y2 - y1, x2 - x1);
  ctx.save(); ctx.translate(x1, y1); ctx.rotate(a); ctx.strokeStyle = color; ctx.lineWidth = w; ctx.beginPath();
  for (let i = 0; i <= 60; i++) { const f = i / 60; const xx = f * (L - 20), yy = Math.sin(f * n * Math.PI * 2) * amp * (f < 0.9 ? 1 : (1 - f) * 10); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }
  ctx.stroke(); ctx.fillStyle = color; poly(ctx, [[L, 0], [L - 24, -12], [L - 24, 12]]); ctx.fill(); ctx.restore();
}
function house(ctx, x, y, s, col = '#c27a4b') {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = col; ctx.fillRect(-50, -60, 100, 60); poly(ctx, [[-62, -58], [0, -110], [62, -58]]); ctx.fillStyle = '#7b3d22'; ctx.fill();
  ctx.fillStyle = '#f4e7c8'; ctx.fillRect(-35, -45, 22, 22); ctx.fillRect(12, -45, 22, 22); ctx.fillStyle = '#5a2c18'; ctx.fillRect(-10, -36, 20, 36);
  ctx.restore();
}
function mangroveTree(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = '#5a3b22'; ctx.lineWidth = 6;
  for (let k = -3; k <= 3; k++) { ctx.beginPath(); ctx.moveTo(0, -60); ctx.quadraticCurveTo(k * 18, -30, k * 26, 10); ctx.stroke(); }
  ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(0, -60); ctx.lineTo(0, -130); ctx.stroke();
  ctx.fillStyle = '#2f7d4a'; [[0, -170, 70], [-50, -140, 46], [50, -140, 46], [0, -120, 50]].forEach(([a, b, r]) => { circle(ctx, a, b, r); ctx.fill(); });
  ctx.restore();
}

// ================================================================ scenes
function sHook(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'hook'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const cards = [
    [u(0).v0 + 0.1, '2024', 'tahun terpanas sepanjang pengukuran', (x, y) => { thermo(ctx, x + 270, y + 330, 220, 0.2 + 0.75 * ap(t, u(0).v0 + 0.5, 2.5), C.clay, ''); text(ctx, '+1,5 °C', x + 330, y + 260, fU(56, 700), C.clayD); }],
    [u(1).v0, 'Timbulsloko, Demak', 'rumah berdiri di atas air laut', (x, y) => { const lv = 40 + 10 * Math.sin(t * 1.2); house(ctx, x + 270, y + 320, 1.3); ctx.fillStyle = 'rgba(58,120,200,0.75)'; ctx.fillRect(x + 20, y + 330 - lv, 500, lv + 80); }],
    [u(2).v0, 'Puncak Jaya, Papua', 'es abadi terus menyusut', (x, y) => { ctx.fillStyle = '#8a7a6a'; poly(ctx, [[x + 40, y + 410], [x + 270, y + 150], [x + 500, y + 410]]); ctx.fill(); const k = 1 - 0.7 * ap(t, u(2).v0 + 0.5, 3); ctx.fillStyle = '#ffffff'; poly(ctx, [[x + 270 - 120 * k, y + 150 + 136 * k], [x + 270, y + 150], [x + 270 + 120 * k, y + 150 + 136 * k]]); ctx.fill(); }],
  ];
  cards.forEach(([t0, a, b, draw], i) => {
    const k = sp(t, t0, SPRING.gentle); if (k <= 0) return;
    const x = 90 + i * 590, y = 200;
    ctx.save(); ctx.translate(0, (1 - k) * 80); ctx.globalAlpha *= clamp(k * 1.5);
    card(ctx, x, y, 560, 560, { r: 30 });
    ctx.save(); rrect(ctx, x + 20, y + 20, 520, 420, 22); ctx.clip(); ctx.fillStyle = i === 1 ? '#dbe8ef' : '#f1e6d6'; ctx.fillRect(x, y, 560, 460); draw(x, y); ctx.restore();
    text(ctx, a, x + 30, y + 495, fU(38, 700), C.ink); text(ctx, b, x + 30, y + 535, fU(26, 500), C.gray);
    ctx.restore();
  });
  const pt = sp(t, u(4).v0 - 0.1, SPRING.bouncy);
  if (pt > 0) { ctx.save(); ctx.translate(W / 2, 470); ctx.scale(pt, pt); card(ctx, -420, -90, 840, 170, { r: 40, bg: C.forest }); text(ctx, 'efek rumah kaca', 0, 30, fD(104), C.cream, 'center'); ctx.restore(); }
  ctx.restore();
}

function sPeta(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'peta'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'peta', 'Peta video ini');
  const steps = [['Energi bumi', 'bagaimana', C.amber], ['Gas penyerap panas', 'kenapa', C.clay], ['Menghitung GWP', 'menghitung', C.forestL], ['Bukti', 'buktinya', C.blue], ['Dampak Indonesia', 'dampaknya', C.clayD], ['Solusi', 'dilakukan', C.forest]];
  steps.forEach(([s, w, col], i) => {
    const t0 = tw(w, u(6).v0); const k = sp(t, t0 - 0.1, SPRING.bouncy); if (k <= 0) return;
    const x = 110 + i * 285, y = 280;
    ctx.save(); ctx.translate(x + 125, y + 110); ctx.scale(k, k); ctx.translate(-(x + 125), -(y + 110));
    card(ctx, x, y, 255, 220, { r: 24 }); rrect(ctx, x, y, 255, 18, 9); ctx.fillStyle = col; ctx.fill();
    text(ctx, `${i + 1}`, x + 127, y + 110, fU(70, 700), col, 'center');
    wrap(ctx, s, fU(28, 700), 220).forEach((l, j) => text(ctx, l, x + 127, y + 160 + j * 32, fU(28, 700), C.ink, 'center'));
    ctx.restore();
    if (i < 5) { const pa = ap(t, tw(steps[i + 1][1], u(6).v0) - 0.15, 0.3); if (pa > 0) arrowLine(ctx, x + 258, y + 110, x + 258 + 24 * pa, y + 110, C.clay, 4, 12); }
  });
  const pc = ap(t, tw('delapan', u(7).v0), 1.3);
  if (pc > 0) { ctx.save(); ctx.globalAlpha *= clamp(pc * 3); card(ctx, 110, 600, 1700, 200, { r: 30, bg: C.forest }); text(ctx, `${Math.round(18 * pc)}`, 300, 760, fU(150, 700), C.amber, 'center'); text(ctx, 'istilah penting akan muncul di layar', 440, 700, fU(46, 700), C.cream); text(ctx, 'Catat semuanya, istilah inilah yang sering dipakai soal OSN.', 440, 760, fU(30, 500), C.forest3); ctx.restore(); }
  ctx.restore();
}

function planck(lam, T) { return Math.pow(lam, -5) / (Math.exp(14388 / (lam * T)) - 1); }
function sGelombang(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'gelombang'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'gelombang', 'Gelombang pendek masuk, gelombang panjang keluar');
  const sw = ap(t, u(15).v0 - 0.4, 0.6, E.inOutCubic);
  if (sw < 1) {
    ctx.save(); ctx.globalAlpha *= 1 - sw;
    const box = { x: 110, y: 240, w: 1700, h: 600 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
    const gx = box.x + 110, gy = box.y + box.h - 90, gw = box.w - 180, gh = box.h - 170;
    const X = (lam) => gx + (Math.log10(lam) + 1) / 3 * gw; // 0.1 .. 100 µm
    ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
    [0.1, 0.5, 1, 4, 10, 50, 100].forEach((v) => { text(ctx, `${v}`.replace('.', ','), X(v), gy + 36, fU(24, 600), C.gray, 'center'); });
    text(ctx, 'panjang gelombang (µm, skala log)', gx + gw, gy + 72, fU(24, 600), C.gray, 'right');
    text(ctx, 'intensitas (dinormalkan)', gx - 10, gy - gh - 18, fU(22, 600), C.gray);
    const curve = (T, col, p, maxL) => {
      let mx = 0; for (let i = 0; i <= 300; i++) { const lam = Math.pow(10, -1 + 3 * i / 300); mx = Math.max(mx, planck(lam, T)); }
      ctx.save(); ctx.beginPath(); ctx.moveTo(gx, gy);
      for (let i = 0; i <= 300 * p; i++) { const lam = Math.pow(10, -1 + 3 * i / 300); ctx.lineTo(X(lam), gy - planck(lam, T) / mx * gh * 0.92); }
      ctx.lineTo(X(Math.pow(10, -1 + 3 * p)), gy); ctx.closePath(); ctx.fillStyle = col.replace('1)', '0.25)'); ctx.fill();
      ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.stroke(); ctx.restore();
    };
    const ps = ap(t, tw('matahari', u(12).v0), 1.6, E.linear), pe = ap(t, tw('bumi', u(13).v0), 1.6, E.linear);
    if (ps > 0) { curve(5800, 'rgba(242,177,58,1)', ps, 0); if (ps > 0.6) { pill(ctx, 'Matahari ±5.800 K', X(0.5), gy - gh - 10 + 40, fU(26, 700), C.amber, C.ink, 18, 46, 'center'); text(ctx, 'gelombang PENDEK', X(0.5), gy - gh * 0.45, fU(30, 700), '#a56d06', 'center'); } }
    if (pe > 0) { curve(288, 'rgba(224,121,79,1)', pe, 0); if (pe > 0.6) { pill(ctx, 'Bumi ±288 K', X(10), gy - gh - 10 + 40, fU(26, 700), C.clay, C.cream, 18, 46, 'center'); text(ctx, 'gelombang PANJANG (inframerah)', X(10), gy - gh * 0.45, fU(30, 700), C.clayD, 'center'); } }
    if (ap(t, u(11).v0, 0.4) > 0) { ctx.save(); ctx.globalAlpha *= ap(t, u(11).v0, 0.4); ctx.setLineDash([8, 8]); ctx.strokeStyle = C.forest; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(X(4), gy - gh); ctx.lineTo(X(4), gy); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'batas ±4 µm', X(4) + 10, gy - gh + 30, fU(22, 700), C.forest); ctx.restore(); }
    ctx.restore();
  }
  if (sw > 0) {
    ctx.save(); ctx.globalAlpha *= sw;
    sun(ctx, 300, 520, 110, t); earthDisc(ctx, 1450, 560, 230, t);
    for (let k = 0; k < 3; k++) arrowLine(ctx, 460, 440 + k * 70, 1180, 470 + k * 60, C.amber, 9, 30);
    for (let k = 0; k < 3; k++) waveArrow(ctx, 1260, 420 + k * 90, 900, 260 + k * 60, C.clay, 10, 6, 5);
    pill(ctx, 'masuk: gelombang pendek', 520, 380, fU(30, 700), C.amber, C.ink, 22, 56);
    pill(ctx, 'keluar: gelombang panjang', 760, 230, fU(30, 700), C.clay, C.cream, 22, 56);
    ctx.restore();
  }
  ctx.restore();
}

const ALB = [['Salju segar', 85, 'salju'], ['Awan tebal', 75, 'salju'], ['Pasir gurun', 35, 'salju'], ['Sawah, rumput', 20, 'hutan'], ['Hutan hujan', 12, 'hutan'], ['Laut, aspal', 7, 'hutan']];
function sAlbedo(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'albedo'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'albedo', 'Albedo: berapa persen yang dipantulkan?');
  const pf = ap(t, u(18).v0, 0.5);
  if (pf > 0) { ctx.save(); ctx.globalAlpha *= pf; card(ctx, 1260, 290, 560, 230, { r: 26, bg: C.forest }); text(ctx, 'albedo =', 1300, 360, fU(34, 700), C.forest3); text(ctx, 'dipantulkan', 1300, 420, fU(40, 700), C.cream); rrect(ctx, 1300, 438, 280, 4, 2); ctx.fillStyle = C.amber; ctx.fill(); text(ctx, 'diterima', 1300, 490, fU(40, 700), C.cream); ctx.restore(); }
  ALB.forEach(([n, v, w], i) => {
    const t0 = i < 3 ? u(19).v0 + i * 0.5 : u(20).v0 + (i - 3) * 0.5;
    const p = ap(t, t0, 0.8, E.outCubic); if (p <= 0) return;
    const y = 290 + i * 92;
    text(ctx, n, 110, y + 46, fU(32, 700), C.ink);
    rrect(ctx, 420, y + 10, 720, 52, 14); ctx.fillStyle = '#ece3d3'; ctx.fill();
    rrect(ctx, 420, y + 10, 7.2 * v * p, 52, 14); ctx.fillStyle = i < 3 ? '#9fc4dd' : '#3b6e4d'; ctx.fill();
    text(ctx, `${Math.round(v * p)}%`, 430 + 7.2 * v * p + 12, y + 48, fU(30, 700), C.ink);
  });
  const pb = ap(t, u(21).v0, 0.6);
  if (pb > 0) {
    ctx.save(); ctx.globalAlpha *= pb; const x = 420 + 7.2 * 30;
    ctx.setLineDash([10, 8]); ctx.strokeStyle = C.clay; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x, 280); ctx.lineTo(x, 850); ctx.stroke(); ctx.setLineDash([]);
    pill(ctx, 'rata-rata bumi ±30%', x, 870, fU(28, 700), C.clay, C.cream, 18, 50, 'center');
    show(ctx, t, tw('awan', u(21).v0), () => pill(ctx, 'penyumbang terbesar: AWAN', 1540, 600, fU(28, 700), C.blue, C.cream, 20, 54, 'center'));
    ctx.restore();
  }
  ctx.restore();
}

function sNeraca(ctx, t) {
  fill(ctx, '#eef3f6'); const ex = exitP(t, 'neraca'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'neraca', 'Neraca energi bumi (dari 100 satuan)');
  // layers
  ctx.fillStyle = 'rgba(160,190,215,0.35)'; ctx.fillRect(110, 360, 1700, 260); text(ctx, 'ATMOSFER', 130, 395, fU(24, 700), C.blue);
  ctx.fillStyle = '#b9a27a'; ctx.fillRect(110, 620, 1700, 220); text(ctx, 'PERMUKAAN BUMI', 130, 660, fU(24, 700), '#5a4326');
  ctx.fillStyle = '#1b2a3a'; ctx.fillRect(110, 240, 1700, 120); text(ctx, 'ANGKASA', 130, 275, fU(24, 700), '#c9d6e3');
  const n = (v, x, y, col) => { circle(ctx, x, y, 46); ctx.fillStyle = col; ctx.fill(); text(ctx, `${v}`, x, y + 16, fU(44, 700), '#fff', 'center'); };
  const pIn = ap(t, u(23).v0, 0.8);
  if (pIn > 0) { arrowLine(ctx, 400, 250, 400, lerp(250, 600, pIn), C.amber, 14, 36); n(100, 400, 300, C.amber); }
  show(ctx, t, u(24).v0, (p) => { arrowLine(ctx, 430, 470, 600, lerp(470, 280, p), '#9fc4dd', 10, 30); n(30, 640, 300, '#6c9ec0'); text(ctx, 'dipantulkan', 700, 310, fU(28, 700), '#c9d6e3'); });
  show(ctx, t, u(25).v0, () => { n(20, 760, 480, '#5a8db1'); text(ctx, 'diserap atmosfer dan awan', 820, 490, fU(28, 700), C.blue); cloud(ctx, 1000, 420, 0.7); });
  show(ctx, t, u(26).v0, () => { n(50, 400, 720, C.clay); text(ctx, 'diserap permukaan', 460, 730, fU(30, 700), '#fff'); });
  show(ctx, t, u(27).v0, () => {
    const items = [['radiasi inframerah', tw('radiasi', u(27).v0), C.clay], ['udara hangat naik', tw('udara', u(27).v0), C.clayD], ['penguapan air', tw('penguapan', u(27).v0), C.blue]];
    items.forEach(([s, t0, col], i) => { const p = ap(t, t0, 0.5); if (p <= 0) return; ctx.save(); ctx.globalAlpha *= p; const x = 1080 + i * 260; if (i === 0) waveArrow(ctx, x, 700, x, lerp(700, 420, p), col, 8, 4, 5); else arrowLine(ctx, x, 700, x, lerp(700, 420, p), col, 8, 26); text(ctx, s, x, 800, fU(22, 700), '#fff', 'center'); ctx.restore(); });
  });
  show(ctx, t, u(28).v0, () => { card(ctx, 1240, 250, 560, 90, { r: 22, bg: C.cream }); text(ctx, 'energi MASUK = energi KELUAR', 1520, 308, fU(30, 700), C.forest, 'center'); });
  ctx.restore();
}

function molecule(ctx, x, y, kind, s = 1) {
  const cols = { CO2: ['#4a4a4a', '#d9534f'], CH4: ['#4a4a4a', '#ffffff'], H2O: ['#d9534f', '#ffffff'] }[kind];
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  if (kind === 'CO2') { [[-26, 0], [26, 0]].forEach(([a]) => { circle(ctx, a, 0, 13); ctx.fillStyle = cols[1]; ctx.fill(); }); circle(ctx, 0, 0, 16); ctx.fillStyle = cols[0]; ctx.fill(); }
  else if (kind === 'CH4') { [[-20, -16], [20, -16], [-20, 16], [20, 16]].forEach(([a, b]) => { circle(ctx, a, b, 9); ctx.fillStyle = cols[1]; ctx.strokeStyle = '#999'; ctx.lineWidth = 2; ctx.fill(); ctx.stroke(); }); circle(ctx, 0, 0, 15); ctx.fillStyle = cols[0]; ctx.fill(); }
  else { [[-18, 14], [18, 14]].forEach(([a, b]) => { circle(ctx, a, b, 9); ctx.fillStyle = cols[1]; ctx.strokeStyle = '#999'; ctx.lineWidth = 2; ctx.fill(); ctx.stroke(); }); circle(ctx, 0, 0, 16); ctx.fillStyle = cols[0]; ctx.fill(); }
  ctx.restore();
}
function sErk(ctx, t) {
  fill(ctx, '#eef3f6'); const ex = exitP(t, 'erk'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'erk', 'Bagaimana gas rumah kaca menahan panas?');
  ctx.fillStyle = 'rgba(160,190,215,0.35)'; ctx.fillRect(110, 280, 1700, 340);
  const glow = ap(t, u(34).v0, 1.0);
  ctx.fillStyle = mix('#b9a27a', '#d9824f', glow * 0.6); ctx.fillRect(110, 620, 1700, 220);
  const mols = [['CO2', 400, 420], ['CH4', 700, 360], ['H2O', 1000, 450], ['CO2', 1300, 380], ['H2O', 1560, 470], ['CO2', 560, 530], ['CH4', 1180, 540]];
  const pm = ap(t, tw('uap', u(31).v0), 0.8);
  mols.forEach(([k, x, y], i) => { if (pm > 0) { ctx.save(); ctx.globalAlpha *= clamp(pm * 7 - i); molecule(ctx, x + Math.sin(t * 1.5 + i) * 8, y + Math.cos(t * 1.2 + i) * 6, k, 1.3); ctx.restore(); } });
  if (pm > 0) { ctx.save(); ctx.globalAlpha *= pm; chem(ctx, 'uap air · CO2 · CH4', 130, 320, 28, 700, C.blue); ctx.restore(); }
  // sunlight passes
  const ps = ap(t, tw('menghalangi', u(31).v0) - 0.6, 0.8);
  if (ps > 0) for (let k = 0; k < 3; k++) arrowLine(ctx, 250 + k * 140, 250, 250 + k * 140 + 80, lerp(250, 640, ps), C.amber, 8, 26);
  // IR up absorbed, re-emitted
  const pi = ap(t, tw('menyerap', u(32).v0), 1.0);
  if (pi > 0) {
    [[820, 700, 1000, 470], [1120, 700, 1300, 400], [1440, 700, 1560, 490]].forEach(([x1, y1, x2, y2]) => waveArrow(ctx, x1, y1, lerp(x1, x2, pi), lerp(y1, y2, pi), C.clay, 8, 4, 5));
  }
  const pr = ap(t, tw('memancarkannya', u(32).v0), 0.8);
  if (pr > 0) [[1000, 450], [1300, 380], [1560, 470]].forEach(([x, y], j) => { ctx.save(); ctx.globalAlpha *= pr; [[0, -1], [0.9, -0.4], [-0.9, -0.4], [0.5, 0.9], [-0.5, 0.9]].forEach(([dx, dy]) => waveArrow(ctx, x + dx * 40, y + dy * 40, x + dx * 130, y + dy * 130, dy > 0 ? C.clayD : 'rgba(224,121,79,0.5)', 5, 3, 4)); ctx.restore(); });
  show(ctx, t, tw('balik', u(33).v0) - 0.3, () => pill(ctx, 'radiasi balik ke permukaan', 1360, 690, fU(30, 700), C.clayD, C.cream, 22, 56, 'center'));
  show(ctx, t, u(35).v0, () => pill(ctx, 'EFEK RUMAH KACA', W / 2, 800, fU(42, 700), C.forest, C.cream, 30, 72, 'center'));
  ctx.restore();
}

function sAlami(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'alami'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'alami', 'Efek rumah kaca alami itu BAIK');
  const p1 = ap(t, u(37).v0, 1.2), p2 = ap(t, u(38).v0, 1.2);
  if (p1 > 0) { ctx.save(); ctx.globalAlpha *= clamp(p1 * 2); card(ctx, 160, 260, 760, 560, { r: 30, bg: '#dfeaf4' }); earthDisc(ctx, 360, 520, 150, t); ctx.fillStyle = 'rgba(255,255,255,0.65)'; circle(ctx, 360, 520, 150); ctx.fill(); thermo(ctx, 620, 660, 300, 0.15 * p1, C.cold, ''); text(ctx, '−18 °C', 690, 520, fU(72, 700), C.blue); text(ctx, 'tanpa efek rumah kaca', 200, 780, fU(32, 700), C.ink); ctx.restore(); }
  if (p2 > 0) { ctx.save(); ctx.globalAlpha *= clamp(p2 * 2); card(ctx, 1000, 260, 760, 560, { r: 30, bg: '#e6f1e6' }); earthDisc(ctx, 1200, 520, 150, t); thermo(ctx, 1460, 660, 300, 0.55 * p2, C.forestL, ''); text(ctx, '+15 °C', 1530, 520, fU(72, 700), C.forest); text(ctx, 'dengan efek rumah kaca: layak huni', 1040, 780, fU(32, 700), C.ink); ctx.restore(); }
  ctx.restore();
}

function sTambahan(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'tambahan'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'tambahan', 'Masalahnya: efek rumah kaca TAMBAHAN', C.clayD);
  // factories
  const pf = ap(t, u(39).v0 + 0.5, 0.6);
  if (pf > 0) { ctx.save(); ctx.globalAlpha *= pf; for (let k = 0; k < 3; k++) { const x = 160 + k * 200; ctx.fillStyle = '#6b6b6b'; ctx.fillRect(x, 620, 140, 200); ctx.fillRect(x + 90, 480, 30, 140); for (let j = 0; j < 4; j++) { const ph = (t * 30 + j * 25 + k * 10) % 100; ctx.fillStyle = `rgba(110,110,110,${0.5 - ph / 220})`; circle(ctx, x + 105 + ph * 0.4, 460 - ph * 1.6, 18 + ph * 0.3); ctx.fill(); } } ctx.restore(); }
  const pc = ap(t, tw('dua', u(41).v0), 4.5, E.inOutCubic);
  if (pc > 0) {
    ctx.save(); ctx.globalAlpha *= clamp(pc * 4);
    card(ctx, 900, 270, 900, 420, { r: 30, bg: C.forest });
    chem(ctx, 'Konsentrasi CO2 di atmosfer', 950, 340, 34, 700, C.forest3);
    text(ctx, `${Math.round(280 + 140 * pc)}`, 1250, 540, fU(200, 700), C.amber, 'center');
    text(ctx, 'ppm', 1500, 540, fU(80, 700), C.cream);
    text(ctx, pc < 0.98 ? 'praindustri: 280 ppm' : 'kini: lebih dari 420 ppm', 950, 640, fU(32, 700), C.cream);
    ctx.restore();
  }
  show(ctx, t, u(42).v0, () => pill(ctx, 'ppm = bagian per sejuta', 900, 740, fU(30, 700), C.clay, C.cream, 22, 56));
  show(ctx, t, u(43).v0, () => pill(ctx, 'tertinggi dalam 800.000 tahun (data inti es)', 900, 820, fU(30, 700), C.forestL, C.cream, 22, 56));
  ctx.restore();
}

function sKeeling(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'keeling'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'keeling', 'Kurva Keeling (Mauna Loa, Hawaii)');
  const box = { x: 110, y: 240, w: 1700, h: 600 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
  const gx = box.x + 110, gy = box.y + box.h - 80, gw = box.w - 160, gh = box.h - 150;
  const Y = (v) => gy - (v - 300) / 140 * gh, X = (yr) => gx + (yr - 1958) / 66 * gw;
  ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
  [320, 360, 400, 440].forEach((v) => { text(ctx, `${v}`, gx - 14, Y(v) + 8, fU(22, 600), C.gray, 'right'); ctx.strokeStyle = '#eee5d6'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(gx, Y(v)); ctx.lineTo(gx + gw, Y(v)); ctx.stroke(); });
  [1960, 1980, 2000, 2020].forEach((yr) => text(ctx, `${yr}`, X(yr), gy + 36, fU(22, 600), C.gray, 'center'));
  chem(ctx, 'CO2 (ppm)', gx - 10, gy - gh - 18, 22, 700, C.gray);
  const p = ap(t, u(44).v0 + 0.5, 6, E.linear);
  ctx.strokeStyle = C.clay; ctx.lineWidth = 3; ctx.beginPath();
  for (let i = 0; i <= 66 * 24 * p; i++) { const yr = 1958 + i / 24; const d = yr - 1958; const v = 315 + 0.8 * d + 0.0129 * d * d + 3 * Math.sin((yr % 1) * Math.PI * 2); i ? ctx.lineTo(X(yr), Y(v)) : ctx.moveTo(X(yr), Y(v)); }
  ctx.stroke();
  show(ctx, t, tw('gelombang', u(46).v0), () => { ctx.save(); ctx.beginPath(); ctx.rect(1300, 300, 480, 260); ctx.clip(); ctx.restore(); card(ctx, 1290, 520, 500, 120, { r: 22, bg: C.forest }); text(ctx, 'gelombang tahunan: fotosintesis', 1540, 570, fU(24, 700), C.cream, 'center'); text(ctx, 'musim panas belahan bumi utara', 1540, 608, fU(24, 600), C.forest3, 'center'); });
  text(ctx, 'disederhanakan dari data tahunan NOAA', box.x + box.w - 30, box.y + 40, fU(18, 500), C.gray, 'right');
  ctx.restore();
}

function sImbalance(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'imbalance'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'imbalance', 'Energi masuk lebih besar dari energi keluar');
  const tilt = -0.14 * ap(t, u(48).v0, 1.5, E.outCubic) * (1 - 0.6 * ap(t, u(49).v0 + 1, 2));
  ctx.save(); ctx.translate(700, 560);
  ctx.fillStyle = C.forest; poly(ctx, [[-30, 260], [30, 260], [0, 0]]); ctx.fill();
  ctx.rotate(tilt); ctx.fillStyle = C.ink; ctx.fillRect(-420, -10, 840, 20);
  [[-380, 'MASUK', C.amber], [380, 'KELUAR', C.clay]].forEach(([x, s, col]) => { ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x, 10); ctx.lineTo(x, 110); ctx.stroke(); rrect(ctx, x - 120, 110, 240, 90, 20); ctx.fillStyle = col; ctx.fill(); text(ctx, s, x, 170, fU(34, 700), '#fff', 'center'); });
  ctx.restore();
  show(ctx, t, u(49).v0, () => { card(ctx, 1220, 300, 600, 160, { r: 26 }); text(ctx, 'Bumi memanas sampai', 1260, 370, fU(32, 700), C.ink); text(ctx, 'keseimbangan baru tercapai', 1260, 420, fU(32, 700), C.ink); });
  show(ctx, t, u(50).v0, () => { card(ctx, 1220, 500, 600, 260, { r: 26, bg: '#2f6f9e' }); text(ctx, 'lebih dari', 1260, 570, fU(30, 700), '#dcecf7'); text(ctx, '90%', 1260, 680, fU(110, 700), C.cream); text(ctx, 'panas tambahan', 1500, 640, fU(28, 700), '#dcecf7'); text(ctx, 'tersimpan di LAUT', 1500, 680, fU(28, 700), '#dcecf7'); });
  ctx.restore();
}

function sGwp(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'gwp'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'gwp', 'GWP: tidak semua gas sama kuat');
  const rows = [['CO2', 'karbon dioksida', 1, u(53).v0, C.gray], ['CH4', 'metana (sawah, ternak, TPA)', 28, u(54).v0, C.clay], ['N2O', 'dinitrogen oksida (pupuk)', 265, u(55).v0, C.clayD], ['gas-F', 'HFC, SF6 (pendingin)', 1500, u(56).v0, C.forest]];
  rows.forEach(([g, d, v, t0, col], i) => {
    const p = ap(t, t0, 1.0); if (p <= 0) return;
    const y = 290 + i * 135;
    ctx.save(); ctx.globalAlpha *= clamp(p * 2);
    chem(ctx, g, 110, y + 60, 56, 700, col); text(ctx, d, 110, y + 100, fU(24, 500), C.gray);
    const len = Math.min(1100, 40 + Math.sqrt(v) * 30) * p;
    rrect(ctx, 600, y + 20, len, 66, 16); ctx.fillStyle = col; ctx.fill();
    text(ctx, v >= 1000 ? 'ribuan ×' : `${v} ×`, 600 + len + 16, y + 68, fU(40, 700), col);
    ctx.restore();
  });
  show(ctx, t, u(52).v0 + 2, () => pill(ctx, 'GWP = Global Warming Potential (relatif terhadap CO2, 100 tahun)', 110, 860, fU(26, 700), C.forest, C.cream, 22, 52));
  text(ctx, 'panjang batang tidak proporsional', 1810, 900, fU(18, 500), C.gray, 'right');
  ctx.restore();
}

function sCo2e(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'co2e'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'co2e', 'Satuan bersama: CO2-ekuivalen');
  const pb = sp(t, u(58).v0, SPRING.snappy);
  if (pb > 0) { ctx.save(); ctx.globalAlpha *= clamp(pb * 1.4); card(ctx, 260, 280, 1400, 220, { r: 32, bg: C.forest }); chem(ctx, 'CO2-e = massa gas × GWP', W / 2, 420, 84, 700, C.amber, 'center'); ctx.restore(); }
  const pe = ap(t, u(60).v0, 0.5);
  if (pe > 0) {
    ctx.save(); ctx.globalAlpha *= pe; card(ctx, 260, 560, 1400, 260, { r: 30 });
    text(ctx, 'Contoh', 300, 620, fU(28, 700), C.clay);
    const steps = [[u(60).v0 + 0.4, '100 ton metana'], [tw('setara', u(60).v0), '× 28'], [tw('ribu', u(60).v0), '= 2.800 ton CO2-e']];
    let x = 300; steps.forEach(([t0, s], i) => { const p = ap(t, t0, 0.4); if (p > 0) { ctx.save(); ctx.globalAlpha *= p; x += chem(ctx, s, x, 740, 62, 700, i === 2 ? C.clayD : C.ink) + 30; ctx.restore(); } else { ctx.font = fU(62, 700); x += ctx.measureText(s).width + 30; } });
    ctx.restore();
  }
  ctx.restore();
}

function sBukti(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'bukti'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'bukti', 'Bukti bumi memanas');
  // temperature anomaly chart
  const box = { x: 110, y: 240, w: 1000, h: 600 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
  const gx = box.x + 90, gy = box.y + box.h - 80, gw = box.w - 130, gh = box.h - 160;
  const X = (yr) => gx + (yr - 1850) / 175 * gw, Y = (v) => gy - (v + 0.3) / 1.9 * gh;
  ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
  [0, 0.5, 1.0, 1.5].forEach((v) => text(ctx, `+${v}`.replace('.', ',').replace('+0', '0'), gx - 12, Y(v) + 8, fU(22, 600), C.gray, 'right'));
  [1850, 1900, 1950, 2000, 2024].forEach((yr) => text(ctx, `${yr}`, X(yr), gy + 36, fU(22, 600), C.gray, 'center'));
  text(ctx, 'anomali suhu global (°C, terhadap 1850–1900)', gx - 10, gy - gh - 16, fU(22, 700), C.gray);
  const anom = (yr) => (yr < 1910 ? -0.05 + 0.05 * Math.sin(yr) : yr < 1970 ? -0.05 + (yr - 1910) * 0.005 : 0.25 + (yr - 1970) * 0.019 + (yr > 2020 ? (yr - 2020) * 0.05 : 0)) + 0.07 * (hash01(yr, 9) - 0.5);
  const p = ap(t, u(62).v0, 4, E.linear);
  ctx.strokeStyle = C.clay; ctx.lineWidth = 5; ctx.beginPath(); for (let yr = 1850; yr <= 1850 + 174 * p; yr++) { const v = anom(yr); yr === 1850 ? ctx.moveTo(X(yr), Y(v)) : ctx.lineTo(X(yr), Y(v)); } ctx.stroke();
  show(ctx, t, tw('satu', u(62).v0), () => pill(ctx, '2011–2020: +1,1 °C (IPCC)', X(1960), Y(1.25), fU(26, 700), C.clayD, C.cream, 18, 48, 'center'));
  text(ctx, 'disederhanakan', box.x + box.w - 30, box.y + 36, fU(18, 500), C.gray, 'right');
  // sea level + thermal expansion
  show(ctx, t, u(63).v0, () => { card(ctx, 1160, 240, 650, 260, { r: 26, bg: '#2f6f9e' }); text(ctx, 'muka laut naik', 1200, 300, fU(30, 700), '#dcecf7'); text(ctx, '±20 cm', 1200, 400, fU(90, 700), C.cream); text(ctx, 'sejak 1901, makin cepat', 1200, 460, fU(26, 600), '#dcecf7'); });
  show(ctx, t, u(64).v0, () => {
    card(ctx, 1160, 540, 650, 300, { r: 26 });
    const heat = ap(t, tw('memuai', u(65).v0), 1.5);
    // glass
    ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(1230, 600); ctx.lineTo(1250, 800); ctx.lineTo(1370, 800); ctx.lineTo(1390, 600); ctx.stroke();
    const lv = 130 + 40 * heat; ctx.fillStyle = mix('#7fb7d6', '#e07a4f', heat); poly(ctx, [[1250 - 0, 800], [1370, 800], [1370 + 16 * lv / 200, 800 - lv], [1250 - 16 * lv / 200, 800 - lv]]); ctx.fill();
    text(ctx, 'es mencair', 1430, 640, fU(28, 700), C.blue); text(ctx, '+ air memuai', 1430, 690, fU(28, 700), C.clayD);
    show(ctx, t, tw('ekspansi', u(66).v0), () => pill(ctx, 'EKSPANSI TERMAL', 1430, 760, fU(26, 700), C.clay, C.cream, 18, 48));
  });
  ctx.restore();
}

function sUmpan(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'umpan'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'umpan', 'Umpan balik positif: pemanasan memperkuat dirinya');
  const cx = 640, cy = 560, R = 300;
  const nodes = [['Es mencair', tw('es', u(70).v0)], ['Laut gelap terbuka', tw('permukaan', u(70).v0)], ['Albedo turun', tw('albedo', u(70).v0)], ['Lebih banyak panas diserap', tw('panas', u(70).v0)]];
  const pl = ap(t, u(69).v0, 0.6);
  if (pl > 0) {
    ctx.save(); ctx.globalAlpha *= pl; ctx.strokeStyle = C.clay; ctx.lineWidth = 8; ctx.setLineDash([22, 14]); ctx.lineDashOffset = -t * 60;
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]);
    text(ctx, 'es–albedo', cx, cy + 12, fD(46), C.clayD, 'center'); ctx.restore();
  }
  nodes.forEach(([s, t0], i) => {
    const k = sp(t, t0, SPRING.bouncy); if (k <= 0) return;
    const a = -Math.PI / 2 + i * Math.PI / 2, x = cx + Math.cos(a) * R, y = cy + Math.sin(a) * R;
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
    ctx.font = fU(28, 700); const w = Math.max(220, ctx.measureText(s).width + 40);
    card(ctx, -w / 2, -40, w, 80, { r: 20, bg: i === 0 ? '#ffffff' : C.cream }); text(ctx, s, 0, 10, fU(28, 700), C.ink, 'center');
    ctx.restore();
  });
  show(ctx, t, u(71).v0, () => { card(ctx, 1150, 300, 660, 200, { r: 26 }); text(ctx, 'Uap air', 1190, 370, fU(38, 700), C.blue); text(ctx, 'udara hangat menampung lebih banyak', 1190, 420, fU(26, 600), C.ink); text(ctx, 'uap air (juga gas rumah kaca)', 1190, 460, fU(26, 600), C.ink); });
  show(ctx, t, u(72).v0, () => { card(ctx, 1150, 540, 660, 200, { r: 26 }); text(ctx, 'Permafrost', 1190, 610, fU(38, 700), C.clayD); text(ctx, 'tanah beku Siberia mencair,', 1190, 660, fU(26, 600), C.ink); text(ctx, 'melepaskan metana', 1190, 700, fU(26, 600), C.ink); });
  ctx.restore();
}

function coral(ctx, x, y, s, bleach) {
  const col = mix('#e8735a', '#f6f1ea', bleach), col2 = mix('#c94f86', '#efe9df', bleach);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.lineCap = 'round';
  const br = (x0, y0, a, len, d, c) => { if (d === 0) return; const x1 = x0 + Math.cos(a) * len, y1 = y0 + Math.sin(a) * len; ctx.strokeStyle = c; ctx.lineWidth = d * 6; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke(); br(x1, y1, a - 0.45, len * 0.75, d - 1, c); br(x1, y1, a + 0.4, len * 0.72, d - 1, c); };
  br(0, 0, -Math.PI / 2, 80, 5, col); br(-90, 0, -Math.PI / 2 - 0.3, 60, 4, col2); br(100, 0, -Math.PI / 2 + 0.3, 66, 4, col2);
  ctx.restore();
}
function sLaut(ctx, t) {
  fill(ctx, '#e6f0f5'); const ex = exitP(t, 'laut'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'laut', 'Laut makin asam', C.blue);
  ctx.fillStyle = '#3a7fb0'; ctx.fillRect(110, 420, 1100, 420); ctx.fillStyle = '#cfe3ef'; ctx.fillRect(110, 260, 1100, 160);
  const pa = ap(t, u(74).v0, 1.2);
  if (pa > 0) for (let k = 0; k < 5; k++) { const ph = ((t * 0.6 + k * 0.2) % 1); ctx.save(); ctx.globalAlpha *= pa * (1 - ph); chem(ctx, 'CO2', 200 + k * 210, 300 + ph * 220, 34, 700, C.ink); ctx.restore(); }
  show(ctx, t, u(75).v0, () => pill(ctx, 'PENGASAMAN LAUT', 660, 500, fU(34, 700), C.cream, C.blue, 24, 60, 'center'));
  show(ctx, t, u(76).v0, () => { card(ctx, 1260, 260, 560, 330, { r: 28, bg: C.forest }); text(ctx, 'pH laut', 1300, 330, fU(34, 700), C.forest3); const v = 8.2 - 0.1 * ap(t, u(76).v0 + 0.5, 2); text(ctx, v.toFixed(2).replace('.', ','), 1300, 470, fU(130, 700), C.amber); text(ctx, 'turun ±0,1 sejak praindustri', 1300, 540, fU(26, 700), C.cream); });
  show(ctx, t, u(77).v0, () => { const d = ap(t, u(77).v0 + 0.5, 3); ctx.save(); ctx.translate(660, 700); ctx.fillStyle = '#f2e6d0'; ctx.globalAlpha *= 1 - 0.6 * d; ctx.beginPath(); for (let k = 0; k < 7; k++) { ctx.moveTo(0, 0); ctx.arc(0, 0, 90, Math.PI + k * Math.PI / 7, Math.PI + (k + 0.85) * Math.PI / 7); } ctx.fill(); ctx.restore(); text(ctx, 'cangkang sulit terbentuk', 660, 800, fU(28, 700), '#ffffff', 'center'); });
  ctx.restore();
}
function sKarang(ctx, t) {
  fill(ctx, '#e6f0f5'); const ex = exitP(t, 'karang'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'karang', 'Pemutihan karang (coral bleaching)', C.blue);
  ctx.fillStyle = '#5aa0c8'; ctx.fillRect(110, 260, 1100, 580); ctx.fillStyle = '#d8c89a'; ctx.fillRect(110, 760, 1100, 80);
  const b = ap(t, tw('mengeluarkan', u(78).v0), 6, E.inOutCubic);
  [[300, 770, 1.1], [560, 770, 1.4], [850, 770, 1.2], [1080, 770, 0.9]].forEach(([x, y, s]) => coral(ctx, x, y, s, b));
  for (let k = 0; k < 4; k++) fish(ctx, 300 + ((t * 40 + k * 200) % 800), 400 + k * 60, 1, '#ffd166');
  const tb = ap(t, u(78).v0 + 1, 3);
  card(ctx, 1260, 260, 560, 300, { r: 28 });
  text(ctx, 'suhu laut', 1300, 320, fU(28, 700), C.gray); text(ctx, `+${(1.0 * tb).toFixed(1).replace('.', ',')} °C`, 1300, 430, fU(96, 700), C.clayD); text(ctx, 'di atas rata-rata maksimum', 1300, 480, fU(24, 600), C.ink); text(ctx, 'selama beberapa minggu', 1300, 515, fU(24, 600), C.ink);
  show(ctx, t, u(79).v0, () => { card(ctx, 1260, 600, 560, 220, { r: 28, bg: C.forest }); text(ctx, 'karang melepas alga simbion', 1300, 670, fU(26, 700), C.cream); text(ctx, '(zooxanthellae)', 1300, 710, fU(26, 600), C.forest3); text(ctx, 'kehilangan warna dan makanan', 1300, 770, fU(26, 700), C.amber); });
  ctx.restore();
}

function sDampak(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'dampak'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'dampak', 'Dampak di daratan Indonesia');
  const box = { x: 110, y: 240, w: 1700, h: 600 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip(); ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
  const P = mapProj(box, [94, 142, -11.5, 7.5]); drawRings(ctx, IND.IDN, P, C.land, '#a8916a', 0.8);
  const items = [['Musim tanam bergeser', 'musim', 110.5, -7.2], ['Kekeringan dan banjir', 'kekeringan', 118, -8.7], ['DBD ke dataran tinggi', 'demam', 138, -4], ['Kebakaran gambut', 'kebakaran', 113.5, -1.8]];
  items.forEach(([s, w, lon, lat], i) => {
    const k = sp(t, tw(w, u(82).v0) - 0.1, SPRING.bouncy); if (k <= 0) return;
    const x = P.PX(lon), y = P.PY(lat);
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k); circle(ctx, 0, 0, 18); ctx.fillStyle = C.clay; ctx.fill();
    ctx.font = fU(28, 700); const w2 = ctx.measureText(s).width + 36; card(ctx, -w2 / 2, -86, w2, 54, { r: 16 }); text(ctx, s, 0, -50, fU(28, 700), C.ink, 'center');
    ctx.restore();
  });
  ctx.restore();
  ctx.restore();
}

function sRob(ctx, t) {
  fill(ctx, '#e6f0f5'); const ex = exitP(t, 'rob'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'rob', 'Rob di Pantura: laut naik + tanah turun', C.blue);
  const sink = 70 * ap(t, u(85).v0, 6, E.inOutCubic), rise = 12 * ap(t, u(84).v0, 6, E.inOutCubic);
  const base = 640;
  ctx.save(); rrect(ctx, 110, 240, 1100, 600, 28); ctx.clip();
  ctx.fillStyle = '#cfe3ef'; ctx.fillRect(110, 240, 1100, 600);
  ctx.fillStyle = '#9b7b55'; ctx.fillRect(110, base + sink, 650, 400); house(ctx, 430, base + sink, 1.2);
  ctx.fillStyle = 'rgba(58,120,200,0.75)'; ctx.fillRect(110, base - 30 - rise + 20, 1100, 400);
  // pump
  show(ctx, t, tw('penyedotan', u(85).v0) - 0.5, () => { ctx.strokeStyle = '#444'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(620, base + sink - 40); ctx.lineTo(620, 830); ctx.stroke(); ctx.fillStyle = '#444'; ctx.fillRect(595, base + sink - 70, 50, 34); text(ctx, 'sumur bor', 660, base + sink - 40, fU(24, 700), C.ink); });
  ctx.restore();
  show(ctx, t, u(84).v0, () => { card(ctx, 1260, 260, 560, 230, { r: 26 }); text(ctx, 'Kenaikan muka laut', 1300, 320, fU(30, 700), C.blue); text(ctx, '±4 mm/tahun', 1300, 410, fU(64, 700), C.blue); arrowLine(ctx, 1760, 440, 1760, 380, C.blue, 6, 20); });
  show(ctx, t, u(85).v0, () => { card(ctx, 1260, 520, 560, 300, { r: 26, bg: C.clayD }); text(ctx, 'Amblesan tanah', 1300, 580, fU(30, 700), C.cream); text(ctx, 'beberapa cm/tahun', 1300, 670, fU(42, 700), C.cream); text(ctx, 'Jakarta Utara · Semarang · Demak', 1300, 730, fU(24, 600), '#f8d9c8'); arrowLine(ctx, 1760, 590, 1760, 690, C.cream, 6, 20); });
  ctx.restore();
}

function sMitadapt(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'mitadapt'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'mitadapt', 'Dua strategi besar');
  const col = (x, head, sub, color, items, t0) => {
    const p = sp(t, t0, SPRING.snappy); if (p <= 0) return;
    ctx.save(); ctx.globalAlpha *= clamp(p * 1.4); ctx.translate(0, (1 - p) * 60);
    card(ctx, x, 250, 830, 600, { r: 30 }); rrect(ctx, x, 250, 830, 120, 30); ctx.fillStyle = color; ctx.fill(); ctx.fillRect(x, 330, 830, 40);
    text(ctx, head, x + 40, 320, fU(52, 700), C.cream); text(ctx, sub, x + 40, 356, fU(24, 600), C.cream);
    items.forEach(([s, tt], i) => { const q = ap(t, tt, 0.4); if (q <= 0) return; ctx.save(); ctx.globalAlpha *= q; circle(ctx, x + 60, 440 + i * 120, 14); ctx.fillStyle = color; ctx.fill(); wrap(ctx, s, fU(32, 600), 700).forEach((l, j) => text(ctx, l, x + 96, 452 + i * 120 + j * 38, fU(32, 600), C.ink)); ctx.restore(); });
    ctx.restore();
  };
  col(110, 'MITIGASI', 'mengurangi emisi / menambah penyerapan', C.forest, [['Ganti PLTU batu bara dengan energi terbarukan', tw('mengganti', u(89).v0)], ['Cegah kebakaran gambut', tw('mencegah', u(89).v0)], ['Tangkap metana dari TPA', tw('menangkap', u(89).v0)]], u(88).v0);
  col(980, 'ADAPTASI', 'menyesuaikan diri terhadap dampak', C.clay, [['Padi tahan kekeringan', tw('menanam', u(91).v0)], ['Meninggikan rumah di daerah rob', tw('meninggikan', u(91).v0)], ['Sistem peringatan dini', tw('peringatan', u(91).v0)]], u(90).v0);
  ctx.restore();
}
function sMangrove(ctx, t) {
  fill(ctx, '#e8f0ea'); const ex = exitP(t, 'mangrove'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'mangrove', 'Mangrove: mitigasi sekaligus adaptasi', C.forest);
  ctx.fillStyle = '#5aa0c8'; ctx.fillRect(110, 640, 1700, 200); ctx.fillStyle = '#8a7350'; ctx.fillRect(110, 690, 1700, 150);
  const k = sp(t, u(93).v0, SPRING.gentle);
  for (let i = 0; i < 6; i++) mangroveTree(ctx, 560 + i * 160, 700, 0.72 * clamp(k * 1.2 - i * 0.1));
  show(ctx, t, tw('menyerap', u(94).v0), () => { pill(ctx, 'menyerap karbon = MITIGASI', 250, 330, fU(32, 700), C.forest, C.cream, 24, 60); });
  show(ctx, t, tw('melindungi', u(94).v0), () => { pill(ctx, 'melindungi pantai = ADAPTASI', 1770, 330, fU(32, 700), C.clay, C.cream, 24, 60, 'right'); for (let j = 0; j < 3; j++) { const ph = (t * 80 + j * 60) % 200; arrowLine(ctx, 1800 - ph, 660, 1740 - ph, 660, '#ffffff', 5, 16); } });
  show(ctx, t, tw('biru', u(95).v0), () => { card(ctx, 660, 380, 600, 150, { r: 26, bg: '#2f6f9e' }); text(ctx, 'KARBON BIRU', 960, 450, fU(48, 700), C.cream, 'center'); text(ctx, 'mangrove · padang lamun', 960, 495, fU(26, 600), '#dcecf7', 'center'); });
  show(ctx, t, u(96).v0, () => pill(ctx, 'per hektare: beberapa kali lipat hutan daratan', W / 2, 610, fU(28, 700), C.cream, C.forest, 22, 54, 'center'));
  ctx.restore();
}
function sParis(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'paris'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'paris', 'Persetujuan Paris dan NDC Indonesia');
  show(ctx, t, u(97).v0, () => { card(ctx, 110, 250, 820, 300, { r: 28, bg: C.forest }); text(ctx, 'Persetujuan Paris · 2015', 150, 320, fU(34, 700), C.forest3); text(ctx, 'jauh di bawah 2 °C', 150, 410, fU(56, 700), C.cream); show(ctx, t, tw('satu', u(98).v0), () => text(ctx, 'berupaya 1,5 °C', 150, 490, fU(56, 700), C.amber)); });
  show(ctx, t, u(99).v0, () => { card(ctx, 110, 590, 820, 250, { r: 28 }); text(ctx, 'NDC', 150, 670, fU(60, 700), C.clay); text(ctx, 'Nationally Determined Contribution', 150, 720, fU(28, 600), C.ink); text(ctx, 'target penurunan emisi tiap negara', 150, 770, fU(28, 600), C.gray); });
  const pb = ap(t, u(100).v0, 0.6);
  if (pb > 0) {
    ctx.save(); ctx.globalAlpha *= pb; card(ctx, 990, 250, 830, 590, { r: 28 });
    text(ctx, 'Target Indonesia 2030', 1030, 320, fU(34, 700), C.ink);
    const bars = [['usaha sendiri', 31.89, tw('tiga', u(100).v0), C.forestL], ['dukungan internasional', 43.2, tw('empat', u(100).v0), C.forest]];
    bars.forEach(([s, v, t0, col], i) => { const p = ap(t, t0, 1.0); const y = 380 + i * 150; text(ctx, s, 1030, y + 20, fU(26, 600), C.gray); rrect(ctx, 1030, y + 40, 700 * v / 50 * p, 60, 14); ctx.fillStyle = col; ctx.fill(); if (p > 0.5) text(ctx, `${v.toFixed(2).replace('.', ',')}%`, 1050 + 700 * v / 50 * p, y + 84, fU(36, 700), col); });
    show(ctx, t, tw('nol', u(100).v0), () => { pill(ctx, 'Emisi nol bersih (NZE) 2060', 1030, 760, fU(32, 700), C.clay, C.cream, 24, 62); });
    ctx.restore();
  }
  ctx.restore();
}

const OPTS = ['5.500 ton CO2-e', '50.500 ton CO2-e', '56.000 ton CO2-e', '61.500 ton CO2-e', '2.000 ton CO2-e'];
function sSoal(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'soal'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const [tp0, tp1] = T.tm.pause;
  const dock = ap(t, u(102).v0 - 0.3, 0.7, E.inOutCubic);
  const correct = ap(t, tw('jawabannya', u(107).v0), 0.3);
  const Q = 'Sebuah TPA mengemisikan 2.000 ton metana per tahun (GWP metana = 28). Jika metana ditangkap lalu dibakar menjadi CO2 (1 ton CH4 menghasilkan 2,75 ton CO2), besar pengurangan emisinya adalah …';
  const opt = (i, ox, oy, ow, oh, fs) => {
    const on = i === 1 && correct > 0; ctx.save(); ctx.globalAlpha *= correct > 0 && i !== 1 ? 0.35 : 1;
    rrect(ctx, ox, oy, ow, oh, 16); ctx.fillStyle = on ? C.clay : C.sand; ctx.fill();
    circle(ctx, ox + oh * 0.5, oy + oh / 2, oh * 0.3); ctx.fillStyle = on ? C.cream : C.forest; ctx.fill();
    text(ctx, 'ABCDE'[i], ox + oh * 0.5, oy + oh / 2 + fs * 0.36, fU(fs * 0.9, 700), on ? C.clay : C.cream, 'center');
    chem(ctx, OPTS[i], ox + oh + 10, oy + oh / 2 + fs * 0.36, fs, 700, on ? C.cream : C.ink);
    ctx.restore();
  };
  const qLines = (fs, wmax) => wrap(ctx, Q, fU(fs, 500), wmax);
  const pq = sp(t, SC.soal[0] + 0.3, SPRING.snappy);
  if (pq > 0 && dock < 1) {
    ctx.save(); ctx.globalAlpha *= clamp(pq * 1.5) * (1 - dock); ctx.translate(210, 120 + (1 - pq) * 80);
    card(ctx, 0, 0, 1500, 790, { r: 32 }); pill(ctx, 'CONTOH SOAL OSN', 50, 64, fU(28, 700), C.clay, C.cream, 22, 54);
    qLines(38, 1400).forEach((l, i) => chem(ctx, l, 50, 160 + i * 52, 38, 500, C.ink));
    OPTS.forEach((o, i) => opt(i, 50 + (i % 3) * 470, 400 + Math.floor(i / 3) * 140, 440, 110, 40));
    ctx.restore();
  }
  if (t > tp0 - 0.2 && t < tp1 + 0.4) {
    const a = 1 - ap(t, tp1, 0.35), p = clamp((t - tp0) / (tp1 - tp0));
    ctx.save(); ctx.globalAlpha *= a * ap(t, tp0 - 0.2, 0.3);
    const cx = 1790, cy = 210; circle(ctx, cx, cy, 76); ctx.fillStyle = C.forest; ctx.fill();
    ctx.strokeStyle = C.amber; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy, 60, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - p)); ctx.stroke();
    text(ctx, `${Math.max(1, Math.ceil((tp1 - tp0) - (t - tp0)))}`, cx, cy + 26, fU(70, 700), C.cream, 'center'); ctx.restore();
  }
  if (dock > 0) {
    ctx.save(); ctx.globalAlpha *= dock;
    card(ctx, 80, 130, 860, 790, { r: 30 }); pill(ctx, 'CONTOH SOAL OSN', 120, 186, fU(24, 700), C.clay, C.cream, 20, 48);
    qLines(29, 780).forEach((l, i) => chem(ctx, l, 120, 260 + i * 40, 29, 500, C.ink));
    OPTS.forEach((o, i) => opt(i, 120, 470 + i * 88, 780, 76, 30));
    card(ctx, 990, 130, 850, 790, { r: 30, bg: C.forest });
    const steps = [[u(102).v0, '1) Emisi awal', C.forest3, 30], [tw('dikali', u(103).v0), '2.000 × 28 = 56.000 ton CO2-e', C.cream, 38],
      [u(104).v0, '2) Setelah dibakar', C.forest3, 30], [u(105).v0, '2.000 × 2,75 = 5.500 ton CO2', C.cream, 38],
      [u(106).v0, '3) Pengurangan', C.forest3, 30], [tw('dikurangi', u(106).v0), '56.000 − 5.500', C.cream, 40], [tw('ribu', u(106).v0, 2), '= 50.500 ton CO2-e', C.amber, 56], [tw('sembilan', u(106).v0), '(±90%)', C.amber, 36]];
    let y = 210; steps.forEach(([t0, s, col, size]) => { const p = ap(t, t0, 0.5, E.outQuint); if (p > 0) { ctx.save(); ctx.beginPath(); ctx.rect(1010, y - size - 10, 810, size + 30); ctx.clip(); chem(ctx, s, 1040, y + (1 - p) * (size + 30), size, 700, col); ctx.restore(); } y += size + 40; });
    show(ctx, t, tw('jawabannya', u(107).v0), () => pill(ctx, 'Jawaban: B', 1415, 870, fU(36, 700), C.clay, C.cream, 30, 64, 'center'));
    ctx.restore();
  }
  ctx.restore();
}

function sJebakan(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'jebakan'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const pw = sp(t, SC.jebakan[0] + 0.05, SPRING.bouncy);
  if (pw > 0) { ctx.save(); ctx.translate(180, 150); ctx.scale(pw, pw); warnIcon(ctx, 0, 0, 60); ctx.restore(); }
  riseText(ctx, 'Tiga jebakan yang sering muncul', 280, 175, fD(76), C.clayD, ap(t, SC.jebakan[0] + 0.15, 0.5, E.outQuint));
  const items = [
    [u(110).v0, 'Efek rumah kaca itu buruk dan harus dihilangkan', 'Yang bermasalah: efek rumah kaca TAMBAHAN', u(111).v0],
    [u(112).v0, 'Lubang ozon menyebabkan pemanasan global', 'Lubang ozon: lebih banyak UV masuk, mekanisme BERBEDA', u(113).v0],
    [u(114).v0, 'Rob Pantura hanya karena kenaikan muka laut', 'Rob = kenaikan muka laut + AMBLESAN TANAH', tw('gabungan', u(114).v0)],
  ];
  items.forEach(([t0, wrong, right, tfix], i) => {
    const p = sp(t, t0, SPRING.snappy); if (p <= 0) return;
    const y = 260 + i * 210; ctx.save(); ctx.globalAlpha *= clamp(p * 1.5); ctx.translate((1 - p) * 80, 0);
    card(ctx, 110, y, 1700, 180, { r: 26 }); text(ctx, `${i + 1}`, 170, y + 110, fU(70, 700), C.clay, 'center');
    const f = ap(t, tfix - 0.3, 0.4);
    text(ctx, wrong, 250, y + 72, fU(34, 600), f > 0 ? 'rgba(152,63,41,0.6)' : C.clayD);
    if (f > 0) { ctx.strokeStyle = C.clay; ctx.lineWidth = 5; ctx.font = fU(34, 600); const w = ctx.measureText(wrong).width; ctx.beginPath(); ctx.moveTo(250, y + 60); ctx.lineTo(250 + w * f, y + 60); ctx.stroke(); ctx.save(); ctx.globalAlpha *= f; circle(ctx, 280, y + 130, 22); ctx.fillStyle = C.forest; ctx.fill(); check(ctx, 280, y + 130, 26, C.cream, f); text(ctx, right, 320, y + 142, fU(36, 700), C.forest); ctx.restore(); }
    ctx.restore();
  });
  ctx.restore();
}

function sKamus(ctx, t) {
  fill(ctx, C.forestD); const ex = exitP(t, 'kamus'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  ctx.save(); ctx.globalAlpha *= 0.06; ctx.strokeStyle = C.cream; for (let x = 0; x < W; x += 80) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); } ctx.restore();
  ctx.save(); ctx.globalAlpha *= ap(t, SC.kamus[0] + 0.05, 0.5); pill(ctx, 'KAMUS ISTILAH OSN', 110, 120, fU(30, 700), C.clay, C.cream, 24, 58); ctx.restore();
  riseText(ctx, '18 istilah yang wajib kamu kuasai', 110, 225, fD(76), C.cream, ap(t, SC.kamus[0] + 0.2, 0.5, E.outQuint));
  const all = ap(t, u(134).v0, 0.6);
  TERMS.forEach(([s], i) => {
    const t0 = U_(116 + i).v0; const k = sp(t, t0 - 0.05, SPRING.snappy);
    const col = i % 3, row = Math.floor(i / 3), x = 110 + col * 575, y = 270 + row * 106, on = k > 0;
    ctx.save(); ctx.globalAlpha *= on ? 1 : 0.25;
    rrect(ctx, x, y, 545, 90, 18); ctx.fillStyle = on ? (bump(t, t0 + 0.4, 0.8) > 0.2 ? C.clay : 'rgba(255,254,250,0.1)') : 'rgba(255,254,250,0.05)'; ctx.fill();
    text(ctx, `${i + 1}`, x + 46, y + 58, fU(30, 700), on ? C.amber : C.forest3, 'center');
    chem(ctx, s, x + 90, y + 58, s.length > 22 ? 28 : 33, 700, C.cream);
    if (all > 0) check(ctx, x + 505, y + 45, 34, C.amber, all);
    ctx.restore();
  });
  ctx.restore();
}

// ---------------------------------------------------------------- hits
function addHits() {
  const u = (i) => U_(i);
  SCN.forEach(([n], i) => { if (i > 0 && n !== 'outro') hit(SC[n][0] + 0.2, 'scene ' + n, 'whoosh', { len: 0.4, gain: 0.22 }); });
  TERMS.forEach(([s, , ui]) => hit(U_(ui).v0, 'term ' + s, 'pop', { pitch: 'A5', gain: 0.32 }));
  hit(u(4).v0 - 0.1, 'title', 'bell', { pitch: 'D6', gain: 0.35 });
  const [p0] = T.tm.pause; for (let k = 0; k < 4; k++) hit(p0 + k, 'timer ' + k, 'blip', { pitch: 880, gain: 0.22 });
  hit(tw('jawabannya', u(107).v0), 'answer', 'bell', { pitch: 'E6', gain: 0.4 });
  TERMS.forEach((s, i) => hit(U_(116 + i).v0 - 0.05, 'recap ' + i, 'click', { gain: 0.25 }));
  hit(SC.outro[0] + 0.2, 'logo', 'bell', { pitch: 'D6', gain: 0.4 });
  HITS.sort((a, b) => a[0] - b[0]);
}

const DRAW = { hook: sHook, peta: sPeta, gelombang: sGelombang, albedo: sAlbedo, neraca: sNeraca, erk: sErk, alami: sAlami, tambahan: sTambahan, keeling: sKeeling,
  imbalance: sImbalance, gwp: sGwp, co2e: sCo2e, bukti: sBukti, umpan: sUmpan, laut: sLaut, karang: sKarang, dampak: sDampak, rob: sRob,
  mitadapt: sMitadapt, mangrove: sMangrove, paris: sParis, soal: sSoal, jebakan: sJebakan, kamus: sKamus };

M.film({
  fonts: [M.font(100, 400, 'Display'), M.font(40, 500, 'UI'), M.font(40, 600, 'UI'), M.font(40, 700, 'UI')],
  hits: HITS,
  samples: () => 3,
  async init() {
    T.tm = await fetch('timing.json').then((r) => r.json());
    IND = await fetch('assets/indo.json').then((r) => r.json());
    buildScenes(); buildCaps(); addHits();
  },
  draw(ctx, u, t) {
    const S = Object.keys(SC).find((k) => t >= SC[k][0] && t < SC[k][1]) || 'outro';
    if (S === 'intro') intro(ctx, t, 'BAB 1 · IKLIM · SANGAT SERING MUNCUL', 'Efek Rumah Kaca', 'dan pemanasan global · 18 istilah penting OSN');
    else if (S === 'outro') outro(ctx, t, SC.outro[0], tw('menu', SC.outro[0]), 'Menu Soal Pendalaman Materi  ·  Bab 1', 'B01-V03 · Sirkulasi Atmosfer Global dan Monsun');
    else DRAW[S](ctx, t);
    if (S !== 'intro' && S !== 'outro') { centerMark(ctx, S === 'kamus' ? 0.9 : 1, S === 'kamus' ? C.cream : C.forest); termCard(ctx, t); }
    lowerThird(ctx, t, 'OSNGEO.id  ·  Bab 1 Iklim  ·  B01-V02');
    if (S !== 'intro') captions(ctx, t);
    cornerMark(ctx);
  },
});
