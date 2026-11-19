"""Word table cells from LaTeX (ScalingGlucose ED Table 5, JL 261118: "how do you think the display of the word? it think
it should be better?"): a header is the rows above the first \\midrule only when they are few; a cell's math keeps its
exponents raised; a \\multicolumn{n}{l}{\\textbf{...}} panel title prints left and bold; \\textit prints italic."""
import importlib.util
import sys
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "scripts" / "latex_room_to_docx.py"

PANEL = ("\\begin{tabular}{lrrrrrrr}\n\\toprule\n"
         "\\multicolumn{8}{l}{\\textbf{Joint fit: $L = E + A N^{-\\alpha} + B D^{-\\beta}$}} \\\\\n"
         "Task & \\textit{E} & A & $\\alpha$ & B & $\\beta$ & $R^2$ & n \\\\\n"
         + "".join(f"t{i} & 1 & 2 & 3 & 4 & 5 & 6 & 7 \\\\\n" for i in range(8))
         + "\\midrule\n\\multicolumn{8}{l}{\\textbf{Data law}} \\\\\nt9 & 1 & 2 & 3 & 4 & 5 & 6 & 7 \\\\\n"
         "\\bottomrule\n\\end{tabular}\n")
SHORT = "\\begin{tabular}{lr}\n\\toprule\n\\multicolumn{2}{c}{Group} \\\\\nA & B \\\\\n\\midrule\nx & 1 \\\\\n\\end{tabular}\n"


@pytest.fixture(scope="module")
def m():
    spec = importlib.util.spec_from_file_location("docx_engine_cells", ENGINE)
    mod = importlib.util.module_from_spec(spec); sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_a_panel_above_the_first_midrule_is_not_a_header(m):
    assert m.count_header_rows(PANEL) == 1          # 10 rows above \midrule: a panel, so only row 0 is bold
    assert m.count_header_rows(SHORT) == 2          # a short head keeps both rows


def test_cell_math_keeps_exponents_raised(m):
    title = m.parse_table_rows(PANEL)[0][0]
    assert "\x10-α\x11" in title and "\x10-β\x11" in title   # raised by add_marked_runs, never "A N-α"


def test_left_panel_title_bold_and_italic_column_name(m):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    rows, spans = m.parse_table_rows(PANEL), m.parse_table_spans(PANEL)
    doc = Document()
    m.add_table(doc, m.Display(kind="table", block=PANEL, caption="x", label="", rows=rows, spans=spans,
                               header_rows=m.count_header_rows(PANEL)))
    t = doc.tables[0]
    title = t.cell(0, 0).paragraphs[0]
    assert title.alignment == WD_ALIGN_PARAGRAPH.LEFT and all(r.bold for r in title.runs if r.text.strip())
    assert any(r.font.superscript for r in title.runs)
    later = t.cell(10, 0).paragraphs[0]               # the second panel's title, a data-area row
    assert later.alignment == WD_ALIGN_PARAGRAPH.LEFT and [r for r in later.runs if r.text][0].bold
    e = [r for r in t.cell(1, 1).paragraphs[0].runs if r.text]
    assert e[0].text == "E" and e[0].italic and not e[0].bold   # a column name under a one-row head
    assert [r for r in t.cell(2, 0).paragraphs[0].runs if r.text][0].bold is not True  # data rows are not bold
    group = m.add_table(doc, m.Display(kind="table", block=SHORT, caption="y", label="", rows=m.parse_table_rows(SHORT),
                                       spans=m.parse_table_spans(SHORT), header_rows=2))
    assert doc.tables[1].cell(0, 0).paragraphs[0].alignment == WD_ALIGN_PARAGRAPH.CENTER   # {c} stays centred
