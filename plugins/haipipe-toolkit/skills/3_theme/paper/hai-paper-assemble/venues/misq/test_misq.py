"""MIS Quarterly: a blind copy in the generic layout, author-date, double-spaced."""
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROF = tomllib.loads((HERE / "profile.toml").read_text(encoding="utf-8"))


def test_generic_layout_blind_copy():
    assert PROF["layout"] == "generic" and not (HERE / "venue.py").exists()
    assert PROF["title_page_fields"] == ["title"] and PROF["latex"]["acknowledgments"] is False


def test_author_date_double_spaced():
    assert PROF["citation_style"] == "author-date" and PROF["latex"]["bibstyle"] == "apalike"
    assert PROF["latex"]["spacing"] == "double" and "title_block" not in PROF["latex"]
