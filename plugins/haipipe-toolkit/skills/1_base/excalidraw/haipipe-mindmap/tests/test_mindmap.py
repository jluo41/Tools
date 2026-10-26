"""haipipe-mindmap: the grammar, the three views, sync both ways, the builders and the refresh that keeps a person's
words. A canvas edit is made the way Excalidraw saves one: the element's words, a new box with its bound text, an
arrow bound to two boxes, a box moved, a box marked deleted."""
from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mindmap  # noqa: E402
import mmbuild as MB  # noqa: E402
import mmcanvas as MC  # noqa: E402
import mmhtml as MH  # noqa: E402
import mmtree as MT  # noqa: E402

SOURCE = """---
mindmap: 1
title: Trip
---

# Trip **plan** <!-- root -->

Why we go: rest.

- Where <!-- n01 -->
  - Lisbon <!-- n02 -->
  - Porto <!-- n03 -->
- When <!-- n04 -->
  the week after the deadline
  - May <!-- n05 -->
- Budget `EUR` <!-- n06 -->

## Notes

Free notes, **kept** as written.
"""


def full(e: dict) -> dict:
    """An element with the fields Excalidraw always saves."""
    base = {"angle": 0, "strokeColor": "#1e1e1e", "backgroundColor": "transparent", "fillStyle": "solid",
            "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": None,
            "roundness": None, "seed": 1, "version": 1, "isDeleted": False, "boundElements": [], "locked": False}
    if e["type"] == "text":
        base.update(fontSize=20, fontFamily=6, textAlign="left", verticalAlign="top", lineHeight=1.25)
    return {**base, **e}


def run(*argv) -> tuple:
    out = io.StringIO()
    with redirect_stdout(out):
        rc = mindmap.main([str(a) for a in argv])
    return rc, out.getvalue()


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.md = self.dir / "trip.mindmap.md"
        self.md.write_text(SOURCE, encoding="utf-8")
        self.v = MT.views(self.md)

    def tearDown(self):
        self.tmp.cleanup()

    def render(self):
        rc, out = run("render", self.md)
        self.assertEqual(rc, 0, out)

    def doc(self) -> dict:
        return json.loads(self.v["canvas"].read_text(encoding="utf-8"))

    def save(self, doc):
        self.v["canvas"].write_text(json.dumps(doc), encoding="utf-8")

    def el(self, doc, eid):
        return next(e for e in doc["elements"] if e["id"] == eid)

    def kids(self, nid="root"):
        node, _ = MT.find(MT.load(self.md), nid)
        return [c.id for c in node.children]

    def text(self, nid):
        return MT.find(MT.load(self.md), nid)[0].text

    def new_box(self, doc, sid, x, y, words):
        doc["elements"] += [full(e) for e in [
            {"id": sid, "type": "rectangle", "x": x, "y": y, "width": 200, "height": 60, "boundElements": [
                {"type": "text", "id": sid + "-t"}]},
            {"id": sid + "-t", "type": "text", "x": x + 10, "y": y + 10, "width": 180, "height": 40, "text": words,
             "originalText": words, "containerId": sid}]]

    def arrow(self, doc, aid, a, b):
        ea, eb = self.el(doc, a), self.el(doc, b)
        x0, y0 = ea["x"] + ea["width"], ea["y"] + ea["height"] / 2
        x1, y1 = eb["x"], eb["y"] + eb["height"] / 2
        doc["elements"].append(full({"id": aid, "type": "arrow", "x": x0, "y": y0, "width": abs(x1 - x0),
                                     "height": abs(y1 - y0), "points": [[0, 0], [x1 - x0, y1 - y0]],
                                     "startBinding": {"elementId": a}, "endBinding": {"elementId": b},
                                     "endArrowhead": "arrow"}))


