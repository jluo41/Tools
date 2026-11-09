"""Common Block frame, real example routing, and isolation of supporting records."""
import html
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '_host'))
from host_paths import bootstrap
bootstrap()
from live import design_context as c, design_focus as d, focus_page as f, frame, skills_section, use_case_examples
from live.design_theme import THEME
from live.work_theme import THEME as WORK_THEME

REPO = Path(__file__).resolve().parents[5]


class DesignContextTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.board = self.root / 'design/Design-Example'
        self.board.mkdir(parents=True)
        (self.board / 'board.md').write_text('# Example\nboard-kind: design-board\nchannel: sms\n')
        self.job = self.board / 'j01_example_goal-only'
        self.job.mkdir()
        (self.job / (self.job.name + '.md')).write_text('---\ngoal: G01\nmethod: M01 m2\ninputs: i1\n---\n# Example Job\n')
        self.topics = []
        for name, tag, marker in [('s01-goals', 'Goals', 'GOALS'), ('s02-methods', 'Methods', 'METHODS'),
                                  ('s03-unassigned', '', 'UNASSIGNED')]:
            topic = self.board / name
            topic.mkdir()
            (topic / (name + '.md')).write_text(f'# {name}\n**Tags:** {tag}\n\n## Decisions\n'
                f'{name}-D01 · {marker}_DECISION 2026-11-02\n## Checklist\n- [ ] {marker}_CHECK\n'
                f'## Things to Know\n{marker}_NOTE\n')
            self.topics.append((topic, [], {'tags': [tag] if tag else []}))
        self.rows = []
        for name, topic, view in [('goals', self.topics[0][0], ''), ('override', self.topics[0][0], 'methods'),
                                  ('unassigned', None, '')]:
            run = self.job / 'runs' / ('r01_' + name)
            (run / 'result').mkdir(parents=True)
            (run / 'run.yaml').write_text(f'run: r01_{name}\nskill: skill_{name}\n')
            (run / 'result/runtime.yaml').write_text('started_at: 2026-11-03T10:00:00\n')
            (run / 'question_collection.md').write_text(name)
            self.rows.append(dict(path=run, page=self.job, topic=topic, view=view, title=name+'_QUESTION',
                state='waiting', form=None, asks=[], answers=None, received='', applied={}, about='', feeds=[]))

    def test_scope_precedence_and_unassigned_records(self):
        self.assertTrue(c.applies(self.board))
        self.assertFalse(c.applies(self.job))
        selected = c.scope(self.board, self.root, 'goals', self.topics, self.rows, [])
        self.assertEqual(selected['interactions'], self.rows[:1])
        self.assertEqual(selected['runs'], [self.rows[0]['path']])
        self.assertEqual(c.scope(self.board, self.root, 'methods', self.topics, self.rows, [])['interactions'], self.rows[1:2])
        self.assertEqual(c.scope(self.board, self.root, 'jobs', self.topics, self.rows, [])['interactions'], [])
        self.assertEqual(c.scope(self.board, self.root, None, self.topics, self.rows, [])['interactions'], self.rows)

    def test_all_shared_sections_use_the_same_selection(self):
        catalog = {}
        for name in ('haipipe-design-goal', 'skill_goals', 'skill_override', 'skill_unassigned'):
            md = self.root / 'skills' / name / 'SKILL.md'
            md.parent.mkdir(parents=True)
            md.write_text(name)
            catalog[name] = ('Description', '1', md)
        with patch.object(skills_section, 'catalog', return_value=catalog):
            bodies = c.shared_bodies(self.board, self.root, 'design', 'Block', 'goals', self.topics, [], [], [], self.rows)
            for key, marker in [('studio', 's01-goals'), ('interactions', 'goals_QUESTION'),
                                ('decisions', 'GOALS_DECISION'), ('checklist', 'GOALS_CHECK'), ('know', 'GOALS_NOTE'),
                                ('timeline', 'r01_goals'), ('skills', 'skill_goals'), ('files', 'r01_goals')]:
                self.assertIn(marker, bodies[key][0], key)
            combined = ''.join(body for body, _ in bodies.values())
            for marker in ('METHODS_DECISION', 'UNASSIGNED_DECISION', 'override_QUESTION', 'unassigned_QUESTION', '/skill_override'):
                self.assertNotIn(marker, combined)
            rail = c.shared_bodies(self.board, self.root, 'design', 'Block', None, self.topics, [], [], [], self.rows)
            self.assertIn('UNASSIGNED_DECISION', rail['decisions'][0])
            self.assertIn('unassigned_QUESTION', rail['interactions'][0])
            self.assertIn('skill_unassigned', rail['skills'][0])

    def test_merged_block_has_actions_and_legacy_links_keep_selected_view(self):
        for key, _ in d.BLOCK_VIEWS:
            page = f.render(THEME, self.root, self.board, 'work', 'work-'+key)
            self.assertIn(f'aria-current="page">{dict(d.BLOCK_VIEWS)[key]}</a>', page)
            self.assertIn('📋 Review Content', page)
            self.assertIn('🧭 Around the Work', page)
            self.assertNotIn('aria-label="Work"', page)
            self.assertNotIn('<h3 class=pb-group>⚙️ Process', page)
            groups = re.findall(r'<h3 class=fd-h>(\d+) · ', page)
            self.assertEqual([int(n) for n in groups], list(range(1,len(groups)+1)))
        self.assertIn('pb-copy', f.render(THEME, self.root, self.board, 'report', 'goals'))
        self.assertIn('Review and approve', f.render(THEME, self.root, self.job, 'work', 'work-release'))
        self.assertIn('aria-label="Work"', f.render(THEME, self.root, self.job, 'work', 'work-release'))

    def test_blueprint_sections_and_examples_are_real_and_routed(self):
        blueprint = REPO / 'blueprints/Project-Ladder/work/b12_theme_design'
        guide = json.loads((blueprint / 'ui/view-guide.json').read_text())
        matrix = f.ui_matrix_html(blueprint / 'ui/block-views.md', REPO)
        for key in ('summary', 'goals', 'jobs', 'rounds', 'methods', 'mindmap'):
            self.assertIn('group='+key, html.unescape(matrix))
        matrices = ''.join(f.ui_matrix_html(blueprint / ('ui/' + level + '-views.md'), REPO)
                           for level in ('block', 'job', 'task'))
        for title, entry in guide['sections'].items():
            if title == '🧭 Around the Work':
                self.assertIn(title, matrices)  # Shared row heading after matrix transposition.
            else:
                self.assertIn('data-title="'+html.escape(title, quote=True)+'"', matrices)
            self.assertTrue(entry['what'])
            self.assertTrue(entry['layout'])
        for ref in guide['examples']['block'].values():
            self.assertTrue((REPO / ref / 'board.md').is_file())
        board = REPO / guide['examples']['block']['Design Board']
        before = {p: p.read_bytes() for p in board.rglob('*') if p.is_file()}
        for key in guide['view_routes']:
            page = f.render(THEME, REPO, board, 'report', guide['view_routes'][key]['group'])
            self.assertIn(f'aria-current="page">{key}</a>', page)
        self.assertEqual(before, {p: p.read_bytes() for p in board.rglob('*') if p.is_file()})
        blueprint_page = f.render(WORK_THEME, REPO, blueprint, 'report', 'ui-block')
        self.assertIn('Work Structure', blueprint_page)
        self.assertIn('Block Type × View Button', blueprint_page)
        self.assertIn('data-title="🎯 The goals"', blueprint_page)

    def test_use_cases_have_real_public_pages_and_correct_task_roles(self):
        ui = REPO / 'blueprints/Project-Ladder/work/b12_theme_design/ui'
        guide = json.loads((ui / 'view-guide.json').read_text())
        # Public fixtures must remain portable; no deployment paths or identities.
        with patch.object(use_case_examples, '_json', return_value={}):
            for level, kinds in guide['use_cases'].items():
                matrix = f.ui_matrix_html(ui / (level+'-views.md'), REPO)
                for kind, cases in kinds.items():
                    for case, configured in cases.items():
                        rows = use_case_examples.examples(ui / (level+'-views.md'), REPO, guide, level, kind, case)
                        self.assertEqual(len(rows), len(configured))
                        self.assertIn('data-title="'+case+'"', matrix)
                        for row in rows:
                            self.assertEqual(row['label'], 'Blueprint example')
                            self.assertEqual(d.level_of(row['page']).lower(), level)
                            if level == 'task':
                                role = {'Reason ideas':'t00', 'One design':'design', 'Review whole':'t99'}[kind]
                                self.assertEqual(d.R.kind_of(row['page']), role)
                        if not configured:
                            self.assertIn('No linked examples yet.', matrix)
            self.assertEqual(list(guide['use_cases']['job']), ['Design Job'])
        for level, kinds in guide['type_view_routes'].items():
            for kind, routes in kinds.items():
                page = REPO / guide['examples'][level][kind]
                allowed = d.views(page, REPO, 'report')
                for route in routes.values():
                    self.assertIn(route['group'], {*allowed, 'mindmap'})
