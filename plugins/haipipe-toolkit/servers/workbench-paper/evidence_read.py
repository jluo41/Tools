"""What a paper's value, citation, display and portal Runs returned, read from their Result files and drawn natively
(stage-2 review round 2, 261106): the Board, a version, an evidence Job and an evidence Task show the same words, drawn
by this one module, so their bars agree.

- Values: a value Task's (or the whole-paper check's) `values.yaml`, each printed number with its state in plain words.
- Citations: a claim group's (or the whole-paper check's) `citations.csv`, each key counted once.
- Portal: the walk's `portal-fields.yaml`, one side tab per portal step.

The pages frame no ledger page any more where a few rows say the same thing (the frame hid its last rows and, at 390
px, its right columns); each row is drawn here and the Run's own page stays one Pop out away. Read-only."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from live.frame import esc
from live.ui_parts import _side_tabs, plural_word
from live.evidence_common import (CITE_WORDS, VALUE_CSS, _kv, _pop, check_task, is_check, item_tasks,  # noqa: F401
                                  newest, url)
from live.evidence_cite import (cite_rows, job_cites, cite_state, cite_waits, _cite_cls, cite_row, verified_by,
                                cite_panel, bib_entries, abstract_bank, _field, reference, abstract_html,
                                citing_sentences, key_detail, cite_lines, cite_key_tabs, _ENTRY, CK_CSS, _PART,
                                _CITE_CMD)  # noqa: F401


# a value's state and a key's status in plain words (the Run's codes stay in its own files)
VALUE_WORDS = {"match": "matches its Run", "differs": "differs from its Run", "owed": "waits for its Run",
               "found": "found, not bound yet", "missing": "missing from its Run", "stale": "its Run changed",
               "pending": "waits for its Run", "no anchor": "its sentence moved"}
VALUE_SHORT = {"match": "matches", "differs": "differs", "owed": "waits for its Run", "found": "found, not bound",
               "missing": "missing", "stale": "Run changed", "pending": "waits", "no anchor": "sentence moved"}


# ── Values ─────────────────────────────────────────────────────────────────────────────────────────────────────
def value_data(task: Path | None) -> dict:
    """A value Task's or check's newest `values.yaml` (values_ledger.py) as one shape: `rows` (one per printed place:
    where, printed, value, status, key, what, bound, note), `never_printed`, `printed_unbound`. The check writes rows;
    a value Task writes its values, each with the places it is printed, and the values it still owes (`needs`)."""
    f = newest(task, "values.yaml") if task is not None else None
    try:
        data = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}) if f else {}
    except Exception:
        return {}
    if isinstance(data.get("values"), list) and not data.get("rows"):   # a ledger Run: one row per printed place
        rows = [dict(v, run=v.get("source", "")) for v in data["values"] if isinstance(v, dict)]
        return {**data, "rows": rows, "board": task.parent.parent}
    if data.get("rows") or not isinstance(data.get("values"), dict):
        return _named(data, task.parent) if data.get("rows") else data
    rows = []
    for key, v in data["values"].items():
        for at in v.get("printed") or []:
            rows.append({"where": at.get("where", ""), "printed": at.get("printed", ""), "status": at.get("status", ""),
                         "bound": at.get("bound", ""), "note": at.get("note", ""), "value": v.get("shown") or v.get("value", ""),
                         "key": key, "id": v.get("id", ""), "what": v.get("what", "")})
    for key, n in (data.get("needs") or {}).items():
        rows.append({"where": " ".join(x for x in (n.get("section", ""), n.get("sentence", "")) if x), "printed": n.get("printed", ""),
                     "status": "owed", "bound": "map", "note": n.get("why", ""), "value": "", "key": key, "what": n.get("what", "")})
    return {**data, "rows": rows}


def value_names(job: Path) -> dict:
    """{value key: its name} of a value Job, from each value Task's newest values.yaml, else its value map: the words a
    page shows for a value (r02: check cards and table rows were headed by keys, sub.b, main.ci_lo)."""
    out = {}
    for t in item_tasks(job) if job is not None and job.is_dir() else []:
        for f in (newest(t, "values.yaml"), t / "scripts" / "value_map.yaml"):
            try:
                vals = (yaml.safe_load(f.read_text(encoding="utf-8")) or {}).get("values") if f is not None and f.is_file() else None
            except Exception:
                vals = None
            for k, v in (vals or {}).items() if isinstance(vals, dict) else []:
                if isinstance(v, dict) and v.get("what"):
                    out.setdefault(k, str(v["what"]))
    return out


def _named(data: dict, job: Path | None) -> dict:
    """The rows of a check, each with its value's name (`what`) when the check left it out."""
    rows = data.get("rows") or []
    if not rows or all(r.get("what") for r in rows) or job is None:
        return data
    names = value_names(job)
    return {**data, "rows": [r if r.get("what") else {**r, "what": names.get(r.get("key", ""), "")} for r in rows]}


