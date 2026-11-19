// B01-04 · Albedo dan Neraca Energi · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 239.6;

function shirt(ctx, x, y, s, col) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
  poly(ctx, [[-40, -70], [-20, -80], [-10, -70], [10, -70], [20, -80], [40, -70], [70, -40], [50, -20], [40, -30], [40, 70], [-40, 70], [-40, -30], [-50, -20], [-70, -40]]); ctx.fill(); ctx.stroke(); ctx.restore();
}
function thermo(ctx, x, y, h, frac, color) {
  rrect(ctx, x - 16, y - h, 32, h, 16); ctx.fillStyle = C.cream; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  circle(ctx, x, y + 14, 28); ctx.fillStyle = C.cream; ctx.fill(); ctx.stroke(); circle(ctx, x, y + 14, 19); ctx.fillStyle = color; ctx.fill();
  const fh = (h - 24) * clamp(frac); rrect(ctx, x - 8, y - fh - 4, 16, fh + 16, 8); ctx.fillStyle = color; ctx.fill();
}
function waveArrow(ctx, x1, y1, x2, y2, color, amp = 8, n = 4, w = 5) {
  const L = Math.hypot(x2 - x1, y2 - y1), a = Math.atan2(y2 - y1, x2 - x1); if (L < 25) return;
  ctx.save(); ctx.translate(x1, y1); ctx.rotate(a); ctx.strokeStyle = color; ctx.lineWidth = w; ctx.beginPath();
  for (let i = 0; i <= 60; i++) { const f = i / 60; const xx = f * (L - 20), yy = Math.sin(f * n * Math.PI * 2) * amp * (f < 0.9 ? 1 : (1 - f) * 10); i ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); }
  ctx.stroke(); ctx.fillStyle = color; poly(ctx, [[L, 0], [L - 24, -12], [L - 24, 12]]); ctx.fill(); ctx.restore();
}
function tree(ctx, x, y, s) { ctx.fillStyle = '#6b4a2b'; ctx.fillRect(x - 4 * s, y - 30 * s, 8 * s, 30 * s); circle(ctx, x, y - 42 * s, 22 * s); ctx.fillStyle = '#3f8a52'; ctx.fill(); }

const hook = {
  cards: [
    [2, 'Kaus hitam vs putih', 'di bawah terik matahari', (ctx, x, y, t) => { sun(ctx, x + 280, y + 70, 40, t); shirt(ctx, x + 160, y + 300, 1.5, '#222'); shirt(ctx, x + 400, y + 300, 1.5, '#fafafa'); }],
    [3, 'Hitam terasa lebih panas', 'lebih banyak cahaya diserap', (ctx, x, y, t, t0) => { const p = ap(t, t0 + 0.3, 1.5); thermo(ctx, x + 180, y + 380, 300, 0.3 + 0.6 * p, C.clay); thermo(ctx, x + 380, y + 380, 300, 0.3 + 0.25 * p, C.amber); text(ctx, 'hitam', x + 230, y + 120, fU(28, 700), C.ink); text(ctx, 'putih', x + 430, y + 200, fU(28, 700), C.ink); }],
    [5, 'Bumi juga begitu', 'ada yang memantulkan, ada yang menyerap', (ctx, x, y) => { ctx.fillStyle = '#f4f8fb'; ctx.fillRect(x, y, 280, 460); ctx.fillStyle = '#1f5f8b'; ctx.fillRect(x + 280, y, 280, 460); for (let k = 0; k < 3; k++) { arrowLine(ctx, x + 60 + k * 60, y + 40, x + 100 + k * 60, y + 260, C.amber, 6, 18); arrowLine(ctx, x + 110 + k * 60, y + 270, x + 150 + k * 60, y + 60, 'rgba(242,177,58,0.8)', 5, 16); arrowLine(ctx, x + 340 + k * 60, y + 40, x + 380 + k * 60, y + 260, C.amber, 6, 18); } text(ctx, 'salju', x + 140, y + 400, fU(30, 700), C.ink, 'center'); text(ctx, 'laut', x + 420, y + 400, fU(30, 700), '#fff', 'center'); }],
  ],
  punch: [6, 'albedo'],
};

