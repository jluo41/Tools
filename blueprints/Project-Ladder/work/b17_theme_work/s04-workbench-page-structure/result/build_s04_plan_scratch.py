"""Scratch for Phase A of the layout plan: what changes in focus_page.py, step by step, before any code (261028).

Code lines are read from servers/workbench/focus_page.py when this runs, so the scratch quotes what is there.
Placeholders only for project content: this blueprint is public. JL's own marks are kept on a rebuild.

    python build_s04_plan_scratch.py     # writes s04-plan-scratch.excalidraw
"""
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = next(p for p in HERE.parents if (p / 'plugins/haipipe-toolkit').is_dir())
sys.path.insert(0, str(TOOLS / 'plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts'))
import canvas  # noqa: E402

canvas.assign_ids = lambda elements: elements      # explicit ids; no content hashes
SRC = TOOLS / 'plugins/haipipe-toolkit/servers/workbench/focus_page.py'
random.seed(1)
HAND, MONO = 6, 3
INK, GRAY, RED, BLUE = '#1e1e1e', '#868e96', '#e03131', '#1971c2'
STICKY = {'ask': '#ffec99', 'fit': '#b2f2bb', 'bend': '#ffd8a8', 'none': '#e9ecef', 'open': '#ffc9c9'}
els, FRAME, OFFSET, FILES = [], [None], [0], {}


def base(key, kind, x, y, w, h, stroke=INK, bg='transparent', sw=2, dashed=False):
    e = {'id': 's-scratch-' + key, 'type': kind, 'x': x, 'y': y + OFFSET[0], 'width': w, 'height': h, 'angle': 0,
         'strokeColor': stroke, 'backgroundColor': bg, 'fillStyle': 'solid', 'strokeWidth': sw,
         'strokeStyle': 'dashed' if dashed else 'solid', 'roughness': 1, 'opacity': 100, 'groupIds': [],
         'frameId': FRAME[0], 'roundness': {'type': 3} if kind == 'rectangle' else None,
         'seed': random.randint(1, 2**31 - 1), 'version': 1, 'versionNonce': random.randint(1, 2**31 - 1),
         'isDeleted': False, 'boundElements': [], 'updated': 1, 'link': None, 'locked': False}
    els.append(e)
    return e


def text(key, x, y, s, size=22, color=INK, font=HAND, container=None):
    lines = s.split('\n')
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.56)
    e = base(key, 'text', x, y, w, len(lines) * size * 1.25, color)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign='left', verticalAlign='top',
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def sticky(key, x, y, w, body, kind, size=22):
    h = 36 + (body.count('\n') + 1) * size * 1.35
    r = base(key, 'rectangle', x, y, w, h, INK, STICKY[kind], 1)
    t = text(key + '-t', x + 16, y + 14, body, size, INK, container=r['id'])
    r['boundElements'] = [{'type': 'text', 'id': t['id']}]
    return y + h


def mono(key, x, y, lines, size=16, width=None, title=None):
    w = width or max(len(l) for l in lines) * size * 0.6 + 40
    top = 36 if title else 14
    base(key, 'rectangle', x, y, w, top + len(lines) * size * 1.3 + 16, GRAY, '#f8f9fa', 1)
    if title:
        text(key + '-title', x + 14, y + 8, title, 20, GRAY)
    for i, l in enumerate(lines):
        text(f'{key}-{i}', x + 18, y + top + i * size * 1.3, l, size, INK, MONO)
    return y + top + len(lines) * size * 1.3 + 16


def mark(key, x, y, w, h):
    base(key, 'rectangle', x, y, w, h, RED, sw=2)


def arrow(key, pts, color=INK, dashed=False):
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base(key, 'arrow', x, y, max(abs(p[0]) for p in rel) or 1, max(abs(p[1]) for p in rel) or 1, color,
             dashed=dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None,
             endArrowhead='arrow')


def src_lines(*needles):
    """The numbered source lines that hold each needle, read now."""
    out = []
    for n, line in enumerate(SRC.read_text().splitlines(), 1):
        if any(k in line for k in needles):
            out.append(f'{n:>3}  {line.strip()[:96]}')
    return out


