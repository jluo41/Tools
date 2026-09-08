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
        "# StoryA-t-fixture\n<!-- haipipe:compile-order:start -->\nmain:\n- S-T-Main-Intro\n- S-T-Main-Methods\n"
        "appendix:\n<!-- haipipe:compile-order:end -->\n")
    (root / "Bb-T-Appendix").mkdir()
    # ready page: fragment embeds the float (as md2tex does) AND cites it
    intro = root / "Ba-T-Main" / "S-T-Main-Intro"
    (intro / "outline").mkdir(parents=True); (intro / "delivery" / "latex").mkdir(parents=True)
    (intro / "S-T-Main-Intro.md").write_text("# S-T-Main-Intro · §1 Introduction\n")
    (intro / "outline" / "S-T-Main-Intro-outline-v1.0.md").write_text("outline-version: v1.0\napproved: ✅ JL\n")
    unit = intro / "outline" / "evidence" / "display" / "S-Display-1-one"
    (unit / "assets").mkdir(parents=True)
    (unit / "float.tex").write_text("\\begin{figure}\\includegraphics{x/S-Display-1-one/assets/figure.pdf}\\caption{one}\\label{fig:one}\\end{figure}\n")
    (unit / "preview.pdf").write_bytes(b"%PDF"); (unit / "assets" / "figure.pdf").write_bytes(b"%PDF")
    (unit / "README.md").write_text("# unit\n\n## Placement\nMain; Introduction, Figure 1\n")
    (intro / "delivery" / "latex" / "S-T-Main-Intro.tex").write_text(
        "\\section{Introduction}\nSee Figure~\\ref{fig:one}.\n"
        "\\begin{figure}\\includegraphics{displays/S-Display-1-one/figure.pdf}\\caption{one}\\label{fig:one}\\end{figure}\n")
    (intro / "delivery" / "latex" / "S-T-Main-Intro.pdf").write_bytes(b"%PDF")
    # not-ready page: has a declared H1 but no fragment
    methods = root / "Ba-T-Main" / "S-T-Main-Methods"; (methods / "outline").mkdir(parents=True)
    (methods / "S-T-Main-Methods.md").write_text("# S-T-Main-Methods · §2 Methods and Data\n")
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
    assert "displays/S-Display-1-one/float" not in master


def test_behavior_A_expect_fail_register_catches_the_double_print(paper):
    """the Gate-1 lesson: switch the dedupe OFF and the register MUST report it."""
    paper.DEDUPE_EMBEDDED_FLOATS = False
    register, master = _assemble(paper)
    assert register["figures"] == 2
    assert any("printed twice" in f for f in register["findings"])
    assert "displays/S-Display-1-one/float" in master


def test_behavior_B_not_ready_page_keeps_its_number(paper):
    register, master = _assemble(paper)
    assert "NOT READY" not in master
    assert "\\section{Methods and Data}" in master
    secs = {s["page"]: s for s in register["sections"]}
    assert secs["S-T-Main-Methods"]["printed"] == "§2" and secs["S-T-Main-Methods"]["declared"] == "§2"
    assert not [f for f in register["findings"] if "S-T-Main-Methods" in f]


def test_behavior_C_declared_vs_printed_and_collisions(paper):
    register, _ = _assemble(paper)
    row = next(r for r in register["rows"] if r["unit"] == "S-Display-1-one")
    assert row["declared"] == "Figure 1" and row["printed"] == "Figure 1"
    # a second unit on disk claiming the same number is a finding even if never printed
    other = paper.ROOT / "Ba-T-Main" / "S-T-Main-Methods" / "outline" / "evidence" / "display" / "S-Display-2-two"
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
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    _add_unit(intro, "S-Display-9-orphan", preview=False, cite_in_fragment=False)
    p = m.inspect("S-T-Main-Intro", m.rel(m.CFG["pages"]["main"]))
    assert p["ready"], p["reasons"]
    assert any("cited by nothing" in w and "S-Display-9-orphan" in w for w in p["warnings"])


def test_behavior_D_folded_unit_without_preview_does_not_gate(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    _add_unit(intro, "S-Display-3a-funnel", preview=False, cite_in_fragment=True,
              state_line="state: 🟣 folded into S-Display-1-one · no standalone display")
    p = m.inspect("S-T-Main-Intro", m.rel(m.CFG["pages"]["main"]))
    assert p["ready"], p["reasons"]
    assert any("folded" in w and "S-Display-3a-funnel" in w for w in p["warnings"])


def test_behavior_D_cited_live_unit_without_preview_still_gates(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    _add_unit(intro, "S-Display-2-live", preview=False, cite_in_fragment=True)
    p = m.inspect("S-T-Main-Intro", m.rel(m.CFG["pages"]["main"]))
    assert not p["ready"]
    assert any("preview.pdf missing for cited unit" in r and "S-Display-2-live" in r for r in p["reasons"])


def test_stale_fragment_is_a_warning_not_a_blocker(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    frag = intro / "delivery" / "latex" / "S-T-Main-Intro.tex"
    old = frag.stat().st_mtime - 600
    os.utime(frag, (old, old))                      # the .md is now newer than its fragment
    p = m.inspect("S-T-Main-Intro", m.rel(m.CFG["pages"]["main"]))
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
    _ready_page(m, "S-T-Main-Methods", 2, "Methods and Data", "\\section{Methods}\nAs Figure~\\ref{fig:one} showed.\n")
    _order(m, ["S-T-Main-Methods", "S-T-Main-Intro"] if citer_first else ["S-T-Main-Intro", "S-T-Main-Methods"])
    register, master = _assemble(m)
    assert register["figures"] == 1, register["rows"]
    assert not [f for f in register["findings"] if "printed twice" in f]
    assert master.count("displays/S-Display-1-one/float") == 0


def test_reader_document_carries_no_reasons_and_no_build_counts(paper):
    register, master = _assemble(paper)
    assert "[This section is not yet compiled into this build.]" in master
    assert "outline not approved" not in master and "no body fragment" not in master
    assert "pages ready" not in master and "built 20" not in master


def test_bib_key_collision_is_warned(paper):
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    (intro / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (intro / "outline" / "evidence" / "bibex" / "a.bib").write_text("@article{k1, title={One}, year={2020}}\n")
    _ready_page(m, "S-T-Main-Methods", 2, "Methods and Data", "\\section{Methods}\n\\citep{k1}\n")
    methods = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Methods"
    (methods / "outline" / "evidence" / "bibex").mkdir(parents=True)
    (methods / "outline" / "evidence" / "bibex" / "b.bib").write_text("@article{k1, title={One, revised}, year={2021}}\n")
    _assemble(m)
    assert any("bib key k1 differs" in w for w in m.BUILD_WARNINGS)
    assert m.BIB.read_text().count("@article{k1") == 1


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
    """<PageID>-Display<N>-<slug> passes; the retired S-Display-* shape is a finding (JL 260908: unify)."""
    m = paper
    intro = m.rel(m.CFG["pages"]["main"]) / "S-T-Main-Intro"
    good = intro / "outline" / "evidence" / "display" / "S-T-Main-Intro-Display2-good"
    good.mkdir(parents=True); (good / "README.md").write_text("## Placement\nMain; Introduction, Figure 7\n")
    register, _ = _assemble(m)
    legacy = [f for f in register["findings"] if f.startswith("legacy unit name")]
    assert any("S-Display-1-one" in f for f in legacy)          # the fixture's own unit is legacy-named on purpose
    assert not any("S-T-Main-Intro-Display2-good" in f for f in legacy)
