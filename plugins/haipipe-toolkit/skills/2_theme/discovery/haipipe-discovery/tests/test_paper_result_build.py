from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "paper_result_build.py"
SPEC = importlib.util.spec_from_file_location("paper_result_build", SCRIPT)
assert SPEC and SPEC.loader
paper_result_build = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paper_result_build
SPEC.loader.exec_module(paper_result_build)


def tiny_pdf(lines_per_page: list[str]) -> bytes:
    """A minimal PDF, one line of Helvetica text per page."""
    objs, kids = [], []
    n = len(lines_per_page)
    objs.append("<< /Type /Catalog /Pages 2 0 R >>")
    objs.append("")  # pages, filled below
    font = 3 + 2 * n
    for i, line in enumerate(lines_per_page):
        page, content = 3 + 2 * i, 4 + 2 * i
        kids.append(f"{page} 0 R")
        stream = f"BT /F1 12 Tf 40 700 Td ({line}) Tj ET"
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 600 800] /Contents {content} 0 R "
                    f"/Resources << /Font << /F1 {font} 0 R >> >> >>")
        objs.append(f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream")
    objs[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {n} >>"
    objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out, offsets = "%PDF-1.4\n", []
    for k, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{k} 0 obj\n{body}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n" + "".join(f"{o:010d} 00000 n \n" for o in offsets)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return out.encode("latin-1")


class SavedCopyIsThePaperTest(unittest.TestCase):
    def test_a_one_page_table_of_contents_is_not_the_book(self) -> None:
        # OpenAlex listed a library's one-page table of contents as the open copy of a book
        title = "The Sciences of the Artificial"
        with tempfile.TemporaryDirectory() as td:
            toc, book = Path(td) / "toc.pdf", Path(td) / "book.pdf"
            toc.write_bytes(tiny_pdf(["Table of contents: The sciences of the artificial"]))
            book.write_bytes(tiny_pdf(["The Sciences of the Artificial, third edition", "Chapter 1"]))
            other = Path(td) / "other.pdf"
            other.write_bytes(tiny_pdf(["Generative agents", "Interactive simulacra"]))
            if paper_result_build._pdf_text(book) is None:
                self.skipTest("no PDF text reader here")
            self.assertFalse(paper_result_build.is_the_paper(toc, title))     # one page
            self.assertTrue(paper_result_build.is_the_paper(book, title))
            self.assertFalse(paper_result_build.is_the_paper(other, title))   # another paper


PMLR_PAGE = """<html><body>
<a href="https://openreview.net/forum?id=qugRvYjaFx">OpenReview</a>
<code class="citecode" id="bibtex">@InProceedings{pmlr-v306-wang26fy,
  title = 	 {{C}on{F}lux: Multivariate Time Series in Flux, One Unified Forecast in Confluence},
  author =       {Wang, Shiyu and Ni, Juntong and Xiang, Yang},
  booktitle = 	 {Proceedings of the 43rd International Conference on Machine Learning},
  pages = 	 {129221--129251},
  year = 	 {2026},
  volume = 	 {306},
  publisher =    {PMLR},
  pdf = 	 {https://raw.githubusercontent.com/mlresearch/v306/main/assets/wang26fy/wang26fy.pdf},
  url = 	 {https://proceedings.mlr.press/v306/wang26fy.html},
  abstract = 	 {Variables evolve &ldquo;in flux&rdquo;; we propose &lt;b&gt;ConFlux&lt;/b&gt;, a model.}
}
</code></body></html>"""


class PmlrPageTest(unittest.TestCase):
    """An ICML paper has no DOI: its PMLR page is the accepted record."""

    def test_identity_comes_from_the_citation_block(self) -> None:
        class Answer:
            def read(self):
                return PMLR_PAGE.encode("utf-8")
        real = paper_result_build.fetch
        paper_result_build.fetch = lambda url, timeout=30: Answer()
        try:
            meta = paper_result_build.pmlr("https://proceedings.mlr.press/v306/wang26fy.html")
        finally:
            paper_result_build.fetch = real
        self.assertEqual("ConFlux: Multivariate Time Series in Flux, One Unified Forecast in Confluence", meta["title"])
        self.assertEqual("Shiyu Wang; Juntong Ni; Yang Xiang", meta["authors"])
        self.assertEqual(("Wang", 3, 2026), (meta["first_family"], meta["n_authors"], meta["year"]))
        self.assertEqual("Proceedings of the 43rd International Conference on Machine Learning, PMLR 306: "
                         "129221-129251 (2026)", meta["venue"])
        self.assertEqual("Variables evolve \u201cin flux\u201d; we propose ConFlux, a model.", meta["abstract"])
        self.assertEqual("https://openreview.net/forum?id=qugRvYjaFx", meta["openreview"])
        self.assertTrue(meta["pdf"].endswith("/wang26fy.pdf"))


class DisplayTextTest(unittest.TestCase):
    def test_latex_accents_and_math_read_as_text(self) -> None:
        plain = paper_result_build.plain
        self.assertEqual("Ağırman, Ahmet", plain("A\\u{g}{\\i}rman, Ahmet"))
        self.assertEqual("Schölkopf", plain('Sch\\"{o}lkopf'))
        self.assertEqual("DT^2: Dual", plain("$\\text{DT}^\\text{2}$: Dual"))
        self.assertEqual("Erdős and François", plain("Erd{\\H o}s and Fran\\c{c}ois"))


class AcceptedFlagsTest(unittest.TestCase):
    """The accepted flags mark a preprint Bib; they are refused before any network call otherwise."""

    def run_main(self, *args):
        import contextlib, io
        argv = sys.argv
        sys.argv = ["paper_result_build.py", "--task", "t01_x", "--run", "r01_x2026_y", "--address",
                    "b01.j01.t01.r01", "--readout", "r", "--reuse", "u"] + list(args)
        try:
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
                paper_result_build.main()
        finally:
            sys.argv = argv
        return stop.exception.code

    def test_a_venue_without_its_page_is_refused(self) -> None:
        self.assertEqual(2, self.run_main("--doi", "10.48550/arXiv.2510.25502", "--bib-from", "arxiv",
                                          "--accepted-venue", "NeurIPS 2026, poster"))

    def test_a_pmlr_record_is_not_a_preprint_stand_in(self) -> None:
        self.assertEqual(2, self.run_main("--pmlr-url", "https://proceedings.mlr.press/v306/bao26c.html",
                                          "--accepted-venue", "ICML 2026", "--accepted-url", "https://openreview.net/x"))

    def test_a_venue_doi_is_not_a_preprint_stand_in(self) -> None:
        self.assertEqual(2, self.run_main("--doi", "10.1145/3770855.3817572", "--accepted-venue", "KDD 2026",
                                          "--accepted-url", "https://example.org/x"))


if __name__ == "__main__":
    unittest.main()
