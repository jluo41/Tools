from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "regroup_bjtr.py"
SPEC = importlib.util.spec_from_file_location("regroup_bjtr", SCRIPT)
assert SPEC and SPEC.loader
regroup_bjtr = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = regroup_bjtr
SPEC.loader.exec_module(regroup_bjtr)


class RegroupBjtrTest(unittest.TestCase):
    def make_bank(self, root: Path) -> Path:
        project = root / "Project-Test"
        bank = project / "discoveries"
        for number, slug in ((1, "retrieval_map"), (2, "safety_review")):
            job = bank / f"b{number:02d}_{slug}" / f"j01_{slug}_inquiry"
            task = job / "t01_primary_question"
            task.mkdir(parents=True)
            (task / "t01_primary_question.md").write_text("# Page\n", encoding="utf-8")
            (task / "discovery.yaml").write_text(
                f"""version: 6
kind: discovery
address: b{number:02d}.j01.t01
address_compact: b{number:02d}j01t01
discovery_type: topic-summary
block:
  id: b{number:02d}
  slug: {slug}
  title: Old block {number}
job:
  id: j01
  slug: {slug}_inquiry
  title: Job {number}
task:
  id: t01
  slug: primary_question
  title: Primary question
page: t01_primary_question.md
status: planned
question: What is known?
""",
                encoding="utf-8",
            )
            (bank / f"b{number:02d}_{slug}" / "_index.md").write_text(
                f"# Group {number}\n", encoding="utf-8"
            )
        (project / "README.md").write_text(
            "See discoveries/b02_safety_review and b02.j01.t01.\n",
            encoding="utf-8",
        )
        return bank

    def test_regroup_preserves_groups_as_jobs_and_rewrites_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            bank = self.make_bank(Path(temp))
            moves = regroup_bjtr.plan_bank(
                bank, "test_evidence_board", "Test evidence board"
            )
            self.assertEqual(2, len(moves))
            self.assertEqual("j02_safety_review_inquiry", moves[1].new_job)
            blocks, jobs, tasks, refs = regroup_bjtr.apply_bank(moves)
            self.assertEqual((1, 2, 2), (blocks, jobs, tasks))
            self.assertGreaterEqual(refs, 1)
            new_job = (
                bank
                / "b01_test_evidence_board"
                / "j02_safety_review_inquiry"
            )
            self.assertTrue((new_job / "_index.md").is_file())
            manifest = (
                new_job / "t01_primary_question" / "discovery.yaml"
            ).read_text(encoding="utf-8")
            self.assertIn("address: b01.j02.t01", manifest)
            self.assertIn("address_compact: b01j02t01", manifest)
            self.assertIn("slug: test_evidence_board", manifest)
            self.assertIn("title: \"Test evidence board\"", manifest)
            readme = (bank.parent / "README.md").read_text(encoding="utf-8")
            self.assertIn(
                "discoveries/b01_test_evidence_board/j02_safety_review_inquiry",
                readme,
            )
            self.assertIn("b01.j02.t01", readme)


if __name__ == "__main__":
    unittest.main()
