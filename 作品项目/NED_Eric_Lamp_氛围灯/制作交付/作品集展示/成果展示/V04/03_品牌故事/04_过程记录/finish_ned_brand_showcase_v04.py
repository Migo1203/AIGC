from pathlib import Path
from PIL import Image,ImageOps,ImageChops
import json,shutil,hashlib,re,base64,xml.etree.ElementTree as ET
R=Path('D:/WLQ/AIGC作品集');build=json.loads((R/'work/ned-brand-showcase-build.json').read_text(encoding='utf-8'));report=json.loads((R/'work/ned-brand-showcase-render-check.json').read_text(encoding='utf-8'))
assert not any(report[k] for k in ['overflow','overlaps','cardOverflow','failedImages','copyErrors','errors'])
O=Path(build['output']);P=O/'01_成品与预览';E=O/'02_可编辑SVG';A=O/'03_原始素材';L=O/'04_过程记录'
im=Image.open(P/'03_品牌故事展示_V04_1600x6600.png').convert('RGB');assert im.size==(1600,6600)
im.save(P/'03_品牌故事展示_V04_1600x6600.jpg',quality=94,subsampling=0)
ImageOps.contain(im,(800,3300)).save(P/'03_品牌故事展示_V04_缩略.jpg',quality=92)
product=Image.open(R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106/01_商品图展示_V04_1600x4640.png').convert('RGB')
aplus=Image.open(R/'outputs/NED_作品集02_高级A+_展示_V04_修订V02_完整手机_20261108/01_成品与预览/02_高级A+展示_V04_修订V02_1600x17280.png').convert('RGB')
assert product.size==(1600,4640) and aplus.size==(1600,17280)
combined=Image.new('RGB',(1600,28520));combined.paste(product,(0,0));combined.paste(aplus,(0,4640));combined.paste(im,(0,21920));combined.save(P/'商品图至品牌故事_完整连续预览.jpg',quality=93,subsampling=0)
seam=Image.new('RGB',(1600,1800));seam.paste(aplus.crop((0,16580,1600,17280)),(0,0));seam.paste(im.crop((0,0,1600,1100)),(0,700));seam.save(P/'高级A+至品牌故事_衔接局部.jpg',quality=94,subsampling=0)
for key,box in [('上半页',(0,0,1600,2050)),('手机01_02',(350,2080,1250,4300)),('手机03_04',(350,4280,1250,6470)),('收尾',(0,6400,1600,6600))]:im.crop(box).save(R/f'work/ned-brand-showcase-{key}-review.jpg',quality=94)
S=R/'work/ned-aplus-showcase-delivery-publish-20261108/作品项目/NED_Eric_Lamp_氛围灯/制作交付/亚马逊A+内容/品牌故事_V01/图片素材'
for record in build['sourcePhotos']:
 assert hashlib.sha256((A/record['file']).read_bytes()).hexdigest()==hashlib.sha256((S/record['file']).read_bytes()).hexdigest()==record['sha256']
ns='{http://www.w3.org/2000/svg}';root=ET.parse(E/'03_品牌故事展示_V04_可编辑.svg').getroot();ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib];assert len(ids)==len(set(ids))
imagehashes={hashlib.sha256(f.read_bytes()).hexdigest() for f in A.iterdir() if f.suffix in ['.jpg','.png']}
for el in root.iter():
 assert el.tag!=ns+'script'
 if el.tag==ns+'image':
  assert el.attrib['href'].startswith('data:')
  assert hashlib.sha256(base64.b64decode(el.attrib['href'].split(',',1)[1])).hexdigest() in imagehashes
 for v in el.attrib.values():
  for ref in re.findall(r'url\(#([^)]+)\)',v):assert ref in ids,ref
for source in build['sources']:assert hashlib.sha256((E/'模块源稿'/source['file']).read_bytes()).hexdigest()==source['sha256']
copylines=['# 品牌故事英文字段与来源','','2026-11-08。完整沿用品牌故事V01英文；仅重新断行与排版。英文为项目创作草案，不是品牌官方文案。','']
for key,value in build['copy'].items():copylines+=['## '+key,'',value,'']
copylines+=['## 来源','','[原品牌故事V01](https://github.com/Migo1203/AIGC/tree/main/作品项目/NED_Eric_Lamp_氛围灯/制作交付/亚马逊A%2B内容/品牌故事_V01)；依据仓库提交63a375e119c506fa000448023e4d16e1345a05a1所存内容。','', '[品牌About原研究来源](https://nedcollections.co.nz/pages/about-us-1)。本轮未重新访问官网；不据品牌创立地推断商品制造地。']
(L/'英文字段与来源.md').write_text('\n'.join(copylines)+'\n',encoding='utf-8')
shutil.copy2(R/'outputs/NED_作品集03品牌故事_展示规划_V01_20261108/03_品牌故事_展示规划_V01.md',L/'执行规划_03品牌故事_V01.md')
for name in ['render_ned_brand_showcase_v04.cjs','finish_ned_brand_showcase_v04.py']:shutil.copy2(R/'work'/name,L/name)
print(json.dumps({'long':[1600,6600],'continuous':[1600,28520],'nativeTextObjects':build['textObjects'],'contentBlocksChecked':report['copyBlocks'],'sourcePhotos':'byte-identical','ids':'unique','images':'embedded'},ensure_ascii=False))
