// OSNGEO.id Promo v2: pure function of time. window.seek(t) paints frame t.
// Times below are in SECONDS (1 beat = 0.5 s on the 120 bpm grid); HITS are in beats (t * 2).
// docs/shotlist.md is the plan this file follows. Real UI comes only from assets/shots/*.png.
import * as M from './lib/motion.js';

const { W, H, E, prog, lerp, clamp, spring, SPRING, wobble, font, layout, glyph, text, fill, rrect, mix } = M;

const C = { forest: '#1d4138', deep: '#162923', f6: '#244e43', f5: '#396957', f4: '#628775', f2: '#cadcd0', f1: '#e2ede4', clay: '#e0794f', clay6: '#983f29', sand: '#f7f1e8', sand2: '#ded0ba', white: '#fffefa' };
const D = 'Display', UI = 'UI';
const sp = (t, t0, cfg = SPRING.snappy) => spring(t - t0, cfg);
const P = (t, a, b) => prog(t, a, b);
const ease = (t, a, b, f = E.outCubic) => f(P(t, a, b));
const logLerp = (a, b, p) => a * (b / a) ** p;

// ------------------------------------------------------------------ hits (beats = seconds * 2)
const S = (t) => +(t * 2).toFixed(3);
const HITS = [
  [S(0), 'globe + title', 'impact'],
  [S(2.25), 'BERAT slam', 'thud', { pitch: 90, to: 45 }],
  [S(3.58), 'card hafalan', 'pop', { pitch: 'A5' }],
  [S(5.11), 'card abstrak', 'pop', { pitch: 'C#6' }],
  [S(6.47), 'card pusing', 'pop', { pitch: 'E6' }],
  [S(7.9), 'zoom into Indonesia', 'whoosh', { len: 0.9, from: 400, to: 3000 }],
  [S(8.55), 'logo lands', 'bell', { pitch: 'D6' }],
  [S(9.38), 'wordmark', 'type', { n: 9, len: 0.35 }],
  [S(10.5), 'phone rises', 'whoosh', { len: 0.5 }],
  [S(10.9), 'phone lands', 'thud'],
  [S(12.4), 'screen: videos', 'click'],
  [S(13.7), 'card pops out', 'pop', { pitch: 'A5' }],
  [S(14.35), 'tap tonton', 'tick'],
  [S(15.0), 'break out', 'whoosh', { len: 0.6, from: 300, to: 2600 }],
  [S(15.55), 'animation full', 'sub', { len: 0.6 }],
  [S(16.9), 'KELIHATAN', 'impact'],
  [S(18.3), 'monsoon flips', 'whoosh', { len: 0.5, from: 2400, to: 500, pan: -0.3 }],
  [S(18.58), 'chip dipahami', 'blip', { pitch: 'A5' }],
  [S(19.7), 'chip nempel', 'blip', { pitch: 'D6' }],
  [S(20.8), 'wipe to sand', 'whoosh', { len: 0.5 }],
  [S(24.2), '13 counts', 'riser', { len: 1.0 }],
  [S(25.3), '13 lands', 'thud'],
  [S(26.16), 'chip iklim', 'pop', { pitch: 'F#5' }],
  [S(27.14), 'chip bencana', 'pop', { pitch: 'A5' }],
  [S(28.06), 'chip peta', 'pop', { pitch: 'D6' }],
  [S(28.85), 'whip', 'whoosh', { len: 0.4, from: 2400, to: 600 }],
  [S(29.4), 'tiles cascade', 'type', { n: 14, len: 1.2 }],
  [S(30.6), '99 lands', 'thud'],
  [S(31.2), 'tiles light', 'coins'],
  [S(33.4), 'series bar', 'pop', { pitch: 'A5' }],
  [S(33.7), 'GRATIS stamp', 'impact'],
  [S(36.8), 'whip', 'whoosh', { len: 0.4, from: 600, to: 2400, pan: 0.3 }],
  [S(38.22), 'uji pemahaman', 'pop', { pitch: 'E6' }],
  [S(40.18), '35 paket', 'thud'],
  [S(40.9), 'exam screen', 'click'],
  [S(42.2), 'tap answer', 'tick'],
  [S(42.35), 'correct', 'bell', { pitch: 'A6' }],
  [S(43.5), 'results', 'whoosh', { len: 0.4 }],
  [S(43.7), 'score lifts', 'pop', { pitch: 'D6' }],
  [S(44.3), 'pembahasan lifts', 'pop', { pitch: 'F#6' }],
  [S(45.2), 'to chart', 'whoosh', { len: 0.4, from: 500, to: 2600 }],
  [S(45.5), 'chart draws', 'riser', { len: 1.4 }],
  [S(47.0), 'last point', 'blip', { pitch: 'A6' }],
  [S(48.85), 'gampang', 'impact'],
  [S(50.18), 'terarah', 'thud'],
  [S(51.88), 'coba gratis', 'impact'],
  [S(52.3), 'gratis card', 'whoosh', { len: 0.4 }],
  [S(52.9), 'url pill', 'bell', { pitch: 'D6' }],
  [S(55.13), 'link di bio', 'pop', { pitch: 'A5' }],
];

// ------------------------------------------------------------------ data loaded in init
let BOX = null, GEO = null, CAP = [], CONT = [];

// ------------------------------------------------------------------ helpers
function contours(ctx, t, color, alpha, cx = 820, cy = 360, seed = 0) {
  ctx.save(); ctx.strokeStyle = color; ctx.globalAlpha = alpha; ctx.lineWidth = 2;
  const drift = t * 6;
  CONT.forEach((r, i) => {
    ctx.beginPath();
    for (let k = 0; k <= 72; k++) {
      const a = (k / 72) * M.TAU;
      const kk = 1 + 0.12 * Math.sin(a * 2 + r / 300 + seed + t * 0.15) + 0.06 * Math.sin(a * 3 + 1.3 + seed);
      const x = cx + Math.cos(a) * (r + drift % 70) * kk * 1.1, y = cy + Math.sin(a) * (r + drift % 70) * kk;
      k ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.stroke();
  });
  ctx.restore();
}

// orthographic globe of land outlines + graticule
function globe(ctx, cx, cy, R, lon0, lat0, { alpha = 1, line = C.f2, landFill = 'rgba(98,135,117,0.55)', disk = C.f6, grat = true } = {}) {
  if (R < 2 || alpha <= 0) return;
  const l0 = lon0 * Math.PI / 180, p0 = lat0 * Math.PI / 180, s0 = Math.sin(p0), c0 = Math.cos(p0);
  const proj = (lon, lat) => {
    const l = lon * Math.PI / 180, p = lat * Math.PI / 180, cp = Math.cos(p), sp_ = Math.sin(p), dl = l - l0;
    const cosc = s0 * sp_ + c0 * cp * Math.cos(dl);
    return [cx + R * cp * Math.sin(dl), cy - R * (c0 * sp_ - s0 * cp * Math.cos(dl)), cosc];
  };
  ctx.save(); ctx.globalAlpha = alpha;
  const g = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R);
  g.addColorStop(0, mix(disk, '#ffffff', 0.12)); g.addColorStop(1, disk);
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.fillStyle = g; ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.clip();
  ctx.lineWidth = Math.max(1, R / 160);
  if (grat) {
    ctx.strokeStyle = 'rgba(255,254,250,0.13)';
    for (let lon = -180; lon < 180; lon += 20) { ctx.beginPath(); let on = false; for (let lat = -90; lat <= 90; lat += 5) { const [x, y, c] = proj(lon, lat); if (c > 0) { on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true } else on = false } ctx.stroke() }
    for (let lat = -60; lat <= 60; lat += 20) { ctx.beginPath(); let on = false; for (let lon = -180; lon <= 180; lon += 5) { const [x, y, c] = proj(lon, lat); if (c > 0) { on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true } else on = false } ctx.stroke() }
  }
  for (const ring of GEO.land) {
    const pts = ring.map(([lo, la]) => proj(lo, la));
    const vis = pts.filter((p) => p[2] > 0).length;
    if (!vis) continue;
    if (vis === pts.length) { ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); ctx.fillStyle = landFill; ctx.fill(); }
    ctx.strokeStyle = line; ctx.beginPath(); let on = false;
    for (const [x, y, c] of pts) { if (c > 0) { on ? ctx.lineTo(x, y) : ctx.moveTo(x, y); on = true } else on = false }
    ctx.stroke();
  }
  ctx.restore();
  ctx.beginPath(); ctx.arc(cx, cy, R, 0, M.TAU); ctx.strokeStyle = 'rgba(255,254,250,0.35)'; ctx.lineWidth = Math.max(1.5, R / 110); ctx.stroke();
  ctx.restore();
}

