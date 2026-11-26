"""Clickable Run addresses (address_links.py, JL 261103): an address resolves inside its Project, work/ before
discovery/, falling back to the Task, Job or Block; only text outside tags, links and buttons is linked. Placeholders
only: the Project is written into a temp folder."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import address_links as al  # noqa: E402


class AddressLinksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.space = Path(self.tmp.name).resolve()
        self.project = self.space / "examples-x" / "Project-Example"
        p = self.project
        for rel in ("work/b52_results/j01_sample/t01_cohort/runs/r01_paper",
                    "work/b52_results/j01_sample/t02_profile/runs/r01_first",
                    "work/b52_results/j01_sample/t02_profile/runs/r01_second",     # a shared Run number
                    "discovery/b03_related/j01_search/t01_papers/runs/r02_read",
                    "paper/Paper-X/j11_writing_v1130_desk/t01_introduction",
                    "paper/Paper-X/j21_evidence_display/t01_table1"):
            (p / rel).mkdir(parents=True)
        (p / "project.yaml").write_text("name: Project-Example\n", encoding="utf-8")
        self.version = p / "paper/Paper-X/j11_writing_v1130_desk"

    def test_resolve_each_level_and_the_fallbacks(self):
        w = self.project / "work/b52_results/j01_sample"
        self.assertEqual(al.resolve("b52.j01.t01.r01", self.project), w / "t01_cohort/runs/r01_paper")
        self.assertEqual(al.resolve("b52 j01 t01", self.project), w / "t01_cohort")
        self.assertEqual(al.resolve("b52.j01.t02.r01", self.project), w / "t02_profile")   # shared Run: the Task
        self.assertEqual(al.resolve("b52.j01.t09", self.project), w)                        # missing Task: the Job
        self.assertEqual(al.resolve("b03.j01.t01.r02", self.project),
                         self.project / "discovery/b03_related/j01_search/t01_papers/runs/r02_read")
        self.assertIsNone(al.resolve("b99.j01", self.project))
        self.assertIsNone(al.resolve("b52.j01.t01 extra", self.project))

    def test_href_is_the_focus_page(self):
        f = al.resolve("b52.j01.t01", self.project)
        self.assertEqual(al.href(f, self.space),
                         "/_board/workbench?path=examples-x/Project-Example/work/b52_results/j01_sample/t01_cohort&layout=focus")

    def test_linkify_only_text_and_never_twice(self):
        html = ('<p title="b52.j01.t01">made-by: b52.j01.t01.r01, then <a href="x">b52.j01.t01</a> '
                '<button>b52.j01</button> b99.j01 and b52.j01.t01.csv</p><script>var a = "b52.j01" < 1;</script>'
                '<textarea>b52.j01</textarea>')
        out = al.linkify(html, self.project, self.space)
        self.assertEqual(out.count("<a class=addr-link"), 1)
        self.assertIn('target="_top">b52.j01.t01.r01</a>', out)
        self.assertIn('title="b52.j01.t01"', out)               # the attribute is untouched
        self.assertIn("<button>b52.j01</button>", out)
        self.assertIn("b99.j01 and b52.j01.t01.csv", out)       # unresolvable and file names stay plain
        self.assertIn('<script>var a = "b52.j01" < 1;</script><textarea>b52.j01</textarea>', out)
        self.assertEqual(al.linkify(out, self.project, self.space), out)   # a second pass adds nothing

    def test_section_name_links_to_its_write_view(self):
        sections = al.writing_jobs(al.paper_board_of(self.version))
        self.assertEqual([j.name for j in sections], ["j11_writing_v1130_desk"])   # the evidence Job is not a version
        out = al.linkify("<td>t01_introduction, t01_table1</td>", self.project, self.space, sections)
        self.assertIn("j11_writing_v1130_desk/t01_introduction&amp;layout=focus&amp;section=work&amp;group=write", out)
        self.assertIn(", t01_table1</td>", out)

    def test_page_linker_and_views(self):
        link = al.page_linker(self.version / "t01_introduction", self.space)
        views = al.linked_views({"a": ("A", lambda: "<p>b52.j01.t01 in t01_introduction</p>"), "runs": ("Runs", None),
                                 "s": ("S", "<p>b52.j01</p>")}, link)
        self.assertEqual(views["a"][1]().count("<a class=addr-link"), 1)     # the page itself is not linked
        self.assertEqual(al.page_linker(self.version, self.space)("<p>b52.j01.t01 in t01_introduction</p>").count("<a "), 2)
        self.assertIsNone(views["runs"][1])
        self.assertIn("j01_sample&amp;layout=focus", views["s"][1])
        outside = al.page_linker(self.version, self.space / "elsewhere")   # a root the folder is not under: no link,
        self.assertEqual(outside("<p>b52.j01</p>"), "<p>b52.j01</p>")      # never an error


if __name__ == "__main__":
    unittest.main()
