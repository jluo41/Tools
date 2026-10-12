"""A design is drawn in its goal's channel (JL 261011, a pre-visit questionnaire shown as a text message: "it is
not message"): a phone for an SMS, a push or a reminder; tick boxes for a checklist; answer boxes for a
questionnaire; the channel comes from the goal the Job pins (design_reader.venue_of)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
from host_paths import bootstrap  # noqa: E402

bootstrap()
from live import design_reader as R  # noqa: E402
from live import design_views as V  # noqa: E402

QUESTIONS = """# Before your visit: two parts of your day

1. What time do you usually wake up?
   answer: time
2. What do you usually do in your first hour?
   answer: sentence
3. Do you eat anything before six?
   answer: yes-no

Done when: every question has an answer."""

TICKS = """Wear it all 14 days
[ ] Charge your watch (Day 14).
[ ] Put your watch on after waking (Day 13).
Done: each day has a tick."""


class ChannelLookTest(unittest.TestCase):
    def test_a_questionnaire_has_answer_boxes_and_no_message(self):
        html = V.as_read(QUESTIONS, "questionnaire")
        self.assertIn("Questionnaire", html)
        self.assertNotIn("Text message", html)
        self.assertIn("1.</b> What time do you usually wake up?", html)
        self.assertIn("__ : __", html)                                  # a time answer
        self.assertIn("○ Yes", html)                                    # a yes-no answer
        self.assertNotIn("answer:", html)                               # the answer line is drawn, not shown

    def test_a_checklist_has_ticks_and_keeps_its_day_labels(self):
        html = V.as_read(TICKS, "checklist")
        self.assertIn("Checklist", html)
        self.assertNotIn("Text message", html)
        self.assertIn("Charge your watch (Day 14).", html)
        self.assertIn("Done: each day has a tick.", html)

    def test_messages_stay_on_a_phone_and_no_channel_is_an_sms(self):
        self.assertIn("Text message", V.as_read("Hi {LINK}", "sms"))
        self.assertIn("Text message", V.as_read("Hi {LINK}", ""))       # an older Block without a venue
        self.assertIn("Push notification", V.as_read("Hi", "push"))
        self.assertIn("Email", V.as_read("Dear …", "email"))

    def test_the_channel_comes_from_the_pinned_goal(self):
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "Design-Demo"
            job = block / "j01_ask-before-visit_goal-only"
            task = job / "t01_d01_two-windows"
            task.mkdir(parents=True)
            (block / "board.md").write_text("# Design-Demo\n\nboard-kind: design-board\n\n## Goals\n\n```yaml\ngoals:\n"
                                            "- id: G01\n  name: ask-before-visit\n  venue: questionnaire\n```\n")
            (job / f"{job.name}.md").write_text("---\ngoal: G01\nmethod: M01 m2\ninputs: i1\n---\n\n# Ask, by Goal only\n")
            self.assertEqual(R.venue_of(task), "questionnaire")
            self.assertEqual(R.venue_of(job), "questionnaire")
            self.assertEqual(R.venue_of(block), "")                         # a Block pins no goal


if __name__ == "__main__":
    unittest.main()
