"""s04 · Studio and Report: s04-studio-and-report.excalidraw, a plain prototype in six frames.

1 · Studio and Report            what each is for, side by side
2 · From studio to report        the report drawing is generated from named studio frames
3 · Idea Studio on screen        the workbench screen at Block, Job and Task (studio_report_ui.py)
4 · Audience Report on screen    the same, for the reports; Work Details may be empty (s04-D05)
5 · the logic tree              what a Block holds (lines) and how studio and report relate (labelled arrows)
Questions                        what is still open

Black and gray lines, placeholders only; red marks what is open. Written through canvas.write, so
every mark a person adds survives a rebuild.

    python build_s04_studio_and_report.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import studio_report_ui as UI  # noqa: E402  (Idea Studio and Audience Report, drawn large; s11 uses it too)

INK, GRAY, RED, MONO = L.INK, L.GRAY, L.RED, L.MONO
text, box, path, base = L.text, L.box, L.path, L.base

COMPARE = [  # what · studio/sNN-<topic>/ · reports/qNN_<topic>/
    ("job", "think, argue, try", "answer, show the evidence"),
    ("drawings", "many, rough: sNN-<topic>.excalidraw + more", "one: qNN_<topic>.excalidraw"),
    ("made by", "a person, seeded by build_<topic>.py", "generated: build_report_drawing.py"),
    ("who edits", "the person, freely; marks are kept", "nobody by hand; Suggest leaves a note"),
    ("lifespan", "grows, gets messy, may end", "settles, then stays"),
    ("the link", "feeds: Q01, Q03  (a plan)", "## Figures: sNN › <frame>  (the source)"),
    ("words", "sNN-<topic>.md: decided · open", "qNN_<topic>.md: Answer · Evidence · Limits · Next"),
    ("on screen", "Block › Idea Studio", "Block › Audience Report"),
]
QUESTIONS = [
    "? keep the person's own marks in a figure (today: yes, except red notes)",
    "? a frame wider than the report shrinks to unreadable: split it, crop it, or a wider report",
    "? where the report drawing lives: qNN_<topic>.excalidraw (s01-D03) or reports/qNN/studio/ (excalidraw-report)",
    "? Suggest on a report figure: a note on the studio frame, or a comment on the report",
    "? when it rebuilds: make.sh, a Run button on the Question's row, or on every studio save",
    "? feeds: in sNN.md and ## Figures in qNN.md: keep both, or derive feeds from the figure lists",
]


def frame_compare(y0):
    fr = L.open_frame("1 · Studio and Report")
    text(0, y0, "Studio and Report: one makes, the other shows", 34)
    text(0, y0 + 50, "Both draw. The studio is the source; the report drawing is built from its frames.", 20, GRAY)
    cols, widths = [0, 220, 900], [220, 680, 760]
    y = y0 + 110
    for i, head in enumerate(["", "studio/sNN-<topic>/", "reports/qNN_<topic>/"]):
        text(cols[i] + 16, y + 14, head, 20, INK, MONO)
    for row in COMPARE:
        y += 56
        path([(0, y), (sum(widths), y)], arrow=False, color=GRAY)
        for i, cell in enumerate(row):
            text(cols[i] + 16, y + 16, cell, 18, GRAY if i == 0 else INK, MONO if "<" in cell or "." in cell else L.SANS)
    y += 56
    path([(0, y), (sum(widths), y)], arrow=False, color=GRAY)
    for x in (cols[1], cols[2]):
        path([(x, y0 + 110), (x, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


def frame_flow(x0, y0):
    fr = L.open_frame("2 · From studio to report")
    text(x0, y0, "From studio to report: generated, never drawn by hand", 34)
    W, H = 360, 64
    a = (x0, y0 + 120)
    b = (x0, y0 + 260)
    box(*a, W, H, "sNN-<a>.excalidraw", 18)
    text(a[0], a[1] + H + 8, "frame \"1 · <name>\"  + the person's marks", 16, GRAY)
    box(*b, W, H, "sNN-<b>.excalidraw", 18)
    text(b[0], b[1] + H + 8, "frame \"<variant>\"", 16, GRAY)
    lst = (x0 + 620, y0 + 150)
    box(*lst, 420, 120, "qNN_<topic>.md", 18)
    text(lst[0] + 16, lst[1] + 66, "## Figures\n- sNN-<a> › 1 · <name> · caption", 15, GRAY, MONO)
    gen = (x0 + 1180, y0 + 180)
    box(*gen, 400, H, "build_report_drawing.py", 18)
    out = (x0 + 1720, y0 + 180)
    box(*out, 420, H, "qNN_<topic>.excalidraw", 18)
    text(out[0], out[1] + H + 8, "heading frame + Fig 1 .. Fig N\nscaled to one width, straight lines,\n"
                                  "red notes left out, a source line each", 16, GRAY)
    path([(a[0] + W + 8, a[1] + H / 2), (lst[0] - 8, lst[1] + 40)])
    path([(b[0] + W + 8, b[1] + H / 2), (lst[0] - 8, lst[1] + 80)])
    text(a[0] + W + 40, a[1] - 6, "cited by frame name", 16, GRAY)
    path([(lst[0] + 428, lst[1] + 60), (gen[0] - 8, gen[1] + H / 2)])
    text(lst[0] + 440, lst[1] + 20, "reads the list", 16, GRAY)
    path([(gen[0] + 408, gen[1] + H / 2), (out[0] - 8, out[1] + H / 2)])
    text(gen[0] + 412, gen[1] - 30, "writes", 16, GRAY)
    ui = (x0 + 1720, y0 + 420)
    box(*ui, 420, H, "Audience Report row", 18)
    path([(out[0] + 210, out[1] + H + 96), (ui[0] + 210, ui[1] - 8)])
    text(out[0] + 230, out[1] + H + 120, "view only", 16, GRAY)
    path([(ui[0] - 8, ui[1] + H / 2), (a[0] + W / 2, ui[1] + H / 2), (a[0] + W / 2, b[1] + H + 40)],
         color=RED, dashed=True)
    text(x0 + 600, ui[1] + H / 2 + 10, "? Suggest: a note goes back to the studio frame, then rebuild", 16, RED)
    L.close_frame(fr)
    return fr


TREE = {  # name -> (x, y, w, box text, the line under it): the logic tree of a Block's studio and reports
    "block": (0, 330, 300, "bNN_<topic>/", "one topic: its Questions and its work"),
    "studio": (400, 120, 240, "studio/", "creation: the team's room"),
    "register": (400, 330, 300, "board.md · Questions", "the register: Q01 · Q02 · Q03"),
    "reports": (400, 560, 240, "reports/", "presentation: one folder per Question"),
    "topic": (780, 120, 280, "sNN-<topic>/", "one topic of thought"),
    "q": (780, 560, 280, "qNN_<topic>/", "one Question's report"),
    "draw": (1200, 20, 380, "sNN-<topic>.excalidraw", 'frames "1 · <name>" · "Questions"; drawn freely'),
    "face": (1200, 120, 380, "sNN-<topic>.md", "decided · open · feeds: Q03"),
    "sess": (1200, 220, 380, "runs/run-draw-<sNN>/", "each session is a pass"),
    "qmd": (1200, 490, 380, "qNN_<topic>.md", "Answer · Evidence (cites Runs) · Limits · Next"),
    "qdraw": (1200, 640, 380, "qNN_<topic>.excalidraw", "generated: one drawing, view only"),
    "tool": (1740, 330, 360, "build_report_drawing.py", "formats the cited frames"),
}
H = 52


def frame_maps(x0, y0):
    """The logic tree: what holds what (plain lines), how studio and report relate (labelled arrows)."""
    fr = L.open_frame("5 · Studio and Report: the logic tree")
    text(x0, y0, "The logic tree: what a Block holds, and how its studio and its reports relate", 34)
    text(x0, y0 + 50, "plain line = holds  ·  arrow = a relationship, labelled  ·  red dashed = open", 20, GRAY)
    oy = y0 + 150
    at = {k: (x0 + x, oy + y, w) for k, (x, y, w, _, _) in TREE.items()}
    for k, (x, y, w, name, line) in TREE.items():
        box(x0 + x, oy + y, w, H, name, 17)
        text(x0 + x, oy + y + H + 6, line, 15, GRAY)
    for parent, kids in [("block", ["studio", "register", "reports"]), ("studio", ["topic"]),
                         ("reports", ["q"]), ("topic", ["draw", "face", "sess"]), ("q", ["qmd", "qdraw"])]:
        px, py, pw = at[parent]
        mx = px + pw + 40
        for k in kids:                                  # the tree: plain lines from parent to child
            kx, ky, _ = at[k]
            path([(px + pw + 4, py + H / 2), (mx, py + H / 2), (mx, ky + H / 2), (kx - 4, ky + H / 2)],
                 arrow=False, color=INK)

    def X(v):
        return x0 + v

    def Y(v):
        return oy + v

    def rel(pts, label, where, color=GRAY, dashed=False):
        path([(X(a), Y(b)) for a, b in pts], color=color, dashed=dashed)
        text(X(where[0]), Y(where[1]), label, 15, color)

    rel([(1588, 140), (1640, 140), (1640, 345), (708, 345)], "feeds: Q03 (a plan)", (1100, 318))
    rel([(708, 372), (920, 372), (920, 552)], "answered in", (930, 440))
    rel([(1588, 510), (1700, 510), (1700, 56), (1588, 56)], "## Figures:\ncites frames\nby name", (1712, 150))
    rel([(1588, 34), (1820, 34), (1820, 322)], "copies the\nframes", (1832, 200))
    rel([(1588, 526), (2060, 526), (2060, 390)], "reads the\nlist", (2072, 430))
    rel([(2108, 356), (2160, 356), (2160, 666), (1588, 666)], "builds", (2172, 500))
    rel([(1540, 700), (1540, 760), (2220, 760), (2220, 0), (1500, 0), (1500, 12)],
        "? Suggest: a note goes back to the studio frame", (1560, 770), RED, True)
    text(x0, oy + 840, "Every level has both: a Job or a Task holds its own studio/ and reports/, related the same way.",
         18, INK)
    L.close_frame(fr)
    return fr


def frame_questions(x0, y0):
    fr = L.open_frame("Questions")
    text(x0, y0, "Questions", 30)
    for i, q in enumerate(QUESTIONS):
        text(x0, y0 + 60 + i * 40, q, 18, RED)
    L.close_frame(fr)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s04-studio-and-report.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a = frame_compare(0)
    b = frame_flow(a["x"] + a["width"] + 300, 0)
    c, d = UI.closeups(0, max(a["y"] + a["height"], b["y"] + b["height"]) + 300,
                       {"Idea Studio": "3 · Idea Studio on screen", "Audience Report": "4 · Audience Report on screen"})
    q = frame_questions(0, d["y"] + d["height"] + 300)
    frame_maps(q["x"] + q["width"] + 300, q["y"])
    canvas.write(out, list(L.els), "build_s04_studio_and_report.py")


if __name__ == "__main__":
    main()
