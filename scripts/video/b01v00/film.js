// B01-V00 · Konsep Dasar: Mesin Iklim Bumi · OSNGEO.id
// Pure function of time (seconds). Beat grid is set to period 1 s, so u === t.
// Timing comes from timing.json (VO phrases aligned to the user's recording, +3 s intro, +3 s think pause).
import * as M from './lib/motion.js';

const { W, H, E, prog, lerp, clamp, spring, SPRING, wobble, font, layout, text, fill, rrect, bump, hash01 } = M;

const C = {
  forest: '#1d4138', forestD: '#162923', forestL: '#396957', forest3: '#aac6b5', forest1: '#e2ede4',
  cream: '#fffefa', sand: '#f7f1e8', sand2: '#efe3cf', sand3: '#ded0ba',
  clay: '#e0794f', clayD: '#983f29', amber: '#f2b13a', ink: '#1b322b', gray: '#52655d',
  sea: '#dcebf3', land: '#f3e6c4', blue: '#2b6cb0', cold: '#4a90c2',
};
const D = 'Display', UI = 'UI';
const fD = (s) => font(s, 400, D), fU = (s, w = 500) => font(s, w, UI);

let TM = null, IND = null;
const WORDS = () => TM.words;
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9ñ]/g, '');
// time of the n-th occurrence of word w at or after time `after`
function tw(w, after = 0, n = 0) {
  const k = norm(w); let c = 0;
  for (const x of WORDS()) if (x.t >= after - 0.01 && norm(x.w) === k) { if (c === n) return x.t; c++; }
  console.error('word not found', w, after); return after;
}
const U_ = (i) => TM.units[i];
const sp = (t, t0, cfg = SPRING.snappy) => spring(t - t0, cfg);
const ap = (t, t0, d = 0.45, ease = E.outCubic) => ease(prog(t, t0, t0 + d));

// ---------------------------------------------------------------- scenes (seconds)
const SC = {
  intro: [0, 3.0], hook: [3.0, 18.4], cuaca: [18.4, 42.95], unsur: [42.95, 55.8], matahari: [55.8, 76.2],
  domino: [76.2, 95.95], kendali: [95.95, 113.25], soal: [113.25, 148.55], jebakan: [148.55, 162.8],
  sering: [162.8, 186.5], outro: [186.5, 197.5],
};
const exitP = (t, name, d = 0.35) => E.inCubic(prog(t, SC[name][1] - d, SC[name][1]));

// ---------------------------------------------------------------- HITS (seconds; sfx voiced by sfx.mjs)
const HITS = [];
const hit = (t, label, sfx, o = {}) => HITS.push([t, label, sfx, { gain: 0.6, ...o }]);

// ---------------------------------------------------------------- drawing helpers
function poly(ctx, pts) { ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); }
function circle(ctx, x, y, r) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); }
function card(ctx, x, y, w, h, { r = 28, bg = C.cream, stroke = null, shadow = true } = {}) {
  ctx.save();
  if (shadow) { ctx.shadowColor = 'rgba(22,41,35,0.14)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10; }
  rrect(ctx, x, y, w, h, r); ctx.fillStyle = bg; ctx.fill();
  ctx.restore();
  if (stroke) { rrect(ctx, x, y, w, h, r); ctx.strokeStyle = stroke; ctx.lineWidth = 3; ctx.stroke(); }
}
function arrowLine(ctx, x1, y1, x2, y2, color, w = 6, head = 22) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - Math.cos(a) * head * 0.6, y2 - Math.sin(a) * head * 0.6); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - head * Math.cos(a - 0.45), y2 - head * Math.sin(a - 0.45));
  ctx.lineTo(x2 - head * Math.cos(a + 0.45), y2 - head * Math.sin(a + 0.45)); ctx.closePath(); ctx.fill();
}
function check(ctx, x, y, s, color, p = 1) {
  ctx.strokeStyle = color; ctx.lineWidth = s * 0.16; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const pts = [[x - s * 0.42, y], [x - s * 0.12, y + s * 0.3], [x + s * 0.45, y - s * 0.35]];
  const L1 = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]), L2 = Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
  const d = p * (L1 + L2);
  ctx.beginPath(); ctx.moveTo(...pts[0]);
  if (d <= L1) ctx.lineTo(lerp(pts[0][0], pts[1][0], d / L1), lerp(pts[0][1], pts[1][1], d / L1));
  else { ctx.lineTo(...pts[1]); const k = (d - L1) / L2; ctx.lineTo(lerp(pts[1][0], pts[2][0], k), lerp(pts[1][1], pts[2][1], k)); }
  ctx.stroke();
}
function cross(ctx, x, y, s, color, w = 10) {
  ctx.strokeStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x - s, y - s); ctx.lineTo(x + s, y + s); ctx.moveTo(x + s, y - s); ctx.lineTo(x - s, y + s); ctx.stroke();
}
function wrap(ctx, str, f, maxW) {
  ctx.font = f; const words = str.split(' '); const lines = []; let cur = '';
  for (const w of words) { const n = cur ? cur + ' ' + w : w; if (ctx.measureText(n).width > maxW && cur) { lines.push(cur); cur = w; } else cur = n; }
  if (cur) lines.push(cur); return lines;
}
// text that rises in with a clip mask (directional entrance)
function riseText(ctx, str, x, y, f, color, p, align = 'left') {
  if (p <= 0) return;
  ctx.save(); ctx.globalAlpha *= clamp(p * 1.6);
  text(ctx, str, x, y + (1 - p) * 40, f, color, align);
  ctx.restore();
}
function pill(ctx, str, x, y, f, bg, fg, padX = 22, h = 56, align = 'left') {
  ctx.font = f; const w = ctx.measureText(str).width + padX * 2;
  const x0 = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  rrect(ctx, x0, y - h / 2, w, h, h / 2); ctx.fillStyle = bg; ctx.fill();
  text(ctx, str, x0 + w / 2, y + h * 0.17, f, fg, 'center');
  return w;
}

// ---------------------------------------------------------------- logo (vector, needle can spin)
function logo(ctx, x, y, s, needle = 0, alpha = 1) {
  ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(x, y); ctx.scale(s / 64, s / 64);
  rrect(ctx, 0, 0, 64, 64, 15); ctx.fillStyle = C.forest; ctx.fill();
  ctx.strokeStyle = C.cream; ctx.lineCap = 'round';
  ctx.globalAlpha *= 0.45; ctx.lineWidth = 2.2;
  ctx.beginPath(); ctx.moveTo(14.6, 32); ctx.lineTo(49.4, 32);
  ctx.moveTo(32, 14.6); ctx.bezierCurveTo(26.8, 19.2, 24.2, 25, 24.2, 32); ctx.bezierCurveTo(24.2, 39, 26.8, 44.8, 32, 49.4); ctx.stroke();
  ctx.globalAlpha /= 0.45; ctx.lineWidth = 3.6;
  ctx.beginPath(); ctx.arc(32, 32, 17.4, -Math.PI / 4, 0, true); ctx.stroke();
  ctx.translate(32, 32); ctx.rotate(needle); ctx.translate(-32, -32);
  poly(ctx, [[51.5, 12.5], [35.4, 35.4], [28.6, 28.6]]); ctx.fillStyle = C.clay; ctx.fill();
  poly(ctx, [[12.5, 51.5], [28.6, 28.6], [35.4, 35.4]]); ctx.fillStyle = C.cream; ctx.fill();
  circle(ctx, 32, 32, 2.4); ctx.fillStyle = C.forest; ctx.fill();
  ctx.restore();
}

// ---------------------------------------------------------------- persistent overlays
function cornerMark(ctx) {
  const h = 84, x1 = W - 40, y0 = 36;
  ctx.font = fU(40, 700); const tw_ = ctx.measureText('OSNGEO.id').width;
  const w = tw_ + h + 34, x0 = x1 - w;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.25)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 4;
  rrect(ctx, x0, y0, w, h, h / 2); ctx.fillStyle = 'rgba(29,65,56,0.92)'; ctx.fill(); ctx.restore();
  logo(ctx, x0 + 10, y0 + 10, h - 20);
  text(ctx, 'OSNGEO.id', x0 + h + 8, y0 + h / 2 + 14, fU(40, 700), C.cream);
}
function centerMark(ctx, a = 1, col = C.forest) {
  ctx.save(); ctx.globalAlpha = 0.065 * a; ctx.translate(W / 2, H * 0.47); ctx.rotate(-12 * Math.PI / 180);
  ctx.font = fU(250, 700); ctx.textAlign = 'center'; ctx.fillStyle = col; ctx.fillText('OSNGEO.id', 0, 85);
  ctx.restore();
}
function lowerThird(ctx, t) {
  const p = ap(t, 5.0, 0.5, E.outQuint), q = E.inCubic(prog(t, 10.2, 10.7));
  if (p <= 0 || q >= 1) return;
  const x = 60 - (1 - p) * 120 - q * 120, y = 64;
  ctx.save(); ctx.globalAlpha = p * (1 - q);
  rrect(ctx, x, y, 860, 92, 22); ctx.fillStyle = C.forest; ctx.fill();
  rrect(ctx, x, y, 14, 92, 7); ctx.fillStyle = C.clay; ctx.fill();
  text(ctx, 'Video Konsep OSN Geografi', x + 40, y + 42, fU(34, 700), C.cream);
  text(ctx, 'OSNGEO.id  ·  Bab 1 Iklim  ·  B01-V00', x + 40, y + 76, fU(26, 500), C.forest3);
  ctx.restore();
}
// captions: phrase chunks from timing.json
let CAPS = null;
function buildCaps() {
  CAPS = [];
  for (const u of TM.units) {
    const ws = TM.words.filter((w) => w.u === u.i);
    let chunk = [], len = 0;
    const flush = (end) => { if (chunk.length) CAPS.push({ t0: chunk[0].t, t1: end, s: chunk.map((w) => w.w).join(' ') }); chunk = []; len = 0; };
    ws.forEach((w, k) => {
      chunk.push(w); len += w.w.length + 1;
      const brk = /[,:]$/.test(w.w) && len > 34;
      if ((brk || len > 62) && k < ws.length - 1) flush(ws[k + 1].t - 0.05);
    });
    flush(u.v1 + 0.25);
    // merge a tiny last chunk back into the previous one of this unit
    const n = CAPS.length;
    if (n >= 2 && CAPS[n - 1].s.length < 18 && CAPS[n - 2].t1 >= CAPS[n - 1].t0 - 0.3 && CAPS[n - 2].s.length + CAPS[n - 1].s.length < 90 && TM.words.find((w) => w.t === CAPS[n - 2].t0)?.u === u.i) {
      CAPS[n - 2].s += ' ' + CAPS[n - 1].s; CAPS[n - 2].t1 = CAPS[n - 1].t1; CAPS.pop();
    }
  }
  for (let i = 0; i < CAPS.length - 1; i++) CAPS[i].t1 = Math.min(CAPS[i].t1, CAPS[i + 1].t0 - 0.02);
}
function captions(ctx, t) {
  const c = CAPS.find((c) => t >= c.t0 && t < c.t1);
  if (!c) return;
  const s = c.s.replace(/\bI O D\b/, 'IOD').replace('O S N Geo titik I D', 'OSNGEO.id').replace('El Nino', 'El Niño').replace('La Nina', 'La Niña');
  const f = fU(38, 500); const lines = wrap(ctx, s, f, 1440);
  const lh = 50, h = lines.length * lh + 28, y0 = H - 40 - h;
  let mw = 0; ctx.font = f; lines.forEach((l) => (mw = Math.max(mw, ctx.measureText(l).width)));
  rrect(ctx, W / 2 - mw / 2 - 30, y0, mw + 60, h, 18); ctx.fillStyle = 'rgba(22,41,35,0.84)'; ctx.fill();
  lines.forEach((l, i) => text(ctx, l, W / 2, y0 + 14 + lh * (i + 0.78), f, C.cream, 'center'));
}