# ── today's Studio page, marked: what changes (JL's screenshot, 261028) ─────────────────────────────────────
SHOT = HERE / 'assets/studio-today-jl-20261028.png'
STUDIO = HERE.parent.parent                       # this builder sits in s04's result/
text('shot-title', 0, 0, "Scratch · today's Studio page, marked: what changes", 44)
text('shot-sub', 0, 66, 'Red = today, as JL sees it. Right = the same page in the new layout. Mark anything in red.', 26, GRAY)
SX, SY = 700, 200
if SHOT.exists():
    import base64
    from PIL import Image
    iw, ih = Image.open(SHOT).size
    FILES['studio-today-jl'] = {'id': 'studio-today-jl', 'mimeType': 'image/png', 'created': 1,
                                'dataURL': 'data:image/png;base64,' + base64.b64encode(SHOT.read_bytes()).decode()}
    img = base('shot', 'image', SX, SY, iw, ih, sw=1)
    img.update(fileId='studio-today-jl', status='saved', scale=[1, 1])
    base('shot-edge', 'rectangle', SX - 2, SY - 2, iw + 4, ih + 4, GRAY, sw=1)
    notes = [  # (key, box in screenshot px, note y on the left, words)
        ('tabs', (40, 38, 1100, 78), 200, '① Three kinds of tabs in one row:\nhelp, level, output.\n-> top = the path only:\nTools / blueprints / b17_theme_work'),
        ('title', (40, 180, 1020, 72), 400, '② Title "Workbench · Studio".\n-> the folder name, its spine,\none status line'),
        ('chips', (76, 318, 1244, 76), 560, '③ Group chips and "+ Group".\n-> groups become sections\non the right: Studio-All,\nStudio-Interface, ...'),
        ('help', (76, 422, 1400, 78), 760, '④ How-to text on every visit.\n-> move it into Guide'),
        ('rows', (98, 545, 40, 560), 900, '⑤ Each row hides its drawing\nbehind ▸ and has 4 controls.\n-> show the drawing and its\nTopic line directly'),
        ('s04', (200, 950, 610, 62), 1110, '⑥ Name and tags cut off.\n-> the full folder name,\ntags on the line under it'),
        ('later', (82, 1200, 1400, 230), 1300, '⑧ Empty sections\n(0 items, 0 results).\n-> hide a section when empty'),
        ('left', (10, 284, 30, 1100), 1500, '⑩ No way to the sibling Blocks.\n-> left rail: b10 ... b17 as\ndashes, names on hover'),
    ]
    for key, (bx, by, bw, bh), ny, words in notes:
        base(f'm-{key}', 'rectangle', SX + bx, SY + by, bw, bh, RED, sw=3)
        sticky(f'n-{key}', 0, ny, 600, words, 'open', 22)
        arrow(f'a-{key}', [(604, ny + 30), (SX + bx - 6, SY + by + min(bh, 60) / 2)], RED)
    right = [('pill', (1348, 544, 108, 48), 740, '⑦ What does this pill mean?\n-> say it in words:\n"Stage: explore"'),
             ('rail', (1532, 284, 86, 240), 300, '⑨ "Disk · Runs" rail.\n-> the right rail lists this\npage\'s sections: dashes,\nnames on hover')]
    rx = SX + iw + 60
    for key, (bx, by, bw, bh), ny, words in right:
        base(f'm-{key}', 'rectangle', SX + bx, SY + by, bw, bh, RED, sw=3)
        sticky(f'n-{key}', rx, ny, 520, words, 'open', 22)
        end = (SX + bx + bw + 6, SY + by + min(bh, 60) / 2)
        arrow(f'a-{key}', [(rx - 4, ny + 30), end], RED)