const ALB = [['Salju segar', 80, 90, 8], ['Awan tebal', 60, 90, 9], ['Pasir gurun', 30, 40, 10], ['Sawah, rumput', 15, 25, 11], ['Hutan hujan tropis', 10, 15, 12], ['Aspal, laut (sinar tegak)', 5, 10, 13]];
function sAlbedo(ctx, t) {
  scene(ctx, t, 'albedo', C.sand, () => {
    title(ctx, t, 'albedo', 'Albedo: berapa persen yang dipantulkan?');
    show(ctx, t, u(7).v0, () => { card(ctx, 1300, 320, 520, 230, { r: 26, bg: C.forest }); text(ctx, 'albedo =', 1340, 385, fU(32, 700), C.forest3); text(ctx, 'radiasi dipantulkan', 1340, 440, fU(34, 700), C.cream); rrect(ctx, 1340, 458, 360, 4, 2); ctx.fillStyle = C.amber; ctx.fill(); text(ctx, 'radiasi diterima', 1340, 510, fU(34, 700), C.cream); });
    ALB.forEach(([n, a, b, ui], i) => {
      const p = ap(t, U_(ui).v0, 0.8, E.outCubic); if (p <= 0) return;
      const y = 300 + i * 95, S = 7.2;
      text(ctx, n, 110, y + 46, fU(30, 700), C.ink);
      rrect(ctx, 520, y + 10, 720, 52, 14); ctx.fillStyle = '#ece3d3'; ctx.fill();
      const col = i < 3 ? '#9fc4dd' : '#3b6e4d';
      rrect(ctx, 520, y + 10, S * b * p, 52, 14); ctx.fillStyle = mix(col, '#ffffff', 0.45); ctx.fill();
      rrect(ctx, 520, y + 10, S * a * p, 52, 14); ctx.fillStyle = col; ctx.fill();
      if (p > 0.7) text(ctx, `${a}–${b}%`, 534 + S * b, y + 48, fU(28, 700), C.ink);
    });
    show(ctx, t, u(14).v0, () => {
      const x = 520 + 7.2 * 30; ctx.setLineDash([10, 8]); ctx.strokeStyle = C.clay; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x, 290); ctx.lineTo(x, 880); ctx.stroke(); ctx.setLineDash([]);
      pill(ctx, 'rata-rata bumi ±30%', x, 900, fU(26, 700), C.clay, C.cream, 18, 48, 'center');
      show(ctx, t, tw('awan', u(14).v0), () => pill(ctx, 'penyumbang terbesar: AWAN', 1560, 640, fU(28, 700), C.blue, C.cream, 20, 54, 'center'));
    });
  });
}