// ---------------------------------------------------------------- shared props
function thermometer(ctx, x, y, h, frac, color, label, labelColor = C.ink) {
  // tube
  rrect(ctx, x - 22, y - h, 44, h, 22); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.stroke();
  circle(ctx, x, y + 18, 40); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke();
  circle(ctx, x, y + 18, 28); ctx.fillStyle = color; ctx.fill();
  const fh = (h - 30) * clamp(frac);
  rrect(ctx, x - 11, y - fh - 5, 22, fh + 20, 11); ctx.fillStyle = color; ctx.fill();
  for (let k = 1; k < 6; k++) { ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x + 22, y - (h - 20) * k / 6); ctx.lineTo(x + 36, y - (h - 20) * k / 6); ctx.stroke(); }
  if (label) text(ctx, label, x + 60, y - h * 0.55, fU(78, 700), labelColor);
}
function sun(ctx, x, y, r, t, alpha = 1) {
  ctx.save(); ctx.globalAlpha *= alpha;
  const g = ctx.createRadialGradient(x, y, r * 0.2, x, y, r * 2.3);
  g.addColorStop(0, 'rgba(242,177,58,0.55)'); g.addColorStop(1, 'rgba(242,177,58,0)');
  ctx.fillStyle = g; circle(ctx, x, y, r * 2.3); ctx.fill();
  ctx.strokeStyle = C.amber; ctx.lineWidth = r * 0.12; ctx.lineCap = 'round';
  for (let k = 0; k < 12; k++) {
    const a = k * Math.PI / 6 + t * 0.25;
    ctx.beginPath(); ctx.moveTo(x + Math.cos(a) * r * 1.25, y + Math.sin(a) * r * 1.25); ctx.lineTo(x + Math.cos(a) * r * 1.6, y + Math.sin(a) * r * 1.6); ctx.stroke();
  }
  circle(ctx, x, y, r); ctx.fillStyle = C.amber; ctx.fill();
  ctx.restore();
}
function cloud(ctx, x, y, s, color = '#ffffff', stroke = C.ink) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.beginPath();
  ctx.arc(-38, 10, 30, Math.PI * 0.5, Math.PI * 1.5); ctx.arc(-8, -18, 38, Math.PI, Math.PI * 1.85);
  ctx.arc(34, -2, 30, Math.PI * 1.3, Math.PI * 0.5); ctx.closePath();
  ctx.fillStyle = color; ctx.fill(); ctx.lineWidth = 5 / s; ctx.strokeStyle = stroke; ctx.stroke();
  ctx.restore();
}
function rain(ctx, x, y, w, t, n = 9, color = C.blue, len = 26, speed = 260, alpha = 1) {
  ctx.save(); ctx.globalAlpha *= alpha; ctx.strokeStyle = color; ctx.lineWidth = 5; ctx.lineCap = 'round';
  for (let k = 0; k < n; k++) {
    const px = x - w / 2 + (k + 0.5) * w / n;
    const ph = ((t * speed + hash01(k, 7) * 120) % 120);
    ctx.globalAlpha = alpha * (1 - ph / 120);
    ctx.beginPath(); ctx.moveTo(px - ph * 0.15, y + ph); ctx.lineTo(px - ph * 0.15 - 6, y + ph + len); ctx.stroke();
  }
  ctx.restore();
}

// ================================================================ S0 INTRO
function sIntro(ctx, t) {
  fill(ctx, C.forest);
  // faint graticule
  ctx.save(); ctx.globalAlpha = 0.08; ctx.strokeStyle = C.cream; ctx.lineWidth = 2;
  for (let k = -6; k <= 6; k++) { ctx.beginPath(); ctx.ellipse(W / 2, H / 2, Math.abs(k) * 90 + 1, 520, 0, 0, Math.PI * 2); ctx.stroke(); }
  for (let k = -4; k <= 4; k++) { ctx.beginPath(); ctx.moveTo(0, H / 2 + k * 120); ctx.lineTo(W, H / 2 + k * 120); ctx.stroke(); }
  ctx.restore();
  const k = sp(t, 0.05, SPRING.bouncy), needle = (1 - spring(t - 0.15, { stiffness: 60, damping: 9 })) * Math.PI * 3;
  const s = 230 * k;
  if (s > 2) logo(ctx, 360 - s / 2, H / 2 - s / 2, s, needle);
  const p1 = ap(t, 0.55, 0.6, E.outQuint), p2 = ap(t, 0.8, 0.7, E.outQuint), p3 = ap(t, 1.15, 0.6, E.outQuint);
  const x = 560;
  ctx.save(); ctx.beginPath(); ctx.rect(x - 10, 300, 1300, 480); ctx.clip();
  if (p1 > 0) { ctx.globalAlpha = p1; pill(ctx, 'BAB 1  ·  IKLIM DAN PERUBAHAN IKLIM', x + (1 - p1) * -80, 410, fU(30, 700), C.clay, C.cream); }
  ctx.globalAlpha = 1;
  if (p2 > 0) text(ctx, 'Mesin Iklim Bumi', x, 590 + (1 - p2) * 140, fD(150), C.cream);
  if (p3 > 0) { ctx.globalAlpha = p3; text(ctx, 'Konsep Dasar  ·  2 menit memahami cara kerja iklim', x, 670 + (1 - p3) * 40, fU(36, 500), C.forest3); }
  ctx.restore();
  // exit: slide up under the hook
  const q = E.inCubic(prog(t, 2.6, 3.0));
  if (q > 0) { ctx.fillStyle = C.sand; ctx.fillRect(0, H * (1 - q), W, H * q); }
}

