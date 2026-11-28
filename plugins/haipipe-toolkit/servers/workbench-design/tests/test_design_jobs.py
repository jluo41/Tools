"""Real Design records in the shared selector; no release or record writes during rendering."""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '_host'))
from host_paths import bootstrap
bootstrap()
from live import design_jobs as D, focus_jobs as F, design_theme, work_theme

ROOT = Path(__file__).resolve().parents[5]
BOARD = ROOT / 'examples/Project-Ladder/design/Design-Example'
BOOK = ROOT / 'examples/Project-Ladder/design/DesignMethodBook-Example'
JOB = BOARD / 'j03_confirm-by-reply_M02-overall-performance-m1_inputs-v2'


class DesignJobsTest(unittest.TestCase):
    def test_board_groups_by_method_family_and_names_pins(self):
        bar, body = F.section(design_theme.THEME, ROOT, BOARD, 'j03')
        fam = lambda f: 'data-topic-to="family-' + hashlib.sha256(f.encode()).hexdigest()[:12] + '"'
        self.assertIn(fam('Goal Only'), bar)             # j01, j02 pin M01
        self.assertIn(fam('Internal'), bar)              # j03 pins M02
        self.assertNotIn('data-topic-to="G01"', bar)
        self.assertIn('j03 · G01 · M02 m1 · inputs-v2', bar)
        self.assertNotIn('could not be drawn', body)
        self.assertIn('data-ttopic-to="ideas"', body)
        self.assertIn('data-ttopic-to="designs"', body)
        self.assertIn('data-ttopic-to="review"', body)
        self.assertIn('aria-label="Tasks" hidden', body)

    def test_main_has_task_links_kept_designs_and_human_gate(self):
        html = D.main(JOB, ROOT)
        for text in ['Brief', 'Tasks', 'Kept designs', 'Ranking', 'Review and approve', 'Workflow', 'Runs']:
            self.assertIn(text, html)
        self.assertIn('data-jsub-to="t01" data-topic="designs"', html)
        self.assertIn('name=attest', html)
        self.assertIn('data-post="/_board/design-ladder-act"', html)
        self.assertIn('Approve the release', html)

    def test_each_task_exposes_all_role_steps_and_original_runs(self):
        for task in sorted(JOB.glob('t[0-9][0-9]*')):
            html = D.task_body(task, ROOT)
            kind = D.task_topic(task)
            labels = {'ideas': ['Inputs', 'Chains', 'Ideas', 'Fence check'],
                      'designs': ['Draft', 'Verify', 'Revise', 'State'],
                      'review': ['Rank', 'Coverage', 'Kept']}[kind]
            for label in labels:
                self.assertIn(f'<b>{label}</b>', html)
            for run in (task / 'runs').iterdir():
                if run.is_dir():
                    self.assertIn(run.name, html)
            self.assertNotIn('Approve the release', html)

    def test_method_job_has_versions_and_consuming_jobs_without_tasks(self):
        method = BOOK / 'j02_M02-overall-performance'
        html = F.job_pane(design_theme.THEME, ROOT, method)
        for text in ['Steps', 'Versions', 'Used by', 'm1', JOB.name]:
            self.assertIn(text, html)
        self.assertNotIn('Nothing to map yet', html)
        self.assertNotIn('aria-label="Tasks"', html)
        self.assertNotIn('Approve the release', html)
        self.assertEqual(D.topic(method)[1], 'Internal')            # M02's registry family

    def test_nested_tabs_have_distinct_outer_addresses(self):
        a = D.task_body(JOB / 't01_d01_reply-first-short', ROOT)
        b = D.task_body(JOB / 't02_d02_reminder-one-ask', ROOT)
        ids = lambda h: set(re.findall(r'data-pbtab="([^"]+-steps-\d+)"', h))
        self.assertEqual(len(ids(a)), 4)
        self.assertFalse(ids(a) & ids(b))
        self.assertLess(len(a), 80000)  # shared CSS/scripts are not copied into every step

    def test_unsigned_method_still_has_its_identity_and_source(self):
        method = BOOK / 'j02_M02-overall-performance'
        book = D.R.method_book(BOOK, ROOT)
        kind = next(m for m in book['types'] if m['path'] == method)
        with patch.object(D.R, 'method_book', return_value={**book, 'types': [{**kind, 'releases': []}], 'proposals': []}):
            html = D.method_main(method, ROOT)
        self.assertIn('M02 · overall performance', html)
        self.assertIn('Open ' + method.name, html)
        self.assertNotIn('Nothing to map yet', html)

    def test_other_themes_keep_the_shared_fallback(self):
        self.assertIsNone(F.design_adapter(work_theme.THEME, BOARD))
        self.assertIsNone(F.design_adapter(design_theme.THEME, ROOT / 'examples/Project-Ladder/blueprint/b12_theme_design'))

    def test_render_does_not_mutate_example_records(self):
        files = [p for base in (BOARD, BOOK) for p in base.rglob('*') if p.is_file()]
        digest = lambda: {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        before = digest()
        for block in (BOARD, BOOK):
            F.section(design_theme.THEME, ROOT, block)
        self.assertEqual(before, digest())

    def test_live_studio_previews_point_to_actual_examples(self):
        from urllib.parse import parse_qs, urlparse
        import html
        base = ROOT / 'examples/Project-Ladder/blueprint/b12_theme_design'
        for topic in ['s11-design-job-preview', 's12-methodbook-job-preview']:
            text = (base / topic / f'{topic}.html').read_text()
            urls = re.findall(r'data-src="([^"]+)"', text)
            self.assertTrue(urls)
            self.assertEqual(len(urls), len(set(urls)))
            for url in urls:
                q = parse_qs(urlparse(html.unescape(url)).query)
                self.assertEqual(q['section'], ['jobs'])
                self.assertTrue((ROOT / q['path'][0]).is_dir())

    def test_method_matrix_does_not_offer_generic_fallback_as_main(self):
        base = ROOT / 'examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec'
        guide = json.loads((base / 'view-guide.json').read_text())
        for view in ('', 'Main'):
            self.assertFalse(guide['type_view_routes']['job']['Design method'][view]['example'])


if __name__ == '__main__':
    unittest.main()
