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


if __name__ == "__main__":
    unittest.main()