// ================================================================ S1 HOOK
function skyline(ctx, x, y, w, color) {
  ctx.fillStyle = color;
  const bs = [[0, 150], [60, 260], [130, 190], [190, 330], [260, 220], [330, 380], [400, 240], [470, 300], [540, 180], [600, 270], [660, 200], [720, 140]];
  bs.forEach(([bx, bh], i) => { const bw = 58; ctx.fillRect(x + bx * w / 780, y - bh, bw * w / 780, bh); });
}
function person(ctx, x, y, s, jacket) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  circle(ctx, 0, -150, 30); ctx.fillStyle = '#8a5a3c'; ctx.fill();
  rrect(ctx, -46, -116, 92, 120, 30); ctx.fillStyle = jacket; ctx.fill();
  ctx.fillStyle = C.ink; ctx.fillRect(-36, 4, 28, 80); ctx.fillRect(8, 4, 28, 80);
  // scarf
  ctx.fillStyle = C.clay; rrect(ctx, -34, -122, 68, 20, 10); ctx.fill(); ctx.fillRect(14, -110, 16, 46);
  ctx.restore();
}
function sHook(ctx, t) {
  fill(ctx, C.sand);
  const u0 = U_(0), u1 = U_(1), u2 = U_(2), u3 = U_(3), u4 = U_(4);
  const ex = exitP(t, 'hook');
  const L = { x: 80, y: 190, w: 840, h: 540 }, R = { x: 1000, y: 190, w: 840, h: 540 };
  // left: Jakarta
  const pl = sp(t, 3.05, SPRING.gentle);
  if (pl > 0) {
    ctx.save(); ctx.translate(-(1 - pl) * 1000 - ex * 1100, 0);
    ctx.save(); rrect(ctx, L.x, L.y, L.w, L.h, 34); ctx.clip();
    const g = ctx.createLinearGradient(0, L.y, 0, L.y + L.h); g.addColorStop(0, '#f6c48a'); g.addColorStop(1, '#f7e4c8');
    ctx.fillStyle = g; ctx.fillRect(L.x, L.y, L.w, L.h);
    sun(ctx, L.x + 640, L.y + 140, 58, t);
    skyline(ctx, L.x + 20, L.y + L.h - 40, 780, '#c8875f');
    ctx.fillStyle = '#9b5038'; ctx.fillRect(L.x, L.y + L.h - 40, L.w, 40);
    // heat shimmer
    ctx.strokeStyle = 'rgba(224,121,79,0.5)'; ctx.lineWidth = 4;
    for (let k = 0; k < 3; k++) { ctx.beginPath(); for (let i = 0; i <= 40; i++) { const xx = L.x + 120 + i * 9, yy = L.y + 330 - k * 40 + Math.sin(i * 0.6 + t * 4 + k) * 6; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
    ctx.restore();
    text(ctx, 'JAKARTA', L.x + 40, L.y + 76, fU(44, 700), C.ink);
    text(ctx, '±0 m dpl · siang', L.x + 40, L.y + 116, fU(28, 500), C.gray);
    const tv = 32 * ap(t, tw('tiga', 4), 1.2);
    thermometer(ctx, L.x + 110, L.y + L.h - 110, 300, tv / 40, C.clay, tv > 0.5 ? `${Math.round(tv)} °C` : '');
    ctx.restore();
  }
  // right: Puncak
  const pr = sp(t, u1.v0, SPRING.gentle);
  if (pr > 0) {
    ctx.save(); ctx.translate((1 - pr) * 1000 + ex * 1100, 0);
    ctx.save(); rrect(ctx, R.x, R.y, R.w, R.h, 34); ctx.clip();
    const g = ctx.createLinearGradient(0, R.y, 0, R.y + R.h); g.addColorStop(0, '#cfe3e8'); g.addColorStop(1, '#e8f0ea');
    ctx.fillStyle = g; ctx.fillRect(R.x, R.y, R.w, R.h);
    ctx.fillStyle = '#9cc3a2'; ctx.beginPath(); ctx.moveTo(R.x, R.y + 330); ctx.quadraticCurveTo(R.x + 300, R.y + 190, R.x + 560, R.y + 300); ctx.quadraticCurveTo(R.x + 720, R.y + 360, R.x + R.w, R.y + 260); ctx.lineTo(R.x + R.w, R.y + R.h); ctx.lineTo(R.x, R.y + R.h); ctx.fill();
    ctx.strokeStyle = '#5e9a6c'; ctx.lineWidth = 6;
    for (let k = 0; k < 7; k++) { ctx.beginPath(); for (let i = 0; i <= 60; i++) { const xx = R.x + i * 14, yy = R.y + 360 + k * 30 + Math.sin(i * 0.25 + k) * 10; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
    // mist
    for (let k = 0; k < 3; k++) { ctx.fillStyle = 'rgba(255,255,255,0.45)'; ctx.beginPath(); ctx.ellipse(R.x + 200 + k * 260 + Math.sin(t * 0.4 + k) * 40, R.y + 300 + k * 20, 220, 34, 0, 0, Math.PI * 2); ctx.fill(); }
    ctx.restore();
    text(ctx, 'PUNCAK', R.x + 40, R.y + 76, fU(44, 700), C.ink);
    text(ctx, '±1.500 m dpl · saat yang sama', R.x + 40, R.y + 116, fU(28, 500), C.gray);
    person(ctx, R.x + 640, R.y + R.h - 70, 1.2, C.forest);
    thermometer(ctx, R.x + 110, R.y + R.h - 110, 300, 0.42 * ap(t, tw('jaket', 6), 0.8), C.cold, ap(t, tw('jaket', 6), 0.4) > 0.5 ? '? °C' : '', C.cold);
    ctx.restore();
  }
  // distance + profile strip
  const pd = ap(t, u2.v0, 0.8, E.inOutCubic);
  if (pd > 0 && ex < 1) {
    ctx.save(); ctx.globalAlpha = 1 - ex;
    const y = 800, x0 = 200, x1 = 1720;
    ctx.fillStyle = C.sand2; ctx.beginPath(); ctx.moveTo(x0, y + 60);
    for (let i = 0; i <= 100; i++) { const f = i / 100; if (f > pd) break; ctx.lineTo(lerp(x0, x1, f), y + 60 - 90 * E.inOutCubic(clamp((f - 0.35) / 0.6))); }
    ctx.lineTo(lerp(x0, x1, pd), y + 62); ctx.closePath(); ctx.fill();
    ctx.setLineDash([16, 14]); ctx.strokeStyle = C.forest; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(x0, y - 10); ctx.lineTo(lerp(x0, x1, pd), y - 10); ctx.stroke(); ctx.setLineDash([]);
    circle(ctx, x0, y - 10, 12); ctx.fillStyle = C.clay; ctx.fill();
    if (pd > 0.98) { circle(ctx, x1, y - 10, 12); ctx.fillStyle = C.cold; ctx.fill(); }
    const pk = ap(t, tw('seratus', u2.v0), 0.4);
    if (pk > 0) pill(ctx, 'kurang dari 100 km', W / 2, y - 12, fU(32, 700), C.forest, C.cream, 26, 60, 'center');
    ctx.restore();
  }
  // "Kenapa?" stamp
  const pq = sp(t, u3.v0, SPRING.bouncy);
  if (pq > 0 && t < u4.v0 + 0.3) {
    const q2 = 1 - ap(t, u4.v0, 0.3);
    ctx.save(); ctx.globalAlpha = q2; ctx.translate(W / 2, 470); ctx.scale(pq, pq); ctx.rotate(-0.06);
    card(ctx, -230, -95, 460, 170, { r: 40, bg: C.clay });
    text(ctx, 'Kenapa?', 0, 35, fD(120), C.cream, 'center'); ctx.restore();
  }
  // title: mesin iklim bumi
  const pm = sp(t, tw('mesin', u4.v0), SPRING.gentle);
  if (pm > 0) {
    ctx.save(); ctx.globalAlpha = 1 - ex; ctx.translate(W / 2, 470); ctx.scale(0.8 + 0.2 * pm, 0.8 + 0.2 * pm);
    card(ctx, -470, -110, 940, 200, { r: 40, bg: C.forest });
    // gear
    const gx = -350, gy = -10;
    ctx.save(); ctx.translate(gx, gy); ctx.rotate(t * 1.2); ctx.fillStyle = C.amber;
    for (let k = 0; k < 8; k++) { ctx.save(); ctx.rotate(k * Math.PI / 4); ctx.fillRect(-12, -62, 24, 24); ctx.restore(); }
    circle(ctx, 0, 0, 46); ctx.fill(); circle(ctx, 0, 0, 18); ctx.fillStyle = C.forest; ctx.fill(); ctx.restore();
    text(ctx, 'Mesin Iklim Bumi', 60, 30, fD(104), C.cream, 'center');
    ctx.restore();
  }
  if (t < 3.6) { ctx.fillStyle = C.sand; }
}
hit(3.1, 'jakarta panel', 'whoosh', { len: 0.45, from: 500, to: 2200, gain: 0.35 });
// filled at init (need timing): see addTimedHits()

// ================================================================ S2 CUACA vs IKLIM
const RAIN_MEAN = [300, 280, 230, 160, 110, 80, 60, 55, 80, 140, 210, 270];
function sCuaca(ctx, t) {
  fill(ctx, C.sand);
  const [a, b] = SC.cuaca; const ex = exitP(t, 'cuaca');
  const u5 = U_(5), u6 = U_(6), u7 = U_(7), u8 = U_(8), u9 = U_(9), u10 = U_(10);
  const LX = 110, RX = 990, Y = 130, CW = 820, CH = 560;
  const pl = sp(t, tw('cuaca', u5.v0), SPRING.snappy), pr = sp(t, tw('iklim', u5.v0), SPRING.snappy);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  if (pl > 0) {
    ctx.save(); ctx.translate(0, (1 - pl) * 80); ctx.globalAlpha *= clamp(pl * 2);
    card(ctx, LX, Y, CW, CH);
    rrect(ctx, LX, Y, CW, 110, 28); ctx.fillStyle = C.forest1; ctx.fill(); ctx.fillRect(LX, Y + 60, CW, 50);
    text(ctx, 'CUACA', LX + 44, Y + 76, fU(54, 700), C.forest);
    const pc = ap(t, u6.v0, 0.5);
    if (pc > 0) {
      ctx.save(); ctx.globalAlpha *= pc;
      // Bogor scene: cloud + rain + clock
      cloud(ctx, LX + 300, Y + 260, 1.7, '#e6ebef');
      rain(ctx, LX + 300, Y + 300, 200, t, 9, C.blue, 30, 300, ap(t, u7.v0, 0.4));
      ctx.fillStyle = C.forestL; ctx.fillRect(LX + 120, Y + 430, 360, 10);
      text(ctx, 'Bogor', LX + 300, Y + 485, fU(36, 700), C.ink, 'center');
      // clock
      const cx = LX + 640, cy = Y + 280;
      circle(ctx, cx, cy, 90); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke();
      const ang = -Math.PI / 2 + (16 / 12) * Math.PI * 2 + t * 0.6;
      ctx.lineCap = 'round'; ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(-Math.PI / 2 + 4 / 12 * Math.PI * 2) * 48, cy + Math.sin(-Math.PI / 2 + 4 / 12 * Math.PI * 2) * 48); ctx.stroke();
      ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(ang) * 70, cy + Math.sin(ang) * 70); ctx.stroke();
      text(ctx, 'sore ini', cx, cy + 140, fU(32, 500), C.gray, 'center');
      ctx.restore();
    }
    const pt = ap(t, tw('sempit', u6.v0), 0.4);
    if (pt > 0) { ctx.globalAlpha *= pt; pill(ctx, 'saat tertentu  ·  wilayah sempit', LX + CW / 2, Y + CH - 46, fU(30, 700), C.clay, C.cream, 24, 58, 'center'); }
    ctx.restore();
  }
  if (pr > 0) {
    ctx.save(); ctx.translate(0, (1 - pr) * 80); ctx.globalAlpha *= clamp(pr * 2);
    card(ctx, RX, Y, CW, CH);
    rrect(ctx, RX, Y, CW, 110, 28); ctx.fillStyle = C.forest; ctx.fill(); ctx.fillRect(RX, Y + 60, CW, 50);
    text(ctx, 'IKLIM', RX + 44, Y + 76, fU(54, 700), C.cream);
    const pg = ap(t, u8.v0, 0.4);
    if (pg > 0) {
      const gx = RX + 90, gy = Y + 440, gw = 640, gh = 260;
      ctx.save(); ctx.globalAlpha *= pg;
      ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
      ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'].forEach((m, i) => text(ctx, m, gx + (i + 0.5) * gw / 12, gy + 34, fU(24, 500), C.gray, 'center'));
      // 30 thin year lines appear (u9), then the mean
      const ny = Math.floor(30 * ap(t, tw('tiga', u9.v0), 2.2, E.linear));
      for (let yv = 0; yv < ny; yv++) {
        ctx.strokeStyle = 'rgba(57,105,87,0.22)'; ctx.lineWidth = 2; ctx.beginPath();
        RAIN_MEAN.forEach((v, i) => { const vv = v * (0.65 + 0.7 * hash01(yv * 12 + i, 3)); const x = gx + (i + 0.5) * gw / 12, y = gy - vv / 380 * gh; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
      }
      const pm = ap(t, u8.v0 + 0.3, 1.6, E.inOutCubic);
      ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.lineJoin = 'round'; ctx.beginPath();
      RAIN_MEAN.forEach((v, i) => { if (i / 11 > pm) return; const x = gx + (i + 0.5) * gw / 12, y = gy - v / 380 * gh; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke();
      text(ctx, 'rata-rata curah hujan bulanan', gx, gy - gh - 20, fU(26, 500), C.gray);
      if (ny > 0) text(ctx, `${1990 + ny}`, gx + gw, gy - gh - 20, fU(30, 700), C.forestL, 'right');
      ctx.restore();
    }
    const pb = sp(t, tw('tiga', u9.v0) + 2.2, SPRING.bouncy);
    if (pb > 0) { ctx.save(); ctx.translate(RX + CW - 150, Y + 190); ctx.scale(pb, pb); circle(ctx, 0, 0, 92); ctx.fillStyle = C.amber; ctx.fill(); text(ctx, '30', 0, 14, fU(66, 700), C.ink, 'center'); text(ctx, 'tahun (WMO)', 0, 52, fU(20, 700), C.ink, 'center'); ctx.restore(); }
    const pt = ap(t, tw('luas', u8.v0), 0.4);
    if (pt > 0) { ctx.globalAlpha *= pt; pill(ctx, 'rata-rata jangka panjang  ·  wilayah luas', RX + CW / 2, Y + CH - 46, fU(30, 700), C.forest, C.cream, 24, 58, 'center'); }
    ctx.restore();
  }
  // scale arrows
  const ps = ap(t, tw('skala', u10.v0), 0.5), pw = ap(t, tw('waktu', u10.v0), 0.5);
  [[ps, 'Skala ruang', 'sempit', 'luas', 742], [pw, 'Skala waktu', 'saat ini', 'minimal 30 tahun', 812]].forEach(([p, lab, l, r, y]) => {
    if (p <= 0) return;
    ctx.save(); ctx.globalAlpha *= p;
    text(ctx, lab, 110, y + 12, fU(34, 700), C.forest);
    const x0 = 400, x1 = lerp(400, 1810, p);
    text(ctx, l, x0, y + 12, fU(30, 500), C.ink);
    ctx.strokeStyle = C.clay; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x0 + 170, y); ctx.lineTo(x1 - 330, y); ctx.stroke();
    arrowLine(ctx, x1 - 340, y, x1 - 310, y, C.clay, 6, 26);
    text(ctx, r, x1, y + 12, fU(30, 700), C.ink, 'right');
    ctx.restore();
  });
  ctx.restore();
}

// ================================================================ S3 UNSUR
const UNSUR = [
  ['suhu', 'Suhu', 'termometer'], ['tekanan', 'Tekanan udara', 'barometer'], ['angin', 'Angin', 'anemometer'],
  ['kelembapan', 'Kelembapan', 'higrometer'], ['awan', 'Awan', 'pengamatan'], ['curah', 'Curah hujan', 'penakar hujan'],
  ['penyinaran', 'Penyinaran matahari', 'Campbell-Stokes'],
];
function icon(ctx, kind, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.lineWidth = 6; ctx.strokeStyle = C.ink; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (kind === 0) { rrect(ctx, -12, -60, 24, 90, 12); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); circle(ctx, 0, 40, 22); ctx.fillStyle = C.clay; ctx.fill(); ctx.stroke(); ctx.fillRect(-5, -30, 10, 60); }
  if (kind === 1) { circle(ctx, 0, 0, 56); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); const a = -2.4 + 0.3 * Math.sin(t); ctx.strokeStyle = C.clay; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * 42, Math.sin(a) * 42); ctx.stroke(); ctx.strokeStyle = C.ink; for (let k = 0; k < 7; k++) { const b = Math.PI * (0.8 + k * 0.233); ctx.beginPath(); ctx.moveTo(Math.cos(b) * 44, Math.sin(b) * 44); ctx.lineTo(Math.cos(b) * 54, Math.sin(b) * 54); ctx.stroke(); } }
  if (kind === 2) { ctx.beginPath(); ctx.moveTo(0, 60); ctx.lineTo(0, -10); ctx.stroke(); const r = t * 5; for (let k = 0; k < 3; k++) { const a = r + k * 2.09; const cx = Math.cos(a) * 46, cy = -10 + Math.sin(a) * 14; ctx.beginPath(); ctx.moveTo(0, -10); ctx.lineTo(cx, cy); ctx.stroke(); circle(ctx, cx, cy, 14); ctx.fillStyle = C.clay; ctx.fill(); ctx.stroke(); } }
  if (kind === 3) { ctx.beginPath(); ctx.moveTo(0, -60); ctx.bezierCurveTo(40, -10, 46, 20, 0, 50); ctx.bezierCurveTo(-46, 20, -40, -10, 0, -60); ctx.fillStyle = '#bfe0f3'; ctx.fill(); ctx.stroke(); text(ctx, '%', 0, 30, fU(40, 700), C.blue, 'center'); }
  if (kind === 4) { ctx.restore(); cloud(ctx, x, y, s * 1.0, '#ffffff'); return; }
  if (kind === 5) { ctx.beginPath(); ctx.moveTo(-34, -50); ctx.lineTo(34, -50); ctx.lineTo(26, 56); ctx.lineTo(-26, 56); ctx.closePath(); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); const lv = 20 + 16 * Math.sin(t * 0.8); ctx.fillStyle = '#9fd0ee'; ctx.fillRect(-25, 50 - lv, 50, lv); for (let k = 0; k < 3; k++) { const ph = (t * 90 + k * 30) % 80; ctx.strokeStyle = C.blue; ctx.beginPath(); ctx.moveTo(-14 + k * 14, -110 + ph); ctx.lineTo(-16 + k * 14, -96 + ph); ctx.stroke(); } }
  if (kind === 6) { ctx.restore(); sun(ctx, x, y, 34 * s, t); return; }
  ctx.restore();
}
function sUnsur(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'unsur');
  const u11 = U_(11), u12 = U_(12), u13 = U_(13);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const ph = ap(t, u11.v0, 0.5, E.outQuint);
  riseText(ctx, 'Unsur cuaca = unsur iklim', 110, 210, fD(96), C.forest, ph);
  riseText(ctx, 'yang diukur, bukan yang mengendalikan', 112, 262, fU(32, 500), C.gray, ap(t, u11.v0 + 0.3, 0.5));
  UNSUR.forEach(([w, lab, tool], i) => {
    const t0 = tw(w, u12.v0) - 0.1; const k = sp(t, t0, SPRING.bouncy);
    if (k <= 0) return;
    const col = i % 4, row = Math.floor(i / 4);
    const cw = 400, chh = 280, x = 110 + col * (cw + 30) + (row ? (cw + 30) / 2 : 0), y = 340 + row * (chh + 34);
    ctx.save(); ctx.translate(x + cw / 2, y + chh / 2); ctx.scale(0.6 + 0.4 * k, 0.6 + 0.4 * k); ctx.translate(-(x + cw / 2), -(y + chh / 2)); ctx.globalAlpha *= clamp(k * 1.5);
    card(ctx, x, y, cw, chh, { r: 26 });
    icon(ctx, i, x + 100, y + 135, 1.05, t);
    { let fs = 36; ctx.font = fU(fs, 700); while (ctx.measureText(lab).width > 196 && fs > 22) { fs -= 1; ctx.font = fU(fs, 700); } if (ctx.measureText(lab).width > 196) { const [l1, ...l2] = lab.split(' '); text(ctx, l1, x + 190, y + 104, fU(32, 700), C.ink); text(ctx, l2.join(' '), x + 190, y + 140, fU(32, 700), C.ink); } else text(ctx, lab, x + 190, y + 124, fU(fs, 700), C.ink); }
    text(ctx, tool, x + 190, y + 182, fU(24, 500), C.gray);
    ctx.restore();
  });
  const ps = ap(t, tw('stasiun', u13.v0), 0.5);
  if (ps > 0) { ctx.globalAlpha *= ps; pill(ctx, 'Diukur setiap hari di stasiun cuaca (BMKG)', W - 110, 210 - 25, fU(30, 700), C.forest, C.cream, 26, 60, 'right'); }
  ctx.restore();
}

