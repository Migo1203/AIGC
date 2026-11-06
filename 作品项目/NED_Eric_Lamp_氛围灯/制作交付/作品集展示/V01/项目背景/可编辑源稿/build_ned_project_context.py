from pathlib import Path
from PIL import Image, ImageCms
import base64
import json
import shutil

ROOT = Path('D:/WLQ/AIGC作品集')
ASSETS = ROOT / 'work/ned-banner-assets'
LOGO = ROOT / 'outputs/NED_Logo_原样重绘_20261105'
OUT = ROOT / 'outputs/NED_项目背景_V01_20261106'
EDIT = OUT / '可编辑源稿'
EDIT.mkdir(parents=True, exist_ok=True)
ICC = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
SCENE_BOX = (310, 0, 1290, 1086)
scene = Image.open(ASSETS / 'P01_Mobile.png').convert('RGB')
scene.crop(SCENE_BOX).resize((704, 780), Image.Resampling.LANCZOS).save(
    EDIT / '日间场景_背景页裁切.png', icc_profile=ICC)

def data(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<title>NED Eric｜项目背景</title>
<desc>自发电商视觉概念项目。左侧介绍项目目标与约束，右侧为既有 AI 辅助日间家居场景。</desc>
<defs><style>
@font-face{{font-family:DM;src:url('{data(ASSETS/'DMSans-VF.ttf', 'font/ttf')}')}}
text{{font-family:DM,'Microsoft YaHei',sans-serif;fill:#302d28}}
.cn{{font-family:'Microsoft YaHei',sans-serif}}
.muted{{fill:#6a6259}}
</style></defs>
<rect width="1600" height="900" fill="#f3efe7"/>
<image id="existing-ai-scene" x="896" y="0" width="704" height="780" href="{data(EDIT/'日间场景_背景页裁切.png', 'image/png')}"/>
<image id="existing-logo-redraw" x="80" y="60" width="100" height="57" href="{data(LOGO/'NED_原样重绘_黑_紧边.svg','image/svg+xml')}"/>
<text x="218" y="96" font-size="17" font-weight="500" letter-spacing="2">PROJECT CONTEXT</text>
<text class="cn muted" x="82" y="179" font-size="21">项目背景</text>
<text class="cn" x="78" y="258" font-size="52" font-weight="700">从一盏灯，</text>
<text class="cn" x="78" y="327" font-size="52" font-weight="700">建立完整的电商视觉。</text>
<text class="cn muted" x="82" y="389" font-size="24">以 NED Eric 无线氛围灯为对象，探索面向</text>
<text class="cn muted" x="82" y="430" font-size="24">亚马逊美国站的电商视觉表达，串联商品图、</text>
<text class="cn muted" x="82" y="471" font-size="24">A+ 内容与 Banner，构建一致的视觉体验。</text>
<path d="M82 535H810" stroke="#d7cfc2" stroke-width="1"/>
<text class="cn muted" x="82" y="586" font-size="19">设计目标</text>
<text class="cn" x="82" y="632" font-size="24">兼顾温暖的家居氛围</text>
<text class="cn" x="82" y="670" font-size="24">与清晰的产品信息。</text>
<text class="cn muted" x="468" y="586" font-size="19">制作约束</text>
<text class="cn" x="468" y="632" font-size="24">现有素材与多版位适配，</text>
<text class="cn" x="468" y="670" font-size="24">保持产品形象一致。</text>
<path d="M80 780H1520" stroke="#ded7cc" stroke-width="1"/>
<text class="cn" x="82" y="849" font-size="23">商品图 / A+ 内容 / Banner 系统</text>
<text class="cn muted" x="1518" y="848" text-anchor="end" font-size="18">自发概念项目 · AI 辅助设计</text>
</svg>'''
(EDIT / 'NED_Eric_项目背景_V01_可编辑.svg').write_text(svg, encoding='utf-8')
shutil.copy2(ASSETS / 'DM-Sans-OFL.txt', EDIT / 'DM-Sans-OFL.txt')
shutil.copy2(Path(__file__), EDIT / Path(__file__).name)
settings = {
    'created': '2026-11-06', 'version': 'V01', 'status': '待审阅',
    'deliverable': '作品集项目背景展示页', 'size': [1600, 900],
    'method': 'Existing image crop plus editable SVG typography; no new AI image generation',
    'source': 'P01_Mobile.png, 1448×1086, existing AI scene from Premium A+',
    'source_repo': '作品项目/NED_Eric_Lamp_氛围灯/制作交付/亚马逊A+内容/高级A+_V01/素材原图/P01_Mobile.png',
    'crop_box': list(SCENE_BOX), 'photo_output': [704, 780],
    'processing': 'Near-uniform downsample (~0.718×); no product reshaping or newly generated details',
    'visual_system': {'background': '#f3efe7', 'ink': '#302d28', 'muted': '#6a6259', 'margin': 80},
    'typefaces': 'DM Sans embedded with OFL; Microsoft YaHei local system reference, not redistributed',
    'editable': 'Live SVG text and embedded bitmap photograph; existing logo unchanged',
}
(OUT / '制作记录.json').write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding='utf-8')
(OUT / 'README.md').write_text('''# NED Eric｜项目背景 V01

日期：2026-11-06。1600×900（16:9），作品集背景展示页，待审阅。

![项目背景](NED_Eric_项目背景_V01_1600x900.jpg)

[PNG 原图](NED_Eric_项目背景_V01_1600x900.png) · [文字可编辑 SVG](可编辑源稿/NED_Eric_项目背景_V01_可编辑.svg) · [制作记录](制作记录.json)

## 内容与视觉

- 交代自发概念项目的对象、展示语境、设计目标与素材/版位约束，不虚构品牌委托或商业数据。
- 延续封面的暖米色底、深炭字、DM Sans / 微软雅黑、80 px 外边距及底部项目说明栏。
- 左文右图，右侧采用已有高级 A+ 日间家居场景，与封面同系列；保持完整灯体及原产品比例。
- 场景为已有 AI 视觉，不是新增摄影或新一轮 AI 生图；裁切后缩小到展示尺寸。
- 图片没有新增背景资料事实；“设计目标”是本项目意图，不代表经过投放验证的结果。

## 文件与编辑

- JPEG / PNG 为 RGB、sRGB 导出，SVG 保留文字，可修改标题和说明；摄影是嵌入位图，不是分层摄影 PSD。
- SVG 嵌入 DM Sans，附 OFL；中文引用本机 Microsoft YaHei，未分发系统字体。跨平台编辑缺少字体时需替换或安装；导出图片不受影响。
- 制作脚本和渲染脚本保留作为操作记录，本机运行路径需按实际环境调整。
- 归档按用户授权执行，待审阅状态不因归档改变。
''', encoding='utf-8')
print(str(OUT))
