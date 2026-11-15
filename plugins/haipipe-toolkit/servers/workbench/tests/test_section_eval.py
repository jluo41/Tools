"""★ AI-eval (section_eval.py): each numbered section's readability on its bar, ☆ before a read, ★ N? after a change."""
import json
import unittest

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame, section_eval  # noqa: E402

import focus_page_fixtures as fixtures  # noqa: E402


class SectionEvalTest(fixtures.FocusPageCase):
    def page(self):
        self.face.write_text('# R\n\n## Review Content\n\n### 🗓️ The week\n\n- Monday: the logs.\n')
        return focus_page.render(frame.Theme(name='work'), self.root, self.block, 'report', 'overview')

    def evals(self, page, **change):
        ((_, end, title, _, body),) = section_eval.sections(page)
        entry = {'score': 8, 'hash': section_eval.digest(page[body:end]), 'comments': ['Short and first.'],
                 'by': 'AI-eval', 'at': '261114'} | change
        (self.block / 'ai-eval').mkdir(exist_ok=True)
        (self.block / section_eval.STORE).write_text(json.dumps({'Overview': {title: entry}}))

    def test_a_section_never_read_shows_an_empty_star(self):
        self.assertIn('<span class="ai-star none" title="AI readability: not read yet">☆</span></summary>', self.page())

    def test_a_read_section_shows_its_score_and_comments(self):
        self.evals(self.page())
        page = self.page()
        self.assertIn('>★ 8</span></summary>', page)
        self.assertIn('<div class=ai-eval><b>★ 8/10</b> AI readability<ul><li>Short and first.</li>', page)

    def test_a_section_changed_since_its_read_shows_a_question_mark(self):
        self.evals(self.page(), hash='000000000000')
        self.assertIn('>★ 8?</span></summary>', self.page())

    def test_the_comments_do_not_change_the_hash(self):
        first = self.page()
        self.evals(first)
        marked = self.page()
        ((_, end, _, _, body),) = section_eval.sections(marked)
        self.assertEqual(section_eval.digest(marked[body:end]), json.loads((self.block / section_eval.STORE).read_text())
                         ['Overview']['🗓️ The week']['hash'])


if __name__ == '__main__':
    unittest.main()
