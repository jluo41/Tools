"""hai-trace's script on a temporary Block: new, prompt, changed, close, check."""
import importlib.util
import os
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("trace", HERE / "scripts" / "trace.py")
trace = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trace)


class TraceScriptTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / "examples/P/work/b01_x").mkdir(parents=True)
        (self.root / "tools").mkdir()
        (self.root / "tools/a.py").write_text("x = 1\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@example.test",
                        "commit", "-qm", "x", "--allow-empty"], check=True)
        self.cwd = os.getcwd()
        os.chdir(self.root)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def run_(self, *argv):
        out = StringIO()
        with redirect_stdout(out):
            code = trace.main(list(argv))
        return code, out.getvalue().strip()

    def test_the_loop_from_plan_to_close(self):
        code, made = self.run_("new", "examples/P/work/b01_x", "--slug", "zoom", "--title", "zoom",
                               "--aim", "It zooms: by day, by trace.", "--plan", "edit|tools/a.py|three levels",
                               "--prompt", "how could I zoom?")
        self.assertEqual(code, 0)
        face = self.root / made
        meta, body = trace.split(face.read_text())
        self.assertEqual(meta["aim"], "It zooms: by day, by trace.")          # a colon cannot break it
        self.assertEqual([i["path"] for i in meta["plan"]], [made, "tools/a.py"])
        self.assertIn("how could I zoom?", trace.section(body, "Prompts"))
        self.run_("prompt", made, "yes, go ahead", "--at", "17:52")
        self.assertIn("**17:52** yes, go ahead", trace.section(trace.split(face.read_text())[1], "Prompts"))
        (self.root / "tools/a.py").write_text("x = 2\n")
        code, out = self.run_("changed", made)
        self.assertIn("tools/a.py", out)                                        # from git
        code, _ = self.run_("close", made, "--check", "tests: 3 passed", "--summary", "It zooms.")
        self.assertEqual(code, 0)
        meta, body = trace.split(face.read_text())
        self.assertTrue(meta["closed"])
        self.assertEqual(trace.section(body, "Summary"), "It zooms.")
        code, out = self.run_("check")
        self.assertEqual(code, 0, out)

    def test_check_finds_a_broken_trace(self):
        bad = self.root / "examples/P/work/b01_x/trace/261125/1200_bad.md"
        bad.parent.mkdir(parents=True)
        bad.write_text("---\naim: two: colons break it\n---\n")
        code, out = self.run_("check")
        self.assertEqual(code, 1)
        self.assertIn("1200_bad.md: no front matter", out)

    def test_a_plan_line_needs_do_path_and_what(self):
        with self.assertRaises(SystemExit):
            self.run_("new", "examples/P/work/b01_x", "--slug", "x", "--title", "x", "--aim", "a",
                      "--plan", "change|tools/a.py|y")


if __name__ == "__main__":
    unittest.main()
