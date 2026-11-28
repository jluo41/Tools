"""Faces and levels: what a page's face says, how each level reads it, its part of the Block's Delivery."""
import unittest

import sys
from pathlib import Path
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
    def test_a_named_board_names_its_own_studio_topic(self):          # insight, design, Question Book (261106)
        for name in ("Insight-Example", "Design-Example", "Prototype-b91-Example", "Paper-Example"):
            board = self.root / name
            topic = board / "j01_first" / "s01-example-flow"
            topic.mkdir(parents=True)
            (board / "board.md").write_text("# Example\n")
            (board / "j01_first" / "j01_first.md").write_text("# First\n")
            (topic / "s01-example-flow.md").write_text("# Flow\n")
            self.assertEqual(focus_page.interaction_topic(f"{name}.j01-s01:x @ y", board / "j01_first"), topic, name)
        self.assertIsNone(focus_page.interaction_topic("Other-Example.j01-s01:x @ y", self.root / "Insight-Example"))

    def test_a_job_and_a_task_show_their_part_of_the_blocks_delivery(self):   # hai-delivery's <job>/<task>/ (261106)
        task = self.block / "j02_estimates" / "t04_deliver"
        task.mkdir(parents=True)
        (self.block / "j02_estimates" / "j02_estimates.md").write_text("# Estimates\n")
        (task / "t04_deliver.md").write_text("# Deliver\n")
        web = self.block / "delivery" / "j02_estimates" / "t04_deliver" / "web"
        web.mkdir(parents=True)
        (web / "index.html").write_text("<p>explorer</p>")
        for page in (self.block / "j02_estimates", task):
            tabs = dict((name, panel) for name, _, panel in focus_page.delivery_tabs(page, self.root))
            self.assertIn("index.html", tabs["Website"], page.name)
            self.assertIn("/delivery/j02_estimates/", focus_page.delivery_html(page, self.root), page.name)
        other = self.block / "j01_source"
        other.mkdir()
        (other / "j01_source.md").write_text("# Source\n")
        self.assertNotIn("index.html", dict((n, p) for n, _, p in focus_page.delivery_tabs(other, self.root))["Website"])

    def test_discovery_and_cowork_pages_take_the_work_shape(self):   # JL 261106: "very similar to the work"
        for name in ("discovery", "cowork"):
            for section in ("report", "work"):
                page = focus_page.render(frame.Theme(name=name), self.root, self.block, section)
                self.assertIn('id="band-overview"', page, (name, section))   # its views are bands (JL 261124)
                self.assertIn('aria-current="page">Main</a>', page, (name, section))   # one Main view holds the bands
        self.assertEqual(focus_page.theme_parts("work", self.block, self.root, "Block"), [])

    def test_a_job_with_no_tasks_is_known_by_its_own_state(self):   # a cowork Job, one line of work (261106)
        job = self.block / "j01_reply"
        job.mkdir()
        for state, word in (("🟡 ACTIVE · waiting on the reply", "running"), ("✅ DONE", "done"),
                            ("🔴 OPEN", "open"), ("", "not run")):
            (job / "j01_reply.md").write_text(f"# Reply\nstate: {state}\n")
            self.assertEqual(focus_page.job_progress(job, self.root)[1], word, state)

    def test_an_older_paper_run_has_its_readout_as_headline(self):   # discovery Paper Runs (261106)
        result = self.block / "j01_x" / "t01_y" / "runs" / "r01_example2024one" / "result"
        result.mkdir(parents=True)
        (result / "r01_example2024one.md").write_text("# Card\n\n- cite: @example2024one\n\n## Readout\n\n"
                                                       "The example shows a small effect. It is one study.\n\n## Limits\n\nOne.\n")
        self.assertEqual(focus_page.run_headline(result.parent), "The example shows a small effect.")

    def test_every_level_has_its_studio_none_yet_with_add_a_topic(self):   # b11 form, JL 261106
        job = self.block / "j01_first"
        job.mkdir()
        (job / "j01_first.md").write_text("# First\n")
        page = focus_page.render(frame.Theme(name="work"), self.root, job, "report")
        self.assertIn("section=studio", page)                          # on the rail with no topic
        studio = focus_page.render(frame.Theme(name="work"), self.root, job, "studio")
        self.assertIn("No Studio topic here yet.", studio)
        self.assertIn(">Add a topic</button>", studio)
        self.assertIn("new_topic.py", studio)

    def test_existing_work_face_needs_no_migration(self):
        data = focus_page.read_face(self.block, self.root)
        self.assertEqual(data["goal"], "Compare the methods.")
        self.assertEqual(data["close"], "Each result names its source.")
        self.assertEqual(focus_page.home_section(data, "work"), "status")
        page = focus_page.render(frame.Theme(name="work"), self.root, self.block)
        self.assertRegex(page, r'<button type="button" class="h1-section[^>]*>Report</button>')  # hai-ui: a Block opens on Report
        self.assertNotIn('class="focus-goal"', page)                 # no goal-line under the title (hai-block A03)
        self.assertNotIn('<dt>Done when</dt>', page)                  # JL 261030: "we don't need this"
        self.assertNotIn('no state recorded', page)                   # an empty state is not shown as a box
        self.assertNotRegex(page, r'<details[^>]*\bopen\b')
        self.assertNotIn('<details class="completion" open', page)

    def test_explicit_sections_override_fields_and_support_frontmatter(self):
        self.face.write_text('---\ngoal: |\n  First line.\n  Second line.\nhome-section: takeaways\n---\n'
                             '# Study\n## Goal\nThe authored goal.\n## Takeaways\n- The reviewed result.\n')
        data = focus_page.read_face(self.block, self.root)
        self.assertEqual(data["goal"], "The authored goal.")
        self.assertEqual(focus_page.home_section(data, "work"), "takeaways")
        self.assertEqual(data["takeaways"], "- The reviewed result.")

    def test_multiline_yaml_goal_and_placeholder_fallback(self):
        self.face.write_text('---\ngoal: |\n  First line.\n  Second line.\n---\n# Study\n')
        self.assertEqual(focus_page.read_face(self.block, self.root)["goal"], "First line.\nSecond line.")
        self.face.write_text('# Study\ngoal: open\nspine: Actual goal.\n')
        self.assertEqual(focus_page.read_face(self.block, self.root)["goal"], "Actual goal.")

    def test_fenced_examples_do_not_become_sections_or_settings(self):
        self.face.write_text('# Study\n```md\nhome-section: takeaways\n## Takeaways\nFake\n```\n'
                             'spine: Real goal.\n## Goal\nText\n```md\n## Takeaways\nExample\n```\n')
        data = focus_page.read_face(self.block, self.root)
        self.assertFalse(data["takeaways"])
        self.assertFalse(data["home"])
        self.assertIn('## Takeaways', data["goal"])

    def test_current_level_never_inherits_parent_content(self):
        job = self.block / "j01_compare"
        job.mkdir()
        (job / (job.name + '.md')).write_text('# Job\ngoal: This job only.\n')
        data = focus_page.read_face(job, self.root)
        self.assertEqual(data["goal"], "This job only.")
        self.assertFalse(data["close"])
        self.face.write_text('# Study\n## Takeaways\nParent takeaway.\n')
        self.assertFalse(focus_page.read_face(job, self.root)["takeaways"])

    def test_a_paper_board_stays_in_its_view_between_report_and_work(self):
        # Paper Board merges Work into Report, retaining old bookmarks.
        page = focus_page.render(frame.Theme(name="paper"), self.root, self.block, "report", "draft")
        legacy = focus_page.render(frame.Theme(name="paper"), self.root, self.block, "work", "work-draft")
        self.assertEqual(page, legacy)
        self.assertNotIn('aria-label="Work"', page)
        other = focus_page.render(frame.Theme(name="work"), self.root, self.block, "report", "draft")
        self.assertNotIn("group=work-draft", other)

    def test_paper_missing_takeaways_is_not_synthesized(self):
        page = focus_page.render(frame.Theme(name="paper"), self.root, self.block, "report", "findings")   # Report opens on MindMap (JL 261031)
        self.assertRegex(page, r'<button type="button" class="h1-section[^>]*>Report</button>')
        self.assertNotIn('>Findings<', page)          # a paper Board has no Findings view (JL 261031: "no need to use them")
        self.assertNotIn('No takeaways recorded', page)
        self.assertLessEqual(page.count('Compare the methods.'), 1)  # never repeated as a takeaway
        self.assertNotIn('class="focus-goal"', page)                 # no goal-line under the title (hai-block A03)
        work = focus_page.render(frame.Theme(name="paper"), self.root, self.block, 'work')
        self.assertIn('>Writing<', work)   # a paper Board's Work shares its Report's list; the versions sit in Writing (JL 261031)

    def test_source_change_is_visible_on_next_render(self):
        self.face.write_text('# Study\ngoal: Before.\n')
        self.assertIn('Before.', focus_page.render(frame.Theme(name="work"), self.root, self.block))
        self.face.write_text('# Study\ngoal: After.\n')
        page = focus_page.render(frame.Theme(name="work"), self.root, self.block)
        self.assertIn('After.', page)
        self.assertNotIn('Before.', page)


if __name__ == '__main__':
    unittest.main()
