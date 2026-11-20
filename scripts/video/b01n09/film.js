// B01-09 · Sirkulasi Tiga Sel dan Angin Pasat · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 242.8;
let W110 = null, ATL = null;
const D2R = Math.PI / 180;

function ship(ctx, x, y, s, dir, sail = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  ctx.fillStyle = '#7b3d22'; poly(ctx, [[-44, 0], [44, 0], [30, 16], [-30, 16]]); ctx.fill();
  ctx.strokeStyle = '#4a2a18'; ctx.lineWidth = 3; [-14, 14].forEach((m) => { ctx.beginPath(); ctx.moveTo(m, 0); ctx.lineTo(m, -64); ctx.stroke(); });
  ctx.fillStyle = '#fffefa'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2;
  [-14, 14].forEach((m) => { ctx.beginPath(); ctx.moveTo(m - 16, -60); ctx.quadraticCurveTo(m + 22 * sail, -36, m - 16, -10); ctx.lineTo(m + 16, -10); ctx.quadraticCurveTo(m + 16 + 18 * sail, -36, m + 16, -60); ctx.closePath(); ctx.fill(); ctx.stroke(); });
  ctx.restore();
}
function stars(ctx, n = 90) { for (let i = 0; i < n; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * H, 1 + hash01(i, 3) * 1.6); ctx.fillStyle = `rgba(255,255,255,${0.25 + 0.5 * hash01(i, 4)})`; ctx.fill(); } }
const pathAt = (pts, f) => { const n = pts.length - 1, x = clamp(f) * n, i = Math.min(n - 1, Math.floor(x)), k = x - i; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; };

// ---------------------------------------------------------------- hook: Atlantic sailing route, desert belt, doldrums
const OUT = [[-9, 38.5], [-16, 28], [-28, 20], [-45, 16], [-62, 16]], BACK = [[-70, 26], [-60, 36], [-40, 42], [-22, 45], [-9, 43]];
function sHook(ctx, t) {
  scene(ctx, t, 'hook', C.sand, () => {
    const box = { x: 0, y: 0, w: W, h: H }; const z = ap(t, 3, 20, E.inOutCubic) * 0.06;
    const ext = [-105 + z * 100, 75 - z * 100, -50 + z * 60, 66 - z * 60]; const pr = G.mapProj(box, ext);
    G.drawMap(ctx, ATL, pr, { t, depth: 10 });
    G.graticule(ctx, pr, ext, 30, 'rgba(29,65,56,0.15)');
    // trade and westerly arrows
    const wa = ap(t, 3.5, 1);
    for (let i = 0; i < 6; i++) { const ph = (t * 0.25 + i / 6) % 1; const a = pr(-20 - ph * 40, 24 - ph * 8), b = pr(-26 - ph * 40, 21 - ph * 8); ctx.globalAlpha = wa * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], C.blue, 6, 18); const c = pr(-65 + ph * 45, 38 + ph * 5), d = pr(-59 + ph * 45, 39 + ph * 5); arrowLine(ctx, c[0], c[1], d[0], d[1], C.clay, 6, 18); ctx.globalAlpha = 1; }
    // route
    const p1 = ap(t, 3.2, 3.6, E.inOutCubic), p2 = ap(t, 7.3, 3.0, E.inOutCubic);
    const drawRoute = (pts, p, col) => { ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.setLineDash([12, 10]); ctx.beginPath(); for (let i = 0; i <= 40 * p; i++) { const q = pr(...pathAt(pts, i / 40)); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); } ctx.stroke(); ctx.setLineDash([]); };
    drawRoute(OUT, p1, C.blue); if (p2 > 0) drawRoute(BACK, p2, C.clay);
    const sp_ = p2 > 0 ? pr(...pathAt(BACK, p2)) : pr(...pathAt(OUT, p1)); if (t < U_(1).v0 + 0.5) ship(ctx, sp_[0], sp_[1] - 10, 0.9, p2 > 0 ? 1 : -1);
    show(ctx, t, 4, () => { const q = pr(-38, 12); pill(ctx, 'berangkat: rute selatan', q[0], q[1] + 30, fU(26, 800), C.blue, C.cream, 16, 48, 'center'); });
    show(ctx, t, 7.8, () => { const q = pr(-42, 50); pill(ctx, 'pulang: rute utara', q[0], q[1] - 20, fU(26, 800), C.clay, C.cream, 16, 48, 'center'); });
    // desert belt
    const pd = ap(t, U_(1).v0, 1.0);
    if (pd > 0) { ctx.save(); ctx.globalAlpha *= pd; [[-15, 35, 12, 32], [35, 60, 15, 30], [12, 28, -30, -18], [114, 140, -32, -20], [-118, -105, 26, 36]].forEach(([a, b, c, d]) => { const p = pr(a, d), q = pr(b, c); ctx.fillStyle = 'rgba(224,160,79,0.55)'; rrect(ctx, p[0], p[1], q[0] - p[0], q[1] - p[1], 18); ctx.fill(); }); [30, -30].forEach((la) => { const a = pr(ext[0], la), b = pr(ext[1], la); ctx.setLineDash([16, 10]); ctx.strokeStyle = C.clayD; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); ctx.stroke(); ctx.setLineDash([]); pill(ctx, `${la > 0 ? '30° LU' : '30° LS'}: sabuk gurun`, a[0] + 140, a[1], fU(24, 800), C.clayD, C.cream, 14, 44, 'center'); }); ctx.restore(); }
    // doldrums ship
    show(ctx, t, U_(2).v0, () => { const q = pr(-25, 2); ship(ctx, q[0], q[1], 1.2, 1, 0.1 + 0.05 * Math.sin(t * 2)); pill(ctx, 'tanpa angin di khatulistiwa', q[0], q[1] + 50, fU(26, 800), C.forest, C.cream, 16, 48, 'center'); });
    show(ctx, t, U_(4).v0, () => { card(ctx, W / 2 - 520, 420, 1040, 170, { r: 40, bg: C.forest }); text(ctx, 'sirkulasi atmosfer global', W / 2, 535, fD(86), C.cream, 'center'); });
  });
}

