const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs/promises'),path=require('node:path');
const root='D:/WLQ/AIGC作品集';
(async()=>{
 const build=JSON.parse(await fs.readFile(path.join(root,'work/ned-brand-showcase-build.json'),'utf8'));const out=build.output;
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 async function open(file){const svg=await fs.readFile(file,'utf8');await page.setContent('<html><head><meta charset="utf-8"><style>html,body{margin:0}body>svg{display:block}</style></head><body>'+svg+'</body></html>');await page.evaluate(()=>document.fonts.ready);}
 await open(path.join(out,'02_可编辑SVG/03_品牌故事展示_V04_可编辑.svg'));
 const failedImages=await page.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(null);im.onerror=()=>resolve(e.id||e.getAttribute('href').slice(0,50));im.src=e.getAttribute('href')})))).then(x=>x.filter(Boolean));
 const copy=await page.locator('[data-copy]').evaluateAll(es=>es.map(e=>({key:e.dataset.copy,text:[...e.querySelectorAll('text')].map(t=>t.textContent).join(' ')})));
 const copyErrors=copy.filter(e=>e.text!==build.copy[e.key]);
 const geometry=await page.evaluate(()=>{
  const ctx=document.createElement('canvas').getContext('2d');
  const glyphs=[...document.querySelectorAll('text')].map(e=>{
   const style=getComputedStyle(e),size=parseFloat(style.fontSize);ctx.font=`${style.fontWeight} ${size}px ${style.fontFamily}`;
   const m=ctx.measureText(e.textContent),matrix=e.getScreenCTM();const x=parseFloat(e.getAttribute('x')),y=parseFloat(e.getAttribute('y'));
   const p1=new DOMPoint(x-m.actualBoundingBoxLeft,y-m.actualBoundingBoxAscent).matrixTransform(matrix),p2=new DOMPoint(x+m.actualBoundingBoxRight,y+m.actualBoundingBoxDescent).matrixTransform(matrix);
   return {id:e.id,text:e.textContent,x:p1.x,y:p1.y,w:p2.x-p1.x,h:p2.y-p1.y};
  });
  const overflow=glyphs.filter(e=>e.x<0||e.y<0||e.x+e.w>1600||e.y+e.h>6600),overlaps=[];
  for(let i=0;i<glyphs.length;i++)for(let j=i+1;j<glyphs.length;j++){const a=glyphs[i],b=glyphs[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>.5&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>.5)overlaps.push([a.id,b.id]);}
  const cardOverflow=[];
  for(const card of document.querySelectorAll('[data-card]')){
   const [x,y,w,h]=card.dataset.bounds.split(',').map(Number),m=card.getScreenCTM(),a=new DOMPoint(x,y).matrixTransform(m),b=new DOMPoint(x+w,y+h).matrixTransform(m);
   for(const e of card.querySelectorAll('text')){const r=e.getBoundingClientRect();if(r.left<a.x||r.right>b.x||r.top<a.y||r.bottom>b.y)cardOverflow.push({card:card.dataset.card,text:e.textContent});}
  }
  return {textCount:glyphs.length,overflow,overlaps,cardOverflow};
 });
 const modules=await page.locator('[data-module]').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return {key:e.dataset.module,x:r.x,y:r.y,w:r.width,h:r.height}}));
 for(let i=0;i<modules.length;i++)for(const k of ['x','y','w','h'])if(Math.abs(modules[i][k]-build.placements[i][k])>.02)throw Error('Module placement mismatch '+modules[i].key);
 await page.screenshot({path:path.join(out,'01_成品与预览/03_品牌故事展示_V04_1600x6600.png'),fullPage:true});
 for(const source of build.sources){
  await page.setViewportSize({width:source.key==='B00_Desktop'?1464:390,height:625});
  await open(path.join(out,'02_可编辑SVG/模块源稿',source.file));
  await page.screenshot({path:path.join(out,'01_成品与预览/逐模块预览',source.key+'.png')});
 }
 const report={...geometry,failedImages,copyErrors,copyBlocks:copy.length,modules,errors};
 await fs.writeFile(path.join(root,'work/ned-brand-showcase-render-check.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));await browser.close();
 if(failedImages.length||copyErrors.length||geometry.overflow.length||geometry.overlaps.length||geometry.cardOverflow.length||errors.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
