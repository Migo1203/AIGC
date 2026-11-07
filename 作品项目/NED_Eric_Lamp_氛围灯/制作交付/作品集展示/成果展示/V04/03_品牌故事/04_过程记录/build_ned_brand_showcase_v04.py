from pathlib import Path
from PIL import Image,ImageFont,ImageChops
from html import escape
import xml.etree.ElementTree as ET,base64,hashlib,json,shutil,re

R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集03_品牌故事_展示_V04_20261108'
P=O/'01_成品与预览';E=O/'02_可编辑SVG';A=O/'03_原始素材';L=O/'04_过程记录'
for d in [P,E,A,L,E/'模块源稿',P/'逐模块预览']:d.mkdir(parents=True,exist_ok=True)
S=R/'work/ned-aplus-showcase-delivery-publish-20261108/作品项目/NED_Eric_Lamp_氛围灯/制作交付/亚马逊A+内容/品牌故事_V01'
F=R/'work/ned-banner-assets/DMSans-VF.ttf';NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS)
for n in ['DMSans-VF.ttf','DM-Sans-OFL.txt']:shutil.copy2(F.parent/n,E/n)
for f in (S/'图片素材').glob('*.jpg'):shutil.copy2(f,A/f.name)
logo=R/'outputs/NED_Logo_原样重绘_20261105/NED_原样重绘_黑_原画布.svg';shutil.copy2(logo,A/logo.name)
plan=R/'outputs/NED_作品集03品牌故事_展示规划_V01_20261108/03_参考素材/连续暖墙_品牌故事规划.png'
bg=Image.open(plan).convert('RGB').crop((0,0,1600,6600));bg.save(A/'连续暖墙_品牌故事展示.png')
previous=Image.open(R/'outputs/NED_作品集02_高级A+_展示_V04_修订V02_完整手机_20261108/03_原始素材/连续暖墙_高级A+展示_完整手机.png').convert('RGB')
assert ImageChops.difference(previous.crop((0,17279,1600,17280)),bg.crop((0,0,1600,1))).getbbox() is None
data=lambda p,mime:'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
fontdata=data(F,'font/ttf')
copy={
 'intro-title':'Everyday Spaces, Considered',
 'intro-body':'Simple forms and thoughtful details for the spaces we call home.',
 'B01-title':'Meet NED Collections',
 'B01-body':'Founded in Christchurch, New Zealand, in 2015, NED Collections brings together furniture, lighting and homewares.',
 'B02-title':'Simple, with Character',
 'B02-body':'Clean lines and considered details add character to the spaces we live in.',
 'B03-title':'Moments That Feel Like Home',
 'B03-body':'From a quiet corner to a shared table, small details make everyday spaces feel more personal.',
 'q1':'How are NED pieces selected?',
 'a1':'The collection is hand-selected from around the world, with an eye for clean design and character.',
 'q2':'What does NED offer?',
 'a2':'NED brings together furniture, lighting and homewares for different spaces around the home.',
 'q3':'How does Eric fit into the collection?',
 'a3':'Eric is a compact cordless lamp with adjustable light for everyday spaces.'}
sourcehtml=(S/'排版预览/品牌故事图文预览.html').read_text(encoding='utf-8')
plain=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',sourcehtml))
for key,value in copy.items():assert value in plain,(key,value)
sources=[];placements=[];counter=0
def header(w,h,title):
 return f'<svg xmlns="{NS}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{escape(title)}</title><desc>作品集模拟展示，待用户审阅。照片为位图，英文为原生文字，Logo为独立路径。</desc><defs><style>@font-face{{font-family:DM;src:url({fontdata})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style></defs>'
