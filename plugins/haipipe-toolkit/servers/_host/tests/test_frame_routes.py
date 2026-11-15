"""The frame's styles, its buttons and skills, and the /_board/workbench route."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from html import unescape
from urllib.parse import parse_qs, unquote, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live import task_draft  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402
from frame_fixtures import project, tiny_deck  # noqa: E402,F401


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
        for space, subs in task_draft.DRAFT_TASK_SUBS.items():
            for sub in subs or ("",):
                for k in task_draft.draft_task_spaces(task, root, sub)[space].run_types:
                    yield "Page Task", space + " " + sub, k

    def test_every_button_names_a_skill_that_exists(self):
        skills = Path(frame.__file__).resolve().parents[3] / "skills"    # servers/workbench/page/frame.py
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