// ---------------------------------------------------------------- mesin panas: globe with surplus / deficit
function sMesin(ctx, t) {
  scene(ctx, t, 'mesin', '#0f2233', () => {
    stars(ctx);
    const g = G.globeProj(20 + (t - SC.mesin[0]) * 3, 12, 380, 700, 600);
    G.drawGlobe(ctx, W110, g);
    ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip();
    const pk = ap(t, U_(5).v0, 1.0);
    const band = (la0, la1, col) => { ctx.fillStyle = col; ctx.beginPath(); const L0 = 20 + (t - SC.mesin[0]) * 3; for (let lo = L0 - 89; lo <= L0 + 89; lo += 2) { const p = g.raw(lo, la1); if (p[2] >= 0) ctx.lineTo(p[0], p[1]); } for (let lo = L0 + 89; lo >= L0 - 89; lo -= 2) { const p = g.raw(lo, la0); if (p[2] >= 0) ctx.lineTo(p[0], p[1]); } ctx.closePath(); ctx.fill(); };
    ctx.globalAlpha = pk; band(-30, 30, 'rgba(224,121,79,0.35)'); band(60, 90, 'rgba(120,170,230,0.45)'); band(-90, -60, 'rgba(120,170,230,0.45)'); ctx.globalAlpha = 1;
    const pf = ap(t, U_(6).v0, 0.8);
    if (pf > 0) for (let i = 0; i < 70; i++) { const lo = (i * 37) % 360 - 180, sg = i % 2 ? 1 : -1, ph = (t * 0.25 + hash01(i, 3)) % 1; const la = sg * ph * 85; const p = g(lo, la); if (!p) continue; circle(ctx, p[0], p[1], 5); ctx.fillStyle = `rgba(255,${200 - 140 * (1 - ph)},120,${pf * (1 - ph)})`; ctx.fill(); }
    const p7 = ap(t, U_(7).v0 + 0.5, 1.2);
    if (p7 > 0) { [30, 60, -30, -60].forEach((la) => { ctx.strokeStyle = `rgba(255,255,255,${0.9 * p7})`; ctx.lineWidth = 4; ctx.setLineDash([14, 10]); ctx.beginPath(); let s0 = false; for (let lo = -180; lo <= 180; lo += 3) { const p = g(lo, la); if (!p) { s0 = false; continue; } s0 ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s0 = true; } ctx.stroke(); ctx.setLineDash([]); }); }
    ctx.restore();
    show(ctx, t, U_(5).v0 + 1, () => { pill(ctx, 'tropis: SURPLUS energi', 1230, 360, fU(30, 800), C.clay, C.cream, 20, 56); pill(ctx, 'kutub: DEFISIT energi', 1230, 450, fU(30, 800), C.blue, C.cream, 20, 56); });
    show(ctx, t, U_(6).v0 + 0.5, () => pill(ctx, 'panas dipindahkan ke arah kutub', 1230, 560, fU(30, 800), C.amber, C.ink, 20, 56));
    show(ctx, t, U_(7).v0 + 0.5, () => { text(ctx, '3 sel', 1230, 720, fD(110), C.cream); text(ctx, 'di setiap belahan bumi', 1235, 775, fU(30, 700), C.forest3); });
    show(ctx, t, U_(8).v0, () => text(ctx, 'three cell model', 1235, 830, fI(40), C.amber));
    title(ctx, t, 'mesin', 'Atmosfer: mesin pemindah panas', C.cream);
  });
}

