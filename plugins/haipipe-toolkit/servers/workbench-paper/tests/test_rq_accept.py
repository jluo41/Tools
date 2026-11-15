"""Accept on a Research Question's edit card writes the new question into the Story's own face, only while the row
still reads as the card's Original (cards.md §7); otherwise it refuses and the card stays proposed. Temp folder only."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import item_card_route, item_cards  # noqa: E402
from live import rq_accept  # noqa: E402,F401  (registers the RQ adapter, as paper_theme does at start)

HEAD = "# s02 · Story\n\n## Content\n\n### 3 · Research Questions\n\n"
KEYED = (HEAD + "| RQ | question | why |\n|---|---|---|\n"
         "| H1 | <first question>? | <why one> |\n| H2 | <second question>? | <why two> |\n\n### 4 · Stakes\n\n<stakes>\n")
LISTED = HEAD + "**The paper's question**: <whole>?\n\n1. <first question>? ⬜\n2. <second question>? ⬜\n"
CARD = ("# s02-story-x · revise\n\n## Pass 1 · test\n\n### Edit · {addr} · sharpen\nBy: test\nWhy: sharper\n"
        "Original: {old}\nExpected: <a sharper question>?\nState: proposed\n")


class RqAcceptTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.page = self.root / "Paper-X" / "s02-story-x"
        (self.page / "draft" / "records").mkdir(parents=True)
        self.face = self.page / "s02-story-x.md"

    def tearDown(self):
        self.tmp.cleanup()

    def story(self, text, addr, old):
        self.face.write_text(text, encoding="utf-8")
        item_cards.files(self.page)["revise"].write_text(CARD.format(addr=addr, old=old), encoding="utf-8")

    def accept(self, addr):
        return item_card_route.item_card_act(self.root, {"page": "Paper-X/s02-story-x", "address": addr, "act": "accept",
                                                         "card": f"Edit · {addr} · sharpen", "was": "proposed"})

    def state(self):
        return item_cards.parse_edits(item_cards.files(self.page)["revise"])[0]["state"]

    def test_accept_writes_the_row_of_its_key(self):
        self.story(KEYED, "RQ.H2", "<second question>?")
        code, _ = self.accept("RQ.H2")
        self.assertEqual(code, 200)
        text = self.face.read_text(encoding="utf-8")
        self.assertIn("| H2 | <a sharper question>? | <why two> |", text)
        self.assertIn("| H1 | <first question>? | <why one> |", text)      # the other row as it was
        self.assertIn("### 4 · Stakes\n\n<stakes>", text)                   # and the rest of the face
        self.assertEqual(self.state(), "accepted")

    def test_a_changed_row_refuses_and_the_card_stays_proposed(self):
        self.story(KEYED.replace("<second question>?", "<edited by hand>?"), "RQ.H2", "<second question>?")
        code, res = self.accept("RQ.H2")
        self.assertEqual(code, 409)
        self.assertIn("Original", res["err"])
        self.assertIn("<edited by hand>?", self.face.read_text(encoding="utf-8"))
        self.assertEqual(self.state(), "proposed")

    def test_the_list_form_writes_item_n(self):
        self.story(LISTED, "RQ.RQ2", "<second question>?")
        code, _ = self.accept("RQ.RQ2")
        self.assertEqual(code, 200)
        self.assertIn("2. <a sharper question>? ⬜", self.face.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
