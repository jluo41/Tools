"""Teeth for the canonical delivery engine (haipipe-paper-assemble scripts/build_delivery.py).

Runs without LaTeX: it exercises order parsing, the milestone, and the three
behaviors on a synthetic paper in tmp_path, then PROVES the register catches
the double-print by switching behavior A off (the expect-fail procedure).
"""
import importlib.util
import os
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "scripts" / "build_delivery.py"


@pytest.fixture
def paper(tmp_path, monkeypatch):
    """a tiny paper: one ready page with an embedded+cited figure, one not-ready page."""
    root = tmp_path / "Paper-T"
    delivery = root / "delivery"; delivery.mkdir(parents=True)
    (delivery / "paper-build.toml").write_text(
        '[paper]\nid = "Paper-T"\ntitle = "T"\n'
        '[pages]\nmain = "../Ba-T-Main"\nappendix = "../Bb-T-Appendix"\norder = "../A1-Story/StoryA-t-fixture/StoryA-t-fixture.md"\n'
        '[source]\nroom = "latex"\nmaster = "master.tex"\nsections = "sections"\nappendices = "appendices"\n'
        'displays = "displays"\nbibliography = "reference.bib"\n'
        '[evidence]\nmode = "draft"\n'
        '[outputs]\nmain_pdf = "latex/T.pdf"\nmain_docx = "word/T.docx"\nmanifest = "build-manifest.json"\n')
    story = root / "A1-Story" / "StoryA-t-fixture"; story.mkdir(parents=True)
    (story / "StoryA-t-fixture.md").write_text(
        "# StoryA-t-fixture\n<!-- haipipe:compile-order:start -->\nmain:\n- S-T-Main-1-Intro\n- S-T-Main-2-Methods\n"
        "appendix:\n<!-- haipipe:compile-order:end -->\n")
    (root / "Bb-T-Appendix").mkdir()
    # ready page: fragment embeds the float (as md2tex does) AND cites it
    intro = root / "Ba-T-Main" / "S-T-Main-1-Intro"
    (intro / "outline").mkdir(parents=True); (intro / "delivery" / "latex").mkdir(parents=True)
    (intro / "S-T-Main-1-Intro.md").write_text("# S-T-Main-1-Intro · §1 Introduction\n")
    (intro / "outline" / "S-T-Main-1-Intro-outline-v1.0.md").write_text("outline-version: v1.0\napproved: ✅ JL\n")
    unit = intro / "outline" / "evidence" / "display" / "Display1-one"
    (unit / "assets").mkdir(parents=True)
    (unit / "float.tex").write_text("\\begin{figure}\\includegraphics{x/Display1-one/assets/figure.pdf}\\caption{one}\\label{fig:one}\\end{figure}\n")
    (unit / "preview.pdf").write_bytes(b"%PDF"); (unit / "assets" / "figure.pdf").write_bytes(b"%PDF")
    (unit / "README.md").write_text("# unit\n\n## Placement\nMain; Introduction, Figure 1\n")
    (intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex").write_text(
        "\\section{Introduction}\nSee Figure~\\ref{fig:one}.\n"
        "\\begin{figure}\\includegraphics{displays/S-T-Main-1-Intro/Display1-one/figure.pdf}\\caption{one}\\label{fig:one}\\end{figure}\n")
    (intro / "delivery" / "latex" / "S-T-Main-1-Intro.pdf").write_bytes(b"%PDF")
    # not-ready page: has a declared H1 but no fragment
    methods = root / "Ba-T-Main" / "S-T-Main-2-Methods"; (methods / "outline").mkdir(parents=True)
    (methods / "S-T-Main-2-Methods.md").write_text("# S-T-Main-2-Methods · §2 Methods and Data\n")
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(delivery / "paper-build.toml"))
    spec = importlib.util.spec_from_file_location("build_delivery_under_test", ENGINE)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def _assemble(m):
    """the engine's build() minus latexmk/docx: everything the register needs."""
    m.reset_placement()
    main_ids, appx_ids, _ = m.read_order()
    for d in (m.SEC, m.APP, m.DISP): d.mkdir(parents=True, exist_ok=True)
    main = [m.inspect(i, m.rel(m.CFG["pages"]["main"])) for i in main_ids]
    appx = [m.inspect(i, m.rel(m.CFG["pages"]["appendix"])) for i in appx_ids]
    m.prescan_embedded(main + appx)
    labels = m.label_index(main + appx); unresolved = []
    main_f = [(p, m.place_fragment(p, m.SEC, labels, unresolved) if p["ready"] else []) for p in main]
    appx_f = [(p, m.place_fragment(p, m.APP, labels, unresolved) if p["ready"] else []) for p in appx]
    m.merge_bib(main + appx)
    m.write_master(main_f, appx_f, "DRAFT", sum(p["ready"] for p in main), len(main))
    return m.display_register(main_f, appx_f), m.MASTER.read_text()


