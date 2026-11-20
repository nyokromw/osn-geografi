// B01-07 · Gaya Coriolis dan Gesekan · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 233.4;
let W110 = null, W50 = null, TROP = null, SIM_G = null, SIM_F = null, SIM_FS = null;

function stars(ctx, n = 90) { for (let i = 0; i < n; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * H, 1 + hash01(i, 3) * 1.6); ctx.fillStyle = `rgba(255,255,255,${0.25 + 0.5 * hash01(i, 4)})`; ctx.fill(); } }
// spiral cloud system; dir +1 = counter-clockwise (BBU), -1 = clockwise (BBS)
function hurricane(ctx, x, y, r, t, dir, a = 1) {
  if (a <= 0 || r <= 2) return; ctx.save(); ctx.globalAlpha *= a; ctx.translate(x, y); ctx.rotate(-dir * t * 1.6);
  for (let k = 0; k < 4; k++) { ctx.beginPath(); for (let i = 0; i <= 40; i++) { const f = i / 40, ang = k * Math.PI / 2 + dir * -f * 3.2, rr = r * (0.15 + 0.85 * f); const px = Math.cos(ang) * rr, py = Math.sin(ang) * rr; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = r * 0.16; ctx.lineCap = 'round'; ctx.stroke(); }
  circle(ctx, 0, 0, r * 0.22); ctx.fillStyle = 'rgba(255,255,255,0.95)'; ctx.fill(); circle(ctx, 0, 0, r * 0.07); ctx.fillStyle = '#5a7fa0'; ctx.fill();
  ctx.restore();
}
function rotArrow(ctx, x, y, r, dir, col, t) { const a0 = t * 2 * dir; ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(x, y, r, a0, a0 + dir * 4.5, dir < 0); ctx.stroke(); const ae = a0 + dir * 4.5; const ex = x + Math.cos(ae) * r, ey = y + Math.sin(ae) * r; arrowLine(ctx, ex - Math.sin(ae) * -dir * 2, ey + Math.cos(ae) * -dir * 2, ex - Math.sin(ae) * dir * 0.1 + Math.cos(ae + dir * Math.PI / 2) * 18, ey + Math.sin(ae + dir * Math.PI / 2) * 18, col, 6, 20); }

// ---------------------------------------------------------------- hook: globe tour of cyclones
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#0f2233', () => {
    stars(ctx);
    const k1 = ap(t, U_(1).v0 - 0.6, 1.4, E.inOutCubic), k2 = ap(t, U_(2).v0 - 0.4, 1.4, E.inOutCubic), k4 = ap(t, U_(4).v0, 1.6, E.inOutCubic);
    const lon0 = lerp(lerp(-75, 128, k1), 110, k2) + k4 * 140 + 3 * Math.sin(t * 0.3), lat0 = lerp(lerp(22, -18, k1), 0, k2);
    const g = G.globeProj(lon0, lat0, 400, W / 2, 590);
    G.drawGlobe(ctx, W110, g);
    ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip();
    const band = ap(t, U_(2).v0 + 0.6, 0.6);
    if (band > 0) { ctx.fillStyle = `rgba(242,177,58,${0.6 * band})`; ctx.beginPath(); for (let lo = lon0 - 88; lo <= lon0 + 88; lo += 2) { const p = g(lo, 5); if (p) ctx.lineTo(p[0], p[1]); } for (let lo = lon0 + 88; lo >= lon0 - 88; lo -= 2) { const p = g(lo, -5); if (p) ctx.lineTo(p[0], p[1]); } ctx.closePath(); ctx.fill(); }
    const pA = g(-75, 26), pB = g(117, -17);
    if (pA) hurricane(ctx, pA[0], pA[1], 80, t, 1, ap(t, 3.2, 0.8));
    if (pB) hurricane(ctx, pB[0], pB[1], 80, t, -1, ap(t, U_(1).v0, 0.8));
    ctx.restore();
    show(ctx, t, U_(0).v0 + 1, () => { if (pA) { rotArrow(ctx, pA[0], pA[1], 120, -1, C.amber, t); pill(ctx, 'BBU: berlawanan arah jarum jam', pA[0], pA[1] - 160, fU(26, 800), C.amber, C.ink, 16, 48, 'center'); } });
    show(ctx, t, U_(1).v0 + 0.6, () => { if (pB) { rotArrow(ctx, pB[0], pB[1], 120, 1, C.clay, t); pill(ctx, 'BBS: searah jarum jam', pB[0], pB[1] + 170, fU(26, 800), C.clay, C.cream, 16, 48, 'center'); } });
    show(ctx, t, U_(2).v0 + 1, () => pill(ctx, 'lintang 0°–5°: hampir tanpa siklon', W / 2, 180, fU(30, 800), C.amber, C.ink, 22, 56, 'center'));
    show(ctx, t, U_(4).v0, () => text(ctx, 'bumi berputar', W / 2, 1000 - 70, fD(90), C.cream, 'center'));
  });
}

