// B01-13 · Adiabatik dan Stabilitas · OSNGEO.id — pure function of time (seconds). New style.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { gumpal, tag, bigNum, thermo, sawah, drop } from './lib/gumpal.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 251.0;
const u = (i) => U_(i).v0;
const sky = (ctx, top, bot) => { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); };
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(k); ctx.restore(); };

// ---------------------------------------------------------------- hook: deodorant cold, pump warm
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#f2efe8', () => {
    ctx.fillStyle = '#e8eef2'; ctx.fillRect(0, 0, W / 2, H); ctx.fillStyle = '#f6e9dc'; ctx.fillRect(W / 2, 0, W / 2, H);
    // deodorant can + spray + hand
    const ks = ap(t, u(0), 0.6);
    ctx.save(); ctx.globalAlpha *= ks; ctx.translate(300, 620); ctx.rotate(-0.25);
    const cg = ctx.createLinearGradient(-60, 0, 60, 0); cg.addColorStop(0, '#5a7f9a'); cg.addColorStop(0.5, '#b6d3e6'); cg.addColorStop(1, '#3f6580'); rrect(ctx, -60, -170, 120, 300, 26); ctx.fillStyle = cg; ctx.fill(); rrect(ctx, -34, -215, 68, 50, 10); ctx.fillStyle = '#e9eef2'; ctx.fill(); ctx.restore();
    if (ks > 0) for (let i = 0; i < 40; i++) { const ph = (t * 1.6 + hash01(i, 2)) % 1, a = -0.25 - 0.35 + hash01(i, 3) * 0.7; const x = 340 + Math.cos(a) * ph * 380, y = 420 + Math.sin(a) * ph * 380 * 0.6 - ph * 40; circle(ctx, x, y, 4 + ph * 10); ctx.fillStyle = `rgba(190,225,245,${(1 - ph) * ks})`; ctx.fill(); }
    ctx.save(); ctx.globalAlpha *= ks; ctx.fillStyle = '#f0c9a3'; rrect(ctx, 620, 380, 220, 120, 50); ctx.fill(); for (let k = 0; k < 4; k++) { rrect(ctx, 820, 385 + k * 28, 80, 24, 12); ctx.fill(); } ctx.restore();
    show_(ctx, t, u(1), 1e9, () => { thermo(ctx, 760, 820, 230, 0.2, C.cold, ''); text(ctx, 'dingin', 760, 560, fU(40, 800), C.blue, 'center'); });
    // bike pump
    const kp = ap(t, u(2), 0.6), stroke = 0.5 + 0.5 * Math.sin(t * 6);
    ctx.save(); ctx.globalAlpha *= kp; const px = 1300, py = 900;
    rrect(ctx, px - 40, py - 420, 80, 420, 18); ctx.fillStyle = '#3c4f5a'; ctx.fill(); const hy = py - 420 - 40 - stroke * 120; ctx.fillStyle = '#c8c8c8'; ctx.fillRect(px - 8, hy, 16, py - 420 - hy); rrect(ctx, px - 110, hy - 26, 220, 34, 16); ctx.fillStyle = '#222'; ctx.fill(); rrect(ctx, px - 120, py - 10, 240, 24, 10); ctx.fillStyle = '#222'; ctx.fill();
    ctx.strokeStyle = '#222'; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(px + 30, py - 60); ctx.bezierCurveTo(px + 200, py - 40, px + 260, py - 220, px + 340, py - 260); ctx.stroke();
    const warm = ap(t, u(3), 1.2); if (warm > 0) { const g = ctx.createRadialGradient(px, py - 120, 10, px, py - 120, 140); g.addColorStop(0, `rgba(255,140,60,${0.6 * warm})`); g.addColorStop(1, 'rgba(255,140,60,0)'); ctx.fillStyle = g; circle(ctx, px, py - 120, 140); ctx.fill(); }
    ctx.restore();
    show_(ctx, t, u(3), 1e9, () => { thermo(ctx, 1620, 820, 230, 0.85, C.clay, ''); text(ctx, 'hangat', 1620, 560, fU(40, 800), C.clayD, 'center'); });
    show_(ctx, t, u(5), 1e9, () => { tag(ctx, 480, 190, 'mengembang', '', 1, C.blue); tag(ctx, 1440, 190, 'memampat', '', 1, C.clay); });
  });
}
// ---------------------------------------------------------------- principle with Gumpal
function sPrinsip(ctx, t) {
  scene(ctx, t, 'prinsip', '#f2efe8', () => {
    const e = ap(t, u(6), 1.6, E.inOutCubic), c = ap(t, u(7), 1.6, E.inOutCubic);
    gumpal(ctx, 560, 560, 170 * (1 + 0.45 * e), { t, temp: lerp(0.6, 0.1, e), mood: e > 0.5 ? 'cold' : 'happy', shiver: e });
    for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; const r0 = 200 + e * 80; arrowLine(ctx, 560 + Math.cos(a) * r0, 560 + Math.sin(a) * r0, 560 + Math.cos(a) * (r0 + 60), 560 + Math.sin(a) * (r0 + 60), `rgba(43,108,176,${e})`, 5, 16); }
    gumpal(ctx, 1360, 560, 170 * (1 - 0.3 * c), { t, temp: lerp(0.6, 0.95, c), mood: c > 0.5 ? 'hot' : 'happy', sweat: c, squash: 0.4 * c });
    for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; const r0 = 260 - c * 60; arrowLine(ctx, 1360 + Math.cos(a) * (r0 + 60), 560 + Math.sin(a) * (r0 + 60), 1360 + Math.cos(a) * r0, 560 + Math.sin(a) * r0, `rgba(224,121,79,${c})`, 5, 16); }
    show_(ctx, t, u(6), 1e9, () => text(ctx, 'mengembang = dingin', 560, 900, fU(42, 800), C.blue, 'center'));
    show_(ctx, t, u(7), 1e9, () => text(ctx, 'dimampatkan = panas', 1360, 900, fU(42, 800), C.clayD, 'center'));
  });
}

