"""The Section canvas: one Section of a draft in one frame, read down (b32 s41; first built as b21 s06, 2026-10-15).
Left: the file today (page pictures), then how the paragraphs read; middle: the text, one sentence a row, its words
black, a pale box under the words a card is about; right: the evidence cards, the comments with our replies, and
the change cards, each joined to its sentence.

It writes no manuscript prose. Every word is read on each build from what the topic's face names in its `canvas:`
yaml block; only `draft_folder` is required:

    canvas:
      draft_folder: <path to the draft/ folder>     one current *-draft-v*.md, older ones in previous/
      section: C5                                   every paragraph C5.P<n>; or paragraphs: [C5.P13, C5.P14]
      pages: {render: <delivery render/ folder>, name: <file name>, pick: [5, 6]}
                                                    the newest version's page pictures (haipipe-delivery word_round.py)
      evidence: <path to evidence/cards.yaml>       CITE blue, WORK violet, a needed item red (haipipe-evidence)
      plan_face: <face.md>  plan_key: <key>  part: "4"
                                                    a revise plan (excalidraw-draft Revise mode): its edits become
                                                    change cards and red asks, its replies the comments
      picture_frame: <frame name>  picture_out: render/<file>.png
                                                    the left picture cut from the plan face's drawing instead of pages
      title, subtitle, key, left_title, logic_title, text_title, evidence_title, comment_title, edits_title, footer

Paths are relative to the face. A rebuild keeps a person's marks (canvas.write). The preview draws each pale box at
its opacity, which the shared offline preview does not.

`sync` reads the canvas back into the files, then rebuilds it, so the step tabs and the canvas show the same thing
(b32 s41-D28; JL 261019: "我都在这个画布上工作，那我这个 stage 1、2、3、4 的内容也会对应更新"):

    a sentence typed over      → §3 of the Draft, by its address (code)
    a note, box, arrow or line  → draft/records/<stem>-feedback.md, at the sentence it sits beside (code);
                                  an agent turns these into Revise cards or a §1 change (haipipe-draft-writing, -logic)

Each applied sentence is logged in the same file as before → after. A mark is recorded once and stays on the canvas.

    python section_canvas.py <topic face.md> [--out <file>.excalidraw]
    python section_canvas.py sync <topic face.md> [--dry]
"""
from pathlib import Path
import argparse
import base64
import io
import json
import math
import re
import sys

import yaml
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[2]                                   # skills/1_base/
sys.path.insert(0, str(SKILLS / 'excalidraw/excalidraw-studio/scripts'))
sys.path.insert(0, str(SKILLS / 'project/haipipe-studio/scripts'))
sys.path.insert(0, str(SKILLS / 'evidence/haipipe-evidence/scripts'))
from draw import Drawing, INK, RED, GREEN, GREY, canvas  # noqa: E402
from render_png import font, save_preview  # noqa: E402
import cards as ev_cards  # noqa: E402

YELLOW = '#fab005'                       # a comment is about these words (a pale box under them)
DEFAULTS = {
    'subtitle': 'the Section canvas (b32 s41): logic left, text middle, evidence and edits right',
    'key': 'One Section, one frame: every card points at its sentence. A pale box marks the words a card is about.',
    'left_title': 'The file today',
    'logic_title': 'How the paragraphs read',
    'text_title': 'The text now · draft',
    'evidence_title': '🔎 Evidence: what backs each claim',
    'comment_title': '💬 Comments',
    'edits_title': "✏️ Changes: the file's words → the draft's",
    'footer': ['Words stay black; a pale box marks what a card is about. Blue = a paper (CITE), violet = our own Run '
               '(WORK), red = still needed, yellow = a comment.'],
}


def spec_of(face):
    return {**DEFAULTS, **yaml.safe_load(re.search(r'```yaml\n(.*?)\n```', face.read_text(), re.S)[1])['canvas']}


