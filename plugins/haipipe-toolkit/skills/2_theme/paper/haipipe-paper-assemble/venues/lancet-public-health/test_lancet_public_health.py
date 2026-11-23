"""The Lancet Public Health: the JAMA manuscript layout under the Lancet's own labels and citation rules."""
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROF = tomllib.loads((HERE / "profile.toml").read_text(encoding="utf-8"))


def test_reuses_the_jama_layout_and_what_it_reads():
    assert PROF["layout"] == "jama-internal-medicine" and not (HERE / "venue.py").exists()
    assert PROF["latex"]["title_block"] == "center" and PROF["latex"]["supplement_float_names"] == ["eTable", "eFigure"]


def test_its_own_labels_and_citations():
    assert PROF["abstract_heading"] == "Summary" and PROF["key_points_heading"] == "Research in context"
    assert PROF["cite_after_punctuation"] == ".,;:" and PROF["latex"]["bibstyle"] == "vancouver"