// Indonesia (mercator) drawn on progressively
function indonesia(ctx, cx, cy, w, p, { stroke = C.f2, fillA = 0, lw = 3, alpha = 1 } = {}) {
  const lonA = 94.5, lonB = 141.5, sc = w / (lonB - lonA) * 180 / Math.PI;
  const merc = (la) => Math.log(Math.tan(Math.PI / 4 + la * Math.PI / 360));
  const yc = merc(-2.5);
  const pt = ([lo, la]) => [cx + (lo - (lonA + lonB) / 2) / (lonB - lonA) * w, cy - (merc(la) - yc) * sc];
  ctx.save(); ctx.globalAlpha = alpha; ctx.lineWidth = lw; ctx.strokeStyle = stroke; ctx.lineJoin = 'round';
  for (const ring of GEO.indonesia) {
    const n = Math.max(2, Math.floor(ring.length * clamp(p)));
    ctx.beginPath();
    for (let i = 0; i < n; i++) { const [x, y] = pt(ring[i]); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    if (p >= 1) { ctx.closePath(); if (fillA) { ctx.fillStyle = `rgba(98,135,117,${fillA})`; ctx.fill(); } }
    ctx.stroke();
  }
  ctx.restore();
}

function shadow(ctx, a = 0.35, blur = 50, oy = 24) { ctx.shadowColor = `rgba(8,18,14,${a})`; ctx.shadowBlur = blur; ctx.shadowOffsetY = oy; }
function noShadow(ctx) { ctx.shadowColor = 'transparent'; ctx.shadowBlur = 0; ctx.shadowOffsetY = 0; }

// phone with a real screenshot. o: {cx, top, w, img, scroll(css px), rot, scale, img2, swap (0..1 slide), scroll2}
function phone(ctx, IMG, o) {
  const w = o.w, h = w * 844 / 390, pad = w * 0.04, R = w * 0.16;
  ctx.save();
  ctx.translate(o.cx, o.top + h / 2);
  ctx.rotate((o.rot || 0) * Math.PI / 180);
  ctx.scale(o.scale || 1, o.scale || 1);
  if (o.skew) ctx.transform(1, o.skew, 0, 1, 0, 0);
  ctx.translate(-w / 2, -h / 2);
  shadow(ctx, 0.45, 70, 36);
  rrect(ctx, -pad, -pad, w + 2 * pad, h + 2 * pad, R + pad); ctx.fillStyle = '#0d1512'; ctx.fill();
  noShadow(ctx);
  rrect(ctx, -pad + 3, -pad + 3, w + 2 * pad - 6, h + 2 * pad - 6, R + pad - 3); ctx.strokeStyle = '#33453d'; ctx.lineWidth = 3; ctx.stroke();
  ctx.save(); rrect(ctx, 0, 0, w, h, R - pad * 0.6); ctx.clip();
  ctx.fillStyle = C.sand; ctx.fillRect(0, 0, w, h);
  const draw = (img, scroll, dx) => { if (!img) return; const sy = Math.min(scroll * 3, img.height - 2532); ctx.drawImage(img, 0, Math.max(0, sy), 1170, 2532, dx, 0, w, h); };
  const sw = o.swap || 0;
  draw(IMG[o.img], o.scroll || 0, -sw * w * 0.35);
  if (sw > 0 && o.img2) {
    ctx.save(); shadow(ctx, 0.3, 30, 0); ctx.fillStyle = C.sand; ctx.fillRect((1 - sw) * w, 0, w, h); noShadow(ctx); ctx.restore();
    draw(IMG[o.img2], o.scroll2 || 0, (1 - sw) * w);
  }
  if (o.dim) { ctx.fillStyle = `rgba(14,26,21,${o.dim})`; ctx.fillRect(0, 0, w, h); }
  ctx.restore();
  rrect(ctx, w / 2 - w * 0.14, pad * 0.35, w * 0.28, w * 0.075, w * 0.04); ctx.fillStyle = '#0d1512'; ctx.fill();
  ctx.restore();
  return { x: o.cx - w / 2, y: o.top, w, h, s: w / 390 };
}

// map a css point of the phone screen to canvas (no rotation: used where rot ~ 0)
const onPhone = (ph, x, y, scroll = 0) => [ph.x + x * ph.s, ph.y + (y - scroll) * ph.s];

// crop of a screenshot (css box) as a floating card
function card(ctx, img, box, cx, cy, w, { k = 1, rot = 0, radius = 26, alpha = 1, scaleY = 1, glow = 0 } = {}) {
  if (!img || k <= 0.001 || alpha <= 0) return;
  const [bx, by, bw, bh] = box, h = w * bh / bw;
  ctx.save(); ctx.globalAlpha = alpha;
  ctx.translate(cx, cy); ctx.rotate(rot * Math.PI / 180); ctx.scale(k, k * scaleY);
  if (glow) { ctx.save(); rrect(ctx, -w / 2 - 10, -h / 2 - 10, w + 20, h + 20, radius + 10); ctx.fillStyle = `rgba(224,121,79,${0.55 * glow})`; ctx.fill(); ctx.restore(); }
  shadow(ctx, 0.35, 50, 26);
  rrect(ctx, -w / 2, -h / 2, w, h, radius); ctx.fillStyle = C.white; ctx.fill();
  noShadow(ctx);
  ctx.save(); rrect(ctx, -w / 2, -h / 2, w, h, radius); ctx.clip();
  ctx.drawImage(img, bx * 3, by * 3, bw * 3, bh * 3, -w / 2, -h / 2, w, h);
  ctx.restore(); ctx.restore();
  return h;
}

function fingerAt(ctx, x, y, t, tIn, tTap, tOut) {
  const a = ease(t, tIn, tIn + 0.2) * (1 - ease(t, tOut, tOut + 0.2));
  if (a <= 0) return;
  const press = M.bump(t, tTap + 0.06, 0.12);
  const rip = P(t, tTap, tTap + 0.5);
  ctx.save(); ctx.globalAlpha = a;
  if (rip > 0 && rip < 1) { ctx.beginPath(); ctx.arc(x, y, 30 + rip * 90, 0, M.TAU); ctx.strokeStyle = `rgba(255,254,250,${(1 - rip) * 0.9})`; ctx.lineWidth = 6; ctx.stroke(); }
  shadow(ctx, 0.35, 20, 8);
  ctx.beginPath(); ctx.arc(x, y + (1 - a) * 60, 34 * (1 - 0.22 * press), 0, M.TAU); ctx.fillStyle = 'rgba(224,121,79,0.55)'; ctx.fill();
  noShadow(ctx); ctx.lineWidth = 5; ctx.strokeStyle = C.white; ctx.stroke();
  ctx.restore();
}

// per-glyph line that springs in. returns width
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

function pill(ctx, str, cx, cy, size, bg, fg, k = 1, rot = 0, padX = 0.9) {
  if (k <= 0.001) return;
  const f = font(size, 800, UI); ctx.font = f;
  const w = ctx.measureText(str).width + size * padX * 2, h = size * 1.9;
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot * Math.PI / 180); ctx.scale(k, k);
  shadow(ctx, 0.25, 24, 10); rrect(ctx, -w / 2, -h / 2, w, h, h / 2); ctx.fillStyle = bg; ctx.fill(); noShadow(ctx);
  ctx.fillStyle = fg; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(str, 0, size * 0.04);
  ctx.textBaseline = 'alphabetic';
  ctx.restore();
  return w;
}

