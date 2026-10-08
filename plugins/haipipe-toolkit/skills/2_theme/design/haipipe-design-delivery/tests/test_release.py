"""release.py: a Job's kept designs with frozen predictions into its delivery/ and the Block's, never twice."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import release as R  # noqa: E402


def _design(job: Path, k: int, state: str, frozen: str) -> Path:
    t = job / f"t0{k}_d0{k}_option-{k}"
    t.mkdir(parents=True)
    (t / f"{t.name}.md").write_text(f"---\nstate: {state}\nname: option-{k}\n---\n\n# d0{k}\n\n## Design\n\n"
                                    f"<words {k}>\n\n## Evaluation\n\nT0 ✓\n", encoding="utf-8")
    (t / "prediction.yaml").write_text(yaml.safe_dump({"predicted": f"+{k}", "against": "the control",
                                                       "by": "reviewer agent", "frozen": frozen}))
    return t


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "b01_demo_app"
        self.job = self.block / "j01_g01_m04"
        self.job.mkdir(parents=True)
        (self.job / "j01_g01_m04.md").write_text("---\ngoal: G01\nmethod: M04 m2\ninputs: i2\nstate: open\n---\n\n# j01\n")
        _design(self.job, 1, "kept", "draft")
        _design(self.job, 2, "kept", "draft")
        _design(self.job, 3, "dropped", "draft")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_draft_prediction_is_refused_without_freeze(self):
        with self.assertRaises(SystemExit):
            R.release(self.job)
        self.assertFalse((self.job / "delivery" / "designs.json").exists())

    def test_a_ranked_job_is_not_released_before_its_ranking_is_projected(self):
        job = self.block / "j02_g01_m04"
        job.mkdir(parents=True)
        (job / "j02_g01_m04.md").write_text("---\ngoal: G01\nmethod: M04 m2\ninputs: i2\nstate: open\n---\n\n# j02\n")
        (job / "t99_review-whole" / "runs" / "run-rank-t99" / "result").mkdir(parents=True)
        for k in (1, 2, 3):
            _design(job, k, "passed", "draft")
        with self.assertRaises(SystemExit):                    # passed, not kept: the ranking was never projected
            R.release(job, freeze="261007")
        self.assertFalse((job / "delivery" / "designs.json").exists())

    def test_placeholder_words_are_never_released_and_nothing_is_half_written(self):
        face = self.job / "t02_d02_option-2" / "t02_d02_option-2.md"
        face.write_text(face.read_text().replace("<words 2>", "<the design, word for word>"))
        with self.assertRaises(SystemExit):                    # d02's face was never projected
            R.release(self.job, freeze="261007")
        self.assertEqual(str(yaml.safe_load((self.job / "t01_d01_option-1" / "prediction.yaml").read_text())["frozen"]),
                         "draft")                              # d01 was checked, not frozen: nothing half written
        self.assertFalse((self.job / "delivery" / "designs.json").exists())

    def test_release_writes_job_and_block_delivery_once(self):
        R.release(self.job, freeze="261007")
        R.release(self.job)                                      # again: the states are released now, so nothing new
        designs = json.loads((self.job / "delivery" / "designs.json").read_text())["designs"]
        self.assertEqual([(d["job"], d["design"]) for d in designs], [("j01", "d01"), ("j01", "d02")])
        self.assertEqual(designs[0]["words"], "<words 1>")
        self.assertEqual(designs[0]["pins"], {"goal": "G01", "method": "M04 m2", "inputs": "i2"})
        self.assertEqual(designs[0]["released"], "261007")
        block = json.loads((self.block / "delivery" / "designs.json").read_text())["designs"]
        self.assertEqual(len(block), 2)
        self.assertIn("state: released", (self.job / "t01_d01_option-1" / "t01_d01_option-1.md").read_text())
        self.assertIn("state: dropped", (self.job / "t03_d03_option-3" / "t03_d03_option-3.md").read_text())
        self.assertEqual(str(yaml.safe_load((self.job / "t01_d01_option-1" / "prediction.yaml").read_text())["frozen"]),
                         "261007")
        self.assertIn("## j01 · d02", (self.block / "delivery" / "designs.md").read_text())

    def test_a_ui_design_carries_its_last_judged_screen(self):
        render = self.job / "t01_d01_option-1" / "runs" / "run-verify-d01-v1" / "result" / "render"
        render.mkdir(parents=True)
        (render / "screen-v1.png").write_bytes(b"png")
        out = R.release(self.job, freeze="261007")
        self.assertEqual(out[0]["screen"], "screens/d01.png")
        self.assertTrue((self.job / "delivery" / "screens" / "d01.png").is_file())


if __name__ == "__main__":
    unittest.main()
