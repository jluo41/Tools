"""s03 · Insight methods: s03-insight-methods.excalidraw, a plain prototype in the shape of b03 s04
(JL 261007: "what is the methods? for the insight discovery? collect all the related code in the
Tools and then create the excalidraw"; "you can follow s04-studio-and-report").

1 · Three families           asking, answering, reading side by side: step, cards, skills, papers, tests
2 · From card to screen      the card files -> the renderers -> Guide › Method; red: no card reaches a run
3 · Today                    Guide › Method, Guide › Related Paper, Insight › a partition, today's UI,
                             each with "on disk" under it, and the pop-outs a ↗ opens; the proposed
                             screens are one topic per level, s11 Block · s12 Job · s13 Task
4 · The sixteen cards        each card's move, reads, returns, tests, source and the skill it names
5 · the logic tree           method -> family -> skill (its cards) -> the code that runs or checks it
Questions                    what is still open

Everything that can be read is read at build time: the cards and their skill lines, the paper
counts, the trees and tests of guide/method.md, the code files (a missing one turns red). Black
and gray lines, red marks what is open. Written through canvas.write, so every mark a person adds
survives a rebuild. methods_drawing.py beside it is another drawing: the product's own picture in
Guide › Method, written into the server.

    python build_s03_insight_methods.py [out.excalidraw]
"""
import re
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parents[4]
B03 = TOOLS / "blueprints" / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"    # the shared drawing helpers and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
from insight_ui import ALL, CARDS, FAMS, future, scratch_questions  # noqa: E402,F401  (the cards, read as the level topics read them)

INK, GRAY, RED, TEAL, MONO, SANS = L.INK, L.GRAY, L.RED, L.TEAL, L.MONO, L.SANS
text, box, path, base = L.text, L.box, L.path, L.base
TK = TOOLS / "plugins" / "haipipe-toolkit"
SERVER = TK / "servers" / "workbench-insight"
GUIDE = SERVER / "guide"
PAPERS = SERVER / "related" / "papers.md"
ASKING = TK / "skills" / "1_base" / "question" / "haipipe-question-asking"
INSIGHT = TK / "skills" / "2_theme" / "insight"
CODE = {  # the code that runs or checks a question: key -> (file, what it does)
    "check_block": (INSIGHT / "haipipe-insight-check/ref/check_block.py", "question rules: SPEC fields, agreed, power declared"),
    "check_evidence": (INSIGHT / "haipipe-insight-check/ref/check_evidence.py", "plan_problems: the plan answers its ask"),
    "run_question": (INSIGHT / "haipipe-insight/ref/run_question.py", "power_rows before any outcome, run(df, ctx), the gate"),
    "record_check": (INSIGHT / "haipipe-insight/ref/record_check.py", "a CHECK by another agent closes the page"),
}

wrap = lambda s, n: textwrap.wrap(s, n, break_on_hyphens=False) or [""]
read = lambda p: p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""
rel = lambda p: p.relative_to(TOOLS).as_posix()
nlines = lambda p: read(p).count("\n")
STEP = 1.5                                                # a wrapped line's advance, in font sizes


def lines(x, y, ls, size, color):
    """Wrapped lines, one text each, so no renderer's line height can make them overlap; returns the bottom."""
    for k, s in enumerate(ls):
        text(x, y + k * size * STEP, s, size, color)
    return y + len(ls) * size * STEP


# ── read the sources ─────────────────────────────────────────────────────────────────────────
def paper_counts():
    """{method: {classic, review, evidence}} from related/papers.md; a row serving two methods counts on both."""
    out = {}
    for line in read(PAPERS).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1].lower() in ("classic", "review", "evidence"):
            for g in cells[0].lower().split(";"):
                out.setdefault(g.strip(), {"classic": 0, "review": 0, "evidence": 0})[cells[1].lower()] += 1
    return out


def method_trees():
    """The three which-method-when trees of guide/method.md, by their first line."""
    blocks = re.findall(r"```\n(.*?)```", read(GUIDE / "method.md"), re.S)
    pick = lambda head: next((b.rstrip("\n") for b in blocks if b.startswith(head)), "(not in method.md)")
    return pick("What does the question"), pick("Does the question"), pick("How could the answer")


