"""workflow_drawing.py · a study's building map (excalidraw-workflow).

One map, read left to right: the finished data → its sources or inputs → the tests → the analysis each
sub-question needs → the sub-question, its guess and its claim → where the answer lands in the paper. A light
version sits on top, one box per column; below it, the foundation columns and one row per sub-question. Solid =
exists on disk; dashed = not run, no code, or not opened.

With a version's comments reports, the map carries a **review overlay** (JL 261014: "highlight that which part the
reviewers wanted us to change, and how will our new field experiment and analysis will fix it"): a card the
reviewers attacked gets a red border and a red ❗ line naming the Review Items; a card whose work answers them gets a
green border and a green 🛠 line. The overlay is read from each Review Item's `hits` and `fixed by` cells
(haipipe-paper-comments); an item that lands on no card is listed under the map, red when nothing fixes it.

A paper's workflow topic holds its words in `<topic>-drawing.yaml` (the foundation cards and the links between them,
the displays, the notes; excalidraw-workflow's SKILL.md has the keys) and a forwarding builder:

    python workflow_drawing.py draw <topic folder>                 redraw one (what the topic's builder calls)
    python workflow_drawing.py make <topic folder> [--force]       the forwarding builder, and a words yaml if none

Read on every build, never copied in: the telling's face (board.md's `story-current:`; its §5 E, §6 D and §7 T
tables), each Board Question's report (its `#### 3.N · Question N · RQN` block: name, question, Section, Tasks,
hypotheses, claims, contributions, work), the Task folders under the Project's `work/` (or `tasks/`), and the newest
version's comments reports. The drawing is written through haipipe-studio's canvas.write, so a person's marks on it
survive the next build; the builder's own boxes are never moved by hand.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "project/haipipe-studio/scripts"))
import canvas  # noqa: E402

INK, INK2, INK3, RULE = "#1e1e1e", "#495057", "#868e96", "#ced4da"
ACC = "#1864ab"                         # the claim column: what the paper would say
RED, GREEN = canvas.RED, canvas.GREEN   # the review overlay: what the reviewers attacked, what fixes it
CW = 0.6                                # a character's width, in em, for wrapping

# the six columns: x and width
XD, WD = 30, 400
XS, WS = 490, 440
XT, WT = 990, 440
XA, WA = 1490, 440
XC, WC = 2010, 500
XF, WF = 2570, 420
RIGHT = XF + WF
COLS = {"D": (XD, WD), "S": (XS, WS), "T": (XT, WT), "A": (XA, WA), "C": (XC, WC), "F": (XF, WF)}


# ── where things are ──────────────────────────────────────────────────────────────────────────────────────────
def up(start, name):
    """The nearest folder at or above `start` that holds `name`."""
    p = Path(start).resolve()
    p = p if p.is_dir() else p.parent
    while p != p.parent:
        if (p / name).exists():
            return p
        p = p.parent
    raise SystemExit(f"no {name} above {start}")


def space_root(start):
    return up(start, "env.sh")


def tasks_root(board):
    project = up(board, "project.yaml")
    return project / "work" if (project / "work").is_dir() else project / "tasks"


def telling_face(board):
    """The telling's face: board.md's `story-current:` topic, else an older Board's A1-Story Page."""
    text = (board / "board.md").read_text(encoding="utf-8")
    m = re.search(r"(?m)^story-current:\s*(\S+)", text)
    if m:
        for p in (board / "studio" / m[1] / f"{m[1]}.md", board / "A1-Story" / m[1] / f"{m[1]}.md"):
            if p.is_file():
                return p
    old = sorted(board.glob("A1-Story/Story*/Story*.md"))
    if old:
        return old[-1]
    raise SystemExit(f"{board.name}: no telling (board.md story-current:, or A1-Story/)")


def board_questions(board):
    """board.md's ## Questions yaml: [{id, title, report, work, ...}]."""
    text = (board / "board.md").read_text(encoding="utf-8")
    m = re.search(r"## Questions\s*\n+```yaml\n(.*?)\n```", text, re.S)
    return (yaml.safe_load(m.group(1)) or {}).get("questions", []) if m else []


# ── the telling, read at run time ─────────────────────────────────────────────────────────────────────────────
def story_table(lines, first):
    """The Markdown table whose header starts with `| first |`, as one dict per row ({} when absent)."""
    for i, ln in enumerate(lines):
        if ln.startswith(f"| {first} |"):
            head = [h.strip() for h in ln.strip().strip("|").split("|")]
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(head, [c.strip() for c in row.strip().strip("|").split("|")])))
            return rows
    return []


def short(s):
    """'Name: the sentence' -> ('Name', 'the sentence'); a name may end in '?'."""
    name, _, rest = s.partition(": ")
    return name.strip(), rest.strip()


