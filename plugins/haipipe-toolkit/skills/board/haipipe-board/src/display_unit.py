#!/usr/bin/env python3
"""Where a display stage is, and where it ships to. Shared by the tools here.

WHY THIS EXISTS. All three tools in this folder derived both answers from
`Path(__file__)`, which is exactly why all three had to LIVE inside the stage
they operated on. They did: one copy each, inside one paper, and a `find` across
the whole repo returned exactly those. A second paper wanting displays had to
copy them by hand and then maintain a fork. The anchor is now an ARGUMENT, so
the tools live here once and the stage is named on the command line:

    <tool> [stage-dir] [--check]        stage-dir defaults to the working directory

The stage skill already wrote the call this way before the tools could take it:
`display/stage.md` declares `dashboard: display-report.py <this stage's dir>`.

THE PAPER ROOT is where `displays/`, `sections/` and the `.bib` live, and every
shipped path is written relative to it, because that is the directory LaTeX
compiles from. On a real paper it sits two levels above the stage, which is
`<paper>/0-lifecycle/<stage>/`. A stage with no paper above it, which is what a
SPECIMEN group is, carries its own root under `_fixture/`. That is not a new
idea here: the board engine spells the same arrangement `paper-root:` in
`board.md`, and resolves it as a plain join (`src/dialect_paper.py:1089`).
"""
import os
import re
import sys
from pathlib import Path, PurePosixPath

SECTION_PAGE = re.compile(r"(?m)^page-type:\s*section\s*$")


def stage_dir(argv=None):
    """The stage folder: the first non-flag argument, else the working directory."""
    args = [a for a in (sys.argv[1:] if argv is None else argv)
            if not a.startswith("-")]
    d = Path(args[0] if args else ".").resolve()
    if not d.is_dir():
        sys.exit(f"not a stage directory: {d}")
    return d


def paper_root(stage):
    """Where the shipped tree lives, and what every shipped path is relative to."""
    fixture = stage / "_fixture"
    if fixture.is_dir():
        return fixture
    return stage.parents[1]


def authoring_dir(stage):
    """The editing side: `display/`, with `workspace/` still accepted.

    BOTH names are accepted because the folder is being renamed (JL 260806) and
    a rename must not be able to arm the deletion path a second time. When an
    earlier hardcoded path stopped existing, the glob found zero source units,
    all 25 shipped files looked orphaned, and the next plain run would have
    unlinked every one of them; `--check` reported STALE and still exited 0, so
    nothing downstream could have stopped it either.
    """
    for name in ("display", "workspace"):
        cand = stage / name
        if cand.is_dir():
            return cand
    sys.exit(
        f"no editing folder in {stage}: expected `display/` or `workspace/`. "
        "REFUSING to run, because an empty source tree here means every "
        "shipped file looks orphaned and gets deleted.")


def units(ws):
    """Every unit: a direct child folder holding a float.tex, `_` names skipped.

    The selector was `glob("S-Display-*")`, which is one paper's page-naming
    convention rather than a rule about what a unit is. `float.tex` IS the rule:
    it is what makes a folder a unit, and it is what the build ships. Skipping
    `_` names keeps `_archive/` out, which the prefix form happened to miss only
    because that folder's own float.tex sits one level deeper than it looked.
    """
    return sorted(d for d in ws.iterdir()
                  if d.is_dir() and not d.name.startswith("_")
                  and (d / "float.tex").is_file())


def rel(path, root):
    """A path relative to the paper root, in LaTeX's forward-slash form.

    `os.path.relpath` and NOT `Path.relative_to`, because the two folders are
    not always nested the same way round. On a real paper the stage sits INSIDE
    the paper root, so the authoring folder is below it and either call works.
    A specimen stage carries its own root under `_fixture/`, so the authoring
    folder sits BESIDE that root rather than under it, and `relative_to` raises
    rather than walking up. `relpath` returns `../display/<unit>`, which is a
    path LaTeX resolves like any other.
    """
    return PurePosixPath(os.path.relpath(Path(path).resolve(),
                                         Path(root).resolve())).as_posix()


def section_pages(stage):
    """Every SECTION page that could point at a display, nearest first.

    There are two ways to be one and both are needed. A real paper files them
    as `S-Main-<n>-<slug>.md` in a sibling stage folder, which is a naming
    convention. The rule underneath that convention is the head key
    `page-type: section`, which is what the board's own type resolution reads
    (`board/haipipe-board/cli/check.py`, `check_page_type`) and which a page
    carries whatever it happens to be called. Matching the filename alone drops
    any page not named for one paper's convention; matching the key alone drops
    the live MISQ pages, which predate it.

    The search stops at the first folder that yields anything, so a stage that
    holds its own section pages never reaches out to its siblings. That is what
    keeps a SPECIMEN stage, which is its own paper, from scanning a whole board.
    """
    def found_in(d):
        out = []
        for f in sorted(d.glob("*.md")):
            head = f.read_text(encoding="utf-8", errors="replace")[:1200]
            if f.name.startswith("S-Main-") or SECTION_PAGE.search(head):
                out.append(f)
        return out

    here = found_in(stage)
    if here:
        return here
    for d in sorted(p for p in stage.parent.iterdir() if p.is_dir()):
        if d != stage and (out := found_in(d)):
            return out
    return []
