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
        self.assertIn('<span class=st title="sentence review score">6/10</span>', html)
        self.assertIn('<span class="st st-ok" title="rewrite easier, same meaning (blind A/B, 261110)">📖 easier to read</span>', html)

    def test_each_other_verdict(self):
        for line, chip in (("original easier", "📖 original easier"), ("rewrite changes meaning", "📖 changes the meaning"),
                           ("no gain", "📖 no gain"), ("keep rewrite", "📖 easier to read")):
            self.assertIn(chip, card(f"Readable: {line}"), line)

    def test_a_card_without_a_review_is_unchanged(self):
        self.assertNotIn("📖", card())
        self.assertNotIn("/10", card())


if __name__ == "__main__":
    unittest.main()
