from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageCms, ImageEnhance, ImageOps
import base64, html, json, shutil, io, zipfile, subprocess
import numpy as np

ROOT=Path('D:/WLQ/AIGC作品集');SRC=ROOT/'work/ned-banner-assets'
OUT=ROOT/'outputs/NED_Banner_V02_20261105';LOGO=ROOT/'outputs/NED_Logo_原样重绘_20261105'
ASSETS=OUT/'图片素材';PRE=OUT/'图文预览';EDIT=OUT/'可编辑源稿'
for p in [ASSETS,PRE,EDIT,EDIT/'品牌Logo',EDIT/'制作脚本']:p.mkdir(parents=True,exist_ok=True)
FONT=SRC/'DMSans-VF.ttf';BONE=(244,241,235);INK=(30,32,30);ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes();MAN=[]
def fnt(size,weight=500):
    f=ImageFont.truetype(str(FONT),size)
    f.set_variation_by_axes([weight if a['name'].decode().lower()=='weight' else 14 for a in f.get_variation_axes()]);return f
def text(im,t,x,y,size,weight=500,color=INK):ImageDraw.Draw(im).text((x,y),t,font=fnt(size,weight),fill=color,anchor='lt')
def save(im,folder,name,role,source):
    p=folder/name
    if p.suffix=='.jpg':im.convert('RGB').save(p,quality=95,subsampling=0,optimize=True,icc_profile=ICC)
    else:im.save(p,icc_profile=ICC)
    MAN.append({'file':str(p.relative_to(OUT)).replace('\\','/'),'width':im.width,'height':im.height,'bytes':p.stat().st_size,'role':role,'source':source});return p
def crop(name,box,size):return Image.open(SRC/name).convert('RGB').crop(box).resize(size,Image.Resampling.LANCZOS)
def logo(im,x,y,w,color='黑'):
    mark=Image.open(LOGO/f'NED_原样重绘_{color}_紧边_4000w.png').convert('RGBA');mark=mark.resize((w,round(w*mark.height/mark.width)),Image.Resampling.LANCZOS);im.paste(mark,(x,y),mark)
def arrow(im,x,y,length=115,color=INK,width=4):
    d=ImageDraw.Draw(im);d.line((x,y,x+length,y),fill=color,width=width);d.line((x+length-15,y-13,x+length,y,x+length-15,y+13),fill=color,width=width)

# Full photograph to the edges. Only existing wall texture and a narrow outer
# furniture-edge strip are extended; the product and scene proportions stay fixed.
original=Image.open(SRC/'P01_PC.png').convert('RGB')
scaled=original.resize((2100,861),Image.Resampling.LANCZOS)
scene=scaled.crop((0,135,2100,735))
hero_base=Image.new('RGB',(3000,600))
left=ImageOps.mirror(scene.crop((0,0,420,600))).resize((820,600),Image.Resampling.BICUBIC)
hero_base.paste(left,(0,0));hero_base.paste(scene,(820,0))
hero_base.paste(ImageOps.mirror(scene.crop((2020,0,2100,600))),(2920,0))
hero=hero_base.copy()
hero_lines=[('Eric Table Lamp',525,115,43,500),('Meet Eric.',515,202,152,500),('Cordless light. Everyday warmth.',525,405,48,400)]
for args in hero_lines:text(hero,*args)
save(hero,ASSETS,'BN01_页头_3000x600.jpg','页头Hero；Logo为独立组件','P01_PC.png; wall texture continuation only')
save(hero_base,EDIT,'BN01_无字底图.png','带墙面补景的无字背景','P01_PC.png')
save(hero,PRE,'BN01_页头_电脑预览.png','Hero本体','P01_PC.png')
save(hero.crop((450,0,2550,600)),PRE,'BN01_中央70百分比裁切检查.png','关键文字与完整灯体裁切检查','BN01')
store=Image.new('RGB',(3000,790),BONE);logo(store,150,35,150);text(store,'Eric Table Lamp',390,65,40,500);store.paste(hero,(0,190))
save(store,PRE,'BN01_品牌组件与页头示意.png','重绘Logo独立配置；品牌栏示意','BN01 + redrawn logo')

