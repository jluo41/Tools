"""b14 j01 · s56-job-ui-studio's drawing: one cell of the discovery 3 x 3 (level × section), drawn by ../../discovery_ui_cells.py
in haipipe-studio's five parts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import discovery_ui_cells  # noqa: E402

if __name__ == "__main__":
    discovery_ui_cells.build(Path(__file__).parent)
