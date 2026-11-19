// B01-V01 · El Niño, La Niña, dan IOD (+MJO) · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import {
  C, fD, fU, T, tw, U_, sp, ap, poly, circle, card, arrowLine, check, cross, wrap, riseText, pill, warnIcon,
  sun, cloud, rain, fish, mapProj, drawRings, cornerMark, centerMark, lowerThird, buildCaps, captions, intro, outro,
} from './lib/common.js';
const { W, H, E, prog, lerp, clamp, spring, SPRING, text, fill, rrect, bump, hash01, mix } = M;

let PAC = null, IND = null, IP = null;
const HITS = [];
const hit = (t, label, sfx, o = {}) => HITS.push([t, label, sfx, { gain: 0.55, ...o }]);

// ---------------------------------------------------------------- scenes, keyed to first VO unit
const SCN = [['hook', 0], ['peta', 7], ['normal', 18], ['elnino', 36], ['dampak', 42], ['peru', 48], ['lanina', 55], ['enso', 60], ['oni', 64],
  ['soi', 79], ['iod', 82], ['wilayah', 92], ['kombinasi', 96], ['mjo', 100], ['skala', 104], ['soal', 110], ['jebakan', 118], ['kamus', 123], ['outro', 143]];
const SC = {};
function buildScenes() {
  SC.intro = [0, 3.0];
  SCN.forEach(([n, u], i) => {
    const a = i === 0 ? 3.0 : U_(u).v0 - 0.2;
    const b = i < SCN.length - 1 ? U_(SCN[i + 1][1]).v0 - 0.2 : 626.5;
    SC[n] = [a, b];
  });
}
const exitP = (t, n, d = 0.35) => E.inCubic(prog(t, SC[n][1] - d, SC[n][1]));
const title = (ctx, t, n, s, col = C.forest) => riseText(ctx, s, 110, 165, fD(76), col, ap(t, SC[n][0] + 0.1, 0.55, E.outQuint));

// ---------------------------------------------------------------- 18 terms (order of appearance)
const TERMS = [
  ['Variabilitas iklim', 'Penyimpangan dari rata-rata (bulanan–tahunan), lalu kembali normal', 13],
  ['Angin pasat', 'Angin tetap dari timur ke barat di sekitar ekuator', 20],
  ['Kolam air hangat', 'Tumpukan air laut hangat di Pasifik barat (warm pool)', 22],
  ['Termoklin', 'Lapisan batas air hangat (atas) dan air dingin (bawah)', 24],
  ['Upwelling', 'Naiknya air dingin kaya nutrien ke permukaan', 27],
  ['Konveksi', 'Udara panas naik, membentuk awan dan hujan', 31],
  ['Sirkulasi Walker', 'Sel sirkulasi barat–timur di atas Pasifik ekuator', 33],
  ['El Niño', 'Pasat melemah, air hangat ke timur, Indonesia kering', 41],
  ['Anomali suhu muka laut', 'Selisih suhu laut terhadap rata-rata normal', 52],
  ['La Niña', 'Pasat menguat, air hangat menumpuk di barat, Indonesia basah', 55],
  ['Osilasi Selatan', 'Jungkat-jungkit tekanan udara Tahiti–Darwin', 61],
  ['ENSO', 'El Niño–Southern Oscillation, berulang tiap 2–7 tahun', 62],
  ['ONI', 'Anomali suhu laut 3 bulanan di Niño 3.4; ambang ±0,5 °C', 66],
  ['Niño 3.4', 'Pasifik tengah: 5° LU–5° LS, 120°–170° BB', 67],
  ['SOI', 'Selisih tekanan Tahiti–Darwin; negatif = El Niño', 79],
  ['IOD dan DMI', 'Dipol suhu Samudra Hindia barat vs timur, dan indeksnya', 84],
  ['Telekoneksi', 'Pengaruh fenomena di satu tempat ke tempat yang jauh', 95],
  ['MJO', 'Gugus awan merambat ke timur, periode 30–60 hari, 8 fase', 100],
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
    text(ctx, term, x + 34, y + 74, fU(term.length > 18 ? 32 : 38, 700), C.ink);
    wrap(ctx, def, fU(22, 500), w - 60).slice(0, 1).forEach((l) => text(ctx, l, x + 34, y + 104, fU(22, 500), C.gray));
    ctx.restore();
  }
}

// ---------------------------------------------------------------- Pacific cross-section (state: -1 La Niña .. 0 normal .. +1 El Niño)
const PB = { x: 110, y: 300, w: 1700, h: 540 };
function pacific(ctx, t, s, f) {
  const { x, y, w, h } = PB, ys = y + 220, yb = y + h;
  const sel = (n, e, l) => (s >= 0 ? lerp(n, e, s) : lerp(n, l, -s));
  const thermo = (u) => sel(lerp(200, 40, u), lerp(125, 105, u), lerp(250, 22, u));
  ctx.save(); rrect(ctx, x, y, w, h, 28); ctx.clip();
  // sky
  const sky = ctx.createLinearGradient(0, y, 0, ys); sky.addColorStop(0, '#dfeaf0'); sky.addColorStop(1, '#f4efe4');
  ctx.fillStyle = sky; ctx.fillRect(x, y, w, ys - y);
  // ocean: cold base
  ctx.fillStyle = '#2f6f9e'; ctx.fillRect(x, ys, w, yb - ys);
  // warm layer above thermocline, colored by surface temperature along x
  const pool = sel(0.15, 0.55, 0.08);
  const g = ctx.createLinearGradient(x, 0, x + w, 0);
  for (let k = 0; k <= 10; k++) {
    const u = k / 10, warm = clamp(1 - Math.abs(u - pool) / sel(0.55, 0.6, 0.45));
    g.addColorStop(u, mix('#7fb7d6', '#e07a4f', warm));
  }
  ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x, ys);
  for (let i = 0; i <= 60; i++) { const u = i / 60; ctx.lineTo(x + u * w, ys + thermo(u) * f.therm); }
  for (let i = 60; i >= 0; i--) ctx.lineTo(x + (i / 60) * w, ys);
  ctx.closePath(); ctx.fill();
  if (f.therm > 0) {
    ctx.save(); ctx.globalAlpha = f.therm; ctx.setLineDash([16, 10]); ctx.strokeStyle = C.cream; ctx.lineWidth = 4;
    ctx.beginPath(); for (let i = 0; i <= 60; i++) { const u = i / 60; const yy = ys + thermo(u); i ? ctx.lineTo(x + u * w, yy) : ctx.moveTo(x + u * w, yy); } ctx.stroke();
    ctx.setLineDash([]); text(ctx, 'termoklin', x + w * 0.5, ys + thermo(0.5) + 34, fU(26, 700), C.cream, 'center'); ctx.restore();
  }
  // land: Indonesia (west) and South America (east)
  ctx.fillStyle = '#c9b48a';
  ctx.beginPath(); ctx.moveTo(x, ys - 60); ctx.quadraticCurveTo(x + 80, ys - 110, x + 150, ys - 20); ctx.lineTo(x + 150, ys + 8); ctx.lineTo(x, ys + 8); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x + w, ys - 170); ctx.lineTo(x + w - 70, ys - 150); ctx.lineTo(x + w - 120, ys - 20); ctx.lineTo(x + w - 140, ys + 8); ctx.lineTo(x + w, ys + 8); ctx.fill();
  text(ctx, 'Indonesia', x + 30, ys - 120, fU(30, 700), C.ink);
  text(ctx, 'Peru', x + w - 30, ys - 190, fU(30, 700), C.ink, 'right');
  text(ctx, 'BARAT', x + 20, yb - 20, fU(22, 700), 'rgba(255,255,255,0.7)'); text(ctx, 'TIMUR', x + w - 20, yb - 20, fU(22, 700), 'rgba(255,255,255,0.7)', 'right');
  // warm pool label
  if (f.pool > 0) { ctx.save(); ctx.globalAlpha = f.pool; pill(ctx, 'kolam air hangat', x + pool * w, ys + 60, fU(26, 700), C.clay, C.cream, 18, 46, 'center'); ctx.restore(); }
  // upwelling arrows near Peru
  const upS = sel(1, 0.2, 1.6) * f.up;
  if (upS > 0.02) {
    ctx.save(); ctx.globalAlpha = clamp(f.up);
    for (let k = 0; k < 3; k++) {
      const xx = x + w - 230 - k * 50, ph = (t * 60 * upS + k * 40) % 120;
      arrowLine(ctx, xx, yb - 30 - ph * 0.3, xx + 10, yb - 120 - ph * 0.6 * upS, '#bfe6ff', 6, 20);
    }
    text(ctx, 'upwelling', x + w - 290, yb - 160, fU(26, 700), '#e6f5ff', 'center');
    const nf = Math.round(4 * clamp(upS));
    for (let k = 0; k < nf; k++) fish(ctx, x + w - 420 + k * 46 + Math.sin(t * 2 + k) * 6, ys + 34 + (k % 2) * 26, 0.9, '#103a2c');
    ctx.restore();
  }
  // trade winds at surface (pointing west)
  const tr = sel(1, 0.22, 1.7) * f.wind;
  if (tr > 0.02) {
    ctx.save(); ctx.globalAlpha = clamp(f.wind);
    const n = 5;
    for (let k = 0; k < n; k++) {
      const off = ((t * 120 * tr + k * w / n) % w);
      const xx = x + w - 160 - off * 0.85;
      if (xx < x + 180) continue;
      arrowLine(ctx, xx, ys - 26, xx - 70 * clamp(tr, 0.3, 1.6), ys - 26, C.forest, 6, 20);
    }
    text(ctx, sel('angin pasat', 'pasat melemah', 'pasat menguat'), x + w * 0.62, ys - 50, fU(26, 700), C.forest, 'center');
    ctx.restore();
  }
  // convection cloud + Walker loop
  const cx = x + w * sel(0.16, 0.56, 0.12), sx = x + w * sel(0.84, 0.88, 0.84);
  if (f.conv > 0) {
    ctx.save(); ctx.globalAlpha = f.conv;
    for (let k = 0; k < 3; k++) { const ph = (t * 50 + k * 30) % 90; arrowLine(ctx, cx - 40 + k * 40, ys - 40 - ph, cx - 40 + k * 40, ys - 80 - ph, C.clay, 5, 16); }
    cloud(ctx, cx, y + 70, 1.2 * sel(1, 1, 1.25), '#ffffff');
    rain(ctx, cx, y + 100, 160, t, 7, C.blue, 22, 220, 0.9);
    ctx.restore();
  }
  if (f.sink > 0) {
    ctx.save(); ctx.globalAlpha = f.sink;
    for (let k = 0; k < 3; k++) { const ph = (t * 40 + k * 30) % 90; arrowLine(ctx, sx - 40 + k * 40, y + 60 + ph, sx - 40 + k * 40, y + 100 + ph, C.gray, 5, 16); }
    text(ctx, 'udara turun', sx, y + 40, fU(24, 700), C.gray, 'center');
    if (s > 0.3) { // during El Niño air sinks over Indonesia
      ctx.globalAlpha = f.sink * clamp((s - 0.3) / 0.5);
      const ix = x + w * 0.12;
      for (let k = 0; k < 3; k++) { const ph = (t * 40 + k * 30) % 90; arrowLine(ctx, ix - 40 + k * 40, y + 60 + ph, ix - 40 + k * 40, y + 100 + ph, C.clayD, 5, 16); }
      text(ctx, 'udara turun, awan sulit terbentuk', ix + 10, y + 40, fU(24, 700), C.clayD);
    }
    ctx.restore();
  }
  if (f.walker > 0) {
    ctx.save(); ctx.globalAlpha = f.walker; ctx.strokeStyle = 'rgba(29,65,56,0.75)'; ctx.lineWidth = 5; ctx.setLineDash([14, 12]); ctx.lineDashOffset = -t * 40;
    const yt = y + 40, yl = ys - 70;
    ctx.beginPath(); ctx.moveTo(cx + 60, yl); ctx.lineTo(cx + 60, yt + 30); ctx.quadraticCurveTo(cx + 60, yt, cx + 100, yt);
    ctx.lineTo(sx - 100, yt); ctx.quadraticCurveTo(sx - 60, yt, sx - 60, yt + 30); ctx.lineTo(sx - 60, yl); ctx.stroke(); ctx.setLineDash([]);
    arrowLine(ctx, (cx + sx) / 2 - 20, yt, (cx + sx) / 2 + 20, yt, 'rgba(29,65,56,0.9)', 5, 20);
    pill(ctx, 'sirkulasi Walker', (cx + sx) / 2, yt + 40, fU(24, 700), C.forest, C.cream, 16, 42, 'center');
    ctx.restore();
  }
  ctx.restore();
  rrect(ctx, x, y, w, h, 28); ctx.strokeStyle = 'rgba(27,50,43,0.25)'; ctx.lineWidth = 2; ctx.stroke();
}

