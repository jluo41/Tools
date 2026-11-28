"""Exercise real file mutations: correct, broken and stale outputs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from checks.paths import owner, using_root
from checks.results import exit_code
from checks.run import check_targets


class StudioChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.skill = self.root / 'skills/example'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: example\n---\n# Example\n')
        self.topic = self.root / 'block/s51-skills-example'
        self.topic.mkdir(parents=True)
        (self.topic.parent / 'board.md').write_text('# Example Block\n')
        (self.topic / f'{self.topic.name}.md').write_text('**Delivery type:** skill\n')
        self.manifest = self.topic / 'studio-views.json'
        module = owner('skills_views')
        with using_root(module, self.root):
            self.manifest.write_text(module.views_text(['skills/example'], self.topic))

    def results(self, target=None):
        return check_targets([target or self.topic], self.root)

    def mutate(self, fn):
        data = json.loads(self.manifest.read_text())
        fn(data)
        self.manifest.write_text(json.dumps(data, indent=2) + '\n')

    def test_correct_output_is_read_only(self):
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(exit_code(self.results()), 0)
        after = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_missing_file_is_rejected(self):
        (self.skill / 'SKILL.md').unlink()
        self.assertEqual(exit_code(self.results()), 1)

    def test_real_file_with_wrong_tab_name_is_rejected(self):
        self.mutate(lambda d: d['views'][0]['items'][0].update(name='Rules'))
        self.assertEqual(exit_code(self.results()), 1)

    def test_extra_skill_file_requires_updated_binding(self):
        (self.skill / 'CONSTITUTION.md').write_text('# Rules\n')
        self.assertEqual(exit_code(self.results()), 1)

    def test_invalid_json_is_not_an_empty_pass(self):
        self.manifest.write_text('{')
        self.assertEqual(exit_code(self.results()), 1)

    def test_malformed_views_and_items_fail(self):
        for data in ({'views': {}}, {'views': [None]}, {'views': [{'name': 'x', 'items': [None]}]}):
            with self.subTest(data=data):
                self.manifest.write_text(json.dumps(data))
                self.assertEqual(exit_code(self.results()), 1)

    def test_parent_escape_is_rejected(self):
        self.mutate(lambda d: d['views'][0]['items'][0].update(path='../outside/SKILL.md'))
        self.assertEqual(exit_code(self.results()), 1)

    def test_symlink_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / 'SKILL.md'
            external.write_text('outside')
            (self.skill / 'SKILL.md').unlink()
            (self.skill / 'SKILL.md').symlink_to(external)
            self.assertEqual(exit_code(self.results()), 1)

    def test_duplicate_view_is_rejected(self):
        self.mutate(lambda d: d['views'].append(d['views'][0].copy()))
        self.assertEqual(exit_code(self.results()), 1)

    def test_manifest_symlink_outside_space_is_never_read_as_valid(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / 'studio-views.json'
            external.write_bytes(self.manifest.read_bytes())
            self.manifest.unlink()
            self.manifest.symlink_to(external)
            self.assertEqual(exit_code(self.results()), 2)
            self.assertEqual(exit_code(self.results(self.topic.parent)), 2)

    def test_face_symlink_outside_space_is_not_used_for_routing(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / 'face.md'
            external.write_text('**Delivery type:** skill')
            face = self.topic / f'{self.topic.name}.md'
            face.unlink()
            face.symlink_to(external)
            self.assertEqual(exit_code(self.results()), 2)

    def make_type(self, tab='SKILL.md'):
        topic = self.root / 'block/s75-studio-type-skills'
        topic.mkdir(exist_ok=True)
        (topic / 'elements.md').write_text(
            '# Requirements\n\n## 〈skill〉\nwhat: Skill\n\n'
            f'### {tab}\nwhat: Content\nmust:\n- read the actual file\ncheck: inspect the source\n')
        return topic

    def bind_check(self):
        topic = self.make_type()
        data = json.loads(self.manifest.read_text())
        data['check_type'] = topic.relative_to(self.root).as_posix()
        data['views'] = [v for v in data['views'] if v['name'] != 'Evaluation']   # this test type lists no Evaluation
        for path, text in owner('check_views').build(self.topic, data, self.root).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        return topic

    def plain_topic(self, name, items):
        topic = self.root / 'block' / name
        (topic / 'delivery').mkdir(parents=True)
        (topic / 'elements.md').write_text('# Elements\n\n## Page\nwhat: The page.\n- The actual file.\n')
        (topic / 'delivery/page.html').write_text('<p>page</p>')
        data = {'views': [{'name': 'Page', 'items': items}], 'check_type': f'block/{name}'}
        (topic / 'studio-views.json').write_text(json.dumps(data))
        return topic

    def test_live_page_item_needs_a_real_page(self):
        live = '/_board/workbench?path=block&layout=focus&mark=view=overview'
        from checks.manifest import read
        topic = self.plain_topic('s11-preview', [{'name': 'live', 'url': live}])
        self.assertEqual([r.status for r in read(topic, self.root)[1]], ['PASS'])
        for bad in ('/_board/workbench?path=nowhere', 'https://example.test/x', '/_board/workbench?path=../out'):
            (topic / 'studio-views.json').write_text(json.dumps({'views': [{'name': 'Page', 'items': [{'name': 'live', 'url': bad}]}]}))
            self.assertEqual([r.status for r in read(topic, self.root)[1]], ['FAIL'], bad)

    def test_type_with_its_own_generator_is_checked_by_it(self):
        from checks import freshness
        topic = self.plain_topic('s72-studio-type-own', [{'name': 'Page', 'path': 'block/s72-studio-type-own/delivery/page.html'}])
        (topic / 'build_type_pages.py').write_text(
            'from pathlib import Path\nHERE = Path(__file__).resolve().parent\nROOT = HERE.parents[1]\n'
            'def built(type_only=False):\n    return {HERE / "delivery/page.html": "<p>page</p>"}\n')
        data = json.loads((topic / 'studio-views.json').read_text())
        self.assertEqual([r.status for r in freshness.check(topic, data, 'type', self.root)], ['PASS'])
        (topic / 'delivery/page.html').write_text('<p>edited by hand</p>')
        self.assertEqual([r.status for r in freshness.check(topic, data, 'type', self.root)], ['FAIL'])

    def test_check_binding_preserved_and_not_a_skill(self):
        self.bind_check()
        self.assertEqual(exit_code(self.results()), 0)
        module = owner('skills_views')
        with using_root(module, self.root):
            self.assertEqual(module.skills_of(self.topic), ['skills/example'])
        self.assertIn('Not verified', (self.topic / 'delivery/check.html').read_text())

    def test_changed_type_criteria_make_check_stale(self):
        topic = self.bind_check()
        source = topic / 'elements.md'
        source.write_text(source.read_text().replace('actual file', 'whole actual file'))
        self.assertEqual(exit_code(self.results()), 1)

    def test_type_source_symlink_outside_space_is_rejected(self):
        topic = self.bind_check()
        source = topic / 'elements.md'
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside) / 'elements.md'
            external.write_bytes(source.read_bytes())
            source.unlink()
            source.symlink_to(external)
            self.assertEqual(exit_code(self.results()), 1)
            self.assertEqual(exit_code(self.results(topic)), 2)

    def test_missing_check_type_is_rejected(self):
        self.mutate(lambda d: d.update(check_type='missing'))
        self.assertEqual(exit_code(self.results()), 1)

    def test_type_placeholder_rule_reused(self):
        topic = self.make_type('Example 1')
        module = owner('type_requirements')
        with using_root(module, self.root):
            for path, text in module.build(topic).items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
        results = self.results(topic)
        self.assertEqual(exit_code(results), 1)
        self.assertTrue(any(r.rule == 'placeholders' and r.status == 'FAIL' for r in results))

    def test_post_write_validation_uses_real_checker(self):
        module = owner('skills_views')
        with using_root(module, self.root):
            (self.skill / 'CONSTITUTION.md').write_text('# Rules\n')
            self.assertEqual(module.main([str(self.topic)]), 0)
        self.assertEqual(exit_code(self.results()), 0)

    def test_post_write_invalid_names_do_not_report_success(self):
        module = owner('skills_views')
        with using_root(module, self.root):
            self.assertEqual(module.main([str(self.topic), '--skills', 'skills/example', 'skills/example']), 1)


if __name__ == '__main__':
    unittest.main()
