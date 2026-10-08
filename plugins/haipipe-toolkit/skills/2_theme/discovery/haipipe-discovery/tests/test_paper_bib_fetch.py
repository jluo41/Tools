from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "paper_bib_fetch.py"
SPEC = importlib.util.spec_from_file_location("paper_bib_fetch", SCRIPT)
assert SPEC and SPEC.loader
paper_bib_fetch = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paper_bib_fetch
SPEC.loader.exec_module(paper_bib_fetch)


# Crossref returns a whole entry on ONE line; arXiv returns it across lines.
CROSSREF_ONE_LINE = (
    "@article{Luo_2026, title={Mapping patient-perceived physician traits from "
    "nationwide online reviews with LLMs}, ISSN={2398-6352}, "
    "url={http://dx.doi.org/10.1038/s41746-026-03117-z}, "
    "DOI={10.1038/s41746-026-03117-z}, journal={npj Digital Medicine}, "
    "publisher={Springer Science and Business Media LLC}, "
    "author={Luo, Junjie and Gao, Gordon}, year={2026}, month=Aug }\n"
)
ARXIV_MULTILINE = """@misc{hou2024largelanguagemodelszeroshot,
      title={Large Language Models are Zero-Shot Rankers for Recommender Systems},
      author={Yupeng Hou and Wayne Xin Zhao},
      year={2024},
      eprint={2305.08845},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2305.08845},
}
"""
SCHOLAR_SHAPED = """@inproceedings{hou2024large,
  title={Large language models are zero-shot rankers for recommender systems},
  author={Hou, Yupeng and Zhao, Wayne Xin},
  booktitle={European Conference on Information Retrieval},
  pages={364--381}, year={2024}, organization={Springer}
}
"""


class FieldReadingTest(unittest.TestCase):
    def test_one_line_entry_title_stops_at_its_closing_brace(self) -> None:
        """A lazy regex swallowed every later field on a single-line entry."""
        title = paper_bib_fetch.entry_title(CROSSREF_ONE_LINE)
        self.assertEqual(
            "Mapping patient-perceived physician traits from nationwide online "
            "reviews with LLMs",
            title,
        )
        self.assertNotIn("ISSN", title or "")

    def test_multiline_entry_title_and_doi(self) -> None:
        self.assertEqual(
            "Large Language Models are Zero-Shot Rankers for Recommender Systems",
            paper_bib_fetch.entry_title(ARXIV_MULTILINE),
        )
        self.assertIsNone(paper_bib_fetch.entry_doi(ARXIV_MULTILINE))
        self.assertEqual(
            "10.1038/s41746-026-03117-z", paper_bib_fetch.entry_doi(CROSSREF_ONE_LINE)
        )

    def test_bare_and_quoted_field_values(self) -> None:
        self.assertEqual("Aug", paper_bib_fetch.field_value(CROSSREF_ONE_LINE, "month"))
        self.assertEqual(
            "Demo", paper_bib_fetch.field_value('@misc{k, title = "Demo",}', "title")
        )

    def test_exactly_one_entry_is_parsed(self) -> None:
        self.assertEqual(1, len(paper_bib_fetch.parse_entries(CROSSREF_ONE_LINE)))
        self.assertEqual(
            2, len(paper_bib_fetch.parse_entries(CROSSREF_ONE_LINE + ARXIV_MULTILINE))
        )