def build(face, out=None, builder=None):
    face = Path(face).resolve()
    base = face.parent
    spec = spec_of(face)
    out = Path(out) if out else face.with_suffix('.excalidraw')
    space = next((p for p in face.parents if (p / 'env.sh').is_file()), base)
    files = list((base / spec['draft_folder']).glob('*-draft-v*.md'))
    if len(files) != 1:
        raise ValueError('Keep one current Draft; older versions belong in previous/.')
    draft = files[0].read_text()
    version = re.search(r'(?m)^draft-version:\s*(\S+)', draft)[1]

    def block(part, address):
        """The lines under `### <address>` inside one of the draft's three sections."""
        body = draft.split(part, 1)[1]
        m = re.search(r'### ' + re.escape(address) + r' · ([^\n]*)\n(.*?)(?=\n### |\n## |\Z)', body, re.S)
        if not m:
            raise ValueError(f'{address} is missing from the Draft.')
        return m[1], m[2]

    paragraphs = spec.get('paragraphs') or re.findall(
        r'(?m)^### (' + re.escape(spec['section']) + r'\.P\d+) · ', draft.split('## 3 · Draft', 1)[1])
    if not paragraphs:
        raise ValueError('The face names no paragraphs, and its section has none in the Draft.')
    section = spec.get('section') or paragraphs[0].split('.')[0]

    edits, reply = [], None                              # a revise plan, when the face names one
    if spec.get('plan_face'):
        plan_text = (base / spec['plan_face']).read_text()
        plan = yaml.safe_load(re.search(r'```yaml\n(.*?)```', plan_text, re.S)[1])[spec['plan_key']]
        edits = [e for e in plan.get('edits', []) if str(e.get('part')) == str(spec.get('part'))]
        reply = next((r for r in plan.get('replies', []) if f"on part {spec.get('part')}" in str(r.get('when', ''))), None)

    rows, logic = [], []                     # rows: (address, b, n, text); logic: (address, title, [(n, tag, changes)])
    for address in paragraphs:
        _, text = block('## 3 · Draft', address)
        rows += [(address, int(b), int(n), t) for b, n, t in re.findall(r'^- B(\d+) · S(\d+) · (.+)$', text, re.M)]
        title, plan_ = block('## 1 · Structure', address)
        bullets = []
        for m in re.finditer(r'^- B\d+ · S(\d+) · (.+)(?:\n\s+Change: (.+))?$', plan_, re.M):
            bullets.append((int(m[1]), m[2], [int(i) for i in re.findall(r'(?:^|, )(\d+) · ', m[3] or '')]))
        logic.append((address, title, bullets))
    sentence = {n: t for _, _, n, t in rows}
    changes_of = {n: ids for _, _, bl in logic for n, _, ids in bl}

    def where(anchor, among=None):
        """The sentence an anchor's words are in, or None when the text no longer has them."""
        return next((n for n, t in sentence.items() if anchor in t and (among is None or n in among)), None)

    # The file today: the newest version's page pictures, or the picture a plan face's drawing holds.
    pictures, picture_note = [], ''
    if spec.get('pages'):
        pg = spec['pages']
        root = base / pg['render']
        found = [(int(m[1]), p) for p in root.glob(f"{pg.get('name', '*')}-v*")
                 if p.is_dir() and (m := re.search(r'-v(\d+)$', p.name))]
        if not found:
            raise ValueError(f"no rendered version in {pg['render']}: run haipipe-delivery word_round.py render")
        n_, vdir = max(found)
        pick = pg.get('pick') or sorted(int(p.stem.split('-')[1]) for p in vdir.glob('p-*.png'))
        pictures = [vdir / f'p-{k}.png' for k in pick]
        picture_note = f"{vdir.name}, page{'s' if len(pick) > 1 else ''} {', '.join(map(str, pick))}"
    elif spec.get('picture_frame'):
        s04 = json.loads((base / spec['plan_face']).with_suffix('.excalidraw').read_text())
        frame_id = next(e['id'] for e in s04['elements'] if e['type'] == 'frame' and e.get('name') == spec['picture_frame'])
        image = next(e for e in s04['elements'] if e['type'] == 'image' and e.get('frameId') == frame_id)
        pic = base / spec.get('picture_out', 'render/file-today.png')
        pic.parent.mkdir(exist_ok=True)
        Image.open(io.BytesIO(base64.b64decode(s04['files'][image['fileId']]['dataURL'].split(',', 1)[1]))).save(pic)
        pictures = [pic]
        picture_note = f"from {Path(spec['plan_face']).parent.name}'s drawing: {spec['picture_frame']}, changed words under a red marker"

    cards = ev_cards.order(ev_cards.load(base / spec['evidence'])) if spec.get('evidence') else []
    project = None
    if cards:
        try:
            project = ev_cards.project_root(base / spec['evidence'])
        except ValueError:
            pass

    d = Drawing()
    f = d.frame(f"{section} · the Section canvas", 2800, 1600)
    canvas.reads_down(f)
    Drawing.detail(f)
    d.text(40, 24, spec.get('title') or f'{section} · the Section canvas', 60)
    d.text(42, 104, spec['subtitle'], 26, GREY)
    d.key(40, 150, 2200, 52, sw=1)
    d.text(56, 162, spec['key'], 25)

    def aside(x, y, text, w, size=21, color=INK):
        e = d.text(x, y, d.wrap(text, w, size), size, color)
        canvas.aside(e)
        return y + e['height']

    # ── left: the file today, then how the paragraphs read ─────────────────────────────────────────────
    LX, LW = 40, 440
    d.text(LX, 240, spec['left_title'], 28)
    y = 288
    for pic in pictures:
        y += d.picture(pic, LX, y, LW, 760 if len(pictures) == 1 else 600) + 10
    if pictures:
        y = aside(LX, y + 2, picture_note, LW, 19, GREY)
    else:
        y = aside(LX, y, 'no page pictures yet: haipipe-delivery word_round.py render', LW, 19, RED)
    d.text(LX, y + 40, spec['logic_title'], 28)
    y += 92
    for i, (address, title, bullets) in enumerate(logic):
        x, w = LX + min(i, 4) * 16, LW - min(i, 4) * 16
        h = d.height(f'{address.split(".")[1]} · {title}', w - 26, 26) + 22
        d.box(x, y, w, h, INK, 1.8)
        d.para(x + 13, y + 10, f'{address.split(".")[1]} · {title}', w - 26, 26)
        y += h + 10
        for n, tag, _ in bullets:
            y = aside(x + 24, y, f'S{n} · {tag}', w - 30, 20) + 4
        if i < len(logic) - 1:
            d.line([(x + 30, y + 6), (x + 30, y + 34), (x + 46, y + 34)], GREY, sw=1.2)
        y += 44
    left_bottom = y

    # ── middle: the text, one sentence a row, pale boxes on what a card is about ─────────────────────────
    MX, MW, SIZE, LH = 530, 990, 28, 35
    marks = {}                               # n -> [(start, end, colour)]

    def mark(n, phrase, colour):
        a = sentence[n].find(phrase)
        marks.setdefault(n, []).append((a, a + len(phrase), colour))

    for card, _ in cards:
        for it in card['items']:
            colour = ev_cards.COLOR['need'] if it.get('need') else ev_cards.COLOR[card['kind']]
            for phrase in it.get('anchor', []):
                if (n := where(phrase, it['for'])):
                    mark(n, phrase, colour)
    for e in [e for c in edits for e in (c.get('evidence') or []) if isinstance(c.get('evidence'), list)] + \
             [c['evidence'] for c in edits if isinstance(c.get('evidence'), dict)]:
        if (n := where(e['anchor'])):
            mark(n, e['anchor'], RED)
    for item in (reply or {}).get('items', []):
        if (n := where(item['anchor'])):
            mark(n, item['anchor'], YELLOW)
    d.text(MX, 240, f"{spec['text_title']} {version} · {', '.join(paragraphs)}", 30)
    note_end = aside(MX, 284, f"from {files[0].parent.parent.name}/draft/{files[0].name}; words in black, a pale box "
                     f"under what a card is about", MW, 20, GREY)
    anchor_y, yy, last, body = {}, max(330, note_end + 20), None, None
    for address, b, n, text in rows:
        if address != last:
            if last is not None:
                body['height'] = yy - body['y'] + 14
                yy += 40
            title = next(t for a, t, _ in logic if a == address)
            d.text(MX, yy, f'{address.split(".")[1]} · {title}', 28)
            yy += 46
            body = d.box(MX, yy, MW, 10, INK, 1.8)
            yy += 18
            last = address
        wrapped = d.wrap(text, MW - 70, SIZE)
        offset = 0
        for li, line in enumerate(wrapped.split('\n')):
            start = text.find(line, offset)
            for a, z, colour in marks.get(n, []):
                lo, hi = max(a, start), min(z, start + len(line))
                if start >= 0 and lo < hi:
                    px = font(SIZE).getlength(line[:lo - start])
                    span = font(SIZE).getlength(line[lo - start:hi - start])
                    e = d.el('rectangle', MX + 50 + px, yy + li * LH + 1, span + 3, LH - 1, strokeColor='transparent',
                             backgroundColor=colour, opacity=22 if colour == YELLOW else 15)
                    e['customData'] = {'highlight': {'sentence': n, 'colour': colour}}
            offset = max(offset, start + len(line))
        e = d.text(MX + 50, yy, wrapped, SIZE)
        e['customData'] = {'sentence': {'address': f'{address}.B{b}', 'n': n, 'built': text}}
        canvas.aside(d.text(MX + 12, yy + 3, f'S{n}', 19, GREY))
        anchor_y[n] = yy + e['height'] / 2
        yy += e['height'] + 12
    if body:
        body['height'] = yy - body['y'] + 14
    middle_bottom = yy + 30

    # ── right: evidence, then the comments and our replies, then the changes ──────────────────────────────
    def card(x, y, w, title, lines, colour=INK):
        """A card: its title, then (words, colour, size) lines. Returns (box, bottom)."""
        box = d.box(x, y, w, 10, colour, 1.6)
        canvas.aside(box)
        yy_ = aside(x + 14, y + 12, title, w - 28, 23, colour) + 6
        for words, c, s in lines:
            yy_ = aside(x + 14, yy_, words, w - 28, s, c) + 5
        box['height'] = yy_ - y + 12
        return box, y + box['height']

    EX, EW = 1610, 520
    d.text(EX, 240, spec['evidence_title'], 28)
    ey, links, k = 300, [], 0                # links: (card box, sentence n, colour)
    for c, label in cards:                   # evidence/cards.yaml, in the order of the sentences they back
        needed = not c.get('source')
        colour = ev_cards.COLOR['need'] if needed else ev_cards.COLOR[c['kind']]
        title = c.get('title')
        if not title and project:
            try:
                title = ev_cards.title_of(ev_cards.resolve(project, c['kind'], c['source']))
            except ValueError:
                title = None
        lines = []
        for it in c['items']:
            hit = [n for n in it['for'] if n in sentence]
            words = it.get('need') or it.get('note') or '; '.join(it.get('anchor', []))
            state = 'needed' if it.get('need') else f"{c.get('source', '')}.{it.get('run', '')}".strip('.')
            lines.append((f"S{','.join(map(str, it['for']))} · {words[:160]}{'…' if len(words) > 160 else ''}",
                          ev_cards.COLOR['need'] if it.get('need') else INK, 19))
            lines.append((state, GREY, 18))
        if not any(n in sentence for it in c['items'] for n in it['for']):
            continue                         # a card for sentences outside this Section
        box, ey = card(EX, ey, EW, f"{label} · {title or c.get('source', '')}", lines, colour)
        ey += 16
        for it in c['items']:
            for n in sorted({n for n in it['for'] if n in sentence}):
                links.append((box, n, ev_cards.COLOR['need'] if it.get('need') else colour))
    for c in edits:                          # a revise plan's asks: who must answer, and on which words
        asks = c.get('evidence') or []
        for e in asks if isinstance(asks, list) else [asks]:
            k += 1
            n = where(e['anchor'])
            lines = [(f"need: {e['need'][:220]}{'…' if len(e['need']) > 220 else ''}", INK, 19),
                     (f"who: {', '.join(e['who'])}", INK, 20),
                     (f"on S{n}: “{e['anchor']}”" if n else f"❓ its words are no longer in {version}: “{e['anchor']}”",
                      GREY if n else RED, 19),
                     ('asked · no answer yet', RED, 20)]
            box, ey = card(EX, ey, EW, f"E{k} · {e['ask']}", lines, RED)
            ey += 16
            if n:
                links.append((box, n, RED))
    if not cards and not k:
        ey = aside(EX, ey, 'no evidence cards: add evidence/cards.yaml (haipipe-evidence)', EW, 19, GREY)

    CX, CW = 2180, 590
    d.text(CX, 240, spec['comment_title'], 28)
    cy = 300
    if reply:
        lines = [(f"“{reply['said']}”", INK, 22), (f"our answer: {reply['brief']}", GREY, 19)]
        _, cy = card(CX, cy, CW, f"{reply['to']} · {reply['when']}", lines, INK)
        cy += 10
        for item in reply['items']:
            n = where(item['anchor'])
            head = f"↳ on S{n}" if n else f"❓ ↳ its words are no longer in {version}"
            rb, cy = card(CX + 30, cy, CW - 30, head,
                          [(item['reply'], INK, 19)] + ([] if n else [(f"“{item['anchor']}”", RED, 19)]),
                          INK if n else RED)
            cy += 10
            if n:
                links.append((rb, n, YELLOW))
    else:
        cy = aside(CX, cy, 'no comments on this Section', CW, 19, GREY)
    if edits:
        cy += 40
        d.text(CX, cy, spec['edits_title'], 28)
        cy += 56
        for c in edits:
            hit = sorted(n for n, ids in changes_of.items() if c['id'] in ids)
            old = ' '.join(str(c.get('find', '')).split())
            lines = [(f"why: {c['why']}", INK, 20),
                     (f"file: {old[:150]}{'…' if len(old) > 150 else ''}", RED, 19),
                     (f"→ draft: {', '.join(f'S{n}' for n in hit)}" if hit else '→ deleted: the template\'s guidance',
                      GREEN, 20),
                     (f'written in {version} · a tracked change in the Word file', GREEN, 19)]
            box, cy = card(CX, cy, CW, f"#{c['id']} · {c['title']}", lines, GREEN)
            cy += 14
            for n in hit:
                links.append((box, n, GREEN))

    # each card to its sentence: out of the text's right edge, along a trunk, into the card's left side
    trunks = {YELLOW: 1560, GREEN: 1580}
    for i, (box, n, colour) in enumerate(links):
        t = trunks.get(colour, 1540) + (i % 3) * 4
        sy, cy_ = anchor_y[n], box['y'] + 24
        d.line([(MX + MW + 4, sy), (t, sy), (t, cy_), (box['x'] - 6, cy_)], GREY if colour == YELLOW else colour, sw=1.1)

    footer = max(left_bottom, middle_bottom, ey, cy) + 40
    for i, words in enumerate(spec['footer']):
        aside(MX, footer + i * 40, words, 2200, 22, RED if words.startswith('❓') else INK)
    f['height'] = footer + 40 * len(spec['footer']) + 60
    d.badge(f)
    if builder is None:
        builder = Path(__file__).resolve()
        builder = next((builder.relative_to(p).as_posix() for p in builder.parents if (p / 'plugins').is_dir()),
                       builder.name)
    d.write(out, builder)
    preview(d, f, out.with_suffix('.png'))
    print(f"{section} in one frame: {len(rows)} sentences, {sum(1 for _ in cards)} evidence cards, {k} asks, "
          f"{len((reply or {}).get('items', []))} replies, {len(edits)} change cards, "
          f"{sum(len(v) for v in marks.values())} pale boxes → {out.name}")
    return out


