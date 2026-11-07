from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageCms
import json,base64,shutil,hashlib,xml.etree.ElementTree as ET
from html import escape

R=Path('D:/WLQ/AIGC作品集');O=R/'outputs/NED_高级A+_V03_20261107';P=O/'01_成品与预览';E=O/'02_可编辑SVG';L=O/'04_过程记录'
NS='http://www.w3.org/2000/svg';ET.register_namespace('',NS)
items=json.loads((L/'渲染清单.json').read_text(encoding='utf-8'));sizes={i['id']:i['size'] for i in items}
FONT=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
order=['P01','P02','P03C','P04B','P05','P06']
longs=[]
for v,w in [('PC',1952),('Mobile',600)]:
 keys=[sid+'_'+v if sid!='P02' or v=='PC' else 'P02_Finish_Mobile' for sid in order]
 h=sum(sizes[k][1] for k in keys)
 root=ET.Element('{'+NS+'}svg',dict(width=str(w),height=str(h),viewBox=f'0 0 {w} {h}'))
 ET.SubElement(root,'{'+NS+'}title').text='NED Eric Lamp Premium A+ V03 continuous '+v+' concept — pending user review'
 y=0
 for n,k in enumerate(keys):
  child=ET.parse(E/(k+'.svg')).getroot();prefix=k+'-'
  for el in child.iter():
   if 'id' in el.attrib:el.set('id',prefix+el.get('id'))
   for attr,value in list(el.attrib.items()):
    if 'url(#' in value:el.set(attr,value.replace('url(#','url(#'+prefix))
  child.set('x','0');child.set('y',str(y));root.append(child);y+=sizes[k][1]
 ET.ElementTree(root).write(E/f'NED_V03_连续长页_{v}.svg',encoding='utf-8',xml_declaration=True)
 # PNG tiles come from the same SVG render; no separate overlay source.
 canvas=Image.new('RGB',(w,h));y=0
 for k in keys:
  im=Image.open(P/'图文预览'/(k+'.png')).convert('RGB');canvas.paste(im,(0,y));y+=im.height
 preview=canvas.resize((1600,round(h*1600/w)),Image.Resampling.LANCZOS) if v=='PC' else canvas
 preview.save(P/f'NED_V03_连续长页_{v}.jpg',quality=94,subsampling=0)
 if v=='PC':
  small=canvas.copy();small.thumbnail((1100,5000));small.save(P/'V03_整页预览.jpg',quality=93)
 longs.append(dict(id=v,size=[w,h],file=f'NED_V03_连续长页_{v}.svg',defaultStates=keys))

