"""The card Guide (b03 studio/s31-guide, s31-D05 to D08), the work family first: every View in three
folding sections, Block · Job · Task, each a stack of cards; a Space card's sub and runs read live from
the frame; the section of the level the Guide was opened from starts open; the old family key answers."""
from __future__ import annotations

import html
import json
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live.guide_families import FAMILIES, family_key  # noqa: E402
from live.workbench_guide import REPOSITORY, VIEWS, guide_html, level_steps, mount_guide  # noqa: E402

from test_frame import project  # noqa: E402

LEVELS = ("Block", "Job", "Task")
SECTION = re.compile(r'<details class="wg-level" data-drawing="level-(\w+)" data-level="\w+"( data-here)?( open)?>')
CARD = re.compile(r'<div class="wg-card"><p class="wg-card-head"><b>([^<]*)</b><span>[^<]*</span></p>'
                  r'<p class="wg-card-line">sub: (.*?)   reads: .*?   runs: (.*?)</p></div>')


def folders(root: Path) -> dict:
    block = root / "Project/tasks/b01_topic"
    return {"Block": block, "Job": block / "j01_job", "Task": block / "j01_job/t01_task"}


def context(root: Path, folder: Path, level: str) -> dict:
    md = frame.face(folder)
    return {"path": md.relative_to(root).as_posix(), "file": md.name, "level": level}


def sections(page: str) -> list:
    """The level sections between one View's lead and its All levels fold: [(level, open)]."""
    return [(level, bool(opened)) for level, _, opened in SECTION.findall(page)]


def here(page):
    """The level marked as the one the Guide was opened from."""
    return [level for level, mark, _ in SECTION.findall(page) if mark]


def space_cards(page: str, level: str) -> dict:
    """{Space: (sub, runs)} of one level's section in a Description page."""
    start = page.index(f'data-level="{level}"')
    end = min([i for i in (page.find('data-level="', start + 10), page.find('data-drawing="level-all"'))
               if i > 0] or [len(page)])
    return {name: (html.unescape(sub), html.unescape(runs)) for name, sub, runs in CARD.findall(page[start:end])}


