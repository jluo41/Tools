"""The Revise Run (rp-revise-NN_<target>) is a Page Writing card with a change ledger."""
import tempfile
import unittest
from pathlib import Path

from live.runs import (_audit_page_run_order, _page_run_label, _track_change_html,
                       local_runs, render)


class ReviseRunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page = Path(self.tmp.name) / "S-Test.md"
        self.page.write_text("# Test\n", encoding="utf-8")
        (self.page.parent / "outline").mkdir()
        (self.page.parent / "runs").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def run_folder(self, stem, target, status="waiting-for-feedback", closed=False, saved="Candidate.\n"):
        (self.page.parent / "runs" / f"{stem}.md").write_text(
            "---\nrun: " + stem + "\nfamily: page\noperation: interactive-writing\n"
            "interaction: human-feedback\ntarget: " + target + "\n---\n- Goal: Review " + target + ".\n",
            encoding="utf-8")
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "run: " + stem + "\nstatus: " + status + "\noperation: interactive-writing\nversion: v001\nstep: s001\n",
            encoding="utf-8")
        (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        closure = "\n## Version closure\n\n### Human close\nApproved.\n" if closed else ""
        (result / "v001.md").write_text(
            "## Step s001\n\n### Human feedback\nCompare v002 with v003 of rp-para-01_P03.\n\n"
            "### Saved result\n" + saved + closure, encoding="utf-8")
        return result

    LEDGER = (
        "#### Inputs\n- Before: results/rp-para-01_P03/v002.md · sha256 aaa\n"
        "- After: results/rp-para-01_P03/v003.md · sha256 bbb\n\n"
        "#### Track changes\n\n##### R01 · wording\n\n###### Before\n\n"
        "The effect was very large.\n\n###### After\n\nThe effect was large (95% CI 0.3 to 0.9).\n\n"
        "###### Why\n\nAnswers F02: hedge with the interval.\n\n###### Decision\n\naccept\n"
    )

    def test_identity_label_and_group(self):
        self.assertEqual(_page_run_label("rp-revise-01_C1.P3"), "rp-revise-01_c1.p3 · Revise · C1.P3")
        rows = [{"lane": "page", "run_id": "rp-struct-01", "status": "Done"},
                {"lane": "page", "run_id": "rp-revise-01_C1.P3", "status": "Waiting"}]
        _audit_page_run_order(rows)
        self.assertEqual(rows[1]["status"], "Waiting")
        self.assertNotIn("audit", rows[1])

    def test_card_renders_under_revise_with_a_decision(self):
        self.run_folder("rp-struct-01", "Structure + P01..PN", status="complete", closed=True)
        self.run_folder("rp-revise-01_C1.P3", "C1.P3", saved=self.LEDGER)
        by_id = {row["run_id"]: row for row in local_runs(self.page)}
        self.assertEqual(by_id["rp-revise-01_C1.P3"]["status"], "Waiting")
        body = render(self.page, "", "")
        self.assertIn("<h3>Revise</h3>", body)
        self.assertIn("Revise · C1.P3", body)
        self.assertIn("Compare before and after for C1.P3", body)
        section = "## Step s001\n\n### Human feedback\nx\n\n### Saved result\n" + self.LEDGER
        cards = _track_change_html(section)
        self.assertIn("track-decision", cards)
        self.assertIn("accept", cards)
        self.assertIn("<del>", cards)
        self.assertIn("<ins>", cards)


if __name__ == "__main__":
    unittest.main()
