"""check_round.py: does a co-author round folder follow the agreed layout (ref/round-folder.md)? One ✅ or ❗ line per
rule; the exit code is the number of ❗ (JL 261122: "should we make the code to do this check? should we have the
check.py in the skill?", Pp-AgreeableRx-Discrention and ScalingGlucose-Board-v2 the same night).

    python check_round.py <RoundN-vMMDD>            one round
    python check_round.py <rounds-dir> --all        every child (--all before or after the path); a child not named RoundN-vMMDD is itself a ❗

Rules: 1 the top holds only working Word files named N-<Name>-vMMDD-<kind>.docx (the one form, JL 261122) · 2 previous/ track/ clean/ submission/ exist · 3 each
subfolder with files has one marker that lists them · 4 Track Changes on in every working file · 5 each working file
has its clean Word and PDF; submission/ holds only numbered slots · 6 previous/ keeps older versions; a submitted
submission/ is unchanged since it was frozen · 7 clean/ is the build: every name ends -clean, no Word file in it holds
tracked changes or comments (AgreeableJama 261123: a co-author edited clean/'s copy, named like the working file).
Reads only; writes nothing."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from word_round_folder import CLEAN, FROZEN, ROUND, parse, tracking  # noqa: E402

SUBS = ("previous", "track", "clean", "submission")
SKIP = (".", "~$", "last-update-")


def files(d: Path) -> list[Path]:
    return sorted(p for p in d.iterdir() if p.is_file() and not p.name.startswith(SKIP)) if d.is_dir() else []


KINDS = ("manuscript", "supplement", "cover-letter", "portal", "extended-data", "supplementary-information", "response")


def rename(p: Path, mmdd: str) -> str:
    """The one name form (JL 261122, "With version"): N-<Name>-vMMDD-<kind>.docx; the kind read from the name's end."""
    m = re.match(r"^(\d+)-(.+?)(?:-v\d{4})?\.docx$", p.name)
    if not m:
        return ""
    name, kind = m[2], next((k for k in KINDS if m[2].endswith("-" + k)), "")
    if kind:
        name = name[:-len(kind) - 1]
    return f"{p.name} → {m[1]}-{name}-v{mmdd}-{kind or ('manuscript' if m[1] == '1' else '<kind>')}.docx"


def check(r: Path) -> list[tuple[bool, str]]:
    out: list[tuple[bool, str]] = []
    m = ROUND.match(r.name)
    if not m:
        return [(False, f"{r.name}: not a round folder name (RoundN-vMMDD); start rounds with open-round or adopt-round")]
    mmdd = m[2]
    top = files(r)
    bad = [p.name for p in top if p.suffix != ".docx" or not parse(p) or p.stem.endswith(CLEAN)]
    nums = [parse(p)[0] for p in top if p.suffix == ".docx" and parse(p)]
    twice = sorted({n for n in nums if nums.count(n) > 1})
    out.append((not bad and not twice and bool(nums), "1 top: only numbered working Word files"
                + (f"; not one: {', '.join(bad)}" if bad else "") + (f"; number used twice: {twice}" if twice else "")
                + ("" if nums else "; no working file")))
    renames = [x for x in (rename(p, mmdd) for p in top if p.suffix == ".docx" and not parse(p)) if x]
    if renames:
        out.append((False, "1 rename to the one form: " + "; ".join(renames)))
    missing = [s for s in SUBS if not (r / s).is_dir()]
    out.append((not missing, "2 subfolders" + (f": missing {', '.join(s + '/' for s in missing)}" if missing else "")))
    for s in SUBS:
        fs = files(r / s)
        if not fs:
            continue
        marks = sorted((r / s).glob("last-update-*.txt"))
        unlisted = [p.name for p in fs if marks and p.name not in marks[-1].read_text(encoding="utf-8")]
        ok = len(marks) == 1 and not unlisted
        out.append((ok, f"3 {s}/ marker" + ("" if marks else ": none") + (f": {len(marks)} markers" if len(marks) > 1 else "")
                    + (f": not listed {', '.join(unlisted)}" if unlisted else "")))
    off = [p.name for p in top if p.suffix == ".docx" and parse(p) and not tracking(p)]
    out.append((not off, "4 Track Changes on" + (f": OFF in {', '.join(off)}" if off else "")))
    clean = {p.name for p in files(r / "clean")}
    lack = [f"{n} .{x}" for n in sorted(set(nums)) for x in ("docx", "pdf")
            if not any(c.startswith(f"{n}-") and c.endswith(f".{x}") for c in clean)]
    loose = [p.name for p in files(r / "submission") if not re.match(r"\d+-", p.name)]
    out.append((not lack and not loose, "5 clean/ per file, submission/ by slot"
                + (f"; clean/ lacks {', '.join(lack)}" if lack else "") + (f"; unnumbered in submission/: {', '.join(loose)}" if loose else "")))
    same = [p.name for p in files(r / "previous") if parse(p) and parse(p)[2] == mmdd]
    unnamed = [p.name for p in files(r / "previous") if not parse(p)]
    marks = sorted((r / "submission").glob("last-update-*.txt"))
    late, sent = [], bool(marks) and FROZEN in marks[-1].read_text(encoding="utf-8")
    if sent:
        frozen_at = marks[-1].stat().st_mtime
        late = [p.name for p in files(r / "submission") if p.stat().st_mtime > frozen_at + 60]
    out.append((not same and not late, "6 previous/ older versions; submission/ "
                + ("frozen since Submit" if sent else "not submitted yet, follows the build")
                + (f"; previous/ holds this round's v{mmdd}: {', '.join(same)}" if same else "")
                + (f"; changed after Submit: {', '.join(late)}" if late else "")
                + (f" (unnumbered, kept as they came: {', '.join(unnamed)})" if unnamed else "")))
    old = [f"{p.name} → {p.stem}{CLEAN}{p.suffix}" for p in files(r / "clean") if parse(p) and not p.stem.endswith(CLEAN)]
    from round_clean import counts, edited
    hit = [f"clean/{p.name} ({counts(m)}); take-clean {parse(p)[0]}" for p, m in edited(r) if parse(p)]
    out.append((not old and not hit, "7 clean/ is the build"
                + (f"; a co-author edited the clean copy: {'; '.join(hit)}" if hit else "")
                + (f"; rename: {'; '.join(old)}" if old else "")))
    return out


def report(r: Path) -> int:
    lines = check(r)
    print(f"## {r.name}")
    for ok, text in lines:
        print(f"{'✅' if ok else '❗'} {text}")
    return sum(not ok for ok, _ in lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("round", type=Path, help="a round folder; with --all, a rounds folder")
    ap.add_argument("--all", action="store_true", help="the path is a rounds folder: check every child")
    a = ap.parse_args(argv)
    a.round = a.round.resolve()   # "." names no round
    targets = sorted(p for p in a.round.iterdir() if p.is_dir() and not p.name.startswith(".")) if a.all else [a.round]
    bad = 0
    for t in targets:
        bad += report(t)
        print()
    return bad


if __name__ == "__main__":
    sys.exit(min(main(), 255))
