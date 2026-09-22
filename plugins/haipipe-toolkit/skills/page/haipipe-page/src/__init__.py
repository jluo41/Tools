"""Page-owned models and runtime. No Board installation is required."""

# A few grammar modules read live projections (`live.outline_preview`,
# `live.outline`, `live.insightboard`). Those presenters live in the workbench's
# servers/ tree; its host folder owns the `live` namespace, so it is put on
# sys.path here, once, for every entry that imports this package.
import sys as _sys
from pathlib import Path as _Path

_HOST = _Path(__file__).resolve().parents[4] / "servers" / "_host"
if _HOST.is_dir() and str(_HOST) not in _sys.path:
    _sys.path.append(str(_HOST))
