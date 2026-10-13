"""Teeth for the 0.9.1 paper-owned options (JL 260929, Paper-FairGlucose-preprint: npj + arXiv).

  [source] head / opening / supplement_head / supplement_opening   the paper owns its LaTeX
  profile appendices = "supplement"     master.tex main, supplement.tex notes, combined.tex both
  [source] store                        fragments read displays/... from the paper's store
  [evidence] draft_citations            a DRAFT merges a Page's unverified draft Bib, as a blocker
  drop_room_defined()                   a \\ref the room itself labels is not unresolved

Runs without LaTeX. Each option has a tooth that fails when the option is off.
"""
import importlib.util
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "scripts" / "build_delivery.py"

CONFIG = """[paper]
id = "Paper-O"
title = "O"
[profile]
appendices = "supplement"
[profile.latex]
engine = "pdflatex"
bibstyle = "naturemag"
[pages]
main = "../Ba-O-Main"
appendix = "../Bb-O-Appendix"
order = "../A1-Story/StoryA-o/StoryA-o.md"
[source]
room = "latex"
master = "master.tex"
sections = "sections"
appendices = "appendices"
displays = "displays"
bibliography = "reference.bib"
head = "../assets/master-head.tex"
opening = "../assets/master-opening.tex"
supplement_head = "../assets/supplement-head.tex"
supplement_opening = "../assets/supplement-opening.tex"
store = "../displays"
[evidence]
mode = "draft"
draft_includes_unready = true
draft_citations = {citations}
[outputs]
main_pdf = "latex/O.pdf"
supplement_pdf = "latex/O-SI.pdf"
combined_pdf = "latex/O-combined.pdf"
main_docx = "word/O.docx"
manifest = "build-manifest.json"
"""


def _page(group, pid, h1, fragment, draft_bib=None):
    d = group / pid
    (d / "delivery" / "latex").mkdir(parents=True)
    (d / f"{pid}.md").write_text(f"# {pid} · {h1}\n")
    (d / "delivery" / "latex" / f"{pid}.tex").write_text(fragment)
    (d / "delivery" / "latex" / f"{pid}.pdf").write_bytes(b"%PDF")
    if draft_bib:
        (d / "delivery" / "latex" / "draft-bibliography").mkdir()
        (d / "delivery" / "latex" / "draft-bibliography" / f"{pid}.bib").write_text(draft_bib)


