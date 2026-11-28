"""Nature Portfolio: the series rules, and a journal table that changes only its own values."""
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
from venue_profile import load  # noqa: E402

PROF = tomllib.loads((HERE / "profile.toml").read_text(encoding="utf-8"))


def test_series_rules():
    assert PROF["layout"] == "generic" and not (HERE / "venue.py").exists()
    assert PROF["citation_style"] == "numeric" and PROF["back_matter_headings"] == ["Methods"]
    assert PROF["word_top_level"] == ["Data availability", "Code availability"]
    assert PROF["supplement_table_prefix"] == "Extended Data Table " and PROF["appendix_heading"] is False


def test_journal_table_on_top_of_series():
    nmi = load("nature/nature-machine-intelligence")
    assert nmi["venue_label"] == "Nature Machine Intelligence" and nmi["main_text_word_limit"] == 3500
    assert nmi["citation_style"] == "numeric" and "journals" not in nmi


def test_paper_overrides_last_and_latex_merges_key_by_key():
    p = load("nature/nature-machine-intelligence", {"supplement_title": "SI", "latex": {"bibstyle": "naturemag"}})
    assert p["supplement_title"] == "SI" and p["latex"] == {**PROF["latex"], "bibstyle": "naturemag"}
