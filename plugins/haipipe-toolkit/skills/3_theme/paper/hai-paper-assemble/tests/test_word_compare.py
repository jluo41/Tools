"""word_compare.py: is the co-authors' Word file the same as the build (AgreeableJama-Board 261122)."""
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import word_compare as wc  # noqa: E402


def para(doc, *parts):
    """parts: plain strings, or ("sup", text) for a superscript run."""
    p = doc.add_paragraph()
    for part in parts:
        if isinstance(part, tuple):
            p.add_run(part[1]).font.superscript = True
        else:
            p.add_run(part)
    return p


def paper(path, intro_cites=("1", "2", "3"), title="Opioid Prescribing and Agreeableness", extra=None):
    doc = Document()
    p = para(doc, title)
    para(doc, "Ada Lovelace, MS", ("sup", "1,2"), "; Grace Hopper, PhD", ("sup", "3"))
    doc.add_paragraph("INTRODUCTION")
    para(doc, "Opioid prescribing varies widely between physicians.", ("sup", intro_cites[0]),
         " Patients report satisfaction differently.", ("sup", intro_cites[1]),
         " We study agreeableness from online reviews.", ("sup", intro_cites[2]))
    doc.add_paragraph("METHODS")
    para(doc, "Adjusted R", ("sup", "2"), " was reported for every model in the analysis.")
    para(doc, "The cohort had 1200 beneficiaries; each was followed for one year.")
    if extra:
        para(doc, extra)
    t = doc.add_table(rows=1, cols=2)
    t.cell(0, 0).text, t.cell(0, 1).text = "Cohort size", "1200"
    doc.add_paragraph("REFERENCES")
    para(doc, "1. Smith J. A paper. 2020.")
    doc.save(path)
    return path


def test_citation_order_flags_the_one_cited_late(tmp_path):
    f = paper(tmp_path / "theirs.docx", intro_cites=("1", "3", "2"))
    lines = wc.citation_order(f)
    assert lines[0].startswith("citation numbers not in order")
    assert any(l.startswith("- 2 is first cited after 3") for l in lines)
    assert not any("- 3 " in l for l in lines)          # one late reference flags only itself


def test_citation_order_ignores_affiliations_powers_and_reads_ranges(tmp_path):
    f = paper(tmp_path / "ok.docx", intro_cites=("1", "2-4", "5,6"))
    assert wc.citation_order(f) == []                    # R² and the author marks are not citations
    assert [n for n, _, _ in wc.citations(f)] == [1, 2, 3, 4, 5, 6]


def test_bracket_citations(tmp_path):
    doc = Document()
    doc.add_paragraph("INTRODUCTION")
    doc.add_paragraph("First claim [2]. Second claim [1, 3].")
    doc.save(tmp_path / "b.docx")
    assert any("1 is first cited after 2" in l for l in wc.citation_order(tmp_path / "b.docx"))


def test_word_vs_word_by_section(tmp_path):
    a = paper(tmp_path / "a.docx", extra="A sentence only the co-authors wrote here.")
    b = paper(tmp_path / "b.docx", intro_cites=("1", "2", "4"), title="Opioid Prescribing And Agreeableness")
    stats, diffs = wc.word_vs_word(a, b)
    assert stats["rows"]["Methods"][2] == 1              # only in a
    text = "\n".join(diffs)
    assert "Introduction · digits differ" in text
    assert "case or punctuation differ" in text
    assert "A sentence only the co-authors wrote here." in text


def test_deleted_text_and_equations_are_read_as_accepted(tmp_path):
    doc = Document()
    doc.add_paragraph("METHODS")
    p = doc.add_paragraph()
    p.add_run("The model fits ")
    dele = OxmlElement("w:del")
    r = OxmlElement("w:r")
    dt = OxmlElement("w:delText")
    dt.text = "badly "
    r.append(dt)
    dele.append(r)
    p._p.append(dele)
    math = OxmlElement("m:oMath")
    mr = OxmlElement("m:r")
    mt = OxmlElement("m:t")
    mt.text = "y=ax"
    mr.append(mt)
    math.append(mr)
    p._p.append(math)
    p.add_run(" for each physician.")
    doc.save(tmp_path / "m.docx")
    texts = [x["text"] for x in wc.paragraphs(tmp_path / "m.docx")]
    assert "The model fits y=ax for each physician." in texts


def test_fold_reads_a_greek_question_mark_as_a_semicolon():
    assert wc.plain("one; two") == "one; two"
    assert wc.fold("beneficiary’s; x") == wc.fold("beneficiary's; x")


@pytest.mark.skipif(not (shutil.which("pdflatex") and shutil.which("pdftotext")), reason="needs pdflatex and pdftotext")
def test_word_vs_pdf(tmp_path):
    tex = tmp_path / "b.tex"
    tex.write_text(r"""\documentclass{article}\begin{document}
\section*{Introduction}
Opioid prescribing varies widely between physicians.\textsuperscript{1} Patients report satisfaction
differ\-ently.\textsuperscript{2} We study agreeableness from online reviews.\textsuperscript{4}
\section*{Methods}
Adjusted R\textsuperscript{2} was reported for every model in the analysis.
The cohort had 1200 beneficiaries; each was followed for one year. Cohort size 1200
\end{document}""")
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex.name], cwd=tmp_path, capture_output=True)
    a = paper(tmp_path / "a.docx", extra="Nothing like this is in the build at all, anywhere.")
    stats, diffs = wc.word_vs_pdf(a, tmp_path / "b.pdf")
    text = "\n".join(diffs)
    assert "digits differ" in text and "We study agreeableness" in text
    assert "not found in the PDF (s)\n- Nothing like this" in text
    assert stats["rows"]["Methods"][0] >= 2
    report = wc.report(a, tmp_path / "b.pdf")
    assert "## By section" in report and "## Citation order" in report


def test_a_citation_after_a_closing_parenthesis_counts(tmp_path):
    doc = Document()
    doc.add_paragraph("METHODS")
    para(doc, "Models used Poisson regression.", ("sup", "1"),
         " Risk ratios were approximated (eAppendix 4 in Supplement 1)", ("sup", "2"), ".")
    doc.save(tmp_path / "p.docx")                        # AgreeableJama-Board 261122: 23 read as never cited
    assert [n for n, _, _ in wc.citations(tmp_path / "p.docx")] == [1, 2]
    assert wc.citation_order(tmp_path / "p.docx") == []


def test_a_supplement_is_not_checked_for_order(tmp_path):
    doc = Document()
    doc.add_paragraph("Online-Only Supplemental Material")
    doc.add_paragraph("METHODS")
    para(doc, "Comorbidities were counted.", ("sup", "21"), " Weights followed.", ("sup", "7"))
    doc.save(tmp_path / "s.docx")
    assert wc.citation_order(tmp_path / "s.docx")[0].startswith("not checked: a supplement")
