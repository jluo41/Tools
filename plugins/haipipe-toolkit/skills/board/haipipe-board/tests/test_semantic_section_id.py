"""Paper Section IDs are semantic and remain usable by the Board parser."""
import unittest
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src.feedback import expand_ids
from src.parse import parse_dir


class TestSemanticSectionId(unittest.TestCase):
    def test_named_main_and_appendix_pages_parse_with_full_ids(self):
        with TemporaryDirectory() as root:
            board = Path(root)
            main = board / "Ba-MISQ-Main" / "S-MISQ-Main-Abstract"
            appendix = board / "Bb-MISQ-Appendix" / "S-MISQ-Appendix-Validation"
            main.mkdir(parents=True)
            appendix.mkdir(parents=True)
            (board / "board.md").write_text(
                "## Pages\n\n### MAIN\nS-MISQ-Main-Abstract.md\n\n"
                "### APPENDIX\nS-MISQ-Appendix-Validation.md\n",
                encoding="utf-8",
            )
            (main / "S-MISQ-Main-Abstract.md").write_text(
                "# S-MISQ-Main-Abstract · Abstract\nstate: 🟡 PARTIAL\n",
                encoding="utf-8",
            )
            (appendix / "S-MISQ-Appendix-Validation.md").write_text(
                "# S-MISQ-Appendix-Validation · Validation\nstate: 🟡 PARTIAL\n",
                encoding="utf-8",
            )
            _board, pages, warnings = parse_dir(board)

        self.assertEqual(warnings, [])
        self.assertEqual(
            [page["id"] for page in pages],
            ["S-MISQ-Main-Abstract", "S-MISQ-Appendix-Validation"],
        )

    def test_hyphenated_desk_name_parses_as_one_semantic_id(self):
        with TemporaryDirectory() as root:
            board = Path(root)
            page_id = "S-JAMA-IM-Main-Abstract"
            page = board / "Ba-JAMA-IM-Main" / page_id
            page.mkdir(parents=True)
            (board / "board.md").write_text(
                f"## Pages\n\n### MAIN\n{page_id}.md\n",
                encoding="utf-8",
            )
            (page / f"{page_id}.md").write_text(
                f"# {page_id} · Abstract\nstate: 🟡 PARTIAL\n",
                encoding="utf-8",
            )
            _board, pages, warnings = parse_dir(board)

        self.assertEqual(warnings, [])
        self.assertEqual([item["id"] for item in pages], [page_id])

    def test_feedback_router_reads_named_section_ids(self):
        ids = expand_ids(
            "S-MISQ-Main-Results + S-MISQ-Appendix-Validation + "
            "S-JAMA-IM-Main-Abstract"
        )
        self.assertEqual(
            ids,
            {
                "S-MISQ-Main-Results",
                "S-MISQ-Appendix-Validation",
                "S-JAMA-IM-Main-Abstract",
            },
        )


if __name__ == "__main__":
    unittest.main()
