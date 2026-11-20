// B01-10 · ITCZ dan Monsun · OSNGEO.id — pure function of time (seconds).
import * as M from './lib/motion.js';
import { C, fD, fU, tw, U_, sp, ap, poly, circle, card, arrowLine, wrap, pill, cloud, sun, rain } from './lib/common.js';
import { run, SC, u, title, show, scene, fI } from './lib/kit.js';
import * as G from './lib/geo.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, rrect, hash01, mix, fill } = M;
const DUR = 256.0;
const D2R = Math.PI / 180;
let W110 = null, REG = null, IND = null, SD = null;

const RAIN = {
  jawa: [300, 300, 210, 150, 130, 90, 60, 50, 60, 110, 140, 200],
  kupang: [390, 350, 230, 60, 20, 5, 5, 2, 5, 25, 90, 240],
  ambon: [130, 130, 140, 280, 520, 630, 600, 410, 250, 150, 110, 140],
  pontianak: [270, 210, 240, 280, 280, 210, 170, 200, 230, 350, 390, 320],
};
function rainChart(ctx, x, y, w, h, data, col, p, label) {
  card(ctx, x, y, w, h, { r: 18 });
  text(ctx, label, x + 16, y + 30, fU(20, 800), C.ink);
  const bw = (w - 32) / 12, mx = 650;
  data.forEach((v, i) => { const bh = (h - 70) * v / mx * clamp(p * 1.6 - i * 0.05); rrect(ctx, x + 16 + i * bw + 2, y + h - 22 - bh, bw - 4, bh, 3); ctx.fillStyle = col; ctx.fill(); });
  'JFMAMJJASOND'.split('').forEach((m, i) => text(ctx, m, x + 16 + (i + 0.5) * bw, y + h - 6, fU(13, 700), C.gray, 'center'));
}
const F_JAN = G.field([[100, 50, 24, 25, 14], [132, -20, -10, 14, 9], [185, 50, -10, 20, 10], [80, -32, 6, 20, 8]], 1010);
const F_JUL = G.field([[80, 30, -14, 25, 14], [135, -28, 11, 18, 9], [165, 32, 8, 20, 10], [100, -32, 6, 20, 8]], 1010);
const F_CALM = G.field([[118, 0, -1.2, 30, 20]], 1010);
const rotC = (la) => (la > 0 ? -0.9 : 0.9) * Math.min(1, Math.abs(la) / 8);

// ---------------------------------------------------------------- hook: three cities with rain charts
function sHook(ctx, t) {
  scene(ctx, t, 'hook', C.sand, () => {
    const box = { x: 0, y: 0, w: W, h: H }; const z = ap(t, 3, 18, E.inOutCubic) * 0.05;
    const pr = G.mapProj(box, [93 + z * 40, 142 - z * 40, -19.5 + z * 18, 8 - z * 18]);
    G.drawMap(ctx, IND, pr, { t, depth: 9 });
    const cities = [['Jawa (Jakarta)', 106.8, -6.2, RAIN.jawa, C.blue, 0, [120, 560]], ['Kupang, NTT', 123.6, -10.2, RAIN.kupang, C.clay, 1, [760, 640]], ['Ambon', 128.2, -3.7, RAIN.ambon, C.forest, 2, [1360, 200]]];
    cities.forEach(([n, lo, la, d, col, ui, [cx, cy]]) => {
      const k = sp(t, U_(ui).v0, SPRING.bouncy); if (k <= 0) return; const p = pr(lo, la);
      ctx.save(); ctx.globalAlpha *= clamp(k); circle(ctx, p[0], p[1], 14 * k); ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = C.cream; ctx.lineWidth = 4; ctx.stroke();
      ctx.strokeStyle = col; ctx.lineWidth = 3; ctx.setLineDash([6, 6]); ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(cx + 210, cy + 120); ctx.stroke(); ctx.setLineDash([]);
      rainChart(ctx, cx, cy, 420, 240, d, col, ap(t, U_(ui).v0 + 0.2, 1.4), `${n} · curah hujan bulanan`);
      ctx.restore();
    });
    show(ctx, t, U_(4).v0, () => { pill(ctx, 'ITCZ yang bergeser', W / 2 - 220, 140, fU(34, 800), C.forest, C.cream, 24, 64, 'center'); pill(ctx, 'angin MONSUN', W / 2 + 220, 140, fU(34, 800), C.clay, C.cream, 24, 64, 'center'); });
  });
}

