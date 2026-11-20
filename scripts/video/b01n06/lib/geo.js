// OSNGEO.id geo kit: pressure fields, isobars (marching squares), wind particles, paper-cut maps, orthographic 3-D globe.
import * as M from './motion.js';
import { C, fU, circle, poly, pill } from './common.js';
const { lerp, clamp, hash01, text, mix } = M;
export const D2R = Math.PI / 180;

// ---------------------------------------------------------------- pressure field = base + sum of gaussians [lon, lat, A, sx, sy]
export function field(centers, base = 1010) {
  const P = (lo, la) => { let p = base; for (const [x, y, A, sx, sy] of centers) p += A * Math.exp(-(((lo - x) / sx) ** 2 + ((la - y) / sy) ** 2)); return p; };
  const G = (lo, la) => { let gx = 0, gy = 0; for (const [x, y, A, sx, sy] of centers) { const e = A * Math.exp(-(((lo - x) / sx) ** 2 + ((la - y) / sy) ** 2)); gx += e * (-2 * (lo - x) / (sx * sx)); gy += e * (-2 * (la - y) / (sy * sy)); } return [gx, gy]; };
  return { P, G, centers };
}
export function blend(f1, f2, k) {
  return { P: (a, b) => lerp(f1.P(a, b), f2.P(a, b), k), G: (a, b) => { const g1 = f1.G(a, b), g2 = f2.G(a, b); return [lerp(g1[0], g2[0], k), lerp(g1[1], g2[1], k)]; }, centers: k < 0.5 ? f1.centers : f2.centers };
}
// marching squares -> {level: [[lo1,la1,lo2,la2], ...]}
export function contours(P, ext, step, levels) {
  const [x0, x1, y0, y1] = ext, nx = Math.round((x1 - x0) / step) + 1, ny = Math.round((y1 - y0) / step) + 1;
  const g = new Float32Array(nx * ny);
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) g[j * nx + i] = P(x0 + i * step, y0 + j * step);
  const out = {};
  for (const L of levels) {
    const segs = [];
    for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
      const a = g[j * nx + i], b = g[j * nx + i + 1], c = g[(j + 1) * nx + i + 1], d = g[(j + 1) * nx + i];
      const X = x0 + i * step, Y = y0 + j * step;
      const pts = [];
      const e = (v1, v2, p1, p2) => { if ((v1 < L) !== (v2 < L)) { const k = (L - v1) / (v2 - v1); pts.push([lerp(p1[0], p2[0], k), lerp(p1[1], p2[1], k)]); } };
      e(a, b, [X, Y], [X + step, Y]); e(b, c, [X + step, Y], [X + step, Y + step]); e(c, d, [X + step, Y + step], [X, Y + step]); e(d, a, [X, Y + step], [X, Y]);
      if (pts.length >= 2) segs.push([pts[0][0], pts[0][1], pts[1][0], pts[1][1]]);
      if (pts.length === 4) segs.push([pts[2][0], pts[2][1], pts[3][0], pts[3][1]]);
    }
    out[L] = segs;
  }
  return out;
}
// draw isobars through a projection; reveal: 0..1 sweep west->east; labels at a stable segment
export function drawIsobars(ctx, cs, proj, { color = 'rgba(29,65,56,0.75)', width = 3, reveal = 1, ext = null, labels = true, fs = 20, hi = null } = {}) {
  const cut = ext ? lerp(ext[0], ext[1], reveal) : 1e9;
  for (const L in cs) {
    const segs = cs[L]; ctx.strokeStyle = hi && hi(+L) ? C.clay : color; ctx.lineWidth = width; ctx.lineCap = 'round'; ctx.beginPath();
    let best = null;
    for (const [a, b, c, d] of segs) {
      if (Math.min(a, c) > cut) continue;
      const p = proj(a, b), q = proj(c, d); if (!p || !q) continue;
      ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]);
      if (!best || Math.abs(b - 0) + a * 0.01 < best[2]) best = [p[0], p[1], Math.abs(b - 0) + a * 0.01];
    }
    ctx.stroke();
    if (labels && best && reveal > 0.95) { pill(ctx, `${L}`, best[0], best[1], fU(fs, 700), C.cream, C.forest, 8, fs * 1.6, 'center'); }
  }
}
// H / L badges
export function drawCenters(ctx, centers, proj, k = 1, t = 0, { lang = 'en', minA = 4 } = {}) {
  centers.forEach(([lo, la, A], i) => {
    if (Math.abs(A) < minA) return; const p = proj(lo, la); if (!p) return;
    const s = k * (1 + 0.04 * Math.sin(t * 3 + i)); if (s <= 0.01) return;
    const hiP = A > 0; const r = 34 * s;
    circle(ctx, p[0], p[1], r); ctx.fillStyle = hiP ? C.blue : C.clay; ctx.fill(); ctx.strokeStyle = C.cream; ctx.lineWidth = 4; ctx.stroke();
    const lab = lang === 'id' ? (hiP ? 'T' : 'R') : (hiP ? 'H' : 'L');
    text(ctx, lab, p[0], p[1] + 13 * s, fU(38 * s, 800), C.cream, 'center');
  });
}

