"""Studio Chat kept-session records (QPf4 §1, JL 260815).

transcript_markdown is pure so the record's shape is pinned without a server:
the same rows the drawer replays are the rows the record writes, and this file
is what notices if the two ever drift.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from live.chat import (ChatMixin, digest_markdown, kept_session_dir,
                       transcript_markdown)  # noqa: E402

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

    def test_digest_is_a_short_reading_path_over_the_same_rows(self):
        md = digest_markdown(ROWS, HEAD)
        self.assertIn("## Ask", md)
        self.assertIn("what pages relate to chat?", md)
        self.assertIn("## Outcome", md)
        self.assertIn("Seven pages, five in QO.", md)
        self.assertIn("Tools observed: Read.", md)
        self.assertIn("[transcript.md](transcript.md)", md)

    def test_kept_folder_uses_timestamp_and_reuses_the_recorded_session(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            chat = Path(tmp) / "studio" / "chat"
            first = kept_session_dir(chat, "260815-1402", HEAD["id"])
            self.assertEqual(first.name, "260815-1402")
            first.mkdir(parents=True)
            (first / "digest.md").write_text(
                "session: %s\n" % HEAD["id"], encoding="utf-8")
            self.assertEqual(
                kept_session_dir(chat, "260815-1402", HEAD["id"]), first
            )
            collided = kept_session_dir(chat, "260815-1402", "other-session")
            self.assertEqual(collided.name, "260815-1402-02")

    def test_keep_writer_lands_both_records_in_canonical_studio_chat(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            page_home = Path(tmp) / "S-Test"
            page_home.mkdir()
            page = page_home / "S-Test.md"
            page.write_text("# Test\n", encoding="utf-8")

            class Fake:
                def sessions_list(self, _f, _p):
                    return {"sessions": [{"id": HEAD["id"], "name": "kept",
                                           "landed": True}]}, None

                def _session_rows(self, _sid):
                    return ROWS, None

                def _jsonl_path(self, sid):
                    return Path(tmp) / (sid + ".jsonl")

            result = ChatMixin.keep_sessions(Fake(), page, {})

            self.assertTrue(result["ok"])
            kept = page_home / "studio" / "chat" / "260815-1402"
            self.assertTrue((kept / "digest.md").is_file())
            self.assertTrue((kept / "transcript.md").is_file())
            self.assertFalse((page_home / "chat").exists())


if __name__ == "__main__":
    unittest.main()
