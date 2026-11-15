"""The frame's groups: Studio and Related groups, the report bar and a theme's shared Studio."""
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


class FrameGroupsTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
