"""Board host: Draft Space exposes Scratch as its browser write surface.

Historical feedback records remain readable, but new Draft interaction uses
the Page-owned Scratch writer and lands in the selected Outline plus its
paired Run receipt.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.outline import OutlineMixin, plan_card


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

    def test_render_has_scratch_composer_but_no_plan_editor(self):
        card = plan_card(self.page, self.board, '/board.md', 'S-test/S-test.md')
        self.assertIn('data-scratch-scope="paragraph"', card)
        self.assertIn('data-scratch-target="C1.P1"', card)
        self.assertIn('name="path" value="/board.md"', card)
        self.assertIn('name="file" value="S-test/S-test.md"', card)
        self.assertNotIn('data-paragraph-feedback', card)
        self.assertNotIn('data-preview-write', card)
        self.assertNotIn('Save Bullet', card)

    def test_feedback_action_is_removed_from_draft_space(self):
        handler = OutlineMixin()
        handler.target = lambda p: ('S-test/S-test.md', self.board)
        result, error = handler.plug_outline(self.payload())
        self.assertIsNone(result)
        self.assertEqual(error, 'Draft comments are removed; use Scratch Mode')
        self.assertFalse((self.folder / 'results').exists())

    def test_scratch_action_accepts_the_board_route_fields(self):
        handler = OutlineMixin()
        handler.target = lambda p: ('S-test/S-test.md', self.board)
        result, error = handler.plug_outline({
            'action': 'scratch', 'phase': 'save',
            'path': '/board.md', 'file': 'S-test/S-test.md',
            'scope': 'paragraph', 'target': 'C1.P1',
            'notes': 'Keep the opening focused.',
        })
        self.assertIsNone(error, error)
        self.assertEqual(result['status'], 'open')
        self.assertEqual(result['target'], 'C1.P1')
        self.assertTrue((self.folder / 'results' / result['run'] / 'v001.md').is_file())

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
