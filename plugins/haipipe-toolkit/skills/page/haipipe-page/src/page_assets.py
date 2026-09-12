"""Shared Page appearance, independent of the Board host."""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def css():
    """Keep the same ordered parts Board consumes via compatibility links."""
    return "\n".join(path.read_text(encoding="utf-8")
                     for path in sorted((ASSETS / "css").glob("*.css")))
