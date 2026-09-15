"""Regression coverage for the retired Draft feedback lane and its replacement.

Run from any directory: python -m unittest discover -s <Page>/tests.
"""
from __future__ import annotations

import http.client
import json
import re
import sys
import tempfile
import threading
import unittest
from pathlib import Path

PAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PAGE_ROOT))

from live.outline import OutlineMixin, plan_card  # noqa: E402
from live.outline_feedback import (feedback_items, paragraphs, run_rows,  # noqa: E402
                                   save_feedback)
from src.page_workspace import load_page  # noqa: E402
from src.standalone_server import create_server  # noqa: E402


PLAN = """# S-test · outline v1.1
outline-version: v1.1
approved: ✅ JL 260910 0900 · in chat: "approve"
arc: Physicians differ, so the design must separate them.

## C1 · Introduction
### C1.P1 · Problem · S1 to S2
- B1 · [Phenomenon] Physicians differ in their prescribing decisions
  Note: first point
  Evidence: none · test fixture
  Draft: Physicians differ in how they prescribe.
- B2 · [Consequence] The difference matters for patients
  Note: second point
  Evidence: none · test fixture
  Draft: That difference reaches patients.
### C1.P2 · Design · S3 to S4
- B1 · [Method] The design isolates the physician
  Note: third point
  Evidence: none · test fixture
  Draft: The design holds the visit fixed.

## C2 · Data
### C2.P3 · Sources · S5 to S6
- B1 · [Data] Medicare claims define the visits
  Note: fourth point
  Evidence: none · test fixture
  Draft: Medicare claims define each visit.
"""

TICKET = """---
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1-C1.P2
paragraphs: P01-P02
result: results/rp-para-01_P01-P02
run: rp-para-01_P01-P02
---

# rp-para-01_P01-P02

- Goal: settle the first two paragraphs.
"""

RUNTIME = """run: rp-para-01_P01-P02
family: page
operation: interactive-writing
interaction: human-feedback
target: C1.P1-C1.P2
paragraphs: P01-P02
ticket: runs/rp-para-01_P01-P02.md
result: results/rp-para-01_P01-P02
status: complete
version: v001
step: s001
version_file: results/rp-para-01_P01-P02/v001.md
version_sha256: abc
worker:
  kind: skill
  name: haipipe-writing
started_at: '2026-09-14T06:58:28Z'
finished_at: '2026-09-14T07:23:49Z'
supersedes: null
failure: null
"""

CLOSED_V001 = """Run: rp-para-01_P01-P02
Version: v001
State: closed
Prior Version: none

## Step s001

### Human feedback

```text
Source: current Codex conversation; message id not supplied
Reviewed output: initial state
Mode: local-edit
```

#### Original request

```text
Make the first sentence shorter.
```

#### Feedback F01

- Target: `C1.P1.B1`
- Human comment: Make the first sentence shorter.
- Agent interpretation: shorten S1

### Saved result

```text
State: waiting-for-feedback
```

#### C1.P1

Physicians differ in how they prescribe. That difference reaches patients.

#### Changes

| Feedback | Disposition | Target | Change and reason |
|---|---|---|---|
| F01 | applied | C1.P1.B1 | Shortened S1. |

## Version closure

### Human close

JL: "P01 and P02 are settled."
"""

WORKING = """# rp-para-01_P01-P02 · working state

- Current version/step: `v001/s001`.
- State: `complete`.
- Open feedback: none.
- Next action: continue with the next Run.
"""


class FeedbackFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="outline-feedback-")
        self.addCleanup(self.tmp.cleanup)
        self.folder = Path(self.tmp.name) / "S-test"
        (self.folder / "outline").mkdir(parents=True)
        self.page = self.folder / "S-test.md"
        self.page.write_text("# S-test\npage-type: section\n\n## Opening\nA page.\n\n"
                             "## Content\n### 1 · Introduction\nPhysicians differ in how they prescribe.\n\n"
                             "## Aims\n- ⬜ A1.1 · Settle the design.\n", encoding="utf-8")
        self.plan = self.folder / "outline" / "S-test-outline-v1.1.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        (self.folder / "runs").mkdir()
        (self.folder / "runs" / "rp-para-01_P01-P02.md").write_text(TICKET, encoding="utf-8")
        self.results = self.folder / "results" / "rp-para-01_P01-P02"
        self.results.mkdir(parents=True)
        (self.results / "runtime.yaml").write_text(RUNTIME, encoding="utf-8")
        (self.results / "v001.md").write_text(CLOSED_V001, encoding="utf-8")
        (self.results / "working.md").write_text(WORKING, encoding="utf-8")

    def payload(self, **over):
        base = dict(action="feedback", paragraph="C1.P2", kind="explore", author="JL",
                    comment="Open with the visit, not the physician.", feedback_id="fb-0123456789ab")
        base.update(over)
        return base


