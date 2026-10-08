"""b14 s01 · discovery ladder: s01-discovery-ladder.excalidraw: every discovery row in one drawing, Block down to Run.

The discovery rows of b03's s06 (Blocks), s07 (Jobs) and s08 (Tasks), together (JL 261007), after an
overview frame that answers Q01: the ladder one line per level, where each of today's Discovery Views
goes, what discovery adds that no other Theme has, and the open points in red. A Run-level frame closes
it: a Paper Run opened from a Task's Runs. The trees, skills and screens are defined once, in b03's
studio/s01-overall-tree-structure/ (build_ladder_v4.py, level_views.py); edit the rows there. This
builder draws only the overview and the Run frame. canvas.write keeps every mark a person adds.

    python build_s01_discovery_ladder.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parents[2] / "b03_project_workbench" / "studio"      # the shared definitions and the canvas writer
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."

# the discovery ladder, one line per level: level · folder · what its tab shows
LADDER = [("Block", "discovery/bNN_<topic>/", "the inquiries and the Questions: Description · Idea Studio · Audience Report "
                                              "| Work Details = its Jobs | Runs · Delivery"),
          ("Job", "jNN_<inquiry>/", "one inquiry, the Block's six Spaces: Work Details = its sub-question Tasks, "
                                    "Audience Report = their answers"),
          ("Task", "tNN_<task>/", "one sub-question, one discovery_type: a Page (its article) that makes facts; "
                                  "Work Details = Papers · Intake · Draft"),
          ("Run", "runs/rNN_<author><year>_<subject>/", "hard, one Subject: Result Card · facts · receipt · one Bib "
                                                       "entry; opens as a pop-out")]
# today's Discovery View (all at the Block, workbench-discovery) -> where it goes
MOVES = [("today (Block level)", "proposed", ""),
         ("Guide › Description · Method · RoadMap Draw · Related Paper", "Guide tab", "unchanged"),
         ("Scope › Block", "Block › Description › Scope", "the Jobs and Tasks: Block › Work Details"),
         ("Scope › Questions", "Block › Audience Report", "one row per Question: Question │ Work │ Report"),
         ("Scope › Resources", "Block › Description › Resources", "where it searches; Related = related/"),
         ("Scope › RoadMap Draw", "Block › Idea Studio", "one drawing after another"),
         ("Work › Papers", "Task › Work Details › Papers", "each Task its own; a row count on Job and Block rows"),
         ("Work › Tasks", "Job › Work Details", "Block › Work Details opens each Job to its Tasks"),
         ("Work › Questions", "Block › Audience Report", "merged with Scope › Questions"),
         ("Check › Runs", "Runs, at each level", "Block, Job: soft; Task: the Paper Runs and its Page's Runs"),
         ("Check › Citations", "a chip on its paper row", "Task › Work Details › Papers; Verify a citation (Q02)"),
         ("Check › Reports", "the state on each report row", "Block › Audience Report; Check a report = a Run"),
         ("Delivery › Reports", "Block › Delivery", "and each Task's built article, from below"),
         ("Delivery › BibTeX", "Delivery, at each level", "the Task's Evidence Bib, merged at Job and Block (Q02)")]
# what discovery has that no other Theme has
OWN = ["a Task is a Page that makes facts: hard Paper Runs, and its Page's soft Runs (structure, section, citation, check)",
       "one Run, one Subject: a Trigger (url, doi, pdf) resolves to Subjects; each admitted Subject gets one rNN_",
       "Intake: the screened candidates (admitted → its Run, excluded, unresolved), from discovery.yaml",
       "discovery_type groups a Job's Tasks by specialist: Search (map) · Review (reading) · Synthesize (verdict, landscape …)",
       "the Bib climbs: one entry per Result → the Task's Evidence Bib → merged at Job and Block Delivery"]
OPEN = ["a Job face jNN_<inquiry>.md (today the job: block is copied into each Task's discovery.yaml) ?",
        "a synthesis across a Job's Tasks: a Task of its own, or the Block's report ?",
        "a Paper Run's receipt: result/runtime.yaml (today) or passes/pNN/runtime.yaml (s01-D15) ?",
        "screened candidates: draft/records/search/ (today results/search/, which merges into runs/) ?",
        "the Evidence Bib: draft/evidence/bibex/tNN_<task>.bib (today) or tNN_<task>.bib, as a Page Task's ?",
        "papers grouped by role on Task › Papers; the citation chip (Q02) ?"]


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def overview(y):
    """Q01's answer in one frame: the ladder, today's Views and where they go, discovery's own, open."""
    fr = L.open_frame("Overview · the discovery ladder")
    L.text(0, y, "Discovery: every level in one drawing", 30)
    L.text(0, y + 46, "Q01 · How does an inquiry climb the ladder? The discovery rows of b03's s06 (Blocks), s07 (Jobs) "
                      "and s08 (Tasks), together; each frame below is drawn from the same definitions as there.",
           16, L.GRAY)
    ty = y + 100
    for level, folder, shows in LADDER:
        L.text(0, ty, level, 18, L.INK)
        L.text(120, ty + 2, folder, 15, L.INK, L.MONO)
        L.text(560, ty + 3, shows, 14, L.TEAL)
        ty += 34
    ty += 26
    L.text(0, ty, "today's Discovery Views (all on the Block) and where each goes", 18, L.INK)
    ty += 34
    for k, (old, new, how) in enumerate(MOVES):
        head = k == 0
        L.text(0, ty, old, 14, L.INK if head else L.GRAY)
        L.text(560, ty, new, 14, L.TEAL)
        L.text(900, ty, how, 14, L.INK if head else L.GRAY)
        ty += 26
    ty += 26
    L.text(0, ty, "what discovery has that no other Theme has", 18, L.INK)
    for k, line in enumerate(OWN):
        L.text(120, ty + 34 + k * 26, line, 14, L.INK)
    ty += 34 + len(OWN) * 26 + 26
    L.text(0, ty, "open", 18, L.RED)
    for k, line in enumerate(OPEN):
        L.text(120, ty + 2 + k * 26, line, 14, L.RED)
    ty += 2 + len(OPEN) * 26 + 20
    L.text(0, ty, "also open: Q02 Where do papers, citations and the Bib show? · Q03 How is a synthesis handed on?",
           14, L.RED)
    L.close_frame(fr, pad=40)
    return bottom()


