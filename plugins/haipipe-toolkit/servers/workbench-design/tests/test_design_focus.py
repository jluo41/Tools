"""The design theme on the focus page (design_focus.py, b12 j01 s51 to s58): the Block, a Job and each Task type in the
cells' letters, Report the Results only, Work ⚙️ Process then 📊 Results with your signs first; a Task never asks you."""
from __future__ import annotations

import re
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

from live import design_focus as D  # noqa: E402
from live import focus_page as FP  # noqa: E402
from live.design_theme import THEME  # noqa: E402
import design_fixture as F  # noqa: E402
from test_design_act import set_state  # noqa: E402

GROUPS = re.compile(r"<h3 class=pb-group>(.*?)</h3>")
HEADS = re.compile(r"<h3 class=fd-h>(.*?)</h3>")


class DesignFocusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = F.make(self.root) / F.BLOCK
        self.job = self.block / "j03_g01_m04"
        self.tasks = sorted(p for p in self.job.iterdir() if p.is_dir() and p.name.startswith("t"))

    def tearDown(self):
        self.tmp.cleanup()

    def names(self, folder: Path, section: str) -> list:
        return [n for n, _ in D.views(folder, self.root, section).values()]

    def test_each_level_has_the_cells_letters(self):
        self.assertEqual(D.level_of(self.block), "Block")
        self.assertEqual(self.names(self.block, "work"), ["Summary", "Goals", "Jobs", "Rounds", "Methods"])
        self.assertEqual(self.names(self.job, "report"), ["Setup", "Ideas", "Designs", "Ranking", "Release"])
        by_kind = {D.R.kind_of(t): self.names(t, "work") for t in self.tasks}
        self.assertEqual(by_kind["t00"], ["Inputs", "Chains", "Ideas", "Fence check"])
        self.assertEqual(by_kind["design"], ["Draft", "Verify", "Revise", "State"])
        self.assertEqual(by_kind["t99"], ["Rank", "Coverage", "Kept"])
        self.assertEqual(D.views(self.root, self.root, "work"), {})              # not a design page: the base page stays

    def test_report_is_its_sections_work_is_process_then_results(self):
        for folder in (self.block, self.job, *self.tasks):
            for key, (_n, build) in D.views(folder, self.root, "report").items():
                html = build()
                self.assertEqual(GROUPS.findall(html), [], (folder.name, key))          # Report: its sections only
                self.assertRegex(HEADS.findall(html)[0], r"^1 · ", (folder.name, key))
                self.assertNotIn("Waits on you", html)
            for key, (_n, build) in D.views(folder, self.root, "work").items():
                html = build()
                self.assertEqual(GROUPS.findall(html), ["⚙️ Process", "📊 Results"], (folder.name, key))
                self.assertNotIn("Traceback", html)

    def test_a_job_ready_to_release_waits_on_you(self):
        for k, t in enumerate(t for t in self.tasks if D.R.kind_of(t) == "design"):    # t99 ranked, three kept, not signed
            if k < 3:
                set_state(t / f"{t.name}.md", "kept")
                pred = yaml.safe_load((t / "prediction.yaml").read_text())
                (t / "prediction.yaml").write_text(yaml.safe_dump({**pred, "frozen": "draft"}, allow_unicode=True))
        for r in ("run-release-j03", "run-freeze-predictions-j03"):
            shutil.rmtree(self.job / "runs" / r)
        job = D.views(self.job, self.root, "work")["work-release"][1]()
        self.assertEqual(HEADS.findall(job)[0], "1 · 🙋 Waits on you")
        self.assertIn('data-post="/_board/design-ladder-act"', job)            # the sign, on the Release view
        block = D.views(self.block, self.root, "work")["work-summary"][1]()
        self.assertIn("Review and approve", block)
        self.assertIn("j03_g01_m04", block.split("📊 Results")[0])

    def test_a_released_job_waits_on_you_to_close(self):
        self.assertTrue(D.V._approved(D.R.job(self.job))[0])                         # the fixture's j03 is released
        job = D.views(self.job, self.root, "work")["work-setup"][1]()
        self.assertEqual(HEADS.findall(job)[0], "1 · 🙋 Waits on you")                # the close is a person's sign
        block = D.views(self.block, self.root, "work")["work-summary"][1]()
        self.assertIn("Close", block.split("📊 Results")[0])
        self.assertNotIn("Nothing waits on you", block)

    def test_a_task_never_asks_you(self):
        for t in self.tasks:
            for _n, build in D.views(t, self.root, "work").values():
                html = build()
                self.assertNotIn("waiting for you", html, t.name)
                self.assertNotIn('data-post=', html, t.name)

    def test_the_focus_page_shows_them(self):
        page = FP.render(THEME, self.root, self.job, "work", "work-designs")
        self.assertIn("Each design", page)
        self.assertIn(">Setup<", page)
        self.assertIn("Summary", FP.render(THEME, self.root, self.block, "report", ""))


if __name__ == "__main__":
    unittest.main()
