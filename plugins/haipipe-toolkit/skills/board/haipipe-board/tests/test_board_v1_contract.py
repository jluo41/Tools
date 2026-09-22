"""Standing boundaries for the public Board V1 family."""

import re
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve()
BOARD_SKILL = HERE.parents[1]
BOARD_FAMILY = HERE.parents[2]
SKILLS = HERE.parents[3]


class BoardV1ContractTest(unittest.TestCase):
    def test_public_door_is_v1_and_release_is_recorded(self):
        skill = (BOARD_SKILL / "SKILL.md").read_text(encoding="utf-8")
        changelog = (BOARD_SKILL / "CHANGELOG.md").read_text(encoding="utf-8")
        match = re.search(r'(?m)^  version: "([^"]+)"$', skill)
        self.assertIsNotNone(match)
        version = match.group(1)
        self.assertEqual(version.split(".", 1)[0], "1")
        self.assertRegex(changelog, rf"\A## {re.escape(version)} · \d{{4}}-\d{{2}}-\d{{2}}\n")

    def test_page_family_has_one_canonical_home_and_no_board_alias(self):
        canonical = SKILLS / "page"
        for name in (
            "haipipe-page",
            "haipipe-workbench",
            "haipipe-workbench-page",
            "haipipe-workbench-studio",
            "haipipe-sentence",
            "haipipe-page-workflow",
            "workflow-runs",
        ):
            self.assertTrue((canonical / name).is_dir(), name)
            self.assertFalse((BOARD_FAMILY / name).exists(), f"board/{name} alias is retired")
        self.assertEqual(sorted(p.name for p in BOARD_FAMILY.iterdir() if p.is_symlink()), [])

    def test_active_board_docs_link_directly_to_canonical_page_contracts(self):
        links = {
            BOARD_FAMILY / "haipipe-folder" / "SKILL.md": (
                "../../page/haipipe-page/SKILL.md",
                "../../page/haipipe-workbench/SKILL.md",
            ),
            BOARD_FAMILY / "agents" / "haipipe-page-auditor-agent.md": (
                "../../page/haipipe-page/SKILL.md",
                "../../page/haipipe-page-workflow/ref/page-run-contract.md",
            ),
            BOARD_FAMILY / "agents" / "haipipe-page-creator-agent.md": (
                "../../page/haipipe-page/SKILL.md",
                "../../page/haipipe-sentence/SKILL.md",
            ),
            BOARD_FAMILY / "agents" / "haipipe-board-reviewer-agent.md": (
                "../../page/haipipe-page/SKILL.md",
                "../../page/workflow-runs/haipipe-page-check/SKILL.md",
            ),
        }
        for source, targets in links.items():
            text = source.read_text(encoding="utf-8")
            for target in targets:
                self.assertIn(target, text, str(source))
                self.assertTrue((source.parent / target).exists(), target)

    def test_run_names_and_current_write_surfaces_do_not_blur(self):
        board = (BOARD_SKILL / "SKILL.md").read_text(encoding="utf-8")
        routing = (
            BOARD_FAMILY / "haipipe-board-routing" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized_board = " ".join(board.split())
        for term in ("Page Run", "Task Run", "Page workflow pass"):
            self.assertIn(term, normalized_board)
        self.assertIn("rp00_mermaid-structure", normalized_board)
        self.assertIn("rpNN_pNN[-pNN]", normalized_board)
        self.assertNotIn("prNN", normalized_board)
        self.assertIn("outline/<stem>-discussion.md", routing)
        self.assertIn("Aims › Decision Now", routing)
        self.assertNotIn("inside `## States`", routing)
        self.assertNotIn("a Log line · a State entry", routing)

    def test_generic_board_examples_use_the_q_group_identity_grammar(self):
        sources = (
            BOARD_SKILL / "SKILL.md",
            BOARD_SKILL / "ref" / "board-form.md",
            BOARD_SKILL / "ref" / "board-example.md",
        )
        for source in sources:
            text = source.read_text(encoding="utf-8")
            self.assertIn("### QA ·", text, str(source))
            self.assertIn("QA1", text, str(source))
            self.assertNotIn("### G1 ·", text, str(source))

    def test_template_gate_distinguishes_diagrams_from_folded_code(self):
        from cli.check import CONSTRUCTS

        patterns = {label: source_pattern for label, _, _, source_pattern in CONSTRUCTS}
        self.assertRegex("```text", re.compile(patterns["ASCII diagram"], re.M))
        self.assertNotRegex("```text", re.compile(patterns["code block"], re.M))
        self.assertRegex("```python", re.compile(patterns["code block"], re.M))

    def test_folder_contract_gate_validates_the_remaining_phase_owner(self):
        result = subprocess.run(
            [
                sys.executable,
                str(BOARD_SKILL / "cli" / "foldercontracts.py"),
                "--check",
                "--workflow",
                "haipipe-insight-workflow",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 phase contracts · 0 findings", result.stdout)


if __name__ == "__main__":
    unittest.main()