# ── the same page, new layout ───────────────────────────────────────────────────────────────────────────────
AX, AY = SX + 1652 + 660, 200
text('after-h', AX, AY - 10, 'after: the same page, new layout', 32)
base('after-screen', 'rectangle', AX, AY + 50, 1300, 1380, INK, sw=2)
cx = AX + 120
block = STUDIO.parent
spine = next((l[7:].strip() for l in (block / 'board.md').read_text().splitlines() if l.startswith('spine:')), '')
topics = sorted(t for t in STUDIO.glob('s[0-9][0-9]-*') if t.is_dir())
text('after-path', cx, AY + 80, f'Tools / blueprints / {block.name}', 18, GRAY, MONO)
text('after-h1', cx, AY + 120, block.name, 34, INK, MONO)
text('after-spine', cx, AY + 175, spine[:88] + ' ...', 18)
base('after-status', 'rectangle', cx - 8, AY + 215, 640, 40, INK, '#fff3bf', 1)
text('after-status-t', cx + 4, AY + 223, f'{len(topics)} Studio topics · groups: Interface, Navigation', 18)
text('after-sec', cx, AY + 285, 'Studio-All', 28)
y = AY + 340
for k, t in enumerate(topics):
    face = t / f'{t.name}.md'
    line = next((l.replace('**Topic:**', '').strip() for l in face.read_text().splitlines()
                 if l.startswith('**Topic:**')), '') if face.exists() else ''
    base(f'after-row{k}', 'rectangle', cx, y, 1080, 150, GRAY, sw=1)
    text(f'after-row{k}-n', cx + 20, y + 16, t.name, 20, INK, MONO)
    text(f'after-row{k}-t', cx + 20, y + 56, (line[:52] + ' ...') if len(line) > 52 else line, 17)
    text(f'after-row{k}-s', cx + 20, y + 104, 'Stage: explore' if 'Stage:** explore' in (face.read_text() if face.exists() else '') else 'Stage: -', 16, GRAY)
    base(f'after-row{k}-img', 'rectangle', cx + 820, y + 14, 240, 122, GRAY, '#f1f3f5', 1)
    text(f'after-row{k}-img-t', cx + 890, y + 62, 'drawing', 18, GRAY)
    y += 168
sibs = sorted(b.name for b in block.parent.glob('b[0-9]*') if b.is_dir())
for k, b in enumerate(sibs):
    cur = b == block.name
    base(f'after-sib{k}', 'line', AX + 20, AY + 340 + k * 30, 46 if cur else 26, 1, INK if cur else GRAY, sw=4 if cur else 2)
    els[-1].update(points=[[0, 0], [46 if cur else 26, 0]], lastCommittedPoint=None, startBinding=None, endBinding=None,
                   startArrowhead=None, endArrowhead=None)
secs = ['Goal & status', 'Studio-All', 'Studio-Interface', 'Studio-Navigation', 'Questions', 'Timeline', 'Folder', 'Guide']
for k, name in enumerate(secs):
    cur = name == 'Studio-All'
    base(f'after-sec{k}', 'line', AX + 1240 - (46 if cur else 26), AY + 340 + k * 30, 46 if cur else 26, 1,
         INK if cur else GRAY, sw=4 if cur else 2)
    els[-1].update(points=[[0, 0], [46 if cur else 26, 0]], lastCommittedPoint=None, startBinding=None, endBinding=None,
                   startArrowhead=None, endArrowhead=None)
base('after-hover', 'rectangle', AX + 1320, AY + 384, 210, 36, GRAY, 'transparent', 1)
text('after-hover-t', AX + 1332, AY + 390, 'Studio-Interface', 18, GRAY)
text('after-hover-w', AX + 1320, AY + 430, 'name on hover', 16, GRAY)
sticky('after-note', AX, AY + 1460, 1300, 'Studio is one section of the page, not a tab. Related, Delivery, Runs show only when they hold something.\nThe code: focus_page.py already draws Studio-All and one section per group; steps 1-4 add the head and the rows.', 'fit', 22)

OFFSET[0] = 2250

# ── title ───────────────────────────────────────────────────────────────────────────────────────────────────
text('title', 0, 0, 'Phase A in the code: the layout=focus page becomes "Goal & status"', 44)
text('sub', 0, 66, 'Read only. Four steps in servers/workbench/focus_page.py. No code until JL marks this.', 26, GRAY)

# ── cluster: today ──────────────────────────────────────────────────────────────────────────────────────────
text('today-h', 0, 150, 'today: what focus_page.py does', 32)
today = src_lines('def home_section', 'if theme == "work"', 'return "goal"', 'sections = [(home',
                  'sections += [("children"', 'elif section == "children"', 'focus-child', '<h1>')
bottom = mono('today', 0, 200, today, 16, title='servers/workbench/focus_page.py, read at build time')
tw = max(len(l) for l in today) * 16 * 0.6 + 40   # the box's width, so a mark fits inside it
row = next(i for i, l in enumerate(today) if 'focus-child' in l)
mark('today-mark', 8, 200 + 36 + row * 16 * 1.3 - 3, tw - 16, 16 * 1.3 + 6)
sticky('today-note', 1120, 330, 400, 'a Job row is a link:\ntitle + folder name.\nNo goal, no status.', 'bend')
arrow('today-arrow', [(1120, 380), (tw + 4, 200 + 36 + row * 16 * 1.3 + 8)], RED)
hrow = next(i for i, l in enumerate(today) if '<h1>' in l)
mark('today-mark2', 8, 200 + 36 + hrow * 16 * 1.3 - 3, tw - 16, 16 * 1.3 + 6)
sticky('today-note2', 1120, 470, 400, 'the head is only the\nfolder name.', 'bend')
arrow('today-arrow2', [(1120, 500), (tw + 4, 200 + 36 + hrow * 16 * 1.3 + 8)], RED)

