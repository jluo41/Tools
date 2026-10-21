"""A paper's workflow as one drawing: its Sections in reader order, the displays they carry, and the dates to the send.

Asked 261019 on Physician-SPACE's Project-LLMRec-Physician (JL: "你觉得我们需要一个 plan 吗？haipipe-paper-plan /
plan for the data flow and plan for the paper flow"; "please think about to make the s03 to be the paper-dataflow, and
s04 to be the s04-paper-workflow"). s03-paper-dataflow is the building map (workflow_drawing.py): how the data becomes
each answer. This draws s04-paper-workflow: how the answers become the paper. Drawn the way excalidraw-story draws s02
(one big main frame, small frames that explain it, as stairs; JL 261013), and read from the faces on every build.

    python paperflow_drawing.py draw <studio/s04-paper-workflow>     redraw one (what the topic's builder calls)
    python paperflow_drawing.py make <studio/s04-paper-workflow>     its forwarding builder

    ① 📝 the paper as it reads (main): the budget, then each Section a step lower and further right,
       its research question, its words and its displays (red and dashed when its evidence is missing)
          ② what each Section must do                     ③ the displays, as stairs: what each shows, the Run
                                                             that makes it, its state
       ④ from here to the send (below): each step with its date, a person's step marked 🙋

What it reads, haipipe-paper-plan's contract for the s04 face: the title line; `**Budget:**`; `**Send:**`; the tables
`| S | section | answers | job | displays | evidence | words |`, `| Display | title | kind | answers | made by | state |`
and `| W | step | when | who | state |`. From the telling (board.md `story-current:`): each research question's name and
answer state, and the E table's support states, so a Section whose evidence is absent shows red. The writer is
haipipe-studio's canvas.write, so a person's marks survive a rebuild.
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
sys.path.insert(0, str(SKILLS / "1_base/excalidraw/excalidraw-story/scripts"))
from draw import GREY, INK, RED, Drawing, canvas  # noqa: E402
from ideation_drawing import box, finish, move  # noqa: E402   one look with s01 and s02
from story_drawing import e_mark, joined, mark, plain, questions, table  # noqa: E402   one reading of the telling

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
SHIFT, SEC_W, STEP_GAP = 150, 1300, 70


# ── what the drawing reads ─────────────────────────────────────────────────────────────────────────────────
def ids(cell: str, letter: str) -> list[str]:
    """'E4 to E7, E9' -> ['E4', 'E5', 'E6', 'E7', 'E9'] ('RQ1, RQ3' with letter 'RQ'); an evidence row may be Ework or
    Ecite (JL 261020), kept with its own prefix and width: 'Ework04 to Ework06' -> ['Ework04', 'Ework05', 'Ework06']."""
    out = []
    pre = rf"{letter}(?:work|cite)?" if letter == "E" else letter
    for m in re.finditer(rf"({pre})(\d+)(?:\s*(?:to|-|–)\s*(?:{pre})?(\d+))?", cell or ""):
        head, a, b = m.group(1), m.group(2), m.group(3)
        out += [f"{head}{k:0{len(a)}d}" for k in range(int(a), int(b or a) + 1)]
    return out


def display_names(cell: str) -> list[str]:
    """'Figure 1, Figure 2 · eTable 1' -> ['Figure 1', 'Figure 2', 'eTable 1']; '—' -> []."""
    return [s.strip() for s in re.split(r"[,·;]", cell or "") if re.search(r"\w", s) and s.strip() not in ("—", "-")]


def board_of(topic: Path) -> Path | None:
    for p in (topic, *topic.parents):
        if (p / "board.md").is_file():
            return p
    return None


def telling(topic: Path) -> dict:
    """The telling the plan follows: board.md's `story-current:` face, its questions and E rows ({} when none)."""
    board = board_of(topic)
    if not board:
        return {"qs": [], "E": {}, "g0": ""}
    m = re.search(r"(?m)^story-current:\s*(\S+)", (board / "board.md").read_text(encoding="utf-8"))
    face = board / "studio" / m[1] / f"{m[1]}.md" if m else None
    if not face or not face.is_file():
        return {"qs": [], "E": {}, "g0": ""}
    lines = face.read_text(encoding="utf-8").splitlines()
    E = {r["e"]: r for r in table(lines, "E")}
    for r in table(lines, "D"):                        # a Discovery row counts as evidence too: its `state`
        st = (r.get("state") or "").lower()
        E[r["d"]] = {"support state": "established" if st.startswith(("done", "read", "closed")) else
                     "provisional" if st.startswith(("partly", "reading", "running")) else "absent"}
    return {"qs": questions(lines), "E": E, "g0": joined(lines, "**G0:**"), "name": m[1]}