# Scene remains visible beneath the native text: no white information panel.
dining=crop('P05_Dining_PC.png',(190,0,1796,803),(3000,1500))
dining_proof=dining.copy()
dining_lines=[('Eric Table Lamp',190,190,43,500),('Set the table.',180,293,126,500),('Keep the glow.',180,440,126,500),('Bring cordless light to the table.',190,642,49,400),('Explore Eric',190,782,52,500)]
for args in dining_lines:text(dining_proof,*args)
ImageDraw.Draw(dining_proof).line((190,854,474,854),fill=INK,width=3);arrow(dining_proof,535,810,85)
save(dining,ASSETS,'BN02_导流_电脑_3000x1500.jpg','完整场景无字素材，标题使用原生字段','P05_Dining_PC.png crop 1606x803, 1.87x interpolation')
save(dining_proof,PRE,'BN02_场景导流_图文预览.png','原生字段排版示意，不是上传图片','P05_Dining_PC.png')
mobile=crop('P05_Dining_Mobile.png',(181,0,1267,1086),(1680,1680))
save(mobile,ASSETS,'BN02_导流_手机备选_1680x1680.jpg','手机备选场景，模块支持以后台为准','P05_Dining_Mobile.png; V01 crop retained')
mob=Image.new('RGB',(840,1110),BONE);mob.paste(mobile.resize((840,840)),(0,0))
text(mob,'Set the table. Keep the glow.',38,879,46,500);text(mob,'Bring cordless light to the table.',40,952,29,400);text(mob,'Explore Eric',40,1025,30,500);arrow(mob,234,1041,55,width=2)
save(mob,PRE,'BN02_手机图文适配示意.png','手机图文相邻布局示意','BN02 mobile')

# REC custom images contain no logo, type or artificial CTA. A separate preview
# carries brand and headline fields.
ad=crop('A03_night.png',(820,0,2163,703),(1200,628))
square=crop('P04_Mobile.png',(181,0,1267,1086),(1200,1200))
portrait=crop('P04_Mobile.png',(415,0,1026,1086),(900,1600))
for im,name,source in [(ad,'BN03_REC_横_1200x628.jpg','A03_night.png; wider bedside context reframed'),(square,'BN03_REC_方_1200x1200.jpg','P04_Mobile.png; V01 composition retained'),(portrait,'BN03_REC_竖_900x1600.jpg','P04_Mobile.png; V01 composition retained')]:save(im,ASSETS,name,'REC无字图片',source)
headline='Evening light, without the cord.'
adproof=Image.new('RGB',(1200,830),BONE);adproof.paste(ad,(0,0));logo(adproof,40,657,104);text(adproof,'Eric Table Lamp',185,674,26,500);text(adproof,headline,40,737,47,500)
save(adproof,PRE,'BN03_REC_广告图文预览.png','品牌、标题组件示意；上传用无字图片','BN03 + redrawn logo')

# Platform preparation files use the same redrawn outlines with neutral margins.
brand=Image.new('RGBA',(1200,1200),(0,0,0,0));logo(brand,240,396,720)
save(brand,EDIT/'品牌Logo','NED_Stores_1200x1200.png','Logo独立组件试排文件，未后台验证','redrawn existing logo')
rec=Image.new('RGBA',(1200,400),(0,0,0,0));logo(rec,300,30,600)
save(rec,EDIT/'品牌Logo','NED_REC_1200x400.png','Logo独立组件试排文件，未后台验证','redrawn existing logo')
for p in LOGO.glob('NED_*.svg'):shutil.copy2(p,EDIT/'品牌Logo'/p.name)

# Native vector text and embedded raster photos; no substitute SVG photography.
font64=base64.b64encode(FONT.read_bytes()).decode()
def svg(name,photo,lines,size,mark=False):
    bio=io.BytesIO();photo.save(bio,format='PNG');b64=base64.b64encode(bio.getvalue()).decode()
    w,h=size
    pieces=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<style>@font-face{{font-family:dm;src:url(data:font/ttf;base64,{font64})}}text{{font-family:dm,"DM Sans",sans-serif}}</style>',f'<rect width="{w}" height="{h}" fill="#f4f1eb"/>',f'<image id="scene" width="{photo.width}" height="{photo.height}" href="data:image/png;base64,{b64}"/>']
    if mark:
        raw=(LOGO/'NED_原样重绘_黑_紧边.svg').read_bytes();pieces.append(f'<image id="existing-logo-redraw" x="40" y="657" width="104" height="59" href="data:image/svg+xml;base64,{base64.b64encode(raw).decode()}"/>')
    for t,x,y,size_,weight in lines:pieces.append(f'<text x="{x}" y="{y+size_*.82}" font-size="{size_}" font-weight="{weight}" fill="#1e201e">{html.escape(t)}</text>')
    if name.startswith('BN02'):
        pieces.append('<path d="M190 854H474 M535 810H620 M605 797L620 810L605 823" fill="none" stroke="#1e201e" stroke-width="3"/>')
    pieces.append('</svg>');(EDIT/(name+'.svg')).write_text('\n'.join(pieces),encoding='utf-8')
svg('BN01_页头_可编辑',hero_base,hero_lines,(3000,600))
svg('BN02_导流_可编辑',dining,dining_lines,(3000,1500))
svg('BN03_REC_组件示意_可编辑',ad,[('Eric Table Lamp',185,674,26,500),(headline,40,737,47,500)],(1200,830),True)
shutil.copy2(FONT,EDIT/FONT.name);shutil.copy2(SRC/'DM-Sans-OFL.txt',EDIT/'DM-Sans-OFL.txt')

