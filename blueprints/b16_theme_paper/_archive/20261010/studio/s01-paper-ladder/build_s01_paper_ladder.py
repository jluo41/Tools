"""b16 s01 · paper ladder: s01-paper-ladder.excalidraw: every paper row in one drawing, Block down to Run.

Q01's answer (261007): an overview frame with the paper ladder (each level, its folder, what it holds), where
each of today's Paper workbench Views moves, the run types and gates per level, and the open points in red;
then the paper rows of b03's s06 (Blocks), s07 (Jobs) and s08 (Tasks), each a frame with its proposed screens
above today's. The rows are defined once, in b03's studio/s01-overall-tree-structure/ (build_ladder_v4.py,
level_views.py); edit them there. b03 has no "paper Section" tree (a Section is a Page Task, s08 1c), so the
Task frame draws the Page Task tree under the paper Section's screens. canvas.write keeps every mark a person adds.

    python build_s01_paper_ladder.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B03 = HERE.parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio"      # the shared definitions and canvas.write live in b03
sys.path.insert(0, str(B03 / "s01-overall-tree-structure"))
sys.path.insert(0, str(B03 / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."

# the paper ladder, one line per level: level · folder · what it is and where it shows
LADDER = [("Block", "Paper-<Name>/  (face bNN_<topic>.md)",
           "one paper: its scope, venues, related work, questions and Story; Work Details = its versions"),
          ("Job", "jNN_v<MMDD>_<desk>/",
           "one send to one venue, dated by it: its Sections, Letters, studio/ · reports/ · runs/, its build"),
          ("Job", "jNN_grant_<funder>/ · jNN_slides_<talk>/",
           "the same Story told as a grant or a talk: Jobs of their own kind"),
          ("Task", "t0N_<title>/ · t2N_ · t3N_  (Page Task)",
           "one Section = one Page; t00 abstract · t0N_ Main · t2N_ Appendix · t31 cover letter · t32 response"),
          ("Run", "runs/run-<type>-<target>/",
           "soft only: a paper computes no facts; numbers come from work and discovery Tasks' hard Runs")]
STORY_TREE = ["studio/s01-ideation/              the idea pool, a studio topic (was the Ideation Page)",
              "studio/sNN-story-<telling>/      one telling: §1 · §2 · §4 in its face, its drawings beside it",
              "board.md ## Questions            each research question, grouped by topic",
              "reports/qNN_<question>/          its report; §5-§7 go into its Work",
              "<version>.md ## Narrative        §8 and the compile order, read by the build"]
# what changed on this drawing, in green (JL 261007: "add the short green comments to where we made the changes")
CHANGES = ["the Story is not a Job (was a j00_story/ reference Job)",
           "the Story and Ideation stop being Pages: studio topics s01-ideation/ · sNN-story-<telling>/, research "
           "questions as Board Questions with reports/qNN_, §8 in the version face's ## Narrative (Q04)",
           "a version is jNN_v<MMDD>_<desk>/, dated by its send (was jNN_v<N>_<venue>/)",
           "Tasks: t00_abstract · t0N_ Main · t2N_ Appendix (A = t21) · t3N_ Letters (was S-<desk>-<N>-<Section>/)",
           "a comments batch is not a Task; the next version answers it",
           "comments are a report of type comments: the answering version's reports/qNN_<kind>-<MMDD>/ (page-type: comments)",
           "Story §8 Narrative → the version's Audience Report › Draft-Main; Delivery › Rounds → its Comments",
           "a second version copies the first one's authored files only"]
# today's Paper workbench View -> where it goes on the ladder
MOVES = [("Guide › 4 Views", "Guide tab, unchanged", ""),
         ("Ideation", "Block › Audience Report › Ideation", "reads studio/s01-ideation/; the ideation skill runs from there"),
         ("Story › Spine", "Block › Audience Report › Spine", "reads the Story the Board tells now"),
         ("Story › High-level logic + Low-level work", "Block › Audience Report › Questions",
          "RQ → claim → work → reports/qNN"),
         ("Story › RoadMap Draw", "Block › Idea Studio", "a drawing: one topic, sNN-roadmap/"),
         ("Story › Related Papers", "Block › Description › Related", "related/related.md (b03 s01-D27)"),
         ("Story §8 Section Narrative", "version Job › Audience Report › Draft-Main", "the version face's ## Narrative, in compile order"),
         ("Sections › Narrative (G3)", "version Job › Audience Report", "release one Section row"),
         ("Sections › Main · Appendix", "version Job › Work Details", "Main · Appendix · Letters, each row its map"),
         ("a Section (Page workbench)", "Task tab", "the six Spaces of a Page Task (s08)"),
         ("Delivery › LaTeX · Word", "version Job › Delivery ?", "Block › Delivery shows it from below (Q02)"),
         ("Delivery › Cover letter", "version Job › Work Details › Letters", "a Page Task; built into Delivery"),
         ("Delivery › Rounds", "version Job › Audience Report › Comments", "Review Items · a report of type comments, reports/qNN_<kind>-<MMDD>/")]
# run types per level, and the gates (G0-G5 of workbench-paper) each level shows
RUNS = [("Block runs/", "run-venue-<venue> · run-question-<qNN> · run-draw-<topic> · run-version-<jNN> · run-status",
         "G2 answers (reports/)"),
        ("Story run types", "run-idea-<idea> · run-claim-<claim> · run-task-<row> · run-structure- · run-section-",
         "G0 pick · G1 release work · G2 claim"),
        ("version runs/", "run-narrative-<section> · run-compile-<build> · run-check-submit · run-delivery-<lane>",
         "G3 release a Section · G4 submit"),
        ("Section runs/", "run-structure- · run-section- · run-paragraph- · run-scratch- · run-revise- · "
         "run-display- · run-value- · run-citation- · run-delivery-latex · run-check-", "Page CHECK"),
        ("hard rNN_", "none in a paper: support.<target> runs in the Project's work/ and discovery/ Tasks", "")]
OPEN = ["Several Stories in one Board (one per idea): the Board shows the one the face's tells: names ?",
        "Block › Work Details groups: versions · grants · slides (b03 has main · appendix · grants · slides) ?",
        "Audience Report's Design group (s01-D22): RoadMap Draw is a drawing, so Idea Studio: drop Design ?",
        "the version face: jNN_v<MMDD>_<desk>.md (b03's tree says jNN_v<N>.md) ?",
        "the built paper: the Board's delivery/ or the version's (Q02) ?",
]


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def overview(y):
    """Q01's answer: the ladder, the story Job, where today's Views go, run types and gates, open points."""
    fr = L.open_frame("paper ladder")
    L.text(0, y, "Paper: every level in one drawing (Q01)", 30)
    L.text(0, y + 46, "The paper rows of b03's s06 (Blocks), s07 (Jobs) and s08 (Tasks), together; each frame "
                      "below is drawn from the same definitions as there.", 16, L.GRAY)
    ty = y + 100
    for level, folder, shows in LADDER:
        red = folder.rstrip().endswith("?") or " ? " in folder
        L.text(0, ty, level, 18, L.INK)
        L.text(120, ty + 2, folder, 15, L.RED if red else L.INK, L.MONO)
        L.text(620, ty + 3, shows, 14, L.TEAL)
        ty += 34
    ty += 30
    L.text(0, ty, "the Story and the Ideation: studio topics and Board Questions on disk, the Audience Report on screen (Q04)", 18,
           L.INK)
    ty += 34
    for line in STORY_TREE:
        L.text(0, ty, line, 14, L.RED if line.startswith("?") else L.INK, L.MONO)
        ty += 24
    ty += 30
    L.text(0, ty, "today's Paper workbench View → where it goes", 18, L.INK)
    ty += 34
    for today, where, note in MOVES:
        red = where.rstrip().endswith("?")
        L.text(0, ty, today, 15, L.GRAY)
        L.text(380, ty + 1, where, 14, L.RED if red else L.TEAL)
        L.text(760, ty + 1, note, 14, L.GRAY)
        ty += 28
    ty += 30
    L.text(0, ty, "Runs: soft at every level, by run type; the gates each level shows", 18, L.INK)
    ty += 34
    for where, types, gates in RUNS:
        L.text(0, ty, where, 15, L.INK)
        L.text(180, ty + 1, types, 14, L.TEAL, L.MONO)
        L.text(1640, ty + 1, gates, 14, L.GRAY)
        ty += 28
    ty += 30
    L.text(0, ty, "open", 18, L.RED)
    for k, line in enumerate(OPEN):
        L.text(120, ty + 2 + k * 26, line, 14, L.RED)
    ty += 2 + len(OPEN) * 26 + 30
    for k, line in enumerate(CHANGES):
        L.text(0, ty + k * 26, line if line.startswith("?") else f"✎ 261007  {line}", 15,
               L.RED if line.startswith("?") else L.GREEN)
    L.close_frame(fr, pad=40)
    return bottom()


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-paper-ladder.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    y = overview(0) + 260
    blocks = [t for t in L.BLOCK_TREES if L.BLOCK_FAMILY.get(t[0]) == "paper"]
    jobs = [t for t in L.JOB_TREES if LV.JOB_FAMILY.get(t[0]) == "paper"]
    # a Section is a Page Task (s08 1c): the Page Task's folder, under the paper Section's screens and skills;
    # a screen b03 does not define for the Section (Table, Evidence-Citation) is the Page Task's (in memory only)
    tasks = [("paper Section", "t0N_<title>/", tree) for v, _, tree in L.TASK_TREES if v == "Page Task"]
    section = LV.TASK_VARIANT_VIEWS.setdefault("paper Section", {})
    for key, spec in LV.TASK_VARIANT_VIEWS["Page Task"].items():
        section.setdefault(key, spec)
    for title, trees, level, block in [("paper Board: what the Block folder holds", blocks, "Block", True),
                                       ("paper version: one venue, its Sections", jobs, "Job", False),
                                       ("paper Section: a Page Task", tasks, "Task", False)]:
        L.draw_trees(title, SUB, trees, y, frame_each=True, views=LV.rows(level), block=block)
        y = bottom() + 260
    canvas.write(out, list(L.els), "build_s01_paper_ladder.py")


if __name__ == "__main__":
    main()
