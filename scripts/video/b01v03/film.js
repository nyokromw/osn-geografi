// B01-02 · Atmosfer Bumi · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud } from './lib/common.js';
import { run, SC, u, title, show, scene, fI, sup } from './lib/kit.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 268.5;

// ---------------------------------------------------------------- props
function mountain(ctx, x, y, w, h, col = '#8a7a6a', snow = true) {
  ctx.fillStyle = col; poly(ctx, [[x - w / 2, y], [x - w * 0.12, y - h * 0.8], [x, y - h], [x + w * 0.15, y - h * 0.75], [x + w / 2, y]]); ctx.fill();
  if (snow) { ctx.fillStyle = '#fff'; poly(ctx, [[x - w * 0.08, y - h * 0.86], [x, y - h], [x + w * 0.07, y - h * 0.87], [x + w * 0.02, y - h * 0.83]]); ctx.fill(); }
}
function person(ctx, x, y, s, col = C.clayD) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.strokeStyle = col; ctx.fillStyle = col; ctx.lineWidth = 6; ctx.lineCap = 'round';
  circle(ctx, 0, -62, 11); ctx.fill(); ctx.beginPath(); ctx.moveTo(0, -50); ctx.lineTo(0, -20); ctx.moveTo(0, -20); ctx.lineTo(-12, 0); ctx.moveTo(0, -20); ctx.lineTo(12, 0); ctx.moveTo(0, -42); ctx.lineTo(16, -28); ctx.moveTo(0, -42); ctx.lineTo(-14, -30); ctx.stroke();
  ctx.fillStyle = C.amber; rrect(ctx, -16, -50, 12, 24, 4); ctx.fill(); ctx.restore();
}
function plane(ctx, x, y, s, col = '#ffffff') {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.ellipse(0, 0, 60, 9, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  poly(ctx, [[-5, 0], [-30, 38], [-14, 38], [22, 2]]); ctx.fill(); ctx.stroke();
  poly(ctx, [[-5, 0], [-30, -38], [-14, -38], [22, -2]]); ctx.fill(); ctx.stroke();
  poly(ctx, [[-48, 0], [-62, -22], [-54, -22], [-38, -2]]); ctx.fill(); ctx.stroke(); ctx.restore();
}
function aurora(ctx, x, y, w, h, t, a = 1) {
  ctx.save(); ctx.globalAlpha *= a;
  for (let k = 0; k < 3; k++) {
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(120,255,170,0)'); g.addColorStop(0.55, `rgba(90,240,150,${0.55 - k * 0.12})`); g.addColorStop(1, 'rgba(60,200,140,0)');
    ctx.fillStyle = g; ctx.beginPath();
    for (let i = 0; i <= 40; i++) { const xx = x + w * i / 40, yy = y + 30 * Math.sin(i * 0.35 + t * 0.9 + k) + k * 20; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }
    for (let i = 40; i >= 0; i--) { const xx = x + w * i / 40, yy = y + h + 20 * Math.sin(i * 0.3 + t * 0.7 + k); ctx.lineTo(xx, yy); }
    ctx.closePath(); ctx.fill();
  }
  ctx.restore();
}
function stars(ctx, x, y, w, h, n = 40) { ctx.fillStyle = 'rgba(255,255,255,0.8)'; for (let i = 0; i < n; i++) { circle(ctx, x + hash01(i, 3) * w, y + hash01(i, 5) * h, 1 + hash01(i, 7) * 2); ctx.fill(); } }
function meteor(ctx, x, y, len, a = 1) {
  ctx.save(); ctx.globalAlpha *= a; const g = ctx.createLinearGradient(x, y, x - len, y - len * 0.6); g.addColorStop(0, '#fff3c4'); g.addColorStop(1, 'rgba(255,200,120,0)');
  ctx.strokeStyle = g; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - len, y - len * 0.6); ctx.stroke(); circle(ctx, x, y, 5); ctx.fillStyle = '#fff'; ctx.fill(); ctx.restore();
}
function cbCloud(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = '#ffffff'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(-30, 0); ctx.lineTo(-22, -150); ctx.lineTo(-110, -178); ctx.lineTo(-100, -200); ctx.lineTo(110, -200); ctx.lineTo(120, -178); ctx.lineTo(26, -150); ctx.lineTo(34, 0); ctx.closePath(); ctx.fill(); ctx.stroke();
  [[-40, -10, 30], [0, -30, 36], [40, -8, 30], [-10, -80, 30], [12, -120, 26]].forEach(([a, b, r]) => { circle(ctx, a, b, r); ctx.fill(); });
  ctx.restore();
}

