"""preview_display.py writes float.pdf beside preview.pdf: float.tex alone, no header or page number, cropped tight."""
import importlib.util
import re
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "preview_display.py"
FLOAT = r"""\begin{figure}[H]
\centering
\rule{2in}{1in}
\caption{\textbf{A tiny figure.} Its caption, 95\% of it.}
\label{fig:tiny}
\end{figure}
"""


def _load():
    spec = importlib.util.spec_from_file_location("preview_display", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.skipif(not (shutil.which("pdflatex") or shutil.which("xelatex")), reason="no LaTeX engine")
def test_float_pdf_is_the_float_alone_cropped(tmp_path):
    pd = _load()
    if not (shutil.which("pdfcrop") or Path("/Library/TeX/texbin/pdfcrop").is_file()):
        pytest.skip("no pdfcrop")
    unit = tmp_path / "Display1-tiny"
    unit.mkdir()
    (unit / "float.tex").write_text(FLOAT, encoding="utf-8")
    preview = pd.bp.build(unit)
    assert preview.is_file()
    before = preview.read_bytes()
    out = pd.float_pdf(unit)
    assert out == unit / "float.pdf" and out.is_file()
    assert preview.read_bytes() == before                     # preview.pdf unchanged
    assert not list(unit.glob("float-only.*"))                # no build leftovers
    # one page, far smaller than a letter page: the float and its caption, cropped
    info = shutil.which("pdfinfo")
    if info:
        said = subprocess.run([info, str(out)], capture_output=True, text=True).stdout
        w, h = map(float, re.search(r"Page size:\s*([\d.]+) x ([\d.]+)", said).groups())
        assert re.search(r"Pages:\s*1\b", said) and w < 612 and h < 300, said


TABLE = r"""\begin{table}
\caption{\textbf{Fitted laws.} A wide table.}
\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}X r r}
Encoding & Points & E \\
Numbers & 114 & 0.0 \\
\end{tabularx}
\end{table}
"""


@pytest.mark.skipif(not (shutil.which("pdflatex") or shutil.which("xelatex")), reason="no LaTeX engine")
def test_a_page_float_table_keeps_its_name_and_number(tmp_path):
    # ScalingGlucose Extended Data Table 2 (261115): preview.tex set the table as a page float (`p`), which cannot sit
    # in float.pdf's tight box ("Not in outer par mode"); float.pdf reuses preview.tex's own lines, the float kept in
    # place, so its name and number match the preview
    pd = _load()
    unit = tmp_path / "Display2-table"
    unit.mkdir()
    (unit / "float.tex").write_text(TABLE, encoding="utf-8")
    (unit / "preview.tex").write_text(
        "\\documentclass{article}\\usepackage{tabularx}\\usepackage{float}\n\\begin{document}\n"
        "\\makeatletter\\renewcommand{\\fps@figure}{H}\\renewcommand{\\fps@table}{H}\\makeatother\n"
        "\\renewcommand{\\tablename}{Extended Data Table}\\renewcommand{\\thetable}{2}\n"
        "{\\makeatletter\\renewcommand{\\fps@table}{p}\\makeatother\\input{float.tex}}\n\\clearpage\nMethod page.\n"
        "\\end{document}\n", encoding="utf-8")
    out = pd.float_pdf(unit)
    assert out == unit / "float.pdf" and out.is_file()
    text = shutil.which("pdftotext")
    if text:
        said = subprocess.run([text, str(out), "-"], capture_output=True, text=True).stdout
        assert "Extended Data Table 2" in said and "Method page" not in said
