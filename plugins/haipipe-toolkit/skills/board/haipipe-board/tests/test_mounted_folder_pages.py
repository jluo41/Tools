"""Task and Discovery Folder Pages mount directly on a Board.

The two fixtures deliberately share one basename.  A real BJTR tree repeats
``t01`` under many Jobs, so a Board that keys only on filenames cannot be the
Task or Discovery view of that tree.
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.common import page_files
from src.parse import parse_dir


BOARD = """# Mounted Folder Pages

spine: Show the Page Face already owned by each Task and Discovery Folder.
close: Both mounted kinds build as distinct Board pages.

## Topic
One Board renderer over two domain-owned Folder kinds.

## Pipeline
Folder Page to Board adapter to generated page.

## Pages
### BT · Tasks
This group lives beside board.md
tasks/b01_program/j01_job/t01_shared/t01_shared.md
### BD · Discoveries
discoveries/b01_program/j01_job/t01_shared/t01_shared.md
"""

TASK = """Legacy task page
================

This older Task Page predates folder-kind frontmatter but remains the readable
face of its Folder. The Board may project it without rewriting the source.

Address
-------
b01j01t01

Runs to land here
-----------------
Two tickets are planned and one Result has landed. Those facts remain owned by
the Task workflow rather than by the Board renderer.
"""

DISCOVERY = """---
folder-kind: discovery
address: b01.j01.t01
address_compact: b01j01t01
discovery_type: landscape-review
status: reported
---

# Discovery page

## Opening

Which sources establish the distinction this Discovery was opened to resolve?
The Board presents this Page Face and leaves source selection to Discovery.

## Content

### 1 · Question and boundary

The question is bounded to one comparison and its directly supporting sources.

### 2 · Evidence map

The completed Runs and Results remain in this Folder beside the Page.

## Aims

### A1 · Question and boundary

- ✅ A1.1 · The question has a stated boundary.
  **Done when:** the Page names what belongs here.
  **Now:** reported in the Page above.
"""


class MountedFolderPagesTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.board = Path(self._tmp.name)
        (self.board / "board.md").write_text(BOARD, encoding="utf-8")
        task = self.board / "tasks/b01_program/j01_job/t01_shared/t01_shared.md"
        discovery = self.board / "discoveries/b01_program/j01_job/t01_shared/t01_shared.md"
        task.parent.mkdir(parents=True)
        discovery.parent.mkdir(parents=True)
        task.write_text(TASK, encoding="utf-8")
        discovery.write_text(DISCOVERY, encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_same_basename_pages_are_discovered_and_ordered_by_path(self):
        found = [p.relative_to(self.board).as_posix() for p in page_files(self.board)]
        self.assertEqual(
            found,
            [
                "discoveries/b01_program/j01_job/t01_shared/t01_shared.md",
                "tasks/b01_program/j01_job/t01_shared/t01_shared.md",
            ],
        )
        meta, pages, warnings = parse_dir(self.board)
        self.assertEqual([p["kind"] for p in pages], ["task", "discovery"])
        self.assertEqual([p["id"] for p in pages], ["T-b01j01t01", "D-b01j01t01"])
        self.assertEqual([p["group"] for p in pages], ["BT · Tasks", "BD · Discoveries"])
        self.assertEqual(pages[0]["title"], "Legacy task page")
        self.assertEqual(pages[1]["state"], "✅ REPORTED")
        self.assertEqual(meta["groups"]["BT · Tasks"],
                         ["This group lives beside board.md"])
        self.assertEqual(warnings, [])

    def test_build_emits_distinct_task_and_discovery_pages(self):
        engine = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, str(engine / "cli/build.py"), str(self.board)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        task_html = self.board / "board/BT/T-b01j01t01.html"
        discovery_html = self.board / "board/BD/D-b01j01t01.html"
        self.assertTrue(task_html.is_file())
        self.assertTrue(discovery_html.is_file())
        self.assertIn('<span class="kind">TASK</span>', task_html.read_text(encoding="utf-8"))
        rendered = discovery_html.read_text(encoding="utf-8")
        self.assertIn('<span class="kind">DISCOVERY</span>', rendered)
        self.assertIn('data-folder-kind="discovery"', rendered)

    def test_checker_routes_mounted_pages_away_from_qs_contract(self):
        engine = Path(__file__).resolve().parent.parent
        subprocess.run(
            [sys.executable, str(engine / "cli/build.py"), str(self.board)],
            check=True,
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            [sys.executable, str(engine / "cli/check.py"), str(self.board),
             "--strict", "--no-template"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("no-state", result.stdout)
        self.assertNotIn("no-owner", result.stdout)
        self.assertNotIn("missing-section", result.stdout)


if __name__ == "__main__":
    unittest.main()
