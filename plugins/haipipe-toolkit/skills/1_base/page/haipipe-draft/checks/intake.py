#!/usr/bin/env python3
"""❄️ Intake · is a frozen display still frozen against the CURRENT source?

    python3 checks/intake.py [--board DIR ...]

A display unit's `intake/manifest.yaml` exists so that staleness is COMPUTABLE
(`workbench-page/ref/evidence/displays.md` §❄️): the unit copied its
sources into `intake/inputs/` and named where each came from, so anyone can ask
whether the copy still matches what is on disk now. Nothing asked.

JL 260819 caught it by reading: "things here is still the old way … check again to
see whether they are aligned semantically". The loop's Run ORDER changed that
day, and four of five figures on `QPw00-page-loop` still draw the old one. The
manifests already knew; no tool was looking.

NO CONTENT HASHES (JL 260928). A manifest names files; it never records a
sha256. The check compares the frozen copy with the live source directly:
byte-equal is `match`; otherwise the live source is `CHANGED` when it was
modified after the copy was frozen (file modification time). A manifest row
that still carries an old `sha256:` line is read the same way; the field is
ignored.

THREE MANIFEST SHAPES:

    file: + source:        names the LIVE path, relative to skills/
    path: + frozen_as:     `path:` is the LIVE source and `frozen_as:` the copy.
                           This is what every unit on the CMSRegBoard writes.
    path: only             names only the COPY. This file resolves such rows by
                           basename and reports `unresolved` when it cannot.

⚠️ 260820: the old regexes demanded one field on the line DIRECTLY after
`path:`, so every manifest with `frozen_as:` in between parsed to ZERO rows and
the run still printed "✅ every frozen intake still matches its source". Five
units on one page were reported green over nothing at all. A checker that finds
no rows now SAYS so, per unit, and refuses to call the run green: silence and a
pass must never look the same.
"""
from __future__ import annotations

import argparse
import filecmp
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")

# `sha256` stays readable so an old row's value never lands in another key;
# the value itself is ignored.
_KEY = re.compile(r"^\s*(?:-\s*)?(path|file|source|frozen_as|sha256|glob|derived):\s*(\S+)\s*$")


def _items(txt: str):
    """-> one dict per `- ` list item under sources:, keys we know only.

    A regex pair cannot do this: `takes: >-` puts prose between `path:` and the
    next field, and prose is exactly where a line-adjacency rule breaks.
    """
    items, cur = [], None
    for line in txt.splitlines():
        if re.match(r"^\s*-\s+\w+:", line):        # a new list item starts
            if cur:
                items.append(cur)
            cur = {}
        if cur is None:
            continue
        m = _KEY.match(line)
        if m and m.group(1) not in cur:              # first wins; prose cannot overwrite
            cur[m.group(1)] = m.group(2)
    if cur:
        items.append(cur)
    return items


def _project_roots(unit: Path):
    """-> the dirs a manifest's relative `path:` may be written against.

    A Page manifest writes `evidence/probe/PP01-.../proof/x.csv` (Page-relative) and
    `tasks/R01_.../scripts/y.do` (project-relative), so resolution walks out
    from the unit and stops at the repo root.
    """
    out, p, last_marker = [], unit.resolve(), None
    while True:
        out.append(p)
        if (p / "pyproject.toml").exists() or (p / ".git").exists():
            last_marker = len(out)               # keep walking: `examples/<proj>`
        if p.parent == p:                        # is a SUBMODULE and carries its
            break                                # own .git, so the FIRST marker is
        p = p.parent                             # the inner root, not the repo's
    return out if last_marker is None else out[:max(last_marker, len(out) - 1)]


def _verdict(copy: Path, live: Path) -> str:
    """-> `match` or `CHANGED`, from the two files themselves.

    Byte-equal is a match whatever the clocks say (a fresh checkout resets
    every file time). A copy that differs is stale only when its source was
    modified after the freeze; a source older than the copy means the copy was
    edited or re-frozen by hand, which a person reads, not a tool.
    """
    if filecmp.cmp(copy, live, shallow=False):
        return "match"
    if live.stat().st_mtime > copy.stat().st_mtime:
        return "CHANGED"
    return "unresolved: copy differs from its source but is newer than it"


def _find_live(name: str):
    """-> the live file a COPY came from, by basename, or None if ambiguous."""
    stem = name.split("/")[-1]
    # the copies rename `a/b/SKILL.md` to `haipipe-x.SKILL.md`
    m = re.match(r"^(haipipe-[\w-]+)\.(SKILL|CHANGELOG)\.md$", stem)
    if m:
        hits = list(SKILLS.glob("*/*/%s/%s.md" % (m.group(1), m.group(2))))
        return hits[0] if len(hits) == 1 else None
    hits = [p for p in SKILLS.rglob(stem)
            if "intake/inputs" not in str(p) and "_archive" not in str(p)]
    return hits[0] if len(hits) == 1 else None


def _glob_count(unit: Path, pattern: str):
    """-> how many files the manifest's glob finds NOW, or None if its root is
    not reachable from this machine (a PHI or server-only tree, legitimately)."""
    if "<" in pattern:                 # a placeholder root, e.g. <results>/...
        return None
    for base in _project_roots(unit):
        hits = list(base.glob(pattern))
        if hits:
            return len(hits)
    return None


