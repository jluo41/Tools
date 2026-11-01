"""Generate seven review deliveries from delivery-specs.json. No active skills are overwritten.
Run with the repository Python. --draw uses screenshots captured by verify_delivery_previews.py.
All delivery output is generated; edit this builder, preview.css, preview.js or the specification.
"""
from pathlib import Path
from html import escape as h
import argparse,json,os,sys,subprocess
HERE=Path(__file__).resolve().parent
BLOCK=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'plugins/haipipe-toolkit').is_dir())
DATA=json.loads((HERE/'delivery-specs.json').read_text())
STUDIOS=DATA['studios']

def rel(target,base):return os.path.relpath(target,base).replace(os.sep,'/')
def folder(s):return BLOCK/s['folder']
def linkdata(base):
 out=[]
 for s in STUDIOS:
  p=folder(s);x=dict(s)
  x.update(preview=rel(p/'result/delivery-preview.png',base),page=rel(p/'delivery/web/index.html',base),contract=rel(p/'delivery/web/contract.html',base),draw=rel(p/'delivery-design.png',base),scene=rel(p/'delivery-design.excalidraw',base),deck=rel(p/'delivery/deck/index.html',base),source_url=rel(ROOT/s['source'],base),studio_url='/_board/workbench?path='+str(p.relative_to(ROOT))+'&layout=focus')
  out.append(x)
 return out

def workbench():
 """The workbench's focus_page, so each preview wears the same frame as every workbench page (JL 261030)."""
 sys.path.insert(0,str(ROOT/'plugins/haipipe-toolkit/servers/_host'))
 from host_paths import bootstrap
 bootstrap()
 from live import focus_page
 return focus_page

def shell(s,body,base,view='Delivery',examples=None):
 items=linkdata(base);current=next(x for x in items if x['id']==s['id'])
 payload={'current':current,'studios':items,'examples':examples if examples is not None else [x for x in items if x['kind']!='Gallery']}
 payload['map']={'id':'root','label':'The total workflow','children':[{'id':'choose','label':'Choose the delivery','children':[{'id':'reader','label':'Name its reader','children':[],'draw':'s01'},{'id':'product','label':'Choose its form','children':[],'draw':'s04'}]},{'id':'design','label':'Explore the design','children':[{'id':'map','label':'Structure the argument','children':[],'draw':'s03'},{'id':'screen','label':'Try the page','children':[],'draw':'s08'}]},{'id':'review','label':'Review and hand over','children':[{'id':'check','label':'Check the real product','children':[],'draw':'s09'}]}]}
 content=(f'<style>{(HERE/'preview.css').read_text()}</style><div class="pv">{body}<footer>Built from the Studio’s delivery specification. <a href="{h(current['source_url'])}">View existing source</a></footer></div>'
          f'<dialog id="viewer"><div class="dialog-head"><h2 id="dialog-title">Main Draw</h2><button id="close-dialog">Close</button></div><div id="dialog-body"></div></dialog>'
          f'<script id="data" type="application/json">{json.dumps(payload).replace('<','\\u003c')}</script><script>{(HERE/'preview.js').read_text()}</script>')
 # the sNN's own frame: its rails, its Topic, Delivery's views under the title; the delivery Draw is a pop-out button
 # beside Draw and "review prototype" a tag beside the stage (JL 261030: "How to make this better.")
 page=workbench().static_page(folder(s),ROOT,{'Delivery':'preview','Contract':'contract','Slides':'slides'}[view],content,'review prototype')
 return page.replace('<!doctype html>','<!doctype html>\n<!-- GENERATED FILE: scripts/build_delivery_previews.py -->',1)