// small code-drawn icons (stroke, white)
function icon(ctx, kind, x, y, s, t, color = C.white) {
  ctx.save(); ctx.translate(x, y); ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = s * 0.08; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  if (kind === 'books') {
    [[-0.42, 0.18, 0.84, 0.2, -4], [-0.36, -0.06, 0.74, 0.2, 5], [-0.4, -0.3, 0.8, 0.2, -3]].forEach(([a, b, w, h, r], i) => {
      ctx.save(); ctx.rotate(r * Math.PI / 180 + Math.sin(t * 3 + i) * 0.03); rrect(ctx, a * s, b * s, w * s, h * s, s * 0.04); ctx.stroke(); ctx.restore();
    });
  } else if (kind === 'swirl') {
    ctx.rotate(t * 2.2); ctx.beginPath();
    for (let i = 0; i <= 60; i++) { const a = i / 60 * M.TAU * 2.2, r = s * 0.06 + i / 60 * s * 0.4; i ? ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r) : ctx.moveTo(r, 0); }
    ctx.stroke();
  } else if (kind === 'map') {
    ctx.beginPath(); ctx.moveTo(-0.45 * s, -0.3 * s); ctx.lineTo(-0.15 * s, -0.4 * s); ctx.lineTo(0.15 * s, -0.3 * s); ctx.lineTo(0.45 * s, -0.4 * s); ctx.lineTo(0.45 * s, 0.3 * s); ctx.lineTo(0.15 * s, 0.4 * s); ctx.lineTo(-0.15 * s, 0.3 * s); ctx.lineTo(-0.45 * s, 0.4 * s); ctx.closePath(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-0.15 * s, -0.4 * s); ctx.lineTo(-0.15 * s, 0.3 * s); ctx.moveTo(0.15 * s, -0.3 * s); ctx.lineTo(0.15 * s, 0.4 * s); ctx.stroke();
    ctx.beginPath(); ctx.arc(0.02 * s, -0.02 * s + Math.sin(t * 6) * s * 0.03, s * 0.08, 0, M.TAU); ctx.fill();
  } else if (kind === 'sun') {
    ctx.beginPath(); ctx.arc(0, 0, s * 0.2, 0, M.TAU); ctx.fill();
    ctx.rotate(t * 1.5);
    for (let i = 0; i < 8; i++) { ctx.rotate(M.TAU / 8); ctx.beginPath(); ctx.moveTo(s * 0.3, 0); ctx.lineTo(s * 0.44, 0); ctx.stroke(); }
  } else if (kind === 'volcano') {
    ctx.beginPath(); ctx.moveTo(-0.45 * s, 0.25 * s); ctx.lineTo(-0.12 * s, -0.25 * s); ctx.lineTo(0.1 * s, -0.25 * s); ctx.lineTo(0.42 * s, 0.25 * s); ctx.stroke();
    for (let i = 0; i < 3; i++) { const p = ((t * 0.9 + i / 3) % 1); ctx.globalAlpha = 1 - p; ctx.beginPath(); ctx.arc(-0.01 * s + Math.sin(p * 6 + i) * s * 0.06, -0.32 * s - p * s * 0.25, s * (0.05 + p * 0.06), 0, M.TAU); ctx.stroke(); }
    ctx.globalAlpha = 1; ctx.beginPath();
    for (let i = 0; i <= 20; i++) { const xx = -0.45 * s + i / 20 * 0.9 * s; ctx.lineTo(xx, 0.38 * s + Math.sin(i * 0.9 + t * 6) * s * 0.04); }
    ctx.stroke();
  } else if (kind === 'contour') {
    for (let r = 1; r <= 3; r++) { ctx.beginPath(); for (let i = 0; i <= 40; i++) { const a = i / 40 * M.TAU, k = 1 + 0.15 * Math.sin(a * 2 + t * 2 + r); const rr = s * 0.13 * r * k; i ? ctx.lineTo(Math.cos(a) * rr, Math.sin(a) * rr * 0.8) : ctx.moveTo(rr, 0); } ctx.stroke(); }
  } else if (kind === 'check') {
    ctx.lineWidth = s * 0.14; ctx.beginPath(); ctx.moveTo(-0.3 * s, 0); ctx.lineTo(-0.08 * s, 0.22 * s); ctx.lineTo(0.32 * s, -0.22 * s); ctx.stroke();
  }
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

function wordmark(ctx, x, y, size, t, t0, align = 'left', color = C.white) {
  return springLine(ctx, 'OSNGEO.id', x, y, size, 800, UI, color, t, t0, { align, accentFrom: 6, stagger: 0.03, track: -0.03 });
}

// ------------------------------------------------------------------ captions (phrase level)
const KEYS = /(video animasi|tiga belas topik|seratus video|gratis|puluhan paket tryout|pembahasan|grafik kemajuan|OSNGEO\.id|abstrak|kelihatan|berat banget)/i;
function captions(ctx, t, dark = true) {
  const cur = CAP.filter(([, a, b]) => t >= a - 0.05 && t < b + 0.25).pop();
  if (!cur) return;
  const [str, a] = cur;
  const k = sp(t, a - 0.05, SPRING.snappy);
  const f = font(40, 700, UI); ctx.font = f;
  const w = ctx.measureText(str).width + 56, h = 70, y = 1440;
  ctx.save(); ctx.translate(W / 2, y); ctx.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k); ctx.globalAlpha = Math.min(1, k * 1.4);
  rrect(ctx, -w / 2, -h / 2, w, h, 18); ctx.fillStyle = dark ? 'rgba(14,26,21,0.82)' : 'rgba(22,41,35,0.9)'; ctx.fill();
  // keyword in clay
  const m = str.match(KEYS);
  let x = -w / 2 + 28;
  const parts = m ? [str.slice(0, m.index), m[0], str.slice(m.index + m[0].length)] : [str, '', ''];
  ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  parts.forEach((p, i) => { if (!p) return; ctx.fillStyle = i === 1 ? C.clay : C.white; ctx.fillText(p, x, 2); x += ctx.measureText(p).width; });
  ctx.restore();
}

