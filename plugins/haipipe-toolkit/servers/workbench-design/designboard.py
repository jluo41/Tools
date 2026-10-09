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
from urllib.parse import parse_qs, quote, unquote, urlencode, urlparse

from host_paths import skill_dir
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
# One method per group (JL 261005: "each job will be a method of design settings"): beside or instead
# of the plain 2-Design/, a board may hold 2-Design-M<NN>-<slug>/ folders, each with its method.md
# card (See input · Conduct process · Check output) and one Design Folder per Brief task, numbered
# as the Brief numbers it, so Design-01 is the same task under every method.
_METHOD_GROUP = re.compile(r"^2-Design-(M\d+)-(.+)$")
METHOD_CARD = "method.md"
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


def _method_views(snapshot: dict, rows: list[dict]) -> list[tuple[str, str, str]]:
    """Design Tasks on a board with method folders: one View per method, its method.md card above
    the table of that method's tasks (the table the family Views use). No All View; the first
    method opens."""
    empty = '<div class=empty>No design task is listed yet.</div>'
    groups = snapshot["methods"]
    views = []                     # no All View (JL 261005: "we can remove All"): the methods alone
    for n, g in enumerate(groups, start=1):
        views.append((f"m-{n}", g["label"], _method_steps(snapshot, rows, g, empty)))
    return views


def _card_parts(card: Path | None) -> tuple[str, list[str]]:
    """A method.md's lead paragraph and its three step sections, in file order, as HTML."""
    if card is None:
        return "", []
    body = re.sub(r"(?s)^\s*#\s[^\n]*\n", "", _read(card), count=1)
    parts = re.split(r"(?m)^##\s+.+?\s*$", body)
    return parts[0].strip(), [_plain_md(x.strip()) for x in parts[1:]]


def _rationale(folder: Path, run: str) -> dict:
    """A Generate result's rationale.yaml as flat key: value pairs (reason, sources, forecast)."""
    out: dict[str, str] = {}
    key = ""
    for line in _read(Path(folder) / "results" / run / "rationale.yaml").splitlines():
        hit = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if hit:
            key = hit.group(1)
            out[key] = hit.group(2).strip()
        elif key and line.startswith("  "):
            out[key] += " " + line.strip()
    return {k: v.strip().strip("'\"").replace("''", "'") for k, v in out.items()}


