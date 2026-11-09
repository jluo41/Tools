"""Face ownership, landing selection and focused-page route regressions."""
import re
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402


class FocusPageTest(unittest.TestCase):
    def findings_block(self):
        report = self.block / 'reports/q01_a/q01_a.md'
        report.parent.mkdir(parents=True)
        report.write_text('# A\nstate: OPEN\n\n## Opening\n\nNo answer has been recorded yet.\n')
        done = self.block / 'reports/q02_b/q02_b.md'
        done.parent.mkdir(parents=True)
        done.write_text('# B\nstate: OPEN\n\n## Opening\n\nAgreed (261104): Every table is stored.\n')
        task = self.block / 'j01_work/t01_read'
        task.mkdir(parents=True)
        (self.block / 'j01_work/j01_work.md').write_text('# j01\nstate: PARTIAL\n')
        (task / 't01_read.md').write_text('# t01\nstate: PARTIAL\n\n## Content\n\n<!-- note -->\nReading of run `r01`.\n\n- 106 tables checked: 84 pass.\n')
        self.face.write_text('# Study\ngoal: Compare.\n\n## Questions\n\n```yaml\nquestions:\n'
                             '- id: Q01\n  title: Stored tables\n  group: Coverage\n  report: reports/q01_a/q01_a.md\n  work:\n  - j01_work/t01_read\n'
                             '- id: Q02\n  title: Whole tables\n  group: Cards\n  report: reports/q02_b/q02_b.md\n```\n')

    def test_findings_is_closed_sections_of_the_results(self):
        self.findings_block()
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'findings')
        self.assertIn('<details class=band-sec><summary>1 · ❓ Coverage<span class=word>no answer yet</span>', page)   # every
        self.assertIn('<details class=band-sec><summary>2 · ❓ Cards<span class=word>answered</span>', page)            # bar its emoji
        self.assertNotIn('band-sec open', page)
        self.assertIn('pb-side', page)                             # left tabs, the content on the right (JL 261104)
        self.assertIn('<b>Stored tables</b>', page)
        self.assertNotIn('<summary>3 · 📦 Delivery', page)
        delivery = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'delivery')
        for lane in ('Models', 'Data', 'Website'):
            self.assertIn(f'<b>{lane}</b>', delivery)
        self.assertNotIn('>Questions<', page)
        self.assertIn('106 tables checked: 84 pass.', page)        # no answer yet: what its work found
        self.assertNotIn('Reading of run', page)
        self.assertIn('Every table is stored.', page)
        self.assertNotIn('No answer has been recorded yet.', page)

    def test_findings_shows_a_tasks_newest_maps_as_tabs(self):
        self.findings_block()
        task = self.block / 'j01_work/t01_read'
        for run, words in (('r01_old', 'Old line.'), ('r02_new', 'One row: one reading.')):
            maps = task / 'runs' / run / 'result/maps'
            maps.mkdir(parents=True)
            (maps / 'CGM.mindmap.md').write_text(f'---\nmindmap: 1\n---\n\n# CGM <!-- root #aaa -->\n\n{words}\n\n- Required\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'findings')
        self.assertIn('<summary>3 · 🧠 Maps', page)
        self.assertNotIn('<summary>4 · 📦 Delivery', page)
        self.assertIn('<b>CGM</b><span title="">', page)                         # no cut grey line under the tab (round 3)
        self.assertIn('onload="window.fitMap&&fitMap(this)"', page)            # the frame as tall as its map
        self.assertIn('r02_new%2Fresult%2Fmaps%2FCGM.mindmap.md', page)
        self.assertNotIn('r01_old%2Fresult', page)
        self.assertIn('class=find-map loading=lazy', page)

    def test_work_has_the_same_views_as_report(self):
        self.findings_block()
        theme = frame.Theme(name='work')
        names = lambda html: re.findall(r'>([^<>]+)</a>', re.search(r'<nav class="section-views".*?</nav>', html, re.S)[0])
        report = focus_page.render(theme, self.root, self.block, 'report')
        work = focus_page.render(theme, self.root, self.block, 'work')
        self.assertEqual(names(work), names(report))
        self.assertNotIn('Progress', names(work))
        self.assertNotIn('⚙️ Process</h3>', work)  # Report and Work now share Review Content
        self.assertIn('j01_work', work.split('📋 Review Content')[1])
        found = focus_page.render(theme, self.root, self.block, 'work', 'findings')
        self.assertIn('Answers to write or agree', found)
        self.assertNotIn('>Questions<', work)
        self.assertIn('106 tables checked: 84 pass.', found.split('📋 Review Content')[1])
        task = focus_page.render(theme, self.root, self.block / 'j01_work/t01_read', 'work')
        self.assertIn('📋 Review Content', task)

    def test_band_title_raises_only_a_lowercase_first_letter(self):
        for given, shown in (("coverage", "Coverage"), ("🧠 heads", "🧠 Heads"), ("the WellDoc datasets", "The WellDoc datasets"),
                             ("WellDoc datasets", "WellDoc datasets"), ("AI-READI", "AI-READI"), (" public ", "Public")):
            self.assertEqual(focus_page.band_title(given), shown)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / "b01_study"
        self.block.mkdir()
        self.face = self.block / "board.md"
        self.face.write_text("# Study\nspine: Compare the methods.\nclose: Each result names its source.\n")

    def test_a_named_board_names_its_own_studio_topic(self):          # insight, design, Prototype (261106)
        for name in ("Insight-Example", "Design-Example", "Prototype-b91-Example", "Paper-Example"):
            board = self.root / name
            topic = board / "j01_first" / "s01-example-flow"
            topic.mkdir(parents=True)
            (board / "board.md").write_text("# Example\n")
            (board / "j01_first" / "j01_first.md").write_text("# First\n")
            (topic / "s01-example-flow.md").write_text("# Flow\n")
            self.assertEqual(focus_page.interaction_topic(f"{name}.j01-s01:x @ y", board / "j01_first"), topic, name)
        self.assertIsNone(focus_page.interaction_topic("Other-Example.j01-s01:x @ y", self.root / "Insight-Example"))

    def test_a_job_and_a_task_show_their_part_of_the_blocks_delivery(self):   # haipipe-delivery's <job>/<task>/ (261106)
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
                bar = page[page.index('class="section-views'):]
                bar = bar[:bar.index('</nav>')]
                self.assertIn('group=findings', bar, (name, section))
                self.assertIn('group=standing', bar, (name, section))
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
        self.assertRegex(page, r'<span class="h1-section"[^>]*>Report</span>')  # haipipe-ui: a Block opens on Report
        self.assertIn('<div class="focus-goal"><span class="goal-word">Purpose</span><p>Compare the methods.</p>', page)  # the head: path, name, goal only
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
        self.assertRegex(page, r'<span class="h1-section"[^>]*>Report</span>')
        self.assertNotIn('>Findings<', page)          # a paper Board has no Findings view (JL 261031: "no need to use them")
        self.assertNotIn('No takeaways recorded', page)
        self.assertEqual(page.count('Compare the methods.'), 1)     # only as the head's goal line, never as a takeaway
        self.assertIn('<div class="focus-goal"><span class="goal-word">Purpose</span><p>Compare the methods.</p>', page)
        work = focus_page.render(frame.Theme(name="paper"), self.root, self.block, 'work')
        self.assertIn('>Writing<', work)   # a paper Board's Work shares its Report's list; the versions sit in Writing (JL 261031)

    def test_source_change_is_visible_on_next_render(self):
        self.face.write_text('# Study\ngoal: Before.\n')
        self.assertIn('Before.', focus_page.render(frame.Theme(name="work"), self.root, self.block))
        self.face.write_text('# Study\ngoal: After.\n')
        page = focus_page.render(frame.Theme(name="work"), self.root, self.block)
        self.assertIn('After.', page)
        self.assertNotIn('Before.', page)

    def test_registered_content_has_distinct_views_and_real_report_links(self):
        report_dir = self.block / 'reports' / 'q01_compare'
        report_dir.mkdir(parents=True)
        report = report_dir / 'q01_compare.md'
        report.write_text('# Comparison\nstate: DRAFT\nresults-read: 2026-10-22\n'
                          '## Opening\nThe recorded answer.\n\nLonger context.\n')
        self.face.write_text('# Study\nspine: Compare the methods.\n'
                             '## Topic\nDetailed context only.\n## Pipeline\nInput to output.\n'
                             '## Questions\n```yaml\nquestions:\n- id: Q01\n  title: Compare\n'
                             '  question: Which method works?\n  hypothesis: An expectation, not a finding.\n'
                             '  report: reports/q01_compare/q01_compare.md\n```\n')
        theme = frame.Theme(name='work')
        home = focus_page.render(theme, self.root, self.block, "report", "findings")   # Report opens on MindMap (JL 261031)
        self.assertIn('The recorded answer.', home)                 # Overview opens on what we know (haipipe-ui)
        self.assertIn('>draft</span>', home)
        self.assertNotIn('Detailed context only.', home)          # the face's prose is not in Report (JL 261030)
        self.assertNotIn('An expectation, not a finding.', home)
        reports = focus_page.render(theme, self.root, self.block, 'reports')
        self.assertIn('The recorded answer.', reports)
        self.assertNotIn('Longer context.', reports)
        self.assertIn('Which method works?', focus_page.render(theme, self.root, self.block, 'overview', 'questions'))
        self.assertNotIn('Detailed context only.', focus_page.render(theme, self.root, self.block, 'work'))
        questions = focus_page.render(frame.Theme(name='ideation'), self.root, self.block, 'questions')   # a work-shaped page has no Questions view (JL 261104); cowork is work-shaped since 261106
        self.assertIn('Hypothesis', questions)
        self.assertIn('An expectation, not a finding.', questions)

    def test_registered_report_outside_root_is_not_read(self):
        with tempfile.TemporaryDirectory() as outside:
            report = Path(outside) / 'private.md'
            report.write_text('# Private\n## Opening\nDo not render.\n')
            self.face.write_text('# Study\n## Questions\n```yaml\nquestions:\n- id: Q01\n'
                                 f'  title: Outside\n  report: {report}\n```\n')
            page = focus_page.render(frame.Theme(name='work'), self.root, self.block)
            self.assertNotIn('Read report', page)
            self.assertNotIn('Do not render.', page)

    def test_a_topic_folder_with_no_face_never_takes_the_page_down(self):
        # 261031 review: b11's s32-insight-element-ui/ held a drawing and a builder but no .md, and its Block's Report
        # (MindMap first) dropped the connection; a bare folder is no topic (is_topic), so the map skips it
        bare = self.block / 's32-element-ui'
        bare.mkdir()
        (bare / 'build_s32_element_ui.py').write_text('')
        (self.block / 'j01_work').mkdir()
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report')
        self.assertIn('class="focus-map', page)
        self.assertFalse(focus_page.is_topic(bare))

    def test_an_sNN_beside_the_jobs_is_a_studio_card_with_no_page_of_its_own(self):
        # JL 261030: "we just have sNN, along side with jNN, to make it visible directly"
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('# s01 · First\n**Stage:** shaping\n')
        (self.block / 'j01_work').mkdir()
        self.assertTrue(focus_page.is_topic(topic))
        self.assertEqual(frame.topic_owner(topic), self.block)
        self.assertEqual(frame.topic_address(topic), 'b01-s01')
        self.assertEqual([p.name for p in focus_page.kids(self.block)], ['j01_work'])   # not taken for a Job
        studio = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('s01', studio)
        self.assertIn('first', studio)
        self.assertIn('<article class="studio-topic-content" id="s01-first">', studio)   # the card a link lands on
        home = focus_page.topic_home(topic, self.root)                  # JL 261031: the sNN page is retired
        self.assertIn('path=b01_study&layout=focus&section=studio', home)
        self.assertTrue(home.endswith('#s01-first'))
        page = focus_page.render(frame.Theme(name='work'), self.root, topic)   # an old link goes to the card
        self.assertIn('http-equiv="refresh"', page)
        rail = focus_page.render(frame.Theme(name='work'), self.root, self.block / 'j01_work')
        rail = rail.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        self.assertIn(frame.esc(home), rail)                             # the left rail's sNN opens its card
        self.assertIn('data-pop="First" href="/', studio)          # its name opens the face, popped out

    def test_studio_group_filters_without_losing_topic_identity(self):
        for name, group in [('s01-first', 'Alpha'), ('s02-second', 'Beta')]:
            topic = self.block / 'studio' / name
            topic.mkdir(parents=True)
            (topic / (name + '.md')).write_text(f'# {name}\n**Tags:** {group}\n')
        def body(*args):                                              # the left rail and the map list every sNN
            page = re.sub(r'<nav class="focus-rail left".*?</nav>', '', focus_page.render(*args), flags=re.S)
            page = re.sub(r'<dialog id="page-drawer".*?</dialog>', '', page, flags=re.S)
            return re.sub(r'<nav class="page-tree".*?</nav>', '', page, flags=re.S)   # (JL 261030; 261031)
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio', 'Beta')
        self.assertIn('s02-second', page)
        self.assertNotIn('s01-first', page)
        self.assertIn('aria-label="Views"', page)                     # the groups are Studio's views (JL 261029)
        self.assertIn('>Beta</a>', page)
        self.assertIn('>All</a>', page)                            # one button per group, no All (JL 261029)
        (self.block / 'studio' / 's03-third').mkdir()
        (self.block / 'studio' / 's03-third' / 's03-third.md').write_text('# s03\n')
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('s01-first', page)                              # it opens on the first group
        self.assertIn('s02-second', page)
        self.assertIn('s03-third', page)                             # the ungrouped get the last button
        page = body(frame.Theme(name='work'), self.root, self.block, 'studio', 'Other')
        self.assertIn('s03-third', page)
        self.assertNotIn('s01-first', page)

    def test_every_section_shows_its_views_above_the_purpose_and_no_count_line(self):
        """JL 261031, b10 r01: the view buttons sit above the Purpose (Q1 B), a single view keeps its bar (Q2 note),
        and no "3 topics" or "2 Jobs" line under the title (Q4 note)."""
        (self.block / 'board.md').write_text('---\ntitle: b01\n---\n# b01\n\n## Purpose\n\nOne purpose line.\n')
        topic = self.block / 'studio' / 's01-first'
        topic.mkdir(parents=True)
        (topic / 's01-first.md').write_text('# s01\n**Tags:** Alpha\n')
        for section in ('studio', 'work', 'report'):
            page = focus_page.render(frame.Theme(name='work'), self.root, self.block, section)
            main = page[page.index('<main'):]
            self.assertIn('class="section-views', main, section)              # one group, one view: still a bar
            if 'focus-goal' in main:
                self.assertLess(main.index('class="section-views'), main.index('focus-goal'), section)
            self.assertNotIn('card-sub', main, section)
            if section != 'work':                                             # Work opens on Status, whose Job rows say "3 Tasks" (JL 261104)
                self.assertNotRegex(main, r'\b\d+ (?:topics?|Jobs?|Tasks?|Runs?|events)\b', section)

    def test_a_theme_block_report_shows_its_block_job_and_task_ui_live(self):
        """JL 261031: "I think you should have these as well ... the block UI, job UI and task UI"."""
        job = self.block / 'j01_x'
        job.mkdir(exist_ok=True)
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text('# b01\n\ntheme: paper\nui-block: http://example.org/board?a=1&b=2\n'
                                             f'ui-job: {rel}\nui-task: javascript:alert(1)\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report')
        bar = page[page.index('class="section-views'):]
        bar = bar[:bar.index('</nav>')]
        self.assertLess(bar.index('Questions') if 'Questions' in bar else -1, bar.index('Block UI'))
        self.assertLess(bar.index('Block UI'), bar.index('Job UI'))
        self.assertLess(bar.index('Job UI'), bar.index('Task UI'))
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertNotIn('data-src="http://example.org', page)          # another server: no blank frame (261106)
        self.assertIn('lives on another server', page)
        self.assertIn('href="http://example.org/board?a=1&amp;b=2"', page)
        self.assertIn('1 · 🖥️ The page, live', page)                  # a numbered section like every view (261105)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertRegex(page, r'<iframe class="ui-page" title="Job UI[^"]*"[^>]*src="[^"]*path=' + re.escape(rel.replace('/', '%2F')))
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        self.assertNotIn('src="javascript', page)                         # only http(s) or a page of this SPACE
        self.assertIn('is not a page here', page)

    def test_ui_matrix_turns_types_into_columns_and_says_a_shared_row_once(self):
        source = self.block / 'matrix.md'
        source.write_text('| Category | Block Type | Use Cases | MindMap | Status |\n|---|---|---|---|---|\n'
                          '| Work | Data | Pipelines | Sources<br>Pipeline | Jobs |\n'
                          '| Work | Models | Experiments | Questions | Runs |\n'
                          '| CoWork | Coordination | Requests | Roles | Waiting |\n'
                          '| All | Around | — | Studio<br>Files | Studio<br>Files |\n')
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('style="--ui-type-count:3"', html)                      # only real types reserve horizontal space
        self.assertIn('<colgroup><col class="ui-view-column"><col><col><col></colgroup>', html)
        self.assertIn('<th class="ui-category" colspan="2">Work</th>', html)   # adjacent types share their category
        self.assertIn('<th class="ui-category" colspan="1">CoWork</th>', html)
        self.assertEqual(html.count('class="ui-block-type"'), 3)               # a column per type
        self.assertIn('<th class="ui-view" scope="row">Use Cases</th><td>Pipelines</td><td>Experiments</td>', html)
        self.assertIn('Sources<br>Pipeline', html)
        self.assertEqual(html.count('class="ui-span" colspan="3"'), 1)          # the shared row, said once across them
        self.assertNotIn('<td>Around</td>', html)

    def test_ui_type_matrix_is_opt_in_and_scoped_to_its_level(self):
        job = self.block / 'j01_example'
        job.mkdir()
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text(f'# Example\nui-block: {rel}\nui-job: {rel}\n')
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'block-views.md').write_text('| Block Type | MindMap | Status | Findings |\n'
                                         '|---|---|---|---|\n| Theme building | Structure | Design | Rules |\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertIn('1 · 📋 Block Type × View Button', page)
        self.assertIn('2 · 🖥️ The page, live', page)
        self.assertIn('class="pb-tabset pb-side"', page)     # one example keeps the same left-list/right-preview layout
        self.assertIn('data-pbtab="fUBx0"', page)
        self.assertIn('data-pbpanel="fUBx0"', page)
        self.assertIn('🙋 Interaction', page)
        self.assertNotIn('3 · 🙋 Interaction', page)
        self.assertIn('<th>MindMap</th>', page)
        self.assertIn('Theme building', page)
        self.assertNotRegex(page, r'<details[^>]*\bopen\b[^>]*>\s*<summary[^>]*>1 · 📋')
        job_page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertNotIn('Theme building', job_page)
        self.assertIn('1 · 🖥️ The page, live', job_page)

    def test_matrix_help_uses_authored_view_context_and_escapes_content(self):
        source = self.block / 'job-views.md'
        source.write_text('| Category | Job Type | Findings |\n|---|---|---|\n'
                          '| Work | Data | Results<br>Skills |\n')
        (self.block / 'view-guide.json').write_text(json.dumps({
            'sections': {
                'Results': {'what': '<script>alert(1)</script>', 'outcome': 'A verified output.',
                            'layout': 'Left tabs · Right content', 'example': 'Show {result}.'},
                'Skills': {'what': 'Relevant skills.'}},
            'types': {'Data': {'result': 'a dataset'}},
            'skills': {'Findings': ['haipipe-{level} — Check the work.']}}))
        page = focus_page.ui_matrix_html(source, self.root)
        self.assertEqual(page.count('class="matrix-section"'), 2)
        self.assertIn('data-context="Job · Data · Findings"', page)
        self.assertIn('data-example="Show a dataset."', page)
        self.assertIn('haipipe-job — Check the work.', page)
        self.assertIn('data-layout="Left tabs · Right content"', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertNotIn('<script>alert(1)</script>', page)
        self.assertIn('aria-haspopup="dialog"', page)
        self.assertIn('aria-labelledby="matrix-help-job-views"', page)

    def test_matrix_examples_use_theme_view_routes_and_keep_default_routes(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'block-views.md'
        source.write_text('| Category | Block Type | Story | Delivery | Findings |\n|---|---|---|---|---|\n'
                          '| Paper | Paper Board | Pitch | Outputs | Answers |\n')
        guide = {'sections': {key: {'what': key} for key in ('Pitch', 'Outputs', 'Answers')},
                 'examples': {'block': {'Paper Board': self.block.relative_to(self.root).as_posix()}},
                 'view_routes': {'Story': {'section': 'report', 'group': 'story'},
                                 'Delivery': {'section': 'delivery', 'group': ''}}}
        config = ui / 'view-guide.json'
        config.write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('section=report&amp;group=story', html)
        self.assertIn('section=delivery&amp;group=', html)
        self.assertIn('section=report&amp;group=findings', html)
        guide['proposed'] = True
        config.write_text(json.dumps(guide))
        self.assertNotIn('data-url="/_board', focus_page.ui_matrix_html(source, self.root))

    def test_matrix_use_cases_are_metadata_and_do_not_shift_view_routes(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'job-views.md'
        source.write_text('| Category | Job Type | Use Cases | Overview | Status |\n'
                          '|---|---|---|---|---|\n'
                          '| Work | Job | Goal<br>Model training | Goal | Tasks |\n')
        guide = {'sections': {'Goal': {'what': 'Goal'}, 'Tasks': {'what': 'Tasks'}},
                 'examples': {'job': {'Job': self.block.relative_to(self.root).as_posix()}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('data-context="Job · Job · Use Cases"', html)
        cases = re.findall(r'<button[^>]*data-template=[^>]*>', html)
        self.assertEqual(len(cases), 2)
        self.assertTrue(all('data-url=' not in tag for tag in cases))
        self.assertIn('No linked examples yet.', html)
        self.assertIn('data-context="Job · Job · Overview"', html)
        self.assertIn('section=report&amp;group=overview', html)
        self.assertIn('section=report&amp;group=standing', html)

    def test_matrix_type_routes_keep_same_named_views_separate(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'job-views.md'
        source.write_text('| Category | Job Type | Values | Display |\n|---|---|---|---|\n'
                          '| Paper | Version | Items | Preview |\n| Paper | Evidence | Items | — |\n')
        ref = self.block.relative_to(self.root).as_posix()
        guide = {'sections': {'Items': {'what': 'Values'}, 'Preview': {'what': 'Conditional'}},
                 'examples': {'job': {'Version': ref, 'Evidence': ref}},
                 'view_routes': {'Values': {'section': 'report', 'group': 'values'}},
                 'type_view_routes': {'job': {'Evidence': {'Values': {'group': 'value-list'}},
                                             'Version': {'Display': {'example': False}}}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        html = focus_page.ui_matrix_html(source, self.root)
        self.assertIn('section=report&amp;group=values', html)
        self.assertIn('section=report&amp;group=value-list', html)
        preview = re.search(r'<button[^>]*data-title="Preview"[^>]*>', html).group()
        self.assertIn('data-url=""', preview)

    def test_ui_proposal_is_opt_in_and_topics_keep_separate_panels(self):
        example = self.block / 'b90_example'
        example.mkdir()
        ref = example.relative_to(self.root).as_posix()
        before = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        self.assertNotIn('Work Structure', before)
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'structure.md').write_text('Proposal\n\n## Overview\nGoal\n\n## Status\nSample only\n'
                                        '\n### Data <script>\nDataset check\n\n### Release\nPackaging\n')
        page = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        self.assertIn('1 · 🧭 Work Structure', page)
        self.assertIn('Proposed', page)
        self.assertIn('data-pbtab="proposal-topic-30"', page)
        self.assertIn('data-pbpanel="proposal-topic-31" hidden', page)
        self.assertIn('Data &lt;script&gt;', page)
        self.assertNotIn('Data <script>', page)
        self.assertIn('2 · 🖥️ The page, live', page)

    def test_proposed_matrix_does_not_link_to_unimplemented_live_views(self):
        ui = self.block / 'ui'
        ui.mkdir()
        source = ui / 'block-views.md'
        source.write_text('| Category | Block Type | Overview |\n|---|---|---|\n| Work | Execution | Goal |\n')
        guide = {'sections': {'Goal': {'what': 'An intended outcome.'}},
                 'examples': {'block': {'Execution': self.block.relative_to(self.root).as_posix()}}}
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        self.assertIn('data-url="/_board/workbench?', focus_page.ui_matrix_html(source, self.root))
        guide['proposed'] = True
        (ui / 'view-guide.json').write_text(json.dumps(guide))
        self.assertIn('data-url=""', focus_page.ui_matrix_html(source, self.root))

    def test_ui_example_type_names_the_tab_without_changing_its_page(self):
        example = self.block / 'b90_example'
        example.mkdir()
        (example / 'board.md').write_text('# Example\n')
        ref = example.relative_to(self.root).as_posix()
        ui = self.block / 'ui'
        ui.mkdir()
        (ui / 'example-types.json').write_text(json.dumps({'block': {ref: '📈 Statistical Analysis'}}))
        page = focus_page.ui_view(ref, 'Block UI', self.root, self.block)
        tab = re.search(r'<button[^>]*data-pbtab="fUBx0".*?</button>', page, re.S)[0]
        self.assertIn('📈 Statistical Analysis', tab)
        self.assertNotIn('b90_example', tab)
        self.assertIn('Block UI · b90_example', page)
        self.assertIn('Open b90_example', page)
        self.assertIn('path=' + ref.replace('/', '%2F'), page)
        job = focus_page.ui_view(ref, 'Job UI', self.root, self.block)
        self.assertNotIn('📈 Statistical Analysis', job)

    def test_a_tools_blueprint_names_its_example_from_the_tools_root_in_any_space(self):
        """261105: a Tools theme Block names its placeholder as `blueprints/...`; inside a SPACE, Tools sits at `Tools/`,
        so the path is found from the Block's own checkout and framed by its path from the SPACE root."""
        tools = self.root / 'Tools'
        block = tools / 'blueprints/Project-X/work/b16_theme_x'
        example = tools / 'blueprints/Project-X/paper/Paper-Example'
        block.mkdir(parents=True)
        example.mkdir(parents=True)
        html = focus_page.ui_view('blueprints/Project-X/paper/Paper-Example', 'Block UI', self.root, block)
        self.assertRegex(html, r'<iframe class="ui-page" title="Block UI[^"]*"[^>]*src="[^"]*path=Tools%2Fblueprints%2FProject-X%2Fpaper%2FPaper-Example')
        for bad in ('../outside', 'blueprints/../../outside', '/etc', 'blueprints/Project-X/paper/Missing'):
            self.assertIn('is not a page here', focus_page.ui_view(bad, 'Block UI', self.root, block), bad)

    def test_each_kind_of_page_at_a_level_is_a_side_tab(self):
        """JL 261105: "they are all the task, but different UI"; "for the paper's job, we might have different versions"."""
        a, b = self.block / 'j01_x' / 't01_items', self.block / 'j01_x' / 't02_meaning'
        a.mkdir(parents=True)
        b.mkdir()
        (a / 't01_items.md').write_text('# t01 · Items\ntask-type: labeling-items\n')
        (b / 't02_meaning.md').write_text('# t02 · Meaning\ntask-type: labeling-meaning\n')
        ra, rb = (p.relative_to(self.root).as_posix() for p in (a, b))
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: labeling\nui-task: {ra}\nui-task: {rb}\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        self.assertIn('1 · 🖥️ The pages, live', page)
        self.assertIn('t01_items', page)
        self.assertIn('labeling items', page)                          # each tab says its kind
        self.assertIn('t02_meaning', page)
        self.assertIn('labeling meaning', page)
        self.assertIn('pb-list', page)                                  # side tabs: the kind left, the page right
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'task.html').write_text('<!doctype html>')      # only the first kind walked
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-task')
        walks = page.split('2 · 🎬 Walkthroughs', 1)[1]                    # the same tabs, in the same order (261105)
        self.assertLess(walks.index('t01_items'), walks.index('t02_meaning'))
        self.assertIn('Not recorded', walks)

    def test_work_on_a_ui_view_says_what_each_kind_still_needs(self):
        """JL 261105: "so we should update the work as well for each tab of UI, right?"."""
        a, b = self.block / 'j01_x' / 't01_items', self.block / 'j01_x' / 't02_meaning'
        a.mkdir(parents=True)
        b.mkdir()
        ra, rb = (p.relative_to(self.root).as_posix() for p in (a, b))
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: labeling\nui-task: {ra}\nui-task: {rb}\n\n## Purpose\n\nOne line.\n')
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'task.html').write_text('<!doctype html>')          # the first kind's walk
        rv = self.block / 'topic' / 'review'
        rv.mkdir(parents=True)
        (rv / 'page-s2-r01.md').write_text(f'```text\npage     http://x/_board/workbench?path={ra} (Report)\n'
                                           'score    mean 6.0/10 · not yet\n```\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work', 'ui-task')
        self.assertNotIn('🎬 Walks to record', page)
        checklist = focus_page.ui_walk_checklist(self.block, self.root, 'ui-task')
        self.assertIn('t02_meaning', checklist)
        self.assertIn('Not recorded', checklist)
        self.assertIn('Recorded', checklist)
        self.assertIn('🔍 Review rounds', page)
        self.assertIn('6.0 of 10 · not yet', page)                                # t01's newest round
        self.assertIn('not reviewed yet', page)                                   # t02's

    def test_a_theme_block_shows_its_walk_under_the_live_page(self):
        """JL 261105: "could you embed the gif as the report as well?"; "a very quick video and we can pause"."""
        job = self.block / 'j01_x'
        job.mkdir(exist_ok=True)
        (self.block / 'walks').mkdir()
        (self.block / 'walks' / 'block.html').write_text('<!doctype html><title>walk</title>')
        rel = job.relative_to(self.root).as_posix()
        (self.block / 'board.md').write_text(f'# b01\n\ntheme: paper\nui-block: {rel}\nui-job: {rel}\n\n## Purpose\n\nOne line.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-block')
        self.assertIn('2 · 🎬 Walkthroughs', page)                         # the second section, under the live page
        self.assertIn('walks/block.html', page)
        self.assertIn('🙋 Interaction', page)
        self.assertNotIn('3 · 🙋 Interaction', page)                       # then Interaction, last as on every view
        empty_walk = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'ui-job')
        self.assertIn('🎬 Walkthroughs', empty_walk)
        self.assertIn('Not recorded', empty_walk)

    def test_a_live_page_written_from_its_face_opens_on_any_server(self):
        """261106: a live page's url with no leading / is from its face's folder, so a SPACE's and Tools' own server
        both open it."""
        site = self.block / 'delivery' / 'web'
        site.mkdir(parents=True)
        (site / 'index.html').write_text('<!doctype html>')
        item = {'url': 'delivery/web/index.html', 'folder': self.block / 'j01_x', 'face': self.block}
        self.assertIn('b01_study/delivery/web/index.html', frame.live_url(item, self.root))
        self.assertEqual(frame.live_url({'url': 'https://example.org/x', 'folder': self.block}, self.root), 'https://example.org/x')
        self.assertEqual(frame.live_url({'url': 'delivery/none.html', 'folder': self.block}, self.root), 'delivery/none.html')

    def test_skills_is_a_rail_section_with_the_page_s_skills(self):
        """JL 261105: "a new tab in the right rail, named 'SKILL', and we can show the most relevent skills"."""
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'skills')
        self.assertIn('>🧰 Skills<', page)
        self.assertIn('Copy prompt', page)
        self.assertIn('/haipipe-work', page)                         # the theme's door first
        self.assertIn('/haipipe-block', page)                        # then the level's skill
        self.assertIn('Copy prompt', page)
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')
        self.assertNotIn('Skills that do it', work)                  # shown once: the rail, not every view's Process

    def test_a_finished_run_reads_done_with_its_headline(self):
        """261105: a receipt saying `completed` read ⬜; every mark has its word, and headline.txt is read."""
        run = self.block / 'j01_x' / 't01_y' / 'runs' / 'r01_z'
        (run / 'result').mkdir(parents=True)
        (run / 'result' / 'runtime.yaml').write_text('run: r01_z\nstatus: completed\n')
        (run / 'result' / 'headline.txt').write_text('9 values\n')
        ((_, mark, head),) = focus_page.run_rows(run.parent.parent)
        self.assertEqual((mark, head), ('✅ done', '9 values'))

    def test_an_sNN_card_shows_its_delivery_type_beside_its_stage(self):
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n\n**Delivery type:** skill\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('<span class="row-type" title="delivery type">skill</span>', page)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Delivery type:** deck\n')   # never a type
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertNotIn('class="row-type"', page)

    def test_a_deliverable_with_a_url_is_a_closed_live_card_in_delivery(self):
        job = self.block / 'j01_x'
        (job / 't01_y').mkdir(parents=True)
        (job / 'j01_x.md').write_text('# x\n\n## Deliverables\n\n```yaml\ndeliverables:\n- what: The try page\n'
                                      '  task: t01_y\n  url: /_api/try/food\n- what: A table\n  task: t01_y\n```\n')
        for folder in (self.block, job, job / 't01_y'):
            html = focus_page.delivery_html(folder, self.root)
            self.assertIn('data-src="/_api/try/food"', html)              # the page itself, loaded only when opened
            self.assertIn('<details class=live-page ', html)              # closed: no `open` (AGENTS rule 15)
            self.assertNotIn(' src="/_api', html)
            self.assertNotIn('A table', html)
        other = self.block / 'j02_z'
        other.mkdir()
        self.assertEqual(focus_page.delivery_html(other, self.root), '')  # another Job has no part of it
        service = focus_page.findings_board([], self.block, self.root)    # Findings: a closed section, one tab per site
        self.assertIn('🌐 Service', service)
        self.assertIn('data-src="/_api/try/food"', service)
        self.assertNotIn('🌐 Service', focus_page.findings_board([], other, self.root))
        items = frame.delivery_items(self.block)                          # the classic view, from one reading
        self.assertEqual([(i['title'], i['fixed'], i['url']) for i in items],
                         [('The try page', ['Live page'], '/_api/try/food')])

    def test_an_sNN_with_a_delivery_gets_a_delivery_button_and_section(self):
        topic = self.block / 's01-first'
        (topic / 'delivery' / 'skill').mkdir(parents=True)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n')
        (topic / 'delivery' / 'skill' / 'rule.md').write_text('the rule\n')
        (topic / 'delivery' / 'render.yaml').write_text('pieces:\n  - code: "the screen"\n    by: j01_x/t01_y\n')
        run = self.block / 'j01_x' / 't01_y' / 'runs' / 'run-a'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('status: done\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('view=focus-delivery', page)                        # a pop-out, like Draw and Mind map
        self.assertIn('· Delivery" href=', page)
        self.assertIn('>Delivery</button>', page)
        self.assertIn('✅ the screen', focus_page.delivery_document(topic, self.root))
        page = focus_page.delivery_document(topic, self.root)
        self.assertIn('✅ the screen', page)                               # a Task's Runs all done
        self.assertLess(page.index('1 · Delivery'), page.index('2 · Render'))   # the thing, then where it goes
        self.assertIn('built by t01_y, done', page)
        self.assertIn('skill/rule.md', page)                              # what it holds
        self.assertIn('<details class="deliv-file"><summary>skill/rule.md</summary>', page)   # opens in place
        self.assertIn('the rule', page)

    def test_a_builder_page_leads_back_to_the_sNN_card(self):
        topic = self.block / 's01-first'
        (topic / 'delivery' / 'web').mkdir(parents=True)
        (topic / 's01-first.md').write_text('s01 · first\n=====\n\n**Stage:** explore\n')
        (topic / 'delivery' / 'web' / 'index.html').write_text('<p>x</p>')
        (self.block / 'j01_x').mkdir()
        page = focus_page.static_page(topic, self.root, 'preview', '<p>the content</p>', 'review prototype')
        rail = page.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        home = frame.esc(focus_page.topic_home(topic, self.root))
        self.assertIn(home, rail)                                        # its level's sNN, each to its card, and Jobs
        self.assertIn('j01_x', rail)
        self.assertIn(f'<a href="{home}">s01-first</a>', page)          # the path ends at its card
        self.assertIn('aria-current="page">Preview</a>', page)           # Delivery's views under the title
        self.assertIn('view=focus-delivery', page)                       # Overview: the card's Delivery pop-out
        self.assertIn('<span class="row-stage">review prototype</span>', page)
        self.assertIn('<p>the content</p>', page)

    def test_external_symlinks_are_not_read(self):
        with tempfile.TemporaryDirectory() as other:
            external = Path(other)
            (external / 'j01_outside.md').write_text('# Private text\n')
            (self.block / 'j01_outside').symlink_to(external, target_is_directory=True)
            page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'children')
            self.assertNotIn('Private text', page)
            self.assertNotIn('j01_outside', page)
            self.assertNotIn('j01_outside', focus_page.folder_html(self.block, self.root))

    def test_log_dates_are_authored_and_sorted(self):
        events = focus_page.log_events('261020 0037 · Second\n260908 · First\n261332 · Bad date\nUndated\n')
        self.assertEqual([e[0] for e in events], ['2026-09-08', '2026-10-20'])

    def test_focus_route_and_old_route_remain_distinct(self):
        handler = FrameMixin()
        handler.root = self.root
        handler.guide_send = lambda body, code, *args, **kwargs: (body, code)
        handler.path = '/_board/workbench?path=b01_study&layout=focus'
        with patch.object(frame, 'themes', return_value={'vanilla': frame.VANILLA}), patch.object(frame, 'render', return_value='legacy'):
            page, status = handler.workbench_frame_view()
            self.assertEqual(status, 200)
            self.assertIn('Compare the methods.', page)
            handler.path = '/_board/workbench?path=b01_study'
            self.assertEqual(handler.workbench_frame_view(), ('legacy', 200))
            handler.path = '/_board/workbench?path=../outside&layout=focus'
            self.assertEqual(handler.workbench_frame_view()[1], 404)


    def write_task(self, job, name, state, figure=False):
        task = self.block / job / name
        task.mkdir(parents=True, exist_ok=True)
        (task / (name + '.md')).write_text(f'# {name}\ngoal: Goal of {name}.\nstate: {state}\n')
        if figure:
            result = task / 'runs' / 'r01_first' / 'result'
            result.mkdir(parents=True)
            (result / 'figure.png').write_bytes(b'png')
            (result / 'display.yaml').write_text('question: Does it differ by region?\n')
            (result / 'headline.txt').write_text('It differs little.\n')
        return task

    def test_report_status_lists_each_job_and_its_tasks(self):
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare two methods.\nnext: settle 3 scores\n')
        self.write_task('j01_compare', 't01_first', '🟡 RESULTS IN, UNREAD · r01 complete')
        self.write_task('j01_compare', 't02_second', '🟡 RESULTS IN, UNREAD · r01 complete')
        self.write_task('j01_compare', 't03_third', '🟠 WAITING FOR A PERSON · pick a cut')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'standing')   # Report opens on MindMap (JL 261031)
        self.assertIn('<details class=band-sec><summary>1 · ', page)   # a Block's Status: one closed section per band (JL 261104)
        self.assertIn('<details class=job-row>', page)     # a row per Job (JL 261104), its short name
        self.assertIn('<b>compare</b>', page)
        self.assertIn('data-pop="t03_third"', page)        # the row opens to its Tasks
        self.assertIn('<ul class=fold-tree>', page)        # Jobs and Tasks first (JL 261108); its one Topic is its one
        self.assertIn('🧩 View BJTR', page)                # Topic navigation remains available beside the flat status
        self.assertNotIn('Next: settle 3 scores', page)    # no "Next:" lines (JL 261104: "just delete them")
        self.assertIn('<span class=jn>j01</span>', page)   # its jNN, then how far in words (JL 261108, the 261105 look)
        self.assertIn('· 3 Tasks', page)
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')   # Work opens on the same Status (JL 261104)
        self.assertIn('<ul class=fold-tree>', work)
        self.assertIn('data-pop="j01_compare" title="j01_compare: Compare two methods"><b>compare</b>', work)   # its folder and goal on hover
        self.assertIn('data-pop="t03_third"', work)
        self.assertIn('<span class=st>🟠 waiting for a person</span>', work)
        self.assertNotIn('🚧 Next steps', work)
        self.assertIn('🧩 View BJTR', work)
        self.assertIn('class="work-topic-tree"', work)

    def test_job_rows_show_each_task_output_in_place(self):
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare two methods.\n')
        self.write_task('j01_compare', 't01_first', '🔶 DRAWN, REVIEW OPEN · r01 drawn', figure=True)
        page = focus_page.render(frame.Theme(name='work'), self.root, job)
        self.assertIn('<figure class="row-output">', page)
        self.assertIn('Does it differ by region?', page)
        self.assertIn('It differs little.', page)
        self.assertIn('🔶 drawn, review open', page)
        self.assertIn('<details class=job-row>', page)       # its Tasks fold, the output inside (JL 261102), the
        self.assertIn('<div class=job-tree><figure class="row-output">', page)   # Block's look (round 2, 261106)
        self.assertIn('<span class=hl>It differs little.</span>', page)          # its headline on its closed row

    def test_block_with_answers_opens_on_findings(self):
        report_dir = self.block / 'reports' / 'q01_compare'
        report_dir.mkdir(parents=True)
        (report_dir / 'q01_compare.md').write_text('# Comparison\nstate: 🟡 DRAFT\n## Opening\nAn answer.\n')
        self.face.write_text('# Study\nspine: Compare the methods.\n## Questions\n```yaml\nquestions:\n'
                             '- id: Q01\n  title: Compare\n  report: reports/q01_compare/q01_compare.md\n'
                             '- id: Q02\n  title: Second\n```\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'findings')
        self.assertIn('An answer.', page)                               # a Block's answers: in Findings, not its map (261103)
        self.assertIn('Findings', page)

    def test_studio_rows_show_topic_line_stage_and_preview(self):
        topic = self.block / 'studio' / 's01-first'
        topic.mkdir(parents=True)
        (topic / 's01-first.md').write_text('# s01\n**Tags:** Alpha\n\n**Stage:** explore\n\n**Topic:** what the first topic asks\n')
        (topic / 's01-first.excalidraw').write_text('{}')
        (topic / 's01-first.png').write_bytes(b'png')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('what the first topic asks', page)
        self.assertIn('<span class="row-stage">explore</span>', page)   # the stage, one word (JL 261029: overwhelmed)
        self.assertNotIn('rounds</span>', page)                            # no bookkeeping on the row
        self.assertIn('>Draw</button>', page)
        self.assertIn('s01-first.png', page)
        self.assertNotIn('Mind map', page)

    def test_a_topic_shows_its_address_and_hangs_on_its_job(self):
        studio = self.block / 'studio'
        for name, at in (('s01-whole', 'b01'), ('s07-one-table', 'j01'), ('s09-cut', 'j01.t03')):
            (studio / name).mkdir(parents=True)
            (studio / name / f'{name}.md').write_text(f'# {name}\n**Stage:** explore\n\n**At:** {at}\n\n**Topic:** about {name}\n')
        job = self.block / 'j01_tables'
        (job / 't03_cut').mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# Tables\ngoal: Build the tables.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio')
        self.assertIn('id="s01-whole"', page)   # s01-D03
        self.assertIn('about s01-whole', page)
        self.assertIn('id="s07-one-table"', page)
        self.assertIn('about s07-one-table', page)                                   # a '-' inside a name becomes '_'
        self.assertIn('id="s09-cut"', page)
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')
        self.assertNotIn('open points wait on you', work)    # Status keeps to the work's state (261106): the open
                                                             # topics are the Studio's, what waits the view's 🙋 Interaction
        page = focus_page.render(frame.Theme(name='work'), self.root, job, 'studio')        # s01-D01: the Job sees its own
        self.assertIn('about s07-one-table', page)
        self.assertIn('about s09-cut', page)
        self.assertNotIn('about s01-whole', page)

    def test_a_topic_link_lands_on_its_card_in_its_group(self):
        # JL 261031: "we will remove the single page for the studio"; the rail's sNN points to its card in section=studio
        topic = self.block / 'studio' / 's05-what-is'
        topic.mkdir(parents=True)
        (topic / 's05-what-is.md').write_text(
            's05 · What is it?\n=================\n\n**Tags:** Interface\n\n**Stage:** shaping\n\n**At:** b01\n\n'
            '**Topic:** what it is. And more words.\n')
        home = focus_page.topic_home(topic, self.root)
        self.assertIn('section=studio&group=Interface#s05-what-is', home)   # its group, so the card is on screen
        studio = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio', 'Interface')
        self.assertIn('id="s05-what-is"', studio)
        self.assertNotIn(frame.esc(focus_page.page_url(topic, self.root)), studio)   # nothing links the old page
        self.assertIn('id="s05-what-is"', studio)          # its line opens the face, popped out
        self.assertIn('what it is.', studio)

    def test_block_map_hangs_each_topic_on_its_rung(self):
        """JL 261029: "each sNN should be just below bNN"; a Block's topics in their groups, each one short line, whole
        (its title), its why, delivery and first open question behind ▸ (JL 261030), no open-question leaves."""
        for name, tag, at, ask in (('s01-what', 'What a topic is', 'b01', 'Who says agreed?'),
                                   ('s02-life', 'What a topic is', 'b01', 'Kept or deleted?'),
                                   ('s03-links', 'How topics connect', 'b01', 'Full label?'),
                                   ('s04-cut', 'What a topic is', 'j01', 'Which cut first?')):
            (self.block / 'studio' / name).mkdir(parents=True, exist_ok=True)
            (self.block / 'studio' / name / f'{name}.md').write_text(
                f'{name[:3]} · What is {name}, said in full?\n=====\n\n**Tags:** {tag}\n\n**At:** {at}\n\n**For:** a deck '
                f'and a rule (JL 261030: "x").\n\n**Topic:** about {name}.\n\nOpen\n----\n\n1. {ask}\n')
        (self.block / 'studio' / '_groups.txt').write_text('How topics connect\nWhat a topic is\n')
        job = self.block / 'j01_tables'
        job.mkdir(exist_ok=True)
        (job / 'j01_tables.md').write_text('# j01 · Tables\n\ngoal: Make the tables.\n')
        page = focus_page.parts_mindmap(self.block, self.root)        # the full map; the page shows page_tree (JL 261031)
        self.assertNotIn('Studio · ', page)                                          # no node only the folder has
        self.assertIn('>How topics connect<', page)
        self.assertNotIn('1 topic', page)                                             # a label carries no count
        self.assertLess(page.index('>How topics connect<'), page.index('>What a topic is<'))   # _groups.txt order
        self.assertIn('What is s01-what, said in full?', page)                       # its title, whole
        self.assertIn('Still open: Who says agreed?', page)                          # in its box, one plain paragraph (b32 s42)
        self.assertIn('Delivers a deck and a rule', page)                           # its For:, the JL quote dropped
        self.assertNotIn('data-raw="open"', page)                                    # no open-question leaves
        self.assertLess(page.index('j01_tables'), page.index('s04-cut'))             # At: j01 hangs under its Job
        self.assertNotIn('pm-draw', page)                                            # no quick drawing yet, no ✎
        (self.block / 'studio' / 's01-what' / 's01-what.excalidraw').write_text('{}')
        page = focus_page.parts_mindmap(self.block, self.root)
        self.assertIn('pm-draw" data-pop="s01-what"', page)                       # its label opens its quick drawing
        self.assertIn('s01-what.excalidraw', page)

    def test_block_map_says_questions_and_short_labels(self):
        """JL 261104: "what does this mean?" of "To find out" and "draft"; long folder names ran past their card."""
        job = self.block / 'j61_a_very_long_folder_name_for_this_job'
        job.mkdir(exist_ok=True)
        (job / f'{job.name}.md').write_text('# j61 · Scores\n\ngoal: Score them.\n')
        with patch.object(focus_page, 'owned_register', return_value=([{'id': 'Q01', 'title': 'Short', 'question': 'Is it trained?'}], '')):
            page = focus_page.parts_mindmap(self.block, self.root)
        self.assertIn('>Questions<', page)
        self.assertNotIn('To find out', page)
        self.assertIn('Is it trained?', page)                                        # the question, not its title
        self.assertIn('⬜ no answer yet', page)
        self.assertIn('title="j61_a_very_long_folder_name_for_this_job">Job 61</span>', page)   # words, no "j61" (round 3)

    def test_block_bands_group_jobs_in_the_same_map(self):
        """JL 261104: 15 flat Jobs were too tall; the same map, one card per band of the face's `bands:`."""
        job = self.block / 'j61_scores'
        job.mkdir(exist_ok=True)
        (job / f'{job.name}.md').write_text('# j61 · pretrain: Scores\n\ngoal: Score them.\n')
        self.face.write_text(self.face.read_text() + 'bands: j6N 📏 eval\n')
        page = focus_page.parts_mindmap(self.block, self.root)
        self.assertIn('pm-folds', page)
        self.assertIn('📏 Eval', page)
        self.assertIn('Scores', page)

    def test_report_opens_on_the_mindmap_with_every_item_closed(self):
        """JL 261031: "show the mindmap all the time"; the compact map beside every section was removed ("we don't need
        this"): Report opens on the MindMap. JL 261104 replaced "every item open": "默认的话，大家都是合着的"."""
        for name, tag in (('s01-first', 'Alpha'), ('s02-second', 'Beta')):        # topics in their groups, as a Block has
            topic = self.block / name
            topic.mkdir()
            (topic / f'{name}.md').write_text(f'{name[:3]} · An idea\n=====\n\n**Tags:** {tag}\n\n**At:** b01\n\n'
                                              f'**Topic:** about {name}.\n\n**For:** a deck and a rule.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block)
        self.assertIn('aria-current="page">Overview</a>', page)                   # the first view, opened by default
        self.assertIn('class="focus-map fit-map"', page)                         # it fits its box (round 3)
        self.assertIn('Delivers a deck and a rule', page)                         # one plain paragraph, as the draft map
        self.assertIn('<div class=pm-detail hidden><p', page)                    # every item starts closed (JL 261104)
        self.assertIn('class="pm pm-folds"', page)
        self.assertNotRegex(page, r'class="[^"]*pm-on')                         # nothing drawn open; no <details open> either
        self.assertNotRegex(page, r'<details[^>]*\bopen\b')
        self.assertNotIn('page-tree', page)                                      # no map column

    def test_one_interaction_record_serves_the_inbox_work_and_the_map(self):
        """JL 261031 (relayed): one record per interaction; an Interactions view that defaults to Needs your input,
        with Answered and All; Work and the map open the same record; answered is not applied."""
        empty = focus_page.render(frame.Theme(name='work'), self.root, self.block)   # always on the rail (JL 261031)
        self.assertIn('>🙋 Interactions<', empty)
        self.assertIn('No Interactions linked to this view.', empty)
        self.assertIn('>Delivery<', empty)                                     # Delivery too (JL 261031)
        self.assertIn('Nothing handed over yet', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'delivery'))
        topic = self.block / 's01-first'
        topic.mkdir()
        (topic / 's01-first.md').write_text('s01 · First idea\n=====\n')
        job = self.block / 'j01_tables'
        task = job / 't01_cut'
        task.mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# j01 · Tables\n\ngoal: Make the tables.\n')
        (task / 't01_cut.md').write_text('# t01 · Cut\nstate: 🔴 OPEN\n')
        wait = task / 'runs' / 'r01_collect_cut_choices'
        wait.mkdir(parents=True)
        (wait / 'run.yaml').write_text('run: r01_collect_cut_choices\nkind: hard\ntype: collect\nstatus: waiting\n')
        (wait / 'question_collection.md').write_text('# Cut choices\n\nfor: b01-s01:study @ first\n\n## Q1 · Cut\n\nWhy.\n\n'
                                                     '**Which cut first?**\n\n- [x] A · Age\n- [ ] B · Sex\n\nWhy A: x.\n')
        (wait / 'r01_collect_cut_choices.html').write_text('<!doctype html>')
        done = job / 'runs' / 'r01_collect_old_choices'
        (done / 'result').mkdir(parents=True)
        (done / 'run.yaml').write_text('run: r01_collect_old_choices\nkind: hard\ntype: collect\nstatus: done\n'
                                       'feeds:\n- b01_study/j01_tables/t01_cut/runs/run-make-x\n')
        (done / 'question_collection.md').write_text('# Old choices\n\n## Q1 · Old\n\nWhy.\n\n**Which one?**\n\n- [x] A · a\n- [ ] B · b\n')
        (done / 'result' / 'answer_collection.md').write_text('# Old choices · answers\n\nreceived: 2026-10-31 12:05\n')
        rows = focus_page.interactions(self.block, self.root)
        self.assertEqual([(r['run'], r['state']) for r in rows],
                         [('r01_collect_cut_choices', 'waiting'), ('r01_collect_old_choices', 'answered')])
        self.assertEqual(rows[0]['topic'], topic)                                 # its for: address names s01
        self.assertEqual(rows[0]['asks'], [('Q1', 'Cut', 'Which cut first?')])
        form = 'href="/b01_study/j01_tables/t01_cut/runs/r01_collect_cut_choices/r01_collect_cut_choices.html"'
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions')
        self.assertIn('data-ixq="Q1"', page)                       # the rail item says something waits, never a count
        self.assertIn('aria-current="page">All</a>', page)          # the default view: all of them (JL 261031)
        self.assertIn('>Answered</a>', page)
        self.assertIn('>All</a>', page)
        self.assertIn('<b>Cut choices</b>', page)
        self.assertIn('data-ixq="Q1"><b>Q1 · Cut</b>', page)                      # what it asks
        self.assertIn('Asked by <a href=', page)                                  # who asked, in words (round 3)
        self.assertIn('title="t01_cut">Cut</a> · about', page)                   # its folder name on hover only
        self.assertIn('>First idea</a>', page)                                    # what it is about, by its title
        self.assertNotIn('<small class=ix-addr>j01 · t01</small>', page)
        self.assertIn(form.replace('href=', 'src='), page)
        self.assertIn('<b>Old choices</b>', page)                               # All shows the answered too
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'waiting')
        self.assertIn('<b>Cut choices</b>', page)
        self.assertNotIn('Old choices', page)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'answered')
        self.assertIn('<b>Old choices</b>', page)
        self.assertIn('answered · 2026-10-31', page)                               # its state and date, no colour tag
        self.assertIn('Applying it belongs to run-make-x.', page)                 # answered is not applied
        self.assertIn('>See answers</a>', page)
        self.assertNotIn('<b>Cut choices</b>', page)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions', 'all')
        self.assertIn('<b>Cut choices</b>', page)
        self.assertIn('<b>Old choices</b>', page)
        self.assertIn('>See answers</a>', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'interactions'))   # no form built: its plain row
        # one button, "Interaction", wherever an item shows; no count and no tag (JL 261031, b16 t01 r04 Q3-Q6); 🙋 when one waits
        button = lambda holder: ('data-pop="' + holder.name + ' · Interaction" href="/_board/workbench?view=focus-part&amp;'
                                 'part=interactions&amp;path=' + str(holder.relative_to(self.root)).replace('/', '%2F') + '"')
        for page in (focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio'),):
            self.assertIn('Interaction</a>', page)
            self.assertIn('>🙋 Interaction</a>', page)       # a waiting question flags it (JL 261031: "flag them as well")
            self.assertNotIn('Questions for you', page)
            self.assertNotIn('Answered</a>', page.replace('>Answered</a>', ''))
        # a Status row whose Job or Task waits on the person carries the same 🙋 Interaction button (JL 261109: "could we
        # change this to the interaction?"), which replaced the row's 🙋 Answer; a row with nothing waiting carries none
        self.assertIn(button(job), focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work'))
        self.assertNotIn('🙋 Answer', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work'))
        self.assertIn(button(topic), focus_page.render(frame.Theme(name='work'), self.root, self.block, 'studio'))
        listed = focus_page.part_document(topic, self.root, 'interactions')      # the pop-out: the topic's items
        self.assertIn('<b>Cut choices</b>', listed)
        self.assertIn('data-ixq="Q1"><b>Q1 · Cut</b>', listed)                     # the standard look: a tab per question
        self.assertIn('waiting for you', listed)
        self.assertIn(form.replace('href=', 'src=') + '></iframe>', listed)          # its own form, on the right
        self.assertNotIn('Old choices', listed)                                    # not about s01
        listed = focus_page.part_document(job, self.root, 'interactions')        # a Job: the items at it or below
        self.assertLess(listed.index('Cut choices'), listed.index('Old choices'))  # the waiting one first

    def test_interaction_closes_every_view_at_every_level(self):
        """JL 261104: "at the bottom for each of the view? not matter for the block, or job or task"; "the standard"."""
        job = self.block / 'j01_tables'
        task = job / 't01_cut'
        task.mkdir(parents=True)
        (job / 'j01_tables.md').write_text('# j01 · Tables\n\ngoal: Make the tables.\n')
        (task / 't01_cut.md').write_text('# t01 · Cut\nstate: 🔴 OPEN\n')
        for page in (self.block, job, task):                                     # none asked: it still stands there
            for section in ('report', 'work'):
                self.assertIn('🙋 Interactions</summary>',
                              focus_page.render(frame.Theme(name='work'), self.root, page, section))
        run = task / 'runs' / 'r01_collect_cut'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_collect_cut\nkind: hard\ntype: collect\nstatus: waiting\nview: status\n')
        (run / 'question_collection.md').write_text('# Cut\n\n## Q1 · Cut\n\nWhy.\n\n**Which?**\n\n- [x] A · a\n- [ ] B · b\n')
        (run / 'r01_collect_cut.html').write_text('<!doctype html>')
        theme = frame.Theme(name='work')
        # The explicit Status assignment is shared at every level; the rail keeps every item.
        for page, view in ((self.block, 'standing'), (job, 'standing'), (task, 'standing')):
            for section, group in (('report', view), ('work', view), ('interactions', '')):
                html = focus_page.render(theme, self.root, page, section, group)
                if section != 'interactions':
                    self.assertIn('🙋 Interactions<span class="word you">1 waits for you</span>', html, (page.name, section))
                self.assertNotIn('🙋 Cut: Q1 · Cut</p>', html, (page.name, section))
                self.assertIn('data-ixq="Q1"', html, (page.name, section))
                if section == 'work':                  # shown once: Process no longer repeats it (JL 261105)
                    self.assertNotIn('Waiting on you', html, page.name)
                    self.assertEqual(html.count('data-ixq="Q1"'), 1, page.name)
        other = focus_page.render(theme, self.root, self.block, 'report', 'mindmap')
        self.assertNotIn('data-ixq="Q1"', other)  # Child inbox belongs to Status; rail aggregates it.
        self.assertIn('data-ixq="Q1"', focus_page.part_document(job, self.root, 'interactions'))
        from live import interaction_section as IX     # numbered after a work band's numbered folds (261105)
        body = '<h3 class=wk-band>📊 Results</h3><details class=band-sec><summary>1 · A</summary></details>' \
               '<details class=band-sec><summary>2 · B</summary></details>'
        self.assertEqual(IX.next_number(body), 3)
        self.assertEqual(IX.next_number('<h3 class=pb-group>RESULTS</h3><section class=fd-sec><h3 class=fd-h>4 · X</h3>'), 5)
        self.assertEqual(IX.next_number('<p>no numbered section</p>'), 0)

    def test_a_bar_carries_its_state_word_and_what_waits_shows_under_it_closed(self):
        """JL 261106: "every closed bar shows a state word on its right, and a section that waits on you also shows that
        one item under its closed bar"; the fold remembers a bar by its title alone, never its word."""
        from live import interaction_section as IX, ui_parts
        from live.focus_draft import JS
        self.assertEqual(ui_parts._section('1 · 🔢 Values', '<p>b</p>', '2 wait for you', '🙋 Q1 · Which?'),
                         '<section class=fd-sec><h3 class=fd-h>1 · 🔢 Values<span class="word you">2 wait for you</span></h3>'
                         '<p class=fd-wait>🙋 Q1 · Which?</p><p>b</p></section>')
        self.assertEqual(ui_parts._section('X', '<p>b</p>', 'done'), '<section class=fd-sec><h3 class=fd-h>X<span class=word>done</span></h3><p>b</p></section>')
        self.assertTrue(ui_parts._numbered(ui_parts._section('X', '<p>b</p>', 'done')).startswith('<section class=fd-sec><h3 class=fd-h>1 · X<span'))
        self.assertEqual(IX.next_number(ui_parts._numbered(ui_parts._section('X', '<p>b</p>', 'done'))), 2)
        for script in (JS, IX.FOLD):                   # the waiting line stays out of the fold; the key skips the word
            self.assertIn("contains('fd-wait')", script)
            self.assertIn("querySelectorAll('.word')", script)
        rows = [('Plan', '', 'done', '', '', False), ('Draw', '', 'waiting for you', '', '', False), ('Run', '', 'not started', '', '', False)]
        self.assertEqual(ui_parts.todo_word(rows), ('1 waits for you', '🙋 Draw'))
        self.assertEqual(ui_parts.todo_word(rows[:1] + rows[2:]), ('1 of 2 done', ''))
        self.assertEqual(ui_parts.todo_word(rows[:1]), ('done', ''))
        self.assertEqual(ui_parts.todo_word([]), ('nothing yet', ''))

    def test_paper_numbered_bars_keep_their_state_words(self):
        """The paper and work placeholders in Tools (blueprints/Project-Ladder) are the prototypes every project gets
        (JL 261105): every numbered bar of every Report and Work view carries its state word (JL 261106)."""
        tools = Path(__file__).resolve().parents[5]
        base = tools / 'blueprints' / 'Project-Ladder'
        board, block = base / 'paper' / 'Paper-Example', base / 'work' / 'b90_example_paper_results'
        if not (board.is_dir() and block.is_dir()):
            self.skipTest('the Tools placeholders are not in this checkout')
        pages = [board] + [j for j in sorted(board.glob('j[0-9]*_*')) if j.is_dir()]
        pages += [next(iter(sorted(j.glob('t00_*'))), None) for j in sorted(board.glob('j1[0-9]_*'))]   # one Section a version
        # Work omits boilerplate availability words; paper retains its contract.
        bar = re.compile(r'<h3 class=fd-h>(\d+ · .*?)</h3>|<details class="?band-sec[^>]*><summary>(\d+ · .*?)</summary>', re.S)
        missing, seen = [], 0
        for page in (p for p in pages if p is not None):
            theme = frame.themes().get(frame.theme_of(page, tools), frame.VANILLA)
            for section in ('report', 'work'):
                nav = re.search(r'<nav class="section-views".*?</nav>', focus_page.render(theme, tools, page, section), re.S)
                for view in dict.fromkeys(re.findall(r'group=([^"&]+)', nav[0]) if nav else ['']):
                    for m in bar.finditer(focus_page.render(theme, tools, page, section, view)):
                        seen += 1
                        title = m.group(1) or m.group(2)
                        if not re.search(r'<span class=(?:word|"word you")>[^<]+</span>', title):
                            missing.append(f'{page.name} {section} {view}: {re.sub("<[^>]+>", "", title)[:60]}')
        self.assertGreater(seen, 100)
        self.assertEqual(missing, [])

    def test_findings_holds_the_forms_its_questions_name(self):
        """JL 261106: a work page's view shows its own items: Findings the forms at a Question's work, Status the forms
        below the page, MindMap the page's own."""
        self.findings_block()
        run = self.block / 'j01_work/t01_read/runs/r02_collect_read'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('status: waiting\nview: findings\n')
        (run / 'question_collection.md').write_text('# Read asks\n\n## Q1 · Read\n\nWhy.\n\n**Which?**\n\n- [ ] A · a\n- [ ] B · b\n')
        (run / 'r02_collect_read.html').write_text('<!doctype html>')
        theme = frame.Theme(name='work')
        found = focus_page.render(theme, self.root, self.block, 'report', 'findings')
        self.assertIn('Read asks', found.split('aria-labelledby="work-shared"', 1)[1].split('<footer>', 1)[0])
        for view in ('standing', 'mindmap'):     # a form that names Findings stays there, even while it waits (261109)
            self.assertNotIn('Read asks', focus_page.render(theme, self.root, self.block, 'report', view).split('aria-labelledby="work-shared"', 1)[1].split('<footer>', 1)[0])
        # Findings' question awaiting agreement shows under its closed bar (JL 261106)
        (self.block / 'reports/q01_a/q01_a.md').write_text('# A\nstate: OPEN\n\n## Opening\n\nProposed (261106): Every table is kept.\n')
        found = focus_page.render(theme, self.root, self.block, 'report', 'findings')
        self.assertIn('<span class="word you">waits for you</span></summary>', found)
        self.assertIn('<p class=band-wait>🙋 Stored tables: its answer waits for your agreement</p>', found)

    def test_a_job_and_a_task_map_show_what_each_child_must_find_out(self):
        """Decided on the lean (261106): a Job's and a Task's MindMap draw each child with its goal, not the Run tree that
        Status shows."""
        job = self.block / 'j01_compare'
        task = job / 't01_first'
        (task / 'runs' / 'r01_fit').mkdir(parents=True)
        (job / 'j01_compare.md').write_text('# j01 · Compare\ngoal: Compare two methods.\n')
        (task / 't01_first.md').write_text('# t01 · First\ngoal: Find out whether the first method holds.\nstate: 🟡 RESULTS IN\n')
        (task / 'runs' / 'r01_fit' / 'run.yaml').write_text('run: r01_fit\nsays: the first fit, by region\nstatus: done\n')
        theme = frame.Theme(name='work')
        jmap = focus_page.render(theme, self.root, job, 'report', 'mindmap')
        self.assertIn('finds out</span><span class=pm-w><span class=pm-t data-edit=words data-raw="Find out whether the first method holds"', jmap)
        self.assertNotIn('r01_fit', jmap)                                  # no Run tree: Status shows it
        tmap = focus_page.render(theme, self.root, task, 'report', 'mindmap')
        self.assertIn('the first fit, by region', tmap)
        self.assertNotIn('✅ done', tmap)
        self.assertIn('r01_fit', focus_page.render(theme, self.root, task, 'report', 'standing'))

    def test_empty_sections_are_hidden(self):
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block)
        self.assertNotIn('Studio-All', page)
        self.assertIn('🕒 Timeline', page)
        self.assertNotIn('>Jobs<', page)
        self.assertIn('aria-label="Report"', page)
        self.assertNotIn('aria-label="Work"', page)

    def test_overview_report_reuses_map_and_registered_reports(self):
        self.face.write_text('# Study\nhome-section: overview-report\noverview-map: studio/map.mindmap.md\nspine: Compare.\n'
                             '## Questions\n```yaml\nquestions:\n- id: Q01\n  title: Compare\n  question: Which works?\n'
                             '  acceptance: Review both outputs.\n  report: reports/q01.md\n  work:\n'
                             '  - path: j01_first\n    role: First contribution\n  - path: j02_second\n```\n')
        (self.block / 'studio').mkdir()
        (self.block / 'studio/map.mindmap.md').write_text('# Existing map\n')
        (self.block / 'reports').mkdir()
        (self.block / 'reports/q01.md').write_text('# Compare\nstate: DRAFT\nanswer-status: open\n\n## Opening\nBoth outputs exist; the answer is still open.\n')
        for name in ['j01_first', 'j02_second']:
            (self.block / name).mkdir()
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'findings')   # Report opens on MindMap (JL 261031)
        self.assertIn('view=focus-map', page)
        self.assertIn('studio%2Fmap.mindmap.md', page)
        self.assertIn('>Report</span></h1>', page)
        self.assertNotIn('overview-report.html', page)
        report_page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'overview-report', 'reports')
        for phrase in ['Answer: open', 'Both outputs exist', 'Review both outputs.', 'First contribution', 'j02_second']:
            self.assertIn(phrase, report_page)
        self.assertNotIn('class="overview-map"', report_page)
        self.assertIn('focus-rail left', report_page)
        self.assertIn('focus-rail right', report_page)
        self.assertEqual(report_page, focus_page.render(frame.Theme(name='work'), self.root, self.block, 'reports'))

    def test_overview_map_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            other = Path(elsewhere) / 'private.mindmap.md'
            other.write_text('# Private\n')
            self.face.write_text('# Study\nhome-section: overview-report\noverview-map: ' + str(other) + '\n')
            page = focus_page.render(frame.Theme(name='work'), self.root, self.block)
            self.assertNotIn('view=focus-map', page)
            self.assertNotIn('private.mindmap.md', page)

    def test_round_two_job_and_task_show_what_came_back(self):
        """Round 2 (261106): a Task's Status shows its newest Run's output, the same in Report and Work, one Run state
        word; a Job's Status is numbered bars with each Task's headline on its row, and it has Findings; no machine
        path in a map; no icon request; a waiting form with no question cards still shows."""
        job = self.block / 'j01_tables'
        (job / 'j01_tables.md').parent.mkdir()
        (job / 'j01_tables.md').write_text('# j01_tables · Tables\n\ngoal: Make the tables.\n')
        task = self.write_task('j01_tables', 't01_cut', '✅ DONE')
        res = task / 'runs' / 'r01_cut' / 'result'
        res.mkdir(parents=True)
        (task / 'runs' / 'r01_cut' / 'run.yaml').write_text('run: r01_cut\nstatus: done\n')
        (res / 'runtime.yaml').write_text('status: complete\nheadline: "3 tables \\xB7 12 rows"\n')
        (res / 'values.csv').write_text('key,value\nn,12\n')
        wait = task / 'runs' / 'r02_collect_cut'
        wait.mkdir(parents=True)
        (wait / 'run.yaml').write_text('run: r02_collect_cut\nkind: hard\ntype: collect\nstatus: waiting\nview: status\n')
        (wait / 'question_collection.md').write_text('# Cut words\n\nfor: b01-s01:study @ cut\n')   # no ## QN cards
        (wait / 'r02_collect_cut.html').write_text('<!doctype html>')
        theme = frame.Theme(name='work')
        report = focus_page.render(theme, self.root, task, 'report', 'standing')
        work = focus_page.render(theme, self.root, task, 'work', 'standing')
        for page in (report, work):
            self.assertIn('3 tables · 12 rows', page)   # decoded, as YAML reads it
            self.assertIn('🗂️ Tables', focus_page.render(theme, self.root, task, 'report', 'findings'))                                     # its returned table, drawn
            self.assertIn('🙋 waiting for you', page)                    # one Run state word in both
            self.assertNotIn('not run', page)
            self.assertIn('<b>Cut words</b><span class="inbox-state waiting">waiting for you', page)  # a form with no cards is kept
            self.assertIn('<link rel="icon" href="data:,">', page)
        self.assertNotIn(str(self.root), focus_page.render(theme, self.root, task, 'report', 'mindmap'))
        status = focus_page.render(theme, self.root, job, 'report', 'standing')
        self.assertIn('<summary>1 · 🧱 Tasks<span class=word>1 of 1 done</span>', status)   # its Tasks first (JL 261108)
        self.assertIn('<span class=hl>3 tables · 12 rows</span>', status)          # each Task's headline on its row
        self.assertNotIn('🧩 Topics', status)              # each Topic is one of its Tasks: the rows above already
        findings = focus_page.render(theme, self.root, job, 'report', 'findings')
        self.assertIn('📌 Headlines<span class=word>1 of 1 returned</span>', findings)
        self.assertNotIn('· 📦 Delivery', findings)


    def test_round3_work_rows_carry_their_verbs_and_words(self):
        """Round 3 (261106): Agree or Write on each answer row, Answer on a Status row whose form waits, Open on a next
        step, words in place of ids, an empty lane says only that, and the Job's state line leads its Status."""
        self.findings_block()
        (self.block / 'reports/q01_a/q01_a.md').write_text('# A\n\n## Opening\n\nProposed: the tables hold.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work', 'findings')
        self.assertIn('class="row-verb pb-copy1"', page)
        self.assertIn('>Agree</button>', page)                                    # its answer waits for agreement
        self.assertIn('/haipipe-report b01_study/reports/q01_a/q01_a.md I agree', page)
        self.assertEqual(page.count('its answer waits for your agreement'), 1)    # once, under Process (round 3)
        self.assertIn('Nothing handed over yet.', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'delivery'))          # no "goes in delivery/model/"
        self.assertNotIn('All files', page)
        self.assertNotIn('<small>j01 · t01</small>', page)
        job = self.block / 'j01_work'
        (job / 'j01_work.md').write_text('# j01\nstate: ⏳ IN PROGRESS · the reading is running\n')
        run = job / 't01_read/runs/r01_collect_cut'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_collect_cut\nstatus: waiting\n')
        (run / 'question_collection.md').write_text('# Cut\n\n## Q1 · Cut\n\nWhy.\n\n**Which cut?**\n\n- [x] A · a\n- [ ] B · b\n')
        (run / 'r01_collect_cut.html').write_text('<html></html>')
        status = focus_page.render(frame.Theme(name='work'), self.root, job, 'report', 'standing')
        self.assertIn('<p class=st-lead>⏳ <b>In progress</b> · the reading is running</p>', status)
        self.assertIn('🙋 Interaction', status)                                    # on the Task's row
        self.assertNotIn('<span class=jn>t01</span>', status)
        self.assertEqual(focus_page.steps_word(['running']), '1 running')
        self.assertEqual(focus_page.steps_word(['running', 'planned']), '2 to do')
        self.assertEqual(focus_page.ladder_words('t03'), 'Task 3')

    def test_round3_run_popout_draws_its_files_and_links_what_it_reads(self):
        """Round 3: the pop-out's files are side tabs, a map is drawn, and the path a Run reads opens that Run."""
        task = self.write_task('j01_compare', 't01_first', '✅ DONE · ok')
        src = task / 'runs/r01_first/result'
        src.mkdir(parents=True)
        (src / 'tables.csv').write_text('a,b\n1,2\n')
        run = task / 'runs/r02_next'
        (run / 'result/maps').mkdir(parents=True)
        (run / 'result/maps/one.mindmap.md').write_text('---\nmindmap: 1\n---\n\n# One\n\n- A\n')
        (run / 'run.yaml').write_text('run: r02_next\nreads:\n- b01_study/j01_compare/t01_first/runs/r01_first/result/tables.csv\n')
        page = focus_page.run_document(run, self.root)
        self.assertIn('pb-side', page)                                             # side tabs, never top tabs
        self.assertNotIn('name="runtab"', page)
        self.assertIn('view=focus-map', page)                                      # the map drawn, not its Markdown
        self.assertIn('part=run&amp;path=b01_study%2Fj01_compare%2Ft01_first%2Fruns%2Fr01_first', page)   # reads: that Run
        self.assertNotIn(str(self.root), page)

    def test_run_page_names_its_ticket_and_pass_once_and_reads_a_report_as_a_page(self):
        """One Run page for every theme (261109): the ticket shows once, a pass is not named twice, a .md is drawn."""
        task = self.write_task('j01_compare', 't01_first', '✅ DONE · ok')
        run = task / 'runs/r01_collect_choice'
        (run / 'result').mkdir(parents=True)
        (run / 'passes/p01-1031').mkdir(parents=True)
        (run / 'r01_collect_choice.html').write_text('<p>form</p>')
        (run / 'run.yaml').write_text('run: r01_collect_choice\ntype: collect\nticket: r01_collect_choice.html\n')
        (run / 'result/answer_collection.md').write_text('# Answers\n\n**How much?** a_very_long_token_' + 'x' * 120 + '\n')
        (run / 'passes/p01-1031/pass.md').write_text('# p01-1031 · the answers came back\n')
        page = focus_page.run_document(run, self.root)
        self.assertEqual(page.count('r01_collect_choice.html</'), 1)            # the ticket fold, not also a row
        self.assertIn('<b>p01-1031</b> <span class="mut">the answers came back</span>', page)
        self.assertIn('class="run-md"', page)
        self.assertIn('<b>How much?</b>', page)
        self.assertIn('overflow-wrap:anywhere', page)

    def test_block_and_task_name_their_type_and_use_case_under_the_title(self):
        """261109: the line under a Block's or Task's title says its type and, when known, its use case."""
        task = self.write_task('j01_compare', 't01_first', '✅ DONE · ok')
        face = task / 't01_first.md'
        face.write_text(face.read_text() + '\ntask-type: fit\n')
        line = focus_page.page_identity_html('work', task, self.root, focus_page.read_face(task, self.root))
        self.assertIn('<dt>Task type</dt><dd>🧩 Task</dd>', line)
        self.assertIn('<dt>Use case</dt><dd>🧪 Model fitting</dd>', line)
        block = task.parent.parent
        line = focus_page.page_identity_html('work', block, self.root, focus_page.read_face(block, self.root))
        self.assertIn('<dt>Block type</dt><dd>🧩 Work Block</dd>', line)
        self.assertNotIn('Use case', line)                                      # none written, none guessed

    def test_run_names_its_type_and_use_case_under_the_title(self):
        task = self.write_task('j01_compare', 't01_first', '✅ DONE · ok')
        run = task / 'runs/r01_fit_main'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_fit_main\ntype: fit\n')
        page = focus_page.run_document(run, self.root)
        self.assertIn('<dt>Run type</dt><dd>🧪 Run</dd>', page)
        self.assertIn('<dt>Use case</dt><dd>🧪 Model fitting</dd>', page)
        (run / 'run.yaml').write_text('run: r01_fit_main\ntype: null\n')
        self.assertNotIn('Use case', focus_page.run_document(run, self.root))

    def test_run_page_shows_its_data_card_in_and_out(self):
        """261109: a Run's result/data-card.yaml shows what it read and wrote; result/ with only receipt and card says so."""
        task = self.write_task('j01_compare', 't01_first', '✅ DONE · ok')
        run = task / 'runs/r01_case_2015'
        (run / 'result').mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_case_2015\ntype: case\n')
        (run / 'result/runtime.yaml').write_text('status: completed\n')
        (run / 'result/data-card.yaml').write_text(
            'run: r01_case_2015\ninputs:\n- table: _WorkSpace/in-2015.dta\n  from: Stage A lines\n  columns: [bene_id, npi]\n'
            'outputs:\n- table: _WorkSpace/CASES-2015.dta\n  row: one patient x physician x day\n  key: [bene_id, npi_id, obs_dt]\n'
            '  rows: 1234\n  size: 1.5 GB\n  columns:\n  - {name: kind, type: byte, means: "1 office, 2 ED"}\n')
        page = focus_page.run_document(run, self.root)
        self.assertIn('2 · 🔄 Data in and out', page)
        self.assertIn('3 · 📊 What it made', page)
        self.assertIn('<code>_WorkSpace/in-2015.dta</code>', page)
        self.assertIn('<code>npi</code>', page)
        self.assertIn('one row = one patient x physician x day · key bene_id, npi_id, obs_dt · 1,234 rows · 1.5 GB', page)
        self.assertIn('<td><code>kind</code></td><td>byte</td><td>1 office, 2 ED</td>', page)
        self.assertNotIn('Nothing made yet', page)
        self.assertNotIn('data-card.yaml</b>', page)                                # not also a result tab
        title, word, body = focus_page.runs_section(task, self.root)
        self.assertIn('<details class="dc-fold"><summary>Data out</summary>', body)
        (run / 'result/data-card.yaml').unlink()
        page = focus_page.run_document(run, self.root)
        self.assertNotIn('Data in and out', page)
        self.assertIn('2 · 📊 What it made', page)

    def test_run_ui_is_a_view_of_a_theme_block(self):
        self.assertIn(('run', 'Run UI'), focus_page.UI_VIEWS)


    def test_round3_shared_words_and_the_draw_page(self):
        """Round 3: a to-do row's short id moves to hover; the Draw page registers no service worker (/sw.js 404)."""
        from live import excalidraw_proxy, ui_parts
        rows = ui_parts._todo([("G0: the telling is not chosen yet", "", "waiting for you", "", "", False)])
        self.assertIn('>the telling is not chosen yet<', rows)
        self.assertIn('title="G0: the telling is not chosen yet"', rows)
        self.assertEqual(ui_parts.todo_word([("T0 · the main Runs", "", "waiting for you")])[1], "🙋 the main Runs")
        self.assertEqual(ui_parts._no_id("G01: kept, a name the theme shows"), "G01: kept, a name the theme shows")
        self.assertIn(b"delete Navigator.prototype.serviceWorker", excalidraw_proxy.NO_SW)


