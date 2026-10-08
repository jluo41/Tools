from __future__ import annotations

import re
import unittest
from pathlib import Path


REF = Path(__file__).parents[1] / "haipipe-paper" / "ref" / "run-naming.md"
CARDS = Path(__file__).parents[1] / "haipipe-paper-workflow" / "ref" / "run-cards.md"
TEXT = REF.read_text(encoding="utf-8")

# Every Run name is the full form (JL 261001): Paper judgment Runs and Page Runs.
JUDGE_RUN = re.compile(r"^run-paper-(?P<judgment>idea|claim|task|narrative)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")
PAGE_RUN = re.compile(r"^run-(structure|scratch|section|paragraph|revise|auto-write|evidence-embed|context|check|"
                      r"value|citation|display)-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*$")
SHORT = re.compile(r"^(rp-|re-|rd[0-9]+_|pm-|pa-|pr-|pj[0-9]|ridea-|rclaim-|rtask-|rnarra-)")


class PaperRunNamingTest(unittest.TestCase):
    def test_judgment_runs_use_the_full_paper_form(self) -> None:
        for run_id in ("run-paper-idea-0901-agentic-learning", "run-paper-claim-0901-beyond-rating",
                       "run-paper-task-0902-funnel-rates", "run-paper-narrative-0903-introduction"):
            self.assertIsNotNone(JUDGE_RUN.fullmatch(run_id), run_id)
        for judgment in ("idea", "claim", "task", "narrative"):
            self.assertIn(f"run-paper-{judgment}-<slug>", TEXT)

    def test_page_runs_use_the_full_page_form(self) -> None:
        self.assertTrue(PAGE_RUN.fullmatch("run-paragraph-0901-c1-p2"))
        self.assertTrue(PAGE_RUN.fullmatch("run-citation-0901-prior-work"))
        self.assertIsNone(JUDGE_RUN.fullmatch("run-paragraph-0901-c1-p2"))

    def test_short_names_are_retired_everywhere(self) -> None:
        self.assertIn("are retired (JL 261001)", TEXT)
        for line in CARDS.read_text(encoding="utf-8").splitlines():
            if line.startswith("🔘 BUTTON"):
                pattern = line.split("·")[2].strip()
                self.assertNotRegex(pattern, r"\^(rp-|re-|rd\\d|ridea|rclaim|rtask|rnarra|pj|pm-|pa-|pr-)", line)
        for example in ("rp-sec-07", "ridea-01_x", "pm-intro-e01-cite-x-r01"):
            self.assertTrue(SHORT.match(example))
            self.assertIsNone(JUDGE_RUN.fullmatch(example))

    def test_lanes_and_levels_are_documented(self) -> None:
        # b16 Q05: a Run lives with its level; lanes come from the Task's number band; comments are a report
        for phrase in ("`paper_lane: main | appendix |\nletters`", "`runs/run-<type>-<target>/`",
                       "`reports/qNN_<kind>-<MMDD>/`", "`page.py run-names`"):
            self.assertIn(phrase, TEXT)


if __name__ == "__main__":
    unittest.main()
