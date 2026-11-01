"""A paper's display plan as one drawing (s06-paper-displays, haipipe-paper-plan; JL 261101: "we should also have the
plan for the displays"; "the display like that should also follow the venue").

    ① The displays, in the paper's order       each a step: Display A → Figure 1, its type and name, what it
                                               shows, the question and Section, main or supplement, the Run
    ② The venue's display rules                 from venues/<venue>/call.md's Displays table
    ③ Does the plan follow them?                haipipe-paper-plan's display_plan.check, one line each

    python displayplan_drawing.py draw <topic>      redraw (the topic's builder does this)
    python displayplan_drawing.py make <topic>      write the topic's forwarding builder

Everything is read on each build: the face's Displays table, the venue's rules, the pool's faces and Results. A
display no Run makes yet, or one that breaks a rule, is red and dashed. The writer is haipipe-studio's canvas.write,
so a person's marks survive a rebuild.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from paperflow_drawing import SKILLS, board_of, make as _make  # noqa: E402
from draw import GREY, INK, RED, Drawing  # noqa: E402
from ideation_drawing import box, finish, move  # noqa: E402
from story_drawing import plain  # noqa: E402

sys.path.insert(0, str(SKILLS / "2_theme/paper/haipipe-paper-plan/scripts"))
import display_plan as dp  # noqa: E402

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
MARK = {"done": "✅", "partly": "⏳", "running": "⏳"}


def state_mark(cell: str) -> str:
    c = (cell or "").strip()
    return c[:1] if c[:1] in "✅⏳⬜🙋" else next((v for k, v in MARK.items() if c.lower().startswith(k)), "⬜")


def displays_frame(d: Drawing, P: list, bad: set) -> dict:
    W, BW, SH = 1900, 1500, 60
    title = "The displays, in the paper's order"
    f = d.frame(f"{CIRCLED[0]} {title}", W)
    d.text(40, 22, title, 44)
    main = sum(1 for r in P if r["where"] == "main")
    key = (f"{main} in the paper, {len(P) - main} in the supplement. Each is made by a Run in j01_evidence_display; "
           "its paper number is counted from this order, never typed.")
    kh = Drawing.height(key, W - 140, 28) + 40
    d.key(40, 100, W - 80, kh)
    d.para(70, 120, key, W - 140, 28)
    y = 100 + kh + 40
    for i, r in enumerate(P):
        st = state_mark(r.get("state", ""))
        red = r.get("display", "") in bad
        top = f"{st} {r.get('display', '')} → {r['as']} · {dp.TYPES[r['type']]} · {plain(r.get('name', ''))}"
        mid = plain(r.get("shows", ""))
        low = (f"answers {r.get('answers', '—')} · {r.get('section', '—')} · {r['where']} · "
               f"made by {plain(r.get('made by', '')) or 'no Run yet'}")
        lines = [(top, 26, RED if red else INK)] + ([(mid, 22, INK)] if mid else []) + [(low, 20, GREY)]
        h = box(d, 40 + i * SH, y, BW, lines, sw=1.5, dashed=st == "⬜" or red)
        y += h + 16
    return finish(d, f, y)


def rules_frame(d: Drawing, R: dict, venue: str) -> dict:
    W = 1300
    title = f"The venue's display rules · {venue}" if venue else "The venue's display rules"
    f = d.frame(f"{CIRCLED[1]} {title}", W)
    d.text(40, 22, title, 44)
    y = 110
    if not R:
        return finish(d, f, d.para(40, y, "No Displays table in the venue's call.md yet: haipipe-paper-venue writes it.",
                                   W - 80, 26, RED) + 14)
    for k in dp.RULES:
        v, src = R.get(k, ("", ""))
        line = f"{k}: {v}" if v else f"{k}: not recorded"
        y = d.para(40, y, line, W - 80, 26, INK if v else GREY) + 10
    return finish(d, f, y)


def check_frame(d: Drawing, lines: list) -> dict:
    W = 1300
    title = "Does the plan follow them?"
    f = d.frame(f"{CIRCLED[2]} {title}", W)
    d.text(40, 22, title, 44)
    y = 110
    for m, t in lines:
        y = d.para(40, y, f"{m} {t}", W - 80, 24, RED if m == "❗" else INK) + 10
    return finish(d, f, y)


def draw(topic: Path, out: Path | None = None) -> Path:
    topic = Path(topic).resolve()
    board = board_of(topic)
    if board is None:
        raise SystemExit(f"{topic}: no board.md above it")
    P, R, lines = dp.rows(board), dp.rules(board), dp.check(board)
    call = dp.venue_call(board)
    bad = {r.get("display", "") for r in P for m, t in lines if m == "❗" and t.startswith(r.get("display", "") + " ")}
    d = Drawing()
    disp = displays_frame(d, P, bad)
    rul = rules_frame(d, R, call.parent.name if call else "")
    chk = check_frame(d, lines)
    move(d.els, disp, 0, 0)
    sx = disp["width"] + 300
    move(d.els, rul, sx, 0)
    move(d.els, chk, sx + 200, rul["height"] + 200)
    d.fid = None
    d.line([(disp["width"] + 10, 160), (sx - 14, 160)], sw=2)
    d.line([(sx + 300, rul["height"] + 14), (sx + 300, rul["height"] + 186)], sw=3)
    builder = next(iter(sorted(topic.glob("build_*.py"))), None)
    out = out or topic / f"{topic.name}.excalidraw"
    d.write(out, builder.name if builder else Path(__file__).name)
    sys.path.insert(0, str(SKILLS / "1_base/project/haipipe-studio/scripts"))
    from render_png import render
    render(out, out.with_suffix(".png"))
    return out


def make(topic: Path, force: bool = False) -> Path:
    b = _make(topic, force)
    b.write_text(b.read_text(encoding="utf-8").replace("paperflow_drawing", "displayplan_drawing")
                 .replace("from this face (its Sections, displays and timeline) and the telling's questions and E rows",
                          "from this face's Displays table, the venue's display rules and the pool"), encoding="utf-8")
    return b


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("draw", help="redraw one display plan topic").add_argument("topic", type=Path)
    m = sub.add_parser("make", help="the topic's forwarding builder")
    m.add_argument("topic", type=Path)
    m.add_argument("--force", action="store_true", help="replace an existing builder")
    a = ap.parse_args(argv)
    print(draw(a.topic) if a.cmd == "draw" else make(a.topic, a.force))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
