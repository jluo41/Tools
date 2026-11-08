"""b13 j01 · s51-block-ui-report's drawing: one cell of the cowork 3 x 3 (level × section), drawn by ../../cowork_ui_cells.py in
haipipe-studio's five parts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import cowork_ui_cells  # noqa: E402

if __name__ == "__main__":
    cowork_ui_cells.build(Path(__file__).parent)
