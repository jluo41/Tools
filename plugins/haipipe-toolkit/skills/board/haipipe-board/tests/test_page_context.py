#!/usr/bin/env python3
"""Related Board Pages grammar, validation, and bounded context tests."""
import tempfile
import unittest
from pathlib import Path
import subprocess
import sys

from src.page_context import (
    RelatedContextError,
    audit_related_rows,
    related_context_packet,
)

HERE = Path(__file__).resolve().parent.parent


BOARD = """# Context fixture
close: both pages remain structurally inspectable

## Pages
### Decisions
QA1-current.md
evidence/QB2-evidence.md
"""

TARGET = """# Evidence boundary
state: 🟡 PARTIAL
owner: CC

## Opening
Which evidence boundary matters?

The Page separates source selection from interpretation.

## Writing Style
Write direct claims.

## Content
### 1 · Background
Background that the current Page did not request.

### 2 · Evidence
Only this division should enter the scoped packet.

## Aims
### A2 · 📚 Evidence
- A2.1 · The evidence boundary is explicit.
  **Done when:** Included sources and exclusions are named.

## States
### A2 · 📚 Evidence
- ✅ A2.1 · Sources and exclusions are named.

## Files
### 🔗 Related Board Pages · what this Page reads by scope
- `reads · PROBE` · [QA1 §1](QA1-current.md)
  This cycle must never be traversed by a one-hop read.
"""


def current(row):
    return f"""# Current Page
state: 🟡 PARTIAL
owner: CC

## Opening
What should this Page establish?

It reads one bounded evidence fragment.

## Writing Style
Use plain English.

## Content
### 1 · Decision
The current Page owns the decision.

## Aims
### A1 · 🧭 Decision
- A1.1 · The decision is supported.
  **Done when:** The related evidence is inspected.

## States
### A1 · 🧭 Decision
- 🔨 A1.1 · Evidence is being inspected.

## Files
### 🔗 Related Board Pages · what this Page reads by scope
{row}
  Read the evidence boundary without loading the whole target Page.
"""


class RelatedBoardPageContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.board = Path(self.tmp.name)
        (self.board / "evidence").mkdir()
        (self.board / "board.md").write_text(BOARD, encoding="utf-8")
        self.source = self.board / "QA1-current.md"
        self.target = self.board / "evidence" / "QB2-evidence.md"
        self.target.write_text(TARGET, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def write_source(self, row):
        self.source.write_text(current(row), encoding="utf-8")

    def codes(self):
        return [finding.code for finding in audit_related_rows(self.source)]

    def test_probe_packet_reads_only_the_declared_closure_and_one_hop(self):
        self.write_source(
            "- `reads · PROBE` · [QB2 §2](evidence/QB2-evidence.md)"
        )
        packet = related_context_packet(self.source, "PROBE")
        self.assertIn("Which evidence boundary matters?", packet)
        self.assertIn("### 2 · Evidence", packet)
        self.assertIn("### A2 · 📚 Evidence", packet)
        self.assertIn("✅ A2.1", packet)
        self.assertNotIn("### 1 · Background", packet)
        self.assertNotIn("This cycle must never be traversed", packet)
        self.assertEqual([], self.codes())

    def test_phase_filter_accepts_all_and_ignores_other_phases(self):
        self.write_source(
            "- `reads · PROBE` · [QB2 §2](evidence/QB2-evidence.md)\n"
            "- `contrasts · ALL` · [QB2 §1](evidence/QB2-evidence.md)"
        )
        check_packet = related_context_packet(self.source, "CHECK")
        self.assertIn("### 1 · Background", check_packet)
        self.assertNotIn("### 2 · Evidence", check_packet)
        probe_packet = related_context_packet(self.source, "PROBE")
        self.assertIn("### 1 · Background", probe_packet)
        self.assertIn("### 2 · Evidence", probe_packet)
        self.assertEqual(1, probe_packet.count("Which evidence boundary matters?"))

    def test_dead_path_is_rejected(self):
        self.write_source("- `reads · PROBE` · [QB2 §2](evidence/missing.md)")
        self.assertIn("dead-related-page", self.codes())

    def test_wrong_page_id_is_rejected(self):
        self.write_source(
            "- `reads · PROBE` · [QB9 §2](evidence/QB2-evidence.md)"
        )
        self.assertIn("related-page-id", self.codes())

    def test_missing_scope_is_rejected(self):
        self.write_source(
            "- `reads · PROBE` · [QB2 §9](evidence/QB2-evidence.md)"
        )
        self.assertIn("dead-related-scope", self.codes())

    def test_path_cannot_climb_out_of_the_board(self):
        self.write_source("- `reads · PROBE` · [QB2 §2](../QB2-evidence.md)")
        self.assertIn("unsafe-related-path", self.codes())

    def test_malformed_row_is_rejected_before_context_is_read(self):
        self.write_source("- [QB2](evidence/QB2-evidence.md)")
        self.assertIn("related-row-form", self.codes())
        with self.assertRaises(RelatedContextError):
            related_context_packet(self.source, "PROBE")

    def test_duplicate_row_is_reported_and_emitted_once(self):
        row = "- `reads · PROBE` · [QB2 §2](evidence/QB2-evidence.md)"
        self.write_source(f"{row}\n{row}")
        self.assertIn("duplicate-related-row", self.codes())
        packet = related_context_packet(self.source, "PROBE")
        self.assertEqual(1, packet.count("## QB2 §2 · reads"))

    def test_board_checker_surfaces_related_page_faults(self):
        self.write_source("- `reads · PROBE` · [QB2 §2](evidence/missing.md)")
        result = subprocess.run(
            [sys.executable, str(HERE / "cli" / "check.py"), str(self.board)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertIn("dead-related-page", result.stdout)

    def test_fenced_grammar_example_is_not_a_live_reference(self):
        self.source.write_text(
            current("- `reads · PROBE` · [QB2 §2](evidence/QB2-evidence.md)")
            + "\n```markdown\n"
            + "### 🔗 Related Board Pages · example only\n"
            + "- `reads · PROBE` · [QB9 §9](missing.md)\n"
            + "```\n",
            encoding="utf-8",
        )
        self.assertEqual([], self.codes())


if __name__ == "__main__":
    unittest.main()
