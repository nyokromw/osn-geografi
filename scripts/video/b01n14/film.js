// B01-14 · Efek Föhn dan Bayangan Hujan · OSNGEO.id — pure function of time (seconds). New style.
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, scene, fI } from './lib/kit.js';
import { gumpal, tag, bigNum, thermo, drop } from './lib/gumpal.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 240.4;
const u = (i) => U_(i).v0;
let IND = null, SUL = null;
const sky = (ctx, top, bot) => { const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, top); g.addColorStop(1, bot); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); };
const show_ = (ctx, t, a, b, fn) => { const k = ap(t, a, 0.4) * (1 - ap(t, b - 0.3, 0.3)); if (k <= 0) return; ctx.save(); ctx.globalAlpha *= k; fn(k); ctx.restore(); };

// mountain profile (world x in px, returns altitude m)
const X0 = 300, XP = 1500, X1 = 2700, HP = 1500;
function altX(x) { if (x <= X0 || x >= X1) return 0; if (x <= XP) { const f = (x - X0) / (XP - X0); return HP * Math.pow(f, 1.15); } const f = (X1 - x) / (X1 - XP); return HP * Math.pow(f, 1.1); }
function mountain(ctx, ox, base, sc, t, wet = 1, dry = 1) {
  const Y = (x) => base - altX(x) * sc;
  // back range
  ctx.fillStyle = '#c3d3c8'; ctx.beginPath(); ctx.moveTo(ox - 200, base); for (let x = -200; x <= 5200; x += 40) ctx.lineTo(ox + x, base - (altX(x * 0.9 + 150) * 0.7 + 60 * Math.sin(x * 0.01)) * sc); ctx.lineTo(ox + 5200, base); ctx.fill();
  // main: windward green, leeward brown
  ctx.beginPath(); ctx.moveTo(ox + X0 - 100, base); for (let x = X0; x <= XP; x += 20) ctx.lineTo(ox + x, Y(x)); ctx.lineTo(ox + XP, base); ctx.closePath(); ctx.fillStyle = mix('#c9b48a', '#5f9a5c', wet); ctx.fill();
  ctx.beginPath(); ctx.moveTo(ox + XP, base); for (let x = XP; x <= X1; x += 20) ctx.lineTo(ox + x, Y(x)); ctx.lineTo(ox + X1 + 100, base); ctx.closePath(); ctx.fillStyle = mix('#7fae6e', '#d4ac6e', dry); ctx.fill();
  // trees on windward
  for (let i = 0; i < 26; i++) { const x = X0 + 40 + i * 44; const y = Y(x); const sw = Math.sin(t * 1.4 + i) * 3; ctx.fillStyle = '#2f6e40'; ctx.beginPath(); ctx.moveTo(ox + x - 12 + sw, y + 4); ctx.lineTo(ox + x + sw, y - 34); ctx.lineTo(ox + x + 12 + sw, y + 4); ctx.fill(); }
  // dry shrubs on leeward
  for (let i = 0; i < 14; i++) { const x = XP + 60 + i * 80; const y = Y(x); circle(ctx, ox + x, y - 6, 8); ctx.fillStyle = '#a07a3e'; ctx.fill(); }
  // sea and lowland
  ctx.fillStyle = '#3c8fc2'; ctx.fillRect(ox - 2000, base, 2000 + X0 - 160, 300); ctx.fillStyle = '#e8d39c'; ctx.fillRect(ox + X0 - 160, base, 7000, 300);
}

