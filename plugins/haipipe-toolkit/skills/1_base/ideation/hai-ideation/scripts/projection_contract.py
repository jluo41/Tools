"""Paper working/release/delivery projections for the Ideation gate checker."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from idea_layout import is_idea_job

IDEA_ID = re.compile(r"^i\d+$")
PROJECTION_CHANGE_CLASSES = {"state", "portfolio", "structure"}
PAGE_STATES = {"missing", "bound", "blocked"}
WORKING_SURFACE_STATES = {"not-requested", "current", "stale", "blocked"}
RELEASE_SURFACE_STATES = {"not-requested", "current", "stale", "blocked"}


class ProjectionChecks:
    def check_projection_surfaces(self, sync: dict[str, Any], path: Path) -> None:
        """Validate the v2 semantic-to-Page projection state machine.

        Version 1 remains readable because existing units only have the legacy
        ``last_projected_revision`` pointer. Version 2 is strict: a current
        surface needs a Page-owned receipt and cannot outrun the semantic
        source or its upstream surface.
        """

        version = sync.get("version")
        page = sync.get("paper_page")
        if version == 1:
            if not isinstance(page, dict):
                self.fail("invalid-shape", path, "paper_page must be a mapping")
            return
        if version != 2:
            self.fail("unsupported-version", path, "paper-ideation-sync version must be 1 or 2")
            return

        # A semantic source is identified by sync_revision alone. No content
        # hash is written or compared (JL 260928); a leftover source_hash in an
        # old packet is ignored.
        self.require_keys(sync, ["projection"], path)

        projection = sync.get("projection")
        if not isinstance(projection, dict):
            self.fail("invalid-shape", path, "projection must be a mapping")
        else:
            self.require_present(projection, ["change_class", "affected_idea_ids", "identity_key"], path, "projection")
            if projection.get("change_class") not in PROJECTION_CHANGE_CLASSES:
                self.fail("invalid-change-class", path, "projection.change_class is invalid")
            if projection.get("identity_key") != "idea_id":
                self.fail("unstable-identity", path, "projection.identity_key must be idea_id")
            affected = projection.get("affected_idea_ids")
            if not isinstance(affected, list):
                self.fail("invalid-shape", path, "projection.affected_idea_ids must be a list")
            else:
                for idea_id in affected:
                    if not isinstance(idea_id, str) or not IDEA_ID.fullmatch(idea_id):
                        self.fail("invalid-id", path, "projection.affected_idea_ids must contain iNN ids")
                    elif idea_id not in self.ideas:
                        self.fail("unknown-idea", path, f"projection names unknown Idea {idea_id}")

        if not isinstance(page, dict):
            self.fail("invalid-shape", path, "paper_page must be a mapping")
            return
        self.require_present(page, ["state", "path", "working", "release", "delivery"], path, "paper_page")
        page_state = page.get("state")
        if page_state not in PAGE_STATES:
            self.fail("invalid-state", path, "paper_page.state must be missing, bound, or blocked")
        if page_state == "missing" and self.nonempty(page.get("path")):
            self.fail("binding-drift", path, "missing Page binding must have paper_page.path null")
        if page_state in {"bound", "blocked"} and not self.nonempty(page.get("path")):
            self.fail("missing-path", path, "bound or blocked Page binding requires paper_page.path")

        revision = sync.get("sync_revision")
        valid_revision = isinstance(revision, int) and not isinstance(revision, bool) and revision >= 1
        surfaces: dict[str, dict[str, Any] | None] = {}
        for name, allowed_states in (
            ("working", WORKING_SURFACE_STATES),
            ("release", RELEASE_SURFACE_STATES),
            ("delivery", RELEASE_SURFACE_STATES),
        ):
            surface = page.get(name)
            surfaces[name] = surface if isinstance(surface, dict) else None
            if not isinstance(surface, dict):
                self.fail("invalid-shape", path, f"paper_page.{name} must be a mapping")
                continue
            self.require_present(surface, ["state", "revision", "receipt"], path, f"paper_page.{name}")
            state = surface.get("state")
            if state not in allowed_states:
                self.fail("invalid-state", path, f"paper_page.{name}.state is invalid")
            surface_revision = surface.get("revision")
            if surface_revision is not None:
                if not isinstance(surface_revision, int) or isinstance(surface_revision, bool) or surface_revision < 1:
                    self.fail("invalid-revision", path, f"paper_page.{name}.revision must be a positive integer or null")
                elif valid_revision and surface_revision > revision:
                    self.fail("revision-ahead", path, f"paper_page.{name}.revision cannot exceed sync_revision")
            if self.nonempty(surface.get("receipt")):
                self.require_unit_path(surface.get("receipt"), path, f"paper_page.{name} receipt")
                if surface_revision is not None:
                    self.check_projection_receipt(
                        surface.get("receipt"),
                        name,
                        surface_revision,
                        page.get("path"),
                        path,
                    )
            if state == "current":
                page_path = self.resolve_unit_path(page.get("path"))
                if page_path is None or not page_path.is_file():
                    self.fail("broken-path", path, "a current projection requires its physical Paper Page")
                if not valid_revision or surface_revision != revision:
                    self.fail("projection-stale", path, f"paper_page.{name}.current must equal sync_revision")
                if not self.nonempty(surface.get("receipt")):
                    self.fail("receipt-missing", path, f"paper_page.{name}.current requires a Page-owned receipt")
            elif state == "not-requested":
                if any(self.nonempty(surface.get(field)) for field in ("revision", "receipt")):
                    self.fail("surface-drift", path, f"paper_page.{name}.not-requested must have null revision/receipt")
            elif state == "stale" and valid_revision:
                if surface_revision == revision:
                    self.fail("surface-drift", path, f"paper_page.{name}.stale cannot match the current semantic source")

        working = surfaces["working"]
        release = surfaces["release"]
        delivery = surfaces["delivery"]
        if isinstance(release, dict) and release.get("state") == "current":
            if not isinstance(working, dict) or working.get("state") != "current":
                self.fail("release-ahead", path, "current release requires current working projection")
            elif release.get("revision") != working.get("revision"):
                self.fail("release-drift", path, "current release must consume the current working source")
        if isinstance(delivery, dict) and delivery.get("state") == "current":
            if not isinstance(release, dict) or release.get("state") != "current":
                self.fail("delivery-ahead", path, "current delivery requires current release")
            elif delivery.get("revision") != release.get("revision"):
                self.fail("delivery-drift", path, "current delivery must identify the current released source")
        if page_state == "missing" and any(
            isinstance(surface, dict) and surface.get("state") == "current"
            for surface in surfaces.values()
        ):
            self.fail("binding-drift", path, "an unbound Page cannot have a current projection surface")

        expected_sync_status = "blocked" if page_state == "blocked" or (isinstance(working, dict) and working.get("state") == "blocked") else "current" if isinstance(working, dict) and working.get("state") == "current" else "stale"
        if sync.get("sync_status") != expected_sync_status:
            self.fail("sync-status-drift", path, f"sync_status should be {expected_sync_status}")

    def check_projection_receipt(
        self,
        raw: Any,
        surface_name: str,
        revision: Any,
        page_path: Any,
        owner: Path,
    ) -> None:
        linked = self.load_linked(raw, owner, f"paper_page.{surface_name}.receipt")
        if linked is None:
            return
        receipt_path, receipt = linked
        projection = receipt.get("paper_projection")
        if not isinstance(projection, dict):
            self.fail("missing-projection", receipt_path, "Page dispatch receipt needs a paper_projection extension")
            return
        self.require_keys(
            receipt,
            ["phase", "status"],
            receipt_path,
        )
        self.require_keys(
            projection,
            [
                "source_packet",
                "source_revision",
                "page_path",
                "surface",
                "created_at",
            ],
            receipt_path,
            "paper_projection",
        )
        if receipt.get("status") != "ok":
            self.fail("receipt-not-ok", receipt_path, "current or retained projection receipt must have status ok")
        if projection.get("source_packet") != "projection/paper-ideation-sync.yaml":
            self.fail("receipt-drift", receipt_path, "paper_projection must name the canonical sync packet")
        if projection.get("source_revision") != revision:
            self.fail("receipt-drift", receipt_path, "paper_projection source_revision must match the surface revision")
        if projection.get("page_path") != page_path:
            self.fail("receipt-drift", receipt_path, "paper_projection page_path must match paper_page.path")
        if projection.get("surface") != surface_name:
            self.fail("receipt-drift", receipt_path, f"paper_projection surface must be {surface_name}")
        expected_phases = {
            "working": {"OUTLINE"},
            "release": {"CONTENT"},
            "delivery": {"CONTENT"},
        }
        if receipt.get("phase") not in expected_phases[surface_name]:
            self.fail("invalid-phase", receipt_path, f"{surface_name} projection must use the Page {surface_name} phase")

    def check_sync(self) -> None:
        self.check_generate()
        sync = self.load("projection/paper-ideation-sync.yaml")
        if sync is None:
            return
        path = self.root / "projection/paper-ideation-sync.yaml"
        if sync.get("kind") != "paper-ideation-sync":
            self.fail("wrong-kind", path, "kind must be paper-ideation-sync")
        self.require_keys(
            sync,
            [
                "version",
                "source",
                "stage",
                "sync_revision",
                "paper_page",
                "discovery_landscape",
                "ideas",
                "portfolio_recommendation",
                "selection_authority",
                "sync_status",
                "updated_at",
            ],
            path,
        )
        self.require_present(sync, ["opportunity_map"], path)
        if sync.get("opportunity_map") == []:
            if not is_idea_job(self.root):
                self.require_keys(sync, ["opportunity_map"], path)
            elif not isinstance(sync.get("open_gaps"), list) or not sync["open_gaps"]:
                self.fail("evidence-gap-missing", path, "an empty opportunity map must name its open evidence gaps")
        if sync.get("stage") not in {"I1", "I2"}:
            self.fail("invalid-stage", path, "sync stage must be I1 or I2")
        revision = sync.get("sync_revision")
        if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
            self.fail("invalid-revision", path, "sync_revision must be a positive integer")
        self.check_projection_surfaces(sync, path)
        source = sync.get("source")
        if isinstance(source, dict):
            for field in ("ideation_manifest", "evidence_bundle", "direction_card"):
                self.require_unit_path(source.get(field), path, f"source.{field}")
            if sync.get("stage") == "I2":
                self.require_unit_path(source.get("test_matrix"), path, "source.test_matrix")
        else:
            self.fail("invalid-shape", path, "source must be a mapping")
        if not isinstance(sync.get("discovery_landscape"), dict):
            self.fail("invalid-shape", path, "discovery_landscape must be a mapping")
        if not isinstance(sync.get("opportunity_map"), list):
            self.fail("invalid-shape", path, "opportunity_map must be a list")
        projected = sync.get("ideas")
        projected_cards: set[str] = set()
        if not isinstance(projected, list):
            self.fail("invalid-shape", path, "ideas must be a list")
        else:
            for item in projected:
                if not isinstance(item, dict):
                    self.fail("invalid-row", path, "every projected Idea must be a mapping")
                    continue
                self.require_keys(item, ["card", "state", "novelty", "identification", "feasibility", "journal_fit", "next_route"], path, "ideas[]")
                card = item.get("card")
                if isinstance(card, str):
                    if card in projected_cards:
                        self.fail("duplicate-card", path, "sync repeats an Idea Card")
                    projected_cards.add(card)
                    self.require_unit_path(card, path, "projected Idea card")
                    idea_id = self.card_identity(card, path)
                    if idea_id is not None:
                        source_card = self.ideas[idea_id][1]
                        if item.get("state") != source_card.get("state", "open"):
                            self.fail("decision-drift", path, f"sync state differs from {idea_id}")
                        if item.get("state") != "open" and not self.same_path(item.get("decision_ref"), source_card.get("decision_ref")):
                            self.fail("decision-drift", path, f"sync disposition for {idea_id} lacks its decision_ref")
            actual_cards = {str(card_path.relative_to(self.root)) for card_path, _ in self.ideas.values()}
            if projected_cards != actual_cards:
                self.fail("portfolio-drift", path, "sync ideas must name every admitted Idea Card exactly once")
        authority = sync.get("selection_authority")
        if not isinstance(authority, dict) or authority.get("status") != "none" or authority.get("receipt") is not None:
            self.fail("selection-leak", path, "I1/I2 sync must keep selection_authority status none and receipt null")
        forbidden = {"decision", "selected_cards", "target_routes", "story_routes", "selected_ideas"}
        leaked = sorted(forbidden.intersection(sync))
        if leaked:
            self.fail("selection-leak", path, f"working sync contains selection fields: {', '.join(leaked)}")

