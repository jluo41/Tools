#!/usr/bin/env python3
"""QA3 · the round's gate, as one command.

Five conditions have to hold before an agent may tell a person that a round of
Board work is done. Until 260802 they were run by hand, as `build.py`, then
`check.py`, then a comparison against a warning count the agent remembered, and
nothing stopped a reply that skipped any of it.

    ① WRITTEN BACK  every change has a record on the page that owns it
    ② REBUILT       board.html came from the .md as it stands now
    ③ CHECKED       0 errors, and no page this round touched got a new warning
    ④ REACHABLE     the tab the person opens can run what shipped
    ⑤ STATED        the reply names which of ①-④ ran, with ③'s numbers

WHAT THIS COMMAND ANSWERS, and what it does not. ② and ③ are mechanical and it
runs them. ① and ④ need a judgment it cannot make: whether a change was
substantive, and whether the person's own browser tab has the new assets. It
prints them as unanswered rather than pretending, because a gate that reports a
condition it did not test is worse than no gate.

WHY THE BASELINE IS PER PAGE. Comparing the board's total warning count breaks
the moment a second session writes the same board, which happened three times
on 260802: the total moved 304 -> 276 while one page was being edited. So the
baseline records ONE COUNT PER PAGE, and the gate fails only on a page whose own
count rose. A concurrent session editing a different page cannot fail your
round, and a warning you introduced cannot hide behind someone else's cleanup.

    python3 cli/gate.py <board-dir> --start   # before the work
    python3 cli/gate.py <board-dir>           # after it; prints pass or fail
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

# Same home as the live layer's transient state (`live/base.py`'s TERM_DIR): a
# baseline is scratch, not a board record. Writing it into the board folder
# would put a second session's state where a reader looks for decisions, which
# is the shared-status-file mistake SKILL.md already forbids.
STATE_DIR = Path(os.environ.get("TMPDIR", "/tmp")) / "haiboard-gate"
FINDING = re.compile(r"^(\S+\.md)\b.*?\b(WARN|ERROR)\b")


def baseline_path(board: Path) -> Path:
    key = hashlib.sha1(str(board.resolve()).encode()).hexdigest()[:12]
    return STATE_DIR / f"{key}.json"


def run_check(board: Path):
    """Per-page warning counts, the error count, and the raw summary line."""
    out = subprocess.run(
        [sys.executable, str(HERE / "cli" / "check.py"), str(board)],
        capture_output=True, text=True).stdout
    pages, errors = {}, 0
    for line in out.splitlines():
        m = FINDING.match(line)
        if not m:
            continue
        if m.group(2) == "ERROR":
            errors += 1
        else:
            pages[m.group(1)] = pages.get(m.group(1), 0) + 1
    summary = next((l for l in reversed(out.splitlines()) if " · " in l and "warn" in l), "")
    return pages, errors, summary


def run_build(board: Path):
    r = subprocess.run(
        [sys.executable, str(HERE / "cli" / "build.py"), str(board)],
        capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]


def main(argv=None):
    ap = argparse.ArgumentParser(description="QA3's five-condition gate.")
    ap.add_argument("board", help="the board folder")
    ap.add_argument("--start", action="store_true",
                    help="record this round's per-page baseline and stop")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when the gate does not pass")
    args = ap.parse_args(argv)

    board = Path(args.board).resolve()
    if not (board / "board.md").is_file():
        print(f"not a board folder: {board}")
        return 2
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    store = baseline_path(board)

    if args.start:
        pages, errors, summary = run_check(board)
        store.write_text(json.dumps({"pages": pages, "errors": errors}), encoding="utf-8")
        print(f"baseline recorded for {board.name}: {summary or 'no summary'}")
        return 0

    built, build_tail = run_build(board)
    pages, errors, summary = run_check(board)

    before = {}
    if store.is_file():
        try:
            before = json.loads(store.read_text(encoding="utf-8")).get("pages", {})
        except Exception:
            before = {}

    risen = sorted(
        (name, before.get(name, 0), count)
        for name, count in pages.items() if count > before.get(name, 0)
    )

    ok_rebuilt = built
    ok_checked = errors == 0 and not risen
    passed = ok_rebuilt and ok_checked

    mark = lambda ok: "PASS" if ok else "FAIL"
    print(f"① WRITTEN BACK  not tested   a person decides what was substantive")
    print(f"② REBUILT       {mark(ok_rebuilt):11} {build_tail[0][:60]}")
    print(f"③ CHECKED       {mark(ok_checked):11} {summary}")
    if not store.is_file():
        print("                             no baseline; run --start next round")
    for name, was, now in risen:
        print(f"                             ↑ {name}: {was} -> {now}")
    print(f"④ REACHABLE     not tested   the person's own tab decides")
    print(f"⑤ STATED        yours        put ③'s numbers in the reply")
    print(f"\n{'gate passes' if passed else 'gate FAILS'} · "
          f"{'0 errors' if errors == 0 else f'{errors} errors'} · "
          f"{len(risen)} page(s) gained a warning")

    return 1 if (args.strict and not passed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