// ================================================================ scenes
function sHook(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'hook');
  const u = (i) => U_(i);
  const L = { x: 80, y: 190, w: 840, h: 520 }, R = { x: 1000, y: 190, w: 840, h: 520 };
  const pl = sp(t, 3.05, SPRING.gentle), pr = sp(t, u(2).v0, SPRING.gentle);
  if (pl > 0) {
    ctx.save(); ctx.translate(-(1 - pl) * 1000 - ex * 1100, 0);
    ctx.save(); rrect(ctx, L.x, L.y, L.w, L.h, 34); ctx.clip();
    const g = ctx.createLinearGradient(0, L.y, 0, L.y + L.h); g.addColorStop(0, '#d97a3a'); g.addColorStop(1, '#f0c27b');
    ctx.fillStyle = g; ctx.fillRect(L.x, L.y, L.w, L.h);
    sun(ctx, L.x + 620, L.y + 140, 46, t, 0.45);
    ctx.fillStyle = '#7b4a32'; [[0, 160], [70, 240], [150, 190], [220, 300], [300, 210], [380, 260], [460, 180], [540, 230], [620, 170], [700, 210]].forEach(([bx, bh]) => ctx.fillRect(L.x + 30 + bx, L.y + L.h - 40 - bh, 60, bh));
    ctx.fillStyle = '#5a3424'; ctx.fillRect(L.x, L.y + L.h - 40, L.w, 40);
    for (let k = 0; k < 7; k++) { ctx.fillStyle = 'rgba(120,90,70,0.28)'; ctx.beginPath(); ctx.ellipse(L.x + ((k * 160 + t * 30) % 1000) - 80, L.y + 160 + k * 40, 220, 50, 0, 0, Math.PI * 2); ctx.fill(); }
    ctx.restore();
    text(ctx, '2015', L.x + 40, L.y + 86, fD(84), C.cream);
    pill(ctx, 'kabut asap · karhutla', L.x + 40, L.y + 140, fU(28, 700), 'rgba(22,41,35,0.75)', C.cream, 20, 50);
    ctx.restore();
  }
  if (pr > 0) {
    ctx.save(); ctx.translate((1 - pr) * 1000 + ex * 1100, 0);
    ctx.save(); rrect(ctx, R.x, R.y, R.w, R.h, 34); ctx.clip();
    const g = ctx.createLinearGradient(0, R.y, 0, R.y + R.h); g.addColorStop(0, '#5f7d93'); g.addColorStop(1, '#a9c1cf');
    ctx.fillStyle = g; ctx.fillRect(R.x, R.y, R.w, R.h);
    for (let k = 0; k < 4; k++) cloud(ctx, R.x + 150 + k * 190, R.y + 140 + (k % 2) * 30, 1.3, '#8aa1b1', '#4a6577');
    rain(ctx, R.x + R.w / 2, R.y + 170, R.w, t, 28, '#dcecf7', 30, 320, 0.9);
    ctx.fillStyle = '#6d7f86'; [[40, 150], [160, 200], [300, 170], [440, 220], [580, 160], [690, 190]].forEach(([bx, bh]) => ctx.fillRect(R.x + bx, R.y + R.h - 30 - bh, 90, bh));
    const fl = 70 + 10 * Math.sin(t * 1.5);
    ctx.fillStyle = 'rgba(120,96,64,0.85)'; ctx.fillRect(R.x, R.y + R.h - fl, R.w, fl);
    ctx.restore();
    text(ctx, '2021', R.x + 40, R.y + 86, fD(84), C.cream);
    pill(ctx, 'hujan terus · banjir', R.x + 40, R.y + 140, fU(28, 700), 'rgba(22,41,35,0.75)', C.cream, 20, 50);
    ctx.restore();
  }
  const pq = ap(t, u(4).v0, 0.4);
  if (pq > 0 && t < u(6).v0) { ctx.save(); ctx.globalAlpha = pq * (1 - ap(t, u(6).v0 - 0.3, 0.3)); pill(ctx, 'Wilayah sama, negara sama. Apa bedanya?', W / 2, 800, fU(36, 700), C.forest, C.cream, 30, 66, 'center'); ctx.restore(); }
  // u6: Pacific map reveal
  const pm = sp(t, u(6).v0 - 0.1, SPRING.gentle);
  if (pm > 0) {
    ctx.save(); ctx.globalAlpha = clamp(pm * 1.4) * (1 - ex);
    const box = { x: 260, y: 170 + (1 - pm) * 60, w: 1400, h: 600 };
    card(ctx, box.x - 10, box.y - 10, box.w + 20, box.h + 20, { r: 30 });
    ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip(); ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
    const P = mapProj(box, [95, 295, -40, 45]); drawRings(ctx, PAC, P, C.land, '#a8916a', 0.8);
    const q = 0.5 + 0.5 * Math.sin(t * 4);
    text(ctx, '?', P.PX(200), P.PY(0) + 40, fD(160 + 20 * q), C.clay, 'center');
    text(ctx, 'SAMUDRA PASIFIK', P.PX(205), P.PY(-18), fU(30, 700), C.blue, 'center');
    text(ctx, 'Indonesia', P.PX(118), P.PY(-12), fU(26, 700), C.ink, 'center');
    ctx.restore(); ctx.restore();
  }
}

