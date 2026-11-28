"""A Block Structure topic's Structure page: drawn from structure.md by the type's own tree."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
import type_requirements
sys.path.insert(0, str(type_requirements.SPACE / 'plugins/haipipe-toolkit/servers/_host'))
import block_structure_page as page

TREES = """## Folder
> bNN_〈block〉/  | the Block
>   board.md

## Job-Task
> 〈Work Block〉
>   〈job-group-name〉  # Job group  | a decade of Job numbers
>     jNN_〈job〉  # Job name

## Studio
> 〈Work Block〉
>   〈🎯 Design〉 · s0N  # Studio Type: 〈none yet〉
"""


class StructurePage(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=type_requirements.SPACE / 'examples')
        self.topic = Path(self.tmp.name) / 's01-sample'
        self.topic.mkdir()
        (self.topic / 'structure.md').write_text(TREES, encoding='utf-8')
        (self.topic / 'studio-views.json').write_text(json.dumps({'check_type': 'x', 'views': [
            {'name': 'Structure', 'items': []}, {'name': 'Draw', 'items': []}, {'name': 'Examples', 'items': []}]}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_three_parts_one_page_no_examples(self):
        out = page.build(self.topic)
        html = out[self.topic / 'delivery/structure.html']
        for anchor in page.PARTS.values():
            self.assertIn(f'id="{anchor}"', html)
        self.assertIn('data-level="job-group" title="a decade of Job numbers"', html)   # level colour and hover
        self.assertNotIn('  | ', html)
        views = json.loads(out[self.topic / 'studio-views.json'])
        self.assertEqual(views['check_type'], 'x')
        self.assertEqual([v['name'] for v in views['views']], ['Structure', 'Draw'])
        self.assertEqual([i['name'] for i in views['views'][0]['items']], ['Folder', 'Job-Task', 'Studio'])

    def test_a_missing_part_is_an_error(self):
        (self.topic / 'structure.md').write_text('## Folder\n> bNN_〈block〉/\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            page.build(self.topic)


if __name__ == '__main__':
    unittest.main()
