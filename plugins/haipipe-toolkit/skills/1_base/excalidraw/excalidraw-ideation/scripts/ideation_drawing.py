"""An ideation as one drawing: every idea as a step down from the question, and small frames that explain it.

Asked 261013 on Physician-SPACE's Paper-LLMRecPhy-Quick s01-ideation, whose first drawing (19 equal frames in left-aligned
rows) was the counterexample: "主次分明 … 一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame 的 … 一定要用阶梯状
的结构 … 不能变成一个跟棋盘一样的东西 … 你不能每一个都是朝左对齐". Lifted here 261014 from that topic's builder so every
paper's s01-ideation draws the same way (JL 261014: "How do you think we can add it to the themes/paper skills set").

    python ideation_drawing.py draw <topic folder>                 redraw one (what the topic's builder calls)
    python ideation_drawing.py make <topic folder> [--force]       the forwarding builder, and a words yaml if none

    ① 🪜 every idea as steps (main, large)                ② the setting, in its real numbers (small)
       the question                                         ③ 🔥 the lead group's first idea (small)
        └─▶ 🔥 the lead group ─ one box per idea ───────────▶    ④ 🔥 its second … one card each
             └─▶ the next group ─ names only                         ⑤ …
                  └─▶ … down to on hold, or far
          ⑦ from here to G0 (small, below): steps, each with what "done" means, then the person's choice
       ⑧ how it scores and where it goes (optional, a step lower): the tests' verdicts, the venues as stairs

Every word is the topic's `<topic>-drawing.yaml` (excalidraw-ideation's SKILL.md has its keys). An idea card reads its
state line from the yaml (`state:`) or, when `state: {columns: …}` is set, from the face's Ideas (ranked) table on every
build. The writer is haipipe-studio's canvas.write, so a person's marks survive a rebuild.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SKILLS = HERE.parents[3]                                   # .../skills
sys.path.insert(0, str(HERE.parents[1] / "excalidraw-studio" / "scripts"))
from draw import GREY, INK, RED, Drawing, canvas  # noqa: E402

PAD = 22
SHIFT, GROUP_W, IDEA_W, STEP_GAP = 460, 820, 960, 170
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"


# ── what the drawing reads ─────────────────────────────────────────────────────────────────────────────────
def words_of(topic: Path) -> dict:
    f = topic / f"{topic.name}-drawing.yaml"
    if not f.is_file():
        raise SystemExit(f"{f.name} not found in {topic}; run: ideation_drawing.py make {topic}")
    return yaml.safe_load(f.read_text(encoding="utf-8")) or {}


def table(text: str, first: str) -> list:
    """Rows of the face's tables whose first cell matches `first` (a regex), as lists of cells."""
    rows = []
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and re.fullmatch(first, cells[0]):
                rows.append(cells)
    return rows


def word(cell: str) -> str:
    """A state cell in words: "🔶 partial (cross-model check)" -> "partial"; "➖ none claimed" -> "none claimed"."""
    parts = re.sub(r"[➖🔶⬜❗✅🟢🟡🔴⚠️]", "", cell).split()
    if not parts:
        return ""
    return " ".join(parts[:2]).lower() if parts[0].lower() in ("none", "basis") else parts[0].lower()


def states(topic: Path, w: dict) -> dict:
    """iNN -> its state line: the idea's own `state:`, else the face's Ideas table by `state.columns`."""
    out = {k: str(v["state"]) for k, v in (w.get("ideas") or {}).items() if isinstance(v, dict) and v.get("state")}
    cols = (w.get("state") or {}).get("columns") or {}
    face = topic / f"{topic.name}.md"
    if cols and face.is_file():
        for c in table(face.read_text(encoding="utf-8"), r"i\d+"):
            if c[0] not in out:
                out[c[0]] = " · ".join(f"{name}: {(word(c[i]) if i < len(c) else '') or '—'}" for name, i in cols.items())
    return out


# ── shared pieces ──────────────────────────────────────────────────────────────────────────────────────────
def box(d, x, y, w, lines, sw=1.5, dashed=False):
    """A box of lines [(words, size, colour)]; returns its height."""
    h = sum(Drawing.height(s, w - 2 * PAD, size) + 6 for s, size, _ in lines if s) + 2 * PAD - 6
    d.box(x, y, w, h, GREY if dashed else INK, sw, dashed=dashed)
    yy = y + PAD
    for s, size, color in lines:
        if s:
            yy = d.para(x + PAD, yy, s, w - 2 * PAD, size, color) + 6
    return h


