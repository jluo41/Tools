"""The Block workbenches stay separate but look the same (JL 261004: "we just separate them ...
but we can make their styles to be the same"). Task, CoWork and Discovery draw one shell with
the Task Workbench's own stylesheet and script; a workbench that brings its own copy fails here."""
from __future__ import annotations

import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

SERVERS = Path(__file__).resolve().parents[2]
TASK_CSS = (SERVERS / "workbench-task/assets/css/90-task-workbench.css").read_text(encoding="utf-8")
TASK_JS = (SERVERS / "workbench-task/assets/js/90-task-workbench.js").read_text(encoding="utf-8")
SHELL = ('<main id="task-workbench">', '<nav class="spaces"', 'id="tw-config"', 'id="tw-run-dialog"', 'class="split"')


class BlockWorkbenchStyleTest(unittest.TestCase):
    def assets(self):
        from live.cowork_views import _assets as cowork_assets
        from live.discovery_views import _assets as discovery_assets
        return {"cowork": cowork_assets(), "discovery": discovery_assets()}

    def test_every_block_workbench_loads_the_task_stylesheet_and_script(self):
        for kind, (css, js, _panel) in self.assets().items():
            with self.subTest(kind=kind):
                self.assertTrue(css.startswith(TASK_CSS), f"{kind}: its stylesheet must start with the Task one, unchanged")
                self.assertEqual(js, TASK_JS, f"{kind}: it must run the Task Workbench's own script")

    def test_no_block_workbench_ships_its_own_stylesheet(self):
        for kind in ("workbench-cowork", "workbench-discovery"):
            with self.subTest(kind=kind):
                own = list((SERVERS / kind).glob("assets/css/*.css")) + list((SERVERS / kind).glob("assets/js/*.js"))
                self.assertEqual(own, [], f"{kind}: style lives in workbench-task (later workbench-shared), not here")

    def test_every_block_workbench_draws_the_same_shell(self):
        from live.cowork_views import render_block as cowork_render, spaces as cowork_spaces
        from live.discovery_views import render_block as discovery_render, spaces as discovery_spaces
        for kind, spaces in (("cowork", cowork_spaces()), ("discovery", discovery_spaces())):
            with self.subTest(kind=kind):
                names = [title for _, title, _ in spaces]
                self.assertEqual(names[0], "Scope")
                self.assertEqual(names[-1], "Delivery")
                self.assertIn("Check", names)
        source = {"cowork": (SERVERS / "workbench-cowork/cowork_views.py").read_text(encoding="utf-8"),
                  "discovery": (SERVERS / "workbench-discovery/discovery_views.py").read_text(encoding="utf-8")}
        for kind, text in source.items():
            for mark in SHELL:
                with self.subTest(kind=kind, mark=mark):
                    self.assertIn(mark, text, f"{kind}: the shared shell needs {mark}")
        self.assertTrue(callable(cowork_render) and callable(discovery_render))



class BlockWorkbenchTitleTest(unittest.TestCase):
    """Each page names its kind first (JL 261004): 📋 Task · 🔭 Discovery · 📨 CoWork, then the Block title."""
    TITLES = {"workbench-task/task_views.py": "📋 Task · ", "workbench-discovery/discovery_views.py": "🔭 Discovery · ",
              "workbench-cowork/cowork_views.py": "📨 CoWork · "}

    def test_every_block_workbench_title_names_its_kind(self):
        for path, prefix in self.TITLES.items():
            text = (SERVERS / path).read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIn(f"<title>{prefix}{{e(snap['title'])}}</title>", text)
                self.assertIn(f"<h1>{prefix}{{e(snap['title'])}}</h1>", text)

    def test_home_shows_each_kind_with_its_emoji(self):
        from live.home import board_kind
        root = Path("/space")
        self.assertEqual(board_kind(root / "p/cowork/b11_x", root), ("CoWork Board", "📨"))
        self.assertEqual(board_kind(root / "p/discoveries/b01_x", root), ("Discovery Board", "🔭"))
        self.assertEqual(board_kind(root / "p/tasks/b01_x", root), ("Task Board", "📋"))


if __name__ == "__main__":
    unittest.main()
