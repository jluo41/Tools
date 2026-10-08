"""s12 · Job variants: one drawing, s12-job-variants.excalidraw: each Job variant: its folder, what it holds, its skills, and where it shows on screen.

The trees, skills and screens are defined once, in ../s01-overall-tree-structure/build_ladder_v4.py
(JOB_TREES and the tables beside it); edit them there. This builder draws them into its own file,
one frame per variant, through canvas.write, so every mark a person adds survives a rebuild.

    python build_s12_job_variants.py [out.excalidraw]
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
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s12-job-variants.excalidraw"
    L.els.clear()
    L.FRAME[0] = None
    L.draw_trees("Job variants: what each Job folder holds", SUB, L.JOB_TREES, 0, frame_each=True, views=LV.rows("Job"), groups=True)  # one frame per variant, in four groups
    L.changes(L.CHANGES_261008 + ["✎ 261008 a design Job's Audience Report: Reason ideas · Design display · Review whole · Predicted vs observed ·", '    Performance; Design display shows each design item as it shows, word for word'])            # what 261008 changed, in green
    canvas.write(out, list(L.els), "build_s12_job_variants.py")


if __name__ == "__main__":
    main()
