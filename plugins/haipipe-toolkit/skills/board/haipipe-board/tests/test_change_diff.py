"""The `> ✎` diff has ONE computation, and this test is what keeps it one.

`live/write.py` and `haipipe-writing/cli/wdiff.py` both used to compute the
word-level change record with difflib. On 260802 they produced byte-identical
output on every case tried, which is agreement by luck: the next edit to either
one splits them silently, and the record is a durable review trail that a
reviewer reads months later.

The board now CALLS `wdiff` when it is installed and keeps a local fallback,
because every unit in this family has to stay deletable from every other. That
fallback is the thing that can drift, so it is compared here on every run.
"""
import importlib.util
import pathlib
import sys
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from live.write import WriteMixin                          # noqa: E402


def _writing_wdiff():
    for f in (HERE.parent.parent / "haipipe-writing" / "cli" / "wdiff.py",
              HERE.parent.parent.parent / "writing" / "haipipe-writing" / "cli" / "wdiff.py"):
        if f.exists():
            spec = importlib.util.spec_from_file_location("_hw", f)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            return m
    return None


CASES = [
    ("The coefficient is 0.41 in the pooled model.",
     "The coefficient is 0.42 in the clustered pooled model."),
    ("A short line.", "A much shorter line."),
    ("one two three", "one three"),
    ("one three", "one two three"),
    ("nothing changes here", "nothing changes here"),
    ("", "a line appeared"),
    ("a line vanished", ""),
    ("swap the first word", "change the first word"),
    ("trailing words go away entirely", "trailing words"),
    ("a b c d e f g", "a x c y e z g"),
]


class ChangeDiffTest(unittest.TestCase):
    def test_the_board_resolves_the_shared_differ(self):
        self.assertIsNotNone(
            WriteMixin._wdiff(),
            "the board could not find haipipe-writing/cli/wdiff.py; if that is "
            "deliberate the fallback still answers, but the two are then free "
            "to drift and this test is the only thing that would have said so")

    def test_the_fallback_agrees_with_haipipe_writing_word_for_word(self):
        hw = _writing_wdiff()
        if hw is None:
            self.skipTest("haipipe-writing is not installed beside this skill")
        for before, after in CASES:
            with self.subTest(before=before, after=after):
                # the local copy, reached by hiding the shared one
                real, WriteMixin._wdiff = WriteMixin._wdiff, staticmethod(lambda: None)
                try:
                    local = WriteMixin._change_diff(before, after)
                finally:
                    WriteMixin._wdiff = real
                self.assertEqual(local, hw.wdiff(before, after, host="board"),
                                 "the board's fallback and haipipe-writing have "
                                 "drifted apart on this pair")

    def test_the_board_host_marks_removals_and_insertions(self):
        out = WriteMixin._change_diff("the pooled model", "the clustered model")
        self.assertIn("~pooled~", out)
        self.assertIn("*clustered*", out)
        self.assertIn("the", out)

    def test_an_unchanged_sentence_produces_no_marks(self):
        out = WriteMixin._change_diff("nothing moved", "nothing moved")
        self.assertNotIn("~", out)
        self.assertNotIn("*", out)


if __name__ == "__main__":
    unittest.main()
