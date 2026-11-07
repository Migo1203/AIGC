const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const fs=require('node:fs/promises');
const root='D:/WLQ/AIGC作品集/outputs/NED_高级A+_V03_20261107';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});const page=await browser.newPage({viewport:{width:1600,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(root+'/01_成品与预览/打开审阅V03.html').href);let n=0;
 async function decoded(){await page.locator('#page img').evaluateAll(es=>Promise.all(es.map(e=>e.decode())));const bad=await page.locator('#page img').evaluateAll(es=>es.filter(e=>!e.naturalWidth).map(e=>e.src));if(bad.length)throw Error(JSON.stringify(bad));n++;}
 await decoded();
 for(const module of ['P03','P04'])for(const i of [0,1,2]){await page.locator(`section[data-module="${module}"] button`).nth(i).click();await decoded();}
 await page.locator('#mobile').click();await page.setViewportSize({width:390,height:1000});await decoded();
 for(const module of ['P02','P03','P04']){const count=await page.locator(`section[data-module="${module}"] button`).count();for(let i=0;i<count;i++){await page.locator(`section[data-module="${module}"] button`).nth(i).click();await decoded();}}
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);if(overflow)throw Error('390px horizontal overflow');
 await page.setViewportSize({width:375,height:1000});await decoded();if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('375px horizontal overflow');
 await page.locator('#overview').click();await page.locator('#all img').evaluateAll(es=>Promise.all(es.map(e=>e.decode())));const all=await page.locator('#all img').count();if(all!==21)throw Error('Expected 21 states');
 const svgChecks=[];
 for(const v of ['PC','Mobile']){
  await page.setViewportSize({width:v==='PC'?1600:390,height:1000});await page.goto(pathToFileURL(root+'/02_可编辑SVG/NED_V03_连续长页_'+v+'.svg').href);await page.evaluate(()=>document.fonts.ready);await page.locator('image').evaluateAll(es=>Promise.all(es.map(async e=>{const i=new Image();i.src=e.getAttribute('href');await i.decode()})));
  const r=await page.locator('text').evaluateAll(es=>es.map(e=>{const b=e.getBBox();return{id:e.id,text:e.textContent,x:b.x,y:b.y}}));svgChecks.push({variant:v,textObjects:r.length});
 }
 await browser.close();const result={decodedReviewStates:n,allStateImages:all,phoneWidths:[375,390],horizontalOverflow:false,scriptErrors:errors,longPageSvg:svgChecks};await fs.writeFile(root+'/04_过程记录/审阅页检查.json',JSON.stringify(result,null,2));console.log(JSON.stringify(result));if(errors.length)process.exitCode=1;
})();
