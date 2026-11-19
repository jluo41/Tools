"""List every constitution article under a root, or rerun each article's Run: check and report (haistack, JL 261118).

    python constitution.py [--root DIR] [--open]     list: id, rule, status
    python constitution.py [--root DIR] --reports    only require every **Report:** file
    python constitution.py [--root DIR] --check      rerun every **Run:** command, require every **Report:** file;
                                                     exit 1 if any fails

A Run: line is `**Run:** `<command>``; it runs from the root, and exit 0 means the rule holds.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP = (".git", "node_modules", "_old", ".trash", "references")


def articles(root: Path):
    """(file, head, status, run command or None) for every article."""
    for f in sorted(root.rglob("CONSTITUTION.md")):
        if any(p in f.relative_to(root).parts for p in SKIP):
            continue
        for art in re.split(r"(?m)^## (?=A\d+)", f.read_text(encoding="utf-8"))[1:]:
            head = art.splitlines()[0].strip()
            status = (re.search(r"(?m)^\*\*Status:\*\*\s*(.+)$", art) or [None, "?"])[1].strip()
            run = re.search(r"(?m)^\*\*Run:\*\*\s*`([^`]+)`", art)
            rep = re.search(r"(?m)^\*\*Report:\*\*\s*`?([^`\s]+)", art)
            report = (f.parent / rep[1]) if rep else None
            yield f, head, status, run[1] if run else None, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[6])
    ap.add_argument("--open", action="store_true", help="only articles whose Status is not solved")
    ap.add_argument("--check", action="store_true", help="rerun every Run: command")
    ap.add_argument("--reports", action="store_true", help="only require every Report: file (no Run lines)")
    a = ap.parse_args()
    if a.check and os.environ.get("HAISTACK_CHECKING"):
        print("a Run: line calls --check, which would run itself forever; use --reports")
        return 2
    a.check = a.check or a.reports
    root, last, broken = a.root.resolve(), None, 0
    for f, head, status, run, report in articles(root):
        if a.open and status.startswith("solved"):
            continue
        if f != last:
            print(f.relative_to(root).parent)
            last = f
        if not a.check:
            print(f"  {head:<60} {status}")
            continue
        if report is None or not report.is_file():
            broken += 1
            print(f"  ❗ {head}  (report missing: {report.relative_to(root) if report else 'no Report: line'})")
            continue
        if a.reports:
            print(f"  ✅ {head}  (report)")
            continue
        if run is None:
            print(f"  ⬜ {head}  (no Run: line; look at its Check)")
            continue
        try:
            r = subprocess.run(run, shell=True, cwd=root, capture_output=True, text=True, timeout=300,
                               env={**os.environ, "HAISTACK_CHECKING": "1"})
            ok, out = r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()
        except subprocess.TimeoutExpired:
            ok, out = False, ["timed out after 300 s"]
        broken += not ok
        print(f"  {'✅' if ok else '❗'} {head}")
        if not ok:
            print("     " + "\n     ".join(out[-8:] or ["(no output)"]))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