// ------------------------------------------------------------------ SCENE 1: hook (0 - 8.1)
const PAINS = [['books', 'Hafalannya banyak', 3.58], ['swirl', 'Konsepnya abstrak', 5.11], ['map', 'Peta & grafik bikin pusing', 6.47]];
function sHook(ctx, t) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.06, 900, 300);
  // globe
  const zoomP = E.inOutCubic(P(t, 6.9, 8.05));
  const R0 = 330 * sp(t, -0.2, SPRING.bouncy);
  const sag = 110 * (sp(t, 2.25, SPRING.wobbly) - sp(t, 3.3, SPRING.gentle));
  let [gx, gy, gr] = M.springKeys(t * 2, [[0, [540, 1060, 1]], [6.9, [540, 860, 0.5]]], SPRING.gentle);
  const R = logLerp(Math.max(R0 * gr, 1), 5200, zoomP);
  const lon = lerp(70 + t * 22, 118, E.inOutCubic(P(t, 6.6, 7.8))), lat = lerp(-8, -2, P(t, 6.6, 7.8));
  const squash = 0.08 * wobble(t - 2.25, 2.4, 4);
  ctx.save(); ctx.translate(gx, gy + sag); ctx.scale(1 + squash, 1 - squash); ctx.translate(-gx, -(gy + sag));
  globe(ctx, gx, gy + sag + zoomP * 320, R, lon, lat, { alpha: 1 - ease(t, 7.75, 8.1) });
  ctx.restore();
  // title
  const out = 6.95;
  ctx.save(); M.shake(ctx, t * 2, S(2.25), 22, 5, 0.25);
  springLine(ctx, 'Belajar geografi OSN', 80, 380, 74, 800, UI, C.white, t, -0.25, { out });
  springLine(ctx, 'kok rasanya', 80, 480, 74, 800, UI, C.white, t, 1.4, { out });
  const f = font(176, 400, D), L = layout(ctx, 'berat banget?', f, -4);
  L.glyphs.forEach((g, j) => {
    const k = sp(t, 2.1 + j * 0.018, SPRING.bouncy);
    if (k <= 0.001) return;
    const o = E.inBack(P(t, out + j * 0.012, out + 0.35 + j * 0.012), 1.6);
    glyph(ctx, g.ch, 74 + g.cx, 650 - (1 - k) * 260 - o * 1600, f, C.clay, 1 + (1 - k) * 0.6, k);
  });
  ctx.restore();
  // pain cards
  PAINS.forEach(([ic, str, t0], i) => {
    const k = sp(t, t0 - 0.08, SPRING.bouncy);
    if (k <= 0.001) return;
    const o = E.inBack(P(t, out + 0.05 * i, out + 0.4 + 0.05 * i), 1.5);
    const dir = i % 2 ? 1 : -1, y = 1060 + i * 122 + o * 1100;
    const x = 110 + dir * (1 - k) * 900;
    ctx.save(); ctx.translate(x + 430, y + 50); ctx.rotate(dir * (1 - k) * 0.15 + (i - 1) * 0.012); ctx.translate(-430, -50);
    shadow(ctx, 0.3, 30, 14); rrect(ctx, 0, 0, 860, 104, 26); ctx.fillStyle = 'rgba(36,78,67,0.96)'; ctx.fill(); noShadow(ctx);
    ctx.strokeStyle = 'rgba(255,254,250,0.16)'; ctx.lineWidth = 2; ctx.stroke();
    ctx.beginPath(); ctx.arc(64, 52, 36, 0, M.TAU); ctx.fillStyle = C.clay; ctx.fill();
    icon(ctx, ic, 64, 52, 50, t, C.deep);
    text(ctx, str, 124, 68, font(46, 800, UI), C.white, 'left', -1);
    ctx.restore();
  });
}

// ------------------------------------------------------------------ SCENE 2: intro (7.6 - 12.5)
function sIntro(ctx, t, IMG) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.05, 200, 1600, 2);
  const mapIn = ease(t, 7.5, 8.6), mapP = P(t, 7.5, 9.6);
  const mapW = logLerp(2600, 1000, mapIn);
  indonesia(ctx, 540, lerp(1080, 1000, mapIn), mapW, Math.max(mapP, 0.45), { stroke: C.f2, lw: 4, alpha: lerp(1, 0.32, ease(t, 10.2, 11)), fillA: 0.25 * ease(t, 9.4, 10.2) });
  // logo + wordmark, then move to header
  const hd = sp(t, 10.35, SPRING.gentle) - sp(t, 12.15, SPRING.snappy) * 0;
  const k = sp(t, 7.85, SPRING.bouncy);
  const needle = (1 - sp(t, 8.55, SPRING.wobbly)) * Math.PI * 3;
  const ly = lerp(560, 300, hd), ls = lerp(190, 92, hd), lx = lerp(540, 128, hd);
  const exit = E.inBack(P(t, 12.1, 12.45), 1.5);
  ctx.save(); ctx.translate(0, -exit * 500);
  if (k > 0.001) { ctx.save(); ctx.translate(lx, ly); ctx.scale(k, k); ctx.translate(-lx, -ly); logoMark(ctx, lx, ly, ls, needle); ctx.restore(); }
  const wy = lerp(800, 328, hd), wsz = lerp(118, 62, hd);
  { const L = layout(ctx, 'OSNGEO.id', font(wsz, 800, UI), -0.03 * wsz); const lxw = lerp(540 - L.width / 2, 196, hd); wordmark(ctx, lxw, wy, wsz, t, 9.3, 'left'); }
  if (hd < 0.5) { const a = ease(t, 9.9, 10.2) * (1 - ease(t, 10.3, 10.5)); if (a > 0) { ctx.globalAlpha = a; text(ctx, 'Platform belajar OSN Geografi', 540, 880, font(40, 600, UI), C.f2, 'center'); ctx.globalAlpha = 1; } }
  ctx.restore();
  // phone
  const pk = sp(t, 10.45, SPRING.gentle);
  if (pk > 0.001) {
    const scroll = 420 * E.inOutCubic(P(t, 11.1, 12.4));
    phone(ctx, IMG, { cx: 540, top: lerp(1900, 470, pk), w: 430, img: 'landing', scroll, rot: lerp(-14, 0, pk) + 2 * wobble(t - 10.9, 1.6, 3) });
  }
}

// ------------------------------------------------------------------ SCENE 3: video animasi (12.3 - 21.0)
const MONSUN_CARD = [14, 50, 362, 395];
function sVideo(ctx, t, IMG) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.05, 900, 400, 4);
  const breakP = E.inOutCubic(P(t, 14.95, 15.6));
  // headline
  const hOut = 14.8;
  springLine(ctx, 'Belajar lewat', 80, 340, 64, 800, UI, C.white, t, 12.3, { out: hOut });
  springLine(ctx, 'video animasi', 80, 470, 128, 400, D, C.clay, t, 12.45, { out: hOut, track: -0.01 });
  // phone
  const swapV = ease(t, 12.35, 12.75, E.inOutCubic);
  const swapP = ease(t, 14.5, 14.75, E.inOutCubic);
  const scroll = 640 * E.inOutCubic(P(t, 12.8, 13.6));
  const push = E.inOutCubic(P(t, 14.55, 15.0));
  const phW = 430 * lerp(1, 1.55, push), phTop = lerp(560, 300, push);
  if (breakP < 1) {
    const ph = phone(ctx, IMG, { cx: 540, top: phTop, w: phW, img: swapP < 1 ? 'landing' : 'player', scroll: swapP < 1 ? 420 : 0, img2: swapP > 0 ? 'player' : 'videos_top', swap: swapP > 0 ? swapP : swapV, scroll2: swapP > 0 ? 0 : scroll, dim: 0.0 });
    if (swapP <= 0 && swapV >= 1) phone(ctx, IMG, { cx: 540, top: phTop, w: phW, img: 'videos_top', scroll });
    // card pops out + tap
    const ck = sp(t, 13.65, SPRING.bouncy), cBack = E.inBack(P(t, 14.45, 14.75), 1.3);
    if (ck > 0.001 && cBack < 1) {
      const cx = 540, cy = lerp(1060, 1010, ck), w = lerp(362 * 430 / 390, 900, ck) * (1 - cBack * 0.6);
      const h = card(ctx, IMG.videos_monsun, MONSUN_CARD, cx, cy, w, { k: 1, rot: (1 - ck) * -6, alpha: 1 - cBack });
      const tx = cx + ((332 - 14) / 362 - 0.5) * w, ty = cy + ((418 - 50) / 395 - 0.5) * h;
      fingerAt(ctx, tx, ty, t, 13.95, 14.35, 14.5);
    }
  }
  // break-out monsoon animation
  if (t >= 14.95) {
    const sx = 540 - phW / 2 + 12 * phW / 390, sy = phTop + 287 * phW / 390, sw = 366 * phW / 390, sh = sw * 9 / 16;
    const x = lerp(sx, 0, breakP), y = lerp(sy, 0, breakP), w = lerp(sw, W, breakP), h = lerp(sh, H, breakP);
    ctx.save(); rrect(ctx, x, y, w, h, lerp(10, 0, breakP)); ctx.clip();
    monsoon(ctx, t, x, y, w, h, breakP);
    ctx.restore();
  }
  // supers over the animation
  if (t > 15.0) {
    const o = 20.55;
    springLine(ctx, 'Konsep abstrak', 80, 360, 70, 800, UI, C.white, t, 15.0, { out: o });
    ctx.save(); M.shake(ctx, t * 2, S(16.9), 16, 8, 0.2);
    springLine(ctx, 'jadi', 80, 500, 70, 800, UI, C.white, t, 16.75, { out: o });
    const f = font(190, 400, D), L = layout(ctx, 'kelihatan.', f, -3);
    L.glyphs.forEach((g, j) => { const k = sp(t, 16.85 + j * 0.02, SPRING.bouncy); if (k <= 0.001) return; const oo = E.inBack(P(t, o + j * 0.012, o + 0.35), 1.6); glyph(ctx, g.ch, 225 + g.cx, 530 + (1 - k) * 120 - oo * 900, f, C.clay, 1 + (1 - k), k); });
    ctx.restore();
    [['gampang dipahami', 18.5], ['nempel di kepala', 19.6]].forEach(([s, t0], i) => {
      const k = sp(t, t0, SPRING.bouncy) * (1 - E.inBack(P(t, o, o + 0.3)));
      if (k <= 0.001) return;
      ctx.save(); ctx.translate(80 + i * 470, 1280); ctx.scale(k, k);
      rrect(ctx, 0, -46, 440, 92, 46); ctx.fillStyle = C.white; shadow(ctx, 0.3, 20, 8); ctx.fill(); noShadow(ctx);
      ctx.beginPath(); ctx.arc(46, 0, 30, 0, M.TAU); ctx.fillStyle = C.forest; ctx.fill(); icon(ctx, 'check', 46, 0, 44, t, C.white);
      text(ctx, s, 90, 14, font(38, 800, UI), C.deep);
      ctx.restore();
    });
  }
}

