"""Display Cards must open on the inspectable artifact, not bury it below prose."""

import tempfile
import unittest
from pathlib import Path

from src import body as board_body
from src.page_board import tree_relink


class DisplayCardPreviewTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.preview = self.root / "preview.png"
        self.preview.write_bytes(b"preview")
        self.previous = (
            board_body.BASE,
            list(board_body.CARDS),
            board_body.CHIP_N,
            set(board_body.FACE_IDS),
        )
        board_body.BASE = self.root
        board_body.CARDS.clear()
        board_body.CHIP_N = 0

    def tearDown(self):
        board_body.BASE, cards, board_body.CHIP_N, face_ids = self.previous
        board_body.CARDS[:] = cards
        board_body.FACE_IDS.clear()
        board_body.FACE_IDS.update(face_ids)
        self.tmp.cleanup()

    def test_display_preview_precedes_status_explanation(self):
        board_body._chip(
            "disp fig", "ready", "display01", "status explanation",
            {"preview": [("img", "Current Float", self.preview, "")]},
        )
        card = board_body.CARDS[-1]
        self.assertLess(card.index("ccprev"), card.index("status explanation"))

    def test_non_display_card_keeps_explanation_first(self):
        board_body._chip(
            "cite", "ok", "example2026", "citation explanation",
            {"preview": [("img", "Source image", self.preview, "")]},
        )
        card = board_body.CARDS[-1]
        self.assertLess(card.index("citation explanation"), card.index("ccprev"))

    def test_span_card_page_id_becomes_a_split_site_route(self):
        board_body.FACE_IDS.clear()
        board_body.FACE_IDS.add("S-Main-4")
        board_body._chip(
            "card",
            "span",
            "Main Results section",
            "Target Page: S-Main-4 · Uses: QBt1-Display1",
        )
        card = board_body.CARDS[-1]
        self.assertIn('href="#S-Main-4"', card)
        linked = tree_relink(
            card,
            {"#S-Main-4": "../QBt/S-Main-4-results.html"},
        )
        self.assertIn('href="../QBt/S-Main-4-results.html"', linked)

    def test_span_card_does_not_link_an_unknown_page_id(self):
        board_body.FACE_IDS.clear()
        board_body._chip(
            "card",
            "span",
            "Main Results section",
            "Target Page: S-Main-4",
        )
        self.assertNotIn("<a ", board_body.CARDS[-1])

    def test_owner_indexed_display_short_and_long_names_are_markers(self):
        class Unit:
            def __init__(self, path):
                self.path = path

        class Index:
            displays = {
                "QBt1-Display1-trait-table": Unit(
                    self.root / "QBt1-Display1-trait-table"
                )
            }
            by_short = {"QBt1-Display1": displays["QBt1-Display1-trait-table"]}

        previous_paper = board_body.PAPER
        previous_marker = board_body.MARKER
        try:
            board_body.use_paper(Index())
            short = board_body.MARKER.search("Inspect QBt1-Display1 here.")
            long = board_body.MARKER.search(
                "Inspect QBt1-Display1-trait-table here."
            )
            self.assertEqual(short.group(6), "QBt1-Display1")
            self.assertEqual(long.group(6), "QBt1-Display1-trait-table")
        finally:
            board_body.PAPER = previous_paper
            board_body.MARKER = previous_marker


if __name__ == "__main__":
    unittest.main()
