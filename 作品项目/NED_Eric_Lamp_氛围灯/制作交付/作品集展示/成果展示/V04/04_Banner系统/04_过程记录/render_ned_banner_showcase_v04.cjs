const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs/promises'),path=require('node:path');
const root='D:/WLQ/AIGC作品集';
(async()=>{
 const build=JSON.parse(await fs.readFile(path.join(root,'work/ned-banner-showcase-build.json'),'utf8')),out=build.output;
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 async function open(file){
  const svg=await fs.readFile(file,'utf8');await page.setContent('<html><head><meta charset="utf-8"><style>html,body{margin:0}body>svg{display:block}</style></head><body>'+svg+'</body></html>');
  await page.evaluate(()=>document.fonts.ready);
  return await page.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(null);im.onerror=()=>resolve(e.id||'image');im.src=e.getAttribute('href')})))).then(a=>a.filter(Boolean));
 }
 async function geometry(w,h){return await page.evaluate(({w,h})=>{
  const ctx=document.createElement('canvas').getContext('2d');
  const glyphs=[...document.querySelectorAll('text')].map(e=>{
   const s=getComputedStyle(e),size=parseFloat(s.fontSize);ctx.font=`${s.fontWeight} ${size}px ${s.fontFamily}`;
   const z=ctx.measureText(e.textContent),m=e.getScreenCTM(),x=parseFloat(e.getAttribute('x')),y=parseFloat(e.getAttribute('y'));
   const a=new DOMPoint(x-z.actualBoundingBoxLeft,y-z.actualBoundingBoxAscent).matrixTransform(m),b=new DOMPoint(x+z.actualBoundingBoxRight,y+z.actualBoundingBoxDescent).matrixTransform(m);
   return {id:e.id,text:e.textContent,x:a.x,y:a.y,w:b.x-a.x,h:b.y-a.y};
  });
  const overflow=glyphs.filter(e=>e.x<-.1||e.y<-.1||e.x+e.w>w+.1||e.y+e.h>h+.1),overlaps=[];
  for(let i=0;i<glyphs.length;i++)for(let j=i+1;j<glyphs.length;j++){const a=glyphs[i],b=glyphs[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>.5&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>.5)overlaps.push([a.id,b.id]);}
  return {textCount:glyphs.length,overflow,overlaps};
 },{w,h})}
 const failedImages=await open(path.join(out,'02_可编辑SVG/04_Banner系统展示_V04_可编辑.svg'));
 const geom=await geometry(1600,6600);
 const copyErrors=await page.locator('[data-copy]').evaluateAll(es=>es.map(e=>({key:e.dataset.copy,text:e.textContent}))).then(a=>a.filter(e=>build.copy[e.key]!==e.text));
 const placements=await page.locator('body>svg>svg[data-module]').evaluateAll(es=>es.map(e=>{const v=e.viewBox.baseVal,m=e.getScreenCTM(),a=new DOMPoint(v.x,v.y).matrixTransform(m),b=new DOMPoint(v.x+v.width,v.y+v.height).matrixTransform(m);return {key:e.dataset.module,x:a.x,y:a.y,w:b.x-a.x,h:b.y-a.y}}));
 if(placements.length!==7)throw Error('Seven showcase frames required');
 for(let i=0;i<placements.length;i++)for(const k of ['x','y','w','h'])if(Math.abs(placements[i][k]-build.placements[i][k])>.02)throw Error('Placement mismatch '+JSON.stringify({got:placements[i],expected:build.placements[i]}));
 await page.screenshot({path:path.join(out,'01_成品与预览/04_Banner系统展示_V04_1600x6600.png'),fullPage:true});
 const moduleChecks=[];
 for(const s of build.sources){
  await page.setViewportSize({width:s.width,height:s.height});const failed=await open(path.join(out,'02_可编辑SVG/模块源稿',s.file));const g=await geometry(s.width,s.height);
  moduleChecks.push({key:s.key,...g,failedImages:failed});
  await page.screenshot({path:path.join(out,'01_成品与预览/逐模块预览',s.key+'.png')});
  if(s.key==='BN02_电脑场景导流'){
   await page.addStyleTag({content:'text,path{visibility:hidden}'});
   await page.screenshot({path:path.join(root,'work/ned-banner-dining-contrast-background.png')});
   await page.addStyleTag({content:'body{background:white}svg image,svg rect,svg path{visibility:hidden}svg text{visibility:visible;fill:black}'});
   await page.screenshot({path:path.join(root,'work/ned-banner-dining-contrast-mask.png')});
  }
 }
 const report={...geom,failedImages,copyErrors,placements,moduleChecks,errors};
 await fs.writeFile(path.join(root,'work/ned-banner-showcase-render-check.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));await browser.close();
 if(failedImages.length||copyErrors.length||geom.overflow.length||geom.overlaps.length||errors.length||moduleChecks.some(m=>m.failedImages.length||m.overflow.length||m.overlaps.length))process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
