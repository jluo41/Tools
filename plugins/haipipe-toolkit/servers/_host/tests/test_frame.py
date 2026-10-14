"""The base frame (servers/workbench/frame.py): the levels, the six Spaces, the third row, the Runs
panel, the vanilla defaults read from disk, a theme laid over them, and the route."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from html import unescape
from urllib.parse import parse_qs, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402


def project(tmp: str) -> Path:
    """A Project with one work Block: a Question, a drawing, one Job, one Task with a hard and a
    soft Run, code, a notebook and a delivery."""
    root = Path(tmp)
    block = root / "Project" / "tasks" / "b01_topic"
    task = block / "j01_job" / "t01_task"
    for d in (block / "studio" / "s01-flow", block / "reports" / "q01_ask", block / "delivery" / "d01-report",
              task / "scripts", task / "notebooks", task / "runs" / "r01_fit", task / "runs" / "run-build-t01"):
        d.mkdir(parents=True)
    (block / "b01_topic.md").write_text("# b01 · Topic\n\nboard-kind: task-block\nspine: a topic\n")
    (block / "studio" / "s01-flow" / "flow.excalidraw").write_text("{}")
    (block / "reports" / "q01_ask" / "q01_ask.md").write_text(
        "# What is asked?\n\nanswer-status: open\n\n## Opening\n\nOne line that answers it.\n")
    (block / "studio" / "s01-flow" / "s01-flow.md").write_text(
        "s01 · Flow\n=====\n\n**Topic:** how it flows.\n\n**Feeds:** `reports/q01_ask/`.\n\ns01-D01 · Proposed: one.\n")
    (block / "j01_job" / "j01_job.md").write_text("# j01 · Job\n\nanswers: Q01\n")
    (block / "delivery" / "d01-report" / "index.html").write_text("<p>x</p>")
    (task / "t01_task.md").write_text("# t01 · Task\n\ngoal: one thing\n\n## Plan\n\ninputs → worker → Runs\n")
    (task / "scripts" / "worker.py").write_text("print(1)\n")
    (task / "notebooks" / "r01_fit.ipynb").write_text("{}")
    (task / "runs" / "r01_fit" / "run.yaml").write_text("run: r01_fit\nkind: hard\ntype: [fit, evaluate]\nstatus: done\n")
    (task / "runs" / "run-build-t01" / "run.yaml").write_text("run: run-build-t01\nkind: soft\ntype: build\nstatus: open\n")
    return root


def tiny_deck(path: Path) -> Path:
    """A one-slide .pptx written by hand: a rounded box with text, an arrow and a picture."""
    A = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    P = 'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    R = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    rel = lambda rid, kind, target: (f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/'
                                     f'2006/relationships/{kind}" Target="{target}"/>')
    rels = lambda *r: ('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       + "".join(r) + "</Relationships>")
    box = ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="box"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm>'
           '<a:off x="127000" y="127000"/><a:ext cx="2540000" cy="1270000"/></a:xfrm><a:prstGeom prst="roundRect">'
           '<a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="1F3A68"/></a:solidFill></p:spPr><p:txBody>'
           '<a:bodyPr anchor="ctr"/><a:p><a:pPr algn="ctr"/><a:r><a:rPr sz="2400" b="1"><a:solidFill>'
           '<a:srgbClr val="FFFFFF"/></a:solidFill></a:rPr><a:t>Prep AI &amp; you</a:t></a:r></a:p></p:txBody></p:sp>')
    arrow = ('<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="3" name=""/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm>'
             '<a:off x="2794000" y="762000"/><a:ext cx="1270000" cy="0"/></a:xfrm><a:prstGeom prst="straightConnector1">'
             '<a:avLst/></a:prstGeom><a:ln w="25400"><a:solidFill><a:srgbClr val="C92A2A"/></a:solidFill>'
             '<a:tailEnd type="triangle"/></a:ln></p:spPr></p:cxnSp>')
    pic = ('<p:pic><p:nvPicPr><p:cNvPr id="4" name=""/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill>'
           '<a:blip r:embed="rImg"/><a:stretch/></p:blipFill><p:spPr><a:xfrm><a:off x="4318000" y="127000"/>'
           '<a:ext cx="1270000" cy="1270000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("ppt/presentation.xml", f'<p:presentation {P} {R}><p:sldIdLst><p:sldId id="256" r:id="rS1"/>'
                   '</p:sldIdLst><p:sldSz cx="9144000" cy="5143500"/></p:presentation>')
        z.writestr("ppt/_rels/presentation.xml.rels", rels(rel("rS1", "slide", "slides/slide1.xml")))
        z.writestr("ppt/slides/slide1.xml", f'<p:sld {P} {A} {R}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" '
                   f'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/>{box}{arrow}{pic}</p:spTree>'
                   '</p:cSld></p:sld>')
        z.writestr("ppt/slides/_rels/slide1.xml.rels", rels(rel("rImg", "image", "/ppt/media/image1.png")))
        z.writestr("ppt/media/image1.png", b"\x89PNG\r\n\x1a\nfake")
    return path


class LadderTest(unittest.TestCase):
    def test_a_folder_knows_its_level_its_chain_and_its_theme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            self.assertEqual(frame.level_of(task), "Task")
            self.assertEqual(sorted(frame.chain(task, root)), ["Block", "Job", "Task"])
            self.assertEqual(frame.theme_of(task, root), "work")          # tasks/ reads as the work theme
            self.assertEqual([r["type"] for r in frame.runs_of(task)], ["fit", "build"])
            tools = root / "Tools" / "blueprints" / "b02_workbench"           # not inside a Project
            tools.mkdir(parents=True)
            (tools / "board.md").write_text("# b02\n")
            self.assertEqual(frame.theme_of(tools, root), "vanilla")



class OptionTest(unittest.TestCase):
    # A theme labels and groups the Job ▾ / Task ▾ options (Theme.option, b12 s32 261008)
    def test_a_theme_labels_and_groups_the_dropdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            job = root / "Project/tasks/b01_topic/j01_job"
            (job / "t02_other").mkdir()
            task = job / "t01_task"
            theme = frame.Theme(option=lambda f: (f"Task · {f.name[:3]}", "steps") if f.name == "t01_task" else None)
            row = frame._level_row(theme, root, task, "Task", "Description")
            self.assertIn('<optgroup label="steps">', row)
            self.assertIn(">Task · t01</option>", row)
            self.assertIn(">t02_other</option>", row)                  # None: the folder name as on disk (b10 s32-D15)
            plain = frame._level_row(frame.VANILLA, root, task, "Task", "Description")
            self.assertNotIn("optgroup", plain)
            self.assertIn('title="t01_task" selected>t01_task</option>', plain)     # the folder name, as on disk


class FillTagTest(unittest.TestCase):
    # a theme's Run name takes the folder's own tag, as the base's buttons do (b17 s32 261008)
    def test_a_placeholder_for_the_folders_level_is_filled(self):
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/t01_fit")), "run-plan-t01")
        self.assertEqual(frame.fill_tag("run-face-<jNN>", Path("x/t01_fit")), "run-face-<jNN>")
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/Design-A")), "run-plan-<tNN>")

    def test_a_themes_own_view_is_not_shadowed_by_a_page_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            out = frame.with_page_views({"Audience Report": frame.Space(subspaces=("Draft", "Report"), open="Draft")},
                                        "Task", task, root, "Draft", {"Description": "Face", "Audience Report": "Report",
                                        "Work Details": "Work", "Runs": "All", "Delivery": "Files"})
            self.assertEqual(out["Audience Report"].subspaces, ("Draft", "Report"))
            self.assertNotIn("page-view", out["Audience Report"].html)

    def test_the_work_themes_draft_shows_its_own_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            (task / "draft").mkdir()
            (task / "draft" / "t01-draft-v1.md").write_text("# plan\n")
            theme = frame.themes()["work"]
            out = frame.spaces_for(theme, "Task", task, root, "Draft")
            self.assertNotIn("page-view", out["Audience Report"].html)
            self.assertIn("t01-draft-v1.md", out["Audience Report"].html)

class LevelPatternTest(unittest.TestCase):
    # A theme names its own Job and Task folders (Theme.level_patterns, b03 261007): a paper's version
    # groups Ba-<desk>-Main and its Sections S-<desk>-<N>-<slug> climb the ladder unrenamed.
    def paper(self, tmp: str) -> Path:
        root = Path(tmp)
        board = root / "Project-X" / "paper" / "Paper-Demo"
        for d in (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "draft", board / "A1-Story" / "StoryA-x",
                  board / "Ba-Desk-Main" / "notes"):
            d.mkdir(parents=True)
        (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
        (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
        return root

    def test_a_theme_names_its_job_and_task_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.paper(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            group, section = board / "Ba-Desk-Main", board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            saved = dict(frame._PATTERNS)
            frame._PATTERNS.clear()
            frame._PATTERNS.update({"paper": {"Job": r"^B[a-z]-", "Task": r"^S-"}, "work": {}})
            try:
                self.assertEqual(frame.level_of(board), "Block")
                self.assertEqual(frame.level_of(group), "Job")
                self.assertEqual(frame.level_of(section), "Task")
                self.assertIsNone(frame.level_of(board / "A1-Story"))           # not declared
                self.assertIsNone(frame.level_of(group / "notes"))              # under a Job, not a Section
                self.assertIsNone(frame.level_of(section / "draft"))            # inside a Task
                self.assertEqual(frame.children(board, "Block"), [group])
                self.assertEqual(frame.children(group, "Job"), [section])
                self.assertEqual(frame.chain(section, root), {"Task": section, "Job": group, "Block": board})
                self.assertEqual(frame.theme_of(section, root), "paper")
                page = frame.render(frame.Theme(name="paper", label="Paper"), root, section)
                self.assertIn("S-Desk-Main-1-Intro", page)
                self.assertNotIn('<select disabled aria-label="Task"', page)  # the Task tab is live
            finally:
                frame._PATTERNS.clear()
                frame._PATTERNS.update(saved)

    def test_a_theme_with_no_patterns_reads_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "Bz-group").mkdir()
            self.assertIsNone(frame.level_of(block / "Bz-group"))               # the work theme declares none
            self.assertEqual([p.name for p in frame.children(block, "Block")], ["j01_job"])


class PageTaskTest(unittest.TestCase):
    # A Page Task on the frame (frame.page_task_spaces, b03 s13 / b16 s13): the Page's own views, embedded.
    def test_a_page_task_opens_the_pages_views_in_the_six_spaces(self):
        from urllib.parse import parse_qs, urlparse
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "draft" / "records").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
            (section / "draft" / "records" / "S-Desk-Main-1-Intro-requirement.md").write_text("V1 · at most 900 words\n")
            spaces = frame.page_task_spaces(section, root)
            self.assertEqual({k: v.subspaces for k, v in spaces.items()}, frame.PAGE_TASK_SUBS)
            src = re.search(r'src="([^"]+)"', spaces["Audience Report"].html).group(1)
            q = parse_qs(urlparse(src.replace("&amp;", "&")).query)
            self.assertEqual(urlparse(src).path, "/_board/draft")
            self.assertEqual((q["path"][0], q["file"][0], q["embed"][0], q["space"][0], q["view"][0]),
                             ("Project-X/paper/Paper-Demo/board.md", "Ba-Desk-Main/S-Desk-Main-1-Intro/S-Desk-Main-1-Intro.md",
                              "1", "bullet", "table"))
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "draft-bibliography").mkdir(parents=True)
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "S-Desk-Main-1-Intro.tex").write_text("x")
            (board / "delivery" / "Ba-Desk-Main/S-Desk-Main-1-Intro" / "latex" / "draft-bibliography" / "S-Desk-Main-1-Intro.bib").write_text("x")
            runs = frame.page_task_spaces(section, root)["Runs"]               # the Page Runs view, embedded (s13)
            self.assertEqual((runs.subspaces, runs.page), ((), True))
            self.assertIn("/_board/runs?", runs.html)
            self.assertIn("embed=1", runs.html)
            deliv = frame.page_task_spaces(section, root)["Delivery"]          # item cards, no third row (s13 1b)
            self.assertEqual((deliv.subspaces, deliv.page), ((), True))
            self.assertIn("<h2>Deliveries</h2>", deliv.html)                    # one card per kind, its result inside
            self.assertIn("📄 LaTeX", deliv.html)
            self.assertIn("S-Desk-Main-1-Intro.pdf is not compiled yet; the piece:", deliv.html)
            self.assertIn("draft-bibliography/S-Desk-Main-1-Intro.bib", deliv.html)
            self.assertIn("not built yet: run Build", deliv.html)                # Word, Web … not built
            self.assertEqual([k["label"] for k in deliv.run_types], ["run-delivery-<target>", "run-check-<page>"])
            self.assertTrue(all(isinstance(x, str) and not x.startswith("[") for k in deliv.run_types for x in k["skills"]))
            merged = frame.spaces_for(frame.Theme(name="paper", spaces=lambda *a: frame.page_task_spaces(section, root)),
                                      "Task", section, root)["Delivery"]
            self.assertEqual((merged.subspaces, [k["label"] for k in merged.run_types]),
                             ((), ["run-delivery-<target>", "run-check-<page>"]))
            self.assertIn("tab=supporting", frame.page_task_spaces(section, root, "Evidence-Supporting")["Work Details"].html)
            self.assertIn("at most 900 words", frame.page_task_spaces(section, root, "Requirement")["Description"].html)
            self.assertIn("-requirement.md", frame.page_task_spaces(section, root, "Records")["Description"].html)
            self.assertIn("No plan yet", frame.page_task_spaces(section, root, "Plan")["Description"].html)
            self.assertEqual(spaces["Description"].html, "")              # Scope: the vanilla face and fields

    def test_a_page_task_reads_in_the_audience_report_and_works_in_work_details(self):
        # b16 s13 Decided 4-5 (JL 261007): Table and Reading carry no run types; Questions asks and
        # answers; each Work Details view has its own run cards; Requirement carries the rubric
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            section = board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            (section / "reports" / "q01_why").mkdir(parents=True)
            (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
            (section / "reports/q01_why/q01_why.md").write_text("# Why this order?\n\nanswer-status: open\n")
            theme = frame.themes()["paper"]

            def runs(sub, space):
                spaces = json.loads(frame.frame_json(theme, root, section, sub))["spaces"]
                return next(s["run_types"] for s in spaces if s["name"] == space)
            self.assertEqual(runs("Table", "Audience Report"), [])
            self.assertEqual(runs("Reading", "Audience Report"), [])
            page = frame.render(theme, root, section, "Audience Report", "Table")
            self.assertNotIn("read only: its content is changed", page)   # no note in the Runs panel (JL 261008)
            self.assertEqual(runs("Questions", "Audience Report"), ["run-ask-<qNN>", "run-report-<qNN>"])   # named by its Run
            self.assertEqual(runs("Draft-Scratch", "Work Details"),
                             ["run-scratch-<target>", "run-structure-<slug>", "run-<value|display|citation>-<slug>"])
            self.assertEqual(runs("Draft-Revise", "Work Details"),
                             ["run-section-<slug>", "run-paragraph-<slug>", "run-revise-<target>", "run-section-<slug>"])
            self.assertEqual(runs("Evidence-Citation", "Work Details"), ["run-citation-<slug>"])
            self.assertEqual([r.split("-")[:2] for r in runs("Scope", "Description")], [["run", "face"]])
            spaces = frame.spaces_for(theme, "Task", section, root, "Questions")
            self.assertIn("Why this order?", spaces["Audience Report"].html)
            self.assertIn("Rubric", frame.page_task_spaces(section, root, "Requirement")["Description"].html)

    def test_a_theme_may_add_its_own_views_after_the_pages(self):
        # b16 s13 (JL 261007): paper adds Reviews after Table · Reading · Questions; the Space stays the
        # theme's, so the base's extra Page-view tabs do not come back and its run types are kept as set
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            section = root / "Project-X/paper/Paper-Demo/Ba-Desk-Main/S-Desk-Main-1-Intro"
            section.mkdir(parents=True)
            (section.parents[1] / "board.md").write_text("# Paper\n\ndialect: paper\n")
            (section / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")

            def spaces(level, folder, root, sub):
                out = frame.page_task_spaces(folder, root, sub)
                ar = out["Audience Report"]
                out["Audience Report"] = frame.Space(html=ar.html, open=ar.open, run_types=ar.run_types,
                                                     subspaces=ar.subspaces + ("Reviews",))
                return out
            theme = frame.Theme(name="paper", label="Paper", spaces=spaces)
            ar = frame.spaces_for(theme, "Task", section, root)["Audience Report"]
            self.assertEqual(ar.subspaces, frame.PAGE_TASK_SUBS["Audience Report"] + ("Reviews",))
            self.assertEqual(ar.run_types, ())
            self.assertTrue(frame.lays_out_page("Audience Report", ar.subspaces))
            self.assertFalse(frame.lays_out_page("Audience Report", ("Reviews", "Table")))

    def test_the_page_view_embeds_without_its_own_chrome(self):
        from live.outline import EMBED_HTML
        self.assertIn("wb-embed", EMBED_HTML)
        for hidden in (".spaces", ".space-split>.runs-panel", ".draft-mode-switcher", "body>header"):
            self.assertIn(hidden, EMBED_HTML)


class ClaimTest(unittest.TestCase):
    # Theme.claims (261007): a theme reads a Block by what it holds, though its Theme folder names
    # another (a labeling Block with schema.yaml kept in tasks/); a failing check claims nothing.
    def test_a_theme_claims_a_block_by_what_it_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            other = root / "Project/tasks/b02_schema"
            other.mkdir()
            (other / "board.md").write_text("# b02\n\nboard-kind: task-block\n")
            (other / "schema.yaml").write_text("question: placeholder\n")
            claiming = frame.Theme(name="labeling", claims=lambda b: (b / "schema.yaml").is_file())
            broken = frame.Theme(name="broken", claims=lambda b: 1 / 0)
            saved = frame.themes
            frame.themes = lambda: {"vanilla": frame.VANILLA, "broken": broken, "labeling": claiming}
            frame._CLAIMS.clear()
            try:
                self.assertEqual(frame.theme_of(other, root), "labeling")
                self.assertEqual(frame.theme_of(block, root), "work")          # no claim: its Theme folder
            finally:
                frame.themes = saved
                frame._CLAIMS.clear()


class FrameTest(unittest.TestCase):
    def test_delivery_is_the_blocks_with_a_part_per_source_and_links_down(self):
        # b10 s03-D06 (JL 261011: "for the section, we will do not have the related studio and delivery";
        # "also for the Jobs"): one Delivery, the Block's; a Job or Task picks its part and links back down
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            task = block / "j01_job/t01_task"
            (block / "delivery/j01_job/t01_task/latex").mkdir(parents=True)
            (block / "delivery/j01_job/t01_task/latex/t01_task.tex").write_text("x", encoding="utf-8")
            (block / "delivery/j01_job/report.pdf").write_bytes(b"x")
            page = frame.render(frame.VANILLA, root, block, "Delivery")
            table = page.split("<h3>By source</h3>", 1)[1]
            self.assertIn(frame._e(frame.href(task, root, frame.VANILLA, "Delivery")), table)   # to the part
            self.assertIn(frame._e("/_board/workbench?path=Project%2Ftasks%2Fb01_topic%2Fj01_job%2Ft01_task"), table)
            self.assertIn("└ ", table)                                                       # a Task under its Job
            self.assertEqual(re.findall(r"<td>(\d+)</td>", table), ["1", "1"])              # a Job's own file only
            for folder, picked in ((block / "j01_job", "j01_job"), (task, "j01 › t01_task")):     # folder names (s32-D15)
                with self.subTest(folder=folder.name):
                    page = frame.render(frame.VANILLA, root, folder, "Delivery")
                    parts = re.search(r'<nav class="row subs delivery-parts">(.*?)</nav>', page).group(1)
                    self.assertEqual(re.findall(r'aria-current="true">([^<]+)</a>', parts), [picked])
                    self.assertIn("Its part of the Block's Delivery", page)
                    self.assertIn("· Delivery · <span class=lv>b01</span>", page)

    def test_a_deliverable_is_one_item_with_its_lanes_and_versions(self):
        # JL 261014: "for the delivery, I think we just make the item to be the same ... all of them should one
        # Delivery Item, and within it, we can see different versions"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            shutil.rmtree(block / "delivery")
            slide, render = block / "delivery/slide", block / "delivery/render"
            slide.mkdir(parents=True), render.mkdir(parents=True)
            for n, name in enumerate(("Deck-v1", "Deck-v2", "Deck-Visual-v3")):
                f = tiny_deck(slide / f"{name}.pptx")
                os.utime(f, (1_700_000_000 + n * 100,) * 2)
            (render / "Deck-Visual-v3.png").write_bytes(b"png")                       # its render: same version
            os.utime(render / "Deck-Visual-v3.png", (1_700_000_300,) * 2)
            sec = block / "delivery/j01_job/t01_task"
            for lane, files in (("web", ("index.html",)), ("word", ("t01_task.docx", "t01_task.pdf")),
                                ("latex", ("t01_task.pdf",))):
                (sec / lane).mkdir(parents=True)
                for name in files:
                    (sec / lane / name).write_bytes(b"x")
            (block / "delivery/word").mkdir()
            (block / "delivery/word/Paper.docx").write_bytes(b"x")
            (block / "delivery/word/Paper-SI.docx").write_bytes(b"x")              # no number: its own item
            items = {i["title"]: i for i in frame.delivery_items(block)}
            self.assertEqual(sorted(items), ["Deck", "Paper", "Paper-SI", "t01_task"])
            deck = items["Deck"]
            self.assertEqual([v["label"] for v in deck["versions"]], ["Visual-v3", "v2", "v1"])
            self.assertEqual([f.name for f in deck["versions"][0]["files"]], ["Deck-Visual-v3.pptx", "Deck-Visual-v3.png"])
            self.assertEqual(items["t01_task"]["fixed"], ["PDF", "Word", "Web page"])     # three lanes, one item
            self.assertEqual(items["t01_task"]["source"], "j01_job › t01_task")
            page = frame.render(frame.VANILLA, root, block, "Delivery")
            card = page.split('data-studio-key="Deck"', 1)[1].split("</details>", 1)[0]
            self.assertIn("3 versions, newest Visual-v3", card)
            self.assertEqual(re.findall(r'data-dv="(\d)" aria-pressed="(\w+)"', card),
                             [("0", "true"), ("1", "false"), ("2", "false")])
            self.assertIn('<img class=related-img loading=lazy alt="Deck-Visual-v3.png"', card)   # the render first
            self.assertIn(frame._e(frame.ROUTE + "?view=pptx&path=Project%2Ftasks%2Fb01_topic%2Fdelivery%2Fslide%2F"
                                   "Deck-v2.pptx"), card)                                    # else the deck, drawn
            self.assertIn('<div class=dv-pane data-dv="1" hidden>', card)
            self.assertIn("PDF · latex ↗", page)                                            # two PDFs: by lane

    def test_related_versions_fold_into_the_item_that_has_a_row(self):
        # JL 261014: "一个东西，我们会有一个 version 又一个 version ... 怎么去比较好地去 handle that?" The same rule as Delivery
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "Project/work/b01_topic"
            (block / "related/files").mkdir(parents=True)
            for n, name in enumerate(("Proposal-v1.docx", "Proposal-v2.docx", "Proposal-v3.pptx")):
                (block / "related/files" / name).write_bytes(b"x")
                os.utime(block / "related/files" / name, (1_700_000_000 + n * 100,) * 2)
            (block / "related/files/Budget.xlsx").write_bytes(b"x")
            (block / "related/files/Budget.pdf").write_bytes(b"x")                 # one name, two formats: apart
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
                "| file | 2026-10-01 | The proposal | `files/Proposal-v1.docx` | s01 | IRB |\n", encoding="utf-8")
            items = frame.related_items(block)
            self.assertEqual([i["title"] for i in items], ["The proposal", "Budget.pdf", "Budget.xlsx"])
            item = items[0]
            self.assertEqual([v["label"] for v in item["versions"]], ["v3", "v2", "v1"])    # newest first
            self.assertEqual(item["groups"], ["files", "IRB"])                             # the row's, kept
            self.assertIn("3 versions", item["meta"])
            html_ = frame.related_view(block, Path(tmp)).html
            self.assertIn('class="row dv-vers"', html_)
            self.assertIn(frame._e("view=pptx&path=Project%2Fwork%2Fb01_topic%2Frelated%2Ffiles%2FProposal-v3.pptx"),
                          html_)                                                            # a deck previews here too

    def test_a_deck_is_drawn_slide_by_slide_from_its_package(self):
        # JL 261014: "could we do the preview of the slide as well?"
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = tiny_deck(root / "deck.pptx")
            page = frame.pptx_preview(deck, root)
            self.assertIn("deck.pptx · read from the deck package: 1 slide · 1 pictures", page)
            self.assertIn('viewBox="0 0 720.00 405.00"', page)                       # 9,144,000 EMU = 720 pt
            self.assertIn('fill="#1f3a68"', page)                                    # the box, its colour
            self.assertIn('translate(10.00 10.00)', page)
            self.assertIn("Prep AI &amp; you</span>", page)                           # its text, escaped
            self.assertIn("font-size:24.00px;font-weight:700;color:#ffffff", page)
            self.assertIn('stroke="#c92a2a" stroke-width="2.00"', page)               # the arrow
            self.assertIn('marker-end="url(#pm0)"', page)
            self.assertIn(frame._e("?view=pptx&path=deck.pptx&media=ppt%2Fmedia%2Fimage1.png"), page)
            self.assertNotIn("base64", page)                                         # pictures by link, not inlined
            self.assertEqual(frame.pptx_media(deck, "ppt/media/image1.png"), (b"\x89PNG\r\n\x1a\nfake", "image/png"))
            self.assertIsNone(frame.pptx_media(deck, "ppt/slides/slide1.xml"))      # only pictures leave the package

    def test_a_related_item_is_grouped_by_its_kind(self):
        # JL 261013 (the groups are "things like meeting, email, paper"): a kept file sits under its subfolder,
        # a row kept as a web link under its kind; the group cell still adds more (b10 s04-D08)
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "Project/paper/Paper-X"
            (block / "related/paper").mkdir(parents=True)
            (block / "related/paper/smith2024.pdf").write_bytes(b"%PDF-1.4")
            (block / "related/meetings").mkdir()
            (block / "related/meetings/2026-10-10-1800 kickoff.md").write_text("# kickoff\n", encoding="utf-8")
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
                "| paper | 2024 | Smith 2024 | `paper/smith2024.pdf` | s01 |  |\n"
                "| paper | 2025 | Jones 2025 | https://doi.org/10.1/x | s01 |  |\n"
                "| meeting | 2026-10-10 | Kickoff | `meetings/2026-10-10-1800 kickoff.md` | s01 | IRB |\n",
                encoding="utf-8")
            groups = {i["title"]: i["groups"] for i in frame.related_items(block)}
            self.assertEqual(groups["Smith 2024"], ["paper"])
            self.assertEqual(groups["Jones 2025"], ["paper"])
            self.assertEqual(groups["Kickoff"], ["meetings", "IRB"])

    def test_related_folds_inside_the_studio_at_every_level(self):
        # b10 s04, JL 261011: Related is the Studio's second folding part, under the topic cards
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "related/meetings").mkdir(parents=True)
            (block / "related/meetings/2026-10-10-1800 kickoff.md").write_text("# kickoff\n", encoding="utf-8")
            (block / "related/files").mkdir()
            (block / "related/files/draft.docx").write_bytes(b"x")
            (block / "related/related.md").write_text(
                "| kind | date | item | link | feeds |\n|---|---|---|---|---|\n"
                "| meeting | 2026-10-10 | Kickoff | `meetings/2026-10-10-1800 kickoff.md` | s01 |\n"
                "| paper | 2024 | A paper | https://example.org/paper | q01 |\n", encoding="utf-8")
            for folder in (block, block / "j01_job/t01_task"):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, "Related")
                    self.assertIn("<details class=studio-related id=studio-related open>", page)  # a Related link unfolds it
                    self.assertIn("related/ · 2 items · meeting 1 · paper 1", page)
                    self.assertNotIn('<nav class="row subs">', page)
                    self.assertIn("Kickoff", page)
                    self.assertIn("A paper", page)
                    self.assertIn("/_board/page?path=%2FProject%2Ftasks%2Fb01_topic%2Frelated%2Fmeetings", page)
                    self.assertIn("example.org/paper ↗", page)
                    # the Studio's group bar; a subfolder is a group of its files (s04-D08, JL 261011)
                    self.assertNotIn("related-group", page)
                    bar = re.search(r'data-group-kind=related data-group-noun=item>(.*?)</nav>', page).group(1)
                    self.assertEqual(re.findall(r'data-studio-tag="([^"]*)"', bar),
                                     ["__current__", "files", "meetings", "paper"])
                    self.assertIn('meetings <span class=tag-count>1</span>', bar)
                    self.assertIn('paper <span class=tag-count>1</span>', bar)            # the web link, by its kind
                    self.assertNotIn("Untagged", bar)
                    self.assertIn('<span class=chip data-tag="meetings">meetings</span>', page)  # no ×: the folder
                    self.assertIn("class=grp-new", bar)
                    self.assertIn("related/files/draft.docx · no row yet", page)   # the sent file has no row
                    self.assertIn("files/draft.docx", page)
                    # a Word file opens on its preview, read from its package (frame.docx_preview)
                    self.assertIn(frame._e("/_board/workbench?view=docx&path=Project%2Ftasks%2Fb01_topic%2Frelated"
                                           "%2Ffiles%2Fdraft.docx"), page)
                    self.assertIn("run-add-related-", page)
                    studio = frame.render(frame.VANILLA, root, folder, "Idea Studio")
                    self.assertIn("<details class=studio-related id=studio-related>", studio)  # folded by default
                    self.assertIn("Kickoff", studio)
                    old = frame.render(frame.VANILLA, root, folder, "Description", "Related")
                    self.assertIn("<details class=studio-related id=studio-related open>", old)

    def test_a_word_file_previews_from_its_package(self):
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            doc = root / "Project/tasks/b01_topic/related/materials/form.docx"
            doc.parent.mkdir(parents=True)
            w = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
            with zipfile.ZipFile(doc, "w") as z:
                z.writestr("word/document.xml", f'<w:document {w}><w:body>'
                           '<w:p><w:commentRangeStart w:id="0"/><w:r><w:t>Your text here</w:t></w:r></w:p>'
                           '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>in a cell</w:t></w:r><w:commentRangeEnd w:id="0"/>'
                           '</w:p></w:tc></w:tr></w:tbl></w:body></w:document>')
                z.writestr("word/comments.xml", f'<w:comments {w}><w:comment w:id="0" w:author="GG">'
                           '<w:p><w:r><w:t>one comment</w:t></w:r></w:p></w:comment></w:comments>')
            page = frame.docx_preview(doc, root)
            self.assertIn("Your text here", page)
            self.assertIn("in a cell", page)                  # a table's text is kept
            self.assertIn("1 comments", page)                 # a comment over two blocks keeps its card
            self.assertIn("one comment", page)

    def test_an_email_previews_as_it_came(self):
        # JL 261011: "the related can have /emails as well"; an .eml opens on its headers and its text
        from email.message import EmailMessage
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            mail = block / "related/emails/2026-10-09-0900 IRB question.eml"
            mail.parent.mkdir(parents=True)
            msg = EmailMessage()
            msg["From"], msg["To"], msg["Subject"] = "a@x.org", "b@y.org", "IRB question"
            msg.set_content("Can we share <the> data?")
            msg.add_attachment(b"pdf", maintype="application", subtype="pdf", filename="form.pdf")
            mail.write_bytes(bytes(msg))
            page = frame.eml_preview(mail, root)
            self.assertIn("<th>Subject</th><td>IRB question</td>", page)
            self.assertIn("Can we share &lt;the&gt; data?", page)                          # escaped
            self.assertIn("form.pdf (1 KB)", page)
            listing = frame.render(frame.VANILLA, root, block, "Related")
            self.assertIn('<span class=chip data-tag="emails">emails</span>', listing)   # its subfolder's group
            self.assertIn(frame._e("/_board/workbench?view=eml&path=Project%2Ftasks%2Fb01_topic%2Frelated%2F"
                                   "emails%2F2026-10-09-0900+IRB+question.eml"), listing)

    def test_a_meeting_note_reads_as_plain_markdown(self):
        # JL 261011: a related meeting opened on "Not a Page"; any .md that is no Page reads as Markdown
        from live.page_reader import markdown_document, markdown_html
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            note = root / "Project/tasks/b01_topic/related/meetings/2026-10-10-1800 kickoff.md"
            note.parent.mkdir(parents=True)
            note.write_text("---\ntitle: kickoff\n---\n\n# Kickoff\n\n## Recording\n![[rec.webm]]\n\n"
                            "> [!quote]- Live transcript (2 lines)\n> [0:09] S1 hello\n> [0:11] S2 <b>hi</b>\n\n"
                            "| kind | link |\n|---|---|\n| paper | [it](papers/a.pdf) |\n\n- [ ] S1 push\n",
                            encoding="utf-8")
            page = markdown_document(note, root)
            self.assertIn("<pre class=front>title: kickoff</pre>", page)
            self.assertIn("<h1>Kickoff</h1>", page)
            self.assertIn("⤷ rec.webm", page)                                     # an Obsidian embed names its file
            self.assertIn('<details class="callout quote"><summary>Live transcript (2 lines)</summary>', page)
            self.assertIn("[0:09] S1 hello<br>[0:11] S2 &lt;b&gt;hi&lt;/b&gt;", page)  # one line per turn, escaped
            self.assertIn('href="/Project/tasks/b01_topic/related/meetings/papers/a.pdf"', page)
            self.assertIn("<li>☐ S1 push</li>", page)
            self.assertIn("<h1>related</h1>", markdown_html("related\n=======\n\nrows\n"))   # an underlined heading
            self.assertNotIn("javascript", markdown_html("[x](javascript:alert(1))"))

    def test_every_level_keeps_studio_and_delivery_in_the_top_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            for folder in (block, block / "j01_job", block / "j01_job/t01_task"):
                for space in ("Description", "Related", "Idea Studio", "Audience Report", "Delivery"):
                    with self.subTest(level=frame.level_of(folder), space=space):
                        page = frame.render(frame.VANILLA, root, folder, space)
                        levels = re.search(r'<nav class="row levels">(.*?)</nav>', page).group(1)
                        spaces = re.search(r'<nav class="row spaces">(.*?)</nav>', page)
                        self.assertEqual(re.findall(r'>([^<]+)</a>', levels)[:2], ["Studio", "Block"])
                        self.assertEqual(re.findall(r'>([^<]+)</a>', levels)[-1], "Delivery")  # Studio | B J T | Delivery
                        self.assertNotIn(">Related</a>", levels)          # Related folds in the Studio (JL 261011)
                        self.assertEqual(levels.count(">Studio</a>"), 1)
                        self.assertEqual(levels.count(">Delivery</a>"), 1)
                        self.assertNotIn(">SPACE</a>", levels)           # SPACE is the Guide's, not the top row's
                        self.assertEqual(levels.count("<span class=bar></span>"), 2)
                        shared = space in frame.TOP_ROW + frame.IN_STUDIO
                        self.assertEqual(levels.count('aria-current="page"'), int(shared))
                        work_space = "Description" if shared else space
                        self.assertIn(frame._e(frame.href(folder, root, frame.VANILLA, work_space, studio=True)), levels)
                        self.assertIn(frame._e(frame.href(folder, root, frame.VANILLA, "Delivery")), levels)
                        heading = re.search(r"<header class=page-title>(.*?)</header>", page).group(1)
                        if space == "Delivery":
                            self.assertIsNone(spaces)                    # no Spaces row: Delivery is in the top row
                            self.assertEqual(levels.count('class="tab on"'), 1)
                            self.assertIn('class="tab on" href="' + frame._e(frame.href(folder, root, frame.VANILLA, "Delivery")), levels)
                            self.assertNotIn('select class="on"', levels)
                            self.assertIn("· Delivery ·", heading)       # the Block's, from every level (s03-D06)
                            self.assertIn("b01", heading)
                            self.assertNotIn("· Job", heading)
                            parts = re.search(r'<nav class="row subs delivery-parts">(.*?)</nav>', page).group(1)
                            picked = re.findall(r'aria-current="true">([^<]+)</a>', parts)
                            self.assertEqual(len(picked), 1)
                            self.assertEqual(re.findall(r'>([^<]+)</a>', parts)[0], "Block")
                            if folder == block:
                                self.assertEqual(picked, ["Block"])
                                self.assertIn("The Block's delivery/", page)
                            else:
                                self.assertIn("Its part of the Block's Delivery", page)
                        elif space == "Related":                     # opens the Block's Studio, Related unfolded
                            self.assertIsNone(spaces)
                            self.assertEqual(levels.count('class="tab on"'), 1)
                            self.assertNotIn('select class="on"', levels)
                            self.assertIn("· Studio ·", heading)
                            self.assertIn("b01", heading)
                            self.assertNotIn("· Job", heading)
                            self.assertIn("<details class=studio-related id=studio-related open>", page)
                            self.assertIn("Nothing related yet", page)
                        elif space == "Idea Studio":
                            self.assertIsNone(spaces)
                            self.assertNotIn('<nav class="row subs">', page)
                            self.assertEqual(levels.count('class="tab on"'), 1)
                            self.assertNotIn('select class="on"', levels)
                            self.assertIn("· Studio ·", heading)
                            self.assertIn("b01", heading)
                            self.assertIn("</span> · Topic", heading)
                            self.assertNotIn("· Job", heading)
                            self.assertNotIn("· Task", heading)
                        else:
                            self.assertIsNotNone(spaces)
                            self.assertNotIn(">Studio</a>", spaces.group(1))
                            self.assertEqual(re.findall(r'>([^<]+)</a>', spaces.group(1)),
                                             [{"Audience Report": "Report", "Work Details": "Work"}.get(name, name)
                                              for name in frame.SPACE_NAMES
                                              if name not in frame.TOP_ROW + frame.IN_STUDIO])
                            self.assertNotIn(">Delivery</a>", spaces.group(1))
                            self.assertNotIn(">Related</a>", spaces.group(1))
                            self.assertEqual(spaces.group(1).count("<span class=bar></span>"), 3)
                            self.assertIn("Block b01", heading)
                        self.assertIn("j01_job", page)
                        self.assertIn("runs-panel", page)
            studio = self._space(root, block, "Idea Studio")
            self.assertIn('<details class=topic id="topic-s01-flow" data-studio-tags="[]"', studio)  # one closed row per topic
            topics = studio.split("id=studio-related", 1)[0]                 # the topic rows, before Related
            self.assertNotIn("class=topic-meta", topics)                     # (Delivery's cards keep their meta)
            self.assertNotIn("class=topic-source", topics)
            self.assertIn('data-src="/_excalidraw/?board=Project%2Ftasks%2Fb01_topic%2Fstudio%2Fs01-flow%2Fflow.excalidraw"',
                          studio)                                            # its canvas loads when opened
            self.assertIn("s02-&lt;topic&gt;", studio)                       # where the next topic goes
            self.assertIn('data-pop="s01-flow · the topic, full size"', studio)  # a topic pops out
            self.assertIn("<dialog id=frame-pop", studio)                    # into the frame's pop-out
            report = self._space(root, block, "Audience Report")
            self.assertIn("What is asked?", report)                          # Logic │ Work │ Report
            self.assertIn("One line that answers it.", report)               # the report's answer line
            self.assertIn(">j01_job</a>", report)                            # the Job that answers it
            self.assertIn("s01-flow ↗", report)                              # the studio topic that feeds it

    def test_an_old_theme_page_sends_its_block_to_the_frame(self):
        class Handler:                                   # records what frame_redirect sends
            def __init__(self): self.sent = {}
            def send_response(self, code): self.sent["code"] = code
            def send_header(self, key, value): self.sent[key] = value
            def end_headers(self): pass
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            for view, space in (("", ""), ("work", "&space=Work+Details"), ("questions", "&space=Audience+Report"),
                                ("scope", ""), ("nonsense", "")):
                h = Handler()
                frame.frame_redirect(h, block, root, view)
                self.assertEqual(h.sent["code"], 302)
                self.assertEqual(h.sent["Location"], "/_board/workbench?path=Project%2Ftasks%2Fb01_topic" + space)

    def test_studio_timeline_reads_dated_decisions_sessions_and_change_notes(self):
        # JL 261011: "add another section of the Timeline" to the Studio, now the fourth folding part
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "studio/s01-flow/s01-flow.md").write_text(
                "s01 · Flow\n=========\n\n**Tags:** `Structure`\n\nDecided\n-------\n\n"
                "s01-D01 · The flow reads down (JL 261007).\n"
                "s01-D02 · Two boxes merged, refined later\n    (JL 261011; revised 261012).\n"
                "s01-D03 · No date on this one.\n", encoding="utf-8")
            (block / "studio/s01-flow/flow.excalidraw").write_text(json.dumps({"elements": [
                {"type": "text", "text": "✎ 261011 boxes merged"},
                {"type": "text", "text": "✎ 261011 arrow added"},
                {"type": "text", "text": "✎ 261009 gone", "isDeleted": True},
                {"type": "text", "text": "a plain box"}]}), encoding="utf-8")
            passes = block / "runs/run-draw-s01/passes/p01-1010"
            passes.mkdir(parents=True)
            (passes / "pass.md").write_text("# First pass\n\nJL 261010: draw it.\n", encoding="utf-8")
            events, undated = frame.timeline_events(block, root)
            self.assertEqual([(e["day"], e["kind"]) for e in events],
                             [("2026-10-11", "decided"), ("2026-10-11", "drawing"),
                              ("2026-10-10", "session"), ("2026-10-07", "decided")])
            self.assertEqual(undated, ["s01-D03"])
            self.assertIn("boxes merged · arrow added", events[1]["html"])      # a deleted note is not read
            for folder in (block, block / "j01_job/t01_task"):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, studio=True)
                    self.assertLess(page.index("id=studio-related"), page.index("id=studio-timeline"))
                    self.assertIn("<summary><b>Timeline</b></summary>", page)       # no counts (JL 261011)
                    # one axis down the page, oldest day at the top (JL 261011: "up to down"; b10 s08)
                    days = re.findall(r'<li class="tl-day(?: tl-quiet)?" data-day="([^"]+)"', page)
                    self.assertEqual(days, ["2026-10-07", "2026-10-08", "2026-10-09", "2026-10-10", "2026-10-11"])
                    self.assertEqual(re.findall(r'<div class="tl-mrow(?: tl-quiet)?" data-day="([^"]+)"', page), days)
                    # the days between stay on the axis, quiet (JL 261012: "show the days between them")
                    self.assertEqual(re.findall(r'<div class="tl-mrow tl-quiet" data-day="([^"]+)"', page),
                                     ["2026-10-08", "2026-10-09"])
                    self.assertEqual(re.findall(r'<li class="tl-day tl-quiet" data-day="([^"]+)"', page),
                                     ["2026-10-08", "2026-10-09"])
                    self.assertIn("function tlGaps(tl)", page)
                    self.assertIn('<div class=tl-wrap data-level=days>', page)
                    self.assertEqual(re.findall(r'data-tl-level=(\w+)', page), ["days", "topics", "everything"])
                    # Days is a chart: a bubble per topic and day, sized by how much moved, and the day's bar
                    self.assertIn('<span class=tl-cell data-tl-key="studio/s01-flow" data-tl-count=3>'
                                  '<a class=tl-b href="#topic-s01-flow" style="--s:26px" '
                                  'title="s01-flow · Sun 11 Oct · 1 decided · 2 notes"></a></span>', page)
                    self.assertIn('<i style="width:100%"></i></span><b>3</b>', page)
                    self.assertIn('<a class=tl-col data-tl-key="studio/s01-flow" href="#topic-s01-flow" title="s01-flow">'
                                  '<b>s01</b><span>flow</span></a>', page)      # the full name, sNN straight (JL 261012)
                    # the chart's columns are the topic groups by default, or the topics (JL 261011)
                    self.assertIn('<div class=tl-map data-cols=groups style="--tl-slant:', page)
                    self.assertIn('<button type=button class=tl-gcol data-tl-group="structure" title="Structure: s01">'
                                  '🏗️ Structure</button>', page)
                    self.assertIn('<span class=tl-gcell data-tl-group="structure" data-tl-parts="{&quot;studio/s01-flow&quot;: 3}">'
                                  '<button type=button class=tl-gb style="--s:30px" '
                                  'title="Structure · Sun 11 Oct · 3 changes: s01 3"></button></span>', page)
                    self.assertIn('data-tl-cols=groups aria-pressed=true>by group</button>', page)
                    # Topics: a line per topic, a stacked bar of its kinds; Everything adds the items
                    self.assertIn('<a class=tl-name href="#topic-s01-flow" title="s01-flow"><b>s01</b><span>flow</span></a>', page)
                    self.assertIn('<i class=k-decided style="flex:1"></i><i class=k-drawing style="flex:2"></i>', page)
                    self.assertNotIn("No date on", page)                 # undated are not listed (JL 261012)
                    self.assertIn("timeline(key)", page)                                  # follows the group bar
                    # its own group picker, filled from the bar by the page script (JL 261012)
                    self.assertIn('<nav class=tl-groups aria-label="Pick a topic group"></nav>', page)
                    self.assertIn("tl-shown", page)

    def test_studio_card_shows_the_topic_stage_or_no_stage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            note = block / "studio/s01-flow/s01-flow.md"
            note.write_text(note.read_text() + "\n**Stage:** shaping\n")
            (block / "studio/s02-bare").mkdir()
            page = frame.render(frame.VANILLA, root, block, studio=True)
            self.assertIn('data-stage="shaping"', page)
            self.assertIn('<span class="stage stage-shaping"', page)            # the badge, at the far right (JL 261010)
            # step 2 of 4 filled, the word after it, no emoji (JL 261010: "more vivid")
            self.assertIn('<i class=stage-steps><b class="on"></b><b class="on"></b><b class=""></b><b class=""></b></i>'
                          'shaping</span></summary>', page)
            self.assertNotIn("🔶", page)
            self.assertIn('<span class="stage stage-none" title="No **Stage:** line yet">no stage</span></summary>', page)
            self.assertRegex(page, r'<b>s02-bare</b>.*?<span class=topic-pop>.*?</span><span class="stage stage-none"')
            note.write_text(note.read_text().replace("shaping", "maybe"))     # an unknown word shows no stage
            self.assertIn('data-stage=""', frame.render(frame.VANILLA, root, block, studio=True))

    def test_studio_tags_are_explicit_shared_and_keep_untyped_topics_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            note = block / "studio/s01-flow/s01-flow.md"
            note.write_text(note.read_text() + "\n**Type:** Structure\n**Tags:** UI · ui, Structure | Reading & writing\n")
            untyped = block / "studio/s02-legacy"
            untyped.mkdir()
            (untyped / "s02-legacy.md").write_text("s02 legacy\n====\n")
            self.assertEqual(frame._note_facts(note)["tags"], ["Structure", "UI", "Reading & writing"])
            for folder in (block, block / "j01_job", block / "j01_job/t01_task"):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, studio=True)
                    listing = re.search(r"<div class=studio-topics[^>]*>(.*?)</div>", page).group(1)
                    self.assertNotIn('data-studio-tag=""', listing)          # no All button; nothing picked shows all (JL 261010)
                    self.assertNotIn(' on"', listing.split("</nav>", 1)[0])    # no group is picked by default
                    self.assertIn('data-studio-tag="ui" aria-pressed="false"><span class=grp-emoji aria-hidden=true>🎨</span>'
                                  'UI <span class=tag-count>1</span>', listing)
                    self.assertIn('data-studio-tag="__untagged__" aria-pressed="false">Untagged <span class=tag-count>1</span>', listing)
                    self.assertIn('Reading &amp; writing', listing)
                    self.assertIn('id="topic-s02-legacy" data-studio-tags="[]"', listing)
                    self.assertNotRegex(listing, r'<details[^>]*\bhidden')
                    self.assertNotIn('<nav class="row spaces">', page)

    def test_vanilla_runs_are_grouped_by_type_in_the_third_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            data = json.loads(frame.frame_json(frame.VANILLA, root, task))
            runs = next(s for s in data["spaces"] if s["name"] == "Runs")
            self.assertEqual(runs["subspaces"], ["All", "build", "fit", "Page Runs"])
            page = frame.render(frame.VANILLA, root, task, "Runs", "build")
            shown = page.split("<section class=runs-panel", 1)[0]          # the Space, not the Disk list
            self.assertIn("run-build-t01", shown)
            self.assertNotIn("r01_fit/", shown)

    def test_a_theme_fills_only_what_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            work = frame.themes()["work"]
            data = json.loads(frame.frame_json(work, root, task))
            by = {s["name"]: s for s in data["spaces"]}
            self.assertEqual(by["Work Details"]["subspaces"], ["Code", "Review", "Notebooks", "Evidence", "Value"])
            self.assertEqual(by["Audience Report"]["subspaces"], ["Draft", "Report"])
            self.assertEqual(by["Runs"]["subspaces"], ["All", "build", "fit", "Page Runs"])   # the frame's own grouping
            self.assertIn("worker.py", frame.render(work, root, task, "Work Details", "Code"))
            self.assertIn("inputs → worker", frame.render(work, root, task, "Description", "Plan"))
            block = json.loads(frame.frame_json(work, root, root / "Project/tasks/b01_topic"))
            self.assertEqual([s["name"] for s in block["spaces"]], list(frame.SPACE_NAMES))

    def test_the_block_list_skips_a_link_that_leaves_the_root(self):
        from live.frame_view import _blocks
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as away:
            root = project(tmp)
            outside = Path(away) / "blueprints" / "b01_utils"     # a Tools checkout beside the SPACE
            outside.mkdir(parents=True)
            (outside / "board.md").write_text("# b01 · Utils\n\nboard-kind: task-block\n")
            (root / "Tools").symlink_to(Path(away), target_is_directory=True)
            found = [frame._rel(b, root) for b in _blocks(root)]    # _rel raised on the outside Block
            self.assertEqual(found, ["Project/tasks/b01_topic"])

    def test_studio_uses_the_block_topics_disk_sessions_and_new_run_target_at_every_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            job, task = block / "j01_job", block / "j01_job/t01_task"
            for folder in (job, task):
                topic = folder / "studio/s99-local"
                topic.mkdir(parents=True)
                (topic / "local.excalidraw").write_text("{}")
                (topic / "s99-local.md").write_text("s99 local\n====\n")
            run = block / "runs/run-draw-s01"
            (run / "passes/p01-1010").mkdir(parents=True)
            (run / "run.yaml").write_text("run: run-draw-s01\nkind: soft\ntype: draw\nstatus: done\ntarget: s01-flow\n")
            for folder in (block, job, task):
                with self.subTest(level=frame.level_of(folder)):
                    page = frame.render(frame.VANILLA, root, folder, "Idea Studio")
                    self.assertIn('data-owner="Project/tasks/b01_topic"', page)
                    self.assertIn('board=Project%2Ftasks%2Fb01_topic%2Fstudio%2Fs01-flow%2Fflow.excalidraw', page)
                    self.assertIn('id="topic-j01_job--s99-local"', page)
                    self.assertIn('id="topic-j01_job--t01_task--s99-local"', page)
                    disk_heading = re.search(r"<p class=disk-head>(.*?)</p>", page).group(1)
                    self.assertIn("b01_topic/", disk_heading)
                    self.assertNotIn("j01_job", disk_heading)
                    self.assertNotIn("t01_task", disk_heading)
                    self.assertIn("run-draw-s01", page)
                    self.assertIn("/haipipe-studio a topic of Project/tasks/b01_topic:", page)
                    self.assertNotIn("/haipipe-studio a topic of Project/tasks/b01_topic/j01_job:", page)

    def test_current_groups_keep_repeated_local_topics_distinct_and_skip_external_links(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as away:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            job, task = block / "j01_job", block / "j01_job/t01_task"
            for folder in (job, task):
                topic = folder / "studio/s01-flow"
                topic.mkdir(parents=True)
                (topic / "s01-flow.md").write_text("s01 local\n====\n\n**Feeds:** q01_ask\n")
                (topic / "flow.excalidraw").write_text("{}")
            report = job / "reports/q01_ask/q01_ask.md"
            report.parent.mkdir(parents=True)
            report.write_text("# Job's question\n")
            (job / "studio/s02-alias").symlink_to(block / "studio/s01-flow", target_is_directory=True)
            outside = Path(away) / "j99_private/studio/s99-secret"
            outside.mkdir(parents=True)
            (outside / "secret.excalidraw").write_text("{}")
            (block / "j99_private").symlink_to(outside.parent.parent, target_is_directory=True)
            (block / "studio/s99-external").symlink_to(outside, target_is_directory=True)
            old = block / "_archive/j98_old/studio/s98-old"
            old.mkdir(parents=True)
            inventory = frame.studio_inventory(block, root)
            self.assertEqual([source for source, _, _ in inventory], [p.resolve() for p in (block, job, task)])
            pages = [frame.render(frame.VANILLA, root, f, studio=True) for f in (block, job, task)]
            for page in pages:
                ids = re.findall(r'<details class=topic id="([^"]+)" data-studio-tags', page)
                self.assertEqual(ids, ["topic-s01-flow", "topic-j01_job--s01-flow", "topic-j01_job--t01_task--s01-flow"])
                listing = re.search(r'<div class=studio-topics[^>]*>(.*?)</div>', page).group(1)
                for name in ("s99-secret", "s99-external", "s02-alias", "s98-old"):
                    self.assertNotIn(name, listing)
                groups = re.findall(r'data-studio-tag="([^"]*)"', listing)
                self.assertEqual((groups[0], groups[-1]), ("__current__", "__untagged__"))
                self.assertIn('data-studio-key="j01_job/studio/s01-flow"', page)
                local = re.search(r'<details class=topic id="topic-j01_job--s01-flow"(.*?)</details>', page).group(1)
                self.assertIn('data-studio-source="j01_job"', local)
                self.assertNotIn("reports%2Fq01_ask", local)
                self.assertIn("s02-&lt;topic&gt;", page)  # old local numbers don't allocate new Block numbers

    def test_studio_groups_are_tags_written_to_the_topic_notes(self):
        """+ Group, drag onto a group, × on a chip, × on a group (b10 s02-D16): each is one tag edit."""
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            note = block / "studio/s01-flow/s01-flow.md"
            plain = block / "studio/s02-bare"
            plain.mkdir()
            (plain / "s02-bare.md").write_text("s02 · Bare\n==========\n\nNo topic line.\n")
            local = block / "j01_job/studio/s01-flow"
            local.mkdir(parents=True)
            (local / "s01-flow.md").write_text("s01 local\n====\n\n**Tags:** `UI`\n\n**Topic:** a Job one.\n")
            path = frame._rel(block, root)
            op = lambda **p: frame.studio_group_op(root, {"path": path, **p})
            res, err = op(op="add", topic="studio/s01-flow", tag="Levels")
            self.assertIsNone(err)
            self.assertEqual(res["topics"], {"studio/s01-flow": ["Levels"]})
            self.assertIn("**Tags:** `Levels`\n\n**Topic:** how it flows.", note.read_text())   # above **Topic:**
            res, err = op(op="add", topic="studio/s02-bare", tag="Levels")
            self.assertIn("\n==========\n\n**Tags:** `Levels`\n", (plain / "s02-bare.md").read_text())
            res, err = op(op="add", topic="j01_job/studio/s01-flow", tag="levels")           # a local topic, any case
            self.assertEqual(res["topics"]["j01_job/studio/s01-flow"], ["UI", "levels"])
            self.assertEqual(op(op="add", topic="studio/s01-flow", tag="Levels")[0]["changed"], 0)
            res, err = op(op="remove", topic="studio/s01-flow", tag="levels")
            self.assertEqual(res["topics"], {"studio/s01-flow": []})
            self.assertNotIn("**Tags:**", note.read_text())                                # no empty line left
            self.assertIn("=====\n\n**Topic:** how it flows.", note.read_text())
            res, err = op(op="delete", tag="Levels")
            self.assertEqual((res["changed"], sorted(res["topics"])), (2, ["j01_job/studio/s01-flow", "studio/s02-bare"]))
            self.assertEqual(frame._note_facts(local / "s01-flow.md")["tags"], ["UI"])
            for bad in ({"op": "add", "topic": "studio/s01-flow", "tag": "a, b"},
                        {"op": "add", "topic": "studio/s01-flow", "tag": "All"},
                        {"op": "add", "topic": "../outside", "tag": "X"},
                        {"op": "rename", "tag": "X"}):
                with self.subTest(bad=bad):
                    self.assertIsNone(op(**bad)[0])
            self.assertEqual(frame.studio_group_op(root, {"path": "../..", "op": "delete", "tag": "X"})[0], None)
            page = frame.render(frame.VANILLA, root, block, studio=True)
            self.assertIn('class=grp-new', page)
            self.assertIn('data-studio-delete="ui"', page)
            self.assertIn('class=tag-x', page)
            # each group's emoji comes from its name; an unknown name gets a fixed palette pick (JL 261010)
            self.assertEqual([frame.group_emoji(n) for n in ("Levels", "guide-ui", "层级", "Draft")], ["🪜", "🧭", "🪜", "✏️"])
            self.assertEqual(frame.group_emoji("My stuff"), frame.group_emoji("My stuff"))
            self.assertIn(frame.group_emoji("My stuff"), frame.GROUP_PALETTE)
            self.assertIn('data-studio-emoji="', page)
            # the group list file: + Group writes it, a drag rewrites the order, × removes the name
            self.assertIsNone(op(op="create", tag="Empty one")[1])
            self.assertEqual(op(op="create", tag="empty ONE")[0]["order"], ["Empty one"])          # no duplicate
            res, err = op(op="order", groups=["UI", "Empty one"])
            self.assertEqual(res["order"], ["UI", "Empty one"])
            self.assertEqual(frame.studio_group_order(block), ["UI", "Empty one"])
            listing = frame.studio_cards(block, root)
            self.assertEqual(re.findall(r'data-studio-tag="([^"]*)"', listing)[:3], ["__current__", "ui", "empty one"])
            self.assertIn('data-studio-tag="empty one" aria-pressed="false"><span class=grp-emoji aria-hidden=true>', listing)
            op(op="delete", tag="Empty one")
            self.assertEqual(frame.studio_group_order(block), ["UI"])
            self.assertIsNone(op(op="order", groups=["a, b"])[0])

    def test_related_groups_are_the_group_cell_of_related_md(self):
        """Related's groups work like the Studio's (JL 261011): a drag writes the row's group cell, a file with
        no row gets one, × on a group clears it from every row, the order is related/_groups.txt."""
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "related/materials").mkdir(parents=True)
            (block / "related/materials/form.docx").write_bytes(b"x")
            table = block / "related/related.md"
            table.write_text("Related\n=======\n\n| kind | date | item | link | feeds |\n|---|---|---|---|---|\n"
                             "| meeting | 2026-10-10 | Kickoff | `meetings/kickoff.md` | s01 |\n"
                             "| paper | 2024 | A paper | https://example.org/paper |\n", encoding="utf-8")
            op = lambda **p: frame.studio_group_op(root, {"path": frame._rel(block, root), "kind": "related", **p})
            # a subfolder is a group of its files (s04-D08): the meeting is in meetings before any drag; a web link
            # sits under its kind (JL 261013)
            self.assertEqual([i["groups"] for i in frame.related_items(block)],
                             [["meetings"], ["paper"], ["materials"]])
            res, err = op(op="add", topic="meetings/kickoff.md", tag="Meetings")              # it is there already
            self.assertEqual((err, res["topics"]), (None, {"meetings/kickoff.md": ["meetings"]}))
            self.assertNotIn("group", table.read_text())                                     # nothing written
            res, err = op(op="add", topic="meetings/kickoff.md", tag="SHIFT")
            self.assertIsNone(err)
            self.assertEqual(res["topics"], {"meetings/kickoff.md": ["meetings", "SHIFT"]})
            lines = table.read_text().splitlines()
            self.assertEqual(lines[:2], ["Related", "======="])                                     # the rest kept
            self.assertEqual(lines[3:6], ["| kind | date | item | link | feeds | group |",
                                          "|---|---|---|---|---|---|",
                                          "| meeting | 2026-10-10 | Kickoff | `meetings/kickoff.md` | s01 | SHIFT |"])
            self.assertEqual(lines[6], "| paper | 2024 | A paper | https://example.org/paper |  |  |")  # padded
            op(op="add", topic="meetings/kickoff.md", tag="IRB")
            self.assertIn("| s01 | SHIFT, IRB |", table.read_text())                          # comma-separated
            res, err = op(op="add", topic="materials/form.docx", tag="SHIFT")                # no row yet: one is added
            self.assertIsNone(err)
            self.assertEqual(table.read_text().splitlines()[-1], "|  |  | form.docx | `materials/form.docx` |  | SHIFT |")
            self.assertEqual([i["row"] for i in frame.related_items(block)], [0, 1, 2])
            res, err = op(op="remove", topic="meetings/kickoff.md", tag="IRB")
            self.assertEqual(res["topics"], {"meetings/kickoff.md": ["meetings", "SHIFT"]})
            res, err = op(op="remove", topic="meetings/kickoff.md", tag="meetings")          # the folder stays
            self.assertIsNone(res)
            self.assertIn("related/meetings/", err)
            self.assertIsNone(op(op="create", tag="Papers")[1])
            self.assertEqual(frame.studio_group_order(block, "related"), ["Papers"])
            self.assertTrue((block / "related/_groups.txt").is_file())
            self.assertFalse((block / "studio/_groups.txt").exists())                      # the Studio's own stays apart
            page = frame.render(frame.VANILLA, root, block, studio=True)
            bar = re.search(r'data-group-kind=related data-group-noun=item>(.*?)</nav>', page).group(1)
            self.assertEqual(re.findall(r'data-studio-tag="([^"]*)"', bar),
                             ["__current__", "papers", "materials", "meetings", "paper", "shift"])   # the web link: paper
            self.assertIn('SHIFT <span class=tag-count>2</span>', bar)
            self.assertIn('data-studio-key="materials/form.docx"', page)
            self.assertIn('class=tag-x title="Take out of SHIFT"', page)
            res, err = op(op="delete", tag="SHIFT")
            self.assertEqual((res["changed"], sorted(res["topics"])), (2, ["materials/form.docx", "meetings/kickoff.md"]))
            self.assertNotIn("SHIFT", table.read_text())
            self.assertIsNone(op(op="add", topic="nowhere.md", tag="X")[0])
            self.assertIsNone(frame.studio_group_op(root, {"path": frame._rel(block, root), "kind": "other",
                                                           "op": "create", "tag": "X"})[0])

    def test_report_bar_at_every_level_and_its_kinds_coloured(self):
        # b10 s05-D16, D17, JL 261012: "the report group tags for both the block level, job level and task level";
        # "the fixed groups (or the suggested default group labels) ... give them different colors"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "b01_topic.md").write_text("# b01 · Topic\n\nboard-kind: task-block\n", encoding="utf-8")
            job = block / "j01_work"
            task = job / "t01_step"
            task.mkdir(parents=True)
            (job / "j01_work.md").write_text("# j01 · Work\n", encoding="utf-8")
            (task / "t01_step.md").write_text("# t01 · Step\n", encoding="utf-8")
            for f in (block, job, task):                     # a bar at every level, before its first Question
                page = frame.render(frame.VANILLA, root, f, "Audience Report")
                self.assertIn("data-group-kind=reports", page)
                self.assertIn('data-studio-tag="random thoughts"', page)
            self.assertIn("the Page", frame.render(frame.VANILLA, root, task, "Audience Report"))
            bar = frame.group_list(block, root, "reports", [["Data"]], "", starting=("Pilot",), fixed=("Data",))
            self.assertIn('class="tab grp-fixed"', bar)
            self.assertIn('class="tab grp-suggested"', bar)
            self.assertNotIn('data-studio-delete="data"', bar)    # a fixed group has no ×
            self.assertIn("gray</span>: fixed by the theme", bar)

    def test_report_groups_are_tags_like_the_studios(self):
        # b10 s05, JL 261011: "if the report card to show, it will be the same as the sNN, we can create and add
        # the tags"; "for someother report, the groups are of the special forms, and that ones are fixed"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            face = block / "b01_topic.md"
            face.write_text("# b01 · Topic\n\nboard-kind: task-block\n\n## Questions\n\n```yaml\nquestions:\n"
                            "- id: Q01\n  title: What is asked?\n  question: What is asked,\n    in two lines?\n"
                            "  report: reports/q01_ask/q01_ask.md\n- id: Q02\n  title: Who asks?\n  group: reviewer\n```\n",
                            encoding="utf-8")
            page = frame.render(frame.VANILLA, root, block, "Audience Report")
            bar = re.search(r'data-group-kind=reports data-group-noun=question>(.*?)</nav>', page).group(1)
            # every theme's suggested group first, in its own colour (s05-D06, D16), then the Block's own
            self.assertEqual(re.findall(r'data-studio-tag="([^"]*)"', bar),
                             ["__current__", "random thoughts", "reviewer", "__untagged__"])
            self.assertIn('class="tab grp-suggested" title="Suggested by the theme', bar)
            self.assertEqual(page.count('class="topic q-card"'), 2)                  # one card per Question
            self.assertIn("<b>Q01 · What is asked?</b>", page)
            self.assertIn("One line that answers it.", page)                         # opened: Logic │ Work │ Report
            self.assertNotIn(">Related Questions<", page)                            # the paper's four buttons are gone
            op = lambda **p: frame.studio_group_op(root, {"path": frame._rel(block, root), "kind": "reports", **p})
            res, err = op(op="add", topic="Q01", tag="Levels")
            self.assertEqual((err, res["topics"]), (None, {"Q01": ["Levels"]}))
            text = face.read_text()
            self.assertIn("- id: Q01\n  title: What is asked?\n  group: Levels\n  question: What is asked,", text)
            op(op="add", topic="Q01", tag="UI")
            self.assertIn("  group: Levels, UI\n", face.read_text())                # comma-separated, like Tags:
            op(op="remove", topic="Q02", tag="reviewer")
            self.assertNotIn("group: reviewer", face.read_text())                   # no groups, no line
            self.assertEqual(frame._register(face)[1], {"id": "Q02", "title": "Who asks?"})
            self.assertIsNone(op(op="create", tag="Random thoughts")[1])
            self.assertEqual(frame.studio_group_order(block, "reports"), ["Random thoughts"])
            self.assertTrue((block / "reports/_groups.txt").is_file())
            # a theme's own groups are fixed: no ×, and they cannot be taken out
            theme = frame.Theme(report_fixed=lambda row: ["Data"] if str(row["id"]) == "Q01" else [],
                                report_groups=("Data", "Wisdom"))
            html = frame.report_view("Block", block, root, theme)
            bar = re.search(r'data-group-kind=reports data-group-noun=question>(.*?)</nav>', html).group(1)
            self.assertEqual(re.findall(r'data-studio-label="([^"]*)"', bar)[:4], ["Current", "Random thoughts", "Data", "Wisdom"])
            self.assertIn('Wisdom <span class=tag-count>0</span>', bar)            # a starting group shows, empty
            self.assertIn('data-studio-fixed="[&quot;data&quot;]"', html)
            self.assertIn('<span class=chip data-tag="Data">Data</span>', html)      # no ×
            orig = frame.themes, frame.theme_of                     # the op finds the Block's theme, here this one
            frame.themes, frame.theme_of = (lambda: {"fixed": theme}), (lambda folder, root: "fixed")
            try:
                res, err = op(op="remove", topic="Q01", tag="Data")
            finally:
                frame.themes, frame.theme_of = orig
            self.assertIsNone(res)
            self.assertIn("fixed by the theme", err)
            # b16's two hooks: report_fixed(row, owner) reads the owner folder; report_cards adds the theme's own
            seen = []
            paper = frame.Theme(report_fixed=lambda row, owner: seen.append(owner.name) or (["Research questions"]
                                                                                            if row["id"] == "Q01" else []),
                                report_cards=lambda level, folder, root: [
                                    {"id": "IDEA-01", "title": "five axes", "groups": ["Ideation"], "status": "sent",
                                     "html": "<p>its verdict</p>"}])
            html = frame.report_view("Block", block, root, paper)
            self.assertIn("b01_topic", seen)                                        # the owner reached the rule
            self.assertIn('<span class=chip data-tag="Research questions">Research questions</span>', html)
            card = re.search(r'<details class="topic q-card q-theme".*?</details>', html, re.S).group(0)
            self.assertIn("<b>IDEA-01 · five axes</b>", card)
            self.assertNotIn("studio-drag", card)                                   # not draggable
            self.assertIn('<span class=chip data-tag="Ideation">Ideation</span>', card)   # its group fixed, no ×
            self.assertIn("<p>its verdict</p>", card)
            self.assertIn('Ideation <span class=tag-count>1</span>', html)          # counted on the bar
            self.assertIsNone(op(op="add", topic="IDEA-01", tag="UI")[0])            # no register line: refused
            # a Task with no Questions: its own Page, under the bar every level now shows (s05-D17, JL 261012)
            task = block / "j01_job/t01_task"
            self.assertIn("data-group-kind=reports", frame.render(frame.VANILLA, root, task, "Audience Report"))
            # the level's own Runs on a Question sit in its Work cell (b10 s05 Open 3): a card whose target: is its id
            for name, target in (("run-report-q02", "q02"), ("run-draw-s01", "s01")):
                (block / "runs" / name).mkdir(parents=True)
                (block / "runs" / name / "run.yaml").write_text(f"run: {name}\ntarget: {target}\nticket: {name}.md\n"
                                                                "status: done\n", encoding="utf-8")
                (block / "runs" / name / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
            html = frame.report_view("Block", block, root)
            # two columns (b10 s32-D23): the work is a line inside the Report column
            work = re.search(r'id="question-Q02"><div class=q-l>.*?<p class=q-work><span class=mut>Work:</span> (.*?)</p>',
                             html, re.S)
            self.assertIn("run-report-q02</a> <span class=mut>done</span>", work.group(1))
            self.assertIn("1 piece of work", html)                                  # counted on its card
            self.assertNotIn("run-draw-s01", html)                                  # a topic's Run is no Question's
            # a Feeds line may name a Question by its bare id, Q01, as well as by its folder (b10 s05 Open 8)
            topic = block / "studio/s01-idea/s01-idea.md"
            topic.parent.mkdir(parents=True)
            topic.write_text("# s01 · Idea\n\n**Feeds:** Q01 (what is asked) · q02_who\n", encoding="utf-8")
            self.assertEqual(frame._note_facts(topic)["feeds"], ["q01", "q02_who"])
            self.assertIn("s01-idea", re.search(r'id="question-Q01">.*?<div class=q-r>', frame.report_view(
                "Block", block, root), re.S).group(0))                               # from the Idea Studio
            self.assertEqual(frame._report_page("q01", block, root), block / "reports/q01_ask/q01_ask.md")

    def test_a_themes_studio_is_also_shared_from_its_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            theme = frame.Theme(spaces=lambda level, folder, root, sub: {
                "Idea Studio": frame.Space(f'<p>Studio source: {folder.name}</p>')})
            page = frame.render(theme, root, task, "Idea Studio")
            self.assertIn("Studio source: b01_topic", page)
            self.assertNotIn("Studio source: t01_task", page)
            self.assertIn("Studio source: b01_topic", frame.spaces_for(theme, "Task", task, root)["Idea Studio"].html)

    @staticmethod
    def _space(root, folder, space):
        return frame.render(frame.VANILLA, root, folder, space)


class BandTest(unittest.TestCase):
    def test_the_page_has_no_band_and_no_old_page_link(self):
        # JL 261007: "why I still have this? please remove that": the level tabs say where you are;
        # the path is the title's tooltip
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            page = frame.render(frame.themes()["work"], root, root / "Project/tasks/b01_topic")
            self.assertNotIn("class=band", page)
            self.assertNotIn("the old page", page)
            self.assertIn('<h1 title="Block · Project/tasks/b01_topic · Work theme · b01_topic" data-guide="🧪 Work · Guide · Block b01">', page)
            # the level row is the page index, the page's title under it (b03 s32-D13, JL 261008)
            self.assertLess(page.index('<nav class="row levels">'), page.index("<header class=page-title>"))
            self.assertIn("<span class=lv>Block b01 ·</span> Topic</h1>", page)   # its tag said once


class StyleTest(unittest.TestCase):
    # JL 261007, "base styles only": the frame carries the base's shared view styles (a theme's Spaces
    # may use their classes) and no theme's own look; those styles never restyle the frame itself.
    def test_the_frame_carries_the_base_view_styles_and_they_leave_its_chrome_alone(self):
        import re
        from live.space_views import SPACE_VIEW_CSS
        from live.work_items import WORK_ITEM_CSS
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            page = frame.render(frame.themes()["work"], root, root / "Project/tasks/b01_topic")
            self.assertIn(SPACE_VIEW_CSS, page)
            self.assertIn(WORK_ITEM_CSS, page)
            for rule in (".st-ok{", ".st-warn{", ".topic.missing{"):      # base status and missing-card marks
                self.assertIn(rule, page)
        chrome = {"tab", "row", "band", "levels", "spaces", "bar", "subs", "split", "space-main", "runs-panel",
                  "topic", "q-row", "chip", "wf-table", "frame-body"}
        for css in (SPACE_VIEW_CSS, WORK_ITEM_CSS):
            css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
            for selector in re.findall(r"([^{}]+)\{", css):
                for part in selector.split(","):
                    first = part.strip().split()[0] if part.strip() else ""
                    with self.subTest(selector=part.strip()):
                        self.assertFalse(first.startswith(("body", "html", ":root")), part)
                        self.assertNotIn(first.split(":")[0].lstrip("."), chrome, part)


    def test_a_tasks_page_views_are_subspaces_drawn_in_place(self):
        # the old Page workbench's routes, one page per tab, are the Task's Spaces now (JL 261007)
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            data = json.loads(frame.frame_json(frame.VANILLA, root, task))
            by = {s["name"]: s["subspaces"] for s in data["spaces"]}
            self.assertEqual(by["Description"], ["Face", "Folder"])
            self.assertEqual(by["Work Details"], ["Folders", "Evidence", "Value"])
            self.assertEqual(by["Delivery"], ["Files", "Lanes"])
            page = frame.render(frame.VANILLA, root, task, "Work Details", "Evidence")
            self.assertIn('class=page-view src="/_board/workbench?view=evidence&amp;path=Project%2Ftasks', page)
            block = json.loads(frame.frame_json(frame.VANILLA, root, root / "Project/tasks/b01_topic"))
            self.assertNotIn("Evidence", {x for s in block["spaces"] for x in s["subspaces"]})   # a Block has none


    def test_the_disk_box_names_the_files_behind_the_open_space(self):
        # JL 261007: "add the disks as well ... so we have both disks and runs"
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            page = frame.render(frame.VANILLA, root, block, "Audience Report")
            self.assertIn("<div class=runs-body><div class=disk-in>", page)   # inside the Runs panel, first: one fold
            self.assertIn("<span>Report: the title and its answer line</span>", page)         # a group, one row per file
            self.assertIn("## Questions: one row per Question", page)
            work = frame.render(frame.VANILLA, root, block, "Work Details")
            self.assertIn('<span class=disk-p>j01_job/</span>', work)                          # the Block's one Job, a row
            missing = frame.disk_markup((("nothing-here/", "what it would feed"),), block, root)
            self.assertIn("<li class=miss", missing)                                           # greyed: not there yet
            self.assertIn("<span class=disk-n>not yet</span>", missing)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            runs = frame.render(frame.VANILLA, root, task, "Runs", "Page Runs")
            self.assertIn("the Page&#x27;s Runs: planned, registered, done", runs)               # the open Page view's own


class ButtonSkillTest(unittest.TestCase):
    """Every Run button the frame draws names its owning skill, and that skill exists (b03 s21-D02;
    haipipe-run ref/run-types-by-space.md)."""

    def buttons(self, root):
        block = root / "Project" / "tasks" / "b01_topic"
        task = block / "j01_job" / "t01_task"
        for level, folder in (("Block", block), ("Job", block / "j01_job"), ("Task", task)):
            for space, view in frame.spaces_for(frame.VANILLA, level, folder, root).items():
                for k in view.run_types:
                    yield level, space, k
        for space, subs in frame.PAGE_TASK_SUBS.items():
            for sub in subs or ("",):
                for k in frame.page_task_spaces(task, root, sub)[space].run_types:
                    yield "Page Task", space + " " + sub, k

    def test_every_button_names_a_skill_that_exists(self):
        skills = Path(frame.__file__).resolve().parents[2] / "skills"
        names = {p.parent.name for p in skills.glob("**/SKILL.md")}
        with tempfile.TemporaryDirectory() as tmp:
            seen = list(self.buttons(project(tmp)))
        self.assertGreater(len(seen), 30)
        for level, space, k in seen:
            self.assertTrue(k.get("skills"), f"{level} · {space} · {k['label']} names no skill")
            for s in k["skills"]:
                self.assertIn(s, names, f"{level} · {space} · {k['label']}: no skill {s}")

    def test_the_level_owns_its_own_buttons(self):
        with tempfile.TemporaryDirectory() as tmp:
            # a button is named by its soft Run, `run-<type>-<target>`, what it does under it (JL 261007)
            buttons = list(self.buttons(project(tmp)))
            seen = {(level, k.get("doing") or k["label"]): k["skills"] for level, _, k in buttons}
        self.assertTrue(all(k["label"].startswith(("run-", "rNN_")) for _, _, k in buttons),
                        [k["label"] for _, _, k in buttons if not k["label"].startswith(("run-", "rNN_"))])
        self.assertEqual(seen[("Block", "add a Job")], ["haipipe-block"])
        self.assertEqual(seen[("Job", "add a Task")], ["haipipe-job"])
        self.assertEqual(seen[("Task", "build the Task")], ["haipipe-task"])
        self.assertEqual(seen[("Job", "write the report")], ["haipipe-report"])
        self.assertEqual(seen[("Block", "add a topic · redraw it · save this session, each a pass")], ["haipipe-studio"])


class RouteTest(unittest.TestCase):
    def _get(self, root, path):
        sent = {}

        class Fake(FrameMixin):
            def guide_send(self, body, code=200, content_type="text/html", head_only=False):
                sent.update(body=body, code=code, type=content_type)

            def runs_view(self, head_only=False):
                sent.update(view="runs", path=self.path)
        handler = Fake()
        handler.root, handler.path = str(root), path
        handler.workbench_frame_view()
        return sent

    def test_a_deck_and_its_pictures_are_served_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            tiny_deck(root / "Project/tasks/b01_topic/deck.pptx")
            sent = self._get(root, "/_board/workbench?view=pptx&path=Project/tasks/b01_topic/deck.pptx")
            self.assertEqual(sent["code"], 200)
            self.assertIn("<svg", sent["body"])
            sent = self._get(root, "/_board/workbench?view=pptx&path=Project/tasks/b01_topic/deck.pptx"
                                   "&media=ppt/media/image1.png")
            self.assertEqual((sent["code"], sent["type"]), (200, "image/png"))
            self.assertEqual(self._get(root, "/_board/workbench?view=pptx&path=../outside.pptx")["code"], 404)
            self.assertEqual(self._get(root, "/_board/workbench?view=pptx&path=Project/tasks/b01_topic/deck.pptx"
                                             "&media=ppt/slides/slide1.xml")["code"], 404)

    def test_studio_delivery_folds_under_related_with_every_result_previewed(self):
        # JL 261014: "a new item after the Related to name it as the delivery ... show all the delivery and
        # preview them here": what came in, then what went out, from every level
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            task = block / "j01_job/t01_task"
            shutil.rmtree(block / "delivery")                                # the fixture's own result out
            page = frame.render(frame.VANILLA, root, task, studio=True)
            self.assertIn("Nothing delivered yet.", page)
            self.assertIn("delivery/ · 0 results", page)
            (block / "delivery/j01_job/t01_task").mkdir(parents=True)
            (block / "delivery/j01_job/t01_task/report.pdf").write_bytes(b"%PDF-1.4")
            (block / "delivery/j01_job/t01_task/report.docx").write_bytes(b"x")
            (block / "delivery/j01_job/slides.html").write_text("<p>x</p>", encoding="utf-8")
            for folder in (block, task):                                     # the Block's, at every level
                with self.subTest(folder=folder.name):
                    page = frame.render(frame.VANILLA, root, folder, studio=True)
                    self.assertLess(page.index("id=studio-related"), page.index("id=studio-delivery"))
                    self.assertLess(page.index("id=studio-delivery"), page.index("id=studio-timeline"))
                    fold = page.split("id=studio-delivery", 1)[1].split("id=studio-timeline", 1)[0]
                    self.assertIn("<summary><b>Delivery</b><span class=related-meta>delivery/ · 2 results · "
                                  "PDF 1 · Word 1 · Web page 1</span>", fold)
                    self.assertIn('data-src="/Project/tasks/b01_topic/delivery/j01_job/t01_task/report.pdf"', fold)
                    self.assertIn('data-src="/Project/tasks/b01_topic/delivery/j01_job/slides.html"', fold)
                    self.assertIn(frame._e(frame.href(block, root, frame.VANILLA, "Delivery")), fold)

    def test_studio_folder_shows_the_block_folder_and_loads_a_folder_when_opened(self):
        # JL 261012: "在 related 和 timeline 下面再搞一个 folder ... 这个 block 的 folder 都长什么内容" (b10 s09)
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / ".seed.json").write_text("{}")                         # a dotfile is left out
            (block / "studio" / "__pycache__").mkdir()                      # and a cache
            page = frame.render(frame.VANILLA, root, block, studio=True)
            self.assertLess(page.index("id=studio-timeline"), page.index("id=studio-folder"))
            self.assertIn("<summary><b>Folder</b></summary>", page)
            self.assertIn("<p class=fd-root>Project/tasks/b01_topic/</p>", page)
            # a folder: its name, how many it holds, what it is for; its rows load when opened
            self.assertIn('<details data-dir="Project/tasks/b01_topic/studio"><summary class=fd-row '
                          'title="Project/tasks/b01_topic/studio/"><span class=fd-name>studio/</span>'
                          '<span class=fd-n>1</span><span class=fd-word>the Studio: a folder per topic</span>', page)
            self.assertIn('<span class=fd-n>2</span><span class=fd-word>j01 · Job</span>', page)   # its face's title
            self.assertLess(page.index('data-dir="Project/tasks/b01_topic/delivery"'),        # folders first
                            page.index('title="Project/tasks/b01_topic/b01_topic.md"'))
            self.assertIn('<span class=fd-i>📝</span><a data-pop="b01_topic.md" href="/_board/page?path=', page)
            self.assertNotIn("seed.json", page.split("id=studio-folder")[1])
            sent = self._get(root, "/_board/workbench?view=dir&path=Project/tasks/b01_topic/studio/s01-flow")
            self.assertEqual(sent["code"], 200)
            self.assertIn('<a data-pop="flow.excalidraw" href="/_excalidraw/?board=', sent["body"])
            self.assertIn("<span class=fd-n>1 KB</span>", sent["body"])                  # Delivery's _size
            self.assertNotIn("__pycache__", self._get(root, "/_board/workbench?view=dir&path=Project/tasks/b01_topic/studio")["body"])
            body = self._get(root, "/_board/workbench?view=dir&path=Project/tasks/b01_topic/j01_job/t01_task/runs")["body"]
            self.assertIn("<span class=fd-name>r01_fit/</span><span class=fd-n>1</span>"          # a Run: its card
                          "<span class=fd-word>hard · fit + evaluate · done</span>", body)
            many = block / "runs"
            for i in range(302):
                (many / f"run-{i:03d}").mkdir(parents=True)
            body = self._get(root, "/_board/workbench?view=dir&path=Project/tasks/b01_topic/runs")["body"]
            self.assertEqual(body.count("<li class=fd-dir>"), 300)                      # past 300, a button
            self.assertIn('data-dir="Project/tasks/b01_topic/runs">Show the other 2</button>', body)
            body = self._get(root, "/_board/workbench?view=dir&path=Project/tasks/b01_topic/runs&all=1")["body"]
            self.assertEqual(body.count("<li class=fd-dir>"), 302)
            self.assertEqual(self._get(root, "/_board/workbench?view=dir&path=../..")["code"], 404)
            self.assertEqual(self._get(root, "/_board/workbench?view=dir&path=Project/nothing")["code"], 404)

    def test_the_route_lists_blocks_opens_a_folder_in_its_theme_and_refuses_outside_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            self.assertIn("Project/tasks/b01_topic", self._get(root, "/_board/workbench")["body"])
            sent = self._get(root, "/_board/workbench?path=Project/tasks/b01_topic/j01_job/t01_task&space=Work+Details")
            self.assertEqual(sent["code"], 200)
            self.assertIn("🧪 Work", sent["body"])
            self.assertIn("Notebooks", sent["body"])
            self.assertEqual(self._get(root, "/_board/workbench?path=../../etc")["code"], 404)
            data = json.loads(self._get(root, "/_board/workbench?path=Project/tasks/b01_topic&format=json")["body"])
            self.assertEqual(data["theme"], "work")
            self.assertEqual(data["level"], "Block")

    def test_studio_preserves_the_task_and_work_view_for_return(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            original = "/_board/workbench?path=Project/tasks/b01_topic/j01_job/t01_task&space=Work+Details&sub=Code"
            page = self._get(root, original)["body"]
            studio_url = unescape(re.search(r'<a class="tab" href="([^"]+)"[^>]*>Studio</a>', page).group(1))
            query = parse_qs(urlparse(studio_url).query)
            self.assertEqual(query["studio"], ["1"])
            self.assertEqual(query["space"], ["Work Details"])
            self.assertEqual(query["sub"], ["Code"])
            studio = self._get(root, studio_url)["body"]
            self.assertNotIn('<nav class="row spaces">', studio)
            self.assertIn('data-owner="Project/tasks/b01_topic"', studio)
            back = unescape(re.search(r'<a class=tab href="([^"]+)" title="t01_task">', studio).group(1))
            self.assertNotIn("studio", parse_qs(urlparse(back).query))
            restored = self._get(root, back)["body"]
            self.assertIn('<nav class="row spaces">', restored)
            self.assertIn("worker.py", restored)
            self.assertIn('class="tab on"', restored)

    def test_view_draws_one_page_task_view_from_the_same_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            sent = self._get(project(tmp), "/_board/workbench?view=runs&path=P/t01.md&run=r01")
            self.assertEqual(sent["view"], "runs")
            self.assertEqual(sent["path"], "/_board/workbench?path=P%2Ft01.md&run=r01")   # view= left out


if __name__ == "__main__":
    unittest.main()