def _load(tmp_path, monkeypatch, citations="true"):
    root = tmp_path / "Paper-O"
    delivery = root / "delivery"; delivery.mkdir(parents=True)
    (delivery / "paper-build.toml").write_text(CONFIG.replace("{citations}", citations))
    story = root / "A1-Story" / "StoryA-o"; story.mkdir(parents=True)
    (story / "StoryA-o.md").write_text(
        "# StoryA-o\n<!-- haipipe:compile-order:start -->\nmain:\n- S-O-Main-1-Intro\n"
        "appendix:\n- S-O-Appendix-A-Data\n<!-- haipipe:compile-order:end -->\n")
    assets = root / "assets"; assets.mkdir()
    (assets / "master-head.tex").write_text("\\documentclass{article}\n\\usepackage{ownstyle}\n\\title{\\thetitle}\n")
    (assets / "master-opening.tex").write_text("\\maketitle\n")
    (assets / "supplement-head.tex").write_text("\\renewcommand{\\thefigure}{S\\arabic{figure}}\n")
    (assets / "supplement-opening.tex").write_text("\\maketitle\n\\tableofcontents\n")
    (assets / "ownstyle.sty").write_text("% the paper's own style\n")
    store = root / "displays"
    (store / "Figure").mkdir(parents=True); (store / "Table").mkdir()
    (store / "Figure" / "fig1.pdf").write_bytes(b"%PDF")
    (store / "Table" / "t1.tex").write_text(
        "\\begin{table}\\input{displays/Table/t1-body}\\caption{t}\\label{tab:t1}\\end{table}\n")
    (store / "Table" / "t1-body.tex").write_text("\\begin{tabular}{c}x\\end{tabular}\n")
    bib = "@article{key1,\n  title = {One},\n  year = {2026}\n}\n"
    _page(root / "Ba-O-Main", "S-O-Main-1-Intro", "§1 Introduction",
          "\\section{Introduction}\nA claim \\cite{key1}, Table~\\ref{tab:t1}.\n"
          "\\begin{figure}\\includegraphics{displays/Figure/fig1.pdf}\\label{fig:one}\\end{figure}\n"
          "\\input{displays/Table/t1}\n", draft_bib=bib)
    _page(root / "Bb-O-Appendix", "S-O-Appendix-A-Data", "Appendix A · Data",
          "\\section{Data}\nSee Figure~\\ref{fig:one} and \\ref{fig:nowhere}.\n")
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(delivery / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("build_delivery_owned", ENGINE)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def _assemble(m):
    """build() minus latexmk and Word: placement, Bib, masters."""
    m.reset_placement()
    main_ids, appx_ids, _ = m.read_order()
    for d in (m.SEC, m.APP, m.DISP): d.mkdir(parents=True, exist_ok=True)
    main = [m.inspect(i, m.rel(m.CFG["pages"]["main"])) for i in main_ids]
    appx = [m.inspect(i, m.rel(m.CFG["pages"]["appendix"])) for i in appx_ids]
    pages = main + appx
    for p in pages:
        p["included"] = True
    m.require_page_bibs(pages)
    labels = m.label_index(pages); unresolved = []
    main_f = [(p, m.place_fragment(p, m.SEC, labels, unresolved)) for p in main]
    appx_f = [(p, m.place_fragment(p, m.APP, labels, unresolved)) for p in appx]
    m.merge_bib(pages)
    m.write_master(main_f, appx_f, "DRAFT", 0, len(pages))
    return pages, unresolved


def test_paper_owned_head_writes_three_documents(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch)
    _assemble(m)
    master = m.MASTER.read_text()
    supplement = (m.LATEX / "supplement.tex").read_text()
    combined = (m.LATEX / "combined.tex").read_text()
    assert master.count("\\documentclass{article}") == 1 and "\\usepackage{ownstyle}" in master
    assert "\\author{}" not in master and "fancyhdr" not in master          # the engine head is gone
    assert "appendices/" not in master and "\\bibliographystyle{naturemag}" in master
    assert "\\renewcommand{\\thefigure}{S" in supplement and "\\tableofcontents" in supplement
    assert "appendices/S-O-Appendix-A-Data" in supplement and "sections/" not in supplement
    assert "sections/S-O-Main-1-Intro" in combined and "\\appendix" in combined
    assert (m.LATEX / "ownstyle.sty").is_file()                              # the head's files travel
    assert m.LATEX_ENGINE == "pdflatex"


def test_without_the_split_master_holds_both_halves(tmp_path, monkeypatch):
    """the expect-fail side of the split: appendices back in the one master, no other documents."""
    m = _load(tmp_path, monkeypatch)
    m.SUPPLEMENT_SPLIT = False
    _assemble(m)
    assert "appendices/S-O-Appendix-A-Data" in m.MASTER.read_text()
    assert not (m.LATEX / "supplement.tex").exists() and not (m.LATEX / "combined.tex").exists()


def test_store_files_are_copied_and_are_a_blocker(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch)
    pages, _ = _assemble(m)
    assert (m.LATEX / "displays" / "Figure" / "fig1.pdf").is_file()
    assert (m.LATEX / "displays" / "Table" / "t1-body.tex").is_file()       # a stored table's own \input
    assert "displays/Table/t1" in m.STORE_READS["S-O-Main-1-Intro"]
    blockers = m.build_readiness(pages, [])["blockers"]
    assert any("paper store" in b and "S-O-Main-1-Intro" in b for b in blockers)


def test_without_a_store_the_path_is_left_unresolved(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch)
    m.STORE = None
    _assemble(m)
    assert not (m.LATEX / "displays" / "Figure" / "fig1.pdf").exists() and not m.STORE_READS


def test_draft_citations_merge_the_draft_bib_as_a_blocker(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch)
    pages, _ = _assemble(m)
    assert "@article{key1" in m.BIB.read_text() and "UNVERIFIED" in m.BIB.read_text()
    assert m.DRAFT_CITED == ["S-O-Main-1-Intro"]
    assert any("citations are unverified" in b for b in m.build_readiness(pages, [])["blockers"])


def test_without_draft_citations_a_citing_page_is_refused(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch, citations="false")
    with pytest.raises(RuntimeError, match="selected-bibliography"):
        _assemble(m)


def test_a_label_the_room_defines_is_not_unresolved(tmp_path, monkeypatch):
    m = _load(tmp_path, monkeypatch)
    _, unresolved = _assemble(m)
    refs = {u["ref"] for u in unresolved}
    assert {"fig:one", "tab:t1", "fig:nowhere"} <= refs                    # no DISPLAY unit knows them
    left = {u["ref"] for u in m.drop_room_defined(unresolved)}
    assert left == {"fig:nowhere"}                                         # only the one nothing defines
