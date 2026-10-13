"""haipipe-studio job_results.py: one Block topic per Job, drawn from its Runs; the face's words kept on a redraw."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import job_results  # noqa: E402


class JobResultsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project-Example" / "work" / "b01_gsm8k"
        job = self.block / "j11_sft"
        task = job / "t01_trl_sft"
        done = task / "runs" / "r02_sft_small" / "result"
        done.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01 · gsm8k\n")
        (job / "j11_sft.md").write_text("# j11 · gsm8k sft\n\ngoal: lift GSM8K accuracy with SFT\n")
        (task / "t01_trl_sft.md").write_text("t01_trl_sft\n===========\n\nGSM8K-SFT with TRL.\n\ndevelops: a checkpoint\n")
        (done / "runtime.yaml").write_text("status: completed\n")
        (done / "eval.json").write_text(json.dumps({"base": {"acc": 0.26}, "trained": {"acc": 0.41}, "delta_acc": 0.15,
                                                   "config": {"acc": 9}}))
        (task / "runs" / "r01_sft").mkdir()                                     # a shared ticket the Run calls
        (task / "runs" / "r01_sft" / "r01_sft.sh").write_text("#!/usr/bin/env bash\n")
        (task / "runs" / "r02_sft_small" / "r02_sft_small.sh").write_text('exec "$HERE/../r01_sft/r01_sft.sh"\n')
        (task / "runs" / "r03_sft_big").mkdir()                                  # queued: no result yet
        self.job = job

    def tearDown(self):
        self.tmp.cleanup()

    def make(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return job_results.make(self.block, [self.job], "j11-sft-results", "j11 · gsm8k sft: current results")

    def test_a_topic_per_job_in_the_runs_band_at_the_block(self):
        out = self.make()
        topic = out.parent
        self.assertEqual(topic.name, "s21-j11-sft-results")
        self.assertEqual(topic.parents[1], self.block.resolve())                        # the Block's studio, not the Job's
        for name in ("s21-j11-sft-results.md", "s21-j11-sft-results.excalidraw", "s21-j11-sft-results.png",
                     "build_s21_j11_sft_results.py"):
            self.assertTrue((topic / name).is_file(), name)
        self.assertIn("Results", (self.block / "studio" / "_groups.txt").read_text())

    def test_values_pair_before_and_after_and_skip_config_and_delta(self):
        rows = job_results.job_rows(self.block, self.job, {})
        runs = {r["name"]: r for r in rows[0]["runs"]}
        self.assertEqual(runs["r02_sft_small"]["values"], ["acc 26.0% → 41.0%"])
        self.assertEqual(runs["r03_sft_big"]["mark"], "⬜")
        self.assertNotIn("r01_sft", runs)                                         # the shared ticket is named, not a Run
        self.assertEqual(rows[0]["shared"], ["r01_sft"])
        self.assertEqual(rows[0]["title"], "GSM8K-SFT with TRL.")

    def test_the_face_keeps_its_words_and_names_picks(self):
        topic = self.make().parent
        face = topic / f"{topic.name}.md"
        text = face.read_text().replace(
            "    j11_sft: ''", "    j11_sft: 'SFT lifts accuracy from 26% to 41%.'").replace(
            "  show: {}", "  show:\n    t01_trl_sft/r02_sft_small:\n"
                          "      - {label: test acc, at: ['eval.json:base.acc', 'eval.json:trained.acc'], fmt: pct}\n"
                          "      - {label: missing, at: 'eval.json:nope'}")
        face.write_text(text)
        with contextlib.redirect_stdout(io.StringIO()):
            job_results.draw(topic)
        after = face.read_text()
        self.assertIn("SFT lifts accuracy from 26% to 41%.", after)
        self.assertIn("test acc 26.0% → 41.0%", after)                           # the ledger reads the picks
        self.assertIn("❓ missing: not in the result", after)
        drawn = (topic / f"{topic.name}.excalidraw").read_text()
        self.assertIn("SFT lifts accuracy", drawn)


if __name__ == "__main__":
    unittest.main()
