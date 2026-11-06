from pathlib import Path
from PIL import Image,ImageCms,ImageFilter
import numpy as np,json,base64,shutil,hashlib,re
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106';E=O/'可编辑源稿';E.mkdir(parents=True,exist_ok=True)
S=R/'work/ned-listing-assets';REF=R/'work/ned-revision-refs';ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
names=['00_主图_近白底_V01.png','01_产品展示_V02.png','02_旋钮操作_V02.png','03_光色调节_V01.png','04_夜间无线续航_V02.png','05_尺寸材质_V02.png','06_户外使用_V02.png','07_多场景使用_V02.png']
assets=[(REF if i==3 else S)/n for i,n in enumerate(names)]
html=(REF/'Listing页面模拟.html').read_text(encoding='utf-8')
for i,p in enumerate(assets):
 old='03_光色调节_V02.png' if i==3 else p.name
 html=re.sub(r'src="[^"]*/'+re.escape(old)+'"','src="'+p.as_uri()+'"',html)
(E/'Listing_V01_仅同步03缩略图.html').write_text(html,encoding='utf-8')
H=4640
master=Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png').convert('RGB')
a=np.asarray(master);idx=np.arange(H)+1200;period=2*(a.shape[0]-1);idx=idx%period;idx=np.where(idx<a.shape[0],idx,period-idx)
orig=a[idx];soft=np.asarray(Image.fromarray(orig).filter(ImageFilter.GaussianBlur(15))).astype(float)
y=np.arange(H)[:,None,None];ramp=np.clip(y/380,0,1);ramp=ramp*ramp*(3-2*ramp)
base=orig.astype(float)*(1-ramp)+soft*ramp
alpha=.26*ramp
bg=np.clip(base*(1-alpha)+np.array([247,240,229])[None,None,:]*alpha,0,255).astype('uint8')
Image.fromarray(bg).save(E/'连续背景_提亮柔焦光影_V03.png',icc_profile=ICC)
def data(p,m):return 'data:'+m+';base64,'+base64.b64encode(p.read_bytes()).decode()
def t(v,x,y,size=22,weight=400):return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="#403a32">{v}</text>'
def image(p,id,x,y,w,h):return f'<image id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" href="{data(p,"image/png")}"/>'
def build():
 listing=E/'Listing_V01_同步选图.png';assert listing.exists()
 li=Image.open(listing);lh=1440*li.height/li.width
 s=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="{H}" viewBox="0 0 1600 {H}"><title>NED商品图展示V04</title><defs><style>@font-face{{font-family:DM;src:url('{data(R/'work/ned-banner-assets/DMSans-VF.ttf','font/ttf')}')}}text{{font-family:DM,'Microsoft YaHei',sans-serif}}</style><filter id="card-shadow" x="-12%" y="-12%" width="124%" height="130%" color-interpolation-filters="sRGB"><feDropShadow dx="0" dy="9" stdDeviation="12" flood-color="#4a3525" flood-opacity=".16"/></filter></defs>''',image(E/'连续背景_提亮柔焦光影_V03.png','background',0,0,1600,H),t('01 / SELECTED WORK',80,82,17,500),t('商品图 / Listing 展示',76,170,53,700),t('从商品识别，到功能理解与生活场景。',80,231,25),t('Listing V01 · 商品图精选',1240,82,18)]
 s += [f'<rect x="80" y="294" width="1440" height="{lh}" fill="#fff" filter="url(#card-shadow)"/>',image(listing,'listing-v01',80,294,1440,lh)]
 s += [t('商品图组',80,1612,34,500),t('完整展示 · 按信息顺序展开',1080,1612,21)]
 placements=[]
 for i,p in enumerate(assets):
  x=120+(i%2)*700;y=1660+(i//2)*700
  s += [f'<rect x="{x}" y="{y}" width="660" height="660" fill="#fff" filter="url(#card-shadow)"/>',image(p,'G%02d'%i,x,y,660,660),f'<rect x="{x+.5}" y="{y+.5}" width="659" height="659" fill="none" stroke="#fff8ee" stroke-opacity=".75"/>']
  placements.append({'id':'G%02d'%i,'file':p.name,'rect':[x,y,660,660],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 s += [t('主图沿用 V01；03 光色调节采用 V01；其余六张辅图采用 V02。',120,4520,20),'</svg>']
 (E/'01_商品图展示_V04_可编辑.svg').write_text('\n'.join(s),encoding='utf-8')
 (O/'制作记录.json').write_text(json.dumps({'size':[1600,H],'status':'本地审阅；未推送','listing':'Listing V01原HTML布局及全文，仅同步03缩略图至V01','assets':placements,'background':'获准V02母版后半段起接，垂直镜向连续延展；15px柔焦；暖白提亮覆盖从0渐至26%；未覆盖获准母版','depth':'外层卡片9px偏移/12px模糊/16%暖深色阴影，1px浅边；不改原图','decision_03':'V01与V02同属暖中性、沙色产品、自然材质、黑色字体体系，木石材差异可接受，采用V01，无需重生图','git_push':False},ensure_ascii=False,indent=2),encoding='utf-8')
 shutil.copy2(R/'work/ned-banner-assets/DM-Sans-OFL.txt',E/'DM-Sans-OFL.txt');shutil.copy2(Path(__file__),E/Path(__file__).name)
if __name__=='__main__':
 import sys
 if '--compose' in sys.argv:build()
