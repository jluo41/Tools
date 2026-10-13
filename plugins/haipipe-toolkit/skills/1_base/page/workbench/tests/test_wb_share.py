"""/wb share (cli/wb_share.py, b10 s52): one grant written into the share root's access.yaml, and its link."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "cli"
sys.path.insert(0, str(CLI))
import wb_share as W  # noqa: E402


class WbShareTest(unittest.TestCase):
    def run_share(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = W.main(list(args))
        return code, out.getvalue()

    def test_a_grant_is_written_once_and_its_link_printed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "env.sh").write_text("")
            block = root / "blueprints" / "b10_demo"
            block.mkdir(parents=True)
            (root / ".server_config").mkdir()
            (root / ".server_config" / "access.yaml").write_text(
                "owners: [owner@jhu.edu]\npublic_url: https://block.example\n")
            code, out = self.run_share(str(block), "Someone@JH.edu", "--share-root", str(root))
            self.assertEqual(code, 0)
            self.assertIn("shared blueprints/b10_demo with someone@jhu.edu (view)", out)
            self.assertIn("https://block.example/_board/workbench?path=blueprints/b10_demo&studio=1", out)
            self.run_share(str(block), "someone@jhu.edu", "--level", "edit", "--share-root", str(root))
            cfg = W.S.ShareConfig.load(root)
            self.assertEqual(cfg.grants, [("someone@jhu.edu", "blueprints/b10_demo", 3)])      # one line, new level
            self.assertEqual(cfg.owners, {"owner@jhu.edu"})                                   # kept
            with self.assertRaises(SystemExit):
                self.run_share(str(block), "someone@gmail.com", "--share-root", str(root))
            with self.assertRaises(SystemExit):
                self.run_share(tmp + "/..", "someone@jhu.edu", "--share-root", str(root))       # outside the root
            code, listed = self.run_share("--list", "--share-root", str(root))
            self.assertIn("someone@jhu.edu", listed)
            code, out = self.run_share(str(block), "--people", "b10", "--share-root", str(root))
            people = root / ".server_config" / "people" / "b10.txt"
            self.assertTrue(people.is_file())
            self.assertIn("people  " + str(people), out)
            people.write_text(people.read_text() + "a.person@jh.edu\n")
            cfg = W.S.ShareConfig.load(root)
            self.assertEqual(cfg.level("a.person@jhu.edu", "blueprints/b10_demo"), 1)


    def test_a_space_with_no_door_is_refused(self):
        """261012: Tools-SPACE's door was dropped; a grant there would be served by nothing."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "env.sh").write_text("")
            block = root / "blueprints" / "b10_demo"
            block.mkdir(parents=True)
            with self.assertRaises(SystemExit) as no:
                self.run_share(str(block), "someone@jhu.edu", "--share-root", str(root))
            self.assertIn("has no share door", str(no.exception))
            self.assertFalse((root / ".server_config" / "access.yaml").exists())        # nothing written

    def test_folder_first_and_who_has_it(self):
        """261012 "/wb xxxx to share": wb.py <folder> share <email> grants; with nobody named it only reports."""
        import os
        import wb
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "env.sh").write_text("")
            job = root / "blueprints" / "b10_demo" / "j01_x"
            job.mkdir(parents=True)
            (root / ".server_config").mkdir()
            table = root / ".server_config" / "access.yaml"
            table.write_text("owners: [owner@jhu.edu]\npublic_url: https://block.example\n")
            here = os.getcwd()
            os.chdir(root)
            try:
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    wb.main(["blueprints/b10_demo", "share"])
                self.assertIn("🔒 blueprints/b10_demo", out.getvalue())                 # nobody yet
                self.assertNotIn("grants", table.read_text())                           # nothing written
                with contextlib.redirect_stdout(io.StringIO()):
                    wb.main(["blueprints/b10_demo", "share", "a.person@jhu.edu"])
                code, out = self.run_share(str(job))                                    # a folder below it
                self.assertIn("🔗 blueprints/b10_demo/j01_x", out)
                self.assertIn("a.person@jhu.edu", out)
                self.assertIn("path=blueprints/b10_demo/j01_x&studio=1", out)
            finally:
                os.chdir(here)

if __name__ == "__main__":
    unittest.main()