// ---------------------------------------------------------------- wind particles (deterministic, pure function of t)
export function seeds(n, ext, salt = 1) { const s = []; for (let i = 0; i < n; i++) s.push([lerp(ext[0], ext[1], hash01(i, salt)), lerp(ext[2], ext[3], hash01(i, salt + 7)), hash01(i, salt + 13)]); return s; }
export function drawFlow(ctx, F, proj, sd, t, { life = 3, speed = 1.2, vmax = 6, steps = 18, color = 'rgba(255,255,255,0.85)', width = 2.4, alpha = 1, rot = null } = {}) {
  ctx.save(); ctx.lineCap = 'round'; ctx.lineWidth = width;
  for (let i = 0; i < sd.length; i++) {
    const [lo0, la0, ph] = sd[i]; const age = ((t / life + ph) % 1) * life;
    let lo = lo0, la = la0; const dt = age / steps; const pts = [];
    for (let k = 0; k <= steps; k++) {
      pts.push([lo, la]); let [gx, gy] = F.G(lo, la); let vx = -gx * speed, vy = -gy * speed;
      if (rot) { const c = Math.cos(rot(la)), s = Math.sin(rot(la)); [vx, vy] = [vx * c - vy * s, vx * s + vy * c]; }
      const m = Math.hypot(vx, vy); if (m > vmax) { vx *= vmax / m; vy *= vmax / m; }
      lo += vx * dt; la += vy * dt;
    }
    const n = pts.length, tail = Math.max(2, Math.floor(n * 0.6)), fadeIn = clamp(age / 0.4), fadeOut = clamp((life - age) / 0.5);
    ctx.globalAlpha = alpha * fadeIn * fadeOut;
    ctx.strokeStyle = color; ctx.beginPath(); let started = false;
    for (let k = n - tail; k < n; k++) { const p = proj(pts[k][0], pts[k][1]); if (!p) { started = false; continue; } if (!started) { ctx.moveTo(p[0], p[1]); started = true; } else ctx.lineTo(p[0], p[1]); }
    ctx.stroke();
  }
  ctx.restore();
}

// ---------------------------------------------------------------- flat map (equirectangular) with paper-cut land
export function mapProj(box, ext) {
  const [x0, x1, y0, y1] = ext; const sx = box.w / (x1 - x0), sy = box.h / (y1 - y0);
  const f = (lo, la) => [box.x + (lo - x0) * sx, box.y + (y1 - la) * sy];
  f.box = box; f.ext = ext; f.k = sx; return f;
}
export function subset(rings, ext, pad = 5) {
  return rings.filter((r) => { let a = 1e9, b = -1e9, c = 1e9, d = -1e9; for (const [x, y] of r) { a = Math.min(a, x); b = Math.max(b, x); c = Math.min(c, y); d = Math.max(d, y); } return b > ext[0] - pad && a < ext[1] + pad && d > ext[2] - pad && c < ext[3] + pad; });
}
export function drawMap(ctx, rings, proj, { sea = '#cfe3ef', land = '#f3e6c4', edge = '#a8916a', shadow = 'rgba(29,65,56,0.22)', t = 0, waves = true, depth = 7 } = {}) {
  const b = proj.box; ctx.save(); M.rrect(ctx, b.x, b.y, b.w, b.h, 26); ctx.clip();
  ctx.fillStyle = sea; ctx.fillRect(b.x, b.y, b.w, b.h);
  if (waves) { ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 2; for (let k = 0; k < 14; k++) { const y = b.y + (k + 0.5) * b.h / 14; ctx.beginPath(); for (let x = b.x; x <= b.x + b.w; x += 20) { const yy = y + 4 * Math.sin(x * 0.02 + t * 0.8 + k); x === b.x ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy); } ctx.stroke(); } }
  const path = () => { ctx.beginPath(); for (const r of rings) { r.forEach(([lo, la], i) => { const [x, y] = proj(lo, la); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); } };
  ctx.save(); ctx.translate(depth * 0.6, depth); path(); ctx.fillStyle = shadow; ctx.fill(); ctx.restore();
  path(); ctx.fillStyle = land; ctx.fill(); ctx.strokeStyle = edge; ctx.lineWidth = 1.4; ctx.stroke();
  ctx.restore();
}
export function graticule(ctx, proj, ext, step = 10, color = 'rgba(29,65,56,0.12)') {
  ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.beginPath();
  for (let lo = Math.ceil(ext[0] / step) * step; lo <= ext[1]; lo += step) { const a = proj(lo, ext[2]), b = proj(lo, ext[3]); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); }
  for (let la = Math.ceil(ext[2] / step) * step; la <= ext[3]; la += step) { const a = proj(ext[0], la), b = proj(ext[1], la); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); }
  ctx.stroke();
}

