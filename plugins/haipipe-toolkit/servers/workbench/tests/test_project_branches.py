"""The Project Timeline's transit map (page/project_branches.py) and the SPACE Home (page/space_home.py)."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()
from live import focus_page, frame, project_branches as PB  # noqa: E402


def _project(root: Path) -> Path:
    """A Project with two work Blocks, each with one finished Run."""
    project = root / "examples" / "Project-Example"
    (project / "work").mkdir(parents=True)
    (project / "project.yaml").write_text("id: Example\nmission: Test the map.\n")
    (project / "project.md").write_text("# Example\n")
    (project / "work" / "work.md").write_text("# Work\n")
    for name, day in (("b01_first", "2026-11-02"), ("b02_second", "2026-11-09")):
        block = project / "work" / name
        run = block / "runs" / "r01_fit"
        (run / "result").mkdir(parents=True)
        (block / "board.md").write_text(f"# {name}\nspine: {name} goal.\n")
        (run / "run.yaml").write_text("run: r01_fit\nkind: hard\nstatus: done\n")
        (run / "result" / "runtime.yaml").write_text(f"finished_at: '{day}T10:00:00'\nstatus: done\n")
    return project


class ColumnsTest(unittest.TestCase):
    def test_a_line_that_has_ended_gives_its_column_to_a_later_one(self):
        a, b, c = Path("a"), Path("b"), Path("c")
        rows = [("d", "run", "", "", a), ("d", "run", "", "", a), ("d", "run", "", "", b), ("d", "run", "", "", c),
                ("d", "run", "", "", b)]
        lane, span = PB.columns([a, b, c], rows)
        self.assertEqual(lane[a], 0)
        self.assertEqual(lane[b], 1)              # b runs over rows 2-4, beside c
        self.assertNotEqual(lane[c], lane[b])
        self.assertEqual(lane[c], 0)              # a ended at row 1, so c takes its column


class MapTest(unittest.TestCase):
    def test_a_projects_timeline_draws_one_line_per_block_with_its_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            project = _project(root)
            html = PB.branches_html(project, root)
            self.assertEqual(len(re.findall(r'class="br-chip"', html)), 2)
            self.assertEqual(len(re.findall(r'class="br-row"', html)), 2)
            self.assertLess(html.index("b02_second</a></div>"), html.index("b01_first</a></div>"))   # newest on top
            page = focus_page.render(frame.Theme(name="work"), root, project, "timeline", "")
            self.assertIn('class="br-map"', page)

    def test_an_empty_project_says_so(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            project = root / "Project-Empty"
            (project / "work").mkdir(parents=True)
            (project / "project.yaml").write_text("id: Empty\n")
            self.assertIn("Nothing dated", PB.branches_html(project, root))


class SpaceHomeTest(unittest.TestCase):
    def test_the_space_page_opens_on_home_with_its_projects_and_no_block_lists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = (Path(tmp) / "Test-SPACE").resolve()
            root.mkdir()
            _project(root)
            page = focus_page.render(frame.VANILLA, root, root, "", "")
            self.assertIn("📁 Projects", page)
            self.assertIn("Project-Example", page)
            self.assertNotIn(">Themes<", page)
            old = focus_page.render(frame.VANILLA, root, root, "report", "themes")   # an old link opens Home
            self.assertIn("📁 Projects", old)


if __name__ == "__main__":
    unittest.main()
