"""A right-click folds the Files pane to the element's folder and the code its Task owns; Task rows show their Run
over its rounds (element_info.py, focus_scope.py, focus_plan_results.py; JL 261126)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import element_info, focus_scope  # noqa: E402
from live.focus_plan_results import round_rows  # noqa: E402


class ShowFilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / "examples" / "P" / "work" / "b01_x"
        self.task = self.block / "j01_a" / "t01_files"
        self.task.mkdir(parents=True)
        (self.root / "plugins" / "k" / "servers" / "files").mkdir(parents=True)
        (self.task / "t01_files.md").write_text("# Files\n\n## Files\n\n`plugins/k/servers/files/` and more.\n\n## Checks\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_right_click_tells_the_pane_and_the_pane_folds(self):
        self.assertIn("wb:show-files", element_info.SCRIPT)
        self.assertIn("window.__scopeFocus=", focus_scope.SCRIPT)
        self.assertIn("else if(!way&&d.open)d.open=false", focus_scope.SCRIPT)     # all else closes

    def test_a_task_owns_the_folders_its_face_names(self):
        rel = self.task.relative_to(self.root).as_posix()
        self.assertEqual(focus_scope.owns(self.block, self.root), {rel: ["plugins/k/servers/files"]})
        self.assertIn(f'"{rel}": ["plugins/k/servers/files"]', focus_scope.assets(self.task, self.root))

    def test_a_task_shows_its_run_over_its_rounds(self):
        run = self.task / "runs" / "run-check-files"
        for name, head in (("p01-1125", "first round"), ("p02-1126", "second round")):
            (run / "passes" / name).mkdir(parents=True)
            (run / "passes" / name / "pass.md").write_text(f"# {head}\n\n## Summary\n\nDone.\n")
        (run / "run.yaml").write_text("run: run-check-files\nstatus: done\n")
        rows = round_rows(self.task)
        self.assertEqual([(r[4], r[1], r[2]) for r in rows],
                         [("run", "run-check-files", ""), ("round", "second round", "round 2 · 11-26"),
                          ("round", "first round", "round 1 · 11-25")])


if __name__ == "__main__":
    unittest.main()