// ---------------------------------------------------------------- hook
const hook = {
  cards: [
    [2, 'Puncak Rinjani', 'sesak napas, padahal udaranya bersih', (ctx, x, y, t) => { ctx.fillStyle = '#cfe3ef'; ctx.fillRect(x, y, 560, 460); mountain(ctx, x + 280, y + 440, 520, 330); person(ctx, x + 278, y + 120, 0.9); for (let k = 0; k < 3; k++) { const ph = (t * 0.8 + k / 3) % 1; ctx.save(); ctx.globalAlpha = 0.7 * (1 - ph); circle(ctx, x + 310 + ph * 50, y + 50 - ph * 30, 6 + ph * 12); ctx.strokeStyle = C.blue; ctx.lineWidth = 3; ctx.stroke(); ctx.restore(); } }, '#cfe3ef'],
    [3, 'Pesawat jet', 'sengaja terbang di ±10 km', (ctx, x, y, t) => { const g = ctx.createLinearGradient(0, y, 0, y + 460); g.addColorStop(0, '#2c5f8a'); g.addColorStop(1, '#a9cde3'); ctx.fillStyle = g; ctx.fillRect(x, y, 560, 460); [[120, 360], [300, 390], [460, 350]].forEach(([a, b]) => cloud(ctx, x + a, y + b, 1.3)); plane(ctx, x + 150 + ((t * 40) % 300), y + 160, 1.4); text(ctx, '±10 km', x + 400, y + 90, fU(38, 700), '#fff'); }],
    [4, 'Langit kutub', 'cahaya hijau yang menari', (ctx, x, y, t) => { ctx.fillStyle = '#0d1b2a'; ctx.fillRect(x, y, 560, 460); stars(ctx, x, y, 560, 300); aurora(ctx, x, y + 60, 560, 240, t); ctx.fillStyle = '#e9f1f5'; poly(ctx, [[x, y + 460], [x, y + 390], [x + 200, y + 360], [x + 380, y + 400], [x + 560, y + 370], [x + 560, y + 460]]); ctx.fill(); }],
  ],
  punch: [6, 'atmosfer bumi'],
};

// ---------------------------------------------------------------- komposisi
function sKomposisi(ctx, t) {
  scene(ctx, t, 'komposisi', C.sand, () => {
    title(ctx, t, 'komposisi', 'Isi atmosfer: udara kering');
    const rows = [['Nitrogen', 'N', '2', 78, 'nitrogen', C.forest], ['Oksigen', 'O', '2', 21, 'oksigen', C.blue], ['Argon', 'Ar', '', 0.93, 'argon', C.gray], ['Karbon dioksida', 'CO', '2', 0.04, 'karbon', C.clay]];
    rows.forEach(([n, a, b, v, w, col], i) => {
      const t0 = tw(w, u(8).v0); const p = ap(t, t0, 0.9, E.outCubic); if (p <= 0) return;
      const y = 280 + i * 120;
      ctx.save(); ctx.globalAlpha *= clamp(p * 2);
      text(ctx, n, 110, y + 50, fU(34, 700), C.ink);
      rrect(ctx, 470, y + 10, 900, 60, 14); ctx.fillStyle = '#ece3d3'; ctx.fill();
      const len = Math.max(14, 900 * v / 80) * p; rrect(ctx, 470, y + 10, len, 60, 14); ctx.fillStyle = col; ctx.fill();
      text(ctx, `${(v * (p > 0.98 ? 1 : p)).toFixed(v < 1 ? 2 : 0).replace('.', ',')}%`, 490 + len, y + 54, fU(36, 700), col);
      ctx.restore();
    });
    show(ctx, t, u(9).v0, () => {
      const y = 760; const v = 2 + 2 * Math.sin(t * 1.3);
      text(ctx, 'Uap air', 110, y + 50, fU(34, 700), C.ink);
      rrect(ctx, 470, y + 10, 900, 60, 14); ctx.fillStyle = '#ece3d3'; ctx.fill();
      rrect(ctx, 470, y + 10, 14 + 900 * v / 80 * 6, 60, 14); ctx.fillStyle = '#7fb7d6'; ctx.fill();
      text(ctx, '0–4%, berubah-ubah', 500 + 900 * v / 80 * 6 + 14, y + 54, fU(32, 700), C.blue);
    });
    show(ctx, t, u(10).v0, () => {
      card(ctx, 1440, 560, 380, 300, { r: 26, bg: C.forest });
      text(ctx, 'sedikit, tapi', 1475, 625, fU(28, 600), C.forest3);
      text(ctx, 'GAS RUMAH', 1475, 700, fU(46, 700), C.amber); text(ctx, 'KACA', 1475, 750, fU(46, 700), C.amber);
      text(ctx, 'uap air · karbon dioksida', 1475, 820, fU(24, 600), C.cream);
    });
    show(ctx, t, u(9).v0 - 1.2, () => text(ctx, 'disederhanakan, panjang batang tidak proporsional untuk gas kecil', 1810, 245, fU(18, 500), C.gray, 'right'));
  });
}

