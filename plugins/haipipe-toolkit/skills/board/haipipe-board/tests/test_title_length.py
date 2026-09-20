#!/usr/bin/env python3
"""Executable contract for short, purpose-bearing Page titles."""
import unittest

from cli.check import (Report, check_board_names, check_division_names,
                   check_page_title, reader_title_words)


class PageTitleLengthTest(unittest.TestCase):
    def findings(self, title):
        rep = Report()
        check_page_title(f"# {title}\n", "QA1-title.md", rep)
        return [row for row in rep.rows if row[1] == "page-title-long"]

    def test_six_reader_words_pass(self):
        self.assertEqual(
            reader_title_words("Page · one grammar for every page"),
            ["Page", "one", "grammar", "for", "every", "page"])
        self.assertEqual(self.findings("Page · one grammar for every page"), [])

    def test_eight_reader_words_pass(self):
        self.assertEqual(
            self.findings("One grammar every Board page must obey today"), [])

    def test_nine_reader_words_warn(self):
        findings = self.findings("One grammar every Board page must obey from today")
        self.assertEqual(len(findings), 1)
        self.assertIn("9 reader-facing words", findings[0][3])

    def test_colon_does_not_reset_the_count(self):
        findings = self.findings(
            "The write path: one browser edit always writes Markdown source")
        self.assertEqual(len(findings), 1)

    def test_machine_identity_and_derived_metadata_do_not_count(self):
        self.assertEqual(
            reader_title_words("S Main 7 · §6 Results for clinicians"),
            ["Results", "for", "clinicians"])
        self.assertEqual(
            reader_title_words(
                "Design-3 · One grammar for pages (Skill haipipe-page v0.39.0)"),
            ["One", "grammar", "for", "pages"])

    def test_hyphenated_word_counts_once(self):
        self.assertEqual(
            reader_title_words("Cross-event normalization improves CGM prediction"),
            ["Cross-event", "normalization", "improves", "CGM", "prediction"])

    def test_board_group_and_division_names_share_the_ceiling(self):
        rep = Report()
        check_board_names(
            "# Nine words make this Board title much too hard to scan\n"
            "## Pages\n"
            "### QA · Nine words make this Question Group title hard to scan\n",
            rep)
        check_division_names(
            "## Content\n"
            "### 1 · Nine words make this division title much too hard to scan\n",
            "QA1-title.md", rep)
        self.assertEqual(
            {row[1] for row in rep.rows},
            {"board-title-long", "question-group-title-long", "division-name-long"})

    def test_model_like_title_is_reported(self):
        rep = Report()
        check_page_title("# A comprehensive guide to Board names\n",
                         "QA1-title.md", rep)
        self.assertIn("name-ai-flavor", {row[1] for row in rep.rows})


if __name__ == "__main__":
    unittest.main()
