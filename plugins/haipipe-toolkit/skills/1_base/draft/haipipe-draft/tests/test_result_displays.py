"""The web lane reads a Page's DISPLAY Results (must-check M-D18): results/re-display-<n>/result.yaml names its unit in
payload/, the unit's float.tex its \\label and caption, its README the name the text calls it. Each \\ref prints "Figure N"
(the number after the text's own "Fig."), and the unit is embedded once, its picture inlined. The Draft Lab server reads
the same module (servers/workbench/tests/test_draft_lab_support.py checks both give one answer). A display shows the
typeset float (page 1 of float.pdf, else preview.pdf cut to its float) with one line, its name and Run, never a
caption rebuilt in HTML."""
import base64
import struct
import sys
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ENGINE))
from src.page_workspace import create_page, render_page  # noqa: E402
from src import float_image  # noqa: E402
from src.float_image import alt_text, can_rasterize, float_png  # noqa: E402
from src.result_displays import ref_map, ref_words, result_units, run_name, web_figures  # noqa: E402


def paper_page(path: Path, header=True) -> Path:
    """A one-page letter PDF: a running header and page number in the bands, a figure (a filled box) and its caption."""
    ops = "0 0 0 rg 156 450 300 200 re f\nBT /F1 11 Tf 156 430 Td (Figure 1: A box. 95% of it.) Tj ET\n"
    if header:
        ops += "BT /F1 10 Tf 72 750 Td (DRAFT) Tj ET\nBT /F1 10 Tf 300 40 Td (1) Tj ET\n"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>", "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
            f"<< /Length {len(ops)} >>\nstream\n{ops}endstream", "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n".encode()
    x = len(out)
    out += (f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
            + b"".join(f"{o:010d} 00000 n \n".encode() for o in offs)
            + f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode())
    path.write_bytes(out)
    return path


def _size(png: Path) -> tuple:
    return struct.unpack(">II", png.read_bytes()[16:24])


@pytest.fixture(autouse=True)
def _cache(tmp_path, monkeypatch):
    monkeypatch.setattr(float_image, "CACHE", tmp_path / "_float-cache")


