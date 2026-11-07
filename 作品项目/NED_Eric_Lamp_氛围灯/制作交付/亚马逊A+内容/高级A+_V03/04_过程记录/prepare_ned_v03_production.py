from pathlib import Path
import json, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageCms

R=Path('D:/WLQ/AIGC作品集')
O=R/'outputs/NED_高级A+_V03_20261107'
G=R/'output/imagegen/NED_Premium_V03_20261107'
REF=O/'03_原始素材/参考素材'
INP=O/'04_过程记录/实际生成输入'
for p in [REF,INP,G,O/'01_成品与预览/平台纯图素材',O/'01_成品与预览/图文预览',O/'02_可编辑SVG',O/'03_原始素材/制作素材']:
 p.mkdir(parents=True,exist_ok=True)
oldref=R/'outputs/NED_高级A+_V02_制作准备_20261107/参考素材'
for n in ['产品_正面近景.jpg','产品_用户斜俯视.png','产品_用户略仰视.png','产品_旋钮按压.jpg','人物_F01.png','人物_M01.png']:
 shutil.copy2(oldref/n,REF/n)
shutil.copy2(R/'outputs/NED_高级A+_V02_制作准备_20261107/参考来源.json',O/'04_过程记录/沿用参考来源.json')

scenes={
'P01':('F01','Use a low, close three-quarter tabletop camera. One complete small lamp in the right foreground at about 66% of the frame width, knob and entire base visible, resting on a modest walnut side table. The lamp occupies about 65% of image height through foreground perspective, not by becoming oversized. Behind it in soft focus, only a partial torso of the existing woman in slate-blue sweater on a sofa, putting down one closed book away from the lamp. Crop her head or keep it distant and unobtrusive. Quiet limestone/bone plaster and subtle window shadows. One book is the only prop. Daylight, restrained localized warm lamp light. Preserve a calm left 38% area for short copy, with natural wall texture, no panel.'),
'P03A':('F01','Shoulder-side slightly elevated close photograph of the lamp top, the whole domed shade and only part of its slender stem. Show just the adult woman\'s natural right hand and slate-blue fine-knit cuff, never a face or body portrait. Her extended index fingertip touches the top of the original knob in a gentle press, with other fingers relaxed and bent away; the knob remains identifiable under the fingertip. Warm neutral side-table environment, soft daylight. The whole lamp base may be outside this intentional close crop. Hand/knob contact near 68% width, shade below, quiet lower-left copy area. No whole room scene.'),
'P03B':('F01','Shoulder-side slightly elevated close photograph of the lamp top, whole domed shade and part of stem. Only the existing adult woman\'s right hand with slate-blue fine-knit cuff, no face or torso. Thumb and index finger touch opposite SIDES of the small original top knob, visibly poised to rotate it; keep the front of the knob visible between fingertips. Fingers anatomically coherent, remaining fingers gently curved away above the shade, never penetrating it. Warm neutral tabletop context, soft natural window light. Hand/knob around 68% width, shade lower right, quiet lower-left area for copy. No full-room portrait and no lamp base needed in this close crop.'),
'P03C':('F01','Same shoulder-side slightly elevated close camera, slate-blue cuff, neutral walnut table and soft window light as the other operation states. Only hand, original top knob, complete domed shade and part of stem. Thumb and index finger lightly grip the SIDES of the same knob while the index is positioned over its rounded top for a gentle combined downward-and-turning action. Knob visible, one anatomically plausible hand, no extra fingers. The photograph illustrates the contact; later editable arrows explain the compound action. Hand/knob around 68% width. Reserve calm left area for title, brief copy and a later color-temperature bar; do not generate any bar or writing. No face, whole body or new scene.'),
'P04A':('M01','Slightly elevated oblique dining tabletop camera, distinct from a sofa portrait. One small complete lamp in foreground at about 62% width with physical contact on walnut, height about 55% image. Only a terracotta-sweater forearm/partial torso of the existing adult man at the far right adjusts one linen napkin next to a modest ceramic plate, far from the lamp knob. No visible face, no large vase, no crowded meal spread, no second lamp. Early evening natural warm-neutral light, lamp sand finish remains neutral. Calm left third has quieter wall/table surfaces for copy. Lamp and plate proportions fit a 20cm lamp.'),
'P04B':('F01','Side view at bedside with a clearly recognizable blue-grey linen bed receding into the left background. A walnut bedside table in right foreground supports one complete small lamp, around 66% width. Only the existing woman\'s slate-blue sleeve and hand enters from upper right to place a closed book to the RIGHT of the lamp; no touching the knob and no front-facing seated portrait. Low blue-grey dusk and local gentle warm light, retain visible sand metal body, natural non-emissive stem and thin subtle contact shadow. Calm darker left third supports pale copy. Keep full base with real thickness and no new black ring.'),
'P04C':('M01','A wider lateral architectural view of a dry sheltered home terrace at dusk, visible roof beam or covered doorway in upper background and a receding planted courtyard beyond; no rain or wet surfaces. One small complete sand lamp on a reliable walnut outdoor side table toward right-middle foreground, about 47% image height. Existing adult man in terracotta sweater is further back at far right, seen sideways only partly while setting down a simple cup away from the knob. No front-facing dining portrait. Different wider spatial camera from indoor dining, plant/covered architecture establishes terrace. Blue-grey dusk with restrained warm local lamp glow. Calm dark left third for copy.'),
}
jobs=[]
for sid,(person,scene) in scenes.items():
 for variant in ['PC','Mobile']:
  refs=[REF/'产品_正面近景.jpg',REF/'产品_用户斜俯视.png',REF/f'人物_{person}.png']
  if sid.startswith('P03'):refs=[REF/'产品_正面近景.jpg',REF/'产品_旋钮按压.jpg',REF/'产品_用户斜俯视.png']
  framing=('Create a single wide 1952 x 800 photograph, approximately 2.44:1. Copy is added later in left negative space. Keep product and action safely inside the frame.' if variant=='PC' else 'Create an independently composed 1440 x 1080 landscape 4:3 mobile photograph. Tighten distances between the product and relevant sleeve/prop; do not squeeze a wide image. No large blank copy area needed: text will be below the image. Keep the whole shade and essential action visible; for non-operation scenes the entire lamp and base must remain visible. The same contextual scene and camera intent apply, but prioritize product at 55–72% of image height and crop faces/torso rather than shrinking the lamp.')
  roles='Image 1: actual product photograph, authoritative visible silhouette, color and proportions. Image 2: supporting angle'+(', actual knob press photograph showing contact, NOT a request to copy its beige sleeve. Image 3: supporting product angle.' if sid.startswith('P03') else '. Image 3: existing fictional AI character identity and clothing, not product geometry.')
  prompt=f'''Use case: photorealistic-natural
Asset type: NED Eric Lamp Premium A+ V03 / {sid} / {variant}, photographic portfolio concept.
Primary request: Produce one refined editorial product lifestyle PHOTOGRAPH using reference product identity and the specified new composition.
Input roles: {roles}
Scene and camera: {scene}
Framing: {framing}
SKU invariants: Exactly ONE small Sand Cashmere Eric table lamp. Same smooth sand-colored powder-coated aluminum domed shade, original small rounded vertical top knob, straight slender metal stem and low round base. Approximately 20.1cm tall and 11cm wide. Preserve credible proportions, no large reading lamp. The stem is opaque sand metal, NEVER an emitting luminous tube. Shade illumination stays beneath the dome, no bright outline.
Edge requirement: Natural photographic transitions and local shading, NO artificial black outline, no added black rubber band, no black circular component beneath the base, no white halo, no glowing rim, no aggressive sharpening. Preserve the low base thickness and physically plausible contact shadow. Dark values belong only to natural shadow where light requires, not uniform contour lines. Do not stylize product with illustrated edge strokes.
Lighting and finish: Natural soft photographic lighting, sand finish distinguishable from background through local tone. No global orange cast, no chrome or high-gloss redesign. Bone, walnut, restrained blue-grey and terracotta project palette. Product edges stay optically sharp without ringing.
Text: NONE. No logo, letters, numbers, arrows, labels, infographic bars, panels, charts or UI; all final graphics are composed separately in SVG.
Avoid: duplicated lamps; malformed hands or fused fingers; fingers passing through shade; oversized knob; new controls, charging ports, cables or hidden hardware; huge foreground faces; staged smiling portrait; three-panel collage; huge dark base band; fake microtexture; rain; RGB/blue illumination.
'''
  name=f'{sid}_{variant}';(INP/(name+'.txt')).write_text(prompt,encoding='utf-8')
  jobs.append({'id':name,'references':[str(p.relative_to(R)) for p in refs],'promptFile':str((INP/(name+'.txt')).relative_to(R)),'status':'prepared_not_submitted','requestedSize':'auto','targetSize':[1952,800] if variant=='PC' else [1440,1080]})