// ================================================================ S4 MATAHARI
function sMatahari(ctx, t) {
  fill(ctx, '#f3ead9'); const ex = exitP(t, 'matahari');
  const u14 = U_(14), u15 = U_(15), u16 = U_(16), u17 = U_(17);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const ex0 = 1220, ey = 560, R = 320;
  const ps = sp(t, tw('matahari', u14.v0) - 0.6, SPRING.gentle);
  sun(ctx, lerp(-200, 170, ps), ey, 110, t);
  riseText(ctx, 'Satu sumber energi', 110, 160, fD(80), C.forest, ap(t, u14.v0, 0.5, E.outQuint));
  // earth
  const pe = sp(t, u14.v0 + 0.4, SPRING.gentle);
  if (pe > 0) {
    ctx.save(); ctx.translate(ex0, ey); ctx.scale(pe, pe);
    const heat = ap(t, u17.v0, 1.2);
    const g = ctx.createLinearGradient(0, -R, 0, R);
    const warm = (a) => `rgba(224,121,79,${a})`, cool = (a) => `rgba(74,144,194,${a})`;
    g.addColorStop(0, M.mix('#9cc3a2', '#7fb1d6', heat)); g.addColorStop(0.5, M.mix('#9cc3a2', '#e9a072', heat)); g.addColorStop(1, M.mix('#9cc3a2', '#7fb1d6', heat));
    circle(ctx, 0, 0, R); ctx.fillStyle = g; ctx.fill(); ctx.lineWidth = 6; ctx.strokeStyle = C.ink; ctx.stroke();
    // latitude lines
    ctx.setLineDash([10, 10]); ctx.lineWidth = 2.5; ctx.strokeStyle = 'rgba(27,50,43,0.5)';
    [0, 30, 60, -30, -60].forEach((lat) => { const yy = -R * Math.sin(lat * Math.PI / 180), xx = R * Math.cos(lat * Math.PI / 180); ctx.beginPath(); ctx.moveTo(-xx, yy); ctx.lineTo(xx, yy); ctx.stroke(); });
    ctx.setLineDash([]);
    text(ctx, 'khatulistiwa', R * 0.15, -12, fU(26, 700), C.ink); text(ctx, '60° LU', R * 0.18, -R * Math.sin(Math.PI / 3) + 34, fU(24, 700), C.ink);
    ctx.restore();
  }
  // beams: equal width bundles from left hitting equator and 60N
  const pb = ap(t, tw('sinar', u15.v0), 1.2, E.inOutCubic);
  const bw = 76;
  const beam = (latDeg, col, p, label) => {
    if (p <= 0) return;
    const yc = ey - R * Math.sin(latDeg * Math.PI / 180);
    const y0 = yc - bw / 2, y1 = yc + bw / 2;
    const hitX = (yy) => ex0 - Math.sqrt(Math.max(0, R * R - (yy - ey) ** 2));
    const xs = 330;
    ctx.save(); ctx.globalAlpha *= 0.85;
    ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(xs, y0); ctx.lineTo(lerp(xs, hitX(y0), p), y0); ctx.lineTo(lerp(xs, hitX(y1), p), y1); ctx.lineTo(xs, y1); ctx.closePath(); ctx.fill();
    ctx.restore();
    if (p >= 1) {
      // footprint arc
      const a0 = Math.asin((y0 - ey) / R), a1 = Math.asin((y1 - ey) / R);
      ctx.strokeStyle = latDeg === 0 ? C.clay : C.cold; ctx.lineWidth = 16; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.arc(ex0, ey, R, Math.PI - a0, Math.PI - a1, true); ctx.stroke();
      if (label) text(ctx, label, ex0 - R - 30, yc + (latDeg ? -78 : 92), fU(30, 700), latDeg === 0 ? C.clayD : C.blue, 'right');
    }
  };
  beam(0, 'rgba(242,177,58,0.55)', pb, ap(t, tw('tegak', u15.v0), 0.3) > 0.5 ? 'jatuh tegak' : '');
  beam(60, 'rgba(242,177,58,0.55)', ap(t, tw('miring', u15.v0) - 0.5, 1.0, E.inOutCubic), ap(t, tw('miring', u15.v0), 0.3) > 0.5 ? 'jatuh miring' : '');
  // comparison panel (u16)
  const pc = sp(t, u16.v0 + 0.2, SPRING.snappy);
  if (pc > 0 && t < u17.v0 + 0.5) {
    const q = 1 - ap(t, u17.v0, 0.5);
    ctx.save(); ctx.globalAlpha *= q; ctx.translate(0, (1 - pc) * 60);
    card(ctx, 110, 700, 760, 230, { r: 26 });
    text(ctx, 'Energi sama, area berbeda', 150, 755, fU(34, 700), C.ink);
    rrect(ctx, 150, 785, 150, 46, 10); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, '1×', 320, 822, fU(34, 700), C.clayD); text(ctx, 'khatulistiwa: panas', 380, 822, fU(30, 500), C.ink);
    rrect(ctx, 150, 855, 300 * ap(t, tw('luas', u16.v0), 0.6), 46, 10); ctx.fillStyle = C.cold; ctx.fill(); text(ctx, '2×', 470, 892, fU(34, 700), C.blue); text(ctx, 'lintang 60°: lebih dingin', 530, 892, fU(30, 500), C.ink);
    ctx.restore();
  }
  // u17 headline
  const ph = sp(t, tw('tidak', u17.v0), SPRING.gentle);
  if (ph > 0) {
    ctx.save(); ctx.translate(110, 720 + (1 - ph) * 60); ctx.globalAlpha *= clamp(ph * 1.5);
    card(ctx, 0, 0, 760, 190, { r: 28, bg: C.forest });
    text(ctx, 'Pemanasan tidak merata', 40, 80, fD(64), C.cream);
    text(ctx, 'menyalakan mesin iklim', 40, 140, fU(34, 700), C.amber);
    ctx.save(); ctx.translate(680, 95); ctx.rotate(t * 1.4); ctx.fillStyle = C.amber;
    for (let k = 0; k < 8; k++) { ctx.save(); ctx.rotate(k * Math.PI / 4); ctx.fillRect(-9, -46, 18, 18); ctx.restore(); }
    circle(ctx, 0, 0, 34); ctx.fill(); circle(ctx, 0, 0, 13); ctx.fillStyle = C.forest; ctx.fill(); ctx.restore();
    ctx.restore();
  }
  ctx.restore();
}

