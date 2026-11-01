"""Embed the third proposal: original styling, changed structure without changing the earlier review."""
import base64
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
TOOLS=next(p for p in HERE.parents if (p/'plugins/haipipe-toolkit').is_dir())
sys.path.insert(0,str(TOOLS/'plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts'))
from draw import Drawing,canvas
canvas.assign_ids=lambda els:els
d=Drawing()
f=d.frame('Studio layout v4 / annotated proposal',2280,1600);f['id']='s-studio-layout-v4-frame';d.fid=f['id']
t=d.text(40,20,'Shared navigation on the right; page-specific views below the title. Proposal.',28);t['id']='s-studio-layout-v4-note'
p=HERE/'assets/studio-layout-proposal-v4-20261028.png'
fid='studio-layout-proposal-v4-20261028'
d.files[fid]={'id':fid,'mimeType':'image/png','created':1,'dataURL':'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()}
e=d.el('image',40,80,2200,2200*2/3,fileId=fid,status='saved',scale=[1,1],locked=True);e['id']='s-studio-layout-v4-image'
d.write(HERE/'studio-layout-v4.excalidraw',Path(__file__).name)
