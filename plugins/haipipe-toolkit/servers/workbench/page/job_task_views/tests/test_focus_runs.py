"""Runs and routes: a Run's page and pop-out, round two and three work rows, the focus route, the know rail."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
from host_paths import bootstrap

bootstrap()

from live import focus_page, frame  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402

sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class FocusPageTest(fixtures.FocusPageCase):
    def test_a_finished_run_reads_done_with_its_headline(self):
        """261105: a receipt saying `completed` read ⬜; every mark has its word, and headline.txt is read."""
        run = self.block / 'j01_x' / 't01_y' / 'runs' / 'r01_z'
        (run / 'result').mkdir(parents=True)
        (run / 'result' / 'runtime.yaml').write_text('run: r01_z\nstatus: completed\n')
        (run / 'result' / 'headline.txt').write_text('9 values\n')
        ((_, mark, head),) = focus_page.run_rows(run.parent.parent)
        self.assertEqual((mark, head), ('✅ done', '9 values'))

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
            self.assertIn('class="focus-page"', page)
            handler.path = '/_board/workbench?path=b01_study'            # a bare address is the focus page
            self.assertIn('class="focus-page"', handler.workbench_frame_view()[0])
            handler.path = '/_board/workbench?path=b01_study&layout=frame'   # the old frame only when asked for
            self.assertEqual(handler.workbench_frame_view(), ('legacy', 200))
            handler.path = '/_board/workbench?path=../outside&layout=focus'
            self.assertEqual(handler.workbench_frame_view()[1], 404)

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
            found = focus_page.render(theme, self.root, task, 'report', 'findings')
            self.assertIn('No findings here.', found)            # JL 261114: no tables.json, no display: nothing drawn
            self.assertNotIn('🔢 Values', found)
            self.assertIn('~ask">🙋 1<', page)       # a waiting Run shows its 🙋 card mark, no words (JL 261116)
            self.assertNotIn('🙋 waiting for you', page)
            self.assertNotIn('not run', page)
            self.assertIn('<b>Cut words</b><span class="inbox-state waiting">waiting for you', page)  # a form with no cards is kept
            self.assertIn('<link rel="icon" href="data:,">', page)
        self.assertNotIn(str(self.root), focus_page.render(theme, self.root, task, 'report', 'mindmap'))
        status = focus_page.render(theme, self.root, job, 'report', 'standing')
        self.assertIn('<summary><span class=bt>1 · 🧱 Tasks<i class="live-dot you" title="waits for you inside"></i></span>'
                      '<span class="word ok mk" aria-label="done">✓</span>', status)   # a waiting Run inside: the amber dot   # its Tasks first (JL 261108)
        self.assertIn('<span>3 tables · 12 rows</span>', status)          # each Task's newest Run as its round row
        self.assertNotIn('🧩 Topics', status)              # each Topic is one of its Tasks: the rows above already
        findings = focus_page.render(theme, self.root, job, 'report', 'findings')
        self.assertNotIn('📌 Headlines', findings)           # a Job's Findings is Values and Displays (JL 261111)
        self.assertNotIn('🖼️ Displays', findings)           # JL 261114: no display Task, no section
        self.assertNotIn('· 📦 Delivery', findings)

    def test_round3_work_rows_carry_their_verbs_and_words(self):
        """Round 3 (261106): Agree or Write on each answer row, Answer on a Status row whose form waits, Open on a next
        step, words in place of ids, an empty lane says only that, and the Job's state line leads its Status."""
        self.findings_block()
        (self.block / 'reports/q01_a/q01_a.md').write_text('# A\n\n## Opening\n\nProposed: the tables hold.\n')
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, 'work', 'findings')
        self.assertNotIn('>Agree</button>', page)                                 # no answer rows in Findings (JL 261109)
        self.assertNotIn('Nothing handed over yet', focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'delivery'))          # no "goes in delivery/model/"
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
        self.assertNotIn('<p class=st-lead>', status)           # JL 261113: no state sentence; the Tasks' marks show it
        self.assertIn('🙋 Interaction', status)                                    # on the Task's row
        self.assertNotIn('<span class=jn>t01</span>', status)
        self.assertEqual(focus_page.steps_word(['running']), 'running')
        self.assertEqual(focus_page.steps_word(['running', 'planned']), 'to do')
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