def story_questions(lines):
    """Every `#### 3.N · Question N · RQN` block: name, question, Section, Tasks, hypotheses, claims, contributions,
    work."""
    qs, cur, part = [], None, None
    for ln in lines:
        m = re.match(r"^#### 3\.\d+ · Question (\d+) · (RQ\d+)", ln)
        if m:
            cur = {"n": int(m[1]), "rq": m[2], "hyp": [], "claims": [], "contrib": [], "work": [], "tasks": []}
            qs.append(cur)
            part = None
            continue
        if ln.startswith(("### ", "#### ")):
            cur = None
            continue
        if cur is None:
            continue
        m = re.match(r"^- \*\*(Name|Question|Section)\*\*: (.*)$", ln)
        if m:
            cur[m[1].lower()] = m[2].strip()
            continue
        m = re.match(r"^\*\*(Tasks|Hypotheses|Potential claims|Potential contributions|Potential work)\*\*$", ln.strip())
        if m:
            part = m[1]
            continue
        if part == "Tasks":
            m = re.match(r"^- (\w+) · (.+?): (.+)$", ln)
            if m:
                cur["tasks"].append((m[1], m[2].strip(), m[3].strip()))
        elif part == "Hypotheses":
            m = re.match(r"^- \*\*(\w+)\*\* · (.+?) · tested by (.+)$", ln)
            if m:
                name, what = short(m[2])
                cur["hyp"].append({"code": m[1], "name": name, "what": what, "tested": re.findall(r"E\d+", m[3])})
        elif part == "Potential claims":
            m = re.match(r"^- \*\*(\w+)\*\* · (C\d+) · from \S+ · (.+)$", ln)
            if m:
                name, what = short(m[3])
                cur["claims"].append({"code": m[1], "c": m[2], "name": name, "what": what})
            m = re.match(r"^\s+- \*\*(Role|Now)\*\*: (.*)$", ln)
            if m and cur["claims"]:
                cur["claims"][-1][m[1].lower()] = m[2].strip()
        elif part == "Potential contributions":
            m = re.match(r"^- rests on .+? · (.+)$", ln)
            if m:
                cur["contrib"].append(short(m[1])[0])
        elif part == "Potential work":
            m = re.match(r"^- \*\*([TD]\d+)\*\* · for ([^·]+?)(?: · (.+))?$", ln)
            if m:
                cur["work"].append({"id": m[1], "for": m[2].strip()})
    return qs


def e_state(cell):
    c = cell.lower()
    return next((s for s in ("absent", "established", "provisional", "contradicted", "gated") if s in c), cell)


class Telling:
    """What the map reads from the paper: the face's tables, the Board Questions' blocks, the Task folders."""

    def __init__(self, board):
        self.board = board
        self.face = telling_face(board)
        lines = self.face.read_text(encoding="utf-8").splitlines()
        qs = []
        for q in board_questions(board):
            rp = board / str(q.get("report", ""))
            if q.get("report") and rp.is_file():
                qs += story_questions(rp.read_text(encoding="utf-8").splitlines())
        self.qs = sorted(qs or story_questions(lines), key=lambda q: q["n"])
        if not self.qs:
            raise SystemExit(f"{self.face.name}: no '#### 3.N · Question N · RQN' block in the reports or the face")
        self.T = {r["T"]: r for r in story_table(lines, "T")}
        self.D = {r["D"]: r for r in story_table(lines, "D")}
        self.E = {r["E"]: e_state(r.get("support state", "")) for r in story_table(lines, "E")}
        topic = next((ln for ln in lines if ln.startswith("**Topic:**")), "")       # a telling's topic face
        if topic:
            self.call = topic.replace("**Topic:**", "").strip()
        elif "## Opening" in lines:                                                    # an older Story Page
            self.call = next((ln for ln in lines[lines.index("## Opening") + 1:] if ln.strip()), "")
        else:
            self.call = ""
        self.tasks = tasks_root(board)

    def tname(self, t):
        return f"{t} {self.T[t]['name']}" if t in self.T else t

    def task_dirs(self, b, j, t):
        jobs = sorted(self.tasks.glob(f"b{b}_*/j{j}_*"))
        return [p for job in jobs for p in (sorted(job.glob(f"t{t}_*")) + sorted(job.glob(f"*/t{t}_*"))) if p.is_dir()]

    @staticmethod
    def ran(dirs):
        """True when a Run's result/ (or an older results/) holds a real file (a .gitignore is not a result)."""
        for d in dirs:
            for res in [d / "results"] + sorted(d.glob("runs/*/result")):
                if res.is_dir() and any(p.is_file() and not p.name.startswith(".") for p in res.rglob("*")):
                    return True
        return False

    def task_folders(self, text):
        """'Task: b02.j01.t01, b01.j01.' -> [('b02.j01', 't01_regression_robustness', ran?), ...]."""
        out = []
        for b, j, t in re.findall(r"b(\d\d)\.j(\d\d)(?:\.t(\d\d))?", text):
            if t:
                dirs = self.task_dirs(b, j, t)
                names = sorted({d.name for d in dirs}) or [f"t{t}"]
                out.append((f"b{b}.j{j}", names[0], self.ran(dirs)))
            else:
                for job in sorted(self.tasks.glob(f"b{b}_*/j{j}_*")):
                    names = {p.name for p in [*job.glob("*/t[0-9][0-9]_*"), *job.glob("t[0-9][0-9]_*")] if p.is_dir()}
                    for name in sorted(names):
                        out.append((f"b{b}.j{j}", name, self.ran(self.task_dirs(b, j, name[1:3]))))
        return out


