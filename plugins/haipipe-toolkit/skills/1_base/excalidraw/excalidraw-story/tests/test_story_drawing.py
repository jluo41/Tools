"""story_drawing.py on a made-up telling: the questions read in order, their marks, and a drawing that shows them.
Placeholders only, no real project data."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import story_drawing as sd  # noqa: E402

FACE = """s02 · Story: does the demo work
================================

**Tags:** `Story`

**G0:** ⬜ not marked.

### 2 · Pitch

1. **Tension**: a demo tension.
2. **What we do**: a demo design,
   wrapped onto a second line.
3. **The answer so far**: it works ⟦pending E2⟧.
4. **Who cares**: demo readers.

### 3 · Research Questions

**The paper's question**: Does the demo
work?

**The story, question by question** (read in order):

1. Does it start? ✅ It starts.
2. Does it last? ⬜ Not measured.

**The narrative, if the questions are answered** (each step is what the paper can say,
as hypothesized):

1. The demo starts (RQ1).
2. It lasts a week, so it can be used (RQ2).

#### 3.1 · Question 1 · RQ1
- **Name**: Does it start?
- **Research question**: To what extent does the demo start on the first try? (RQ1a: does it start? RQ1b: how fast?)
- **Question**: We start it.
- **Why it matters**: a demo that does not start shows nothing.
- **If answered**: if it starts, the paper can say it works at all.
- **Answer state**: ✅ it starts: 10 of 10 runs.

**Hypotheses**
- **1a** · Starts: it starts · tested by E1

**Potential claims**
- **1a** · C1 · from 1a · It starts: the demo starts.
  - **Now**: ✅

**Potential work**
- **T1** · for 1a

#### 3.2 · Question 2 · RQ2
- **Name**: Does it last?
- **Research question**: Does the demo keep working for a week?
- **Question**: We run it for a week.
- **Why it matters**: a demo that stops is not usable.
- **Answer state**: ⬜ not measured.

**Hypotheses**
- **2a** · Lasts: it lasts · tested by E2

**Potential claims**
- **2a** · C2 · from 1a, 2a · It lasts: the demo lasts a week.
  - **Now**: ⬜ needs a Run

**Potential work**
- **T2** · for 2a

### 5 · Evidence Basis and Boundaries

| E | evidence | source | support state |
|---|---|---|---|
| E1 | it starts | demo.r01 | established |
| E2 | it lasts | no Run | absent |

**We will not claim**:
- that it is fast;
- that it is cheap.

### 7 · Task Roadmap

| T | work | where | state | starts |
|---|---|---|---|---|
| T1 | start it | demo.t01 | done | done |
| T2 | run it a week | demo.t02 | not started | JL starts |

### 9 · Venues

