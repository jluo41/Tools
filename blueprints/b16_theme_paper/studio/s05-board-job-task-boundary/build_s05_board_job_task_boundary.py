"""s05 · The Board, Job and Task boundary: s05-board-job-task-boundary.excalidraw, drawn by this builder (haipipe-studio).

JL 261009: the Board is venue-free and close to the work (the basic questions, the related work); the Job is
attached to one venue and decides which questions and results it reports, without calling the work; the topic
covers all three levels ("it should be the board job and task boundary"). Two lines: the venue (Board | Job) and
one Section (Job | Task). Frames in topic groups, side by side (JL 261009): the boundary (1 · the two lines, 4 · edges), the Idea
Studio (5: its screens, each topic's question), the Audience Report (2, and 6: its screens, each button explained),
how the levels talk (7); then the studio (5), the ScalingGlucose case (3), open. Black = drawn from the decision, red = open, green = changed.

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s05_board_job_task_boundary.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)
sys.path.insert(0, str(HERE.parent / "_build"))
import paper_ui as U  # noqa: E402  (the screens s11 · s12 · s13 draw; JL 261009: "like s11 and s12 and s13, you just
                      #                draw the UI out")
import textwrap  # noqa: E402

INK, RED = canvas.INK, canvas.RED      # the studio look: black; red for an open question; green notes
SANS, MONO = canvas.FONT, canvas.CODE_FONT   # Nunito and Cascadia: no hand-drawn font (JL 261009)
LINE = 28
els = []
# every change to this drawing: (date YYMMDD, what changed). Each gets a green note where it changed
# (canvas.change_note beside the changed thing) and a line in the title frame (JL 261007)
CHANGES = [("261009", "new topic: JL's rule, Board venue-free and Job venue-targeted"),
           ("261009", "renamed s05-venue-boundary -> s05-board-job-task-boundary (JL: the Board, Job and Task boundary)"),
           ("261009", "the Task column and the second line, one Section"),
           ("261009", "Block › Audience Report › Related Papers, by question (built: workbench-paper 0.34.0)"),
           ("261009", "frame 2, what each level asks (JL: each level asks different questions)"),
           ("261009", "frames 5-7: studio topics, Audience Report views, how the levels talk (JL)"),
           ("261009", "frames in topic groups, side by side, not one column (JL)"),
           ("261009", "frame 6 drawn as the workbench screens (paper_ui, as s11-s13), each button explained (JL)"),
           ("261009", "frame 5 drawn as the Idea Studio screens, each topic's question explained (JL)"),
           ("261010", "s01-s04 retired; shared ladder and all five Story/Ideation decisions carried here"),
           ("261010", "open: show Job studio topics and reports from the Board too (JL)")]

LINES = ["Board | Job · the venue: send the paper to another venue instead; whatever must change is the Job's.",
         "Job | Task · one Section: if only this Section needs it, it is the Task's; if it spans Sections, the Job's."]
BOARD = ["Board · Paper-<Name>/            venue-free, close to the work",
         "",
         "board.md ## Questions            the basic research questions",
         "reports/qNN_<question>/          each answered by the work's Results",
         "studio/s01-ideation/             the idea pool",
         "studio/sNN-story-<idea>/         the telling: identity · pitch",
         "                                 · questions · stakes · roadmaps",
         "studio/sNN-<topic>/              e.g. the paper workflow",
         "related/related.md               every related paper, by question",
         "  shown: Audience Report › Related Papers",
         "",
         "-> the work: tasks/bNN_… · discoveries/bNN_…",
         "   (the Board asks; the work's Tasks run)"]
JOB = ["Job · jNN_v<MMDD>_<desk>/         one venue, one send",
       "",
       "face ## Narrative                 which Questions, Main or ED, in order",
       "? venue/call.md                   the rules this send goes out under",
       "? studio/s01-venue-fit/           why this venue: its papers, its limits",
       "? studio/s02-narrative-cut/       the cut, the word budget per Section",
       "? studio/s03-figure-plan/         which Question each figure carries",
       "? studio/s04-response-map/        a revision: reviewer point -> Section",
       "reports/  J1-J5 · comments        the send's questions; reviewer batches",
       "delivery/                         the whole paper, built from the Tasks",
       "",
       "never runs work; picks, orders, budgets"]
TASK = ["Task · tNN_<title>/               one Section, the Abstract or a letter",
        "",
        "tNN_<title>.md  story-row         its row in the Job's ## Narrative",
        "draft/  plan · Draft sentences    its words, edited only here",
        "draft/<stem>-evidence-items.md    which Result each sentence needs",
        "draft/records/<stem>-requirement   the venue's rules, for this Section",
        "runs/ · results/                  value, display, citation Runs",
        "delivery/latex/<stem>.tex         its fragment; the Job's build reads it",
        "? studio/sNN-argument-flow/       rare: this Section's logic, drawn",
        "? reports/                        drop: a one-Section question is an ask",
        "",
        "binds Results to sentences; never asks a new question"]
# what each level asks (JL 261009: "in each three level, we might ask different questions"), with a real example
# from Paper-ScalingGlucose-NatSeries2026: (level, it asks, e.g., answered by, kept as)
ASKS = [("Board", "what is true? the science, venue-free", "q03 · does scale help further ahead?",
         "the work's Results", "reports/qNN_: Answer · Evidence · Limits · Next"),
        ("Job", "what do we tell this venue; is it ready?", "J2 · why NMI? · a reviewer's comment",
         "the cut, the venue's rules, the checks", "reports/: J1-J5 · qNN_<kind>-<MMDD>"),
        ("Task", "what does this Section's reader need?", "t03 · what changes on Monday?",
         "its sentences, bound to Results", "its Narrative row; asks in its plan")]
ASK_RULE = ("Same word, three sizes: the Board asks a topic that grows into a report; the Job asks about one send; "
            "a Task asks one reader's question, and its smaller asks stay in its plan.")
# Paper-ScalingGlucose-NatSeries2026 (branch v1009-paper-ladder): each part, where it stays or goes
MOVES = [("§1 Identity · §2 Pitch · §3 Questions", "stays", ""),
         ("§4 Stakes · §5 Evidence · §7 Task Roadmap", "stays", ""),
         ("§5.3 Related papers", "all 45, grouped by question", "? the NMI-first order, P1-P15 as NMI's own"),
         ("§6 Discovery Roadmap", "D1-D3, D5, D6", "? D4 · does this journal publish laws?"),
         ("§8 Section Narrative + compile order", "", "j01_v1009_nmi.md ## Narrative (moved 261009)"),
         ("the desk: line · the Opening sentence", "", "? j01's face and s01-venue-fit"),
         ("studio/s02-story-nmi-cgm-scaling-axes", "? s02-story-cgm-scaling-axes", ""),
         ("venue rules (the QBv12 NMI page today)", "", "? j01_v1009_nmi/venue/call.md"),
         ("the six Sections' words and evidence", "", "Tasks t00-t04, t21 in j01 (moved 261009)")]
EDGES = [["reviewer: \"add a 1B model\"",
          "  -> an ask under q01_model_or_data              the Board: it is science",
          "  -> a b04 Task runs it                          the work theme",
          "  -> j02's s04-response-map cites the Result     the Job: it only points"],
         ["t02_results needs a number no Run has made",
          "  -> its Evidence Item names the need            the Task: one Section",
          "  -> a b04 Task Run makes it (a supporting Run)   the work theme",
          "  -> t02's run-value binds it to the sentence    the Task: it binds"]]
RULES = ["The Job chooses which Questions it reports and where; it never rewords one (that forks the science per venue).",
         "A Section never asks a new research question; a gap it finds goes up as an ask under a Board Question."]
# JL 261009: "for each level's studio, what are the typical questions (topics)? and what are not? ... for each level's
# report, what are the subviews ... why we must keep it ... how does the three level's communicated with each other"
# 5 · the Idea Studio on screen at each level (JL 261009: "where is the Idea Studio, what are the typical questions
# for the Studio for each level?"): (tab, level label, its topic rows as (name, the question it thinks through, what it
# feeds); a name starting "?" is proposed, what is not a studio topic here, the run buttons as (name, it does))
STUDIO = [("Block", "Block · the paper",
           [("s01-ideation", "Which idea is this paper, and why not the others?",
             "the Board's Questions · Audience Report › Ideation"),
            ("s02-story-<idea>", "What is the telling: its identity, pitch, stakes and research questions?",
             "q00 … q06 · Audience Report › Narrative"),
            ("s03-paper-workflow", "Which work answers which question, and what is still missing?",
             "each question's Work · High-level logic + Low-level work"),
            ("? s04-related-landscape", "Where does each related paper sit against our questions, and where is the gap?",
             "Audience Report › Related Papers")],
           ["the venue fit, the Main or Extended Data cut, a reviewer map: the Job's",
            "one Section's argument flow: the Task's",
            "a report's own drawing: its reports/qNN_<question>/ folder",
            "an experiment's plots: the work's Task (tasks/b04_…)"],
           [("Redraw", "rerun each topic's builder; a person's marks are kept")]),
          ("Job", "Job · one version, one send",
           [("? s01-venue-fit", "Why this venue: what does it publish, what are its limits, does our paper fit?",
             "J2 · Why this venue?"),
            ("? s02-narrative-cut", "Which questions go in Main and which in Extended Data, in what order, "
             "with how many words each?", "J1 · the face's ## Narrative"),
            ("? s03-figure-plan", "Which question does each figure carry, within the venue's display limits?",
             "the Narrative's display column"),
            ("? s04-response-map", "A revision: which reviewer point lands on which Section, and what changes?",
             "J5 · Audience Report › Comments")],
           ["a new research question or the science's map: the Board's",
            "a figure itself: the Section's display unit",
            "the venue's rules: venue/call.md, a file, not a topic"],
           [("Redraw the paper map", "redraw the version's map of its Sections")]),
          ("Task", "Task · one Section",
           [("? sNN-argument-flow", "What does this Section claim, on which reasons, through which Bullets?",
             "its plan in draft/ · drawn with draw-logic-tree")],
           ["anything two Sections share: the Job's",
            "evidence: runs/ and results/",
            "? the Page's studio/draw/ and studio/chat/ lanes share this folder"],
           [("run-draw-<sNN>", "add a topic, redraw it, or save a session (the base's)")])]
# 6 · the Audience Report on screen at each level, every button explained (JL 261009: "for the frame 6, I want you
# to show the workbench UI for that, and for each button you will explain them"): (tab, level label, the view drawn
# open, its view buttons as (name, it shows, why the writing needs it), the open view's run buttons as (name, it does),
# the open view's placeholder content)
AR = [("Block", "Block · the paper", "High-level logic + Low-level work",
       [("Ideation", "the ideas, ranked, admitted and eliminated (studio/s01-ideation)",
         "why this paper and not another: the Introduction's choice, the Discussion's alternatives"),
        ("Narrative", "the telling: its identity, pitch and stakes (studio/sNN-story-<idea>)",
         "the one-minute story every Section is cut from"),
        ("High-level logic + Low-level work", "each research question: hypothesis, claim and contribution beside the "
         "work that tests it (Block › Job › Task › Run) and its report", "no claim leaves without its Result: the Results"),
        ("Related Questions", "the questions a reviewer, coauthor, editor or reader will ask (board.md ## Questions, "
         "grouped by who asks)", "the objections the paper must survive: the Discussion and its limits"),
        ("Related Papers", "the related work under the research question each bears on",
         "the gap and the citations: the Introduction and the Discussion")],
       [("Claim review", "judge a claim against its evidence, its bounds and its open risks"),
        ("Task review", "review the question's Task Roadmap row and its study plan"),
        ("Write the report", "from the closed Runs: what they show, which claims follow"),
        ("Review the report", "check every number against its Result: answered or partial"),
        ("Rebuild report drawing", "redraw the report's one drawing from its figure list"),
        ("Task runs", "open or continue the work Task that answers the question"),
        ("Discovery runs", "open or continue the literature reading that answers it")],
       "logic"),
      ("Job", "Job · one version, one send", "Draft-Main",
       [("Questions", "J1-J5 (the one-minute story, why this venue, the writing principles, ready to send, what "
         "changed) and the version's own", "whether this send can go out"),
        ("Draft-Main", "each Main Section in reading order: its reader question, the claims it carries, its state; "
         "its draft and its drawing open from the card", "the manuscript as this venue reads it"),
        ("Draft-Appendix", "the same for the Extended Data and the Supplement", "what a reviewer checks behind the main text"),
        ("Comments", "the reviewers' and the editor's points as Review Items: what each cites (R1.1), where it "
         "lands, its Run, its reply", "what the next send must answer, point by point"),
        ("Cover letter", "the letter paragraph by paragraph, with the question each answers",
         "the editor's first read; it argues for this venue")],
       [("Narrative review", "check a Section's Narrative row against its current draft"),
        ("Release a Section", "release a Section for writing (G3); a person signs it")],
       "draft"),
      ("Task", "Task · one Section", "Table",
       [("Table", "each Bullet of the plan beside its sentence and the evidence it cites",
         "every point has its words and its Result"),
        ("Reading", "the Section as prose, as its reader reads it", "does it answer its reader question?"),
        ("Questions", "the Section's own questions; ? proposed: its reader question and its asks, not reports",
         "what this Section owes"),
        ("Comments", "the review points that land on this Section", "what to fix here")],
       [],
       "table")]
# 7 · how the levels talk: (direction, what moves, the field that carries it)
TALK = [("Board -> Job", "the telling to tell; the Questions and their accepted Results", "tells: on the Job face · reports/qNN_"),
        ("Job -> Task", "one Narrative row: reader question, entry and exit state,", "story-row: on the Section face"),
        ("", "  moves, must establish and refuse, evidence, display", ""),
        ("Job -> Task", "the venue's rules for this Section", "draft/records/<stem>-requirement.md"),
        ("Task -> Job", "its LaTeX file for the build; ready or not", "delivery/latex/<stem>.tex · its CHECK -> J4"),
        ("Task -> Task", "one Section's exit state is the next one's entry state", "## Narrative entry and exit columns"),
        ("Task -> Board", "a gap: an ask under a Board Question", "? no field yet"),
        ("Job -> Board", "a reviewer's new science: an ask; the send's outcome", "responds-to: · state: · ? no field for the ask"),
        ("Job -> Board", "which Questions each Section carries", "? the row names claims C1-C5, not Q01-Q06"),
        ("Board, Task <-> work", "the Questions ask; the Results come back", "Evidence Items' Supporting Runs · a report's Evidence")]
OPEN = ["? the two lines, proposed: the venue (Board | Job) and one Section (Job | Task)",
        "? frame 2, proposed: each level asks its own kind of question, answered by its own kind of thing",
        "? venues/ into the Job: s11 (Block › Description › Venue) and Q02's hypothesis put it on the Board",
        "? a telling's name: sNN-story-<desk>-<idea> -> sNN-story-<idea> (haipipe-paper-story, paper_ladder.py)",
        "? the Job's standard topics: s01-venue-fit · s02-narrative-cut · s03-figure-plan · s04-response-map",
        "? Task-level reports/: haipipe-question calls a one-Section question too narrow; drop them?",
        "? a Task's studio/: only sNN-argument-flow, when a Section's logic needs drawing?",
        "? on screen: the Venue view moves from Block › Description to Job › Description",
        "? the Board's Related view: by question only, the target venue's papers shown in the Job",
        "? frames 5-7, proposed: the studio topics, the report views and how the levels talk",
        "? a Questions column in the Job's ## Narrative, so each Section names the Board Questions it carries",
        "? a field for an ask sent up (a Section's gap, a reviewer's new science) under a Board Question",
        "? the Block's Narrative view and the Job's ## Narrative share a name: call the Block's view Story?",
        "? a Task's studio/: the ladder's sNN topics and the Page's draw/ and chat/ lanes in one folder",
        "? JL 261010: show Job studio topics and reports from the Block; keep Job/version labels and one owner",
        "? all Jobs or a selected version; Task items too? This is proposed, not built",
        "? carried from s04: old Story readers and an earlier telling's sent and judged questions"]


def el(kind, x, y, w, h, **extra):
    e = {"id": f"e{len(els)}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
          "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
          "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
          "roundness": None, "seed": 1, "version": 1, "versionNonce": 1, "isDeleted": False,
          "boundElements": [], "updated": 1, "link": None, "locked": False}
    e.update(extra)
    els.append(e)
    return e


def text(x, y, s, size=20, frame=None, color=INK, font=SANS):
    lines = s.split("\n")
    w = 0.6 if font == MONO else 0.55
    return el("text", x, y, max(len(l) for l in lines) * size * w, len(lines) * size * 1.25, text=s,
              originalText=s, fontSize=size, fontFamily=font, textAlign="left", verticalAlign="top",
              containerId=None, autoResize=True, lineHeight=1.25, frameId=frame, strokeColor=color)


def _split(line):
    """A box line `<path>   <words>` → (path, words); an indented line with no path continues the words
    column (None); any other line is all words ('')."""
    parts = re.split(r"\s{3,}", line.strip(), maxsplit=1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return (None if line.startswith("   ") else ""), line.strip()


def box(x, y, lines, frame, size=16, code=True):
    """A lines-only box: each line's path in Cascadia (`code`; else Nunito too), its words in Nunito, in two
    columns; a line starting "?" is red. Returns (right, bottom)."""
    rows = [_split(l) for l in lines]
    left = max((len(a) for a, _ in rows if a), default=0) * size * 0.6 + 30
    w = max((left if a else 0) + len(b) * size * 0.52 for a, b in rows) + 50
    h = 24 + len(lines) * LINE
    el("rectangle", x, y, w, h, frameId=frame, roughness=0)
    for i, (l, (a, b)) in enumerate(zip(lines, rows)):
        color = RED if l.startswith("?") else INK
        if a:
            text(x + 20, y + 12 + i * LINE, a, size, frame, color, MONO if code else SANS)
        text(x + 20 + (0 if a == "" else left), y + 12 + i * LINE, b, size, frame, color, SANS)
    return x + w, y + h


def arrow(x0, y0, x1, y1, frame, label=""):
    el("arrow", x0, y0, x1 - x0, y1 - y0, frameId=frame, strokeWidth=2, points=[[0, 0], [x1 - x0, y1 - y0]],
       lastCommittedPoint=None, startBinding=None, endBinding=None, startArrowhead=None, endArrowhead="arrow")
    if label:
        text(min(x0, x1) + 10, min(y0, y1) - 30, label, 16, frame)


def frame(y, h, name, w=3000):
    return el("frame", 0, y, w, h, name=name)


def table_frame(title, heads, cols, rows, size=17, step=40):
    """A frame holding one lines-only table, drawn at the origin: a header, a rule as wide as the table, then
    one row per line; a cell starting "?" is red. Returns the frame."""
    f = frame(0, 10, title)
    text(40, 40, title, 28, f["id"])
    for c, h in zip(cols, heads):
        text(c, 100, h, 18, f["id"])
    width = max(c + len(cell) * size * 0.55 for row in rows + [heads] for c, cell in zip(cols, row)) - 40
    el("line", 40, 130, width, 0, frameId=f["id"], points=[[0, 0], [width, 0]], lastCommittedPoint=None,
       startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None, roughness=0)
    for i, row in enumerate(rows):
        for c, cell in zip(cols, row):
            if cell:
                text(c, 146 + i * step, cell, size, f["id"], RED if cell.startswith("?") else INK, SANS)
    return f


def fit(fr, pad=50):
    """The frame drawn around what it holds."""
    kids = [e for e in els if e.get("frameId") == fr["id"]]
    x0, y0 = min(e["x"] for e in kids), min(e["y"] for e in kids)
    x1, y1 = max(e["x"] + e["width"] for e in kids), max(e["y"] + e["height"] for e in kids)
    fr.update(x=x0 - pad, y=y0 - pad, width=x1 - x0 + 2 * pad, height=y1 - y0 + 2 * pad)


def move(fr, x, y):
    """A fitted frame's top-left to (x, y), what it holds with it."""
    dx, dy = x - fr["x"], y - fr["y"]
    for e in els:
        if e is fr or e.get("frameId") == fr["id"]:
            e["x"], e["y"] = e["x"] + dx, e["y"] + dy