# ── the review overlay ────────────────────────────────────────────────────────────────────────────────────────
def review_items(board, version=None):
    """The Review Items of the newest version's comments reports (or `version`'s): one dict per row, its `hits` and
    `fixed by` cells split into anchors. Returns (items, report paths)."""
    versions = [board / version] if version else sorted(
        (p for p in board.glob("j[0-9][0-9]_v*") if p.is_dir()), key=lambda p: p.name, reverse=True)
    for v in versions:
        pages = [q for q in sorted(v.glob("reports/q[0-9][0-9]_*/q[0-9][0-9]_*.md"))
                 if q.stem == q.parent.name and re.search(r"(?m)^page-type:\s*(comments|round)\b",
                                                         q.read_text(encoding="utf-8", errors="replace"))]
        items = []
        for page in pages:
            text = page.read_text(encoding="utf-8")
            if "\n## Review Items\n" not in text:
                continue
            seg = text.split("\n## Review Items\n", 1)[1].split("\n## ", 1)[0]
            rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in seg.splitlines() if ln.startswith("|")]
            rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
            if not rows:
                continue
            head = [h.lower() for h in rows[0]]
            for r in rows[1:]:
                x = dict(zip(head, r))
                x["page"] = page
                for col in ("hits", "fixed by"):
                    x[col] = [a.strip() for a in re.split(r"[·,]", x.get(col, "")) if a.strip() and a.strip() != "—"]
                items.append(x)
        if items:
            return items, pages
    return [], []


def label(item):
    """'Review-more-shots' -> 'more shots'."""
    return re.sub(r"^Review-", "", item.get("item", "")).replace("-", " ")


class Review:
    """Which cards the reviewers attacked and which answer them, by anchor: a card's `key`, a Task or Discovery id
    (T9, D2), a claim id (C1), a Question's landing (Q1), or a Section stem (t03_research-design)."""

    def __init__(self, items):
        self.items = items
        self.hits, self.fixes, self.drawn = {}, {}, set()
        for x in items:
            for a in x["hits"]:
                self.hits.setdefault(a, []).append(x)
            for a in x["fixed by"]:
                self.fixes.setdefault(a, []).append(x)

    def lines(self, keys, size=13):
        """The overlay lines for a card known by `keys`, and its border colour (red when hit, green when it fixes)."""
        hit = [x for k in keys for x in self.hits.get(k, [])]
        fix = [x for k in keys for x in self.fixes.get(k, [])]
        out = []
        if hit:
            out.append(("❗ reviewers: " + ", ".join(dict.fromkeys(label(x) for x in hit)), size, RED))
        if fix:
            out.append(("🛠 fixes: " + ", ".join(dict.fromkeys(label(x) for x in fix)), size, GREEN))
        self.drawn |= {(x["item"], "hit") for x in hit} | {(x["item"], "fix") for x in fix}
        return out, (RED if hit else GREEN if fix else None)

    def leftovers(self):
        """Items no card answers: (item, the Sections that answer it in writing) and (item, nothing answers it)."""
        writing, open_ = [], []
        for x in self.items:
            if (x["item"], "fix") in self.drawn:
                continue
            stems = [a for a in x["fixed by"] if re.match(r"^t\d\d_", a)]
            (writing if stems else open_).append((x, stems))
        return writing, open_


