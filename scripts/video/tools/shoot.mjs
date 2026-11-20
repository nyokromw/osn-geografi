const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 2200 } });
  for (const f of process.argv.slice(2)) {
    await p.goto(`http://localhost:8765/${f}/thumbs.html`); await p.evaluate(async () => { await document.fonts.load('900 40px UI'); await document.fonts.load('40px D'); await document.fonts.ready; });
    await p.waitForTimeout(300);
    for (const [id, n] of [['a', '1_osn'], ['b', '2_formal_web'], ['c', '3_umum']]) { const dir = `out/${f}`; await (await p.$('#' + id)).screenshot({ path: `${dir}/thumb_${n}.png` }); }
  }
  await b.close();
})();
