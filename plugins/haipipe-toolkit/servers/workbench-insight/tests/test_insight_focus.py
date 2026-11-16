"""The insight pages on the focus page (insight_focus.py, b11 j01): the Report's letters, each Work view ⚙️ Process then
📊 Results (the Report's view by the same function), sign the plan before the close, the grid's cells their next verb;
and the shared page rules (haipipe-ui, 261106): every bar its state word, no 🙋 section of the theme's own, no count in
a side tab's label, the MindMap always a view."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page as FP  # noqa: E402
from live import insight_act as A  # noqa: E402
from live import insight_focus as IF  # noqa: E402
from live import insight_plan_c as P  # noqa: E402
from live.insight_theme import THEME  # noqa: E402
import plan_c_fixture as F  # noqa: E402

HEADS = re.compile(r"<h3 class=fd-h>(.*?)</h3>")
GROUPS = re.compile(r"<h3 class=pb-group>(.*?)</h3>")


class InsightFocusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.open = self.board / "j04_prototype-p2_data-demov3"          # open: its Runs planned, no page written
        self.closed = self.board / "j03_prototype-p2_data-demov2"        # closed: every page checked

    def tearDown(self):
        self.tmp.cleanup()

    def view(self, job: Path, key: str) -> str:
        return IF.job_work_views(job, self.root)["work-" + key][1]()

    def test_the_letters_of_the_report(self):
        self.assertEqual([n for n, _ in IF.job_work_views(self.open, self.root).values()],
                         ["Findings", "Changes", "Progress", "MindMap"])
        self.assertEqual(IF.job_work_views(self.board, self.root), {})          # the Board is not a Job
        self.assertEqual(IF.job_work_views(self.open / "t03_K01_question-c", self.root), {})

    def test_each_view_is_one_list_your_signs_in_overall(self):
        """JL 261111, "the Work is no longer used": its steps then its results, one numbered list, no band heading."""
        for key, _ in IF.VIEWS:
            html = self.view(self.open, key)
            self.assertEqual(GROUPS.findall(html), [], key)
            self.assertNotIn('<p class="view-caption">', html, key)
            self.assertFalse(any("🙋" in h for h in HEADS.findall(html)), key)     # no 🙋 of its own (R2)
        html = self.view(self.open, "overall")                    # your signs: a step of Overall's Process
        self.assertRegex(HEADS.findall(html)[0], r"^1 · 🔏 Sign and close")
        self.assertLess(html.index("Sign and close"), html.index("Close the Job"))   # sign before close
        self.assertNotIn("Sign and close", self.view(self.open, "grid"))

    def test_the_close_waits_until_every_step_is_done(self):
        html = self.view(self.open, "overall")
        self.assertIn("waits on the launch</span>", html)                 # one step as its word (round 1), the rest below
        self.assertIn("the launch, the runs, the pages, the checks", html)
        self.assertIn("<button type=button class=fd-btn disabled>Close</button>", html)
        self.assertNotIn('data-post="/_board/insight-act"', html)
        self.assertNotIn("What the close locks", html)              # shown once the close is yours to sign

    def test_an_unsigned_plan_waits_on_you(self):
        A.set_front(self.root / F.PROJECT / F.PROTO / "j02_p2" / "j02_p2.md", {"signed": ""})   # the plan p2
        html = self.view(self.open, "overall")
        self.assertIn('<span class="word you mk" title="1 waits for you">🙋 1</span>', html)   # the bar's mark, then its line
        self.assertIn("<p class=fd-wait>🙋 Sign ", html)
        self.assertIn("Sign in the Question Book", html)
        self.assertNotIn("is not signed", self.view(self.open, "overall"))   # the waiting line says it; no state sentence

    def test_the_grid_cells_carry_their_next_verb(self):
        html = self.view(self.open, "grid")
        self.assertEqual(html.count("🔲 Progress"), 1)              # one grid, not two
        self.assertIn('class="pb-pill ">launch</span>', html)        # a planned Run: launch it
        self.assertNotIn(">launch</span>", self.view(self.closed, "grid"))
        self.assertEqual(self.view(self.closed, "grid").count("<!--pb-prompt-->"), 0)   # nothing left to run

    def test_the_focus_page_shows_them_in_work(self):
        html = FP.render(THEME, self.root, self.open, "work", "work-grid")
        self.assertIn("🔲 Progress", html)
        self.assertIn("Overall", html)
        self.assertNotIn("Traceback", html)



class InsightLettersTest(unittest.TestCase):
    """The Board's Report and Work, the Job's Report, the Task's Report and Work (b11 j01 s51, s52, s54, s57, s58):
    a Report is its numbered sections only; an old Work view its steps then its results, one list (JL 261111)."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.job = self.board / "j04_prototype-p2_data-demov3"
        self.task = next(p for p in sorted(self.job.iterdir()) if p.is_dir() and p.name.startswith("t"))

    def tearDown(self):
        self.tmp.cleanup()

    def report_ok(self, views, keys):
        self.assertEqual(list(views), keys)
        for key, (_, build) in views.items():
            html = build()
            self.assertNotIn("<h3 class=pb-group>", html)                 # no band in a Report
            self.assertNotIn("Nothing waits on you", html)
            if key != "mindmap":
                self.assertRegex(html, r"<h3 class=fd-h>1 · ")
                self.assertIn("fd-fold:", html)                           # the fold script: bars start closed (R1)

    def work_ok(self, views, keys):
        self.assertEqual(list(views), ["work-" + k for k in keys] + ["work-mindmap"])   # the MindMap last (R6)
        for key, (_, build) in views.items():
            html = build()
            self.assertEqual(GROUPS.findall(html), [], key)              # no ⚙️ Process or 📊 Results heading
            self.assertNotIn('<p class="view-caption">', html, key)

    def test_board(self):
        keys = ["answers", "questions", "data", "handoff", "jobs"]
        self.report_ok(IF.board_report_views(self.board, self.root), keys)
        work = IF.board_work_views(self.board, self.root)
        self.work_ok(work, keys)
        self.assertRegex(HEADS.findall(work["work-questions"][1]())[0], r"^1 · 📋 The next question version")

    def test_job_report(self):
        views = IF.job_report_views(self.job, self.root)
        self.assertEqual(list(views), ["overall", "vs-previous", "grid", "mindmap"])
        for _, build in views.values():
            self.assertNotIn("<h3 class=pb-group>", build())

    def test_task(self):
        keys = ["answer", "across-jobs", "plan"]
        self.report_ok(IF.task_views(self.task, self.root, "report"), keys + ["mindmap"])   # its own map (round 2)
        work = IF.task_views(self.task, self.root, "work")
        self.work_ok(work, keys)
        chain = work["work-answer"][1]()
        self.assertGreaterEqual(chain.count("class=pb-todo>"), 6)           # the chain of roles, a row per link
        self.assertIn("checker · ", chain)
        self.assertNotIn("🙋", work["work-answer"][1]())                  # a Task never asks you

    def test_not_insight(self):
        self.assertEqual(IF.board_report_views(self.root, self.root), {})
        self.assertEqual(IF.task_views(self.root, self.root, "work"), {})

    def test_a_question_with_no_run_shows_its_answer(self):
        """W01 cites the answers below it and has no Run: what it found is its newest answer, not "Not asked"."""
        html = IF.board_report_views(self.board, self.root)["answers"][1]()
        found = html.split("🔎 Answers", 1)[1]
        self.assertNotIn("Not asked on this segment", found)
        self.assertIn("it cites the answers below it", found)
        jobs = IF.board_report_views(self.board, self.root)["jobs"][1]()
        self.assertIn("cites the answers below it", jobs)                  # W01 has no Run, by design: never "not run"

    def test_a_cross_only_question_shows_its_cross_answer(self):
        """A question asked only on cross has no Run on full: what it found is its cross answer, named as such."""
        for job in sorted(p for p in self.board.iterdir() if p.is_dir() and p.name.startswith("j0")):
            for t in job.glob("t*_K02_*/runs/r0[1-3]_*"):
                import shutil
                shutil.rmtree(t)
        html = IF.board_report_views(self.board, self.root)["answers"][1]()
        row = html.split("id=question-K02", 1)[1].split("id=question-", 1)[0]
        self.assertNotIn("Not asked on this segment", row)
        self.assertIn("asked on cross", row)

    def test_a_draft_plan_reads_its_kept_questions_from_the_newest_job(self):
        """A next plan no Job runs yet: its kept questions read their newest Job's page on the canvas, the one count's
        rule (round 1: the counts must agree); Questions no longer lists each answer, which Answers holds (shown once)."""
        proto = self.root / F.PROJECT / F.PROTO
        draft = proto / "j03_p3"
        F._write(draft / "j03_p3.md", F._front({"release": "p3", "state": "open", "signed": "", "from": "p2"}, "# p3\n"))
        F._write(draft / "release.yaml", "release: p3\nquestions:\n  D01: {task: ../j01_p1/t01_D01_question-a, change: kept}\n")
        html = IF.board_report_views(self.board, self.root)["questions"][1]()
        self.assertNotIn("Each question and its answer", html)
        self.assertIn('"id": "D01"', html)
        self.assertIn('"state": "open"', html)                         # the newest Job's page, not an older answer

    def test_a_question_with_no_run_rests_on_what_it_cites(self):
        """W01 has no Run: its Answer rests on, and its By segment lists, the Tasks its page cites, never "no Run yet"."""
        w = next(p for p in self.job.iterdir() if p.name.startswith("t05_W01"))
        page = w / f"{w.name}.md"
        page.write_text(page.read_text(encoding="utf-8") + "\n- It rests on the test (K01 · t03).\n", encoding="utf-8")
        views = IF.task_views(w, self.root, "report")
        self.assertIn("K01", views["answer"][1]().split("How sure", 1)[1])
        self.assertNotIn("no Run yet", views["answer"][1]())
        self.assertIn("What it cites", views["answer"][1]())             # By segment is a section of Answer (JL 261109)

    def test_a_collection_run_is_not_a_cut(self):
        """A 🙋 form under a Task (runs/rNN_collect_<slug>/, kind hard, type collect) is no segment of its question."""
        from live import insight_plan_c as P
        F._write(self.task / "runs" / "r09_collect_a_form" / "run.yaml", "run: r09_collect_a_form\nkind: hard\ntype: collect\nstatus: waiting\n")
        self.assertNotIn("r09_collect_a_form", [h["run"] for h in P.task(self.task)["hard"]])

    def test_an_executive_figure_is_read_under_its_task(self):
        from live import insight_views as V
        from live import insight_plan_c as P
        j = P.job(self.job)
        t = j["tasks"][0]
        part = self.board / "delivery" / self.job.name
        self.assertEqual(V._fig_png(part, j, t["qid"], "a"), part / "figures" / f'{t["qid"]}-a.png')   # the older place
        F._write(part / t["name"] / f'{t["qid"]}-a.png', "png")
        self.assertEqual(V._fig_png(part, j, t["qid"], "a"), part / t["name"] / f'{t["qid"]}-a.png')

    def test_an_unsigned_handoff_waits_for_your_sign(self):
        F._write(self.board / "delivery" / "handoff-w02.md", F._front({"counsel": "W02", "job": "j03_prototype-p2_data-demov2",
                                                                       "signed": ""}, "# W02 · a draft\n"))
        work = IF.board_work_views(self.board, self.root)["work-handoff"][1]()
        self.assertIn("Sign the advice W02", work)
        self.assertIn("waiting for you", work.split("Sign the advice W02", 1)[1][:400])
        self.assertIn("<p class=fd-wait>🙋 Sign the advice W02", work)          # its waiting line, under the closed bar
        self.assertIn("W02 waits for your sign", IF.board_report_views(self.board, self.root)["handoff"][1]())

    # ── the shared page rules (haipipe-ui, 261106) ──────────────────────────────────────────────────────────────
    def every_view(self):
        """(where, html) of every insight view of the fixture's Board, a Job and a Task, Report and Work."""
        tasks = [p for p in sorted(self.job.iterdir()) if p.is_dir() and p.name.startswith("t")]
        sets = [("board report", IF.board_report_views(self.board, self.root)),
                ("board work", IF.board_work_views(self.board, self.root)),
                ("job report", IF.job_report_views(self.job, self.root)),
                ("job work", IF.job_work_views(self.job, self.root))]
        for t in tasks:
            sets += [(t.name + " report", IF.task_views(t, self.root, "report")),
                     (t.name + " work", IF.task_views(t, self.root, "work"))]
        for where, views in sets:
            for key, (_, build) in views.items():
                yield f"{where} {key}", build()

    def test_a_bar_has_a_mark_or_nothing(self):
        """A numbered bar never shows a state word: on its right sits an orange 🙋 (with how many wait for you), a quiet
        ✓, or nothing. The state never sits in the title either."""
        mark = r'<span class="word you mk" title="[^"]*">🙋(?: \d+)?</span>|<span class="word ok mk" aria-label="done">✓</span>'
        for where, html in self.every_view():
            for head in HEADS.findall(html):
                title, _, right = head.partition("<span")
                self.assertRegex("<span" + right if right else "", rf"^(?:{mark})?$", f"{where}: {head}")
                self.assertNotRegex(title, r"Nothing waits|Waits on you|Next: ", where)

    def test_no_view_draws_its_own_interaction(self):
        """R2: 🙋 Interaction is the page's, added last to every view; no insight view draws a 🙋 section."""
        for where, html in self.every_view():
            self.assertFalse([h for h in HEADS.findall(html) if "🙋" in h.partition("<span")[0]], where)   # a bar's 🙋 mark is not a section

    def test_no_count_in_a_side_tab_label(self):
        """R4: a side tab's label carries no count; its state is a word ("partly answered")."""
        for where, html in self.every_view():
            for label in re.findall(r'class="pb-item[^"]*"[^>]*><b>(.*?)</b>', html):
                self.assertNotRegex(label, r"\(\d+\)|\b\d+ (questions|Tasks|runs|Jobs|open)\b", f"{where}: {label}")
        side = IF.board_report_views(self.board, self.root)["answers"][1]()
        self.assertIn("pb-tabset pb-side", side)                         # what each question found: side tabs

    def test_report_view_is_work_results(self):
        """R3: each Work view ends on its Report view, drawn by the same function: the same large line and the same
        sections, in order, after its steps (JL 261111: one list, no 📊 Results heading)."""
        titles = lambda html: [re.sub(r"<span class=\"?word.*|^\d+ · ", "", h) for h in HEADS.findall(html)]
        big = lambda html: re.findall(r"<p class=in-big>(.*?)</p>", html)
        pairs = [(IF.board_report_views(self.board, self.root), IF.board_work_views(self.board, self.root)),
                 (IF.job_report_views(self.job, self.root), IF.job_work_views(self.job, self.root)),
                 (IF.task_views(self.task, self.root, "report"), IF.task_views(self.task, self.root, "work"))]
        for report, work in pairs:
            for key, (_, build) in report.items():
                if key == "mindmap":
                    continue
                res, shown = work["work-" + key][1](), build()
                self.assertEqual(titles(res)[len(titles(res)) - len(titles(shown)):], titles(shown), key)
                self.assertEqual(big(res)[len(big(res)) - len(big(shown)):], big(shown), key)

    def test_vs_previous_waits_for_a_second_job(self):
        """JL 261106: the vs previous button stays hidden until a second Job exists."""
        first = self.board / "j01_prototype-p1_data-demov1"
        self.assertNotIn("vs-previous", IF.job_report_views(first, self.root))
        self.assertNotIn("work-vs-previous", IF.job_work_views(first, self.root))
        self.assertIn("vs-previous", IF.job_report_views(self.job, self.root))

    def test_each_form_goes_to_its_view(self):
        """R2: a form's view by what it is about (view_of_item): a Wisdom Task's under Handoff at the Board, a Task's
        under Grid at its Job, an Executive one's under Overall."""
        w = next(p for p in self.job.iterdir() if p.name.startswith("t05_W01"))
        x = next((p for p in self.job.iterdir() if re.match(r"t\d+_X", p.name)), None)
        k = next(p for p in self.job.iterdir() if re.match(r"t\d+_K", p.name))
        keys = ["answers", "questions", "jobs", "data", "handoff", "mindmap"]
        self.assertEqual(IF.view_of_item({"page": w}, self.board, self.root, "Block", keys), "handoff")
        self.assertEqual(IF.view_of_item({"page": k}, self.board, self.root, "Block", keys), "jobs")
        self.assertEqual(IF.view_of_item({"page": k}, self.job, self.root, "Job", ["overall", "grid"]), "grid")
        if x is not None:
            self.assertEqual(IF.view_of_item({"page": x}, self.job, self.root, "Job", ["overall", "grid"]), "overall")
        self.assertEqual(IF.view_of_item({"page": k}, k, self.root, "Task", ["answer"]), "answer")