# ── drawing ───────────────────────────────────────────────────────────────────────────────────────────────────
class Canvas:
    def __init__(self):
        self.els, self.n = [], 9000

    def base(self, t, x, y, w, h, stroke=INK, fill="transparent", sw=2, style="solid", rounded=False):
        self.n += 1
        return {"id": f"{t[:3]}-{self.n}", "type": t, "x": x, "y": y, "width": w, "height": h, "angle": 0,
                "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid", "strokeWidth": sw,
                "strokeStyle": style, "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
                "roundness": {"type": 3} if rounded else None, "seed": self.n, "version": 1,
                "versionNonce": self.n * 7, "isDeleted": False, "boundElements": None, "updated": 1790000000000,
                "link": None, "locked": False}

    def rect(self, x, y, w, h, stroke=INK, sw=2, style="solid", fill="#ffffff"):
        self.els.append(self.base("rectangle", x, y, w, h, stroke, fill, sw, style, True))

    def text(self, x, y, s, size=14, color=INK2):
        lines = s.split("\n")
        e = self.base("text", x, y, max(len(ln) for ln in lines) * size * CW, size * 1.25 * len(lines), stroke=color)
        e.update({"text": s, "fontSize": size, "fontFamily": canvas.FONT, "textAlign": "left", "verticalAlign": "top",
                  "containerId": None, "originalText": s, "lineHeight": 1.25, "autoResize": True})
        self.els.append(e)

    def line(self, pts, stroke=INK2, sw=2, style="solid", arrow=False):
        x0, y0 = pts[0]
        rel = [[px - x0, py - y0] for px, py in pts]
        xs, ys = [p[0] for p in rel], [p[1] for p in rel]
        e = self.base("arrow" if arrow else "line", x0, y0, max(xs) - min(xs), max(ys) - min(ys), stroke,
                      "transparent", sw, style)
        e.update({"points": rel, "lastCommittedPoint": None, "startBinding": None, "endBinding": None,
                  "startArrowhead": None, "endArrowhead": "arrow" if arrow else None})
        if arrow:
            e["elbowed"] = False
        self.els.append(e)


def wrap(s, width, size):
    room, out, cur = max(8, int(width / (size * CW))), [], ""
    for word in str(s).split():
        if cur and len(cur) + 1 + len(word) > room:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return out + [cur] if cur else out


def card(c, x, y, w, lines, dashed=False, stroke=INK, sw=2, pad=14):
    """A rounded box around lines of (text, size, colour), each wrapped to the box. Returns its height."""
    rows = [(part, sz, col) for s, sz, col in lines for part in wrap(s, w - 2 * pad, sz)]
    h = 10 + sum(int(sz * 1.55) for _, sz, _ in rows) + 8
    if stroke in (RED, GREEN):
        c.rect(x, y, w, h, stroke=stroke, sw=3 if stroke == RED else 2, style="dashed" if dashed else "solid")
    else:
        c.rect(x, y, w, h, stroke=INK3 if dashed else stroke, sw=1 if dashed else sw,
               style="dashed" if dashed else "solid")
    yy = y + 10
    for s, sz, col in rows:
        c.text(x + pad, yy, s, sz, col)
        yy += int(sz * 1.55)
    return h


def overview(c, boxes, top):
    """The light version: one box per column, lined up with the full map below. Returns its height."""
    c.text(30, top, "THE LAYOUT AT A GLANCE · the light version; the full map is below, column by column", 17, INK)
    y, h = top + 44, 80
    at = {}
    for k, title, l1, l2 in boxes:
        x, w = COLS[k]
        c.rect(x, y, w, h, stroke=ACC if k == "C" else INK, sw=2)
        c.text(x + 16, y + 10, title, min(18, (w - 32) / (max(1, len(title)) * CW)), ACC if k == "C" else INK)
        c.text(x + 16, y + 38, l1, min(14, (w - 32) / (max(1, len(l1)) * CW)), INK2)
        c.text(x + 16, y + 58, l2, min(12, (w - 32) / (max(1, len(l2)) * CW)), INK3)
        at[k] = (x, w)
    ym = y + h / 2
    for a, b in (("D", "S"), ("S", "T"), ("T", "A"), ("A", "C"), ("C", "F")):
        if a in at and b in at:
            c.line([(at[a][0] + at[a][1], ym), (at[b][0] - 2, ym)], stroke=INK2, sw=2, arrow=True)
    yb = y + h + 30
    for x0, x1, words in ((XD, XT + WT, "the foundation · every question stands on it"),
                          (XA, XF + WF, "one row per sub-question")):
        c.line([(x0, yb - 8), (x0, yb), (x1, yb), (x1, yb - 8)], stroke=INK3, sw=1)
        c.text((x0 + x1) / 2 - len(words) * 15 * CW / 2, yb + 6, words, 15, INK2)
    return yb + 40 - top


def bracket(c, x, froms, tos, dashed_to=()):
    """Thin ticks from the right edges in froms to a vertical line at x, then arrows to the left edges in tos."""
    for fx, fy in froms:
        c.line([(fx, fy), (x, fy)], stroke=INK3, sw=1)
    ys = [fy for _, fy in froms] + [ty for _, ty in tos]
    if len(ys) > 1:
        c.line([(x, min(ys)), (x, max(ys))], stroke=INK3, sw=1)
    for i, (tx, ty) in enumerate(tos):
        d = i in dashed_to
        c.line([(x, ty), (tx - 2, ty)], stroke=INK3 if d else INK2, sw=1 if d else 2,
               style="dashed" if d else "solid", arrow=True)