// ---------------------------------------------------------------- aerosol
function sAerosol(ctx, t) {
  scene(ctx, t, 'aerosol', '#eef3f6', () => {
    title(ctx, t, 'aerosol', 'Aerosol: partikel kecil yang melahirkan awan');
    const items = [['debu', 'debu', '#b08a5a'], ['garam laut', 'garam', '#e8eef2'], ['abu gunung api', 'abu', '#6b6b6b'], ['asap', 'asap', '#9a9a9a']];
    items.forEach(([s, w, col], i) => {
      const k = sp(t, tw(w, u(11).v0) - 0.1, SPRING.bouncy); if (k <= 0) return;
      const x = 260 + i * 260, y = 420;
      ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
      card(ctx, -110, -130, 220, 260, { r: 24 });
      for (let j = 0; j < 9; j++) { circle(ctx, -50 + hash01(j, i) * 100, -70 + hash01(j, i + 9) * 100, 6 + hash01(j, i + 4) * 9); ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = 'rgba(0,0,0,0.25)'; ctx.lineWidth = 2; ctx.stroke(); }
      text(ctx, s, 0, 100, fU(26, 700), C.ink, 'center'); ctx.restore();
    });
    show(ctx, t, u(12).v0, () => pill(ctx, 'semua ini disebut AEROSOL', 650, 640, fU(34, 700), C.forest, C.cream, 26, 64, 'center'));
    // droplet formation
    const pd = ap(t, tw('tempat', u(13).v0) - 0.5, 3.0, E.inOutCubic);
    show(ctx, t, u(13).v0, () => {
      card(ctx, 1300, 290, 520, 560, { r: 28 });
      text(ctx, 'inti kondensasi', 1560, 345, fU(30, 700), C.ink, 'center');
      const cx = 1560, cy = 560;
      circle(ctx, cx, cy, 60 + 70 * pd); ctx.fillStyle = `rgba(127,183,214,${0.25 + 0.5 * pd})`; ctx.fill();
      for (let j = 0; j < 18; j++) { const a = j / 18 * Math.PI * 2 + t * 0.3, r = lerp(230, 70, pd) + 10 * Math.sin(t * 3 + j); circle(ctx, cx + Math.cos(a) * r, cy + Math.sin(a) * r * 0.8, 7); ctx.fillStyle = C.blue; ctx.fill(); }
      circle(ctx, cx, cy, 22); ctx.fillStyle = '#8a6a44'; ctx.fill();
      text(ctx, pd < 0.7 ? 'uap air mendekat' : 'titik awan terbentuk', cx, 790, fU(28, 700), C.blue, 'center');
    });
    show(ctx, t, u(14).v0, () => pill(ctx, 'tanpa aerosol, awan sulit terbentuk', 650, 760, fU(30, 700), C.clay, C.cream, 24, 58, 'center'));
  });
}

