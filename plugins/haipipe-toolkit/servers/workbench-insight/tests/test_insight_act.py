"""A person's own actions on the insight screens (insight_act.py, b11 s12, 261023): CHECK a page, sign a Job's close.
Each writes what an agent's Run would (the page's check: line, the Job's state, a pass of its soft Run, by: a person)
and nothing at all when a gate is not met."""
from __future__ import annotations

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

from live import frame  # noqa: E402
from live import insight_act as A  # noqa: E402
from live import insight_plan_c as P  # noqa: E402
from live import insight_views as V  # noqa: E402
from live.insight_theme import THEME  # noqa: E402
import plan_c_fixture as F  # noqa: E402


def front(md: Path) -> dict:
    return yaml.safe_load(md.read_text(encoding="utf-8").split("---")[1]) or {}


class InsightActTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.open = self.board / "j04_prototype-p2_data-demov3"          # open: its Runs planned, no page written
        self.closed = self.board / "j03_prototype-p2_data-demov2"        # closed: every page checked
        self.task = self.open / "t03_K01_question-c"
        self.page = self.task / f"{self.task.name}.md"
        A.set_front(self.page, {"answer-status": "answered", "answer": "<one line>"})

    def tearDown(self):
        self.tmp.cleanup()

    def rel(self, p: Path) -> str:
        return p.relative_to(self.root).as_posix()

    def check(self, verdict="pass", why="", **more):
        return A.act(self.root, {"action": "check", "task": self.rel(self.task), "verdict": verdict, "why": why,
                                 "attest": True, **more})

    def test_a_person_passes_a_page(self):
        before = front(self.page)
        code, res = self.check()
        self.assertEqual(code, 200, res)
        after = front(self.page)
        self.assertRegex(after["check"], r"^✅ \d{6} · a person$")
        self.assertEqual({k: v for k, v in after.items() if k != "check"}, {k: v for k, v in before.items() if k != "check"})
        card = yaml.safe_load((self.task / "runs" / "run-check-t03" / "run.yaml").read_text())
        self.assertEqual((card["by"], card["verdict"], len(card["passes"])), ("a person", "pass", 1))   # the planned Run, its pass
        self.assertNotRegex((self.task / "runs" / "run-check-t03" / "run.yaml").read_text(), r"/(Users|home)/")

    def test_a_returned_page_goes_back_to_write_with_its_reason(self):
        self.assertEqual(self.check("return")[0], 400)                       # a reason is asked for
        code, res = self.check("return", "the B cut's interval is not cited")
        self.assertEqual(code, 200, res)
        self.assertTrue(front(self.page)["check"].startswith("↩ "))
        f = V._work_facts(P.job(self.open))
        self.assertIn(self.task.name, {t["name"] for t in f["returned"]})
        self.assertIn(self.task.name, {t["name"] for t in f["unwritten"]})
        page = frame.render(THEME, self.root, self.open, "Work Details", "3 · Write")
        self.assertIn("Returned by CHECK", page)

    def test_nothing_is_written_without_its_gate(self):
        untouched = self.page.read_text()
        card = (self.task / "runs" / "run-check-t03" / "run.yaml").read_text()          # the planned Run, untouched
        self.assertEqual(A.act(self.root, {"action": "check", "task": self.rel(self.task), "verdict": "pass"})[0], 400)
        self.assertEqual(A.act(self.root, {"action": "check", "task": self.rel(self.task), "verdict": "pass",
                                           "attest": True}, read_only=True)[0], 403)
        self.assertEqual(A.act(self.root, {"action": "check", "task": "../../etc", "verdict": "pass", "attest": True})[0], 400)
        other = self.open / "t01_D01_question-a"                          # not written yet
        self.assertEqual(A.act(self.root, {"action": "check", "task": self.rel(other), "verdict": "pass",
                                           "attest": True})[0], 409)
        frozen = self.closed / "t03_K01_question-c"                        # its Job is closed
        self.assertEqual(A.act(self.root, {"action": "check", "task": self.rel(frozen), "verdict": "pass",
                                           "attest": True})[0], 409)
        self.assertEqual(self.page.read_text(), untouched)
        self.assertEqual((self.task / "runs" / "run-check-t03" / "run.yaml").read_text(), card)
        self.assertFalse((self.task / "runs" / "run-check-t03" / "passes").exists())

    def test_a_page_a_person_wrote_goes_to_another_checker(self):
        A._pass(self.task, "write", "t03", "haipipe-insight-knowledge", "none", "written by a person", "", [], {})
        self.assertEqual(self.check()[0], 409)

    def test_the_close_waits_on_every_step_then_a_person_signs_it(self):
        code, res = A.act(self.root, {"action": "close", "job": self.rel(self.open), "attest": True})
        self.assertEqual(code, 409)
        self.assertIn("waits on", res["err"])
        self.assertEqual(front(self.open / f"{self.open.name}.md")["state"], "open")
        # a Job whose every step is done, still open: the person signs and it closes
        A.set_front(self.closed / f"{self.closed.name}.md", {"state": "open"})
        import shutil
        shutil.rmtree(self.closed / "runs" / "run-close-j03")
        page = frame.render(THEME, self.root, self.closed, "Work Details", "6 · Close")
        self.assertIn('data-post="/_board/insight-act"', page)
        code, res = A.act(self.root, {"action": "close", "job": self.rel(self.closed), "attest": True})
        self.assertEqual(code, 200, res)
        face = front(self.closed / f"{self.closed.name}.md")
        self.assertEqual(face["state"], "closed")
        self.assertRegex(face["signed"], r"^✅ \d{6}$")
        card = yaml.safe_load((self.closed / "runs" / "run-close-j03" / "run.yaml").read_text())
        self.assertEqual((card["status"], card["by"]), ("closed", "a person"))
        self.assertRegex(card["signed"], r"^✅ \d{6} · a person, in the workbench$")
        self.assertEqual(A.act(self.root, {"action": "close", "job": self.rel(self.closed), "attest": True})[0], 409)

    def test_the_screen_offers_each_action_where_it_belongs(self):
        page = frame.render(THEME, self.root, self.open, "Work Details", "4 · Check")
        self.assertIn("check it", page)
        self.assertIn('data-fields="attest why"', page)
        close = frame.render(THEME, self.root, self.open, "Work Details", "6 · Close")
        self.assertIn("it waits on", close)
        self.assertIn("disabled>Sign the close", close)


if __name__ == "__main__":
    unittest.main()
