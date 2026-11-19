// B01-03 · Radiasi Matahari dan Insolasi · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun } from './lib/common.js';
import { run, SC, u, title, show, scene, fI, sup } from './lib/kit.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix } = M;
const DUR = 250.7;

function earthDisc(ctx, x, y, r, tilt = 0) {
  const g = ctx.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  g.addColorStop(0, '#8fc1e3'); g.addColorStop(1, '#2f6f9e'); circle(ctx, x, y, r); ctx.fillStyle = g; ctx.fill();
  ctx.save(); circle(ctx, x, y, r); ctx.clip(); ctx.fillStyle = 'rgba(120,170,90,0.85)';
  [[-0.3, -0.2, 0.35, 0.22], [0.25, 0.1, 0.3, 0.35], [-0.1, 0.45, 0.25, 0.15]].forEach(([a, b, c, d]) => { ctx.beginPath(); ctx.ellipse(x + a * r, y + b * r, c * r, d * r, 0.4, 0, Math.PI * 2); ctx.fill(); });
  ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.ellipse(x, y - r * 0.92, r * 0.45, r * 0.14, 0, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}
function planck(lam, T) { return Math.pow(lam, -5) / (Math.exp(14388 / (lam * T)) - 1); }

const hook = {
  cards: [
    [2, '21 Juni', 'puncak musim panas belahan utara', (ctx, x, y) => { card(ctx, x + 150, y + 70, 260, 300, { r: 24 }); rrect(ctx, x + 150, y + 70, 260, 80, 24); ctx.fillStyle = C.clay; ctx.fill(); ctx.fillRect(x + 150, y + 120, 260, 30); text(ctx, 'JUNI', x + 280, y + 128, fU(40, 700), C.cream, 'center'); text(ctx, '21', x + 280, y + 320, fU(150, 700), C.ink, 'center'); }],
    [3, 'Kutub utara', 'matahari bersinar 24 jam', (ctx, x, y, t) => { ctx.fillStyle = '#dbe8ef'; ctx.fillRect(x, y, 560, 460); ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.ellipse(x + 280, y + 330, 230, 70, 0, 0, Math.PI * 2); ctx.fill(); ctx.strokeStyle = '#9fc4dd'; ctx.lineWidth = 3; ctx.stroke(); ctx.setLineDash([8, 8]); ctx.strokeStyle = C.amber; ctx.beginPath(); ctx.ellipse(x + 280, y + 170, 200, 50, 0, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash([]); const a = t * 1.2; sun(ctx, x + 280 + Math.cos(a) * 200, y + 170 + Math.sin(a) * 50, 26, t); }, '#dbe8ef'],
    [4, 'Lebih banyak dari ekuator?', 'energi matahari harian', (ctx, x, y, t, t0) => { const p = ap(t, t0 + 0.3, 1.2); [['ekuator', 410, C.amber], ['kutub utara', 525, C.clay]].forEach(([n, v, col], i) => { const h = v / 525 * 300 * p; rrect(ctx, x + 110 + i * 200, y + 400 - h, 140, h, 14); ctx.fillStyle = col; ctx.fill(); text(ctx, n, x + 180 + i * 200, y + 435, fU(26, 700), C.ink, 'center'); }); text(ctx, '?', x + 470, y + 120, fD(140), C.clayD, 'center'); }],
  ],
  punch: [5, 'radiasi matahari'],
};

// ---------------------------------------------------------------- Wien
function sWien(ctx, t) {
  scene(ctx, t, 'wien', C.sand, () => {
    title(ctx, t, 'wien', 'Hukum Wien: makin panas, makin pendek gelombangnya');
    const box = { x: 110, y: 300, w: 1080, h: 600 }; card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 28 });
    const gx = box.x + 80, gy = box.y + box.h - 90, gw = box.w - 130, gh = box.h - 170;
    const X = (lam) => gx + (Math.log10(lam) + 1) / 3 * gw;
    ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy); ctx.lineTo(gx + gw, gy); ctx.stroke();
    [0.1, 0.5, 1, 4, 10, 100].forEach((v) => text(ctx, `${v}`.replace('.', ','), X(v), gy + 34, fU(22, 600), C.gray, 'center'));
    text(ctx, 'panjang gelombang (µm, skala log)', gx + gw, gy + 68, fU(22, 600), C.gray, 'right');
    text(ctx, 'intensitas (dinormalkan)', gx - 10, gy - gh - 18, fU(20, 600), C.gray);
    const curve = (T, col, p) => {
      let mx = 0; for (let i = 0; i <= 300; i++) mx = Math.max(mx, planck(Math.pow(10, -1 + 3 * i / 300), T));
      ctx.save(); ctx.beginPath(); ctx.moveTo(gx, gy);
      for (let i = 0; i <= 300 * p; i++) { const lam = Math.pow(10, -1 + 3 * i / 300); ctx.lineTo(X(lam), gy - planck(lam, T) / mx * gh * 0.9); }
      ctx.lineTo(X(Math.pow(10, -1 + 3 * p)), gy); ctx.closePath(); ctx.fillStyle = col.replace('1)', '0.25)'); ctx.fill(); ctx.strokeStyle = col; ctx.lineWidth = 5; ctx.stroke(); ctx.restore();
    };
    const ps = ap(t, tw('memancarkan', u(10).v0), 1.6, E.linear), pe = ap(t, tw('memancarkan', u(12).v0), 1.6, E.linear);
    if (ps > 0) curve(5800, 'rgba(242,177,58,1)', ps);
    if (pe > 0) curve(288, 'rgba(224,121,79,1)', pe);
    show(ctx, t, u(11).v0, () => { pill(ctx, 'Matahari ±5.800 K', X(0.5), gy - gh + 10, fU(24, 700), C.amber, C.ink, 16, 44, 'center'); text(ctx, 'gelombang PENDEK', X(0.5), gy - gh * 0.42, fU(28, 700), '#a56d06', 'center'); text(ctx, 'shortwave', X(0.5), gy - gh * 0.42 + 40, fI(30), '#a56d06', 'center'); });
    show(ctx, t, u(13).v0, () => { pill(ctx, 'Bumi ±288 K', X(10), gy - gh + 10, fU(24, 700), C.clay, C.cream, 16, 44, 'center'); text(ctx, 'gelombang PANJANG', X(10), gy - gh * 0.42, fU(28, 700), C.clayD, 'center'); text(ctx, 'longwave · inframerah', X(10), gy - gh * 0.42 + 40, fI(30), C.clayD, 'center'); });
    show(ctx, t, u(8).v0, () => {
      card(ctx, 1240, 300, 580, 330, { r: 28, bg: C.forest });
      text(ctx, 'panjang gelombang puncak', 1280, 365, fU(28, 600), C.forest3);
      text(ctx, '= 2.898 ÷ T', 1280, 460, fU(72, 700), C.amber);
      text(ctx, 'hasil dalam µm · T dalam kelvin', 1280, 520, fU(24, 600), C.cream);
      show(ctx, t, u(9).v0, () => pill(ctx, 'makin panas, makin pendek', 1280, 585, fU(26, 700), C.clay, C.cream, 18, 48));
    });
    show(ctx, t, u(10).v0, () => {
      card(ctx, 1240, 670, 580, 230, { r: 28 });
      text(ctx, 'Matahari: 2.898 ÷ 5.800', 1280, 735, fU(28, 700), '#a56d06'); text(ctx, '= ±0,5 µm (cahaya tampak)', 1280, 775, fU(28, 600), C.ink);
      show(ctx, t, u(12).v0, () => { text(ctx, 'Bumi: 2.898 ÷ 288', 1280, 830, fU(28, 700), C.clayD); text(ctx, '= ±10 µm (inframerah)', 1280, 870, fU(28, 600), C.ink); });
    });
  });
}

