"""🎨 Design Board · the Board-level grain of the Design workbench.

One DesignBoard holds a Brief with a list of designs (one line per audience ×
job × venue, with how many designs it asks for and which Insight board it
draws from) and many Design Folders under ``2-Design/``.  This presenter
stacks every folder's ``design_snapshot`` into one view, in the same five
Spaces as the Page level, one grain up: Goal (the list of design tasks),
Design (every item), Insight (the boards and pages the programme draws on),
Run (who is waited on, what ran), Delivery (what is ready for handoff).  It reads the
same files as the Page level and stores nothing of its own.  Its two writes
are adding design tasks to the design task file (0-BR-brief) and opening a Design Folder for a
line that has none yet.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlparse

from host_paths import SKILLS
from live.design import (
    _declared_insight_boards, _handoff_says, _insight_bindings, _read, because_words, shared_rules,
    brief_page, brief_rows, with_link, design_runs_panel, design_snapshot, design_title, runs_panel_assets,
    is_task_header, venue_word,
)

_TITLE = re.compile(r"(?m)^#\s+(.+?)\s*$")
_FIELD = re.compile(r"(?m)^\s*([a-z][a-z-]*):\s*(.*?)\s*$", re.I)
_READS_LINE = re.compile(r"(?im)^\s*reads:\s*(.*?)\s*$")
_DESIGN_BOARD = re.compile(r"(?:^|[-_])designboard(?:$|[-_])", re.I)
_BOARD_GLOBS = ("examples*/*/designs/*/board.md",     # a Project's designs/ world (JL 261001)
                "examples*/*/applications/*/board.md", "examples*/*/*/board.md",
                "designs/*/board.md", "applications/*/board.md",   # a Project folder served as the root
                "*/board.md", "board.md")
_ROW = re.compile(r"^\s*\|(.+)\|\s*$")
DESIGN_GROUP = "2-Design"                      # the group folder of Design Folders
_FOLDER_ID = re.compile(r"^Design-(\d+)-")     # Design-01-<audience>-<job>-<venue>
_TABLE_COLUMNS = ("line", "audience", "job", "venue", "designs", "insight", "folder")


def _e(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


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
            or (board_root / DESIGN_GROUP).is_dir())


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
    group = board_root / DESIGN_GROUP
    folders = []
    for page_dir in sorted(group.iterdir()) if group.is_dir() else []:
        page = page_dir / f"{page_dir.name}.md"
        if not page_dir.is_dir() or not page.is_file():
            continue
        snap = design_snapshot(page, server_root)
        snap["name"] = page_dir.name
        snap["rel"] = f"{DESIGN_GROUP}/{page_dir.name}/{page.name}"
        folders.append(snap)
    by_name = {f["name"]: f for f in folders}
    for row in brief_lines:
        row["snapshot"] = by_name.get(row["folder"])
        row["status"] = ("no folder yet" if not row["folder"] else
                         "folder missing on disk" if row["snapshot"] is None else
                         row["snapshot"]["reason"] if not row["snapshot"]["current"] else
                         _folder_summary(row["snapshot"]))
        row["registered"] = len(row["snapshot"]["items"]) if row["snapshot"] else 0
        row["ready"] = sum(1 for i in row["snapshot"]["items"] if i.get("ready")) if row["snapshot"] else 0
    listed = {row["folder"] for row in brief_lines if row["folder"]}
    items = [dict(item, folder=f["name"], rel=f["rel"]) for f in folders for item in f["items"]]
    runs = sorted((dict(run, folder=f["name"]) for f in folders for run in f["runs"]),
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
        "unlisted": [f for f in folders if f["name"] not in listed],
        "items": items, "runs": runs, "waiting": waiting,
        "ready": [i for i in items if i.get("ready")],
        "audit": [f'{f["name"]}: {issue}' for f in folders for issue in f["audit"]],
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


def _used_by(snapshot: dict, users: list[tuple]) -> str:
    """Who uses a page, per folder: 'Design-01 · 6 items', each linked to that folder's Insight Space."""
    if not users:
        return "<span class=mut>no item yet</span>"
    per: dict[str, list] = {}
    for name, rel, item in users:
        per.setdefault((name, rel), []).append(item)
    return " · ".join(f'<a href="{_e(_page_url(snapshot, rel, "design"))}">{_e(name.split("-", 2)[0] + "-" + name.split("-", 2)[1])}</a> '
                      f'<span class=mut>{len(ids)} item{"s" if len(ids) != 1 else ""}</span>'
                      for (name, rel), ids in per.items())


# ----------------------------------------------------------------- render --