def _method_steps(snapshot: dict, rows: list[dict], g: dict, empty: str) -> str:
    """One method's View (JL 261005: a subsubspace under each method): the design unit's three
    steps as its own Views, ① See input · ② Designs · ③ Check output, each step's part of the
    method card on top. ② opens: the messages themselves, task by task (JL 261005: "changed to
    the message content")."""
    board = Path(snapshot["board"])
    lead, parts = _card_parts(g["card"])
    parts += [""] * (3 - len(parts))
    step_card = lambda i: (f'<div class=step-card>{parts[i]}</div>' if parts[i] else "")
    if not g["key"]:
        lead = "Folders in the plain <code>2-Design/</code>: made before methods were stated."
    elif g["card"] is None:
        lead = 'No <code>method.md</code> in this method folder: the method is not stated.'
    else:
        lead = _plain_md(lead) if lead else ""

    # ① See input: the packet the writer saw, by the path the card names, and the shared goal
    packets = list(dict.fromkeys(re.findall(r"1-IN-inputs/[^`\s,;)]+\.md", _read(g["card"]) if g["card"] else "")))
    see = step_card(0)
    for rel in packets:
        f = board / rel
        see += (f'<details class=packet open><summary>The packet · <code>{_e(rel)}</code></summary>'
                + (f'<div class=packet-body>{_plain_md(_read(f))}</div>' if f.is_file()
                   else '<div class=bad>not on disk</div>') + '</details>')
    if (board / "design-goal.md").is_file():
        see += ('<details class=packet><summary>The goal every method shares · <code>design-goal.md</code></summary>'
                f'<div class=packet-body>{_plain_md(_read(board / "design-goal.md"))}</div></details>')
    if not packets and not parts[0]:
        see += '<div class=empty>The method card names no input.</div>'

    # ② Designs and ③ Check output: task by task, this method's folder for each Brief task
    designs, checks = step_card(1), step_card(2)
    for row in rows:
        snap = next((f for f in row["snapshots"] if f["group"] == g["group"]), None)
        title = _e(design_title(row))
        if snap is None:
            missing = (f'<h3>{title}</h3><div class=mut>not designed this way yet'
                       + ("" if snapshot["static"] else
                          f' <button class=do data-action=new-folder data-row="{_e(row["id"])}" '
                          f'data-method="{_e(g["group"])}">New Design Folder</button><span class=msg></span>')
                       + '</div>')
            designs += missing
            checks += f'<h3>{title}</h3><div class=mut>not designed this way yet</div>'
            continue
        link = (f'<h3><a href="{_e(_page_url(snapshot, snap["rel"], "design"))}">{title}</a> '
                f'<span class=mut>{_e(snap["reason"] if not snap["current"] else _folder_summary(snap))}</span></h3>')
        drows, crows = [], []
        for it in snap["items"]:
            shown = it.get("ready") or it.get("latest")
            why = _rationale(snap["folder"], shown["run"]) if shown else {}
            text = _e(shown["text"]) if shown else '<span class=mut>no draft yet</span>'
            drows.append(f'<tr><td>{_e(why.get("message") or it["id"])}</td><td class=msg-text>{text}</td>'
                         f'<td>{_e(why.get("reason", ""))}</td></tr>')
            verdict = ("✅ pass" if it.get("ready") else
                       f'{_e(it.get("glyph", ""))} {_e(it["state"])}')
            crows.append(f'<tr><td>{_e(why.get("message") or it["id"])}</td><td>{verdict}</td>'
                         f'<td>{_e(why.get("forecast", "").replace("the designer" + chr(39) + "s forecast: ", ""))}</td></tr>')
        designs += link + ('<table class=msgs><tr><th>design</th><th>message</th><th>why</th></tr>'
                           + "".join(drows) + '</table>' if drows else '<div class=empty>No design registered yet.</div>')
        checks += link + ('<table class=msgs><tr><th>design</th><th>verify</th><th>predicted click-through</th></tr>'
                          + "".join(crows) + '</table>' if crows else '<div class=empty>Nothing to check yet.</div>')
    if not rows:
        designs, checks = designs + empty, checks + empty

    steps = (("see", "① See input", see), ("designs", "② Designs", designs), ("check", "③ Check output", checks))
    return (f'<h2>{_e(g["label"])}</h2>' + (f'<div class=mut>{lead}</div>' if lead else "")
            + '<div class=steps>' + "".join(f'<button type=button data-step="{k}"{" class=on" if k == "designs" else ""}>{v}</button>'
                                             for k, v, _ in steps) + '</div>'
            + "".join(f'<div class="step{" on" if k == "designs" else ""}" data-step="{k}">{b}</div>' for k, _, b in steps))


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
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8;--ext:#7a4f9a;--acc-soft:#e6edf5}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a;--ext:#b896d6;--acc-soft:#22304a}}
*{box-sizing:border-box}body{margin:0;padding:16px 18px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px}
h1{font-size:18px;margin:0 0 2px;font-weight:700}h2{font-size:14px;margin:18px 0 6px;font-weight:650}
.mut{color:var(--mut);font-size:12.5px}.bad{color:var(--bad)}.ok{color:var(--ok)}
/* one tab style for every workbench (JL 261003), the Guide's: a Space tab is a filled pill when on */
.tabs{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}
.tabs button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;cursor:pointer;background:#fff;color:#1e1e1e}
.tabs button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}
@media(prefers-color-scheme:dark){.tabs button{background:#191c21;color:#edf0f4;border-color:#414852}.tabs button.on{background:#253749;color:#91caff;border-color:#91caff}}
/* the board header, as the Insight board draws it (JL 261003) */
.dataset{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;background:var(--acc-soft,#e6edf5);color:var(--acc);font-size:14px}
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
/* the Method page: a part (A · …) above its sub-sections (A1 · …) (Paper session, 261003) */
article.theory h2{font-size:18px;margin:28px 0 8px;padding-top:12px;border-top:1px solid var(--line)}article.theory h3{font-size:14.5px;margin:18px 0 6px;font-weight:650}
details.draw-fold,details.sec-fold{margin:4px 0 12px;border:1px solid #dee2e6;border-radius:8px}details.sec-fold>summary{padding:14px 16px;cursor:pointer}details.sec-fold>summary strong{color:#1864ab;font-size:18px;font-weight:500}.sec-body{padding:0 18px 14px}.sec-body>h3:first-child{margin-top:4px}@media(prefers-color-scheme:dark){details.sec-fold{border-color:#414852}details.sec-fold>summary strong{color:#91caff}}
details.draw-fold>summary{padding:14px 16px;cursor:pointer}details.draw-fold>summary strong{color:#1864ab;font-size:18px;font-weight:500}
details.draw-fold>summary span{display:block;color:var(--mut);font-size:14px;margin-top:3px;margin-left:18px}.draw-body{padding:0 12px 12px}
@media(prefers-color-scheme:dark){details.draw-fold{border-color:#414852}details.draw-fold>summary strong{color:#91caff}}
details.ref-fold{margin:22px 0 0;border-top:1px solid var(--line);padding-top:10px}details.ref-fold>summary{cursor:pointer;font-weight:650;font-size:15px}
ul.fam-methods{margin:4px 0 10px;padding-left:18px}ul.fam-methods li{margin:3px 0}.steps{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 12px}.steps button{font:400 14px system-ui,sans-serif;padding:4px 12px;border:1px solid #ced4da;border-radius:14px;background:#fff;color:#1e1e1e;cursor:pointer}.steps button.on{background:#f1f3f5;border-color:#495057;font-weight:600}.step{display:none}.step.on{display:block}.step-card{border:1px solid #dee2e6;border-radius:8px;padding:2px 14px;margin:0 0 12px;background:#f8f9fa}details.packet{border:1px solid #dee2e6;border-radius:8px;margin:0 0 10px}details.packet>summary{padding:8px 12px;cursor:pointer}.packet-body{padding:0 14px 8px;max-height:520px;overflow:auto}table.msgs td:first-child{white-space:nowrap}table.msgs td.msg-text{font-family:ui-monospace,Menlo,monospace;font-size:13px;width:52%}@media(prefers-color-scheme:dark){.steps button{background:#191c21;color:#edf0f4;border-color:#414852}.steps button.on{background:#253749}.step-card,details.packet{border-color:#414852;background:transparent}}
/* a View (sub-Space) tab, the same look as a Space tab (JL 261003) */
.views{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}.views button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;background:#fff;color:#1e1e1e;cursor:pointer}
.views button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}
@media(prefers-color-scheme:dark){.views button{background:#191c21;color:#edf0f4;border-color:#414852}.views button.on{background:#253749;color:#91caff;border-color:#91caff}}.view{display:none}.view.on{display:block}
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


# Guide › Method is one document (JL 261003): the six steps, then steps 2, 3, 4 and 6 in depth,
# why it works, and the reference, folded. The older
# view keys (design-theory, methods) read the same file.
METHODS = Path(__file__).resolve().parent / "guide" / "method.md"        # the theme's Guide (261007)
THEORY = METHODS
# The methods studio (JL 261002: "add a new studio … put it in the excalidraw to explain
# these methods"): one Excalidraw drawing of the loop, the families and the ten cards,
# opened in the self-hosted canvas and saved back to this file.
# The design theme's drawings live in its Block's studio, each in its topic (JL 261007), like any Block's.
B12 = Path(__file__).resolve().parents[4] / "blueprints" / "b12_theme_design" / "studio"
STUDIO = B12 / "s03-design-methods" / "parts" / "design-methods.excalidraw"
# The design unit (JL 261004: "each column to be the step … lines across different elements to be
# a method"): See input → Conduct process → Check output, each step's parts with their options above,
# and one row per method below, its choice in every part.
# Written by Tools/blueprints/b12_theme_design/studio/s03-design-methods/design_unit_drawing.py.
UNIT = B12 / "s03-design-methods" / "parts" / "design-unit-methods.excalidraw"


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
        # a web link, [text](https://...), opens in a new tab (JL 261003: the people's wiki pages)
        t = re.sub(r"\[([^\]]+)\]\((https?://(?:[^()\s]|\([^()\s]*\))+)\)",   # a DOI may hold (05)
                   r'<a href="\2" target=_blank rel=noopener>\1</a>', t)
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
        if line.strip() and re.fullmatch(r"=+|-+|~+", nxt.strip()) and len(nxt.strip()) >= 3:
            flush()
            tag = {"=": "h1", "-": "h2", "~": "h3"}[nxt.strip()[0]]       # ~~~ under a title: a sub-section
            out.append(f'<{tag}>{inline(line.strip())}</{tag}>')
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
                ("papers", "Papers"), ("method", "Method"))
# `method` is Guide › Method's one page (JL 261003: "move the design theory things to here";
# no view named Design methods): the theory, its sections 1 to 9, then the method cards,
# 10 to 12, then the methods drawing. The other keys stay for old links and for Insight.


def studio_html(root: Path, drawing: Path = STUDIO, note: str = "") -> str:
    """Theory › Methods studio: the methods drawing in the Excalidraw canvas, editable, as
    the Paper workbench's RoadMap Draw shows a Story's drawing. It loads only when shown."""
    rel = _href(root, drawing) if Path(drawing).is_file() else ""
    if not rel:
        return '<div class=empty>No methods drawing yet: the design workbench keeps it as <code>b12_theme_design/studio/s03-design-methods/parts/design-methods.excalidraw</code>.</div>'
    url = "/_excalidraw/?board=" + quote(rel.lstrip("/"), safe="/") + "&edit=1"
    note = note or ('The four kinds of reasoning, three inputs, Design and the Exp, the Revise and Learning loops, '
                    'three families, the cards and the tests.')
    return (f'<div class=st-bar><span class=mut>{_e(note)} Edits save to <code>{_e(Path(drawing).name)}</code>.</span>'
            f'<a href="{_e(url)}" target="_blank" rel="noopener">Open full screen ↗</a></div>'
            # no referrer: Excalidraw refuses a same-site embed ("I'm not a pretzel!")
            f'<iframe class=st-frame title="Methods studio" referrerpolicy="no-referrer" data-src="{_e(url)}"></iframe>')


def theory_page(board: Path, root: Path | None = None, view: str = "design-theory", only=None) -> str:
    """The theory of design: one view at a time, its name in a bar above it. `only` keeps a
    subset of the views, in its order (Guide's Method shows the methods, the studio and
    the theory; its Related Paper shows the papers alone)."""
    def article(path: Path, cls: str, empty: str) -> str:
        if path.is_file():
            return f'<article class="{cls}">{_plain_md(path.read_text(encoding="utf-8"))}</article>'
        return f'<div class=empty>{empty}</div>'
    # build only the views this page shows (JL 261003: "why it takes such a long time"): the papers
    # view reads every Paper Run, about six seconds, and Guide › Method never shows it
    builders = {
        "design-theory": lambda: article(THEORY, "theory", "No design theory file is present."),
        "methods": lambda: (f'<article class="theory">{_plain_md(_read(METHODS), method_cards(board, root or board, METHODS, PAPERS, in_use="in the Exp", now="in Evaluate"))}</article>'
                            if METHODS.is_file() else '<div class=empty>No design methods file is present.</div>'),
        "studio": lambda: studio_html(root or board, STUDIO),
        "unit": lambda: studio_html(root or board, UNIT, "One design unit in five steps; ③ and ④ run once per "
                                    "idea. Above, every choice in each step; below, one row per method, holding "
                                    "only the choices that make it."),
        "papers": lambda: papers_page(board, root or board, PAPERS)}
    wanted = set(only) if only else {k for k, _ in THEORY_VIEWS if k != "method"}
    if "method" in wanted:
        wanted |= {"methods", "studio", "unit"}
    views = {k: build() for k, build in builders.items() if k in wanted}
    if "method" in wanted:
        untitled = lambda h: re.sub(r"<h1>.*?</h1>", "", h, count=1)
        # the drawing first, the method in one picture (JL 261003: "maybe put it at the top?")
        page = untitled(views["methods"])
        # every part folds, in the drawing's card style (JL 261003: "make each section collapsable"),
        # and every card starts closed, as on the shared Method page ("make it into this style")
        inner = page[page.find(">") + 1:page.rfind("</article>")] if page.startswith("<article") else page
        bits = re.split(r"(<h2>.*?</h2>)", inner)
        cards = bits[0]
        for title_html, body in zip(bits[1::2], bits[2::2]):
            title = re.sub(r"<[^>]+>", "", title_html)
            cards += (f'<details class=sec-fold><summary><strong>{title}</strong>'
                      f'</summary><div class=sec-body>{body}</div></details>')
        page = f'<article class="theory">{cards}</article>'
        # the drawing in a folding card, as Guide › RoadMap Draw shows "Workbench design" (JL 261003)
        # no subtitle under the card's name (JL 261003: "do not add this, delete it")
        views["method"] = ('<details class=draw-fold><summary><strong>Method design</strong>'
                           f'</summary><div class=draw-body>{views["studio"]}</div></details>'
                           # the design unit beside it (JL 261004: "put it in the method")
                           '<details class=draw-fold><summary><strong>Design unit · See input → Reason ideas → '
                           'Conduct process → Check output → Check overall</strong></summary>'
                           f'<div class=draw-body>{views["unit"]}</div></details>' + page)
    labels = dict(THEORY_VIEWS)        # `only` also sets the order (Guide's Method: methods first, theory last)
    plain = [(k, v) for k, v in THEORY_VIEWS if k != "method"]    # Method shows only when asked for
    shown = [(k, labels[k]) for k in only if k in labels] if only else plain
    shown = shown or plain
    view = view if view in dict(shown) else shown[0][0]
    bar = "".join(f'<button type=button data-view="{k}"{" class=on" if k == view else ""}>{_e(label)}</button>'
                  for k, label in shown)
    return ((f'<div class=views>{bar}</div>' if len(shown) > 1 else "")
            + "".join(f'<div class="view{" on" if k == view else ""}" data-view="{k}">{views[k]}</div>' for k, _ in shown))


# Theory › Papers (JL 261001): the papers behind the theory, one card each. The rows are the
# workbench's own `related/papers.md`, the same for every board (JL 261002: "put them in
# the Tools of the workbench of the design"). The table's shape and check are the shared
# rule skills/0_utils/table-papers; its renderer is the shared live.related_papers (JL 261003:
# "this is the rule and should be shared"), imported here under the names it always had.
from .related_papers import (PAPER_ROLES, UTD24, _href, _paper_card, _paper_pdf, _run_abstract,  # noqa: E402,F401
                             is_utd24, paper_id, paper_rows, paper_runs, short_cite)
from .related_papers import papers_page as _papers_page  # noqa: E402

PAPERS = Path(__file__).resolve().parent / "related" / "papers.md"


def papers_page(board: Path, root: Path, table: Path = PAPERS) -> str:
    """Theory › Papers, through the shared Related Paper renderer."""
    return _papers_page(board, root, table)


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


CARD_KEYS = {"family", "also", "reasoning", "move", "status", "taxonomy", "comes from", "reads", "returns", "test now", "test in use", "rationale", "context",
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


# Theory › Design theory · Design methods · Methods studio · Papers: one view at a time, a
# paper's PDF loaded only when its card opens, a cited paper opening its card. Guide ›
# Methods frames the same page (render_theory_embed), so both use this one script.
_THEORY_JS = (
    # a Space's views (Theory: Design theory · Design methods · Papers): one shown at a time, kept in the URL
    "function loadFrames(pane){pane.querySelectorAll('.view.on iframe.st-frame[data-src]').forEach(function(f){"
    "if(f.closest('details:not([open])'))return;"          # a closed card's canvas loads when it opens
    "if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})}"
    "document.querySelectorAll('.pane').forEach(loadFrames);"
    "document.querySelectorAll('.views button').forEach(function(b){b.onclick=function(){"
    "var pane=b.closest('.pane');pane.querySelectorAll('.views button').forEach(function(x){x.classList.toggle('on',x===b)});"
    "pane.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',v.dataset.view===b.dataset.view)});"
    "loadFrames(pane);"
    "var u=new URL(location.href);u.searchParams.set('view',b.dataset.view);history.replaceState({},'',u)}});"
    # a paper's PDF loads only when its card opens; toggle does not bubble, so listen in capture
    "document.addEventListener('toggle',function(ev){var d=ev.target;if(d.matches&&d.matches('details.draw-fold')&&d.open)"
    "d.querySelectorAll('iframe.st-frame[data-src]').forEach(function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})},true);"
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
)


# the theory page sits inside Guide: a pinch over it must not zoom the tab (guide-mount.js says why)
_NO_PINCH = ("<script>addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false});"
             "['gesturestart','gesturechange','gestureend'].forEach(function(t){addEventListener(t,function(e){e.preventDefault()},{passive:false})})</script>")


def render_theory_embed(snapshot: dict, view: str = "methods", only=None) -> str:
    """The theory of design as one page, for Guide › Method to frame (JL 261002): Design
    theory · Design methods (the method cards) · Methods studio · Papers, one view at a time.
    Read-only; it tells its frame how tall it is."""
    theory_html = theory_page(Path(snapshot["board"]), Path(snapshot["root"]), view, only)
    height = ("<script>(function(){function post(){parent.postMessage({kind:'haipipe-explain-height',"
              "height:document.documentElement.scrollHeight},location.origin)}"
              "if(window.ResizeObserver)new ResizeObserver(post).observe(document.body);"
              "addEventListener('load',post);document.addEventListener('toggle',post,true);"
              "document.addEventListener('click',function(){setTimeout(post,60)},true)})()</script>")
    return ('<!doctype html><html lang=en><head><meta charset=utf-8>'
            '<meta name=viewport content="width=device-width,initial-scale=1">'
            # inside Guide this page's frame takes the page's own height, so nothing here is sized by the
            # viewport: a 100vh canvas would grow the frame, which grows the canvas, without end (JL 261003)
            f'<title>🎨 Design · {_e(view)}</title><style>{_CSS}body{{max-width:none;padding:2px 2px 12px}}.st-frame{{height:640px;min-height:0}}.rp-frame{{height:720px}}</style></head><body>'
            f'<main><section class="pane on" data-space=theory><div class=space-main>{theory_html}</div></section></main>'
            f'<script>(function(){{{_THEORY_JS}}})();</script>{height}{_NO_PINCH}</body></html>')


THEORY_SPACES = ("theory", "theories", "knowledge", "methods", "studio", "papers")


def render_design_board(snapshot: dict, space: str = "tasks", view: str = "design-theory") -> str:
    aliases = {"goal": "tasks", "brief": "tasks", "frame": "tasks", "plan": "tasks", "design": "tasks",
               "items": "tasks", "run": "tasks", "runs": "tasks", "delivery": "tasks", "ready": "tasks",
               "theories": "theory", "knowledge": "theory", "methods": "theory", "studio": "theory", "papers": "theory"}
    selected = "tasks"            # the one working Space; the theory is Guide's (below)
    # the header in the Insight board's style (JL 261003): the title, where to go next, one
    # line of facts in a band, then the Space buttons
    rel = snapshot["relative"]
    designs = sum(int(r["designs"]) for r in snapshot["brief_rows"] if str(r.get("designs") or "").isdigit())
    facts = [Path(rel or snapshot["root"]).name.split("_")[0] or "board",
             f'{len(snapshot["brief_rows"])} design task{"s" if len(snapshot["brief_rows"]) != 1 else ""}',
             f'{len(snapshot["folders"])} Design page{"s" if len(snapshot["folders"]) != 1 else ""}']
    if designs:
        facts.append(f"{designs} designs")
    if snapshot.get("methods"):
        n = sum(1 for g in snapshot["methods"] if g["key"])
        facts.insert(2, f'{n} method{"s" if n != 1 else ""}')
    header = (
        # the board's short name, the words before its title's colon (JL 261003: "this is too long");
        # the full title stays in the hover
        f'<h1 title="{_e(snapshot["title"])}">🎨 {_e(snapshot["title"].split(":", 1)[0].strip() or snapshot["title"])}</h1>'
        # no `all boards · board index` line (JL 261003: "could you remove this?")
        f'<div class=dataset>{_e(" · ".join(facts))}</div>'
    )                                    # no records-check line in the header (JL 261003: "remove this out")

    # Design Tasks Space: the list of design tasks, from the Brief, in one View per method family
    # (JL 261003: "why you don't add the subspace here? We have discussed different types of the
    # designing"): All tasks, then the six families of Guide › Method, each with its methods and
    # the tasks done by them. A task's method is its Brief row's `method` column.
    def task_row(row: dict) -> str:
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
        method = row.get("method") or ""
        # a page from before methods mixes them (JL 261003): shown, kept out of every family View
        method = ('<span class=mut title="designed before methods existed; kept out of the method comparison">'
                  'mixed · before methods</span>' if method.lower() == "mixed" else
                  _e(method) or '<span class=mut>not declared</span>')
        return (f'<tr data-row="{_e(row["id"])}"><td><b>{name}</b></td><td>{method}</td><td>{_e(progress)}</td>'
                f'<td>{folder_cell}</td>'
                f'<td class="{"bad" if not row["snapshot"] else ""}">{_e(row["status"])} {action}</td></tr>')

    def task_table(rows: list[dict]) -> str:
        return ('<table><tr><th>design task</th><th>method</th><th>designs</th><th>folder</th><th>state</th></tr>'
                + "".join(task_row(r) for r in rows) + '</table>')

    rows = snapshot["brief_rows"]
    if rows:
        all_html = '<h2>Design tasks</h2>' + task_table(rows)
    elif snapshot["brief"]:
        all_html = (f'<h2>Design tasks</h2><div class=empty>The design task file '
                    f'<code>{_e(snapshot["brief"].name)}</code> has no list yet; add the first design tasks from the Runs panel.</div>')
    else:
        all_html = '<h2>Design tasks</h2><div class=empty>No design task file under 0-BR-brief/; add one before listing design tasks.</div>'
    families: dict[str, dict] = {}
    for card in sorted((METHODS.parent / "methods").glob("*.md")):
        f = method_card_fields(card)
        label, _, gloss = f["head"].get("family", "").partition(":")
        fam = families.setdefault(label.strip() or "Other", {"gloss": gloss.strip(), "methods": []})
        fam["methods"].append(f)
    views = [("all", "All", all_html)]
    # every family View is the All table (JL 261003: "the same structure to the All"): one row per
    # design task; a task this family's methods design shows its page, the others a dash.
    def undesigned(title: str) -> str:
        return (f'<tr><td><b>{_e(title)}</b></td><td><span class=mut>—</span></td><td><span class=mut>—</span></td>'
                '<td><span class=mut>—</span></td><td class=mut>not designed this way yet</td></tr>')

    titles = list(dict.fromkeys(design_title(r) for r in rows))
    for n, (label, fam) in enumerate(families.items(), start=1):
        names = {m["name"].lower() for m in fam["methods"]}
        names |= {m["name"].lower() for f in families.values() for m in f["methods"]
                  if m["head"].get("also", "").lower().startswith(label.lower())}
        body_rows = []
        for title in titles:
            hits = [r for r in rows if design_title(r) == title and (r.get("method") or "").lower() in names]
            body_rows += [task_row(r) for r in hits] or [undesigned(title)]
        moves = "".join(f'<li><b>{_e(m["name"])}</b>'
                        + (' <span class=mut>· future</span>' if m["head"].get("status", "").lower().startswith("future") else "")
                        + f' <span class=mut>{_e(m["head"].get("move", ""))}</span></li>' for m in fam["methods"])
        body = (f'<h2>Design tasks · {_e(label)}</h2>'
                + (f'<div class=mut>{_e(fam["gloss"])}</div>' if fam["gloss"] else "")
                + ('<table><tr><th>design task</th><th>method</th><th>designs</th><th>folder</th><th>state</th></tr>'
                   + "".join(body_rows) + '</table>' if titles else '<div class=empty>No design task is listed yet.</div>')
                + f'<details class=fam-moves><summary>Its methods: {_e(" · ".join(m["name"] for m in fam["methods"]))}</summary>'
                  f'<ul class=fam-methods>{moves}</ul></details>')
        views.append((f"fam-{n}", label, body))      # the family name is the tab (JL 261003: Goal Only, …)
    if snapshot.get("methods"):
        views = _method_views(snapshot, rows)
    first = views[0][0] if views else "all"          # the View that opens: All, or the first method
    goal_html = ('<div class=views>' + "".join(f'<button type=button data-view="{k}"{" class=on" if k == first else ""}>{_e(v)}</button>'
                                             for k, v, _ in views) + '</div>'
                 + "".join(f'<div class="view{" on" if k == first else ""}" data-view="{k}">{b}</div>' for k, _, b in views))
    if snapshot["unlisted"]:
        goal_html += ('<div class=mut>folders no design task lists: '
                      + ", ".join(f'<a href="{_e(_page_url(snapshot, f["rel"], "goal"))}"><code>{_e(f["label"])}</code></a>'
                                  for f in snapshot["unlisted"]) + '</div>')
    rules = shared_rules(snapshot["items"])
    if rules:
        goal_html += ('<div class=task><span class=mut>every design task keeps</span> '
                      + " · ".join(_e(r) for r in rules) + '</div>')
    count = len(bundle_rows(snapshot))
    if count and not snapshot["static"]:
        goal_html += (f'<div class=mut><a href="/_board/design-bundle?path={quote(board_path_of(snapshot), safe="")}">'
                      f'↓ Download all designs · {count} · csv</a></div>')

    # JL 261002 ("follow the design here, workbench"; "work on the guide space first"):
    # the theory of design explains the family, so it is Guide › Method now, the same on
    # every board (render_theory_embed). The board keeps one working Space, its design tasks.

    # The board level has two Spaces (JL 261001): the design tasks, and the theory
    # every design draws on. Every design, run and delivery lives at the page level.
    root = Path(snapshot["root"])
    board_rel = board_path_of(snapshot).lstrip("/")
    runs = [r for f in snapshot["folders"] for r in (dict(x, folder=f.get("label", f["name"])) for x in f["runs"])]
    panes = {"tasks": goal_html}
    for key in panes:
        panel = design_runs_panel(key, runs, root=root, page=board_rel, board=board_rel,
                                  whole="this board")
        panes[key] = f'<div class=space-main>{panes[key]}</div>{panel}'
    panel_css, panel_js = runs_panel_assets()
    tabs = "".join(f'<button type=button data-space="{k}"{" class=on" if k == selected else ""}>{v}</button>'
                   for k, v in (("tasks", "Design Tasks"),))
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
        + _THEORY_JS +
        "document.querySelectorAll('.steps button').forEach(function(b){b.onclick=function(){var v=b.closest('.view')||document;"
        "v.querySelectorAll('.steps button').forEach(function(x){x.classList.toggle('on',x===b)});"
        "v.querySelectorAll('.step').forEach(function(x){x.classList.toggle('on',x.dataset.step===b.dataset.step)})}});"
        "document.querySelectorAll('button.do').forEach(function(b){b.onclick=function(){"
        "var box=b.closest('[data-act]'),msg=b.parentNode.querySelector('.msg'),body={path:BOARD,action:b.dataset.action,row:b.dataset.row||'',method:b.dataset.method||''};"
        "if(box){box.querySelectorAll('input,textarea,select').forEach(function(f){if(f.name)body[f.name]=f.value})}"
        "msg.className='msg';msg.textContent='writing…';b.disabled=true;"
        "fetch('/_board/design-board-act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})"
        ".then(function(r){return r.json()}).then(function(j){if(!j.ok){msg.className='msg bad';msg.textContent=j.err||'refused';b.disabled=false;return}"
        "location.href=j.url}).catch(function(e){msg.className='msg bad';msg.textContent=String(e);b.disabled=false})}});})();</script>"
    )
    document = (
        '<!doctype html><html lang=en><head><meta charset=utf-8>'
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        f'<title>🎨 Design Board · {_e(snapshot["title"])}</title><style>{_CSS}{panel_css}</style></head><body>'
        f'<header>{header}</header><nav class="tabs spaces">{tabs}</nav><main>{pane_html}</main>{script}{panel_js}</body></html>'
    )
    if snapshot["static"]:
        return document
    from live.workbench_guide import mount_guide
    return mount_guide(document, "design", {"path": board_path, "file": "board.md"},
                       "nav.tabs", "main")


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
        line = by_folder.get(i.get("folder_name", i["folder"]), {})
        rows.append({
            "line": line.get("id", ""), "who": line.get("audience") or i.get("audience", ""),
            "their_job": line.get("job") or i.get("job", ""), "venue": line.get("venue") or i.get("type", ""),
            "folder": i["folder"], "method": i.get("method", ""), "item": i["id"], "title": i["title"], "state": i["state"], "text": with_link(design["text"]),
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
    if snapshot.get("methods"):              # a board with method folders says each design's method
        fields.insert(fields.index("folder") + 1, "method")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n", extrasaction="ignore")
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
        space, view = (query.get("space") or ["goal"])[0], (query.get("view") or [""])[0]
        embed = (query.get("embed") or [""])[0]
        if space in THEORY_SPACES and embed != "theory":
            # the theory moved into Guide (JL 261002): an old link opens Guide › Method (papers: Related Paper)
            self.send_response(303)
            # Guide's views (261002): Method holds the theory; Related Paper the papers
            target = "related-paper" if space == "papers" or view == "papers" else "method"
            self.send_header("Location", "/_board/design-board?" + urlencode({"path": raw, "guide": target}))
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if embed == "theory":
            # the theory page reads only the board's place, never its pages, items or runs: building
            # the whole board snapshot first took about six seconds (JL 261003: "such a long time")
            only = [v for v in ((query.get("views") or [""])[0]).split(",") if v] or None
            body = render_theory_embed({"board": board, "root": self.root}, view or "methods", only).encode("utf-8")
        else:
            snapshot = design_board_snapshot(board, self.root)
            body = render_design_board(snapshot, space, view or "design-theory").encode("utf-8")
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
                out = new_folder(board, str(payload.get("row") or ""), str(payload.get("method") or ""))
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