class CardGuideTest(unittest.TestCase):
    def test_index_is_first_in_guide_and_leaves_the_parent_workbench(self):
        for view, _, _ in VIEWS:
            with self.subTest(view=view):
                page = guide_html("shared", view, {"path": "", "file": ""}, True,
                                  index_url="https://example.test/?view=radial&measure=studios")
                nav = re.search(r'<nav class="wg-views"[^>]*>(.*?)</nav>', page).group(1)
                labels = re.findall(r'>([^<]+)</a>', nav)
                self.assertEqual(labels, ["Index"] + [label for _, label, _ in VIEWS])
                self.assertIn('href="https://example.test/?view=radial&amp;measure=studios" target="_top" data-guide-index', nav)
                self.assertEqual(nav.count('aria-current="page"'), 1)
        default = guide_html("shared", "description", {"path": "", "file": ""}, True)
        self.assertIn('href="/?view=radial&amp;measure=studios" target="_top" data-guide-index', default)
        invalid = guide_html("shared", "description", {"path": "", "file": ""}, True,
                             index_url="javascript:alert(1)")
        self.assertNotIn("javascript:alert", invalid)

    def test_every_view_is_three_folding_level_sections_then_all_levels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            ctx = context(root, folders(root)["Block"], "Block")
            for view, _, _ in VIEWS:
                with self.subTest(view=view):
                    page = guide_html("work", view, ctx, True, root=root)
                    self.assertEqual([level for level, _ in sections(page)], list(LEVELS))
                    self.assertIn('data-drawing="level-all"', page)       # the View's earlier body, folded
                    self.assertIn('class="wg-card', page)

    def test_every_level_starts_closed_and_the_opened_one_is_marked(self):   # JL 261008: collapsed by default
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            for level, folder in folders(root).items():
                with self.subTest(level=level):
                    page = guide_html("work", "description", context(root, folder, level), True, root=root)
                    self.assertEqual([lv for lv, opened in sections(page) if opened], [])
                    self.assertEqual(here(page), [level])
            page = guide_html("work", "method", {"path": "", "file": ""}, True, root=root)
            self.assertEqual([lv for lv, opened in sections(page) if opened], [])   # no level: none open

    def test_a_space_cards_sub_and_runs_are_the_frames_own(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            theme = frame.theme_for_guide("work")
            self.assertEqual(theme.name, "work")
            page = guide_html("work", "description", context(root, folders(root)["Task"], "Task"), True, root=root)
            for level, folder in folders(root).items():
                with self.subTest(level=level):
                    cards = space_cards(page, level)
                    self.assertEqual(list(cards), list(frame.SPACE_NAMES))
                    tabs = json.loads(frame.frame_json(theme, root, folder))["spaces"]
                    for space in tabs:
                        sub, runs = cards[space["name"]]
                        self.assertEqual(sub, " · ".join(space["subspaces"]) or "—", space["name"])
                        self.assertEqual(runs, " · ".join(space["run_types"]) or "—", space["name"])

    def test_a_level_with_no_folder_shows_the_themes_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "Project/tasks/b02_empty"
            block.mkdir(parents=True)
            (block / "b02_empty.md").write_text("# b02 · Empty\n\nboard-kind: task-block\n")
            page = guide_html("work", "description", context(root, block, "Block"), True, root=root)
            theme = frame.theme_for_guide("work")
            for level in ("Job", "Task"):
                with self.subTest(level=level):
                    want = {name: (" · ".join(subs) or "—", " · ".join(runs) or "—")
                            for name, subs, runs in frame.space_cards(theme, level, None, root)}
                    self.assertEqual(space_cards(page, level), want)
            self.assertIn("run-plan-<tNN>", space_cards(page, "Task")["Description"][1])   # the work theme's own, by its Run

    def test_the_frame_tells_the_guide_its_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            for level, folder in folders(root).items():
                with self.subTest(level=level):
                    page = frame.render(frame.themes()["work"], root, folder)
                    config = json.loads(re.search(r'id="wb-guide-mount">(.*?)</script>', page).group(1))
                    self.assertEqual(config["family"], "work")
                    self.assertEqual(config["context"]["level"], level)


class RouteTest(unittest.TestCase):
    def test_every_frame_folder_opens_its_level_guide(self):
        # the frame names a faceless folder (a Job of bare Tasks) by its path alone; the Guide once
        # answered "file is missing" there
        from live.base import BaseMixin
        from live.workbench_guide import WorkbenchGuideMixin
        sent = {}

        class Fake(WorkbenchGuideMixin, BaseMixin):
            only = None

            def guide_send(self, body, code=200, content_type="text/html", head_only=False):
                sent.update(body=body, code=code)
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            job = folders(root)["Job"]
            (job / "j01_job.md").unlink()
            handler = Fake()
            handler.root = root
            handler.workbench_index_url = "https://example.test/?view=radial&measure=studios"
            handler.path = ("/_board/guide?family=task&view=description&embed=1&level=Job&file=&path="
                            + job.relative_to(root).as_posix())
            handler.guide_view()
            self.assertEqual(sent["code"], 200, sent["body"][:200])
            self.assertEqual(here(sent["body"]), ["Job"])
            self.assertIn('href="https://example.test/?view=radial&amp;measure=studios" target="_top" data-guide-index', sent["body"])
            self.assertEqual(len(space_cards(sent["body"], "Job")), 6)
            task = folders(root)["Task"]                                 # a Task's face is not a Board Page
            handler.path = ("/_board/guide?family=work&view=method&embed=1&level=Task&path="
                            + (task / "t01_task.md").relative_to(root).as_posix() + "&file=t01_task.md")
            handler.guide_view()
            self.assertEqual(sent["code"], 200, sent["body"][:200])
            self.assertEqual(here(sent["body"]), ["Task"])
            handler.path = "/_board/guide?family=work&view=description&embed=1&path=../../etc"
            handler.guide_view()
            self.assertNotEqual(sent["code"], 200)                      # outside the root: still refused


class FamilyTest(unittest.TestCase):
    def test_the_old_family_key_answers_as_work(self):
        self.assertEqual(family_key("task"), "work")
        self.assertIn("work", FAMILIES)
        self.assertNotIn("task", FAMILIES)
        page = mount_guide("<body></body>", "task", {"path": "x/board.md", "file": "board.md"}, "nav", "main")
        self.assertIn('"family": "work"', page)

    def test_a_family_takes_the_card_guide_only_by_declaring_levels(self):
        # any family opts in by its guide.yaml levels: (work, then paper, insight …); the others keep
        # their Guide as it was. The conformance test's GAPS lists who has not moved yet.
        for family in FAMILIES:
            with self.subTest(family=family):
                page = guide_html(family, "description", {"path": "", "file": ""}, True)
                if FAMILIES[family].get("levels"):
                    self.assertEqual([lv for lv, _ in sections(page)], list(LEVELS))
                else:
                    self.assertNotIn('class="wg-level"', page)
        self.assertTrue(FAMILIES["work"].get("levels"))

    def test_every_work_step_is_done_in_one_of_the_six_spaces(self):
        steps = level_steps(REPOSITORY / FAMILIES["work"]["method_doc"])
        self.assertEqual(sorted(steps), sorted(LEVELS))
        for level, rows in steps.items():
            for row in rows:
                with self.subTest(level=level, step=row["step"]):
                    for part in row["where in the workbench"].split(";"):
                        space = re.split(r"\s+[›·]\s+", part.strip())[0]
                        self.assertIn(space, frame.SPACE_NAMES)

    def test_every_work_paper_names_its_levels_and_every_roadmap_drawing_is_on_disk(self):
        from live.related_papers import paper_rows
        rows = paper_rows(REPOSITORY / FAMILIES["work"]["papers_table"])
        self.assertTrue(rows)
        for r in rows:
            with self.subTest(paper=r["paper"][:40]):
                self.assertTrue({w.strip() for w in r["level"].split(";")} <= set(LEVELS) | {"all"})
        roadmap = FAMILIES["work"]["roadmap"]
        self.assertEqual(sorted(roadmap), sorted(LEVELS))
        for level, drawings in roadmap.items():
            for d in drawings:
                with self.subTest(level=level, drawing=d["title"]):
                    self.assertTrue((REPOSITORY / d["board"][len("Tools/"):]).is_file(), d["board"])


if __name__ == "__main__":
    unittest.main()