// ---------------------------------------------------------------- lempar bola: polar view rotating disk
function sLempar(ctx, t) {
  scene(ctx, t, 'lempar', '#0f2233', () => {
    stars(ctx);
    const t0 = U_(5).v0; const w = 0.35; // rad/s
    const rot = (t - SC.lempar[0]) * w;
    const g = G.globeProj(-rot / G.D2R, 89.9, 360, 620, 600);
    G.drawGlobe(ctx, W110, g, { grid: true });
    text(ctx, 'tampak dari atas kutub utara', 620, 1000 - 50, fU(24, 600), '#9fb7c9', 'center');
    // rotation arrow (counter-clockwise seen from above)
    show(ctx, t, U_(6).v0, () => { ctx.strokeStyle = C.amber; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(620, 600, 410, -0.4, -1.6, true); ctx.stroke(); const ae = -1.6; arrowLine(ctx, 620 + Math.cos(ae + 0.08) * 410, 600 + Math.sin(ae + 0.08) * 410, 620 + Math.cos(ae) * 410 - 14, 600 + Math.sin(ae) * 410 - 4, C.amber, 6, 22); pill(ctx, 'bumi berputar ke timur', 1150, 275, fU(26, 800), C.amber, C.ink, 16, 48); });
    // throws repeat every 5 s
    if (t >= t0) {
      const cyc = 5, n = Math.floor((t - t0) / cyc), tau = (t - t0) - n * cyc, th0 = 1.9 + n * 0.0; const v = 360 / 4.2;
      const T = Math.min(tau, 4.2);
      // inertial straight line
      ctx.setLineDash([10, 10]); ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(620, 600); ctx.lineTo(620 + Math.cos(th0) * v * T, 600 + Math.sin(th0) * v * T); ctx.stroke(); ctx.setLineDash([]);
      // ground trace (rotates with earth) - screen angle = th0 + w*(tau - tau')  [screen y down => ccw is negative]
      const tr = ap(t, U_(7).v0 - 0.5, 0.5);
      if (tr > 0) { ctx.save(); ctx.globalAlpha *= tr; ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.beginPath(); for (let i = 0; i <= 40; i++) { const tp = T * i / 40, ang = th0 - w * (T - tp); const x = 620 + Math.cos(ang) * v * tp, y = 600 + Math.sin(ang) * v * tp; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); ctx.restore(); }
      const bx = 620 + Math.cos(th0) * v * T, by = 600 + Math.sin(th0) * v * T;
      circle(ctx, bx, by, 16); ctx.fillStyle = C.amber; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke();
      // thrower at pole
      circle(ctx, 620, 600, 14); ctx.fillStyle = C.cream; ctx.fill();
    }
    // side panel
    const P = [[U_(5).v0, 'bola dilempar dari kutub ke selatan', 'rgba(255,255,255,0.9)'], [U_(7).v0, 'jejak di permukaan: berbelok ke KANAN', C.clay], [U_(9).v0, 'dari luar angkasa: lintasannya LURUS', '#cfe0ff'], [U_(10).v0, 'kita ikut berputar bersama bumi', C.amber]];
    P.forEach(([tt, s, col], i) => show(ctx, t, tt, () => { rrect(ctx, 1150, 330 + i * 120, 680, 96, 22); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1150, 330 + i * 120, 10, 96, 5); ctx.fillStyle = col; ctx.fill(); text(ctx, s, 1186, 390 + i * 120, fU(30, 700), C.cream); }));
    show(ctx, t, U_(8).v0, () => { text(ctx, 'gaya Coriolis', 1150, 860, fD(80), C.cream); text(ctx, 'Coriolis effect · gaya semu', 1152, 910, fI(36), C.amber); });
    title(ctx, t, 'lempar', 'Melempar bola di atas bumi yang berputar', C.cream);
  });
}

