// "Kenapa Indonesia punya 3 zona waktu?": pure function of time. window.seek(t) paints frame t.
// Times in SECONDS (1 beat = 0.5 s at 120 bpm); HITS in beats (t * 2). VO: audio/vo.wav (ElevenLabs).
import * as M from './lib/motion.js';

const { W, H, E, prog, lerp, clamp, spring, SPRING, wobble, font, layout, glyph, text, fill, rrect, mix } = M;
const C = { forest: '#1d4138', deep: '#162923', f6: '#244e43', f5: '#396957', f4: '#628775', f2: '#cadcd0', clay: '#e0794f', clay6: '#983f29', sand: '#f7f1e8', sand2: '#ded0ba', white: '#fffefa', night: '#0e1d18' };
const D = 'Display', UI = 'UI';
const sp = (t, t0, cfg = SPRING.snappy) => spring(t - t0, cfg);
const P = (t, a, b) => prog(t, a, b);
const ease = (t, a, b, f = E.outCubic) => f(P(t, a, b));
const logLerp = (a, b, p) => a * (b / a) ** p;
const S = (t) => +(t * 2).toFixed(3);

const HITS = [
  [S(0), 'clocks', 'impact'], [S(0.3), 'clock 2', 'pop', { pitch: 'A5' }], [S(0.6), 'clock 3', 'pop', { pitch: 'D6' }],
  [S(2.4), '3 zona waktu', 'thud'], [S(4.2), 'clocks out', 'whoosh', { len: 0.5 }], [S(5.2), 'garis bujur', 'riser', { len: 0.8 }],
  [S(6.85), '360 counter', 'type', { n: 10, len: 1.2 }], [S(8.6), '24 jam', 'thud'],
  [S(12.1), '15 wedge', 'whoosh', { len: 0.4, from: 500, to: 2600 }], [S(15.8), '1 jam', 'bell', { pitch: 'D6' }],
  [S(16.85), '1 derajat', 'blip', { pitch: 'A5' }], [S(17.9), '4 menit', 'blip', { pitch: 'D6' }],
  [S(18.7), 'to map', 'whoosh', { len: 0.6 }], [S(20.6), '95', 'pop', { pitch: 'F#5' }], [S(23.6), '141', 'pop', { pitch: 'A5' }],
  [S(25.8), 'ruler', 'riser', { len: 1.2 }], [S(27.2), '46', 'thud'], [S(28.62), '3 jam', 'impact'],
  [S(33.3), 'WIB', 'pop', { pitch: 'D5' }], [S(37.43), 'WITA', 'pop', { pitch: 'F#5' }], [S(38.91), 'WIT', 'pop', { pitch: 'A5' }],
  [S(41.8), 'quiz', 'impact'], [S(43.3), 'jakarta pin', 'tick'], [S(46.5), 'jayapura pin', 'tick'],
  [S(47.2), 'count 3', 'tok', { pitch: 'A4' }], [S(48.2), 'count 2', 'tok', { pitch: 'A4' }], [S(49.2), 'count 1', 'tok', { pitch: 'A4' }],
  [S(50.3), 'answer', 'bell', { pitch: 'A6' }], [S(50.5), 'answer arc', 'whoosh', { len: 0.5 }],
  [S(52.2), 'cta', 'whoosh', { len: 0.5 }], [S(53.8), 'OSN Geografi', 'thud'], [S(57.5), 'url', 'bell', { pitch: 'D6' }],
];

let GEO = null, CAP = [];
const RINGS = []; for (let r = 80; r < 2300; r += 70) RINGS.push(r);

