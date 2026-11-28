"""Where an Evidence Item's binding points on disk: one resolver for every reader (export, health, Draft Lab).

`resolve(path, root, page_dir)` tries the path as written, then from the repository root, the Page folder and each
folder above it up to its Board (the folder with board.md): a Paper Board's Section binds a citation Job's Run by its
Board-relative path (`j03_evidence_cite/tNN_<group>/runs/r01_check_citations/result/citations.csv`, written by
hai-paper-evidence `cite_tasks.py bind`). A path from before the world and folder renames is found where it
lives today (`moved_path`).
"""
from pathlib import Path


def up_to_board(page_dir: Path) -> list:
    """The Page folder and the folders above it, through its Board (board.md), at most four levels up."""
    out = []
    for folder in [Path(page_dir), *Path(page_dir).parents][:5]:
        out.append(folder)
        if (folder / "board.md").is_file():
            break
    return out


_WORLD_RENAMES = {"discoveries": "discovery", "tasks": "work", "papers": "paper"}


def moved_path(root: Path, rel: str):
    """Where a receipt's repository path lives today, or None. A receipt keeps the path its Run had (AGENTS.md:
    written once), so `examples/<Project>/discoveries/…/<task>/results/<run>` (before 261010-261014) is found as
    `<examples-N-world>/<Project>/discovery/…/<task>/runs/<run>/result` (MISQ t01, 261022)."""
    parts = Path(rel).parts
    if len(parts) < 3 or not parts[0].startswith("examples"):
        return None
    worlds = [w for w in sorted(Path(root).glob("examples*")) if (w / parts[1]).is_dir()]
    if len(worlds) != 1:
        return None
    rest = [_WORLD_RENAMES.get(parts[2], parts[2]), *parts[3:]]
    for i, part in enumerate(rest[:-1]):
        if part == "results" and i + 1 < len(rest):
            rest = rest[:i] + ["runs", rest[i + 1], "result"] + rest[i + 2:]
            break
    candidate = worlds[0] / parts[1] / Path(*rest)
    return candidate if candidate.exists() else None


def resolve(path_str: str, root: Path, page_dir: Path):
    """Return the Result path a local binding points at, or None. A note after the path (`… · supersedes …`) is not
    part of it, and a path from before the world and folder renames is found where it lives today."""
    if not path_str:
        return None
    for text in dict.fromkeys([path_str, path_str.split(" · ")[0].strip().strip("`")]):
        p = Path(text)
        candidates = [p] if p.is_absolute() else [root / p, *(f / p for f in up_to_board(page_dir)),
                                                     Path.cwd() / p]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        if not p.is_absolute() and (moved := moved_path(root, text)) is not None:
            return moved
    return None