// ---------------------------------------------------------------- aturan: globe with deflected paths
function gPath(lo, la, head, len, k, steps = 40) { const pts = []; let x = lo, y = la, h = head; for (let i = 0; i <= steps; i++) { pts.push([x, y]); h -= k * Math.sin(y * G.D2R) * 0.05; x += Math.cos(h) * len / steps / Math.max(0.3, Math.cos(y * G.D2R)); y += Math.sin(h) * len / steps; } return pts; }
function sAturan(ctx, t) {
  scene(ctx, t, 'aturan', '#0f2233', () => {
    stars(ctx);
    const g = G.globeProj(105 + (t - SC.aturan[0]) * 2, 8, 380, 640, 600);
    G.drawGlobe(ctx, W110, g);
    ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip();
    // equator line
    ctx.strokeStyle = 'rgba(242,177,58,0.8)'; ctx.lineWidth = 3; ctx.beginPath(); let s0 = false; for (let lo = -180; lo <= 180; lo += 3) { const p = g(lo, 0); if (!p) { s0 = false; continue; } s0 ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s0 = true; } ctx.stroke();
    const drawP = (pts, col, prog_) => { const n = Math.floor(pts.length * prog_); if (n < 2) return; ctx.strokeStyle = col; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.beginPath(); let st = false; for (let i = 0; i < n; i++) { const p = g(pts[i][0], pts[i][1]); if (!p) { st = false; continue; } st ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); st = true; } ctx.stroke(); const pe = g(pts[n - 1][0], pts[n - 1][1]), pd = g(pts[n - 2][0], pts[n - 2][1]); if (pe && pd) arrowLine(ctx, pd[0], pd[1], pe[0], pe[1], col, 6, 20); };
    const cyc = (t * 0.35) % 1;
    const pN = ap(t, U_(12).v0, 0.4), pS = ap(t, U_(13).v0, 0.4);
    [[80, 25, 1.2], [110, 40, 0.3], [140, 18, -1.6], [95, 55, 2.4]].forEach(([lo, la, h]) => pN > 0 && drawP(gPath(lo, la, h, 48, 1.6), C.amber, 0.25 + 0.75 * cyc));
    [[80, -25, -1.2], [115, -40, 0.3], [140, -18, 1.6], [95, -55, -2.4]].forEach(([lo, la, h]) => pS > 0 && drawP(gPath(lo, la, h, 48, 1.6), C.clay, 0.25 + 0.75 * cyc));
    // magnitude: deflection bars per latitude
    show(ctx, t, U_(14).v0, () => { [0, 20, 40, 60, 80].forEach((la) => [1, -1].forEach((sg) => { const p = g(g.raw ? 105 + (t - SC.aturan[0]) * 2 : 105, la * sg); if (!p) return; const L = 70 * Math.sin(la * G.D2R); circle(ctx, p[0], p[1], 8 + L * 0.25); ctx.fillStyle = `rgba(255,255,255,${0.25 + 0.6 * Math.sin(la * G.D2R)})`; ctx.fill(); })); });
    ctx.restore();
    const rows = [[U_(12).v0, 'BBU: dibelokkan ke KANAN', C.amber], [U_(13).v0, 'BBS: dibelokkan ke KIRI', C.clay], [U_(14).v0, 'nol di ekuator, maksimum di kutub', '#cfe0ff'], [U_(15).v0, 'makin cepat angin, makin besar belokannya', C.forest3]];
    rows.forEach(([tt, s, col], i) => show(ctx, t, tt, () => { rrect(ctx, 1120, 330 + i * 130, 700, 104, 22); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1120, 330 + i * 130, 10, 104, 5); ctx.fillStyle = col; ctx.fill(); wrap(ctx, s, fU(32, 800), 640).forEach((l, j, a) => text(ctx, l, 1156, 393 + i * 130 + (j - (a.length - 1) / 2) * 38, fU(32, 800), C.cream)); }));
    show(ctx, t, U_(15).v0, () => { [[260, 0.5], [600, 1.0]].forEach(([len, k], j) => { const x0 = 1150, y0 = 900 - j * 0; }); });
    title(ctx, t, 'aturan', 'Aturan gaya Coriolis', C.cream);
  });
}

