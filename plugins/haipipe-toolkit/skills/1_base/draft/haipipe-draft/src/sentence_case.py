"""Write one Draft's sentence ids in lowercase: `page.py sentence-case <draft.md> [--records] [--dry-run]`.

A sentence id is written `s8` (`C1.P2.s8`, `- B2 · s3 · …`, `s1 to s10`) so it never reads like a Studio topic
(`s01`, `s02-D01`). Every reader already takes an older `S8` as the same sentence; this command only tidies one file
(and, with `--records`, its `draft/records/<stem>-revise.md`, `-comments.md`, `-checked.md`) so its text says `s`.

It changes only what is a sentence id by its place: a Draft's Bullet lines, its full addresses `C1.P2.S8`, and the
`· S1 to S4` spans of its paragraph headings and overview; in the records, the card and comment headings, the review
report's `- S1 · …` and `Flow P1:` lines, the checked lines' own ids, and every full address. A sentence's own words
are never touched ("Table S1" stays), and nor is a Word address (`P8.S3`, no C before it).
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

from .sentence_id import sid

BULLET = re.compile(r"(?m)^(\s*- (?:\[[ xX]\]\s*)?B\d+[a-z]* · )([Ss]\d+[a-z]*)(?= · )")
FULL = re.compile(r"\bC\d+\.P\d+\.[Ss]\d+[a-z]*\b")
SPAN = re.compile(r"(?m)^((?:#{2,4} |- )C\d+(?:\.P\d+)? · .*·\s*)([Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?)(\s*)$")
BARE = re.compile(r"(?<![A-Za-z0-9_.:])[Ss]\d+[a-z]*(?![0-9A-Za-z-])")


def _low(m) -> str:
    return sid(m.group(0))


def draft_text(text: str) -> str:
    text = BULLET.sub(lambda m: m.group(1) + sid(m.group(2)), text)
    text = FULL.sub(_low, text)
    return SPAN.sub(lambda m: m.group(1) + sid(m.group(2)) + m.group(3), text)


def record_text(text: str, kind: str) -> str:
    out = []
    for line in text.splitlines(True):
        line = FULL.sub(_low, line)
        if kind == "checked":
            line = re.sub(r"^(- )([Ss]\d+[a-z]*)(?= · )", lambda m: m.group(1) + sid(m.group(2)), line)
        elif line.startswith("### ") or (kind == "revise" and re.match(r"^(- [Ss]\d+[a-z]* · |Flow P\d+:)", line)):
            line = BARE.sub(_low, line)
        elif kind == "comments" and line.startswith("- Reply · "):
            line = BARE.sub(_low, line)
        out.append(line)
    return "".join(out)


def targets(draft: Path, records: bool) -> list:
    """[(path, kind)]: the Draft, then its records when asked."""
    out = [(draft, "draft")]
    if records:
        stem = re.sub(r"-draft-v[\w.]+$", "", draft.stem)
        rec = draft.parent / "records"
        out += [(rec / f"{stem}-{k}.md", k) for k in ("revise", "comments", "checked")]
    return out


def convert(draft: Path, *, records: bool = False, dry_run: bool = False) -> list:
    """[(path, changed lines, unified diff)] for each file that would change; written unless dry_run."""
    report = []
    for path, kind in targets(Path(draft), records):
        if not path.is_file():
            continue
        before = path.read_text(encoding="utf-8")
        after = draft_text(before) if kind == "draft" else record_text(before, kind)
        if after == before:
            continue
        diff = list(difflib.unified_diff(before.splitlines(), after.splitlines(), str(path.name), str(path.name),
                                         n=0, lineterm=""))
        report.append((path, sum(1 for d in diff if d.startswith("+") and not d.startswith("+++")), diff))
        if not dry_run:
            path.write_text(after, encoding="utf-8")
    return report


def render(report: list, dry_run: bool, limit: int = 12) -> str:
    if not report:
        return "✅ its sentence ids already read s"
    lines = []
    for path, n, diff in report:
        lines.append(f"{'🔎' if dry_run else '✏️'} {path.name} · {n} line(s) {'would change' if dry_run else 'changed'}")
        body = [d for d in diff if d[:1] in "+-" and not d.startswith(("+++", "---"))]
        lines += ["   " + d for d in body[:2 * limit]]
        if len(body) > 2 * limit:
            lines.append(f"   … {len(body) - 2 * limit} more")
    return "\n".join(lines)