def run_level(y):
    """The Run level: a Paper Run opened from Task › Runs (or from its paper row), and its folder."""
    fr = L.open_frame("Run level · a Paper Run")
    L.text(0, y, "discovery · Run level", 30)
    L.text(0, y + 46, "One Paper Run = one Subject, hard: its output stays in its own result/. It opens as a pop-out "
                      "from Task › Runs or from its row in Task › Work Details › Papers.", 16, L.GRAY)
    tree = [("rNN_<author><year>_<subject>/", ""), ("├── run.yaml", "the card: run · kind hard · type read · scope tNN"),
            ("├── rNN_<…>.sh", "the ticket: one Subject, frozen inputs"),
            ("├── result/", "generated by the ticket, never by hand"),
            ("│   ├── rNN_<…>.md", "the Result Card: cite · venue · verification · Readout"),
            ("│   ├── facts.md · abstract.md", "what the source says"), ("│   ├── rNN_<…>.bib", "exactly one entry"),
            ("│   ├── source-access.json", "how it was read (paper-source-v2)"),
            ("│   └── paper.pdf · trigger.md", "optional"),
            ("└── passes/pNN-<MMDD>/ ?", "log · runtime.yaml: a retry is a pass; a new analysis a new rNN")]
    ty = y + 110
    for line, meaning in tree:
        red = line.endswith("?")
        L.text(0, ty, line, 14, L.RED if red else L.INK, L.MONO)
        L.text(330, ty + 1, meaning, 13, L.RED if red else L.GRAY)
        ty += 22
    lines = [("r02_<author><year>_<subject>", "read", "complete · p02"),
             "the Result Card, as it reads: cite · venue · Readout", "facts · abstract · one Bib entry · source access",
             "passes: p01 (blocked: no access) · p02, compare any two", "cited by: tNN › C2 · its chip: to verify"]
    sp_ = ("discovery", "Task", "discovery Task", "Runs", "read", "preview", "", "")
    L.wireframe(1000, y + 100, sp_, lines=lines, runs=["Open the result", "Run it again (a pass)", "Verify a citation"],
                header="discovery Task · Task › Runs › r02_<author><year>_<subject>")
    L.text(1600, y + 124, "today: runs/rNN_<…>.sh + results/rNN_<…>/ (runtime.yaml inside);", 14, L.GRAY)
    L.text(1600, y + 148, "a Run's row opens its Result Card in the shared pop-out", 14, L.GRAY)
    L.text(1600, y + 180, "differs: the two folders become one, runs/rNN_<…>/ (s01-D15) ?", 14, L.RED)
    L.close_frame(fr, pad=40)
    return bottom()


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-discovery-ladder.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    y = overview(0) + 260
    for title, trees, fam, level, block in [("Board level", L.BLOCK_TREES, L.BLOCK_FAMILY, "Block", True),
                                            ("Job level", L.JOB_TREES, LV.JOB_FAMILY, "Job", False),
                                            ("Task level", L.TASK_TREES, LV.TASK_FAMILY, "Task", False)]:
        rows = [t for t in trees if fam.get(t[0]) == "discovery"]
        L.draw_trees(f"discovery · {title}", SUB, rows, y, frame_each=True, views=LV.rows(level), block=block)
        y = bottom() + 260
    run_level(y)
    canvas.write(out, list(L.els), "build_s01_discovery_ladder.py")


if __name__ == "__main__":
    main()