def test_engine_knows_its_version_and_paper(paper):
    assert paper.ENGINE_VERSION not in ("", "?")
    assert paper.ROOT.name == "Paper-T" and paper.HERE.name == "delivery"


def test_behavior_A_embedded_display_prints_once(paper):
    register, master = _assemble(paper)
    assert register["figures"] == 1
    assert not [f for f in register["findings"] if "printed twice" in f]
    assert "displays/S-T-Main-1-Intro/Display1-one/float" not in master


def test_behavior_A_expect_fail_register_catches_the_double_print(paper):
    """the Gate-1 lesson: switch the dedupe OFF and the register MUST report it."""
    paper.DEDUPE_EMBEDDED_FLOATS = False
    register, master = _assemble(paper)
    assert register["figures"] == 2
    assert any("printed twice" in f for f in register["findings"])
    assert "displays/S-T-Main-1-Intro/Display1-one/float" in master


def test_behavior_B_not_ready_page_keeps_its_number(paper):
    register, master = _assemble(paper)
    assert "NOT READY" not in master
    assert "\\section{Methods and Data}" in master
    secs = {s["page"]: s for s in register["sections"]}
    assert secs["S-T-Main-2-Methods"]["printed"] == "§2" and secs["S-T-Main-2-Methods"]["declared"] == "§2"
    assert not [f for f in register["findings"] if "S-T-Main-2-Methods" in f]


def test_behavior_C_declared_vs_printed_and_collisions(paper):
    register, _ = _assemble(paper)
    row = next(r for r in register["rows"] if r["unit"] == "S-T-Main-1-Intro/Display1-one")
    assert row["declared"] == "Figure 1" and row["printed"] == "Figure 1"
    # a second unit on disk claiming the same number is a finding even if never printed
    other = paper.ROOT / "Ba-T-Main" / "S-T-Main-2-Methods" / "outline" / "evidence" / "display" / "Display2-two"
    other.mkdir(parents=True)
    (other / "README.md").write_text("## Placement\nMain; Methods, Figure 1\n")
    register, _ = _assemble(paper)
    assert any("Figure 1 claimed by 2 units" in f for f in register["findings"])


def test_order_block_must_be_exactly_one(paper):
    story = paper.rel(paper.CFG["pages"]["order"])
    story.write_text(story.read_text() + "\n<!-- haipipe:compile-order:start -->\n")
    with pytest.raises(RuntimeError):
        paper.read_order()


def _add_unit(page_dir, name, *, preview=True, cite_in_fragment=True, state_line=None, placement="Main; Introduction, Figure 9"):
    """a display unit on a page; optionally without preview, uncited, or folded"""
    u = page_dir / "outline" / "evidence" / "display" / name
    (u / "assets").mkdir(parents=True, exist_ok=True)
    (u / "float.tex").write_text("\\begin{figure}\\caption{x}\\label{fig:" + name + "}\\end{figure}\n")
    if preview: (u / "preview.pdf").write_bytes(b"%PDF")
    head = f"# {name}\n" + (f"{state_line}\n" if state_line else "")
    (u / "README.md").write_text(head + "\n## Placement\n" + placement + "\n")
    if cite_in_fragment:
        frag = page_dir / "delivery" / "latex" / f"{page_dir.name}.tex"
        frag.write_text(frag.read_text() + f"\nSee \\ref{{fig:{name}}}.\n")
    return u


