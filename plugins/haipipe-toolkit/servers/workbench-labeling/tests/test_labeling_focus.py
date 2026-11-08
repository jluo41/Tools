"""The live focus layout preserves source content, read-only routing and writers."""
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
import io
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap
bootstrap()
from live import frame, labeling_focus as L
from test_labeling_theme import project, items_task
import tempfile


class LabelingFocusTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root, self.block, self.task = project(self.temp.name)
        self.items = items_task(self.task.parent)
        self.theme = frame.themes()['labeling']

    def tearDown(self):
        self.temp.cleanup()

    def test_items_task_has_the_shared_shape_on_real_preparation_content(self):
        """Round 2: the items Task's steps are its views, each ⚙️ Process then 📊 Results then 🙋 Interaction."""
        page = L.render(self.theme, self.root, self.items, 'items')
        self.assertIn('placeholder words here', page)
        self.assertIn('One item', page)
        self.assertIn('/_board/labeling/sample?', page)
        views = page.split('<nav class="section-views" aria-label="Views">', 1)[1].split('</nav>', 1)[0]
        self.assertEqual(re.findall(r'>(Data|Items|Embedding)<', views), ['Data', 'Items', 'Embedding'])
        order = [page.index(w) for w in ('⚙️ Process', '📊 Results', '🙋 Interaction')]
        self.assertEqual(order, sorted(order))
        rail = page.split('aria-label="Page sections">', 1)[1].split('</nav>', 1)[0]
        for name in ('Report', 'Work', 'Interactions', 'Delivery', 'Skills', 'Files'):
            self.assertIn(f'<span class="rail-name">{name}<', rail)
        report = L.render(self.theme, self.root, self.items, 'report', 'items')
        self.assertNotIn('⚙️ Process', report)
        self.assertIn('📊 Results', report)
        self.assertNotIn('<p class=pb-sess>', page)                          # no grey session line (round 2)

    def test_a_job_has_the_shared_shape_with_its_tasks_in_the_left_rail(self):
        page = L.render(self.theme, self.root, self.task.parent)
        left = page.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        self.assertIn(self.items.name, left)
        self.assertIn(self.task.name, left)
        views = page.split('<nav class="section-views" aria-label="Views">', 1)[1].split('</nav>', 1)[0]
        self.assertEqual(re.findall(r'>(MindMap|Status|Findings)<', views), ['MindMap', 'Status', 'Findings'])
        for section in ('report', 'work'):
            for view in ('mindmap', 'standing', 'findings'):
                with self.subTest(section=section, view=view):
                    html = L.render(self.theme, self.root, self.task.parent, section, view)
                    self.assertEqual(re.findall(r'<h3 class=fd-h>(?:\d+ · )?([^<]*)', html)[-1], '🙋 Interaction')
                    self.assertEqual('⚙️ Process' in html or '📊 Results' in html, section == 'work')

    def test_left_menu_contains_only_same_level_pages(self):
        other = self.block / 'j02_other'
        other.mkdir()
        page = L.render(self.theme, self.root, self.task.parent)
        rail = page.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        self.assertIn('j02_other', rail)
        page = L.render(self.theme, self.root, self.items)
        rail = page.split('class="focus-rail left"', 1)[1].split('</nav>', 1)[0]
        self.assertIn(self.task.name, rail)
        self.assertIn(self.items.name, rail)
        self.assertNotIn('j02_other', rail)

    def test_next_step_does_not_settle_or_run(self):
        with patch.object(L.TL.IT, 'next_step', return_value={
            'step':'items','do':'Review the recipe','note':''}) as read:
            result = L.next_action(self.task.parent, self.root)
            read.assert_called_once_with(self.items, settle_runs=False)
        self.assertEqual(result[:3], (self.items, 'items', 'Review the recipe'))

    def test_a_two_loop_job_points_to_its_next_run_its_form_then_its_score(self):
        """b15 261101 (DICES use case 2): a Job with a meaning Task is led by its own Runs, not by item making."""
        from test_labeling_theme import task
        job = self.task.parent
        meaning = task(job, "t05_demo_meaning", "labeling-meaning")
        score = task(job, "t06_demo_score", "eval")
        def run(t, name, status):
            folder = t / "runs" / name
            folder.mkdir(parents=True)
            (folder / "run.yaml").write_text(f"run: {name}\nstatus: {status}\n")
            return folder
        draw = run(meaning, "r02_draw_report_m01", "planned")
        run(score, "r01_score_loop1", "planned")
        self.assertEqual(L.next_action(job, self.root)[:2], (meaning, "runs"))
        self.assertIn("r02_draw_report_m01", L.next_action(job, self.root)[2])
        (draw / "result").mkdir()
        (draw / "result" / "runtime.yaml").write_text("status: complete\n")
        self.assertIn("Report prompt", L.next_action(job, self.root)[2])
        form = run(meaning, "r04_collect_report_m01", "waiting")
        self.assertIn("Answer r04_collect_report_m01", L.next_action(job, self.root)[2])
        (form / "run.yaml").write_text("run: r04_collect_report_m01\nstatus: done\n")
        self.assertEqual(L.next_action(job, self.root)[0], score)

    def test_an_older_job_link_opens_the_nearest_view(self):
        for old, (section, view) in (('goal', ('Report', 'MindMap')), ('tasks', ('Work', 'Status')),
                                     ('reports', ('Report', 'Findings'))):
            with self.subTest(old=old):
                page = L.render(self.theme, self.root, self.task.parent, old)
                self.assertIn(f'">{section}</span></h1>', page)
                self.assertIn(f'aria-current="page">{view}</a>', page)

    def test_reports_remain_in_the_owning_run_and_do_not_write(self):
        path = self.items / 'runs/r01_demo/result/REPORT.md'
        path.write_text('# Prepared corpus\nThe real saved report.\n')
        sealed = self.items / 'labeling/test/sealed'
        sealed.mkdir(parents=True)
        (sealed/'REPORT.md').write_text('PROTECTED_SENTINEL')
        before = {str(p):p.stat().st_mtime_ns for p in self.root.rglob('*') if p.is_file()}
        page = L.render(self.theme, self.root, self.items, 'reports')
        self.assertIn('📊 Results', page)
        self.assertNotIn('PROTECTED_SENTINEL', page)
        self.assertEqual(before, {str(p):p.stat().st_mtime_ns for p in self.root.rglob('*') if p.is_file()})

    def test_engine_embed_keeps_existing_identity_and_route(self):
        page = L.render(self.theme, self.root, self.task, 'definition')
        self.assertIn('/_board/labeling?path=', page)
        self.assertIn('view=definition', page)
        self.assertIn('focus=1', page)
        self.assertNotIn('Sample report layout', page)

    def test_types_own_different_sections(self):
        self.assertIn(('items','Items'), L.roster(self.items,self.root))
        self.assertNotIn(('definition','Definition'),L.roster(self.items,self.root))
        self.assertIn(('definition','Definition'),L.roster(self.task,self.root))

    def test_flatten_preserves_actions_and_scripts(self):
        source = '<details><summary>Recipe</summary><button data-post="/writer">Sign</button></details><script>const example="<details>";</script>'
        result = L.flat_content(source)
        self.assertIn('data-post="/writer"',result)
        self.assertIn('const example="<details>";',result)
        self.assertNotIn('<summary>',result)

    def test_outside_root_rejected(self):
        with self.assertRaises(ValueError):
            L.render(self.theme,self.root,self.root.parent)

    def handler(self):
        from live.labeling import LabelingMixin
        class Handler(LabelingMixin):
            def send_response(self, status): self.status = status
            def send_header(self, *args): pass
            def end_headers(self): pass
            def reply(self, status, body): self.status, self.body = status, body
        h = Handler()
        h.root, h.headers, h.wfile = self.root, {'Host':'example.test'}, io.BytesIO()
        return h

    def test_sample_endpoint_uses_task_presenter(self):
        h = self.handler()
        h.path = '/_board/labeling/sample?' + urlencode({'task':str(self.items.relative_to(self.root)), 'kind':'items'})
        h.labeling_sample_view()
        self.assertEqual(h.status,200)
        self.assertIn(b'placeholder words here',h.wfile.getvalue())

    def test_sign_endpoint_uses_current_engine_and_preserves_origin_guard(self):
        h = self.handler()
        payload = {'action':'sign','task':str(self.items.relative_to(self.root)), 'run':'r01_demo','by':'Reviewer'}
        with patch.object(L.TL.IT,'sign',return_value={'by':'Reviewer'}) as sign:
            status, body = h.labeling_items_act(payload)
            self.assertEqual(status,200)
            sign.assert_called_once_with(self.items.resolve(),'r01_demo','Reviewer')
            h.headers['Origin']='https://other.test'
            status, body = h.labeling_items_act(payload)
            self.assertEqual(status,403)
            self.assertEqual(sign.call_count,1)

    def test_item_target_refuses_paths_outside_workspace(self):
        h=self.handler()
        self.assertIsNone(h._items_task_target('../outside')[0])
        self.assertIsNone(h._items_task_target(str(self.task.relative_to(self.root)))[0])


if __name__ == '__main__':
    unittest.main()