def _unit(folder: Path, n=1, label="fig:study", place="Figure 1", png=True):
    res = folder / "results" / f"re-display-{n}"
    unit = res / "payload" / f"Display{n}-study"
    (unit / "assets").mkdir(parents=True)
    (res / "result.yaml").write_text(f"item: E0{n}-DISPLAY-fig{n}\ntype: DISPLAY\nstatus: ready\n"
                                     "source: j01_display/t53_fair/runs/r21_pairs/result\n"
                                     f"payload:\n  unit: Display{n}-study\n")
    (unit / "float.tex").write_text("\\begin{figure}\n\\caption{\\textbf{Study design.} Two sources.}\n"
                                    f"\\label{{{label}}}\n\\end{{figure}}\n")
    (unit / "README.md").write_text(f"# Display{n}-study\n\n## Placement\n\n{place}\n")
    if png:
        (unit / "assets" / "figure.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    return unit


def test_units_refs_and_run(tmp_path):
    _unit(tmp_path)
    _unit(tmp_path, 2, "tab:edt1", "Extended Data Table 1", png=False)
    (tmp_path / "results" / "re-value-3").mkdir()
    (tmp_path / "results" / "re-value-3" / "result.yaml").write_text("item: E03-VALUE-x\ntype: VALUE\n")
    us = result_units(tmp_path)
    assert [u["shown"] for u in us] == ["Figure 1", "Extended Data Table 1"]
    assert us[0]["run"] == "t53 r21" and us[0]["alt"] == "Study design. Two sources."
    assert run_name("a/t01_q00/runs/r06_x/result") == "t01 r06"
    refs = ref_map(tmp_path)
    assert refs == {"fig:study": "Figure 1", "tab:edt1": "Extended Data Table 1"}
    assert ref_words("(Fig. \\ref{fig:study}) and \\ref{tab:edt1}; \\ref{fig:none}", refs) == \
        "(Fig. 1) and Extended Data Table 1; \\ref{fig:none}"


def test_a_payload_unit_outside_its_payload_is_skipped(tmp_path):
    _unit(tmp_path)
    y = tmp_path / "results" / "re-display-1" / "result.yaml"
    y.write_text(y.read_text().replace("unit: Display1-study", "unit: ../../../elsewhere"))
    assert result_units(tmp_path) == []


def test_web_page_prints_figure_and_embeds_it(tmp_path):
    original = tmp_path / "input.md"
    original.write_text("# Notes\n\nWe used 2,660 patients (Fig. \\ref{fig:study}).\n\nAgain \\ref{fig:study}.\n",
                        encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    _unit(page.folder)
    html = render_page(page)
    assert "\\ref{" not in html
    assert "(Fig. 1).</p>" in html and "Again Figure 1." in html
    assert html.count('class="page-display"') == 1
    assert "data:image/png;base64," in html and ">Figure 1 · t53 r21</figcaption>" in html
    assert "Two sources.</figcaption>" not in html                 # no caption rebuilt in HTML (M-D18)


def test_web_figures_without_units_leaves_the_page():
    html = "<p>See \\ref{fig:x}.</p>"
    assert web_figures(html, Path("/nonexistent")) == html


needs_raster = pytest.mark.skipif(not can_rasterize(), reason="no PyMuPDF and no pdftoppm")


@needs_raster
def test_preview_page_one_is_cut_to_its_float(tmp_path):
    unit = _unit(tmp_path)
    png = float_png(paper_page(unit / "preview.pdf"))
    assert png and float_image.CACHE in png.parents and unit not in png.parents   # cached outside the paper folder
    w, h = _size(png)
    # the 300 x 200 pt box and its caption line at 170 dpi; the whole page (with its header and page number) is
    # 1445 x 1870
    assert 700 <= w < 800 and 500 <= h < 620, (w, h)


@needs_raster
def test_a_float_pdf_wins_and_a_runs_float_pdf_too(tmp_path):
    unit = _unit(tmp_path)
    paper_page(unit / "preview.pdf")
    run = tmp_path / "j01_display" / "t53_fair" / "runs" / "r21_pairs" / "result"
    run.mkdir(parents=True)
    paper_page(run / "float.pdf", header=False)
    assert result_units(tmp_path)[0]["float"] == run / "float.pdf"
    paper_page(unit / "float.pdf", header=False)
    u = result_units(tmp_path)[0]
    assert u["float"] == unit / "float.pdf"
    assert _size(float_png(u["float"]))[0] > 1400               # a float.pdf is shown whole: it is cropped already


@needs_raster
def test_web_lane_embeds_the_typeset_float_and_its_run_line(tmp_path):
    original = tmp_path / "input.md"
    original.write_text("# Notes\n\nWe used 2,660 patients (Fig. \\ref{fig:study}).\n", encoding="utf-8")
    page = create_page(original, tmp_path / "page")
    unit = _unit(page.folder)
    (unit / "float.tex").write_text("\\begin{figure}\n\\caption{\\textbf{Study.} A 95\\% interval.}\n"
                                    "\\label{fig:study}\n\\end{figure}\n")
    png = float_png(paper_page(unit / "preview.pdf"))
    html = render_page(page)
    assert base64.b64encode(png.read_bytes()).decode() in html
    assert ">Figure 1 · t53 r21</figcaption>" in html
    assert "\\%" not in html and 'alt="Study. A 95% interval."' in html


def test_without_a_rasterizer_the_unit_picture_stands_in(tmp_path, monkeypatch):
    monkeypatch.setattr(float_image, "_fitz", lambda: None)
    monkeypatch.setattr(float_image, "_pdftoppm", lambda: "")
    unit = _unit(tmp_path)
    assert float_png(paper_page(unit / "preview.pdf")) is None
    html = web_figures("<p>See \\ref{fig:study}.</p>", tmp_path)
    assert "data:image/png;base64," + base64.b64encode(b"\x89PNG\r\n\x1a\n").decode() in html
    assert ">Figure 1 · t53 r21</figcaption>" in html


def test_alt_text_reads_latex_escapes_as_characters():
    assert alt_text("\\textbf{Gap.} A 95\\% interval; R\\&D, $n=5$~models\\,here") == "Gap. A 95% interval; R&D, n=5 models here"
