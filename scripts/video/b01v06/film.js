// B01-05 · Suhu Udara · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 294.6;

function thermo(ctx, x, y, h, frac, color) {
  rrect(ctx, x - 16, y - h, 32, h, 16); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  circle(ctx, x, y + 14, 28); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); circle(ctx, x, y + 14, 19); ctx.fillStyle = color; ctx.fill();
  const fh = (h - 24) * clamp(frac); rrect(ctx, x - 8, y - fh - 4, 16, fh + 16, 8); ctx.fillStyle = color; ctx.fill();
}
function tree(ctx, x, y, s, col = '#3f8a52') { ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 3 * s, y - 24 * s, 6 * s, 24 * s); circle(ctx, x, y - 34 * s, 17 * s); ctx.fillStyle = col; ctx.fill(); }
function flake(ctx, x, y, r, col = '#ffffff') { ctx.strokeStyle = col; ctx.lineWidth = 3; for (let k = 0; k < 3; k++) { const a = k * Math.PI / 3; ctx.beginPath(); ctx.moveTo(x - Math.cos(a) * r, y - Math.sin(a) * r); ctx.lineTo(x + Math.cos(a) * r, y + Math.sin(a) * r); ctx.stroke(); } }
const YAK = [-39, -35, -22, -7, 6, 16, 19, 15, 6, -8, -28, -37], JKT = [27, 27, 27.5, 28, 28.3, 28, 27.8, 28, 28.3, 28.4, 28, 27.6];

const hook = {
  cards: [
    [2, 'Siberia', '−40 °C sampai +25 °C dalam setahun', (ctx, x, y, t) => { ctx.fillStyle = '#dbe8ef'; ctx.fillRect(x, y, 560, 460); const f = 0.5 + 0.45 * Math.sin(t * 1.4); thermo(ctx, x + 280, y + 380, 320, f, mix(C.cold, C.clay, f)); text(ctx, f > 0.5 ? '+25 °C' : '−40 °C', x + 330, y + 150, fU(48, 700), f > 0.5 ? C.clayD : C.blue); }, '#dbe8ef'],
    [3, 'Jakarta', 'hampir sama sepanjang tahun', (ctx, x, y, t) => { thermo(ctx, x + 180, y + 380, 320, 0.72 + 0.02 * Math.sin(t * 1.4), C.clay); ctx.strokeStyle = C.clay; ctx.lineWidth = 6; ctx.beginPath(); for (let i = 0; i < 12; i++) { const xx = x + 260 + i * 22, yy = y + 200 + Math.sin(i) * 4; i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); text(ctx, '±27–28 °C', x + 260, y + 160, fU(36, 700), C.clayD); }],
    [4, 'Dieng', 'embun membeku merusak kentang', (ctx, x, y, t) => { ctx.fillStyle = '#e7eef3'; ctx.fillRect(x, y, 560, 460); ctx.fillStyle = '#7a8f5a'; ctx.fillRect(x, y + 300, 560, 160); for (let i = 0; i < 7; i++) { circle(ctx, x + 50 + i * 75, y + 300, 26); ctx.fillStyle = mix('#3f8a52', '#e9f2f7', 0.5 + 0.3 * Math.sin(t + i)); ctx.fill(); flake(ctx, x + 50 + i * 75, y + 296, 12); } for (let i = 0; i < 10; i++) flake(ctx, x + 40 + hash01(i, 2) * 480, y + 40 + ((t * 30 + hash01(i, 4) * 200) % 220), 8, '#9fc4dd'); }, '#e7eef3'],
  ],
  punch: [5, 'suhu udara'],
};

