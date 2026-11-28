"""Where a theme Block keeps its page spec: `<block>/delivery/page-spec/`.

The spec is what the Block hands to the outside (the workbench code and the skills read it): each level's views
table (`<level>-views.md`), the section guide (`view-guide.json`), the shared shape (`structure.md`), the example
pages (`example-types.json`) and the elements read off them (`<level>-elements.md`, by ui_elements_harvest). The
Block's topics decide it, its Job writes it, a script writes the elements lists.

A Block not moved yet keeps it in `ui/`; that folder is read only while the new one is missing.
"""
from __future__ import annotations

from pathlib import Path

SPEC = Path("delivery") / "page-spec"
OLD = Path("ui")


def spec_dir(folder: Path) -> Path:
    """The Block's page-spec folder: delivery/page-spec/, or ui/ while only that one exists."""
    new, old = folder / SPEC, folder / OLD
    return old if not new.is_dir() and old.is_dir() else new
