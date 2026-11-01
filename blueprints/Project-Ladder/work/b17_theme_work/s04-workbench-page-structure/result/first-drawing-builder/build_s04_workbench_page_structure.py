"""Build the discussion sketch from its face; keep human edits and deletions."""
import argparse
import re
import sys
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--tools-root', type=Path)
args = parser.parse_args()
TOOLS = args.tools_root or next(p for p in HERE.parents if (p / 'plugins/haipipe-toolkit').is_dir())
sys.path.insert(0, str(TOOLS / 'plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts'))
from draw import Drawing, RED, canvas

# This workspace forbids content hashes. Keep explicit, stable drawing slots and
# use the shared structural merge writer without its content-ID assignment.
canvas.assign_ids = lambda elements: elements
class NamedDrawing(Drawing):
    slot = 'base'
    slot_count = 0
    def el(self, *a, **kw):
        e = super().el(*a, **kw)
        e['id'] = 's-' + self.slot + (f'-{self.slot_count}' if self.slot_count else '')
        self.slot_count += 1
        return e

d = NamedDrawing()
def at(key, method, *a, **kw):
    d.slot = key
    d.slot_count = 0
    return method(*a, **kw)
w = yaml.safe_load(re.search(r'```yaml\n(.*?)```', (HERE / (HERE.name+'.md')).read_text(), re.S).group(1))['drawing']
f=at('frame',d.frame,'Page structure discussion',2400,1440)
at('title',d.text,60,35,w['title'],54)
at('subtitle',d.text,60,110,w['subtitle'],28)
at('path-box',d.box,420,190,1560,100)
at('path',d.text,455,215,w['path'],34)
at('path-intro',d.line,[(1200,295),(1200,330)])
at('intro-box',d.box,420,340,1560,100)
at('intro',d.text,455,365,w['introduction'],34)
at('intro-question',d.line,[(1200,445),(1200,480)])
at('question-box',d.box,420,490,1560,150,color=RED,dashed=True)
at('question',d.text,455,515,w['question'],36,RED)
at('options',d.text,455,570,w['options'],30,RED)
at('question-content',d.line,[(1200,645),(1200,700)],color=RED,dashed=True)
at('content-box',d.key,420,710,1560,370)
at('content',d.text,455,740,w['content'],36)
at('row',d.text,455,805,w['row'],46)
at('reason',d.text,455,875,w['reason'],30)
at('result',d.text,455,945,w['result'],30)
at('distinction',d.text,455,1005,w['distinction'],30)
for side,x,edge in [('left',55,400),('right',2025,2000)]:
    at(side+'-heading',d.text,x,500,w[side],32,RED)
    at(side+'-options',d.text,x,550,w[side+'_options'],28,RED)
    at(side+'-reason',d.text,x,610,d.wrap(w[side+'_reason'],320,28),28)
    at(side+'-arrow',d.line,[(x+150,795),(edge,795)],color=RED,dashed=True)
at('rule',d.text,420,1110,w['rule'],30)
at('hover',d.text,420,1165,w['hover'],30)
at('levels',d.text,420,1220,w['levels'],28,RED)
at('evidence',d.text,420,1270,d.wrap(w['evidence'],1800,28),28,RED)
at('owner',d.text,420,1360,w['owner'],28,RED)
at('density',d.badge,f)

# ② One answer to "what comes immediately below?", drawn as a screen (261028). Placeholders only:
# this blueprint is public, so no real Block, Job, number or figure.
from draw import INK, GREY
def button(key, x, y, label, red=False):
    at(key+'-box', d.box, x, y, d.measure(label, 24)+40, 48, RED if red else INK, 2 if red else 1.5)
    at(key+'-text', d.text, x+20, y+9, label, 24, RED if red else INK)
g = at('screen-frame', d.frame, 'Proposal: one Block page, top to bottom', 2560, 1440)
canvas.ui_frame(g)                               # a screen: the workbench's own look
at('screen-title', d.text, 60, 35, 'Proposal · one Block page, top to bottom', 54)
at('screen-sub', d.text, 60, 110, 'Answers the red box: below the introduction come the section name, then one row per Job.', 28)
at('screen', d.box, 40, 180, 2060, 1220, INK, 2)
cx = 200
at('s-path', d.text, cx, 205, '<Project>  ›  <theme>  ›  bNN_<block>', 26, GREY, code=True)
at('s-rule1', d.line, [(40, 262), (2100, 262)], GREY, arrow=False)
at('s-name', d.text, cx, 285, 'bNN_<block>', 46, code=True)
at('s-spine', d.text, cx, 355, '<the spine: line of board.md: what this Block delivers>', 28)
at('s-status-box', d.key, cx-12, 410, 1180, 54)
at('s-status', d.text, cx+4, 420, '<n> Jobs · <n> Tasks · 🟠 <n> wait for you · 🔶 <n> review open · 🟡 <n> unread', 26)
at('s-rule2', d.line, [(40, 490), (2100, 490)], GREY, arrow=False)
at('s-section', d.text, cx, 515, 'Goal & status', 40)
cols = [cx, cx+430, cx+1100, cx+1560]
for k, (c, name) in enumerate(zip(cols, ['Job', 'goal', 'status', 'do'])):
    at(f's-col{k}', d.text, c, 585, name, 22, GREY)
