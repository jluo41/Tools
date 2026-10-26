"""haipipe-mindmap: the grammar, the map drawn by the same code as a draft's §1 Structure map, each edit (the
payload §1's map sends) written into the file, the builders, and the refresh that keeps a person's words."""
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
import mapview as MV  # noqa: E402
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
    def test_the_map_is_the_drafts_structure_map_drawn_by_the_same_code(self):
        out = MM.fragment(self.md, "trip.mindmap.md")
        self.assertIn(MV.CSS, out)                                       # §1's own CSS and script, shared
        self.assertIn(MV.JS, out)
        self.assertIn('<div class=pm-edit data-task="trip.mindmap.md" data-file="trip.mindmap.md" '
                      'data-endpoint="/_board/mindmap">', out)
        self.assertIn('<div class="pm-node pm-root"><b>Trip plan</b>', out)
        self.assertIn('<p data-edit=arc data-raw="Why we go: rest."', out)  # the root's note, as §1's arc
        self.assertEqual(re.findall(r'<div class=pm-para data-p="([^"]+)">', out), ["n01", "n04", "n06"])
        self.assertEqual(re.findall(r'<li data-s="([^"]+)">', out), ["n02", "n03", "n05"])
        self.assertIn('<span class=pm-id>2</span><b data-edit=para data-raw="When"', out)
        self.assertIn('<span class=pm-s draggable=true>1.2</span>', out)   # a point's number, as §1's S1
        self.assertIn("Budget `EUR`", out)
        detail = re.search(r'<li data-s="n05">.*?<div class=pm-detail hidden>(.*?)<button', out, re.S).group(1)
        self.assertEqual(detail, "")                                    # no detail yet: ▸ opens an empty one to type

    def test_a_branch_hands_a_question_to_the_next_and_a_point_shows_its_role(self):
        self.md.write_text(SOURCE.replace("  the week after the deadline", "  → Then how much can we spend?\n"
                                          "  the week after the deadline").replace("  - May", "  - [month] May"),
                           encoding="utf-8")
        out = MM.fragment(self.md, "trip.mindmap.md")
        self.assertIn('<div class=pm-q><span data-edit=ask data-p="n04" data-raw="Then how much can we spend?"', out)
        self.assertIn('<span class=pm-role data-edit=role data-raw="month" contenteditable=plaintext-only spellcheck=false>month</span>', out)
        self.assertIn('<span class=pm-t data-edit=words data-raw="May"', out)

    def test_a_node_can_hold_nodes_at_any_depth_down_to_its_leaves(self):
        deep = SOURCE.replace("  - May <!-- n05 -->", "  - May <!-- n05 -->\n    - week 2 <!-- n07 -->\n      - Monday <!-- n08 -->\n        - 9am <!-- n09 -->")
        self.md.write_text(deep, encoding="utf-8")
        out = MM.fragment(self.md, "trip.mindmap.md")
        self.assertIn('<li data-s="n09"><span class=pm-s draggable=true>2.1.1.1.1</span>', out)   # five levels down
        self.assertEqual(out.count("<ul class=pm-sub>"), 3)

    def test_a_point_that_names_a_file_has_a_chip_and_its_detail_shows_a_picture(self):
        (self.dir / "shot.png").write_bytes(b"png")
        self.md.write_text(SOURCE.replace("  - Porto <!-- n03 -->", "  - [shot.png](shot.png) and [gone.md](gone.md) <!-- n03 -->\n"
                                          "    ![shot.png](shot.png)"), encoding="utf-8")
        out = MM.fragment(self.md, "trip.mindmap.md", url_of=lambda f: "/open/" + f.name)
        self.assertIn('<a class="pm-card pm-open" data-pop="shot.png" href="/open/shot.png"', out)
        self.assertNotIn("/open/gone.md", out)                          # not on disk: no chip
        self.assertIn(">shot.png and gone.md</span>", out)              # the line shows the words
        detail = re.search(r'<li data-s="n03">.*?<div class=pm-detail hidden>(.*?)<button', out, re.S).group(1)
        self.assertIn('<img src="/open/shot.png" alt="shot.png" loading=lazy>', detail)

    def test_read_only_the_map_carries_no_editing(self):
        out = MM.draw(MT.load(self.md), "", False)
        self.assertNotIn("contenteditable", out)
        self.assertNotIn("<li class=pm-add>", out)
        self.assertNotIn("<div class=pm-addp>", out)
        self.assertIn('<li data-s="n05">', out)

    def test_render_writes_the_static_page(self):
        rc, out = run("render", self.md)
        self.assertEqual(rc, 0, out)
        page = self.v["html"].read_text(encoding="utf-8")
        self.assertIn("<title>Trip · mind map</title>", page)
        self.assertIn('<div class="pm-node pm-root">', page)
        self.assertIn("Free notes, <strong>kept</strong> as written.", page)
        self.assertNotIn("contenteditable", page)

    def test_the_page_renders_markdown_blocks(self):
        page = MH.blocks("## Head\n\n- one\n  - two\n\n```\ncode <x>\n```\n\n| a | b |\n|---|---|\n| 1 | 2 |")
        self.assertIn("<h3>Head</h3>", page)
        self.assertIn("<ul><li>one<ul><li>two</li></ul></li></ul>", page)
        self.assertIn("code &lt;x&gt;", page)
        self.assertIn("<td>2</td>", page)