class Grammar(Case):
    def test_a_file_reads_and_writes_back_the_same(self):
        mm = MT.load(self.md)
        self.assertEqual(mm.meta["title"], "Trip")
        self.assertEqual([c.text for c in mm.root.children], ["Where", "When", "Budget `EUR`"])
        self.assertEqual(MT.find(mm, "n04")[0].note, ["the week after the deadline"])
        self.assertIn("Free notes, **kept** as written.", mm.tail)
        self.assertEqual(MT.dump(MT.parse(MT.dump(mm))), MT.dump(mm))

    def test_a_typed_bullet_gets_the_next_free_id_never_one_the_canvas_remembers(self):
        self.md.write_text(SOURCE.replace("- Budget", "- Food\n- Budget"), encoding="utf-8")
        mm = MT.load(self.md)
        self.assertEqual(MT.ensure_ids(mm, {"n07"}), 1)
        self.assertEqual(mm.root.children[2].id, "n08")

    def test_the_canvas_shows_words_without_markdown_marks(self):
        self.assertEqual(MT.display("a **bold** `code` [link](x.md) *it*"), "a bold code link it")

    def test_a_file_without_a_root_line_is_named_in_the_error(self):
        with self.assertRaises(MT.GrammarError):
            MT.parse("---\nmindmap: 1\n---\n\n- no root\n")

    def test_files_are_utf8_with_lf_line_ends(self):
        mm = MT.load(self.md)
        mm.root.children[0].text = "Où · 去哪里"
        MT.save(mm, self.md)
        raw = self.md.read_bytes()
        self.assertNotIn(b"\r\n", raw)
        self.assertIn("去哪里".encode("utf-8"), raw)


class Views(Case):
    def test_render_draws_the_canvas_the_preview_and_the_page(self):
        self.render()
        doc = self.doc()
        ids = {e["id"] for e in doc["elements"]}
        for nid in ("root", "n01", "n02", "n03", "n04", "n05", "n06"):
            self.assertIn(f"mm:{nid}:box", ids)
        self.assertNotIn("mm:root:edge", ids)
        edge = self.el(doc, "mm:n02:edge")
        self.assertEqual((edge["startBinding"]["elementId"], edge["endBinding"]["elementId"]), ("mm:n01:box", "mm:n02:box"))
        self.assertEqual(self.el(doc, "mm:n06:text")["originalText"], "Budget EUR")
        self.assertEqual(MC.base_of(doc)["n05"], {"text": "May", "parent": "n04", "order": 0})
        root, child = self.el(doc, "mm:root:box"), self.el(doc, "mm:n01:box")
        self.assertLess(root["x"] + root["width"], child["x"])          # left to right
        self.assertTrue(self.v["png"].is_file() and self.v["png"].stat().st_size > 1000)
        page = self.v["html"].read_text(encoding="utf-8")
        self.assertIn("<strong>plan</strong>", page)
        self.assertIn("<code>EUR</code>", page)
        self.assertIn('<img src="trip.png"', page)
        self.assertIn("<p class=note>the week after the deadline</p>", page)

    def test_a_second_render_is_the_same_canvas(self):
        self.render()
        first = self.doc()
        self.render()
        self.assertEqual(first["elements"], self.doc()["elements"])

    def test_a_persons_own_drawing_is_kept_through_a_render(self):
        self.render()
        doc = self.doc()
        doc["elements"].append(full({"id": "mine", "type": "ellipse", "x": 5000, "y": 5000, "width": 50, "height": 50}))
        self.save(doc)
        self.render()
        self.assertIn("mine", {e["id"] for e in self.doc()["elements"]})

    def test_an_edit_in_the_file_reaches_the_canvas(self):
        self.render()
        self.md.write_text(SOURCE.replace("Porto", "Porto and Braga"), encoding="utf-8")
        rc, out = run("sync", self.md)
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.el(self.doc(), "mm:n03:text")["originalText"], "Porto and Braga")

    def test_the_page_renders_markdown_blocks(self):
        page = MH.blocks("## Head\n\n- one\n  - two\n\n```\ncode <x>\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |")
        self.assertIn("<h3>Head</h3>", page)
        self.assertIn("<ul><li>one<ul><li>two</li></ul></li></ul>", page)
        self.assertIn("code &lt;x&gt;", page)
        self.assertIn("<td>2</td>", page)


