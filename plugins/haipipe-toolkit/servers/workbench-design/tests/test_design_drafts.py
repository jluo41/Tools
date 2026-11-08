"""A design's drafts as the design example exposed them (261108): a revise keeps its draft in its pass
(run-revise-d<NN>/passes/pNN-<MMDD>/design.md), so the Revise view lists it with its words and the step's Out names
the latest draft; a design.md whose words sit in a fenced block with a count note shows the words only, as
release.py's words_of does for the delivery."""
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

from live import design_focus as DF  # noqa: E402
from live import design_reader as R  # noqa: E402
from live import design_views as V  # noqa: E402
import design_fixture as F  # noqa: E402

DRAFT2 = "{SENDER}: draft two words. Reply STOP to opt out."


class Drafts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.block = F.make(self.tmp) / F.BLOCK
        task = next((self.block / "j01_g01_m04").glob("t05_d05_*"))        # a passed design, given one revise pass
        run = task / "runs" / "run-revise-d05"
        (run / "passes" / "p01-1108").mkdir(parents=True)
        (run / "run.yaml").write_text(yaml.safe_dump({"type": "revise", "kind": "soft", "target": "d05", "status": "closed",
                                                      "by": "designer agent"}), encoding="utf-8")
        (run / "passes" / "p01-1108" / "design.md").write_text(f"```text\n{DRAFT2}\n```\n\n40 characters.\n", encoding="utf-8")
        self.task = task

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_a_revise_pass_is_a_draft(self):
        d = R.design(self.task)
        files = V.draft_files(d)
        self.assertEqual([f.parent.name for _, f in files], ["result", "p01-1108"])
        html = V._drafts(d, R.job(self.task.parent), {}, self.tmp)
        self.assertIn("draft 2", html)
        self.assertIn("p01-1108", html)
        self.assertIn("draft two words", html)

    def test_the_revise_step_names_the_latest_draft(self):
        _caption, process, _results = DF.task_view(self.task, self.tmp, "Revise")
        self.assertIn("Draft v2", process)
        self.assertIn("1 revision", process)
        self.assertNotIn("1 revisions", process)
        self.assertNotIn("Draft v3", process)

    def test_an_older_revise_with_a_result_still_counts(self):
        task = next((self.block / "j03_g01_m04").glob("t04_d04_*"))          # the fixture's revise keeps result/
        self.assertEqual(len(V.draft_files(R.design(task))), 2)

    def test_the_reader_gives_the_words(self):
        face = self.task / f"{self.task.name}.md"
        text = face.read_text(encoding="utf-8")
        head, _, rest = text.partition("## Design")
        body, _, tail = rest.partition("## Evaluation")
        face.write_text(head + f"## Design\n\n```text\n{DRAFT2}\n```\n\n40 characters.\n\n## Evaluation" + tail, encoding="utf-8")
        self.assertEqual(R.design(self.task)["message"], DRAFT2)

    def test_the_words_not_the_fence(self):
        self.assertEqual(V.words_of(f"```text\n{DRAFT2}\n```\n\n40 characters."), DRAFT2)
        self.assertEqual(V.words_of("plain words"), "plain words")
        html = V.as_read(f"```text\n{DRAFT2}\n```\n\n40 characters.", "sms")
        self.assertIn("draft two words", html)
        self.assertNotIn("```", html)
        self.assertNotIn("40 characters", html)


if __name__ == "__main__":
    unittest.main()