// ------------------------------------------------------------------ helpers
function contours(ctx, t, color, alpha, cx, cy, seed = 0) {
  ctx.save(); ctx.strokeStyle = color; ctx.globalAlpha = alpha; ctx.lineWidth = 2;
  for (const r0 of RINGS) {
    const r = r0 + (t * 6) % 70;
    ctx.beginPath();
    for (let k = 0; k <= 72; k++) { const a = k / 72 * M.TAU, kk = 1 + 0.12 * Math.sin(a * 2 + r / 300 + seed + t * 0.15) + 0.06 * Math.sin(a * 3 + 1.3 + seed); const x = cx + Math.cos(a) * r * kk * 1.1, y = cy + Math.sin(a) * r * kk; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.stroke();
  }
  ctx.restore();
}
function shadow(ctx, a = 0.35, blur = 40, oy = 18) { ctx.shadowColor = `rgba(8,18,14,${a})`; ctx.shadowBlur = blur; ctx.shadowOffsetY = oy; }
function noShadow(ctx) { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }

function springLine(ctx, str, x, y, size, weight, fam, color, t, t0, { align = 'left', stagger = 0.022, from = 90, cfg = SPRING.bouncy, track = -0.035, out = null, accentFrom = -1, accent = C.clay } = {}) {
  const f = font(size, weight, fam), L = layout(ctx, str, f, track * size);
  const x0 = align === 'center' ? x - L.width / 2 : align === 'right' ? x - L.width : x;
  L.glyphs.forEach((g, j) => {
    const k = sp(t, t0 + j * stagger, cfg);
    if (k <= 0.001) return;
    const o = out ? E.inBack(P(t, out + j * 0.012, out + 0.35 + j * 0.012), 1.6) : 0;
    glyph(ctx, g.ch, x0 + g.cx, y + (1 - k) * from - o * 1600, f, accentFrom >= 0 && j >= accentFrom ? accent : color, Math.min(1, k), k);
  });
  return L.width;
}
function pill(ctx, str, cx, cy, size, bg, fg, k = 1, rot = 0) {
  if (k <= 0.001) return;
  ctx.font = font(size, 800, UI);
  const w = ctx.measureText(str).width + size * 1.8, h = size * 1.9;
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot * Math.PI / 180); ctx.scale(k, k);
  shadow(ctx, 0.25, 24, 10); rrect(ctx, -w / 2, -h / 2, w, h, h / 2); ctx.fillStyle = bg; ctx.fill(); noShadow(ctx);
  ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(str, 0, size * 0.04); ctx.textBaseline = 'alphabetic';
  ctx.restore();
}

// analog clock; time in hours (decimal); sec hand spins with t
function clock(ctx, x, y, r, hours, t, k = 1, label = '', accent = C.clay) {
  if (k <= 0.001) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
  shadow(ctx, 0.35, 30, 14); ctx.beginPath(); ctx.arc(0, 0, r, 0, M.TAU); ctx.fillStyle = C.white; ctx.fill(); noShadow(ctx);
  ctx.lineWidth = r * 0.06; ctx.strokeStyle = C.deep; ctx.stroke();
  for (let i = 0; i < 12; i++) { const a = i / 12 * M.TAU; ctx.beginPath(); ctx.moveTo(Math.sin(a) * r * 0.78, -Math.cos(a) * r * 0.78); ctx.lineTo(Math.sin(a) * r * (i % 3 ? 0.86 : 0.9), -Math.cos(a) * r * (i % 3 ? 0.86 : 0.9)); ctx.lineWidth = r * (i % 3 ? 0.025 : 0.05); ctx.stroke(); }
  const hand = (a, len, w, col) => { ctx.save(); ctx.rotate(a); ctx.beginPath(); ctx.moveTo(0, r * 0.12); ctx.lineTo(0, -len); ctx.lineCap = 'round'; ctx.lineWidth = w; ctx.strokeStyle = col; ctx.stroke(); ctx.restore(); };
  hand((hours % 12) / 12 * M.TAU, r * 0.5, r * 0.09, C.deep);
  hand((hours % 1) * M.TAU, r * 0.72, r * 0.06, C.deep);
  hand(t * M.TAU / 4, r * 0.78, r * 0.025, accent);
  ctx.beginPath(); ctx.arc(0, 0, r * 0.07, 0, M.TAU); ctx.fillStyle = accent; ctx.fill();
  if (label) text(ctx, label, 0, r + r * 0.42, font(r * 0.32, 800, UI), C.white, 'center');
  ctx.restore();
}

