from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


SKILL = Path(__file__).resolve().parents[1]
CHECKER = SKILL / "scripts" / "check_ideation.py"


class IdeationGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.unit = Path(self.temp.name)
        for relative in (
            "bundle",
            "cards/venue-fit",
            "projection",
            "workflow/generate",
            "workflow/novelty",
            "workflow/pressure",
            "handoff",
        ):
            (self.unit / relative).mkdir(parents=True, exist_ok=True)
        self.write(
            "ideation.yaml",
            {
                "version": 1,
                "kind": "ideation-unit",
                "address": "b01.j01.t01",
                "direction": "d",
                "question": "q",
                "scope": "bounded fixture",
                "decision_rule": "select only after Test resolves",
                "stage": "generate",
                "state": "open",
                "bundle": "bundle/evidence-bundle.yaml",
                "direction_card": "cards/direction.yaml",
                "test_matrix": "cards/test-matrix.yaml",
                "paper_sync": "projection/paper-ideation-sync.yaml",
                "selection_receipt": "workflow/selection.yaml",
                "paper_handoff": "handoff/paper-ideation.yaml",
                "created_at": "2026-09-08T11:00:00-04:00",
                "updated_at": "2026-09-08T11:00:00-04:00",
            },
        )
        self.write(
            "bundle/evidence-bundle.yaml",
            {
                "kind": "ideation-evidence-bundle",
                "direction": {"question": "q"},
                "sources": {"internal": [], "external": [], "venues": []},
                "policy": {"no_copy": True},
            },
        )
        self.write(
            "workflow/generate/g01_fixture.yaml",
            {
                "version": 1,
                "kind": "ideation-generate",
                "id": "g01",
                "direction": "cards/direction.yaml",
                "bundle": "bundle/evidence-bundle.yaml",
                "bundle_updated_at": "2026-09-08T11:00:00-04:00",
                "lenses_attempted": ["contradiction", "mechanism"],
                "provisional_candidates": [
                    {
                        "provisional_id": "p01",
                        "disposition": "admitted",
                        "canonical_card": "cards/i01_idea.yaml",
                        "reason": "distinct claim-method tuple",
                    }
                ],
                "created_at": "2026-09-08T11:05:00-04:00",
            },
        )
        self.write(
            "cards/direction.yaml",
            {
                "kind": "direction-card",
                "id": "direction",
                "title": "D",
                "question": "q",
                "scope": "s",
                "bundle": "bundle/evidence-bundle.yaml",
            },
        )
        self.card = {
            "kind": "idea-card",
            "id": "i01",
            "canonical_id": "i01",
            "title": "Idea",
            "claim": "falsifiable claim",
            "method": "steps",
            "hypothesis": "h",
            "minimum_experiment": "experiment",
            "expected_outcome": "signal",
            "failure_interpretation": "null means revise",
            "novelty_delta": "delta",
            "core_claims": [
                {
                    "id": "c01",
                    "claim": "claim",
                    "contribution_role": "central",
                    "novelty_check": {"status": "unverified"},
                }
            ],
            "identification": {"credibility": "unknown", "fatal_assumptions": [], "repair_path": ""},
            "feasibility": {"pilot": "pending", "receipt": "", "pressure_receipt": "", "waiver": ""},
            "venue_fit": {
                "card": "venue-fit/i01_venue-fit.yaml",
                "broad_screen": "pending",
                "deep_fit": "pending",
                "overall": "unknown",
                "recommended_target": "unresolved",
                "nature_review": None,
                "human_target": "open",
            },
            "risk": "risk",
            "reviewer_objection": "objection",
            "recommendation": "unresolved",
            "state": "open",
            "evidence_bundle": "../bundle/evidence-bundle.yaml",
        }
        self.write("cards/i01_idea.yaml", self.card)

    def write_sync(self, stage: str = "I1") -> None:
        self.write(
            "projection/paper-ideation-sync.yaml",
            {
                "version": 1,
                "kind": "paper-ideation-sync",
                "source": {
                    "ideation_task": "b01.j01.t01",
                    "ideation_manifest": "ideation.yaml",
                    "evidence_bundle": "bundle/evidence-bundle.yaml",
                    "direction_card": "cards/direction.yaml",
                    "test_matrix": "cards/test-matrix.yaml" if stage == "I2" else None,
                },
                "stage": stage,
                "sync_revision": 1,
                "paper_page": {
                    "state": "missing",
                    "path": None,
                    "last_projected_revision": None,
                },
                "discovery_landscape": {
                    "accepted_syntheses": [],
                    "direct_result_ids": [],
                    "convergent_signals": [],
                    "contradictions": [],
                    "unresolved_territory": ["closest-work search remains open"],
                },
                "opportunity_map": [
                    {
                        "id": "o01",
                        "opportunity": "bounded opening",
                        "evidence": ["context01"],
                        "interpretation": "hypothesis, not claim support",
                        "idea_ids": ["i01"],
                        "status": "open",
                    }
                ],
                "ideas": [
                    {
                        "card": "cards/i01_idea.yaml",
                        "state": "open",
                        "comparison_order": 1,
                        "novelty": "unverified" if stage == "I1" else "hold",
                        "identification": "unknown",
                        "feasibility": "pending",
                        "journal_fit": "pending" if stage == "I1" else "unknown",
                        "next_route": "novelty",
                    }
                ],
                "portfolio_recommendation": {
                    "status": "not-reviewed",
                    "summary": "machine comparison only; not a decision",
                    "ideas": [
                        {
                            "idea_id": "i01",
                            "recommendation": "unresolved",
                            "reason": "Test remains open",
                        }
                    ],
                },
                "selection_authority": {
                    "owner": "haipipe-ideation-select",
                    "status": "none",
                    "receipt": None,
                },
                "sync_status": "current",
                "open_gaps": ["novelty"],
                "updated_at": "2026-09-08T11:10:00-04:00",
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, value: object) -> None:
        path = self.unit / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")

    def run_gate(self, gate: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), str(self.unit), "--gate", gate],
            text=True,
            capture_output=True,
            check=False,
        )

    def make_test_ready(self) -> None:
        self.write(
            "workflow/novelty/i01_receipt.yaml",
            {
                "version": 1,
                "kind": "idea-novelty-check",
                "idea_id": "i01",
                "scope": {
                    "searched_through": "2026-09-08",
                    "evidence_boundary": "fixture",
                    "status": "complete",
                },
                "query_families": [
                    {
                        "family": "exact-proposition",
                        "formulations": ["has c01 been established?"],
                        "status": "searched",
                    }
                ],
                "channels": [{"channel": "journal-index", "status": "searched"}],
                "candidates": [],
                "claims": [
                    {
                        "claim_id": "c01",
                        "contribution_role": "central",
                        "search_question": "has c01 been established?",
                        "closest_results": [],
                        "closest_work": "explicit none found",
                        "evidence_depth": "full-text",
                        "rejection_case": "rejection",
                        "defense_case": "defense",
                        "delta_tuple": {
                            "research_question": "different",
                            "mechanism": "different",
                            "identification_or_setting": "shared",
                            "outcome": "different",
                        },
                        "remaining_delta": "delta",
                        "verdict": "novel",
                        "confidence": "medium",
                        "limitation": "bounded search",
                    }
                ],
                "limits": ["fixture"],
                "created_at": "2026-09-08T11:20:00-04:00",
            },
        )
        self.write(
            "workflow/pressure/i01_receipt.yaml",
            {
                "version": 1,
                "kind": "idea-pressure-test",
                "idea_id": "i01",
                "chain": {
                    "claim": "falsifiable claim",
                    "mechanism": "mechanism",
                    "design": "design",
                    "outcome": "outcome",
                },
                "falsifiable": True,
                "fatal_assumptions": [],
                "repairable_weaknesses": [],
                "identification": {
                    "credibility": "conditional",
                    "confounds": [],
                    "repair_path": "test",
                },
                "minimum_experiment": {
                    "question": "question",
                    "population": "population",
                    "exposure": "exposure",
                    "comparator": "comparator",
                    "outcome": "outcome",
                    "estimator_or_rule": "estimator",
                    "expected_artifact": "report",
                    "task_result": "pilot.yaml",
                    "acceptance_rule": "rule",
                    "failure_interpretation": "revise",
                },
                "pilot": {
                    "status": "positive",
                    "task_result": "pilot.yaml",
                    "waiver": None,
                },
                "ethics_privacy": [],
                "residual_risks": [],
                "next_test": "replicate",
                "created_at": "2026-09-08T11:25:00-04:00",
            },
        )
        self.write("pilot.yaml", {"kind": "task-runtime"})
        self.card["core_claims"][0]["novelty_check"] = {
            "search_question": "has c01 been established?",
            "closest_work": "explicit none found",
            "remaining_delta": "delta",
            "rejection_case": "rejection",
            "defense_case": "defense",
            "delta_tuple": {
                "research_question": "different",
                "mechanism": "different",
                "identification_or_setting": "shared",
                "outcome": "different",
            },
            "evidence_depth": "full-text",
            "limitation": "bounded search",
            "status": "novel",
            "receipt": "workflow/novelty/i01_receipt.yaml",
        }
        self.card["identification"] = {"credibility": "conditional", "fatal_assumptions": [], "repair_path": "test"}
        self.card["feasibility"] = {
            "pilot": "positive",
            "receipt": "pilot.yaml",
            "pressure_receipt": "workflow/pressure/i01_receipt.yaml",
            "waiver": "",
        }
        self.card["venue_fit"].update({"broad_screen": "complete", "deep_fit": "complete", "overall": "strong"})
        self.write("cards/i01_idea.yaml", self.card)
        self.write(
            "cards/venue-fit/i01_venue-fit.yaml",
            {
                "kind": "idea-venue-fit",
                "broad_screen": {"status": "complete"},
                "candidates": [
                    {
                        "id": "v01",
                        "target": "Journal",
                        "category": "Article",
                        "profile": "deep-fit",
                        "venue_contract": {
                            "status": "current",
                            "path": "venue-contract.md#versioned-contract",
                        },
                    }
                ],
            },
        )
        self.write(
            "cards/test-matrix.yaml",
            {
                "kind": "ideation-test-matrix",
                "ideas": [
                    {
                        "idea_id": "i01",
                        "novelty": "ready",
                        "identification": "conditional",
                        "feasibility": "positive",
                        "journal_fit": "strong",
                        "nature_shape": "not-requested",
                        "receipts": {
                            "novelty": "workflow/novelty/i01_receipt.yaml",
                            "pressure": "workflow/pressure/i01_receipt.yaml",
                            "venue_fit": "cards/venue-fit/i01_venue-fit.yaml",
                        },
                        "fatal_blockers": [],
                        "repairable_gaps": [],
                        "next_route": "select",
                    }
                ],
            },
        )

    def test_generate_gate_passes_minimum_scientific_object(self) -> None:
        result = self.run_gate("generate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_sync_gate_passes_without_selection_authority(self) -> None:
        self.write_sync()
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_sync_gate_rejects_selection_leak(self) -> None:
        self.write_sync()
        path = self.unit / "projection/paper-ideation-sync.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["selected_cards"] = ["cards/i01_idea.yaml"]
        self.write("projection/paper-ideation-sync.yaml", value)
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 1)
        self.assertIn("selection-leak", result.stdout)

    def test_test_gate_rejects_unverified_claim(self) -> None:
        self.write(
            "cards/test-matrix.yaml",
            {
                "kind": "ideation-test-matrix",
                "ideas": [
                    {
                        "idea_id": "i01",
                        "novelty": "hold",
                        "identification": "unknown",
                        "feasibility": "pending",
                        "journal_fit": "unknown",
                        "nature_shape": "not-requested",
                        "receipts": {
                            "novelty": "pending",
                            "pressure": "pending",
                            "venue_fit": "pending",
                        },
                        "next_route": "novelty",
                    }
                ],
            },
        )
        result = self.run_gate("test")
        self.assertEqual(result.returncode, 1)
        self.assertIn("novelty-open", result.stdout)
        self.assertNotIn("positive/negative pilot requires feasibility.receipt", result.stdout)

    def test_test_gate_passes_reconciled_evidence(self) -> None:
        self.make_test_ready()
        result = self.run_gate("test")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_select_and_handoff_gates(self) -> None:
        self.make_test_ready()
        self.write_sync("I2")
        self.write(
            "workflow/selection.yaml",
            {
                "kind": "ideation-selection",
                "decision": "select",
                "selection_posture": "proceed-with-caution",
                "selected_cards": ["cards/i01_idea.yaml"],
                "story_routes": [{"card": "cards/i01_idea.yaml", "story_role": "Story-A", "story_path": "Paper/A1-Story/StoryA/StoryA.md"}],
                "target_routes": [{"card": "cards/i01_idea.yaml", "target": "Journal", "category": "Article", "venue_contract": "venue-contract.md#versioned-contract"}],
                "by": "person:test",
                "at": "2026-09-08T12:00:00-04:00",
                "accepted_risks": ["risk"],
                "assertions": {
                    "evidence_complete": True,
                    "novelty_reviewed": True,
                    "feasibility_receipt_or_waiver": True,
                    "venue_fit_reviewed": True,
                    "target_selected": True,
                },
                "reason": "bounded decision",
            },
        )
        self.write("venue-contract.md", {"versioned_contract": {"state": "current"}})
        selected = self.run_gate("select")
        self.assertEqual(selected.returncode, 0, selected.stdout + selected.stderr)

        self.write(
            "handoff/paper-ideation.yaml",
            {
                "kind": "paper-ideation-handoff",
                "source": {
                    "direction_card": "cards/direction.yaml",
                    "evidence_bundle": "bundle/evidence-bundle.yaml",
                    "paper_ideation_sync": "projection/paper-ideation-sync.yaml",
                    "selection_receipt": "workflow/selection.yaml",
                },
                "selected_ideas": [
                    {
                        "card": "cards/i01_idea.yaml",
                        "story_role": "Story-A",
                        "story_path": "Paper/A1-Story/StoryA/StoryA.md",
                        "claim_ids": ["c01"],
                        "evidence_ids": ["ext01"],
                        "feasibility_receipt_or_waiver": "pilot.yaml",
                        "venue_fit_card": "cards/venue-fit/i01_venue-fit.yaml",
                        "intended_target": "Journal",
                        "intended_category": "Article",
                        "venue_contract": "venue-contract.md#versioned-contract",
                        "hard_limits": ["no causal claim"],
                    }
                ],
                "paper_route": "haipipe-paper-ideation",
                "status": "ready",
                "created_at": "2026-09-08T12:05:00-04:00",
            },
        )
        handoff = self.run_gate("handoff")
        self.assertEqual(handoff.returncode, 0, handoff.stdout + handoff.stderr)

    def test_defer_decision_can_preserve_open_tests(self) -> None:
        self.write(
            "workflow/selection.yaml",
            {
                "kind": "ideation-selection",
                "decision": "defer",
                "by": "person:test",
                "at": "2026-09-08T12:00:00-04:00",
                "assertions": {
                    "evidence_complete": False,
                    "novelty_reviewed": False,
                    "feasibility_receipt_or_waiver": False,
                    "venue_fit_reviewed": False,
                    "target_selected": False,
                },
                "reason": "closest-work review remains open",
            },
        )
        result = self.run_gate("select")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
