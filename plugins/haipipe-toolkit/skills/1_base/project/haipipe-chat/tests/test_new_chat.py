"""haipipe-chat: a Block's chat sessions are cNN_<slug>/ folders, numbered in time order."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import new_chat  # noqa: E402


class NewChatTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / "env.sh").write_text("")
        self.block = self.root / "Project-X" / "work" / "b01_demo"
        (self.block / "j01_build").mkdir(parents=True)
        (self.block / "board.md").write_text("# b01 · Demo\n")
        (self.block / "j01_build" / "j01_build.md").write_text("# j01 · Build\n")

    def tearDown(self):
        self.tmp.cleanup()

    def new(self, slug, *extra):
        return new_chat.main(["new", str(self.block), "--slug", slug, "--title", slug.replace("_", " "), *extra])

    def test_numbers_follow_time_and_paths_are_space_relative(self):
        self.new("first_talk", "--changed", str(self.block / "j01_build" / "j01_build.md"), "--date", "2026-11-20")
        self.new("second_talk")
        names = [p.name for p in new_chat.chats(self.block)]
        self.assertEqual(names, ["c01_first_talk", "c02_second_talk"])
        meta, body = new_chat.read_face(self.block / "c01_first_talk")
        self.assertEqual(meta["paths"], ["Project-X/work/b01_demo/j01_build/j01_build.md"])
        self.assertEqual(meta["date"], "2026-11-20")
        self.assertIn("# c01 · first talk", body)
        self.assertEqual(new_chat.problems(self.block), [])

    def test_without_a_space_root_paths_are_block_relative(self):
        (self.root / "env.sh").unlink()
        (self.root / "PRINCIPLE.md").write_text("x")
        self.new("talk", "--changed", str(self.root / "PRINCIPLE.md"))
        meta, _ = new_chat.read_face(self.block / "c01_talk")
        self.assertEqual(meta["paths"], ["../../../PRINCIPLE.md"])
        self.assertEqual(new_chat.problems(self.block), [])

    def test_check_finds_a_missing_path(self):
        self.new("talk", "--changed", "Project-X/gone.md")
        self.assertEqual(new_chat.problems(self.block), ["c01_talk: Project-X/gone.md is not on disk"])

    def test_transcript_keeps_words_not_tools(self):
        jl = self.root / "s.jsonl"
        jl.write_text("\n".join(json.dumps(r) for r in [
            {"type": "user", "message": {"content": "add cNN"}},
            {"type": "assistant", "message": {"content": [{"type": "text", "text": "done"},
                                                           {"type": "tool_use", "name": "Bash"}]}}]))
        self.new("talk", "--transcript", str(jl))
        text = (self.block / "c01_talk" / "transcript.md").read_text()
        self.assertIn("add cNN", text)
        self.assertIn("done", text)
        self.assertNotIn("Bash", text)

    def test_refuses_a_folder_that_is_not_a_block(self):
        with self.assertRaises(SystemExit):
            new_chat.main(["new", str(self.block / "j01_build"), "--slug", "x", "--title", "x"])


if __name__ == "__main__":
    unittest.main()