class Sync(Case):
    def test_words_changed_on_the_canvas_come_back_to_the_file(self):
        self.render()
        doc = self.doc()
        t = self.el(doc, "mm:n02:text")
        t["text"] = t["originalText"] = "Lisbon, three days"
        self.save(doc)
        rc, out = run("sync", self.md)
        self.assertEqual(rc, 0, out)
        self.assertEqual(self.text("n02"), "Lisbon, three days")

    def test_a_box_joined_by_an_arrow_becomes_a_node_and_leaves_the_canvas_as_drawn(self):
        self.render()
        doc = self.doc()
        n05 = self.el(doc, "mm:n05:box")
        self.new_box(doc, "p1", n05["x"] + 600, n05["y"] + 200, "June, if not May")
        self.arrow(doc, "a1", "mm:n04:box", "p1")
        doc["elements"].append(full({"id": "doodle", "type": "text", "x": 9000, "y": 9000, "width": 90,
                                     "height": 30, "text": "just a note"}))
        self.save(doc)
        rc, out = run("sync", self.md)
        self.assertEqual(rc, 0, out)
        mm = MT.load(self.md)
        when = MT.find(mm, "n04")[0]
        self.assertEqual([c.text for c in when.children], ["May", "June, if not May"])
        self.assertEqual(when.children[1].id, "n07")
        ids = {e["id"] for e in self.doc()["elements"]}
        self.assertTrue({"p1", "p1-t", "a1"}.isdisjoint(ids))           # drawn again as the map's own
        self.assertIn("mm:n07:box", ids)
        self.assertIn("doodle", ids)                                     # not joined: still the person's

    def test_an_arrow_from_another_node_rewires_it(self):
        self.render()
        doc = self.doc()
        self.arrow(doc, "a2", "mm:n04:box", "mm:n03:box")
        self.save(doc)
        self.assertEqual(run("sync", self.md)[0], 0)
        self.assertEqual(self.kids("n01"), ["n02"])
        self.assertIn("n03", self.kids("n04"))

    def test_a_box_moved_above_its_sibling_reorders_them(self):
        self.render()
        doc = self.doc()
        self.el(doc, "mm:n03:box")["y"] = self.el(doc, "mm:n02:box")["y"] - 200
        self.save(doc)
        self.assertEqual(run("sync", self.md)[0], 0)
        self.assertEqual(self.kids("n01"), ["n03", "n02"])

    def test_a_deleted_box_deletes_its_node_and_its_children_move_up(self):
        self.render()
        doc = self.doc()
        for eid in ("mm:n01:box", "mm:n01:text", "mm:n01:edge"):
            self.el(doc, eid)["isDeleted"] = True
        self.save(doc)
        self.assertEqual(run("sync", self.md)[0], 0)
        self.assertIsNone(MT.find(MT.load(self.md), "n01")[0])
        self.assertEqual(MT.find(MT.load(self.md), "n02")[1].id, "root")

    def test_an_edit_on_both_sides_stops_until_a_side_is_picked(self):
        self.render()
        doc = self.doc()
        t = self.el(doc, "mm:n02:text")
        t["text"] = t["originalText"] = "Lisboa"
        self.save(doc)
        self.md.write_text(SOURCE.replace("Lisbon", "Lisbon old town"), encoding="utf-8")
        before = self.md.read_text(encoding="utf-8")
        rc, out = run("sync", self.md)
        self.assertEqual(rc, 2)
        self.assertIn("words changed on both sides", out)
        self.assertEqual(self.md.read_text(encoding="utf-8"), before)    # nothing written
        rc, out = run("render", self.md)
        self.assertEqual(rc, 2)                                          # render will not draw over the edit
        self.assertEqual(run("sync", self.md, "--take", "n02=canvas")[0], 0)
        self.assertEqual(self.text("n02"), "Lisboa")

    def test_taking_the_file_side_keeps_the_files_words(self):
        self.render()
        doc = self.doc()
        t = self.el(doc, "mm:n02:text")
        t["text"] = t["originalText"] = "Lisboa"
        self.save(doc)
        self.md.write_text(SOURCE.replace("Lisbon", "Lisbon old town"), encoding="utf-8")
        self.assertEqual(run("sync", self.md, "--take", "file")[0], 0)
        self.assertEqual(self.text("n02"), "Lisbon old town")
        self.assertEqual(self.el(self.doc(), "mm:n02:text")["originalText"], "Lisbon old town")

    def test_check_passes_when_in_step_and_fails_on_an_unsynced_canvas(self):
        self.render()
        self.assertEqual(run("check", self.md)[0], 0)
        doc = self.doc()
        t = self.el(doc, "mm:n05:text")
        t["text"] = t["originalText"] = "late May"
        self.save(doc)
        rc, out = run("check", self.md)
        self.assertEqual(rc, 1)
        self.assertIn("the canvas has edits not in the file", out)


def work(root: Path) -> Path:
    block = root / "work" / "b01_demo"
    for t, runs in (("t01_load", ["r01_a", "r02_b"]), ("t02_fit", ["r01_x", "r02_y", "r03_z", "r04_w", "r05_v", "r06_u"])):
        for r in runs:
            (block / "j01_build" / t / "runs" / r).mkdir(parents=True)
            (block / "j01_build" / t / "runs" / r / "run.yaml").write_text(f"run: {r}\nstatus: done\n")
    (block / "board.md").write_text("# b01 · Demo\n")
    return block