class Map:
    """One build: the telling, the SPEC, the review overlay, and where each card landed."""

    def __init__(self, telling, spec, review):
        self.t, self.spec, self.rv = telling, spec, review
        self.c = Canvas()
        self.at = {}                       # card key -> (x, y, w, h)

    # one foundation card, from its SPEC entry
    def fcard(self, item, x, y, w):
        t = self.t
        keys = [item.get("key")] + ([item["task"]] if item.get("task") else [])
        q_tasks = [(f"{k} · {name}: {what}", 12, INK2)                 # a question's Tasks, from its report
                   for q in t.qs if q["n"] == item.get("tasks_of") for k, name, what in q["tasks"]]
        if item.get("task"):
            row = t.T.get(item["task"], {})
            dirs = t.task_folders(row.get("feeds", ""))
            done = any(r for *_, r in dirs)
            where = item.get("where") or (", ".join(f"{j} {n}" for j, n, _ in dirs[:2]) if dirs else "no task folder yet")
            state = item.get("state", "ran" if done else "not run")
            lines = [(t.tname(item["task"]), 15, INK), (item.get("line") or row.get("question", ""), 12, INK2),
                     (where, 12, INK3)] + ([(state, 12, INK if done else INK3)] if state else []) + q_tasks
            dashed = item.get("dashed", not done)
        elif item.get("tasks_of"):
            lines = [(item["title"], 16, INK)] + q_tasks
            dashed = item.get("dashed", False)
        else:
            lines = [(item["title"], item.get("size", 15), INK)] + [(ln, 13, INK2) for ln in item.get("lines", [])] + \
                    ([(item["gray"], 12, INK3)] if item.get("gray") else [])
            dashed = item.get("dashed", False)
        extra, stroke = self.rv.lines([k for k in keys if k])
        h = card(self.c, x, y, w, lines + extra, dashed=dashed, stroke=stroke or item.get("stroke", INK),
                 sw=item.get("sw", 2))
        if item.get("key"):
            self.at[item["key"]] = (x, y, w, h)
        if item.get("task"):
            self.at.setdefault(item["task"], (x, y, w, h))
        return h

    def column(self, k, top):
        """A foundation column: its cards top to bottom, a group drawn as small cards inside one dashed box."""
        x, w = COLS[k]
        y, prev = top, None
        for item in self.spec["foundation"].get(k, []):
            y += item.get("gap", 0)
            if "group" in item:
                gtop = y + 22
                gy = gtop
                for sub in item["group"]:
                    gy += self.fcard({**sub, "size": 14, "sw": 1, "stroke": INK2}, x + 10, gy, w - 20) + 8
                self.c.rect(x - 10, gtop - 8, w + 20, gy - gtop + 8, stroke=INK3, sw=1, style="dashed", fill="transparent")
                if item.get("key"):
                    self.at[item["key"]] = (x - 10, gtop - 8, w + 20, gy - gtop + 8)
                if prev:
                    self.c.line([(x + w / 2, prev), (x + w / 2, gtop - 10)], stroke=INK3, sw=1)
                prev, y = gy, gy + 14
                continue
            h = self.fcard(item, x, y, w)
            if prev is not None and item.get("down"):
                self.c.line([(x + w / 2, prev), (x + w / 2, y - 2)], stroke=INK3 if item.get("dashed_arrow") else INK2,
                            sw=1 if item.get("dashed_arrow") else 2, style="dashed" if item.get("dashed_arrow") else "solid",
                            arrow=True)
            prev, y = y + h, y + h + 14
        return y

    def links(self, bottom):
        """Arrows between foundation cards: right edge to a bus just left of the target column, then in; 'under' goes
        below the columns first."""
        for k, ln in enumerate(self.spec.get("links", [])):
            a, b = self.at.get(ln["from"]), self.at.get(ln["to"])
            if not a or not b:
                print(f"link {ln['from']} -> {ln['to']}: no such card")
                continue
            ay, by = a[1] + min(40, a[3] / 2), b[1] + min(40, b[3] / 2) + ln.get("dy", 0)
            col = ln.get("color", INK3 if ln.get("dashed") else INK2)
            style, sw = ("dashed", 1) if ln.get("dashed") else ("solid", 2)
            bus = b[0] - 26 - ln.get("bus", 0)
            if ln.get("route") == "under":
                low = bottom + 20
                pts = [(a[0] + a[2], ay), (a[0] + a[2] + 14, ay), (a[0] + a[2] + 14, low), (bus - 12, low),
                       (bus - 12, by), (b[0] - 2, by)]
                if ln.get("label"):
                    self.c.text(a[0] + a[2] + 20, low + 4, ln["label"], 12, INK3)
            else:
                pts = [(a[0] + a[2], ay), (bus, ay), (bus, by), (b[0] - 2, by)]
                if ln.get("label"):
                    self.c.text(a[0] + a[2] + 4, ay - 22, ln["label"], 12, INK3)
            self.c.line(pts, stroke=col, sw=sw, style=style, arrow=True)

    def rows(self, top):
        """One row per sub-question, grouped by question: analysis → sub-question and claim → where it lands."""
        t, c, spec = self.t, self.c, self.spec
        foundation = {i.get("task") for col in spec["foundation"].values() for i in col if i.get("task")} | \
                     {s.get("task") for col in spec["foundation"].values() for i in col for s in i.get("group", [])}
        y, seen = top, {}
        for q in t.qs:
            gtop = y
            c.text(XA, y + 4, f"Question {q['n']} · {q.get('name', q['rq'])}", 18, INK)
            qlines = wrap(q.get("question", ""), RIGHT - XA - 20, 13)
            for k, s in enumerate(qlines):
                c.text(XA, y + 32 + 18 * k, s, 13, INK2)
            y += 40 + 18 * len(qlines)
            ay, a_edges = y, []
            for w in [w for w in q["work"] if w["id"] not in foundation]:
                wid = w["id"]
                row = t.T.get(wid) or t.D.get(wid) or {"name": "", "question": ""}
                if wid in seen:
                    h = card(c, XA, ay, WA, [(f"{wid} {row['name']}", 14, INK), (f"the same work as Question {seen[wid]}", 12, INK3)],
                             dashed=True)
                    a_edges.append((XA + WA, ay + h / 2, True))
                    ay += h + 10
                    continue
                seen[wid] = q["n"]
                if wid in t.T:
                    dirs = t.task_folders(row.get("feeds", ""))
                    done = any(r for *_, r in dirs)
                    where = (", ".join(f"{j} {n}" for j, n, _ in dirs[:2]) if dirs else "no task folder yet")
                    lines = [(f"{wid} {row['name']}", 15, INK), (row.get("question", ""), 12, INK2), (where, 12, INK3),
                             ("ran" if done else "not run", 12, INK if done else INK3)]
                    dashed = not done
                else:
                    folder = row.get("folder", "")
                    dashed = "none yet" in folder or not folder
                    lines = [(f"{wid} {row['name']}", 15, INK), (row.get("question", ""), 12, INK2),
                             ("Discovery · " + ("not opened" if dashed else folder.split(":")[-1].strip(" `")), 12, INK3)]
                extra, stroke = self.rv.lines([wid])
                h = card(c, XA, ay, WA, lines + extra, dashed=dashed, stroke=stroke or INK)
                self.at[wid] = (XA, ay, WA, h)
                a_edges.append((XA + WA, ay + h / 2, dashed))
                ay += h + 10
            cy, c_mids, c_dash = y, [], []
            claims = {cl["code"]: cl for cl in q["claims"]}
            for hy in q["hyp"]:
                states = [(e, t.E.get(e, "?")) for e in hy["tested"]]
                dashed = all(s == "absent" for _, s in states)
                tested = "tested by " + " · ".join(f"{e} {s}" for e, s in states)
                cl = claims.get(hy["code"])
                lines = [(f"Q{hy['code']}  {hy['name']}", 15, INK), ("guess: " + hy["what"], 12, INK2)]
                keys = [f"Q{hy['code']}"]
                if cl:
                    now = re.split(r"(?<=[.;])\s", cl.get("now", ""))[0].rstrip(".;")
                    lines += [(f"{cl['c']} · {cl['name']}", 15, INK3 if dashed else ACC),
                              (cl.get("role", "").rstrip("."), 12, INK2), (tested, 12, INK3)]
                    if now:
                        lines.append(("now: " + now, 12, INK3))
                    keys.append(cl["c"])
                else:
                    lines += [("no claim of its own", 13, INK2), (tested, 12, INK3)]
                    dashed = True
                extra, stroke = self.rv.lines(keys)
                h = card(c, XC, cy, WC, lines + extra, dashed=dashed, stroke=stroke or ACC)
                c_mids.append(cy + h / 2)
                c_dash.append(dashed)
                cy += h + 10
            contrib = q["contrib"][0] if q["contrib"] else "none yet"
            lines = [(spec.get("figures", {}).get(q["n"], "no display named yet"), 15, INK), (q.get("section", ""), 13, INK2),
                     ("a reader gains: " + contrib, 12, INK2), (spec.get("figures_state", "drawn by its display script"), 12, INK3)]
            extra, stroke = self.rv.lines([f"Q{q['n']}"])
            fh = card(c, XF, y, WF, lines + extra, dashed=True, stroke=stroke or INK)
            f_mid = y + fh / 2
            bracket(c, XA + WA + 30, [(ex, ey) for ex, ey, _ in a_edges], [(XC, m) for m in c_mids],
                    [i for i, d in enumerate(c_dash) if d])
            bracket(c, XC + WC + 30, [(XC + WC, m) for m in c_mids], [(XF, f_mid)], [0] if all(c_dash) else [])
            bottom = max(ay - 10, cy - 10, y + fh)
            c.rect(XA - 16, gtop - 8, RIGHT - XA + 32, bottom - gtop + 22, stroke=INK3, sw=1, style="dashed",
                   fill="transparent")
            feed = self.at.get(spec.get("feeds", {}).get(q["n"], ""))
            if a_edges and feed:
                bus = XT + WT + 22 + 10 * q["n"]
                fy = feed[1] + min(40, feed[3] / 2)
                c.line([(XT + WT, fy), (bus, fy), (bus, a_edges[0][1]), (XA - 2, a_edges[0][1])],
                       stroke=INK3, sw=1, style="dashed", arrow=True)
            y = bottom + 44
        return y

    def draw(self, review_pages):
        t, c, spec = self.t, self.c, self.spec
        c.text(30, 18, spec["title"], 30, INK)
        c.text(30, 62, spec["sub"], 15, INK3)
        c.text(30, 92, "the question:  " + t.call, 15, INK2)
        top = 136
        if self.rv.items:
            rel = " · ".join(str(p.relative_to(t.board)) for p in review_pages)
            c.text(30, top, f"❗ red: what the reviewers asked us to change   🛠 green: the work that fixes it   "
                            f"({len(self.rv.items)} Review Items, from {rel})", 16, INK)
            top += 34
        foundation = {i.get("task") for col in spec["foundation"].values() for i in col}
        work = sorted({w["id"] for q in t.qs for w in q["work"] if w["id"] not in foundation},
                      key=lambda w: (w[0] == "D", int(w[1:])))
        claims = sorted({cl["c"] for q in t.qs for cl in q["claims"]}, key=lambda x: int(x[1:]))
        fill = {"analysis": " ".join(work), "questions": len(t.qs), "subq": sum(len(q["hyp"]) for q in t.qs),
                "claims": f"{claims[0]}-{claims[-1]}" if claims else "no claim"}
        boxes = [(k, title, str(l1).format(**fill), str(l2).format(**fill)) for k, title, l1, l2 in spec["overview"]]
        oh = overview(c, boxes, top)
        c.line([(30, top + oh), (RIGHT, top + oh)], stroke=INK3, sw=1)
        y0 = top + oh - 116
        for k, (title, sub) in spec["columns"].items():
            x, _ = COLS[k]
            c.text(x, y0 + 136, title, 17, ACC if k == "C" else INK)
            c.text(x, y0 + 160, sub, 13, INK3)
        c.line([(30, y0 + 184), (RIGHT, y0 + 184)], stroke=RULE, sw=1)
        T = y0 + 196
        bottoms = [self.column(k, T) for k in ("D", "S", "T")]
        self.links(max(bottoms))
        y = self.rows(T)
        fy = max(max(bottoms) + 60, y - 20) + 34
        c.line([(30, fy - 12), (RIGHT, fy - 12)], stroke=RULE, sw=1)
        notes = list(spec.get("notes", []))
        writing, open_ = self.rv.leftovers()
        k = 0
        for s in notes:
            c.text(30, fy + 22 * k, s, 14, INK2 if k == 0 else INK3)
            k += 1
        if writing:
            c.text(30, fy + 22 * k + 8, "🛠 fixed in the writing, not on a card: " + " · ".join(
                f"{label(x)} → {', '.join(stems)}" for x, stems in writing), 14, GREEN)
            k += 1
        if open_:
            c.text(30, fy + 22 * k + 8, "❓ nothing fixes yet: " + " · ".join(label(x) for x, _ in open_), 14, RED)
        return c.els


