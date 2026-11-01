"""Embed the second annotated UI proposal without changing the earlier review."""
import base64
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
TOOLS=next(p for p in HERE.parents if (p/'plugins/haipipe-toolkit').is_dir())
sys.path.insert(0,str(TOOLS/'plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts'))
from draw import Drawing,canvas
canvas.assign_ids=lambda els:els
d=Drawing()
f=d.frame('Studio layout v2 / annotated proposal',2400,1680);f['id']='s-studio-layout-v2-frame';d.fid=f['id']
t=d.text(40,20,'Proposal: side navigation is shown open for discussion; normally collapsed.',28);t['id']='s-studio-layout-v2-note'
p=HERE/'assets/studio-layout-proposal-v2-20261028.png'
fid='studio-layout-proposal-v2-20261028'
d.files[fid]={'id':fid,'mimeType':'image/png','created':1,'dataURL':'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()}
e=d.el('image',40,80,2320,2320*2/3,fileId=fid,status='saved',scale=[1,1],locked=True);e['id']='s-studio-layout-v2-image'
d.write(HERE/'studio-layout-v2.excalidraw',Path(__file__).name)