if __name__ == '__main__':
    unittest.main()


def test_a_run_folder_opens_as_its_run_page(tmp_path):
    """JL 261108: a Run's link showed the Block page (MindMap, Status, Findings, nothing to map); it shows the Run."""
    run = tmp_path / "b01_x" / "j01_y" / "t01_z" / "runs" / "r01_z_2016"
    (run / "result").mkdir(parents=True)
    (run / "run.yaml").write_text("run: r01_z_2016\nstatus: complete\n")
    (run / "result" / "summary.txt").write_text("cases 42\n")
    html = focus_page.render(frame.Theme(name="work"), tmp_path, run)
    assert "cases 42" in html and "Nothing to map yet" not in html


def test_know_rail_keeps_current_page_scope(tmp_path):
    """JL 261108: what to know is a right-rail section of its own, apart from Interactions; a note kept on a page shows
    on every page below it."""
    block = tmp_path / "b01_study"
    job = block / "j01_work"
    job.mkdir(parents=True)
    (block / "board.md").write_text("# Study\nspine: Compare.\n")
    (job / "j01_work.md").write_text("# j01\nstate: PARTIAL\n")
    run = block / "runs" / "r01_collect_lesson"
    run.mkdir(parents=True)
    (run / "run.yaml").write_text("run: r01_collect_lesson\ntype: collect\nstatus: done\nsource: know\ntarget: b01-s01:x\n")
    (run / "question_collection.md").write_text("# Lessons: scoring\n\nfor: b01-s01:x\n")
    theme = frame.Theme(name="work")
    know = focus_page.render(theme, tmp_path, job, "know")
    assert "section=know" in know and "r01_collect_lesson" not in know
    assert "r01_collect_lesson" in focus_page.render(theme, tmp_path, block, "know")
    asked = focus_page.render(theme, tmp_path, job, "interactions")
    assert "r01_collect_lesson" not in asked
    plain = tmp_path / "b02_other"
    plain.mkdir()
    (plain / "board.md").write_text("# Other\nspine: Nothing to know.\n")
    assert "section=know" in focus_page.render(theme, tmp_path, plain, "work")
