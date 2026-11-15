"""The frame's Studio: the top row at every level, timeline, topic cards, runs and the theme overlay."""
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


class FrameStudioTest(unittest.TestCase):
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

    def test_a_topic_with_a_structured_side_switches_free_and_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            topic = block / "studio" / "s01-flow"
            (topic / "s01-flow.mindmap.md").write_text(
                "---\nmindmap: 1\n---\n\n# Flow <!-- root -->\n\n- in <!-- n01 -->\n  - **raw** rows <!-- n02 -->\n")
            row_of = lambda: re.search(r'<details class=topic id="topic-s01-flow".*?</details>',
                                       frame.render(frame.VANILLA, root, block, studio=True), re.S).group(0)
            row = row_of()
            self.assertIn('data-sides="free structured" data-side="free"', row)
            self.assertIn('<button type=button data-side=free aria-pressed="true"', row)
            self.assertIn('<button type=button data-side=structured aria-pressed="false"', row)
            free = re.search(r'<div class=st-pane data-side=free>(.*?)</div>', row, re.S).group(1)
            self.assertIn("flow.excalidraw", unquote(free))                # the free side: the topic's own drawing
            # the structured side: the mind map drawn by the code that draws a draft's §1 map (haipipe-mindmap), no canvas
            mind = row[row.index('<div class="st-pane st-map" data-side=structured hidden>'):]
            rel = "Project/tasks/b01_topic/studio/s01-flow/s01-flow.mindmap.md"
            self.assertIn(f'<div class=pm-edit data-task="{rel}" data-file="{rel}" data-endpoint="/_board/mindmap">', mind)
            self.assertIn('<div class=pm-para data-p="n01">', mind)
            self.assertIn('<li data-s="n02">', mind)
            self.assertIn("<strong>raw</strong> rows", mind)
            self.assertNotIn("_excalidraw", mind.split("<script>")[0])
            # Edit opens the free canvas, so it shows on Free only, and only for a hand-drawn drawing
            self.assertIn('class=draw-edit data-sides="free">Edit', row)
            self.assertIn("localStorage.setItem(key,side)", frame.render(frame.VANILLA, root, block, studio=True))
            (topic / "build_s01_flow.py").write_text("print(1)\n")
            self.assertNotIn("draw-edit", row_of())
            # a topic with only its mind map opens on it; the map is never taken for the main drawing
            (topic / "flow.excalidraw").unlink()
            row = row_of()
            self.assertIn('data-side="structured"', row)
            self.assertIn('data-side=free aria-pressed="false" disabled', row)
            self.assertIn("No drawing", row)
            # a change on the map (the payload a draft's §1 map sends) is written into the file by haipipe-mindmap
            code, res = frame.mindmap_module().act(root, {"task": rel, "what": "add", "p": "n01", "after": "n02",
                                                         "value": "clean rows"})
            self.assertEqual(code, 200)
            self.assertIn("  - clean rows <!-- n03 -->", (topic / "s01-flow.mindmap.md").read_text())

    def test_studio_runs_lists_every_hard_run_with_its_status(self):
        """JL 261019: "list another one to show the Hard Run, for each task, and just show their status"."""
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            runs = block / "j01_job/t01_task/runs"
            (runs / "r01_done/result").mkdir(parents=True)
            (runs / "r01_done/result/runtime.yaml").write_text("status: complete\nfinished_at: '2026-10-19T12:00:00'\n")
            (runs / "r02_waits").mkdir(parents=True)
            (runs / "r02_waits/run.yaml").write_text("run: r02_waits\nstatus: planned\n")
            (runs / "run-draw-s01").mkdir(parents=True)                       # a soft Run: not listed
            page = frame.render(frame.VANILLA, root, block, studio=True)
            self.assertIn("id=studio-runs", page)
            self.assertNotIn("3 hard Runs", page)                           # no tally on the page (JL 261113)
            self.assertRegex(page, r"✅</span><code>r01_done</code><span class=rn-st>complete</span><span class=rn-day>2026-10-19")
            self.assertRegex(page, r"⬜</span><code>r02_waits</code><span class=rn-st>planned")
            self.assertNotIn("<code>run-draw-s01</code>", page)
            self.assertNotIn("<code>run-build-t01</code>", page)
            self.assertLess(page.index("id=studio-delivery"), page.index("id=studio-runs"))
            self.assertLess(page.index("id=studio-runs"), page.index("id=studio-timeline") if "id=studio-timeline" in page else len(page))

    def test_hard_runs_read_flat_tickets_and_show_a_running_runs_start(self):
        """JL 261019: "show the current run progress"; Proj11 b01 keeps runs/rNN_*.sh tickets, receipts in results/."""
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp) / "b01_topic"
            task = block / "j04_job/t01_task"
            (task / "runs").mkdir(parents=True)
            for name in ("r01_done", "r02_going", "r03_elsewhere"):
                (task / "runs" / f"{name}.sh").write_text("#!/bin/bash\n")
            (task / "runs/eval_old.sh").write_text("#!/bin/bash\n")               # not rNN_: not a hard Run
            (task / "results/r01_done").mkdir(parents=True)
            (task / "results/r01_done/runtime.yaml").write_text("status: complete\nfinished_at: 2026-10-10T18:36:27-04:00\n")
            (block / "j04_job/results/t01_task/r02_going").mkdir(parents=True)  # the Job's results/<task>/<run>/
            (block / "j04_job/results/t01_task/r02_going/runtime.yaml").write_text(
                "status: running\nstarted_at: 2026-10-19T13:02:11-04:00\nprogress: 1200/5000 steps\n")
            self.assertEqual(frame.hard_runs(block), [
                ("j04_job", "t01_task", "r01_done", "complete", "2026-10-10"),
                ("j04_job", "t01_task", "r02_going", "running", "since 10-19 13:02 · 1200/5000 steps"),
                ("j04_job", "t01_task", "r03_elsewhere", "no receipt", "")])
            self.assertEqual(frame.runs_tally(frame.hard_runs(block)), "✅1 ▶️1 ⬜1")

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

    @staticmethod
    def _space(root, folder, space):
        return frame.render(frame.VANILLA, root, folder, space)


if __name__ == "__main__":
    unittest.main()
