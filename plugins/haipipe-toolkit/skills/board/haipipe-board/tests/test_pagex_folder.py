import tempfile
import unittest
from pathlib import Path

from live.pagex import PagexMixin, _folder_markers, _is_addressable_folder


class _PagexHarness(PagexMixin):
    def __init__(self, root, state):
        self.root = root
        self.state = state

    def _url_of(self, path):
        try:
            return "/" + Path(path).relative_to(self.root).as_posix()
        except ValueError:
            return None

    def _pagex_state(self, _payload):
        return self.state, None


class PagexFolderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tmp_root = Path(self.tmp.name)
        self.root = self.tmp_root / "repo"
        self.root.mkdir()
        self.consumer = self.root / "board" / "Q1"
        self.consumer.mkdir(parents=True)
        self.page = self.consumer / "Q1.md"
        self.page.write_text("# Q1\nstate: 🟡 active\n", encoding="utf-8")
        self.base = self.consumer / "evidence" / "pagex"
        self.base.mkdir(parents=True)
        self.store = self.base / "Q1.md"
        self.state = {
            "page": self.page,
            "dir": self.base,
            "stem": "Q1",
            "store": self.store,
            "rows": {},
            "order": [],
            "board": self.root / "board",
            "ctx": {"path": "board", "file": "Q1.md"},
        }
        self.fake = _PagexHarness(self.root, self.state)

    def tearDown(self):
        self.tmp.cleanup()

    def task_folder(self):
        folder = self.root / "project" / "tasks" / "A01"
        (folder / "workflow").mkdir(parents=True)
        (folder / "workflow" / "plan.yaml").write_text(
            "task: test\n", encoding="utf-8")
        return folder

    def mint_one(self, path):
        self.state["rows"] = {
            path: {"removed": False, "note": "relationship"}}
        self.state["order"] = [path]
        return self.fake._pagex_mint(self.state)[0]

    def test_whole_task_folder_is_linked_and_both_faces_are_visible(self):
        folder = self.task_folder()
        rec = self.mint_one("project/tasks/A01/")

        self.assertEqual(rec["state"], "ok")
        self.assertEqual(rec["kind"], "folder")
        self.assertTrue(rec["folder_status"]["plan"])
        self.assertFalse(rec["folder_status"]["page"])
        link = self.base / "_folders" / "project" / "tasks" / "A01"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), folder.resolve())

        self.fake._pagex_write(self.state)
        self.fake._pagex_view(self.state, [rec])
        view = (self.base / "Q1-view.html").read_text(encoding="utf-8")
        self.assertIn("Folder linked", view)
        self.assertIn("⬜ Page Face", view)
        self.assertIn("✅ Task plan", view)
        self.assertIn("⬜ Task report", view)

    def test_report_and_qa_status_are_read_from_source_files(self):
        folder = self.task_folder()
        (folder / "workflow" / "report.yaml").write_text(
            "# O: status=complete\n", encoding="utf-8")
        (folder / "QA").mkdir()
        (folder / "QA" / "check.md").write_text("# check\n", encoding="utf-8")

        status = _folder_markers(folder)
        self.assertEqual(status["badge"], "✅")
        self.assertEqual(status["qa_n"], 1)
        self.assertIn("complete", status["label"])

    def test_named_page_folder_is_a_linkable_folder(self):
        folder = self.root / "pages" / "Q2"
        folder.mkdir(parents=True)
        (folder / "Q2.md").write_text("# Q2\nstate: ✅ settled\n",
                                      encoding="utf-8")
        self.assertTrue(_is_addressable_folder(folder))
        rec = self.mint_one("pages/Q2/")
        self.assertEqual(rec["state"], "ok")
        self.assertTrue(rec["folder_status"]["page"])

    def test_arbitrary_directory_is_refused(self):
        folder = self.root / "scratch" / "assets"
        folder.mkdir(parents=True)
        rec = self.mint_one("scratch/assets/")
        self.assertEqual(rec["state"], "refused")
        self.assertIn("neither a Page Face nor a Task Face", rec["why"])

    def test_own_home_and_outside_resolution_are_refused(self):
        own = self.mint_one("board/Q1/")
        self.assertEqual(own["state"], "refused")
        self.assertIn("own home", own["why"])

        outside = self.tmp_root / "outside"
        outside.mkdir()
        (outside / "outside.md").write_text("# outside\n", encoding="utf-8")
        (self.root / "outside-link").symlink_to(outside)
        escaped = self.mint_one("outside-link/")
        self.assertEqual(escaped["state"], "refused")
        self.assertIn("outside the repo root", escaped["why"])

    def test_existing_file_borrow_keeps_file_behavior(self):
        folder = self.root / "pages" / "Q2"
        folder.mkdir(parents=True)
        source = folder / "Q2.md"
        source.write_text("# Q2\n", encoding="utf-8")
        rec = self.mint_one("pages/Q2/Q2.md")
        self.assertEqual(rec["state"], "ok")
        self.assertEqual(rec["kind"], "file")
        self.assertTrue((self.base / "Q2" / "Q2.md").is_symlink())

    def test_entry_normalizes_a_whole_folder_with_trailing_slash(self):
        self.task_folder()
        result, err = self.fake.pagex_entry({
            "borrow": "project/tasks/A01",
            "note": "whole work object",
        })
        self.assertIsNone(err)
        self.assertEqual(result["path"], "project/tasks/A01/")
        self.assertIn("project/tasks/A01/", self.state["rows"])
        self.assertIn("- project/tasks/A01/ · note: whole work object",
                      self.store.read_text(encoding="utf-8"))

    def test_retired_task_plugin_runtime_is_absent(self):
        board = Path(__file__).resolve().parents[1]
        serve = (board / "cli" / "serve.py").read_text(encoding="utf-8")
        self.assertNotIn("TaskMixin", serve)
        self.assertNotIn('"/_board/task"', serve)
        self.assertFalse((board / "live" / "task.py").exists())


if __name__ == "__main__":
    unittest.main()