def read(topic: Path) -> dict:
    topic = Path(topic)
    face = topic / f"{topic.name}.md"
    if not face.is_file():
        raise SystemExit(f"{face.name} not found in {topic}")
    lines = face.read_text(encoding="utf-8").splitlines()
    title = re.sub(r"^s\d\d\s*·\s*", "", lines[0]).strip()
    title = re.sub(r"^Paper workflow:\s*", "", title)
    title = title[:1].upper() + title[1:]
    secs = table(lines, "S")
    if not secs:
        raise SystemExit(f"{face.name}: no '| S | section | answers | job | displays | evidence | words |' table")
    return {"title": title, "budget": joined(lines, "**Budget:**"), "send": joined(lines, "**Send:**"),
            "S": secs, "displays": table(lines, "Display"), "W": table(lines, "W"), "story": telling(topic)}


def displays_by_question(board: Path) -> dict[int, str]:
    """For the building map (workflow_drawing.py): RQ number -> 'Figure 1 · Figure 2', from the Board's
    s04-paper-workflow face, so the displays are named once."""
    for face in sorted(Path(board).glob("studio/s??-paper-workflow/s??-paper-workflow.md")):
        lines = face.read_text(encoding="utf-8").splitlines()
        out: dict[int, list[str]] = {}
        for r in table(lines, "Display"):
            for rq in ids(r.get("answers", ""), "RQ"):
                out.setdefault(int(rq[2:]), []).append(r.get("display", ""))
        return {k: " · ".join(v) for k, v in out.items()}
    return {}


def ev_mark(sec: dict, E: dict) -> str:
    """A Section's mark from its evidence rows (E rows, and Discovery D rows by their state): ✅ all in hand, ⬜ none,
    🔶 some; '' when it names none."""
    cell = sec.get("evidence", "")
    marks = [e_mark(E[e]) for e in ids(cell, "E") + ids(cell, "D") if e in E]
    if not marks:
        return ""
    if all(m == "✅" for m in marks):
        return "✅"
    return "⬜" if all(m == "⬜" for m in marks) else "🔶"


def d_mark(r: dict) -> str:
    s = (r.get("state") or "").strip().lower()
    return mark(r.get("state", "")) or ("✅" if s.startswith(("done", "on disk", "made")) else
                                        "🔶" if s.startswith(("partly", "draft", "running")) else "⬜")


def words(cell: str) -> int:
    return sum(int(n.replace(",", "")) for n in re.findall(r"\d[\d,]*", re.sub(r"\(.*?\)", "", cell or "")))


def counted(sec: dict) -> bool:
    """A row counts toward the desk's cap unless its words cell says it is outside it ("350 (outside the count)")."""
    return "outside" not in (sec.get("words") or "").lower()


