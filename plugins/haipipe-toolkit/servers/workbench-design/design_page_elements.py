"""The design's elements: each draft split against the starting text, the designer's own
element record, and the element matrix across the page's designs.

Split out of design_page.py; design_page.py re-exports every name here."""
from __future__ import annotations

import difflib
import re

from live.design import _escape, _read, _yaml, design_number, shown_design, with_link, yaml
from live.design_page_chain import _level


# ------------------------------------------------------------ design elements --

_SLOT_TOKEN = re.compile(r"^\{[A-Z]+\}$")
_ABBREV = {"dr.", "mr.", "mrs.", "ms.", "st.", "jr.", "sr.", "e.g.", "i.e."}


def _norm(token: str) -> str:
    return token.lower().strip(".,:;!?\"'“”‘’")


def design_elements(base: str, text: str, opt_out: str = "") -> list[dict]:
    """The design split into its elements against the starting text: one per
    sentence, clause or slot of the design, [{kind, parts: [(kind, words)]}]. An element is
    kept (the starting text's own words), new, removed, goal (a slot such as {LINK}, or the
    opt-out, that the design goal requires) or changed. A sentence is cut into its kept and
    new parts only when every part has three words or more; otherwise it stays whole,
    `changed`, with its new and removed words marked inside it."""
    a, b = base.split(), with_link(text.strip()).split()
    match = difflib.SequenceMatcher(None, [_norm(t) for t in a], [_norm(t) for t in b], autojunk=False)
    stream = []
    for op, i1, i2, j1, j2 in match.get_opcodes():
        stream += ([(t, "kept") for t in b[j1:j2]] if op == "equal"
                   else [(t, "removed") for t in a[i1:i2]] + [(t, "new") for t in b[j1:j2]])
    sentences, cur = [], []
    for tok, kind in stream:
        if kind != "removed" and _SLOT_TOKEN.match(tok):
            sentences += ([cur] if cur else []) + [[(tok, kind)]]
            cur = []
            continue
        cur.append((tok, kind))
        if kind != "removed" and re.search(r"[.:!?]$", tok) and tok.lower() not in _ABBREV:
            sentences.append(cur)
            cur = []
    sentences += [cur] if cur else []
    out = []
    for sentence in sentences:
        runs: list[tuple[str, list[str]]] = []
        for tok, kind in sentence:
            if runs and runs[-1][0] == kind:
                runs[-1][1].append(tok)
            else:
                runs.append((kind, [tok]))
        if len(runs) == 1 or all(len(toks) >= 3 for _, toks in runs):
            for kind, toks in runs:
                words = " ".join(toks)
                goal = kind == "new" and (_SLOT_TOKEN.match(words) or (opt_out and words == opt_out))
                out.append({"kind": "goal" if goal else kind, "parts": [(kind, words)]})
        else:
            out.append({"kind": "changed", "parts": [(kind, " ".join(toks)) for kind, toks in runs]})
    return out


def _ids(rows: list[dict]) -> str:
    """Row ids for the Support column; with their page when the rows sit on more than one."""
    pages = {r["pid"] for r in rows}
    return " · ".join(r["id"] if len(pages) == 1 else f'{r["pid"]} · {r["id"]}' for r in rows)


_FROM = {"requirements": "requirements", "internal": "internal insight", "external": "external insight",
         "intuition": "intuition"}


def element_record(item: dict) -> list[dict]:
    """The designer's own element record for the shown draft: `elements.yaml`, named in its result.yaml as
    `elements`, one entry per element with its words, where it came from, the rule, row or
    theory it rests on, and whether it was reasoned or intuitive. Empty when there is none."""
    shown = shown_design(item)
    run = next((r for r in item.get("runs") or [] if shown and r["id"] == shown.get("run")), None)
    if run is None or yaml is None:
        return []
    ref = _yaml(run["result_dir"] / "result.yaml").get("elements")
    path = run["result_dir"] / str(ref.get("path")) if isinstance(ref, dict) and ref.get("path") else None
    if path is None or not path.is_file():
        return []
    try:
        data = yaml.safe_load(_read(path))
    except yaml.YAMLError:
        return []
    return [e for e in data if isinstance(e, dict)] if isinstance(data, list) else []


