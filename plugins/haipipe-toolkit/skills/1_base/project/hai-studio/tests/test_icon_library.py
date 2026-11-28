"""icon_library.py: an item of a downloaded Excalidraw library, drawn by its name at a place and size."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import icon_library  # noqa: E402

BOX = {"id": "a", "type": "rectangle", "x": 100, "y": 50, "width": 40, "height": 20, "strokeColor": "#000",
       "backgroundColor": "#ff0", "boundElements": [{"id": "t", "type": "text"}]}
WORD = {"id": "t", "type": "text", "x": 105, "y": 55, "width": 20, "height": 10, "fontSize": 10, "containerId": "a",
        "strokeColor": "#000", "text": "hi"}
LINE = {"id": "l", "type": "line", "x": 120, "y": 60, "width": 20, "height": 30, "strokeColor": "transparent",
        "points": [[0, 0], [-40, 30]]}


class IconLibrary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        folder = Path(self.tmp.name)
        (folder / "kit.excalidrawlib").write_text(json.dumps({"type": "excalidrawlib", "version": 2, "libraryItems": [
            {"name": "Card", "elements": [BOX, WORD, LINE]}, {"name": "Card", "elements": [BOX]}]}))
        (folder / "old.excalidrawlib").write_text(json.dumps({"version": 1, "library": [[BOX]]}))
        self.folders = (folder,)
        icon_library.libraries.cache_clear()

    def tearDown(self):
        icon_library.libraries.cache_clear()
        self.tmp.cleanup()

    def test_names_cover_both_file_forms_and_number_a_repeated_name(self):
        self.assertEqual(icon_library.names(folders=self.folders),
                         [("kit", "Card"), ("kit", "Card 2"), ("old", "item 1")])

    def test_an_item_is_placed_scaled_grouped_and_renamed(self):
        els = icon_library.item("card", "k", 10, 20, w=120, folders=self.folders)       # the box is 60 wide: x 80 to 140
        self.assertEqual([e["id"] for e in els], ["k_0", "k_1", "k_2"])
        self.assertEqual(icon_library._box(els)[:2], (10, 20))
        self.assertAlmostEqual(icon_library._box(els)[2] - 10, 120)
        self.assertEqual(els[1]["containerId"], "k_0")
        self.assertEqual(els[0]["boundElements"], [{"id": "k_1", "type": "text"}])
        self.assertEqual(els[1]["fontSize"], 20)
        self.assertTrue(all(e["groupIds"] == ["k"] for e in els))

    def test_a_colour_goes_on_lines_and_outlines_not_on_what_is_transparent(self):
        els = icon_library.item("Card", "k", 0, 0, color="#047857", folders=self.folders)
        self.assertEqual([e["strokeColor"] for e in els], ["#047857", "#047857", "transparent"])
        self.assertEqual(els[0]["backgroundColor"], "#ff0")

    def test_an_unknown_name_says_what_is_near(self):
        with self.assertRaises(KeyError) as raised:
            icon_library.item("Cart", "k", 0, 0, folders=self.folders)
        self.assertIn("near: Card", str(raised.exception))

    def test_every_item_of_the_kept_libraries_draws(self):
        icon_library.libraries.cache_clear()
        found = icon_library.names()
        self.assertGreater(len(found), 100)
        for n, (lib, name) in enumerate(found):
            self.assertTrue(icon_library.item(name, f"x{n}", 0, 0, w=100, lib=lib))


if __name__ == "__main__":
    unittest.main()
