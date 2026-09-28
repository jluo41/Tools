"""Teeth for the Word engine (scripts/latex_room_to_docx.py): tables must arrive.

Paper-MISQ-Board, 260908: in a 13/13 build three of four main tables reached Word
as a caption with nothing under it, and seven appendix tables never arrived.
Cause: the column-spec regex could not read nested braces (p{3cm}, @{}, >{...}),
so parse_table_rows returned no rows. These tests drive the REAL engine over a
tiny LaTeX room and count <w:tbl> in the written .docx files.
"""
import importlib.util
import json
import re
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
    for d in ("sections", "appendices", "displays/S-D-Main-1-Results/Display1-main", "displays/S-D-Appendix-A-Validation/Display1-perf"):
        (latex / d).mkdir(parents=True)
    (latex / "sections" / "S-D-Main-1-Results.tex").write_text(
        "\\section{Results}\nTable~\\ref{tab:main} shows it.\n"
        "\\begin{table}[H]\\centering\\input{displays/S-D-Main-1-Results/Display1-main/table-body}\\caption{Main regression.}\\label{tab:main}\\end{table}\n")
    (latex / "displays" / "S-D-Main-1-Results" / "Display1-main" / "table-body.tex").write_text(P_SPEC_TABLE)
    (latex / "appendices" / "S-D-Appendix-A-Validation.tex").write_text(
        "\\section{Validation}\nSee Table~\\ref{tab:a1}.\n"
        "\\begin{table}[p]\\centering\\caption{Model performance.}\\label{tab:a1}\\input{displays/S-D-Appendix-A-Validation/Display1-perf/table-body}\\end{table}\n")
    (latex / "displays" / "S-D-Appendix-A-Validation" / "Display1-perf" / "table-body.tex").write_text(X_SPEC_TABLE)
    (latex / "reference.bib").write_text("")
    (latex / "master.tex").write_text(
        "\\documentclass{article}\\title{D}\\author{}\\date{}\\begin{document}\\maketitle\n"
        "\\begin{abstract}One sentence.\\end{abstract}\n"
        "\\input{sections/S-D-Main-1-Results}\n"
        "\\section*{Acknowledgments}\n\\noindent\\textit{[draft]}\n"
        "\\clearpage\\bibliographystyle{apalike}\\bibliography{reference}\n"
        "\\clearpage\\appendix\n\\input{appendices/S-D-Appendix-A-Validation}\n\\end{document}\n")
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


def test_per_appendix_numbering_restarts_under_each_letter(room):
    """0.8.2 · AgreeableRx 260928: with appendix_float_numbering = "per-appendix" the
    second appendix's first table is Table B1 in caption AND in the text that \\ref's it,
    matching the LaTeX lane's \\counterwithin*; the main table stays Table 1."""
    latex = room / "delivery" / "latex"
    (latex / "displays" / "S-D-Appendix-B-Robustness" / "Display1-window").mkdir(parents=True)
    (latex / "appendices" / "S-D-Appendix-B-Robustness.tex").write_text(
        "\\section{Robustness}\nSee Table~\\ref{tab:b1}.\n"
        "\\begin{table}[p]\\centering\\caption{Window sensitivity.}\\label{tab:b1}\\input{displays/S-D-Appendix-B-Robustness/Display1-window/table-body}\\end{table}\n")
    (latex / "displays" / "S-D-Appendix-B-Robustness" / "Display1-window" / "table-body.tex").write_text(X_SPEC_TABLE)
    master = latex / "master.tex"
    master.write_text(master.read_text().replace(
        "\\input{appendices/S-D-Appendix-A-Validation}\n",
        "\\input{appendices/S-D-Appendix-A-Validation}\n\\input{appendices/S-D-Appendix-B-Robustness}\n"))
    cfg = room / "delivery" / "paper-build.toml"
    cfg.write_text(cfg.read_text().replace('venue_label = "Test"\n', 'venue_label = "Test"\nappendix_float_numbering = "per-appendix"\n'))
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(cfg))
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    main, supp = _text(room / "delivery" / "word" / "D.docx"), _text(room / "delivery" / "word" / "D-supp.docx")
    assert "Table 1." in main
    assert "Table A1." in supp and "Table B1." in supp and "Table A2" not in supp
    assert "See Table A1" in supp and "See Table B1" in supp


def _build_with(room, abstract: str, profile_extra: str = "") -> str:
    master = room / "delivery" / "latex" / "master.tex"
    master.write_text(master.read_text().replace("\\begin{abstract}One sentence.\\end{abstract}", abstract))
    cfg = room / "delivery" / "paper-build.toml"
    cfg.write_text(cfg.read_text().replace('venue_label = "Test"\n', 'venue_label = "Test"\n' + profile_extra))
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(cfg))
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    return _text(room / "delivery" / "word" / "D.docx")


