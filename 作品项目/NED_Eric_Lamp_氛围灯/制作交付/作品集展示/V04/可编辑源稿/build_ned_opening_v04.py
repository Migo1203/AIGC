from pathlib import Path
from PIL import Image, ImageCms, ImageFilter
import numpy as np
import base64, json, shutil

ROOT=Path('D:/WLQ/AIGC作品集');SRC=ROOT/'work/ned-banner-assets'
BG=ROOT/'outputs/NED_作品集连续背景_V02_20261106'
OUT=ROOT/'outputs/NED_作品集开篇_V04_轻过渡与视觉情绪板_20261106'
EDIT=OUT/'可编辑源稿';EDIT.mkdir(parents=True,exist_ok=True)
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
def imtag(p,x,y,w,h,id):return f'<image id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/png")}"/>'
def text(t,x,y,size=24,weight=400,color='#302d28',cn=True,extra=''):
 return f'<text class="{"cn" if cn else "en"}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{t}</text>'
def base(title):return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200"><title>{title}</title>
<defs><style>@font-face{{font-family:DM;src:url('{data(SRC/'DMSans-VF.ttf','font/ttf')}')}}.en{{font-family:DM,sans-serif}}.cn{{font-family:'Microsoft YaHei',sans-serif}}</style><clipPath id="macro-circle"><circle cx="1082" cy="452" r="88"/></clipPath></defs>''']
def save(s,name):
 s.append('</svg>');(EDIT/name).write_text('\n'.join(s),encoding='utf-8')
def crop(name,box,size,outname):
 p=EDIT/outname;Image.open(SRC/name).convert('RGB').crop(box).resize(size,Image.Resampling.LANCZOS).save(p,icc_profile=ICC);return p

wall=np.asarray(Image.open(BG/'NED_连续墙面背景_V02_1600x2400.png').convert('RGB'))
extension=wall[:1200][::-1].copy()
Image.fromarray(wall[:1200]).save(EDIT/'策略页_连续背景.png',icc_profile=ICC)
Image.fromarray(wall[1200:]).save(OUT/'成果速览_下一屏背景_1600x1200.png',icc_profile=ICC)
scene=crop('P01_PC.png',(355,0,1783,803),(1600,900),'封面_原场景裁切.png')
sa=np.asarray(Image.open(scene),dtype=np.float32)
se=np.concatenate([sa,np.repeat(sa[-1:],300,axis=0)],axis=0)
y=np.arange(1200,dtype=np.float32)[:,None,None]
blur=np.asarray(Image.fromarray(se.astype(np.uint8)).filter(ImageFilter.GaussianBlur(12)),dtype=np.float32)
e=np.clip((y-850)/50,0,1);e=e*e*(3-2*e)
se=se*(1-e)+blur*e
t=np.clip((y-880)/120,0,1);smooth=t*t*(3-2*t)
cover=np.clip(se*(1-smooth)+extension.astype(np.float32)*smooth,0,255).astype(np.uint8)
Image.fromarray(cover).save(EDIT/'封面_场景至墙面过渡.png',icc_profile=ICC)
Image.fromarray(np.repeat((smooth[:,0,:]*255).astype(np.uint8)[:,None,:],1600,axis=1).squeeze()).save(EDIT/'封面_环境过渡蒙版.png')
s=base('NED Eric｜轻过渡封面 V04')
s += [imtag(EDIT/'封面_场景至墙面过渡.png',0,0,1600,1200,'scene-to-approved-wall'),
 f'<image id="existing-ned-wordmark" x="80" y="42" width="98" height="56" href="{data(ROOT/"outputs/NED_Logo_原样重绘_20261105/NED_原样重绘_黑_紧边.svg","image/svg+xml")}"/>',
 text('AMAZON E-COMMERCE DESIGN',219,79,17,500,cn=False,extra='letter-spacing="1.8"'),
 text('Eric.',74,318,156,500,cn=False,extra='letter-spacing="-7"'),text('无线氛围灯',82,427,43),text('电商视觉系统',82,492,43),
 text('商品图 / A+ 内容 / Banner',84,551,24),text('自发概念项目 · AI 辅助设计',84,601,18,color='#51493f')]
save(s,'01_NED_Eric_封面_V04_4x3_可编辑.svg')

# Evidence uses the project's own photography. No Behance art is composited.
dining=crop('P05_Dining_PC.png',(320,0,1770,803),(830,460),'策略_餐桌暮色.png')
night=crop('P05_Bed_PC.png',(1000,135,1730,635),(365,250),'策略_夜间暖光.png')
macro=crop('product_reference.png',(480,310,700,530),(176,176),'策略_灯罩细节.png')
im=Image.open(SRC/'product_reference.png').convert('RGB')
pa=np.asarray(im).astype(np.float32)
# Warm product differs from the neutral background; preserve source RGB and use a chroma matte.
alpha=np.clip((pa[:,:,0]-pa[:,:,2]-6)/14,0,1)
rgba=np.dstack([pa,alpha*255]).astype(np.uint8)
product=EDIT/'策略_产品透明抠图.png'
Image.fromarray(rgba).crop((345,155,900,1135)).save(product,icc_profile=ICC)
s=base('NED Eric｜背景与视觉策略 V04')
s += [imtag(EDIT/'策略页_连续背景.png',0,0,1600,1200,'approved-wall-upper-half'),
 text('PROJECT BRIEF / VISUAL DIRECTION',80,82,17,500,cn=False,extra='letter-spacing="2"'),
 text('让氛围被感受，',76,168,53,700),text('让产品被看懂。',76,239,53,700),
 text('以 NED Eric 无线氛围灯为对象，',920,140,24,color='#51493f'),
 text('探索面向亚马逊美国站的电商视觉。',920,181,24,color='#51493f'),
 text('把生活氛围与产品信息，串成一致的体验。',920,222,24,color='#51493f'),
 text('01',80,323,21,500,color='#715b46',cn=False),text('暖中性基调，昼夜有变化',128,323,26,500),
 imtag(dining,80,351,830,460,'dining-dusk'),
 text('DINING / DUSK',104,390,15,500,color='#ede6dc',cn=False,extra='letter-spacing="1.5"'),
 '<rect x="72" y="572" width="381" height="266" fill="#eee5d9"/>',
 imtag(night,80,580,365,250,'bedside-night'),
 text('NIGHT / 夜间暖光',96,869,17,500,cn=False),
 text('自然材质打底，以日光、夜间蓝灰',490,857,21,color='#51493f'),
 text('与暮色拉开层次。',490,892,21,color='#51493f'),
 text('02',1160,323,21,500,color='#715b46',cn=False),text('产品优先',1208,323,26,500),
 imtag(product,1192,365,282,498,'product-silhouette'),
 '<g clip-path="url(#macro-circle)">',imtag(macro,994,364,176,176,'shade-macro'),'</g>',
 '<circle cx="1082" cy="452" r="88" fill="none" stroke="#efe4d5" stroke-width="6"/>',
 '<path d="M1162 488L1216 515" stroke="#715b46" stroke-width="1.2" fill="none"/>',
 text('轮廓建立识别，近景解释质感；',1115,897,21,color='#51493f'),text('功能信息按问题分组。',1115,932,21,color='#51493f')]
# Reference colors, not claimed official brand colors.
for cx,col in [(508,'#F4F1EB'),(560,'#D8CABC'),(612,'#5A463B'),(664,'#2F302E')]:
 s.append(f'<circle cx="{cx}" cy="930" r="18" fill="{col}" stroke="#a5907d" stroke-width=".5"/>')
s += [text('项目参考色',704,937,18,color='#51493f'),
 '<path d="M80 976H1520" stroke="#8c7763" stroke-opacity=".4"/>',
 text('03',80,1033,21,500,color='#715b46',cn=False),text('按购物问题',80,1080,26,500),text('组织内容',80,1118,26,500),
 text('商品图',400,1049,29,500),text('识别产品 · 解释卖点',400,1100,21,color='#51493f'),
 text('A+ 内容',815,1049,29,500),text('展开细节 · 理解体验',815,1100,21,color='#51493f'),
 text('Banner',1230,1049,30,500,cn=False),text('建立认知 · 场景导流',1230,1100,21,color='#51493f'),
 '<path d="M682 1058H756m-9-7 9 7-9 7M1097 1058H1171m-9-7 9 7-9 7" fill="none" stroke="#8c7763" stroke-width="1.5"/>']
save(s,'02_NED_Eric_背景与视觉策略_V04_4x3_可编辑.svg')
shutil.copy2(SRC/'DM-Sans-OFL.txt',EDIT/'DM-Sans-OFL.txt')
shutil.copy2(Path(__file__),EDIT/Path(__file__).name)
record={'date':'2026-11-06','version':'V04','status':'待审阅','page_size':[1600,1200],
 'transition':{'start_y':880,'end_y':1000,'curve':'smoothstep','blur_radius_px':12,'V03_blur_radius_px':48,'V03_fade':[820,1060]},
 'protected_source_rows':[0,850],'background_master':'Approved wall V02; strategy 0:1200; next overview 1200:2400',
 'method':'Existing scenes, deterministic crops, lighter environmental crossfade, chroma product matte, editable SVG text; no new AI generation',
 'references':[{'title':'Brand Identity Moodboard & Presentation Slides','author':'STEPHEN ALEJI','url':'https://www.behance.net/gallery/242874515/Moodboard-Design-Presentation-Slides-Brand-Identity','applied':'Asymmetric scene collage, overlapping photos, palette near visual evidence'},
 {'title':'Amazon Listing Design for Kids Supplement','author':'Anzhela Nefedova','url':'https://www.behance.net/gallery/247462769/Amazon-Listing-Design-for-Kids-Supplement','applied':'Short approach and visual evidence paired together before output grid'}],
 'limits':'Reference layouts do not establish commercial performance. Source RGB product preserved but matte is derived. Scene bottom extended before fade. No Behance artwork reused. SVG images are embedded raster; Chinese font depends on local Microsoft YaHei.'}
(OUT/'制作记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'README.md').write_text('''# NED Eric｜作品集开篇 V04

