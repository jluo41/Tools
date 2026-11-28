"""A Block's 💼 Jobs section: the place to work, one view per own jNN, each Job's Main on the Block page."""
import unittest

import sys
from pathlib import Path
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class JobsSectionTest(fixtures.FocusPageCase):
    def test_a_block_lists_its_jobs_as_views_and_draws_each_in_place(self):
        # JL 261125: "so the Job will be place to work, and in the Report, we also have Jobs, but that is for reporting"
        for name in ('j02_second', 'j01_first'):
            (self.block / name).mkdir()
            (self.block / name / f'{name}.md').write_text(f'# {name}\n\n**Goal:** do {name}\n')   # one decade: number order
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs')
        self.assertIn('data-side-key="jobs"', page)                     # in the sections menu
        self.assertLess(page.index('data-job-to="j01"'), page.index('data-job-to="j02"'))   # number order
        self.assertIn('>j01 · First</a>', page)
        self.assertIn('data-job-pane="j01">', page)                     # the first shown, the second built and hidden
        self.assertIn('data-job-pane="j02" hidden', page)
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs', 'j02')
        self.assertIn('data-job-pane="j02">', page)                     # an old link to one Job opens it

    def test_an_insight_board_groups_jobs_by_question_version_and_tasks_by_level(self):
        # b11 s07 (261126): a Job is a question version on a data version; a Task is one question at one DIKW level
        for name, data, state in (('j01_question-v1-ex_data-v1', 'data-v1', 'closed'), ('j02_question-v1-ex_data-v2', 'data-v2', 'open')):
            (self.block / name).mkdir()
            (self.block / name / f'{name}.md').write_text(f'---\nrelease: question-v1\ndata: {data}\nstate: {state}\ngoal: g\n---\n# {name}\n')
        job = self.block / 'j02_question-v1-ex_data-v2'
        for name in ('t03_I01_outcome-by-arm', 't01_D01_extract-shape', 't05_K01_gap'):
            (job / name).mkdir()
            (job / name / f'{name}.md').write_text(f'# {name}\n')
        page = focus_page.render(frame.Theme(name='insight'), self.root, self.block, 'jobs')
        self.assertIn('data-topic-to="question-v1"', page)                # row 1: the question version
        self.assertIn('>j02 · data-v2</a>', page)                         # row 2: a Job by its data version
        self.assertLess(page.index('data-job-to="j02"'), page.index('data-job-to="j01"'))   # newest first
        self.assertIn('data-job-to="j01" data-topic="question-v1" title="g" class="old"', page)   # a closed Job reads faded
        pane = page.split('data-job-pane="j02"', 1)[1]
        self.assertLess(pane.index('data-ttopic-to="D"'), pane.index('data-ttopic-to="I"'))  # row 3: levels in ladder order
        self.assertLess(pane.index('data-ttopic-to="I"'), pane.index('data-ttopic-to="K"'))
        self.assertIn('📈 Information', pane)
        self.assertIn('data-jsub-to="t03" data-topic="I"', pane)          # row 4: a question under its level
        main = pane.split('data-jsub="main"', 1)[1].split('data-jsub="t', 1)[0]
        for band in ('🧭 Overview', '📊 Tasks'):                         # its Main: the same bands as a work Job's
            self.assertIn(band, main)                                      # (b11 s11, JL 261126: "follow the same structure")

    def test_a_job_has_main_then_one_view_per_task(self):
        # s07, JL 261125: "should we call it the main?"; "how about we get the tasks to be the view as well"
        job = self.block / 'j01_first'
        job.mkdir()
        (job / 'j01_first.md').write_text('# j01 · First\ngoal: build the first thing\n')
        for name in ('t02_second', 't01_first'):
            (job / name).mkdir()
            (job / name / f'{name}.md').write_text(f'# {name}\nstate: 🔴 OPEN\ngoal: do {name}\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs')
        pane = page.split('data-job-pane="j01"', 1)[1]
        self.assertIn('data-jsub-to="main" aria-current="page">Main</a>', pane)          # Main first
        self.assertLess(pane.index('data-jsub-to="t01" data-topic="0">t01 · First</a>'), pane.index('data-jsub-to="t02" data-topic="0">t02 · Second</a>'))
        self.assertNotIn('🔴', pane.split('</nav>', 2)[1])                # an open Task shows no mark, never the 🔴
        self.assertIn('data-jsub="t01" hidden', pane)                     # each Task's page built, shown on its click
        self.assertIn('title="build the first thing"', page)             # the goal is its Job button's hover
        self.assertIn('class=open-dot', pane)                            # a Task opens from its dot

    def test_job_buttons_read_newest_decade_first_and_earlier_ones_faded(self):
        # s07 drawing, JL 261125: "How could we make this to be better?" (buttons wrapping onto three lines)
        for name in ('j01_old', 'j02_gone', 'j11_new'):
            (self.block / name).mkdir()
        (self.block / 'j01_old' / 'j01_old.md').write_text('# j01 · Old\n')
        (self.block / 'j02_gone' / 'j02_gone.md').write_text('# j02 · Gone\nstate: ✅ closed, superseded by j11\n')
        (self.block / 'j11_new' / 'j11_new.md').write_text('# j11 · New\n')
        bar = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs').split('aria-label="Jobs"', 1)[1]
        bar = bar.split('</nav>', 1)[0]
        self.assertLess(bar.index('data-job-to="j11"'), bar.index('data-job-to="j01"'))   # the newest decade first
        self.assertIn('data-job-to="j01" data-topic="0" title="j01_old" hidden', bar)      # another topic's Jobs wait hidden
        self.assertLess(bar.index('data-job-to="j01"'), bar.index('data-job-to="j02"'))   # a closed Job last
        self.assertIn('data-job-to="j11" data-topic="1" title="j11_new" aria-current="page"', bar)   # the newest opens first

    def test_four_rows_job_topic_job_view_task_topic_task_view(self):
        # s07, JL 261125: "rows 1: Job topic, rows 2: job view, rows 3: task topic, rows 4: task view"
        for name in ('j01_old', 'j11_new', 'j12_more'):
            (self.block / name).mkdir()
            (self.block / name / f'{name}.md').write_text(f'# {name}\n')
        (self.block / 'board.md').write_text((self.block / 'board.md').read_text() + '\nbands: j0N Earlier · j1N Workbench\n')
        for name in ('t01_a', 't02_b', 't11_check'):
            (self.block / 'j11_new' / name).mkdir()
            (self.block / 'j11_new' / name / f'{name}.md').write_text(f'# {name}\n')
        (self.block / 'j11_new' / 'j11_new.md').write_text('# j11_new\nbands: t0N Build · t1N Check\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs')
        row1 = page.split('aria-label="Job topics">', 1)[1].split('</nav>', 1)[0]       # row 1: Job topics, always
        self.assertLess(row1.index('Workbench <span class="topic-code">· j1N</span>'), row1.index('Earlier <span class="topic-code">· j0N</span>'))
        self.assertIn('data-topic-to="0" class="old"', row1)                               # an earlier decade faded
        self.assertNotIn('row-switch', page)                                                # no switch: always four rows (18:17)
        self.assertIn('class="section-views jrow job-bar"', page)                          # row 2: one line, scrolls sideways
        pane = page.split('data-job-pane="j11"', 1)[1]
        row3 = pane.split('aria-label="Task topics">', 1)[1].split('</nav>', 1)[0]      # row 3: Main, then Task topics
        self.assertIn('<a href="#" data-jsub-to="main" aria-current="page">Main</a>', row3)
        self.assertNotIn('class="old"', row3)                                             # Task decades are steps, never faded
        self.assertIn('data-ttopic-to="0">Build <span class="topic-code">· t0N</span>', row3)
        self.assertIn('data-ttopic-to="1">Check', row3)
        self.assertIn('aria-label="Tasks" hidden>', pane)                                 # row 4 waits for a Task topic
        self.assertIn('<a href="#" data-jsub-to="t11" data-topic="1">', pane)             # row 4: a Task in its topic
        one = page.split('data-job-pane="j12"', 1)[1]
        self.assertNotIn('aria-label="Task topics"', one.split('data-job-pane', 1)[0])    # a Job with no Task has no rows 3, 4

    def test_a_job_type_row_sits_above_the_groups_when_jobs_name_a_type(self):
        # b17 trace 261127/1310: a Job's type (job-type:) is apart from its group (board.md bands:)
        (self.block / 'board.md').write_text('# b\nbands: j0N First version · j1N Second version\n')
        for name, kind in (('j01_cli', 'code'), ('j02_docs', 'doc'), ('j11_checks', 'check'), ('j12_speed', 'code')):
            (self.block / name).mkdir()
            (self.block / name / f'{name}.md').write_text(f'# {name}\njob-type: {kind}\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs')
        self.assertIn('aria-label="Job types"', page)
        self.assertLess(page.index('aria-label="Job types"'), page.index('aria-label="Job topics"'))   # above the groups
        self.assertIn('data-type-to="" aria-current="page">All</a>', page)
        for kind in ('code', 'doc', 'check'):
            self.assertIn(f'data-type-to="{kind}">{kind}</a>', page)
        self.assertIn('data-job-to="j02"', page)
        self.assertRegex(page, r'data-job-to="j02"[^>]*data-jtype="doc"')
        self.assertRegex(page, r'data-topic-to="1" data-types="check code"')   # a group knows its Jobs' types

    def test_no_job_type_row_when_no_job_names_one(self):
        for name in ('j01_first', 'j02_second'):
            (self.block / name).mkdir()
            (self.block / name / f'{name}.md').write_text(f'# {name}\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'jobs')
        self.assertNotIn('aria-label="Job types"', page)

    def test_a_block_with_no_jobs_has_no_jobs_section(self):
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report')
        self.assertNotIn('data-side-key="jobs"', page)


if __name__ == '__main__':
    unittest.main()
