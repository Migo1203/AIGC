from pathlib import Path
from PIL import Image,ImageFilter,ImageChops
from html import escape
import base64,json,shutil,hashlib,xml.etree.ElementTree as ET
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集03品牌故事_展示规划_V01_20261108'
A=O/'03_参考素材';E=O/'02_可编辑SVG';P=O/'01_示意图与预览';L=O/'04_过程记录'
W,H=1600,7160
data=lambda p,mime:'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
font=R/'work/ned-banner-assets/DMSans-VF.ttf'
for n in ['DMSans-VF.ttf','DM-Sans-OFL.txt']:shutil.copy2(font.parent/n,E/n)
master=Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png').convert('RGB')
pad=48;period=2*(master.height-1);raw=Image.new('RGB',(W,H+2*pad))
for yy in range(-pad,H+pad):
 q=(1200+21920+yy)%period;q=q if q<master.height else period-q
 raw.paste(master.crop((0,q,W,q+1)),(0,yy+pad))
bg=Image.blend(raw.filter(ImageFilter.GaussianBlur(15)),Image.new('RGB',raw.size,(247,240,229)),.26).crop((0,pad,W,pad+H))
previous=Image.open(R/'outputs/NED_作品集02_高级A+_展示_V04_修订V02_完整手机_20261108/03_原始素材/连续暖墙_高级A+展示_完整手机.png').convert('RGB')
last=previous.crop((0,17279,W,17280)).load();pixels=bg.load();delta=[tuple(last[x,0][c]-pixels[x,0][c] for c in range(3)) for x in range(W)]
for y in range(120):
 f=(1-y/120)**2
 for x in range(W):pixels[x,y]=tuple(max(0,min(255,round(pixels[x,y][c]+delta[x][c]*f))) for c in range(3))
bg.save(A/'连续暖墙_品牌故事规划.png')
assert ImageChops.difference(previous.crop((0,17279,W,17280)),bg.crop((0,0,W,1))).getbbox() is None
parts=[];counter=0;placements=[]
def text(s,x,y,size=24,color='#403a32',weight=400):
 global counter
 counter+=1;parts.append(f'<text id="label-{counter}" x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(s)}</text>')
def image(p,x,y,w,h,key):
 mime='image/jpeg' if p.suffix.lower()=='.jpg' else 'image/png'
 parts.append(f'<g id="{key}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f5efe5" filter="url(#shadow)"/><image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="{data(p,mime)}"/><rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" fill="none" stroke="#fff8ee" stroke-opacity=".75"/></g>')
 placements.append(dict(key=key,x=x,y=y,w=w,h=h,file=p.name))
def section(n,title,y):
 text(n,80,y,17,'#735f4b',500);text(title,80,y+54,34,weight=500)
text('03 / SELECTED WORK',80,82,17,weight=500)
text('PLAN V01 · 待审阅',1280,82,18)
text('品牌故事 / 从产品走向生活方式',76,170,48,weight=700)
text('沿用连续暖墙，完整展示桌面整体与手机四个故事状态。',80,231,25)
hero=Image.open(A/'B00_电脑背景.jpg');heroH=1440*hero.height/hero.width
image(A/'B00_电脑背景.jpg',80,294,1440,heroH,'brand-atmosphere')
text('A / 品牌氛围开场',80,979,22,'#735f4b',500)
text('让背景中的产品、家具与窗光先被看见；不叠加功能参数。',80,1017,23)
section('B / DESKTOP · THE COMPLETE STORY','桌面整体：品牌介绍 → 审美 → 日常 → 问答',1130)
image(A/'桌面整体_规划参考.png',80,1238,1440,625*1440/1464,'desktop-complete')
text('背景是环境，四张卡片承载故事；作品集模拟排版，非Amazon后台截图。',80,1906,23)
text('规划参考已替换为现有高清重绘Logo；正式制作时重排原生文字。',80,1946,22,'#735f4b')
section('C / MOBILE · ALL FOUR STATES','手机四个状态，按阅读顺序完整下排',2070)
text('四张卡片均展示；不只选两张示例，不将电脑横图拉成竖图。',80,2184,24)
states=['B01 / 品牌介绍 · Meet NED Collections','B02 / 审美与造型 · Simple, with Character','B03 / 日常生活 · Moments That Feel Like Home','B04 / 品牌问答 · 三组问答完整显示']
y=2280
for i,label in enumerate(states):
 text(label,500,y,22,'#735f4b',500)
 image(A/f'手机状态0{i+1}_规划参考.png',500,y+34,600,625*600/390,f'mobile-state-{i+1}')
 y+=1100
section('D / PRODUCTION NOTES · 仅供本轮审阅','正式制作前，重点落实三件事',6815)
text('01 统一可编辑文字与Logo对象；照片继续保留为位图。',80,6924,24)
text('02 检查B02／B03底座暗边、产品比例与全部问答；不沿产品轮廓描边。',80,6968,24)
text('03 维持桌面全貌＋手机四状态；英文沿用现稿，品牌事实保留来源。',80,7012,24)
text('本图为展示规划示意，非正式03展示成品；素材V01未在本轮被视为已终审。',80,7090,20,'#735f4b')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><title>03品牌故事作品集展示规划V01</title><desc>待审阅的单列长图规划。章节标题和规划说明为可编辑文字；桌面与手机内容为已有HTML重新渲染的位图参考，不宣称内部文字可编辑。</desc><defs><style>@font-face{{font-family:DM;src:url({data(font,'font/ttf')})}}text{{font-family:DM,"Microsoft YaHei",sans-serif}}</style><filter id="shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs><image id="wall" x="0" y="0" width="1600" height="{H}" href="{data(A/'连续暖墙_品牌故事规划.png','image/png')}"/>'''+''.join(parts)+'</svg>'
(E/'03_品牌故事_展示规划示意_V01.svg').write_text(svg,encoding='utf-8')
ET.fromstring(svg)
(L/'版式与素材记录.json').write_text(json.dumps({'size':[W,H],'status':'规划示意，待审阅','placements':placements,'backgroundSeamMaxDifference':0,'assets':[dict(file=p.name,size=list(Image.open(p).size),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in A.iterdir() if p.is_file()],'editableScope':'外层标题和规划说明可编辑；图文参考为位图'},ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(Path(__file__),L/Path(__file__).name)
shutil.copy2(R/'work/prepare_ned_brand_showcase_plan.cjs',L/'prepare_ned_brand_showcase_plan.cjs')
print(json.dumps({'size':[W,H],'mobileStates':4,'images':len(placements),'textObjects':counter},ensure_ascii=False))