_CSS = """
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8;--ext:#7a4f9a}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a;--ext:#b896d6}}
*{box-sizing:border-box}body{margin:0;padding:16px 18px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px}
h1{font-size:17px;margin:0 0 2px;font-weight:650}h2{font-size:14px;margin:18px 0 6px;font-weight:650}
.mut{color:var(--mut);font-size:12.5px}.bad{color:var(--bad)}.ok{color:var(--ok)}
.tabs{display:flex;gap:4px;margin:12px 0 4px;border-bottom:1px solid var(--line)}
.tabs button{font:600 12.5px -apple-system,sans-serif;border:0;border-bottom:2px solid transparent;padding:6px 10px;cursor:pointer;background:transparent;color:var(--mut)}
.tabs button.on{color:var(--fg);border-bottom-color:var(--acc)}
.pane{display:none}.pane.on{display:block}
table{border-collapse:collapse;width:100%;margin:4px 0 8px}td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
code{font:12px ui-monospace,Menlo,monospace;word-break:break-word}a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
tr.me td{background:var(--soft)}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:8px 0}.card .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
pre.text{margin:8px 0;padding:10px 12px;background:var(--soft);border-left:3px solid var(--acc);font:15px/1.45 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
table.designs td.who{width:230px}.design{white-space:pre-wrap;word-break:break-word;font-size:14.5px}
img.shot{display:block;width:100%;height:auto;margin:0 0 6px;border:1px solid var(--line);border-radius:18px;background:#fff}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:20px 18px;margin:10px 0}.gallery figure{margin:0}.gallery figcaption{font-size:13px;line-height:1.35}
button.do{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:4px;padding:3px 9px;background:var(--bg);color:var(--acc);cursor:pointer}
.msg{font-size:12.5px}.msg.bad{color:var(--bad)}.msg.ok{color:var(--ok)}
.empty{color:var(--mut);padding:10px 0}
details{margin:2px 0}summary{cursor:pointer;color:var(--acc);font-size:12.5px}
.form{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;max-width:760px;margin:6px 0}.form label{color:var(--mut);font-size:12px;padding-top:5px}
.form input,.form textarea,.form select{font:13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:4px;padding:4px 6px;background:var(--bg);color:var(--fg)}
.form textarea{min-height:72px}.form .full{grid-column:1/3}
details.taskblock{border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:8px 0}details.taskblock>summary{font-size:14px;color:var(--fg)}
.task{border:1px solid var(--acc);border-radius:8px;background:var(--soft);padding:8px 12px;margin:10px 0}
article.theory{max-width:980px}article.theory h1{font-size:16px;margin:8px 0 6px}article.theory h2{margin:22px 0 6px}
article.theory p{margin:6px 0;line-height:1.55}pre.theory{margin:8px 0;padding:10px 12px;background:var(--soft);border-radius:6px;font:12px/1.5 ui-monospace,Menlo,monospace;overflow-x:auto}
.views{display:flex;gap:6px;margin:4px 0 12px}.views button{font:600 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:14px;padding:3px 11px;background:transparent;color:var(--mut);cursor:pointer}
.views button.on{color:var(--fg);border-color:var(--acc);background:var(--soft)}.view{display:none}.view.on{display:block}
.rp-head{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}
details.rp-venues{margin:0 0 10px}details.rp-more{margin:2px 0 4px}details.rp-more>summary{font-size:12.5px;color:var(--mut);padding:2px 0}details.rp-more[open]>summary{margin-bottom:4px}details.rp-venues>div{margin-top:4px;line-height:1.6}
.lw-k{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--acc);margin:14px 0 6px}.lw-kn{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85;margin-left:6px}
.rp-group{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 4px}
.rp-card+.rp-card{border-top:1px solid var(--line)}
.rp-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}
.rp-card>summary::-webkit-details-marker{display:none}.rp-card>summary:hover,.rp-card[open]>summary{background:var(--soft)}
.bjt-chev{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}.rp-card[open]>summary .bjt-chev{transform:rotate(90deg)}
.lw-sum{min-width:0}.rp-title{font-weight:600;font-size:14.5px;line-height:1.4;color:var(--fg)}
.rp-sub{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}
.rp-marks{display:flex;gap:10px;flex:none}.rp-utd{font:700 10.5px -apple-system,sans-serif;color:#9c6500;border:1px solid #e3c27a;border-radius:4px;padding:0 4px;letter-spacing:.03em}.rp-q{color:var(--acc);font-weight:600}.rp-q.rp-evidence{color:var(--ok)}.rp-q.rp-classic{color:var(--mut)}
.rp-body{padding:6px 14px 14px calc(14px + 1em + 6px)}.rp-why{font-size:14.5px;line-height:1.55;margin:4px 0 6px}
.rp-acts{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}.rp-nopdf{font-size:13.5px;margin-top:8px}
details.rp-absd>summary{font-size:13px;color:var(--mut);cursor:pointer}details.rp-absd>p{font-size:13.5px;line-height:1.55;margin:4px 0 6px}
.st-bar{display:flex;justify-content:space-between;gap:12px;align-items:baseline;margin:0 0 6px;font-size:13px}
.st-frame{display:block;width:100%;height:calc(100vh - 210px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:#fff}
.rp-frame{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}
table.mdt{display:table;width:100%;border-collapse:collapse;margin:6px 0 14px;font-size:13.5px}
table.mdt td:first-child{font-weight:600;white-space:nowrap}
.mcards{margin:8px 0 16px}.mc-fam{font-size:13px;margin:14px 0 6px;padding:5px 10px;background:var(--soft);border-radius:6px}
details.mcard{border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--bg)}
details.mcard>summary{color:var(--fg);list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:11px 14px}
details.mcard>summary::-webkit-details-marker{display:none}details.mcard>summary:hover,details.mcard[open]>summary{background:var(--soft)}
details.mcard[open]>summary .bjt-chev{transform:rotate(90deg)}
.mc-top{display:flex;align-items:baseline;gap:8px}.mnum{color:var(--mut);font-weight:500}.mc-name{font-weight:650;font-size:15px}
.mc-status{margin-left:auto;font:600 11.5px -apple-system,sans-serif;white-space:nowrap}.mc-status.ok{color:var(--ok)}.mc-status.gap{color:var(--bad)}.mc-status.future{color:var(--acc)}
details.mcard.future{border-style:dashed;border-color:var(--acc)}
.mc-move{margin:2px 0 6px;font-size:14px;line-height:1.45}
.mc-io,.mc-from,.mc-tests,.mc-papers{font-size:12.5px;line-height:1.7}.mc-io .arrow{color:var(--mut);margin:0 6px}
.lbl{display:inline-block;min-width:7.2em;margin-right:4px;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
.mc-io .lbl+.chip{margin-left:0}.mc-from .src{white-space:normal}
/* the three inputs a design reads: its requirements, internal insights, external insights */
.chip.in-req{border-color:var(--acc);color:var(--acc)}.chip.in-int{border-color:var(--ok);color:var(--ok)}.chip.in-ext{border-color:var(--ext);color:var(--ext)}
.mc-body{padding:4px 14px 14px calc(14px + 1em + 6px)}
.mc-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;margin:6px 0 10px}
@media(max-width:900px){.mc-cols{grid-template-columns:minmax(0,1fr)}}
.mc-col{border:1px solid var(--line);border-radius:8px;padding:10px 12px}.mc-col.ai{border-color:var(--acc);background:var(--soft)}
.mc-h{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 6px}.mc-col.ai .mc-h{color:var(--acc)}
.mc-col dl{margin:0}.mc-col dt{font-weight:650;font-size:12.5px;margin:6px 0 1px}.mc-col dd{margin:0;font-size:13px;line-height:1.5}
.mc-col .line{margin:0 0 3px}.mc-tests .when{margin:0 4px 0 14px}.mc-tests .lbl+.when{margin-left:0}
.chip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap}
a.pchip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap;background:var(--bg)}
a.pchip:hover{border-color:var(--acc);text-decoration:none}a.pchip .rp-pdf{margin-left:5px;font-size:9.5px;padding:0 4px}
.tcode{font:700 11px ui-monospace,Menlo,monospace;color:var(--acc);border:1px solid var(--acc);border-radius:4px;padding:0 3px;cursor:help}
.when{display:inline-block;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
a.cite{white-space:nowrap}a.cite .rp-pdf{margin-left:3px;font-size:9px;padding:0 3px}.ours{color:var(--mut);font-style:italic}
.rp-pdf{font:700 10.5px -apple-system,sans-serif;color:#fff;background:var(--acc);border-radius:4px;padding:1px 5px;letter-spacing:.03em}
.rp-tools{margin:2px 0 8px}.rp-only{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:14px;padding:3px 11px;cursor:pointer}
.rp-only[aria-pressed=true]{background:var(--acc);color:#fff}
.rp-list.only-pdf .rp-card:not(.has-pdf),.rp-list.only-pdf .rp-band:not(.has-pdf),.rp-list.only-pdf details.rp-more>summary{display:none}
@media(max-width:640px){body{padding:12px}td,th{padding:5px 6px}.form{grid-template-columns:1fr}.form .full{grid-column:1}}
@media(max-width:720px){main table{display:block;max-width:100%;overflow-x:auto}main table code{white-space:nowrap;word-break:normal}}
"""


