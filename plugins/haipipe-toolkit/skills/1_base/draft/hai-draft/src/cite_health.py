"""Folder health's citation look (hai-paper ref/must-check.md M-D20): every CITE evidence item names the
citation Run that read it.

A `### E<nn>-CITE-<slug>` item in draft/<stem>-evidence-items.md with no `Local Run` (or one that reads a dash) is a
WARN while writing, and a FAIL at the final gate (folder_health.finalize). A Local Run whose Result path is not on
disk (read from the Section, its version or its Board) is a WARN too. The fix is a command, never a hand edit:
`cite_tasks.py bind <Section Task>` (hai-paper-evidence) writes each Local Run from the citation Job's check.
"""
from __future__ import annotations

import re
from pathlib import Path

ITEM = re.compile(r"(?m)^###\s+(E\d+[a-z]?-CITE-\S+)[^\n]*$")
FIELD = re.compile(r"(?mi)^-\s*\*\*([^*]+)\*\*\s*:\s*(.*?)\s*$")
BIND = "cite_tasks.py bind <Section Task> (hai-paper-evidence) writes them"


def _items(text: str) -> list:
    heads = list(ITEM.finditer(text))
    out = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        body = text[m.end():end]
        nxt = re.search(r"(?m)^#{1,6}\s", body)
        body = body[:nxt.start()] if nxt else body
        out.append((m.group(1), {k.strip().lower(): v for k, v in FIELD.findall(body)}))
    return out


def _found(path: str, folder: Path) -> bool:
    """The one resolver the export and Draft Lab use too (result_paths.resolve)."""
    from .item_table import repo_root
    from .result_paths import resolve
    return resolve(path.strip(), repo_root(folder), folder) is not None


def check_cite_runs(items_file: Path, folder: Path, out: list, finding, warn: str) -> None:
    """Append one finding for CITE items that name no Run, one for bound Runs whose Result is not on disk."""
    if not items_file.is_file():
        return
    unbound, lost = [], []
    for name, f in _items(items_file.read_text(encoding="utf-8", errors="replace")):
        if "retired" in f.get("target", "").lower():
            continue
        run = f.get("local run", "")
        if not run or run.startswith(("\u2014", "-")):
            unbound.append(name.split("-CITE-")[0])
            continue
        result = run.partition("→")[2]
        if result.strip() and not _found(result, folder):
            lost.append(name.split("-CITE-")[0])
    if unbound:
        out.append(finding(warn, "cite", f"CITE item(s) name no citation Run: {', '.join(unbound[:12])}"
                           + (" …" if len(unbound) > 12 else "") + f"; {BIND}", items_file.name))
    if lost:
        out.append(finding(warn, "cite", f"CITE item(s) bound to a Result not on disk: {', '.join(lost[:12])}; "
                           f"rerun the citation Job's ticket, then {BIND.split(' (')[0]}", items_file.name))
