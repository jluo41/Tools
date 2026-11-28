"""JAMA Internal Medicine: the Word file has its own shape (venue.py), and the PDF gives that shape what it reads."""
import ast
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROF = tomllib.loads((HERE / "profile.toml").read_text(encoding="utf-8"))


def test_the_layout_is_this_folder_and_prints_its_own_word_file():
    assert PROF["layout"] == HERE.name
    tree = ast.parse((HERE / "venue.py").read_text(encoding="utf-8"))
    assert "build_word" in {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}


def test_the_master_carries_what_build_word_parses():
    latex = PROF["latex"]
    assert latex["title_block"] == "center" and latex["abstract_as_written"] is True
    assert latex["section_headings"] == ["Introduction", "Methods", "Results", "Discussion"]
    assert latex["supplement_float_names"] == ["eTable", "eFigure"]


def test_the_supplement_and_its_bibliography_style():
    assert PROF["supplement_table_prefix"] == "eTable " and PROF["supplement_contents"] is True
    assert (HERE / "jama-ama.bst").is_file()


def test_references_print_their_doi():
    """AMA prints a DOI when one exists; the venue's own .bst does, stock vancouver.bst does not."""
    assert PROF["latex"]["bibstyle"] == "jama-ama"
    bst = (HERE / "jama-ama.bst").read_text(encoding="utf-8")
    assert "#1 'adddoiresolver :=" in bst and "FUNCTION {format.url}" in bst
