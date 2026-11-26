"""Status and the map: registered reports, job rows, the Block map, the MindMap and the overview."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
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
        self.assertNotIn('The recorded answer.', home)              # Findings holds no question answers (JL 261109)
        self.assertNotIn('Detailed context only.', home)          # the face's prose is not in Report (JL 261030)
        self.assertNotIn('An expectation, not a finding.', home)
        reports = focus_page.render(theme, self.root, self.block, 'reports')
        self.assertNotIn('The recorded answer.', reports)          # the old reports link opens Findings, no answers (JL 261109)
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

    def test_report_status_lists_each_job_and_its_tasks(self):
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare two methods.\nnext: settle 3 scores\n')
        self.write_task('j01_compare', 't01_first', '🟡 RESULTS IN, UNREAD · r01 complete')
        self.write_task('j01_compare', 't02_second', '🟡 RESULTS IN, UNREAD · r01 complete')
        self.write_task('j01_compare', 't03_third', '🟠 WAITING FOR A PERSON · pick a cut')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'standing')   # Report opens on MindMap (JL 261031)
        self.assertIn('<details class=band-sec><summary><span class=bt>1 · ', page)   # a Block's Status: one closed section per band (JL 261104)
        self.assertIn('<details class=job-row>', page)     # a row per Job (JL 261104), its short name
        self.assertIn('<b>compare</b>', page)
        self.assertIn('data-pop="t03_third"', page)        # the row opens to its Tasks
        self.assertIn('<ul class=fold-tree>', page)        # Jobs and Tasks first (JL 261108); its one Topic is its one
        self.assertNotIn('🧩 View BJTR', page)             # no topic navigation in Plan + Results (JL 261109)
        self.assertNotIn('Next: settle 3 scores', page)    # no "Next:" lines (JL 261104: "just delete them")
        self.assertIn('<span class=jn>j01</span>', page)   # its jNN, then how far as a mark (JL 261113: no state words)
        self.assertNotIn('· 3 Tasks', page)                # no Task count on the row
        self.assertRegex(page, r'<small title="[a-z ]+">[✅🔶🏃🙋⬜]</small>')
        work = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work')   # Work opens on the same Status (JL 261104)
        self.assertIn('<ul class=fold-tree>', work)
        self.assertIn('data-pop="j01_compare" title="j01_compare: Compare two methods"><b>compare</b>', work)   # its folder and goal on hover
        self.assertIn('data-pop="t03_third"', work)
        self.assertIn('<span class="st fx-you" title="waiting for a person">', work)
        self.assertNotIn('🚧 Next steps', work)
        self.assertNotIn('🧩 View BJTR', work)

    def test_job_rows_show_each_task_and_its_rounds(self):
        """s07's Topic rows preview (JL 261125): a Job's Main band is 📊 Tasks; under 1 · 🧱 Tasks, no progress bar, a
        row per Task named tNN · its heading, its newest round's mark; opened, a row per round under it."""
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare two methods.\n')
        task = self.write_task('j01_compare', 't01_first', '🔶 DRAWN, REVIEW OPEN · r01 drawn', figure=True)
        run = task / 'runs' / 'r02_check'
        (run / 'passes' / 'p01-1124').mkdir(parents=True)
        (run / 'passes' / 'p02-1125').mkdir()
        (run / 'run.yaml').write_text('status: done\n')
        (run / 'passes' / 'p01-1124' / 'pass.md').write_text('# first check round\n\n## Summary\n\nTests pass. More.\n')
        (run / 'passes' / 'p02-1125' / 'pass.md').write_text('# live restarts\n\n## Summary\n\nNo traceback.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, job)
        self.assertIn('📊 Tasks</h2>', page)
        self.assertNotIn('<span class=bar>', fixtures.band(page, 'standing'))      # no progress bar on 1 · 🧱 Tasks
        self.assertRegex(page, r'<details class="job-row fx-done" data-path="[^"]*t01_first"><summary><b class=tn title="t01_first">t01 · t01_first</b>')
        rounds = page[page.index('<div class=task-rounds>'):]
        self.assertLess(rounds.index('live restarts'), rounds.index('first check round'))    # newest first
        self.assertRegex(page, r'<a class="task-rr round fx-done" data-path="[^"]*p02-1125" href="[^"]*pass\.md" data-pop="[^"]*" title="No traceback.">')    # its Summary's first sentence on hover
        self.assertIn('<small>round 2 · 11-25</small>', page)
        self.assertIn('<span>It differs little.</span><small>r01_first</small>', page)   # a Run with no passes
        self.assertNotIn('<div class=job-tree>', fixtures.band(page, 'standing'))    # no figure or headline in the row

    def test_new_tasks_and_runs_since_the_last_commit_fade_in(self):
        """JL 261126: "for the new runs, and new task, you can show it as well": a Task or Run git does not track yet is
        new (a plus, fading); a new Run leaves its Task's own mark."""
        import subprocess
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare.\n')
        old = self.write_task('j01_compare', 't01_first', '✅ done')
        (old / 'runs' / 'r01_check').mkdir(parents=True)
        (old / 'runs' / 'r01_check' / 'run.yaml').write_text('status: done\n')
        git = lambda *a: subprocess.run(['git', '-C', str(self.block), *a], capture_output=True, check=True)
        git('init', '-q')
        git('add', '.')
        git('-c', 'user.name=t', '-c', 'user.email=t@example.test', 'commit', '-qm', 'first')
        (old / 'runs' / 'r02_again').mkdir()
        (old / 'runs' / 'r02_again' / 'run.yaml').write_text('status: planned\n')
        self.write_task('j01_compare', 't02_second', '⬜ open')
        band = fixtures.band(focus_page.render(frame.Theme(name='work'), self.root, job), 'standing')
        self.assertRegex(band, r'<details class="job-row fx-done" data-path="[^"]*"><summary><b class=tn title="t01_first">')   # its own mark
        self.assertIn('<a class="task-rr run fx-new"', band)                                          # its new Run
        self.assertRegex(band, r'<details class="job-row fx-new" data-path="[^"]*"><summary><b class=tn title="t02_second">')

    def test_job_tasks_fold_by_their_group(self):
        """JL 261125: "each fold here should be ... the Task group name": one fold per tNN decade, named by the face's
        `bands:` line; a face with no `bands:` keeps one fold, Tasks."""
        job = self.block / 'j01_compare'
        job.mkdir()
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare.\nbands: t0N Page parts · t1N Shared tools\n')
        self.write_task('j01_compare', 't01_first', '🔶 OPEN')
        self.write_task('j01_compare', 't11_second', '🔶 OPEN')
        band = fixtures.band(focus_page.render(frame.Theme(name='work'), self.root, job), 'standing')
        self.assertIn('🧱 Page parts', band)
        self.assertIn('🧱 Shared tools', band)
        self.assertLess(band.index('Shared tools'), band.index('t11 · t11_second'))   # t11 under its own fold
        self.assertLess(band.index('t01 · t01_first'), band.index('Shared tools'))
        self.assertEqual(band.count('<details class=band-sec'), 2)
        (job / 'j01_compare.md').write_text('# Job\ngoal: Compare.\n')
        band = fixtures.band(focus_page.render(frame.Theme(name='work'), self.root, job), 'standing')
        self.assertEqual(band.count('<details class=band-sec'), 1)
        self.assertIn('🧱 Tasks', band)

    def test_block_with_answers_opens_on_findings(self):
        report_dir = self.block / 'reports' / 'q01_compare'
        report_dir.mkdir(parents=True)
        (report_dir / 'q01_compare.md').write_text('# Comparison\nstate: 🟡 DRAFT\n## Opening\nAn answer.\n')
        self.face.write_text('# Study\nspine: Compare the methods.\n## Questions\n```yaml\nquestions:\n'
                             '- id: Q01\n  title: Compare\n  report: reports/q01_compare/q01_compare.md\n'
                             '- id: Q02\n  title: Second\n```\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'findings')
        self.assertNotIn('An answer.', page)                            # no question answers in Findings (JL 261109)
        self.assertIn('Findings', page)

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
        with patch('live.focus_base.owned_register', return_value=([{'id': 'Q01', 'title': 'Short', 'question': 'Is it trained?'}], '')):
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
        self.assertLess(page.index('id="band-overview"'), page.index('class="focus-map fit-map"'))   # the first band
        self.assertIn('class="focus-map fit-map"', page)                         # it fits its box (round 3)
        self.assertIn('Delivers a deck and a rule', page)                         # one plain paragraph, as the draft map
        self.assertIn('<div class=pm-detail hidden><p', page)                    # every item starts closed (JL 261104)
        self.assertIn('class="pm pm-folds"', page)
        self.assertNotRegex(page, r'class="[^"]*pm-on')                         # nothing drawn open; no <details open> either
        self.assertNotRegex(page, r'<details[^>]*\bopen\b')
        self.assertNotIn('page-tree', page)                                      # no map column

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
        self.assertIn('>Report</button></h1>', page)
        self.assertNotIn('overview-report.html', page)
        report_page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'overview-report', 'reports')
        for phrase in ['Answer: open', 'Both outputs exist', 'Review both outputs.', 'First contribution', 'j02_second']:
            self.assertIn(phrase, report_page)
        self.assertNotIn('class="overview-map"', fixtures.band(report_page, 'reports'))
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


if __name__ == '__main__':
    unittest.main()
