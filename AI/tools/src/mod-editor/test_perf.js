const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const fx = n => fs.readFileSync('fx/' + n, 'latin1');
  const b = await chromium.launch(); const ctx = await b.newContext({viewport:{width:1440,height:900}}); const p = await ctx.newPage();
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  p.on('dialog', d => d.accept());
  await p.goto('http://127.0.0.1:8765/RA2_Mod_Editor.html');
  await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go');
  await p.waitForSelector('#list .row');
  // no folder
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]'); await p.screenshot({path:'p0_nofolder.png'});
  console.log('nofolder prev:', await p.textContent('#pf-prev'));
  await p.click('#pf-cancel');
  // fake folder in OPFS
  await p.evaluate(async files => {
    const root = await navigator.storage.getDirectory();
    for (const [n, t] of Object.entries(files)){ const fh = await root.getFileHandle(n, {create:true}); const w = await fh.createWritable(); await w.write(Uint8Array.from(t, c => c.charCodeAt(0))); await w.close(); }
    dir = root; updateSrc();
  }, {'gamemd.exe':'MZ', 'ddraw.ini':fx('ddraw.ini'), 'RA2MD.INI':fx('RA2MD.INI'), 'RA2.INI':fx('RA2.INI')});
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]');
  console.log('initial prev:', await p.textContent('#pf-prev'));
  await p.screenshot({path:'p1_open.png'});
  await p.click('#pf-reco'); await p.waitForTimeout(100);
  await p.selectOption('#pf-det-yr','1');
  console.log('reco prev:', await p.textContent('#pf-prev'));
  await p.locator('#dlg-perf .db').evaluate(e => e.scrollTop = 0); await p.screenshot({path:'p2_reco.png'});
  await p.locator('#dlg-perf .db').evaluate(e => e.scrollTop = 9999); await p.screenshot({path:'p3_reco_bottom.png'});
  await p.click('#pf-go');
  await p.waitForSelector('#dlg-save[open]'); await p.screenshot({path:'p4_save.png'});
  await p.click('#sv-go'); await p.waitForTimeout(800);
  console.log('toast:', await p.locator('.toast').textContent().catch(()=>'-'));
  const out = await p.evaluate(async () => {
    const root = await navigator.storage.getDirectory(); const o = {};
    for await (const [n, h] of root.entries()){ if (h.kind === 'file') { const u = new Uint8Array(await (await h.getFile()).arrayBuffer()); let s=''; for (const x of u) s += String.fromCharCode(x); o[n] = s; } else { o[n + '/'] = []; for await (const [m] of h.entries()) o[n + '/'].push(m); } }
    return o;
  });
  for (const [n, t] of Object.entries(out)) { if (Array.isArray(t)) console.log(n, t); else fs.writeFileSync('out_' + n, t, 'latin1'); }
  console.log('undo enabled', !(await p.locator('#b-undo').isDisabled()), 'nchg', await p.textContent('#nchg'));
  // reopen: should say nothing changes
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]'); console.log('reopen prev:', await p.textContent('#pf-prev'));
  await p.setViewportSize({width:390, height:800}); await p.waitForTimeout(200); await p.screenshot({path:'p5_mobile.png'});
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
