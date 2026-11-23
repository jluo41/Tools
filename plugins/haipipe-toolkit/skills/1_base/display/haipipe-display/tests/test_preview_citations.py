"""build_preview: a display that cites a paper prints the citation as the built paper does, never "(?)"
(Pp-AgreeableRx 261121, Table C1: three \\citep printed "(?)" because the preview had no bibliography)."""
import importlib.util
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("bp_cite", Path(__file__).resolve().parents[1] / "scripts" / "build_preview.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

MASTER = ("\\documentclass{article}\n\\usepackage{natbib}\n\\usepackage{graphicx}\n\\begin{document}\nText.\n"
          "\\bibliographystyle{plainnat}\n\\bibliography{reference}\n\\end{document}\n")
BIB = "@article{dowell2016cdc, author={Dowell, Deborah and Haegerich, Tamara}, title={CDC guideline}, journal={JAMA}, year={2016}}\n"
TABLE = "\\begin{table}[H]\\caption{Variables}\\input{table-body.tex}\\end{table}\n"
BODY = "\\begin{tabular}{l}CDC guidance \\citep{dowell2016cdc}\\\\\\end{tabular}\n"


class PreviewCitationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.latex, self.unit = root / "delivery" / "latex", root / "unit"
        self.latex.mkdir(parents=True); self.unit.mkdir()
        (self.latex / "master.tex").write_text(MASTER)
        (self.latex / "reference.bib").write_text(BIB)
        (self.unit / "float.tex").write_text(TABLE)
        (self.unit / "table-body.tex").write_text(BODY)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_cite_in_an_input_file_is_found(self):
        self.assertTrue(bp.cited(self.unit))
        (self.unit / "table-body.tex").write_text("\\begin{tabular}{l}x\\\\\\end{tabular}\n")
        self.assertFalse(bp.cited(self.unit))

    def test_hidden_bib_points_at_the_papers_bib(self):
        line = bp.hidden_bib(self.latex / "master.tex")
        self.assertIn("\\setbox0=\\vbox{\\bibliographystyle{plainnat}", line)
        self.assertIn((self.latex / "reference").as_posix() + "}", line)

    @unittest.skipUnless(shutil.which("pdflatex") and shutil.which("bibtex") and shutil.which("pdftotext"), "needs TeX")
    def test_preview_prints_the_citation(self):
        pdf = bp.build(self.unit, preamble_from=self.latex / "master.tex")
        text = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True).stdout
        self.assertIn("Dowell and Haegerich", text)
        self.assertNotIn("(?)", text)
        self.assertFalse((self.unit / "preview.bbl").exists())   # build files are cleaned


if __name__ == "__main__":
    unittest.main()
