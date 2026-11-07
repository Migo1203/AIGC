from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import json
R=Path('D:/WLQ/AIGC作品集');G=R/'output/imagegen/NED_Premium_V03_20261107';O=R/'outputs/NED_高级A+_V03_20261107';M=O/'03_原始素材/制作素材'
areas={'P04A_Mobile':(440,740,830,1020),'P04B_Mobile':(600,740,1000,1020),'P04C_Mobile':(770,760,1090,1020),'P05_Mobile':(670,735,1070,1015),'P04A_PC':(735,530,1100,775),'P04B_PC':(1070,525,1440,770),'P04C_PC':(1175,590,1455,785)}
records=[]
for key,box in areas.items():
 f=G/(key+'_basefix.png')
 if not f.exists():raise RuntimeError('Missing repair '+str(f))
 source=G/('P05_Mobile_r2.png' if key=='P05_Mobile' else key+'.png');im=Image.open(source).convert('RGB');patch=Image.open(f).convert('RGB');w=box[2]-box[0];h=box[3]-box[1];patch=patch.resize((w,h),Image.Resampling.LANCZOS)
 mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rectangle((18,18,w-19,h-19),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(6))
 im.paste(patch,(box[0],box[1]),mask);im.save(M/(key+'_底座局部修复合成.png'))
 records.append(dict(id=key,source=source.name,patch=f.name,sourceBox=box,method='API local crop repair, resampled to original crop dimensions and composited with feathered 18px margin; original full scene preserved outside patch',derived='03_原始素材/制作素材/'+key+'_底座局部修复合成.png'))
(O/'04_过程记录/底座局部修复记录.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('Composited local base repairs:',len(records))
