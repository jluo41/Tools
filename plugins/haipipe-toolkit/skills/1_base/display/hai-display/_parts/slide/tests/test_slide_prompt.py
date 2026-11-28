"""slide_prompt.py: the styles, one prompt, and a deck's prompts."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import slide_prompt as sp  # noqa: E402


def test_every_style_has_a_look():
    looks = sp.styles()
    assert len(looks) == 19
    assert {"sketch-notes", "intuition-machine", "ian-handdrawn", "glossy-cartoon"} <= set(looks)
    assert all(looks.values())


def test_a_prompt_is_shell_then_style_then_content():
    text = sp.build("sketch-notes", 'Headline: "A Block is a promise?"')
    assert text.index("No slide numbers") < text.index("#FAF8F0") < text.index("A Block is a promise?")
    assert "source:" not in text                               # the credit line stays in the file


def test_unknown_style_and_empty_content_are_refused():
    with pytest.raises(SystemExit, match="pick one of"):
        sp.build("nope", "x")
    with pytest.raises(SystemExit, match="no content"):
        sp.build("sketch-notes", " ")


def test_a_deck_gives_each_slide_its_prompt(tmp_path):
    deck = tmp_path / "s09-x"
    deck.mkdir()
    (deck / "s09-x.slides.json").write_text(json.dumps({"style": "ian-handdrawn", "slides": [
        {"id": "01", "content": "Headline: one"}, {"id": "02", "content": "Headline: two"}]}))
    both = sp.deck_prompts(deck)
    assert list(both) == ["01", "02"] and "#FBFAF5" in both["02"]
    assert list(sp.deck_prompts(deck, "02")) == ["02"]
