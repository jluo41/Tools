"""Examples resolve existing content; bad bindings cannot become empty successes."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import type_requirements
import requirement_examples as examples
import check_views


class RequirementExamples(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.topic = self.root / 'type'
        self.instance = self.root / 'instance'
        self.block = self.root / 'block'
        for folder in (self.topic, self.instance, self.block):
            folder.mkdir()
        (self.block / 'board.md').write_text('Block')
        (self.block / 'j01_example/t02_example').mkdir(parents=True)
        self.el = {'view': 'Page-Task', 'tab': 'task-runs', 'name': 'task-runs'}
        self.write_binding({'url': '/_board/workbench?path=block/j01_example/t02_example&layout=focus&mark=view=standing'})

    def tearDown(self):
        self.tmp.cleanup()

    def write_binding(self, item):
        (self.instance / 'studio-views.json').write_text(json.dumps({'views': [
            {'name': 'Page-Task', 'items': [dict(item, name='task-runs')]}]}))
        (self.topic / 'examples.json').write_text(json.dumps({'Page-Task / task-runs': {
            'topic': 'instance', 'view': 'Page-Task', 'item': 'task-runs'}}))

    def test_task_example_stays_in_block(self):
        from urllib.parse import urlsplit, parse_qs
        url, _ = examples.resolve(self.topic, self.el, self.root)
        query = parse_qs(urlsplit(url).query)
        self.assertEqual(query['path'], ['block'])
        self.assertEqual(query['group'], ['j01'])
        self.assertEqual(query['task'], ['t02'])
        self.assertEqual(query['mark'], ['view=standing'])

    def test_missing_selector_and_source_fail(self):
        for binding in ({}, {'Page-Task / task-runs': {'topic': '../outside'}},
                        {'Page-Task / task-runs': {'topic': 'missing'}}):
            (self.topic / 'examples.json').write_text(json.dumps(binding))
            with self.assertRaises(ValueError):
                examples.resolve(self.topic, self.el, self.root)

    def test_wrong_fragment_fails(self):
        (self.instance / 'sample.html').write_text('<section id="actual">Tree</section>')
        self.write_binding({'path': 'instance/sample.html', 'fragment': 'missing'})
        with self.assertRaises(ValueError):
            examples.resolve(self.topic, self.el, self.root)

    def test_external_url_rejected(self):
        self.write_binding({'url': 'https://example.test/other'})
        with self.assertRaises(ValueError):
            examples.resolve(self.topic, self.el, self.root)

    def test_drawing_uses_shared_draw_route(self):
        from live import frame
        path = self.instance / 'example.excalidraw'
        path.write_text('{}')
        self.write_binding({'path': 'instance/example.excalidraw'})
        url, _ = examples.resolve(self.topic, self.el, self.root)
        self.assertEqual(url, frame._draw_url(path, self.root))

    def test_shared_preview_and_no_fabricated_success(self):
        output = examples.render(self.topic, self.el, self.root)
        self.assertIn('class=open-dot', output)
        self.assertIn('<summary>Example</summary>', output)
        self.assertIn('loading="lazy"', output)
        self.assertNotIn('Passed', output)
        (self.topic / 'examples.json').unlink()
        self.assertEqual(examples.render(self.topic, self.el, self.root), '')

    def test_real_types_cover_each_rendered_requirement(self):
        root = type_requirements.SPACE
        block = root / 'examples/Project-Ladder/blueprint/b17_theme_work'
        from live.studio_types import elements_of
        for name in ('s71-studio-type-block-structure', 's72-studio-type-block-job-ui-preview'):
            topic = block / name
            elements = elements_of(topic)
            views = json.loads((topic / 'studio-views.json').read_text())['views']
            labels = {v['name'] for v in views}
            for el in elements:
                siblings = [e for e in elements if e['view'] == el['view'] and e.get('tab')]
                if el['view'] not in labels or el.get('mark') or (not el.get('tab') and siblings):
                    continue
                if (topic / 'examples.json').is_file():      # a type whose Pattern is its example binds none
                    self.assertIsNotNone(examples.resolve(topic, el, root), (name, el['name']))
            all_criteria = [m for el in elements for m in el.get('must', [])]
            cards = check_views.groups(check_views.criteria(topic), views, 'elements')
            shown = [m for _, rows in cards for el in rows for m in el.get('must', [])]
            self.assertTrue(all(m in shown for m in all_criteria))

    def test_s71_shows_one_tree_the_pattern_and_no_example(self):
        root = type_requirements.SPACE
        topic = root / 'examples/Project-Ladder/blueprint/b17_theme_work/s71-studio-type-block-structure'
        outputs = type_requirements.build(topic)
        manifest = json.loads(outputs[topic / 'studio-views.json'])
        self.assertNotIn('Examples', [v['name'] for v in manifest['views']])
        check = manifest['views'][-1]
        self.assertEqual(check['name'], 'Check')
        self.assertFalse(any(i['name'].startswith('Examples') for i in check['items']))
        self.assertFalse(any(p.name.startswith('examples--') for p in outputs))
        page = outputs[topic / 'delivery/requirements/structure--job-task.html']
        self.assertNotIn('<summary>Example</summary>', page)          # one tree: the Pattern, drawn as an instance's
        self.assertIn('<dt>Pattern</dt>', page)
        self.assertIn('data-level="job-group"', page)
        self.assertIn('data-level="task-name"', page)


if __name__ == '__main__':
    unittest.main()
