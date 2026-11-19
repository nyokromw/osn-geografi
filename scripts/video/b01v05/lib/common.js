// Shared OSNGEO.id video kit: palette, type, props, watermark, captions, timing helpers.
import * as M from './motion.js';
const { W, H, E, prog, lerp, clamp, spring, SPRING, font, text, rrect, hash01 } = M;

export const C = {
  forest: '#1d4138', forestD: '#162923', forestL: '#396957', forest3: '#aac6b5', forest1: '#e2ede4',
  cream: '#fffefa', sand: '#f7f1e8', sand2: '#efe3cf', sand3: '#ded0ba',
  clay: '#e0794f', clayD: '#983f29', amber: '#f2b13a', ink: '#1b322b', gray: '#52655d',
  sea: '#dcebf3', land: '#f3e6c4', blue: '#2b6cb0', cold: '#4a90c2', warm: '#e9a072',
};
export const D = 'Display', UI = 'UI';
export const fD = (s) => font(s, 400, D);
export const fU = (s, w = 500) => font(s, w, UI);

// ---------------------------------------------------------------- timing
export const T = { tm: null };
const norm = (s) => s.toLowerCase().replace(/[^a-z0-9]/g, '');
export function tw(w, after = 0, n = 0) {
  const k = norm(w); let c = 0;
  for (const x of T.tm.words) if (x.t >= after - 0.01 && norm(x.w) === k) { if (c === n) return x.t; c++; }
  console.error('word not found', w, after); return after;
}
export const U_ = (i) => T.tm.units[i];
export const sp = (t, t0, cfg = SPRING.snappy) => spring(t - t0, cfg);
export const ap = (t, t0, d = 0.45, ease = E.outCubic) => ease(prog(t, t0, t0 + d));

// ---------------------------------------------------------------- primitives
export function poly(ctx, pts) { ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); }
export function circle(ctx, x, y, r) { ctx.beginPath(); ctx.arc(x, y, Math.max(0, r), 0, Math.PI * 2); }
export function card(ctx, x, y, w, h, { r = 28, bg = C.cream, stroke = null, shadow = true } = {}) {
  ctx.save();
  if (shadow) { ctx.shadowColor = 'rgba(22,41,35,0.14)'; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10; }
  rrect(ctx, x, y, w, h, r); ctx.fillStyle = bg; ctx.fill();
  ctx.restore();
  if (stroke) { rrect(ctx, x, y, w, h, r); ctx.strokeStyle = stroke; ctx.lineWidth = 3; ctx.stroke(); }
}
export function arrowLine(ctx, x1, y1, x2, y2, color, w = 6, head = 22) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  if (Math.hypot(x2 - x1, y2 - y1) < 2) return;
  ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2 - Math.cos(a) * head * 0.6, y2 - Math.sin(a) * head * 0.6); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - head * Math.cos(a - 0.45), y2 - head * Math.sin(a - 0.45));
  ctx.lineTo(x2 - head * Math.cos(a + 0.45), y2 - head * Math.sin(a + 0.45)); ctx.closePath(); ctx.fill();
}
export function check(ctx, x, y, s, color, p = 1) {
  ctx.strokeStyle = color; ctx.lineWidth = s * 0.16; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const pts = [[x - s * 0.42, y], [x - s * 0.12, y + s * 0.3], [x + s * 0.45, y - s * 0.35]];
  const L1 = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]), L2 = Math.hypot(pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]);
  const d = p * (L1 + L2);
  ctx.beginPath(); ctx.moveTo(...pts[0]);
  if (d <= L1) ctx.lineTo(lerp(pts[0][0], pts[1][0], d / L1), lerp(pts[0][1], pts[1][1], d / L1));
  else { ctx.lineTo(...pts[1]); const k = (d - L1) / L2; ctx.lineTo(lerp(pts[1][0], pts[2][0], k), lerp(pts[1][1], pts[2][1], k)); }
  ctx.stroke();
}
export function cross(ctx, x, y, s, color, w = 10) {
  ctx.strokeStyle = color; ctx.lineWidth = w; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x - s, y - s); ctx.lineTo(x + s, y + s); ctx.moveTo(x + s, y - s); ctx.lineTo(x - s, y + s); ctx.stroke();
}
export function wrap(ctx, str, f, maxW) {
  ctx.font = f; const words = str.split(' '); const lines = []; let cur = '';
  for (const w of words) { const n = cur ? cur + ' ' + w : w; if (ctx.measureText(n).width > maxW && cur) { lines.push(cur); cur = w; } else cur = n; }
  if (cur) lines.push(cur); return lines;
}
export function riseText(ctx, str, x, y, f, color, p, align = 'left') {
  if (p <= 0) return;
  ctx.save(); ctx.globalAlpha *= clamp(p * 1.6);
  text(ctx, str, x, y + (1 - p) * 40, f, color, align);
  ctx.restore();
}
export function pill(ctx, str, x, y, f, bg, fg, padX = 22, h = 56, align = 'left') {
  ctx.font = f; const w = ctx.measureText(str).width + padX * 2;
  const x0 = align === 'center' ? x - w / 2 : align === 'right' ? x - w : x;
  rrect(ctx, x0, y - h / 2, w, h, h / 2); ctx.fillStyle = bg; ctx.fill();
  text(ctx, str, x0 + w / 2, y + h * 0.17, f, fg, 'center');
  return w;
}
export function warnIcon(ctx, x, y, s) {
  poly(ctx, [[x, y - s], [x + s * 1.1, y + s * 0.85], [x - s * 1.1, y + s * 0.85]]); ctx.fillStyle = C.amber; ctx.fill();
  ctx.lineJoin = 'round'; ctx.strokeStyle = C.ink; ctx.lineWidth = s * 0.1; ctx.stroke();
  text(ctx, '!', x, y + s * 0.7, fU(s * 1.2, 700), C.ink, 'center');
}

