"""The DesignBoard's two writes: add design tasks to the Brief's list, and open a Design Folder for a line
(split from designboard.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path

from live.design import (
    _declared_insight_boards, _read,
    brief_page, brief_rows, design_title, is_task_header, venue_word,
)
from live.designboard_snapshot import DESIGN_GROUP, _FOLDER_ID, design_groups


_ROW = re.compile(r"^\s*\|(.+)\|\s*$")


_TABLE_COLUMNS = ("line", "audience", "job", "venue", "designs", "insight", "folder")


# ----------------------------------------------------------------- writes --

_FILLER = {"a", "an", "the", "with", "within", "of", "for", "to", "in", "on", "or", "and", "at", "by", "under", "over"}


def _slug(text: str, words: int = 3) -> str:
    """The first content words of a Brief cell, so a folder name says the goal."""
    parts = [p for p in re.sub(r"[^a-z0-9]+", " ", text.lower()).split() if p and p not in _FILLER]
    return "-".join(parts[:words]) or "item"


def _table_bounds(lines: list[str]) -> tuple[int, int, list[str]] | None:
    """(header index, index after the last row, header cells lowercased) of the list table."""
    for i, line in enumerate(lines):
        hit = _ROW.match(line)
        if not hit:
            continue
        cells = [c.strip().lower() for c in hit.group(1).split("|")]
        if is_task_header(cells):
            end = i + 1
            while end < len(lines) and _ROW.match(lines[end]):
                end += 1
            return i, end, cells
    return None


def _ensure_columns(lines: list[str], start: int, end: int, header: list[str]) -> tuple[list[str], list[str]]:
    """Add any missing list columns (designs, insight, folder) to the header, the separator, and every row."""
    missing = [c for c in ("designs", "insight", "folder") if not any(c in h for h in header)]
    if not missing:
        return lines, header
    # keep folder last: insert new columns before it when it exists
    header_cells = [c.strip() for c in _ROW.match(lines[start]).group(1).split("|")]
    folder_at = next((i for i, c in enumerate(header_cells) if "folder" in c.lower()), None)
    insert_at = folder_at if folder_at is not None else len(header_cells)
    add = [c for c in missing if c != "folder"]
    new_lines = list(lines)
    for i in range(start, end):
        cells = [c.strip() for c in _ROW.match(new_lines[i]).group(1).split("|")]
        while len(cells) < len(header_cells):
            cells.append("")
        if i == start:
            fill = add
        elif all(set(c) <= set("-: ") for c in cells):
            fill = ["---"] * len(add)
        else:
            fill = [""] * len(add)
        cells = cells[:insert_at] + fill + cells[insert_at:]
        if "folder" in missing:
            cells.append("folder" if i == start else "---" if all(set(c) <= set("-: ") for c in cells[:1]) else "")
        new_lines[i] = "| " + " | ".join(cells) + " |"
    return new_lines, [c.strip().lower() for c in _ROW.match(new_lines[start]).group(1).split("|")]


def add_tasks(board_root: Path, subgroups: list[str], job: str, venue: str, designs: int,
              insight: str = "", open_folders: bool = True) -> dict:
    """Add one design task per subgroup to the Brief's list, and optionally open its folder."""
    subgroups = [s.strip() for s in subgroups if s and s.strip()]
    if not subgroups:
        raise ValueError("name at least one subgroup, one per line")
    if not job.strip():
        raise ValueError("say what the recipient is trying to do (their job)")
    if not venue.strip():
        raise ValueError("name the venue (sms · ui-card · email · push)")
    if designs < 1:
        raise ValueError("how many designs must be 1 or more")
    brief = brief_page(board_root)
    if brief is None:
        raise ValueError("no design task file under 0-BR-brief/; the list of designs lives there")
    if insight and not _declared_insight_boards(board_root, [insight]):
        raise ValueError(f"Insight board {insight!r} was not found beside this board")
    text = _read(brief)
    lines = text.splitlines()
    bounds = _table_bounds(lines)
    if bounds is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines += ["### What to design", "",
                  "| " + " | ".join(_TABLE_COLUMNS) + " |", "|" + "---|" * len(_TABLE_COLUMNS)]
        bounds = _table_bounds(lines)
    start, end, header = bounds
    lines, header = _ensure_columns(lines, start, end, header)
    start, end, header = _table_bounds(lines)
    existing = brief_rows("\n".join(lines))
    numbers = [int(m.group(1)) for r in existing if (m := re.match(r"^R(\d+)$", r["id"]))]
    next_number = max(numbers, default=0) + 1
    new_ids = []
    new_rows = []
    for offset, who in enumerate(subgroups):
        row_id = f"R{next_number + offset}"
        cells = []
        for key in header:
            if "audience" in key:
                cells.append(who)
            elif "job" in key:
                cells.append(job.strip())
            elif "venue" in key:
                cells.append(venue.strip())
            elif "design" in key or "wanted" in key or "how many" in key:
                cells.append(str(designs))
            elif "insight" in key:
                cells.append(f"`{insight}`" if insight else "")
            elif "folder" in key:
                cells.append("—")
            elif key in ("line", "row", "id", "#", "page"):
                cells.append(row_id)
            else:
                cells.append("")
        new_rows.append("| " + " | ".join(cells) + " |")
        new_ids.append(row_id)
    lines[end:end] = new_rows
    brief.write_text("\n".join(lines) + "\n", encoding="utf-8")
    folders = []
    if open_folders:
        for row_id in new_ids:
            folders.append(new_folder(board_root, row_id)["folder"])
    return {"lines": new_ids, "folders": folders, "brief": brief.name}