class ReadSideTest(FeedbackFixture):
    def test_paragraph_index_and_run_coverage(self):
        paras = paragraphs(self.page)
        self.assertEqual(list(paras), ["C1.P1", "C1.P2", "C2.P3"])
        self.assertEqual(paras["C1.P2"]["brief"], "Design")
        self.assertEqual(paras["C1.P1"]["bullets"], ["C1.P1.B1", "C1.P1.B2"])
        rows = run_rows(self.page, {1, 2, 3})
        self.assertEqual(rows[0]["covers"], {1, 2})
        self.assertEqual(rows[0]["status"], "complete")

    def test_historical_items_show_under_their_paragraph(self):
        items = feedback_items(self.page)
        self.assertEqual(len(items["C1.P1"]), 1)
        self.assertEqual(items["C1.P1"][0]["disposition"], "applied")
        self.assertFalse(items["C1.P1"][0]["pending"])
        self.assertEqual(items["C1.P2"], [])

    def test_draft_space_renders_scratch_controls_not_feedback(self):
        card = plan_card(self.page)
        self.assertIn('data-scratch-scope="section"', card)
        self.assertIn('data-scratch-scope="subsection"', card)
        self.assertIn('data-scratch-scope="paragraph"', card)
        self.assertIn('data-scratch-target="C1.P2"', card)
        self.assertIn("Finish Scratch", card)
        self.assertNotIn("paragraph-feedback", card)
        self.assertNotIn("Save note", card)
        self.assertNotIn("data-fb-add=", card)

    def test_read_only_render_has_no_scratch_writer(self):
        card = plan_card(self.page, read_only=True)
        self.assertNotIn("paragraph-feedback", card)
        self.assertNotIn("data-scratch-form", card)
        self.assertNotIn("data-scratch-scope=", card)
        self.assertNotIn("Finish Scratch", card)


