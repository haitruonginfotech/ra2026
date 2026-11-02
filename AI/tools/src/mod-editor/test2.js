const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const out = process.argv[3];
  const b = await chromium.launch(); const ctx = await b.newContext({viewport:{width:1440,height:900}, acceptDownloads:true}); const p = await ctx.newPage();
  const errs=[]; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type()==='error') errs.push(m.text()); });
  p.on('dialog', d => d.accept());
  await p.goto('file://' + process.argv[2]);
  await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go');
  await p.waitForSelector('#list .row');
  // 1 edit cost
  await p.click('[data-cat=veh]'); await p.fill('#q','HTNK'); await p.click('#list .row >> nth=0');
  let c = p.locator('input[data-k=Cost]').first(); await c.fill('500'); await c.dispatchEvent('change');
  // weapon link
  await p.click('.wlink a >> nth=0'); await p.waitForTimeout(200);
  console.log('weapon view:', await p.textContent('.dossier h1'));
  await p.screenshot({path: out+'/t_weapon.png'});
  const dmg = p.locator('input[data-k=Damage]').first(); console.log('dmg before', await dmg.inputValue()); await dmg.fill('200'); await dmg.dispatchEvent('change');
  // verses edit
  const v0 = p.locator('[data-verse="5"]'); if (await v0.count()) { await v0.fill('150%'); await v0.dispatchEvent('change'); }
  // general
  await p.fill('#q',''); await p.click('[data-cat=gen]'); await p.waitForTimeout(200);
  console.log('gen view:', await p.textContent('.dossier h1'));
  const bs = p.locator('input[data-k=BuildSpeed]').first(); console.log('BuildSpeed', await bs.inputValue());
  await p.screenshot({path: out+'/t_general.png'});
  // quick mod: cost 0.5 for Yuri only infantry
  await p.click('#b-quick'); await p.selectOption('#qs-side','Y'); await p.selectOption('#qs-cat','InfantryTypes'); await p.fill('#qo-cost','0.5');
  console.log(await p.textContent('#q-prev'));
  await p.screenshot({path: out+'/t_quick.png'});
  await p.click('#q-go'); await p.waitForTimeout(300);
  console.log('changes after quick', await p.textContent('#nchg'));
  // undo quick
  await p.click('#b-undo'); await p.waitForTimeout(300); console.log('after undo', await p.textContent('#nchg'));
  await p.keyboard.press('Control+Shift+Z'); await p.waitForTimeout(300); console.log('after redo', await p.textContent('#nchg'));
  // changes dialog
  await p.click('#b-changes'); await p.waitForSelector('#dlg-changes[open]'); await p.screenshot({path: out+'/t_changes.png'});
  await p.click('#cg-close');
  // clone
  await p.click('[data-cat=veh]'); await p.fill('#q','HTNK'); await p.click('#list .row >> nth=0');
  await p.click('#b-clone'); await p.fill('#cl-id','HTNK2'); await p.click('#cl-go'); await p.waitForTimeout(300);
  console.log('clone view', await p.textContent('.dossier h1'), await p.textContent('.dossier code'));
  // save -> download
  await p.click('#b-save'); await p.waitForSelector('#dlg-save[open]');
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#sv-dl')]);
  await dl.saveAs(out+'/out_rulesmd.ini'); console.log('downloaded', dl.suggestedFilename());
  // switch RA2
  await p.click('[data-game=ra2]'); await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go');
  await p.waitForTimeout(500); await p.click('[data-cat=inf]'); await p.waitForTimeout(200);
  console.log('ra2 inf rows', await p.locator('#list .row').count());
  await p.screenshot({path: out+'/t_ra2.png'});
  console.log('errors', JSON.stringify(errs));
  await b.close();
})();
