from pathlib import Path
from PIL import Image, ImageChops
from html import escape
import base64, hashlib, json, math, re, shutil, xml.etree.ElementTree as ET

R=Path('D:/WLQ/AIGC作品集')
O=R/'outputs/NED_作品集02_高级A+_展示_V04_修订V02_完整手机_20261108'
P=O/'01_成品与预览';E=O/'02_可编辑SVG';A=O/'03_原始素材';L=O/'04_过程记录'
for d in [P,E,A,L,E/'模块源稿']:d.mkdir(parents=True,exist_ok=True)
V=R/'outputs/NED_高级A+_V03_20261107'
OLD=R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106'
SVGNS='http://www.w3.org/2000/svg'
ET.register_namespace('',SVGNS)
FONT=R/'work/ned-banner-assets/DMSans-VF.ttf'
for name in ['DMSans-VF.ttf','DM-Sans-OFL.txt']:shutil.copy2(FONT.parent/name,E/name)
def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
fontdata=data(FONT,'font/ttf')
parts=[];placements=[];sources=[];counter=0
def txt(value,x,y,size=24,weight=400,color='#403a32',id=None):
 global counter
 counter+=1
 parts.append(f'<text id="{id or "caption-"+str(counter)}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
def section(key,eyebrow,title,y):
 parts.append(f'<g id="section-{key}-heading">')
 txt(eyebrow,80,y,17,500,color='#735f4b')
 txt(title,80,y+54,34,500)
 parts.append('</g>')
 return y+108
def module(key,x,y,w):
 source=V/'02_可编辑SVG'/(key+'.svg')
 root=ET.parse(source).getroot()
 ow,oh=[float(root.attrib[k]) for k in ['width','height']];h=w*oh/ow
 originaltext=[e.text for e in root.iter('{'+SVGNS+'}text')]
 prefix=key.lower().replace('_','-')+'-'
 idmap={e.attrib['id']:prefix+e.attrib['id'] for e in root.iter() if 'id' in e.attrib}
 for el in root.iter():
  if 'id' in el.attrib:el.attrib['id']=idmap[el.attrib['id']]
  for k,val in list(el.attrib.items()):
   if val.startswith('#') and val[1:] in idmap:el.attrib[k]='#'+idmap[val[1:]]
   elif 'url(#' in val:
    el.attrib[k]=re.sub(r'url\(#([^)]+)\)',lambda m:'url(#'+idmap.get(m.group(1),m.group(1))+')',val)
 for parent in root.iter():
  for child in list(parent):
   if child.tag=='{'+SVGNS+'}style':parent.remove(child)
 for el in root:
  if el.tag=='{'+SVGNS+'}desc':el.text='高级A+ V03暂通过用户审稿；当前作品集展示段待审阅。摄影为位图，文字与标注为独立对象。'
 root.set('id','content-'+key);root.set('x',str(x));root.set('y',str(y));root.set('width',str(w));root.set('height',str(h))
 root.set('preserveAspectRatio','xMidYMid meet')
 assert [e.text for e in root.iter('{'+SVGNS+'}text')]==originaltext
 images=[]
 for im in root.iter('{'+SVGNS+'}image'):
  href=im.attrib.get('href',im.attrib.get('{http://www.w3.org/1999/xlink}href',''))
  assert href.startswith('data:'),key
  images.append(hashlib.sha256(base64.b64decode(href.split(',',1)[1])).hexdigest())
 parts.append(f'<g id="module-{key}" data-module="{key}">')
 parts.append(f'<rect id="frame-{key}" x="{x}" y="{y}" width="{w}" height="{h}" fill="#f5efe5" filter="url(#display-shadow)"/>')
 parts.append(ET.tostring(root,encoding='unicode'))
 parts.append(f'<rect id="edge-{key}" x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" fill="none" stroke="#fff8ee" stroke-opacity=".75"/>')
 parts.append('</g>')
 shutil.copy2(source,E/'模块源稿'/source.name)
 photo=V/'01_成品与预览/平台纯图素材'/(key+'.jpg')
 if photo.exists():shutil.copy2(photo,A/photo.name)
 placements.append(dict(key=key,x=x,y=y,w=w,h=h,originalSize=[ow,oh],textObjects=len(originaltext),imageHashes=images))
 sources.append(dict(file=source.name,sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
 return math.ceil(y+h)

txt('02 / SELECTED WORK',80,82,17,500)
txt('Premium A+ · V03',1290,82,18)
txt('高级 A+ / 内容体验展示',76,170,53,700)
txt('从生活场景，到细节、操作与小屏体验。',80,231,25)
end=module('P01_PC',80,294,1440)

y=section('B','DETAIL / HOTSPOTS','整体与真实细节',end+116)
end=module('P02_PC',80,y,1440)

y=section('C','ONE KNOB / THREE ACTIONS','一颗旋钮，三个操作',end+120)
for i,(key,label) in enumerate([('P03A_PC','01 / 按压开关'),('P03B_PC','02 / 旋转调光'),('P03C_PC','03 / 按压并旋转，调节色温')]):
 txt(label,80,y,24,500,color='#735f4b')
 end=module(key,80,y+42,1440)
 y=end+90

y=section('D','ONE LAMP / THREE SETTINGS','同一盏灯，三种生活场景',end+120)
for key,label in [('P04A_PC','01 / 餐桌'),('P04B_PC','02 / 床头'),('P04C_PC','03 / 露台')]:
 txt(label,80,y,24,500,color='#735f4b')
 end=module(key,80,y+42,1440)
 y=end+90

y=section('E','COMPACT FORM / EVERYDAY QUESTIONS','尺度与使用问答',end+120)
end=module('P05_PC',80,y,1440)
end=module('P06_PC',80,end+56,1440)

y=section('F','MOBILE / THE COMPLETE EXPERIENCE','完整的手机阅读体验',end+120)
txt('从开场到问答，完整展示手机图文与全部操作、场景状态。',80,y,24)
y+=84
mobile_states=[
 ('P01_Mobile','01 / 居家开场'),
 ('P02_Knob_Mobile','02 / 真实细节：顶部旋钮'),
 ('P02_Finish_Mobile','03 / 真实细节：沙色表面'),
 ('P03A_Mobile','04 / 按压开关'),
 ('P03B_Mobile','05 / 旋转调光'),
 ('P03C_Mobile','06 / 按压并旋转，调节色温'),
 ('P04A_Mobile','07 / 餐桌场景'),
 ('P04B_Mobile','08 / 床头场景'),
 ('P04C_Mobile','09 / 露台场景'),
 ('P05_Mobile','10 / 尺度与造型'),
 ('P06_Mobile','11 / 使用问答')]
for key,label in mobile_states:
 txt(label,80,y,24,500,color='#735f4b')
 end=module(key,500,y+42,600)
 y=end+90
txt('NED ERIC LAMP / DESKTOP & MOBILE',80,end+110,18,500,color='#735f4b')
W,H=1600,math.ceil((end+210)/20)*20

from PIL import ImageFilter
master=Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png').convert('RGB')
pad=48;period=2*(master.height-1)
raw=Image.new('RGB',(W,H+2*pad))
for yy in range(-pad,H+pad):
 q=(1200+4640+yy)%period;q=q if q<master.height else period-q
 raw.paste(master.crop((0,q,W,q+1)),(0,yy+pad))
bg=Image.blend(raw.filter(ImageFilter.GaussianBlur(15)),Image.new('RGB',raw.size,(247,240,229)),.26).crop((0,pad,W,pad+H))
oldbg=Image.open(OLD/'可编辑源稿/连续背景_提亮柔焦光影_V03.png').convert('RGB')
last=oldbg.crop((0,4639,W,4640)).load();bp=bg.load()
delta=[tuple(last[xx,0][c]-bp[xx,0][c] for c in range(3)) for xx in range(W)]
for yy in range(120):
 factor=(1-yy/120)**2
 for xx in range(W):bp[xx,yy]=tuple(max(0,min(255,round(bp[xx,yy][c]+delta[xx][c]*factor))) for c in range(3))
bg.save(A/'连续暖墙_高级A+展示_完整手机.png')
assert ImageChops.difference(oldbg.crop((0,4639,1600,4640)),bg.crop((0,0,1600,1))).getbbox() is None
old_display_bg=Image.open(R/'outputs/NED_作品集02_高级A+_展示_V04_20261108/03_原始素材/连续暖墙_高级A+展示.png').convert('RGB')
assert ImageChops.difference(old_display_bg.crop((0,0,1600,7800)),bg.crop((0,0,1600,7800))).getbbox() is None
head=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>NED Eric Lamp｜02高级A+作品集展示V04</title><desc>按单列长图规划V02制作。六段纵向阅读，三个操作和三个场景完整展示。摄影为位图，英文文案、箭头、色温条、尺寸线及作品集文字为独立SVG对象。当前展示稿待用户审阅；原双示例版保留。</desc><defs><style>@font-face{{font-family:DM;src:url({fontdata})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style><filter id="display-shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs><image id="continuous-wall-background" x="0" y="0" width="{W}" height="{H}" href="{data(A/'连续暖墙_高级A+展示_完整手机.png','image/png')}"/>'''
name=f'02_高级A+展示_V04_修订V02_1600x{H}'
svg=head+'\n'+'\n'.join(parts)+'\n</svg>'
(E/'02_高级A+展示_V04_修订V02_可编辑.svg').write_text(svg,encoding='utf-8')
root=ET.fromstring(svg);ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
assert [m['key'] for m in placements]==['P01_PC','P02_PC','P03A_PC','P03B_PC','P03C_PC','P04A_PC','P04B_PC','P04C_PC','P05_PC','P06_PC']+[key for key,label in mobile_states]
for a,b in zip(placements,placements[1:]):assert a['y']+a['h']<b['y']
for m in placements:assert abs(m['x']+m['w']/2-800)<.001
meta=dict(output=str(O),name=name,size=[W,H],moduleOrder=[m['key'] for m in placements],placements=placements,sourceSvgs=sources,textObjects=len(list(root.iter('{'+SVGNS+'}text'))),uniqueIds=len(ids),seamMaxDifference=0)
(R/'work/ned-aplus-showcase-v04-full-mobile-build.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')

readme=f'''# 02_高级A+｜作品集展示 V04 · 修订V02

2026-11-08。按单列长图规划 V02 制作；根据用户反馈补齐完整手机内容。**高级A+ V03素材暂通过审稿；本次作品集展示稿已制作，待用户审阅，尚未正式定稿。**

六段依次向下：居家开场 → 真实细节 → 三个操作 → 三种场景 → 尺度与FAQ → 手机适配。桌面与手机的三个操作、三个场景均完整展示；手机含开场、两种细节、三种操作、三种场景、尺寸与FAQ，共11个独立图文状态。

## 查看与编辑

- [高清展示长图 JPG（{W}×{H}）](01_成品与预览/{name}.jpg) · [PNG](01_成品与预览/{name}.png) · [缩略图](01_成品与预览/02_高级A+展示_V04_修订V02_缩略.jpg)
- [商品图→高级A+完整连续预览](01_成品与预览/商品图至高级A+_完整连续预览_修订V02.jpg) · [接缝局部](01_成品与预览/商品图至高级A+_衔接局部_修订V02.jpg)
- [整页可编辑SVG](02_可编辑SVG/02_高级A+展示_V04_修订V02_可编辑.svg) · [21份模块源稿](02_可编辑SVG/模块源稿/)
- [使用说明与检查范围](使用说明_修订V02.md) · [制作与检查记录](04_过程记录/制作与检查记录_修订V02.md)

## 展示长图

[![02高级A+展示长图](01_成品与预览/{name}.jpg)](01_成品与预览/{name}.jpg)

## 与商品图段衔接

[![商品图至高级A+衔接局部](01_成品与预览/商品图至高级A+_衔接局部_修订V02.jpg)](01_成品与预览/商品图至高级A+_完整连续预览_修订V02.jpg)
'''
(O/'README.md').write_text(readme,encoding='utf-8')
(O/'使用说明_修订V02.md').write_text(f'''# 02高级A+展示V04｜使用说明

2026-11-08。作品集外层版本V04，内容素材高级A+ V03，执行规划V02。当前为已制作、待审阅的作品集展示稿；源素材V03暂通过审稿不等于此展示稿已终审。

## 看图与修改

先看README中的{W}×{H}高清长图，再查看商品图→A+连续预览。两段长度分别4640px与{H}px，完整连续预览为1600×{4640+H}px。中文章节标题和各完整模块独立，可在整页SVG调整位置。

整页SVG直接组装21份原模块SVG；英文文字、箭头、色温条、热点标记及尺寸线保留独立对象。摄影中的产品、手部、背景与照片阴影仍为位图；不宣称分层PSD。21份原模块SVG另附，源稿文件与V03交付一致。

使用Illustrator/Inkscape等SVG编辑器修改；Photoshop通常会栅格化SVG，不能保证保留文字对象。编辑后须重新渲染导出，对照同版预览。已用Chrome检查渲染，目标矢量编辑器导入未实测。

## 素材、字体与衔接

复用V03的原照片和文字对象，没有调用生图API、改写英文、重绘产品、锐化照片或改变照片色彩。图像保持原比例。模块外框沿用商品图段的9px偏移、12px柔影与16%暖深色透明度，浅描边仅在整个模块外沿，不描产品轮廓。

连续暖墙沿用V02规划背景，从4640px商品图段末端接续；首行与前段背景末行相同。原母版、商品图段和V03交付不覆盖。正式展示移除规划虚线注释，保留必要章节及动作/场景标签。

DM Sans与OFL许可随源稿附带；中文使用本机微软雅黑，未打包系统字体。字体缺失/替换可能改变断行；源稿照片和字体以data URI嵌入，可单独移动整页SVG。

## 展示用途与检查

此为电商视觉作品集模拟，不代表真实Amazon上架、平台审核或品牌委托。README嵌图为静态展示，热点/轮播通过原V03交互审阅页下载后查看，GitHub不会直接运行HTML。

本轮检查结果与限制集中在制作与检查记录中。素材参数继续沿用原交付的资料标称，手机11个状态均为既有独立手机稿，不将宽幅图拉伸成竖图。
''',encoding='utf-8')
lines=['# 制作与检查记录','', '2026-11-08。02高级A+作品集展示V04；待用户审阅；原双示例版保留。','', '## 本次实际制作','',
 f'- 根据单列长图规划V02制作，画布{W}×{H}。六段顺序下排，桌面10个模块及手机11个状态均完整保留。',
 '- 三个操作：P03A按压、P03B旋转、P03C按压并旋转；三个场景：P04A餐桌、P04B床头、P04C露台。',
 '- 原模块作为嵌套SVG导入，保留可编辑英文与标注；统一前缀防止渐变/箭头等ID冲突。模块文字内容与原稿逐一核对一致。',
 '- 移除规划注释，沿用商品图展示V04的外层标题、边距和投影。没有新增生图或原照片调色。',
 f'- {len(ids)}个唯一ID，{meta["textObjects"]}个文字对象；21个模块均在同一中轴，垂直范围无重叠。',
 '- 前段背景末行与本段首行逐像素相同。', '', '## 原模块来源与SHA256','', '| 模块 | SHA256 |','| --- | --- |']
for source in sources:lines.append('| '+source['file']+' | `'+source['sha256']+'` |')
lines+=['','## 渲染与视觉复核','','在出图后补充实际检查结果。']
(L/'制作与检查记录_修订V02.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
shutil.copy2(Path(__file__),L/Path(__file__).name)
print(json.dumps({k:meta[k] for k in ['size','moduleOrder','textObjects','uniqueIds','seamMaxDifference']},ensure_ascii=False))
