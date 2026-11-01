"""A building Task's focus page (labeling_focus.building_page) and its Decide view (decision_report_view.py).

A placeholder Project (test_labeling_theme.project and items_task) with a building Task whose face says
`task-type: labeling-building` and a goal line. BuildingPageTest needs no decision store: the page's shell, rails and
views, the honest states. DecideViewTest writes real records through the labeling engine's own store
(meaning_store.py: publish_report, save_draft, submit_feedback) into the Task's lane, labeling/meaning/, and reads them
back through the page; it skips when that store is absent. Every word is a placeholder; rendering writes nothing."""
from __future__ import annotations

import html
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap, skill_dir  # noqa: E402
bootstrap()

from live import decision_report_view as DR  # noqa: E402
from live import focus_page as F  # noqa: E402
from live import frame, labeling_focus as L  # noqa: E402
from test_labeling_theme import items_task, project  # noqa: E402

ENGINE = skill_dir("labeling") / "engine"
GOAL = "a standard you sign, frozen for labeling at scale"
QUESTIONS = ("Can practical help count as support?", "Does this item have the wrong label?", "What makes a case hard?")


def building_task(job: Path) -> Path:
    folder = job / "t03_demo_building"
    folder.mkdir()
    (folder / "t03_demo_building.md").write_text(f"# Demo building\nstate: 🔴 OPEN\ntask-type: labeling-building\n"
                                                 f"goal: {GOAL}\n\n## Opening\n\nA placeholder building Task.\n")
    return folder


def card(did: str, short: str, question: str) -> dict:
    case = lambda role, text: {"item_ref": f"L{did}-{role}", "split": "train", "role": role,
                               "context": "Person: a placeholder turn", "text": text, "signal": "a placeholder signal"}
    return {"decision_id": did, "short_title": short, "question_type": "boundary", "question": question,
            "why_now": "a placeholder reason", "current_rule": "a placeholder rule",
            "evidence": [case("case_a", "<a reply that offers practical help>"),
                         case("case_b", "<a reply that offers reassurance>")],
            "options": [{"option_id": "A", "label": "Count it", "effect": "a placeholder effect", "scope": "a rule"},
                        {"option_id": "B", "label": "Do not count it", "effect": "a placeholder effect", "scope": "a rule"}],
            "none_allowed": True, "defer_allowed": True, "comments_allowed": True,
            "approval_scope": "preference_only", "source_ids": ["S01"]}


def report(rid: str, round_id: str, cards: list, revision: int = 1) -> dict:
    return {"schema": "labeling.decision_report", "schema_version": 1, "job_id": "demo_job", "report_id": rid,
            "report_revision": revision, "round_id": round_id, "title": f"Placeholder {rid}",
            "purpose": "a placeholder purpose",
            "base": {"task_frame_version": "f01", "meaning_version": "m02", "reference_version": "l02",
                     "split_version": "s01"},
            "sources": [{"source_id": "S01", "kind": "human_idea", "label": "A placeholder idea"}],
            "cards": cards, "synthetic": True}


def views_bar(page: str) -> str:
    return page.split('<nav class="section-views" aria-label="Views">', 1)[1].split("</nav>", 1)[0]


def rail(page: str, label: str) -> str:
    return page.split(f'aria-label="{label}">', 1)[1].split("</nav>", 1)[0]


def current_view(page: str) -> str:
    return re.search(r'<a [^>]*aria-current="page">([^<]+)</a>', views_bar(page)).group(1)


def content(page: str) -> str:
    """The open view's own markup: the page's card, without the stylesheets and scripts that ride with it."""
    return page.split('<section class="focus-card">', 1)[1].split("</section><footer>", 1)[0]