| V | venue | kind | why it fits | leads with | still needs | desk record |
|---|---|---|---|---|---|---|
| V1 | Demo Journal | journal · target | it shows demos | RQ1 | RQ2 run | QBv0-demo |
| V2 | Demo Conference | conference | fast | RQ1 | a desk record | none yet |
"""


class StoryDrawingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.topic = Path(self.tmp.name) / "Paper-Demo" / "studio" / "s02-story-demo-works"
        self.topic.mkdir(parents=True)
        (self.topic / f"{self.topic.name}.md").write_text(FACE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_face_reads_as_its_questions_in_order(self):
        S = sd.read(self.topic)
        self.assertEqual(S["title"], "Does the demo work")
        self.assertEqual(S["question"], "Does the demo work?")                  # wrapped onto two lines
        self.assertEqual([q["rq"] for q in S["qs"]], ["RQ1", "RQ2"])
        self.assertEqual([q["told"] for q in S["qs"]], ["Does it start?", "Does it last?"])
        self.assertEqual(S["qs"][1]["claims"][0]["c"], "C2")              # a claim from two hypotheses still reads
        self.assertEqual(len(S["pitch"]), 4)
        self.assertEqual(len(S["narrative"]), 2)                           # its heading wraps onto a second line
        self.assertEqual(S["qs"][0]["why it matters"], "a demo that does not start shows nothing.")
        self.assertIn("wrapped onto a second line", S["pitch"][1])
        self.assertIn("(pending E2)", S["pitch"][2])                       # the font cannot show ⟦ ⟧
        self.assertEqual(S["refuse"], ["that it is fast;", "that it is cheap."])

    def test_marks_follow_the_face(self):
        S = sd.read(self.topic)
        self.assertEqual(sd.mark(S["qs"][0]["answer state"]), "✅")
        self.assertTrue(sd.missing(S["qs"][1]["answer state"]))
        self.assertEqual((sd.e_mark(S["E"]["E1"]), sd.e_mark(S["E"]["E2"])), ("✅", "⬜"))
        self.assertEqual((sd.t_mark(S["T"]["T1"]), sd.t_mark(S["T"]["T2"])), ("✅", "⬜"))
        self.assertEqual(sd.t_mark({"state": "not done"}), "⬜")            # "done" inside is not done

    def test_the_drawing_shows_every_question_and_what_is_missing(self):
        out = sd.draw(self.topic)
        texts = [e.get("text", "") for e in json.loads(out.read_text())["elements"] if e.get("type") == "text"]
        self.assertTrue(any("RQ1 · Does it start?" in t for t in texts), texts)
        self.assertTrue(any("RQ2 · Does it last?" in t for t in texts))
        self.assertTrue(any("To what extent does the demo start on the first try?" in t for t in texts))   # formal
        self.assertTrue(any("Why it matters: a demo that does not start" in t for t in texts))             # its card
        self.assertTrue(any("If answered: if it starts" in t for t in texts))
        self.assertTrue(any("RQ1a: does it start?" in t for t in texts))                    # sub-questions, card
        self.assertTrue(any("It lasts a week, so it can be used" in t for t in texts))      # the narrative
        frames = [e.get("name", "") for e in json.loads(out.read_text())["elements"] if e.get("type") == "frame"]
        self.assertTrue(any("The narrative, if the questions are answered" in f for f in frames), frames)
        self.assertTrue(any(t.startswith("Act 1") for t in texts))                           # the rows are named
        self.assertTrue(any("V1 · Demo Journal · journal · target" in t for t in texts))      # the venues, as stairs
        self.assertTrue(any(f.startswith("⑦ Where the story could go") or "Where the story could go" in f for f in frames))
        self.assertTrue(any("T2 · run it a week" in t for t in texts))                  # a Run to make
        self.assertTrue(any(t.startswith("1 Run to make") for t in texts))              # one Run, not "1 Runs"
        self.assertFalse(any("JL" in t for t in texts if "Run to make" in t))          # no one person named
        self.assertTrue(any("G0" in t for t in texts))
        self.assertFalse(any("T1 · start it" in t for t in texts))                      # a done Run is not missing
        self.assertTrue(out.with_suffix(".png").is_file())

    def test_a_plan_takes_the_runs_and_dates(self):
        (self.topic.parent / "s03-paper-dataflow").mkdir()                 # haipipe-paper-plan's topic exists
        out = sd.draw(self.topic)
        els = json.loads(out.read_text())["elements"]
        texts = [e.get("text", "") for e in els if e.get("type") == "text"]
        frames = [e.get("name", "") for e in els if e.get("type") == "frame"]
        self.assertFalse(any("From here to the send" in f for f in frames), frames)
        self.assertFalse(any("T2 · run it a week" in t for t in texts))           # the plan lists the Runs now
        self.assertTrue(any("s03-paper-dataflow" in t and "G0 ⬜" in t for t in texts), texts)   # where they went
        self.assertTrue(any(t.startswith("Act 3 · Where it could go") for t in texts))          # no gap in the acts
        self.assertTrue(any("Where the story could go" in f for f in frames))

    def test_each_question_reads_as_a_row_and_the_theory_shows(self):
        face = (self.topic / f"{self.topic.name}.md").read_text(encoding="utf-8")
        face = face.replace("- **1a** · Starts: it starts · tested by E1",
                            "- **1a** · Starts: it starts (demo theory) · tested by E1")
        face = face.replace("### 5 · Evidence Basis and Boundaries", """#### 3.3 · Hypothesis development

| theory | it says | so here | hypotheses | the data decides by |
|---|---|---|---|---|
| Demo theory | demos start | this one starts | 1a | T1 |

### 4 · Stakes

- **Theory** (proposed): one lens. The contribution: a demo that starts is a demo that works.

| theory | the idea in one line | what it predicts here | questions | how the data tests it | role | reference |
|---|---|---|---|---|---|---|
| Demo theory | demos start | it starts | RQ1 | T1 | core | Demo 2020 |
| Noise theory | nothing works | it fails | RQ2 | T2 | set aside: says nothing here | Noise 1999 |

