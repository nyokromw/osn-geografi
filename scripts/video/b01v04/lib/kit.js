// OSNGEO.id concept-video kit (3–5 min videos): scene timing, bilingual term cards, soal, jebakan, ringkasan + glosarium, hook, outro.
import * as M from './motion.js';
import {
  C, fD, fU, T, tw, U_, sp, ap, poly, circle, card, arrowLine, check, cross, wrap, riseText, pill, warnIcon,
  cornerMark, centerMark, lowerThird, buildCaps, captions, intro, outro,
} from './common.js';
const { W, H, E, prog, lerp, clamp, SPRING, text, fill, rrect, bump } = M;

export const fI = (s) => `${Math.round(s)}px DisplayI`;
export const SC = {};
export const HITS = [];
export const hit = (t, label, sfx, o = {}) => HITS.push([t, label, sfx, { gain: 0.55, ...o }]);
export const u = (i) => U_(i);
export const exitP = (t, n, d = 0.35) => E.inCubic(prog(t, SC[n][1] - d, SC[n][1]));
export const title = (ctx, t, n, s, col = C.forest) => { let fs = 72; ctx.font = fD(fs); while (ctx.measureText(s).width > 1040 && fs > 48) { fs -= 2; ctx.font = fD(fs); } riseText(ctx, s, 110, 165, fD(fs), col, ap(t, SC[n][0] + 0.1, 0.55, E.outQuint)); };
export const show = (ctx, t, t0, fn, d = 0.45) => { const p = ap(t, t0, d); if (p <= 0) return; ctx.save(); ctx.globalAlpha *= p; fn(p); ctx.restore(); };
// "T" with raised exponent, returns width
export function sup(ctx, base, exp, x, y, size, weight, color, align = 'left') {
  ctx.font = fU(size, weight); const w1 = ctx.measureText(base).width; ctx.font = fU(size * 0.58, weight); const w2 = ctx.measureText(exp).width;
  const x0 = align === 'center' ? x - (w1 + w2) / 2 : align === 'right' ? x - w1 - w2 : x;
  text(ctx, base, x0, y, fU(size, weight), color); text(ctx, exp, x0 + w1 + 2, y - size * 0.42, fU(size * 0.58, weight), color);
  return w1 + w2 + 2;
}
// scene wrapper: background + fade-out
export function scene(ctx, t, n, bg, fn) { fill(ctx, bg); const ex = exitP(t, n); ctx.save(); ctx.globalAlpha = 1 - ex; fn(); ctx.restore(); }

let CFG = null;
function buildScenes() {
  SC.intro = [0, 3.0];
  const S = CFG.SCN;
  S.forEach(([n, ui], i) => { SC[n] = [i === 0 ? 3.0 : U_(ui).v0 - 0.2, i < S.length - 1 ? U_(S[i + 1][1]).v0 - 0.2 : CFG.DUR]; });
}

// ---------------------------------------------------------------- bilingual term cards
function termCard(ctx, t) {
  const TM = CFG.TERMS, N = TM.length;
  for (let i = 0; i < N; i++) {
    const [term, eng, def, ui] = TM[i];
    const t0 = typeof ui === 'number' ? U_(ui).v0 : ui();
    const nx = i < N - 1 ? (typeof TM[i + 1][3] === 'number' ? U_(TM[i + 1][3]).v0 : TM[i + 1][3]()) : 1e9;
    const t1 = Math.min(t0 + 8, nx - 0.1, SC.soal[0]);
    if (t < t0 || t > t1 + 0.4) continue;
    const p = M.spring(t - t0, SPRING.snappy), q = E.inCubic(prog(t, t1, t1 + 0.4));
    const x = 1212 + (1 - p) * 80 + q * 80, y = 140, w = 668, h = 150;
    ctx.save(); ctx.globalAlpha = clamp(p * 1.4) * (1 - q);
    card(ctx, x, y, w, h, { r: 24, bg: C.cream });
    rrect(ctx, x, y, 12, h, 6); ctx.fillStyle = C.clay; ctx.fill();
    text(ctx, `ISTILAH ${i + 1}/${N}`, x + 34, y + 32, fU(20, 700), C.clay);
    let fs = 38; ctx.font = fU(fs, 700); while (ctx.measureText(term).width > w - 70 && fs > 26) { fs -= 2; ctx.font = fU(fs, 700); }
    text(ctx, term, x + 34, y + 72, fU(fs, 700), C.ink);
    if (eng) { let fe = 34; ctx.font = fI(fe); while (ctx.measureText(eng).width > w - 70 && fe > 22) { fe -= 2; ctx.font = fI(fe); } text(ctx, eng, x + 34, y + 108, fI(fe), C.clayD); }
    text(ctx, wrap(ctx, def, fU(21, 500), w - 60)[0], x + 34, y + 138, fU(21, 500), C.gray);
    ctx.restore();
  }
}

