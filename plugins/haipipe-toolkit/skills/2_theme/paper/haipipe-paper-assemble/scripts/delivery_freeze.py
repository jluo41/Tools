"""delivery_freeze.py: `build.py send <target>` and `build.py release <target>` (freeze, freeze_targets).
build_delivery.py runs this file inside its own namespace (_load_part), so ROOT, VERSION, HERE, OUT, PROFILE and rel
come from there.

A send's target is where the comments on it will collect: on the ladder the review Job on the Board,
jNN_review_<kind>_v<MMDD>/ (`send j31`, or its full name), whose face says `for:` this version; an older version's
comments report, <version>/reports/qNN_<kind>-<MMDD>/ (`send q02`); or an older Board's Round, RD<NN>-<...>/."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path


def _named(p: Path, rd: str) -> bool:
    return p.is_dir() and (p.name == rd or p.name.startswith(rd + "_"))


def _serves_this_version(job: Path) -> bool:
    """A review Job whose face names another version in `for:` is not this send's batch; one with no `for:` line is."""
    face = job / f"{job.name}.md"
    text = face.read_text(encoding="utf-8") if face.is_file() else ""
    said = re.search(r"(?m)^for:[ \t]*(\S.*?)\s*$", text)
    return not said or VERSION.name in said.group(1)


def freeze_targets(rd: str) -> list:
    """Every folder `rd` names: a Round, a version's comments report, or (on the ladder) a review Job of the Board."""
    rounds = list(ROOT.glob(f"B*-*-Round/{rd}-*")) + (list(VERSION.glob(f"{rd}-*")) if VERSION != ROOT else [])
    if VERSION != ROOT:                     # on the ladder: a comments report of this version (b16 Q05)
        rounds += [p for p in VERSION.glob("reports/q[0-9][0-9]_*") if _named(p, rd)]
        for job in ROOT.glob("j[0-9][0-9]_review_*"):       # the review Job this send collects into
            if _named(job, rd):
                if not _serves_this_version(job):
                    sys.exit(f"{job.name} is for another version (its face's for: line), not {VERSION.name}")
                rounds.append(job)
    return rounds


def freeze(kind: str, rd: str):
    """Cut one immutable Round snapshot from the current generated delivery.

    The Round contract is output-config driven: every declared output must be
    present, and the derived display register travels with the manifest. A
    partially populated destination is never repaired in place; a new Round
    (or an explicit human migration) is required.
    """
    try:   # 0.17.0: a --pdf-only build leaves Word behind its PDFs; a send carries one build
        if json.loads((HERE / OUT["manifest"]).read_text(encoding="utf-8")).get("pdf_only"):
            sys.exit("cannot freeze a --pdf-only build: its Word files are older than its PDFs; run a full build first")
        if json.loads((HERE / OUT["manifest"]).read_text(encoding="utf-8")).get("word_draft"):
            sys.exit("cannot freeze a --word-draft build: its displays were not placed by measuring; run a full build first")
    except (OSError, ValueError, KeyError):
        pass
    if kind not in {"sent", "released"}:
        sys.exit(f"invalid freeze target {kind!r}; expected sent or released")
    rounds = freeze_targets(rd)
    if len(rounds) != 1:
        sys.exit(f"expected one send target (a review Job, report or Round) for {rd}, found {len(rounds)}")

    dst = rounds[0] / kind
    if dst.exists():
        leftovers = [p for p in dst.iterdir() if p.name != ".gitkeep"]
        if leftovers:
            names = ", ".join(sorted(p.name for p in leftovers))
            sys.exit(f"{dst.relative_to(ROOT)} is immutable and already contains: {names}")
    dst.mkdir(parents=True, exist_ok=True)

    sources = []
    missing = []
    targets = set()
    no_supplement = str(PROFILE.get("appendices", "")).lower() == "main"
    for key, configured in OUT.items():
        if configured in ("", None):
            continue      # 0.9.0: an output switched off (e.g. section_snapshots = "") is not part of a Round
        if no_supplement and key.startswith("supplement_"):
            continue      # 0.9.0: appendices inside the manuscript (MISQ) produce no supplement file
        src = rel(configured)
        if not src.exists():
            missing.append(f"{key}: {configured}")
            continue
        target_name = src.name
        if target_name in targets:
            sys.exit(f"freeze output name collision: {target_name}")
        targets.add(target_name)
        sources.append((key, src))

    register = HERE / "display-register.md"
    if not register.exists():
        missing.append(f"display-register: {register.relative_to(ROOT)}")
    elif register.name in targets:
        sys.exit(f"freeze output name collision: {register.name}")
    else:
        sources.append(("display-register", register))

    if missing:
        sys.exit("cannot freeze an incomplete build; missing: " + "; ".join(missing))
    try:   # 0.9.0: say so when a letter that is not ready travels with the Round
        cover = json.loads((HERE / OUT["manifest"]).read_text(encoding="utf-8")).get("cover_letter")
    except (OSError, ValueError, KeyError):
        cover = None
    if cover and not cover.get("ready"):
        print("  ⚠ the cover letter is not ready: " + "; ".join(c["check"] for c in cover.get("checks", []) if not c["ok"]))

    for key, src in sources:
        target = dst / src.name
        if src.is_dir():
            shutil.copytree(src, target)
        else:
            shutil.copy2(src, target)
        print(f"  → {dst.relative_to(ROOT)}/{target.name} ({key})")
    print(f"{kind}/ frozen for {rounds[0].name}")