def page(s):
 if s['kind']=='Skill':
  steps=''.join(f'<button data-step="{i}" aria-pressed="false">{i+1}. {h(t)}</button>' for i,(t,_) in enumerate(s['steps']))
  checks=''.join(f'<label class="check"><input type="checkbox"><span>{h(c)}</span></label>' for c in s['checks'])
  return f'<h2>Method · work through the guide</h2><p class="muted">{h(s["product"])}</p><div class="guide-layout"><div class="steps">{steps}</div><div id="step-body" class="detail"></div></div><section class="detail"><h2>Check the delivery</h2>{checks}<p id="check-state" class="muted">Review each condition. These checks do not mark a delivery accepted.</p></section><p class="notice">Draft method for review. The installed skill has not been replaced.</p><a class="button" href="../review-guide.md" download>Download guide</a>'
 if s['id']=='s08':
  return '''<h2>Mind map · select a node to edit</h2><div class="toolbar"><button id="edit-selected">Edit selected node</button><button id="save-map">Save in browser</button><button id="export-map">Export map</button><label class="button">Import map<input id="import-map" type="file" accept="application/json,.json" hidden></label></div><p id="map-status" class="muted" role="status">Edits stay local to this browser. Export the map to share it.</p><div class="map-layout"><div class="map detail" id="map"></div><section class="detail"><h2>Selected node</h2><label for="node-label">Node text</label><input id="node-label" type="text" maxlength="180"><div class="actions"><button id="rename-node">Rename</button><button id="add-node">Add child</button><button id="remove-node">Remove leaf</button></div><p id="node-note" class="muted"></p></section></div><p class="notice">Shared workbench saving and multi-person editing are outside this prototype.</p>'''
  # s02 and galleries use one-row-per-example with real links
 label='Studio · think' if s['id']=='s02' else 'Gallery · explore examples'
 return f'<h2>{label}</h2><p class="muted">{h(s["product"])}</p><div class="toolbar"><input id="search" aria-label="Search examples" placeholder="Search by purpose or product"><select id="kind" aria-label="Filter by kind"><option value="">Every kind</option><option>Skill</option><option>Page</option></select><button id="export-examples">Export examples</button></div><p id="result-count" class="muted" role="status"></p><div id="rows"></div>'

def guide(s):
 return '<!-- GENERATED FILE: edit scripts/delivery-specs.json -->\n\n'+f'# {s["title"]}: review guide\n\nStatus: draft for review; not an installed skill.\n\n## Outcome\n\n{s["product"]}\n\nReader: {s["audience"]}\n\n## Procedure\n\n'+ '\n\n'.join(f'### {i+1}. {name}\n\n{body}' for i,(name,body) in enumerate(s['steps']))+'\n\n## Acceptance checks\n\n'+'\n'.join('- [ ] '+x for x in s['checks'])+f'\n\n## Open design choice\n\n{s["open"]}\n'

def build():
 for s in STUDIOS:
  p=folder(s);web=p/'delivery/web';deck=p/'delivery/deck';web.mkdir(parents=True,exist_ok=True);deck.mkdir(parents=True,exist_ok=True)
  examples=linkdata(web) if s['id']=='s02' else None
  (web/'index.html').write_text(shell(s,page(s),web,examples=examples))
  files=[('web/index.html','Usable product preview'),('web/contract.html','Scope and acceptance criteria'),('contract.json','Machine-readable delivery contract'),('deck/index.html','Three-slide explanation'),('review-guide.md','Reviewable procedure and checks')]
  contract='<h2>Delivery contract · review the outcome</h2><dl class="contract-list">'+''.join(f'<dt>{name}</dt><dd>{h(value)}</dd>' for name,value in [('Product',s['product']),('Reader',s['audience']),('Current state','Review prototype. Acceptance and release remain open.'),('Open choice',s['open'])])+'</dl><h2>Files handed over</h2><ul>'+''.join(f'<li><code>{name}</code>: {h(desc)}</li>' for name,desc in files)+'</ul><h2>Acceptance checks</h2><ul>'+''.join('<li>'+h(c)+'</li>' for c in s['checks'])+'</ul><button id="export-contract">Export delivery contract</button>'
  (web/'contract.html').write_text(shell(s,contract,web,'Contract'))
  (p/'delivery/contract.json').write_text(json.dumps(s,indent=2)+'\n')
  if s['id'] in ('s02','s04','s05'):
   examples=[x for x in linkdata(web) if s['id']=='s02' or x['kind']!='Gallery']
   (p/'delivery/examples.json').write_text(json.dumps(examples,indent=2)+'\n')
  (p/'delivery/review-guide.md').write_text(guide(s))
  x=next(x for x in linkdata(deck) if x['id']==s['id'])
  slides=f'<div class="toolbar"><button id="slide-prev">Previous</button><span id="slide-count"></span><button id="slide-next">Next</button></div><section class="slide"><p class="muted">01 · The outcome</p><h2>{h(s["title"])}</h2><p class="big">{h(s["product"])}</p><p>For {h(s["audience"].lower())}.</p><p class="notice">Review prototype, ready to inspect. Not yet an accepted release.</p></section><section class="slide"><p class="muted">02 · The design</p><img src="{h(x["draw"])}" alt="Main delivery Draw"></section><section class="slide"><p class="muted">03 · Try and review</p><h2>Open the product. Check the outcome.</h2><ul>'+''.join('<li>'+h(c)+'</li>' for c in s['checks'])+f'</ul><p>Open choice: {h(s["open"])}</p><a class="button primary" href="{h(x["page"])}">Try the delivery</a></section>'
  (deck/'index.html').write_text(shell(s,slides,deck,'Slides'))
 print('Generated seven product pages, seven contracts, seven guides and seven decks.')

