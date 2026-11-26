"""ⓘ on every element (JL 261124: "every element will have that"): the layer rides on every focus page, and a
comment on an element address is written and shown back."""
import json
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()
from live import element_info as EI, focus_page, frame  # noqa: E402
from live.item_card_route import item_card_act  # noqa: E402


class ElementInfoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.block = self.root / 'b01_study'
        self.block.mkdir()
        (self.block / 'board.md').write_text('# b01 · Study\n\ngoal: Compare the methods.\n')

    def tearDown(self):
        self.tmp.cleanup()

    def test_every_focus_page_carries_the_layer_with_the_page_parts(self):
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block)
        self.assertIn('window.__elInfo=', page)
        data = json.loads(page.split('window.__elInfo=', 1)[1].split(';</script>', 1)[0])
        self.assertEqual({k for k, _, _ in data['kinds']} >= {'band', 'fold', 'path', 'title'}, True)
        self.assertIn(EI.MARK, data['empty'])

    def test_a_comment_on_an_element_is_written_and_shown_back(self):
        code, res = item_card_act(self.root, {'page': 'b01_study', 'address': 'el.overview.fold.goal', 'act': 'add',
                                              'text': 'Too long.'})
        self.assertEqual(code, 200, res)
        data = json.loads(EI.assets(self.block, self.root).split('window.__elInfo=', 1)[1].split(';</script>', 1)[0])
        self.assertIn('Too long.', data['slots']['el.overview.fold.goal'])

    def test_the_files_pane_marks_the_page_folder_and_fades_the_rest(self):
        page = focus_page.render(frame.Theme(name='work'), self.root, self.block, panel='files')
        self.assertIn('window.__scopePage="b01_study"', page)   # JL 261125: out of this job's scope, transparent
        self.assertIn('.fixed-folder .sc-out{opacity', page)        # only the Block part fades; UI and Skills are the page's own
        self.assertNotIn('sc-what', page)                           # a folder's title is on the hover card, not its row


if __name__ == '__main__':
    unittest.main()
