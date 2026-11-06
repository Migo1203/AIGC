from pathlib import Path
from PIL import Image, ImageCms
import base64, json, shutil

ROOT = Path('D:/WLQ/AIGC作品集')
SRC = ROOT / 'work/ned-banner-assets'
LOGO = ROOT / 'outputs/NED_Logo_原样重绘_20261105'
OUT = ROOT / 'outputs/NED_作品集封面_V01_20261105'
EDIT = OUT / '可编辑源稿'
EDIT.mkdir(parents=True, exist_ok=True)
icc = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
scene = Image.open(SRC / 'P01_PC.png').convert('RGB')
box = (355, 70, 1775, 762)
scene = scene.crop(box).resize((1600, 780), Image.Resampling.LANCZOS)
scene.save(EDIT / '日间场景_封面裁切.png', icc_profile=icc)
def data(path, mime):
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<title>NED Eric｜无线氛围灯电商视觉系统</title>
<desc>自发概念项目，AI 辅助设计。日间家居场景中的完整灯体，与左侧项目标题及底部交付范围。</desc>
<defs><style>
@font-face{{font-family:DM;src:url('{data(SRC/'DMSans-VF.ttf','font/ttf')}')}}
text{{font-family:DM,'Microsoft YaHei',sans-serif;fill:#302d28}}
.cn{{font-family:'Microsoft YaHei',sans-serif}}
</style></defs>
<rect width="1600" height="900" fill="#f3efe7"/>
<image id="scene" width="1600" height="780" href="{data(EDIT/'日间场景_封面裁切.png','image/png')}"/>
<image id="existing-logo-redraw" x="80" y="60" width="100" height="57" href="{data(LOGO/'NED_原样重绘_黑_紧边.svg','image/svg+xml')}"/>
<text x="218" y="96" font-size="17" font-weight="500" letter-spacing="2">DESIGN CASE STUDY</text>
<text x="76" y="365" font-size="174" font-weight="500" letter-spacing="-8">Eric.</text>
<text class="cn" x="84" y="442" font-size="38" font-weight="400">无线氛围灯电商视觉系统</text>
<text x="86" y="484" font-size="18" font-weight="400" letter-spacing="2.5">E-COMMERCE VISUAL SYSTEM</text>
<path d="M80 780H1520" stroke="#ded7cc" stroke-width="1"/>
<text class="cn" x="82" y="849" font-size="23">商品图 / A+ 内容 / Banner 系统</text>
<text class="cn" x="1518" y="848" text-anchor="end" font-size="18" style="fill:#666056">自发概念项目 · AI 辅助设计</text>
</svg>'''
(EDIT/'NED_Eric_项目封面_V01_可编辑.svg').write_text(svg, encoding='utf-8')
shutil.copy2(SRC/'DM-Sans-OFL.txt', EDIT/'DM-Sans-OFL.txt')
manifest = {
    'version': 'V01', 'status': '待审阅的项目封面试排', 'size': [1600,900],
    'source': 'Existing AI scene P01_PC.png, 1959×803',
    'crop_box': list(box), 'scene_output': [1600,780],
    'processing': 'Uniform crop and ~1.127× interpolation; no new generation, no product reshaping, no white overlay',
    'logo': 'Existing ned. wordmark contour redraw, unchanged shapes',
    'fonts': 'DM Sans embedded with OFL; Microsoft YaHei referenced locally, not distributed',
    'editable': 'SVG live text; scene and existing logo embedded images',
}
(OUT/'制作记录.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'README.md').write_text('''# NED Eric｜项目封面 V01

1600×900，16:9。作品集封面试排，待审阅。

![封面](NED_Eric_项目封面_V01_1600x900.jpg)

- 使用已有日间场景重新裁切和排版，保留完整灯体及原产品比例；没有新增 AI 生图。
- 左侧项目名称，右侧产品场景，底部列交付范围和项目性质；未将超宽 Banner 直接裁作封面。
- 原始场景 1959×803，裁切 1420×692 后等比插值为 1600×780；输出尺寸不代表新增真实细节。
- Logo 使用既有字标的原样轮廓重绘，不代表原创 Logo 设计或官方品牌合作。
- PNG/JPEG 为审阅图；SVG 为文字可编辑源稿，摄影场景为嵌入位图，并非分层摄影 PSD。
- SVG 嵌入 DM Sans（附 OFL），中文使用本机 Microsoft YaHei；跨平台编辑若缺字体需安装或指定替代，已导出图片不受影响。
- 本地交付，尚未推送 GitHub；没有覆盖先前版本。
''',encoding='utf-8')
shutil.copy2(Path(__file__), EDIT/'build_ned_portfolio_cover.py')
print(OUT)
