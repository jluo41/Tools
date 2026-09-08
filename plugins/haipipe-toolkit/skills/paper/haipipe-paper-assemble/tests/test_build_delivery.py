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
    main_ids, appx_ids, _ = m.read_order()
    for d in (m.SEC, m.APP, m.DISP): d.mkdir(parents=True, exist_ok=True)
    main = [m.inspect(i, m.rel(m.CFG["pages"]["main"])) for i in main_ids]
    appx = [m.inspect(i, m.rel(m.CFG["pages"]["appendix"])) for i in appx_ids]
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
