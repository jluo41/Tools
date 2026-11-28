"""round_adopt.py: a flat shared folder becomes a round, by moving (never copying away, never deleting) its files into
the agreed layout (ScalingGlucose-Board-v2 and Pp-AgreeableRx 261122: open-round refused, so sessions moved files and
wrote markers by hand).

    python word_round_folder.py adopt-round <flat-dir> --name <Name> --date MMDD [--round N] [--into <paper-dir>]
                                            --file N=<file in it>:<kind> ... [--dry-run]

Without --into, the folder itself is RENAMED RoundN-vMMDD (default N = 1, or the number it already has), inside its
parent, which keeps its SharePoint history; only an old round folder (named RoundN-vMMDD or vMMDD) is renamed, any
other name is refused. With --into, the round is made inside <paper-dir> (Paper-FairGlucose-preprint 261123: a new
paper folder renamed to Round1-v1123 vanished), and <flat-dir>'s files move into it; <flat-dir> may be <paper-dir>
itself, whose RoundN-vMMDD folders stay where they are. The dry run prints the full target path. Each --file goes to the top as N-<Name>-vMMDD-<kind>.docx with Track Changes on, and a copy
of it as built goes to clean/; a PDF with the same stem goes to clean/ under the same number. A marked copy (its name
says "tracked") moves into track/, every other file into previous/, both as they came. track/ and submission/ are made empty. Each folder written gets its marker."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from word_round_folder import CLEAN, ROUND, marker, track_on


def adopt_round(flat, name, mmdd, files, round_n=None, dry=False, into=None):
    flat = Path(flat).resolve()
    if not flat.is_dir():
        raise SystemExit(f"no folder {flat}")
    m = ROUND.match(flat.name)
    n = round_n or (int(m[1]) if m and not into else 1)
    if into is None and not (m or re.fullmatch(r"v\d{4}", flat.name)):
        raise SystemExit(f"{flat.name} is not a round folder: adopt-round would rename it Round{n}-v{mmdd}. "
                         f"Pass --into <paper-dir> to make the round inside a paper folder")
    target = (Path(into).resolve() if into else flat.parent) / f"Round{n}-v{mmdd}"
    if target != flat and target.exists():
        raise SystemExit(f"{target} exists: choose --round")
    home = flat if into is None else target       # where the layout is built
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
            plan.append((pdf, Path("clean") / f"{stem}{CLEAN}.pdf", "move"))
            used.add(pdf.name)
    for f in sorted(p for p in flat.iterdir() if p.is_file() and p.name not in used and not p.name.startswith(".")):
        plan.append((f, Path("track" if "tracked" in f.stem.lower() else "previous") / f.name, "move"))
    keep = {"previous", "track", "clean", "submission"} if into is None else set()
    for p in sorted(p for p in flat.iterdir() if p.is_dir() and p.name not in keep and not ROUND.match(p.name)):
        plan.append((p, Path("previous") / p.name, "move"))
    how_made = (f"renamed {flat} ─▶ {target}" if into is None else f"made {target}, the files of {flat} moved into it")
    lines = [how_made + (" (dry run: nothing moved)" if dry else "")]
    lines += [f"  {src.name} ─▶ {dst.as_posix()}" + ("  (Track Changes on; a copy as built to clean/)" if how == "top" else "")
              for src, dst, how in plan]
    if dry:
        return target, lines
    home.mkdir(parents=True, exist_ok=True)
    for src, dst, how in plan:
        out = home / dst
        out.parent.mkdir(exist_ok=True)
        if how == "top":
            (home / "clean").mkdir(exist_ok=True)
            shutil.copy2(src, home / "clean" / f"{dst.stem}{CLEAN}.docx")
        src.rename(out)
        if how == "top":
            track_on(out)
    for sub in ("previous", "track", "clean", "submission"):
        (home / sub).mkdir(exist_ok=True)
    if home != target:
        flat.rename(target)
    for sub, why in (("previous", "Where this round started: the files the folder held before it became a round."),
                     ("track", "Marked copies of a working file, saved before any clean or replace."),
                     ("clean", "The LaTeX PDF and the LaTeX-made Word of each file, no marks.")):
        if any(p.is_file() and not p.name.startswith(".") for p in (target / sub).iterdir()):
            marker(target / sub, why)
    return target, lines