def _page_url(snapshot: dict, rel: str, space: str = "design", item: str = "") -> str:
    board_path = "/" + (f'{snapshot["relative"]}/board.md' if snapshot["relative"] else "board.md")
    url = f'/_board/design?path={quote(board_path, safe="")}&file={quote(rel, safe="")}&space={space}'
    return url + (f"&item={quote(item)}" if item else "")


THEORY = SKILLS / "design" / "haipipe-workbench-design" / "ref" / "design-theory.md"
METHODS = SKILLS / "design" / "haipipe-workbench-design" / "ref" / "design-methods.md"
# The methods studio (JL 261002: "add a new studio … put it in the excalidraw to explain
# these methods"): one Excalidraw drawing of the loop, the families and the ten cards,
# opened in the self-hosted canvas and saved back to this file.
STUDIO = SKILLS / "design" / "haipipe-workbench-design" / "ref" / "design-methods.excalidraw"


def _pipe_rows(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    """A pipe table's header words (lower case) and its body rows."""
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    body = [r for r in cells[1:] if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return [c.lower() for c in cells[0]], body


def _plain_md(text: str, table=None) -> str:
    """The ASCII doc style (underlined titles, paragraphs, `- ` lists, fenced blocks, pipe
    tables) as HTML. `table(head, rows)` may render a table it knows; None falls back."""
    out, para, items, lines = [], [], [], text.splitlines()

    def inline(t: str) -> str:
        t = _e(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)

    def flush():
        if para:
            out.append(f'<p>{inline(" ".join(para))}</p>')
            para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
            items.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre class=theory>" + _e("\n".join(lines[i + 1:j])) + "</pre>")
            i = j + 1
            continue
        if line.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            head, rows = _pipe_rows(lines[i:j])
            html_table = table(head, rows) if table else None
            out.append(html_table or (
                "<table class=mdt><thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead><tbody>"
                + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table>"))
            i = j
            continue
        if line.strip() and re.fullmatch(r"[=-]{3,}", nxt.strip()):
            flush()
            out.append(f'<{"h1" if nxt.startswith("=") else "h2"}>{inline(line.strip())}</{"h1" if nxt.startswith("=") else "h2"}>')
            i += 2
            continue
        if line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        elif items and not para and line.startswith("  ") and line.strip():
            items[-1] += " " + line.strip()          # a list item that wraps goes on, indented
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "".join(out)


# The Theory of Design Space has three views (JL 261001), all of them general: how to
# design, the methods a design can be made by, and the papers behind both. Knowledge of
# one channel (message theories for SMS) is not design theory and is not shown here.
THEORY_VIEWS = (("design-theory", "Design theory"), ("methods", "Design methods"), ("studio", "Methods studio"),
                ("papers", "Papers"))


def studio_html(root: Path, drawing: Path = STUDIO) -> str:
    """Theory › Methods studio: the methods drawing in the Excalidraw canvas, editable, as
    the Paper workbench's RoadMap Draw shows a Story's drawing. It loads only when shown."""
    rel = _href(root, drawing) if Path(drawing).is_file() else ""
    if not rel:
        return '<div class=empty>No methods drawing yet: the design workbench keeps it as <code>ref/design-methods.excalidraw</code>.</div>'
    url = "/_excalidraw/?board=" + quote(rel.lstrip("/"), safe="/") + "&edit=1"
    return ('<div class=st-bar><span class=mut>One task, thirteen ways to design it: three inputs, Design and the Exp, '
            'the Revise and Learning loops, six families, the cards and the tests. Edits save to '
            '<code>ref/design-methods.excalidraw</code>.</span>'
            f'<a href="{_e(url)}" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            f'<iframe class=st-frame title="Methods studio" referrerpolicy="no-referrer" data-src="{_e(url)}"></iframe>')


def theory_page(board: Path, root: Path | None = None, view: str = "design-theory") -> str:
    """The Theory of Design Space: one view at a time, its name in a bar above it."""
    def article(path: Path, cls: str, empty: str) -> str:
        if path.is_file():
            return f'<article class="{cls}">{_plain_md(path.read_text(encoding="utf-8"))}</article>'
        return f'<div class=empty>{empty}</div>'
    views = {"design-theory": article(THEORY, "theory", "No design theory file is present."),
             "methods": (f'<article class="theory">{_plain_md(_read(METHODS), method_cards(board, root or board, METHODS, PAPERS, in_use="in the Exp", now="in Evaluate"))}</article>'
                         if METHODS.is_file() else '<div class=empty>No design methods file is present.</div>'),
             "studio": studio_html(root or board, STUDIO),
             "papers": papers_page(board, root or board, PAPERS)}
    view = view if view in views else "design-theory"
    bar = "".join(f'<button type=button data-view="{k}"{" class=on" if k == view else ""}>{_e(label)}</button>'
                  for k, label in THEORY_VIEWS)
    return (f'<div class=views>{bar}</div>'
            + "".join(f'<div class="view{" on" if k == view else ""}" data-view="{k}">{views[k]}</div>' for k, _ in THEORY_VIEWS))


# Theory › Papers (JL 261001): the papers behind the theory, one card each, as the Paper
# workbench shows a Story's Related Papers: closed, the title and then who, when and
# which journal; open, why it is here, its links and its full text. The rows are the
# workbench's own `ref/design-papers.md`, the same for every board (JL 261002: "put them
# in the Tools of the workbench of the design"); a row's `pdf` names its copy in
# `ref/papers/`, kept only when its license lets it be shared.
PAPERS = SKILLS / "design" / "haipipe-workbench-design" / "ref" / "design-papers.md"
PAPER_ROLES = ("classic", "review", "evidence")
# The UT Dallas list of 24 leading business journals (JL 261002: "is there a paper from
# the UTD24 list?"): a card in one of them carries the mark, and the head counts them.
UTD24 = ("the accounting review", "journal of accounting and economics", "journal of accounting research",
         "journal of finance", "journal of financial economics", "review of financial studies",
         "information systems research", "informs journal on computing", "mis quarterly",
         "journal of consumer research", "journal of marketing", "journal of marketing research", "marketing science",
         "management science", "operations research", "journal of operations management",
         "manufacturing & service operations management", "production and operations management",
         "academy of management journal", "academy of management review", "administrative science quarterly",
         "organization science", "journal of international business studies", "strategic management journal")


def is_utd24(venue: str) -> bool:
    name = re.sub(r"^the\s+", "", (venue or "").strip().lower())
    return name in {re.sub(r"^the\s+", "", v) for v in UTD24}


def paper_rows(table: Path = PAPERS) -> list[dict]:
    """The papers table: one dict per row, keyed by the header words."""
    rows, head = [], []
    for line in _read(Path(table)).splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not head:
            head = [c.lower() for c in cells]
        elif not all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
    return rows


def _href(root: Path, path: Path) -> str:
    """A plain server path for a file under the SPACE root, or reached through a folder
    linked in under it (`Tools` -> `../Tools-SPACE`); '' when it is neither."""
    root, path = Path(root), Path(path).resolve()
    try:
        return "/" + path.relative_to(root.resolve()).as_posix()
    except ValueError:
        pass
    for link in (c for c in root.iterdir() if c.is_symlink()):
        try:
            return "/" + (Path(link.name) / path.relative_to(link.resolve())).as_posix()
        except ValueError:
            continue
    return ""


def paper_runs(board: Path) -> dict[str, Path]:
    """DOI -> the Discovery Paper Run that holds it in the board's Project (its Bib, its
    abstract and, when a free copy exists, paper.pdf), so a card can read it."""
    out: dict[str, Path] = {}
    for rt in sorted(Path(board).parent.parent.glob("discoveries/b*/j*/t*/results/r*/runtime.yaml")):
        doi = re.search(r'(?m)^\s+doi:\s*"?([^"\s]+)"?\s*$', _read(rt))
        if doi:
            out.setdefault(doi.group(1).lower(), rt.parent)
    return out


def _run_abstract(run: Path) -> str:
    """The retrieved abstract, without its heading and source line."""
    return " ".join(ln.strip() for ln in _read(run / "abstract.md").splitlines()
                    if ln.strip() and not ln.lstrip().startswith(("#", "Source:", ">")))


def _paper_pdf(row: dict, table: Path, run: Path | None) -> Path | None:
    """The paper's full text: its copy beside the table, else its Paper Run's free copy."""
    kept = Path(table).parent / row["pdf"] if row.get("pdf") else None
    if kept is not None and kept.is_file():
        return kept
    return run / "paper.pdf" if run is not None and (run / "paper.pdf").is_file() else None


def _paper_card(root: Path, row: dict, table: Path, run: Path | None) -> str:
    who_year, _, title = row.get("paper", "").partition(" · ")
    year = (re.search(r"(\d{4})\s*$", who_year) or re.search(r"(\d{4})", who_year))
    names = (who_year[:year.start()] if year else who_year).strip(" :")
    # one author by name, two as `A & B`, three or more as `A et al.`, as a citation says them
    first = names if "," not in names else names.split(",")[0].strip() + " et al."
    who = " · ".join(x for x in (first, year.group(1) if year else "", row.get("venue", "")) if x)
    role = row.get("role", "").lower()
    doi = row.get("doi", "")
    pdf = _paper_pdf(row, table, run)
    card = run / f"{run.name}.md" if run is not None else None
    pdf_url = _href(root, pdf) if pdf is not None else ""
    acts = [f'<a href="{_e(pdf_url)}" target="_blank" rel="noopener">Open the PDF in a new tab ↗</a>' if pdf_url else "",
            f'<a href="https://doi.org/{_e(doi)}" target="_blank" rel="noopener">Publisher page ↗</a>' if doi else "",
            f'<a href="{_e(_href(root, card))}" target="_blank" rel="noopener">Paper Run ↗</a>'
            if card is not None and card.is_file() and _href(root, card) else ""]
    abstract = _run_abstract(run) if run is not None else ""
    if pdf_url:
        tail = f'<iframe class="rp-frame" title="{_e("PDF · " + (title or row.get("paper", "")))}" data-pdf="{_e(pdf_url)}"></iframe>'
    elif doi:
        tail = '<div class="rp-nopdf mut">No free full text here. Read it on the publisher page; it may need a subscription.</div>'
    else:
        tail = '<div class="rp-nopdf mut">A book or report with no DOI: read it in print or on its publisher\'s page.</div>'
    return (f'<details class="rp-card{" has-pdf" if pdf_url else ""}" id="{paper_id(row)}"><summary><span class="bjt-chev">▸</span><div class="lw-sum">'
            f'<div class="rp-title">{_e(title or row.get("paper", ""))}</div>'
            f'<div class="rp-sub"><span>{_e(who)}</span><span class="rp-marks">'
            + ('<span class=rp-pdf title="the PDF opens inside this card">PDF</span>' if pdf_url else "")
            + ('<span class=rp-utd title="on the UTD24 journal list">UTD24</span>' if is_utd24(row.get("venue", "")) else "")
            + f'<span class="rp-q rp-{_e(role)}">{_e(role)}</span></span></div>'
            '</div></summary><div class="rp-body">'
            + (f'<p class="rp-why">{_e(row.get("why here", ""))}</p>' if row.get("why here") else "")
            + '<div class="rp-acts">' + "".join(f"<span>{a}</span>" for a in acts if a) + '</div>'
            + (f'<details class="rp-absd"><summary>Abstract</summary><p>{_e(abstract)}</p></details>' if abstract else "")
            + f'{tail}</div></details>')


def papers_page(board: Path, root: Path, table: Path = PAPERS) -> str:
    """Theory › Papers: one band per design method, in the file's order, each a count and
    one box of cards; the journals they come from are named above the bands."""
    rows = paper_rows(table)
    if not rows:
        return ('<div class=empty>No related paper yet: the design workbench keeps them in '
                '<code>ref/design-papers.md</code> (group · role · key · paper · venue · doi · why here · pdf).</div>')
    groups: dict[str, list[dict]] = {}
    for row in rows:
        # a paper may serve two methods (`by a; by b`): it shows once, in its first group
        groups.setdefault(row.get("group", "").split(";")[0].strip() or "other", []).append(row)
    roles = " · ".join(f"{sum(r.get('role', '').lower() == k for r in rows)} {k}" for k in PAPER_ROLES)
    index = paper_runs(board)
    run_of = {id(r): index.get(r.get("doi", "").lower()) for r in rows}
    pdfs = sum(_paper_pdf(r, table, run_of[id(r)]) is not None for r in rows)
    venues: dict[str, int] = {}
    for row in rows:
        venues[row.get("venue", "") or "—"] = venues.get(row.get("venue", "") or "—", 0) + 1
    utd = sum(is_utd24(r.get("venue", "")) for r in rows)
    keys = sum(bool(r.get("key")) for r in rows)
    head = (f'<div class="rp-head">{len(rows)} papers · {keys} key · {roles} · {utd} in UTD24 journals · {pdfs} with a PDF</div>'
            + (f'<div class=rp-tools><button type=button class=rp-only aria-pressed=false>Show only the {pdfs} papers with a PDF</button></div>'
               if pdfs else "")
            + f'<details class=rp-venues><summary>{len(venues)} journals and publishers</summary><div class=mut>'
            + " · ".join(f"{_e(v)} ({n})" for v, n in sorted(venues.items(), key=lambda kv: (-kv[1], kv[0])))
            + '</div></details>')
    card = lambda r: _paper_card(root, r, table, run_of[id(r)])
    # each band shows its key papers (★ in `key`) and folds the rest (JL 261002: "collapse the
    # less important papers"); a band with no key paper shows all of its papers
    def band(group: str, rs: list[dict]) -> str:
        top = [r for r in rs if r.get("key")] or rs
        rest = [r for r in rs if r not in top]
        cards = [card(r) for r in top], [card(r) for r in rest]
        has = any("rp-card has-pdf" in c for c in cards[0] + cards[1])
        more = (f'<details class=rp-more><summary>{len(rest)} more paper{"s" if len(rest) != 1 else ""}</summary>'
                f'<div class="rp-group">{"".join(cards[1])}</div></details>' if rest else "")
        return (f'<section class="rp-band{" has-pdf" if has else ""}">'
                f'<div class="lw-k">{_e(group[:1].upper() + group[1:])}<span class="lw-kn">{len(rs)}</span></div>'
                f'<div class="rp-group">{"".join(cards[0])}</div>{more}</section>')
    bands = "".join(band(g, rs) for g, rs in groups.items())
    return f'<div class="rp-list">{head}{bands}</div>'


def paper_id(row: dict) -> str:
    """A paper card's anchor: its DOI, else its citation, as `paper-<slug>`."""
    return "paper-" + re.sub(r"[^a-z0-9]+", "-", (row.get("doi") or row.get("paper", "")).lower()).strip("-")[:80]


def short_cite(row: dict) -> str:
    """`Dow, Glassco, Kass et al. 2010 · …` -> `Dow et al. 2010`; `A & B 2001` stays."""
    who_year = row.get("paper", "").partition(" · ")[0]
    year = re.search(r"(\d{4})\s*$", who_year) or re.search(r"(\d{4})", who_year)
    names = (who_year[:year.start()] if year else who_year).strip(" :")
    names = names.split(",")[0].strip() + " et al." if "," in names else names
    return f"{names} {year.group(1)}" if year else names


def method_card_fields(path: Path) -> dict:
    """One method card file: its name, then the `key: value` fields of its head and of its
    two parts, What the literature says (`lit`) and Applied to AI (`ai`). A value may wrap
    onto indented lines."""
    lines = _read(path).splitlines()
    out = {"name": lines[0].strip() if lines else Path(path).stem, "head": {}, "lit": {}, "ai": {}}
    part, key = "head", None
    for i, line in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.strip() and re.fullmatch(r"-{3,}", nxt.strip()):
            part, key = ("ai" if line.strip().lower().startswith("applied") else "lit"), None
            continue
        m = re.match(r"^([A-Za-z][A-Za-z ]*):\s+(.*)$", line)
        if m and m.group(1).lower() in CARD_KEYS:
            key = m.group(1).lower()
            out[part][key] = m.group(2).strip()
        elif key and line.startswith("  ") and line.strip():
            out[part][key] += " " + line.strip()
        elif not line.strip():
            key = None
    return out


CARD_KEYS = {"family", "reasoning", "move", "status", "taxonomy", "comes from", "reads", "returns", "test now", "test in use", "rationale", "context",
             "steps", "strengths", "limitations", "agent", "verify", "risk", "evidence on ai", "skill"}
LIT_FIELDS = (("rationale", "Rationale"), ("context", "Context"), ("steps", "Steps"),
              ("strengths", "Strengths"), ("limitations", "Limitations"))
AI_FIELDS = (("agent", "The agent"), ("steps", "Steps"), ("returns", "Returns"), ("verify", "Verify"),
             ("risk", "AI risk"), ("evidence on ai", "Evidence on AI"), ("skill", "Skill"))


def method_cards(board: Path, root: Path, doc_path: Path, table: Path = PAPERS, in_use: str = "in use", now: str = "now"):
    """The Design methods view's renderer for its card index (JL 261002: "make each of them
    a card (design method card)", "add a new thing about how this can be applied to AI").
    The index table names one card file per method. Closed, a card is the method's name,
    whether any study tests it, its move, what it reads and returns, and where it comes
    from. Open, What the literature says (as O'Cathain et al. 2019 describe approaches)
    stands beside Applied to AI, and the method's papers close it. Every paper links to
    its card in the Papers view, PDF and all. What a card reads is coloured by input
    (JL 261002): design requirements, internal insights, external insights; `now` and
    `in_use` name where the two kinds of test happen ("in Evaluate", the Revise loop, and
    "in the Exp", the Learning loop, for design methods)."""
    doc_path = Path(doc_path)
    doc = _read(doc_path)
    papers = paper_rows(table)
    index = paper_runs(board)
    by_group: dict[str, list[dict]] = {}
    for r in papers:
        for g in r.get("group", "").lower().split(";"):       # and counts on every card it serves
            by_group.setdefault(g.strip(), []).append(r)
    tests = {}
    for line in doc.splitlines():                       # T0 … T4 and what each asks, for the badges
        m = re.match(r"^\|\s*(T\d)\s+([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            tests[m.group(1)] = f"{m.group(1)} {m.group(2)}: {m.group(3)}"

    def chip(r: dict) -> str:
        has = _paper_pdf(r, table, index.get(r.get("doi", "").lower())) is not None
        return (f'<a class="pchip to-paper" href="#{paper_id(r)}" title="{_e(r.get("paper", ""))}">{_e(short_cite(r))}'
                + ('<span class=rp-pdf>PDF</span>' if has else "") + '</a>')

    def find(cite: str) -> dict | None:
        """The papers-table row a citation names: the same first author and year, if only one."""
        first_word = lambda t: t.replace(",", " ").split()[0].lower() if t.strip() else ""
        year = re.search(r"\b\d{4}\b", cite)
        hits = [p for p in papers if first_word(p.get("paper", "")) == first_word(cite)
                and (year is None or re.search(rf"\b{year.group(0)}\b", p.get("paper", "").partition(" · ")[0]))]
        if len(hits) > 1:                   # `O'Cathain 2019 taxonomy`: a title word picks one of two
            rest = [w for w in re.findall(r"[a-z]{4,}", cite.lower()) if w not in first_word(cite)]
            hits = [p for p in hits if all(w in p.get("paper", "").partition(" · ")[2].lower() for w in rest)] if rest else hits
        return hits[0] if len(hits) == 1 else None

    def cited(entry: str) -> str:
        """`Newell & Simon 1972, generate and test` -> the paper's link, then the idea it gives;
        an unmatched source stays text."""
        cite, _, idea = entry.strip().partition(", ")
        hit = find(cite)
        head = chip(hit) if hit else f'<span class=chip>{_e(cite)}</span>'
        return f'<span class=src>{head}{(" " + _e(idea)) if idea else ""}</span>'

    def prose(text: str) -> str:
        """A cell's text with each `[Author Year]` linked to its paper card, `(ours)` muted
        and test codes badged."""
        def link(m):
            parts = []
            for c in m.group(1).split(";"):
                hit = find(c.strip())
                has = hit is not None and _paper_pdf(hit, table, index.get(hit.get("doi", "").lower())) is not None
                parts.append(f'<a class="cite to-paper" href="#{paper_id(hit)}" title="{_e(hit.get("paper", ""))}">{_e(c.strip())}'
                             + ('<span class=rp-pdf>PDF</span>' if has else "") + '</a>' if hit else _e(c.strip()))
            return "[" + "; ".join(parts) + "]"
        links: list[str] = []

        def stash(m):                       # set each linked citation aside while the text is escaped
            links.append(link(m))
            return f"\x00{len(links) - 1}\x00"
        out = _e(re.sub(r"\[([^\]]+)\]", stash, text))
        out = re.sub(r"\bT\d\b", lambda m: f'<span class=tcode title="{_e(tests.get(m.group(0), ""))}">{m.group(0)}</span>', out)
        out = out.replace("(ours)", '<span class=ours title="this workbench\'s own judgment">(ours)</span>')
        return re.sub(r"\x00(\d+)\x00", lambda m: links[int(m.group(1))], out)

    def lines(text: str, steps: bool = False) -> str:
        """Steps one per line (`1. … 2. …`); otherwise one sentence per line."""
        numbered = steps and re.search(r"\b1\.\s", text)
        parts = re.split(r"\s(?=\d\.\s)", text) if numbered else re.split(r"(?<=\.)\s+(?=[A-Z])", text)
        return "".join(f"<div class=line>{prose(p)}</div>" for p in parts if p.strip())

    def ranked(rs: list[dict]) -> list[dict]:
        return sorted(rs, key=lambda r: (not r.get("key"), r.get("role", "").lower() != "evidence"))

    def tested(cell: str) -> str:
        return re.sub(r"\bT\d\b", lambda m: f'<span class=tcode title="{_e(tests.get(m.group(0), ""))}">{m.group(0)}</span>',
                      _e(cell))

    def card(n: int, f: dict) -> str:
        name, h, lit, ai = f["name"], f["head"], f["lit"], f["ai"]
        group = by_group.get(name.lower(), [])
        studies = sum(p.get("role", "").lower() == "evidence" for p in group)
        future = h.get("status", "").lower().startswith("future")
        status = (f'<span class="mc-status future" title="{_e(h["status"])}">future · not run yet</span>' if future else
                  f'<span class="mc-status ok">tested in {studies} stud{"y" if studies == 1 else "ies"}</span>' if studies
                  else '<span class="mc-status gap">no study tests it yet</span>')
        def kind(x: str) -> str:            # an input's chip is coloured by its kind; any other stays plain
            w = x.lower()
            return next((f'class="chip {c}"' for c, k in (("in-req", "design requirements"), ("in-int", "internal insights"),
                                                          ("in-ext", "external insights")) if w.startswith(k)), "class=chip")
        reads = "".join(f"<span {kind(x.strip())}>{_e(x.strip())}</span>" for x in h.get("reads", "").split("·") if x.strip())
        frm = '<span class=mut> · </span>'.join(cited(e) for e in h.get("comes from", "").split(";") if e.strip())
        skill, _, note = ai.get("skill", "").partition(" ")

        def dl(fields: tuple, part: dict) -> str:
            rows = []
            for key, label in fields:
                if key == "skill" and skill:
                    body = f'<code>{_e(skill)}</code>' + (f' <span class=mut>{_e(note)}</span>' if note else "")
                elif part.get(key):
                    body = lines(part[key], steps=key == "steps")
                else:
                    continue
                rows.append(f"<dt>{_e(label)}</dt><dd>{body}</dd>")
            return "<dl>" + "".join(rows) + "</dl>"
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        return (f'<details class="mcard{" future" if future else ""}" id="method-{slug}"><summary><span class="bjt-chev">▸</span><div class=mc-sum>'
                f'<div class=mc-top><span class=mnum>{n}</span><span class=mc-name>{_e(name)}</span>{status}</div>'
                f'<div class=mc-move>{_e(h.get("move", ""))}</div>'
                + (f'<div class=mc-from><span class=lbl>reasoning</span>{_e(h["reasoning"])}</div>' if h.get("reasoning") else "")
                +                 f'<div class=mc-io><span class=lbl>reads</span>{reads}<span class=arrow>→</span>'
                f'<span class=lbl>returns</span>{_e(h.get("returns", ""))}</div>'
                + (f'<div class=mc-from><span class=lbl>comes from</span>{frm}</div>' if frm else "")
                + (f'<div class=mc-from><span class=lbl>taxonomy</span>{prose(h["taxonomy"])}</div>' if h.get("taxonomy") else "")
                + '</div></summary><div class=mc-body><div class=mc-cols>'
                f'<div class=mc-col><div class=mc-h>What the literature says</div>{dl(LIT_FIELDS, lit)}</div>'
                f'<div class="mc-col ai"><div class=mc-h>Applied to AI</div>{dl(AI_FIELDS, ai)}</div></div>'
                f'<div class=mc-tests><span class=lbl>tested</span><span class=when>{_e(now)}</span> {tested(h.get("test now", ""))}'
                f'<span class=when>{_e(in_use)}</span> {tested(h.get("test in use", ""))}</div>'
                + (f'<div class=mc-papers><span class=lbl>papers</span>{"".join(chip(p) for p in ranked(group))}</div>' if group else "")
                + '</div></details>')

    def render(head: list[str], rows: list[list[str]]):
        if head != ["family", "method", "card"]:
            return None
        out, family = [], None
        for n, r in enumerate(rows, start=1):
            path = doc_path.parent / r[2] if len(r) > 2 else None
            if path is None or not path.is_file():
                out.append(f'<div class="mcard missing">{n} · {_e(r[1] if len(r) > 1 else "")}: no card at <code>{_e(r[2] if len(r) > 2 else "")}</code></div>')
                continue
            f = method_card_fields(path)
            label, _, gloss = f["head"].get("family", r[0]).partition(":")
            if label.strip() != family:
                family = label.strip()
                out.append(f'<div class=mc-fam><b>{_e(family)}</b>'
                           + (f' <span class=mut>· {_e(gloss.strip())}</span>' if gloss.strip() else "") + '</div>')
            out.append(card(n, f))
        return f'<div class=mcards>{"".join(out)}</div>'
    return render


def render_design_board(snapshot: dict, space: str = "tasks", view: str = "design-theory") -> str:
    aliases = {"goal": "tasks", "brief": "tasks", "frame": "tasks", "plan": "tasks", "design": "tasks",
               "items": "tasks", "run": "tasks", "runs": "tasks", "delivery": "tasks", "ready": "tasks",
               "theories": "theory", "knowledge": "theory", "methods": "theory", "studio": "theory", "papers": "theory"}
    selected = aliases.get(space, space) if space else "tasks"
    if selected not in ("tasks", "theory"):
        selected = "tasks"
    # the header names the board and nothing else (JL 261001: counts draw the eye away)
    header = (
        f'<h1>🎨 {_e(snapshot["title"])}</h1><div class=mut>Board level</div>'
        + (f'<div class="mut bad">records check: {len(snapshot["audit"])} finding(s) across folders</div>' if snapshot["audit"] else "")
    )

    # Goal Space: the list of design tasks, from the Brief -------------------
    task_rows = []
    for row in snapshot["brief_rows"]:
        if row["snapshot"] is not None:
            folder_cell = f'<a href="{_e(_page_url(snapshot, row["snapshot"]["rel"], "goal"))}"><code>{_e(row["folder"])}</code></a>'
            action = ""
        elif row["folder"]:
            folder_cell = f'<code class=bad>{_e(row["folder"])}</code>'
            action = ""
        else:
            folder_cell = '<span class=mut>—</span>'
            action = (f'<button class=do data-action=new-folder data-row="{_e(row["id"])}">New Design Folder</button>'
                      '<span class=msg></span>') if not snapshot["static"] else ""
        progress = str(row["designs"] or row["registered"] or "—")
        # the task by its full name (job · venue · who), never the Brief's row id (JL 260918)
        name = _e(design_title(row))
        if row["snapshot"] is not None:
            name = f'<a href="{_e(_page_url(snapshot, row["snapshot"]["rel"], "design"))}">{name}</a>'
        task_rows.append(
            f'<tr data-row="{_e(row["id"])}"><td><b>{name}</b></td><td>{_e(progress)}</td>'
            f'<td>{folder_cell}</td>'
            f'<td class="{"bad" if not row["snapshot"] else ""}">{_e(row["status"])} {action}</td></tr>')
    if task_rows:
        goal_html = ('<h2>Design tasks</h2><table><tr><th>design task</th>'
                     f'<th>designs</th><th>folder</th><th>state</th></tr>{"".join(task_rows)}</table>')
    elif snapshot["brief"]:
        goal_html = (f'<h2>Design tasks</h2><div class=empty>The design task file '
                     f'<code>{_e(snapshot["brief"].name)}</code> has no list yet; add the first design tasks from the Runs panel.</div>')
    else:
        goal_html = '<h2>Design tasks</h2><div class=empty>No design task file under 0-BR-brief/; add one before listing design tasks.</div>'
    if snapshot["unlisted"]:
        goal_html += ('<div class=mut>folders no design task lists: '
                      + ", ".join(f'<a href="{_e(_page_url(snapshot, f["rel"], "goal"))}"><code>{_e(f["name"])}</code></a>'
                                  for f in snapshot["unlisted"]) + '</div>')
    rules = shared_rules(snapshot["items"])
    if rules:
        goal_html += ('<div class=task><span class=mut>every design task keeps</span> '
                      + " · ".join(_e(r) for r in rules) + '</div>')
    count = len(bundle_rows(snapshot))
    if count and not snapshot["static"]:
        goal_html += (f'<div class=mut><a href="/_board/design-bundle?path={quote(board_path_of(snapshot), safe="")}">'
                      f'↓ Download all designs · {count} · csv</a></div>')

    # Theory of Design Space: how to design, then this board's domain knowledge ----
    theory_html = theory_page(Path(snapshot["board"]), Path(snapshot["root"]), view)

    # The board level has two Spaces (JL 261001): the design tasks, and the theory
    # every design draws on. Every design, run and delivery lives at the page level.
    root = Path(snapshot["root"])
    board_rel = board_path_of(snapshot).lstrip("/")
    runs = [r for f in snapshot["folders"] for r in (dict(x, folder=f["name"]) for x in f["runs"])]
    panes = {"tasks": goal_html, "theory": theory_html}
    for key in panes:
        panel = design_runs_panel(key, runs, root=root, page=board_rel, board=board_rel,
                                  whole="this board")
        panes[key] = f'<div class=space-main>{panes[key]}</div>{panel}'
    panel_css, panel_js = runs_panel_assets()
    tabs = "".join(f'<button type=button data-space="{k}"{" class=on" if k == selected else ""}>{v}</button>'
                   for k, v in (("tasks", "Design Tasks Space"), ("theory", "Theory of Design Space")))
    pane_html = "".join(f'<section class="pane split{" on" if k == selected else ""}" data-space="{k}">{v}</section>'
                        for k, v in panes.items())
    board_path = "/" + (f'{snapshot["relative"]}/board.md' if snapshot["relative"] else "board.md")
    script = (
        "<script>(function(){var BOARD=" + _json(board_path) + ";"
        "var bs=[].slice.call(document.querySelectorAll('.tabs button')),ps=[].slice.call(document.querySelectorAll('.pane'));"
        "function sel(s,w){bs.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});"
        "ps.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});"
        "if(w){var u=new URL(location.href);u.searchParams.set('space',s);history.replaceState({},'',u)}}"
        "bs.forEach(function(b){b.onclick=function(){sel(b.dataset.space,true)}});"
        # a Space's views (Theory: Design theory · Design methods · Papers): one shown at a time, kept in the URL
        "function loadFrames(pane){pane.querySelectorAll('.view.on iframe.st-frame[data-src]').forEach(function(f){"
        "if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})}"
        "document.querySelectorAll('.pane').forEach(loadFrames);"
        "document.querySelectorAll('.views button').forEach(function(b){b.onclick=function(){"
        "var pane=b.closest('.pane');pane.querySelectorAll('.views button').forEach(function(x){x.classList.toggle('on',x===b)});"
        "pane.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',v.dataset.view===b.dataset.view)});"
        "loadFrames(pane);"
        "var u=new URL(location.href);u.searchParams.set('view',b.dataset.view);history.replaceState({},'',u)}});"
        # a paper's PDF loads only when its card opens; toggle does not bubble, so listen in capture
        "document.addEventListener('toggle',function(ev){var w=ev.target;if(!(w.matches&&w.matches('details.rp-card')))return;"
        "var f=w.open&&w.querySelector('iframe[data-pdf]');if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf)},true);"
        # a paper named in the Design methods table opens its card in the Papers view
        "function toPaper(id){var c=document.getElementById(id);if(!c)return;var b=document.querySelector('.views button[data-view=papers]');"
        "if(b&&!b.classList.contains('on'))b.click();var f=c.closest('details.rp-more');if(f)f.open=true;c.open=true;"
        "c.scrollIntoView({block:'start'});history.replaceState({},'',location.pathname+location.search+'#'+id)}"
        "document.querySelectorAll('a.to-paper').forEach(function(a){a.onclick=function(e){e.preventDefault();"
        "toPaper(a.getAttribute('href').slice(1))}});"
        "if(location.hash.indexOf('#paper-')===0)toPaper(location.hash.slice(1));"
        # "Show only the papers with a PDF": hide the rest, and open the folds so every PDF card shows
        "document.querySelectorAll('.rp-only').forEach(function(b){b.onclick=function(){var l=b.closest('.rp-list'),"
        "on=!l.classList.contains('only-pdf');l.classList.toggle('only-pdf',on);b.setAttribute('aria-pressed',on);"
        "if(on)l.querySelectorAll('details.rp-more').forEach(function(d){d.open=true})}});"
        "document.querySelectorAll('button.do').forEach(function(b){b.onclick=function(){"
        "var box=b.closest('[data-act]'),msg=b.parentNode.querySelector('.msg'),body={path:BOARD,action:b.dataset.action,row:b.dataset.row||''};"
        "if(box){box.querySelectorAll('input,textarea,select').forEach(function(f){if(f.name)body[f.name]=f.value})}"
        "msg.className='msg';msg.textContent='writing…';b.disabled=true;"
        "fetch('/_board/design-board-act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})"
        ".then(function(r){return r.json()}).then(function(j){if(!j.ok){msg.className='msg bad';msg.textContent=j.err||'refused';b.disabled=false;return}"
        "location.href=j.url}).catch(function(e){msg.className='msg bad';msg.textContent=String(e);b.disabled=false})}});})();</script>"
    )
    return (
        '<!doctype html><html lang=en><head><meta charset=utf-8>'
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        f'<title>🎨 Design Board · {_e(snapshot["title"])}</title><style>{_CSS}{panel_css}</style></head><body>'
        f'<header>{header}</header><nav class=tabs>{tabs}</nav><main>{pane_html}</main>{script}{panel_js}</body></html>'
    )


def board_path_of(snapshot: dict) -> str:
    return "/" + (f'{snapshot["relative"]}/board.md' if snapshot["relative"] else "board.md")


def bundle_rows(snapshot: dict) -> list[dict]:
    """One row per design on the board, with its state and the Brief line it serves.

    The design is the candidate whose independent Verify passed; a failed or
    unverified draft is never listed for handoff."""
    by_folder = {r["folder"]: r for r in snapshot["brief_rows"] if r["folder"]}
    rows = []
    for i in snapshot["items"]:
        design = i.get("ready")
        if not design:
            continue
        line = by_folder.get(i["folder"], {})
        rows.append({
            "line": line.get("id", ""), "who": line.get("audience") or i.get("audience", ""),
            "their_job": line.get("job") or i.get("job", ""), "venue": line.get("venue") or i.get("type", ""),
            "folder": i["folder"], "item": i["id"], "title": i["title"], "state": i["state"], "text": with_link(design["text"]),
            "draft_run": design["run"], "because": because_words(i),
            "render": i["render"]["render"] if i.get("render") else "",
        })
    return rows


def bundle_csv(snapshot: dict, folder: str = "") -> str:
    """Every passed design on the board as CSV; `folder` keeps one design task's rows."""
    import csv
    import io
    out = io.StringIO()
    fields = ["line", "who", "their_job", "venue", "folder", "item", "title", "state", "text", "draft_run", "render", "because"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in bundle_rows(snapshot):
        if not folder or row["folder"] == folder:
            writer.writerow(row)
    return out.getvalue()


def _json(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


# ----------------------------------------------------------------- writes --

_FILLER = {"a", "an", "the", "with", "within", "of", "for", "to", "in", "on", "or", "and", "at", "by", "under", "over"}


def _slug(text: str, words: int = 3) -> str:
    """The first content words of a Brief cell, so a folder name says the goal (JL 260917)."""
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


def new_folder(board_root: Path, row_id: str) -> dict:
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
    title = design_title(row)
    wanted = row["designs"]
    count = "" if wanted == 1 else f"{wanted} " if wanted else ""
    ask = (f"Which {count}{row['job'].strip()} {venue_word(row['venue'])} design{'' if wanted == 1 else 's'} "
           f"should we make for {row['audience'].strip()}?")
    folder = group / name
    folder.mkdir()
    (folder / f"{name}.md").write_text(
        f"# {title}\nfolder-kind: design\nstate: 🔴 OPEN · no design registered yet\nowner: {_owner(board_root)}\n\n"
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
    cells = [c.strip() for c in _ROW.match(lines[target]).group(1).split("|")]
    while len(cells) <= folder_col:
        cells.append("")
    cells[folder_col] = f"`{name}`"
    lines[target] = "| " + " | ".join(cells) + " |"
    brief.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    _list_page(board_root, f"{DESIGN_GROUP}/{name}/{name}.md")
    return {"folder": name, "rel": f"{DESIGN_GROUP}/{name}/{name}.md", "brief_updated": True}


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


class DesignBoardMixin:
    """GET/HEAD/POST surface for a whole DesignBoard."""

    def _design_board_target(self, raw: str) -> Path | None:
        return resolve_board(Path(self.root), raw)

    def design_board_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        raw = (query.get("board") or query.get("path") or [""])[0]
        board = self._design_board_target(raw)
        if board is None or not is_design_board(board):
            items = "".join(
                f'<li><a href="/_board/design-board?board={quote(b.name)}">{_e(b.name)}</a></li>'
                for b in design_boards(Path(self.root))) or "<li>No DesignBoard under this root.</li>"
            body = ("<!doctype html><meta charset=utf-8><title>🎨 Design Board</title>"
                    '<body style="font:14px/1.5 system-ui;margin:24px"><h1>🎨 Design Board</h1>'
                    f"<p>This link does not name a DesignBoard (got <code>{_e(raw) or 'nothing'}</code>). Pick one:</p>"
                    f"<ul>{items}</ul></body>").encode("utf-8")
            # a bare link is a question with a good answer (the list); a wrong name is a 404
            return self._design_board_send(body, 404 if raw else 200, head_only)
        snapshot = design_board_snapshot(board, self.root)
        body = render_design_board(snapshot, (query.get("space") or ["goal"])[0],
                                   (query.get("view") or ["design-theory"])[0]).encode("utf-8")
        return self._design_board_send(body, 200, head_only)

    def design_bundle_view(self, head_only=False):
        """GET /_board/design-bundle?path=… -> every design on the board as CSV."""
        query = parse_qs(urlparse(self.path).query)
        board = self._design_board_target((query.get("board") or query.get("path") or [""])[0])
        if board is None or not is_design_board(board):
            return self._design_board_send(b"no DesignBoard at that path", 404, head_only)
        snapshot = design_board_snapshot(board, self.root)
        body = bundle_csv(snapshot, (query.get("folder") or [""])[0]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv; charset=utf-8")
        self.send_header("Content-Disposition", f'attachment; filename="{board.name}-design-bundle.csv"')
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def _design_board_send(self, body: bytes, code: int, head_only: bool):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_design_board(self, payload):
        board = self._design_board_target(payload.get("path") or "")
        if board is None:
            return None, "path must identify a Board with board.md"
        if not is_design_board(board):
            return None, "selected Board is not a DesignBoard"
        return {"url": "/_board/design-board?path=%s" % quote(payload.get("path") or "")}, None

    def design_board_act(self, payload):
        board = self._design_board_target(payload.get("path") or "")
        if board is None or not is_design_board(board):
            return None, "path must identify a DesignBoard"
        action = payload.get("action")
        path_q = quote(payload.get("path") or "")
        try:
            if action == "new-folder":
                out = new_folder(board, str(payload.get("row") or ""))
                out["url"] = "/_board/design?path=%s&file=%s&space=goal" % (path_q, quote(out["rel"], safe=""))
            elif action == "add-tasks":
                try:
                    designs = int(str(payload.get("designs") or "0").strip() or "0")
                except ValueError:
                    raise ValueError("how many designs must be a whole number") from None
                out = add_tasks(board, str(payload.get("subgroups") or "").splitlines(),
                                str(payload.get("job") or ""), str(payload.get("venue") or ""), designs,
                                str(payload.get("insight") or "").strip(),
                                str(payload.get("open") or "yes").lower() not in ("no", "false", "0", ""))
                out["url"] = "/_board/design-board?path=%s&space=goal" % path_q
            else:
                return None, f"unknown action {action!r}"
        except (ValueError, OSError) as exc:
            return None, str(exc)
        return out, None
