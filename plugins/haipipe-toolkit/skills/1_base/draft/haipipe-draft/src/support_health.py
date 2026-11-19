"""health row `support`: every Draft sentence that prints a number has a VALUE, CITE or DISPLAY Evidence Item whose
Target names it (a legend's numbers come from its display's Run). This is the rule behind the Draft Lab's "⚠ no item"
chip (workbench-task-draft draft_step_support.py, the same NUM and NOT_NUM patterns), so health and the page agree
(JL 261116: "why still no item?"). A split sentence or a renumbered paragraph that the items' Target lines did not
follow shows up here. WARN while writing; the final gate makes it a FAIL."""
from __future__ import annotations

import re
from pathlib import Path

# keep in step with workbench-task-draft/draft_step_support.py
NUM = re.compile(r"(?<![\w.,\-])[-+−]?\d[\d,]*(?:\.\d+)?%?(?![\w])")
NOT_NUM = re.compile(r"\\(?:ref|cite[pt]?|autoref|label)\*?\{[^}]*\}|\b(?:Extended Data |Supplementary )?"
                     r"(?:Fig\.|Figs\.|Figure|Table)\s*~?\d+[A-Za-z]?\b|\bC\d+(?:\.P\d+)?(?:\.[BbSs]\d+)?\b|\$[^$]*\$")
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
                           f"{len(loose)} sentence(s) print a number that no VALUE, CITE or DISPLAY item targets (the page's "
                           f"⚠ no item): {', '.join(loose[:8])}; add the address to the right item's Target"))
    else:
        out.append(Finding(OK, "support", "every sentence that prints a number has a VALUE, CITE or DISPLAY item"))
