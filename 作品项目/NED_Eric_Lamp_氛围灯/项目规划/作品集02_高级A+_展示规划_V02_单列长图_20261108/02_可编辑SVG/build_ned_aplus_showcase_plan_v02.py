from pathlib import Path
from PIL import Image, ImageFilter, ImageChops
from html import escape
import base64, hashlib, json, shutil, xml.etree.ElementTree as ET

R = Path('D:/WLQ/AIGC作品集')
O = R / 'outputs/NED_作品集02高级A+_展示规划_V02_单列长图_20261108'
E = O / '02_可编辑SVG'
A = O / '03_参考素材'
P = O / '01_示意图与预览'
for d in [E, A, P]: d.mkdir(parents=True, exist_ok=True)
SRC = R / 'outputs/NED_高级A+_V03_20261107/01_成品与预览'
OLD = R / 'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106'
W, H = 1600, 11060
manifest = []

def copy_asset(name, pure=False):
    origin = SRC / ('平台纯图素材' if pure else '图文预览') / name
    target = A / name
    if not target.exists(): shutil.copy2(origin, target)
    if not any(x['file'] == name for x in manifest):
        manifest.append(dict(file=name, source=str(origin.relative_to(R)), sha256=hashlib.sha256(origin.read_bytes()).hexdigest()))
    return target

master = Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png').convert('RGB')
oldbg = Image.open(OLD/'可编辑源稿/连续背景_提亮柔焦光影_V03.png').convert('RGB')
# Continue the same mirrored wall coordinate beyond the existing 4,640 px segment.
pad = 48
raw = Image.new('RGB', (W,H+pad*2))
period = 2 * (master.height-1)
for y in range(-pad,H+pad):
    q = (1200 + 4640 + y) % period
    q = q if q < master.height else period-q
    raw.paste(master.crop((0,q,W,q+1)), (0,y+pad))
bg = Image.blend(raw.filter(ImageFilter.GaussianBlur(15)), Image.new('RGB',raw.size,(247,240,229)), .26).crop((0,pad,W,pad+H))
# Correct the previous renderer's blur-edge clamp over 120 px; preserve source files.
last = oldbg.crop((0,oldbg.height-1,W,oldbg.height)).load()
bp = bg.load()
delta = [tuple(last[x,0][c]-bp[x,0][c] for c in range(3)) for x in range(W)]
for y in range(120):
    f = (1-y/120)**2
    for x in range(W): bp[x,y] = tuple(max(0,min(255,round(bp[x,y][c]+delta[x][c]*f))) for c in range(3))
bg.save(A/'展示规划_连续背景.png')
assert ImageChops.difference(oldbg.crop((0,4639,W,4640)),bg.crop((0,0,W,1))).getbbox() is None

def uri(path):
    mime = 'font/ttf' if path.suffix == '.ttf' else ('image/jpeg' if path.suffix.lower()=='.jpg' else 'image/png')
    return 'data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()

