from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from check_idea_block import check_block


class IdeaBlockTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        (Path(self.temp.name) / "AGENTS.md").write_text("Temporary validation workspace.\n")
        self.root = Path(self.temp.name) / "b01_direction"
        self.root.mkdir()
        (self.root / "board.md").write_text("# Direction\n\nboard-kind: ideation-block\n")
        self.index = {"version": 1, "kind": "ideation-block", "direction": "Robustness",
                      "question": "When do gains survive?", "scope": "Bounded fixture", "ideas": []}
        self.add_job("j01_calibration", "i01")
        self.add_job("j02_missingness", "i09")

    def write(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(yaml.safe_dump(data))

    def add_job(self, name, identity):
        job = self.root / name
        self.write(job / "ideation.yaml", {"version": 1, "kind": "ideation-unit",
                   "layout": "idea-job", "block": "../ideation.yaml", "idea_id": identity,
                   "address": "b01." + name.split("_", 1)[0]})
        (job / f"{name}.md").write_text("# Idea\n\ngoal: Answer this question\n")
        self.write(job / f"cards/{identity}_idea.yaml",
                   {"kind": "idea-card", "id": identity, "canonical_id": identity})
        self.write(job / "workflow/generate/g01_provisional.yaml", {"kind": "ideation-generate"})
        self.index["ideas"].append({"job": name, "idea_id": identity})
        self.write(self.root / "ideation.yaml", self.index)

    def codes(self, **kwargs):
        return {f.code for f in check_block(self.root, **kwargs)}

    def test_multiple_jobs_keep_independent_semantic_ids(self):
        self.assertEqual(self.codes(), set())

    def test_idea_block_in_paper_is_named_idea_slug(self):
        named = self.root.parent / "Idea-Robustness"      # JL 261124: paper/Idea-<Slug>/, no ideation/ world
        self.root.rename(named)
        self.root = named
        self.assertIn("job-address", self.codes())         # its Jobs still say b01.jNN
        for name in ("j01_calibration", "j02_missingness"):
            f = named / name / "ideation.yaml"
            data = yaml.safe_load(f.read_text())
            data["address"] = "Idea-Robustness." + name.split("_", 1)[0]
            self.write(f, data)
        self.assertEqual(self.codes(), set())

    def test_two_cards_cannot_hide_inside_one_idea_job(self):
        self.write(self.root / "j01_calibration/cards/i02_second.yaml",
                   {"kind": "idea-card", "id": "i02", "canonical_id": "i02"})
        self.assertIn("idea-ownership", self.codes())

    def test_duplicate_id_or_unindexed_job_is_rejected(self):
        self.index["ideas"][1]["idea_id"] = "i01"
        self.write(self.root / "ideation.yaml", self.index)
        self.assertIn("duplicate-idea", self.codes())
        (self.root / "j03_unindexed").mkdir()
        self.assertIn("job-index", self.codes())

    def test_task_is_not_another_portfolio(self):
        task = self.root / "j01_calibration/t01_falsification"
        task.mkdir()
        self.assertIn("task-face", self.codes())
        (task / "t01_falsification.md").write_text("# What would refute this?\n\ntask-type: ideation\n")
        self.assertEqual(self.codes(), set())
        self.write(task / "ideation.yaml", {"kind": "ideation-unit"})
        self.assertIn("task-portfolio", self.codes())

    def test_soft_assessment_cannot_claim_a_scientific_result(self):
        task = self.root / "j01_calibration/t01_falsification"
        task.mkdir()
        (task / "t01_falsification.md").write_text("# What would refute this?\n\ntask-type: ideation\n")
        run = task / "runs/run-assess-claim"
        self.write(run / "run.yaml", {"run": run.name, "kind": "soft", "type": "assess", "ticket": run.name + ".md"})
        (run / (run.name + ".md")).write_text("# Assess the frozen claim\n")
        self.assertEqual(self.codes(), set())
        (run / "result").mkdir()
        self.assertIn("assessment-result", self.codes())

    def test_shared_audits_recognize_ideation_without_work_only_debt(self):
        base = SCRIPTS.parents[2]
        commands = [
            [base / "task/hai-task/scripts/check_task_tree.py", self.root],
            [base / "project/hai-project/scripts/ladder.py", "audit", self.root],
        ]
        for command in commands:
            with self.subTest(command=str(command[0])):
                result = subprocess.run([sys.executable, *map(str, command)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                if Path(command[0]).name == "ladder.py":
                    totals = re.findall(r"\b(?:block|job|task|run)\s+\d+\s+ok\s+\d+\s+debt\s+(\d+)\s+failed\s+(\d+)", result.stdout)
                    self.assertTrue(totals, result.stdout)
                    self.assertTrue(all(pair == ("0", "0") for pair in totals), result.stdout)
                self.assertNotIn("not in the ladder", result.stdout.lower())

    def test_structure_never_substitutes_for_scientific_gate(self):
        self.assertEqual(self.codes(), set())
        self.assertIn("missing-field", self.codes(gate="generate", job="j01_calibration"))

    def test_parent_or_job_address_must_match(self):
        path = self.root / "j01_calibration/ideation.yaml"
        data = yaml.safe_load(path.read_text())
        data["address"] = "b01.j02"
        data["block"] = "../../unrelated.yaml"
        self.write(path, data)
        self.assertTrue({"job-address", "idea-ownership"}.issubset(self.codes()))

    def test_missing_block_and_malformed_index_report_findings(self):
        self.assertTrue(check_block(self.root / "missing"))
        self.index["ideas"] = [None, {"job": "../j01_elsewhere"}]
        self.write(self.root / "ideation.yaml", self.index)
        self.assertTrue({"idea-index", "job-address"}.issubset(self.codes()))

    def test_cli_is_read_only_and_unknown_job_fails(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = subprocess.run([sys.executable, str(SCRIPTS / "check_idea_block.py"),
                                 str(self.root), "--json"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("unknown-job", self.codes(job="j99_missing"))
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