def _frozen_as_row(unit: Path, it: dict):
    """One `path: + frozen_as:` row -> (name, verdict)."""
    name = it["frozen_as"].split("/")[-1]
    copy = unit / it["frozen_as"]
    if not copy.exists():
        return name, "copy GONE"
    if "glob" in it:
        # A glob has no single file to compare, so the freeze is a LISTING and
        # the staleness question is "did the SET move?". Re-resolve the
        # pattern and compare how many files it finds against how many
        # lines were frozen. Cheap, and it catches the drift that matters.
        n_live = _glob_count(unit, it["glob"])
        n_frozen = len([ln for ln in
                        copy.read_text(errors="replace").splitlines()
                        if ln.strip() and not ln.lstrip().startswith("#")])
        if n_live is None:
            return name, "unresolved: glob root not reachable from here"
        if n_live == n_frozen:
            return name, "match"
        return name, "CHANGED: glob finds %d, listing froze %d" % (n_live, n_frozen)
    live = next((base / it["path"] for base in _project_roots(unit)
                 if (base / it["path"]).is_file()), None)
    if live is None:
        # PHI and server-only sources are legitimately absent on a laptop:
        # the ORIGINAL simply cannot be reached from here. That is not a pass
        # and not a rot; it is unresolved.
        return name, "unresolved: source not reachable from here"
    if it.get("derived") == "true" or name != it["path"].split("/")[-1]:
        # A TRANSCRIPTION, not a byte copy: `spec-ladder.txt` is read OUT of
        # a .do script, so a byte compare would call every such row stale
        # forever. The source's own drift needs a human read; the file time
        # says whether there is anything to read.
        src = it["path"].split("/")[-1]
        if live.stat().st_mtime > copy.stat().st_mtime:
            return name, "unresolved: derived from %s, which was edited after the freeze" % src
        return name, "match"
    return name, _verdict(copy, live)


def audit(unit: Path):
    """-> (rows, shape) · one row per input: (name, verdict)."""
    man = unit / "intake/manifest.yaml"
    if not man.exists():
        return [("—", "no manifest")], "none"
    txt = man.read_text(encoding="utf-8", errors="replace")
    items = _items(txt)

    # ── the shape every unit on a project board writes: `path:` is LIVE,
    # `frozen_as:` is the copy. Parsed by block, so a `takes: >-` prose field
    # between them changes nothing (260820).
    rows = [_frozen_as_row(unit, it) for it in items
            if "frozen_as" in it and "path" in it]
    if rows:
        return rows, "frozen_as"

    rows = []
    for it in items:
        if "file" not in it or "source" not in it:
            continue
        src, copy = it["source"], unit / it["file"]
        live = SKILLS / src
        name = src.split("/")[-1]
        if not live.exists():
            rows.append((name, "source GONE"))
        elif not copy.exists():
            rows.append((name, "copy GONE"))
        else:
            rows.append((name, _verdict(copy, live)))
    if rows:
        return rows, "new"

    for it in items:
        if "path" not in it:
            continue
        path = it["path"]
        copy, name = unit / path, path.split("/")[-1]
        if not copy.exists():
            rows.append((name, "copy GONE"))
            continue
        live = _find_live(path)
        if live is None:
            rows.append((name, "unresolved: manifest names no source"))
        else:
            rows.append((name, _verdict(copy, live)))
    if rows:
        return rows, "old"
    # 260820: five units read as green over ZERO parsed rows. Silence and a
    # pass must never look the same, so say so.
    return [("intake/manifest.yaml", "UNPARSED: no input rows found")], "none"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", nargs="*", default=None)
    args = ap.parse_args()
    boards = [Path(b) for b in args.board] if args.board else \
        sorted(p for p in (SKILLS / "diagrams").iterdir() if p.is_dir())

    stale, unparsed, unresolved, n, rowsread = [], [], 0, 0, 0
    for b in boards:
        units = sorted(b.rglob("display/*/README.md"))
        if not units:
            continue
        head = False
        for r in units:
            unit = r.parent
            rows, shape = audit(unit)
            rowsread += len([x for x in rows
                             if not x[1].startswith(("UNPARSED", "no manifest"))])
            bad = [x for x in rows if x[1] in ("CHANGED", "source GONE")
                   or x[1].startswith("UNPARSED")]
            unk = [x for x in rows if x[1].startswith("unresolved")]
            n += 1
            if not bad and not unk:
                continue
            if not head:
                print("📋 %s" % b.name)
                head = True
            mark = "🚨" if bad else "⚠️"
            print("   %s %-38s %s shape · %d input(s)" % (mark, unit.name, shape, len(rows)))
            for name, verdict in bad + unk:
                print("        %-34s %s" % (name[:34], verdict))
            for x in bad:
                (unparsed if x[1].startswith("UNPARSED")
                 else stale).append("%s: %s %s" % (unit.name, x[0], x[1]))
            unresolved += len(unk)

    print()
    print("%d display unit(s) audited · %d input row(s) read" % (n, rowsread))
    if unresolved:
        print("⚠️  %d input(s) UNRESOLVED: the source cannot be reached from here, "
              "is named by no manifest row, or needs a human read (a derived "
              "copy whose source moved)." % unresolved)
    if unparsed:
        print("🚨 %d unit(s) cannot be checked AT ALL: no input row parsed, so a "
              "green run above would have meant nothing:" % len(unparsed))
        for s in unparsed:
            print("   ", s)
    if stale:
        print("🚨 %d input(s) CHANGED since the unit was frozen — the figure may "
              "now draw something that is no longer true:" % len(stale))
        for s in stale:
            print("   ", s)
    if stale or unparsed:
        return 1
    if not unresolved and rowsread:
        print("✅ every frozen intake still matches its source")
    elif not rowsread:
        print("🚨 ZERO input rows were read. This is NOT a pass: no manifest on "
              "these boards parsed, so nothing was checked at all.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