// ---------------------------------------------------------------- lapisan (vertical profile)
const PROF = [[0, 15], [12, -56], [20, -56], [50, -2], [85, -90], [110, -40]];
const LAY = [['Troposfer', 'troposphere', 0, 12, '#cfe6d6', 17], ['Stratosfer', 'stratosphere', 12, 50, '#dbe6f2', 24], ['Mesosfer', 'mesosphere', 50, 85, '#e4def0', 27], ['Termosfer', 'thermosphere', 85, 110, '#1f2a44', 30]];
function sLapisan(ctx, t) {
  scene(ctx, t, 'lapisan', C.sand, () => {
    title(ctx, t, 'lapisan', 'Lapisan atmosfer: dilihat dari perubahan suhu');
    const gx = 230, gy = 900, gw = 760, gh = 660;
    const Y = (km) => gy - km / 110 * gh, X = (c) => gx + (c + 100) / 130 * gw;
    const cur = LAY.reduce((a, l, i) => (t >= U_(l[5]).v0 - 0.2 ? i : a), -1);
    // bands
    LAY.forEach(([n, en, a, b, col, ui], i) => {
      const p = ap(t, U_(ui).v0 - 0.2, 0.6); if (p <= 0) return;
      ctx.save(); ctx.globalAlpha *= p * (i === cur ? 1 : 0.55);
      ctx.fillStyle = col; ctx.fillRect(gx, Y(b), gw, Y(a) - Y(b));
      text(ctx, n.toUpperCase(), gx + gw - 16, Y(b) + 36, fU(24, 700), i === 3 ? '#cfe0ff' : C.ink, 'right');
      ctx.restore();
    });
    if (cur === 3) { stars(ctx, gx, Y(110), gw, Y(85) - Y(110), 25); aurora(ctx, gx + 380, Y(108), 360, Y(92) - Y(108), t, ap(t, u(32).v0, 0.8)); }
    // axes
    ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
    [0, 12, 50, 85, 110].forEach((k) => text(ctx, `${k} km`, gx - 14, Y(k) + 8, fU(22, 600), C.gray, 'right'));
    [-90, -60, -30, 0].forEach((c) => text(ctx, `${c}`.replace('-', '−'), X(c), gy + 32, fU(20, 600), C.gray, 'center'));
    text(ctx, 'suhu (°C)', gx + gw, gy + 60, fU(22, 600), C.gray, 'right');
    // curve up to current top
    const top = [0, 12, 50, 85, 110][cur + 1] || 0; const kmTop = cur < 0 ? 0 : lerp(LAY[cur][2], top, ap(t, U_(LAY[cur][5]).v0, 2.5, E.inOutCubic));
    if (cur >= 0) {
      ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.lineJoin = 'round'; ctx.beginPath();
      const T_ = (km) => { for (let i = 0; i < PROF.length - 1; i++) if (km <= PROF[i + 1][0]) return lerp(PROF[i][1], PROF[i + 1][1], (km - PROF[i][0]) / (PROF[i + 1][0] - PROF[i][0])); return PROF[PROF.length - 1][1]; };
      for (let km = 0; km <= kmTop; km += 0.5) { km ? ctx.lineTo(X(T_(km)), Y(km)) : ctx.moveTo(X(T_(km)), Y(km)); }
      ctx.stroke();
    }
    // overlays in graph
    show(ctx, t, u(19).v0 + 1, () => { pill(ctx, 'turun 0,6 °C / 100 m', X(-10), Y(6), fU(24, 700), C.clay, C.cream, 16, 44); });
    show(ctx, t, u(20).v0, () => { text(ctx, 'lapse rate', X(-10) + 20, Y(6) + 52, fI(34), C.clayD); });
    show(ctx, t, u(21).v0, () => { ctx.setLineDash([10, 8]); ctx.strokeStyle = C.forest; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, Y(12)); ctx.lineTo(gx + gw, Y(12)); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'tropopause', gx + 14, Y(12) - 10, fI(30), C.forest); });
    show(ctx, t, u(23).v0, () => cbCloud(ctx, X(-75), Y(0), Y(0) - Y(12) > 0 ? (Y(0) - Y(12)) / 200 : 1));
    show(ctx, t, tw('ozon', u(25).v0), () => { ctx.fillStyle = 'rgba(120,90,200,0.25)'; ctx.fillRect(gx, Y(32), gw, Y(18) - Y(32)); text(ctx, 'lapisan ozon', X(-95), Y(25) + 9, fU(24, 700), '#5b3fa0'); for (let k = 0; k < 3; k++) { const ph = (t * 0.7 + k / 3) % 1; arrowLine(ctx, X(-40) + k * 80, Y(45), X(-40) + k * 80, lerp(Y(45), Y(30), ph), '#8e5bd6', 4, 14); } });
    show(ctx, t, u(26).v0, () => plane(ctx, X(-20), Y(12) - 14, 0.6));
    show(ctx, t, u(29).v0, () => { for (let k = 0; k < 3; k++) { const ph = (t * 0.6 + k * 0.33) % 1; meteor(ctx, X(-80) + k * 150 + ph * 120, Y(80) + ph * (Y(60) - Y(80)), 70, 1 - ph); } });
    show(ctx, t, u(31).v0 + 1.5, () => { ctx.strokeStyle = '#ffd36b'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(X(-90), Y(0)); ctx.lineTo(X(-60), Y(95)); ctx.lineTo(X(-30), Y(0)); ctx.stroke(); text(ctx, 'radio dipantulkan', X(-60), Y(97), fU(20, 700), '#ffd36b', 'center'); });
    // right info card
    if (cur >= 0) {
      const [n, en, a, b, col, ui] = LAY[cur]; const k = sp(t, U_(ui).v0 - 0.1, SPRING.snappy);
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); ctx.translate((1 - k) * 60, 0);
      card(ctx, 1080, 330, 740, 570, { r: 28 });
      rrect(ctx, 1080, 330, 740, 16, 8); ctx.fillStyle = cur === 3 ? '#3b4f8a' : C.forestL; ctx.fill();
      text(ctx, n, 1120, 420, fD(70), C.forest); text(ctx, en, 1120, 470, fI(40), C.clayD);
      text(ctx, cur === 3 ? 'di atas 85 km' : `${a}–${b} km`, 1780, 420, fU(32, 700), C.gray, 'right');
      const facts = [
        [['hampir semua cuaca terjadi di sini', u(19).v0], ['ekuator ±17 km, kutub ±8 km', u(18).v0], ['suhu TURUN ke atas', u(19).v0 + 2], ['batas atas: tropopause', u(21).v0]],
        [['suhu NAIK: ozon menyerap UV', u(25).v0], ['udara stabil', u(26).v0], ['jet terbang di bagian bawahnya', tw('pesawat', u(26).v0)]],
        [['suhu turun lagi sampai ±−90 °C', u(28).v0], ['lapisan terdingin', tw('terdingin', u(28).v0)], ['meteor terbakar di sini', u(29).v0]],
        [['ionosfer (ionosphere): memantulkan radio', u(31).v0], ['aurora borealis (utara)', tw('borealis', u(33).v0)], ['aurora australis (selatan)', tw('australis', u(33).v0)], ['partikel matahari menumbuk O dan N', u(34).v0]],
      ][cur];
      facts.forEach(([s, t0], j) => show(ctx, t, t0, () => { circle(ctx, 1132, 548 + j * 82, 10); ctx.fillStyle = C.clay; ctx.fill(); wrap(ctx, s, fU(30, 600), 640).slice(0, 1).forEach((l) => text(ctx, l, 1160, 558 + j * 82, fU(30, 600), C.ink)); }));
      ctx.restore();
    }
    // equator vs pole inset (troposphere thickness)
    show(ctx, t, u(18).v0, () => {
      if (cur !== 0) return; ctx.save(); ctx.globalAlpha *= 1 - ap(t, u(19).v0 + 1.5, 0.4);
      const cx = 1400, cy = 875; ctx.fillStyle = '#cfe6d6'; ctx.beginPath(); ctx.ellipse(cx, cy, 160, 118, 0, Math.PI, 0); ctx.fill();
      circle(ctx, cx, cy, 94); ctx.fillStyle = '#2f6f9e'; ctx.fill(); ctx.fillStyle = '#fffefa'; ctx.fillRect(cx - 200, cy, 400, 24);
      text(ctx, 'tebal di ekuator', cx + 175, cy - 20, fU(22, 700), C.forest); text(ctx, 'tipis di kutub', cx + 70, cy - 112, fU(22, 700), C.forest);
      ctx.restore();
    });
  });
}

