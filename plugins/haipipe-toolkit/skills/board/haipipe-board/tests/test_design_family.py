"""Clean-break gates for the current DesignBoard grammar."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.check import Report, check_design_family


def build(root: Path) -> Path:
    board = root / "Current-DesignBoard"
    folder = board / "2-Design" / "Design-01-patient-confirm-sms"
    folder.mkdir(parents=True)
    (board / "board.md").write_text("# Current DesignBoard\n", encoding="utf-8")
    (folder / "Design-01-patient-confirm-sms.md").write_text(
        "# Current Design\n\nfolder-kind: design\n", encoding="utf-8"
    )
    return board


def findings(board: Path):
    report = Report()
    check_design_family(board, report)
    return report.rows


class DesignFamilyTest(unittest.TestCase):
    def test_current_empty_design_folder_has_no_design_findings(self):
        with TemporaryDirectory() as td:
            self.assertEqual(findings(build(Path(td))), [])

    def test_d0_d5_thread_shape_is_rejected(self):
        with TemporaryDirectory() as td:
            board = build(Path(td))
            old = (
                board / "2-Design" / "Design-01-patient-confirm-sms"
                / "design" / "DU01-old"
            )
            old.mkdir(parents=True)
            rows = findings(board)
            self.assertIn("retired-design-shape", {row[1] for row in rows})

    def test_pagex_is_rejected(self):
        with TemporaryDirectory() as td:
            board = build(Path(td))
            old = (
                board / "2-Design" / "Design-01-patient-confirm-sms"
                / "outline" / "evidence" / "pagex"
            )
            old.mkdir(parents=True)
            rows = findings(board)
            self.assertIn("retired-design-shape", {row[1] for row in rows})

    def test_rnn_design_ticket_is_rejected(self):
        with TemporaryDirectory() as td:
            board = build(Path(td))
            runs = board / "2-Design" / "Design-01-patient-confirm-sms" / "runs"
            runs.mkdir()
            (runs / "r01_design_generate_sms.yaml").write_text(
                "schema: haipipe.design-ticket/v1\n", encoding="utf-8"
            )
            rows = findings(board)
            self.assertIn("design-run-contract", {row[1] for row in rows})


if __name__ == "__main__":
    unittest.main()