class Edit(Case):
    """Each edit is the payload a draft's §1 map sends; the mind map answers it into its file."""
    def act(self, **p):
        return MM.act(self.dir, {"task": "trip.mindmap.md", "file": "trip.mindmap.md", **p})

    def test_a_points_words_and_role_are_written_into_the_file(self):
        code, res = self.act(what="words", s="n02", was="Lisbon", value="Lisbon, **three** days")
        self.assertEqual((code, res["html"]), (200, "Lisbon, <strong>three</strong> days"))
        self.assertEqual(self.act(what="role", s="n02", was="", value="city")[0], 200)
        self.assertEqual(self.text("n02"), "[city] Lisbon, **three** days")
        self.assertIn("three", self.v["html"].read_text(encoding="utf-8"))      # the static page follows

    def test_a_branchs_name_its_question_and_the_roots_line(self):
        self.assertEqual(self.act(what="para", p="n04", was="When", value="When we go")[0], 200)
        self.assertEqual(self.act(what="ask", p="n04", was="", value="So what does it cost?")[0], 200)
        self.assertEqual(self.act(what="arc", was="Why we go: rest.", value="Why: rest, and sea.")[0], 200)
        mm = MT.load(self.md)
        n04 = MT.find(mm, "n04")[0]
        self.assertEqual((n04.text, n04.note), ("When we go", ["→ So what does it cost?", "the week after the deadline"]))
        self.assertEqual(mm.root.note, ["Why: rest, and sea."])

    def test_a_point_and_a_branch_added_where_they_go(self):
        code, res = self.act(what="add", p="n01", after="n02", value="Coimbra", role="maybe")
        self.assertEqual((code, res["s"]), (200, "n07"))
        self.assertEqual(self.kids("n01"), ["n02", "n07", "n03"])
        self.assertEqual(self.text("n07"), "[maybe] Coimbra")
        self.assertEqual(self.act(what="add", p="n06", after="", value="flights")[0], 200)   # the first under n06
        self.assertEqual(self.act(what="addpara", after="n04", value="Who")[0], 200)
        self.assertEqual(self.kids(), ["n01", "n04", "n09", "n06"])

    def test_a_dropped_point_takes_its_lines_with_it_up_a_level(self):
        self.md.write_text(SOURCE.replace("  - May <!-- n05 -->", "  - May <!-- n05 -->\n    - week 2 <!-- n07 -->"),
                           encoding="utf-8")
        self.assertEqual(self.act(what="drop", s="n05", was="May", value="")[0], 200)
        self.assertEqual(self.kids("n04"), ["n07"])

    def test_a_point_moved_into_another_branch_before_a_point(self):
        self.assertEqual(self.act(what="move", s="n05", p="n01", before="n03")[0], 200)
        self.assertEqual(self.kids("n01"), ["n02", "n05", "n03"])
        self.assertEqual(self.act(what="move", s="n02", p="n04")[0], 200)       # onto a branch: last in it
        self.assertEqual(self.kids("n04"), ["n02"])

    def test_a_detail_is_written_as_lines_under_its_bullet(self):
        code, _ = self.act(what="note", s="n02", was="", value="old town, **3** days\n- a list line\n![map](map.png)")
        self.assertEqual(code, 200)
        self.assertEqual(MT.find(MT.load(self.md), "n02")[0].note, ["old town, **3** days", "· a list line", "![map](map.png)"])
        self.assertEqual(self.kids("n02"), [])                              # a detail line never becomes a node

    def test_words_changed_on_disk_since_the_page_showed_them_are_kept(self):
        self.md.write_text(SOURCE.replace("Lisbon", "Lisbon old town"), encoding="utf-8")
        self.assertEqual(self.act(what="words", s="n02", was="Lisbon", value="Lisboa")[0], 409)
        self.assertEqual(self.text("n02"), "Lisbon old town")

    def test_a_read_only_host_and_a_path_outside_are_refused(self):
        self.assertEqual(MM.act(self.dir, {"task": "trip.mindmap.md", "what": "words"}, read_only=True)[0], 403)
        self.assertEqual(MM.act(self.dir, {"task": "../x.mindmap.md", "what": "words"})[0], 400)
        self.assertEqual(MM.act(self.dir, {"task": "trip.md", "what": "words"})[0], 400)

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

    def test_a_long_leaf_is_short_on_its_card_and_whole_in_its_detail(self):
        topic = self.root / "studio" / "s05-pics"
        topic.mkdir(parents=True)
        (topic / "s05-pics.md").write_text("s05 · Pics\n==========\n\n**Topic:** every kind of element the work theme draws "
                                           "today, side by side, so one look is picked.\n", encoding="utf-8")
        (topic / "shot.png").write_bytes(b"png")
        (topic / "Files.md").write_text("x")
        (topic / "s05-pics.md").write_text((topic / "s05-pics.md").read_text() + "\nFiles\n-----\n\n", encoding="utf-8")
        run("from-topic", topic)
        mm = MT.load(topic / "m05-pics.mindmap.md")
        lf = mm.root.children[0].children[0]
        self.assertEqual(lf.text, "every kind of element the work theme …")
        self.assertEqual(lf.note, ["every kind of element the work theme draws today, side by side, so one look is picked."])
        shot = next(c for c in mm.root.children[1].children if "shot.png" in c.text)
        self.assertEqual((shot.text, shot.note), ("[png] [shot.png](shot.png)", ["![shot.png](shot.png)"]))
        (topic / "s05-pics.md").write_text((topic / "s05-pics.md").read_text().replace("every kind", "each kind"))
        run("refresh", topic / "m05-pics.mindmap.md")                       # the builder's words change twice:
        (topic / "s05-pics.md").write_text((topic / "s05-pics.md").read_text().replace("each kind", "every sort"))
        run("refresh", topic / "m05-pics.mindmap.md")                       #   both refreshes take them
        mm = MT.load(topic / "m05-pics.mindmap.md")
        lf = mm.root.children[0].children[0]
        self.assertEqual(lf.text, "every sort of element the work theme …")
        lf.note = ["my own detail"]                                         # a person's detail survives a refresh
        MT.save(mm, topic / "m05-pics.mindmap.md")
        run("refresh", topic / "m05-pics.mindmap.md")
        self.assertEqual(MT.find(MT.load(topic / "m05-pics.mindmap.md"), lf.id)[0].note, ["my own detail"])

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
        self.assertEqual(mm.root.children[0].children[0].note, [])          # short already: no detail
        self.assertEqual([c.text for c in mm.root.children[3].children], ["who pays the court fee"])
        self.assertEqual(mm.root.note, ["**Stage:** shaping"])
        files = [c.text for c in mm.root.children[2].children]
        self.assertEqual(files, ["[md] [s04-fees.md](s04-fees.md)"])          # a file is a link its card opens
        self.assertTrue((topic / "m04-fees.mindmap.html").is_file())
        self.assertFalse(list(topic.glob("*.excalidraw")))


if __name__ == "__main__":
    unittest.main()