def frame_boundary():
    """1 · the two lines and what each level holds, with the topic's title and its change notes."""
    f = frame(0, 10, "1 · two lines: the venue, one Section (JL 261009)")
    text(40, 40, "s05 · The Board, Job and Task boundary", 36, f["id"])
    for i, l in enumerate(LINES):
        text(40, 100 + i * 34, l, 22, f["id"])
    for i, (date, what) in enumerate(CHANGES):          # the title frame's list of changes
        els.append(canvas.change_note(40, 180 + i * 26, what, date, f["id"]))
    top = 180 + len(CHANGES) * 26 + 50          # below the change notes
    r1, _ = box(40, top, BOARD, f["id"])
    jx = r1 + 220
    r2, _ = box(jx, top, JOB, f["id"])
    tx = r2 + 220
    box(tx, top, TASK, f["id"])
    arrow(r1 + 20, top + 150, jx - 20, top + 150, f["id"], "the venue")
    text(r1 + 30, top + 166, "Questions,\naccepted Results", 15, f["id"])
    arrow(r2 + 20, top + 150, tx - 20, top + 150, f["id"], "one Section")
    text(r2 + 30, top + 166, "its row: which\nQuestion, where,\nhow many words", 15, f["id"])
    return f


def frame_asks():
    """2 · what each level asks."""
    f = table_frame("2 · what each level asks (proposed)", ("level", "it asks", "e.g. in ScalingGlucose", "answered by",
                    "kept as"), (40, 200, 720, 1280, 1760), ASKS, step=48)
    text(40, 160 + len(ASKS) * 48, ASK_RULE, 20, f["id"])
    return f


