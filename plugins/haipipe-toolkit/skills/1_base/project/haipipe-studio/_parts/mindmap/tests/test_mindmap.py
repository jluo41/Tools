"""haipipe-mindmap: the grammar, the map drawn as the draft's §1 Structure map, each in-place edit written into the
file, the builders, and the refresh that keeps a person's words."""
from __future__ import annotations

import io
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import mindmap  # noqa: E402
import mmbuild as MB  # noqa: E402
import mmhtml as MH  # noqa: E402
import mmmap as MM  # noqa: E402
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

    def kids(self, nid="root"):
        node, _ = MT.find(MT.load(self.md), nid)
        return [c.id for c in node.children]

    def text(self, nid):
        return MT.find(MT.load(self.md), nid)[0].text


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


class Map(Case):
    def test_the_map_is_html_drawn_as_the_drafts_structure_map(self):
        out = MM.fragment(self.md, "trip.mindmap.md")
        self.assertIn('<div class=mm-edit data-file="trip.mindmap.md">', out)
        self.assertIn('class="mm-node mm-root', out)
        self.assertIn("<strong>plan</strong>", out)                       # Markdown shown as Markdown
        self.assertIn("<code>EUR</code>", out)
        self.assertIn('title="the week after the deadline"', out)        # a note shows on hover, as §1's
        rows = re.findall(r'<div class=mm-row data-id="([^"]+)">', out)
        self.assertEqual(rows, ["root", "n01", "n02", "n03", "n04", "n05", "n06"])
        self.assertIn("fetch('/_board/mindmap'", out)
        self.assertNotIn("excalidraw", out)

    def test_a_node_can_hold_nodes_at_any_depth_down_to_its_leaves(self):
        deep = SOURCE.replace("  - May <!-- n05 -->", "  - May <!-- n05 -->\n    - week 2 <!-- n07 -->\n      - Monday <!-- n08 -->\n        - 9am <!-- n09 -->")
        self.md.write_text(deep, encoding="utf-8")
        out = MM.fragment(self.md, "trip.mindmap.md")
        self.assertIn('<div class=mm-row data-id="n09"><div class="mm-node mm-d3"', out)   # five levels below the root
        self.assertEqual([n.id for n, _p, d, _k in MT.walk(MT.load(self.md).root) if d == 5], ["n09"])

    def test_a_card_that_links_a_file_opens_it(self):
        (self.dir / "shot.png").write_bytes(b"png")
        self.md.write_text(SOURCE.replace("- Budget `EUR`", "- [shot.png](shot.png) and [gone.md](gone.md) - Budget `EUR`"),
                           encoding="utf-8")
        out = MM.fragment(self.md, "trip.mindmap.md", url_of=lambda f: "/open/" + f.name)
        self.assertIn('<a class=mm-open data-pop="shot.png" href="/open/shot.png"', out)    # a picture: 🖼, the pop-out
        self.assertIn('title="open shot.png">🖼</a>', out)
        self.assertNotIn("/open/gone.md", out)                                              # not on disk: no button
        self.assertIn('data-raw="[shot.png](shot.png) and [gone.md](gone.md) - Budget `EUR`"', out)   # typed as written
        self.assertIn(">shot.png and gone.md - Budget <code>EUR</code></span>", out)          # the card shows the words
        page = MH.page(MT.load(self.md))
        self.assertIn('href="shot.png"', page)                         # the static page links the file beside it

    def test_read_only_the_map_carries_no_editing(self):
        out = MM.draw(MT.load(self.md))
        self.assertNotIn("contenteditable", out)
        self.assertNotIn("/_board/mindmap", out)
        self.assertIn('data-id="n05"', out)

    def test_a_typed_bullet_gets_its_id_when_the_map_is_drawn(self):
        self.md.write_text(SOURCE.replace("- Budget", "- Food\n- Budget"), encoding="utf-8")
        MM.fragment(self.md, "trip.mindmap.md")
        self.assertEqual(self.kids(), ["n01", "n04", "n07", "n06"])

    def test_render_writes_the_static_page(self):
        rc, out = run("render", self.md)
        self.assertEqual(rc, 0, out)
        page = self.v["html"].read_text(encoding="utf-8")
        self.assertIn("<title>Trip · mind map</title>", page)
        self.assertIn('class="mm-node mm-root', page)
        self.assertIn("Free notes, <strong>kept</strong> as written.", page)
        self.assertNotIn("contenteditable", page)

    def test_the_page_renders_markdown_blocks(self):
        page = MH.blocks("## Head\n\n- one\n  - two\n\n```\ncode <x>\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |")
        self.assertIn("<h3>Head</h3>", page)
        self.assertIn("<ul><li>one<ul><li>two</li></ul></li></ul>", page)
        self.assertIn("code &lt;x&gt;", page)
        self.assertIn("<td>2</td>", page)


