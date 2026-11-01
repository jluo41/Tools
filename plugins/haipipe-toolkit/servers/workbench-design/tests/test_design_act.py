"""A person's Review and approve on a design Job's Delivery (design_ladder_act.py, b12 s12, 261023): release.py's own
dry run decides whether it is ready; one tick and one sign freeze the kept designs' predictions and release them, and
the two soft Runs say `by: a person`. Nothing is written when release.py would refuse."""
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

from live import design_ladder_act as A  # noqa: E402
from live import frame  # noqa: E402
from live.design_theme import THEME  # noqa: E402
import design_fixture as F  # noqa: E402


def set_state(md: Path, state: str) -> None:
    text = md.read_text(encoding="utf-8")
    md.write_text(text.replace("state: " + yaml.safe_load(text.split("---")[1])["state"], f"state: {state}", 1),
                  encoding="utf-8")


class DesignApproveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = F.make(self.root) / F.BLOCK
        self.job = self.block / "j03_g01_m04"
        # the Job as it stands before the person's sign: t99 ranked, its top designs kept, their predictions a draft
        for k, t in enumerate(sorted(p for p in self.job.iterdir() if p.name.startswith("t") and "_d" in p.name)):
            if k < 3:
                set_state(t / f"{t.name}.md", "kept")
                pred = yaml.safe_load((t / "prediction.yaml").read_text())
                (t / "prediction.yaml").write_text(yaml.safe_dump({**pred, "frozen": "draft"}, allow_unicode=True))
        for r in ("run-release-j03", "run-freeze-predictions-j03"):
            shutil.rmtree(self.job / "runs" / r)
        self.kept = sorted(p for p in self.job.iterdir() if p.name.startswith("t") and "_d" in p.name)[:3]

    def tearDown(self):
        self.tmp.cleanup()

    def approve(self, **more):
        return A.act(self.root, {"action": "approve", "job": self.job.relative_to(self.root).as_posix(), "attest": True,
                                 **more})

    def test_the_delivery_shows_what_one_sign_releases(self):
        page = frame.render(THEME, self.root, self.job, "Delivery", "")
        self.assertIn("🙋 Review and approve", page)
        self.assertIn('data-post="/_board/design-ladder-act"', page)
        self.assertIn("freezes the 3 predictions", page)

    def test_a_person_approves_once(self):
        code, res = self.approve()
        self.assertEqual(code, 200, res)
        self.assertEqual(len(res["released"]), 3)
        for t in self.kept:
            self.assertRegex(str(yaml.safe_load((t / "prediction.yaml").read_text())["frozen"]), r"^\d{6}$")
            self.assertIn("state: released", (t / f"{t.name}.md").read_text())
        for r in ("run-freeze-predictions-j03", "run-release-j03"):
            card = yaml.safe_load((self.job / "runs" / r / "run.yaml").read_text())
            self.assertEqual((card["status"], card["by"]), ("closed", "a person"))
            self.assertRegex(card["signed"], r"^✅ \d{6} · a person, in the workbench$")
        page = frame.render(THEME, self.root, self.job, "Delivery", "")
        self.assertIn("✓ released", page)
        self.assertEqual(self.approve()[0], 409)                         # nothing new to release
        summary = frame.render(THEME, self.root, self.block, "Audience Report", "Summary")
        self.assertIn("approved ✅", summary)                           # the sign, no name

    def test_nothing_is_written_when_release_would_refuse(self):
        self.assertEqual(A.act(self.root, {"action": "approve", "job": self.job.relative_to(self.root).as_posix()})[0], 400)
        self.assertEqual(A.act(self.root, {"action": "approve", "job": "nowhere", "attest": True})[0], 400)
        self.assertEqual(A.act(self.root, {"action": "approve", "attest": True,
                                           "job": self.job.relative_to(self.root).as_posix()}, read_only=True)[0], 403)
        t = self.kept[0]
        (t / "prediction.yaml").write_text(yaml.safe_dump({"against": "the control", "frozen": "draft"}))
        before = {p: p.read_text() for p in self.job.rglob("*") if p.is_file()}
        code, res = self.approve()
        self.assertEqual(code, 409)
        self.assertIn("no predicted effect", res["err"])
        self.assertEqual({p: p.read_text() for p in self.job.rglob("*") if p.is_file()}, before)
        self.assertIn("not ready", frame.render(THEME, self.root, self.job, "Delivery", ""))


if __name__ == "__main__":
    unittest.main()
