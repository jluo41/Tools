import unittest
import sys
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from live.outline import _bundle_state
from live.pagex import _pagex_match_score


class PagexMatchScoreTest(unittest.TestCase):
    def test_candidate_score_is_transparent_but_not_a_reuse_decision(self):
        score = _pagex_match_score(
            "scan WellDoc tables for a cycle indicator",
            "scan WellDoc tables for a cycle indicator; a result was found.",
        )
        self.assertEqual(score["overlap"], score["total"])
        self.assertTrue(score["all_terms"])
        self.assertEqual(score["score"], 1.0)

    def test_topic_overlap_is_only_a_shortlist(self):
        score = _pagex_match_score(
            "scan WellDoc tables for a cycle indicator",
            "This page discusses a cycle topic but contains no table scan.",
        )
        self.assertLess(score["score"], 1.0)
        self.assertFalse(score["all_terms"])

    def test_empty_question_has_no_candidates(self):
        self.assertEqual(
            _pagex_match_score("", "anything"),
            {"overlap": 0, "total": 0, "score": 0.0, "all_terms": False},
        )

    def test_explicit_why_empty_can_land_a_value_without_a_file(self):
        bundle = _bundle_state(
            "value", [], "C1.P1.B1", {"C1.P1.B1": ["PP01"]}, {},
            {"PP01": ("answered", 0, "definition", True)}, {}, {},
        )
        self.assertEqual(bundle["summary"], "complete")
        self.assertNotIn("status", bundle)

    def test_bundle_rollup_has_no_legacy_status_vocabulary(self):
        bundle = _bundle_state(
            "value", [], "C1.P1.B1", {}, {}, {}, {}, {},
        )
        self.assertEqual(bundle["summary"], "incomplete")
        self.assertNotIn("status", bundle)
        rendered = repr(bundle)
        for retired in (
            "evidence-ready", "needs-probe", "needs-intake", "needs-citation",
        ):
            self.assertNotIn(retired, rendered)

    def test_citation_feedback_exposes_the_human_verification_state(self):
        bundle = _bundle_state(
            "cite", ["Deyo2015"], "C1.P1.B1", {}, {}, {}, {},
            {"Deyo2015": {"verified": False}},
        )
        self.assertEqual(bundle["feedback"], ["Deyo2015: unverified"])


if __name__ == "__main__":
    unittest.main()