2026-11-06。封面与背景/策略两页均为 1600×1200（4:3），待审阅；旧版保留。

![连续阅读预览](封面至策略_连续阅读预览.jpg)

## 封面：减轻下缘虚化

![封面](01_NED_Eric_封面_V04_1600x1200.jpg)

[PNG](01_NED_Eric_封面_V04_1600x1200.png) · [可编辑 SVG](可编辑源稿/01_NED_Eric_封面_V04_4x3_可编辑.svg)

保留 V03 的紧凑顶部与产品构图。环境模糊半径从 48px 改为 12px，渐变区由 y=820–1060 缩至 y=880–1000；桌面清晰区延长。仅处理主体之外的下缘环境，前 850 行背景与原裁切一致；不声称虚化程度降低了某个感知百分比。底部环境有延展，非新拍摄。

## 背景与视觉策略：用画面说明策略

![背景与策略](02_NED_Eric_背景与视觉策略_V04_1600x1200.jpg)

[PNG](02_NED_Eric_背景与视觉策略_V04_1600x1200.png) · [可编辑 SVG](可编辑源稿/02_NED_Eric_背景与视觉策略_V04_4x3_可编辑.svg)

- 简短背景置于顶部；餐桌暮色与夜间暖光错落叠放，呈现暖中性基调中的场景层次。
- 项目参考色靠近场景；单独的产品轮廓与灯罩局部呈现识别和质感焦点。色块不是品牌官方色号。
- 下方以三段内容路径呈现商品图、A+、Banner 的分工。箭头表示展示组织，不代表真实购物路径或转化数据。
- 三条策略保持当前统一规划：暖中性与昼夜变化、产品优先、按购物问题组织内容。
- 策略背景直接使用获准连续墙面 V02 的前 1200 行，下一屏仍接后 1200 行；未替换母版或重新调色。

## 布局参考

实际查看 Behance 页面图片后借鉴：[STEPHEN ALEJI 的情绪板](https://www.behance.net/gallery/242874515/Moodboard-Design-Presentation-Slides-Brand-Identity)中的大小错落、照片叠放及配色关联；[Anzhela Nefedova 的电商案例](https://www.behance.net/gallery/247462769/Amazon-Listing-Design-for-Kids-Supplement)中的简短策略与视觉依据配对。未使用其图片、品牌或文案。详细参考截图与研究留本地，不在本目录归档。

本项目为自发概念项目、AI 辅助设计，未实际上传亚马逊或投放广告，不含销售效果主张。此轮复用项目已有位图，并非新一轮 AI 生图。源稿中的文字可编辑，图片为嵌入位图；产品透明图采用中性背景色差蒙版，不增造结构。附 DM Sans OFL；中文字体引用本机微软雅黑，不分发系统字体。脚本路径需按运行环境调整。

[制作记录](制作记录.json) · [连续背景 V02](../共享背景/V02/README.md) · [当前统一视觉规划 v0.2](../../../项目规划/统一主视觉与设计方向-v0.2.md)
''',encoding='utf-8')
print(OUT)
