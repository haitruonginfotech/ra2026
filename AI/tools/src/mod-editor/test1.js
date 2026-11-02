const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1440,height:900}});
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  await p.goto('file://' + process.argv[2]);
  await p.waitForSelector('#dlg-start[open]');
  await p.screenshot({path: process.argv[3]+'/s0.png'});
  await p.check('input[name=src][value=mod]'); await p.click('#st-go');
  await p.waitForSelector('#list .row');
  console.log('rows inf', await p.locator('#list .row').count());
  await p.screenshot({path: process.argv[3]+'/s1.png'});
  // pick Rhino
  await p.click('[data-cat=veh]'); await p.fill('#q','HTNK'); await p.click('#list .row >> nth=0');
  await p.screenshot({path: process.argv[3]+'/s2.png', fullPage:false});
  // change cost
  const cost = p.locator('input[data-k=Cost]').first(); await cost.fill('500'); await cost.dispatchEvent('change');
  console.log('changes', await p.textContent('#nchg'));
  await p.screenshot({path: process.argv[3]+'/s3.png'});
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
