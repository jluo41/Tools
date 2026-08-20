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

THREE MANIFEST SHAPES, and until 260820 only two parsed:

    file: + source: + sha256    ✅ names the LIVE path, so a re-hash is possible
    path: + frozen_as: + sha256 ✅ `path:` is the LIVE source and `frozen_as:` the
                                copy, so BOTH can be re-hashed. This is what every
                                unit on the CMSRegBoard writes.
    path: + sha256 + takes:     ⚠️ names only the COPY, so the sha256 proves the
                                copy has not rotted and says NOTHING about the
                                original. This file resolves such rows by
                                basename and reports `unresolved` when it cannot.

⚠️ 260820: the two regexes demanded `sha256:` on the line DIRECTLY after
`path:`, so every manifest with `frozen_as:` in between parsed to ZERO rows and
the run still printed "✅ every frozen intake still matches its source". Five
units on one page were reported green over nothing at all. A checker that finds
no rows now SAYS so, per unit, and refuses to call the run green: silence and a
pass must never look the same. Found by the Display2 repair agent, which
re-hashed its inputs by hand after the tool said nothing.
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
_KEY = re.compile(r"^\s*(?:-\s*)?(path|file|source|frozen_as|sha256|glob):\s*(\S+)\s*$")


def _items(txt: str):
    """-> one dict per `- ` list item under sources:, keys we know only.

    A regex pair cannot do this: `takes: >-` puts prose between `path:` and
    `sha256:`, and prose is exactly where a line-adjacency rule breaks.
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

    A page's manifest writes `probe/PP01-.../proof/x.csv` (page-relative) and
    `tasks/R01_.../scripts/y.do` (project-relative), so resolution walks out
    from the unit and stops at the repo root.
    """
    out, p = [], unit.resolve()
    while True:
        out.append(p)
        if (p / "pyproject.toml").exists() or (p / ".git").exists():
            break
        if p.parent == p:
            break
        p = p.parent
    return out


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

    # ── the shape every unit on a project board writes: `path:` is LIVE,
    # `frozen_as:` is the copy, and both are re-hashable. Parsed by block, so
    # a `takes: >-` prose field between them changes nothing (260820).
    items = _items(txt)
    rows = []
    for it in items:
        if "frozen_as" not in it or "path" not in it or "sha256" not in it:
            continue
        sha, name = it["sha256"], it["frozen_as"].split("/")[-1]
        copy = unit / it["frozen_as"]
        if not copy.exists():
            rows.append((name, "copy GONE"))
            continue
        if _sha(copy) != sha:
            rows.append((name, "COPY ROTTED"))
            continue
        live = next((base / it["path"] for base in _project_roots(unit)
                     if (base / it["path"]).is_file()), None)
        if live is None:
            # PHI and server-only sources are legitimately absent on a laptop:
            # the copy is proven intact, the ORIGINAL simply cannot be reached
            # from here. That is not a pass and not a rot; it is unresolved.
            rows.append((name, "unresolved: source not reachable from here"))
        elif _sha(live) == sha:
            rows.append((name, "match"))
        elif it.get("derived") == "true" or \
                name != it["path"].split("/")[-1]:
            # A TRANSCRIPTION, not a byte copy: `spec-ladder.txt` is read OUT of
            # a .do script, so its sha was never the script's and a byte compare
            # would call every such row stale forever. The sha still proves the
            # copy is intact; the source's own drift needs a human read.
            rows.append((name, "unresolved: derived from %s, not a byte copy"
                         % it["path"].split("/")[-1]))
        else:
            rows.append((name, "CHANGED"))
    if rows:
        return rows, "frozen_as"

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
    if not rows:
        # 260820: five units read as green over ZERO parsed rows. Silence and a
        # pass must never look the same, so say WHICH of the two this is.
        items = _items(txt)
        if items and not any("sha256" in i for i in items):
            return ([("intake/manifest.yaml",
                      "NOT PINNED: %d source(s), no sha256 on any of them"
                      % len(items))], "unpinned")
        return [("intake/manifest.yaml", "UNPARSED: no input rows found")], "none"
    return rows, shape


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", nargs="*", default=None)
    args = ap.parse_args()
    boards = [Path(b) for b in args.board] if args.board else \
        sorted(p for p in (SKILLS / "diagrams").iterdir() if p.is_dir())

    stale, unresolved, n, rowsread = [], 0, 0, 0
    for b in boards:
        units = sorted(b.rglob("display/*/README.md"))
        if not units:
            continue
        head = False
        for r in units:
            unit = r.parent
            rows, shape = audit(unit)
            rowsread += len([x for x in rows
                             if not x[1].startswith(("UNPARSED", "NOT PINNED",
                                                     "no manifest"))])
            bad = [x for x in rows if x[1] in ("CHANGED", "source GONE",
                                               "COPY ROTTED")
                   or x[1].startswith(("UNPARSED", "NOT PINNED"))]
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
    print("%d display unit(s) audited · %d input row(s) read" % (n, rowsread))
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
    if not unresolved and rowsread:
        print("✅ every frozen intake still matches its source")
    elif not rowsread:
        print("🚨 ZERO input rows were read. This is NOT a pass: no manifest on "
              "these boards parsed, so nothing was checked at all.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
