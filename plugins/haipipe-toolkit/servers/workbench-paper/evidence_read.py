"""What a paper's value, citation, display and portal Runs returned, read from their Result files and drawn natively
(stage-2 review round 2, 261106): the Board, a version, an evidence Job and an evidence Task show the same words, drawn
by this one module, so their bars agree.

- Values: a value Task's (or the whole-paper check's) `values.yaml`, each printed number with its state in plain words.
- Citations: a claim group's (or the whole-paper check's) `citations.csv`, each key counted once.
- Portal: the walk's `portal-fields.yaml`, one side tab per portal step.

The pages frame no ledger page any more where a few rows say the same thing (the frame hid its last rows and, at 390
px, its right columns); each row is drawn here and the Run's own page stays one Pop out away. Read-only."""
from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import quote

import yaml

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _side_tabs, plural_word


# a value's state and a key's status in plain words (the Run's codes stay in its own files)
VALUE_WORDS = {"match": "matches its Run", "differs": "differs from its Run", "owed": "waits for its Run",
               "found": "found, not bound yet", "missing": "missing from its Run", "stale": "its Run changed",
               "pending": "waits for its Run", "no anchor": "its sentence moved"}
VALUE_SHORT = {"match": "matches", "differs": "differs", "owed": "waits for its Run", "found": "found, not bound",
               "missing": "missing", "stale": "Run changed", "pending": "waits", "no anchor": "sentence moved"}
CITE_WORDS = {"verified": "verified", "card-only": "source card, not in the bib", "bib-only": "in the bib, no source card",
              "missing-bib": "not in the bib", "TOADD": "to add", "toadd": "to add"}


def is_check(task: Path) -> bool:
    """A whole-paper check Task (t99_*): it reads every other Task of its Job, so it is shown once, as a verdict."""
    return task.name.startswith("t99_")


def check_task(job: Path) -> Path | None:
    return next((t for t in sorted(job.glob("t99_*")) if t.is_dir()), None)


def item_tasks(job: Path) -> list:
    """A Job's Tasks without its whole-paper check, in their number order."""
    return sorted((t for t in job.glob("t[0-9]*_*") if t.is_dir() and not is_check(t)), key=lambda t: t.name)


def newest(task: Path, name: str) -> Path | None:
    """The newest Run's result file `name` of a Task (by Run name, then time), else None."""
    found = list(task.glob(f"runs/*/result/{name}")) if task is not None else []
    return max(found, key=lambda f: (f.parent.parent.name, f.stat().st_mtime)) if found else None


def url(f: Path, root: Path) -> str:
    return "/" + quote(ds._rel(f, root))


def _pop(label: str, f: Path | None, root: Path, name: str = "") -> str:
    return (f'<a class=fd-btn data-pop="{esc(name or label)}" href="{esc(url(f, root))}">{esc(label)}</a>'
            if f is not None and f.is_file() else "")


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


def value_counts(data: dict) -> dict:
    out: dict = {}
    for r in data.get("rows") or []:
        out[r.get("status", "")] = out.get(r.get("status", ""), 0) + 1
    return out


def value_line(data: dict) -> str:
    """The check's count line in plain words, said once: '6 match · 1 differs from its Run · …'."""
    c = value_counts(data)
    bits = [f"{c[k]} {('match' if c[k] != 1 else 'matches') if k == 'match' else VALUE_WORDS.get(k, k)}"
            for k in ("differs", "missing", "stale", "owed", "pending", "found", "no anchor", "match") if c.get(k)]
    never, loose = len(data.get("never_printed") or []), len(data.get("printed_unbound") or [])
    if never:
        bits.append(f"{plural_word(never, 'value', 'values')} never printed")
    if loose:
        bits.append(f"{plural_word(loose, 'printed number', 'printed numbers')} with no binding")
    return " · ".join(bits)


