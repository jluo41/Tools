"""s05 · Runs: s05-runs.excalidraw, a plain prototype in five frames.

1 · Hard and soft        the two kinds side by side, as haipipe-run states them, and a wet hard Run (open)
2 · In the folder        a Task's runs/ (hard and soft), a Block's or Job's runs/ (soft), the older layout
3 · Life of a Run        run type -> Run Spec -> runs/<run>/ -> passes -> close; when a pass, when a new Run
4 · On screen            the Runs panel beside every Space, the Runs Space on every level, a Run pop-out
Questions                what is still open

Black and gray lines, placeholders only; red marks what is open. Written through canvas.write, so
every mark a person adds survives a rebuild.

    python build_s05_runs.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402

INK, GRAY, RED, MONO, SANS = L.INK, L.GRAY, L.RED, L.MONO, L.SANS
text, box, path, base = L.text, L.box, L.path, L.base

KINDS = [  # what · hard · soft · wet (a hard Run a person carries out; proposed)
    ("name", "rNN_<slug>", "run-<type>-<target>", "rNN_<slug>"),
    ("ticket", "rNN_<slug>.sh  (or a runner's .yaml)", "run-<type>-<target>.md", "rNN_<slug>.md: the protocol"),
    ("output", "its own result/, generated", "its scope's items: draft/ studio/\nreports/ delivery/",
     "its own result/: data a person\ncollected + an observation log"),
    ("counts as", "evidence", "work, not evidence", "evidence"),
    ("where", "a work Task only", "a Block, a Job or a Task", "a work Task only"),
    ("receipt", "runtime.yaml, written by the ticket", "ledger · touched.yaml per pass", "runtime.yaml, signed by the person"),
    ("new pass", "a retry or rerun, same ticket + inputs", "one more round on the same target", "none: it cannot repeat exactly"),
    ("new Run", "new inputs, data, goal or close rule", "a new target", "a replication"),
]
TREES = [  # (title, lines)
    ("a work Task's runs/", [
        ("tNN_<task>/runs/", ""),
        ("├── r03_<slug>/", "hard"),
        ("│   ├── run.yaml", "the card: run · kind · type · target · status · passes"),
        ("│   ├── r03_<slug>.sh", "the ticket"),
        ("│   ├── config.yaml", "its frozen inputs"),
        ("│   ├── result/", "generated: metrics · tables · figures · heavy.yaml"),
        ("│   └── passes/p01-<MMDD>/", "log · runtime.yaml, one per execution"),
        ("└── run-<type>-<target>/", "soft"),
        ("    ├── run.yaml", ""),
        ("    ├── run-<type>-<target>.md", "the ticket: target · ask · close rule"),
        ("    └── passes/p01-<MMDD>/", "ask · before/after · ledger · touched.yaml"),
    ]),
    ("a Block's or a Job's runs/", [
        ("bNN_<topic>/runs/", "soft only"),
        ("├── README.md", "its run types"),
        ("├── run-draw-<sNN>/", "-> studio/sNN-<topic>/"),
        ("├── run-report-<qNN>/", "-> reports/qNN_<topic>/"),
        ("└── run-delivery-<dNN>/", "-> delivery/dNN-<...>/"),
    ]),
    ("today, the older layout", [
        ("tNN_<task>/", ""),
        ("├── runs/r03_<slug>.sh", "the ticket, beside ..."),
        ("└── results/r03_<slug>/", "... its Result, in another folder"),
        ("", ""),
        ("haipipe-project update moves it,", ""),
        ("one Block at a time", ""),
    ]),
]
QUESTIONS = [
    "? wet Runs: a protocol ticket and a person-signed receipt; add them to haipipe-run?",
    "? Block and Job Runs are soft only: where does a Job's batch launch (run-launch-<group>) go?",
    "? a hard Run's heavy output (heavy.yaml -> ProjectResult): show it on screen, or only its pointer?",
    "? the Runs Space: this level's Runs only, or rolled up from the levels below?",
    "? a soft pass: when does it close, and who writes its touched.yaml?",
    "? the older layout: when does haipipe-project update move each Project's Runs?",
]


def frame_kinds(x0, y0):
    fr = L.open_frame("1 · Hard and soft")
    text(x0, y0, "Hard and soft Runs: decided by where the output lands", 34)
    text(x0, y0 + 50, "From haipipe-run 0.31.0. The wet column is a proposal (s01-D28): a hard Run a person carries out.",
         20, GRAY)
    cols, widths = [0, 180, 700, 1230], [180, 520, 530, 520]
    y = y0 + 110
    for i, head in enumerate(["", "hard", "soft", "wet (open)"]):
        text(x0 + cols[i] + 16, y + 12, head, 22, RED if "open" in head else INK)
    y += 52
    for row in KINDS:
        path([(x0, y), (x0 + sum(widths), y)], arrow=False, color=GRAY)
        for i, cell in enumerate(row):
            text(x0 + cols[i] + 16, y + 12, cell, 17, GRAY if i == 0 else RED if i == 3 else INK,
                 MONO if ("<" in cell or "/" in cell or ".yaml" in cell) else SANS)
        y += 52 + 22 * max(c.count("\n") for c in row)       # a two-line cell makes a taller row
    path([(x0, y), (x0 + sum(widths), y)], arrow=False, color=GRAY)
    for c in cols[1:]:
        path([(x0 + c, y0 + 110), (x0 + c, y)], arrow=False, color=GRAY)
    L.close_frame(fr)
    return fr


def frame_folder(x0, y0):
    fr = L.open_frame("2 · In the folder")
    text(x0, y0, "In the folder: one Run, one folder in runs/", 34)
    text(x0, y0 + 50, "folder name = ticket stem = run.yaml run:   heavy output -> _WorkSpace/ProjectResult/<...>/<run>/",
         20, GRAY)
    x = x0
    for title, lines in TREES:
        text(x, y0 + 110, title, 22, RED if "today" in title else INK)
        for i, (line, meaning) in enumerate(lines):
            text(x, y0 + 156 + i * 28, line, 16, GRAY if "today" in title else INK, MONO)
            if meaning:
                text(x + 330, y0 + 157 + i * 28, meaning, 15, GRAY)
        x += 330 + max(len(m) for _, m in lines) * 15 * 0.55 + 120
    L.close_frame(fr)
    return fr


def frame_life(x0, y0):
    fr = L.open_frame("3 · Life of a Run")
    text(x0, y0, "Life of a Run: type -> Spec -> folder -> passes -> close", 34)
    W, H, G = 330, 64, 110
    steps = [("run type", "a button in a Space's\nRuns panel"),
             ("Run Spec", "skill (how) · agent (who)\n· signs (the person)"),
             ("runs/<run>/", "made first: ticket +\nrun.yaml status: planned"),
             ("passes/p01-<MMDD>/", "one execution, or\none round on the target"),
             ("closed", "the close rule is met;\nrun.yaml status: closed")]
    for i, (name, note) in enumerate(steps):
        x = x0 + i * (W + G)
        box(x, y0 + 110, W, H, name, 18)
        text(x, y0 + 110 + H + 10, note, 16, GRAY)
        if i:
            path([(x - G + 8, y0 + 110 + H / 2), (x - 8, y0 + 110 + H / 2)])
    px = x0 + 3 * (W + G)
    path([(px + W / 2, y0 + 110 - 8), (px + W / 2, y0 + 60), (px + W + 60, y0 + 60),
          (px + W + 60, y0 + 110 + H / 2), (px + W + 8, y0 + 110 + H / 2)], color=GRAY)
    text(px + W / 2 + 20, y0 + 30, "a rerun (hard) or one more round (soft): p02, p03 ...", 16, GRAY)
    y = y0 + 300
    text(x0, y, "a new Run instead of a pass:", 20)
    for i, line in enumerate(["hard: new inputs, data, goal or close rule  ->  r04_<slug>",
                              "soft: a new target  ->  run-<type>-<other target>",
                              "wet: a replication  ->  r05_<slug>   (?)"]):
        text(x0 + 20, y + 40 + i * 32, line, 17, RED if "?" in line else INK, MONO)
    L.close_frame(fr)
    return fr


def ui_box(x, y, w, h, title, lines, heads=None):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 20, y + 16, title, 20)
    path([(x, y + 56), (x + w, y + 56)], arrow=False, color=GRAY)
    yy = y + 72
    if heads:
        text(x + 20, yy, heads, 15, GRAY, MONO)
        yy += 30
    for line in lines:
        text(x + 20, yy, line, 16, RED if line.startswith("?") else INK, MONO)
        yy += 28


def frame_screen(x0, y0):
    fr = L.open_frame("4 · On screen")
    text(x0, y0, "On screen: a Runs panel beside every Space, a Runs Space on every level", 34)
    ui_box(x0, y0 + 110, 520, 420, "Runs panel · <Space>",
           ["[ Draw a topic ]", "[ Write the report ]", "[ Rebuild report drawing ]", "  copies the prompt;",
            "  starts nothing itself", "", "recent here:", "run-draw-s01   p02 closed", "run-report-q03 p01 open"])
    text(x0, y0 + 545, "beside every Space, at every level:\nits run types, then the recent Runs of this Space", 16, GRAY)
    ui_box(x0 + 600, y0 + 110, 1100, 420, "Block › Runs  ·  All · hard · soft · <type>",
           ["r03_<slug>        hard  fit     t02     closed  2   p02 1003",
            "run-report-q03    soft  report  q03     open    1   p01 1007",
            "run-draw-s01      soft  draw    s01     closed  2   p02 1006",
            "? from below: the Jobs' and Tasks' Runs too"],
           heads="run               kind  type    target  status  passes  last")
    text(x0 + 600, y0 + 545, "one plain list of the Runs at this level, read from each run.yaml;\n"
                             "the third row filters by kind or type", 16, GRAY)
    ui_box(x0 + 1780, y0 + 110, 700, 420, "Run pop-out · r03_<slug>",
           ["run.yaml: the card", "  kind hard · type fit · target t02", "  skill · agent · signs",
            "passes: p01 1001 failed · p02 1003 ok", "result/ preview:", "  metrics · the first figure",
            "  heavy.yaml -> ProjectResult/<...>", "soft: before/after · the ledger"])
    text(x0 + 1780, y0 + 545, "a row opens it; Preview in the Runs Space shows the same", 16, GRAY)
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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s05-runs.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    a = frame_kinds(0, 0)
    b = frame_folder(a["x"] + a["width"] + 300, 0)
    c = frame_life(0, max(a["y"] + a["height"], b["y"] + b["height"]) + 300)
    d = frame_screen(0, c["y"] + c["height"] + 300)
    frame_questions(d["x"] + d["width"] + 300, d["y"] + 40)
    canvas.write(out, list(L.els), "build_s05_runs.py")


if __name__ == "__main__":
    main()