// ================================================================ S5 DOMINO
const CHAIN = [['suhu', 'Suhu', C.clay], ['tekanan', 'Tekanan', C.amber], ['angin', 'Angin', C.forestL], ['uap', 'Uap air', '#6fb1d8'], ['awan', 'Awan', '#9aa9b5'], ['hujan', 'Hujan', C.blue]];
function sDomino(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'domino');
  const u18 = U_(18), u19 = U_(19), u20 = U_(20), u21 = U_(21), u22 = U_(22), u23 = U_(23), u24 = U_(24);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  riseText(ctx, 'Efek domino unsur iklim', 110, 170, fD(84), C.forest, ap(t, u18.v0, 0.5, E.outQuint));
  const times = [tw('suhu', u19.v0), tw('tekanan', u19.v0), tw('angin', u21.v0), tw('uap', u22.v0), tw('awan', u23.v0), tw('hujan', u23.v0)];
  const wob = Math.max(0, wobble(t - tw('berubah', u24.v0), 2.2, 3));
  const cw = 250, gap = 34, x0 = (W - (6 * cw + 5 * gap)) / 2, y = 660;
  CHAIN.forEach(([w, lab, col], i) => {
    const k = sp(t, times[i] - 0.15, SPRING.bouncy); if (k <= 0) return;
    const x = x0 + i * (cw + gap);
    // domino tips in from upright rotation
    ctx.save(); ctx.translate(x + cw / 2, y + 150); ctx.rotate((1 - k) * -0.9 + wob * 0.08 * (i % 2 ? 1 : -1)); ctx.translate(-(x + cw / 2), -(y + 150));
    card(ctx, x, y, cw, 150, { r: 24 });
    rrect(ctx, x, y, cw, 18, 9); ctx.fillStyle = col; ctx.fill();
    text(ctx, `${i + 1}`, x + 26, y + 70, fU(30, 700), C.gray);
    text(ctx, lab, x + cw / 2, y + 104, fU(lab.length > 6 ? 40 : 44, 700), C.ink, 'center');
    ctx.restore();
    if (i < 5) { const pa = ap(t, times[i + 1] - 0.15, 0.35); if (pa > 0) arrowLine(ctx, x + cw + 4, y + 75, x + cw + 4 + (gap - 8) * pa, y + 75, C.clay, 5, 16); }
  });
  // process diagram above
  const dy = 300, dh = 300;
  const pd = ap(t, u19.v0, 0.5);
  if (pd > 0) {
    ctx.save(); ctx.globalAlpha *= pd;
    rrect(ctx, 110, dy, W - 220, dh, 26); ctx.fillStyle = '#eef3ee'; ctx.fill();
    // ground: hot left, cool right
    const g = ctx.createLinearGradient(110, 0, W - 110, 0); g.addColorStop(0, '#e9a072'); g.addColorStop(1, '#9cc3d6');
    ctx.fillStyle = g; ctx.fillRect(110, dy + dh - 40, W - 220, 40);
    const pT = ap(t, tw('tekanan', u19.v0), 0.5);
    if (pT > 0) {
      ctx.globalAlpha = pd * pT;
      text(ctx, 'L', 470, dy + 140, fU(110, 700), C.clay, 'center'); text(ctx, 'panas · tekanan rendah', 470, dy + 200, fU(26, 700), C.clayD, 'center');
      text(ctx, 'H', W - 470, dy + 140, fU(110, 700), C.blue, 'center'); text(ctx, 'dingin · tekanan tinggi', W - 470, dy + 200, fU(26, 700), C.blue, 'center');
      ctx.globalAlpha = pd;
    }
    const pW = ap(t, u20.v0, 1.4, E.inOutCubic);
    if (pW > 0) {
      for (let k = 0; k < 3; k++) { const yy = dy + dh - 70 - k * 16; const xx1 = lerp(W - 600, 620, pW); arrowLine(ctx, W - 560, yy, xx1 + k * 40, yy, C.forestL, 6, 20); }
      if (ap(t, tw('angin', u21.v0), 0.3) > 0) text(ctx, 'angin', W / 2, dy + dh - 96, fU(32, 700), C.forestL, 'center');
    }
    const pV = ap(t, tw('uap', u22.v0), 1.0);
    if (pV > 0) {
      ctx.strokeStyle = '#6fb1d8'; ctx.lineWidth = 5; ctx.setLineDash([4, 12]);
      for (let k = 0; k < 4; k++) { const xx = 420 + k * 40; const ph = (t * 50 + k * 30) % 110; ctx.beginPath(); ctx.moveTo(xx, dy + dh - 50 - ph * pV); ctx.lineTo(xx + 6, dy + dh - 90 - ph * pV); ctx.stroke(); }
      ctx.setLineDash([]);
    }
    const pC = sp(t, tw('awan', u23.v0), SPRING.bouncy);
    if (pC > 0) cloud(ctx, 480, dy + 80, 0.9 * pC, '#ffffff');
    const pR = ap(t, tw('hujan', u23.v0) - 0.1, 0.4);
    if (pR > 0) rain(ctx, 480, dy + 110, 140, t, 6, C.blue, 24, 220, pR);
    ctx.restore();
  }
  const pz = ap(t, tw('berubah', u24.v0) - 0.3, 0.4);
  if (pz > 0) { ctx.globalAlpha *= pz; pill(ctx, 'Satu unsur berubah, yang lain ikut berubah', W / 2, 890, fU(34, 700), C.forest, C.cream, 30, 64, 'center'); }
  ctx.restore();
}