def frame_edges():
    """4 · two cases at the edges, and the two rules they show."""
    f = frame(0, 10, "4 · edges")
    text(40, 40, "4 · edges", 28, f["id"])
    x = 40
    for e in EDGES:
        x, _ = box(x, 100, e, f["id"], code=False)
        x += 120
    for i, rule in enumerate(RULES):
        text(40, 300 + i * 36, rule, 20, f["id"])
    return f


def _content(kind, cx, cy, cw):
    """The open view's placeholders, as s11 · s12 · s13 draw them."""
    if kind == "logic":
        U.table(cx, cy, cw, ["question", "logic: hypothesis · claim", "work: Block › Job › Task › Run", "report"],
                (0, 250, 560, 880), [("Q01 · <question>", "H1 · C1 <claim>", "b04 › j01 › t02 › r01", "answered ✓"),
                                     ("Q02 · <question>", "H2 · C2 <claim>", "b04 › j01 › t02 › r02", "partial"),
                                     ("Q03 · <question>", "H3 · C3 <claim>", "? no work yet", "open")], mono=(2,))
    elif kind == "draft":
        y = U.card(cx, cy, cw, "t01_introduction · <its reader question>", "carries C0 · written · CHECK ✓")
        y = U.card(cx, y, cw, "t02_results · <its reader question>", "carries C1 · C2 · C3 · drafting")
        U.card(cx, y, cw, "t03_discussion · <its reader question>", "carries C2 · C3 · planned")
    else:
        U.table(cx, cy, cw, ["Bullet", "its sentence", "its evidence"], (0, 300, 820),
                [("B1 · <point>", "\"<the sentence>\"", "E01-VALUE ✓"), ("B2 · <point>", "\"<the sentence>\"", "E02-CITE draft"),
                 ("B3 · <point>", "? no sentence yet", "—")])