// ---------------------------------------------------------------- weather props
export function sun(ctx, x, y, r, t, alpha = 1) {
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
export function cloud(ctx, x, y, s, color = '#ffffff', stroke = C.ink) {
  if (s <= 0.01) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.beginPath();
  ctx.arc(-38, 10, 30, Math.PI * 0.5, Math.PI * 1.5); ctx.arc(-8, -18, 38, Math.PI, Math.PI * 1.85);
  ctx.arc(34, -2, 30, Math.PI * 1.3, Math.PI * 0.5); ctx.closePath();
  ctx.fillStyle = color; ctx.fill(); ctx.lineWidth = 5 / s; ctx.strokeStyle = stroke; ctx.stroke();
  ctx.restore();
}
export function rain(ctx, x, y, w, t, n = 9, color = C.blue, len = 26, speed = 260, alpha = 1) {
  if (alpha <= 0) return;
  ctx.save(); ctx.strokeStyle = color; ctx.lineWidth = 5; ctx.lineCap = 'round';
  for (let k = 0; k < n; k++) {
    const px = x - w / 2 + (k + 0.5) * w / n;
    const ph = ((t * speed + hash01(k, 7) * 120) % 120);
    ctx.globalAlpha = alpha * (1 - ph / 120);
    ctx.beginPath(); ctx.moveTo(px - ph * 0.15, y + ph); ctx.lineTo(px - ph * 0.15 - 6, y + ph + len); ctx.stroke();
  }
  ctx.restore();
}
export function fish(ctx, x, y, s, color = C.forestL) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = color;
  ctx.beginPath(); ctx.ellipse(0, 0, 22, 11, 0, 0, Math.PI * 2); ctx.fill();
  poly(ctx, [[18, 0], [34, -12], [34, 12]]); ctx.fill();
  circle(ctx, -12, -3, 2.5); ctx.fillStyle = '#fff'; ctx.fill();
  ctx.restore();
}

// ---------------------------------------------------------------- maps
export function mapProj(box, ext) {
  const PX = (lon) => box.x + (lon - ext[0]) / (ext[1] - ext[0]) * box.w;
  const PY = (lat) => box.y + (ext[3] - lat) / (ext[3] - ext[2]) * box.h;
  return { PX, PY };
}
export function drawRings(ctx, rings, P, fill = C.land, stroke = '#a8916a', lw = 1.1) {
  ctx.fillStyle = fill; ctx.strokeStyle = stroke; ctx.lineWidth = lw;
  for (const r of rings) { ctx.beginPath(); r.forEach(([lo, la], i) => (i ? ctx.lineTo(P.PX(lo), P.PY(la)) : ctx.moveTo(P.PX(lo), P.PY(la)))); ctx.closePath(); ctx.fill(); if (lw) ctx.stroke(); }
}

