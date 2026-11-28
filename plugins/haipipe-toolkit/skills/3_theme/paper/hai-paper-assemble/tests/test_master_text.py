"""What a reader copies from the built PDF is what the source wrote (AgreeableJama-Board 261122)."""
from test_build_delivery import _assemble, paper  # noqa: F401  (paper is the fixture)


def test_master_copies_a_semicolon_as_a_semicolon(paper):
    """Times New Roman maps ";" and U+037E to one glyph; ActualText keeps a copied ";" U+003B."""
    _, master = _assemble(paper)
    assert master.index("\\XeTeXgenerateactualtext=1") < master.index("\\documentclass")