def _marker(x, y, label, f):
    """A small numbered (or lettered) circle, the key from a button to its explanation."""
    el("ellipse", x, y, 26, 26, frameId=f, strokeWidth=1.5)
    text(x + (8 if len(label) == 1 else 4), y + 3, label, 15, f)


def frame_studio():
    """5 · the Idea Studio as the workbench shows it at each level (paper_ui.screen, the s11-s13 screens): one
    folding row per topic, the first open on its drawing; each row numbered and each run button lettered, and
    beside the screen the question each topic thinks through, what it feeds, and what is not a topic here."""
    f = frame(0, 10, "5 · the Idea Studio on screen, topic by topic")
    text(40, 40, "5 · the Idea Studio on screen at each level: its typical topics, and what is not one", 28, f["id"])
    y = 110
    for tab, label, topics, notes, runs in STUDIO:
        text(40, y, f"{label} · Idea Studio", 24, f["id"])
        sy = y + 50
        start = len(U.L.els)
        cx, cy, cw = U.screen(40, sy, tab, "Idea Studio", None, runs=[r[0] for r in runs])
        rows, ry = [], cy
        for k, (name, _, _) in enumerate(topics):
            red = name.startswith("?")
            rows.append(ry)
            ry = U.card(cx, ry, cw, name.lstrip("? "), "decided · open · sessions · feeds its Questions",
                        red=red, mark="▾" if k == 0 else "▸")
            if k == 0:
                ry = U.drawing_box(cx + 20, ry, cw - 40, 220, "[ its drawing, live: the person draws, the builder redraws ]")
        for e in U.L.els[start:]:                      # the screen joins this frame, drawn straight
            e.update(id=f"u{len(els)}", frameId=f["id"], roughness=0)
            els.append(e)
        del U.L.els[start:]
        for k, ty in enumerate(rows):
            _marker(cx - 20, ty - 12, str(k + 1), f["id"])
        rx = 40 + U.SW - U.RW + 20
        for k, _ in enumerate(runs):
            _marker(rx - 18, sy + 176 + k * 54 - 14, "abcdefgh"[k], f["id"])
        ex, ey = 40 + U.SW + 100, sy                   # the explanation column
        text(ex, ey, "the topics: the question each thinks through", 22, f["id"])
        ey += 44
        for k, (name, question, feeds) in enumerate(topics):
            red = name.startswith("?")
            _marker(ex, ey, str(k + 1), f["id"])
            text(ex + 40, ey, name.lstrip("? ") + ("   (proposed)" if red else ""), 20, f["id"], RED if red else INK)
            ey += 32
            for line in textwrap.wrap(question, 96):
                text(ex + 40, ey, line, 17, f["id"])
                ey += 25
            text(ex + 40, ey, "feeds: " + feeds, 16, f["id"])
            ey += 42
        text(ex, ey, "not a studio topic here", 22, f["id"])
        ey += 40
        for n in notes:
            text(ex + 20, ey, "· " + n.lstrip("? "), 16, f["id"], RED if n.startswith("?") else INK)
            ey += 26
        ey += 20
        text(ex, ey, "the run buttons", 22, f["id"])
        ey += 44
        for k, (name, does) in enumerate(runs):
            _marker(ex, ey, "abcdefgh"[k], f["id"])
            text(ex + 40, ey + 2, f"{name}: {does}", 17, f["id"])
            ey += 38
        y = max(sy + U.SH, ey) + 120
    return f