rows = [('j01_<job>', '🟡 <n> results unread', 'Read', False),
        ('j02_<job>', '🟠 <n> waits for you', 'Your call', True),
        ('j03_<job>', '🔶 <n> review open', 'Review', False),
        ('j04_<job>', '🟢 <n> serving', 'Open values', False)]
y = 620
for k, (name, status, op, mine) in enumerate(rows):
    at(f's-row{k}-rule', d.line, [(cx, y), (cx+1840, y)], GREY, arrow=False, sw=1)
    at(f's-row{k}-name', d.text, cols[0], y+16, name, 24, code=True)
    at(f's-row{k}-goal', d.text, cols[1], y+16, '<the goal: line of the Job face>', 24)
    at(f's-row{k}-status', d.text, cols[2], y+16, status, 24, RED if mine else INK)
    button(f's-row{k}-op', cols[3], y+8, op, mine)
    y += 66
    if k == 2:                                   # one row opened: its output attached under it
        at('s-open-task', d.text, cols[0]+40, y+10, '└ tNN_<task>', 24, code=True)
        at('s-open-status', d.text, cols[2], y+10, '🔶 drawn, review open', 24)
        button('s-open-pass', cols[3], y+4, 'Pass review')
        button('s-open-back', cols[3]+190, y+4, 'Send back')
        y += 66
        at('s-fig', d.box, cols[0]+70, y, 520, 260, GREY, 1.5)
        at('s-fig-text', d.text, cols[0]+220, y+112, 'figure.png', 28, GREY, code=True)
        at('s-fig-q', d.text, cols[0]+640, y+10, 'question: <the question this figure answers>', 26)
        at('s-fig-cap', d.text, cols[0]+640, y+64, '<caption: headline.txt of its Run>', 24, GREY)
        at('s-fig-run', d.text, cols[0]+640, y+222, 'Run rNN_<run> · figure.png · values.csv', 22, GREY, code=True)
        y += 290
at('s-row-end', d.line, [(cx, y), (cx+1840, y)], GREY, arrow=False, sw=1)
for k in range(5):                               # left: siblings; right: sections; names on hover
    at(f's-sib{k}', d.line, [(70, 560+k*42), (122 if k == 2 else 104, 560+k*42)], INK if k == 2 else GREY, arrow=False, sw=5 if k == 2 else 3)
    at(f's-sec{k}', d.line, [(1992 if k == 0 else 2012, 560+k*42), (2080, 560+k*42)], INK if k == 0 else GREY, arrow=False, sw=5 if k == 0 else 3)
at('s-sib-word', d.text, 60, 780, 'siblings', 20, GREY)
at('s-sec-word', d.text, 1990, 780, 'sections', 20, GREY)
for k, (ty, words) in enumerate([(205, '① path: where am I'), (285, '② intro: what it delivers,\nwhere it stands'),
                                  (515, '③ section: what I read now'), (630, '④ a row per Job:\ngoal, status, what to do'),
                                  (900, '⑤ an opened row: its\noutput, in place')]):
    at(f's-call{k}', d.text, 2140, ty, words, 30)
at('s-call-q', d.text, 2140, 1250, '? Is this the first screen?', 28, RED)

h = at('memory-frame', d.frame, 'The site is the project memory', 1700, 1000)
canvas.explains(h)
at('m-title', d.text, 60, 35, 'The site is the project memory', 54)
at('m-sub', d.text, 60, 110, 'It reads the folders live and writes back to them; the page itself is never saved.', 26)
at('m-disk', d.box, 60, 260, 620, 300, INK, 2)
at('m-disk-t', d.text, 84, 276, 'on disk', 30)
for k, s in enumerate(['bNN_<block>/board.md     spine:', 'jNN_<job>/jNN_<job>.md   goal:',
                       'tNN_<task>/tNN_<task>.md  state:', 'runs/rNN_<run>/result/']):
    at(f'm-disk{k}', d.text, 84, 330+k*52, s, 22, code=True)
for k, (a, b) in enumerate([('show content', 'figures, tables, text, in place'),
                            ('show progress', "each Task's state:, totalled per Job"),
                            ('do operations', 'Read · Review · Your call · Run (a person presses)')]):
    yy = 220 + k*170
    at(f'm-job{k}-box', d.key if k == 2 else d.box, 940, yy, 680, 130)
    at(f'm-job{k}-a', d.text, 966, yy+18, a, 34)
    at(f'm-job{k}-b', d.text, 966, yy+72, b, 22)
    at(f'm-job{k}-arrow', d.line, [(690, 410), (930, yy+65)])
