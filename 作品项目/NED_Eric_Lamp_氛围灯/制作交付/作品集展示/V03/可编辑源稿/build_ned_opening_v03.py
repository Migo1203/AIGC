from pathlib import Path
from PIL import Image, ImageCms, ImageFilter
import numpy as np
import base64, json, shutil

ROOT=Path('D:/WLQ/AIGC作品集');SRC=ROOT/'work/ned-banner-assets'
PREV=ROOT/'outputs/NED_作品集开篇_V02_4x3_20261106/可编辑源稿'
BG=ROOT/'outputs/NED_作品集连续背景_V02_20261106'
OUT=ROOT/'outputs/NED_作品集开篇_V03_连续背景_20261106'
EDIT=OUT/'可编辑源稿';EDIT.mkdir(parents=True,exist_ok=True)
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()

def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
def imtag(p,x,y,w,h,id):return f'<image id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/png")}"/>'
def text(t,x,y,size=24,weight=400,color='#302d28',cn=True,extra=''):
 return f'<text class="{"cn" if cn else "en"}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{t}</text>'
def base(title):return [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200"><title>{title}</title>
<defs><style>@font-face{{font-family:DM;src:url('{data(SRC/'DMSans-VF.ttf','font/ttf')}')}}.en{{font-family:DM,sans-serif}}.cn{{font-family:'Microsoft YaHei',sans-serif}}</style></defs>''']
def line(y):return f'<path d="M884 {y}H1520" stroke="#8c7763" stroke-opacity=".36" stroke-width="1"/>'
def save(s,name):
 s.append('</svg>');(EDIT/name).write_text('\n'.join(s),encoding='utf-8')
def crop(name,box,size,outname):
 p=EDIT/outname;Image.open(SRC/name).convert('RGB').crop(box).resize(size,Image.Resampling.LANCZOS).save(p,icc_profile=ICC);return p

# Keep the approved master pixel-for-pixel for strategy and next results section.
wall=Image.open(BG/'NED_连续墙面背景_V02_1600x2400.png').convert('RGB')
arr=np.asarray(wall)
extension=arr[:1200][::-1].copy()
full=np.concatenate([extension,arr],axis=0)
Image.fromarray(full).save(EDIT/'全篇背景_封面延展加既定母版_1600x3600.png',icc_profile=ICC)
Image.fromarray(arr[:1200]).save(EDIT/'策略页_连续背景.png',icc_profile=ICC)
Image.fromarray(arr[1200:]).save(OUT/'成果速览_下一屏背景_1600x1200.png',icc_profile=ICC)

# The whole lamp ends above the blend. Only environment/table texture fades.
scene=crop('P01_PC.png',(355,0,1783,803),(1600,900),'封面_原场景裁切.png')
scene_arr=np.asarray(Image.open(scene),dtype=np.float32)
scene_extended=np.concatenate([scene_arr,np.repeat(scene_arr[-1:],300,axis=0)],axis=0)
y=np.arange(1200,dtype=np.float32)[:,None,None]
environment_blur=np.asarray(Image.fromarray(scene_extended.astype(np.uint8)).filter(ImageFilter.GaussianBlur(48)),dtype=np.float32)
e=np.clip((y-800)/100,0,1);e=e*e*(3-2*e)
scene_extended=scene_extended*(1-e)+environment_blur*e
t=np.clip((y-820)/240,0,1)
smooth=t*t*(3-2*t)
cover=np.clip(scene_extended*(1-smooth)+extension.astype(np.float32)*smooth,0,255).astype(np.uint8)
Image.fromarray(cover).save(EDIT/'封面_场景至墙面过渡.png',icc_profile=ICC)
mask=Image.fromarray(np.repeat((smooth[:,0,:]*255).astype(np.uint8)[:,None,:],1600,axis=1).squeeze())
mask.save(EDIT/'封面_环境过渡蒙版.png')
s=base('NED Eric｜连续背景封面 V03')
s += [imtag(EDIT/'封面_场景至墙面过渡.png',0,0,1600,1200,'scene-to-approved-wall'),
 f'<image id="existing-ned-wordmark" x="80" y="42" width="98" height="56" href="{data(ROOT/"outputs/NED_Logo_原样重绘_20261105/NED_原样重绘_黑_紧边.svg","image/svg+xml")}"/>',
 text('AMAZON E-COMMERCE DESIGN',219,79,17,500,cn=False,extra='letter-spacing="1.8"'),
 text('自发概念项目 · AI 辅助设计',84,601,18,color='#51493f'),
 text('Eric.',74,318,156,500,cn=False,extra='letter-spacing="-7"'),
 text('无线氛围灯',82,427,43),text('电商视觉系统',82,492,43),
 text('商品图 / A+ 内容 / Banner',84,551,24)]
save(s,'01_NED_Eric_封面_V03_4x3_可编辑.svg')

dining=EDIT/'策略_餐桌场景.png';shutil.copy2(PREV/'策略_餐桌场景.png',dining)
detail=EDIT/'策略_产品细节.png';shutil.copy2(PREV/'策略_产品细节.png',detail)
day=crop('P01_PC.png',(965,100,1695,600),(258,177),'策略_日间证据.png')
night=crop('P05_Bed_PC.png',(1000,135,1730,635),(258,177),'策略_夜间证据.png')
s=base('NED Eric｜背景与视觉策略 V03')
s += [imtag(EDIT/'策略页_连续背景.png',0,0,1600,1200,'approved-wall-upper-half'),
 text('PROJECT BRIEF / DESIGN APPROACH',82,97,18,500,cn=False,extra='letter-spacing="2"'),
 text('让氛围被感受，',78,200,53,700),text('让产品被看懂。',78,276,53,700),
 text('以 NED Eric 无线氛围灯为对象，探索面向',82,361,25,color='#51493f'),
 text('亚马逊美国站的电商视觉：从商品识别、',82,406,25,color='#51493f'),
 text('卖点解释到场景导流，保持一致的表达。',82,451,25,color='#51493f'),
 imtag(dining,80,548,720,510,'dining-evidence'),
 text('同一盏灯，贯穿产品信息与生活场景。',82,1103,20,color='#51493f'),
 text('视觉策略',884,102,25,500),line(135),
 text('01',884,193,24,500,color='#715b46',cn=False),
 text('暖中性基调，昼夜有变化',948,193,29,500),
 text('日光、夜间蓝灰与户外暮色拉开层次，',948,242,23,color='#51493f'),
 text('保持沙色灯体与自然材质的统一。',948,279,23,color='#51493f'),
 imtag(day,948,308,258,177,'daylight-evidence'),
 imtag(night,1228,308,258,177,'night-evidence'),
 text('日间窗光',948,515,18,color='#51493f'),text('夜间暖光',1228,515,18,color='#51493f'),line(551),
 text('02',884,610,24,500,color='#715b46',cn=False),
 text('产品优先，信息清楚',948,610,29,500),
 text('完整轮廓先建立识别，',948,667,23,color='#51493f'),
 text('近景与动作分组解释功能；',948,704,23,color='#51493f'),
 text('人物和道具辅助理解。',948,741,23,color='#51493f'),
 imtag(detail,1332,642,172,226,'complete-product-evidence'),line(895),
 text('03',884,952,24,500,color='#715b46',cn=False),
 text('按购物问题组织内容',948,952,29,500),
 text('商品图',948,1010,23,500),text('识别产品 · 解释卖点',1110,1010,22,color='#51493f'),
 text('A+ 内容',948,1053,23,500),text('展开细节 · 理解体验',1110,1053,22,color='#51493f'),
 text('Banner',948,1096,24,500,cn=False),text('建立认知 · 场景导流',1110,1096,22,color='#51493f')]
save(s,'02_NED_Eric_背景与视觉策略_V03_4x3_可编辑.svg')
shutil.copy2(SRC/'DM-Sans-OFL.txt',EDIT/'DM-Sans-OFL.txt')
shutil.copy2(Path(__file__),EDIT/Path(__file__).name)
record={'date':'2026-11-06','version':'V03','status':'待审阅', 'page_size':[1600,1200],
 'cover_crop':[355,0,1783,803],'scene_rendered':[1600,900],
 'method':'Existing AI scene reuse, deterministic crop, environmental crossfade, editable SVG typography; no new image generation',
 'top_information':'No solid header; compact brand content within approximately 110px rather than previous 180px band',
 'transition':{'start_y':820,'end_y':1060,'curve':'smoothstep','target':'approved wall V02 upper 1200 rows reversed vertically'},
 'background_coordinates':{'cover_extension':[0,1200],'strategy_approved_master':[0,1200],'next_overview_approved_master':[1200,2400]},
 'invariants':'Complete lamp and contact surface above transition remain unblended. Existing approved background unchanged for strategy and results.',
 'typefaces':'DM Sans embedded with OFL; Microsoft YaHei local reference, not distributed',
 'sources':['P01_PC.png','P05_Dining_PC.png','P05_Bed_PC.png','Existing ned. contour redraw','Approved wall background V02'],
 'limitations':'Scene interpolated about 1.12×; bottom environment extended before blending, not newly photographed; 4:3 layout and continuity mockup are portfolio presentation.'}
(OUT/'制作记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'README.md').write_text('''# NED Eric｜作品集开篇 V03：连续背景

2026-11-06。两张均为 1600×1200（4:3），新试排待审阅，V01/V02 保留。

## 连续阅读预览

![封面至策略连续预览](封面至策略_连续阅读预览.jpg)

## 封面

![封面](01_NED_Eric_封面_V03_1600x1200.jpg)

[PNG](01_NED_Eric_封面_V03_1600x1200.png) · [可编辑 SVG](可编辑源稿/01_NED_Eric_封面_V03_4x3_可编辑.svg)

## 简短背景与视觉策略

![策略](02_NED_Eric_背景与视觉策略_V03_1600x1200.jpg)

[PNG](02_NED_Eric_背景与视觉策略_V03_1600x1200.png) · [可编辑 SVG](可编辑源稿/02_NED_Eric_背景与视觉策略_V03_4x3_可编辑.svg)

## 变化与边界

- 封面移除原 180px 纯色顶部栏，品牌信息直接叠入墙面，收至顶部约 110px 内容区。
- 采用已有场景重新裁切，灯体及底座完整。下方在主体之外的桌面/环境区渐变至用户指定的连续墙面，避免硬切至策略页。
- 策略页采用既定背景 V02 的上半段，不重新调色或重复贴图；成果速览继续取下半段。另提供下一屏背景供后续排版。
- V03 策略改为“暖中性基调，昼夜有变化”“产品优先，信息清楚”“按购物问题组织内容”，与新版视觉规划一致，加入日夜证据图。
- 此为展示层的场景至背景过渡，不代表桌面实际变成墙面。仅环境进行渐变，产品及承托接触区不渐隐；底部环境有延展，不是新拍摄。
- 原场景约 1.12 倍插值，不增加真实细节；没有新一轮 AI 生图。
- SVG 文字可编辑、摄影为嵌入位图；附 DM Sans OFL，中文引用本机微软雅黑，跨平台缺字体需替换。
- 脚本保留操作记录，路径须按运行环境调整。

[制作记录](制作记录.json) · [连续背景 V02](../共享背景/V02/README.md) · [当前统一视觉规划 v0.2](../../../项目规划/统一主视觉与设计方向-v0.2.md)
''',encoding='utf-8')
print(str(OUT))
