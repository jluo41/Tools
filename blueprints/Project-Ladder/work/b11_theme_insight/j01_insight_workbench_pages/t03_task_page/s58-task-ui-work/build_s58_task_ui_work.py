"""b11 j01 · s58-task-ui-work's drawing: one cell of the insight 3 x 3 (level × section), drawn by ../../insight_ui_cells.py in
haipipe-studio's five parts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import insight_ui_cells  # noqa: E402

if __name__ == "__main__":
    insight_ui_cells.build(Path(__file__).parent)
