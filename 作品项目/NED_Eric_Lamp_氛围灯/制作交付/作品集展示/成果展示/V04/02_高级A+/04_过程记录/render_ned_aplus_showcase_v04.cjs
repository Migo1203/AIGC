const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const fs=require('node:fs/promises');
const path=require('node:path');
const base='D:/WLQ/AIGC作品集';
(async()=>{
 const build=JSON.parse(await fs.readFile(path.join(base,'work/ned-aplus-showcase-v04-build.json'),'utf8'));
 const out=build.output;
 const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const p=await b.newPage({viewport:{width:1600,height:build.size[1]},deviceScaleFactor:1});
 const errors=[];p.on('pageerror',e=>errors.push(e.message));
 await p.goto(pathToFileURL(path.join(out,'02_可编辑SVG/02_高级A+展示_V04_可编辑.svg')).href);
 await p.evaluate(()=>document.fonts.ready);
 const decoded=await p.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{
  const im=new Image();im.onload=()=>resolve({id:e.id,ok:true});im.onerror=()=>resolve({id:e.id,ok:false});im.src=e.getAttribute('href');
 }))));
 const boxes=await p.locator('text').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return {id:e.id,text:e.textContent,x:r.x,y:r.y,w:r.width,h:r.height};}));
 const overflow=boxes.filter(r=>r.x<-.1||r.y<-.1||r.x+r.w>1600.1||r.y+r.h>build.size[1]+.1);
 const fontBoxOverlaps=[];
 for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
  const a=boxes[i],c=boxes[j];if(a.x<c.x+c.w&&c.x<a.x+a.w&&a.y<c.y+c.h&&c.y<a.y+a.h)fontBoxOverlaps.push([a.id,c.id]);
 }
 const glyphs=await p.locator('text').evaluateAll(es=>{
  const ctx=document.createElementNS('http://www.w3.org/1999/xhtml','canvas').getContext('2d');
  return es.map(e=>{
   const style=getComputedStyle(e);ctx.font=`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
   ctx.textAlign=style.textAnchor==='end'?'right':style.textAnchor==='middle'?'center':'left';
   const m=ctx.measureText(e.textContent),x=Number(e.getAttribute('x')),y=Number(e.getAttribute('y'));
   const matrix=e.getScreenCTM();
   const a=new DOMPoint(x-m.actualBoundingBoxLeft,y-m.actualBoundingBoxAscent).matrixTransform(matrix);
   const b=new DOMPoint(x+m.actualBoundingBoxRight,y+m.actualBoundingBoxDescent).matrixTransform(matrix);
   return {id:e.id,text:e.textContent,x:a.x,y:a.y,w:b.x-a.x,h:b.y-a.y};
  });
 });
 const overlaps=[];
 for(let i=0;i<glyphs.length;i++)for(let j=i+1;j<glyphs.length;j++){
  const a=glyphs[i],c=glyphs[j];if(a.x<c.x+c.w&&c.x<a.x+a.w&&a.y<c.y+c.h&&c.y<a.y+a.h)overlaps.push([a.id,c.id,a.text,c.text]);
 }
 const clipped=await p.locator('svg svg text').evaluateAll(es=>es.flatMap(e=>{
  const r=e.getBBox(),v=e.ownerSVGElement.viewBox.baseVal;
  return r.x<-.2||r.y<-.2||r.x+r.width>v.width+.2||r.y+r.height>v.height+.2?[{id:e.id,text:e.textContent,rect:[r.x,r.y,r.width,r.height],viewBox:[v.width,v.height]}]:[];
 }));
 const modules=await p.locator('[data-module]').evaluateAll(es=>es.map(e=>{
  const r=e.querySelector('svg').getBoundingClientRect();return {key:e.dataset.module,x:r.x,y:r.y,w:r.width,h:r.height,texts:e.querySelectorAll('text').length};
 }));
 await p.screenshot({path:path.join(out,'01_成品与预览',build.name+'.png')});
 const report={size:build.size,images:decoded.length,failedImages:decoded.filter(e=>!e.ok),textCount:boxes.length,overflow,overlaps,fontBoxOverlapCount:fontBoxOverlaps.length,clipped,modules,errors};
 await fs.writeFile(path.join(base,'work/ned-aplus-showcase-v04-render-check.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({...report,modules:modules.length}));
 await b.close();
 if(report.failedImages.length||overflow.length||overlaps.length||clipped.length||errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1);});
