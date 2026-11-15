"""Renumber a Draft whose sentence ids restart in every paragraph (page_renumber calls this when an id repeats).

`### C2.P3 · … · S1 to S4` and `### C2.P4 · … · S1 to S4` both hold an S1, so a bare `S1` names no one sentence and
a plain id replace would rewrite every S1 at once. Here a sentence is its place, its full address `C2.P3.S1`, and the
ids run s1, s2, … through the whole Section in reading order:

- the Draft: each Bullet line by the paragraph heading above it (in §1 and §3 alike), each paragraph's `· s<a> to s<b>`
  span, and every full address `C2.P3.S1`;
- the records (`<stem>-revise.md`, `-revise-rules.md`, `-comments.md`): every full address; a bare id on a line that
  also names one paragraph (`### Edit · S1 · C2.P3.B1 · …`) is that paragraph's sentence;
- `<stem>-checked.md`: a line is the sentence its words are;
- every other bare id (an `evidence/cards.yaml` `for:` number, a line naming no paragraph) is left as written and
  listed, since only a person can say which sentence it meant.
"""
from __future__ import annotations

import re
from pathlib import Path

from .page_ranges import fix as _ranges
from .sentence_id import sid

HEAD = re.compile(r"^#{2,4} (C\d+\.P\d+)\b")
OVERVIEW = re.compile(r"^- (C\d+\.P\d+) · ")              # a Structure Overview line, `- C1.P1 · Why · S1 to S4`
LINE = re.compile(r"^(- B\d+[a-z]* · )([Ss]\d+[a-z]*)( · )(.*)$")
FULL = re.compile(r"\b(C\d+\.P\d+)\.([Ss]\d+[a-z]*)\b")
BARE = re.compile(r"(?<![A-Za-z0-9_.:])[Ss]\d+[a-z]*(?![0-9A-Za-z-])")
PARA = re.compile(r"\b(C\d+\.P\d+)(?:\.B\d+[a-z]*)?\b")
SPAN = re.compile(r"(·\s*)[Ss]\d+[a-z]*(?:\s+to\s+[Ss]\d+[a-z]*)?(\s*)$")


def positions(plan_text: str) -> list:
    """[(paragraph, id, words)] of `## 3 · Draft` (else the whole plan) in reading order, ids as sid() writes them."""
    from .page_renumber import DRAFT_SECTION
    m = DRAFT_SECTION.search(plan_text)
    body = re.split(r"(?m)^## ", plan_text[m.end():], maxsplit=1)[0] if m else plan_text
    out, pid = [], ""
    for line in body.splitlines():
        h = HEAD.match(line)
        pid = h.group(1) if h else pid
        b = LINE.match(line)
        if b:
            out.append((pid, sid(b.group(2)), " ".join(b.group(4).split())))
    return out


def renumber_by_position(report: dict, folder: Path, stem: str, plan: Path, records: Path, *, dry_run: bool) -> dict:
    from .page_renumber import write_edits
    text = plan.read_text(encoding="utf-8")
    pos = positions(text)
    first = 0 if pos and pos[0][1] == "s0" and pos[0][0].endswith(".P0") else 1   # a title paragraph keeps s0
    new = {}
    for i, (pid, old, _) in enumerate(pos, first):
        new.setdefault((pid, old), f"s{i}")
    words = {}
    for (pid, old, w), i in zip(pos, range(first, len(pos) + first)):
        words.setdefault(w, f"s{i}")
    report["mapping"] = {f"{pid}.{old}": v for (pid, old), v in new.items() if old != v}
    if not report["mapping"]:
        return report
    amb = report["ambiguous"]

    def full(t: str) -> str:
        return FULL.sub(lambda m: f"{m.group(1)}." + new.get((m.group(1), sid(m.group(2))), m.group(2)), t)

    def draft(t: str) -> str:
        out, pid = [], ""
        span = {}
        for p_, v in new.items():
            span.setdefault(p_[0], []).append(int(v[1:]))
        for n, line in enumerate(t.splitlines(True), 1):
            h = HEAD.match(line) or OVERVIEW.match(line)
            if h:
                pid = h.group(1) if line.startswith("#") else pid
                ns = span.get(h.group(1))
                if ns and SPAN.search(line.rstrip("\n")):
                    to = f"s{min(ns)}" + (f" to s{max(ns)}" if max(ns) != min(ns) else "")
                    line = SPAN.sub(lambda m: m.group(1) + to + m.group(2), line.rstrip("\n")) + "\n" * line.endswith("\n")
                out.append(full(line))
                continue
            b = LINE.match(line.rstrip("\n"))
            if b and (pid, sid(b.group(2))) in new:
                line = b.group(1) + new[(pid, sid(b.group(2)))] + line[b.end(2):]
            else:
                line = full(line)
                for m in BARE.finditer(line):
                    amb.append(f"{plan.name}:{n} {m.group(0)}")
            out.append(line)
        return "".join(out)

    def record(name: str, only=None):
        def edit(t: str) -> str:
            out = []
            for n, line in enumerate(t.splitlines(True), 1):
                if only and not line.startswith(only):
                    out.append(line)
                    continue
                line = full(line)
                paras = set(PARA.findall(FULL.sub("", line)))
                if len(paras) == 1:
                    pid = next(iter(paras))
                    line = BARE.sub(lambda m: new.get((pid, sid(m.group(0))), m.group(0)), line)
                for m in BARE.finditer(FULL.sub("", line)):
                    if not re.fullmatch(r"s\d+[a-z]*", m.group(0)) or len(paras) != 1:
                        amb.append(f"{name}:{n} {m.group(0)}")
                out.append(line)
            return "".join(out)
        return edit

    def checked(t: str) -> str:
        out = []
        for n, line in enumerate(t.splitlines(True), 1):
            m = re.match(r"^(- )([Ss]\d+[a-z]*)( · [^·]+ · )(.*)$", line.rstrip("\n"))
            got = m and words.get(" ".join(m.group(4).split()))
            if got:
                line = m.group(1) + got + line[m.end(2):]
            elif m:
                amb.append(f"{stem}-checked.md:{n} {m.group(2)}")
            out.append(line)
        return "".join(out)

    def cards(t: str) -> str:
        under = False
        for n, line in enumerate(t.splitlines(), 1):
            if re.match(r"^\s*(?:- )?for:\s*$", line):
                under = True
            elif under and re.match(r"^\s*- [Ss]?\d+[a-z]*\s*$", line):
                amb.append(f"evidence/cards.yaml:{n} {line.strip()[2:]}")
            else:
                under = False
        return t

    edits = {plan: lambda t: _ranges(draft(t)),
             records / f"{stem}-revise.md": record(f"{stem}-revise.md"),
             records / f"{stem}-revise-rules.md": record(f"{stem}-revise-rules.md"),
             records / f"{stem}-comments.md": record(f"{stem}-comments.md", ("### Comment", "- Reply · ")),
             records / f"{stem}-checked.md": checked,
             folder / "evidence" / "cards.yaml": cards}
    return write_edits(report, folder, edits, dry_run)