function sFaktor(ctx, t) {
  scene(ctx, t, 'faktor', C.sand, () => {
    title(ctx, t, 'faktor', 'Enam faktor pengendali suhu udara');
    const F = [['Lintang', 'lintang'], ['Ketinggian tempat', 'ketinggian'], ['Jarak dari laut', 'jarak'], ['Arus laut', 'arus'], ['Tutupan awan', 'tutupan'], ['Jenis permukaan', 'jenis']];
    F.forEach(([s, w], i) => {
      const k = sp(t, tw(w, u(7).v0) - 0.1, SPRING.bouncy); if (k <= 0) return;
      const x = 160 + (i % 3) * 560, y = 320 + Math.floor(i / 3) * 290;
      ctx.save(); ctx.translate(x + 240, y + 120); ctx.scale(k, k); ctx.translate(-(x + 240), -(y + 120));
      card(ctx, x, y, 480, 250, { r: 26 }); const cx = x + 110, cy = y + 125;
      if (i === 0) { circle(ctx, cx, cy, 60); ctx.fillStyle = '#7fb7d6'; ctx.fill(); ctx.strokeStyle = '#fff'; ctx.lineWidth = 3; [-30, 0, 30].forEach((d) => { ctx.beginPath(); ctx.moveTo(cx - Math.sqrt(3600 - d * d), cy + d); ctx.lineTo(cx + Math.sqrt(3600 - d * d), cy + d); ctx.stroke(); }); }
      if (i === 1) { ctx.fillStyle = '#9a8670'; poly(ctx, [[cx - 70, cy + 55], [cx, cy - 60], [cx + 70, cy + 55]]); ctx.fill(); }
      if (i === 2) { ctx.fillStyle = '#5aa0c8'; ctx.fillRect(cx - 70, cy - 50, 60, 100); ctx.fillStyle = '#d9c28f'; ctx.fillRect(cx - 10, cy - 50, 80, 100); }
      if (i === 3) { ctx.fillStyle = '#5aa0c8'; ctx.fillRect(cx - 70, cy - 50, 140, 100); arrowLine(ctx, cx - 55, cy + 20, cx + 55, cy - 20, C.clay, 8, 22); }
      if (i === 4) cloud(ctx, cx, cy + 10, 1.4);
      if (i === 5) { [['#7d8791', -70], ['#3f8a52', -20], ['#d9c28f', 30]].forEach(([c, dx]) => { ctx.fillStyle = c; ctx.fillRect(cx + dx, cy - 40, 44, 80); }); }
      text(ctx, `${i + 1}`, x + 440, y + 60, fU(40, 700), C.clay, 'right'); wrap(ctx, s, fU(34, 700), 250).forEach((l, j) => text(ctx, l, x + 200, y + 120 + j * 40, fU(34, 700), C.ink));
      ctx.restore();
    });
  });
}

function sDarat(ctx, t) {
  scene(ctx, t, 'darat', C.sand, () => {
    title(ctx, t, 'darat', 'Darat dan laut: siapa cepat panas?');
    // heating comparison
    show(ctx, t, u(9).v0, () => {
      card(ctx, 110, 300, 760, 600, { r: 28 });
      ctx.fillStyle = '#d9c28f'; ctx.fillRect(140, 640, 340, 230); ctx.fillStyle = '#5aa0c8'; ctx.fillRect(500, 640, 340, 230);
      text(ctx, 'daratan', 310, 770, fU(30, 700), '#5a4326', 'center'); text(ctx, 'laut', 670, 770, fU(30, 700), '#fff', 'center');
      const ph = ap(t, u(10).v0, 0.5) * Math.sin(t * 1.2);
      thermo(ctx, 310, 600, 240, 0.5 + 0.42 * ph, C.clay); thermo(ctx, 670, 600, 240, 0.5 + 0.08 * ph, C.blue);
      show(ctx, t, u(10).v0, () => { text(ctx, 'cepat panas, cepat dingin', 310, 830, fU(22, 700), '#5a4326', 'center'); text(ctx, 'lambat panas, lambat dingin', 670, 830, fU(22, 700), '#fff', 'center'); });
      text(ctx, 'kapasitas panas laut besar · panas masuk hingga puluhan meter', 490, 345, fU(20, 600), C.gray, 'center');
    });
    // monthly chart
    const pc = ap(t, u(11).v0, 1.6, E.linear);
    if (pc > 0) {
      card(ctx, 920, 300, 900, 600, { r: 28 });
      const gx = 1010, gy = 800, gw = 760, gh = 400; const Y = (v) => gy - (v + 45) / 80 * gh, X = (m) => gx + m / 11 * gw;
      ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
      [-40, -20, 0, 20].forEach((v) => text(ctx, `${v}`.replace('-', '−'), gx - 12, Y(v) + 8, fU(20, 600), C.gray, 'right'));
      'JFMAMJJASOND'.split('').forEach((m, i) => text(ctx, m, X(i), gy + 30, fU(20, 600), C.gray, 'center'));
      text(ctx, 'suhu rata-rata bulanan (°C)', gx, gy - gh - 8, fU(20, 600), C.gray);
      [[YAK, C.blue, 'Siberia (Yakutsk)'], [JKT, C.clay, 'Jakarta']].forEach(([d, col, n]) => { ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath(); for (let i = 0; i <= 11 * pc; i++) i ? ctx.lineTo(X(i), Y(d[i])) : ctx.moveTo(X(i), Y(d[i])); ctx.stroke(); if (pc > 0.95) text(ctx, n, X(11) - 10, Y(d[11]) + (col === C.blue ? 40 : -20), fU(22, 700), col, 'right'); });
      show(ctx, t, tw('selisih', u(11).v0) + 0.6, () => { ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(X(6) + 30, Y(19)); ctx.lineTo(X(6) + 30, Y(-39)); ctx.stroke(); pill(ctx, 'amplitudo ±58 °C', X(6) + 50, Y(-10), fU(22, 700), C.blue, C.cream, 14, 40); });
      show(ctx, t, u(12).v0, () => pill(ctx, 'maritim: amplitudo kecil', 1190, 342, fU(20, 700), C.clay, C.cream, 12, 38));
      show(ctx, t, u(13).v0, () => pill(ctx, 'kontinental: amplitudo besar', 1460, 342, fU(20, 700), C.blue, C.cream, 12, 38));
      show(ctx, t, u(15).v0, () => pill(ctx, 'Indonesia: amplitudo tahunan hanya ±1–2 °C', 1370, 870, fU(24, 700), C.forest, C.cream, 18, 46, 'center'));
    }
  });
}

