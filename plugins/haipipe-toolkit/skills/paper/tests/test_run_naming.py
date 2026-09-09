from __future__ import annotations

import re
import unittest
from pathlib import Path


REF = Path(__file__).parents[1] / "haipipe-paper" / "ref" / "run-naming.md"
TEXT = REF.read_text(encoding="utf-8")

PAPER_RUN = re.compile(
    r"^p(?P<lane>[mar])-[a-z0-9]+(?:-[a-z0-9]+)*-"
    r"(?P<target>[ef][0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*)-r[0-9]{2}$"
)
PAGE_RUN = re.compile(r"^r[0-9]{2}_[a-z0-9-]+_[a-z0-9-]+$")
PARAGRAPH_WRITING = re.compile(r"^r[0-9]{2}_page-writing_c[0-9]{2}-p[0-9]{2}$")
LEGACY_PJ = re.compile(r"^pj[0-9]{2}t[0-9]{2}r[0-9]{2}(?:_.+)?$")


class PaperRunNamingTest(unittest.TestCase):
    def test_semantic_paper_examples_are_lane_qualified(self) -> None:
        examples = [
            "pm-introduction-e01-cite-prescribing-variation-r01",
            "pm-results-e13-display-cohort-overview-r01",
            "pa-robustness-e01-value-sensitivity-r01",
            "pr-rd01-misq-feedback-20260825-e01-cite-response-r01",
        ]
        for run_id in examples:
            match = PAPER_RUN.fullmatch(run_id)
            self.assertIsNotNone(match, run_id)
            self.assertIn(match.group("lane"), {"m", "a", "r"})

    def test_page_and_paragraph_writing_names_remain_distinct(self) -> None:
        self.assertTrue(
            PARAGRAPH_WRITING.fullmatch("r01_page-writing_c01-p01")
        )
        self.assertTrue(
            PAGE_RUN.fullmatch("r05_page-evidence-item_e03-cite-prior-work")
        )
        self.assertNotEqual(
            "pm-introduction-e01-cite-prescribing-variation-r01",
            "r01_page-writing_c01-p01",
        )
        self.assertIsNone(PARAGRAPH_WRITING.fullmatch("r01_page-division-writing_c01"))
        self.assertIsNone(PARAGRAPH_WRITING.fullmatch("r01_page-writing_c01"))

    def test_old_pj_form_is_explicitly_read_only(self) -> None:
        self.assertTrue(LEGACY_PJ.fullmatch("pj02t01r01_rx_variation"))
        self.assertIsNone(PAPER_RUN.fullmatch("pj02t01r01_rx_variation"))
        self.assertIn("historical, read-only Runs", TEXT)
        self.assertIn("must not be guessed or reused", TEXT)

    def test_lane_map_and_round_token_are_documented(self) -> None:
        for phrase in (
            "`Ba-<desk>-Main/`",
            "`Bb-<desk>-Appendix/`",
            "`Bc-<desk>-Round/`",
            "`RD` remains the",
            "`m`",
            "`a`",
            "`r`",
        ):
            self.assertIn(phrase, TEXT)


if __name__ == "__main__":
    unittest.main()
