"""build_preview.numbering: page 1 prints the display's own name and number (pp-LBP-JAMA 261103)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("bp", Path(__file__).resolve().parents[1] / "scripts" / "build_preview.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)


class NumberingTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_readme_supplement(self):
        u = self.root / "Display3-etable"
        u.mkdir()
        (u / "README.md").write_text("number: eTable 11\n")
        tex = bp.numbering(u)
        self.assertIn(r"\renewcommand{\tablename}{eTable}", tex)
        self.assertIn(r"\renewcommand{\thetable}{11}", tex)

    def test_task_face_of_a_run(self):
        res = self.root / "t09_x" / "runs" / "r01_a" / "result"
        res.mkdir(parents=True)
        (self.root / "t09_x" / "t09_x.md").write_text("label: Display J\nnumber: Figure 3\n")
        tex = bp.numbering(res)
        self.assertIn(r"\renewcommand{\figurename}{Figure}", tex)
        self.assertIn(r"\renewcommand{\thefigure}{3}", tex)

    def test_lettered_and_label_fallback(self):
        res = self.root / "t02_b" / "runs" / "r01" / "result"
        res.mkdir(parents=True)
        (self.root / "t02_b" / "t02_b.md").write_text("label: Table B1\n")
        self.assertIn(r"\renewcommand{\thetable}{B1}", bp.numbering(res))

    def test_nothing(self):
        u = self.root / "plain"
        u.mkdir()
        self.assertEqual(bp.numbering(u), "")


if __name__ == "__main__":
    unittest.main()
