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

**The paper's question**: Does the demo work?

**The story, question by question** (read in order):

1. Does it start? ✅ It starts.
2. Does it last? ⬜ Not measured.

#### 3.1 · Question 1 · RQ1
- **Name**: Does it start?
- **Question**: We start it.
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
- **Question**: We run it for a week.
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
        self.assertEqual(S["question"], "Does the demo work?")
        self.assertEqual([q["rq"] for q in S["qs"]], ["RQ1", "RQ2"])
        self.assertEqual([q["told"] for q in S["qs"]], ["Does it start?", "Does it last?"])
        self.assertEqual(S["qs"][1]["claims"][0]["c"], "C2")              # a claim from two hypotheses still reads
        self.assertEqual(len(S["pitch"]), 4)
        self.assertIn("wrapped onto a second line", S["pitch"][1])
        self.assertIn("(pending E2)", S["pitch"][2])                       # the font cannot show ⟦ ⟧
        self.assertEqual(S["refuse"], ["that it is fast;", "that it is cheap."])

    def test_marks_follow_the_face(self):
        S = sd.read(self.topic)
        self.assertEqual(sd.mark(S["qs"][0]["answer state"]), "✅")
        self.assertTrue(sd.missing(S["qs"][1]["answer state"]))
        self.assertEqual((sd.e_mark(S["E"]["E1"]), sd.e_mark(S["E"]["E2"])), ("✅", "⬜"))
        self.assertEqual((sd.t_mark(S["T"]["T1"]), sd.t_mark(S["T"]["T2"])), ("✅", "⬜"))

    def test_the_drawing_shows_every_question_and_what_is_missing(self):
        out = sd.draw(self.topic)
        texts = [e.get("text", "") for e in json.loads(out.read_text())["elements"] if e.get("type") == "text"]
        self.assertTrue(any("RQ1 · Does it start?" in t for t in texts), texts)
        self.assertTrue(any("RQ2 · Does it last?" in t for t in texts))
        self.assertTrue(any("Does it start? → Does it last?" in t for t in texts))      # the narrative chain
        self.assertTrue(any("T2 · run it a week" in t for t in texts))                  # a Run to make
        self.assertTrue(any("G0" in t for t in texts))
        self.assertFalse(any("T1 · start it" in t for t in texts))                      # a done Run is not missing
        self.assertTrue(out.with_suffix(".png").is_file())

    def test_a_face_with_no_question_blocks_says_so(self):
        (self.topic / f"{self.topic.name}.md").write_text("s02 · Story: empty\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            sd.read(self.topic)


if __name__ == "__main__":
    unittest.main()
