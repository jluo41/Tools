"""Rebuild the three conceptual Studio workflows with the shared drawing kit."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
BLOCK = HERE.parents[2]
ROOT = next(p for p in HERE.parents if (p / 'PRINCIPLE.md').is_file())
sys.path.insert(0, str(ROOT / 'plugins/haipipe-toolkit/skills/1_base/project/hai-studio/scripts'))
import quick_draw as q
import icons
from render_png import render


def label(eid, x, y, words, size=27):
    return q.text(eid, x, y, words, size, q.ON, 'center')


def build(kind, topic, title):
    els = q.heading(title)
    if kind == 'items':
        els += icons.document('source', 30, 160, 'off', w=120)
        els += label('source-label', 90, 325, 'Corpus')
        els += icons.person('person', 285, 155, 'off')
        els += label('recipe', 325, 365, 'Item recipe')
        els += icons.server('build', 550, 160, 'off')
        els += label('build-label', 615, 325, 'Build + check')
        els += icons.cylinder('items', 825, 160, 'off')
        els += label('items-label', 900, 340, 'Versioned Items')
        for i, (x,y) in enumerate([(180,260),(425,520),(705,795)]):
            els += q.arrow(f'flow-{i}', [(x,235),(y,235)])
        els += q.arrow('guideline', [(1005,210),(1110,140)], label='sample', at=(1050,140))
        els += q.arrow('scale', [(1005,275),(1110,355)], label='execute', at=(1060,340))
        els += label('guideline-label', 1240, 110, 'Guideline Generation')
        els += label('scale-label', 1240, 355, 'Labeling at Scale')
        els += q.text('example', 25, 460, 'Example: assistant reply + preceding turns + source turn ID', 24)
    elif kind == 'guideline':
        els += icons.cylinder('items', 25, 190, 'off')
        els += label('items-label', 100, 360, 'Items')
        els += icons.person('human', 370, 90, 'off')
        els += label('human-label', 410, 270, 'Human judgments')
        els += icons.server('candidate', 720, 190, 'off')
        els += label('candidate-label', 785, 360, 'Generate + validate')
        els += q.arrow('cases', [(190,205),(340,160)], label='cases', at=(260,140))
        els += q.arrow('judgments', [(460,175),(695,235)], label='decisions', at=(580,150))
        els += q.arrow('errors', [(785,390),(785,470),(410,470),(410,305)], label='boundary evidence', at=(590,485))
        els += icons.document('release', 1090, 190, 'off', w=130)
        els += icons.lock('lock', 1225, 170, color=q.SEM['decision'][1])
        els += label('release-label', 1155, 360, 'Signed Guideline')
        els += q.arrow('sign', [(880,245),(1065,245)], label='human confirms', at=(970,185))
        els += q.text('version-note', 25, 555, 'New meaning creates a new version. Existing scale bindings stay fixed.', 24)
    else:
        els += icons.cylinder('items', 30, 120, 'off')
        els += label('items-label', 105, 285, 'Items snapshot')
        els += icons.document('guideline', 30, 390, 'off', w=120)
        els += label('guideline-label', 110, 550, 'Signed Guideline')
        els += icons.gate('gate', 360, 245, 'off')
        els += label('gate-label', 425, 420, 'Qualified executor')
        els += q.arrow('items-input', [(195,205),(325,310)])
        els += q.arrow('guideline-input', [(180,455),(325,335)])
        for i,y in enumerate([160,350]):
            els += icons.server(f'batch-{i}', 670, y, 'off', w=120, h=125)
            els += q.arrow(f'fan-{i}', [(520,325),(630,y+60)])
        els += label('batches', 730, 530, 'Run all / resume')
        els += icons.shield('audit', 960, 245, 'off')
        els += label('audit-label', 1020, 420, 'Audit + coverage')
        els += q.arrow('join1', [(820,220),(930,300)])
        els += q.arrow('join2', [(820,410),(930,345)])
        els += icons.document('labels', 1250, 245, 'off', w=120)
        els += label('labels-label', 1310, 420, 'Final labels')
        els += q.arrow('release', [(1120,325),(1215,325)])
        els += q.text('feedback', 310, 620, 'Meaning issues return to Guideline Generation; never silently edit a release.', 24)
    # Neutral pictograms denote roles, not fabricated completion states.
    for e in els:
        if e['type']=='text': e['fontFamily']=6
    folder=BLOCK/topic; dest=folder/(topic+'.excalidraw')
    q.write(dest,els)
    render(dest,folder/(topic+'.png'),1)
    print(topic, len(els), 'elements')


if __name__ == '__main__':
    for args in [('items','s11-itemization-job-preview','Itemization'),
                 ('guideline','s12-guideline-job-preview','Guideline Generation'),
                 ('scale','s14-scale-job-preview','Labeling at Scale')]:
        build(*args)