def finish(d, f, bottom, least=0, small=True):
    f["height"] = max(bottom + 40, least)
    if small:
        canvas.explains(f)                          # small on purpose: it explains the main frame
    if f["height"] > canvas.FRAME_MAX[1]:
        canvas.reads_down(f)
    d.fid = f["id"]
    if not small:                                   # a small frame carries no check badge: its words are the point
        d.badge(f)
    return f


def move(els, f, x, y):
    """Put frame `f` and what is drawn in it at (x, y)."""
    dx, dy = x - f["x"], y - f["y"]
    for e in els:
        if e["id"] == f["id"] or e.get("frameId") == f["id"]:
            e["x"], e["y"] = e["x"] + dx, e["y"] + dy


def red(s) -> bool:
    return str(s).lstrip().startswith(("❗", "❓"))


# ── ① the main frame: every idea as steps ─────────────────────────────────────────────────────────────────
def main_frame(d, ix, groups, ideas):
    width = 140 + (len(groups) - 1) * SHIFT + GROUP_W + 100 + IDEA_W + 60
    heading = ix.get("heading") or ix.get("title", "🪜 The ideas")
    f = d.frame(ix.get("frame") or f"① {heading}", width)
    Drawing.room(f)
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    d.text(40, 22, heading, 64)
    d.para(40, 112, ix.get("sub", ""), width - 80, 26, GREY)
    y = 180
    kh = Drawing.height(ix["key"], width - 140, 34) + 44
    d.key(40, y, width - 80, kh)
    d.para(70, y + 22, ix["key"], width - 140, 34)
    y += kh + 80
    qw = min(1500, width - 80)
    qh = box(d, 40, y, qw, [(ix["question"], 46, INK)], sw=3)
    question = {"right": 40 + qw, "mid": y + qh / 2}
    spine_x, spine_top = 70, y + qh
    y += qh + STEP_GAP
    first, mids = {}, []
    for i, g in enumerate(groups):
        gx = 140 + i * SHIFT
        lead = i == 0
        gh = box(d, gx, y, GROUP_W, [(g["name"], 38, INK)], sw=2.5)
        d.para(gx + 36, y + gh + 12, g.get("line", ""), GROUP_W - 60, 26, GREY)
        mid = y + gh / 2
        mids.append(mid)
        d.line([(spine_x, mid), (gx - 8, mid)], sw=3)
        # its ideas branch to the right: the lead group in full weight, the rest as names
        ix_, iy, ends = gx + GROUP_W + 100, y + gh + 24, []
        for k in g["ideas"]:
            w = ideas.get(k) or {}
            hold = red(w.get("now", ""))
            label = f"{'🔥 ' if lead else '❗ ' if hold else ''}{k} · {w.get('short', k)}"
            h = box(d, ix_, iy, IDEA_W, [(label, 30 if lead else 26, INK)], sw=2.5 if lead else 1.2, dashed=hold)
            ends.append(iy + h / 2)
            if lead:
                first[k] = {"right": ix_ + IDEA_W, "mid": iy + h / 2}
            iy += h + 16
        bx = gx + GROUP_W - 60
        if ends:
            d.line([(bx, y + gh), (bx, ends[-1])], arrow=False, sw=1.5)
        for e in ends:
            d.line([(bx, e), (ix_ - 8, e)], sw=1.5)
        y = max(y + gh + 60, iy) + STEP_GAP
    d.line([(spine_x, spine_top), (spine_x, mids[-1])], arrow=False, sw=3)
    said = sum(Drawing.words_in(e.get("text", "")) for e in d.els if e.get("frameId") == f["id"] and e["type"] == "text")
    if said > 200:
        Drawing.detail(f)
    return finish(d, f, y - STEP_GAP + 40, small=False), question, first


# ── ② the setting, small ───────────────────────────────────────────────────────────────────────────────────
def flow_of(r: dict) -> str:
    if r.get("flow"):
        return " → ".join(r["flow"])
    keys = [r.get("start"), r.get("roster"), " · ".join(x for x in ((r.get("google") or [""])[0], (r.get("agent") or ["", ""])[1]) if x),
            r.get("end")]                                                   # the older keys (Paper-LLMRecPhy-Quick)
    return " → ".join(k for k in keys if k)


