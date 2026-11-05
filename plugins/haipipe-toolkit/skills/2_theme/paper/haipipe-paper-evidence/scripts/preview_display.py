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
import re
import sys
import time
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


def earlier_versions(unit: Path) -> list[dict]:
    """A display Run's earlier versions: the same Task's lower-numbered Runs that left a preview.pdf, newest first
    (the picture as that Run drew it). A unit that is not a Run's result/ has none. A Run card's `change:` says what
    changed; without one, its `says:`."""
    if unit.name != "result" or unit.parent.parent.name != "runs":
        return []
    number = lambda p: int(m.group(1)) if (m := re.match(r"r(\d+)_", p.name)) else -1
    here = number(unit.parent)
    out = []
    for run in sorted(unit.parent.parent.iterdir(), key=number, reverse=True):
        pdf = run / "result" / "preview.pdf"
        if not -1 < number(run) < here or not pdf.is_file():
            continue
        card = (run / "run.yaml").read_text(encoding="utf-8", errors="ignore") if (run / "run.yaml").is_file() else ""
        note = re.search(r"(?m)^change:\s*(.+)$", card) or re.search(r"(?m)^says:\s*(.+)$", card)
        stamp = run / "result" / "runtime.yaml"
        when = (stamp if stamp.is_file() else pdf).stat().st_mtime
        out.append({"pdf": pdf, "name": run.name, "date": time.strftime("%Y-%m-%d", time.localtime(when)),
                    "note": note.group(1).strip().strip("'\"").replace("''", "'") if note else ""})
    return out


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
    earlier = earlier_versions(unit)
    if master is None:
        print("note: no built paper yet (delivery/<writing Job>/latex/master.tex); page 1 uses the paper's default "
              "look. Build the paper (haipipe-paper-assemble), then rerun for its own head.")
        print(bp.build(unit, src, look="paper", earlier=earlier))
    else:
        print(f"page 1 uses the built paper's head (fonts, captions, header) from: {master}")
        print(bp.build(unit, src, preamble_from=master, earlier=earlier))


if __name__ == "__main__":
    main(sys.argv[1:])
