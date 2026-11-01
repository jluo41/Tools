"""One detailed, editable workflow map, requested 261027.

Text is authored in s03-agent-role-workflow.yaml. No outside frame. User-requested
large architecture-map format overrides the normal one-screen Studio limit.
Use the shared writer, explicit ordinal IDs, and preserve human marks.
"""
import json
import sys
from pathlib import Path
import yaml
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str((HERE/'../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts').resolve()))
from draw import Drawing, canvas
INK='#29394a'; MUTED='#75849a'; BLUE='#287eb8'; PURPLE='#8563c6'; TEAL='#39887d'; GOLD='#b78026'; RED='#bb4d4d'


def main():
    w=yaml.safe_load((HERE/'s03-agent-role-workflow.yaml').read_text())
    d=Drawing(); cards={}; limits=[]
    def tx(x,y,s,size=26,color=INK):return d.text(x,y,s,size,color)
    tx(50,30,w['title'],68)
    tx(52,130,w['subtitle'],32,MUTED)
    tx(52,190,w['status'],25,RED)

    def zone(key,x,y,width,height,fill,stroke):
        d.box(x,y,width,height,stroke,1.5,fill)
        title,sub=w['zones'][key]
        d.para(x+30,y+25,title,width-60,36,stroke)
        d.para(x+30,y+86,sub,width-60,25,MUTED)
    zone('inputs',50,300,680,1550,'#f7f3ff','#af96d6')
    zone('meaning',850,300,1740,1550,'#fff9ed','#d5ac67')
    zone('expression',2750,300,1740,1550,'#fff9ed','#d5ac67')
    zone('scale',4630,300,1200,1550,'#eef8f5','#83b8ae')
    zone('delivery',5940,300,780,1550,'#edf6ff','#8cb5d5')
    zone('records',50,2110,3290,510,'#f2f5f8','#a9b4c3')
    zone('evaluation',3420,2110,3300,510,'#eef8f5','#83b8ae')

    def card(key,x,y,width,height,fill='#ffffff',stroke='#b8c8d8',accent=INK,size=26,title_size=32):
        start=len(d.els); v=w['cards'][key]
        shape=d.box(x,y,width,height,stroke,1.4,fill)
        shape['id']=f's-complete-card-{key}'
        yy=d.para(x+24,y+25,v['title'],width-48,title_size,accent)+24
        for line in v['lines']:
            yy=d.para(x+24,yy,line,width-48,size,INK)+12
        limits.append((key,round(yy-y),height))
        # Bounds are checked together before writing.
        cards[key]=shape
        for i,e in enumerate(d.els[start:]):
            if e is not shape:e['id']=f's-complete-{key}-{i}'
            e['groupIds']=[f'node-{key}']

    card('entry_a',80,500,620,260,'#ffffff','#b8a2df',PURPLE)
    card('entry_b',80,820,620,380,'#ffffff','#b8a2df',PURPLE)
    card('intake',80,1320,620,430,'#ffffff','#b8a2df',PURPLE)
    for key,x in [('explore',900),('question',1480)]:card(key,x,500,480,450,'#fff1bb','#dfb75d')
    card('judge',2060,500,480,450,'#e9f6ef','#83b8ae',TEAL)
    card('conflict',900,1250,480,500,'#fff4f1','#daa49a',RED)
    card('example',1480,1250,480,500,'#ffffff','#dfb75d',GOLD)
    card('meaning_update',2060,1250,480,530,'#e9f6ef','#83b8ae',TEAL)
    for key,x in [('rewrite',2800),('execute',3380),('compare',3960)]:card(key,x,500,480,450,'#fff1bb','#dfb75d')
    for key,x in [('preservation',2800),('models',3380),('diagnose',3960)]:card(key,x,1250,480,500,'#ffffff','#dfb75d',GOLD)
    for key,x in [('qualify',4680),('batch',5260)]:card(key,x,500,480,490,'#ffffff','#83b8ae',TEAL)
    card('gates',4680,1250,480,530,'#ffffff','#83b8ae',TEAL)
    card('audit',5260,1250,480,530,'#e9f6ef','#83b8ae',TEAL)
    for key,y in [('out_guide',500),('out_labels',820),('out_report',1140),('out_open',1460)]:card(key,6000,y,660,280,'#ffffff','#8cb5d5',BLUE)
    for key,x in [('record_corpus',80),('record_rules',730),('record_decisions',1380),('record_runs',2030),('record_issues',2680)]:card(key,x,2280,620,290,'#ffffff','#a9b4c3',INK,24,30)
    for key,x in [('eval_effort',3450),('eval_semantics',4260),('eval_models',5070),('eval_protocol',5880)]:card(key,x,2280,780,290,'#ffffff','#83b8ae',TEAL,24,30)

    overflow=[v for v in limits if v[1]>v[2]-8]
    assert not overflow, overflow

    def arrow(points,label=None,lx=0,ly=0,lw=350,color=BLUE,dashed=False,detail=False):
        e=d.line(points,color=color,dashed=dashed or detail,sw=2.1 if not detail else 1.5)
        if detail:e['strokeStyle']='dotted'
        if label:d.para(lx,ly,w['labels'][label],lw,24,color)
        return e

    arrow([(700,630),(760,630),(760,1240),(600,1240),(600,1320)],'input_a',520,1185,220,PURPLE)
    arrow([(390,1200),(390,1320)],'input_b',100,1200,280,PURPLE)
    arrow([(700,1510),(805,1510),(805,725),(900,725)],'prepare',750,1060,145)
    arrow([(1720,500),(1720,445),(5920,445),(5920,1280),(6000,1280)],'audit_only',3030,451,1700,MUTED,True)
    arrow([(1380,725),(1480,725)],'explore',1386,650,96)
    arrow([(1960,725),(2060,725)],'ask',1988,675,70)
    arrow([(2300,950),(2300,1250)],'approve',2320,1090,210,TEAL)
    arrow([(2060,820),(2005,820),(2005,1100),(1140,1100),(1140,1250)],'conflict',1170,1118,360,RED,True)
    arrow([(1380,1470),(1430,1470),(1430,1020),(1720,1020),(1720,950)],'followup',1460,1045,460,PURPLE,True)
    arrow([(1820,1250),(1820,950)],'example',1845,1185,120,MUTED,detail=True)
    arrow([(2540,1470),(2670,1470),(2670,725),(2800,725)],'meaning',2610,1000,135,TEAL)
    arrow([(2300,1780),(2300,1810),(875,1810),(875,1000),(1140,1000),(1140,950)],'next_cases',1170,1770,1000,PURPLE,True)
    arrow([(3280,725),(3380,725)],'wording',3285,610,90)
    arrow([(3860,725),(3960,725)],'predictions',3864,640,95)
    arrow([(3040,950),(3040,1250)],'checks',3070,1110,180,MUTED,detail=True)
    arrow([(3620,950),(3620,1250)],'model_panel',3645,1090,250,MUTED,detail=True)
    arrow([(4200,950),(4200,1250)],'diagnosis',4220,1090,210)
    arrow([(4440,725),(4680,725)],'candidate',4485,670,190)
    arrow([(5160,725),(5260,725)],'qualified',5166,660,95)
    arrow([(4920,1250),(4920,990)],'policy',4945,1100,210,MUTED,detail=True)
    arrow([(5500,990),(5500,1250)],'audit',5525,1090,190)
    arrow([(4200,1750),(4200,1810),(2775,1810),(2775,1030),(2940,1030),(2940,950)],'wording_loop',2980,1770,1180,PURPLE,True)
    # Semantic failure uses a separate top return lane, outside the development zone.
    arrow([(4440,1500),(4540,1500),(4540,250),(2300,250),(2300,500)],'semantic_return',2900,205,1540,PURPLE,True)
    arrow([(5500,1780),(5500,1950),(1450,1950),(1450,980),(1600,980),(1600,950)],'audit_return',2680,1905,1850,PURPLE,True)
    # Release branches to the four artifacts, without cutting through a card.
    arrow([(5740,1480),(5885,1480),(5885,640),(6000,640)],'accept',5780,1050,130,TEAL)
    for yy in (960,1280,1600):arrow([(5885,yy),(6000,yy)])
    d.line([(5885,640),(5885,1600)],color=BLUE,arrow=False,sw=2)
    tx(6000,1785,w['labels']['release'],25,BLUE)

    # Legend and infrastructure relationship stay explicit without a web of redundant wires.
    y=2025
    for i,(key,color,style) in enumerate([('main',BLUE,'solid'),('feedback',PURPLE,'dashed'),('evidence',MUTED,'dotted'),('human',TEAL,'solid')]):
        x=60+i*1220
        e=d.line([(x,y+16),(x+110,y+16)],color=color,sw=2, dashed=style=='dashed');e['strokeStyle']=style
        tx(x+130,y,w['legend'][key],26,color)
    tx(60,2690,w['footer'],32,INK)

    for i,e in enumerate(d.els):
        if not e['id'].startswith('s-'):e['id']=f's-complete-flow-{i}'
        e['roughness']=0
    canvas.assign_ids=lambda els:els
    out=HERE/'s03-agent-role.excalidraw'
    d.write(out,Path(__file__).name)
    scene=json.loads(out.read_text());els=[e for e in scene['elements'] if not e.get('isDeleted')]
    assert not any(e['type'] in ('frame','image') for e in els)
    assert len({e['id'] for e in els})==len(els)
    print(f'{len(cards)} cards, {len(els)} native editable elements; no outer frame.')
    print('All authored card text fits:',limits)
    import render_png
    render_png.PREVIEW_W=10000
    render_png.render(out,HERE/'s03-agent-role.full.png',1)
    render_png.PREVIEW_W=2400
    render_png.render(out,HERE/'s03-agent-role.png',0.6)


if __name__=='__main__':main()
