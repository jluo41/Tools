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
        xml = z.read("word/document.xml").decode()
    # 0.12.0: a display floated to the top of its page sits in a borderless one-cell frame, which is not a table
    return xml.count("<w:tbl>") - xml.count('<w:tblDescription w:val="haipipe-display-float"/>')


def test_a_display_floats_to_the_top_of_its_page(room):
    """display_float = "top" (default): the display's frame is pinned to the top margin; "inline" leaves it in place."""
    cfg = room / "delivery" / "paper-build.toml"
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(cfg))
    supp = room / "delivery" / "word" / "D-supp.docx"   # the fixture's main tables print after the references
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    assert 'w:tblpYSpec="top"' in _text(supp) and _tables(supp) == 1
    cfg.write_text(cfg.read_text().replace('venue_label = "Test"', 'venue_label = "Test"\ndisplay_float = "inline"'))
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    assert "tblpYSpec" not in _text(supp) and _tables(supp) == 1


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


def test_a_stuck_word_is_found_quickly(room, monkeypatch):
    """b16.j02-s22 261104: a Word that gives no answer is asked once, within its time limit, and says False."""
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(room / "delivery" / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("docx_engine_stuck", ENGINE)
    m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    asked = []
    def stuck(cmd, **kw):
        asked.append(kw["timeout"])
        raise subprocess.TimeoutExpired(cmd, kw["timeout"])
    monkeypatch.setattr(m.subprocess, "run", stuck)
    assert m.word_answers(wait=5) is False and asked == [15]
    class Ok: returncode = 0
    monkeypatch.setattr(m.subprocess, "run", lambda cmd, **kw: Ok)
    assert m.word_answers() is True


def test_the_word_step_keeps_the_last_builds_manifest(room):
    """Paper-PhyAbsence 261104: replacing the manifest emptied the Writing view for the rest of every build."""
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(room / "delivery" / "paper-build.toml"))
    path = room / "delivery" / "build-manifest.json"
    path.write_text(json.dumps({"outputs": {"pdf": "latex/D.pdf"}, "portal": {"uploads": []}, "published": {"a": 1},
                                "build": {"status": "OLD"}}))
    r = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-1500:]
    manifest = json.loads(path.read_text())
    assert manifest["outputs"] == {"pdf": "latex/D.pdf"}       # the named files stay until the build names them again
    assert manifest["portal"] == {"uploads": []} and manifest["published"] == {"a": 1}
    assert manifest["build"]["status"] != "OLD"                # this step's own receipt is new


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
    # 0.12.0 (JL 261023 "why the color of the table is like this?"): no fill and horizontal rules are the default;
    # a profile can still ask for a colour and a grid
    plain = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert "w:fill=" not in plain and "Table 1." in plain
    assert '<w:insideV w:val="nil"/>' in plain               # no vertical lines
    shaded = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}",
                         'table_header_fill = "F2F4F7"\ntable_borders = "grid"\n')
    assert 'w:fill="F2F4F7"' in shaded


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


def test_jama_main_displays_keep_numbers_refs_and_figure_notes(room):
    from PIL import Image
    latex = room / "delivery/latex"
    image = latex / "displays/observed.png"
    Image.new("RGB", (12, 12), "white").save(image)
    (latex / "master.tex").write_text(
        r"\documentclass{article}\begin{document}\begin{center}D\end{center}"
        r"\section*{Key Points}\textbf{Question} One?"
        r"\section*{Abstract}\textbf{Importance} One."
        r"\section{Introduction}See Table~\ref{tab:main} and Figure~\ref{fig:observed}."
        r"\input{sections/S-D-Main-1-Results}"
        r"\begin{figure}\includegraphics{displays/observed.png}"
        r"\caption{Observed values.}\label{fig:observed}"
        r"\begin{flushleft}Intervals use requests.\end{flushleft}\end{figure}"
        r"\bibliography{reference}\appendix\section{Extra}One.\end{document}"
    )
    config = room / "delivery/paper-build.toml"
    config.write_text(config.read_text().replace(
        'venue_label = "Test"',
        'venue_label = "Test"\nlayout = "jama-internal-medicine"\ninclude_main_displays = true'))
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(config))
    result = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr[-1500:]
    xml = _text(room / "delivery/word/D.docx")
    assert "Table 1" in xml and "Figure 1" in xml
    assert "Table 1. Main regression." in xml and "Figure 1. Observed values." in xml
    assert "Intervals use requests." in xml
    assert "Tablemain" not in xml and "Figureobserved" not in xml


def test_a_parbox_table_note_reaches_word(room):
    """0.12.0 (JL 261023): Table 2's note sat in \\parbox{\\linewidth}{\\footnotesize ...} after the tabular; Word dropped it."""
    body = room / "delivery" / "latex" / "displays" / "S-D-Main-1-Results" / "Display1-main" / "table-body.tex"
    body.write_text(body.read_text() + "\\par\\smallskip\\parbox{\\linewidth}{\\footnotesize\\raggedright SE, standard error. * \\textit{p}$<$0.10.}\n")
    out = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert "SE, standard error." in out