def setting_frame(d, r, n):
    W = 1600
    title = re.sub(r"^[①-⑩]\s*", "", r["title"])
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    y = d.para(40, 90, r.get("sub", ""), W - 80, 22, GREY) + 24
    kh = Drawing.height(r["key"], W - 140, 30) + 40
    d.key(40, y, W - 80, kh)
    d.para(70, y + 20, r["key"], W - 140, 30)
    y += kh + 40
    flow = flow_of(r)
    if flow:
        y = d.para(40, y, flow, W - 80, 26) + 50
    for i, num in enumerate((r.get("numbers") or [])[: int(r.get("show", 3))]):   # hero numbers, as steps
        x = 40 + i * 160
        d.text(x, y, num["big"], 52, RED if red(num["big"]) else INK)
        y = d.para(x, y + 72, num["tag"], W - 120 - i * 160, 24) + 30
    if r.get("reading"):
        y = d.para(40, y + 10, r["reading"], W - 80, 24, GREY) + 10
    return finish(d, f, y)


# ── ③ on: the lead group, one small card each ─────────────────────────────────────────────────────────────
def idea_card(d, n, k, w, state):
    W = 1500
    f = d.frame(f"{CIRCLED[n]} 🔥 {k} · {w['short']}", W)
    y = d.para(40, 22, f"🔥 {k} · {w['short']}", W - 80, 40) + 6
    if state:
        y = d.para(40, y, state, W - 80, 22, GREY) + 24
    else:
        y += 18
    why = f"Why it matters: {w['why']}"
    kh = Drawing.height(why, W - 140, 26) + 36
    d.key(40, y, W - 80, kh)
    y = d.para(70, y + 18, why, W - 140, 26) + 18 + 28
    if w.get("does"):                                               # the design in one line, when the face has one
        y = d.para(40, y - 10, f"Does: {w['does']}", W - 80, 26) + 24
    if w.get("closest") or w.get("new"):                            # its novelty check: the closest work, what stays new
        y -= 10
        for label, k in (("Closest", "closest"), ("New", "new")):
            if w.get(k):
                y = d.para(40, y, f"{label}: {w[k]}", W - 80, 26) + 8
        y += 16
    d.text(40, y, "If we find → it would mean", 24, GREY)
    y += 44
    for res in (w.get("results") or [])[:3]:
        y = d.para(60, y, f"· {res['find']} → {res['means']}", W - 100, 26) + 10
    if w.get("now"):
        y = d.para(40, y + 18, f"Now: {w['now']}", W - 80, 26, RED if red(w["now"]) else None) + 6
    return finish(d, f, y)


# ── the last frame: from here to G0, small ─────────────────────────────────────────────────────────────────
def path_frame(d, p, n):
    W = 2100
    title = re.sub(r"^[①-⑲]\s*", "", p["title"])
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    y = 100
    kh = Drawing.height(p["key"], W - 140, 30) + 40
    d.key(40, y, W - 80, kh)
    d.para(70, y + 20, p["key"], W - 140, 30)
    y += kh + 50
    prev, bottom = None, y
    for i, s in enumerate(p["steps"]):                              # each step lower and further right
        x, yy = 40 + i * 400, y + i * 70
        last = i == len(p["steps"]) - 1
        h = box(d, x, yy, 360, [(s["title"], 26, RED if red(s["title"]) else INK),
                                ((s.get("lines") or [""])[-1], 22, GREY)], sw=2.5 if last else 1.5)
        if prev:
            d.line([(prev[0] + 360 + 6, prev[1] + 30), (x - 6, yy + 30)], sw=2)
        prev, bottom = (x, yy), max(bottom, yy + h)
    y = bottom + 40
    for ln in p.get("open", []):
        y = d.para(40, y, ln, W - 80, 24, RED if red(ln) else None) + 8
    return finish(d, f, y)


