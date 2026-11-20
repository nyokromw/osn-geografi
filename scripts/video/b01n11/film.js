// B01-11 · Sirkulasi Walker · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, rain, fish } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 222.5;
const D2R = Math.PI / 180;
let W110 = null, PAC = null;

const sig = (x) => 1 / (1 + Math.exp(-x));
function sst(lo, la, shift = 0) { const e = lo - shift * 40; return 29.5 - 7.5 * sig((e - 205) / 24) - 3 * Math.exp(-((la / 5) ** 2)) * sig((e - 235) / 15) - 0.12 * Math.abs(la) * 1.2; }
function sstCol(T) { const k = clamp((T - 18) / 12); return k > 0.5 ? mix('#f2b13a', '#c8452c', (k - 0.5) * 2) : mix('#3b7fc4', '#f2b13a', k * 2); }
function drawSST(ctx, pr, ext, shift = 0) {
  const nx = 64, ny = 26, dx = (ext[1] - ext[0]) / nx, dy = (ext[3] - ext[2]) / ny;
  for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) { const lo = ext[0] + (i + 0.5) * dx, la = ext[2] + (j + 0.5) * dy; const a = pr(ext[0] + i * dx, ext[2] + (j + 1) * dy), b = pr(ext[0] + (i + 1) * dx, ext[2] + j * dy); ctx.fillStyle = sstCol(sst(lo, la, shift)); ctx.fillRect(a[0], a[1], b[0] - a[0] + 1, b[1] - a[1] + 1); }
}
function pacMap(ctx, t, box, ext, shift = 0) {
  const pr = G.mapProj(box, ext);
  ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
  drawSST(ctx, pr, ext, shift);
  G.drawMap(ctx, PAC, pr, { t, sea: 'rgba(0,0,0,0)', waves: false, depth: 7 });
  const e1 = pr(ext[0], 0), e2 = pr(ext[1], 0); ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 2; ctx.setLineDash([10, 8]); ctx.beginPath(); ctx.moveTo(e1[0], e1[1]); ctx.lineTo(e2[0], e2[1]); ctx.stroke(); ctx.setLineDash([]);
  ctx.restore();
  return pr;
}
function legend(ctx, x, y) { for (let i = 0; i < 60; i++) { ctx.fillStyle = sstCol(18 + i * 0.2); ctx.fillRect(x + i * 5, y, 5, 18); } text(ctx, '18 °C', x, y + 42, fU(18, 700), C.ink); text(ctx, '30 °C', x + 300, y + 42, fU(18, 700), C.ink, 'right'); text(ctx, 'suhu permukaan laut', x, y - 10, fU(18, 700), C.ink); }

// ---------------------------------------------------------------- hook: Pacific SST
function sHook(ctx, t) {
  scene(ctx, t, 'hook', C.sand, () => {
    const box = { x: 0, y: 0, w: W, h: H }; const z = ap(t, 3, 16, E.inOutCubic) * 0.05;
    const ext = [95 + z * 60, 292 - z * 60, -42 + z * 20, 34 - z * 20];
    const pr = pacMap(ctx, t, box, ext);
    show(ctx, t, U_(0).v0 + 0.5, () => { const p = pr(125, -2); pill(ctx, 'Indonesia–Papua: ±29–30 °C', p[0], p[1] - 160, fU(30, 800), C.clayD, C.cream, 20, 56, 'center'); });
    show(ctx, t, U_(1).v0 + 0.5, () => { const p = pr(278, -12); pill(ctx, 'lepas pantai Peru: dingin, kering', p[0] - 120, p[1] + 140, fU(30, 800), C.blue, C.cream, 20, 56, 'center'); });
    show(ctx, t, U_(2).v0 + 1, () => { const a = pr(130, 4), b = pr(270, 4); ctx.strokeStyle = C.cream; ctx.lineWidth = 6; ctx.setLineDash([16, 12]); ctx.lineDashOffset = -t * 40; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo((a[0] + b[0]) / 2, a[1] - 260, b[0], b[1]); ctx.stroke(); ctx.setLineDash([]); pill(ctx, 'satu sirkulasi raksasa di sepanjang ekuator', (a[0] + b[0]) / 2, a[1] - 160, fU(30, 800), C.forest, C.cream, 20, 56, 'center'); });
    legend(ctx, 120, 960);
  });
}

