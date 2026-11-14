"""Renumber a Draft's sentences in reading order: `page.py renumber <page> [--dry-run]`.

A sentence's S number is its id, and the cards, comments and rulings name it by that id. When a sentence is added,
moved or merged, the ids no longer follow the text (S5 before S4, a new S22 after S8), which a reader finds odd
(JL 261021: "我这 index 是不是要与时俱进一下？ ... 不要 S22，比较奇怪啊"). This renumbers them S1, S2, … in the order
`## 3 · Draft` reads (the plan's order when §3 lists none), in one pass over every file that names a sentence:

- the current Draft (its §1 points, §3 sentences, notes and header lines);
- `evidence/cards.yaml`, each item's `for:` numbers;
- `draft/records/<stem>-revise.md` and `<stem>-revise-rules.md`, every S id;
- `draft/records/<stem>-comments.md`, each comment's target and each AI reply; a person's own notes stay as written.

Only page addresses change: `S4`, `· S4 ·`, `C2.P3.S4`, `S4 to S7`. A Word or tracked-edit address, `P8.S3` or
`02-literature:P4.S3` (a P with no C before it), keeps its numbers. An id the text no longer has (a cut or merged
sentence) is left as it is, unless a new sentence takes that number: then it is marked `S2-cut`, so an old note never
points at the new S2. Say where a merged one went with `--merged`.
"""
from __future__ import annotations

import re
from pathlib import Path

from .folder_health import _page_md
from .outline_version import latest_outline, plan_dir

DRAFT_SECTION = re.compile(r"(?m)^## \d+ · Draft\b")
SID = re.compile(r"(?<![A-Za-z0-9_])S(\d+[a-z]*)(?![0-9A-Za-z-])")
WORD_ADDRESS = re.compile(r"(?<![.A-Za-z0-9])P\d+\.$")   # "P8." or ":P4." just before the id: a Word address


def order_of(plan_text: str) -> list:
    """The sentence ids in reading order: `## 3 · Draft`'s lines, else the plan's points."""
    match = DRAFT_SECTION.search(plan_text)
    section = re.split(r"(?m)^## ", plan_text[match.end():], maxsplit=1)[0] if match else ""
    ids = re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", section) or re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", plan_text)
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
    records = plan_dir(folder) / "records"
    page_ids = lambda text: [m for m in SID.finditer(text) if not WORD_ADDRESS.search(text[max(0, m.start() - 12):m.start()])]
    names = {records / f"{stem}-{k}.md" for k in ("revise", "revise-rules", "comments")} | {plan}
    seen = {m.group(0) for path in names if path.is_file() for m in page_ids(path.read_text(encoding="utf-8"))}
    taken = set(mapping.values())
    for gone in sorted(seen - set(mapping)):          # a cut sentence whose number a new sentence now takes
        if gone in taken:
            mapping[gone] = f"{gone}-cut"
    report["mapping"] = {k: v for k, v in mapping.items() if k != v}
    if not report["mapping"]:
        return report

    def sub(text: str) -> str:
        out, at = [], 0
        for m in page_ids(text):
            out += [text[at:m.start()], mapping.get(m.group(0), m.group(0))]
            at = m.end()
        return "".join(out) + text[at:]
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
            elif under and (m := re.match(r"^(\s*- )(\d+[a-z]*)\s*$", line)):
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
