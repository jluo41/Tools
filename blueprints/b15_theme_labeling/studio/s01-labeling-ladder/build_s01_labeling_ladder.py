"""b15 s01 · labeling ladder: s01-labeling-ladder.excalidraw: every labeling row in one drawing, Block down to Run.

The labeling rows of b03's s06 (Blocks), s07 (Jobs) and s08 (Tasks), together (JL 261007), after an
overview frame with this Block's open questions. Drawn by b03's studio/_build/theme_ladder.py from the
shared definitions (b03's studio/s01-overall-tree-structure/); edit the rows there. canvas.write keeps
every mark a person adds.

    python build_s01_labeling_ladder.py [out.excalidraw]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "_build"))
import theme_ladder  # noqa: E402

if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "s01-labeling-ladder.excalidraw"
    theme_ladder.draw("labeling", ['labeling'], HERE.parents[1] / "board.md", out, "build_s01_labeling_ladder.py")
