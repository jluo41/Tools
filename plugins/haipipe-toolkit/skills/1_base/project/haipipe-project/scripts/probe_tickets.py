#!/usr/bin/env python3
"""Where does each moved Run ticket write its Result? A path-only probe that never runs the work.

    probe_tickets.py <project|world|Block> [--quiet]

For every ticket in one folder per Run (`runs/<run>/<run>.sh`), the probe runs only the ticket's lines up to
the line that sets its result folder (RESULTS_DIR, RESULT_DIR or HAIPIPE_RESULT_DIR; for a Discovery ticket
that hands its Task to a builder, TASK_DIR), with every line that could write dropped (mkdir, touch, rm, mv,
cp, exec, tee), under the ticket's own name and path, and prints where it lands:

    resolves   the ticket's own runs/<run>/result (or its Task folder)
    gated      the owner's own gate stopped it first (a BLOCKED message), before any path was set
    unexpected anything else: the ticket would write somewhere else, or could not find itself

The real ticket is set aside for the moment of the probe and put back. Exit 1 when any ticket is unexpected.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ASSIGN = re.compile(r'^\s*(export\s+)?(RESULTS?_DIR|HAIPIPE_RESULT_DIR)=')
TASK_ASSIGN = re.compile(r'^\s*(export\s+)?TASK_DIR=')
WRITES = re.compile(r"\s*(mkdir|touch|rm|mv|cp|exec|tee|ln|rsync)\b")
SKIP = {"_legacy", "_old", "result", "results", "passes", "notebooks"}


def tickets(path: Path) -> list[Path]:
    out = []
    for t in sorted(path.rglob("runs/*/*.sh")):
        if t.parent.name != t.stem or SKIP & set(t.relative_to(path).parts):
            continue
        out.append(t)
    return out


def probe(t: Path) -> tuple[str, str]:
    """(verdict, where) for one ticket."""
    text = t.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("#!"):
        return "skipped", "not a shell ticket"
    lines = text.splitlines()
    idx = [i for i, l in enumerate(lines) if ASSIGN.match(l)]
    want_task = False
    if not idx:
        idx = [i for i, l in enumerate(lines) if TASK_ASSIGN.match(l)][:1]
        if not idx:
            return "skipped", "no result-folder line"
        want_task = True
    # the HAIPIPE header sets HAIPIPE_RESULT_DIR first and RESULT_DIR from it: read through the last of the header
    cut = idx[-1] if "HAIPIPE_RESULT_DIR" in lines[idx[0]] and len(idx) > 1 else idx[0]
    keep = [l for l in lines[:cut + 1] if not WRITES.match(l)]
    echo = ('echo "__RD__=$TASK_DIR"' if want_task
            else 'echo "__RD__=${RESULTS_DIR:-${RESULT_DIR:-${HAIPIPE_RESULT_DIR:-}}}"')
    aside = t.parent / f".probe-orig-{t.name}"
    os.replace(t, aside)
    try:
        t.write_text("\n".join(keep) + "\n" + echo + "\n", encoding="utf-8")
        run = subprocess.run(["bash", str(t)], capture_output=True, text=True, timeout=60,
                             stdin=subprocess.DEVNULL, cwd=t.parent)
    except subprocess.TimeoutExpired:
        return "unexpected", "timed out"
    finally:
        os.replace(aside, t)
    m = re.search(r"__RD__=(.*)", run.stdout)
    got = m.group(1).strip() if m else ""
    want = t.parent.parent.parent if want_task else t.parent / "result"
    if got and (os.path.realpath(got) == os.path.realpath(want)
                or (not want_task and got.rstrip("/").endswith("/".join(t.parent.parts[-2:]) + "/result"))):
        return "resolves", got
    if not got and re.search(r"BLOCKED", run.stderr):
        return "gated", run.stderr.strip().splitlines()[-1][:160]
    return "unexpected", got or (run.stderr.strip().splitlines()[-1][:160] if run.stderr.strip() else "(nothing)")


def probe_all(path: Path, quiet: bool = False) -> dict[str, int]:
    counts = {"resolves": 0, "gated": 0, "unexpected": 0, "skipped": 0}
    for t in tickets(path):
        verdict, where = probe(t)
        counts[verdict] += 1
        if verdict == "unexpected" or (verdict == "gated" and not quiet):
            print(f"  {verdict:10} {t.relative_to(path)} → {where}")
    return counts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--quiet", action="store_true", help="list only the unexpected tickets")
    a = ap.parse_args()
    c = probe_all(a.path.resolve(), a.quiet)
    print(f"tickets: resolves {c['resolves']} · gated {c['gated']} · unexpected {c['unexpected']} · "
          f"skipped {c['skipped']}")
    return 1 if c["unexpected"] else 0


if __name__ == "__main__":
    sys.exit(main())
