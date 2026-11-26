// B01-15 · Awan dan Mekanisme Hujan · OSNGEO.id — pure function of time (seconds). New style.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { gumpal, tag, bigNum, drop } from './lib/gumpal.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 232.3;
const u = (i) => U_(i).v0;
const sky = (ctx, top, bot) => { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); };
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(k); ctx.restore(); };

// ---------------------------------------------------------------- cloud painters
function puff(ctx, x, y, s, col = '#ffffff', shade = '#c9d4dc', t = 0) {
  const g = ctx.createLinearGradient(0, y - 80 * s, 0, y + 40 * s); g.addColorStop(0, col); g.addColorStop(1, shade); ctx.fillStyle = g;
  [[-70, 10, 48], [-30, -25, 62], [25, -35, 70], [70, 0, 50], [0, 15, 60]].forEach(([a, b, r], i) => { circle(ctx, x + a * s, y + b * s + Math.sin(t + i) * 2 * s, r * s); ctx.fill(); });
}
function cirrus(ctx, x, y, s, t, a = 1) { ctx.save(); ctx.globalAlpha *= a; ctx.strokeStyle = 'rgba(255,255,255,0.95)'; ctx.lineCap = 'round'; for (let i = 0; i < 6; i++) { ctx.lineWidth = (6 - i * 0.6) * s; ctx.beginPath(); const y0 = y + i * 14 * s; ctx.moveTo(x - 160 * s, y0); ctx.bezierCurveTo(x - 60 * s, y0 - 30 * s + Math.sin(t + i) * 4, x + 40 * s, y0 + 10 * s, x + 170 * s, y0 - 50 * s); ctx.stroke(); } ctx.restore(); }
function layer(ctx, x, y, w, h, col, t, a = 1) { ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = col; for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.ellipse(x + Math.sin(t * 0.3 + k) * 30, y + k * h * 0.18, w * (1 - k * 0.08), h * 0.35, 0, 0, Math.PI * 2); ctx.fill(); } ctx.restore(); }
function mackerel(ctx, x, y, w, t, a = 1) { ctx.save(); ctx.globalAlpha *= a; for (let i = 0; i < 9; i++) for (let j = 0; j < 3; j++) { const px = x - w / 2 + i * w / 8 + j * 22, py = y + j * 30 + Math.sin(i + t) * 3; ctx.fillStyle = 'rgba(255,255,255,0.92)'; ctx.beginPath(); ctx.ellipse(px, py, 30, 14, 0.2, 0, Math.PI * 2); ctx.fill(); } ctx.restore(); }
function cbCloud(ctx, x, base, h, t, a = 1) {
  if (h <= 10) return; ctx.save(); ctx.globalAlpha *= a;
  const g = ctx.createLinearGradient(0, base - h, 0, base); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#7d8a96'); ctx.fillStyle = g;
  for (let i = 0; i < 16; i++) { const f = i / 15, cy = base - f * h, r = 90 + 50 * Math.sin(f * 3 + 1); circle(ctx, x + Math.sin(i * 1.7 + t * 0.4) * 26, cy, r); ctx.fill(); }
  if (h > 450) { const k = clamp((h - 450) / 200); ctx.beginPath(); ctx.ellipse(x + 80, base - h, 340 * k, 60 * k, 0, 0, Math.PI * 2); ctx.fill(); }
  ctx.restore();
}

