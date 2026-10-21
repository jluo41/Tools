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

    def test_the_skeleton_draws_in_black_red_and_green_and_one_key_colour(self):
        # excalidraw-studio's principle 5 (b31 s01-D05): one slight colour marks a frame's key point, nothing else
        md = new_topic.new_topic(self.block, "plain", "Plain", builder=True)
        els = json.loads(md.with_suffix(".excalidraw").read_text())["elements"]
        key = canvas.KEY
        self.assertEqual(canvas.off_palette(els), [])                                   # the key fill is the look's
        kept = [{"type": "rectangle", "backgroundColor": key}, {"type": "rectangle", "backgroundColor": "#ffec99"}]
        canvas.apply_palette(kept)                                  # the palette on keeps the key point (b10 s52, 261012)
        self.assertEqual([e["backgroundColor"] for e in kept], [key, "transparent"])
        self.assertEqual(sum(e.get("backgroundColor") == key for e in els), 1)
        self.assertEqual({e["strokeColor"] for e in els}, {canvas.INK, canvas.RED})
        self.assertIn("from draw import", (md.parent / "build_s01_plain.py").read_text())   # excalidraw-studio's helpers
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

    def test_s00_is_three_frames_each_a_tree_and_other_topics_are_free(self):
        """JL 261012: "如果有 background，大概三个 frame 就差不多了 ... 就像 folder tree 那样", for s00 only: "I just mean for
        the s00 to have the tree, why you make all the others to be the tree as well"."""
        studio = self.block / "studio"
        s00 = studio / "s00-background-and-index" / "s00-background-and-index.excalidraw"
        self.assertEqual(canvas.frame_limit(s00), canvas.MAX_FRAMES)
        for free in (studio / "s05-x" / "s05-x.excalidraw", studio / "s32-element-ui" / "s32-element-ui.excalidraw",
                     studio / "s61-deck" / "s61-deck.excalidraw", self.block / "reports" / "q01_x" / "q01_x.excalidraw"):
            self.assertIsNone(canvas.frame_limit(free))
        nodes = [{"studio/": ["s01 · one", {"s02 · two": ["? still open", "✎ 261012 changed"]}]}, "j01 · a Job"]
        els, height = canvas.tree(0, 0, nodes, 1200, "f")
        texts = {e["text"]: e for e in els if e["type"] == "text"}
        self.assertEqual(texts["? still open"]["strokeColor"], canvas.RED)
        self.assertEqual(texts["✎ 261012 changed"]["strokeColor"], canvas.GREEN)
        self.assertTrue(any(e["type"] == "line" for e in els) and height > 0)
        frame = lambda i, **kw: dict({"id": f"f{i}", "type": "frame", "name": f"step {i}", "x": i * 3000, "y": 0,
                                      "width": 2560, "height": 1440}, **kw)
        word = lambda i, n: {"id": f"w{i}", "type": "text", "x": i * 3000, "y": 0, "width": 10, "height": 10,
                             "frameId": f"f{i}", "fontSize": 20, "strokeColor": canvas.INK, "text": " ".join(["w"] * n)}
        slides = [frame(i) for i in range(4)] + [word(i, 30) for i in range(4)]
        self.assertEqual(len(canvas.sparse(slides)), 4)                                  # 30 words a screen: a slide
        self.assertEqual(canvas.sparse([frame(0), word(0, 600)]), [])                     # a full screen is not
        self.assertEqual(canvas.sparse([frame(9)]), [])                                   # no words: not judged
        topic = studio / "s05-x" / "s05-x.excalidraw"                                    # any other topic: free
        topic.parent.mkdir(parents=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            canvas.write(topic, [dict(e) for e in slides], "build_s05_x.py")
        self.assertNotIn("over 3", buf.getvalue())
        self.assertNotIn("reads like a slide", buf.getvalue())
        s00.parent.mkdir(parents=True)                                                    # s00: checked
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            canvas.write(s00, [dict(e) for e in slides], "block_index.py")
        self.assertIn("4 frames, over 3", buf.getvalue())
        self.assertIn("reads like a slide", buf.getvalue())

    def test_every_block_gets_its_background_and_index(self):
        """JL 261012: "for every block, we also want to have the s00-background-and-index to show the background
        information, and what are the sNN and jNN and what are the progress of them"."""
        import block_index
        b = self.block
        (b / "board.md").write_text("# b01 · Topic\n\nspine: why this Block exists.\nclose: when every Question is "
                                    "answered.\n\nThis Block asks one thing. It holds two Jobs of work.\n")
        for rel, text in {"studio/s01-a/s01-a.md": "s01 · A\n=======\n\n**Stage:** shaping\n\n**Topic:** the first "
                                                   "topic.\n\n**Feeds:** q01_one\n\ns01-D01 · decided (261012)\n\n\n"
                                                   "Open\n----\n\n1. Who signs?\n",
                          "j01_work/j01_work.md": "# j01 · Work\n\nstate: ACTIVE\n",
                          "j01_work/t01_first/t01_first.md": "# t01 · First\n\nstate: ✅ DONE\n",
                          "j01_work/t02_second/t02_second.md": "# t02 · Second\n\nstate: 🟡 PLANNED\n",
                          "reports/q01_one/q01_one.md": "# Q01 · Does it hold?\n\nanswer-status: partial\n"}.items():
            (b / rel).parent.mkdir(parents=True, exist_ok=True)
            (b / rel).write_text(text)
        (b / "j01_work" / "t01_first" / "runs" / "r01_x").mkdir(parents=True)
        tree = block_index.index_tree(block_index.read_block(b))
        flat = json.dumps(tree, ensure_ascii=False)
        for said in ("🔶 s01 · A", "the first topic.", "→ Q01", "🧱 j01 · Work",
                     "📋 2 Tasks: ✅ 1 done · ⬜ 1 open · 1 Runs", "🔶 q01_one · partial · Does it hold?"):
            self.assertIn(said, flat)
        self.assertEqual(block_index.state_word("🟢 RUNNING"), "active")
        self.assertEqual(block_index.state_word("🟡 PLANNED"), "open")
        self.assertEqual(block_index.state_word("🟡 PARTIAL · r03 done"), "partly")
        with contextlib.redirect_stdout(io.StringIO()):
            out = block_index.draw(b)
        face = b / "studio" / block_index.S00 / f"{block_index.S00}.md"
        self.assertTrue(face.is_file() and out.is_file() and out.with_suffix(".png").is_file())
        self.assertIn("❓ Seeded from the Block", face.read_text())
        frames = lambda: [e["name"] for e in json.loads(out.read_text())["elements"] if e["type"] == "frame"]
        self.assertEqual(frames(), ["s00 · b01_topic · the index"])                      # a thin background folds in
        drawn = json.loads(out.read_text())["elements"]
        said = " | ".join(e.get("text", "") for e in drawn if e["type"] == "text").replace("\n", " ")
        for words in ("thinks in", "works in", "🧠 Studio | where we think", "🧱 Jobs | where we work", "🔶 s01 · A",
                      "📝 Q01 · Does it hold?", "🧱 j01 · Work", "Tasks 1/2 done", "why it exists | why this Block exists.",
                      "❓ no close: line yet"):
            self.assertIn(words, said)                       # a mind map: Block → Studio / Jobs → each → what it leads to
        self.assertGreaterEqual(sum(e["type"] == "arrow" for e in drawn), 5)
        self.assertIn("🔶 s01 · A | the first topic.", said)                    # each topic says what it is for
        size = {e["text"]: e["fontSize"] for e in drawn if e["type"] == "text"}
        self.assertGreater(size["Topic"], size["🧠 Studio"])                             # the Block, then a branch,
        self.assertGreater(size["🧠 Studio"], size["🔶 s01 · A"])                        # then an item,
        self.assertGreater(size["🔶 s01 · A"], size["the first topic."])                 # then its detail (JL 261012)
        self.assertNotIn("open", said.split("🔶 s01 · A")[1].split("|")[1])             # no "N open" (JL 261012)
        self.assertFalse(any(e.get("link") for e in drawn))                              # no links (JL 261012)
        index = next(e for e in drawn if e["type"] == "frame" and e["name"].endswith("the index"))
        rows = [e for e in drawn if e["type"] == "rectangle" and e.get("frameId") == index["id"]
                and e["x"] > block_index.X_ITEM - 5]
        self.assertEqual(len({round(e["x"]) for e in rows}), 1)                          # one column: a row each
        self.assertNotRegex(said, r"\d+ (explore|shaping|agreed|closed)\b")              # no counts: they go stale
        rich = {"background": [{"title": "Why", "tree": [{f"Part {k}": [" ".join(["word"] * 30)] * 3} for k in range(8)]},
                               {"title": "How", "tree": ["one leaf", "two leaf"]}]}
        face.write_text(re.sub(r"```yaml\n.*?```", "```yaml\n" + yaml.safe_dump(rich) + "```", face.read_text(),
                               flags=re.S))
        with contextlib.redirect_stdout(io.StringIO()):
            block_index.draw(b)
        # background first; a background too small for a screen's third merges into the index, under its title
        # (excalidraw-studio: "a thin frame is merged, not padded"), with its heading and tree (JL 261012)
        self.assertEqual(frames(), ["s00 · Why", "s00 · b01_topic · the index"])
        drawn = json.loads(out.read_text())["elements"]
        index = next(e for e in drawn if e["type"] == "frame" and e["name"].endswith("the index"))
        inside = {e["text"]: e for e in drawn if e["type"] == "text" and e.get("frameId") == index["id"]}
        self.assertIn("How", inside)
        self.assertTrue(any("one leaf" in k for k in inside))
        self.assertLess(inside["How"]["y"], inside["Topic"]["y"])                       # above the mind map
        self.assertEqual(sum(e.get("backgroundColor") == block_index.KEY for e in drawn
                             if e.get("frameId") == index["id"]), 1)                     # one key point: the Block
        self.assertEqual(block_index.blocks(Path(self.tmp.name)), [b])

    def test_s00_draws_proposed_topics_and_jobs_until_made(self):
        """JL 261012: "s00 should also work in a way for the proposing the sNN and jNN as well"; "we also need to propose
        the new studio and new jobs in a new frame": one row each, the gap ─▶ the topic ─▶ the Job ─▶ what it delivers."""
        import block_index
        b = self.block
        (b / "studio" / "s01-a").mkdir(parents=True)
        (b / "studio" / "s01-a" / "s01-a.md").write_text("s01 · A\n=======\n\n**Stage:** shaping\n\n**Topic:** a.\n")
        face = b / "studio" / block_index.S00 / f"{block_index.S00}.md"
        face.parent.mkdir(parents=True)
        face.write_text("s00 · Background and index\n\n```yaml\nstudio_plan:\n  steps:\n  - title: Plan\n"
                        "    ids: [s01, s02]\n```\n\n```yaml\n" + yaml.safe_dump({"studio_proposals": [
                            {"id": "s02", "title": "Moved", "status": "proposed", "question": "What moves?",
                             "output": "a list", "why": "Q01 nobody feeds"}]}) + "```\n\n```yaml\n" +
                        yaml.safe_dump({"job_proposals": [
                            {"id": "j01", "slug": "move", "title": "Move them", "status": "proposed",
                             "topics": ["s02", "s01"], "finish": "every builder moved", "why": "nothing moves them"},
                            {"id": "j02", "slug": "keep", "title": "Keep it", "status": "proposed", "topics": ["s01"],
                             "finish": "kept", "why": "s01 Open 1"}]}) + "```\n")
        with contextlib.redirect_stdout(io.StringIO()):
            out = block_index.draw(b)
        drawn = json.loads(out.read_text())["elements"]
        frames = {e["id"]: e["name"] for e in drawn if e["type"] == "frame"}
        self.assertEqual(list(frames.values())[-1], "s00 · 💡 b01_topic · what we propose next")   # ④, after the index
        fid = lambda end: next((e["id"] for e in drawn if e["type"] == "frame" and e["name"].endswith(end)), None)
        text = lambda end: " | ".join(e["text"] for e in drawn if e["type"] == "text" and e.get("frameId") == fid(end)
                                      ).replace("\n", " ")
        ask = text("what we propose next")
        for words in ("❓ the gap it closes", "🧠 the topic", "🧱 the Job", "🏁 what it delivers",   # the columns
                      "❓ s02: Q01 nobody feeds", "❓ j01: nothing moves them",                   # row 1: both gaps,
                      "⬜ s02 · Moved [proposed]", "What moves?", "→ a list",                       # the topic,
                      "⬜ j01_move · Move them [proposed]", "rests on: s02 · s01", "🏁 every builder moved",  # its Job
                      "❓ s01 Open 1", "🔶 s01 · A", "⬜ j02_keep · Keep it [proposed]", "🏁 kept"):  # row 2: a made one
            self.assertIn(words, ask)
        self.assertLess(ask.index("Q01 nobody feeds"), ask.index("s02 · Moved"))                  # read left to right
        self.assertLess(ask.index("s02 · Moved"), ask.index("j01_move"))
        boxes = [e for e in drawn if e["type"] == "rectangle" and e.get("frameId") == fid("what we propose next")
                 and e.get("backgroundColor") != "#fff3bf"]                      # the key point is not a cell
        # excalidraw-studio's principles where they fit s00 (JL 261012): each frame's key point on the slight colour,
        # and the frames as acts, named at the left, a named arrow for each step
        for f in (e for e in drawn if e["type"] == "frame"):
            self.assertEqual(sum(e.get("backgroundColor") == "#fff3bf" for e in drawn if e.get("frameId") == f["id"]),
                             1, f["name"])
        free = [e for e in drawn if not e.get("frameId")]
        self.assertTrue(any(e["type"] == "text" and e["text"].startswith("Act 2 ·") for e in free))
        self.assertTrue(any(e["type"] == "text" and e["text"] == "still needs" for e in free))
        self.assertEqual(sum(e["strokeColor"] == canvas.RED and e["strokeStyle"] == "dashed" for e in boxes), 3)
        self.assertEqual(sum(e["strokeColor"] == canvas.INK and e["strokeStyle"] == "solid" for e in boxes), 1)
        self.assertEqual(sum(e["type"] == "arrow" and e.get("frameId") == fid("what we propose next") for e in drawn), 6)
        index = text("the index")
        self.assertNotIn("Move them", index)                                           # the index: what is on disk,
        self.assertIn("❓ proposed, not made yet: j01_move · j02_keep", index)          # and one line naming the rest
        (b / "j01_move").mkdir()
        (b / "j01_move" / "j01_move.md").write_text("# j01 · Move them\n\nstate: ACTIVE\n")
        with contextlib.redirect_stdout(io.StringIO()):
            block_index.draw(b)
        drawn = json.loads(out.read_text())["elements"]
        self.assertIn("🧱 j01 · Move them", text("the index"))                          # made: a Job row now
        self.assertNotIn("j01_move", text("what we propose next"))
        self.assertIn("⬜ s02 · Moved [proposed]", text("what we propose next"))
        (b / "studio" / "s02-moved").mkdir()
        (b / "j02_keep").mkdir()
        (b / "j02_keep" / "j02_keep.md").write_text("# j02 · Keep it\n\nstate: ACTIVE\n")
        with contextlib.redirect_stdout(io.StringIO()):
            block_index.draw(b)
        drawn = json.loads(out.read_text())["elements"]
        self.assertIsNone(fid("what we propose next"))                                  # all made: no ④

    def test_a_topic_draws_from_its_face_as_boxes_and_arrows(self):
        """JL 261012: "so we can have both tree and box, and -->"; "add the things like the emoji"."""
        import topic_map
        topic = self.block / "studio" / "s02-x"
        topic.mkdir(parents=True)
        frames = {"frames": [
            {"title": "🧭 Background", "tree": ["📁 a leaf", {"🧱 a branch": ["❓ still open"]}]},
            {"title": "🌳 The tree", "boxes": [
                {"id": "a", "at": [0, 0], "title": "🧠 Studio", "why": "where we think", "tree": ["s01 · one"]},
                {"id": "b", "at": [1, 0], "title": "📝 Questions", "why": "what we answer", "tree": ["Q01 · one"]}],
             "arrows": [{"from": "a", "to": "b", "label": "feeds"}, {"from": "b", "to": "a", "label": "? asks back"}]}]}
        (topic / "s02-x.md").write_text("s02 · X\n=======\n\n```yaml\n" + yaml.safe_dump(frames, allow_unicode=True)
                                       + "```\n")
        extra = lambda els: els.append(dict(topic_map.frame_el("screen", "③ the screen", 400, 300)))
        with contextlib.redirect_stdout(io.StringIO()) as buf:
            out = topic_map.draw_topic(topic, extra=extra)
        drawn = json.loads(out.read_text())["elements"]
        self.assertEqual([e["name"] for e in drawn if e["type"] == "frame"],
                         ["s02 · 🧭 Background", "s02 · 🌳 The tree", "③ the screen"])
        by_text = {e["text"]: e for e in drawn if e["type"] == "text"}
        self.assertEqual(by_text["❓ still open"]["strokeColor"], canvas.RED)
        self.assertEqual(by_text["feeds"]["strokeColor"], canvas.INK)
        arrows = [e for e in drawn if e["type"] == "arrow"]
        self.assertEqual(sorted((e["strokeStyle"], e["strokeColor"]) for e in arrows),
                         [("dashed", canvas.RED), ("solid", canvas.INK)])
        self.assertTrue(out.with_suffix(".png").is_file())
        self.assertNotIn("over 3", buf.getvalue())


    def test_chinese_text_is_as_wide_as_it_is_drawn(self):
        # JL 261012, on b32 s00's "EB1A 递交" frame: "this is not complete" (each line cut at a width guessed for English)
        e, _ = canvas.tree_text(0, 0, "📦 EB1A 递交：什么交给谁", 48)
        self.assertGreaterEqual(e["width"], 10 * 48)                # ten Chinese characters at a full em each
        e, _ = canvas.tree_text(0, 0, "表格 / 个人事实 / 原件 / 陈述 / 最终目录", 24, 300)
        self.assertGreater(len(e["text"].split("\n")), 1)           # wrapped, not one line past the box
        self.assertLessEqual(e["width"], 300 + 4)
        self.assertTrue(all(canvas.text_width(ln, 24) <= 300 for ln in e["text"].split("\n")))


if __name__ == "__main__":
    unittest.main()


def test_a_csv_row_is_read_by_its_columns(tmp_path):
    import job_results as jr
    (tmp_path / "slopes.csv").write_text("model_id,context,estimate\nm5,lbp,9.19\nm5,cancer,0.12\n")
    assert jr.at_value(tmp_path, "slopes.csv:model_id=m5&context=cancer.estimate", "") == "0.12"


def test_feeds_find_the_report_of_each_answered_id(tmp_path):
    """A Job's answers: holds Question ids (Q01, Q-food-1, a need Q01.E2); Feeds names their report folders
    (b51 261020: `Q-food-1` gave "none yet" because only `qNN_` folder names were read)."""
    import job_results as jr
    for name in ("q-food-1_input_output", "q-food-10_other", "q01_lookup", "q-all-6_check_lane_gaps"):
        (tmp_path / "reports" / name).mkdir(parents=True)
    job = tmp_path / "j01_x"
    job.mkdir()
    (job / "j01_x.md").write_text("# j01 · x\n\ngoal: g\nanswers: Q-food-1, Q01.E2, Q-all-6\n")
    assert jr.feeds_of([job], tmp_path) == ["q-food-1_input_output", "q01_lookup", "q-all-6_check_lane_gaps"]


class StairsTest(unittest.TestCase):
    """canvas.stairs (JL 261013: "你不能每一个都是朝左对齐"): the main frame at the origin, each next frame lower and
    further right, so no two share a left edge; each frame moves with what is drawn in it."""

    def test_frames_step_down_and_right(self):
        els = [{"id": f, "type": "frame", "x": 0, "y": 0, "width": w, "height": h}
               for f, w, h in (("main", 2000, 1500), ("a", 900, 600), ("b", 700, 400))]
        els.append({"id": "t", "type": "text", "x": 10, "y": 10, "frameId": "a"})
        placed = canvas.stairs(els, ["main", ("a", 600), "b"], gap=200, step=400)
        main, a, b = placed
        self.assertEqual((main["x"], main["y"]), (0, 0))
        self.assertEqual((a["x"], a["y"]), (600, 1700))
        self.assertEqual((b["x"], b["y"]), (1000, 2500))
        self.assertEqual(next(e for e in els if e["id"] == "t")["x"], 610)
        with self.assertRaises(AssertionError):
            canvas.stairs(els, ["main", "a"])                         # every frame placed once

    def test_grid_carries_what_follows_a_frame_and_gives_it_room(self):
        """A staircase's results sit outside its frame, marked customData.follows: grid moves them with the frame
        and the next row starts below them (261014, b01 s24: the results stayed behind when Acts laid it out)."""
        els = [{"id": "f0", "type": "frame", "x": 500, "y": 500, "width": 400, "height": 300},
               {"id": "r", "type": "rectangle", "x": 1000, "y": 500, "width": 200, "height": 600,
                "customData": {"follows": "f0"}},
               {"id": "f1", "type": "frame", "x": 0, "y": 0, "width": 100, "height": 100}]
        canvas.grid(els, [["f0"], ["f1"]], gap=20)
        r = next(e for e in els if e["id"] == "r")
        self.assertEqual((r["x"], r["y"]), (500, 0))                  # moved with f0 by (-500, -500)
        self.assertEqual(els[2]["y"], 620)                            # f1 below r's bottom (600) + gap, not f0's
