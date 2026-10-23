"""evidence_ledger.py on a made-up project: a version whose Sections read one value from two Runs, label one value
two ways, show more displays than the venue allows, show displays that have not passed the revise loop, and frame
a picture that no work Run drew.
Placeholders only, no real project data."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import evidence_ledger as led  # noqa: E402

BIB = "@article{doe2026demo,\n  author = {Doe, Jane and Roe, Rick},\n  title = {A demo paper},\n  journal = {Demo},\n  year = {2026}\n}\n"


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def cards(*items: str) -> str:
    return "evidence:\n" + "".join(items)


VALUE = ("  - kind: value\n    source: b01.j01.t01\n    items:\n"
        "      - {{run: {run}, for: [1], anchor: ['4.1'], file: metrics.json, key: effect}}\n")
CITE = "  - kind: cite\n    source: b01.j01.t01\n    items:\n      - {run: r01, for: [2], anchor: ['a demo']}\n"
NEED = "  - kind: cite\n    title: Sources still needed\n    items:\n      - {need: 'a source', for: [3], anchor: ['x']}\n"


def review(unit: Path, question: str = "Does the effect differ by group?", **rounds: str) -> None:
    """A display unit's README (with its question: when given) and its review rounds, {"r01": "<scores line>"}."""
    write(unit / "README.md", f"# {unit.name}\n" + (f"question: {question}\n" if question else "") + "claim: a demo claim\n")
    for rnd, line in rounds.items():
        write(unit / "review" / f"{rnd}.md", f"# {unit.name} · review {rnd}\n\nround: {rnd}\n\n### {unit.name}\n{line}\n")


DRAWN = "work/b03_demo/j09_demo_displays/t01_figure1_effect/runs/r01_draw/result"


def drawn_by(unit: Path, run: str = DRAWN) -> None:
    """The unit's intake points at the work Run that draws its picture."""
    write(unit / "intake/manifest.yaml", f"sources:\n  - role: asset\n    path: {run}/figure.pdf\n")


PASS = "scores: question 9 · readability 8 · honesty 8 · journal-ready 8 · overall 8.5"
FAIL = "scores: question 6 · readability 5 · honesty 7 · journal-ready 5 · overall 5.5"