def key_states(job: Path) -> dict:
    """{value key: (its worst state, what the paper prints for it)} from the value check: the Values table's Status and
    As printed cells agree with the bar (r03: the table said "current" for the one value the bar said differs)."""
    order = {"differs": 0, "missing": 0, "stale": 0, "owed": 1, "pending": 1, "found": 2, "no anchor": 2, "match": 3}
    out = {}
    for r in job_values(job).get("rows") or []:
        k, st = r.get("key", ""), r.get("status", "")
        if k and (k not in out or order.get(st, 4) < order.get(out[k][0], 4)):
            out[k] = (st, str(r.get("printed", "")))
    return out


def job_values(job: Path) -> dict:
    """A value Job's check: the whole-paper check's values.yaml, else its Tasks' rows put together."""
    data = value_data(check_task(job))
    if data.get("rows"):
        return _named(data, job)
    rows, never, unbound = [], [], []
    for t in item_tasks(job):
        d = value_data(t)
        rows += d.get("rows") or []
        never += d.get("never_printed") or []
        unbound += d.get("printed_unbound") or []
    return {"rows": rows, "never_printed": never, "printed_unbound": unbound} if rows else {}



def value_state(data: dict) -> tuple:
    """(word, waiting line) of a set of printed numbers: none. A page carries no check tally ("6 to fix", "41 of 70
    match", "🙋 6 printed numbers to fix: …"); each printed number's own row shows its state where it lands (AGENTS
    § Page words). The counts stay in the check's own receipt. Kept so callers still unpack a pair."""
    return "", ""


def value_waits(data: dict) -> bool:
    """Does a printed number wait on the person (differs, missing, stale)? For a to-do row's pill, never a count."""
    return any(r.get("status") in ("differs", "missing", "stale") for r in data.get("rows") or [])


def _value_cls(status: str) -> str:
    return "bad" if status in ("differs", "missing", "stale") else "wait" if status in ("owed", "pending", "found", "no anchor") \
        else "ok" if status == "match" else ""


def sentence_at(board: Path | None, where: str) -> tuple:
    """(Section, S-id, sentence) of a place like 't05_results S14', read from the Section's newest Draft; empty when
    it cannot be found. Shared by the Values and Citations views."""
    sec, _, sid = (where or "").strip().partition(" ")
    if board is None or not sec or not sid:
        return ("", "", "")
    drafts = sorted(board.glob(f"j*/{sec}/draft/{sec}-draft-v*.md"), key=lambda f: f.stat().st_mtime)
    if not drafts:
        return (sec, sid, "")
    hits = re.findall(r"(?m)^- B\d+ · " + re.escape(sid.split()[0]) + r" · (.+)$",
                      drafts[-1].read_text(encoding="utf-8", errors="ignore"))
    text = re.sub(r"\s{2,}", " ", _CITE_CMD.sub("", hits[-1])).strip() if hits else ""
    return (sec, sid, re.sub(r"\s+([.,;])", r"\1", text))


