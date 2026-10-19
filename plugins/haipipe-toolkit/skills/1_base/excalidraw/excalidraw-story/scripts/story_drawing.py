"""A paper's story as one drawing: its research questions as steps, each with what supports it and what is missing.

Asked 261019 on Physician-SPACE's Paper-LLMRecPhy (JL: "In the story studio s02-story, I think we might need to list
the research questions, and how could we support them"; "should we have a things named /excalidraw-story?"; "This
is more like the story, do you get it."). Drawn the way excalidraw-ideation draws s01 (one big main frame, small
frames that explain it, as stairs; JL 261013), and read from the telling's face on every build, so the drawing can
never say what the story does not.

    python story_drawing.py draw <studio/sNN-story-<desk>-<idea>>     redraw one (what the topic's builder calls)
    python story_drawing.py make <studio/sNN-story-<desk>-<idea>>     its forwarding builder

    ① 📖 the questions as steps (main)                 ② the pitch (small)
       the paper's question                               ③ what we will not claim
        └─▶ ✅ RQ0 · name ─▶ answer now · its claim · E rows · T rows
             └─▶ 🔶 RQ1 · name ─▶ …
                  └─▶ ⬜ RQ2 · name ─▶ … (red, dashed: nothing supports it yet)
          ④ from here to the send (small, below): each Run still to make, who starts it, then G0

What it reads from the face (haipipe-paper-story's contract): the title line; `**The paper's question**:`; `**G0:**`;
`**The story, question by question**`, the questions in reading order, which title the steps (JL 261019: "the
quesiton can be the narrative as well");
§2's numbered Pitch; §3's `#### 3.N · Question N · RQn` blocks (Name, Question, Answer state, Hypotheses with their
E rows, Potential claims with Now, Potential work with their T and D rows); §5's E table (`support state`) and its
`**We will not claim**:` list; §7's T table (`state`, `starts`). A state is the first mark of its line: ✅ answered,
🔶 partly, ⬜ missing (red), ❗ contradicted (red). The writer is haipipe-studio's canvas.write, so a person's marks
survive a rebuild.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILLS = next(p for p in HERE.parents if p.name == "skills")
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-studio/scripts"))
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-ideation/scripts"))
from draw import GREY, INK, RED, Drawing, canvas  # noqa: E402
from ideation_drawing import box, finish, move  # noqa: E402   one look with s01: a box of lines, a small frame

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
SHIFT, RQ_W, CARD_W, STEP_GAP = 260, 760, 1180, 140
MARK = {"established": "✅", "provisional": "🔶", "absent": "⬜", "contradicted": "❗", "gated": "⬜",
        "done": "✅", "ticket next": "⬜", "not started": "⬜"}


# ── what the drawing reads ─────────────────────────────────────────────────────────────────────────────────
def mark(s: str) -> str:
    """The state mark a line starts with, else ''."""
    m = re.match(r"\s*(✅|🔶|⬜|❗)", str(s))
    return m.group(1) if m else ""


def missing(s: str) -> bool:
    return mark(s) in ("⬜", "❗")


def unmark(s: str) -> str:
    return re.sub(r"^\s*(✅|🔶|⬜|❗)\s*", "", str(s))


def table(lines: list[str], first: str) -> list[dict]:
    """The Markdown table whose header starts with `| first |`, one dict per row."""
    for i, ln in enumerate(lines):
        if ln.startswith(f"| {first} |"):
            head = [h.strip().lower() for h in ln.strip().strip("|").split("|")]
            rows = []
            for row in lines[i + 2:]:
                if not row.startswith("|"):
                    break
                rows.append(dict(zip(head, [c.strip() for c in row.strip().strip("|").split("|")])))
            return rows
    return []


def section(lines: list[str], head: str) -> list[str]:
    """The lines under a `### N · head` heading, to the next `### `."""
    out, on = [], False
    for ln in lines:
        if ln.startswith("### "):
            on = re.sub(r"^###\s+\d+\s*·\s*", "", ln).strip().lower().startswith(head.lower())
            continue
        if on:
            out.append(ln)
    return out


def items(lines: list[str], start: str) -> list[str]:
    """The list under the first line starting with `start`: `- x` or `1. x`, wrapped lines joined."""
    out, on = [], not start                          # no start line: the list starts at once
    for ln in lines:
        if start and ln.startswith(start):
            on = True
            continue
        if not on:
            continue
        m = re.match(r"^(?:-|\d+\.)\s+(.*)$", ln)
        if m:
            out.append(m.group(1).strip())
        elif ln.startswith("  ") and out:
            out[-1] += " " + ln.strip()
        elif ln.strip():
            break
        elif out:
            break
    return out


def plain(s: str) -> str:
    """Markdown marks off; a ⟦pending E4⟧ mark as (pending E4), which the drawing's font can show."""
    s = re.sub(r"⟦([^⟧]*)⟧", r"(\1)", s)
    return re.sub(r"\*\*(.+?)\*\*", r"\1", re.sub(r"`([^`]*)`", r"\1", s)).strip()


