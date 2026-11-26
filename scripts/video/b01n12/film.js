// B01-12 · Kelembapan Udara · OSNGEO.id — pure function of time (seconds). New style: character + motion, minimal text.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, check, cross } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { gumpal, tag, bigNum, thermo, sawah, drop, iceTea } from './lib/gumpal.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 232.5;
const u = (i) => U_(i).v0;
const sky = (ctx, top, bot) => { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); };
function vapor(ctx, x, y, w, h, n, t, a = 1, col = '#4a9be0', salt = 1) {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a;
  for (let i = 0; i < n; i++) { const px = x + ((hash01(i, salt) * w + Math.sin(t * 0.7 + i) * 30) % w + w) % w, py = y + ((hash01(i, salt + 3) * h + Math.cos(t * 0.6 + i * 1.3) * 26) % h + h) % h; const r = 5 + hash01(i, salt + 5) * 4; circle(ctx, px, py, r); ctx.fillStyle = col; ctx.fill(); circle(ctx, px - r * 0.9, py - r * 0.5, r * 0.55); circle(ctx, px + r * 0.9, py - r * 0.5, r * 0.55); ctx.fillStyle = '#ffffff'; ctx.fill(); }
  ctx.restore();
}

// ---------------------------------------------------------------- hook: iced tea sweating
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#f3e7d4', () => {
    // warm table + window light
    ctx.fillStyle = '#e8d2ae'; ctx.fillRect(0, 760, W, 320); ctx.fillStyle = 'rgba(255,240,200,0.5)'; poly(ctx, [[1300, 0], [1700, 0], [1200, 760], [800, 760]]); ctx.fill();
    sun(ctx, 1620, 170, 70, t);
    const z = 1 + 0.25 * ap(t, 3, 9, E.inOutCubic);
    ctx.save(); ctx.translate(W / 2, 640); ctx.scale(z, z); ctx.translate(-W / 2, -640);
    ctx.fillStyle = 'rgba(0,0,0,0.12)'; ctx.beginPath(); ctx.ellipse(W / 2, 770, 150, 26, 0, 0, Math.PI * 2); ctx.fill();
    iceTea(ctx, W / 2, 640, 1.35, t, ap(t, u(1) - 0.5, 3.5, E.linear));
    ctx.restore();
    // question mark
    const q = sp(t, u(3), SPRING.bouncy); if (q > 0) { ctx.save(); ctx.translate(W / 2 + 330, 330); ctx.scale(q, q); ctx.rotate(Math.sin(t * 2) * 0.08); text(ctx, '?', 0, 60, fD(220), C.clay, 'center'); ctx.restore(); }
    // invisible vapor reveal
    vapor(ctx, 0, 100, W, 600, 40, t, ap(t, u(5) - 0.2, 0.8), '#4a9be0', 4);
  });
}
// ---------------------------------------------------------------- air carries invisible vapor (zoom into air)
function sUdara(ctx, t) {
  scene(ctx, t, 'udara', '#dcebf3', () => {
    const t0 = SC.udara[0];
    // magnifier lens sweeping
    const lx = lerp(500, 1400, ap(t, t0 + 0.3, 6, E.inOutCubic)), ly = 520 + 60 * Math.sin(t * 0.8);
    vapor(ctx, 0, 0, W, H, 30, t, 0.18, '#4a9be0', 7);
    ctx.save(); circle(ctx, lx, ly, 260); ctx.clip(); ctx.fillStyle = '#eef6fb'; ctx.fillRect(0, 0, W, H); vapor(ctx, lx - 300, ly - 300, 600, 600, 26, t, 1, '#2b6cb0', 9); ctx.restore();
    ctx.strokeStyle = C.forest; ctx.lineWidth = 18; circle(ctx, lx, ly, 260); ctx.stroke(); ctx.lineWidth = 34; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(lx + 190, ly + 190); ctx.lineTo(lx + 330, ly + 330); ctx.stroke();
    tag(ctx, W / 2, 180, 'uap air', 'water vapour', ap(t, tw('uap', u(6)) - 0.2, 0.5));
  });
}
// ---------------------------------------------------------------- sources: evaporation & transpiration
function sSumber(ctx, t) {
  scene(ctx, t, 'sumber', '#cfe6f2', () => {
    sky(ctx, '#bfe0f2', '#eef6fb'); sun(ctx, 1650, 160, 70, t);
    // paper-cut layers
    ctx.fillStyle = '#3c8fc2'; ctx.fillRect(0, 760, 760, 320);
    for (let k = 0; k < 5; k++) { ctx.strokeStyle = 'rgba(255,255,255,0.35)'; ctx.lineWidth = 3; ctx.beginPath(); for (let x = 0; x <= 760; x += 20) { const y = 790 + k * 50 + 5 * Math.sin(x * 0.02 + t * 2 + k); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
    ctx.fillStyle = '#9dcf7e'; ctx.beginPath(); ctx.moveTo(740, H); ctx.lineTo(740, 760); for (let x = 740; x <= W; x += 30) ctx.lineTo(x, 740 - 20 * Math.sin(x * 0.006)); ctx.lineTo(W, H); ctx.fill();
    ctx.fillStyle = '#5aa0c8'; ctx.beginPath(); ctx.ellipse(1060, 860, 140, 36, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#b7895a'; ctx.beginPath(); ctx.ellipse(1300, 900, 120, 30, 0, 0, Math.PI * 2); ctx.fill();
    const trees = [1480, 1600, 1720, 1820];
    trees.forEach((x, i) => { const sway = Math.sin(t * 1.2 + i) * 6; ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 8, 640, 16, 110); ctx.fillStyle = '#3f8a52'; circle(ctx, x + sway, 600, 70); ctx.fill(); circle(ctx, x - 40 + sway, 630, 46); ctx.fill(); circle(ctx, x + 44 + sway, 625, 50); ctx.fill(); });
    // rising wisps
    const wisp = (x0, y0, w, a, col, salt) => { if (a <= 0) return; for (let i = 0; i < 14; i++) { const ph = (t * 0.25 + hash01(i, salt)) % 1, x = x0 + hash01(i, salt + 1) * w + Math.sin(ph * 6 + i) * 18, y = y0 - ph * 380; ctx.save(); ctx.globalAlpha = a * Math.sin(ph * Math.PI) * 0.9; circle(ctx, x, y, 7 + ph * 10); ctx.fillStyle = col; ctx.fill(); ctx.restore(); } };
    wisp(80, 790, 640, ap(t, u(7), 0.8), '#6fb3e6', 1); wisp(950, 850, 420, ap(t, tw('danau', u(7)) - 0.2, 0.8), '#6fb3e6', 3);
    wisp(1420, 600, 440, ap(t, u(9), 0.8), '#7fd3a0', 5);
    tag(ctx, 400, 300, 'evaporasi', 'evaporation', ap(t, u(8), 0.5) * (1 - ap(t, u(11), 0.4)), C.blue);
    tag(ctx, 1620, 300, 'transpirasi', 'transpiration', ap(t, u(10), 0.5) * (1 - ap(t, u(11), 0.4)), C.forestL);
    // merge arrow at u11
    const mg = ap(t, u(11), 0.8); if (mg > 0) { ctx.save(); ctx.globalAlpha *= mg; arrowLine(ctx, 420, 340, 780, 260, C.forest, 6, 20); arrowLine(ctx, 1600, 340, 1140, 260, C.forest, 6, 20); ctx.restore(); tag(ctx, 960, 240, 'evapotranspirasi', '', mg, C.forest); }
  });
}
// ---------------------------------------------------------------- the glass metaphor driven by temperature
function sGelas(ctx, t) {
  scene(ctx, t, 'gelas', '#f2efe8', () => {
    // temperature path: warm at u16, cold at u18, ticking at u19
    let T = 24 + 6 * Math.sin((t - SC.gelas[0]) * 0.9) * (t < u(16) ? ap(t, u(14), 1) : 0);
    if (t >= u(16)) T = lerp(T, 34, ap(t, u(16), 1.2, E.inOutCubic));
    if (t >= u(18)) T = lerp(34, 12, ap(t, u(18), 1.4, E.inOutCubic));
    if (t >= u(19)) T = lerp(12, 22, ap(t, u(19), 3.5, E.linear));
    const cap = Math.pow(1.07, T - 24); // relative capacity
    const tc = clamp((T - 10) / 25);
    thermo(ctx, 360, 820, 520, tc, mix(C.cold, C.clay, tc), `${Math.round(T)} °C`);
    // glass
    const gw = 360 * Math.sqrt(cap), gh = 480 * Math.sqrt(cap), gx = 1050 - gw / 2, gy = 840 - gh;
    const pIn = ap(t, u(12), 0.8);
    if (pIn > 0) {
      ctx.save(); ctx.globalAlpha *= pIn;
      ctx.fillStyle = 'rgba(0,0,0,0.08)'; ctx.beginPath(); ctx.ellipse(1050, 852, gw * 0.6, 22, 0, 0, Math.PI * 2); ctx.fill();
      rrect(ctx, gx, gy, gw, gh, 24); ctx.fillStyle = 'rgba(210,232,246,0.55)'; ctx.fill(); ctx.strokeStyle = C.forest; ctx.lineWidth = 6; ctx.stroke();
      // contents = fixed amount of vapor dots
      const n = 34; ctx.save(); rrect(ctx, gx, gy, gw, gh, 24); ctx.clip();
      for (let i = 0; i < n * ap(t, u(13), 1.5); i++) { const px = gx + 20 + hash01(i, 2) * (gw - 40) + Math.sin(t * 1.3 + i) * 10, py = gy + gh - 20 - hash01(i, 4) * Math.min(gh - 40, 300) + Math.cos(t + i) * 8; circle(ctx, px, py, 9); ctx.fillStyle = '#2b6cb0'; ctx.fill(); }
      ctx.restore();
      ctx.restore();
    }
    text(ctx, 'udara', 1050, 920, fU(34, 800), C.forest, 'center');
    show_(ctx, t, u(16), u(18), () => tag(ctx, 1050, 200, 'hangat: gelas besar', '', 1, C.clay));
    show_(ctx, t, u(18), u(19), () => tag(ctx, 1050, 200, 'dingin: gelas kecil', '', 1, C.blue));
    show_(ctx, t, u(19), SC.gelas[1], () => { tag(ctx, 1050, 200, '+1 °C', '', 1, C.forest); bigNum(ctx, 1560, 560, 7, '%', 1, 140, C.clay); text(ctx, 'kapasitas bertambah', 1560, 620, fU(28, 700), C.gray, 'center'); });
  });
}
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(); ctx.restore(); };

// ---------------------------------------------------------------- meet Si Gumpal; three humidity measures
function sGumpal(ctx, t) {
  scene(ctx, t, 'gumpal', '#cfe6f2', () => {
    sky(ctx, '#a9d4ee', '#eaf5fb'); sun(ctx, 1680, 160, 70, t); sawah(ctx, 820, t, W);
    const t0 = SC.gumpal[0]; const enter = sp(t, t0 + 0.2, SPRING.gentle);
    const gx = lerp(-200, 760, enter), gy = 470;
    const m = t >= u(30) ? 'rel' : t >= u(27) ? 'spec' : t >= u(25) ? 'abs' : 'intro';
    const expand = m === 'spec' && t > u(29) ? 0.15 * Math.sin((t - u(29)) * 1.6) ** 2 : 0;
    gumpal(ctx, gx, gy, 230 * (1 + expand), { t, temp: 0.75, mood: 'happy', glass: 0.95, fill: t < u(23) ? 0.75 * ap(t, u(22), 1.5) : 0.75, look: [1, 0] });
    tag(ctx, gx, 170, 'Si Gumpal', '', ap(t, tw('Gumpal', u(20)), 0.5) * (1 - ap(t, u(24), 0.4)), C.clay);
    show_(ctx, t, u(21), u(24), () => { thermo(ctx, 1180, 700, 300, 0.75, C.clay, '30 °C'); });
    show_(ctx, t, u(22), u(25), () => { text(ctx, 'kapasitas 20 g/kg', 1440, 440, fU(40, 800), C.forest); });
    show_(ctx, t, u(23), u(25), () => { text(ctx, 'isi 15 g/kg', 1440, 510, fU(40, 800), C.blue); });
    // measure 1: cube m3
    show_(ctx, t, u(25), u(27), () => { const x = 1180, y = 600, s = 180; ctx.strokeStyle = C.forest; ctx.lineWidth = 5; ctx.strokeRect(x, y, s, s); ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 60, y - 60); ctx.lineTo(x + s + 60, y - 60); ctx.lineTo(x + s, y); ctx.moveTo(x + s + 60, y - 60); ctx.lineTo(x + s + 60, y + s - 60); ctx.lineTo(x + s, y + s); ctx.stroke(); for (let i = 0; i < 10; i++) { circle(ctx, x + 20 + hash01(i, 3) * (s - 40), y + 20 + hash01(i, 5) * (s - 40), 8); ctx.fillStyle = C.blue; ctx.fill(); } bigNum(ctx, x + 520, y + 120, 0, '', 0); text(ctx, 'g / m³', x + 470, y + 120, fU(90, 800), C.forest, 'center'); });
    // measure 2: balance kg, stays when expanding
    show_(ctx, t, u(27), u(30), () => { const x = 1460, y = 760; ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - 200); ctx.moveTo(x - 160, y - 200); ctx.lineTo(x + 160, y - 200); ctx.stroke(); [-1, 1].forEach((s) => { ctx.beginPath(); ctx.moveTo(x + s * 160, y - 200); ctx.lineTo(x + s * 130, y - 120); ctx.lineTo(x + s * 190, y - 120); ctx.closePath(); ctx.stroke(); }); text(ctx, 'g / kg', x, y - 260, fU(90, 800), C.forest, 'center'); if (t > u(29)) tag(ctx, x, y + 70, 'tetap!', '', ap(t, u(29) + 1, 0.4), C.clay); });
    // measure 3: RH gauge
    show_(ctx, t, u(31), SC.gumpal[1] + 1, () => { const x = 1460, y = 640, r = 190; const v = 75 * ap(t, tw('tujuh', u(34)) - 0.3, 1.2, E.outCubic); ctx.lineWidth = 34; ctx.lineCap = 'round'; ctx.strokeStyle = '#e3e9ec'; ctx.beginPath(); ctx.arc(x, y, r, Math.PI * 0.8, Math.PI * 2.2); ctx.stroke(); ctx.strokeStyle = C.blue; ctx.beginPath(); ctx.arc(x, y, r, Math.PI * 0.8, Math.PI * (0.8 + 1.4 * v / 100)); ctx.stroke(); bigNum(ctx, x, y + 40, v, '%', 1, 120, C.forest); show_(ctx, t, u(33), 1e9, () => text(ctx, 'isi ÷ kapasitas', x, y + 120, fU(32, 800), C.gray, 'center')); });
  });
}

