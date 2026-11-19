"""How many sentences each planned paragraph holds, and which fall outside the paper's range (JL 261112: "we want to
make each paragraph about 4 to 6 sentences", then "abstract should be okay. for other, unless having good reason, we
might make sure they are between 4~7 sentences").

One reader for every check: `page.py health` (the `paragraph` row), haipipe-paper's paper_check, the review audit and
the workbench's Plan maps. A paragraph is a `### C<n>.P<m> · <name> · s<a> to s<b>` heading of a draft's
`## 1 · Structure`; its count is b - a + 1, else the Bullets (`- B<n> · …`) under it. A `reason: <why>` line under the
heading accepts a count outside the range. The Abstract, an appendix or supplement (legends), a letter and a P0 title
paragraph are exempt.
"""
from __future__ import annotations

import re

RANGE = (4, 7)
EXEMPT = ("abstract", "summary", "appendix", "supplement", "supplementary", "extended data", "extended-data",
          "letter", "cover letter", "cover-letter", "response",
          "back-matter", "back matter", "front-matter", "front matter")   # one field per line (JAMA Article Information)

HEAD = re.compile(r"(?m)^###\s+(C\d+\.P\d+)\s*·\s*(.*?)\s*$")
SPAN = re.compile(r"·\s*[Ss](\d+)[a-z]*(?:\s+to\s+[Ss](\d+)[a-z]*)?\s*$")
BULLET = re.compile(r"(?m)^\s*-\s*B\d+\b")
REASON = re.compile(r"(?mi)^\s*(?:[-*]\s*)?reason:\s*(.+?)\s*$")


def _structure(plan_text: str) -> str:
    m = re.search(r"(?ms)^## 1 · Structure\b(.*?)(?=^## \d+ · |\Z)", plan_text or "")
    return m.group(1) if m else (plan_text or "")


def paragraphs(plan_text: str) -> list:
    """[(C1.P3, sentences, reason)] for each planned paragraph of §1, P0 (the title) left out."""
    body = _structure(plan_text)
    heads = list(HEAD.finditer(body))
    out = []
    for k, h in enumerate(heads):
        pid, rest = h.group(1), h.group(2)
        if pid.endswith(".P0"):
            continue
        block = body[h.end():heads[k + 1].start() if k + 1 < len(heads) else len(body)]
        block = re.split(r"(?m)^#{1,3}\s", block, maxsplit=1)[0]
        span = SPAN.search(rest)
        if span:
            a, b = int(span.group(1)), int(span.group(2) or span.group(1))
            n = b - a + 1
        else:
            n = len(BULLET.findall(block))
        reason = REASON.search(block)
        out.append((pid, n, reason.group(1) if reason else ""))
    return out


def exempt(kind: str) -> bool:
    """A Section the range does not hold for: the Abstract, an appendix or supplement, a letter, a response."""
    return (kind or "").strip().lower() in EXEMPT


def off_range(plan_text: str, kind: str = "", lo: int = RANGE[0], hi: int = RANGE[1]) -> list:
    """[(C1.P3, sentences, reason)] of the paragraphs outside lo..hi; [] for an exempt Section. A paragraph with a
    `reason:` is in the list (the page marks it as accepted), so callers decide: `[p for p in off if not p[2]]`
    are the ones to fix."""
    if exempt(kind):
        return []
    return [p for p in paragraphs(plan_text) if p[1] and not lo <= p[1] <= hi]


def section_kind(face_text: str) -> str:
    """The `section_kind:` a paper Section's face declares; "" for any other page (the rule then does not apply)."""
    m = re.search(r"(?m)^section_kind:\s*(\S.*?)\s*$", face_text or "")
    return m.group(1) if m else ""


# Two more plan patterns from ScalingGlucose (JL 261112), read by page.py health beside the paragraph row
BULLET_LINE = re.compile(r"(?m)^\s*-\s*B\d+\s*·\s*([Ss]\d+[a-z]*)\s*·\s*\[([^\]]+)\]\s*(.*)$")


def unsupported_expectations(plan_text: str) -> list:
    """[S3] for each `[Expect]` Bullet whose next line says `Evidence: none` (JL 261112: "do we really have evidence
    for this?"): an Introduction asks the question and cites the prior result; the answer is the Results'."""
    lines = (plan_text or "").splitlines()
    out = []
    for k, line in enumerate(lines):
        m = BULLET_LINE.match(line)
        if m and m.group(2).strip().lower() == "expect":
            nxt = next((x for x in lines[k + 1:k + 4] if x.strip().lower().startswith("evidence:")), "")
            if re.match(r"\s*evidence:\s*none\b", nxt, re.I):
                out.append(m.group(1))
    return out


def title_placeholder(plan_text: str) -> list:
    """[S0] for each `[Title]` Bullet that still holds a placeholder, not the title (JL 261112: "could you put the
    title here?")."""
    return [m.group(1) for m in BULLET_LINE.finditer(plan_text or "")
            if m.group(2).strip().lower() == "title"
            and re.search(r"(?i)^the paper'?s title|⟦|<[^>]+>", m.group(3).strip())]