def rows(page: str) -> list:
    """The inbox: (question, pill class, pill word, Open expanded) per row."""
    return re.findall(r'<div class="dec-row[^"]*" data-row="\d+"><p class="dec-rq">(.*?)</p><span class="dec-pill (\w+)" '
                      r'data-pill="\d+" data-state="\w+">(.*?)</span><button [^>]*aria-expanded="(\w+)"[^>]*>Open</button>',
                      page)


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root, self.block, self.labeling = project(self.temp.name)
        self.root = self.root.resolve()
        self.items = items_task(self.labeling.parent)
        self.task = building_task(self.labeling.parent).resolve()
        self.lane = self.task / "labeling"
        self.theme = frame.themes()["labeling"]

    def tearDown(self):
        self.temp.cleanup()

    def render(self, section="", group=""):
        return L.render(self.theme, self.root, self.task, section, group)


class BuildingPageTest(Fixture):
    """The page itself: the base page's shell and rails, its views, and what it says with no report or no store."""

    def test_the_view_buttons_and_the_aim(self):
        page = self.render("work")
        bar = views_bar(page)
        for key, name in (("frame", "Frame"), ("decide", "Decide"), ("changes", "Changes"), ("staging", "Staging"),
                          ("release", "Release"), ("runs", "Runs")):
            self.assertIn(f"section=work&amp;group={key}\"", bar)
            self.assertIn(f">{name}</a>", bar)
        self.assertIn(">Work</span></h1>", page)
        self.assertIn('<span class="goal-word">Aim</span>', page)
        self.assertIn(GOAL, page)
        self.assertIn("section=report&amp;group=decide", views_bar(self.render("report")))

    def test_shell_and_rails_are_the_base_pages(self):
        mine, base = self.render("work"), F.render(self.theme, self.root, self.task, "work")
        self.assertEqual(rail(mine, "Page sections"), rail(base, "Page sections"))
        self.assertEqual(rail(mine, "Pages"), rail(base, "Pages"))
        self.assertEqual(rail(mine, "Sections"), rail(base, "Sections"))   # the phone's section-line
        crumb = lambda p: p.split('<div class="focus-crumb">', 1)[1].split("</div>", 1)[0]
        self.assertEqual(crumb(mine), crumb(base))
        goal = lambda p: p.split('<div class="focus-goal">', 1)[1].split("</div>", 1)[0]
        self.assertEqual(goal(mine), goal(base))
        self.assertIn("Open this page&#x27;s Markdown", mine)
        for key in ("interactions", "delivery", "files"):
            self.assertIn(f"section={key}", rail(mine, "Page sections"))
        report = self.render("report")
        self.assertEqual(rail(report, "Page sections"), rail(F.render(self.theme, self.root, self.task, "report"),
                                                               "Page sections"))

    def test_the_base_sections_are_the_base_pages(self):
        for section in ("interactions", "delivery", "files", "folders"):
            with self.subTest(section=section):
                self.assertEqual(self.render(section), F.render(self.theme, self.root, self.task, section))

    def test_other_labeling_pages_are_unchanged(self):
        for folder, section in ((self.labeling, ""), (self.labeling, "definition"), (self.items, "items"),
                                (self.labeling.parent, "timeline")):
            with self.subTest(page=folder.name, section=section):
                page = L.render(self.theme, self.root, folder, section)
                self.assertIn('<main class="focus-page labeling-focus">', page)
                self.assertNotIn("dec-view", page)
                self.assertNotIn("decisionReportView", page)
        self.assertFalse(L.is_building(self.labeling))               # today's labeling Page is building and scanning
        self.assertTrue(L.is_building(self.task))

    def test_honest_state_without_a_store(self):
        with patch.object(DR, "store", return_value=None):
            self.assertEqual(current_view(self.render("work")), "Frame")
            for section in ("work", "report"):
                body = content(self.render(section, "decide"))
                self.assertIn('<p class="dec-big">The decision store is not available</p>', body)
                self.assertNotIn("data-dec-form", body)
                self.assertNotIn("dec-row", body)

    def test_unbuilt_steps_name_what_they_will_show_and_make_up_nothing(self):
        for key, caption in (("frame", "The task: the label, who decides, its values."),
                             ("changes", "What your answers changed, and the labels it touches."),
                             ("staging", "This round&#x27;s run, and where its report sends it."),
                             ("release", "What is frozen, and whether it is ready.")):
            with self.subTest(view=key):
                body = content(self.render("work", key))
                self.assertIn(caption, body)
                self.assertIn("Nothing to show yet", body)
                self.assertNotRegex(re.sub(r"<[^>]+>", "", body), r"\d{2}")
        self.assertIn("next: 🧪 Staging →", content(self.render("work", "changes")))
        self.assertIn("next: 🙋 Decide →", content(self.render("work", "frame")))
        self.assertNotIn("dec-next", content(self.render("work", "release")))
        self.assertNotIn("dec-next", content(self.render("report", "frame")))

    def test_runs_lists_the_tasks_runs(self):
        self.assertIn("No Runs yet.", content(self.render("work", "runs")))
        run = self.task / "runs" / "r01_report_01"
        run.mkdir(parents=True)
        (run / "run.yaml").write_text("run: r01_report_01\nkind: hard\ntype: publish-report\nstatus: complete\n")
        body = content(self.render("work", "runs"))
        self.assertIn('<span class="n">r01_report_01</span><span class="d">publish-report</span><span class="w">complete</span>',
                      body)
        self.assertIn('class="dec-btn" data-pop="r01_report_01"', body)
        self.assertEqual(current_view(self.render("runs")), "Runs")      # the older section key still opens it