class WriteSideTest(FeedbackFixture):
    def test_finished_covering_run_is_reopened_in_a_new_version(self):
        before_plan = self.plan.read_bytes()
        before_page = self.page.read_bytes()
        before_v001 = (self.results / "v001.md").read_bytes()
        result, err = save_feedback(self.page, self.payload())
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], "rp-para-01_P01-P02")
        self.assertEqual((result["run_version"], result["step"], result["feedback"]), ("v002", "s001", "F01"))
        v002 = (self.results / "v002.md").read_text(encoding="utf-8")
        self.assertIn("Prior Version: v001.md · SHA-256 ", v002)
        self.assertIn("## Step s001", v002)
        self.assertIn("### Human feedback", v002)
        self.assertNotIn("### Saved result", v002)
        self.assertIn("- Id: fb-0123456789ab", v002)
        self.assertIn("- Target: `C1.P2` · P02", v002)
        self.assertIn("- Kind: explore", v002)
        self.assertIn("- Human comment: Open with the visit, not the physician.", v002)
        self.assertIn("- Agent interpretation: pending", v002)
        # The plan, the Page, and the sealed journal are untouched.
        self.assertEqual(self.plan.read_bytes(), before_plan)
        self.assertEqual(self.page.read_bytes(), before_page)
        self.assertEqual((self.results / "v001.md").read_bytes(), before_v001)
        runtime = (self.results / "runtime.yaml").read_text(encoding="utf-8")
        self.assertRegex(runtime, r"(?m)^status: waiting-for-feedback$")
        self.assertRegex(runtime, r"(?m)^version: v002$")
        self.assertRegex(runtime, r"(?m)^step: s001$")
        self.assertRegex(runtime, r"(?m)^supersedes: results/rp-para-01_P01-P02/v001.md$")
        self.assertRegex(runtime, r"(?m)^version_sha256: [0-9a-f]{64}$")
        self.assertRegex(runtime, r"(?m)^  name: haipipe-writing$")   # nested keys survive
        working = (self.results / "working.md").read_text(encoding="utf-8")
        self.assertIn("- Current version/step: v002/s001", working)
        self.assertIn("- Open feedback: F01 · explore on C1.P2 · from Draft Space by JL", working)
        # The read side sees the pending item at once.
        items = feedback_items(self.page)["C1.P2"]
        self.assertEqual([(i["label"], i["pending"], i["disposition"]) for i in items],
                         [("F01", True, "pending")])
        self.assertEqual(result["pending"], 1)
        self.assertIn("fb-pending", result["list_html"])

    def test_second_note_joins_the_pending_step_and_retry_is_idempotent(self):
        save_feedback(self.page, self.payload())
        result, err = save_feedback(self.page, self.payload(comment="Also name the five cohorts here.",
                                                            kind="wording", feedback_id="fb-fedcba987654"))
        self.assertIsNone(err, err)
        self.assertEqual((result["run_version"], result["step"], result["feedback"]), ("v002", "s001", "F02"))
        v002 = (self.results / "v002.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^## Step s", v002)), 1)
        self.assertIn("#### Feedback F02", v002)
        self.assertIn("- Kind: wording", v002)
        again, err = save_feedback(self.page, self.payload(comment="Also name the five cohorts here.",
                                                           kind="wording", feedback_id="fb-fedcba987654"))
        self.assertIsNone(err, err)
        self.assertEqual(again["feedback"], "F02")
        self.assertEqual(v002, (self.results / "v002.md").read_text(encoding="utf-8"))
        self.assertEqual(again["count"], 2)

    def test_uncovered_paragraph_allocates_the_next_paragraph_run(self):
        result, err = save_feedback(self.page, self.payload(paragraph="C2.P3", bullet="C2.P3.B1",
                                                            comment="Say which years of claims."))
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], "rp-para-02_P03")
        ticket = (self.folder / "runs" / "rp-para-02_P03.md").read_text(encoding="utf-8")
        self.assertIn("paragraphs: P03", ticket)
        self.assertIn("Mermaid Structure description: P03 · C2.P3 · Sources", ticket)
        v001 = (self.folder / "results" / "rp-para-02_P03" / "v001.md").read_text(encoding="utf-8")
        self.assertIn("Prior Version: none", v001)
        self.assertIn("- Target: `C2.P3.B1` · P03", v001)
        runtime = (self.folder / "results" / "rp-para-02_P03" / "runtime.yaml").read_text(encoding="utf-8")
        self.assertRegex(runtime, r"(?m)^run: rp-para-02_P03$")
        self.assertRegex(runtime, r"(?m)^status: waiting-for-feedback$")
        self.assertTrue((self.folder / "results" / "rp-para-02_P03" / "working.md").is_file())

    def test_open_structure_run_takes_paragraph_notes_before_paragraph_runs_exist(self):
        (self.folder / "runs" / "rp-struct-01.md").write_text(
            "---\nfamily: page\noperation: interactive-writing\ninteraction: human-feedback\n"
            "target: whole Page\nparagraphs: P01-P03\nresult: results/rp-struct-01\nrun: rp-struct-01\n---\n",
            encoding="utf-8")
        struct = self.folder / "results" / "rp-struct-01"
        struct.mkdir()
        (struct / "runtime.yaml").write_text("run: rp-struct-01\nstatus: waiting-for-feedback\nversion: v001\nstep: s002\n",
                                             encoding="utf-8")
        (struct / "v001.md").write_text(
            "Run: rp-struct-01\nVersion: v001\nState: open\n\n## Step s001\n\n### Human feedback\n\nx\n\n"
            "### Saved result\n\ny\n\n## Step s002\n\n### Human feedback\n\nz\n\n### Saved result\n\nw\n",
            encoding="utf-8")
        result, err = save_feedback(self.page, self.payload(paragraph="C2.P3"))
        self.assertIsNone(err, err)
        self.assertEqual((result["run"], result["run_version"], result["step"]), ("rp-struct-01", "v001", "s003"))
        text = (struct / "v001.md").read_text(encoding="utf-8")
        self.assertIn("## Step s003", text)
        self.assertIn("Reviewed output: rp-struct-01 v001/s002", text)

    def test_validation_rejects_bad_input_without_writing(self):
        snapshot = sorted(p.relative_to(self.folder).as_posix() for p in self.folder.rglob("*"))
        for bad in (dict(paragraph="C9.P9"), dict(kind="praise"), dict(author=""),
                    dict(author="A · B"), dict(comment=""), dict(bullet="C1.P1.B1"),
                    dict(paragraph="C1.P1.B1")):
            result, err = save_feedback(self.page, self.payload(**bad))
            self.assertIsNone(result, bad)
            self.assertTrue(err, bad)
        result, err = save_feedback(self.page, self.payload(), read_only=True)
        self.assertIsNone(result)
        self.assertIn("read-only", err)
        self.assertEqual(snapshot, sorted(p.relative_to(self.folder).as_posix() for p in self.folder.rglob("*")))

    def test_outline_mixin_rejects_the_retired_feedback_action(self):
        handler = OutlineMixin()
        handler.target = lambda p: (self.page.name, self.folder)
        result, err = handler.plug_outline(self.payload())
        self.assertIsNone(result)
        self.assertIn("Draft comments are removed", err)
        result, err = handler.plug_outline({"action": "edit-preview", "path": "", "file": ""})
        self.assertIsNone(result)
        self.assertIn("read-only", err)

    def test_outline_mixin_dispatches_a_scratch_action(self):
        handler = OutlineMixin()
        handler.target = lambda p: (self.page.name, self.folder)
        result, err = handler.plug_outline({
            "action": "scratch", "phase": "finish", "scope": "paragraph",
            "target": "C1.P2", "notes": "Explain the design move.",
            "summary": "The paragraph should connect design to the visit.",
        })
        self.assertIsNone(err, err)
        self.assertEqual(result["run"], "rp-scratch-01_C1.P2")
        self.assertEqual(result["version"], "v001")
        self.assertRegex(self.plan.read_text(encoding="utf-8"),
                         r"(?m)^- Status: closed$")


