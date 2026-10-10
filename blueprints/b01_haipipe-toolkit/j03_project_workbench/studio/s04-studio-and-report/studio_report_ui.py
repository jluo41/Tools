"""Idea Studio and Audience Report on screen, at every level: the workbench screens drawn large.

Shared by s04-studio-and-report (its frames 3 and 4) and s11-block-variants (its close-up frames).
Every level tab (Block, Job, Task) has Idea Studio and Audience Report; Work Details, the level's
children, may be empty, and a Task has none (s04-D05). One frame per Space, one screen per level.
Draws through build_ladder_v4's helpers, so the caller's canvas.write keeps a person's marks.
"""
import build_ladder_v4 as L

SPACES = ["Description", "Idea Studio", "Audience Report", "|", "Work Details", "|", "Runs", "Delivery"]
TABS = {"Block": "Block", "Job": "Job · j11 ▾", "Task": "Task · t02 ▾"}
CHILDREN = {"Block": "Work Details = its Jobs", "Job": "Work Details = its Tasks",
            "Task": "Work Details: none (no children)"}
STUDIO_ROWS = {  # level -> rows: (topic, status, sessions, feeds); a session is a pass of run-draw-<sNN>
    "Block": [("s01-<topic>", "decided 4 · open 3", "2 sessions", "feeds Q01 · Q03"),
              ("s02-<topic>", "decided 1 · open 5", "1 session", "feeds Q03")],
    "Job": [("s01-<job-topic>", "decided 0 · open 2", "1 session", "feeds Q02")],
    "Task": [("s01-<page-logic>", "the argument", "1 session", "feeds its Page")]}
REPORT_ROWS = {  # level -> rows: (question, work, the report's answer line, its figures, the studio topics feeding it)
    "Block": [("Q01 · <question>\nanswered", "j11 · t02 · r03", "Answer: <one line>", "Fig 1 · s01 › 1",
               ["s01-<topic>"]),
              ("Q03 · <question>\nopen", "j12 · t01", "no answer yet", "Fig 1 · s01 › 1\nFig 2 · s11 › <frame>",
               ["s01-<topic>", "s02-<topic>"])],
    "Job": [("Q02 · <question>\nopen", "t01 · t02", "Answer: <draft>", "Fig 1 · s01-<job-topic> › 1",
             ["s01-<job-topic>"])],
    "Task": [("the Page\nTable · Reading", "r01\nrun-<type>-<target>", "the Page itself",
              "Fig 1 · s01-<page-logic> › 1", ["s01-<page-logic>"])]}
THIRD_ROW = {  # the Audience Report's third row: the register's Question groups; a Page Task's two views
    "Block": ["All", "<group A>", "<group B>"], "Job": ["All", "<group A>"], "Task": ["Table", "Reading"]}
ROW_GROUP = {"Block": ["<group A>", "<group B>"], "Job": ["<group A>"], "Task": [None]}   # each row's group
OPEN = {"Block": 0, "Job": None, "Task": 0}   # the studio row shown open on each tab (None: all closed)
RUNS = {"Idea Studio": ["Add a topic", "Redraw a topic", "Save this session"],
        "Audience Report": ["Ask a Question", "Rebuild report drawing", "Write the report", "Check a report"]}
RECENT = {  # the Runs panel's recent list; in Idea Studio the open topic's sessions, each a pass
    "Idea Studio": "run-draw-s01\n  p02 1007 <summary>\n  p01 1006 <summary>\nopen: the session's ask\nand what it changed",
    "Audience Report": "recent: run-<type>-<target>\nclosed · p02"}
SW, SH, RW = 1500, 760, 360          # one screen; the Runs panel inside it


