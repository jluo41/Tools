"""An old link to a renamed folder still opens (JL 261012: "I cannot open you anymore"): the folder's face keeps
`renamed-from:`, and frame_view.renamed() finds the new path, part by part."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live.frame_view import renamed  # noqa: E402


def _face(folder: Path, front: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{folder.name}.md").write_text(f"---\n{front}\n---\n\n# {folder.name}\n", encoding="utf-8")


class RenamedLinkTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        board = self.root / "Project-Demo" / "insight" / "Insight-Demo"
        board.mkdir(parents=True)
        (board / "board.md").write_text("---\nboard-kind: insight-board\n---\n", encoding="utf-8")
        self.job = board / "j01_prototype-p1-basic-questions_data-Demov1"
        _face(self.job, "release: p1\nrenamed-from: j01_p1_Demov1")
        _face(self.job / "t01_D01_extract-shape", "question: D01")
        _face(board / "j02_prototype-p1-basic-questions_data-Demov2", "renamed-from: [j02_p1_Demov2, j02_old]")

    def tearDown(self):
        self.tmp.cleanup()

    def test_an_old_job_link_finds_the_new_folder(self):
        self.assertEqual(renamed(self.root, "Project-Demo/insight/Insight-Demo/j01_p1_Demov1"),
                         "Project-Demo/insight/Insight-Demo/j01_prototype-p1-basic-questions_data-Demov1")

    def test_a_task_under_the_old_job_name_opens_too(self):
        self.assertEqual(renamed(self.root, "/Project-Demo/insight/Insight-Demo/j01_p1_Demov1/t01_D01_extract-shape"),
                         "Project-Demo/insight/Insight-Demo/j01_prototype-p1-basic-questions_data-Demov1/"
                         "t01_D01_extract-shape")

    def test_a_list_of_old_names_and_an_unknown_name(self):
        self.assertTrue(renamed(self.root, "Project-Demo/insight/Insight-Demo/j02_old").endswith("_data-Demov2"))
        self.assertEqual(renamed(self.root, "Project-Demo/insight/Insight-Demo/j99_never"), "")


if __name__ == "__main__":
    unittest.main()