class StandaloneWireTest(FeedbackFixture):
    def setUp(self):
        super().setUp()
        self.context = load_page(self.page)
        self.server = create_server(self.context)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop)
        self.origin = "http://127.0.0.1:%d" % self.server.server_port

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(self, method, path, payload=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=10)
        headers = {"Origin": self.origin, "Content-Type": "application/json"}
        try:
            connection.request(method, path, body=json.dumps(payload) if payload is not None else None,
                               headers=headers)
            response = connection.getresponse()
            return response.status, response.read().decode("utf-8", "replace")
        finally:
            connection.close()

    def test_draft_space_get_then_post_writes_a_scratch_run(self):
        code, body = self.request("GET", "/_board/outline?path=&file=%s&lens=div" % self.page.name)
        self.assertEqual(code, 200)
        self.assertIn('data-scratch-scope="paragraph"', body)
        self.assertNotIn("Save note", body)
        scratch = {
            "action": "scratch", "phase": "finish", "scope": "paragraph",
            "target": "C1.P2", "notes": "Start with the visit.",
            "summary": "The paragraph should foreground the visit.",
            "file": self.page.name, "path": "",
        }
        code, body = self.request("POST", "/_board/outline", scratch)
        self.assertEqual(code, 200, body)
        result = json.loads(body)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["run"], "rp-scratch-01_C1.P2")
        scratch_result = self.folder / "results" / "rp-scratch-01_C1.P2"
        self.assertTrue((scratch_result / "v001.md").is_file())
        self.assertIn("Human confirmed the Scratch Summary.",
                      (scratch_result / "v001.md").read_text(encoding="utf-8"))
        code, body = self.request("GET", "/_board/outline?path=&file=%s&lens=div" % self.page.name)
        self.assertIn("Scratch ✓", body)


if __name__ == "__main__":
    unittest.main()
