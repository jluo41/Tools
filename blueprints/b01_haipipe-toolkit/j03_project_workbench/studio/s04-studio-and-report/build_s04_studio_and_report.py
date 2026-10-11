"""s04 · Studio and Report: s04-studio-and-report.excalidraw, a prototype with a shared relationship and linked-panel proposal.

1 · Studio and Report            what each is for, side by side
2 · From studio to report        the report drawing is generated from named studio frames
3 · Idea Studio on screen        the workbench screen at Block, Job and Task (studio_report_ui.py)
4 · Audience Report on screen    the same, for the reports; Work Details may be empty (s04-D05)
5 · the logic tree              what a Block holds (lines) and how studio and report relate (labelled arrows)
6 · Studio item, frames and Questions  N frames; n primary frames linked to Question-Report pairs
7 · Linked Studio and Report panels    one workspace, two panels (UI proposal)
8 · From exploration to an answer      no Question until a frame has a question worth answering
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
    ("lifespan", "grows; new frames can stay exploratory", "current answer: open, partial, answered"),
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
    note(0, y + 38, "Report holds the current answer, even while it is partial")
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
    "topic": (780, 120, 280, "sNN-<topic>/", "one Studio item: a broad topic"),
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
    rel([(1588, 34), (1820, 34), (1820, 322)], "formats cited\nsource frames", (1832, 200))
    rel([(1588, 526), (2060, 526), (2060, 390)], "reads the\nlist", (2072, 430))
    rel([(2108, 356), (2160, 356), (2160, 666), (1588, 666)], "builds", (2172, 500))
    rel([(1540, 700), (1540, 760), (2220, 760), (2220, 0), (1500, 0), (1500, 12)],
        "? Suggest: a note goes back to the studio frame", (1560, 770), RED, True)
    text(x0, oy + 840, "Every level has both: a Job or a Task holds its own studio/ and reports/, related the same way.",
         18, INK)
    note(x0, oy + 880, "sNN is a Studio item; frames may stay exploratory")
    L.close_frame(fr)
    return fr


def frame_questions(x0, y0):
    fr = L.open_frame("Questions")
    text(x0, y0, "Questions", 30)
    for i, q in enumerate(QUESTIONS):
        text(x0, y0 + 60 + i * 40, q, 18, RED)
    L.close_frame(fr)
    return fr



CHANGES = [
    "sNN means Studio item; it contains N named frames",
    "n of N frames anchor qNN Question-Report pairs; rNN stays Run",
    "Report holds the current answer, even while it is partial",
    "Linked panels and source-change review drawn as UI proposals",
]


def note(x, y, what, size=17):
    e = canvas.change_note(x, y, what, "261010", L.FRAME[0], size)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


def card(x, y, w, h, title, body, size=21):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 22, y + 18, title, size)
    text(x + 22, y + 64, body, 19)


def frame_relationship():
    fr = L.open_frame("6 · Studio item, frames and Questions")
    text(0, 0, "One Studio item, N frames, n Question-Report pairs", 36)
    text(0, 58, "Idea Studio = the view  |  sNN = a Studio item  |  frame = one area of its drawing", 22)
    box(0, 145, 390, 72, "studio/s01-<topic>/", 23)
    text(0, 236, "A broad topic can keep expanding.\nIts drawing contains N named frames.", 21)
    path([(390, 181), (440, 181), (440, 438), (488, 438)], arrow=False)
    base("rectangle", 500, 140, 620, 970, INK, 1.5)
    text(522, 162, "s01 drawing: N frames", 25)
    for y, title, body in [
        (245, "Frame A · <question A>", "primary frame for q01\nideas, alternatives, evidence, marks"),
        (490, "Frame B · <question B>", "primary frame for q02\nits own question, answer and work"),
        (735, "Frame C · <background>", "exploration or supporting material\nno Question required yet"),
        (950, "... Frame N", "new frames as the topic expands"),
    ]:
        card(525, y, 570, 155 if y == 950 else 175, title, body)
    for y, q, title in [(245, "q01", "<question A>"), (490, "q02", "<question B>")]:
        path([(1100, y + 70), (1260, y + 70)])
        text(1140, y + 25, "anchors", 19)
        card(1280, y, 960, 175, f"{q}  Question + its Report: one identity",
             f"Question: {title}\nReport: current answer | Evidence | Limits | Next\nWork: links to Jobs, Tasks and Runs when needed")
    note(1280, 725, "n of N frames have primary Question links; n <= N")
    text(1280, 780, "Default: one primary frame per Question.\nA Question can cite extra supporting frames.\nBackground frames can feed several Reports.", 23)
    note(1280, 900, "qNN is the pair's identity; rNN remains a Run")
    text(1280, 945, "A frame is a visual source. A Question names what to answer.\nIts Report records what we can say now.\nThey are linked, so drawing and answering stay together.", 21)
    text(0, 1180, "Shared across themes and levels: a Block's Studio holds shared thinking; a Job or Task holds its own.", 22)
    text(0, 1225, "This shared contract belongs at Block-level Studio; a new Job is useful only for a bounded implementation goal.", 22)
    text(0, 1310, "Changes in this drawing", 24)
    for i, change in enumerate(CHANGES):
        note(0, 1360 + i * 32, change)
    L.close_frame(fr)
    return fr


def frame_linked_panels():
    fr = L.open_frame("7 · Linked Studio and Report panels")
    text(0, 0, "One workspace, two linked panels", 36)
    text(0, 58, "UI proposal: stay on the canvas while a Question and its current answer open beside it.", 23)
    sx, sy, sw, sh = 0, 145, 2360, 890
    base("rectangle", sx, sy, sw, sh, INK, 1.5)
    text(24, sy + 18, "Guide    [ Block ]    Job    Task", 22)
    text(24, sy + 72, "Description    [ Idea Studio + Audience Report ]    Work Details    Runs    Delivery", 22)
    path([(0, sy + 120), (sw, sy + 120)], arrow=False)
    path([(1280, sy + 120), (1280, sy + sh)], arrow=False)
    path([(2080, sy + 120), (2080, sy + sh)], arrow=False)
    text(24, sy + 148, "Studio  s01-<topic>      Frames: A | B | C | ... | N", 23)
    text(1304, sy + 148, "Question + Report  q01    [collapse]", 23)
    text(2104, sy + 148, "Runs", 23)
    base("rectangle", 24, sy + 212, 1224, 604, INK, 1.5)
    card(60, sy + 252, 760, 348, "Frame A · <question A>     [ q01 ]",
         "<the question we are trying to answer>\n\n<ideas and alternatives drawn here>\n\n<evidence, notes and human marks>")
    base("rectangle", 62, sy + 252, 756, 344, INK, 3)
    card(865, sy + 252, 335, 210, "Frame B   [q02]", "<another question>\n<its own ideas>")
    card(865, sy + 500, 335, 210, "Frame C", "<background>\nno Question yet")
    text(60, sy + 760, "Draw here; this is the shared source canvas.", 22)
    text(1304, sy + 212, "Question: <question A>", 24)
    text(1304, sy + 254, "State: partial    Source: s01 / Frame A [locate]", 21)
    path([(1304, sy + 305), (2056, sy + 305)], arrow=False)
    text(1304, sy + 340, "Answer\n<what we can say now>", 22)
    text(1304, sy + 445, "Evidence\n<cited frames and Results>", 22)
    text(1304, sy + 550, "Limits\n<what is still uncertain>", 22)
    text(1304, sy + 655, "Next\n<the next useful question or work>", 22)
    text(1304, sy + 784, "Figure: view generated from selected source frames", 20)
    text(2104, sy + 212, "run-draw-s01\n\nSave session\n\nrun-report-q01\n\nWrite / review", 18, INK, MONO)
    text(24, sy + 850, "Selection: Frame A <-> q01      Keep the canvas position when switching between Questions.", 22)
    note(0, 1080, "Linked panels are proposed; this drawing does not implement the live UI")
    text(0, 1140, "Select a linked frame -> open its Question and Report. Select a Question -> locate its primary frame.", 23)
    text(0, 1180, "Collapse the right panel to keep exploring; a new unlinked frame stays in the Studio until a Question emerges.", 23)
    text(0, 1220, "Both panels use the same source link. A work session is saved once, as a pass of run-draw-sNN.", 23)
    text(0, 1310, "On disk: the same level owns both", 26)
    text(0, 1360, "<level>/\n  studio/s01-<topic>/s01-<topic>.excalidraw\n  studio/s01-<topic>/s01-<topic>.md\n  reports/q01_<topic>/q01_<topic>.md\n  reports/q01_<topic>/q01_<topic>.excalidraw\n  runs/run-draw-s01/passes/pNN-<MMDD>/", 20, INK, MONO)
    text(920, 1395, "Studio panel: source drawing and named frames\nItem details: decided / open / feeds\nReport panel: question, current answer and source citations\nReport figure: generated output, edit its source\nOne session: ask, summary, changed files", 21)
    text(0, 1655, "? Durable frame ID + readable name, or name only? How should split or renamed frames keep their links?", 22, RED)
    L.close_frame(fr)
    return fr


def frame_answer_flow():
    fr = L.open_frame("8 · From exploration to an answer")
    text(0, 0, "Let the topic expand; promote a useful question", 36)
    text(0, 58, "A new frame does not need a Report immediately. Give it qNN when the question is worth tracking.", 23)
    card(0, 160, 550, 200, "1  Explore in s01 / Frame A", "<an idea, sketch or background>\nNo Question required yet.\nN frames can grow freely.")
    card(690, 160, 620, 200, "2  Define q01 for this primary frame", "What needs answering?\nWhat evidence could settle it?\nWhat would count as a useful answer?")
    card(1450, 160, 690, 200, "3  Develop the current answer", "Draw, compare, gather evidence.\nq01 Report can be open or partial.\nJobs / Tasks / Runs supply work and Results.")
    path([(558, 260), (678, 260)])
    path([(1318, 260), (1438, 260)])
    text(0, 460, "The Question asks. The Studio frame explores. The Report explains the current answer.", 26)
    card(0, 570, 750, 210, "Source: s01 / named Frame A", "Keep ideas and marks on the Studio canvas.\nReport's Figures list cites the source frame.\nSupporting frames may also be cited.")
    card(1040, 570, 1100, 210, "q01 Report: answer + generated presentation", "Answer | Evidence | Limits | Next\nRebuild the figure from its selected source frames.\nA diagram by itself does not make the answer complete.")
    path([(760, 660), (1028, 660)])
    text(800, 607, "format / cite", 21)
    text(0, 870, "3a  Continue exploring: the same Question can acquire a clearer answer and more evidence.", 24)
    text(0, 920, "3b  Answered: the Report meets the Question's acceptance criteria; remaining uncertainty is explicit.", 24)
    note(0, 1020, "Report is a current answer, not a second independent drawing")
    text(0, 1080, "? UI proposal: when a cited frame changes, flag its Report for review; preserve the accepted answer until reviewed.", 22, RED)
    text(0, 1135, "? When a frame contains two independent questions, split the primary frame or add a supporting reference?", 22, RED)
    text(0, 1225, "Naming remains: sNN = Studio item; qNN = Question + Report pair; rNN = computational Run.", 24)
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
    m = frame_maps(q["x"] + q["width"] + 300, q["y"])
    relationship = frame_relationship()
    panels = frame_linked_panels()
    answer = frame_answer_flow()
    # First row: today's relationship. Old frame names remain stable for existing citations.
    canvas.grid(L.els, [[relationship["id"], panels["id"], answer["id"]],
                        [a["id"], b["id"]], [c["id"], d["id"]], [m["id"], q["id"]]], gap=180)
    canvas.write(out, list(L.els), "build_s04_studio_and_report.py")


if __name__ == "__main__":
    main()
