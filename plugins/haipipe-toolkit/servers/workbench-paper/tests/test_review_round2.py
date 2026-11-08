"""Stage-2 review round 2 of the paper pages (261106): the whole-paper check shows once, each citation key is counted
once, the Values word agrees with the check, a submission's letter link opens its own version, a version's MindMap
carries the send's facts and a revision's reviewer points, a Section's map and steps read the text its Text shows, and
the evidence Tasks show what they made first. Placeholders only: the Board is written into a temp folder."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page, frame  # noqa: E402

SECTION = ("# {t} · Summary\ntask-type: draft\nreader-question: <what the reader asks>\n\n## Opening\n\n<one opening line>.\n\n"
           "## Content\n\n#### C1.P1 · Background · S1 to S2\nThe first sentence states the problem \\citep{{key2024}}. "
           "The second sentence says why.\n\n## Aims\n\n- Target: <the aim> · Done when: <the close> · Now: not started\n")
CITES = ("key,group,status,cited_in,sentences,bib_entry,bib_in,in_reference_bib,doi,doi_conflict,title,year,doi_record,"
         "verified,cite_card,card_gaps,discovery_runs\n"
         "key2024,t01_cite,bib-only,t01_intro C1.P1.1,1,yes,t01_intro,no,10.0/x,,<a title>,2024,no,no signed Result,,,\n"
         "key2021,t01_cite,bib-only,t01_intro C1.P1.2,1,yes,t01_intro,no,,,<a title>,2021,no,no signed Result,,,\n"
         "key2022,t01_cite,missing-bib,t01_intro C1.P1.2,1,no,,no,,,,,no,no signed Result,,,\n")
CHECK = """task: t99_check
rows:
- {where: t03_results C2.P1.B2, status: differs, printed: '4.10', value: '4.12', key: sub.b}
- {where: t03_results C2.P1.B1, status: match, printed: '2.35', value: '2.35', key: main.b}
never_printed: []
printed_unbound: []
"""
REPORT = """# q01_review · Comments on version 1

## Feedback Concern Table

| item | source | concern | local severity | review item | state |
|---|---|---|---|---|---|
| R1.1 | Reviewer 1 | Say how <the policy> was assigned | material | Review-a | open |

## Review Items

