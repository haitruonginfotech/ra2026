const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1920,height:945}});
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); }); p.on('dialog', d => d.accept());
  await p.goto('file://' + require('path').resolve(process.argv[2] || 'RA2_Mod_Editor.html'));
  await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go'); await p.waitForSelector('#list .row');
  // tạo thay đổi giống người dùng: giảm mảnh vỡ + FPS + sửa giá Sniper + sát thương 1 vũ khí
  await p.click('#b-perf'); await p.waitForSelector('#dlg-perf[open]'); await p.selectOption('#pf-debris','reduce'); await p.fill('#pf-detfps','30'); await p.click('#pf-go');
  await p.waitForSelector('#dlg-save[open]'); await p.click('#sv-cancel');
  await p.fill('#q','Sniper'); await p.click('#list .row >> nth=0'); const c = p.locator('input[data-k=Cost]').first(); await c.fill('700'); await c.dispatchEvent('change');
  await p.click('.wlink a >> nth=0'); await p.waitForTimeout(200); const dm = p.locator('input[data-k=Damage]').first(); await dm.fill('250'); await dm.dispatchEvent('change');
  const t0 = Date.now(); await p.click('#b-changes'); await p.waitForSelector('#dlg-changes[open]'); console.log('open ms', Date.now() - t0, 'groups', await p.locator('.cg').count(), 'rows', await p.locator('.cg-r').count());
  await p.screenshot({path:'chg1.png'});
  await p.locator('#dlg-changes .db').evaluate(e => e.scrollTop = 1e6); await p.screenshot({path:'chg2.png'});
  const kinds = await p.$$eval('.cg-h', hs => hs.map(h => h.querySelector('b').textContent + ' | ' + h.querySelector('.kind').textContent + ' | ' + (h.querySelector('img') ? 'img' : 'badge')));
  const cnt = {}; kinds.forEach(k => { const t = k.split(' | ')[1].replace(/ của .*| · dùng bởi .*/,''); cnt[t] = (cnt[t]||0) + 1; }); console.log(JSON.stringify(cnt));
  console.log(kinds.filter(k => /Mục khác|Hình ảnh/.test(k)).slice(0, 12).join('\n'));
  // hoàn lại 1 dòng
  await p.locator('[data-rv]').first().click(); await p.waitForTimeout(300); console.log('after revert', await p.textContent('#nchg'));
  // Xem -> điều hướng
  await p.locator('.cg-h a').last().click(); await p.waitForTimeout(300); console.log('dialog open?', await p.locator('#dlg-changes[open]').count(), 'view', await p.textContent('.dossier h1'));
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
