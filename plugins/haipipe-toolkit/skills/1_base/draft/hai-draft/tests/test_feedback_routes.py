"""`Routed:` is one grammar for the Page's Feedback column and check.py's tooth."""
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src.feedback import routed_pairs, routed_rows  # noqa: E402


class RoutedGrammarTest(unittest.TestCase):
    def test_one_row_keeps_its_round(self):
        self.assertEqual(routed_pairs("RD01 S1-PP1"), [("RD01", "S1-PP1")])

    def test_semicolons_separate_rows_that_each_name_their_round(self):
        self.assertEqual(routed_pairs("RD01 S1-PP5; RD01 S1-PP7"),
                         [("RD01", "S1-PP5"), ("RD01", "S1-PP7")])

    def test_commas_separate_rows_that_inherit_the_round(self):
        self.assertEqual(routed_pairs("RD01 S3-PP2, S3-PP3"),
                         [("RD01", "S3-PP2"), ("RD01", "S3-PP3")])

    def test_a_round_id_is_never_a_row(self):
        for text in ("RD01 S1-PP5; RD01 S1-PP7", "RD01 RD02 S2-PP1", "RD01"):
            self.assertNotIn("RD01", [rid for _rd, rid in routed_pairs(text)], text)
        self.assertEqual(routed_pairs("RD01"), [])

    def test_a_later_round_id_owns_the_rows_after_it(self):
        self.assertEqual(routed_pairs("RD01 S1-PP1, RD02 S1-PP2 S1-PP3"),
                         [("RD01", "S1-PP1"), ("RD02", "S1-PP2"), ("RD02", "S1-PP3")])

    def test_a_bare_row_has_no_round(self):
        self.assertEqual(routed_pairs("S1-PP1"), [("", "S1-PP1")])
        self.assertEqual(routed_pairs("   "), [])

    def test_trailing_punctuation_never_reaches_the_row_id(self):
        self.assertEqual(routed_pairs("RD01 S1-PP1."), [("RD01", "S1-PP1")])

    def test_routed_rows_reads_a_plan_and_filters_by_round(self):
        plan = ("# QA1 · outline v1\n\n## C1 · One\n### C1.P1 · Two\n"
                "- B1 · first move\n  Note: n\n  Routed: RD01 S1-PP1, S1-PP2\n"
                "- B2 · second move\n  Routed: RD02 S1-PP3; RD01 S1-PP4\n"
                "Routed: not-indented-so-not-a-row\n")
        self.assertEqual(routed_rows(plan), [
            ("RD01", "S1-PP1"), ("RD01", "S1-PP2"), ("RD02", "S1-PP3"), ("RD01", "S1-PP4")])
        self.assertEqual([rid for _rd, rid in routed_rows(plan, "RD01")],
                         ["S1-PP1", "S1-PP2", "S1-PP4"])
        self.assertEqual(routed_rows(plan, "RD09"), [])


if __name__ == "__main__":
    unittest.main()