// the lesson motion graphic (Asia-Australia monsoon), drawn into a box
function monsoon(ctx, t, x, y, w, h, full) {
  ctx.fillStyle = '#20483d'; ctx.fillRect(x, y, w, h);
  // map: lon 85..158, lat 32..-42 fitted to width, centred vertically at ~ y+0.52h
  const lonA = 82, lonB = 160, s = w / (lonB - lonA);
  const cy = y + h * (0.5 + 0.03 * full), latC = -4;
  const pt = (lo, la) => [x + (lo - lonA) * s, cy - (la - latC) * s];
  ctx.save(); ctx.lineWidth = Math.max(1, w / 500);
  for (const ring of GEO.land) {
    let any = false; for (const [lo, la] of ring) if (lo > lonA - 20 && lo < lonB + 20 && la > -50 && la < 50) { any = true; break; }
    if (!any) continue;
    ctx.beginPath(); ring.forEach(([lo, la], i) => { const [px, py] = pt(lo, la); i ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }); ctx.closePath();
    ctx.fillStyle = '#5f8a74'; ctx.fill(); ctx.strokeStyle = '#2b5a4c'; ctx.stroke();
  }
  // seasons: west monsoon (wet) until 18.3, then east (dry)
  const flip = E.inOutCubic(P(t, 18.1, 18.6));
  // ITCZ band
  const itczLat = lerp(-9, 9, flip) + Math.sin(t * 2) * 1.2;
  const [, iy] = pt(0, itczLat);
  ctx.globalAlpha = 0.3; ctx.fillStyle = C.clay; ctx.fillRect(x, iy - 5 * s, w, 10 * s); ctx.globalAlpha = 1;
  ctx.setLineDash([10 * s / 3, 7 * s / 3]); ctx.strokeStyle = C.clay; ctx.lineWidth = Math.max(1.5, s * 0.45); ctx.beginPath(); ctx.moveTo(x, iy); ctx.lineTo(x + w, iy); ctx.stroke(); ctx.setLineDash([]);
  text(ctx, 'ITCZ', x + w - 18, iy - 6 * s, font(Math.max(10, s * 3.2), 800, UI), C.clay, 'right');
  // flowing arrows
  const flows = 5;
  for (let i = 0; i < flows; i++) {
    const off = (i - 2) * 6;
    const A = flip < 0.5 ? [[100 + off, 24], [112 + off, 2], [128 + off, -16]] : [[136 + off, -26], [122 + off, -4], [104 + off, 14]];
    const [ax, ay] = pt(...A[0]), [bx, by] = pt(...A[1]), [cx2, cy2] = pt(...A[2]);
    const a = flip < 0.5 ? 1 - flip * 2 : (flip - 0.5) * 2;
    ctx.save(); ctx.globalAlpha = a;
    ctx.strokeStyle = flip < 0.5 ? C.f2 : C.clay; ctx.lineWidth = Math.max(2, s * 0.9); ctx.lineCap = 'round';
    ctx.setLineDash([6 * s, 4 * s]); ctx.lineDashOffset = -t * 18 * s;
    ctx.beginPath(); ctx.moveTo(ax, ay); ctx.quadraticCurveTo(bx, by, cx2, cy2); ctx.stroke(); ctx.setLineDash([]);
    const ang = Math.atan2(cy2 - by, cx2 - bx); ctx.translate(cx2, cy2); ctx.rotate(ang);
    ctx.fillStyle = ctx.strokeStyle; ctx.beginPath(); ctx.moveTo(2.4 * s, 0); ctx.lineTo(-1.6 * s, -1.8 * s); ctx.lineTo(-1.6 * s, 1.8 * s); ctx.closePath(); ctx.fill();
    ctx.restore();
  }
  // weather over Indonesia
  const [ix, iyy] = pt(116, 4);
  if (flip < 0.6) {
    ctx.save(); ctx.globalAlpha = 1 - ease(flip, 0.3, 0.6);
    for (const [dx, dy, r] of [[0, 0, 7], [-7, 2, 5], [7, 2, 5]]) { ctx.beginPath(); ctx.arc(ix + dx * s, iyy + dy * s + Math.sin(t * 2) * s * 0.4, r * s, 0, M.TAU); ctx.fillStyle = C.white; ctx.fill(); }
    ctx.strokeStyle = C.f2; ctx.lineWidth = Math.max(1.5, s * 0.6);
    for (let i = 0; i < 9; i++) { const p = (t * 1.6 + i * 0.37) % 1, rx = ix + (i - 4) * 2.2 * s; ctx.globalAlpha = (1 - p) * (1 - ease(flip, 0.3, 0.6)); ctx.beginPath(); ctx.moveTo(rx, iyy + 6 * s + p * 9 * s); ctx.lineTo(rx - s, iyy + 9 * s + p * 9 * s); ctx.stroke(); }
    ctx.restore();
  }
  if (flip > 0.4) {
    ctx.save(); ctx.globalAlpha = ease(flip, 0.4, 0.8);
    const [sx2, sy2] = pt(132, -22);
    ctx.translate(sx2, sy2); ctx.rotate(t);
    ctx.beginPath(); ctx.arc(0, 0, 5 * s, 0, M.TAU); ctx.fillStyle = C.clay; ctx.fill();
    ctx.strokeStyle = C.clay; ctx.lineWidth = Math.max(1.5, s * 0.7);
    for (let i = 0; i < 10; i++) { ctx.rotate(M.TAU / 10); ctx.beginPath(); ctx.moveTo(7 * s, 0); ctx.lineTo(10 * s, 0); ctx.stroke(); }
    ctx.restore();
  }
  // season label (inside the lesson frame)
  const lab = flip < 0.5 ? 'Monsun Barat · Okt–Apr · basah' : 'Monsun Timur · Apr–Okt · kering';
  const fs = Math.max(10, s * 3.4);
  ctx.save(); ctx.globalAlpha = flip < 0.5 ? 1 - flip * 2 : (flip - 0.5) * 2;
  const lx = x + w * 0.065, ly = y + h * (full > 0.5 ? 0.6 : 0.85);
  ctx.font = font(fs, 800, UI); const lw = ctx.measureText(lab).width + fs * 1.4;
  rrect(ctx, lx, ly - fs * 1.1, lw, fs * 1.9, fs * 0.95); ctx.fillStyle = flip < 0.5 ? C.f2 : C.clay; ctx.fill();
  text(ctx, lab, lx + fs * 0.7, ly + fs * 0.3, font(fs, 800, UI), C.deep);
  ctx.restore();
  // lesson chrome: title + progress (only while in the player)
  if (full < 0.6) {
    ctx.globalAlpha = 1 - full / 0.6;
    text(ctx, 'B01-10', x + w * 0.04, y + h * 0.12, font(Math.max(8, h * 0.06), 800, UI), C.clay);
    text(ctx, 'ITCZ dan Monsun Asia–Australia', x + w * 0.04, y + h * 0.22, font(Math.max(9, h * 0.085), 800, UI), C.white);
    ctx.globalAlpha = 1;
  }
  ctx.fillStyle = C.clay; ctx.fillRect(x, y + h - Math.max(3, h * 0.012), w * (0.12 + 0.14 * P(t, 15, 20.5)), Math.max(3, h * 0.012));
  ctx.restore();
}

