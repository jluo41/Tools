"""Authored views share Studio's existing renderer without replacing other topics."""
import json
import re
import tempfile
import unittest
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

from host_paths import bootstrap
bootstrap()
from live import frame, studio_tabs, studio_views


class StructureViewsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.topic = self.root / 'b01' / 's01-structure'
        self.topic.mkdir(parents=True)
        (self.topic.parent / 'board.md').write_text('# Block\n')
        (self.topic / 's01-structure.md').write_text('s01 · Structure\n====\n')
        (self.root / 'jobs.html').write_text('<p>Job 1</p>')
        (self.root / 'studio.html').write_text('<p>Studio topic 1</p>')
        (self.root / 'SKILL.md').write_text('# Skill\n')

    def manifest(self, views):
        (self.topic / 'studio-views.json').write_text(json.dumps({'views': views}))

    def test_four_top_views_and_no_standalone_skill_topic(self):
        self.manifest([{'name': n, 'items': [{'name': n, 'path': p}]} for n, p in
                       [('Structure', 'jobs.html'), ('Draw', 'studio.html'),
                        ('Examples', 'jobs.html'), ('Skills', 'SKILL.md')]])
        html = studio_tabs.render([(self.topic, [], {})], self.root)
        self.assertEqual(re.findall(r'data-studio-view="\d+"[^>]*>([^<]+)</button>', html),
                         ['Structure', 'Draw', 'Examples', 'Skills'])
        self.assertEqual(html.count('class="studio-topic-content"'), 1)
        self.assertIn('SKILL.md', html)

    def test_paths_and_symlinks_cannot_escape_served_space(self):
        (self.root / 'escape.md').symlink_to('/etc/hosts')
        self.manifest([{'name': 'Skills', 'items': [{'name': x, 'path': x} for x in
            ['../outside.md', '/etc/hosts', 'https://example.test', 'escape.md', 'missing.md']]}])
        self.assertIsNone(studio_views.read_views(self.topic, self.root))

    def test_empty_and_duplicate_views_are_omitted(self):
        self.manifest([{'name': 'Empty', 'items': []},
                       {'name': 'Skills', 'items': [{'name': 'Skill', 'path': 'SKILL.md'}]},
                       {'name': 'Skills', 'items': [{'name': 'Other', 'path': 'jobs.html'}]}])
        views, _ = studio_views.read_views(self.topic, self.root)
        self.assertEqual([v[0] for v in views], ['Skills'])

    def test_multiple_skills_use_shared_side_tabs(self):
        self.manifest([{'name': 'Skills', 'items': [{'name': 'Skill 1', 'path': 'SKILL.md'},
                                                  {'name': 'Skill 2', 'path': 'studio.html'}]}])
        html = studio_tabs.render([(self.topic, [], {})], self.root)
        self.assertIn('data-pbtab=', html)
        self.assertIn('Skill 1', html)
        self.assertIn('Skill 2', html)

    def test_malformed_manifest_falls_back_to_existing_page(self):
        (self.topic / 'studio-views.json').write_text('{oops')
        (self.topic / 's01-structure.html').write_text('<p>Existing page</p>')
        html = studio_tabs.render([(self.topic, [], {})], self.root)
        self.assertIn('>Page</button>', html)

    def test_examples_require_a_block_and_draw_keeps_fragment(self):
        self.manifest([{'name': 'Examples', 'items': [
            {'name': 'Example 1', 'block': 'b01'},
            {'name': 'Not a Block', 'block': 'b01/s01-structure'}]},
            {'name': 'Draw', 'items': [{'name': 'Jobs', 'path': 'jobs.html', 'fragment': 'draw'}]}])
        views, parts = studio_views.read_views(self.topic, self.root)
        self.assertEqual(len(parts['Examples']), 1)
        self.assertIn('path=b01&layout=focus&section=work', views[0][1])
        self.assertTrue(views[1][1].endswith('#draw'))

    def test_an_item_may_be_a_live_workbench_page_and_an_earlier_one(self):
        # b17 trace 261127/1440: a view's left tabs can be parts of a live page
        live = frame.ROUTE + '?path=b01&layout=focus&mark=view=overview'
        self.manifest([{'name': 'Page-Job', 'items': [
            {'name': 'job-overview', 'url': live},
            {'name': 'elsewhere', 'url': 'https://example.test/x'},
            {'name': 'earlier', 'url': live, 'old': True}]}])
        views, parts = studio_views.read_views(self.topic, self.root)
        self.assertEqual(parts['Page-Job'], [('job-overview', live, False), ('earlier', live, True)])

    def test_a_view_with_nothing_current_reads_faded(self):
        # b17 trace 261127/2010: an instance keeps every view of its type; one it has not built shows faded
        self.manifest([{'name': 'Draw', 'items': [{'name': 'Draw', 'path': 'jobs.html'}]},
                       {'name': 'QuickHtml', 'items': [{'name': 'rule', 'path': 'studio.html', 'old': True}]}])
        html = studio_tabs.render([(self.topic, [], {})], self.root)
        self.assertRegex(html, r'<button[^>]*class="old"[^>]*>QuickHtml</button>')
        self.assertNotRegex(html, r'<button[^>]*class="old"[^>]*>Draw</button>')

    def test_topics_keep_independent_panel_ids(self):
        self.manifest([{'name': 'Structure', 'items': [
            {'name': 'Jobs', 'path': 'jobs.html'}, {'name': 'Studio', 'path': 'studio.html'}]}])
        other = self.topic.parent / 's02-structure'
        other.mkdir()
        (other / 'studio-views.json').write_bytes((self.topic / 'studio-views.json').read_bytes())
        html = studio_tabs.render([(self.topic, [], {}), (other, [], {})], self.root)
        self.assertIn('sts01structure0', html)
        self.assertIn('sts02structure0', html)

    def test_excalidraw_uses_canvas_viewer(self):
        (self.root / 'model.excalidraw').write_text('{"type":"excalidraw","elements":[]}')
        self.manifest([{'name': 'Draw', 'items': [
            {'name': 'Model', 'path': 'model.excalidraw'}]}])
        views, _ = studio_views.read_views(self.topic, self.root)
        self.assertEqual(views[0][1], studio_tabs.frame._draw_url(self.root / 'model.excalidraw', self.root))
        self.assertNotEqual(views[0][1], '/model.excalidraw')

    def test_mindmap_uses_existing_folded_viewer(self):
        from live import frame
        path = self.root / 'organization.mindmap.md'
        path.write_text('# Block\n\n- [Job type] Type <!-- n01 -->\n  - [Job name] Job <!-- n02 -->\n    - [Task type] Kind <!-- n03 -->\n      - [Task name] Task <!-- n04 -->\n')
        self.manifest([{'name': name, 'items': [
            {'name': 'Jobs', 'path': path.name}]} for name in ('Structure', 'Draw', 'Examples')])
        views, _ = studio_views.read_views(self.topic, self.root)
        for _, href, _ in views:
            self.assertEqual(parse_qs(urlsplit(href).query),
                             {'view': ['focus-map'], 'path': [path.name], 'fit': ['1']})
        html = studio_tabs.render([(self.topic, [], {})], self.root)
        self.assertIn('view=focus-map', html)
        rendered = frame.mindmap_module().fragment(path, path.name, editable=False)
        self.assertIn('pm-folds', rendered)
        self.assertIn('data-foldall=1', rendered)
        self.assertIn('Task', rendered)
        self.assertNotIn('contenteditable=plaintext-only', rendered)

    def test_mindmap_outside_space_is_rejected(self):
        path = self.root / 'escape.mindmap.md'
        path.symlink_to('/etc/hosts')
        self.manifest([{'name': 'Structure', 'items': [{'name': 'Map', 'path': path.name}]}])
        self.assertIsNone(studio_views.read_views(self.topic, self.root))

    def test_images_render_responsively_alone_and_in_side_tabs(self):
        (self.root / 'model.png').write_bytes(b'preview')
        for count in (1, 2):
            with self.subTest(count=count):
                self.manifest([{'name': 'Draw', 'items': [
                    {'name': f'Model {i}', 'path': 'model.png'} for i in range(count)]}])
                html = studio_tabs.render([(self.topic, [], {})], self.root)
                self.assertEqual(html.count('<img src="/model.png"'), count)
                self.assertNotIn('data-studio-src="/model.png"', html)
                self.assertIn('width:100%;height:auto', html)


if __name__ == '__main__':
    unittest.main()
