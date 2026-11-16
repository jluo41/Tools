"""Accept on a card whose new words are two sentences writes two rows (JL 261115, M-D22)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()
from live import draft_step_revise_notes as N  # noqa: E402

DRAFT = "# Note · draft v1.0\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One and two.\n- B2 · s2 · Three.\n"


class SplitAcceptTest(unittest.TestCase):
    def test_a_split_writes_each_sentence_on_its_own_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp) / "t01-draft-v1.0.md"
            d.write_text(DRAFT, encoding="utf-8")
            (Path(tmp) / "t01-evidence-items.md").write_text("### E01-VALUE-x · x\n- **Target**: C1.P1.B2\n", encoding="utf-8")
            _, why, done = N._write_sentence_locked(d, "s1", "One and two.", "One \\citep{a}. Two follows.")
            text = d.read_text(encoding="utf-8")
            items_text = (Path(tmp) / "t01-evidence-items.md").read_text(encoding="utf-8")
        self.assertEqual(why, "")
        self.assertTrue(done)
        self.assertIn("- B1 · s1 · One \\citep{a}.\n- B2 · s1a · Two follows.\n- B3 · s2 · Three.", text)   # Bullets count on
        self.assertIn("C1.P1.B3", items_text)                         # the item on s2 moved with it

    def test_an_abbreviation_never_splits(self):
        self.assertEqual(N.split_sentences("Gu et al. 2026 found it, e.g. Fig. 2 shows it."),
                         ["Gu et al. 2026 found it, e.g. Fig. 2 shows it."])


if __name__ == "__main__":
    unittest.main()
