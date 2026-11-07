from pathlib import Path
from PIL import Image,ImageCms,ImageFont,ImageFilter,ImageOps
from html import escape
import json,base64,shutil,hashlib,xml.etree.ElementTree as ET

R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_高级A+_V03_20261107';G=R/'output/imagegen/NED_Premium_V03_20261107'
A=O/'01_成品与预览/平台纯图素材';P=O/'01_成品与预览/图文预览';E=O/'02_可编辑SVG';LOG=O/'04_过程记录';RAW=O/'03_原始素材/实际生成原图'
RAW.mkdir(exist_ok=True)
FONT=R/'work/ned-banner-assets/DMSans-VF.ttf'
shutil.copy2(FONT,E/'DMSans-VF.ttf');shutil.copy2(FONT.parent/'DM-Sans-OFL.txt',E/'DM-Sans-OFL.txt')
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
def data(p,mime):return 'data:'+mime+';base64,'+base64.b64encode(p.read_bytes()).decode()
fontdata=data(FONT,'font/ttf')
logo=data(R/'outputs/NED_Logo_原样重绘_20261105/NED_原样重绘_黑_紧边.svg','image/svg+xml')
copy={
'P01':dict(title=['A small light for','everyday moments.'],body='A compact, cordless lamp for adjustable ambient light at home.',eyebrow='ERIC TABLE LAMP'),
'P03A':dict(title=['Press.','A simple start.'],body='Press the top knob to switch on or off.',eyebrow='ONE KNOB / POWER'),
'P03B':dict(title=['Turn.','Find your glow.'],body='Turn the knob to dim from 5% to 100%.',eyebrow='ONE KNOB / BRIGHTNESS'),
'P03C':dict(title=['Press & turn.','Warm to neutral.'],body='Press and turn to adjust color temperature continuously from 2700K to 4000K.',eyebrow='ONE KNOB / COLOR TEMPERATURE'),
'P04A':dict(title=['A little light','at the table.'],body='Bring a little ambiance to the table.',eyebrow='DINING'),
'P04B':dict(title=['A quiet','bedside glow.'],body='Up to 8 hours on a full charge. Runtime varies with brightness.',eyebrow='BEDSIDE'),
'P04C':dict(title=['Outdoor','moments.'],body='IP65-rated. Bring indoors after outdoor use.',eyebrow='TERRACE'),
'P05':dict(title=['Small lamp.','Thoughtful form.'],body='Approx. 7.9 in high × 4.3 in diameter\n(20.1 × 11 cm)',eyebrow='COMPACT BY DESIGN'),
}
hotspots=[dict(id='Knob',title='Top knob',body='One top knob controls power, brightness and color temperature.'),dict(id='Finish',title='Sand Cashmere',body='A soft sand-colored finish on the powder-coated aluminum body.')]
faqs=[('How do I adjust the light?','Press the knob for power, turn to dim, and press and turn to change color temperature.'),('How long does it last on a charge?','Up to 8 hours on a full charge, depending on brightness. NED lists a charging time of approximately 6 hours.'),('Can I use it outdoors?','NED lists an IP65 rating and recommends bringing the lamp indoors after outdoor use.')]
selected={'P03B_Mobile':'P03B_Mobile_r2.png','P05_PC':'P05_PC_r3.png','P05_Mobile':'P05_Mobile_r2.png'}
shadow_areas={'P01_PC':(1320,675,1607,710),'P01_Mobile':(825,936,1166,977),'P04A_PC':(780,674,1050,704),'P04A_Mobile':(486,891,777,927),'P04B_PC':(1125,660,1385,690),'P04B_Mobile':(644,860,944,895),'P04C_PC':(1218,688,1415,714),'P04C_Mobile':(816,875,1043,903),'P05_PC':(1410,644,1680,673),'P05_Mobile':(726,867,1015,902)}
def soften_contact(im,key):
 if key not in shadow_areas:return im
 x1,y1,x2,y2=shadow_areas[key];out=im.copy();px=im.load();op=out.load()
 for y in range(y1,y2):
  for x in range(x1,x2):
   c=px[x,y];mx=max(c)
   if mx>=112:continue
   feather=min(1,(x-x1)/5,(x2-1-x)/5,(y-y1)/3,(y2-1-y)/3)
   a=max(0,feather)*((112-mx)/112)**1.15
   op[x,y]=tuple(min(255,round(c[k]+a*(.65*c[k]+15))) for k in range(3))
 return out
