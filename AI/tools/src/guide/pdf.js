const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.pdf({ path: process.argv[3], format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:7pt;color:#999;padding:0 13mm;display:flex;justify-content:space-between;font-family:Inter"><span>Red Alert 2: Yuri\'s Revenge · Sổ tay người chơi</span><span class="pageNumber"></span></div>' });
  await b.close();
})();