# ── ① the main frame: the Sections as steps ───────────────────────────────────────────────────────────────
def main_frame(d: Drawing, P: dict) -> dict:
    secs, story = P["S"], P["story"]
    names = {q["rq"]: q.get("name", "") for q in story["qs"]}
    width = 140 + (len(secs) - 1) * SHIFT + SEC_W + 80
    heading = f"📝 {P['title']}"
    f = d.frame(f"① {heading}", width)
    Drawing.room(f)
    if width > canvas.FRAME_MAX[0]:
        canvas.large(f)
    hb = d.para(40, 22, heading, width - 680, 44)
    total = sum(words(s.get("words", "")) for s in secs if counted(s))
    shown = sum(len(display_names(s.get("displays", ""))) for s in secs)
    unplaced = [q["rq"] for q in story["qs"] if not any(q["rq"] in ids(s.get("answers", ""), "RQ") for s in secs)]
    sub = f"{len(secs)} sections · {total:,} words counted · {shown} displays · ✅ evidence in hand, 🔶 partly, ⬜ missing" + \
          (f" · ❗ {', '.join(unplaced)} has no section" if unplaced else "")
    sy = max(112, hb + 20)
    d.para(40, sy, sub, width - 80, 28, RED if unplaced else GREY)
    y = sy + 70
    key = " · ".join(f"{k}: {v}" for k, v in (("Budget", P["budget"]), ("Send", P["send"])) if v) or \
        "❓ the face names no budget and no send date"
    kh = Drawing.height(key, width - 140, 30) + 40
    d.key(40, y, width - 80, kh)
    d.para(70, y + 20, key, width - 140, 30)
    spine_x, spine_top = 70, y + kh
    y += kh + STEP_GAP
    mids = []
    for i, s in enumerate(secs):
        x = 140 + i * SHIFT
        st = ev_mark(s, story["E"])
        hole = st == "⬜"
        rqs = ids(s.get("answers", ""), "RQ")
        top = f"{st + ' ' if st else ''}{s.get('s', '')} · {s.get('section', '')}"
        asks = " · ".join(f"{rq} {names.get(rq, '')}".strip() for rq in rqs)
        size = re.sub(r"\s*\(.*?\)", "", s.get("words", "")).strip()          # "350 (outside the count)"
        size = size and f"{size} words" + ("" if counted(s) else " (outside the count)")
        low = " · ".join(v for v in (size, s.get("displays", "").strip("— ")) if v)
        h = box(d, x, y, SEC_W, [(top, 34, RED if hole else INK), (asks, 28, INK), (low, 28, GREY)],
                sw=2.5 if rqs else 1.5, dashed=hole)
        mids.append(y + 36)
        d.line([(spine_x, y + 36), (x - 8, y + 36)], sw=3)
        y += h + STEP_GAP
    d.line([(spine_x, spine_top), (spine_x, mids[-1])], arrow=False, sw=3)
    return finish(d, f, y - STEP_GAP + 40, small=False)


# ── ② what each Section must do, ③ the displays, ④ from here to the send ─────────────────────────────────
def jobs_frame(d: Drawing, n: int, P: dict) -> dict:
    W = 1500
    title = "What each section must do"
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    y = 110
    for s in P["S"]:
        ev = s.get("evidence", "").strip("— ")
        line = f"{s.get('s', '')} · {s.get('section', '')}: {plain(s.get('job', ''))}" + (f" ({ev})" if ev else "")
        y = d.para(40, y, line, W - 80, 24, RED if ev_mark(s, P["story"]["E"]) == "⬜" else INK) + 14
    return finish(d, f, y)


def displays_frame(d: Drawing, n: int, P: dict) -> dict:
    """Each display as a step: what it shows, the question it answers, and the Run that makes it (figures are made by
    a Run, never drawn by hand); a display no Run makes yet is red and dashed."""
    W, BW, SH = 1700, 1300, 60
    title = "The displays, and the Run that makes each"
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    made = sum(1 for r in P["displays"] if d_mark(r) == "✅")
    key = f"{made} of {len(P['displays'])} made. A figure or table is made by a Run and only shown here."
    kh = Drawing.height(key, W - 140, 28) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 28)
    y = 100 + kh + 40
    for i, r in enumerate(P["displays"]):
        st = d_mark(r)
        top = f"{st} {r.get('display', '')} · {plain(r.get('title', ''))}"
        low = f"{r.get('kind', '')} · answers {r.get('answers', '—')} · made by {plain(r.get('made by', ''))}"
        h = box(d, 40 + i * SH, y, BW, [(top, 24, RED if st == "⬜" else INK), (low, 20, GREY)],
                sw=1.5, dashed=st == "⬜")
        y += h + 14
    return finish(d, f, y)


