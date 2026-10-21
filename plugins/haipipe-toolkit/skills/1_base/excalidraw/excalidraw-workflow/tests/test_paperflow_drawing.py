"""paperflow_drawing.py on a made-up Board: the Sections read in order, a question with no Section flagged, each display
named once for the building map. Placeholders only, no real project data."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import paperflow_drawing as pf  # noqa: E402

STORY = """s02 · Story: does the demo work
================================

**G0:** ⬜ not marked.

### 3 · Research Questions

**The paper's question**: Does the demo work?

#### 3.1 · Question 1 · RQ1
- **Name**: Does it start?
- **Research question**: Does the demo start on the first try?
- **Answer state**: ✅ it starts.

#### 3.2 · Question 2 · RQ2
- **Name**: Does it last?
- **Research question**: Does the demo keep working for a week?
- **Answer state**: ⬜ not measured.

### 5 · Evidence Basis and Boundaries

| E | evidence | source | support state |
|---|---|---|---|
| E1 | it starts | demo.r01 | established |
| E2 | it lasts | no Run | absent |
"""

PLAN = """s04 · Paper workflow: a short demo paper
=========================================

**Tags:** `Plan`

**Budget:** Demo Journal: 1,000 words, up to 2 displays.

**Send:** 2026-12-01 (proposed).

### 1 · Sections

| S | section | answers | job | displays | evidence | words |
|---|---|---|---|---|---|---|
| S0 | Abstract | RQ1 | Gives the answer | — | E1 | 150 (outside the count) |
| S1 | Introduction | — | Asks the question | — | D1 | 300 |
| S2 | Results: it starts | RQ1 | Shows that it starts | Figure 1 | E1 | 700 |

### 2 · Displays

| Display | title | kind | answers | made by | state |
|---|---|---|---|---|---|
| Figure 1 | Starts per try | figure | RQ1 | demo.t01.r02 | done |
| Table 1 | Days it lasts | table | RQ2 | a new figure Run | not started |

### 3 · Timeline

| W | step | when | who | state |
|---|---|---|---|---|
| W1 | G0: mark the story | 11-01 | JL marks | not started |
| W2 | Send | 12-01 | the team sends | not started |
"""


class PaperflowTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        board = Path(self.tmp.name) / "Paper-Demo"
        (board / "studio" / "s02-story-demo-works").mkdir(parents=True)
        (board / "studio" / "s02-story-demo-works" / "s02-story-demo-works.md").write_text(STORY, encoding="utf-8")
        (board / "board.md").write_text("# Paper-Demo\nstory-current: s02-story-demo-works\n", encoding="utf-8")
        self.topic = board / "studio" / "s04-paper-workflow"
        self.topic.mkdir()
        (self.topic / "s04-paper-workflow.md").write_text(PLAN, encoding="utf-8")
        self.board = board

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_face_reads_as_its_tables(self):
        P = pf.read(self.topic)
        self.assertEqual(P["title"], "A short demo paper")                 # capitalized
        self.assertEqual([s["s"] for s in P["S"]], ["S0", "S1", "S2"])
        self.assertEqual(P["displays"][1]["display"], "Table 1")
        self.assertEqual(len(P["W"]), 2)
        self.assertIn("1,000 words", P["budget"])
        self.assertEqual([q["rq"] for q in P["story"]["qs"]], ["RQ1", "RQ2"])     # read from the telling

    def test_marks_and_ids(self):
        P = pf.read(self.topic)
        self.assertEqual(pf.ids("E4 to E6, E9", "E"), ["E4", "E5", "E6", "E9"])
        self.assertEqual(pf.ids("RQ1, RQ3", "RQ"), ["RQ1", "RQ3"])
        self.assertEqual(pf.ids("Ework04 to Ework06, Ecite02", "E"), ["Ework04", "Ework05", "Ework06", "Ecite02"])   # JL 261020
        self.assertEqual(pf.ev_mark(P["S"][2], P["story"]["E"]), "✅")
        self.assertEqual(pf.ev_mark({"evidence": "E2"}, P["story"]["E"]), "⬜")
        self.assertEqual(pf.ev_mark(P["S"][1], P["story"]["E"]), "")             # a Discovery row only
        self.assertEqual(pf.words("350 + 100"), 450)
        self.assertEqual(pf.words("350 (outside the count)"), 350)
        self.assertFalse(pf.counted({"words": "350 (outside the count)"}))

    def test_the_building_map_reads_the_displays_once(self):
        self.assertEqual(pf.displays_by_question(self.board), {1: "Figure 1", 2: "Table 1"})

    def test_the_drawing_flags_a_question_with_no_section(self):
        out = pf.draw(self.topic)
        texts = [e.get("text", "") for e in json.loads(out.read_text())["elements"] if e.get("type") == "text"]
        self.assertTrue(any("RQ2 has no section" in t for t in texts), texts)
        self.assertTrue(any("S2 · Results: it starts" in t for t in texts))
        self.assertTrue(any("1,000 words counted" in t for t in texts))           # the abstract is outside the count
        self.assertTrue(any(t.startswith("Budget: Demo Journal") for t in texts))
        self.assertTrue(any("Table 1 · Days it lasts" in t for t in texts))
        self.assertTrue(any("🙋" in t and "team" in t for t in texts))           # a person's step, no name built in
        self.assertTrue(out.with_suffix(".png").is_file())


if __name__ == "__main__":
    unittest.main()
