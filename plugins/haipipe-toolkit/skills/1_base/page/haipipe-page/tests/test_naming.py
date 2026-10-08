import tempfile
import unittest
from pathlib import Path

from live.chat import ChatMixin
from live.structure import structure_op
from src.naming import compact_name, name_problem, name_words


class NamingLawTest(unittest.TestCase):
    def test_english_words_and_chinese_characters_are_counted(self):
        self.assertEqual(len(name_words("Short Board names stay clear")), 5)
        self.assertEqual(len(name_words("会话分区名称")), 6)

    def test_authored_names_are_rewritten_not_truncated(self):
        problem = name_problem(
            "Nine reader facing words make this name too hard to scan")
        self.assertIn("never more than 8", problem)

    def test_automatic_session_fallback_stops_on_a_word(self):
        self.assertEqual(
            compact_name("one two three four five six seven eight nine ten"),
            "one two three four five six seven eight")

    def test_structure_writer_rejects_long_and_model_like_names(self):
        with tempfile.TemporaryDirectory() as td:
            board = Path(td)
            (board / "board.md").write_text(
                "# Test Board\n## Pages\n### QA · Test group\n",
                encoding="utf-8")
            _, error = structure_op(board, {
                "op": "add_question", "group": "QA",
                "title": "Nine reader facing words make this Page title hard to scan",
            })
            self.assertIn("never more than 8", error)
            _, error = structure_op(board, {
                "op": "add_group", "title": "A comprehensive workflow",
                "letter": "B",
            })
            self.assertIn("model-like", error)

    def test_session_writer_rejects_long_names(self):
        with tempfile.TemporaryDirectory() as td:
            chat = ChatMixin()
            chat.root = Path(td)
            _, error = chat.name_session(Path(td) / "page.md", {
                "id": "session-id",
                "name": "Nine reader facing words make this session name hard to scan",
            })
            self.assertIn("never more than 8", error)


if __name__ == "__main__":
    unittest.main()
