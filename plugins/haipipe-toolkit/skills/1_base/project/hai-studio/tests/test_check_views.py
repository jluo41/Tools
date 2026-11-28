"""Type-defined checks survive generation and never invent execution results."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS.parent / 'gallery/skills/scripts'))
import check_views
import skills_views
import type_requirements


class CheckViews(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.kind = self.root / 'block/s71-type'
        self.topic = self.root / 'block/s01-instance'
        self.kind.mkdir(parents=True)
        self.topic.mkdir()
        self.source = self.kind / 'elements.md'
        self.source.write_text('## Structure\n### Studio\nmust:\n- Use Folder Tree\ncheck: Expand a Band\n')
        self.data = {'check_type': 'block/s71-type', 'custom': 'retain', 'views': [{'name': 'Structure', 'items': []}]}
        for topic in (self.topic, self.kind):
            (topic / 'studio-views.json').write_text(json.dumps(self.data))
        self.old = (type_requirements.SPACE, skills_views.SPACE)
        type_requirements.SPACE = skills_views.SPACE = self.root

    def tearDown(self):
        type_requirements.SPACE, skills_views.SPACE = self.old
        self.tmp.cleanup()

    def write(self, outputs):
        for p, text in outputs.items():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)

    def test_type_and_instance_inherit_the_same_source(self):
        for target in (self.kind, self.topic):
            out = check_views.build(target, root=self.root)
            page = out[target / 'delivery/check.html']
            self.assertIn('Use Folder Tree', page)
            self.assertIn('Expand a Band', page)
            self.assertIn('Check definition' if target == self.kind else 'Not verified', page)
            self.assertNotIn('Passed', page)
            meta = json.loads(out[target / 'studio-views.json'])
            self.assertEqual(meta['views'][-1]['name'], 'Check')
            self.assertEqual(meta['custom'], 'retain')

    def test_changed_criteria_change_the_generated_page(self):
        first = check_views.build(self.topic, root=self.root)
        self.write(first)
        self.source.write_text(self.source.read_text().replace('Folder Tree', 'Collapsible Folder Tree'))
        second = check_views.build(self.topic, root=self.root)
        self.assertNotEqual(first[self.topic / 'delivery/check.html'], second[self.topic / 'delivery/check.html'])

    def test_invalid_and_missing_type_fail(self):
        for name in ('../outside', '/tmp/outside', 'missing'):
            with self.assertRaises(ValueError):
                check_views.build(self.topic, dict(self.data, check_type=name), self.root)

    def test_type_regeneration_preserves_one_check(self):
        for _ in range(2):
            self.write(type_requirements.build(self.kind))
        data = json.loads((self.kind / 'studio-views.json').read_text())
        self.assertEqual([v['name'] for v in data['views']], ['Structure', 'Check'])
        self.assertTrue((self.kind / 'delivery/check.html').is_file())

    def test_skills_regeneration_maps_checks_to_actual_skills(self):
        self.source.write_text('## 〈skill〉\n### SKILL.md\nmust:\n- Read the whole file\ncheck: Open SKILL.md\n')
        skill = self.root / 'skills/example'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('Example')
        for args in (['--skills', 'skills/example'], [], ['--check']):
            self.assertEqual(skills_views.main(['block/s01-instance', *args]), 0)
        meta = json.loads((self.topic / 'studio-views.json').read_text())
        self.assertEqual([v['name'] for v in meta['views']], ['example', 'Check'])
        self.assertEqual(meta['views'][-1]['items'][0]['name'], 'example')
        self.assertEqual(skills_views.skills_of(self.topic), ['skills/example'])
        (skill / 'new.md').write_text('New file')
        self.assertEqual(skills_views.main(['block/s01-instance', '--check']), 1)

    def test_empty_requirements_are_not_a_pass(self):
        self.source.write_text('# No criteria')
        with self.assertRaises(ValueError):
            check_views.build(self.topic, root=self.root)

    def test_element_layout_keeps_top_and_right_requirements(self):
        self.source.write_text('## Structure\nmust:\n- Keep all left tabs\n### Studio\nmust:\n- Use Folder Tree\ncheck: Expand a Band\n')
        out = check_views.build(self.topic, dict(self.data, check_layout='elements'), self.root)
        meta = json.loads(out[self.topic / 'studio-views.json'])
        self.assertEqual(meta['views'][-1]['items'][0]['name'], 'Structure › Studio')
        page = out[self.topic / 'delivery/check.html']
        for text in ('Keep all left tabs', 'Use Folder Tree', 'Expand a Band', 'Not verified'):
            self.assertIn(text, page)
        self.assertNotIn('Passed', page)

    def test_unknown_layout_fails(self):
        with self.assertRaises(ValueError):
            check_views.build(self.topic, dict(self.data, check_layout='invalid'), self.root)


if __name__ == '__main__':
    unittest.main()
