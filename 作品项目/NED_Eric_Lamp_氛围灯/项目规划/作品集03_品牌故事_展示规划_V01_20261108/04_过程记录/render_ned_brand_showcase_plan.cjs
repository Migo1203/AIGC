const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs/promises'),path=require('node:path');
const base='D:/WLQ/AIGC作品集/outputs/NED_作品集03品牌故事_展示规划_V01_20261108';
(async()=>{
 const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const p=await b.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:1});
 const svg=await fs.readFile(path.join(base,'02_可编辑SVG/03_品牌故事_展示规划示意_V01.svg'),'utf8');
 await p.setContent('<html><head><meta charset="utf-8"><style>body{margin:0}svg{display:block}</style></head><body>'+svg+'</body></html>');
 await p.evaluate(()=>document.fonts.ready);
 const images=await p.locator('image').evaluateAll(es=>Promise.all(es.map(e=>new Promise(resolve=>{const i=new Image();i.onload=()=>resolve(true);i.onerror=()=>resolve(false);i.src=e.getAttribute('href')}))));
 const texts=await p.locator('text').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return {text:e.textContent,x:r.x,y:r.y,w:r.width,h:r.height}}));
 const overflow=texts.filter(r=>r.x<0||r.y<0||r.x+r.w>1600||r.y+r.h>7160);
 await p.screenshot({path:path.join(base,'01_示意图与预览/03_品牌故事_展示规划示意_V01_1600x7160.png'),fullPage:true});
 const report={images:images.length,failedImages:images.filter(x=>!x).length,texts:texts.length,overflow};
 await fs.writeFile(path.join(base,'04_过程记录/渲染检查.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));await b.close();if(report.failedImages||overflow.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});