def test_abstract_prose_before_a_keywords_label_reaches_word(room):
    """0.8.4 (JL 260928 "why I don't have the abstract"): an MISQ abstract ends in
    \\noindent\\textbf{Keywords:}; the Word lane printed only from the first bold label on,
    so the abstract prose was dropped and Word showed the heading, then Keywords."""
    main = _build_with(room, "\\begin{abstract}\nPhysicians differ in how they prescribe.\n\n\\smallskip\n"
                             "\\noindent\\textbf{Keywords:} opioids, reviews\n\\end{abstract}")
    assert "Physicians differ in how they prescribe." in main
    assert "Keywords:" in main and main.index("Physicians differ") < main.index("Keywords:")


def test_table_header_fill_follows_the_profile(room):
    """0.8.4 (JL 260928 "why the header is with color? are we using the MISQ format?"):
    the header fill was hard-coded F2F4F7 for every venue; MISQ's official file has none."""
    shaded = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert 'w:fill="F2F4F7"' in shaded                      # default unchanged for other venues
    plain = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}", 'table_header_fill = ""\n')
    assert 'w:fill="F2F4F7"' not in plain and "Table 1." in plain


def test_misq_official_layout_front_page_tables_and_notes(room):
    """0.8.4 (JL 260928 "Title abstract and keywords should be in the first page, right?" and
    "does this really following the MISQ word template?"): the official-format file puts the
    title, a centred ABSTRACT, the single-spaced abstract and Keywords on page 1, then a page
    break; tables have horizontal rules only, 8 pt cells, and a "Note." paragraph under them."""
    results = room / "delivery" / "latex" / "sections" / "S-D-Main-1-Results.tex"
    results.write_text(results.read_text().replace(
        "\\end{table}", "\\begin{flushleft}\\footnotesize\\textit{Note.} Standard errors in parentheses.\\end{flushleft}\\end{table}", 1))
    main = _build_with(room, "\\begin{abstract}\nPhysicians differ.\n\n\\noindent\\textbf{Keywords:} opioids\n\\end{abstract}",
                       'front_matter = "title-abstract-keywords"\nabstract_line_spacing = 1.0\nheading_align = "center"\n'
                       'caption_plain = true\ntable_borders = "horizontal"\ntable_font_size = 8\ntable_header_fill = ""\n')
    head = main[:main.index("Keywords:")]
    assert 'w:type="page"' not in head                         # no break between title and abstract
    assert '<w:pStyle w:val="Title"/>' in head
    after_keywords = main[main.index("Keywords:"):]
    assert after_keywords.index('w:type="page"') < after_keywords.index("RESULTS")   # break before the first section
    assert 'w:jc w:val="center"' in main[main.index("ABSTRACT") - 400:main.index("ABSTRACT")]
    assert '<w:insideV w:val="nil"/>' in main and '<w:insideH w:val="single"' in main
    assert "Standard errors in parentheses." in main
    styles = zipfile.ZipFile(room / "delivery" / "word" / "D.docx").read("word/styles.xml").decode()
    title = styles[styles.index('w:styleId="Title"'):]
    title = title[:title.index("</w:style>")]
    assert "<w:pBdr>" not in title and "17365D" not in title      # no blue rule, no blue text (JL 260928 screenshot)


