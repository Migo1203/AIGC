const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');const fs=require('node:fs/promises');
const root='D:/WLQ/AIGC作品集/outputs/NED_高级A+_V03_20261107';
(async()=>{
 const list=JSON.parse(await fs.readFile(root+'/04_过程记录/渲染清单.json','utf8'));
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const checks=[];
 for(const item of list){
  const [w,h]=item.size;const page=await browser.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  await page.goto(pathToFileURL(root+'/02_可编辑SVG/'+item.id+'.svg').href);await page.evaluate(()=>document.fonts.ready);
  const boxes=await page.locator('text').evaluateAll(es=>es.map(e=>{const s=getComputedStyle(e),ctx=document.createElementNS('http://www.w3.org/1999/xhtml','canvas').getContext('2d');ctx.font=`${s.fontWeight} ${s.fontSize} ${s.fontFamily}`;const m=ctx.measureText(e.textContent),anchor=e.getAttribute('text-anchor'),offset=anchor==='end'?m.width:anchor==='middle'?m.width/2:0;return{id:e.id,text:e.textContent,x:+e.getAttribute('x')-offset-m.actualBoundingBoxLeft,y:+e.getAttribute('y')-m.actualBoundingBoxAscent,w:m.actualBoundingBoxLeft+m.actualBoundingBoxRight,h:m.actualBoundingBoxAscent+m.actualBoundingBoxDescent}}));
  const overflow=boxes.filter(b=>b.x<0||b.y<0||b.x+b.w>w+.5||b.y+b.h>h+.5);
  const overlaps=[];for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(a.x+2<b.x+b.w&&b.x+2<a.x+a.w&&a.y+2<b.y+b.h&&b.y+2<a.y+a.h)overlaps.push([a.id,b.id]);}
  const imageErrors=await page.locator('image').evaluateAll(async es=>{let r=[];for(const e of es){const p=new Image();p.src=e.getAttribute('href');await p.decode().catch(()=>r.push(e.id));}return r;});
  await page.screenshot({path:root+'/01_成品与预览/图文预览/'+item.id+'.png'});
  if(item.id.endsWith('Mobile')){
   await page.setViewportSize({width:390,height:Math.ceil(h*390/w)});
   await page.evaluate(({h,w})=>{document.documentElement.setAttribute('width','390');document.documentElement.setAttribute('height',String(h*390/w));},{h,w});
   await page.screenshot({path:root+'/04_过程记录/'+item.id+'_390w.png'});
  }
  checks.push({id:item.id,size:item.size,overflow,overlaps,imageErrors,textObjects:boxes.length});await page.close();
 }
 await browser.close();await fs.writeFile(root+'/04_过程记录/SVG版式检查.json',JSON.stringify(checks,null,2));
 const failures=checks.filter(c=>c.overflow.length||c.overlaps.length||c.imageErrors.length);console.log(JSON.stringify({rendered:checks.length,failures}));if(failures.length)process.exitCode=1;
})();
