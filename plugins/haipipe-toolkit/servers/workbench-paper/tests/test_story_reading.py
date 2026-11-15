"""The Story view reads as a story (Paper-CMS-AI-Usage 261110: "the display here is not well to ready"): the
Direction's question large and its other labels as rows; the Pitch a sentence a line, its stage only on the bar, a
pending mark a chip; each Research Question with what it lets the paper say, its state a chip, no process text.
Placeholders only, in a temp folder."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page, frame  # noqa: E402

IDEA = ("# s01 · Ideation\n\n**Stage:** agreed\n\n## Content\n\n### 1 · Direction\n\n"
        "**Direction question**: what does <the data> show about <the people>?\n\n"
        "**Why now**: <the reason>.\n\n**Admission rule**: <the rule>.\n")
STORY = ("# s02 · Story\n\n**Stage:** explore\n\n## Content\n\n### 1 · Identity\n\n**One-sentence identity**: <the paper in one line>.\n\n"
         "### 2 · Pitch\n\n<The tension>. <What we do>. ⟦pending E01⟧ We expect <the answer>. <Who cares>.\n\n"
         "### 3 · Research Questions\n\n**The paper's question**: <the whole question>?\n\n"
         "1. <first question>? ⬜ nothing yet\n2. <second question>? ⬜ nothing yet (supplement only)\n\n"
         "**The narrative, if the questions are answered**:\n\n1. <what the first lets us say>.\n2. <what the second lets us say>.\n\n"
         "Each question is a Board Question with its report (`board.md`, `reports/`).\n\n"
         "**Why we ask each question, and how others asked it**:\n\n"
         "| RQ | why we ask it | how others asked it | what is new here |\n|---|---|---|---|\n"
         "| 1 · how many | a payer plans around people | counted claims per code | people, not claims |\n")


class StoryReadingTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        b = self.b = self.root / "paper" / "Paper-X"
        for name, text in (("s01-ideation", IDEA), ("s02-story-desk-x", STORY)):
            (b / name).mkdir(parents=True)
            (b / name / f"{name}.md").write_text(text, encoding="utf-8")
        (b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\nstory-current: s02-story-desk-x\n", encoding="utf-8")
        page = focus_page.render(frame.Theme(name="paper"), self.root, b, "report", "story")
        self.raw = page
        self.page = re.sub(r"<style>.*?</style>|<script>.*?</script>", "", page, flags=re.S)

    def part(self, name, until):
        return self.page.split(name, 1)[1].split(until, 1)[0]

    def test_a_capped_block_sits_in_the_middle_of_its_card(self):
        # JL 261110: "at least you put the paragraph in the middle"
        self.assertIn(".pb-story,.pb-story.pb-wide .pb-head{max-width:92ch;margin-inline:auto}", self.raw)
        self.assertIn(".fd-body>p,.fd-body>ol,.fd-body>ul,.fd-body>.pb-big{margin-left:auto;margin-right:auto}", self.raw)

    def test_direction_question_large_the_rest_rows(self):
        d = self.part("🧭 Direction", "💡 Pitch")
        self.assertIn("<p class=pb-big>What does &lt;the data&gt; show about &lt;the people&gt;?</p>", d)
        self.assertIn("<dt>Why now</dt><dd>&lt;the reason&gt;.</dd>", d)
        self.assertIn("<dt>Admission rule</dt>", d)
        self.assertNotIn("<strong>", d)

    def test_pitch_a_sentence_a_line_pending_a_chip(self):
        p = self.part("💡 Pitch", "🎓 Theory")
        self.assertEqual(p.count("<li>"), 4)
        self.assertIn("<span class=pb-chip>pending E01</span>", p)
        self.assertNotIn("⟦", p)
        self.assertNotIn("<p class=pb-state>", p)             # the stage is the bar's word only

    def test_one_table_a_row_per_question_every_field_side_by_side(self):
        # JL 261111: "why you don't just add more columns????? so hard to review and read"
        q = self.part("❓ Research Questions", "Interaction")
        self.assertNotIn("2 of 2 open", q)                                  # no progress tally on the bar
        self.assertIn("<div class=pb-rqhead data-addr=\"RQ.Q\"><p class=pb-label>The paper's question", q)
        self.assertIn("<p class=pb-big>&lt;the whole question&gt;?</p>", q)
        self.assertIn("<thead><tr><th></th><th>Question</th><th>Why we ask</th><th>Asked before</th><th>New here</th>"
                      "<th>Expected</th><th></th></tr></thead>", q)
        self.assertNotIn('data-h="State"', q)                                # JL 261111: "no need for this, drop it"
        first = q.split("<td class=k>RQ1</td>", 1)[1].split("</tr>", 1)[0]
        self.assertIn('<td data-h="Question">&lt;first question&gt;?</td>', first)
        self.assertIn('<td data-h="Why we ask">a payer plans around people</td>', first)
        self.assertIn('<td data-h="Expected">&lt;what the first lets us say&gt;.</td>', first)
        second = q.split("<td class=k>RQ2</td>", 1)[1].split("</tr>", 1)[0]
        self.assertIn('<td data-h="Why we ask"></td>', second)                  # no row in §3's table, an empty cell
        self.assertNotIn("pb-rqs", q)
        self.assertNotIn("Each question is a Board Question", q)


class SectionRowsTest(unittest.TestCase):
    def test_section_rows_read_as_the_questions_do(self):
        # JL 261111: "they are very differnt, where is the 1, 2, 3, 4"
        from live.board_results import _section_rows
        low = {"reader question": "what does the reader ask?", "ordered moves": "move a; move b; move c",
               "exit": "what they leave with", "displays": "Display A, Display F (supplement, one)",
               "must refuse": "a causal claim"}
        html = _section_rows([("t01_introduction", low, [{"claim": "C1", "proposition": "the claim"}]),
                              ("t02_methods", {"reader question": "how?"}, []),
                              ("t21_supplement", {"reader question": "does it hold?"}, [])])
        self.assertIn('<div class="pb-story pb-wide"><ol class="pb-rqs pb-secs">', html)
        self.assertIn("<span class=k>1<span class=nm>Introduction</span></span>", html)
        self.assertIn("<span class=k>2<span class=nm>Methods</span></span>", html)
        self.assertIn("<span class=k>S1<span class=nm>Supplement</span></span>", html)
        self.assertIn("<ol class=mvs><li>move a</li><li>move b</li><li>move c</li></ol>", html)   # numbered flow (JL 261111)
        self.assertIn("<p class=if>→ what they leave with</p>", html)
        self.assertIn("<span class=pb-chip>Display F (supplement, one)</span>", html)
        self.assertIn('<span class=pb-chip title="the claim">C1</span>', html)
        self.assertIn("<p class=mv>✗ a causal claim</p>", html)


if __name__ == "__main__":
    unittest.main()