def count_line(spec, root):
    """A grey line counted from a JSON file on disk, on every build (a number is never typed): `{json: <path from the
    SPACE root>, list: <key>, where: {<field>: <value>}, say: "… {n} … {<field of the first match>}", none: "…"}`."""
    p = root / spec["json"]
    data = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    rows = data.get(spec.get("list", ""), []) if isinstance(data, dict) else data
    hit = [r for r in rows if all(str(r.get(k)) == str(v) for k, v in (spec.get("where") or {}).items())]
    if not hit:
        return spec.get("none", f"none in {p.name}")
    return spec.get("say", "{n} in " + p.name).format(n=len(hit), **{k: v for k, v in hit[0].items() if isinstance(v, str)})


def words_of(topic):
    f = Path(topic) / f"{Path(topic).name}-drawing.yaml"
    if not f.is_file():
        raise SystemExit(f"{f.name} not found in {topic}; run: workflow_drawing.py make {topic}")
    return yaml.safe_load(f.read_text(encoding="utf-8")) or {}


def resolve_counts(spec, root):
    """Every card's `count:` becomes its grey line, read now."""
    for col in (spec.get("foundation") or {}).values():
        for item in col:
            for x in [item] + list(item.get("group", [])):
                if x.get("count"):
                    x["gray"] = count_line(x["count"], root)
    return spec