function sNeraca(ctx, t) {
  scene(ctx, t, 'neraca', '#eef3f6', () => {
    title(ctx, t, 'neraca', 'Neraca energi bumi (dari 100 satuan)');
    show(ctx, t, u(15).v0 + 1.5, () => text(ctx, 'energy budget', 112, 222, fI(34), C.clayD));
    ctx.fillStyle = '#1b2a3a'; ctx.fillRect(110, 300, 1700, 110); text(ctx, 'ANGKASA', 130, 335, fU(24, 700), '#c9d6e3');
    ctx.fillStyle = 'rgba(160,190,215,0.35)'; ctx.fillRect(110, 410, 1700, 230); text(ctx, 'ATMOSFER', 130, 445, fU(24, 700), C.blue);
    ctx.fillStyle = '#b9a27a'; ctx.fillRect(110, 640, 1700, 240); text(ctx, 'PERMUKAAN BUMI', 130, 680, fU(24, 700), '#5a4326');
    const n = (v, x, y, col) => { circle(ctx, x, y, 44); ctx.fillStyle = col; ctx.fill(); text(ctx, `${v}`, x, y + 16, fU(42, 700), '#fff', 'center'); };
    const pIn = ap(t, u(16).v0, 0.8);
    if (pIn > 0) { arrowLine(ctx, 400, 310, 400, lerp(310, 620, pIn), C.amber, 14, 36); n(100, 400, 355, C.amber); }
    show(ctx, t, tw('tiga', u(16).v0), (p) => { arrowLine(ctx, 430, 520, lerp(430, 600, p), lerp(520, 330, p), '#9fc4dd', 10, 30); n(30, 650, 355, '#6c9ec0'); text(ctx, 'dipantulkan ke angkasa', 710, 366, fU(28, 700), '#c9d6e3'); });
    show(ctx, t, u(17).v0, () => { n(20, 780, 530, '#5a8db1'); text(ctx, 'diserap atmosfer dan awan', 840, 542, fU(28, 700), C.blue); cloud(ctx, 700, 470, 0.6); });
    show(ctx, t, u(18).v0, () => { n(50, 400, 760, C.clay); text(ctx, 'diserap permukaan', 460, 772, fU(30, 700), '#fff'); });
    const flows = [['radiasi inframerah', '', u(20).v0, C.clay], ['panas sensibel', 'sensible heat', tw('sensibel', u(21).v0), C.clayD], ['panas laten', 'latent heat', tw('laten', u(22).v0), C.blue]];
    flows.forEach(([s, en, t0, col], i) => {
      const p = ap(t, t0, 0.7); if (p <= 0) return; const x = 1080 + i * 260;
      ctx.save(); ctx.globalAlpha *= p;
      if (i === 0) waveArrow(ctx, x, 730, x, lerp(730, 450, p), col, 8, 4, 5); else arrowLine(ctx, x, 730, x, lerp(730, 450, p), col, 8, 26);
      if (i === 2) { for (let k = 0; k < 4; k++) { const ph = (t * 0.6 + k / 4) % 1; circle(ctx, x - 30 + k * 20, 720 - ph * 220, 6); ctx.fillStyle = `rgba(43,108,176,${1 - ph})`; ctx.fill(); } show(ctx, t, tw('dilepaskan', u(22).v0), () => { cloud(ctx, x, 460, 0.9); text(ctx, 'panas dilepas saat mengembun', x, 600, fU(18, 700), C.blue, 'center'); }); }
      text(ctx, s, x, 822, fU(24, 700), '#fff', 'center'); if (en) text(ctx, en, x, 856, fI(26), '#fff3d6', 'center');
      ctx.restore();
    });
    show(ctx, t, u(23).v0, () => { card(ctx, 1240, 310, 560, 90, { r: 22, bg: C.cream }); text(ctx, 'energi MASUK = energi KELUAR', 1520, 368, fU(30, 700), C.forest, 'center'); });
    show(ctx, t, u(24).v0, () => pill(ctx, 'keseimbangan radiasi · radiative equilibrium', 1520, 445, fU(24, 700), C.forest, C.cream, 18, 46, 'center'));
  });
}

function sUhi(ctx, t) {
  scene(ctx, t, 'uhi', C.sand, () => {
    title(ctx, t, 'uhi', 'Pulau bahang kota (urban heat island)');
    const x0 = 110, x1 = 1110, base = 860;
    card(ctx, x0 - 10, 290, x1 - x0 + 20, 600, { r: 28 });
    // skyline
    ctx.fillStyle = '#c9d9a5'; ctx.fillRect(x0, base - 20, x1 - x0, 30);
    for (let i = 0; i < 6; i++) { tree(ctx, x0 + 30 + i * 30, base - 20, 1); tree(ctx, x1 - 30 - i * 30, base - 20, 1); }
    const bl = [[330, 90], [380, 140], [430, 110], [500, 230], [560, 300], [620, 260], [680, 320], [740, 220], [800, 150], [860, 100], [910, 80]];
    bl.forEach(([x, h], i) => { ctx.fillStyle = i % 2 ? '#7d8791' : '#9aa4ad'; ctx.fillRect(x, base - 20 - h, 46, h); ctx.fillStyle = '#f3e5a8'; for (let k = 0; k < h / 30 - 1; k++) { ctx.fillRect(x + 8, base - 20 - h + 14 + k * 30, 10, 10); ctx.fillRect(x + 28, base - 20 - h + 14 + k * 30, 10, 10); } });
    text(ctx, 'desa', x0 + 100, base + 2, fU(20, 700), C.forest, 'center'); text(ctx, 'pusat kota', 640, base + 2, fU(20, 700), '#fff', 'center'); text(ctx, 'desa', x1 - 100, base + 2, fU(20, 700), C.forest, 'center');
    // temperature dome
    const p = ap(t, u(26).v0, 2.0, E.inOutCubic);
    if (p > 0) {
      ctx.strokeStyle = C.clay; ctx.lineWidth = 7; ctx.beginPath();
      for (let i = 0; i <= 100 * p; i++) { const f = i / 100, x = lerp(x0 + 20, x1 - 20, f); const y = 520 - 160 * Math.exp(-(((f - 0.53) / 0.2) ** 2)); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      ctx.stroke(); text(ctx, 'suhu udara', x0 + 30, 490, fU(22, 700), C.clay);
      show(ctx, t, tw('dua', u(26).v0), () => pill(ctx, '+2 sampai 4 °C', 640, 330, fU(30, 700), C.clay, C.cream, 20, 56, 'center'));
      show(ctx, t, tw('malam', u(26).v0), () => { circle(ctx, 1030, 350, 26); ctx.fillStyle = '#f3e5a8'; ctx.fill(); circle(ctx, 1042, 340, 22); ctx.fillStyle = C.cream; ctx.fill(); text(ctx, 'terutama malam', 1000, 400, fU(20, 700), C.gray, 'right'); });
    }
    const causes = [['Beton dan aspal menyimpan panas', 'dilepas pada malam hari', 29, '#7d8791'], ['Vegetasi sedikit', 'pendinginan lewat penguapan rendah', 30, '#3f8a52'], ['Panas buangan', 'kendaraan, industri, AC', 31, C.clay], ['Gedung tinggi rapat', 'memerangkap radiasi, menghambat angin', 32, C.blue]];
    causes.forEach(([a, b, ui, col], i) => {
      const k = sp(t, U_(ui).v0 - 0.1, SPRING.snappy); if (k <= 0) return; const y = 300 + i * 148;
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); ctx.translate((1 - k) * 60, 0);
      card(ctx, 1170, y, 650, 128, { r: 22 }); rrect(ctx, 1170, y, 14, 128, 7); ctx.fillStyle = col; ctx.fill();
      text(ctx, `${i + 1}`, 1225, y + 80, fU(48, 700), col, 'center'); text(ctx, a, 1275, y + 56, fU(29, 700), C.ink); text(ctx, b, 1275, y + 96, fU(23, 500), C.gray);
      ctx.restore();
    });
  });
}

