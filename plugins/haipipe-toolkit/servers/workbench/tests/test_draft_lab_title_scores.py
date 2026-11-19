"""Draft Lab: a part title and a paragraph title carry their own ★ from the report's Titles: block (CONSTITUTION A02)."""
from live.draft_step_titles import title_cards, title_lines

BODY = """### Revise review report
Reviewer: fresh
Titles:
- C4 · title 7/10 · register 8 · first-read 7 · names 7 · names the claim, not the measure · AI decided: kept, wording only · Fix: none
- C4.P8 · title 6/10 · register 6 · first-read 6 · names 7 · a metaphor · asked in Comment 3 · Fix: How error changes with scale
Sentences:
- C4.P8.s40 · logic 8/10 · read 8/10 · fine · Fix: none
"""


def test_titles_are_read_before_the_sentences():
    got = {x["t"]: x for x in title_lines(BODY)}
    assert set(got) == {"C4", "C4.P8"}
    assert got["C4"]["score"] == 7 and got["C4"]["decided"] == "kept, wording only" and got["C4"]["fix"] == ""
    assert got["C4.P8"]["decided"] == "asked in Comment 3" and got["C4.P8"]["fix"] == "How error changes with scale"
    assert got["C4"]["axes"] == ["register 8", "first-read 7", "names 7"]


def test_cards_carry_the_score_and_the_decision():
    html = title_cards(BODY)
    assert 'data-t="C4"' in html and 'data-low="7"' in html and "🤖 kept, wording only" in html
    assert 'data-t="C4.P8"' in html and "🙋 asked in Comment 3" in html and "Suggested:" in html


def test_no_titles_block_gives_nothing():
    assert title_cards("### Revise review report\nSentences:\n- s1 · logic 8/10 · read 8/10 · x · Fix: none\n") == ""


PARAS = """### Revise review report
Paragraphs:
- C2.P4 · 5/10 · question 7 · order 7 · inference 5 · scope 7 · complete 5 · shape 6 · fit 5 (r06) · asked in Comment 21 · Fix: none
Titles:
- C2.P4 · title 7/10 · register 8 · first-read 7 · names 7 · gain lacks its source · Fix: none
Sentences:
- C2.P4.s16 · logic 8/10 · read 8/10 · fine · Fix: none
"""


def test_paragraph_scores_are_their_own_cards():
    from live.draft_step_titles import score_lines
    p = score_lines(PARAS, "Paragraphs")[0]
    assert p["t"] == "C2.P4" and p["score"] == 5 and p["decided"] == "asked in Comment 21" and "fit 5 (r06)" in p["axes"]
    assert [x["t"] for x in title_lines(PARAS)] == ["C2.P4"]
    html = title_cards(PARAS)
    assert 'class=tt-pcard data-t="C2.P4" data-low="5"' in html and 'class=tt-card data-t="C2.P4" data-low="7"' in html
