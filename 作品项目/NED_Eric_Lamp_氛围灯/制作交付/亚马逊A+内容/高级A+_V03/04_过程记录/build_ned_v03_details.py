from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageCms,ImageFont
import json

R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_高级A+_V03_20261107'
M=O/'03_原始素材/制作素材';A=O/'01_成品与预览/平台纯图素材'
im=Image.open(O/'03_原始素材/参考素材/产品_正面近景.jpg').convert('RGB')
pts=[]
def move(p):pts.append(p)
def curve(a,b,c,n=45):
 p=pts[-1]
 for j in range(1,n+1):
  t=j/n;u=1-t;pts.append((u*u*u*p[0]+3*u*u*t*a[0]+3*u*t*t*b[0]+t*t*t*c[0],u*u*u*p[1]+3*u*u*t*a[1]+3*u*t*t*b[1]+t*t*t*c[1]))
# Hand-traced silhouette from the actual 1024px photograph. No chroma threshold:
# the previous chroma matte lost dark base pixels and retained disconnected specks.
move((493.5,211.5));move((493.5,164))
curve((493.5,136),(525,138),(527,162));move((527,211))
curve((636,218),(709,297),(710,428));curve((704,438),(613,450),(528,451))
move((528,795));curve((621,799),(700,817),(708,839));move((708,862))
curve((692,893),(603,902),(509,902));curve((418,902),(329,888),(314,863));move((314,839))
curve((320,814),(406,798),(493,795));move((493,451))
curve((409,450),(317,439),(308,428));curve((309,301),(383,221),(493.5,211.5))
scale=4;mask4=Image.new('L',(4096,4096));ImageDraw.Draw(mask4).polygon([(round(x*scale),round(y*scale)) for x,y in pts],fill=255)
mask=mask4.resize(im.size,Image.Resampling.LANCZOS).filter(ImageFilter.MinFilter(3))
mask.save(M/'P02_产品轮廓蒙版.png')
rgba=im.convert('RGBA');rgba.putalpha(mask);rgba.save(M/'P02_真实产品_修订蒙版.png')
shadow=Image.new('L',(1024,1024));ImageDraw.Draw(shadow).ellipse((312,878,710,906),fill=42);shadow=shadow.filter(ImageFilter.GaussianBlur(9));shadow.save(M/'P02_独立接触阴影.png')

def cutback(w,h,bg,box=None):
 canvas=Image.new('RGBA',(w,h),bg)
 return canvas

bg='#e7dfd2';pc=Image.new('RGBA',(1952,800),bg)
# Preserve full-resolution product texture; only shrink it for the complete lamp.
product=rgba.crop((298,130,722,912));factor=0.79
product=product.resize((round(product.width*factor),round(product.height*factor)),Image.Resampling.LANCZOS)
sh=Image.new('RGBA',pc.size);ImageDraw.Draw(sh).ellipse((296,683,630,712),fill=(62,48,32,38));sh=sh.filter(ImageFilter.GaussianBlur(10));pc.alpha_composite(sh)
pc.alpha_composite(product,(294,78))
# The original neutral photo remains in the single detail window to avoid inventing
# an extreme macro. The window is a genuine crop, not a second generated product.
box=(390,125,630,365);crop=im.crop(box);crop.save(M/'P02_旋钮原像素裁切.png')
detailbg=Image.new('RGB',(600,390),'#ededeb');detail=crop.resize((300,300),Image.Resampling.LANCZOS);detailbg.paste(detail,(150,44));detailbg.save(M/'P02_旋钮展示窗口.jpg',quality=96)
pc.alpha_composite(detailbg.convert('RGBA'),(1035,210))
icc=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
pc.convert('RGB').save(A/'P02_PC.jpg',quality=96,subsampling=0,icc_profile=icc)
mobile=Image.new('RGBA',(600,450),bg)
full=rgba.crop((298,130,722,912));full.thumbnail((226,416),Image.Resampling.LANCZOS)
sh=Image.new('RGBA',mobile.size);ImageDraw.Draw(sh).ellipse((195,411,410,430),fill=(62,48,32,34));mobile.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
mobile.alpha_composite(full,((600-full.width)//2,19))
mobile.convert('RGB').save(A/'P02_Finish_Mobile.jpg',quality=96,subsampling=0,icc_profile=icc)
# A tighter actual-source 600x450 framing increases knob emphasis, with no made-up
# coating detail; mild resampling is recorded as resampling, not true resolution.
knob=im.crop((350,80,675,324)).resize((600,450),Image.Resampling.LANCZOS)
knob.save(A/'P02_Knob_Mobile.jpg',quality=96,subsampling=0,icc_profile=icc)
board=Image.new('RGB',(1500,600),'#f1eee8');d=ImageDraw.Draw(board)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
for i,color in enumerate(['#eee9df','#383d3b','#8b735d']):
 b=Image.new('RGBA',(430,510),color);p=rgba.crop((298,130,722,912));p.thumbnail((240,450),Image.Resampling.LANCZOS);b.alpha_composite(p,((430-p.width)//2,25));board.paste(b.convert('RGB'),(20+i*490,50));d.text((20+i*490,12),'P02 蒙版 / '+color,font=font,fill='#3b3832')
board.save(O/'04_过程记录/P02_蒙版背景检查.jpg',quality=95)
(O/'04_过程记录/P02_制作依据.md').write_text('''# P02真实照片处理

来源：沿用参考素材/产品_正面近景.jpg，1024×1024。按真实轮廓重描非破坏蒙版，替代V02依色差阈值提取的方法；产品RGB来自原照，未生成产品细节。保留底部正常薄暗线，另存独立接触阴影。桌面一张完整灯＋一处旋钮原照窗口；手机两状态为旋钮和完整沙色灯。

旋钮原像素裁切为240×240；桌面展示放到300×300，手机裁切325×244后重采样600×450。重采样不增加真实细节，不作微观涂层或工艺证据。所有标注在SVG中单独制作。蒙版边界仍须以导出图及放大图目视复核。
''',encoding='utf-8')
print('P02 three real-photo assets and editable mask created.')
