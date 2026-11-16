"""A review line's Fix is offered as a new sentence only when it is one (JL 261115: "the editing card is very bad,
report to Workbench to avoid it again": "Fix: see the card" was offered with ✓ Use this)."""
import unittest

from host_paths import bootstrap

bootstrap()
from live.draft_step_revise_blind import not_a_sentence  # noqa: E402

OLD = "Scaling laws tell a builder how much error falls when the data grows tenfold."


class FixSentenceTest(unittest.TestCase):
    def test_pointers_and_fragments_are_notes(self):
        for fix in ("see the card", "See card.", "split", "Keep.", "as above", "none", "<a fragment without an end"):
            self.assertTrue(not_a_sentence(fix, OLD), fix)

    def test_a_short_or_unrelated_sentence_is_refused(self):
        self.assertTrue(not_a_sentence("Data helps.", OLD))
        self.assertTrue(not_a_sentence("Patients prefer morning visits over evening clinic hours today.", OLD))

    def test_a_real_rewrite_passes(self):
        self.assertEqual(not_a_sentence("A scaling law tells a builder how much the error falls with tenfold data.", OLD), "")
        self.assertEqual(not_a_sentence("Error falls as data grows tenfold \\citep{kaplan2020}.", OLD), "")


if __name__ == "__main__":
    unittest.main()
