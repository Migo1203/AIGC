from pathlib import Path
from PIL import Image, ImageFilter, ImageChops
from html import escape
import base64, hashlib, json, shutil, xml.etree.ElementTree as ET

R = Path('D:/WLQ/AIGC作品集')
O = R / 'outputs/NED_作品集02高级A+_展示规划_V01_20261108'
E = O / '02_可编辑SVG'
A = O / '03_参考素材'
P = O / '01_示意图与预览'
for d in [E, A, P]: d.mkdir(parents=True, exist_ok=True)
SRC = R / 'outputs/NED_高级A+_V03_20261107/01_成品与预览'
OLD = R / 'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106'
W, H = 1600, 7800
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

s=start(W,H,'02 高级A+｜展示规划示意 V01',A/'展示规划_连续背景.png')
text(s,'02 / PREMIUM A+ CONTENT',80,82,20,500)
text(s,'高级 A+ / 展示段规划',80,166,54,600)
text(s,'从场景认识产品，到理解操作、细节与小屏体验。',80,226,27)
text(s,'规划 V01 · 素材 V03 暂通过审稿',1040,82,20)
note(s,['示意图：采用真实交付素材试排。虚线框为规划注释，正式展示时移除。'],258)
sample(s,'P01_PC',80,390,1440)
text(s,'A / 宽幅开场：使用 P01；章节标题只出现一次，保留产品与人物的主次。',80,1030,25)

section(s,'B','DETAIL / HOTSPOTS','整体与真实细节',1130)
sample(s,'P02_PC',80,1240,1440)
note(s,['两个热点：①顶部旋钮  ②沙色表面。沿用现有照片与蒙版，不新增放大工艺纹理。',
        '静态展示保留两个标记及对应说明；完整切换状态链接至审阅包。'],1870)

section(s,'C','INTERACTION / 3 STATES','一颗旋钮，三个操作',2080)
sample(s,'P03C_PC',80,2190,1440)
text(s,'03 / 按压并旋转：连续调色温',80,2820,26,500)
sample(s,'P03A_PC',80,2850,700,pure=True)
sample(s,'P03B_PC',820,2850,700,pure=True)
text(s,'01 / 按压开关',80,3184,27,500)
text(s,'02 / 旋转调光',820,3184,27,500)
note(s,['上方主展 P03C「按压并旋转」与胶囊形连续色温条；下方补充另外两种动作。',
        '辅助图采用无字素材另排短标签；不把三个带长文案的宽幅模块硬缩成一排。'],3240)

section(s,'D','SCENES / 1 LAMP','同一盏灯，不同生活时刻',3450)
sample(s,'P04B_PC',80,3560,1440)
sample(s,'P04A_PC',80,4220,700,pure=True)
sample(s,'P04C_PC',820,4220,700,pure=True)
text(s,'餐桌 / 日间互动',80,4554,27,500)
text(s,'露台 / 户外使用后收回室内',820,4554,27,500)
note(s,['床头夜景主展，餐桌与露台辅助；保持日间、夜间、暮色的真实画面差异。',
        '静态展开用于说明场景导航设计，画面表现同一单灯的不同使用情境。'],4610)

section(s,'E','SCALE / FAQ','尺度收束与使用问答',4820)
sample(s,'P05_PC',80,4930,1440)
sample(s,'P06_PC',80,5570,1440)
note(s,['P05 与 FAQ 按原有信息顺序收束；尺寸、续航和户外使用条件随对应模块保留。'],6150)

section(s,'F','RESPONSIVE / DESKTOP + MOBILE','为小屏重新组织阅读',6350)
sample(s,'P03C_PC',80,6470,900)
sample(s,'P03C_Mobile',1150,6470,330)
text(s,'操作：横幅中的文字与渐变条 → 手机图下独立排版',80,6910,25)
text(s,'手机稿原比例',1150,6950,22)
sample(s,'P04B_PC',80,7060,900)
sample(s,'P04B_Mobile',1150,7060,330)
text(s,'场景：独立竖向取景，保留产品、手部动作和阅读顺序',80,7498,25)
text(s,'手机稿原比例',1150,7498,22)
note(s,['桌面图与手机图分别来自现有交付；这里展示适配关系，图片保持原比例。',
        '本段为作品集模拟展示；静态示意不执行热点或轮播，完整内容另附原图入口。'],7590)
