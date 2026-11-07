from pathlib import Path
from PIL import Image, ImageChops
from html import escape
import xml.etree.ElementTree as ET
import base64, hashlib, json, shutil, re, copy

R=Path('D:/WLQ/AIGC作品集')
O=R/'outputs/NED_作品集04_Banner系统_展示_V04_20261108'
P=O/'01_成品与预览'; E=O/'02_可编辑SVG'; A=O/'03_原始素材'; L=O/'04_过程记录'
for d in [P,P/'逐模块预览',E,E/'模块源稿',A,A/'图片素材',A/'原始SVG',A/'排版底图',L]:d.mkdir(parents=True,exist_ok=True)
S=R/'outputs/NED_Banner_V02_20261105'; F=S/'可编辑源稿/DMSans-VF.ttf'
PLAN=R/'outputs/NED_作品集04Banner系统_展示规划_V01_20261108'
NS='http://www.w3.org/2000/svg'; Q='{'+NS+'}'; ET.register_namespace('',NS)
for n in ['DMSans-VF.ttf','DM-Sans-OFL.txt']:shutil.copy2(F.parent/n,E/n)
assets=[]
for f in sorted((S/'图片素材').glob('*.jpg')):
 shutil.copy2(f,A/'图片素材'/f.name)
 assets.append(dict(file=f.name,size=list(Image.open(f).size),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
assert len(assets)==6
logo=S/'可编辑源稿/品牌Logo/NED_原样重绘_黑_紧边.svg'
shutil.copy2(logo,A/logo.name)
raws={}; extracted={}
for key,name in [('hero','BN01_页头_可编辑'),('dining','BN02_导流_可编辑'),('rec','BN03_REC_组件示意_可编辑')]:
 f=S/'可编辑源稿'/(name+'.svg');shutil.copy2(f,A/'原始SVG'/f.name)
 root=ET.parse(f).getroot();raws[key]=root
 photo=root.find(Q+'image');h=photo.attrib['href'];b=base64.b64decode(h.split(',',1)[1])
 path=A/'排版底图'/({'hero':'BN01_无字底图.png','dining':'BN02_电脑无字_源SVG提取.png','rec':'BN03_横版无字_源SVG提取.png'}[key]);path.write_bytes(b);extracted[key]=path

bg=Image.open(PLAN/'03_参考素材/连续暖墙_Banner系统规划.png').convert('RGB').crop((0,0,1600,6600))
bg.save(A/'连续暖墙_Banner系统展示.png')
prev=Image.open(R/'outputs/NED_作品集03_品牌故事_展示_V04_20261108/03_原始素材/连续暖墙_品牌故事展示.png').convert('RGB')
assert ImageChops.difference(bg.crop((0,0,1600,1)),prev.crop((0,6599,1600,6600))).getbbox() is None
data=lambda p,m:'data:'+m+';base64,'+base64.b64encode(p.read_bytes()).decode()
fontdata=data(F,'font/ttf'); counter=0; placements=[]; modules=[];copies={}
INK='#1e201e'; BONE='#f4f1eb'
def header(w,h,title):
 return f'<svg xmlns="{NS}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{escape(title)}</title><desc>作品集展示审阅稿。文字为独立对象、Logo为路径；照片为位图。非真实后台截图。</desc><defs><style>@font-face{{font-family:DM;src:url({fontdata})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style></defs>'

class Canvas:
 def __init__(self,key,w,h):self.key=key;self.w=w;self.h=h;self.parts=[];self.copykeys=[]
 def rect(self,x,y,w,h,fill,attrs=''):self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {attrs}/>')
 def image(self,p,x,y,w,h):
  iw,ih=Image.open(p).size;assert abs(w/h-iw/ih)<.001,(p,w,h,iw,ih)
  self.parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/jpeg" if p.suffix==".jpg" else "image/png")}" preserveAspectRatio="xMidYMid meet"/>')
 def text(self,s,x,y,size=24,weight=400,color='#403a32',key=None):
  global counter
  counter+=1
  self.parts.append(f'<text id="text-{counter}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}"'+(f' data-copy="{key}"' if key else '')+'>'+escape(s)+'</text>')
  if key:copies[key]=s;self.copykeys.append(key)
 def logo(self,x,y,w):
  root=ET.parse(logo).getroot();vb=list(map(float,root.attrib['viewBox'].split()))
  root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(w*vb[3]/vb[2]));root.set('data-logo','existing-wordmark-trace')
  self.parts.append(ET.tostring(root,encoding='unicode'))
 def path(self,d,color=INK,width=3):self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"/>')
 def finish(self):return header(self.w,self.h,self.key)+''.join(self.parts)+'</svg>'

def reused_text(c,source,prefix,color=None):
 for i,t in enumerate(raws[source].findall(Q+'text')):
  a=t.attrib;c.text(t.text,float(a['x']),float(a['y']),float(a['font-size']),int(a['font-weight']),color or a['fill'],prefix+'-'+str(i+1))

def nest(c,child,x,y,w,h=None,viewbox=None):
 root=ET.fromstring(child.finish());prefix=c.key+'-'+child.key+'-'+str(len(c.parts))+'-'
 for el in root.iter():
  if 'id' in el.attrib:el.set('id',prefix+el.attrib['id'])
  for k,v in list(el.attrib.items()):
   if 'url(#' in v:el.set(k,re.sub(r'url\(#([^)]+)\)',lambda m:'url(#'+prefix+m[1]+')',v))
 for parent in root.iter():
  for e in list(parent):
   if e.tag==Q+'style':parent.remove(e)
 root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h if h is not None else w*child.h/child.w))
 root.set('overflow','hidden')
 if viewbox:root.set('viewBox',viewbox)
 root.set('data-module',child.key)
 c.parts.append(ET.tostring(root,encoding='unicode'));c.copykeys+=child.copykeys