# ── cluster: the four steps ─────────────────────────────────────────────────────────────────────────────────
y0 = 640
text('steps-h', 0, y0, 'Phase A: four steps, each one change', 32)
steps = [
    ('1 · intro', 'ask',
     'under <h1>: the spine (data["goal"])\n+ one status line:\ncount every Task state: below this folder',
     ['new  states_under(folder) -> Counter', '     reads tNN_<task>.md  state:', '     label = words before " · "',
      'edit render(): head after <h1>']),
    ('2 · Goal & status', 'fit',
     'work theme lands on "Goal & status":\none full-width row per child:\nname | goal | status | link',
     ['edit home_section(): work -> "status"', 'new  status_html(folder, level)', '     goal = read_face(child)["goal"]',
      '     status = states_under(child)', '     button = a link (Phase B: a write)']),
    ('3 · output in place', 'fit',
     'a Task row shows its newest Run\'s\nfigure + question + caption,\nno click to open',
     ['new  output_of(task)', '     runs/<run>/result/figure.png', '     display.yaml  question:', '     headline.txt',
      'only on the Job page (rows = Tasks)']),
    ('4 · same rows below', 'fit',
     'Job page: rows = Tasks\nTask page: rows = Runs\n(the same status_html)',
     ['level Job  -> frame.children()', 'level Task -> frame.runs_of()', 'replaces the "children" section']),
]
for k, (head, kind, body, where) in enumerate(steps):
    x = k * 640
    text(f'step{k}-h', x, y0 + 56, head, 30)
    yb = sticky(f'step{k}-s', x, y0 + 104, 600, body, kind)
    mono(f'step{k}-m', x, yb + 18, where, 16, width=600)
    if k < 3:
        arrow(f'step{k}-a', [(x + 604, y0 + 150), (x + 636, y0 + 150)])

# ── cluster: files and tests ────────────────────────────────────────────────────────────────────────────────
y1 = 1260
text('files-h', 0, y1, 'what changes on disk', 32)
mono('files', 0, y1 + 50, [
    'servers/workbench/',
    '├── focus_page.py           steps 1-4 (Codex wrote it 261028; uncommitted)',
    '├── focus-assets/focus.css  .status-row, .output-in-place',
    '├── frame_view.py           no change in Phase A',
    '└── tests/test_focus_page.py',
    '      + test_intro_status_line',
    '      + test_status_rows_per_child',
    '      + test_output_in_place_on_job_page',
    '      keep test_focus_route_and_old_route_remain_distinct',
], 16)
sticky('files-old', 1280, y1 + 60, 520, 'the old route (no layout=focus)\nstays as it is until step 6', 'none')
sticky('files-check', 1280, y1 + 180, 520, 'check: open a demo Block in the\nbrowser, then b03 with JL', 'ask')

# ── Questions frame ─────────────────────────────────────────────────────────────────────────────────────────
qx, qy = 1860, 1260
fq = base('qframe', 'frame', qx, qy, 1400, 760, INK, sw=1)
fq['name'] = 'Questions'
FRAME[0] = fq['id']
qs = [('Q1 · Status comes from each Task\'s state: line only,\nor also from Run receipts (work_progress)?', 'state: only, first'),
      ('Q2 · Output in place on the Job page only,\nor also on the Block page for rows waiting for you?', 'Job page only'),
      ('Q3 · Buttons in Phase A are plain links to the\nchild page. OK until Phase B writes back?', 'yes, links'),
      ('Q4 · A child with no state: lines shows\n"no state recorded". OK?', 'yes')]
for k, (q, idea) in enumerate(qs):
    y = qy + 30 + k * 180
    sticky(f'q{k}', qx + 30, y, 760, q, 'ask', 22)
    sticky(f'q{k}-idea', qx + 820, y, 320, 'idea: ' + idea, 'none', 22)
    text(f'q{k}-mark', qx + 1170, y + 20, '?', 40, RED)
FRAME[0] = None

out = HERE / 's04-plan-scratch.excalidraw'
canvas.write(out, els, Path(__file__).name, files=FILES, palette=False)
