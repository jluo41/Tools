"""Reference-style native diagrams, 261027; words live in the topic face.

No canvas frame or global group. Pale local zone and editable cards. Generate through
canvas.write to preserve human marks. Explicit ordinal IDs, no content hashes.
"""
import json
import re
import sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / '../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts').resolve()))
from draw import Drawing, canvas

INK='#29394a'
MUTED='#73859c'
BLUE='#287eb8'
PURPLE='#8563c6'
TEAL='#39887d'
GOLD='#bd812b'


def build(w):
    d=Drawing()
    d.text(45, 28, w['title'], 48, INK)
    d.text(48, 98, w['subtitle'], 27, MUTED)
    # The only large rectangle is a local collaboration zone, never an outer frame.
    d.box(520, 185, 990, 870, color='#e1bf80', fill='#fff9ed', sw=1.3)
    d.text(550, 210, w['zone'], 30, GOLD)
    d.text(550, 260, w['zone_note'], 23, MUTED)
    d.text(50, 240, 'Inputs and context', 28, PURPLE)
    d.text(1580, 240, w['output_label'], 28, BLUE)

    def card(key,x,y,width,height,fill,stroke,accent):
        start=len(d.els)
        v=w['nodes'][key]
        d.box(x,y,width,height,color=stroke,fill=fill,sw=1.3)
        d.text(x+24,y+24,v['icon'],32)
        yy=d.para(x+74,y+25,v['title'],width-98,30,accent)+26
        for line in v['body'].split('\\n'):
            yy=d.para(x+24,yy,line,width-48,26,INK)+10
        assert yy <= y+height-10,(key,yy,y+height)
        for i,e in enumerate(d.els[start:]):
            e['id']=f"s-{w['file']}-card-{key}-{i}"
            e['groupIds']=[f'node-{key}']

    card('idea',50,320,400,270,'#f5f0ff','#b8a2df',PURPLE)
    card('source',50,740,400,240,'#f5f0ff','#b8a2df',PURPLE)
    card('agent',550,320,410,270,'#fff1bb','#dfb75d',INK)
    card('human',1070,320,410,270,'#eef8f5','#96c7bb',INK)
    card('guide',1070,740,410,290,'#ffffff','#96c7bb',TEAL)
    card('result',1580,390,435,335,'#eef6ff','#9bbfdf',BLUE)

    def arrow(points,key,tx,ty,color=BLUE,dashed=False,width=200):
        d.line(points,color=color,dashed=dashed,sw=1.8)
        d.para(tx,ty,w['arrows'][key],width,23,color)

    arrow([(450,430),(550,430)],'input',455,350,width=96)
    arrow([(960,430),(1070,430)],'ask',982,382,width=88)
    arrow([(1275,590),(1275,740)],'approve',1295,648,TEAL,width=160)
    arrow([(1480,860),(1540,860),(1540,550),(1580,550)],'apply',1558,770,BLUE,width=170)
    arrow([(1070,850),(1010,850),(1010,665),(755,665),(755,590)],'loop',790,680,PURPLE,True,width=230)
    arrow([(450,855),(490,855),(490,620),(650,620),(650,590)],'source',525,645,PURPLE,True,width=210)

    # A short takeaway in the output lane replaces long floating annotations.
    d.para(1580,875,w['takeaway'],435,30,BLUE)
    d.text(50,1100,w['note'],26,INK)
    d.text(50,1150,w['status'],22,MUTED)
    for i,e in enumerate(d.els):
        if not e['id'].startswith('s-'):
            e['id']=f"s-{w['file']}-reference-{i}"
        e['roughness']=0
    canvas.assign_ids=lambda els:els
    out=HERE/(w['file']+'.excalidraw')
    d.write(out,Path(__file__).name)
    scene=json.loads(out.read_text())
    els=[e for e in scene['elements'] if not e.get('isDeleted')]
    assert not any(e['type']=='frame' or e.get('frameId') for e in els)
    assert not any(e['type']=='image' for e in els)
    assert len({e['id'] for e in els})==len(els)
    print(f"Verified {out.name}: {len(els)} native elements, no outer frame")


def main():
    face=(HERE/'s03-agent-role.md').read_text()
    words=yaml.safe_load(re.search(r'(?ms)^```yaml\n(.*?)^```',face).group(1))
    for w in words['flows']:build(w)


if __name__=='__main__':main()