def item(item_id: str, label: str, result: str = "") -> str:
    run = result.split("/")[1] if result else ""
    local = f"- **Local Run**: Page · Evidence Item · new-run · {run} → {result}\n" if result else ""
    return f"### {item_id} · C1.P1.B1 · a value\n- **Target**: C1.P1.B1\n- **Label**: {label}\n{local}\n"


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "Project-Demo"
        write(root / "project.yaml", "name: demo\n")
        for run, effect in (("r01_first", 0.041), ("r02_second", 0.043)):
            write(root / f"work/b01_demo/j01_demo/t01_demo/runs/{run}/result/metrics.json", json.dumps({"effect": effect}))
        write(root / "discovery/b01_demo/j01_demo/t01_demo/runs/r01_paper/result/doe2026.bib", BIB)
        write(root / DRAWN / "figure.pdf", "%PDF placeholder\n")
        self.job = root / "paper/Paper-Demo/j01_v1019_demo"
        write(root / "paper/Paper-Demo/board.md", "# Paper-Demo\n")
        for t in ("t00_abstract", "t03_results", "t05_discussion", "t21_appendix"):
            write(self.job / t / f"{t}.md", f"# {t}\ntask-type: draft\npage-type: section\n")
        write(self.job / "t00_abstract/evidence/cards.yaml", cards(VALUE.format(run="r01"), CITE))
        write(self.job / "t03_results/evidence/cards.yaml", cards(VALUE.format(run="r01"), NEED))
        write(self.job / "t05_discussion/evidence/cards.yaml", cards(VALUE.format(run="r02")))
        for d in ("Display1-effect", "Display2-cohort"):
            (self.job / "t03_results/display" / d).mkdir(parents=True)
        (self.job / "t21_appendix/display/Display1-cohort").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_one_value_read_from_two_runs_is_flagged(self):
        L = led.ledger(self.job)
        self.assertTrue(any("one value, two Runs" in b and "r01 in t00_abstract, t03_results" in b
                            and "r02 in t05_discussion" in b for b in L["bad"]), L["bad"])

    def test_sections_are_read_in_order_with_their_part_and_counts(self):
        L = led.ledger(self.job)
        self.assertEqual([(s["task"], s["part"]) for s in L["sections"]],
                         [("t00_abstract", "abstract"), ("t03_results", "main"), ("t05_discussion", "main"),
                          ("t21_appendix", "appendix")])
        abstract = L["sections"][0]
        self.assertEqual((abstract["cite"], abstract["work"], abstract["shape"]), (1, 1, "cards"))
        self.assertEqual(L["sections"][0]["rows"][0]["value"], 0.041)
        self.assertEqual(L["open_cite"], 1)                     # the needed source in t03

    def test_displays_are_numbered_for_the_paper_and_held_to_the_limit(self):
        L = led.ledger(self.job, max_displays=1)
        self.assertEqual([n for n, _, _ in L["displays"]], ["Display 1", "Display 2", "eDisplay 1"])
        self.assertTrue(any("too many displays: 2" in b for b in L["bad"]))
        self.assertTrue(any("one display twice: cohort" in w for w in L["warn"]))

    def test_an_older_page_label_with_different_estimates_is_a_conflict_and_a_copy_is_not(self):
        for t, res, est in (("t03_results", "results/run-value-a", 0.5), ("t05_discussion", "results/run-value-b", 0.7)):
            write(self.job / t / "draft" / f"{t}-evidence-items.md", item("E01-VALUE-effect", "Effect", res + "/result.yaml"))
            write(self.job / t / res / "result.yaml", f"estimate: {est}\n")
        L = led.ledger(self.job)
        self.assertTrue(any("one label, different estimates: Effect" in b for b in L["bad"]), L["bad"])
        write(self.job / "t05_discussion/results/run-value-b/result.yaml", "values:\n  estimate: 0.5\n")
        L = led.ledger(self.job)
        self.assertFalse(any("Effect" in b for b in L["bad"]), L["bad"])
        self.assertTrue(any("the same estimates: Effect" in w for w in L["warn"]), L["warn"])

    def test_percentage_points_and_proportions_compare_in_one_unit(self):
        for t, res, body in (("t03_results", "results/run-value-a", "estimate: 0.0007\n"),
                             ("t05_discussion", "results/run-value-b", "estimate_pp: 0.07\n")):
            write(self.job / t / "draft" / f"{t}-evidence-items.md", item("E01-VALUE-effect", "Effect", res + "/result.yaml"))
            write(self.job / t / res / "result.yaml", body)
        L = led.ledger(self.job)
        self.assertFalse(any("Effect" in b for b in L["bad"]), L["bad"])
        write(self.job / "t05_discussion/results/run-value-b/result.yaml", "estimate_pp: -0.07\n")
        L = led.ledger(self.job)
        self.assertTrue(any("different estimates: Effect" in b and "estimate 0.0007 vs estimate_pp -0.07" in b
                            for b in L["bad"]), L["bad"])

    def test_a_section_out_of_the_compile_order_is_not_numbered_counted_or_compared(self):
        write(self.job / f"{self.job.name}.md", "# demo\n<!-- haipipe:compile-order:start -->\nmain:\n- t00_abstract\n"
              "- t03_results\nappendix:\n- t21_appendix\n<!-- haipipe:compile-order:end -->\n")
        L = led.ledger(self.job)
        self.assertEqual([s["task"] for s in L["sections"] if not s["printed"]], ["t05_discussion"])
        self.assertFalse(any("two Runs" in b for b in L["bad"]), L["bad"])     # t05's r02 no longer prints

    def test_one_citation_key_with_two_years_is_flagged(self):
        for t, year in (("t00_abstract", "2024"), ("t03_results", "2023")):
            write(self.job / t / "draft/evidence/bibex" / f"{t}.bib",
                  f"@misc{{ada2024,\n  title = {{Standards of Care}},\n  year = {{{year}}},\n}}\n")
        L = led.ledger(self.job)
        self.assertTrue(any("one citation key, two entries: ada2024" in b and "2024" in b and "2023" in b
                            for b in L["bad"]), L["bad"])
        # the same entry written on one line, with more fields, is the same entry
        write(self.job / "t03_results/draft/evidence/bibex/t03_results.bib",
              "@misc{ada2024, title={Standards of {Care}}, year={2024}, month=Jan, pages={1--9}}\n")
        L = led.ledger(self.job)
        self.assertFalse(any("ada2024" in b for b in L["bad"]), L["bad"])

    def test_a_main_text_display_without_a_question_or_a_passing_review_is_flagged(self):
        units = self.job / "t03_results/display"
        review(units / "Display1-effect", r01=FAIL, r02=PASS)               # the latest round passes
        review(units / "Display2-cohort", question="", r01=FAIL)            # no question:, and r01 fails
        drawn_by(units / "Display1-effect"); drawn_by(units / "Display2-cohort")
        L = led.ledger(self.job)
        self.assertFalse(any("Display1-effect" in b for b in L["bad"]), L["bad"])
        self.assertIn("display has no question: t03_results/Display2-cohort (its README names none)", L["bad"])
        self.assertTrue(any(b.startswith("display review not passed: t03_results/Display2-cohort (r01 overall 5.5/10")
                            and "readability 5" in b for b in L["bad"]), L["bad"])
        # an appendix display with no review is a ⚠️, not a ❗
        self.assertTrue(any("display review not passed: t21_appendix/Display1-cohort (no review/ round)" in w
                            for w in L["warn"]), L["warn"])
        self.assertFalse(any("t21_appendix" in b for b in L["bad"]), L["bad"])
        # the listing shows the latest score
        shown = led.show(L)
        self.assertIn("Display1-effect   r02 8.5/10 ✅", shown)
        self.assertIn("Display2-cohort   r01 5.5/10 open · no question:", shown)

    def test_a_display_not_drawn_by_a_work_run_of_the_versions_work_block_is_flagged(self):
        unit = self.job / "t03_results/display/Display1-effect"
        review(unit, r01=PASS)
        L = led.ledger(self.job)
        self.assertIn("display drawn inside the paper: t03_results/Display1-effect (it has no intake/manifest.yaml)", L["bad"])
        write(unit / "intake/manifest.yaml", "sources:\n  - role: values\n    path: intake/inputs/source_data.csv\n")
        self.assertTrue(any("Display1-effect (its intake/manifest.yaml names no work Run result/)" in b
                            for b in led.ledger(self.job)["bad"]))
        drawn_by(unit)
        self.assertFalse(any("Display1-effect" in b for b in led.ledger(self.job)["bad"]))
        # the version names another work Block
        write(self.job / f"{self.job.name}.md", "# demo\nwork-block: `work/b04_other`\n")
        self.assertTrue(any("Display1-effect (it reads work/b03_demo, the version's work-block: is work/b04_other)" in b
                            for b in led.ledger(self.job)["bad"]))
        write(self.job / f"{self.job.name}.md", "# demo\nwork-block: work/b03_demo\n")
        self.assertFalse(any("Display1-effect" in b for b in led.ledger(self.job)["bad"]))
        # a Run that is not on disk, and a Run outside the display Job
        drawn_by(unit, "work/b03_demo/j09_demo_displays/t01_figure1_effect/runs/r02_gone/result")
        self.assertTrue(any("r02_gone/result is not on disk" in b for b in led.ledger(self.job)["bad"]))
        write(self.job.parents[2] / "work/b03_demo/j02_question/t01_q/runs/r01/result/figure.pdf", "%PDF\n")
        drawn_by(unit, "work/b03_demo/j02_question/t01_q/runs/r01/result")
        L = led.ledger(self.job)
        self.assertFalse(any("Display1-effect" in b for b in L["bad"]), L["bad"])
        self.assertTrue(any(w.startswith("display outside the display Job: t03_results/Display1-effect") for w in L["warn"]))

    def test_the_pass_rule_needs_overall_8_and_every_dimension_7_from_the_latest_round(self):
        unit = self.job / "t03_results/display/Display1-effect"
        review(unit, r09=PASS, r10="scores: question 9 · readability 6.5 · honesty 9 · journal-ready 9 · overall 8.5")
        r = led.unit_review(unit)
        self.assertEqual((r["round"], r["passed"]), ("r10", False))       # r10 is later than r09
        self.assertEqual(r["why"], "r10 overall 8.5/10, readability 6.5 under 7")
        review(unit, r11="scores: question 9/10 · readability 8/10 · honesty 9/10 · overall 8/10")
        self.assertEqual(led.unit_review(unit)["why"], "r11 has no score for journal-ready")
        review(unit, r12="4. **scores:** question 8 · readability 7 · honesty 7 · journal ready 7 · overall 8")
        self.assertTrue(led.unit_review(unit)["passed"])

    def test_the_command_exits_1_on_a_conflict_and_prints_the_ledger(self):
        self.assertEqual(led.main([str(self.job)]), 1)
        for t in ("t03_results", "t05_discussion"):
            (self.job / t / "evidence/cards.yaml").write_text(cards(VALUE.format(run="r01")), encoding="utf-8")
        (self.job / "t21_appendix/display/Display1-cohort").rename(self.job / "t21_appendix/display/Display1-extra")
        self.assertEqual(led.main([str(self.job)]), 1)                     # the main-text displays are not reviewed
        for d in ("Display1-effect", "Display2-cohort"):
            review(self.job / "t03_results/display" / d, r01=PASS)
        self.assertEqual(led.main([str(self.job)]), 1)                     # their pictures are not drawn by a work Run
        for d in ("Display1-effect", "Display2-cohort"):
            drawn_by(self.job / "t03_results/display" / d)
        self.assertEqual(led.main([str(self.job)]), 0)


if __name__ == "__main__":
    unittest.main()
