"""Scaffold a new Block: `bNN_<slug>/board.md`, its face (haipipe-board, b03 s21, 261007).

A Block sits in a Project's Theme folder (work/, discovery/, cowork/, paper/, insight/, design/,
labeling/; the older plural names still read). The face carries the title line, its header fields (board-kind, spine, close, and an
optional workbench: naming the theme that reads it when the Theme folder names another), a Topic, and,
with --questions, an empty Questions register for haipipe-question. No empty folders are made: studio/,
reports/, runs/ and the Jobs come with their first content.

    python new_board.py <theme folder> --slug <topic> --title '<title>'
        [--nn NN] [--kind <board-kind>] [--spine '…'] [--close '…'] [--workbench <theme>]
        [--questions] [--dry-run]

It prints the new face's path. It refuses a folder or an NN that already exists.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# a Theme folder -> the board-kind its Blocks declare by default
KIND_OF = {"tasks": "task-block", "work": "task-block", "discoveries": "discovery-block",
           "discovery": "discovery-block", "cowork": "cowork-block", "designs": "design-board",
           "design": "design-board", "insights": "insight-board", "insight": "insight-board",
           "labelings": "labeling-board", "labeling": "labeling-board"}
SLUG = re.compile(r"^[a-z0-9][a-z0-9_]*$")


def taken(world: Path) -> set[int]:
    """The NNs already used by a bNN_ folder in this Theme folder."""
    out = set()
    for p in world.iterdir() if world.is_dir() else []:
        m = re.match(r"^b(\d+)_", p.name)
        if p.is_dir() and m:
            out.add(int(m.group(1)))
    return out


def face_text(nn: str, title: str, kind: str, spine: str, close: str, workbench: str, questions: bool) -> str:
    head = [f"# b{nn} · {title}", "", f"board-kind: {kind}",
            f"spine: {spine or '<one sentence naming the Block’s topic and boundary>'}",
            f"close: {close or '<what must be true for this Block to close>'}"]
    if workbench:
        head.append(f"workbench: {workbench}")
    body = ["", "## Topic", "", "<Why these Jobs belong to one Block, and what this Block excludes.>", ""]
    if questions:
        body += ["## Questions", "", "```yaml", "questions: []", "```", ""]
    return "\n".join(head + body)


def new_board(world: Path, slug: str, title: str, nn: int | None = None, kind: str = "", spine: str = "",
              close: str = "", workbench: str = "", questions: bool = False, dry_run: bool = False) -> Path:
    if not SLUG.match(slug):
        raise ValueError(f"slug {slug!r}: lower-case letters, digits and _ only")
    if not world.is_dir():
        raise ValueError(f"{world}: no such Theme folder")
    used = taken(world)
    nn = nn if nn is not None else (max(used) + 1 if used else 1)
    if nn in used:
        raise ValueError(f"b{nn:02d}_ is taken in {world.name}/")
    kind = kind or KIND_OF.get(world.name, "")
    if not kind:
        raise ValueError(f"{world.name}/ has no default board-kind: pass --kind")
    folder = world / f"b{nn:02d}_{slug}"
    if folder.exists():
        raise ValueError(f"{folder.name} exists")
    md = folder / "board.md"
    if not dry_run:
        folder.mkdir()
        md.write_text(face_text(f"{nn:02d}", title, kind, spine, close, workbench, questions), encoding="utf-8")
    return md


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("world", type=Path, help="the Theme folder, e.g. <Project>/tasks/")
    ap.add_argument("--slug", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--nn", type=int)
    ap.add_argument("--kind", default="")
    ap.add_argument("--spine", default="")
    ap.add_argument("--close", default="")
    ap.add_argument("--workbench", default="", help="the theme that reads this Block, if not its folder's")
    ap.add_argument("--questions", action="store_true", help="add an empty ## Questions register")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        md = new_board(a.world, a.slug, a.title, a.nn, a.kind, a.spine, a.close, a.workbench, a.questions, a.dry_run)
    except ValueError as err:
        print(f"refused: {err}", file=sys.stderr)
        return 2
    print(("would write " if a.dry_run else "") + str(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