// ================================================================ S6 PENGENDALI
const MAP = { x: 90, y: 200, w: 1130, h: 447, ext: [94, 142, -11.5, 7.5] };
const PX = (lon) => MAP.x + (lon - MAP.ext[0]) / (MAP.ext[1] - MAP.ext[0]) * MAP.w;
const PY = (lat) => MAP.y + (MAP.ext[3] - lat) / (MAP.ext[3] - MAP.ext[2]) * MAP.h;
function drawMap(ctx) {
  ctx.save(); rrect(ctx, MAP.x, MAP.y, MAP.w, MAP.h, 24); ctx.clip();
  ctx.fillStyle = C.sea; ctx.fillRect(MAP.x, MAP.y, MAP.w, MAP.h);
  for (const [c, rings] of Object.entries(IND)) {
    ctx.fillStyle = c === 'IDN' ? C.land : '#e7e3da'; ctx.strokeStyle = c === 'IDN' ? '#a8916a' : '#c9c2b4'; ctx.lineWidth = 1.2;
    for (const r of rings) { ctx.beginPath(); r.forEach(([lo, la], i) => (i ? ctx.lineTo(PX(lo), PY(la)) : ctx.moveTo(PX(lo), PY(la)))); ctx.closePath(); ctx.fill(); ctx.stroke(); }
  }
  ctx.restore();
}
const KENDALI = [['lintang', 'Lintang'], ['ketinggian', 'Ketinggian tempat'], ['sebaran', 'Sebaran darat dan laut'], ['arus', 'Arus laut'], ['relief', 'Relief'], ['sirkulasi', 'Sirkulasi atmosfer']];
function sKendali(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'kendali');
  const u25 = U_(25), u26 = U_(26), u27 = U_(27), u28 = U_(28);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const card2 = ap(t, u28.v0 - 0.2, 0.5, E.inOutCubic); // shift to unsur vs pengendali card
  riseText(ctx, 'Kenapa iklim tiap tempat berbeda?', 90, 165, fD(76), C.forest, ap(t, u25.v0, 0.5, E.outQuint));
  const pm = sp(t, u25.v0 + 0.3, SPRING.gentle);
  const T = KENDALI.map(([w]) => tw(w, u27.v0));
  if (pm > 0 && card2 < 1) {
    ctx.save(); ctx.globalAlpha *= clamp(pm * 1.5) * (1 - card2); ctx.translate(0, (1 - pm) * 50);
    drawMap(ctx);
    ctx.save(); rrect(ctx, MAP.x, MAP.y, MAP.w, MAP.h, 24); ctx.clip();
    const act = (i) => ap(t, T[i] - 0.1, 0.4);
    // 3 darat-laut: pulse sea
    if (act(2) > 0) { ctx.globalAlpha = 0.35 * act(2) * (0.6 + 0.4 * Math.sin(t * 4)); ctx.fillStyle = C.blue; ctx.fillRect(MAP.x, MAP.y, MAP.w, MAP.h); ctx.globalAlpha = 1; drawLand(ctx, act(2)); }
    // 1 lintang
    if (act(0) > 0) { ctx.globalAlpha = act(0); ctx.strokeStyle = C.clay; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(MAP.x, PY(0)); ctx.lineTo(MAP.x + MAP.w * act(0), PY(0)); ctx.stroke(); ctx.setLineDash([8, 8]); ctx.lineWidth = 2; [-10, -5, 5].forEach((la) => { ctx.beginPath(); ctx.moveTo(MAP.x, PY(la)); ctx.lineTo(MAP.x + MAP.w, PY(la)); ctx.stroke(); }); ctx.setLineDash([]); text(ctx, '0°  khatulistiwa', PX(129.5), PY(0) - 12, fU(24, 700), C.clayD); ctx.globalAlpha = 1; }
    // 2 ketinggian: Puncak + Jayawijaya
    if (act(1) > 0) { ctx.globalAlpha = act(1); [[106.98, -6.7, 'Puncak'], [137.2, -4.08, 'Jayawijaya']].forEach(([lo, la, n]) => { const x = PX(lo), y = PY(la); poly(ctx, [[x, y - 40], [x - 30, y + 6], [x + 30, y + 6]]); ctx.fillStyle = C.forestL; ctx.fill(); poly(ctx, [[x, y - 40], [x - 10, y - 25], [x + 10, y - 25]]); ctx.fillStyle = '#fff'; ctx.fill(); text(ctx, n, x, y + 34, fU(22, 700), C.ink, 'center'); }); ctx.globalAlpha = 1; }
    // 4 arus laut: ARLINDO arrows
    if (act(3) > 0) { ctx.globalAlpha = act(3); [[[128, 5], [125.5, 1], [119.5, -2.5], [117.5, -7.5], [116, -10]], [[130, -1], [128.5, -4.5], [125.5, -8.5], [122, -10.5]]].forEach((pts) => { ctx.strokeStyle = C.blue; ctx.lineWidth = 6; ctx.setLineDash([14, 10]); ctx.lineDashOffset = -t * 40; ctx.beginPath(); pts.forEach(([lo, la], i) => (i ? ctx.lineTo(PX(lo), PY(la)) : ctx.moveTo(PX(lo), PY(la)))); ctx.stroke(); ctx.setLineDash([]); const n = pts.length; arrowLine(ctx, PX(pts[n - 2][0]), PY(pts[n - 2][1]), PX(pts[n - 1][0]), PY(pts[n - 1][1]), C.blue, 6, 22); }); text(ctx, 'Arlindo', PX(121), PY(1.5), fU(24, 700), C.blue, 'center'); ctx.globalAlpha = 1; }
    // 5 relief: Bukit Barisan ridge
    if (act(4) > 0) { ctx.globalAlpha = act(4); ctx.strokeStyle = '#8a6a3a'; ctx.lineWidth = 3; for (let k = 0; k < 14; k++) { const f = k / 13; const lo = lerp(95.6, 105.2, f), la = lerp(5.0, -5.4, f); const x = PX(lo), y = PY(la); ctx.beginPath(); ctx.moveTo(x - 12, y + 8); ctx.lineTo(x, y - 12); ctx.lineTo(x + 12, y + 8); ctx.stroke(); } text(ctx, 'Bukit Barisan', PX(97.3), PY(-1.8), fU(22, 700), '#6b4d22'); ctx.globalAlpha = 1; }
    // 6 sirkulasi: monsoon arrows
    if (act(5) > 0) { ctx.globalAlpha = act(5); for (let k = 0; k < 3; k++) { const x0 = PX(110 + k * 9), y0 = PY(-11.3); const xx = PX(104 + k * 9), yy = PY(-2 + Math.sin(t + k)); arrowLine(ctx, x0, y0, lerp(x0, xx, act(5)), lerp(y0, yy, act(5)), C.clay, 7, 26); } text(ctx, 'monsun', PX(124), PY(-9.8), fU(24, 700), C.clayD, 'center'); ctx.globalAlpha = 1; }
    ctx.restore();
    ctx.restore();
  }
  // right list
  const ph = ap(t, tw('pengendali', u26.v0), 0.4);
  if (ph > 0 && card2 < 1) {
    ctx.save(); ctx.globalAlpha *= ph * (1 - card2);
    pill(ctx, 'PENGENDALI IKLIM', 1290, 230, fU(32, 700), C.clay, C.cream, 26, 62);
    KENDALI.forEach(([w, lab], i) => {
      const k = sp(t, T[i] - 0.1, SPRING.snappy); if (k <= 0) return;
      const y = 300 + i * 74;
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); ctx.translate((1 - k) * 60, 0);
      circle(ctx, 1312, y + 24, 22); ctx.fillStyle = C.forest; ctx.fill(); text(ctx, `${i + 1}`, 1312, y + 35, fU(28, 700), C.cream, 'center');
      text(ctx, lab, 1352, y + 36, fU(36, 700), C.ink);
      ctx.restore();
    });
    ctx.restore();
  }
  // unsur vs pengendali sorting card
  if (card2 > 0) {
    ctx.save(); ctx.globalAlpha *= card2;
    const colY = 200, lx = 200, rx = 1000, cw2 = 720, ch2 = 520;
    card(ctx, lx, colY, cw2, ch2, { r: 30 }); card(ctx, rx, colY, cw2, ch2, { r: 30, bg: C.forest });
    text(ctx, 'UNSUR (diukur)', lx + 40, colY + 70, fU(40, 700), C.forest); text(ctx, 'PENGENDALI (penentu)', rx + 40, colY + 70, fU(40, 700), C.cream);
    ['suhu', 'tekanan', 'angin', 'hujan'].forEach((s, i) => pill(ctx, s, lx + 40, colY + 150 + i * 80, fU(32, 700), C.forest1, C.forest, 24, 58));
    ['arus laut', 'relief', 'darat-laut'].forEach((s, i) => pill(ctx, s, rx + 40, colY + 150 + i * 80, fU(32, 700), C.forestL, C.cream, 24, 58));
    // flying chips: lintang & ketinggian start in UNSUR column (wrong) then move to PENGENDALI
    const chips = [['lintang', tw('lintang', u28.v0)], ['ketinggian', tw('ketinggian', u28.v0)]];
    chips.forEach(([s, t0], i) => {
      const m = sp(t, tw('pengendali', u28.v0) - 0.2 + i * 0.25, SPRING.snappy);
      const x = lerp(lx + 380, rx + 360, m), y = lerp(colY + 150 + i * 80, colY + 390 + i * 80, m);
      const app = ap(t, t0 - 0.2, 0.3); if (app <= 0) return;
      ctx.save(); ctx.globalAlpha *= app;
      pill(ctx, s, x, y, fU(32, 700), C.clay, C.cream, 24, 58);
      if (m < 0.2 && ap(t, t0, 0.2) > 0) cross(ctx, x - 30, y, 18, C.clayD, 7);
      ctx.restore();
    });
    const pw = ap(t, tw('bukan', u28.v0), 0.4);
    if (pw > 0) { ctx.globalAlpha *= pw; pill(ctx, 'Lintang dan ketinggian = PENGENDALI, bukan unsur', W / 2, colY + ch2 + 70, fU(34, 700), C.clay, C.cream, 30, 64, 'center'); }
    ctx.restore();
  }
  ctx.restore();
}
function drawLand(ctx, a) {
  ctx.save(); ctx.globalAlpha = a;
  for (const [c, rings] of Object.entries(IND)) {
    ctx.fillStyle = c === 'IDN' ? C.land : '#e7e3da';
    for (const r of rings) { ctx.beginPath(); r.forEach(([lo, la], i) => (i ? ctx.lineTo(PX(lo), PY(la)) : ctx.moveTo(PX(lo), PY(la)))); ctx.closePath(); ctx.fill(); }
  }
  ctx.restore();
}

