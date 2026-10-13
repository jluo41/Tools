"""excalidraw-studio's drawing helpers: one set for every Studio topic builder (b31 s01-D08).

A builder makes one Drawing, draws its frames with these helpers, lays them out by acts, then writes:

    sys.path.insert(0, str(<skills>/1_base/display/excalidraw-studio/scripts))
    from draw import Drawing
    d = Drawing()
    f = d.frame("① The principles: one mind map")
    d.heading("🧠 The principles", "one line on what the frame says")
    d.mind_map("the centre", branches)            # or a flow, boxes, a folder tree for real folders
    d.badge(f)                                    # principle 6: the frame's density, measured
    d.acts([{"name": "Act 1 · ...", "frames": [f["id"], g["id"]], "arrow": "lives in"}])
    d.write(out, "build_sNN_<topic>.py")

The rules these follow are the skill's SKILL.md (the principles, the look); the writer that keeps a person's marks
is haipipe-studio's canvas.write, called by `write`.
"""
from __future__ import annotations

import base64
import io
import json
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
STUDIO = HERE.parents[2] / "project/haipipe-studio/scripts"       # haipipe-studio's canvas.py, its writer
sys.path.insert(0, str(STUDIO))
import canvas  # noqa: E402

INK, RED, GREEN = canvas.INK, canvas.RED, canvas.GREEN
GREY = "#868e96"                      # a table's rules, and a value not yet checked
KEY = "#fff3bf"                       # principle 5: the one slight colour, a frame's key point
W, H = 2560, 1440                     # principle 1: one screen, whole at 50% zoom
T_ACT, T_FRAME, T_NODE, T_KEY, T_TEXT, T_SMALL = 56, 60, 38, 30, 24, 21   # principle 5: big for the logic
FLOOR = getattr(canvas, "SPARSE_MIN", 120)                          # principle 6: words per million px, a text frame
MAP_FLOOR = 70                       # retired by principle 7 (261012): a map is measured by its words; kept for old builders
SMALL, MAP_WORDS, SMALL_SHARE = 28, 200, 0.25   # principle 7: a map holds few words, few of them a detail (under 28 px)