main_svg=save_svg(s,'02_高级A+_规划示意_V01.svg')

# Compact decision map: keep it legible without opening the whole long page.
s=start(1600,1200,'02 高级A+｜规划总览 V01')
text(s,'02 / PREMIUM A+ · DISPLAY PLAN',80,82,20,500,'#795f49')
text(s,'展示结构：六段阅读，一条主线',80,157,48,600)
text(s,'A+ V03 暂通过审稿 · 本图为作品集展示规划，待审阅',80,216,26)
cards=[
('A','宽幅开场','P01_PC',['以产品与居家情绪开场','承接01商品图展示']),
('B','真实细节','P02_PC',['完整灯体＋两个热点','真实照片、旋钮与表面']),
('C','三个操作','P03C_PC',['色温渐变条作主展','按压、旋转作补充']),
('D','三种场景','P04B_PC',['床头主展，餐桌/露台辅助','形成昼夜与暮色的变化']),
('E','尺度与问答','P05_PC',['尺寸图＋FAQ收束','条件随对应内容保留']),
('F','手机适配','P03C_Mobile',['对照操作与床头两组','画面取景与文字分别重排'])]
for i,(letter,title,key,lines) in enumerate(cards):
    x=80+(i%2)*740;y=270+(i//2)*280
    rect(s,x,y,700,250,fill='#f8f3eb',stroke='#d3bfa9',r=8)
    text(s,letter+' / '+title,x+24,y+43,30,500)
    path=copy_asset(key+'.png');im=Image.open(path);im.thumbnail((315,150))
    image(s,path,x+24,y+73,315,150)
    for j,line in enumerate(lines):text(s,line,x+363,y+112+j*40,23)
text(s,'复用现有素材 / 不新增生图 / 暖墙连续衔接 / 图像不统一染色',80,1150,25)
save_svg(s,'02_高级A+_规划总览_V01.svg')

plan='''# 02_高级A+｜作品集展示规划 V01

2026-11-08。**用户已明确：高级 A+ V03 暂通过审稿。** 本次只制作作品集展示规划及示意图，展示布局待审阅；不是 A+ 正式定稿或上架。

## 看图入口

- [规划总览](01_示意图与预览/02_高级A+_规划总览_V01.jpg)：先看六段内容取舍。
- [长页规划示意](01_示意图与预览/02_高级A+_规划示意_V01.jpg)：使用真实 V03 素材，含虚线规划注释。
- [商品图至A+衔接示意](01_示意图与预览/商品图至A+_衔接示意_V01.jpg)：检查商品图尾部、背景接缝和下一章节入口。
- [可编辑SVG](02_可编辑SVG/)：规划标题、说明、边框和各图片对象独立；摄影与已有带字预览仍为位图。

![规划总览](01_示意图与预览/02_高级A+_规划总览_V01.jpg)

## 展示目标与取舍

商品图段已经完整展示 Listing 与八张商品图，A+段转向页面叙事、交互状态与手机适配。推荐一条连续阅读路径，重点为操作设计和多场景体验。

不在开头完整缩放一遍整条 A+，随后又重复展示全部局部；完整桌面/手机长页留作附录链接。主线按 P01→P02→P03→P04→P05→P06 展开，再展示两组手机适配。P03/P04 的全部状态通过主次排布展开，避免三张带长文案宽幅硬缩为一排。

| 区段 | 展示内容与素材 | 版式与阅读任务 |
| --- | --- | --- |
| A 宽幅开场 | P01_PC | 居家开场，完整产品为焦点；章节标题只出现一次 |
| B 真实细节 | P02_PC，两个热点的既有字段 | 完整灯体＋旋钮窗口，对应①顶部旋钮②沙色表面；静态图保留对应关系 |
| C 三个操作 | P03C_PC 主展；P03A_PC/P03B_PC 无字素材辅助 | 色温渐变条作为记忆点；辅助图另排按压/旋转短标签，不挤小英文正文 |
| D 三种场景 | P04B_PC 主展；P04A_PC/P04C_PC 无字素材辅助 | 床头夜景带出光感，餐桌和露台补充场景变化，标明同一单灯多场景 |
| E 尺度与FAQ | P05_PC＋P06_PC | 完整尺寸图收束；FAQ保留现有三问，条件紧邻对应宣称 |
| F 手机适配 | P03C_PC/Mobile、P04B_PC/Mobile | 两组桌面/手机对应展示，解释独立取景、图下文案和阅读重排 |

示意图里的 A—F 是规划标记，不是另建六个商品模块。正式展示只保留必要标题与短说明，移除虚线规划框。

## 画布与衔接

- 外层作品集版本沿用 V04，素材版本标明高级 A+ V03；本次规划为 V01。
- 试排画布1600×7800 px，主内容宽1440、两侧80 px。高度是本次含注释的示意值，正式排版按文字与留白调整，不硬凑长度。
- 商品图段实际高4640 px。背景继续使用同一暖墙V02母版与提亮衍生逻辑，从商品图末端的连续坐标接续，不从母版顶端重贴。
- 原母版、商品图、A+成品全部保留。本轮仅生成规划用背景衍生图：15px柔焦、26%暖白混合；前120px修正旧渲染器边缘差异，第一行与商品图背景最后一行逐像素一致。
- 商品图末端至A+入口的留白在衔接预览中一起审阅。A+照片保留日夜色彩，不染成同一暖墙色。
- 延续深炭文字、DM Sans/微软雅黑、共同边距。无字辅助照片的动作标签与条件独立排版。

## 静态展示与交互入口

GitHub README展示JPG；点击可看原尺寸。静态示意不能执行热点、轮播，也不冒充Amazon后台页面。正式展示拟附可切换原审阅页的下载入口及全部状态原图；GitHub文件页不会直接运行HTML。

## 制作范围与检查

本次复用已有交付，不调用生图API，不修改V03的产品照片、功能参数或原文；仅生成规划背景、SVG、同版预览及说明。原图哈希记录在制作脚本生成的素材记录中。PNG示意由SVG同版渲染，JPG由其导出。

自检覆盖图片可解码、SVG唯一ID、无外部图片依赖、文字边界、同版导出、原素材哈希、背景首尾接缝和实际看图。预览正常不代表Illustrator/Inkscape导入已实测。

后续正式制作重点：B区两个热点的清楚对应；C区色温条与操作箭头；P02/P04/P05产品底部在缩放后有无新增描边或厚黑条；F区手机文字清楚且不被截断。不因V03暂通过审稿而省略作品集组合后的复核。

## 拟归档位置与后续交付

作品集正式展示：`作品集展示/成果展示/V04/02_高级A+/`。

本次规划：`项目规划/作品集02_高级A+_展示规划_V01_20261108/`。规划示意保持与正式展示段分开，避免把占位和注释当成最终成品。

正式制作交付拟含高清展示长图、缩略图、可编辑SVG、必要独立素材、商品图→A+连续预览和嵌图README。制作以本次用户对规划的反馈为依据。

## 长页规划示意

![长页规划示意](01_示意图与预览/02_高级A+_规划示意_V01.jpg)

## 与商品图段衔接

![商品图至A+衔接示意](01_示意图与预览/商品图至A+_衔接示意_V01.jpg)
'''
(O/'README.md').write_text(plan,encoding='utf-8')
(O/'04_制作记录.md').write_text('''# 制作记录

2026-11-08。高级 A+ V03 暂通过用户审稿；作品集02展示段规划 V01 待审阅。

- 六段试排均使用已有V03交付；不调用生图API。
- 原始素材独立保存至03_参考素材，摄影和既有英文文字为位图；规划文字、形状和版式为SVG独立对象。
- 图像按原比例缩放，示意不裁切产品，不叠加产品描边、不调色、不锐化。
- 背景按商品图尾部连续坐标衍生；末行对首行差值为0。原背景及既有交付未覆盖。
- DM Sans随附OFL许可；中文使用本机微软雅黑，未打包系统字体。SVG未实测目标矢量编辑器兼容。
- 规划示意以静态画面表达状态，不冒充可操作平台界面。

源文件哈希、渲染检查与实际视觉复核结论见交付时补充。
''',encoding='utf-8')
shutil.copy2(Path(__file__), E/Path(__file__).name)
(R/'work/ned-aplus-showcase-plan-assets.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(output=str(O),assets=len(manifest),svg=[p.name for p in E.glob('*.svg')],seam='identical boundary row'),ensure_ascii=False))
