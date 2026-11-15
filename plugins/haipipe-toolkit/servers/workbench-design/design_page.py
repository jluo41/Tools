"""The older Design Page-Folder, drawn: its CSS, the item cards, the evidence chain, the element matrix and the page.

design.py reads the folder, decides what may run and serves it; this module turns that snapshot into HTML.
Its parts live in the ``design_page_*`` modules beside it (css, runs, evaluation, chain, elements,
card); every name they hold still answers here.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
import re

from live.design import (
    _VENUE_LABEL, _escape, _read, design_chat_copy_script, design_chat_prompt, design_input, design_number,
    design_picture, design_runs_panel, renamed_folder, runs_panel_assets, venue_defaults, with_link,
)
from live.design_page_css import _CSS
from live.design_page_runs import _href, _run_rows
from live.design_page_card import _item_card, _sms_bubble, _task_block, shared_rules
from live.design_page_elements import _element_matrix_html

# Names that once lived here, kept answering for older imports (and design.py's _PAGE_NAMES).
from live.design import (  # noqa: F401  (re-exported)
    LINK_SLOT, _BECAUSE, _LEVEL_WORD, _SIGNED, _STEP, _board_page, _cited_page, _held_at, _nearest_board,
    _relative_href, _stale_names, _yaml, because_rule, design_chat_copy, design_next_run, design_title,
    name_refs, shown_design, yaml,
)
from live.design_page_runs import (  # noqa: F401  (re-exported)
    _CONTRACT_WORDS, _CRITERION_WORDS, _actions, _artifact_details, _checks_details, _criterion_words,
    _design_runs_list, _revise_of, _rule_words, _whole_word, plain_words, run_short,
)
from live.design_page_evaluation import (  # noqa: F401  (re-exported)
    _bet_changed, _evaluation_col, _review_notes, _rule_checks,
)
from live.design_page_chain import (  # noqa: F401  (re-exported)
    _LEVEL_ID, _LINEAGE, _PAGE_STEM_ID, _REF_TOKEN, _STEP_WORD, _SUPPORT_ROLES, _chain_heads, _chain_html, _code,
    _compact, _expand, _insight_href, _level, _level_of, _page_id, _page_link, _page_words, _row_lineage,
    _row_texts, _walk, because_rows, evidence_chain,
)
from live.design_page_elements import (  # noqa: F401  (re-exported)
    _ABBREV, _FROM, _SLOT_PART, _SLOT_TOKEN, _elements_html, _ids, _norm, _record_html, design_elements,
    element_record, element_slots, record_reading, slot_reading,
)
from live.design_page_card import _card_columns, _rationale_col  # noqa: F401  (re-exported)


def _input_html(root: Path, row: dict, inp: dict, counts: str, rules: list[str], lead: str = "") -> str:
    """The Design Goal Space: the task's design input as column tables, as in the Paper workbench."""
    # The screen shows the specification only; where each line came from stays in the
    # file after `<-` (no source column, no file ids on screen).
    blocks = inp["blocks"]

    def cell(value: str) -> str:
        return '<span class=mut>Not specified</span>' if value in ("", "?") else _escape(value)

    def grid(title: str, heads: tuple[str, ...], rows: list[str]) -> str:
        head = "".join(f"<th>{_escape(h)}</th>" for h in heads)
        return f'<h3>{title}</h3><table class="grid input"><tr>{head}</tr>{"".join(rows)}</table>'

    def line(key: str, value: str) -> str:
        return f'<tr><td class=key>{_escape(key[:1].upper() + key[1:])}</td><td>{cell(value)}</td></tr>'

    job = (row["job"] or "").strip()
    out = []
    aim = [line(k, v) for k, v, _ in blocks.get("Aim", [])]
    if job and not any(k.lower() == "patient task" for k, _, _ in blocks.get("Aim", [])):
        aim.insert(1, line("Patient task", job[:1].upper() + job[1:]))
    aim.append(f'<tr><td class=key>Deliverables</td><td>{counts}</td></tr>')
    views = {"aim": [grid("Aim", ("Item", "Specification"), aim)], "requirements": [], "resources": [], "leave-out": []}
    venue = row["venue"] or ""
    defaults = {k: v[:1].upper() + v[1:] for k, v in venue_defaults(venue).items()}
    used, rows = set(), []
    for key, value, _ in blocks.get("Venue", []):
        used.add(key.lower())
        rows.append(f'<tr><td class=key>{_escape(_VENUE_LABEL.get(key.lower(), key))}</td><td>{cell(value)}</td>'
                    f'<td class=mut>{_escape(defaults.get(key.lower(), "—"))}</td></tr>')
    rows += [f'<tr><td class=key>{_escape(_VENUE_LABEL.get(k, k))}</td><td class=mut>As the channel standard</td>'
             f'<td class=mut>{_escape(v)}</td></tr>' for k, v in defaults.items() if k not in used]
    name = venue.upper() if len(venue) <= 4 else venue.title()
    views["requirements"].append(grid(f"Channel requirements · {_escape(name)}", ("Requirement", "This task", f"{name} standard"), rows)
               if rows else f'<h3>Channel requirements · {_escape(name)}</h3><div class=empty>No channel profile for {_escape(venue)}.</div>')
    rule_rows = [line(k, v) for k, v, _ in blocks.get("Rules", [])]
    if rules:
        rule_rows.append(f'<tr><td class=key>Acceptance checks</td><td>{"<br>".join(_escape(r) for r in rules)}</td></tr>')
    views["requirements"].append(grid("Rules", ("Item", "Specification"), rule_rows))
    for key, title, heading in (("resources", "Resources", "Inputs and resources"), ("leave-out", "Leave out", "Exclusions")):
        views[key].append(grid(heading, ("Item", "Specification"), [line(k, v) for k, v, _ in blocks[title]])
                          if blocks.get(title) else f'<div class=empty>No {title.lower()} block in design-goal.md.</div>')
    # one view at a time, as the Guide's tabs
    labels = (("aim", "Aim"), ("requirements", "Requirements"), ("resources", "Resources"), ("leave-out", "Leave out"))
    # the View tabs head the Space, as Insight's Questions · Studio; `lead` (the task) sits under them
    out.append('<div class=views>' + "".join(f'<button type=button data-view="{k}"{" class=on" if k == "aim" else ""}>{v}</button>'
                                             for k, v in labels) + '</div>' + lead
               + "".join(f'<div class="view{" on" if k == "aim" else ""}" data-view="{k}">{"".join(views[k])}</div>'
                         for k, _ in labels))
    if not inp["path"]:
        out.append('<div class=bad>No design-goal.md beside board.md: only the task line is shown.</div>')
    return "".join(out)


