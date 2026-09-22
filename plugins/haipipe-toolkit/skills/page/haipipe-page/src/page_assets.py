"""Shared Page appearance, read from the servers tree.

The Page's stylesheet parts and reader scripts are served by
``plugins/haipipe-toolkit/servers/haipipe-page/assets``; the static Page build
reads the same files so a built ``delivery/web/`` and the live server agree.
"""
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[4] / "servers" / "haipipe-page" / "assets"


def css():
    """The ordered Page stylesheet parts; the Board bundle includes the same files."""
    return "\n".join(path.read_text(encoding="utf-8")
                     for path in sorted((ASSETS / "css").glob("*.css")))
