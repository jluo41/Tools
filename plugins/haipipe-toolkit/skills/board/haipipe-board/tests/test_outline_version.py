import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.outline_version import (  # noqa: E402
    latest_outline,
    legacy_integer_issue,
    version_key,
    version_policy_issues,
    version_tag,
)


class OutlineVersionTest(unittest.TestCase):
    def test_numeric_major_and_revision_order(self):
        names = [
            "Q1-outline-v5.0.md",
            "Q1-outline-v5.2.md",
            "Q1-outline-v5.10.md",
            "Q1-outline-v6.0.md",
        ]
        ordered = sorted((Path(name) for name in names), key=version_key)
        self.assertEqual(
            [path.name for path in ordered],
            [
                "Q1-outline-v5.0.md",
                "Q1-outline-v5.2.md",
                "Q1-outline-v5.10.md",
                "Q1-outline-v6.0.md",
            ],
        )

    def test_initial_revisions_promote_to_v1_point_0(self):
        names = ["Q1-outline-v0.5.md", "Q1-outline-v0.6.md", "Q1-outline-v1.0.md"]
        ordered = sorted((Path(name) for name in names), key=version_key)
        self.assertEqual([path.name for path in ordered], names)

    def test_latest_plan_is_scoped_to_page_stem(self):
        with tempfile.TemporaryDirectory() as tmp:
            outline = Path(tmp)
            for name in (
                "Q1-outline-v5.0.md",
                "Q1-outline-v5.1.md",
                "Q2-outline-v9.md",
            ):
                (outline / name).write_text(name, encoding="utf-8")
            latest = latest_outline(outline, "Q1")
            self.assertIsNotNone(latest)
            self.assertEqual(latest.name, "Q1-outline-v5.1.md")
            self.assertEqual(version_tag(latest), "v5.1")

    def test_version_policy_requires_approval_only_on_integer_major(self):
        cases = (
            ("Q1-outline-v0.6.md", "approved: ⬜\n", []),
            ("Q1-outline-v1.0.md", "approved: ✅ JL · in channel\n", []),
            (
                "Q1-outline-v1.0.md",
                "approved: ⬜\n",
                ["v1.0: a frozen .0 baseline requires explicit channel approval"],
            ),
            (
                "Q1-outline-v0.6.md",
                "approved: ✅\n",
                ["v0.6: a pre-approval revision cannot be approved; promote it to v1.0"],
            ),
            (
                "Q1-outline-v1.2.md",
                "approved: ✅\n",
                ["v1.2: a working minor cannot be approved; promote it to v2.0"],
            ),
        )
        for name, text, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(version_policy_issues(Path(name), text), expected)


if __name__ == "__main__":
    unittest.main()

    def test_integer_only_latest_plan_is_legacy_input(self):
        self.assertEqual(
            legacy_integer_issue(Path("Q1-outline-v5.md")),
            "v5: integer-only plan version is legacy; renumber the chain "
            "v1…v5 to v0.1…v0.5 (no v1.0 until a person promotes one)",
        )
        self.assertEqual(legacy_integer_issue(Path("Q1-outline-v0.5.md")), "")
        self.assertEqual(legacy_integer_issue(Path("Q1-outline-v1.0.md")), "")


if __name__ == "__main__":
    unittest.main()