FONT = R/'work/ned-banner-assets/DMSans-VF.ttf'
for name in ['DMSans-VF.ttf','DM-Sans-OFL.txt']: shutil.copy2(FONT.parent/name,E/name)
counter = 0
def start(width,height,title,back=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><title>{escape(title)}</title><desc>展示规划示意；素材高级A+ V03暂通过审稿，展示布局待审阅。图片为位图，规划标题、说明与边框为独立对象。</desc><defs><style>@font-face{{font-family:DM;src:url({uri(FONT)})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style></defs>']
    s.append(f'<rect width="{width}" height="{height}" fill="#efe5d7"/>')
    if back: image(s,back,0,0,width,height)
    return s
def text(s,value,x,y,size=26,weight=400,color='#403a32'):
    global counter
    counter += 1
    s.append(f'<text id="text-{counter}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>')
def rect(s,x,y,w,h,fill='none',stroke='#ac9279',dash=None,r=0):
    s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def image(s,path,x,y,w,h):
    global counter
    counter += 1
    s.append(f'<image id="asset-{counter}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="{uri(path)}"/>')
def sample(s,key,x,y,w,pure=False):
    path=copy_asset(key+('.jpg' if pure else '.png'),pure)
    im=Image.open(path);h=w*im.height/im.width
    image(s,path,x,y,w,h)
    rect(s,x+.5,y+.5,w-1,h-1,stroke='#f8f0e6')
    return h
def section(s,letter,tag,title,y):
    text(s,letter+' / '+tag,80,y,20,500,'#795f49')
    text(s,title,80,y+64,42,600)
def note(s,lines,y):
    rect(s,80,y,1440,36+len(lines)*36,fill='#f6f0e7',stroke='#b49c85',dash='7 6',r=4)
    for i,line in enumerate(lines): text(s,line,104,y+42+i*36,24,color='#68533f')
def save_svg(s,name):
    s.append('</svg>');path=E/name;path.write_text('\n'.join(s),encoding='utf-8')
    root=ET.parse(path).getroot();ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
    return path

# This body is joined to the V01 drawing helpers to make a standalone V02 builder.
s=start(W,H,'02 高级A+｜单列长图规划示意 V02',A/'展示规划_连续背景.png')
text(s,'02 / PREMIUM A+ CONTENT',80,82,20,500)
text(s,'高级 A+ / 单列长图规划',80,166,54,600)
text(s,'六段顺序向下展开，完整呈现三个操作与三个场景。',80,226,27)
text(s,'规划 V02 · 素材 V03 暂通过审稿',1040,82,20)
note(s,['规划示意：沿用开篇V04与商品图展示V04的连续长图方式；虚线注释正式展示时移除。'],258)
sample(s,'P01_PC',80,390,1440)
text(s,'A / 宽幅开场：承接商品图展示，完整保留居家开场画面。',80,1030,25)

section(s,'B','DETAIL / HOTSPOTS','整体与真实细节',1130)
sample(s,'P02_PC',80,1240,1440)
note(s,['保留完整灯体、旋钮窗口及两个热点的对应关系；真实照片沿用V03。',
        '此处为原A+模块内部构图，作品集外层始终为一个纵向阅读栏。'],1870)

section(s,'C','INTERACTION / 3 STATES','一颗旋钮，三个操作',2080)
for key,label,y in [
 ('P03A_PC','01 / 按压：开关灯',2190),
 ('P03B_PC','02 / 旋转：调节亮度',2940),
 ('P03C_PC','03 / 按压并旋转：连续调色温',3690)]:
 text(s,label,80,y,28,500)
 sample(s,key,80,y+60,1440)
note(s,['按压 → 旋转 → 按压并旋转，三张带字完整画面依次往下排，每张同宽展示。',
        '色温条、动作箭头、英文说明保留在各自原模块中，避免只展示局部动作。'],4400)

section(s,'D','SCENES / 1 LAMP','同一盏灯，三种生活场景',4630)
for key,label,y in [
 ('P04A_PC','01 / 餐桌：日间生活',4790),
 ('P04B_PC','02 / 床头：夜间阅读',5540),
 ('P04C_PC','03 / 露台：暮色时刻',6290)]:
 text(s,label,80,y,28,500)
 sample(s,key,80,y+60,1440)
note(s,['餐桌 → 床头 → 露台，三张完整场景逐张向下展开，保留各自图文。',
        '续航条件、户外用后收回等说明随图保留；画面呈现同一单灯的不同情境。'],7000)

section(s,'E','SCALE / FAQ','尺度收束与使用问答',7230)
sample(s,'P05_PC',80,7340,1440)
sample(s,'P06_PC',80,7990,1440)
note(s,['尺寸图 → FAQ，按原顺序收束；尺寸、续航、户外使用条件保留。'],8580)

section(s,'F','RESPONSIVE / MOBILE','手机适配，继续向下阅读',8780)
text(s,'01 / 操作手机版，对应上文 C 区第三张',80,8940,28,500)
sample(s,'P03C_Mobile',500,9000,600)
text(s,'手机独立取景，文字与色温条在图下按阅读顺序排布。',80,9830,25)
text(s,'02 / 床头手机版，对应上文 D 区第二张',80,9950,28,500)
sample(s,'P04B_Mobile',500,10010,600)
text(s,'手机稿保持原始600px宽度与原比例，在统一中轴上顺序排列。',80,10770,25)
note(s,['六段均为单列纵向阅读；手机版按600px居中展示，保持文字清楚与画面比例。',
        '本图为规划试排，展示布局待审阅；静态图不执行热点、轮播或平台后台功能。'],10840)
save_svg(s,'02_高级A+_单列长图规划示意_V02.svg')

s=start(1600,2260,'02 高级A+｜纵向阅读结构 V02')
text(s,'02 / PREMIUM A+ · VERTICAL PLAN',80,82,20,500,'#795f49')
text(s,'六段阅读，从上到下',80,157,48,600)
text(s,'规划 V02 · 完整操作与场景逐张展开 · 布局待审阅',80,216,26)
items=[
 ('A / 宽幅开场','P01 居家开场，承接商品图展示','整体画面同宽呈现；沿用连续墙面背景。'),
 ('B / 真实细节','P02 整体灯体、旋钮窗口与两个热点','保留原A+模块的内部构图，清楚对应真实照片细节。'),
 ('C / 三个操作','按压开关 ↓ 旋转调光 ↓ 按压并旋转调色温','P03A、P03B、P03C 三张完整图文同宽，依次向下排。'),
 ('D / 三种场景','餐桌 ↓ 床头 ↓ 露台','P04A、P04B、P04C 三张完整场景同宽，依次向下排。'),
 ('E / 尺度与问答','P05 尺寸图 ↓ P06 FAQ','保留原图信息与使用条件，作为桌面阅读主线的收束。'),
 ('F / 手机适配','色温操作手机版 ↓ 床头场景手机版','与上文对应，按原比例居中，继续向下阅读。')]
for i,(title,line1,line2) in enumerate(items):
 y=270+i*320
 rect(s,80,y,1440,250,fill='#f8f3eb',stroke='#c9b298',r=6)
 text(s,title,112,y+62,36,500)
 text(s,line1,112,y+124,29)
 text(s,line2,112,y+184,25,color='#735f4b')
 if i<5: text(s,'↓',778,y+297,38,500,'#795f49')
text(s,'展示画布1600px宽；C/D完整宽幅图1440px宽；手机稿600px宽。',80,2230,25)
save_svg(s,'02_高级A+_纵向阅读结构_V02.svg')

plan='''# 02_高级A+｜单列长图展示规划 V02

2026-11-08。**高级 A+ V03 暂通过用户审稿；本次作品集展示布局待审阅。**

按用户最新要求，参考作品集开篇 V04 和商品图展示 V04，采用六段依次向下的连续长图。三个操作、三个场景均使用完整图文逐张展示；手机段也顺序往下排。

## 看图入口

- [单列长图示意（1600×11060）](01_示意图与预览/02_高级A+_单列长图规划示意_V02.jpg)
- [纵向阅读结构](01_示意图与预览/02_高级A+_纵向阅读结构_V02.jpg)
- [商品图至A+衔接示意](01_示意图与预览/商品图至A+_衔接示意_V02.jpg)
- [可编辑SVG](02_可编辑SVG/)

## 本次修改

1. 六段组成一个连续阅读栏，按A→F向下展开；结构总览也改为单列。
2. C区改为P03A按压开关→P03B旋转调光→P03C按压并旋转调色温，三张同宽完整带字画面逐张展开，色温渐变条保留。
3. D区改为P04A餐桌→P04B床头→P04C露台，三张同宽完整带字场景逐张展开，各自使用条件保留。
4. F区依次展示色温操作手机版、床头手机版，分别对应上文C03/D02；沿中轴居中排列。
5. V01完整保留作历史对照，当前执行以V02为准。

## 展示顺序与素材

| 区段 | 从上到下的顺序 | 展示尺寸与信息 |
| --- | --- | --- |
| A 开场 | P01_PC | 完整宽幅1440px宽，承接01商品图段 |
| B 细节 | P02_PC | 完整宽幅1440px宽，整体灯体、旋钮窗口、两个热点保留 |
| C 操作 | P03A_PC → P03B_PC → P03C_PC | 三张完整图文，每张1440px宽，依次下排 |
| D 场景 | P04A_PC → P04B_PC → P04C_PC | 三张完整图文，每张1440px宽，依次下排 |
| E 收束 | P05_PC → P06_PC | 尺度与FAQ连续向下展开 |
| F 手机 | P03C_Mobile → P04B_Mobile | 两张各600px宽，居中，原比例；对应上文桌面模块 |

“单列”约束作品集外层的阅读顺序。P02原模块内部的灯体与细节组合、手机稿自身图文结构均保留，不重新拆改V03成品。

## 画布、背景与阅读节奏

- 画布1600×11060px，主内容1440px宽，左右80px。高度为含规划注释的试排值，正式制作按留白调整。
- 摄影及已排好的英文图文保持原比例，整张嵌入；C/D六张完整图不会以小图形式挤在同一行。
- 三个操作采用按压→旋转→组合操作的顺序；场景采用日间餐桌→夜间床头→暮色露台的场景分组，不声称真实拍摄时间线。
- 暖墙背景从现有4640px商品图末端延展，沿用V01规划的衍生逻辑；背景首行与商品图背景末行逐像素一致。原母版及既有成品不覆盖。
- 延续开篇V04与商品图展示V04的深炭文字、暖墙、共同边距和纵向阅读方式；段内仅用必要小标题连接，正式展示移除虚线规划注释。
- 展示完整操作与场景会增加长图长度，本版优先保证图片与英文说明清楚。手机段通过对应上文模块说明适配关系。

## 版本与范围

外层作品集仍归V04；内容素材为高级A+ V03；展示规划为V02。用户对V03“暂通过审稿”的状态保留，本次不升级为正式定稿。

本轮只调整展示规划与示意，复用12份现有完整图文预览，不调用生图API，不修改产品、参数、原图配色或已有英文。SVG的规划标题、说明、边框和每张图片对象可编辑；既有图文中的照片与英文是位图。中文字体使用系统微软雅黑，未打包；DM Sans随附OFL许可。目标矢量编辑器导入未实测。

GitHub README直接嵌入长图，点击可查看原尺寸；静态图不执行热点与轮播，完整交互审阅页继续从V03原交付下载打开。

## 长图示意

![单列长图规划示意](01_示意图与预览/02_高级A+_单列长图规划示意_V02.jpg)

## 纵向阅读结构

![纵向阅读结构](01_示意图与预览/02_高级A+_纵向阅读结构_V02.jpg)

## 商品图段衔接

![商品图至A+衔接示意](01_示意图与预览/商品图至A+_衔接示意_V02.jpg)
'''
(O/'README.md').write_text(plan,encoding='utf-8')
(O/'04_制作记录.md').write_text('''# 制作与检查记录

2026-11-08。按用户要求将展示规划改为单列长图V02，旧V01保留。

- 复用高级A+ V03完整图文：P01、P02、P03A/B/C、P04A/B/C、P05、P06以及P03C/P04B手机版，共12份。
- C区与D区所有状态完整同宽展示；F区两张手机稿以原始600px宽居中，从上往下排。
- 本轮没有生图、原图改色、产品重绘或原图裁切。规划文字和边框独立，摄影和既有英文为位图。
- 背景承接4640px商品图末端，首行与前段背景末行一致；不覆盖原母版。
- SVG和同版渲染、图片解码、文字边界、图层唯一ID、单列位置和原素材哈希在出图时检查。
''',encoding='utf-8')
shutil.copy2(Path(__file__),E/Path(__file__).name)
(R/'work/ned-aplus-showcase-plan-v02-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(output=str(O),assets=len(manifest),height=H,seam='identical boundary row'),ensure_ascii=False))