function sKetinggian(ctx, t) {
  scene(ctx, t, 'ketinggian', '#eef3f6', () => {
    title(ctx, t, 'ketinggian', 'Ketinggian: naik 100 m, suhu turun 0,6 °C');
    card(ctx, 110, 290, 880, 610, { r: 28 });
    const base = 860, top = 360; const Y = (h) => base - h / 3000 * (base - top);
    ctx.fillStyle = '#9a8670'; poly(ctx, [[150, base], [560, Y(3000)], [960, base]]); ctx.fill();
    ctx.fillStyle = '#5aa0c8'; ctx.fillRect(110, base, 880, 30);
    const pts = [[0, 26.3], [1000, 20.3], [2000, 14.3], [3000, 8.3]];
    pts.forEach(([h, T], i) => show(ctx, t, u(17).v0 + i * 0.9, () => { const x = lerp(150, 560, h / 3000); circle(ctx, x, Y(h), 10); ctx.fillStyle = C.clay; ctx.fill(); text(ctx, `${h.toLocaleString('id-ID')} m`, x - 20, Y(h) + 8, fU(22, 700), C.ink, 'right'); pill(ctx, `${T.toString().replace('.', ',')} °C`, x + 24, Y(h), fU(24, 700), mix(C.clay, C.cold, i / 3), C.cream, 14, 42); }));
    show(ctx, t, u(18).v0, () => text(ctx, 'lapse rate', 700, 450, fI(48), C.clayD));
    show(ctx, t, u(19).v0, () => {
      card(ctx, 1040, 300, 780, 270, { r: 28, bg: C.forest });
      text(ctx, 'Rumus Braak (Indonesia)', 1080, 360, fU(28, 600), C.forest3);
      text(ctx, 'T = 26,3 − 0,6 h', 1080, 460, fU(70, 700), C.amber);
      show(ctx, t, tw('dengan', u(20).v0), () => text(ctx, 'h dalam ratusan meter', 1080, 530, fU(28, 600), C.cream));
    });
    show(ctx, t, u(21).v0, () => {
      card(ctx, 1040, 610, 780, 290, { r: 28 });
      text(ctx, 'Suhu satu titik sudah diketahui?', 1080, 668, fU(28, 700), C.clayD);
      text(ctx, 'pakai bentuk SELISIH', 1080, 712, fU(28, 700), C.ink);
      show(ctx, t, u(22).v0, () => { text(ctx, 'T baru = T lama − 0,6 × selisih h', 1080, 790, fU(38, 700), C.forest); text(ctx, 'selisih h dalam ratusan meter', 1080, 840, fU(24, 600), C.gray); });
    });
  });
}

