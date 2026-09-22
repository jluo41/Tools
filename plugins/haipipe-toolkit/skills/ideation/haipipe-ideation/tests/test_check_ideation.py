from __future__ import annotations

import copy
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
            "question": "Does the idea hold beyond the rating?",
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
                "source_hash": "sha256:fixture",
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

    def write_sync_v2(self) -> None:
        self.write("Paper/A1-Story/Story00-ideation/Story00-ideation.md", {"kind": "fixture-paper-page"})
        self.write(
            "Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml",
            {
                "step": 1,
                "round": 1,
                "phase": "OUTLINE",
                "status": "ok",
                "paper_projection": {
                    "source_packet": "projection/paper-ideation-sync.yaml",
                    "source_revision": 2,
                    "source_hash": "sha256:sync-v2",
                    "page_path": "Paper/A1-Story/Story00-ideation/Story00-ideation.md",
                    "surface": "working",
                    "output_hash": "sha256:working-v2",
                    "created_at": "2026-09-13T10:00:00-04:00",
                },
            },
        )
        self.write(
            "Paper/A1-Story/Story00-ideation/workflow/receipts/release-v1.yaml",
            {
                "step": 2,
                "round": 1,
                "phase": "CONTENT",
                "status": "ok",
                "paper_projection": {
                    "source_packet": "projection/paper-ideation-sync.yaml",
                    "source_revision": 1,
                    "source_hash": "sha256:sync-v1",
                    "page_path": "Paper/A1-Story/Story00-ideation/Story00-ideation.md",
                    "surface": "release",
                    "output_hash": "sha256:release-v1",
                    "created_at": "2026-09-12T10:00:00-04:00",
                },
            },
        )
        self.write(
            "projection/paper-ideation-sync.yaml",
            {
                "version": 2,
                "kind": "paper-ideation-sync",
                "source": {
                    "ideation_task": "b01.j01.t01",
                    "ideation_manifest": "ideation.yaml",
                    "evidence_bundle": "bundle/evidence-bundle.yaml",
                    "direction_card": "cards/direction.yaml",
                    "test_matrix": None,
                },
                "stage": "I1",
                "sync_revision": 2,
                "source_hash": "sha256:sync-v2",
                "projection": {
                    "change_class": "state",
                    "affected_idea_ids": ["i01"],
                    "identity_key": "idea_id",
                },
                "paper_page": {
                    "state": "bound",
                    "path": "Paper/A1-Story/Story00-ideation/Story00-ideation.md",
                    "working": {
                        "state": "current",
                        "revision": 2,
                        "source_hash": "sha256:sync-v2",
                        "receipt": "Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml",
                    },
                    "release": {
                        "state": "stale",
                        "revision": 1,
                        "source_hash": "sha256:sync-v1",
                        "receipt": "Paper/A1-Story/Story00-ideation/workflow/receipts/release-v1.yaml",
                    },
                    "delivery": {
                        "state": "not-requested",
                        "revision": None,
                        "source_hash": None,
                        "receipt": None,
                    },
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
                        "novelty": "unverified",
                        "identification": "unknown",
                        "feasibility": "pending",
                        "journal_fit": "pending",
                        "next_route": "novelty",
                    }
                ],
                "portfolio_recommendation": {
                    "status": "not-reviewed",
                    "summary": "machine comparison only; not a decision",
                    "ideas": [{"idea_id": "i01", "recommendation": "unresolved", "reason": "open"}],
                },
                "selection_authority": {"owner": "haipipe-ideation-select", "status": "none", "receipt": None},
                "sync_status": "current",
                "open_gaps": ["novelty"],
                "updated_at": "2026-09-13T10:00:00-04:00",
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

    def read(self, relative: str) -> dict:
        return yaml.safe_load((self.unit / relative).read_text())

    def write_contract(self) -> None:
        self.write("official.md", {"kind": "discovery-result", "verified": True})
        self.write("venue-contract.md", {"versioned_contract": {
            "schema_version": 1, "contract_version": "v1",
            "target": "Journal", "category": "Article", "profile": "cfp-only",
            "state": "current", "verified_at": "2026-09-08", "refresh_due": None,
            "official_source_results": ["official.md"], "blocking_unknowns": [],
        }})

    def make_test_ready(self) -> None:
        self.write_contract()
        bundle = self.read("bundle/evidence-bundle.yaml")
        bundle["sources"]["external"] = [{"id": "ext01", "result": "official.md"}]
        self.write("brief.md", {"kind": "fixture-brief"})
        bundle["sources"]["context"] = [{"id": "context01", "path": "brief.md", "claim_support": False}]
        self.write("bundle/evidence-bundle.yaml", bundle)
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

    def add_candidate(self, idea_id: str, ready: bool = True) -> str:
        card = copy.deepcopy(self.read("cards/i01_idea.yaml"))
        card.update(id=idea_id, canonical_id=idea_id, state="open")
        card.pop("decision_ref", None)
        card["venue_fit"].update(card=f"venue-fit/{idea_id}_venue-fit.yaml", human_target="open")
        fit = copy.deepcopy(self.read("cards/venue-fit/i01_venue-fit.yaml"))
        self.write(f"cards/venue-fit/{idea_id}_venue-fit.yaml", fit)
        if ready:
            for lane in ("novelty", "pressure"):
                receipt = self.read(f"workflow/{lane}/i01_receipt.yaml")
                receipt["idea_id"] = idea_id
                self.write(f"workflow/{lane}/{idea_id}_receipt.yaml", receipt)
            card["core_claims"][0]["novelty_check"]["receipt"] = f"workflow/novelty/{idea_id}_receipt.yaml"
            card["feasibility"]["pressure_receipt"] = f"workflow/pressure/{idea_id}_receipt.yaml"
        else:
            card["core_claims"][0]["novelty_check"] = {"status": "unverified", "evidence_depth": "none"}
            card["identification"]["credibility"] = "unknown"
            card["feasibility"] = {"pilot": "pending", "receipt": None, "pressure_receipt": None}
            card["venue_fit"]["deep_fit"] = "pending"
        raw = f"cards/{idea_id}_idea.yaml"
        self.write(raw, card)
        matrix = self.read("cards/test-matrix.yaml")
        row = copy.deepcopy(matrix["ideas"][0])
        row["idea_id"] = idea_id
        row["receipts"] = {
            "novelty": f"workflow/novelty/{idea_id}_receipt.yaml" if ready else "pending",
            "pressure": f"workflow/pressure/{idea_id}_receipt.yaml" if ready else "pending",
            "venue_fit": f"cards/venue-fit/{idea_id}_venue-fit.yaml",
        }
        if not ready:
            row.update(novelty="hold", identification="unknown", feasibility="pending", next_route="defer")
        matrix["ideas"].append(row)
        self.write("cards/test-matrix.yaml", matrix)
        return raw

    def make_selection_v3(self, dispositions: dict[str, str] | None = None) -> None:
        self.write_sync_v2()
        dispositions = dispositions or {"i01": "select"}
        receipt = {
            "version": 3, "kind": "ideation-selection", "id": "s01",
            "snapshot": "workflow/selections/s01.yaml",
            "source": {"sync_revision": 2, "source_hash": "sha256:sync-v2"},
            "by": "person:test", "at": "2026-09-20T12:00:00-04:00", "reason": "Explicit answers",
            "reviewed_cards": [], "candidates": [], "selected_cards": [], "story_routes": [], "target_routes": [],
        }
        sync = self.read("projection/paper-ideation-sync.yaml")
        sync["stage"] = "I2"
        sync["source"]["test_matrix"] = "cards/test-matrix.yaml"
        sync["ideas"] = []
        sync["portfolio_recommendation"] = {
            "status": "provisional", "summary": "Fixture machine comparison, separate from human answers", "ideas": [],
        }
        handoff_rows = []
        for index, (idea_id, disposition) in enumerate(dispositions.items()):
            raw = f"cards/{idea_id}_idea.yaml"
            card = self.read(raw)
            row = {"card": raw, "disposition": disposition, "reason": "The person's answer" if disposition != "open" else "Awaiting an answer"}
            receipt["reviewed_cards"].append(raw)
            if disposition == "select":
                target = {"venue_fit_card": f"cards/venue-fit/{idea_id}_venue-fit.yaml", "target": "Journal", "category": "Article",
                          "venue_contract": "venue-contract.md#versioned-contract", "contract_version": "v1"}
                story = {"story_role": f"Story-{index}", "story_path": f"Paper/Story{index}/Story{index}.md"}
                row.update(posture="proceed-with-caution" if index == 0 else "proceed",
                           accepted_risks=["Associational only"] if index == 0 else [],
                           target_route=target, story_route=story,
                           assertions={key: True for key in ("evidence_complete", "novelty_reviewed", "feasibility_receipt_or_waiver", "venue_fit_reviewed", "target_selected")})
                receipt["selected_cards"].append(raw)
                receipt["story_routes"].append({"card": raw, **story})
                receipt["target_routes"].append({"card": raw, **target})
                handoff_rows.append({"card": raw, **story, "claim_ids": ["c01"], "evidence_ids": ["ext01"],
                                     "feasibility_receipt_or_waiver": "pilot.yaml", "venue_fit_card": target["venue_fit_card"],
                                     "intended_target": "Journal", "intended_category": "Article", "venue_contract": target["venue_contract"],
                                     "contract_version": "v1", "selection_posture": row["posture"], "accepted_risks": row["accepted_risks"],
                                     "hard_limits": ["No causal claim"]})
            receipt["candidates"].append(row)
            state = {"select": "selected", "defer": "deferred", "abandon": "eliminated", "open": "open"}[disposition]
            human_target = {"select": "selected", "defer": "deferred", "abandon": "rejected", "open": "open"}[disposition]
            card["state"] = state
            card["venue_fit"]["human_target"] = human_target
            if disposition != "open":
                card["decision_ref"] = receipt["snapshot"]
                fit_path = f"cards/venue-fit/{idea_id}_venue-fit.yaml"
                fit = self.read(fit_path)
                target = row.get("target_route", {})
                fit["human_target"] = {"status": human_target, "selection_receipt": receipt["snapshot"],
                    **{key: target.get(key, "") for key in ("target", "category", "venue_contract", "contract_version")},
                    "by": receipt["by"], "at": receipt["at"], "accepted_conditions": row.get("accepted_risks", [])}
                self.write(fit_path, fit)
            self.write(raw, card)
            sync["portfolio_recommendation"]["ideas"].append({
                "idea_id": idea_id, "recommendation": card["recommendation"], "reason": "Fixture machine advice",
            })
            matrix_row = next(r for r in self.read("cards/test-matrix.yaml")["ideas"] if r["idea_id"] == idea_id)
            sync["ideas"].append({"card": raw, "state": state, "decision_ref": card.get("decision_ref"),
                **{key: matrix_row[key] for key in ("novelty", "identification", "feasibility", "journal_fit", "next_route")}})
        receipt["decision"] = "select" if receipt["selected_cards"] else "defer" if "defer" in dispositions.values() else "abandon" if set(dispositions.values()) == {"abandon"} else "open"
        self.write("projection/paper-ideation-sync.yaml", sync)
        manifest = self.read("ideation.yaml")
        manifest.update(stage="select", state={"select": "selected", "defer": "deferred", "abandon": "abandoned", "open": "open"}[receipt["decision"]])
        self.write("ideation.yaml", manifest)
        self.save_selection(receipt)
        handoff = {"version": 3, "kind": "paper-ideation-handoff", "id": "s01", "snapshot": "handoff/history/s01.yaml",
            "source": {"direction_card": "cards/direction.yaml", "evidence_bundle": "bundle/evidence-bundle.yaml",
                       "paper_ideation_sync": "projection/paper-ideation-sync.yaml", "selection_receipt": receipt["snapshot"], **receipt["source"]},
            "selected_ideas": handoff_rows, "paper_route": "haipipe-paper-ideation", "status": "ready", "created_at": "2026-09-20T12:05:00-04:00"}
        self.save_handoff(handoff)

    def save_selection(self, receipt: dict) -> None:
        self.write("workflow/selection.yaml", receipt)
        self.write(receipt["snapshot"], receipt)

    def save_handoff(self, handoff: dict) -> None:
        self.write("handoff/paper-ideation.yaml", handoff)
        self.write(handoff["snapshot"], handoff)

    def assert_gate(self, gate: str, ok: bool, code: str = "") -> None:
        result = self.run_gate(gate)
        self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
        if code:
            self.assertIn(code, result.stdout)

    def test_v3_selected_subset_preserves_unselected_hold(self) -> None:
        self.make_test_ready()
        self.add_candidate("i03", ready=False)
        self.make_selection_v3({"i01": "select", "i03": "defer"})
        self.assert_gate("select", True)
        self.assert_gate("handoff", True)
        self.assert_gate("test", False, "novelty-open")

    def test_v3_mixed_dispositions_and_per_card_risks(self) -> None:
        self.make_test_ready()
        for idea_id in ("i02", "i03", "i04", "i05"):
            self.add_candidate(idea_id)
        self.make_selection_v3({"i01": "select", "i02": "select", "i03": "defer", "i04": "abandon", "i05": "open"})
        self.assert_gate("handoff", True)
        receipt = self.read("workflow/selection.yaml")
        receipt["candidates"][0]["accepted_risks"] = []
        self.save_selection(receipt)
        self.assert_gate("select", False, "risk-missing")

    def test_unanswered_state_cannot_be_eliminated_by_machine(self) -> None:
        self.card.update(state="eliminated")
        self.write("cards/i01_idea.yaml", self.card)
        self.assert_gate("generate", False, "decision_ref")

    def test_selected_open_or_preempted_claim_is_ineligible(self) -> None:
        for status in ("unverified", "preempted"):
            with self.subTest(status=status):
                self.make_test_ready()
                card = self.read("cards/i01_idea.yaml")
                card["core_claims"][0]["novelty_check"]["status"] = status
                self.write("cards/i01_idea.yaml", card)
                novelty = self.read("workflow/novelty/i01_receipt.yaml")
                novelty["claims"][0]["verdict"] = status
                self.write("workflow/novelty/i01_receipt.yaml", novelty)
                matrix = self.read("cards/test-matrix.yaml")
                matrix["ideas"][0].update(novelty="preempted" if status == "preempted" else "hold", next_route="abandon")
                self.write("cards/test-matrix.yaml", matrix)
                self.make_selection_v3()
                self.assert_gate("select", False, "novelty-ineligible")

    def test_same_length_wrong_card_routes_are_rejected(self) -> None:
        self.make_test_ready()
        self.add_candidate("i02")
        self.make_selection_v3({"i01": "select", "i02": "open"})
        receipt = self.read("workflow/selection.yaml")
        receipt["target_routes"][0]["card"] = "cards/i02_idea.yaml"
        self.save_selection(receipt)
        self.assert_gate("select", False, "route-card-drift")

    def test_handoff_must_match_the_selected_set_and_target(self) -> None:
        self.make_test_ready()
        self.add_candidate("i02")
        self.make_selection_v3({"i01": "select", "i02": "open"})
        original = self.read("handoff/paper-ideation.yaml")
        for field, value, code in (("card", "cards/i02_idea.yaml", "selection-drift"),
                                   ("intended_target", "Other Journal", "target-drift"),
                                   ("contract_version", "old", "selection-drift"),
                                   ("claim_ids", ["missing"], "claim-drift"),
                                   ("evidence_ids", ["missing"], "evidence-drift"),
                                   ("feasibility_receipt_or_waiver", "official.md", "feasibility-drift")):
            with self.subTest(field=field):
                handoff = copy.deepcopy(original)
                handoff["selected_ideas"][0][field] = value
                self.save_handoff(handoff)
                self.assert_gate("handoff", False, code)

    def test_current_view_cannot_drift_from_snapshot(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        receipt = self.read("workflow/selection.yaml")
        receipt["reason"] = "Changed without a new version"
        self.write("workflow/selection.yaml", receipt)
        self.assert_gate("select", False, "snapshot-drift")

    def test_contract_content_and_fenced_markdown(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        original = self.read("venue-contract.md")
        (self.unit / "venue-contract.md").write_text("# Venue\n\n~~~yaml\n" + yaml.safe_dump(original) + "~~~\n")
        self.assert_gate("select", True)
        for key, value in (("target", "Wrong"), ("category", "Wrong"), ("state", "stale"), ("contract_version", "v2"),
                           ("blocking_unknowns", ["unresolved scope"]), ("official_source_results", ["missing.md"])):
            with self.subTest(key=key):
                record = copy.deepcopy(original)
                record["versioned_contract"][key] = value
                self.write("venue-contract.md", record)
                self.assert_gate("select", False)

    def test_sync_revision_and_selection_source_must_match(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        handoff = self.read("handoff/paper-ideation.yaml")
        handoff["source"]["sync_revision"] = 99
        self.save_handoff(handoff)
        self.assert_gate("handoff", False, "sync-stale")
        handoff["source"]["sync_revision"] = 2
        handoff["source"]["selection_receipt"] = "workflow/selection.yaml"
        self.save_handoff(handoff)
        self.assert_gate("handoff", False, "source-drift")

    def test_duplicate_physical_story_paths_are_rejected(self) -> None:
        self.make_test_ready()
        self.add_candidate("i02")
        self.make_selection_v3({"i01": "select", "i02": "select"})
        receipt = self.read("workflow/selection.yaml")
        raw = receipt["story_routes"][0]["story_path"]
        receipt["story_routes"][1]["story_path"] = raw
        receipt["candidates"][1]["story_route"]["story_path"] = raw
        self.save_selection(receipt)
        self.assert_gate("select", False, "duplicate-route")

    def test_depth_alias_and_drift(self) -> None:
        self.make_test_ready()
        card = self.read("cards/i01_idea.yaml")
        card["core_claims"][0]["novelty_check"]["evidence_depth"] = "metadata-only"
        self.write("cards/i01_idea.yaml", card)
        receipt = self.read("workflow/novelty/i01_receipt.yaml")
        receipt["claims"][0]["evidence_depth"] = "metadata"
        self.write("workflow/novelty/i01_receipt.yaml", receipt)
        self.assert_gate("test", True)
        card["core_claims"][0]["novelty_check"]["evidence_depth"] = "none"
        self.write("cards/i01_idea.yaml", card)
        self.assert_gate("test", False, "receipt-drift")

    def test_skipped_history_requires_reason_but_no_task_result(self) -> None:
        self.make_test_ready()
        raw = self.add_candidate("i03", ready=False)
        card = self.read(raw)
        card["feasibility"].update(pilot="skipped", pressure_receipt="workflow/pressure/i03_receipt.yaml")
        self.write(raw, card)
        pressure = self.read("workflow/pressure/i01_receipt.yaml")
        pressure["idea_id"] = "i03"
        pressure["pilot"] = {"status": "skipped", "task_result": None, "reason": "Access not available", "waiver": None}
        self.write("workflow/pressure/i03_receipt.yaml", pressure)
        matrix = self.read("cards/test-matrix.yaml")
        matrix["ideas"][1]["receipts"]["pressure"] = "workflow/pressure/i03_receipt.yaml"
        self.write("cards/test-matrix.yaml", matrix)
        self.make_selection_v3({"i01": "select", "i03": "defer"})
        self.assert_gate("handoff", True)
        self.assert_gate("test", False, "feasibility-open")
        pressure["pilot"]["reason"] = ""
        self.write("workflow/pressure/i03_receipt.yaml", pressure)
        self.assert_gate("select", False, "reason-missing")

    def test_ready_summary_does_not_hide_unresolved_supporting_claim(self) -> None:
        self.make_test_ready()
        card = self.read("cards/i01_idea.yaml")
        card["core_claims"].append({"id": "c02", "claim": "support", "contribution_role": "supporting",
                                    "novelty_check": {"status": "unverified", "evidence_depth": "none"}})
        self.write("cards/i01_idea.yaml", card)
        self.make_selection_v3()
        self.assert_gate("select", False, "novelty-ineligible")

    def test_v3_projection_drift_is_rejected(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        fit = self.read("cards/venue-fit/i01_venue-fit.yaml")
        fit["human_target"]["target"] = "Other Journal"
        self.write("cards/venue-fit/i01_venue-fit.yaml", fit)
        self.assert_gate("select", False, "target-projection")

    def test_nonselect_does_not_authorize_handoff(self) -> None:
        self.make_test_ready()
        self.make_selection_v3({"i01": "defer"})
        self.assert_gate("select", True)
        self.assert_gate("handoff", False, "selection-open")

    def test_early_defer_can_close_before_venue_work(self) -> None:
        self.make_test_ready()
        self.make_selection_v3({"i01": "defer"})
        (self.unit / "cards/venue-fit/i01_venue-fit.yaml").unlink()
        self.assert_gate("select", True)

    def test_open_draft_and_empty_select_do_not_close(self) -> None:
        self.make_test_ready()
        self.make_selection_v3({"i01": "open"})
        self.assert_gate("select", False, "selection-open")
        receipt = self.read("workflow/selection.yaml")
        receipt["decision"] = "select"
        self.save_selection(receipt)
        self.assert_gate("select", False, "missing-selection")

    def test_reselection_preserves_immutable_history(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        old_selection = (self.unit / "workflow/selections/s01.yaml").read_bytes()
        old_handoff = (self.unit / "handoff/history/s01.yaml").read_bytes()
        sync = self.read("projection/paper-ideation-sync.yaml")
        sync.update(sync_revision=3, source_hash="sha256:revised")
        self.write("projection/paper-ideation-sync.yaml", sync)
        self.assert_gate("handoff", False, "sync-stale")
        receipt = self.read("workflow/selection.yaml")
        receipt.update(id="s02", snapshot="workflow/selections/s02.yaml",
                       source={"sync_revision": 3, "source_hash": "sha256:revised"})
        self.save_selection(receipt)
        card = self.read("cards/i01_idea.yaml")
        card["decision_ref"] = receipt["snapshot"]
        self.write("cards/i01_idea.yaml", card)
        fit = self.read("cards/venue-fit/i01_venue-fit.yaml")
        fit["human_target"]["selection_receipt"] = receipt["snapshot"]
        self.write("cards/venue-fit/i01_venue-fit.yaml", fit)
        sync["ideas"][0]["decision_ref"] = receipt["snapshot"]
        sync["paper_page"]["working"].update(revision=3, source_hash="sha256:revised")
        working = self.read("Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml")
        working["paper_projection"].update(source_revision=3, source_hash="sha256:revised")
        self.write("Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml", working)
        self.write("projection/paper-ideation-sync.yaml", sync)
        handoff = self.read("handoff/paper-ideation.yaml")
        handoff.update(id="s02", snapshot="handoff/history/s02.yaml")
        handoff["source"].update(selection_receipt=receipt["snapshot"], **receipt["source"])
        self.save_handoff(handoff)
        self.assert_gate("handoff", True)
        self.assertEqual((self.unit / "workflow/selections/s01.yaml").read_bytes(), old_selection)
        self.assertEqual((self.unit / "handoff/history/s01.yaml").read_bytes(), old_handoff)

    def test_v3_requires_current_physical_working_projection(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        original = self.read("projection/paper-ideation-sync.yaml")
        self.write_sync("I2")
        self.assert_gate("select", False, "sync-stale")
        self.write("projection/paper-ideation-sync.yaml", original)
        (self.unit / original["paper_page"]["path"]).unlink()
        self.assert_gate("handoff", False, "broken-path")

    def test_matrix_cannot_link_another_candidate_receipt(self) -> None:
        self.make_test_ready()
        self.add_candidate("i03", ready=False)
        self.make_selection_v3({"i01": "select", "i03": "defer"})
        matrix = self.read("cards/test-matrix.yaml")
        matrix["ideas"][1]["receipts"]["novelty"] = "workflow/novelty/i01_receipt.yaml"
        self.write("cards/test-matrix.yaml", matrix)
        self.assert_gate("select", False, "matrix-receipt-drift")

    def test_manifest_cannot_override_the_current_decision(self) -> None:
        self.make_test_ready()
        self.make_selection_v3()
        manifest = self.read("ideation.yaml")
        manifest.update(stage="generate", state="open")
        self.write("ideation.yaml", manifest)
        self.assert_gate("select", False, "manifest-projection")

    def test_generate_gate_passes_minimum_scientific_object(self) -> None:
        result = self.run_gate("generate")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_sync_gate_passes_without_selection_authority(self) -> None:
        self.write_sync()
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_generate_gate_reports_a_title_shaped_question_as_unframed(self) -> None:
        # an Idea is the research question it asks; a topic label in `question` is not one
        card = dict(self.card)
        card["question"] = "Selection and ordering audit"
        self.write("cards/i01_idea.yaml", card)
        result = self.run_gate("generate")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unframed-idea", result.stdout)

    def test_generate_gate_requires_the_question(self) -> None:
        card = dict(self.card)
        del card["question"]
        self.write("cards/i01_idea.yaml", card)
        result = self.run_gate("generate")
        self.assertEqual(result.returncode, 1)
        self.assertIn("question", result.stdout)

    def test_sync_gate_rejects_selection_leak(self) -> None:
        self.write_sync()
        path = self.unit / "projection/paper-ideation-sync.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["selected_cards"] = ["cards/i01_idea.yaml"]
        self.write("projection/paper-ideation-sync.yaml", value)
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 1)
        self.assertIn("selection-leak", result.stdout)

    def test_sync_v2_separates_working_release_and_delivery(self) -> None:
        self.write_sync_v2()
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_sync_v2_rejects_delivery_without_current_release(self) -> None:
        self.write_sync_v2()
        path = self.unit / "projection/paper-ideation-sync.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["paper_page"]["delivery"] = {
            "state": "current",
            "revision": 2,
            "source_hash": "sha256:sync-v2",
            "receipt": "projection/receipts/delivery.yaml",
        }
        self.write("projection/paper-ideation-sync.yaml", value)
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 1)
        self.assertIn("delivery-ahead", result.stdout)

    def test_sync_v2_rejects_surface_revision_ahead_of_source(self) -> None:
        self.write_sync_v2()
        path = self.unit / "projection/paper-ideation-sync.yaml"
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        value["paper_page"]["working"]["revision"] = 3
        self.write("projection/paper-ideation-sync.yaml", value)
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 1)
        self.assertIn("revision-ahead", result.stdout)

    def test_sync_v2_rejects_receipt_source_drift(self) -> None:
        self.write_sync_v2()
        receipt = self.unit / "Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml"
        value = yaml.safe_load(receipt.read_text(encoding="utf-8"))
        value["paper_projection"]["source_hash"] = "sha256:other-source"
        self.write("Paper/A1-Story/Story00-ideation/workflow/receipts/working.yaml", value)
        result = self.run_gate("sync")
        self.assertEqual(result.returncode, 1)
        self.assertIn("receipt-drift", result.stdout)

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
        self.write_contract()
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
                    "sync_revision": 1, "source_hash": "sha256:fixture",
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