// orthographic globe with a day side (sun to the right) and longitude highlight
function globe(ctx, cx, cy, R, lon0, { alpha = 1, wedge = null, sweep = null } = {}) {
  if (R < 2 || alpha <= 0) return;
  const l0 = lon0 * Math.PI / 180, p0 = -0.12, s0 = Math.sin(p0), c0 = Math.cos(p0);
  const proj = (lon, lat) => { const l = lon * Math.PI / 180, p = lat * Math.PI / 180, cp = Math.cos(p), spp = Math.sin(p), dl = l - l0; return [cx + R * cp * Math.sin(dl), cy - R * (c0 * spp - s0 * cp * Math.cos(dl)), s0 * spp + c0 * cp * Math.cos(dl)]; };
  ctx.save(); ctx.globalAlpha = alpha;
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.fillStyle = C.f6; ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.clip();
  ctx.lineWidth = Math.max(1, R / 170);
  for (const ring of GEO.land) {
    const pts = ring.map(([a, b]) => proj(a, b)); const vis = pts.filter((q) => q[2] > 0).length; if (!vis) continue;
    if (vis === pts.length) { ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); ctx.fillStyle = C.f4; ctx.fill(); }
    ctx.strokeStyle = C.f2; ctx.beginPath(); let on = false; for (const [x, y, c] of pts) { if (c > 0) { on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true } else on = false } ctx.stroke();
  }
  const meridian = (lon, col, w) => { ctx.strokeStyle = col; ctx.lineWidth = w; ctx.beginPath(); let on = false; for (let lat = -90; lat <= 90; lat += 3) { const [x, y, c] = proj(lon, lat); if (c > 0) { on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true } else on = false } ctx.stroke(); };
  for (let lon = -180; lon < 180; lon += 15) meridian(lon, 'rgba(255,254,250,0.22)', Math.max(1, R / 200));
  if (wedge) {
    const [a, b, k] = wedge;
    ctx.beginPath(); let first = true;
    for (let lat = -88; lat <= 88; lat += 4) { const [x, y] = proj(a, lat); first ? ctx.moveTo(x, y) : ctx.lineTo(x, y); first = false; }
    for (let lat = 88; lat >= -88; lat -= 4) { const [x, y] = proj(a + (b - a) * k, lat); ctx.lineTo(x, y); }
    ctx.closePath(); ctx.fillStyle = 'rgba(224,121,79,0.55)'; ctx.fill();
    meridian(a, C.clay, R / 70); meridian(a + (b - a) * k, C.clay, R / 70);
  }
  if (sweep !== null) meridian(sweep, C.clay, R / 60);
  // night side (sun to the right)
  const g = ctx.createLinearGradient(cx - R, 0, cx + R * 0.25, 0);
  g.addColorStop(0, 'rgba(8,16,13,0.78)'); g.addColorStop(0.55, 'rgba(8,16,13,0.6)'); g.addColorStop(0.8, 'rgba(8,16,13,0)');
  ctx.fillStyle = g; ctx.fillRect(cx - R, cy - R, R * 2, R * 2);
  ctx.restore();
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.strokeStyle = 'rgba(255,254,250,0.4)'; ctx.lineWidth = Math.max(2, R / 100); ctx.stroke();
  ctx.restore();
}

