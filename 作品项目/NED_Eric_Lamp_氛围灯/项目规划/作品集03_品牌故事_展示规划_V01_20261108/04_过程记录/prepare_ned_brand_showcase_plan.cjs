const {chromium}=require('C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs/promises');const path=require('node:path');const {pathToFileURL}=require('node:url');
const root='D:/WLQ/AIGC作品集',out=path.join(root,'outputs/NED_作品集03品牌故事_展示规划_V01_20261108');
(async()=>{
 for(const dir of ['01_示意图与预览','02_可编辑SVG','03_参考素材','04_过程记录'])await fs.mkdir(path.join(out,dir),{recursive:true});
 const source=path.join(root,'work/ned-aplus-showcase-delivery-publish-20261108/作品项目/NED_Eric_Lamp_氛围灯/制作交付/亚马逊A+内容/品牌故事_V01');
 const b=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const p=await b.newPage({viewport:{width:1600,height:1200},deviceScaleFactor:2});
 await p.goto(pathToFileURL(path.join(source,'排版预览/品牌故事图文预览.html')).href);
 const logo='data:image/png;base64,'+(await fs.readFile(path.join(root,'outputs/NED_Logo_原样重绘_20261105/NED_原样重绘_黑_原画布_4000w.png'))).toString('base64');
 await p.locator('.about-logo').evaluateAll((es,src)=>es.forEach(e=>e.src=src),logo);
 await p.evaluate(()=>Promise.all([...document.images].map(im=>im.decode())));
 await p.locator('#desktop').screenshot({path:path.join(out,'03_参考素材/桌面整体_规划参考.png')});
 const records=[];
 for(let i=0;i<4;i++){
  const loc=p.locator('.mobile-stage').nth(i);
  await loc.screenshot({path:path.join(out,`03_参考素材/手机状态0${i+1}_规划参考.png`)});
  records.push({state:i+1,text:await loc.innerText()});
 }
 await fs.copyFile(path.join(source,'图片素材/B00_电脑背景.jpg'),path.join(out,'03_参考素材/B00_电脑背景.jpg'));
 await fs.writeFile(path.join(out,'04_过程记录/参考渲染记录.json'),JSON.stringify({source:'品牌故事_V01/排版预览/品牌故事图文预览.html',deviceScaleFactor:2,change:'仅在内存中将旧低清Logo替换为项目已有原样轮廓重绘PNG，原HTML未改；照片和英文不改',states:records},null,2));
 await b.close();console.log('Prepared desktop and all 4 mobile states for planning.');
})().catch(e=>{console.error(e);process.exit(1)});