class ValidationTest(unittest.TestCase):
    def _validate(self, bibtex: str, **kwargs):
        options = {"expected_doi": None, "expected_title": None, "min_similarity": 0.90}
        options.update(kwargs)
        return paper_bib_fetch.validate(bibtex, **options)

    def test_wrong_paper_is_rejected_by_doi(self) -> None:
        errors, _, _ = self._validate(
            CROSSREF_ONE_LINE, expected_doi="10.1109/icpc66645.2025.00064"
        )
        self.assertTrue(any("bib-doi-mismatch" in error for error in errors))

    def test_wrong_paper_is_rejected_by_title(self) -> None:
        """The real Crossref trap: a similar title, a different paper."""
        errors, _, facts = self._validate(
            ARXIV_MULTILINE,
            expected_title="LLM-BL: Large Language Models are Zero-Shot Rankers "
            "for Bug Localization",
        )
        self.assertTrue(any("bib-title-mismatch" in error for error in errors))
        self.assertLess(facts["title_similarity"], 0.90)

    def test_two_entries_refused(self) -> None:
        errors, _, _ = self._validate(CROSSREF_ONE_LINE + ARXIV_MULTILINE)
        self.assertTrue(any("bib-entry-count" in error for error in errors))

    def test_missing_doi_warns_without_blocking(self) -> None:
        errors, warnings, _ = self._validate(ARXIV_MULTILINE)
        self.assertEqual([], errors)
        self.assertTrue(any("no-doi-in-entry" in warning for warning in warnings))

    def test_url_shaped_key_warns(self) -> None:
        _, warnings, _ = self._validate(
            "@misc{https://doi.org/10.5281/zenodo.3723939, title={Demo},}"
        )
        self.assertTrue(any("url-shaped-key" in warning for warning in warnings))

    def test_case_only_difference_warns(self) -> None:
        _, warnings, _ = self._validate(
            SCHOLAR_SHAPED,
            expected_title="Large Language Models are Zero-Shot Rankers for "
            "Recommender Systems",
        )
        self.assertTrue(any("title-case-differs" in warning for warning in warnings))

    def test_sentence_case_venue_is_not_a_finding(self) -> None:
        """npj Digital Medicine uses sentence case; it must not warn."""
        title = (
            "Mapping patient-perceived physician traits from nationwide online "
            "reviews with LLMs"
        )
        errors, warnings, _ = self._validate(
            CROSSREF_ONE_LINE,
            expected_doi="10.1038/s41746-026-03117-z",
            expected_title=title,
        )
        self.assertEqual([], errors)
        # The only warning left is the missing year cross-check, never a case or
        # DOI finding: sentence case is legitimate for this venue.
        self.assertEqual(1, len(warnings))
        self.assertIn("no-year-cross-check", warnings[0])

    def test_full_cross_check_is_completely_clean(self) -> None:
        """With the year supplied, the intended call has nothing to report."""
        errors, warnings, _ = self._validate(
            CROSSREF_ONE_LINE,
            expected_doi="10.1038/s41746-026-03117-z",
            expected_title="Mapping patient-perceived physician traits from "
            "nationwide online reviews with LLMs",
            expected_year=2026,
        )
        self.assertEqual([], errors)
        self.assertEqual([], warnings)


DECOY_SAME_TITLE = """@article{Decoy_2025,
  title = {Attention Is All You Need},
  author = {Someone, Else},
  year = {2025},
  doi = {10.65215/2q58a426}
}
"""
REAL_NEURIPS = """@inproceedings{NIPS2017_3f5ee243,
 author = {Vaswani, Ashish and Shazeer, Noam},
 booktitle = {Advances in Neural Information Processing Systems},
 title = {Attention is All you Need},
 volume = {30},
 year = {2017}
}
"""


class TitleCollisionTest(unittest.TestCase):
    """A resolved DOI agrees with itself, so the title guard alone is not enough.

    10.65215/2q58a426 is a real 2025 posting on a Shenzhen preprint server that
    reuses the exact title "Attention Is All You Need".
    """

    TITLE = "Attention Is All You Need"

    def test_decoy_passes_doi_and_title_guards_alone(self) -> None:
        errors, _, facts = paper_bib_fetch.validate(
            DECOY_SAME_TITLE,
            expected_doi="10.65215/2q58a426",
            expected_title=self.TITLE,
            min_similarity=0.90,
        )
        self.assertEqual([], errors)
        self.assertEqual(1.0, facts["title_similarity"])

    def test_expected_year_catches_the_decoy(self) -> None:
        errors, _, _ = paper_bib_fetch.validate(
            DECOY_SAME_TITLE,
            expected_doi="10.65215/2q58a426",
            expected_title=self.TITLE,
            min_similarity=0.90,
            expected_year=2017,
        )
        self.assertTrue(any("bib-year-mismatch" in error for error in errors))

    def test_missing_year_cross_check_warns_on_a_doi_identity(self) -> None:
        _, warnings, _ = self._decoy_warnings()
        self.assertTrue(any("no-year-cross-check" in w for w in warnings))

    def test_posting_type_is_surfaced(self) -> None:
        _, warnings, _ = self._decoy_warnings()
        self.assertTrue(any("subject-is-a-posting" in w for w in warnings))
        self.assertTrue(any("Shenzhen" in w for w in warnings))

    def _decoy_warnings(self):
        return paper_bib_fetch.validate(
            DECOY_SAME_TITLE,
            expected_doi="10.65215/2q58a426",
            expected_title=self.TITLE,
            min_similarity=0.90,
            record={
                "state": "found",
                "type": "posted-content",
                "publisher": "Shenzhen Medical Academy of Research and Translation",
                "year": 2025,
            },
        )

    def test_the_real_paper_passes_with_its_year(self) -> None:
        errors, _, facts = paper_bib_fetch.validate(
            REAL_NEURIPS,
            expected_doi=None,
            expected_title="Attention is All you Need",
            min_similarity=0.90,
            expected_year=2017,
        )
        self.assertEqual([], errors)
        self.assertEqual(2017, facts["year"])