def value_row(r: dict, board: Path | None = None) -> str:
    """One printed number, opened like a citation key (JL 261110: "for the values, you should update it as well"): its
    name, the number as printed and its state on the closed line; open, the sentence that prints it (the number in
    bold), the value its Run returned, the Run and key it reads, and any note."""
    st = r.get("status", "")
    name = r.get("what") or r.get("key") or r.get("id") or ""
    printed = str(r.get("printed", "") or "")
    word = VALUE_WORDS.get(st, st)
    if st == "no anchor" and not printed:         # the sentence rests on the value but prints no number of it
        word = "backs its sentence, no number printed"
    cls = "fd-ok" if st == "match" else "fd-you" if _value_cls(st) == "bad" else ""
    sec, sid, sent = sentence_at(board, r.get("where", ""))
    if sent and printed and printed in sent:
        shown = esc(sent).replace(esc(printed), f"<b class=vk>{esc(printed)}</b>", 1)
    else:
        shown = esc(sent)
    body = []
    if r.get("where"):
        body.append("<h5>Where it is printed</h5>" + (f'<p class=ck-cite>{shown} <span class=src>{esc(r["where"])}</span></p>'
                                                      if sent else f'<p>{esc(r["where"])}</p>'))
    run, key = r.get("run") or r.get("source") or "", r.get("key", "")
    body.append("<h5>What it is checked against</h5><p>" + " · ".join(x for x in (
        f"returned value <b>{esc(str(r.get('value', '')))}</b>" if r.get("value", "") != "" else "no returned value yet",
        f"Run {esc(run)}" if run else "", f"key <code>{esc(key)}</code>" if key else "") if x) + "</p>")
    if r.get("note"):
        body.append(f"<h5>Note</h5><p>{esc(r['note'])}</p>")
    return (f'<details class=ck><summary class=fd-row><span class=n>{esc(printed or "—")}</span><span class=d>{esc(name)}</span>'
            f'<span class="w {cls}">{esc(word)}</span></summary><div class=ck-body>' + "".join(body) + '</div></details>')


def value_check_html(data: dict, task: Path | None, root: Path) -> str:
    """The whole-paper value check, drawn as rows: what to fix first, every printed number, then
    the values never printed and the printed numbers with no binding; the Run's own page one Pop out away."""
    rows = data.get("rows") or []
    if not rows:
        return ""
    order = {"differs": 0, "missing": 0, "stale": 0, "owed": 1, "pending": 1, "found": 2, "no anchor": 2, "match": 3}
    shown = sorted(rows, key=lambda r: order.get(r.get("status", ""), 4))
    page = newest(task, "values.html") if task is not None else None
    out = (VALUE_CSS
           + (f'<div class=pb-verbs>{_pop(f"⤢ Open {task.name}{chr(39)}s table", page, root, task.name + " · values")}</div>'
              if page and task is not None else "")
           + CK_CSS + "<style>b.vk{background:var(--hl,#fff3bf);padding:0 2px}</style>"
           + "".join(value_row(r, data.get("board")) for r in shown))
    loose = data.get("printed_unbound") or []
    if loose:
        out += ('<p class=pb-state>Printed numbers with no binding</p><div class=ev-rows>' + "".join(
            f'<div class="ev-row wait"><b>{esc(str(u.get("printed", "")))}</b>'
            + _kv((("Printed in", esc(u.get("where", ""))), ("Sentence", esc(u.get("sentence", ""))))) + '</div>' for u in loose) + '</div>')
    never = data.get("never_printed") or []
    if never:
        out += f'<p class=pb-state>Never printed: {esc(", ".join(map(str, never)))}</p>'   # names, not a count
    return out


