"""haipipe-run: keep only meaningful Runs (JL 261019). prune_runs.py marks a replaced or never-run hard Run for
pruning only when nothing in use reads it, and --apply deletes exactly those, with their configs."""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import prune_runs  # noqa: E402


def run(task: Path, name: str, result: bool = True, config: str = "", status: str = "") -> Path:
    folder = task / "runs" / name
    (folder / "result").mkdir(parents=True)
    (folder / f"{name}.sh").write_text("#!/usr/bin/env bash\n")
    (folder / "run.yaml").write_text(f"run: {name}\nkind: hard\nstatus: {status or 'null'}\n")
    if result:
        (folder / "result" / "metrics.json").write_text("{}")
    cfg = task / "scripts" / "config"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / f"{name}.yaml").write_text(config or f"run: {name}\n")
    return folder


class PruneRunsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "Project-Example"
        (root).mkdir()
        (root / "project.yaml").write_text("name: Project-Example\n")
        self.task = root / "work" / "b01_topic" / "j01_job" / "t01_fit"
        self.task.mkdir(parents=True)
        (self.task / "t01_fit.md").write_text("# Fit\n- r02_old and r05_old are listed here\n")
        run(self.task, "r01_placeholder", result=False)                      # never ran, not planned
        run(self.task, "r02_old")                                            # replaced, but read by r04
        run(self.task, "r03_new", config="run: r03_new\nsupersedes: r02_old   # new inputs\n")
        run(self.task, "r04_figures", config="reads: t01_fit/runs/r02_old/result\n")
        run(self.task, "r05_old")                                            # replaced, read by nothing
        run(self.task, "r06_new", config="supersedes: r05_old\n")
        run(self.task, "r07_planned", result=False, status="planned")        # open: kept
        report = root / "work" / "b01_topic" / "reports" / "q01_x"
        report.mkdir(parents=True)
        (report / "build.py").write_text('T = "t01_fit"\nOLD = T + "/runs/" + "r05_old"\n')  # a stale reader

    def tearDown(self):
        self.tmp.cleanup()

    def verdicts(self):
        runs, out, _ = prune_runs.verdicts(self.task)
        return {r.name: out[r.folder][0] for r in runs}

    def test_only_unread_replaced_or_never_run_runs_are_marked(self):
        v = self.verdicts()
        self.assertEqual(v["r01_placeholder"], "prune")
        self.assertEqual(v["r02_old"], "keep")          # r04's config reads it
        self.assertEqual(v["r05_old"], "keep")          # a report builder names the Task and the Run
        for name in ("r03_new", "r04_figures", "r06_new", "r07_planned"):
            self.assertEqual(v[name], "keep", name)

    def test_a_run_that_wrote_to_a_store_is_not_never_ran(self):
        space = self.task.parents[4]
        (space / "env.sh").write_text("")
        store = space / "_WorkSpace" / "Calls" / "fold00_v1"
        store.mkdir(parents=True)
        (store / "answers.jsonl").write_text("{}\n")
        run(self.task, "r08_store_ran", result=False, config="output_dir: _WorkSpace/Calls/fold00_v1\n")
        run(self.task, "r09_store_elsewhere", result=False, config="output_dir: _WorkSpace/Calls/fold01_v1\n")
        v = self.verdicts()
        self.assertEqual(v["r08_store_ran"], "keep")      # its output is in the store: it ran
        self.assertEqual(v["r09_store_elsewhere"], "check")  # not here: maybe another machine; a person looks
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.task), "--apply", "--untracked-ok"])
        self.assertTrue((self.task / "runs" / "r09_store_elsewhere").is_dir())   # --apply never takes a check

    def test_to_old_moves_an_untracked_run_and_its_config_instead_of_deleting(self):
        """JL 261021: a pruned Run git does not hold is kept in work/_old/, not lost."""
        with redirect_stdout(io.StringIO()) as out:
            prune_runs.main([str(self.task), "--apply", "--to-old", "--only", "r01_placeholder"])
        self.assertFalse((self.task / "runs" / "r01_placeholder").exists())
        batch = next((self.task.parents[2] / "_old").glob("b01_pruned_*"))
        home = batch / "j01_t01_fit_runs"
        self.assertTrue((home / "runs" / "r01_placeholder" / "run.yaml").is_file())
        self.assertTrue((home / "config" / "r01_placeholder.yaml").is_file())
        self.assertTrue((batch / "README.md").is_file())
        self.assertNotIn("refused", out.getvalue())                  # untracked, yet nothing is lost: no refusal

    def test_the_task_page_is_a_mention_not_a_reader(self):
        (self.task.parent.parent / "reports" / "q01_x" / "build.py").unlink()
        self.assertEqual(self.verdicts()["r05_old"], "prune")

    def test_dry_run_deletes_nothing(self):
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.task)])
        self.assertTrue((self.task / "runs" / "r01_placeholder").is_dir())

    def test_apply_deletes_the_marked_runs_and_their_configs(self):
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.task), "--apply", "--untracked-ok"])
        self.assertFalse((self.task / "runs" / "r01_placeholder").exists())
        self.assertFalse((self.task / "scripts" / "config" / "r01_placeholder.yaml").exists())
        for name in ("r02_old", "r03_new", "r05_old", "r07_planned"):
            self.assertTrue((self.task / "runs" / name).is_dir(), name)

    def test_only_prunes_a_read_candidate_once_a_person_judges_its_reader_stale(self):
        with redirect_stdout(io.StringIO()) as out:
            prune_runs.main([str(self.task), "--apply", "--untracked-ok", "--only", "r05_old", "r03_new"])
        self.assertFalse((self.task / "runs" / "r05_old").exists())
        self.assertTrue((self.task / "runs" / "r03_new").is_dir())    # current: never a candidate
        self.assertIn("r03_new: not a candidate", out.getvalue())


