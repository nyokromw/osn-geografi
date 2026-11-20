// B01-08 · Angin Lokal · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 217.9;
let W50 = null, JAVA = null, INDO = null, ADR = null;

function boat(ctx, x, y, s, dir, sail = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  ctx.fillStyle = '#7b3d22'; poly(ctx, [[-40, 0], [40, 0], [28, 16], [-28, 16]]); ctx.fill();
  ctx.strokeStyle = '#4a2a18'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -70); ctx.stroke();
  ctx.fillStyle = '#fffefa'; ctx.beginPath(); ctx.moveTo(2, -68); ctx.quadraticCurveTo(2 + 40 * sail, -40, 2, -6); ctx.closePath(); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.stroke();
  ctx.restore();
}
function moon(ctx, x, y, r) { circle(ctx, x, y, r); ctx.fillStyle = '#f3e5a8'; ctx.fill(); circle(ctx, x + r * 0.4, y - r * 0.2, r * 0.85); ctx.fillStyle = 'rgba(15,34,51,1)'; ctx.fill(); }
function clockBadge(ctx, x, y, r, hour, label) {
  circle(ctx, x, y, r); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2; ctx.beginPath(); ctx.moveTo(x + Math.sin(a) * r * 0.8, y - Math.cos(a) * r * 0.8); ctx.lineTo(x + Math.sin(a) * r * 0.92, y - Math.cos(a) * r * 0.92); ctx.stroke(); }
  const ah = (hour % 12) / 12 * Math.PI * 2, am = (hour % 1) * Math.PI * 2;
  ctx.lineCap = 'round'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.sin(ah) * r * 0.5, y - Math.cos(ah) * r * 0.5); ctx.stroke();
  ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.sin(am) * r * 0.75, y - Math.cos(am) * r * 0.75); ctx.stroke();
  if (label) pill(ctx, label, x, y + r + 34, fU(24, 800), C.forest, C.cream, 14, 44, 'center');
}
const hh = (h) => `${String(Math.floor(h) % 24).padStart(2, '0')}.${String(Math.floor((h % 1) * 60)).padStart(2, '0')}`;

