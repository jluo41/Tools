"""The design ladder's scaffold (ref/design-ladder.md) makes each level, names every Run run-<type>-<target>, never
overwrites, and writes what the design workbench's reader (servers/workbench-design/design_reader.py) reads."""
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE))
import design_ladder as D  # noqa: E402
from ladder_kit import ready  # noqa: E402

READER = HERE.parents[4] / "servers" / "workbench-design" / "design_reader.py"
sys.path.insert(0, str(READER.parents[1] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()  # the reader imports src.common, the Page engine's shared paths


def reader():
    spec = importlib.util.spec_from_file_location("design_reader_under_test", READER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class DesignLadderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project" / "designs" / "b01_demo_app"
        ready(self.block, n=3)
        self.job = self.block / "j01_g01_m04"
        D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])
        D.main(["task", str(self.job), "t00"])
        D.main(["task", str(self.job), "d01", "reason-first"])
        D.main(["task", str(self.job), "t99"])

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_level_has_its_face_and_folders(self):
        for p in ("board.md", "design-goal.md", "inputs", "observed", "studio", "reports", "delivery", "runs/README.md"):
            self.assertTrue((self.block / p).exists(), p)
        for p in ("j01_g01_m04.md", "inputs", "delivery", "t00_reason-ideas/t00_reason-ideas.md",
                  "t01_d01_reason-first/t01_d01_reason-first.md", "t01_d01_reason-first/elements.yaml",
                  "t99_review-whole/t99_review-whole.md"):
            self.assertTrue((self.job / p).exists(), p)
        self.assertIn("method: M04 m2", (self.job / "j01_g01_m04.md").read_text())

    def test_every_run_is_run_type_target_and_hard_ones_keep_a_result(self):
        t00, d01, t99 = self.job / "t00_reason-ideas", self.job / "t01_d01_reason-first", self.job / "t99_review-whole"
        made = {D.run(self.block, "setup-rules", "", []), D.run(self.block, "add-goal", "g01", []),
                D.run(self.job, "setup-goal", "", []), D.run(self.job, "open-designs", "", []),
                D.run(t00, "reason", "", []), D.run(d01, "generate", "", []), D.run(d01, "verify", "", [])}
        rev = D.run(d01, "revise", "", [])
        (rev / "passes" / "p01-1007").mkdir(parents=True)
        (rev / "passes" / "p01-1007" / "design.md").write_text("<draft 2>\n")
        made |= {rev, D.run(d01, "verify", "", []), D.run(t99, "rank", "", [])}
        self.assertEqual({p.name for p in made},
                         {"run-setup-rules", "run-add-goal-g01", "run-setup-goal-j01", "run-open-designs-j01",
                          "run-reason-t00", "run-generate-d01", "run-verify-d01-v1", "run-revise-d01",
                          "run-verify-d01-v2", "run-rank-t99"})
        for p in made:
            hard = p.name.split("-")[1] in D.HARD
            self.assertIn(f"kind: {'hard' if hard else 'soft'}", (p / "run.yaml").read_text())
            self.assertTrue((p / ("result" if hard else "passes")).is_dir(), p.name)

    def test_nothing_is_overwritten(self):
        self.assertEqual(D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"]), [])
        with self.assertRaises(SystemExit):                     # verify needs a draft to read
            D.main(["run", str(self.job / "t01_d01_reason-first"), "verify"])
        self.assertEqual(D.main(["task", str(self.job), "d01", "reason-first"]), [])

    def test_bad_names_are_refused(self):
        for argv in (["job", str(self.block / "j02_reminder_by-insight"), "--goal", "G01", "--method", "M04 m2",
                      "--inputs", "i2"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "by insight", "--inputs", "i2"],
                     ["task", str(self.job), "d02"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m9", "--inputs", "i2"],
                     ["job", str(self.block / "j02_g02_m04"), "--goal", "G02", "--method", "M04 m2", "--inputs", "i2"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i7"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2",
                      "--n", "9"],
                     ["job", str(self.block / "j02_g01_m01"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"],
                     ["run", str(self.job / "t00_reason-ideas"), "generate"],
                     ["run", str(self.block), "reason"]):
            with self.assertRaises(SystemExit):
                D.main(argv)

    def test_a_job_name_carries_readable_slugs(self):
        """The older id form jNN_<goal>-<goal-slug>_<method>-<method-slug> (JL 261008) stays readable."""
        job = self.block / "j02_g01-a-goal_m04-actionable-insights"
        D.main(["job", str(job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])
        self.assertTrue((job / f"{job.name}.md").is_file())
        self.assertEqual(D.level_of(job), "Job")
        with self.assertRaises(SystemExit):                              # the ids must still match the pins
            D.main(["job", str(self.block / "j03_g02-a-goal_m04-x"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"])

    def test_a_job_is_named_by_its_goal_and_method_in_words(self):
        """jNN_<goal name>_<method name> (JL 261011): the ids stay in the face's pins; the title is in words."""
        board = self.block / "board.md"
        board.write_text(board.read_text().replace("id: G01", "id: G01\n  name: prepare-before-visit", 1))
        job = self.block / "j02_prepare-before-visit_actionable-insights"
        D.main(["job", str(job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])
        face = (job / f"{job.name}.md").read_text()
        self.assertIn("goal: G01 · prepare-before-visit\n", face)       # the id, then the goal's name (261108)
        self.assertEqual(reader().job(job)["goal"], "G01")                 # the reader takes the id
        self.assertIn("method: M04 m2", face)
        self.assertIn("# Prepare before visit, by Actionable insights", face)
        self.assertEqual(D.level_of(job), "Job")
        D.main(["task", str(job), "t00"])                                  # a Task opens in a readable Job
        for wrong in ("j03_prepare-before-visit_goal-only", "j03_questions-before-visit_actionable-insights"):
            with self.assertRaises(SystemExit):                          # the words must name the pinned goal and method
                D.main(["job", str(self.block / wrong), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"])

    def test_goals_gives_an_older_job_face_its_goal_name(self):
        """`goals <block>` adds the goal's name to a face whose `goal:` holds the id alone, and touches nothing else."""
        board = self.block / "board.md"
        board.write_text(board.read_text().replace("id: G01", "id: G01\n  name: a-goal", 1))
        face = self.job / f"{self.job.name}.md"
        before = face.read_text()
        self.assertIn("goal: G01\n", before)                              # made before G01 had a name
        self.assertEqual(D.main(["goals", str(self.block)]), [face])
        after = face.read_text()
        self.assertEqual(after, before.replace("goal: G01\n", "goal: G01 · a-goal\n", 1))
        self.assertEqual(D.main(["goals", str(self.block)]), [])          # a named face is left as it is
        self.assertEqual(reader().job(self.job)["goal"], "G01")

    def test_a_block_is_named_by_its_kind(self):
        """A design Block is a special board, Design-<name>[-<YYMMDD>] (JL 261008); bNN_<app> stays readable."""
        root = Path(self.tmp.name) / "Project" / "designs"
        D.main(["block", str(root / "Design-Demo-Round2-261008"), "--title", "<application>"])
        self.assertTrue((root / "Design-Demo-Round2-261008" / "board.md").is_file())
        self.assertEqual(D.level_of(root / "Design-Demo-Round2-261008"), "Block")
        for bad in ("Insight-Demo", "demo_app", "design-demo"):
            with self.assertRaises(SystemExit):
                D.main(["block", str(root / bad)])

    def test_the_workbench_reads_what_the_scaffold_makes(self):
        R = reader()
        D.run(self.job / "t00_reason-ideas", "reason", "", [])
        D.run(self.job / "t01_d01_reason-first", "generate", "", [])
        self.assertTrue(R.is_ladder(self.block))
        j = R.job(self.job)
        self.assertEqual((j["method"], j["version"], j["inputs"]), ("M04", "m2", "i2"))
        self.assertEqual([d["id"] for d in j["designs"]], ["d01"])
        self.assertEqual(j["reason"]["run"], "run-reason-t00")
        self.assertEqual(j["reason"]["kind"], "hard")          # read from run.yaml, not from the name
        self.assertEqual(j["designs"][0]["drafts"][0]["run"], "run-generate-d01")


class MethodBookScaffoldTest(unittest.TestCase):
    """A Design Method Book beside its Board (JL 261109): book, release, then a Job named by release and inputs."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.design = Path(self.tmp.name) / "Project" / "design"
        self.board = self.design / "Design-Try"
        D.main(["block", str(self.board), "--title", "Try", "--channel", "sms"])
        text = (self.board / "board.md").read_text().replace(
            "goals: []", "goals:\n- id: G01\n  name: confirm-by-reply\n  n: 1\n  signed: ✅ 261109")
        (self.board / "board.md").write_text(text)
        rules = self.board / "design-goal.md"
        rules.write_text(rules.read_text().replace("signed: ''", "signed: ✅ 261109"))
        (self.board / "inputs" / "inputs-v1").mkdir(parents=True)
        self.book = self.design / "DesignMethodBook-Try"
        D.main(["book", str(self.book), "--serves", "design/Design-Try"])
        self.rel = self.book / "j01_M01-goal-only"
        D.main(["method", str(self.rel), "--version", "m2"])
        self.job = self.board / "j01_confirm-by-reply_M01-goal-only-m2_inputs-v1"

    def _sign(self):
        face = self.rel / f"{self.rel.name}.md"
        face.write_text(face.read_text().replace("m2: ''", "m2: ✅ 261109"))

    def test_book_links_its_board_and_freezes_the_version(self):
        self.assertIn("board-kind: design-method-book", (self.book / "board.md").read_text())
        channel = re.search(r"(?m)^channel:.*$", (self.board / "board.md").read_text()).group(0)
        self.assertIn(channel, (self.book / "board.md").read_text())            # the Book takes its Board's channel
        self.assertIn("method-book: design/DesignMethodBook-Try", (self.board / "board.md").read_text())
        self.assertIn("version: m2", (self.rel / "m2.md").read_text())
        D.main(["method", str(self.rel), "--version", "m1"])                 # the same type gains a version
        face = (self.rel / f"{self.rel.name}.md").read_text()
        self.assertIn("  m2: ''", face)
        self.assertIn("  m1: ''", face)
        self.assertTrue((self.rel / "m1.md").is_file())
        with self.assertRaises(SystemExit):                                  # a type is named as it is registered
            D.main(["method", str(self.book / "j02_M02-goal-only"), "--version", "m1"])

    def test_a_job_runs_only_a_signed_version_and_is_named_by_it(self):
        with self.assertRaises(SystemExit):
            D.main(["job", str(self.job), "--goal", "G01"])
        self._sign()
        D.main(["job", str(self.job), "--goal", "G01"])
        face = (self.job / f"{self.job.name}.md").read_text()
        self.assertIn("method: M01 m2", face)
        self.assertIn("inputs: inputs-v1", face)
        D.main(["task", str(self.job), "t00"])
        self.assertTrue((self.job / "t00_reason-ideas").is_dir())
        with self.assertRaises(SystemExit):                                  # M02 is no method type of this Book
            D.main(["job", str(self.board / "j02_confirm-by-reply_M02-overall-performance-m1_inputs-v1"), "--goal", "G01"])
        self.assertEqual(reader().job(self.job)["release"], "M01 m2")


class UpdateOlderBoardTest(unittest.TestCase):
    """design_ladder.py update: an older Board (inputs/i1, jNN_<goal>_<method name>) onto the current names, with its
    Book; a file whose hash a manifest records is never rewritten."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.design = Path(self.tmp.name).resolve() / "design"
        self.board = self.design / "Design-Old"
        old = self.board / "j01_confirm-by-reply_goal-only"
        (self.board / "inputs" / "i1").mkdir(parents=True)
        (old / "inputs").mkdir(parents=True)
        (self.board / "board.md").write_text("---\nboard-kind: design-board\nchannel: sms\n---\n# Old\n\nJob j01_confirm-by-reply_goal-only on i1.\n")
        task = self.board / "inputs" / "i1" / "task.md"
        task.write_text("The task, frozen with i1.\n")
        import hashlib
        sha = hashlib.sha256(task.read_bytes()).hexdigest()[:12]
        (self.board / "inputs" / "i1" / "manifest.yaml").write_text(f"version: i1\nfiles:\n- path: task.md\n  sha256: {sha}\n")
        (old / f"{old.name}.md").write_text("---\ngoal: G01 · confirm-by-reply\nmethod: M01 m2\ninputs: i1\nstate: open\n---\n# Job\n")
        (old / "inputs" / "task.md").symlink_to("../../inputs/i1/task.md")

    def test_dry_run_changes_nothing_and_apply_renames_and_builds_the_book(self):
        D.main(["update", str(self.board)])
        self.assertTrue((self.board / "j01_confirm-by-reply_goal-only").is_dir())
        D.main(["update", str(self.board), "--apply"])
        job = self.board / "j01_confirm-by-reply_M01-goal-only-m2_inputs-v1"
        self.assertIn("inputs: inputs-v1", (job / f"{job.name}.md").read_text())
        self.assertEqual((job / "inputs" / "task.md").read_text(), "The task, frozen with i1.\n")   # hashed: its words stay
        self.assertIn("version: inputs-v1", (self.board / "inputs" / "inputs-v1" / "manifest.yaml").read_text())
        self.assertIn(job.name + " on inputs-v1", (self.board / "board.md").read_text())
        self.assertIn("method-book: design/DesignMethodBook-SMS", (self.board / "board.md").read_text())
        kind = self.design / "DesignMethodBook-SMS" / "j01_M01-goal-only"
        self.assertIn("  m2: ''", (kind / f"{kind.name}.md").read_text())          # a person signs; update never does
        self.assertTrue((kind / "m2.md").is_file())
        import design_update as U
        self.assertEqual([r[2] for r in U.audit(self.board, lambda m: D.method_card(m)[0])], [0, 0, 0, 0, 1, 0])
        D.main(["update", str(self.board), "--apply"])                              # a second run finds nothing to do
        self.assertEqual(reader().job(job)["release"], "M01 m2")


if __name__ == "__main__":
    unittest.main()
