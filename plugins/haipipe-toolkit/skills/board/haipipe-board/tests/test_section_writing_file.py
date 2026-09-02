#!/usr/bin/env python3
"""Manuscript Section writing rules live in the outline process folder."""
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from cli.check import Report, check_section_writing_requirements
from cli.requirement import _writing_records


PAGE = """# Results fixture
state: 🟡 PARTIAL
owner: JL
page-type: section
section_kind: results

## Opening
What did the analysis show?

## Content
### 1 · Result
The accepted result belongs here.
"""

WRITING = """# S-Desk-Main-Results · requirement
page: S-Desk-Main-Results
kind: requirement · generated venue + authored page writing

# --- requirement:begin (generated) ---
REQUIREMENT, MEASURED 260902 1200. GENERATED; do not hand-edit.
# --- requirement:end ---

# --- writing:begin (authored) ---

### W1 · Keep estimates and intervals together
- **Rule**: Report each estimate with its 95% confidence interval.
- **Applies**: Results sentences.
- **Source**: Section reporting contract.
# --- writing:end ---
"""


class SectionWritingFileTest(unittest.TestCase):
    def _fixture(self, directory):
        folder = Path(directory) / "S-Desk-Main-Results"
        folder.mkdir()
        page = folder / "S-Desk-Main-Results.md"
        page.write_text(PAGE, encoding="utf-8")
        return page

    def test_valid_outline_writing_record_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._fixture(directory)
            outline = page.parent / "outline"
            outline.mkdir()
            (outline / "S-Desk-Main-Results-requirement.md").write_text(
                WRITING, encoding="utf-8"
            )
            report = Report()
            check_section_writing_requirements(PAGE, page, page.name, report)

        self.assertEqual([], report.rows)

    def test_legacy_page_block_is_named(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._fixture(directory)
            legacy = PAGE.replace(
                "\n## Content", "\n### Writing Style\nKeep estimates together.\n\n## Content"
            )
            report = Report()
            check_section_writing_requirements(legacy, page, page.name, report)

        codes = [row[1] for row in report.rows]
        self.assertIn("section-writing-in-page", codes)

    def test_requirement_refresh_preserves_authored_w_records(self):
        self.assertIn(
            "### W1 · Keep estimates and intervals together",
            _writing_records(WRITING),
        )

    def test_retired_sidecar_can_be_imported_once(self):
        sidecar = """# fixture · writing
page: fixture
kind: writing · authored

### W2 · Use association language
- **Rule**: Use associated with rather than caused.
- **Applies**: Results prose.
- **Source**: Study design boundary.
"""
        self.assertTrue(_writing_records("", sidecar).startswith("### W2 ·"))


if __name__ == "__main__":
    unittest.main()