// ---------------------------------------------------------------- tekanan
function sTekanan(ctx, t) {
  scene(ctx, t, 'tekanan', '#eef3f6', () => {
    title(ctx, t, 'tekanan', 'Tekanan udara: berat kolom udara di atas kita');
    // columns
    const base = 860; ctx.fillStyle = '#5aa0c8'; ctx.fillRect(110, base, 900, 40);
    mountain(ctx, 700, base, 560, 420, '#9a8670');
    const pc = ap(t, u(36).v0 + 1, 1.2, E.outCubic);
    const col = (x, y0, h, lab) => { const hh = h * pc; const g = ctx.createLinearGradient(0, y0 - hh, 0, y0); g.addColorStop(0, 'rgba(43,108,176,0.05)'); g.addColorStop(1, 'rgba(43,108,176,0.45)'); ctx.fillStyle = g; ctx.fillRect(x - 60, y0 - hh, 120, hh); ctx.strokeStyle = C.blue; ctx.lineWidth = 3; ctx.strokeRect(x - 60, y0 - hh, 120, hh); if (pc > 0.8) text(ctx, lab, x, y0 - hh - 16, fU(24, 700), C.blue, 'center'); };
    if (pc > 0) { col(260, base, 540, 'kolom tinggi'); col(700, base - 420, 180, 'kolom pendek'); }
    person(ctx, 720, base - 420, 0.9);
    show(ctx, t, u(37).v0, () => pill(ctx, 'permukaan laut ±1.013 mb', 260, base - 30, fU(24, 700), C.forest, C.cream, 16, 46, 'center'));
    // graph
    card(ctx, 1080, 290, 740, 610, { r: 28 });
    const gx = 1180, gy = 820, gw = 580, gh = 440; const X = (p) => gx + p / 1013 * gw, Y = (km) => gy - km / 12 * gh;
    ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
    [0, 3, 5.5, 9, 12].forEach((k) => text(ctx, `${k}`.replace('.', ','), gx - 12, Y(k) + 8, fU(20, 600), C.gray, 'right'));
    [0, 500, 1013].forEach((p) => text(ctx, `${p}`.replace('1013', '1.013'), X(p), gy + 30, fU(20, 600), C.gray, 'center'));
    text(ctx, 'ketinggian (km)', gx - 60, gy - gh - 22, fU(20, 700), C.gray); text(ctx, 'tekanan (mb)', gx + gw, gy + 60, fU(20, 700), C.gray, 'right');
    const pg = ap(t, u(38).v0, 2.5, E.linear);
    if (pg > 0) { ctx.strokeStyle = C.clay; ctx.lineWidth = 6; ctx.beginPath(); for (let k = 0; k <= 12 * pg; k += 0.1) { const p = 1013 * Math.exp(-k / 7.94); k ? ctx.lineTo(X(p), Y(k)) : ctx.moveTo(X(p), Y(k)); } ctx.stroke(); }
    show(ctx, t, tw('separuh', u(39).v0) - 0.6, () => { ctx.setLineDash([8, 8]); ctx.strokeStyle = C.forest; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, Y(5.5)); ctx.lineTo(X(506), Y(5.5)); ctx.lineTo(X(506), gy); ctx.stroke(); ctx.setLineDash([]); pill(ctx, '5,5 km: tinggal separuh', X(506) + 20, Y(5.5) - 40, fU(24, 700), C.forest, C.cream, 16, 44); });
    show(ctx, t, u(40).v0, () => { card(ctx, 1110, 300, 680, 110, { r: 22, bg: C.forest }); text(ctx, 'lapisan bawah: turun ±1 mb tiap naik 10 m', 1450, 368, fU(28, 700), C.amber, 'center'); });
    show(ctx, t, u(36).v0, () => text(ctx, 'atmospheric pressure', 112, 222, fI(34), C.clayD));
  });
}