// ================================================================ S7 SOAL
const OPTS = ['17,3 °C', '25,4 °C', '11,3 °C', '20,3 °C', '21,8 °C'];
function sSoal(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'soal');
  const u29 = U_(29), u30 = U_(30), u31 = U_(31), u32 = U_(32), u33 = U_(33), u34 = U_(34), u35 = U_(35), u36 = U_(36), u37 = U_(37);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  // recall chip (u29)
  const pr = sp(t, u29.v0, SPRING.gentle), prq = ap(t, u30.v0, 0.4);
  if (pr > 0 && prq < 1) {
    ctx.save(); ctx.globalAlpha *= (1 - prq);
    text(ctx, 'Kembali ke pertanyaan awal', W / 2, 300, fD(80), C.forest, 'center');
    thermometer(ctx, W / 2 - 60, 760, 300 * pr, 0.42, C.cold, '? °C', C.cold);
    text(ctx, 'Puncak ±1.500 m', W / 2 + 160, 520, fU(34, 700), C.gray);
    ctx.restore();
  }
  // question card: big first, then a compact docked version on the left (crossfade)
  const pq = sp(t, u30.v0, SPRING.snappy);
  const dock = ap(t, u31.v0 - 0.2, 0.7, E.inOutCubic);
  const correct = ap(t, tw('jawabannya', u36.v0), 0.3);
  const Q = 'Suhu rata-rata di tepi pantai Jakarta 26,3 °C. Menurut rumus Braak, T = 26,3 − 0,6h (h dalam ratusan meter), suhu rata-rata kawasan Puncak (±1.500 m dpl) adalah …';
  const opt = (i, ox, oy, ow, oh, fs) => {
    const isA = i === 0, on = isA && correct > 0; const dim = correct > 0 && !isA ? 0.35 : 1;
    ctx.save(); ctx.globalAlpha *= dim;
    rrect(ctx, ox, oy, ow, oh, 18); ctx.fillStyle = on ? C.clay : C.sand; ctx.fill();
    const r = oh * 0.3; circle(ctx, ox + oh * 0.5, oy + oh / 2, r); ctx.fillStyle = on ? C.cream : C.forest; ctx.fill();
    text(ctx, 'ABCDE'[i], ox + oh * 0.5, oy + oh / 2 + fs * 0.36, fU(fs * 0.85, 700), on ? C.clay : C.cream, 'center');
    text(ctx, OPTS[i], ox + oh + 10, oy + oh / 2 + fs * 0.36, fU(fs, 700), on ? C.cream : C.ink);
    if (on) check(ctx, ox + ow - 50, oy + oh / 2, oh * 0.45, C.cream, correct);
    ctx.restore();
  };
  if (pq > 0 && dock < 1) {
    ctx.save(); ctx.globalAlpha *= clamp(pq * 1.5) * (1 - dock); ctx.translate(260, 150 + (1 - pq) * 80);
    card(ctx, 0, 0, 1400, 760, { r: 32 });
    pill(ctx, 'CONTOH SOAL OSN', 50, 66, fU(30, 700), C.clay, C.cream, 24, 58);
    wrap(ctx, Q, fU(42, 500), 1300).forEach((l, i) => text(ctx, l, 50, 170 + i * 58, fU(42, 500), C.ink));
    OPTS.forEach((o, i) => opt(i, 50 + (i % 3) * 440, 400 + Math.floor(i / 3) * 140, 410, 110, 42));
    ctx.restore();
  }
  if (dock > 0) {
    ctx.save(); ctx.globalAlpha *= dock; ctx.translate((1 - dock) * -40, 0);
    card(ctx, 80, 140, 860, 760, { r: 32 });
    pill(ctx, 'CONTOH SOAL OSN', 120, 196, fU(26, 700), C.clay, C.cream, 22, 52);
    wrap(ctx, Q, fU(32, 500), 780).forEach((l, i) => text(ctx, l, 120, 275 + i * 44, fU(32, 500), C.ink));
    OPTS.forEach((o, i) => opt(i, 120, 500 + i * 76, 780, 64, 32));
    ctx.restore();
  }
  // timer during think pause
  const tp0 = u30.v1 + 0.15, tp1 = tp0 + 3.0;
  if (t > tp0 - 0.2 && t < tp1 + 0.4) {
    const a = 1 - ap(t, tp1, 0.35);
    const p = clamp((t - tp0) / 3);
    ctx.save(); ctx.globalAlpha *= a * ap(t, tp0 - 0.2, 0.3);
    const cx = 1760, cy = 220;
    circle(ctx, cx, cy, 80); ctx.fillStyle = C.forest; ctx.fill();
    ctx.strokeStyle = C.amber; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy, 64, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - p)); ctx.stroke();
    text(ctx, `${Math.max(1, Math.ceil(3 - (t - tp0)))}`, cx, cy + 26, fU(74, 700), C.cream, 'center');
    text(ctx, 'pikirkan dulu', cx, cy + 130, fU(28, 700), C.forest, 'center');
    ctx.restore();
  }
  // board on right
  if (dock > 0) {
    const bx = 1000, by = 140, bw = 840;
    ctx.save(); ctx.globalAlpha *= dock;
    card(ctx, bx, by, bw, 760, { r: 32, bg: C.forest });
    text(ctx, 'Rumus Braak', bx + 50, by + 80, fU(36, 700), C.forest3);
    const lines = [
      [tw('braak', u31.v0) + 0.3, 'T = 26,3 − 0,6 h', C.cream, 70],
      [tw('ingat', u32.v0), 'h dalam ratusan meter', C.amber, 40],
      [tw('jadi', u33.v0), 'h = 1.500 ÷ 100 = 15', C.cream, 62],
      [tw('nol', u34.v0), '0,6 × 15 = 9', C.cream, 62],
      [tw('dikurangi', u35.v0) - 0.6, 'T = 26,3 − 9', C.cream, 62],
      [tw('hasilnya', u35.v0), '= 17,3 °C', C.amber, 92],
    ];
    let y = by + 190;
    lines.forEach(([t0, s, col, size]) => {
      const p = ap(t, t0, 0.5, E.outQuint);
      if (p > 0) {
        ctx.save(); ctx.beginPath(); ctx.rect(bx + 30, y - size - 10, bw - 60, size + 40); ctx.clip();
        text(ctx, s, bx + 50, y + (1 - p) * (size + 30), fU(size, 700), col);
        ctx.restore();
      }
      y += size + 34;
    });
    // highlight 15 when computed
    const hl = bump(t, tw('belas', u33.v0) + 0.3, 0.6);
    if (hl > 0) { ctx.save(); ctx.globalAlpha = hl; rrect(ctx, bx + 520, by + 190 + 70 + 34 + 40 + 34 - 54, 100, 70, 14); ctx.strokeStyle = C.amber; ctx.lineWidth = 5; ctx.stroke(); ctx.restore(); }
    // answer tag
    const pk = ap(t, tw('pengendalinya', u37.v0), 0.4);
    if (pk > 0) { ctx.globalAlpha *= pk; pill(ctx, 'Pengendali: ketinggian tempat', bx + bw / 2, by + 700, fU(32, 700), C.clay, C.cream, 26, 60, 'center'); }
    ctx.restore();
  }
  ctx.restore();
}

// ================================================================ S8 JEBAKAN
function warnIcon(ctx, x, y, s) {
  poly(ctx, [[x, y - s], [x + s * 1.1, y + s * 0.85], [x - s * 1.1, y + s * 0.85]]); ctx.fillStyle = C.amber; ctx.fill();
  ctx.lineJoin = 'round'; ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.stroke();
  text(ctx, '!', x, y + s * 0.7, fU(s * 1.2, 700), C.ink, 'center');
}
function sJebakan(ctx, t) {
  fill(ctx, C.sand); const ex = exitP(t, 'jebakan');
  const u38 = U_(38), u39 = U_(39), u40 = U_(40), u41 = U_(41), u42 = U_(42);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  const pw = sp(t, SC.jebakan[0] + 0.05, SPRING.bouncy);
  if (pw > 0) { ctx.save(); ctx.translate(200, 230); ctx.scale(pw, pw); warnIcon(ctx, 0, 0, 80); ctx.restore(); }
  riseText(ctx, 'Jebakan yang sering terjadi', 330, 255, fD(84), C.clayD, ap(t, SC.jebakan[0] + 0.15, 0.5, E.outQuint));
  const cx = 160, w = 1600;
  const p1 = ap(t, u39.v0, 0.5, E.outQuint);
  if (p1 > 0) {
    ctx.save(); ctx.globalAlpha *= p1; card(ctx, cx, 360, w, 300, { r: 30 });
    text(ctx, 'Salah:', cx + 50, 440, fU(36, 700), C.clayD);
    text(ctx, 'h = 1.500', cx + 50, 530, fU(64, 700), C.ink);
    const p2 = ap(t, tw('hasilnya', u40.v0), 0.6);
    if (p2 > 0) { ctx.globalAlpha *= p2; text(ctx, 'T = 26,3 − 0,6 × 1.500 = −873,7 °C', cx + 50, 615, fU(56, 700), C.clayD); }
    ctx.restore();
    const ps = ap(t, tw('mustahil', u41.v0) - 0.3, 0.35, E.inOutCubic);
    if (ps > 0) {
      ctx.strokeStyle = C.clay; ctx.lineWidth = 10; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(cx + 40, 500); ctx.lineTo(cx + 40 + 1080 * ps, 590); ctx.stroke();
      const st = sp(t, tw('mustahil', u41.v0), SPRING.bouncy);
      ctx.save(); ctx.translate(cx + w - 230, 500); ctx.rotate(-0.12); ctx.scale(st, st);
      rrect(ctx, -170, -60, 340, 120, 20); ctx.strokeStyle = C.clayD; ctx.lineWidth = 8; ctx.stroke();
      text(ctx, 'MUSTAHIL', 0, 22, fU(60, 700), C.clayD, 'center'); ctx.restore();
    }
  }
  const p3 = sp(t, u42.v0, SPRING.snappy);
  if (p3 > 0) {
    ctx.save(); ctx.globalAlpha *= clamp(p3 * 1.5); ctx.translate(0, (1 - p3) * 60);
    card(ctx, cx, 700, w, 170, { r: 30, bg: C.forest });
    circle(ctx, cx + 90, 785, 46); ctx.fillStyle = C.cream; ctx.fill(); check(ctx, cx + 90, 785, 50, C.forest, ap(t, u42.v0 + 0.2, 0.4));
    text(ctx, 'Benar: h = 15  (h dalam ratusan meter)', cx + 170, 805, fU(54, 700), C.cream);
    ctx.restore();
  }
  ctx.restore();
}