def screen(x, y, level, space):
    """One workbench screen at full size: the level tabs, the Space row, the content, the Runs panel."""
    L.base("rectangle", x, y, SW, SH, L.INK, 1.5)
    tx = x + 24
    for tab in ["Guide", "Block", "Job · j11 ▾", "Task · t02 ▾"]:
        on = tab == TABS[level]
        L.text(tx, y + 18, tab, 20, L.INK if on else L.GRAY)
        if on:
            L.path([(tx, y + 48), (tx + len(tab) * 11, y + 48)], arrow=False, color=L.INK)
        tx += len(tab) * 11 + 46
    sx = x + 24
    for sp in SPACES:
        if sp == "|":
            L.text(sx, y + 70, "|", 18, L.GRAY)
            sx += 26
            continue
        w = len(sp) * 10 + 24
        if sp == space:
            L.base("rectangle", sx - 8, y + 62, w, 36, L.INK, 1.5, rough=0)
        elif sp == "Work Details" and level == "Task":
            L.base("rectangle", sx - 8, y + 62, w, 36, L.GRAY, 1, dashed=True, rough=0)
        L.text(sx, y + 70, sp, 18, L.INK if sp == space else L.GRAY)
        sx += w + 14
    L.path([(x, y + 112), (x + SW, y + 112)], arrow=False, color=L.GRAY)
    L.path([(x + SW - RW, y + 112), (x + SW - RW, y + SH)], arrow=False, color=L.GRAY)
    rx = x + SW - RW + 20
    L.text(rx, y + 132, f"Runs · {space}", 20)
    for i, r in enumerate(RUNS[space]):
        L.base("rectangle", rx, y + 176 + i * 54, RW - 40, 40, L.GRAY, 1, rough=0)
        L.text(rx + 12, y + 184 + i * 54, r, 17)
    L.text(rx, y + 176 + len(RUNS[space]) * 54 + 16, RECENT[space], 15, L.GRAY, L.MONO)
    L.text(x + 24, y + SH - 40, CHILDREN[level], 16, L.RED if level == "Task" else L.GRAY)
    cx, cy, cw = x + 24, y + 136, SW - RW - 48
    if space == "Idea Studio":
        L.text(cx, cy, "one topic per row, by name; click one and it opens in place", 16, L.GRAY)
        ry = cy + 40
        for i, (topic, status, sessions, feeds) in enumerate(STUDIO_ROWS[level]):
            opened = OPEN[level] == i
            L.base("rectangle", cx, ry, cw, 48, L.INK if opened else L.GRAY, 1, rough=0)
            L.text(cx + 14, ry + 12, ("▾ " if opened else "▸ ") + topic, 18, L.INK, L.MONO)
            if opened:                                 # closed rows show the name only; the details come with opening
                L.text(cx + 330, ry + 14, f"{status}  ·  {sessions}  ·  {feeds}", 16, L.GRAY)
            ry += 48
            if opened:                                 # the open row: the live drawing, the whole width
                L.base("rectangle", cx, ry, cw, 320, L.GRAY, 1, rough=0)
                L.base("rectangle", cx + 14, ry + 14, cw - 28, 292, L.GRAY, 1, dashed=True, rough=0)
                L.text(cx + 34, ry + 130, "[ the live drawing: draw here, saved as you go ]", 17, L.GRAY)
                L.text(cx + 34, ry + 270, "its sessions are passes of run-draw-<sNN>: in the Runs panel ->",
                       15, L.GRAY)
                ry += 320
            ry += 10
        L.text(cx, ry + 10, "+ Add topic  ->  studio/sNN-<topic>/", 17, L.GRAY, L.MONO)
    else:
        px = cx                                     # the third row: buttons, the selected one outlined
        for k, label in enumerate(THIRD_ROW[level]):
            w = len(label) * 10 + 34
            L.base("rectangle", px, cy - 8, w, 38, L.INK if k == 0 else L.GRAY, 2 if k == 0 else 1, rough=0)
            L.text(px + 17, cy, label, 17, L.INK if k == 0 else L.GRAY)
            px += w + 12
        heads, cols = ["Logic · the question", "Work · the Tasks and Runs", "Report · what it says"], [0, 300, 580]
        for h, c in zip(heads, cols):
            L.text(cx + c + 10, cy + 48, h, 16, L.GRAY)
        ry, last = cy + 80, None
        rows = REPORT_ROWS[level]
        for (question, work, answer, figs, topics), group in zip(rows, ROW_GROUP[level]):
            if group and group != last:             # one table per register group, as today's work workbench
                n = ROW_GROUP[level].count(group)
                L.text(cx, ry, f"{group}  ·  {n} Question{'s' if n > 1 else ''}", 17, L.INK)
                L.path([(cx, ry + 28), (cx + cw, ry + 28)], arrow=False, color=L.INK)
                ry, last = ry + 40, group
            L.base("rectangle", cx, ry, cw, 182, L.GRAY, 1, rough=0)
            for c in cols[1:]:
                L.path([(cx + c, ry), (cx + c, ry + 182)], arrow=False, color=L.GRAY)
            L.text(cx + 10, ry + 16, question, 16, L.INK)
            L.text(cx + 10, ry + 84, "from the Idea Studio:", 14, L.GRAY)      # the topics that feed it
            for k, topic in enumerate(topics):
                L.text(cx + 10, ry + 108 + k * 26, f"{topic} ↗", 15, L.INK, L.MONO)
            L.text(cx + cols[1] + 10, ry + 16, work, 15, L.INK, L.MONO)
            px = cx + cols[2] + 10                      # as today's Report cell: title, answer, one drawing, tag
            L.text(px, ry + 12, "Report", 14, L.GRAY)
            L.text(px, ry + 34, "<report title> ↗", 16, L.INK)
            L.text(px, ry + 60, answer, 15, L.GRAY)
            L.base("rectangle", px, ry + 88, 230, 66, L.GRAY, 1, dashed=True, rough=0)
            L.text(px + 10, ry + 96, "[ its drawing ] ↗", 14, L.GRAY)
            L.text(px + 246, ry + 134, "report qNN", 13, L.GRAY)
            ry += 196


