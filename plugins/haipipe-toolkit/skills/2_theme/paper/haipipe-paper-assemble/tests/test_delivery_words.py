"""delivery_words.py: a Section whose Content was never adopted from its Draft is named (LLMRecJamaAI 261122)."""
import re
from pathlib import Path

NS = {"re": re, "Path": Path}
exec((Path(__file__).resolve().parents[1] / "scripts" / "delivery_words.py").read_text(encoding="utf-8"), NS)


def section(tmp_path, content, draft=True):
    d = tmp_path / "t02_methods"
    (d / "draft").mkdir(parents=True)
    (d / "t02_methods.md").write_text(f"# t02_methods · Methods\n\n## Content\n\n{content}\n\n## Aims\n\n- x\n")
    if draft:
        (d / "draft" / "t02_methods-draft-v0.3.md").write_text("word " * 2300)
    return d


def test_a_placeholder_content_beside_a_draft_is_named(tmp_path):
    d = section(tmp_path, "<the Section's prose, adopted from its Draft>")
    [line] = NS["unadopted"](d, "t02_methods")
    assert "t02_methods-draft-v0.3.md has 2300 words" in line and "page.py adopt t02_methods" in line


def test_adopted_content_or_no_draft_is_quiet(tmp_path):
    assert NS["unadopted"](section(tmp_path, "We did it. <!-- realizes: C1.P1.B1 -->"), "t02_methods") == []
    assert NS["unadopted"](section(tmp_path / "x", "<placeholder>", draft=False), "t02_methods") == []