def value_state(data: dict) -> tuple:
    """(word, waiting line) of a set of printed numbers: what differs first, since a person must fix it."""
    rows = data.get("rows") or []
    if not rows:
        return "nothing yet", ""
    c = value_counts(data)
    bad = [r for r in rows if r.get("status") in ("differs", "missing", "stale")]
    if bad:
        r = bad[0]
        what = (f'{r.get("where", "")} prints {r.get("printed", "")}, its Run returned {r.get("value", "")}'
                if r.get("status") == "differs" else f'{r.get("where", "")}: {VALUE_WORDS.get(r.get("status"), r.get("status"))}')
        word = f'{len(bad)} {"differs" if len(bad) == 1 else "differ"}' if all(x.get("status") == "differs" for x in bad) \
            else f"{len(bad)} to fix"
        return word, f"🙋 {plural_word(len(bad), 'printed number', 'printed numbers')} to fix: {what}"
    return f'{c.get("match", 0)} of {len(rows)} match', ""


VALUE_CSS = """<style>.ev-line{margin:0 0 10px;font-size:13.5px}.ev-verdict{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;
margin:0 0 12px;padding:7px 12px;border:1px solid var(--line);border-radius:8px;font-size:13.5px}.ev-verdict b{font-weight:600}
.ev-verdict .fd-btn{margin-left:auto}
.ev-rows{display:grid;gap:6px;margin:0 0 12px}.ev-row{border:1px solid var(--line);border-radius:8px;padding:7px 11px;font-size:13.5px}
.ev-row.bad{border-left:3px solid light-dark(#c92a2a,#ff8787)}.ev-row.wait{border-left:3px solid light-dark(#b35c00,#ffc078)}
.ev-row.ok{border-left:3px solid light-dark(#2b8a3e,#8bd49a)}
.ev-row>b{display:block;font-size:14px;margin:0 0 3px;overflow-wrap:anywhere}
.ev-kv{display:grid;grid-template-columns:110px minmax(0,1fr);gap:2px 10px;margin:0;font-size:13px}
.ev-kv dt{color:var(--muted)}.ev-kv dd{margin:0;overflow-wrap:anywhere}
@media(max-width:600px){.ev-kv{grid-template-columns:1fr;gap:0}.ev-kv dt{margin-top:4px}.ev-verdict .fd-btn{margin-left:0}}</style>"""


def _kv(pairs) -> str:
    return '<dl class=ev-kv>' + "".join(f'<dt>{esc(k)}</dt><dd>{v}</dd>' for k, v in pairs if v) + '</dl>'


def _value_cls(status: str) -> str:
    return "bad" if status in ("differs", "missing", "stale") else "wait" if status in ("owed", "pending", "found", "no anchor") \
        else "ok" if status == "match" else ""


def value_row(r: dict) -> str:
    """One printed number as a card: what it is, where it is printed, printed against returned, its state in words."""
    st = r.get("status", "")
    name = r.get("what") or r.get("key") or r.get("id") or ""          # the value's name; its key on hover (r02)
    key = " · ".join(str(x) for x in (r.get("key"), r.get("id")) if x)
    return (f'<div class="ev-row {_value_cls(st)}"><b title="{esc(key)}">{esc(name)}</b>' + _kv((
        ("State", esc(VALUE_WORDS.get(st, st))), ("Printed in", esc(r.get("where", ""))),
        ("Printed", esc(str(r.get("printed", "")) or "not yet")), ("Its Run", esc(str(r.get("value", "")))),
        ("Bound by", esc({"card": "an evidence card", "map": "the value map"}.get(r.get("bound", ""), r.get("bound", "")))),
        ("Note", esc(r.get("note", ""))))) + '</div>')


def value_check_html(data: dict, task: Path | None, root: Path) -> str:
    """The whole-paper value check, drawn as rows: the count line once, what to fix first, every printed number, then
    the values never printed and the printed numbers with no binding; the Run's own page one Pop out away."""
    rows = data.get("rows") or []
    if not rows:
        return ""
    order = {"differs": 0, "missing": 0, "stale": 0, "owed": 1, "pending": 1, "found": 2, "no anchor": 2, "match": 3}
    shown = sorted(rows, key=lambda r: order.get(r.get("status", ""), 4))
    page = newest(task, "values.html") if task is not None else None
    out = (VALUE_CSS + f'<p class=ev-line>{esc(value_line(data))}</p>'
           + (f'<div class=pb-verbs>{_pop(f"⤢ Open {task.name}{chr(39)}s table", page, root, task.name + " · values")}</div>'
              if page and task is not None else "")
           + '<div class=ev-rows>' + "".join(value_row(r) for r in shown) + '</div>')
    loose = data.get("printed_unbound") or []
    if loose:
        out += ('<p class=pb-state>Printed numbers with no binding</p><div class=ev-rows>' + "".join(
            f'<div class="ev-row wait"><b>{esc(str(u.get("printed", "")))}</b>'
            + _kv((("Printed in", esc(u.get("where", ""))), ("Sentence", esc(u.get("sentence", ""))))) + '</div>' for u in loose) + '</div>')
    never = data.get("never_printed") or []
    if never:
        out += f'<p class=pb-state>Never printed: {esc(", ".join(map(str, never)))}</p>'
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


