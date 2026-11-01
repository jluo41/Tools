"""b12 j01 · s53-block-ui-studio's drawing: one cell of the design 3 x 3 (level × section), drawn by ../../design_ui_cells.py in
haipipe-studio's five parts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import design_ui_cells  # noqa: E402

if __name__ == "__main__":
    design_ui_cells.build(Path(__file__).parent)