def draw():
 sys.path.insert(0,str(ROOT/'plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts'))
 from draw import Drawing
 sys.path.insert(0,str(ROOT/'plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts'))
 import quick_draw
 for s in STUDIOS:
  p=folder(s);d=Drawing();f=d.frame('The delivery: '+s['title']);d.heading(s['title'],s['purpose'])
  d.text(40,190,'WHY',32);d.para(40,245,s['audience'],430,32)
  d.text(40,415,'SOURCE',32);d.para(40,470,'Delivery specification + real examples',430,30)
  d.text(40,650,'REVIEW',32);d.para(40,705,s['open'],430,30)
  screenshot=p/'result/delivery-preview.png'
  if screenshot.exists():d.picture(screenshot,560,185,1400,1020)
  d.text(2020,190,'HAND OVER',32);d.key(2000,230,500,300);d.para(2020,250,s['product'],460,30)
  d.text(2020,600,'PACKAGE',32);d.text(2020,650,'Web page\nConfiguration\nMain Draw\nExplanation deck',30)
  d.line([(470,510),(545,510)],sw=3);d.line([(1970,510),(2010,510)],sw=3)
  d.text(560,1260,'Source → build → preview → person reviews → accepted delivery',32)
  d.text(560,1320,'Current state: review prototype',28)
  # Stable sequential element ids; no content hashes. New drawing is separate from previous drawings.
  out=p/'delivery-design.excalidraw'
  old=json.loads(out.read_text()) if out.exists() else {};snap=p/'.delivery-design-elements.json'
  previous=json.loads(snap.read_text()) if snap.exists() else []
  old_by={e['id']:e for e in old.get('elements',[])};prev_by={e['id']:e for e in previous}
  changed={i for i,e in old_by.items() if i not in prev_by or e!=prev_by[i]}
  generated=d.els
  merged=[old_by[e['id']] if e['id'] in changed else e for e in generated]
  new_ids={e['id'] for e in generated};merged += [e for i,e in old_by.items() if i in changed and i not in new_ids]
  quick_draw.write(out,merged)
  doc=json.loads(out.read_text());doc['source']='build_delivery_previews.py';doc['files']={**old.get('files',{}),**d.files};out.write_text(json.dumps(doc)+'\n');snap.write_text(json.dumps(generated)+'\n')
  subprocess.run([sys.executable,str(ROOT/'plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py'),str(out),str(out.with_suffix('.png')),'0.65'],check=True,stdout=subprocess.DEVNULL)
 print('Generated seven editable main delivery Draws and PNG previews; existing main drawings preserved.')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--draw',action='store_true');a=ap.parse_args();draw() if a.draw else build()
