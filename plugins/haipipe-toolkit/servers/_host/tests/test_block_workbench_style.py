"""A Block workbench names its kind first in its title. The CoWork and Discovery Block workbenches were retired to
servers/_old/ (their Blocks open on the shared focus page); the Task one remains."""
from __future__ import annotations

import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

SERVERS = Path(__file__).resolve().parents[2]


class BlockWorkbenchTitleTest(unittest.TestCase):
    """The page names its kind first (🧪 Task ·), then the Block title."""
    TITLES = {"workbench-work/task_views.py": "🧪 Task · "}

    def test_every_block_workbench_title_names_its_kind(self):
        for path, prefix in self.TITLES.items():
            text = (SERVERS / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn(f"<title>{prefix}{{e(snap['title'])}}</title>", text)
                self.assertIn(f"<h1>{prefix}{{e(snap['title'])}}</h1>", text)

    def test_home_shows_each_kind_with_its_emoji(self):
        from live.home import board_kind
        root = Path("/space")
        self.assertEqual(board_kind(root / "p/cowork/b11_x", root), ("CoWork Board", "📨"))
        self.assertEqual(board_kind(root / "p/discoveries/b01_x", root), ("Discovery Board", "🔭"))
        self.assertEqual(board_kind(root / "p/tasks/b01_x", root), ("Task Board", "🧪"))


if __name__ == "__main__":
    unittest.main()
