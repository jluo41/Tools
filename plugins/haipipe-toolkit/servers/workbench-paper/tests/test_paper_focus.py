"""Paper's common frame: live routing, scope isolation and preserved workflows."""
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '_host'))
from host_paths import bootstrap
bootstrap()
from live import focus_page as f, frame, paper_focus as p, skills_section, work_frame as w


class PaperFocusTest(unittest.TestCase):
    def test_shared_content_owners_are_in_the_view_skill_links(self):
        catalog = {}
        for name in ('haipipe-paper-related', 'haipipe-paper-story'):
            skill = self.root / 'skills' / name / 'SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('# ' + name)
            catalog[name] = ('Description', '1', skill)
        with patch.object(skills_section, 'catalog', return_value=catalog):
            for view, name in [('idea', 'haipipe-paper-related'), ('displays', 'haipipe-paper-story')]:
                bodies = p.shared_bodies(self.board, self.root, 'paper', 'Block', view,
                                         self.topics, [], [], [], self.rows, only=('skills',))
                self.assertIn(name, bodies['skills'][0])

    def test_job_identity_matches_renderer_and_only_uses_own_header(self):
        cases = [('j11_writing_v1130_desk', '✍️ Writing Version', 'Manuscript drafting'),
                 ('j12_writing_v0215_desk', '✍️ Writing Version', 'Feedback revision'),
                 ('j01_evidence_display', '🖼️ Display Evidence', 'Figure and table preparation'),
                 ('j02_evidence_value', '🔢 Value Evidence', 'Printed-value verification'),
                 ('j03_evidence_cite', '📚 Citation Evidence', 'Citation verification'),
                 ('j21_submission_v1130_desk', '📮 Submission', 'Submission package preparation')]
        for name, kind, case in cases:
            with self.subTest(name=name):
                job = self.board / name
                job.mkdir(exist_ok=True)
                face = job / (name + '.md')
                face.write_text(f'# Example\nuse-case: {case}\n\n## Notes\nuse-case: WRONG_BODY\n')
                html = f.render(frame.themes()['paper'], self.root, job, 'report')
                identity = re.search(r'<dl class="job-identity">.*?</dl>', html, re.S).group()
                self.assertIn(kind, identity)
                self.assertIn(case, identity)
                self.assertNotIn('WRONG_BODY', identity)
                face.write_text('# Example\n\n## Notes\nuse-case: WRONG_BODY\n')
                identity = f.job_identity_html('paper', job, self.root, f.read_face(job, self.root))
                self.assertIn(kind, identity)
                self.assertNotIn('Use case', identity)

    def test_unknown_evidence_job_does_not_invent_an_identity(self):
        job = self.board / 'j99_evidence_misc'
        job.mkdir()
        (job / (job.name + '.md')).write_text('# Other evidence\nuse-case: A local purpose\n')
        self.assertEqual(f.job_identity_html('paper', job, self.root,
                                            f.read_face(job, self.root)), '')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.board = self.root / 'paper/Paper-Example'
        self.board.mkdir(parents=True)
        (self.board / 'board.md').write_text('# Paper Example\nboard-kind: paper-board\nstory-current: s02-story\n')
        self.topics = []
        for name, tags, marker in [('s01-ideation', '', 'IDEA'), ('s02-story', '', 'STORY'),
                                    ('s03-unassigned', '', 'UNASSIGNED')]:
            t = self.board / name
            t.mkdir()
            (t / (name + '.md')).write_text(
                f'# {name}\n**Tags:** {tags}\n\n## Decisions\n{name}-D01 · {marker}_DECISION 2026-11-02\n'
                f'## Checklist\n- [ ] {marker}_CHECK\n## Things to Know\n{marker}_NOTE\n')
            self.topics.append((t, [], {'tags': []}))
        self.job = self.board / 'j11_writing_v1130_desk'
        self.job.mkdir()
        (self.job / (self.job.name + '.md')).write_text('# Version\n')
        self.rows = []
        for n, topic, view in [('story', self.topics[1][0], ''), ('override', self.topics[1][0], 'idea'),
                               ('unassigned', None, '')]:
            run = self.job / 'runs' / ('r01_' + n)
            (run / 'result').mkdir(parents=True)
            (run / 'run.yaml').write_text(f'run: r01_{n}\nskill: skill_{n}\n')
            (run / 'result/runtime.yaml').write_text('started_at: 2026-11-03T10:00:00\n')
            (run / 'question_collection.md').write_text(n)
            self.rows.append(dict(path=run, page=self.job, topic=topic, view=view, title=n + '_QUESTION',
                                  state='waiting', form=None, asks=[], answers=None, received='', applied={}, about='', feeds=[]))

    def test_explicit_view_overrides_topic_and_unassigned_never_falls_into_writing(self):
        story = p.scope(self.board, self.root, 'story', self.topics, self.rows, [])
        self.assertEqual(story['interactions'], self.rows[:1])
        self.assertEqual(story['runs'], [self.rows[0]['path']])
        self.assertEqual(story['topics'], self.topics[1:2])
        self.assertEqual(p.scope(self.board, self.root, 'idea', self.topics, self.rows, [])['interactions'], self.rows[1:2])
        self.assertEqual(p.scope(self.board, self.root, 'draft', self.topics, self.rows, [])['interactions'], [])
        self.assertEqual(p.scope(self.board, self.root, None, self.topics, self.rows, [])['interactions'], self.rows)

    def test_all_eight_sections_share_scope_and_rail_retains_records(self):
        catalog = {}
        for name in ['haipipe-paper-story', 'haipipe-paper-draft', 'skill_story', 'skill_override', 'skill_unassigned']:
            md = self.root / 'skills' / name / 'SKILL.md'
            md.parent.mkdir(parents=True)
            md.write_text(name)
            catalog[name] = ('Description', '1', md)
        with patch.object(skills_section, 'catalog', return_value=catalog):
            args = (self.board, self.root, 'paper', 'Block', 'story', self.topics, [], [], [], self.rows)
            bodies = p.shared_bodies(*args)
            for key, marker in [('studio', 's02-story'), ('interactions', 'story_QUESTION'),
                                ('decisions', 'STORY_DECISION'), ('checklist', 'STORY_CHECK'), ('know', 'STORY_NOTE'),
                                ('timeline', 'r01_story'), ('skills', 'skill_story'), ('files', 'r01_story')]:
                self.assertIn(marker, bodies[key][0], key)
            combined = ''.join(html for html, _ in bodies.values())
            for marker in ['IDEA_DECISION', 'UNASSIGNED_DECISION', 'override_QUESTION', 'unassigned_QUESTION', '/skill_override']:
                self.assertNotIn(marker, combined)
            rail = p.shared_bodies(self.board, self.root, 'paper', 'Block', None, self.topics, [], [], [], self.rows)
            self.assertIn('UNASSIGNED_DECISION', rail['decisions'][0])
            self.assertIn('unassigned_QUESTION', rail['interactions'][0])
            self.assertIn('skill_unassigned', rail['skills'][0])

    def test_topic_explicit_metadata_overrides_legacy_role(self):
        face = self.topics[1][0] / 's02-story.md'
        face.write_text('view: idea\n' + face.read_text())
        self.assertEqual(p.scope(self.board, self.root, 'story', self.topics, self.rows, [])['topics'], [])
        self.assertIn(self.topics[1], p.scope(self.board, self.root, 'idea', self.topics, self.rows, [])['topics'])

    def test_live_report_and_old_work_bookmark_are_the_same_view(self):
        theme = frame.themes()['paper']
        with patch.object(f, 'interactions', return_value=self.rows):
            report = f.render(theme, self.root, self.board, 'report', 'story')
            legacy = f.render(theme, self.root, self.board, 'work', 'work-story')
        for html in (report, legacy):
            self.assertIn('📋 Review Content', html)
            self.assertIn('🧭 Around the Work', html)
            self.assertNotIn('Process</h3>', html)
            self.assertNotIn('Results</h3>', html)
            self.assertNotIn('unassigned_QUESTION', html)
            self.assertNotIn('view-caption', re.sub(r'<style>.*?</style>', '', html, flags=re.S))
            content = html.split('id="work-shared"', 1)[1]
            positions = [content.index(title) for _, title in w.SHARED]
            self.assertEqual(positions, sorted(positions))
            self.assertEqual(html.count('<h2>📋 Review Content</h2>'), 1)
            self.assertEqual(html.count('<summary>🎨 Studio'), 1)
            self.assertNotIn('aria-label="Work"', html)
        self.assertEqual(report, legacy)

    def test_legacy_renderers_and_version_workflow_remain_available(self):
        from live import board_views, paper_version
        self.assertIn('work-story', board_views.board_work_views(self.board, self.root, lambda s, p: s))
        version = f.render(frame.themes()['paper'], self.root, self.job, 'work', '')
        self.assertIn('Work', version)
        self.assertNotIn('work-shared', re.sub(r'<style>.*?</style>', '', version, flags=re.S))


if __name__ == '__main__':
    unittest.main()