def new_folder(board_root: Path, row_id: str, method: str = "") -> dict:
    """Open a Design Folder for one Brief line that has none, and name it on the line.

    The line is found by its place in the task table (a Brief with no `line`
    column still numbers its rows R1, R2 …), and the folder cell is written on
    that same row, so a second click finds the folder and refuses (audit L9)."""
    brief = brief_page(board_root)
    if brief is None:
        raise ValueError("no design task file under 0-BR-brief/; the list of designs lives there")
    text = _read(brief)
    rows = brief_rows(text)
    index = next((n for n, r in enumerate(rows) if r["id"] == row_id), None)
    if index is None:
        raise ValueError(f"that design task is not in {brief.name}; reload the page")
    row = rows[index]
    if method:
        return _new_method_folder(board_root, brief, text, rows, index, method)
    if row["folder"]:
        raise ValueError(f"{design_title(row)} already has its folder {row['folder']}")
    lines = text.splitlines()
    bounds = _table_bounds(lines)
    if bounds is None:
        raise ValueError(f"no design-task table in {brief.name}")
    lines, header = _ensure_columns(lines, *bounds)
    start, end, header = _table_bounds(lines)
    data_rows = [i for i in range(start + 1, end)
                 if not all(set(c.strip()) <= set("-: ") for c in _ROW.match(lines[i]).group(1).split("|"))]
    target = data_rows[index]
    folder_col = next(i for i, c in enumerate(header) if "folder" in c)
    group = board_root / DESIGN_GROUP
    group.mkdir(exist_ok=True)
    numbers = [int(m.group(1)) for p in group.iterdir() if (m := _FOLDER_ID.match(p.name))]
    name = f"Design-{max(numbers, default=0) + 1:02d}-{_slug(row['audience'])}-{_slug(row['job'])}-{_slug(row['venue'])}"
    return _finish_new_folder(board_root, brief, text, lines, target, folder_col, name, row)


def _write_design_folder(folder: Path, name: str, row: dict, method: str = "") -> None:
    """A new Design Folder: its Page and its empty Design Item register."""
    board_root = folder.parent.parent
    title = design_title(row)
    wanted = row["designs"]
    count = "" if wanted == 1 else f"{wanted} " if wanted else ""
    ask = (f"Which {count}{row['job'].strip()} {venue_word(row['venue'])} design{'' if wanted == 1 else 's'} "
           f"should we make for {row['audience'].strip()}?")
    folder.mkdir()
    (folder / f"{name}.md").write_text(
        f"# {title}\nfolder-kind: design\n" + (f"method: {method} · `../method.md`\n" if method else "")
        + f"state: 🔴 OPEN · no design registered yet\nowner: {_owner(board_root)}\n\n"
        f"## Opening\n\n{ask}\n\nListed in the board's design tasks.\n\n"
        f"## Outline\n\nDesign Items are registered in `draft/{name}-design-items.md`; their drafts,\n"
        "verifications are `run-design-*` Runs; a passed Verify is ready for Delivery.\n\n## Content\n\nDraft wording lives in "
        "immutable Design Run Results, never here.\n\n## Aims\n\n### A1 · Every registered item reaches a "
        "truthful terminal decision\n\n- ⬜ A1.1 · pass Verify so the item is ready for Delivery.\n",
        encoding="utf-8")
    (folder / "draft").mkdir()
    (folder / "draft" / f"{name}-design-items.md").write_text(
        f"# {title} · Design Items\n\nOne block per design target: the goal, its evidence, and its acceptance rules.\n"
        "Runs name an item through `item:`; state is derived from those Runs, never typed here.\n",
        encoding="utf-8")


