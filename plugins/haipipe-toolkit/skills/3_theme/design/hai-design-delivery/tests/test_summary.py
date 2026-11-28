"""summary.py: a design Block's one-page summary, from what the Runs wrote, with one design traced."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import summary as S  # noqa: E402

BOARD = """# b01_demo_app · Demo carry-over

board-kind: design-board

## Goals

```yaml
goals:
- id: G01
  aim: <the behaviour to change>
  who: <audience>
  venue: sms
  n: 2
```

## Questions

```yaml
questions:
- id: Q01
  title: Which designs go out?
  report: reports/q01_send/
- id: Q02
  title: Did insight help?
  report: reports/q02_insight/
```
"""


def _job(block: Path, name: str, method: str, state: str, ranking: str = "", signed: str = "", hold: str = "") -> None:
    j = block / name
    (j / "t99_review-whole/runs/run-rank-t99/result").mkdir(parents=True)
    (j / f"{name}.md").write_text(f"---\ngoal: G01\nmethod: {method}\ninputs: i1\nstate: {state}\n---\n\n# {name}\n"
                                  + (f"\n## Hold\n\n{hold}\n" if hold else ""), encoding="utf-8")
    if ranking:
        (j / "t99_review-whole/runs/run-rank-t99/result/ranking.csv").write_text(ranking, encoding="utf-8")
    if signed:
        (j / f"runs/run-release-{name[:3]}").mkdir(parents=True)
        (j / f"runs/run-release-{name[:3]}/run.yaml").write_text(f"status: closed\nsigned: {signed}\n", encoding="utf-8")


class SummaryTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        b = self.block = Path(self.tmp.name) / "b01_demo_app"
        b.mkdir()
        (b / "board.md").write_text(BOARD, encoding="utf-8")
        for q, status in (("q01_send", "partial"), ("q02_insight", "open")):
            (b / "reports" / q).mkdir(parents=True)
            (b / "reports" / q / f"{q}.md").write_text(f"# {q}\nanswers: x\nanswer-status: {status}\n\n## Opening\n\n"
                                                       f"<opening of {q}>\n", encoding="utf-8")
        _job(b, "j01_goal-only", "M01 m2", "open", "rank,design,predicted,why,kept\n1,d02,+5 [-2; +12],<w>,yes\n"
             "2,d01,+4 [-3; +11],<w>,yes\n", signed="<person> 261012 · all 2 at once")
        _job(b, "j02_actionable", "M04 m3", "open", "rank,design,predicted,why,kept\n1,d01,+3.6 pp [+2.0; +4.7],<w>,yes\n",
             signed="<person> 261012 · all 2 at once")
        _job(b, "j03_raw", "M05 m2", "held", hold="Held: it reads row-level data. More detail here.")
        (b / "delivery").mkdir()
        designs = [{"job": "j01", "job_name": "j01_goal-only", "design": "d02", "name": "visit-anchor", "words": "<words a>",
                    "predicted": "+5 [-2; +12]", "against": "the control", "why": "<why a>", "released": "261012"},
                   {"job": "j02", "job_name": "j02_actionable", "design": "d01", "name": "leader", "words": "<words b>",
                    "predicted": "+3.6 pp [+2.0; +4.7]", "against": "the control", "why": "<why b>", "released": "261012"}]
        (b / "delivery/designs.json").write_text(json.dumps({"designs": designs}), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_page_reads_the_runs_and_traces_the_most_certain_design(self):
        html = S.page(self.block, "")
        self.assertIn("Demo carry-over", html)                                  # the title from board.md
        self.assertIn("&lt;opening of q01_send&gt;", html)                      # the bottom line: a partly answered question
        self.assertNotIn("opening of q02_insight", html)                        # an open one is left out
        self.assertIn("Actionable insights", html)                              # method names, not ids
        self.assertIn("Held: it reads row-level data.", html)                   # a held Job's first sentence only
        self.assertNotIn("More detail here", html)
        self.assertIn("Approved by &lt;person&gt; 261012, all 2 at once.", html)  # who, when and how, once
        self.assertIn("&lt;words b&gt;", html)                                  # the narrowest range is traced
        self.assertIn("&lt;why b&gt;", html)
        self.assertNotIn("&lt;words a&gt;", html)                               # and only that one is shown as it reads
        self.assertNotIn("/Users/", html)

    def test_an_example_can_be_named(self):
        html = S.page(self.block, "j01:d02")
        self.assertIn("&lt;words a&gt;", html)
        self.assertNotIn("&lt;words b&gt;", html)


if __name__ == "__main__":
    unittest.main()