// ---------------------------------------------------------------- ITCZ globe
function itczLat(lo, m) { const land = Math.exp(-(((lo - 110) / 40) ** 2)) * 0.9 + Math.exp(-(((lo - 20) / 20) ** 2)) * 0.6; return m * (7 + 10 * land) + 1.5 * Math.sin(lo * 0.08); }
function sItcz(ctx, t) {
  scene(ctx, t, 'itcz', '#0f2233', () => {
    for (let i = 0; i < 80; i++) { circle(ctx, hash01(i, 1) * W, hash01(i, 2) * H, 1 + hash01(i, 3) * 1.4); ctx.fillStyle = 'rgba(255,255,255,0.5)'; ctx.fill(); }
    const lon0 = 108 + 6 * Math.sin((t - SC.itcz[0]) * 0.1);
    const g = G.globeProj(lon0, 5, 380, 640, 600); G.drawGlobe(ctx, W110, g);
    // month parameter: -1 = Januari, +1 = Juli
    let m = 0; const tj = U_(9).v0, ta = U_(10).v0;
    if (t < tj) m = ap(t, U_(7).v0, 1) * Math.sin((t - U_(7).v0) * 1.1);
    else if (t < ta) m = lerp(m, 1, ap(t, tj, 1.5, E.inOutCubic));
    else m = lerp(1, -1, ap(t, ta, 1.8, E.inOutCubic));
    if (t > U_(11).v0) m = -1 + 0.0 * Math.sin(t);
    ctx.save(); circle(ctx, g.cx, g.cy, g.R); ctx.clip();
    // converging trades
    const pc = ap(t, U_(6).v0, 0.8);
    if (pc > 0) for (let i = 0; i < 10; i++) { const lo = lon0 - 70 + i * 15, ph = (t * 0.5 + i * 0.13) % 1; const c = itczLat(lo, m); [[1, -1], [-1, 1]].forEach(([s, d]) => { const a = g(lo + 8 * ph, c + s * (22 - 16 * ph)), b = g(lo + 8 * ph - 3, c + s * (19 - 16 * ph)); if (a && b) { ctx.globalAlpha = pc * Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], C.amber, 5, 16); ctx.globalAlpha = 1; } }); }
    // cloud band
    const pb = ap(t, U_(5).v0 + 0.3, 0.8);
    for (let lo = lon0 - 85; lo <= lon0 + 85; lo += 9) { const p = g(lo, itczLat(lo, m)); if (p && pb > 0) cloud(ctx, p[0], p[1], pb * (0.45 + 0.15 * Math.cos((lo - lon0) * D2R)), '#ffffff'); }
    // equator
    ctx.strokeStyle = 'rgba(242,177,58,0.8)'; ctx.lineWidth = 3; ctx.setLineDash([10, 8]); ctx.beginPath(); let s0 = false; for (let lo = lon0 - 89; lo <= lon0 + 89; lo += 3) { const p = g(lo, 0); if (!p) continue; s0 ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); s0 = true; } ctx.stroke(); ctx.setLineDash([]);
    ctx.restore();
    // sun marker on the side
    const sy = 600 - m * 23.5 / 90 * 380 * 1.2; sun(ctx, 1080, sy, 34, t);
    ctx.strokeStyle = 'rgba(242,177,58,0.6)'; ctx.setLineDash([6, 8]); ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(1040, sy); ctx.lineTo(980, sy); ctx.stroke(); ctx.setLineDash([]);
    // month switch
    const k = ap(t, U_(8).v0, 0.6); ctx.save(); ctx.globalAlpha *= k;
    rrect(ctx, 1220, 300, 600, 96, 48); ctx.fillStyle = 'rgba(255,255,255,0.1)'; ctx.fill();
    const mk = (m + 1) / 2; rrect(ctx, 1226 + 294 * mk, 306, 294, 84, 42); ctx.fillStyle = m < 0 ? C.clay : C.blue; ctx.fill();
    text(ctx, 'JANUARI', 1373, 362, fU(32, 800), C.cream, 'center'); text(ctx, 'JULI', 1667, 362, fU(32, 800), C.cream, 'center'); ctx.restore();
    const rows = [[U_(6).v0, 'pasat utara dan selatan bertemu', C.amber], [U_(8).v0, 'bergeser mengikuti matahari', '#cfe0ff'], [U_(9).v0, 'Juli: ITCZ ke utara (±5°–10°)', C.blue], [U_(10).v0, 'Januari: ITCZ ke selatan', C.clay], [U_(11).v0, 'paling jauh di atas Asia dan Australia', C.forest3], [U_(12).v0, 'Indonesia selatan ekuator: hujan Des–Feb', '#9fe0b0']];
    rows.forEach(([tt, s, col], i) => show(ctx, t, tt, () => { const y = 430 + i * 86; rrect(ctx, 1220, y, 600, 70, 18); ctx.fillStyle = 'rgba(255,255,255,0.08)'; ctx.fill(); rrect(ctx, 1220, y, 8, 70, 4); ctx.fillStyle = col; ctx.fill(); text(ctx, s, 1246, y + 45, fU(25, 700), C.cream); }));
    show(ctx, t, U_(5).v0 + 0.8, () => text(ctx, 'Intertropical Convergence Zone', 112, 222, fI(34), C.amber));
    title(ctx, t, 'itcz', 'ITCZ: sabuk awan yang bergeser', C.cream);
  });
}

