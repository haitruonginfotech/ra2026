const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w,h] of [[2560,1440],[1920,1080],[1440,900],[1366,768],[1280,720],[1024,768],[853,480],[820,1180],[390,844]]){
    const p = await b.newPage({viewport:{width:w,height:h}}); p.on('dialog', d => d.accept());
    await p.goto('file://' + require('path').resolve(process.argv[2] || 'RA2_Mod_Editor.html'));
    await p.waitForSelector('#dlg-start[open]'); await p.check('input[name=src][value=mod]'); await p.click('#st-go'); await p.waitForSelector('.fields');
    const r = await p.evaluate(() => { const sv = document.querySelector('#b-save').getBoundingClientRect(); const ls = document.querySelector('#list').getBoundingClientRect(); return {
      fields: getComputedStyle(document.querySelector('.fields')).gridTemplateColumns.split(' ').length,
      hscroll: document.documentElement.scrollWidth > innerWidth + 1, barH: document.querySelector('.bar').offsetHeight,
      saveVisible: sv.right <= innerWidth && sv.bottom <= innerHeight && sv.width > 0, listBottom: Math.round(ls.bottom), mainScroll: document.querySelector('main').scrollHeight > document.querySelector('main').clientHeight }; });
    console.log(w+'x'+h, JSON.stringify(r)); await p.close();
  }
  await b.close();
})();
