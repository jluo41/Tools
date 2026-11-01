"""One paper display's preview.pdf, page 1 as the paper prints it (JL 261101: "the full pdf preview, just like the one
we will see in the paper pdf").

    python preview_display.py <unit folder> [--method-from <source preview.pdf>]

The unit is a display Run's result/ under the Board's j01_evidence_display, or a writing Job's
tNN_<section>/display/Display<n>-<slug>/. The page head comes from the paper itself:

    1  the unit's own writing Job, if it sits in one:  <Board>/delivery/<that job>/latex/master.tex
    2  else the newest built writing Job:             <Board>/delivery/jNN_writing_v<MMDD>_<desk>/latex/master.tex
    3  else the paper's default look (haipipe-display build_preview.py --look paper), with a note to build the paper

Then haipipe-display scripts/build_preview.py writes preview.tex and compiles preview.pdf: page 1 the display (its
float.tex, with the paper's fonts, caption style, preamble.tex and header), pages 2 and on how it was made (method.md).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
_spec = importlib.util.spec_from_file_location(
    "build_preview", SKILLS / "1_base" / "display" / "haipipe-display" / "scripts" / "build_preview.py")
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)


def board_of(unit: Path) -> Path | None:
    """The paper Board above the unit: the nearest folder named Paper-* that holds board.md."""
    return next((p for p in unit.parents if p.name.startswith("Paper-") and (p / "board.md").is_file()), None)


def paper_master(unit: Path) -> Path | None:
    board = board_of(unit)
    if board is None:
        return None
    own = next((p.name for p in unit.parents if p.parent == board and "_writing_" in p.name), None)
    if own and (board / "delivery" / own / "latex" / "master.tex").is_file():
        return board / "delivery" / own / "latex" / "master.tex"
    built = sorted((board / "delivery").glob("j*_writing_*/latex/master.tex"), key=lambda m: m.parts[-3])
    return built[-1] if built else None


def main(argv: list[str]) -> None:
    src = None
    if "--method-from" in argv:
        i = argv.index("--method-from")
        if i + 1 >= len(argv):
            sys.exit(__doc__)
        src = Path(argv[i + 1])
        del argv[i:i + 2]
    if len(argv) != 1:
        sys.exit(__doc__)
    unit = Path(argv[0]).resolve()
    master = paper_master(unit)
    if master is None:
        print("note: no built paper yet (delivery/<writing Job>/latex/master.tex); page 1 uses the paper's default "
              "look. Build the paper (haipipe-paper-assemble), then rerun for its own head.")
        print(bp.build(unit, src, look="paper"))
    else:
        print(f"page 1 uses the built paper's head (fonts, captions, header) from: {master}")
        print(bp.build(unit, src, preamble_from=master))


if __name__ == "__main__":
    main(sys.argv[1:])