// ---------------------------------------------------------------- Stefan–Boltzmann
function sStefan(ctx, t) {
  scene(ctx, t, 'stefan', C.sand, () => {
    title(ctx, t, 'stefan', 'Hukum Stefan–Boltzmann: suhu pangkat empat');
    show(ctx, t, u(15).v0, () => {
      card(ctx, 360, 290, 1200, 200, { r: 32, bg: C.forest });
      ctx.font = fU(80, 700); const a = 'E sebanding '; const w = ctx.measureText(a).width;
      text(ctx, a, 520, 425, fU(80, 700), C.cream); sup(ctx, 'T', '4', 520 + w, 425, 80, 700, C.amber);
      text(ctx, 'energi pancaran total · T = suhu mutlak (K)', 960, 470, fU(24, 600), C.forest3, 'center');
    });
    const p16 = ap(t, u(16).v0, 0.5);
    if (p16 > 0) {
      ctx.save(); ctx.globalAlpha *= p16;
      card(ctx, 260, 540, 560, 360, { r: 28 }); card(ctx, 1000, 540, 660, 360, { r: 28 });
      text(ctx, 'suhu T', 540, 600, fU(34, 700), C.ink, 'center'); text(ctx, 'suhu 2T', 1330, 600, fU(34, 700), C.clayD, 'center');
      rrect(ctx, 500, 680, 70, 70, 10); ctx.fillStyle = C.amber; ctx.fill(); text(ctx, '1×', 540, 860, fU(40, 700), C.ink, 'center');
      const n = Math.floor(16 * ap(t, tw('enam', u(16).v0) - 0.5, 1.2, E.linear));
      for (let i = 0; i < 16; i++) { const x = 1190 + (i % 8) * 36, y = 660 + Math.floor(i / 8) * 36; rrect(ctx, x, y, 30, 30, 6); ctx.fillStyle = i < n ? C.clay : '#ece3d3'; ctx.fill(); }
      text(ctx, `${Math.max(1, n)}×`, 1330, 860, fU(40, 700), C.clayD, 'center');
      text(ctx, '2 × 2 × 2 × 2 = 16', 1330, 790, fU(28, 600), C.gray, 'center');
      ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- insolasi + konstanta matahari
function sInsolasi(ctx, t) {
  scene(ctx, t, 'insolasi', '#0f2233', () => {
    title(ctx, t, 'insolasi', 'Insolasi dan konstanta matahari', C.cream);
    sun(ctx, 170, 600, 120, t);
    earthDisc(ctx, 1350, 600, 200);
    ctx.strokeStyle = 'rgba(160,200,230,0.5)'; ctx.lineWidth = 16; circle(ctx, 1350, 600, 218); ctx.stroke();
    const pa = ap(t, u(17).v0, 1.0);
    for (let k = 0; k < 7; k++) { const y = 430 + k * 57; const xe = 1350 - Math.sqrt(Math.max(0, 218 * 218 - (y - 600) ** 2)); arrowLine(ctx, 330, y, lerp(330, xe, pa), y, C.amber, 6, 20); }
    show(ctx, t, u(17).v0 + 1.2, () => { text(ctx, 'insolasi', 600, 330, fD(64), C.amber); text(ctx, 'incoming solar radiation', 600, 380, fI(34), '#f6d18a'); });
    show(ctx, t, u(18).v0, () => {
      ctx.fillStyle = 'rgba(242,177,58,0.85)'; ctx.fillRect(1080, 560, 18, 80); text(ctx, '1 m²', 1060, 545, fU(24, 700), C.amber, 'right');
      card(ctx, 330, 700, 620, 170, { r: 26, bg: C.cream });
      text(ctx, 'di puncak atmosfer, tegak lurus', 370, 755, fU(26, 600), C.gray);
      text(ctx, '±1.361 W/m²', 370, 840, fU(64, 700), C.clayD);
    });
    show(ctx, t, u(19).v0, () => pill(ctx, 'KONSTANTA MATAHARI · solar constant', 640, 930 - 50, fU(26, 700), C.amber, C.ink, 20, 50, 'center'));
    const p20 = ap(t, u(20).v0, 0.6);
    if (p20 > 0) {
      ctx.save(); ctx.globalAlpha *= p20;
      card(ctx, 1100, 300, 720, 230, { r: 26, bg: C.cream });
      text(ctx, 'bumi bulat dan berotasi:', 1140, 360, fU(28, 600), C.gray);
      text(ctx, 'luas penampang ÷ luas bola = 1/4', 1140, 410, fU(30, 700), C.ink);
      show(ctx, t, tw('tiga', u(20).v0), () => text(ctx, '1.361 ÷ 4 = ±340 W/m²', 1140, 490, fU(48, 700), C.clayD));
      ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- empat faktor
function sFaktor(ctx, t) {
  scene(ctx, t, 'faktor', C.sand, () => {
    title(ctx, t, 'faktor', 'Empat faktor besar kecilnya insolasi');
    const cells = [[110, 310], [985, 310], [110, 620], [985, 620]]; const cw = 825, ch = 285;
    const heads = [['1 · Sudut datang sinar', 'angle of incidence', u(22).v0], ['2 · Lama penyinaran', 'day length', u(24).v0], ['3 · Jarak bumi–matahari', 'perihelion · aphelion', u(25).v0], ['4 · Keadaan atmosfer', 'awan, aerosol, uap air', u(28).v0]];
    heads.forEach(([h, en, t0], i) => {
      const k = sp(t, t0 - 0.1, SPRING.snappy); if (k <= 0) return; const [x, y] = cells[i];
      ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); ctx.translate(0, (1 - k) * 40);
      card(ctx, x, y, cw, ch, { r: 26 }); text(ctx, h, x + 30, y + 52, fU(32, 700), C.ink); text(ctx, en, x + 30, y + 92, fI(32), C.clayD);
      const bx = x + 420, by = y + 30;
      if (i === 0) {
        const p = ap(t, u(23).v0, 1.0);
        ctx.fillStyle = '#b9a27a'; ctx.fillRect(bx, by + 200, 370, 24);
        ctx.fillStyle = 'rgba(242,177,58,0.7)'; ctx.fillRect(bx + 40, by + 20, 60, 180 * p); text(ctx, 'tegak: terpusat', bx + 70, by + 250, fU(20, 700), C.ink, 'center');
        if (p > 0) { ctx.fillStyle = 'rgba(242,177,58,0.7)'; poly(ctx, [[bx + 200, by + 20], [bx + 250, by + 20], [bx + 250 + 110 * p, by + 20 + 180 * p], [bx + 200 + 30 * p, by + 20 + 180 * p]]); ctx.fill(); text(ctx, 'miring: menyebar', bx + 290, by + 250, fU(20, 700), C.ink, 'center'); }
      } else if (i === 1) {
        [['0°', 12], ['30° LU', 14], ['66,5° LU', 24]].forEach(([n, hgt], j) => { const p = ap(t, tw('lintang', u(24).v0) + j * 0.3, 0.8); rrect(ctx, bx + 110, by + 40 + j * 70, 240 * hgt / 24 * p, 44, 10); ctx.fillStyle = j === 2 ? C.clay : C.amber; ctx.fill(); text(ctx, n, bx + 95, by + 72 + j * 70, fU(22, 700), C.ink, 'right'); if (p > 0.9) text(ctx, `${hgt} jam`, bx + 120 + 240 * hgt / 24, by + 72 + j * 70, fU(22, 700), C.ink); });
        text(ctx, 'panjang siang, 21 Juni', bx + 110, by + 250, fU(20, 600), C.gray);
      } else if (i === 2) {
        const cx = bx + 180, cy = by + 130; ctx.strokeStyle = C.gray; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(cx, cy, 170, 90, 0, 0, Math.PI * 2); ctx.stroke();
        sun(ctx, cx - 40, cy, 24, t);
        show(ctx, t, tw('Januari', u(26).v0) - 0.3, () => { circle(ctx, cx - 210, cy, 14); ctx.fillStyle = C.blue; ctx.fill(); text(ctx, 'perihelion', cx - 210, cy + 50, fI(28), C.clayD, 'center'); text(ctx, '±3 Jan · dekat', cx - 210, cy + 78, fU(18, 700), C.ink, 'center'); });
        show(ctx, t, tw('Juli', u(26).v0) - 0.3, () => { circle(ctx, cx + 170, cy, 14); ctx.fillStyle = C.blue; ctx.fill(); text(ctx, 'aphelion', cx + 170, cy - 30, fI(28), C.clayD, 'center'); text(ctx, '±4 Jul · jauh', cx + 170, cy + 44, fU(18, 700), C.ink, 'center'); });
        show(ctx, t, u(27).v0, () => pill(ctx, 'pengaruhnya kecil', x + 30, y + 150, fU(24, 700), C.forest, C.cream, 16, 44));
      } else {
        sun(ctx, bx + 60, by + 50, 30, t); cloud(ctx, bx + 210, by + 110, 1.4, '#eef2f5'); cloud(ctx, bx + 320, by + 80, 1.0, '#eef2f5');
        arrowLine(ctx, bx + 90, by + 80, bx + 170, by + 100, C.amber, 6, 18); arrowLine(ctx, bx + 210, by + 150, bx + 230, by + 230, 'rgba(242,177,58,0.4)', 4, 14);
        text(ctx, 'sebagian dipantulkan dan diserap', bx + 200, by + 250, fU(20, 600), C.gray, 'center');
      }
      ctx.restore();
    });
  });
}

// ---------------------------------------------------------------- kutub utara 21 Juni
function sKutub(ctx, t) {
  scene(ctx, t, 'kutub', C.sand, () => {
    title(ctx, t, 'kutub', '21 Juni: insolasi harian menurut lintang');
    card(ctx, 110, 290, 1000, 610, { r: 28 });
    const data = [['0°', 410], ['23,5° LU', 465], ['45° LU', 480], ['66,5° LU', 500], ['90° LU', 525]];
    const p = ap(t, u(30).v0, 2.0, E.outCubic);
    data.forEach(([n, v], i) => { const h = (v - 250) / 300 * 460 * p; const x = 190 + i * 180; rrect(ctx, x, 820 - h, 120, h, 14); ctx.fillStyle = i === 4 ? C.clay : i === 0 ? C.amber : '#e8c27a'; ctx.fill(); text(ctx, n, x + 60, 860, fU(22, 700), C.ink, 'center'); if (p > 0.8) text(ctx, `${v}`, x + 60, 806 - h, fU(26, 700), C.ink, 'center'); });
    text(ctx, 'rata-rata harian di puncak atmosfer (W/m², dibulatkan)', 140, 330, fU(20, 600), C.gray);
    show(ctx, t, u(31).v0, () => { card(ctx, 1160, 300, 660, 230, { r: 26, bg: C.forest }); text(ctx, 'sinar miring, tetapi', 1200, 365, fU(28, 600), C.forest3); text(ctx, 'disinari 24 jam', 1200, 435, fU(52, 700), C.amber); text(ctx, 'total harian melampaui ekuator', 1200, 490, fU(26, 600), C.cream); });
    show(ctx, t, u(32).v0, () => { card(ctx, 1160, 570, 660, 330, { r: 26 }); text(ctx, 'tetapi suhu kutub tetap rendah', 1200, 630, fU(30, 700), C.clayD); text(ctx, '• es memantulkan banyak sinar', 1200, 700, fU(28, 600), C.ink); text(ctx, '  (albedo tinggi)', 1200, 740, fU(28, 600), C.gray); show(ctx, t, tw('sebagian', u(32).v0), () => { text(ctx, '• energi dipakai untuk', 1200, 810, fU(28, 600), C.ink); text(ctx, '  mencairkan es', 1200, 850, fU(28, 600), C.ink); }); });
  });
}

run({
  DUR, no: 3, code: 'B01-03', chip: 'BAB 1 · IKLIM · VIDEO #3 · DASAR', title: 'Radiasi Matahari', sub: 'hukum Wien, Stefan–Boltzmann, dan insolasi · istilah asing OSN',
  next: '#4 · B01-04 · Albedo dan Neraca Energi',
  SCN: [['hook', 0], ['wien', 6], ['stefan', 14], ['insolasi', 17], ['faktor', 21], ['kutub', 29], ['soal', 33], ['jebakan', 38], ['ringkas', 42], ['outro', 45]],
  TERMS: [
    ['Hukum pergeseran Wien', "Wien's displacement law", 'Panjang gelombang puncak = 2.898 ÷ T (µm)', 7],
    ['Radiasi gelombang pendek', 'shortwave radiation', 'Pancaran matahari, puncak ±0,5 µm', 11],
    ['Radiasi gelombang panjang', 'longwave radiation', 'Pancaran bumi berupa inframerah, puncak ±10 µm', 13],
    ['Hukum Stefan–Boltzmann', 'Stefan–Boltzmann law', 'Energi pancaran sebanding suhu mutlak pangkat empat', 14],
    ['Insolasi', 'incoming solar radiation', 'Radiasi matahari yang sampai ke permukaan bumi', 17],
    ['Konstanta matahari', 'solar constant', '±1.361 W/m² di puncak atmosfer; rata-rata bumi ±340', 19],
    ['Sudut datang sinar', 'angle of incidence', 'Sinar tegak terpusat, sinar miring menyebar', 22],
    ['Lama penyinaran', 'day length', 'Panjang siang; bergantung lintang dan musim', 24],
    ['Perihelion · aphelion', 'perihelion · aphelion', 'Terdekat ±3 Januari, terjauh ±4 Juli', () => tw('perihelion', u(26).v0)],
    ['Kemiringan sumbu bumi', 'axial tilt', '23,5°; inilah penyebab musim', () => tw('kemiringan', u(39).v0)],
  ],
  hook,
  soal: {
    q: 'Menurut hukum Wien (panjang gelombang puncak = 2.898 ÷ T, dalam µm), panjang gelombang puncak pancaran bumi yang bersuhu ±288 K adalah …',
    opts: ['0,5 µm, cahaya tampak', '0,1 µm, ultraviolet', '4 µm, batas spektrum', '±10 µm, inframerah', '100 µm, radio'], ans: 3, optFs: 30,
    ansT: () => tw('jawabannya', u(37).v0 - 0.3),
    steps: () => [[u(34).v0, '1) Gunakan hukum Wien', C.forest3, 30], [u(35).v0, '2.898 ÷ T', C.cream, 42], [tw('dibagi', u(35).v0), '= 2.898 ÷ 288', C.cream, 42], [tw('hasilnya', u(35).v0), '= ±10 µm', C.amber, 64],
      [u(36).v0, '2) Kategori', C.forest3, 30], [tw('inframerah', u(36).v0), 'inframerah = gelombang panjang', C.cream, 36]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[u(39).v0, 'Musim terjadi karena jarak bumi–matahari', 'Penyebab musim: kemiringan sumbu 23,5° (axial tilt)', tw('kemiringan', u(39).v0)],
      [u(41).v0, 'Menerima insolasi besar pasti panas', 'Ada pantulan (albedo) dan energi untuk mencairkan es', tw('pantulan', u(41).v0)]],
    extra: (ctx, t) => show(ctx, t, u(40).v0, () => pill(ctx, 'bukti: saat perihelion (Januari), belahan utara justru musim dingin', W / 2, 860, fU(28, 700), C.forest, C.cream, 24, 56, 'center')),
  },
  ringkas: {
    items: () => [[tw('matahari', u(43).v0), 'Matahari: gelombang pendek (±0,5 µm)'], [tw('bumi', u(43).v0), 'Bumi: gelombang panjang, inframerah (±10 µm)'], [tw('insolasi', u(43).v0), 'Insolasi: sudut sinar, lama penyinaran, jarak, atmosfer']],
  },
  scenes: { wien: sWien, stefan: sStefan, insolasi: sInsolasi, faktor: sFaktor, kutub: sKutub },
});