// ---------------------------------------------------------------- meridional vs zonal on globe
function sArah(ctx, t) {
  scene(ctx, t, 'arah', '#0f2233', () => {
    for (let i = 0; i < 80; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * H, 1 + hash01(i, 3) * 1.4); ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.fill(); }
    const lon0 = 160 + 8 * Math.sin((t - SC.arah[0]) * 0.12), g = G.globeProj(lon0, 12, 380, 640, 600); G.drawGlobe(ctx, W110, g);
    ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip();
    const pm = ap(t, U_(4).v0, 0.8) * (1 - 0.65 * ap(t, U_(6).v0, 0.6));
    if (pm > 0) for (let k = 0; k < 5; k++) { const lo = lon0 - 50 + k * 25; for (let j = 0; j < 3; j++) { const ph = (t * 0.35 + j / 3 + k * 0.1) % 1, la = lerp(-55, 55, ph); const a = g(lo, la), b = g(lo, la + 7); if (a && b) { ctx.globalAlpha = pm * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], C.amber, 7, 20); } } }
    ctx.globalAlpha = 1;
    const pz = ap(t, U_(6).v0, 0.8);
    if (pz > 0) for (let k = 0; k < 3; k++) { const la = [-2, 2, 6][k]; for (let j = 0; j < 5; j++) { const ph = (t * 0.25 + j / 5) % 1, lo = lon0 - 85 + ph * 170; const a = g(lo, la), b = g(lo + 9, la); if (a && b) { ctx.globalAlpha = pz * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], C.clay, 8, 24); } } }
    ctx.globalAlpha = 1; ctx.restore();
    const rows = [[U_(3).v0, 'Hadley, Ferrel, kutub', '', '#cfe0ff'], [U_(5).v0, 'MERIDIONAL: utara–selatan', 'meridional circulation', C.amber], [U_(7).v0, 'ZONAL: barat–timur', 'zonal circulation', C.clay], [U_(8).v0, 'contoh: sirkulasi Walker', 'Walker circulation · ekuator Pasifik', '#9fe0b0']];
    rows.forEach(([tt, a, en, col], i) => show(ctx, t, tt, () => { const y = 330 + i * 140; rrect(ctx, 1150, y, 680, 116, 22); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1150, y, 10, 116, 5); ctx.fillStyle = col; ctx.fill(); text(ctx, a, 1186, y + 52, fU(32, 800), C.cream); if (en) text(ctx, en, 1186, y + 92, fI(30), mix(col, '#ffffff', 0.35)); }));
    title(ctx, t, 'arah', 'Meridional dan zonal', C.cream);
  });
}