function sPeta(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'peta'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const p2 = ap(t, u(12).v0 - 0.2, 0.5, E.inOutCubic); // switch to variabilitas
  if (p2 < 1) {
    ctx.save(); ctx.globalAlpha *= 1 - p2;
    riseText(ctx, 'Yang kita bahas', 110, 165, fD(76), C.forest, ap(t, SC.peta[0] + 0.1, 0.5, E.outQuint));
    const cards = [['El Niño', C.clay, tw('el', u(8).v0)], ['La Niña', C.blue, tw('la', u(8).v0)], ['IOD', C.forestL, tw('i', u(8).v0, 0)], ['MJO', C.amber, u(9).v0 + 0.3]];
    cards.forEach(([s, col, t0], i) => {
      const k = sp(t, t0 - 0.1, SPRING.bouncy); if (k <= 0) return;
      const x = 110 + i * 430, y = 260;
      ctx.save(); ctx.translate(x + 190, y + 150); ctx.scale(k, k); ctx.translate(-(x + 190), -(y + 150));
      card(ctx, x, y, 380, 300, { r: 30 });
      rrect(ctx, x, y, 380, 22, 11); ctx.fillStyle = col; ctx.fill();
      text(ctx, s, x + 190, y + 190, fD(i === 3 ? 92 : 104), C.ink, 'center');
      if (i === 3) pill(ctx, 'BONUS', x + 190, y + 80, fU(24, 700), C.amber, C.ink, 18, 44, 'center');
      ctx.restore();
    });
    const pc = ap(t, tw('delapan', u(10).v0), 1.4, E.outCubic);
    if (pc > 0) {
      ctx.save(); ctx.globalAlpha *= clamp(pc * 3);
      card(ctx, 110, 620, 1700, 200, { r: 30, bg: C.forest });
      text(ctx, `${Math.round(18 * pc)}`, 300, 780, fU(150, 700), C.amber, 'center');
      text(ctx, 'istilah penting akan muncul di layar', 440, 715, fU(46, 700), C.cream);
      text(ctx, 'Catat semuanya: istilah inilah yang sering dipakai soal untuk menjebak.', 440, 775, fU(30, 500), C.forest3);
      ctx.restore();
    }
    ctx.restore();
  }
  if (p2 > 0) {
    ctx.save(); ctx.globalAlpha *= p2;
    riseText(ctx, 'Variabilitas iklim vs perubahan iklim', 110, 165, fD(70), C.forest, p2);
    const panel = (x, label, col, trend, p) => {
      card(ctx, x, 250, 820, 520, { r: 28 });
      text(ctx, label, x + 40, 320, fU(40, 700), col);
      const gx = x + 60, gy = 680, gw = 700, gh = 280;
      ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
      text(ctx, 'waktu', gx + gw, gy + 36, fU(24, 500), C.gray, 'right');
      // mean line
      ctx.setLineDash([10, 10]); ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath();
      ctx.moveTo(gx, gy - gh / 2 + (trend ? 60 : 0)); ctx.lineTo(gx + gw, gy - gh / 2 - (trend ? 70 : 0)); ctx.stroke(); ctx.setLineDash([]);
      ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath();
      const n = Math.floor(160 * p);
      for (let i = 0; i <= n; i++) { const f = i / 160; const base = gy - gh / 2 + (trend ? 60 - 130 * f : 0); const yy = base - Math.sin(f * 22) * 55 * (trend ? 0.5 : 1); i ? ctx.lineTo(gx + f * gw, yy) : ctx.moveTo(gx + f * gw, yy); }
      ctx.stroke();
    };
    panel(110, 'Variabilitas iklim', C.clay, false, ap(t, u(14).v0, 4, E.linear));
    const pp = ap(t, u(16).v0, 0.4);
    if (pp > 0) { ctx.save(); ctx.globalAlpha *= pp; panel(990, 'Perubahan iklim', C.blue, true, ap(t, u(16).v0, 3.5, E.linear)); ctx.restore(); }
    const sub = [[u(14).v0 + 1.5, 'bulanan – beberapa tahun, lalu kembali normal', 150], [u(16).v0 + 2.5, 'rata-ratanya bergeser selama puluhan tahun', 1030]];
    sub.forEach(([t0, s, x]) => { const p = ap(t, t0, 0.4); if (p > 0) { ctx.save(); ctx.globalAlpha *= p; text(ctx, s, x, 370, fU(26, 500), C.gray); ctx.restore(); } });
    const pb = ap(t, u(15).v0, 0.4);
    if (pb > 0) { ctx.save(); ctx.globalAlpha *= pb; ['El Niño', 'La Niña', 'IOD'].forEach((s, i) => pill(ctx, s, 160 + i * 170, 420, fU(26, 700), C.clay, C.cream, 18, 46)); ctx.restore(); }
    const pz = ap(t, u(17).v0, 0.4);
    if (pz > 0) { ctx.save(); ctx.globalAlpha *= pz; pill(ctx, 'El Niño BUKAN perubahan iklim', W / 2, 830, fU(36, 700), C.forest, C.cream, 30, 66, 'center'); ctx.restore(); }
    ctx.restore();
  }
  ctx.restore();
}

function sNormal(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'normal'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'normal', 'Kondisi normal di Pasifik ekuator');
  const f = {
    wind: ap(t, u(19).v0, 0.6), pool: ap(t, tw('kolam', u(22).v0), 0.5), therm: ap(t, u(23).v0 + 0.5, 1.5, E.inOutCubic),
    up: ap(t, u(26).v0 + 1, 1.0), conv: ap(t, u(30).v0, 0.8), sink: ap(t, u(32).v0, 0.6), walker: ap(t, u(33).v0 + 1, 1.0),
  };
  const pb = sp(t, SC.normal[0] + 0.2, SPRING.gentle);
  ctx.save(); ctx.translate(0, (1 - pb) * 60); ctx.globalAlpha *= clamp(pb * 1.5);
  pacific(ctx, t, 0, f);
  ctx.restore();
  const ps = ap(t, u(35).v0, 0.4);
  if (ps > 0) {
    ctx.save(); ctx.globalAlpha *= ps;
    pill(ctx, 'Indonesia: cukup basah', 140, 880, fU(30, 700), C.forest, C.cream, 22, 56);
    pill(ctx, 'Peru: kering, laut kaya ikan', 1780, 880, fU(30, 700), C.blue, C.cream, 22, 56, 'right');
    ctx.restore();
  }
  ctx.restore();
}
function sElnino(ctx, t) {
  fill(ctx, '#f7ece2'); const ex = exitP(t, 'elnino'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'elnino', 'Saat angin pasat melemah…', C.clayD);
  const s = ap(t, u(36).v0 + 0.5, u(39).v1 - u(36).v0, E.inOutCubic);
  pacific(ctx, t, s, { wind: 1, pool: 1, therm: 1, up: 1, conv: 1, sink: 1, walker: 1 });
  const pk = sp(t, u(41).v0, SPRING.bouncy);
  if (pk > 0) { ctx.save(); ctx.translate(W / 2, 560); ctx.scale(pk, pk); ctx.rotate(-0.04); card(ctx, -260, -90, 520, 160, { r: 36, bg: C.clay }); text(ctx, 'EL NIÑO', 0, 30, fU(96, 700), C.cream, 'center'); ctx.restore(); }
  ctx.restore();
}
function sLanina(ctx, t) {
  fill(ctx, '#e8f0f4'); const ex = exitP(t, 'lanina'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'lanina', 'La Niña: kebalikannya', C.blue);
  const s = -ap(t, u(56).v0, 3.0, E.inOutCubic);
  pacific(ctx, t, s, { wind: 1, pool: 1, therm: 1, up: 1, conv: 1, sink: 1, walker: 1 });
  const pk = sp(t, SC.lanina[0] + 0.3, SPRING.bouncy);
  if (pk > 0 && t < u(58).v0) { ctx.save(); ctx.globalAlpha = 1 - ap(t, u(58).v0 - 0.4, 0.4); ctx.translate(W / 2, 560); ctx.scale(pk, pk); card(ctx, -260, -90, 520, 160, { r: 36, bg: C.blue }); text(ctx, 'LA NIÑA', 0, 30, fU(96, 700), C.cream, 'center'); ctx.restore(); }
  const p1 = ap(t, u(58).v0, 0.4), p2 = ap(t, u(59).v0, 0.4);
  if (p1 > 0) { ctx.save(); ctx.globalAlpha *= p1; pill(ctx, 'Indonesia: banjir, longsor, gelombang tinggi', 140, 880, fU(30, 700), C.blue, C.cream, 22, 56); ctx.restore(); }
  if (p2 > 0) { ctx.save(); ctx.globalAlpha *= p2; pill(ctx, 'Peru: upwelling kuat, ikan melimpah', 1780, 880, fU(30, 700), C.forest, C.cream, 22, 56, 'right'); ctx.restore(); }
  ctx.restore();
}