// ---------------------------------------------------------------- hook (3 cards + punch word)
function sHook(ctx, t) {
  const H_ = CFG.hook;
  scene(ctx, t, 'hook', C.sand, () => {
    H_.cards.forEach(([t0f, a, b, draw, bg], i) => {
      const t0 = typeof t0f === 'number' ? U_(t0f).v0 : t0f();
      const k = M.spring(t - t0, SPRING.gentle); if (k <= 0) return;
      const x = 90 + i * 590, y = 200;
      ctx.save(); ctx.translate(0, (1 - k) * 80); ctx.globalAlpha *= clamp(k * 1.5);
      card(ctx, x, y, 560, 560, { r: 30 });
      ctx.save(); rrect(ctx, x + 20, y + 20, 520, 420, 22); ctx.clip(); ctx.fillStyle = bg || '#f1e6d6'; ctx.fillRect(x, y, 560, 460); draw(ctx, x, y, t, t0); ctx.restore();
      text(ctx, a, x + 30, y + 495, fU(36, 700), C.ink); text(ctx, b, x + 30, y + 535, fU(25, 500), C.gray);
      ctx.restore();
    });
    const pt = M.spring(t - (typeof H_.punch[0] === 'number' ? U_(H_.punch[0]).v0 - 0.1 : H_.punch[0]()), SPRING.bouncy);
    if (pt > 0) { ctx.save(); ctx.translate(W / 2, 470); ctx.scale(pt, pt); ctx.font = fD(104); const w = ctx.measureText(H_.punch[1]).width + 120; card(ctx, -w / 2, -90, w, 170, { r: 40, bg: C.forest }); text(ctx, H_.punch[1], 0, 30, fD(104), C.cream, 'center'); ctx.restore(); }
  });
}

