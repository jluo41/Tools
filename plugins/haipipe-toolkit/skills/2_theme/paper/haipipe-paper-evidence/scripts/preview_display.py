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

Beside it, float.pdf: float.tex alone in the same preamble, no header, no page number, no method pages, cropped tight by
pdfcrop: only the figure (or table) and its caption, the picture a workbench shows for the display. preview.pdf is
unchanged by it.
"""
from __future__ import annotations

import importlib.util
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
_spec = importlib.util.spec_from_file_location(
    "build_preview", SKILLS / "1_base" / "display" / "haipipe-display" / "scripts" / "build_preview.py")
bp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bp)


def board_of(unit: Path) -> Path | None:
    """The paper Board above the unit: the nearest folder named Paper-* or Grant-* that holds board.md."""
    return next((p for p in unit.parents if p.name.startswith(("Paper-", "Grant-")) and (p / "board.md").is_file()), None)


def paper_master(unit: Path) -> Path | None:
    board = board_of(unit)
    if board is None:
        return None
    own = next((p.name for p in unit.parents if p.parent == board and "_writing_" in p.name), None)
    if own and (board / "delivery" / own / "latex" / "master.tex").is_file():
        return board / "delivery" / own / "latex" / "master.tex"
    built = sorted((board / "delivery").glob("j*_writing_*/latex/master.tex"), key=lambda m: m.parts[-3])
    # the version's own build, not a variant of it (_springer, _si: another template or the supplement alone,
    # whose head may need a class file the preview cannot find; ScalingGlucose 261121)
    plain = [m for m in built if re.fullmatch(r"j\d+_writing_v\d+_[a-z0-9-]+", m.parts[-3])]
    return (plain or built)[-1] if built else None


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


def float_pdf(unit: Path) -> Path | None:
    """float.pdf beside preview.pdf: the unit's float.tex in preview.tex's own preamble (so the paper's fonts and
    caption style), set in a text-width box on a page cut to that box (LaTeX's preview package, tightpage: no header,
    no page number, a 4 pt border). Without that package, a full page cropped by pdfcrop (which needs Ghostscript).
    None, with a note, when neither works."""
    unit = Path(unit).resolve()
    head = (unit / "preview.tex").read_text(encoding="utf-8", errors="ignore").split(r"\begin{document}")[0]
    head = head.replace(bp.MARK, "")
    engine = "xelatex" if shutil.which("xelatex") else "pdflatex"
    if not shutil.which(engine):
        print("note: no LaTeX engine on PATH; float.pdf not written")
        return None
    # fit_page sets a page-sized float to `p`; a float cannot sit inside the tight box (a tabularx table, Extended Data
    # Table 2: "Not in outer par mode"), so float.pdf keeps every float in place (H)
    to_h = lambda t: re.sub(r"\\renewcommand\{\\fps@(figure|table)\}\{p\}", r"\\renewcommand{\\fps@\1}{H}", t)
    # the float exactly as preview.pdf set it: preview.tex's own lines from \begin{document} through its
    # \input{float.tex} (its name and number, "Extended Data Table 2"), never recomputed apart from it
    body = (unit / "preview.tex").read_text(encoding="utf-8", errors="ignore").split(r"\begin{document}", 1)[-1]
    upto = re.search(r"(?s)\A(.*?\\input\{float\.tex\}\}?)", body)
    here = to_h(upto.group(1).strip() + "\n") if upto else (
        "\\makeatletter\\renewcommand{\\fps@figure}{H}\\renewcommand{\\fps@table}{H}\\makeatother\n"
        + bp.numbering(unit) + to_h(bp.fit_page(unit)))
    tight = (head + "\\usepackage[active,tightpage]{preview}\\setlength\\PreviewBorder{4pt}\n\\begin{document}\n"
             "\\begin{preview}\\begin{minipage}{\\textwidth}\n" + here + "\\end{minipage}\\end{preview}\n\\end{document}\n")
    page = head + "\\begin{document}\n\\pagestyle{empty}\\thispagestyle{empty}\n" + here + "\\end{document}\n"
    crop = shutil.which("pdfcrop") or next((x for x in ("/Library/TeX/texbin/pdfcrop",) if Path(x).is_file()), None)
    stem, out, log = "float-only", unit / "float.pdf", ""
    try:
        for body, cut in ((tight, False), (page, True)):
            if cut and not crop:
                break
            (unit / f"{stem}.tex").write_text(body, encoding="utf-8")
            (unit / f"{stem}.aux").unlink(missing_ok=True)
            for _ in range(2):
                r = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error", f"{stem}.tex"], cwd=unit,
                                   capture_output=True, text=True)
            log = r.stdout
            if r.returncode != 0 or not (unit / f"{stem}.pdf").is_file():
                continue
            if not cut:
                shutil.move(str(unit / f"{stem}.pdf"), out)
                return out
            c = subprocess.run([crop, "--margins", "4", f"{stem}.pdf", "float.pdf"], cwd=unit, capture_output=True, text=True)
            if c.returncode == 0 and out.is_file():
                return out
            log = c.stdout + c.stderr
        print("note: float.pdf not written:\n" + "\n".join(log.splitlines()[-12:]))
        return None
    finally:
        for ext in (".tex", ".aux", ".log", ".out", ".pdf"):
            (unit / f"{stem}{ext}").unlink(missing_ok=True)


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
    print(float_pdf(unit) or "")


if __name__ == "__main__":
    main(sys.argv[1:])
