"""Board host: Draft Space's one browser write is the paragraph note composer,
and it lands in the owning Run's journal under results/, never in the plan."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.outline import OutlineMixin, plan_card
from live.outline_feedback import feedback_items


PLAN = '''# S-test · outline v1.1
approved: ✅ JL
## C1 · Introduction
### C1.P1 · Problem
- B1 · Physicians differ in their prescribing decisions
  Note: first point
  Evidence: none · test fixture
  Draft: A candidate sentence.
'''


class DraftSpaceFeedbackTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.board = Path(self.tmp.name)
        (self.board / 'board.md').write_text('# board\n')
        self.folder = self.board / 'S-test'
        (self.folder / 'outline').mkdir(parents=True)
        self.page = self.folder / 'S-test.md'
        self.page.write_text('# Test\npage-type: section\n## Content\nPublished sentence.\n')
        self.plan = self.folder / 'outline/S-test-outline-v1.1.md'
        self.plan.write_text(PLAN)

    def payload(self, **over):
        base = dict(action='feedback', path='/board.md', file='S-test/S-test.md',
                    paragraph='C1.P1', kind='explore', author='Reviewer',
                    comment='Make the subject clearer.', feedback_id='fb-00aa11bb22cc')
        base.update(over)
        return base

    def test_render_has_composer_but_no_plan_editor(self):
        card = plan_card(self.page, self.board, '/board.md', 'S-test/S-test.md')
        self.assertIn('data-fb-add="C1.P1"', card)
        self.assertIn('data-paragraph-feedback', card)
        self.assertNotIn('data-preview-write', card)
        self.assertNotIn('Save Bullet', card)

    def test_feedback_action_writes_results_not_outline(self):
        handler = OutlineMixin()
        handler.target = lambda p: ('S-test/S-test.md', self.board)
        before = self.plan.read_bytes()
        result, error = handler.plug_outline(self.payload())
        self.assertIsNone(error, error)
        self.assertEqual(result['run'], 'rp-para-01_P01')
        self.assertNotIn('version', result)
        self.assertEqual(self.plan.read_bytes(), before)
        journal = self.folder / 'results/rp-para-01_P01/v001.md'
        self.assertTrue(journal.is_file())
        self.assertIn('- Kind: explore', journal.read_text())
        self.assertTrue((self.folder / 'runs/rp-para-01_P01.md').is_file())
        items = feedback_items(self.page)['C1.P1']
        self.assertEqual([i['disposition'] for i in items], ['pending'])

    def test_legacy_editor_actions_stay_rejected(self):
        handler = OutlineMixin()
        handler.target = lambda p: ('S-test/S-test.md', self.board)
        for action in ('edit-preview', 'edit-bullet', 'append-bullet', 'comment-preview'):
            result, error = handler.plug_outline({'action': action, 'path': '/board.md', 'file': 'S-test/S-test.md'})
            if action == 'comment-preview':
                self.assertIsNone(error)      # unknown legacy action: URL registration only
                self.assertEqual(result, {'url': '/_board/outline?path=/board.md&file=S-test/S-test.md'})
            else:
                self.assertIsNone(result)
                self.assertIn('read-only', error)
        self.assertFalse((self.folder / 'results').exists())


if __name__ == '__main__':
    unittest.main()
