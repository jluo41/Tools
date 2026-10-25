#!/usr/bin/env python3
"""Turn a text into the key clicks for the Chrome Remote Desktop on-screen keyboard.

Usage:
    key_plan.py SOURCE [--from-markdown] [--compare FILE] [--out-dir DIR]

SOURCE is a file path, or - for stdin. Writes two files to DIR (default: next to
SOURCE, or the current folder for stdin):

    <stem>.typed.txt   the exact text that will be typed (the check reads it)
    <stem>.plan.json   one entry per line: the text and its base-key clicks

--from-markdown is for text copied out of a rich-text editor (chat, a doc); it
refuses a code file, where "\\*" is real code. --compare FILE prints every line
where the text differs from FILE (the repository copy).

Every click names a BASE key (the unshifted label), so "$" is ["Shift", "4"].
The key refs are read once while the keyboard is unshifted and never change.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

BASE_ROWS = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
SHIFT_ROWS = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
NAMED = {" ": "Space", "\\": "Backslash"}
SMART = {"‘": "'", "’": "'", "“": '"', "”": '"', " ": " ", "–": "-", "—": "-"}
MD_SIGNS = re.compile(r"&#x?[0-9a-fA-F]+;|^\*[A-Z][A-Za-z-]+\*", re.M)
TEXT_SUFFIXES = {"", ".md", ".txt", ".markdown"}
PROBE_KEYS = {"Shift", "a", "4", "Backslash", "9", "[", "'", ";", "Space", "z", "/"}
PUNCT = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"


def base_key(ch):
    if ch in NAMED:
        return NAMED[ch]
    return ch


def clicks_for(ch):
    if ch in BASE_ROWS:
        return [base_key(ch)]
    if ch in SHIFT_ROWS:
        return ["Shift", base_key(BASE_ROWS[SHIFT_ROWS.index(ch)])]
    if ch == " ":
        return ["Space"]
    return None


def from_markdown(text):
    changes, suspects = [], []
    out, anchor = [], ""
    for n, line in enumerate(text.split("\n"), 1):
        before = line
        line = html.unescape(line)
        for k, v in SMART.items():
            line = line.replace(k, v)
        kept = []
        i = 0
        while i < len(line):
            if line[i] == "\\" and i + 1 < len(line) and line[i + 1] in PUNCT:
                kept.append(("lit", line[i + 1]))
                i += 2
            else:
                kept.append(("raw", line[i]))
                i += 1
        plain = "".join("\x00" if kind == "lit" else c for kind, c in kept)
        lits = [c for kind, c in kept if kind == "lit"]
        plain = re.sub(r"(?<![\w*])\*(?=\S)([^*\x00]*?\S)\*(?![\w*])", r"\1", plain)
        rebuilt = []
        it = iter(lits)
        for c in plain:
            rebuilt.append(next(it) if c == "\x00" else c)
        line = "".join(rebuilt)
        if line != before:
            changes.append((n, before, line))
        if before.startswith("*"):
            if line and not line[0].isspace() and anchor[:1].isspace():
                suspects.append((n, line))
        elif line.strip():
            anchor = line
        out.append(line)
    return "\n".join(out), changes, suspects


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--from-markdown", action="store_true")
    ap.add_argument("--compare")
    ap.add_argument("--out-dir")
    a = ap.parse_args()

    if a.source == "-":
        text, stem, out_dir = sys.stdin.read(), "stdin", Path(a.out_dir or ".")
    else:
        src = Path(a.source)
        text, stem, out_dir = src.read_text(encoding="utf-8"), src.stem, Path(a.out_dir or src.parent)
    text = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")

    if a.from_markdown and a.source != "-" and Path(a.source).suffix.lower() not in TEXT_SUFFIXES:
        print(f"STOP: --from-markdown is for pasted text, not a code file ({a.source}).")
        print("      A code file is typed as it is.")
        sys.exit(2)

    changes, suspects = [], []
    if a.from_markdown:
        text, changes, suspects = from_markdown(text)
    elif MD_SIGNS.search(text):
        print("WARNING: the text looks like Markdown source (&#x20; or a line starting *Cmdlet*).")
        print("         If it was copied from a rich-text editor, rerun with --from-markdown.")

    lines = text.split("\n")
    plan, bad = [], []
    for n, line in enumerate(lines, 1):
        keys = []
        for col, ch in enumerate(line, 1):
            k = clicks_for(ch)
            if k is None:
                bad.append(f"line {n} col {col}: {ch!r} (U+{ord(ch):04X}) has no key")
            else:
                keys += k
        plan.append({"n": n, "text": line, "keys": keys})

    if bad:
        print("STOP: these characters cannot be typed on the keyboard:")
        print("\n".join("  " + b for b in bad))
        sys.exit(2)

    out_dir.mkdir(parents=True, exist_ok=True)
    typed = out_dir / f"{stem}.typed.txt"
    typed.write_text(text + "\n", encoding="utf-8")
    needed = sorted({k for p in plan for k in p["keys"]} | {"Enter", "Backspace"} | PROBE_KEYS)
    total = sum(len(p["keys"]) for p in plan) + len(plan) - 1
    (out_dir / f"{stem}.plan.json").write_text(
        json.dumps({"lines": plan, "keys_needed": needed, "clicks": total}, indent=1), encoding="utf-8"
    )

    if changes:
        print(f"CLEANED {len(changes)} line(s) from Markdown:")
        for n, b, c in changes:
            print(f"  {n:>3} was: {b}")
            print(f"  {n:>3} now: {c}")
        print()
    if suspects:
        print("CHECK INDENT: these lines began with *Cmdlet* and lost their indent in the copy;")
        print("              the indent cannot be recovered. Use the original file as SOURCE:")
        for n, line in suspects:
            print(f"  {n:>3}| {line}")
        print()
    if a.compare:
        other = Path(a.compare).read_text(encoding="utf-8").replace("\r\n", "\n").rstrip("\n").split("\n")
        diffs = [(i + 1, x, y) for i, (x, y) in enumerate(zip(lines + [""] * len(other), other + [""] * len(lines)))
                 if i < max(len(lines), len(other)) and x != y]
        if diffs:
            print(f"DIFFERS from {a.compare} on {len(diffs)} line(s):")
            for n, x, y in diffs:
                print(f"  {n:>3} text: {x}")
                print(f"  {n:>3} file: {y}")
        else:
            print(f"SAME as {a.compare}, line for line.")
        print()
    print("TEXT TO TYPE:")
    for p in plan:
        print(f"  {p['n']:>3}| {p['text']}")
    print()
    print(f"{len(plan)} lines, {total} clicks, {len(needed)} distinct keys")
    print(f"typed text: {typed}")
    print(f"plan:       {out_dir / (stem + '.plan.json')}")


if __name__ == "__main__":
    main()