### 5 · Evidence Basis and Boundaries""")
        (self.topic / f"{self.topic.name}.md").write_text(face, encoding="utf-8")
        S = sd.read(self.topic)
        self.assertEqual([r["codes"] for r in S["theory"]], [["1a"], []])
        self.assertEqual(S["theory_claim"], "a demo that starts is a demo that works")
        els = json.loads(sd.draw(self.topic).read_text())["elements"]
        texts = [e.get("text", "") for e in els if e.get("type") == "text"]
        frames = [e.get("name", "") for e in els if e.get("type") == "frame"]
        rq1 = [f for f in frames if "RQ1 · Does it start?" in f]
        self.assertEqual(len(rq1), 1, frames)                                         # one wide frame a question
        self.assertTrue(any(t == "What we expect, and why" for t in texts), texts)    # its panels, left to right
        self.assertTrue(any(t == "What the paper can say" for t in texts))
        wide = [e for e in els if e.get("type") == "frame" and "RQ1 · Does it start?" in e.get("name", "")][0]
        self.assertEqual((wide.get("customData") or {}).get("columns"), 3)            # ⑨ judged per panel
        self.assertTrue(any("theory: demo theory" in t for t in texts), texts)              # each hypothesis's theory
        self.assertTrue(any(t.startswith("Theory Demo theory") for t in texts))             # on its question's card
        self.assertTrue(any("Why the questions hang together" in f for f in frames))
        self.assertTrue(any(t.startswith("core · Demo theory: demos start") for t in texts))
        self.assertTrue(any(t.startswith("set aside · Noise theory") for t in texts))
        self.assertFalse(any("How it fits together" in f for f in frames))                  # its table is in ①
        self.assertTrue(any(t == "Hypotheses" for t in texts))                                   # ①'s column names
        self.assertTrue(any(t.startswith("✅ 1a Starts") for t in texts), texts)                # a hypothesis cell,
        self.assertTrue(any(t.startswith("⬜ C2 It lasts") for t in texts))                     #   marked; a claim cell

    def test_a_face_with_no_question_blocks_says_so(self):
        (self.topic / f"{self.topic.name}.md").write_text("s02 · Story: empty\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            sd.read(self.topic)


if __name__ == "__main__":
    unittest.main()


OLD_TABLE = """# s02-story-demo-old · The Story: one prospective paper

### 2 · Pitch

### 3 · Research Questions

| RQ | question | why the paper needs it | answer form | Discovery | Task | intended claim / Section | answer state |
|---|---|---|---|---|---|---|---|
| RQ1 | Does it start? | It must start. | a rate | D1 | T1 | C1 / Results | ✅ supported |
| RQ2 | Does it last? | It must last. | days | D2 | T2 | E2 / Appendix | 🔨 provisional |

| E | RQ | proposition | support state |
|---|---|---|---|
| E2 | RQ2 | it lasts | provisional |

| T | question | stage |
|---|---|---|
| T1 | start it | data |
"""

REPORT = """# q01 · Does it start?

#### 3.1 · Question 1 · RQ1
- **Name**: Does it start?
- **Question**: Does the demo start on the first try?
- **Why the paper needs it**: a demo that does not start shows nothing.
- **Answer state**: ⬜ open
"""


class OlderFacesTest(unittest.TestCase):
    """A face with no question blocks: its Board's Questions' reports first, then an older §3 table."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.board = Path(self.tmp.name) / "Paper-Old"
        self.topic = self.board / "studio" / "s02-story-demo-old"
        self.topic.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_an_older_table_reads_as_questions(self):
        (self.topic / f"{self.topic.name}.md").write_text(OLD_TABLE, encoding="utf-8")
        (self.board / "board.md").write_text("# Paper-Old\nspine: One idea, told to a desk.\n", encoding="utf-8")
        S = sd.read(self.topic)
        self.assertEqual([q["rq"] for q in S["qs"]], ["RQ1", "RQ2"])
        self.assertEqual(S["qs"][1]["why it matters"], "It must last.")
        self.assertEqual(S["qs"][1]["work"], ["T2", "D2"])
        self.assertEqual(sd.mark(S["qs"][1]["answer state"]), "🔶")          # 🔨 reads as partly
        self.assertEqual(S["title"], "Paper-Old")                            # "one prospective paper" names nothing
        self.assertEqual(S["question"], "Does it start?")                   # the first question, the spine asks none
        self.assertEqual(sd.t_mark(S["T"]["T1"]), "")                       # no state column: no mark, never a guess
        out = sd.draw(self.topic)
        texts = [e.get("text", "") for e in json.loads(out.read_text())["elements"] if e.get("type") == "text"]
        self.assertFalse(any("Run to make" in t for t in texts))            # no path frame from a stateless table

    def test_the_boards_reports_come_before_the_table(self):
        (self.topic / f"{self.topic.name}.md").write_text("s02 · The current telling: demo\n", encoding="utf-8")
        rp = self.board / "reports" / "q01_start"
        rp.mkdir(parents=True)
        (rp / "q01_start.md").write_text(REPORT, encoding="utf-8")
        (self.board / "board.md").write_text("# Paper-Old\nspine: Can the demo run? More words.\n\n## Questions\n\n"
                                             "```yaml\nquestions:\n- id: Q01\n  report: reports/q01_start/q01_start.md\n```\n",
                                             encoding="utf-8")
        S = sd.read(self.topic)
        self.assertEqual(S["qs"][0]["name"], "Does it start?")
        self.assertEqual(S["qs"][0]["why it matters"], "a demo that does not start shows nothing.")
        self.assertEqual(S["question"], "Can the demo run?")               # the spine's own question
        self.assertEqual(S["title"], "Demo")