// impact icons
function impactIcon(ctx, k, x, y, t) {
  ctx.save(); ctx.translate(x, y); ctx.lineWidth = 6; ctx.strokeStyle = C.ink; ctx.lineCap = 'round';
  if (k === 0) { cloud(ctx, 0, -10, 0.8, '#ffffff'); cross(ctx, 30, 30, 14, C.clay, 7); }
  if (k === 1) { sun(ctx, 0, 0, 34, t); }
  if (k === 2) { ctx.fillStyle = '#7b5a3c'; ctx.fillRect(-50, 10, 100, 30); for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(i * 20, 10); ctx.lineTo(i * 20 + 6, -10 + (i % 2) * 8); ctx.stroke(); } }
  if (k === 3) { ctx.fillStyle = C.clay; ctx.beginPath(); ctx.moveTo(0, -46); ctx.bezierCurveTo(34, -10, 30, 30, 0, 36); ctx.bezierCurveTo(-30, 30, -34, -10, 0, -46); ctx.fill(); ctx.fillStyle = C.amber; ctx.beginPath(); ctx.moveTo(0, -10); ctx.bezierCurveTo(16, 6, 14, 26, 0, 30); ctx.bezierCurveTo(-14, 26, -16, 6, 0, -10); ctx.fill(); }
  if (k === 4) { ctx.strokeStyle = '#b58a2a'; for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(i * 16, 40); ctx.quadraticCurveTo(i * 16 + 10, 0, i * 16 + 4, -36); ctx.stroke(); } text(ctx, 'Rp↑'.replace('↑', '+'), 34, -20, fU(26, 700), C.clayD); }
  if (k === 5) { ctx.fillStyle = '#9cc3d6'; ctx.fillRect(-50, 0, 100, 36); ctx.strokeRect(-50, -40, 100, 76); ctx.fillStyle = C.amber; poly(ctx, [[0, -32], [-14, -6], [2, -6], [-6, 18], [16, -12], [0, -12]]); ctx.fill(); }
  ctx.restore();
}
function sDampak(ctx, t) {
  fill(ctx, '#f7ece2'); const ex = exitP(t, 'dampak'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'dampak', 'Rantai dampak El Niño di Indonesia', C.clayD);
  const items = [
    ['Hujan berkurang', 'terutama Juni–November', tw('berkurang', u(43).v0)],
    ['Kemarau panjang', 'lebih lama dan kering', u(44).v0],
    ['Gambut mengering', 'mudah terbakar', tw('gambut', u(45).v0)],
    ['Karhutla dan asap', 'kabut asap lintas negara', tw('kebakaran', u(45).v0)],
    ['Padi turun', 'harga beras naik', u(46).v0],
    ['Debit waduk turun', 'PLTA terganggu', u(47).v0],
  ];
  items.forEach(([a, b, t0], i) => {
    const k = sp(t, t0 - 0.1, SPRING.bouncy); if (k <= 0) return;
    const col = i % 3, row = Math.floor(i / 3), x = 110 + col * 580, y = 260 + row * 300;
    ctx.save(); ctx.translate(x + 260, y + 130); ctx.rotate((1 - k) * -0.5); ctx.translate(-(x + 260), -(y + 130)); ctx.globalAlpha *= clamp(k * 1.5);
    card(ctx, x, y, 520, 250, { r: 26 });
    circle(ctx, x + 40, y + 40, 22); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, `${i + 1}`, x + 40, y + 50, fU(26, 700), C.cream, 'center');
    impactIcon(ctx, i, x + 120, y + 145, t);
    text(ctx, a, x + 220, y + 130, fU(36, 700), C.ink); text(ctx, b, x + 220, y + 175, fU(26, 500), C.gray);
    ctx.restore();
    if (i < 5 && i % 3 !== 2) { const pa = ap(t, items[i + 1][2] - 0.15, 0.3); if (pa > 0) arrowLine(ctx, x + 524, y + 125, x + 524 + 52 * pa, y + 125, C.clay, 5, 16); }
  });
  ctx.restore();
}

function anomalyMap(ctx, t, box, sign, a, showBox = 0) {
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip();
  ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
  const P = mapProj(box, [100, 290, -32, 32]);
  if (a > 0) {
    const cx = P.PX(sign > 0 ? 235 : 220), cy = P.PY(0);
    ctx.save(); ctx.globalAlpha = a; ctx.translate(cx, cy); ctx.scale(1, 0.28);
    const r = (P.PX(240) - P.PX(170));
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, r);
    const col = sign > 0 ? [224, 98, 60] : [58, 120, 200];
    g.addColorStop(0, `rgba(${col},0.95)`); g.addColorStop(0.6, `rgba(${col},0.45)`); g.addColorStop(1, `rgba(${col},0)`);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  }
  drawRings(ctx, PAC, P, C.land, '#a8916a', 0.8);
  ctx.strokeStyle = 'rgba(27,50,43,0.35)'; ctx.setLineDash([8, 8]); ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(box.x, P.PY(0)); ctx.lineTo(box.x + box.w, P.PY(0)); ctx.stroke(); ctx.setLineDash([]);
  text(ctx, 'ekuator', box.x + 14, P.PY(0) - 8, fU(20, 700), C.gray);
  if (showBox > 0) {
    ctx.save(); ctx.globalAlpha = showBox;
    const x0 = P.PX(190), x1 = P.PX(240), y0 = P.PY(5), y1 = P.PY(-5);
    ctx.fillStyle = 'rgba(242,177,58,0.25)'; ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
    ctx.strokeStyle = C.clayD; ctx.lineWidth = 4; ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
    pill(ctx, 'Niño 3.4', (x0 + x1) / 2, y0 - 30, fU(26, 700), C.clayD, C.cream, 16, 44, 'center');
    text(ctx, '5° LU – 5° LS · 120° – 170° BB', (x0 + x1) / 2, y1 + 34, fU(22, 700), C.clayD, 'center');
    ctx.restore();
  }
  ctx.restore();
  return P;
}
function sPeru(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'peru'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const sw = ap(t, u(51).v0 - 0.2, 0.6, E.inOutCubic);
  if (sw < 1) {
    ctx.save(); ctx.globalAlpha *= 1 - sw;
    title(ctx, t, 'peru', 'Bagaimana dengan Peru?', C.blue);
    pacific(ctx, t, 1, { wind: 1, pool: 0, therm: 1, up: 1, conv: 0, sink: 0, walker: 0 });
    const r = ap(t, tw('hujan', u(50).v0), 0.5);
    if (r > 0) { cloud(ctx, 1640, 380, 1.1 * r, '#e6ebef'); rain(ctx, 1640, 410, 140, t, 6, C.blue, 22, 220, r); }
    const items = [[tw('dalam', u(49).v0), 'termoklin lebih dalam'], [tw('upwelling', u(49).v0), 'upwelling melemah'], [tw('tangkapan', u(49).v0), 'tangkapan ikan anjlok'], [tw('hujan', u(50).v0), 'hujan lebat di pesisir kering']];
    items.forEach(([t0, s], i) => { const p = ap(t, t0, 0.4); if (p > 0) { ctx.save(); ctx.globalAlpha *= p; pill(ctx, s, 140 + i * 430, 880, fU(28, 700), i === 3 ? C.blue : C.clayD, C.cream, 20, 54); ctx.restore(); } });
    ctx.restore();
  }
  if (sw > 0) {
    ctx.save(); ctx.globalAlpha *= sw;
    riseText(ctx, 'Anomali suhu muka laut', 110, 165, fD(76), C.clayD, sw);
    const box = { x: 110, y: 240, w: 1150, h: 480 };
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    const P = anomalyMap(ctx, t, box, 1, ap(t, tw('positif', u(54).v0) - 0.5, 1.2));
    const pf = ap(t, u(53).v0, 0.5);
    if (pf > 0) {
      ctx.save(); ctx.globalAlpha *= pf; card(ctx, 1300, 270, 520, 450, { r: 28, bg: C.forest });
      text(ctx, 'anomali =', 1340, 350, fU(40, 700), C.forest3);
      text(ctx, 'suhu saat ini', 1340, 400, fU(44, 700), C.cream);
      text(ctx, '− rata-rata normal', 1340, 460, fU(44, 700), C.cream);
      const pp = ap(t, tw('positif', u(54).v0), 0.4);
      if (pp > 0) { ctx.globalAlpha *= pp; pill(ctx, 'El Niño: anomali POSITIF', 1340, 560, fU(30, 700), C.clay, C.cream, 20, 56); text(ctx, 'Pasifik tengah–timur lebih hangat', 1340, 640, fU(26, 500), C.forest3); }
      ctx.restore();
    }
    if (ap(t, tw('positif', u(54).v0), 0.4) > 0) { text(ctx, '+ hangat', P.PX(235), P.PY(0) + 70, fU(28, 700), C.clayD, 'center'); }
    ctx.restore();
  }
  ctx.restore();
}

function sEnso(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'enso'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'enso', 'Satu sistem: ENSO');
  const box = { x: 110, y: 240, w: 1150, h: 480 };
  card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
  const P = anomalyMap(ctx, t, box, 1, 0.35);
  const pt = ap(t, tw('tahiti', u(61).v0) - 0.2, 0.4), pd = ap(t, tw('darwin', u(61).v0) - 0.2, 0.4);
  const osc = Math.sin(t * 1.4);
  const pin = (lon, lat, name, p, hi) => {
    if (p <= 0) return; const x = P.PX(lon), y = P.PY(lat);
    ctx.save(); ctx.globalAlpha *= p; circle(ctx, x, y, 12); ctx.fillStyle = C.clayD; ctx.fill();
    text(ctx, name, x, y + 44, fU(28, 700), C.ink, 'center');
    const bh = 70 + 40 * hi; rrect(ctx, x - 18, y - 30 - bh, 36, bh, 8); ctx.fillStyle = hi > 0 ? C.blue : C.clay; ctx.fill();
    text(ctx, hi > 0 ? 'T' : 'R', x, y - 40 - bh, fU(26, 700), C.ink, 'center');
    ctx.restore();
  };
  pin(210.6, -17.5, 'Tahiti', pt, osc); pin(130.8, -12.5, 'Darwin', pd, -osc);
  const pr = ap(t, tw('enso', u(62).v0), 0.5);
  if (pr > 0) {
    ctx.save(); ctx.globalAlpha *= pr;
    card(ctx, 1300, 270, 520, 450, { r: 28, bg: C.forest });
    text(ctx, 'LAUT', 1340, 320, fU(26, 700), C.forest3); text(ctx, 'El Niño / La Niña', 1340, 360, fU(40, 700), C.cream);
    text(ctx, '+', 1560, 420, fU(56, 700), C.amber, 'center');
    text(ctx, 'ATMOSFER', 1340, 470, fU(26, 700), C.forest3); text(ctx, 'Osilasi Selatan', 1340, 520, fU(40, 700), C.cream);
    rrect(ctx, 1340, 560, 440, 4, 2); ctx.fillStyle = C.amber; ctx.fill();
    text(ctx, '= ENSO', 1340, 640, fU(64, 700), C.amber);
    ctx.restore();
  }
  const pc = ap(t, u(63).v0, 0.5);
  if (pc > 0) {
    ctx.save(); ctx.globalAlpha *= pc;
    pill(ctx, 'berulang tidak teratur · tiap 2–7 tahun', 110, 800, fU(30, 700), C.clay, C.cream, 22, 58);
    ctx.strokeStyle = C.clay; ctx.lineWidth = 5; ctx.beginPath();
    for (let i = 0; i <= 200; i++) { const f = i / 200; const yy = 800 + Math.sin(f * 18 + Math.sin(f * 5) * 2) * 26; i ? ctx.lineTo(820 + f * 1000, yy) : ctx.moveTo(820, yy); }
    ctx.stroke(); ctx.restore();
  }
  ctx.restore();
}