if __name__ == "__main__":
    unittest.main()


class RoundOneTest(unittest.TestCase):
    """The b11 design loop's round 1 (261106): a Question Book's own parts and state words, one count for every "N of M",
    the Grid's question opening its answer, a freeze's folder found from any root, a cite-only Task's By segment."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.proto = self.root / F.PROJECT / F.PROTO
        self.job = self.board / "j04_prototype-p2_data-demov3"

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_prototype_shows_its_questions_and_their_state_words(self):
        parts = IF.prototype_parts(self.proto, self.root, "Block")
        self.assertEqual([p[0] for p in parts], ["❓ Questions", "📮 Ideas", "✂️ Segments"])
        self.assertIn("2 wait for you", [p[1] for p in parts])                 # two open proposals, the person's
        status = IF.prototype_status(self.proto, self.root, "Block")
        self.assertTrue(all(s[1] == "✅" for s in status))                       # release.yaml's state and sign, as a mark
        words = " ".join(s[1] for s in status) + "".join(s[2] for s in status)
        for gone in ("no state", "not run", "0 of"):
            self.assertNotIn(gone, words)
        job = next(p for p in sorted(self.proto.iterdir()) if p.name.startswith("j01_"))
        self.assertEqual([s[0] for s in IF.prototype_status(job, self.root, "Job")], ["📜 The release"])  # questions:
        levels = IF.prototype_parts(job, self.root, "Job")[0]                   # Findings' (round 2)
        self.assertEqual(levels[0], "❓ Questions")                             # by DIKW level at a release
        self.assertEqual(levels[1], "✅")                                       # its state as a mark

    def test_a_prototype_is_signed_and_triaged_on_its_own_work(self):
        """Round 2: the Question Book's Work · Findings carries the triage and the sign, each a Copy prompt for
        /haipipe-insight; Status says "nothing to do" when nothing waits; a release's map groups its questions by
        DIKW level; Status and Findings each open with a main line."""
        A.set_front(self.root / F.PROJECT / F.PROTO / "j02_p2" / "j02_p2.md", {"signed": "", "state": "draft"})
        steps = IF.prototype_process(self.proto, self.root, "Block", "findings")
        body = steps[0][2]
        self.assertIn("Sort the open ideas", body)
        self.assertIn("Sign ", body)
        self.assertIn("/haipipe-insight ", body)
        self.assertIn("for you", steps[0][1])
        job = next(p for p in sorted(self.proto.iterdir()) if p.name.startswith("j01_"))
        self.assertEqual(IF.prototype_process(job, self.root, "Job", "standing")[0][1], "✅")
        self.assertIsNone(IF.prototype_process(job, self.root, "Job", "mindmap"))
        levels = [lv for lv, _ in IF.prototype_map_branches(job, self.root, "Job")]
        self.assertTrue(levels and set(levels) <= {"Data", "Information", "Knowledge", "Wisdom", "Executive"})
        self.assertIn("✅", IF.prototype_lead(job, self.root, "Job", "standing"))
        self.assertRegex(IF.prototype_lead(job, self.root, "Job", "findings"), r"\d+ questions")
        for _, _, panel in IF.prototype_delivery_tabs(self.proto, self.root, "Block"):
            self.assertNotIn("Nothing handed over yet", panel)

    def test_every_count_reads_one_function(self):
        from live import insight_views as V
        j = P.job(self.job)
        done, asked = V.written_of(j["tasks"])
        grid = IF.job_report_views(self.job, self.root)["grid"][1]()
        self.assertIn(V.far(done, asked, "answered"), grid)                    # a state word, never a tally
        self.assertNotRegex(grid, r"\d+ of \d+ (answered|written)")
        jobs = IF.board_report_views(self.board, self.root)["jobs"][1]()
        self.assertIn(V.far(done, asked, "written"), jobs)                     # the same Job, the same word (the
        answers = IF.board_report_views(self.board, self.root)["answers"][1]()  # plans × freezes: Jobs' alone, round 2)
        self.assertNotIn("Question versions × data versions", answers)

    def test_the_grid_question_opens_its_answer(self):
        grid = IF.job_report_views(self.job, self.root)["grid"][1]()
        self.assertIn('href="/_board/insight-run?answer=', grid)
        self.assertNotRegex(grid, r'insight-run\?run=[^"]*/t\d+_[DIKWX]\d+_[a-z-]+"')   # a Task is no Run ("No such run.")

    def test_a_freeze_folder_is_found_from_a_tools_root(self):
        tools = self.root / "Tools"
        data = tools / "blueprints" / "data" / "v1"
        data.mkdir(parents=True)
        v = {"version": "v1", "folder": "Tools/blueprints/data/v1/"}
        self.assertEqual(P.version_folder(v, tools), data.resolve())
        self.assertEqual(P.version_folder(v, self.root), data.resolve())

    def test_a_cite_only_task_keeps_by_cut_and_gathers_what_it_cites(self):
        w = next(p for p in self.job.iterdir() if p.name.startswith("t05_W01"))
        page = w / f"{w.name}.md"
        page.write_text(page.read_text(encoding="utf-8") + "\n- It rests on the test (K01 · t03).\n", encoding="utf-8")
        report = IF.task_views(w, self.root, "report")
        self.assertNotIn("by-cut", report)                                         # a section of Answer now (JL 261109)
        self.assertIn("🔗 What it cites", report["answer"][1]())
        work = IF.task_views(w, self.root, "work")
        self.assertNotIn("Next on each segment", work["work-answer"][1]())
        self.assertNotIn("A new segment", work["work-answer"][1]())
        self.assertIn("Gather what it cites", work["work-answer"][1]())
        self.assertNotIn("Run every segment", work["work-answer"][1]())


class QuestionMapTest(unittest.TestCase):
    def test_the_dots_map_keeps_executive_on_top(self):
        """Dots: Executive is a row across the top in number order, never a fifth column; its lines are marked so
        they stay faint until lit (workbench-insight ref/topics.md T08)."""
        from live import question_canvas as QC
        net = QC.JS[QC.JS.index("function drawNet()"):QC.JS.index("function dot(")]
        self.assertIn("cols=['D','I','K','W']", net)
        self.assertNotIn("'W','X']", net)
        self.assertIn("keep('X').sort(num)", net)
        self.assertIn("'e ex'", net)
        self.assertIn("path.e.ex:not(.down):not(.up)", QC.CSS)
