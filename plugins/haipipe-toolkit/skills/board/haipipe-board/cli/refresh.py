#!/usr/bin/env python3
"""Re-measure every generated block on a board, in one command.

WHY THIS EXISTS, and it is a defect report on the rest of this folder. Three
generators write measured blocks onto pages, and `check.py` reports a block
older than its page. Nothing ran the generators. An automated complaint with no
automated fix is worse than neither: the warning count climbs, people learn to
scroll past it, and the checker stops being read at all.

So this is the fix half. It finds which generators apply to the board it is
given, runs each, and reports what moved.

    python3 refresh.py <board-dir>            run every applicable generator
    python3 refresh.py <board-dir> --check     say what WOULD run, change nothing

Deliberately NOT wired into `build.py`. Build renders; it is asserted to be
deletable and to leave a board byte-identical when the paper dialect is absent.
A build that silently rewrote page SOURCE would break that, and would also mean
a person could never look at a stale block on purpose. Refresh is a thing you
run, and `generated-block-stale` is what tells you to.
"""
import pathlib
import re
import subprocess
import sys
import time

CLI = pathlib.Path(__file__).resolve().parent
SKILLS = CLI.parents[2]                      # .../skills/
PAPER = SKILLS / "paper" / "haipipe-paper"

MARKER = re.compile(r"^# --- (\w+):begin \(generated\) ---$", re.M)


def applicable(board):
    """Which generators have something to do on this board, decided by evidence.

    A generator runs because the board HAS what it measures, never because a
    list somewhere says it should. That way a board that grows an evidence page
    starts getting an evidence block with nobody editing this file.
    """
    jobs = []
    pages = [p for p in board.rglob("*.md")
             if "/board/" not in str(p) and "/_archive/" not in str(p)]
    text = {p: p.read_text(errors="ignore") for p in pages}

    if any(re.search(r"(?m)^route:\s*(outward|inward)\s*$", t) for t in text.values()):
        jobs.append(("evidence", [sys.executable, str(CLI / "evidence.py"),
                                  str(board), "--write"],
                     "evidence roll-up and content"))

    # A unit roll-up applies wherever some family has more than one unit page.
    sys.path.insert(0, str(CLI))
    import dash                                                   # noqa: E402
    if dash.groups(board):
        jobs.append(("units", [sys.executable, str(CLI / "dash.py"),
                               str(board), "--write"], "unit roll-ups"))

    main = next((d for d in board.glob("S*-main") if d.is_dir()), None)
    if main and (PAPER / "section-stats.py").exists() and any(main.glob("S-Main-[0-9]*.md")):
        jobs.append(("form", [sys.executable, str(PAPER / "section-stats.py"),
                              str(main), "--dashboard"], "section form dashboard"))
    return jobs


def stale_blocks(board):
    """Every generated block on the board, tagged, so the report can be honest."""
    out = []
    for p in board.rglob("*.md"):
        if "/board/" in str(p) or "/_archive/" in str(p):
            continue
        for m in MARKER.finditer(p.read_text(errors="ignore")):
            out.append((p.name, m.group(1)))
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    board = pathlib.Path(args[0]).resolve()
    today = time.strftime("%y%m%d")
    before = stale_blocks(board)
    jobs = applicable(board)

    if not jobs:
        print(f"{board.name}: no generator has anything to measure here")
        sys.exit(0)
    print(f"{board.name}: {len(jobs)} generator(s) apply · "
          f"{len(before)} generated block(s) on disk\n")
    for tag, cmd, label in jobs:
        if "--check" in sys.argv:
            print(f"  · would run {label}")
            continue
        r = subprocess.run(cmd + [f"--date={today}"], capture_output=True, text=True)
        if r.returncode:
            print(f"  ❌ {label}\n{r.stderr.strip()[:400]}")
            continue
        head = [ln for ln in r.stdout.splitlines() if ln.strip()][:1]
        print(f"  ✅ {label:<28} {head[0].strip()[:60] if head else 'done'}")
    if "--check" in sys.argv:
        sys.exit(0)
    after = stale_blocks(board)
    print(f"\n{len(after)} generated block(s) after the run"
          + (f", up from {len(before)}" if len(after) != len(before) else ""))
    print("now rebuild the board so the rendered pages carry the new numbers")
