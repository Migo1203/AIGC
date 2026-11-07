from pathlib import Path
from PIL import Image, ImageChops
import json, shutil, hashlib, re
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集02高级A+_展示规划_V01_20261108';P=O/'01_示意图与预览';E=O/'02_可编辑SVG'
for f in P.glob('*.png'):
 im=Image.open(f).convert('RGB');im.save(f.with_suffix('.jpg'),quality=94,subsampling=0)
long=Image.open(P/'02_高级A+_规划示意_V01.png').convert('RGB')
thumb=long.resize((800,3900),Image.Resampling.LANCZOS);thumb.save(P/'02_高级A+_规划示意_V01_缩略.jpg',quality=92)
old=Image.open(R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106/01_商品图展示_V04_1600x4640.png').convert('RGB')
joint=Image.new('RGB',(1600,1800));joint.paste(old.crop((0,3940,1600,4640)),(0,0));joint.paste(long.crop((0,0,1600,1100)),(0,700));joint.save(P/'商品图至A+_衔接示意_V01.jpg',quality=94,subsampling=0)
long.crop((0,2040,1600,3380)).resize((1200,1005),Image.Resampling.LANCZOS).save(R/'work/ned-aplus-plan-operation-check.jpg',quality=94)
long.crop((0,6310,1600,7800)).resize((1200,1117),Image.Resampling.LANCZOS).save(R/'work/ned-aplus-plan-mobile-check.jpg',quality=94)
checks=json.loads((R/'work/ned-aplus-showcase-plan-render-check.json').read_text(encoding='utf-8'))
assert not any(c['failed'] or c['overflow'] or c['overlaps'] or c['errors'] for c in checks)
assets=json.loads((R/'work/ned-aplus-showcase-plan-assets.json').read_text(encoding='utf-8'))
for a in assets:assert hashlib.sha256((O/'03_参考素材'/a['file']).read_bytes()).hexdigest()==a['sha256']
for f in O.rglob('*'):
 if f.suffix.lower() in ['.png','.jpg']:
  with Image.open(f) as im: im.verify()
for m in re.finditer(r'\]\(([^)]+)\)',(O/'README.md').read_text(encoding='utf-8')):
 target=m.group(1)
 assert (O/target).exists(),target
note=O/'04_制作记录.md'
text=note.read_text(encoding='utf-8').replace('源文件哈希、渲染检查与实际视觉复核结论见交付时补充。',f'素材哈希：{len(assets)}份所用素材与V03来源逐字节一致。两张SVG均已Chrome渲染：总览6个图片引用，长页15个图片引用；全部解码成功，文字无越界、无相互重叠、无脚本错误。PNG与SVG同版渲染；JPG由该PNG导出。全部本轮图片可解码，README相对链接目标存在。')
note.write_text(text,encoding='utf-8')
for name in ['render_ned_aplus_showcase_plan.cjs','finish_ned_aplus_showcase_plan.py']:shutil.copy2(R/'work'/name,E/name)
print(json.dumps({'files':len([f for f in O.rglob('*') if f.is_file()]),'assets':len(assets),'totalMB':round(sum(f.stat().st_size for f in O.rglob('*') if f.is_file())/1024/1024,1),'maxMB':round(max(f.stat().st_size for f in O.rglob('*') if f.is_file())/1024/1024,1),'checks':checks},ensure_ascii=False))
