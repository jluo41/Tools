"""Renumber a Draft's sentences in reading order: `page.py renumber <page> [--dry-run]`.

A sentence's S number is its id, and the cards, comments and rulings name it by that id. When a sentence is added,
moved or merged, the ids no longer follow the text (S5 before S4, a new S22 after S8), which a reader finds odd
(JL 261021: "我这 index 是不是要与时俱进一下？ ... 不要 S22，比较奇怪啊"). This renumbers them S1, S2, … in the order
`## 3 · Draft` reads (the plan's order when §3 lists none), in one pass over every file that names a sentence:

- the current Draft (its §1 points, §3 sentences, notes and header lines);
- `evidence/cards.yaml`, each item's `for:` numbers;
- `draft/records/<stem>-revise.md` and `<stem>-revise-rules.md`, every S id;
- `draft/records/<stem>-comments.md`, each comment's target and each AI reply; a person's own notes stay as written.

An id the text no longer has (a retired or merged sentence) is left as it is; say where it went with `--merged`.
"""
from __future__ import annotations

import re
from pathlib import Path

from .folder_health import _page_md
from .outline_version import latest_outline, plan_dir

DRAFT_SECTION = re.compile(r"(?m)^## \d+ · Draft\b")
SID = re.compile(r"(?<![A-Za-z0-9_])S(\d+[a-z]?)(?![0-9])")


def order_of(plan_text: str) -> list:
    """The sentence ids in reading order: `## 3 · Draft`'s lines, else the plan's points."""
    match = DRAFT_SECTION.search(plan_text)
    section = re.split(r"(?m)^## ", plan_text[match.end():], maxsplit=1)[0] if match else ""
    ids = re.findall(r"(?m)^- B\d+ · (S\d+[a-z]?) · ", section) or re.findall(r"(?m)^- B\d+ · (S\d+[a-z]?) · ", plan_text)
    return list(dict.fromkeys(ids))


def renumber(target, *, dry_run: bool = False, merged: dict | None = None) -> dict:
    """Renumber; returns {page, plan, mapping, files, written}."""
    page = _page_md(Path(target))
    folder, stem = page.parent, page.stem
    plan = latest_outline(plan_dir(folder), stem)
    report = {"page": str(page), "plan": plan.name if plan else None, "mapping": {}, "files": [], "written": False}
    if plan is None:
        return report
    order = order_of(plan.read_text(encoding="utf-8"))
    mapping = {old: f"S{i}" for i, old in enumerate(order, 1)}
    for gone, into in (merged or {}).items():
        if into in mapping:
            mapping[gone] = mapping[into]
    report["mapping"] = {k: v for k, v in mapping.items() if k != v}
    if not report["mapping"]:
        return report
    sub = lambda text: SID.sub(lambda m: mapping.get(m.group(0), m.group(0)), text)
    records = plan_dir(folder) / "records"
    edits = {plan: sub}
    edits[records / f"{stem}-revise.md"] = sub
    edits[records / f"{stem}-revise-rules.md"] = sub
    edits[records / f"{stem}-comments.md"] = lambda text: "".join(
        sub(line) if line.startswith(("### Comment", "- Reply · ")) else line for line in text.splitlines(True))

    def cards(text: str) -> str:
        out, under = [], False
        for line in text.splitlines(True):
            if line.strip() == "for:":
                under = True
            elif under and (m := re.match(r"^(\s*- )(\d+[a-z]?)\s*$", line)):
                line = f"{m.group(1)}{mapping.get('S' + m.group(2), 'S' + m.group(2))[1:]}\n"
            else:
                under = False
            out.append(line)
        return "".join(out)
    edits[folder / "evidence" / "cards.yaml"] = cards
    for path, edit in edits.items():
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = edit(before)
        if after != before:
            report["files"].append(str(path.relative_to(folder)))
            if not dry_run:
                path.write_text(after, encoding="utf-8")
    report["written"] = bool(report["files"]) and not dry_run
    return report


def render(report: dict) -> str:
    name = Path(report["page"]).stem
    if not report["mapping"]:
        return f"✅ {name} · its sentences already run S1, S2, … in reading order ({report['plan']})"
    head = f"{'✏️' if report['written'] else '🔎'} {name} · renumbered in reading order ({report['plan']})"
    return "\n".join([head, "   " + " ".join(f"{k}→{v}" for k, v in report["mapping"].items())]
                     + [f"   - {f}" for f in report["files"]])