def _record_html(record: list[dict]) -> str:
    """The element record as the designer wrote it: words, where each came from, how it was chosen."""
    rows = []
    for e in record:
        frm = str(e.get("from") or "").strip().lower()
        how = str(e.get("thinking") or "").strip().lower()
        src = str(e.get("source") or "").strip()
        why = str(e.get("because") or "").strip()
        alts = e.get("alternatives") if isinstance(e.get("alternatives"), list) else []
        role = str(e.get("element") or "").strip()
        rows.append(
            f'<tr><td>{f"<span class=ids>{_escape(role)}</span>" if role else ""}{_escape(str(e.get("words") or ""))}</td>'
            f'<td class=elsup><span class="el-from {_escape(frm)}">{_escape(_FROM.get(frm, frm or "not said"))}</span>'
            f'{f" · <span class=el-how>{_escape(how)}</span>" if how else ""}'
            f'{f"<span class=ids>{_escape(src)}</span>" if src and src.lower() != "none" else ""}'
            f'{f"<span class=ids>because {_escape(why)}</span>" if why else ""}'
            f'{"<span class=ids>weighed: " + _escape(" · ".join(map(str, alts))) + "</span>" if alts else ""}</td></tr>')
    reasoned = sum(str(e.get("thinking") or "").lower() == "reasoned" for e in record)
    intuitive = sum(str(e.get("thinking") or "").lower() == "intuitive" for e in record)
    return ('<div class=mut>As the designer recorded it: where each element came from, and whether it was '
            f'reasoned (System 2) or intuitive (System 1). {reasoned} reasoned · {intuitive} intuitive.</div>'
            f'<table class=elems><tr><th>Element</th><th>From · how</th></tr>{"".join(rows)}</table>')


def _elements_html(item: dict, goal: dict, ev: dict) -> tuple[str, str]:
    """(summary, body) of the Design elements fold: each element of the design and what supports it.

    A kept element rests on the chain when the design follows the evidence (stance follow);
    otherwise it is the starting text as sent. A new, removed or changed element is licensed
    by the named rows when the design explores; a design that follows the evidence has no
    row for its change, and its limits are said beside it."""
    shown = shown_design(item)
    base = (goal or {}).get("starting text", "")
    if not shown or not (shown.get("text") or "").strip():
        return "after the first draft", '<div class=mut>Shown once a draft exists, element by element against the starting text.</div>'
    if not base:
        record = element_record(item)          # the designer's own record needs no starting text
        return (f"{len(record)} recorded" if record else "no starting text"), (_record_html(record) if record else "") + (
            '<div class=mut>The design goal names no starting text '
            '(<code>Starting text:</code> under Resources), so the elements cannot be compared.</div>')
    quoted = re.search(r'"([^"]+)"', (goal or {}).get("opt-out", ""))
    opt_out = quoted.group(1) if quoted else ""
    elements = design_elements(base, shown["text"], opt_out)
    follow, backing = item.get("stance") == "follow", ev["backing"]
    measured = [n["id"] for c in ev["chains"] for n in c if _level(n["pid"]) == "I" and n["id"]][:1]
    if follow:
        change = "none" + "".join(f" · {h['id']}" for h in ev["limits"])
    else:
        change = ("licensed · " + _ids(backing)) if backing and ev["named"] else "not named" if backing else "none"
    rows, kept_rows = [], False
    for e in elements:
        words = " ".join(w for k, w in e["parts"] if k != "removed")
        cell = " ".join(f'<span class=el-new>{_escape(w)}</span>' if k == "new"
                        else f'<s class=el-gone>{_escape(w)}</s>' if k == "removed" else _escape(w)
                        for k, w in e["parts"]) if e["kind"] in ("new", "removed", "changed") else _escape(words)
        if e["kind"] == "goal":
            why = "<span class=ids>Design Goal</span>"
        elif e["kind"] == "kept":
            ids = ("Design Goal" if opt_out and words == opt_out
                   else " · ".join([_ids(backing)] + measured) if follow and backing else "as sent")
            kept_rows |= ids not in ("Design Goal", "as sent")
            why = f'kept<span class=ids>{_escape(ids)}</span>'
        else:
            why = f'<span class=el-new>★ {e["kind"]}</span><span class=ids>{_escape(change)}</span>'
        rows.append(f'<tr><td>{cell}</td><td class=elsup>{why}</td></tr>')
    counts = " · ".join(f"{n} {k}" for k in ("new", "changed", "removed")
                        if (n := sum(e["kind"] == k for e in elements)))
    summary = f"{counts} of {len(elements)}" if counts else "all kept"
    note = ('<div class=mut>Kept parts are backed as part of the message as it was tested, not one by one.</div>'
            if kept_rows else "")
    record = element_record(item)
    if record:
        summary += f" · {len(record)} recorded"
    against = ('<div class=mut>Against the starting text:</div>' if record else "")
    return summary, (_record_html(record) if record else "") + (
        f'{against}<table class=elems><tr><th>Element</th><th>Support</th></tr>{"".join(rows)}</table>{note}')