# ── Citations ──────────────────────────────────────────────────────────────────────────────────────────────────
def cite_rows(task: Path | None) -> list:
    """A claim group's (or the check's) newest citations.csv, one dict per key."""
    f = newest(task, "citations.csv") if task is not None else None
    if f is None:
        return []
    try:
        with f.open(encoding="utf-8", newline="") as fh:
            return [r for r in csv.DictReader(fh) if r.get("key")]
    except Exception:
        return []


def job_cites(job: Path) -> list:
    """Every key a citation Job checks, once: the whole-paper check's rows, else its claim groups' put together."""
    rows = cite_rows(check_task(job))
    if not rows:
        rows = [r for t in item_tasks(job) for r in cite_rows(t)]
    seen, out = set(), []
    for r in rows:
        if r["key"] not in seen:
            seen.add(r["key"])
            out.append(r)
    return out


def cite_state(rows: list) -> tuple:
    """(word, waiting line) of a set of keys, each counted once: how many are verified; a key not in the bib waits."""
    if not rows:
        return "nothing yet", ""
    ok = sum(r.get("status") == "verified" for r in rows)
    missing = [r["key"] for r in rows if r.get("status") in ("missing-bib", "TOADD", "toadd")]
    waits = (f"🙋 {plural_word(len(missing), 'key', 'keys')} not in the bib: {', '.join(missing)}" if missing else "")
    return f"{ok} of {plural_word(len(rows), 'key', 'keys')} verified", waits


def cite_line(rows: list) -> str:
    """The keys' count line in plain words, said once."""
    c: dict = {}
    for r in rows:
        w = CITE_WORDS.get(r.get("status", ""), r.get("status", ""))
        c[w] = c.get(w, 0) + 1
    nodoi = sum(not r.get("doi") for r in rows)
    bits = [f"{n} {w}" for w, n in c.items()] + ([f"{nodoi} without a DOI"] if nodoi else [])
    return " · ".join(bits)


def _cite_cls(status: str) -> str:
    return "ok" if status == "verified" else "bad" if status in ("missing-bib", "TOADD", "toadd") else "wait"


def cite_row(r: dict) -> str:
    """One key as a card that stacks at phone width: its title and year, its status in words, where it is cited, its
    DOI, its signature and its source card."""
    st = r.get("status", "")
    title = " · ".join(x for x in (r.get("title", ""), r.get("year", "")) if x) or "no bib entry yet"
    return (f'<div class="ev-row {_cite_cls(st)}"><b>{esc(r["key"])}</b>' + _kv((
        ("Status", esc(CITE_WORDS.get(st, st))), ("Paper", esc(title)), ("Cited in", esc(r.get("cited_in", ""))),
        ("DOI", esc(r.get("doi", "") or "none")), ("Verified by", esc(verified_by(r.get("verified", "")))),
        ("Source card", esc(r.get("cite_card", "") or "none yet: a Discovery card on the citing sentence")),
        ("Discovery Run", esc(r.get("discovery_runs", ""))))) + '</div>')


def verified_by(said: str) -> str:
    """Who verified a key, in words (r02: "Signed: no signed Result")."""
    return "nobody yet" if not said or said.startswith("no signed") else said


def cite_panel(task: Path, root: Path) -> str:
    """A claim group's keys, each a card (no framed page: it hid Status and DOI at 390 px), the count line once, the
    Run's own page one Pop out away."""
    rows = cite_rows(task)
    if not rows:
        return ""
    page = newest(task, "citations.html")
    return (VALUE_CSS + f'<p class=ev-line>{esc(cite_line(rows))}</p>'
            + (f'<div class=pb-verbs>{_pop(f"⤢ Open {task.name}{chr(39)}s table", page, root, task.name + " · citations")}</div>' if page else "")
            + '<div class=ev-rows>' + "".join(cite_row(r) for r in rows) + '</div>')


