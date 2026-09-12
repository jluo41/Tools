"""Review survives prose edits without becoming manuscript text or approval."""
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.outline import plan_card, OutlineMixin
from live.outline_comments import save_comment, comments, comment_list
from live.outline_preview import read_previews, save_preview, record_token, bullet_token, preview_path
from src.plan_shape import iter_plan_bullets

PLAN = '''# S-test · outline v1.1
approved: ✅ JL
## C1 · Introduction
### C1.P1 · Problem
- B1 · Physicians differ in their prescribing decisions
  Note: first point
  Evidence: none · test fixture
- B2 · Clinical conditions constrain the available choices
  Note: second point
  Evidence: none · test fixture
### C1.P2 · Design
- B1 · Claims capture the observed prescribing outcomes
  Note: other paragraph
  Evidence: none · test fixture
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
        self.tokens = {b['address']: bullet_token(b) for b in iter_plan_bullets(PLAN)}
        for address, token in self.tokens.items():
            save_preview(self.page, address, 'A candidate sentence.', token, 'missing')

    def payload(self, identity='PC' + 'a' * 32, address='C1.P1.B1', message='Make the subject clearer.'):
        return dict(address=address, comment_id=identity, author='Reviewer', comment=message,
                    expected_bullet=self.tokens[address],
                    expected_record=record_token(read_previews(self.page)[address]))

    def test_comment_roundtrip_scoped_and_no_publication(self):
        before = self.page.read_bytes(), self.plan.read_bytes()
        old_token = self.payload()['expected_record']
        result, error = save_comment(self.page, self.payload())
        self.assertIsNone(error)
        self.assertEqual(result['open_count'], 1)
        record = read_previews(self.page)['C1.P1.B1']
        self.assertEqual(record['text'], 'A candidate sentence.')
        self.assertEqual(record_token(record), old_token)
        self.assertEqual(comments(record)[0]['quote'], record['text'])
        self.assertEqual(comments(record)[0]['shape'], 'v1.1')
        self.assertEqual(comment_list(read_previews(self.page), 'C1.P2'), ('', 0))
        self.assertEqual(before, (self.page.read_bytes(), self.plan.read_bytes()))
        self.assertEqual(len(list(self.plan.parent.glob('*-outline-*'))), 1)

    def test_prose_edit_preserves_comment_quote_and_reply(self):
        save_comment(self.page, self.payload())
        path = preview_path(self.page)
        source = path.read_text().replace('> Shape: v1.1', '> Shape: v1.1\n>> Codex · Addressed: Named the actor. · 260911 1200 UTC', 1)
        path.write_text(source)
        record = read_previews(self.page)['C1.P1.B1']
        review = record['reviews']
        _, error = save_preview(self.page, 'C1.P1.B1', 'Physicians choose different treatments.',
                                self.tokens['C1.P1.B1'], record_token(record))
        self.assertIsNone(error)
        updated = read_previews(self.page)['C1.P1.B1']
        self.assertEqual(updated['reviews'], review)
        listing, count = comment_list(read_previews(self.page), 'C1.P1')
        self.assertEqual(count, 0)
        self.assertIn('Addressed', listing)
        self.assertIn('Sentence revised since this comment', listing)
        self.assertIn('0 open · 1 addressed', plan_card(self.page))
        self.assertIn('A candidate sentence.', listing)
        self.assertNotIn('Comment', updated['text'])

    def test_retry_is_idempotent_and_collisions_rejected(self):
        payload = self.payload()
        save_comment(self.page, payload)
        before = preview_path(self.page).read_bytes()
        result, error = save_comment(self.page, payload)
        self.assertIsNone(error)
        self.assertEqual(result['open_count'], 1)
        self.assertEqual(preview_path(self.page).read_bytes(), before)
        _, error = save_comment(self.page, {**payload, 'comment': 'Different text'})
        self.assertIn('identity', error)

    def test_concurrent_comments_preserved(self):
        payloads = [self.payload('PC' + str(n) * 32) for n in range(5)]
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(pool.map(lambda p: save_comment(self.page, p), payloads))
        self.assertTrue(all(error is None for _, error in results))
        self.assertEqual(len(comments(read_previews(self.page)['C1.P1.B1'])), 5)

    def test_lost_response_retry_after_sentence_clearing(self):
        payload = self.payload()
        save_comment(self.page, payload)
        save_preview(self.page, payload['address'], '', payload['expected_bullet'], payload['expected_record'])
        result, error = save_comment(self.page, payload)
        self.assertIsNone(error)
        self.assertEqual(result['open_count'], 1)
        self.assertEqual(len(comments(read_previews(self.page)[payload['address']])), 1)

    def test_stale_sentence_and_bullet_reject_without_writes(self):
        payload = self.payload()
        save_preview(self.page, payload['address'], 'Changed sentence.', payload['expected_bullet'], payload['expected_record'])
        before = preview_path(self.page).read_bytes()
        _, error = save_comment(self.page, payload)
        self.assertIn('Sentence changed', error)
        self.assertEqual(preview_path(self.page).read_bytes(), before)
        payload = self.payload()
        self.plan.write_text(PLAN.replace('first point', 'changed point'))
        _, error = save_comment(self.page, payload)
        self.assertIn('Bullet changed', error)

    def test_comment_text_inert_and_multiline_cannot_inject_records(self):
        result, error = save_comment(self.page, self.payload(message='</p><script>alert(1)</script>\n## C2.P1.B1\n> Comment bogus'))
        self.assertIsNone(error)
        self.assertNotIn('<script>', result['comments_html'])
        self.assertIn('&lt;script&gt;', result['comments_html'])
        self.assertEqual(len(read_previews(self.page)), 3)
        self.assertEqual(len(comments(read_previews(self.page)['C1.P1.B1'])), 1)

    def test_invalid_or_missing_targets_do_not_write(self):
        before = preview_path(self.page).read_bytes()
        for patch in ({'author': ''}, {'comment': ''}, {'comment_id': '../../x'},
                      {'address': 'C1.P8.B1'}, {'author': 'A · B'}, {'comment': 5}):
            _, error = save_comment(self.page, {**self.payload(), **patch})
            self.assertIsNotNone(error)
        self.assertEqual(preview_path(self.page).read_bytes(), before)

    def test_comments_are_after_reading_and_keep_existing_controls(self):
        save_comment(self.page, self.payload())
        card = plan_card(self.page, path_q='/Board/board.md', file_q='S-test.md')
        self.assertEqual(card.count('class="paragraph-comments"'), 2)
        self.assertLess(card.index('Read paragraph'), card.index('class="paragraph-comments"'))
        self.assertIn('value="C1.P1.B1"', card)
        self.assertIn('Make the subject clearer.', card)
        self.assertNotIn('+ Bullet', card)
        self.assertIn('Save Bullet', card)

    def test_endpoint_routes_to_preview_not_shape(self):
        handler = OutlineMixin()
        handler.target = lambda p: (self.page, self.page.parent)
        result, error = handler.plug_outline({**self.payload(), 'action': 'comment-preview'})
        self.assertIsNone(error)
        self.assertIn('comment_id', result)
        self.assertNotIn('version', result)  # no compact-Shape rebuild required

    def test_symlink_preview_refused(self):
        path = preview_path(self.page)
        target = path.with_name('source.md')
        path.rename(target)
        path.symlink_to(target)
        before = target.read_bytes()
        _, error = save_comment(self.page, self.payload())
        self.assertIn('local Markdown', error)
        self.assertEqual(target.read_bytes(), before)
