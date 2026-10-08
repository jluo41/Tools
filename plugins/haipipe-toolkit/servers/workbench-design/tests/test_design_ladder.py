"""The design theme on b12's ladder (s11 · s12 · s13, 261007): the Block, a Job and each kind of Task drawn from a
placeholder Project (design_fixture.py), plus a Block on today's `_by-<method>` layout, which keeps its own reading.
Every Space's views and run types as the design draws them, the Job read from its face's pins (no `_by-`), and
every ↗ in a page opening something that exists."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import design_reader as R  # noqa: E402
from live import design_views as V  # noqa: E402
from live import frame  # noqa: E402
from live.design_theme import THEME  # noqa: E402
import design_fixture as F  # noqa: E402

# (Space, views, run types), as b12's s11 · s12 · s13 SCREENS draw them (a red "?" run is left out)
BLOCK = {"Description": (["Map", "Goals", "Methods", "Inputs"], ["run-add-job-<jNN>"]),
         "Idea Studio": ([], ["run-draw-<sNN>"]),
         "Audience Report": (["Questions", "Cost", "Predicted vs observed", "Method scorecard"],
                             ["run-propose-questions", "run-report-<qNN>"]),
         "Work Details": (["All", "G01", "G02"], ["run-add-job-<jNN>"]),
         "Runs": (["All", "Set up", "Launch a Job", "Report"],
                  ["run-add-goal-<goal>", "run-add-job-<jNN>", "run-propose-questions"]),
         "Delivery": ([], ["run-release-<jNN>"])}
BLOCK_VIEWS = {("Description", "Goals"): ["run-add-goal-<goal>"], ("Description", "Methods"): ["run-propose-method-<slug>"],
               ("Description", "Inputs"): ["run-add-inputs-<iN>"], ("Audience Report", "Cost"): [],
               ("Audience Report", "Predicted vs observed"): ["run-add-observed-<eNN>", "run-score-<eNN>"],
               ("Audience Report", "Method scorecard"): []}
JOB = {"Description": (["Goal", "Method", "Inputs"], ["run-setup-goal-j03", "run-close-j03"]),
       "Idea Studio": ([], ["run-draw-s01"]),
       "Audience Report": (["Reason ideas", "Design display", "Review whole", "Predicted vs observed", "Performance"],
                           ["run-reason-t00"]),
       "Work Details": (["Reason ideas", "Conduct & review", "Review whole"], ["run-reason-t00", "run-open-designs-j03"]),
       "Runs": (["Setup", "Reason ideas", "Conduct & review", "Review whole"],
                ["run-setup-goal-j03", "run-setup-method-j03", "run-setup-inputs-j03", "run-open-designs-j03"]),
       "Delivery": (["designs.md", "designs.json"], ["run-release-j03"])}
JOB_VIEWS = {("Description", "Method"): ["run-setup-method-j03"], ("Description", "Inputs"): ["run-setup-inputs-j03"],
             ("Audience Report", "Design display"): ["run-generate-dNN", "run-verify-dNN-v1"],
             ("Audience Report", "Review whole"): ["run-rank-t99"],
             ("Audience Report", "Predicted vs observed"): ["run-freeze-predictions-j03"],
             ("Audience Report", "Performance"): ["run-freeze-predictions-j03"],
             ("Work Details", "Conduct & review"): ["run-generate-dNN", "run-verify-dNN-v1", "run-revise-dNN"],
             ("Work Details", "Review whole"): ["run-rank-t99"],
             ("Runs", "Reason ideas"): ["run-reason-t00"],
             ("Runs", "Conduct & review"): ["run-generate-dNN", "run-verify-dNN-v1", "run-revise-dNN"],
             ("Runs", "Review whole"): ["run-rank-t99", "run-freeze-predictions-j03", "run-release-j03"]}
T00 = {"Description": (["Task"], ["run-reason-t00"]), "Idea Studio": ([], ["run-draw-s01"]),
       "Audience Report": (["Topics", "Ideas"], ["run-reason-t00"]), "Work Details": (["Chains"], ["run-reason-t00"]),
       "Runs": (["All", "hard", "soft"], ["run-reason-t00"]), "Delivery": ([], [])}
DESIGN = {"Description": (["Design", "Evaluation"], []), "Idea Studio": ([], ["run-draw-s01"]),
          "Audience Report": (["Tests", "Drafts", "Performance"], ["run-verify-d04"]),
          "Work Details": (["Elements"], ["run-revise-d04"]),
          "Runs": (["All", "hard", "soft"], ["run-generate-d04", "run-verify-d04", "run-revise-d04"]), "Delivery": ([], [])}
T99 = {"Description": (["Task"], ["run-rank-t99"]), "Idea Studio": ([], ["run-draw-s01"]),
       "Audience Report": (["Ranking", "Coverage"], ["run-rank-t99"]), "Work Details": (["Kept · Dropped"], ["run-rank-t99"]),
       "Runs": (["All", "hard", "soft"], ["run-rank-t99"]), "Delivery": ([], [])}


def space_html(root: Path, folder: Path, space: str, sub: str = "") -> str:
    """One Space's own content, as the frame lays it out (never the frame's own parts)."""
    level = frame.level_of(folder) or "Block"
    return frame.spaces_for(THEME, level, folder, root, sub)[space].html


class DesignLadderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = F.make(self.root) / F.BLOCK
        self.job = self.block / "j03_g01_m04"
        self.t00 = self.job / "t00_reason-ideas"
        self.design = self.job / "t04_d04_ask-only"
        self.t99 = self.job / "t99_review-whole"

    def tearDown(self):
        self.tmp.cleanup()

    def frame_of(self, folder, sub=""):
        return {s["name"]: s for s in json.loads(frame.frame_json(THEME, self.root, folder, sub))["spaces"]}

    def test_every_level_is_the_design_theme_on_the_ladder(self):
        self.assertTrue(R.is_ladder(self.block))
        for folder in (self.block, self.job, self.t00, self.design, self.t99):
            self.assertEqual(frame.theme_of(folder, self.root), "design")

    def test_each_level_serves_the_designed_views_and_run_types(self):
        for folder, want in ((self.block, BLOCK), (self.job, JOB), (self.t00, T00), (self.design, DESIGN), (self.t99, T99)):
            got = self.frame_of(folder)
            for space, (subs, runs) in want.items():
                with self.subTest(level=folder.name, space=space):
                    self.assertEqual(got[space]["subspaces"], subs)
                    self.assertEqual(got[space]["run_types"], runs)

    def test_each_view_carries_its_own_run_types(self):
        for folder, views in ((self.block, BLOCK_VIEWS), (self.job, JOB_VIEWS)):
            for (space, view), runs in views.items():
                with self.subTest(level=folder.name, view=view):
                    self.assertEqual(self.frame_of(folder, view)[space]["run_types"], runs)
                    self.assertEqual(self.frame_of(folder, view)[space]["open"], view)

    def test_each_runs_panel_entry_carries_its_run_card(self):
        """Named as its Run, each entry takes its skill, agent, sign and prompt from the ladder run cards (b12 s21)."""
        kinds = {k["label"]: k for k in frame.spaces_for(THEME, "Job", self.job, self.root, "Conduct & review")["Runs"].run_types}
        ver = kinds["run-verify-dNN-v1"]
        self.assertEqual(ver["skills"], ["haipipe-design-unit"])
        self.assertTrue(ver["prompt"].startswith("Run with haipipe-design-reviewer-agent."))
        goal = {k["label"]: k for k in frame.spaces_for(THEME, "Block", self.block, self.root, "Goals")["Description"].run_types}
        self.assertEqual(goal["run-add-goal-<goal>"]["skills"], ["haipipe-design-goal"])
        self.assertIn("I sign the goal", goal["run-add-goal-<goal>"]["prompt"])
        method = {k["label"]: k for k in frame.spaces_for(THEME, "Block", self.block, self.root, "Methods")["Description"].run_types}
        self.assertEqual(method["run-propose-method-<slug>"]["skills"], ["haipipe-design-method"])
        for label in ("run-reason-t00", "run-generate-d04", "run-rank-t99", "run-setup-method-j03", "run-release-j03"):
            self.assertIsNotNone(V.card_for(label), label)

    def test_the_method_types_come_from_the_registry(self):
        self.assertTrue(R.REGISTRY, "the registry haipipe-design-method/methods/ is read")
        self.assertEqual(R.METHODS["M04"], ("Actionable insights", "By insight"))
        self.assertIn("m2", R.REGISTRY["M04"]["versions"])

    def test_the_job_is_read_from_its_pins_not_a_by_slug(self):
        j = R.job(self.job)
        self.assertEqual((j["goal"], j["method"], j["version"], j["inputs"], j["type"]), ("G01", "M04", "m2", "i2", "By insight"))
        self.assertEqual([d["id"] for d in j["designs"]][:3], ["d01", "d02", "d03"])
        self.assertEqual(sum(d["state"] == "dropped" for d in j["designs"]), 5)
        self.assertEqual(len(j["ideas"]), 15)
        self.assertTrue(any(f["link"].startswith("../../inputs/i2/") for f in j["files"]))

    def test_the_block_reads_goals_inputs_observed_and_scores(self):
        b = R.board(self.block)
        self.assertEqual([g["id"] for g in b["goals"]], ["G01", "G02", "G03"])
        self.assertEqual([v["id"] for v in b["inputs"]], ["i1", "i2"])
        self.assertEqual(b["scores"][("j03", "d04")]["direction"], "✓")
        self.assertTrue(all(r["kind"] == "soft" for r in b["runs"]))        # every Block Run is soft (s11)

    def test_the_views_show_what_the_design_draws(self):
        page = lambda folder, space, sub="": space_html(self.root, folder, space, sub)
        self.assertIn("M04 · Actionable insights", page(self.block, "Description", "Map"))
        cmp_ = page(self.block, "Description", "Map/j02_g01_m04~j03_g01_m04")
        self.assertIn("the method, m1 → m2", cmp_)
        self.assertIn("inputs held", cmp_)
        self.assertIn("proposed · not signed", page(self.block, "Description", "Goals"))
        pvo = page(self.block, "Audience Report", "Predicted vs observed")
        self.assertIn("Text message", pvo)
        self.assertIn("arm B of e01", pvo)
        self.assertIn("<code>t00</code> reason ideas", page(self.block, "Work Details"))        # the open Job previews its Tasks
        self.assertIn("j04", page(self.block, "Delivery"))
        self.assertIn("../../inputs/i2/rules.md", unescape(page(self.job, "Description", "Inputs")))
        self.assertIn("Dropped by t99", page(self.job, "Audience Report", "Design display"))
        self.assertIn("arm B of e01", page(self.job, "Audience Report", "Predicted vs observed"))
        self.assertIn("{LINK}", page(self.design, "Description", "Design"))
        self.assertIn("draft 2", page(self.design, "Audience Report", "Drafts"))
        self.assertIn("kept", page(self.t99, "Work Details"))

    def test_the_b12_s32_rulings(self):
        """b12 s32 (b03's rulings, 261008): no tags, the base table, dropped plain, the Map's every method, a row per
        design Task in Runs, a UI design's screen, and the Task dropdown by step."""
        page = lambda folder, space, sub="": space_html(self.root, folder, space, sub)
        for folder, space, sub in ((self.job, "Description", "Inputs"), (self.job, "Audience Report", "Reason ideas"),
                                   (self.t00, "Audience Report", "Topics")):
            with self.subTest(view=sub):
                self.assertNotIn("class=chip", page(folder, space, sub))               # an id is mono text, no chip
        self.assertIn("<code>I04</code> &lt;idea 4&gt;", page(self.job, "Audience Report", "Reason ideas"))
        for folder, space, sub in ((self.block, "Work Details", "All"), (self.block, "Delivery", ""),
                                   (self.job, "Delivery", "designs.md"), (self.design, "Audience Report", "Drafts")):
            with self.subTest(view=f"{space} {sub}"):
                html = page(folder, space, sub)
                self.assertNotIn("display:grid", html)                                  # the base table, not a tile grid
                self.assertIn("wf-table", html)
        for folder, space, sub in ((self.t99, "Work Details", ""), (self.job, "Audience Report", "Design display"),
                                   (self.job, "Work Details", "Conduct & review")):
            with self.subTest(view=f"{space} {sub}"):
                self.assertNotIn("topic missing", page(folder, space, sub))            # dropped: plain and folded
        self.assertIn("Dropped by t99", page(self.t99, "Work Details"))
        heads = re.search(r"<thead>(.*?)</thead>", page(self.block, "Description", "Map"), re.S).group(1)
        for m in R.REGISTRY:                                                            # a column per registered method
            self.assertIn(m + " · ", heads)
        runs = page(self.job, "Runs", "Conduct & review")
        self.assertEqual(runs.count("<details"), 15)                                    # one row per design Task
        self.assertIn("t04_d04_ask-only", runs)
        shot = self.design / "screens" / "screen-1.png"                                 # a UI design: its rendered screen
        shot.parent.mkdir()
        shot.write_bytes(b"\x89PNG\r\n\x1a\n")
        html = page(self.job, "Audience Report", "Design display") + page(self.design, "Description", "Design")
        self.assertIn("screens/screen-1.png", html)
        select = frame.render(THEME, self.root, self.design, "Description")
        self.assertIn('<optgroup label="③ Conduct process">', select)
        self.assertIn(">Task · d04 · ask-only<", select)
        self.assertIn(">Task · t00 · reason ideas<", select)
        self.assertIn("· dropped<", select)

    def test_every_link_opens_something_that_exists(self):
        folders = [self.block, self.job, self.t00, self.design, self.t99]
        for folder in folders:
            for space, s in self.frame_of(folder).items():
                for sub in (s["subspaces"] or [""]):
                    html = space_html(self.root, folder, space, sub)
                    for url in re.findall(r'href="([^"]+)"', html):
                        url = unescape(url)
                        q = parse_qs(urlparse(url).query)
                        with self.subTest(folder=folder.name, space=space, sub=sub, url=url):
                            if url.startswith("/_board/page"):
                                self.assertTrue((self.root / q["path"][0].lstrip("/")).exists())
                            elif url.startswith("/_board/workbench"):
                                self.assertTrue((self.root / q["path"][0]).exists())
                            else:
                                self.assertTrue(url.startswith("/_board/guide"))

    def test_base_look_only(self):
        for folder in (self.block, self.job, self.design):
            html = space_html(self.root, folder, "Description")
            frame.render(THEME, self.root, folder, "Description")
            self.assertNotIn("<style", html)

    def test_a_by_method_block_keeps_todays_reading(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("tdt", HERE / "test_design_theme.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with tempfile.TemporaryDirectory() as tmp:
            root = mod.demo(tmp)
            block = root / "Project/designs/b01_demo_app"
            self.assertFalse(R.is_ladder(block))
            self.assertEqual(self.frame_of_root(root, block)["Description"]["subspaces"], ["Goal list", "Theory", "Rules"])

    def frame_of_root(self, root, folder):
        return {s["name"]: s for s in json.loads(frame.frame_json(THEME, root, folder))["spaces"]}


if __name__ == "__main__":
    unittest.main()
