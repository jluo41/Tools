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

    def test_a_new_topic_has_both_sides_its_drawing_and_its_mind_map(self):
        with contextlib.redirect_stdout(io.StringIO()):
            md = new_topic.new_topic(self.block, "fees", "Fees", feeds=["q02_fees"])
        mind = md.parent / "s01-fees.mindmap.md"                         # the same number, linked: s01 and m01
        self.assertTrue(mind.is_file())
        text = mind.read_text(encoding="utf-8")
        self.assertIn("built: from-topic .", text)
        self.assertIn("# s01 · Fees", text)
        self.assertTrue((md.parent / "s01-fees.mindmap.html").is_file())

    def test_an_sNN_sits_beside_its_level_and_the_count_is_limited(self):
        # JL 261030: "we just have sNN, along side with jNN, to make it visible directly"; "we might have many sNN,
        # but we need to control the numbers"
        for nn in range(1, 10):
            new_topic.new_topic(self.block, f"topic-{nn}", f"Topic {nn}", nn=nn)
        self.assertTrue((self.block / "s01-topic-1/s01-topic-1.md").is_file())   # beside the Jobs, no studio/
        self.assertTrue((self.block / "s01-topic-1/delivery/deck").is_dir())     # its agreed version goes here
        self.assertFalse((self.block / "studio").exists())
        with self.assertRaises(ValueError) as said:                       # a Block holds at most 9
            new_topic.new_topic(self.block, "ten", "Ten", nn=10)
        self.assertIn("at most 9", str(said.exception))
        with contextlib.redirect_stdout(io.StringIO()):
            new_topic.new_topic(self.block, "ten", "Ten", nn=10, over_limit=True)
        job = self.block / "j01_work"
        task = job / "t01_item"
        task.mkdir(parents=True)
        md = new_topic.new_topic(task, "server", "Server", nn=51)         # in the Task's own folder
        self.assertEqual(md.parent, task / "s51-server")
        self.assertNotIn("**At:**", md.read_text())                      # where it sits says its level
        self.assertIn(51, new_topic.block_topics(job))
        with self.assertRaises(ValueError):                              # one sNN numbering across the Block
            new_topic.new_topic(job, "again", "Again", nn=51)
        nxt = new_topic.new_topic(job, "next", "Next", band="level")     # the next free number, Block-wide
        self.assertEqual(nxt.parent, job / "s11-next")
        for nn in (12, 13, 14, 15):
            new_topic.new_topic(job, f"more-{nn}", "More", nn=nn)
        with self.assertRaises(ValueError) as said:                      # a Job holds at most 5
            new_topic.new_topic(job, "six", "Six", nn=16)
        self.assertIn("a Job holds at most 5", str(said.exception))

    def test_child_sessions_find_shared_topics_and_preserve_legacy_local_topics(self):
        new_topic.new_topic(self.block, "shared", "Shared")
        job = self.block / "j01_work"
        task = job / "t01_item"
        task.mkdir(parents=True)
        shared = new_topic.save_session(task, "s01", "Shared session", date="1010")
        self.assertTrue(shared.is_relative_to(self.block / "s01-shared/passes"))
        local = job / "s01-local"
        local.mkdir(parents=True)
        (local / "s01-local.md").write_text("s01 local\n====\n")
        legacy = new_topic.save_session(job, "s01", "Legacy session", date="1010")
        self.assertTrue(legacy.is_relative_to(local / "passes"))
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

    def test_a_round_lives_in_its_topic(self):
        new_topic.new_topic(self.block, "first", "First")
        p1 = new_topic.save_session(self.block, "s01", "First session", ask="<ask>", date="1007",
                                    decided=["Overview is Report"], started=["j02"])
        p2 = new_topic.save_session(self.block, "s01", "A meeting", date="1008", kind="meeting", read=["related/m.md"])
        self.assertEqual((p1.name, p2.name), ("p01-1007", "p02-1008"))
        self.assertEqual(p1.parent, self.block / "s01-first/passes")
        text = (p1 / "pass.md").read_text()
        self.assertIn("kind: session", text)
        self.assertIn("## Decided\n\n- Overview is Report", text)
        self.assertIn("## Started\n\n- j02", text)
        self.assertIn("kind: meeting", (p2 / "pass.md").read_text())
        self.assertFalse((self.block / "runs").exists())                  # no run-draw Run any more
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


class RenderDeliveryTest(unittest.TestCase):
    """An sNN's delivery/ renders out to where it is used (JL 261030)."""

    def test_a_text_piece_renders_between_its_markers_and_only_there(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("render_delivery", Path(new_topic.__file__).with_name("render_delivery.py"))
        rd = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rd)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "skill" / "SKILL.md"
            target.parent.mkdir()
            target.write_text("# head\n<!-- render b07-s01 rule: generated -->\nold\n<!-- /render b07-s01 rule -->\ntail\n")
            topic = root / "work" / "b07_x" / "s01-rule"
            (topic / "delivery" / "skill").mkdir(parents=True)
            (topic / "delivery" / "skill" / "rule.md").write_text("new text\n")
            (topic / "delivery" / "render.yaml").write_text(
                "pieces:\n  - from: skill/rule.md\n    to: skill/SKILL.md\n    block: rule\n  - code: 'x'\n    by: j01\n"
                "  - from: paper/s03.md\n    rendered_by: haipipe-paper-assemble\n")
            self.assertEqual([s for _, s, _ in rd.render(topic)], ["differs", "code", "theme"])
            self.assertEqual([s for _, s, _ in rd.render(topic, apply=True)], ["rendered", "code", "theme"])
            self.assertEqual(target.read_text(), "# head\n<!-- render b07-s01 rule: generated -->\nnew text\n<!-- /render b07-s01 rule -->\ntail\n")
            self.assertEqual([s for _, s, _ in rd.render(topic)], ["same", "code", "theme"])   # a Theme's skill renders it



