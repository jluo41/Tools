#!/usr/bin/env python3
"""Regression tests for sentence-local comments and tracked edits."""

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))

sys.path.insert(0, str(HERE / "cli"))          # the CLI moved into cli/ (260801)

import serve as board_serve  # noqa: E402
from src.body import body  # noqa: E402


class SentenceEditingTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.page = Path(self.temp.name) / "QA1-test.md"
        self.handler = object.__new__(board_serve.Handler)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, text):
        self.page.write_text(text, encoding="utf-8")

    def read(self):
        return self.page.read_text(encoding="utf-8")

    def test_new_comment_is_directly_under_its_sentence(self):
        self.write("First sentence.\nSecond sentence.\n")
        result, error = self.handler.add_comment(self.page, {
            "sentence": "First sentence.", "who": "JL", "text": "Please clarify.",
            "when": "260729 1502",
        })
        self.assertIsNone(error)
        self.assertEqual(result["sentence"], "First sentence.")
        self.assertEqual(
            self.read(),
            # `> Comment WHO …` since 260802: the engine must not write what
            # check.py flags. `## Discussion` keeps its own `> JL:` grammar.
            "First sentence.\n> Comment JL Please clarify. · 260729 1502\nSecond sentence.\n",
        )
        self.assertNotIn("## Comments", self.read())

    def test_edit_replaces_sentence_and_adds_one_whole_sentence_diff(self):
        self.write("The coefficient is 0.42 in the pooled model.\n")
        result, error = self.handler.edit_sentence(self.page, {
            "sentence": "The coefficient is 0.42 in the pooled model.",
            "replacement": "The coefficient is 0.42 in the clustered pooled model.",
            "who": "JL", "when": "260729 1502",
        })
        self.assertIsNone(error)
        self.assertEqual(
            result["diff"],
            "The coefficient is 0.42 in the *clustered* pooled model.",
        )
        self.assertEqual(
            self.read(),
            "The coefficient is 0.42 in the clustered pooled model.\n"
            "> ✎ The coefficient is 0.42 in the *clustered* pooled model. · JL · 260729 1502\n",
        )

    def test_edit_refuses_an_ambiguous_sentence(self):
        original = "Repeated sentence.\nRepeated sentence.\n"
        self.write(original)
        _result, error = self.handler.edit_sentence(self.page, {
            "sentence": "Repeated sentence.", "replacement": "Changed sentence.",
        })
        self.assertIn("不止一次", error)
        self.assertEqual(self.read(), original)

    def test_inline_comment_and_change_are_visible_below_the_sentence(self):
        html = body(
            "New sentence.\n"
            "> Comment JL Please clarify. · 260729 1502\n"
            "> ✎ ~Old~ *New* sentence. · JL · 260729 1503\n"
        )
        # SHUT since 260801: nothing on a page opens itself, and the badge
        # is what keeps the 260724 rule that an invisible fold is broken.
        # `💬` says a person is waiting, which is the half that was missing
        # when this could only say that SOMETHING was attached.
        self.assertIn('<details class="sent">', html)
        self.assertIn('<span class="sbadge">💬 2</span>', html)
        self.assertIn("Please clarify.", html)
        self.assertIn('<del class="chg-old">Old</del>', html)
        self.assertIn('<ins class="chg-new">New</ins>', html)


if __name__ == "__main__":
    unittest.main()
