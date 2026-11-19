"""health row `support`: every Draft sentence that prints a number has a VALUE, CITE or DISPLAY Evidence Item whose
Target names it (a legend's numbers come from its display's Run). The Draft Lab once showed these as a "⚠ no item" chip; since
JL 261117 ("I don't wnat this ... Too large") only health lists them (draft_step_support.py keeps the same NUM and
NOT_NUM patterns). A split sentence or a renumbered paragraph that the items' Target lines did not
follow shows up here. WARN while writing; the final gate makes it a FAIL."""
from __future__ import annotations

import re
from pathlib import Path

# keep in step with workbench-task-draft/draft_step_support.py
NUM = re.compile(r"(?<![\w.,\-])[-+−]?\d[\d,]*(?:\.\d+)?%?(?![\w])")
NOT_NUM = re.compile(r"\\(?:ref|cite[pt]?|autoref|label)\*?\{[^}]*\}|\b(?:Extended Data |Supplementary )?"
                     r"(?:Fig\.|Figs\.|Figure|Table|Supplement|eTable|eFigure|eAppendix|eMethods)\s*~?\d+[A-Za-z]?\b"
                     r"|\b\d+-(?:part|day|week|month|year|hour|minute|step|fold|way|level|stage|item|point)s?\b"   # a label or a
                     r"|\bC\d+(?:\.P\d+)?(?:\.[BbSs]\d+)?\b|\$[^$]*\$")   # modifier (\"See Supplement 2\", \"2-part model\"), not a value
ITEM = re.compile(r"(?m)^###\s+(E\d+[a-z]?)-(VALUE|CITE|DISPLAY|TABLE)-\S+")
TARGET = re.compile(r"(?mi)^-\s*\*\*Target\*\*\s*:\s*(.*?)\s*$")
PARA = re.compile(r"^#{2,6}\s*(C\d+\.P\d+)\b")
ROW = re.compile(r"^- (B\d+[a-z]*) · ([Ss]\d+[a-z]*) · (.*)$")


def numbers(words: str) -> list:
    return NUM.findall(NOT_NUM.sub(" ", words))


def _draft_rows(plan_text: str) -> list:
    """[(paragraph, B, sid, words)] from § 3 of the Draft (the sentences), else the whole file."""
    i = plan_text.find("## 3 ·")
    body = plan_text[i:] if i >= 0 else plan_text
    rows, pid = [], ""
    for line in body.splitlines():
        h = PARA.match(line)
        if h:
            pid = h.group(1)
            continue
        m = ROW.match(line)
        if m:
            rows.append((pid, m.group(1), m.group(2).lower(), m.group(3)))
    return rows


def check_support(items_file: Path, plan_text: str, out: list, Finding, WARN, OK):
    rows = _draft_rows(plan_text)
    if not rows or not items_file.is_file():
        return
    alias = {}
    for pid, b, sid, _ in rows:
        for key in (f"{pid}.{b}", f"{pid}.{sid}", sid):
            alias[key.lower()] = sid
    text = items_file.read_text(encoding="utf-8", errors="replace")
    heads = list(ITEM.finditer(text))
    covered: set = set()
    for k, m in enumerate(heads):
        # a DISPLAY item counts too: an Extended Data legend's numbers (panel sizes, model counts) come from the
        # display's own Run (Board 261116, t21_extended-data)
        body = text[m.end():heads[k + 1].start() if k + 1 < len(heads) else len(text)]
        t = TARGET.search(body)
        for tgt in re.split(r"[,;]", t.group(1) if t else ""):
            sid = alias.get(tgt.strip().lower())
            if sid:
                covered.add(sid)
    loose = [f"{pid}.{sid}" for pid, b, sid, words in rows if sid not in covered and numbers(words)]
    if loose:
        out.append(Finding(WARN, "support",
                           f"{len(loose)} sentence(s) print a number that no VALUE, CITE or DISPLAY item targets: {', '.join(loose[:8])}; add the address to the right item's Target"))
    else:
        out.append(Finding(OK, "support", "every sentence that prints a number has a VALUE, CITE or DISPLAY item"))
    check_files(items_file, out, Finding, WARN, OK)


def check_files(items_file: Path, out: list, Finding, WARN, OK):
    """health row `evidence-files`: each item's named files, Result or Bib key is on disk, by the same check that
    marks 📊❗ on the page (evidence_resolve.resolve). WARN while writing, FAIL at the final gate."""
    from .evidence_resolve import bib_keys, evidence_items, resolve
    from .result_displays import result_units
    task = items_file.parent.parent
    try:
        done = {u["item"] for u in result_units(task)}
    except Exception:  # noqa: BLE001  an older Task with no results/ reads as none
        done = set()
    bib = bib_keys(task)
    miss = []
    for it in evidence_items(task):
        r = resolve(it, task, bib, done)
        if r["state"] == "miss":
            miss.append(f"{it['id']} ({'; '.join(w for w in r['why'] if not w.startswith('its '))[:90]})")
    if miss:
        out.append(Finding(WARN, "evidence-files", f"{len(miss)} item(s) show 📊❗ on the page: " + ", ".join(miss[:6])
                           + "; fix the path in Expected or Local Input"))
    else:
        out.append(Finding(OK, "evidence-files", "every Evidence Item's files, Result or Bib key is on disk"))
