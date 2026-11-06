from pathlib import Path
from PIL import Image,ImageCms,ImageDraw,ImageFont
import numpy as np,json,re,xml.etree.ElementTree as ET,base64,hashlib,shutil
R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_商品图展示_V04_亮背景与ListingV01_20261106';E=O/'可编辑源稿';icc=ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
p=O/'01_商品图展示_V04_1600x4640.png';im=Image.open(p).convert('RGB');im.save(p,icc_profile=icc);im.save(p.with_suffix('.jpg'),quality=96,subsampling=0,icc_profile=icc);im.resize((800,2320),Image.Resampling.LANCZOS).save(O/'01_商品图展示_V04_缩略.jpg',quality=96,icc_profile=icc)
im.crop((0,270,1600,1530)).save(O/'Listing_V01_展示局部.jpg',quality=96,subsampling=0,icc_profile=icc)
im.crop((70,1610,1530,3080)).save(O/'组图前两排_投影与描边.jpg',quality=96,subsampling=0,icc_profile=icc)
font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',24)
board=Image.new('RGB',(1400,760),'#f3eadf');d=ImageDraw.Draw(board)
for i,(path,title) in enumerate([(R/'work/ned-revision-refs/03_光色调节_V01.png','03 V01：本轮采用'),(R/'work/ned-listing-assets/03_光色调节_V02.png','03 V02：对照')]):
 board.paste(Image.open(path).convert('RGB').resize((670,670)),(15+i*700,55));d.text((20+i*700,14),title,font=font,fill='#40392f')
board.save(O/'03光色调节_V01与V02_风格对照.jpg',quality=96,icc_profile=icc)
old=Image.open(R/'outputs/NED_成果展示排版_V03_商品图已置入_20261106/可编辑源稿/商品图_连续墙面背景.png').convert('RGB').resize((400,1160));new=Image.open(E/'连续背景_提亮柔焦光影_V03.png').convert('RGB').resize((400,1160));comp=Image.new('RGB',(800,1200),'#f7f0e5');comp.paste(old,(0,40));comp.paste(new,(400,40));d=ImageDraw.Draw(comp);d.text((15,7),'原背景',font=font,fill='#40392f');d.text((415,7),'修订：提亮并恢复光影',font=font,fill='#40392f');comp.save(O/'背景修订对照.jpg',quality=95,icc_profile=icc)
prev=Image.open(R/'outputs/NED_作品集开篇_V04_轻过渡与视觉情绪板_20261106/02_NED_Eric_背景与视觉策略_V04_1600x1200.png');joined=Image.new('RGB',(1600,5840));joined.paste(prev,(0,0));joined.paste(im,(0,1200));joined.resize((800,2920),Image.Resampling.LANCZOS).save(O/'策略至商品图_连续预览.jpg',quality=95,icc_profile=icc)
orig=(R/'work/ned-revision-refs/Listing页面模拟.html').read_text(encoding='utf-8');html=(E/'Listing_V01_仅同步03缩略图.html').read_text(encoding='utf-8');assert re.sub('src="[^"]*"','src=""',orig)==re.sub('src="[^"]*"','src=""',html)
rec=json.loads((O/'制作记录.json').read_text(encoding='utf-8'));svg=ET.parse(E/'01_商品图展示_V04_可编辑.svg');ns={'s':'http://www.w3.org/2000/svg'}
for a in rec['assets']:
 el=svg.find('.//s:image[@id="'+a['id']+'"]',ns);assert hashlib.sha256(base64.b64decode(el.get('href').split(',',1)[1])).hexdigest()==a['sha256']
bg=np.asarray(Image.open(E/'连续背景_提亮柔焦光影_V03.png'));master=np.asarray(Image.open(R/'outputs/NED_作品集连续背景_V02_20261106/NED_连续墙面背景_V02_1600x2400.png'))
assert np.array_equal(bg[0],master[1200])
qa={'listing_html_unchanged_except_image_src':True,'source_images_hash_match':True,'03_adopted':'V01; not regenerated','size':list(im.size),'strategy_to_background_first_row_identical':True,'old_background_rgb_mean':np.asarray(old).mean(axis=(0,1)).tolist(),'revised_background_rgb_mean':bg.mean(axis=(0,1)).tolist(),'git_push':False}
(O/'素材与背景检查.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['render_ned_listing_revision_v04.cjs','package_ned_listing_revision_v04.py']:shutil.copy2(R/'work'/n,E/n)
(O/'README.md').write_text('''# NED 商品图展示 V04：亮背景、Listing V01与图组层次

2026-11-06。仅本地审阅，不提交、不推送。保留旧版；本轮只修改01商品图展示。

## 四项调整

1. 原长图延展只取末行颜色，原有模糊光影丢失。此次以获准暖墙V02的完整母版从y=1200继续，垂直镜向延展保留光影，15px柔焦；暖白覆盖从0渐至26%以提亮。首行仍与策略背景相邻行一致。获准母版本身未覆盖；修订背景为本地衍生V03，不再声称全篇背景像素等同旧母版。附背景前后对照。
2. 使用实际Listing V01的HTML及全部英文文案、页面布局，替换上一版占位信息区。唯一修改是本地图片路径，以及03缩略图改用本轮选择的V01。HTML除图片src外逐字一致，渲染后嵌入作品集；完整内容包含标题、五点、商品描述与规格。展示不是已上架截图。
3. 八张图组外层增加暖深色柔影（dy9px、std12px、opacity16%）与1px浅描边。图片本身未调色、裁切、变形或重绘；外部阴影不写进源图片。完整Listing区亦加轻投影。
4. 对照03的V01/V02与整组：V01与套图共有沙色灯体、暖中性背景、自然材质、黑色无衬线及暖至中性渐变条；V01有暖木桌和窗光，V02为石桌与蓝灰墙。现套图本已包含昼夜、木石变化，所以我判断不是风格迥异，直接采用V01更符合用户对其图文层级的偏好，未触发重新合成或AI生图。标题→色温范围→渐变条与标签→操作说明的顺序完整保留。该判断为视觉判断，不是品牌官方规范结论。附两版对照图。

## 当前选图

主图V01；辅图01、02、04、05、06、07采用V02；辅图03光色调节采用V01。原图均1254×1254，图组以660×660等比展示。上方Listing缩略图同步此组合。源图哈希已检查，不覆盖任何既有交付。

03的正式名称是“光色调节”；其参数与操作继续沿用项目资料标称，未变成独立测量结论。V01的木桌差异保留，之后若希望该张也严格使用石桌蓝灰背景，可另做布局与场景的结合版本，但当前整组并不需要强行同墙同桌。

## 文件

- `01_商品图展示_V04_1600x4640.png/.jpg`：高清长图，因完整展示Listing V01，高度由4200增至4640。
- `01_商品图展示_V04_缩略.jpg`：800px宽预览。
- `Listing_V01_展示局部.jpg`、`组图前两排_投影与描边.jpg`：局部。
- `03光色调节_V01与V02_风格对照.jpg`、`背景修订对照.jpg`：判断依据。
- `策略至商品图_连续预览.jpg`：检查前后衔接。
- `可编辑源稿/01_商品图展示_V04_可编辑.svg`：外层排版、独立图片、投影与描边；Listing为HTML渲染位图，其可编辑HTML同目录保留，本地源图路径需相应调整。

不是新一轮AI生成。A+与Banner未修改，未选终稿；新的4640px商品图模块更长，后续填A+时需重新从统一背景坐标衔接，不直接接旧占位截图。
''',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
