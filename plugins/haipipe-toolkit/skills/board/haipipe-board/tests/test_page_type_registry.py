#!/usr/bin/env python3
"""The executable Page Type registry follows the cross-family resolver."""
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from cli.check import Report, check_page_type  # noqa: E402


class PageTypeRegistryTest(unittest.TestCase):
    def test_current_cross_family_types_resolve_by_declared_key(self):
        # `intervention` and `artifact` retired 260820 (renamed/absorbed into
        # `design`); the InsightBoard decomposed into meta + question + DIKW
        # levels 260820-21. `principle` retired as an independent key on
        # 260831; promoted principles are subordinate design-division roles.
        for value in (
            "seed",
            "venue",
            "narrative",
            "section",
            "round",
            "dash",
            "insight",
            "meta",
            "question",
            "data",
            "information",
            "knowledge",
            "wisdom",
            "brief",
            "design",
        ):
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

    def test_retired_principle_type_is_not_a_resolver_key(self):
        report = Report()
        check_page_type(
            Path("Q-principle.md"),
            "# Fixture\npage-type: principle\n\n## Opening\nQuestion?\n",
            "Q-principle.md",
            report,
        )
        self.assertTrue(
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