// ---------------------------------------------------------------- 3-D Pacific slab (ocean + atmosphere)
function slab(ctx, t, o) {
  const az = -0.32 + 0.1 * Math.sin(t * 0.12);
  const P0 = G.iso(660, 650, 60, az, 0.42), P = (x, y, z) => P0(x - 6, y - 1.5, z);
  const sh = o.shift || 0; // + = El Nino-like (warm pool east), - = La Nina-like
  const hS = (x) => 0.18 * (1 - x / 12) * (1 - sh * 0.8); // sea surface tilt
  const dT = (x) => -lerp(2.0, 0.35, clamp(x / 12 - sh * 0.25)) ; // thermocline depth (negative z)
  const D = -2.6;
  // front cross-section (y = 3)
  const N = 40;
  const face = (fn, col) => { ctx.fillStyle = col; ctx.beginPath(); for (let i = 0; i <= N; i++) { const x = 12 * i / N; const p = P(x, 3, fn(x)); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } for (let i = N; i >= 0; i--) { const x = 12 * i / N; const p = P(x, 3, D); ctx.lineTo(p[0], p[1]); } ctx.closePath(); ctx.fill(); };
  // side (x = 12) face
  ctx.fillStyle = '#1f4f7a'; poly(ctx, [P(12, 0, hS(12)), P(12, 3, hS(12)), P(12, 3, D), P(12, 0, D)]); ctx.fill();
  face(hS, '#2a5f93');
  // warm layer on front face
  ctx.fillStyle = 'rgba(232,120,70,0.9)'; ctx.beginPath(); for (let i = 0; i <= N; i++) { const x = 12 * i / N, p = P(x, 3, hS(x)); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } for (let i = N; i >= 0; i--) { const x = 12 * i / N, p = P(x, 3, dT(x)); ctx.lineTo(p[0], p[1]); } ctx.closePath(); ctx.fill();
  show(ctx, t, o.tTherm || 1e9, () => { ctx.strokeStyle = C.cream; ctx.lineWidth = 3; ctx.setLineDash([10, 8]); ctx.beginPath(); for (let i = 0; i <= N; i++) { const x = 12 * i / N, p = P(x, 3, dT(x)); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); } ctx.stroke(); ctx.setLineDash([]); const p = P(6, 3, dT(6) - 0.25); text(ctx, 'batas air hangat dan dingin', p[0], p[1] + 30, fU(20, 800), C.cream, 'center'); });
  // sea surface (top)
  const M_ = 24; for (let i = 0; i < M_; i++) { const x0 = 12 * i / M_, x1 = 12 * (i + 1) / M_; ctx.fillStyle = sstCol(sst(130 + (x0 + x1) / 2 / 12 * 150, 0, sh)); poly(ctx, [P(x0, 0, hS(x0)), P(x1, 0, hS(x1)), P(x1, 3, hS(x1)), P(x0, 3, hS(x0))]); ctx.fill(); }
  // lands
  G.isoBox(ctx, P, -1.6, -0.2, D, 1.6, 3.4, -D + 0.6, '#7fb07a', '#5e8f5a', '#6c9d67');
  G.isoBox(ctx, P, 12, -0.2, D, 1.4, 3.4, -D + 0.9, '#d9c28f', '#b9a27a', '#c8b083');
  const lI = P(-0.8, 1.5, 0.9), lP = P(12.7, 1.5, 1.2); text(ctx, 'Indonesia', lI[0], lI[1] - 10, fU(26, 800), C.forest, 'center'); text(ctx, 'Peru', lP[0], lP[1] - 10, fU(26, 800), '#7a5a2c', 'center');
  // trade wind arrows over surface
  if (o.trades > 0) for (let j = 0; j < 7; j++) { const ph = (t * 0.3 + j / 7) % 1, x = 11 - ph * 10; const a = P(x, 1.5, hS(x) + 0.35), b = P(x - 1, 1.5, hS(x - 1) + 0.35); ctx.globalAlpha = o.trades * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], '#ffffff', 7, 22); ctx.globalAlpha = 1; }
  // warm water particles drifting west on front face
  if (o.drift > 0) for (let j = 0; j < 40; j++) { const ph = (t * 0.12 + hash01(j, 3)) % 1, x = 11.5 - ph * 11; const z = lerp(hS(x) - 0.08, dT(x) + 0.08, hash01(j, 4)); const p = P(x, 3, z); circle(ctx, p[0], p[1], 4); ctx.fillStyle = `rgba(255,230,190,${o.drift * 0.9})`; ctx.fill(); }
  // upwelling arrows near Peru
  if (o.up > 0) for (let j = 0; j < 4; j++) { const ph = (t * 0.6 + j / 4) % 1; const x = 10.6 + j * 0.3; const a = P(x, 3, D * 0.8 + ph * 1.6), b = P(x, 3, D * 0.8 + ph * 1.6 + 0.5); ctx.globalAlpha = o.up * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], '#bfe3ff', 6, 18); ctx.globalAlpha = 1; }
  if (o.fish > 0) for (let j = 0; j < 5; j++) { const p = P(10.2 + j * 0.3 + 0.2 * Math.sin(t + j), 3, -0.5 - (j % 2) * 0.4); fish(ctx, p[0], p[1], 1.1 * o.fish, '#cfe9ff'); }
  // atmospheric loop (vertical plane y = 1.5)
  const xr = clamp(1.6 + sh * 5, 1.2, 9), xs = clamp(10.4 + sh * 1, 8, 11.5);
  if (o.loop > 0) {
    const pts = [[xr, 0.4], [xr, 3.0], [xs, 3.0], [xs, 0.4]]; const seg = (s) => { const i = Math.floor(s) % 4, f = s - Math.floor(s); const [a, b] = [pts[i], pts[(i + 1) % 4]]; return [lerp(a[0], b[0], f), lerp(a[1], b[1], f)]; };
    const segOn = [o.up1, o.top, o.down, o.ret];
    for (let j = 0; j < 70; j++) { const s = ((t * 0.07 + j / 70) % 1) * 4, si = Math.floor(s); const a = segOn[si] || 0; if (a <= 0) continue; const [x, z] = seg(s); const p = P(x, 1.5, z + 0.2); circle(ctx, p[0], p[1], 6); ctx.fillStyle = si === 0 ? `rgba(224,121,79,${a})` : si === 2 ? `rgba(43,108,176,${a})` : `rgba(255,255,255,${a})`; ctx.fill(); }
    if (o.up1 > 0) { const c = P(xr, 1.5, 3.3); ctx.save(); ctx.globalAlpha *= o.up1; cloud(ctx, c[0], c[1], 2.2, '#f4f6f8'); rain(ctx, c[0], c[1] + 40, 120, t, 8); ctx.restore(); }
    if (o.lowH > 0) { const a = P(xr, 1.5, 0.1), b = P(xs, 1.5, 0.1); ctx.save(); ctx.globalAlpha *= o.lowH; circle(ctx, a[0], a[1] + 50, 34); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, 'L', a[0], a[1] + 64, fU(38, 800), C.cream, 'center'); if (o.hiH > 0) { ctx.globalAlpha = o.hiH; circle(ctx, b[0], b[1] + 50, 34); ctx.fillStyle = C.blue; ctx.fill(); text(ctx, 'H', b[0], b[1] + 64, fU(38, 800), C.cream, 'center'); } ctx.restore(); }
  }
}
function infoRows(ctx, t, rows, x = 1290, y0 = 310, w = 540) {
  rows.forEach(([tt, a, en, col], i) => show(ctx, t, tt, () => { const y = y0 + i * 104; card(ctx, x, y, w, 90, { r: 20 }); rrect(ctx, x, y, 10, 90, 5); ctx.fillStyle = col; ctx.fill(); text(ctx, a, x + 30, y + 42, fU(26, 800), C.ink); if (en) text(ctx, en, x + 30, y + 75, fI(26), C.clayD); }));
}
function sLaut(ctx, t) {
  scene(ctx, t, 'laut', '#e3edf3', () => {
    slab(ctx, t, { trades: ap(t, U_(10).v0, 0.6), drift: ap(t, U_(11).v0, 0.8), up: ap(t, U_(14).v0, 0.6), fish: ap(t, U_(16).v0, 0.6), tTherm: U_(13).v0 });
    infoRows(ctx, t, [[U_(10).v0, 'angin pasat timur: timur ke barat', 'easterly trade winds', C.ink], [U_(12).v0, 'air hangat menumpuk di barat', 'warm pool', C.clay], [U_(13).v0, 'muka laut barat sedikit lebih tinggi', '', C.amber], [U_(15).v0, 'Peru: air dingin naik', 'upwelling', C.blue], [U_(16).v0, 'kaya nutrien: perikanan kaya', '', C.forestL]]);
    title(ctx, t, 'laut', 'Kondisi normal: lautnya');
  });
}
function sAtmos(ctx, t) {
  scene(ctx, t, 'atmos', '#dfe9f0', () => {
    const k = (n) => ap(t, U_(n).v0, 0.6);
    slab(ctx, t, { trades: 0.6, drift: 0.4, up: 0.5, fish: 0.6, loop: 1, up1: k(18), lowH: k(19), top: k(20), down: k(21), hiH: k(21), ret: k(22) });
    infoRows(ctx, t, [[U_(18).v0, 'Indonesia: udara naik, awan, hujan', '', C.clay], [U_(19).v0, 'tekanan permukaan RENDAH', '', C.clay], [U_(20).v0, 'atas: mengalir ke timur', '', C.ink], [U_(21).v0, 'Peru: udara turun, tekanan TINGGI', '', C.blue], [U_(22).v0, 'permukaan: kembali sebagai pasat', '', C.forestL]]);
    show(ctx, t, U_(23).v0, () => { card(ctx, 110, 230, 580, 130, { r: 24, bg: C.forest }); text(ctx, 'SIRKULASI WALKER', 150, 290, fU(40, 800), C.amber); text(ctx, 'Walker circulation', 150, 335, fI(32), C.cream); });
    title(ctx, t, 'atmos', 'Kondisi normal: atmosfernya');
  });
}

