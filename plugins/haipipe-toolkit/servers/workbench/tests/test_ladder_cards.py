"""Ladder rows as cards (JL 261116): a Job, Task or Run row carries marks and cards, addressed from its Block."""
import tempfile
import unittest
from pathlib import Path

from live import item_cards as IC
from live import ladder_cards as LC
from live.item_card_route import item_card_act


class LadderCardsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.block = self.root / "b01_study"
        self.run = self.block / "j02_tables" / "t01_cut" / "runs" / "r05_first"
        self.run.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_row_is_addressed_from_its_block(self):
        task = self.run.parent.parent
        self.assertEqual(LC.address(task.parent, self.block), "j02")
        self.assertEqual(LC.address(task, self.block), "j02.t01")
        self.assertEqual(LC.address(self.run, self.block), "j02.t01.r05")
        self.assertEqual(LC.row_cards(self.root, self.root), ("", ""))       # off the ladder: nothing

    def test_a_comment_on_a_task_row_lands_in_the_blocks_records_and_shows(self):
        task = self.run.parent.parent
        strip, slot = LC.row_cards(task, self.root, "Cut")
        self.assertIn('data-addr="j02.t01"', strip)
        self.assertNotIn("🙋", strip)                                           # nothing waits: no 🙋
        code, res = item_card_act(self.root, {"page": "b01_study", "address": "j02.t01", "act": "add",
                                               "text": "Why only one cut?"})
        self.assertEqual(code, 200, res)
        self.assertTrue((self.block / "records" / "board-comments.md").is_file())
        self.assertIn("💬 1", LC.row_cards(task, self.root, "Cut")[0])
        self.assertEqual(list(IC.cards(self.block)), ["j02.t01"])

    def test_a_waiting_form_gives_the_row_its_question_card(self):
        run = self.run.parent / "r06_collect_cut"
        run.mkdir()
        (run / "run.yaml").write_text("run: r06_collect_cut\nkind: hard\ntype: collect\nstatus: waiting\n")
        (run / "question_collection.md").write_text("# Cut\n\n## Q1 · Cut\n\n**Which?**\n\n- [x] A · a\n- [ ] B · b\n")
        (run / "r06_collect_cut.html").write_text("<!doctype html>")
        strip, slot = LC.row_cards(self.run.parent.parent, self.root, "Cut")
        self.assertIn('data-im-open="j02.t01~ask">🙋 1<', strip)
        self.assertIn('data-ixq="Q1"', slot)
        self.assertNotIn(' src="', slot.split("pb-ixframe", 1)[1].split(">", 1)[0])   # loads when the card opens


if __name__ == "__main__":
    unittest.main()
