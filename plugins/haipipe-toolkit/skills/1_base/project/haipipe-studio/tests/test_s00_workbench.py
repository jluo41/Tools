"""S00 generation stays connected to the shared Workbench and current Tools writer."""
import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS.parents[2] / "workbench/workbench/cli"))
import block_index
import wb


class S00WorkbenchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        tools = next(p for p in SCRIPTS.parents if (p / "install.sh").is_file())
        (self.root / "Tools").symlink_to(tools, target_is_directory=True)
        (self.root / "env.sh").write_text("")
        self.block = self.root / "Project-Example/work/b01_topic"
        self.block.mkdir(parents=True)
        (self.block / "board.md").write_text("# Example\nboard-kind: task-block\nspine: Check the setup.\n")
        self.topic = self.block / "studio" / block_index.S00

    def tearDown(self):
        self.tmp.cleanup()

    def draw(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return block_index.draw(self.block)

    def test_generated_s00_is_view_only_and_runner_preserves_human_marks(self):
        scene_path = self.draw()
        runner = self.topic / "build_s00_background_and_index.py"
        self.assertTrue(runner.is_file())
        self.assertIn("Tools/plugins/", runner.read_text())
        self.assertNotIn(str(self.root), runner.read_text())
        row = wb.frame._topic_row(self.topic, [scene_path], self.root, self.block, shared=self.block)
        self.assertNotIn("class=draw-edit", row)
        self.assertIn("<iframe", row)
        self.assertIn("studio=1", wb.target(self.block, self.root)["url"])
        scene = json.loads(scene_path.read_text())
        mark = dict(next(e for e in scene["elements"] if e["type"] == "text"))
        mark.update(id="human-note", text="keep this human note", originalText="keep this human note")
        scene["elements"].append(mark)
        scene_path.write_text(json.dumps(scene))
        subprocess.run([sys.executable, str(runner)], cwd=self.root, check=True, capture_output=True)
        rebuilt = json.loads(scene_path.read_text())
        self.assertIn("keep this human note", [e.get("text") for e in rebuilt["elements"]])

    def test_existing_local_builder_is_preserved(self):
        self.topic.mkdir(parents=True)
        runner = self.topic / "build_s00_background_and_index.py"
        runner.write_text("# an existing owner-written runner\n")
        self.draw()
        self.assertEqual(runner.read_text(), "# an existing owner-written runner\n")


if __name__ == "__main__":
    unittest.main()