def frame_screens():
    """6 · the Audience Report as the workbench shows it at each level (paper_ui.screen, the s11-s13 screens),
    each view button numbered and each run button lettered, explained beside the screen."""
    f = frame(0, 10, "6 · the Audience Report on screen, button by button")
    text(40, 40, "6 · the Audience Report on screen at each level, every button explained", 28, f["id"])
    y = 110
    for tab, label, open_view, views, runs, kind in AR:
        text(40, y, f"{label} · Audience Report, {open_view} open", 24, f["id"])
        sy = y + 50
        start = len(U.L.els)
        cx, cy, cw = U.screen(40, sy, tab, "Audience Report", U.third([v[0] for v in views], open_view),
                              runs=[r[0] for r in runs] or ["(none: this view is for reading)"])
        _content(kind, cx, cy, cw)
        for e in U.L.els[start:]:                      # the screen joins this frame, drawn straight
            e.update(id=f"u{len(els)}", frameId=f["id"], roughness=0)   # paper_ui's ids restart with each screen
            els.append(e)
        del U.L.els[start:]
        px = 40 + 24                                   # the view buttons, as paper_ui.screen() places them
        for k, (name, _, _) in enumerate(views):
            w = len(name) * 10 + 34
            _marker(px + w - 14, sy + 136 - 26, str(k + 1), f["id"])
            px += w + 12
        rx = 40 + U.SW - U.RW + 20
        for k, _ in enumerate(runs):
            _marker(rx - 18, sy + 176 + k * 54 - 14, "abcdefgh"[k], f["id"])
        ex, ey = 40 + U.SW + 100, sy                   # the explanation column
        text(ex, ey, "the view buttons", 22, f["id"])
        ey += 44
        for k, (name, shows, why) in enumerate(views):
            _marker(ex, ey, str(k + 1), f["id"])
            text(ex + 40, ey, name, 20, f["id"])
            ey += 32
            for line in textwrap.wrap("shows: " + shows, 96):
                text(ex + 40, ey, line, 16, f["id"], RED if "? " in line else INK)
                ey += 24
            for line in textwrap.wrap("the writing needs it: " + why, 96):
                text(ex + 40, ey, line, 16, f["id"])
                ey += 24
            ey += 18
        ey += 10
        text(ex, ey, "the run buttons of the open view" if runs else "no run buttons here: the Audience Report is for "
             "reading; a Section's Runs are in Work Details", 22 if runs else 18, f["id"])
        ey += 44
        for k, (name, does) in enumerate(runs):
            _marker(ex, ey, "abcdefgh"[k], f["id"])
            text(ex + 40, ey + 2, f"{name}: {does}", 17, f["id"])
            ey += 38
        y = max(sy + U.SH, ey) + 120
    return f