// ---------------------------------------------------------------- no cyclone at equator: tropical map with tracks
const TRACKS = [[[150, 10], [140, 15], [132, 20], [128, 27], [133, 34]], [[145, 13], [133, 16], [123, 19], [115, 22]], [[90, 12], [87, 16], [88, 20], [91, 22]], [[65, 14], [62, 18], [60, 22]], [[125, -11], [118, -14], [113, -19], [115, -26]], [[95, -11], [85, -15], [72, -19], [62, -24]], [[160, -12], [163, -18], [170, -24]], [[170, 12], [158, 16], [148, 22], [143, 30]], [[132, -10], [128, -15], [125, -20]]];
function sNol(ctx, t) {
  scene(ctx, t, 'nol', C.sand, () => {
    const box = { x: 110, y: 270, w: 1700, h: 640 }; const pr = G.mapProj(box, [50, 185, -38, 38]);
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    G.drawMap(ctx, TROP, pr, { t });
    ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
    const pb = ap(t, U_(16).v0 + 0.5, 0.8);
    const a = pr(50, 5), b = pr(185, -5);
    ctx.fillStyle = `rgba(242,177,58,${0.35 * pb})`; ctx.fillRect(a[0], a[1], b[0] - a[0], b[1] - a[1]);
    ctx.save(); ctx.globalAlpha *= pb; ctx.strokeStyle = 'rgba(152,63,41,0.35)'; ctx.lineWidth = 2; for (let x = a[0] - 200; x < b[0]; x += 26) { ctx.beginPath(); ctx.moveTo(x, b[1]); ctx.lineTo(x + (b[1] - a[1]), a[1]); ctx.stroke(); } ctx.restore();
    const pt = ap(t, U_(17).v0, 3.0, E.linear);
    TRACKS.forEach((tr, i) => { const n = tr.length, f = clamp(pt * 1.6 - i * 0.07) * (n - 1); if (f <= 0) return; ctx.strokeStyle = C.clayD; ctx.lineWidth = 5; ctx.setLineDash([2, 10]); ctx.lineCap = 'round'; ctx.beginPath(); for (let k = 0; k <= Math.floor(f); k++) { const p = pr(tr[k][0], tr[k][1]); k ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } const kk = Math.floor(f), fr = f - kk; let e = tr[kk]; if (kk < n - 1) e = [lerp(tr[kk][0], tr[kk + 1][0], fr), lerp(tr[kk][1], tr[kk + 1][1], fr)]; const pe = pr(e[0], e[1]); ctx.lineTo(pe[0], pe[1]); ctx.stroke(); ctx.setLineDash([]); hurricane(ctx, pe[0], pe[1], 22, t, e[1] > 0 ? 1 : -1); });
    ctx.restore();
    show(ctx, t, U_(16).v0 + 1, () => pill(ctx, 'Coriolis ±0: udara tidak bisa diputar', pr(118, 0)[0], pr(118, 0)[1], fU(28, 800), C.forest, C.cream, 20, 54, 'center'));
    show(ctx, t, U_(17).v0 + 1.5, () => pill(ctx, 'lintasan siklon tropis (ilustrasi)', box.x + box.w - 30, box.y + 40, fU(22, 700), C.clayD, C.cream, 14, 42, 'right'));
    title(ctx, t, 'nol', 'Kenapa siklon jarang lahir di khatulistiwa?');
  });
}