# ── optional, below the path: how the lead idea scores and where it goes ──────────────────────────────────
def evaluation_frame(d, e, n):
    """The tests that read the lead idea (novelty, pressure, journal fit, a Nature lens), each with its verdict and
    who ran it, then the venues from ambitious to fallback as stairs. A test not run yet, or a venue still open, is
    red: its verdict or name starts with ❓ or ⬜."""
    W = 2100
    title = re.sub(r"^[①-⑲]\s*", "", e["title"])
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    y = d.para(40, 90, e.get("sub", ""), W - 80, 22, GREY) + 24
    kh = Drawing.height(e["key"], W - 140, 30) + 40
    d.key(40, y, W - 80, kh)
    d.para(70, y + 20, e["key"], W - 140, 30)
    y += kh + 44
    d.text(40, y, e.get("checks_title", "The tests, and what each found"), 26, GREY)
    y += 46
    cw, gap = (W - 80 - 40) / 2, 40                                 # two tests a row, read left to right
    for r in range(0, len(e.get("checks") or []), 2):
        hs = []
        for k, c in enumerate(e["checks"][r:r + 2]):
            open_ = str(c.get("verdict", "")).lstrip().startswith(("❓", "⬜"))
            lines = [(f"{c['name']} · {c.get('verdict', '')}", 28, RED if open_ else INK),
                     (c.get("by", ""), 22, GREY), (c.get("note", ""), 24, INK)]
            hs.append(box(d, 40 + k * (cw + gap), y, cw, lines, sw=1.5, dashed=open_))
        y += max(hs) + 24
    y += 20
    d.text(40, y, e.get("venues_title", "Where it goes: ambitious to fallback"), 26, GREY)
    y += 46
    prev, bottom, yy = None, y, y
    for i, v in enumerate(e.get("venues") or []):                   # each venue a step lower and further right
        x = 40 + i * 420
        open_ = red(v["name"])
        lines = [(v["name"], 28, RED if open_ else INK), (v.get("fit", ""), 24, INK), (v.get("rules", ""), 22, GREY)]
        h = box(d, x, yy, 900, lines, sw=2.5 if i == 0 else 1.5, dashed=open_)
        if prev:
            d.line([(prev[0] + 120, prev[1] + prev[2]), (prev[0] + 120, yy + 30), (x - 6, yy + 30)], sw=2)
            d.text(prev[0] + 140, prev[1] + prev[2] + 10, e.get("venue_arrow", "if not"), 22, GREY)
        prev, bottom = (x, yy, h), max(bottom, yy + h)
        yy += h + 60                                                # the next step starts below this one
    y = bottom + 40
    for ln in e.get("open", []):
        y = d.para(40, y, ln, W - 80, 24, RED if red(ln) else None) + 8
    return finish(d, f, y)


# ── the drawing ────────────────────────────────────────────────────────────────────────────────────────────
def draw(topic: Path, out: Path | None = None) -> Path:
    topic = Path(topic).resolve()
    w = words_of(topic)
    ideas, groups = w.get("ideas") or {}, w["groups"]
    ix = w.get("index") or {}
    if not ix.get("question"):
        raise SystemExit(f"{topic.name}-drawing.yaml: index.question is missing (the root of the steps)")
    st = states(topic, w)
    d = Drawing()
    big, question, first = main_frame(d, ix, groups, ideas)
    setting = setting_frame(d, w.get("setting") or w["roster"], 1)
    lead = [k for k in groups[0]["ideas"] if k in ideas]
    cards = [idea_card(d, 2 + i, k, ideas[k], st.get(k, "")) for i, k in enumerate(lead)]
    path = path_frame(d, w["path"], 2 + len(cards))
    ev = evaluation_frame(d, w["evaluation"], 3 + len(cards)) if w.get("evaluation") else None
    # the main frame at the origin; the small ones step down and to its right; G0 below it, set in
    move(d.els, big, 0, 0)
    sx = big["width"] + 360
    move(d.els, setting, sx, 0)
    y = setting["height"] + 220
    for i, c in enumerate(cards):
        move(d.els, c, sx + 260 + i * 200, y)
        y += c["height"] + 200
    move(d.els, path, 760, big["height"] + 320)
    d.fid = None
    # the setting explains the question; each lead card explains its idea; the path follows the steps
    sy = setting["y"] + 120
    d.line([(question["right"] + 10, question["mid"]), (sx - 160, question["mid"]), (sx - 160, sy), (sx - 14, sy)], sw=3)
    d.text(question["right"] + 30, question["mid"] - 52, ix.get("link", "the setting"), 32)
    for i, (k, c) in enumerate(zip(lead, cards)):
        at, cy, ex = first[k], c["y"] + 50, big["width"] + 80 + i * 50
        d.line([(at["right"] + 10, at["mid"]), (ex, at["mid"]), (ex, cy), (c["x"] - 14, cy)], sw=2)
    px = path["x"] + 300
    d.line([(px, big["height"] + 14), (px, path["y"] - 14)], sw=5)
    d.text(px + 20, big["height"] + 130, w["path"].get("arrow", "then G0"), 36)
    if ev:                                                          # what G0 reads: a step below the path, to its right
        move(d.els, ev, path["x"] + 420, path["y"] + path["height"] + 240)
        d.fid = None
        ex = ev["x"] + 300
        d.line([(ex, path["y"] + path["height"] + 14), (ex, ev["y"] - 14)], sw=4)
        d.text(ex + 20, path["y"] + path["height"] + 80, w["evaluation"].get("arrow", "G0 reads"), 32)
    builder = next(iter(sorted(topic.glob("build_*.py"))), None)
    out = out or topic / f"{topic.name}.excalidraw"
    d.write(out, builder.name if builder else Path(__file__).name)
    return out