function sMitigasi(ctx, t) {
  scene(ctx, t, 'mitigasi', C.sand, () => {
    title(ctx, t, 'mitigasi', 'Cara mendinginkan kota');
    const items = [['Ruang terbuka hijau', 'minimal 30% luas kota', '', 'ruang'], ['Atap hijau', 'tanaman di atap', 'green roof', 'atap'], ['Atap terang', 'memantulkan panas', 'cool roof', 'terang'], ['Perkerasan berpori', 'air meresap, permukaan lebih sejuk', 'permeable pavement', 'perkerasan']];
    items.forEach(([a, b, en, w], i) => {
      const k = sp(t, tw(w, u(33).v0) - 0.15, SPRING.bouncy); if (k <= 0) return;
      const x = 110 + i * 430, y = 320; ctx.save(); ctx.translate(x + 195, y + 280); ctx.scale(k, k); ctx.translate(-(x + 195), -(y + 280));
      card(ctx, x, y, 390, 560, { r: 28 });
      const cx = x + 195, cy = y + 190;
      if (i === 0) { for (let j = 0; j < 5; j++) tree(ctx, cx - 120 + j * 60, cy + 70, 1.8); text(ctx, '30%', cx, cy - 70, fU(64, 700), C.forest, 'center'); }
      if (i === 1 || i === 2) { ctx.fillStyle = '#b37a52'; ctx.fillRect(cx - 110, cy - 10, 220, 120); ctx.fillStyle = i === 1 ? '#3f8a52' : '#f4f6f7'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; poly(ctx, [[cx - 130, cy - 10], [cx, cy - 90], [cx + 130, cy - 10]]); ctx.fill(); ctx.stroke();
        if (i === 2) { arrowLine(ctx, cx - 80, cy - 190, cx - 40, cy - 80, C.amber, 6, 18); arrowLine(ctx, cx - 20, cy - 80, cx + 20, cy - 190, 'rgba(242,177,58,0.8)', 6, 18); } else for (let j = 0; j < 5; j++) { circle(ctx, cx - 80 + j * 40, cy - 30 - (j === 2 ? 40 : j % 2 * 20), 16); ctx.fillStyle = '#2f7d4a'; ctx.fill(); } }
      if (i === 3) { for (let r = 0; r < 3; r++) for (let c = 0; c < 5; c++) { rrect(ctx, cx - 140 + c * 58, cy - 30 + r * 40, 50, 32, 6); ctx.fillStyle = '#9aa4ad'; ctx.fill(); } for (let j = 0; j < 3; j++) { const ph = (t * 0.8 + j / 3) % 1; arrowLine(ctx, cx - 60 + j * 60, cy - 100 + ph * 160, cx - 60 + j * 60, cy - 70 + ph * 160, C.blue, 5, 14); } }
      text(ctx, a, cx, y + 400, fU(32, 700), C.ink, 'center'); wrap(ctx, b, fU(24, 500), 340).forEach((l, j) => text(ctx, l, cx, y + 442 + j * 30, fU(24, 500), C.gray, 'center'));
      if (en) text(ctx, en, cx, y + 520, fI(34), C.clayD, 'center');
      ctx.restore();
    });
  });
}

