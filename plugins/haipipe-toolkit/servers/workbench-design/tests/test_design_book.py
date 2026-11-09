"""A Design Method Book (JL 261109): the method's own Block beside the Design Board, one Job per release."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / '_host'))
from host_paths import bootstrap
bootstrap()
from live import design_book as BK, design_focus as D, design_reader as R, focus_page as f

REPO = Path(__file__).resolve().parents[5]


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


class DesignBookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.book = self.root / 'design/DesignMethodBook-T'
        self.board = self.root / 'design/Design-T'
        _write(self.book / 'board.md', '---\nboard-kind: design-method-book\nserves: design/Design-T\n---\n# Book\n')
        for n, rel, src, sees in (('j01_method-v1_goal-only', 'method-v1', 'M01 m2', 'goal only'),
                                  ('j02_method-v2_examples', 'method-v2', 'M02 m1', 'goal and examples')):
            _write(self.book / n / f'{n}.md', f'---\nrelease: {rel}\nfrom: {src}\nsigned: ✅ 261109\n---\n# {rel}\n')
            _write(self.book / n / 'method.md', f'---\nsteps:\n  ① See input: {sees}\n  ② Reason ideas: N ideas\n---\n')
        _write(self.book / 'proposals/fewer.md', '---\nkind: change a step\nstep: ② Reason ideas\nstate: waiting\n---\n# Fewer ideas\n\nWhy.\n')
        _write(self.board / 'board.md', '# T\nboard-kind: design-board\nmethod-book: design/DesignMethodBook-T\n')
        for n, pin, rel in (('j01_g_method-v1-goal-only_inputs-v1', 'M01 m2', 'method-v1'),
                            ('j02_g_method-v2-examples_inputs-v1', 'M02 m1', 'method-v2')):
            _write(self.board / n / f'{n}.md', f'---\ngoal: G01\nmethod: {pin}\nrelease: {rel}\ninputs: inputs-v1\n---\n# Job\n')

    def test_reader_pairs_each_release_with_the_jobs_that_run_it(self):
        self.assertTrue(R.is_method_book(self.book))
        self.assertFalse(R.is_method_book(self.board))
        b = R.method_book(self.book)
        self.assertEqual([(r['id'], r['from'], [j['id'] for j in r['jobs']]) for r in b['releases']],
                         [('method-v1', 'M01 m2', ['j01']), ('method-v2', 'M02 m1', ['j02'])])
        self.assertEqual([p['title'] for p in b['proposals']], ['Fewer ideas'])
        self.assertEqual(R.book_of(self.board), self.book)

    def test_book_is_a_block_with_its_own_views(self):
        self.assertEqual(D.level_of(self.book), 'Block')
        self.assertEqual(list(D.views(self.book, self.root, 'report')), [k for k, _ in BK.BOOK_VIEWS])
        _, versions = BK.book_view(self.book, self.root, 'versions')
        self.assertIn('① See input', versions)            # what changed from method-v1 to method-v2
        self.assertEqual(D.level_of(self.book / 'j01_method-v1_goal-only'), '')   # a release is no Design Job

    def test_type_line_names_the_book_and_its_release(self):
        self.assertEqual(f.page_type('design', 'Block', self.book, self.root, {}), '📘 Design Method Book')
        self.assertEqual(f.page_type('design', 'Job', self.book / 'j01_method-v1_goal-only', self.root, {}), '📘 Method release')
        self.assertEqual(f.page_type('design', 'Block', self.board, self.root, {}), '🎨 Design Board')

    def test_the_example_book_serves_the_example_board(self):
        book = REPO / 'blueprints/Project-Ladder/design/DesignMethodBook-Example'
        b = R.method_book(book)
        self.assertEqual({r['id']: [j['id'] for j in r['jobs']] for r in b['releases']},
                         {'method-v1': ['j01', 'j02'], 'method-v2': ['j03']})
        self.assertEqual(R.book_of(REPO / 'blueprints/Project-Ladder/design/Design-Example'), book)


if __name__ == '__main__':
    unittest.main()
