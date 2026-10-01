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
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a}}
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
article.theory.domain{border-top:1px solid var(--line);margin-top:28px;padding-top:8px}
@media(max-width:640px){body{padding:12px}td,th{padding:5px 6px}.form{grid-template-columns:1fr}.form .full{grid-column:1}}
@media(max-width:720px){main table{display:block;max-width:100%;overflow-x:auto}main table code{white-space:nowrap;word-break:normal}}
"""


def _page_url(snapshot: dict, rel: str, space: str = "design", item: str = "") -> str:
    board_path = "/" + (f'{snapshot["relative"]}/board.md' if snapshot["relative"] else "board.md")
    url = f'/_board/design?path={quote(board_path, safe="")}&file={quote(rel, safe="")}&space={space}'
    return url + (f"&item={quote(item)}" if item else "")


THEORY = SKILLS / "design" / "haipipe-workbench-design" / "ref" / "design-theory.md"


def _plain_md(text: str) -> str:
    """The ASCII doc style (underlined titles, paragraphs, `- ` lists, fenced blocks) as HTML."""
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
        if line.strip() and re.fullmatch(r"[=-]{3,}", nxt.strip()):
            flush()
            out.append(f'<{"h1" if nxt.startswith("=") else "h2"}>{inline(line.strip())}</{"h1" if nxt.startswith("=") else "h2"}>')
            i += 2
            continue
        if line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        elif not line.strip():
            flush()
        else:
            para.append(line.strip())
        i += 1
    flush()
    return "".join(out)


def theory_page(board: Path) -> str:
    """The Theory of Design Space: the general theory, then the board's own domain knowledge."""
    parts = []
    for path, cls in ((THEORY, "theory"), (board / "design-theory.md", "theory domain")):
        if path.is_file():
            parts.append(f'<article class="{cls}">{_plain_md(path.read_text(encoding="utf-8"))}</article>')
    return "".join(parts) or '<div class=empty>No design theory file is present.</div>'


def render_design_board(snapshot: dict, space: str = "tasks") -> str:
    aliases = {"goal": "tasks", "brief": "tasks", "frame": "tasks", "plan": "tasks", "design": "tasks",
               "items": "tasks", "run": "tasks", "runs": "tasks", "delivery": "tasks", "ready": "tasks",
               "theories": "theory", "knowledge": "theory"}
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
    theory_html = theory_page(Path(snapshot["board"]))

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
        body = render_design_board(snapshot, (query.get("space") or ["goal"])[0]).encode("utf-8")
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
