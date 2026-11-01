"""b15 j01 · s51-block-ui-report's drawing: one cell of the labeling 3 x 3 (level × section), drawn by ../../labeling_ui_cells.py in
haipipe-studio's five parts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import labeling_ui_cells  # noqa: E402

if __name__ == "__main__":
    labeling_ui_cells.build(Path(__file__).parent)
