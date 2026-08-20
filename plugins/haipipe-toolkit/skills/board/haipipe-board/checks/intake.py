#!/usr/bin/env python3
"""❄️ Intake · is a frozen display still frozen against the CURRENT source?

    python3 checks/intake.py [--board DIR ...]

A display unit's `intake/manifest.yaml` exists so that staleness is COMPUTABLE
(`haipipe-plugin-display` §❄️): the unit copied its sources and recorded a
sha256, so anyone can ask whether the copy still matches what is on disk now.
Nothing asked.

JL 260819 caught it by reading: "things here is still the old way … check again to
see whether they are aligned semantically". The loop's phase ORDER changed that
day, and four of five figures on `QPw00-page-loop` still draw the old one. The
manifests already knew; no tool was looking.

TWO MANIFEST SHAPES, and only one was checkable:

    file: + source: + sha256    ✅ names the LIVE path, so a re-hash is possible
    path: + sha256 + takes:     ⚠️ names only the COPY, so the sha256 proves the
                                copy has not rotted and says NOTHING about the
                                original. This file resolves such rows by
                                basename and reports `unresolved` when it cannot.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parents[1]
SKILLS = ENGINE.parents[1]

_NEW = re.compile(r"-\s*file:\s*(\S+)\s*\n\s*source:\s*(\S+)\s*\n\s*sha256:\s*(\w+)")
_OLD = re.compile(r"-\s*path:\s*(\S+)\s*\n\s*sha256:\s*(\w+)")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


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


def audit(unit: Path):
    """-> (rows, shape) · one row per input: (name, verdict)."""
    man = unit / "intake/manifest.yaml"
    if not man.exists():
        return [("—", "no manifest")], "none"
    txt = man.read_text(encoding="utf-8", errors="replace")

    rows, shape = [], "new"
    for _copy, src, sha in _NEW.findall(txt):
        live = SKILLS / src
        if not live.exists():
            rows.append((src.split("/")[-1], "source GONE"))
        else:
            rows.append((src.split("/")[-1],
                         "match" if _sha(live) == sha else "CHANGED"))
    if rows:
        return rows, shape

    shape = "old"
    for path, sha in _OLD.findall(txt):
        copy = unit / path
        name = path.split("/")[-1]
        if not copy.exists():
            rows.append((name, "copy GONE"))
            continue
        if _sha(copy) != sha:
            rows.append((name, "COPY ROTTED"))
            continue
        live = _find_live(path)
        if live is None:
            rows.append((name, "unresolved: manifest names no source"))
        else:
            rows.append((name, "match" if _sha(live) == sha else "CHANGED"))
    return rows, shape


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", nargs="*", default=None)
    args = ap.parse_args()
    boards = [Path(b) for b in args.board] if args.board else \
        sorted(p for p in (SKILLS / "diagrams").iterdir() if p.is_dir())

    stale, unresolved, n = [], 0, 0
    for b in boards:
        units = sorted(b.rglob("display/*/README.md"))
        if not units:
            continue
        head = False
        for r in units:
            unit = r.parent
            rows, shape = audit(unit)
            bad = [x for x in rows if x[1] in ("CHANGED", "source GONE",
                                               "COPY ROTTED")]
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
                stale.append("%s: %s %s" % (unit.name, x[0], x[1]))
            unresolved += len(unk)

    print()
    print("%d display unit(s) audited" % n)
    if unresolved:
        print("⚠️  %d input(s) UNRESOLVED: the manifest froze a copy and named no "
              "source, so its staleness cannot be computed. That is the promise "
              "`haipipe-plugin-display` §❄️ makes and this shape cannot keep." % unresolved)
    if stale:
        print("🚨 %d input(s) CHANGED since the unit was frozen — the figure may "
              "now draw something that is no longer true:" % len(stale))
        for s in stale:
            print("   ", s)
        return 1
    if not unresolved:
        print("✅ every frozen intake still matches its source")
    return 0


if __name__ == "__main__":
    sys.exit(main())
