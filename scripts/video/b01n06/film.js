// B01-06 · Tekanan Udara dan Lahirnya Angin · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun, warnIcon } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 242.0;

let W110 = null, W50 = null, RID = null, PHONE = null;
// fields
const F_ID = G.field([[128, 14, -16, 3.6, 3.6], [128, -27, 9, 16, 8], [152, 24, 5, 10, 8], [105, -3, -3, 15, 5]], 1009);
const F_JAN = G.field([[100, 48, 24, 22, 14], [185, 52, -14, 18, 10], [132, -20, -9, 14, 9], [80, -30, 8, 25, 8], [210, -30, 6, 25, 8]], 1010);
const F_JUL = G.field([[75, 30, -12, 25, 14], [205, 35, 12, 25, 10], [135, -28, 10, 18, 9], [60, -30, 8, 15, 8], [100, 55, -3, 20, 10]], 1010);
const EXT_ID = [88, 152, -32, 24];
const LV = []; for (let p = 994; p <= 1018; p += 2) LV.push(p);
let CS_ID = null, SD_ID = null, SD_PH = null, SD_GL = null;

// ---------------------------------------------------------------- hook: tilted phone with live weather map
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#e9eef1', () => {
    // backdrop: big faded map
    const bp = G.mapProj({ x: 0, y: 0, w: W, h: H }, [80 + t * 0.4, 160 + t * 0.4, -30, 15]);
    ctx.save(); ctx.globalAlpha = 0.35; G.drawMap(ctx, RID, bp, { t, sea: '#dfe9ef', land: '#efe6d2', shadow: 'rgba(0,0,0,0)', waves: false }); ctx.restore();
    // phone screen (offscreen)
    const pc = PHONE.getContext('2d'); const pw = PHONE.width, ph = PHONE.height;
    const z = 1 - 0.08 * ap(t, 4, 10, E.inOutCubic);
    const ext = [118 - 18 * z, 118 + 18 * z, 4 - 32 * z, 4 + 33 * z];
    const pp = G.mapProj({ x: 0, y: 0, w: pw, h: ph }, ext);
    pc.save(); pc.clearRect(0, 0, pw, ph);
    G.drawMap(pc, RID, pp, { t, depth: 4 });
    const rv = ap(t, U_(1).v0 - 0.5, 2.0, E.linear);
    G.drawIsobars(pc, CS_ID, pp, { reveal: rv, ext, width: 3, fs: 18 });
    if (rv > 0.2) G.drawFlow(pc, F_ID, pp, SD_PH, t, { speed: 1.4, vmax: 5, color: 'rgba(22,58,80,0.8)', width: 3, alpha: clamp(rv * 2) });
    G.drawCenters(pc, F_ID.centers, pp, sp(t, tw('H', U_(1).v0) - 0.2, SPRING.bouncy), t);
    // status bar
    pc.fillStyle = 'rgba(22,41,35,0.85)'; pc.fillRect(0, 0, pw, 90); text(pc, 'Peta Angin', 30, 60, fU(34, 700), C.cream); text(pc, '09.41', pw - 30, 60, fU(30, 600), C.forest3, 'right');
    pc.restore();
    // place phone with 3-D-ish tilt
    const k = sp(t, 3.1, SPRING.gentle); const yaw = 0.18 * Math.sin(t * 0.5) - 0.1;
    ctx.save(); ctx.translate(W / 2 - 80, 560 + (1 - k) * 300);
    ctx.transform(Math.cos(yaw), Math.sin(yaw) * 0.25, -0.28 + 0.1 * Math.sin(t * 0.4), 1, 0, 0);
    ctx.scale(0.72, 0.72);
    ctx.shadowColor = 'rgba(0,0,0,0.35)'; ctx.shadowBlur = 60; ctx.shadowOffsetY = 40;
    rrect(ctx, -pw / 2 - 26, -ph / 2 - 26, pw + 52, ph + 52, 70); ctx.fillStyle = '#16231f'; ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.save(); rrect(ctx, -pw / 2, -ph / 2, pw, ph, 48); ctx.clip(); ctx.drawImage(PHONE, -pw / 2, -ph / 2); ctx.restore();
    rrect(ctx, -70, -ph / 2 - 10, 140, 26, 13); ctx.fillStyle = '#16231f'; ctx.fill();
    ctx.restore();
    // call-outs
    show(ctx, t, U_(2).v0, () => { pill(ctx, 'ke mana angin bertiup?', 1330, 420, fU(32, 700), C.forest, C.cream, 24, 62, 'center'); });
    show(ctx, t, tw('kencang', U_(2).v0) - 0.4, () => { pill(ctx, 'seberapa kencang?', 1330, 520, fU(32, 700), C.clay, C.cream, 24, 62, 'center'); });
  });
}