def draw(topic, out=None):
    """Redraw one workflow topic from its `<topic>-drawing.yaml`; what its builder calls."""
    topic = Path(topic).resolve()
    board = up(topic, "board.md")
    root = space_root(topic)
    spec = resolve_counts(words_of(topic), root)
    telling = Telling(board)
    items, pages = review_items(board, spec.get("review"))
    m = Map(telling, spec, Review(items))
    els = m.draw(pages)
    out = Path(out) if out else topic / f"{topic.name}.excalidraw"
    builder = next(iter(sorted(topic.glob("build_*.py"))), None)
    canvas.write(out, els, builder.name if builder else Path(__file__).name, palette=False)
    rel = out.relative_to(root) if out.is_relative_to(root) else out
    print(f"{len(els)} elements · {len(telling.qs)} questions · {len(items)} Review Items "
          f"({len({i for i, _ in m.rv.drawn})} on cards) -> {rel}")
    return out


# ── a topic's builder and words ───────────────────────────────────────────────────────────────────────────────
SKILLS = HERE.parents[3]                                   # .../skills


def scripts_from(topic):
    """This folder, relative to the topic: through the SPACE's Tools link, or inside the Tools SPACE itself."""
    here_rel = HERE.relative_to(SKILLS.parents[2])         # plugins/haipipe-toolkit/skills/1_base/display/...
    for p in (topic, *topic.parents):
        for base in (p / "Tools", p):
            if (base / here_rel).is_dir():
                return Path(os.path.relpath(base / here_rel, topic)).as_posix()
    return str(HERE)


