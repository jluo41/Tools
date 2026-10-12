"""haipipe-studio: the topic scaffold, a builder that keeps the person's marks, the preview, sessions."""
import contextlib
import io
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

    def test_the_topic_count_is_guidance_and_child_inputs_use_the_block(self):
        messages = io.StringIO()
        with contextlib.redirect_stderr(messages):
            for nn in range(1, 11):
                new_topic.new_topic(self.block, f"topic-{nn}", f"Topic {nn}", nn=nn)
        self.assertEqual(messages.getvalue(), "")
        job = self.block / "j01_work"
        task = job / "t01_item"
        task.mkdir(parents=True)
        with contextlib.redirect_stderr(messages):
            md = new_topic.new_topic(task, "server", "Server", nn=51)
        self.assertEqual(md.parent.parent, self.block / "studio")
        self.assertFalse((task / "studio").exists())
        self.assertTrue(md.is_file())
        self.assertEqual(len(new_topic.topics(self.block)), 11)
        self.assertIn("11 studio topics", messages.getvalue())
        self.assertIn("at most 10", messages.getvalue())

    def test_child_sessions_find_shared_topics_and_preserve_legacy_local_topics(self):
        new_topic.new_topic(self.block, "shared", "Shared")
        job = self.block / "j01_work"
        task = job / "t01_item"
        task.mkdir(parents=True)
        shared = new_topic.save_session(task, "s01", "Shared session", date="1010")
        self.assertTrue(shared.is_relative_to(self.block / "runs/run-draw-s01"))
        local = job / "studio/s01-local"
        local.mkdir(parents=True)
        (local / "s01-local.md").write_text("s01 local\n====\n")
        legacy = new_topic.save_session(job, "s01", "Legacy session", date="1010")
        self.assertTrue(legacy.is_relative_to(job / "runs/run-draw-s01"))
        self.assertTrue((shared / "pass.md").is_file() and (legacy / "pass.md").is_file())

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

    def test_words_are_written_in_one_readable_font(self):
        out = self.block / "font.excalidraw"
        mk = lambda s, fam, y: {"id": s, "type": "text", "x": 0, "y": y, "width": 10, "height": 10, "text": s,
                                "originalText": s, "fontSize": 20, "fontFamily": fam}
        canvas.write(out, [mk("hand", 1, 0), mk("comic", 8, 40), mk("path/to/code.py", 3, 80)], "test")
        fams = {e["text"]: e["fontFamily"] for e in json.loads(out.read_text())["elements"]}
        self.assertEqual(fams, {"hand": canvas.FONT, "comic": canvas.FONT, "path/to/code.py": canvas.CODE_FONT})
        self.assertEqual(canvas.change_note(0, 0, "moved", "261009")["fontFamily"], canvas.FONT)
        md = new_topic.new_topic(self.block, "plain", "Plain", builder=True)
        texts = [e for e in json.loads(md.with_suffix(".excalidraw").read_text())["elements"] if e["type"] == "text"]
        self.assertEqual({e["fontFamily"] for e in texts}, {canvas.FONT})


    def test_grid_sets_frames_in_rows_not_one_column(self):
        """JL 261009: "don't put all the things in one column"; each frame moves with what is in it."""
        frame = lambda fid, y: {"id": fid, "type": "frame", "x": 0, "y": y, "width": 100, "height": 50}
        els = [frame(f"f{i}", i * 80) for i in range(4)] + [{"id": "t", "type": "text", "x": 10, "y": 250,
                                                             "frameId": "f3"}]
        self.assertTrue(canvas.one_column(els))
        canvas.grid(els, [["f0", "f1"], ["f2", "f3"]], gap=20)
        self.assertEqual([(e["x"], e["y"]) for e in els[:4]], [(0, 0), (120, 0), (0, 70), (120, 70)])
        self.assertEqual((els[4]["x"], els[4]["y"]), (130, 80))
        self.assertFalse(canvas.one_column(els))
        with self.assertRaises(AssertionError):
            canvas.grid(els, [["f0", "f1", "f2"]])
    def test_a_frame_fits_the_screen(self):
        """JL 261010: "when I zoom in 50% I can read the whole workflow, when I read 100%, I can see most part of
        the frame"; a frame over FRAME_MAX is listed, and the build warns."""
        w, h = canvas.FRAME_MAX
        els = [{"id": "ok", "type": "frame", "name": "fits", "x": 0, "y": 0, "width": 2560, "height": 1440},
               {"id": "big", "type": "frame", "name": "huge", "x": 0, "y": 0, "width": 9200, "height": 5650}]
        self.assertTrue(2560 <= w and 1440 <= h)
        self.assertEqual(canvas.oversized(els), [("huge", 9200, 5650)])
        # one piece read top to bottom stays one frame: only its width must fit (JL 261010)
        long = [canvas.reads_down({"id": "t", "type": "frame", "name": "written out", "width": 2560, "height": 9000}),
                canvas.reads_down({"id": "w", "type": "frame", "name": "too wide", "width": 4000, "height": 9000})]
        self.assertEqual(canvas.oversized(long), [("too wide", 4000, 9000)])
        cut = [{"id": f"p{i}", "type": "frame", "name": f"Task 2.1 written out · {i}"} for i in (1, 2, 3)]
        self.assertEqual(canvas.numbered_frames(cut + long), {"Task 2.1 written out": 3})
        self.assertEqual(canvas.numbered_frames([{"id": "a", "type": "frame", "name": "s03 · Why"}]), {})
        out = self.block / "studio" / "s01-x" / "s01-x.excalidraw"
        out.parent.mkdir(parents=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            canvas.write(out, els, "build_s01_x.py")
        self.assertIn("frame 'huge' is 9200 x 5650 px", buf.getvalue())
        self.assertNotIn("'fits'", buf.getvalue())
        word = lambda fid, size, color=canvas.INK: {"id": f"t{fid}{size}", "type": "text", "x": 0, "y": 0,
                                                    "width": 10, "height": 10, "frameId": fid, "fontSize": size,
                                                    "strokeColor": color, "text": "w"}
        frames = [{"id": "ok", "type": "frame", "name": "fits"}, {"id": "big", "type": "frame", "name": "tiny words"}]
        words = [word("ok", 20), word("ok", 22), word("ok", 16, canvas.GREEN), word("big", 6), word("big", 6)]
        self.assertEqual(canvas.small_text(frames + words), [("tiny words", 6)])
        notes = [canvas.aside(word("ok", 14)) for _ in range(5)]     # side notes, small on purpose
        self.assertEqual(canvas.small_text(frames + words + notes), [("tiny words", 6)])

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
        ticket = (run / "run-draw-s01.md").read_text()
        self.assertIn(f"close: {new_topic.DRAW_CLOSE}", ticket)      # a real close rule, not the placeholder
        self.assertNotIn("<what settles it>", ticket)
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
        designs = SCRIPTS.parents[4].parent.parent / "blueprints"   # Tools/designs, renamed 261009
        if not designs.is_dir():
            self.skipTest("no blueprint Blocks beside this plugin")
        self.assertFalse((designs / "b10_project_workbench" / "studio" / "_build" / "canvas.py").exists())
        for f in designs.glob("*/studio/**/*.py"):
            if "history" in f.parts:
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"(?m)^\s*import canvas\b", text):
                self.assertIn("haipipe-studio", text, f"{f.name} imports canvas without haipipe-studio's path")

    def test_the_inventory_reads_what_the_work_already_answers(self):
        # b10 s10, JL 261012: topics and Questions inferred from the Block's own Jobs and Tasks
        import block_inventory as inv
        for j, (ready, gap) in enumerate((("ready", "42 people"), ("ready", "12 people"), ("blocked", "No people"))):
            job = self.block / f"j0{j + 1}_drop{j + 1}"
            job.mkdir()
            (job / f"{job.name}.md").write_text(f"# {job.name}\n\ngoal: open\n")
            for name, body in ((f"t01_profile_glucose", f"family: csv\n\n## Opening\n\n`glucose`: 9 rows; "
                                f"{'no event time' if j == 2 else '2021-01 to 2022-01'}.\n\n### 1 · Whose data is it?\n"
                                f"**{gap}** in `id`.\n"),
                               (f"t02_profile_meals", "family: xml\n\n### 1 · Whose data is it?\n**5 people**.\n"),
                               (f"t93_source_handoff", f"### 1 · Is the dataset ready for Source?\n**`{ready}`**.\n"
                                                       "### 2 · Where does each file go?\n**Every file has a place**\n")):
                (job / name).mkdir()
                (job / name / f"{name}.md").write_text(f"# {name}\n\nstate: done\n{body}")
        b = inv.read_block(self.block)
        s = inv.summarize(b)
        c = inv.candidates(b, s)
        self.assertEqual(s["kinds"]["profile"], {"tasks": 6, "jobs": 3})
        self.assertEqual(s["splits"], {"family": {"csv": 3, "xml": 3}})            # a field that splits the Tasks
        block_q = {q["question"]: q for q in c["block_questions"]}
        self.assertEqual(block_q["Is the dataset ready for Source?"]["differ"], {"blocked": ["j03_drop3"]})
        self.assertNotIn("Where does each file go?", block_q)                      # answered the same everywhere
        self.assertNotIn("Where does each file go?", [q["question"] for q in c["job_questions"]])
        self.assertIn("Is the dataset ready for Source?", [q["question"] for q in c["job_questions"]])
        self.assertTrue(any("no event time: 1 Tasks in j03_drop3" in line for line in s["stands_out"]))
        self.assertIn("how the profile Tasks are done", [t["topic"] for t in c["topics"]])


    def test_a_screen_frame_wears_the_workbench_colours_and_the_rest_stays_black(self):
        def box(i, x, y, w, h, fid, **kw):
            return {"id": i, "type": "rectangle", "x": x, "y": y, "width": w, "height": h, "frameId": fid,
                    "strokeColor": canvas.INK, "backgroundColor": "transparent", "strokeWidth": kw.get("sw", 1.5),
                    "strokeStyle": kw.get("style", "solid")}

        def word(i, x, y, s, fid, color=canvas.INK, size=20):
            return {"id": i, "type": "text", "x": x, "y": y, "width": 60, "height": 24, "frameId": fid,
                    "text": s, "fontSize": size, "strokeColor": color, "backgroundColor": "transparent"}

        screen = canvas.ui_frame({"id": "f1", "type": "frame", "x": 0, "y": 0, "width": 900, "height": 500})
        plain = {"id": "f2", "type": "frame", "x": 1000, "y": 0, "width": 400, "height": 400}
        els = [screen, plain,
               box("tab", 20, 20, 100, 40, "f1", sw=3.5), word("tabw", 30, 28, "Report", "f1"),
               box("btn", 140, 20, 100, 40, "f1"), word("btnw", 150, 28, "Work", "f1"),
               box("new", 260, 20, 100, 40, "f1", style="dashed"), word("neww", 270, 28, "+ Group", "f1"),
               box("pill", 380, 20, 110, 40, "f1"), word("pillw", 390, 28, "shaping", "f1"),
               box("bar", 20, 100, 80, 10, "f1"),
               word("q", 20, 200, "? who signs", "f1", color=canvas.RED),
               word("st", 20, 240, "partial", "f1"),
               box("pane", 10, 10, 880, 480, "f1"),                       # drawn last, to fit it
               box("card", 1020, 20, 200, 80, "f2", sw=3.5), word("cardw", 1030, 30, "a card", "f2")]
        canvas.colour_ui(els)
        canvas.apply_palette(els)
        by = {e["id"]: e for e in els}
        self.assertEqual((by["pane"]["strokeColor"], by["pane"]["backgroundColor"]), (canvas.UI["edge"], canvas.UI["wash"]))
        self.assertLess(els.index(by["pane"]), els.index(by["tab"]))                    # the pane sits behind
        self.assertEqual((by["tab"]["strokeColor"], by["tab"]["backgroundColor"]), (canvas.UI["on"], canvas.UI["on_bg"]))
        self.assertEqual(by["tabw"]["strokeColor"], canvas.UI["on"])
        self.assertEqual(by["btn"]["backgroundColor"], canvas.UI["box"])
        self.assertEqual(by["new"]["strokeColor"], canvas.UI["new"])
        self.assertEqual(by["pill"]["strokeColor"], canvas.STAGE_UI["shaping"][0])
        self.assertEqual(by["bar"]["backgroundColor"], canvas.UI["on"])
        self.assertEqual(by["q"]["strokeColor"], canvas.RED)                              # a question stays red
        self.assertEqual(by["st"]["strokeColor"], canvas.STATUS_UI["partial"])
        self.assertEqual((by["card"]["strokeColor"], by["card"]["backgroundColor"]), (canvas.INK, "transparent"))
        self.assertEqual(canvas.off_palette(els), [])                                    # a screen is not off the palette


if __name__ == "__main__":
    unittest.main()