assets=[];missing=[]
for sid in copy:
 for v in ['PC','Mobile']:
  key=sid+'_'+v;f=G/selected.get(key,key+'.png')
  if not f.exists():missing.append(key);continue
  derived=O/'03_原始素材/制作素材'/(key+'_底座局部修复合成.png')
  im=Image.open(derived if derived.exists() else f).convert('RGB');size=im.size;target=(1952,800) if v=='PC' else (1440,1080)
  # Aspect-preserving fit removes only the provider's few excess pixels. No stretch.
  im=ImageOps.fit(im,target,method=Image.Resampling.LANCZOS,centering=(.5,.5))
  # Gentle optical low-pass suppresses provider ringing without repainting geometry.
  im=im.filter(ImageFilter.GaussianBlur(.32))
  if not derived.exists():im=soften_contact(im,key)
  im.save(A/(key+'.jpg'),quality=96,subsampling=0,icc_profile=ICC)
  shutil.copy2(f,RAW/f.name)
  assets.append(dict(id=key,source=str((RAW/f.name).relative_to(O)),adoptedSource=str(derived.relative_to(O)) if derived.exists() else str((RAW/f.name).relative_to(O)),size=list(target),originalSize=list(size),file=str((A/(key+'.jpg')).relative_to(O)),sha256=hashlib.sha256((A/(key+'.jpg')).read_bytes()).hexdigest(),processing='aspect-preserving fit; gentle 0.32px low-pass; adopted local API base repair where available, restrained shadow curve only elsewhere; no sharpening',shadowAdjustmentArea=None if derived.exists() else shadow_areas.get(key)))
for f in G.glob('*.png'):
 if not (RAW/f.name).exists():shutil.copy2(f,RAW/f.name)
if missing:print('Pending images: '+', '.join(missing))

def start(w,h,title,bg='#e7dfd2'):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><title>{escape(title)}</title><desc>V03 portfolio concept, pending user review. Photograph is raster; text and annotations remain editable.</desc><defs><style>@font-face{{font-family:DM;src:url({fontdata})}}text{{font-family:DM,Arial,sans-serif}}</style></defs><rect id="base" width="{w}" height="{h}" fill="{bg}"/>']
def txt(s,t,x,y,size=28,col='#302e2a',weight=400,id='text',anchor=None):
 s.append(f'<text id="{id}" x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{col}"'+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(t)+'</text>')
def image(s,p,x,y,w,h,id='photographic-scene'):
 s.append(f'<image id="{id}" x="{x}" y="{y}" width="{w}" height="{h}" href="{data(p,"image/jpeg")}" preserveAspectRatio="xMidYMid meet"/>')
def wrap(t,width,size):
 f=ImageFont.truetype(str(FONT),size);out=[]
 for para in t.split('\n'):
  line=''
  for word in para.split():
   n=(line+' '+word).strip()
   if line and f.getlength(n)>width:out.append(line);line=word
   else:line=n
  if line:out.append(line)
 return out
def block(s,t,x,y,width,size=26,lh=36,col='#302e2a',id='body'):
 lines=wrap(t,width,size)
 for i,l in enumerate(lines):txt(s,l,x,y+i*lh,size,col,id=f'{id}-{i}')
 return y+len(lines)*lh