def test_wide_table_fits_the_line_and_group_headers_merge(room, monkeypatch):
    """0.8.4 (JL 260928 "The table is just not good"): a 13-column table got 900 twips per
    column on a 9,360-twip line, so the last column went negative and printed one letter per
    line; \\multicolumn group headers sat in one narrow cell instead of spanning."""
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(room / "delivery" / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("docx_engine_widths", ENGINE)
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    header = ["", "LM-as-a-Judge", "", "", "", "Human-as-a-Judge", "", "", "", "Hard cases", "", "", ""]
    spans = [[1, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0]] + [[1] * 13] * 2
    rows = [header, ["Candidate LM"] + ["MAE", "RMSE", "High%", "Low%"] * 3,
            ["Gemini-2.5-flash-lite"] + ["0.1307", "0.2163", "92.18%", "83.76%"] * 3]
    widths = m.column_widths(rows, spans)
    assert 9360 <= sum(widths) <= 10400 and min(widths) >= 450   # may run into the margins, like the official Table 1
    assert widths[0] == max(widths)                         # row labels get the widest column
    char = 8 * 20 * 0.55 * 1.1
    assert all(w >= len("94.56%") * char + 120 - 1 for w in widths[1:])   # "94.56%" never breaks
    narrow = m.column_widths([["Outcome", "Binary", "Continuous"], ["Total MME", "9.34", "12.90"]], None)
    assert sum(narrow) == 9360                              # a table that fits keeps the text width
    main = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert 'w:gridSpan w:val="2"' in main                    # the fixture's \multicolumn{2}{c}{Outcomes}


def test_equations_become_word_equations_and_header_rows_repeat(room):
    """0.8.4 (JL 260928 screenshots): a display equation reached Word as "Y_ijc(o) = β_c(o) …" and
    lost \\varepsilon; a continued table repeated only its first header row."""
    results = room / "delivery" / "latex" / "sections" / "S-D-Main-1-Results.tex"
    results.write_text(results.read_text().replace(
        "\\section{Results}", "\\section{Results}\nWe estimate $$ Y_{ijc}^{(o)} = \\beta_c^{(o)} H_j + \\varepsilon_{ijc}^{(o)} $$ "
        "where $H_j$ is the indicator.\n", 1))
    main = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert "<m:oMathPara" in main and "<m:sSubSup>" in main        # a native Word equation
    assert "\u03b5" in main                                       # epsilon survives
    assert "Y_ijc" not in main and "H_j" not in main               # no flattened underscores
    assert main.count("<w:tblHeader") >= 2                          # the fixture's two header rows both repeat


def test_math_symbols_in_table_cells_survive(room, monkeypatch):
    """0.8.4 (JL 260928 screenshot): a Results header printed "HDLD ( pp)" because \\Delta was
    not in the symbol map and the generic command stripper dropped it."""
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(room / "delivery" / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("docx_engine_symbols", ENGINE)
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    assert m.latex_to_text("HDLD ($\\Delta$\\,pp)") == "HDLD (Δ pp)"
    assert m.latex_to_text("$\\varepsilon_{ijc}$, $n \\ge 20$, $x \\in S$") == "ε_ijc, n ≥ 20, x ∈ S"
    assert m.latex_to_text("\\mu and \\multicolumn") == "μ and"     # whole names only


def test_verbatim_prompt_is_a_framed_box_line_by_line(room):
    """0.8.4 (JL 260928 appendix screenshot): a published prompt in \\begin{verbatim} reached Word
    as double-spaced prose, its lines joined into one paragraph and the word "verbatim" printed."""
    results = room / "delivery" / "latex" / "sections" / "S-D-Main-1-Results.tex"
    results.write_text(results.read_text().replace(
        "\\section{Results}", "\\section{Results}\nThe prompt:\n\n\\begin{verbatim}\nYou are an expert psychologist.\n\n"
        "- Openness\n- Agreeableness 100%\n    <score>High</score>\n\\end{verbatim}\n\nAfter the prompt.\n", 1))
    main = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    body = main[main.index("The prompt"):main.index("After the prompt")]
    assert "verbatim</w:t>" not in body and ">verbatim " not in body     # no leaked environment name
    assert 'w:tblDescription w:val="verbatim"' in body and "Courier New" in body
    assert body.count("<w:p>") + body.count("<w:p ") >= 5                   # one paragraph per source line
    assert ">- Agreeableness 100%<" in body                                  # a % in a prompt is text, not a comment
    assert "&lt;score&gt;High&lt;/score&gt;" in body                          # XML tags print as written
    assert 'w:tblBorders><w:top w:val="single"' in body.replace("\n", "")    # a framed box


def test_bold_and_italic_reach_word_prose(room):
    """0.8.4 (JL 260928 appendix screenshot): \\textbf and \\textit in body prose printed plain in
    Word ("Agreeableness specification" lost its bold) while the PDF set them."""
    results = room / "delivery" / "latex" / "sections" / "S-D-Main-1-Results.tex"
    results.write_text(results.read_text().replace(
        "\\section{Results}", "\\section{Results}\nThe \\textbf{Agreeableness specification} is \\textit{compact} and $x$ is \\emph{a {nested} term}.\n", 1))
    main = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    para = main[main.rindex("<w:p>", 0, main.index("Agreeableness specification")):]
    para = para[:para.index("</w:p>")]
    runs = re.findall(r"<w:r>(.*?)</w:r>", para, re.S)
    styled = {re.search(r"<w:t[^>]*>(.*?)</w:t>", r).group(1): ("<w:b/>" in r, "<w:i/>" in r) for r in runs if "<w:t" in r}
    assert styled["Agreeableness specification"] == (True, False)
    assert styled["compact"] == (False, True) and styled["a nested term"] == (False, True)
    assert styled["The "] == (False, False) and "<m:oMath" in para
    assert not re.search("[\x02-\x05]", main)                              # no marker leaks


def test_blind_copy_without_acknowledgments_still_converts(room):
    """0.8.4 (JL 260928): the MISQ blind copy prints no Acknowledgments section (profile
    [latex] acknowledgments = false), and the Word lane used that heading as the end of the
    main text, so it raised "missing acknowledgments". The main text now runs to the bibliography."""
    master = room / "delivery" / "latex" / "master.tex"
    master.write_text(master.read_text().replace("\\section*{Acknowledgments}\n\\noindent\\textit{[draft]}\n", ""))
    main = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert "shows it" in main and "Acknowledgments" not in main and "[draft]" not in main


def test_section_snapshots_can_be_switched_off(room):
    """0.8.4 (JL 260928: "why it is not the same to each section's word? and no references"):
    draft-sections/ was a second, reference-less copy of each Section Page's own Word file.
    section_snapshots = "" switches the lane off; nothing is written there."""
    cfg = room / "delivery" / "paper-build.toml"
    cfg.write_text(cfg.read_text().replace('section_snapshots = "word/draft-sections"', 'section_snapshots = ""'))
    _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert not (room / "delivery" / "word" / "draft-sections").exists()