hero=Canvas('BN01_Hero',3000,600);hero.image(extracted['hero'],0,0,3000,600);reused_text(hero,'hero','hero')
c=Canvas('BN01_品牌栏与页头',3000,790);c.rect(0,0,3000,790,BONE);c.logo(150,35,150);c.text('Eric Table Lamp',390,97.8,40,500,INK,'brand-product');nest(c,hero,0,190,3000);modules.append(c)
c=Canvas('BN01_中央70百分比裁切检查',2100,600);nest(c,hero,0,0,2100,600,'450 0 2100 600');modules.append(c)
c=Canvas('BN02_电脑场景导流',3000,1500);c.image(extracted['dining'],0,0,3000,1500)
# Independent, non-destructive warm charcoal gradient: the lamp begins farther right.
c.parts.append('<defs><linearGradient id="copy-shade" x1="0" y1="0" x2="1800" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#171915" stop-opacity=".31"/><stop offset=".72" stop-color="#171915" stop-opacity=".31"/><stop offset="1" stop-color="#171915" stop-opacity="0"/></linearGradient></defs>')
c.rect(0,0,1800,1500,'url(#copy-shade)','id="copy-contrast-layer"')
reused_text(c,'dining','dining','#fff9ef');c.path('M190 854H474 M535 810H620 M605 797L620 810L605 823','#fff9ef',3);modules.append(c)
c=Canvas('BN02_手机场景导流',840,1110);c.rect(0,0,840,1110,BONE);c.image(A/'图片素材/BN02_导流_手机备选_1680x1680.jpg',0,0,840,840)
c.text('Set the table. Keep the glow.',38,916.72,46,500,INK,'mobile-heading')
c.text('Bring cordless light to the table.',40,975.78,29,400,INK,'mobile-body')
c.text('Explore Eric',40,1049.6,30,500,INK,'mobile-cta');c.path('M234 1041H289 M278 1031L289 1041L278 1051',INK,2);modules.append(c)
c=Canvas('BN03_REC_横版组件',1200,830);c.rect(0,0,1200,830,BONE);c.image(extracted['rec'],0,0,1200,628);c.logo(40,657,104);reused_text(c,'rec','rec');modules.append(c)
for name,file,w,h in [('BN03_REC_方版','BN03_REC_方_1200x1200.jpg',1200,1200),('BN03_REC_竖版','BN03_REC_竖_900x1600.jpg',900,1600)]:
 c=Canvas(name,w,h);c.image(A/'图片素材'/file,0,0,w,h);modules.append(c)