# User-facing review index uses all states; adjacent buttons are review controls,
# not a promise of Amazon's real editor or consumer interaction.
html='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NED 高级A+ V03 审阅</title><style>
*{box-sizing:border-box}body{margin:0;background:#eee9df;color:#302e2a;font:15px "Microsoft YaHei",Arial,sans-serif}header{padding:22px 5%;background:#f7f4ed}h1{font-size:23px;margin:0 0 9px}p{line-height:1.6;margin:8px 0}nav{display:flex;gap:9px;flex-wrap:wrap;margin:14px 0 0}button{font:inherit;border:1px solid #b9b09f;border-radius:22px;background:transparent;padding:8px 19px;color:inherit;cursor:pointer}button[aria-pressed=true]{background:#3e4944;color:#fff;border-color:#3e4944}main{max-width:1600px;margin:24px auto;background:#e7dfd2}main.mobile{max-width:390px}section{position:relative;margin:0}section img{width:100%;display:block}section .switch{display:flex;gap:7px;justify-content:center;padding:11px;background:#e7dfd2}.switch button{font-size:13px;padding:6px 16px}footer{padding:22px 5%;font-size:13px}a{color:#465e4e}#all{display:none;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;padding:22px}#all figure{margin:0}#all img{width:100%;height:320px;object-fit:contain;object-position:top;background:#e7dfd2}figcaption{padding:8px}
</style><header><h1>NED Eric Lamp｜高级 A+ V03</h1><p>待用户审稿。可切换电脑、手机及全部状态；操作和场景按钮用于审阅不同画面。本地模拟预览，平台后台尚待核验。</p><nav><button id="desktop" aria-pressed="true">电脑</button><button id="mobile" aria-pressed="false">手机</button><button id="overview" aria-pressed="false">全部状态</button><a href="../使用说明.md">使用说明</a></nav></header><main id="page"></main><div id="all"></div><footer>摄影内容为位图，文字、色温条、箭头和尺寸线在SVG中独立编辑。平台纯图素材与作品集图文预览分开保存。</footer><script>'''
html+='const sizes='+json.dumps(sizes)+';'
html+='''
let mode='PC';const state={P02:'Finish',P03:'C',P04:'B'};
const groups=[['P01',null],['P02',[['Knob','Top knob'],['Finish','Sand Cashmere']]],['P03',[['A','Press'],['B','Turn'],['C','Press & turn']]],['P04',[['A','Dining'],['B','Bedside'],['C','Terrace']]],['P05',null],['P06',null]];
function key(id){if(id==='P02')return mode==='PC'?'P02_PC':'P02_'+state.P02+'_Mobile';if(id==='P03'||id==='P04')return id+state[id]+'_'+mode;return id+'_'+mode}
function draw(){document.querySelector('#page').className=mode==='Mobile'?'mobile':'';document.querySelector('#page').innerHTML='';for(const [id,options] of groups){let s=document.createElement('section');s.dataset.module=id;let img=document.createElement('img');img.alt=id+' '+mode;img.src='图文预览/'+key(id)+'.png';s.append(img);if(options && !(id==='P02'&&mode==='PC')){let bar=document.createElement('div');bar.className='switch';for(const [v,label] of options){let b=document.createElement('button');b.textContent=label;b.setAttribute('aria-pressed',String(state[id]===v));b.onclick=()=>{state[id]=v;draw()};bar.append(b)}s.append(bar)}document.querySelector('#page').append(s)}}
function select(id){for(const x of ['desktop','mobile','overview'])document.getElementById(x).setAttribute('aria-pressed',String(x===id));document.querySelector('#page').style.display=id==='overview'?'none':'block';document.querySelector('#all').style.display=id==='overview'?'grid':'none';if(id!=='overview'){mode=id==='mobile'?'Mobile':'PC';draw()}}
document.querySelector('#desktop').onclick=()=>select('desktop');document.querySelector('#mobile').onclick=()=>select('mobile');document.querySelector('#overview').onclick=()=>select('overview');for(const k of Object.keys(sizes)){let f=document.createElement('figure');f.innerHTML='<figcaption>'+k+'</figcaption><a href="图文预览/'+k+'.png"><img src="图文预览/'+k+'.png" alt="'+k+'"></a>';document.querySelector('#all').append(f)}draw();
</script></html>'''
(P/'打开审阅V03.html').write_text(html,encoding='utf-8')

# Focused edge crops include the source and all flagged modules at 2–3×.
edges=[('原始照片，仅作细暗线依据',O/'03_原始素材/参考素材/产品_正面近景.jpg',(300,790,720,925)),('P02_PC',P/'平台纯图素材/P02_PC.jpg',(280,590,650,720)),('P02_Finish_Mobile',P/'平台纯图素材/P02_Finish_Mobile.jpg',(185,368,415,438)),('P04A_PC',P/'平台纯图素材/P04A_PC.jpg',(770,620,1050,715)),('P04A_Mobile',P/'平台纯图素材/P04A_Mobile.jpg',(488,820,775,942)),('P04B_PC',P/'平台纯图素材/P04B_PC.jpg',(1120,618,1390,700)),('P04B_Mobile',P/'平台纯图素材/P04B_Mobile.jpg',(640,807,945,900)),('P04C_PC',P/'平台纯图素材/P04C_PC.jpg',(1210,654,1420,720)),('P04C_Mobile',P/'平台纯图素材/P04C_Mobile.jpg',(810,828,1045,915)),('P05_PC',P/'平台纯图素材/P05_PC.jpg',(1400,590,1690,680)),('P05_Mobile',P/'平台纯图素材/P05_Mobile.jpg',(725,805,1020,920))]
board=Image.new('RGB',(1500,((len(edges)+1)//2)*330),'#ede7dd');d=ImageDraw.Draw(board)
for i,(name,f,box) in enumerate(edges):
 crop=Image.open(f).crop(box);scale=min(3,710/crop.width,270/crop.height);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST);x=22+i%2*750;y=20+i//2*330;d.text((x,y),name+f' / {scale:.1f}×',font=FONT,fill='#302e2a');board.paste(crop,(x,y+39))
board.save(L/'产品底部_放大复核.jpg',quality=97,subsampling=0)

# Save complete outputs; prepared-but-not-submitted prompts must not be mistaken
# for executed inputs. This ledger explicitly records the successful image files.
g=R/'output/imagegen/NED_Premium_V03_20261107';files=sorted(g.glob('*.png'))
ledger=[]
for f in files:
 name=f.stem;prompt=L/'实际生成输入'/(name+'.txt')
 ispatch=name.endswith('_basefix')
 if ispatch:prompt=L/'实际生成输入'/(name.replace('_basefix','_底座修复')+'.txt')
 rec=dict(output='03_原始素材/实际生成原图/'+f.name,prompt='04_过程记录/实际生成输入/'+prompt.name,size=list(Image.open(f).size),status='actual_image_returned',model='gpt-image-2.5-sunburst',provider='https://www.apophiscode.com/v1',selected=f.name not in ['P05_PC.png','P05_PC_r2.png','P03B_Mobile.png'],role='local_repair_patch' if ispatch else 'scene_image')
 if ispatch:refs=['03_原始素材/制作素材/'+name.replace('_basefix','_底座修复输入')+'.png']
 elif name in ['P05_PC']:refs=['outputs/NED_高级A+_V02_20261107/03_原始素材/素材原图/P05_PC_r2.png','03_原始素材/参考素材/产品_正面近景.jpg']
 elif name=='P05_PC_r2':refs=['03_原始素材/参考素材/产品_正面近景.jpg','outputs/NED_高级A+_V02_20261107/03_原始素材/素材原图/P05_PC_r2.png']
 elif name=='P05_PC_r3':refs=['03_原始素材/制作素材/P05_PC_宽幅扩展底稿.png','03_原始素材/参考素材/产品_正面近景.jpg']
 elif name=='P05_Mobile_r2':refs=['03_原始素材/参考素材/产品_正面近景.jpg','outputs/NED_高级A+_V02_20261107/03_原始素材/素材原图/P05_Mobile.png']
 elif name in ['P03A_PC','P03C_PC','P03B_Mobile_r2']:refs=['03_原始素材/实际生成原图/P03B_PC.png','03_原始素材/参考素材/产品_正面近景.jpg']
 elif name in ['P03A_Mobile','P03C_Mobile']:refs=['03_原始素材/实际生成原图/P03B_Mobile_r2.png','03_原始素材/参考素材/产品_正面近景.jpg']
 elif name.startswith('P04') and name.endswith('Mobile'):refs=['03_原始素材/实际生成原图/'+name.replace('Mobile','PC')+'.png','03_原始素材/参考素材/产品_正面近景.jpg','03_原始素材/参考素材/人物_'+('F01' if name.startswith('P04B') else 'M01')+'.png']
 else:
  task=next(j for j in json.loads((L/'生成任务.json').read_text(encoding='utf-8')) if j['id']==name);refs=task['references']
 rec['inputImagesInOrder']=refs;ledger.append(rec)
(L/'实际生成记录.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
tasks=json.loads((L/'生成任务.json').read_text(encoding='utf-8'))
for j in tasks:j['status']='completed_with_selected_revision' if any(x['selected'] and Path(x['output']).stem.startswith(j['id']) for x in ledger) else 'prepared_not_submitted'
(L/'生成任务.json').write_text(json.dumps(tasks,ensure_ascii=False,indent=2),encoding='utf-8')
content=json.loads((L/'模块内容.json').read_text(encoding='utf-8'))
md='# V03 平台字段候选\n\n美国站作品集模拟；数值为既有资料标称，不表示实测或真实后台已验证。图片与原生字段分开，叠字预览不是可直接整页上传的素材。\n\n'
for sid,c in content['copy'].items():md+='## '+sid+'\n\nTitle: '+' '.join(c['title'])+'\n\nDescription: '+c['body'].replace('\n',' ')+'\n\n'
for c in content['hotspots']:md+='## P02 '+c['id']+'\n\nTitle: '+c['title']+'\n\nDescription: '+c['body']+'\n\n'
for q,a in content['faq']:md+='## P06 '+q+'\n\n'+a+'\n\n'
(P/'平台字段候选.md').write_text(md,encoding='utf-8')
(L/'长页组成.json').write_text(json.dumps(longs,ensure_ascii=False,indent=2),encoding='utf-8')
for n in ['prepare_ned_v03_production.py','build_ned_v03_details.py','build_ned_v03_delivery.py','finish_ned_v03_package.py','render_ned_v03.cjs','compose_ned_v03_base_repairs.py','check_ned_v03_review.cjs']:
 shutil.copy2(R/'work'/n,L/n)
print(json.dumps(dict(longPages=longs,actualReturnedImages=len(ledger),selectedSceneImages=sum(x['selected'] and x['role']=='scene_image' for x in ledger),localRepairPatches=sum(x['role']=='local_repair_patch' for x in ledger)),ensure_ascii=True))