const ZONES = [['Zona panas', '0–700 m', '26,3–22 °C', 'padi, kelapa, tebu', 0, 700, '#e9a072', 24], ['Zona sedang', '700–1.500 m', '22–17,1 °C', 'kopi, sayuran', 700, 1500, '#e8c27a', 25], ['Zona sejuk', '1.500–2.500 m', '17,1–11,1 °C', 'teh, sayuran dataran tinggi', 1500, 2500, '#a9cfa0', 26], ['Zona dingin', 'di atas 2.500 m', 'di bawah 11,1 °C', 'lumut, rerumputan', 2500, 3600, '#bcd6e6', 27]];
function sJunghuhn(ctx, t) {
  scene(ctx, t, 'junghuhn', C.sand, () => {
    title(ctx, t, 'junghuhn', 'Empat zona suhu Junghuhn');
    const base = 880, top = 300, Y = (h) => base - h / 3600 * (base - top), cx = 560;
    ctx.save(); poly(ctx, [[110, base], [cx, top], [1010, base]]); ctx.clip();
    ZONES.forEach(([n, , , , a, b, col, ui]) => { ctx.globalAlpha = ap(t, U_(ui).v0 - 0.3, 0.6) * 0.9 + 0.1; ctx.fillStyle = col; ctx.fillRect(110, Y(b), 900, Y(a) - Y(b)); });
    ctx.restore();
    ZONES.forEach(([n, h, T, c, a, b, col, ui], i) => {
      const k = sp(t, U_(ui).v0 - 0.1, SPRING.snappy); if (k <= 0) return; const y = Y((a + Math.min(b, 3300)) / 2);
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4);
      ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.setLineDash([6, 6]); ctx.beginPath(); ctx.moveTo(cx + (base - y) * 0.75 - 40, y); ctx.lineTo(1080, y); ctx.stroke(); ctx.setLineDash([]);
      card(ctx, 1080, y - 62, 740, 124, { r: 22 }); rrect(ctx, 1080, y - 62, 16, 124, 8); ctx.fillStyle = col; ctx.fill();
      text(ctx, n, 1116, y - 16, fU(32, 700), C.ink); text(ctx, `${h} · ${T}`, 1790, y - 16, fU(24, 700), C.gray, 'right');
      text(ctx, c, 1116, y + 34, fU(28, 600), C.forest);
      ctx.restore();
    });
  });
}

