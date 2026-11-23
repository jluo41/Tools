"""Displays list (Pp-AgreeableRx 261121): a renumbered display's tab line takes the plan's name, never its folder's old
number, and a display the paper no longer prints (`number: not printed`) leaves the list."""
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(HERE.parent / "_host"), str(HERE), str(HERE.parent / "workbench")]
import board_displays as bd  # noqa: E402


class DisplayListNamesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.job = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def task(self, name, face):
        t = self.job / name
        t.mkdir()
        (t / f"{name}.md").write_text(face)
        return t

    def test_renumbered_display_uses_the_plan_name(self):
        t = self.task("t57_tablec3-icd-codes", "# t57_tablec3-icd-codes · Table C4\nnumber: Table C4\ntype: table\n")
        self.assertEqual(bd._display_line(t, "c3 icd codes", "Which ICD-10 codes define each cohort?"),
                         "📊 Table · Which ICD-10 codes define each cohort?")
        self.assertEqual(bd._display_line(t, "c3 icd codes"), "📊 Table · Icd codes")   # no plan: the old number goes

    def test_not_printed_display_is_retired(self):
        self.assertTrue(bd.retired(self.task("t54_tabled1-robustness", "# t54 · Table D1\nnumber: not printed\n")))
        self.assertFalse(bd.retired(self.task("t59_tabled1-prior-opioid", "# t59 · Table D1\nnumber: Table D1\n")))


if __name__ == "__main__":
    unittest.main()
