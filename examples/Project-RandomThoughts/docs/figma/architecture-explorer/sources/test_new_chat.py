"""hai-chat: a Block's chat sessions are cNN_<slug>/ folders, numbered in time order."""
import io
import json
import os
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
        self.reg = self.root / "kept.json"
        os.environ["HAIPIPE_CHAT_REGISTRY"] = str(self.reg)

    def tearDown(self):
        os.environ.pop("HAIPIPE_CHAT_REGISTRY", None)
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

    def session(self):
        jl = self.root / "s.jsonl"
        out = self.block / "j01_build" / "j01_build.md"
        rows = [
            {"type": "user", "timestamp": "2026-11-21T01:00:00Z", "message": {"content": "add <pasted_content id=x>cNN</pasted_content>"}},
            {"type": "user", "message": {"content": "<system-reminder>context</system-reminder>"}},
            {"type": "assistant", "message": {"content": [{"type": "thinking", "thinking": "hmm"},
                                                          {"type": "tool_use", "name": "Bash", "input": {"command": "ls"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "content": "files"}]}},
            {"type": "attachment", "attachment": {"type": "queued_command", "prompt": "and the face?",
                                                  "origin": {"kind": "human"}, "timestamp": "2026-11-21T01:05:00Z"}},
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Edit", "input": {"file_path": str(out)}},
                                                          {"type": "text", "text": "Done: the face is written.\n\n## 1. More"}]}},
        ]
        jl.write_text("\n".join(json.dumps(r) for r in rows))
        return jl

    def test_a_chat_is_its_questions_answers_and_outputs(self):
        self.new("talk", "--from", str(self.session()))
        meta, body = new_chat.read_face(self.block / "c01_talk")
        self.assertRegex(body, r"- \*\*q01\*\* \d\d:\d\d · add cNN and the face\?")   # sent mid-turn: the same QA
        self.assertNotIn("q02", body)
        self.assertIn("  → Done: the face is written.", body)
        self.assertIn("  ⇢ `j01_build.md`", body)
        self.assertEqual(meta["paths"], ["Project-X/work/b01_demo/j01_build/j01_build.md"])
        self.assertLessEqual(len(body.split("## QA")[1].strip().splitlines()), 3)
        for left_out in ("context", "hmm", "Bash", "files", "## 1. More", "pasted_content"):
            self.assertNotIn(left_out, body)
        self.assertFalse((self.block / "c01_talk" / "transcript.md").exists())

    def test_refresh_keeps_number_title_and_date(self):
        self.new("talk", "--ask", "first?", "--answer", "yes", "--date", "2026-11-20", "--summary", "kept")
        new_chat.main(["refresh", str(self.block / "c01_talk"), "--from", str(self.session())])
        meta, body = new_chat.read_face(self.block / "c01_talk")
        self.assertEqual((meta["date"], meta["goal"]), ("2026-11-20", "talk"))
        self.assertIn("and the face?", body)
        self.assertIn("kept", body)
        self.assertNotIn("first?", body)
        self.assertEqual([p.name for p in new_chat.chats(self.block)], ["c01_talk"])

    def test_the_stop_hook_refreshes_only_a_kept_session(self):
        import chat_hook
        jl = self.session()
        self.new("talk", "--from", str(jl))
        face = self.block / "c01_talk" / "c01_talk.md"
        face.write_text(face.read_text().replace("and the face?", "OLD"))
        for sid, expect in (("other", "OLD"), (jl.stem, "and the face?")):
            sys.stdin = io.StringIO(json.dumps({"session_id": sid, "transcript_path": str(jl)}))
            self.assertEqual(chat_hook.main(), 0)
            self.assertIn(expect, face.read_text())
        sys.stdin = sys.__stdin__

    def test_refuses_a_folder_that_is_not_a_block(self):
        with self.assertRaises(SystemExit):
            new_chat.main(["new", str(self.block / "j01_build"), "--slug", "x", "--title", "x"])


if __name__ == "__main__":
    unittest.main()
