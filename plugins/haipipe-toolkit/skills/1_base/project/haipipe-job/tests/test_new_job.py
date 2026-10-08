"""haipipe-job: the new-Job scaffold, Task slots in order, a theme's own names, the check."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import new_job  # noqa: E402


class NewJobTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project-Example" / "tasks" / "b01_topic"
        self.block.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01 · <topic>\n\nboard-kind: task-block\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_job_has_its_face_and_an_empty_task_list(self):
        md = new_job.new_job(self.block, "first", "First", answers="Q01")
        self.assertEqual(md.relative_to(self.block).as_posix(), "j01_first/j01_first.md")
        text = md.read_text()
        self.assertTrue(text.startswith("# j01 · First\n"))
        self.assertIn("answers: Q01", text)
        self.assertIn("## Tasks", text)
        self.assertEqual(new_job.check(md.parent), [])

    def test_tasks_are_added_in_order_and_listed(self):
        job = new_job.new_job(self.block, "first", "First").parent
        new_job.add_task(job, "load", "Load", answers="Q01.E1")
        md = new_job.add_task(job, "write", "Write it up", kind="page")
        self.assertEqual(md.parent.name, "t02_write")
        self.assertIn("task-kind: page", md.read_text())
        self.assertEqual(new_job.listed((job / "j01_first.md").read_text()), ["t01_load", "t02_write"])
        self.assertIn("2. t02_write · Write it up", (job / "j01_first.md").read_text())
        self.assertEqual(new_job.check(job), [])

    def test_the_check_finds_a_folder_not_listed_and_a_name_not_on_disk(self):
        job = new_job.new_job(self.block, "first", "First").parent
        new_job.add_task(job, "load", "Load")
        stray = job / "t05_stray"
        stray.mkdir()
        (stray / "t05_stray.md").write_text("# t05\n")
        md = job / "j01_first.md"
        md.write_text(md.read_text().replace("1. t01_load · Load", "1. t01_load · Load\n2. t09_gone · Gone"))
        found = new_job.check(job)
        self.assertIn("## Tasks names t09_gone, which is not a Task folder here", found)
        self.assertIn("t05_stray/ is not in ## Tasks", found)

    def test_a_theme_names_its_own_jobs_and_tasks(self):
        job = new_job.new_job(self.block, "", "Version A", name="Ba-version").parent
        self.assertEqual(job.name, "Ba-version")
        self.assertTrue((job / "Ba-version.md").read_text().startswith("# Ba-version · Version A"))
        md = new_job.add_task(job, "", "Introduction", name="S-introduction")
        self.assertEqual(md.parent.name, "S-introduction")
        self.assertEqual(new_job.check(job), [])

    def test_refusals(self):
        with self.assertRaises(ValueError):                      # not a Block
            new_job.new_job(self.block.parent, "x", "X")
        new_job.new_job(self.block, "first", "First")
        with self.assertRaises(ValueError):                      # the number is taken
            new_job.new_job(self.block, "again", "Again", nn=1)
        with self.assertRaises(ValueError):                      # a Task needs a Job face
            new_job.add_task(self.block, "x", "X")

    def test_the_report_check_counts_a_task_answering_a_need(self):
        (self.block / "board.md").write_text("# b01\n\n## Questions\n\n```yaml\nquestions:\n  - id: Q01\n```\n")
        job = new_job.new_job(self.block, "first", "First").parent
        new_job.add_task(job, "load", "Load", answers="Q01.E1")
        sys.path.insert(0, str(SCRIPTS.parents[1] / "haipipe-report" / "scripts"))
        import check_report
        rows, findings = check_report.rows(self.block)
        self.assertEqual(rows[0]["work"], ["j01_first/t01_load"])
        self.assertEqual(findings, [])

    def test_the_cli(self):
        run = lambda *a: subprocess.run([sys.executable, str(SCRIPTS / "new_job.py"), *a], capture_output=True, text=True)
        out = run("job", str(self.block), "--slug", "cli", "--title", "CLI")
        self.assertEqual(out.returncode, 0, out.stderr)
        job = self.block / "j01_cli"
        self.assertEqual(run("task", str(job), "--slug", "one", "--title", "One").returncode, 0)
        self.assertEqual(run("check", str(job)).returncode, 0)


if __name__ == "__main__":
    unittest.main()