// ---------------------------------------------------------------- hook: sky time-lapse
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#a9d4ee', () => {
    sky(ctx, '#8ec5e8', '#e6f3fb');
    const k1 = ap(t, tw('bulu', u(1)) - 0.3, 0.6), k2 = ap(t, tw('kapas', u(1)) - 0.3, 0.6), k3 = ap(t, tw('abu-abu', u(1)) - 0.3, 0.8);
    cirrus(ctx, 420 + t * 8, 260, 1.4, t, k1);
    if (k2 > 0) { ctx.save(); ctx.globalAlpha *= k2; puff(ctx, 960 + Math.sin(t * 0.3) * 30, 520, 1.6, '#ffffff', '#cfd9e0', t); puff(ctx, 1450, 600, 1.1, '#ffffff', '#cfd9e0', t); ctx.restore(); }
    layer(ctx, 960, 180, 1200, 200, 'rgba(150,160,170,0.75)', t, k3);
    ctx.fillStyle = '#9dcf7e'; ctx.fillRect(0, 900, W, 180);
    show_(ctx, t, u(2), 1e9, () => { [['cerah', 560, C.amber], ['hujan', 960, C.blue], ['badai', 1360, C.clayD]].forEach(([s, x, col], i) => { const k = sp(t, u(2) + i * 0.4, SPRING.bouncy); ctx.save(); ctx.translate(x, 800); ctx.scale(k, k); circle(ctx, 0, 0, 70); ctx.fillStyle = col; ctx.fill(); text(ctx, s, 0, 12, fU(30, 800), C.cream, 'center'); ctx.restore(); }); });
  });
}
// ---------------------------------------------------------------- Gumpal becomes a cloud; droplets on nuclei
function sTerbentuk(ctx, t) {
  scene(ctx, t, 'terbentuk', '#cfe6f2', () => {
    sky(ctx, '#a9d4ee', '#eaf5fb');
    const k = ap(t, u(4), 5, E.inOutCubic);
    const y = lerp(820, 380, k);
    gumpal(ctx, 700, y, 150, { t, temp: lerp(0.7, 0.4, k), cloud: clamp((k - 0.6) * 2.5), mood: k > 0.8 ? 'wow' : 'happy', look: [0.5, -1] });
    // micro inset
    show_(ctx, t, u(3), 1e9, () => { const cx = 1400, cy = 480, R = 260; circle(ctx, cx, cy, R); ctx.fillStyle = '#eef7fc'; ctx.fill(); ctx.strokeStyle = C.forest; ctx.lineWidth = 10; ctx.stroke(); ctx.save(); circle(ctx, cx, cy, R); ctx.clip(); for (let i = 0; i < 16; i++) { const px = cx - 200 + hash01(i, 2) * 400 + Math.sin(t + i) * 8, py = cy - 200 + hash01(i, 4) * 400 + Math.cos(t * 0.8 + i) * 8; const g = ap(t, u(4) + 2 + hash01(i, 6) * 2, 1.5); circle(ctx, px, py, 8 + 22 * g); ctx.fillStyle = 'rgba(90,168,224,0.75)'; ctx.fill(); circle(ctx, px, py, 6); ctx.fillStyle = '#8a6a44'; ctx.fill(); } ctx.restore(); text(ctx, 'titik air + kristal es', cx, cy + R + 50, fU(30, 800), C.forest, 'center'); });
  });
}
// ---------------------------------------------------------------- four root words
function sKata(ctx, t) {
  scene(ctx, t, 'kata', '#f2efe8', () => {
    const items = [['cirrus', 'serat', u(6)], ['stratus', 'lapisan', u(7)], ['cumulus', 'gumpalan', u(8)], ['nimbus', 'hujan', u(9)]];
    const merge = ap(t, u(10), 1.2, E.inOutCubic);
    items.forEach(([a, b, t0], i) => {
      const k = sp(t, t0 - 0.1, SPRING.bouncy); if (k <= 0) return;
      const x = 270 + i * 460, y = 470; const xx = x;
      ctx.save(); ctx.translate(xx, y); ctx.scale(k, k);
      card(ctx, -190, -230, 380, 460, { r: 32 }); ctx.save(); rrect(ctx, -170, -210, 340, 260, 22); ctx.clip(); ctx.fillStyle = '#9fcdec'; ctx.fillRect(-170, -210, 340, 260);
      if (i === 0) cirrus(ctx, 0, -110, 0.9, t); if (i === 1) layer(ctx, 0, -110, 220, 120, 'rgba(160,170,180,0.9)', t); if (i === 2) puff(ctx, 0, -60, 1.0, '#fff', '#d0dae2', t); if (i === 3) { layer(ctx, 0, -150, 200, 90, 'rgba(110,120,130,0.95)', t); rain(ctx, 0, -110, 220, t, 9); }
      ctx.restore();
      text(ctx, a, 0, 120, fI(64), C.forest, 'center'); text(ctx, b, 0, 180, fU(36, 800), C.clay, 'center');
      ctx.restore();
    });
    show_(ctx, t, u(10) + 0.5, 1e9, () => { tag(ctx, 560, 860, 'cirro + stratus = sirostratus', '', 1, C.forest); tag(ctx, 1380, 860, 'nimbo + stratus = nimbostratus', '', ap(t, u(10) + 1.5, 0.4), C.gray); });
  });
}
// ---------------------------------------------------------------- climb through cloud layers
function sLangit(ctx, t) {
  const climb = ap(t, u(14) - 1, 2.5, E.inOutCubic) * 0.5 + ap(t, u(15) - 1, 2.5, E.inOutCubic) * 0.5; // 0 low .. 1 high
  const off = climb * 1500;
  sky(ctx, mix('#9fd0ee', '#3d6e9e', climb), mix('#eaf5fb', '#b2d3ea', climb));
  const ex = E.inCubic(prog(t, SC.langit[1] - 0.35, SC.langit[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  ctx.save(); ctx.translate(0, off);
  // ground
  ctx.fillStyle = '#9dcf7e'; ctx.fillRect(0, 920, W, 600);
  // altitude ruler
  ctx.strokeStyle = 'rgba(29,65,56,0.4)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(150, -1800); ctx.lineTo(150, 920); ctx.stroke();
  [[2, 600], [7, -560]].forEach(([km, y]) => { ctx.setLineDash([14, 10]); ctx.beginPath(); ctx.moveTo(160, y); ctx.lineTo(W - 100, y); ctx.stroke(); ctx.setLineDash([]); text(ctx, `${km} km`, 140, y + 9, fU(28, 800), C.forest, 'right'); });
  // low: stratus + cumulus
  layer(ctx, 600, 800, 420, 90, 'rgba(165,172,180,0.9)', t, ap(t, tw('stratus', u(12)) - 0.3, 0.6));
  if (ap(t, u(13), 0.6) > 0) { ctx.save(); ctx.globalAlpha *= ap(t, u(13), 0.6); puff(ctx, 1300, 780, 1.1, '#fff', '#d0dae2', t); puff(ctx, 1600, 800, 0.8, '#fff', '#d0dae2', t); ctx.restore(); }
  // mid: altocumulus + altostratus
  mackerel(ctx, 640, -230, 600, t, ap(t, tw('altokumulus', u(14)) - 0.3, 0.6));
  layer(ctx, 1400, -200, 380, 110, 'rgba(170,178,188,0.85)', t, ap(t, tw('altostratus', u(14)) - 0.3, 0.6));
  if (ap(t, tw('altostratus', u(14)), 0.5) > 0) { ctx.save(); ctx.globalAlpha *= 0.6; circle(ctx, 1400, -240, 40); ctx.fillStyle = '#fff6d6'; ctx.fill(); ctx.restore(); }
  // high: cirrus + cirrostratus with halo
  cirrus(ctx, 600, -900, 1.6, t, ap(t, tw('sirus', u(16)) - 0.3, 0.6));
  const kc = ap(t, tw('sirostratus', u(16)) - 0.3, 0.8);
  if (kc > 0) { ctx.save(); ctx.globalAlpha *= kc; sun(ctx, 1400, -900, 50, t); ctx.strokeStyle = 'rgba(255,240,200,0.8)'; ctx.lineWidth = 10; circle(ctx, 1400, -900, 190); ctx.stroke(); layer(ctx, 1400, -900, 420, 120, 'rgba(255,255,255,0.35)', t); ctx.restore(); }
  ctx.restore();
  // name tags (screen space)
  const tags = [[tw('stratus', u(12)), u(13), 'stratus', 600, 680, C.gray], [u(13), u(14) - 0.5, 'kumulus', 1300, 640, C.forestL], [tw('altokumulus', u(14)), u(15) - 0.5, 'altokumulus', 640, -330, C.forest], [tw('altostratus', u(14)), u(15) - 0.5, 'altostratus', 1400, -330, C.gray], [tw('sirus', u(16)), 1e9, 'sirus', 600, -1040, C.blue], [tw('sirostratus', u(16)), 1e9, 'sirostratus · halo', 1400, -660, C.amber]];
  tags.forEach(([a, b, s_, x, wy, col]) => show_(ctx, t, a, b, () => tag(ctx, x, wy + off, s_, '', 1, col)));
  const lay = climb < 0.25 ? 'rendah · di bawah 2 km' : climb < 0.75 ? 'menengah · 2–7 km' : 'tinggi · di atas 7 km';
  if (t > u(12)) pill(ctx, lay, W - 120, 300, fU(30, 800), C.forest, C.cream, 20, 56, 'right');
  ctx.restore();
}
// ---------------------------------------------------------------- rain clouds: Ns and Cb
function sHujan(ctx, t) {
  const cbP = ap(t, u(19), 5, E.inOutCubic);
  sky(ctx, mix('#8c9aa6', '#5b6a78', cbP), '#c9d4dc');
  const ex = E.inCubic(prog(t, SC.hujan[1] - 0.35, SC.hujan[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  ctx.fillStyle = '#7fae6e'; ctx.fillRect(0, 900, W, 180);
  const ns = ap(t, u(18), 0.8) * (1 - ap(t, u(19), 0.8));
  if (ns > 0) { layer(ctx, 960, 300, 1100, 220, 'rgba(90,100,110,0.95)', t, ns); ctx.save(); ctx.globalAlpha *= ns; rain(ctx, 960, 420, 1700, t, 40, '#9fc4dd', 30, 380); ctx.restore(); show_(ctx, t, u(18), u(19), () => tag(ctx, 960, 150, 'nimbostratus', 'hujan merata, lama', 1, C.gray)); }
  if (cbP > 0) {
    const h = 80 + 700 * cbP; cbCloud(ctx, 960, 900, h, t);
    ctx.setLineDash([16, 10]); ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(0, 120); ctx.lineTo(W, 120); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'tropopause', 120, 108, fU(24, 800), '#fff');
    if (t > u(21)) { if (Math.sin(t * 6) > 0.75) { ctx.strokeStyle = '#ffe680'; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(1000, 540); ctx.lineTo(950, 700); ctx.lineTo(1010, 700); ctx.lineTo(950, 900); ctx.stroke(); } rain(ctx, 960, 860, 400, t, 18, '#9fc4dd', 30, 420); for (let i = 0; i < 10; i++) { const ph = (t * 0.9 + i / 10) % 1; circle(ctx, 820 + i * 30, 860 + ph * 60, 7); ctx.fillStyle = '#ffffff'; ctx.fill(); } }
    show_(ctx, t, u(20), 1e9, () => { arrowLine(ctx, 1400, 200, 1260, 140, C.amber, 6, 20); text(ctx, 'landasan', 1410, 220, fU(30, 800), C.amber); });
  }
  ctx.restore();
}
// ---------------------------------------------------------------- droplets collide into a raindrop
function sButir(ctx, t) {
  scene(ctx, t, 'butir', '#e9f2f8', () => {
    const t0 = u(23), mg = ap(t, u(24) + 1, 3.5, E.inOutCubic), fall = ap(t, u(24) + 4.8, 2.5, E.inCubic);
    for (let i = 0; i < 70; i++) { const ax = 300 + hash01(i, 2) * 1300 + Math.sin(t * 2 + i) * 14, ay = 220 + hash01(i, 4) * 500 + Math.cos(t * 1.6 + i) * 12; const x = lerp(ax, 960, mg), y = lerp(ay, 470, mg); if (mg > 0.98) break; circle(ctx, x, y, 9); ctx.fillStyle = 'rgba(90,168,224,0.8)'; ctx.fill(); }
    if (mg > 0.5) drop(ctx, 960, 470 + fall * 520, 30 + 50 * clamp((mg - 0.5) * 2), '#3d8ccc');
    show_(ctx, t, u(23), u(24), () => tag(ctx, 960, 900, 'terlalu ringan untuk jatuh', '', 1, C.gray));
    show_(ctx, t, u(24) + 1, 1e9, () => tag(ctx, 960, 900, 'bertabrakan · bergabung · jatuh', '', 1, C.blue));
  });
}
// ---------------------------------------------------------------- four lifting mechanisms
function sEmpat(ctx, t) {
  const ph = t < u(31) ? 0 : t < u(34) ? 1 : t < u(37) ? 2 : 3;
  const t0 = [u(27), u(31), u(34), u(37)][ph], t1 = [u(31), u(34), u(37), SC.empat[1]][ph];
  const k = clamp((t - t0) / (t1 - t0));
  sky(ctx, ['#9fd0ee', '#a9cfe6', '#b9d8ee', '#a8c4dc'][ph], '#eef6fb');
  const ex = E.inCubic(prog(t, SC.empat[1] - 0.35, SC.empat[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  if (t < u(27)) { // intro: up arrow
    ctx.fillStyle = '#9dcf7e'; ctx.fillRect(0, 900, W, 180); gumpal(ctx, 960, lerp(820, 560, ap(t, u(25), 2, E.inOutCubic)), 130, { t, temp: 0.6, look: [0, -1] }); for (let i = 0; i < 4; i++) { const p = (t * 0.6 + i / 4) % 1; arrowLine(ctx, 760 + i * 130, 900 - p * 300, 760 + i * 130, 860 - p * 300, `rgba(29,65,56,${1 - p})`, 6, 20); } tag(ctx, 960, 180, '4 cara udara naik', '', ap(t, u(26), 0.5), C.forest);
  } else if (ph === 0) {
    ctx.fillStyle = mix('#9dcf7e', '#d9b97a', k); ctx.fillRect(0, 900, W, 180); sun(ctx, 1600, 180, 70, t);
    for (let i = 0; i < 8; i++) { const p = (t * 0.7 + i / 8) % 1; ctx.strokeStyle = `rgba(224,121,79,${1 - p})`; ctx.lineWidth = 4; const x = 600 + i * 90; ctx.beginPath(); ctx.moveTo(x, 900 - p * 140); ctx.bezierCurveTo(x + 10, 880 - p * 140, x - 10, 860 - p * 140, x, 840 - p * 140); ctx.stroke(); }
    const y = lerp(820, 300, ap(t, u(28), 3, E.inOutCubic)); gumpal(ctx, 960, y, 120, { t, temp: 0.9, cloud: clamp((820 - y) / 400 - 0.3), mood: 'happy', look: [0, -1] });
    if (t > u(29)) { cbCloud(ctx, 960, 900, 600 * ap(t, u(29), 3), t, 0.85); rain(ctx, 960, 860, 300, t, 12); }
    show_(ctx, t, u(30), 1e9, () => pill(ctx, 'Bogor, Kota Hujan', 960, 980, fU(30, 800), C.forest, C.cream, 20, 56, 'center'));
  } else if (ph === 1) {
    ctx.fillStyle = '#5f9a5c'; poly(ctx, [[300, 920], [1300, 330], [1500, 360], [1900, 920]]); ctx.fill(); ctx.fillStyle = '#9dcf7e'; ctx.fillRect(0, 900, W, 180);
    const p = ap(t, u(32), 4, E.inOutCubic); const x = lerp(250, 1250, p), y = lerp(780, 230, Math.pow(p, 1.1));
    gumpal(ctx, x, y, 110, { t, temp: lerp(0.7, 0.3, p), cloud: clamp(p * 2 - 0.6), mood: p > 0.5 ? 'wow' : 'happy', look: [1, -0.5] });
    if (p > 0.4) rain(ctx, x, y + 80, 140, t, 7);
    for (let i = 0; i < 4; i++) { const q = (t * 0.5 + i / 4) % 1; arrowLine(ctx, -60 + q * 400, 820 - i * 30, q * 400, 820 - i * 30, '#ffffff', 5, 16); }
    show_(ctx, t, u(33), 1e9, () => pill(ctx, 'lereng barat Bukit Barisan', 960, 990, fU(30, 800), C.forest, C.cream, 20, 56, 'center'));
  } else if (ph === 2) {
    ctx.fillStyle = '#3c8fc2'; ctx.fillRect(0, 900, W, 180);
    const p = ap(t, u(35), 3, E.inOutCubic);
    for (let i = 0; i < 6; i++) { const q = (t * 0.6 + i / 6) % 1; arrowLine(ctx, 100 + q * 600, 820 - (i % 3) * 40, 160 + q * 600, 820 - (i % 3) * 40, C.amber, 6, 20); arrowLine(ctx, W - 100 - q * 600, 820 - (i % 3) * 40, W - 160 - q * 600, 820 - (i % 3) * 40, C.amber, 6, 20); }
    gumpal(ctx, 960, lerp(800, 300, p), 120, { t, temp: 0.75, cloud: clamp(p * 2 - 0.6), squash: 0.3 * (1 - p), mood: 'wow', look: [0, -1] });
    if (p > 0.6) { for (let i = 0; i < 5; i++) puff(ctx, 600 + i * 180, 240 + Math.sin(i) * 20, 0.8, '#fff', '#c9d4dc', t); }
    show_(ctx, t, u(36), 1e9, () => pill(ctx, 'ITCZ', 960, 990, fU(32, 800), C.forest, C.cream, 22, 58, 'center'));
  } else {
    ctx.fillStyle = '#9dcf7e'; ctx.fillRect(0, 900, W, 180);
    const p = ap(t, u(38), 4, E.inOutCubic); const fx = lerp(-200, 900, p);
    ctx.fillStyle = 'rgba(80,140,210,0.55)'; poly(ctx, [[-400, 900], [fx, 900], [fx - 700, 250], [-400, 250]]); ctx.fill(); text(ctx, 'udara dingin', fx - 520, 820, fU(32, 800), '#1d4f8a', 'center');
    ctx.fillStyle = 'rgba(240,150,90,0.25)'; poly(ctx, [[fx, 900], [W + 100, 900], [W + 100, 200], [fx - 700, 200]]); ctx.fill(); text(ctx, 'udara hangat', 1500, 820, fU(32, 800), C.clayD, 'center');
    const gx_ = Math.max(fx + 120, 1100) - 400 * p, gy_ = lerp(780, 320, p); gumpal(ctx, gx_, gy_, 110, { t, temp: 0.8, cloud: clamp(p * 2 - 0.6), mood: 'wow', look: [-1, -1] });
    if (p > 0.5) { layer(ctx, gx_ - 100, gy_ - 60, 500, 110, 'rgba(140,150,160,0.85)', t); rain(ctx, gx_ - 100, gy_, 500, t, 16); }
    show_(ctx, t, u(39), 1e9, () => pill(ctx, 'lintang tengah ±60°', 960, 990, fU(30, 800), C.forest, C.cream, 20, 56, 'center'));
  }
  if (t >= u(27)) { const n = ph + 1; circle(ctx, 120, 140, 50); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, `${n}`, 120, 160, fU(54, 800), C.cream, 'center'); }
  ctx.restore();
}

run({
  DUR, no: 15, code: 'B01-15', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Awan dan Hujan', sub: 'nama awan dan empat cara udara naik',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-16 · Pola Hujan Indonesia',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['terbentuk', 3], ['kata', 5], ['langit', 11], ['hujan', 17], ['butir', 22], ['empat', 25], ['soal', 40], ['jebakan', 44], ['ringkas', 47], ['outro', 50]],
  TERMS: [
    ['Kumulonimbus', 'cumulonimbus', '', 19],
    ['Konveksi', 'convection', '', 27],
    ['Orografi', 'orographic lifting', '', 31],
    ['Konvergensi', 'convergence', '', 34],
    ['Frontal', 'frontal lifting', '', 37],
  ],
  hook: { cards: [], punch: [2, ''] },
  soal: {
    q: 'Dari empat penyebab perawanan (konveksi, konvergensi, orografi, front), penyebab utama hujan di sekitar lintang 60° LU adalah …',
    opts: ['konveksi', 'konvergensi', 'orografi', 'front', 'semuanya sama besar'], ans: 3, optFs: 34,
    ansT: () => tw('jawabannya', u(43) - 0.3),
    steps: () => [[u(41), 'lintang 60°', C.forest3, 30], [tw('front', u(41)), 'front kutub', C.cream, 48], [tw('dingin', u(41)), 'udara kutub bertemu baratan', C.cream, 34], [u(42), '= hujan FRONTAL', C.amber, 56]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(45), 'Awan sirus menghasilkan hujan', 'Sirus tinggi: TIDAK menghasilkan hujan', tw('tidak', u(45))],
      [u(46), 'Hujan sore di Bogor = orografi', 'Pagi terik, sore hujan = KONVEKSI', tw('konveksi', u(46))]],
  },
  ringkas: {
    items: () => [[tw('nama', u(48)), 'Nama awan: cirrus, stratus, cumulus, nimbus'], [tw('kumulonimbus', u(48)), 'Kumulonimbus = awan badai'], [tw('konveksi', u(48)), 'Konveksi, orografi, konvergensi, frontal']],
  },
  scenes: { hook: sHook, terbentuk: sTerbentuk, kata: sKata, langit: sLangit, hujan: sHujan, butir: sButir, empat: sEmpat },
});
