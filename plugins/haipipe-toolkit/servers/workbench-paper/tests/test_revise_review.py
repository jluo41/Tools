"""A Revise card shows its sentence review beside its state (JL 261110): the score and the blind readers' easier-to-read
verdict from its `Score:` and `Readable:` lines. Placeholders only."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import draft_steps  # noqa: E402


def card(*lines: str) -> str:
    body = "\n".join(("Why: pattern 3, a room metaphor.", "Original: <old>.", "Expected: <new>.", "State: proposed") + lines)
    c = {"why": "pattern 3, a room metaphor.", "original": "<old>.", "expected": "<new>.", "state": "proposed", "body": body}
    return draft_steps._revise_card("Edit · S2 · <title>", c, "t01_x", "Pass 1", "C1.P1")


class ReviseReviewTest(unittest.TestCase):
    def test_easier_and_same_meaning_is_green(self):
        html = card("Score: 6/10", "Readable: rewrite easier, same meaning (blind A/B, 261110)")
        self.assertIn('<span class=st title="sentence review score">★6/10</span>', html)
        self.assertIn('<span class="st st-ok" title="rewrite easier, same meaning (blind A/B, 261110)">📖 easier to read</span>', html)

    def test_each_other_verdict(self):
        for line, chip in (("original easier", "📖 original easier"), ("rewrite changes meaning", "📖 changes the meaning"),
                           ("no gain", "📖 no gain"), ("keep rewrite", "📖 easier to read")):
            self.assertIn(chip, card(f"Readable: {line}"), line)

    def test_a_card_without_a_review_is_unchanged(self):
        self.assertNotIn("📖", card())
        self.assertNotIn("/10", card())

    def test_the_change_comes_first_and_a_long_reason_folds(self):
        # JL 261115: "this is not readable": the change first, the Why clamped, quotes and papers in a closed Detail
        c = {"why": "pattern 3, a room metaphor.", "original": "<old>.", "expected": "<new>.", "state": "proposed",
             "detail": "the source says <a quote>", "body": ""}
        html = draft_steps._revise_card("Edit · S2 · <title>", c, "t01_x", "Pass 1", "C1.P1")
        self.assertLess(html.index("rv-choices"), html.index("rv-why"))      # the change (its choices) first
        self.assertIn("<details class=rv-detail><summary>Detail</summary>", html)
        c["why"] = "the citation sits far from its claim. (1) s2 cites three papers (2) each backs one clause (3) move each"
        html = draft_steps._revise_card("Edit · S2 · <title>", c, "t01_x", "Pass 1", "C1.P1")
        self.assertEqual(html.count("class=rv-pt>"), 3)                  # one row per point, the reason kept whole
        self.assertIn("each backs one clause", html)

    def test_every_option_shows_its_change_and_an_unchanged_one_says_so(self):
        # JL 261115: "I didn't find what does the B mean here? ... if B is unchanged, you say unchanged"
        from live.draft_step_revise_cards import _opt_diff
        self.assertIn("<del", _opt_diff("9 models, and more tokens.", "9 models. More tokens."))
        self.assertEqual(_opt_diff("a  b.", "a b."), '<span class="mut rv-same">unchanged</span>')
    def test_a_keep_option_is_the_original_and_chosen_option_b_is_read(self):
        # JL 261115: "this is very confusing" (t02 s40: A "Keep." drawn as a rewrite; "Chosen: Option B" showed A)
        from live.draft_step_revise_cards import _chosen, _options
        c = {"original": "<old>.", "expected": "", "body": "Option A: Keep.\nOption B (cut): <new>.\nChosen: Option B\n"}
        opts = _options(c)
        self.assertEqual(opts[0][2], "<old>.")
        self.assertEqual(_chosen(c, opts), "B")
        for line in ("Chosen: B", "Chosen: B.", "Chosen: Option B (cut)"):
            self.assertEqual(_chosen({"body": line}, opts), "B", line)
        self.assertIn("unchanged", draft_steps._revise_card("Edit · S2 · <title>", dict(c, state="proposed"), "t", "P", "C1.P1"))


if __name__ == "__main__":
    unittest.main()