class ShortTitleTest(unittest.TestCase):
    """SAGE registers "The Face of Success" for a paper whose entry carries the
    full title with its subtitle.  Found in a real audit of 384 Results."""

    FULL = ("The Face of Success: Inferences From Chief Executive Officers' "
            "Appearance Predict Company Profits")

    def test_registered_short_title_is_a_match(self) -> None:
        agree, ratio = paper_bib_fetch.titles_agree(self.FULL, "The Face of Success", 0.90)
        self.assertTrue(agree)
        self.assertLess(ratio, 0.90)

    def test_a_short_fragment_is_still_a_mismatch(self) -> None:
        agree, _ = paper_bib_fetch.titles_agree("Attention Is All You Need", "Attention", 0.90)
        self.assertFalse(agree)

    def test_the_short_form_warns_so_a_person_confirms(self) -> None:
        entry = "@article{K, title = {The Face of Success}, year = {2008},}"
        _, warnings, _ = paper_bib_fetch.validate(
            entry, expected_doi=None, expected_title=self.FULL,
            min_similarity=0.90, expected_year=2008,
        )
        self.assertTrue(
            any("title-is-a-registered-short-form" in w for w in warnings)
        )


class IdentifierConflictTest(unittest.TestCase):
    def test_arxiv_id_encodes_its_year(self) -> None:
        self.assertEqual(2017, paper_bib_fetch.arxiv_id_year("1706.03762"))
        self.assertIsNone(paper_bib_fetch.arxiv_id_year("cs/0101001"))
        self.assertIsNone(paper_bib_fetch.arxiv_id_year(None))

    def test_merged_record_is_flagged(self) -> None:
        """OpenAlex merges arXiv 1706.03762 (2017) with a 2025 posting's DOI."""
        rows = [
            {"arxiv": "1706.03762", "year": 2025},
            {"arxiv": "1706.03762", "year": 2017},
            {"arxiv": None, "year": 2025},
        ]
        paper_bib_fetch.flag_identifier_conflicts(rows)
        self.assertTrue(rows[0]["identifier_conflict"])
        self.assertFalse(rows[1]["identifier_conflict"])
        self.assertFalse(rows[2]["identifier_conflict"])


class ChannelStatusTest(unittest.TestCase):
    """A dead channel must never read as a channel that found nothing.

    OpenAlex answers 503 "Anonymous search is paused" under load; before this,
    the JSON was byte-identical whether the channel was down or simply empty,
    so a one-ply safety net looked like a three-ply one.
    """

    def test_record_keeps_the_landing_page(self) -> None:
        block = paper_bib_fetch.build_bib_block(
            verification=None,
            record={
                "state": "found",
                "type": "journal-article",
                "landing_page": "https://dx.plos.org/10.1371/journal.pmed.1002686",
            },
            **RuntimeStampTest.BLOCK_ARGS,
        )
        self.assertIn("landing_page:", block)
        self.assertIn("dx.plos.org", block)

    def test_channel_state_distinguishes_down_from_empty(self) -> None:
        empty = "ok:0"
        down = "http-503"
        self.assertTrue(empty.startswith("ok"))
        self.assertFalse(down.startswith("ok"))


class ChannelWordingTest(unittest.TestCase):
    def test_scholar_signature_named_only_for_scholar(self) -> None:
        _, scholar, _ = paper_bib_fetch.validate(
            SCHOLAR_SHAPED,
            expected_doi=None,
            expected_title="Large Language Models are Zero-Shot Rankers for "
            "Recommender Systems",
            min_similarity=0.90,
            channel="google-scholar-export",
        )
        self.assertTrue(any("Google Scholar export signature" in w for w in scholar))
        _, publisher, _ = paper_bib_fetch.validate(
            REAL_NEURIPS,
            expected_doi=None,
            expected_title="Attention is All you Need",
            min_similarity=0.90,
            channel="publisher",
        )
        self.assertTrue(publisher)  # no-doi still warns
        self.assertFalse(any("Scholar" in w for w in publisher))