// ------------------------------------------------------------------ SCENE 4: 13 topik (20.7 - 29.1), sand
const TOPICS = [['sun', 'Iklim', 26.16], ['volcano', 'Kebencanaan', 27.14], ['contour', 'Perpetaan', 28.06]];
function sTopik(ctx, t, IMG) {
  fill(ctx, C.sand);
  contours(ctx, t, C.forest, 0.07, 150, 1500, 6);
  springLine(ctx, 'Videonya disusun', 72, 360, 62, 800, UI, C.deep, t, 20.8);
  springLine(ctx, 'per topik', 72, 490, 140, 400, D, C.clay6, t, 21.0, { track: -0.01 });
  // phone on the right
  const pk = sp(t, 20.9, SPRING.gentle);
  const sw = ease(t, 27.0, 27.35, E.inOutCubic);
  phone(ctx, IMG, { cx: lerp(1400, 800, pk), top: 560, w: 340, img: 'videos_top', scroll: lerp(300, 806, E.inOutCubic(P(t, 21.3, 26.8))), img2: 'videos_bab2', swap: sw, scroll2: lerp(380, 700, P(t, 27.3, 29)), rot: lerp(18, 5, pk) + 1.5 * Math.sin(t * 1.3) });
  // 13 counter with ring
  const ck = sp(t, 24.0, SPRING.bouncy);
  if (ck > 0.001) {
    const cp = E.outCubic(P(t, 24.1, 25.3)), n = Math.round(13 * cp);
    const cx = 270, cy = 800, r = 170;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(ck, ck);
    ctx.beginPath(); ctx.arc(0, 0, r, 0, M.TAU); ctx.strokeStyle = C.sand2; ctx.lineWidth = 18; ctx.stroke();
    ctx.beginPath(); ctx.arc(0, 0, r, -Math.PI / 2, -Math.PI / 2 + cp * M.TAU); ctx.strokeStyle = C.clay; ctx.lineCap = 'round'; ctx.stroke();
    const bump = 1 + 0.12 * wobble(t - 25.3, 2.5, 5);
    ctx.scale(bump, bump);
    text(ctx, String(n), 0, 70, font(220, 800, UI), C.deep, 'center', -8);
    ctx.restore();
    const a = ease(t, 24.6, 25);
    ctx.globalAlpha = a; text(ctx, 'topik OSN Geografi', 270, 1030 + (1 - a) * 20, font(40, 700, UI), C.f5, 'center'); ctx.globalAlpha = 1;
  }
  TOPICS.forEach(([ic, s, t0], i) => {
    const k = sp(t, t0 - 0.1, SPRING.bouncy);
    if (k <= 0.001) return;
    const y = 1120 + i * 100, x = 72 - (1 - k) * 500;
    ctx.save(); ctx.translate(x, y); ctx.rotate((1 - k) * -0.2);
    shadow(ctx, 0.18, 20, 8); rrect(ctx, 0, -40, 440, 80, 40); ctx.fillStyle = C.forest; ctx.fill(); noShadow(ctx);
    ctx.beginPath(); ctx.arc(40, 0, 30, 0, M.TAU); ctx.fillStyle = C.clay; ctx.fill();
    icon(ctx, ic, 40, 0, 44, t, C.deep);
    text(ctx, s, 88, 14, font(40, 800, UI), C.white);
    ctx.restore();
  });
}

// ------------------------------------------------------------------ SCENE 5: 99 video (28.7 - 37.0)
function sSeri(ctx, t, IMG) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.05, 950, 1500, 8);
  springLine(ctx, 'Hampir', 72, 350, 66, 800, UI, C.white, t, 28.55);
  const cp = E.outCubic(P(t, 28.9, 30.6)), n = Math.round(99 * cp);
  const k = sp(t, 28.6, SPRING.bouncy), bmp = 1 + 0.1 * wobble(t - 30.6, 2.5, 5);
  if (k > 0.001) { ctx.save(); ctx.translate(300, 470); ctx.scale(k * bmp, k * bmp); text(ctx, String(n), 0, 70, font(250, 800, UI), C.clay, 'left', -10); ctx.restore(); }
  springLine(ctx, 'video animasi', 640, 548, 54, 800, UI, C.white, t, 29.6);
  // grid of 99 tiles: 12 live
  const cols = 11, tw = 58, th = 36, gx = 12, gy = 10, x0 = (W - (cols * tw + (cols - 1) * gx)) / 2, y0 = 660;
  for (let i = 0; i < 99; i++) {
    const c = i % cols, r = Math.floor(i / cols);
    const kk = sp(t, 29.05 + (c + r) * 0.035, SPRING.bouncy);
    if (kk <= 0.001) continue;
    const live = i < 12 ? ease(t, 31.2 + i * 0.07, 31.4 + i * 0.07) : 0;
    const x = x0 + c * (tw + gx), y = y0 + r * (th + gy);
    ctx.save(); ctx.translate(x + tw / 2, y + th / 2); ctx.scale(kk, kk);
    rrect(ctx, -tw / 2, -th / 2, tw, th, 9);
    ctx.fillStyle = live ? mix('#2a5a4c', C.clay, live) : 'rgba(255,254,250,0.06)'; ctx.fill();
    ctx.strokeStyle = live ? C.clay : 'rgba(255,254,250,0.22)'; ctx.lineWidth = 2; ctx.stroke();
    if (live > 0.5) { ctx.fillStyle = C.deep; ctx.beginPath(); ctx.moveTo(-6, -9); ctx.lineTo(9, 0); ctx.lineTo(-6, 9); ctx.closePath(); ctx.fill(); }
    ctx.restore();
  }
  const la = ease(t, 31.6, 32.0) * (1 - ease(t, 33.2, 33.45));
  if (la > 0) { ctx.globalAlpha = la; text(ctx, '12 sudah tayang · sisanya dirilis bertahap', W / 2, 1140, font(36, 700, UI), C.f2, 'center'); ctx.globalAlpha = 1; }
  // real series bar from the app
  const bk = sp(t, 33.35, SPRING.bouncy);
  if (bk > 0.001) card(ctx, IMG.videos_top, BOX.videos.el.series, W / 2, lerp(1700, 1235, bk), 860, { rot: (1 - bk) * 8 });
  // GRATIS stamp
  const gk = sp(t, 33.65, SPRING.bouncy);
  if (gk > 0.001) {
    ctx.save(); M.shake(ctx, t * 2, S(33.7), 10, 2, 0.2);
    pill(ctx, 'GRATIS', 790, 690, 58, C.clay, C.deep, lerp(2.6, 1, gk) , -9);
    ctx.restore();
    const a = ease(t, 34.0, 34.4); ctx.globalAlpha = a; text(ctx, 'sebagian bisa ditonton', 790, 800, font(34, 700, UI), C.white, 'center'); ctx.globalAlpha = 1;
  }
}

