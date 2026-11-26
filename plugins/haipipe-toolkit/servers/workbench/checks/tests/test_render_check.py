"""render_check.py names the same kinds as the format table, and a file whose page breaks is reported (haipipe-ui A09)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "render_check.py"
spec = importlib.util.spec_from_file_location("render_check", HERE)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


class RenderCheckTest(unittest.TestCase):
    def test_the_table_and_the_script_name_the_same_kinds(self):
        self.assertEqual(rc.table_kinds(), list(rc.KINDS))

    def test_a_page_missing_its_goal_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            face = Path(tmp) / "j01_x" / "j01_x.md"
            face.parent.mkdir()
            face.write_text("# j01 · X\ngoal: Count the rows of the extract.\n")
            original = rc.page
            rc.page = lambda folder, **kw: "<html>" + "x" * 600 + folder.name + "</html>"     # a page without its goal
            try:
                self.assertIn("does not show its goal", rc.face_page(face, True))
                rc.page = lambda folder, **kw: "<p>" + folder.name + " Count the rows of the extract.</p>" + "x" * 600
                self.assertEqual(rc.face_page(face, True), "")
                rc.page = lambda folder, **kw: ""
                self.assertEqual(rc.face_page(face, True), "renders empty")
            finally:
                rc.page = original

    def test_a_trace_without_its_fields_is_reported(self):
        rc._live()
        with tempfile.TemporaryDirectory() as tmp:
            face = Path(tmp) / "0900_x.md"
            face.write_text("---\ntitle: x\n---\n")
            self.assertIn("lacks date, aim, plan", rc.trace(face))


if __name__ == "__main__":
    unittest.main()