class Builders(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_from_work_draws_block_job_task_run_with_run_counts(self):
        block = work(self.root)
        rc, out = run("from-work", block)
        self.assertEqual(rc, 0, out)
        md = block / "studio" / "mind-map.mindmap.md"
        mm = MT.load(md)
        self.assertEqual(mm.meta["built"], "from-work ..")
        self.assertEqual(mm.root.text, "b01_demo · 1 job")
        job = mm.root.children[0]
        self.assertEqual(job.text, "j01_build · 2 tasks · 8 runs")
        self.assertEqual([t.text for t in job.children], ["t01_load · 2 runs, all done", "t02_fit · 6 runs, all done"])
        self.assertEqual([r.text for r in job.children[1].children][-1], "+3 more")
        self.assertTrue((block / "studio" / "mind-map.excalidraw").is_file())

    def test_a_refresh_keeps_a_persons_node_and_words_and_updates_the_rest(self):
        block = work(self.root)
        run("from-work", block)
        md = block / "studio" / "mind-map.mindmap.md"
        text = md.read_text(encoding="utf-8")
        text = text.replace("t01_load · 2 runs, all done", "t01_load: the raw files")
        text = text.replace("<!-- @j01_build/t02_fit ", "<!-- @j01_build/t02_fit ").replace(
            "\n  - t02_fit", "\n    - ask the lab about r03\n  - t02_fit", 1)
        md.write_text(text, encoding="utf-8")
        (block / "j01_build" / "t01_load" / "runs" / "r03_c").mkdir()
        (block / "j01_build" / "t03_report").mkdir()
        rc, out = run("refresh", md)
        self.assertEqual(rc, 0, out)
        mm = MT.load(md)
        job = mm.root.children[0]
        self.assertEqual(job.text, "j01_build · 3 tasks · 9 runs")            # unedited: updated
        self.assertEqual(job.children[0].text, "t01_load: the raw files")     # a person's words: kept
        self.assertIn("ask the lab about r03", [c.text for c in job.children[0].children])
        self.assertIn("r03_c ⬜", [c.text for c in job.children[0].children])
        self.assertEqual(job.children[-1].text, "t03_report · 0 runs")

    def test_from_topic_writes_the_structured_side_mnn(self):
        topic = self.root / "studio" / "s04-fees"
        topic.mkdir(parents=True)
        (topic / "s04-fees.md").write_text(
            "s04 · Fees\n==========\n\n**Stage:** shaping\n\n**Topic:** what the firm charges. Two kinds of fee.\n\n"
            "**Feeds:** `reports/q02_fees/`.\n\nFiles\n-----\n\n```text\ns04-fees/\n```\n\nOpen\n----\n\n"
            "- who pays the court fee\n- (write here, or mark the drawing in red)\n", encoding="utf-8")
        rc, out = run("from-topic", topic)
        self.assertEqual(rc, 0, out)
        md = topic / "m04-fees.mindmap.md"
        mm = MT.load(md)
        self.assertEqual(mm.meta["built"], "from-topic .")
        self.assertEqual([c.text for c in mm.root.children], ["Topic", "Feeds", "Files", "Open"])
        self.assertEqual([c.text for c in mm.root.children[0].children], ["what the firm charges", "Two kinds of fee"])
        self.assertEqual([c.text for c in mm.root.children[3].children], ["who pays the court fee"])
        self.assertEqual(mm.root.note, ["**Stage:** shaping"])
        self.assertNotIn("m04-fees", " ".join(c.text for c in mm.root.children[2].children))
        for name in ("m04-fees.excalidraw", "m04-fees.png", "m04-fees.mindmap.html"):
            self.assertTrue((topic / name).is_file(), name)

    def test_a_built_map_keeps_within_two_hundred_words(self):
        root = MB.built(".", "root", [MB.built(f"b{i}", f"branch {i}", [MB.built(f"b{i}/{j}", "four words in here")
                                                                       for j in range(12)]) for i in range(6)])
        root.id = "root"
        mm = MT.MindMap({}, root)
        self.assertGreater(MB.words(mm), 200)
        MB.fit(mm)
        self.assertLessEqual(MB.words(mm), 200)
        self.assertTrue(any(c.text.startswith("+") for b in mm.root.children for c in b.children))


if __name__ == "__main__":
    unittest.main()
