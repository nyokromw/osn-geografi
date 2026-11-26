// Si Gumpal: animated air-parcel character + small scene props. Pure function of time.
import * as M from './motion.js';
import { C, fU, circle, poly, arrowLine, cloud } from './common.js';
const { lerp, clamp, hash01, text, rrect, mix } = M;

// o: { t, temp 0..1 (cold..hot), cloud 0..1, mood: 'happy'|'cold'|'hot'|'wow'|'calm', glass: 0..1 size, fill: 0..1, sweat, shiver, look:[dx,dy], squash }
export function gumpal(ctx, x, y, r, o = {}) {
  const t = o.t || 0, temp = o.temp ?? 0.6, cl = o.cloud || 0, mood = o.mood || 'happy';
  const sh = (o.shiver || 0) * Math.sin(t * 46) * r * 0.025;
  const sq = o.squash || 0;
  ctx.save(); ctx.translate(x + sh, y + Math.sin(t * 2.1) * r * 0.04); ctx.scale(1 + sq * 0.12, 1 - sq * 0.12);
  // shadow
  ctx.save(); ctx.globalAlpha *= 0.18; ctx.fillStyle = '#000'; ctx.beginPath(); ctx.ellipse(0, r * 1.15, r * 0.8, r * 0.14, 0, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  // body
  const N = 64; const body = (k) => { ctx.beginPath(); for (let i = 0; i <= N; i++) { const a = i / N * Math.PI * 2; const rr = r * k * (1 + 0.035 * Math.sin(3 * a + t * 2.2) + 0.025 * Math.sin(5 * a - t * 3.1) + cl * 0.13 * Math.abs(Math.sin(4 * a + 0.4))); const px = Math.cos(a) * rr, py = Math.sin(a) * rr * 0.94; i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.closePath(); };
  const warm = temp > 0.5 ? mix('#ffe4c4', '#ffa25e', (temp - 0.5) * 2) : mix('#8fcaf2', '#ffe4c4', temp * 2); const base = mix(warm, '#ffffff', cl * 0.85);
  const g = ctx.createRadialGradient(-r * 0.35, -r * 0.4, r * 0.1, 0, 0, r * 1.1); g.addColorStop(0, mix(base, '#ffffff', 0.45)); g.addColorStop(1, mix(base, '#1d4138', 0.12));
  body(1); ctx.fillStyle = g; ctx.fill(); ctx.lineWidth = r * 0.05; ctx.strokeStyle = mix(base, '#1d4138', 0.55); ctx.stroke();
  // inner glass (capacity metaphor)
  if (o.glass != null) {
    const gw = r * 0.9 * o.glass, gh = r * 1.0 * o.glass, gx = -gw / 2, gy = r * 0.62 - gh;
    ctx.save(); ctx.globalAlpha *= 0.9;
    rrect(ctx, gx, gy, gw, gh, gw * 0.12); ctx.fillStyle = 'rgba(255,255,255,0.35)'; ctx.fill();
    const f = clamp(o.fill ?? 0.5), wh = gh * Math.min(1, f);
    ctx.save(); rrect(ctx, gx, gy, gw, gh, gw * 0.12); ctx.clip();
    ctx.fillStyle = f >= 0.999 ? 'rgba(43,108,176,0.85)' : 'rgba(64,140,210,0.7)'; ctx.beginPath(); ctx.moveTo(gx, gy + gh - wh); for (let i = 0; i <= 20; i++) { const xx = gx + gw * i / 20; ctx.lineTo(xx, gy + gh - wh + Math.sin(i * 0.9 + t * 4) * r * 0.012); } ctx.lineTo(gx + gw, gy + gh); ctx.lineTo(gx, gy + gh); ctx.closePath(); ctx.fill(); ctx.restore();
    rrect(ctx, gx, gy, gw, gh, gw * 0.12); ctx.strokeStyle = f >= 0.999 ? '#ffe680' : 'rgba(255,255,255,0.95)'; ctx.lineWidth = r * (f >= 0.999 ? 0.05 : 0.03); ctx.stroke();
    ctx.restore();
  }
  // face
  const fy = o.glass != null ? -r * 0.48 : -r * 0.12, lk = o.look || [0, 0];
  const blink = ((t + (o.seed || 0)) % 3.7) < 0.13 ? 0.15 : 1;
  [-1, 1].forEach((s) => { ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.ellipse(s * r * 0.28, fy, r * 0.13, r * 0.15 * blink, 0, 0, Math.PI * 2); ctx.fill(); ctx.fillStyle = '#1b322b'; ctx.beginPath(); ctx.ellipse(s * r * 0.28 + lk[0] * r * 0.05, fy + r * 0.02 + lk[1] * r * 0.04, r * 0.07, r * 0.08 * blink, 0, 0, Math.PI * 2); ctx.fill(); circle(ctx, s * r * 0.28 + lk[0] * r * 0.05 + r * 0.025, fy - r * 0.02, r * 0.022); ctx.fillStyle = '#fff'; ctx.fill(); });
  ctx.fillStyle = 'rgba(232,110,90,0.35)'; [-1, 1].forEach((s) => { ctx.beginPath(); ctx.ellipse(s * r * 0.48, fy + r * 0.17, r * 0.1, r * 0.06, 0, 0, Math.PI * 2); ctx.fill(); });
  ctx.strokeStyle = '#1b322b'; ctx.lineWidth = r * 0.045; ctx.lineCap = 'round';
  const my = fy + r * 0.24;
  if (mood === 'happy' || mood === 'calm') { ctx.beginPath(); ctx.arc(0, my - r * 0.06, r * (mood === 'happy' ? 0.16 : 0.1), 0.2 * Math.PI, 0.8 * Math.PI); ctx.stroke(); }
  else if (mood === 'cold') { ctx.beginPath(); for (let i = 0; i <= 8; i++) { const xx = -r * 0.16 + i * r * 0.04, yy = my + Math.sin(i * 2 + t * 30) * r * 0.025; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
  else if (mood === 'hot') { ctx.fillStyle = '#7a2a1a'; ctx.beginPath(); ctx.ellipse(0, my, r * 0.12, r * 0.08, 0, 0, Math.PI); ctx.fill(); }
  else if (mood === 'wow') { ctx.beginPath(); ctx.ellipse(0, my + r * 0.02, r * 0.07, r * 0.09, 0, 0, Math.PI * 2); ctx.stroke(); }
  // sweat drops / frost
  if (o.sweat > 0) for (let i = 0; i < 3; i++) { const ph = (t * 0.9 + i / 3) % 1; ctx.save(); ctx.globalAlpha *= o.sweat * (1 - ph); const sx = r * (0.65 + 0.1 * i), sy = -r * 0.5 + ph * r * 0.8; ctx.fillStyle = '#6fb7e6'; ctx.beginPath(); ctx.moveTo(sx, sy - r * 0.08); ctx.quadraticCurveTo(sx + r * 0.06, sy, sx, sy + r * 0.05); ctx.quadraticCurveTo(sx - r * 0.06, sy, sx, sy - r * 0.08); ctx.fill(); ctx.restore(); }
  if (o.shiver > 0) { ctx.save(); ctx.globalAlpha *= o.shiver; ctx.strokeStyle = '#ffffff'; ctx.lineWidth = r * 0.025; [[-1.05, -0.4], [1.05, -0.2], [-0.95, 0.4]].forEach(([a, b]) => { const sx = a * r, sy = b * r; for (let k = 0; k < 3; k++) { const an = k * Math.PI / 3; ctx.beginPath(); ctx.moveTo(sx - Math.cos(an) * r * 0.08, sy - Math.sin(an) * r * 0.08); ctx.lineTo(sx + Math.cos(an) * r * 0.08, sy + Math.sin(an) * r * 0.08); ctx.stroke(); } }); ctx.restore(); }
  ctx.restore();
}

// minimal floating label (term + optional English)
export function tag(ctx, x, y, a, b, k = 1, col = C.forest) {
  if (k <= 0) return; ctx.save(); ctx.globalAlpha *= clamp(k); ctx.translate(x, y + (1 - clamp(k)) * 20);
  ctx.font = fU(34, 800); const w1 = ctx.measureText(a).width; ctx.font = `30px DisplayI`; const w2 = b ? ctx.measureText(b).width + 24 : 0;
  const w = w1 + w2 + 48; rrect(ctx, -w / 2, -34, w, 68, 34); ctx.fillStyle = col; ctx.fill();
  text(ctx, a, -w / 2 + 24, 12, fU(34, 800), C.cream); if (b) text(ctx, b, -w / 2 + 24 + w1 + 24, 11, '30px DisplayI', C.amber);
  ctx.restore();
}
// big number that counts
export function bigNum(ctx, x, y, v, suffix, k, size = 150, col = C.forest, dec = 0) {
  if (k <= 0) return; ctx.save(); ctx.globalAlpha *= clamp(k * 1.5); const s = `${v.toFixed(dec).replace('.', ',')}${suffix}`; text(ctx, s, x, y, fU(size, 800), col, 'center'); ctx.restore();
}
// thermometer prop
export function thermo(ctx, x, y, h, frac, color, label) {
  rrect(ctx, x - 16, y - h, 32, h, 16); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  circle(ctx, x, y + 14, 28); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); circle(ctx, x, y + 14, 19); ctx.fillStyle = color; ctx.fill();
  const fh = (h - 24) * clamp(frac); rrect(ctx, x - 8, y - fh - 4, 16, fh + 16, 8); ctx.fillStyle = color; ctx.fill();
  if (label) text(ctx, label, x, y + 80, fU(30, 800), C.ink, 'center');
}
// paper-cut rice field with swaying grass
export function sawah(ctx, y0, t, W, night = 0) {
  const rows = [['#a9cf8a', 0], ['#8cc06c', 40], ['#73ad57', 90]];
  rows.forEach(([c, dy], k) => { ctx.fillStyle = mix(c, '#22362c', night * 0.6); ctx.beginPath(); ctx.moveTo(0, 1080); ctx.lineTo(0, y0 + dy); for (let x = 0; x <= W; x += 40) ctx.lineTo(x, y0 + dy + 8 * Math.sin(x * 0.01 + k)); ctx.lineTo(W, 1080); ctx.closePath(); ctx.fill(); });
  ctx.strokeStyle = mix('#4f8a3c', '#1a2a20', night * 0.6); ctx.lineWidth = 3; ctx.lineCap = 'round';
  for (let i = 0; i < 90; i++) { const x = (i * 23.7) % W, yb = y0 + 60 + (i % 5) * 22, sw = 6 * Math.sin(t * 1.6 + i); ctx.beginPath(); ctx.moveTo(x, yb); ctx.quadraticCurveTo(x + sw * 0.5, yb - 18, x + sw, yb - 34); ctx.stroke(); }
}
// water drop
export function drop(ctx, x, y, s, col = '#5aa8e0') { ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(x, y - s); ctx.quadraticCurveTo(x + s * 0.75, y, x, y + s * 0.6); ctx.quadraticCurveTo(x - s * 0.75, y, x, y - s); ctx.fill(); circle(ctx, x - s * 0.18, y - s * 0.05, s * 0.15); ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.fill(); }
// glass of iced tea (perspective)
export function iceTea(ctx, x, y, s, t, wet = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = 'rgba(200,225,240,0.35)'; ctx.beginPath(); ctx.moveTo(-90, -220); ctx.lineTo(-70, 120); ctx.ellipse(0, 120, 70, 18, 0, Math.PI, 0, true); ctx.lineTo(90, -220); ctx.closePath(); ctx.fill();
  ctx.fillStyle = '#c0712f'; ctx.beginPath(); ctx.moveTo(-84, -140); ctx.lineTo(-70, 118); ctx.ellipse(0, 118, 70, 16, 0, Math.PI, 0, true); ctx.lineTo(84, -140); ctx.ellipse(0, -140, 84, 18, 0, 0, Math.PI, false); ctx.closePath(); ctx.fill();
  ctx.fillStyle = 'rgba(255,255,255,0.75)'; [[-40, -150, 0.3], [25, -160, -0.4], [-5, -120, 0.1]].forEach(([a, b, r], i) => { ctx.save(); ctx.translate(a, b + Math.sin(t * 2 + i) * 3); ctx.rotate(r + Math.sin(t + i) * 0.05); rrect(ctx, -26, -22, 52, 44, 8); ctx.fill(); ctx.restore(); });
  ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.ellipse(0, -220, 90, 20, 0, 0, Math.PI * 2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-90, -220); ctx.lineTo(-70, 120); ctx.moveTo(90, -220); ctx.lineTo(70, 120); ctx.stroke();
  ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(-60, -190); ctx.lineTo(-48, 80); ctx.stroke();
  // condensation
  for (let i = 0; i < 46; i++) { const k = clamp(wet * 1.4 - hash01(i, 3) * 0.5); if (k <= 0) continue; const yy0 = -200 + hash01(i, 5) * 300; const slide = hash01(i, 7) > 0.7 ? ((t * 0.25 + hash01(i, 9)) % 1) * 120 * k : 0; const yy = Math.min(110, yy0 + slide); const half = 80 - (yy + 220) / 340 * 12; const xx = (hash01(i, 11) * 2 - 1) * half * 0.92; drop(ctx, xx, yy, (4 + hash01(i, 13) * 7) * k, 'rgba(180,215,240,0.95)'); }
  ctx.restore();
}
