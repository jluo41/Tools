"""round_clean.py: a co-author who edited clean/'s Word instead of the working file (AgreeableJama-Board 261123:
Round2-v1120, a co-author left 29 tracked insertions, 18 deletions and 3 comments in clean/1-...-manuscript.docx,
the same name as the working file one folder down; a pull of the working file saw none of it).

    word_round.py take-clean <round-dir> <N> --clean N=<docx>[,<pdf>] [--dry-run]
    word_round.py clean-names <round-dir> [--dry-run]     an older clean/ named like the working files: add -clean

1. Refuse while either file is open in Word, or when clean/ holds no marks for file N.
2. Refuse when the working file has its own marks, comments or edits since its last synced point: both are listed
   and a person decides (settle N first, or merge by hand).
3. A marked copy of each into track/ (the working file's as always; clean/'s as ...-<kind>-clean-tracked-<stamp>.docx).
4. The working file's words are kept as settle's baseline (track/.placed-<N>.docx), the co-author's marked copy
   becomes the working file under its working name, Track Changes on: the next settle lists exactly their marks.
5. clean/ is refilled from --clean (the build, no marks); every marker is the tool's.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from word_round_folder import (CLEAN, PLACED, STAMP, changes, guard, in_use, last_seen, marker, marks, now, parse,
                               place_clean, track_on, working)


def counts(m: dict) -> str:
    return (f"{sum(m['ins'].values())} insertions, {sum(m['del'].values())} deletions, {len(m['comments'])} comments"
            f" by {', '.join(sorted(set(m['ins']) | set(m['del']) | {a for a, _ in m['comments']})) or 'nobody'}")


def edited(round_dir) -> list[tuple[Path, dict]]:
    """clean/ Word files that hold tracked changes or comments: a co-author edited the clean copy."""
    out = []
    for p in sorted((Path(round_dir) / "clean").glob("*.docx")):
        if p.name.startswith("~$"):
            continue
        m = marks(p)
        if m["changes"] or m["comments"] or sum(m["ins"].values()) or sum(m["del"].values()):
            out.append((p, m))
    return out


def take_clean(round_dir, n: int, clean=None, dry=False) -> list[str]:
    round_dir = Path(round_dir)
    top = working(round_dir).get(n)
    if top is None:
        raise SystemExit(f"no working file {n} at the top of {round_dir.name}")
    hit = [(p, m) for p, m in edited(round_dir) if parse(p) and parse(p)[0] == n]
    if not hit:
        return [f"clean/ holds no marks or comments for file {n}: nothing to take"]
    copy, cm = hit[0]
    for f in (top, copy):
        why = in_use(f)
        if why:
            raise SystemExit(f"{f.name}: {why}; close it in Word first (AutoSave writes over any outside change)")
    lines = [f"## {top.name}", "", f"clean/{copy.name}: {counts(cm)}"]
    base = last_seen(round_dir, n)
    own = changes(top, base) if base is not None else []
    tm = marks(top)
    if own or tm["changes"] or tm["comments"]:
        lines += [f"working file: {counts(tm)}; {len(own)} changes since its last synced point",
                  "refused: both files hold edits; settle the working file first, or merge the two by hand"]
        return lines
    if not clean and not dry:
        raise SystemExit(f"take-clean needs the build to refill clean/: --clean {n}=<docx>[,<pdf>]")
    stamp = f"{now():{STAMP}}"
    num, name, ver, kind = parse(top)
    keep_top = round_dir / "track" / f"{num}-{name}-v{ver}-{kind}-tracked-{stamp}.docx"
    keep_clean = round_dir / "track" / f"{copy.stem}-tracked-{stamp}.docx"
    if dry:
        return lines + [f"would save track/{keep_top.name} and track/{keep_clean.name}, make the co-author's copy "
                        f"the working file {top.name}, and refill clean/ from the build (dry run: nothing written)"]
    for dst in (keep_top, keep_clean):
        guard(dst, round_dir)
    keep_top.parent.mkdir(exist_ok=True)
    shutil.copy2(top, keep_top)
    shutil.copy2(copy, keep_clean)
    shutil.copyfile(top, round_dir / "track" / PLACED.format(n=n))   # their marks are listed against these words
    shutil.copy2(copy, top)
    track_on(top)
    copy.unlink()
    placed = place_clean(round_dir, top, clean, ver)
    marker(keep_top.parent, "Before anyone accepts changes or closes comments in a working file, a marked copy of "
                            "it is saved here first.")
    if not placed.is_file():
        lines.append(f"❗ clean/{placed.name} not placed: pass --clean {n}=<docx>[,<pdf>]")
    return lines + [f"saved: track/{keep_top.name}", f"saved: track/{keep_clean.name}",
                    f"working file: {top.name} holds the co-author's marks now, Track Changes on; "
                    f"settle {n} lists them", f"clean/: {placed.name} from the build"]


def clean_names(round_dir, dry=False) -> list[str]:
    """Rename an older clean/ (N-<Name>-vMMDD-<kind>.docx, the working file's own name) to ...-<kind>-clean, by moving
    within the folder (a move keeps a SharePoint file's history); the marker is the tool's."""
    cdir = Path(round_dir) / "clean"
    todo = [(p, p.with_name(f"{p.stem}{CLEAN}{p.suffix}")) for p in sorted(cdir.glob("*.*"))
            if parse(p) and not p.stem.endswith(CLEAN) and not p.name.startswith("~$")]
    lines = [f"clean/{a.name} → {b.name}" for a, b in todo] or ["clean/: every name ends -clean already"]
    if dry or not todo:
        return lines + (["(dry run: nothing moved)"] if dry and todo else [])
    for a, b in todo:
        if b.exists():
            raise SystemExit(f"clean/{b.name} exists beside {a.name}: keep one by hand")
        a.rename(b)
    marker(cdir, "The LaTeX PDF and the LaTeX-made Word of each file, no marks; rebuilt when the top changes.")
    return lines


__all__ = ["clean_names", "edited", "take_clean", "CLEAN"]