// ---------------------------------------------------------------- force balance simulations (math coords: x right, y up)
function simulate(fric, damp, n = 900, dt = 0.02) { const f = 1.0, g = 1.0; let x = 0, y = 0, vx = 0, vy = 0; const out = []; for (let i = 0; i < n; i++) { const ax = f * vy - fric * vx - damp * (vx + g / f), ay = -g - f * vx - fric * vy - damp * vy; vx += ax * dt; vy += ay * dt; x += vx * dt; y += vy * dt; out.push([x, y, vx, vy]); } return out; }
function forceScene(ctx, t, name, sim, opts) {
  const { t0, len = 7, fric = 0 } = opts;
  const O = { x: opts.ox || 1500, y: 360 }, SX = opts.sx || 55, SY = opts.sy || 200;
  const Y = (k) => 330 + k * 150;
  [0, 1, 2, 3].forEach((k) => { ctx.strokeStyle = 'rgba(29,65,56,0.55)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(110, Y(k)); ctx.lineTo(1810, Y(k)); ctx.stroke(); pill(ctx, `${1012 - k * 4} mb`, 160, Y(k), fU(20, 800), C.cream, C.forest, 10, 36, 'center'); });
  text(ctx, 'TINGGI', 1780, 300, fU(26, 800), C.blue, 'right'); text(ctx, 'RENDAH', 1780, 850, fU(26, 800), C.clay, 'right');
  const p = clamp((t - t0) / len); const idx = Math.min(sim.length - 1, Math.floor(p * (sim.length - 1)));
  const scr = ([x, y]) => [O.x + x * SX, O.y - y * SY];
  ctx.strokeStyle = C.clayD; ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.beginPath(); for (let i = 0; i <= idx; i += 3) { const q = scr(sim[i]); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); } ctx.stroke();
  const [x, y, vx, vy] = sim[idx]; const [px, py] = scr([x, y]);
  // forces
  const F = 70;
  arrowLine(ctx, px, py, px, py + F * 1.3, C.clay, 7, 22);
  const cor = [vy, -vx]; const cm = Math.hypot(...cor) || 1e-6; if (opts.showC) arrowLine(ctx, px, py, px + cor[0] / cm * F * Math.min(1.3, cm), py - cor[1] / cm * F * Math.min(1.3, cm), C.blue, 7, 22);
  if (fric && opts.showF) { const vm = Math.hypot(vx, vy) || 1e-6; arrowLine(ctx, px, py, px - vx / vm * F * 0.8, py + vy / vm * F * 0.8, C.gray, 7, 22); }
  circle(ctx, px, py, 22); ctx.fillStyle = C.amber; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke();
  // legend
  const lg = [['gaya gradien tekanan', C.clay, true], ['gaya Coriolis', C.blue, opts.showC], ['gaya gesekan', C.gray, fric && opts.showF]];
  card(ctx, 140, 690, 500, 200, { r: 22 }); lg.forEach(([s, c, on], i) => { ctx.globalAlpha = on ? 1 : 0.3; rrect(ctx, 175, 722 + i * 54, 40, 14, 7); ctx.fillStyle = c; ctx.fill(); text(ctx, s, 232, 736 + i * 54, fU(26, 700), C.ink); ctx.globalAlpha = 1; });
}
function sSeimbang(ctx, t) {
  scene(ctx, t, 'seimbang', '#eef3f6', () => {
    forceScene(ctx, t, 'seimbang', SIM_G, { t0: U_(19).v0, len: 16, showC: t > U_(20).v0 });
    show(ctx, t, U_(21).v0, () => pill(ctx, 'lapisan atas (di atas ±1 km): tanpa gesekan', 960, 905, fU(26, 800), C.forest, C.cream, 18, 50, 'center'));
    show(ctx, t, U_(23).v0, () => pill(ctx, 'akhirnya SEJAJAR isobar', 900, 270, fU(28, 800), C.clayD, C.cream, 18, 52, 'center'));
    show(ctx, t, U_(24).v0, () => { card(ctx, 700, 690, 620, 150, { r: 24, bg: C.forest }); text(ctx, 'angin geostropik', 740, 755, fU(40, 800), C.amber); text(ctx, 'geostrophic wind', 740, 805, fI(36), C.cream); });
    title(ctx, t, 'seimbang', 'Lapisan atas: gradien tekanan seimbang Coriolis');
  });
}
function sGesekan(ctx, t) {
  scene(ctx, t, 'gesekan', '#eef3f6', () => {
    // paper-cut ground texture strip
    ctx.fillStyle = '#d9e7d0'; ctx.fillRect(0, 940, W, 140);
    forceScene(ctx, t, 'gesekan', SIM_F, { t0: U_(25).v0 + 0.5, len: 10, showC: true, showF: true, fric: 1, ox: 1350, sx: 150, sy: 150 });
    show(ctx, t, U_(26).v0, () => { for (let i = 0; i < 9; i++) { const x = 760 + i * 110, y = 900; ctx.fillStyle = i % 3 === 2 ? '#8a96a3' : '#3f8a52'; if (i % 3 === 2) ctx.fillRect(x - 24, y - 90, 48, 90); else { ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 4, y - 30, 8, 30); circle(ctx, x, y - 48, 26); ctx.fillStyle = '#3f8a52'; ctx.fill(); } } });
    show(ctx, t, tw('sepuluh', U_(27).v0) - 0.3, () => pill(ctx, 'memotong isobar 10°–45° ke tekanan rendah', 900, 270, fU(28, 800), C.clayD, C.cream, 18, 52, 'center'));
    show(ctx, t, U_(28).v0, () => { card(ctx, 700, 690, 620, 150, { r: 24 }); text(ctx, 'laut: gesekan kecil (±10–20°)', 735, 750, fU(28, 700), C.blue); text(ctx, 'darat kasar: gesekan besar (±30–45°)', 735, 800, fU(28, 700), C.clayD); });
    title(ctx, t, 'gesekan', 'Dekat permukaan: gesekan ikut bekerja');
  });
}