const ONI = [[2010, -1.6], [2011, -1.0], [2012, 0.4], [2013, -0.4], [2014, 0.7], [2015, 2.6], [2016, -0.7], [2017, -1.0], [2018, 0.9], [2019, 0.7], [2020, -1.3], [2021, -1.0], [2022, -1.0], [2023, 2.0], [2024, -0.5]];
function oniChart(ctx, t, box, prog_, hl = 0, bands = 0) {
  const { x, y, w, h } = box; const y0 = y + h * 0.62, sc = h * 0.62 / 2.8;
  card(ctx, x - 8, y - 8, w + 16, h + 16, { r: 28 });
  if (bands > 0) {
    ctx.save(); ctx.globalAlpha = bands;
    [[0.5, 1.0, '#fde8d8', 'lemah'], [1.0, 1.5, '#fbd2b4', 'sedang'], [1.5, 2.0, '#f6b48a', 'kuat'], [2.0, 2.8, '#ee935f', 'sangat kuat']].forEach(([a, b, c, n]) => { ctx.fillStyle = c; ctx.fillRect(x + 90, y0 - b * sc, w - 120, (b - a) * sc); text(ctx, n, x + w - 40, y0 - (a + b) / 2 * sc + 8, fU(20, 700), C.clayD, 'right'); });
    ctx.fillStyle = '#d6e6f3'; ctx.fillRect(x + 90, y0 + 0.5 * sc, w - 120, 1.3 * sc);
    ctx.restore();
  }
  ctx.strokeStyle = C.gray; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x + 90, y0); ctx.lineTo(x + w - 30, y0); ctx.stroke();
  [0.5, -0.5].forEach((v) => { ctx.setLineDash([10, 8]); ctx.strokeStyle = v > 0 ? C.clay : C.blue; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x + 90, y0 - v * sc); ctx.lineTo(x + w - 30, y0 - v * sc); ctx.stroke(); ctx.setLineDash([]); text(ctx, (v > 0 ? '+0,5' : '−0,5'), x + 80, y0 - v * sc + 8, fU(22, 700), v > 0 ? C.clay : C.blue, 'right'); });
  text(ctx, 'ONI (°C)', x + 20, y + 36, fU(24, 700), C.gray);
  const bw = (w - 140) / ONI.length;
  ONI.forEach(([yr, v], i) => {
    const p = clamp(prog_ * ONI.length - i); if (p <= 0) return;
    const bx = x + 100 + i * bw, vv = v * E.outCubic(p);
    const col = v >= 0.5 ? C.clay : v <= -0.5 ? C.blue : '#b9c4bd';
    ctx.globalAlpha = hl > 0 && yr !== 2015 ? 1 - 0.6 * hl : 1;
    rrect(ctx, bx + 6, Math.min(y0, y0 - vv * sc), bw - 12, Math.abs(vv * sc), 6); ctx.fillStyle = col; ctx.fill();
    text(ctx, `${yr}`.slice(2), bx + bw / 2, y + h - 10, fU(20, 700), C.gray, 'center');
    if (yr === 2015 && hl > 0) { text(ctx, '+2,6', bx + bw / 2, y0 - vv * sc - 14, fU(30, 700), C.clayD, 'center'); }
    ctx.globalAlpha = 1;
  });
  text(ctx, 'puncak tahunan, disederhanakan (NOAA)', x + w - 30, y + 36, fU(18, 500), C.gray, 'right');
}
function sOni(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'oni'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'oni', 'Indeks ENSO: ONI');
  const sw = ap(t, u(68).v0 - 0.3, 0.6, E.inOutCubic);
  if (sw < 1) {
    ctx.save(); ctx.globalAlpha *= 1 - sw;
    const box = { x: 110, y: 240, w: 1700, h: 560 };
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    anomalyMap(ctx, t, box, 1, 0.25, ap(t, tw('nino', u(67).v0), 0.5));
    const pk = ap(t, u(66).v0, 0.4);
    if (pk > 0) { ctx.save(); ctx.globalAlpha *= pk; pill(ctx, 'ONI = Oceanic Niño Index', 140, 290, fU(30, 700), C.forest, C.cream, 22, 56); ctx.restore(); }
    const p3 = ap(t, tw('tiga', u(67).v0), 0.4);
    if (p3 > 0) { ctx.save(); ctx.globalAlpha *= p3; pill(ctx, 'anomali suhu rata-rata 3 bulanan', 140, 360, fU(28, 700), C.clay, C.cream, 20, 52); ctx.restore(); }
    ctx.restore();
  }
  if (sw > 0) {
    ctx.save(); ctx.globalAlpha *= sw;
    oniChart(ctx, t, { x: 110, y: 240, w: 1080, h: 600 }, ap(t, u(68).v0, 3.0, E.linear), ap(t, u(77).v0, 0.5), ap(t, u(72).v0, 0.6));
    const rules = [[u(69).v0, 'ONI +0,5 °C atau lebih', 'El Niño', C.clay, 'min. 5 periode berturut-turut'], [u(70).v0, 'ONI −0,5 °C atau kurang', 'La Niña', C.blue, ''], [u(71).v0, 'di antara −0,5 dan +0,5', 'Netral', C.gray, '']];
    rules.forEach(([t0, a, b, col, c], i) => {
      const p = sp(t, t0, SPRING.snappy); if (p <= 0) return;
      const y = 270 + i * 140; ctx.save(); ctx.globalAlpha *= clamp(p * 1.4); ctx.translate((1 - p) * 60, 0);
      card(ctx, 1230, y, 590, 122, { r: 24 }); rrect(ctx, 1230, y, 12, 122, 6); ctx.fillStyle = col; ctx.fill();
      text(ctx, a, 1270, y + 52, fU(32, 700), C.ink); text(ctx, '= ' + b, 1270, y + 98, fU(34, 700), col);
      if (c) text(ctx, c, 1560, y + 98, fU(18, 500), C.gray);
      ctx.restore();
    });
    const pf = ap(t, u(78).v0, 0.5);
    if (pf > 0) { ctx.save(); ctx.globalAlpha *= pf; card(ctx, 1230, 700, 590, 140, { r: 24, bg: C.clay }); text(ctx, '2015: ±2,6 juta ha', 1270, 765, fU(40, 700), C.cream); text(ctx, 'lahan terbakar (El Niño sangat kuat)', 1270, 810, fU(24, 500), C.cream); ctx.restore(); }
    ctx.restore();
  }
  ctx.restore();
}
function sSoi(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'soi'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'soi', 'Indeks kedua: SOI');
  const box = { x: 110, y: 240, w: 1100, h: 600 };
  card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
  const y0 = box.y + box.h / 2, gx = box.x + 80, gw = box.w - 140, sc = 90;
  ctx.strokeStyle = C.gray; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(gx, y0); ctx.lineTo(gx + gw, y0); ctx.stroke();
  const p = ap(t, SC.soi[0] + 0.4, 4, E.linear);
  const oni = (f) => 2.4 * Math.exp(-(((f - 0.45) / 0.15) ** 2)) - 0.9 * Math.exp(-(((f - 0.85) / 0.08) ** 2));
  const line = (fn, col) => { ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath(); for (let i = 0; i <= 200 * p; i++) { const f = i / 200; const yy = y0 - fn(f) * sc; i ? ctx.lineTo(gx + f * gw, yy) : ctx.moveTo(gx + f * gw, yy); } ctx.stroke(); };
  line(oni, C.clay); const ps = ap(t, tw('soi', u(81).v0) - 1, 0.5); if (ps > 0) { ctx.save(); ctx.globalAlpha = ps; line((f) => -0.85 * oni(f), C.forest); ctx.restore(); }
  text(ctx, 'ONI', gx + 10, box.y + 60, fU(28, 700), C.clay); if (ps > 0) text(ctx, 'SOI', gx + 90, box.y + 60, fU(28, 700), C.forest);
  text(ctx, 'ilustrasi pola 2014–2017', box.x + box.w - 30, box.y + 60, fU(20, 500), C.gray, 'right');
  const pk = ap(t, u(79).v0, 0.5);
  if (pk > 0) { ctx.save(); ctx.globalAlpha *= pk; card(ctx, 1260, 270, 560, 210, { r: 26, bg: C.forest }); text(ctx, 'SOI', 1300, 340, fU(52, 700), C.amber); text(ctx, 'selisih tekanan udara', 1300, 395, fU(30, 700), C.cream); text(ctx, 'Tahiti − Darwin', 1300, 440, fU(30, 700), C.cream); ctx.restore(); }
  const pw = sp(t, tw('terbalik', u(80).v0), SPRING.bouncy);
  if (pw > 0) {
    ctx.save(); ctx.translate(1540, 640); ctx.scale(pw, pw); card(ctx, -280, -150, 560, 300, { r: 28, bg: C.cream }); warnIcon(ctx, -200, -70, 40);
    text(ctx, 'Tandanya terbalik!', -130, -56, fU(34, 700), C.clayD);
    text(ctx, 'SOI negatif = El Niño', -240, 30, fU(36, 700), C.clay); text(ctx, 'SOI positif = La Niña', -240, 90, fU(36, 700), C.blue);
    ctx.restore();
  }
  ctx.restore();
}