// ---------------------------------------------------------------- hook: two worlds
function sHook(ctx, t) {
  scene(ctx, t, 'hook', '#cfe3ef', () => {
    sky(ctx, '#a9cfe6', '#eaf4fa');
    const sc = 0.42, ox = W / 2 - XP, base = 900;
    mountain(ctx, ox, base, sc, t);
    // left: rain clouds
    const kl = ap(t, u(0), 0.8); if (kl > 0) { ctx.save(); ctx.globalAlpha *= kl; [[420, 380], [600, 330], [780, 300]].forEach(([x, y], i) => { cloud(ctx, x + Math.sin(t * 0.4 + i) * 10, y, 1.8, '#b8c3cc'); rain(ctx, x, y + 40, 160, t + i, 8); }); ctx.restore(); }
    const kr = ap(t, u(1), 0.8); if (kr > 0) { ctx.save(); ctx.globalAlpha *= kr; sun(ctx, 1500, 260, 70, t); for (let i = 0; i < 10; i++) { const ph = (t * 0.6 + i / 10) % 1, x = 1150 + i * 60; ctx.strokeStyle = `rgba(224,121,79,${1 - ph})`; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x, 860 - ph * 120); ctx.bezierCurveTo(x + 10, 840 - ph * 120, x - 10, 820 - ph * 120, x, 800 - ph * 120); ctx.stroke(); } ctx.restore(); }
    show_(ctx, t, u(2), u(3), () => { card(ctx, 1240, 160, 600, 330, { r: 26 }); const pr = G.mapProj({ x: 1260, y: 180, w: 300, h: 290 }, [118.8, 121.6, -2.6, 0.2]); G.drawMap(ctx, SUL, pr, { t, depth: 4 }); const p = pr(119.87, -0.9); circle(ctx, p[0], p[1], 10); ctx.fillStyle = C.clayD; ctx.fill(); text(ctx, 'Palu', p[0] + 16, p[1] + 8, fU(24, 800), C.clayD); bigNum(ctx, 1700, 330, 500 + 300 * ap(t, u(2) + 2, 2), '', 1, 64, C.clay); text(ctx, 'mm / tahun', 1700, 380, fU(26, 700), C.gray, 'center'); });
    const q = sp(t, u(3), SPRING.bouncy); if (q > 0) { ctx.save(); ctx.translate(W / 2, 200); ctx.scale(q, q); text(ctx, '?', 0, 60, fD(200), C.clay, 'center'); ctx.restore(); }
  });
}

// ---------------------------------------------------------------- the journey (camera follows Gumpal)
function gx(t) {
  const k = (a, b, d) => ap(t, a, d, E.inOutCubic);
  let x = lerp(-150, 200, k(u(6), 0, 2));
  x = lerp(x, X0, k(u(8), 0, 2.5));
  x = lerp(x, 700, k(u(11), 0, u(13) - u(11)));
  x = lerp(x, XP, k(u(15), 0, u(17) - u(15)));
  x = lerp(x, X1 - 80, k(u(20), 0, u(24) - u(20)));
  return x;
}
function tempJ(x, t) { const a = altX(x); if (x <= XP) return a <= 500 ? 26 - a / 100 : 21 - (a - 500) / 100 * 0.6; return 15 + (HP - a) / 100; }
function sJalan(ctx, t) {
  const x = gx(t), a = altX(x), T = tempJ(x, t);
  const sc = 0.3, base = 960, camX = Math.max(x - 760, -300), ox = -camX;
  const lee = x > XP ? 1 : 0;
  sky(ctx, lee ? '#f3d9b0' : '#a9cfe6', lee ? '#fbefd9' : '#eaf4fa');
  const ex = E.inCubic(prog(t, SC.jalan[1] - 0.35, SC.jalan[1])); ctx.save(); ctx.globalAlpha = 1 - ex;
  if (lee) sun(ctx, W - 260, 200, 60, t);
  mountain(ctx, ox, base, sc, t);
  // LCL line
  const yL = base - 500 * sc; show_(ctx, t, u(13) - 0.5, 1e9, () => { ctx.setLineDash([14, 10]); ctx.strokeStyle = C.blue; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(ox + X0, yL); ctx.lineTo(ox + XP, yL); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'dasar awan · 500 m', ox + X0 + 10, yL - 12, fU(22, 800), C.blue); });
  // trail of rain clouds on windward
  const rainK = ap(t, u(15), 1) * (1 - ap(t, u(20) + 2, 1));
  if (rainK > 0) for (let i = 0; i < 5; i++) { const xx = 760 + i * 160; const yy = base - altX(xx) * sc - 160; ctx.save(); ctx.globalAlpha *= rainK; cloud(ctx, ox + xx, yy, 1.2, '#c3ccd4'); rain(ctx, ox + xx, yy + 30, 100, t + i, 6); ctx.restore(); }
  // Gumpal
  const gyS = base - a * sc - 150;
  const isCloud = x > 690 && x <= XP + 40 ? 1 : 0;
  gumpal(ctx, ox + x, gyS, 120, { t, temp: clamp((T - 12) / 20), cloud: isCloud * ap(t, u(13), 0.8), mood: lee ? 'hot' : T < 20 ? 'cold' : 'happy', sweat: lee ? clamp((T - 24) / 5) : 0, shiver: !lee && T < 18 ? 0.5 : 0, look: [1, lee ? 0.5 : -0.3] });
  if (isCloud && t > u(15) && t < u(20)) rain(ctx, ox + x, gyS + 90, 140, t, 7);
  // thermometer badge following Gumpal
  const th = ap(t, u(5), 0.6); if (th > 0) { ctx.save(); ctx.globalAlpha *= th; card(ctx, ox + x + 150, gyS - 120, 230, 120, { r: 22, bg: C.forest }); text(ctx, `${T.toFixed(T % 1 ? 1 : 0).replace('.', ',')} °C`, ox + x + 265, gyS - 52, fU(52, 800), C.amber, 'center'); text(ctx, `${Math.round(a)} m`, ox + x + 265, gyS - 16, fU(24, 700), C.forest3, 'center'); ctx.restore(); }
  // step pills at top
  const steps = [[u(10), 'naik kering', '−1 °C/100 m', C.clay], [u(14), 'naik basah', '−0,6 °C/100 m', C.blue], [u(19), 'turun kering', '+1 °C/100 m', C.clayD]];
  steps.forEach(([tt, s1, s2, col], i) => show_(ctx, t, tt, 1e9, (k) => { const on = (i === 0 && t < u(14)) || (i === 1 && t >= u(14) && t < u(19)) || (i === 2 && t >= u(19)); const X = 380 + i * 470; ctx.globalAlpha *= on ? 1 : 0.45; rrect(ctx, X - 210, 120, 420, 96, 48); ctx.fillStyle = col; ctx.fill(); text(ctx, `${i + 1}. ${s1}`, X, 162, fU(30, 800), C.cream, 'center'); text(ctx, s2, X, 198, fU(24, 700), C.cream, 'center'); }));
  show_(ctx, t, u(9), u(10) + 2, () => tag(ctx, ox + 900, base - 900 * sc * 0.6 - 80, 'lereng hadap angin', 'windward', 1, C.forestL));
  show_(ctx, t, u(20), u(22), () => tag(ctx, ox + 2100, base - 900 * sc * 0.6 - 80, 'lereng bawah angin', 'leeward', 1, C.clayD));
  // wind arrows
  for (let i = 0; i < 5; i++) { const ph = (t * 0.4 + i / 5) % 1; const wx = ox - 100 + ph * 500, wy = base - 60 - i * 30; ctx.globalAlpha = (1 - ex) * Math.sin(ph * Math.PI) * 0.7; arrowLine(ctx, wx, wy, wx + 60, wy, '#ffffff', 5, 16); ctx.globalAlpha = 1 - ex; }
  ctx.restore();
}

