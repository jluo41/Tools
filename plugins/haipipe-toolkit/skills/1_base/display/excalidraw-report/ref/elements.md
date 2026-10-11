# Display elements: Python helpers for a scratch, and for tidy views

Copy what the drawing needs into `studio/_build/build_<name>.py`. Each builder carries its
own copy (no shared import), so a Block's drawings rebuild even if this file changes.
Every helper takes real values the script has read from disk (a file listing, a receipt,
a csv, a skill's own text). Do not type a number into a helper that the script could read.

The scratch helpers come first: they are the default. The "Tidy views" sections below are
for a polished frame the person asked for.


## Scratch: hand-drawn elements on a shared canvas

```python
import json, random, sys
from pathlib import Path

random.seed(1)                                   # stable ids and seeds, so a rebuild diffs cleanly
HAND, MONO = 6, 3                                # Excalidraw fonts: Nunito (readable sans), Cascadia (mono); never 1 Virgil / 5 Excalifont
INK, GRAY, RED, BLUE = "#1e1e1e", "#868e96", "#e03131", "#1971c2"
STICKY = {"ask": "#ffec99", "fit": "#b2f2bb", "bend": "#ffd8a8", "none": "#e9ecef", "open": "#ffc9c9"}
els = []


def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False, angle=0.0):
    e = {"id": f"s-{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": angle,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 1, "opacity": 100, "groupIds": [],
         "frameId": None, "roundness": {"type": 3} if kind == "rectangle" else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=22, color=INK, font=HAND, angle=0.0, container=None):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (0.6 if font == MONO else 0.58)
    e = base("text", x, y, w, len(lines) * size * 1.25, color, angle=angle)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
             containerId=container, autoResize=True, lineHeight=1.25)
    return e


def box(x, y, w, h, stroke=INK, bg="transparent", dashed=False, sw=2, angle=0.0):
    return base("rectangle", x, y, w, h, stroke, bg, sw, dashed, angle)


def sticky(x, y, w, h, body, kind, size=20):
    """A note the person can double-click and rewrite: its text is bound to it."""
    h = max(h, 40 + (body.count("\n") + 1) * size * 1.35)   # straight, sized to its text
    r = box(x, y, w, h, INK, STICKY[kind], sw=1)
    t = text(x + 16, y + 14, body, size, INK, container=r["id"])
    r["boundElements"] = [{"type": "text", "id": t["id"]}]
    return r


def mono(x, y, lines, size=15, width=None, title=None):
    """Real lines (a tree, a receipt, a matrix) in a rough box; returns its bottom."""
    w = width or max(len(l) for l in lines) * size * 0.6 + 40
    top = 34 if title else 14
    box(x, y, w, top + len(lines) * size * 1.3 + 16, GRAY, "#f8f9fa", sw=1)
    if title:
        text(x + 14, y + 8, title, 18, GRAY)
    for i, l in enumerate(lines):
        text(x + 18, y + top + i * size * 1.3, l, size, INK, MONO)
    return y + top + len(lines) * size * 1.3 + 16


def mark(x, y, w, h, color=RED):                 # a rectangle fitted to the one line that matters
    base("rectangle", x, y, w, h, color, sw=2)    # (not an ellipse: it cuts across neighbouring lines)
# for line i of a mono() block at size s: mark(x + 10, top_y + i * s * 1.3 - 3, len(line) * s * 0.6 + 16, s * 1.3 + 6)


def arrow(pts, color=INK, sw=2, dashed=False):   # from a hand note to what it is about
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base("arrow", x, y, max(abs(p[0]) for p in rel) or 1, max(abs(p[1]) for p in rel) or 1, color,
             sw=sw, dashed=dashed)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow")


def write(out):
    """Superseded: judging edits by `version` fails, since an Excalidraw save re-stamps every
    element. Use the snapshot writer, `haipipe-studio`'s `scripts/canvas.py`
    (`canvas.write(out, els, source)`): content-based ids, a seed snapshot beside the
    builder, the person's additions, edits and deletions kept."""
```

A folder tree for `mono()`: walk the real directory and indent with `└ ` / `├ `, clipping
long names (about 66 characters at 14px fills a 760px box). Ids stay stable only while the
drawing code keeps its order; reordering it redraws every untouched seed element.


# Tidy views (only when a polished frame is asked for)

## Core: elements, frames, writing the file

```python
import base64, hashlib, json, random, struct
from pathlib import Path

random.seed(1)                                   # stable ids and seeds, so a rebuild diffs cleanly
INK, GRAY, LIGHT, RULE = "#1e1e1e", "#6b7280", "#adb5bd", "#e9ecef"
GREEN, ORANGE, RED, BLUE = "#2f9e44", "#e8590c", "#c92a2a", "#1971c2"
FILL = {"blue": "#e7f5ff", "green": "#ebfbee", "orange": "#fff4e6", "gray": "#f8f9fa", "red": "#fff5f5"}
EDGE = {"blue": BLUE, "green": GREEN, "orange": ORANGE, "gray": LIGHT, "red": RED}
DOT = {"done": GREEN, "todo": ORANGE, "later": LIGHT, "bad": RED, "info": BLUE}
EM, MONO_EM = 0.55, 0.62                         # text width per character, as a share of font size
els, FILES, FRAME = [], {}, [None]               # FRAME[0]: every element drawn now belongs to it


def base(kind, x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False, rounded=True):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
         "strokeColor": stroke, "backgroundColor": bg, "fillStyle": "solid", "strokeWidth": sw,
         "strokeStyle": "dashed" if dashed else "solid", "roughness": 0, "opacity": 100, "groupIds": [],
         "frameId": FRAME[0], "roundness": {"type": 3} if rounded else None,
         "seed": random.randint(1, 2**31 - 1), "version": 1, "versionNonce": random.randint(1, 2**31 - 1),
         "isDeleted": False, "boundElements": [], "updated": 1, "link": None, "locked": False}
    els.append(e)
    return e


def text(x, y, s, size=18, color=INK, align="left", link=None, mono=False):
    lines = s.split("\n")
    w = max(len(l) for l in lines) * size * (MONO_EM if mono else EM)
    e = base("text", x - {"left": 0, "center": w / 2, "right": w}[align], y, w, len(lines) * size * 1.25,
             color, rounded=False)
    e.update(text=s, originalText=s, fontSize=size, fontFamily=3 if mono else 6, textAlign=align,
             verticalAlign="top", containerId=None, autoResize=True, lineHeight=1.25, link=link)
    return e


def rect(x, y, w, h, stroke=INK, bg="transparent", sw=2, dashed=False, rounded=True):
    return base("rectangle", x, y, w, h, stroke, bg, sw, dashed, rounded)


def dot(x, y, color, r=9):
    return base("ellipse", x - r, y - r, 2 * r, 2 * r, color, color, 1, rounded=False)


def line(pts, color=INK, sw=2, dashed=False, arrow=False):
    x, y = pts[0]
    rel = [[px - x, py - y] for px, py in pts]
    e = base("arrow" if arrow else "line", x, y, max(abs(p[0]) for p in rel), max(abs(p[1]) for p in rel),
             color, sw=sw, dashed=dashed, rounded=False)
    e.update(points=rel, lastCommittedPoint=None, startBinding=None, endBinding=None,
             startArrowhead=None, endArrowhead="arrow" if arrow else None)
    return e


def pill(x_right, y, label, color=BLUE):          # a small tag, right-aligned at x_right
    w = len(label) * 15 * EM + 22
    rect(x_right - w, y - 15, w, 30, color, "#ffffff", 1.5)
    text(x_right - w / 2, y - 9, label, 15, color, "center")


def frame(name, x, y=0, w=1800, h=10):            # fix e["height"] (and width) once the content is drawn
    FRAME[0] = None
    e = base("frame", x, y, w, h, "#bbbbbb", rounded=False)
    e["name"] = name
    FRAME[0] = e["id"]
    return e


def write(out):
    Path(out).write_text(json.dumps({"type": "excalidraw", "version": 2, "source": "studio/_build/" + Path(__file__).name,
                                     "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                                     "files": FILES}, ensure_ascii=False, indent=1))
```

Views side by side in one file: draw each view at `x = X`, then move `X` past it.

```python
X, GAP = 0, 200
for name, draw in [("Answer", draw_answer), ("Evidence", draw_evidence), ("Flow", draw_flow)]:
    fr = frame(name, X)
    bottom, right = draw(X + 60, 40)             # each view returns its bottom y and right edge
    fr["height"], fr["width"] = bottom + 60, right - X + 60
    X += fr["width"] + GAP
FRAME[0] = None
```


## Headline and sources (every frame)

```python
def headline(x, y, answer, sub):                 # the answer as a sentence, one gray line under it
    text(x, y, answer, 44, INK)
    text(x, y + 66, sub, 20, GRAY)
    return y + 120


def sources(x, y, items):                        # items: [(label, relative link)], clickable
    text(x, y, "Sources", 16, GRAY)
    sx = x + 90
    for label, link in items:
        text(sx, y, label, 16, BLUE, link=link)
        sx += len(label) * 16 * EM + 34
    return y + 40
```


## Table: real cells

```python
def table(x, y, header, rows, widths, num=(), size=18, colors=None):
    """header: column names; rows: lists of cell strings; num: column indexes right-aligned;
    colors: {(row, col): color} to mark the cells the headline is about."""
    rh, W = size * 2.1, sum(widths)
    for k in range(0, len(rows), 2):             # banded rows
        rect(x, y + rh * (k + 1), W, rh, "transparent", FILL["gray"], rounded=False)
    line([(x, y + rh - 4), (x + W, y + rh - 4)], LIGHT, 1.5)
    cx = x
    for j, (head, w) in enumerate(zip(header, widths)):
        right = j in num
        tx, al = (cx + w - 14, "right") if right else (cx + 14, "left")
        text(tx, y + rh * 0.22, head, size - 2, GRAY, al)
        for i, row in enumerate(rows):
            text(tx, y + rh * (i + 1) + rh * 0.22, str(row[j]), size, (colors or {}).get((i, j), INK), al)
        cx += w
    return y + rh * (len(rows) + 1) + 24
```

Column widths: about `max(len(cell)) * size * EM + 40` per column. Numbers right-aligned,
with the same number of decimals down a column. More than about 15 rows: show the rows
the answer turns on and say "top <k> of <n>" in the sub line.


## Charts: horizontal bars and dot-intervals on one scale

```python
def hbars(x, y, w, items, hi, fmt="{:.1f}%", label_w=320, highlight=()):
    """items: [(label, value)]; one bar per row, value printed at the bar's end."""
    rh, L, R = 40, x + label_w, x + w - 100
    for i, (label, v) in enumerate(items):
        ry, col = y + i * rh, BLUE if label in highlight else LIGHT
        text(x, ry + 8, label, 19)
        rect(L, ry + 6, max(3, (R - L) * v / hi), rh - 14, col, col, 1, rounded=False)
        text(L + (R - L) * v / hi + 10, ry + 8, fmt.format(v), 17)
    return y + rh * len(items) + 30


def intervals(x, y, w, rows, lo, hi, ticks, zero=0, label_w=320, note_w=280, axis=""):
    """rows: [(label, estimate, low, high, state, note)]: a line for the interval, a dot for the
    estimate, coloured by state; a dashed line at `zero` (no effect)."""
    rh, L, R = 44, x + label_w, x + w - note_w
    sx = lambda v: L + (v - lo) / (hi - lo) * (R - L)
    top, bot = y, y + rh * len(rows)
    for v in ticks:
        line([(sx(v), top), (sx(v), bot)], RULE, 1)
        text(sx(v), bot + 8, f"{v:g}", 15, GRAY, "center")
    if lo < zero < hi:
        line([(sx(zero), top - 6), (sx(zero), bot)], GRAY, 2, dashed=True)
    for i, (label, est, a, b, state, note) in enumerate(rows):
        ry = top + rh * i + rh / 2
        text(x, ry - 12, label, 20)
        line([(sx(a), ry), (sx(b), ry)], DOT[state], 4)
        dot(sx(est), ry, DOT[state], 8)
        text(R + 20, ry - 11, note, 17, GRAY)
    text(L, bot + 34, axis, 15, GRAY)
    return bot + 70
```

Vertical bars and grouped bars (a cluster per group) are in b11's `build_q_reports.py`
(`bars()`, `clusters()`); use them when the categories are few and short.


## Figure: an existing PNG, embedded

```python
def image(path, x, y, max_w):
    """A figure a Run already made (matplotlib, a Result's plot), embedded so the drawing is self-contained."""
    raw = Path(path).read_bytes()
    pw, ph = struct.unpack(">II", raw[16:24])     # PNG width and height from the IHDR chunk
    w = min(max_w, pw); h = w * ph / pw
    fid = hashlib.sha1(raw).hexdigest()
    FILES[fid] = {"mimeType": "image/png", "id": fid, "created": 1, "lastRetrieved": 1,
                  "dataURL": "data:image/png;base64," + base64.b64encode(raw).decode("ascii")}
    e = base("image", x, y, w, h, "transparent", rounded=False)
    e.update(fileId=fid, status="saved", scale=[1, 1], crop=None)
    return y + h + 30
```

Give the figure a title line above it that says what it shows and what to see in it
(`<measure> by <group>; <group> highest`), and draw a call-out at the point that matters. If the figure's own
fonts are too small at the frame's width, regenerate the PNG larger rather than shrinking it.


## Folder tree and code excerpt: monospace

```python
def fs_tree(root, depth=2, notes=None, skip=("__pycache__",)):
    """The real tree under `root`, `depth` levels deep; notes: {relative path: short note}."""
    root, notes = Path(root), notes or {}
    def walk(p, d, pre):
        kids = sorted(k for k in p.iterdir() if k.name not in skip and not k.name.startswith("."))
        out = []
        for i, k in enumerate(kids):
            last, rel = i == len(kids) - 1, k.relative_to(root).as_posix()
            note = f"   # {notes[rel]}" if rel in notes else ""
            out.append(pre + ("└── " if last else "├── ") + k.name + ("/" if k.is_dir() else "") + note)
            if k.is_dir() and d > 1:
                out += walk(k, d - 1, pre + ("    " if last else "│   "))
        return out
    return [root.name + "/"] + walk(root, depth, "")


def excerpt(path, a, b):
    """Lines a..b (1-based, inclusive) of a real file, with their line numbers."""
    lines = Path(path).read_text().splitlines()[a - 1:b]
    return "\n".join(f"{a + i:>4}  {l}" for i, l in enumerate(lines))


def mono_block(x, y, body, title=None, size=16):
    """A gray box of monospace text: a tree from fs_tree(), or an excerpt() of code or config."""
    lines = body.split("\n")
    w, h = max(len(l) for l in lines) * size * MONO_EM + 40, len(lines) * size * 1.25 + 32
    if title:
        text(x, y, title, 17, GRAY)
        y += 30
    rect(x, y, w, h, LIGHT, FILL["gray"], 1.5, rounded=False)
    text(x + 20, y + 16, body, size, INK, mono=True)
    return y + h + 24
```

Keep a tree to the 10 to 25 lines that matter (depth 2, `skip` the rest) and a code excerpt
to the 5 to 20 lines that make the point; a call-out can point at the one line that matters.


## Comparison: A vs B, or before vs after

```python
def compare(x, y, w, a, b, rows, label_w=320, size=19):
    """rows: [(aspect, (a_value, state), (b_value, state))]; the dot shows which side is better."""
    cw, rh = (w - label_w) / 2, 46
    text(x + label_w, y, a, 22, BLUE)
    text(x + label_w + cw, y, b, 22, BLUE)
    line([(x, y + 38), (x + w, y + 38)], LIGHT, 1.5)
    for i, (aspect, *cells) in enumerate(rows):
        ry = y + 54 + i * rh
        text(x, ry, aspect, size)
        for k, (v, state) in enumerate(cells):
            cx = x + label_w + k * cw
            dot(cx + 9, ry + 12, DOT[state])
            text(cx + 28, ry, v, size)
    return y + 54 + rh * len(rows) + 24
```

The cells hold values (`<rate>`, `<n> rows`, `<k> of <n> releases`), not "better"/"worse".


## Flow: numbered steps down one spine

```python
def spine(x, y, steps, dy=70, right=None):
    """steps: [(name, detail, value, who)]: a numbered circle, the step, one gray detail line,
    the step's real value (a count, a file, a time), and who does it as a tag."""
    line([(x + 20, y + 20), (x + 20, y + 20 + dy * (len(steps) - 1))], GREEN, 3)
    for i, (name, detail, value, who) in enumerate(steps):
        sy = y + i * dy
        base("ellipse", x, sy, 40, 40, GREEN, "#ffffff", 2, rounded=False)
        text(x + 20, sy + 9, str(i + 1), 18, GREEN, "center")
        text(x + 60, sy + 2, name, 22)
        text(x + 60, sy + 32, detail, 16, GRAY)
        if value:
            text(x + 520, sy + 6, value, 20, BLUE)
        if who and right:
            pill(right, sy + 20, who, ORANGE)
    return y + dy * len(steps) + 20
```


## Status rows and the dot key

```python
KEYTEXT = {"done": "done", "todo": "to do or decide", "later": "later / no change", "bad": "problem", "info": "fact"}


def key(x, y, states):                           # only the colours this frame uses
    for s in states:
        dot(x + 9, y + 11, DOT[s]); text(x + 26, y, KEYTEXT[s], 17, GRAY)
        x += 60 + len(KEYTEXT[s]) * 17 * EM
    return y + 40


def status_row(x, y, state, label, detail, tag=None, right=None, label_w=380):
    dot(x + 9, y + 12, DOT[state])
    text(x + 30, y, label, 22)
    text(x + 30 + label_w, y + 3, detail, 18, GRAY)
    if tag and right:
        pill(right, y + 12, tag)
    return y + 46
```

The status view (headline, a few big blocks with the key numbers, an orange "still to do"
strip, zones of status rows) is b11's `report()`; copy it when the report's question is
"where do things stand".


## Call-out: a note pointing at one element

```python
def callout(x, y, note, target, color=ORANGE, size=18):
    """A short note in a coloured box at (x, y), with an arrow to `target` (x, y): the cell,
    bar, line of code or point on a figure the note is about."""
    w, h = len(note) * size * EM + 32, size * 1.25 + 24
    rect(x, y, w, h, color, FILL["orange"] if color == ORANGE else "#ffffff", 2)
    text(x + 16, y + 12, note, size, color)
    sx = x if target[0] < x else x + w if target[0] > x + w else x + w / 2
    sy = y + h / 2 if sx != x + w / 2 else (y if target[1] < y else y + h)
    line([(sx, sy), target], color, 2, arrow=True)
```

Place call-outs in the margin beside what they point at, never on top of data; at most
three per frame, so each one is noticed.


## The PNG preview

The Pillow previewer (`render_png.py`) draws text by `fontFamily`: hand text in a hand-like
system font, monospace in Menlo, the rest proportional. It does not draw roughness or small
rotations; it is a preview of the seed, Excalidraw shows the real canvas.

```python
FONTS = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Helvetica.ttc",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
MONO = ["/System/Library/Fonts/Menlo.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
HAND = ["/System/Library/Fonts/Supplemental/ChalkboardSE.ttc", "/System/Library/Fonts/Noteworthy.ttc"]

def font(size, family=2):                        # 1 hand, 3 mono, 5 hand (Excalifont)
    for f in {1: HAND, 3: MONO, 5: HAND}.get(family, []) + FONTS:
        if Path(f).exists():
            return ImageFont.truetype(f, max(6, int(size)))
    return ImageFont.load_default()
# ...and in the text loop: font(e["fontSize"] * s, e.get("fontFamily", 2))
```

Right-aligned text is drawn from its `x`, so a table's numbers line up only as well as `EM`
estimates their width; check the column edges in the render.
