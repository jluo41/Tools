"""The venue template checklist catches a difference and passes a match (JL 261104)."""
import importlib.util
from pathlib import Path

import pytest

docx = pytest.importorskip("docx")
from docx.shared import Pt  # noqa: E402

SPEC = importlib.util.spec_from_file_location(
    "venue_template_check", Path(__file__).resolve().parents[1] / "scripts" / "venue_template_check.py")
check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check)


def make(path, title_size=20, abstract_spacing=1.5, heading="1 INTRODUCTION"):
    doc = docx.Document()
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(12)
    doc.styles["Normal"].paragraph_format.line_spacing = 2.0
    title = doc.add_paragraph("A Title", style="Title")
    title.runs[0].font.size = Pt(title_size)
    doc.add_paragraph("Abstract", style="Heading 1")
    doc.add_paragraph("Words.").paragraph_format.line_spacing = abstract_spacing
    doc.add_paragraph("Keywords: a, b").paragraph_format.line_spacing = abstract_spacing
    doc.add_paragraph(heading, style="Heading 1")
    doc.save(path)
    return path


def states(rows):
    return {r["rule"]: r["state"] for r in rows}


def test_a_match_passes(tmp_path):
    rows = check.word_rows(make(tmp_path / "t.docx"), make(tmp_path / "b.docx"))
    assert "differs" not in states(rows).values()


def test_each_difference_is_named(tmp_path):
    built = make(tmp_path / "b.docx", title_size=16, abstract_spacing=1.0, heading="INTRODUCTION")
    got = states(check.word_rows(make(tmp_path / "t.docx"), built))
    assert got["title size (pt)"] == got["abstract line spacing"] == got["keywords line spacing"] == "differs"
    assert got["major heading numbered"] == "differs"


def test_an_accepted_difference_stays_listed(tmp_path):
    built = make(tmp_path / "b.docx", title_size=16)
    got = states(check.word_rows(make(tmp_path / "t.docx"), built, accepted=("title size (pt)",)))
    assert got["title size (pt)"] == "accepted"


