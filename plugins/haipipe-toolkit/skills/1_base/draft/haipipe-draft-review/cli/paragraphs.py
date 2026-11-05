#!/usr/bin/env python3
"""How many sentences does each paragraph hold? Read-only (JL 261104: a paragraph is 4 to 6 sentences).

A file with `## Content` is read from that part only, where `####` starts a paragraph; any other file splits at
blank lines. Blocks under a `###` heading that matches --skip are left out: abstracts, conclusions and keywords.
Exit 1 when a paragraph falls outside the range. A count is a prompt to look, not a verdict.
"""
import argparse
import re
import sys
from pathlib import Path

NOT_AN_END = re.compile(r"\b(vs|et al|e\.g|i\.e|No|Dr|Mr|Ms|Fig|cf)\.")


def sentences(text: str) -> int:
    t = re.sub(r"\\(input|citep|cite|ref)\{[^}]*\}", "", text)
    t = NOT_AN_END.sub(r"\1", t)
    t = re.sub(r"(\d)\.(\d)", r"\1\2", t)            # 8.5
    t = re.sub(r"([<=] )\.(\d)", r"\1\2", t)         # P = .04
    return len(re.findall(r"[.?!][\"')\]]*(?:\s|$)", t))


def paragraphs(source: str, skip: re.Pattern):
    """Yield (label, text) for each paragraph, in order."""
    m = re.search(r"(?m)^## Content\s*$", source)
    if not m:
        for i, block in enumerate(re.split(r"\n\s*\n", source), 1):
            if block.strip() and not block.lstrip().startswith("#"):
                yield f"paragraph {i}", block
        return
    rest = source[m.end():]
    end = re.search(r"(?m)^## ", rest)
    body = re.sub(r"<!--.*?-->", "", rest[:end.start()] if end else rest, flags=re.S)
    section, label, buf = "", None, []

    def flush():
        return (label, " ".join(buf)) if label is not None and " ".join(buf).strip() and not skip.search(section) else None

    for line in body.splitlines():
        if line.startswith("### ") or line.startswith("#### "):
            done = flush()
            if done:
                yield done
            buf = []
            if line.startswith("### "):
                section, label = line[4:], None
            else:
                label = line[5:]
        elif label is not None:
            buf.append(line)
    done = flush()
    if done:
        yield done


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--min", type=int, default=4)
    ap.add_argument("--max", type=int, default=6)
    ap.add_argument("--skip", default=r"(?i)abstract|key points|keywords|conclusion|article information")
    a = ap.parse_args()
    skip, bad = re.compile(a.skip), 0
    for f in a.files:
        print(f)
        for label, text in paragraphs(Path(f).read_text(encoding="utf-8"), skip):
            n = sentences(text)
            off = n < a.min or n > a.max
            bad += off
            print(f"  {'❌' if off else '✅'} {n:2d} sentences  {label[:70]}")
    print(f"{bad} paragraph(s) outside {a.min} to {a.max} sentences")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