function indianMap(ctx, t, box, state, a = 1) {
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip();
  ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
  const P = mapProj(box, [30, 140, -28, 22]);
  const blob = (lon, sign, k) => {
    if (k <= 0) return; const cx = P.PX(lon), cy = P.PY(-2), r = P.PX(lon + 18) - cx;
    ctx.save(); ctx.globalAlpha = k * a; ctx.translate(cx, cy); ctx.scale(1, 0.75);
    const col = sign > 0 ? [224, 98, 60] : [58, 120, 200];
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, r); g.addColorStop(0, `rgba(${col},0.85)`); g.addColorStop(1, `rgba(${col},0)`);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  };
  const s = state; // +1 positive IOD, -1 negative
  blob(60, s >= 0 ? 1 : -1, Math.abs(s)); blob(100, s >= 0 ? -1 : 1, Math.abs(s));
  drawRings(ctx, IP, P, C.land, '#a8916a', 0.8);
  ctx.setLineDash([10, 8]); ctx.lineWidth = 3;
  [[50, 70, 10, -10, 'BARAT'], [90, 110, 0, -10, 'TIMUR']].forEach(([a0, a1, b0, b1, n]) => { ctx.strokeStyle = C.forest; ctx.strokeRect(P.PX(a0), P.PY(b0), P.PX(a1) - P.PX(a0), P.PY(b1) - P.PY(b0)); text(ctx, n, (P.PX(a0) + P.PX(a1)) / 2, P.PY(b1) + 30, fU(22, 700), C.forest, 'center'); });
  ctx.setLineDash([]);
  text(ctx, 'Afrika Timur', P.PX(38), P.PY(6), fU(22, 700), C.ink, 'center'); text(ctx, 'Sumatra', P.PX(100), P.PY(5.5), fU(22, 700), C.ink, 'center');
  text(ctx, 'SAMUDRA HINDIA', P.PX(78), P.PY(-20), fU(26, 700), C.blue, 'center');
  if (Math.abs(s) > 0.2) { const cx = P.PX(s > 0 ? 55 : 100); cloud(ctx, cx, P.PY(10), 0.9 * Math.abs(s), '#ffffff'); rain(ctx, cx, P.PY(10) + 30, 120, t, 6, C.blue, 20, 220, Math.abs(s)); }
  ctx.restore();
  return P;
}
function sIod(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'iod'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'iod', 'Samudra Hindia: Indian Ocean Dipole (IOD)');
  const box = { x: 110, y: 240, w: 1150, h: 560 };
  card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
  const s = ap(t, u(85).v0, 1.2, E.inOutCubic) - 2 * ap(t, u(89).v0 + 0.5, 1.6, E.inOutCubic);
  indianMap(ctx, t, box, s);
  const pk = ap(t, tw('dmi', u(84).v0) - 0.3, 0.4);
  if (pk > 0) { ctx.save(); ctx.globalAlpha *= pk; pill(ctx, 'Indeks: DMI (Dipole Mode Index)', 140, 290, fU(28, 700), C.forest, C.cream, 20, 52); ctx.restore(); }
  const panel = (y, head, col, lines, p) => {
    if (p <= 0) return; ctx.save(); ctx.globalAlpha *= p; ctx.translate((1 - p) * 60, 0);
    card(ctx, 1300, y, 520, 265, { r: 26 }); rrect(ctx, 1300, y, 12, 265, 6); ctx.fillStyle = col; ctx.fill();
    text(ctx, head, 1336, y + 56, fU(36, 700), col);
    lines.forEach((l, i) => text(ctx, l, 1336, y + 110 + i * 44, fU(26, 500), C.ink));
    ctx.restore();
  };
  panel(270, 'IOD POSITIF', C.clay, ['barat Sumatra lebih DINGIN', 'Hindia barat lebih hangat', 'Indonesia barat: hujan berkurang', 'Afrika Timur: banjir'], ap(t, u(85).v0, 0.5));
  panel(555, 'IOD NEGATIF', C.blue, ['barat Sumatra lebih HANGAT', 'Indonesia barat: hujan bertambah', '', ''], ap(t, u(89).v0, 0.5));
  const pc = ap(t, u(91).v0, 0.5);
  if (pc > 0) {
    ctx.save(); ctx.globalAlpha *= pc;
    const x0 = 140, y = 870, cw = 92; ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'].forEach((m, i) => { rrect(ctx, x0 + i * cw, y - 26, cw - 8, 52, 10); ctx.fillStyle = i >= 8 && i <= 10 ? C.clay : C.sand2; ctx.fill(); text(ctx, m, x0 + i * cw + cw / 2 - 4, y + 10, fU(24, 700), i >= 8 && i <= 10 ? C.cream : C.gray, 'center'); });
    text(ctx, 'puncak IOD: September–November', x0 + 12 * cw + 20, y + 10, fU(28, 700), C.clayD);
    ctx.restore();
  }
  ctx.restore();
}

function sWilayah(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'wilayah'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'wilayah', 'Siapa memengaruhi wilayah mana?');
  const box = { x: 110, y: 240, w: 1700, h: 560 };
  card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip(); ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
  const P = mapProj(box, [88, 148, -14, 10.5]);
  const pe = ap(t, tw('enso', u(93).v0), 0.6), pi = ap(t, tw('iod', u(94).v0), 0.6);
  for (const [c, rings] of Object.entries(IND)) {
    for (const r of rings) {
      const cl = r.reduce((s, q) => s + q[0], 0) / r.length;
      let col = c === 'IDN' ? C.land : '#e7e3da';
      if (c === 'IDN') { const wE = clamp((cl - 108) / 10) * pe, wI = clamp((112 - cl) / 8) * pi; col = mix(mix(C.land, '#9cc3e6', wE), '#f2b48c', wI); }
      ctx.fillStyle = col; ctx.strokeStyle = '#a8916a'; ctx.lineWidth = 1;
      ctx.beginPath(); r.forEach(([lo, la], i) => (i ? ctx.lineTo(P.PX(lo), P.PY(la)) : ctx.moveTo(P.PX(lo), P.PY(la)))); ctx.closePath(); ctx.fill(); ctx.stroke();
    }
  }
  if (pi > 0) { ctx.save(); ctx.globalAlpha = pi; arrowLine(ctx, P.PX(90), P.PY(-9), P.PX(101), P.PY(-4), C.clay, 8, 30); pill(ctx, 'IOD · Samudra Hindia', P.PX(91), P.PY(-11.5), fU(28, 700), C.clay, C.cream, 18, 50); text(ctx, 'Indonesia barat', P.PX(102), P.PY(3), fU(28, 700), C.clayD, 'center'); ctx.restore(); }
  if (pe > 0) { ctx.save(); ctx.globalAlpha = pe; arrowLine(ctx, P.PX(146), P.PY(6), P.PX(134), P.PY(1), C.blue, 8, 30); pill(ctx, 'ENSO · Pasifik', P.PX(146), P.PY(8.5), fU(28, 700), C.blue, C.cream, 18, 50, 'right'); text(ctx, 'Indonesia tengah–timur', P.PX(128), P.PY(-10), fU(28, 700), C.blue, 'center'); ctx.restore(); }
  ctx.restore();
  const pt = ap(t, tw('telekoneksi', u(95).v0) - 0.3, 0.4);
  if (pt > 0) { ctx.save(); ctx.globalAlpha *= pt; pill(ctx, 'Pengaruh jarak jauh = TELEKONEKSI', W / 2, 880, fU(34, 700), C.forest, C.cream, 30, 64, 'center'); ctx.restore(); }
  ctx.restore();
}

function sKombinasi(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'kombinasi'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'kombinasi', 'Kalau keduanya terjadi bersamaan');
  const x0 = 460, y0 = 300, cw = 660, ch = 250;
  const ph = ap(t, SC.kombinasi[0] + 0.3, 0.5);
  ctx.save(); ctx.globalAlpha *= ph;
  text(ctx, 'IOD positif', x0 + cw / 2, y0 - 24, fU(34, 700), C.clay, 'center'); text(ctx, 'IOD negatif', x0 + cw * 1.5 + 20, y0 - 24, fU(34, 700), C.blue, 'center');
  text(ctx, 'El Niño', x0 - 30, y0 + ch / 2 + 12, fU(40, 700), C.clay, 'right'); text(ctx, 'La Niña', x0 - 30, y0 + ch * 1.5 + 32, fU(40, 700), C.blue, 'right');
  ctx.restore();
  const cells = [
    [0, 0, ap(t, u(97).v0, 0.5), '#f1b08a', 'Kemarau SANGAT parah', '2015 · 2019 · 2023', C.clayD],
    [1, 1, ap(t, u(99).v0, 0.5), '#a9cdec', 'Hujan BERLEBIH', '2010 · 2016 · 2022', C.blue],
    [1, 0, ap(t, u(99).v1 - 1, 0.5), '#e7e3da', 'Saling melemahkan', 'dampak tidak sekuat kombinasi searah', C.gray],
    [0, 1, ap(t, u(99).v1 - 1, 0.5), '#e7e3da', 'Saling melemahkan', 'dampak tidak sekuat kombinasi searah', C.gray],
  ];
  cells.forEach(([c, r, p, bg, a, b, col]) => {
    if (p <= 0) return; const x = x0 + c * (cw + 20), y = y0 + r * (ch + 20);
    ctx.save(); ctx.globalAlpha *= p; ctx.translate(x + cw / 2, y + ch / 2); ctx.scale(0.9 + 0.1 * p, 0.9 + 0.1 * p); ctx.translate(-(x + cw / 2), -(y + ch / 2));
    card(ctx, x, y, cw, ch, { r: 26, bg });
    text(ctx, a, x + 40, y + 110, fU(46, 700), col); text(ctx, b, x + 40, y + 170, fU(30, 700), C.ink);
    ctx.restore();
  });
  ctx.restore();
}

