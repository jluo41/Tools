"""The DesignBoard page: its Design Tasks Space, one View per method family or method, and the designs bundle
(split from designboard.py, which re-exports every name here)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live.design import (
    _escape as _e, _json, _read,
    because_words, shared_rules,
    with_link, design_runs_panel, design_title, runs_panel_assets,
)
from live.designboard_snapshot import _folder_summary
from live.designboard_style import _CSS, _THEORY_JS
from live.designboard_theory import METHODS, _plain_md, method_card_fields


# ----------------------------------------------------------------- render --


def _page_url(snapshot: dict, rel: str, space: str = "design", item: str = "") -> str:
    board_path = "/" + (f'{snapshot["relative"]}/board.md' if snapshot["relative"] else "board.md")
    url = f'/_board/design?path={quote(board_path, safe="")}&file={quote(rel, safe="")}&space={space}'
    return url + (f"&item={quote(item)}" if item else "")


def _method_views(snapshot: dict, rows: list[dict]) -> list[tuple[str, str, str]]:
    """Design Tasks on a board with method folders: one View per method, its method.md card above
    the table of that method's tasks (the table the family Views use). No All View; the first
    method opens."""
    empty = '<div class=empty>No design task is listed yet.</div>'
    groups = snapshot["methods"]
    views = []                     # no All View: the methods alone
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
    """One method's View (a subsubspace under each method): the design unit's three
    steps as its own Views, ① See input · ② Designs · ③ Check output, each step's part of the
    method card on top. ② opens: the messages themselves, task by task."""
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
        see += (f'<details class=packet><summary>The packet · <code>{_e(rel)}</code></summary>'
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


def render_design_board(snapshot: dict, space: str = "tasks", view: str = "design-theory") -> str:
    selected = "tasks"            # the one working Space; the theory is Guide's (below)
    # the header in the Insight board's style: the title, where to go next, one
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
        # the board's short name, the words before its title's colon;
        # the full title stays in the hover
        f'<h1 title="{_e(snapshot["title"])}">🎨 {_e(snapshot["title"].split(":", 1)[0].strip() or snapshot["title"])}</h1>'
        # no `all boards · board index` line
        f'<div class=dataset>{_e(" · ".join(facts))}</div>'
    )                                    # no records-check line in the header

    # Design Tasks Space: the list of design tasks, from the Brief, in one View per method family
    #: All tasks, then the six families of Guide › Method, each with its methods and
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
        # the task by its full name (job · venue · who), never the Brief's row id
        name = _e(design_title(row))
        if row["snapshot"] is not None:
            name = f'<a href="{_e(_page_url(snapshot, row["snapshot"]["rel"], "design"))}">{name}</a>'
        method = row.get("method") or ""
        # a page from before methods mixes them: shown, kept out of every family View
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
    # every family View is the All table: one row per
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
        views.append((f"fam-{n}", label, body))      # the family name is the tab (Goal Only, …)
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

    # The theory of design explains the family, so it is Guide › Method now, the same on
    # every board (render_theory_embed). The board keeps one working Space, its design tasks.

    # The board level has two Spaces: the design tasks, and the theory
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
