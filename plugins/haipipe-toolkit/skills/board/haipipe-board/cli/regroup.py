#!/usr/bin/env python3
"""Move a board's root pages into one named folder per Q group (QA1, JL 260726).

    python3 regroup.py <board-dir>            # dry run, prints the plan
    python3 regroup.py <board-dir> --apply    # do it (git mv when tracked)
    python3 regroup.py --all <root>           # every board under root, dry run

The ruling is "one folder per group, on every board, from page one", so the
move has to be a command rather than a habit: a rule enforced by hand drifts the
first time somebody is in a hurry.

WHY THE FOLDER CARRIES A NAME. It is `<N>-Q<key>-<slug of the group title>`,
never a bare `QA/`. `QA/` writes the id a second time, and the id is already the
prefix of every filename inside; the group's SUBJECT is the half a reader cannot
recover from those filenames, so it is the half the folder name owes them.

WHY IT CARRIES A NUMBER (JL 260816). Letters carry identity and cannot carry
order: `QC-engine/` sorted four rows above `QPs-page-structure/` while board.md
read them the other way round, and a folder that contradicts the board it stores
is a folder nobody trusts. `N` is this group's position among board.md's `###`
headings, so the folder listing IS the reading order. `## Pages` stays the only
authority and `check.py` fails when the two disagree. This tool always numbers,
because it lays down the whole set at once; `＋Q`, which opens one folder into an
existing set, follows whatever the board already does.

WHAT IS DELIBERATELY NOT MOVED. A board whose folders are already its groups is
left alone, which is the paper `0-lifecycle/` case: `0-seed/ 1-work/ 3-display/`
are the subject folders AND the S families at once, and their numbers carry
lifecycle order that letters cannot. Satisfying the ruling is the point; looking
like a design board is not.

`## Pages` is never edited, because it lists bare filenames and always did.
That is the whole reason this is a `mv` and not a migration.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))

from src.common import page_files  # noqa: E402

HEAD = re.compile(r"^###\s+(Q[0-9A-Za-z]+)\s*·\s*(.+?)\s*$")


CAP = 30


def slug(text):
    """Slug the group title, cut at a word boundary near CAP.

    A title like "A task-folder: what it is, and running one" makes a 40-char
    folder that wraps in every listing it appears in, and the tail is where the
    least information is. Cutting at the last hyphen under CAP keeps the head,
    which is the part that distinguishes this group from its siblings.
    """
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(s) <= CAP:
        return s
    cut = s[:CAP].rsplit("-", 1)[0]
    return cut or s[:CAP]


def groups_of(board):
    """-> [(key, title, n)] from board.md's `### Q<key> · <title>` headings.

    `n` is the heading's 1-based position in READING order, which is the number
    the folder carries (JL 260816). It is captured before the sort below,
    because that sort is for MATCHING and would otherwise destroy the only
    ordering the board actually declares."""
    out = []
    for ln in (board / "board.md").read_text(encoding="utf-8").split("\n"):
        m = HEAD.match(ln.strip())
        if m:
            out.append((m.group(1), m.group(2), len(out) + 1))
    # longest key first, so QAa wins over QA on `QAa3-foo.md`
    return sorted(out, key=lambda g: -len(g[0]))


def plan(board):
    """-> (moves, skipped, note). Only ROOT pages move; nested ones are already home."""
    gs = groups_of(board)
    if not gs:
        return [], [], "no `### Q<key> · <title>` groups in board.md"
    roots = [p for p in page_files(board) if p.parent == board]
    if not roots:
        return [], [], "every page already lives in a folder"
    moves, skipped = [], []
    for p in sorted(roots):
        hit = next((g for g in gs if p.name.startswith(g[0])), None)
        if not hit:
            skipped.append((p.name, "matches no group key"))
            continue
        key, title, n = hit
        dest = board / f"{n}-{key}-{slug(title)}" / p.name
        (moves if not dest.exists() else skipped).append(
            (p, dest) if not dest.exists() else (p.name, "destination exists"))
    return moves, skipped, ""


def apply(moves):
    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "mv", str(src), str(dest)],
                           cwd=src.parent, capture_output=True)
        if r.returncode:                      # untracked, or not a repo
            src.rename(dest)


def run(board, do_it):
    board = Path(board).resolve()
    moves, skipped, note = plan(board)
    print(f"\n📋 {board.name}")
    if note:
        print(f"   {note}")
    by_dest = {}
    for src, dest in moves:
        by_dest.setdefault(dest.parent.name, []).append(src.name)
    for folder in sorted(by_dest):
        print(f"   {folder}/  ← {len(by_dest[folder])} pages")
    for name, why in skipped:
        print(f"   ⚠️  {name}: {why}")
    if moves and do_it:
        apply(moves)
        print(f"   ✅ moved {len(moves)}")
    elif moves:
        print(f"   (dry run: {len(moves)} would move; pass --apply)")
    return len(moves)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", help="a board folder, or a root with --all")
    ap.add_argument("--all", action="store_true",
                    help="every board.md under target")
    ap.add_argument("--apply", action="store_true", help="actually move")
    a = ap.parse_args(argv)
    root = Path(a.target).resolve()
    if not a.all:
        run(root, a.apply)
        return 0
    total = 0
    for bmd in sorted(root.rglob("board.md")):
        rel = bmd.parent.relative_to(root).as_posix()
        if any(s.startswith((".", "_")) for s in rel.split("/")):
            continue
        total += run(bmd.parent, a.apply)
    print(f"\n{total} pages {'moved' if a.apply else 'would move'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