# ----------------------------------------------------------- element matrix --
# The design element is a first citizen, so the page shows the part each one played. The Design Goal names the starting text's parts
# (Resources › Elements); every design is read slot by slot against them, so the page shows
# which elements each design changed, and which the task explored at all.

_SLOT_PART = re.compile(r'([A-Za-z][A-Za-z -]*?)\s*=\s*"([^"]+)"')


def element_slots(aim: dict) -> list[tuple[str, str]]:
    """The Design Goal's `Elements:` line, `greeting = "Hi," · sender = "…"`: the starting
    text named part by part, in reading order."""
    return [(m.group(1).strip(), m.group(2)) for m in _SLOT_PART.finditer((aim or {}).get("elements", ""))]


def slot_reading(base: str, slots: list[tuple[str, str]], text: str) -> dict:
    """One design read slot by slot against the starting text: {"slots": {name: (status,
    words)}, "added": [(after, words)]}. A slot is same (its words kept), changed (other
    words in its place), or removed; words the design adds between two slots are added
    after the slot before them. A slot whose words are not in the starting text is missing."""
    a, b = with_link(base).split(), with_link(text.strip()).split()
    na, nb = [_norm(t) for t in a], [_norm(t) for t in b]
    span, pos = {}, 0
    for name, phrase in slots:                        # where each slot sits in the starting text
        words = [_norm(t) for t in phrase.split()]       # as written: a colon here takes no {LINK}
        for k in range(pos, len(na) - len(words) + 1):
            if na[k:k + len(words)] == words:
                span[name], pos = (k, k + len(words)), k + len(words)
                break
    owner = {i: name for name, (s, e) in span.items() for i in range(s, e)}
    kept = {name: [] for name in span}
    words_of = {name: [] for name in span}
    changed, added = set(), []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, na, nb, autojunk=False).get_opcodes():
        if op == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                if i in owner:
                    words_of[owner[i]].append(b[j])
                    kept[owner[i]].append(i)
            continue
        hit = [owner[i] for i in range(i1, i2) if i in owner]
        if op == "insert":
            inside = owner.get(i1) if owner.get(i1) and owner.get(i1 - 1) == owner.get(i1) else None
            if inside:
                changed.add(inside)
                words_of[inside] += b[j1:j2]
            else:
                added.append((owner.get(i1 - 1, "start"), " ".join(b[j1:j2])))
            continue
        for name in dict.fromkeys(hit):
            changed.add(name)
        if hit and j2 > j1:
            words_of[hit[0]] += b[j1:j2]
    out = {}
    for name, _ in slots:
        if name not in span:
            out[name] = ("missing", "")
        elif name not in changed:
            out[name] = ("same", " ".join(words_of[name]))
        else:
            words = " ".join(words_of[name]).strip()
            out[name] = ("changed", words) if words else ("removed", "")
    return {"slots": out, "added": added}


