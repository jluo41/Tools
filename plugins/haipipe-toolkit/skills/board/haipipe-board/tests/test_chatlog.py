"""The chat/ plugin's transcript formatter (QPf4 §1, JL 260815).

transcript_markdown is pure so the record's shape is pinned without a server:
the same rows the drawer replays are the rows the record writes, and this file
is what notices if the two ever drift.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.chat import transcript_markdown  # noqa: E402

ROWS = [
    {"k": "you", "t": "what pages relate to chat?", "ts": "2026-08-15T14:02:11Z"},
    {"k": "tool", "name": "Read", "t": "QPf4-chat.md", "ts": "2026-08-15T14:02:14Z"},
    {"k": "ai", "t": "Seven pages, five in QO.", "ts": "2026-08-15T14:02:20Z"},
]
HEAD = {"id": "2a45769d-85f8-4704-a30f-17adb2c82776", "name": "QPf4-chat-history",
        "kept": "260815 1710", "source": "~/.claude/projects/x/2a45769d.jsonl"}


class TranscriptMarkdown(unittest.TestCase):
    def setUp(self):
        self.md = transcript_markdown(ROWS, HEAD)

    def test_head_names_the_session_and_its_source(self):
        self.assertIn("# 💬 QPf4-chat-history", self.md)
        self.assertIn("session: 2a45769d", self.md)
        self.assertIn("kept: 260815 1710", self.md)

    def test_every_row_kind_lands(self):
        self.assertIn("**You** · 14:02", self.md)
        self.assertIn("what pages relate to chat?", self.md)
        self.assertIn("> 🔧 Read · QPf4-chat.md", self.md)
        self.assertIn("**Claude** · 14:02", self.md)

    def test_falls_back_to_title_then_id(self):
        md = transcript_markdown([], {"id": "abcd1234-rest", "title": "a title"})
        self.assertIn("# 💬 a title", md)
        md = transcript_markdown([], {"id": "abcd1234-rest"})
        self.assertIn("# 💬 abcd1234", md)


if __name__ == "__main__":
    unittest.main()
