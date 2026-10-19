"""s21 · The 1_base/draft skills: which stay, which merge: s21-draft-skill-map.excalidraw, drawn by this builder.

How it looks and reads: /excalidraw-studio (principles, scripts/draw.py). The topic, its face and sessions:
/haipipe-studio. A rebuild keeps what a person drew on the canvas (canvas.write). Check: excalidraw-studio's check.py.

What is on disk is read on every build: the pieces of 1_base/draft/, the Run skills, which targets exist.
The proposed moves are the face's inventory (s21-draft-skill-map.md).

    python build_s21_draft_skill_map.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[3]
BASE = TOOLS / "plugins/haipipe-toolkit/skills/1_base"
sys.path.insert(0, str((BASE / "excalidraw/excalidraw-studio/scripts").resolve()))
from draw import Drawing, RED, GREEN, canvas  # noqa: E402

DRAFT = BASE / "draft"


def dirs(p):
    return sorted(q.name for q in p.iterdir() if q.is_dir() and not q.name.startswith(("_", "."))) if p.is_dir() else []


def here(name):
    """Is the piece still inside 1_base/draft/ on this build?"""
    return any((DRAFT / s / name).exists() for s in ("", "workflow-runs", "writing"))


def main():
    out = HERE / "s21-draft-skill-map.excalidraw"
    top = dirs(DRAFT)
    runs = dirs(DRAFT / "workflow-runs")
    prose = dirs(DRAFT / "writing")
    pieces = [t for t in top if t not in ("workflow-runs", "writing")] + runs + prose
    bench = [t for t in top if t.startswith("workbench")]
    d = Drawing()

    # ① today
    f1 = d.frame("① Today: what 1_base/draft/ holds")
    d.heading(f"{len(pieces)} pieces in 1_base/draft/", "counted from disk on this build; the face lists 21 with the old alias")
    d.key(40, 190, 1000, 330)
    d.text(80, 215, "Writes and judges", 56)
    d.text(80, 295, "nothing says who judges", 38)
    d.text(80, 360, "one door, a controller,", 34)
    d.text(80, 405, f"{len(runs)} steps, each its own skill", 34)

    def card(x, y, w, h, title, sub, red=False):
        d.box(x, y, w, h, RED if red else "#1e1e1e", 2.5, dashed=red)
        d.text(x + 24, y + 18, title, 38, RED if red else "#1e1e1e")
        d.text(x + 24, y + 78, sub, 30, RED if red else "#1e1e1e")

    card(1120, 190, 560, 150, "door", "haipipe-draft")
    card(1760, 190, 700, 150, "controller", "haipipe-draft-workflow")
    card(1120, 400, 1340, 190, f"{len(runs)} Run skills", "  ·  ".join(r.replace("haipipe-draft-", "") for r in runs))
    card(40, 680, 760, 170, "prose worker", f"writing/  ({len(prose)} pieces)")
    card(880, 680, 760, 170, f"{len(bench)} workbench skills", "page  ·  studio  ·  the contract")
    card(1720, 680, 740, 170, "2 contracts", "haipipe-folder  ·  haipipe-sentence")
    card(40, 930, 760, 150, "example", "pages-example")
    alias = (DRAFT / "haipipe-page").exists()
    card(880, 930, 760, 150, "old alias", "haipipe-page " + ("(a link)" if alias else "(gone)"))
    d.line([(1680, 265), (1750, 265)], sw=4)
    d.text(1640, 150, "calls", 28)
    d.line([(2110, 350), (2110, 390)], sw=4)
    d.line([(1400, 600), (1400, 670), (420, 670), (420, 676)], sw=4)
    d.text(900, 622, "writing step calls", 28)
    d.text(40, 1160, "Every one of them is a skill with its own door.", 38)
    d.text(40, 1230, "Which stay, which merge?", 56, RED)
    d.badge(f1)

    # ② the moves
    f2 = d.frame("② The moves: each piece to where it goes", 2560, 1600)
    d.heading("Each piece goes to one of the four", "red and 🙋 = open for JL; green = already moved on disk")
    rows = [  # (label, still-here name or None, target key, arrow words)
        ("haipipe-draft (door)", "haipipe-draft", "draft", "stays"),
        ("haipipe-draft-workflow", "haipipe-draft-workflow", "draft", "folds in"),
        ("5 Run skills: context · structure · scratch · writing · revise", "haipipe-draft-context", "draft", "steps as ref/"),
        ("haipipe-sentence", "haipipe-sentence", "draft", "ref/sentence.md"),
        ("pages-example", "pages-example", "draft", "examples/"),
        ("workbench-page", "workbench-page", "draft", "its screen"),
        ("writing/ (haipipe-writing)", "haipipe-writing", "draft", "drafting half"),
        ("Run skill: check", "haipipe-draft-check", "review", "the gate"),
        ("Run skill: evidence", "haipipe-draft-evidence", "evidence", "LAND + EMBED"),
        ("🙋3 Run skill: delivery", "haipipe-draft-delivery", "deliv", "which home?"),
        ("🙋2 haipipe-folder", "haipipe-folder", "else", ""),
        ("🙋4 workbench · workbench-studio", "workbench-studio", "else", ""),
        ("haipipe-page (alias)", "haipipe-page", "gone", "after the sweep"),
    ]
    x0, w0, pitch, y0, hh = 60, 840, 100, 190, 80
    ys = {}
    for i, (label, name, tk, words) in enumerate(rows):
        y = y0 + i * pitch
        red = label.startswith("🙋")
        gone_now = name and not here(name) and name != "haipipe-draft"
        d.box(x0, y, w0, hh, RED if red else "#1e1e1e", 2.5, dashed=red)
        d.text(x0 + 20, y + 22, label, 30, RED if red else "#1e1e1e")
        if gone_now:
            d.els.append(canvas.change_note(x0 + w0 - 190, y + 4, "moved", None, d.fid, size=21))
        ys[i] = y + hh / 2
    # targets (x 1500..2480), each spanning the rows it receives
    tx, tw = 1560, 900

    def target(i0, i1, title, sub, key=False, red=False):
        y, h = y0 + i0 * pitch - 4, (i1 - i0) * pitch + hh + 8
        if key:
            d.key(tx, y, tw, h)
        else:
            d.box(tx, y, tw, h, RED if red else "#1e1e1e", 3, dashed=red)
        d.text(tx + 30, y + h / 2 - 48, title, 38 if not key else 44, RED if red else "#1e1e1e")
        d.text(tx + 30, y + h / 2 + 8, sub, 30, RED if red else "#1e1e1e")

    target(0, 6, "haipipe-draft", "writes: the steps become ref/", key=True)
    target(7, 7, "haipipe-draft-review", "judges")
    target(8, 8, "haipipe-evidence", "backs")
    target(9, 9, "haipipe-delivery or a ref", "🙋3 two homes", red=True)
    target(10, 11, "elsewhere", "🙋 haipipe-task · 1_base/project · studio", red=True)
    target(12, 12, "gone", "the link")
    # arrows
    tgt_y = {"draft": y0 + 3 * pitch + hh / 2 - 4, "review": ys[7], "evidence": ys[8], "deliv": ys[9], "else": ys[10] + pitch / 2, "gone": ys[12]}
    for i, (label, name, tk, words) in enumerate(rows):
        red = label.startswith("🙋")
        yt = ys[i] if tk in ("review", "evidence", "deliv", "gone") else (ys[i] if tk == "draft" else ys[i])
        d.line([(x0 + w0 + 10, ys[i]), (tx - 10, yt)], RED if red else "#1e1e1e", sw=3)
        if words:
            d.text(x0 + w0 + 40, ys[i] - 36, words, 28, RED if red else "#1e1e1e")
    # the writing row also sends its judging half to review
    d.line([(x0 + w0 + 10, ys[6] + 20), (tx - 10, ys[7] - 10)], sw=3)
    d.text(x0 + w0 + 500, ys[6] + 30, "judging half", 28)
    d.text(1560, 1520, "🙋1  Four skills, or keep any Run skill apart?", 40, RED)
    d.badge(f2)

    # ③ the end shape
    f3 = d.frame("③ The end shape: four skills, who calls whom")
    d.heading("Four skills", "the writer never judges its own text, so review is its own skill")
    have = lambda n: (BASE / n).is_dir()
    dx, dw, dy, dh = 880, 800, 230, 280
    d.key(dx, dy, dw, dh)
    d.text(dx + 40, dy + 30, "haipipe-draft", 56)
    d.text(dx + 40, dy + 120, "writes", 44)
    d.text(dx + 40, dy + 200, "+ workbench-page, its screen", 30)
    cards = [("haipipe-draft-review", "judges", 100, "draft"), ("haipipe-evidence", "backs", 1000, "evidence"),
             ("haipipe-display", "shows", 1900, "display")]
    by, bh, bw = 860, 300, 560
    for name, verb, bx, folder in cards:
        d.box(bx, by, bw, bh, "#1e1e1e", 3)
        d.text(bx + 30, by + 30, name, 38)
        d.text(bx + 30, by + 100, verb, 56)
        d.text(bx + 30, by + 210, f"1_base/{folder}/", 28, code=True)
        if have(folder) and name != "haipipe-draft-review":
            d.els.append(canvas.change_note(bx + 30, by + 255, "folder is there", None, d.fid, size=22))
    mid = by - 150
    starts = [dx + 160, dx + 400, dx + 640]
    for (name, verb, bx, folder), sx, words, ly in zip(cards, starts, ["asks for a judge", "needs backing", "asks for a figure"], [mid - 50, dy + dh + 50, mid - 50]):
        cx = bx + bw / 2
        d.line([(sx, dy + dh + 12), (sx, mid), (cx, mid), (cx, by - 12)], sw=5)
        d.text({0: cx - 60, 1: sx + 30, 2: cx + 40}[starts.index(sx)] if starts.index(sx) != 2 else sx + 90, ly, words, 34)
    d.line([(1900 - 10, by + bh / 2), (1560 + 10, by + bh / 2)], sw=5)
    d.text(1590, by + bh / 2 - 56, "reads", 40)
    d.text(100, 1250, "Order: review first (new, nothing breaks), then the Run skills, then the alias sweep.", 30)
    d.text(100, 1310, "🙋5  Check each step by opening a real Page.", 30, RED)
    d.badge(f3)

    d.acts([{"name": "Act 1 · today", "frames": [f1["id"]]},
            {"name": "Act 2 · the moves", "frames": [f2["id"]]},
            {"name": "Act 3 · the end", "frames": [f3["id"]]}],
           between=[(f1["id"], f2["id"], "each piece moves"), (f2["id"], f3["id"], "what is left")])
    d.write(out, "build_s21_draft_skill_map.py")


if __name__ == "__main__":
    main()