// ---------------------------------------------------------------- the rise: altitude camera
function altAt(t) {
  const a1 = ap(t, u(10), u(18) - u(10), E.inOutCubic) * 1000; // 0 -> 1000 m
  const a2 = ap(t, u(26), u(28) - u(26) + 1.5, E.inOutCubic) * 1000; // 1000 -> 2000 m
  return a1 + a2;
}
const tempAt = (a) => (a <= 1000 ? 30 - a / 100 : 20 - (a - 1000) / 100 * 0.6);
function sNaik(ctx, t) {
  const a = altAt(t), T = tempAt(a), cloudK = ap(t, u(18) - 0.2, 1.2);
  const PX = 0.42; // px per metre
  const night = 0; sky(ctx, mix('#9fd0ee', '#5b8fbf', a / 2200), mix('#eaf5fb', '#b9d8ee', a / 2200));
  const ex = E.inCubic(prog(t, SC.naik[1] - 0.35, SC.naik[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  const gy = 620, base = gy + a * PX; // screen y of altitude 0
  // far mountains + clouds parallax
  ctx.fillStyle = '#b8d0c4'; ctx.beginPath(); ctx.moveTo(0, base + 60); for (let x = 0; x <= W; x += 40) ctx.lineTo(x, base - 160 * 0.6 - 90 * Math.sin(x * 0.004) + a * 0.12); ctx.lineTo(W, H + 400); ctx.lineTo(0, H + 400); ctx.fill();
  for (let i = 0; i < 9; i++) { const alt = 300 + i * 260, y = base - alt * PX + a * 0.1 * (i % 3); const x = ((hash01(i, 2) * W + t * (10 + i * 3)) % (W + 400)) - 200; cloud(ctx, x, y, 0.8 + hash01(i, 3) * 0.8, 'rgba(255,255,255,0.85)', 'rgba(0,0,0,0)'); }
  sawah(ctx, base, t, W);
  // air molecules: denser near ground
  for (let i = 0; i < 160; i++) { const alt = Math.pow(hash01(i, 7), 1.8) * 2600, y = base - alt * PX, x = hash01(i, 8) * W + Math.sin(t + i) * 12; if (y < -20 || y > H + 20) continue; circle(ctx, x, y, 4); ctx.fillStyle = 'rgba(29,65,56,0.25)'; ctx.fill(); }
  // altitude ruler
  ctx.strokeStyle = 'rgba(29,65,56,0.5)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(160, 0); ctx.lineTo(160, H); ctx.stroke();
  for (let m = 0; m <= 2500; m += 250) { const y = base - m * PX; if (y < -30 || y > H + 30) continue; ctx.beginPath(); ctx.moveTo(150, y); ctx.lineTo(m % 500 ? 170 : 185, y); ctx.stroke(); if (m % 500 === 0) text(ctx, `${m.toLocaleString('id-ID')} m`, 140, y + 9, fU(24, 800), C.forest, 'right'); }
  // LCL dashed line
  const yL = base - 1000 * PX; show_(ctx, t, u(16), 1e9, () => { ctx.setLineDash([16, 12]); ctx.strokeStyle = C.blue; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(190, yL); ctx.lineTo(W - 80, yL); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'dasar awan', 200, yL - 14, fU(28, 800), C.blue); });
  // Gumpal
  const r = 150 * (1 + a / 4000);
  gumpal(ctx, 860, gy, r, { t, temp: clamp((T - 10) / 22), cloud: cloudK, mood: cloudK > 0.5 ? 'wow' : T < 24 ? 'cold' : 'happy', shiver: clamp((24 - T) / 8) * (1 - cloudK) * 0.7, glass: cloudK > 0.4 ? null : 0.8, fill: clamp(0.62 + (30 - T) / 8 * 0.38) });
  // latent heat sparks
  show_(ctx, t, u(29), u(31), () => { for (let i = 0; i < 10; i++) { const ph = (t * 1.2 + i / 10) % 1, an = i / 10 * Math.PI * 2; const x = 860 + Math.cos(an) * r * 0.6 * (0.4 + ph), y = gy + Math.sin(an) * r * 0.5 * (0.4 + ph); ctx.fillStyle = `rgba(255,150,60,${1 - ph})`; ctx.beginPath(); ctx.moveTo(x, y - 14); ctx.quadraticCurveTo(x + 10, y, x, y + 10); ctx.quadraticCurveTo(x - 10, y, x, y - 14); ctx.fill(); } tag(ctx, 860, gy - r - 70, 'panas laten', 'latent heat', 1, C.clay); });
  // thermometer + number beside Gumpal
  thermo(ctx, 1260, 760, 300, clamp((T - 10) / 22), mix(C.cold, C.clay, clamp((T - 10) / 22)), '');
  bigNum(ctx, 1500, 650, T, ' °C', ap(t, u(13) - 1, 0.5), 110, C.forest, a > 1000 ? 1 : 0);
  bigNum(ctx, 1500, 760, a, ' m', ap(t, u(13) - 1, 0.5), 60, C.gray);
  // rate pills
  show_(ctx, t, u(13), u(18), () => pill(ctx, '−1 °C / 100 m', 1500, 860, fU(36, 800), C.clay, C.cream, 22, 64, 'center'));
  show_(ctx, t, u(26), u(31), () => pill(ctx, '−0,6 °C / 100 m', 1500, 860, fU(36, 800), C.blue, C.cream, 22, 64, 'center'));
  // LCL formula, minimal
  show_(ctx, t, u(21), u(26), () => { card(ctx, 520, 150, 880, 150, { r: 30, bg: C.forest }); const k1 = ap(t, u(22), 0.4), k2 = ap(t, u(23), 0.4), k3 = ap(t, tw('seribu', u(24)), 0.4); text(ctx, '125 × (', 560, 248, fU(56, 800), C.cream); if (k1 > 0) { ctx.save(); ctx.globalAlpha *= k1; text(ctx, '30 − 22', 760, 248, fU(56, 800), C.amber); ctx.restore(); } text(ctx, ')', 975, 248, fU(56, 800), C.cream); if (k3 > 0) { ctx.save(); ctx.globalAlpha *= k3; text(ctx, '= 1.000 m', 1010, 248, fU(56, 800), C.amber); ctx.restore(); } });
  ctx.restore();
}

// ---------------------------------------------------------------- compare with surroundings
function sBanding(ctx, t) {
  scene(ctx, t, 'banding', '#e6f0f6', () => {
    const warmCase = t < u(35);
    const k = warmCase ? ap(t, u(34), 3.5, E.inOutCubic) : ap(t, u(35), 3, E.inOutCubic);
    // environment crowd
    for (let i = 0; i < 46; i++) { const x = 140 + (i % 9) * 205 + Math.sin(t + i) * 8, y = 220 + Math.floor(i / 9) * 160 + Math.cos(t * 0.8 + i) * 6; if (Math.hypot(x - 960, y - 560) < 220) continue; circle(ctx, x, y, 46); ctx.fillStyle = warmCase ? 'rgba(143,202,242,0.8)' : 'rgba(255,190,140,0.8)'; ctx.fill(); }
    const gy = 560 + (warmCase ? -380 * k : 300 * k);
    gumpal(ctx, 960, gy, 130, { t, temp: warmCase ? 0.95 : 0.05, mood: warmCase ? 'happy' : 'cold', shiver: warmCase ? 0 : 0.6, look: [0, warmCase ? -1 : 1] });
    if (warmCase && k > 0) { ctx.strokeStyle = '#8a6a44'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(900, gy + 110); ctx.lineTo(925, gy + 180); ctx.moveTo(1020, gy + 110); ctx.lineTo(995, gy + 180); ctx.stroke(); rrect(ctx, 920, gy + 175, 80, 50, 10); ctx.fillStyle = '#b07a3e'; ctx.fill(); }
    show_(ctx, t, u(34), u(35), () => tag(ctx, 960, 960, 'lebih hangat: naik', '', 1, C.clay));
    show_(ctx, t, u(35), 1e9, () => tag(ctx, 960, 160, 'lebih dingin: turun', '', 1, C.blue));
    show_(ctx, t, u(33), u(34), () => tag(ctx, 960, 960, 'bandingkan dengan sekitarnya', '', 1, C.forest));
  });
}
// ---------------------------------------------------------------- ball in bowl vs on hill
function sBola(ctx, t) {
  scene(ctx, t, 'bola', '#f2efe8', () => {
    const bowl = (x, y) => { ctx.fillStyle = '#c9d8c2'; ctx.beginPath(); ctx.moveTo(x - 300, y - 160); ctx.quadraticCurveTo(x, y + 260, x + 300, y - 160); ctx.lineTo(x + 300, y + 120); ctx.lineTo(x - 300, y + 120); ctx.closePath(); ctx.fill(); ctx.strokeStyle = C.forest; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x - 300, y - 160); ctx.quadraticCurveTo(x, y + 260, x + 300, y - 160); ctx.stroke(); };
    const hill = (x, y) => { ctx.fillStyle = '#e8d2ae'; ctx.beginPath(); ctx.moveTo(x - 300, y + 120); ctx.quadraticCurveTo(x, y - 380, x + 300, y + 120); ctx.closePath(); ctx.fill(); ctx.strokeStyle = C.clayD; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x - 300, y + 120); ctx.quadraticCurveTo(x, y - 380, x + 300, y + 120); ctx.stroke(); };
    const k1 = ap(t, u(37), 0.6), k2 = ap(t, u(39), 0.6);
    if (k1 > 0) { ctx.save(); ctx.globalAlpha *= k1; bowl(520, 600); const ph = Math.max(0, t - u(37) - 0.8); const off = Math.exp(-ph * 0.6) * Math.cos(ph * 3) * 200 * (ph > 0 ? 1 : 0); const x = 520 + off, y = 600 + 260 * 0.5 * (1 - (off / 300) ** 2) - 60 + (off / 300) ** 2 * -40; circle(ctx, x, y - 40, 44); ctx.fillStyle = C.blue; ctx.fill(); ctx.restore(); }
    if (k2 > 0) { ctx.save(); ctx.globalAlpha *= k2; hill(1400, 600); const ph = Math.max(0, t - u(39) - 1.0); const s = Math.min(1, ph * ph * 0.35); const x = 1400 + s * 320, yy = (xx) => { const f = (xx - 1100) / 600; return 600 + 120 - 2 * f * (1 - f) * 500 * 1 - 0; }; const y = s < 0.94 ? yy(x) : 720 + (s - 0.94) * 600; circle(ctx, x, y - 44, 44); ctx.fillStyle = C.clay; ctx.fill(); ctx.restore(); }
    show_(ctx, t, u(38), 1e9, () => tag(ctx, 520, 900, 'stabil', 'stable', 1, C.blue));
    show_(ctx, t, u(40), 1e9, () => tag(ctx, 1400, 900, 'labil', 'unstable', 1, C.clay));
  });
}
// ---------------------------------------------------------------- atmosphere: unstable / stable / conditional
function cb(ctx, x, y, h, t, a = 1) {
  if (h <= 5) return; ctx.save(); ctx.globalAlpha *= a;
  const g = ctx.createLinearGradient(0, y - h, 0, y); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#9aa8b5'); ctx.fillStyle = g;
  for (let i = 0; i < 14; i++) { const f = i / 13, cy = y - f * h, r = 70 + 40 * Math.sin(f * 3 + 1) + (f > 0.85 ? 60 : 0); circle(ctx, x + Math.sin(i * 1.7 + t * 0.5) * 20, cy, r); ctx.fill(); }
  if (h > 500) { ctx.beginPath(); ctx.ellipse(x + 60, y - h, 260, 50, 0, 0, Math.PI * 2); ctx.fill(); }
  ctx.restore();
}
function sAtmos(ctx, t) {
  const ph = t < u(45) ? 0 : t < u(48) ? 1 : 2;
  sky(ctx, ph === 0 ? '#7a8fa3' : ph === 1 ? '#b9d8ee' : '#9fc6e2', ph === 0 ? '#c9d4dc' : '#eef6fb');
  const ex = E.inCubic(prog(t, SC.atmos[1] - 0.35, SC.atmos[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  sawah(ctx, 860, t, W, ph === 0 ? 0.3 : 0);
  if (ph === 0) {
    const g = ap(t, u(42), 6, E.inOutCubic); cb(ctx, 960, 820, 80 + 640 * g, t);
    const gyy = 820 - 640 * g * 0.7; gumpal(ctx, 560, lerp(780, 300, g), 90, { t, temp: 0.9, mood: 'happy', cloud: g > 0.5 ? (g - 0.5) * 2 : 0, look: [1, -1] });
    if (g > 0.7 && Math.sin(t * 5) > 0.8) { ctx.strokeStyle = '#ffe680'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(980, 520); ctx.lineTo(940, 650); ctx.lineTo(990, 650); ctx.lineTo(940, 800); ctx.stroke(); }
    if (g > 0.6) rain(ctx, 960, 830, 300, t, 12);
    show_(ctx, t, u(43), 1e9, () => tag(ctx, 960, 160, 'labil', 'unstable', 1, C.clay));
  } else if (ph === 1) {
    for (let k = 0; k < 3; k++) { ctx.fillStyle = `rgba(255,255,255,${0.5 + k * 0.1})`; ctx.beginPath(); ctx.ellipse(960 + Math.sin(t * 0.2 + k) * 60, 520 + k * 40, 900, 40, 0, 0, Math.PI * 2); ctx.fill(); }
    const s = ap(t, u(45), 3); const bob = Math.sin(t * 1.5) * 20;
    gumpal(ctx, 760, 700 - 150 * Math.sin(Math.min(1, s) * Math.PI) + bob * (s > 0.99 ? 1 : 0), 110, { t, temp: 0.2, mood: 'calm' });
    sun(ctx, 1600, 200, 60, t);
    show_(ctx, t, u(46), 1e9, () => tag(ctx, 960, 160, 'stabil', 'stable', 1, C.blue));
  } else {
    const k = ap(t, u(49) - 0.5, 4, E.inOutCubic); const sat = k > 0.45;
    const y = sat ? lerp(560, 200, (k - 0.45) / 0.55) : lerp(760, 560, k / 0.45);
    gumpal(ctx, 960, y, 120, { t, temp: sat ? 0.6 : 0.3, cloud: sat ? clamp((k - 0.45) * 4) : 0, mood: sat ? 'wow' : 'calm' });
    ctx.setLineDash([14, 10]); ctx.strokeStyle = C.blue; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(200, 560); ctx.lineTo(W - 200, 560); ctx.stroke(); ctx.setLineDash([]);
    text(ctx, 'kering: stabil', 1500, 650, fU(34, 800), C.forest, 'center'); text(ctx, 'jenuh: labil', 1500, 480, fU(34, 800), C.clayD, 'center');
    show_(ctx, t, u(48), 1e9, () => tag(ctx, 960, 160, 'labil bersyarat', 'conditionally unstable', 1, C.forestL));
  }
  ctx.restore();
}

run({
  DUR, no: 13, code: 'B01-13', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Adiabatik & Stabilitas', sub: 'udara naik, mengembang, dan mendingin',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-14 · Efek Föhn dan Bayangan Hujan',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['prinsip', 6], ['naik', 9], ['banding', 31], ['bola', 36], ['atmos', 41], ['soal', 50], ['jebakan', 54], ['ringkas', 57], ['outro', 62]],
  TERMS: [
    ['Proses adiabatik', 'adiabatic process', '', 12],
    ['Laju adiabatik kering', 'dry adiabatic lapse rate', '', 14],
    ['Dasar awan', 'lifting condensation level', '', 19],
    ['Laju adiabatik basah', 'saturated adiabatic lapse rate', '', 27],
    ['Labil', 'unstable', '', 43],
    ['Stabil', 'stable', '', 46],
    ['Labil bersyarat', 'conditionally unstable', '', 48],
  ],
  hook: { cards: [], punch: [5, ''] },
  soal: {
    q: 'Suhu udara di permukaan 31 °C dan titik embunnya 23 °C. Dengan rumus h ≈ 125 × (T − Td), ketinggian dasar awan kumulus adalah …',
    opts: ['125 m', '800 m', '1.000 m', '2.875 m', '3.875 m'], ans: 2, optFs: 34,
    ansT: () => tw('jawabannya', u(53) - 0.3),
    steps: () => [[u(51), 'T − Td', C.forest3, 30], [tw('delapan', u(51)), '31 − 23 = 8', C.cream, 46], [u(52), '125 × 8', C.cream, 46], [tw('seribu', u(52)), '= 1.000 m', C.amber, 60]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(55), 'Laju basah kecil karena udara jenuh berat', 'Karena pelepasan PANAS LATEN', tw('bukan', u(55))],
      [u(56), 'Atmosfer stabil menghasilkan badai', 'Stabil = cuaca tenang, cerah atau berkabut', tw('bukan', u(56))]],
  },
  ringkas: {
    items: () => [[tw('mengembang', u(58)), 'Naik: mengembang dan mendingin'], [tw('satu', u(58)), 'Kering −1 °C, jenuh −0,6 °C per 100 m'], [u(59), 'Labil: udara terus naik, badai']],
  },
  scenes: { hook: sHook, prinsip: sPrinsip, naik: sNaik, banding: sBanding, bola: sBola, atmos: sAtmos },
});
