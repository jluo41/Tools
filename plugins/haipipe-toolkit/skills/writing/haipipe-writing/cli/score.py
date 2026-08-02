#!/usr/bin/env python3
"""Find the prose most likely to fail the weak-English test. Read-only.

    python3 score.py FILE [--section "## Content"] [--top 20]

It reports; it never rewrites. The point is to put a RANKED LIST in front of a
person before anything is touched, because the failure this catches is invisible
from the inside: an author reads their own jargon as plain language.

WHAT IT COUNTS, and what it deliberately does not
Three signals, all mechanical: house words this repo invented, long words, and
sentence length. It cannot judge whether a sentence is CLEAR, and it does not
try; a low score is not a pass. It is a worklist, and the judgment stays human.
"""
import argparse
import re
from pathlib import Path

# Words this repo invented or repurposed. A reader cannot look them up, and an
# author cannot see them, which is exactly why they need a list.
HOUSE = {
    "division", "apparatus", "drawer", "render", "renders", "managed", "span",
    "contract", "verdict", "axis", "axes", "stack", "unit", "frame", "variant",
    "fold", "folds", "roster", "protocol", "marker", "alias", "provenance",
    "deported", "cardinality", "extension", "consumer", "executor", "stake",
    "bearing", "on-stage", "lane", "digest", "gate", "harness", "dialect",
}
# Constructions that read as machine-written.
TELLS = [
    (r"\bis not (?:the thing|about|merely|simply)\b.{0,40}?\bit is\b", "the 'X is not Y, it is Z' turn"),
    (r"\bwhich is (?:why|what|how)\b", "'which is why' tacked onto a finished sentence"),
    (r"\bthat is (?:why|the|what)\b.{0,30},", "'that is why …,' as a hinge"),
    (r"\bnot only\b.{0,40}\bbut also\b", "'not only … but also'"),
    (r"\bIt (?:succeeds|works) when\b", "the banned house skeleton"),
    (r"\bThis (?:page|section) defines\b", "the banned house skeleton"),
    (r"\bThe hard part is\b", "the banned house skeleton"),
    (r"\bWithout that\b", "the banned house skeleton"),
]


def score_line(ln):
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", ln)
    if not words:
        return 0, []
    why = []
    house = sorted({w for w in words if w.lower() in HOUSE})
    longw = sorted({w for w in words if len(w) >= 12})
    n = len(words)
    s = 2 * len(house) + len(longw)
    if house:
        why.append("house words: " + ", ".join(house[:4]))
    if longw:
        why.append("long words: " + ", ".join(longw[:3]))
    if n > 32:
        s += 3
        why.append("%d words in one sentence" % n)
    elif n > 25:
        s += 1
        why.append("%d words" % n)
    for pat, name in TELLS:
        if re.search(pat, ln, re.I):
            s += 3
            why.append("AI tell: " + name)
    return s, why


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--section", help="limit to one `## Section`")
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--headings", action="store_true", help="score headings only")
    a = ap.parse_args()

    text = Path(a.file).read_text()
    if a.section:
        # LINE-anchored: `## Content` also appears inside figures and inside
        # prose that talks about the section, and matching those silently
        # scores the wrong span.
        m = re.search(r"^" + re.escape(a.section) + r"\s*$", text, re.M)
        if not m:
            raise SystemExit("✗ no section line matching %r" % a.section)
        j = text.find("\n## ", m.end())
        text = text[m.start():j if j > 0 else len(text)]
    # YAML frontmatter is machine-facing: `description:` is a discovery string
    # written long ON PURPOSE, so scoring it reports a defect that is not one.
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)          # figures are not prose
    text = re.sub(r"^> .*$", "", text, flags=re.M)              # records are not prose

    rows = []
    for i, ln in enumerate(text.splitlines(), 1):
        t = ln.strip()
        if not t or t.startswith(("|", "-", "*", "(")):
            continue
        is_head = t.startswith("#")
        if a.headings != is_head:
            continue
        s, why = score_line(re.sub(r"^#+\s*[\d.]*\s*·?\s*", "", t))
        if s >= 3:
            rows.append((s, i, t, why))
    rows.sort(reverse=True)
    kind = "headings" if a.headings else "sentences"
    print("%s · %d %s worth a second look\n" % (a.file.split("/")[-1], len(rows), kind))
    for s, i, t, why in rows[:a.top]:
        print("  %2d  L%-5d %s" % (s, i, t[:88]))
        print("          %s" % " · ".join(why))
    if not rows:
        print("  nothing flagged. That is a worklist being empty, not a verdict of clear.")


if __name__ == "__main__":
    main()
