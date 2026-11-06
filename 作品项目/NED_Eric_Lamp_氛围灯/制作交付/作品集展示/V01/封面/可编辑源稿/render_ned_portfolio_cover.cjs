const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('node:url');
const fs=require('node:fs/promises');
const root='D:/WLQ/AIGC作品集/outputs/NED_作品集封面_V01_20261105';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(pathToFileURL(root+'/可编辑源稿/NED_Eric_项目封面_V01_可编辑.svg').href);
 await page.evaluate(()=>document.fonts.ready);
 const textBounds=await page.locator('text').evaluateAll(es=>es.map(e=>{const b=e.getBBox();return{text:e.textContent,x:b.x,y:b.y,width:b.width,height:b.height};}));
 const overflow=textBounds.filter(b=>b.x<0||b.y<0||b.x+b.width>1600||b.y+b.height>900);
 await page.screenshot({path:root+'/NED_Eric_项目封面_V01_1600x900.png'});
 await browser.close();
 await fs.writeFile(root+'/版式检查.json',JSON.stringify({errors,overflow,textBounds},null,2));
 console.log(JSON.stringify({errors,overflow,textBounds}));
 if(errors.length||overflow.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
