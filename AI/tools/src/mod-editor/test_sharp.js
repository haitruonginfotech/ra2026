const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const fx = n => fs.readFileSync('fx/' + n, 'latin1');
  const b = await chromium.launch(); const ctx = await b.newContext({viewport:{width:1440,height:900}, screen:{width:1920,height:1080}}); const p = await ctx.newPage();
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  p.on('dialog', d => d.accept());
  await p.goto('http://127.0.0.1:8765/RA2_Mod_Editor.html');
  await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go'); await p.waitForSelector('#list .row');
  const files = {'gamemd.exe':'MZ', 'ddraw.ini':fx('ddraw.ini'), 'RA2MD.INI':fx('RA2MD.INI'), 'RA2.INI':fx('RA2.INI')};
  const read = async () => p.evaluate(async () => { const root = await navigator.storage.getDirectory(); const o = {}; for await (const [n, h] of root.entries()) if (h.kind === 'file'){ const u = new Uint8Array(await (await h.getFile()).arrayBuffer()); let s=''; for (const x of u) s += String.fromCharCode(x); o[n] = s; } return o; });
  await p.evaluate(async files => { const root = await navigator.storage.getDirectory(); for await (const [n] of root.entries()) await root.removeEntry(n, {recursive:true});
    for (const [n, t] of Object.entries(files)){ const fh = await root.getFileHandle(n, {create:true}); const w = await fh.createWritable(); await w.write(Uint8Array.from(t, c => c.charCodeAt(0))); await w.close(); } dir = root; updateSrc(); }, files);
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]');
  console.log('scale now:', await p.inputValue('#pf-scale'), 'maintas', await p.inputValue('#pf-maintas'), '| prev:', await p.textContent('#pf-prev'));
  await p.click('#pf-sharp'); console.log('sharp prev:', await p.textContent('#pf-prev'));
  await p.locator('.ph', {hasText:'Độ nét hình'}).scrollIntoViewIfNeeded(); await p.screenshot({path:'s1_sharp.png'});
  await p.click('#pf-go'); await p.waitForTimeout(500);
  let o = await read(); fs.writeFileSync('out_sharp_ddraw.ini', o['ddraw.ini'], 'latin1'); fs.writeFileSync('out_sharp_RA2MD.INI', o['RA2MD.INI'], 'latin1'); fs.writeFileSync('out_sharp_RA2.INI', o['RA2.INI'], 'latin1');
  // reopen: state detection
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]');
  console.log('reopen scale:', await p.inputValue('#pf-scale'), 'res yr', await p.inputValue('#pf-res-yr'), '| prev:', await p.textContent('#pf-prev'));
  await p.selectOption('#pf-scale','xbrz'); console.log('after xbrz renderer=', await p.inputValue('#pf-renderer'), '| prev:', await p.textContent('#pf-prev'));
  await p.selectOption('#pf-renderer','direct3d9'); console.log('back d3d9 scale=', await p.inputValue('#pf-scale'));
  await p.selectOption('#pf-scale','xbrz'); await p.click('#pf-go'); await p.waitForTimeout(500);
  o = await read(); fs.writeFileSync('out_xbrz_ddraw.ini', o['ddraw.ini'], 'latin1');
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]'); console.log('reopen2 scale:', await p.inputValue('#pf-scale'), 'renderer', await p.inputValue('#pf-renderer'), '| prev:', await p.textContent('#pf-prev'));
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