// Indonesia mercator map
const MAP = { lonA: 94, lonB: 142, cx: 540, cy: 900, w: 880 };
const merc = (la) => Math.log(Math.tan(Math.PI / 4 + la * Math.PI / 360));
function mp(lo, la, m = MAP) { const s = m.w / (m.lonB - m.lonA); return [m.cx + (lo - (m.lonA + m.lonB) / 2) * s, m.cy - (merc(la) - merc(-2.5)) * s * 180 / Math.PI]; }
function mapPath(ctx, ring, m) { ctx.beginPath(); ring.forEach(([lo, la], i) => { const [x, y] = mp(lo, la, m); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); }
// stylised zone borders (lon/lat), WIB|WITA and WITA|WIT
const B1 = [[114.45, 12], [114.2, 1.6], [114.8, 0.4], [115.5, -2.2], [114.45, -4.2], [114.45, -14]];
const B2 = [[127.3, 12], [127.3, 3], [126.2, 2], [125.6, 0.5], [124.2, -1.6], [124.6, -3.6], [125.6, -7], [125.4, -14]];
const ZONES = [
  { name: 'WIB', utc: 'UTC+7', mer: 105, poly: [[80, 12], ...B1, [80, -14]], col: '#8fbfa6', h: 7 },
  { name: 'WITA', utc: 'UTC+8', mer: 120, poly: [...B1, ...B2.slice().reverse()], col: '#e0a06f', h: 8 },
  { name: 'WIT', utc: 'UTC+9', mer: 135, poly: [...B2, [150, -14], [150, 12]], col: '#e0794f', h: 9 },
];
function indonesiaMap(ctx, t, m, { lw = 3, stroke = C.f2, fillCol = 'rgba(98,135,117,0.6)', draw = 1, zones = [0, 0, 0] } = {}) {
  ctx.save(); ctx.lineJoin = 'round';
  for (const ring of GEO.indonesia) {
    const n = Math.max(2, Math.floor(ring.length * clamp(draw)));
    if (draw >= 1) { mapPath(ctx, ring, m); ctx.fillStyle = fillCol; ctx.fill(); }
    ctx.beginPath(); for (let i = 0; i < n; i++) { const [x, y] = mp(ring[i][0], ring[i][1], m); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke();
  }
  ZONES.forEach((z, i) => {
    const k = zones[i]; if (k <= 0) return;
    ctx.save();
    ctx.beginPath(); z.poly.forEach(([lo, la], j) => { const [x, y] = mp(lo, la, m); j ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); ctx.clip();
    ctx.globalAlpha = k;
    for (const ring of GEO.indonesia) { mapPath(ctx, ring, m); ctx.fillStyle = z.col; ctx.fill(); ctx.strokeStyle = C.white; ctx.lineWidth = lw * 0.6; ctx.stroke(); }
    ctx.restore();
  });
  ctx.restore();
}

function logoMark(ctx, cx, cy, s, needleRot = 0) {
  ctx.save(); ctx.translate(cx, cy); ctx.scale(s / 64, s / 64); ctx.translate(-32, -32);
  rrect(ctx, 0, 0, 64, 64, 15); ctx.fillStyle = C.forest; ctx.fill();
  ctx.strokeStyle = 'rgba(255,254,250,0.25)'; ctx.lineWidth = 1.5; rrect(ctx, 0.75, 0.75, 62.5, 62.5, 14.5); ctx.stroke();
  ctx.lineCap = 'round'; ctx.strokeStyle = C.white;
  ctx.globalAlpha = 0.45; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.moveTo(14.6, 32); ctx.lineTo(49.4, 32); ctx.moveTo(32, 14.6); ctx.bezierCurveTo(26.8, 19.2, 24.2, 25, 24.2, 32); ctx.bezierCurveTo(24.2, 39, 26.8, 44.8, 32, 49.4); ctx.stroke();
  ctx.globalAlpha = 1; ctx.lineWidth = 3.6; ctx.beginPath(); ctx.arc(32, 32, 17.4, -0.29 * Math.PI, 1.96 * Math.PI * 0.86 - 0.29 * Math.PI + 0.3); ctx.stroke();
  ctx.translate(32, 32); ctx.rotate(needleRot);
  ctx.beginPath(); ctx.moveTo(19.5, -19.5); ctx.lineTo(3.4, 3.4); ctx.lineTo(-3.4, -3.4); ctx.closePath(); ctx.fillStyle = C.clay; ctx.fill();
  ctx.beginPath(); ctx.moveTo(-19.5, 19.5); ctx.lineTo(-3.4, -3.4); ctx.lineTo(3.4, 3.4); ctx.closePath(); ctx.fillStyle = C.white; ctx.fill();
  ctx.beginPath(); ctx.arc(0, 0, 2.4, 0, M.TAU); ctx.fillStyle = C.forest; ctx.fill();
  ctx.restore();
}

const KEYS = /(tiga zona waktu|garis bujur|15 derajat|satu jam|empat menit|46 derajat|tiga jam|WIB|WITA|WIT|Jayapura|Jakarta|OSN Geografi|OSNGEO\.id)/;
function captions(ctx, t) {
  const cur = CAP.filter(([, a, b]) => t >= a - 0.05 && t < b + 0.25).pop();
  if (!cur) return;
  const [str, a] = cur, k = sp(t, a - 0.05, SPRING.snappy);
  ctx.font = font(40, 700, UI);
  const w = ctx.measureText(str).width + 56, h = 70;
  ctx.save(); ctx.translate(W / 2, 1440); ctx.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k); ctx.globalAlpha = Math.min(1, k * 1.4);
  rrect(ctx, -w / 2, -h / 2, w, h, 18); ctx.fillStyle = 'rgba(14,26,21,0.85)'; ctx.fill();
  const mm = str.match(KEYS), parts = mm ? [str.slice(0, mm.index), mm[0], str.slice(mm.index + mm[0].length)] : [str, '', ''];
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left'; let x = -w / 2 + 28;
  parts.forEach((p, i) => { if (!p) return; ctx.fillStyle = i === 1 ? C.clay : C.white; ctx.fillText(p, x, 2); x += ctx.measureText(p).width; });
  ctx.restore();
}

// ------------------------------------------------------------------ scenes
function sHook(ctx, t) {
  fill(ctx, C.forest); contours(ctx, t, C.white, 0.06, 900, 300);
  const out = 4.15;
  springLine(ctx, 'Kenapa Indonesia', 80, 360, 76, 800, UI, C.white, t, -0.2, { out });
  springLine(ctx, 'punya', 80, 470, 76, 800, UI, C.white, t, 1.25, { out });
  ctx.save(); M.shake(ctx, S(t), S(2.4), 18, 5, 0.25);
  const f = font(170, 400, D), L = layout(ctx, '3 zona waktu?', f, -3);
  L.glyphs.forEach((g, j) => { const k = sp(t, 2.3 + j * 0.02, SPRING.bouncy); if (k <= 0.001) return; const o = E.inBack(P(t, out, out + 0.35), 1.6); glyph(ctx, g.ch, 74 + g.cx, 640 - (1 - k) * 220 - o * 1600, f, C.clay, 1 + (1 - k) * 0.6, k); });
  ctx.restore();
  // three clocks
  ZONES.forEach((z, i) => {
    const k = sp(t, -0.2 + i * 0.3, SPRING.bouncy), o = E.inBack(P(t, out + 0.06 * i, out + 0.45 + 0.06 * i), 1.5);
    const x = 200 + i * 340, y = 1000 + o * 1200 + 14 * Math.sin(t * 3 + i);
    clock(ctx, x, y, 120, z.h + (t * 0.02), t, k, z.name);
  });
  // garis bujur reveal
  if (t > 4.2) {
    const gk = sp(t, 4.3, SPRING.gentle);
    globe(ctx, 540, lerp(1900, 1000, gk), 360, 40 + t * 12, { sweep: t > 5.2 ? ((t - 5.2) * 120) % 360 - 180 : null });
    springLine(ctx, 'Jawabannya ada di', 80, 380, 64, 800, UI, C.white, t, 4.3);
    springLine(ctx, 'garis bujur.', 80, 540, 150, 400, D, C.clay, t, 5.15, { track: -0.01 });
  }
}

function sGlobe(ctx, t) {
  fill(ctx, C.forest); contours(ctx, t, C.white, 0.05, 200, 1600, 2);
  const lon = 40 + t * 12;
  const wk = ease(t, 12.2, 13.6, E.inOutCubic);
  const wedgeA = 40 + 12.1 * 12 - 4;
  const gR = lerp(360, 330, ease(t, 6.7, 7.5));
  globe(ctx, 540, lerp(1000, 980, ease(t, 6.7, 7.5)), gR, lon, { wedge: t > 12.1 ? [wedgeA, wedgeA + 15, wk] : null });
  // 360° / 24 jam
  const out = 12.0;
  const n = Math.round(360 * E.outCubic(P(t, 6.9, 8.4)));
  const k1 = sp(t, 6.8, SPRING.bouncy) * (1 - E.inBack(P(t, out, out + 0.3)));
  if (k1 > 0.001) { ctx.save(); ctx.translate(80, 420); ctx.scale(k1, k1); text(ctx, n + '°', 0, 0, font(170, 800, UI), C.clay, 'left', -6); ctx.restore(); }
  const k2 = sp(t, 8.5, SPRING.bouncy) * (1 - E.inBack(P(t, out, out + 0.3)));
  if (k2 > 0.001) { ctx.save(); ctx.translate(640, 420); ctx.scale(k2, k2); text(ctx, '= 24 jam', 0, 0, font(96, 800, UI), C.white, 'left', -3); ctx.restore(); }
  // 15° = 1 jam
  const k3 = sp(t, 12.1, SPRING.bouncy);
  if (k3 > 0.001) {
    ctx.save(); ctx.translate(540, 330); ctx.scale(k3, k3);
    text(ctx, '360° ÷ 24 =', 0, 0, font(64, 800, UI), C.white, 'center', -2);
    ctx.restore();
    const k4 = sp(t, 13.2, SPRING.bouncy);
    if (k4 > 0.001) { ctx.save(); ctx.translate(540, 500); ctx.scale(k4, k4); M.shake(ctx, S(t), S(15.8), 10, 3, 0.2); text(ctx, '15° = 1 jam', 0, 0, font(150, 400, D), C.clay, 'center', -2); ctx.restore(); }
  }
  // 1° = 4 menit
  const k5 = sp(t, 16.85, SPRING.bouncy);
  pill(ctx, '1° = 4 menit', 540, 1300, 52, C.clay, C.deep, k5, -3);
}

const M_A = { ...MAP }, M_Z = { ...MAP, cy: 860 };
function sIndo(ctx, t) {
  fill(ctx, C.sand); contours(ctx, t, C.forest, 0.07, 150, 1500, 6);
  const draw = P(t, 18.8, 20.6);
  const m = { ...MAP, cy: 880 };
  indonesiaMap(ctx, t, m, { draw, stroke: C.forest, fillCol: 'rgba(57,105,87,0.45)' });
  springLine(ctx, 'Indonesia membentang', 72, 360, 62, 800, UI, C.deep, t, 18.75);
  // meridian ticks
  const ruler = (lon, t0, label) => {
    const k = sp(t, t0, SPRING.bouncy); if (k <= 0.001) return;
    const [x] = mp(lon, 0, m);
    ctx.save(); ctx.strokeStyle = C.clay6; ctx.lineWidth = 5; ctx.setLineDash([14, 10]);
    ctx.beginPath(); ctx.moveTo(x, 620); ctx.lineTo(x, 620 + 560 * k); ctx.stroke(); ctx.setLineDash([]);
    pill(ctx, label, x, 590, 38, C.clay6, C.white, k);
    ctx.restore();
  };
  ruler(95, 20.4, '95° BT'); ruler(141, 23.4, '141° BT');
  // bracket 95 -> 141 with degree counter
  const bk = ease(t, 25.8, 27.2, E.inOutCubic);
  if (bk > 0) {
    const [xa] = mp(95, 0, m), [xb] = mp(141, 0, m), xe = lerp(xa, xb, bk), y = 1150;
    ctx.save(); ctx.strokeStyle = C.deep; ctx.lineWidth = 6; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(xa, y - 24); ctx.lineTo(xa, y); ctx.lineTo(xe, y); ctx.lineTo(xe, y - 24); ctx.stroke(); ctx.restore();
    const n = Math.round(46 * bk), kk = 1 + 0.15 * wobble(t - 27.2, 2.5, 5);
    ctx.save(); ctx.translate((xa + xe) / 2, 1260); ctx.scale(kk, kk); text(ctx, n + '°', 0, 0, font(110, 800, UI), C.deep, 'center', -4); ctx.restore();
  }
  const hk = sp(t, 28.6, SPRING.bouncy);
  if (hk > 0.001) { ctx.save(); ctx.translate(540, 480); ctx.scale(hk, hk); M.shake(ctx, S(t), S(28.62), 12, 4, 0.2); text(ctx, '≈ 3 jam!', 0, 0, font(150, 400, D), C.clay6, 'center', -2); ctx.restore(); }
}

function sZona(ctx, t) {
  fill(ctx, C.forest); contours(ctx, t, C.white, 0.05, 900, 300, 9);
  const m = M_Z;
  const zk = [ease(t, 33.3, 33.8), ease(t, 37.4, 37.9), ease(t, 38.9, 39.4)];
  indonesiaMap(ctx, t, m, { stroke: C.f2, fillCol: 'rgba(98,135,117,0.55)', zones: zk });
  springLine(ctx, 'Makanya dibagi', 72, 360, 62, 800, UI, C.white, t, 30.4);
  springLine(ctx, 'tiga.', 560, 370, 150, 400, D, C.clay, t, 31.0, { track: -0.01 });
  const t0s = [33.3, 37.4, 38.9];
  ZONES.forEach((z, i) => {
    const k = sp(t, t0s[i], SPRING.bouncy); if (k <= 0.001) return;
    const [x] = mp(z.mer, 0, m);
    ctx.save(); ctx.strokeStyle = C.white; ctx.lineWidth = 4; ctx.setLineDash([12, 9]); ctx.beginPath(); ctx.moveTo(x, 560); ctx.lineTo(x, 560 + 540 * k); ctx.stroke(); ctx.setLineDash([]); ctx.restore();
    const cx = 200 + i * 340;
    clock(ctx, cx, 1240, 78, z.h + t * 0.01, t, k, '', C.clay);
    ctx.save(); ctx.globalAlpha = Math.min(1, k);
    ctx.restore();
    pill(ctx, `${z.name} · ${z.mer}°BT`, x, 530, 32, z.col, C.deep, k);
    pill(ctx, `${z.utc}`, cx, 1360, 30, C.white, C.deep, k);
  });
}

const JKT = [106.85, -6.2], JYP = [140.72, -2.53];
function sQuiz(ctx, t) {
  fill(ctx, C.sand); contours(ctx, t, C.forest, 0.07, 900, 1500, 11);
  const m = { ...MAP, cy: 860 };
  indonesiaMap(ctx, t, m, { stroke: C.forest, fillCol: 'rgba(57,105,87,0.4)', zones: [0.55, 0.55, 0.55] });
  springLine(ctx, 'Coba jawab!', 72, 380, 120, 400, D, C.clay6, t, 41.75, { track: -0.01 });
  const pin = (ll, t0, label, hour, q) => {
    const k = sp(t, t0, SPRING.bouncy); if (k <= 0.001) return;
    const [x, y] = mp(ll[0], ll[1], m);
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
    ctx.beginPath(); ctx.arc(0, 0, 16, 0, M.TAU); ctx.fillStyle = C.clay6; ctx.fill(); ctx.lineWidth = 5; ctx.strokeStyle = C.white; ctx.stroke();
    ctx.restore();
    pill(ctx, label, Math.min(x, 940), y + 60, 30, C.deep, C.white, k);
    const cx = x < 540 ? 230 : 850;
    if (q) {
      const ans = ease(t, 50.3, 50.5);
      clock(ctx, cx, 1180, 100, lerp(7, 9, E.outBack(P(t, 50.3, 51.2))) , t, k, '', C.clay);
      pill(ctx, ans > 0.5 ? '09.00 WIT' : '?? WIT', cx, 1340, 40, ans > 0.5 ? C.clay : C.deep, ans > 0.5 ? C.deep : C.white, k * (1 + 0.2 * wobble(t - 50.3, 2.5, 4)));
    } else {
      clock(ctx, cx, 1180, 100, hour, t, k, '', C.clay);
      pill(ctx, '07.00 WIB', cx, 1340, 40, C.forest, C.white, k);
    }
  };
  pin(JKT, 43.3, 'Jakarta', 7, false);
  pin(JYP, 46.5, 'Jayapura', 7, true);
  // countdown
  [47.2, 48.2, 49.2].forEach((t0, i) => {
    const p = P(t, t0, t0 + 0.95); if (p <= 0 || p >= 1) return;
    const k = 1 + 0.5 * (1 - E.outCubic(Math.min(1, p * 3)));
    ctx.save(); ctx.globalAlpha = 1 - E.inCubic(p); ctx.translate(540, 1180); ctx.scale(k, k);
    text(ctx, String(3 - i), 0, 50, font(160, 800, UI), C.clay6, 'center'); ctx.restore();
  });
  // answer arc +2 jam
  const ak = ease(t, 50.5, 51.3, E.inOutCubic);
  if (ak > 0) {
    const [xa, ya] = mp(...JKT, m), [xb, yb] = mp(...JYP, m), mx = (xa + xb) / 2, my = Math.min(ya, yb) - 260;
    ctx.save(); ctx.strokeStyle = C.clay6; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.beginPath();
    for (let i = 0; i <= 40 * ak; i++) { const q = i / 40, x = (1 - q) ** 2 * xa + 2 * (1 - q) * q * mx + q * q * xb, y = (1 - q) ** 2 * ya + 2 * (1 - q) * q * my + q * q * yb; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.stroke(); ctx.restore();
    pill(ctx, '+2 jam', mx, my + 40, 46, C.clay, C.deep, sp(t, 50.9, SPRING.bouncy), -4);
    const na = ease(t, 51.2, 51.6);
    if (na > 0) { ctx.globalAlpha = na; text(ctx, 'WIB = UTC+7  ·  WIT = UTC+9', 540, 500, font(38, 700, UI), C.f5, 'center'); ctx.globalAlpha = 1; }
  }
}

function sCta(ctx, t) {
  fill(ctx, C.forest); contours(ctx, t, C.white, 0.06, 540, 960, 14);
  globe(ctx, 540, 1150, 520, 60 + t * 12, { alpha: 0.35 });
  const o1 = 56.0;
  springLine(ctx, 'Soal kayak gini', 80, 420, 72, 800, UI, C.white, t, 52.25, { out: o1 });
  springLine(ctx, 'sering keluar di', 80, 530, 72, 800, UI, C.white, t, 52.9, { out: o1 });
  ctx.save(); M.shake(ctx, S(t), S(53.8), 14, 4, 0.2);
  springLine(ctx, 'OSN Geografi.', 74, 720, 170, 400, D, C.clay, t, 53.7, { out: o1, track: -0.01 });
  ctx.restore();
  if (t > 56.1) {
    const lk = sp(t, 56.2, SPRING.bouncy);
    ctx.save(); ctx.translate(540, 560); ctx.scale(lk, lk); logoMark(ctx, 0, 0, 200, (1 - sp(t, 56.3, SPRING.wobbly)) * 6); ctx.restore();
    springLine(ctx, 'Latihan soal lainnya', W / 2, 820, 64, 800, UI, C.white, t, 56.3, { align: 'center' });
    pill(ctx, 'osngeo.id', W / 2, 980, 76, C.clay, C.deep, sp(t, 57.45, SPRING.bouncy));
  }
}

function whip(ctx, t, a, b, A, B) {
  const p = E.inOutCubic(P(t, a, b));
  ctx.save(); ctx.translate(-p * W, 0); A(ctx); ctx.restore();
  ctx.save(); ctx.translate((1 - p) * W, 0); B(ctx); ctx.restore();
}
function circleWipe(ctx, t, a, b, A, B) {
  A(ctx); const p = E.inOutCubic(P(t, a, b));
  ctx.save(); ctx.beginPath(); ctx.arc(W / 2, H / 2, logLerp(10, 1300, p), 0, M.TAU); ctx.clip(); B(ctx); ctx.restore();
}

function draw(ctx, u, t) {
  if (t < 6.55) sHook(ctx, t);
  else if (t < 6.9) { sGlobe(ctx, t); ctx.save(); ctx.globalAlpha = 1 - ease(t, 6.55, 6.9); sHook(ctx, t); ctx.restore(); }
  else if (t < 18.55) sGlobe(ctx, t);
  else if (t < 19.0) circleWipe(ctx, t, 18.55, 19.0, (c) => sGlobe(c, t), (c) => sIndo(c, t));
  else if (t < 30.2) sIndo(ctx, t);
  else if (t < 30.6) whip(ctx, t, 30.2, 30.6, (c) => sIndo(c, t), (c) => sZona(c, t));
  else if (t < 41.5) sZona(ctx, t);
  else if (t < 41.9) whip(ctx, t, 41.5, 41.9, (c) => sZona(c, t), (c) => sQuiz(c, t));
  else if (t < 52.0) sQuiz(ctx, t);
  else if (t < 52.4) circleWipe(ctx, t, 52.0, 52.4, (c) => sQuiz(c, t), (c) => sCta(c, t));
  else sCta(ctx, t);
  if (t < 55.9) captions(ctx, t);
}

M.film({
  fonts: [font(100, 800, UI), font(100, 400, D), font(40, 700, UI)],
  images: {},
  hits: HITS,
  samples: 8,
  async init() {
    GEO = await fetch('assets/geo.json').then((r) => r.json());
    const tm = await fetch('docs/timing.json').then((r) => r.json());
    const out = [];
    for (const [s, a, b] of tm.display) {
      const last = out[out.length - 1];
      if (last && (last[0].split(' ').length <= 1) && (last[0] + ' ' + s).length < 40) { last[0] += ' ' + s; last[2] = b; } else out.push([s, a, b]);
    }
    for (const [s, a, b] of out) {
      if (s.length <= 30) { CAP.push([s, a, b]); continue; }
      const w = s.split(' '), n = Math.ceil(s.length / 30), per = Math.ceil(w.length / n), ch = [];
      for (let i = 0; i < w.length; i += per) ch.push(w.slice(i, i + per).join(' '));
      const tot = ch.reduce((q, c) => q + c.length, 0); let tt = a;
      for (const c of ch) { const d = (b - a) * c.length / tot; CAP.push([c, tt, tt + d]); tt += d; }
    }
  },
  draw,
});
