"""Research Questions rows carry their address (workbench/ref/cards.md §2): a keyed first cell (H1, "H2 check", RQ1,
"1 · …") is parsed into rows, so a Story that writes §3 as one keyed table is a table, never the Markdown fallback; each
row is `data-addr="RQ.<key>"` and the paper's question `RQ.Q`. Placeholders only, in a temp folder."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import board_read, board_story, item_card_route  # noqa: E402

HEAD = "# s02 · Story\n\n**Stage:** explore\n\n## Content\n\n### 3 · Research Questions\n\n"
KEYED = (HEAD + "**The paper's question**: <the whole question>?\n\n"
         "| RQ | question | why the paper needs it | answer form | answer state |\n|---|---|---|---|---|\n"
         "| H1 | <first question>? | <why one> | associational | ⬜ |\n"
         "| H2 | <second question>? | <why two> | associational | ⬜ |\n"
         "| H2 check | <a check>? | <why check> | associational | ⬜ |\n\n"
         "#### 3.1 · Primary question\n<more>\n")
NUMBERED = (HEAD + "| RQ | question | why we ask it |\n|---|---|---|\n"
            "| RQ1 | <one>? | <a> |\n| 2 · how many | <two>? | <b> |\n")
LISTED = (HEAD + "**The paper's question**: <the whole question>?\n\n1. <first question>? ⬜\n2. <second question>? ⬜\n")


class RqAddressTest(unittest.TestCase):
    def tabs(self, text, root=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = root or Path(tmp)
            topic = root / "Paper-X" / "s02-story-x"
            topic.mkdir(parents=True, exist_ok=True)
            (topic / "s02-story-x.md").write_text(text, encoding="utf-8")
            tabs = board_story.story_tabs(topic.parent, topic, root, lambda body, where: f"<md>{body}</md>")
        return dict((name, panel) for name, _, panel in tabs)["Research Questions"]

    def test_keys_from_each_first_cell_style(self):
        self.assertEqual([board_read.rq_key(c) for c in ("H1", "H2 check", "RQ1", "RQ 3", "1 · how many", "2")],
                         ["H1", "H2-check", "RQ1", "RQ3", "RQ1", "RQ2"])

    def test_a_keyed_table_is_a_table_with_addressed_rows(self):
        panel = self.tabs(KEYED)
        self.assertIn("class=pb-rqtab", panel)                      # no longer the Markdown fallback
        self.assertNotIn("<md>", panel)
        for addr in ("RQ.H1", "RQ.H2", "RQ.H2-check", "RQ.Q"):
            self.assertIn(f'data-addr="{addr}"', panel)
        self.assertIn("<td class=k>H2 check</td>", panel)             # the key reads as written
        self.assertNotIn("Answer state", panel)                       # no State column (JL 261111)
        self.assertIn("Why the paper needs it", panel)

    def test_rq_and_numbered_keys(self):
        panel = self.tabs(NUMBERED)
        self.assertIn('data-addr="RQ.RQ1"', panel)
        self.assertIn('data-addr="RQ.RQ2"', panel)
        self.assertNotIn('data-addr="RQ.Q"', panel)                   # no paper's question written, none drawn

    def test_the_list_form_keeps_its_table_and_gains_addresses(self):
        panel = self.tabs(LISTED)
        self.assertIn('<tr data-addr="RQ.RQ1">', panel)
        self.assertIn('<tr data-addr="RQ.RQ2">', panel)
        self.assertIn('data-addr="RQ.Q"', panel)

    def test_each_row_has_its_marks_and_a_closed_card_row(self):
        panel = self.tabs(KEYED)
        self.assertIn('<span class="im-marks" data-addr="RQ.H2">', panel)       # the strip in the row's last cell
        self.assertIn('data-im-slot="RQ.H2-check" data-page="Paper-X/s02-story-x"', panel)
        self.assertIn('<td colspan="5">', panel)                                 # key + 3 columns (no state) + marks
        self.assertIn('data-im-slot="RQ.Q"', panel)                              # the paper's question has its cards
        self.assertNotIn("💬", panel)                                              # nothing written, no count drawn

    def test_a_comment_and_a_check_written_to_the_story_show_on_its_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.tabs(KEYED, root)                                                # the topic, in the temp folder only
            (root / "Paper-X" / "s02-story-x" / "draft" / "records").mkdir(parents=True)
            page = "Paper-X/s02-story-x"
            code, _ = item_card_route.item_card_act(root, {"page": page, "address": "RQ.H2", "act": "add", "text": "Define the order."})
            self.assertEqual(code, 200)
            code, _ = item_card_route.item_card_act(root, {"page": page, "address": "RQ.H1", "act": "check", "words": "<first question>?"})
            self.assertEqual(code, 200)
            records = root / page / "draft" / "records"
            self.assertIn("RQ.H2", (records / "s02-story-x-comments.md").read_text(encoding="utf-8"))
            self.assertIn("- RQ.H1 · ", (records / "s02-story-x-checked.md").read_text(encoding="utf-8"))
            panel = self.tabs(KEYED, root)
        self.assertRegex(panel, r'data-addr="RQ.H2">[^<]*<button[^>]*>💬 1</button>')
        self.assertRegex(panel, r'data-addr="RQ.H1">.*?title="checked">✓</button>')

    def test_venues_with_a_call_still_render_beside_the_rq_cards(self):
        # 261114 regression: the RQ cards' page path rebound story_tabs' rel() helper and the Venues tab failed
        # ("'str' object is not callable", the Story view gave an empty response)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            call = root / "Paper-X" / "venues" / "some-journal" / "call.md"
            call.parent.mkdir(parents=True)
            call.write_text("# call\n", encoding="utf-8")
            text = KEYED + "\n### Venues\n\n| venue | why it fits |\n|---|---|\n| Some Journal | <why> |\n"
            topic = root / "Paper-X" / "s02-story-x"
            topic.mkdir(parents=True)
            (topic / "s02-story-x.md").write_text(text, encoding="utf-8")
            tabs = dict((n, p) for n, _, p in board_story.story_tabs(topic.parent, topic, root, lambda b, w: b))
        self.assertIn("Venues", tabs)
        self.assertIn("Open call.md", tabs["Venues"])
        self.assertIn('data-addr="RQ.H1"', tabs["Research Questions"])


if __name__ == "__main__":
    unittest.main()