def questions(lines: list[str]) -> list[dict]:
    """Every `#### 3.N · Question N · RQn` block: its fields, hypotheses, claims and work (a claim's `from` may name
    several hypotheses: `from 1a, 1b`)."""
    qs, cur, part = [], None, None
    for ln in lines:
        m = re.match(r"^#### 3\.\d+ · Question (\d+) · (RQ\d+)", ln)
        if m:
            cur = {"n": int(m[1]), "rq": m[2], "hyp": [], "claims": [], "work": []}
            qs.append(cur)
            part = None
            continue
        if ln.startswith(("### ", "#### ")):
            cur = None
            continue
        if cur is None:
            continue
        m = re.match(r"^- \*\*(Name|Question|Answer state|Section)\*\*: (.*)$", ln)
        if m:
            cur[m[1].lower()] = plain(m[2])
            continue
        m = re.match(r"^\*\*(Hypotheses|Potential claims|Potential contributions|Potential work)\*\*$", ln.strip())
        if m:
            part = m[1]
            continue
        if part == "Hypotheses":
            m = re.match(r"^- \*\*(\w+)\*\* · (.+?) · tested by (.+)$", ln)
            if m:
                name, _, what = m[2].partition(": ")
                cur["hyp"].append({"code": m[1], "name": name, "what": what, "tested": re.findall(r"E\d+", m[3])})
        elif part == "Potential claims":
            m = re.match(r"^- \*\*(\w+)\*\* · (C\d+) · from [^·]+? · (.+)$", ln)
            if m:
                name, _, what = m[3].partition(": ")
                cur["claims"].append({"code": m[1], "c": m[2], "name": name, "what": what})
            m = re.match(r"^\s+- \*\*(Role|Now|If it fails)\*\*: (.*)$", ln)
            if m and cur["claims"]:
                cur["claims"][-1][m[1].lower()] = plain(m[2])
        elif part == "Potential work":
            m = re.match(r"^- \*\*([TD]\d+)\*\* · for ([^·]+?)(?: · (.+))?$", ln)
            if m:
                cur["work"].append(m[1])
    return sorted(qs, key=lambda q: q["n"])


def read(topic: Path) -> dict:
    face = topic / f"{topic.name}.md"
    if not face.is_file():
        raise SystemExit(f"{face}: no face")
    lines = face.read_text(encoding="utf-8").splitlines()
    qs = questions(lines)
    if not qs:
        raise SystemExit(f"{face.name}: no '#### 3.N · Question N · RQn' block (haipipe-paper-story §3)")
    title = re.sub(r"^s\d+\s*·\s*(Story:\s*)?", "", lines[0]).strip()
    one = lambda key: next((plain(ln.split(":**", 1)[1]) for ln in lines if ln.startswith(f"**{key}:**")), "")
    q = next((plain(ln.split("**:", 1)[1]) for ln in lines if ln.startswith("**The paper's question**:")), "")
    told = [plain(x) for x in items(lines, "**The story, question by question**")]
    if len(told) == len(qs):                          # the questions as the narrative: each step titled by its own
        for rq, s in zip(qs, told):
            rq["told"] = s[:s.index("?") + 1] if "?" in s else rq.get("name", "")
    E = {r["e"]: r for r in table(lines, "E")}
    T = {r["t"]: r for r in table(lines, "T")}
    return {"title": title[:1].upper() + title[1:], "question": q or title, "g0": one("G0"), "qs": qs, "E": E,
            "T": T, "pitch": [plain(x) for x in items(section(lines, "Pitch"), "")],
            "refuse": [plain(x) for x in items(lines, "**We will not claim**")]}


def e_mark(r: dict) -> str:
    s = (r.get("support state") or "").lower()
    return next((v for k, v in MARK.items() if k in s), "⬜")


def t_mark(r: dict) -> str:
    s = (r.get("state") or "").lower()
    return next((v for k, v in MARK.items() if k in s), "⬜")