function sInversi(ctx, t) {
  scene(ctx, t, 'inversi', '#eef3f6', () => {
    title(ctx, t, 'inversi', 'Inversi suhu: suhu justru naik ke atas');
    card(ctx, 110, 290, 780, 610, { r: 28 });
    const gx = 200, gy = 820, gw = 640, gh = 460; const X = (T) => gx + (T - 5) / 25 * gw, Y = (h) => gy - h / 2000 * gh;
    ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
    text(ctx, 'ketinggian', gx - 10, gy - gh - 16, fU(20, 700), C.gray); text(ctx, 'suhu', gx + gw, gy + 34, fU(20, 700), C.gray, 'right');
    const pn = ap(t, u(28).v0, 1.0, E.linear);
    if (pn > 0) { ctx.strokeStyle = C.forestL; ctx.lineWidth = 5; ctx.setLineDash([12, 8]); ctx.beginPath(); ctx.moveTo(X(26), Y(0)); ctx.lineTo(lerp(X(26), X(14), pn), lerp(Y(0), Y(2000), pn)); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'normal', X(15) + 16, Y(1750), fU(22, 700), C.forestL); }
    const pi = ap(t, u(30).v0, 1.2, E.linear);
    if (pi > 0) { const P = [[17, 0], [22, 500], [19, 1100], [14, 2000]]; ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.beginPath(); const n = Math.min(3, pi * 3); for (let i = 0; i <= Math.floor(n); i++) i ? ctx.lineTo(X(P[i][0]), Y(P[i][1])) : ctx.moveTo(X(P[0][0]), Y(P[0][1])); const f = n - Math.floor(n), j = Math.floor(n); if (j < 3) ctx.lineTo(lerp(X(P[j][0]), X(P[j + 1][0]), f), lerp(Y(P[j][1]), Y(P[j + 1][1]), f)); ctx.stroke(); ctx.fillStyle = 'rgba(224,121,79,0.14)'; ctx.fillRect(gx, Y(500), gw, Y(0) - Y(500)); text(ctx, 'lapisan inversi', gx + 16, Y(250), fU(22, 700), C.clayD); }
    show(ctx, t, u(31).v0, () => pill(ctx, 'temperature inversion', 640, 322, fU(26, 700), C.clay, C.cream, 18, 48, 'center'));
    // right panel: stage by unit
    const stg = [[u(32).v0, 'Inversi radiasi', 'radiation inversion', 'malam cerah, tenang: tanah cepat dingin'], [u(33).v0, 'Aliran udara dingin', 'cold air drainage', 'udara dingin turun dari lereng ke lembah'], [u(34).v0, 'Polutan terperangkap', 'contoh: cekungan Bandung', 'lapisan inversi sangat stabil'], [u(35).v0, 'Embun upas Dieng', 'frost', 'cerah, kering, tinggi, kaldera']];
    const cur = stg.reduce((a, s, i) => (t >= s[0] - 0.2 ? i : a), -1);
    if (cur >= 0) {
      const [t0, a, en, d] = stg[cur]; const k = sp(t, t0 - 0.1, SPRING.snappy);
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4);
      card(ctx, 940, 300, 880, 600, { r: 28 });
      ctx.save(); rrect(ctx, 960, 320, 840, 380, 22); ctx.clip();
      const night = cur !== 2; ctx.fillStyle = night ? '#16263a' : '#dfe6ec'; ctx.fillRect(960, 320, 840, 380);
      if (night) { for (let i = 0; i < 30; i++) { circle(ctx, 960 + hash01(i, 3) * 840, 330 + hash01(i, 5) * 150, 1.5 + hash01(i, 6) * 1.5); ctx.fillStyle = '#fff'; ctx.fill(); } }
      ctx.fillStyle = cur === 3 ? '#7a8f5a' : '#8a7350'; poly(ctx, [[960, 420], [1180, 640], [1580, 640], [1800, 420], [1800, 700], [960, 700]]); ctx.fill();
      if (cur === 0) { for (let j = 0; j < 4; j++) arrowLine(ctx, 1200 + j * 110, 630, 1200 + j * 110, 560 - ((t * 40 + j * 20) % 60), '#f2b13a', 5, 16); text(ctx, 'panas tanah lepas ke angkasa', 1380, 380, fU(24, 700), '#fff', 'center'); }
      if (cur === 1) { const g = ctx.createLinearGradient(0, 560, 0, 650); g.addColorStop(0, 'rgba(120,180,230,0)'); g.addColorStop(1, 'rgba(120,180,230,0.85)'); ctx.fillStyle = g; ctx.fillRect(1180, 560, 400, 90); for (let j = 0; j < 3; j++) { const ph = (t * 0.5 + j / 3) % 1; arrowLine(ctx, lerp(990, 1170, ph), lerp(440, 620, ph), lerp(1010, 1190, ph), lerp(460, 640, ph), '#bfe0ff', 5, 16); arrowLine(ctx, lerp(1770, 1590, ph), lerp(440, 620, ph), lerp(1750, 1570, ph), lerp(460, 640, ph), '#bfe0ff', 5, 16); } }
      if (cur === 2) { ctx.fillStyle = 'rgba(120,120,120,0.55)'; ctx.fillRect(1000, 520, 760, 120); ctx.strokeStyle = C.clay; ctx.lineWidth = 6; ctx.setLineDash([16, 10]); ctx.beginPath(); ctx.moveTo(1000, 520); ctx.lineTo(1760, 520); ctx.stroke(); ctx.setLineDash([]); text(ctx, 'tutup inversi', 1380, 505, fU(24, 700), C.clayD, 'center'); for (let j = 0; j < 6; j++) { ctx.fillStyle = '#6b6b6b'; ctx.fillRect(1220 + j * 55, 580, 30, 60); } }
      if (cur === 3) { for (let i = 0; i < 9; i++) { circle(ctx, 1220 + i * 42, 640, 16); ctx.fillStyle = '#d8e8ee'; ctx.fill(); flake(ctx, 1220 + i * 42, 638, 9, '#5a8db1'); } text(ctx, 'embun membeku di daun kentang', 1380, 380, fU(24, 700), '#fff', 'center'); }
      ctx.restore();
      text(ctx, a, 990, 760, fU(40, 700), C.ink); text(ctx, en, 990, 810, fI(36), C.clayD); text(ctx, d, 990, 860, fU(26, 600), C.gray);
      ctx.restore();
    }
  });
}