// ---------------------------------------------------------------- the three-cell globe (shared by several scenes)
const CELLS = [ // [lat0, lat1, dir(+1: surface equatorward), name, color]
  [0, 30, 1, 'Hadley', '#e0794f'], [30, 60, -1, 'Ferrel', '#2b6cb0'], [60, 90, 1, 'Polar', '#7fb3d5']];
function cellLoop(ctx, cx, cy, R, la0, la1, dir, hemi, col, t, a, thick = 75) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a;
  const r0 = R + 14, r1 = R + thick; const ang = (la) => hemi * la * D2R;
  const P_ = (la, r) => [cx + r * Math.cos(ang(la)), cy - r * Math.sin(ang(la))];
  // loop path param s in [0,4): surface la1->la0 (if dir>0), rise at la0, aloft la0->la1, sink at la1
  const A = dir > 0 ? la1 : la0, B = dir > 0 ? la0 : la1;
  const pt = (s) => { const si = Math.floor(s) % 4, f = s - Math.floor(s); if (si === 0) return P_(lerp(A, B, f), r0); if (si === 1) return P_(B, lerp(r0, r1, f)); if (si === 2) return P_(lerp(B, A, f), r1); return P_(A, lerp(r1, r0, f)); };
  ctx.strokeStyle = col; ctx.lineWidth = 4; ctx.setLineDash([8, 8]); ctx.beginPath(); for (let i = 0; i <= 120; i++) { const q = pt(i / 30); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); } ctx.stroke(); ctx.setLineDash([]);
  for (let i = 0; i < 26; i++) { const s = ((t * 0.18 + i / 26) % 1) * 4; const q = pt(s); circle(ctx, q[0], q[1], 8); ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 2; ctx.stroke(); }
  const q1 = pt(2.6), q0 = pt(2.4); arrowLine(ctx, q0[0], q0[1], q1[0], q1[1], col, 6, 22);
  const qs1 = pt(0.6), qs0 = pt(0.4); arrowLine(ctx, qs0[0], qs0[1], qs1[0], qs1[1], col, 6, 22);
  ctx.restore();
}
function surfaceWinds(ctx, g, t, la, vec, col, a, n = 6) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a;
  for (let i = 0; i < n; i++) { const lo0 = g.lon0 - 70 + i * 28; const ph = (t * 0.35 + i * 0.17) % 1; const L = 14; const s = [lo0 + vec[0] * L * ph, la + vec[1] * L * ph], e = [s[0] + vec[0] * 9, s[1] + vec[1] * 9]; const p = g(...s), q = g(...e); if (!p || !q) continue; ctx.globalAlpha = a * Math.sin(ph * Math.PI); arrowLine(ctx, p[0], p[1], q[0], q[1], col, 6, 18); }
  ctx.restore();
}
function cellGlobe(ctx, t, st) {
  // st: { hadley, ferrel, polar, itcz, anti, sink, desert, trades, wester, easter, front, belts }
  stars(ctx, 60);
  const lon0 = 18 + 4 * Math.sin(t * 0.08); const cx = 600, cy = 630, R = 255;
  const g = G.globeProj(lon0, 0, R, cx, cy); g.lon0 = lon0;
  G.drawGlobe(ctx, W110, g);
  ctx.save(); circle(ctx, cx, cy, R); ctx.clip();
  // latitude guides
  [30, 60, -30, -60].forEach((la) => { ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 2; ctx.beginPath(); let s0 = false; for (let lo = lon0 - 89; lo <= lon0 + 89; lo += 3) { const p = g(lo, la); if (!p) continue; s0 ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s0 = true; } ctx.stroke(); });
  if (st.desert > 0) { ctx.save(); ctx.globalAlpha *= st.desert; [[12, 24, 14], [45, 23, 9], [22, -23, 7]].forEach(([lo, la, r]) => { const p = g(lo, la); if (!p) return; ctx.fillStyle = 'rgba(224,160,79,0.75)'; ctx.beginPath(); ctx.ellipse(p[0], p[1], r * 4.5, r * 2.2, 0, 0, Math.PI * 2); ctx.fill(); }); ctx.restore(); }
  if (st.itcz > 0) { for (let lo = lon0 - 80; lo <= lon0 + 80; lo += 14) { const p = g(lo + 3 * Math.sin(lo + t), 2 * Math.sin(lo * 0.3)); if (p) cloud(ctx, p[0], p[1], 0.55 * st.itcz * (0.8 + 0.3 * Math.cos(lo * D2R)), '#ffffff'); } }
  surfaceWinds(ctx, g, t, 15, [-1, -0.55], C.amber, st.trades); surfaceWinds(ctx, g, t, -15, [-1, 0.55], C.amber, st.trades);
  surfaceWinds(ctx, g, t, 45, [1, 0.35], C.clay, st.wester); surfaceWinds(ctx, g, t, -45, [1, -0.35], C.clay, st.wester);
  surfaceWinds(ctx, g, t, 72, [-1, -0.3], '#cfe0ff', st.easter, 4); surfaceWinds(ctx, g, t, -72, [-1, 0.3], '#cfe0ff', st.easter, 4);
  ctx.restore();
  // cells on the right limb (both hemispheres) and mirrored on the left limb
  const A = [st.hadley, st.ferrel, st.polar];
  CELLS.forEach(([a, b, d, n, col], i) => { [1, -1].forEach((h) => cellLoop(ctx, cx, cy, R, a, b, d, h, col, t, A[i])); });
  CELLS.forEach(([a, b, d, n, col], i) => { if (A[i] <= 0) return; const ang = (a + b) / 2 * D2R; ctx.save(); ctx.globalAlpha *= A[i]; pill(ctx, `Sel ${n === 'Polar' ? 'kutub' : n}`, cx + R + 100, cy - (R + 40) * Math.sin(ang), fU(24, 800), col, C.cream, 14, 44); ctx.restore(); });
  // belts H/L at limb
  if (st.belts > 0) { [[0, 'L'], [30, 'H'], [60, 'L'], [90, 'H'], [-30, 'H'], [-60, 'L'], [-90, 'H']].forEach(([la, k], i) => { const ang = la * D2R; const x = cx - (R + 40) * Math.cos(ang), y = cy - (R + 40) * Math.sin(ang); const s = st.belts * clamp(1 - i * 0.05); circle(ctx, x, y, 26 * s); ctx.fillStyle = k === 'H' ? C.blue : C.clay; ctx.fill(); text(ctx, k, x, y + 10 * s, fU(28 * s, 800), C.cream, 'center'); }); }
  return g;
}
function infoRows(ctx, t, rows) {
  rows.forEach(([tt, a, en, col], i) => show(ctx, t, tt, () => { const y = 300 + i * 112; rrect(ctx, 1150, y, 680, 96, 22); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1150, y, 10, 96, 5); ctx.fillStyle = col; ctx.fill(); text(ctx, a, 1186, y + 44, fU(30, 800), C.cream); if (en) text(ctx, en, 1186, y + 80, fI(28), mix(col, '#ffffff', 0.35)); }));
}
function sHadley(ctx, t) {
  scene(ctx, t, 'hadley', '#0f2233', () => {
    cellGlobe(ctx, t, { hadley: ap(t, U_(9).v0, 0.8), itcz: ap(t, U_(10).v0, 1.0), desert: ap(t, U_(15).v0, 0.8), trades: ap(t, U_(17).v0, 0.8) });
    infoRows(ctx, t, [[U_(9).v0, 'Sel Hadley · 0°–30°', 'Hadley cell', C.clay], [U_(11).v0, 'ITCZ: naik, rendah, hujan', 'Intertropical Convergence Zone · doldrums', '#ffffff'], [U_(13).v0, 'atas: angin antipasat', 'antitrade winds', '#cfe0ff'], [U_(14).v0, '30°: tekanan tinggi subtropis', 'subtropical high · horse latitudes', C.blue], [U_(15).v0, 'udara turun kering: gurun', 'Sahara · Arab · Kalahari · Australia', C.amber], [U_(19).v0, 'pasat timur laut · pasat tenggara', 'trade winds', C.amber]]);
    title(ctx, t, 'hadley', 'Sel Hadley dan angin pasat', C.cream);
  });
}
function sFerrel(ctx, t) {
  scene(ctx, t, 'ferrel', '#0f2233', () => {
    cellGlobe(ctx, t, { hadley: 0.5, ferrel: ap(t, U_(22).v0, 0.8), trades: 0.5, wester: ap(t, U_(23).v0, 0.8) });
    infoRows(ctx, t, [[U_(22).v0, 'Sel Ferrel · 30°–60°', 'Ferrel cell', C.blue], [U_(23).v0, 'angin baratan', 'westerlies', C.clay], [U_(24).v0, 'diputar dua sel di sampingnya', 'seperti roda gigi', C.forest3]]);
    show(ctx, t, U_(24).v0 + 0.5, () => { const gear = (x, y, r, a, col) => { ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.fillStyle = col; ctx.beginPath(); for (let i = 0; i < 24; i++) { const ang = i / 24 * Math.PI * 2; const rr = i % 2 ? r : r * 1.2; ctx.lineTo(Math.cos(ang) * rr, Math.sin(ang) * rr); } ctx.closePath(); ctx.fill(); circle(ctx, 0, 0, r * 0.35); ctx.fillStyle = '#0f2233'; ctx.fill(); ctx.restore(); }; gear(1320, 760, 60, t * 1.2, C.clay); gear(1460, 760, 60, -t * 1.2 + 0.13, C.blue); gear(1600, 760, 60, t * 1.2, '#7fb3d5'); text(ctx, 'Hadley', 1320, 860, fU(22, 800), C.cream, 'center'); text(ctx, 'Ferrel', 1460, 860, fU(22, 800), C.cream, 'center'); text(ctx, 'kutub', 1600, 860, fU(22, 800), C.cream, 'center'); });
    title(ctx, t, 'ferrel', 'Sel Ferrel dan angin baratan', C.cream);
  });
}
function sKutub(ctx, t) {
  scene(ctx, t, 'kutub', '#0f2233', () => {
    const g = cellGlobe(ctx, t, { hadley: 0.5, ferrel: 0.5, polar: ap(t, U_(25).v0, 0.8), trades: 0.5, wester: 0.6, easter: ap(t, U_(26).v0 + 2, 0.8) });
    show(ctx, t, U_(27).v0, () => { ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip(); ctx.strokeStyle = C.clayD; ctx.lineWidth = 6; [60, -60].forEach((la) => { ctx.beginPath(); let s0 = false; for (let lo = g.lon0 - 89; lo <= g.lon0 + 89; lo += 2) { const p = g(lo, la + 2 * Math.sin(lo * 0.2 + t)); if (!p) continue; s0 ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s0 = true; } ctx.stroke(); }); ctx.restore(); });
    infoRows(ctx, t, [[U_(25).v0, 'Sel kutub · 60°–90°', 'polar cell', '#7fb3d5'], [U_(26).v0, 'kutub: tekanan tinggi', 'polar high', C.blue], [U_(26).v0 + 2, 'angin timuran kutub', 'polar easterlies', '#cfe0ff'], [U_(28).v0, '60°: front kutub, siklon lintang tengah', 'polar front', C.clay]]);
    title(ctx, t, 'kutub', 'Sel kutub dan front kutub', C.cream);
  });
}
function sSabuk(ctx, t) {
  scene(ctx, t, 'sabuk', '#0f2233', () => {
    cellGlobe(ctx, t, { hadley: 1, ferrel: 1, polar: 1, trades: 1, wester: 1, easter: 1, itcz: 0.8, belts: ap(t, U_(29).v0 + 0.5, 0.8) });
    const rows = [['90°', 'TINGGI', C.blue], ['60°', 'RENDAH', C.clay], ['30°', 'TINGGI', C.blue], ['0°', 'RENDAH', C.clay]];
    rows.forEach(([la, k, col], i) => show(ctx, t, tw(i === 3 ? 'rendah' : i === 2 ? 'tinggi' : i === 1 ? 'rendah' : 'tinggi', U_(30).v0, i === 3 ? 0 : i === 2 ? 0 : i === 1 ? 1 : 1) - 0.1, () => { const y = 330 + (3 - i) * 0; const yy = 300 + i * 140; rrect(ctx, 1200, yy, 600, 110, 24); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); text(ctx, la, 1250, yy + 70, fU(40, 800), C.cream); pill(ctx, k, 1600, yy + 55, fU(32, 800), col, C.cream, 22, 58, 'center'); }));
    title(ctx, t, 'sabuk', 'Sabuk tekanan bergantian', C.cream);
  });
}