def tests():
    """T0-T8 from the method.md table: (id name, asks, when)."""
    out = []
    for line in read(GUIDE / "method.md").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 4 and re.match(r"T\d ", c[0]):
            out.append((c[0], c[1], c[2]))
    return out


COUNTS = paper_counts()
TESTS = tests()
TREES = dict(zip([f[0] for f in FAMS], method_trees()))
pc = lambda c: COUNTS.get(c["name"].lower(), {"classic": 0, "review": 0, "evidence": 0})


# ── 1 · three families, side by side ───────────────────────────────────────────────────────
def frame_compare(y0):
    fr = L.open_frame("1 · Three families")
    text(0, y0, f"Insight methods: {len(ALL)} cards in three families, chosen at steps 1, 3 and 5", 34)
    text(0, y0 + 50, "Every question takes the same six steps; only steps 1, 3 and 5 have a method to choose. "
                     "Read from the cards and guide/method.md at build time.", 20, GRAY)
    rows = [("step", lambda f: f"{f[2]} · " + ["Ask: Logic, in the Prototype", "", "Run each partition: Work, in the Instance", "",
                                                 "Write the page: Report, in the Instance"][f[2] - 1], INK),
            ("asks", lambda f: f[3], INK),
            ("choose by", lambda f: TREES[f[0]].split("\n")[0], INK),
            ("cards", lambda f: f"{len(CARDS[f[0]])} · " + ", ".join(c["name"].replace("By ", "") for c in CARDS[f[0]]), INK),
            ("future", lambda f: ", ".join(c["name"] for c in CARDS[f[0]] if future(c)) or "none", INK),
            ("lives in", lambda f: rel(f[4]) + "/", GRAY),
            ("skill named", lambda f: (lambda cs: f"{sum(c['skill exists'] for c in cs)} exist · "
                                                  f"{sum(not c['skill exists'] for c in cs)} proposed (no folder)")(CARDS[f[0]]), INK),
            ("papers", lambda f: (lambda s: f"{s[0]} classic · {s[1]} review · {s[2]} evidence")(
                [sum(pc(c)[k] for c in CARDS[f[0]]) for k in ("classic", "review", "evidence")]), INK),
            ("tests", lambda f: " · ".join(t[0] for t in TESTS if re.search(rf"step {f[5]}\b", t[2])), INK),
            ("recorded", lambda f: "the skill returns method:, the question file has no field" if f[2] == 1
             else "nowhere: no file names the method used", RED),
            ("on screen", lambda f: f"Guide › Method · § {(f[2] + 1) // 2 + 1} step {f[2]} in depth", TEAL)]
    cols, W = [0, 200, 860, 1520], 660
    y = y0 + 110
    for i, f in enumerate(FAMS):
        text(cols[i + 1] + 16, y + 14, f"{f[0]} {f[1]}", 20, INK)
    for label, fn, color in rows:
        y += 46
        path([(0, y), (cols[-1] + W, y)], arrow=False, color=GRAY)
        text(16, y + 14, label, 16, GRAY)
        h = 0
        for i, f in enumerate(FAMS):
            ls = wrap(fn(f), 64)
            text(cols[i + 1] + 16, y + 14, "\n".join(ls), 16, color, MONO if label == "lives in" else SANS)
            h = max(h, len(ls))
        y += (h - 1) * 20
    y += 46
    path([(0, y), (cols[-1] + W, y)], arrow=False, color=GRAY)
    for x in cols[1:]:
        path([(x, y0 + 110), (x, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


# ── 2 · from card to screen ─────────────────────────────────────────────────────────────────
def frame_flow(x0, y0):
    fr = L.open_frame("2 · From card to screen")
    text(x0, y0, "From card to screen: the methods are text the workbench shows", 34)
    text(x0, y0 + 50, "No arrow leaves the cards for a question's run: the code runs the steps, not a method.", 20, GRAY)
    y0 += 110                                             # the diagram starts under the title
    W, H = 420, 60
    src = [(f"{len(CARDS['Question-asking'])} asking cards", rel(ASKING / "methods") + "/"),
           (f"{len(CARDS['Question-answering'])} + {len(CARDS['Question-results reading'])} answer, read cards",
            rel(GUIDE / "methods") + "/{answer,read}/"),
           ("guide/method.md", "the six steps, trees, T0-T8, the card index"),
           ("related/papers.md", f"{sum(sum(v.values()) for v in COUNTS.values())} paper rows, one group each")]
    for k, (a, b) in enumerate(src):
        sy = y0 + 130 + k * 120
        box(x0, sy, W, H, a, 18)
        text(x0, sy + H + 6, b, 14, GRAY, MONO)
    rnd = (x0 + 640, y0 + 200)
    box(*rnd, 440, H, "designboard.method_cards", 18)
    text(rnd[0], rnd[1] + H + 6, "workbench-design: the card renderer insight borrows", 15, GRAY)
    pap = (x0 + 640, y0 + 470)
    box(*pap, 440, H, "related_papers.papers_page", 18)
    text(pap[0], pap[1] + H + 6, "workbench: the shared Related Paper view", 15, GRAY)
    srv = (x0 + 1260, y0 + 300)
    box(*srv, 440, H, "insightboard._render_methods", 18)
    text(srv[0], srv[1] + H + 6, "embed=methods&view=method | papers", 15, GRAY, MONO)
    scr = (x0 + 1880, y0 + 300)
    box(*scr, 380, H, "Guide › Method", 18)
    box(scr[0], scr[1] + 170, 380, H, "Guide › Related Paper", 18)
    for k in range(3):
        path([(x0 + W + 8, y0 + 160 + k * 120), (rnd[0] - 8, rnd[1] + 30)])
    path([(x0 + W + 8, y0 + 520), (pap[0] - 8, pap[1] + 30)])
    path([(rnd[0] + 448, rnd[1] + 30), (srv[0] - 8, srv[1] + 20)])
    path([(pap[0] + 448, pap[1] + 30), (srv[0] - 8, srv[1] + 44)])
    path([(srv[0] + 448, srv[1] + 30), (scr[0] - 8, scr[1] + 30)])
    path([(srv[0] + 448, srv[1] + 44), (scr[0] - 8, scr[1] + 200)])
    text(rnd[0] + 460, rnd[1] - 30, "renders each card:\nclosed head, open two columns", 15, GRAY)
    dr = (x0 + 640, y0 + 30)
    box(*dr, 440, H, "methods_drawing.py", 18)
    text(dr[0], dr[1] + H + 6, rel(HERE) + "/", 13, GRAY, MONO)
    box(x0 + 1260, y0 + 30, 440, H, "guide/methods.excalidraw", 18)
    path([(dr[0] + 448, dr[1] + 30), (x0 + 1252, y0 + 60)])
    text(dr[0] + 456, dr[1] - 4, "writes", 15, GRAY)
    path([(x0 + 1708, y0 + 60), (scr[0] + 190, y0 + 60), (scr[0] + 190, scr[1] - 8)])
    text(scr[0] + 200, y0 + 150, "the Methods\ndrawing fold", 15, GRAY)
    run = (x0 + 1260, y0 + 640)
    base("rectangle", run[0], run[1], 1000, H, RED, 1.5, dashed=True)
    text(run[0] + 16, run[1] + 18, "a question's run: run_question.py, check_block.py, record_check.py", 17, RED, MONO)
    path([(x0 + W / 2, y0 + 130 + 3 * 120 + H + 40), (x0 + W / 2, run[1] + H / 2), (run[0] - 8, run[1] + H / 2)],
         color=RED, dashed=True)
    text(x0 + W / 2 + 16, run[1] + H / 2 + 10, "? no card is read here: which method a run used is chosen by the agent, recorded nowhere",
         16, RED)
    L.close_frame(fr)
    return fr


# ── 3 · on screen ───────────────────────────────────────────────────────────────────────────
SW, SH, RW = 1500, 980, 360
SPACES = ["Guide", "|", "Scope", "Prototype", "Insight", "Check", "Delivery"]
SUB = {"Guide": ["Description", "Method", "RoadMap Draw", "Related Paper"], "Insight": ["Full", "<partition A>", "<partition B>", "Cross"]}
RUNS = {"Method": (["Add a method"], "haipipe-insight-agent\nworkbench-insight\nwrites guide/methods/<family>/"),
        "Related Paper": (["Add a paper"], "haipipe-discovery-orchestrator-agent\nhaipipe-discovery\nwrites related/papers.md"),
        "<partition A>": (["Run a partition", "Write the Data report", "Check alignment", "Pool or split"],
                          "recent: run-<type>-<target>\nclosed · p02")}


def screen(x, y, space, view):
    """One Insight workbench screen at full size: the Spaces, the views, the content, the Runs panel."""
    base("rectangle", x, y, SW, SH, INK, 1.5)
    sx = x + 24
    for sp in SPACES:
        if sp == "|":
            text(sx, y + 18, "|", 20, GRAY)
            sx += 26
            continue
        text(sx, y + 18, sp, 20, INK if sp == space else GRAY)
        if sp == space:
            path([(sx, y + 48), (sx + len(sp) * 11, y + 48)], arrow=False, color=INK)
        sx += len(sp) * 11 + 40
    vx = x + 24
    for v in SUB[space]:
        w = len(v) * 10 + 24
        if v == view:
            base("rectangle", vx - 8, y + 62, w, 36, INK, 1.5, rough=0)
        text(vx, y + 70, v, 18, INK if v == view else GRAY)
        vx += w + 14
    path([(x, y + 112), (x + SW, y + 112)], arrow=False, color=GRAY)
    path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=GRAY)
    rx = x + SW - RW + 20
    text(rx, y + 132, f"Runs · {view}", 20)
    runs, recent = RUNS[view]
    for i, r in enumerate(runs):
        base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, GRAY, 1, rough=0)
        text(rx + 12, y + 184 + i * 54, r, 17)
    text(rx, y + 176 + len(runs) * 54 + 16, recent, 14, GRAY, MONO)
    cx, cy, cw = x + 24, y + 136, SW - RW - 48
    return cx, cy, cw


def fold(cx, y, cw, title, opened=False):
    base("rectangle", cx, y, cw, 40, INK if opened else GRAY, 1, rough=0)
    text(cx + 14, y + 10, ("▾ " if opened else "▸ ") + title, 17, INK)
    return y + 48


def screen_method(x, y):
    method_body(*screen(x, y, "Guide", "Method"))


def method_body(cx, cy, cw):
    """Guide › Method's page: the folds of guide/method.md, the six steps open, three asking cards closed."""
    yy = fold(cx, cy, cw, "Methods drawing   (guide/methods.excalidraw, editable)")
    yy = fold(cx, yy, cw, "1 · The six steps", True)
    for k, (s, _) in enumerate([("1 Ask the question", ""), ("2 Plan and agree", ""), ("3 Run each partition", ""),
                                ("4 Check the run", ""), ("5 Write the page", ""), ("6 Hand off", "")]):
        text(cx + 24, yy + k * 24, s, 15, INK)
        text(cx + 260, yy + k * 24, ["asking methods · a person signs", "T0-T3 · another agent agrees", "answering methods",
                                     "T4 T7 · another agent", "reading methods · T5 T6", "a person signs · T8 in use"][k], 14, GRAY)
    yy += 6 * 24 + 12
    yy = fold(cx, yy, cw, "2 · Step 1 in depth: ask the question", True)
    for k, c in enumerate(CARDS["Question-asking"][:3]):
        base("rectangle", cx + 20, yy, cw - 40, 34, GRAY, 1, rough=0)
        e = pc(c)["evidence"]
        text(cx + 34, yy + 8, f"▸ {k + 1}  {c['name']}", 15, INK)
        text(cx + 360, yy + 9, f"tested in {e} stud{'y' if e == 1 else 'ies'}" if e else "no study tests it yet", 13,
             GRAY if e else RED)
        text(cx + 540, yy + 9, wrap(c.get("move", ""), 46)[0] + " …", 13, GRAY)
        yy += 40
    text(cx + 34, yy, f"… {len(CARDS['Question-asking']) - 3} more cards", 14, GRAY)
    yy += 34
    for t in ["3 · Step 3 in depth: run each partition", "4 · Step 5 in depth: write the page",
              "5 · Steps 2, 4, 5 and 6 in depth: checking", "6 · Why it works", "Reference"]:
        yy = fold(cx, yy, cw, t)


def screen_papers(x, y):
    cx, cy, cw = screen(x, y, "Guide", "Related Paper")
    n = sum(sum(v.values()) for v in COUNTS.values())
    text(cx, cy, f"{n} paper rows · ★ key · classic · review · evidence · with a PDF", 16, GRAY)
    yy = cy + 40
    for c in ALL[:6]:
        p = pc(c)
        text(cx, yy, c["name"].lower(), 17, INK)
        text(cx + 330, yy + 2, f"{p['classic']} classic · {p['review']} review · {p['evidence']} evidence", 14,
             GRAY if p["evidence"] else RED)
        yy += 30
        for k in range(min(1, sum(p.values()))):
            base("rectangle", cx + 20, yy, cw - 40, 30, GRAY, 1, rough=0)
            text(cx + 32, yy + 7, ("★ " if k == 0 else "") + "<Author Year> · <title> · <venue>  ↗", 14, GRAY)
            yy += 36
        yy += 6
    text(cx, yy, "… one group per method, then the tests (before / after the run)", 14, GRAY)


def screen_partition(x, y):
    cx, cy, cw = screen(x, y, "Insight", "<partition A>")
    heads, cols = ["Logic · the question", "Work · its script and run", "Report · the page"], [0, 340, 680]
    for h, c in zip(heads, cols):
        text(cx + c + 10, cy, h, 16, GRAY)
    ry = cy + 34
    for qid, level in [("D01", "Data"), ("I01", "Information"), ("K01", "Knowledge")]:
        base("rectangle", cx, ry, cw, 190, GRAY, 1, rough=0)
        for c in cols[1:]:
            path([(cx + c, ry), (cx + c, ry + 190)], arrow=False, color=GRAY)
        text(cx + 10, ry + 12, f"{qid} · <question>\n{level} · signed ✅", 15, INK)
        text(cx + cols[1] + 10, ry + 12, "scripts/<qid>.py\nruns/<dataset>_<partition>.sh\n● ok · power ok", 14, INK, MONO)
        text(cx + cols[2] + 10, ry + 12, "<page title> ↗\nAnswer: <one line>\nCHECK ✅", 15, INK)
        ry += 204
    text(cx, ry + 6, "no row says which method its question used: see s11 · s12: three method chips on each row", 14, RED)


FILES = {  # screen -> (tree line, what on screen it feeds); a path in [] is checked on disk
    "method": [
        ("servers/workbench-insight/", ""),
        ("├── guide/guide.yaml", "the Guide entry: method_doc, method_drawing, explain › method"),
        ("├── guide/method.md", "the folds: six steps, steps 1 · 3 · 5 in depth, tests, why"),
        ("├── guide/methods/answer/01-05", "the answering cards (§ 3)"),
        ("├── guide/methods/read/01-03", "the reading cards (§ 4)"),
        ("├── guide/methods.excalidraw", "the Methods drawing fold (methods_drawing.py)"),
        ("└── insightboard.py", "_render_methods, render_methods_embed"),
        ("skills/1_base/question/haipipe-question-asking/", ""),
        ("└── methods/01-08", "the asking cards (§ 2)"),
        ("servers/workbench-design/designboard.py", "method_cards: closed head, open two columns"),
        ("skills/2_theme/insight/workbench-insight/", "ref/workbench-table.md: the Add a method run"),
    ],
    "papers": [
        ("servers/workbench-insight/related/", ""),
        ("├── papers.md", "one row per paper: group = method · role · ★ key · why here"),
        ("└── papers/", "a kept PDF (none yet)"),
        ("servers/workbench/related_papers.py", "papers_page: the shared view, one group each"),
        ("skills/0_utils/table-papers/", "the Related Paper rule"),
    ],
    "partition": [
        ("bNN_<topic>_dikw/  (an Insight Block)", ""),
        ("├── meta/partitions.md · thresholds.yaml", "the third row; power.smallest_effect_pp"),
        ("├── j01_data/t01_<name>/", "a row: D01"),
        ("│   ├── question.md", "Logic: ask · DIKW level · needs · partitions · power · agreed"),
        ("│   ├── scripts/ · runs/<dataset>_<partition>.sh", "Work"),
        ("│   ├── results/<run>/ · reports/<run>/", "partition_power.csv, the gated tables"),
        ("│   └── t01_<name>.md", "Report: the page, CHECK by another agent"),
        ("skills/2_theme/insight/…/ref/run_question.py", "runs a cell: power, run(df, ctx), gate"),
        ("skills/2_theme/insight/…/ref/check_block.py", "each cell's status"),
    ]}


def files(x, y, key):
    text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(FILES[key]):
        text(x, y + 44 + i * 28, line, 15, RED if line.strip("│ ").startswith("?") else INK, MONO)
        if meaning:
            text(x + 560, y + 45 + i * 28, meaning, 15, RED if "proposed" in meaning else GRAY)


def window(x, y, w, title, rows):
    """A pop-out: a title bar and its rows; a row in [] is a placeholder box."""
    h = 72 + sum(150 if r[0].startswith("[") else 26 * (r[0].count("\n") + 1) + 4 for r in rows) + 20
    base("rectangle", x, y, w, h, INK, 2, rough=0)
    text(x + 18, y + 14, "↗ " + title, 20, INK)
    text(x + w - 40, y + 12, "×", 22, GRAY)
    path([(x, y + 54), (x + w, y + 54)], arrow=False, color=GRAY)
    yy = y + 72
    for s, color in rows:
        if s.startswith("["):
            base("rectangle", x + 18, yy, w - 36, 136, GRAY, 1, dashed=True, rough=0)
            text(x + 34, yy + 56, s, 16, GRAY)
            yy += 150
        else:
            text(x + 18, yy, s, 15, color)
            yy += 26 * (s.count("\n") + 1) + 4
    return y + h


def popouts(x, y):
    text(x, y - 40, "pop-out, from a ↗", 24)
    c = next((c for c in ALL if c["name"] == "By hypothesis test"), ALL[0])
    p = pc(c)
    y = window(x, y, 900, f"{c['name']}  ·  a card, opened", [
        (f"tested in {p['evidence']} studies  ·  {c.get('file').relative_to(TK).as_posix()}", GRAY),
        ("\n".join(wrap(c.get("move", ""), 92)), INK),
        ("\n".join(wrap("reads  " + c.get("reads", "") + "   →   returns  " + c.get("returns", ""), 96)), INK),
        ("What the literature says         │  Applied to AI", INK),
        ("  Rationale · Context · Steps ·  │  The agent · Steps · Returns · Verify ·\n"
         "  Strengths · Limitations        │  AI risk · Evidence on AI · Skill", GRAY),
        (f"  skill: {c['skill']} {c['skill note']}", INK if c["skill exists"] else RED),
        ("\n".join(wrap("tested now  " + c.get("test now", "") + "   ·   in use  " + c.get("test in use", ""), 92)), INK),
        ("papers: <Author Year> ↗ · <Author Year> ↗ · …", GRAY)]) + 40
    y = window(x, y, 900, "Methods drawing  ·  full screen, editable", [
        ("[ guide/methods.excalidraw: the ladder, the six steps, the cards, the nine tests ]", GRAY),
        ("  written by methods_drawing.py, then edited on the canvas", GRAY)]) + 40
    window(x, y, 900, "<Author Year>  ·  a paper card", [
        ("<title> · <venue> · DOI ↗ · PDF", INK), ("group: by hypothesis test · role: evidence · ★", GRAY),
        ("why here: <what the paper gives the method>", GRAY)])


def frame_screens(x0, y0):
    fr = L.open_frame("3 · Today: the methods on screen")
    text(x0, y0, "Today: Guide shows the methods; a question's row does not", 34)
    text(x0, y0 + 50, "Today's Insight workbench, at the Block. The proposed screens, one topic per level: s11 Block · "
                      "s12 Job · s13 Task.", 20, GRAY)
    for i, (label, fn, key) in enumerate([("Guide › Method", screen_method, "method"),
                                          ("Guide › Related Paper", screen_papers, "papers"),
                                          ("Insight › <partition A>", screen_partition, "partition")]):
        x = x0 + i * (SW + 120)
        text(x, y0 + 110, label, 24)
        fn(x, y0 + 150)
        files(x, y0 + 150 + SH + 50, key)
    popouts(x0 + 3 * (SW + 120), y0 + 150)
    L.close_frame(fr, pad=60)
    return fr


# ── 4 · the sixteen cards ───────────────────────────────────────────────────────────────────
def frame_cards(x0, y0):
    fr = L.open_frame("4 · The sixteen cards")
    text(x0, y0, f"The {len(ALL)} cards: what each does, and the skill it names", 34)
    text(x0, y0 + 50, "Read off each card at build time. papers = classic · review · evidence (red: no study tests it). "
                      "Dashed = status: future. Red skill = proposed, no folder yet.", 20, GRAY)
    CW, CG, top = 600, 30, y0 + 120
    cols = [("Question-asking · step 1", CARDS["Question-asking"][:4]), (None, CARDS["Question-asking"][4:]),
            ("Question-answering · step 3", CARDS["Question-answering"]),
            ("Question-results reading · step 5", CARDS["Question-results reading"])]
    for ci, (head, cs) in enumerate(cols):
        x = x0 + ci * (CW + CG)
        if head:
            text(x, top, head, 20, INK)
            w = (2 * CW + CG) if ci == 0 else CW
            path([(x, top + 32), (x + w, top + 32)], arrow=False, color=INK)
        cy = top + 52
        for c in cs:
            p, fut = pc(c), future(c)
            rows = [("move", wrap(c.get("move", ""), 70), 14, INK), ("reads", wrap(c.get("reads", ""), 64), 13, INK),
                    ("returns", wrap(c.get("returns", ""), 64), 13, INK), ("tests", wrap(c.get("test now", ""), 64), 13, INK),
                    ("in use", wrap(c.get("test in use", ""), 64), 13, INK),
                    ("from", wrap(re.sub(r",[^;]*", "", c.get("comes from", "")).replace(";", " ·"), 64), 13, GRAY),
                    ("skill", wrap(c["skill"] + ("" if c["skill exists"] else "  (proposed)"), 64), 13,
                     INK if c["skill exists"] else RED)]
            note = wrap("future: " + c["status"].split(":", 1)[1].strip(), 76) if fut else []
            h = 64 + sum(len(r[1]) * r[2] * STEP + 8 for r in rows) + len(note) * 12 * STEP + (8 if fut else 0)
            base("rectangle", x, cy, CW, h, GRAY if fut else INK, 1, dashed=fut, rough=0)
            text(x + 14, cy + 12, c["name"], 18, INK)
            ptxt = f"papers {p['classic']} · {p['review']} · {p['evidence']}"
            text(x + CW - len(ptxt) * 13 * 0.55 - 20, cy + 16, ptxt, 13, GRAY if p["evidence"] else RED)
            text(x + 14, cy + 38, c["file"].name, 12, GRAY, MONO)
            yy = cy + 60
            yy = lines(x + 14, yy, note, 12, RED) + (8 if fut else 0)
            for label, ls, size, color in rows:
                text(x + 14, yy, label, 12, GRAY)
                yy = lines(x + 84, yy, ls, size, color) + 8
            cy += h + 16
    L.close_frame(fr, pad=60)
    return fr


# ── 5 · the logic tree ──────────────────────────────────────────────────────────────────────
LINKS = {  # skill -> (code key, label); None = no code runs it
    "haipipe-insight-question": ("check_block", "question rules\nT1 · T2 · T3"),
    "haipipe-insight-evidence-plan": ("check_evidence", "the plan answers\nits ask: T0 · T1 · T2"),
    "haipipe-insight-data": ("run_question", "power, run, gate\nT3 · T4"),
    "haipipe-insight-knowledge": ("record_check", "a CHECK by another\nagent: T5 · T6"),
    "haipipe-insight": (None, "POOL · SPLIT: prose only\n(ref/partition.md)")}


def frame_tree(x0, y0):
    fr = L.open_frame("5 · the logic tree")
    text(x0, y0, "The logic tree: method → family → skill and its cards → the code that runs or checks it", 34)
    text(x0, y0 + 50, "plain line = holds  ·  arrow = runs or checks, labelled with its tests  ·  red dashed = no folder "
                      "or no code yet", 20, GRAY)
    oy, H = y0 + 150, 52
    FX, SX, CX = 420, 900, 1900
    groups = []                                           # (family, skill, exists, [card names])
    for f in FAMS:
        seen = {}
        for c in CARDS[f[0]]:
            seen.setdefault((c["skill"], c["skill exists"]), []).append(c["name"])
        groups += [(f[0], s, e, names) for (s, e), names in seen.items()]
    sy, fam_y, skill_at = oy, {}, {}
    for fam, s, e, names in groups:
        base("rectangle", x0 + SX, sy, 480, H, INK if e else RED, 1.5, dashed=not e)
        text(x0 + SX + 16, sy + 15, s, 17, INK if e else RED, MONO)
        text(x0 + SX, sy + H + 6, " · ".join(names), 14, GRAY)
        fam_y.setdefault(fam, []).append(sy)
        skill_at[(fam, s)] = sy
        sy += H + 52
    fy = {}
    for f in FAMS:
        ys = fam_y[f[0]]
        y = (ys[0] + ys[-1]) / 2
        fy[f[0]] = y
        box(x0 + FX, y, 400, H, f"{f[0]} · step {f[2]}", 16)
        mx = x0 + FX + 400 + 40
        for ky in ys:
            path([(x0 + FX + 404, y + H / 2), (mx, y + H / 2), (mx, ky + H / 2), (x0 + SX - 4, ky + H / 2)],
                 arrow=False, color=INK)
    my = (min(fy.values()) + max(fy.values())) / 2
    box(x0, my, 340, H, "guide/method.md", 17)
    text(x0, my + H + 6, "the Insight method: six steps", 15, GRAY)
    for y in fy.values():
        path([(x0 + 344, my + H / 2), (x0 + 380, my + H / 2), (x0 + 380, y + H / 2), (x0 + FX - 4, y + H / 2)],
             arrow=False, color=INK)
    # the code column
    keys = list(CODE) + ["none"]
    cy = {k: oy + i * ((sy - oy) / len(keys)) for i, k in enumerate(keys)}
    for k in CODE:
        f, what = CODE[k]
        ok = f.is_file()
        box(x0 + CX, cy[k], 480, H, f.name, 17, INK if ok else RED)
        text(x0 + CX, cy[k] + H + 6, f"{what} · {nlines(f)} lines" if ok else "missing", 14, GRAY if ok else RED)
    base("rectangle", x0 + CX, cy["none"], 480, H, RED, 1.5, dashed=True)
    text(x0 + CX + 16, cy["none"] + 16, "no code: T7 robustness · T8 replication", 16, RED)
    lane = x0 + SX + 480 + 60
    for i, ((fam, s), ky) in enumerate(skill_at.items()):
        if s not in LINKS:
            continue
        k, label = LINKS[s]
        ty = cy[k or "none"] + H / 2
        lx = lane + i * 26
        color, dashed = (GRAY, False) if k else (RED, True)
        path([(x0 + SX + 484, ky + H / 2), (lx, ky + H / 2), (lx, ty), (x0 + CX - 6, ty)], color=color, dashed=dashed)
        text(x0 + SX + 500, ky + H / 2 - 44, label, 13, RED if not k else GRAY)
    text(x0, sy + 40, "Steps 2, 4 and 6 have no method: their rules are the same code for every question "
                      "(check_block, check_evidence, run_question, record_check).", 18, INK)
    L.close_frame(fr)
    return fr


QUESTIONS = [
    "? record the method: method: {ask, answer, read} in question.md (frame 3b, Task), checked by check_block",
    "? who picks the methods: part of Plan the evidence (agreed with the plan), or its own Run, Pick the methods",
    "? Job › Audience Report once Work Details holds the table: the answers only (question × partition, Cross verdict)",
    "? a Job holds one DIKW level (as decided), not a topic climbing D → W: keep it",
    "? a method outside its DIKW levels (by the card's taxonomy): a red chip, or a check_block problem",
    "? the 7 proposed skills (haipipe-insight-by-<method>): build them, or keep the cards as guidance an agent reads",
    "? T7 robustness and T8 replication: a run kind each (rival analyses; the same question on the next extract)",
    "? By heterogeneity's POOL · SPLIT verdict is prose (ref/partition.md): give it code",
    "? the 3 future cards (target trial, automated insight search, pattern mining): Guide, or a backlog",
    "? answering and reading cards live in the server, asking cards in a base skill: move them to skills too",
    "? the card renderer lives in workbench-design: move method_cards to the shared base (b03 s02)",
    "? two methods drawings: guide/methods.excalidraw (the product) and this one (the design): keep both",
]


def frame_questions(x0, y0):
    return scratch_questions(x0, y0, QUESTIONS)            # loose notes, as s11-s13 draw theirs


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s03-insight-methods.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a = frame_compare(0)
    b = frame_flow(a["x"] + a["width"] + 300, 0)
    c = frame_screens(0, max(a["y"] + a["height"], b["y"] + b["height"]) + 300)
    d = frame_cards(0, c["y"] + c["height"] + 300)
    q = frame_questions(0, d["y"] + d["height"] + 300)
    frame_tree(q["x"] + q["width"] + 300, q["y"])
    canvas.write(out, list(L.els), Path(__file__).name)


if __name__ == "__main__":
    main()
