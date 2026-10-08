"""haipipe-report: the Question │ Work │ Report check and the report drawing, on a synthetic Block."""
import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import build_report_drawing  # noqa: E402
import check_report  # noqa: E402

BOARD = """# b01 · <topic>

board-kind: task-block
spine: <one sentence>
close: <what closes it>

## Questions

```yaml
questions:
  - id: Q01
    title: First topic
    question: <the question>
  - id: Q02
    title: Second topic
    question: <the question>
```
"""


def report(qid: str, status: str, evidence: str = "", opening: str = "<the answer>", extra: str = "") -> str:
    return textwrap.dedent(f"""\
        # {qid} · <title>

        answers: {qid}
        answer-status: {status}
        {extra}
        ## Opening

        {opening}

        ## Content

        ### Answer

        <reasoning>

        ### Evidence

        {evidence}

        ### Limits

        <limits>

        ### Next

        <next>
        """)


class Block:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "b01_topic"
        self.root.mkdir()
        (self.root / "board.md").write_text(BOARD)

    def write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p


class CheckReportTest(unittest.TestCase):
    def setUp(self):
        self.b = Block()

    def tearDown(self):
        self.b.tmp.cleanup()

    def found(self):
        rows, findings = check_report.rows(self.b.root)
        return {r["id"]: r for r in rows}, findings

    def test_a_register_without_reports_is_open_and_clean(self):
        rows, findings = self.found()
        self.assertEqual([rows[q]["status"] for q in ("Q01", "Q02")], ["open", "open"])
        self.assertEqual(findings, [])

    def test_a_job_and_a_task_link_by_answers_and_a_need_id(self):
        self.b.write("j01_job/j01_job.md", "# j01 · <job>\n\nanswers: Q01\n")
        self.b.write("j01_job/t01_task/t01_task.md", "# t01 · <task>\n\nanswers: Q01.E2, Q02\n")
        rows, findings = self.found()
        self.assertEqual(rows["Q01"]["work"], ["j01_job", "j01_job/t01_task"])
        self.assertEqual(rows["Q02"]["work"], ["j01_job/t01_task"])
        self.assertEqual(findings, [])

    def test_answers_naming_an_unknown_question_is_an_error(self):
        self.b.write("j01_job/j01_job.md", "# j01\n\nanswers: Q09\n")
        _, findings = self.found()
        self.assertTrue(any(l == "error" and "Q09" in t for l, t in findings))

    def test_the_walk_open_partial_answered_and_nothing_else(self):
        self.b.write("reports/q01_first/q01_first.md", report("Q01", "done"))
        _, findings = self.found()
        self.assertTrue(any("is not one of open · partial · answered" in t for _, t in findings))

    def test_answered_needs_an_opening_and_evidence(self):
        self.b.write("reports/q01_first/q01_first.md", report("Q01", "answered", opening=""))
        _, findings = self.found()
        texts = " | ".join(t for l, t in findings if l == "error")
        self.assertIn("Opening states no answer", texts)
        self.assertIn("Evidence links nothing", texts)

    def test_answered_with_evidence_and_read_time_is_clean(self):
        self.b.write("reports/q01_first/q01_first.md",
                     report("Q01", "answered", "- [the result](../../j01_job/t01_task/runs/r01_x/result/metrics.json)",
                            extra="results-read: 2026-01-01T00:00:00+00:00"))
        rows, findings = self.found()
        self.assertEqual(rows["Q01"]["status"], "answered")
        self.assertEqual(findings, [])

    def test_partial_without_results_read_warns(self):
        self.b.write("reports/q02_second/q02_second.md", report("Q02", "partial"))
        _, findings = self.found()
        self.assertIn(("warn", "reports/q02_second/q02_second.md: partial, but results-read: is not recorded"),
                      findings)

    def test_a_report_must_name_its_own_question(self):
        self.b.write("reports/q01_first/q01_first.md", report("Q01", "open").replace("answers: Q01", "answers: Q02"))
        _, findings = self.found()
        self.assertTrue(any("answers: does not name Q01" in t for _, t in findings))

    def test_an_unregistered_report_is_a_row_and_an_error(self):
        self.b.write("reports/q03_third/q03_third.md", report("Q03", "open"))
        rows, findings = self.found()
        self.assertIn("Q03", rows)
        self.assertTrue(any("no register row names Q03" in t for _, t in findings))

    def test_a_comments_batch_is_a_report_like_any_other(self):
        board = BOARD.replace("```\n", "  - id: Q03\n    title: Reviewer comments\n    group: comments\n```\n", 1)
        self.b.write("board.md", board)
        self.b.write("reports/q03_comments-0101/q03_comments-0101.md",
                     report("Q03", "open", extra="page-type: comments"))
        rows, findings = self.found()
        self.assertEqual(rows["Q03"]["group"], "comments")
        self.assertEqual(rows["Q03"]["report"], "reports/q03_comments-0101/q03_comments-0101.md")
        self.assertEqual(findings, [])

    def test_a_broken_register_is_a_finding_not_a_crash(self):
        self.b.write("board.md", BOARD.replace("title: First topic", "title: 'it's broken'"))
        rows, findings = self.found()
        self.assertEqual(rows, {})
        self.assertIn("does not parse", findings[0][1])

    def test_the_cli_exits_1_on_an_error(self):
        self.b.write("reports/q01_first/q01_first.md", report("Q01", "done"))
        out = subprocess.run([sys.executable, str(SCRIPTS / "check_report.py"), str(self.b.root), "--json"],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 1)
        self.assertEqual(json.loads(out.stdout)["rows"][0]["status"], "done")


