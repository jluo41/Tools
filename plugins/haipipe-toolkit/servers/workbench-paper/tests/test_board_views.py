"""A paper Board's Report and Work views (board_views.py, b16 s32 and s33): every view is two bands, each numbered from
1; Report reads RESULTS first and Work PROCESS first; Work's RESULTS is Report's, section for section; the phone rules
come after the base rules they change. Placeholders only: the Board is written into a temp folder, never a real paper."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import board_views, ui_parts  # noqa: E402

FLOW = """# s03 · Paper dataflow

**Topic:** <the data> go in; <the tables> come out.

**Stage:** shaping


Open
----

1. <an open point>
"""
STORY = """# s02 · Story

**Stage:** shaping

### 7 · Task Roadmap

| T | work | where | state | what it gives | feeds |
|---|---|---|---|---|---|
| T0 | <a Run> | b11.j25.t01 | ⬜ waiting for JL | <its tables> | E1 |
| T1 | <a Run> | b11.j25.t02 | ✅ done | <its tables> | E2 |
"""


def board(tmp: Path) -> Path:
    b = tmp / "paper" / "Paper-X"
    for rel, text in (("s02-story-desk-idea/s02-story-desk-idea.md", STORY), ("s03-paper-dataflow/s03-paper-dataflow.md", FLOW)):
        (b / rel).parent.mkdir(parents=True, exist_ok=True)
        (b / rel).write_text(text, encoding="utf-8")
    (b / "j11_writing_v1130_desk" / "t00_summary").mkdir(parents=True)
    (b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\n", encoding="utf-8")
    return b


def bars(html: str) -> list:
    """The band names and the numbered section bars, in page order."""
    return re.findall(r"<h3 class=pb-group>\S+ ([A-Za-z]+)<|<h3 class=fd-h>(\d+) · ", html)


def results(html: str) -> str:
    """The RESULTS band: from its heading to the next band, the dashed rule or the page's scripts."""
    part = html.split("Results</h3>", 1)[1]
    return re.split(r"<h3 class=pb-group>|<hr class=pb-rule>|<script>", part, maxsplit=1)[0]


class BoardViewsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.b = board(self.root)
        md = lambda text, base: text
        self.report = {k: f() for k, (_, f) in board_views.board_report_views(self.b, self.root, md).items()}
        self.work = {k: f() for k, (_, f) in board_views.board_work_views(self.b, self.root, md).items()}

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_band_numbers_from_one(self):
        for key, html in {**self.report, **{f"work-{k}": v for k, v in self.work.items()}}.items():
            seq, band = [], None
            for name, num in bars(html):
                if name:
                    band = name
                    seq.append([])
                elif band:
                    seq[-1].append(int(num))
            for nums in seq:
                self.assertEqual(nums, list(range(1, len(nums) + 1)), key)

    def test_report_reads_results_first_and_work_process_first(self):
        self.assertEqual([n for n, _ in bars(self.report["dataflow"]) if n], ["Results", "Process"])
        self.assertEqual([n for n, _ in bars(self.work["work-dataflow"]) if n], ["Process", "Results"])

    def test_work_results_are_report_results(self):
        for key in self.report:
            self.assertEqual(results(self.report[key]), results(self.work["work-" + key]), key)

    def test_data_flow_process_is_its_plan_and_runs(self):
        work = self.work["work-dataflow"]
        self.assertIn("· 🧭 Plan<", work)
        self.assertIn("use /haipipe-paper-plan", work)
        self.assertIn('class="fd-btn pb-copy"', work)                 # the shared Prompt box (ui_parts.prompt_box)
        self.assertIn("⚙️ Runs to do<", work)               # a title names the step, never a count
        self.assertNotIn(" of 2 open", work)
        self.assertIn("pb-pill you", work)              # T0 waits for you: an orange pill

    def test_phone_rules_come_after_the_base_rules(self):
        css = ui_parts.PB_CSS
        self.assertLess(css.index(".pb-side{display:grid"), css.index(".pb-side{grid-template-columns:1fr}"))
        self.assertLess(css.index(".pb-flow{position:relative"), css.index(".pb-flow{grid-template-columns:1fr}"))


if __name__ == "__main__":
    unittest.main()


class StoryListsTest(unittest.TestCase):
    def test_a_story_that_starts_at_rq0_keeps_its_numbers(self):
        """A setup question RQ0 (haipipe-paper-story) is RQ0, and its narrative item is paired by number, not position."""
        from live import board_read
        body = ("**The story, question by question:**\n0. <a setup question>? set up\n1. <a question>? open\n\n"
                "**The narrative:**\n0. <what RQ0 says>\n1. <what RQ1 says>\n")
        qs, said = board_read._rq_lists(body)
        self.assertEqual([k for k, _ in qs], [0, 1])
        self.assertEqual(said[0], "<what RQ0 says>")
