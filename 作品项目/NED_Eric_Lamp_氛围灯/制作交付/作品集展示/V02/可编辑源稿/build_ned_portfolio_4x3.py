from pathlib import Path
from PIL import Image, ImageCms
import base64, json, shutil

ROOT=Path('D:/WLQ/AIGC作品集')
SRC=ROOT/'work/ned-banner-assets'
LOGO=ROOT/'outputs/NED_Logo_原样重绘_20261105'
OUT=ROOT/'outputs/NED_作品集开篇_V02_4x3_20261106'
EDIT=OUT/'可编辑源稿'
EDIT.mkdir(parents=True,exist_ok=True)
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
manifest=[]

def crop(name,box,size,target):
    im=Image.open(SRC/name).convert('RGB').crop(box).resize(size,Image.Resampling.LANCZOS)
    p=EDIT/target;im.save(p,icc_profile=ICC)
    manifest.append({'source':name,'crop_box':list(box),'output_size':list(size),'file':target})
    return p

def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
def photo(p,x,y,w,h,id):return f'<image id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/png")}"/>'
def tx(t,x,y,size=24,weight=400,color='#302d28',cn=True,extra=''):
    return f'<text class="{"cn" if cn else "en"}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{t}</text>'
def base(title):return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200">
<title>{title}</title><defs><style>@font-face{{font-family:DM;src:url('{data(SRC/'DMSans-VF.ttf','font/ttf')}')}}.en{{font-family:DM,sans-serif}}.cn{{font-family:'Microsoft YaHei',sans-serif}}</style></defs>
<rect width="1600" height="1200" fill="#f3efe7"/>''']
def line(x1,y1,x2,y2):return f'<path d="M{x1} {y1}H{x2}" stroke="#d8cec0" stroke-width="1"/>'
def save(parts,name):
    parts.append('</svg>');(EDIT/name).write_text('\n'.join(parts),encoding='utf-8')

# A taller composition with an intact product; typography is reflowed, not stretched.
day=crop('P01_PC.png',(440,0,1699,803),(1600,1020),'封面_日间场景.png')
s=base('NED Eric｜无线氛围灯电商视觉系统 · 4:3 封面 V02')
s += [photo(day,0,180,1600,1020,'day-scene'),
      f'<image id="existing-wordmark" x="80" y="57" width="112" height="64" href="{data(LOGO/"NED_原样重绘_黑_紧边.svg","image/svg+xml")}"/>',
      tx('AMAZON E-COMMERCE DESIGN',246,101,19,500,cn=False,extra='letter-spacing="2"'),
      tx('Eric.',72,463,180,500,cn=False,extra='letter-spacing="-8"'),
      tx('无线氛围灯',82,575,46),tx('电商视觉系统',82,643,46),
      tx('商品图 / A+ 内容 / Banner',84,708,24),
      tx('自发概念项目 · AI 辅助设计',1520,100,18,color='#665f56',extra='text-anchor="end"')]
save(s,'01_NED_Eric_封面_V02_4x3_可编辑.svg')

# One compact brief and three visible design decisions, following the reference's narrative.
dining=crop('P05_Dining_PC.png',(550,0,1684,803),(720,510),'策略_餐桌场景.png')
detail=crop('P01_PC.png',(1210,120,1670,725),(172,226),'策略_产品细节.png')
s=base('NED Eric｜简短背景与视觉策略 · 4:3 V02')
s += [tx('PROJECT BRIEF / DESIGN APPROACH',82,97,18,500,cn=False,extra='letter-spacing="2"'),
      tx('让氛围被感受，',78,200,53,700),tx('让产品被看懂。',78,276,53,700),
      tx('以 NED Eric 无线氛围灯为对象，探索面向',82,361,25,color='#665f56'),
      tx('亚马逊美国站的电商视觉：从商品识别、',82,406,25,color='#665f56'),
      tx('卖点解释到场景导流，保持一致的表达。',82,451,25,color='#665f56'),
      photo(dining,80,548,720,510,'dining-scene'),
      tx('同一盏灯，贯穿产品信息与生活场景。',82,1103,20,color='#665f56'),
      tx('视觉策略',884,102,25,500),
      line(884,135,1520,135),
      tx('01',884,197,24,500,color='#8b7460',cn=False),
      tx('自然暖色，建立家居氛围',948,197,29,500),
      tx('米色、暖木与柔和日光，',948,248,23,color='#665f56'),
      tx('延续灯具的沙色与安静气质。',948,286,23,color='#665f56')]
for i,c in enumerate(['#e2c7a3','#b7875e','#f3efe7','#302d28']):
    s.append(f'<rect x="{948+i*124}" y="321" width="110" height="46" fill="{c}" stroke="#d8cec0" stroke-width="1"/>')
s += [line(884,407,1520,407),
      tx('02',884,469,24,500,color='#8b7460',cn=False),
      tx('产品优先，保留完整轮廓',948,469,29,500),
      photo(detail,1332,506,172,226,'product-detail'),
      tx('控制文字与道具的位置，',948,540,23,color='#665f56'),
      tx('让灯体清楚、材质可见；',948,578,23,color='#665f56'),
      tx('细节图补充操作与尺度。',948,616,23,color='#665f56'),
      line(884,761,1520,761),
      tx('03',884,823,24,500,color='#8b7460',cn=False),
      tx('信息分工，每类内容各有重点',948,823,29,500),
      tx('商品图',948,895,24,500),tx('识别产品 · 解释卖点',1110,895,23,color='#665f56'),
      tx('A+ 内容',948,949,24,500),tx('展开细节 · 理解体验',1110,949,23,color='#665f56'),
      tx('Banner',948,1003,25,500,cn=False),tx('建立认知 · 场景导流',1110,1003,23,color='#665f56'),
      tx('现有素材复用 · 多版位适配 · 产品一致性',884,1103,20,color='#665f56')]
save(s,'02_NED_Eric_背景与视觉策略_V02_4x3_可编辑.svg')
shutil.copy2(SRC/'DM-Sans-OFL.txt',EDIT/'DM-Sans-OFL.txt')
shutil.copy2(Path(__file__),EDIT/Path(__file__).name)
record={'date':'2026-11-06','version':'V02','status':'待审阅','size':[1600,1200],
    'scope':'4:3 项目封面与简短背景/视觉策略两张',
    'method':'Existing AI scene reuse, cropping, deterministic live-text SVG layout; no new AI image generation',
    'sources':manifest,'logo':'Existing ned. contour redraw, unchanged shapes',
    'fonts':'Embedded DM Sans (OFL); Microsoft YaHei local reference, not distributed',
    'attribution':'Self-initiated concept project, AI assisted; no verified commercial performance claims',
    'reference_scope':'Borrowed narrative only; third-party case images and local analysis not included in archive',
    'note':'4:3 requested by user; distinct from the reference projects’ ~1.28:1 Behance listing covers. Cover photo is interpolated ~1.27×; no new true detail.'}
(OUT/'制作记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'README.md').write_text('''# NED Eric｜作品集开篇 V02 · 4:3

