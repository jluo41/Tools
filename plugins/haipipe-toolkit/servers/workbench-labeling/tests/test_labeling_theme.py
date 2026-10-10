"""The labeling theme on the base frame (labeling_theme.py): status and links only, read only.

A placeholder Project with one labeling Block (schema.yaml, one Job, one labeling Task Page with no
labeling/ lane yet): the Block's Description and Work Details, the Task's views, each linking to the
Labeling workbench at that view; without the labeling package the theme falls back to vanilla."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import frame  # noqa: E402
from live import labeling_theme as T  # noqa: E402


def project(tmp: str) -> tuple[Path, Path, Path]:
    root = Path(tmp)
    block = root / "Project-X" / "labeling" / "b61_demo_label"
    task = block / "j01_building_demo" / "t01_demo_labeling"
    task.mkdir(parents=True)
    (block / "board.md").write_text("# /demo-label: How <placeholder> is it?\n\nboard-kind: task-block\n"
                                    "spine: one placeholder schema\n")
    (block / "schema.yaml").write_text("schema: S_00\nlabels: [high, low, none]\n")
    (task / "t01_demo_labeling.md").write_text("# Demo labeling\nstate: 🔴 OPEN\ntask-type: labeling\n"
                                              "page-type: labeling\n\n## Opening\n\nA placeholder job.\n")
    return root, block, task


def spaces(theme, root, folder, sub=""):
    data = json.loads(frame.frame_json(theme, root, folder, sub))
    return {s["name"]: s for s in data["spaces"]}


class LabelingThemeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root, self.block, self.task = project(self.tmp.name)
        self.theme = frame.themes()["labeling"]

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_labeling_block_reads_by_its_theme_folder(self):
        self.assertEqual(frame.theme_of(self.task, self.root), "labeling")

    def test_the_block_shows_its_schema_and_its_jobs_status(self):
        s = spaces(self.theme, self.root, self.block)
        self.assertEqual(s["Description"]["subspaces"], ["Scope", "Schema"])
        self.assertEqual(s["Work Details"]["subspaces"], ["Jobs", "Labeling"])
        self.assertIn("Prepare a corpus", s["Work Details"]["run_doing"])
        page = frame.render(self.theme, self.root, self.block, "Description", "Schema")
        self.assertIn("labels: [high, low, none]", page)
        page = frame.render(self.theme, self.root, self.block, "Work Details", "Labeling")
        # labeling/ is the Theme's name (s01-D29), so the row is the Job, b61j01, as under labelings/
        self.assertIn("b61j01", page)
        self.assertIn("/_board/labeling?path=", page)

    def test_a_job_page_opens_each_view_in_the_labeling_workbench(self):
        s = spaces(self.theme, self.root, self.task)
        work = [v[2] for v in T.WORK]
        self.assertEqual(s["Work Details"]["subspaces"][:len(work)], work)
        self.assertEqual(s["Description"]["subspaces"][:2], ["Scope", "Contract"])
        self.assertEqual(s["Delivery"]["subspaces"][:4], ["Files", "Handoff", "Scan", "Final labels"])
        for sub, space, view in (("Rounds", "Work Details", "space=labeling&amp;view=rounds"),
                                 ("Audit", "Work Details", "space=quality&amp;view=audit"),
                                 ("Handoff", "Delivery", "space=delivery&amp;view=handoff"),
                                 ("Contract", "Description", "space=data&amp;view=contract")):
            with self.subTest(sub=sub):
                page = frame.render(self.theme, self.root, self.task, space, sub)
                self.assertIn(view, page)
                self.assertEqual(spaces(self.theme, self.root, self.task, sub)[space]["run_doing"], [sub])

    def test_it_writes_nothing_and_shows_no_items(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        for sub in [v[2] for v in T.VIEWS] + ["Scope", "Files"]:
            frame.render(self.theme, self.root, self.task, "Work Details", sub)
        self.assertEqual(sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*")), before)

    def test_without_the_labeling_package_it_is_vanilla(self):
        saved, T.L = T.L, None
        try:
            self.assertEqual(T.spaces("Block", self.block, self.root, ""), {})
            self.assertEqual(T.spaces("Task", self.task, self.root, ""), {})
        finally:
            T.L = saved

    def test_a_task_that_is_no_labeling_job_is_vanilla(self):
        other = self.block / "j01_building_demo" / "t02_notes"
        other.mkdir()
        (other / "t02_notes.md").write_text("# Notes\n")
        self.assertEqual(T.spaces("Task", other, self.root, ""), {})


if __name__ == "__main__":
    unittest.main()
