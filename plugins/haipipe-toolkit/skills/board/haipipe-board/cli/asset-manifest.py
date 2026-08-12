#!/usr/bin/env python3
"""Write a generated provenance manifest into every 0-lifecycle/S05-display/display/S-Display-*/assets/README.md.

    python3 <skill>/cli/asset-manifest.py [stage-dir] [--check]

The stage directory defaults to the working directory. `src/display_unit.py` holds the
anchor rules and says why they are arguments rather than a hardcoded path: this
file used to require being run from one paper's root and to glob one paper's
`S-Display-*` naming, neither of which is a rule about what a unit is.

Why this is generated rather than hand-written: the same provenance claim was being
asserted in three hand-maintained places (float.tex header comments, the unit README,
the S-Display page) and drifted in all three. A hash can be re-checked against disk,
so it is the only form of the claim that cannot rot silently.

Two provenance KINDS, because assets arrive two ways:
  promoted  a figure copied from versions/ or candidates/. Byte-identity PROVES the source.
  generated a table body produced from source/ by a build step. Provenance is the input,
            and the useful check is whether the asset is older than that input.

--check exits non-zero if any asset is stale or untraceable, for use in a pre-submit sweep.
"""
import glob
import hashlib
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import display_unit as _stage                            # noqa: E402