def test_a_pending_cell_is_shaded_yellow_in_word(room):
    """0.12.0 (JL 261023: "these unfilled ones, can you highlight them?"): a cell written \\pending{--} prints on yellow
    in Word, the mark itself never printed; the expect-fail side is the plain cell, unshaded."""
    body = room / "delivery" / "latex" / "displays" / "S-D-Main-1-Results" / "Display1-main" / "table-body.tex"
    body.write_text("\\providecommand{\\pending}[1]{\\colorbox{yellow}{#1}}\n"
                    + body.read_text().replace("Observations & 765,701 & 765,701", "Observations & \\pending{--} & 765,701"))
    out = _build_with(room, "\\begin{abstract}One sentence.\\end{abstract}")
    assert 'w:fill="FFFF00"' in out and "\\pending" not in out and "providecommand" not in out
    assert out.count('w:fill="FFFF00"') == 1


def test_jama_supplement_prints_etable_labels_and_raises_superscripts(room):
    """pp-LBP-JAMA 261103: the Supplement Word file printed captions with no "eTable N." and flattened \\textsuperscript."""
    from PIL import Image
    latex = room / "delivery/latex"
    Image.new("RGB", (12, 12), "white").save(latex / "displays/extra.png")
    (latex / "master.tex").write_text(
        r"\documentclass{article}\begin{document}\begin{center}D\end{center}"
        r"\section*{Key Points}\textbf{Question} One?"
        r"\section*{Abstract}\textbf{Importance} One."
        r"\section{Introduction}One."
        r"\bibliography{reference}\appendix\section{Extra}One."
        r"\begin{table}\caption{First supplement table.}\label{tab:s1}"
        r"\begin{tabular}{ll}\toprule Group & Mean\textsuperscript{a} \\\midrule Older & 1 \\\bottomrule\end{tabular}"
        r"\begin{flushleft}Adjusted. \textsuperscript{a}The cut chosen.\end{flushleft}\end{table}"
        r"\begin{figure}\includegraphics{displays/extra.png}\caption{First supplement figure.}\label{fig:s1}\end{figure}"
        r"\begin{table}\caption{Second supplement table.}\label{tab:s2}"
        r"\begin{tabular}{ll}\toprule A & B \\\midrule 1 & 2 \\\bottomrule\end{tabular}\end{table}"
        r"\end{document}")
    config = room / "delivery/paper-build.toml"
    config.write_text(config.read_text().replace('venue_profile = ""', 'venue_profile = "jama-internal-medicine"')
                      .replace('venue_label = "Test"', 'venue_label = "Test"\nsupplement_contents = true'))
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(config))
    result = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr[-1500:]
    from docx import Document
    doc = Document(room / "delivery/word/D-supp.docx")
    text = _text(room / "delivery/word/D-supp.docx")
    for caption in ("eTable 1. First supplement table.", "eFigure 1. First supplement figure.", "eTable 2. Second supplement table."):
        assert text.count(caption) == 2, (caption, text.count(caption))   # the contents list and the caption
    raised = [r.text for t in doc.tables for row in t.rows for c in row.cells for p in c.paragraphs
              for r in p.runs if r.font.superscript]
    assert "a" in raised
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn
    every = [Paragraph(e, doc) for e in doc.element.body.iter(qn("w:p"))]     # a display may sit in a float frame
    note = [p for p in every if "The cut chosen" in p.text][0]
    assert [r.text for r in note.runs if r.font.superscript] == ["a"]
    assert "Adjusted. a" in note.text          # a note's mark keeps its space, unlike a citation
    with zipfile.ZipFile(room / "delivery/word/D-supp.docx") as z:
        assert "\x10" not in z.read("word/document.xml").decode()