FILES = {  # (space, level) -> the folders and files behind the screen: (tree line, what on screen it feeds)
    ("Idea Studio", "Block"): [
        ("bNN_<topic>/", ""),
        ("├── studio/", "the Space: one row per topic folder"),
        ("│   ├── s01-<topic>/", "a row; its name is the row's name"),
        ("│   │   ├── s01-<topic>.excalidraw", "the live drawing, when the row is open"),
        ("│   │   ├── s01-<topic>.md", "the details: decided · open · feeds: Q01 Q03"),
        ("│   │   └── build_s01_<topic>.py", "optional: seeds the drawing, keeps marks"),
        ("│   └── s02-<topic>/ …", "the next row"),
        ("└── runs/", ""),
        ("    └── run-draw-s01/", "the Runs panel: this topic's sessions"),
        ("        ├── run.yaml", "the card"),
        ("        └── passes/p01-<MMDD>/", "one session: ask · summary · what changed"),
    ],
    ("Idea Studio", "Job"): [
        ("jNN_<job>/", ""),
        ("├── studio/", "optional: a Job may have no topics"),
        ("│   └── s01-<job-topic>/", "a row"),
        ("│       ├── s01-<job-topic>.excalidraw", "the live drawing"),
        ("│       └── s01-<job-topic>.md", "decided · open · feeds: Q02"),
        ("└── runs/run-draw-s01/", "its sessions, as passes"),
    ],
    ("Idea Studio", "Task"): [
        ("tNN_<task>/", ""),
        ("├── studio/", "optional"),
        ("│   └── s01-<page-logic>/", "a row: the Page's argument"),
        ("│       ├── s01-<page-logic>.excalidraw", "the live drawing"),
        ("│       └── s01-<page-logic>.md", "feeds: its Page"),
        ("└── runs/run-draw-s01/", "its sessions, as passes"),
    ],
    ("Audience Report", "Block"): [
        ("bNN_<topic>/", ""),
        ("├── bNN_<topic>.md", "the register: Q01 · Q03 and their groups (third row)"),
        ("├── reports/", "the Space: one row per Question folder"),
        ("│   ├── q01_<topic>/", "a row"),
        ("│   │   ├── q01_<topic>.md", "Report: its title, answer line, ## Figures"),
        ("│   │   ├── q01_<topic>.excalidraw", "its drawing, generated; .png = the thumbnail"),
        ("│   │   ├── page.toml", "lets the workbench show the Page"),
        ("│   │   └── draft/", "the Page's plan and records (off screen)"),
        ("│   └── q03_<topic>/ …", "the next row"),
        ("├── studio/sNN-<topic>/sNN-<topic>.md", "feeds: -> the Question's studio links"),
        ("├── runs/run-report-q01/", "the Runs panel: Write · Check · Rebuild"),
        ("└── jNN_<job>/tNN_<task>/runs/rNN_<slug>/", "the Work column: the Runs it cites"),
    ],
    ("Audience Report", "Job"): [
        ("jNN_<job>/", ""),
        ("├── jNN_<job>.md", "its register: Q02 and its group"),
        ("├── reports/", "optional: a Job may have no Questions"),
        ("│   └── q02_<topic>/", "a row"),
        ("│       ├── q02_<topic>.md", "Report: title · answer line · ## Figures"),
        ("│       └── q02_<topic>.excalidraw", "its drawing, generated"),
        ("├── runs/run-report-q02/", "Write · Check · Rebuild"),
        ("└── tNN_<task>/runs/rNN_<slug>/", "the Work column"),
    ],
    ("Audience Report", "Task"): [
        ("tNN_<task>/", "a Page Task: its Page is its report"),
        ("├── tNN_<task>.md", "the Page: Table · Reading (third row)"),
        ("├── tNN_<task>.excalidraw", "its drawing, generated from its studio frames"),
        ("├── page.toml", ""),
        ("├── draft/", "the plan, evidence items (off screen)"),
        ("└── runs/", "r01 · run-<type>-<target>: the Work column, the Runs panel"),
    ],
}


