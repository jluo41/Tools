"""haipipe-board src/ (QB5): build.py (here) and servers/_host/serve.py are thin
entries; the grammar lives here by topic — common · parse · body · page_board · page_question ·
page_stage. One grammar, assembled into pages."""

from pathlib import Path

# Board owns its orchestration; shared Page modules live only with Page.
__path__.append(str(Path(__file__).resolve().parents[3] / "page" / "haipipe-page" / "src"))

# A few grammar modules read live projections (`live.outline_preview`,
# `live.outline`, `live.insightboard`). Those presenters live in the workbench's
# servers/ tree; its host folder owns the `live` namespace, so it is put on
# sys.path here, once, for every entry that imports this package.
import sys as _sys
from pathlib import Path as _Path

_HOST = _Path(__file__).resolve().parents[4] / "servers" / "_host"
if _HOST.is_dir() and str(_HOST) not in _sys.path:
    _sys.path.append(str(_HOST))
