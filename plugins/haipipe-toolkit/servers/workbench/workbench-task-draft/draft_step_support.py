"""Each sentence's support in Draft Lab (must-check M-D18, shown calmly per M-D17): the Page's evidence items
(draft/<stem>-evidence-items.md, `### E<nn>-VALUE|CITE|DISPLAY-<slug>` with Target, Expected, Verified, Local Input,
Local Run) bound to the sentences they target, each resolved against disk; a printed number no VALUE item covers; a
citation's verified state from the citation Job (cite_tasks.py citations.csv, status `verified`) or a signed item.

A sentence whose items all resolve and whose numbers are all covered shows one quiet ✓; otherwise one small chip per
item (✓ resolved, ❗ bound but not found); an uncovered number shows only in health. A chip opens its details on click (focus)."""
from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path

from live.frame import esc
from src.evidence_resolve import (  # noqa: F401  one check for the page and health
    ITEM_HEAD, PATH, VID, _field, _find, _items_file, _read, evidence_items, resolve)

# a printed number: 2,660 · 57.5 · -6.7% · 95%; never a part of an id (C1.P2), a word (AI-READI, h24) or a \ref
NUM = re.compile(r"(?<![\w.,\-])[-+−]?\d[\d,]*(?:\.\d+)?%?(?![\w])")
NOT_NUM = re.compile(r"\\(?:ref|cite[pt]?|autoref|label)\*?\{[^}]*\}|\b(?:Extended Data |Supplementary )?"
                     r"(?:Fig\.|Figs\.|Figure|Table|Supplement|eTable|eFigure|eAppendix|eMethods)\s*~?\d+[A-Za-z]?\b"
                     r"|\b\d+-(?:part|day|week|month|year|hour|minute|step|fold|way|level|stage|item|point)s?\b"   # a label or a
                     r"|\bC\d+(?:\.P\d+)?(?:\.[BbSs]\d+)?\b|\$[^$]*\$")   # modifier (\"See Supplement 2\", \"2-part model\"), not a value

SUPPORT_CSS = """<style>
.ev-sup{position:relative;display:inline;font:11px/1 system-ui,-apple-system,sans-serif;margin-left:4px;white-space:nowrap}
.ev-sup .ev-chip,.ev-sup .ev-allok{cursor:pointer;border-radius:4px;padding:0 3px;margin-left:2px;color:var(--mut)}
.ev-sup .ev-chip.miss{color:#c92a2a;border:1px solid #f1aeb5}.ev-sup .ev-chip.none{color:#b35c00;border:1px solid #f3c58a}
.ev-sup .ev-chip.ok{opacity:.75}.ev-sup .ev-allok{opacity:.6}
.ev-sup .ev-det{display:none;position:absolute;z-index:5;left:0;top:1.6em;min-width:280px;max-width:460px;white-space:normal;
 background:var(--bg,#fff);border:1px solid var(--line,#ddd);border-radius:6px;padding:6px 8px;font-size:12px;line-height:1.45;
 box-shadow:0 4px 14px rgba(0,0,0,.12);color:var(--fg,#222)}
.ev-sup>span:focus+.ev-det,.ev-sup .ev-det:hover{display:block}
.cite-unv{display:none}   /* an unverified citation lights its row's ❝ mark instead (JL 261115) */.disp-xref{border-bottom:1px dotted currentColor;cursor:help}
</style>"""


def numbers(words: str) -> list:
    """The numbers a sentence prints, its display calls, citations, ids and maths left out."""
    return NUM.findall(NOT_NUM.sub(" ", words))


def _targets(d: dict) -> dict:
    """{target as an item names it: the sentence's full address} for C1.P1.B2, C1.P1.s2 and a bare s2."""
    from live.draft_step_evidence import _sx_paras
    out = {}
    for pid, rows in _sx_paras(d):
        for b, sid in rows:
            a = f"{pid}.{sid}" if pid else sid
            out[f"{pid}.{b}"] = a
            out[a.lower()] = a
            out.setdefault(sid.lower(), a)
    return out


def sentence_support(d: dict, task: Path) -> dict:
    """{address: {"items": [(item, resolved)], "loose": [numbers no VALUE item covers]}} for every sentence."""
    from live.draft_step_evidence import _bib_names
    from src.result_displays import result_units
    task = Path(task)
    items = evidence_items(task)
    tmap = _targets(d)
    bib = _bib_names(d)
    done = {u["item"] for u in result_units(task)}
    out = {}
    for it in items:
        r = resolve(it, task, bib, done)
        for t in it["targets"]:
            a = tmap.get(t) or tmap.get(t.lower())
            if a:
                out.setdefault(a, {"items": [], "loose": []})["items"].append((it, r))
    for _, body in (d or {}).get("text", []):
        pid = ""
        for line in body.splitlines():
            h = re.match(r"^#{1,6}\s*(C\d+\.P\d+)\b", line)
            if h:
                pid = h.group(1)
                continue
            m = re.match(r"^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · (.*)$", line)
            if not m:
                continue
            a = f"{pid}.{m.group(1).lower()}" if pid else m.group(1).lower()
            row = out.setdefault(a, {"items": [], "loose": []})
            kinds = {it["kind"] for it, _ in row["items"]}
            # a number in a sentence a CITE item covers, with no VALUE item, is a cited fact, not our result
            # ("every 5 minutes \citep{Battelino_2019}"): no ⚠ (must-check M-D18)
            if not kinds & {"VALUE", "CITE", "DISPLAY", "TABLE"}:   # a display item backs its numbers too, as health's support row
                row["loose"] = numbers(m.group(2))
    return {a: r for a, r in out.items() if r["items"] or r["loose"]}


