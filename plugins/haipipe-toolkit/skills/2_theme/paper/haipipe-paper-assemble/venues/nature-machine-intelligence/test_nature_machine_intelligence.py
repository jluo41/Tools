"""Nature Machine Intelligence: generic layout, numbered citations, Extended Data as the supplement."""
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROF = tomllib.loads((HERE / "profile.toml").read_text(encoding="utf-8"))


def test_generic_layout_numbered_citations():
    assert PROF["layout"] == "generic" and not (HERE / "venue.py").exists()
    assert PROF["citation_style"] == "numeric" and PROF["latex"]["bibstyle"] == "unsrtnat"


def test_word_limit_counts_main_text_only():
    assert PROF["main_text_word_limit"] == 3500 and PROF["back_matter_headings"] == ["Methods"]


def test_extended_data_and_availability_sections():
    assert PROF["supplement_table_prefix"] == "Extended Data Table " and PROF["appendix_heading"] is False
    assert PROF["word_top_level"] == ["Data availability", "Code availability"]
