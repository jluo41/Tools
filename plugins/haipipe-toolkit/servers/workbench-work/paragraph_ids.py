"""Give each paragraph of a page's own sections its invisible id, once (ref/cards.md §3 rule 5; JL 261116), so a
paragraph can carry marks and cards (workbench/page/element_marks/paragraph_cards.py).

    python paragraph_ids.py <page folder> [<page folder> ...]           show what it would add
    python paragraph_ids.py <page folder> ... --apply                   add it

A page's own sections are its face's `## Review Content`, `## Plan + Results`, `## Findings` and `## Design`, and the
`.md` files they bring in with `embed:` or `each:`. A paragraph is a run of plain text lines (no heading, list, table,
quote, fence, HTML or `key: value` line), or a one-line top-level list item (not a bold header item, not one with
sub-items: those read as cards already). Its id, ` <!-- id: pNN -->`, goes at the end of its last line; NN counts on
from the highest id the page already has, so an id is never reused or renumbered. `/hai-work update` runs it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OWN = re.compile(r"(?mi)^##\s+(review content|plan \+ results|findings|design)\s*$")
HAS = re.compile(r"<!--\s*id:\s*p(\d+)\s*-->")
ITEM = re.compile(r"^[-*+]\s+\S")                    # a top-level list item, one line
BOLD = re.compile(r"^[-*+]\s+\*\*.*\*\*\s*$")          # a header item (bold all through): it groups the items after it
NOT_PROSE = re.compile(r"^\s*(#|[-*+]\s|\d+[.)]\s|\||>|<|```|~~~|[A-Za-z][\w-]*:\s)")


def face_of(page: Path) -> Path | None:
    for name in (page.name + ".md", "board.md"):
        if (page / name).is_file():
            return page / name
    return None


def own_ranges(text: str) -> list:
    """[(start, end)] line ranges of the face's own sections, each up to the next `## ` heading."""
    lines, out = text.splitlines(), []
    for i, line in enumerate(lines):
        if OWN.match(line):
            j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
            out.append((i + 1, j))
    return out


def brought_in(page: Path, text: str, ranges: list) -> list:
    """The `.md` files an own section brings in with `embed:` or `each:`, inside the page's folder."""
    lines, files = text.splitlines(), []
    for a, b in ranges:
        for line in lines[a:b]:
            m = re.match(r"^(embed|each):\s*(\S.*?)\s*$", line)
            if m:
                for p in sorted(page.glob(m[2])):
                    if p.suffix == ".md" and p.is_file() and page.resolve() in p.resolve().parents:
                        files.append(p)
    return files


def mint(lines: list, a: int, b: int, next_n) -> int:
    """Add an id to each paragraph in lines[a:b] that has none; returns how many it added."""
    added, fence, i = 0, False, a
    while i < b:
        line = lines[i]
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
        if not fence and ITEM.match(line) and not BOLD.match(line) and not HAS.search(line) and not (
                i + 1 < b and re.match(r"^\s+\S", lines[i + 1])):      # a top-level item with no sub-items
            lines[i] = line.rstrip() + f" <!-- id: p{next_n():02d} -->"
            added += 1
            i += 1
            continue
        if fence or not line.strip() or NOT_PROSE.match(line):
            i += 1
            continue
        j = i
        while j + 1 < b and lines[j + 1].strip() and not NOT_PROSE.match(lines[j + 1]):
            j += 1
        if not any(HAS.search(lines[k]) for k in range(i, j + 1)):
            lines[j] = lines[j].rstrip() + f" <!-- id: p{next_n():02d} -->"
            added += 1
        i = j + 1
    return added


def run(page: Path, apply: bool) -> list:
    """[(file, paragraphs given an id)] for one page."""
    face = face_of(page)
    if face is None:
        return []
    text = face.read_text(encoding="utf-8")
    ranges = own_ranges(text)
    files = [(face, ranges)] + [(p, [(0, None)]) for p in brought_in(page, text, ranges)]
    texts = {f: f.read_text(encoding="utf-8") for f, _ in files}
    top = max([int(n) for t in texts.values() for n in HAS.findall(t)] or [0])
    counter = iter(range(top + 1, 10 ** 6))
    report = []
    for f, rs in files:
        lines = texts[f].splitlines()
        n = sum(mint(lines, a, len(lines) if b is None else b, lambda: next(counter)) for a, b in rs)
        if n:
            report.append((f, n))
            if apply:
                f.write_text("\n".join(lines) + ("\n" if texts[f].endswith("\n") else ""), encoding="utf-8")
    return report


def main(argv: list) -> int:
    apply = "--apply" in argv
    for arg in [a for a in argv if a != "--apply"]:
        for f, n in run(Path(arg).resolve(), apply):
            print(f"{'added' if apply else 'would add'} {n} paragraph id{'s' * (n != 1)}: {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
