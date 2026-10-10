"""s01 · Design: s01-design.excalidraw: the design ladder at a glance.

The first topic of b12_theme_design (JL 261007; drawn first in b03, before the Block existed): one
overview frame of the design ladder, the design method's six steps and where each shows, its 13 methods
in 3 families, how an insight Block steers a design, and the open points. Each level is drawn on its own
(JL 261007, "instead of nesting all the things together"): s11 Block, s12 Job, s13 Task.

The trees, skills and screens are defined once, in b03_project_workbench/studio/s01-overall-tree-structure/
(build_ladder_v4.py and level_views.py); edit them there, and b03's variant topics and this drawing all follow. This
builder draws them into its own file through canvas.write, so every mark a person adds survives a rebuild.

    python build_s01_design.py [out.excalidraw]
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

# the design ladder, one line per level: level · folder · where it shows
LADDER = [("Block", "B00_DesignBoard-<app>/", "one application, one channel · Description: the goal list, theory, "
                                              "shared rules | Work Details: its Jobs, by method family"),
          ("Job", "jNN_<goal>_<design-method>/", "one goal × one method → N designs: the Block's six Spaces"),
          ("Task", "tNN_d<NN>_<slug>/", "one design: Design · Rationale · Evaluation"),
          ("Run", "runs/", "commission (soft) · generate (hard, the Job's) · verify · revise (per design)"),
          ("today", "0-BR-brief/ · 1-P-principle/ · 2-Design[-M<NN>]/",
           "stages; a method folder holds every goal; a Design folder = one goal")]
# the design method's six steps (design-method.md) and where each shows on the design Job
STEPS = [("1 Set the Design Task", "Job › Description › Goal", "a person signs the aim and the rules"),
         ("2 Pick the method", "Job › Description › Method", "one of 13, frozen in method.md"),
         ("3 Generate N designs", "Job › Runs › generate", "an agent; each design with its element record"),
         ("4 Evaluate", "Job › Audience Report · a Task's verify", "a different agent; weak → Revise"),
         ("5 Release", "Job › Delivery", "a person: passed designs, word for word"),
         ("6 Run the Exp", "outside the workbench", "its data becomes the next Insight: the Learning loop")]
FAMILIES = [("Goal Only", "no rule yet", "by goal · by principle · by exploring · by slots"),
            ("External Insights", "a rule from research", "by theory · by implementation"),
            ("Internal Insights", "a rule from our data", "by insight · precedent · revising · tailoring ·"),
            ("", "", "theory and insight · user test · co-design (future)")]
STEER = ["insight Block › j04_wisdom › tNN_<counsel>: a signed W",
         "    ↓ handoff: the only crossing between the two Blocks",
         "design Block › Description › Resources: W-NN",
         "a design Job by insight · tailoring · theory and insight reads W-NN",
         "each design's elements say where they came from: from = W-NN",
         "    (Job › Audience Report › Elements)"]
OPEN = ["Generate at the Job: one Run makes the N drafts and opens N Tasks ?",
        "method-folders.md makes the method alone the Job, holding every goal: change it once agreed ?",
        "the Brief and the principles: the Block's Description (goal list, shared rules) ?",
        "a design's Rationale: its Task's Audience Report, or its card ?",
        "the Task row: one design (b03's s13-task-variants still draws a Design folder, one goal) ?",
        "B00_DesignBoard-<app>/ → bNN_<topic>/; old names read until renamed ?"]


def bottom():
    return max(e["y"] + e.get("height", 0) for e in L.els)


def overview(y):
    """The design ladder, the method and where it shows, its families, the insight link; then the open points."""
    fr = L.open_frame("design ladder")
    L.text(0, y, "Design: the ladder at a glance", 30)
    L.text(0, y + 46, "The ladder at a glance; each level is drawn on its own: s11 Block, s12 Job, s13 Task "
                      "(the rows of b03's s11, s12 and s13 variants).", 16, L.GRAY)
    ty = y + 100
    for level, folder, shows in LADDER:
        L.text(0, ty, level, 18, L.INK)
        L.text(120, ty + 2, folder, 15, L.INK, L.MONO)
        L.text(620, ty + 3, shows, 14, L.TEAL)
        ty += 34
    ty += 30
    L.text(0, ty, "the method: six steps, and where each shows", 18, L.INK)
    ty += 34
    for step, where, who in STEPS:
        L.text(0, ty, step, 15, L.INK)
        L.text(260, ty + 1, where, 14, L.TEAL)
        L.text(620, ty + 1, who, 14, L.GRAY)
        ty += 28
    ty += 30
    L.text(0, ty, "13 methods, 3 families: where the rule comes from", 18, L.INK)
    ty += 34
    for fam, rule, methods in FAMILIES:
        L.text(0, ty, fam, 15, L.INK)
        L.text(260, ty + 1, rule, 14, L.GRAY)
        L.text(620, ty + 1, methods, 14, L.TEAL)
        ty += 28
    ty += 30
    L.text(0, ty, "insight steers design", 18, L.INK)
    ty += 34
    for line in STEER:
        L.text(0, ty, line, 14, L.INK, L.MONO)
        ty += 24
    ty += 30
    L.text(0, ty, "open", 18, L.RED)
    for k, line in enumerate(OPEN):
        L.text(120, ty + 2 + k * 26, line, 14, L.RED)
    L.close_frame(fr, pad=40)
    return bottom()


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-design.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    overview(0)                                       # each level is its own drawing: s11 Block · s12 Job · s13 Task
    canvas.write(out, list(L.els), "build_s01_design.py")


if __name__ == "__main__":
    main()
