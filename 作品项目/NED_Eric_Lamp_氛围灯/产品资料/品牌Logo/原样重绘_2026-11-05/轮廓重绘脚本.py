from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys, json, re, shutil, subprocess
import numpy as np
sys.path.insert(0,'D:/WLQ/AIGC作品集/work/ned-vector-libs')
import vtracer

ROOT=Path('D:/WLQ/AIGC作品集')
SRC=ROOT/'work/aigc-banner-publish-20261105/作品项目/NED_Eric_Lamp_氛围灯/产品资料/品牌Logo'
OUT=ROOT/'outputs/NED_Logo_原样重绘_20261105'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'原始文件').mkdir(exist_ok=True)
for p in SRC.glob('*.png'): shutil.copy2(p,OUT/'原始文件'/p.name)
original=Image.open(next(SRC.glob('*白*'))).convert('RGBA')
alpha=original.getchannel('A')
S=8
up=alpha.resize((original.width*S,original.height*S),Image.Resampling.BICUBIC)
mask=up.point(lambda x:0 if x>=128 else 255).convert('RGB')
mask.save(OUT/'描摹输入.png')
vtracer.convert_image_to_svg_py(str(OUT/'描摹输入.png'),str(OUT/'trace.svg'),colormode='binary',mode='spline',filter_speckle=0,corner_threshold=75,length_threshold=2,max_iterations=10,splice_threshold=45,path_precision=4)
raw=(OUT/'trace.svg').read_text()
paths='\n'.join(re.findall(r'<path\b[^>]*?/>',raw,re.S))
if not paths: raise RuntimeError('No vector paths')
bbox=alpha.getbbox()
for color,label in [('#1d1d1b','黑'),('#ffffff','白')]:
    for tight,variant in [(False,'原画布'),(True,'紧边')]:
        if tight:
            x0,y0,x1,y1=bbox
            view=f'{x0*S} {y0*S} {(x1-x0)*S} {(y1-y0)*S}'
            w,h=(x1-x0)*S,(y1-y0)*S
        else: view=f'0 0 {original.width*S} {original.height*S}';w,h=original.width*S,original.height*S
        coloured=re.sub(r'fill="[^"]*"',f'fill="{color}"',paths)
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{view}"><title>NED existing logo — contour redraw, {variant}</title>{coloured}</svg>'
        (OUT/f'NED_原样重绘_{label}_{variant}.svg').write_text(svg,encoding='utf-8')
node='C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
sharp='C:/Users/Migo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp'
code="""const fs=require('fs'),p=require('path'),sharp=require(process.argv[1]);(async()=>{const dir=process.argv[2];for(const f of fs.readdirSync(dir).filter(f=>f.startsWith('NED_')&&f.endsWith('.svg'))){await sharp(p.join(dir,f)).resize({width:4000}).png().toFile(p.join(dir,f.replace('.svg','_4000w.png')))}await sharp(p.join(dir,'NED_原样重绘_白_原画布.svg')).resize(250,74).png().toFile(p.join(dir,'轮廓核对_原尺寸.png'));})().catch(e=>{console.error(e);process.exit(1)})"""
subprocess.run([node,'-e',code,sharp,str(OUT)],check=True)
render=Image.open(OUT/'轮廓核对_原尺寸.png').getchannel('A')
a=np.array(alpha)>=128;b=np.array(render)>=128
iou=float(np.logical_and(a,b).sum()/np.logical_or(a,b).sum())
def components(binary):
    data=binary.copy();sizes=[]
    for y,x in np.argwhere(data):
        if not data[y,x]:continue
        stack=[(int(y),int(x))];data[y,x]=False;n=0
        while stack:
            yy,xx=stack.pop();n+=1
            for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
                ny,nx=yy+dy,xx+dx
                if 0<=ny<data.shape[0] and 0<=nx<data.shape[1] and data[ny,nx]:data[ny,nx]=False;stack.append((ny,nx))
        sizes.append(n)
    return sorted(sizes,reverse=True)
metrics={'source':'NED品牌logo白 .png','source_canvas':[250,74],'source_ink_bbox':bbox,'method':'existing alpha contour → bicubic 8× sampling → binary spline vector trace; no font replacement or generative redraw','iou_at_native_threshold_128':iou,'components_original':components(a),'components_redraw':components(b),'paths':len(re.findall('<path',paths)),'black_and_white_share_identical_paths':True,'note':'Low-resolution contour reconstruction, not recovered official vector. Original asymmetry, connections, counters and period retained as visible in source.'}
metrics['holes_original']=len(components(~np.pad(a,1,constant_values=False)))-1
metrics['holes_redraw']=len(components(~np.pad(b,1,constant_values=False)))-1
(OUT/'轮廓核对记录.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
overlay=np.full((*a.shape,3),244,dtype='uint8');overlay[a&b]=(55,55,55);overlay[a&~b]=(210,65,65);overlay[b&~a]=(0,150,170)
Image.fromarray(overlay).crop((60,0,205,74)).resize((1450,740),Image.Resampling.NEAREST).save(OUT/'轮廓叠图检查.png')
board=Image.new('RGB',(1600,800),'#eeeae3');d=ImageDraw.Draw(board)
f=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',30);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
d.text((60,35),'NED Logo｜原样轮廓重绘',font=f,fill='#292929')
for x,label,im in [(60,'原始白版（仅放大查看）',original.crop(bbox)),(840,'矢量重绘（同一轮廓）',Image.open(OUT/'NED_原样重绘_白_紧边_4000w.png'))]:
    d.rounded_rectangle((x,145,x+700,590),radius=4,fill='#292929')
    im=im.convert('RGBA');scale=min(590/im.width,340/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    board.paste(im,(x+(700-im.width)//2,145+(445-im.height)//2),im)
    d.text((x,105),label,font=small,fill='#292929')
d.text((60,640),f'原尺寸二值轮廓重叠 IoU：{iou:.2%} ｜黑白版共用路径｜保留 ned. 字形与句点',font=small,fill='#292929')
d.text((60,695),'低清轮廓描摹稿，不冒充官方原始矢量文件；原图完整保留。',font=small,fill='#67655f')
board.save(OUT/'Logo原样重绘对照.jpg',quality=95)
print(json.dumps(metrics,ensure_ascii=False))