// ---------------------------------------------------------------- definisi: streaks over paper-cut landscape
function sDefinisi(ctx, t) {
  scene(ctx, t, 'definisi', '#dcebf3', () => {
    // paper-cut hills (parallax)
    const layers = [['#cfe0c9', 600, 0.2], ['#a9cfa0', 700, 0.4], ['#7fb07a', 800, 0.7], ['#e8dcc0', 900, 1.0]];
    layers.forEach(([col, y0, par], li) => { ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(0, H); for (let x = 0; x <= W; x += 20) ctx.lineTo(x, y0 + 40 * Math.sin((x + t * 40 * par) * 0.004 + li) + 20 * Math.sin((x + t * 40 * par) * 0.011 + li * 2)); ctx.lineTo(W, H); ctx.closePath(); ctx.shadowColor = 'rgba(0,0,0,0.12)'; ctx.shadowBlur = 16; ctx.shadowOffsetY = -6; ctx.fill(); ctx.shadowColor = 'transparent'; });
    // wind streaks
    for (let i = 0; i < 26; i++) { const y = 260 + hash01(i, 3) * 380, ph = (t * 0.5 + hash01(i, 5)) % 1, x = -300 + ph * (W + 600); ctx.strokeStyle = `rgba(255,255,255,${0.7 * Math.sin(ph * Math.PI)})`; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.beginPath(); for (let k = 0; k < 12; k++) { const xx = x - k * 22, yy = y + 10 * Math.sin((xx + t * 60) * 0.01); k ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
    const k = sp(t, SC.definisi[0] + 0.2, SPRING.snappy);
    ctx.save(); ctx.globalAlpha *= clamp(k * 1.5); ctx.translate(0, (1 - k) * 40);
    text(ctx, 'angin', W / 2, 330, fD(170), C.forest, 'center');
    text(ctx, '= udara yang bergerak secara horizontal', W / 2, 410, fU(40, 700), C.ink, 'center');
    ctx.restore();
    const chain = [['perbedaan pemanasan', 'pemanasan', C.amber], ['perbedaan tekanan', 'tekanan', C.clay], ['angin', 'Penyebab', C.forest]];
    chain.forEach(([s, w, col], i) => {
      const t0 = i === 2 ? tw('Penyebab', U_(4).v0) : tw(w, U_(4).v0, i === 0 ? 0 : 1); const kk = sp(t, i === 2 ? t0 : t0 - 0.2, SPRING.bouncy);
      if (kk <= 0) return; const x = 470 + (2 - i) * 490, y = 560;
      ctx.save(); ctx.translate(x, y); ctx.scale(kk, kk); ctx.font = fU(34, 700); const w_ = ctx.measureText(s).width + 60; rrect(ctx, -w_ / 2, -38, w_, 76, 38); ctx.fillStyle = col; ctx.fill(); text(ctx, s, 0, 12, fU(34, 700), C.cream, 'center'); ctx.restore();
      if (i < 2 && kk > 0.8) arrowLine(ctx, x - 230, y, x - 260, y, C.ink, 5, 16);
    });
    show(ctx, t, tw('Penyebab', U_(4).v0), () => text(ctx, 'dibaca dari kanan: pemanasan melahirkan tekanan, tekanan melahirkan angin', W / 2, 660, fU(26, 600), C.gray, 'center'));
  });
}

// ---------------------------------------------------------------- diorama (isometric, orbiting camera)
function gauge(ctx, x, y, r, val, label, col) {
  circle(ctx, x, y, r); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  for (let i = 0; i <= 10; i++) { const a = Math.PI * (0.8 + 1.4 * i / 10); ctx.strokeStyle = C.gray; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r * 0.78, y + Math.sin(a) * r * 0.78); ctx.lineTo(x + Math.cos(a) * r * 0.9, y + Math.sin(a) * r * 0.9); ctx.stroke(); }
  const a = Math.PI * (0.8 + 1.4 * clamp((val - 996) / 28)); arrowLine(ctx, x, y, x + Math.cos(a) * r * 0.72, y + Math.sin(a) * r * 0.72, col, 5, 14);
  circle(ctx, x, y, 6); ctx.fillStyle = C.ink; ctx.fill();
  text(ctx, `${Math.round(val)} mb`, x, y + r * 0.55, fU(r * 0.24, 700), C.ink, 'center');
  pill(ctx, label, x, y - r - 26, fU(26, 800), col, C.cream, 16, 46, 'center');
}
function sDiorama(ctx, t) {
  scene(ctx, t, 'diorama', '#eef3f6', () => {
    title(ctx, t, 'diorama', 'Pemanasan berbeda, tekanan berbeda');
    const az = 0.22 + 0.16 * Math.sin((t - SC.diorama[0]) * 0.18);
    const P = G.iso(900, 640, 56, az, 0.48);
    const heat = ap(t, U_(6).v0, 2.5);
    // slab
    G.isoBox(ctx, P, -0.5, -0.5, -0.8, 11, 7, 0.8, '#d9c9a4', '#b9a27a', '#a68d63');
    G.isoBox(ctx, P, 0, 0, 0, 5, 6, 0.12, mix('#d8c08a', '#e9925e', heat), '#b9864f', '#a9744a');
    G.isoBox(ctx, P, 5, 0, 0, 5, 6, 0.12, '#9cc29a', '#7a9f78', '#6b8f69');
    for (let i = 0; i < 5; i++) { const [x, y] = P(6 + (i % 3) * 1.4, 1 + Math.floor(i / 3) * 3 + 0.5, 0.12); ctx.fillStyle = '#5e7f45'; ctx.fillRect(x - 3, y - 26, 6, 26); circle(ctx, x, y - 34, 16); ctx.fillStyle = '#3f8a52'; ctx.fill(); }
    // heat shimmer
    if (heat > 0) for (let i = 0; i < 10; i++) { const ph = (t * 0.6 + hash01(i, 2)) % 1; const [x, y] = P(0.6 + hash01(i, 4) * 3.8, 0.6 + hash01(i, 6) * 4.8, 0.2 + ph * 2.2); ctx.strokeStyle = `rgba(233,146,94,${0.6 * heat * (1 - ph)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.bezierCurveTo(x + 8, y - 10, x - 8, y - 20, x, y - 30); ctx.stroke(); }
    // sun
    const [sx, sy] = P(2.5, 3, 8.2); sun(ctx, sx, sy, 44, t, ap(t, U_(6).v0 - 0.4, 0.6));
    // columns (wire)
    const col = (x0, colr, a) => { ctx.save(); ctx.globalAlpha *= a; ctx.strokeStyle = colr; ctx.lineWidth = 2; ctx.setLineDash([8, 8]); const c = [[x0, 0.5], [x0 + 4, 0.5], [x0 + 4, 5.5], [x0, 5.5]]; [0, 6].forEach((z) => { ctx.beginPath(); c.forEach(([a_, b], i) => { const [X, Y] = P(a_, b, z); i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y); }); ctx.closePath(); ctx.stroke(); }); c.forEach(([a_, b]) => { const p1 = P(a_, b, 0), p2 = P(a_, b, 6); ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke(); }); ctx.setLineDash([]); ctx.restore(); };
    col(0.5, C.clay, ap(t, U_(7).v0 - 0.5, 0.5)); col(5.5, C.blue, ap(t, U_(10).v0, 0.5));
    // particles on circulation loop
    const on = [ap(t, U_(7).v0, 0.6), ap(t, U_(13).v0, 0.6), ap(t, U_(11).v0, 0.6), ap(t, U_(13).v0, 0.6)];
    const seg = [[[2.5, 0.4], [2.5, 5.6]], [[2.5, 5.6], [7.5, 5.6]], [[7.5, 5.6], [7.5, 0.4]], [[7.5, 0.4], [2.5, 0.4]]];
    for (let i = 0; i < 160; i++) {
      const y = 0.8 + hash01(i, 11) * 4.4, s = ((t * 0.09 + hash01(i, 12)) % 1) * 4, si = Math.floor(s), f = s - si; const a = on[si]; if (a <= 0) continue;
      const [[x1, z1], [x2, z2]] = seg[si]; const jx = (hash01(i, 14) - 0.5) * 1.4, jz = (hash01(i, 15) - 0.5) * 0.6;
      const x = lerp(x1, x2, f) + (si % 2 === 0 ? jx : 0), z = lerp(z1, z2, f) + (si % 2 === 1 ? jz : 0);
      const [X, Y] = P(x, y, z); circle(ctx, X, Y, si === 3 ? 6 : 5); ctx.fillStyle = si === 0 ? `rgba(224,121,79,${a})` : si === 2 ? `rgba(43,108,176,${a})` : `rgba(255,255,255,${a})`; ctx.fill();
    }
    // surface wind arrow
    show(ctx, t, tw('angin', U_(14).v0) - 0.6, () => { const p1 = P(8.6, 6.4, 0.2), p2 = P(1.6, 6.4, 0.2); arrowLine(ctx, p1[0], p1[1], p2[0], p2[1], C.forest, 12, 34); const m = P(5, 6.9, 0.2); pill(ctx, 'ANGIN: tinggi ke rendah', m[0], m[1] + 40, fU(30, 800), C.forest, C.cream, 22, 56, 'center'); });
    // gauges
    show(ctx, t, U_(8).v0, () => { const [x, y] = P(2.5, 3, 7.6); gauge(ctx, x - 120, y - 30, 80, lerp(1013, 1004, ap(t, U_(8).v0, 1.5)), 'TEKANAN RENDAH', C.clay); });
    show(ctx, t, U_(11).v0 + 1.5, () => { const [x, y] = P(7.5, 3, 7.6); gauge(ctx, x + 120, y - 30, 80, lerp(1013, 1018, ap(t, U_(11).v0 + 1.5, 1.5)), 'TEKANAN TINGGI', C.blue); });
    show(ctx, t, U_(9).v0, () => text(ctx, 'thermal low', 300, 860, fI(52), C.clayD));
    show(ctx, t, U_(12).v0, () => text(ctx, 'high pressure', 1620, 860, fI(52), C.blue, 'right'));
    // balloon inset
    const pb = ap(t, U_(13).v0, 0.5) * (1 - ap(t, U_(14).v0 + 0.5, 0.4));
    if (pb > 0) {
      ctx.save(); ctx.globalAlpha *= pb; card(ctx, 1460, 320, 360, 330, { r: 26 });
      const pop = ap(t, tw('ditusuk', U_(13).v0), 0.6); const bx = 1640, by = 470;
      if (pop < 0.3) { ctx.fillStyle = C.clay; ctx.beginPath(); ctx.ellipse(bx, by, 70, 86, 0, 0, Math.PI * 2); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx, by + 86); ctx.lineTo(bx, by + 150); ctx.stroke(); }
      for (let i = 0; i < 24; i++) { const a = i / 24 * Math.PI * 2, r = 20 + pop * 140; circle(ctx, bx + Math.cos(a) * r, by + Math.sin(a) * r, 5 * (1 - pop * 0.6)); ctx.fillStyle = `rgba(43,108,176,${pop})`; ctx.fill(); }
      text(ctx, 'udara keluar: padat ke renggang', 1640, 625, fU(22, 700), C.ink, 'center'); ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- barometer
function sBarometer(ctx, t) {
  scene(ctx, t, 'barometer', C.sand, () => {
    title(ctx, t, 'barometer', 'Tekanan diukur dengan barometer');
    const k = sp(t, SC.barometer[0] + 0.2, SPRING.gentle); const cx = 640, cy = 600, r = 270 * k;
    if (r > 5) {
      const g = ctx.createRadialGradient(cx - 60, cy - 60, 20, cx, cy, r * 1.15); g.addColorStop(0, '#d7b56d'); g.addColorStop(1, '#8a6a2c'); circle(ctx, cx, cy, r * 1.12); ctx.fillStyle = g; ctx.fill();
      circle(ctx, cx, cy, r); ctx.fillStyle = C.cream; ctx.fill();
      for (let v = 960; v <= 1060; v += 5) { const a = Math.PI * (0.75 + 1.5 * (v - 960) / 100), big = v % 20 === 0; ctx.strokeStyle = C.ink; ctx.lineWidth = big ? 4 : 2; ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * r * (big ? 0.78 : 0.84), cy + Math.sin(a) * r * (big ? 0.78 : 0.84)); ctx.lineTo(cx + Math.cos(a) * r * 0.92, cy + Math.sin(a) * r * 0.92); ctx.stroke(); if (big) text(ctx, `${v}`, cx + Math.cos(a) * r * 0.64, cy + Math.sin(a) * r * 0.64 + 9, fU(r * 0.09, 700), C.ink, 'center'); }
      [['HUJAN', 0.95], ['BERUBAH', 1.5], ['CERAH', 2.05]].forEach(([s, a]) => text(ctx, s, cx + Math.cos(Math.PI * a) * r * 0.42, cy + Math.sin(Math.PI * a) * r * 0.42, fU(r * 0.07, 700), C.gray, 'center'));
      const v = 1013 + 14 * Math.sin((t - SC.barometer[0]) * 0.9) * (1 - ap(t, U_(16).v0 + 1, 2)); const a = Math.PI * (0.75 + 1.5 * (v - 960) / 100);
      arrowLine(ctx, cx - Math.cos(a) * r * 0.15, cy - Math.sin(a) * r * 0.15, cx + Math.cos(a) * r * 0.8, cy + Math.sin(a) * r * 0.8, C.clayD, 8, 26);
      circle(ctx, cx, cy, 16); ctx.fillStyle = C.ink; ctx.fill();
      text(ctx, 'mb', cx, cy + r * 0.45, fU(r * 0.11, 800), C.clayD, 'center');
    }
    show(ctx, t, U_(15).v0 + 1.5, () => { card(ctx, 1080, 330, 740, 200, { r: 26, bg: C.forest }); text(ctx, 'satuan tekanan', 1120, 395, fU(28, 600), C.forest3); text(ctx, 'milibar (mb)', 1120, 470, fU(56, 800), C.amber); });
    show(ctx, t, U_(16).v0, () => { card(ctx, 1080, 570, 740, 200, { r: 26 }); text(ctx, '1 mb = 1 hPa', 1120, 690, fU(70, 800), C.ink); text(ctx, 'hektopascal', 1120, 740, fI(34), C.clayD); });
  });
}

// ---------------------------------------------------------------- isobar map
const BOX = { x: 110, y: 240, w: 1700, h: 680 };
function zoomExt(t, t0, ext, k = 0.08) { const z = ap(t, t0, 18, E.inOutCubic) * k; const cx = (ext[0] + ext[1]) / 2, cy = (ext[2] + ext[3]) / 2; return [lerp(ext[0], cx, z), lerp(ext[1], cx, z), lerp(ext[2], cy, z), lerp(ext[3], cy, z)]; }
function sIsobar(ctx, t) {
  scene(ctx, t, 'isobar', C.sand, () => {
    const ext = zoomExt(t, SC.isobar[0], [90, 152, -30, 21]);
    const pr = G.mapProj(BOX, ext);
    card(ctx, BOX.x - 8, BOX.y - 8, BOX.w + 16, BOX.h + 16, { r: 30 });
    G.drawMap(ctx, RID, pr, { t });
    ctx.save(); rrect(ctx, BOX.x, BOX.y, BOX.w, BOX.h, 26); ctx.clip();
    G.graticule(ctx, pr, ext, 10);
    const rv = ap(t, U_(17).v0 + 0.5, 3.0, E.linear);
    G.drawIsobars(ctx, CS_ID, pr, { reveal: rv, ext, width: 3.2, fs: 20 });
    if (rv > 0.3) G.drawFlow(ctx, F_ID, pr, SD_ID, t, { speed: 1.4, vmax: 5, color: 'rgba(22,58,80,0.75)', width: 2.8, alpha: 0.9 });
    const lang = t >= U_(20).v0 + 0.5 && t < U_(20).v0 + 4.5 ? 'id' : 'en';
    G.drawCenters(ctx, F_ID.centers, pr, sp(t, U_(19).v0, SPRING.bouncy), t, { lang });
    ctx.restore();
    title(ctx, t, 'isobar', 'Isobar: garis bertekanan sama');
    show(ctx, t, U_(18).v0, () => pill(ctx, 'isobar', 1600, 300, fI(38), C.forest, C.cream, 26, 62, 'center'));
    show(ctx, t, U_(19).v0 + 1, () => { card(ctx, 140, 720, 520, 170, { r: 22 }); text(ctx, 'H = high · tekanan tinggi', 175, 790, fU(30, 700), C.blue); text(ctx, 'L = low · tekanan rendah', 175, 845, fU(30, 700), C.clay); });
    show(ctx, t, U_(20).v0, () => pill(ctx, 'peta Indonesia: T = tinggi, R = rendah', 900, 860, fU(26, 700), C.forest, C.cream, 18, 50, 'center'));
    text(ctx, 'medan tekanan ilustratif · isobar tiap 2 mb', BOX.x + BOX.w - 24, BOX.y + BOX.h - 18, fU(18, 600), C.gray, 'right');
  });
}

// ---------------------------------------------------------------- gradien barometrik
function ruler(ctx, p1, p2, label, col) {
  ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.setLineDash([14, 10]); ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke(); ctx.setLineDash([]);
  [p1, p2].forEach(([x, y]) => { circle(ctx, x, y, 10); ctx.fillStyle = col; ctx.fill(); });
  pill(ctx, label, (p1[0] + p2[0]) / 2, Math.min(p1[1], p2[1]) - 36, fU(24, 800), col, C.cream, 14, 44, 'center');
}
function sGradien(ctx, t) {
  scene(ctx, t, 'gradien', C.sand, () => {
    const z = ap(t, SC.gradien[0], 2.5, E.inOutCubic);
    const ext = [lerp(90, 102, z), lerp(152, 146, z), lerp(-30, -31, z), lerp(21, 22, z)];
    const pr = G.mapProj(BOX, ext);
    card(ctx, BOX.x - 8, BOX.y - 8, BOX.w + 16, BOX.h + 16, { r: 30 });
    G.drawMap(ctx, RID, pr, { t });
    ctx.save(); rrect(ctx, BOX.x, BOX.y, BOX.w, BOX.h, 26); ctx.clip();
    const hi = (L) => t > U_(27).v0 && L <= 1000;
    G.drawIsobars(ctx, CS_ID, pr, { width: 3, fs: 18, hi });
    G.drawFlow(ctx, F_ID, pr, SD_ID, t, { speed: 1.5, vmax: 7, color: 'rgba(22,58,80,0.8)', width: 3, alpha: 0.95 });
    G.drawCenters(ctx, F_ID.centers, pr, 1, t);
    ctx.restore();
    title(ctx, t, 'gradien', 'Gradien barometrik: rapat berarti kencang');
    show(ctx, t, U_(22).v0, () => { card(ctx, 140, 270, 640, 190, { r: 24, bg: C.forest }); text(ctx, 'gradien barometrik =', 175, 330, fU(28, 600), C.forest3); text(ctx, 'selisih tekanan ÷ jarak', 175, 390, fU(40, 800), C.amber); text(ctx, 'pressure gradient', 175, 438, fI(30), C.cream); });
    show(ctx, t, U_(23).v0, () => { card(ctx, 140, 480, 640, 120, { r: 22 }); text(ctx, 'satuan soal: mb per 111 km', 175, 532, fU(30, 800), C.ink); text(ctx, '111 km = 1° lintang', 175, 576, fU(26, 600), C.gray); const a = pr(108, -20), b = pr(108, -21); ctx.strokeStyle = C.clay; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); text(ctx, '1° = 111 km', a[0] + 14, (a[1] + b[1]) / 2 + 8, fU(22, 800), C.clayD); });
    show(ctx, t, U_(25).v0, () => ruler(ctx, pr(121.5, 14), pr(125.5, 14), 'RAPAT: kencang', C.clay));
    show(ctx, t, U_(26).v0, () => ruler(ctx, pr(118, -25), pr(140, -25), 'RENGGANG: lemah', C.blue));
    show(ctx, t, U_(27).v0, () => { const c = pr(128, 14); for (let k = 0; k < 3; k++) { const ph = (t * 0.7 + k / 3) % 1; circle(ctx, c[0], c[1], 30 + ph * 120); ctx.strokeStyle = `rgba(152,63,41,${1 - ph})`; ctx.lineWidth = 4; ctx.stroke(); } pill(ctx, 'badai: isobar sangat rapat', c[0] + 160, c[1] - 90, fU(24, 800), C.clayD, C.cream, 14, 44); });
    show(ctx, t, U_(28).v0, () => { const c = pr(128, -27); pill(ctx, 'tekanan tinggi luas: tenang', c[0], c[1] + 70, fU(24, 800), C.blue, C.cream, 14, 44, 'center'); });
    text(ctx, 'partikel: arah gaya gradien tekanan saja (disederhanakan)', BOX.x + BOX.w - 24, BOX.y + BOX.h - 18, fU(18, 600), C.gray, 'right');
  });
}

// ---------------------------------------------------------------- gaya gradien tekanan
function sGaya(ctx, t) {
  scene(ctx, t, 'gaya', '#eef3f6', () => {
    title(ctx, t, 'gaya', 'Gaya gradien tekanan');
    const t0 = SC.gaya[0]; const Y = (k) => 340 + k * 170;
    [1012, 1008, 1004].forEach((L, k) => { const p = ap(t, t0 + 0.2 + k * 0.25, 0.8, E.inOutCubic); ctx.strokeStyle = C.forest; ctx.lineWidth = 4; ctx.beginPath(); for (let x = 110; x <= 110 + 1700 * p; x += 10) { const y = Y(k) + 18 * Math.sin(x * 0.004 + k); x === 110 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke(); if (p > 0.9) pill(ctx, `${L} mb`, 180, Y(k), fU(22, 800), C.cream, C.forest, 10, 38, 'center'); });
    text(ctx, 'TINGGI', 1700, 300, fU(30, 800), C.blue, 'center'); text(ctx, 'RENDAH', 1700, 760, fU(30, 800), C.clay, 'center');
    // parcel
    const mv = ap(t, U_(31).v0, 3.0, E.inOutCubic) * (1 - ap(t, U_(32).v0 + 0.2, 0.01));
    const px = 900, py = lerp(320, 700, mv);
    circle(ctx, px, py, 34); ctx.fillStyle = C.amber; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke();
    show(ctx, t, U_(29).v0 + 1, () => { arrowLine(ctx, px, py + 40, px, py + 180, C.clay, 10, 30); text(ctx, 'pressure gradient force', px + 30, py + 130, fI(36), C.clayD); });
    show(ctx, t, U_(30).v0, () => { ctx.strokeStyle = C.ink; ctx.lineWidth = 2; const y = Y(0) + 18 * Math.sin(px * 0.004); ctx.strokeRect(px - 1, y - 30, 30, 30); pill(ctx, 'tegak lurus isobar', px - 60, Y(0) - 60, fU(24, 800), C.forest, C.cream, 14, 44, 'right'); });
    show(ctx, t, U_(32).v0, () => { ctx.setLineDash([12, 10]); ctx.strokeStyle = C.clayD; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(900, 320); ctx.bezierCurveTo(900, 480, 1000, 600, 1250, 650); ctx.stroke(); ctx.setLineDash([]); circle(ctx, 1290, 640, 40); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, '?', 1290, 660, fU(54, 800), C.cream, 'center'); });
    show(ctx, t, U_(33).v0, () => pill(ctx, 'video berikutnya: gaya Coriolis', 1290, 760, fU(28, 800), C.forest, C.cream, 20, 54, 'center'));
  });
}

// ---------------------------------------------------------------- musim: 3-D globe Januari vs Juli
function sMusim(ctx, t) {
  scene(ctx, t, 'musim', '#0f2233', () => {
    const t0 = SC.musim[0];
    for (let i = 0; i < 80; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * H, 1 + hash01(i, 3) * 1.6); ctx.fillStyle = `rgba(255,255,255,${0.3 + 0.5 * hash01(i, 4)})`; ctx.fill(); }
    const spin = ap(t, t0, 3.5, E.inOutCubic);
    const lon0 = lerp(20, 112, spin) + 4 * Math.sin((t - t0) * 0.25), lat0 = lerp(0, 12, spin);
    const g = G.globeProj(lon0, lat0, 390, 700, 600);
    G.drawGlobe(ctx, W110, g);
    const kJul = ap(t, U_(37).v0, 1.6, E.inOutCubic);
    const F = G.blend(F_JAN, F_JUL, kJul);
    const show_ = ap(t, U_(35).v0 - 0.5, 1.0);
    if (show_ > 0) {
      ctx.save(); ctx.globalAlpha *= show_; circle(ctx, g.cx, g.cy, g.R); ctx.clip();
      const cs = G.contours(F.P, [40, 220, -55, 75], 3, [996, 1000, 1004, 1008, 1012, 1016, 1020, 1024, 1028, 1032]);
      G.drawIsobars(ctx, cs, g, { color: 'rgba(255,255,255,0.55)', width: 2.4, labels: false });
      G.drawFlow(ctx, F, g, SD_GL, t, { speed: 1.6, vmax: 6, color: 'rgba(255,240,200,0.95)', width: 2.6, life: 2.6 });
      ctx.restore();
      const cen = kJul < 0.5 ? F_JAN.centers : F_JUL.centers; G.drawCenters(ctx, cen, g, Math.abs(kJul - 0.5) * 2, t, { minA: 8 });
    }
    // month switch
    const k = ap(t, t0 + 0.6, 0.6);
    ctx.save(); ctx.globalAlpha *= k;
    rrect(ctx, 1220, 300, 600, 96, 48); ctx.fillStyle = 'rgba(255,255,255,0.1)'; ctx.fill();
    rrect(ctx, 1226 + 294 * kJul, 306, 294, 84, 42); ctx.fillStyle = kJul < 0.5 ? C.blue : C.clay; ctx.fill();
    text(ctx, 'JANUARI', 1373, 362, fU(32, 800), C.cream, 'center'); text(ctx, 'JULI', 1667, 362, fU(32, 800), C.cream, 'center');
    const lines = kJul < 0.5 ? [['Asia dingin', 'tekanan tinggi Siberia', C.blue, U_(35).v0], ['Australia musim panas', 'tekanan rendah', C.clay, U_(36).v0]] : [['Asia panas', 'tekanan rendah', C.clay, U_(37).v0 + 0.6], ['Australia musim dingin', 'tekanan tinggi', C.blue, U_(37).v0 + 1.2]];
    lines.forEach(([a, b, col, tt], i) => show(ctx, t, tt, () => { rrect(ctx, 1220, 440 + i * 170, 600, 145, 24); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1220, 440 + i * 170, 12, 145, 6); ctx.fillStyle = col; ctx.fill(); text(ctx, a, 1260, 500 + i * 170, fU(34, 800), C.cream); text(ctx, b, 1260, 548 + i * 170, fU(28, 600), mix(col, '#ffffff', 0.4)); }));
    show(ctx, t, U_(35).v0 + 1.5, () => { if (kJul < 0.5) text(ctx, 'Siberian High', 1260, 800 - 0, fI(40), '#bcd6ff'); });
    show(ctx, t, U_(38).v0, () => pill(ctx, 'cikal bakal angin MONSUN Indonesia', 1520, 850, fU(28, 800), C.amber, C.ink, 22, 56, 'center'));
    ctx.restore();
    title(ctx, t, 'musim', 'Pola tekanan musiman: Januari dan Juli', C.cream);
  });
}

// ---------------------------------------------------------------- config
run({
  DUR, no: 6, code: 'B01-06', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Tekanan Udara & Angin', sub: 'isobar, gradien barometrik, dan lahirnya angin',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-07 · Gaya Coriolis dan Gesekan',
  SCN: [['hook', 0], ['definisi', 3], ['diorama', 5], ['barometer', 15], ['isobar', 17], ['gradien', 21], ['gaya', 29], ['musim', 34], ['soal', 39], ['jebakan', 45], ['ringkas', 49], ['outro', 52]],
  TERMS: [
    ['Tekanan rendah termal', 'thermal low', 'Udara dipanaskan, mengembang, naik; tekanan permukaan turun', 9],
    ['Tekanan tinggi', 'high pressure', 'Udara dingin padat dan turun; tekanan permukaan naik', 12],
    ['Isobar', 'isobar', 'Garis yang menghubungkan tempat bertekanan sama', 17],
    ['Gradien barometrik', 'pressure gradient', 'Selisih tekanan ÷ jarak, mb per 111 km', 22],
    ['Gaya gradien tekanan', 'pressure gradient force', 'Mendorong udara dari tinggi ke rendah, tegak lurus isobar', 29],
    ['Tekanan tinggi Siberia', 'Siberian High', 'Terbentuk saat daratan Asia sangat dingin (Januari)', 35],
  ],
  hook: { cards: [], punch: [0, ''] },
  soal: {
    q: 'Kota P bertekanan 1.012 mb dan kota Q bertekanan 1.004 mb. Jarak P–Q 444 km. Gradien barometrik dan arah angin di antara keduanya adalah …',
    opts: ['8 mb/111 km, dari Q ke P', '2 mb/111 km, dari P ke Q', '2 mb/111 km, dari Q ke P', '0,5 mb/111 km, dari P ke Q', '8 mb/111 km, dari P ke Q'], ans: 1, optFs: 28,
    ansT: () => tw('jawabannya', U_(44).v0 - 0.3),
    steps: () => [[U_(40).v0, '1) Selisih tekanan', C.forest3, 28], [tw('yaitu', U_(40).v0), '1.012 − 1.004 = 8 mb', C.cream, 40],
      [U_(41).v0, '2) Jarak', C.forest3, 28], [tw('atau', U_(41).v0), '444 km = 4 × 111 km', C.cream, 40],
      [U_(42).v0, '3) Gradien', C.forest3, 28], [tw('yaitu', U_(42).v0), '8 ÷ 4 = 2 mb/111 km', C.amber, 50], [U_(43).v0, 'arah: P (tinggi) ke Q (rendah)', C.cream, 34]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(46).v0, 'Angin barat = angin yang menuju ke barat', 'Angin barat DATANG DARI barat (nama = arah asal)', U_(47).v0],
      [U_(48).v0, 'Isobar rapat berarti tekanan tinggi', 'Isobar rapat berarti angin KENCANG', U_(48).v0 + 2.5]],
    extra: (ctx, t) => show(ctx, t, U_(47).v0, () => { const cx = 1660, cy = 385, r = 72; circle(ctx, cx, cy, r); ctx.fillStyle = C.forest1; ctx.fill(); ['U', 'T', 'S', 'B'].forEach((s, i) => { const a = -Math.PI / 2 + i * Math.PI / 2; text(ctx, s, cx + Math.cos(a) * (r - 16), cy + Math.sin(a) * (r - 16) + 8, fU(22, 800), C.forest, 'center'); }); const ph = ((t * 0.8) % 1); arrowLine(ctx, cx - r - 60 + ph * 40, cy, cx - 10 + ph * 40, cy, C.clay, 8, 22); }),
  },
  ringkas: {
    items: () => [[tw('perbedaan', U_(50).v0), 'Beda pemanasan menciptakan beda tekanan'], [tw('udara', U_(50).v0), 'Udara bergerak dari tekanan tinggi ke rendah'], [tw('isobar', U_(50).v0), 'Isobar rapat berarti angin kencang']],
  },
  scenes: { hook: sHook, definisi: sDefinisi, diorama: sDiorama, barometer: sBarometer, isobar: sIsobar, gradien: sGradien, gaya: sGaya, musim: sMusim },
  async init() {
    W110 = await fetch('assets/world110.json').then((r) => r.json());
    W50 = await fetch('assets/world50.json').then((r) => r.json());
    RID = G.subset(W50, [70, 170, -50, 50]);
    PHONE = document.createElement('canvas'); PHONE.width = 560; PHONE.height = 1000;
    CS_ID = G.contours(F_ID.P, [70, 170, -45, 45], 1, LV);
    SD_ID = G.seeds(420, [90, 152, -30, 22], 3); SD_PH = G.seeds(260, [96, 140, -30, 38], 5); SD_GL = G.seeds(520, [40, 220, -55, 75], 9);
  },
});
