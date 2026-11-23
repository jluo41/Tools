"""round_adopt.py: a flat shared folder becomes a round, by moving (never copying away, never deleting) its files into
the agreed layout (ScalingGlucose-Board-v2 and Pp-AgreeableRx 261122: open-round refused, so sessions moved files and
wrote markers by hand).

    python word_round_folder.py adopt-round <flat-dir> --name <Name> --date MMDD [--round N]
                                            --file N=<file in it>:<kind> ... [--dry-run]

The folder itself is renamed RoundN-vMMDD (default N = 1, or the number it already has), inside its parent, which keeps
its SharePoint history. Each --file goes to the top as N-<Name>-vMMDD-<kind>.docx with Track Changes on, and a copy
of it as built goes to clean/; a PDF with the same stem goes to clean/ under the same number. A marked copy (its name
says "tracked") moves into track/, every other file into previous/, both as they came. track/ and submission/ are made empty. Each folder written gets its marker."""
from __future__ import annotations

import shutil
from pathlib import Path

from word_round_folder import ROUND, marker, track_on


def adopt_round(flat, name, mmdd, files, round_n=None, dry=False):
    flat = Path(flat)
    if not flat.is_dir():
        raise SystemExit(f"no folder {flat}")
    m = ROUND.match(flat.name)
    n = round_n or (int(m[1]) if m else 1)
    target = flat.parent / f"Round{n}-v{mmdd}"
    if target != flat and target.exists():
        raise SystemExit(f"{target.name} exists beside {flat.name}: choose --round")
    plan, used = [], set()
    for num, (src, kind) in sorted(files.items()):
        f = flat / src
        if not f.is_file() or f.suffix != ".docx":
            raise SystemExit(f"--file {num}: no Word file {src} in {flat.name}")
        stem = f"{num}-{name}-v{mmdd}-{kind}"
        plan.append((f, Path(f"{stem}.docx"), "top"))
        used.add(f.name)
        pdf = f.with_suffix(".pdf")
        if pdf.is_file():
            plan.append((pdf, Path("clean") / f"{stem}.pdf", "move"))
            used.add(pdf.name)
    for f in sorted(p for p in flat.iterdir() if p.is_file() and p.name not in used and not p.name.startswith(".")):
        plan.append((f, Path("track" if "tracked" in f.stem.lower() else "previous") / f.name, "move"))
    for p in sorted(p for p in flat.iterdir() if p.is_dir() and p.name not in ("previous", "track", "clean", "submission")):
        plan.append((p, Path("previous") / p.name, "move"))
    lines = [f"{flat.name} ─▶ {target.name}" + (" (dry run: nothing moved)" if dry else "")]
    lines += [f"  {src.name} ─▶ {dst.as_posix()}" + ("  (Track Changes on; a copy as built to clean/)" if how == "top" else "")
              for src, dst, how in plan]
    if dry:
        return target, lines
    for src, dst, how in plan:
        out = flat / dst
        out.parent.mkdir(exist_ok=True)
        if how == "top":
            (flat / "clean").mkdir(exist_ok=True)
            shutil.copy2(src, flat / "clean" / dst.name)
        src.rename(out)
        if how == "top":
            track_on(out)
    for sub in ("previous", "track", "clean", "submission"):
        (flat / sub).mkdir(exist_ok=True)
    if target != flat:
        flat.rename(target)
    for sub, why in (("previous", "Where this round started: the files the folder held before it became a round."),
                     ("track", "Marked copies of a working file, saved before any clean or replace."),
                     ("clean", "The LaTeX PDF and the LaTeX-made Word of each file, no marks.")):
        if any(p.is_file() and not p.name.startswith(".") for p in (target / sub).iterdir()):
            marker(target / sub, why)
    return target, lines
