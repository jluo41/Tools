"""The Spaces of an insight Board (Scope, the Question Book, Check, Delivery) and the Runs panel beside each."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from .insight_board_reader import (  # noqa: F401 · this module keeps answering these names
    CROSS, _read, _e, _field, _inline)
from .insight_board_parts import _cell_view, _pill, _clip, _tabs, _view, _render_input_data
from .insight_board_runtime import _render_runtime_inventory, groom_snapshot
from .insight_board_studio import _render_studio
from .insight_board_work import (
    page_cells, _STAGE, _part_label, work_runs, page_tickets, _run_url, _pop_url, _answered_by, _behind)


# ─── the Runs panel beside each Space ───────────────────────────────────────

def _runs_panel(space: str, kinds: list[dict]) -> str:
    """Run types on top, the runs of the chosen type below, each with its skill and a
    prompt to copy.  Picking a question narrows the runs to it.  Nothing here starts,
    sends or writes: Copy hands the prompt to a Claude or Codex session."""
    first = max(range(len(kinds)), key=lambda i: len(kinds[i]["rows"])) if kinds else 0
    buttons = "".join(f'<button type=button class="rp-type{" on" if i == first else ""}" data-k="{i}">'
                      f'{_e(k["label"])} <span class=rp-n>{len(k["rows"])}</span></button>' for i, k in enumerate(kinds))
    bodies = []
    for i, k in enumerate(kinds):
        rows = "".join(f'<li data-keys="{_e(" ".join(r.get("keys", [])))}"><a class=pop href="{_e(r["url"])}" data-pop="{_e(r["name"])}">'
                       f'{_e(r["name"])}</a> <span class=mut>{_e(r["status"])}</span></li>' if r.get("url") else
                       f'<li data-keys="{_e(" ".join(r.get("keys", [])))}">{_e(r["name"])} <span class=mut>{_e(r["status"])}</span></li>'
                       for r in k["rows"])
        bodies.append(f'<div class=rp-kind data-k="{i}"{"" if i == first else " hidden"}>'
                      f'<p class=rp-skill>Skill <code>{_e(k["skill"])}</code></p>'
                      f'<div class=rp-prompt><div class=rp-ph>Prompt <button type=button class=rp-copy>Copy</button></div>'
                      f'<pre data-base="{_e(k["prompt"])}">{_e(k["prompt"])}</pre></div>'
                      f'<ul class=rp-runs>{rows}</ul><p class=rp-empty{"" if not k["rows"] else " hidden"}>No runs yet.</p></div>')
    # Folded to a thin strip by default, like the Paper and Page workbenches; the
    # person's choice is remembered per Space (runs hidden until wanted).
    return (f'<aside class="rp folded" data-space="{_e(space)}"><div class=rp-head>'
            f'<button type=button class=rp-fold title="Open or fold the runs">◂</button><b>Runs</b> '
            f'<span class="rp-for mut"></span></div>'
            f'<div class=rp-body><div class=rp-types>{buttons}</div>{"".join(bodies)}</div></aside>')


def _resting(snap: dict) -> dict[tuple[str, str], set[str]]:
    """(segment, lower question) -> the Knowledge and Wisdom answers that rest on it,
    so picking a K or W question shows the runs behind its answer."""
    if "resting" in snap:
        return snap["resting"]
    answered, out = _answered_by(snap), {}
    for q in snap["questions"]:
        if q["id"][1] not in "KW":
            continue
        for pid, cell in q["cells"].items():
            for lower in _behind(snap, snap["by_id"].get(cell.get("page", "")), answered):
                out.setdefault((pid, lower), set()).add(q["id"])
    snap["resting"] = out
    return out


def _run_rows(snap: dict, level: str) -> list[dict]:
    resting = _resting(snap)
    called: dict[int, set[str]] = {}          # run -> the cells whose page tickets call it
    for page in snap["pages"]:
        cells = [(q, p) for q, p in page_cells(snap, page) if q[1] == level]
        for r in page_tickets(snap, page) if cells else []:
            called.setdefault(id(r), set()).update(f"{p}:{q}" for q, p in cells)
    out = []
    for r in work_runs(snap):
        mine = [a for a in r["answers"] if a[1] == level]
        if mine or id(r) in called:
            where = r["partition"] or CROSS
            keys = {f"{w}:{a}" for a in mine for w in (where, CROSS)} | called.get(id(r), set())
            keys |= {f"{w}:{up}" for a in mine for w in (where, CROSS) for up in resting.get((w, a), ())}
            out.append({"name": f'{r["task"]} · {r["call"]}', "status": r["status"], "url": _run_url(snap, r),
                        "keys": sorted(keys)})
    return out


def _report_rows(snap: dict) -> list[dict]:
    """Every report file on the board, keyed to its question and segment."""
    if "report_rows" in snap:               # an Instance: each run's generated report (instance_reader)
        return snap["report_rows"]
    names = {p["name"]: p["id"] for p in snap["partitions"]}
    out = []
    for path in sorted((snap["board"] / "reports").glob("*/Q[DIKW]*.md")):
        pid = names.get(path.parent.name, path.parent.name)
        out.append({"name": f"{path.stem} · {_part_label(snap, pid)}", "status": _field(_read(path), "strength") or "written",
                    "url": f"/_board/insight?board={quote(snap['board'].name)}&report={quote(pid + ':' + path.stem)}",
                    "keys": [f"{pid}:{path.stem}"]})
    return out


def _space_kinds(snap: dict) -> dict[str, list[dict]]:
    rel = snap["relative"]
    return {
        # the Question Book's runs, in the order the method takes them (ref/workbench-table.md)
        "prototype": [
            {"label": "Carry a board over", "skill": "hai-insight", "rows": [],
             "prompt": f"/hai-insight carry a register board over into this board's Question Book ({rel})."},
            {"label": "Register a segment", "skill": "hai-insight-partition (new)", "rows": [],
             "prompt": f"/hai-insight add a segment to the Question Book's 0-Meta/partitions.md, with its filter and why ({rel})."},
            {"label": "Review the questions", "skill": "hai-report", "rows": [],
             "prompt": f"/hai-insight review the Question Book's questions by Q1-Q7 and propose keep, split, merge or move ({rel})."},
            {"label": "Plan the evidence", "skill": "hai-insight-evidence-plan", "rows": [],
             "prompt": f"/hai-insight-evidence-plan {{question}}: write its needs, each with a full work spec ({rel})."},
            {"label": "Write the script", "skill": "hai-insight", "rows": [],
             "prompt": f"/hai-insight write the Question Book script for {{question}} from its live needs ({rel})."},
            {"label": "Review the script", "skill": "hai-insight", "rows": [],
             "prompt": f"/hai-insight review the script of {{question}}: an agent that did not write it ({rel})."},
            {"label": "Draw the question map", "skill": "hai-insight", "rows": [],
             "prompt": "/hai-insight redraw the Question Book's question map: run ref/question_map.py on the "
                       "Question Book board; it writes studio/question-map.excalidraw, never edited by hand."},
        ],
        "scope": [
            {"label": "Prepare extract", "skill": "hai-task", "rows": [],
             "prompt": f"/hai-task: prepare the extract this board reads; MT00 records it ({rel})."},
            {"label": "Ask", "skill": "hai-insight-question", "rows": [],
             "prompt": f'/hai-insight application {rel} question "<your question>"'},
            # Add a method and Add a paper are Guide runs now (ref/workbench-table.md): the method
            # library is the family's, shared by every board, not this board's data.
        ],
        "insight": [
            {"label": "Data runs", "skill": "hai-task", "rows": _run_rows(snap, "D"),
             "prompt": "/hai-task: run the task call that answers {question} on {partition}; its config lists it under answers:."},
            {"label": "Information runs", "skill": "hai-task", "rows": _run_rows(snap, "I"),
             "prompt": "/hai-task: run the task call that answers {question} on {partition}; its config lists it under answers:."},
            {"label": "Report", "skill": "hai-insight-data · -information · -knowledge · -wisdom",
             "rows": _report_rows(snap),
             "prompt": f"/hai-insight application {rel} report {{question}} {{partition}}: read the runs that "
                       "answer it and write reports/<segment>/<question>.md (headline, answer, strength, limit, runs)."},
            {"label": "Pool or split", "skill": "hai-insight-workflow", "rows": [],
             "prompt": f"/hai-insight application {rel} verdict"},
        ],
        "check": [
            {"label": "Mechanical check", "skill": "cli/check.py", "rows": [],
             "prompt": f"/hai-insight application {rel} check"},
            {"label": "Answer review", "skill": "hai-draft-review", "rows": [],
             "prompt": f"/hai-insight application {rel} review {{question}} {{partition}}"},
        ],
        "delivery": [
            {"label": "Handoff draft", "skill": "hai-insight-wisdom", "rows": [],
             "prompt": f"/hai-insight application {rel} handoff {{question}} {{partition}}"},
        ],
    }


# ─── the Spaces ─────────────────────────────────────────────────────────────
def _render_scope(snap: dict) -> str:
    prow = "".join(
        f'<tr><td><b>{_e(_part_label(snap, r["id"]))}</b></td><td class=mono>{_e(r["where"] or ("no rows of its own" if r["id"] == CROSS else "—"))}</td>'
        f'<td class=num>{_e(r["rows"] or "—")}</td><td class=num>{_e(r["share"] or "—")}</td>'
        f'<td class=mono>{_e((r.get("config") or "—") + (".yaml" if r.get("config") else ""))}</td></tr>'
        for r in snap["partitions"])
    partitions = ('<h2>Segments</h2><p class=lead>Segments of this one extract, from MT00. A segment is one config per task, never a second dataset.</p>'
                  f'<div class=scroll><table><tr><th>Segment</th><th>Where</th><th>Rows</th><th>Share</th><th>Config</th></tr>{prow}</table></div>')
    counts = "".join(f'<li>{_e(_STAGE[lv])} questions <span class=mut>{sum(q["id"][1] == lv for q in snap["questions"])}</span></li>'
                     for lv in "DIKW")
    ask = ('<h2>Questions</h2><ul class=counts>' + counts + '</ul>'
           '<p class=lead>Type the question. Claude Code decides its level, the segments it runs on and what it grows out of, then registers it. It never answers it here.</p>'
           f'<form id=askform class=form data-root="{_e(snap["relative"])}">'
           '<div class="field full"><textarea id=ask-text required placeholder="e.g. does the send hour change which message works best?"></textarea></div>'
           '<div class="full actions"><button class="btn primary" type=submit>Ask</button><span class=status id=ask-status></span></div></form>'
           '<div id=ask-out hidden><p class=mut>Give this to Claude Code (copied to your clipboard):</p><p><code id=ask-cmd></code></p></div>')
    # Scope is this board's own data to understand; the Question Book has its own Space now,
    # and the family's methods and papers are the shared Guide's.
    return (_tabs([("dataset", "Dataset"), ("partitions", "Partitions"), ("questions", "Questions")])
            + _view("dataset", _render_input_data(snap), True) + _view("partitions", partitions)
            + _view("questions", ask))


def _render_prototype_space(snap: dict) -> str:
    """Question Book: Meta, Data, Information, Knowledge, Wisdom (instance_reader.prototype_views)."""
    if not snap.get("prototype"):
        return '<p class=note>This board is made the register way, without a Question Book.</p>'
    from .instance_reader import prototype_views
    views = prototype_views(snap["board"], Path(snap["root"]))
    views = views + [("roadmap", "RoadMap Draw", _render_studio(snap))]
    return _tabs([(k, label) for k, label, _ in views]) + "".join(
        _view(k, body, i == 0) for i, (k, _, body) in enumerate(views))


def _gate_label(key: str) -> str:
    """A gate as the screen names it: GI0 -> Gate-I0. The id stays GI0
    in records, receipts and skills; only the label changes, and the id is the cell's tooltip."""
    return "Gate-" + key[1:] if len(key) > 1 and key[0] == "G" else key