def files(x, y, space, level):
    """Under a screen: the folders and files that back it, each with what on screen it feeds."""
    L.text(x, y, "on disk", 22)
    for i, (line, meaning) in enumerate(FILES[(space, level)]):
        L.text(x, y + 44 + i * 28, line, 16, L.INK, L.MONO)
        if meaning:
            L.text(x + 520, y + 45 + i * 28, meaning, 15, L.GRAY)


def window(x, y, w, h, title, lines):
    """A pop-out window: a title bar with its close button, then its content."""
    L.base("rectangle", x, y, w, h, L.INK, 2, rough=0)
    L.text(x + 18, y + 14, "↗ " + title, 20, L.INK)
    L.text(x + w - 40, y + 12, "×", 22, L.GRAY)
    L.path([(x, y + 54), (x + w, y + 54)], arrow=False, color=L.GRAY)
    yy = y + 72
    for line in lines:
        if line.startswith("[") and line.endswith("]"):       # a placeholder box: a drawing, a figure
            L.base("rectangle", x + 18, yy, w - 36, 150, L.GRAY, 1, dashed=True, rough=0)
            L.text(x + 34, yy + 62, line, 16, L.GRAY)
            yy += 168
        else:
            L.text(x + 18, yy, line, 16, L.INK if line and not line.startswith(" ") else L.GRAY)
            yy += 28


POPOUTS = {  # space -> windows a ↗ opens, on any tab: (title, lines)
    "Idea Studio": [("s01-<topic>  ·  the topic, full size", [
        "[ the live drawing: draw here, saved as you go ]", "sessions: run-draw-s01 › p01 1006 · p02 1007  (in the Runs panel)",
        "  feeds Q01 · Q03   ·   decided 4 · open 3", "  Redraw  ·  Save this session  ·  open the .md"])],
    "Audience Report": [
        ("Q01 · Report  ·  the Page", ["Answer", "  <the answer, a few lines>", "Evidence",
                                       "  <cited Runs and Results>", "Limits  ·  Next", "  Write the report  ·  Check a report"]),
        ("s01-<topic>  ·  from Q03's studio link", ["[ the topic's live drawing, full size ]",
                                                  "  feeds Q01 · Q03   ·   open it in Idea Studio"]),
        ("Q01 · Drawing  ·  generated, view only", ["[ Q01 · report: the heading frame ]",
                                                    "[ Fig 1 · s01 › 1 · <caption> ]",
                                                    "  from s01 › 1, built <date>", "  Rebuild  ·  Suggest  ·  open the studio frame"])],
}
PW = 900                             # a pop-out's width


def popouts(x, y, space):
    """The fourth column: the windows a ↗ in this Space opens, from any tab."""
    L.text(x, y - 40, "pop-out, from any tab's ↗", 24)
    for title, lines in POPOUTS[space]:
        h = 72 + sum(168 if l.startswith("[") else 28 for l in lines) + 20
        window(x, y, PW, h, title, lines)
        y += h + 40


def closeups(x0, y0, names=None):
    """Two frames: Idea Studio, then Audience Report, each at Block, Job and Task; returns them.
    names: {space: frame name}; default "<space> · Block, Job, Task"."""
    frames = []
    for space, note in [("Idea Studio", "the studio: rough drawings a person edits, one topic after another"),
                        ("Audience Report", "the reports: one row per Question; each Report drawing is built "
                                            "from studio frames (s04)")]:
        fr = L.open_frame((names or {}).get(space, f"{space} · Block, Job, Task"))
        L.text(x0, y0, f"{space} at every level", 34)
        L.text(x0, y0 + 50, note + ". Work Details may be empty; these two are always there.", 20, L.GRAY)
        for i, level in enumerate(["Block", "Job", "Task"]):
            L.text(x0 + i * (SW + 120), y0 + 110, f"{level} tab", 24)
            screen(x0 + i * (SW + 120), y0 + 150, level, space)
            files(x0 + i * (SW + 120), y0 + 150 + SH + 50, space, level)
        popouts(x0 + 3 * (SW + 120), y0 + 150, space)
        L.close_frame(fr, pad=60)
        frames.append(fr)
        y0 = fr["y"] + fr["height"] + 300
    return frames