# There is no bar that acts on every item at once. JL asked on 260921 for it to go:
# one decision, one item, one sentence on the record. The all-items writers in
# design_actions are no longer reachable from a surface, and perform_action refuses
# the `-all` actions the way it already refuses `adopt-all`.


def render_design(snapshot: dict, space: str = "goal", selected_item: str = "",
                  flow_space: str | None = None, query: dict | None = None) -> str:
    """Three Spaces: Goal (the one design task, stated once), Design (the task
    again, then one card per design: Design · Rationale · Supporting work · Expectation, with
    its insight pages and its runs folded inside), Delivery (designs whose Verify passed).
    The old Insight and Run Spaces open the Design Space."""
    root = snapshot["root"]
    items = snapshot["items"]
    human = snapshot.get("human", "person")
    aliases = {"frame": "goal", "plan": "goal", "brief": "goal", "ask": "goal",
               "intent": "design", "draft": "design", "items": "design",
               "insight": "design", "signal": "design", "evidence": "design", "insights": "design",
               "run": "design", "runs": "design", "shape": "design", "workflow": "design", "runtime": "design",
               "create": "design", "review": "design", "launch": "delivery", "commit": "delivery"}
    selected = aliases.get(space, space) if space else "goal"
    if selected not in ("goal", "design", "delivery"):
        selected = "goal"
    ids = [item["id"] for item in items]
    if selected_item not in ids:
        selected_item = ""
    q = query or {}
    # the owning board, two folders up (2-Design/<page>/): a /w/ link passes the page itself as path
    board_md = Path(snapshot["folder"]).parent.parent / "board.md"
    try:
        board_rel = "/" + board_md.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        board_rel = ""
    board_link = (f' · <a href="/_board/design-board?path={quote(board_rel, safe="")}">↑ Board level</a>'
                  if board_rel and board_md.is_file() else "")
    # the header as the Insight board and the Shared Workbench draw it: the title, where to go next, one band of facts, then the Space tabs
    goal = snapshot.get("goal") or {}
    name = snapshot["folder"].name
    facts = ["-".join(name.split("-")[:2]) if name.startswith("Design-") else name]
    if goal.get("wanted"):
        facts.append(f'{goal["wanted"]} designs asked')
    facts += [f'{goal.get("registered", len(items))} registered', f'{goal.get("ready", 0)} ready']
    # a Design Folder under 2-Design-M<NN>-<slug>/ is made by that method: its name
    # in the band, from the method folder's method.md
    group = Path(snapshot["folder"]).parent
    if re.match(r"^2-Design-M\d+-", group.name):
        card = group / "method.md"
        hit = re.search(r"(?m)^#\s+(.+?)\s*$", _read(card)) if card.is_file() else None
        facts.insert(1, hit.group(1) if hit else group.name.replace("2-Design-", "").replace("-", " "))
    header = (
        f'<h1>🎨 {_escape(snapshot["title"])}</h1>'
        # only the Board-level link; no `all boards · board index` line
        + (f'<div class=mut>{board_link.replace(" · ", "", 1)}</div>' if board_link else "")
        + f'<div class=dataset title="{_escape(name)}">{_escape(" · ".join(facts))}</div>'
    )
    if not snapshot["current"]:
        header += f'<div class=bad>{_escape(snapshot["reason"])}</div>'
    # no insight-eligibility line in the header
    if not snapshot["yaml"]:
        header += '<div class=bad>PyYAML is not installed for this server; Run records cannot be read.</div>'

    # Goal Space -------------------------------------------------------------
    goal = snapshot["goal"]
    missing = max(goal["wanted"] - goal["registered"], 0)
    request = snapshot.get("draft_request")
    if goal["row"]:
        row = goal["row"]
        # counts is HTML from here on: the text is escaped once, the button below is markup
        declined = sum(1 for i in items if i["state"] == "declined")
        counts = _escape((f'{goal["wanted"]} designs requested · ' if goal["wanted"] else "") +
                         f'{goal["registered"]} registered · {goal["ready"]} ready'
                         + (f' · {declined} declined' if declined else ""))
        if missing and request:
            counts += (f' · <span class=mut>draft request open: {request["items"]} item(s) asked by '
                       f'{_escape(request["asked_by"])} {_escape(request["asked_at"][:16])}</span>')
        elif missing and snapshot["current"] and not snapshot.get("static"):
            counts += (f' <span class=act data-item="__all__"><button class=do data-action=draft-request>'
                       f'Ask the agent to draft the missing {missing}</button><span class=msg></span></span>')
        board_dir = Path(snapshot["folder"]).parent.parent
        goal_html = _input_html(root, row, design_input(board_dir, Path(snapshot["folder"])), counts,
                                shared_rules(items),
                                lead='<h2>The design task</h2>'
                                     f'<pre class=text>{_escape(goal["sentence"])}</pre>')
    elif goal["brief"]:
        goal_html = (f'<div class=empty>No line in {_href(root, goal["brief"], goal["brief"].name)} names this folder yet; '
                     'add a row (audience · job · venue · designs · folder) and the goal appears here.</div>')
    else:
        goal_html = '<div class=empty>No design task file under 0-BR-brief/ on the owning board; the goal has nowhere to be read from.</div>'

    # Design Space -----------------------------------------------------------
    writable = snapshot["current"] and not snapshot.get("static")
    chat_prompts = {item["id"]: design_chat_prompt(snapshot, item) for item in items}
    inp = design_input(Path(snapshot["folder"]).parent.parent, Path(snapshot["folder"]))
    # every design-input line by its key: the aim, and the starting text and opt-out the elements read
    aim = {k.lower(): v for block in ("Venue", "Resources", "Aim") for k, v, _ in inp["blocks"].get(block, [])}
    design_html = _task_block(snapshot, items, aim)
    design_html += _element_matrix_html(items, aim)

    if items:
        # A declined item is retired: its card stays for the record, folded after the live ones.
        live = [item for item in items if item["state"] != "declined"]
        retired = [item for item in items if item["state"] == "declined"]
        design_html += ('<div class="mut foldbar"><a href=# data-fold=open>open all</a> · '
                        '<a href=# data-fold=close>close all</a></div>'
                        '<div class=cardhead><span>Design</span><span>Rationale</span>'
                        '<span>Evaluation</span></div>')
        design_html += "".join(_item_card(root, item, human, item["id"] == selected_item, writable=writable,
                                         chat_prompt=chat_prompts[item["id"]], aim=aim)
                               for item in live)
        if retired:
            opened = " open" if selected_item in {item["id"] for item in retired} else ""
            design_html += (f'<details class=retired{opened}><summary>Declined, kept for the record · {len(retired)}</summary>'
                            + "".join(_item_card(root, item, human, item["id"] == selected_item, writable=writable,
                                                 aim=aim) for item in retired)
                            + '</details>')
    else:
        design_html = (f'<div class=empty>No Design Item register yet. Add the first item below; it writes '
                       f'<code>{_escape(snapshot["register"].relative_to(snapshot["folder"]).as_posix())}</code>.</div>')
    if snapshot["unassigned"]:
        design_html += ('<h2>Runs without an item</h2>'
                        '<table><tr><th>run</th><th>Run type</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["unassigned"])}</table>')

    # Design Space, continued: runs that name no item, and the records check -----
    if not items and not snapshot["runs"]:
        design_html += '<div class=empty>No Design Run records are present in this folder.</div>'
    if not items and snapshot["runs"]:
        design_html += ('<h2>Runs</h2><table><tr><th>run</th><th>Run type</th><th>who</th><th>when</th><th>status</th><th>outcome</th><th>next</th></tr>'
                        f'{_run_rows(root, snapshot["runs"])}</table>')
    audit = snapshot["audit"]
    if snapshot["current"]:
        if audit:
            design_html += (f'<details><summary class=bad>records check: {len(audit)} finding(s)</summary><ul class=rules>'
                            + "".join(f"<li><code>{_escape(issue)}</code></li>" for issue in audit) + '</ul></details>')
        else:
            design_html += '<div class="mut ok">records check: PASS · every run has its result and receipt</div>'

    # Delivery Space ---------------------------------------------------------
    # A quick overview of what is ready to hand to the next team: one row per
    # item whose independent Verify passed.
    def listing(group: list[dict]) -> str:
        rows, tiles = [], []
        for item in (item for item in group if item.get("ready")):
            design = item.get("ready")
            label = _escape(design_number(item["id"]))
            if q.get("path") and q.get("file"):
                label = (f'<a href="?path={quote(str(q["path"]), safe="")}&amp;file={quote(str(q["file"]), safe="")}'
                         f'&amp;space=design&amp;item={_escape(item["id"])}">{label}</a>')
            sent = with_link(design["text"]) if design else ""
            text_html = (_sms_bubble(sent) if design and (item["type"] or "").lower() == "sms"
                         else _escape(sent) if design else "")
            body = (f"<div class=design>{text_html}</div>" if design else "<span class=mut>not ready for Delivery yet</span>")
            rows.append(f'<tr><td class=who><b>{label}</b><div class=mut>{_escape(item["title"])}</div></td><td>{body}</td></tr>')
            tiles.append(f'<figure>{design_picture(root, item) or body}'
                         f'<figcaption><b>{label}</b> {_escape(item["title"])}</figcaption></figure>')
        if any(item.get("render") and item.get("ready") for item in group):
            # Screens read side by side as pictures; text designs keep the table.
            return f'<div class=gallery>{"".join(tiles)}</div>'
        return ('<table class=designs><tr><th>design</th><th>the text, word for word</th></tr>' + "".join(rows) + '</table>') if rows else ""

    # A declined item is retired, like a retired Evidence Item: kept for the record, out of the overview.
    live = [item for item in items if item["state"] != "declined"]
    retired = [item for item in items if item["state"] == "declined"]
    delivery_html = [listing(live) or '<div class=empty>No design is ready yet. A design appears here after Verify passes.</div>']
    if retired:
        delivery_html.append(f'<details class=retired><summary>Declined, kept for the record · {len(retired)}</summary>'
                             f'{listing(retired)}</details>')

    if snapshot.get("csv_url") and any(item.get("ready") for item in live):
        delivery_html.append(f'<div class=mut><a href="{_escape(snapshot["csv_url"])}">↓ This design task\'s designs · '
                             f'{sum(1 for item in live if item.get("ready"))} · csv</a></div>')
    panes = {"goal": goal_html, "design": design_html, "delivery": "".join(delivery_html)}
    def _rel(path) -> str:
        try:
            return str(Path(path).resolve().relative_to(Path(root).resolve()))
        except (TypeError, ValueError):
            return str(path or "")
    page_rel = _rel(snapshot["page"])
    board_rel = _rel(Path(snapshot["insight"].get("design_board") or Path(snapshot["folder"]).parent.parent) / "board.md")
    for key in panes:
        panel = design_runs_panel(key, snapshot["runs"], root=root, page=page_rel, board=board_rel,
                                  whole="this design task")
        panes[key] = f'<div class=space-main>{panes[key]}</div>{panel}'
    panel_css, panel_js = runs_panel_assets()
    tabs = "".join(f'<button type=button data-space="{key}"{" class=on" if key == selected else ""}>{label}</button>'
                   for key, label in (("goal", "Design Task"), ("design", "Design Item"), ("delivery", "Delivery")))
    pane_html = "".join(f'<section class="pane split{" on" if key == selected else ""}" data-space="{key}">{value}</section>'
                        for key, value in panes.items())
    ctx = {"path": str(q.get("path") or ""), "file": str(q.get("file") or "")}
    script = (
        "<script>(function(){var CTX=" + _json(ctx) + ";"
        "var bs=[].slice.call(document.querySelectorAll('.tabs button')),ps=[].slice.call(document.querySelectorAll('.pane'));"
        "function sel(s,w){bs.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});"
        "ps.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});"
        "if(w){var u=new URL(location.href);u.searchParams.set('space',s);history.replaceState({},'',u)}}"
        "bs.forEach(function(b){b.onclick=function(){sel(b.dataset.space,true)}});"
        # a Space's View tabs (Design Task: Aim · Requirements · Resources · Leave out), one shown, kept in the URL
        "function view(v,w){document.querySelectorAll('.views button').forEach(function(x){var box=x.closest('.space-main');"
        "if(!box||!box.querySelector('.view[data-view=\"'+v+'\"]'))return;x.classList.toggle('on',x.dataset.view===v);"
        "box.querySelectorAll('.view').forEach(function(d){d.classList.toggle('on',d.dataset.view===v)})});"
        "if(w){var u=new URL(location.href);u.searchParams.set('view',v);history.replaceState({},'',u)}}"
        "document.querySelectorAll('.views button').forEach(function(x){x.onclick=function(){view(x.dataset.view,true)}});"
        "try{var vw=new URL(location.href).searchParams.get('view');if(vw)view(vw,false)}catch(e){}"
        "var me=document.querySelector('.pane.on .item.sel');if(me)me.scrollIntoView({block:'start'});"
        "document.querySelectorAll('[data-fold]').forEach(function(a){a.onclick=function(e){e.preventDefault();"
        "document.querySelectorAll('details.itemfold').forEach(function(d){d.open=a.dataset.fold==='open'})}});"
        "document.querySelectorAll('button.do').forEach(function(b){b.onclick=function(){"
        "var box=b.closest('[data-item]'),msg=box.querySelector('.msg'),body={path:CTX.path,file:CTX.file,action:b.dataset.action,item:box.dataset.item};"
        "box.querySelectorAll('input,textarea,select').forEach(function(f){if(f.name)body[f.name]=f.value});"
        "msg.className='msg';msg.textContent='writing…';b.disabled=true;"
        "fetch('/_board/design-act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})"
        ".then(function(r){return r.json()}).then(function(j){if(!j.ok){msg.className='msg bad';msg.textContent=j.err||'refused';b.disabled=false;return}"
        "msg.className='msg ok';msg.textContent='written '+(j.run||j.item||'');location.href=j.url})"
        ".catch(function(e){msg.className='msg bad';msg.textContent=String(e);b.disabled=false})}});})();</script>"
    )
    document = (
        '<!doctype html><html lang=en><head><meta charset=utf-8>'
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        f'<title>🎨 Design · {_escape(snapshot["title"])}</title><style>{_CSS}{panel_css}</style></head><body>'
        f'<header>{header}</header><nav class=tabs>{tabs}</nav><main>{pane_html}</main>{script}{panel_js}{design_chat_copy_script()}</body></html>'
    )
    from live.workbench_guide import mount_guide
    return mount_guide(document, "design", ctx, "nav.tabs", "main")