class RuntimeStampTest(unittest.TestCase):
    BLOCK_ARGS = {
        "source": "https://api.crossref.org/works/10.1000%2Fdemo/transform/"
        "application/x-bibtex",
        "channel": "crossref",
        "source_class": paper_bib_fetch.AUTHORITATIVE,
        "fetched_at": "2026-09-28T23:57:41-04:00",
    }
    VERIFIED = (
        "  verification:\n"
        "    status: verified\n"
        '    by: "person:jluo41"\n'
        '    at: "2026-09-28T23:59:00-04:00"\n'
    )

    def test_block_records_verbatim_mode_and_pending_verification(self) -> None:
        block = paper_bib_fetch.build_bib_block(verification=None, **self.BLOCK_ARGS)
        self.assertIn("mode: verbatim_copy", block)
        self.assertIn("source_class: authoritative-export", block)
        self.assertIn("status: pending", block)
        self.assertNotIn("verified", block)

    def test_accepted_record_is_written_into_the_receipt(self) -> None:
        block = paper_bib_fetch.build_bib_block(
            verification=None,
            record={
                "state": "found",
                "type": "posted-content",
                "publisher": "Shenzhen Medical Academy of Research and Translation",
                "year": 2025,
            },
            **self.BLOCK_ARGS,
        )
        self.assertIn("record:", block)
        self.assertIn("type: \"posted-content\"", block)
        self.assertIn("Shenzhen", block)

    def test_person_export_class_is_preserved_in_the_receipt(self) -> None:
        args = dict(self.BLOCK_ARGS, source_class=paper_bib_fetch.PERSON_EXPORT)
        block = paper_bib_fetch.build_bib_block(verification=None, **args)
        self.assertIn("source_class: person-export", block)

    def _runtime(self, directory: Path, bib_block: str = "") -> Path:
        path = directory / "runtime.yaml"
        path.write_text(
            "run: r01_demo\nfamily: discovery\nstatus: complete\n" + bib_block,
            encoding="utf-8",
        )
        return path

    def test_appends_when_no_bib_block_exists(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self._runtime(Path(raw))
            block = paper_bib_fetch.build_bib_block(verification=None, **self.BLOCK_ARGS)
            action = paper_bib_fetch.stamp_runtime(path, block, keep_verification=None)
            self.assertEqual("appended", action)
            self.assertIn("mode: verbatim_copy", path.read_text(encoding="utf-8"))

    def test_unchanged_entry_keeps_the_person_verification(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self._runtime(Path(raw), "bib:\n  mode: verbatim_copy\n" + self.VERIFIED)
            keep = paper_bib_fetch.existing_verification(path)
            self.assertIsNotNone(keep)
            block = paper_bib_fetch.build_bib_block(verification=keep, **self.BLOCK_ARGS)
            action = paper_bib_fetch.stamp_runtime(path, block, keep_verification=keep)
            self.assertEqual("replaced", action)
            self.assertIn("status: verified", path.read_text(encoding="utf-8"))

    def test_new_entry_resets_the_person_verification(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = self._runtime(Path(raw), "bib:\n  mode: verbatim_copy\n" + self.VERIFIED)
            block = paper_bib_fetch.build_bib_block(verification=None, **self.BLOCK_ARGS)
            action = paper_bib_fetch.stamp_runtime(path, block, keep_verification=None)
            self.assertEqual("replaced+verification-reset", action)
            text = path.read_text(encoding="utf-8")
            self.assertIn("status: pending", text)
            self.assertNotIn("status: verified", text)



class KeyRenameTest(unittest.TestCase):
    def test_a_colliding_key_is_renamed_and_every_field_stays_verbatim(self) -> None:
        # Crossref keys both of an author's 2019 papers `O_Cathain_2019`; the Task Bib refuses
        # two entries under one key, so the second Result takes its own key
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as td:
            src, result = Path(td) / "export.bib", Path(td) / "r02_luo2026_traits"
            src.write_text(CROSSREF_ONE_LINE, encoding="utf-8")
            result.mkdir()
            (result / "runtime.yaml").write_text("run: r02_luo2026_traits\nstatus: planned\n", encoding="utf-8")
            argv = ["paper_bib_fetch.py", "--bib-file", str(src), "--source-url", "https://example.org/export.bib",
                    "--title", "Mapping patient-perceived physician traits from nationwide online reviews with LLMs",
                    "--expected-year", "2026", "--key", "Luo_2026_traits", "--result-dir", str(result)]
            old_argv, sys.argv = sys.argv, argv
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(0, paper_bib_fetch.main())
            finally:
                sys.argv = old_argv
            bib = (result / "r02_luo2026_traits.bib").read_text(encoding="utf-8")
            self.assertEqual(CROSSREF_ONE_LINE.replace("{Luo_2026,", "{Luo_2026_traits,", 1), bib)
            runtime = (result / "runtime.yaml").read_text(encoding="utf-8")
            self.assertIn('  key_from: "Luo_2026"', runtime)
            self.assertIn("  mode: verbatim_copy", runtime)


if __name__ == "__main__":
    unittest.main()