// ------------------------------------------------------------------ SCENE 6: tryout (36.7 - 43.6), sand
function sTryout(ctx, t, IMG) {
  fill(ctx, C.sand);
  contours(ctx, t, C.forest, 0.06, 900, 300, 9);
  springLine(ctx, 'Habis nonton,', 72, 350, 60, 800, UI, C.deep, t, 36.55);
  springLine(ctx, 'uji pemahamanmu.', 72, 480, 112, 400, D, C.clay6, t, 38.15, { track: -0.01 });
  const pk = sp(t, 36.6, SPRING.gentle);
  const toExam = ease(t, 40.85, 41.2, E.inOutCubic);
  const push = E.inOutCubic(P(t, 41.3, 41.9));
  const w = 380 * lerp(1, 1.42, push), top = lerp(570, 470, push) - push * 60;
  const exAns = t >= 42.25;
  const ph = phone(ctx, IMG, { cx: lerp(1500, 540, pk) - push * 60, top, w, img: 'tryouts_top', scroll: 230 * E.inOutCubic(P(t, 37.6, 39.8)), img2: exAns ? 'exam_q1_ans' : 'exam_q1', swap: toExam, rot: lerp(-16, 0, pk) });
  if (toExam >= 1) {
    // highlight chosen answer
    const b = BOX.exam_q1.el['opt' + BOX.correct0];
    const [ox, oy] = onPhone(ph, b[0] + b[2] / 2, b[1] + b[3] / 2);
    fingerAt(ctx, ox, oy, t, 41.85, 42.2, 42.7);
    const g = ease(t, 42.25, 42.4) * (1 - ease(t, 43.2, 43.5));
    if (g > 0) {
      ctx.save(); ctx.globalAlpha = g;
      rrect(ctx, ph.x + b[0] * ph.s - 8, ph.y + b[1] * ph.s - 8, b[2] * ph.s + 16, b[3] * ph.s + 16, 22); ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.stroke();
      const bx = ph.x + (b[0] + b[2]) * ph.s - 6, by = ph.y + b[1] * ph.s - 4, kk = sp(t, 42.3, SPRING.bouncy);
      ctx.translate(bx, by); ctx.scale(kk, kk); ctx.beginPath(); ctx.arc(0, 0, 38, 0, M.TAU); ctx.fillStyle = C.forest; ctx.fill(); icon(ctx, 'check', 0, 0, 52, t, C.white);
      ctx.restore();
    }
  }
  // 35 paket badge + chips
  const bk = sp(t, 40.1, SPRING.bouncy) * (1 - ease(t, 41.2, 41.4));
  if (bk > 0.001) {
    ctx.save(); ctx.translate(800, 690); ctx.scale(bk, bk); ctx.rotate(-0.06);
    shadow(ctx, 0.25, 30, 12); rrect(ctx, -190, -110, 380, 220, 36); ctx.fillStyle = C.forest; ctx.fill(); noShadow(ctx);
    text(ctx, String(Math.round(35 * E.outCubic(P(t, 40.2, 40.9)))), 0, 22, font(150, 800, UI), C.clay, 'center', -6);
    text(ctx, 'paket tryout', 0, 80, font(36, 800, UI), C.white, 'center');
    ctx.restore();
  }
  [['OSN-K', 41.75], ['OSN-P', 42.45]].forEach(([s, t0], i) => {
    const k = sp(t, t0, SPRING.bouncy) * (1 - ease(t, 43.3, 43.5));
    pill(ctx, s, 170 + i * 0, 1180 + i * 110, 40, C.forest, C.white, k, i ? 4 : -4);
  });
}

// ------------------------------------------------------------------ SCENE 7: pembahasan (43.4 - 45.4)
function sBahas(ctx, t, IMG) {
  fill(ctx, C.sand);
  contours(ctx, t, C.forest, 0.06, 150, 400, 11);
  springLine(ctx, 'Lengkap dengan', 72, 340, 58, 800, UI, C.deep, t, 43.4);
  springLine(ctx, 'pembahasan.', 72, 470, 120, 400, D, C.clay6, t, 43.55, { track: -0.01 });
  phone(ctx, IMG, { cx: 540, top: 600, w: 360, img: 'results_top', scroll: 60 * P(t, 43.5, 45.3), dim: 0.25 * ease(t, 43.7, 44.0) });
  const k1 = sp(t, 43.7, SPRING.bouncy), k2 = sp(t, 44.25, SPRING.bouncy);
  card(ctx, IMG.results_top, [14, 180, 362, 170], lerp(540, 540, k1), lerp(900, 760, k1), lerp(360, 900, k1), { k: Math.min(1, k1 * 1.1), rot: (1 - k1) * -5, alpha: Math.min(1, k1 * 3) });
  card(ctx, IMG.results_top, [14, 360, 362, 290], 540, lerp(1300, 1135, k2), lerp(360, 860, k2), { k: Math.min(1, k2 * 1.1), rot: (1 - k2) * 5, alpha: Math.min(1, k2 * 3) });
}

// ------------------------------------------------------------------ SCENE 8: grafik (45.1 - 49.0)
const CHART = [14, 985, 362, 265];
function sGrafik(ctx, t, IMG) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.05, 950, 300, 12);
  springLine(ctx, 'Grafik', 72, 350, 66, 800, UI, C.white, t, 45.15, { out: 48.6 });
  springLine(ctx, 'kemajuan', 300, 350, 120, 400, D, C.clay, t, 45.3, { out: 48.6, track: -0.01 });
  springLine(ctx, 'otomatis', 72, 450, 66, 800, UI, C.white, t, 45.5, { out: 48.6 });
  const k = sp(t, 45.25, SPRING.gentle), o = E.inBack(P(t, 48.6, 48.95), 1.4);
  const w = 940, h = w * CHART[3] / CHART[2], x = 70, y = lerp(1600, 560, k) + o * 1300;
  ctx.save();
  shadow(ctx, 0.35, 60, 30); rrect(ctx, x, y, w, h, 30); ctx.fillStyle = C.white; ctx.fill(); noShadow(ctx);
  rrect(ctx, x, y, w, h, 30); ctx.clip();
  // header always; plot area revealed left -> right
  const rev = E.inOutCubic(P(t, 45.6, 47.0));
  const plotX = x + (60 - 14) / 362 * w;
  ctx.drawImage(IMG.dashboard, CHART[0] * 3, CHART[1] * 3, CHART[2] * 3, CHART[3] * 3, x, y, w, h);
  const coverX = lerp(plotX, x + w, rev);
  ctx.fillStyle = C.white; ctx.fillRect(coverX, y + h * 0.2, x + w - coverX, h * 0.72);
  if (rev > 0 && rev < 1) { const g = ctx.createLinearGradient(coverX - 60, 0, coverX + 6, 0); g.addColorStop(0, 'rgba(224,121,79,0)'); g.addColorStop(1, 'rgba(224,121,79,0.55)'); ctx.fillStyle = g; ctx.fillRect(coverX - 60, y + h * 0.2, 66, h * 0.72); }
  ctx.restore();
  // pulse on the latest point
  const lp = [(346 - 14) / 362, (1055 - 985) / 265];
  const pp = P(t, 47.0, 48.4);
  if (pp > 0 && o < 1) { const px = x + lp[0] * w, py = y + lp[1] * h; for (let i = 0; i < 2; i++) { const q = (pp * 2 + i * 0.5) % 1; ctx.beginPath(); ctx.arc(px, py, 14 + q * 60, 0, M.TAU); ctx.strokeStyle = `rgba(224,121,79,${1 - q})`; ctx.lineWidth = 5; ctx.stroke(); } }
  const ck = sp(t, 46.65, SPRING.bouncy) * (1 - E.inBack(P(t, 48.6, 48.9)));
  pill(ctx, 'Tahu topik yang masih lemah', W / 2, 1300, 40, C.clay, C.deep, ck, -2);
}

