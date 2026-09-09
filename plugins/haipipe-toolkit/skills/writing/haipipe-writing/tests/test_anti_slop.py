#!/usr/bin/env python3
"""Regression tests for the optional, read-only anti-slop adapter."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cli"))
import anti_slop  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
RULES = anti_slop.load_rules()


def test_rule_findings_have_stable_locations():
    text = "This is a pivotal and robust approach.\nIt is not just useful but clear — today.\n"
    result = anti_slop.audit_text(text, RULES)
    assert result["diagnostic_only"] is True
    assert result["finding_count"] >= 4
    assert result["findings"][0]["line"] == 1
    assert result["findings"][0]["column"] == 11
    assert result["stats"]["short_sample"] is True


def test_unicode_emoji_rule_works_in_python_adapter():
    result = anti_slop.audit_text("A result 😊 is here.", RULES)
    assert [item["id"] for item in result["findings"]] == ["emoji"]


def test_markdown_non_prose_is_masked_without_moving_lines():
    text = (
        "---\n"
        "title: pivotal\n"
        "---\n"
        "This is pivotal.\n"
        "```\n"
        "pivotal robust\n"
        "```\n"
        "Use `robust` and visit https://example.com/pivotal.\n"
    )
    result = anti_slop.audit_text(text, RULES)
    matches = [item for item in result["findings"] if item["match"].lower() == "pivotal"]
    assert len(matches) == 1
    assert matches[0]["line"] == 4


def test_fact_extraction_preserves_quotes_and_inner_hard_facts():
    text = (
        'Release v0.9.0 on 2026-09-08: API handles 42 cases at 17.5%. '
        'The approved address is "C1.P2".\n'
    )
    facts = anti_slop.extract_facts(text)
    assert facts["dates"] == ["2026-09-08"]
    assert facts["percentages"] == ["17.5%"]
    assert facts["versions"] == ["0.9.0"]
    assert facts["numbers"] == ["42"]
    assert facts["acronyms"] == ["API", "C1", "P2"]
    assert facts["citations"] == []
    assert facts["quoted_terms"] == ['"C1.P2"']


def test_citation_author_is_preserved_when_formatting_changes():
    before = "The result is supported by (Lee et al., 2025)."
    after = "Lee et al. (2025) support the result."
    clean = anti_slop.compare_facts(before, after)
    assert clean["ok"] is True
    assert clean["missing"] == {}

    changed = anti_slop.compare_facts(
        before, "The result is supported by (Kim et al., 2025)."
    )
    assert changed["ok"] is False
    assert changed["missing"]["citations"] == ["Lee et al. 2025"]


def test_fact_compare_accepts_reformatted_values_and_flags_loss():
    before = (
        'Release v0.9.0 on 2026-09-08: API handles 42 cases at 17.5%. '
        'See https://example.com/v0.9.0?q=42 and email team@example.org. '
        'The term "C1.P2" is approved.\n'
    )
    after = (
        'On September 8, 2026, API handles forty-two cases at 17.5%. '
        'See https://example.com/v0.9.0?q=42 and email team@example.org. '
        'The term "C1.P2" is approved.\n'
    )
    clean = anti_slop.compare_facts(before, after)
    assert clean["ok"] is True
    assert clean["missing"] == {}

    lossy = anti_slop.compare_facts(before, "The rewrite omits the source URL and 42.")
    assert lossy["ok"] is False
    assert "https://example.com/v0.9.0?q=42" in lossy["missing"]["urls"]
    assert "team@example.org" in lossy["missing"]["emails"]
    assert "2026-09-08" in lossy["missing"]["dates"]
    assert '"C1.P2"' in lossy["missing"]["quoted_terms"]
    assert lossy["critical_missing_count"] >= 3


def test_cli_json_is_machine_readable_and_no_write_mode_exists():
    result = anti_slop.audit_text("A plain sentence.", RULES)
    payload = json.dumps(result, sort_keys=True)
    assert json.loads(payload)["tool"] == "haipipe-writing/anti_slop.py"
    assert not hasattr(anti_slop._parser().parse_args(["audit", "-"]), "fix")


if __name__ == "__main__":
    tests = [value for name, value in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print("✅", test.__name__)
    print(f"✅ {len(tests)} anti-slop tests passed")
