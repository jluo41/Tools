import sys
from pathlib import Path

WORKBENCH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKBENCH.parent / "_host"))
from host_paths import bootstrap
bootstrap()