class Drawing:
    """The elements and embedded files of one drawing, and the frame being drawn into."""

    def __init__(self):
        self.els: list = []
        self.files: dict = {}
        self.fid = None

    # ── elements ────────────────────────────────────────────────────────────────────────────────────────────
    def el(self, kind, x, y, w, h, **extra):
        n = len(self.els)
        e = {"id": f"e{n}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
             "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": self.fid,
             "roundness": None, "seed": n + 1, "version": 1, "versionNonce": n + 1, "isDeleted": False,
             "boundElements": [], "updated": 1, "link": None, "locked": False}
        e.update(extra)
        self.els.append(e)
        return e

    @staticmethod
    def measure(s, size=T_TEXT, code=False):
        """A line's width as Excalidraw draws it: Cascadia is 0.6 em a letter; Nunito is measured, a Chinese
        character a full em (canvas.text_width). Excalidraw cuts a text element at its width, so a width guessed
        for English cut Chinese lines in half (asked 261012: "this is not complete")."""
        return len(s) * size * 0.6 if code else canvas.text_width(s, size)

    def text(self, x, y, s, size=T_TEXT, color=INK, code=False):
        lines = str(s).split("\n")
        return self.el("text", x, y, max(self.measure(ln, size, code) for ln in lines) + 4,
                       len(lines) * size * 1.25, text=str(s), originalText=str(s), fontSize=size,
                       fontFamily=canvas.CODE_FONT if code else canvas.FONT, textAlign="left", verticalAlign="top",
                       containerId=None, autoResize=True, lineHeight=1.25, strokeColor=color)

    @staticmethod
    def wrap(s, width, size=T_TEXT, code=False):
        if not code:                                   # measured, and a line may break before a Chinese character
            return "\n".join(canvas.wrap_text(" ".join(str(s).split()), size, width))
        return "\n".join(textwrap.wrap(" ".join(str(s).split()), max(8, int(width / (size * 0.6))),
                                       break_long_words=False))      # a name like canvas.small_text stays whole

    @classmethod
    def height(cls, s, width, size=T_TEXT, code=False):
        return len(cls.wrap(s, width, size, code).split("\n")) * size * 1.25

    def para(self, x, y, s, width, size=T_TEXT, color=None, code=False):
        """Wrapped text, red when it is an open point (❓ or ❌ first); returns the y below it."""
        s = str(s)
        color = color or (RED if s.lstrip().startswith(("❓", "❌", "?")) else INK)
        return y + self.text(x, y, self.wrap(s, width, size, code), size, color, code)["height"]

    def box(self, x, y, w, h, color=INK, sw=1.5, fill=None, dashed=False):
        return self.el("rectangle", x, y, w, h, strokeColor=color, strokeWidth=sw, roundness={"type": 3},
                       backgroundColor=fill or "transparent", fillStyle="solid",
                       strokeStyle="dashed" if dashed else "solid")

    def key(self, x, y, w, h, sw=3):
        """Principle 5: the frame's key point, the one slight colour."""
        return self.box(x, y, w, h, INK, sw, KEY)

    def line(self, points, color=INK, arrow=True, dashed=False, sw=1.5):
        x0, y0 = points[0]
        xs, ys = [p[0] for p in points], [p[1] for p in points]
        return self.el("arrow" if arrow else "line", x0, y0, max(1, max(xs) - min(xs)), max(1, max(ys) - min(ys)),
                       strokeColor=color, strokeWidth=sw, strokeStyle="dashed" if dashed else "solid",
                       points=[[x - x0, y - y0] for x, y in points], lastCommittedPoint=None, startBinding=None,
                       endBinding=None, startArrowhead=None, endArrowhead="arrow" if arrow else None)

    def grid_table(self, x, y, columns, rows, widths, size=30, pad=40):
        """A table drawn as b03's model × engine grid (asked 261012 of b01: "I want the tables like this"): column
        names in small type, one grey rule above each row, no boxes. `rows`: [{cells, dim}]; a cell is words, or a
        value {big, tag, color}: its number large, its mark and Run small under it (grey unchecked, red broken).
        A dim row (a candidate, not chosen) is grey. `pad`: the room in a row around its words (a long table of
        one-line rows reads closer). Returns the y below the last row."""
        xs = [x + sum(widths[:k]) for k in range(len(widths))]
        right = x + sum(widths)
        self.rows_at = []                              # each row's (top, height): a chart beside it lines up
        hh = max(self.height(c, w - 24, 28) for c, w in zip(columns, widths))
        for cx, c, w in zip(xs, columns, widths):
            self.para(cx, y, c, w - 24, 28, GREY)
        y += hh + 26
        for r in rows:
            cells, dim = r.get("cells") or [], r.get("dim")
            tall = [(c.get("size", 44) * 1.25 + (34 if c.get("tag") else 0)) if isinstance(c, dict)
                    else self.height(str(c), w - 24, size) for c, w in zip(cells, widths)]
            rh = max(tall + [size * 1.25]) + pad
            self.rows_at.append((y, rh))
            self.line([(x, y), (right, y)], GREY, arrow=False)
            for cx, c, w in zip(xs, cells, widths):
                if isinstance(c, dict):
                    col = c.get("color") or (GREY if dim else INK)
                    if c.get("big"):
                        self.text(cx, y + pad / 2, str(c["big"]), c.get("size", 44), col)
                    if c.get("tag"):
                        self.text(cx, y + pad / 2 + (c.get("size", 44) * 1.25 if c.get("big") else 0), str(c["tag"]),
                                  24, col)
                elif str(c):
                    self.para(cx, y + pad / 2, str(c), w - 24, size, GREY if dim else None)
            y += rh
        self.line([(x, y), (right, y)], GREY, arrow=False)
        return y

    # ── frames ──────────────────────────────────────────────────────────────────────────────────────────────
    def frame(self, name, w=W, h=H):
        """A new frame of one screen; what is drawn next belongs to it. Name it '<①> <what it says>'."""
        self.fid = None
        f = self.el("frame", 0, 0, w, h, name=name)
        self.fid = f["id"]
        return f

    def heading(self, title, sub="", width=W - 640):
        self.text(40, 22, title, T_FRAME)
        if sub:
            self.para(40, 110, sub, width, T_SMALL)

    def picture(self, path, x, y, w, hmax, fid=None):
        """A preview (png), scaled to fit w x hmax, embedded as a jpeg at 1.5x; returns its height. `fid`: its own
        id, when two pictures share a file name (every Task's full_scan.png); else one is drawn twice."""
        from PIL import Image
        img = Image.open(path).convert("RGB")
        scale = min(w / img.width, hmax / img.height)
        dw, dh = img.width * scale, img.height * scale
        small = img.resize((max(1, int(dw * 1.5)), max(1, int(dh * 1.5))), Image.LANCZOS)
        buf = io.BytesIO()
        small.save(buf, "JPEG", quality=82)
        fid = fid or "img-" + re.sub(r"[^a-z0-9]+", "-", Path(path).stem.lower())
        self.files[fid] = {"mimeType": "image/jpeg", "id": fid, "created": 1,
                           "dataURL": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}
        self.box(x - 2, y - 2, dw + 4, dh + 4, INK, 1)
        self.el("image", x, y, dw, dh, fileId=fid, status="saved", scale=[1, 1])
        return dh

    # ── principle 6: density, measured ──────────────────────────────────────────────────────────────────────
    @staticmethod
    def words_in(s):
        """Words a reader reads: spaced words, two Chinese characters as one, each folder and file of a path."""
        s = str(s)
        cjk = len(re.findall(r"[\u3400-\u9fff]", s))
        rest = re.sub(r"[\u3400-\u9fff]", " ", s).replace("/", " ")
        return len(rest.split()) + (cjk + 1) // 2

    @staticmethod
    def room(frame):
        """Mark a frame laid out with room between its boxes (principle 8, asked 261012: "leave some rooms, not all
        the things nested together"): principle 6 measures its words over its boxes, not the space between them."""
        frame.setdefault("customData", {})["room"] = True
        return frame

    @staticmethod
    def area_of(elements, f):
        """The px² principle 6 divides by: the frame's, or for a frame with room (principle 8) its boxes' sum."""
        if not (f.get("customData") or {}).get("room"):
            return f["width"] * f["height"]
        boxes = [e for e in elements if e.get("frameId") == f["id"] and e.get("type") == "rectangle"
                 and not e.get("isDeleted") and not (e.get("customData") or {}).get("aside")]
        return sum(e["width"] * e["height"] for e in boxes) or f["width"] * f["height"]

    @classmethod
    def words_per_mpx(cls, elements, fid, w, h):
        words = sum(cls.words_in(e.get("text", "")) for e in elements
                    if e.get("frameId") == fid and e.get("type") == "text" and e.get("strokeColor") != GREEN
                    and not e.get("isDeleted"))
        f = next((e for e in elements if e.get("id") == fid and e.get("type") == "frame"), None)
        area = cls.area_of(elements, {**f, "width": w, "height": h}) if f else w * h
        return round(words / max(area / 1e6, 0.01)), words

    @staticmethod
    def kind(elements, f):
        """'picture' (holds an image or draws a screen: not measured, as canvas.sparse), 'map' (boxes joined by
        arrows or lines: a flow, a mind map) or 'text'."""
        mine = [e for e in elements if e.get("frameId") == f["id"] and not e.get("isDeleted")]
        if (f.get("customData") or {}).get("ui") or any(e.get("type") == "image" for e in mine):
            return "picture"
        arrows = sum(1 for e in mine if e.get("type") in ("arrow", "line"))    # a mind map's links are lines
        boxes = sum(1 for e in mine if e.get("type") == "rectangle")
        return "map" if arrows >= 3 and boxes >= 4 else "text"     # four steps in a row: three arrows (b31 s06 Open 4)

    @classmethod
    def words_small(cls, elements, fid):
        """A frame's words and how many are small (under SMALL px): principle 7. A green change note and the badge
        (canvas.aside) are not counted."""
        texts = [e for e in elements if e.get("frameId") == fid and e.get("type") == "text" and not e.get("isDeleted")
                 and e.get("strokeColor") != GREEN and not (e.get("customData") or {}).get("aside")]
        words = sum(cls.words_in(e.get("text", "")) for e in texts)
        return words, sum(cls.words_in(e.get("text", "")) for e in texts if e.get("fontSize", 20) < SMALL)

    @staticmethod
    def detail(frame):
        """Mark the frame that holds the detail principle 7 sends out of a map (a video's full frame, a Run's
        record): read up close, it is measured by principle 6 (words per million px), not by 7's 200 words.
        Asked 261012: "I still cannot get the full picture of the rNN of a video". Returns it."""
        frame.setdefault("customData", {})["detail"] = True
        return frame

    @staticmethod
    def is_detail(frame):
        return bool((frame.get("customData") or {}).get("detail"))

    @classmethod
    def detail_floor(cls, elements, fid):
        """⑥'s floor for a detail frame, scaled by its body type: FLOOR × (24 / body px)². ⑥'s 120 was set for body
        words of 20 to 24 px; ⑦ wants 28 px or more, and a word at 30 px takes (30/24)² of the room, so a frame just
        as full reads 77 (measured by the Proj10 session on b51 s01, 261012). Body = the size most words are set in."""
        sizes = {}
        for e in elements:
            if e.get("frameId") == fid and e.get("type") == "text" and not e.get("isDeleted") and \
                    e.get("strokeColor") != GREEN and not (e.get("customData") or {}).get("aside"):
                sizes[e.get("fontSize", 20)] = sizes.get(e.get("fontSize", 20), 0) + cls.words_in(e.get("text", ""))
        body = max(sizes, key=sizes.get) if sizes else 24
        return round(FLOOR * (24 / max(body, 24)) ** 2)

    def badge(self, f):
        """The frame's own measure in its top right corner: a text frame's density against its floor (principle 6),
        a map's words and its small ones (principle 7); a picture or a screen is not measured."""
        kind = self.kind(self.els, f)
        if kind == "map" and not self.is_detail(f):
            words, small = self.words_small(self.els, f["id"])
            ok = words <= MAP_WORDS and small <= SMALL_SHARE * max(words, 1)
            top = f"🪶 {words} words, {round(100 * small / max(words, 1))}% small"
            low = f"{'✅' if ok else '❌'} a map: at most {MAP_WORDS} words, {round(100 * SMALL_SHARE)}% small"
        else:
            per, words = self.words_per_mpx(self.els, f["id"], f["width"], f["height"])
            floor = self.detail_floor(self.els, f["id"]) if self.is_detail(f) else FLOOR
            ok = kind == "picture" or per >= floor
            top = f"📊 {per} words per million px"
            low = "🖼️ holds pictures: not measured" if kind == "picture" else \
                f"{'✅' if ok else '❌'} a {'detail' if self.is_detail(f) else 'text'} frame, floor {floor} · {words} words"
        color = INK if ok else RED
        canvas.aside(self.box(f["width"] - 590, 24, 550, 74, color, 1.5))
        for e in (self.text(f["width"] - 572, 30, top, T_SMALL + 3, color),
                  self.text(f["width"] - 572, 64, low, T_SMALL, color)):
            canvas.aside(e)

    @classmethod
    def density_of(cls, path):
        """Each frame of a drawing on disk, top left first: (name, words per million px, kind)."""
        path = Path(path)
        if not path.is_file():
            return []
        drawn = json.loads(path.read_text(encoding="utf-8"))["elements"]
        fs = sorted((e for e in drawn if e.get("type") == "frame" and not e.get("isDeleted")),
                    key=lambda e: (e["y"], e["x"]))
        return [(re.sub(r"^s\d+ · ", "", str(e.get("name") or "")),
                 cls.words_per_mpx(drawn, e["id"], e["width"], e["height"])[0], cls.kind(drawn, e)) for e in fs]

    # ── patterns: a mind map, a flow, a folder tree for real folders ─────────────────────────────────────────
    def branch_height(self, b, w, title=34, leaf=21):
        bold = str(b.get("by", "")).startswith("asked")
        h = 22 + self.height(b["title"], w - 52, title) + (30 if bold else 0) + 10
        if b.get("summary"):
            h += self.height(b["summary"], w - 52, 28) + 12
        for lf in b.get("leaves", []):
            h += self.height("· " + str(lf), w - 52, leaf) + 6
        return h + 14

    def branch(self, b, x, y, w, h=None, title=34, leaf=21):
        """One branch of a mind map: its title, when it was asked (bold), its summary large, its leaves small."""
        bold = str(b.get("by", "")).startswith("asked")
        h = h or self.branch_height(b, w, title, leaf)
        self.box(x, y, w, h, INK, 3.5 if bold else 1.5)
        yy = self.para(x + 26, y + 18, b["title"], w - 52, title)
        if bold:
            self.text(x + 26, yy + 2, f"{b['by']}, in the asker's words", T_SMALL)
            yy += 30
        yy += 10
        if b.get("summary"):
            yy = self.para(x + 26, yy, b["summary"], w - 52, 28) + 12
        for lf in b.get("leaves", []):
            yy = self.para(x + 26, yy, ("" if str(lf).startswith("❓") else "· ") + str(lf), w - 52, leaf) + 6
        return (x, y, w, h)

    def mind_map(self, centre, branches, top=196, bw=790):
        """A centre (the key point) with up to three branches above, two beside and three below, every line along
        a bus between the rows so no line crosses a box. Bold branches (by: asked …) go above and below first.
        The frame grows taller than a screen only as far as its rows need. Returns the y below it."""
        bold = [b for b in branches if str(b.get("by", "")).startswith("asked")]
        rest = [b for b in branches if b not in bold]
        order = bold + rest
        up, side, down = order[:3], order[6:8], order[3:6]
        gap = (W - 80 - 3 * bw) / 2
        xs = [40, 40 + bw + gap, 40 + 2 * (bw + gap)]
        ch = max(210, self.height(centre, bw - 68, 44) + 44)         # grows only past three lines of words
        h1 = max([self.branch_height(b, bw) for b in up] or [0])
        h3 = max([self.branch_height(b, bw) for b in down] or [0])
        band0 = top + h1 + 44
        band1 = band0 + max([self.branch_height(b, bw) for b in side] + [ch])
        ups = [self.branch(b, x, top, bw, h1) for b, x in zip(up, xs)]
        downs = [self.branch(b, x, band1 + 44, bw, h3) for b, x in zip(down, xs)]
        cy = (band0 + band1) / 2 - ch / 2
        self.key(xs[1], cy, bw, ch, 4.5)
        self.para(xs[1] + 34, cy + 36, centre, bw - 68, 44)
        sides = []
        for b, x in zip(side, (xs[0], xs[2])):
            sh = self.branch_height(b, bw)
            sides.append(self.branch(b, x, (band0 + band1) / 2 - sh / 2, bw))
        cx = xs[1] + bw / 2
        for row, bus_y, edge, is_up in ((ups, band0 - 22, cy, True), (downs, band1 + 22, cy + ch, False)):
            if not row:
                continue
            self.line([(cx, edge), (cx, bus_y)], arrow=False, sw=3)
            self.line([(row[0][0] + bw / 2, bus_y), (row[-1][0] + bw / 2, bus_y)], arrow=False, sw=3)
            for x, y, w, h in row:
                self.line([(x + bw / 2, bus_y), (x + bw / 2, y + h if is_up else y)], arrow=False, sw=3)
        for x, y, w, h in sides:
            sx = xs[1] if x < xs[1] else xs[1] + bw
            self.line([(sx, cy + ch / 2), (x + w if x < xs[1] else x, cy + ch / 2)], arrow=False, sw=2)
        bottom = band1 + 44 + h3 if downs else band1
        return bottom

    def flow(self, steps, x, y, w, h=None, gap=60, title=30, leaf=21, labels=()):
        """A workflow in one row: a box per step (title, lines), an arrow between each, its words above it
        (labels). A step whose title starts with ❓ is drawn red and dashed. Returns the boxes (x, y, w, h)."""
        bw = (w - gap * (len(steps) - 1)) / len(steps)
        hh = h or max(22 + self.height(s["title"], bw - 40, title) + 10 +
                      sum(self.height("· " + str(l_), bw - 40, leaf) + 6 for l_ in s.get("lines", [])) + 14
                      for s in steps)
        out = []
        for i, s in enumerate(steps):
            bx = x + i * (bw + gap)
            open_ = str(s["title"]).startswith("❓")
            if s.get("key"):
                self.key(bx, y, bw, hh)
            else:
                self.box(bx, y, bw, hh, RED if open_ else INK, 2.5, dashed=open_)
            yy = self.para(bx + 20, y + 16, s["title"], bw - 40, title, RED if open_ else INK) + 10
            for l_ in s.get("lines", []):
                yy = self.para(bx + 20, yy, ("" if str(l_).startswith("❓") else "· ") + str(l_), bw - 40, leaf) + 6
            out.append((bx, y, bw, hh))
            if i:
                self.line([(bx - gap + 4, y + 50), (bx - 4, y + 50)], sw=3)
                if i - 1 < len(labels) and labels[i - 1]:
                    self.text(bx - gap + 6, y + 8, labels[i - 1], T_SMALL)
        return out

    NOTES = {"SKILL.md": "the rules", "CHANGELOG.md": "its versions", "agents/": "Codex's card", "ref/": "the contracts",
             "scripts/": "its scripts", "tests/": "its tests"}

    @classmethod
    def folder_tree(cls, folder, open_=(), most=6, notes=None):
        """A real folder as a folder tree (principle 4: only for folders): its entries, those in `open_` opened one
        level (.py, .md, .yaml), a note beside the ones `notes` names."""
        notes = {**cls.NOTES, **(notes or {})}
        folder = Path(folder)
        if not folder.is_dir():
            return [f"❓ {folder.name}/ is gone"]
        entries = sorted([p for p in folder.iterdir() if not p.name.startswith((".", "__"))],
                         key=lambda p: (p.is_dir(), p.name))
        out = [folder.name + "/"]
        for i, p in enumerate(entries):
            last = i == len(entries) - 1
            name = p.name + ("/" if p.is_dir() else "")
            note = notes.get(name, "")
            if p.is_dir() and p.name not in open_:
                n = sum(1 for q in p.rglob("*") if q.is_file() and "__pycache__" not in q.parts)
                note = f"{note}, {n} files" if note else f"{n} files"
            out.append(f"{'└──' if last else '├──'} {name:<16} {note}".rstrip())
            if p.is_dir() and p.name in open_:
                kids = sorted(q for q in p.iterdir() if q.suffix in (".py", ".md", ".yaml") and not q.name.startswith("_"))
                for j, q in enumerate(kids[:most]):
                    end = j == len(kids[:most]) - 1 and len(kids) <= most
                    out.append(f"{'    ' if last else '│   '}{'└──' if end else '├──'} {q.name:<16} "
                               f"{notes.get(q.name, '')}".rstrip())
                if len(kids) > most:
                    out.append(f"{'    ' if last else '│   '}└── … {len(kids) - most} more")
        return out

    # ── principle 3: the frames as acts, a row each, named at the left, a named arrow for each step ──────────
    def acts(self, acts, between=(), gap=340):
        """`acts`: [{name, frames: [frame ids in the row], arrow: words for each step across}], `between`:
        [(from frame id, to frame id, words)] for a step down to another act. Lays the frames out (canvas.grid),
        names each act at the left of its row, draws the arrows."""
        canvas.grid(self.els, [a["frames"] for a in acts], gap=gap)
        self.fid = None
        at = {e["id"]: e for e in self.els if e["type"] == "frame"}
        steps = []
        for a in acts:
            words = a.get("arrow")
            arrows = words if isinstance(words, list) else [words] * (len(a["frames"]) - 1)
            steps += [(x, y, w_) for x, y, w_ in zip(a["frames"], a["frames"][1:], arrows)]
        steps += list(between)
        for a, b, words in steps:
            fa, fb = at[a], at[b]
            if abs(fa["x"] - fb["x"]) < 10:                              # one above the other: bottom to top
                x = fa["x"] + fa["width"] / 2
                self.line([(x, fa["y"] + fa["height"] + 14), (x, fb["y"] - 14)], sw=6)
                if words:
                    self.text(x + 20, (fa["y"] + fa["height"] + fb["y"]) / 2 - 24, words, 40)
            else:                                                        # side by side: right side to left side
                y = fa["y"] + min(fa["height"], fb["height"]) / 2
                self.line([(fa["x"] + fa["width"] + 14, y), (fb["x"] - 14, y)], sw=6)
                if words:
                    self.text(fa["x"] + fa["width"] + 24, y - 62, words, 40)
        for a in acts:
            f0 = at[a["frames"][0]]
            self.para(f0["x"] - 820, f0["y"] + 20, a["name"], 760, T_ACT)

    # ── write ───────────────────────────────────────────────────────────────────────────────────────────────
    def write(self, out, source):
        """canvas.write keeps a person's marks; the palette is off, so what a builder draws stays as drawn (since
        haipipe-studio 0.13.14 the palette keeps the key-point colour too, so a builder on canvas.write keeps it)."""
        return canvas.write(Path(out), self.els, source, files=self.files, palette=False)