def frame_open():
    f = frame(0, 10, "open")
    for i, o in enumerate(OPEN):
        text(40, 40 + i * 40, o, 20, f["id"], RED)
    return f


def frame_ladder():
    f = table_frame("8 · the shared ladder, carried from s01; current paper names",
                    ("level", "what it holds", "folder"), (40, 350, 1160),
                    [("Board / Block", "one venue-free paper; research questions and tellings", "Paper-<Name>/"),
                     ("Job", "one version for one venue; Section order and comments", "jNN_v<MMDD>_<desk>/"),
                     ("Task", "one Section, Abstract or letter; its writing and evidence", "tNN_<title>/"),
                     ("Run", "one execution under its own level; paper Runs are soft", "runs/run-<type>-<target>/")], step=48)
    y = 370
    text(40, y, "Six Spaces at each level: Description · Idea Studio · Audience Report | Work Details | Runs · Delivery", 18, f["id"])
    text(40, y + 42, "Work Details opens the children: Board -> version Jobs -> Section Tasks; Runs stay with their owner.", 18, f["id"])
    text(40, y + 84, "Scientific work runs in the Project's work/discovery Tasks; the paper selects and cites its Results.", 18, f["id"])
    text(40, y + 134, "261010 · s01's useful overview kept; j00_story and the old Section names retired", 18, f["id"], canvas.GREEN)
    return f