// ---------------------------------------------------------------- Tahiti - Darwin
function baro(ctx, x, y, r, v, col, lab) { circle(ctx, x, y, r); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke(); const a = Math.PI * (0.8 + 1.4 * clamp((v - 1000) / 24)); arrowLine(ctx, x, y, x + Math.cos(a) * r * 0.75, y + Math.sin(a) * r * 0.75, col, 5, 14); circle(ctx, x, y, 5); ctx.fillStyle = C.ink; ctx.fill(); text(ctx, `${v.toFixed(0)} mb`, x, y + r * 0.6, fU(r * 0.24, 800), C.ink, 'center'); pill(ctx, lab, x, y - r - 24, fU(24, 800), col, C.cream, 14, 44, 'center'); }
function sTahiti(ctx, t) {
  scene(ctx, t, 'tahiti', C.sand, () => {
    const box = { x: 110, y: 240, w: 1700, h: 680 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
    const pr = pacMap(ctx, t, box, [100, 290, -40, 32]);
    const d = pr(130.8, -12.5), th = pr(210.4, -17.6);
    const k = ap(t, U_(24).v0 + 1, 0.6);
    if (k > 0) { ctx.save(); ctx.globalAlpha *= k; [d, th].forEach((p) => { circle(ctx, p[0], p[1], 12); ctx.fillStyle = C.ink; ctx.fill(); }); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.setLineDash([12, 8]); ctx.beginPath(); ctx.moveTo(d[0], d[1]); ctx.lineTo(th[0], th[1]); ctx.stroke(); ctx.setLineDash([]); baro(ctx, d[0] - 20, d[1] + 150, 74, 1008 + Math.sin(t) * 0.5, C.clay, 'Darwin'); baro(ctx, th[0], th[1] + 150, 74, 1013 + Math.sin(t * 0.8) * 0.5, C.blue, 'Tahiti'); ctx.restore(); }
    show(ctx, t, U_(25).v0, () => { card(ctx, 600, 270, 720, 150, { r: 24, bg: C.forest }); text(ctx, 'selisih tekanan Tahiti – Darwin', 640, 330, fU(30, 800), C.cream); text(ctx, 'dasar indeks osilasi selatan (SOI) · video El Niño', 640, 380, fU(24, 600), C.amber); });
    title(ctx, t, 'tahiti', 'Memantau kekuatan sirkulasi Walker');
  });
}

// ---------------------------------------------------------------- weak / strong + MJO
function sPenting(ctx, t) {
  const mjo = t >= U_(30).v0 - 0.3;
  if (!mjo) {
    scene(ctx, t, 'penting', '#dfe9f0', () => {
      const wk = ap(t, U_(28).v0, 1.6, E.inOutCubic), st = ap(t, U_(29).v0, 1.4, E.inOutCubic);
      const sh = wk * 1 - st * 1.6;
      slab(ctx, t, { trades: 0.8 - 0.6 * wk + 0.6 * st, drift: 0.4, up: 0.5 - 0.4 * wk, loop: 1, up1: 1, lowH: 1, top: 1, down: 1, hiH: 1, ret: 1, shift: sh });
      const lab = st > 0.5 ? ['MENGUAT', 'Indonesia lebih BASAH', 'La Niña', C.blue] : wk > 0.5 ? ['MELEMAH', 'warm pool ke timur, Indonesia lebih KERING', 'El Niño', C.clay] : ['NORMAL', 'gangguan sirkulasi ini memicu', 'El Niño dan La Niña', C.forest];
      card(ctx, 110, 300, 640, 190, { r: 24, bg: lab[3] }); text(ctx, `Walker ${lab[0]}`, 150, 365, fU(40, 800), C.cream); text(ctx, lab[1], 150, 412, fU(24, 700), C.cream); text(ctx, lab[2], 150, 460, fI(34), C.amber);
      title(ctx, t, 'penting', 'Mengapa penting bagi Indonesia?');
    });
  } else {
    scene(ctx, t, 'penting', C.sand, () => {
      const box = { x: 110, y: 240, w: 1700, h: 680 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 });
      const pr = G.mapProj(box, [40, 220, -30, 40]);
      const W2 = PAC; G.drawMap(ctx, W2, pr, { t });
      const ph = ((t - U_(30).v0) / 7) % 1, lo = lerp(60, 190, ph);
      ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
      for (let j = 0; j < 7; j++) { const p = pr(lo + (j - 3) * 4, (hash01(j, 2) - 0.5) * 10); cloud(ctx, p[0], p[1], 1.0 + 0.4 * hash01(j, 3), '#e9eef3'); rain(ctx, p[0], p[1] + 20, 50, t + j, 4); }
      const a = pr(lo + 16, -14), b = pr(lo + 34, -14); arrowLine(ctx, a[0], a[1], b[0], b[1], C.clayD, 10, 30);
      ctx.restore();
      card(ctx, 140, 270, 760, 150, { r: 24, bg: C.forest }); text(ctx, 'MJO merambat ke timur', 180, 335, fU(38, 800), C.amber); text(ctx, 'Madden–Julian Oscillation · fenomena zonal', 180, 385, fI(32), C.cream);
      title(ctx, t, 'penting', 'Fenomena zonal lain: MJO');
    });
  }
}