class Canvas:
 def __init__(self,key,w,h):self.key=key;self.w=w;self.h=h;self.parts=[];self.copies=[]
 def rect(self,x,y,w,h,fill,attrs=''):self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {attrs}/>')
 def image(self,p,x,y,w,h,mode='meet'):
  self.parts.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/jpeg" if p.suffix==".jpg" else "image/png")}" preserveAspectRatio="xMidYMid {mode}"/>')
 def line(self,s,x,y,size=24,weight=400,color='#403a32'):
  global counter
  counter+=1;self.parts.append(f'<text id="text-{counter}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(s)}</text>')
 def paragraph(self,key,x,top,w,size,lh,weight=400,color='#4b4d49'):
  value=copy[key];font=ImageFont.truetype(str(F),round(size*10))
  try:font.set_variation_by_name('Bold' if weight>=600 else 'Regular')
  except ValueError:pass
  lines=[];line=''
  for word in value.split():
   trial=(line+' '+word).strip()
   if line and font.getlength(trial)/10>w:lines.append(line);line=word
   else:line=trial
  if line:lines.append(line)
  assert ' '.join(lines)==value
  self.parts.append(f'<g data-copy="{key}" data-block="{x},{top},{w},{len(lines)*lh}">')
  for i,s in enumerate(lines):self.line(s,x,top+size+i*lh,size,weight,color)
  self.parts.append('</g>');self.copies.append(key)
  return top+len(lines)*lh
 def logo(self,x,y,w):
  root=ET.parse(logo).getroot();vb=[float(n) for n in root.attrib['viewBox'].split()]
  root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(w*vb[3]/vb[2]));root.set('data-logo','ned-original-trace');self.parts.append(ET.tostring(root,encoding='unicode'))
 def finish(self):return header(self.w,self.h,self.key)+''.join(self.parts)+'</svg>'
def intro(c,mobile):
 if mobile:
  c.line('BRAND STORY',24,35,10,700,'#ffffff')
  end=c.paragraph('intro-title',24,43,342,21,25,600,'#ffffff')
  c.paragraph('intro-body',24,end+5,342,12.5,16,400,'#ffffff')
 else:
  c.line('BRAND STORY',40,92,12,700,'#ffffff')
  end=c.paragraph('intro-title',40,112,240,32,37,600,'#ffffff')
  c.paragraph('intro-body',40,end+16,240,16,24,400,'#ffffff')
def card(c,state,x,y,w,h,mobile):
 c.parts.append(f'<g data-card="{state}" data-bounds="{x},{y},{w},{h}">')
 c.rect(x,y,w,h,'#fbfaf7');px=x+20;inner=w-40
 if state=='B01':
  c.logo(px,y+35,150)
  end=c.paragraph('B01-title',px,y+(123 if mobile else 122),inner,24 if mobile else 23,28,600,'#292b28')
  end=c.paragraph('B01-body',px,end+14,inner,15,23)
 elif state in ['B02','B03']:
  end=c.paragraph(state+'-title',px,y+20,inner,20 if mobile else 19,24 if mobile else 22,600,'#292b28')
  end=c.paragraph(state+'-body',px,(end+10 if mobile else y+76),inner,14,20)
  im= A/('B02_审美与造型.jpg' if state=='B02' else 'B03_夜间生活.jpg');iw,ih=Image.open(im).size
  pw=240 if mobile else inner;ph=pw*ih/iw;iy=end+16 if mobile else y+176
  assert iy+ph<=y+h-12,(state,iy+ph,y+h)
  c.image(im,x+(w-pw)/2,iy,pw,ph)
  end=iy+ph
 else:
  end=y+20
  for i in range(1,4):
   end=c.paragraph('q'+str(i),px,end,inner,14,18,600,'#292b28')
   end=c.paragraph('a'+str(i),px,end+5,inner,13,18)
   end+=14
 assert end<=y+h-10,(state,end,y+h)
 c.parts.append('</g>')
modules=[]
c=Canvas('B00_Desktop',1464,625);c.image(A/'B00_电脑背景.jpg',0,0,1464,625,'slice')
c.parts.append('<defs><linearGradient id="intro-shade" x2="1" y2="0"><stop stop-color="#1c1f1d" stop-opacity=".75"/><stop offset=".35" stop-color="#1c1f1d" stop-opacity=".16"/><stop offset="1" stop-color="#1c1f1d" stop-opacity=".08"/></linearGradient></defs>');c.rect(0,0,1464,625,'url(#intro-shade)');intro(c,False)
for i,state in enumerate(['B01','B02','B03','B04']):card(c,state,312+i*284,44,270,537,False)
modules.append(c)
for i,state in enumerate(['B01','B02','B03','B04']):
 c=Canvas(state+'_Mobile',390,625);c.image(A/'B00_手机背景.jpg',0,0,390,625,'slice')
 c.parts.append('<defs><linearGradient id="intro-shade" x2="0" y2="1"><stop stop-color="#191d1b" stop-opacity=".75"/><stop offset=".37" stop-color="#191d1b" stop-opacity=".18"/><stop offset="1" stop-color="#191d1b" stop-opacity=".12"/></linearGradient></defs>');c.rect(0,0,390,625,'url(#intro-shade)');intro(c,True);card(c,state,48,123,294,480,True);modules.append(c)
