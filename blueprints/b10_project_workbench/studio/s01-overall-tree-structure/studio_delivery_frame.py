"""s01 frame 2 · Studio sNN and Block, Job, Task, Delivery: drawn into s01-overall-tree-structure.excalidraw by
build_ladder_v4.py, after frame 1 (the ladder). It was s09's one frame until s09 was merged into s01 (JL 261012:
"plesae merge the s09 to the s01"; s01-D37); s09's old builder, face and drawing are in history/.

One dense frame (JL 261010: one idea, one frame):
  left   the centre (the Block's Studio) issues down to Block, Job and Task; every level reports up;
         the Block's Delivery collects every level's output (one per Block, like the Studio)
  right  the stage of one sNN (explore · shaping · agreed · closed), its gate, b10's numbers, the index
The Delivery design frame moved to s03-delivery-workbench-skill on 261010 (JL: "have a s03
delivery-workbench-skill").

From the JL meeting of 261010 (related/meetings/2026-10-10-1800 ...md, [58:10], [73:52]): the Studio is
the centre's policy paper; Block, Job and Task are province, city and county; each one reports.

    draw(L)    L: the build_ladder_v4 module that is drawing (its els, text, path, base, open_frame)
"""
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer; build_ladder_v4 put it on sys.path)

L = None                       # the drawing module, set by draw()
# a change gets one green note beside what changed (note() below), never a list at the top (JL 261010:
# "don't always put the green comment in the left corner"); a new topic or a rename goes in the face

LEVELS = [  # (title, what it holds, its report, is the report's home settled)
    ("PROVINCE · Block  bNN_<topic>/", "board.md register · delivery/ (s02-D14)", "Block report", "reports/qNN_<topic>/"),
    ("CITY · Job  jNN_<job>/", "one line of work · its runs, results", "Job report", "jNN_<job>/reports/qNN_<topic>/"),
    ("COUNTY · Task  tNN_<task>/", "one Page · its runs, results", "Task report", "tNN_<task>/reports/qNN_<topic>/"),
]
STAGES = [  # (name, what it looks like)
    ("1  explore", "rough drawing\nmany red ?\nno plan yet"),
    ("2  shaping", "one idea frame\ndecisions growing\neach red ? has\nan owner"),
    ("3  agreed", "no red left\nOpen list empty\nJL signs\nmay build a Job"),
    ("4  closed", "its Jobs closed\nReports answered\nfrozen"),
]
B10 = [  # topic, red ?, green notes, frames: read off the drawings on 261010
    ("s21_project-run-skill", 1, 17, 6, "nearly agreed"),
    ("s01-overall-tree", 2, 0, 1, ""),
    ("s02-studio-workbench-skill", 13, 10, 9, ""),
    ("s02-studio-workbench-skill", 30, 23, 12, ""),
    ("s11-block-variants", 111, 4, 19, "two drawings"),
]


def card(x, y, w, h, title, body, size=24, body_size=21, body_color=None):
    L.base("rectangle", x, y, w, h, L.INK, 1.5)
    L.text(x + 22, y + 16, title, size)
    if body:
        L.text(x + 22, y + 16 + size * 1.25 + 14, body, body_size, body_color or L.INK)


