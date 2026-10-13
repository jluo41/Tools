"""s09 · Studio sNN and Block, Job, Task, Delivery: s09-studio-block-job-task-delivery.excalidraw, drawn by this builder (haipipe-studio).

One dense frame (JL 261010: one idea, one frame):
  left   the centre (the Block's Studio) issues down to Block, Job and Task; every level reports up;
         the Block's Delivery collects every level's output (one per Block, like the Studio)
  right  the stage of one sNN (explore · shaping · agreed · closed), its gate, b10's numbers, the index
The Delivery design frame moved to s03-delivery-workbench-skill on 261010 (JL: "have a s03
delivery-workbench-skill").

From the JL meeting of 261010 (related/meetings/2026-10-10-1800 ...md, [58:10], [73:52]): the Studio is
the centre's policy paper; Block, Job and Task are province, city and county; each one reports.

A rebuild keeps whatever a person drew on the canvas (canvas.write, a seed snapshot beside the drawing).

    python build_s09_studio_block_job_task_delivery.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared drawing helpers)
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import canvas  # noqa: E402  (haipipe-studio's merge-safe writer)

INK, RED, SANS, MONO = L.INK, L.RED, L.SANS, L.MONO
text, path, base = L.text, L.path, L.base
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


def card(x, y, w, h, title, body, size=24, body_size=21, body_color=INK):
    base("rectangle", x, y, w, h, INK, 1.5)
    text(x + 22, y + 16, title, size)
    if body:
        text(x + 22, y + 16 + size * 1.25 + 14, body, body_size, body_color)


def note(x, y, what, date="261010"):
    e = canvas.change_note(x, y, what, date, L.FRAME[0], 17)
    e["id"] = f"e{len(L.els)}"
    L.els.append(e)


def centre_and_levels():
    """Left: the centre issues down; every level reports up."""
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
        card(720, y, 440, 112, report, home, 23, 20, RED if home.startswith("?") else INK)
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
    text(x0, 610, "b10 today: red ? · green notes · frames (the gate's inputs)", 22)
    rows = "\n".join(f"{t:<24}{r:>4}{g:>6}{f:>6}   {n}" for t, r, g, f, n in B10)
    text(x0, 650, rows, 20, INK, MONO)
    card(x0, 830, 1180, 250, "INDEX · SPACE home, radial view, size by Studio topics",
         "colour each sNN by its stage; a Block shows its topics' stages\n"
         "Current (what we work on now) drawn bold; everything else plain\n"
         "the centre sees at a glance what is moving and what is not", 24, 21)
    text(x0 + 22, 1030, "later: Current lives in one browser; the index cannot read it: move it to a file in the Block", 20)
    text(x0, 1120, "later: does the 10-topic cap count only explore and shaping topics (b10 has 16 now)", 21)
    text(x0, 1160, "later: a deliverable that crosses Blocks (a meeting deck): its own Block, as a paper Board is?", 21)
    note(x0, 1196, "agreed: the open ? moved to Later (s09-D09)", "261011")


def main():
    out = HERE / "s09-studio-block-job-task-delivery.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    fr = L.open_frame("1 · Studio sNN and Block, Job, Task, Delivery")
    text(0, 0, "s09 · Studio sNN and Block, Job, Task, Delivery: Studio and Delivery at the Block, a report at every level", 34)
    text(0, 52, "JL meeting 261010 [58:10] [73:52]: the Studio is the centre's policy paper; "
                "Block, Job and Task are province, city and county; each one reports.", 21)
    centre_and_levels()
    stage_and_index()
    L.close_frame(fr)
    for e in canvas.off_palette(L.els):                  # the look: black, red, green only
        print("off the studio palette:", e["type"], e.get("text", "")[:40])
    canvas.write(out, list(L.els), "build_s09_studio_block_job_task_delivery.py")


if __name__ == "__main__":
    main()