class StudioUpdateTest(unittest.TestCase):
    def test_audit_names_the_misses_and_name_writes_for_type_and_an_open_point(self):
        import studio_update as su
        with tempfile.TemporaryDirectory() as tmp:
            topic = Path(tmp) / "Project-X" / "work" / "b01_x" / "studio" / "s01-a"
            topic.mkdir(parents=True)
            (topic / "s01-a.md").write_text("s01 · a\n=====\n\n**Topic:** one thing.\n\n\nOpen\n----\n\n1. first\n")
            keys = {k for _, k, _ in su.checks(topic, su.level_counts([topic]))}
            self.assertEqual(keys, {"place", "stage", "for", "type", "delivery", "render", "mindmap", "draw", "slides"})
            su.add_stage(topic)
            su.add_delivery(topic)
            su.name(topic, "a deck, and one table, for its reader", "data")
            text = (topic / "s01-a.md").read_text()
            self.assertIn("**Stage:** explore", text)
            self.assertLess(text.index("**For:**"), text.index("**Delivery type:** data"))
            self.assertIn("2. Agree its **For:** line and **Delivery type:** (data)", text)
            self.assertTrue((topic / "delivery" / "render.yaml").is_file())
            keys = {k for _, k, _ in su.checks(topic, su.level_counts([topic]))}
            # a data topic also owes its data drawn step by step (excalidraw-studio § A data topic, JL 261031)
            self.assertEqual(keys, {"place", "mindmap", "draw", "slides", "data-built"})     # never deck as a type
            with self.assertRaises(SystemExit):
                su.name(topic, "", "deck")


class GalleryScanTest(unittest.TestCase):
    def test_a_delivery_is_sorted_by_its_files_and_an_sNN_by_its_level_and_theme(self):
        import gallery_scan
        with tempfile.TemporaryDirectory() as tmp:
            proj = Path(tmp) / "Project-X"
            word = proj / "paper" / "Paper-Y" / "delivery"
            (word / "word").mkdir(parents=True)
            (word / "word" / "paper.docx").write_text("x")
            (word / "paper.pdf").write_text("x")
            deck = proj / "work" / "b01_x" / "s01-a" / "delivery"
            (deck / "deck").mkdir(parents=True)
            (deck / "deck" / "a.pptx").write_text("x")
            empty = proj / "work" / "b01_x" / "j01_y" / "s02-b" / "delivery"
            (empty / "deck").mkdir(parents=True)
            (empty / "render.yaml").write_text("pieces: []\n")
            self.assertEqual([gallery_scan.kind_of(d) for d in (word, deck, empty)], ["Word + PDF", "deck", "empty"])
            self.assertEqual([gallery_scan.level_of(d.parent.parent) for d in (deck, empty)], ["Block", "Job"])
            self.assertEqual(gallery_scan.level_of(deck.parent), "sNN")
            self.assertEqual([gallery_scan.theme_of(d) for d in (word, deck)], ["paper", "work"])
            self.assertEqual(gallery_scan.theme_of(Path(tmp) / "Proj01-CGM" / "discovery" / "b01_x" / "s01-a"), "discovery")

    def test_a_delivery_is_its_main_thing_not_its_deck_and_an_sNN_names_its_type(self):
        import gallery_scan
        with tempfile.TemporaryDirectory() as tmp:
            snn = Path(tmp) / "Project-X" / "work" / "b01_x" / "s01-a"
            for sub in ("deck", "skill"):
                (snn / "delivery" / sub).mkdir(parents=True)
                (snn / "delivery" / sub / "x.md").write_text("x")
            self.assertEqual(gallery_scan.kind_of(snn / "delivery"), "skill")       # the deck is never the kind
            (snn / "s01-a.md").write_text("s01 · a\n=====\n\n**For:** a deck, and a skill\n\n**Delivery type:** skill\n")
            self.assertEqual(gallery_scan.type_of(snn), "skill")
            (snn / "s01-a.md").write_text("s01 · a\n=====\n\n**Delivery type:** deck\n")
            self.assertEqual(gallery_scan.type_of(snn), "")                        # deck is not a type
            self.assertEqual(gallery_scan.type_of(snn.parent), "")                 # only an sNN has one

    def test_a_gallery_shows_the_newest_of_each_kind_and_only_a_tools_sNN_shows_its_words(self):
        import gallery_scan
        with tempfile.TemporaryDirectory() as tmp:
            rows = []
            for k, (space, name, for_line) in enumerate((("Tools", "s01-old", "a deck, and an old skill"),
                                                          ("Tools", "s02-new", "a deck, and a new skill"),
                                                          ("Physician", "s03-private", "a deck, and private words"))):
                d = Path(tmp) / f"{space}-SPACE" / "Project-X" / "work" / "b01_x" / name
                d.mkdir(parents=True)
                (d / f"{name}.md").write_text(f"{name} · title\n=====\n\n**For:** {for_line}\n")
                rows.append({"space": space, "path": d, "level": "Block", "theme": "work", "beside": True, "mtime": k})
            saved = dict(gallery_scan._cache)
            gallery_scan._cache.update(s=[(r["space"], r["path"]) for r in rows], d=[])
            try:
                md = gallery_scan.studio_md()
            finally:
                gallery_scan._cache.clear()
                gallery_scan._cache.update(saved)
            self.assertIn("a deck, and a new skill", md)          # the newest Tools one with a For: line
            self.assertNotIn("private words", md)                # another SPACE never shows its face's words
            self.assertIn("| Block | 3 |", md)
