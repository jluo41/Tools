"""Scope and failure semantics must not turn no coverage into success."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from checks.common.results import Result, exit_code
from checks.run import check_targets, main
from checks.skills.studio.scope import kind


class Runner(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()

    def test_unsupported_target_is_not_success(self):
        page = self.root / 'other.md'
        page.write_text('# Other\n')
        self.assertEqual(exit_code(check_targets([page], self.root)), 2)

    def test_missing_target_is_error(self):
        self.assertEqual(exit_code(check_targets([self.root / 'missing'], self.root)), 2)

    def test_empty_block_is_uncovered(self):
        (self.root / 'board.md').write_text('# Block\n')
        self.assertEqual(exit_code(check_targets([self.root], self.root)), 2)

    def test_no_targets_do_not_pass(self):
        self.assertEqual(exit_code(check_targets([], self.root)), 2)

    def test_outside_target_is_error(self):
        self.assertEqual(exit_code(check_targets([self.root.parent], self.root)), 2)

    def test_cli_requires_explicit_target(self):
        with self.assertRaises(SystemExit) as exc:
            main([])
        self.assertEqual(exc.exception.code, 2)

    def test_rule_execution_failure_is_error(self):
        topic = self.root / 's51-example'
        topic.mkdir()
        (topic / f'{topic.name}.md').write_text('**Delivery type:** skill')
        with patch('checks.run.manifest.read', side_effect=ImportError('missing dependency')):
            results = check_targets([topic], self.root)
        self.assertEqual(exit_code(results), 2)
        self.assertIn('missing dependency', results[0].detail)

    def test_duplicate_targets_checked_once(self):
        topic = self.root / 's51-example'
        topic.mkdir()
        (topic / f'{topic.name}.md').write_text('**Delivery type:** skill')
        with patch('checks.run.manifest.read', return_value=(None, [Result('FAIL', 'bindings', topic, 'bad')])) as read:
            results = check_targets([topic, topic], self.root)
        self.assertEqual(read.call_count, 1)
        self.assertEqual(exit_code(results), 1)

    def test_embedded_skill_view_does_not_make_a_skills_topic(self):
        data = {'views': [
            {'name': 'Structure', 'items': [{'name': 'Folder', 'path': 'structure.html'}]},
            {'name': 'Skills', 'items': [{'name': 'one', 'path': 'skills/one/SKILL.md'}]},
        ]}
        self.assertIsNone(kind(self.root / 's01-structure', data))

    def test_type_with_another_renderer_is_not_rebuilt_as_requirements(self):
        self.assertIsNone(kind(self.root / 's72-studio-type-preview', {'views': []}))

    def test_block_does_not_follow_a_topic_outside_the_space(self):
        (self.root / 'board.md').write_text('# Block\n')
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 's51-outside').symlink_to(outside, target_is_directory=True)
            self.assertEqual(exit_code(check_targets([self.root], self.root)), 2)


if __name__ == '__main__':
    unittest.main()