function sMjo(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'mjo'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'mjo', 'Madden–Julian Oscillation (MJO)');
  const box = { x: 110, y: 250, w: 1700, h: 430 };
  card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 24); ctx.clip(); ctx.fillStyle = C.sea; ctx.fillRect(box.x, box.y, box.w, box.h);
  const P = mapProj(box, [20, 200, -26, 26]);
  drawRings(ctx, IP, P, C.land, '#a8916a', 0.8);
  const phases = [[1, 15, 35], [2, 55, 65], [3, 65, 85], [4, 85, 115], [5, 115, 135], [6, 135, 155], [7, 155, 175], [8, 175, 198]];
  const pp = ap(t, tw('delapan', u(102).v0) - 0.2, 0.6), hl = ap(t, tw('empat', u(103).v0), 0.5);
  if (pp > 0) phases.forEach(([n, a, b], i) => {
    const k = clamp(pp * 8 - i); if (k <= 0) return;
    const on = hl > 0 && (n === 4 || n === 5);
    ctx.save(); ctx.globalAlpha = k * (on ? 0.4 : 0.15); ctx.fillStyle = on ? C.clay : C.forest; ctx.fillRect(P.PX(a), box.y, P.PX(b) - P.PX(a), box.h); ctx.restore();
    ctx.save(); ctx.globalAlpha = k; text(ctx, `${n}`, (P.PX(a) + P.PX(b)) / 2, box.y + 46, fU(36, 700), on ? C.clayD : C.forest, 'center'); ctx.restore();
  });
  const pc = ap(t, u(101).v0, 0.5);
  if (pc > 0) {
    const lon = 30 + ((t - u(101).v0) * 9) % 165; const cx = P.PX(lon), cy = P.PY(0);
    ctx.save(); ctx.globalAlpha = pc;
    for (let k = 0; k < 4; k++) cloud(ctx, cx - 60 + k * 40, cy - 20 + (k % 2) * 30, 0.9, '#ffffff', '#4a6577');
    rain(ctx, cx, cy + 20, 180, t, 8, C.blue, 22, 240, 0.9);
    arrowLine(ctx, cx + 120, cy + 80, cx + 220, cy + 80, C.clay, 7, 24);
    text(ctx, 'merambat ke timur', cx + 230, cy + 88, fU(26, 700), C.clayD);
    ctx.restore();
  }
  text(ctx, 'Samudra Hindia', P.PX(70), box.y + box.h - 24, fU(24, 700), C.blue, 'center'); text(ctx, 'Benua Maritim', P.PX(118), box.y + box.h - 24, fU(24, 700), C.ink, 'center'); text(ctx, 'Pasifik', P.PX(170), box.y + box.h - 24, fU(24, 700), C.blue, 'center');
  ctx.restore();
  const facts = [[tw('tiga', u(101).v0), 'periode 30–60 hari', C.forest], [tw('delapan', u(102).v0), '8 fase', C.forest], [tw('empat', u(103).v0), 'fase 4–5 di Indonesia: hujan lebat 1–2 minggu, lalu lebih kering', C.clay]];
  let x = 110; facts.forEach(([t0, s, col]) => { const p = ap(t, t0, 0.4); if (p > 0) { ctx.save(); ctx.globalAlpha *= p; x += pill(ctx, s, x, 760, fU(30, 700), col, C.cream, 22, 60) + 20; ctx.restore(); } else { ctx.font = fU(30, 700); x += ctx.measureText(s).width + 64; } });
  ctx.restore();
}

function sSkala(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'skala'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  title(ctx, t, 'skala', 'Susun berdasarkan skala waktu');
  const rows = [['MJO', '30–60 hari', 0.16, C.amber, u(106).v0], ['Monsun', '±6 bulan (musiman)', 0.3, C.forestL, u(105).v0], ['IOD', 'tahunan (puncak Sep–Nov)', 0.45, C.clay, u(107).v0], ['ENSO', '2–7 tahun', 0.68, C.blue, u(108).v0], ['Perubahan iklim', 'puluhan tahun', 1.0, C.forest, u(109).v0]];
  rows.forEach(([n, s, f, col, t0], i) => {
    const p = ap(t, t0, 0.7, E.outCubic); if (p <= 0) return;
    const y = 260 + i * 120;
    ctx.save(); ctx.globalAlpha *= clamp(p * 2);
    text(ctx, n, 110, y + 52, fU(40, 700), C.ink);
    rrect(ctx, 520, y + 14, 1200 * f * p, 56, 16); ctx.fillStyle = col; ctx.fill();
    text(ctx, s, 540, y + 54, fU(30, 700), col === C.amber ? C.ink : C.cream);
    ctx.restore();
  });
  text(ctx, 'skala ilustratif (bukan proporsional)', 1810, 900, fU(20, 500), C.gray, 'right');
  ctx.restore();
}

const OPTS = ['Papua bagian utara, karena ONI positif menambah hujan di Pasifik barat', 'Seluruh Indonesia mengalami hujan di atas normal',
  'Sumatra bagian selatan, Jawa, Kalimantan bagian selatan, dan Nusa Tenggara', 'Hanya Afrika Timur, karena IOD positif tidak memengaruhi Indonesia', 'Tidak ada, karena nilai ONI dan DMI masih tergolong netral'];
