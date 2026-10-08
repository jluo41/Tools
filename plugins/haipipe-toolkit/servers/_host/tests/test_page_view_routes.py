"""The old Page workbench's routes answer through the frame (JL 261007: "why not merge them into the
base"): a GET or HEAD of /_board/<old>?q is /_board/workbench?view=<view>&q; its POST twin keeps its
address; a board page's old name is its theme's name now."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import host_registry as R  # noqa: E402
import serve  # noqa: E402


class PageViewRouteTest(unittest.TestCase):
    def test_old_page_routes_answer_as_frame_views(self):
        self.assertEqual(serve.new_route_name("/_board/runs?path=a.md&run=r1"),
                         "/_board/workbench?view=runs&path=a.md&run=r1")
        self.assertEqual(serve.new_route_name("/_board/outline", "HEAD"), "/_board/workbench?view=draft")
        self.assertEqual(serve.new_route_name("/_board/folderstat?path=a.md"),
                         "/_board/workbench?view=folder&path=a.md")
        self.assertEqual(serve.new_route_name("/_board/draft", "POST"), "/_board/draft")   # the write twin

    def test_board_pages_take_their_themes_names(self):
        self.assertEqual(serve.new_route_name("/_board/task-board?path=x"), "/_board/work-board?path=x")
        self.assertEqual(serve.new_route_name("/_board/paper?path=x"), "/_board/paper-board?path=x")

    def test_only_page_host_serves_page_views_through_the_frame(self):
        self.assertTrue(R.route_allowed("/_board/workbench?view=draft&path=x", {"page"}))
        self.assertFalse(R.route_allowed("/_board/workbench?path=x", {"page"}))

    def test_every_view_has_a_method_and_every_old_route_a_view(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "workbench"))
        import frame_view  # noqa: E402
        self.assertEqual(set(serve.PAGE_VIEW_ROUTES.values()), set(frame_view.VIEW_METHODS))
        for method in frame_view.VIEW_METHODS.values():
            self.assertTrue(hasattr(serve.Handler, method), method)


    def test_a_task_pages_short_tab_link_opens_its_space_in_the_frame(self):
        from live.home import resolve_workbench
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "Project-X/work/b01_topic"
            task = block / "j01_job/t01_task"
            task.mkdir(parents=True)
            (root / "Project-X/project.yaml").write_text("name: x\n")
            (block / "board.md").write_text("# Topic\n\nboard-kind: task-block\n")
            (task / "t01_task.md").write_text("# A task\n")
            self.assertEqual(resolve_workbench(root, "b01_topic", "t01_task", "runs")[0],
                             "/_board/workbench?path=Project-X%2Fwork%2Fb01_topic%2Fj01_job%2Ft01_task"
                             "&space=Runs&sub=Page+Runs")
            self.assertTrue(resolve_workbench(root, "b01_topic", "t01_task", "pageruns")[0]
                            .startswith("/_board/pageruns?"))          # data, not a Space


if __name__ == "__main__":
    unittest.main()
