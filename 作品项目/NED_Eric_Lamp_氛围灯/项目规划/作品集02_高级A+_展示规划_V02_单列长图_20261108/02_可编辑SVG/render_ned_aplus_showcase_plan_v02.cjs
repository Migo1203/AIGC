const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const fs=require('node:fs/promises');
const path=require('node:path');
const out='D:/WLQ/AIGC作品集/outputs/NED_作品集02高级A+_展示规划_V02_单列长图_20261108';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const reports=[];
 for(const [name,height] of [['02_高级A+_纵向阅读结构_V02',2260],['02_高级A+_单列长图规划示意_V02',11060]]){
  const page=await browser.newPage({viewport:{width:1600,height},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(out,'02_可编辑SVG',name+'.svg')).href);
  await page.evaluate(()=>document.fonts.ready);
  const decode=await page.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{
   const im=new Image();im.onload=()=>resolve({id:e.id,ok:true});im.onerror=()=>resolve({id:e.id,ok:false});im.src=e.getAttribute('href');
  }))));
  const boxes=await page.locator('text').evaluateAll(es=>es.map(e=>{const b=e.getBBox();return {text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};}));
  const overflow=boxes.filter(b=>b.x<0||b.y<0||b.x+b.w>1600||b.y+b.h>height);
  const overlaps=[];
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
   const a=boxes[i],b=boxes[j];if(a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h)overlaps.push([a.text,b.text]);
  }
  await page.screenshot({path:path.join(out,'01_示意图与预览',name+'.png')});
  reports.push({name,size:[1600,height],images:decode.length,failed:decode.filter(i=>!i.ok),overflow,overlaps,errors});
  await page.close();
 }
 await browser.close();
 await fs.writeFile('D:/WLQ/AIGC作品集/work/ned-aplus-showcase-plan-v02-render-check.json',JSON.stringify(reports,null,2));
 console.log(JSON.stringify(reports));
 if(reports.some(r=>r.failed.length||r.overflow.length||r.overlaps.length||r.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
