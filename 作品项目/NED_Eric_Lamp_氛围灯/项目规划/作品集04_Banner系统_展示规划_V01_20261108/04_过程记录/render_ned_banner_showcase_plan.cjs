const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs/promises'),path=require('node:path');
const base='D:/WLQ/AIGC作品集/outputs/NED_作品集04Banner系统_展示规划_V01_20261108';
(async()=>{
 const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const p=await b.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:1});
 await p.setContent('<html><head><meta charset="utf-8"><style>body{margin:0}svg{display:block}</style></head><body>'+await fs.readFile(path.join(base,'02_可编辑SVG/04_Banner系统_展示规划示意_V01.svg'),'utf8')+'</body></html>');await p.evaluate(()=>document.fonts.ready);
 const images=await p.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{const im=new Image();im.onload=()=>resolve(true);im.onerror=()=>resolve(false);im.src=e.getAttribute('href')}))));
 const geometry=await p.evaluate(()=>{
  const c=document.createElement('canvas').getContext('2d'),glyphs=[...document.querySelectorAll('text')].map(e=>{const s=getComputedStyle(e);c.font=`${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;const m=c.measureText(e.textContent),x=+e.getAttribute('x'),y=+e.getAttribute('y');return {text:e.textContent,x:x-m.actualBoundingBoxLeft,y:y-m.actualBoundingBoxAscent,w:m.actualBoundingBoxLeft+m.actualBoundingBoxRight,h:m.actualBoundingBoxAscent+m.actualBoundingBoxDescent}});
  const overflow=glyphs.filter(r=>r.x<0||r.y<0||r.x+r.w>1600||r.y+r.h>7040),overlaps=[];
  for(let i=0;i<glyphs.length;i++)for(let j=i+1;j<glyphs.length;j++){const a=glyphs[i],b=glyphs[j];if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)+.5&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y)+.5)overlaps.push([a.text,b.text]);}
  return {textObjects:glyphs.length,overflow,overlaps};
 });
 await p.screenshot({path:path.join(base,'01_示意图与预览/04_Banner系统_展示规划示意_V01_1600x7040.png'),fullPage:true});
 await p.setViewportSize({width:1200,height:1420});await p.setContent('<html><head><meta charset="utf-8"><style>body{margin:0}svg{display:block}</style></head><body>'+await fs.readFile(path.join(base,'02_可编辑SVG/04_Banner系统_阅读结构_V01.svg'),'utf8')+'</body></html>');await p.evaluate(()=>document.fonts.ready);
 await p.screenshot({path:path.join(base,'01_示意图与预览/04_Banner系统_阅读结构_V01.png')});
 const report={...geometry,images:images.length,failedImages:images.filter(e=>!e).length};await fs.writeFile(path.join(base,'04_过程记录/渲染检查.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));await b.close();if(report.failedImages||geometry.overflow.length||geometry.overlaps.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