def _json(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def _pick_board_page(root: Path, short: str, boards: list[Path], held: bool) -> bytes:
    """The answer to a short link that names no board and fits several, or none."""
    from urllib.parse import urlencode
    rows = []
    for b in boards:
        rel = b.resolve().relative_to(root.resolve()).as_posix()
        name = renamed_folder(b, short) if held else ""
        href = "/_board/design?" + urlencode({"folder": short, "board": b.name}) if held else \
               "/_board/design-board?" + urlencode({"board": b.name})
        rows.append(f'<li><a href="{_escape(href)}">{_escape(b.name)}</a>'
                    f'{(" · " + _escape(name)) if name else ""} <span class=mut>{_escape(rel)}</span></li>')
    head = (f"<code>{_escape(short)}</code> is on {len(boards)} DesignBoards; pick one, or add <code>&amp;board=</code> to the link:"
            if held else f"No DesignBoard here has a folder <code>{_escape(short)}</code>. The boards:")
    return (f'<!doctype html><meta charset=utf-8><title>🎨 Design · pick a board</title><style>{_CSS}</style>'
            f'<h1>🎨 Design</h1><p>{head}</p><ul>{"".join(rows)}</ul>').encode("utf-8")


def _pick_method_page(root: Path, board: Path, hits: list[str]) -> bytes:
    """The answer to a short link whose task is designed under several methods."""
    from urllib.parse import urlencode
    rel = board.resolve().relative_to(root.resolve()).as_posix()
    path = "/" + ("" if rel == "." else rel + "/") + "board.md"
    rows = "".join(f'<li><a href="{_escape("/_board/design?" + urlencode({"path": path, "file": h}))}">'
                   f'{_escape(h.split("/")[0])}</a> <span class=mut>{_escape(h.split("/")[1])}</span></li>' for h in hits)
    return (f'<!doctype html><meta charset=utf-8><title>🎨 Design · pick a method</title><style>{_CSS}</style>'
            f'<h1>🎨 Design</h1><p>This task is designed by {len(hits)} methods; pick one:</p><ul>{rows}</ul>').encode("utf-8")
