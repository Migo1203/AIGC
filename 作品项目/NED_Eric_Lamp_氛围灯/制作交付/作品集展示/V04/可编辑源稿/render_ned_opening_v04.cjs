const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const fs=require('node:fs/promises');
const root='D:/WLQ/AIGC作品集/outputs/NED_作品集开篇_V04_轻过渡与视觉情绪板_20261106';
const files=[['01_NED_Eric_封面_V04_4x3_可编辑.svg','01_NED_Eric_封面_V04_1600x1200.png'],['02_NED_Eric_背景与视觉策略_V04_4x3_可编辑.svg','02_NED_Eric_背景与视觉策略_V04_1600x1200.png']];
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});const checks=[];
 for(const [src,dst] of files){
  const page=await browser.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(root+'/可编辑源稿/'+src).href);await page.evaluate(()=>document.fonts.ready);
  const boxes=await page.locator('text').evaluateAll(es=>es.map(e=>{let b=e.getBBox();return{text:e.textContent,x:b.x,y:b.y,w:b.width,h:b.height};}));
  const overflow=boxes.filter(b=>b.x<0||b.y<0||b.x+b.w>1600||b.y+b.h>1200);const overlaps=[];
  for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){let a=boxes[i],b=boxes[j];if(a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h)overlaps.push([a.text,b.text]);}
  await page.screenshot({path:root+'/'+dst});await page.close();checks.push({file:dst,errors,overflow,overlaps,textBounds:boxes});
 }
 await browser.close();await fs.writeFile(root+'/版式检查.json',JSON.stringify(checks,null,2));console.log(JSON.stringify(checks.map(({textBounds,...c})=>c)));
 if(checks.some(c=>c.errors.length||c.overflow.length||c.overlaps.length))process.exitCode=1;
})();
