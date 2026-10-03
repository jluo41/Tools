"""Every workbench follows the shared Workbench rules (servers/README.md, "Adding a workbench").

A new Workbench family must pass all of these before it is served. The families that
predate a rule are named in GAPS with the rules they still miss, so a new family cannot
slip in without them, and a gap closed here shows up as a stale entry.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live.guide_families import FAMILIES  # noqa: E402
from live.workbench_guide import REPOSITORY, VIEWS  # noqa: E402

SERVERS = Path(__file__).resolve().parents[2]
SKILLS = SERVERS.parent / "skills"
GUIDE_RULES = ("description", "table", "papers", "design")
# Families that predate a rule, and the rules they still miss (JL 261003: "make sure other
# new workbench UI will do the same thing"). Remove a rule here when its family meets it.
GAPS = {}

# Families whose working Spaces do not yet use the shared Runs panel (live.runs_panel): Insight
# draws its own (Labeling switched 261003). Remove a family when it switches.
RUNS_GAPS = {"insight"}


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def guide_rules(profile: dict) -> set[str]:
    """The Guide rules a family's registry entry meets."""
    explain = profile.get("explain") or {}
    met = set()
    if profile.get("description"):
        met.add("description")
    if profile.get("table"):
        met.add("table")
    if profile.get("papers_table") or explain.get("related-paper"):
        met.add("papers")
    if len(explain.get("roadmap-draw") or ()) > 2 and explain["roadmap-draw"][2] == "Workbench design":
        met.add("design")
    return met


class GuideFamilyTest(unittest.TestCase):
    def test_guide_has_the_four_views(self):
        self.assertEqual([key for key, _, _ in VIEWS], ["description", "method", "roadmap-draw", "related-paper"])

    def test_every_family_has_a_presenter_that_mounts_guide(self):
        for family, profile in FAMILIES.items():
            with self.subTest(family=family):
                presenter = REPOSITORY / profile["presenter"]
                if not presenter.is_file():      # an optional plugin (labeling) may be absent
                    continue
                folder = presenter.parent
                self.assertTrue(any("mount_guide(" in p.read_text(encoding="utf-8") for p in folder.glob("*.py")),
                                f"{folder.name}: no presenter calls mount_guide()")
                self.assertTrue(profile.get("method"), f"{family}: no Method steps")

    def test_spaces_follow_the_space_order(self):
        # workbench-shared/README.md § Space order: Guide -> setup -> work -> Delivery. Guide is
        # mounted first and never listed again; Delivery, when a family has it, comes last.
        for family, profile in FAMILIES.items():
            with self.subTest(family=family):
                names = [name.split("›")[-1].strip() for name, _ in profile["spaces"]]
                self.assertNotIn("Guide", names, f"{family}: Guide is mounted first, not listed as a Space")
                if "Delivery" in names:
                    self.assertEqual(names[-1], "Delivery", f"{family}: Delivery comes last, not {names}")

    def test_every_family_meets_the_guide_rules_or_names_its_gap(self):
        for family, profile in FAMILIES.items():
            with self.subTest(family=family):
                missing = set(GUIDE_RULES) - guide_rules(profile)
                self.assertEqual(missing, GAPS.get(family, set()),
                                 f"{family}: misses {sorted(missing)}; a new family meets every rule, "
                                 "and an old one's GAPS entry lists exactly what it still misses")

    def test_every_working_space_puts_its_runs_in_the_shared_right_panel(self):
        # JL 261003: "always put the run in the right panel". One panel for every workbench:
        # live.runs_panel (panel_markup, PANEL_CSS, PANEL_JS, SPLIT_CSS), on the right, folding
        # to a vertical "Runs" tab.
        for family, profile in FAMILIES.items():
            with self.subTest(family=family):
                presenter = REPOSITORY / profile["presenter"]
                if not presenter.is_file():
                    continue
                shared = any("runs_panel import" in p.read_text(encoding="utf-8") for p in presenter.parent.glob("*.py"))
                self.assertEqual(not shared, family in RUNS_GAPS,
                                 f"{family}: {'uses' if shared else 'does not use'} the shared Runs panel; "
                                 "a new family must, and RUNS_GAPS lists exactly the ones that do not yet")

    def test_the_guide_space_shows_its_runs_on_the_right(self):
        from live.workbench_guide import guide_html, table_rows
        for family, profile in FAMILIES.items():
            if any(r["Space"] == "Guide" and r["Run type"] not in ("", "none") for r in table_rows(profile)):
                with self.subTest(family=family):
                    page = guide_html(family, "description", {"path": "", "file": ""})
                    self.assertIn('class="split wg-split"', page)
                    self.assertIn("class=runs-panel", page)

    def test_every_table_reads_and_every_papers_table_checks(self):
        workbench = load(SKILLS / "0_utils/table-workbench/ref/render_workbench_table.py", "render_workbench_table")
        papers = load(SKILLS / "0_utils/table-papers/ref/check_papers_table.py", "check_papers_table")
        for family, profile in FAMILIES.items():
            if not (REPOSITORY / profile["presenter"]).is_file():
                continue                          # an optional plugin (labeling) may be absent
            with self.subTest(family=family):
                if profile.get("table"):
                    self.assertTrue(workbench.read_table(REPOSITORY / profile["table"]), f"{family}: empty Workbench Table")
                if profile.get("papers_table"):
                    table = REPOSITORY / profile["papers_table"]
                    problems, _ = papers.check(papers.read_table(table), table)
                    self.assertEqual(problems, [], f"{family}: papers table fails table-papers")


class EmbeddedPageTest(unittest.TestCase):
    def test_a_page_shown_inside_guide_has_no_viewport_sized_canvas(self):
        # Guide's frame takes the embedded page's height; a canvas sized by vh grows the frame,
        # which grows the canvas, without end (JL 261003: "quickly zoom and zoom out").
        posters = [p for p in SERVERS.rglob("*.py") if not {"__pycache__", "tests"} & set(p.parts)
                   and "postMessage({kind:'haipipe-explain-height'" in p.read_text(encoding="utf-8")]
        self.assertTrue(posters)
        for page in posters:
            with self.subTest(page=page.name):
                text = page.read_text(encoding="utf-8")
                self.assertRegex(text, r"\.st-frame\{\{?height:\d+px", f"{page.name}: embedded studio canvas needs a fixed height")
                self.assertRegex(text, r"\.rp-frame\{\{?height:\d+px", f"{page.name}: embedded PDF frame needs a fixed height")


class HostTest(unittest.TestCase):
    def test_a_workbench_tab_never_gets_the_excalidraw_icon(self):
        serve = (SERVERS / "_host" / "serve.py").read_text(encoding="utf-8")
        self.assertIn('EXCAL_ICONS = ("/favicon", "/apple-touch-icon.png")', serve)
        self.assertRegex(serve, r"startswith\(self\.EXCAL_ICONS\) and \"/_excalidraw\" not in")

    def test_every_workbench_folder_is_reachable(self):
        from host_registry import WORKBENCH_ROUTES, workbench_folders
        names = {f.name.split("-", 1)[1] for f in workbench_folders()}
        self.assertTrue(names <= set(WORKBENCH_ROUTES), names - set(WORKBENCH_ROUTES))


if __name__ == "__main__":
    unittest.main()
