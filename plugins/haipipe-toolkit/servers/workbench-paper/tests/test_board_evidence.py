"""The paper Board's Evidence view (board_evidence.py, haipipe-paper-evidence 0.7.0): a value or citation Task shows
its newest Run's ledger page tall, with a pop-out, and its headline as its status; an evidence Job with no Task says
which script makes them. Placeholders only, in a temp folder."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import board_evidence, board_results  # noqa: E402


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def value_job(root: Path, source: str = "a,b\n1,2\n") -> Path:
    """A value Job: one Run holding a copied file, its source, a printed value, and a built tables.json."""
    write(root / "work" / "b01_x" / "result" / "t.csv", source)
    job = root / "paper" / "Paper-X" / "j02_evidence_value"
    res = job / "t01_v" / "runs" / "r07_any_name" / "result"
    write(res / "k" / "t.csv", "a,b\n1,2\n")
    write(res / "k" / "SOURCE.txt", "copied from work/b01_x/result\n")
    write(res / "values.json", json.dumps({"V_one": {"text": "1", "says": "one", "source": "b01 · t.csv"}}))
    built = job / "t02_tables" / "runs" / "r01_build" / "result"
    write(built / "tables.json", json.dumps({"tabs": [{"slug": "s", "title": "Readable topic", "line": "its line", "story": "A story.",
          "values": ["V_"], "method": ["Step one."], "tables": [{"key": [], "from": "t01_v/k/t.csv", "file": "s.csv", "cols": ["a"], "rows": []}]}]}))
    return job


class ValueTabsTest(unittest.TestCase):
    def test_tabs_read_any_run_name_and_check_the_source(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            job = value_job(root)
            (title, line, panel), = board_evidence.value_tabs(job, root)
            self.assertEqual((title, line), ("Readable topic", "its line"))
            self.assertIn("✅ current", panel)
            self.assertIn("How this table is made", panel)
            self.assertNotRegex(panel, r"<details[^>]*\bopen")
            self.assertIn("<b>1</b>: one", panel)              # the numbered value, from a Run not called r01_collect_values

    def test_a_changed_or_gone_source_says_so(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            job = value_job(root, "a,b\n9,9\n")
            self.assertIn("❗ source changed", board_evidence.value_tabs(job, root)[0][2])
            (root / "work" / "b01_x" / "result" / "t.csv").unlink()
            self.assertIn("❗ source gone", board_evidence.value_tabs(job, root)[0][2])

    def test_sections_are_read_not_typed(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            job = value_job(root)
            self.assertIn('"sections": ""', board_evidence.value_tabs(job, root)[0][2].replace("&quot;", '"'))
            write(job.parent / "j11_writing_v1" / "t03_results" / "draft" / "t03-draft-v1.md", "As shown, V_one holds.\n")
            self.assertIn('"sections": "t03_results"', board_evidence.value_tabs(job, root)[0][2].replace("&quot;", '"'))

    def test_no_tables_json_falls_back_to_a_tab_per_task(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            b = root / "paper" / "Paper-X"
            write(b / "j02_evidence_value" / "t01_values-main" / "t01_values-main.md", "# t01\n\nlabel: Main values\n")
            self.assertIsNone(board_evidence.value_tabs(b / "j02_evidence_value", root))
            html, n = board_results._evidence_kinds(b, root, ("Values",))
            self.assertEqual(n, 1)
            self.assertIn("Main values", html)
            self.assertNotIn("vt-panel", html)


class EvidenceViewTest(unittest.TestCase):
    def test_ledger_pages_and_an_empty_job(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            b = root / "paper" / "Paper-X"
            write(b / "board.md", "# Paper-X\n\nboard-kind: paper-board\n")
            (b / "j11_writing_v1130_desk" / "t00_summary").mkdir(parents=True)
            t = b / "j02_evidence_value" / "t01_values-main"
            write(t / "t01_values-main.md", "# t01_values-main · the main association\n\nlabel: RQ1 · the main association\n"
                                            "status: see runs/r01_collect_values/result/headline.txt\n")
            res = t / "runs" / "r01_collect_values" / "result"
            write(res / "values.html", "<!doctype html><title>x</title><table></table>")
            write(res / "headline.txt", "t01_values-main: 3 values, 2 printed in 2 places (2 match); 1 never printed\n")
            write(b / "j03_evidence_cite" / "j03_evidence_cite.md", "# j03_evidence_cite\n\nstate: open\n")
            label, status, body = board_evidence.evidence_body(t, root)
            self.assertEqual(status, "3 values, 2 printed in 2 places (2 match); 1 never printed")
            self.assertIn("height:max(560px,78vh)", body)
            self.assertIn("⤢ Pop out", body)
            self.assertIn("values.html", body)
            html = board_results.evidence_view(b, root, None)
            self.assertIn("cite_tasks.py gen", html)
            self.assertNotIn("No Tasks yet.</p>", html)


if __name__ == "__main__":
    unittest.main()
