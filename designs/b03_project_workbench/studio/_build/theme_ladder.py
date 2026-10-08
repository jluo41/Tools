"""One theme's ladder in one drawing: every row of that theme, Block down to Run (JL 261007).

Each theme Block (Tools/designs/bNN_theme_<theme>/) draws its studio/s01-<theme>-ladder/ through this:
an overview frame (the theme, its Block's open questions), then the theme's rows of b03's s11 (Blocks),
s12 (Jobs) and s13 (Tasks), each a frame with its proposed screens above today's. The trees, skills and
screens are defined once, in ../s01-overall-tree-structure/ (build_ladder_v4.py, level_views.py); edit
them there and every drawing follows. It writes through canvas.write, so a person's marks survive.

    draw("cowork", ["cowork"], board_md, out)       # from a Block's build_s01_<theme>_ladder.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE))
import build_ladder_v4 as L  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."


def questions(board_md):
    """(id, title) of each question in a Block's board.md register."""
    s = Path(board_md).read_text()
    return re.findall(r"- id: (Q\d+)\n  title: (.+)", s)


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def overview(theme, families, board_md, y=0):
    fr = L.open_frame(f"{theme} ladder")
    L.text(0, y, f"Theme {theme}: every level in one drawing", 30)
    L.text(0, y + 46, f"The {theme} rows of b03's s11 (Blocks), s12 (Jobs) and s13 (Tasks), together; each frame "
                      "below is drawn from the same definitions as there.", 16, L.GRAY)
    ty = y + 100
    L.text(0, ty, "rows drawn", 18, L.INK)
    for k, (level, trees, fam) in enumerate([("Board level", L.BLOCK_TREES, L.BLOCK_FAMILY),
                                             ("Job level", L.JOB_TREES, LV.JOB_FAMILY),
                                             ("Task level", L.TASK_TREES, LV.TASK_FAMILY)]):
        names = [t[0] for t in trees if fam.get(t[0]) in families]
        L.text(160, ty + 2 + k * 26, f"{level}: " + (" · ".join(names) or "none yet ?"), 15,
               L.RED if not names else L.TEAL)
    ty += 3 * 26 + 40
    L.text(0, ty, "open", 18, L.RED)
    for k, (qid, title) in enumerate(questions(board_md)):
        L.text(160, ty + 2 + k * 26, f"{qid}  {title}", 15, L.RED)
    L.close_frame(fr, pad=40)
    return bottom()


def draw(theme, families, board_md, out, source):
    """Draw the theme's ladder into out; families = the family keys of its rows (b03's *_FAMILY values)."""
    L.els.clear()
    L.FRAME[0] = None
    y = overview(theme, families, board_md) + 260
    for title, trees, fam, level, block in [("Board level", L.BLOCK_TREES, L.BLOCK_FAMILY, "Block", True),
                                            ("Job level", L.JOB_TREES, LV.JOB_FAMILY, "Job", False),
                                            ("Task level", L.TASK_TREES, LV.TASK_FAMILY, "Task", False)]:
        rows = [t for t in trees if fam.get(t[0]) in families]
        if not rows:
            continue
        L.draw_trees(f"{theme} · {title}", SUB, rows, y, frame_each=True, views=LV.rows(level), block=block)
        y = bottom() + 260
    canvas.write(out, list(L.els), source)
