"""project_draft.py: a design's newest draft into its face and elements.yaml; its verdict into its state."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "haipipe-design" / "scripts"))
sys.path.insert(0, str(HERE.parents[1] / "haipipe-design" / "tests"))
import design_ladder as D  # noqa: E402
import project_draft as P  # noqa: E402
from ladder_kit import ready  # noqa: E402


class ProjectDraftTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        block = ready(Path(self.tmp.name) / "designs" / "b01_demo_app", n=2)
        job = block / "j01_g01_m04"
        D.main(["job", str(job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"])
        D.main(["task", str(job), "d01", "reason-first"])
        self.task = job / "t01_d01_reason-first"
        gen = D.run(self.task, "generate", "", [])
        (gen / "result" / "design.md").write_text("<draft one>\n")
        (gen / "result" / "elements.yaml").write_text("- element: opening\n  words: <one>\n  from: goal\n")

    def tearDown(self):
        self.tmp.cleanup()

    def face(self):
        return (self.task / f"{self.task.name}.md").read_text()

    def verify(self, k, status):
        run = D.run(self.task, "verify", "", [])
        self.assertEqual(run.name, f"run-verify-d01-v{k}")
        card = yaml.safe_load((run / "run.yaml").read_text())
        card.update({"status": status, "by": "reviewer agent", "tests": {"T0": "✓", "T1": "✓" if status == "passed" else "✗"}})
        (run / "run.yaml").write_text(yaml.safe_dump(card, allow_unicode=True))

    def test_draft_verdict_revise_verdict(self):
        P.main(["draft", str(self.task)])
        self.assertIn("<draft one>", self.face())
        self.assertIn("state: verify", self.face())
        self.assertIn("words: <one>", (self.task / "elements.yaml").read_text())
        with self.assertRaises(SystemExit):                    # v1 not written yet
            P.main(["verdict", str(self.task)])
        self.verify(1, "failed")
        P.main(["verdict", str(self.task)])
        self.assertIn("state: revise", self.face())
        rev = D.run(self.task, "revise", "", [])
        (rev / "passes" / "p01-1007").mkdir(parents=True)
        (rev / "passes" / "p01-1007" / "design.md").write_text("<draft two>\n")
        P.main(["draft", str(self.task)])
        self.assertIn("<draft two>", self.face())
        self.assertIn("draft: 2", self.face())
        with self.assertRaises(SystemExit):                    # v1 judged draft 1, not this one
            P.main(["verdict", str(self.task)])
        self.verify(2, "passed")
        P.main(["verdict", str(self.task)])
        self.assertIn("state: passed", self.face())
        self.assertIn("v2 (reviewer agent)", self.face())


if __name__ == "__main__":
    unittest.main()