# ── ① the main frame: the questions as steps ──────────────────────────────────────────────────────────────
def support(q: dict, S: dict) -> list:
    """A question's support card: the answer now, its claim, its E rows and T rows, each with its mark."""
    state = q.get("answer state", "⬜ no answer state in the face")
    out = [(state, 26, RED if missing(state) else INK)]
    for c in q["claims"][:1]:
        out.append((f"{c['c']} · {c['name']}: {c['what']}", 24, INK))
    tested = list(dict.fromkeys(e for h in q["hyp"] for e in h["tested"]))
    if tested:
        out.append(("evidence  " + " · ".join(f"{e_mark(S['E'].get(e, {}))} {e}" for e in tested), 22, GREY))
    runs = [t for t in q["work"] if t.startswith("T")]
    if runs:
        out.append(("work  " + " · ".join(f"{t_mark(S['T'].get(t, {}))} {t}" + (f" {S['T'][t]['where']}"
                                                                               if t in S["T"] else "")
                                         for t in runs), 22, GREY))
    return out


def main_frame(d: Drawing, S: dict) -> tuple[dict, dict]:
    qs = S["qs"]
    width = 140 + (len(qs) - 1) * SHIFT + RQ_W + 100 + CARD_W + 60
    heading = f"📖 {S['title']}"
    f = d.frame(f"① {heading}", width)
    Drawing.room(f)
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    d.text(40, 22, heading, 60)
    done = sum(1 for q in qs if mark(q.get("answer state", "")) == "✅")
    sub = (f"{len(qs)} research questions as steps: {done} answered · ✅ answered · 🔶 partly · ⬜ nothing supports it "
           "yet (red, dashed) · every number names its Run in the face")
    d.para(40, 112, sub, width - 80, 26, GREY)
    y = 180
    key = next((p for p in S["pitch"] if p.lower().startswith("the answer so far")), S["pitch"][2] if len(S["pitch"]) > 2
               else S["question"])
    kh = Drawing.height(key, width - 140, 34) + 44
    d.key(40, y, width - 80, kh)
    d.para(70, y + 22, key, width - 140, 34)
    y += kh + 30
    chain = "The story, as its questions:  " + "  →  ".join(q.get("name", q["rq"]) for q in qs)
    y = d.para(40, y, chain, width - 80, 30) + 60                 # read in order, the questions are the narrative
    qw = min(1500, width - 80)
    qh = box(d, 40, y, qw, [(S["question"], 46, INK)], sw=3)
    root = {"right": 40 + qw, "mid": y + qh / 2}
    spine_x, spine_top = 70, y + qh
    y += qh + STEP_GAP
    mids = []
    for i, q in enumerate(qs):
        x = 140 + i * SHIFT
        st = mark(q.get("answer state", "")) or "⬜"
        hole = missing(q.get("answer state", "⬜"))
        h = box(d, x, y, RQ_W, [(f"{st} {q['rq']} · {q.get('told') or q.get('name', '')}", 34, RED if hole else INK),
                                (q.get("question", ""), 22, GREY)], sw=2.5, dashed=hole)
        mid = y + 40
        mids.append(mid)
        d.line([(spine_x, mid), (x - 8, mid)], sw=3)
        cx = x + RQ_W + 100
        ch = box(d, cx, y, CARD_W, support(q, S), sw=1.5, dashed=hole)
        d.line([(x + RQ_W + 8, mid), (cx - 8, mid)], sw=2)
        y += max(h, ch) + STEP_GAP
    d.line([(spine_x, spine_top), (spine_x, mids[-1])], arrow=False, sw=3)
    if sum(Drawing.words_in(e.get("text", "")) for e in d.els if e.get("frameId") == f["id"] and e["type"] == "text") > 200:
        Drawing.detail(f)
    return finish(d, f, y - STEP_GAP + 40, small=False), root


# ── ② the pitch, ③ what we will not claim, ④ from here to the send ────────────────────────────────────────
def list_frame(d: Drawing, n: int, title: str, lines: list[str], numbered: bool = False) -> dict:
    W = 1500
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    y = 110
    for i, s in enumerate(lines, 1):
        y = d.para(40, y, (f"{i}. " if numbered else "· ") + s, W - 80, 26, RED if missing(s) else INK) + 14
    return finish(d, f, y)