// ---------------------------------------------------------------- soal
function sSoal(ctx, t) {
  const Q = CFG.soal;
  scene(ctx, t, 'soal', C.sand, () => {
    const [tp0, tp1] = T.tm.pause;
    const dock = ap(t, tp1 + 0.2, 0.7, E.inOutCubic);
    const correct = ap(t, Q.ansT(), 0.3);
    const opt = (i, ox, oy, ow, oh, fs) => {
      const on = i === Q.ans && correct > 0; ctx.save(); ctx.globalAlpha *= correct > 0 && i !== Q.ans ? 0.35 : 1;
      rrect(ctx, ox, oy, ow, oh, 16); ctx.fillStyle = on ? C.clay : C.sand; ctx.fill();
      circle(ctx, ox + oh * 0.5, oy + oh / 2, oh * 0.3); ctx.fillStyle = on ? C.cream : C.forest; ctx.fill();
      text(ctx, 'ABCDE'[i], ox + oh * 0.5, oy + oh / 2 + fs * 0.36, fU(fs * 0.9, 700), on ? C.clay : C.cream, 'center');
      text(ctx, Q.opts[i], ox + oh + 10, oy + oh / 2 + fs * 0.36, fU(fs, 700), on ? C.cream : C.ink);
      ctx.restore();
    };
    const pq = M.spring(t - SC.soal[0] - 0.3, SPRING.snappy);
    if (pq > 0 && dock < 1) {
      ctx.save(); ctx.globalAlpha *= clamp(pq * 1.5) * (1 - dock); ctx.translate(210, 120 + (1 - pq) * 80);
      card(ctx, 0, 0, 1500, 790, { r: 32 }); pill(ctx, 'CONTOH SOAL OSN', 50, 64, fU(28, 700), C.clay, C.cream, 22, 54);
      wrap(ctx, Q.q, fU(38, 500), 1400).forEach((l, i) => text(ctx, l, 50, 160 + i * 52, fU(38, 500), C.ink));
      Q.opts.forEach((o, i) => opt(i, 50 + (i % 3) * 470, 420 + Math.floor(i / 3) * 140, 440, 110, Q.optFs || 36));
      ctx.restore();
    }
    if (t > tp0 - 0.2 && t < tp1 + 0.4) {
      const a = 1 - ap(t, tp1, 0.35), p = clamp((t - tp0) / (tp1 - tp0));
      ctx.save(); ctx.globalAlpha *= a * ap(t, tp0 - 0.2, 0.3);
      const cx = 1790, cy = 330; circle(ctx, cx, cy, 76); ctx.fillStyle = C.forest; ctx.fill();
      ctx.strokeStyle = C.amber; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy, 60, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * (1 - p)); ctx.stroke();
      text(ctx, `${Math.max(1, Math.ceil((tp1 - tp0) - (t - tp0)))}`, cx, cy + 26, fU(70, 700), C.cream, 'center'); ctx.restore();
    }
    if (dock > 0) {
      ctx.save(); ctx.globalAlpha *= dock;
      card(ctx, 80, 130, 860, 790, { r: 30 }); pill(ctx, 'CONTOH SOAL OSN', 120, 186, fU(24, 700), C.clay, C.cream, 20, 48);
      const ql = wrap(ctx, Q.q, fU(28, 500), 780); ql.forEach((l, i) => text(ctx, l, 120, 255 + i * 38, fU(28, 500), C.ink));
      const oy = Math.max(470, 255 + ql.length * 38 + 20);
      Q.opts.forEach((o, i) => opt(i, 120, oy + i * 84, 780, 72, 28));
      card(ctx, 990, 130, 850, 790, { r: 30, bg: C.forest });
      let y = 215; Q.steps().forEach(([t0, s, col, size]) => {
        const p = ap(t, t0, 0.5, E.outQuint);
        const lines = wrap(ctx, s, fU(size, 700), 770);
        lines.forEach((l) => { if (p > 0) { ctx.save(); ctx.beginPath(); ctx.rect(1010, y - size - 10, 810, size + 30); ctx.clip(); text(ctx, l, 1040, y + (1 - p) * (size + 30), fU(size, 700), col); ctx.restore(); } y += size + 16; });
        y += 22;
      });
      show(ctx, t, Q.ansT(), () => pill(ctx, `Jawaban: ${'ABCDE'[Q.ans]}`, 1415, 870, fU(36, 700), C.clay, C.cream, 30, 64, 'center'));
      ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- jebakan
function sJebakan(ctx, t) {
  const J = CFG.jebakan;
  scene(ctx, t, 'jebakan', C.sand, () => {
    const pw = M.spring(t - SC.jebakan[0] - 0.05, SPRING.bouncy);
    if (pw > 0) { ctx.save(); ctx.translate(180, 150); ctx.scale(pw, pw); warnIcon(ctx, 0, 0, 60); ctx.restore(); }
    riseText(ctx, J.title, 280, 175, fD(72), C.clayD, ap(t, SC.jebakan[0] + 0.15, 0.5, E.outQuint));
    J.items().forEach(([t0, wrong, right, tfix], i) => {
      const p = M.spring(t - t0, SPRING.snappy); if (p <= 0) return;
      const y = 280 + i * 250; ctx.save(); ctx.globalAlpha *= clamp(p * 1.5); ctx.translate((1 - p) * 80, 0);
      card(ctx, 110, y, 1700, 210, { r: 26 }); text(ctx, `${i + 1}`, 170, y + 120, fU(70, 700), C.clay, 'center');
      const f = ap(t, tfix - 0.3, 0.4);
      text(ctx, wrong, 250, y + 82, fU(36, 600), f > 0 ? 'rgba(152,63,41,0.6)' : C.clayD);
      if (f > 0) { ctx.strokeStyle = C.clay; ctx.lineWidth = 5; ctx.font = fU(36, 600); const w = ctx.measureText(wrong).width; ctx.beginPath(); ctx.moveTo(250, y + 70); ctx.lineTo(250 + w * f, y + 70); ctx.stroke(); ctx.save(); ctx.globalAlpha *= f; circle(ctx, 280, y + 150, 24); ctx.fillStyle = C.forest; ctx.fill(); check(ctx, 280, y + 150, 28, C.cream, f); text(ctx, right, 322, y + 163, fU(36, 700), C.forest); ctx.restore(); }
      ctx.restore();
    });
    if (J.extra) J.extra(ctx, t);
  });
}

// ---------------------------------------------------------------- ringkasan + glosarium
function sRingkas(ctx, t) {
  const R = CFG.ringkas;
  scene(ctx, t, 'ringkas', C.forestD, () => {
    ctx.save(); ctx.globalAlpha *= 0.06; ctx.strokeStyle = C.cream; for (let x = 0; x < W; x += 80) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); } ctx.restore();
    ctx.save(); ctx.globalAlpha *= ap(t, SC.ringkas[0] + 0.05, 0.5); pill(ctx, 'RINGKASAN', 110, 120, fU(30, 700), C.clay, C.cream, 24, 58); ctx.restore();
    riseText(ctx, R.title || 'Yang wajib kamu ingat', 110, 225, fD(72), C.cream, ap(t, SC.ringkas[0] + 0.2, 0.5, E.outQuint));
    R.items().forEach(([t0, s], i) => {
      const k = M.spring(t - t0, SPRING.snappy); if (k <= 0) return;
      const y = 290 + i * 160; ctx.save(); ctx.globalAlpha *= clamp(k * 1.4); ctx.translate((1 - k) * -60, 0);
      rrect(ctx, 110, y, 900, 136, 22); ctx.fillStyle = bump(t, t0 + 0.3, 1.2) > 0.1 ? C.clay : 'rgba(255,254,250,0.1)'; ctx.fill();
      text(ctx, `${i + 1}`, 160, y + 86, fU(52, 700), C.amber, 'center');
      wrap(ctx, s, fU(32, 700), 790).forEach((l, j, arr) => text(ctx, l, 210, y + 68 + (j - (arr.length - 1) / 2) * 40 + 12, fU(32, 700), C.cream));
      ctx.restore();
    });
    // glossary
    const pg = ap(t, SC.ringkas[0] + 0.4, 0.6);
    if (pg > 0) {
      ctx.save(); ctx.globalAlpha *= pg;
      rrect(ctx, 1070, 270, 750, 640, 26); ctx.fillStyle = 'rgba(255,254,250,0.07)'; ctx.fill();
      text(ctx, 'ISTILAH ASING OSN', 1110, 322, fU(24, 700), C.amber);
      const G = CFG.TERMS.filter((x) => x[1]);
      const lh = Math.min(64, 560 / G.length);
      G.forEach(([id, en], i) => {
        const y = 370 + i * lh; const k = ap(t, SC.ringkas[0] + 0.6 + i * 0.12, 0.4); if (k <= 0) return;
        ctx.save(); ctx.globalAlpha *= k;
        let fs = Math.min(27, lh * 0.5); ctx.font = fU(fs, 600); while (ctx.measureText(id).width > 330 && fs > 16) { fs--; ctx.font = fU(fs, 600); }
        text(ctx, id, 1110, y, fU(fs, 600), C.forest3);
        let fe = Math.min(32, lh * 0.6); ctx.font = fI(fe); while (ctx.measureText(en).width > 340 && fe > 18) { fe--; ctx.font = fI(fe); }
        text(ctx, en, 1785, y, fI(fe), C.cream, 'right');
        ctx.restore();
      });
      ctx.restore();
    }
  });
}

// ---------------------------------------------------------------- hits
function addHits() {
  CFG.SCN.forEach(([n], i) => { if (i > 0 && n !== 'outro') hit(SC[n][0] + 0.2, 'scene ' + n, 'whoosh', { len: 0.4, gain: 0.22 }); });
  CFG.TERMS.forEach(([s, , , ui]) => hit(typeof ui === 'number' ? U_(ui).v0 : ui(), 'term ' + s, 'pop', { pitch: 'A5', gain: 0.3 }));
  hit((typeof CFG.hook.punch[0] === 'number' ? U_(CFG.hook.punch[0]).v0 : CFG.hook.punch[0]()) - 0.1, 'title', 'bell', { pitch: 'D6', gain: 0.35 });
  const [p0] = T.tm.pause; for (let k = 0; k < 4; k++) hit(p0 + k, 'timer ' + k, 'blip', { pitch: 880, gain: 0.22 });
  hit(CFG.soal.ansT(), 'answer', 'bell', { pitch: 'E6', gain: 0.4 });
  CFG.ringkas.items().forEach(([t0], i) => hit(t0, 'recap ' + i, 'click', { gain: 0.3 }));
  hit(SC.outro[0] + 0.2, 'logo', 'bell', { pitch: 'D6', gain: 0.4 });
  (CFG.hits || (() => {}))(hit);
  HITS.sort((a, b) => a[0] - b[0]);
}

export function run(cfg) {
  CFG = cfg;
  const DRAW = { hook: sHook, soal: sSoal, jebakan: sJebakan, ringkas: sRingkas, ...cfg.scenes };
  M.film({
    fonts: [M.font(100, 400, 'Display'), '40px DisplayI', M.font(40, 500, 'UI'), M.font(40, 600, 'UI'), M.font(40, 700, 'UI')],
    hits: HITS,
    samples: () => 3,
    async init() {
      T.tm = await fetch('timing.json').then((r) => r.json());
      if (cfg.init) await cfg.init();
      buildScenes(); buildCaps(); addHits();
    },
    draw(ctx, uu, t) {
      const S = Object.keys(SC).find((k) => t >= SC[k][0] && t < SC[k][1]) || 'outro';
      if (S === 'intro') intro(ctx, t, cfg.chip, cfg.title, cfg.sub);
      else if (S === 'outro') outro(ctx, t, SC.outro[0], SC.outro[0] + 1.4, 'Menu Soal Pendalaman Materi  ·  Bab 1', cfg.next);
      else DRAW[S](ctx, t);
      if (S !== 'intro' && S !== 'outro') { centerMark(ctx, S === 'ringkas' ? 0.9 : 1, S === 'ringkas' ? C.cream : C.forest); if (S !== 'ringkas') termCard(ctx, t); }
      lowerThird(ctx, t, `OSNGEO.id  ·  Bab 1 Iklim  ·  Video #${cfg.no}  ·  ${cfg.code}`);
      if (S !== 'intro') captions(ctx, t);
      cornerMark(ctx);
    },
  });
}
