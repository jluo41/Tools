"""Rebuild this S00 with the current shared haipipe-studio generator."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str((HERE / "../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts").resolve()))
import block_index  # noqa: E402

if __name__ == "__main__":
    block_index.draw(HERE.parent.parent)
