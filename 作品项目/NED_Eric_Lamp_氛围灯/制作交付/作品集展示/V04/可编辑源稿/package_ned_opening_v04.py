from pathlib import Path
from PIL import Image, ImageCms
import numpy as np
import json, shutil

root=Path('D:/WLQ/AIGC作品集')
out=root/'outputs/NED_作品集开篇_V04_轻过渡与视觉情绪板_20261106';edit=out/'可编辑源稿'
icc=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes();checks=[];pages=[]
for stem in ['01_NED_Eric_封面_V04_1600x1200','02_NED_Eric_背景与视觉策略_V04_1600x1200']:
 p=out/(stem+'.png');im=Image.open(p).convert('RGB');im.save(p,icc_profile=icc)
 im.save(out/(stem+'.jpg'),quality=96,subsampling=0,optimize=True,icc_profile=icc);pages.append(im)
 assert im.size==(1600,1200)
 checks.append({'file':p.name,'size':list(im.size),'mode':im.mode,'icc':True})
board=Image.new('RGB',(1600,2400));board.paste(pages[0],(0,0));board.paste(pages[1],(0,1200))
board.save(out/'封面至策略_连续阅读预览.jpg',quality=95,subsampling=0,optimize=True,icc_profile=icc)
board.resize((800,1200),Image.Resampling.LANCZOS).save(out/'封面至策略_缩略预览.jpg',quality=95,icc_profile=icc)
base=np.asarray(Image.open(edit/'封面_场景至墙面过渡.png'))
scene=np.asarray(Image.open(edit/'封面_原场景裁切.png'))
wall=np.asarray(Image.open(root/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png'))
strategy=np.asarray(Image.open(edit/'策略页_连续背景.png'))
next_bg=np.asarray(Image.open(out/'成果速览_下一屏背景_1600x1200.png'))
qa={'cover_product_area_unchanged':bool(np.array_equal(base[:850],scene[:850])),
 'cover_strategy_boundary_identical':bool(np.array_equal(base[-1],wall[0])),
 'strategy_matches_approved_master':bool(np.array_equal(strategy,wall[:1200])),
 'next_overview_matches_approved_master':bool(np.array_equal(next_bg,wall[1200:])),
 'natural_adjacent_row_mean_difference':float(np.abs(wall[1199].astype(float)-wall[1200].astype(float)).mean())}
assert all(v for k,v in qa.items() if k!='natural_adjacent_row_mean_difference')
(out/'连续性与产品保护检查.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'导出检查.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
shutil.copy2(root/'work/render_ned_opening_v04.cjs',edit/'render_ned_opening_v04.cjs')
shutil.copy2(Path(__file__),edit/Path(__file__).name)
print(json.dumps(qa,ensure_ascii=False))
