"""project_predictions.py: t99's ranking into each design Task's prediction.yaml and state; a frozen prediction stays."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import project_predictions as P  # noqa: E402


def _face(task: Path, state: str) -> None:
    task.mkdir(parents=True)
    (task / f"{task.name}.md").write_text(f"---\nstate: {state}\nname: x\n---\n\n# {task.name}\n", encoding="utf-8")


class ProjectPredictionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.job = Path(self.tmp.name) / "b01_demo_app" / "j01_g01_m04"
        for k, state in ((1, "passed"), (2, "passed"), (3, "passed"), (4, "verify")):
            _face(self.job / f"t0{k}_d0{k}_option-{k}", state)
        frozen = self.job / "t03_d03_option-3" / "prediction.yaml"
        frozen.write_text("predicted: +z\nagainst: the control\nby: someone\nfrozen: '261001'\n", encoding="utf-8")
        run = self.job / P.RANK
        (run / "result").mkdir(parents=True)
        (run / "run.yaml").write_text("run: run-rank-t99\nkind: hard\ntype: rank\nstatus: closed\nby: reviewer agent\n")
        (run / "result" / "ranking.csv").write_text("rank,design,predicted,why,kept\n1,d02,+x [lo; hi],<why>,yes\n"
                                                    "2,d01,+y [lo; hi],<why>,no\n3,d03,+w,<why>,yes\n4,d04,+v,<why>,no\n")

    def tearDown(self):
        self.tmp.cleanup()

    def _read(self, d):
        task = next(self.job.glob(f"t*_{d}_*"))
        return yaml.safe_load((task / "prediction.yaml").read_text()), (task / f"{task.name}.md").read_text()

    def test_rows_become_draft_predictions_and_states(self):
        P.project(self.job)
        pred, face = self._read("d02")
        self.assertEqual(pred, {"predicted": "+x [lo; hi]", "against": "the control", "by": "reviewer agent",
                                "frozen": "draft"})
        self.assertIn("state: kept", face)
        self.assertIn("state: dropped", self._read("d01")[1])

    def test_a_frozen_prediction_and_an_unpassed_design_are_left_alone(self):
        P.project(self.job)
        pred, face = self._read("d03")
        self.assertEqual(str(pred["frozen"]), "261001")
        self.assertIn("state: passed", face)
        pred4, face4 = self._read("d04")
        self.assertEqual(pred4["frozen"], "draft")
        self.assertIn("state: verify", face4)

    def test_an_open_rank_is_refused_and_dry_writes_nothing(self):
        P.project(self.job, dry=True)
        self.assertFalse((self.job / "t02_d02_option-2" / "prediction.yaml").exists())
        card = self.job / P.RANK / "run.yaml"
        card.write_text(card.read_text().replace("status: closed", "status: open"))
        with self.assertRaises(SystemExit):
            P.project(self.job)


if __name__ == "__main__":
    unittest.main()