// ---------------------------------------------------------------- brand
export function logo(ctx, x, y, s, needle = 0, alpha = 1) {
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
export function cornerMark(ctx) {
  const h = 84, x1 = W - 40, y0 = 36;
  ctx.font = fU(40, 700); const tw_ = ctx.measureText('OSNGEO.id').width;
  const w = tw_ + h + 34, x0 = x1 - w;
  ctx.save(); ctx.shadowColor = 'rgba(0,0,0,0.25)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 4;
  rrect(ctx, x0, y0, w, h, h / 2); ctx.fillStyle = 'rgba(29,65,56,0.92)'; ctx.fill(); ctx.restore();
  logo(ctx, x0 + 10, y0 + 10, h - 20);
  text(ctx, 'OSNGEO.id', x0 + h + 8, y0 + h / 2 + 14, fU(40, 700), C.cream);
}
export function centerMark(ctx, a = 1, col = C.forest) {
  ctx.save(); ctx.globalAlpha = 0.065 * a; ctx.translate(W / 2, H * 0.47); ctx.rotate(-12 * Math.PI / 180);
  ctx.font = fU(250, 700); ctx.textAlign = 'center'; ctx.fillStyle = col; ctx.fillText('OSNGEO.id', 0, 85);
  ctx.restore();
}
export function lowerThird(ctx, t, line2, t0 = 5.0, t1 = 10.2) {
  const p = ap(t, t0, 0.5, E.outQuint), q = E.inCubic(prog(t, t1, t1 + 0.5));
  if (p <= 0 || q >= 1) return;
  const x = 60 - (1 - p) * 120 - q * 120, y = 64;
  ctx.save(); ctx.globalAlpha = p * (1 - q);
  rrect(ctx, x, y, 860, 92, 22); ctx.fillStyle = C.forest; ctx.fill();
  rrect(ctx, x, y, 14, 92, 7); ctx.fillStyle = C.clay; ctx.fill();
  text(ctx, 'Video Konsep OSN Geografi', x + 40, y + 42, fU(34, 700), C.cream);
  text(ctx, line2, x + 40, y + 76, fU(26, 500), C.forest3);
  ctx.restore();
}

// ---------------------------------------------------------------- captions
let CAPS = null;
const REPL = [[/\bI O D\b/g, 'IOD'], [/\bO N I\b/g, 'ONI'], [/\bS O I\b/g, 'SOI'], [/\bD M I\b/g, 'DMI'], [/\bM J O\b/g, 'MJO'],
  [/O S N Geo titik I D/g, 'OSNGEO.id'], [/El Nino/g, 'El Niño'], [/La Nina/g, 'La Niña'], [/Nino tiga koma empat/g, 'Niño 3.4'], [/Oceanic Nino/g, 'Oceanic Niño'], [/C O dua ekuivalen/g, 'CO2-ekuivalen'], [/\bG W P\b/g, 'GWP'], [/\bI P C C\b/g, 'IPCC'], [/\bN D C\b/g, 'NDC'], [/\b[Pp] p m\b/g, 'ppm']];
export const capText = (s) => REPL.reduce((a, [r, b]) => a.replace(r, b), s);
export function buildCaps() {
  CAPS = [];
  for (const u of T.tm.units) {
    const ws = T.tm.words.filter((w) => w.u === u.i);
    let chunk = [], len = 0;
    const flush = (end) => { if (chunk.length) CAPS.push({ t0: chunk[0].t, t1: end, s: chunk.map((w) => w.w).join(' '), u: u.i }); chunk = []; len = 0; };
    ws.forEach((w, k) => {
      chunk.push(w); len += w.w.length + 1;
      const brk = /[,:]$/.test(w.w) && len > 34;
      if ((brk || len > 62) && k < ws.length - 1) flush(ws[k + 1].t - 0.05);
    });
    flush(u.v1 + 0.25);
    const n = CAPS.length;
    if (n >= 2 && CAPS[n - 1].u === u.i && CAPS[n - 2].u === u.i && CAPS[n - 1].s.length < 18 && CAPS[n - 2].s.length + CAPS[n - 1].s.length < 90) {
      CAPS[n - 2].s += ' ' + CAPS[n - 1].s; CAPS[n - 2].t1 = CAPS[n - 1].t1; CAPS.pop();
    }
  }
  for (let i = 0; i < CAPS.length - 1; i++) CAPS[i].t1 = Math.min(CAPS[i].t1, CAPS[i + 1].t0 - 0.02);
  return CAPS;
}
export function captions(ctx, t) {
  const c = CAPS.find((c) => t >= c.t0 && t < c.t1);
  if (!c) return;
  const s = capText(c.s);
  const f = fU(38, 500); const lines = wrap(ctx, s, f, 1440);
  const lh = 50, h = lines.length * lh + 28, y0 = H - 40 - h;
  let mw = 0; ctx.font = f; lines.forEach((l) => (mw = Math.max(mw, ctx.measureText(l).width)));
  rrect(ctx, W / 2 - mw / 2 - 30, y0, mw + 60, h, 18); ctx.fillStyle = 'rgba(22,41,35,0.84)'; ctx.fill();
  lines.forEach((l, i) => text(ctx, l, W / 2, y0 + 14 + lh * (i + 0.78), f, C.cream, 'center'));
}

// ---------------------------------------------------------------- intro / outro
export function intro(ctx, t, chip, title, sub) {
  ctx.fillStyle = C.forest; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.globalAlpha = 0.08; ctx.strokeStyle = C.cream; ctx.lineWidth = 2;
  for (let k = -6; k <= 6; k++) { ctx.beginPath(); ctx.ellipse(W / 2, H / 2, Math.abs(k) * 90 + 1, 520, 0, 0, Math.PI * 2); ctx.stroke(); }
  for (let k = -4; k <= 4; k++) { ctx.beginPath(); ctx.moveTo(0, H / 2 + k * 120); ctx.lineTo(W, H / 2 + k * 120); ctx.stroke(); }
  ctx.restore();
  const k = sp(t, 0.05, SPRING.bouncy), needle = (1 - spring(t - 0.15, { stiffness: 60, damping: 9 })) * Math.PI * 3;
  const s = 230 * k;
  if (s > 2) logo(ctx, 360 - s / 2, H / 2 - s / 2, s, needle);
  const p1 = ap(t, 0.55, 0.6, E.outQuint), p2 = ap(t, 0.8, 0.7, E.outQuint), p3 = ap(t, 1.15, 0.6, E.outQuint);
  const x = 560;
  ctx.save(); ctx.beginPath(); ctx.rect(x - 10, 300, 1340, 480); ctx.clip();
  if (p1 > 0) { ctx.globalAlpha = p1; pill(ctx, chip, x + (1 - p1) * -80, 410, fU(30, 700), C.clay, C.cream); }
  ctx.globalAlpha = 1;
  if (p2 > 0) text(ctx, title, x, 590 + (1 - p2) * 140, fD(title.length > 22 ? 118 : 150), C.cream);
  if (p3 > 0) { ctx.globalAlpha = p3; text(ctx, sub, x, 670 + (1 - p3) * 40, fU(36, 500), C.forest3); }
  ctx.restore();
  const q = E.inCubic(prog(t, 2.6, 3.0));
  if (q > 0) { ctx.fillStyle = C.sand; ctx.fillRect(0, H * (1 - q), W, H * q); }
}
export function outro(ctx, t, a, menuT, sub, next) {
  const lt = t - a;
  ctx.fillStyle = C.forest; ctx.fillRect(0, 0, W, H);
  const wipe = E.inOutCubic(prog(lt, 0, 0.45));
  if (wipe < 1) { ctx.fillStyle = C.forestD; ctx.fillRect(0, 0, W, H * (1 - wipe)); }
  const k = sp(t, a + 0.2, SPRING.bouncy), needle = (1 - spring(lt - 0.3, { stiffness: 60, damping: 9 })) * Math.PI * 2;
  const s = 280 * k; if (s > 2) logo(ctx, W / 2 - s / 2, 150, s, needle);
  riseText(ctx, 'Latihan soalnya di OSNGEO.id', W / 2, 560, fD(110), C.cream, ap(t, a + 0.5, 0.6, E.outQuint), 'center');
  const p2 = ap(t, menuT, 0.5);
  if (p2 > 0) { ctx.save(); ctx.globalAlpha = p2; pill(ctx, sub, W / 2, 650, fU(36, 700), C.clay, C.cream, 30, 68, 'center'); ctx.restore(); }
  const p3 = ap(t, a + 3.5, 0.5);
  if (p3 > 0) {
    ctx.save(); ctx.globalAlpha = p3;
    rrect(ctx, W / 2 - 560, 740, 1120, 110, 24); ctx.fillStyle = 'rgba(255,254,250,0.08)'; ctx.fill();
    text(ctx, 'BERIKUTNYA', W / 2 - 520, 785, fU(24, 700), C.forest3);
    text(ctx, next, W / 2 - 520, 830, fU(38, 700), C.cream);
    ctx.restore();
  }
}
