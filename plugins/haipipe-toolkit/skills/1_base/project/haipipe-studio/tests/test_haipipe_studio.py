"""haipipe-studio: the topic scaffold, a builder that keeps the person's marks, the preview, sessions."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import canvas  # noqa: E402
import new_topic  # noqa: E402


class StudioTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project-Example" / "tasks" / "b01_topic"
        self.block.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_topics_number_in_their_band(self):
        a = new_topic.new_topic(self.block, "first", "First")
        b = new_topic.new_topic(self.block, "runs", "Runs", band="run")
        c = new_topic.new_topic(self.block, "second", "Second")
        self.assertEqual([p.parent.name for p in (a, b, c)], ["s01-first", "s21-runs", "s02-second"])
        with self.assertRaises(ValueError):
            new_topic.new_topic(self.block, "again", "Again", nn=21)

    def test_a_slide_draft_numbers_in_s6x(self):
        d = new_topic.new_topic(self.block, "deck", "Deck", band="slides")
        self.assertEqual(d.parent.name, "s61-deck")

    def test_the_face_reads_as_the_frame_reads_it(self):
        md = new_topic.new_topic(self.block, "first", "First", feeds=["q01_one", "q02_two"])
        text = md.read_text()
        self.assertTrue(text.startswith("s01 · First\n==========="))
        self.assertIn("**Topic:**", text)
        self.assertIn("**Feeds:** `reports/` q01_one · q02_two", text)
        for head in ("Files\n-----", "Decided\n-------", "Open\n----"):
            self.assertIn(head, text)

    def test_a_builder_draws_and_a_rebuild_keeps_the_persons_mark(self):
        md = new_topic.new_topic(self.block, "drawn", "Drawn", builder=True)
        drawing = md.with_suffix(".excalidraw")
        script = md.parent / "build_s01_drawn.py"
        self.assertTrue(drawing.is_file() and script.is_file())
        self.assertTrue((md.parent / ".s01-drawn.seed.json").is_file())
        doc = json.loads(drawing.read_text())
        doc["elements"].append({"id": "mine", "type": "text", "x": 5, "y": 5, "width": 10, "height": 10,
                                "text": "my note", "strokeColor": "#e03131"})
        drawing.write_text(json.dumps(doc))
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
        texts = [e.get("text") for e in json.loads(drawing.read_text())["elements"]]
        self.assertIn("my note", texts)
        self.assertIn("s01 · Drawn", texts)
        self.assertIn('sys.path.insert(0, str((HERE / "..', script.read_text())   # a relative path, never absolute

    def test_a_change_gets_a_green_note_where_it_changed_and_in_the_title(self):
        note = canvas.change_note(100, 200, "moved the box", "261007", frame="f1")
        self.assertEqual((note["text"], note["strokeColor"], note["frameId"]), ("✎ 261007 moved the box", canvas.GREEN, "f1"))
        md = new_topic.new_topic(self.block, "drawn", "Drawn", builder=True)
        script = md.parent / "build_s01_drawn.py"
        script.write_text(script.read_text().replace("CHANGES = []", 'CHANGES = [("261007", "added the first box")]'))
        subprocess.run([sys.executable, str(script)], check=True, capture_output=True)
        els = json.loads(md.with_suffix(".excalidraw").read_text())["elements"]
        green = [e for e in els if e.get("strokeColor") == canvas.GREEN]
        self.assertEqual([e["text"] for e in green], ["✎ 261007 added the first box"])

    def test_the_skeleton_draws_in_black_red_and_green_only(self):
        md = new_topic.new_topic(self.block, "plain", "Plain", builder=True)
        els = json.loads(md.with_suffix(".excalidraw").read_text())["elements"]
        self.assertEqual(canvas.off_palette(els), [])
        self.assertEqual({e["strokeColor"] for e in els}, {canvas.INK, canvas.RED})
        self.assertEqual(len(canvas.off_palette([{"strokeColor": "#1971c2"}, {"backgroundColor": "#ffec99"}])), 2)

    def test_two_elements_with_one_id_stay_two(self):
        out = self.block / "dup.excalidraw"
        mk = lambda x: {"id": "same", "type": "rectangle", "x": x, "y": 0, "width": 10, "height": 10}
        canvas.write(out, [mk(0), mk(50)], "test")
        canvas.write(out, [mk(0), mk(50)], "test")             # a rebuild: still two, nothing "kept"
        els = json.loads(out.read_text())["elements"]
        self.assertEqual(len({e["id"] for e in els}), 2)

    def test_a_canvas_from_another_writer_is_flagged(self):
        out = self.block / "foreign.excalidraw"
        out.write_text(json.dumps({"elements": [{"id": "ds-box", "type": "rectangle", "x": 0, "y": 0,
                                                  "width": 10, "height": 10}]}))
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            canvas.write(out, [{"id": "a", "type": "rectangle", "x": 0, "y": 0, "width": 10, "height": 10}], "test")
        self.assertIn("no seed snapshot", buf.getvalue())

    def test_the_preview_renders(self):
        md = new_topic.new_topic(self.block, "drawn", "Drawn", builder=True)
        png = md.with_suffix(".png")
        out = subprocess.run([sys.executable, str(SCRIPTS / "render_png.py"), str(md.with_suffix(".excalidraw")), str(png)],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertGreater(png.stat().st_size, 1000)

    def test_a_session_is_a_pass_of_run_draw(self):
        new_topic.new_topic(self.block, "first", "First")
        p1 = new_topic.save_session(self.block, "s01", "First session", ask="<ask>", date="1007")
        p2 = new_topic.save_session(self.block, "s01", "Second session", date="1008")
        run = self.block / "runs" / "run-draw-s01"
        self.assertEqual((p1.name, p2.name), ("p01-1007", "p02-1008"))
        card = yaml.safe_load((run / "run.yaml").read_text())
        self.assertEqual((card["skill"], card["passes"]), ("haipipe-studio", ["p01-1007", "p02-1008"]))
        new_topic.new_topic(self.block, "fed", "Fed", feeds=["q02_two"])
        new_topic.save_session(self.block, "s02", "One", date="1008")
        fed = yaml.safe_load((self.block / "runs" / "run-draw-s02" / "run.yaml").read_text())
        self.assertEqual(fed["feeds"], ["reports/q02_two"])
        with self.assertRaises(ValueError):
            new_topic.save_session(self.block, "s07", "No such topic")

    def test_legacy_snapshots_are_looked_up_only_where_registered(self):
        self.assertEqual(canvas.LEGACY_DIRS, [])
        self.assertIsNone(canvas.legacy_seed(self.block / "x.excalidraw", [{"id": "s-1"}]))

    def test_no_builder_reaches_canvas_through_the_old_address(self):
        designs = SCRIPTS.parents[4].parent.parent / "designs"
        if not designs.is_dir():
            self.skipTest("no design Blocks beside this plugin")
        self.assertFalse((designs / "b01_haipipe-toolkit" / "j03_project_workbench" / "studio" / "_build" / "canvas.py").exists())
        for f in designs.glob("*/studio/**/*.py"):
            if "history" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?m)^\s*import canvas\b", text):
                self.assertIn("haipipe-studio", text, f"{f.name} imports canvas without haipipe-studio's path")


if __name__ == "__main__":
    unittest.main()