run({
  DUR, no: 4, code: 'B01-04', chip: 'BAB 1 · IKLIM · VIDEO #4 · DASAR–MENENGAH', title: 'Albedo dan Neraca Energi', sub: 'pantulan, aliran energi bumi, dan pulau bahang kota',
  next: '#5 · B01-05 · Suhu Udara',
  SCN: [['hook', 0], ['albedo', 7], ['neraca', 15], ['uhi', 25], ['mitigasi', 33], ['soal', 34], ['jebakan', 40], ['ringkas', 43], ['outro', 46]],
  TERMS: [
    ['Albedo', 'albedo', 'Persentase radiasi yang dipantulkan; rata-rata bumi ±30%', 7],
    ['Neraca energi', 'energy budget', '100 masuk: 30 dipantulkan, 20 atmosfer, 50 permukaan', 15],
    ['Panas sensibel', 'sensible heat', 'Panas dibawa udara hangat lewat konduksi dan konveksi', 21],
    ['Panas laten', 'latent heat', 'Energi terbawa saat air menguap, dilepas saat mengembun', 22],
    ['Keseimbangan radiasi', 'radiative equilibrium', 'Jangka panjang: energi masuk = energi keluar', 24],
    ['Pulau bahang kota', 'urban heat island', 'Pusat kota 2–4 °C lebih hangat, terutama malam', 27],
    ['Atap hijau · atap terang', 'green roof · cool roof', 'Menyerap lebih sedikit panas di atap bangunan', () => tw('atap', u(33).v0)],
    ['Perkerasan berpori', 'permeable pavement', 'Air meresap, permukaan lebih sejuk', () => tw('perkerasan', u(33).v0)],
  ],
  hook,
  soal: {
    q: 'Sebuah lahan menerima radiasi 800 W/m². Lahan berubah dari hutan (albedo 12%) menjadi permukiman beratap seng terang (albedo 30%). Perubahan energi yang diserap adalah …',
    opts: ['berkurang 144 W/m²', 'bertambah 144 W/m²', 'berkurang 240 W/m²', 'berkurang 18 W/m²', 'tidak berubah'], ans: 0, optFs: 30,
    ansT: () => tw('jawabannya', u(39).v0 - 0.3),
    steps: () => [[u(35).v0, 'diserap = radiasi × (1 − albedo)', C.amber, 34], [u(36).v0, 'Hutan', C.forest3, 28], [tw('nol', u(36).v0), '800 × 0,88 = 704 W/m²', C.cream, 38],
      [u(37).v0, 'Permukiman', C.forest3, 28], [tw('nol', u(37).v0), '800 × 0,70 = 560 W/m²', C.cream, 38], [u(38).v0, '704 − 560', C.cream, 38], [tw('seratus', u(38).v0), '= berkurang 144 W/m²', C.amber, 50]],
  },
  jebakan: {
    title: 'Hati-hati, ini jebakannya',
    items: () => [[u(41).v0, 'Energi diserap berkurang, maka pasti lebih sejuk', 'Tetap bisa lebih panas: penguapan hilang + panas buangan', tw('tetap', u(41).v0)]],
    extra: (ctx, t) => show(ctx, t, u(42).v0, () => { card(ctx, 110, 560, 1700, 220, { r: 26, bg: C.forest }); text(ctx, 'Soal olimpiade menguji kemampuan', 960, 650, fU(40, 700), C.cream, 'center'); text(ctx, 'melihat LEBIH DARI SATU FAKTOR', 960, 720, fU(48, 700), C.amber, 'center'); }),
  },
  ringkas: {
    items: () => [[tw('albedo', u(44).v0), 'Albedo menentukan energi yang dipantulkan'], [tw('neraca', u(44).v0), 'Neraca energi: masuk = keluar'], [tw('kota', u(44).v0), 'Kota jadi pulau bahang: beton, minim vegetasi, panas buangan']],
  },
  scenes: { albedo: sAlbedo, neraca: sNeraca, uhi: sUhi, mitigasi: sMitigasi },
});