at('m-back', d.line, [(1280, 730), (1280, 800), (370, 800), (370, 570)], RED)
at('m-back-t', d.text, 420, 812, 'an operation writes back: state:, review, a Run start', 26, RED)
at('m-memory', d.text, 60, 900, 'Memory = the folders. The site is how a person reads and moves them.', 28)
# ③ The plan to update the layout (261028): from today's layout=focus page to the proposal, in six steps.
p = at('plan-frame', d.frame, 'Plan: update the layout in six steps', 2560, 1440)
at('p-title', d.text, 60, 35, 'Plan · update the layout in six steps', 54)
at('p-sub', d.text, 60, 110, 'Starts from servers/workbench/focus_page.py (layout=focus); the old route stays until step 6.', 28)
for k, (x, head, lines) in enumerate([
        (60, 'today · layout=focus', ['path', 'folder name', 'section name', 'Goal: text + criteria + question cards',
                                      'Jobs: plain links, no status']),
        (1000, 'after', ['path', 'folder name + spine + status line', 'section name', 'Goal & status: a row per Job',
                         'opened row: output in place'])]):
    at(f'p-ba{k}-head', d.text, x, 190, head, 34, INK)
    for i, s in enumerate(lines):
        changed = k == 1 and i in (1, 3, 4)
        at(f'p-ba{k}-{i}', d.text, x, 250+i*44, ('▸ ' if changed else '') + s, 28, INK)
at('p-ba-arrow', d.line, [(780, 340), (960, 340)], sw=4)
steps = [
    ('1 · intro', 'spine + status line', 'render() head · Task state:', False),
    ('2 · Goal & status', 'a row per Job: goal, status, button', 'home_section() · new status_html()', False),
    ('3 · output in place', 'figure + question + caption + review', 'result/figure.png · display.yaml', False),
    ('4 · same rows below', 'Job: Tasks · Task: Runs', "'children' section", False),
    ('5 · operations', 'Read · Review · Your call · Run', 'new POST in frame_view.py', True),
    ('6 · make it default', 'work theme opens layout=focus', 'frame_view.py · old view kept', False),
]
bw, bh = 700, 230
for k, (head, what, where, open_) in enumerate(steps):
    x, y = 60 + (k % 3) * 840, 560 + (k // 3) * 420
    if k == 1:                                   # the key point: the main change
        at(f'p-step{k}-box', d.key, x, y, bw, bh)
    else:
        at(f'p-step{k}-box', d.box, x, y, bw, bh, RED if open_ else INK, 2, None, open_)
    at(f'p-step{k}-head', d.text, x+28, y+22, head, 38, RED if open_ else INK)
    at(f'p-step{k}-what', d.text, x+28, y+92, what, 28)
    at(f'p-step{k}-where', d.text, x+28, y+160, where, 24, GREY, code=True)
    if k % 3 < 2:
        at(f'p-step{k}-next', d.line, [(x+bw+10, y+bh/2), (x+830, y+bh/2)], sw=3)
at('p-step-down', d.line, [(2040, 800), (2040, 880), (410, 880), (410, 970)], sw=3)
at('p-gate1', d.text, 790, 500, '🙋 JL: Q1 yes', 28, RED)
at('p-gate5', d.text, 1630, 1220, '🙋 owner of servers/workbench', 26, RED)
at('p-gate6', d.text, 1700, 1300, '🙋 JL checks b03, then switch', 26, RED)
at('p-phase-a', d.text, 60, 1240, 'Phase A, read only: steps 1-4', 30)
at('p-phase-b', d.text, 60, 1300, 'Phase B, writes back: 5 · Phase C: 6', 30)

# Public blueprint screenshot proposal, kept beside the original discussion.
import base64
asset = HERE / 'result/assets/studio-layout-proposal-20261028.png'
if asset.exists():
    preview_frame = at('studio-review-frame', d.frame, 'Studio layout / image proposal', 2400, 1600)
    preview_frame['x'] = 2600
    title = at('studio-review-title', d.text, 2640, 25, 'Studio layout: open the annotated review', 38)
    title['link'] = '/_excalidraw/?board=blueprints/Project-Ladder/work/b17_theme_work/s04-workbench-page-structure/studio-layout-review.excalidraw'
    file_id = 'studio-layout-proposal-20261028'
    d.files[file_id] = {'id': file_id, 'mimeType': 'image/png', 'created': 1,
                        'dataURL': 'data:image/png;base64,' + base64.b64encode(asset.read_bytes()).decode()}
    at('studio-review-image', d.el, 'image', 2640, 100, 2200, 2200*2/3,
       fileId=file_id, status='saved', scale=[1,1], locked=True)

# All frames laid out once, after every frame exists (the studio review frame included).
d.slot, d.slot_count = 'acts', 0
d.acts([{'name': 'The page', 'frames': [f['id'], g['id']], 'arrow': 'one answer'},
        {'name': 'Why', 'frames': [h['id']]},
        {'name': 'The plan', 'frames': [p['id']]}]
       + ([{'name': 'Studio review', 'frames': [preview_frame['id']]}] if asset.exists() else []))

if len({e['id'] for e in d.els}) != len(d.els):
    raise ValueError('Duplicate drawing slot; assign an explicit unique name.')
d.write(HERE / (HERE.name+'.excalidraw'),Path(__file__).name)
