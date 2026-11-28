#!/usr/bin/env python3
"""Mechanical stage-gate checks for one durable Ideation unit.

This checker validates shape and cross-file assertions only. It deliberately
does not score scientific novelty, identification quality, or editorial merit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml

from selection_contract import SelectionChecks
from projection_contract import ProjectionChecks


NOVELTY = {"novel", "partial", "preempted", "inconclusive", "unverified"}
IDENTIFICATION = {"strong", "conditional", "weak", "unknown"}
PILOT = {"positive", "negative", "skipped", "waived", "pending"}
FIT = {"strong", "conditional", "weak", "off-fit", "unknown"}
SEARCH_COVERAGE = {"searched", "planned-not-run", "unavailable", "omitted"}
READING_DEPTH = {"none", "metadata", "abstract", "full-text"}
MATRIX_NEXT = {
    "novelty",
    "pressure",
    "task",
    "discovery",
    "venue",
    "select",
    "defer",
    "abandon",
}
IDEA_ID = re.compile(r"^i\d+$")


@dataclass
class Finding:
    code: str
    path: str
    message: str


class GateCheck(SelectionChecks, ProjectionChecks):
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.findings: list[Finding] = []
        self.ideas: dict[str, tuple[Path, dict[str, Any]]] = {}
        self.matrix_rows: dict[str, dict[str, Any]] = {}
        self._generated = False

    def fail(self, code: str, path: Path | str, message: str) -> None:
        try:
            shown = str(Path(path).resolve().relative_to(self.root))
        except (ValueError, OSError):
            shown = str(path)
        self.findings.append(Finding(code, shown, message))

    def load(self, relative: str, required: bool = True) -> dict[str, Any] | None:
        path = self.root / relative
        if not path.is_file():
            if required:
                self.fail("missing-file", path, "required YAML file is absent")
            return None
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            self.fail("invalid-yaml", path, str(exc))
            return None
        if not isinstance(value, dict):
            self.fail("invalid-shape", path, "top-level YAML value must be a mapping")
            return None
        return value

    @staticmethod
    def nonempty(value: Any) -> bool:
        return value is not None and value != "" and value != [] and value != {}

    def require_keys(
        self, value: dict[str, Any], keys: Iterable[str], path: Path, prefix: str = ""
    ) -> None:
        for key in keys:
            if not self.nonempty(value.get(key)):
                field = f"{prefix}.{key}" if prefix else key
                self.fail("missing-field", path, f"required field {field!r} is empty")

    def require_present(
        self, value: dict[str, Any], keys: Iterable[str], path: Path, prefix: str = ""
    ) -> None:
        for key in keys:
            if key not in value:
                field = f"{prefix}.{key}" if prefix else key
                self.fail("missing-field", path, f"required field {field!r} is absent")

    def resolve_unit_path(self, raw: Any) -> Path | None:
        if not isinstance(raw, str) or not raw.strip():
            return None
        value = raw.split("#", 1)[0]
        path = Path(value)
        if path.is_absolute():
            return path
        local = self.root / path
        if local.exists():
            return local
        # Page-owned receipts may be stored beside, rather than inside, the
        # Ideation unit. Permit a repository-relative pointer by walking
        # ancestors, while keeping unit-local paths as the first authority.
        for parent in self.root.parents:
            candidate = parent / path
            if candidate.exists():
                return candidate
        return local

    def require_unit_path(self, raw: Any, owner: Path, field: str) -> None:
        path = self.resolve_unit_path(raw)
        if path is None:
            self.fail("missing-path", owner, f"{field} does not name a path")
        elif not path.exists():
            self.fail("broken-path", owner, f"{field} does not resolve: {raw}")

    def load_linked(self, raw: Any, owner: Path, field: str) -> tuple[Path, dict[str, Any]] | None:
        path = self.resolve_unit_path(raw)
        if path is None:
            self.fail("missing-path", owner, f"{field} does not name a path")
            return None
        if not path.is_file():
            self.fail("broken-path", owner, f"{field} does not resolve: {raw}")
            return None
        try:
            value = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            self.fail("invalid-yaml", path, str(exc))
            return None
        if not isinstance(value, dict):
            self.fail("invalid-shape", path, "top-level YAML value must be a mapping")
            return None
        return path, value

    def check_novelty_receipt(
        self,
        raw: Any,
        idea_id: str,
        claim: dict[str, Any],
        owner: Path,
    ) -> None:
        linked = self.load_linked(raw, owner, f"claim {claim.get('id', '<unknown>')} novelty receipt")
        if linked is None:
            return
        path, receipt = linked
        if receipt.get("kind") != "idea-novelty-check" or receipt.get("version") != 1:
            self.fail("wrong-kind", path, "novelty receipt must be version 1 kind idea-novelty-check")
        if receipt.get("idea_id") != idea_id:
            self.fail("receipt-drift", path, f"novelty receipt idea_id must be {idea_id}")
        self.require_keys(receipt, ["scope", "query_families", "channels", "claims", "created_at"], path)
        scope = receipt.get("scope")
        if not isinstance(scope, dict):
            self.fail("invalid-shape", path, "scope must be a mapping")
        else:
            self.require_keys(scope, ["searched_through", "evidence_boundary", "status"], path, "scope")
            if scope.get("status") not in {"complete", "bounded", "blocked"}:
                self.fail("invalid-status", path, "scope.status is invalid")
        for lane in ("query_families", "channels"):
            rows = receipt.get(lane)
            if not isinstance(rows, list) or not rows:
                continue
            identity = "family" if lane == "query_families" else "channel"
            for index, row in enumerate(rows, 1):
                if not isinstance(row, dict):
                    self.fail("invalid-row", path, f"{lane}[{index}] must be a mapping")
                    continue
                self.require_keys(row, [identity, "status"], path, f"{lane}[{index}]")
                if lane == "query_families":
                    self.require_keys(row, ["formulations"], path, f"{lane}[{index}]")
                if row.get("status") not in SEARCH_COVERAGE:
                    self.fail("invalid-status", path, f"{lane}[{index}].status is invalid")
                elif row.get("status") != "searched" and not self.nonempty(row.get("reason")):
                    self.fail("missing-field", path, f"{lane}[{index}].reason is required")
        claim_rows = receipt.get("claims")
        matching = [row for row in claim_rows or [] if isinstance(row, dict) and row.get("claim_id") == claim.get("id")]
        if len(matching) != 1:
            self.fail("receipt-drift", path, f"receipt must contain exactly one row for claim {claim.get('id')}")
            return
        row = matching[0]
        self.require_keys(
            row,
            [
                "contribution_role",
                "search_question",
                "closest_work",
                "evidence_depth",
                "rejection_case",
                "defense_case",
                "delta_tuple",
                "remaining_delta",
                "verdict",
                "confidence",
                "limitation",
            ],
            path,
            f"claims[{claim.get('id')}]",
        )
        if row.get("verdict") != claim.get("novelty_check", {}).get("status"):
            self.fail("receipt-drift", path, f"claim {claim.get('id')} verdict does not match Idea Card")
        depth = lambda value: "metadata" if value == "metadata-only" else value
        if depth(row.get("evidence_depth")) != depth(claim.get("novelty_check", {}).get("evidence_depth")):
            self.fail("receipt-drift", path, f"claim {claim.get('id')} evidence_depth differs from Idea Card")
        if depth(row.get("evidence_depth")) not in READING_DEPTH:
            self.fail("invalid-status", path, f"claim {claim.get('id')} evidence_depth is invalid")
        delta = row.get("delta_tuple")
        if isinstance(delta, dict):
            self.require_keys(delta, ["research_question", "mechanism", "identification_or_setting", "outcome"], path, "delta_tuple")

    def check_pressure_receipt(self, raw: Any, idea_id: str, idea: dict[str, Any], owner: Path) -> None:
        linked = self.load_linked(raw, owner, "feasibility.pressure_receipt")
        if linked is None:
            return
        path, receipt = linked
        if receipt.get("kind") != "idea-pressure-test" or receipt.get("version") != 1:
            self.fail("wrong-kind", path, "pressure receipt must be version 1 kind idea-pressure-test")
        if receipt.get("idea_id") != idea_id:
            self.fail("receipt-drift", path, f"pressure receipt idea_id must be {idea_id}")
        self.require_keys(
            receipt,
            [
                "chain",
                "falsifiable",
                "identification",
                "minimum_experiment",
                "pilot",
                "next_test",
                "created_at",
            ],
            path,
        )
        self.require_present(
            receipt,
            ["fatal_assumptions", "repairable_weaknesses", "ethics_privacy", "residual_risks"],
            path,
        )
        chain = receipt.get("chain")
        if isinstance(chain, dict):
            self.require_keys(chain, ["claim", "mechanism", "design", "outcome"], path, "chain")
        experiment = receipt.get("minimum_experiment")
        if isinstance(experiment, dict):
            self.require_keys(
                experiment,
                [
                    "question",
                    "population",
                    "exposure",
                    "comparator",
                    "outcome",
                    "estimator_or_rule",
                    "expected_artifact",
                    "acceptance_rule",
                    "failure_interpretation",
                ],
                path,
                "minimum_experiment",
            )
        pilot = receipt.get("pilot")
        if not isinstance(pilot, dict) or pilot.get("status") not in PILOT:
            self.fail("invalid-status", path, "pilot.status is invalid")
        else:
            feasibility = idea.get("feasibility", {})
            if pilot.get("status") != feasibility.get("pilot"):
                self.fail("receipt-drift", path, "pilot.status does not match Idea Card feasibility.pilot")
            if pilot.get("status") in {"positive", "negative"} and not self.same_path(pilot.get("task_result"), feasibility.get("receipt")):
                self.fail("receipt-drift", path, "pilot.task_result differs from Idea Card Task receipt")
            if pilot.get("status") == "skipped" and not self.nonempty(pilot.get("reason")):
                self.fail("reason-missing", path, "skipped pilot requires pilot.reason")
            if pilot.get("status") in {"pending", "skipped"} and self.nonempty(pilot.get("task_result")):
                self.fail("pilot-drift", path, "pending/skipped pilot must not claim a Task result")
            if pilot.get("status") == "waived" and pilot.get("waiver") != feasibility.get("waiver"):
                self.fail("receipt-drift", path, "pilot.waiver differs from Idea Card")

    def check_generate(self) -> None:
        if self._generated:
            return
        self._generated = True
        manifest = self.load("ideation.yaml")
        bundle = self.load("bundle/evidence-bundle.yaml")
        direction = self.load("cards/direction.yaml")

        if manifest is not None:
            if manifest.get("kind") != "ideation-unit":
                self.fail("wrong-kind", self.root / "ideation.yaml", "kind must be ideation-unit")
            self.require_keys(
                manifest,
                [
                    "version",
                    "address",
                    "direction",
                    "question",
                    "scope",
                    "decision_rule",
                    "stage",
                    "state",
                    "bundle",
                    "direction_card",
                    "created_at",
                    "updated_at",
                ],
                self.root / "ideation.yaml",
            )
            if manifest.get("stage") not in {"generate", "test", "select"}:
                self.fail("invalid-stage", self.root / "ideation.yaml", "stage must be generate, test, or select")
            if manifest.get("state") not in {"open", "held", "selected", "deferred", "abandoned"}:
                self.fail("invalid-state", self.root / "ideation.yaml", "state is invalid")
        if bundle is not None:
            if bundle.get("kind") != "ideation-evidence-bundle":
                self.fail(
                    "wrong-kind",
                    self.root / "bundle/evidence-bundle.yaml",
                    "kind must be ideation-evidence-bundle",
                )
            self.require_keys(bundle, ["direction", "sources", "policy"], self.root / "bundle/evidence-bundle.yaml")
            sources = bundle.get("sources")
            context = sources.get("context", []) if isinstance(sources, dict) else []
            if isinstance(context, list):
                for index, item in enumerate(context, 1):
                    if not isinstance(item, dict) or item.get("claim_support") is not False:
                        self.fail(
                            "context-as-support",
                            self.root / "bundle/evidence-bundle.yaml",
                            f"sources.context[{index}] must declare claim_support: false",
                        )
        if direction is not None:
            if direction.get("kind") != "direction-card":
                self.fail("wrong-kind", self.root / "cards/direction.yaml", "kind must be direction-card")
            self.require_keys(direction, ["id", "title", "question", "scope", "bundle"], self.root / "cards/direction.yaml")

        cards_dir = self.root / "cards"
        paths = sorted(cards_dir.glob("i*.yaml")) if cards_dir.is_dir() else []
        for path in paths:
            value = self.load(str(path.relative_to(self.root)))
            if value is None or value.get("kind") != "idea-card":
                continue
            idea_id = value.get("id")
            if not isinstance(idea_id, str) or not IDEA_ID.fullmatch(idea_id):
                self.fail("invalid-id", path, "Idea id must match iNN")
                continue
            if idea_id in self.ideas:
                self.fail("duplicate-id", path, f"Idea id {idea_id} appears more than once")
                continue
            self.ideas[idea_id] = (path, value)
            self.check_card_decision(path, value)
            venue = value.get("venue_fit")
            if value.get("state", "open") == "open" and isinstance(venue, dict) and venue.get("human_target", "open") != "open":
                self.fail("target-projection", path, "an unanswered card cannot have a decided human_target")
            self.require_keys(
                value,
                [
                    "canonical_id",
                    "title",
                    "question",
                    "claim",
                    "method",
                    "hypothesis",
                    "minimum_experiment",
                    "expected_outcome",
                    "failure_interpretation",
                    "core_claims",
                    "evidence_bundle",
                ],
                path,
            )
            question = value.get("question")
            if self.nonempty(question) and not str(question).strip().endswith("?"):
                self.fail("unframed-idea", path, "question must be the research question this Idea asks: one sentence ending in ?")
            claims = value.get("core_claims")
            if not isinstance(claims, list) or not claims:
                continue
            for index, claim in enumerate(claims, 1):
                if not isinstance(claim, dict):
                    self.fail("invalid-claim", path, f"core_claims[{index}] must be a mapping")
                    continue
                self.require_keys(claim, ["id", "claim", "novelty_check"], path, f"core_claims[{index}]")
                role = claim.get("contribution_role", "central")
                if role not in {"central", "supporting"}:
                    self.fail("invalid-role", path, f"core_claims[{index}].contribution_role is invalid")
                novelty = claim.get("novelty_check")
                if not isinstance(novelty, dict):
                    continue
                status = novelty.get("status")
                if status not in NOVELTY:
                    self.fail("invalid-status", path, f"core_claims[{index}].novelty_check.status is invalid")

        if not self.ideas:
            self.fail("missing-ideas", cards_dir, "at least one admitted Idea Card is required")

        generate_receipts = sorted((self.root / "workflow/generate").glob("*.yaml"))
        if not generate_receipts:
            self.fail("missing-generate-receipt", self.root / "workflow/generate", "at least one Generate receipt is required")
        for receipt_path in generate_receipts:
            receipt = self.load(str(receipt_path.relative_to(self.root)))
            if receipt is None:
                continue
            if receipt.get("kind") != "ideation-generate":
                self.fail("wrong-kind", receipt_path, "kind must be ideation-generate")
            self.require_keys(
                receipt,
                ["version", "id", "direction", "bundle", "lenses_attempted", "provisional_candidates", "created_at"],
                receipt_path,
            )

    def check_test(self, selected_ids: set[str] | None = None) -> None:
        """None checks full Test completion; a set scopes completion to selection."""
        self.check_generate()
        matrix = self.load("cards/test-matrix.yaml")
        if matrix is None:
            return
        if matrix.get("kind") != "ideation-test-matrix":
            self.fail("wrong-kind", self.root / "cards/test-matrix.yaml", "kind must be ideation-test-matrix")
        rows = matrix.get("ideas")
        if not isinstance(rows, list):
            self.fail("invalid-shape", self.root / "cards/test-matrix.yaml", "ideas must be a list")
            return
        self.matrix_rows.clear()
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("idea_id"), str):
                self.fail("invalid-row", self.root / "cards/test-matrix.yaml", "every matrix row needs idea_id")
                continue
            idea_id = row["idea_id"]
            if idea_id in self.matrix_rows:
                self.fail("duplicate-row", self.root / "cards/test-matrix.yaml", f"duplicate row for {idea_id}")
            self.matrix_rows[idea_id] = row
            self.require_keys(
                row,
                ["novelty", "identification", "feasibility", "journal_fit", "nature_shape", "receipts", "next_route"],
                self.root / "cards/test-matrix.yaml",
                idea_id,
            )
            if row.get("next_route") not in MATRIX_NEXT:
                self.fail("invalid-route", self.root / "cards/test-matrix.yaml", f"{idea_id} has invalid next_route")
            if idea_id not in self.ideas:
                self.fail("unknown-idea", self.root / "cards/test-matrix.yaml", f"unknown matrix Idea {idea_id}")

        for idea_id, (path, idea) in self.ideas.items():
            row = self.matrix_rows.get(idea_id)
            if row is None:
                self.fail("missing-row", self.root / "cards/test-matrix.yaml", f"no test row for {idea_id}")
                continue
            require_complete = selected_ids is None or idea_id in selected_ids
            is_selected = selected_ids is not None and idea_id in selected_ids
            terminal_preemption = row.get("next_route") == "abandon" and row.get("novelty") == "preempted"
            claims = idea.get("core_claims", [])
            if not isinstance(claims, list) or not claims:
                self.fail("missing-claims", path, "Core Claims must be a nonempty list")
                continue
            central_statuses: list[str] = []
            for index, claim in enumerate(claims, 1):
                novelty = claim.get("novelty_check", {}) if isinstance(claim, dict) else {}
                if not isinstance(novelty, dict):
                    self.fail("invalid-shape", path, f"claim {index} novelty_check must be a mapping")
                    continue
                status = novelty.get("status")
                if isinstance(claim, dict) and claim.get("contribution_role", "central") == "central" and isinstance(status, str):
                    central_statuses.append(status)
                if require_complete and status in {"unverified", "inconclusive"}:
                    self.fail("novelty-open", path, f"claim {index} remains {status}")
                if is_selected and status not in {"novel", "partial"}:
                    self.fail("novelty-ineligible", path, f"selected claim {index} must be novel or partial")
                for field in (
                    "search_question",
                    "closest_work",
                    "remaining_delta",
                    "rejection_case",
                    "defense_case",
                    "delta_tuple",
                    "evidence_depth",
                    "limitation",
                    "receipt",
                ):
                    if (require_complete or status in {"novel", "partial", "preempted"}) and not self.nonempty(novelty.get(field)):
                        self.fail("novelty-incomplete", path, f"claim {index} lacks novelty_check.{field}")
                depth = novelty.get("evidence_depth")
                if depth is not None and depth not in READING_DEPTH | {"metadata-only"}:
                    self.fail("invalid-depth", path, f"claim {index} evidence_depth is invalid")
                if self.nonempty(novelty.get("receipt")):
                    self.check_novelty_receipt(novelty.get("receipt"), idea_id, claim, path)

            if "preempted" in central_statuses:
                expected_novelty = "preempted"
            elif any(status in {"inconclusive", "unverified"} for status in central_statuses):
                expected_novelty = "hold"
            elif "partial" in central_statuses:
                expected_novelty = "partial"
            elif central_statuses and all(status == "novel" for status in central_statuses):
                expected_novelty = "ready"
            else:
                expected_novelty = "hold"
            if row.get("novelty") != expected_novelty:
                self.fail(
                    "novelty-projection",
                    self.root / "cards/test-matrix.yaml",
                    f"{idea_id} novelty should project to {expected_novelty}",
                )

            venue = idea.get("venue_fit")
            fit_data: dict[str, Any] | None = None
            if not isinstance(venue, dict) or venue.get("broad_screen") != "complete":
                self.fail("broad-screen-open", path, "venue_fit.broad_screen must be complete")
            elif self.nonempty(venue.get("card")):
                fit_raw = (
                    "cards/" + str(venue["card"]).lstrip("./")
                    if str(venue["card"]).startswith("venue-fit/")
                    else str(venue["card"])
                )
                self.require_unit_path(fit_raw, path, "venue fit card")
                fit_path = self.resolve_unit_path(fit_raw)
                if fit_path is not None and fit_path.is_file():
                    try:
                        loaded = yaml.safe_load(fit_path.read_text(encoding="utf-8"))
                        fit_data = loaded if isinstance(loaded, dict) else None
                        if fit_data is None or not isinstance(fit_data.get("broad_screen"), dict) or fit_data["broad_screen"].get("status") != "complete":
                            self.fail("broad-screen-drift", fit_path, "Venue Fit Card must confirm its complete broad screen")
                    except (OSError, yaml.YAMLError) as exc:
                        self.fail("invalid-yaml", fit_path, str(exc))
            else:
                self.fail("missing-path", path, "venue_fit.card is required")

            links = row.get("receipts")
            if not isinstance(links, dict):
                self.fail("invalid-shape", path, "matrix receipts must be a mapping")
            else:
                novelty_links = [c["novelty_check"].get("receipt") for c in claims if isinstance(c, dict) and isinstance(c.get("novelty_check"), dict) and self.nonempty(c["novelty_check"].get("receipt"))]
                pressure = idea.get("feasibility", {})
                expected_links = {
                    "novelty": novelty_links,
                    "pressure": [pressure.get("pressure_receipt")] if isinstance(pressure, dict) and self.nonempty(pressure.get("pressure_receipt")) else [],
                    "venue_fit": [self.fit_path(venue)] if isinstance(venue, dict) and self.nonempty(venue.get("card")) else [],
                }
                for field, expected in expected_links.items():
                    actual = links.get(field)
                    actual_list = actual if isinstance(actual, list) else [actual]
                    if expected:
                        if not all(any(self.same_path(raw, target) for target in expected) for raw in actual_list) or not all(any(self.same_path(raw, target) for raw in actual_list) for target in expected):
                            self.fail("matrix-receipt-drift", path, f"matrix {field} receipts differ from this card")
                    elif actual not in (None, "pending", "not-required") and actual != []:
                        self.fail("matrix-receipt-drift", path, f"matrix {field} must remain pending without a card receipt")

            feasibility = idea.get("feasibility", {})
            pilot = feasibility.get("pilot") if isinstance(feasibility, dict) else None
            expected_pilot = "pending" if pilot in {"pending", "skipped"} else pilot
            if row.get("feasibility") not in {expected_pilot, "hold"}:
                self.fail("feasibility-projection", path, "matrix feasibility differs from pilot (skipped maps to pending)")
            identification = idea.get("identification", {})
            if isinstance(identification, dict) and row.get("identification") != identification.get("credibility"):
                self.fail("identification-projection", path, "matrix identification differs from card")
            if not require_complete or (terminal_preemption and not is_selected):
                if isinstance(feasibility, dict) and self.nonempty(feasibility.get("pressure_receipt")):
                    self.check_pressure_receipt(feasibility["pressure_receipt"], idea_id, idea, path)
                continue
            if is_selected and (row.get("fatal_blockers") or row.get("feasibility") == "hold"):
                self.fail("selection-blocked", path, "selected card still has a fatal blocker or feasibility HOLD")
            identification = idea.get("identification")
            if not isinstance(identification, dict) or identification.get("credibility") not in IDENTIFICATION - {"unknown"}:
                self.fail("identification-open", path, "identification.credibility must be resolved")
            feasibility = idea.get("feasibility")
            if not isinstance(feasibility, dict):
                self.fail("feasibility-open", path, "feasibility block is required")
            else:
                pilot = feasibility.get("pilot")
                if pilot not in {"positive", "negative", "waived"}:
                    self.fail("feasibility-open", path, "pilot must be positive, negative, or waived")
                if pilot == "waived":
                    if not self.nonempty(feasibility.get("waiver")):
                        self.fail("waiver-missing", path, "waived pilot requires feasibility.waiver")
                elif pilot in {"positive", "negative"}:
                    if self.nonempty(feasibility.get("receipt")):
                        self.require_unit_path(feasibility.get("receipt"), path, "feasibility receipt")
                    else:
                        self.fail("missing-path", path, "positive/negative pilot requires feasibility.receipt")
                if self.nonempty(feasibility.get("pressure_receipt")):
                    self.check_pressure_receipt(feasibility.get("pressure_receipt"), idea_id, idea, path)
                else:
                    self.fail("missing-path", path, "feasibility.pressure_receipt is required")

            if (is_selected or row.get("next_route") == "select") and isinstance(venue, dict):
                if venue.get("deep_fit") != "complete":
                    self.fail("deep-fit-open", path, "Select route requires venue_fit.deep_fit complete")
                candidates = fit_data.get("candidates") if isinstance(fit_data, dict) else None
                finalists = [
                    item
                    for item in (candidates if isinstance(candidates, list) else [])
                    if isinstance(item, dict) and item.get("profile") == "deep-fit"
                ]
                if not finalists:
                    self.fail("missing-finalist", path, "Select route requires a deep-fit candidate")
                for finalist in finalists:
                    contract = finalist.get("venue_contract")
                    if not isinstance(contract, dict) or contract.get("status") != "current":
                        self.fail(
                            "venue-contract-open",
                            path,
                            f"deep-fit candidate {finalist.get('id', '<unknown>')} lacks a current Venue contract",
                        )
                    if isinstance(contract, dict):
                        self.check_venue_contract(contract.get("path"), finalist.get("target"), finalist.get("category"), path, contract.get("contract_version"))



def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("unit", type=Path, help="durable Ideation unit directory")
    parser.add_argument(
        "--gate",
        choices=("generate", "sync", "test", "select", "handoff"),
        required=True,
        help="stage gate to validate",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.unit.is_dir():
        result = {
            "ok": False,
            "gate": args.gate,
            "unit": str(args.unit),
            "findings": [{"code": "missing-unit", "path": str(args.unit), "message": "unit directory does not exist"}],
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"FAIL {args.gate}: {args.unit} does not exist")
        return 2

    check = GateCheck(args.unit)
    getattr(check, f"check_{args.gate}")()
    result = {
        "ok": not check.findings,
        "gate": args.gate,
        "unit": str(check.root),
        "idea_count": len(check.ideas),
        "findings": [asdict(item) for item in check.findings],
    }
    if args.json:
        print(json.dumps(result, indent=2))
    elif check.findings:
        print(f"FAIL {args.gate}: {len(check.findings)} finding(s)")
        for item in check.findings:
            print(f"- {item.code} {item.path}: {item.message}")
    else:
        print(f"PASS {args.gate}: {len(check.ideas)} Idea Card(s)")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