function sIsoterm(ctx, t) {
  scene(ctx, t, 'isoterm', C.sand, () => {
    title(ctx, t, 'isoterm', 'Isoterm: garis bersuhu sama');
    const bx = 110, by = 290, bw = 1700, bh = 610;
    ctx.save(); rrect(ctx, bx, by, bw, bh, 28); ctx.clip(); ctx.fillStyle = '#cfe3ef'; ctx.fillRect(bx, by, bw, bh);
    ctx.fillStyle = C.land; ctx.strokeStyle = '#a8916a'; ctx.lineWidth = 2;
    poly(ctx, [[bx, by], [bx + 560, by], [bx + 620, by + 140], [bx + 520, by + 300], [bx + 430, by + 420], [bx + 330, by + 520], [bx + 250, by + bh], [bx, by + bh]]); ctx.fill(); ctx.stroke();
    poly(ctx, [[bx + 1150, by], [bx + bw, by], [bx + bw, by + bh], [bx + 1350, by + bh], [bx + 1260, by + 480], [bx + 1180, by + 330], [bx + 1230, by + 220], [bx + 1120, by + 120]]); ctx.fill(); ctx.stroke();
    text(ctx, 'Amerika Utara', bx + 200, by + 200, fU(26, 700), '#8a7350'); text(ctx, 'Eropa', bx + 1450, by + 160, fU(26, 700), '#8a7350'); text(ctx, 'Afrika', bx + 1500, by + 520, fU(26, 700), '#8a7350'); text(ctx, 'Samudra Atlantik', bx + 780, by + 400, fU(26, 700), '#4a7da0', 'center');
    const p = ap(t, u(36).v0 + 0.5, 2.5, E.linear);
    [[0, '0 °C'], [1, '10 °C'], [2, '20 °C']].forEach(([k, lab]) => {
      const y0 = by + 110 + k * 160; const bend = ap(t, u(38).v0, 1.5) * (90 - k * 25);
      ctx.strokeStyle = mix(C.cold, C.clay, k / 2); ctx.lineWidth = 5; ctx.beginPath();
      for (let i = 0; i <= 100 * p; i++) { const f = i / 100, x = bx + f * bw; const y = y0 + 18 * Math.sin(f * 7) - bend * Math.exp(-(((f - 0.66) / 0.1) ** 2)); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.stroke(); if (p > 0.3) pill(ctx, lab, bx + 60, y0, fU(22, 700), mix(C.cold, C.clay, k / 2), C.cream, 12, 38);
    });
    show(ctx, t, u(37).v0, () => { ctx.setLineDash([16, 10]); ctx.strokeStyle = C.clayD; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(bx, by + 560); for (let i = 0; i <= 50; i++) { const f = i / 50; ctx.lineTo(bx + f * bw, by + 560 - 30 * Math.sin(f * 4)); } ctx.stroke(); ctx.setLineDash([]); pill(ctx, 'ekuator termal · thermal equator', bx + 900, by + 575, fU(22, 700), C.clayD, C.cream, 14, 40, 'center'); });
    show(ctx, t, tw('Arus', u(38).v0), () => { ctx.strokeStyle = C.clay; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(bx + 450, by + 470); ctx.bezierCurveTo(bx + 700, by + 380, bx + 900, by + 260, bx + 1150, by + 170); ctx.stroke(); arrowLine(ctx, bx + 1100, by + 190, bx + 1170, by + 160, C.clay, 12, 36); pill(ctx, 'Arus Teluk · Gulf Stream', bx + 820, by + 250, fU(24, 700), C.clay, C.cream, 16, 44, 'center'); });
    ctx.restore();
    text(ctx, 'skema, tidak berskala', bx + bw - 20, by + bh - 16, fU(18, 500), C.gray, 'right');
  });
}

run({
  DUR, no: 5, code: 'B01-05', chip: 'BAB 1 · IKLIM · VIDEO #5 · DASAR–MENENGAH', title: 'Suhu Udara', sub: 'amplitudo, ketinggian, zona Junghuhn, inversi, isoterm',
  next: '#6 · B01-06 · Tekanan Udara dan Lahirnya Angin',
  SCN: [['hook', 0], ['faktor', 6], ['darat', 8], ['ketinggian', 16], ['junghuhn', 23], ['inversi', 28], ['isoterm', 36], ['soal', 39], ['jebakan', 45], ['ringkas', 48], ['outro', 53]],
  TERMS: [
    ['Amplitudo suhu', 'temperature range', 'Selisih suhu tertinggi dan terendah', 11],
    ['Iklim maritim', 'maritime climate', 'Dekat laut: amplitudo kecil', 12],
    ['Iklim kontinental', 'continental climate', 'Pedalaman benua: amplitudo sangat besar', 13],
    ['Kontinentalitas', 'continentality', 'Sifat daratan yang memperbesar amplitudo suhu', 14],
    ['Laju penurunan suhu', 'lapse rate', 'Turun ±0,6 °C setiap naik 100 m', 18],
    ['Rumus Braak', '', 'T = 26,3 − 0,6 h (h dalam ratusan meter)', 19],
    ['Zona Junghuhn', '', 'Empat zona suhu menurut ketinggian di Jawa', 23],
    ['Inversi suhu', 'temperature inversion', 'Suhu naik terhadap ketinggian pada suatu lapisan', 31],
    ['Inversi radiasi', 'radiation inversion', 'Malam cerah dan tenang, tanah cepat dingin', () => tw('radiation', u(32).v0)],
    ['Aliran udara dingin', 'cold air drainage', 'Udara dingin mengalir turun ke lembah', () => tw('cold', u(33).v0)],
    ['Embun upas', 'frost', 'Embun membeku; di Dieng merusak tanaman', 35],
    ['Isoterm', 'isotherm', 'Garis yang menghubungkan tempat bersuhu sama', 36],
    ['Ekuator termal', 'thermal equator', 'Garis tempat terpanas di setiap garis bujur', 37],
    ['Arus Teluk', 'Gulf Stream', 'Arus hangat Atlantik yang menghangatkan Eropa Barat', () => tw('Arus', u(38).v0)],
  ],
  hook,
  soal: {
    q: 'Suhu di Kota P (200 m) tercatat 27,0 °C. Bila laju penurunan normal berlaku, suhu di puncak bukit Q (1.400 m) pada saat yang sama dan zona Junghuhn-nya adalah …',
    opts: ['17,9 °C, zona sejuk', '19,8 °C, zona sedang', '18,0 °C, zona sedang', '26,3 °C, zona panas', '19,8 °C, zona sejuk'], ans: 1, optFs: 30,
    ansT: () => tw('jawabannya', u(44).v0 - 0.3),
    steps: () => [[u(40).v0, '1) Selisih tinggi', C.forest3, 28], [tw('yaitu', u(40).v0), '1.400 − 200 = 1.200 m = 12 ratus m', C.cream, 34],
      [u(41).v0, '2) Penurunan suhu', C.forest3, 28], [tw('yaitu', u(41).v0), '0,6 × 12 = 7,2 °C', C.cream, 38],
      [u(42).v0, '3) Suhu di Q', C.forest3, 28], [tw('sembilan', u(42).v0), '27,0 − 7,2 = 19,8 °C', C.amber, 46], [u(43).v0, '1.400 m: zona sedang (700–1.500 m)', C.cream, 32]],
  },
  jebakan: {
    title: 'Jebakan yang sering muncul',
    items: () => [[u(46).v0, 'Memakai 26,3 − 0,6 h padahal suhu awal diketahui', 'Suhu awal diketahui: pakai bentuk SELISIH', u(47).v0]],
    extra: (ctx, t) => show(ctx, t, u(47).v0 + 0.3, () => { card(ctx, 110, 560, 1700, 220, { r: 26, bg: C.forest }); text(ctx, 'T baru = T lama − 0,6 × selisih h (ratusan m)', 960, 690, fU(48, 700), C.amber, 'center'); }),
  },
  ringkas: {
    items: () => [[tw('laut', u(49).v0), 'Laut meredam perubahan suhu: amplitudo kecil'], [tw('ketinggian', u(49).v0), 'Naik 100 m, suhu turun 0,6 °C'], [tw('inversi', u(49).v0), 'Inversi: polutan terperangkap dekat permukaan'], [u(50).v0, 'Tahap 1 selesai! Berikutnya Tahap 2: angin']],
  },
  scenes: { faktor: sFaktor, darat: sDarat, ketinggian: sKetinggian, junghuhn: sJunghuhn, inversi: sInversi, isoterm: sIsoterm },
});
