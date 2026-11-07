from pathlib import Path
from PIL import Image, ImageChops, ImageStat
import json, shutil, hashlib, base64, xml.etree.ElementTree as ET, re
R=Path('D:/WLQ/AIGC作品集');build=json.loads((R/'work/ned-aplus-showcase-v04-full-mobile-build.json').read_text(encoding='utf-8'));O=Path(build['output']);P=O/'01_成品与预览';E=O/'02_可编辑SVG';L=O/'04_过程记录'
report=json.loads((R/'work/ned-aplus-showcase-v04-full-mobile-render-check.json').read_text(encoding='utf-8'))
assert not any(report[k] for k in ['failedImages','overflow','overlaps','clipped','errors'])
assert report['textCount']==build['textObjects']==135
for a,b in zip(build['placements'],report['modules']):
 assert a['key']==b['key']
 for k in ['x','y','w','h']:assert abs(a[k]-b[k])<.01,(a['key'],k)
 assert a['textObjects']==b['texts']
for source in build['sourceSvgs']:
 assert hashlib.sha256((E/'模块源稿'/source['file']).read_bytes()).hexdigest()==source['sha256']
ns='{http://www.w3.org/2000/svg}'
root=ET.parse(E/'02_高级A+展示_V04_修订V02_可编辑.svg').getroot()
ids={e.attrib['id'] for e in root.iter() if 'id' in e.attrib}
for placement in build['placements']:
 group=next(e for e in root.iter(ns+'g') if e.attrib.get('data-module')==placement['key'])
 hashes=[]
 for im in group.iter(ns+'image'):
  hashes.append(hashlib.sha256(base64.b64decode(im.attrib['href'].split(',',1)[1])).hexdigest())
 assert hashes==placement['imageHashes'],placement['key']
for el in root.iter():
 for val in el.attrib.values():
  for ref in re.findall(r'url\(#([^)]+)\)',val):assert ref in ids,ref
 assert el.tag!=ns+'script'
png=P/(build['name']+'.png')
if report.get('tiles'):
 stitched=Image.new('RGB',tuple(build['size']))
 for tile in report['tiles']:
  im=Image.open(tile['file']).convert('RGB');pad=tile.get('pad',0);assert im.size==(1600,tile['height']+pad*2);stitched.paste(im.crop((0,pad,1600,pad+tile['height'])),(0,tile['y']))
 stitched.save(png)
long=Image.open(png).convert('RGB')
assert long.size==tuple(build['size'])
long.save(P/(build['name']+'.jpg'),quality=95,subsampling=0)
long.resize((800,long.height//2),Image.Resampling.LANCZOS).save(P/'02_高级A+展示_V04_修订V02_缩略.jpg',quality=93)
old=Image.open(R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106/01_商品图展示_V04_1600x4640.png').convert('RGB')
joint=Image.new('RGB',(1600,4640+long.height));joint.paste(old,(0,0));joint.paste(long,(0,4640));joint.save(P/'商品图至高级A+_完整连续预览_修订V02.jpg',quality=94,subsampling=0)
detail=Image.new('RGB',(1600,1900));detail.paste(old.crop((0,3940,1600,4640)),(0,0));detail.paste(long.crop((0,0,1600,1200)),(0,700));detail.save(P/'商品图至高级A+_衔接局部_修订V02.jpg',quality=94,subsampling=0)
placements={p['key']:p for p in build['placements']}
for label,first,last in [('操作','P03A_PC','P03C_PC'),('场景','P04A_PC','P04C_PC'),('收束','P05_PC','P06_PC'),('手机','P01_Mobile','P06_Mobile')]:
 a=placements[first];b=placements[last];crop=long.crop((0,int(a['y']-100),1600,int(b['y']+b['h']+50)))
 crop.resize((1000,round(crop.height*1000/1600)),Image.Resampling.LANCZOS).save(R/f'work/ned-aplus-showcase-v04-full-mobile-{label}-review.jpg',quality=95)
# Inspect enlarged contact edges after the actual SVG render, alongside the V03 preview.
basekeys=['P02_PC','P04A_PC','P04B_PC','P04C_PC','P05_PC','P04A_Mobile','P04B_Mobile','P04C_Mobile','P05_Mobile']
sheet=Image.new('RGB',(1200,len(basekeys)*210),'#f6f0e7')
from PIL import ImageDraw
draw=ImageDraw.Draw(sheet)
for i,key in enumerate(basekeys):
 m=placements[key];x,y,w,h=[m[k] for k in ['x','y','w','h']]
 if key=='P02_PC':box=(x+w*.20,y+h*.69,x+w*.48,y+h*.94)
 elif 'Mobile' in key:box=(x+w*.35,y+h*.36,x+w*.79,y+h*.64)
 else:box=(x+w*.38,y+h*.66,x+w*.98,y+h*.92)
 cropped=long.crop(tuple(round(v) for v in box));cropped.thumbnail((1150,165))
 sheet.paste(cropped,(20,i*210+30));draw.text((20,i*210+9),key,fill='#403a32')
sheet.save(R/'work/ned-aplus-showcase-v04-full-mobile-contact-bases-review.jpg',quality=96)
for f in O.rglob('*'):
 if f.suffix.lower() in ['.png','.jpg']:
  with Image.open(f) as im:im.verify()
for doc in [O/'README.md',O/'使用说明_修订V02.md']:
 for link in re.findall(r'\]\(([^)]+)\)',doc.read_text(encoding='utf-8')):assert (O/link).exists(),link
log=L/'制作与检查记录_修订V02.md'
c=log.read_text(encoding='utf-8').replace('在出图后补充实际检查结果。',
 f'已用Chrome渲染整页SVG，21个图片引用全部解码，135个文字对象无越界、无可见字形碰撞，所有嵌套模块文字未越出原viewBox。字体行框有9处相邻标题行重叠，进一步按实际字形测量无碰撞；未因此改动原模块的行距。21个模块实际渲染位置与制作清单一致，按同一中轴纵向排列。渐变/滤镜引用目标均存在，所有ID唯一；原模块源稿SHA256与V03一致，嵌入照片/Logo字节逐一匹配，英文内容不变。PNG为该SVG同版渲染，JPG由此PNG导出。完整商品图→A+连续预览为1600×{4640+long.height}。README相对链接目标存在；本轮PNG/JPG全部可解码。')
log.write_text(c,encoding='utf-8')
for name in ['render_ned_aplus_showcase_v04_full_mobile.cjs','finish_ned_aplus_showcase_v04_full_mobile.py']:shutil.copy2(R/'work'/name,L/name)
print(json.dumps({'size':long.size,'sourceModules':len(build['sourceSvgs']),'nativeTextObjects':report['textCount'],'rasterReferences':report['images'],'combinedSize':[1600,4640+long.height],'files':len([p for p in O.rglob('*') if p.is_file()]),'totalMB':round(sum(p.stat().st_size for p in O.rglob('*') if p.is_file())/1024/1024,1),'maxMB':round(max(p.stat().st_size for p in O.rglob('*') if p.is_file())/1024/1024,1)},ensure_ascii=False))
