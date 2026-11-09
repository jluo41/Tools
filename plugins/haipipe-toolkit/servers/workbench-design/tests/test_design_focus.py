"""The design theme on the focus page (design_focus.py, b12 j01 s51 to s58): the Block, a Job and each Task type in the
cells' letters on the shared page rules (haipipe-ui, 261106): every bar a state word, Report the Results only, Work ⚙️
Process then the same 📊 Results, a person's sign a Process step (never a 🙋 section of the view's own), 🙋 Interaction
last with the view's own forms, side tabs with no count in a label, the MindMap at every level; a Task never asks you."""
from __future__ import annotations

import html as H
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import design_focus as D  # noqa: E402
from live import focus_page as FP  # noqa: E402
from live.design_theme import THEME  # noqa: E402
import design_fixture as F  # noqa: E402
from test_design_act import set_state  # noqa: E402

GROUPS = re.compile(r"<h3 class=pb-group>(.*?)</h3>")
HEADS = re.compile(r"<h3 class=fd-h>(.*?)</h3>")
BAR = re.compile(r"<h3 class=fd-h>(\d+ · .*?)</h3>", re.S)
WORD = re.compile(r'<span class=(?:word|"word you")>[^<]+</span>')
TAB = re.compile(r'<button type=button class="pb-item[^"]*" data-pbtab="[^"]*"><b>(.*?)</b>')


def title(head: str) -> str:
    """A bar's title: its words without the number and the state word."""
    return H.unescape(re.sub(r"<[^>]+>", "", WORD.sub("", re.sub(r"^\d+ · ", "", head)))).strip()


class DesignFocusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = F.make(self.root) / F.BLOCK
        self.job = self.block / "j03_g01_m04"
        self.tasks = sorted(p for p in self.job.iterdir() if p.is_dir() and p.name.startswith("t"))

    def tearDown(self):
        self.tmp.cleanup()

    def names(self, folder: Path, section: str) -> list:
        return [n for n, _ in D.views(folder, self.root, section).values()]

    def test_each_level_has_the_cells_letters(self):
        self.assertEqual(D.level_of(self.block), "Block")
        self.assertEqual(self.names(self.block, "work"), ["Summary", "Goals", "Jobs", "Rounds", "Methods", "MindMap"])
        self.assertEqual(self.names(self.job, "report"), ["Setup", "Ideas", "Designs", "Ranking", "Release"])
        by_kind = {D.R.kind_of(t): self.names(t, "work") for t in self.tasks}
        self.assertEqual(by_kind["t00"], ["Inputs", "Chains", "Ideas", "Fence check", "MindMap"])
        self.assertEqual(by_kind["design"], ["Draft", "Verify", "Revise", "State", "MindMap"])
        self.assertEqual(by_kind["t99"], ["Rank", "Coverage", "Kept", "MindMap"])
        # Report keys are plain, Work's the same keys with work- (R3: the rail's same views and rail_view read them so)
        for folder in (self.block, self.job, *self.tasks):
            report, work = D.views(folder, self.root, "report"), D.views(folder, self.root, "work")
            self.assertFalse(any(k.startswith("report-") for k in report), folder.name)
            self.assertEqual({"work-" + k for k in report} | {"work-mindmap"}, set(work), folder.name)
        self.assertEqual(D.views(self.root, self.root, "work"), {})              # not a design page: the base page stays

    def test_report_is_its_sections_work_is_process_then_results(self):
        for folder in (self.block, self.job, *self.tasks):
            for key, (_n, build) in D.views(folder, self.root, "report").items():
                html = build()
                self.assertEqual(GROUPS.findall(html), [], (folder.name, key))          # Report: its sections only
                self.assertRegex(HEADS.findall(html)[0], r"^1 · ", (folder.name, key))
                self.assertNotIn("Waits on you", html)
            for key, (_n, build) in D.views(folder, self.root, "work").items():
                html = build()
                want = ["📊 Results"] if key == "work-mindmap" else ["⚙️ Process", "📊 Results"]
                self.assertEqual(GROUPS.findall(html), want, (folder.name, key))
                self.assertNotIn("Traceback", html)

    def test_a_job_ready_to_release_waits_on_you(self):
        for k, t in enumerate(t for t in self.tasks if D.R.kind_of(t) == "design"):    # t99 ranked, three kept, not signed
            if k < 3:
                set_state(t / f"{t.name}.md", "kept")
                pred = yaml.safe_load((t / "prediction.yaml").read_text())
                (t / "prediction.yaml").write_text(yaml.safe_dump({**pred, "frozen": "draft"}, allow_unicode=True))
        for r in ("run-release-j03", "run-freeze-predictions-j03"):
            shutil.rmtree(self.job / "runs" / r)
        job = D.views(self.job, self.root, "work")["work-release"][1]()
        process = job.split("📊 Results")[0]
        self.assertIn('<span class="word you">1 waits for you</span>', process)     # a Process step, its word and line
        self.assertIn("<p class=fd-wait>🙋 Review and approve", process)
        self.assertIn('data-post="/_board/design-ladder-act"', process)        # the sign, on the Release view's Process
        block = D.views(self.block, self.root, "work")["work-jobs"][1]()
        self.assertIn("Review and approve · ", block.split("📊 Results")[0])
        self.assertIn("j03_g01_m04", block.split("📊 Results")[0])

    def test_a_released_job_waits_on_you_to_close(self):
        self.assertTrue(D.V._approved(D.R.job(self.job))[0])                         # the fixture's j03 is released
        job = D.views(self.job, self.root, "work")["work-release"][1]()
        self.assertIn("<p class=fd-wait>🙋 Close the Job", job.split("📊 Results")[0])  # the close is a person's sign
        block = D.views(self.block, self.root, "work")["work-jobs"][1]()
        self.assertIn("Close the Job · ", block.split("📊 Results")[0])
        summary = D.views(self.block, self.root, "report")["summary"][1]()
        self.assertIn("<p class=fd-wait>🙋 Close the Job", summary)              # flagged on the Report too, under its bar

    def test_a_task_never_asks_you(self):
        for t in self.tasks:
            for _n, build in D.views(t, self.root, "work").values():
                html = build()
                self.assertNotIn("waiting for you", html, t.name)
                self.assertNotIn('data-post=', html, t.name)

    def pages(self):
        return (self.block, self.job, *self.tasks)

    def test_every_design_bar_has_a_word(self):
        """R1: every numbered bar of every Report and Work view carries its state word (the page's own 🙋 too)."""
        missing, seen = [], 0
        for folder in self.pages():
            for section in ("report", "work"):
                for key in FP.render(THEME, self.root, folder, section) and D.views(folder, self.root, section):
                    for m in BAR.finditer(FP.render(THEME, self.root, folder, section, key)):
                        seen += 1
                        if not WORD.search(m.group(1)):
                            missing.append(f"{folder.name} {section} {key}: {title(m.group(1))}")
        self.assertGreater(seen, 150)
        self.assertEqual(missing, [])

    def test_no_view_draws_its_own_interaction(self):
        """R2: a design view draws no 🙋 section; the page adds one 🙋 Interaction, the last section of the view."""
        for folder in self.pages():
            for section in ("report", "work"):
                for key, (_n, build) in D.views(folder, self.root, section).items():
                    own = [title(h) for h in HEADS.findall(build())]
                    self.assertFalse([t for t in own if "🙋" in t], (folder.name, key, own))
                    page = FP.render(THEME, self.root, folder, section, key)
                    heads = [title(h) for h in HEADS.findall(page.split('class="focus-card', 1)[-1])]
                    if folder == self.block:
                        self.assertIn('🧭 Around the Work', page)
                        self.assertIn('🙋 Interactions', page)
                        self.assertNotIn('🙋 Interaction', heads)
                        continue
                    self.assertEqual([t for t in heads if "🙋" in t], ["🙋 Interaction"], (folder.name, key))
                    self.assertEqual(heads[-1], "🙋 Interaction", (folder.name, key))

    def test_the_report_view_is_the_work_results(self):
        """R3: a Work view's 📊 Results are its Report view, drawn by the same function."""
        for folder in self.pages():
            report, work = D.views(folder, self.root, "report"), D.views(folder, self.root, "work")
            for key, (_n, build) in report.items():
                shown = build()
                res = work["work-" + key][1]().split("<h3 class=pb-group>📊 Results</h3>", 1)[1].split("<script>", 1)[0]
                res = re.sub(r"<p class=dz-next>.*?</p>$", "", res)               # Work ends on where the next step is
                self.assertIn(res, shown, (folder.name, key))
                self.assertNotIn("pb-copy", res, (folder.name, key))            # Report shows, Work asks

    def test_the_mindmap_is_shown_at_every_level(self):
        """R6: the shared MindMap stays a view at the Block, the Job and the Task, last; Report opens on its first letter."""
        for folder, first in ((self.block, "Summary"), (self.job, "Setup"), (self.tasks[0], "Inputs")):
            page = FP.render(THEME, self.root, folder, "report", "")
            nav = re.search(r'<nav class="section-views".*?</nav>', page, re.S).group(0)
            names = re.findall(r">([^<>]+)</a>", nav)
            self.assertEqual(names[-1], "MindMap", folder.name)
            self.assertIn(f'aria-current="page">{first}</a>', nav)
            self.assertIn("focus-map", FP.render(THEME, self.root, folder, "report", "mindmap"))
            self.assertIn("focus-map", FP.render(THEME, self.root, folder, "work", "work-mindmap"))
        self.assertIn('aria-current="page">Summary</a>', FP.render(THEME, self.root, self.block, "report", "summary"))

    def test_labels_carry_no_counts(self):
        """R4: a bar's title, a side tab's name and a view button carry no count; lists of items are side tabs."""
        for folder in self.pages():
            for section in ("report", "work"):
                for key, (name, build) in D.views(folder, self.root, section).items():
                    html = build()
                    self.assertNotRegex(name, r"\d", (folder.name, key))
                    for h in HEADS.findall(html):
                        self.assertNotRegex(title(h), r"\d", (folder.name, key, h))
                    for t in TAB.findall(html):
                        self.assertNotRegex(H.unescape(re.sub(r"<[^>]+>", "", t)), r"·\s*\d+\s*$|\(\d+\)", (folder.name, key, t))
                    self.assertNotIn('<details class="topic', html, (folder.name, key))   # no folds of items

    def test_each_view_shows_its_own_forms(self):
        """R2: a form at a Job's Task shows under that step's Job view and under the Block's Jobs, nowhere else."""
        t99 = next(t for t in self.tasks if D.R.kind_of(t) == "t99")
        run = t99 / "runs" / "r01_collect_rank_rule"
        run.mkdir(parents=True)
        (run / "run.yaml").write_text("status: waiting\n", encoding="utf-8")
        (run / "question_collection.md").write_text("# Rank rule asks\n\nfor: rank rule\n\n## Q1 · Rule\n\nWhy.\n\n"
                                                    "**Which?**\n\n- [ ] A · a\n- [ ] B · b\n", encoding="utf-8")
        (run / "r01_collect_rank_rule.html").write_text("<!doctype html>", encoding="utf-8")
        for folder, home in ((self.job, "ranking"),):
            for key in D.views(folder, self.root, "report"):
                last = FP.render(THEME, self.root, folder, "report", key).split("🙋 Interaction")[-1]
                (self.assertIn if key == home else self.assertNotIn)("Rank rule asks", last, (folder.name, key))
        # Block support now requires an explicit View/Topic; the unassigned question stays in the rail.
        for key in D.views(self.block, self.root, "report"):
            self.assertNotIn("Rank rule asks", FP.render(THEME, self.root, self.block, "report", key))
        self.assertIn("Rank rule asks", FP.render(THEME, self.root, self.block, "interactions"))
        self.assertEqual(D.view_of_item({"page": self.job, "about": "release choices @ next test arm"}, self.job,
                                        self.root, "Job", ["setup", "release", "mindmap"]), "release")

    def test_a_goal_pin_names_its_goal(self):
        """A Job face pins `goal: G01 · <name>` (the map reads the name); every reader takes the id before it."""
        face = self.job / f"{self.job.name}.md"
        face.write_text(face.read_text(encoding="utf-8").replace("goal: G01", "goal: G01 · a-name", 1), encoding="utf-8")
        self.assertEqual(D.R.job(self.job)["goal"], "G01")
        self.assertEqual(D.R.goal_pin("G01 · a-name"), "G01")
        self.assertEqual(D.goal_line(self.job, "G01 · a-name"), D.goal_line(self.job, "G01"))
        self.assertTrue(D.goal_line(self.job, "G01"))

    def test_the_focus_page_shows_them(self):
        page = FP.render(THEME, self.root, self.job, "work", "work-designs")
        self.assertIn("Each design", page)
        self.assertIn(">Setup<", page)
        self.assertIn("Summary", FP.render(THEME, self.root, self.block, "report", ""))


if __name__ == "__main__":
    unittest.main()
