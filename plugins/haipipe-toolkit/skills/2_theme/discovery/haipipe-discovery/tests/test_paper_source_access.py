from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "paper_source_access.py"
SPEC = importlib.util.spec_from_file_location("paper_source_access", SCRIPT)
assert SPEC and SPEC.loader
paper_source_access = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paper_source_access
SPEC.loader.exec_module(paper_source_access)


class PaperSourceAccessTest(unittest.TestCase):
    def test_offline_identity_hints_restore_pubmed_and_pmc_routes(self) -> None:
        record = paper_source_access.build_record(
            "10.1000/demo",
            "Demo paper",
            "https://api.crossref.org/demo",
            1.0,
            offline=True,
            pmid_hint="12345678",
            pmcid_hint="PMC123456",
        )
        self.assertEqual(
            "https://pubmed.ncbi.nlm.nih.gov/12345678/",
            record["links"]["pubmed"],
        )
        self.assertEqual(
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC123456/",
            record["links"]["full_text"],
        )
        self.assertEqual("metadata-only", record["retrieval"]["reading_depth"])

    def test_openalex_reads_one_work_by_doi_and_drops_boilerplate_abstracts(self) -> None:
        seen = []

        def fake(url, timeout):
            seen.append(url)
            words = {"International": [0], "audience": [1]} if "short" in url else \
                {"w%d" % i: [i] for i in range(40)}
            return {"id": "https://openalex.org/W1", "abstract_inverted_index": words,
                    "open_access": {"is_oa": True}, "best_oa_location": {"pdf_url": "https://example.org/p.pdf"}}, "ok"

        real = paper_source_access._get_json
        paper_source_access._get_json = fake
        try:
            short = paper_source_access._openalex("10.1000/short", 1.0)
            full = paper_source_access._openalex("10.1000/full", 1.0)
        finally:
            paper_source_access._get_json = real
        # a single-work lookup, not a filtered search (searches run out of budget first)
        self.assertEqual("https://api.openalex.org/works/doi:10.1000/short", seen[0])
        self.assertIsNone(short["abstract"])
        self.assertEqual(40, len(full["abstract"].split()))
        self.assertEqual("https://example.org/p.pdf", full["pdf_url"])

    def test_markdown_exposes_required_human_links_and_scope(self) -> None:
        record = {
            "links": {
                "article": "https://doi.org/10.1000/demo",
                "publisher": "https://example.org/paper",
                "pubmed": "https://pubmed.ncbi.nlm.nih.gov/?term=demo",
                "google_scholar": "https://scholar.google.com/scholar?q=demo",
                "google": "https://www.google.com/search?q=demo",
                "bibtex": "https://api.crossref.org/demo",
                "crossref": "https://api.crossref.org/works/demo",
                "openalex": None,
                "full_text": None,
            },
            "retrieval": {
                "reading_depth": "metadata-only",
                "claim_support": "pending",
                "locator_status": "pending",
                "full_text": "not-found",
            },
        }
        rendered = paper_source_access.render_markdown(record)
        self.assertIn("Google Scholar", rendered)
        self.assertIn("Google", rendered)
        self.assertIn("PubMed", rendered)
        self.assertIn("Reading depth:** metadata-only", rendered)
        self.assertIn("navigation aids, not evidence authority", rendered)


if __name__ == "__main__":
    unittest.main()
