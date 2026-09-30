"""Direct static URLs must not bypass source and Labeling custody."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()
from host_registry import static_path_allowed  # noqa: E402


class PrivateStaticPathsTest(unittest.TestCase):
    def test_denies_private_source_and_labeling_files_but_keeps_board_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            private = root / "source" / "corpus-preparation" / "versions" / "source-1"
            private.mkdir(parents=True)
            (root / "board-one" / "board.md").parent.mkdir(parents=True)
            (root / "board-one" / "board.md").write_text("# Board\n", encoding="utf-8")
            data = private / "normalized.private.jsonl"
            data.write_text('PRIVATE_TARGET\n', encoding="utf-8")
            alias = root / "public-link.txt"
            alias.symlink_to(data)
            outside = root.parent / "outside-sensitive.txt"
            outside_alias = root / "outside-link.txt"
            outside_alias.symlink_to(outside)
            denied = [
                root / "source" / "transcripts.jsonl",
                root / "source" / "transcripts.jsonl.gz",
                data, alias, outside_alias,
                root / "board-one" / "S-Label-1" / "labeling" / "preparation-owner.yaml",
                root / "board-one" / "S-Label-1" / "labeling" / "corpus" / "items.jsonl",
                root / "source" / "board" / "labeling" / "private.html",
                root / ".server_config" / "settings.env",
            ]
            for path in denied:
                self.assertFalse(static_path_allowed(root, path), path)
            allowed = [
                root / "board-one" / "board" / "Labeling" / "S-Label-1.html",
                root / "board-one" / "board" / "index.html",
                root / "board-one" / "S-Label-1.md",
                root / "board-one" / "board" / "_assets" / "app.js",
            ]
            for path in allowed:
                self.assertTrue(static_path_allowed(root, path), path)


if __name__ == "__main__":
    unittest.main()