# ── a topic's builder and words ────────────────────────────────────────────────────────────────────────────
def rel(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def scripts_from(topic: Path) -> str:
    """This folder, relative to the topic: through the SPACE's Tools link, or inside the Tools SPACE itself."""
    here_rel = HERE.relative_to(SKILLS.parents[2])          # plugins/haipipe-toolkit/skills/1_base/display/...
    for p in (topic, *topic.parents):
        for base in (p / "Tools", p):
            if (base / here_rel).is_dir():
                return rel(base / here_rel, topic)
    return str(HERE)


def builder_text(topic: Path, script: str) -> str:
    return (f'"""{topic.name}: drawn by excalidraw-ideation\'s ideation_drawing.py from {topic.name}-drawing.yaml '
            "(and the face's Ideas table, when the yaml asks); a person's marks on the drawing are kept.\n\n"
            f'    python {script}\n"""\n'
            "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
            f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
            "import ideation_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    ideation_drawing.draw(HERE)\n")


TEMPLATE = """# The words of {name}'s drawing (excalidraw-ideation). Edit here, then run its builder.
index:
  heading: "🪜 N ideas, from the lead group to on hold"
  sub: "the lead group has a card each, to the right; the others keep their words in the face; none is selected"
  key: "🔥 The lead group in one sentence."
  question: "The paper's question, in one line?"
setting:
  title: "The setting, in its real numbers"
  sub: "what each word below means"
  key: "The question the setting asks."
  flow: ["🔑 what goes in", "⚙️ what happens", "👥 what comes out"]
  numbers:
  - {{big: "❓", tag: "a number already on disk, and where it was read"}}
  reading: ""
groups:
- {{name: "🔥 The lead group", line: "why these come first", ideas: [i01]}}
- {{name: "On hold, or far", line: "why they wait", ideas: []}}
ideas:
  i01:
    short: "A short question?"
    why: "Why it matters, in one or two sentences."
    results:
    - {{find: "what we might find", means: "what it would mean"}}
    now: "⬜ where it stands today"
    state: "novelty: ⬜ · pilot: ⬜"
path:
  title: "From here to G0"
  key: "The steps, then the person's G0 choice."
  steps:
  - {{title: "a step", lines: ["done when: …"]}}
  - {{title: "🙋 G0", lines: ["the person's choice"]}}
  open: []
"""


def make(topic: Path, force: bool = False) -> Path:
    topic = Path(topic).resolve()
    if not topic.is_dir():
        raise SystemExit(f"{topic} is not a folder; make the topic first (haipipe-studio new_topic.py)")
    m = re.match(r"s(\d\d)-(.+)$", topic.name)
    builder = topic / (f"build_s{m.group(1)}_{m.group(2).replace('-', '_')}.py" if m else "build.py")
    if builder.exists() and not force:
        raise SystemExit(f"{builder.name} exists; --force replaces it (keep a copy first if it holds drawing code)")
    builder.write_text(builder_text(topic, builder.name), encoding="utf-8")
    words = topic / f"{topic.name}-drawing.yaml"
    if not words.exists():
        words.write_text(TEMPLATE.format(name=topic.name), encoding="utf-8")
    return builder


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one ideation topic").add_argument("topic", type=Path)
    m = sub.add_parser("make", help="the topic's forwarding builder, and a words yaml if none")
    m.add_argument("topic", type=Path)
    m.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    if a.cmd == "draw":
        print(draw(a.topic))
    else:
        print(make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
