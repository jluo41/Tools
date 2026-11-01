"""All of a paper's displays as one PDF (JL 261101: "I also want a link for the display, so we can view all the
displays as one pdf file").

    python build_displays_pdf.py <paper Board>/<display Job>      e.g. …/Paper-X/j01_evidence_display

Reads the display Job's Tasks in order (main t01-t49, then appendix t50 on), finds each one's drawn file the way the
workbench does (the Task's own Run result, else the work Run its `made-by:` names, else its Section display unit),
and sets one page per display: its label and caption, then the picture or the table. A display not drawn yet gets a
page that says so. Writes <Board>/delivery/<display Job>/<job>-all-displays.pdf; rerun it after a display changes, never
edit the PDF. The workbench's Evidence view links to it. Compiled with xelatex, so the paper's own unicode prints.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
TOOLS = next(p for p in HERE.parents if (p / "plugins/haipipe-toolkit").is_dir())
sys.path[:0] = [str(TOOLS / "plugins/haipipe-toolkit/servers/_host")]
import live  # noqa: E402,F401  (grafts every server folder onto the live namespace)
from live import board_evidence as fd  # noqa: E402  (the one place that knows where a display's drawn file is)
from live.board_read import _field  # noqa: E402
from live.frame import face  # noqa: E402

HEAD = r"""\documentclass[11pt]{article}
\usepackage[letterpaper,margin=0.9in]{geometry}
\usepackage{fontspec}
\usepackage{graphicx,booktabs,tabularx,multirow,amsmath,amssymb,caption,float,xcolor,array,longtable}
\usepackage{newunicodechar}
\IfFontExistsTF{STIXGeneral}{\newfontfamily\pb{STIXGeneral}}{\newfontfamily\pb{Apple Symbols}}
\newunicodechar{⟦}{{\pb ⟦}}\newunicodechar{⟧}{{\pb ⟧}}
\pagestyle{plain}\setlength{\parindent}{0pt}
\begin{document}
"""


def tex(s: str) -> str:
    return re.sub(r"([&%$#_{}])", r"\\\1", s).replace("~", r"\textasciitilde{}").replace("^", r"\^{}")


def num(t: Path) -> int:
    return int(re.match(r"t(\d+)", t.name).group(1))


def page(task: Path) -> str:
    md = face(task)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    label = _field(text, "label") or task.name
    caption = _field(text, "caption")
    shown = fd._evidence_file(task, text)
    out = r"\clearpage" + "\n" + rf"{{\Large\bfseries {tex(label)}}}\par\smallskip" + "\n"
    out += rf"{{\small\color{{gray}} {tex(task.name)}}}\par\medskip" + "\n"
    if caption and not caption.startswith("⟦"):
        out += tex(caption) + r"\par\medskip" + "\n"
    if shown is None:
        return out + r"\emph{Not drawn yet.}" + "\n"
    if shown.suffix == ".tex":
        body = shown.read_text(encoding="utf-8", errors="ignore")
        body = re.sub(r"\\begin\{table\}(\[[^\]]*\])?", r"\\begin{table}[H]", body)
        return out + body + "\n"
    if shown.suffix.lower() in (".png", ".jpg", ".jpeg", ".pdf"):
        return out + (r"\begin{center}\includegraphics[width=\linewidth,height=0.8\textheight,keepaspectratio]{"
                      + str(shown) + r"}\end{center}" + "\n")
    return out + rf"\emph{{Drawn as {tex(shown.name)}, which a PDF cannot hold; open it in the workbench.}}" + "\n"


def build(job: Path) -> Path:
    job = job.resolve()
    tasks = sorted((t for t in job.glob("t[0-9]*_*") if t.is_dir()), key=num)
    board = job.parent
    title = (r"{\LARGE\bfseries " + tex(board.name) + r"}\par\medskip{\large All displays}\par\bigskip "
             + "".join(rf"{tex(_field((face(t).read_text(encoding='utf-8', errors='ignore') if face(t) else ''), 'label') or t.name)}"
                       rf" \quad {{\small\color{{gray}}{tex(t.name)}}}\par " for t in tasks))
    src = HEAD + title + "\n" + "".join(page(t) for t in tasks) + r"\end{document}" + "\n"
    out = board / "delivery" / job.name / f"{job.name}-all-displays.pdf"   # the Board owns delivery/ (haipipe-delivery)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / "all.tex").write_text(src, encoding="utf-8")
        for _ in range(2):
            r = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "all.tex"], cwd=d,
                               capture_output=True, text=True)
        if r.returncode != 0 or not (Path(d) / "all.pdf").is_file():
            sys.exit("xelatex failed:\n" + "\n".join(r.stdout.splitlines()[-25:]))
        out.write_bytes((Path(d) / "all.pdf").read_bytes())
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(build(Path(sys.argv[1])))