// ---------------------------------------------------------------- compare: graph of the journey
function sBanding(ctx, t) {
  scene(ctx, t, 'banding', '#f2efe8', () => {
    gumpal(ctx, 330, 520, 130, { t, temp: 0.55, mood: 'happy' }); bigNum(ctx, 330, 760, 26, ' °C', ap(t, u(26), 0.5), 72, C.blue);
    gumpal(ctx, 1590, 520, 130, { t, temp: 0.95, mood: 'hot', sweat: 1 }); bigNum(ctx, 1590, 760, 30, ' °C', ap(t, tw('tiba', u(26)), 0.5), 72, C.clayD);
    show_(ctx, t, u(27), 1e9, () => tag(ctx, 1590, 850, '+4 °C, kering', '', 1, C.clayD));
    // graph: altitude vs temperature
    const gx0 = 620, gy0 = 860, gw = 680, gh = 560; const X = (T) => gx0 + (T - 12) / 20 * gw, Y = (a) => gy0 - a / 1600 * gh;
    const kg = ap(t, u(28), 0.6);
    if (kg > 0) {
      ctx.save(); ctx.globalAlpha *= kg; ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx0, gy0 - gh); ctx.lineTo(gx0, gy0); ctx.lineTo(gx0 + gw, gy0); ctx.stroke();
      text(ctx, 'tinggi', gx0 - 10, gy0 - gh - 14, fU(22, 800), C.gray); text(ctx, 'suhu', gx0 + gw, gy0 + 34, fU(22, 800), C.gray, 'right');
      const pu = ap(t, u(29), 2.5, E.linear), pd = ap(t, u(30), 2.5, E.linear);
      ctx.lineWidth = 7; ctx.lineCap = 'round';
      ctx.strokeStyle = C.blue; ctx.beginPath(); ctx.moveTo(X(26), Y(0)); const up = [[26, 0], [21, 500], [15, 1500]]; const n1 = pu * 2; for (let i = 1; i <= Math.ceil(n1); i++) { const f = Math.min(1, n1 - (i - 1)); ctx.lineTo(lerp(X(up[i - 1][0]), X(up[i][0]), f), lerp(Y(up[i - 1][1]), Y(up[i][1]), f)); } ctx.stroke();
      if (pd > 0) { ctx.strokeStyle = C.clay; ctx.beginPath(); ctx.moveTo(X(15), Y(1500)); ctx.lineTo(lerp(X(15), X(30), pd), lerp(Y(1500), Y(0), pd)); ctx.stroke(); }
      show_(ctx, t, u(29), 1e9, () => text(ctx, 'naik: sebagian basah', X(19) - 30, Y(900), fU(24, 800), C.blue, 'right'));
      show_(ctx, t, u(30), 1e9, () => text(ctx, 'turun: kering', X(25) + 20, Y(700), fU(24, 800), C.clayD));
      show_(ctx, t, u(31), 1e9, () => { ctx.setLineDash([8, 8]); ctx.strokeStyle = C.amber; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(X(26), Y(0) - 10); ctx.lineTo(X(30), Y(0) - 10); ctx.stroke(); ctx.setLineDash([]); tag(ctx, (X(26) + X(30)) / 2, Y(0) - 60, 'panas laten', 'latent heat', 1, C.amber); });
      ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- names on the Indonesia map
const FOHN = [['Gending', 113.2, -7.75], ['Kumbang', 108.9, -6.85], ['Brubu', 119.4, -5.15], ['Bahorok', 98.6, 3.6], ['Wambraw', 136.1, -1.0]];
function sNama(ctx, t) {
  scene(ctx, t, 'nama', C.sand, () => {
    const box = { x: 80, y: 120, w: 1760, h: 820 }; const ext = [94, 142, -12.5, 8]; const pr = G.mapProj(box, [94, 142, -12.5, -12.5 + 48 * box.h / box.w]);
    G.drawMap(ctx, IND, pr, { t, depth: 8 });
    show_(ctx, t, u(32), 1e9, () => tag(ctx, W / 2, 190, 'angin fohn', 'foehn wind', 1, C.clay));
    FOHN.forEach(([n, lo, la], i) => { const t0 = tw(n, u(34)); const k = sp(t, t0 - 0.1, SPRING.bouncy); if (k <= 0) return; const p = pr(lo, la); ctx.save(); ctx.translate(p[0], p[1]); ctx.scale(k, k); ctx.fillStyle = '#8a7350'; poly(ctx, [[-50, 26], [-6, -50], [36, 26]]); ctx.fill(); for (let j = 0; j < 3; j++) { const ph = (t * 0.8 + j / 3) % 1; arrowLine(ctx, -4 + ph * 20, -30 + ph * 30, 40 + ph * 50, 8 + ph * 34, `rgba(224,121,79,${1 - ph})`, 5, 16); } ctx.restore(); pill(ctx, n, p[0], p[1] - 70 * k, fU(26, 800), C.clayD, C.cream, 14, 46, 'center'); });
  });
}
// ---------------------------------------------------------------- rain shadow: Palu vs wet slopes
function sBayang(ctx, t) {
  scene(ctx, t, 'bayang', '#e9eef1', () => {
    const z = ap(t, u(37) - 0.5, 1.6, E.inOutCubic);
    const box = { x: 0, y: 0, w: W, h: H };
    const c0 = [119.9, -0.9, 3.2], c1 = [119, -2, 26];
    const cx = lerp(c0[0], c1[0], z), cy = lerp(c0[1], c1[1], z), sx = lerp(c0[2], c1[2], z), sy = sx * H / W;
    const pr = G.mapProj(box, [cx - sx, cx + sx, cy - sy, cy + sy]);
    G.drawMap(ctx, IND, pr, { t, depth: 10 });
    // Palu valley ridges
    if (z < 0.6) { ctx.save(); ctx.globalAlpha *= 1 - z / 0.6; [[119.55, -0.4, -1.6], [120.25, -0.4, -1.6]].forEach(([lo, la0, la1]) => { for (let la = la0; la >= la1; la -= 0.12) { const p = pr(lo + Math.sin(la * 5) * 0.05, la); ctx.fillStyle = '#8a7350'; poly(ctx, [[p[0] - 26, p[1] + 16], [p[0], p[1] - 30], [p[0] + 26, p[1] + 16]]); ctx.fill(); } }); const p = pr(119.87, -0.9); sun(ctx, p[0], p[1] - 60, 40, t); circle(ctx, p[0], p[1], 12); ctx.fillStyle = C.clayD; ctx.fill(); pill(ctx, 'Palu: bayangan hujan', p[0], p[1] + 50, fU(28, 800), C.clayD, C.cream, 16, 50, 'center'); [[119.0, -1.0], [120.9, -1.2], [119.2, -0.2], [120.8, -0.3]].forEach(([lo, la], i) => { const q = pr(lo, la); cloud(ctx, q[0], q[1] - 40, 1.2, '#c3ccd4'); rain(ctx, q[0], q[1] - 10, 90, t + i, 6); }); ctx.restore(); }
    if (z > 0.6) { ctx.save(); ctx.globalAlpha *= (z - 0.6) / 0.4; [['lereng barat Bukit Barisan', 100.2, -0.8], ['Pegunungan Tengah Papua', 138.5, -4.0]].forEach(([n, lo, la], i) => { const q = pr(lo, la); cloud(ctx, q[0], q[1] - 50, 1.0, '#c3ccd4'); rain(ctx, q[0], q[1] - 20, 70, t + i, 6); pill(ctx, n, q[0], q[1] + 40, fU(22, 800), C.blue, C.cream, 12, 40, 'center'); }); const p = pr(119.87, -0.9); circle(ctx, p[0], p[1], 10); ctx.fillStyle = C.clayD; ctx.fill(); ctx.restore(); }
    show_(ctx, t, u(35), u(36), () => tag(ctx, W / 2, 140, 'bayangan hujan', 'rain shadow', 1, C.clayD));
    show_(ctx, t, u(37) + 1, 1e9, () => tag(ctx, W / 2, 140, 'lebih dari 4.000 mm / tahun', '', 1, C.blue));
  });
}

run({
  DUR, no: 14, code: 'B01-14', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'Efek Föhn', sub: 'dan bayangan hujan · perjalanan Si Gumpal melewati gunung',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 3: Air di Atmosfer', next: 'B01-15 · Awan dan Mekanisme Hujan',
  badge: true, noCaps: true, cam: true,
  SCN: [['hook', 0], ['jalan', 4], ['banding', 25], ['nama', 32], ['bayang', 35], ['soal', 38], ['jebakan', 43], ['ringkas', 47], ['outro', 51]],
  TERMS: [
    ['Lereng hadap angin', 'windward', '', 9],
    ['Lereng bawah angin', 'leeward', '', 20],
    ['Angin fohn', 'foehn wind', '', 32],
    ['Bayangan hujan', 'rain shadow', '', 35],
  ],
  hook: { cards: [], punch: [3, ''] },
  soal: {
    q: 'Udara 30 °C di permukaan laut naik melewati pegunungan 2.000 m dan jenuh di 600 m (kering 1 °C/100 m, jenuh 0,6 °C/100 m). Setelah melewati puncak, udara turun ke kota di ketinggian 200 m. Suhu di kota tersebut adalah …',
    opts: ['30,0 °C', '24,0 °C', '15,6 °C', '33,6 °C', '35,6 °C'], ans: 3, optFs: 34,
    ansT: () => tw('jawabannya', u(42) - 0.3),
    steps: () => [[u(39), '1) naik kering 600 m', C.forest3, 28], [tw('menjadi', u(39)), '30 − 6 = 24 °C', C.cream, 44], [u(40), '2) naik jenuh 1.400 m', C.forest3, 28], [tw('menjadi', u(40)), '24 − 8,4 = 15,6 °C', C.cream, 44], [u(41), '3) turun kering 1.800 m', C.forest3, 28], [tw('menjadi', u(41)), '15,6 + 18 = 33,6 °C', C.amber, 52]],
  },
  jebakan: {
    title: 'Dua jebakan',
    items: () => [[u(44), 'Saat turun memakai laju basah', 'Turun: laju KERING (uap sudah habis)', tw('karena', u(44))],
      [u(45), 'Turun dihitung sampai permukaan laut', 'Hitung dari puncak sampai KOTA tujuan', u(46)]],
  },
  ringkas: {
    items: () => [[u(48), 'Naik kering, lalu basah · turun kering'], [tw('panas', u(49)), 'Lereng bawah angin lebih panas dan kering'], [tw('bayangan', u(49)), 'Lereng bawah angin = bayangan hujan']],
  },
  scenes: { hook: sHook, jalan: sJalan, banding: sBanding, nama: sNama, bayang: sBayang },
  async init() {
    const W50 = await fetch('assets/world50.json').then((r) => r.json());
    IND = G.subset(W50, [90, 145, -15, 10]); SUL = G.subset(W50, [116, 124, -4, 2]);
  },
});
