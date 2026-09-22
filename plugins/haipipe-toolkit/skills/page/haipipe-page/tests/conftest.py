"""Make the Page engine and the servers' `live` namespace importable from tests/.

The Page presenters (`live.outline`, `live.delivery`, ...) moved to the workbench's
servers/ tree; its host folder owns the `live` namespace and resolves each
module wherever it now sits.
"""
import sys
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ENGINE))
sys.path.insert(0, str(_ENGINE.parents[2] / "servers" / "_host"))
