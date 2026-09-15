"""Scratch Mode contract: inline targets and an AI-assisted close gate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

PAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAGE_ROOT))

from live.outline import _PAGE, plan_card  # noqa: E402
from live.outline_scratch import (ai_summarize_scratch, read_scratch,  # noqa: E402
                                  save_scratch)
from live.runs import run_inventory  # noqa: E402


PLAN = """# S-scratch · outline v1.1
outline-version: v1.1
approved: ✅

## C1 · The argument
### C1.P1 · The opening move · S1 to S2
- B1 · [Phenomenon] Physicians differ in prescribing
  Draft: Physicians differ in how they prescribe.
- B2 · [Bridge] The difference reaches patients
  Draft: That difference reaches patients.
### C1.P2 · The mechanism · S3 to S4
- B1 · [Mechanism] Pressure shapes accommodation
  Draft: Pressure can shape accommodation.

## Aims
- ⬜ A1.1 · Settle the design.
"""


class ScratchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="outline-scratch-")
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / "S-scratch"
        (self.folder / "outline").mkdir(parents=True)
        self.page = self.folder / "S-scratch.md"
        self.page.write_text("# S-scratch\n\n## Content\n", encoding="utf-8")
        self.plan = self.folder / "outline" / "S-scratch-outline-v1.1.md"
        self.plan.write_text(PLAN, encoding="utf-8")

    def ai_summary(self, *_args):
        return "AI summary of the rough plan."

    def failing_summary(self, *_args):
        raise ValueError("AI summary unavailable")

    def save(self, scope, target, phase="save", run_id="", summary=""):
        return save_scratch(self.page, {
            "scope": scope, "target": target, "phase": phase,
            "run_id": run_id, "notes": "First thought\nSecond thought",
            "summary": summary,
        }, summarizer=self.ai_summary)

    def test_each_scope_accepts_its_canonical_target(self):
        for scope, target in (("section", "C1"), ("subsection", "C1.P1"),
                              ("paragraph", "C1.P1")):
            result, err = self.save(scope, target)
            self.assertIsNone(err, err)
            self.assertEqual(result["status"], "open")
        inventory = read_scratch(self.page)
        self.assertEqual(len(inventory["latest"]), 3)
        self.assertEqual(self.plan.read_text(encoding="utf-8").count("## Scratch"), 1)

    def test_bullet_target_is_rejected(self):
        result, err = self.save("paragraph", "C1.P1.B1")
        self.assertIsNone(result)
        self.assertIn("target does not exist", err)

    def test_ai_summary_closes_and_closed_run_is_immutable(self):
        result, err = self.save("paragraph", "C1.P1")
        self.assertIsNone(err, err)
        run_id = result["run"]
        result, err = self.save("paragraph", "C1.P1", "finish", run_id,
                                "Manual text is ignored; Finish asks the AI.")
        self.assertIsNone(err, err)
        self.assertEqual(result["status"], "closed")
        self.assertEqual(result["summary"], "AI summary of the rough plan.")
        runtime = self.folder / "results" / run_id / "runtime.yaml"
        self.assertIn("status: complete", runtime.read_text(encoding="utf-8"))
        _, err = self.save("paragraph", "C1.P1", "finish", run_id, "A new summary")
        self.assertIn("immutable", err)

    def test_ai_summary_failure_keeps_finish_open(self):
        result, err = save_scratch(self.page, {
            "scope": "section", "target": "C1", "phase": "finish",
            "notes": "Keep the section focused.",
        }, summarizer=self.failing_summary)
        self.assertIsNone(result)
        self.assertIn("AI summary unavailable", err)

    def test_save_updates_one_open_run_and_later_restarts_after_close(self):
        result, err = self.save("paragraph", "C1.P1")
        self.assertIsNone(err, err)
        first = result["run"]
        result, err = save_scratch(self.page, {
            "scope": "paragraph", "target": "C1.P1", "phase": "save",
            "run_id": first, "notes": "Refine the causal hinge.", "summary": "",
        }, summarizer=self.ai_summary)
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], first)
        self.assertIn("Refine the causal hinge.", self.plan.read_text(encoding="utf-8"))
        result, err = self.save("paragraph", "C1.P1", "finish", first,
                                "The paragraph should make the causal hinge explicit.")
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], first)
        result, err = self.save("paragraph", "C1.P1")
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], "rp-scratch-02_C1.P1")

    def test_draft_renders_one_control_per_current_target_but_read_only_has_none(self):
        card = plan_card(self.page)
        self.assertIn('data-scratch-scope="section"', card)
        self.assertIn('data-scratch-scope="paragraph"', card)
        self.assertNotIn('data-scratch-scope="subsection"', card)
        self.assertNotRegex(card, r'data-scratch-target="[^"]+\.B\d+"')
        self.assertIn("if(mode==='scratch')", _PAGE)
        self.assertIn("x.open=false", _PAGE)
        self.assertIn('position:static', card)
        self.assertIn('box-shadow:none', card)
        self.assertIn("Finish Scratch", card)
        self.assertIn('rows="12"', card)
        self.assertIn('textarea[name="notes"]{min-height:clamp(240px,32vh,420px)}', card)
        self.assertNotIn('name="summary"', card)
        self.assertNotIn("Summarize when you are done", card)
        self.assertIn("setTimeout(function(){location.reload();},180)", card)
        readonly = plan_card(self.page, read_only=True)
        self.assertNotIn("data-scratch-form", readonly)
        self.assertNotIn("Finish Scratch", readonly)

    def test_saved_scratch_is_visible_by_default_in_scratch_mode(self):
        result, err = self.save("paragraph", "C1.P1")
        self.assertIsNone(err, err)
        card = plan_card(self.page)
        self.assertIn('class="scratch-saved has-saved"', card)
        self.assertIn("First thought", card)
        self.assertIn("Second thought", card)
        self.assertNotIn("scratch-saved-summary", card)

    def test_closed_scratch_appears_in_run_inventory_as_done(self):
        result, err = self.save("paragraph", "C1.P1", "finish",
                               summary="Set the opening move before the mechanism.")
        self.assertIsNone(err, err)
        rows = run_inventory(self.page)
        row = next(item for item in rows if item["run_id"] == result["run"])
        self.assertEqual(row["status"], "Done")
        self.assertEqual(row["mode"], "scratch")
        self.assertEqual(row["target_scope"], "paragraph")
        card = plan_card(self.page)
        self.assertIn("First thought", card)
        self.assertIn("AI summary of the rough plan.", card)

    def test_ai_summary_uses_the_local_cli_without_tools(self):
        completed = SimpleNamespace(
            returncode=0,
            stdout="One concise summary.",
            stderr="",
        )
        with patch("live.outline_scratch.subprocess.run", return_value=completed) as run:
            summary = ai_summarize_scratch(
                self.page, "paragraph", "C1.P1", "Keep the causal hinge visible."
            )
        self.assertEqual(summary, "One concise summary.")
        argv = run.call_args.args[0]
        self.assertIn("--no-session-persistence", argv)
        self.assertIn("--tools", argv)


if __name__ == "__main__":
    unittest.main()
