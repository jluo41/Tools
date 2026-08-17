#!/usr/bin/env python3
"""The executable Page Type registry follows the cross-family resolver."""
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from cli.check import Report, check_page_type  # noqa: E402


class PageTypeRegistryTest(unittest.TestCase):
    def test_new_task_and_application_types_resolve_by_declared_key(self):
        for value in ("venue", "insight", "brief", "intervention", "artifact"):
            with self.subTest(value=value):
                report = Report()
                check_page_type(
                    Path(f"Q-{value}.md"),
                    f"# Fixture\npage-type: {value}\n\n## Opening\nQuestion?\n",
                    f"Q-{value}.md",
                    report,
                )
                self.assertFalse(
                    [row for row in report.rows if row[1] == "page-type-unknown"]
                )

    def test_unknown_type_still_warns(self):
        report = Report()
        check_page_type(
            Path("Q-unknown.md"),
            "# Fixture\npage-type: not-a-real-type\n\n## Opening\nQuestion?\n",
            "Q-unknown.md",
            report,
        )
        self.assertEqual(1, len([r for r in report.rows if r[1] == "page-type-unknown"]))


if __name__ == "__main__":
    unittest.main()