def timeline_frame(d: Drawing, n: int, P: dict, max_w: int = 2400) -> dict:
    """Each step to the send, left to right and a step lower: what, when, who; a person's step is marked 🙋."""
    steps = P["W"]
    BW, DY = 270, 64
    X = max(BW + 20, min(330, (max_w - 80 - BW) // max(1, len(steps) - 1)))
    W = max(1600, 80 + (len(steps) - 1) * X + BW)
    title = "From here to the send"
    f = d.frame(f"{CIRCLED[n]} {title}", W)
    d.text(40, 22, title, 44)
    done = sum(1 for r in steps if d_mark(r) == "✅")
    key = f"{done} of {len(steps)} steps done. 🙋 a person's step. " + (f"Send: {P['send']}" if P["send"] else
                                                                          "No send date yet.")
    kh = Drawing.height(key, W - 140, 30) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 30)
    y = 100 + kh + 50
    prev, bottom = None, y
    for i, r in enumerate(steps):
        x, yy = 40 + i * X, y + i * DY
        st = d_mark(r)
        person = bool(re.search(r"\b(marks|presses|reads|signs|sends|agrees|approves|decides|starts)\b",
                                r.get("who", "").lower()))      # a person's step names its verb: "<who> sends"
        top = f"{st} {r.get('w', '')} · {plain(r.get('step', ''))}"
        low = f"{r.get('when', '')} · {'🙋 ' if person and st != '✅' else ''}{r.get('who', '')}"
        h = box(d, x, yy, BW, [(top, 22, INK), (low, 20, GREY)], sw=2.5 if i == len(steps) - 1 else 1.5,
                dashed=st == "⬜")
        if prev:
            d.line([(prev[0] + BW + 6, prev[1] + 30), (x - 6, yy + 30)], sw=2)
        prev, bottom = (x, yy), max(bottom, yy + h)
    return finish(d, f, bottom)


def draw(topic: Path, out: Path | None = None) -> Path:
    topic = Path(topic).resolve()
    P = read(topic)
    d = Drawing()
    big = main_frame(d, P)
    jobs = jobs_frame(d, 1, P)
    disp = displays_frame(d, 2, P) if P["displays"] else None
    path = timeline_frame(d, 3 if disp else 2, P, big["width"]) if P["W"] else None
    move(d.els, big, 0, 0)
    sx = big["width"] + 360
    move(d.els, jobs, sx, 0)
    if disp:                                                       # a step lower and further right
        move(d.els, disp, sx + 260, jobs["height"] + 220)
    if path:                                                       # under the main frame
        move(d.els, path, 40, big["height"] + 320)
    d.fid = None
    acts = [(big, "Act 1 · The paper, as it reads")]
    acts += [(disp, "Act 2 · What the reader sees")] if disp else []
    acts += [(path, "Act 3 · From here to the send")] if path else []
    for f, name in acts:
        if f is disp:
            d.text(f["x"], f["y"] - 80, name, 44)
        else:
            d.para(f["x"] - 820, f["y"] + 20, name, 760, 44)
    ty = jobs["y"] + 60
    d.line([(big["width"] + 10, 160), (sx - 14, ty)], sw=2)
    if path:
        px = path["x"] + 300
        d.line([(px, big["height"] + 14), (px, path["y"] - 14)], sw=5)
        d.text(px + 20, big["height"] + 130, "to the send", 36)
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
        raise SystemExit(f"{topic} is not a folder; make the topic first (haipipe-paper-plan)")
    m = re.match(r"s(\d\d)-(.+)$", topic.name)
    builder = topic / (f"build_s{m.group(1)}_{m.group(2).replace('-', '_')}.py" if m else "build.py")
    if builder.exists() and not force:
        raise SystemExit(f"{builder.name} exists; --force replaces it (keep a copy first if it holds drawing code)")
    builder.write_text(
        f'"""{topic.name}: drawn by excalidraw-workflow\'s paperflow_drawing.py from this face (its Sections, '
        "displays and timeline) and the telling's questions and E rows; a person's marks on the drawing are kept.\n\n"
        f'    python {builder.name}\n"""\n'
        "import sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\n"
        f'sys.path.insert(0, str((HERE / "{scripts_from(topic)}").resolve()))\n'
        "import paperflow_drawing  # noqa: E402\n\nif __name__ == \"__main__\":\n    print(paperflow_drawing.draw(HERE))\n",
        encoding="utf-8")
    return builder


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one paper workflow topic").add_argument("topic", type=Path)
    m = sub.add_parser("make", help="the topic's forwarding builder")
    m.add_argument("topic", type=Path)
    m.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    print(draw(a.topic) if a.cmd == "draw" else make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
