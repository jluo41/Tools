"""s11 · Block variants, proposed: s11-block-variants-proposed.excalidraw: each Block variant: its folder, what it holds, its skills, and one screen per view of the Block tab.

s11-block-variants.excalidraw beside it is JL's own copy (261006): JL marks and moves it, and no
script writes it. Proposals go to the -proposed file; JL compares the two and carries over what they keep.

The trees, skills and screens are defined once, in ../s01-overall-tree-structure/build_ladder_v4.py
(BLOCK_TREES and the tables beside it); edit them there. This builder draws them into its own file,
one frame per variant, through canvas.write, so every mark a person adds survives a rebuild.

    python build_s11_block_variants.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)
sys.path.insert(0, str(HERE.parent / "s04-studio-and-report"))
import studio_report_ui as UI  # noqa: E402  (Idea Studio and Audience Report, drawn large)
import screens as SC  # noqa: E402  (the workbench screens, drawn large; s02-workbench-shared uses it too)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."

# ── the new style (JL 261007: "how do you update the s11 to s13 to follow the same style?"): one full
# screen per Space, what the theme changes, what today shows, and the files behind it. Pilot: the work Block.
WORK_BLOCK = [
    dict(space="Description", third=["Scope", "Resources", "Related"], kind="lines",
         content=["bNN_<topic>.md", "kind: task-block", "spine: the one line this Block answers",
                  "covers: <topic> · <topic> · …", "excluded: what it leaves to others", "close: when it is done"],
         runs=["Update the Block status", "Edit the spine"], recent="run-face-<bNN>   p02 closed",
         note="the work theme: Resources lists data · code · heavy output", changed=True,
         today="Scope › Block · Resources (two views)",
         disk=[("bNN_<topic>/", ""), ("├── bNN_<topic>.md", "Scope: kind · spine · covers · close"),
               ("│", "Resources: data · code · heavy, in the face"), ("└── related/related.md", "Related: one table")]),
    dict(space="Idea Studio", kind="rows", content=["s01-<topic>", "s02-<topic>", "s03-question-map"],
         runs=["Add a topic", "Redraw a topic", "Save this session"], recent="run-draw-s01   p03 open",
         note="same as the base; s03-question-map is generated, view only",
         today="Scope › RoadMap Draw (flat studio/*.excalidraw)",
         disk=[("bNN_<topic>/studio/", "one row per topic folder"), ("├── s01-<topic>/s01-<topic>.excalidraw", "the live drawing"),
               ("├── s01-<topic>/s01-<topic>.md", "its details, when opened"), ("└── s03-question-map/", "built from the register")]),
    dict(space="Audience Report", third=["All", "<group A>", "<group B>"], kind="table",
         heads=["Logic · the question", "Work · Tasks and Runs", "Report · what it says"], cols=(0, 420, 760),
         content=[("q01 <question>", "j11 › t02 › r03", "<title> · answered"), ("q02 <question>", "j12 › t01", "<title> · draft"),
                  ("q03 <question>", "—", "asked")],
         runs=["Ask a Question", "Write the report", "Draw the report", "Check a report"], recent="run-report-q02   p02 closed",
         note="same as the base: one row per Question, grouped as the register groups them",
         today="Scope › Questions; Task › <group A> · <group B>",
         disk=[("bNN_<topic>/bNN_<topic>.md", "the register: Questions and their groups"),
               ("└── reports/qNN_<topic>/", "a row: the Page, its drawing (generated)"),
               ("jNN_<job>/tNN_<task>/runs/rNN_<slug>/", "the Work column: the Runs it cites")]),
    dict(space="Work Details", third=["All", "j0N", "j1N", "j5N"], kind="table",
         heads=["Job", "Tasks · feeds", "state"],
         content=[("j01_<data>", "3/3 · Q01", "done"), ("j11_<job>", "3/5 · Q01", "half · waits on t02"),
                  ("j51_<dataset>", "0/2 · Q02", "stale · 30 days")],
         runs=["Open a Job", "Update a Job"], recent="run-plan-jobs   p01 closed",
         note="the work theme names the Job series: j0N data · j1N work · j5N per dataset", changed=True,
         today="no Job list: Task › Not under a Question; Check › Tasks",
         disk=[("bNN_<topic>/", ""), ("├── j01_<data>/ · j11_<job>/ · j51_<dataset>/", "one row per Job folder"),
               ("│   └── jNN_<job>.md", "the row: Tasks · feeds · state"), ("└── jNN_<job>/src/ · sbatch/", "a Job's code (Job tab)")]),
    dict(space="Runs", third=["All", "draw", "report", "check", "delivery"], kind="table",
         heads=["Run", "type · writes", "state"],
         content=[("run-draw-s01", "Draw · s01", "open · p03"), ("run-report-q02", "Write the report · q02", "closed · p02"),
                  ("run-check-q02", "Check a report · q02", "waiting"), ("run-delivery-d01", "Build · d01", "closed · p01")],
         runs=["Draw", "Write the report", "Check a report", "Build the report"], recent="run-check-q02   waiting",
         note="same as the base: a Block's Runs are soft; its Tasks' hard Runs show one level down",
         today="Check › Runs",
         disk=[("bNN_<topic>/runs/", "one row per Run folder"), ("├── run-draw-s01/run.yaml", "the row: type · writes · state"),
               ("└── run-report-q02/passes/p02-<MMDD>/", "the pop-out: its passes")]),
    dict(space="Delivery", third=["All", "Report", "Export"], kind="lines",
         content=["its own: empty (optional for a work Block)", "from below:", "j11 · t02     Report   released",
                  "j12 · t01     Report   web · LaTeX"],
         runs=["Build a delivery", "Release"], recent="run-delivery-d01   p01 closed",
         note="same as the base: optional; what leaves the Block, and what rolls up from below",
         today="Delivery › Reports",
         disk=[("bNN_<topic>/delivery/", "its own deliveries, if any"), ("└── dNN-<name>/", "one built report or export"),
               ("jNN_<job>/tNN_<task>/delivery/", "rolled up: \"from below\"")]),
]
WORK_POPOUTS = [("run-report-q02  ·  the Run", ["run.yaml: kind soft · type report · target q02",
                                                "passes: p01 1005 · p02 1006 closed", "[ p02: before / after of the Page ]",
                                                "  the ledger · open the report · Rerun"]),
                ("q01 <question>  ·  the report", ["Answer", "  <the answer, a few lines>", "Evidence · Limits · Next",
                                                   "[ its drawing, generated from studio frames ]"])]


def screens_pilot(x0, y0):
    fr = L.open_frame("work Block · on screen")
    SC.variant(x0, y0, "work Block on screen: the six Spaces, full size (pilot)",
               "Teal: what the work theme changes. Gray: the same as the base (s02-workbench-shared). "
               "Under each: what today shows instead, and the files behind it.",
               SC.TABS, 1, WORK_BLOCK, WORK_POPOUTS)
    L.close_frame(fr, pad=60)
    return fr


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s11-block-variants-proposed.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    L.draw_trees("Block variants: what each board folder holds", SUB, L.BLOCK_TREES, 0, frame_each=True, views=LV.rows("Block"), groups=True)  # one frame per variant, in four groups
    bottom = max(e["y"] + e["height"] for e in L.els if e["type"] == "frame")
    UI.closeups(0, bottom + 600)                       # Idea Studio and Audience Report, under the groups
    right = max(e["x"] + e["width"] for e in L.els if e["type"] == "frame") + 600
    screens_pilot(right, 0)                            # the new style, beside everything (pilot: work Block)
    L.changes(L.CHANGES_261008 + [])            # what 261008 changed, in green
    canvas.write(out, list(L.els), "build_s11_block_variants.py")


if __name__ == "__main__":
    main()