// ================================================================ S9 SERING MUNCUL
const SERING = [
  ['El Niño, La Niña, IOD, dan MJO', 'SANGAT SERING', 'B01-V01', 1.0],
  ['Efek rumah kaca dan pemanasan global', 'SANGAT SERING', 'B01-V02', 0.97],
  ['Sirkulasi atmosfer global dan monsun', 'SERING', 'B01-V03', 0.72],
  ['Pola curah hujan dan klasifikasi iklim', 'SERING', 'B01-V05', 0.68],
  ['Suhu udara: Braak, lapse rate, föhn', 'SERING', 'B01-V04', 0.66],
  ['Awan, hujan, dan kelembapan', 'SERING', 'B01-V04', 0.62],
];
function sSering(ctx, t) {
  fill(ctx, C.forestD); const ex = exitP(t, 'sering');
  const u43 = U_(43), u44 = U_(44), u45 = U_(45), u46 = U_(46);
  ctx.save(); ctx.globalAlpha = 1 - ex;
  // background grid
  ctx.save(); ctx.globalAlpha *= 0.06; ctx.strokeStyle = C.cream; for (let x = 0; x < W; x += 80) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); } ctx.restore();
  const ph = ap(t, SC.sering[0] + 0.05, 0.5, E.outQuint);
  if (ph > 0) { ctx.save(); ctx.globalAlpha *= ph; pill(ctx, 'SERING MUNCUL DI OSN  ·  BAB 1', 120, 160, fU(32, 700), C.clay, C.cream, 26, 62); ctx.restore(); }
  riseText(ctx, 'Materi yang wajib kamu kuasai', 120, 270, fD(84), C.cream, ap(t, SC.sering[0] + 0.25, 0.5, E.outQuint));
  const T = [tw('el', u44.v0), tw('efek', u44.v0), tw('sirkulasi', u45.v0), tw('klasifikasi', u45.v0), tw('suhu', u45.v0), tw('awan', u45.v0)];
  SERING.forEach(([lab, freq, code, f], i) => {
    const k = sp(t, T[i] - 0.15, SPRING.snappy); if (k <= 0) return;
    const y = 320 + i * 100;
    ctx.save(); ctx.globalAlpha *= clamp(k * 1.5); ctx.translate((1 - k) * -80, 0);
    rrect(ctx, 120, y, 1680, 84, 18); ctx.fillStyle = i < 2 ? 'rgba(224,121,79,0.16)' : 'rgba(255,254,250,0.06)'; ctx.fill();
    const big = i < 2;
    rrect(ctx, 140, y + 16, 240, 44, 22); ctx.fillStyle = big ? C.clay : C.amber; ctx.fill();
    text(ctx, freq, 260, y + 47, fU(22, 700), big ? C.cream : C.ink, 'center');
    text(ctx, lab, 410, y + 56, fU(42, 700), C.cream);
    // frequency bar
    const bw = 260 * f * ap(t, T[i], 0.7);
    rrect(ctx, 1360, y + 28, 260, 20, 10); ctx.fillStyle = 'rgba(255,254,250,0.12)'; ctx.fill();
    rrect(ctx, 1360, y + 28, bw, 20, 10); ctx.fillStyle = big ? C.clay : C.amber; ctx.fill();
    text(ctx, code, 1780, y + 49, fU(28, 700), C.forest3, 'right');
    ctx.restore();
  });
  const pn = ap(t, tw('berikutnya', u46.v0), 0.5);
  if (pn > 0) { ctx.save(); ctx.globalAlpha *= pn; text(ctx, 'Dibahas satu per satu di video berikutnya', 120, 935, fU(36, 700), C.amber); arrowLine(ctx, 870, 923, 930 + 20 * Math.sin(t * 5), 923, C.amber, 6, 22); ctx.restore(); }
  ctx.restore();
}

// ================================================================ S10 OUTRO
function sOutro(ctx, t) {
  const [a] = SC.outro; const lt = t - a;
  fill(ctx, C.forest);
  const wipe = E.inOutCubic(prog(lt, 0, 0.45));
  if (wipe < 1) { ctx.fillStyle = C.forestD; ctx.fillRect(0, 0, W, H * (1 - wipe)); }
  const k = sp(t, a + 0.2, SPRING.bouncy), needle = (1 - spring(lt - 0.3, { stiffness: 60, damping: 9 })) * Math.PI * 2;
  const s = 280 * k; if (s > 2) logo(ctx, W / 2 - s / 2, 150, s, needle);
  riseText(ctx, 'Latihan soalnya di OSNGEO.id', W / 2, 560, fD(110), C.cream, ap(t, a + 0.5, 0.6, E.outQuint), 'center');
  const p2 = ap(t, tw('menu', a), 0.5);
  if (p2 > 0) { ctx.save(); ctx.globalAlpha = p2; pill(ctx, 'Menu Soal Pendalaman Materi  ·  Bab 1', W / 2, 650, fU(36, 700), C.clay, C.cream, 30, 68, 'center'); ctx.restore(); }
  const p3 = ap(t, a + 3.5, 0.5);
  if (p3 > 0) {
    ctx.save(); ctx.globalAlpha = p3;
    rrect(ctx, W / 2 - 520, 740, 1040, 110, 24); ctx.fillStyle = 'rgba(255,254,250,0.08)'; ctx.fill();
    text(ctx, 'BERIKUTNYA', W / 2 - 480, 785, fU(24, 700), C.forest3);
    text(ctx, 'B01-V01 · El Niño, La Niña, dan IOD', W / 2 - 480, 830, fU(38, 700), C.cream);
    ctx.restore();
  }
}

// ---------------------------------------------------------------- timed hits (need timing)
function addTimedHits() {
  const u = (i) => U_(i);
  hit(tw('tiga', 4), 'thermo 32', 'tick', { gain: 0.4 });
  hit(u(1).v0, 'puncak panel', 'whoosh', { len: 0.45, from: 2200, to: 500, gain: 0.35 });
  hit(u(3).v0, 'kenapa', 'pop', { pitch: 'A5', gain: 0.5 });
  hit(tw('mesin', u(4).v0), 'title', 'bell', { pitch: 'D6', gain: 0.35 });
  hit(tw('cuaca', u(5).v0), 'card cuaca', 'click', { gain: 0.4 });
  hit(tw('iklim', u(5).v0), 'card iklim', 'click', { gain: 0.4 });
  hit(tw('tiga', u(9).v0) + 2.2, '30 badge', 'pop', { pitch: 'E6', gain: 0.45 });
  UNSUR.forEach(([w], i) => hit(tw(w, u(12).v0) - 0.1, 'unsur ' + w, 'pop', { pitch: 600 + i * 70, gain: 0.35 }));
  hit(u(14).v0, 'sun', 'swell', { len: 0.8, gain: 0.25 });
  hit(tw('tidak', u(17).v0), 'headline', 'thud', { gain: 0.35 });
  [tw('suhu', u(19).v0), tw('tekanan', u(19).v0), tw('angin', u(21).v0), tw('uap', u(22).v0), tw('awan', u(23).v0), tw('hujan', u(23).v0)].forEach((x, i) => hit(x - 0.15, 'domino ' + i, 'tok', { pitch: 420 + i * 60, gain: 0.4 }));
  KENDALI.forEach(([w], i) => hit(tw(w, u(27).v0) - 0.1, 'kendali ' + w, 'tick', { gain: 0.35 }));
  hit(tw('pengendali', u(28).v0) - 0.2, 'chips fly', 'whoosh', { len: 0.35, gain: 0.3 });
  hit(u(30).v0, 'soal card', 'whoosh', { len: 0.4, gain: 0.3 });
  [0, 1, 2].forEach((k) => hit(u(30).v1 + 0.15 + k, 'timer ' + k, 'blip', { pitch: 880, gain: 0.25 }));
  hit(tw('hasilnya', u(35).v0), 'result', 'pop', { pitch: 'G5', gain: 0.4 });
  hit(tw('jawabannya', u(36).v0), 'answer A', 'bell', { pitch: 'E6', gain: 0.45 });
  hit(u(38).v0, 'warning', 'thud', { gain: 0.4 });
  hit(tw('mustahil', u(41).v0), 'stamp', 'impact', { gain: 0.3 });
  hit(u(42).v0, 'correct', 'bell', { pitch: 'D6', gain: 0.35 });
  hit(u(43).v0, 'sering header', 'whoosh', { len: 0.45, gain: 0.3 });
  [tw('el', u(44).v0), tw('efek', u(44).v0), tw('sirkulasi', u(45).v0), tw('klasifikasi', u(45).v0), tw('suhu', u(45).v0), tw('awan', u(45).v0)].forEach((x, i) => hit(x - 0.15, 'row ' + i, 'click', { gain: 0.35 }));
  hit(SC.outro[0] + 0.2, 'logo', 'bell', { pitch: 'D6', gain: 0.4 });
  HITS.sort((a, b) => a[0] - b[0]);
}

// ---------------------------------------------------------------- film
M.film({
  fonts: [font(100, 400, D), font(40, 500, UI), font(40, 700, UI)],
  hits: HITS,
  samples: (t) => 4,
  async init() {
    TM = await fetch('timing.json').then((r) => r.json());
    IND = await fetch('assets/indo.json').then((r) => r.json());
    buildCaps(); addTimedHits();
  },
  draw(ctx, u, t) {
    const S = Object.entries(SC).find(([, [a, b]]) => t >= a && t < b)?.[0] || 'outro';
    ({ intro: sIntro, hook: sHook, cuaca: sCuaca, unsur: sUnsur, matahari: sMatahari, domino: sDomino, kendali: sKendali, soal: sSoal, jebakan: sJebakan, sering: sSering, outro: sOutro })[S](ctx, t);
    if (S !== 'intro' && S !== 'outro') centerMark(ctx, S === 'sering' ? 0.9 : 1, S === 'sering' ? C.cream : C.forest);
    lowerThird(ctx, t);
    if (S !== 'intro') captions(ctx, t);
    cornerMark(ctx);
  },
});