def _gate_blocks(snap: dict) -> str:
    """The seven gates of every answered cell; the picked question shows its own."""
    out = []
    for q in snap["questions"]:
        for pid, cell in q["cells"].items():
            if cell["mark"] == "·" or (cell["mark"] == "🚫" and not cell["page"]):
                continue
            view = _cell_view(snap, q["id"], pid)
            out.append(f'<div class=gateset data-key="{_e(pid)}:{_e(q["id"])}" hidden>'
                       f'<p class=mut>{_e(_STAGE[q["id"][1]])} question {_e(q["id"][2:])} · {_e(_part_label(snap, pid))}</p><div class=gates>'
                       + "".join(f'<div class="gate {g["state"]}" title="{_e(g["key"])}"><span class=k>{_e(_gate_label(g["key"]))}</span><span class=n>{_e(g["name"])}</span>'
                                 f'<span class=who><span class="pill {"human" if g["who"] == "person" else "acc" if g["who"] == "agent" else ""}">'
                                 f'{_e(g["who"])}</span> {_e(g["state"])}</span>'
                                 f'{("<span class=n>" + _e(_clip(g["note"], 90)) + "</span>") if g["note"] else ""}</div>'
                                 for g in view["gates"]) + '</div></div>')
    return ('<h2>Gates</h2><p class=lead>Pick a question in Insight; its gates show here. A gate is closed by its owner, never by this screen.</p>'
            + "".join(out) + '<p class="note gate-none">The picked question has no gates on this segment.</p>')


