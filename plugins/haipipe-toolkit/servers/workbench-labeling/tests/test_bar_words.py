"""Every closed bar of a labeling page shows a state word on its right, and a bar whose state waits on the person shows
that one thing under it (JL 261106, built for the other themes in servers/workbench/ui_parts.py). Checked on the
placeholder Job that runs both loops with the real tools (labeling_example.py), on an items Task whose recipe waits for
a Sign behind a waiting form, and on a building Task's bars."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import decision_report_view as DR, frame, interaction_section as IX, labeling_focus as L  # noqa: E402
from live import labeling_steps as S  # noqa: E402
from live import task_labeling as TL  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labeling_example  # noqa: E402

BAR = re.compile(r"<h3 class=fd-h>(\d+ · [^<]*)(.*?)</h3>(<p class=fd-wait>([^<]*)</p>)?", re.S)


def bars(html: str) -> list:
    """[(title, word, waiting line)] of every numbered bar on a page."""
    out = []
    for m in BAR.finditer(html):
        word = re.search(r'<span class="?word(?: you)?"?>([^<]*)</span>', m.group(2))
        out.append((m.group(1), word.group(1) if word else "", m.group(4) or ""))
    return out


class StepBarsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name).resolve()
        block = labeling_example.build(cls.root / "Project-X" / "labeling" / "b01_labeling_example")
        cls.job = block / "j01_example_response_safety"
        cls.meaning, cls.expression = cls.job / "t03_example_meaning", cls.job / "t04_example_expression"
        cls.theme = frame.themes()["labeling"]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def page(self, task, section, view):
        return L.render(self.theme, self.root, task, section, view)

    def test_every_numbered_bar_of_every_step_carries_a_word(self):
        for task in (self.meaning, self.expression):
            for key, *_ in S.STEPS[S.kind(task)]:
                for section in ("report", "work"):
                    with self.subTest(task=task.name, view=key, section=section):
                        html = self.page(task, section, key)
                        found = bars(html)
                        self.assertTrue(found)
                        self.assertEqual(len(found), len(re.findall(r"<h3 class=fd-h>\d+ · ", html)))
                        self.assertEqual([t for t, w, _ in found if not w.strip()], [])

    def test_the_bar_keeps_its_numbered_start_and_the_word_sits_after_the_title(self):
        html = self.page(self.meaning, "work", "frame")
        self.assertIn("<h3 class=fd-h>1 · 🎯 Frame the labeling task<span class=word>agreed</span></h3>", html)
        self.assertNotIn("fd-verb", html.split("📊 Results")[0].split("⚙️ Process")[-1])   # no pill in the bar any more

    def test_a_step_that_waits_on_you_says_so_and_shows_what_waits_under_its_bar(self):
        html = self.page(self.meaning, "work", "preferences")                   # Loop 2's form waits for the person
        first = IX.state_word(S.view_forms(self.meaning, self.root, "preferences"))[1]   # the waiting item itself, its
        self.assertTrue(first.startswith("🙋 ") and " · " in first)                     # first open question (round 4)
        self.assertIn('1 · 🙋 Collect preferences<span class="word you">waiting for you</span></h3>'
                      f"<p class=fd-wait>{frame.esc(first)}</p>", html)
        self.assertNotIn("then press Copy prompt</p>", html)
        self.assertIn("fd-wait", S.view_html(self.meaning, self.root, "work", "preferences"))
        done = self.page(self.meaning, "work", "frame")                         # an agreed step waits on no one
        self.assertNotIn("<p class=fd-wait>", done)

    def test_a_made_guideline_waits_for_your_sign_until_you_sign_it(self):
        self.assertEqual(S.bar_word(("sign m02", "you")), "waits for your sign")
        self.assertEqual(S.bar_word(("draw planned", "you")), "draw planned, waits for you")
        self.assertEqual(S.bar_word(("", "")), "not started yet")
        self.assertEqual(S.bar_word(("waiting for you", "you")), "waiting for you")
        update = self.page(self.meaning, "work", "update")                      # m01 is signed in the fixture
        self.assertIn("1 · 🔁 Integrate feedback and check alignment<span class=word>m01 approved</span>", update)

    def test_results_words_come_from_the_files(self):
        found = dict((t, w) for t, w, _ in bars(self.page(self.expression, "report", "evaluate")))
        self.assertIn("models", found["3 · 📈 Labeling performance"])
        self.assertRegex(found["2 · 🔍 Errors, by kind"], r"^\d+ errors? in \d+ kinds?$")
        release = dict((t.split(" · ", 1)[1], w) for t, w, _ in bars(self.page(self.expression, "report", "release")))
        self.assertRegex(release["✅ Release criteria"], r"^(all met|\d+ of \d+ met)$")
        self.assertTrue(all("not signed yet" not in t for t in release))      # the state is the word, not the title
        prepare = dict((t.split(" · ", 1)[1], w) for t, w, _ in bars(self.page(self.meaning, "report", "prepare")))
        self.assertRegex(prepare["📌 Typical cases"], r"^(\d+ cases?|nothing yet)$")
        self.assertRegex(prepare["🧠 Guideline rules, as a mind map"], r"^m\d\d (approved|not approved yet)$")


class ItemsBarTest(unittest.TestCase):
    """An items Task whose recipe (r03_items) waits for a Sign, and a form (r02) whose choices that Sign rests on."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        job = self.root / "Project-X" / "labeling" / "b01_demo" / "j01_demo_safety"
        self.items = job / "t01_demo_items"
        (self.items / "scripts" / "config").mkdir(parents=True)
        (self.items / "t01_demo_items.md").write_text("# t01 · Demo items\ntask-type: items\n\n## Opening\n\nA placeholder.\n")
        form = self.items / "runs" / "r02_collect_items_recipe"
        form.mkdir(parents=True)
        (form / "run.yaml").write_text("run: r02_collect_items_recipe\nkind: hard\ntype: collect\nstatus: waiting\n"
                                       "writes:\n- result/answer_collection.md\nfeeds:\n- r03_items\n")
        (form / "question_collection.md").write_text("# Items recipe choices\n\nfor: placeholder\n\n## Q1 · The text judged\n"
                                                     "Why.\n**Which text is judged?**\n- [x] A · one\n- [ ] B · two\n")
        (form / "r02_collect_items_recipe.html").write_text("<p>placeholder form</p>\n")
        run = self.items / "runs" / "r03_items"
        run.mkdir(parents=True)
        (run / "run.yaml").write_text("run: r03_items\nkind: hard\ntype:\n- items-items\nstatus: planned\nneeds: signed\n")
        (self.items / "scripts" / "config" / "r03_items.yaml").write_text(
            "operation: items\nrecipe:\n  unit: chat\n  item_id: chat_id\n  main: reply\nout: placeholder/items-v1\n")
        meaning = job / "t03_demo_meaning"
        meaning.mkdir()
        (meaning / "t03_demo_meaning.md").write_text("# t03 · Demo meaning\ntask-type: labeling-meaning\n")
        self.job = job

    def tearDown(self):
        self.temp.cleanup()

    def test_the_recipe_step_waits_for_your_sign_with_its_line_and_its_form(self):
        box = TL._step_box(1, self.items, self.root, None, "sign")
        self.assertIn("✍ waits for your sign", box)
        self.assertIn("<p class=items-wait", box)
        self.assertIn("🙋 Answer Items recipe choices first, then read the recipe below and press Sign", box)
        self.assertIn('href="/_board/labeling/form/', box)                    # the form opens through its route
        self.assertLess(box.index("items-wait"), box.index("work-body"))     # under the bar, before the step's body
        done = TL._step_box(1, self.items, self.root, None, "done")
        self.assertNotIn("items-wait", done)
        self.assertIn("· later", TL.CHIPS["todo"])

    def test_the_items_page_puts_the_form_in_the_items_views_interaction_and_serves_it(self):
        """Round 2: the form the recipe's Sign rests on is the Items view's 🙋 Interaction (never in Process), named in
        the step's waiting line, and it opens through the form route (it gave a 404 for any Task but meaning)."""
        from unittest.mock import patch
        with patch.object(TL, "_step_states", return_value={"raw": "done", "make": "sign", "embed": "todo"}):
            html = L.render(frame.themes()["labeling"], self.root, self.items, "work", "items")
        process = html.split("⚙️ Process", 1)[1].split("📊 Results", 1)[0]
        self.assertNotIn("r02_collect_items_recipe.html", process)
        self.assertIn("<p class=fd-wait>🙋 Items recipe choices: Q1 · ", process)   # the waiting item (round 4)
        self.assertNotIn("then read the recipe and press Sign", process)
        self.assertIn("r02_collect_items_recipe", html.split("📊 Results", 1)[1])
        self.assertNotIn("r02_collect_items_recipe.html", L.render(frame.themes()["labeling"], self.root, self.items,
                                                                    "work", "data"))
        from live.labeling import LabelingMixin
        import io

        class Handler(LabelingMixin):
            def send_response(self, status): self.status = status
            def send_error(self, status, *_): self.status = status
            def send_header(self, *args): pass
            def end_headers(self): pass
        h = Handler()
        h.root, h.headers, h.wfile = self.root, {"Host": "example.test"}, io.BytesIO()
        h.path = frame._file_url(self.items / "runs" / "r02_collect_items_recipe" / "r02_collect_items_recipe.html", self.root)
        h.labeling_form_view()
        self.assertEqual(h.status, 200)
        self.assertIn(b"placeholder form", h.wfile.getvalue())

    def test_the_items_step_holds_its_prompt_its_runs_and_a_sign_with_no_name(self):
        """Round 4: the prompt card sits inside the step's closed bar, the step links its own Runs (r03_items opens its
        card), and Sign asks for no name."""
        from unittest.mock import patch
        with patch.object(TL, "_step_states", return_value={"raw": "done", "make": "sign", "embed": "todo"}):
            html = L.render(frame.themes()["labeling"], self.root, self.items, "work", "items")
            words = TL.items_words(self.items, self.root)
        process = html.split("⚙️ Process", 1)[1].split("📊 Results", 1)[0]
        self.assertIn("pb-prompt", process)
        self.assertNotIn("pb-prompt", re.sub(r"<section class=fd-sec>.*?</section>", "", process, flags=re.S))
        self.assertIn("part=run", process)                                      # r03_items opens its Run card
        self.assertIn("<code>r03_items</code>", process)
        self.assertNotIn("name (optional)", html)
        self.assertNotIn("class=sign-by", html)
        self.assertEqual(words["embedding"], ("later", ""))                       # every button has its word

    def test_without_a_form_the_line_is_the_sign_alone(self):
        (self.items / "runs" / "r02_collect_items_recipe" / "run.yaml").write_text(
            "run: r02_collect_items_recipe\nkind: hard\ntype: collect\nstatus: done\nfeeds:\n- r03_items\n")
        self.assertEqual(TL._wait_line(self.items, "items", "sign"), ("✍️ Read the recipe below and press Sign", None))

    def test_the_next_action_names_the_items_step_never_preferences(self):
        dest, key, words, _ = L.next_action(self.job, self.root)
        self.assertEqual((dest, key), (self.items, "items"))
        self.assertIn("read the recipe in 2 · Items and press Sign", words)
        self.assertIn("Items recipe choices", words)
        self.assertNotIn("Preferences", words)


class BuildingBarTest(unittest.TestCase):
    def test_a_building_bar_carries_its_word_and_what_waits_only_while_closed(self):
        html = DR.section(1, "🙋 Decisions waiting for you", "<p>b</p>", word="waiting for you", waits="🙋 Which?")
        self.assertIn('data-fold="1 · 🙋 Decisions waiting for you"', html)  # the fold keys on the title alone
        self.assertIn('<span class="word you">waiting for you</span></summary>', html)
        self.assertTrue(html.endswith('</details><p class="dec-wait">🙋 Which?</p>'))
        css = (Path(DR.__file__).parent / "focus-assets" / "decision_report.css").read_text(encoding="utf-8")
        self.assertIn(".dec-sec[open]+.dec-wait{display:none}", css)
        self.assertNotIn("dec-wait", DR.section(2, "🪜 Earlier reports", "x", word="none yet"))


if __name__ == "__main__":
    unittest.main()