for variant in ['PC','Mobile']:
 old=R/'outputs/NED_高级A+_V02_20261107/03_原始素材/素材原图'/('P05_PC_r2.png' if variant=='PC' else 'P05_Mobile.png')
 prompt=f'''Use case: precise-object-edit
Asset type: NED Premium A+ V03 P05 {variant} photographic image repair.
Image 1 is the V02 edit target. Image 2 is the authoritative actual product photograph. Repair Image 1 for the revised size module.
Change only these issues: remove the person, hand and sleeve completely, continue the existing wall and table naturally in that area. Keep one closed book. Repair the lamp dome, stem and base so sand metal has soft real photographic transitions with NO artificial black contour, white halo or glowing outline. Stem must be opaque sand-colored metal, NOT a glowing tube. Remove the invented thick black band at the base; preserve its real sand side thickness and subtle natural contact shadow. Preserve a stable contact with the table, no levitation. Keep the same lamp placement, complete visible silhouette, table, book, dusk palette and background camera. Keep left space available for editable title and dimensions. Do not redesign the product; use actual reference for material and visible shape. No words, lines, measurements, logo, arrows or panels. Output one {'1952x800 wide 2.44:1' if variant=='PC' else '1440x1080 4:3'} photograph.
'''
 name=f'P05_{variant}';(INP/(name+'.txt')).write_text(prompt,encoding='utf-8')
 jobs.append({'id':name,'references':[str(old.relative_to(R)),str((REF/'产品_正面近景.jpg').relative_to(R))],'promptFile':str((INP/(name+'.txt')).relative_to(R)),'status':'prepared_not_submitted','requestedSize':'auto','targetSize':[1952,800] if variant=='PC' else [1440,1080]})
(O/'04_过程记录/生成任务.json').write_text(json.dumps(jobs,ensure_ascii=False,indent=2),encoding='utf-8')
(O/'04_过程记录/制作记录.md').write_text('# V03 制作记录\n\n阶段：制作中，尚未交付用户审稿。\n\n使用用户指定的 Apophis API，模型标识 gpt-image-2.5-sunburst；模型别名不证明后台模型身份。按规划执行19份图片槽位、21份逐图SVG及预览。P02采用真实照片，其他素材采用实际生图或修复，不用占位图冒充成品。\n\n尚未记录成功生成结果。凭据仅从本机用户环境载入，不写入文件。\n',encoding='utf-8')
print('V03 references and 16 prompts prepared.')
