"""A Job's card in the Block's Jobs view (design_views._preview), as the design example's partly-done Job exposed it
(261108): t00's tile shows its reason Run's own status, never "closed" while the Run is still running, and a Job with
no design Task yet says when its Tasks open instead of an empty table."""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import design_canvas as C  # noqa: E402
from live import design_reader as R  # noqa: E402
from live import design_views as V  # noqa: E402
import design_fixture as F  # noqa: E402


class JobPreview(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp
        self.block = F.make(self.tmp) / F.BLOCK
        self.href = lambda space="", sub="", path=None: "#"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_running_reason_and_no_design_task_yet(self):
        job = self.block / "j05_g02_m01"
        card = job / "t00_reason-ideas" / "runs" / "run-reason-t00" / "run.yaml"
        data = yaml.safe_load(card.read_text(encoding="utf-8"))
        data.update(status="running", finished_at="")
        card.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        for task in job.glob("t*_d*_*"):
            shutil.rmtree(task)
        html = V._preview(R.job(job), self.href, self.root)
        t00_row = html.split("reason ideas", 1)[1].split("</tr>", 1)[0]
        self.assertIn(V._st("running"), t00_row)
        self.assertNotIn(V._st("closed"), t00_row)
        self.assertNotIn("Nothing here yet", html)
        self.assertIn("open after t00's ideas pass the fence check (run-open-designs-j05)", html)

    def test_closed_reason_and_designs_unchanged(self):
        html = V._preview(R.job(self.block / "j01_g01_m04"), self.href, self.root)
        t00_row = html.split("reason ideas", 1)[1].split("</tr>", 1)[0]
        self.assertIn(V._st("closed"), t00_row)
        self.assertIn("as it reads", html)                  # the design table, one row per design
        self.assertNotIn("open after t00's ideas", html)

    def test_a_placeholder_release_sign_never_reads_as_a_person(self):
        job = self.block / "j03_g01_m04"                                    # released in the fixture
        card = job / "runs" / "run-release-j03" / "run.yaml"
        data = yaml.safe_load(card.read_text(encoding="utf-8"))
        self.assertIn("signed by a person", C._approved_words(R.job(job)))
        data.update(signed="✅ 261106 · placeholder sign on the example, no person signed")
        card.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        words = C._approved_words(R.job(job))
        self.assertEqual(words, "✅ placeholder sign 261106, no person signed")


if __name__ == "__main__":
    unittest.main()
