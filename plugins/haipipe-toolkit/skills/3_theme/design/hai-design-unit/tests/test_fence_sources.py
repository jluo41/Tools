"""check_unit.in_fence: a reasoning step's or an element's `from` names a fence file, or is `own knowledge`;
free prose that only mentions a file is not a source (the cold review's counterexamples, 261007). cites_answers: a
`query q<NN>` names an answer the method's own tool gave in t00 (M05 m3, 261022)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from check_unit import cites_answers, in_fence  # noqa: E402

FENCE = ["goal.md", "method.md", "rules.md", "handoff-W-03.md", "theory/papers.md"]


class FenceSourcesTest(unittest.TestCase):
    def test_sources_that_name_a_fence_file(self):
        for src in ("own knowledge", "goal.md", "goal", "rules.md r2.1", "rule r2.1", "rules", "W-03 row 2",
                    "handoff-W-03.md", "theory/papers.md", "papers"):
            self.assertTrue(in_fence(src, FENCE), src)

    def test_prose_is_not_a_source(self):
        for src in ("", "my hunch about the goal", "the method I like", "common sense, no rules apply", "i1 rules",
                    "own knowledge and more", "W-09 row 1", "intuition"):
            self.assertFalse(in_fence(src, FENCE), src)

    def test_query_answers(self):
        answers = {"q01", "q02", "q05"}
        for src in ("query q01", "query q02 · q05", "Query q05"):
            self.assertTrue(cites_answers(src, answers), src)
        for src in ("query q09", "query q01 · q09", "query", "q01", "my query q01", "own knowledge"):
            self.assertFalse(cites_answers(src, answers), src)


if __name__ == "__main__":
    unittest.main()
