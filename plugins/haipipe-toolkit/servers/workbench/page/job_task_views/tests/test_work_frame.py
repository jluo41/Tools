"""Live topic mapping, shared history provenance, and four-view routing."""
import tempfile
import re
import unittest
from pathlib import Path
import sys
from host_paths import bootstrap

bootstrap()
from live import frame, focus_page as f, work_frame as w
sys.path.insert(0, str(next(d for d in Path(__file__).resolve().parents if d.name == "workbench") / "tests"))  # shared fixtures
import focus_page_fixtures as fixtures  # noqa: E402


class WorkFrameTest(unittest.TestCase):
    def test_walkthrough_checklist_is_view_scoped_and_tracks_recordings(self):
        (self.block / 'board.md').write_text(
            f'# Example\nui-task: missing/example\nui-task: {self.a.relative_to(self.root)}\n'
            f'ui-task: {self.b.relative_to(self.root)}\nui-job: {self.job.relative_to(self.root)}\n')
        (self.block / 'walks').mkdir()
        recording = self.block / 'walks/task.html'
        recording.write_text('<html>Recorded walkthrough</html>')
        def checklist(view):
            return w.shared_bodies(self.block, self.root, 'work', 'Block', view,
                                   [], [], [], [], [], only='checklist')['checklist'][0]
        task = checklist('ui-task')
        self.assertIn('t01_a', task)
        self.assertIn('t02_b', task)
        self.assertIn('Recorded', task)
        self.assertIn('Not recorded', task)
        self.assertNotIn('t01_a', checklist('ui-job'))
        self.assertNotIn('Record walkthrough', checklist('overview'))
        self.assertIn('Task UI', checklist(None))
        self.assertIn('Job UI', checklist(None))
        recording.unlink()
        self.assertNotIn('Recorded', checklist('ui-task'))
        recording.symlink_to(self.root.parent / 'outside.html')
        self.assertIsNone(f.ui_walk_path(recording, self.a, 0, self.root))

    def test_job_identity_uses_own_declared_case_across_views(self):
        face = self.job / 'j01_work.md'
        face.write_text('# Work\nuse-case: Data preparation\nstate: ACTIVE\n')
        for view in ('overview', 'standing', 'findings', 'delivery'):
            html = f.render(frame.Theme(name='work'), self.root, self.job, 'report', view)
            identity = re.search(r'<dl class="job-identity">.*?</dl>', html).group()
            self.assertIn('<dt>Job type</dt><dd>🧩 Job</dd>', identity)
            self.assertIn('<dt>Use case</dt><dd>Data preparation</dd>', identity)
            self.assertLess(html.index(identity), html.index('view-band'))   # its views are bands (JL 261124)

    def test_job_identity_does_not_guess_or_inherit_a_case(self):
        (self.block / 'board.md').write_text('# Block\nuse-case: Inherited purpose\n')
        (self.job / 'j01_work.md').write_text('# Work\n\n## Content\nuse-case: Example only\n')
        data = f.read_face(self.job, self.root)
        identity = f.job_identity_html('work', self.job, self.root, data)
        self.assertNotIn('Use case', identity)
        self.assertIn('Collaboration Job', f.job_identity_html('cowork', self.job, self.root, data))
        self.assertIn('Inquiry Job', f.job_identity_html('discovery', self.job, self.root, data))
        self.assertEqual(f.job_identity_html('design', self.job, self.root, data), '')
        self.assertEqual(f.job_identity_html('work', self.a, self.root, data), '')

    def test_people_identity_and_html_escaping(self):
        people = self.block / 'j00_people'
        people.mkdir()
        identity = f.job_identity_html('cowork', people, self.root, {'use_case':'<script>example</script>'})
        self.assertIn('👥 People', identity)
        self.assertNotIn('<script>', identity)
        self.assertIn('&lt;script&gt;', identity)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / 'work/b01_example'
        self.block.mkdir(parents=True)
        (self.block / 'board.md').write_text('# Example\nspine: Compare results.\nclose: Evidence checked.\n')
        self.job = self.block / 'j01_work'
        self.job.mkdir()
        (self.job / 'j01_work.md').write_text('# Work\nstate: ACTIVE\n')
        self.a, self.b = self.task('t01_a'), self.task('t02_b')

    def task(self, name):
        p = self.job / name
        p.mkdir()
        (p / (name + '.md')).write_text('# ' + name + '\nstate: ACTIVE\n')
        return p

    def test_topics_reuse_links_and_keep_unlinked_work_without_overwrite(self):
        questions = [{'group': 'Other Work', 'work': [{'path': 'j01_work/t01_a'}]}]
        groups = w.topics_for(self.block, self.root, questions)
        self.assertEqual(groups, [('Other Work', [self.a, self.b])])
        narrowed = w.tree(self.block, [self.a], self.root)
        self.assertIn('t01_a', narrowed)
        self.assertNotIn('t02_b', narrowed)
        self.assertNotIn(str(self.root), narrowed)

    def test_plan_and_results_has_no_topic_navigation(self):
        groups = [('First topic', [self.a]), ('Second topic', [self.b])]
        page = w.status(self.block, self.root, f.read_face(self.block, self.root), groups)
        self.assertNotIn('🧩 View BJTR', page)            # JL 261109: "maybe we don't need this"
        self.assertNotIn('work-status-topic', page)

    def test_block_runs_only_appear_when_the_block_is_selected(self):
        run = self.block / 'runs/r01_collect'
        run.mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_collect\nstatus: completed\n')
        self.assertIn('r01_collect', w.tree(self.block, [self.block], self.root))
        self.assertNotIn('r01_collect', w.tree(self.block, [self.a], self.root))
        self.assertIn('r01_collect', w.tree(self.block, [run], self.root))
        other = self.block / 'runs/r02_other'
        other.mkdir()
        (other / 'run.yaml').write_text('run: r02_other\nstatus: completed\n')
        self.assertNotIn('r02_other', w.tree(self.block, [run], self.root))

    def test_topics_cannot_import_sibling_or_external_work(self):
        outside = self.root / 'elsewhere'
        outside.mkdir()
        groups = w.topics_for(self.block, self.root, [{'group': 'Outside', 'work': ['../../elsewhere']}])
        self.assertNotIn('Outside', [n for n, _ in groups])

    def test_job_level_runs_and_dated_receipts_have_real_source_links(self):
        run = self.job / 'runs/r01_review'
        (run / 'result').mkdir(parents=True)
        (run / 'run.yaml').write_text('run: r01_review\nstatus: completed\n')
        receipt = run / 'result/runtime.yaml'
        receipt.write_text('status: completed\nstarted_at: 2026-11-07T09:00:00\nfinished_at: 2026-11-08T10:00:00\n')
        self.assertIn('r01_review', w.tree(self.block, [self.job], self.root))
        history = w.timeline(self.block, self.root, [], [], [])
        self.assertIn('Run started', history)
        self.assertIn('Run finished', history)
        self.assertIn('runtime.yaml', history)
        self.assertIn('2026-11-07', history)
        self.assertNotIn('Run started</b><p>r01_review · completed', history)

    def test_a_ui_view_shows_only_its_studio_group(self):
        for name, group in (('s01-block-ui', 'Block UI'), ('s02-job-ui', 'Job UI')):
            topic = self.block / name
            topic.mkdir()
            (topic / (name + '.md')).write_text(f'# {name}\n**Tags:** {group}\n\nDecided\n-------\n\n{name}-D01 · Kept.\n')
        topics = f.topic_rows(self.block, self.root)
        block_ui = w.shared(self.block, self.root, 'work', 'Block', 'ui-block', topics, [], [], [], [])
        self.assertIn('s01-block-ui-D01', block_ui)
        self.assertNotIn('s02-job-ui-D01', block_ui)   # its folder name may show in the Block's own Files tree
        overview = ''.join(body for body, _ in w.shared_bodies(self.block, self.root, 'work', 'Block', None, topics, [], [], [], []).values())
        self.assertIn('s01-block-ui-D01', overview)
        self.assertIn('s02-job-ui-D01', overview)

    def test_all_shared_sections_use_explicit_scope_and_rail_keeps_unassigned(self):
        from live import skills_section, work_files
        from unittest.mock import patch
        (self.block / 'board.md').write_text('# Example\n## Decisions\nb01-D01 · ROOT_UNASSIGNED 2026-11-01\n## Checklist\n- [ ] ROOT_CHECK\n')
        topics = []
        for name, tag, marker in [('s01-status', 'Status', 'STATUS'),
                                  ('s02-findings', 'Findings', 'FINDINGS'),
                                  ('s03-other', '', 'UNASSIGNED')]:
            topic = self.block / name
            topic.mkdir()
            (topic / (name + '.md')).write_text(
                f'# {name}\n**Tags:** {tag}\n\n## Decisions\n{name}-D01 · {marker}_DECISION 2026-11-02\n'
                f'## Checklist\n- [ ] {marker}_CHECK\n## Things to Know\n{marker}_NOTE\n')
            topics.append((topic, [], {'tags': [tag] if tag else []}))
        rows = []
        for name, target, explicit in [('status', topics[0][0], ''), ('override', topics[0][0], 'delivery'),
                                       ('findings', topics[1][0], ''), ('unassigned', None, '')]:
            run = self.a / 'runs' / ('r01_' + name)
            (run / 'result').mkdir(parents=True)
            (run / 'run.yaml').write_text(f'skill: skill_{name}\n')
            (run / 'result/runtime.yaml').write_text('started_at: 2026-11-03T10:00:00\n')
            (run / 'question_collection.md').write_text(name)
            rows.append(dict(path=run, page=self.a, topic=target, view=explicit, title=name + '_QUESTION',
                             state='waiting', form=None, asks=[], answers=None, received='', applied={}, about='', feeds=[]))
        catalog = {}
        for name in ['hai-job', 'hai-task', 'hai-run', 'hai-interaction', 'hai-studio'] + ['skill_' + r['title'].split('_')[0] for r in rows]:
            md = self.root / 'skills' / name / 'SKILL.md'
            md.parent.mkdir(parents=True)
            md.write_text(name)
            catalog[name] = ('description', '1', md)
        with patch.object(skills_section, 'catalog', return_value=catalog):
            scope = w.shared_scope(self.block, self.root, 'standing', topics, rows, [])
            # Status also holds what waits on the person, unless a form names another view (261109)
            self.assertEqual(scope['interactions'], [rows[0], rows[2], rows[3]])
            self.assertEqual(scope['runs'], [rows[0]['path']])
            body = w.shared_bodies(self.block, self.root, 'work', 'Block', 'standing', topics, rows, [], [], rows)
            self.assertIn('s01-status', body['studio'][0])
            self.assertIn('status_QUESTION', body['interactions'][0])
            self.assertIn('STATUS_DECISION', body['decisions'][0])
            self.assertIn('STATUS_CHECK', body['checklist'][0])
            self.assertIn('STATUS_NOTE', body['know'][0])
            self.assertIn('r01_status', body['timeline'][0])
            self.assertIn('/skill_status', body['skills'][0])
            combined = ''.join(html for html, _ in body.values())
            self.assertIn('unassigned_QUESTION', body['interactions'][0])
            for marker in ['ROOT_UNASSIGNED', 'ROOT_CHECK', 'UNASSIGNED_DECISION', 'FINDINGS_DECISION',
                           'override_QUESTION', '/skill_override']:
                self.assertNotIn(marker, combined)
            self.assertNotIn('r01_findings', body['timeline'][0])   # its form waits in Status; its Run stays out
            delivery = w.shared_scope(self.block, self.root, 'delivery', topics, rows, [])
            self.assertEqual(delivery['interactions'], [rows[1]])
            rail = w.shared_bodies(self.block, self.root, 'work', 'Block', None, topics, [], [], [], rows)
            all_html = ''.join(html for html, _ in rail.values())
            for marker in ['ROOT_UNASSIGNED', 'ROOT_CHECK', 'UNASSIGNED_DECISION', 'FINDINGS_DECISION',
                           'override_QUESTION', 'unassigned_QUESTION', '/skill_override', 'r01_findings']:
                self.assertIn(marker, all_html)
            files = dict(work_files.folder_groups(self.block, self.root, 'standing', scope=scope,
                         skill_rows=w.scope_skills(self.block, self.root, 'work', 'Block', 'standing', scope)))
            self.assertNotIn(self.block, files['🧩 Blocks'])
            self.assertIn(rows[0]['path'], files['🧩 Blocks'])
            self.assertEqual(files['🗂️ Workspace'], [])
            self.assertEqual(files['💻 Code'], [])

    def test_rail_skills_are_not_truncated_to_ten(self):
        from live import skills_section
        from unittest.mock import patch
        names = [f'skill_{i}' for i in range(12)]
        catalog = {name: ('description', '1', self.root / name / 'SKILL.md') for name in names}
        with patch.object(skills_section, 'catalog', return_value=catalog), patch.object(skills_section, 'run_skills', return_value=names):
            scope = w.shared_scope(self.block, self.root, None, [], [], [])
            self.assertEqual([name for name, _ in w.scope_skills(self.block, self.root, 'work', 'Block', None, scope)], names)
            self.assertEqual(w.scope_skills(self.block, self.root, 'work', 'Block', 'standing', scope), [])

    def test_explicit_page_view_and_topic_view_precedence(self):
        (self.a / (self.a.name + '.md')).write_text('# Task\nview: report-status\n## Checklist\n- [ ] Scoped check\n')
        topic = self.block / 's01-topic'
        topic.mkdir()
        (topic / (topic.name + '.md')).write_text('# Topic\nview: delivery\n**Tags:** Status\n')
        topics = [(topic, [], {'tags': ['Status']})]
        scope = w.shared_scope(self.block, self.root, 'standing', topics, [], [])
        self.assertEqual(scope['pages'], [self.a])
        self.assertEqual(scope['topics'], [])
        self.assertEqual(w.shared_scope(self.block, self.root, 'delivery', topics, [], [])['topics'], topics)
        body = w.shared_bodies(self.block, self.root, 'work', 'Block', 'standing', topics, [], [], [], [])
        self.assertIn('Scoped check', body['checklist'][0])
        self.assertNotIn('Scoped check', w.shared_bodies(self.block, self.root, 'work', 'Block', 'findings', topics, [], [], [], [])['checklist'][0])
        ancestor = dict(page=self.root, state='to know')
        self.assertEqual(w.shared_scope(self.block, self.root, None, [], [], [ancestor])['knows'], [])

    def test_decisions_read_as_one_row_each_with_tags_from_their_own_words(self):
        text = ('s01-D01 · Its delivery is one piece: the table (JL 261031). Replaced by s01-D02 (261031).\n\n'
                's01-D02 · Its delivery is the whole file: every rung (JL 261031).\n\n'
                's01-D03 · Six pieces, the shared parts. This replaces the last clause of s01-D01.\n\n'
                's01-D04 · The grid stays, in red, as an open proposal.\n\n'
                'Previously stated requirements:\n\n1. Show the path first.\n')
        html = w.decision_list(text, self.block, self.root)
        self.assertEqual(html.count('<details>'), 4)
        self.assertIn('wk-dec-head>Its delivery is one piece</span><span class=wk-dec-tag>Replaced</span>', html)
        self.assertIn('wk-dec-head>Its delivery is the whole file</span></summary>', html)    # no tag invented
        self.assertIn('wk-dec-head>Six pieces, the shared parts</span></summary>', html)      # replaces, not replaced
        self.assertIn('<span class=wk-dec-tag>Proposed</span>', html)
        self.assertIn('Show the path first', html)                                        # other text kept

    def test_a_skill_shows_every_file_it_holds_skill_md_first(self):
        from live import skills_section as S
        home = self.root / 'skills/demo'
        for rel in ('SKILL.md', 'CHANGELOG.md', 'ref/rules.md', 'scripts/run.py', '.pytest_cache/v/x', 'scripts/__pycache__/run.pyc'):
            (home / rel).parent.mkdir(parents=True, exist_ok=True)
            (home / rel).write_text('x')
        files = [p.relative_to(home).as_posix() for p in S.skill_files(home / 'SKILL.md', self.root)]
        self.assertEqual(files, ['SKILL.md', 'CHANGELOG.md', 'ref/rules.md', 'scripts/run.py'])
        bar = S.files_bar(home / 'SKILL.md', self.root)
        self.assertEqual(bar.count('class="sk-file'), 4)
        self.assertIn('class="sk-file on"', bar)
        (lone := self.root / 'skills/lone').mkdir(parents=True)
        (lone / 'SKILL.md').write_text('x')
        self.assertEqual(S.files_bar(lone / 'SKILL.md', self.root), '')                   # one file needs no bar

    def test_all_views_have_shared_sections_and_delivery_alias(self):
        theme = frame.Theme(name='work')
        titles = ['🎨 Studio', '🙋 Interactions', '⚖️ Decisions', '📚 Things to Know', '📝 Checklist', '🕒 Timeline', '🧰 Skills', ' Files</span></summary>']
        for level in [self.block, self.job, self.a]:
            for view in ['overview', 'standing', 'findings', 'delivery']:
                html = f.render(theme, self.root, level, 'report', view)
                for title in titles:                       # an empty one is hidden (JL 261113); a shown one is unnumbered
                    self.assertNotRegex(html, r'\d+ · ' + title)
                self.assertNotIn('No Decisions linked to this view.', html)
                for name in ['Overview']:                  # its views are bands; an empty one is not drawn (JL 261124)
                    self.assertIn(name, fixtures.band_names(html))
                self.assertNotIn('💬 Feedback', html)
                self.assertNotIn('🧭 Around the Work', html)   # the side pane holds these (hai-block A01)
        old_map = f.render(theme, self.root, self.block, 'report', 'mindmap')
        self.assertIn('id="band-overview"', old_map)   # an old view link opens the page of bands (JL 261124)
        old_delivery = f.render(theme, self.root, self.block, 'delivery')
        self.assertIn('view-band', old_delivery)
        self.assertNotIn('Acceptance', old_delivery.split('</main>')[0])   # JL 261114: empty, not drawn

    def test_delivery_feedback_has_explicit_view_ownership(self):
        rows = [{'page': self.block, 'view': 'delivery'}, {'page': self.block, 'view': ''}]
        keys = ['mindmap', 'standing', 'findings', 'delivery']
        self.assertEqual(f.view_items('work', self.block, self.root, 'Block', 'delivery', keys, rows, []), rows[:1])
        self.assertEqual(f.view_items('work', self.block, self.root, 'Block', 'mindmap', keys, rows, []), rows[1:])

    def test_report_merges_work_actions_and_old_work_links(self):
        for theme_name in ('work', 'cowork', 'discovery'):
            theme = frame.Theme(name=theme_name)
            for page in (self.block, self.job, self.a):
                report = f.render(theme, self.root, page, 'report', 'standing')
                self.assertEqual(report, f.render(theme, self.root, page, 'work', 'standing'))
                self.assertIn('view-band', report)   # its views are bands (JL 261124)
                self.assertNotIn('⚙️ Process</h3>', report)
                self.assertNotIn('>View Content</h2>', report)
                for nav in re.findall(r'<nav[^>]+aria-label="Page sections"[^>]*>(.*?)</nav>', report, re.S):
                    self.assertNotIn('>Work</a>', nav)
                    self.assertNotIn('aria-label="Work"', nav)
        report = f.render(frame.Theme(name='work'), self.root, self.block, 'report', 'standing')
        self.assertNotIn('🚧 Next steps', report)
        self.assertIn('view-band', report)   # its views are bands (JL 261124)
        self.assertNotIn('🧩 View BJTR', report)

    def test_shared_rail_order_and_child_record_rollup(self):
        (self.a / (self.a.name + '.md')).write_text('# Task\n## Decisions\nChild decision.\n## Checklist\n- [ ] Verify child.\n')
        theme = frame.Theme(name='work')
        page = f.render(theme, self.root, self.block, 'report', 'overview')
        rail = re.search(r'<nav class="focus-rail right"[^>]*>(.*?)</nav>', page, re.S)[1]
        labels = [re.sub(r'<[^>]+>', '', name).strip() for name in re.findall(r'<span class="rail-name">(.*?)</span>', rail)]
        self.assertEqual(labels, ['Report', '💼 Jobs'] + [name.removeprefix('📁 ') for _, name in w.SHARED])   # a Block with Jobs (JL 261125)
        self.assertNotIn('Child decision.', page)
        self.assertIn('Child decision.', f.render(theme, self.root, self.block, 'decisions'))
        self.assertIn('Verify child.', f.render(theme, self.root, self.block, 'checklist'))

    def test_code_type_uses_space_code_store_only(self):
        from live import work_files
        (self.block / 'src').mkdir()
        (self.block / 'code').mkdir()
        groups = dict(work_files.folder_groups(self.block, self.root))
        self.assertEqual(groups['💻 Code'], [])
        self.assertNotIn('Code</span>', work_files.render(self.block, self.root))   # the Files tree has no groups
        self.assertEqual(groups['🗂️ Workspace'], [])
        workspace = self.root / '_WorkSpace'
        workspace.mkdir()
        self.assertEqual(dict(work_files.folder_groups(self.block, self.root))['🗂️ Workspace'], [workspace])
        self.assertNotIn('path=_WorkSpace', work_files.render(self.block, self.root))
        store = self.root / 'code'
        store.mkdir()
        groups = dict(work_files.folder_groups(self.block, self.root))
        self.assertEqual(groups['💻 Code'], [store])
        self.assertNotIn('path=code&', work_files.render(self.block, self.root).replace('b01_example%2Fcode', ''))

    def test_files_pane_parts_hold_real_folders_only(self):
        from live import work_files
        from unittest.mock import patch
        block = self.root / 'Project-Fixture' / 'work' / 'b01_files'
        job = block / 'j01_build'
        job.mkdir(parents=True)
        (block / 'board.md').write_text('# Files\n')
        (block / 'runs' / 'r01_example').mkdir(parents=True)
        (block / 'private.env').write_text('SECRET=value')
        skills, ui = self.root / 'skills' / 'skill_a', self.root / 'ui_code'
        for source in (skills, ui):
            source.mkdir(parents=True)
        groups = [('🗂️ Workspace', []), ('🧩 Blocks', [block]), ('💻 Code', []),
                  ('🧰 Tools · Skills', [skills]), ('🖥️ Tools · UI', [ui])]
        with patch.object(work_files, 'folder_groups', return_value=groups), \
             patch.object(work_files, 'own_skills', return_value=[skills]):
            here, deeper = work_files.render(block, self.root), work_files.render(job, self.root)
        for page in (here, deeper):
            tree = page.split('<div class="file-tree">', 1)[1].split('</style>', 1)[0]
            self.assertLess(tree.index('<h3>Block</h3>'), tree.index('<h3>Maintain: ServerUI</h3>'))
            self.assertLess(tree.index('<h3>Maintain: ServerUI</h3>'), tree.index('<h3>Maintain: Skills</h3>'))
            self.assertEqual(tree.count('<h3>Maintain: Skills</h3>'), 1)
            self.assertIn('data-folder-path="ui_code"', tree.split('<h3>Maintain: ServerUI</h3>', 1)[1].split('</section>', 1)[0])
            maintained = tree.split('<h3>Maintain: Skills</h3>', 1)[1].split('</section>', 1)[0]
            self.assertIn('data-folder-path="skills/skill_a"', maintained)
            self.assertEqual(re.findall(r'<li data-n="(\d+)"', maintained), ['1'])   # each kind numbers its own rows
            self.assertEqual(maintained.count('class="files-where"'), 1)   # one path line: the folder the rows share
            self.assertIn('>skills/</p>', maintained)
            self.assertIn('data-folder-path="Project-Fixture/work/b01_files" open', tree)
            self.assertIn('>runs</span>', tree)
            self.assertNotIn('>r01_example</span>', tree)
            self.assertNotIn('private.env', tree)
            self.assertIn('<span aria-hidden="true">📝</span> board.md', tree)   # a file shows its type's icon
            from live.file_icons import file_icon
            self.assertIn('#3776AB', file_icon(Path('x.py')))                       # Python shows its own mark
            self.assertIn('>skill_a</span>', tree)          # a row in the shared folder: its own name
            self.assertIn('>ui_code</span>', tree)
            self.assertIn('<p class="files-where" title="Project-Fixture/work/">Project-Fixture/work/</p>', tree)
            for label in ('Tools', 'Workspace', 'Blocks', 'Code'):     # collections are never drawn as folders
                self.assertNotIn('>' + label + '</span>', tree)
            self.assertNotIn('🧵', page)
            self.assertNotIn('Sessions', page)
        self.assertIn('data-folder-path="Project-Fixture/work/b01_files/j01_build" open', deeper)   # a Job page opens to itself
        nested = [self.root / 'skills' / 'set_b' / 'skill_b', skills]                  # the real nesting is kept
        for path in nested:
            path.mkdir(parents=True, exist_ok=True)
        base, rows = work_files.flat_tree(nested, self.root)
        self.assertEqual(base, self.root / 'skills')
        self.assertLess(rows.index('>set_b</span>'), rows.index('>skill_b</span>'))
        self.assertIn('data-folder-path="skills/set_b" open', rows)                    # the way down is open
        with patch.object(work_files, 'folder_groups', return_value=groups[:3]), \
             patch.object(work_files, 'own_skills', return_value=[]):
            self.assertNotIn('<h3>Maintain: Skills</h3>', work_files.render(block, self.root))   # an empty part is not drawn

    def test_floating_files_reuses_the_files_body_without_a_second_shell(self):
        theme = frame.Theme(name='work')
        report = f.render(theme, self.root, self.block, 'report', 'overview')
        self.assertIn('class="rail-tab left"', report)
        self.assertNotIn('class="rail-tab right"', report)                  # no right rail (JL 261126)
        self.assertNotIn('id="section-drawer"', report)
        self.assertIn('<span class="rail-tab-label" aria-hidden="true">Pages</span>', report)
        self.assertNotIn('<span aria-hidden="true">☰</span>', report)
        self.assertIn('class="files-ball"', report)
        self.assertIn('aria-controls="side-menu"', report)
        self.assertIn('id="files-drawer"', report)
        # the right rail's sections sit behind the round button; each opens alone in the side pane
        self.assertRegex(report, r'data-side-key="files" data-side-src="[^"]*panel=files"')
        self.assertRegex(report, r'data-side-key="report" data-side-src="[^"]*panel=report"')
        self.assertIn('.focus-rail.right{display:none}',
                      (Path(f.__file__).resolve().parents[2] / 'focus-assets' / 'focus.css').read_text())
        # wide screens dock Files as a right split the person can widen by its left edge
        self.assertIn('<div class="files-grip" aria-hidden="true"></div>', report)
        assets = (Path(f.__file__).resolve().parents[2] / 'focus-assets')
        self.assertIn('body.files-split{padding-right:var(--files-w)}', (assets / 'focus.css').read_text())
        self.assertIn("pane.show();", (assets / 'focus.js').read_text())
        # a file clicked in the side pane opens in the main page's viewer, full size, not inside the pane
        self.assertIn("host.__wbPop(link.href, link.dataset.pop)", (assets / 'focus.js').read_text())
        # the viewer keeps one header line: the preview's own tools move up beside the file's name
        self.assertIn("bar.className = 'viewer-tools'", (assets / 'focus.js').read_text())
        self.assertIn('#focus-viewer .viewer-verbs{margin-left:auto', (assets / 'focus.css').read_text())
        bar = report.split('<dialog id="focus-viewer">')[1].split('</header>')[0]      # two icons, their names on hover
        self.assertIn('title="Go to this page" aria-label="Go to this page">↗</a>', bar)
        self.assertIn('title="Close" aria-label="Close">✕</button>', bar)
        self.assertNotIn('>Close<', bar)
        self.assertNotIn('class="mobile-rail-controls"', report)
        panel = f.render(theme, self.root, self.block, files_panel=True)
        self.assertIn('class="files-panel-content focus-content"', panel)
        self.assertIn('class="file-tree"', panel)
        self.assertNotIn('id="files-drawer"', panel)
        self.assertIn('id="focus-viewer"', panel)
        # the Files pane is the tree only: no Sessions list and no 🧵 marks pointing at it
        self.assertNotIn('class="fd-th"', panel)
        self.assertNotIn('<b>Sessions</b>', panel)
        # Files is never a page of its own: an old link renders the page, and focus.js opens Files beside it
        old_link = f.render(theme, self.root, self.block, 'files')
        self.assertNotIn('class="file-tree"', old_link.split('id="files-drawer"')[0])
        self.assertIn('data-side-key="files"', old_link)

    def test_source_tree_merges_ancestors_without_unrelated_siblings(self):
        from live import work_files
        base = self.root / 'plugins' / 'example' / 'skills'
        selected = [base / '1_base' / 'project' / 'block',
                    base / '1_base' / 'project' / 'job',
                    base / '2_work' / 'work' / 'workbench']
        for path in selected + [base / '1_base' / 'unrelated']:
            path.mkdir(parents=True)
        tree = work_files.grouped_tree(selected, self.root)
        self.assertEqual(tree.count('>1_base</span>'), 1)
        self.assertEqual(tree.count('>project</span>'), 1)
        self.assertEqual(tree.count('data-folder-src='), 3)
        self.assertNotIn('unrelated', tree)
        self.assertNotIn('<details open', tree)
        (selected[0] / 'nested').mkdir()
        self.assertEqual(work_files.grouped_tree([selected[0], selected[0] / 'nested'], self.root),
                         work_files.grouped_tree([selected[0]], self.root))

    def test_files_scope_preview_and_download_access(self):
        from live import work_files
        results = self.block / 'results'
        results.mkdir()
        (results / 'values.csv').write_text('x,y\n1,2\n')
        (self.block / 'private.env').write_text('SECRET=value')
        (self.block / 'sample.private.txt').write_text('private')
        (self.block / 'loop').symlink_to(self.block, target_is_directory=True)
        own = work_files.render(self.block, self.root, 'overview', [], [self.block])
        all_files = work_files.tree_rows(results, self.root)
        listing = work_files.tree_rows(self.block, self.root)
        self.assertNotIn('values.csv', own)
        self.assertNotIn('🗂️ Workspace', own)
        self.assertNotIn('🧩 Blocks', own)
        self.assertNotIn('<iframe', own)
        self.assertNotIn('values.csv', listing)
        self.assertIn('fragment=1', listing)
        self.assertNotIn('Select a file', own)
        self.assertNotIn('loop', listing)
        self.assertEqual(work_files.browse(Path('/etc'), self.root), '')
        self.assertIn('values.csv', all_files)
        self.assertNotIn('private.env', listing)
        self.assertNotIn('sample.private.txt', listing)
        self.assertIn('data-pop="values.csv"', all_files)
        self.assertIn('download href="/work/b01_example/results/values.csv"', work_files.preview(results / 'values.csv', self.root))
        self.assertIn('1,2', work_files.preview(results / 'values.csv', self.root))
        self.assertEqual(work_files.preview(self.block / 'private.env', self.root), '')
        self.assertEqual(work_files.preview(Path('/etc/passwd'), self.root), '')

    def test_python_preview_colors_tokens_and_preserves_incomplete_source(self):
        from live import work_files
        from html import unescape
        source = '# Note\ndef example(x):\n    return "<script>" + str(42)\n\n"""unfinished'
        rendered = work_files.python_preview(source)
        self.assertIn('class="py-keyword">def</span>', rendered)
        self.assertIn('class="py-function">example</span>', rendered)
        self.assertIn('class="py-comment"># Note</span>', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertEqual(unescape(re.sub(r'<[^>]+>', '', rendered)), source)
        unusual = '\fdef f():\n    return "a\u2028b"\n'
        self.assertEqual(unescape(re.sub(r'<[^>]+>', '', work_files.python_preview(unusual))), unusual)

    def test_undated_acceptance_does_not_become_a_timeline_event(self):
        record = self.block / 'board.md'
        history = w.timeline(self.block, self.root, [], [], [(record, 'Accepted when checks pass.')])
        self.assertIn('No dated events', history)


if __name__ == '__main__':
    unittest.main()


class BlankSectionTest(unittest.TestCase):
    def test_an_empty_shared_section_is_hidden(self):
        """JL 261113: "if the section is empty, then we can hide that section"."""
        from live import work_frame
        self.assertTrue(work_frame.blank('<p class="mut">No decision records yet.</p>'))
        self.assertTrue(work_frame.blank('<p class=mut>Nothing asked yet.</p>'))
        self.assertTrue(work_frame.blank('<p class="mut">No Studio topic here yet.</p><div class="focus-actions"><a>Add</a></div>'))
        self.assertFalse(work_frame.blank('<ol class="work-history"><li>261113</li></ol>'))
