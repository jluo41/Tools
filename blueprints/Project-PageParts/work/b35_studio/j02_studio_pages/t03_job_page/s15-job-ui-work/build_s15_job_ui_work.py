"""b35 j02 · s15-job-ui-work's drawing: one UI cell (level × section), drawn by ../../studio_ui_cells.py in haipipe-studio's five
parts, its Design the real page and the face's Rules."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import studio_ui_cells  # noqa: E402

if __name__ == "__main__":
    studio_ui_cells.build(Path(__file__).parent)
