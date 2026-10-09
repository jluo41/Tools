"""s13 · Task variants, proposed: s13-task-variants-proposed.excalidraw: each Task variant: its folder (one folder per Run in runs/), its skills, and where it shows on screen.

s13-task-variants.excalidraw beside it is JL's own copy (261006): JL marks and moves it, and no
script writes it. Proposals go to the -proposed file; JL compares the two and carries over what they keep.

The trees, skills and screens are defined once, in ../s01-overall-tree-structure/build_ladder_v4.py
(TASK_TREES and the tables beside it); edit them there. This builder draws them into its own file,
one frame per variant, through canvas.write, so every mark a person adds survives a rebuild.

    python build_s13_task_variants.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "s01-overall-tree-structure"))
sys.path.insert(0, str(HERE.parent / "_build"))
import build_ladder_v4 as L  # noqa: E402  (the shared trees and drawing helpers)
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts"))  # canvas (haipipe-studio)
import canvas  # noqa: E402
import level_views as LV  # noqa: E402  (proposed screens per Space, and today's beside them)

SUB = "Read off real folders where one exists, otherwise the family's contract; red ? = open."


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s13-task-variants-proposed.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    L.draw_trees("Task variants: what each Task folder holds", SUB, L.TASK_TREES, 0, frame_each=True, views=LV.rows("Task"), groups=True)  # one frame per variant, in four groups
    L.changes(L.CHANGES_261008 + ["✎ 261008 a work Task's Page views sit in its Spaces: Folder · Draft · Evidence · Value · Page Runs · Lanes", "    (the frame's ?view=, once separate /_board/draft, /evidence, … pages)", '✎ 261008 a Page Task as the frame draws it: Runs and Delivery have no third row; Evidence-Supporting'])            # what 261008 changed, in green
    canvas.write(out, list(L.els), "build_s13_task_variants.py")


if __name__ == "__main__":
    main()
