"""A Block Structure topic's drawing: every name of structure.md, as pictures."""
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import block_structure_draw as draw  # noqa: E402

TREES = """## Folder
> bNN_〈block〉/  | the Block
>   jNN_〈job〉/
>   board.md

## Job-Task
> 〈Work Block〉
>   〈job-group-name〉  # Job group  | a decade of Job numbers
>     jNN_〈job〉  # Job name

## Studio
> 〈Work Block〉
>   〈🎯 Design〉 · s0N  # Studio Type: 〈none yet〉
>     s0N-〈question〉
"""


class StructureDrawing(unittest.TestCase):
    def test_every_name_is_drawn_and_the_things_are_pictures(self):
        with tempfile.TemporaryDirectory() as tmp:
            topic = Path(tmp) / "s01-sample"
            topic.mkdir()
            (topic / "structure.md").write_text(TREES, encoding="utf-8")
            els = draw.drawing(topic)
            text = " ".join(e.get("text", "") for e in els)
            for name in draw.names(topic):
                self.assertIn(name, text)
            self.assertNotIn("  | ", text)                       # a hover is not drawn
            self.assertGreaterEqual(sum(e["type"] in ("line", "ellipse") for e in els), 6)   # folders, files, a group
            self.assertEqual(len({e["id"] for e in els}), len(els))


if __name__ == "__main__":
    unittest.main()
