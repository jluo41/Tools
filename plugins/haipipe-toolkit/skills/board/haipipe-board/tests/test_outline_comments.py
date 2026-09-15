"""Draft Space deliberately has no browser comment surface or write path."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.outline import OutlineMixin, plan_card
from live.outline_comments import paragraph_comments, save_comment
from live.outline_preview import bullet_token, preview_path, read_previews, record_token
from src.plan_shape import iter_plan_bullets


PLAN = '''# S-test · outline v1.1
approved: ✅ JL
## C1 · Introduction
### C1.P1 · Problem
- B1 · Physicians differ in their prescribing decisions
  Note: first point
  Evidence: none · test fixture
  Draft: A candidate sentence.
'''


class PreviewCommentsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.page = Path(self.tmp.name) / 'S-test.md'
        self.page.write_text('# Test\npage-type: section\n## Content\nPublished sentence.\n')
        (self.page.parent / 'outline').mkdir()
        self.plan = self.page.parent / 'outline/S-test-outline-v1.1.md'
        self.plan.write_text(PLAN)
        block = iter_plan_bullets(PLAN)[0]
        self.token = bullet_token(block)
        self.record = read_previews(self.page)['C1.P1.B1']

    def payload(self):
        return dict(address='C1.P1.B1', comment_id='PC' + 'a' * 32,
                    author='Reviewer', comment='Make the subject clearer.',
                    expected_bullet=self.token,
                    expected_record=record_token(self.record))

    def test_render_has_no_comment_surface_or_editor(self):
        card = plan_card(self.page)
        self.assertNotIn('paragraph-comments', card)
        self.assertNotIn('data-preview-comment', card)
        self.assertNotIn('Save comment', card)
        self.assertNotIn('Comment', card)
        self.assertNotIn('Save Bullet', card)

    def test_comment_writer_is_rejected_without_writing(self):
        before = self.plan.read_bytes()
        result, error = save_comment(self.page, self.payload())
        self.assertIsNone(result)
        self.assertIn('read-only', error)
        self.assertEqual(self.plan.read_bytes(), before)

    def test_legacy_comment_renderer_is_empty(self):
        self.assertEqual(
            paragraph_comments(read_previews(self.page),
                               {b['address']: b for b in iter_plan_bullets(PLAN)},
                               'C1.P1', '', ''),
            '',
        )

    def test_retired_endpoint_does_not_write_outline(self):
        handler = OutlineMixin()
        handler.target = lambda p: (self.page, self.page.parent)
        before = preview_path(self.page).read_bytes()
        result, error = handler.plug_outline({**self.payload(), 'action': 'comment-preview'})
        self.assertIsNone(error)
        self.assertEqual(result, {'url': '/_board/outline?path=&file='})
        self.assertEqual(preview_path(self.page).read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