class PruneRunsCasesTest(unittest.TestCase):
    """The cases a fresh reviewer found on LLMRec b03 (261019): same-named Runs in sibling Tasks, a lost
    supersedes chain, ambiguous --only names, an untracked scope, and code that globs a config folder."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "Project-Example"
        self.root.mkdir()
        (self.root / "project.yaml").write_text("name: Project-Example\n")
        job = self.root / "work" / "b01_topic" / "j01_job"
        self.t1, self.t2 = job / "t01_fit", job / "t02_other"
        for task in (self.t1, self.t2):
            task.mkdir(parents=True)
            run(task, "r02_old")
            run(task, "r04_new", config="supersedes: r02_old\n")

    def tearDown(self):
        self.tmp.cleanup()

    def verdicts(self, scope=None):
        runs, out, _ = prune_runs.verdicts(scope or self.t1.parent)
        return {f"{r.task.name[:3]}/{r.name}": out[r.folder][0] for r in runs}

    def test_a_line_about_a_sibling_tasks_run_does_not_keep_this_one(self):
        report = self.root / "work" / "b01_topic" / "reports"
        report.mkdir()
        (report / "build.py").write_text('T01 = "t01_fit"\nT02 = "t02_other"\n'
                                         'OLD = T01 / "r02_old/result"; NEW = T02 / "r04_new/result"\n')
        (self.t2 / "scripts" / "config" / "r04_new.yaml").write_text(
            "supersedes: r02_old\nreads: t01_fit/runs/r02_old/result\n")
        v = self.verdicts()
        self.assertEqual(v["t01/r02_old"], "keep")     # the builder's T01 line names t01's Run
        self.assertEqual(v["t02/r02_old"], "prune")    # neither line is about t02's r02

    def test_a_replaced_runs_config_is_a_frozen_input_not_a_reader(self):
        run(self.t1, "r01_older", status="superseded")
        run(self.t1, "r03_mid", config="supersedes: r02_old\nreads: t01_fit/runs/r01_older/result\n")
        (self.t1 / "scripts" / "config" / "r04_new.yaml").write_text("supersedes: r03_mid\n")
        v = self.verdicts(self.t1)
        self.assertEqual(v["t01/r01_older"], "prune")  # only the replaced r03 names it

    def test_deleting_a_middle_run_marks_the_one_it_replaced(self):
        run(self.t1, "r03_mid", config="supersedes: r02_old\n")
        (self.t1 / "scripts" / "config" / "r04_new.yaml").write_text("supersedes: r03_mid\n")
        (self.t1 / "scripts" / "config" / "r09_fig.yaml").write_text("reads: t01_fit/runs/r02_old/result\n")
        run(self.t1, "r09_fig", config="reads: t01_fit/runs/r02_old/result\n")
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.t1), "--apply", "--untracked-ok", "--only", "r03_mid"])
        self.assertFalse((self.t1 / "runs" / "r03_mid").exists())
        self.assertIn("status: superseded", (self.t1 / "runs" / "r02_old" / "run.yaml").read_text())

    def test_only_refuses_a_bare_name_two_tasks_hold(self):
        with redirect_stdout(io.StringIO()) as out:
            prune_runs.main([str(self.t1.parent), "--apply", "--untracked-ok", "--only", "r02_old"])
        self.assertIn("name it as <task>/<run>", out.getvalue())
        self.assertTrue((self.t1 / "runs" / "r02_old").is_dir() and (self.t2 / "runs" / "r02_old").is_dir())
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.t1.parent), "--apply", "--untracked-ok", "--only", "t02/r02_old"])
        self.assertFalse((self.t2 / "runs" / "r02_old").exists())
        self.assertTrue((self.t1 / "runs" / "r02_old").is_dir())

    def test_apply_refuses_what_git_does_not_hold(self):
        with redirect_stdout(io.StringIO()) as out:
            prune_runs.main([str(self.t1), "--apply"])
        self.assertIn("git holds no copy", out.getvalue())
        self.assertTrue((self.t1 / "runs" / "r02_old").is_dir())

    def test_code_that_globs_a_tasks_config_folder_reads_every_run_there(self):
        tools = self.root / "work" / "b01_topic" / "tools"
        tools.mkdir()
        (tools / "export.py").write_text('D = ROOT / "t01_fit/scripts/config"\nfor p in D.glob("*.yaml"): pass\n')
        v = self.verdicts()
        self.assertEqual(v["t01/r02_old"], "keep")
        self.assertEqual(v["t02/r02_old"], "prune")

    def test_a_paper_page_citing_an_address_range_reads_the_run(self):
        story = self.root / "paper" / "Paper-X" / "studio" / "s02-story"
        story.mkdir(parents=True)
        (story / "s02-story.md").write_text("| E18 | 40% unmatched | b01.j01.t01 r01 to r03 |\n")
        own = self.root / "work" / "b01_topic" / "studio" / "s21-j01"
        own.mkdir(parents=True)
        (own / "s21-j01.md").write_text("runs:\n  t02_other/r02_old: replaced\n")
        v = self.verdicts()
        self.assertEqual(v["t01/r02_old"], "keep")     # the story cites b01.j01.t01 r01 to r03
        self.assertEqual(v["t02/r02_old"], "prune")    # its own Block's Studio face only lists it

    def test_an_orphan_companion_config_goes_with_its_run(self):
        (self.t1 / "scripts" / "config" / "driver_tags_r02.yaml").write_text("tags: []\n")
        with redirect_stdout(io.StringIO()):
            prune_runs.main([str(self.t1), "--apply", "--untracked-ok"])
        self.assertFalse((self.t1 / "scripts" / "config" / "driver_tags_r02.yaml").exists())


if __name__ == "__main__":
    unittest.main()