def line(s,d,id,col='#635448',sw=2):s.append(f'<path id="{id}" d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
def cct(s,x,y,w,h,fs):
 s.append('<defs><linearGradient id="cct-gradient" x1="0%" x2="100%" y1="0%" y2="0%"><stop stop-color="#ffbd69"/><stop offset="100%" stop-color="#f6f4ef"/></linearGradient></defs>')
 s.append(f'<g id="cct-information"><rect id="cct-pill" x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="url(#cct-gradient)"/>')
 txt(s,'2,700K · Warm',x,y+h+fs+13,fs,id='cct-warm-label');txt(s,'4,000K · Neutral',x+w,y+h+fs+13,fs,id='cct-neutral-label',anchor='end');s.append('</g>')
def arrows(s,kind,x,y,scale=1):
 s.append(f'<g id="action-arrows" transform="translate({x} {y}) scale({scale})" fill="none" stroke="#80583c" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">')
 if kind in ['P03A','P03C']:s.append('<path id="press-arrow" d="M0 -63V-19m-10 -12 10 12 10 -12"/>')
 if kind in ['P03B','P03C']:s.append('<path id="turn-arrow" d="M25 -40C74 -64 104 -34 86 0m-1 -16 1 16 16 -6"/>')
 s.append('</g>')
render=[]
def write(key,s,size):
 s.append('</svg>');(E/(key+'.svg')).write_text('\n'.join(s),encoding='utf-8');render.append(dict(id=key,size=list(size)))
for sid,c in copy.items():
 key=sid+'_PC';f=A/(key+'.jpg')
 if not f.exists():continue
 s=start(1952,800,key);image(s,f,0,0,1952,800)
 dark=sid in ['P04B','P04C'];col='#f5efe5' if dark else '#302e2a'
 if sid.startswith('P03'):
  txt(s,c['eyebrow'],100,420,18,id='eyebrow')
  for i,t in enumerate(c['title']):txt(s,t,96,485+i*66,57,weight=500,id=f'headline-{i}')
  block(s,c['body'],100,600,620,26,35,id='body')
  if sid=='P03C':cct(s,100,690,490,18,22)
  elif sid=='P03B':
   txt(s,'5%',100,712,25,id='brightness-low');txt(s,'100%',590,712,25,id='brightness-high',anchor='end');line(s,'M155 704H510','brightness-range','#927b60',3)
  arrows(s,sid,1350,250,.85)
 elif sid=='P01':
  s.append(f'<image id="existing-brand-logo" x="100" y="63" width="108" height="60" href="{logo}"/>')
  txt(s,c['eyebrow'],104,207,19,weight=500,id='eyebrow')
  for i,t in enumerate(c['title']):txt(s,t,100,302+i*77,64,weight=500,id=f'headline-{i}')
  block(s,c['body'],104,458,510,27,38,id='body')
 elif sid=='P05':
  txt(s,c['eyebrow'],104,174,19,weight=500,id='eyebrow')
  for i,t in enumerate(c['title']):txt(s,t,100,270+i*78,65,weight=500,id=f'headline-{i}')
  block(s,c['body'],104,432,620,28,40,id='body')
  line(s,'M1740 105V658M1732 105h16M1732 658h16','height-dimension','#665849')
  txt(s,'20.1 cm',1770,385,23,id='height-label')
  line(s,'M1410 76H1680M1410 68v16M1680 68v16','diameter-dimension','#665849')
  txt(s,'Ø 11 cm',1545,48,22,id='diameter-label',anchor='middle')
 else:
  x=100;y=154
  txt(s,c['eyebrow'],x+4,y,19,col,500,'eyebrow')
  for i,t in enumerate(c['title']):txt(s,t,x,y+98+i*77,65,col,500,f'headline-{i}')
  block(s,c['body'],x+4,y+308,530,28,39,col,id='body')
 write(key,s,(1952,800))
 key=sid+'_Mobile';f=A/(key+'.jpg')
 if not f.exists():continue
 title=' '.join(c['title']);tl=wrap(title,520,36);bl=wrap(c['body'],520,24)
 by=500+len(tl)*44+20;bottom=by+len(bl)*34
 h=bottom+(130 if sid=='P03C' else 62)
 s=start(600,h,key,'#e7dfd2');image(s,f,0,0,600,450)
 for i,t in enumerate(tl):txt(s,t,40,504+i*44,36,weight=500,id=f'headline-{i}')
 block(s,c['body'],40,by,520,24,34,id='body')
 if sid=='P03C':cct(s,40,bottom+15,520,18,22)
 if sid.startswith('P03'):arrows(s,sid,438,132,.48)
 if sid=='P05':
  # Endpoints are visually mapped to this actual mobile image, not an engineering drawing.
  line(s,'M463 86V370M458 86h10M458 370h10','height-dimension','#665849',1.2)
  txt(s,'20.1 cm',475,230,15,id='height-label')
  line(s,'M288 66H435M288 61v10M435 61v10','diameter-dimension','#665849',1.2)
  txt(s,'Ø 11 cm',362,51,15,id='diameter-label',anchor='middle')
 write(key,s,(600,h))

# P02 keeps two real-photo information targets, independent labels and hotspot markers.
s=start(1952,800,'P02 actual photo details');image(s,A/'P02_PC.jpg',0,0,1952,800)
txt(s,'FORM & FINISH',1035,100,19,weight=500,id='eyebrow');txt(s,'A closer look.',1031,164,55,weight=500,id='headline')
txt(s,'Sand Cashmere',700,394,31,weight=500,id='finish-title');block(s,hotspots[1]['body'],700,440,280,23,32,id='finish-body')
txt(s,'Top knob',1035,652,31,weight=500,id='knob-title');block(s,hotspots[0]['body'],1035,698,670,23,32,id='knob-body')
for k,(x,y) in enumerate([(654,361),(1670,240)]):
 s.append(f'<g id="hotspot-{k}"><circle cx="{x}" cy="{y}" r="18" fill="#69563f"/><path d="M{x-6} {y}h12M{x} {y-6}v12" stroke="#f8f2e8" stroke-width="2"/></g>')
write('P02_PC',s,(1952,800))
for c in hotspots:
 key='P02_'+c['id']+'_Mobile';ls=wrap(c['body'],520,24);h=600+len(ls)*34
 s=start(600,h,key);image(s,A/(key+'.jpg'),0,0,600,450);txt(s,c['title'],40,510,36,weight=500,id='headline');block(s,c['body'],40,563,520,24,34,id='body');write(key,s,(600,h))

for v,w in [('PC',1952),('Mobile',600)]:
 x=100 if v=='PC' else 40;y=118 if v=='PC' else 85
 s=start(w,1200,'P06 frequently asked questions','#343d3b');txt(s,'A little more to know.',x,y,53 if v=='PC' else 35,'#f4eee4',500,'headline');y+=100 if v=='PC' else 80
 for k,(q,a) in enumerate(faqs):
  qs=wrap(q,w-x*2,29 if v=='PC' else 25)
  for j,t in enumerate(qs):txt(s,t,x,y+j*35,29 if v=='PC' else 25,'#f4eee4',500,f'question-{k}-{j}')
  y+=len(qs)*35+23
  y=block(s,a,x,y,w-x*2,25 if v=='PC' else 23,34,'#d7d7ca',id=f'answer-{k}')
  y+=44
  if k<2:line(s,f'M{x} {y-15}H{w-x}',f'rule-{k}','#707d75',1)
  y+=26
 h=y+20
 s[0]=s[0].replace('height="1200"',f'height="{h}"').replace(f'{w} 1200',f'{w} {h}')
 write('P06_'+v,s,(w,h))

(LOG/'渲染清单.json').write_text(json.dumps(render,ensure_ascii=False,indent=2),encoding='utf-8')
(LOG/'素材清单.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2),encoding='utf-8')
(LOG/'模块内容.json').write_text(json.dumps(dict(copy=copy,hotspots=hotspots,faq=faqs),ensure_ascii=False,indent=2),encoding='utf-8')
for f in E.glob('P*.svg'):
 root=ET.parse(f).getroot();ids=[e.get('id') for e in root.iter() if e.get('id')];assert len(ids)==len(set(ids)),f
print(json.dumps(dict(sceneAssets=len(assets),realPhotoAssets=3,svg=len(render),missing=missing),ensure_ascii=True))