@unittest.skipUnless((ENGINE / "meaning_store.py").is_file(), "the engine's decision store is not written yet")
class DecideViewTest(Fixture):
    """Decide, read through the real store: what it publishes, what a person drafts and submits."""

    def setUp(self):
        super().setUp()
        self.S = DR.store()
        self.assertIsNotNone(self.S, "meaning_store.py is present but does not load")

    def publish(self, rid, round_id, cards, revision=1):
        return self.S.publish_report(self.lane, report(rid, round_id, cards, revision), "meaning-agent")

    def round_three(self, first=QUESTIONS[0]):
        """report-01, both cards decided; then report-03, submitted in part: practical help still waits, the wrong
        label is deferred, the hard cases are answered (option A)."""
        self.publish("report-01", "round-01", [card("D01", "first card", "A first question?"),
                                               card("D02", "second card", "A second question?")])
        self.S.submit_feedback(self.lane, "report-01", 1, "Reviewer", "req-report-01-a",
                               {"D01": {"kind": "chosen", "option_id": "A"}, "D02": {"kind": "chosen", "option_id": "B"}},
                               True)
        self.publish("report-03", "round-03", [card("D01", "practical help", first),
                                               card("D02", "a wrong label?", QUESTIONS[1]),
                                               card("D03", "hard cases", QUESTIONS[2])])
        self.S.submit_feedback(self.lane, "report-03", 1, "Reviewer", "req-report-03-a",
                               {"D02": {"kind": "defer", "comment": "need more <cases>"},
                                "D03": {"kind": "chosen", "option_id": "A", "comment": "only for adults"}}, True)

    # ── Work › Decide ─────────────────────────────────────────────────────────────────────────────────────────
    def test_work_opens_on_decide_the_inbox_one_row_per_card(self):
        self.round_three()
        page = self.render("work")
        self.assertEqual(current_view(page), "Decide")          # a card still waits for the person
        body = content(page)
        self.assertIn("This round&#x27;s decision report, card by card.", body)
        # the version strip over the Process group, then section 1 with the report's main point
        self.assertIn('<p class="dec-strip">🔒 rules m02 · reference labels l02</p><h3 class="dec-group">⚙️ Process</h3>', body)
        self.assertIn("1 · 🙋 Decisions waiting for you", body)
        self.assertIn('<p class="dec-big">report-03: 1 card waits for you, 1 deferred</p>', body)
        self.assertIn('<p class="dec-state ok">submitted</p>', body)
        # the inbox: one full-width row per card, its full question, its state in a pill, Open; the first waiting opens
        self.assertEqual(body.count('class="dec-row'), 3)
        self.assertEqual(rows(body), [(QUESTIONS[0], "wait", "Needs your judgment", "true"),
                                      (QUESTIONS[1], "more", "More evidence requested", "false"),
                                      (QUESTIONS[2], "ok", "Answered", "false")])
        self.assertIn('<p class="dec-quiet">Continue later. Your draft stays saved.</p>', body)
        self.assertLess(body.index('class="dec-quiet"'), body.index('class="dec-cardbox"'))
        # the open card (slide 16), the others hidden until their Open
        self.assertIn('<section class="dec-card" id="dec-card-0" aria-labelledby="dec-q-0" data-decision="D01">', body)
        self.assertIn('id="dec-card-1" aria-labelledby="dec-q-1" data-decision="D02" hidden>', body)
        self.assertIn("Decision 01 · boundary", body)
        self.assertIn(f'<h4 class="dec-cq" id="dec-q-0">{QUESTIONS[0]}</h4>', body)
        self.assertIn('<figcaption>Case A<small>Train</small></figcaption>', body)
        self.assertIn('<figcaption>Case B<small>Train</small></figcaption>', body)
        self.assertIn('<span class="dec-letter">A</span><span><b>Count it</b><small class="dec-effect" data-effect hidden>'
                      'a placeholder effect · a rule</small>', body)
        self.assertIn("None of these: write my own rule", body)
        self.assertIn("Defer: show more evidence", body)
        self.assertIn("<b>Current rule</b> a placeholder rule", body)
        self.assertIn("<b>Applies to</b> preference only", body)
        # Save draft and Submit feedback, which waits for a visible confirmation; the Task's own path to post with
        self.assertIn(">Save draft</button>", body)
        self.assertIn('data-submit disabled>Submit feedback</button>', body)
        self.assertIn("I confirm these are my answers", body)
        self.assertIn(f'data-path="{frame.rel(self.task, self.root)}"', body)
        self.assertIn('data-act="/_board/labeling/act"', body)
        self.assertIn('data-report="report-03" data-revision="1" data-submitted="1"', body)
        # the earlier reports as a chain, then the step after this one
        self.assertIn('<h3 class="dec-group">📊 Results</h3>', body)
        self.assertIn("2 · 🪜 Earlier reports", body)
        self.assertIn('<span class="dec-role">done</span><div class="dec-box">report-01 · 2 decided</div>', body)
        self.assertIn("next: 🔁 Changes →", body)
        self.assertIn("section=work&amp;group=changes", body.split('class="dec-next"', 1)[1])
        # the scoped assets ride with the page, after the workbench's own
        self.assertLess(page.index("focus-rail{"), page.index(".dec-view .dec-row{"))
        self.assertIn("window.decisionReportView", page)

    def test_an_open_report_waits_for_you(self):
        self.publish("report-01", "round-01", [card("D01", "practical help", QUESTIONS[0]),
                                               card("D02", "a wrong label?", QUESTIONS[1])])
        page = self.render()
        self.assertEqual(current_view(page), "Decide")
        body = content(page)
        self.assertIn('<p class="dec-big">report-01: 2 cards wait for you</p><p class="dec-state wait">waiting for you</p>', body)
        self.assertEqual([(r[2], r[3]) for r in rows(body)], [("Needs your judgment", "true"), ("Needs your judgment", "false")])
        self.assertIn('data-submitted="0"', body)
        self.assertIn("None: this is the first report.", body)

    def test_a_saved_draft_says_draft_saved_and_rides_in_the_form(self):
        self.publish("report-03", "round-03", [card("D01", "practical help", QUESTIONS[0]),
                                               card("D02", "a wrong label?", QUESTIONS[1])])
        self.S.save_draft(self.lane, "report-03", 1, "Reviewer", {"D01": {"kind": "chosen", "option_id": "B",
                                                                          "comment": "a note"}}, 0)
        body = content(self.render("work", "decide"))
        self.assertIn('<p class="dec-big">report-03: 1 card waits for you</p><p class="dec-state wait">waiting for you</p>',
                      body)
        self.assertEqual([(r[1], r[2], r[3]) for r in rows(body)], [("draft", "Draft saved", "false"),
                                                                    ("wait", "Needs your judgment", "true")])
        got = json.loads(html.unescape(re.search(r'data-drafts="([^"]*)"', body).group(1)))
        self.assertEqual(got["Reviewer"]["draft_revision"], 1)
        self.assertEqual(got["Reviewer"]["report_revision"], 1)
        self.assertEqual(got["Reviewer"]["answers"]["D01"], {"kind": "chosen", "option_id": "B", "comment": "a note"})
        self.assertEqual(got["Reviewer"]["answers"]["D02"], {"kind": "unanswered"})
        self.assertNotIn(" checked", body)                          # the browser fills it in, for that person only

    def test_a_draft_of_an_older_revision_is_not_mapped_onto_the_new_one(self):
        cards = [card("D01", "practical help", QUESTIONS[0])]
        self.publish("report-03", "round-03", cards)
        self.S.save_draft(self.lane, "report-03", 1, "Reviewer", {"D01": {"kind": "chosen", "option_id": "A"}}, 0)
        self.publish("report-03", "round-03", cards, revision=2)
        body = content(self.render("work", "decide"))
        self.assertEqual([r[2] for r in rows(body)], ["Needs your judgment"])
        self.assertIn('data-revision="2"', body)
        got = json.loads(html.unescape(re.search(r'data-drafts="([^"]*)"', body).group(1)))
        self.assertEqual(got["Reviewer"]["report_revision"], 1)        # the browser leaves it unfilled, and says so

    def test_no_option_is_chosen_for_the_person(self):
        self.round_three()
        body = content(self.render("work", "decide"))
        inputs = re.findall(r"<input[^>]*>", body)
        self.assertEqual(sum('type="radio"' in i for i in inputs), 3 * 4)    # two options, None, Defer per card
        self.assertFalse([i for i in inputs if re.search(r"\bchecked\b", i)])
        self.assertNotIn(" checked", body)
        self.assertNotIn(" selected", body)

    def test_report_text_is_escaped(self):
        self.round_three(first='<script>alert("x")</script> & <b>bold</b>?')
        self.S.save_draft(self.lane, "report-03", 1, "Reviewer",
                          {"D01": {"kind": "custom", "text": "</script><script>alert(2)</script>"}}, 0)
        escaped = "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt; &amp; &lt;b&gt;bold&lt;/b&gt;?"
        for section in ("work", "report"):
            with self.subTest(section=section):
                page = self.render(section, "decide")
                body = content(page)
                self.assertEqual(rows(body)[0][0], escaped)                    # the row's full question
                self.assertIn(f'<h4 class="dec-cq" id="dec-q-0">{escaped}</h4>', body)
                self.assertNotIn('<script>alert("x")', page)
                self.assertNotIn("<b>bold</b>", page)
                self.assertNotIn("<script>alert(2)", page)
                self.assertIn("&lt;a reply that offers practical help&gt;", body)
                self.assertEqual(page.count("<script>"), 2)          # focus.js and decision_report.js, nothing else

    # ── Report › Decide ───────────────────────────────────────────────────────────────────────────────────────
    def test_report_shows_each_cards_answer_read_only(self):
        self.round_three()
        page = self.render("report", "decide")
        self.assertIn(">Report</span></h1>", page)
        self.assertEqual(current_view(page), "Decide")
        body = content(page)
        self.assertIn('<p class="dec-strip">🔒 rules m02 · reference labels l02</p><h3 class="dec-group">📊 Results</h3>', body)
        self.assertNotIn("⚙️ Process", body)
        self.assertIn('<p class="dec-big">report-03: 1 card waits for you, 1 deferred</p>', body)
        self.assertEqual([r[2] for r in rows(body)], ["Needs your judgment", "More evidence requested", "Answered"])
        for absent in ("<input", "<textarea", "Save draft", "Submit", "data-dec-form", "dec-quiet", "next:"):
            self.assertNotIn(absent, body)
        self.assertIn('<dt>Answer</dt><dd>Needs your judgment</dd>', body)
        self.assertIn('<dt>Answer</dt><dd>Deferred: show more evidence<br><small class="dec-comment">'
                      'Comment: need more &lt;cases&gt;</small></dd>', body)
        self.assertIn('<dt>Answer</dt><dd>Chose: Count it<br><small class="dec-comment">Comment: only for adults</small>',
                      body)
        self.assertIn('<div class="dec-box">report-01 · 2 decided</div>', body)

    # ── which view opens, and the honest empty states ─────────────────────────────────────────────────────────
    def test_it_opens_on_frame_when_no_report_waits(self):
        self.publish("report-01", "round-01", [card("D01", "practical help", QUESTIONS[0])])
        self.S.submit_feedback(self.lane, "report-01", 1, "Reviewer", "req-report-01-a",
                               {"D01": {"kind": "chosen", "option_id": "A"}}, True)
        for section in ("", "work", "report"):
            with self.subTest(section=section):
                page = self.render(section)
                self.assertEqual(current_view(page), "Frame")
                self.assertIn("The task: the label, who decides, its values.", page)
                self.assertIn("1 · 🎯 Frame the task", page)
        body = content(self.render("work", "decide"))
        self.assertIn('<p class="dec-big">report-01: 1 answered</p><p class="dec-state ok">submitted</p>', body)

    def test_honest_empty_state_when_no_report_exists(self):
        self.assertEqual(current_view(self.render("work")), "Frame")
        for section in ("work", "report"):
            body = content(self.render(section, "decide"))
            self.assertIn('<p class="dec-big">No decision report yet</p>', body)
            self.assertIn("nothing waits for you", body)
            for absent in ('class="dec-row', "data-dec-form", "dec-strip"):
                self.assertNotIn(absent, body)
        self.lane.joinpath("meaning").mkdir(parents=True)                # a lane with nothing published yet
        self.assertIn("No decision report yet", content(self.render("work", "decide")))

    def test_rendering_writes_nothing(self):
        self.round_three()
        before = {p: p.stat().st_mtime_ns for p in self.root.rglob("*")}
        for section in ("work", "report"):
            for key, *_ in L.BUILD_VIEWS:
                self.render(section, key)
        self.assertEqual(before, {p: p.stat().st_mtime_ns for p in self.root.rglob("*")})

    def test_the_engine_demo_report_end_to_end(self):
        """The engine's own demo report (fixtures/decision_report_demo.json): published, drafted, then submitted."""
        demo = json.loads((ENGINE / "fixtures" / "decision_report_demo.json").read_text(encoding="utf-8"))
        self.S.publish_report(self.lane, demo, "meaning-agent-demo")
        rid, cards = demo["report_id"], demo["cards"]
        body = content(self.render("work"))
        self.assertEqual(len(rows(body)), len(cards))
        self.assertEqual([html.unescape(r[0]) for r in rows(body)], [c["question"] for c in cards])
        self.assertEqual({r[2] for r in rows(body)}, {"Needs your judgment"})
        self.assertIn(f'<p class="dec-strip">🔒 rules {demo["base"]["meaning_version"]} · reference labels '
                      f'{demo["base"]["reference_version"]}</p>', body)
        self.assertNotIn(" checked", body)
        first = cards[0]
        self.S.save_draft(self.lane, rid, 1, "Reviewer", {first["decision_id"]: {"kind": "defer"}}, 0)
        self.assertEqual(rows(content(self.render("work")))[0][2], "Draft saved")
        option = first["options"][1]
        self.S.submit_feedback(self.lane, rid, 1, "Reviewer", "req-demo-0001",
                               {first["decision_id"]: {"kind": "chosen", "option_id": option["option_id"]}}, True)
        body = content(self.render("report", "decide"))
        self.assertEqual(rows(body)[0][2], "Answered")
        self.assertIn(f"<dt>Answer</dt><dd>Chose: {html.escape(option['label'])}</dd>", body)
        self.assertIn(f'<p class="dec-big">{rid}: {len(cards) - 1} cards wait for you</p>', body)


if __name__ == "__main__":
    unittest.main()
