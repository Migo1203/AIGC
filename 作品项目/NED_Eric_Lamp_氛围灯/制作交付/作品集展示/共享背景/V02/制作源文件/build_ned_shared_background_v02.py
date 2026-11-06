from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageCms
import numpy as np
import json, shutil

ROOT=Path('D:/WLQ/AIGC作品集')
OUT=ROOT/'outputs/NED_作品集连续背景_V02_20261106'
EDIT=OUT/'制作源文件';EDIT.mkdir(parents=True,exist_ok=True)
SRC=ROOT/'work/ned-banner-assets/P01_PC.png'
ICC=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
wall=Image.open(SRC).convert('RGB').crop((0,0,965,580))
wall.save(EDIT/'原场景_墙面提取.png',icc_profile=ICC)
texture=wall.resize((1600,2400),Image.Resampling.BICUBIC)
texture=ImageEnhance.Color(texture).enhance(.85)
soft=texture.filter(ImageFilter.GaussianBlur(11))
# Strengthen existing light/shadow detail relative to its broad wall illumination,
# rather than darkening the entire page. Left text field receives a smaller gain.
a=np.asarray(soft,dtype=np.float32)
b=np.asarray(soft.filter(ImageFilter.GaussianBlur(180)),dtype=np.float32)
x=np.linspace(0,1,1600,dtype=np.float32)[None,:,None]
gain=.45+.70*x
enhanced=np.clip(a+(a-b)*gain,0,255).astype(np.uint8)
bg=Image.fromarray(enhanced)
bg=ImageEnhance.Contrast(bg).enhance(1.12)
bg=Image.blend(bg,Image.new('RGB',bg.size,'#f3eadd'),.10)
for ext in ['png','jpg']:
 kw={'icc_profile':ICC}
 if ext=='jpg':kw.update(quality=96,subsampling=0,optimize=True)
 bg.save(OUT/f'NED_连续墙面背景_V02_1600x2400.{ext}',**kw)
for n,y in [(1,0),(2,1200)]:
 bg.crop((0,y,1600,y+1200)).save(OUT/f'连续切片_0{n}_1600x1200.jpg',quality=96,subsampling=0,icc_profile=ICC)
bg.resize((800,1200),Image.Resampling.LANCZOS).save(OUT/'连续背景_V02_缩略预览.jpg',quality=95,icc_profile=ICC)
old=Image.open(ROOT/'outputs/NED_作品集连续背景_V01_20261106/连续背景_缩略预览.jpg')
board=Image.new('RGB',(1600,1200));board.paste(old,(0,0));board.paste(bg.resize((800,1200),Image.Resampling.LANCZOS),(800,0))
board.save(OUT/'V01左_V02右_光影对比.jpg',quality=95,icc_profile=ICC)
record={'date':'2026-11-06','version':'V02','status':'本地参考，待审阅；暂不推送','size':[1600,2400],
 'source':str(SRC),'wall_crop':[0,0,965,580],
 'method':'Existing wall light/shadow enhanced with local contrast, soft blur and reduced warm overlay; no AI generation',
 'blur_radius_px':11,'broad_illumination_radius_px':180,'detail_gain_left':.45,'detail_gain_right':1.15,
 'global_contrast':1.12,'warm_overlay':.10,
 'continuity':'One continuous master; two sequential 1600×1200 slices, not a repeating tile.'}
(OUT/'制作记录.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'README.md').write_text('''# NED｜作品集连续背景 V02

2026-11-06，本地参考，待审阅，暂不推送。1600×2400，RGB/sRGB。

按反馈增强既有墙面光影：柔焦半径由 18 px 减至 11 px，减少暖白覆盖，增强局部明暗。左侧正文区域增幅较弱，右侧光影增幅较强。没有新增 AI 生图，也没有覆盖 V01。

母版可连续切成两张 1600×1200 的 4:3 页面。V01/V02 对比图左旧右新；母版不是无缝循环纹理。
''',encoding='utf-8')
shutil.copy2(Path(__file__),EDIT/Path(__file__).name)
with Image.open(OUT/'NED_连续墙面背景_V02_1600x2400.png') as im:
 assert im.size==(1600,2400) and im.mode=='RGB' and im.info.get('icc_profile')
print(str(OUT))