def _render_check(snap: dict) -> str:
    groom = groom_snapshot(snap["board"], snap)
    crow = "".join(
        f'<tr><td>{_pill("🚫" if c["level"] == "FAIL" else "🟡" if c["level"] == "WARN" else "✅", c["level"])}</td>'
        f'<td class=mono>{_e(c["where"])}</td><td>{_inline(c["message"])}</td></tr>' for c in groom["checks"])
    mech = f'<h2>Checks</h2><p class=lead>From <code>cli/check.py</code>, whole board.</p><table><tr><th>Level</th><th>Where</th><th>Finding</th></tr>{crow}</table>'
    return (_tabs([("gates", "Gates"), ("checks", "Checks"), ("runtime", "Runtime")])
            + _view("gates", _gate_blocks(snap), True) + _view("checks", mech)
            + _view("runtime", _render_runtime_inventory(snap)))


def _render_delivery(snap: dict) -> str:
    """What leaves this board: person-signed Wisdom answers a DesignBoard may use."""
    hrows = "".join(
        f'<tr><td><a class=pop href="{_e(_pop_url(snap, h["record"]))}" data-pop="{_e(h["title"])}">{_e(h["title"])}</a></td>'
        f'<td class=mono>{_e(h["serves"])}</td>'
        f'<td>{_pill("✅" if h["bindable"] else "🟡", h["eligibility"])} · {_e(h["eligibility_reason"])}</td></tr>'
        for h in snap["handoffs"]) or '<tr><td colspan=3 class=mut>No Wisdom answer is ready to leave this board yet.</td></tr>'
    ready = sum(h["bindable"] for h in snap["handoffs"])
    return (_tabs([("handoff", "Handoff")])
            + _view("handoff", f'<h2>Handoff</h2><p class=lead>{ready} signed Wisdom answer{"" if ready == 1 else "s"} ready for design. '
                    'Only a signed, current handoff leaves this board.</p>'
                    f'<table><tr><th>Wisdom answer</th><th>Serves</th><th>Current eligibility</th></tr>{hrows}</table>', True))
