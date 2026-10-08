#!/usr/bin/env python3
"""Audit the holes in a document: unowned placeholders, and dangling owners.

    python3 holes.py FILE [--dialect paper|board|plain]

Both directions, because half of this check is useless on its own:

    FORWARD   every hole has an owner   -> an unowned hole is never filled
    REVERSE   every owner is real       -> a hole that LOOKS owned is worse,
                                           because nobody goes looking for it

READ-ONLY. It reports where each hole is, what kind it is, and who owes it.
One writer takes the report and does the insertions (ref/holes.md §3).
"""
import argparse
import re
import sys
from pathlib import Path

# (name, hole pattern, owner-bracket pattern, owner-declaration pattern)
DIALECTS = {
    "paper": dict(
        holes=[(r"\\cite\{TOADD\}", "missing source"),
               (r"\{VAL:\?[^}]*\}", "missing number")],
        owner=r"\[(Q-[A-Za-z]+-\d+)\]",
        declares=r"(?:^|\s)(Q-[A-Za-z]+-\d+)\b",
    ),
    # The board's holes are its TYPED LANES, not an invented notation. QB4 §3.3.3
    # names eight, and maps three of them one-to-one onto the paper placeholders:
    #   📚 > Citation: ←→ \cite{TOADD}   🔢 > Value: ←→ {VAL:? …}   🖼 > Display: ←→ a display id
    # A lane that states what it is still WAITING for is a hole; a lane that
    # states what it found is not. `> Value: 9.1 months` is filled;
    # `> Value: {VAL:? median follow-up}` and `> Check: …` are owed.
    "board": dict(
        holes=[(r"^>\s*(?:Citation|Value|Display|Source|Link):\s*(?:\{VAL:\?|TOADD|\?|TBD)", "lane still owed"),
               (r"^>\s*Check:\s+\S", "unverified"),
               (r"^>\s*Q-consumer:\s+\S", "question owed"),
               (r"\{VAL:\?[^}]*\}", "missing number")],
        owner=r"\[([A-Z]{1,4}\d*[a-z]?(?:[.-][A-Za-z0-9.]+)?)\]",
        declares=r"^\s*[-*]\s*(?:\[.\]\s*)?[^\w]*\b([AP]\d+(?:\.\d+)?)\b",
    ),
    "plain": dict(
        holes=[(r"TODO\([^)]*\)", "todo"), (r"\bTBD\b", "unresolved")],
        owner=r"TODO\(([^)]+)\)",
        declares=r"(?!x)x",          # a plain host declares no owners
    ),
}


def audit(path, d):
    text = Path(path).read_text()
    lines = text.splitlines()
    cfg = DIALECTS[d]
    declared = set(re.findall(cfg["declares"], text, re.M))
    unowned, dangling = [], []
    for i, ln in enumerate(lines, 1):
        # A marker inside `backticks` is the notation being DESCRIBED, not a
        # hole. Without this every file that documents the grammar reports
        # itself as full of unowned holes, and a checker that cries wolf on its
        # own contract stops being read.
        ln = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), ln)
        for pat, kind in cfg["holes"]:
            for m in re.finditer(pat, ln, re.M):
                tail = ln[m.end():m.end() + 120]
                own = re.search(cfg["owner"], tail)
                if not own:
                    unowned.append((i, kind, ln.strip()[:88]))
                elif d != "plain" and own.group(1) not in declared:
                    dangling.append((i, own.group(1), ln.strip()[:88]))
    return unowned, dangling, len(declared)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--dialect", default="paper", choices=sorted(DIALECTS))
    a = ap.parse_args()
    unowned, dangling, ndecl = audit(a.file, a.dialect)

    print("%s · dialect %s · %d owner(s) declared\n" % (a.file.split("/")[-1], a.dialect, ndecl))
    if unowned:
        print("➡️  FORWARD · %d hole(s) with NO owner. Nobody will fill these." % len(unowned))
        for i, kind, ln in unowned:
            print("     L%-5d %-16s %s" % (i, kind, ln))
    if dangling:
        print("\n⬅️  REVERSE · %d hole(s) pointing at an owner that does not exist." % len(dangling))
        for i, who, ln in dangling:
            print("     L%-5d %-16s %s" % (i, who, ln))
    if not unowned and not dangling:
        print("✅ every hole has a real owner, in both directions.")
    sys.exit(1 if (unowned or dangling) else 0)


if __name__ == "__main__":
    main()
