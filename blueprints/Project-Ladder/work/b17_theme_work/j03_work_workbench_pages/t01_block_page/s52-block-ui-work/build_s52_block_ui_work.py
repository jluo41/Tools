"""b17 j03 · s52-block-ui-work's drawing: one cell of the work theme's 3 x 3 (level × section), drawn by ../../work_ui_cells.py in
haipipe-studio's five parts (five_parts.build)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import work_ui_cells  # noqa: E402

if __name__ == "__main__":
    work_ui_cells.build(Path(__file__).parent)
