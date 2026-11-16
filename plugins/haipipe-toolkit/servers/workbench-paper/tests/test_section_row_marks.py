"""A version's Draft view row (paper_version.section_row): each step shows its mark (✅ done, 🙋 waits on you, ⬜ not
yet), never a state word (AGENTS.md § Page words); the word stays in the hover. A Section whose steps cannot be read
keeps its failure reason. Placeholders only, in a temp folder."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import paper_version as P  # noqa: E402

SECTION = ("# t01_intro · Introduction\ntask-type: draft\nreader-question: Why does it matter?\n\n## Content\n\n"
           "#### C1.P1 · Background · S1 to S2\nThe first sentence states the problem.\n")
STATE_WORDS = ("done", "next", "later", "sign", "asked", "send", "optional", "pass", "before the sign")


def chip_texts(row: str) -> list:
    """Each step chip's visible text, its hover dropped."""
    return [re.sub(r"<[^>]+>", "", c) for c in re.findall(r'<a class="fd-step[^"]*"[^>]*>(.*?)</a>', row)]


class SectionRowMarksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.task = self.root / "paper" / "Paper-X" / "j11_writing_v1130_venue" / "t01_intro"
        self.task.mkdir(parents=True)
        (self.task / "t01_intro.md").write_text(SECTION, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_step_shows_a_mark_not_a_state_word(self):
        row = P.section_row(self.task, self.root)
        chips = chip_texts(row)
        self.assertEqual(len(chips), len(P.WORK), row)
        for (key, step), text in zip(P.WORK, chips):
            name, mark = text.rsplit(" ", 1)
            self.assertEqual(name, step.split(" · ")[1])
            self.assertIn(mark, ("✅", "🙋", "⬜"), row)
            self.assertFalse(any(w in text.lower().split() for w in STATE_WORDS), text)
        self.assertRegex(row, r'title="[^"]+"')               # the state's word lives in the hover

    def test_marks_follow_the_step_class(self):
        self.assertEqual((P.step_mark("fd-ok"), P.step_mark("fd-you"), P.step_mark("")), ("✅", "🙋", "⬜"))

    def test_a_row_that_cannot_be_read_says_why(self):
        def broken(*_):
            raise ValueError("no face")
        real, P._facts = P._facts, broken
        try:
            row = P.section_row(self.task, self.root)
        finally:
            P._facts = real
        self.assertIn("❗ its steps could not be read", row)
        self.assertIn('title="no face"', row)


if __name__ == "__main__":
    unittest.main()