def test_behavior_D_uncited_unit_without_preview_does_not_gate(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    _add_unit(intro, "Display9-orphan", preview=False, cite_in_fragment=False)
    p = m.inspect("S-T-Main-1-Intro", m.rel(m.CFG["pages"]["main"]))
    assert p["ready"], p["reasons"]
    assert any("cited by nothing" in w and "Display9-orphan" in w for w in p["warnings"])


def test_behavior_D_folded_unit_without_preview_does_not_gate(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    _add_unit(intro, "Display3-funnel", preview=False, cite_in_fragment=True,
              state_line="state: 🟣 folded into Display1-one · no standalone display")
    p = m.inspect("S-T-Main-1-Intro", m.rel(m.CFG["pages"]["main"]))
    assert p["ready"], p["reasons"]
    assert any("folded" in w and "Display3-funnel" in w for w in p["warnings"])


def test_behavior_D_cited_live_unit_without_preview_still_gates(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    _add_unit(intro, "Display2-live", preview=False, cite_in_fragment=True)
    p = m.inspect("S-T-Main-1-Intro", m.rel(m.CFG["pages"]["main"]))
    assert not p["ready"]
    assert any("preview.pdf missing for cited unit" in r and "Display2-live" in r for r in p["reasons"])


def test_stale_fragment_is_a_warning_not_a_blocker(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    frag = intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex"
    old = frag.stat().st_mtime - 600
    os.utime(frag, (old, old))                      # the .md is now newer than its fragment
    p = m.inspect("S-T-Main-1-Intro", m.rel(m.CFG["pages"]["main"]))
    assert p["ready"], p["reasons"]
    assert any("fragment may be stale" in w for w in p["warnings"])


def _ready_page(m, pid, number, title, body, *, group="main"):
    """a second ready page with an H1, approved outline, fragment and pdf"""
    g = m.rel(m.CFG["pages"][group]); d = g / pid
    (d / "outline").mkdir(parents=True, exist_ok=True); (d / "delivery" / "latex").mkdir(parents=True, exist_ok=True)
    (d / f"{pid}.md").write_text(f"# {pid} · §{number} {title}\n")
    (d / "outline" / f"{pid}-outline-v1.0.md").write_text("outline-version: v1.0\napproved: ✅ JL\n")
    (d / "delivery" / "latex" / f"{pid}.tex").write_text(body)
    (d / "delivery" / "latex" / f"{pid}.pdf").write_bytes(b"%PDF")
    return d


def _order(m, main_ids):
    story = m.rel(m.CFG["pages"]["order"])
    story.write_text("# StoryA-t-fixture\n<!-- haipipe:compile-order:start -->\nmain:\n" +
                     "".join(f"- {i}\n" for i in main_ids) + "appendix:\n<!-- haipipe:compile-order:end -->\n")


@pytest.mark.parametrize("citer_first", [False, True])
def test_behavior_A_cross_page_ref_prints_the_display_once(paper, citer_first):
    """page 2 \\ref's a figure page 1 embeds; whichever page comes first, one print."""
    m = paper
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods and Data", "\\section{Methods}\nAs Figure~\\ref{fig:one} showed.\n")
    _order(m, ["S-T-Main-2-Methods", "S-T-Main-1-Intro"] if citer_first else ["S-T-Main-1-Intro", "S-T-Main-2-Methods"])
    register, master = _assemble(m)
    assert register["figures"] == 1, register["rows"]
    assert not [f for f in register["findings"] if "printed twice" in f]
    assert master.count("displays/S-T-Main-1-Intro/Display1-one/float") == 0


def test_reader_document_carries_no_reasons_and_no_build_counts(paper):
    register, master = _assemble(paper)
    assert "[This section is not yet compiled into this build.]" in master
    assert "outline not approved" not in master and "no body fragment" not in master
    assert "pages ready" not in master and "built 20" not in master


def test_bib_key_collision_is_warned(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    (intro / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (intro / "outline" / "evidence" / "bibex" / "a.bib").write_text("@article{k1, title={One}, year={2020}}\n")
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods and Data", "\\section{Methods}\n\\citep{k1}\n")
    methods = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-2-Methods"
    (methods / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (methods / "outline" / "evidence" / "bibex" / "b.bib").write_text("@article{k1, title={One, revised}, year={2021}}\n")
    _assemble(m)
    assert any("bib key k1 differs" in w for w in m.BUILD_WARNINGS)
    assert m.BIB.read_text().count("@article{k1") == 1


def test_one_work_under_two_keys_is_a_finding_when_both_are_cited(paper):
    """expect-fail proof for 0.7.7: this IS the broken state (§1 and §2 spell the same
    article differently), and the register must say the reference list prints it twice."""
    m = paper
    doi = "10.1257/pol.20160094"
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    (intro / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (intro / "outline" / "evidence" / "bibex" / "a.bib").write_text(
        "@article{Author_2018, title={The Effect}, author={Author, A.}, year={2018}, doi={%s}}\n" % doi)
    (intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex").write_text(
        "\\section{Introduction}\n\\citep{Author_2018}\n")
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods and Data", "\\section{Methods}\n\\citep{author2018effect}\n")
    methods = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-2-Methods"
    (methods / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (methods / "outline" / "evidence" / "bibex" / "b.bib").write_text(
        "@article{author2018effect, title={the effect}, author={Author, A}, year={2018}, doi={%s}}\n" % doi)
    reg, _ = _assemble(m)
    hit = [f for f in reg["findings"] if "prints it twice" in f]
    assert hit, reg["findings"]
    assert "Author_2018" in hit[0] and "author2018effect" in hit[0]


def test_duplicate_work_is_found_when_only_one_twin_carries_a_doi(paper):
    """the hole the first 0.7.7 draft had: a hand-written entry has no `doi` while its
    Crossref twin does, so a doi-FIRST identity bucketed them apart and found nothing.
    Titles also differ in case and brace protection ({CDC} vs CDC)."""
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    (intro / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (intro / "outline" / "evidence" / "bibex" / "a.bib").write_text(
        "@article{dowell2016cdc, title={{CDC} guideline for prescribing opioids}, author={Dowell, D}, year={2016}}\n")
    (intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex").write_text(
        "\\section{Introduction}\n\\citep{dowell2016cdc}\n")
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods and Data", "\\section{Methods}\n\\citep{Dowell_2016}\n")
    methods = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-2-Methods"
    (methods / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (methods / "outline" / "evidence" / "bibex" / "b.bib").write_text(
        "@article{Dowell_2016, title={CDC Guideline for Prescribing Opioids}, author={Dowell, Deborah}, "
        "year={2016}, DOI={10.1001/jama.2016.1464}}\n")
    reg, _ = _assemble(m)
    hit = [f for f in reg["findings"] if "prints it twice" in f]
    assert hit, reg["findings"]
    assert "dowell2016cdc" in hit[0] and "Dowell_2016" in hit[0]


def test_one_work_under_two_keys_is_only_a_warning_when_one_is_cited(paper):
    """the spare key is staged but never cited: nothing prints twice yet, so it is a
    warning about the trap, not a finding that blocks."""
    m = paper
    doi = "10.1257/pol.20160094"
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    (intro / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (intro / "outline" / "evidence" / "bibex" / "a.bib").write_text(
        "@article{Author_2018, title={The Effect}, author={Author, A.}, year={2018}, doi={%s}}\n"
        "@article{author2018effect, title={the effect}, author={Author, A}, year={2018}, doi={%s}}\n" % (doi, doi))
    (intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex").write_text(
        "\\section{Introduction}\n\\citep{Author_2018}\n")
    reg, _ = _assemble(m)
    assert not [f for f in reg["findings"] if "prints it twice" in f], reg["findings"]
    assert any("staged under 2 keys" in w for w in m.BUILD_WARNINGS), m.BUILD_WARNINGS


def _abstract_page(m, prose, title=None):
    """an Abstract page: no §, an abstract environment, optionally its own ### Title."""
    d = _ready_page(m, "S-T-Main-Abstract", 0, "Abstract",
                    "\\begin{abstract}\n" + prose + "\n\\end{abstract}\n")
    head = "# S-T-Main-Abstract \u00b7 Abstract\n"
    if title:
        head += f"\n### Title\n\n{title}\n"
    (d / "S-T-Main-Abstract.md").write_text(head + "\n## Content\n")
    _order(m, ["S-T-Main-Abstract", "S-T-Main-1-Intro", "S-T-Main-2-Methods"])
    return d


def test_abstract_page_title_wins_over_the_config(paper):
    """expect-fail proof for 0.7.8: paper-build.toml and the Abstract page both carry a
    title and they drifted. The PAGE is printed, and the drift is a finding."""
    m = paper
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods", "\\section{Methods}\nText.\n")
    _abstract_page(m, "One two three four five six seven eight nine ten.", title="The Page's Own Title")
    reg, master = _assemble(m)
    assert "The Page's Own Title" in master, master[:500]
    assert any("title drift" in f for f in reg["findings"]), reg["findings"]


def test_venue_pack_abstract_band_is_a_finding(paper, monkeypatch):
    """the venue pack measured MISQ at 120-160 words and 4-7 sentences and NOTHING read
    it, so a 168-word 10-sentence abstract passed every gate (JL 260908). The keyword
    line must not be counted: stripping \\textbf{Keywords:} leaves the bare keywords."""
    m = paper
    monkeypatch.setitem(m.PROFILE, "abstract_words", [120, 160])
    monkeypatch.setitem(m.PROFILE, "abstract_sentences", [4, 7])
    monkeypatch.setitem(m.PROFILE, "venue_pack", "playbook-utd-is/MISQ")
    _ready_page(m, "S-T-Main-2-Methods", 2, "Methods", "\\section{Methods}\nText.\n")
    _abstract_page(m, "This sentence carries exactly seven ordinary words. " * 9
                   + "\n\n\\smallskip\n\\noindent\\textbf{Keywords:} alpha, beta, gamma, delta, epsilon, zeta")
    reg, _ = _assemble(m)
    hits = [f for f in reg["findings"] if f.startswith("abstract is")]
    assert any("sentences" in f for f in hits), reg["findings"]
    assert all("playbook-utd-is/MISQ" in f for f in hits), hits
    words = next((f for f in hits if "words" in f), "")
    assert "63 words" in words, words   # 9 x 7, and NOT 69 with the six keywords


def test_profile_latex_switches_reach_the_master(paper, monkeypatch):
    m = paper
    monkeypatch.setattr(m, "LATEX_SPACING", "double"); monkeypatch.setattr(m, "LATEX_DISPLAYS", "end")
    monkeypatch.setattr(m, "LATEX_APPENDIX_NEWPAGE", True); monkeypatch.setattr(m, "LATEX_TITLE_PAGE", "separate")
    monkeypatch.setattr(m, "LATEX_ABSTRACT_PAGE", True); monkeypatch.setattr(m, "LATEX_BIBSTYLE", "plainnat")
    _, master = _assemble(m)
    assert "\\doublespacing" in master and "endfloat" in master and "\\bibliographystyle{plainnat}" in master
    assert "\\maketitle\n\\thispagestyle{empty}\n\\clearpage" in master


def test_misq_profile_ships_with_the_latex_table():
    import tomllib
    prof = tomllib.loads((ENGINE.parents[1] / "profiles" / "misq.toml").read_text())
    assert prof["latex"]["spacing"] == "double" and prof["latex"]["appendix_newpage"] is True
    assert prof["latex"]["displays"] in ("inline", "end") and prof["venue_label"] == "MIS Quarterly"


def test_missing_latexmk_is_reported_not_a_traceback(paper, monkeypatch):
    m = paper
    def boom(cmd, **kw): raise FileNotFoundError(cmd[0])
    monkeypatch.setattr(m.subprocess, "run", boom)
    m.build()
    import json
    manifest = json.loads((m.HERE / "build-manifest.json").read_text())
    assert manifest["render"]["latexmk_rc"] == 127 and manifest["status"] == "DRAFT"
    assert "not found" in manifest["render"]["latexmk_tail"]


def test_round_freeze_copies_all_declared_outputs_and_is_immutable(paper):
    """send/release must include a declared supplement and never overwrite a snapshot."""
    m = paper
    m.OUT.update({
        "supplement_pdf": "latex/T-supp.pdf",
        "supplement_docx": "word/T-supp.docx",
    })
    for configured in m.OUT.values():
        path = m.rel(configured)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"%PDF" if path.suffix == ".pdf" else b"artifact")
    (m.HERE / "display-register.md").write_text("# display register\n")
    round_dir = m.ROOT / "Bc-T-Round" / "RD01-T-review-20260908"
    round_dir.mkdir(parents=True)

    m.freeze("sent", "RD01")
    snapshot = round_dir / "sent"
    assert (snapshot / "T.pdf").exists()
    assert (snapshot / "T.docx").exists()
    assert (snapshot / "T-supp.pdf").exists()
    assert (snapshot / "T-supp.docx").exists()
    assert (snapshot / "build-manifest.json").exists()
    assert (snapshot / "display-register.md").exists()

    with pytest.raises(SystemExit, match="immutable"):
        m.freeze("sent", "RD01")


def test_display_unit_folder_grammar_is_a_register_tooth(paper):
    """0.7.5 (JL 260908, third pass): page id carries the index (S-T-Main-1-Intro), unit is Display<n>-<slug>.

    Legacy shapes (S-Display-*, Sec1-Display1-*, <PageID>-Display1-*) are findings; a page whose folder
    index disagrees with its H1, or whose H1 is numbered while the id carries no index, is a finding.
    """
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"          # H1 says §1, id says 1 → agree
    disp = intro / "outline" / "evidence" / "display"
    for name in ("Display2-good", "Sec1-Display3-old-second-pass", "S-Display-4-oldest", "S-T-Main-1-Intro-Display5-pageid"):
        (disp / name).mkdir(parents=True); (disp / name / "README.md").write_text("## Placement\nMain; Introduction, Figure 7\n")
    wrong = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-9-Wrong"; wrong.mkdir()
    (wrong / "S-T-Main-9-Wrong.md").write_text("# S-T-Main-9-Wrong · §3 Wrong Index\n")
    noidx = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Unindexed"; noidx.mkdir()
    (noidx / "S-T-Main-Unindexed.md").write_text("# S-T-Main-Unindexed · §4 Needs An Index\n")
    register, _ = _assemble(m)
    F = register["findings"]
    assert not any("Display2-good" in f and "legacy" in f for f in F)
    for bad in ("Sec1-Display3-old-second-pass", "S-Display-4-oldest", "S-T-Main-1-Intro-Display5-pageid"):
        assert any(f.startswith("legacy unit name") and bad in f for f in F), bad
    assert any("S-T-Main-9-Wrong: folder index 9 but its H1 says §3" in f for f in F)
    assert any("S-T-Main-Unindexed: H1 says §4 but the page id carries no index" in f for f in F)


def test_conforming_unit_is_not_a_finding_and_unnumbered_pages_are_allowed(paper):
    m = paper
    abstract = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Abstract"; abstract.mkdir()
    (abstract / "S-T-Main-Abstract.md").write_text("# S-T-Main-Abstract · Abstract\n")
    register, _ = _assemble(m)
    assert not any("Display1-one" in f and "legacy" in f for f in register["findings"])
    assert not any("S-T-Main-Abstract" in f for f in register["findings"])


def test_inner_section_headings_shift_numbers_and_are_a_finding(paper):
    """a fragment whose inner divisions use \\section prints several numbered sections (0.7.6 tooth)."""
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-1-Intro"
    frag = intro / "delivery" / "latex" / "S-T-Main-1-Intro.tex"
    frag.write_text(frag.read_text() + "\n\\section{Study design}\nInner text.\n")
    register, _ = _assemble(m)
    secs = {s_["page"]: s_ for s_ in register["sections"]}
    assert secs["S-T-Main-1-Intro"]["printed"] == "§1"
    assert secs["S-T-Main-2-Methods"]["printed"] == "§3"                      # shifted by the inner \\section
    assert any("S-T-Main-1-Intro: its fragment prints 2 numbered sections" in f for f in register["findings"])
    assert any("S-T-Main-2-Methods: page H1 says §2, prints §3" in f for f in register["findings"])
