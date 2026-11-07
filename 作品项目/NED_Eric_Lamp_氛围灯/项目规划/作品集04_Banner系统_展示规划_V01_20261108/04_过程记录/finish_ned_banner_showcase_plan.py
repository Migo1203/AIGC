from pathlib import Path
from PIL import Image,ImageOps
import shutil
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_作品集04Banner系统_展示规划_V01_20261108';P=O/'01_示意图与预览'
im=Image.open(P/'04_Banner系统_展示规划示意_V01_1600x7040.png').convert('RGB');assert im.size==(1600,7040)
im.save(P/'04_Banner系统_展示规划示意_V01_1600x7040.jpg',quality=94,subsampling=0);ImageOps.contain(im,(800,3520)).save(P/'04_Banner系统_展示规划示意_V01_缩略.jpg',quality=92)
prev=Image.open(R/'outputs/NED_作品集03_品牌故事_展示_V04_20261108/01_成品与预览/03_品牌故事展示_V04_1600x6600.png').convert('RGB')
seam=Image.new('RGB',(1600,1850));seam.paste(prev.crop((0,5850,1600,6600)),(0,0));seam.paste(im.crop((0,0,1600,1100)),(0,750));seam.save(P/'03至04_衔接示意_V01.jpg',quality=94,subsampling=0)
for n,box in [('页头',(0,0,1600,1400)),('餐桌',(0,1410,1600,3350)),('REC',(150,3370,1450,6500)),('页尾',(0,6550,1600,7040))]:im.crop(box).save(R/f'work/ned-banner-plan-{n}-review.jpg',quality=94)
for name in ['render_ned_banner_showcase_plan.cjs','finish_ned_banner_showcase_plan.py']:shutil.copy2(R/'work'/name,O/'04_过程记录'/name)
print('Saved long JPG, thumbnail, seam and review crops.')
