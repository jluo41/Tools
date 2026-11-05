"""display_pick: the face's printed: version wins over the newest alternative (pp-LBP-JAMA 261103)."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
import live  # noqa: E402,F401
from live import board_evidence as fd  # noqa: E402


class DisplayPickTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.task = Path(self.tmp.name) / "t05_table3"
        for run in ("r07_v7_dots", "r08_v8_slim"):
            res = self.task / "runs" / run / "result"
            res.mkdir(parents=True)
            (res / "preview.pdf").write_bytes(b"%PDF-1.4\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_newest_without_printed(self):
        pdf, pic = fd.display_pick(self.task, "label: Table 3\n")
        self.assertEqual(pdf.parent.parent.name, "r08_v8_slim")
        self.assertIsNone(pic)

    def test_printed_wins(self):
        pdf, _ = fd.display_pick(self.task, "label: Table 3\nprinted: r07_v7_dots\n")
        self.assertEqual(pdf.parent.parent.name, "r07_v7_dots")

    def test_printed_png(self):
        res = self.task / "runs" / "r06_v6" / "result"
        res.mkdir(parents=True)
        (res / "preview.png").write_bytes(b"png")
        pdf, pic = fd.display_pick(self.task, "printed: r06_v6\n")
        self.assertIsNone(pdf)
        self.assertEqual(pic.name, "preview.png")


if __name__ == "__main__":
    unittest.main()
