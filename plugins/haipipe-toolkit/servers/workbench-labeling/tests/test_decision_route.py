"""The building Task's decision door (labeling.py labeling_decision_act; b15 j01 s58 C2, s03 CONTRACTS.md v2):
save a draft and submit answers to a published report; every refusal leaves the lane unchanged.

A placeholder Project with one building Task (task-type: labeling-building) and the engine's synthetic demo report
published into its lane. Skipped when the engine's decision store is absent."""
from __future__ import annotations

import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import labeling as LB  # noqa: E402
from test_labeling_theme import project, task, items_task  # noqa: E402

STORE = LB._meaning_store_module()
DEMO = (Path(STORE.__file__).with_name("fixtures") / "decision_report_demo.json") if STORE else None


@unittest.skipUnless(STORE is not None and DEMO is not None and DEMO.is_file(), "the decision store is absent")
class DecisionDoorTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root, self.block, legacy = project(self.temp.name)
        self.job = legacy.parent
        self.items = items_task(self.job)
        self.building = task(self.job, "t03_demo_building", "labeling-building")
        self.lane = self.building / "labeling"
        self.report = json.loads(DEMO.read_text())
        STORE.publish_report(self.lane, copy.deepcopy(self.report), "test")
        self.card = self.report["cards"][0]
        self.base = {"path": str(self.building.relative_to(self.root)), "report_id": self.report["report_id"],
                     "report_revision": self.report["report_revision"], "human_id": "Reviewer One", "attest": True}

    def tearDown(self):
        self.temp.cleanup()

    def handler(self, origin=None):
        class Handler(LB.LabelingMixin):
            def send_response(self, status): self.status = status
            def send_header(self, *args): pass
            def end_headers(self): pass
            def reply(self, status, body): self.status, self.body = status, body
        h = Handler()
        h.root, h.headers, h.wfile = self.root, {"Host": "example.test"}, io.BytesIO()
        if origin:
            h.headers["Origin"] = origin
        return h

    def answers(self, kind="chosen"):
        a = {"kind": kind, "comment": "  only for adults  "}
        if kind == "chosen":
            a["option_id"] = self.card["options"][0]["option_id"]
        return {self.card["decision_id"]: a}

    def files(self):
        return sorted(p.relative_to(self.lane).as_posix() for p in self.lane.rglob("*") if p.is_file()
                      and not p.name.endswith(".lock"))

    def test_draft_saves_then_refuses_a_stale_revision(self):
        h = self.handler("http://example.test")
        code, body = h.labeling_act(dict(self.base, action="decision_draft_save", answers=self.answers(),
                                         expected_draft_revision=0))
        self.assertEqual(code, 200, body)
        self.assertEqual(body["draft"]["draft_revision"], 1)
        before = self.files()
        code, body = h.labeling_act(dict(self.base, action="decision_draft_save", answers=self.answers("defer"),
                                         expected_draft_revision=0))
        self.assertEqual(code, 409, body)
        self.assertEqual(self.files(), before)

    def test_submit_needs_confirmation_then_is_idempotent(self):
        h = self.handler()
        sub = dict(self.base, action="decision_feedback_submit", answers=self.answers(), request_id="req-0001-demo")
        code, body = h.labeling_act(sub)
        self.assertEqual(code, 400, body)                       # no "I confirm" tick
        code, first = h.labeling_act(dict(sub, confirmed=True))
        self.assertEqual(code, 200, first)
        code, again = h.labeling_act(dict(sub, confirmed=True))
        self.assertEqual((code, again["receipt"]), (200, first["receipt"]))
        self.assertEqual(len(STORE.list_submissions(self.lane, self.report["report_id"])), 1)
        code, body = h.labeling_act(dict(sub, confirmed=True, answers=self.answers("defer")))
        self.assertEqual(code, 409, body)                       # the same request id, other answers
        bundle = STORE.list_submissions(self.lane, self.report["report_id"])[0]
        self.assertIn("  only for adults  ", json.dumps(bundle))   # a comment is kept exactly as written

    def test_refusals_write_nothing(self):
        before = self.files()
        ok = dict(self.base, action="decision_draft_save", answers=self.answers(), expected_draft_revision=0)
        cases = [
            (self.handler("https://other.test"), ok, 403),
            (self.handler(), dict(ok, path="../outside"), 400),
            (self.handler(), dict(ok, path=str(self.items.relative_to(self.root))), 400),   # an items Task
            (self.handler(), dict(ok, attest=False), 400),
            (self.handler(), dict(ok, human_id="  "), 400),
            (self.handler(), dict(ok, answers=[]), 400),
            (self.handler(), dict(ok, report_revision="one"), 400),
            (self.handler(), dict(ok, answers={"no-such-card": {"kind": "defer"}}), 422),
            (self.handler(), dict(ok, report_id="no-such-report"), 404),
        ]
        for h, payload, want in cases:
            code, body = h.labeling_act(payload)
            self.assertEqual(code, want, (payload, body))
            self.assertFalse(body["ok"])
        self.assertEqual(self.files(), before)

    def test_a_read_only_workbench_refuses(self):
        h = self.handler()
        h.server = type("S", (), {"read_only": True})()
        code, body = h.labeling_act(dict(self.base, action="decision_draft_save", answers=self.answers(),
                                         expected_draft_revision=0))
        self.assertEqual(code, 403, body)


if __name__ == "__main__":
    unittest.main()
