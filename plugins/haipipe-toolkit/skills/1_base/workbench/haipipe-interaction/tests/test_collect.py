"""haipipe-interaction: a collection Run under a page; its questions in Markdown, rendered into a compact form; the
answers back as the same Markdown with the person's picks ticked."""
import contextlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import yaml

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import collect  # noqa: E402

QUESTIONS = """# Report and Delivery

for: b01-s01:x @ y

You said the Report should show the paper.

<!-- a note to the writer, never content -->

## Q1 · Report or Delivery

The Report shows what the paper looks like: the delivery.

```text
today ─▶ A
```

**Where does a delivery show?**

- [x] A · In the Report.
- [ ] B · In both.

Why A: One thing in one place.

## Q2 · View buttons

Its buttons name what the page hands over.

**Which buttons?**

- [ ] A · All first.
- [ ] B · No All.
"""


class CollectTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.task = Path(self.tmp.name) / "b01_x" / "j01_y" / "t01_z"
        self.task.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def run_with(self, text=QUESTIONS) -> Path:
        run = collect.new(self.task, "report_and_delivery", "Report and Delivery", "b01-s01:x @ y", "JL")
        (run / collect.QUESTIONS).write_text(text, encoding="utf-8")
        return run

    def run_with_slug(self, slug):
        page = self.task.parent / f"t09_{slug}"
        page.mkdir()
        run = collect.new(page, slug, "Report and Delivery", "b01-s01:x @ y", "JL")
        (run / collect.QUESTIONS).write_text(QUESTIONS, encoding="utf-8")
        return run

    def test_new_allocates_the_next_rnn_with_a_hard_collect_card(self):
        (self.task / "runs" / "r03_fit_model").mkdir(parents=True)
        run = collect.new(self.task, "report_and_delivery", "Report and Delivery", "b01-s01:x @ y", "JL")
        self.assertEqual(run.name, "r04_collect_report_and_delivery")
        card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))
        self.assertEqual((card["kind"], card["type"], card["agent"], card["status"]), ("hard", "collect", "JL", "planned"))
        self.assertEqual(card["skill"], "haipipe-interaction")
        self.assertTrue((run / collect.QUESTIONS).read_text(encoding="utf-8").startswith("# Report and Delivery"))
        with self.assertRaises(SystemExit):
            collect.new(self.task, "report_and_delivery", "Again here", "b01-s02:x @ z", "JL")

    def test_the_markdown_reads_into_cards(self):
        spec = collect.parse(QUESTIONS)
        self.assertEqual((spec["title"], spec["for"], spec["intro"]),
                         ("Report and Delivery", "b01-s01:x @ y", "You said the Report should show the paper."))
        q1, q2 = spec["questions"]
        self.assertEqual((q1["ask"], q1["because"], q1["show"]), ("Where does a delivery show?",
                                                                  "One thing in one place.", [{"sketch": "today ─▶ A"}]))
        self.assertEqual([(o["key"], bool(o.get("pick"))) for o in q1["options"]], [("A", True), ("B", False)])
        self.assertEqual(collect.markdown(spec).strip(), collect.markdown(collect.parse(collect.markdown(spec))).strip())
        self.assertEqual(q2["options"][1]["text"], "No All.")

    def test_build_renders_the_markdown_into_a_compact_form_and_the_card_waits(self):
        run = self.run_with()
        page = collect.build(run).read_text(encoding="utf-8")
        self.assertEqual(page.count('<section class="card" id="Q'), 2)
        self.assertIn('name="Q1" value="A" checked', page)
        self.assertNotIn('name="Q2" value="A" checked', page)
        self.assertIn('<p class="because">Why A: One thing in one place.</p>', page)
        self.assertIn('<pre class="sketch">today ─▶ A</pre>', page)
        self.assertIn(f'href="{collect.QUESTIONS}"', page)
        self.assertIn('<p class="label">Questions for you · ', page)                # concrete words for the reader
        self.assertIn("GENERATED FILE by haipipe-interaction", page)
        self.assertIn("'haipipe-interaction answers · '", page)
        self.assertIn("localStorage.getItem(OLD)", page)                          # answers kept before the rename
        self.assertIn("GENERATED FILE", page)
        self.assertNotIn("a note to the writer", page)
        self.assertNotRegex(page, r"<script[^>]+src=|<link[^>]+stylesheet")      # self-contained
        data = json.loads(re.search(r'id="form-data">(.*?)</script>', page, re.S).group(1))
        self.assertEqual((data["run"], [q["pick"] for q in data["questions"]]), (run.name, ["A", ""]))
        self.assertEqual(yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))["status"], "waiting")

    def test_check_holds_the_compact_limits(self):
        long = QUESTIONS.replace("Report or Delivery", "A title of five words").replace(
            "Where does a delivery show?", "Where it shows").replace("Why A: One thing in one place.\n", "").replace(
            "- [ ] B · In both.", "- [x] B · " + "word " * 15).replace("today ─▶ A", "\n".join("abcdefg"))
        found = collect.problems(collect.parse(long), self.task / "runs" / "r01_collect_x")
        for text in ("one to three words", "ends with ?", "tick at most one", "Why A: missing", "at most 14",
                     "sketch, at most 6"):
            self.assertTrue(any(text in p for p in found), text)
        stray = QUESTIONS.replace("Why A: One thing in one place.", "Why A: One thing.\n\nA stray line here.")
        self.assertTrue(any("is not part of its card" in p for p in collect.problems(collect.parse(stray), self.task)))
        many = QUESTIONS + "".join(f"\n## Q{n} · More\n\nWhy.\n\n**Ask?**\n\n- [ ] A · a\n- [ ] B · b\n" for n in range(3, 23))
        self.assertTrue(any("at most 20 per Run" in p for p in collect.problems(collect.parse(many), self.task)))

    def test_one_page_answers_every_waiting_form_and_one_paste_saves_each(self):
        """JL 261031: "should actively think about combine the different interactions in to one page"."""
        runs = [self.run_with(), self.run_with_slug("second")]
        for run in runs:
            collect.build(run)
        page = collect.bundle(self.task.parent)
        html_ = page.read_text(encoding="utf-8")
        self.assertEqual(html_.count('class="b-form"'), 2)
        self.assertIn("Copy all answers", html_)
        root = Path(self.tmp.name)
        lines = ("Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: A · All first.")
        pasted = "\n".join(self.paste(r, *lines, form="/" + str((r / f"{r.name}.html").relative_to(root))) for r in runs)
        saved = collect.save_all(pasted, root, datetime(2026, 10, 31, 18, 0))
        self.assertEqual(len(saved), 2)
        for run in runs:
            self.assertEqual(yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))["status"], "done")

    def test_save_ticks_the_persons_picks_and_closes_the_run(self):
        run = self.run_with()
        collect.build(run)
        pasted = (f"haipipe-interaction answers · {run.name} · Report and Delivery · 2026-10-31 12:00\n"
                  f"form: {run / (run.name + '.html')}\nbuilt: {collect.form_built((run / (run.name + '.html')).read_text(encoding='utf-8'))}\n"
                  "Q1 · Report or Delivery: B · In both. (changed from A)\n"
                  "   note: keep it short\n         second line\nQ2 · View buttons: A · All first.\n")
        out = collect.save(run, pasted, datetime(2026, 10, 31, 12, 5))
        text = out.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# Report and Delivery · answers\n\nreceived: 2026-10-31 12:05"))
        self.assertIn("- [ ] A · In the Report.\n- [x] B · In both.", text)
        self.assertIn("Answer: B, changed from my pick A.", text)
        self.assertIn("> note: keep it short\n> second line", text)
        self.assertIn(pasted.strip(), text)                                     # word for word below
        card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))
        self.assertEqual((card["status"], card["passes"], card["writes"]), ("done", ["p01-1031"], [collect.ANSWERS]))
        with self.assertRaises(SystemExit):                                     # another Run's paste is refused
            collect.save(run, "haipipe-collect feedback · r09_collect_other · x\n")

    def test_the_old_first_line_still_saves_and_an_unstamped_paste_asks_for_a_reload(self):
        run = self.run_with()
        collect.build(run)
        lines = ("Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All.")
        with self.assertRaises(SystemExit) as no:                              # a tab left open on an older build
            collect.save(run, self.paste(run, *lines, built=False))
        self.assertIn("reload this Run's form and copy again", str(no.exception))
        self.assert_nothing_saved(run)
        old = self.paste(run, *lines, head="haipipe-collect feedback")         # the old words, on the current build
        text = collect.save(run, old, datetime(2026, 10, 31, 12, 30)).read_text(encoding="utf-8")
        self.assertIn("- [x] B · No All.", text)
        self.assertIn(old.strip(), text)

    def test_a_closed_result_is_never_rewritten_and_a_loose_note_still_counts(self):
        run = self.run_with()
        collect.build(run)
        stamp = collect.form_built((run / f"{run.name}.html").read_text(encoding="utf-8"))
        head = f"haipipe-interaction answers · {run.name} · Report and Delivery · 2026-10-31 12:00\nbuilt: {stamp}\n"
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            out = collect.save(run, head + "Q1 · Report or Delivery: A · In the Report.\nnote: a note that lost its indent\n"
                                            "  and a second line\nQ2 · View buttons: B · No All.\nsomething else\n")
        text = out.read_text(encoding="utf-8")
        self.assertIn("> note: a note that lost its indent\n> and a second line", text)
        self.assertIn("Answer: A, my pick. Where the note below says otherwise, the note wins.", text)
        self.assertIn("something else", err.getvalue())                         # named, and kept word for word
        with self.assertRaises(SystemExit):                                     # a changed mind is a new Run
            collect.save(run, head + "Q1 · Report or Delivery: B · In both.\nQ2 · View buttons: A · All first.\n")
        self.assertIn("- [x] A · In the Report.", out.read_text(encoding="utf-8"))

    def test_one_waiting_run_per_page_and_plain_separators(self):
        run = self.run_with(QUESTIONS.replace("## Q2 · View buttons", "## Q2 - View buttons").replace("- [ ] B · No All.", "- [ ] B: No All."))
        self.assertEqual([o["text"] for o in collect.load(run)["questions"][1]["options"]], ["All first.", "No All."])
        collect.build(run)                                                     # the card now says waiting
        with self.assertRaises(SystemExit):
            collect.new(self.task, "another_choice", "Another choice", "b01-s01:x @ other", "JL")
        with self.assertRaises(SystemExit):                                    # the same sNN: refused
            collect.new(self.task, "same_topic", "Same topic", "b01-s01:x @ y", "JL")
        other = collect.new(self.task, "other_topic", "Another topic", "b01.j01.t01-s05:x @ other", "JL")
        self.assertTrue(other.is_dir())                                        # another sNN: its own waiting Run

    def test_an_interaction_is_attached_to_one_studio_topic(self):
        """JL 261031: "the interaction page should be attached to one studio as well"."""
        for about in ("", "j01 · j01_v1130_lanpub", "b01 · the page itself"):
            with self.assertRaises(SystemExit):
                collect.new(self.task, "no_topic", "No topic here", about, "JL")
        self.assertFalse((self.task / "runs").exists() and any((self.task / "runs").iterdir()))
        run = self.run_with(QUESTIONS.replace("for: b01-s01:x @ y\n\n", ""))
        self.assertTrue(any("names no Studio topic" in p for p in collect.problems(collect.load(run), run)))
        with self.assertRaises(SystemExit):
            collect.build(run)

    def test_applied_answers_get_their_flags(self):
        """JL 261031: "if we already fix them, then give them the flags": collect.py applied writes applied.md beside
        run.yaml (never in result/), one line per question; the form reads it; a template change keeps the stamp."""
        run = self.run_with()
        form = collect.build(run)
        with self.assertRaises(SystemExit):                                       # not answered: nothing to apply
            collect.applied(run, ["Q1"], "x")
        stamp = collect.form_built(form.read_text(encoding="utf-8"))
        collect.save(run, self.paste(run, "Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All."))
        with self.assertRaises(SystemExit):                                       # not one of its questions
            collect.applied(run, ["Q9"], "x")
        with self.assertRaises(SystemExit):                                       # says what changed
            collect.applied(run, ["Q1"], "  ")
        now = datetime(2026, 10, 31, 16, 40)
        path = collect.applied(run, ["Q2", "Q1"], "focus_page.py: one bar (b10-s33-D04)", now=now)
        collect.applied(run, ["Q2"], "labeling session builds it", "in progress", now=now)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(path, run / "applied.md")
        self.assertIn("Q1 · applied · 2026-10-31 16:40 · focus_page.py: one bar (b10-s33-D04)\nQ2 · in progress · ", text)
        self.assertEqual(text.count("Q2 ·"), 1)                                  # a later line replaces the earlier
        self.assertFalse((run / "result" / "applied.md").exists())
        self.assertTrue(all(collect.APPLIED_LINE.match(ln) for ln in text.splitlines() if ln.startswith("Q")))
        collect.build(run)                                                        # the flags' template, the same stamp
        page = form.read_text(encoding="utf-8")
        self.assertIn('id="applied-Q1"', page)
        self.assertIn("fetch('applied.md'", page)
        self.assertEqual(collect.form_built(page), stamp)
        data = json.loads(re.search(r'<script type="application/json" id="form-data">(.*?)</script>', page, re.S).group(1))
        self.assertEqual(data["answered"]["picks"]["Q2"]["pick"], "B")             # the person's picks, read only
        self.assertIn("your picks and notes are shown, read only", page)

    def test_an_option_shows_its_own_live_preview(self):
        run = self.run_with(QUESTIONS.replace("- [x] A · ", "- [x] A · ", 1))
        text = (run / collect.QUESTIONS).read_text(encoding="utf-8")
        lines = text.splitlines()
        at = next(i for i, ln in enumerate(lines) if ln.startswith("- [x] A"))
        lines.insert(at + 1, "  [preview](option-a.html)")
        (run / collect.QUESTIONS).write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertTrue(any("preview not found" in p for p in collect.problems(collect.load(run), run)))   # refused until it exists
        (run / "option-a.html").write_text("<p>A</p>", encoding="utf-8")
        q = collect.load(run)["questions"][0]
        self.assertEqual(q["options"][0]["preview"], "option-a.html")
        collect.build(run)
        form = (run / f"{run.name}.html").read_text(encoding="utf-8")
        self.assertIn('<iframe src="option-a.html"', form)                     # side by side, live
        self.assertIn("  [preview](option-a.html)", collect.markdown(collect.load(run)))   # kept in the Markdown

    def paste(self, run, *lines, title="Report and Delivery", form=None, built=True, head="haipipe-interaction answers"):
        stamp = collect.form_built((run / f"{run.name}.html").read_text(encoding="utf-8")) if built else ""
        top = [f"{head} · {run.name} · {title} · 2026-10-31 13:00"]
        return "\n".join(top + ([f"form: {form}"] if form else []) + ([f"built: {stamp}"] if stamp else [])
                         + list(lines)) + "\n"

    def assert_nothing_saved(self, run):
        self.assertFalse((run / collect.ANSWERS).exists())
        self.assertFalse((run / "passes").exists())
        self.assertEqual(yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))["status"], "waiting")

    def test_a_same_named_run_on_another_page_is_refused(self):
        """Codex review 261031: one Run name under two pages; the paste's form: names one page, save targets the other."""
        runs = {}
        for page in ("t01_alpha", "t02_beta"):
            folder = self.task.parent / page
            folder.mkdir()
            run = collect.new(folder, "same_choice", "Report and Delivery", "b01-s01:x @ y", "JL")
            (run / collect.QUESTIONS).write_text(QUESTIONS, encoding="utf-8")
            collect.build(run)
            runs[page] = run
        self.assertEqual(runs["t01_alpha"].name, runs["t02_beta"].name)
        alpha_form = "/" + (runs["t01_alpha"] / (runs["t01_alpha"].name + ".html")).relative_to(Path(self.tmp.name)).as_posix()
        pasted = self.paste(runs["t01_alpha"], "Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All.",
                            form=alpha_form)
        with self.assertRaises(SystemExit) as no:
            collect.save(runs["t02_beta"], pasted)
        self.assertIn("this Run's own form ends with b01_x/j01_y/t02_beta/runs/", str(no.exception))
        self.assert_nothing_saved(runs["t02_beta"])
        bare = f"/runs/{runs['t01_alpha'].name}/{runs['t01_alpha'].name}.html"        # names no page (tester case c1f)
        with self.assertRaises(SystemExit):
            collect.save(runs["t02_beta"], self.paste(runs["t02_beta"], "Q1 · Report or Delivery: A · In the Report.",
                                                     "Q2 · View buttons: B · No All.", form=bare))
        self.assert_nothing_saved(runs["t02_beta"])
        self.assertTrue(collect.save(runs["t01_alpha"], pasted).is_file())           # the page it names takes it

    def test_an_answered_run_is_never_rebuilt_and_close_checks_the_body(self):
        """The tester's k6d, k6b and b2: an answered Run's form is not rebuilt (no Run left stuck); close refuses an
        answer file whose body is not what save writes from its kept paste; a rebuild that changes nothing keeps the
        stamp, so a paste copied before it still saves."""
        run = self.run_with()
        form = collect.build(run)
        early = self.paste(run, "Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All.")
        stamp = collect.form_built(form.read_text(encoding="utf-8"))
        collect.build(run)                                                        # b2: nothing changed
        self.assertEqual(collect.form_built(form.read_text(encoding="utf-8")), stamp)
        collect.save(run, early)                                                  # the earlier paste still saves
        collect.build(run)                                                        # answered, the same questions: the
        self.assertEqual(collect.form_built(form.read_text(encoding="utf-8")), stamp)   # template only, the same stamp
        self.assertEqual(yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))["status"], "done")
        (run / collect.QUESTIONS).write_text((run / collect.QUESTIONS).read_text(encoding="utf-8")
                                             .replace("Where does a delivery show?", "Where does it show?"), encoding="utf-8")
        with self.assertRaises(SystemExit) as no:                                 # k6d, k6e: a changed question, never
            collect.build(run)
        self.assertIn("answered", str(no.exception))
        other = self.run_with_slug("edited_answer")                               # k6b: a body edited by hand
        collect.build(other)
        collect.save(other, self.paste(other, "Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All."))
        card = yaml.safe_load((other / "run.yaml").read_text(encoding="utf-8"))
        card.update({"status": "waiting", "passes": []})
        (other / "run.yaml").write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")
        answers = other / collect.ANSWERS
        answers.write_text(answers.read_text(encoding="utf-8").replace("- [x] A · In the Report.\n- [ ] B · In both.",
                                                                       "- [ ] A · In the Report.\n- [x] B · In both."), encoding="utf-8")
        with self.assertRaises(SystemExit) as no:
            collect.close(other)
        self.assertIn("not what save writes", str(no.exception))
        self.assertEqual(yaml.safe_load((other / "run.yaml").read_text(encoding="utf-8"))["status"], "waiting")
        answers.write_text(answers.read_text(encoding="utf-8").replace("- [ ] A · In the Report.\n- [x] B · In both.",
                                                                       "- [x] A · In the Report.\n- [ ] B · In both.")
                           .replace("\n", "\r\n") + "\r\n", encoding="utf-8", newline="")   # k6b2: CRLF and one more line end
        self.assertTrue(collect.close(other).is_file())
        self.assertEqual(yaml.safe_load((other / "run.yaml").read_text(encoding="utf-8"))["status"], "done")

    def test_a_new_template_alone_never_makes_a_form_stale(self):
        """0.6.1: save compares the questions a form was built from, not its markup; a form from before 0.6.1 (no
        questions inside) is compared on its cards' words. A changed question is still refused."""
        run = self.run_with()
        form = collect.build(run)
        text = form.read_text(encoding="utf-8")
        self.assertIn('id="haipipe-questions"', text)
        lines = ("Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All.")
        form.write_text(text.replace("<style>", "<style>/* a later template */"), encoding="utf-8")   # new markup, same questions
        pasted = self.paste(run, *lines)
        older = collect.QUESTIONS_IN_FORM.sub("", form.read_text(encoding="utf-8"))   # as if built before 0.6.1
        form.write_text(older, encoding="utf-8")
        self.assertTrue(collect.save(run, pasted).is_file())
        other = self.run_with_slug("question_changed")
        collect.build(other)
        source = other / collect.QUESTIONS
        source.write_text(source.read_text(encoding="utf-8").replace("Which buttons?", "Which buttons now?"), encoding="utf-8")
        with self.assertRaises(SystemExit) as no:
            collect.save(other, self.paste(other, *lines))
        self.assertIn("the form no longer matches", str(no.exception))

    def test_my_own_decision_is_a_choice_with_its_words(self):
        """JL 261031: "you should have something like others: like I will add my decisions": every question's last
        choice is the person's own decision; its words are the note, then required."""
        run = self.run_with()
        form = collect.build(run)
        text = form.read_text(encoding="utf-8")
        self.assertEqual(text.count('value="own"'), 2)                            # one per question
        self.assertEqual(collect.card_words(text),                                # older forms are not made stale by it
                         collect.card_words(re.sub(r'<label class="opt own">.*?</label>', "", text, flags=re.S)))
        with self.assertRaises(SystemExit) as no:
            collect.save(run, self.paste(run, "Q1 · Report or Delivery: my own decision", "Q2 · View buttons: B · No All."))
        self.assertIn("has no words", str(no.exception))
        self.assert_nothing_saved(run)
        out = collect.save(run, self.paste(run, "Q1 · Report or Delivery: my own decision",
                                           "   note: Show it in Work, under each Job.", "Q2 · View buttons: B · No All."))
        answer = out.read_text(encoding="utf-8")
        self.assertIn("Answer: my own decision.\n\n> decision: Show it in Work, under each Job.", answer)
        self.assertIn("- [ ] A · In the Report.\n- [ ] B · In both.", answer)          # no option ticked
        kept = collect.picks(collect.KEPT_PASTE.search(answer).group(1))[0]         # the answered view reads it back
        self.assertEqual(kept["Q1"]["pick"], collect.OWN)

    def test_a_block_folder_reached_through_a_link_still_names_its_own_run(self):
        """The tester's x2: a symlink standing for the Block folder; the path still leads to this Run's form."""
        run = self.run_with()
        collect.build(run)
        (Path(self.tmp.name) / "link_x").symlink_to(self.task.parent.parent, target_is_directory=True)
        linked = f"/link_x/j01_y/t01_z/runs/{run.name}/{run.name}.html"
        lines = ("Q1 · Report or Delivery: A · In the Report.", "Q2 · View buttons: B · No All.")
        other = self.run_with_slug("report_and_delivery")                     # the same Run name, another page
        collect.build(other)
        with self.assertRaises(SystemExit):
            collect.save(other, self.paste(other, *lines, form=linked))
        self.assertTrue(collect.save(run, self.paste(run, *lines, form=linked)).is_file())

    def test_invalid_picks_are_refused_before_anything_is_written(self):
        """Codex review 261031: a pick must be one of its question's options; unknown, twice-given or stale lines
        are refused, and nothing is written; "no option picked" and notes still save."""
        run = self.run_with()
        collect.build(run)
        q2 = "Q2 · View buttons: B · No All."
        for lines, title, words in (
                (["Q1 · Report or Delivery: Z · Nonexistent choice.", q2], "Report and Delivery", "Z is not one of its options"),
                (["Q1 · Report or Delivery: A · In the Report.", q2, "Q9 · Extra: A · x"], "Report and Delivery", "Q9 is not one"),
                (["Q1 · Report or Delivery: A · In the Report.", "Q1 · Report or Delivery: B · In both.", q2],
                 "Report and Delivery", "Q1 is answered twice"),
                (["Q1 · Report or Delivery: A · In the Report, as it read before.", q2], "Report and Delivery", "an older form"),
                (["Q1 · Report or Delivery, older: A · In the Report.", q2], "Report and Delivery", "is titled"),
                (["Q1 · Report or Delivery: A · In the Report.", q2], "An older title", "the questions say 'Report and Delivery'"),
                (["Q1 · Report or Delivery: A · In the Report."], "Report and Delivery", "no line for Q2")):
            with self.assertRaises(SystemExit) as no:
                collect.save(run, self.paste(run, *lines, title=title))
            self.assertIn(words, str(no.exception))
            self.assert_nothing_saved(run)
        out = collect.save(run, self.paste(run, "Q1 · Report or Delivery: (no option picked)", "   note: ask me again", q2,
                                           form=str(run / (run.name + ".html"))))
        self.assertIn("Answer: none picked.", out.read_text(encoding="utf-8"))

    def test_an_interrupted_save_keeps_its_answers(self):
        """Codex review 261031: answers already on disk close the Run even when the card still says waiting."""
        run = self.run_with()
        collect.build(run)
        lines = ("Q1 · Report or Delivery: B · In both.", "Q2 · View buttons: B · No All.")
        collect.save(run, self.paste(run, *lines), datetime(2026, 10, 31, 12, 0))
        kept = (run / collect.ANSWERS).read_text(encoding="utf-8")
        card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))
        card.update({"status": "waiting", "passes": []})                        # the card was never updated (k2: the pass was)
        (run / "run.yaml").write_text(yaml.safe_dump(card, sort_keys=False), encoding="utf-8")
        with self.assertRaises(SystemExit) as no:
            collect.save(run, self.paste(run, "Q1 · Report or Delivery: A · In the Report.", lines[1]))
        self.assertIn("already saved and closed", str(no.exception))
        self.assertIn("collect.py close finishes it", str(no.exception))
        collect.close(run)                                                       # finishes it, answers untouched
        card = yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))
        self.assertEqual((card["status"], card["passes"]), ("done", ["p01-1031"]))   # the pass already written, reused
        self.assertEqual((run / collect.ANSWERS).read_text(encoding="utf-8"), kept)
        self.assertEqual([x.name for x in (run / "passes").iterdir()], ["p01-1031"])
        other = self.run_with_slug("partial_answer")                            # k6: a file that is no saved answer
        collect.build(other)
        (other / "result").mkdir()
        (other / collect.ANSWERS).write_text("partial\n", encoding="utf-8")
        with self.assertRaises(SystemExit) as no:
            collect.close(other)
        self.assertIn("not a saved answer", str(no.exception))
        self.assertEqual(yaml.safe_load((other / "run.yaml").read_text(encoding="utf-8"))["status"], "waiting")

    def test_a_form_older_than_its_questions_and_a_note_at_column_zero(self):
        """The tester's c4f2 and c6g: a question reworded after the build is refused (file times, no hash); a note's
        later line keeps counting at column 0, until a blank line; kept picks follow their option's text."""
        run = self.run_with()
        form = collect.build(run)
        self.assertIn("filter(function(o){ return o.text === a.text; })", form.read_text(encoding="utf-8"))
        source = run / collect.QUESTIONS
        source.write_text(source.read_text(encoding="utf-8").replace("Which buttons?", "Which buttons, now?"), encoding="utf-8")
        os.utime(form, (source.stat().st_mtime - 5, source.stat().st_mtime - 5))   # the form was built before the edit
        lines = ("Q1 · Report or Delivery: A · In the Report.", "   note: keep year first,", "         ",
                 "but put 2020 last.", "Q2 · View buttons: B · No All.")
        old = self.paste(run, *lines)                                            # copied from the first build
        with self.assertRaises(SystemExit) as no:                               # c4f2: the question changed after the build
            collect.save(run, old)
        self.assertIn("the form no longer matches", str(no.exception))
        self.assert_nothing_saved(run)
        collect.build(run)
        with self.assertRaises(SystemExit) as no:                               # c4f3: rebuilt, then the old paste
            collect.save(run, old)
        self.assertIn("reload this Run's form and copy again", str(no.exception))
        self.assert_nothing_saved(run)
        os.utime(source, None)                                                   # c4f4: touched, the same content
        text = collect.save(run, self.paste(run, *lines)).read_text(encoding="utf-8")
        self.assertIn("> note: keep year first,\n> \n> but put 2020 last.", text)   # n1: both paragraphs

    def test_an_open_sketch_is_one_line_not_a_traceback(self):
        run = self.run_with(QUESTIONS.replace("today ─▶ A\n```", "today ─▶ A"))
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(collect.main(["check", str(run)]), 1)
        self.assertRegex(out.getvalue(), r"^r01_collect_report_and_delivery/question_collection\.md: a ``` block is never closed\n$")
        with self.assertRaises(SystemExit):
            collect.build(run)

    def test_a_form_with_nothing_picked_says_so_and_answers_without_my_pick(self):
        """b15 r02_simulate_task_workflow (261101): a labeling report preselects nothing; its form must not claim a
        pick, its answer lines must not say "changed from my pick", and once saved it reopens read only."""
        blank = QUESTIONS.replace("- [x] A · In the Report.", "- [ ] A · In the Report.").replace(
            "Why A: One thing in one place.\n", "")
        run = self.run_with(blank)
        form = collect.build(run)
        page = form.read_text(encoding="utf-8")
        stamp = collect.form_built(page)
        self.assertIn("Nothing is picked for you", page)
        self.assertNotIn("My pick is selected", page)
        collect.save(run, self.paste(run, "Q1 · Report or Delivery: B · In both.", "Q2 · View buttons: A · All first."))
        answers = (run / collect.ANSWERS).read_text(encoding="utf-8")
        self.assertIn("Answer: B.", answers)
        self.assertIn("Answer: A.", answers)
        self.assertNotIn("changed from my pick", answers)
        again = form.read_text(encoding="utf-8")
        data = json.loads(re.search(r'id="form-data">(.*?)</script>', again, re.S).group(1))
        self.assertEqual(data["answered"]["picks"]["Q1"]["pick"], "B")              # read only, the person's picks
        self.assertEqual(collect.form_built(again), stamp)                           # the same build stamp
        self.assertEqual(yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8"))["status"], "done")

    def test_a_form_with_my_pick_keeps_its_words(self):
        run = self.run_with()
        page = collect.build(run).read_text(encoding="utf-8")
        self.assertIn("My pick is selected", page)
        collect.save(run, self.paste(run, "Q1 · Report or Delivery: B · In both. (changed from A)",
                                     "Q2 · View buttons: A · All first."))
        answers = (run / collect.ANSWERS).read_text(encoding="utf-8")
        self.assertIn("Answer: B, changed from my pick A.", answers)
        self.assertIn("Answer: A.", answers)                                         # Q2 had no pick of mine


class RecordTest(unittest.TestCase):
    """A decision made in the chat is kept like an answered form (JL 261031: "the big decisions like this should also
    be recorded")."""

    def test_a_chat_decision_is_a_done_interaction_with_its_words_and_flag(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page"
            page.mkdir()
            waiting = collect.new(page, "open_form", "Open form", for_="b01-s01:x @ y")
            card = yaml.safe_load((waiting / "run.yaml").read_text()); card["status"] = "waiting"
            (waiting / "run.yaml").write_text(yaml.safe_dump(card))
            run = collect.record(page, "views", "Board views", "b01-s01:x @ y",   # a waiting form never blocks it
                                 [("Report parts", "Idea, Story, Venue", "we should have the idea")], "focus_draft.py",
                                 now=datetime(2026, 10, 31, 17, 0))
            self.assertEqual(run.name, "r02_collect_views")
            card = yaml.safe_load((run / "run.yaml").read_text())
            self.assertEqual((card["status"], card["source"]), ("done", "chat"))
            answers = (run / collect.ANSWERS).read_text()
            self.assertIn("Answer: my own decision.", answers)
            self.assertIn("> decision: Idea, Story, Venue", answers)
            self.assertIn('Said in the chat: "we should have the idea"', answers)
            self.assertIn("Q1 · applied · ", (run / collect.APPLIED).read_text())
            again = collect.record(page, "other_slug", "Ignored", "b01-s01:x @ y",   # the same topic: appended, one set
                                   [("Second", "a second decision", "more words")], now=datetime(2026, 10, 31, 18, 0))
            self.assertEqual(again, run)
            text = (run / collect.ANSWERS).read_text()
            self.assertIn("## Q2 · Second", text)
            self.assertIn("> decision: Idea, Story, Venue", text)
            with self.assertRaises(SystemExit):                                   # every part filled
                collect.record(page, "empty", "Empty", "b01-s01:x @ y", [("A title", "", "words")])

    def test_know_keeps_notes_that_wait_on_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "b01_x"
            page.mkdir()
            run = collect.know(page, "to_know", "To Know", "b01-s01:x @ y", [("First", "a thing to know", "the place")],
                               now=datetime(2026, 11, 5, 9, 0))
            card = yaml.safe_load((run / "run.yaml").read_text())
            self.assertEqual((card["status"], card["source"]), ("done", "know"))
            self.assertIn("a thing to know", (run / f"{run.name}.html").read_text())
            self.assertFalse((run / collect.ANSWERS).exists())
            again = collect.know(page, "other", "Ignored", "b01-s01:x @ y", [("Second", "one more")])  # the same topic: appended
            self.assertEqual(again, run)
            self.assertIn("## Q2 · Second", (run / collect.QUESTIONS).read_text())
            collect.applied(run, ["Q1"], "fixed in a.py")                         # settled: the page says so
            self.assertIn("✅ applied", (run / f"{run.name}.html").read_text())
            with self.assertRaises(SystemExit):
                collect.know(page, "bad", "Bad", "b01-s01:x @ y", [("A title", "")])


if __name__ == "__main__":
    unittest.main()