// ---------------------------------------------------------------- Buys Ballot: top-down figure
function figure(ctx, x, y, ang, s = 1) { ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s); ctx.fillStyle = C.forest; ctx.beginPath(); ctx.ellipse(0, 0, 46, 24, 0, 0, Math.PI * 2); ctx.fill(); circle(ctx, 0, 0, 20); ctx.fillStyle = '#e6b98f'; ctx.fill(); poly(ctx, [[-8, -20], [8, -20], [0, -38]]); ctx.fillStyle = C.clay; ctx.fill(); ctx.restore(); }
function sBuys(ctx, t) {
  scene(ctx, t, 'buys', C.sand, () => {
    title(ctx, t, 'buys', "Hukum Buys Ballot");
    show(ctx, t, U_(29).v0 + 1.5, () => text(ctx, "Buys Ballot's law", 112, 222, fI(34), C.clayD));
    const panels = [[110, 'BELAHAN BUMI UTARA', 'L', -1, U_(32).v0], [990, 'BELAHAN BUMI SELATAN', 'L', 1, U_(32).v0 + 3]];
    panels.forEach(([x0, lab, , side, tt], i) => {
      const k = ap(t, i === 0 ? U_(30).v0 : tw('kiri', U_(30).v0), 0.6); if (k <= 0) return;
      ctx.save(); ctx.globalAlpha *= k;
      card(ctx, x0, 270, 820, 620, { r: 28, bg: i === 0 ? '#e7f0f6' : '#f6ece4' });
      text(ctx, lab, x0 + 410, 325, fU(28, 800), i === 0 ? C.blue : C.clayD, 'center');
      const cx = x0 + 410, cy = 600;
      for (let j = 0; j < 6; j++) { const ph = (t * 0.8 + j / 6) % 1; const yy = cy + 240 - ph * 200; ctx.strokeStyle = `rgba(43,108,176,${0.8 * Math.sin(ph * Math.PI)})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(cx - 60 + j * 24, yy + 40); ctx.lineTo(cx - 60 + j * 24, yy); ctx.stroke(); }
      figure(ctx, cx, cy, 0, 1.4);
      text(ctx, 'angin dari belakang', cx, cy + 270, fU(22, 700), C.blue, 'center');
      const pl = ap(t, tt, 0.5); if (pl > 0) { const lx = cx + side * 250; circle(ctx, lx, cy - 40, 52 * pl); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, 'L', lx, cy - 22, fU(52 * pl, 800), C.cream, 'center'); circle(ctx, cx - side * 250, cy - 40, 52 * pl); ctx.fillStyle = C.blue; ctx.fill(); text(ctx, 'H', cx - side * 250, cy - 22, fU(52 * pl, 800), C.cream, 'center'); text(ctx, side < 0 ? 'rendah di KIRI' : 'rendah di KANAN', lx, cy + 50, fU(26, 800), C.clayD, 'center'); }
      ctx.restore();
    });
  });
}

// ---------------------------------------------------------------- cyclone / anticyclone 3-D helices
function sSiklon(ctx, t) {
  scene(ctx, t, 'siklon', '#e9eef1', () => {
    title(ctx, t, 'siklon', 'Siklon dan antisiklon');
    const draw = (cx, kind, t0, lab, en, col) => {
      const k = ap(t, t0, 0.6); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k;
      const P = G.iso(cx, 640, 46, 0.3 + 0.1 * Math.sin(t * 0.3), 0.45);
      G.isoBox(ctx, P, -5, -5, -0.4, 10, 10, 0.4, '#cfe0c9', '#a9c39e', '#97b38c');
      // pressure center ring
      ctx.strokeStyle = col; ctx.lineWidth = 4; ctx.beginPath(); for (let i = 0; i <= 60; i++) { const a = i / 60 * Math.PI * 2; const p = P(Math.cos(a) * 4, Math.sin(a) * 4, 0.05); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } ctx.stroke();
      for (let i = 0; i < 70; i++) {
        const ph = (t * 0.12 + hash01(i, kind === 'c' ? 3 : 4)) % 1; const f = kind === 'c' ? ph : 1 - ph;
        const r = kind === 'c' ? lerp(4.6, 0.6, Math.min(1, f * 1.6)) : lerp(0.6, 4.6, Math.min(1, (1 - f) * 1.6));
        const z = kind === 'c' ? Math.max(0, (f - 0.55) * 11) : Math.max(0, (f - 0.45) * -11 + 6);
        const a = hash01(i, 9) * 6.28 + (kind === 'c' ? 1 : -1) * ph * 9;
        const p = P(Math.cos(a) * r, Math.sin(a) * r, z); circle(ctx, p[0], p[1], 5); ctx.fillStyle = kind === 'c' ? 'rgba(224,121,79,0.9)' : 'rgba(43,108,176,0.9)'; ctx.fill();
      }
      if (kind === 'c') { const top = P(0, 0, 5.6); cloud(ctx, top[0], top[1] - 20, 2.0, '#ffffff'); for (let j = 0; j < 6; j++) { const ph = (t * 1.5 + j / 6) % 1; ctx.strokeStyle = C.blue; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(top[0] - 50 + j * 20, top[1] + 20 + ph * 50); ctx.lineTo(top[0] - 54 + j * 20, top[1] + 34 + ph * 50); ctx.stroke(); } }
      else { const top = P(0, 0, 5.6); for (let j = 0; j < 3; j++) arrowLine(ctx, top[0] - 40 + j * 40, top[1] - 30, top[0] - 40 + j * 40, top[1] + 30, C.blue, 5, 16); }
      const c = P(0, 0, 0); circle(ctx, c[0], c[1], 32); ctx.fillStyle = col; ctx.fill(); text(ctx, kind === 'c' ? 'L' : 'H', c[0], c[1] + 13, fU(36, 800), C.cream, 'center');
      text(ctx, lab, cx, 905, fU(36, 800), col, 'center');
      ctx.restore();
    };
    draw(500, 'c', U_(34).v0, 'SIKLON · tekanan rendah', 'cyclone · konvergen, naik, hujan', C.clay);
    draw(1420, 'a', U_(37).v0, 'ANTISIKLON · tekanan tinggi', 'anticyclone · divergen, turun, cerah', C.blue);
    show(ctx, t, U_(36).v0, () => { if (t < U_(39).v0) pill(ctx, 'siklon · BBU: berlawanan jarum jam · BBS: searah', 110, 245, fU(26, 800), C.clay, C.cream, 18, 50); });
    show(ctx, t, U_(39).v0, () => pill(ctx, 'antisiklon: arah putaran berkebalikan dengan siklon', 110, 245, fU(26, 800), C.blue, C.cream, 18, 50));
  });
}

run({
  DUR, no: 7, code: 'B01-07', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Gaya Coriolis', sub: 'dan gesekan · angin geostropik · Buys Ballot · siklon',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-08 · Angin Lokal',
  SCN: [['hook', 0], ['lempar', 5], ['aturan', 11], ['nol', 16], ['seimbang', 18], ['gesekan', 25], ['buys', 29], ['siklon', 33], ['soal', 40], ['jebakan', 44], ['ringkas', 47], ['outro', 50]],
  TERMS: [
    ['Gaya Coriolis', 'Coriolis effect', 'Pembelokan semu akibat rotasi bumi', 8],
    ['Angin geostropik', 'geostrophic wind', 'Lapisan atas: sejajar isobar (gradien = Coriolis)', 24],
    ['Gaya gesekan', 'friction', 'Memperlambat angin dekat permukaan (hingga ±1 km)', 25],
    ['Hukum Buys Ballot', "Buys Ballot's law", 'BBU: membelakangi angin, tekanan rendah di kiri', 29],
    ['Siklon', 'cyclone', 'Tekanan rendah: konvergen, naik, berawan dan hujan', 34],
    ['Konvergen', 'convergence', 'Udara mengalir menuju pusat', 35],
    ['Antisiklon', 'anticyclone', 'Tekanan tinggi: turun, divergen, cerah dan kering', 37],
    ['Divergen', 'divergence', 'Udara menyebar keluar dari pusat', 38],
  ],
  hook: { cards: [], punch: [0, ''] },
  soal: {
    q: 'Seorang pengamat cuaca di Darwin, Australia, berdiri membelakangi arah datangnya angin. Menurut hukum Buys Ballot, pusat tekanan rendah berada di sebelah …',
    opts: ['kiri, karena dibelokkan ke kanan', 'kiri, karena gaya gesekan', 'depan, menuju tekanan rendah', 'kanan, karena dibelokkan ke kiri', 'belakang, Coriolis nol'], ans: 3, optFs: 26,
    ansT: () => tw('jawabannya', U_(43).v0 - 0.3),
    steps: () => [[U_(41).v0, '1) Darwin di belahan bumi selatan', C.forest3, 28], [tw('kiri', U_(41).v0), 'angin dibelokkan ke KIRI', C.cream, 40], [U_(42).v0, '2) Membelakangi angin di BBS', C.forest3, 28], [tw('kanan', U_(42).v0), 'tekanan rendah di KANAN', C.amber, 50]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(45).v0, 'Putaran air di wastafel ditentukan Coriolis', 'Skala terlalu kecil: Coriolis tidak berpengaruh', tw('skalanya', U_(45).v0)],
      [U_(46).v0, 'Gaya Coriolis yang membuat angin', 'Coriolis hanya MEMBELOKKAN arah angin', tw('hanya', U_(46).v0)]],
  },
  ringkas: {
    items: () => [[tw('Coriolis', U_(48).v0), 'Coriolis: kanan di BBU, kiri di BBS, nol di ekuator'], [tw('geostropik', U_(48).v0), 'Angin geostropik sejajar isobar (lapisan atas)'], [tw('gesekan', U_(48).v0), 'Gesekan: angin permukaan memotong isobar']],
  },
  scenes: { hook: sHook, lempar: sLempar, aturan: sAturan, nol: sNol, seimbang: sSeimbang, gesekan: sGesekan, buys: sBuys, siklon: sSiklon },
  async init() {
    W110 = await fetch('assets/world110.json').then((r) => r.json());
    W50 = await fetch('assets/world50.json').then((r) => r.json());
    TROP = G.subset(W50, [50, 185, -40, 40]);
    SIM_G = simulate(0, 0.45); SIM_F = simulate(0.9, 0.0, 260);
  },
});