// ---------------------------------------------------------------- night: cooling to saturation
function sMalam(ctx, t) {
  const n = ap(t, SC.malam[0], 2.2, E.inOutCubic);
  sky(ctx, mix('#a9d4ee', '#13263a', n), mix('#eaf5fb', '#2a4560', n));
  const ex = E.inCubic(prog(t, SC.malam[1] - 0.35, SC.malam[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  if (n > 0.3) { ctx.save(); ctx.globalAlpha *= n; for (let i = 0; i < 60; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * 520, 1.5); ctx.fillStyle = '#fff'; ctx.fill(); } circle(ctx, 1640, 180, 46); ctx.fillStyle = '#f3e5a8'; ctx.fill(); circle(ctx, 1660, 168, 40); ctx.fillStyle = mix('#a9d4ee', '#13263a', n); ctx.fill(); ctx.restore(); }
  sawah(ctx, 820, t, W, n);
  const cool = ap(t, u(36), 9, E.inOutCubic); // capacity 20 -> 15
  const cap = lerp(20, 15, cool), fill = 15 / cap;
  const full = fill >= 0.999;
  gumpal(ctx, 760, 470, 230 * lerp(1, 0.94, cool), { t, temp: lerp(0.75, 0.15, cool), mood: full ? 'wow' : cool > 0.3 ? 'cold' : 'calm', shiver: cool > 0.3 ? cool : 0, glass: lerp(0.95, 0.95 * Math.sqrt(15 / 20), cool), fill });
  // RH gauge
  const x = 1460, y = 600, r = 170; const v = 100 * fill;
  ctx.lineWidth = 30; ctx.lineCap = 'round'; ctx.strokeStyle = 'rgba(255,255,255,0.25)'; ctx.beginPath(); ctx.arc(x, y, r, Math.PI * 0.8, Math.PI * 2.2); ctx.stroke(); ctx.strokeStyle = full ? C.amber : '#6fb3e6'; ctx.beginPath(); ctx.arc(x, y, r, Math.PI * 0.8, Math.PI * (0.8 + 1.4 * v / 100)); ctx.stroke();
  bigNum(ctx, x, y + 40, v, '%', 1, 110, n > 0.5 ? C.cream : C.forest);
  thermo(ctx, 1180, 880, 260, lerp(0.75, 0.35, cool), mix(C.clay, C.cold, cool), '');
  tag(ctx, 760, 170, 'jenuh', 'saturated', ap(t, u(41), 0.5) * (1 - ap(t, u(42) - 0.2, 0.3)), C.amber);
  tag(ctx, 760, 170, 'titik embun', 'dew point', ap(t, u(42), 0.5), C.blue);
  ctx.restore();
}

// ---------------------------------------------------------------- beyond dew point: drops, dew, fog, glass
function sEmbun(ctx, t) {
  const t0 = SC.embun[0];
  sky(ctx, '#2a4560', '#6f8ea8');
  const ex = E.inCubic(prog(t, SC.embun[1] - 0.35, SC.embun[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  const sub = t < u(45) ? 0 : t < u(46) ? 1 : t < u(47) ? 2 : 3;
  if (sub === 0) {
    sawah(ctx, 820, t, W, 0.7);
    gumpal(ctx, 860, 430, 220, { t, temp: 0.1, mood: 'wow', shiver: 0.8, glass: 0.85, fill: 1 });
    for (let i = 0; i < 18; i++) { const ph = (t * 0.6 + hash01(i, 2)) % 1; const k = ap(t, u(44), 0.6); if (k <= 0) continue; drop(ctx, 760 + hash01(i, 4) * 200, 520 + ph * 330, 12 * k, '#7fc1ee'); }
  } else if (sub === 1) {
    // morning dew + valley fog montage
    sky(ctx, '#f6d9b4', '#dceaf2'); sun(ctx, 300, 760, 70, t);
    ctx.fillStyle = '#7fae8a'; poly(ctx, [[0, 700], [500, 420], [960, 720], [1400, 380], [1920, 650], [1920, 1080], [0, 1080]]); ctx.fill();
    for (let k = 0; k < 4; k++) { ctx.fillStyle = `rgba(255,255,255,${0.35 + k * 0.08})`; ctx.beginPath(); ctx.ellipse(960 + Math.sin(t * 0.3 + k) * 80, 700 + k * 30, 700 - k * 80, 60, 0, 0, Math.PI * 2); ctx.fill(); }
    sawah(ctx, 860, t, W);
    for (let i = 0; i < 40; i++) { const x = (i * 49) % W, y = 900 + (i % 4) * 24; drop(ctx, x, y - 30, 8, 'rgba(220,240,255,0.95)'); }
    tag(ctx, 500, 220, 'embun', 'dew', 1, C.blue); tag(ctx, 1420, 220, 'kabut', 'fog', ap(t, tw('kabut', u(45)) - 0.2, 0.5), C.forestL);
  } else if (sub === 2) {
    sky(ctx, '#f3e7d4', '#f3e7d4'); ctx.fillStyle = '#e8d2ae'; ctx.fillRect(0, 760, W, 320);
    iceTea(ctx, 760, 640, 1.3, t, 1);
    // cold air shell around glass
    for (let i = 0; i < 26; i++) { const a = i / 26 * Math.PI * 2 + t * 0.4, r = 230 + Math.sin(t * 2 + i) * 10; circle(ctx, 760 + Math.cos(a) * r * 0.75, 560 + Math.sin(a) * r, 8); ctx.fillStyle = '#7fc1ee'; ctx.fill(); }
    gumpal(ctx, 1380, 480, 150, { t, temp: 0.2, mood: 'cold', shiver: 0.6, look: [-1, 0.3] });
    arrowLine(ctx, 1220, 500, 1000, 520, C.blue, 6, 20);
  } else {
    sky(ctx, '#f2efe8', '#f2efe8');
    const k1 = sp(t, u(48), SPRING.bouncy), k2 = sp(t, tw('bukan', u(48)), SPRING.bouncy);
    if (k1 > 0) { ctx.save(); ctx.translate(620, 540); ctx.scale(k1, k1); circle(ctx, 0, 0, 200); ctx.fillStyle = C.forest; ctx.fill(); check(ctx, 0, -10, 180, C.cream, clamp(k1)); text(ctx, 'didinginkan', 0, 290, fU(54, 800), C.forest, 'center'); ctx.restore(); }
    if (k2 > 0) { ctx.save(); ctx.translate(1300, 540); ctx.scale(k2, k2); circle(ctx, 0, 0, 200); ctx.fillStyle = C.clayD; ctx.fill(); cross(ctx, 0, 0, 90, C.cream, 34); text(ctx, 'dipanaskan', 0, 290, fU(54, 800), C.clayD, 'center'); ctx.restore(); }
  }
  ctx.restore();
}

run({
  DUR, no: 12, code: 'B01-12', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Kelembapan Udara', sub: 'gelas, uap air, dan titik embun',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-13 · Adiabatik dan Stabilitas',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['udara', 4], ['sumber', 7], ['gelas', 12], ['gumpal', 20], ['malam', 35], ['embun', 43], ['soal', 49], ['jebakan', 53], ['ringkas', 58], ['outro', 61]],
  TERMS: [
    ['Evapotranspirasi', 'evapotranspiration', '', 11],
    ['Kelembapan mutlak', 'absolute humidity', '', 26],
    ['Kelembapan spesifik', 'specific humidity', '', 28],
    ['Kelembapan relatif', 'relative humidity', '', 32],
    ['Jenuh', 'saturated', '', 41],
    ['Titik embun', 'dew point', '', 42],
  ],
  hook: { cards: [], punch: [4, ''] },
  soal: {
    q: 'Udara bersuhu 28 °C mengandung uap air 12 g/kg, sedangkan kapasitas maksimumnya 16 g/kg. Kelembapan relatif dan cara membuatnya jenuh adalah …',
    opts: ['75%, dipanaskan', '75%, didinginkan', '133%, didinginkan', '4%, ditambah uap', '75%, tekanan dinaikkan'], ans: 1, optFs: 30,
    ansT: () => tw('jawabannya', u(52) - 0.3),
    steps: () => [[u(50), 'RH = isi ÷ kapasitas', C.forest3, 30], [tw('dua', u(50)), '12 ÷ 16 = 75%', C.amber, 56], [u(51), 'jenuh: didinginkan', C.cream, 40], [tw('dua', u(51)), 'sampai kapasitas 12 g/kg', C.cream, 34]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(54), 'Kenaikan suhu menyebabkan kondensasi', 'Pendinginan yang membuat udara jenuh', u(55)],
      [u(56), 'RH tinggi pasti uap airnya banyak', 'Udara kutub bisa jenuh walau uapnya sedikit', u(57)]],
  },
  ringkas: {
    items: () => [[tw('suhu', u(59)), 'Suhu menentukan besar gelas'], [tw('relatif', u(59)), 'RH = seberapa penuh gelasnya'], [tw('penuh', u(59), 1), 'Gelas penuh = jenuh = titik embun']],
  },
  scenes: { hook: sHook, udara: sUdara, sumber: sSumber, gelas: sGelas, gumpal: sGumpal, malam: sMalam, embun: sEmbun },
});
