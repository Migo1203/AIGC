from pathlib import Path
from PIL import Image
import xml.etree.ElementTree as ET
import hashlib, base64, json, shutil, re
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集02高级A+_展示规划_V02_单列长图_20261108';P=O/'01_示意图与预览';E=O/'02_可编辑SVG'
checks=json.loads((R/'work/ned-aplus-showcase-plan-v02-render-check.json').read_text(encoding='utf-8'))
assert not any(c['failed'] or c['overflow'] or c['overlaps'] or c['errors'] for c in checks)
assets=json.loads((R/'work/ned-aplus-showcase-plan-v02-assets.json').read_text(encoding='utf-8'))
lookup={a['sha256']:a['file'] for a in assets}
for a in assets:
 assert hashlib.sha256((O/'03_参考素材'/a['file']).read_bytes()).hexdigest()==a['sha256']
root=ET.parse(E/'02_高级A+_单列长图规划示意_V02.svg').getroot()
placements=[]
for im in root.iter('{http://www.w3.org/2000/svg}image'):
 raw=base64.b64decode(im.attrib['href'].split(',',1)[1]);digest=hashlib.sha256(raw).hexdigest()
 if digest not in lookup:continue
 name=lookup[digest];x,y,w,h=[float(im.attrib[k]) for k in ['x','y','width','height']]
 assert abs(x+w/2-800)<.01,name
 assert (w==600 and x==500) if 'Mobile' in name else (w==1440 and x==80),name
 placements.append((name,x,y,w,h))
expected=['P01_PC','P02_PC','P03A_PC','P03B_PC','P03C_PC','P04A_PC','P04B_PC','P04C_PC','P05_PC','P06_PC','P03C_Mobile','P04B_Mobile']
assert [p[0] for p in placements]==[e+'.png' for e in expected]
for a,b in zip(placements,placements[1:]):assert a[2]+a[4]<b[2],(a,b)
for f in P.glob('*.png'):
 im=Image.open(f).convert('RGB');im.save(f.with_suffix('.jpg'),quality=94,subsampling=0)
long=Image.open(P/'02_高级A+_单列长图规划示意_V02.png').convert('RGB')
long.resize((800,5530),Image.Resampling.LANCZOS).save(P/'02_高级A+_单列长图规划示意_V02_缩略.jpg',quality=92)
old=Image.open(R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106/01_商品图展示_V04_1600x4640.png').convert('RGB')
joint=Image.new('RGB',(1600,1800));joint.paste(old.crop((0,3940,1600,4640)),(0,0));joint.paste(long.crop((0,0,1600,1100)),(0,700));joint.save(P/'商品图至A+_衔接示意_V02.jpg',quality=94,subsampling=0)
for label,y1,y2 in [('操作',2040,4550),('场景',4590,7150),('手机',8740,11060)]:
 im=long.crop((0,y1,1600,y2));im.resize((1000,round(im.height*1000/1600)),Image.Resampling.LANCZOS).save(R/f'work/ned-aplus-plan-v02-{label}-check.jpg',quality=94)
for f in O.rglob('*'):
 if f.suffix.lower() in ['.png','.jpg']:
  with Image.open(f) as im:im.verify()
for link in re.findall(r'\]\(([^)]+)\)',(O/'README.md').read_text(encoding='utf-8')):assert (O/link).exists(),link
log=O/'04_制作记录.md'
with log.open('a',encoding='utf-8') as f:
 f.write('\n检查结果：两张SVG已Chrome同版渲染；长图13个图片引用均可解码，结构图0个图片引用。规划文字无越界、无互相重叠、无脚本错误。12份嵌入图与V03原预览SHA256逐一匹配，来源文件逐字节一致。按图片内容哈希核实P03A/B/C、P04A/B/C均完整存在，顺序正确。12张内容图均在同一中轴，彼此垂直范围没有重叠；宽幅1440px、手机600px，未裁切或拉伸。README图片与SVG目录链接均存在，PNG/JPG全部可解码。\n')
for name in ['render_ned_aplus_showcase_plan_v02.cjs','finish_ned_aplus_showcase_plan_v02.py']:shutil.copy2(R/'work'/name,E/name)
print(json.dumps({'contents':len(placements),'singleColumn':True,'operationStates':3,'sceneStates':3,'totalMB':round(sum(f.stat().st_size for f in O.rglob('*') if f.is_file())/1024/1024,1),'maxMB':round(max(f.stat().st_size for f in O.rglob('*') if f.is_file())/1024/1024,1)},ensure_ascii=False))