def builder_text(topic, script):
    return (f'"""{topic.name}: the building map, drawn by excalidraw-workflow\'s workflow_drawing.py from '
            f"{topic.name}-drawing.yaml, the telling, the Board Questions' reports and the newest version's Review "
            "Items; a person's marks on the drawing are kept.\n\n"
            f'    python {script}\n"""\n'
            "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
            f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
            "import workflow_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    workflow_drawing.draw(HERE)\n")


TEMPLATE = """# The words of {name}'s building map (excalidraw-workflow). Edit here, then run its builder.
# Everything else is read on every build: the telling (board.md story-current:), the Board Questions' reports,
# the Task folders, and the newest version's comments report (its Review Items' hits and fixed by).
title: "The paper: from the data to the answer"
sub: "names read from the telling and the Board Questions' reports · solid = exists on disk · dashed = not run"
columns:
  D: ["THE DATA", "what every question reads · T1"]
  S: ["THE SOURCES", "what the study builds from the data"]
  T: ["THE TESTS", "what checks it"]
  A: ["ANALYSIS", "the work each sub-question needs"]
  C: ["SUB-QUESTION → CLAIM", "the guess, and what the paper would say if it holds"]
  F: ["IN THE PAPER", "where each answer lands"]
foundation:
  D:
  - {{key: data, title: "The data", lines: ["what it holds"], gray: "where it lives"}}
  S:
  - {{key: method, title: "How the study works", tasks_of: 1}}
  T:
  - {{key: test, title: "The test", lines: ["what it checks"], gray: "not run", dashed: true}}
links:
- {{from: data, to: method}}
feeds: {{1: test}}
figures: {{1: "Figure 2 (proposed)"}}
figures_state: "drawn by its display script"
overview:
- [D, "THE DATA", "what it holds", "T1"]
- [S, "THE SOURCES", "what is built", "T2"]
- [T, "THE TESTS", "what checks it", "T3"]
- [A, "ANALYSIS", "the work each sub-question needs", "{{analysis}}"]
- [C, "SUB-QUESTION → CLAIM", "{{questions}} questions · {{subq}} sub-questions", "{{claims}}"]
- [F, "IN THE PAPER", "Results, Discussion", "one script per display"]
notes: []
"""


def make(topic, force=False):
    """The topic's forwarding builder, and a words yaml from the template when it has none."""
    topic = Path(topic).resolve()
    if not topic.is_dir():
        raise SystemExit(f"{topic} is not a folder; make the topic first (haipipe-studio new_topic.py)")
    m = re.match(r"s(\d\d)-(.+)$", topic.name)
    builder = topic / (f"build_s{m.group(1)}_{m.group(2).replace('-', '_')}.py" if m else "build.py")
    if builder.exists() and not force:
        raise SystemExit(f"{builder.name} exists; --force replaces it (keep a copy in history/ first)")
    builder.write_text(builder_text(topic, builder.name), encoding="utf-8")
    words = topic / f"{topic.name}-drawing.yaml"
    if not words.exists():
        words.write_text(TEMPLATE.format(name=topic.name), encoding="utf-8")
    return builder


def main(argv=None):
    ap = argparse.ArgumentParser(description="a study's building map, with the review overlay (excalidraw-workflow)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one workflow topic").add_argument("topic", type=Path)
    mk = sub.add_parser("make", help="the topic's forwarding builder, and a words yaml if none")
    mk.add_argument("topic", type=Path)
    mk.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    print(draw(a.topic) if a.cmd == "draw" else make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
