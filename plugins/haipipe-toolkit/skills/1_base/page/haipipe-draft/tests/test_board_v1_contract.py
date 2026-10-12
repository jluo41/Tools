"""Standing checks the Board checker and the Folder-contract gate keep (the Board skill is retired, JL 261005)."""

import re
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve()
BOARD_SKILL = HERE.parents[1]                    # the Page engine, home of cli/foldercontracts.py


class BoardV1ContractTest(unittest.TestCase):
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
        self.assertIn("6 Folder contracts · 0 findings", result.stdout)


if __name__ == "__main__":
    unittest.main()