日期：2026-11-06。两张均为 **1600×1200（4:3）**，待审阅。既有 V01 保留。

## 01 项目封面

![封面](01_NED_Eric_封面_V02_1600x1200.jpg)

[PNG](01_NED_Eric_封面_V02_1600x1200.png) · [可编辑 SVG](可编辑源稿/01_NED_Eric_封面_V02_4x3_可编辑.svg)

## 02 简短背景与视觉策略

![背景与视觉策略](02_NED_Eric_背景与视觉策略_V02_1600x1200.jpg)

[PNG](02_NED_Eric_背景与视觉策略_V02_1600x1200.png) · [可编辑 SVG](可编辑源稿/02_NED_Eric_背景与视觉策略_V02_4x3_可编辑.svg)

## 结构与制作

- 按用户指定制作 4:3，不能称为所参考案例的 Behance 列表封面比例。
- 借鉴参考案例 1 的“产品开场 → 简短背景与策略”叙事。保留 NED 的暖米色、深炭字和自然家居场景，未复制其品牌元素或第三方图像。
- 策略页压缩背景，连接三项设计选择与具体视觉证据：自然暖色、完整产品识别、商品图/A+/Banner 的信息分工；这些是设计意图，不是转化测试结论。
- 复用既有 AI 场景，重新裁切和排版，没有新一轮 AI 生图。封面场景约 1.27 倍插值，不能当成新增高清细节。
- SVG 文字可编辑，照片为嵌入位图；非分层摄影 PSD。DM Sans 已嵌入并附 OFL，中文依赖本机微软雅黑；跨平台缺字体需替换，已导出图片不受影响。
- 源素材为高级 A+ 原场景 `P01_PC.png` 和 `P05_Dining_PC.png`，Logo 为此前原样描摹字标。[制作记录](制作记录.json)含裁切坐标。
- 源脚本保留操作记录，运行路径需要根据本机调整。
- 按用户既有授权归档本次两张产出；此前 Behance 案例分析仅留本地，没有随本次提交。
''',encoding='utf-8')
print(str(OUT))