// ---------------------------------------------------------------- monsoon map
const BOX = { x: 110, y: 235, w: 1150, h: 690 }, EXT = [70, 160, -30, 24];
function sMonsun(ctx, t) {
  scene(ctx, t, 'monsun', C.sand, () => {
    const pr = G.mapProj(BOX, EXT);
    const kSwap = ap(t, U_(23).v0, 2.0, E.inOutCubic), kCalm = ap(t, U_(27).v0, 1.5, E.inOutCubic);
    let F = G.blend(F_JAN, F_JUL, kSwap); if (kCalm > 0) F = G.blend(F, F_CALM, kCalm);
    const dry = kSwap;
    card(ctx, BOX.x - 8, BOX.y - 8, BOX.w + 16, BOX.h + 16, { r: 30 });
    G.drawMap(ctx, REG, pr, { t, land: mix('#e3efcf', '#f0dcae', dry) });
    ctx.save(); rrect(ctx, BOX.x, BOX.y, BOX.w, BOX.h, 26); ctx.clip();
    G.graticule(ctx, pr, EXT, 10);
    const e1 = pr(EXT[0], 0), e2 = pr(EXT[1], 0); ctx.strokeStyle = C.amber; ctx.lineWidth = 3; ctx.setLineDash([12, 8]); ctx.beginPath(); ctx.moveTo(e1[0], e1[1]); ctx.lineTo(e2[0], e2[1]); ctx.stroke(); ctx.setLineDash([]);
    text(ctx, 'ekuator', e1[0] + 14, e1[1] - 10, fU(20, 800), '#a56d06');
    const cs = G.contours(F.P, [60, 175, -40, 55], 2.5, [998, 1002, 1006, 1010, 1014, 1018, 1022, 1026, 1030]);
    G.drawIsobars(ctx, cs, pr, { labels: false, width: 2.4, color: 'rgba(29,65,56,0.35)' });
    const pf = ap(t, U_(16).v0, 1.0) * (1 - 0.6 * kCalm);
    if (pf > 0) G.drawFlow(ctx, F, pr, SD, t, { speed: 1.7, vmax: 6, color: 'rgba(22,58,80,0.85)', width: 3, alpha: pf, rot: rotC, life: 3.2 });
    // centers (clamped into box)
    const cen = [[kSwap < 0.5 ? 'H' : 'L', 100, 21, kSwap < 0.5 ? C.blue : C.clay, kSwap < 0.5 ? U_(18).v0 : U_(24).v0, kSwap < 0.5 ? 'dari Asia (Siberia)' : 'Asia panas'], [kSwap < 0.5 ? 'L' : 'H', 133, -22, kSwap < 0.5 ? C.clay : C.blue, kSwap < 0.5 ? U_(17).v0 : U_(24).v0, kSwap < 0.5 ? 'Australia panas' : 'Australia dingin']];
    cen.forEach(([k, lo, la, col, tt, lab]) => { const s = sp(t, tt, SPRING.bouncy) * (1 - kCalm); if (s <= 0.02) return; const p = pr(lo, la); circle(ctx, p[0], p[1], 40 * s); ctx.fillStyle = col; ctx.fill(); ctx.strokeStyle = C.cream; ctx.lineWidth = 4; ctx.stroke(); text(ctx, k, p[0], p[1] + 15 * s, fU(44 * s, 800), C.cream, 'center'); pill(ctx, lab, p[0], p[1] + 66, fU(20, 800), col, C.cream, 12, 36, 'center'); });
    // equator crossing highlight
    show(ctx, t, U_(20).v0, () => { if (kSwap > 0.5) return; const p = pr(106, 0); for (let k = 0; k < 2; k++) { const ph = (t * 0.8 + k / 2) % 1; circle(ctx, p[0], p[1], 30 + ph * 70); ctx.strokeStyle = `rgba(152,63,41,${1 - ph})`; ctx.lineWidth = 4; ctx.stroke(); } const a = pr(112, 10), b = pr(106, 1), c = pr(104, -6); ctx.strokeStyle = C.clayD; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.quadraticCurveTo(b[0], b[1], c[0] + 10, c[1]); ctx.stroke(); arrowLine(ctx, b[0] - 6, (b[1] + c[1]) / 2, c[0] + 30, c[1] + 6, C.clayD, 9, 28); pill(ctx, 'timur laut, lalu berbelok jadi barat laut', p[0] + 20, p[1] - 120, fU(22, 800), C.clayD, C.cream, 14, 42); });
    // rain over Java (west monsoon)
    show(ctx, t, U_(21).v0, () => { if (kSwap > 0.5) return; [[106.8, -6.5], [110.5, -7], [113, -7.5], [120, -8.6], [102, -3]].forEach(([lo, la], i) => { const p = pr(lo, la); cloud(ctx, p[0], p[1] - 40, 0.7, '#e9eef3'); rain(ctx, p[0], p[1] - 10, 60, t + i, 5); }); });
    // narrow seas + dry NTT (east monsoon)
    show(ctx, t, tw('Timor', U_(25).v0) - 0.3, () => { if (kSwap < 0.5) return; [['Laut Timor', 126, -11.5], ['Laut Arafura', 135, -9.5]].forEach(([n, lo, la]) => { const p = pr(lo, la); pill(ctx, n, p[0], p[1], fU(20, 800), C.blue, C.cream, 12, 36, 'center'); }); });
    show(ctx, t, U_(26).v0 + 1, () => { if (kSwap < 0.5) return; const p = pr(123.6, -10.2); circle(ctx, p[0], p[1], 46); ctx.fillStyle = '#d9a35a'; ctx.fill(); ctx.strokeStyle = '#7a5a2c'; ctx.lineWidth = 3; [[-20, -10, 10, 14], [0, -20, -6, 20], [5, 5, 25, -5]].forEach(([a, b, c, d]) => { ctx.beginPath(); ctx.moveTo(p[0] + a, p[1] + b); ctx.lineTo(p[0] + c, p[1] + d); ctx.stroke(); }); pill(ctx, 'NTT: paling kering', p[0], p[1] + 70, fU(22, 800), C.clayD, C.cream, 14, 40, 'center'); });
    // pancaroba: lightning + whirlwind
    if (kCalm > 0) { const p = pr(110, -7); ctx.save(); ctx.globalAlpha *= kCalm; cloud(ctx, p[0], p[1] - 110, 1.4, '#6b7480'); if (Math.sin(t * 7) > 0.85) { ctx.strokeStyle = '#ffe680'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(p[0], p[1] - 90); ctx.lineTo(p[0] - 14, p[1] - 50); ctx.lineTo(p[0] + 6, p[1] - 50); ctx.lineTo(p[0] - 10, p[1] - 10); ctx.stroke(); } for (let k = 0; k < 8; k++) { const y = p[1] - 80 + k * 12, r = 6 + k * 3; ctx.strokeStyle = 'rgba(80,80,90,0.7)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(p[0] + 60 + Math.sin(t * 3 + k) * 4, y + 70, r, r * 0.35, 0, t * 4 + k, t * 4 + k + 4.5); ctx.stroke(); } ctx.restore(); }
    ctx.restore();
    // right panel
    const ph = kCalm > 0.5 ? 2 : kSwap > 0.5 ? 1 : 0;
    const P = [['MONSUN BARAT', 'west monsoon', 'Desember–Februari', ['Asia tekanan tinggi', 'Australia tekanan rendah', 'angin melintasi laut luas', 'membawa HUJAN'], C.blue],
      ['MONSUN TIMUR', 'east monsoon', 'Juni–Agustus', ['Australia tekanan tinggi', 'Asia tekanan rendah', 'melintasi laut sempit', 'membawa KEMARAU'], C.clay],
      ['PANCAROBA', 'masa peralihan', 'April–Mei · Oktober–November', ['angin lemah, berubah-ubah', 'hujan lebat singkat', 'petir', 'puting beliung'], C.forestL]][ph];
    const t0 = [U_(16).v0, U_(22).v0, U_(27).v0][ph];
    const kk = sp(t, t0, SPRING.snappy);
    if (t > U_(13).v0) {
      ctx.save(); ctx.globalAlpha *= t < U_(16).v0 ? ap(t, U_(13).v0, 0.5) : clamp(kk * 1.4);
      card(ctx, 1300, 305, 520, 620, { r: 28, bg: C.forest });
      if (t < U_(16).v0) { text(ctx, 'MONSUN', 1340, 380, fU(48, 800), C.amber); text(ctx, 'monsoon', 1340, 425, fI(40), C.cream); wrap(ctx, 'angin yang berganti arah setiap ±6 bulan, akibat beda pemanasan benua dan samudra', fU(28, 600), 440).forEach((l, i) => text(ctx, l, 1340, 500 + i * 40, fU(28, 600), C.cream)); show(ctx, t, U_(15).v0, () => wrap(ctx, 'Indonesia di antara Benua Asia dan Benua Australia', fU(28, 800), 440).forEach((l, i) => text(ctx, l, 1340, 740 + i * 40, fU(28, 800), C.amber))); }
      else {
        rrect(ctx, 1300, 305, 520, 14, 7); ctx.fillStyle = P[4]; ctx.fill();
        text(ctx, P[0], 1340, 380, fU(44, 800), C.cream); text(ctx, P[1], 1340, 424, fI(36), mix(P[4], '#ffffff', 0.4)); text(ctx, P[2], 1340, 466, fU(26, 700), C.forest3);
        P[3].forEach((s, i) => show(ctx, t, t0 + 1 + i * 1.6, () => { circle(ctx, 1352, 548 + i * 86, 10); ctx.fillStyle = P[4]; ctx.fill(); text(ctx, s, 1376, 558 + i * 86, fU(30, 700), C.cream); }));
      }
      ctx.restore();
    }
    title(ctx, t, 'monsun', 'Monsun Asia–Australia');
  });
}

// ---------------------------------------------------------------- exceptions
function sBeda(ctx, t) {
  scene(ctx, t, 'beda', C.sand, () => {
    const box = { x: 110, y: 235, w: 1150, h: 690 }; const z = ap(t, U_(31).v0 - 0.5, 1.6, E.inOutCubic);
    const ext = [lerp(94, 120, z), lerp(132, 134, z), lerp(-12, -9, z), lerp(6, 2, z)]; const sy = (ext[1] - ext[0]) * box.h / box.w; ext[3] = ext[2] + sy;
    const pr = G.mapProj(box, ext);
    card(ctx, box.x - 8, box.y - 8, box.w + 16, box.h + 16, { r: 30 }); G.drawMap(ctx, IND, pr, { t, depth: 8 });
    ctx.save(); rrect(ctx, box.x, box.y, box.w, box.h, 26); ctx.clip();
    const e1 = pr(ext[0], 0), e2 = pr(ext[1], 0); ctx.strokeStyle = C.amber; ctx.lineWidth = 3; ctx.setLineDash([12, 8]); ctx.beginPath(); ctx.moveTo(e1[0], e1[1]); ctx.lineTo(e2[0], e2[1]); ctx.stroke(); ctx.setLineDash([]);
    [['Pontianak', 109.3, 0], ['Padang', 100.4, -0.95]].forEach(([n, lo, la]) => show(ctx, t, U_(30).v0, () => { const p = pr(lo, la); circle(ctx, p[0], p[1], 12); ctx.fillStyle = C.blue; ctx.fill(); pill(ctx, n, p[0], p[1] - 30, fU(22, 800), C.blue, C.cream, 12, 38, 'center'); }));
    show(ctx, t, U_(31).v0 + 1, () => { for (let i = 0; i < 6; i++) { const ph = (t * 0.4 + i / 6) % 1; const a = pr(lerp(131, 128.6, ph), lerp(-7, -4.2, ph) + (i - 3) * 0.3); const b = pr(lerp(131, 128.6, ph) - 0.4, lerp(-7, -4.2, ph) + 0.35 + (i - 3) * 0.3); ctx.globalAlpha = Math.sin(ph * Math.PI); arrowLine(ctx, a[0], a[1], b[0], b[1], C.blue, 6, 18); ctx.globalAlpha = 1; } const s = pr(129.5, -3.0); ctx.fillStyle = '#8a7350'; poly(ctx, [[s[0] - 60, s[1] + 20], [s[0], s[1] - 50], [s[0] + 60, s[1] + 20]]); ctx.fill(); cloud(ctx, s[0], s[1] - 70, 1.0, '#eef2f5'); rain(ctx, s[0], s[1] - 40, 80, t, 6); const a = pr(128.2, -3.7); circle(ctx, a[0], a[1], 12); ctx.fillStyle = C.forest; ctx.fill(); pill(ctx, 'Ambon', a[0] - 20, a[1] + 34, fU(22, 800), C.forest, C.cream, 12, 38, 'center'); const bs = pr(127, -6); text(ctx, 'Laut Banda', bs[0], bs[1], fU(24, 800), '#4a7da0', 'center'); });
    ctx.restore();
    show(ctx, t, U_(30).v0 + 0.5, () => { rainChart(ctx, 1300, 240, 520, 300, RAIN.pontianak, C.blue, ap(t, U_(30).v0 + 0.5, 1.4), 'Pontianak: DUA puncak hujan'); text(ctx, 'ITCZ melintas dua kali', 1320, 575, fU(24, 700), C.blue); });
    show(ctx, t, U_(31).v0, () => { rainChart(ctx, 1300, 610, 520, 300, RAIN.ambon, C.forest, ap(t, U_(31).v0, 1.4), 'Ambon: puncak Juni–Juli'); });
    title(ctx, t, 'beda', 'Tidak semua wilayah ikut pola monsun');
  });
}

run({
  DUR, no: 10, code: 'B01-10', chip: 'BAB 1 · IKLIM · OSN GEOGRAFI 2027', title: 'ITCZ dan Monsun', sub: 'monsun barat, monsun timur, pancaroba',
  lt: 'OSNGEO.id  ·  Bab 1 Iklim  ·  Tahap 2: Angin dan Sirkulasi',
  next: 'B01-11 · Sirkulasi Walker',
  SCN: [['hook', 0], ['itcz', 5], ['monsun', 13], ['beda', 29], ['soal', 32], ['jebakan', 37], ['ringkas', 40], ['outro', 43]],
  TERMS: [
    ['ITCZ', 'Intertropical Convergence Zone', 'Sabuk tekanan rendah tempat pasat bertemu; bergeser musiman', 5],
    ['Monsun', 'monsoon', 'Angin yang berganti arah setiap ±6 bulan', 14],
    ['Monsun barat', 'west monsoon', 'Des–Feb: dari Asia, basah, musim hujan', 16],
    ['Monsun timur', 'east monsoon', 'Jun–Agu: dari Australia, kering, kemarau', 22],
    ['Pancaroba', 'transition season', 'Peralihan: angin lemah, hujan lebat singkat, petir', 27],
  ],
  hook: { cards: [], punch: [4, ''] },
  soal: {
    q: 'Pada peta cuaca bulan Januari, tekanan tinggi berada di Siberia dan tekanan rendah di utara Australia. Angin di atas Laut Jawa bertiup dari arah …',
    opts: ['timur laut, tidak dibelokkan', 'tenggara, dari Australia', 'barat laut, dibelokkan ke kiri', 'barat daya, dari Samudra Hindia', 'utara, lurus dari Asia'], ans: 2, optFs: 27,
    ansT: () => tw('jawabannya', U_(36).v0 - 0.3),
    steps: () => [[U_(33).v0, '1) Tinggi (Asia) ke rendah (Australia)', C.forest3, 28], [U_(34).v0, 'BBU: angin dari timur laut', C.cream, 38], [U_(35).v0, '2) Menyeberangi ekuator', C.forest3, 28], [tw('kiri', U_(35).v0), 'BBS: Coriolis ke KIRI', C.cream, 38], [tw('barat', U_(35).v0), 'Laut Jawa: dari BARAT LAUT', C.amber, 48]],
  },
  jebakan: {
    title: 'Dua jebakan yang sering muncul',
    items: () => [[U_(38).v0, 'Monsun barat berasal dari Samudra Hindia', 'Monsun barat dari ASIA, berbelok setelah ekuator', tw('melainkan', U_(38).v0)],
      [U_(39).v0, 'Seluruh Indonesia hujan Des–Feb', 'Ambon (Jun–Jul) dan daerah ekuator (dua puncak) beda', tw('ingat', U_(39).v0)]],
  },
  ringkas: {
    items: () => [[tw('bergeser', U_(41).v0), 'ITCZ bergeser mengikuti matahari'], [tw('barat', U_(41).v0), 'Monsun barat: hujan · monsun timur: kemarau'], [tw('pancaroba', U_(41).v0), 'Di antaranya ada pancaroba']],
  },
  scenes: { hook: sHook, itcz: sItcz, monsun: sMonsun, beda: sBeda },
  async init() {
    W110 = await fetch('assets/world110.json').then((r) => r.json());
    const W50 = await fetch('assets/world50.json').then((r) => r.json());
    REG = G.subset(W50, [60, 170, -40, 30]); IND = G.subset(W50, [90, 145, -15, 10]);
    SD = G.seeds(520, [70, 160, -30, 24], 21);
  },
});
