from pathlib import Path
from PIL import Image,ImageOps,ImageChops
import json,hashlib,base64,xml.etree.ElementTree as ET,re,shutil

R=Path('D:/WLQ/AIGC作品集');build=json.loads((R/'work/ned-banner-showcase-build.json').read_text(encoding='utf-8'))
O=Path(build['output']);P=O/'01_成品与预览';E=O/'02_可编辑SVG';A=O/'03_原始素材';L=O/'04_过程记录'
report=json.loads((R/'work/ned-banner-showcase-render-check.json').read_text(encoding='utf-8'))
for key in ['overflow','overlaps','failedImages','copyErrors','errors']:assert not report[key],(key,report[key])
for m in report['moduleChecks']:
 for key in ['overflow','overlaps','failedImages']:assert not m[key],(m['key'],key,m[key])
im=Image.open(P/'04_Banner系统展示_V04_1600x6600.png').convert('RGB');assert im.size==(1600,6600)
im.save(P/'04_Banner系统展示_V04_1600x6600.jpg',quality=94,subsampling=0)
ImageOps.contain(im,(800,3300)).save(P/'04_Banner系统展示_V04_缩略.jpg',quality=92)
for f in (P/'逐模块预览').glob('*.png'):
 with Image.open(f) as module:module.convert('RGB').save(f.with_suffix('.jpg'),quality=94,subsampling=0)
previous=Image.open(R/'outputs/NED_作品集03_品牌故事_展示_V04_20261108/01_成品与预览/03_品牌故事展示_V04_1600x6600.png').convert('RGB')
seam=Image.new('RGB',(1600,1850));seam.paste(previous.crop((0,5850,1600,6600)),(0,0));seam.paste(im.crop((0,0,1600,1100)),(0,750));seam.save(P/'品牌故事至Banner系统_衔接局部.jpg',quality=94,subsampling=0)
combined=Image.new('RGB',(1600,35120))
paths=[R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106/01_商品图展示_V04_1600x4640.png',R/'outputs/NED_作品集02_高级A+_展示_V04_修订V02_完整手机_20261108/01_成品与预览/02_高级A+展示_V04_修订V02_1600x17280.png']
y=0
for f in paths:
 p=Image.open(f).convert('RGB');combined.paste(p,(0,y));y+=p.height
combined.paste(previous,(0,y));y+=previous.height;assert y==28520
combined.paste(im,(0,y));combined.save(P/'商品图至Banner系统_完整连续预览.jpg',quality=93,subsampling=0)
for key,box in [('页头',(0,0,1600,1400)),('餐桌',(0,1410,1600,3350)),('REC横方',(0,3370,1600,5290)),('REC竖与页尾',(0,5290,1600,6600))]:im.crop(box).save(R/f'work/ned-banner-showcase-{key}-review.jpg',quality=94)

# Contrast of the actual cream letters against the independently rendered background,
# sampling solid glyph cores rather than antialiased edge pixels.
back=Image.open(R/'work/ned-banner-dining-contrast-background.png').convert('RGB');mask=Image.open(R/'work/ned-banner-dining-contrast-mask.png').convert('L')
lut=[(v/255/12.92 if v/255<=.04045 else ((v/255+.055)/1.055)**2.4) for v in range(256)]
def luminance(rgb):return .2126*lut[rgb[0]]+.7152*lut[rgb[1]]+.0722*lut[rgb[2]]
fg=luminance((255,249,239));ratios=[];bounds=mask.point(lambda x:255 if x<32 else 0).getbbox();assert bounds
bp=back.load();mp=mask.load()
for y in range(bounds[1],bounds[3]):
 for x in range(bounds[0],bounds[2]):
  if mp[x,y]<32:
   lum=luminance(bp[x,y]);ratios.append((max(fg,lum)+.05)/(min(fg,lum)+.05))
ratios.sort();contrast={'sampledGlyphCorePixels':len(ratios),'minimum':round(ratios[0],3),'percentile05':round(ratios[int(len(ratios)*.05)],3),'median':round(ratios[len(ratios)//2],3),'method':'Rendered cream text against underlying photo plus independent gradient; glyph cores only; not a platform approval test'}
assert ratios[0]>=4.5,contrast

S=R/'outputs/NED_Banner_V02_20261105/图片素材'
for a in build['sourceAssets']:
 f=A/'图片素材'/a['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256']==hashlib.sha256((S/a['file']).read_bytes()).hexdigest()
 assert list(Image.open(f).size)==a['size']
hashes={hashlib.sha256(f.read_bytes()).hexdigest() for f in A.rglob('*') if f.suffix in ['.png','.jpg']}
svgs=[]
for f in E.rglob('*.svg'):
 root=ET.parse(f).getroot();ids=[el.attrib['id'] for el in root.iter() if 'id' in el.attrib];assert len(ids)==len(set(ids))
 for el in root.iter():
  assert not el.tag.endswith('script')
  if el.tag.endswith('image'):
   h=el.attrib['href'];assert h.startswith('data:image/');assert hashlib.sha256(base64.b64decode(h.split(',',1)[1])).hexdigest() in hashes
  for value in el.attrib.values():
   for ref in re.findall(r'url\(#([^)]+)\)',value):assert ref in ids,ref
 svgs.append(dict(file=f.relative_to(O).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
checks=dict(status='制作自检完成，待用户审阅',size=[1600,6600],continuousSize=[1600,35120],nativeTextObjects=build['textObjects'],sourceAssets=build['sourceAssets'],moduleChecks=report['moduleChecks'],geometry={k:report[k] for k in ['textCount','overflow','overlaps','failedImages','copyErrors','errors']},contrast=contrast,backgroundSeamMaxDifference=0,files=svgs)
(L/'制作自检记录.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# Banner英文字段与来源','','2026-11-08。沿用独立Banner V02现有文案，未增加性能或销量宣称。','']
for k,v in build['copy'].items():lines+=['- **'+k+'**：'+v]
lines+=['','[原Banner V02交付](https://github.com/Migo1203/AIGC/tree/main/作品项目/NED_Eric_Lamp_氛围灯/制作交付/独立Banner/V02)。本轮未重新核验平台现时规则。','', 'REC标题为32个字符（含空格与标点），只描述现有文案，不代表现时平台字段上限。']
(L/'英文字段与来源.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for name in ['render_ned_banner_showcase_v04.cjs','finish_ned_banner_showcase_v04.py']:shutil.copy2(R/'work'/name,L/name)
print(json.dumps(dict(size=checks['size'],continuousSize=checks['continuousSize'],nativeTextObjects=checks['nativeTextObjects'],svgFiles=len(svgs),contrast=contrast,sourceAssets='byte-identical'),ensure_ascii=False))
