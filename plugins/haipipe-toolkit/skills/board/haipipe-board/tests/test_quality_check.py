#!/usr/bin/env python3
"""Executable safety checks for the one-click, read-only Quality Check."""
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))

from live.chat import QUALITY_READONLY, chat_scope, quality_tool_allowed  # noqa: E402


class QualityCheckContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chat_dir = HERE / "assets/js/10-drawer/20-chat"
        cls.client = "\n".join(
            f.read_text(encoding="utf-8") for f in sorted(chat_dir.glob("*.js"))
        )
        cls.server = (HERE / "live/chat.py").read_text(encoding="utf-8")

    def test_client_sends_a_dedicated_scoped_quality_check(self):
        self.assertIn("✅ Quality Check", self.client)
        self.assertIn("✨ Quick actions", self.client)
        self.assertIn("⚙ Settings", self.client)
        self.assertIn("qualityCheck: true", self.client)
        self.assertIn("scope: 'scoped'", self.client)
        self.assertIn("quality_check: !!(opts && opts.qualityCheck)", self.client)

    def test_quick_actions_use_canonical_aim_state_language(self):
        self.assertIn("open Aim States", self.client)
        self.assertIn("which Aims on this page have", self.client)
        self.assertNotIn("## Done when are still unchecked", self.client)

    def test_page_quality_check_uses_section_evaluation_contract(self):
        self.assertIn("haipipe-board-page/SKILL.md", self.client)
        self.assertIn("Resolve requirements in order", self.client)
        self.assertIn("every direct ### Content division", self.client)
        self.assertIn("applicable requirements + source", self.client)
        self.assertIn("MEETS, NEEDS WORK, N/A, or NOT VERIFIABLE", self.client)
        self.assertIn("Every MEETS needs visible evidence", self.client)

    def test_quality_check_forces_scoped_even_from_bypass(self):
        self.assertEqual(chat_scope({"quality_check": True, "scope": "bypass"}), "scoped")
        self.assertEqual(chat_scope({"quality_check": True, "scope": "full"}), "scoped")
        self.assertEqual(chat_scope({"scope": "bypass"}), "bypass")
        # A browser that names no tier gets Full · no ask (JL 260802). The old
        # default was `full`, which prompts per tool call; this test asserted
        # that older default until 260803. The ESCALATION GUARD above is what
        # this test exists for and it is unchanged: quality_check forces
        # `scoped` no matter what the client asks for.
        self.assertEqual(chat_scope({}), "bypass")

    def test_quality_check_tool_allowlist_is_evidence_only(self):
        self.assertEqual(QUALITY_READONLY, {"Read", "Glob", "Grep", "NotebookRead"})
        for name in QUALITY_READONLY:
            self.assertTrue(quality_tool_allowed(name), name)
        for name in ("Bash", "Edit", "Write", "MultiEdit", "TodoWrite", "WebFetch"):
            self.assertFalse(quality_tool_allowed(name), name)

    def test_server_applies_the_executable_safety_helpers(self):
        self.assertIn("mode = chat_scope(p)", self.server)
        self.assertIn("not quality_tool_allowed(name)", self.server)
        self.assertIn('SCOPED_OFF += ["Edit", "Write", "MultiEdit", "TodoWrite"]', self.server)


if __name__ == "__main__":
    unittest.main()