def record_reading(slots: list[tuple[str, str]], record: dict) -> dict:
    """A design's element record read slot by slot: a slot it names is same when its words are
    the starting text's, else changed; a slot it leaves out is removed; an element that names no
    slot is added. Same shape as `slot_reading`."""
    same = lambda x, y: [_norm(t) for t in x.split()] == [_norm(t) for t in y.split()]
    names = {name.lower() for name, _ in slots}
    out = {}
    for name, phrase in slots:
        rec = record.get(name.lower())
        words = str(rec.get("words") or "").strip() if rec else ""
        out[name] = (("same" if same(words, phrase) else "changed"), words) if rec else ("removed", "")
    added = [(k, str(e.get("words") or "")) for k, e in record.items() if k not in names]
    return {"slots": out, "added": added}


def _element_matrix_html(items: list[dict], aim: dict) -> str:
    """The page's designs, one row each, read slot by slot against the starting text: ★ what
    a design changed, · what it kept, and a last row counting how many designs changed each slot."""
    slots = element_slots(aim)
    base = (aim or {}).get("starting text", "")
    drafts = [(i, shown_design(i)) for i in items if i["state"] != "declined"]
    drafts = [(i, d) for i, d in drafts if d and (d.get("text") or "").strip()]
    if not slots or not base:
        return ""
    if not drafts:
        return ('<details class=elmatrix><summary>Design elements · no draft yet</summary><div class=mut>'
                'Once a design has a draft, it is read here slot by slot against the starting text.</div></details>')
    head = "".join(f"<th>{_escape(name)}</th>" for name, _ in slots) + "<th>added</th>"
    rows, counts = [], {name: 0 for name, _ in slots}
    added_n = 0
    for item, draft in drafts:
        record = {str(e.get("element") or "").strip().lower(): e for e in element_record(item)}
        # the designer's own record is the first source; the word comparison reads the rest
        reading = record_reading(slots, record) if record else slot_reading(base, slots, draft["text"])
        cells = []
        for name, _ in slots:
            status, words = reading["slots"][name]
            rec = record.get(name.lower())
            tag = ""
            if rec:
                frm, how = str(rec.get("from") or "").lower(), str(rec.get("thinking") or "").lower()
                tag = (f'<span class="ids el-from {_escape(frm)}">{_escape(_FROM.get(frm, frm))}'
                       f'{" · " + _escape(how) if how else ""}</span>')
            if status in ("changed", "removed"):
                counts[name] += 1
            cells.append(f'<td class="el-{status}" title="{_escape(words)}">'
                         + ({"same": "·", "missing": "–", "removed": "<s>removed</s>"}.get(status)
                            or f"★ {_escape(words)}") + tag + "</td>")
        extra = reading["added"]
        added_n += bool(extra)
        cells.append('<td class="el-changed">' + "<br>".join(f"★ {_escape(w)}" for _, w in extra) + "</td>"
                     if extra else '<td class="el-same">·</td>')
        rows.append(f'<tr><th><a href="#item-{_escape(item["id"])}" data-item="{_escape(item["id"])}">'
                    f'{_escape(design_number(item["id"]))}</a> <span class=glyph>{item.get("glyph", "")}</span></th>'
                    + "".join(cells) + "</tr>")
    total = len(drafts)
    foot = ("".join(f"<td>{counts[name]} of {total}</td>" for name, _ in slots) + f"<td>{added_n} of {total}</td>")
    explored = sum(1 for n in counts.values() if n) + (1 if added_n else 0)
    return ('<details class=elmatrix><summary>Design elements · '
            f'{total} design{"s" if total != 1 else ""} × {len(slots)} slots · {explored} explored</summary>'
            '<div class=mut>Each design read slot by slot against the starting text (Design Goal › Resources › '
            'Elements): ★ what it changed, · what it kept. Where a design recorded its elements, each cell says '
            'where the element came from and how it was chosen.</div>'
            f'<div class=elscroll><table class=elmat><tr><th>design</th>{head}</tr>{"".join(rows)}'
            f'<tr class=elcount><th>changed in</th>{foot}</tr></table></div></details>')