BEGIN = "# --- manifest:begin (generated) ---"
END = "# --- manifest:end ---"
POOL_DIRS = ("versions", "candidates", "source")
# Files that live in source/ and are NOT inputs. The staleness test compares an
# asset against the newest thing in source/, and it counted these, so editing a
# rebuild note re-flagged an untouched figure. Measured on the live MISQ paper
# 260807: 16 staleness flags, of which 10 were a `REBUILD.md` and nothing else.
# A tool whose alarms are two-thirds false stops being read, which costs more
# than the check was ever worth.
SOURCE_DOCS = {"REBUILD.md", "README.md", "NOTES.md", "export.md"}
# `.gitkeep` exists to make git carry an empty directory. It is not an asset and
# has no provenance to trace.
NOT_AN_ASSET = {".gitkeep"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def stamp(path):
    # Local time, to match the mtimes quoted by hand on the S-Display pages.
    return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")


def human(n):
    return f"{n/1024:.0f} KB" if n < 1024 * 1024 else f"{n/1048576:.1f} MB"


def float_targets(unit, prefix):
    """Unit-relative paths that float.tex actually pulls in.

    `prefix` is the unit written the way FLOAT.TEX writes it, which is relative
    to the paper root, because that is the directory LaTeX compiles from. It
    used to be derived from `unit` itself and that worked only by accident: the
    script demanded being run from the paper root, so a relative `unit` and the
    paper's own frame were the same string. Once the tool moved out of the paper
    the two came apart, every target stopped matching its own prefix, and all 11
    units reported `float.tex DOES NOT POINT AT assets/`.
    """
    f = os.path.join(unit, "float.tex")
    if not os.path.exists(f):
        return None
    body = "".join(l for l in open(f) if not l.lstrip().startswith("%"))
    out = []
    for pat in (r"\includegraphics", r"\input"):
        i = 0
        while True:
            i = body.find(pat, i)
            if i < 0:
                break
            j = body.find("{", i)
            k = body.find("}", j)
            if j < 0 or k < 0:
                break
            p = body[j + 1:k].strip()
            out.append(p[len(prefix):] if p.startswith(prefix) else p)
            i = k
    return out


def describe(unit, prefix):
    """Return (lines, problems) for one unit's assets/."""
    assets = os.path.join(unit, "assets")
    pool = {}
    for d in POOL_DIRS:
        for f in sorted(glob.glob(os.path.join(unit, d, "*"))):
            if os.path.isfile(f):
                pool.setdefault(sha(f), []).append(os.path.relpath(f, unit))

    allsrc = [f for f in sorted(glob.glob(os.path.join(unit, "source", "*")))
              if os.path.isfile(f)]
    sources = [f for f in allsrc if os.path.basename(f) not in SOURCE_DOCS]
    docs = [f for f in allsrc if os.path.basename(f) in SOURCE_DOCS]
    gen = [f for f in sources if f.endswith((".py", ".sh", ".do", ".R"))]
    newest_source = max(sources, key=os.path.getmtime) if sources else None

    targets = float_targets(unit, prefix)
    lines, problems = [], []

    # The header claims assets/ holds what float.tex points at. Verify it rather than assert it:
    # a unit whose float reaches past assets/ into versions/ is the failure this catches.
    if targets is not None:
        outside = [t for t in targets if not t.startswith("assets/")]
        if outside:
            lines.append("  ⚠️ float.tex DOES NOT POINT AT assets/")
            for t in outside:
                lines.append(f"       it pulls in {t}")
            lines.append("       so the file the manuscript prints is NOT the selected artifact below.")
            lines.append("       Fix by promoting that file into assets/ and repointing float.tex there.")
            lines.append("")
            problems.append("float.tex points outside assets/: " + ", ".join(outside))

    for f in sorted(glob.glob(os.path.join(assets, "*"))):
        if not os.path.isfile(f):
            continue
        name = os.path.basename(f)
        if name == "README.md" or name in NOT_AN_ASSET:
            continue  # this manifest itself is not an asset
        digest = sha(f)
        match = pool.get(digest)
        lines.append(f"  assets/{name}")
        lines.append(f"    sha256 {digest[:16]}  ·  {human(os.path.getsize(f))}  ·  built {stamp(f)}")
        if match:
            lines.append(f"    kind   promoted")
            lines.append(f"    from   {', '.join(match)}  (byte-identical, so this is proven not asserted)")
        elif name.endswith(".tex"):
            lines.append(f"    kind   generated (table body; no version file is expected to match)")
            if newest_source:
                lines.append(f"    input  source/{os.path.basename(newest_source)}  ·  {stamp(newest_source)}")
            elif docs:
                # source/ holds a rebuild NOTE and no input. That is provenance
                # in prose: weaker than a hash, and not a defect. Reporting it
                # as "source/ is empty" was false, because the folder is not
                # empty and the origin IS written down, just not checkably.
                lines.append(f"    input  PROSE ONLY · {os.path.basename(docs[0])} "
                             f"says where this came from; nothing here can be hash-checked")
            else:
                lines.append(f"    input  UNRECORDED · nothing in source/ at all, so this table's origin is not traceable")
                problems.append(f"{name}: generated and source/ holds nothing")
        elif gen:
            # PRODUCED by a script in source/. Its bytes match no input because
            # a generator's output is not a copy of its input, so hash-identity
            # is the wrong test here and its absence is not a defect. Reporting
            # it as untraceable put five false alarms on the live paper.
            lines.append(f"    kind   generated by source/{os.path.basename(gen[0])}")
            if newest_source:
                lines.append(f"    input  source/{os.path.basename(newest_source)}  ·  {stamp(newest_source)}")
        elif docs:
            # PROSE provenance, for any asset kind and not just a .tex. A folded
            # or hand-made unit records where its artifact came from in a rebuild
            # note; that is weaker than a hash and it is not nothing. Calling it
            # untraceable told a reader the origin was unknown when it is written
            # down one folder away.
            lines.append(f"    kind   traceable by PROSE ONLY · "
                         f"source/{os.path.basename(docs[0])} says where it came from")
            lines.append(f"           nothing here can be hash-checked, so a change to the "
                         f"artifact cannot be detected mechanically")
        else:
            lines.append(f"    kind   UNTRACEABLE · matches no file in versions/, candidates/ or source/, and source/ holds no generator")
            lines.append(f"           either it was promoted from a file since deleted, or it was written straight into assets/")
            problems.append(f"{name}: untraceable")
        # A SAME-STEM TWIN of a used asset is not unused. `\includegraphics{figure}`
        # resolves either extension, and the .png beside a used .pdf is the raster
        # the board previews. Flagging it told a reader to delete the only file
        # the page can show.
        stem = os.path.splitext(name)[0]
        twin = targets is not None and any(
            os.path.splitext(os.path.basename(x))[0] == stem for x in targets)
        if targets is not None and f"assets/{name}" not in targets and not twin:
            lines.append(f"    ⚠️ UNUSED  float.tex does not reference this file")
            problems.append(f"{name}: in assets/ but float.tex does not use it")
        elif targets is not None and twin and f"assets/{name}" not in targets:
            lines.append(f"    twin of assets/{stem}.* which float.tex does use; "
                         f"kept as the previewable raster")
        # A PROMOTED asset's lineage is the CANDIDATE it is byte-identical to,
        # and that is proven rather than asserted. Its origin is not a file in
        # source/, so a source/ staleness test says nothing about it. On the
        # live MISQ paper this flagged `S-Display-1b`'s figure against
        # `source/prompt-E.md`, which is the spec for candidate E, the RUNNER-UP
        # that was never promoted; the shipped asset came from candidate H.
        # A folder that keeps every losing candidate's spec, which `for-design`
        # REQUIRES it to, would otherwise report its winner stale forever.
        if match:
            pass
        elif newest_source and os.path.getmtime(newest_source) > os.path.getmtime(f):
            lines.append(f"    ⚠️ STALE  source/{os.path.basename(newest_source)} is NEWER than this asset")
            problems.append(f"{name}: stale against source/")
        lines.append("")
    # PREVIEW AGAINST ASSET, which nothing checked until 260807. Every rule
    # above compares an asset with its INPUTS. None compared the asset with the
    # RENDER a person is shown, and that render is what rung ④ accepts. A stale
    # preview therefore let a person say yes to a picture that is no longer the
    # one the paper prints, which is the worst staleness this type can carry and
    # the only one the tool could not see. Found on the specimen itself.
    pv = os.path.join(unit, "preview.pdf")
    if os.path.exists(pv):
        live = [f for f in glob.glob(os.path.join(assets, "*"))
                if os.path.isfile(f) and os.path.basename(f) != "README.md"]
        newer = [f for f in live if os.path.getmtime(f) > os.path.getmtime(pv)]
        if newer:
            names = ", ".join(sorted(os.path.basename(f) for f in newer))
            lines.append(f"  ⚠️ PREVIEW IS STALE  assets/{names} is newer than preview.pdf")
            lines.append("       the render a person is shown is NOT the current asset;")
            lines.append("       recompile preview.tex from the PAPER ROOT before asking for rung ④.")
            lines.append("")
            problems.append("preview.pdf: older than the asset it renders")

    if not lines:
        lines = ["  (no files in assets/)", ""]
    return lines, problems


def main():
    check = "--check" in sys.argv
    stage = _stage.stage_dir()
    root = _stage.paper_root(stage)
    ws = _stage.authoring_dir(stage)
    today = datetime.now().strftime("%Y-%m-%d")
    all_problems = {}

    for unit_path in _stage.units(ws):
        unit = str(unit_path)
        if not os.path.isdir(os.path.join(unit, "assets")):
            continue
        unit_name = unit_path.name
        lines, problems = describe(unit, _stage.rel(unit_path, root) + "/")
        if problems:
            all_problems[unit_name] = problems

        block = [
            BEGIN,
            f"  ASSET PROVENANCE for {unit_name}, MEASURED {today}. GENERATED; do not hand-edit.",
            "  regenerate: python3 <skill>/cli/asset-manifest.py <stage-dir>",
            "",
            "  assets/ holds the SELECTED artifact that float.tex points at.",
            "  versions/ and candidates/ hold the lineage. Promote by copying a winner over the",
            "  asset path; never repoint float.tex into versions/.",
            "",
        ] + lines + [END]

        readme = os.path.join(unit, "assets", "README.md")
        head = [f"# {unit_name} · assets", "",
                "The files float.tex actually points at. Provenance below is measured, not asserted:",
                "a `promoted` asset is byte-identical to the lineage file named for it.", ""]
        if os.path.exists(readme):
            old = open(readme).read()
            if BEGIN in old and END in old:
                pre = old.split(BEGIN)[0]
                post = old.split(END)[1]
                new = pre + "\n".join(block) + post
            else:
                new = old.rstrip() + "\n\n" + "\n".join(block) + "\n"
        else:
            new = "\n".join(head + block) + "\n"
        with open(readme, "w") as fh:
            fh.write(new)
        print(f"wrote {readme}")

    if all_problems:
        print("\nPROBLEMS")
        for unit, ps in all_problems.items():
            for p in ps:
                print(f"  {unit}  {p}")
        if check:
            sys.exit(1)
    else:
        print("\nno problems: every asset is traceable and none is stale")


if __name__ == "__main__":
    main()
