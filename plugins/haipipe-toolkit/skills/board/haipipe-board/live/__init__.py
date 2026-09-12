"""QC8 · serve.py's live layer, one module per area."""

from pathlib import Path

__path__.append(str(Path(__file__).resolve().parents[3] / "page" / "haipipe-page" / "live"))
