"""Build an annotated layout discussion; preserve all human canvas marks."""
import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / 'plugins/haipipe-toolkit').is_dir())
sys.path.insert(0, str(TOOLS / 'plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts'))
from draw import Drawing, canvas
canvas.assign_ids = lambda elements: elements  # Explicit IDs; no content hashes.

class NamedDrawing(Drawing):
    def el(self, *a, **kw):
        element = super().el(*a, **kw)
        element['id'] = 's-layout-review-' + str(len(self.els))
        return element

d = NamedDrawing()
RED = '#c92a2a'
GREEN = '#35644d'
GRAY = '#68746d'

def image(name, x, y, w, h):
    path = HERE / 'assets' / name
    fid = path.stem
    d.files[fid] = {'id': fid, 'mimeType': 'image/png', 'created': 1,
                    'dataURL': 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode()}
    d.el('image', x, y, w, h, fileId=fid, status='saved', scale=[1, 1], locked=True)

def note(x, y, title, words, width=650):
    text = d.wrap(words, width-40, 27)
    h = 80 + len(text.splitlines()) * 34
    d.box(x, y, width, h, color=RED, fill='#fff5f5')['roughness'] = 1
    d.text(x+20, y+14, title, 34, RED)
    d.text(x+20, y+65, text, 27)

f = d.frame('Top / left / right: proposed responsibilities', 2700, 1600)
d.text(50, 35, 'Where am I?  /  Where else?  /  What do I want to see?', 48)
d.text(50, 105, 'Current screenshot + editable annotations. Navigation choices remain proposals.', 27, GRAY)
image('studio-current-20261028.png', 50, 180, 1158, 942)
# Exact screenshot regions, unchanged image underneath.
for x,y,w,h in [(56,199,1135,57),(56,267,800,45),(68,337,640,52),(58,446,45,305),(1152,322,45,120),(72,790,1048,285)]:
    d.box(x,y,w,h,color=RED,sw=2)['roughness']=1

note(1320,180,'TOP / location + purpose',
     'Breadcrumb first. Then the current title and one sentence about this Block. Show Studio / All as a plain heading, not another selector.', 1260)
d.line([(1320,245),(1260,245),(1191,228)], color=RED, sw=2)
note(1320,420,'LEFT / other Blocks',
     'Quiet short bars. Hover or keyboard focus reveals sibling names; click opens one. At Job level, this becomes sibling Jobs. Children stay in the main content.', 750)
d.line([(1320,510),(1250,510),(1250,1140),(35,1140),(35,590),(58,590)],color=RED,sw=2)
note(1320,680,'RIGHT / this Block',
     'One section navigator. Studio groups live here too. Folder replaces Disk; Runs is a section for execution. Remove the separate Disk / Runs strip.',750)
d.line([(1320,775),(1230,775),(1230,380),(1197,380)],color=RED,sw=2)

# Open state of the single right navigator, adjacent to the proposal.
d.box(2150,420,430,690,color=GREEN,fill='#f5f8f5')['roughness']=1
d.text(2180,445,'RIGHT / revealed on hover',27,GREEN)
for i,label in enumerate(['Overview','Questions / Reports','Jobs (when present)','Studio / All','Studio / Interface','Studio / Navigation','Runs','Timeline','Folder']):
    yy=505+i*53
    if label=='Studio / All': d.box(2170,yy-5,390,45,sw=0,fill='#e8f0e8')
    d.text(2190,yy,label,27)
d.line([(2180,1000),(2545,1000)],color=GRAY,arrow=False)
d.text(2190,1030,'Guide',27)
d.text(2190,1074,'... Manage groups',24,GRAY)
d.line([(2070,785),(2140,785)],color=RED,sw=2)

d.text(75,1195,'MAIN CONTENT / one topic per full-width row',36,GREEN)
d.box(75,1260,1160,220,color=GREEN,fill='#f5f8f5')['roughness']=1
d.text(100,1280,'s04  Workbench page structure',34)
d.text(100,1335,'Purpose + selected sketch shown directly',29,GRAY)
d.text(100,1395,'Draw     Mind map     Slides (only when available)',27,GREEN)
d.text(1320,1190,'Keep navigation quiet; keep the work visible.',36,GREEN)
d.text(1320,1250,d.wrap('Move setup instructions and group editing into Guide / overflow. Do not fill the main page with empty Related, Delivery or Runs panels.',1170,29),29)
d.text(1320,1380,d.wrap('Image concept on the next frame is illustrative. Use ONE right navigator; the generated picture repeats menus. Its color bars do not represent status.',1170,27),27,RED)

g = d.frame('Annotated image concept / proposal', 2600, 1600)
g['x']=2900; g['y']=140
image('studio-layout-proposal-20261028.png',2940,180,2304,1536)
d.fid=None
d.line([(2700,800),(2880,800)],color=GREEN,dashed=True,sw=2)

# Overview uses the real haipipe-mindmap renderer, captured from its static page.
# Append only: keep existing frames and human marks at their original positions.
ov = d.frame('Latest proposal / Overview with haipipe-mindmap', 2300, 1600)
ov['x'] = 300; ov['y'] = 1950
label = d.text(350, 1975, 'Overview / actual b17 questions, Studio topics and reports', 38)
label['link'] = '/blueprints/Project-Ladder/work/b17_theme_work/s04-workbench-page-structure/result/b17-overview.mindmap.html'
image('b17-overview.png', 350, 2050, 2000, 2000*992/1406)

assert len({e['id'] for e in d.els}) == len(d.els)
d.write(HERE/'studio-layout-review.excalidraw',Path(__file__).name)