| item | cites | lands on | work | reply | state |
|---|---|---|---|---|---|
| Review-a | R1.1 | t02_methods ¶1 | run-revise-a | P1 | answered |
"""


def views_of(page: str) -> list:
    nav = re.search(r'<nav class="section-views".*?</nav>', page, re.S)[0]
    return re.findall(r'group=([^"&]+)', nav)


def result(task: Path, run: str, name: str, text: str) -> None:
    d = task / "runs" / run / "result"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(text, encoding="utf-8")
    (d / "runtime.yaml").write_text("status: completed\n", encoding="utf-8")


class ReviewRound2Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        b = self.b = self.root / "paper" / "Paper-X"
        b.mkdir(parents=True)
        (b / "board.md").write_text("# Paper-X\n\nboard-kind: paper-board\n", encoding="utf-8")
        for v, extra in (("j11_writing_v1130_desk", "from: none\n"),
                         ("j12_writing_v0215_desk", "from: j11_writing_v1130_desk\nresponds-to: reports/q01_review/q01_review.md\n")):
            (b / v).mkdir()
            (b / v / f"{v}.md").write_text(f"# {v} · a send\nstate: drafting\nvenue: Example Journal\ngoal: <the send>\n{extra}",
                                           encoding="utf-8")
            for t in ("t00_summary", "t31_cover-letter"):
                (b / v / t).mkdir()
                (b / v / t / f"{t}.md").write_text(SECTION.format(t=t), encoding="utf-8")
        rep = b / "j12_writing_v0215_desk" / "reports" / "q01_review"
        rep.mkdir(parents=True)
        (rep / "q01_review.md").write_text(REPORT, encoding="utf-8")
        cite = b / "j03_evidence_cite"
        for t in ("t01_cite", "t99_check"):
            (cite / t).mkdir(parents=True)
            (cite / t / f"{t}.md").write_text(f"# {t}\nlabel: {t}\nstatus: see runs\n", encoding="utf-8")
            result(cite / t, "r01_check_citations", "citations.csv", CITES)
        value = b / "j02_evidence_value"
        (value / "t99_check").mkdir(parents=True)
        (value / "t99_check" / "t99_check.md").write_text("# t99_check\nlabel: Paper value check\n", encoding="utf-8")
        result(value / "t99_check", "r01_check_values", "values.yaml", CHECK)
        (value / "t01_values").mkdir()
        (value / "t01_values" / "t01_values.md").write_text("# t01_values\nlabel: Values\n", encoding="utf-8")
        result(value / "t01_values", "r01_collect_values", "values.yaml", CHECK)
        sub = b / "j21_submission_v1130_desk"
        (sub / "t01_cover-letter").mkdir(parents=True)
        (sub / "j21_submission_v1130_desk.md").write_text("# j21\nfor: j11_writing_v1130_desk\n", encoding="utf-8")
        (sub / "t01_cover-letter" / "t01_cover-letter.md").write_text(
            "# t01_cover-letter\nwords-in: ../../j11_writing_v1130_desk/t31_cover-letter\n", encoding="utf-8")
        walk = sub / "t02_portal-walk"
        walk.mkdir()
        (walk / "t02_portal-walk.md").write_text("# t02_portal-walk\ntask-type: description\n", encoding="utf-8")
        result(walk, "r01_read_portal", "portal-fields.yaml",
               "portal: <a portal>\ndraft_saved: 'not opened yet: a starter'\nsteps:\n- step: 1 Files\n  fields:\n"
               "  - {id: fi.m, label: Manuscript, kind: upload, required: true, now: ''}\n")
        self.theme = frame.Theme(name="paper")

    def render(self, folder, section="", group=""):
        return focus_page.render(self.theme, self.root, folder, section, group)

    def test_citations_count_each_key_once_and_the_check_shows_once(self):
        for page in (self.render(self.b, "report", "evidence"), self.render(self.b / "j03_evidence_cite", "report", "cite-list"),
                     self.render(self.b / "j11_writing_v1130_desk", "report", "citations")):
            self.assertIn("Citations<span class=word>0 of 3 keys verified</span>", page)   # was "0 of 6": t01 and t99
            self.assertIn("🙋 1 key not in the bib: key2022", page)                        # under the closed bar
            if "j03_evidence_cite" not in page.split("<title>")[1][:40]:                 # the check, once, a line; the
                self.assertIn("The whole-paper check", page)                              # citation Job's Check view owns it
            self.assertNotIn('<b>t99_check</b>', page)                                    # never a tab of its own
            self.assertNotIn("<iframe", page.split("Citations<span")[1].split("🙋 Interaction")[0])   # cards, no frame
        check = self.render(self.b / "j03_evidence_cite", "report", "cite-check")
        self.assertIn("Check<span class=word>0 of 3 keys verified</span>", check)
        listed = self.render(self.b / "j03_evidence_cite", "report", "cite-list")
        self.assertNotIn("class=ev-row", listed.split("Citations<span")[1].split("🙋 Interaction")[0])   # r03: one line per
        self.assertIn("class=ev-row", check)                                                            # key; Check: cards

    def test_the_values_word_agrees_with_the_check(self):
        listed = self.render(self.b / "j02_evidence_value", "report", "value-list")
        check = self.render(self.b / "j02_evidence_value", "report", "value-check")
        version = self.render(self.b / "j11_writing_v1130_desk", "report", "values")
        for page in (check, version, listed):
            self.assertIn("🙋 1 printed number to fix: t03_results C2.P1.B2 prints 4.10, its Run returned 4.12", page)
        self.assertIn("Check<span class=word>1 differs</span>", check)
        self.assertNotIn("iframe", check.split("Check<span")[1].split("🙋 Interaction")[0])   # each row drawn

    def test_a_submission_links_its_own_versions_letter(self):
        letter = self.render(self.b / "j21_submission_v1130_desk", "work", "work-letter")
        links = re.findall(r'href="([^"]*t31_cover-letter[^"]*)"', letter)
        self.assertTrue(links)
        self.assertTrue(all("j11_writing_v1130_desk" in x for x in links), links)   # r01: it opened j12's letter

    def test_a_versions_mindmap_carries_the_send_and_the_reviewer_points(self):
        first = self.render(self.b / "j11_writing_v1130_desk", "report", "mindmap")
        self.assertIn("This send", first)
        self.assertIn("&lt;what the reader asks&gt;", first)                         # each Section's question
        self.assertNotIn("Reviewer points", first)
        rev = self.render(self.b / "j12_writing_v0215_desk", "report", "mindmap")
        self.assertIn("Reviewer points", rev)
        self.assertIn("Say how &lt;the policy&gt; was assigned", rev)
        self.assertIn("t02_methods ¶1", rev)
        self.assertIn('href="/_board/workbench?path=paper/Paper-X/j11_writing_v1130_desk&amp;layout=focus"', rev)   # from
        self.assertIn(">responds to<", rev)                                          # the comments it answers
        self.assertIn("q01_review.md", rev)                                          # opening the report

    def test_a_sections_map_and_steps_read_the_text_its_text_shows(self):
        sec = self.b / "j11_writing_v1130_desk" / "t00_summary"
        mind = self.render(sec, "report", "mindmap")
        self.assertNotIn("Nothing to map yet", mind)
        self.assertIn("The first sentence states the problem", mind)
        self.assertNotIn("\\citep", mind)
        text = self.render(sec, "report", "text")
        self.assertIn("<section class=fd-sec data-open>", text)                      # the Text starts open
        self.assertIn("[<span title=\"not in this Section's bib\">key2024 ⚠</span>]", text)   # a key the bib lacks (r03)
        for step in ("write", "revise"):
            page = self.render(sec, "work", step)
            self.assertIn("The adopted text", page, step)
            self.assertNotIn("No text yet.", page, step)
        self.assertNotIn("<p class=pb-sess>", self.render(sec, "work", "write"))   # the session line rides the copy only
        status = self.render(sec, "report", "status")
        self.assertIn("&lt;the aim&gt;", status)
        self.assertIn("&lt;one opening line&gt;", status)

    def test_evidence_tasks_show_what_they_made_first(self):
        cite = self.b / "j03_evidence_cite" / "t01_cite"
        report, work = self.render(cite, "report"), self.render(cite, "work")
        self.assertEqual(views_of(report), ["mindmap", "findings", "standing"])
        self.assertEqual(views_of(work), ["work-findings", "work-standing"])
        self.assertNotIn(">Progress<", work)
        made = self.render(cite, "report", "findings")
        self.assertIn("1 · 📚 Its citations<span class=word>0 of 3 keys verified</span>", made)
        self.assertIn("pb-side", made)                                               # a side tab per key
        self.assertIn("not in the bib", made)                                        # plain words, not missing-bib
        values = self.render(self.b / "j02_evidence_value" / "t01_values", "work", "work-findings")
        self.assertLess(values.index("⚙️ Process"), values.index("📊 Results"))
        self.assertIn("Its values<span class=word>1 differs</span>", values)
        walk = self.render(self.b / "j21_submission_v1130_desk" / "t02_portal-walk", "report", "findings")
        self.assertIn("starter, not walked", walk)
        self.assertIn("🙋 A person starts this walk", walk)


if __name__ == "__main__":
    unittest.main()
