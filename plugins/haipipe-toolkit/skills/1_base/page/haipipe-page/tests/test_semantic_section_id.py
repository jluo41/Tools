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

    def test_lettered_story_ids_parse_new_grammar_and_grandfathered(self):
        with TemporaryDirectory() as root:
            board = Path(root)
            story_dir = board / "STORY"
            story_dir.mkdir()
            page_ids = [
                "StoryA-misq-phytrait-discretion",   # 260908 grammar Story<Letter>-<desk>-<idea-slug>
                "StoryB-jama-phytrait-highdose",
                "Story-C",                           # grandfathered bare-letter form still parses
            ]
            (board / "board.md").write_text(
                "## Pages\n\n### STORY\n"
                + "\n".join(f"{page_id}.md" for page_id in page_ids)
                + "\n",
                encoding="utf-8",
            )
            for page_id in page_ids:
                page = story_dir / page_id
                page.mkdir()
                (page / f"{page_id}.md").write_text(
                    f"# {page_id} · Story\nstate: 🟡 PARTIAL\n",
                    encoding="utf-8",
                )
            _board, pages, warnings = parse_dir(board)

        self.assertEqual(warnings, [])
        self.assertEqual([item["id"] for item in pages], page_ids)
        self.assertTrue(all(item["kind"] == "stage" for item in pages))

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


    def test_indexed_section_ids_parse_and_sort_by_index(self):
        """260908 third naming pass: S-<desk>-Main-<N>-<Title>, S-<desk>-Appendix-<L>-<Title>; unnumbered keep title."""
        with TemporaryDirectory() as root:
            board = Path(root)
            ids = ["S-MISQ-Main-Abstract", "S-MISQ-Main-5-Results", "S-MISQ-Main-4-Empirical-Strategy",
                   "S-MISQ-Appendix-D-Instrumental-Variables", "S-JAMA-IM-Main-Key-Points"]
            (board / "board.md").write_text("## Pages\n\n### MAIN\n" + "\n".join(f"{i}.md" for i in ids) + "\n", encoding="utf-8")
            for i in ids:
                d = board / "Ba-X-Main" / i; d.mkdir(parents=True)
                (d / f"{i}.md").write_text(f"# {i} · Section\nstate: 🟡 PARTIAL\n", encoding="utf-8")
            _board, pages, warnings = parse_dir(board)
        self.assertEqual(warnings, [])
        self.assertEqual(sorted(p["id"] for p in pages), sorted(ids))
        self.assertTrue(all(p["kind"] == "stage" for p in pages))
        self.assertEqual(expand_ids("S-MISQ-Main-4-Empirical-Strategy + S-MISQ-Appendix-D-Instrumental-Variables"),
                         {"S-MISQ-Main-4-Empirical-Strategy", "S-MISQ-Appendix-D-Instrumental-Variables"})


    def test_checker_exempts_indexed_paper_sections_from_the_stage_contract(self):
        """check.py reads the one shared grammar, so S-<desk>-Main-<N>-<Title> is a paper section, not a stage page."""
        import importlib.util, sys as _sys
        cli = Path(__file__).resolve().parent.parent / "cli"
        _sys.path.insert(0, str(cli))
        spec = importlib.util.spec_from_file_location("check_under_test", cli / "check.py")
        mod = importlib.util.module_from_spec(spec); _sys.modules[spec.name] = mod; spec.loader.exec_module(mod)
        for ok in ("S-JAMA-IM-Main-1-Introduction.md", "S-MISQ-Appendix-D-Instrumental-Variables.md",
                   "S-MISQ-Main-Abstract.md", "S-JAMA-IM-Main-Key-Points.md"):
            self.assertIsNotNone(mod.SEMANTIC_SECTION_PAGE.fullmatch(ok), ok)
        for stage in ("S-Work-R1.md", "S03.md", "S-Main-Dash.md"):
            self.assertIsNone(mod.SEMANTIC_SECTION_PAGE.fullmatch(stage), stage)