def preview(d, f, png):
    """Each pale box at its opacity, the pictures, then the words."""
    out = Image.new('RGBA', (int(f['width']), int(f['height'])), 'white')
    for e in d.els:
        kind = e['type']
        if kind not in ('rectangle', 'frame', 'line', 'arrow', 'image'):
            continue
        x, y, w, h = (e[k_] for k_ in ('x', 'y', 'width', 'height'))
        layer = Image.new('RGBA', out.size)
        p = ImageDraw.Draw(layer)
        if kind in ('rectangle', 'frame'):
            bg = e['backgroundColor']
            stroke = e['strokeColor'] if kind != 'frame' else '#c8cdd4'
            p.rectangle((x, y, x + w, y + h), fill=None if bg == 'transparent' else bg,
                        outline=None if stroke == 'transparent' else stroke, width=max(1, int(e['strokeWidth'])))
        elif kind in ('line', 'arrow'):
            pts = [(e['x'] + a, e['y'] + b) for a, b in e['points']]
            p.line(pts, fill=e['strokeColor'], width=max(1, int(e['strokeWidth'])))
            if kind == 'arrow' and len(pts) > 1:
                a, b = pts[-2:]
                ang, L = math.atan2(b[1] - a[1], b[0] - a[0]), 9
                p.polygon([b, (b[0] - L * math.cos(ang - .4), b[1] - L * math.sin(ang - .4)),
                           (b[0] - L * math.cos(ang + .4), b[1] - L * math.sin(ang + .4))], fill=e['strokeColor'])
        else:
            raw = d.files[e['fileId']]['dataURL'].split(',', 1)[1]
            im = Image.open(io.BytesIO(base64.b64decode(raw))).convert('RGBA').resize((int(w), int(h)))
            layer.alpha_composite(im, (int(x), int(y)))
        if e.get('opacity', 100) < 100:
            layer.putalpha(layer.getchannel('A').point(lambda a, o=e['opacity']: round(a * o / 100)))
        out = Image.alpha_composite(out, layer)
    p = ImageDraw.Draw(out)
    for e in d.els:
        if e['type'] != 'text':
            continue
        for i, line in enumerate(e['text'].split('\n')):
            p.text((e['x'], e['y'] + i * e['fontSize'] * 1.25), line, fill=e['strokeColor'],
                   font=font(e['fontSize'], e.get('fontFamily', 6)))
    save_preview(out.convert('RGB'), png)


