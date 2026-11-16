"""The paragraph Logic card reads at a glance (JL 261115: "the logic here is less readable")."""
import unittest

from host_paths import bootstrap

bootstrap()
from live.draft_step_flow_card import body, parse  # noqa: E402

LINE = ('7/10 · s15 studies disagree → s16 wearables improve → s17 a heart model is worse · '
        'the paragraph never says what the disagreement is about · weakest join s16 to s17, a new topic with no setup')
inline = lambda t, _: t


class FlowCardTest(unittest.TestCase):
    def test_the_line_splits_into_problem_steps_and_join(self):
        f = parse(LINE)
        self.assertEqual(f["score"], "7/10")
        self.assertEqual([s for s, _ in f["steps"]], ["s15", "s16", "s17"])
        self.assertTrue(f["problem"].startswith("the paragraph never says"))
        self.assertEqual(f["weak"][:2], ("s16", "s17"))

    def test_problem_first_and_the_cut_between_its_two_steps(self):
        html = body(LINE, inline)
        self.assertLess(html.index("the paragraph never says"), html.index("studies disagree"))
        self.assertLess(html.index("wearables improve"), html.index("✂ weakest join"))
        self.assertLess(html.index("✂ weakest join"), html.index("a heart model is worse"))
        self.assertNotIn("lg-clip2", html)

    def test_the_map_is_the_structure_view_of_the_paragraph(self):
        # JL 261115: "why not just have the thins like the mindmap graph like we have in the structure"
        from live.draft_step_flow_card import map_html
        para = ("C1.P3", "Studies disagree · s15 to s17", [("s15", "Known", "studies disagree", ""),
                ("s16", "Known", "wearables improve", ""), ("s17", "Turn", "a heart model is worse", "")])
        html = map_html(LINE + ' · weakest join s16 to s17, from "a" to "b", a new topic', inline, para)
        self.assertIn('<span class=pm-id>C1.P3</span><b>Studies disagree · s15 to s17</b>', html)
        self.assertEqual(html.count("class=pm-role>"), 3)
        self.assertIn("<span class=pm-role>Turn</span>", html)
        self.assertIn("★7/10", html)
        self.assertEqual(html.count("class=pm-cut"), 1)                  # on s17's row only, in words
        self.assertIn("<span class=pm-cut>weak link from s16: a new topic with no setup</span>", html)
        self.assertLess(html.index("a heart model is worse"), html.index("class=pm-cut"))
        self.assertNotIn("pm-edit", html)                                 # read-only: nothing writes from here
        self.assertEqual(map_html(LINE, inline, None), "")               # no § 1 paragraph, no map
        self.assertIn("Fix", body(LINE + " · fix: say what disagrees", inline))

    def test_an_older_line_shows_as_written(self):
        html = body("S1 the shift, then S2 · weakest join S1 to S2", inline)
        self.assertIn("S1 the shift, then S2", html)
        self.assertIn("weakest join", html)


if __name__ == "__main__":
    unittest.main()