def drawing(frames):
    els = []
    for i, name in enumerate(frames):
        fid = f"s-frame{i}"
        els.append({"id": fid, "type": "frame", "name": name, "x": i * 1000, "y": 0, "width": 800, "height": 400})
        els.append({"id": f"s-text{i}", "type": "text", "x": i * 1000 + 20, "y": 20, "width": 100, "height": 20,
                    "text": f"seed {i}", "fontSize": 20, "frameId": fid})
        els.append({"id": f"mine{i}", "type": "text", "x": i * 1000 + 40, "y": 60, "width": 100, "height": 20,
                    "text": "a red note", "fontSize": 20, "frameId": fid, "strokeColor": "#e03131"})
    return {"type": "excalidraw", "version": 2, "elements": els, "files": {}}


class BuildReportDrawingTest(unittest.TestCase):
    def setUp(self):
        self.b = Block()
        self.b.write("studio/s01-topic/s01-topic.excalidraw", json.dumps(drawing(["1 · First", "2 · Second"])))
        self.page = self.b.write("reports/q01_first/q01_first.md", report("Q01", "partial") + textwrap.dedent("""
            ## Figures

            ```yaml
            figures:
            - from: ../../studio/s01-topic/s01-topic.excalidraw
              frame: "2 · Second"
              caption: the second frame
            ```
            """))

    def tearDown(self):
        self.b.tmp.cleanup()

    def test_a_figure_is_copied_without_the_persons_red_notes(self):
        out = build_report_drawing.build(self.page.parent, 3000)
        els = json.loads(out.read_text())["elements"]
        self.assertEqual([e["name"] for e in els if e["type"] == "frame"], ["Q01 · report", "Fig 1 · 2 · Second"])
        texts = [e["text"] for e in els if e["type"] == "text"]
        self.assertIn("seed 1", texts)
        self.assertNotIn("seed 0", texts)
        self.assertNotIn("a red note", texts)

    def test_the_check_sees_a_stale_drawing(self):
        _, findings = check_report.rows(self.b.root)
        self.assertTrue(any("not built yet" in t for _, t in findings))
        build_report_drawing.build(self.page.parent, 3000)
        _, findings = check_report.rows(self.b.root)
        self.assertFalse(any("drawing" in t for _, t in findings))

    def test_the_old_address_is_retired(self):
        old = SCRIPTS.parents[2] / "display" / "excalidraw-report" / "ref" / "build_report_drawing.py"
        self.assertFalse(old.exists())


if __name__ == "__main__":
    unittest.main()