def _finish_new_folder(board_root, brief, text, lines, target, folder_col, name, row) -> dict:
    group = board_root / DESIGN_GROUP
    _write_design_folder(group / name, name, row)
    cells = [c.strip() for c in _ROW.match(lines[target]).group(1).split("|")]
    while len(cells) <= folder_col:
        cells.append("")
    cells[folder_col] = f"`{name}`"
    lines[target] = "| " + " | ".join(cells) + " |"
    brief.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    _list_page(board_root, f"{DESIGN_GROUP}/{name}/{name}.md")
    return {"folder": name, "rel": f"{DESIGN_GROUP}/{name}/{name}.md", "brief_updated": True}


def _new_method_folder(board_root: Path, brief: Path, text: str, rows: list[dict], index: int, method: str) -> dict:
    """One Brief task's Design Folder under one method: the task's Design-NN name, the same under
    every method. A task with no folder name yet takes the next free number, written to the Brief."""
    groups = {g["group"]: g for g in design_groups(board_root) if g["key"]}
    if method not in groups:
        raise ValueError(f"no method folder {method!r} on this board")
    row, group = rows[index], groups[method]["dir"]
    name, brief_updated = row["folder"], False
    if not name:
        used = [int(m.group(1)) for g in design_groups(board_root) for p in g["dir"].iterdir()
                if (m := _FOLDER_ID.match(p.name))]
        used += [int(m.group(1)) for r in rows if (m := _FOLDER_ID.match(r["folder"] or ""))]
        name = f"Design-{max(used, default=0) + 1:02d}-{_slug(row['audience'])}-{_slug(row['job'])}-{_slug(row['venue'])}"
        lines = text.splitlines()
        lines, _ = _ensure_columns(lines, *_table_bounds(lines))
        start, end, header = _table_bounds(lines)
        data_rows = [i for i in range(start + 1, end)
                     if not all(set(c.strip()) <= set("-: ") for c in _ROW.match(lines[i]).group(1).split("|"))]
        folder_col = next(i for i, c in enumerate(header) if "folder" in c)
        cells = [c.strip() for c in _ROW.match(lines[data_rows[index]]).group(1).split("|")]
        while len(cells) <= folder_col:
            cells.append("")
        cells[folder_col] = f"`{name}`"
        lines[data_rows[index]] = "| " + " | ".join(cells) + " |"
        brief.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
        brief_updated = True
    if (group / name).exists():
        raise ValueError(f"{design_title(row)} already has its folder under {method}")
    _write_design_folder(group / name, name, row, method=groups[method]["label"])
    rel = f"{method}/{name}/{name}.md"
    _list_page(board_root, rel)
    return {"folder": name, "rel": rel, "brief_updated": brief_updated}


def _owner(board_root: Path) -> str:
    """The person a new page names as owner: the board's own owner line, else the Brief's."""
    for page in (Path(board_root) / "board.md", brief_page(board_root)):
        hit = re.search(r"(?m)^owner:\s*(\S.*?)\s*$", _read(page)) if page else None
        if hit:
            return hit.group(1)
    return "person"


def _list_page(board_root: Path, rel: str) -> None:
    """Add a new Design Folder page to board.md's Pages, under its Design heading when there is one."""
    board_md = Path(board_root) / "board.md"
    text = _read(board_md)
    if not text or rel in text:
        return
    lines = text.splitlines()
    pages = next((i for i, l in enumerate(lines) if re.match(r"^##\s+Pages\b", l)), None)
    if pages is None:
        lines.extend(["", "## Pages"])
        pages = len(lines) - 1
    stop = next((i for i in range(pages + 1, len(lines)) if re.match(r"^##\s", lines[i])), len(lines))
    heading = next((i for i in range(pages + 1, stop) if re.match(r"^###\s+.*Design", lines[i])), None)
    at = stop
    if heading is not None:
        at = next((i for i in range(heading + 1, stop) if re.match(r"^###\s", lines[i])), stop)
    while at > pages + 1 and not lines[at - 1].strip():
        at -= 1
    lines[at:at] = [rel]
    board_md.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
