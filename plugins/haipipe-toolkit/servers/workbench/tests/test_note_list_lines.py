"""An AI comment's indented lines stay with it and show as a list; its answering card is a link (A03, 261118)."""
from live.draft_step_revise_notes import _note_card
from live.item_cards import parse_comments

TEXT = """### Comment 4 · s48
Quote: two matches
State: open
- Note · 2026-11-18 19:30 · AI: s48 is hard to read.
  1. Problem: two matches and two sets of brackets in one sentence.
  2. Proposed: split it in two.
  3. Your call: split, or keep it as one?
- Reply · 2026-11-18 19:40: Split it.
"""


def test_indented_lines_stay_with_their_message(tmp_path):
    f = tmp_path / "x-comments.md"
    f.write_text(TEXT)
    c = parse_comments(f)[0]
    assert len(c["thread"]) == 2
    assert c["thread"][0][2].split("\n") == ["s48 is hard to read.", "1. Problem: two matches and two sets of brackets "
                                             "in one sentence.", "2. Proposed: split it in two.",
                                             "3. Your call: split, or keep it as one?"]
    assert c["thread"][1][2] == "Split it."


def test_the_card_shows_a_numbered_list_and_a_card_link(tmp_path):
    f = tmp_path / "x-comments.md"
    f.write_text(TEXT)
    c = {**parse_comments(f)[0], "target": "s48"}
    html = _note_card(c, ["Edit · s48 · split in two"])
    assert "<ol class=nt-list><li>Problem:" in html and "Your call: split" in html
    assert 'class=nt-go' in html and 'data-card="Edit · s48 · split in two"' in html