// ------------------------------------------------------------------ SCENE 9: CTA (48.8 - end)
const GRATIS_CARD = [14, 250, 362, 335];
function sCta(ctx, t, IMG) {
  fill(ctx, C.forest);
  contours(ctx, t, C.white, 0.06, 540, 960, 14);
  globe(ctx, 540, 1180, 520, 90 + t * 18, -6, { alpha: 0.28 });
  const o1 = 51.55;
  ctx.save(); M.shake(ctx, t * 2, S(48.85), 14, 4, 0.2);
  springLine(ctx, 'Belajar lebih', 80, 470, 78, 800, UI, C.white, t, 48.75, { out: o1 });
  springLine(ctx, 'gampang.', 80, 640, 190, 400, D, C.clay, t, 48.9, { out: o1, track: -0.01 });
  springLine(ctx, 'Latihan lebih', 80, 860, 78, 800, UI, C.white, t, 50.05, { out: o1 });
  springLine(ctx, 'terarah.', 80, 1030, 190, 400, D, C.clay, t, 50.2, { out: o1, track: -0.01 });
  ctx.restore();
  if (t > 51.7) {
    const lk = sp(t, 51.75, SPRING.bouncy);
    ctx.save(); ctx.translate(540, 330); ctx.scale(lk, lk); logoMark(ctx, -175, 0, 84, (1 - sp(t, 51.8, SPRING.wobbly)) * 6); ctx.restore();
    wordmark(ctx, 425, 352, 58, t, 51.85, 'left');
    ctx.save(); M.shake(ctx, t * 2, S(51.88), 14, 6, 0.2);
    springLine(ctx, 'Coba', W / 2, 530, 110, 800, UI, C.white, t, 51.85, { align: 'center' });
    springLine(ctx, 'GRATIS', W / 2, 720, 210, 400, D, C.clay, t, 51.95, { align: 'center', track: 0 });
    ctx.restore();
    const ck = sp(t, 52.25, SPRING.bouncy);
    if (ck > 0.001) card(ctx, IMG.paket, GRATIS_CARD, W / 2, 1010, 520, { k: 1, scaleY: 1, rot: (1 - ck) * 30, alpha: Math.min(1, ck * 2), glow: 0 });
    const pk = sp(t, 52.85, SPRING.bouncy) + 0.12 * wobble(t - 55.1, 2.2, 4);
    pill(ctx, 'osngeo.id', W / 2, 1320, 68, C.clay, C.deep, pk);
    const a = ease(t, 55.1, 55.4);
    if (a > 0) { ctx.globalAlpha = a; text(ctx, 'Link ada di bio', W / 2, 1450 + (1 - a) * 20, font(40, 700, UI), C.f2, 'center'); ctx.globalAlpha = 1; }
  }
}

// ------------------------------------------------------------------ timeline
const SCENES = [
  [0, 8.1, sHook], [7.6, 12.5, sIntro], [12.3, 21.0, sVideo], [20.7, 29.1, sTopik], [28.7, 37.0, sSeri],
  [36.7, 43.6, sTryout], [43.4, 45.4, sBahas], [45.1, 49.0, sGrafik], [48.8, 60, sCta],
];
// transitions: [t0, t1, kind]
function draw(ctx, u, t, IMG) {
  const active = SCENES.filter(([a, b]) => t >= a && t < b);
  // 0-7.6 hook alone; 7.6-8.1 hook zoom crossfades into intro
  if (t < 7.6) sHook(ctx, t);
  else if (t < 8.1) { sIntro(ctx, t, IMG); ctx.save(); ctx.globalAlpha = 1 - ease(t, 7.6, 7.95); sHook(ctx, t); ctx.restore(); }
  else if (t < 12.3) sIntro(ctx, t, IMG);
  else if (t < 20.75) sVideo(ctx, t, IMG);
  else if (t < 21.25) { // circle wipe: sand grows from centre over the animation
    sVideo(ctx, Math.min(t, 20.7), IMG);
    const p = E.inOutCubic(P(t, 20.75, 21.25)), r = logLerp(10, 1300, p);
    ctx.save(); ctx.beginPath(); ctx.arc(W / 2, H / 2, r, 0, M.TAU); ctx.clip(); sTopik(ctx, t, IMG); ctx.restore();
  }
  else if (t < 28.75) sTopik(ctx, t, IMG);
  else if (t < 29.15) whip(ctx, t, 28.75, 29.15, -1, (c) => sTopik(c, t, IMG), (c) => sSeri(c, t, IMG));
  else if (t < 36.75) sSeri(ctx, t, IMG);
  else if (t < 37.15) whip(ctx, t, 36.75, 37.15, -1, (c) => sSeri(c, t, IMG), (c) => sTryout(c, t, IMG));
  else if (t < 43.45) sTryout(ctx, t, IMG);
  else if (t < 43.8) slideUp(ctx, t, 43.45, 43.8, (c) => sTryout(c, t, IMG), (c) => sBahas(c, t, IMG));
  else if (t < 45.15) sBahas(ctx, t, IMG);
  else if (t < 45.5) slideUp(ctx, t, 45.15, 45.5, (c) => sBahas(c, t, IMG), (c) => sGrafik(c, t, IMG));
  else if (t < 48.85) sGrafik(ctx, t, IMG);
  else if (t < 49.2) { sCta(ctx, t, IMG); ctx.save(); ctx.globalAlpha = 1 - ease(t, 48.85, 49.2); sGrafik(ctx, t, IMG); ctx.restore(); }
  else sCta(ctx, t, IMG);
  const sandish = (t >= 21 && t < 28.95) || (t >= 36.95 && t < 45.3);
  if (t < 51.8) captions(ctx, t, !sandish);
}
function whip(ctx, t, a, b, dir, A, B) {
  const p = E.inOutCubic(P(t, a, b));
  ctx.save(); ctx.translate(dir * p * W, 0); A(ctx); ctx.restore();
  ctx.save(); ctx.translate(dir * (p - 1) * W, 0); B(ctx); ctx.restore();
}
function slideUp(ctx, t, a, b, A, B) {
  const p = E.inOutCubic(P(t, a, b));
  ctx.save(); ctx.translate(0, -p * H); A(ctx); ctx.restore();
  ctx.save(); ctx.translate(0, (1 - p) * H); B(ctx); ctx.restore();
}

M.film({
  fonts: [font(100, 800, UI), font(100, 400, D), font(40, 700, UI)],
  images: {
    landing: 'assets/shots/landing_top.png', videos_top: 'assets/shots/videos_top.png', videos_monsun: 'assets/shots/videos_monsun.png',
    videos_bab2: 'assets/shots/videos_bab2.png', player: 'assets/shots/player.png', tryouts_top: 'assets/shots/tryouts_top.png',
    exam_q1: 'assets/shots/exam_q1.png', exam_q1_ans: 'assets/shots/exam_q1_ans.png', results_top: 'assets/shots/results_top.png',
    dashboard: 'assets/shots/dashboard.png', paket: 'assets/shots/paket.png',
  },
  hits: HITS,
  samples: 8,
  async init() {
    [BOX, GEO] = await Promise.all([fetch('assets/shots/boxes.json').then((r) => r.json()), fetch('assets/geo.json').then((r) => r.json())]);
    const tm = await fetch('docs/vo_timing.json').then((r) => r.json());
    // merge very short phrases into the next one for readable captions
    const ph = tm.phrases.map(([s, a, b]) => [s.replace(/OSN-?GEO dot ID/g, 'OSNGEO.id'), a, b]);
    const out = [];
    for (const p of ph) {
      const last = out[out.length - 1];
      if (last && (last[0].split(' ').length <= 1 || p[1] - last[2] < 0.05) && (last[0] + ' ' + p[0]).length < 40) { last[0] += ' ' + p[0]; last[2] = p[2]; }
      else out.push([...p]);
    }
    CAP = [];
    for (const [s, a, b] of out) {
      const w = s.split(' ');
      if (s.length <= 30) { CAP.push([s, a, b]); continue; }
      const n = Math.ceil(s.length / 30), per = Math.ceil(w.length / n);
      const chunks = []; for (let i = 0; i < w.length; i += per) chunks.push(w.slice(i, i + per).join(' '));
      const tot = chunks.reduce((q, c) => q + c.length, 0); let tt = a;
      for (const c of chunks) { const d = (b - a) * c.length / tot; CAP.push([c, tt, tt + d]); tt += d; }
    }
    for (let r = 80; r < 2300; r += 70) CONT.push(r);
  },
  draw,
});