run({
  DUR, no: 9, code: 'B01-09', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Sirkulasi Tiga Sel', sub: 'Hadley, Ferrel, kutub · angin pasat · ITCZ',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-10 · ITCZ dan Monsun',
  SCN: [['hook', 0], ['mesin', 5], ['hadley', 9], ['ferrel', 22], ['kutub', 25], ['sabuk', 29], ['soal', 31], ['jebakan', 35], ['ringkas', 38], ['outro', 42]],
  TERMS: [
    ['Model tiga sel', 'three cell model', 'Tiga sel sirkulasi di setiap belahan bumi', 8],
    ['Sel Hadley', 'Hadley cell', '0°–30°: naik di ekuator, turun di 30°', 9],
    ['ITCZ', 'Intertropical Convergence Zone', 'Sabuk tekanan rendah ekuator; pelaut: doldrums', 11],
    ['Angin antipasat', 'antitrade winds', 'Aliran atas sel Hadley ke arah kutub', 13],
    ['Tekanan tinggi subtropis', 'subtropical high', '±30°: udara turun, kering; horse latitudes', 14],
    ['Angin pasat', 'trade winds', 'BBU dari timur laut, BBS dari tenggara', 21],
    ['Sel Ferrel', 'Ferrel cell', '30°–60°: diputar dua sel di sampingnya', 22],
    ['Angin baratan', 'westerlies', 'Angin permukaan lintang tengah', 23],
    ['Sel kutub', 'polar cell', '60°–90°: udara dingin turun di kutub', 25],
    ['Angin timuran kutub', 'polar easterlies', 'Dari kutub menuju lintang 60°', () => tw('timuran', U_(26).v0)],
    ['Front kutub', 'polar front', 'Pertemuan udara kutub dan baratan di ±60°', 28],
  ],
  hook: { cards: [], punch: [4, ''] },
  soal: {
    q: 'Sebelum ada kapal uap, pedagang Eropa yang berlayar ke Karibia memanfaatkan angin … dan kembali ke Eropa memanfaatkan angin …',
    opts: ['pasat timur laut; baratan', 'pasat tenggara; baratan', 'baratan; pasat timur laut', 'timuran kutub; pasat timur laut', 'pasat timur laut; timuran kutub'], ans: 0, optFs: 28,
    ansT: () => tw('jawabannya', U_(34).v0 - 0.3),
    steps: () => [[U_(32).v0, '1) Berangkat ke barat, 5°–30° LU', C.forest3, 28], [tw('pasat', U_(32).v0), 'pasat timur laut', C.cream, 42], [U_(33).v0, '2) Pulang ke timur, 30°–60° LU', C.forest3, 28], [tw('baratan', U_(33).v0), 'angin baratan', C.amber, 50]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(36).v0, 'Pasat tenggara dipakai di Atlantik utara', 'Pasat tenggara hanya di belahan bumi SELATAN', tw('selatan', U_(36).v0)],
      [U_(37).v0, 'Sel Ferrel digerakkan pemanasan langsung', 'Sel Ferrel diputar oleh sel Hadley dan sel kutub', U_(37).v0 + 2.5]],
  },
  ringkas: {
    items: () => [[U_(39).v0, 'Tiga sel: Hadley, Ferrel, kutub'], [tw('pasat', U_(40).v0), 'Pasat ke ekuator, baratan di lintang tengah'], [tw('gurun', U_(40).v0), 'Gurun di sabuk tekanan tinggi subtropis']],
  },
  scenes: { hook: sHook, mesin: sMesin, hadley: sHadley, ferrel: sFerrel, kutub: sKutub, sabuk: sSabuk },
  async init() {
    W110 = await fetch('assets/world110.json').then((r) => r.json());
    const W50 = await fetch('assets/world50.json').then((r) => r.json());
    ATL = G.subset(W50, [-115, 80, -55, 70]);
  },
});