def _engine_module(room, monkeypatch):
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(room / "delivery/paper-build.toml"))
    spec = importlib.util.spec_from_file_location("engine_under_test", ENGINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_layout_codes_never_print(room, monkeypatch):
    # pp-LBP-JAMA 261103: "=2em=11emLinear", "1em2-part model", "1.9in Primary"
    m = _engine_module(room, monkeypatch)
    rows = m.parse_table_rows(
        r"\begin{tabular}{ll}\toprule A & B \\\midrule "
        r"\hangindent=2em\hangafter=1\hspace*{1em}Linear & 1 \\"
        r"\hspace*{2em}\textit{2-part model} & 2 \\"
        r"\parbox[t]{1.9in}{\raggedright Primary: Total\textsuperscript{a}} & 3 \\\bottomrule\end{tabular}")
    assert [r[0] for r in rows[1:]] == [m.INDENT_MARK + "Linear", m.INDENT_MARK * 2 + "2-part model", "Primary: Total\x10a\x11"]
    assert m.latex_to_text(r"\setlength{\tabcolsep}{4.5pt}Word\vspace{2em}") == "Word"


@pytest.mark.parametrize("cell,expected", [
    ("-2.5", "−2.5"), ("-2.5 (-3.1 to -0.5)", "−2.5 (−3.1 to −0.5)"), ("$-.5$", "−.5"),
    ("2016-2019", "2016-2019"), ("ICD-10", "ICD-10"), ("14-day", "14-day"), ("-", "-"), ("1.2-3.4", "1.2-3.4"),
])
def test_a_cell_number_gets_a_true_minus(room, monkeypatch, cell, expected):
    m = _engine_module(room, monkeypatch)
    assert m._expand_cell(cell) == [expected]


def test_a_square_root_and_a_word_survive_as_equations(room, monkeypatch):
    # pp-LBP-JAMA 261103: "RR + RR(RR-1)", "s c o r e"
    m = _engine_module(room, monkeypatch)
    from lxml import etree
    xml = etree.tostring(m.latex_to_omml(r"\mathrm{RR} + \sqrt{\mathrm{RR}(\mathrm{RR}-1)}")).decode()
    assert "m:rad>" in xml and xml.count(">RR</m:t>") == 3
    assert ">score</m:t>" in etree.tostring(m.latex_to_omml(r"\mathrm{score}_j")).decode()
    assert m.latex_to_text(r"\sqrt{x}+1") == "√(x)+1"


def test_a_table_note_keeps_its_equation(room, monkeypatch):
    m = _engine_module(room, monkeypatch)
    display = m.parse_display(r"\begin{table}\caption{T.}\begin{tabular}{l}A\\\end{tabular}"
                              r"\par\parbox{\linewidth}{\footnotesize E = $\sqrt{x}$, change -2.5.}\end{table}")
    assert re.fullmatch(r"E = @@MATH\d+@@, change −2\.5\.", display.note)


def test_a_jama_supplement_lists_its_contents_and_keeps_heading_case(room):
    latex = room / "delivery/latex"
    (latex / "master.tex").write_text(
        r"\documentclass{article}\begin{document}\begin{center}D\end{center}"
        r"\section*{Key Points}\textbf{Question} One?\section*{Abstract}\textbf{Importance} One."
        r"\section{Introduction}Text.\bibliography{reference}\appendix"
        r"\section{eAppendix 1. Inherited exposure}One."
        r"\begin{table}\caption{\textbf{The title.} A long legend under it.}\label{tab:s1}"
        r"\begin{tabular}{ll}\toprule A & B\\\midrule\hspace*{1em}Row & -1\\\bottomrule\end{tabular}\end{table}"
        r"\end{document}")
    config = room / "delivery/paper-build.toml"
    config.write_text(config.read_text().replace('venue_profile = ""', 'venue_profile = "jama-internal-medicine"'))
    env = dict(os.environ, HAIPIPE_PAPER_BUILD_CONFIG=str(config))
    result = subprocess.run([sys.executable, str(ENGINE)], cwd=room / "delivery", env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr[-1500:]
    from docx import Document
    doc = Document(room / "delivery/word/D-supp.docx")
    text = [p.text for p in doc.paragraphs]
    assert text.count("eAppendix 1. Inherited exposure") == 2           # the contents list and the heading, no capitals
    assert "EAPPENDIX 1. INHERITED EXPOSURE" not in text
    assert any(line.strip() == "eTable 1. The title." for line in text)  # the contents list: the title, not the legend
    from docx.text.paragraph import Paragraph
    from docx.oxml.ns import qn
    every = [Paragraph(e, doc) for e in doc.element.body.iter(qn("w:p"))]     # a display may sit in a float frame
    cell = [p for p in every if p.text == "Row"][0]
    assert cell.paragraph_format.left_indent is not None
    with zipfile.ZipFile(room / "delivery/word/D-supp.docx") as z:
        assert "\x13" not in z.read("word/document.xml").decode()


def test_a_word_draft_never_measures(monkeypatch):
    """--word-draft: no display is held for measuring, so Word is only asked to print."""
    import latex_room_to_docx as L
    monkeypatch.setattr(L.sys, "platform", "darwin")
    monkeypatch.setattr(L, "MSWORD_APP", type("App", (), {"exists": staticmethod(lambda: True)}))
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.delenv("HAIPIPE_WORD_PREVIEW", raising=False)
    monkeypatch.delenv("HAIPIPE_WORD_DRAFT", raising=False)
    assert L.word_can_measure()
    monkeypatch.setenv("HAIPIPE_WORD_DRAFT", "1")
    assert not L.word_can_measure()
