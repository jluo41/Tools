"""Exercise existing scientific gates with an Idea Job and no Paper yet."""

from pathlib import Path
import shutil
import sys
import unittest

import yaml

import test_check_ideation as legacy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_ideation import GateCheck


class IdeaJobSelectionTest(unittest.TestCase):
    def setUp(self):
        self.fixture = legacy.IdeationGateTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        base = self.fixture.unit
        children = list(base.iterdir())
        block = base / "ideation/b01_direction"
        job = block / "j01_idea"
        job.mkdir(parents=True)
        for child in children:
            shutil.move(str(child), str(job / child.name))
        self.fixture.unit = job
        (block / "board.md").write_text("# Direction\n\nboard-kind: ideation-block\n")
        (block / "ideation.yaml").write_text(yaml.safe_dump({
            "version": 1, "kind": "ideation-block", "direction": "d", "question": "q?", "scope": "s",
            "ideas": [{"idea_id": "i01", "job": job.name}]}))
        (job / f"{job.name}.md").write_text("# Idea\n\ngoal: Test the claim\n")
        manifest = self.fixture.read("ideation.yaml")
        manifest.update(layout="idea-job", block="../ideation.yaml", idea_id="i01", address="b01.j01")
        self.fixture.write("ideation.yaml", manifest)
        self.fixture.make_test_ready()
        self.fixture.make_selection_v3()
        sync = self.fixture.read("projection/paper-ideation-sync.yaml")
        sync["source"]["ideation_job"] = "b01.j01"
        sync["paper_page"] = {"state": "missing", "path": None, **{
            surface: {"state": "not-requested", "revision": None, "receipt": None}
            for surface in ("working", "release", "delivery")}}
        sync["sync_status"] = "stale"
        self.fixture.write("projection/paper-ideation-sync.yaml", sync)
        selection = self.fixture.read("workflow/selection.yaml")
        selection["source"]["ideation_job"] = "b01.j01"
        route = {"paper_block": "../../../paper/Paper-Example",
                 "story_role": "Story-A",
                 "story_path": "../../../paper/Paper-Example/s02-story/s02-story.md"}
        selection["candidates"][0]["story_route"] = route
        selection["story_routes"][0].update(route)
        self.fixture.save_selection(selection)
        handoff = self.fixture.read("handoff/paper-ideation.yaml")
        handoff["source"]["ideation_job"] = "b01.j01"
        handoff["selected_ideas"][0].update(route)
        self.fixture.save_handoff(handoff)

    def findings(self, gate):
        checker = GateCheck(self.fixture.unit)
        getattr(checker, f"check_{gate}")()
        return checker.findings

    def codes(self, gate):
        return {f.code for f in self.findings(gate)}

    def test_selected_idea_can_handoff_before_paper_exists(self):
        self.assertEqual(self.findings("select"), [])
        self.assertEqual(self.findings("handoff"), [])
        self.assertFalse((self.fixture.unit / "../../../paper/Paper-Example").exists())

    def test_empty_opportunity_map_requires_explicit_gaps(self):
        sync = self.fixture.read("projection/paper-ideation-sync.yaml")
        sync["opportunity_map"] = []
        sync["open_gaps"] = ["No verified literature or pilot for this hypothesis yet"]
        self.fixture.write("projection/paper-ideation-sync.yaml", sync)
        self.assertEqual(self.findings("sync"), [])
        sync["open_gaps"] = []
        self.fixture.write("projection/paper-ideation-sync.yaml", sync)
        self.assertIn("evidence-gap-missing", self.codes("sync"))

    def test_newer_semantic_revision_still_requires_new_decision(self):
        sync = self.fixture.read("projection/paper-ideation-sync.yaml")
        sync["sync_revision"] += 1
        self.fixture.write("projection/paper-ideation-sync.yaml", sync)
        self.assertIn("sync-stale", self.codes("handoff"))

    def test_human_gate_remains_required(self):
        selection = self.fixture.read("workflow/selection.yaml")
        selection["by"] = ""
        self.fixture.save_selection(selection)
        self.assertTrue(self.findings("select"))

    def test_scientific_gate_remains_required(self):
        card = self.fixture.read("cards/i01_idea.yaml")
        card["core_claims"][0]["novelty_check"]["status"] = "unverified"
        self.fixture.write("cards/i01_idea.yaml", card)
        self.assertIn("novelty-ineligible", self.codes("handoff"))

    def test_layout_marker_cannot_bypass_legacy_gate(self):
        (self.fixture.unit.parent / "ideation.yaml").unlink()
        self.assertTrue({"idea-ownership", "sync-stale"}.issubset(self.codes("select")))

    def test_wrong_job_binding_is_rejected(self):
        selection = self.fixture.read("workflow/selection.yaml")
        selection["source"]["ideation_job"] = "b01.j02"
        self.fixture.save_selection(selection)
        self.assertIn("sync-binding", self.codes("select"))

    def test_handoff_must_keep_selected_paper_destination(self):
        handoff = self.fixture.read("handoff/paper-ideation.yaml")
        handoff["selected_ideas"][0]["paper_block"] = "../../../paper/Paper-Other"
        self.fixture.save_handoff(handoff)
        self.assertIn("paper-route", self.codes("handoff"))

    def test_story_cannot_land_outside_selected_paper(self):
        selection = self.fixture.read("workflow/selection.yaml")
        selection["candidates"][0]["story_route"]["paper_block"] = "../../../paper/Paper-Other"
        selection["story_routes"][0]["paper_block"] = "../../../paper/Paper-Other"
        self.fixture.save_selection(selection)
        self.assertIn("paper-route", self.codes("select"))
