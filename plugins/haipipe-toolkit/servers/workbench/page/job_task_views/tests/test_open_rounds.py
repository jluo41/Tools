"""On a Job's Main, a Task fold's Run row opens its Run page and each round row its pass.md, in the page's viewer."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import focus_plan_results as fp  # noqa: E402


class OpenRoundsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.job = self.root / "P" / "work" / "b01_x" / "j01_a"
        self.task = self.job / "t01_one"
        run = self.task / "runs" / "run-check-one"
        for name, head in (("p01-1125", "first round"), ("p02-1126", "second round")):
            (run / "passes" / name).mkdir(parents=True)
            (run / "passes" / name / "pass.md").write_text(f"# {head}\n\n## Summary\n\nIt ran.\n")
        (run / "run.yaml").write_text("run: run-check-one\nstatus: done\n")
        (self.job / "j01_a.md").write_text("# j01 · A\n\n## Tasks\n\n1. t01_one · One\n")
        (self.task / "t01_one.md").write_text("# One\nstate: OPEN\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_run_is_a_fold_the_newest_open(self):
        older = self.task / "runs" / "run-build-one"
        (older / "passes" / "p01-1120").mkdir(parents=True)
        (older / "passes" / "p01-1120" / "pass.md").write_text("# build\n")
        (older / "run.yaml").write_text("run: run-build-one\nstatus: done\n")
        html = "".join(body for _, _, body in fp.tasks_section(self.job, self.root))
        folds = re.findall(r'<details class=task-run( open)?><summary><div class="task-rr run[^>]*>.*?<a class=rr-name[^>]*>([^<]+)</a>', html)
        self.assertEqual([(o, name) for o, name in folds], [(" open", "run-check-one"), ("", "run-build-one")])

    def test_run_and_round_rows_are_links_to_the_viewer(self):
        html = "".join(body for _, _, body in fp.tasks_section(self.job, self.root))
        rows = re.findall(r'class="task-rr (run|round)[^"]*"[^>]*>(?:<[^>]*>)*?(?:<a class=rr-name )?href="([^"]*)" data-pop="([^"]*)"', html)
        rows = [(k, h, p) for k, h, p in re.findall(r'<a class="task-rr (round)[^"]*"[^>]*href="([^"]*)" data-pop="([^"]*)"', html)]
        run = re.search(r'<a class=rr-name href="([^"]*)" data-pop="([^"]*)"', html)
        rows = [("run", run.group(1), run.group(2))] + rows
        kinds = [k for k, _, _ in rows]
        self.assertEqual(kinds, ["run", "round", "round"])
        self.assertIn("part=run", rows[0][1].replace("&amp;", "&"))
        self.assertIn("p02-1126", rows[1][1].replace("%2F", "/"))
        self.assertIn("pass.md", rows[1][1].replace("%2F", "/"))
        self.assertTrue(all(pop for _, _, pop in rows))


if __name__ == "__main__":
    unittest.main()