# A compact presentation board avoids the V01's large external commentary columns.
board=Image.new('RGB',(1800,2770),'#ebe7e0')
logo(board,80,38,105);text(board,'Eric / Banner V02',225,65,40,500)
text(board,'01  Store header',80,150,24,500)
board.paste(hero.resize((1640,328),Image.Resampling.LANCZOS),(80,197))
text(board,'02  In-store discovery',80,580,24,500)
board.paste(dining_proof.resize((1640,820),Image.Resampling.LANCZOS),(80,625))
text(board,'03  REC advertising',80,1500,24,500)
board.paste(adproof.resize((1640,1134),Image.Resampling.LANCZOS),(80,1545))
text(board,'Portfolio preview / Image, logo and headline supplied separately.',80,2710,22,400)
save(board,OUT,'三款Banner_V02总览.jpg','三款主视觉紧凑审阅总览','V02')

# V01 vs V02 compare at the same display width and aspect ratio.
compare=Image.new('RGB',(2400,1830),'#ebe7e0');text(compare,'V01',50,35,40);text(compare,'V02',1230,35,40)
v01=ROOT/'outputs/NED_Banner_V01_20261105/图文预览'
for y,p1,p2,size in [(120,'BN01_页头_电脑预览.png',hero,(1120,224)),(440,'BN02_场景导流_图文预览.png',dining_proof,(1120,560)),(1100,'BN03_REC_广告图文预览.png',adproof,(960,680))]:
    old=Image.open(v01/p1).convert('RGB');compare.paste(ImageOps.contain(old,size,Image.Resampling.LANCZOS),(50,y));compare.paste(ImageOps.contain(p2,size,Image.Resampling.LANCZOS),(1230,y))
save(compare,OUT,'V01与V02同尺寸对照.jpg','同显示尺寸比较，含广告组件','V01 + V02')

copydata={'version':'V02','BN01':{'product':'Eric Table Lamp','heading':'Meet Eric.','body':'Cordless light. Everyday warmth.'},'BN02':{'prefix':'Eric Table Lamp','heading':'Set the table. Keep the glow.','body':'Bring cordless light to the table.','link_text':'Explore Eric','destination':None},'BN03':{'headline':headline,'headline_characters':len(headline),'destination':None},'brand_logo':'Existing NED ned. wordmark, contour redraw from user-supplied white PNG','method':'Existing AI scene reuse and deterministic photographic compositing; no image generation API used','status':'Awaiting review; not Amazon-approved; no performance claims'}
(EDIT/'文案与制作设置.json').write_text(json.dumps(copydata,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'文件与规格清单.json').write_text(json.dumps(MAN,ensure_ascii=False,indent=2),encoding='utf-8')

page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NED Eric｜Banner V02</title><style>@font-face{font-family:dm;src:url('可编辑源稿/DMSans-VF.ttf')}*{box-sizing:border-box}body{margin:0;background:#ebe7e0;color:#1e201e;font-family:dm,Arial,sans-serif}main{max-width:1500px;margin:auto;padding:36px 26px}h1{font-size:34px;font-weight:500}h2{font-size:20px;font-weight:500}p{line-height:1.7;color:#67645f}section{margin:32px 0}img{display:block;width:100%;height:auto}summary{cursor:pointer;padding:14px 0}a{color:inherit}.brand{width:90px;height:auto}.ad{max-width:1000px}</style><main><img class="brand" src="可编辑源稿/品牌Logo/NED_原样重绘_黑_紧边.svg"><h1>Eric / Banner V02</h1><p>品牌氛围与商业表达：真实场景铺陈、清晰产品、紧凑信息。V02 待审阅。</p><section><h2>01 / 店铺页头</h2><img src="图文预览/BN01_品牌组件与页头示意.png"><details><summary>页头中央 70% 裁切检查</summary><img src="图文预览/BN01_中央70百分比裁切检查.png"></details></section><section><h2>02 / 店内餐桌场景导流</h2><img src="图文预览/BN02_场景导流_图文预览.png"><details><summary>手机图文适配示意</summary><img style="max-width:420px" src="图文预览/BN02_手机图文适配示意.png"></details></section><section class="ad"><h2>03 / REC 广告图文组件示意</h2><img src="图文预览/BN03_REC_广告图文预览.png"><p>图片、Logo 与标题独立提供。预览不代表真实平台界面或已实际投放。</p><details><summary>方版与竖版素材</summary><img style="max-width:420px" src="图片素材/BN03_REC_方_1200x1200.jpg"><img style="max-width:360px;margin-top:20px" src="图片素材/BN03_REC_竖_900x1600.jpg"></details></section><details><summary>V01 / V02 同尺寸对照</summary><img src="V01与V02同尺寸对照.jpg"></details><p>源稿文字可编辑，场景为嵌入位图。实际上传与原生文字排版需在编辑器核对，链接目的地址尚未配置。详见 README.md。</p></main></html>'''
(OUT/'打开查看三款Banner_V02.html').write_text(page,encoding='utf-8')
print(json.dumps({'output':str(OUT),'image_assets':len(list(ASSETS.glob('*.jpg'))),'headline_characters':len(headline)},ensure_ascii=False))