run({
  DUR, no: 11, code: 'B01-11', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Sirkulasi Walker', sub: 'sirkulasi zonal di ekuator Pasifik · warm pool · upwelling',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-12 · Kelembapan Udara',
  SCN: [['hook', 0], ['arah', 3], ['laut', 9], ['atmos', 17], ['tahiti', 24], ['penting', 26], ['soal', 31], ['jebakan', 35], ['ringkas', 39], ['outro', 43]],
  TERMS: [
    ['Sirkulasi meridional', 'meridional circulation', 'Bergerak sepanjang meridian (utara–selatan)', 5],
    ['Sirkulasi zonal', 'zonal circulation', 'Bergerak sepanjang garis lintang (barat–timur)', 7],
    ['Sirkulasi Walker', 'Walker circulation', 'Sirkulasi zonal di ekuator Pasifik', 8],
    ['Kolam air hangat', 'warm pool', 'Tumpukan air hangat di sekitar Indonesia–Papua', 12],
    ['Upwelling', 'upwelling', 'Naiknya air dingin kaya nutrien (Peru)', 15],
    ['MJO', 'Madden–Julian Oscillation', 'Gangguan awan-hujan yang merambat ke timur', 30],
  ],
  hook: { cards: [], punch: [2, ''] },
  soal: {
    q: 'Sirkulasi Walker termasuk sirkulasi zonal karena …',
    opts: ['digerakkan perbedaan salinitas', 'bergerak sepanjang ekuator, barat–timur', 'terjadi hanya di lintang tengah', 'bergerak dari ekuator ke kutub', 'berganti arah setiap enam bulan'], ans: 1, optFs: 27,
    ansT: () => tw('jawabannya', U_(34).v0 - 0.3),
    steps: () => [[U_(32).v0, '1) Arah gerak Walker', C.forest3, 28], [tw('barat', U_(32).v0), 'sepanjang ekuator: barat–timur', C.cream, 38], [tw('lintang', U_(32).v0), 'sepanjang garis lintang', C.cream, 38], [U_(33).v0, '= sirkulasi ZONAL', C.amber, 52]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(36).v0, 'Udara naik di Peru dan turun di Indonesia', 'Udara NAIK di Indonesia, TURUN di Peru', tw('bukan', U_(36).v0)],
      [U_(37).v0, 'Walker adalah bagian dari sel Hadley', 'Hadley meridional, Walker ZONAL', U_(38).v0]],
  },
  ringkas: {
    items: () => [[tw('zonal', U_(40).v0), 'Walker: sirkulasi zonal di ekuator Pasifik'], [tw('naik', U_(41).v0), 'Naik di Indonesia (warm pool), turun di Peru'], [tw('pasat', U_(41).v0), 'Digerakkan angin pasat timur']],
  },
  scenes: { hook: sHook, arah: sArah, laut: sLaut, atmos: sAtmos, tahiti: sTahiti, penting: sPenting },
  async init() {
    W110 = await fetch('assets/world110.json').then((r) => r.json());
    const W50 = await fetch('assets/world50.json').then((r) => r.json());
    const sh = W50.map((r) => (r.every(([lo]) => lo < -20) ? r.map(([lo, la]) => [lo + 360, la]) : r));
    PAC = G.subset(sh, [40, 300, -50, 45]);
  },
});
