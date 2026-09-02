from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "migrate_bjtr.py"
SPEC = importlib.util.spec_from_file_location("migrate_bjtr", SCRIPT)
assert SPEC and SPEC.loader
migrate_bjtr = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = migrate_bjtr
SPEC.loader.exec_module(migrate_bjtr)


class MigrateBjtrTest(unittest.TestCase):
    def make_legacy_bank(self, root: Path) -> Path:
        project = root / "project"
        task = (
            project
            / "discoveries"
            / "L01_clinical-evidence-map"
            / "01_retrieval-grounding-review"
        )
        task.mkdir(parents=True)
        (task / "notes.md").write_text("# Notes\n", encoding="utf-8")
        (task / "landscape.md").write_text("# Landscape\n", encoding="utf-8")
        (task / "discovery.yaml").write_text(
            """kind: discovery
id: L01.01
type: Review
role: landscape_review
group:
  id: L01
  slug: clinical-evidence-map
  title: Clinical evidence map
slug: retrieval-grounding-review
title: Retrieval grounding review
status: ok
created_at: "2026-08-01T00:00:00-04:00"
updated_at: "2026-08-02T00:00:00-04:00"

question: |
  Which retrieval designs ground clinical language model answers?
sources:
  local_first: true
build:
  needed: false
  artifact: ""
expected_outputs:
  - notes.md
  - landscape.md
report:
  outcome: mapped
""",
            encoding="utf-8",
        )
        (project / "README.md").write_text(
            "See discoveries/L01_clinical-evidence-map/"
            "01_retrieval-grounding-review and `01_retrieval-grounding-review`.\n",
            encoding="utf-8",
        )
        return project / "discoveries"

    def test_plan_exposes_all_bjt_segments(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            units = migrate_bjtr.plan_bank(bank)
            self.assertEqual(1, len(units))
            unit = units[0]
            self.assertEqual("b01_project_evidence_board", unit.block_name)
            self.assertEqual("j01_clinical_evidence_map_inquiry", unit.job_name)
            self.assertEqual("t01_retrieval_grounding_review", unit.task_name)
            self.assertEqual("b01.j01.t01", unit.address)

    def test_write_preserves_records_and_builds_canonical_task_page(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            units = migrate_bjtr.plan_bank(bank)
            blocks, changed_refs = migrate_bjtr.apply_bank(units)
            self.assertEqual(1, blocks)
            self.assertGreaterEqual(changed_refs, 1)
            task = units[0].new_path
            self.assertTrue((task / "notes.md").is_file())
            self.assertTrue((task / "landscape.md").is_file())
            self.assertTrue((task / "t01_retrieval_grounding_review.md").is_file())
            manifest = (task / "discovery.yaml").read_text(encoding="utf-8")
            self.assertIn("version: 6", manifest)
            self.assertIn("address: b01.j01.t01", manifest)
            self.assertIn("discovery_type: landscape-review", manifest)
            self.assertIn("typed_record: landscape.md", manifest)
            self.assertIn("instrument:", manifest)
            self.assertNotIn("expected_outputs:", manifest)
            self.assertNotIn("type: Review", manifest)
            self.assertIn("status: reported", manifest)
            page = (task / "t01_retrieval_grounding_review.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("state: 🟡 REPORTED", page)
            self.assertIn("folder-kind: discovery", page)
            self.assertIn("## Writing Style", page)
            self.assertIn("### 2 · Type payload", page)
            self.assertIn("### A2 · 📚 Type payload", page)
            self.assertIn("- 🔨 A2.1", page)
            self.assertIn("### 3 · Evidence map", page)
            self.assertIn("- ❄️ A3.1", page)
            readme = (bank.parent / "README.md").read_text(encoding="utf-8")
            self.assertIn(
                "discoveries/b01_project_evidence_board/"
                "j01_clinical_evidence_map_inquiry/"
                "t01_retrieval_grounding_review",
                readme,
            )
            self.assertNotIn("tt01_", readme)

    def test_legacy_groups_become_jobs_in_one_board(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            second = bank / "R02_safety-counterevidence" / "01_failure-modes"
            second.mkdir(parents=True)
            (bank / "R02_safety-counterevidence" / "_index.md").write_text(
                "# Safety group\n", encoding="utf-8"
            )
            (second / "discovery.yaml").write_text(
                """kind: discovery
type: Review
role: counterevidence
group:
  title: Safety counterevidence
title: Failure modes
status: planned
question: What failure modes remain?
""",
                encoding="utf-8",
            )
            units = migrate_bjtr.plan_bank(bank)
            self.assertEqual(2, len(units))
            self.assertEqual(1, len({unit.block_name for unit in units}))
            self.assertEqual(
                [
                    "j01_clinical_evidence_map_inquiry",
                    "j02_safety_counterevidence_inquiry",
                ],
                [unit.job_name for unit in units],
            )
            blocks, _ = migrate_bjtr.apply_bank(units)
            self.assertEqual(1, blocks)
            self.assertTrue(
                (
                    bank
                    / "b01_project_evidence_board"
                    / "j02_safety_counterevidence_inquiry"
                    / "_index.md"
                ).is_file()
            )

    def test_terminal_legacy_status_without_report_reopens_truthfully(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            legacy_manifest = next(bank.rglob("discovery.yaml"))
            source = legacy_manifest.read_text(encoding="utf-8")
            legacy_manifest.write_text(
                source.replace("report:\n  outcome: mapped\n", ""),
                encoding="utf-8",
            )
            units = migrate_bjtr.plan_bank(bank)
            migrate_bjtr.apply_bank(units)
            task = units[0].new_path
            manifest = (task / "discovery.yaml").read_text(encoding="utf-8")
            page = (task / "t01_retrieval_grounding_review.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("status: executing", manifest)
            self.assertNotIn("\nreport:", manifest)
            self.assertIn("state: 🟡 ACTIVE", page)
            self.assertIn("- ✅ A1.1", page)
            self.assertIn("- 🔨 A2.1", page)

    def test_repair_refreshes_only_migration_page_and_preserves_heading(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            units = migrate_bjtr.plan_bank(bank)
            migrate_bjtr.apply_bank(units)
            task = units[0].new_path
            page = task / "t01_retrieval_grounding_review.md"
            page.write_text(
                page.read_text(encoding="utf-8").replace(
                    "# Retrieval grounding review", "# Human-edited concise title"
                ),
                encoding="utf-8",
            )
            found, changed = migrate_bjtr.repair_canonical_pages(bank, True)
            self.assertEqual((1, 1), (found, changed))
            repaired = page.read_text(encoding="utf-8")
            self.assertTrue(repaired.startswith("# Human-edited concise title\n"))
            self.assertIn("## Writing Style", repaired)
            self.assertIn("### 4 · Limits and next move", repaired)

    def test_repair_does_not_overwrite_authored_page(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_legacy_bank(Path(temp))
            units = migrate_bjtr.plan_bank(bank)
            migrate_bjtr.apply_bank(units)
            page = units[0].new_path / "t01_retrieval_grounding_review.md"
            authored = page.read_text(encoding="utf-8").replace(
                migrate_bjtr.MIGRATION_METHOD,
                "method: Human-authored evidence synthesis.",
            )
            page.write_text(authored, encoding="utf-8")
            found, changed = migrate_bjtr.repair_canonical_pages(bank, True)
            self.assertEqual((0, 0), (found, changed))
            self.assertEqual(authored, page.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