def note(x, y, what, date="261010"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


def centre_and_levels():
    """Left: the centre issues down; every level reports up."""
    text, path = L.text, L.path
    card(0, 150, 1160, 180, "CENTRE · the Block's Studio · studio/sNN-<topic>/",
         "one copy per Block; Block, Job and Task views open the same topics (s02-D03, D09)\n"
         "it writes the plan (the drawing), the decisions sNN-DNN, and what each level reports\n"
         "a topic is a draft policy until it is agreed: see the stage of an sNN, right")
    path([(300, 338), (300, 462)])
    text(320, 380, "issues: an agreed topic builds a Job, linked back (s02-D04)", 21)
    for i, (title, holds, report, home) in enumerate(LEVELS):
        y = 470 + i * 170
        card(0, y, 600, 112, title, holds, 23, 20)
        if i:
            path([(90, y - 50), (90, y - 6)])
            text(108, y - 44, "holds", 20)
        path([(608, y + 56), (712, y + 56)])
        text(616, y + 20, "writes", 20)
        card(720, y, 440, 112, report, home, 23, 20, L.RED if home.startswith("?") else L.INK)
        if i:                                          # settled 261010: each level's own reports/
            note(742, y + 84, "in its own folder (s09-D08)")     # inside its card, under the path
    path([(1168, 866), (1230, 866), (1230, 270), (1168, 270)])
    text(720, 936, "reports go up: to read one, go to its level ([58:26])", 21)
    path([(300, 930), (300, 1002)])
    text(320, 950, "every level's output, filed by its source", 21)
    card(0, 1010, 1160, 150, "OUT · the Block's Delivery · delivery/  (one per Block, like the Studio)",
         "Block outputs: delivery/<lane>/ · Job and Task outputs keep their source: delivery/jNN_<job>/tNN_<task>/<lane>/\n"
         "Job and Task views show their own part; the Block shows all (s02-D14)", 24, 20)
    note(0, 1172, "Delivery is Block-level, the same as the Studio (JL)")
    note(0, 1196, "each subfolder links back to its source: jNN_<job>/ to the Job folder, jNN/tNN/ to the Task folder (JL)")
    text(0, 1222, "later: what each kind of Block, Job and Task must report: the centre writes it ([74:18])", 21)
    note(0, 1258, "agreed: the open ? moved to Later (s09-D09)", "261011")


def stage_and_index():
    """Right: the stage of one sNN, its gate, b10's numbers, and the index that shows them."""
    text, path = L.text, L.path
    x0 = 1340
    path([(1168, 190), (x0 - 10, 190)])
    text(x0, 150, "STAGE of one sNN: a person moves it, the gate only counts", 25)
    w, gap = 265, 40
    for i, (name, body) in enumerate(STAGES):
        x = x0 + i * (w + gap)
        card(x, 210, w, 220, name, body, 24, 20)
        if i:
            path([(x - gap + 6, 320), (x - 6, 320)])
    text(x0, 470, "Gate, counted by new_topic.py check (proposed): it reports, it never moves the stage", 22)
    text(x0, 510, "red ? left on the drawing · items in Open · dated decisions · frame checks\n"
                  "moving the stage = one line  Stage: agreed  in the face + one decision row sNN-DNN", 20)
    text(x0, 610, "b10 on 261010: red ? · green notes · frames (the gate's inputs)", 22)
    rows = "\n".join(f"{t:<24}{r:>4}{g:>6}{f:>6}   {n}" for t, r, g, f, n in B10)
    text(x0, 650, rows, 20, L.INK, L.MONO)
    card(x0, 830, 1180, 250, "INDEX · SPACE home, radial view, size by Studio topics",
         "colour each sNN by its stage; a Block shows its topics' stages\n"
         "Current (what we work on now) drawn bold; everything else plain\n"
         "the centre sees at a glance what is moving and what is not", 24, 21)
    text(x0 + 22, 1030, "later: Current lives in one browser; the index cannot read it: move it to a file in the Block", 20)
    note(x0, 1088, "List · Index: each Block folds open to its Studio and Job rows, each opening its drawing or face (s01-D38)",
         "261012")
    note(x0 + 22, 992, "Guide: SPACE and Project link here; ?project= shows one Project (s01-D39)", "261012")
    text(x0, 1120, "later: does the 10-topic cap count only explore and shaping topics (b10 had 16 on 261010, 12 on 261012)", 21)
    text(x0, 1160, "later: a deliverable that crosses Blocks (a meeting deck): its own Block, as a paper Board is?", 21)
    note(x0, 1196, "agreed: the open ? moved to Later (s09-D09)", "261011")


def draw(module):
    """Frame 2 of s01's drawing; returns the frame."""
    global L
    L = module
    fr = L.open_frame("2 · Studio sNN and Block, Job, Task, Delivery")
    L.text(0, 0, "2 · Studio and Delivery at the Block, a report at every level (was s09)", 34)
    L.text(0, 52, "JL meeting 261010 [58:10] [73:52]: the Studio is the centre's policy paper; "
                  "Block, Job and Task are province, city and county; each one reports.", 21)
    note(0, 96, "s09 merged into s01: this was s09's frame; its decisions keep their ids, s09-D01 to D09 (s01-D37)",
         "261012")
    centre_and_levels()
    stage_and_index()
    L.close_frame(fr)
    return fr
