"""Studio › Sessions: episodes read where they are, joined to the folders they touched (ref/three-views.md)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

import os  # noqa: E402

from live import focus_studio, frame_folders, frame_sessions  # noqa: E402


class SessionsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / "env.sh").write_text("")
        self.block = self.root / "Project-X" / "paper" / "Paper-X"
        task = self.block / "j02_writing_v1115_jama" / "t02_methods"
        (task / "draft" / "records").mkdir(parents=True)
        (self.block / "board.md").write_text("# Paper X\n")
        (task / "draft" / "t02_methods-draft-v0.4.md").write_text("# Methods\n")
        (task / "draft" / "records" / "t02_methods-revise.md").write_text(
            "# Revise\n\n## Pass 1 · 261105 · v0.2 to v0.4\n\ntext\n\n## Pass · review round · 261116 0201\n")
        rel = (task / "draft" / "t02_methods-draft-v0.4.md").relative_to(self.root).as_posix()
        p = self.block / "runs" / "run-revise-t02" / "passes" / "p01-1117"
        p.mkdir(parents=True)
        (p / "pass.md").write_text(f"---\nsession: Paper-X-t02\ndate: 2026-11-17\ngoal: Tighten Methods\n"
                                   f"paths:\n  - {rel}\ncards:\n  - t02.C3.P5.s14\n---\n\n# Tighten Methods\n")
        s = self.block / "s02-story" / "passes" / "p01-1110"
        s.mkdir(parents=True)
        (s / "digest.md").write_text("# Story round\n")
        (s / "transcript.md").write_text("# raw chat\n")
        self.task, self.rel = task, rel

    def tearDown(self):
        self.tmp.cleanup()

    def test_every_kind_of_record_is_an_episode_newest_first(self):
        eps = frame_sessions.episodes(self.block)
        self.assertEqual([e["goal"] for e in eps],
                         ["Tighten Methods", "Pass · review round", "Story round", "Pass 1 · v0.2 to v0.4"])
        self.assertEqual(eps[0]["day"], "2026-11-17")
        self.assertEqual(eps[0]["cards"], ["t02.C3.P5.s14"])
        self.assertEqual(eps[2]["record"].name, "digest.md")       # never the transcript

    def test_touched_folders_and_their_parents_carry_the_thread(self):
        marked = frame_sessions.touched_set(self.block)
        self.assertIn((self.root / self.rel).resolve(), marked)
        self.assertIn(self.task.resolve(), marked)
        rows = frame_folders.folder_rows(self.block, self.root)
        self.assertIn("🧵", rows)
        self.assertIn('data-th="Project-X/paper/Paper-X/j02_writing_v1115_jama"', rows)

    def test_the_part_groups_by_folder_and_shows_no_count(self):
        html = frame_sessions.sessions_part(self.block, self.root)
        self.assertIn("id=studio-sessions", html)
        self.assertIn("<h4 class=ss-where>t02_methods/</h4>", html.replace("j02_writing_v1115_jama/", ""))
        self.assertNotIn("transcript.md", html)
        self.assertNotRegex(html.split("<style>")[0], r"\d+ (episodes|sessions|passes)")

    def test_a_block_without_episodes_shows_no_part(self):
        empty = self.root / "Project-X" / "paper" / "Paper-Y"
        empty.mkdir(parents=True)
        self.assertEqual(frame_sessions.sessions_part(empty, self.root), "")

    def test_a_server_config_marks_the_space_root_too(self):
        (self.root / "env.sh").unlink()
        (self.root / ".server_config").write_text("")
        self.assertEqual(frame_sessions.space_of(self.block), self.root)
        self.assertIn((self.root / self.rel).resolve(), frame_sessions.touched_set(self.block))

    def test_a_digest_edited_in_place_is_read_again(self):
        digest = self.block / "s02-story" / "passes" / "p01-1110" / "digest.md"
        frame_sessions.episodes(self.block)
        digest.write_text("# Story round, rewritten\n")
        st = digest.stat()
        os.utime(digest, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))
        self.assertIn("Story round, rewritten", [e["goal"] for e in frame_sessions.episodes(self.block)])
        self.assertEqual(sum(1 for k in frame_sessions._PARSED if k == str(digest)), 1)

    def test_a_task_page_shows_only_its_own_episodes(self):
        html = frame_sessions.sessions_part(self.block, self.root, under=self.task)
        self.assertIn("Tighten Methods", html)
        self.assertNotIn("Story round", html)

    def test_a_block_chat_is_an_episode_grouped_at_its_block(self):
        chat = self.block / "c01_tighten_methods"
        chat.mkdir()
        (chat / "c01_tighten_methods.md").write_text(
            f"---\nsession: Paper-X\ndate: 2026-11-21\ngoal: Talk through Methods\npaths:\n  - {self.rel}\n---\n\n"
            "# c01 · Talk through Methods\n")
        (chat / "transcript.md").write_text("# raw\n")
        eps = frame_sessions.episodes(self.block)
        self.assertEqual(eps[0]["goal"], "Talk through Methods")
        self.assertEqual(eps[0]["record"].name, "c01_tighten_methods.md")
        html = frame_sessions.sessions_part(self.block, self.root)
        self.assertIn("<h4 class=ss-where>Paper-X/</h4>", html)
        self.assertNotIn("transcript.md", html)
        self.assertIn("Talk through Methods", frame_sessions.sessions_part(self.block, self.root, under=self.task))

    def test_the_focus_files_section_carries_the_thread_and_sessions(self):
        html = focus_studio.files_html(self.block, self.root)
        self.assertIn('class=fd-th data-th="Project-X/paper/Paper-X/j02_writing_v1115_jama"', html)
        self.assertIn("id=studio-sessions", html)


if __name__ == "__main__":
    unittest.main()
