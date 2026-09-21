"""Selection/target joins for the Ideation checker; no artifact writes."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re
from typing import Any

import yaml


ASSERTIONS = {
    "evidence_complete", "novelty_reviewed", "feasibility_receipt_or_waiver",
    "venue_fit_reviewed", "target_selected",
}
STATES = {"select": "selected", "defer": "deferred", "abandon": "eliminated", "open": "open"}
TARGET_STATES = {"select": "selected", "defer": "deferred", "abandon": "rejected", "open": "open"}


class SelectionChecks:
    """Mixin using GateCheck's read-only loaders and finding collector."""

    def same_path(self, left: Any, right: Any, *, fragment: bool = False) -> bool:
        a, b = self.resolve_unit_path(left), self.resolve_unit_path(right)
        if a is None or b is None or a.resolve() != b.resolve():
            return False
        return not fragment or str(left).partition("#")[2] == str(right).partition("#")[2]

    def card_identity(self, raw: Any, owner: Path) -> str | None:
        for idea_id, (path, idea) in self.ideas.items():
            if self.same_path(raw, str(path)):
                if idea.get("canonical_id") != idea_id:
                    self.fail("noncanonical-card", owner, f"{raw} must use its canonical Idea Card")
                    return None
                return idea_id
        self.fail("unknown-card", owner, f"not an admitted canonical Idea Card: {raw}")
        return None

    def card_map(self, rows: Any, owner: Path, field: str) -> dict[str, dict]:
        result: dict[str, dict] = {}
        if not isinstance(rows, list):
            self.fail("invalid-shape", owner, f"{field} must be a list")
            return result
        for row in rows:
            if not isinstance(row, dict):
                self.fail("invalid-shape", owner, f"{field} items must be mappings")
                continue
            identity = self.card_identity(row.get("card"), owner)
            if identity is None:
                continue
            if identity in result:
                self.fail("duplicate-card", owner, f"{field} repeats {identity}")
            result[identity] = row
        return result

    def human_stamp(self, value: dict, path: Path) -> None:
        by, at = value.get("by"), value.get("at")
        if not isinstance(by, str) or not by.startswith("person:") or not by[7:].strip():
            self.fail("human-missing", path, "by must name person:<identifier>")
        try:
            stamp = datetime.fromisoformat(str(at).replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError("missing timezone")
        except (ValueError, TypeError):
            self.fail("human-missing", path, "at must be an ISO-8601 timestamp with timezone")

    def check_snapshot(self, record: dict, path: Path, directory: str) -> None:
        record_id = record.get("id")
        if not isinstance(record_id, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", record_id):
            self.fail("invalid-id", path, "id must be a stable filename-safe decision id")
            return
        expected = f"{directory}/{record_id}.yaml"
        if record.get("snapshot") != expected:
            self.fail("snapshot-drift", path, f"snapshot must be {expected}")
            return
        linked = self.load_linked(expected, path, "immutable snapshot")
        if linked and linked[1] != record:
            self.fail("snapshot-drift", path, "current record differs from its immutable snapshot")

    def check_card_decision(self, path: Path, card: dict) -> None:
        """A historical disposition needs its own explicit human source."""
        state = card.get("state", "open")
        if state not in set(STATES.values()):
            self.fail("invalid-state", path, "Idea state is invalid")
        if state == "open":
            return
        linked = self.load_linked(card.get("decision_ref"), path, "card.decision_ref")
        if linked is None:
            return
        source_path, receipt = linked
        self.human_stamp(receipt, source_path)
        if receipt.get("kind") != "ideation-selection":
            self.fail("wrong-kind", source_path, "decision_ref must name an Ideation selection")
        if receipt.get("version") == 3:
            self.check_snapshot(receipt, source_path, "workflow/selections")
            rows = receipt.get("candidates")
            matches = [row for row in rows if isinstance(row, dict) and self.same_path(row.get("card"), str(path))] if isinstance(rows, list) else []
            if len(matches) != 1 or STATES.get(matches[0].get("disposition")) != state:
                self.fail("decision-drift", path, "state does not match the referenced per-card human disposition")
        else:
            selected = receipt.get("selected_cards", [])
            if state != "selected" or receipt.get("decision") != "select" or not isinstance(selected, list) or not any(self.same_path(raw, str(path)) for raw in selected):
                self.fail("decision-unattributed", path, "legacy global defer/abandon cannot establish a per-card disposition")

    def read_venue_contract(self, raw: Any, owner: Path) -> tuple[Path, dict] | None:
        path = self.resolve_unit_path(raw)
        if path is None or not path.is_file():
            self.fail("venue-contract-open", owner, f"Venue contract must resolve to a file: {raw}")
            return None
        if "#" in str(raw) and str(raw).partition("#")[2] not in {"versioned-contract", "versioned_contract"}:
            self.fail("venue-contract-open", owner, "Venue locator must identify its versioned contract block")
            return None
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as exc:
            self.fail("unreadable-contract", path, str(exc))
            return None
        # Venue owns this public block. Read YAML documents or fenced YAML in
        # a rich Markdown Page, without attempting to parse its prose as YAML.
        fences = re.findall(r"(?ms)^\s*(?:\x60{3}|~{3})(?:yaml|yml)\s*\n(.*?)^\s*(?:\x60{3}|~{3})\s*$", content)
        docs = fences if fences else [content]
        contracts = []
        for doc in docs:
            try:
                value = yaml.safe_load(doc)
            except yaml.YAMLError:
                continue
            if isinstance(value, dict) and isinstance(value.get("versioned_contract"), dict):
                contracts.append(value["versioned_contract"])
        if len(contracts) != 1:
            self.fail("venue-contract-open", path, "expected exactly one current versioned_contract block; archive older blocks separately")
            return None
        return path, contracts[0]

    def check_venue_contract(self, raw: Any, target: Any, category: Any, owner: Path, version: Any = None) -> None:
        linked = self.read_venue_contract(raw, owner)
        if linked is None:
            return
        path, contract = linked
        self.require_keys(contract, ["schema_version", "contract_version", "target", "category", "profile", "verified_at", "official_source_results"], path)
        if contract.get("schema_version") != 1 or contract.get("state") != "current":
            self.fail("venue-contract-open", path, "Venue contract must use schema 1 and state current")
        if not target or not category or (contract.get("target"), contract.get("category")) != (target, category):
            self.fail("target-drift", owner, "target/category do not match the named Venue contract")
        if version is not None and version != contract.get("contract_version"):
            self.fail("contract-version-drift", owner, "selected contract_version has changed")
        if contract.get("profile") not in {"pack-backed", "cfp-only"}:
            self.fail("venue-contract-open", path, "Venue profile is invalid")
        if contract.get("blocking_unknowns") != []:
            self.fail("venue-contract-open", path, "blocking_unknowns must be an empty list")
        try:
            verified = date.fromisoformat(str(contract.get("verified_at")))
            due = contract.get("refresh_due")
            if verified > date.today() or (due is not None and date.fromisoformat(str(due)) < date.today()):
                self.fail("venue-contract-open", path, "Venue verification is future-dated or refresh is overdue")
        except (TypeError, ValueError):
            self.fail("venue-contract-open", path, "invalid verified_at/refresh_due date")
        sources = contract.get("official_source_results")
        if not isinstance(sources, list) or not sources:
            self.fail("venue-contract-open", path, "official_source_results must be a nonempty list")
        else:
            for source in sources:
                self.require_unit_path(source, path, "official-source Result")

    def check_select(self) -> None:
        self.check_generate()
        self.selection = self.load("workflow/selection.yaml")
        self.selected_decisions = {}
        receipt = self.selection
        if receipt is None:
            return
        path = self.root / "workflow/selection.yaml"
        if receipt.get("kind") != "ideation-selection":
            self.fail("wrong-kind", path, "kind must be ideation-selection")
        version = receipt.get("version", 2)
        if version not in {2, 3}:
            self.fail("unsupported-version", path, "selection version must be 2 or 3")
            return
        self.human_stamp(receipt, path)
        self.require_keys(receipt, ["decision", "reason"], path)
        candidates = {}
        if version == 3:
            self.check_snapshot(receipt, path, "workflow/selections")
            candidates = self.card_map(receipt.get("candidates"), path, "candidates")
            reviewed = self.card_map([{"card": raw} for raw in receipt.get("reviewed_cards", [])] if isinstance(receipt.get("reviewed_cards"), list) else None, path, "reviewed_cards")
            if not candidates or set(candidates) != set(reviewed):
                self.fail("decision-coverage", path, "candidates must cover reviewed_cards exactly once")
            for idea_id, row in candidates.items():
                disposition = row.get("disposition")
                if disposition not in STATES:
                    self.fail("invalid-decision", path, f"{idea_id} has invalid disposition")
                self.require_keys(row, ["reason"], path, idea_id)
                if disposition != "select" and any(self.nonempty(row.get(field)) for field in ("target_route", "story_route", "accepted_risks", "posture", "assertions")):
                    self.fail("selection-leak", path, f"{idea_id} is not selected but carries selection authorization")
            dispositions = {row.get("disposition") for row in candidates.values() if isinstance(row.get("disposition"), str)}
            summary = "select" if "select" in dispositions else "defer" if "defer" in dispositions else "abandon" if dispositions == {"abandon"} else "open"
            if receipt.get("decision") != summary:
                self.fail("decision-drift", path, f"decision summary must be {summary}")
            manifest = self.load("ideation.yaml") or {}
            expected_state = {"select": "selected", "defer": "deferred", "abandon": "abandoned", "open": "open"}[summary]
            if manifest.get("stage") != "select" or manifest.get("state") != expected_state:
                self.fail("manifest-projection", path, "manifest stage/state must project this current selection summary")
        elif receipt.get("decision") not in {"select", "defer", "abandon"}:
            self.fail("invalid-decision", path, "legacy decision must be select, defer, or abandon")

        selected_raw = receipt.get("selected_cards", [])
        selected = self.card_map([{"card": raw} for raw in selected_raw] if isinstance(selected_raw, list) else None, path, "selected_cards")
        stories = self.card_map(receipt.get("story_routes", []), path, "story_routes")
        targets = self.card_map(receipt.get("target_routes", []), path, "target_routes")
        if set(stories) != set(selected) or set(targets) != set(selected):
            self.fail("route-card-drift", path, "selected cards, Story routes, and target routes must match by card identity")
        if version == 3:
            if {key for key, row in candidates.items() if row.get("disposition") == "select"} != set(selected):
                self.fail("decision-drift", path, "selected_cards must project the select dispositions")
            for idea_id, row in candidates.items():
                self.check_decision_projection(idea_id, row, receipt, path)
        if receipt.get("decision") != "select":
            if selected or stories or targets:
                self.fail("selection-leak", path, "non-select receipt must not carry selected cards/routes")
            if receipt.get("decision") == "open":
                self.fail("selection-open", path, "an all-open draft is not a completed human decision")
            return
        if not selected:
            self.fail("missing-selection", path, "decision select requires at least one selected card")
        self.check_test(selected_ids=set(selected))
        seen_stories = set()
        for idea_id in selected:
            row = candidates.get(idea_id, receipt)
            posture = row.get("posture") if version == 3 else row.get("selection_posture")
            risks = row.get("accepted_risks")
            if posture not in {"proceed", "proceed-with-caution"}:
                self.fail("invalid-posture", path, f"{idea_id} needs a valid selection posture")
            if not isinstance(risks, list) or any(not isinstance(risk, str) or not risk.strip() for risk in risks) or (posture == "proceed-with-caution" and not risks):
                self.fail("risk-missing", path, f"{idea_id} needs explicit accepted_risks for caution")
            assertions = row.get("assertions")
            if not isinstance(assertions, dict) or any(assertions.get(key) is not True for key in ASSERTIONS):
                self.fail("assertion-open", path, f"{idea_id} requires all five selection assertions")
            story, target = stories.get(idea_id, {}), targets.get(idea_id, {})
            self.require_keys(story, ["story_role", "story_path"], path, idea_id)
            self.require_keys(target, ["target", "category", "venue_contract"], path, idea_id)
            if version == 3:
                self.require_keys(target, ["contract_version", "venue_fit_card"], path, idea_id)
                for key, projection in (("story_route", story), ("target_route", target)):
                    expected = {k: v for k, v in projection.items() if k != "card"}
                    if row.get(key) != expected:
                        self.fail("route-projection", path, f"{idea_id} {key} differs from its compatibility projection")
            story_path = self.resolve_unit_path(story.get("story_path"))
            if story_path:
                key = str(story_path.resolve())
                if key in seen_stories:
                    self.fail("duplicate-route", path, "selected cards require distinct physical Story paths")
                seen_stories.add(key)
            self.check_venue_contract(target.get("venue_contract"), target.get("target"), target.get("category"), path, target.get("contract_version"))
            card_path, card = self.ideas[idea_id]
            venue = card.get("venue_fit", {})
            fit_raw = self.fit_path(venue)
            fit = self.load_linked(fit_raw, card_path, "Venue Fit Card")
            if fit:
                fit_candidates = fit[1].get("candidates", [])
                matches = [c for c in fit_candidates if isinstance(c, dict) and c.get("profile") == "deep-fit" and c.get("target") == target.get("target") and c.get("category") == target.get("category") and isinstance(c.get("venue_contract"), dict) and self.same_path(c["venue_contract"].get("path"), target.get("venue_contract"), fragment=True)] if isinstance(fit_candidates, list) else []
                if len(matches) != 1:
                    self.fail("target-drift", path, f"{idea_id} selected target must name one matching deep-fit candidate")
                if version == 3 and not self.same_path(target.get("venue_fit_card"), fit_raw):
                    self.fail("fit-drift", path, f"{idea_id} target route points to a different Venue Fit Card")
            self.selected_decisions[idea_id] = {"story": story, "target": target, "posture": posture, "accepted_risks": risks}
        if version == 3:
            self.check_sync()
            self.check_sync_binding(receipt.get("source"), path, require_projection=True)

    @staticmethod
    def fit_path(venue: dict) -> Any:
        raw = venue.get("card")
        return "cards/" + raw if isinstance(raw, str) and raw.startswith("venue-fit/") else raw

    def check_decision_projection(self, idea_id: str, row: dict, receipt: dict, path: Path) -> None:
        card_path, card = self.ideas[idea_id]
        disposition = row.get("disposition")
        if card.get("state", "open") != STATES.get(disposition):
            self.fail("decision-drift", card_path, "state differs from the current per-card disposition")
        if disposition == "open":
            return
        if not self.same_path(card.get("decision_ref"), receipt.get("snapshot")):
            self.fail("decision-drift", card_path, "decision_ref must identify this immutable selection")
        venue = card.get("venue_fit", {})
        if not isinstance(venue, dict):
            return
        if venue.get("human_target") != TARGET_STATES.get(disposition):
            self.fail("target-projection", card_path, "human_target differs from the per-card disposition")
        fit_raw = self.fit_path(venue)
        fit_path = self.resolve_unit_path(fit_raw)
        if disposition != "select" and (fit_path is None or not fit_path.exists()):
            return
        fit = self.load_linked(fit_raw, card_path, "Venue Fit Card")
        if fit is None:
            return
        target = row.get("target_route") if isinstance(row.get("target_route"), dict) else {}
        expected = {
            "status": TARGET_STATES.get(disposition), "selection_receipt": receipt.get("snapshot"),
            "target": target.get("target", ""), "category": target.get("category", ""),
            "venue_contract": target.get("venue_contract", ""), "contract_version": target.get("contract_version", ""),
            "by": receipt.get("by"), "at": receipt.get("at"),
            "accepted_conditions": row.get("accepted_risks", []),
        }
        if fit[1].get("human_target") != expected:
            self.fail("target-projection", fit[0], "human_target must project the exact selection fields")

    def check_sync_binding(self, source: Any, owner: Path, *, require_projection: bool = False) -> None:
        sync = self.load("projection/paper-ideation-sync.yaml")
        if not isinstance(source, dict) or sync is None:
            self.fail("sync-binding", owner, "source must pin the current sync revision/hash")
            return
        if sync.get("stage") != "I2" or sync.get("sync_status") != "current":
            self.fail("sync-stale", owner, "selection/handoff requires current I2 working sync")
        if require_projection:
            page = sync.get("paper_page", {})
            working = page.get("working", {}) if isinstance(page, dict) else {}
            if sync.get("version") != 2 or not isinstance(working, dict) or working.get("state") != "current":
                self.fail("sync-stale", owner, "v3 decisions require a v2 sync with a current working projection")
        for key in ("sync_revision", "source_hash"):
            if not self.nonempty(source.get(key)) or source.get(key) != sync.get(key):
                self.fail("sync-stale", owner, f"source.{key} differs from current sync")

    def check_handoff(self) -> None:
        self.check_select()
        self.check_sync()
        selection = self.selection
        path = self.root / "handoff/paper-ideation.yaml"
        handoff = self.load("handoff/paper-ideation.yaml")
        if not selection or selection.get("decision") != "select":
            self.fail("selection-open", path, "a ready handoff requires a human select decision")
        if handoff is None or selection is None:
            return
        if handoff.get("kind") != "paper-ideation-handoff" or handoff.get("status") != "ready" or handoff.get("paper_route") != "haipipe-paper-ideation":
            self.fail("handoff-open", path, "expected ready paper-ideation-handoff routed to haipipe-paper-ideation")
        if handoff.get("version", 2) not in {2, 3}:
            self.fail("unsupported-version", path, "handoff version must be 2 or 3")
        self.require_keys(handoff, ["created_at"], path)
        if handoff.get("version") == 3:
            self.check_snapshot(handoff, path, "handoff/history")
            if selection.get("version") != 3 or handoff.get("id") != selection.get("id"):
                self.fail("selection-drift", path, "handoff must pin the same v3 selection id")
        elif selection.get("version") == 3:
            self.fail("unsupported-version", path, "v3 selection requires v3 handoff")
        source = handoff.get("source")
        if not isinstance(source, dict):
            self.fail("invalid-shape", path, "source must be a mapping")
        else:
            for field, expected in (
                ("direction_card", "cards/direction.yaml"), ("evidence_bundle", "bundle/evidence-bundle.yaml"),
                ("paper_ideation_sync", "projection/paper-ideation-sync.yaml"),
                ("selection_receipt", selection.get("snapshot", "workflow/selection.yaml")),
            ):
                self.require_unit_path(source.get(field), path, field)
                if not self.same_path(source.get(field), expected):
                    self.fail("source-drift", path, f"source.{field} must identify {expected}")
            # Legacy receipts remain readable, but cannot authorize a new ready
            # handoff until the revision/hash actually consumed is supplied.
            self.check_sync_binding(source, path, require_projection=handoff.get("version") == 3)
        rows = self.card_map(handoff.get("selected_ideas"), path, "selected_ideas")
        if not rows or set(rows) != set(self.selected_decisions):
            self.fail("selection-drift", path, "handoff selected_ideas must equal the human-selected set")
        bundle = self.load("bundle/evidence-bundle.yaml") or {}
        lanes = bundle.get("sources", {})
        evidence_ids = {item.get("id") for name, lane in lanes.items() if name != "context" and isinstance(lane, list) for item in lane if isinstance(item, dict) and item.get("claim_support") is not False and isinstance(item.get("id"), str)} if isinstance(lanes, dict) else set()
        for idea_id, row in rows.items():
            decision = self.selected_decisions.get(idea_id)
            if decision is None:
                continue
            card_path, card = self.ideas[idea_id]
            for field in ("story_role", "story_path"):
                expected = decision["story"].get(field)
                matches = self.same_path(row.get(field), expected) if field == "story_path" else row.get(field) == expected
                if not matches:
                    self.fail("route-drift", path, f"{idea_id} {field} differs from human selection")
            for field, source_key in (("intended_target", "target"), ("intended_category", "category"), ("venue_contract", "venue_contract")):
                expected = decision["target"].get(source_key)
                matches = self.same_path(row.get(field), expected, fragment=True) if field == "venue_contract" else row.get(field) == expected
                if not matches:
                    self.fail("target-drift", path, f"{idea_id} {field} differs from human selection")
            if handoff.get("version") == 3:
                for field, expected in (("contract_version", decision["target"].get("contract_version")), ("selection_posture", decision["posture"]), ("accepted_risks", decision["accepted_risks"])):
                    if row.get(field) != expected:
                        self.fail("selection-drift", path, f"{idea_id} {field} differs from human selection")
            claims = card.get("core_claims", [])
            expected_claims = {c.get("id") for c in claims if isinstance(c, dict) and isinstance(c.get("id"), str)}
            actual_claims = row.get("claim_ids")
            if not isinstance(actual_claims, list) or any(not isinstance(c, str) for c in actual_claims) or set(actual_claims) != expected_claims or len(actual_claims) != len(expected_claims):
                self.fail("claim-drift", path, f"{idea_id} claim_ids must name all current Core Claims exactly once")
            actual_evidence = row.get("evidence_ids")
            required_evidence = {e for c in claims if isinstance(c, dict) for e in c.get("evidence", []) if isinstance(e, str)}
            if not isinstance(actual_evidence, list) or any(not isinstance(e, str) for e in actual_evidence) or not set(actual_evidence).issubset(evidence_ids) or not required_evidence.issubset(set(actual_evidence)) or len(actual_evidence) != len(set(actual_evidence)):
                self.fail("evidence-drift", path, f"{idea_id} evidence_ids must resolve and include its claim support")
            venue = card.get("venue_fit", {})
            if not self.same_path(row.get("venue_fit_card"), self.fit_path(venue)):
                self.fail("fit-drift", path, f"{idea_id} venue_fit_card differs from the card")
            feasibility = card.get("feasibility", {})
            expected = str(card_path) + "#feasibility.waiver" if feasibility.get("pilot") == "waived" else feasibility.get("receipt")
            if not self.same_path(row.get("feasibility_receipt_or_waiver"), expected, fragment=True):
                self.fail("feasibility-drift", path, f"{idea_id} feasibility source differs from the card")
            if not isinstance(row.get("hard_limits"), list):
                self.fail("invalid-shape", path, f"{idea_id} hard_limits must be an explicit list")
