from pathlib import Path
from PIL import Image,ImageFilter,ImageChops
from html import escape
import base64,hashlib,json,shutil,xml.etree.ElementTree as ET
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集04Banner系统_展示规划_V01_20261108'
P=O/'01_示意图与预览';E=O/'02_可编辑SVG';A=O/'03_参考素材';L=O/'04_过程记录'
for d in [P,E,A/'图片素材',A/'图文参考',L]:d.mkdir(parents=True,exist_ok=True)
S=R/'outputs/NED_Banner_V02_20261105';F=R/'work/ned-banner-assets/DMSans-VF.ttf'
for n in ['DMSans-VF.ttf','DM-Sans-OFL.txt']:shutil.copy2(F.parent/n,E/n)
sources=[]
for f in (S/'图片素材').glob('*.jpg'):
 shutil.copy2(f,A/'图片素材'/f.name);im=Image.open(f)
 sources.append(dict(file=f.name,size=list(im.size),mode=im.mode,bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
assert len(sources)==6
proofs=['BN01_品牌组件与页头示意.png','BN01_中央70百分比裁切检查.png','BN02_场景导流_图文预览.png','BN02_手机图文适配示意.png','BN03_REC_广告图文预览.png']
for n in proofs:shutil.copy2(S/'图文预览'/n,A/'图文参考'/n)
W,H=1600,7040;master=Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png').convert('RGB');pad=48;period=2*(master.height-1);raw=Image.new('RGB',(W,H+2*pad))
for yy in range(-pad,H+pad):
 q=(1200+28520+yy)%period;q=q if q<master.height else period-q
 raw.paste(master.crop((0,q,W,q+1)),(0,yy+pad))
bg=Image.blend(raw.filter(ImageFilter.GaussianBlur(15)),Image.new('RGB',raw.size,(247,240,229)),.26).crop((0,pad,W,pad+H))
prev=Image.open(R/'outputs/NED_作品集03_品牌故事_展示_V04_20261108/03_原始素材/连续暖墙_品牌故事展示.png').convert('RGB');last=prev.crop((0,6599,W,6600)).load();pix=bg.load();delta=[tuple(last[x,0][c]-pix[x,0][c] for c in range(3)) for x in range(W)]
for y in range(120):
 f=(1-y/120)**2
 for x in range(W):pix[x,y]=tuple(max(0,min(255,round(pix[x,y][c]+delta[x][c]*f))) for c in range(3))
bg.save(A/'连续暖墙_Banner系统规划.png');assert ImageChops.difference(prev.crop((0,6599,W,6600)),bg.crop((0,0,W,1))).getbbox() is None
data=lambda p,mime:'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
parts=[];texts=0;placements=[]
def text(s,x,y,size=24,weight=400,color='#403a32'):
 global texts
 texts+=1;parts.append(f'<text id="label-{texts}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(s)}</text>')
def section(k,title,y):text(k,80,y,17,500,'#735f4b');text(title,80,y+54,34,500)
def image(p,x,y,w,key):
 im=Image.open(p);h=w*im.height/im.width;mime='image/jpeg' if p.suffix=='.jpg' else 'image/png'
 parts.append(f'<g id="{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f5efe5" filter="url(#shadow)"/><image x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,mime)}" preserveAspectRatio="xMidYMid meet"/><rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" fill="none" stroke="#fff8ee" stroke-opacity=".75"/></g>')
 placements.append(dict(key=key,x=x,y=y,w=w,h=h,file=p.relative_to(O).as_posix()))
text('04 / SELECTED WORK',80,82,17,500);text('BANNER PLAN V01 · 待审阅',1180,82,17)
text('Banner 系统 / 不同入口，同一种光',76,170,48,700)
text('从认识 Eric，到餐桌导流，再到夜间广告。',80,231,25)
section('A / STORE HEADER · BRAND RECOGNITION','店铺页头：先认识 Eric',310)
image(A/'图文参考/BN01_品牌组件与页头示意.png',80,420,1440,'bn01-complete')
text('Meet Eric. / Cordless light. Everyday warmth.',80,850,25,500)
text('品牌栏与Hero一起展示；素材保持横幅比例。',80,893,23)
text('补充检查 / 原图中央70%裁切，仅用于观察文字与灯体是否保留',260,970,22,500,'#735f4b')
image(A/'图文参考/BN01_中央70百分比裁切检查.png',260,1006,1080,'bn01-central-crop')
text('此裁切不是新增手机版，也不是后台实机预览。',260,1362,22,color='#735f4b')
section('B / IN-STORE DISCOVERY · TABLE SETTING','餐桌导流：让场景带出一个入口',1480)
image(A/'图文参考/BN02_场景导流_图文预览.png',80,1588,1440,'bn02-desktop')
text('手机图文适配 / 独立构图，图片与入口相邻',500,2412,22,500,'#735f4b')
image(A/'图文参考/BN02_手机图文适配示意.png',500,2446,600,'bn02-mobile')
text('Set the table. Keep the glow. / Explore Eric',500,3290,22,500)
section('C / REC ADVERTISING · EVENING LIGHT','REC 广告：同一主题，三种比例',3430)
text('Evening light, without the cord.',80,3540,25,500)
text('横版 / 用完整图文预览说明图片、品牌与标题的关系',200,3610,22,500,'#735f4b')
image(A/'图文参考/BN03_REC_广告图文预览.png',200,3644,1200,'bn03-landscape')
text('方版 / 无字图片，1200×1200',500,4590,22,500,'#735f4b')
image(A/'图片素材/BN03_REC_方_1200x1200.jpg',500,4624,600,'bn03-square')
text('竖版 / 无字图片，900×1600',500,5350,22,500,'#735f4b')
image(A/'图片素材/BN03_REC_竖_900x1600.jpg',500,5384,600,'bn03-portrait')
section('D / EXECUTION NOTES · 仅供规划审阅','制作前，落实三个检查重点',6610)
text('01 三主题、六份适配全部呈现；横、方、竖不挤成一排小缩略图。',80,6718)
text('02 复核餐桌文字对比、底座暗边与比例；保留合理接触阴影。',80,6762)
text('03 正式展示保留可编辑文字／Logo；REC无字素材与品牌字段分开。',80,6806)
text('本图是04展示段规划，非正式成品；V02原素材待审阅，尚未实际投放。',80,6910,21,color='#735f4b')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>04 Banner系统作品集展示规划V01</title><desc>规划示意，待审阅。外层文字可编辑；内部图文参考为Banner V02原有预览位图，不宣称截图内文字可改。</desc><defs><style>@font-face{{font-family:DM;src:url({data(F,"font/ttf")})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style><filter id="shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs><image id="wall" x="0" y="0" width="1600" height="{H}" href="{data(A/"连续暖墙_Banner系统规划.png","image/png")}"/>'+''.join(parts)+'</svg>'
(E/'04_Banner系统_展示规划示意_V01.svg').write_text(svg,encoding='utf-8');ET.fromstring(svg)
meta={'size':[W,H],'placements':placements,'sourceAssets':sources,'textObjects':texts,'backgroundSeamMaxDifference':0,'status':'规划示意，待审阅','headlineCharacters':len('Evening light, without the cord.')}
(L/'版式与素材记录.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),L/Path(__file__).name)
print(json.dumps({'size':[W,H],'sourceAssets':len(sources),'frames':len(placements),'textObjects':texts},ensure_ascii=False))