def _det(lines: list) -> str:
    return '<span class=ev-det>' + "<br>".join(lines) + '</span>'


KIND_ICON = {"VALUE": "📊", "CITE": "❝", "DISPLAY": "🖼", "TABLE": "🖼"}


def chips(row: dict) -> str:
    """One sentence's support marks: a chip per item that does not resolve (its kind's icon and ❗);
    nothing when all resolve."""
    items, loose = row["items"], row["loose"]
    line = lambda it, r: (f'<b>{esc(it["id"])} {esc(it["kind"])}</b> {"✓" if r["state"] == "ok" else "❗"} '
                          f'{esc(it["label"])}<br><span class=mut>{esc("; ".join(r["why"]))}'
                          + (f' · verified: {esc(it["verified"])}' if it["verified"] else "") + '</span>')
    # evidence that resolves draws nothing here: the row's 📊n and ❝n marks already say it is there (JL 261115: "we have
    # the emoji for the numbers and for the cite, why we still need this"); only a broken item or a loose number shows
    out = []
    for it, r in items:
        if r["state"] == "ok":
            continue
        icon = KIND_ICON.get(it["kind"], "🔗")             # the kind's own icon; ❗ beside it when it does not resolve
        mark = icon if r["state"] == "ok" else icon + "❗"
        out.append(f'<span class="ev-chip {"ok" if r["state"] == "ok" else "miss"}" tabindex=0 '
                   f'title="{esc(it["id"])} {esc(it["kind"])}">{mark}</span>'
                   + _det([line(it, r)]))
    # a loose number draws nothing on the page (JL 261117 on "⚠ no item": "I don't wnat this, could you remove it?
    # Too large"); page.py health row `support` still lists those sentences
    return ('<span class=ev-sup>' + "".join(out) + '</span>') if out else ""


def support_marks(html: str, d: dict, task: Path) -> str:
    """Each sentence row of the board (`<li data-s=… data-a=…>`) with its support marks at the end of its words."""
    sup = sentence_support(d, task)
    if not sup:
        return html
    def one(m):
        row = sup.get(m.group(2)) or sup.get(m.group(2).lower())
        return m.group(1) + chips(row) + m.group(3) if row else m.group(0)
    return SUPPORT_CSS + re.sub(r'(?s)(<li data-s="[^"]*" data-a="([^"]*)"[^>]*>.*?)(</span></li>)', one, html)


def xref_spans(html: str, xs) -> str:
    """An Extended Data name in the visible text, read as a reference to the Section that holds it."""
    refs = {x["names"][0]: x["owner"] for x in xs or () if x.get("ref") and x.get("names")}
    if not refs:
        return html
    pat = re.compile("|".join(re.escape(n) for n in sorted(refs, key=len, reverse=True)))
    seg = lambda m: ">" + pat.sub(lambda r: f'<span class=disp-xref title="in {esc(refs[r.group(0)])}">{r.group(0)}</span>',
                                  m.group(1)) + "<"
    return re.sub(r">([^<]*)<", seg, html)


@lru_cache(maxsize=32)
def _csv_states(path: str, mtime: float) -> dict:
    with open(path, encoding="utf-8", newline="") as fh:
        return {r.get("key", ""): (r.get("status", ""), r.get("verified", "")) for r in csv.DictReader(fh) if r.get("key")}


def cite_states(task: Path) -> dict:
    """{key: (verified?, why)}: the citation Job's newest check (t99 first, then each claim group), as cite_tasks.py
    decides `verified` (a bib entry and a signed CITE Result); a CITE evidence item marked `Verified: ✅` counts too."""
    task = Path(task)
    board = task.parent.parent
    out = {}
    runs = sorted(board.glob("j*/t99*/runs/*/result/citations.csv"), reverse=True) + sorted(
        board.glob("j*/t[0-8]*/runs/*/result/citations.csv"), reverse=True)
    for f in runs:
        try:
            rows = _csv_states(str(f), f.stat().st_mtime)
        except OSError:
            continue
        for k, (status, by) in rows.items():
            if k not in out or (status == "verified" and not out[k][0]):
                out[k] = (status == "verified", f"{status}" + (f" · {by}" if by and by != "nobody yet" else ""))
    for it in evidence_items(task):
        if it["kind"] == "CITE" and it["verified"].startswith("✅"):
            out[it["label"].strip()] = (True, it["verified"])
    return out
