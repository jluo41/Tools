"""b13 s01 · cowork ladder: s01-cowork-ladder.excalidraw: every cowork row in one drawing, Block down to Run.

An overview frame with Q01's proposed answer (the cowork ladder, why an email or a meeting is a row and
not a Task, each level's six Spaces, where today's Views go, the open points in red), then the cowork
rows of b03's s06 (Blocks) and s07 (Jobs), each with its proposed screens above today's. There is no
cowork Task row: a Task appears only for a document written in rounds, and it is then a Page Task.

The trees, skills and screens are defined once, in b03_project_workbench/studio/s01-overall-tree-structure/
(build_ladder_v4.py, level_views.py); edit the cowork entries there and b03's s06, s07 and this drawing
follow. canvas.write keeps every mark a person adds.

    python build_s01_cowork_ladder.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = Path(__file__).resolve().parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"      # the shared definitions and canvas.write live in b03
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."

# the cowork ladder, one line per level: level · folder · what it is and where it shows
LADDER = [("Block", "cowork/bNN_<topic>/", "one coordination topic: people, Questions, its Jobs · the Block tab"),
          ("Job", "jNN_<job>/", "one line of work, usually one request to one office · the Job tab, six Spaces"),
          ("item", "Timeline · CHECKLIST · emails/ · meetings/", "rows of Job › Work Details, by date: not Tasks"),
          ("Task ?", "tNN_<doc>/", "only a document written with others in rounds: a Page Task"),
          ("Run", "runs/run-<type>-<target>/", "soft only, at Block and Job; one pass per round of work")]
# Q01's Task question: why an email or a meeting is a row
WHY_ROW = ["an email or a meeting is one file; a Task is a folder with its face, runs/ and delivery/",
           "its work is a soft Run of the Job: run-email-<thread> writes emails/<thread>.md, a pass per round",
           "cowork makes no facts: no hard Runs, so no work Task (code work is a work Task, cited)",
           "one Job screen answers who has the move: Timeline lists every email, meeting and step by date",
           "a Task only for a document written with others in rounds (a protocol, an SOP): a Page Task"]
# each level's six Spaces: Space · Block · Job (was = today's View)
SPACES = [("Description", "bNN_<topic>.md · Scope · People · Resources · Related",
           "jNN_<job>.md header and text · Job · Files"),
          ("Idea Studio", "studio/sNN-<topic>/ (was Scope › RoadMap Draw)", "optional studio/"),
          ("Audience Report", "reports/qNN_*: Question │ Work │ Report (was Work › Questions)",
           "optional: the Block's Questions that cite this Job"),
          ("Work Details", "its Jobs: All · open · waiting · done (was Work › Jobs)",
           "its rows: Timeline · Checklist · Emails · Meetings (was Work › Emails · Meetings)"),
          ("Runs", "run-status- · run-draw- · run-report- · run-check-",
           "run-email- · run-notes- · run-update-job · run-check-"),
          ("Delivery", "optional: answered reports · done Jobs (Q03)", "optional: what it sent and decided (Q03)")]
# today's Check Space has no Space of its own any more (b03 s01-D18); Q02 settles where each goes
CHECK = [("Check › Waiting on", "a chip on each Job row: waiting-on · since (Q02)"),
         ("Check › Drafts", "Runs: an open run-email-<thread> until the person sends it (Q02)"),
         ("Check › Reports", "Runs: run-check-<qNN>; the release in Delivery (Q02 · Q03)")]
OPEN = ["j00_people/ is not a line of work: People as people.md at the Block? (changes real Blocks: JL) ?",
        "a Job's design/: drawings → studio/, notes → materials/? (changes real Jobs: JL) ?",
        "Task ▾ on a cowork Block: greyed unless the open Job has a tNN_<doc>/ ?",
        "board.md → bNN_<topic>.md (b03 s01-D12), with every Theme ?",
        "Q02: waiting-on, drafts and a stale Job once there is no Check ?",
        "Q03: what the Block and a Job deliver ?"]


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def overview(y):
    """The cowork ladder, the Task answer, each level's Spaces, where Check goes; then the open points."""
    fr = L.open_frame("cowork ladder")
    L.text(0, y, "Cowork: every level in one drawing (Q01, proposed 261007)", 30)
    L.text(0, y + 46, "The cowork rows of b03's s06 (Blocks) and s07 (Jobs), together; each frame below is drawn "
                      "from the same definitions as there.", 16, L.GRAY)
    ty = y + 100
    for level, folder, shows in LADDER:
        red = level.endswith("?")
        L.text(0, ty, level, 18, L.RED if red else L.INK)
        L.text(120, ty + 2, folder, 15, L.INK, L.MONO)
        L.text(620, ty + 3, shows, 14, L.RED if red else L.TEAL)
        ty += 34
    ty += 30
    L.text(0, ty, "Is an email, a meeting or a draft a Task?  No: a row of its Job.", 18, L.INK)
    ty += 34
    for line in WHY_ROW:
        L.text(0, ty, "· " + line, 14, L.INK)
        ty += 26
    ty += 30
    L.text(0, ty, "the six Spaces, level by level", 18, L.INK)
    ty += 34
    L.text(0, ty, "Space", 14, L.GRAY)
    L.text(200, ty, "Block tab", 14, L.GRAY)
    L.text(820, ty, "Job tab", 14, L.GRAY)
    ty += 26
    for space, block, job in SPACES:
        L.text(0, ty, space, 15, L.INK)
        L.text(200, ty + 1, block, 14, L.TEAL)
        L.text(820, ty + 1, job, 14, L.TEAL)
        ty += 28
    ty += 30
    L.text(0, ty, "today's Check Space, gone (b03 s01-D18)", 18, L.INK)
    ty += 34
    for was, now in CHECK:
        L.text(0, ty, was, 15, L.INK)
        L.text(260, ty + 1, now, 14, L.TEAL)
        ty += 28
    ty += 30
    L.text(0, ty, "open", 18, L.RED)
    for k, line in enumerate(OPEN):
        L.text(120, ty + 2 + k * 26, line, 14, L.RED)
    L.close_frame(fr, pad=40)
    return bottom()


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-cowork-ladder.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    y = overview(0) + 260
    blocks = [t for t in L.BLOCK_TREES if L.BLOCK_FAMILY.get(t[0]) == "cowork"]
    jobs = [t for t in L.JOB_TREES if LV.JOB_FAMILY.get(t[0]) == "cowork"]
    for title, trees, level, block in [("cowork Block: the Block tab", blocks, "Block", True),
                                       ("cowork Job: one line of work, the Job tab", jobs, "Job", False)]:
        L.draw_trees(title, SUB, trees, y, frame_each=True, views=LV.rows(level), block=block)
        y = bottom() + 260
    canvas.write(out, list(L.els), "build_s01_cowork_ladder.py")


if __name__ == "__main__":
    main()
