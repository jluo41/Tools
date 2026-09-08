"""Teeth for the Word engine (scripts/latex_room_to_docx.py): tables must arrive.

Paper-MISQ-Board, 260908: in a 13/13 build three of four main tables reached Word
as a caption with nothing under it, and seven appendix tables never arrived.
Cause: the column-spec regex could not read nested braces (p{3cm}, @{}, >{...}),
so parse_table_rows returned no rows. These tests drive the REAL engine over a
tiny LaTeX room and count <w:tbl> in the written .docx files.
"""
import importlib.util
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "scripts" / "latex_room_to_docx.py"

P_SPEC_TABLE = (
    "\\begin{tabular}{@{}\n  >{\\raggedright\\arraybackslash}p{1.1in}\n  >{\\centering\\arraybackslash}p{0.7in} r@{}}\n"
    "\\toprule\n & \\multicolumn{2}{c}{\\textbf{Outcomes}} \\\\\n\\cmidrule(lr){2-3}\n"
    " & \\shortstack{(1)\\\\Basic} & (2) \\\\\n\\midrule\nAgreeableness & 12.90 & 15.33 \\\\\n"
    "Observations & 765,701 & 765,701 \\\\\n\\bottomrule\n\\end{tabular}\n")
X_SPEC_TABLE = (
    "\\begin{tabularx}{\\linewidth}{@{}p{3.45cm}*{2}{>{\\centering\\arraybackslash}X}@{}}\n"
    "\\toprule\nModel & MAE & RMSE \\\\\n\\midrule\nGPT & 0.10 & 0.14 \\\\\n\\bottomrule\n\\end{tabularx}\n")


@pytest.fixture
def room(tmp_path):
    root = tmp_path / "Paper-D"; latex = root / "delivery" / "latex"
    for d in ("sections", "appendices", "displays/u1", "displays/u2"):
        (latex / d).mkdir(parents=True)
    (latex / "sections" / "S-D-Main-Results.tex").write_text(
        "\\section{Results}\nTable~\\ref{tab:main} shows it.\n"
        "\\begin{table}[H]\\centering\\input{displays/u1/table-body}\\caption{Main regression.}\\label{tab:main}\\end{table}\n")
    (latex / "displays" / "u1" / "table-body.tex").write_text(P_SPEC_TABLE)
    (latex / "appendices" / "S-D-Appendix-Validation.tex").write_text(
        "\\section{Validation}\nSee Table~\\ref{tab:a1}.\n"
        "\\begin{table}[p]\\centering\\caption{Model performance.}\\label{tab:a1}\\input{displays/u2/table-body}\\end{table}\n")
    (latex / "displays" / "u2" / "table-body.tex").write_text(X_SPEC_TABLE)
    (latex / "reference.bib").write_text("")
    (latex / "master.tex").write_text(
        "\\documentclass{article}\\title{D}\\author{}\\date{}\\begin{document}\\maketitle\n"
        "\\begin{abstract}One sentence.\\end{abstract}\n"
        "\\input{sections/S-D-Main-Results}\n"
        "\\section*{Acknowledgments}\n\\noindent\\textit{[draft]}\n"
        "\\clearpage\\bibliographystyle{apalike}\\bibliography{reference}\n"
        "\\clearpage\\appendix\n\\input{appendices/S-D-Appendix-Validation}\n\\end{document}\n")
    (root / "delivery" / "paper-build.toml").write_text(
        '[paper]\nid = "Paper-D"\ntitle = "D"\nsource_format = "latex-room"\nvenue_profile = ""\n'
        '[profile]\nvenue_label = "Test"\n'
        '[source]\nroom = "latex"\nmaster = "master.tex"\nsections = "sections"\ndisplays = "displays"\nbibliography = "reference.bib"\n'
        '[evidence]\nmode = "draft"\n'
        '[outputs]\nmain_docx = "word/D.docx"\nsupplement_docx = "word/D-supp.docx"\nmain_pdf = "latex/D.pdf"\n'
        'supplement_pdf = "latex/D-supp.pdf"\nsection_snapshots = "word/draft-sections"\nassets = "latex/submission-assets"\nmanifest = "build-manifest.json"\n')
    return root


def _tables(docx: Path) -> int:
    with zipfile.ZipFile(docx) as z:
        return z.read("word/document.xml").decode().count("<w:tbl>")


def _text(docx: Path) -> str:
    with zipfile.ZipFile(docx) as z:
        return z.read("word/document.xml").decode()


def test_nested_brace_colspecs_arrive_as_word_tables(room):
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(room / "delivery" / "paper-build.toml"))
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    main, supp = room / "delivery" / "word" / "D.docx", room / "delivery" / "word" / "D-supp.docx"
    assert _tables(main) == 1 and _tables(supp) == 1
    assert "Table 1." in _text(main) and "Main regression." in _text(main)
    assert "Table S1." in _text(supp) and "Model performance." in _text(supp)
    manifest = json.loads((room / "delivery" / "build-manifest.json").read_text())
    assert manifest["build"]["checks"]["tables_rendered"]["ok"] is True


def test_parse_table_rows_reads_nested_specs_and_spans(room, monkeypatch):
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(room / "delivery" / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("docx_engine_under_test", ENGINE)
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m   # dataclasses need the module registered
    spec.loader.exec_module(m)
    rows = m.parse_table_rows(P_SPEC_TABLE)
    assert rows, "a p{} / >{} / @{} column spec must still yield rows"
    assert rows[0] == ["", "Outcomes", ""]            # multicolumn{2} pads one empty cell
    assert rows[1][1] == "(1) Basic"                  # shortstack stays ONE cell
    assert rows[2][0] == "Agreeableness" and rows[-1][-1] == "765,701"
    xrows = m.parse_table_rows(X_SPEC_TABLE)
    assert xrows and xrows[0] == ["Model", "MAE", "RMSE"] and xrows[1] == ["GPT", "0.10", "0.14"]


def test_expect_fail_old_regex_shape_lost_the_rows(room, monkeypatch):
    """the Gate-1 lesson for this defect: the pre-0.7.1 spec regex returns nothing for p{}."""
    import re
    old = re.search(r"\\begin\{(tabular|longtable)\}\{[^{}]*\}(.*?)\\end\{\1\}", P_SPEC_TABLE, re.S)
    assert old is None