// ---------------------------------------------------------------- config
run({
  DUR, no: 2, code: 'B01-02', chip: 'BAB 1 · IKLIM · VIDEO #2 · DASAR', title: 'Atmosfer Bumi', sub: 'isi, lapisan, dan tekanan udara · istilah asing OSN',
  next: '#3 · B01-03 · Radiasi Matahari dan Insolasi',
  SCN: [['hook', 0], ['komposisi', 7], ['aerosol', 11], ['lapisan', 15], ['tekanan', 35], ['soal', 42], ['jebakan', 47], ['ringkas', 51], ['outro', 54]],
  TERMS: [
    ['Aerosol', 'condensation nuclei', 'Partikel kecil tempat uap air mengembun menjadi titik awan', 13],
    ['Troposfer', 'troposphere', '0–12 km; tempat hampir semua cuaca terjadi', 17],
    ['Laju penurunan suhu', 'lapse rate', 'Suhu turun ±0,6 °C setiap naik 100 m', 20],
    ['Tropopause', 'tropopause · anvil', 'Batas atas troposfer; puncak awan Cb mendatar (anvil)', 21],
    ['Stratosfer', 'stratosphere', '12–50 km; suhu naik karena ozon menyerap UV', 24],
    ['Lapisan ozon', 'ozone layer', 'Penyerap sinar ultraviolet di stratosfer', () => tw('ozon', u(25).v0)],
    ['Mesosfer', 'mesosphere', '50–85 km; terdingin (±−90 °C), meteor terbakar', 27],
    ['Termosfer', 'thermosphere', 'Lapisan paling atas, di atas 85 km', 30],
    ['Ionosfer', 'ionosphere', 'Bagian bermuatan ion; memantulkan gelombang radio', 31],
    ['Aurora', 'aurora borealis · australis', 'Partikel bermuatan matahari menumbuk atom O dan N', 33],
    ['Tekanan udara', 'atmospheric pressure', 'Berat kolom udara; ±1.013 mb di permukaan laut', 36],
  ],
  hook,
  soal: {
    q: 'Tekanan di permukaan laut 1.012 mb. Dengan pendekatan penurunan 1 mb setiap naik 10 m, tekanan udara di Dataran Tinggi Dieng (±2.000 m) adalah …',
    opts: ['1.212 mb', '992 mb', '812 mb', '612 mb', '200 mb'], ans: 2,
    ansT: () => tw('jawabannya', u(45).v0 - 0.3),
    steps: () => [[u(43).v0, '1) Penurunan tekanan', C.forest3, 30], [tw('dibagi', u(43).v0), '2.000 ÷ 10 = 200 mb', C.cream, 40],
      [u(44).v0, '2) Tekanan di Dieng', C.forest3, 30], [tw('dikurangi', u(44).v0), '1.012 − 200', C.cream, 40], [tw('delapan', u(44).v0), '= 812 mb', C.amber, 60],
      [u(46).v0, 'Catatan: pendekatan kasar, hanya untuk beberapa km pertama', C.forest3, 26]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[u(48).v0, 'Aurora = pantulan sinar matahari oleh es kutub', 'Aurora: partikel matahari menumbuk atom O dan N', u(48).v0 + 2.6],
      [u(49).v0, 'Lapisan ozon pelindung ada di troposfer', 'Ozon pelindung di STRATOSFER; ozon permukaan = polutan', u(50).v0]],
  },
  ringkas: {
    items: () => [[tw('troposfer', u(52).v0), 'Troposfer: tempat cuaca, suhu turun 0,6 °C/100 m'], [tw('stratosfer', u(52).v0), 'Stratosfer: lapisan ozon, suhu naik'], [tw('tekanan', u(52).v0), 'Tekanan turun saat naik (±1 mb per 10 m)']],
  },
  scenes: { komposisi: sKomposisi, aerosol: sAerosol, lapisan: sLapisan, tekanan: sTekanan },
});