function sSoal(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'soal'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const [tp0, tp1] = T.tm.pause;
  const dock = ap(t, u(111).v0 - 0.3, 0.7, E.inOutCubic);
  const correct = ap(t, tw('jawabannya', u(117).v0), 0.3);
  const Q = 'Pada Agustus–Oktober suatu tahun, BMKG melaporkan ONI +1,2 °C dan DMI +0,9 °C. Wilayah yang paling berisiko mengalami kekeringan ekstrem adalah …';
  const pq = sp(t, SC.soal[0] + 0.3, SPRING.snappy);
  const opt = (i, ox, oy, ow, oh, fs) => {
    const on = i === 2 && correct > 0; ctx.save(); ctx.globalAlpha *= correct > 0 && i !== 2 ? 0.35 : 1;
    rrect(ctx, ox, oy, ow, oh, 16); ctx.fillStyle = on ? C.clay : C.sand; ctx.fill();
    circle(ctx, ox + oh * 0.5, oy + oh / 2, oh * 0.3); ctx.fillStyle = on ? C.cream : C.forest; ctx.fill();
    text(ctx, 'ABCDE'[i], ox + oh * 0.5, oy + oh / 2 + fs * 0.36, fU(fs * 0.9, 700), on ? C.clay : C.cream, 'center');
    const ls = wrap(ctx, OPTS[i], fU(fs, 600), ow - oh - 30);
    ls.slice(0, 2).forEach((l, k) => text(ctx, l, ox + oh + 10, oy + oh / 2 + fs * 0.36 + (k - (ls.length > 1 ? 0.5 : 0)) * fs * 1.15, fU(fs, 600), on ? C.cream : C.ink));
    ctx.restore();
  };
  if (pq > 0 && dock < 1) {
    ctx.save(); ctx.globalAlpha *= clamp(pq * 1.5) * (1 - dock); ctx.translate(210, 120 + (1 - pq) * 80);
    card(ctx, 0, 0, 1500, 790, { r: 32 });
    pill(ctx, 'CONTOH SOAL OSN', 50, 64, fU(28, 700), C.clay, C.cream, 22, 54);
    wrap(ctx, Q, fU(38, 500), 1400).forEach((l, i) => text(ctx, l, 50, 160 + i * 52, fU(38, 500), C.ink));
    OPTS.forEach((o, i) => opt(i, 50, 300 + i * 92, 1400, 80, 28));
    ctx.restore();
  }
  if (t > tp0 - 0.2 && t < tp1 + 0.4) {
    const a = 1 - ap(t, tp1, 0.35), p = clamp((t - tp0) / (tp1 - tp0));
    ctx.save(); ctx.globalAlpha *= a * ap(t, tp0 - 0.2, 0.3);
    const cx = 1790, cy = 150; circle(ctx, cx, cy + 60, 76); ctx.fillStyle = C.forest; ctx.fill();
    ctx.strokeStyle = C.amber; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy + 60, 60, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - p)); ctx.stroke();
    text(ctx, `${Math.max(1, Math.ceil((tp1 - tp0) - (t - tp0)))}`, cx, cy + 86, fU(70, 700), C.cream, 'center');
    ctx.restore();
  }
  if (dock > 0) {
    ctx.save(); ctx.globalAlpha *= dock;
    card(ctx, 80, 130, 860, 790, { r: 30 });
    pill(ctx, 'CONTOH SOAL OSN', 120, 186, fU(24, 700), C.clay, C.cream, 20, 48);
    wrap(ctx, Q, fU(29, 500), 780).forEach((l, i) => text(ctx, l, 120, 260 + i * 40, fU(29, 500), C.ink));
    OPTS.forEach((o, i) => opt(i, 120, 440 + i * 92, 780, 84, 24));
    card(ctx, 990, 130, 850, 790, { r: 30, bg: C.forest });
    const steps = [
      [u(111).v0, 'ONI +1,2 °C', C.amber, 50], [tw('berarti', u(112).v0), 'El Niño, kategori sedang', C.cream, 38],
      [u(113).v0, 'DMI +0,9 °C  →  IOD positif', C.amber, 40], [u(114).v0, 'keduanya mengurangi hujan', C.cream, 34],
      [u(115).v0, 'IOD+ : Indonesia barat', C.cream, 34], [tw('el', u(115).v0), 'El Niño : Indonesia tengah–timur', C.cream, 34],
      [u(116).v0 + 2, 'Sumsel, Jawa, Kalsel, Nusa Tenggara', C.amber, 36],
    ];
    let y = 220; steps.forEach(([t0, s, col, size]) => { const p = ap(t, t0, 0.5, E.outQuint); if (p > 0) { ctx.save(); ctx.beginPath(); ctx.rect(1010, y - size - 10, 810, size + 30); ctx.clip(); text(ctx, s.replace('→', '›'), 1040, y + (1 - p) * (size + 30), fU(size, 700), col); ctx.restore(); } y += size + 48; });
    const pk = ap(t, tw('jawabannya', u(117).v0), 0.4);
    if (pk > 0) { ctx.globalAlpha *= pk; pill(ctx, 'Jawaban: C', 1415, 860, fU(36, 700), C.clay, C.cream, 30, 64, 'center'); }
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
    [u(119).v0, 'El Niño: Pasifik timur hangat, Indonesia ikut basah', 'El Niño: Pasifik timur hangat, Indonesia justru KERING', tw('kering', u(119).v0)],
    [u(121).v0, 'SOI negatif = La Niña', 'SOI negatif = EL NIÑO', tw('bukan', u(121).v0)],
    [u(122).v0, 'IOD positif: barat Sumatra lebih hangat', 'IOD positif: barat Sumatra lebih DINGIN', tw('dingin', u(122).v0)],
  ];
  items.forEach(([t0, wrong, right, tfix], i) => {
    const p = sp(t, t0, SPRING.snappy); if (p <= 0) return;
    const y = 260 + i * 210; ctx.save(); ctx.globalAlpha *= clamp(p * 1.5); ctx.translate((1 - p) * 80, 0);
    card(ctx, 110, y, 1700, 180, { r: 26 });
    text(ctx, `${i + 1}`, 170, y + 110, fU(70, 700), C.clay, 'center');
    const f = ap(t, tfix - 0.4, 0.4);
    text(ctx, wrong, 250, y + 72, fU(34, 600), f > 0 ? 'rgba(152,63,41,0.6)' : C.clayD);
    if (f > 0) { ctx.strokeStyle = C.clay; ctx.lineWidth = 5; ctx.font = fU(34, 600); const w = ctx.measureText(wrong).width; ctx.beginPath(); ctx.moveTo(250, y + 60); ctx.lineTo(250 + w * f, y + 60); ctx.stroke(); }
    if (f > 0) { ctx.save(); ctx.globalAlpha *= f; circle(ctx, 280, y + 130, 22); ctx.fillStyle = C.forest; ctx.fill(); check(ctx, 280, y + 130, 26, C.cream, f); text(ctx, right, 320, y + 142, fU(36, 700), C.forest); ctx.restore(); }
    ctx.restore();
  });
  ctx.restore();
}

const RECAP = ['Variabilitas iklim', 'Angin pasat', 'Kolam air hangat', 'Termoklin', 'Upwelling', 'Konveksi', 'Sirkulasi Walker', 'El Niño', 'La Niña',
  'Anomali suhu muka laut', 'Osilasi Selatan', 'ENSO', 'ONI', 'Niño 3.4', 'SOI', 'IOD dan DMI', 'Telekoneksi', 'MJO'];
function sKamus(ctx, t) {
  fill(ctx, C.forestD); const ex = exitP(t, 'kamus'); const u = (i) => U_(i);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  ctx.save(); ctx.globalAlpha *= 0.06; ctx.strokeStyle = C.cream; for (let x = 0; x < W; x += 80) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); } ctx.restore();
  ctx.save(); ctx.globalAlpha *= ap(t, SC.kamus[0] + 0.05, 0.5); pill(ctx, 'KAMUS ISTILAH OSN', 110, 120, fU(30, 700), C.clay, C.cream, 24, 58); ctx.restore();
  riseText(ctx, '18 istilah yang wajib kamu kuasai', 110, 225, fD(76), C.cream, ap(t, SC.kamus[0] + 0.2, 0.5, E.outQuint));
  const all = ap(t, u(142).v0, 0.6);
  RECAP.forEach((s, i) => {
    const t0 = U_(124 + i).v0; const k = sp(t, t0 - 0.05, SPRING.snappy);
    const col = i % 3, row = Math.floor(i / 3), x = 110 + col * 575, y = 270 + row * 106;
    const on = k > 0;
    ctx.save(); ctx.globalAlpha *= on ? 1 : 0.25;
    rrect(ctx, x, y, 545, 90, 18); ctx.fillStyle = on ? (bump(t, t0 + 0.4, 0.8) > 0.2 ? C.clay : 'rgba(255,254,250,0.1)') : 'rgba(255,254,250,0.05)'; ctx.fill();
    text(ctx, `${i + 1}`, x + 46, y + 58, fU(30, 700), on ? C.amber : C.forest3, 'center');
    text(ctx, s, x + 90, y + 58, fU(34, 700), C.cream);
    if (all > 0) check(ctx, x + 505, y + 45, 34, C.amber, all);
    ctx.restore();
  });
  ctx.restore();
}

// ---------------------------------------------------------------- hits
function addHits() {
  const u = (i) => U_(i);
  SCN.forEach(([n], i) => { if (i > 0 && n !== 'outro') hit(SC[n][0] + 0.2, 'scene ' + n, 'whoosh', { len: 0.4, gain: 0.25 }); });
  TERMS.forEach(([s, , ui]) => hit(U_(ui).v0, 'term ' + s, 'pop', { pitch: 'A5', gain: 0.35 }));
  hit(u(41).v0, 'EL NINO', 'impact', { gain: 0.25 });
  ['berkurang', 'kemarau', 'gambut', 'kebakaran', 'padi', 'debit'].forEach((w, i) => hit(tw(w, u(43).v0) - 0.1, 'dampak ' + i, 'tok', { pitch: 420 + i * 60, gain: 0.35 }));
  const [p0, p1] = T.tm.pause; for (let k = 0; k < 4; k++) hit(p0 + k, 'timer ' + k, 'blip', { pitch: 880, gain: 0.22 });
  hit(tw('jawabannya', u(117).v0), 'answer', 'bell', { pitch: 'E6', gain: 0.4 });
  RECAP.forEach((s, i) => hit(U_(124 + i).v0 - 0.05, 'recap ' + i, 'click', { gain: 0.25 }));
  hit(SC.outro[0] + 0.2, 'logo', 'bell', { pitch: 'D6', gain: 0.4 });
  HITS.sort((a, b) => a[0] - b[0]);
}

const DRAW = { hook: sHook, peta: sPeta, normal: sNormal, elnino: sElnino, dampak: sDampak, peru: sPeru, lanina: sLanina, enso: sEnso, oni: sOni,
  soi: sSoi, iod: sIod, wilayah: sWilayah, kombinasi: sKombinasi, mjo: sMjo, skala: sSkala, soal: sSoal, jebakan: sJebakan, kamus: sKamus };

M.film({
  fonts: [M.font(100, 400, 'Display'), M.font(40, 500, 'UI'), M.font(40, 700, 'UI')],
  hits: HITS,
  samples: () => 3,
  async init() {
    T.tm = await fetch('timing.json').then((r) => r.json());
    [PAC, IND, IP] = await Promise.all(['assets/pacific.json', 'assets/indo.json', 'assets/indo_pac.json'].map((p) => fetch(p).then((r) => r.json())));
    buildScenes(); buildCaps(); addHits();
  },
  draw(ctx, u, t) {
    const S = Object.keys(SC).find((k) => t >= SC[k][0] && t < SC[k][1]) || 'outro';
    if (S === 'intro') intro(ctx, t, 'BAB 1 · IKLIM · SANGAT SERING MUNCUL', 'El Niño, La Niña, dan IOD', '+ MJO dan 18 istilah penting OSN');
    else if (S === 'outro') outro(ctx, t, SC.outro[0], tw('menu', SC.outro[0]), 'Menu Soal Pendalaman Materi  ·  Bab 1', 'B01-V02 · Efek Rumah Kaca dan Pemanasan Global');
    else DRAW[S](ctx, t);
    if (S !== 'intro' && S !== 'outro') { centerMark(ctx, S === 'kamus' ? 0.9 : 1, S === 'kamus' ? C.cream : C.forest); termCard(ctx, t); }
    lowerThird(ctx, t, 'OSNGEO.id  ·  Bab 1 Iklim  ·  B01-V01');
    if (S !== 'intro') captions(ctx, t);
    cornerMark(ctx);
  },
});
