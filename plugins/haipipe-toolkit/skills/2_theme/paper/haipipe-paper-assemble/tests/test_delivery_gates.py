"""The engine's gates on a paper's readiness: the compile order, an approved outline and G4 (haipipe-paper-assemble).

Moved here from Paper-AgreeablePrescriptionDiscretion/tests/ on 2026-10-20: they test the engine, which every
paper's delivery/build.py execs, so they belong with it. Runs without LaTeX and changes no live artifact.
"""
import importlib.util
from pathlib import Path

import pytest

ENGINE = Path(__file__).resolve().parents[1] / "scripts" / "build_delivery.py"
STORY = "s02-story-fixture.md"


@pytest.fixture
def adapter(tmp_path, monkeypatch):
    config = tmp_path / "delivery" / "paper-build.toml"
    config.parent.mkdir(parents=True)
    config.write_text('[paper]\nid = "Paper-T"\ntitle = "T"\n[pages]\nmain = "../j01_v0101_desk"\n'
                      'appendix = "../j01_v0101_desk"\norder = "../%s"\n'
                      '[source]\nroom = "latex"\nmaster = "master.tex"\nsections = "sections"\n'
                      'appendices = "appendices"\ndisplays = "displays"\nbibliography = "reference.bib"\n'
                      '[evidence]\nmode = "draft"\n[outputs]\nmain_pdf = "latex/T.pdf"\nmain_docx = "word/T.docx"\nmanifest = "build-manifest.json"\n' % STORY)
    monkeypatch.setenv("HAIPIPE_PAPER_BUILD_CONFIG", str(config))
    spec = importlib.util.spec_from_file_location("delivery_gates_under_test", ENGINE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "HERE", tmp_path / "delivery")
    monkeypatch.setattr(module, "CFG", {"pages": {"order": "../" + STORY}})
    return module


def order_text(main="- t01_introduction", appendix=""):
    return (
        "<!-- haipipe:compile-order:start -->\nmain:\n"
        f"{main}\nappendix:\n{appendix}\n"
        "<!-- haipipe:compile-order:end -->"
    )


def make_section(root, versions):
    pid = "t01_introduction"
    (root / "board.md").write_text("board-kind: paper-board\n")   # Delivery needs a containing Block
    group = root / "j01_v0101_desk"
    page = group / pid
    (page / "draft").mkdir(parents=True)
    (page / "delivery" / "latex").mkdir(parents=True)
    (page / "delivery" / "latex" / f"{pid}.tex").write_text("Section body.")
    (page / "delivery" / "latex" / f"{pid}.pdf").write_bytes(b"test PDF placeholder")
    for version, contents in versions.items():
        (page / "draft" / f"{pid}-outline-{version}.md").write_text(contents)
    return pid, group


def test_order_comes_from_story(adapter):
    (adapter.ROOT / STORY).write_text(order_text())
    assert adapter.read_order()[:2] == (["t01_introduction"], [])


@pytest.mark.parametrize("text", ["", order_text() + "\n" + order_text()])
def test_missing_or_multiple_order_blocks_fail(adapter, text):
    (adapter.ROOT / STORY).write_text(text)
    with pytest.raises(RuntimeError):
        adapter.read_order()


@pytest.mark.parametrize("text", [
    order_text(main="- t01_introduction\n- t01_introduction"),
    order_text(appendix="- t01_introduction"),
    order_text(main="- t01_introduction\n- typo_section"),
    order_text() + "\n<!-- haipipe:compile-order:start -->",
])
def test_ambiguous_or_malformed_order_never_silently_drops_entries(adapter, text):
    (adapter.ROOT / STORY).write_text(text)
    with pytest.raises(RuntimeError):
        adapter.read_order()


@pytest.mark.parametrize("versions", [
    {"v1.0": "outline-version: v1.0\napproved: ⬜\n"},
    {"v1.0": "approved: ✅ JL\n", "v1.1": "approved: ⬜\n"},
    {"v1.9": "approved: ✅ JL\n", "v1.10": "approved: ⬜\n"},
    {"v0.2": "outline-version: v0.2\napproved: ⬜\n"},
    {"v0.2": "outline-version: v0.2\napproved: ✅ JL\n"},
    {"v1.0": "outline-version: v0.2\napproved: ✅ JL\n"},
    {"v1.0": "approved: ✅ JL\n", "v0.3": "supersedes: v1.0\napproved: ⬜\n"},
    {"v1.0": "outline-version: v1.0\napproved: ⬜\napproved: ✅ JL\n"},
])
def test_filename_or_other_revision_is_not_approval(adapter, versions):
    pid, group = make_section(adapter.ROOT, versions)
    before = {p: p.read_bytes() for p in (group / pid / "draft").iterdir()}
    result = adapter.inspect(pid, group)
    assert not result["ready"]
    assert any("outline" in reason for reason in result["reasons"])
    assert before == {p: p.read_bytes() for p in before}


def test_admission_records_exact_approved_outline(adapter):
    pid, group = make_section(adapter.ROOT, {
        "v1.0": "outline-version: v1.0\napproved: ✅ · JL · explicit approval\n",
    })
    result = adapter.inspect(pid, group)
    assert result["ready"]
    assert result["outline"]["version"] == "v1.0"
    assert result["outline"]["approval"].startswith("✅")


def test_quoted_approval_is_not_current_approval(adapter):
    pid, group = make_section(adapter.ROOT, {
        "v1.0": "outline-version: v1.0\n\n## Notes\n```\napproved: ✅ JL\n```\n",
    })
    assert not adapter.inspect(pid, group)["ready"]


def test_renderable_sections_do_not_close_g4(adapter):
    readiness = adapter.build_readiness(
        [{"id": "t01_introduction", "ready": True}],
        unresolved=[], latex_rc=0, docx_rc=0,
    )
    assert readiness["status"] == "DRAFT"
    assert readiness["blockers"]


def test_render_failures_remain_explicit(adapter):
    readiness = adapter.build_readiness([], unresolved=["missing-label"], latex_rc=1)
    assert readiness["status"] == "DRAFT"
    assert any("LaTeX" in reason for reason in readiness["blockers"])
    assert any("reference" in reason for reason in readiness["blockers"])
