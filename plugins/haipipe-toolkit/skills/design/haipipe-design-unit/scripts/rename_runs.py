#!/usr/bin/env python3
"""Rename a Design Folder's runs to the current names, once (JL 261001).

    rdNN_<step>_itemNN  ->  run-design-<step>-<MMDD>-design-<N>[-2]

`step` is commission, generate, verify or adopt. `MMDD` is the day the run started
(its receipt's started_at, else queued_at, else finished_at). A second run of the
same step, day and design gets `-2`, `-3`, in the old run-number order. The old run
number is kept as the ticket's `sequence:` line, so the order of runs is unchanged.

Every file and folder named after a run is renamed (the ticket, the result folder,
the frozen config), and every mention of an old name inside the Design Folder's
text files is rewritten, so tickets, receipts and verify targets keep pointing at
each other. Nothing else changes.

    python rename_runs.py <design-folder> [<design-folder> ...]          dry run
    python rename_runs.py --write <design-folder> [<design-folder> ...]  rename
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

OLD = re.compile(r"^rd(\d+)_(commission|generate|verify|adopt)_([a-z0-9][a-z0-9_-]*)$", re.I)
TEXT = {".yaml", ".yml", ".md", ".json", ".txt", ".csv", ".html"}


def _load(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _day(folder: Path, run: str) -> str:
    runtime = _load(folder / "results" / run / "runtime.yaml")
    decision = _load(folder / "results" / run / "decision.yaml")
    for value in (runtime.get("started_at"), runtime.get("queued_at"), runtime.get("finished_at"), decision.get("at")):
        hit = re.match(r"^\d{4}-(\d{2})-(\d{2})", str(value or ""))
        if hit:
            return hit.group(1) + hit.group(2)
    return "0000"


def _design(item: str, slug: str) -> str:
    hit = re.match(r"^ITEM0*(\d+)$", str(item or ""), re.I) or re.match(r"^item0*(\d+)$", slug, re.I)
    return f"design-{hit.group(1)}" if hit else re.sub(r"[^a-z0-9]+", "-", slug.lower()).strip("-")


def plan(folder: Path) -> list[tuple[str, str, int]]:
    """[(old, new, sequence)] for every old-named run in the folder, in run-number order."""
    tickets = sorted(((int(m.group(1)), p, m) for p in (folder / "runs").glob("rd*_*.yaml")
                      if (m := OLD.match(p.stem))), key=lambda t: t[0])
    taken = {p.stem for p in (folder / "runs").glob("run-design-*.yaml")}
    out = []
    for number, path, m in tickets:
        step, slug = m.group(2).lower(), m.group(3)
        base = f"run-design-{step}-{_day(folder, path.stem)}-{_design(_load(path).get('item'), slug)}"
        name, n = base, 1
        while name in taken:
            n += 1
            name = f"{base}-{n}"
        taken.add(name)
        out.append((path.stem, name, number))
    return out


def apply(folder: Path, pairs: list[tuple[str, str, int]]) -> int:
    """Rewrite mentions, add `sequence:`, then rename files and folders. Returns files changed."""
    if not pairs:
        return 0
    pattern = re.compile(r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(o) for o, _, _ in pairs) + r")(?![A-Za-z0-9_])")
    new_of = {o: n for o, n, _ in pairs}
    changed = 0
    for path in sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in TEXT):
        text = path.read_text(encoding="utf-8", errors="surrogateescape")
        fresh = pattern.sub(lambda m: new_of[m.group(1)], text)
        if fresh != text:
            path.write_text(fresh, encoding="utf-8", errors="surrogateescape")
            changed += 1
    for old, new, number in pairs:
        ticket = folder / "runs" / f"{old}.yaml"
        text = ticket.read_text(encoding="utf-8")
        if not re.search(r"(?m)^sequence:", text):
            text = re.sub(r"(?m)^(run: .*)$", rf"\1\nsequence: {number}", text, count=1)
            ticket.write_text(text, encoding="utf-8")
    # rename deepest first, so a folder is renamed after what it holds
    for path in sorted(folder.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        for old, new, _ in pairs:
            if path.name == old or path.name.startswith(old + "."):
                path.rename(path.with_name(new + path.name[len(old):]))
                break
    return changed


def main(argv: list[str]) -> int:
    write = "--write" in argv
    folders = [Path(a) for a in argv if a != "--write"]
    if not folders:
        print(__doc__)
        return 2
    for folder in folders:
        pairs = plan(folder)
        print(f"{folder.name}: {len(pairs)} runs")
        for old, new, number in pairs:
            print(f"  {old:30s} -> {new}  (sequence {number})")
        if write:
            print(f"  rewrote {apply(folder, pairs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
