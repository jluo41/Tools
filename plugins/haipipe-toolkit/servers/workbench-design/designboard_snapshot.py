"""Finding DesignBoards and reading one into a snapshot: its groups of Design Folders, its Brief rows, its
Insight space (split from designboard.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from live.design import (
    _READS as _READS_LINE, _TITLE, _declared_insight_boards, _handoff_says, _insight_bindings, _read,
    brief_page, brief_rows, design_snapshot,
)


_FIELD = re.compile(r"(?m)^\s*([a-z][a-z-]*):\s*(.*?)\s*$", re.I)
_DESIGN_BOARD = re.compile(r"(?:^|[-_])designboard(?:$|[-_])", re.I)
_BOARD_GLOBS = ("examples*/*/designs/*/board.md",     # a Project's designs/ world
                "examples*/*/applications/*/board.md", "examples*/*/*/board.md",
                "designs/*/board.md", "applications/*/board.md",   # a Project folder served as the root
                "*/board.md", "board.md")


DESIGN_GROUP = "2-Design"                      # the group folder of Design Folders
_FOLDER_ID = re.compile(r"^Design-(\d+)-")     # Design-01-<audience>-<job>-<venue>
# One method per group: beside or instead
# of the plain 2-Design/, a board may hold 2-Design-M<NN>-<slug>/ folders, each with its method.md
# card (See input · Conduct process · Check output) and one Design Folder per Brief task, numbered
# as the Brief numbers it, so Design-01 is the same task under every method.
_METHOD_GROUP = re.compile(r"^2-Design-(M\d+)-(.+)$")
METHOD_CARD = "method.md"


def _field(text: str, name: str) -> str:
    for key, value in _FIELD.findall(text):
        if key.lower() == name.lower():
            return value.strip().strip("'\"")
    return ""


def is_design_board(board_root: Path) -> bool:
    board_root = Path(board_root)
    text = _read(board_root / "board.md")
    return (_field(text, "board-kind").lower() in {"design", "design-board"}
            or bool(_DESIGN_BOARD.search(board_root.name))
            or (board_root / DESIGN_GROUP).is_dir()
            or any(p.is_dir() and _METHOD_GROUP.match(p.name) for p in board_root.glob("2-Design-M*")))


def design_groups(board_root: Path) -> list[dict]:
    """The board's groups of Design Folders: the plain 2-Design/ when it exists (one method, or
    before methods), then one 2-Design-M<NN>-<slug>/ per method, in number order."""
    board_root = Path(board_root)
    groups = []
    if (board_root / DESIGN_GROUP).is_dir():
        groups.append({"dir": board_root / DESIGN_GROUP, "group": DESIGN_GROUP, "key": "",
                       "label": "no method stated", "card": None})
    for d in sorted(board_root.glob("2-Design-M*"), key=lambda p: (len(p.name.split("-")[2]), p.name)):
        hit = _METHOD_GROUP.match(d.name)
        if not (d.is_dir() and hit):
            continue
        card = d / METHOD_CARD
        title = _TITLE.search(_read(card)) if card.is_file() else None
        groups.append({"dir": d, "group": d.name, "key": hit.group(1),
                       "label": title.group(1).strip() if title else f"{hit.group(1)} · {hit.group(2).replace('-', ' ')}",
                       "card": card if card.is_file() else None})
    return groups


def design_boards(root: Path) -> list[Path]:
    found = {}
    for pattern in _BOARD_GLOBS:
        for board_md in Path(root).glob(pattern):
            if is_design_board(board_md.parent):
                found.setdefault(board_md.parent.resolve(), board_md.parent)
    return sorted(found.values(), key=lambda p: p.name)


def resolve_board(root: Path, raw: str) -> Path | None:
    """``?path=/…/board.md`` (browser pathname) or ``?board=<folder name>``.

    A bare link (no board named) opens the only DesignBoard the server has:
    the root itself, or the single one under it.
    """
    root = Path(root)
    value = unquote(raw or "").split("?", 1)[0].split("#", 1)[0].strip()
    if not value:
        if (root / "board.md").is_file() and is_design_board(root):
            return root
        only = design_boards(root)
        return only[0] if len(only) == 1 else None
    if "/" not in value.strip("/") and not value.endswith("board.md"):
        name = value.strip("/")
        boards = design_boards(root)
        matches = [b for b in boards if b.name == name]
        if not matches:  # the start of the name is enough when it is unique: ?board=B00
            matches = [b for b in boards if b.name.lower().startswith(name.lower())]
        return matches[0] if len(matches) == 1 else None
    try:
        resolved = (root / value.lstrip("/")).resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError, RuntimeError):
        return None
    if resolved.is_file() and resolved.name == "board.md":
        resolved = resolved.parent
    return resolved if (resolved / "board.md").is_file() else None


def reads_names(board_root: Path) -> list[str]:
    """The Insight boards named on ``board.md`` ``reads:``, in order."""
    match = _READS_LINE.search(_read(Path(board_root) / "board.md"))
    if not match:
        return []
    return [n.strip().strip("`'\"") for n in re.split(r"\s*·\s*", match.group(1)) if n.strip()]


# --------------------------------------------------------------- snapshot --

def design_board_snapshot(board_root: Path, server_root: Path | None = None,
                          static: bool = False) -> dict:
    board_root = Path(board_root)
    server_root = Path(server_root or board_root)
    text = _read(board_root / "board.md")
    title = _TITLE.search(text).group(1).strip() if _TITLE.search(text) else board_root.name
    brief = brief_page(board_root)
    brief_lines = brief_rows(_read(brief)) if brief else []
    groups = design_groups(board_root)
    folders = []
    for g in groups:
        for page_dir in sorted(g["dir"].iterdir()):
            page = page_dir / f"{page_dir.name}.md"
            if not page_dir.is_dir() or not page.is_file():
                continue
            snap = design_snapshot(page, server_root)
            snap["name"] = page_dir.name
            snap["rel"] = f'{g["group"]}/{page_dir.name}/{page.name}'
            snap["group"], snap["method_key"], snap["method_label"] = g["group"], g["key"], g["label"]
            # a method's folder is named with its method, since Design-01 recurs under every method
            snap["label"] = f'{g["key"]} · {page_dir.name}' if g["key"] else page_dir.name
            folders.append(snap)
    number = lambda name: int(_FOLDER_ID.match(name).group(1)) if _FOLDER_ID.match(name or "") else None
    matched: set[str] = set()
    for row in brief_lines:
        # the plain group's folder by its exact name; a method's folder by its name or its Design-NN
        no = number(row["folder"])
        row["snapshots"] = [f for f in folders if f["name"] == row["folder"]
                            or (f["method_key"] and no is not None and number(f["name"]) == no)]
        matched |= {f["rel"] for f in row["snapshots"]}
        plain = [f for f in row["snapshots"] if not f["method_key"]]
        row["snapshot"] = plain[0] if plain else (row["snapshots"][0] if len(row["snapshots"]) == 1 else None)
        row["status"] = ("no folder yet" if not row["folder"] else
                         f'{len(row["snapshots"])} methods' if row["snapshot"] is None and row["snapshots"] else
                         "folder missing on disk" if row["snapshot"] is None else
                         row["snapshot"]["reason"] if not row["snapshot"]["current"] else
                         _folder_summary(row["snapshot"]))
        row["registered"] = sum(len(f["items"]) for f in row["snapshots"])
        row["ready"] = sum(1 for f in row["snapshots"] for i in f["items"] if i.get("ready"))
    items = [dict(item, folder=f["label"], rel=f["rel"], folder_name=f["name"], method=f["method_key"])
             for f in folders for item in f["items"]]
    runs = sorted((dict(run, folder=f["label"]) for f in folders for run in f["runs"]),
                  key=lambda r: (r["finished"] or r["started"] or "", r["number"]), reverse=True)
    waiting = [i for i in items if i["waiting"]]
    waiting.sort(key=lambda i: (i["waiting"].startswith("agent"), i["folder"], i["id"]))
    try:
        rel = board_root.resolve().relative_to(server_root.resolve()).as_posix()
        if rel == ".":
            rel = ""          # the board is the server root: links say /board.md, not /./board.md
    except ValueError:
        rel = ""
    # Insight: the board's reads: plus every board a Brief line names, once each.
    names = reads_names(board_root)
    for row in brief_lines:
        if row["insight"] and row["insight"] not in names:
            names.append(row["insight"])
    names = [n for n in names if _declared_insight_boards(board_root, [n])]   # a dead or non-Insight entry is not offered
    insight = _insight_bindings(board_root / "board.md", server_root, names or None)
    return {
        "title": title, "board": board_root, "root": server_root, "static": static,
        "reads": _field(text, "reads"), "close": _field(text, "close"),
        "brief": brief, "brief_rows": brief_lines, "folders": folders,
        "unlisted": [f for f in folders if f["rel"] not in matched],
        "methods": [g for g in groups if g["key"]] and groups,      # every group once any method exists
        "items": items, "runs": runs, "waiting": waiting,
        "ready": [i for i in items if i.get("ready")],
        "audit": [f'{f["label"]}: {issue}' for f in folders for issue in f["audit"]],
        "insight": insight, "insight_names": names,
        "insight_space": _board_insight_space(folders, insight),
        "totals": {"lines": len(brief_lines), "wanted": sum(r["designs"] for r in brief_lines),
                   "registered": len(items), "ready": sum(1 for i in items if i.get("ready"))},
        "human": next((f["human"] for f in folders if f["human"] != "person"), "person"),
        "relative": rel, "current": is_design_board(board_root),
    }


def _folder_summary(snap: dict) -> str:
    if not snap["items"]:
        return "no Design Item yet"
    counts: dict[str, int] = {}
    for item in snap["items"]:
        counts[item["state"]] = counts.get(item["state"], 0) + 1
    return " · ".join(f"{n} {state}" for state, n in counts.items())


def _board_insight_space(folders: list[dict], insight: dict) -> list[dict]:
    """Every signed page on the boards the programme reads, and who uses it."""
    used: dict[Path, list[str]] = {}
    for f in folders:
        for block in f["insight_space"]["items"]:
            for r in block["rows"]:
                if r["exists"]:
                    try:
                        used.setdefault(r["file"].resolve(), []).append((f["name"], f["rel"], block["item"]["id"]))
                    except OSError:
                        pass
    boards = []
    for board in insight["boards"]:
        pages = []
        for h in board["handoffs"]:
            page = Path(h["page"])
            if not page.is_absolute():
                page = Path(board["board"]) / page
            try:
                resolved = page.resolve()
            except OSError:
                resolved = page
            says = _handoff_says(_read(page))
            pages.append({"title": h["title"], "name": page.name, "file": page,
                          "signed": h["signature"] if h["signed"] else "",
                          "finding": says["finding"], "counsel": says.get("counsel", []),
                          "used_by": used.get(resolved, [])})
        boards.append({"title": board["title"], "live_url": board["live_url"], "pages": pages})
    # pages the items rest on that are not signed insights: shown too, so nothing an item uses is hidden
    listed = {Path(p["file"]).resolve() for b in boards for p in b["pages"]}
    others = [{"title": (re.search(r"(?m)^#\s+(.+?)\s*$", _read(f)) or [None, f.stem])[1], "name": f.name, "file": f,
               "signed": "", "finding": "", "counsel": [], "used_by": users}
              for f, users in sorted(used.items(), key=lambda kv: kv[0].as_posix()) if f not in listed]
    if others:
        boards.append({"title": "Other pages the designs use (not signed insights)", "live_url": "", "pages": others,
                       "unsigned": True})
    return boards