class Edit(Case):
    def act(self, **p):
        return MM.act(self.dir, {"file": "trip.mindmap.md", **p})

    def test_changed_words_are_written_into_the_file(self):
        code, res = self.act(what="text", id="n02", was="Lisbon", value="Lisbon, **three** days")
        self.assertEqual((code, res["ok"]), (200, True))
        self.assertEqual(self.text("n02"), "Lisbon, **three** days")
        self.assertEqual(res["html"], "Lisbon, <strong>three</strong> days")
        self.assertIn("three", self.v["html"].read_text(encoding="utf-8"))      # the static page follows

    def test_a_node_added_after_another_takes_the_next_id(self):
        code, res = self.act(what="add", parent="n01", after="n02", value="Coimbra")
        self.assertEqual(code, 200)
        self.assertEqual(res["id"], "n07")
        self.assertEqual(self.kids("n01"), ["n02", "n07", "n03"])
        code, _ = self.act(what="add", parent="n06", value="flights")      # ＋ on a leaf: its first child
        self.assertEqual(self.kids("n06"), ["n08"])

    def test_an_emptied_node_is_taken_out_and_its_children_move_up(self):
        code, _ = self.act(what="drop", id="n04", was="When", value="")
        self.assertEqual(code, 200)
        self.assertEqual(self.kids(), ["n01", "n05", "n06"])

    def test_a_node_dropped_onto_another_goes_before_it(self):
        self.assertEqual(self.act(what="move", id="n06", before="n02")[0], 200)
        self.assertEqual(self.kids("n01"), ["n06", "n02", "n03"])
        self.assertEqual(self.act(what="move", id="n03", parent="n04")[0], 200)       # onto a ＋: last under it
        self.assertEqual(self.kids("n04"), ["n05", "n03"])

    def test_a_node_cannot_go_under_itself(self):
        code, res = self.act(what="move", id="n01", parent="n02")
        self.assertEqual(code, 400)
        self.assertEqual(self.kids(), ["n01", "n04", "n06"])

    def test_words_changed_on_disk_since_the_page_showed_them_are_kept(self):
        self.md.write_text(SOURCE.replace("Lisbon", "Lisbon old town"), encoding="utf-8")
        code, res = self.act(what="text", id="n02", was="Lisbon", value="Lisboa")
        self.assertEqual(code, 409)
        self.assertTrue(res["reload"])
        self.assertEqual(self.text("n02"), "Lisbon old town")

    def test_a_read_only_host_and_a_path_outside_are_refused(self):
        self.assertEqual(MM.act(self.dir, {"file": "trip.mindmap.md", "what": "text"}, read_only=True)[0], 403)
        self.assertEqual(MM.act(self.dir, {"file": "../x.mindmap.md", "what": "text"})[0], 400)
        self.assertEqual(MM.act(self.dir, {"file": "trip.md", "what": "text"})[0], 400)

    def test_check_passes_and_names_a_duplicate_id(self):
        self.assertEqual(run("check", self.md)[0], 0)
        self.md.write_text(SOURCE.replace("<!-- n05 -->", "<!-- n02 -->"), encoding="utf-8")
        rc, out = run("check", self.md)
        self.assertEqual(rc, 1)
        self.assertIn("an id used twice: n02", out)


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
        self.assertEqual(len(job.children[1].children), 6)                    # every Run, none folded
        self.assertEqual(job.children[1].children[0].text, "r01_x ✅")
        self.assertTrue((block / "studio" / "mind-map.mindmap.html").is_file())

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
        files = [c.text for c in mm.root.children[2].children]
        self.assertEqual(files, ["[s04-fees.md](s04-fees.md)"])          # a file is a link its card opens
        self.assertTrue((topic / "m04-fees.mindmap.html").is_file())
        self.assertFalse(list(topic.glob("*.excalidraw")))


if __name__ == "__main__":
    unittest.main()