// ---------------------------------------------------------------- hook: Java coast map, boats, Tengger
function sHook(ctx, t) {
  scene(ctx, t, 'hook', C.sand, () => {
    const box = { x: 0, y: 0, w: W, h: H };
    const k = ap(t, U_(1).v0 - 0.3, 2.2, E.inOutCubic);
    const cx = lerp(110.0, 113.1, k), cy = lerp(-6.6, -7.75, k), sx = lerp(5.4, 1.6, k), sy = sx * H / W;
    const pr = G.mapProj(box, [cx - sx, cx + sx, cy - sy, cy + sy]);
    G.drawMap(ctx, JAVA, pr, { t, depth: 10 });
    // boats leaving coast north
    const hour = lerp(3, 13, ap(t, 3, 5.5, E.linear));
    [[108.6, -6.6], [109.6, -6.75], [110.6, -6.85], [111.4, -6.75]].forEach(([lo, la], i) => { const out = Math.sin(clamp((hour - 3) / 10) * Math.PI); const p = pr(lo + 0.1 * i, la + 0.15 + 0.55 * out); boat(ctx, p[0], p[1], 0.7 * (1 - k), hour < 8 ? 1 : -1); });
    if (k < 0.5) { ctx.save(); ctx.globalAlpha *= 1 - k * 2; clockBadge(ctx, 1700, 300, 80, hour, hour < 8 ? 'dini hari: berangkat' : 'siang: pulang'); ctx.restore(); }
    // Tengger wind
    if (k > 0.3) {
      ctx.save(); ctx.globalAlpha *= clamp((k - 0.3) * 2);
      const m = pr(112.95, -7.94); ctx.fillStyle = '#9a8670'; poly(ctx, [[m[0] - 260, m[1] + 80], [m[0], m[1] - 140], [m[0] + 260, m[1] + 80]]); ctx.fill(); text(ctx, 'Pegunungan Tengger', m[0], m[1] + 120, fU(30, 800), '#5a4326', 'center');
      for (let j = 0; j < 4; j++) { const ph = (t * 0.6 + j / 4) % 1; arrowLine(ctx, m[0] - 40 + j * 30, m[1] - 100 + ph * 40, m[0] - 200 - j * 40 + ph * -100, m[1] - 260 + ph * 40, `rgba(224,121,79,${1 - ph})`, 7, 22); }
      const pb = pr(113.22, -7.75); circle(ctx, pb[0], pb[1], 14); ctx.fillStyle = C.clayD; ctx.fill(); pill(ctx, 'Probolinggo', pb[0] + 24, pb[1] - 30, fU(26, 800), C.clayD, C.cream, 14, 46);
      // wilting tobacco leaf
      const wl = ap(t, U_(1).v0 + 2, 2); ctx.save(); ctx.translate(1600, 760); ctx.rotate(0.8 * wl); ctx.fillStyle = mix('#3f8a52', '#a08a3c', wl); ctx.beginPath(); ctx.ellipse(0, -60, 34, 70, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore(); text(ctx, 'tembakau', 1600, 860, fU(26, 800), C.ink, 'center');
      ctx.restore();
    }
    show(ctx, t, U_(2).v0, () => { card(ctx, W / 2 - 330, 420, 660, 170, { r: 40, bg: C.forest }); text(ctx, 'angin lokal', W / 2, 535, fD(96), C.cream, 'center'); });
  });
}

// ---------------------------------------------------------------- definisi: 24-hour switch + scale
function sDefinisi(ctx, t) {
  scene(ctx, t, 'definisi', '#eef3f6', () => {
    title(ctx, t, 'definisi', 'Angin lokal: skala kecil, berganti dalam sehari');
    show(ctx, t, U_(3).v0 + 0.5, () => text(ctx, 'local wind', 112, 222, fI(34), C.clayD));
    const hour = ((t - SC.definisi[0]) * 2.4 + 8) % 24, day = hour > 7 && hour < 19;
    clockBadge(ctx, 520, 590, 210, hour, `pukul ${hh(hour)}`);
    const dir = day ? 1 : -1; for (let j = 0; j < 5; j++) { const ph = (t * 0.7 + j / 5) % 1; const x = 1020 + (dir > 0 ? ph : 1 - ph) * 700; arrowLine(ctx, x - dir * 60, 520 + j * 40, x + dir * 40, 520 + j * 40, day ? C.blue : C.clay, 6, 20); }
    ctx.fillStyle = '#5aa0c8'; rrect(ctx, 1000, 760, 380, 60, 14); ctx.fill(); ctx.fillStyle = '#d9c28f'; rrect(ctx, 1380, 760, 400, 60, 14); ctx.fill();
    text(ctx, 'laut', 1190, 800, fU(28, 800), '#fff', 'center'); text(ctx, 'darat', 1580, 800, fU(28, 800), '#5a4326', 'center');
    pill(ctx, day ? 'siang: laut ke darat' : 'malam: darat ke laut', 1390, 440, fU(30, 800), day ? C.blue : C.clay, C.cream, 20, 56, 'center');
    show(ctx, t, tw('puluh', U_(3).v0) - 0.3, () => { ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(1000, 870); ctx.lineTo(1780, 870); ctx.moveTo(1000, 855); ctx.lineTo(1000, 885); ctx.moveTo(1780, 855); ctx.lineTo(1780, 885); ctx.stroke(); pill(ctx, 'beberapa puluh km', 1390, 870, fU(24, 800), C.cream, C.ink, 14, 42, 'center'); });
  });
}

// ---------------------------------------------------------------- pantai: paper-cut coast with circulation
function sPantai(ctx, t) {
  const t0 = SC.pantai[0];
  // local hour: day phase until u9, night u9..u13, dawn->noon u13..end
  const hour = t < U_(9).v0 ? lerp(9, 14, ap(t, t0, U_(9).v0 - t0, E.linear)) : t < U_(13).v0 ? lerp(19, 27, ap(t, U_(9).v0, 2.5, E.inOutCubic)) % 24 : lerp(3, 13, ap(t, U_(13).v0, 9, E.linear));
  const night = (hour >= 18.5 || hour < 5.5) ? 1 : (hour < 6.5 ? 6.5 - hour : hour > 17.5 ? hour - 17.5 : 0);
  const nk = clamp(night);
  const sky = ctx.createLinearGradient(0, 0, 0, H); sky.addColorStop(0, mix('#9cc8e6', '#0f2233', nk)); sky.addColorStop(1, mix('#e9f2f7', '#26405a', nk));
  ctx.fillStyle = sky; ctx.fillRect(0, 0, W, H);
  const ex = E.inCubic(prog(t, SC.pantai[1] - 0.35, SC.pantai[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  // sun / moon arc
  const ang = ((hour - 6) / 12) * Math.PI; const bx = W / 2 - Math.cos(ang) * 760, by = 760 - Math.sin(ang) * 520;
  if (nk < 0.9) sun(ctx, bx, by, 50, t, 1 - nk); if (nk > 0.1) { ctx.save(); ctx.globalAlpha *= nk; for (let i = 0; i < 60; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * 500, 1.5); ctx.fillStyle = '#fff'; ctx.fill(); } moon(ctx, 1500, 260, 40); ctx.restore(); }
  // layers: sea (left) and land (right)
  ctx.fillStyle = mix('#3c8fc2', '#1d3d5c', nk); ctx.fillRect(0, 780, 900, 300);
  for (let k = 0; k < 6; k++) { ctx.strokeStyle = 'rgba(255,255,255,0.3)'; ctx.lineWidth = 3; ctx.beginPath(); for (let x = 0; x <= 900; x += 20) { const y = 800 + k * 40 + 5 * Math.sin(x * 0.02 + t * 2 + k); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
  const land = [['#e8d39c', 790, 0], ['#a9cf8a', 770, 0.4], ['#7fb07a', 730, 0.8]];
  land.forEach(([c, y0, j]) => { ctx.fillStyle = mix(c, '#2a3d33', nk * 0.6); ctx.beginPath(); ctx.moveTo(880 + j * 80, H); ctx.lineTo(880 + j * 80, y0); for (let x = 880 + j * 80; x <= W; x += 30) ctx.lineTo(x, y0 - j * 120 - 30 * Math.sin(x * 0.01 + j * 3)); ctx.lineTo(W, H); ctx.closePath(); ctx.shadowColor = 'rgba(0,0,0,0.18)'; ctx.shadowBlur = 14; ctx.shadowOffsetX = -6; ctx.fill(); ctx.shadowColor = 'transparent'; });
  for (let i = 0; i < 5; i++) { const x = 1150 + i * 120; ctx.fillStyle = mix('#c27a4b', '#3a2a22', nk * 0.6); ctx.fillRect(x, 700, 70, 50); poly(ctx, [[x - 8, 702], [x + 35, 670], [x + 78, 702]]); ctx.fillStyle = mix('#7b3d22', '#2a1a12', nk * 0.6); ctx.fill(); if (nk > 0.5) { ctx.fillStyle = '#f3e5a8'; ctx.fillRect(x + 25, 715, 18, 16); } }
  // circulation loop (day: sea->land at surface)
  const dayDir = nk < 0.5 ? 1 : -1; const wk = ap(t, U_(7).v0 - 0.4, 0.6) * (t < U_(9).v0 ? 1 : 1) * (t > U_(10).v0 || t < U_(9).v0 ? 1 : 0);
  if (wk > 0) for (let i = 0; i < 120; i++) {
    const s = ((t * 0.08 + hash01(i, 3)) % 1) * 4, si = Math.floor(s), f = s - si;
    const L = 380, R = 1450, B = 740, T_ = 380;
    let x, y; const seg = dayDir > 0 ? [[L, B, R, B], [R, B, R, T_], [R, T_, L, T_], [L, T_, L, B]] : [[R, B, L, B], [L, B, L, T_], [L, T_, R, T_], [R, T_, R, B]];
    const [x1, y1, x2, y2] = seg[si]; x = lerp(x1, x2, f) + (si % 2 ? (hash01(i, 5) - 0.5) * 120 : 0); y = lerp(y1, y2, f) + (si % 2 ? 0 : (hash01(i, 6) - 0.5) * 50);
    circle(ctx, x, y, si === 0 ? 6 : 4.5); ctx.fillStyle = si === 0 ? `rgba(255,255,255,${0.95 * wk})` : `rgba(255,255,255,${0.45 * wk})`; ctx.fill();
  }
  if (wk > 0) { ctx.save(); ctx.globalAlpha *= wk; const y = 690; arrowLine(ctx, dayDir > 0 ? 500 : 1350, y, dayDir > 0 ? 1350 : 500, y, '#ffffff', 10, 32); ctx.restore(); }
  // thermometers + pressure labels
  show(ctx, t, U_(5).v0, () => { const hot = nk < 0.5; pill(ctx, hot ? 'darat PANAS · tekanan RENDAH' : 'darat DINGIN · tekanan TINGGI', 1450, 560, fU(26, 800), hot ? C.clay : C.blue, C.cream, 16, 48, 'center'); pill(ctx, hot ? 'laut sejuk · tekanan tinggi' : 'laut hangat · tekanan rendah', 450, 560, fU(26, 800), hot ? C.blue : C.clay, C.cream, 16, 48, 'center'); });
  // name cards
  show(ctx, t, U_(8).v0, () => { if (nk < 0.5) { card(ctx, 110, 250, 640, 150, { r: 26, bg: C.forest }); text(ctx, 'ANGIN LAUT', 150, 315, fU(44, 800), C.amber); text(ctx, 'sea breeze · ±09.00–16.00', 150, 365, fI(34), C.cream); } });
  show(ctx, t, U_(12).v0, () => { if (nk >= 0.5) { card(ctx, 110, 250, 640, 150, { r: 26, bg: C.cream }); text(ctx, 'ANGIN DARAT', 150, 315, fU(44, 800), C.clayD); text(ctx, 'land breeze · ±20.00–06.00', 150, 365, fI(34), C.ink); } });
  clockBadge(ctx, 1760, 450, 64, hour, hh(hour));
  // fishermen
  if (t > U_(13).v0) { const go = ap(t, U_(14).v0 - 0.5, 2.5, E.inOutCubic), back = ap(t, tw('pulang', U_(14).v0) - 0.3, 2.5, E.inOutCubic); const bxp = lerp(lerp(860, 240, go), 860, back); boat(ctx, bxp, 800, 1.1, back > 0 ? 1 : -1, back > 0 ? 1 : -1); pill(ctx, back > 0 ? 'pulang siang: didorong angin laut' : 'berangkat dini hari: didorong angin darat', 450, 470, fU(26, 800), back > 0 ? C.forest : C.clayD, C.cream, 16, 48, 'center'); }
  ctx.restore();
  title(ctx, t, 'pantai', 'Angin laut dan angin darat', nk > 0.5 ? C.cream : C.forest);
}

// ---------------------------------------------------------------- lembah: 3-D valley terrain
function zV(x, y) { const d = Math.abs(x - 5 - 0.6 * Math.sin(y * 0.5)) / 5; return 3.4 * Math.pow(Math.min(1.2, d), 1.25) + 0.7 * Math.sin(y * 0.9 + x) * d * d + 0.35 * Math.sin(x * 1.7) * Math.cos(y * 1.3) * d + 0.2; }
function sLembah(ctx, t) {
  const night = ap(t, U_(19).v0 - 0.3, 1.5, E.inOutCubic);
  ctx.fillStyle = mix('#dcebf3', '#13263a', night); ctx.fillRect(0, 0, W, H);
  const ex = E.inCubic(prog(t, SC.lembah[1] - 0.35, SC.lembah[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  if (night > 0) { ctx.save(); ctx.globalAlpha *= night; for (let i = 0; i < 60; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * 400, 1.5); ctx.fillStyle = '#fff'; ctx.fill(); } moon(ctx, 1640, 220, 36); ctx.restore(); }
  else sun(ctx, 1640, 230, 48, t);
  const az = -0.785 + 0.18 * Math.sin((t - SC.lembah[0]) * 0.15);
  const P0 = G.iso(1050, 660, 50, az, 0.55); const P = (x, y, z) => P0(x - 5, y - 5, z);
  const ca = Math.cos(az), sa = Math.sin(az); const depth = (x, y) => (x - 5) * ca - (y - 5) * sa + (x - 5) * sa + (y - 5) * ca;
  const N = 28, cs = 10 / N, quads = [];
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const x0 = i * cs, y0 = j * cs; const q = [[x0, y0], [x0 + cs, y0], [x0 + cs, y0 + cs], [x0, y0 + cs]].map(([a, b]) => P(a, b, zV(a, b)));
    const h = zV(x0 + cs / 2, y0 + cs / 2) / 4.5; const sl = (zV(x0 + cs, y0 + cs / 2) - zV(x0, y0 + cs / 2)) / cs, sl2 = (zV(x0 + cs / 2, y0 + cs) - zV(x0 + cs / 2, y0)) / cs; const lit = clamp(0.55 - 0.16 * sl + 0.1 * sl2, 0.15, 1);
    const base = mix(mix('#5f9a5c', '#b9a27a', clamp(h * 1.3 - 0.3)), '#f4f1ea', clamp((h - 0.85) * 4));
    quads.push([depth(x0 + cs / 2, y0 + cs / 2), q, mix(mix('#1d3329', base, 0.45 + 0.55 * lit), '#13263a', night * 0.6)]);
  }
  quads.sort((a, b) => a[0] - b[0]);
  for (const [, q, c] of quads) { ctx.fillStyle = c; poly(ctx, q); ctx.fill(); ctx.strokeStyle = c; ctx.lineWidth = 1; ctx.stroke(); }
  // cold pool at night
  const pool = ap(t, U_(22).v0 - 1, 2.5) * night;
  if (pool > 0) { ctx.save(); ctx.globalAlpha *= 0.55 * pool; ctx.fillStyle = '#9fc4dd'; ctx.beginPath(); for (let j = 0; j <= 10; j++) { const xc = 5 + 0.6 * Math.sin(j * 0.5), p = P(xc - 1.4 - 0.3 * pool, j, zV(xc - 1.4 - 0.3 * pool, j) + 0.1); j ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } for (let j = 10; j >= 0; j--) { const xc = 5 + 0.6 * Math.sin(j * 0.5), p = P(xc + 1.4 + 0.3 * pool, j, zV(xc + 1.4 + 0.3 * pool, j) + 0.1); ctx.lineTo(p[0], p[1]); } ctx.closePath(); ctx.fill(); ctx.restore(); }
  // flow particles along slopes
  const on = t > U_(17).v0 - 0.5 ? 1 : 0;
  if (on) for (let i = 0; i < 110; i++) {
    const side = i % 2 ? 1 : -1, y = hash01(i, 4) * 10, ph = (t * 0.22 + hash01(i, 5)) % 1; const f = night > 0.5 ? 1 - ph : ph; const x = 5 + 0.6 * Math.sin(y * 0.5) + side * (0.4 + 4.4 * f); const p = P(x, y, zV(x, y) + 0.25);
    circle(ctx, p[0], p[1], 5); ctx.fillStyle = night > 0.5 ? 'rgba(159,196,221,0.95)' : 'rgba(224,121,79,0.95)'; ctx.fill();
  }
  // labels
  const lab = night < 0.5 ? [['ANGIN LEMBAH', 'valley breeze · anabatic wind', 'siang: udara naik menyusuri lereng', C.clay, U_(18).v0]] : [['ANGIN GUNUNG', 'mountain breeze · katabatic wind', 'malam: udara dingin turun ke lembah', C.blue, U_(21).v0]];
  lab.forEach(([a, en, d, col, tt]) => show(ctx, t, tt, () => { card(ctx, 110, 700, 760, 200, { r: 26, bg: C.cream }); text(ctx, a, 150, 770, fU(46, 800), col); text(ctx, en, 150, 818, fI(36), C.ink); text(ctx, d, 150, 862, fU(26, 600), C.gray); }));
  show(ctx, t, U_(22).v0, () => pill(ctx, 'udara dingin menggenang di lembah dan kaldera', 1240, 880, fU(26, 800), C.blue, C.cream, 18, 50, 'center'));
  ctx.restore();
  title(ctx, t, 'lembah', 'Angin lembah dan angin gunung', night > 0.5 ? C.cream : C.forest);
}

// ---------------------------------------------------------------- fohn: paper-cut mountain cross-section
function sFohn(ctx, t) {
  scene(ctx, t, 'fohn', '#e7eef3', () => {
    title(ctx, t, 'fohn', 'Angin jatuh: angin fohn');
    const base = 900, peak = [960, 380];
    ctx.fillStyle = '#9a8670'; poly(ctx, [[160, base], [peak[0] - 60, peak[1] + 20], peak, [peak[0] + 70, peak[1] + 30], [1760, base]]); ctx.shadowColor = 'rgba(0,0,0,0.2)'; ctx.shadowBlur = 18; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.fillStyle = '#7fb07a'; poly(ctx, [[160, base], [700, 560], [900, 420], [960, 400], [960, base]]); ctx.fill();
    ctx.fillStyle = '#d9c28f'; poly(ctx, [[960, base], [960, 400], [1060, 430], [1400, 620], [1760, base]]); ctx.fill();
    text(ctx, 'lereng depan (lembap)', 400, 950, fU(26, 800), C.forest, 'center'); text(ctx, 'lereng belakang (kering)', 1520, 950, fU(26, 800), '#7a5a2c', 'center');
    // parcel path
    const pathPt = (f) => { if (f < 0.5) { const k = f / 0.5; return [lerp(200, 930, k), lerp(850, 360, Math.pow(k, 1.2))]; } const k = (f - 0.5) / 0.5; return [lerp(990, 1720, k), lerp(360, 850, Math.pow(k, 0.8))]; };
    const p = ap(t, U_(25).v0, 7.5, E.linear);
    ctx.setLineDash([12, 10]); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); for (let i = 0; i <= 60; i++) { const q = pathPt(i / 60); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); } ctx.stroke(); ctx.setLineDash([]);
    show(ctx, t, U_(25).v0 + 1, () => { cloud(ctx, 640, 480, 1.6, '#f4f6f8'); cloud(ctx, 820, 420, 1.3, '#f4f6f8'); rain(ctx, 650, 520, 160, t, 7); rain(ctx, 820, 450, 120, t, 5); });
    if (p > 0) { const [x, y] = pathPt(p % 1); circle(ctx, x, y, 26); ctx.fillStyle = p < 0.5 ? '#7fb7d6' : C.clay; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke(); }
    show(ctx, t, U_(26).v0 + 1, () => { for (let i = 0; i < 6; i++) { const ph = (t * 0.6 + i / 6) % 1; const x = 1300 + i * 60; ctx.strokeStyle = `rgba(224,121,79,${1 - ph})`; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x, 860 - ph * 80); ctx.bezierCurveTo(x + 10, 840 - ph * 80, x - 10, 820 - ph * 80, x, 800 - ph * 80); ctx.stroke(); } pill(ctx, 'turun: kering dan panas', 1450, 640, fU(28, 800), C.clay, C.cream, 18, 52, 'center'); });
    show(ctx, t, U_(24).v0, () => text(ctx, 'foehn wind', 112, 222, fI(34), C.clayD));
    show(ctx, t, U_(27).v0, () => pill(ctx, 'hitungan lengkap: video Efek Fohn', 1780, 360, fU(24, 800), C.forest, C.cream, 16, 46, 'right'));
  });
}

// ---------------------------------------------------------------- peta angin fohn Indonesia (living camera)
const FOHN = [['Gending', 'Probolinggo–Pasuruan', 113.2, -7.75, 29, 'Juli–September, merusak tembakau'], ['Kumbang', 'Cirebon–Tegal', 108.9, -6.85, 30, 'turun dari Ciremai dan Slamet'], ['Brubu', 'Makassar', 119.4, -5.15, 31, 'kemarau, kering'], ['Bahorok', 'Deli, Sumatra Utara', 98.6, 3.6, 32, 'merusak tembakau Deli'], ['Wambraw', 'Biak, Papua', 136.1, -1.0, 33, 'kering dan panas']];
function sPetaFohn(ctx, t) {
  scene(ctx, t, 'petafohn', C.sand, () => {
    const box = { x: 110, y: 240, w: 1700, h: 680 };
    const cur = FOHN.reduce((a, f, i) => (t >= U_(f[4]).v0 - 0.4 ? i : a), -1);
    let cx = 117, cy = -2.5, sx = 25; // overview
    if (cur >= 0) { const f = FOHN[cur], k = ap(t, U_(f[4]).v0 - 0.4, 1.0, E.inOutCubic); const prev = cur > 0 ? FOHN[cur - 1] : null; const px = prev ? prev[2] : 117, py = prev ? prev[3] : -2.5, ps = prev ? 9 : 25; cx = lerp(px, f[2], k); cy = lerp(py, f[3], k); sx = lerp(ps, 9, k); }
    const zoomOut = ap(t, U_(34).v0 - 1.2, 0.8); if (zoomOut > 0) { cx = lerp(cx, 117, zoomOut); cy = lerp(cy, -2.5, zoomOut); sx = lerp(sx, 25, zoomOut); }
    const sy = sx * box.h / box.w; const ext = [cx - sx, cx + sx, cy - sy, cy + sy];
    const pr = G.mapProj(box, ext);
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    G.drawMap(ctx, INDO, pr, { t, depth: 8 });
    ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
    FOHN.forEach(([n, loc, lo, la, ui], i) => {
      const k = sp(t, U_(ui).v0, SPRING.bouncy); if (k <= 0) return; const p = pr(lo, la);
      ctx.save(); ctx.translate(p[0], p[1]); ctx.scale(k, k);
      ctx.fillStyle = '#8a7350'; poly(ctx, [[-60, 30], [-10, -60], [40, 30]]); ctx.fill();
      for (let j = 0; j < 3; j++) { const ph = (t * 0.8 + j / 3) % 1; arrowLine(ctx, -10 + ph * 20, -40 + ph * 30, 40 + ph * 60, 10 + ph * 40, `rgba(224,121,79,${1 - ph})`, 6, 18); }
      circle(ctx, 0, 0, 12); ctx.fillStyle = i === cur ? C.clayD : C.clay; ctx.fill(); ctx.strokeStyle = C.cream; ctx.lineWidth = 3; ctx.stroke();
      ctx.restore();
      pill(ctx, `Angin ${n}`, p[0], p[1] - 90 * k, fU(i === cur ? 30 : 22, 800), i === cur ? C.clayD : C.clay, C.cream, 14, i === cur ? 52 : 40, 'center');
    });
    ctx.restore();
    if (cur >= 0) { const [n, loc, , , ui, d] = FOHN[cur]; const k = sp(t, U_(ui).v0, SPRING.snappy); ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); card(ctx, 140, 760, 720, 130, { r: 22, bg: C.forest }); text(ctx, `Angin ${n} · ${loc}`, 175, 815, fU(32, 800), C.amber); text(ctx, d, 175, 860, fU(26, 600), C.cream); ctx.restore(); }
    title(ctx, t, 'petafohn', 'Angin fohn di Indonesia');
  });
}

// ---------------------------------------------------------------- bora: Adriatic map
function sBora(ctx, t) {
  scene(ctx, t, 'bora', '#e9eef1', () => {
    const box = { x: 110, y: 240, w: 1700, h: 680 }; const ext = [11.5, 22, 40.5, 46.7];
    const pr = G.mapProj(box, ext);
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    G.drawMap(ctx, ADR, pr, { t, depth: 8, land: '#eef0e6' });
    ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
    // Dinaric highlands hatch
    const hk = ap(t, U_(35).v0, 1); ctx.save(); ctx.globalAlpha *= hk; ctx.strokeStyle = '#8a7350'; ctx.lineWidth = 3; for (let i = 0; i < 14; i++) { const p = pr(15 + i * 0.45, 45.2 - i * 0.32); ctx.beginPath(); ctx.moveTo(p[0] - 30, p[1] + 20); ctx.lineTo(p[0], p[1] - 20); ctx.lineTo(p[0] + 30, p[1] + 20); ctx.stroke(); } ctx.restore();
    const pk = ap(t, U_(34).v0 + 0.5, 0.8);
    if (pk > 0) for (let i = 0; i < 9; i++) { const ph = (t * 0.5 + i / 9) % 1; const a = pr(15.5 + i * 0.5, 45.6 - i * 0.33), b = pr(14.6 + i * 0.5, 44.6 - i * 0.33); const x = lerp(a[0], b[0], ph), y = lerp(a[1], b[1], ph); arrowLine(ctx, x - (b[0] - a[0]) * 0.25, y - (b[1] - a[1]) * 0.25, x, y, `rgba(43,108,176,${pk * Math.sin(ph * Math.PI)})`, 7, 22); }
    for (let i = 0; i < 14; i++) { const ph = (t * 0.3 + hash01(i, 2)) % 1; const p = pr(15 + hash01(i, 3) * 5, 46.5 - ph * 2.5); ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2.5; for (let k = 0; k < 3; k++) { const a = k * Math.PI / 3; ctx.beginPath(); ctx.moveTo(p[0] - Math.cos(a) * 8, p[1] - Math.sin(a) * 8); ctx.lineTo(p[0] + Math.cos(a) * 8, p[1] + Math.sin(a) * 8); ctx.stroke(); } }
    ctx.restore();
    show(ctx, t, U_(35).v0 + 0.5, () => { const p = pr(14.2, 42.5); text(ctx, 'Laut Adriatik', p[0], p[1], fU(30, 800), '#4a7da0', 'center'); const q = pr(18.5, 45.6); text(ctx, 'dataran tinggi (Dinarik)', q[0], q[1], fU(26, 800), '#5a4326', 'center'); });
    show(ctx, t, U_(34).v0, () => { card(ctx, 140, 720, 640, 170, { r: 24, bg: C.forest }); text(ctx, 'ANGIN BORA', 175, 790, fU(44, 800), '#bcd6ff'); text(ctx, 'bora wind · angin jatuh yang DINGIN', 175, 840, fI(32), C.cream); });
    title(ctx, t, 'bora', 'Angin jatuh yang dingin: bora');
  });
}

run({
  DUR, no: 8, code: 'B01-08', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Angin Lokal', sub: 'angin laut-darat, lembah-gunung, fohn, dan bora',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-09 · Sirkulasi Tiga Sel dan Angin Pasat',
  SCN: [['hook', 0], ['definisi', 3], ['pantai', 4], ['lembah', 15], ['fohn', 23], ['petafohn', 28], ['bora', 34], ['soal', 36], ['jebakan', 40], ['ringkas', 43], ['outro', 47]],
  TERMS: [
    ['Angin lokal', 'local wind', 'Akibat beda pemanasan skala kecil, berganti dalam sehari', 3],
    ['Angin laut', 'sea breeze', 'Siang: dari laut ke darat (±09.00–16.00)', 8],
    ['Angin darat', 'land breeze', 'Malam: dari darat ke laut (±20.00–06.00)', 12],
    ['Angin lembah', 'valley breeze · anabatic', 'Siang: udara naik dari lembah menyusuri lereng', 18],
    ['Angin gunung', 'mountain breeze · katabatic', 'Malam: udara dingin turun ke lembah', 21],
    ['Angin fohn', 'foehn wind', 'Angin jatuh yang kering dan panas', 24],
    ['Angin bora', 'bora wind', 'Angin jatuh yang dingin (contoh: Adriatik)', 34],
  ],
  hook: { cards: [], punch: [2, ''] },
  soal: {
    q: 'Nelayan tradisional di pantai utara Jawa berangkat melaut pukul 03.00. Angin yang mereka manfaatkan dan penyebabnya adalah …',
    opts: ['angin laut, laut lebih cepat dingin', 'angin gunung, udara lereng turun', 'angin fohn, udara kering turun', 'angin pasat, bertiup sepanjang tahun', 'angin darat, darat lebih cepat dingin'], ans: 4, optFs: 26,
    ansT: () => tw('jawabannya', U_(39).v0 - 0.3),
    steps: () => [[U_(37).v0, '1) Dini hari', C.forest3, 28], [tw('daratan', U_(37).v0), 'darat lebih dingin dari laut', C.cream, 36], [tw('tekanan', U_(37).v0), 'tekanan darat lebih TINGGI', C.cream, 36], [U_(38).v0, '2) Arah angin', C.forest3, 28], [tw('darat', U_(38).v0), 'darat ke laut = ANGIN DARAT', C.amber, 46]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(41).v0, 'Angin laut bertiup dari darat ke laut', 'Angin laut: DARI laut ke darat (nama = asal)', tw('mengikuti', U_(41).v0)],
      [U_(42).v0, 'Fohn dan bora sama-sama panas', 'Fohn kering-panas, bora DINGIN', tw('bora', U_(42).v0)]],
  },
  ringkas: {
    items: () => [[tw('laut', U_(44).v0), 'Angin laut siang, angin darat malam'], [tw('lembah', U_(44).v0), 'Angin lembah siang, angin gunung malam'], [tw('fohn', U_(44).v0), 'Angin fohn: kering dan panas']],
  },
  scenes: { hook: sHook, definisi: sDefinisi, pantai: sPantai, lembah: sLembah, fohn: sFohn, petafohn: sPetaFohn, bora: sBora },
  async init() {
    W50 = await fetch('assets/world50.json').then((r) => r.json());
    JAVA = G.subset(W50, [100, 120, -12, 0]); INDO = G.subset(W50, [85, 150, -20, 15]); ADR = G.subset(W50, [8, 25, 38, 49]);
  },
});