def cite_lines(task: Path, root: Path) -> str:
    """A claim group in the Citations view: its claim first, then one line per key (the key and its paper, its status in
    words) and one Open; the cards are the Check view's (r02: the Citations tab drew the same three cards as Check)."""
    from live.board_read import _task_url
    rows = cite_rows(task)
    if not rows:
        return ""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    claim = (re.search(r"(?m)^answers:\s*(.+?)\s*$", text) or [None, ""])[1]
    order = {"missing-bib": 0, "TOADD": 0, "toadd": 0, "bib-only": 1, "card-only": 1, "verified": 2}
    lines = "".join(
        f'<div class=fd-row><span class=n>{esc(r["key"])}</span><span class=d>{esc(r.get("title") or "no bib entry yet")}</span>'
        f'<span class="w {"fd-ok" if r.get("status") == "verified" else "fd-you" if _cite_cls(r.get("status", "")) == "bad" else ""}">'
        f'{esc(CITE_WORDS.get(r.get("status", ""), r.get("status", "")))}</span></div>'
        for r in sorted(rows, key=lambda r: order.get(r.get("status", ""), 3)))
    return (VALUE_CSS + (f'<p class=ev-line><b>Claim</b> · {esc(claim)}</p>' if claim else "") + lines
            + f'<p style="margin-top:10px"><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>')


def cite_key_tabs(rows: list, eid: str) -> str:
    """A claim group's keys, one side tab each (the key; its status in words), its card on the right."""
    if not rows:
        return ""
    order = {"missing-bib": 0, "TOADD": 0, "toadd": 0, "bib-only": 1, "card-only": 1, "verified": 2}
    rows = sorted(rows, key=lambda r: order.get(r.get("status", ""), 3))
    return VALUE_CSS + _side_tabs(eid, [(r["key"], CITE_WORDS.get(r.get("status", ""), r.get("status", ""))) for r in rows],
                                  [cite_row(r) for r in rows])


# ── the whole-paper check, once, as a verdict line on top of the items it checks ───────────────────────────────
def verdict(job: Path, root: Path, kind: str, href: str = "") -> str:
    """One line above a Job's Values or Citations: what the whole-paper check found (its t99 Task), and where to read it.
    `href`: the check's view (the evidence Job's Check view); '' when the line sits in that view."""
    task = check_task(job)
    if task is None:
        return ""
    if kind == "Values":
        data = value_data(task)
        if not data.get("rows"):
            return ""
        word, _ = value_state(data)
        line = value_line(data)
    else:
        rows = cite_rows(task)
        if not rows:
            return ""
        word, _ = cite_state(rows)
        line = cite_line(rows)
    go = f'<a class=fd-btn href="{esc(href)}">Open the check</a>' if href else ""
    said = line if kind == "Values" else f"{word} · {line}"     # a value line already says what differs
    return VALUE_CSS + f'<div class=ev-verdict><span>🔎 <b>The whole-paper check</b>: {esc(said)}</span>{go}</div>'


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
    """(its line, its pill) from what its newest Run returned, so a checked claim group no longer reads "not started"
    beside its own count line: keys verified, numbers that match, a drawn display."""
    from live.board_evidence import evidence_done
    rows = cite_rows(task)
    if rows:
        word, waits = cite_state(rows)
        return word, "waiting for you" if waits else "checked"
    data = value_data(task)
    if data.get("rows"):
        word, waits = value_state(data)
        return word, "waiting for you" if waits else "done"
    if newest(task, "tables.json") is not None:
        return "the raw tables, built", "done"
    st = (status or "").lower()
    return status or "", "done" if evidence_done(status) else "waiting for you" if st.startswith("wait") else "not started"


def where_rows(tasks: list, root: Path, read: dict | None = None) -> list:
    """Each Task as a to-do row: its label, its line, its pill, Open (ui_parts.todo_section's rows)."""
    from live.board_evidence import evidence_body
    from live.board_read import _task_url
    out = []
    for t in tasks:
        label, status, _ = (read or {}).get(t) or evidence_body(t, root)
        line, pill = task_state(t, status)
        out.append((label or t.name, line, pill, "Open", _task_url(t, root), False))
    return out