sources=[]
for c in modules:
 f=E/'模块源稿'/(c.key+'.svg');f.write_text(c.finish(),encoding='utf-8')
 sources.append(dict(key=c.key,file=f.name,width=c.w,height=c.h,copykeys=c.copykeys,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))

outer=Canvas('04_Banner系统展示_V04',1600,6600);outer.image(A/'连续暖墙_Banner系统展示.png',0,0,1600,6600)
outer.parts.append('<defs><filter id="display-shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs>')
def section(label,title,y):outer.text(label,80,y,17,500,'#735f4b');outer.text(title,80,y+54,34,500)
def place(c,x,y,w):
 h=w*c.h/c.w;outer.rect(x,y,w,h,'#f5efe5','filter="url(#display-shadow)"');nest(outer,c,x,y,w)
 outer.rect(x+.5,y+.5,w-1,h-1,'none','stroke="#fff8ee" stroke-opacity=".75"');placements.append(dict(key=c.key,x=x,y=y,w=w,h=h))
outer.text('04 / SELECTED WORK',80,82,17,500);outer.text('Banner System · V02',1250,82,18)
outer.text('Banner 系统 / 不同入口，同一种光',76,170,48,700)
outer.text('从认识 Eric，到餐桌导流，再到夜间广告。',80,231,25)
section('A / STORE HEADER · BRAND RECOGNITION','店铺页头：先认识 Eric',310)
place(modules[0],80,420,1440)
outer.text('完整灯体与短标题，让产品成为入口的主角。',80,866,24)
outer.text('中央裁切 / 70% 内容保留检查',260,970,22,500,'#735f4b')
place(modules[1],260,1006,1080)
outer.text('辅助裁切检查，非独立手机稿。',260,1362,21,400,'#735f4b')
section('B / IN-STORE DISCOVERY · TABLE SETTING','餐桌导流：让场景带出一个入口',1480)
place(modules[2],80,1588,1440)
outer.text('MOBILE / 独立构图，图文相邻',500,2412,22,500,'#735f4b')
place(modules[3],500,2446,600)
section('C / REC ADVERTISING · EVENING LIGHT','REC 广告：同一主题，三种比例',3430)
outer.text('横版 / 图片、品牌与标题，分别承担信息',200,3610,22,500,'#735f4b')
place(modules[4],200,3644,1200)
outer.text('方版 / 1200×1200',500,4590,22,500,'#735f4b')
place(modules[5],500,4624,600)
outer.text('竖版 / 900×1600',500,5350,22,500,'#735f4b')
place(modules[6],500,5384,600)
outer.text('NED ERIC LAMP / BANNER SYSTEM',80,6540,17,500,'#735f4b')
output=outer.finish();f=E/'04_Banner系统展示_V04_可编辑.svg';f.write_text(output,encoding='utf-8')
root=ET.fromstring(output);ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
shutil.copy2(PLAN/'04_Banner系统_展示规划_V01.md',L/'执行规划_04Banner系统_V01.md')
shutil.copy2(Path(__file__),L/Path(__file__).name)
meta=dict(output=str(O),size=[1600,6600],placements=placements,sources=sources,copy=copies,textObjects=len(list(root.iter(Q+'text'))),sourceAssets=assets,backgroundSeamMaxDifference=0,contrastLayer=dict(color='#171915',opacity=.31,plateauEnd=1296,fadeEnd=1800,textColor='#fff9ef'),status='待用户审阅')
(R/'work/ned-banner-showcase-build.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:meta[k] for k in ['output','size','textObjects']},ensure_ascii=False))
