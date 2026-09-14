"""Page-v2 Insight routing and derived Question Group invariants."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from cli.check import Report, check_insight_family


def write_page(board: Path, rel: str, text: str) -> Path:
    path = board / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def codes(board: Path) -> list[str]:
    report = Report()
    check_insight_family(board, report)
    return [code for _, code, _, _ in report.rows]


class InsightPageV2Test(unittest.TestCase):
    def test_folder_kind_wisdom_reaches_signature_check(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "4-W-wisdom/W01-counsel/W01-counsel.md",
                "# Counsel\nfolder-kind: wisdom\n\nSERVES QW1\nsigned: ⬜\n",
            )
            self.assertIn("wisdom-handoff-unsigned", codes(board))

    def test_current_phase_file_resolves_the_insight_folder_kind(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "4-W-wisdom/W01-counsel/W01-counsel.md",
                "# Counsel\n\nSERVES QW1\nsigned: ⬜\n",
            )
            write_page(
                board,
                "4-W-wisdom/W01-counsel/workflow/phase.yaml",
                "current:\n  phase: I5\n  folder-kind: wisdom\n",
            )
            self.assertIn("wisdom-handoff-unsigned", codes(board))

    def test_current_question_requires_target_rung(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "0-MT-meta/MT02-question-information/MT02-question-information.md",
                "# Information questions\nfolder-kind: question\n\nQI1   who is here?   ⬜\n",
            )
            self.assertIn("question-rung-missing", codes(board))

    def test_question_id_must_agree_with_dikw_axis(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "0-MT-meta/MT02-question-information/MT02-question-information.md",
                "# Information questions\nfolder-kind: question\n"
                "question-rung: information\n\nQW1   what should we do?   ⬜\n",
            )
            self.assertIn("question-rung-id-mismatch", codes(board))

    def test_question_group_is_derived_not_stored(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "0-MT-meta/MT02-question-information/MT02-question-information.md",
                "# Information questions\nfolder-kind: question\n"
                "question-rung: information\nquestion-group: QG-B-I\n\n"
                "QI1   who is here?   ⬜\n",
            )
            self.assertIn("question-group-stored", codes(board))

    def test_valid_current_question_is_clean(self):
        with TemporaryDirectory() as tmp:
            board = Path(tmp) / "Current-InsightBoard"
            write_page(
                board,
                "0-MT-meta/MT02-question-information/MT02-question-information.md",
                "# Information questions\nfolder-kind: question\n"
                "question-rung: information\n\nQI1   who is here?   ⬜\n",
            )
            self.assertEqual([], codes(board))


if __name__ == "__main__":
    unittest.main()