def frame_story_homes():
    f = table_frame("9 · Story and Ideation homes: all five s04 decisions carried into s05",
                    ("decision", "what belongs here", "home / action"), (40, 280, 1130),
                    [("s04-D01", "Story and Ideation cease being Pages", "Board: board.md · studio/ · reports/ · runs/"),
                     ("s04-D02", "Ideation; each telling's identity, pitch and stakes", "studio/s01-ideation/ · studio/sNN-story-<telling>/"),
                     ("s04-D03", "Research questions, their answers and supporting work", "board.md ## Questions · reports/qNN_<question>/"),
                     ("s04-D04", "Story and Ideation skills stay callable from both views", "write a topic or register a Question"),
                     ("s04-D05", "Section Narrative and compile order belong to each version", "version face ## Narrative; build reads its order")], step=48)
    text(40, 430, "261010 · decisions kept as s05-D06-D10, with their original s04 ids and dates", 18, f["id"], canvas.GREEN)
    text(40, 475, "s01-s04 are frozen under _archive/20261010/studio/; their topic numbers are not reused.", 18, f["id"])
    return f


def main():
    out = HERE / "s05-board-job-task-boundary.excalidraw"
    els.clear()
    f1, f2, f4 = frame_boundary(), frame_asks(), frame_edges()
    f3 = table_frame("3 · Paper-ScalingGlucose-NatSeries2026: what moves (branch v1009-paper-ladder)",
                     ("the part", "stays on the Board", "goes to j01_v1009_nmi (the Job or its Tasks)"),
                     (40, 640, 1140), MOVES, step=44)
    f5 = frame_studio()
    f6 = frame_screens()
    f7 = table_frame("7 · how the three levels talk: down, up, sideways",
                     ("direction", "what moves", "carried by"), (40, 330, 1150), TALK)
    fo = frame_open()
    f8, f9 = frame_ladder(), frame_story_homes()
    # JL 261009: "why you are keep stacking the frame from top to down, could you try to make them into different
    # groups by topic?" Groups side by side, a heading over each; the concepts on the first row
    groups = [[("the boundary: where each level ends", [f1, f4]),
               ("Idea Studio: what each level thinks on", [f5]),
               ("Audience Report: what each level asks and shows", [f2, f6])],
              [("how the levels talk", [f7]),
               ("the case: Paper-ScalingGlucose-NatSeries2026", [f3]),
               ("open: not decided yet", [fo])],
              [("the paper ladder: the shared frame", [f8]),
               ("Story and Ideation: the decided homes", [f9])]]
    y = 0
    for row in groups:
        x, row_h = 0, 0
        for title, frames in row:
            head = text(x, y, title, 44, None, RED if title.startswith("open") else INK)
            fy, gw = y + 100, head["width"]
            for fr in frames:
                fit(fr)
                move(fr, x, fy)
                fy, gw = fy + fr["height"] + 80, max(gw, fr["width"])
            x, row_h = x + gw + 300, max(row_h, fy - y)
        y += row_h + 220

    for e in canvas.off_palette(els):                    # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, els, "build_s05_board_job_task_boundary.py")
    print(f"{len(els)} elements -> {out.name}")


if __name__ == "__main__":
    main()