// ---------------------------------------------------------------- orthographic globe (3-D)
export function globeProj(lon0, lat0, R, cx, cy) {
  const p0 = lat0 * D2R, sp0 = Math.sin(p0), cp0 = Math.cos(p0);
  const raw = (lo, la) => { const l = (lo - lon0) * D2R, p = la * D2R; const cp = Math.cos(p), sp = Math.sin(p), cl = Math.cos(l); const cosc = sp0 * sp + cp0 * cp * cl; return [cx + R * cp * Math.sin(l), cy - R * (cp0 * sp - sp0 * cp * cl), cosc]; };
  const f = (lo, la) => { const r = raw(lo, la); return r[2] < 0 ? null : [r[0], r[1]]; };
  f.raw = raw; f.R = R; f.cx = cx; f.cy = cy; return f;
}
export function drawGlobe(ctx, rings, g, { sea = '#7fb3d5', land = '#f3e6c4', edge = '#a8916a', grid = true, glow = true, shade = true } = {}) {
  const { R, cx, cy } = g;
  if (glow) { const gg = ctx.createRadialGradient(cx, cy, R * 0.95, cx, cy, R * 1.18); gg.addColorStop(0, 'rgba(170,210,240,0.55)'); gg.addColorStop(1, 'rgba(170,210,240,0)'); ctx.fillStyle = gg; circle(ctx, cx, cy, R * 1.18); ctx.fill(); }
  const og = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R); og.addColorStop(0, mix(sea, '#ffffff', 0.25)); og.addColorStop(1, mix(sea, '#0d2c45', 0.35));
  circle(ctx, cx, cy, R); ctx.fillStyle = og; ctx.fill();
  ctx.save(); circle(ctx, cx, cy, R); ctx.clip();
  if (grid) { ctx.strokeStyle = 'rgba(255,255,255,0.18)'; ctx.lineWidth = 1.2; for (let lo = -180; lo < 180; lo += 30) { ctx.beginPath(); let s = false; for (let la = -90; la <= 90; la += 5) { const p = g(lo, la); if (!p) { s = false; continue; } s ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s = true; } ctx.stroke(); } for (let la = -60; la <= 60; la += 30) { ctx.beginPath(); let s = false; for (let lo = -180; lo <= 180; lo += 4) { const p = g(lo, la); if (!p) { s = false; continue; } s ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s = true; } ctx.stroke(); } }
  ctx.beginPath();
  for (const r of rings) {
    let any = false; const pts = r.map(([lo, la]) => { const q = g.raw(lo, la); if (q[2] >= 0) { any = true; return [q[0], q[1]]; } const dx = q[0] - cx, dy = q[1] - cy, m = Math.hypot(dx, dy) || 1; return [cx + dx / m * R, cy + dy / m * R]; });
    if (!any) continue; pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath();
  }
  ctx.fillStyle = land; ctx.fill(); ctx.strokeStyle = edge; ctx.lineWidth = 1.2; ctx.stroke();
  if (shade) { const sg = ctx.createRadialGradient(cx - R * 0.4, cy - R * 0.45, R * 0.2, cx, cy, R * 1.02); sg.addColorStop(0, 'rgba(255,255,255,0.10)'); sg.addColorStop(0.7, 'rgba(0,0,0,0)'); sg.addColorStop(1, 'rgba(10,30,50,0.45)'); ctx.fillStyle = sg; ctx.fillRect(cx - R, cy - R, 2 * R, 2 * R); }
  ctx.restore();
}

// ---------------------------------------------------------------- isometric (3-D diorama) projection with orbiting camera
export function iso(cx, cy, s, az = 0, el = 0.5) {
  const ca = Math.cos(az), sa = Math.sin(az);
  return (x, y, z) => { const X = x * ca - y * sa, Y = x * sa + y * ca; return [cx + (X - Y) * 0.866 * s, cy + (X + Y) * el * s - z * s]; };
}
export function isoBox(ctx, P, x, y, z, w, d, h, top, side1, side2) {
  const q = (a, b, c) => P(a, b, c);
  ctx.fillStyle = side1; poly(ctx, [q(x, y + d, z), q(x + w, y + d, z), q(x + w, y + d, z + h), q(x, y + d, z + h)]); ctx.fill();
  ctx.fillStyle = side2; poly(ctx, [q(x + w, y, z), q(x + w, y + d, z), q(x + w, y + d, z + h), q(x + w, y, z + h)]); ctx.fill();
  ctx.fillStyle = top; poly(ctx, [q(x, y, z + h), q(x + w, y, z + h), q(x + w, y + d, z + h), q(x, y + d, z + h)]); ctx.fill();
}