def value_tabs_per_value(data: dict, eid: str) -> str:
    """A value Task's numbers, one side tab per value (its number and what it is; its state word: the worst of the places
    it is printed), each place it is printed as a card on the right: what a person reads first on the Task's page."""
    rows = data.get("rows") or []
    if not rows:
        return ""
    order = {"differs": 0, "missing": 0, "stale": 0, "owed": 1, "pending": 1, "found": 2, "no anchor": 2, "match": 3}
    by: dict = {}
    for r in rows:
        by.setdefault(r.get("key") or r.get("id") or r.get("printed", ""), []).append(r)
    keys = sorted(by, key=lambda k: min(order.get(r.get("status", ""), 4) for r in by[k]))
    items, panels = [], []
    for k in keys:
        places = sorted(by[k], key=lambda r: order.get(r.get("status", ""), 4))
        worst = places[0].get("status", "")
        first = places[0]
        items.append((f'{first.get("what") or k} · {first.get("value") or first.get("printed") or "—"}',
                      VALUE_SHORT.get(worst, worst) + (f" · {len(places)} places" if len(places) > 1 else "")))
        panels.append('<div class=ev-rows>' + "".join(value_row(r) for r in places) + '</div>')
    return VALUE_CSS + _side_tabs(eid, items, panels)


# ── the whole-paper check, once, as a verdict line on top of the items it checks ───────────────────────────────
def verdict(job: Path, root: Path, kind: str, href: str = "") -> str:
    """One line above a Job's Values or Citations: what the whole-paper check found (its t99 Task), and where to read it.
    `href`: the check's view (the evidence Job's Check view); '' when the line sits in that view."""
    task = check_task(job)
    if task is None:
        return ""
    if not (value_data(task) if kind == "Values" else {"rows": cite_rows(task)}).get("rows"):
        return ""
    # no count line (AGENTS § Page words): what it found shows on each number or key below; the line only leads there
    go = f'<a class=fd-btn href="{esc(href)}">Open the check</a>' if href else ""
    return VALUE_CSS + f'<div class=ev-verdict><span>🔎 <b>The whole-paper check</b></span>{go}</div>'


# ── Portal ─────────────────────────────────────────────────────────────────────────────────────────────────────
def portal_fields(task: Path) -> dict:
    f = newest(task, "portal-fields.yaml")
    try:
        return (yaml.safe_load(f.read_text(encoding="utf-8")) or {}) if f else {}
    except Exception:
        return {}


def portal_tabs(data: dict, eid: str) -> str:
    """The portal's steps, one side tab each (its name; how many fields, how many required), a row per field on the
    right: its label, whether it is required, what the draft holds now and what the portal says about it."""
    steps = data.get("steps") or []
    if not steps:
        return ""
    items, panels = [], []
    for s in steps:
        fields = s.get("fields") or []
        req = sum(bool(x.get("required")) for x in fields)
        items.append((re.sub(r"^\d+\s+", "", str(s.get("step", ""))), f"{plural_word(len(fields), 'field', 'fields')}, {req} required"))
        # one row per field, the portal's own words on hover (r02: a four-row card per field)
        panels.append("".join(
            f'<div class=fd-row title="{esc(x.get("says", "") or x.get("kind", ""))}"><span class=n>{esc(x.get("label", ""))}</span>'
            f'<span class=d>{esc(str(x.get("now", "")) or "empty in the draft")}</span>'
            f'<span class="w {"fd-you" if x.get("required") and not x.get("now") else ""}">'
            f'{"required" if x.get("required") else "optional"}</span></div>' for x in fields))
    return VALUE_CSS + _side_tabs(eid, items, panels)


# ── where each evidence Task stands, one to-do row each (a version's and an evidence Job's ⚙️ Process) ──────────
def task_state(task: Path, status: str = "") -> tuple:
    """(its line, its pill) from what its newest Run returned, so a checked claim group no longer reads "not started";
    no count in the line (each key and number shows its own state on its page)."""
    from live.board_evidence import evidence_done
    rows = cite_rows(task)
    if rows:
        return "", "waiting for you" if cite_waits(rows) else "checked"
    data = value_data(task)
    if data.get("rows"):
        return "", "waiting for you" if value_waits(data) else "done"
    if newest(task, "tables.json") is not None:
        return "the raw tables, built", "done"
    st = (status or "").lower()
    return status or "", "done" if evidence_done(status) else "waiting for you" if st.startswith("wait") else "not started"