for c in modules:
 f=E/'模块源稿'/(c.key+'.svg');f.write_text(c.finish(),encoding='utf-8');sources.append(dict(key=c.key,file=f.name,copies=c.copies,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
outer=Canvas('03品牌故事作品集展示V04',1600,6600)
outer.image(A/'连续暖墙_品牌故事展示.png',0,0,1600,6600)
outer.parts.append('<defs><filter id="display-shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs>')
outer.line('03 / SELECTED WORK',80,82,17,500);outer.line('Brand Story · V01',1290,82,18)
outer.line('品牌故事 / 从产品走向生活方式',76,170,48,700)
outer.line('用空间、造型与日常片刻，连接同一种家居气质。',80,231,25)
def frame(x,y,w,h):outer.rect(x,y,w,h,'#f5efe5','filter="url(#display-shadow)"')
def edge(x,y,w,h):outer.rect(x+.5,y+.5,w-1,h-1,'none','stroke="#fff8ee" stroke-opacity=".75"')
def place(c,x,y,w):
 h=w*c.h/c.w;frame(x,y,w,h);root=ET.fromstring(c.finish());prefix=c.key.lower()+'-'
 for el in root.iter():
  if 'id' in el.attrib:el.set('id',prefix+el.attrib['id'])
  for k,val in list(el.attrib.items()):
   if 'url(#' in val:el.set(k,re.sub(r'url\(#([^)]+)\)',lambda m:'url(#'+prefix+m[1]+')',val))
 for parent in root.iter():
  for child in list(parent):
   if child.tag=='{'+NS+'}style':parent.remove(child)
 root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h));root.set('data-module',c.key)
 outer.parts.append(ET.tostring(root,encoding='unicode'));edge(x,y,w,h);placements.append(dict(key=c.key,x=x,y=y,w=w,h=h))
frame(80,294,1440,1440*829/1897);outer.image(A/'B00_电脑背景.jpg',80,294,1440,1440*829/1897);edge(80,294,1440,1440*829/1897)
outer.line('DESKTOP / THE COMPLETE STORY',80,1040,17,500,'#735f4b');outer.line('认识品牌，感受造型，再走进日常',80,1094,34,500)
place(modules[0],80,1148,1440)
outer.line('MOBILE / ALL FOUR STATES',80,1920,17,500,'#735f4b');outer.line('四个故事，延续同一种家居气质',80,1974,34,500)
outer.line('品牌介绍 → 审美与造型 → 日常生活 → 品牌问答',80,2030,24)
labels=['01 / 品牌介绍','02 / 审美与造型','03 / 日常生活','04 / 品牌问答']
for i,c in enumerate(modules[1:]):
 y=2130+i*1100;outer.line(labels[i],500,y,22,500,'#735f4b');place(c,500,y+34,600)
outer.line('NED ERIC LAMP / BRAND STORY',80,6540,17,500,'#735f4b')
output=outer.finish();(E/'03_品牌故事展示_V04_可编辑.svg').write_text(output,encoding='utf-8')
root=ET.fromstring(output);ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
meta={'output':str(O),'size':[1600,6600],'placements':placements,'sources':sources,'copy':copy,'textObjects':len(list(root.iter('{'+NS+'}text'))),'ids':len(ids),'backgroundSeamMaxDifference':0,'sourcePhotos':[{ 'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in A.glob('*.jpg')]}
(R/'work/ned-brand-showcase-build.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),L/Path(__file__).name)
print(json.dumps({k:meta[k] for k in ['size','textObjects','ids']},ensure_ascii=False))