def path_frame(d: Drawing, n: int, S: dict) -> dict:
    """Each Run still to make, as stairs: what it is, where, and who starts it; then G0 when it is not marked."""
    todo = [(t, r) for t, r in S["T"].items() if t_mark(r) != "✅"]
    steps = [(f"{t} · {r.get('work', '')}", f"{r.get('starts', '')} · {r.get('where', '')}") for t, r in todo]
    if S["g0"] and mark(S["g0"]) != "✅":
        steps.append(("🙋 G0", "JL's mark on the story"))
    BW, X, DY = 440, 500, 70                                       # each step lower and further right, no overlap
    W = max(1600, 80 + (len(steps) - 1) * X + BW)
    title = "From here to the send"
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    key = (f"{len(todo)} Runs to make, then G0. " if todo else "Every Run is made. ") + \
          "A Run that costs new model calls waits for JL to start it."
    kh = Drawing.height(key, W - 140, 30) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 30)
    y = 100 + kh + 50
    prev, bottom = None, y
    for i, (top, low) in enumerate(steps):
        x, yy = 40 + i * X, y + i * DY
        new_calls = "jl starts" in low.lower()
        h = box(d, x, yy, BW, [(top, 24, RED if new_calls else INK), (low, 20, GREY)],
                sw=2.5 if i == len(steps) - 1 else 1.5, dashed=new_calls)
        if prev:
            d.line([(prev[0] + BW + 6, prev[1] + 30), (x - 6, yy + 30)], sw=2)
        prev, bottom = (x, yy), max(bottom, yy + h)
    return finish(d, f, bottom)


def draw(topic: Path, out: Path | None = None) -> Path:
    topic = Path(topic).resolve()
    S = read(topic)
    d = Drawing()
    big, root = main_frame(d, S)
    pitch = list_frame(d, 1, "The pitch", S["pitch"], numbered=True) if S["pitch"] else None
    refuse = list_frame(d, 2, "What we will not claim", S["refuse"]) if S["refuse"] else None
    path = path_frame(d, 3, S) if S["T"] else None
    # the main frame at the origin; the small ones step down and to its right; the path below it, set in
    move(d.els, big, 0, 0)
    sx, y = big["width"] + 360, 0
    for i, f in enumerate(x for x in (pitch, refuse) if x):
        move(d.els, f, sx + i * 260, y)
        y += f["height"] + 200
    if path:
        move(d.els, path, 760, big["height"] + 320)
    d.fid = None
    if pitch:
        py = pitch["y"] + 120
        d.line([(root["right"] + 10, root["mid"]), (sx - 160, root["mid"]), (sx - 160, py), (sx - 14, py)], sw=3)
        d.text(root["right"] + 30, root["mid"] - 52, "in one minute", 32)
    if path:
        px = path["x"] + 300
        d.line([(px, big["height"] + 14), (px, path["y"] - 14)], sw=5)
        d.text(px + 20, big["height"] + 130, "what is missing", 36)
    builder = next(iter(sorted(topic.glob("build_*.py"))), None)
    out = out or topic / f"{topic.name}.excalidraw"
    d.write(out, builder.name if builder else Path(__file__).name)
    sys.path.insert(0, str(SKILLS / "1_base/project/haipipe-studio/scripts"))
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


# ── a topic's builder ──────────────────────────────────────────────────────────────────────────────────────
def scripts_from(topic: Path) -> str:
    """This folder, relative to the topic: through the SPACE's Tools link, or inside the Tools SPACE itself."""
    here_rel = HERE.relative_to(SKILLS.parents[2])
    for p in (topic, *topic.parents):
        for base in (p / "Tools", p):
            if (base / here_rel).is_dir():
                return Path(os.path.relpath(base / here_rel, topic)).as_posix()
    return str(HERE)


def make(topic: Path, force: bool = False) -> Path:
    topic = Path(topic).resolve()
    if not topic.is_dir():
        raise SystemExit(f"{topic} is not a folder; make the topic first (haipipe-paper-story)")
    m = re.match(r"s(\d\d)-(.+)$", topic.name)
    builder = topic / (f"build_s{m.group(1)}_{m.group(2).replace('-', '_')}.py" if m else "build.py")
    if builder.exists() and not force:
        raise SystemExit(f"{builder.name} exists; --force replaces it (keep a copy first if it holds drawing code)")
    builder.write_text(
        f'"""{topic.name}: drawn by excalidraw-story\'s story_drawing.py from this face (its research questions, '
        "their E and T rows, the pitch and what we will not claim); a person's marks on the drawing are kept.\n\n"
        f'    python {builder.name}\n"""\n'
        "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
        f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
        "import story_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    print(story_drawing.draw(HERE))\n",
        encoding="utf-8")
    return builder


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one story topic").add_argument("topic", type=Path)
    m = sub.add_parser("make", help="the topic's forwarding builder")
    m.add_argument("topic", type=Path)
    m.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    print(draw(a.topic) if a.cmd == "draw" else make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
