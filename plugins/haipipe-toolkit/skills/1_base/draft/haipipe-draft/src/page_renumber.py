"""Renumber a Draft's sentences in reading order: `page.py renumber <page> [--dry-run]`.

A sentence's s number is its id, and the cards, comments and rulings name it by that id. When a sentence is added,
moved or merged, the ids no longer follow the text (s5 before s4, a new s22 after s8), which a reader finds odd
(JL 261021: "我这 index 是不是要与时俱进一下？ ... 不要 S22，比较奇怪啊"). This renumbers them s1, s2, … in the order
`## 3 · Draft` reads (the plan's order when §3 lists none), through the whole Section, in one pass over every file
that names a sentence:

- the current Draft (its §1 points, §3 sentences, notes and header lines);
- `evidence/cards.yaml`, each item's `for:` numbers;
- `draft/records/<stem>-revise.md` and `<stem>-revise-rules.md`, every sentence id;
- `draft/records/<stem>-comments.md`, each comment's target and each AI reply; a person's own notes stay as written.

Only page addresses change: `s4`, `· s4 ·`, `C2.P3.s4`, `s4 to s7`. An older `S4` is read as the same sentence and
written `s4`. A Word or tracked-edit address, `P8.S3` or `02-literature:P4.S3` (a P with no C before it), keeps its
numbers. An id the text no longer has (a cut or merged sentence) is left as it is, unless a new sentence takes that
number: then it is marked `s2-cut`, so an old note never points at the new s2. Say where a merged one went with
`--merged`.

A Draft that restarts its ids in every paragraph (`### C2.P3 · … · S1 to S4`, then `### C2.P4 · … · S1 to S4`) has
the same id twice, so a bare id names no one sentence: it is renumbered by position (page_renumber_position).
"""
from __future__ import annotations

import re
from pathlib import Path

from .folder_health import _page_md
from .outline_version import latest_outline, plan_dir
from .sentence_id import sid

DRAFT_SECTION = re.compile(r"(?m)^## \d+ · Draft\b")
SID = re.compile(r"(?<![A-Za-z0-9_])[Ss](\d+[a-z]*)(?![0-9A-Za-z-])")
WORD_ADDRESS = re.compile(r"(?<![.A-Za-z0-9])P\d+\.$")   # "P8." or ":P4." just before the id: a Word address
BULLET = re.compile(r"(?m)^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · ")


def _ids(plan_text: str) -> list:
    """Every sentence id in reading order, repeats kept, as sid() writes them."""
    match = DRAFT_SECTION.search(plan_text)
    section = re.split(r"(?m)^## ", plan_text[match.end():], maxsplit=1)[0] if match else ""
    return [sid(x) for x in (BULLET.findall(section) or BULLET.findall(plan_text))]


def order_of(plan_text: str) -> list:
    """The sentence ids in reading order: `## 3 · Draft`'s lines, else the plan's points."""
    return list(dict.fromkeys(_ids(plan_text)))


def repeated(plan_text: str) -> list:
    """The sentence ids a Draft carries more than once (a Draft numbered per paragraph), in reading order."""
    ids = _ids(plan_text)
    return list(dict.fromkeys(x for x in ids if ids.count(x) > 1))


def renumber(target, *, dry_run: bool = False, merged: dict | None = None) -> dict:
    """Renumber; returns {page, plan, mapping, files, written, ambiguous}."""
    page = _page_md(Path(target))
    folder, stem = page.parent, page.stem
    plan = latest_outline(plan_dir(folder), stem)
    report = {"page": str(page), "plan": plan.name if plan else None, "mapping": {}, "files": [], "written": False,
              "ambiguous": []}
    if plan is None:
        return report
    text = plan.read_text(encoding="utf-8")
    records = plan_dir(folder) / "records"
    if repeated(text):
        from .page_renumber_position import renumber_by_position
        return renumber_by_position(report, folder, stem, plan, records, dry_run=dry_run)
    order = order_of(text)
    first = 0 if order and order[0] == "s0" else 1      # an Abstract's title paragraph (C1.P0) holds s0 by design
    mapping = {old: f"s{i}" for i, old in enumerate(order, first)}
    for gone, into in (merged or {}).items():
        if sid(into) in mapping:
            mapping[sid(gone)] = mapping[sid(into)]
    page_ids = lambda text: [m for m in SID.finditer(text) if not WORD_ADDRESS.search(text[max(0, m.start() - 12):m.start()])]
    names = {records / f"{stem}-{k}.md" for k in ("revise", "revise-rules", "comments")} | {plan}
    seen = {sid(m.group(0)) for path in names if path.is_file() for m in page_ids(path.read_text(encoding="utf-8"))}
    taken = set(mapping.values())
    for gone in sorted(seen - set(mapping)):          # a cut sentence whose number a new sentence now takes
        if gone in taken:
            mapping[gone] = f"{gone}-cut"
    report["mapping"] = {k: v for k, v in mapping.items() if k != v}
    from .page_ranges import fix as fix_ranges
    if not report["mapping"]:                         # ids in order; a range may still be wrong (261115)
        return write_edits(report, folder, {plan: fix_ranges}, dry_run)

    def sub(text: str) -> str:                         # every id the text has is written s, renumbered or not
        out, at = [], 0
        for m in page_ids(text):
            out += [text[at:m.start()], mapping.get(sid(m.group(0)), m.group(0))]
            at = m.end()
        return "".join(out) + text[at:]
    edits = {plan: lambda t: fix_ranges(sub(t))}       # ranges from the paragraphs' new ids, never shifted ends
    edits[records / f"{stem}-revise.md"] = sub
    edits[records / f"{stem}-revise-rules.md"] = sub
    edits[records / f"{stem}-checked.md"] = lambda text: re.sub(   # only each line's own id, never its words
        r"(?m)^(- )([Ss]\d+[a-z]*)(?= · )", lambda m: m.group(1) + mapping.get(sid(m.group(2)), m.group(2)), text)
    edits[records / f"{stem}-comments.md"] = lambda text: "".join(
        sub(line) if line.startswith(("### Comment", "- Reply · ")) else line for line in text.splitlines(True))

    def cards(text: str) -> str:
        out, under = [], False
        for line in text.splitlines(True):
            if line.strip() == "for:":
                under = True
            elif under and (m := re.match(r"^(\s*- )([Ss]?)(\d+[a-z]*)\s*$", line)):
                new = mapping.get("s" + m.group(3), "s" + m.group(3))
                line = f"{m.group(1)}{new if m.group(2) else new[1:]}\n"
            else:
                under = False
            out.append(line)
        return "".join(out)
    edits[folder / "evidence" / "cards.yaml"] = cards
    return write_edits(report, folder, edits, dry_run)


def write_edits(report: dict, folder: Path, edits: dict, dry_run: bool) -> dict:
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
        if report["files"]:
            return f"{'✏️' if report['written'] else '🔎'} {name} · ids in order; ranges rebuilt from their paragraphs ({report['plan']})"
        return f"✅ {name} · its sentences already run s1, s2, … in reading order ({report['plan']})"
    head = f"{'✏️' if report['written'] else '🔎'} {name} · renumbered in reading order ({report['plan']})"
    lines = [head, "   " + " ".join(f"{k}→{v}" for k, v in report["mapping"].items())]
    lines += [f"   - {f}" for f in report["files"]]
    if report.get("ambiguous"):
        lines.append("   left as written (a bare id the repeated numbering makes ambiguous):")
        lines += [f"   ? {a}" for a in report["ambiguous"]]
    return "\n".join(lines)
