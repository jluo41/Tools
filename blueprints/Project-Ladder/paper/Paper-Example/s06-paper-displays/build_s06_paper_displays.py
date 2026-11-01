"""s06-paper-displays: drawn by excalidraw-workflow's displayplan_drawing.py from this face's Displays table, the venue's display rules and the pool; a person's marks on the drawing are kept.

    python build_s06_paper_displays.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../../plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-workflow/scripts").resolve()))
import displayplan_drawing  # noqa: E402

if __name__ == "__main__":
    print(displayplan_drawing.draw(HERE))
