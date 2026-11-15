"""Design names: `Design N` on screen, old links and renamed Design Folders, and the
Design Pages a short folder name finds on a board.

Split out of design.py; design.py re-exports every name here."""
from __future__ import annotations

import re
from pathlib import Path


def design_number(item_id: str) -> str:
    """`ITEM03` said on screen: `Design 3` (Design N on screen, ITEMNN in the files)."""
    hit = re.match(r"^ITEM0*(\d+)$", str(item_id))
    return f"Design {hit.group(1)}" if hit else str(item_id)


_OLD_GROUP = re.compile(r"(^|/)2-DS-design(/|$)")
_OLD_FOLDER = re.compile(r"(^|/)DS(\d{2})-")


def modern_file(file: str) -> str:
    """Old links said 2-DS-design/DS01-…; the folders are 2-Design/Design-01-… now."""
    out = _OLD_GROUP.sub(r"\g<1>2-Design\2", file or "")
    out = _OLD_FOLDER.sub(r"\g<1>Design-\2-", out)
    return _OLD_FOLDER.sub(r"\g<1>Design-\2-", out)      # the page file name carries the id twice


_FOLDER_FILE = re.compile(r"^(2-Design(?:-M\d+-[^/]+)?)/(Design-\d+-[^/]+)/\2\.md$")


def renamed_folder(board: Path | None, name: str, group_name: str = "2-Design") -> str:
    """A folder renamed to say its goal keeps its Design-NN id: an old name finds the one folder with that id."""
    hit = re.match(r"^Design-(\d+)(?:-|$)", name or "")  # the bare id works too: Design-04, Design-4
    group = Path(board) / group_name if board is not None else None
    if group is None or not hit or (group / name).is_dir():
        return name
    found = [p.name for p in group.glob(f"Design-{int(hit.group(1)):02d}-*") if p.is_dir()]
    return found[0] if len(found) == 1 else name


def _folder_hits(board: Path, short: str) -> list[str]:
    """Every Design Page a short folder name finds on a board, as board-relative paths: the plain
    2-Design/ and each 2-Design-M<NN>-<slug>/ method folder; `M01/Design-01` keeps one method."""
    from live.designboard import design_groups
    method, _, name = short.rpartition("/")
    found = []
    for g in design_groups(board):
        if method and method.lower() not in (g["key"].lower(), g["group"].lower()):
            continue
        current = renamed_folder(board, name, g["group"])
        page = g["dir"] / current / f"{current}.md"
        if page.is_file():
            found.append(f'{g["group"]}/{current}/{current}.md')
    return found