def words(e):
    return ' '.join((e.get('originalText') or e.get('text') or '').split())


def sync(face, out=None, dry=False):
    """Read the canvas back into the files (sentences into §3, a person's marks into the feedback record), then
    rebuild it. Returns (applied, recorded)."""
    import datetime
    face = Path(face).resolve()
    spec = spec_of(face)
    out = Path(out) if out else face.with_suffix('.excalidraw')
    doc = json.loads(out.read_text())
    els = [e for e in doc['elements'] if not e.get('isDeleted')]
    draft_file = next(iter((face.parent / spec['draft_folder']).glob('*-draft-v*.md')))
    stem = draft_file.name.split('-draft-v')[0]
    record = draft_file.parent / 'records' / f'{stem}-feedback.md'
    stamp = datetime.datetime.now().strftime('%y%m%d %H%M')

    # 1. sentences typed over: (address, n, built, now)
    rows = [e for e in els if e['type'] == 'text' and (e.get('customData') or {}).get('sentence')]
    edited = [(e['customData']['sentence']['address'], e['customData']['sentence']['n'],
               e['customData']['sentence']['built'], words(e)) for e in rows
              if words(e) != e['customData']['sentence']['built']]

    # 2. a person's own marks, not yet recorded: each at the sentence it sits beside
    band = sorted((e['y'], e['y'] + e['height'], e['customData']['sentence']['address'],
                   e['customData']['sentence']['n'], e['x']) for e in rows)
    text_x = min((b[4] for b in band), default=0)

    def beside(x, y):
        if not band:
            return 'the canvas'
        a, z, address, n, _ = min(band, key=lambda b: 0 if b[0] <= y <= b[1] else min(abs(y - b[0]), abs(y - b[1])))
        col = 'the file and logic' if x < text_x - 60 else 'the text' if x < text_x + 1000 else 'the cards'
        return f'S{n} ({address}), in {col}'

    colour = {'#e03131': 'red', '#2f9e44': 'green', '#1971c2': 'blue', '#1e1e1e': 'black'}
    marks = []
    for e in els:
        if e['id'].startswith('s-') or (e.get('customData') or {}).get('recorded') or e.get('containerId'):
            continue
        if e['type'] not in ('text', 'rectangle', 'ellipse', 'diamond', 'arrow', 'line', 'freedraw'):
            continue
        cx, cy = e['x'] + e.get('width', 0) / 2, e['y'] + e.get('height', 0) / 2
        bound = next((t for t in els if t.get('containerId') == e['id']), None)
        what = words(e) if e['type'] == 'text' else words(bound) if bound else ''
        kind = f"a {colour.get(e.get('strokeColor'), e.get('strokeColor'))} {e['type']}"
        if e['type'] in ('arrow', 'line') and e.get('points'):
            (x0, y0), (x1, y1) = e['points'][0], e['points'][-1]
            where = f"from {beside(e['x'] + x0, e['y'] + y0)} to {beside(e['x'] + x1, e['y'] + y1)}"
        else:
            where = f'beside {beside(cx, cy)}'
        marks.append((e, f'{kind} {where}' + (f': "{what}"' if what else '')))

    for address, n, built, now in edited:
        print(f'S{n} {address}\n  before: {built}\n  after:  {now}')
    for _, line in marks:
        print(f'mark: {line}')
    if not edited and not marks:
        print(f'{out.name}: nothing new on the canvas')
    if dry or (not edited and not marks):
        return edited, marks

    if edited:                                           # into §3 by address; the line must still read as built
        lines = draft_file.read_text(encoding='utf-8').split('\n')
        want = {(a, b): now for a, _, b, now in edited}
        section, para, hit = None, None, 0
        for k, line in enumerate(lines):
            if (m := re.match(r'^## (\d+) · (\w+)', line)):
                section = m[2]
            if (m := re.match(r'^### (C\d+\.P\d+)', line)):
                para = m[1]
            m = re.match(r'^(- B(\d+) · S\d+ · )(.*\S)\s*$', line)
            if section == 'Draft' and m and (f'{para}.B{m[2]}', m[3]) in want:
                lines[k] = m[1] + want[(f'{para}.B{m[2]}', m[3])]
                hit += 1
        if hit != len(want):
            raise SystemExit(f'{draft_file.name}: {len(want) - hit} edited sentence(s) no longer read as built; '
                             'the Draft changed since this canvas was built: rebuild, then type the edit again')
        draft_file.write_text('\n'.join(lines), encoding='utf-8')

    record.parent.mkdir(exist_ok=True)
    head = '' if record.is_file() else (f'Feedback · {stem}\n{"=" * (11 + len(stem))}\n\nWritten by excalidraw-draft '
                                        '`section_canvas.py sync`: what a person did on a Section canvas. An agent '
                                        'turns the marks into Revise cards or a §1 change.\n')
    entry = [f'\n{stamp} · {out.name}']
    entry += [f'- applied S{n} {a}: "{b}" → "{now}"' for a, n, b, now in edited]
    entry += [f'- [ ] {line}' for _, line in marks]
    with record.open('a', encoding='utf-8') as fh:
        fh.write(head + '\n'.join(entry) + '\n')

    gone = {id(e) for e in rows if words(e) != e['customData']['sentence']['built']}
    for e, _ in marks:
        e['customData'] = {**(e.get('customData') or {}), 'recorded': stamp}
    doc['elements'] = [e for e in doc['elements'] if id(e) not in gone]
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1))
    print(f'{len(edited)} sentence(s) into {draft_file.name}; {len(marks)} mark(s) into records/{record.name}')
    build(face, out, builder=doc.get('source'))
    return edited, marks


if __name__ == '__main__':
    import sys as _sys
    if len(_sys.argv) > 1 and _sys.argv[1] == 'sync':
        sp = argparse.ArgumentParser(description='read the canvas back into the files, then rebuild it')
        sp.add_argument('face', type=Path)
        sp.add_argument('--out', type=Path, help='the drawing (default: beside the face)')
        sp.add_argument('--dry', action='store_true', help='only say what would be written')
        a = sp.parse_args(_sys.argv[2:])
        sync(a.face, a.out, a.dry)
        raise SystemExit
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('face', type=Path, help="the topic's face, holding the `canvas:` yaml")
    ap.add_argument('--out', type=Path, help='where the drawing goes (default: beside the face)')
    a = ap.parse_args()
    build(a.face, a.out)
