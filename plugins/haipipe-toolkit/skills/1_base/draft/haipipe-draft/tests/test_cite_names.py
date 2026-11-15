"""The web export prints each citation name-year (must-check M-D02): `\\cite{key}` → "(Wolff et al. 2018)", keys on
hover; a key missing from the Page's Bib, or an entry without author or year, shows the key and "not in Bib"; code and
tag attributes keep the raw words."""
import tempfile
from pathlib import Path

from src.cite_names import bib_names, name_year


def test_name_year_with_not_in_bib():
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp)
        (folder / "draft/evidence/bibex").mkdir(parents=True)
        (folder / "draft/evidence/bibex/page.bib").write_text(
            "@article{wolff2018,\n  author = {Wolff, J. and Roter, D. and Boyd, C.},\n  year = {2018}\n}\n"
            "@article{lum2024,\n  author = {Lum, H. and Kim, B.},\n  year = {2024}\n}\n"
            "@misc{noyear,\n  author = {Lee, A.}\n}\n")
        assert bib_names(folder) == {"wolff2018": "Wolff et al. 2018", "lum2024": "Lum and Kim 2024"}
        html = ('<p class="pnew">Effects varied \\cite{wolff2018}. </p><p>Also \\citep{lum2024,TOADD}; '
                '\\citet{lum2024} and \\cite{noyear}.</p><code>\\cite{wolff2018}</code><b title="\\cite{x}">t</b>')
        out = name_year(html, folder)
        assert '<span class="cite cite-ay" title="wolff2018">(Wolff et al. 2018)</span>' in out
        assert "(Lum and Kim 2024; TOADD <span class=cite-miss" in out
        assert ">Lum and Kim (2024)</span>" in out
        assert out.count(">not in Bib</span>") == 2
        assert "<code>\\cite{wolff2018}</code>" in out and 'title="\\cite{x}"' in out
