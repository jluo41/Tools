"""A paragraph's sentence range, everywhere the Draft writes one, is rebuilt from the sentences that paragraph holds:
its heading (`### C2.P3 · Why · s21 to s26`) and its Structure Overview line (`- C2.P3 · Why · s21 to s26` or
`C2.P3 … → s21 to s26`). Renumber never shifts a range's ends on their own (ScalingGlucose 261115: "s21 to s26" became
s27 while the paragraph still ended at s26; the Overview ranges were left for the person to fix by hand). A
paragraph's first and last sentence in `## 3 · Draft`, in reading order, are its range; a one-sentence paragraph
reads `s5`. A line that names no paragraph the Draft has is left as it is."""
from __future__ import annotations

import re

from .sentence_id import sid

HEAD = re.compile(r"^#{2,4} (C\d+\.P\d+)\b")
LINE = re.compile(r"^- B\d+[a-z]* · ([Ss]\d+[a-z]*) · ")
NAMED = re.compile(r"\b(C\d+\.P\d+)\b")
# a renumber may leave "s152-cut" or a doubled "to" inside a range (t04_methods 261118): the whole run is replaced
RANGE = re.compile(r"[Ss]\d+[a-z]*(?:-cut)?(?:\s+to\s+[Ss]\d+[a-z]*(?:-cut)?)*")
DRAFT = re.compile(r"(?m)^## \d+ · Draft\b")


def spans(text: str) -> dict:
    """{paragraph: [its sentence ids in reading order]} from `## 3 · Draft` (else the whole text)."""
    m = DRAFT.search(text)
    body = re.split(r"(?m)^## ", text[m.end():], maxsplit=1)[0] if m else text
    out, pid = {}, ""
    for line in body.splitlines():
        h = HEAD.match(line)
        pid = h.group(1) if h else pid
        b = LINE.match(line)
        if b and pid:
            out.setdefault(pid, []).append(sid(b.group(1)))
    return out


def label(ids: list) -> str:
    return ids[0] if len(ids) == 1 or ids[0] == ids[-1] else f"{ids[0]} to {ids[-1]}"


def fix(text: str) -> str:
    """Every heading and Overview line that names one paragraph and carries a range gets that paragraph's own range;
    a Bullet line and any line naming no known paragraph or two of them stay as written."""
    have = spans(text)
    out = []
    for line in text.splitlines(True):
        body = line.rstrip("\n")
        named = set(NAMED.findall(body))
        if body.startswith("- B") or len(named) != 1 or next(iter(named)) not in have:
            out.append(line)
            continue
        want = label(have[next(iter(named))])
        tail = body.rfind("·") if "→" not in body else body.rfind("→")      # the range sits after the last · or →
        if tail < 0 or not RANGE.search(body[tail:]):
            out.append(line)
            continue
        head, rest = body[:tail], body[tail:]
        rest = RANGE.sub(want, rest, count=1)
        out.append(head + rest + line[len(body):])
    return "".join(out)


def wrong(text: str) -> list:
    """[(line number, written, should be)] for each range that does not match its paragraph: the health check."""
    after = fix(text).splitlines()
    case = lambda x: re.sub(r"\b[Ss](\d)", r"s\1", x)           # S1 and s1 are one id: a case is not a wrong range
    return [(n, a.strip(), b.strip()) for n, (a, b) in enumerate(zip(text.splitlines(), after), 1) if case(a) != case(b)]
