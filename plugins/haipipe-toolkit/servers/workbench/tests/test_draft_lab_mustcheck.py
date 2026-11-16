"""Draft Lab against haipipe-paper ref/must-check.md: full-address keys (M-D05), decided cards folded and answered
comments faded, stale ★ (M-D13), a checked sentence left alone (M-D06), the blind pair's `meaning: no` (M-D07), merged
earlier wordings, and name-year citations with "not in Bib" (M-D02). Every case runs on a temp Draft."""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import task_draft  # noqa: E402
from live import draft_steps  # noqa: E402
from live.draft_step_revise_keys import Keys  # noqa: E402

# a Draft numbered per paragraph, as the AITC LOI t01 was at v5.0: s1 repeats in C1.P1, C2.P1, C2.P2
PER_PARA = ("# Note · draft v5.0\n\n## 3 · Draft\n\n### C0.P0 · Title · s0\n- B0 · s0 · A title.\n\n"
            "### C1.P1 · Why · s1 to s2\n- B1 · s1 · Care relies on reports.\n- B2 · s2 · Reports decline.\n\n"
            "### C2.P1 · What · s1 to s2\n- B1 · s1 · We propose an agent.\n- B2 · s2 · It reads the record.\n\n"
            "### C2.P2 · How · s1\n- B1 · s1 · Each agent has four parts.\n")


def _line(sid, low, fix="none"):
    return f"- {sid} · logic {low}/10 · read {low}/10 · ai 9/10 · link: continues, carried · a problem · Fix: {fix}\n"


def _task(root: Path, draft: str, revise: str, version="v5.0", checked="", comments="") -> Path:
    task = root / "Project-X/paper/Paper-Demo/j01_writing_v1/t01_note"
    rec = task / "draft" / "records"
    rec.mkdir(parents=True)
    (root / "Project-X/paper/Paper-Demo/board.md").write_text("# Paper\n")
    (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
    (task / "draft" / f"t01_note-draft-{version}.md").write_text(draft)
    (rec / "t01_note-revise.md").write_text(revise)
    if checked:
        (rec / "t01_note-checked.md").write_text("# t01_note · checked sentences\n\n" + checked)
    if comments:
        (rec / "t01_note-comments.md").write_text("# t01_note · comments\n\n" + comments)
    return task


def _revise(lines: str, title="Pass 1 · 261115 · on draft v5.0", cards="") -> str:
    return (f"# t01_note · revise\n\n## {title}\n\n{cards}### Revise review report\nVerdict: ok.\nSentences:\n{lines}")


def _html(root, task):
    return task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html


def _stars(html):
    return re.findall(r'class="rv-card rv-rev" data-s="([^"]*)" data-state="review" data-low="([^"]*)"[^>]*?'
                      r'( data-stale=1| data-fixed=1)?>', html)


class FullAddressTest(unittest.TestCase):
    def test_a_full_address_report_gets_its_cards_and_stars(self):
        # the AITC t02 report shape: `- C3.P1.s1 · …`, a note before the scores, `Flow C3.P1:` lines
        draft = ("# Note · draft v6.2\n\n## 3 · Draft\n\n### C3.P1 · How · s1 to s2\n- B1 · s1 · We adapt Osler.\n"
                 "- B2 · s2 · Osler runs inside REACH.\n\n### C4.P1 · Aim 1 · s3\n- B1 · s3 · Aim 1 builds it.\n")
        lines = (_line("C3.P1.s1", 6, "We adapt Osler, a model.") + "- C4.P1.s3 · (v6.0 C4.P1.S1, now split) · "
                 + _line("x", 7)[6:] + "Flow C3.P1: topic s1 · weakest join s1 to s2\nFlow C4.P1: topic s3\n")
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(lines, "Pass 2 · 261115 · on draft v6.2"), "v6.2")
            html = _html(Path(tmp), task)
            self.assertEqual([s for s, _, _ in _stars(html)], ["s1", "s3"])      # unique ids: keyed bare as before
            self.assertIn('data-adopt="s1"', html)
            self.assertEqual(re.findall(r'rv-flow" data-s="[^"]*" data-p="([^"]*)"', html), ["C3.P1", "C4.P1"])
            self.assertNotIn("Cards on no sentence", html)

    def test_a_per_paragraph_draft_keys_every_line_by_its_full_address(self):
        # bare lines in paragraph blocks (each ends with its Flow P<k>), the title C0.P0 not scored and not counted
        lines = (_line("s1", 7) + _line("s2", 6, "Reports decline with age.") + "Flow P1: s1 → s2\n"
                 + _line("s1", 8) + _line("s2", 5) + "Flow P2: s1 → s2\n" + _line("s1", 6) + "Flow P3: four parts s1\n")
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), PER_PARA, _revise(lines))
            html = _html(Path(tmp), task)
            self.assertEqual([(s, low) for s, low, _ in _stars(html)],
                             [("C1.P1.s1", "7"), ("C1.P1.s2", "6"), ("C2.P1.s1", "8"), ("C2.P1.s2", "5"), ("C2.P2.s1", "6")])
            self.assertEqual(re.findall(r'rv-flow" data-s="[^"]*" data-p="([^"]*)"', html), ["C1.P1", "C2.P1", "C2.P2"])
            self.assertIn('data-adopt="C1.P1.s2"', html)
            # each ★ sits in its own sentence's row
            row = re.search(r'data-slot="C2.P1.s2">(.*?)</div></div>', html, re.S)
            self.assertIsNotNone(row)
            self.assertIn('data-low="5"', html[html.index('data-slot="C2.P1.s2"'):html.index('data-slot="C2.P2"')])

    def test_flow_p3_lands_on_the_third_paragraph_by_reading_order(self):
        k = Keys({"text": [("Draft", PER_PARA)]})
        self.assertTrue(k.rep)
        self.assertEqual([k.flow_pid(x) for x in ("P1", "P2", "P3", "C2.P1", "P9")], ["C1.P1", "C2.P1", "C2.P2", "C2.P1", ""])
        unique = Keys({"text": [("Draft", "### C3.P4 · a\n- B1 · s1 · One.\n\n### C3.P5 · b\n- B1 · s2 · Two.\n")]})
        self.assertEqual(unique.flow_pid("P5"), "C3.P5")                     # unique numbers: by number

    def test_a_check_and_a_use_this_on_a_repeated_id_touch_only_their_paragraph(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = _task(root, PER_PARA, _revise(_line("C2.P1.s2", 6, "It reads the whole record.")))
            rel = task.relative_to(root).as_posix()
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "check", "s": "C2.P1.s1"})[0], 200)
            self.assertIn("- C2.P1.s1 · ", (task / "draft/records/t01_note-checked.md").read_text())
            html = _html(root, task)
            self.assertIn('<li data-s="s1" data-checked="1" data-a="C2.P1.s1"', html)
            self.assertIn('<li data-s="s1" data-a="C1.P1.s1"', html)          # the other s1 is not checked
            code, res = draft_steps.card_act(root, {"task": rel, "act": "adopt", "s": "C2.P1.s2",
                                                    "original": "It reads the record.",
                                                    "expected": "It reads the whole record."})
            self.assertEqual(code, 200, res)
            text = (task / "draft/t01_note-draft-v5.0.md").read_text()
            self.assertIn("- B2 · s2 · It reads the whole record.", text)
            self.assertIn("- B2 · s2 · Reports decline.", text)               # C1.P1.s2 untouched


class FoldFadeStaleTest(unittest.TestCase):
    def test_decided_cards_fold_answered_comments_fade_open_ones_stay(self):
        draft = "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n- B2 · s2 · Two.\n"
        cards = "".join(f"### Edit · s{i} · {st}\nWhy: w\nOriginal: x\nExpected: y\nState: {st}\n\n"
                        for i, st in ((1, "accepted · 2026-11-15 10:00"), (1, "rejected"), (2, "superseded"),
                                      (2, "proposed")))
        comments = ("### Comment 1 · s1\nState: answered\n- Note · 2026-11-15 09:00: why?\n- Reply · 2026-11-15 09:30: done\n\n"
                    "### Comment 2 · s2\nState: open\n- Note · 2026-11-15 09:00: odd\n- Reply · 2026-11-15 09:30: fixed\n\n"
                    "### Comment 3 · s2\nState: open\n- Note · 2026-11-15 09:40: still?\n")
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise("", "Pass 1 · 261115 · on draft v0.1", cards), "v0.1", comments=comments)
            html = _html(Path(tmp), task)
            for st in ("accepted", "rejected", "superseded"):
                self.assertRegex(html, r'class="rv-card sx-old[^"]*"[^>]*data-state="' + st + '"')
            self.assertRegex(html, r'class="rv-card[^"]*"(?<!sx-old")[^>]*data-state="proposed"')
            self.assertNotRegex(html, r'class="rv-card sx-old[^"]*"[^>]*data-state="proposed"')
            self.assertIn('data-n="1" data-s="s1" data-faded=1', html)
            self.assertIn('data-n="2" data-s="s2" data-faded=1', html)          # a Reply after the last Note
            self.assertRegex(html, r'data-n="3" data-s="s2" data-state="open"')  # open: full

    def test_a_star_on_other_words_or_an_older_numbering_is_stale(self):
        old = ("# Note · draft v1.0\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One old.\n- B2 · s2 · Two.\n"
               "- B3 · s3 · Three.\n")
        new = "# Note · draft v1.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One new.\n- B2 · s2 · Two.\n- B3 · s3 · Four.\n"
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), new, _revise(_line("s1", 6) + _line("s2", 6) + _line("s3", 6) + _line("s4", 6),
                                                   "Pass 1 · 261115 · on draft v1.0"), "v1.1")
            (task / "draft/previous").mkdir()
            (task / "draft/previous/t01_note-draft-v1.0.md").write_text(old)
            got = {s: flag for s, _, flag in _stars(_html(Path(tmp), task))}
            # s4: the scored numbering had no s4, so its ★ is stale too
            self.assertEqual(got, {"s1": " data-stale=1", "s2": "", "s3": " data-stale=1", "s4": " data-stale=1"})


class CheckedTest(unittest.TestCase):
    def test_a_checked_sentence_gets_no_card_no_suggestion_and_no_star(self):
        draft = "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n- B2 · s2 · Two.\n"
        cards = "### Edit · s1 · x\nWhy: w\nOriginal: One.\nExpected: Uno.\nState: proposed\n\n"
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(_line("s1", 5, "Uno.") + _line("s2", 5, "Dos."),
                                                   "Pass 1 · 261115 · on draft v0.1", cards), "v0.1",
                         checked="- s1 · 2026-11-15 10:00 · One.\n")
            html = _html(Path(tmp), task)
            self.assertEqual([s for s, _, _ in _stars(html)], ["s2"])
            self.assertNotIn('data-adopt="s1"', html)
            self.assertNotIn('data-card="Edit · s1 · x"', html)
            self.assertIn('<li data-s="s1" data-checked="1"', html)
            # its words changed: the ✓ lapses and the card and ★ come back
            (task / "draft/records/t01_note-checked.md").write_text("- s1 · 2026-11-15 10:00 · One earlier.\n")
            html = _html(Path(tmp), task)
            self.assertIn('data-card="Edit · s1 · x"', html)
            self.assertIn('data-checked="stale"', html)


class BlindMeaningTest(unittest.TestCase):
    def test_a_rewrite_whose_blind_pair_says_meaning_no_is_never_written(self):
        draft = "# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One thing.\n- B2 · s2 · Two.\n"
        cards = ("### Edit · s2 · y\nWhy: w\nOriginal: Two.\nExpected: Second.\nReadable: rewrite easier · meaning: no\n"
                 "State: proposed\n\n")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = _task(root, draft, _revise("", "Pass 1 · 261115 · on draft v0.1", cards), "v0.1")
            res = root / "Project-X/paper/Paper-Demo/j31_review_v1/t02_readability_check/runs/r01_blind_ab/result"
            (res / "pairs").mkdir(parents=True)
            (res / "key.json").write_text(json.dumps({"t01_note-001": {"id": "C1.P1.S1", "A": "rewrite"},
                                                      "t01_note-002": {"id": "C1.P1.S1", "A": "original"}}))
            (res / "pairs/pairs-t01_note.md").write_text("### t01_note-001\nA: One changed thing.\nB: One thing.\n\n"
                                                         "### t01_note-002\nA: One thing.\nB: One changed thing, kept.\n")
            # the first pair said meaning: no; a later pair "kept" a rewrite that carries the same words
            (res / "unblinded.md").write_text("t01_note C1.P1.S1 | rewrite changes meaning | meaning: no | x | t01_note-001\n"
                                              "t01_note C1.P1.S1 | keep rewrite | meaning: yes | x | t01_note-002\n")
            rel = task.relative_to(root).as_posix()
            for words in ("One changed thing.", "One changed thing, kept."):
                code, out = draft_steps.card_act(root, {"task": rel, "act": "adopt", "s": "s1", "original": "One thing.",
                                                        "expected": words})
                self.assertEqual(code, 409, words)
                self.assertIn("meaning: no", out["err"])
            code, out = draft_steps.card_act(root, {"task": rel, "pass": "Pass 1 · 261115 · on draft v0.1",
                                                    "card": "Edit · s2 · y", "state": "accepted", "was": "proposed"})
            self.assertEqual(code, 409)
            self.assertIn("meaning: no", out["err"])
            self.assertIn("- B1 · s1 · One thing.\n- B2 · s2 · Two.", (task / "draft/t01_note-draft-v0.1.md").read_text())
            self.assertEqual(draft_steps.card_act(root, {"task": rel, "act": "adopt", "s": "s1", "original": "One thing.",
                                                         "expected": "One clear thing."})[0], 200)


class HistoryAndCiteTest(unittest.TestCase):
    def test_two_wordings_of_one_draft_merged_into_one_sentence_are_one_row(self):
        new = "# Note · draft v2.0\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · Care relies on accurate reports from patients, and those reports decline with cognition.\n"
        old = ("# Note · draft v1.0\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · Care relies on accurate reports from patients.\n"
               "- B2 · s2 · Those reports decline with cognition.\n")
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), new, "# t01_note · revise\n", "v2.0")
            (task / "draft/previous").mkdir()
            (task / "draft/previous/t01_note-draft-v1.0.md").write_text(old)
            from live.draft_step_revise import _sentence_history
            from live.draft_steps_common import read_draft
            rows = _sentence_history(read_draft(task), task / "draft/records/t01_note-revise.md")["s1"]
            self.assertEqual([r[2] for r in rows][0], "Care relies on accurate reports from patients. Those reports decline with cognition.")
            self.assertEqual(len(rows), 2)                                      # the merged old one, then now

    def test_citations_read_name_year_and_a_missing_key_says_not_in_bib(self):
        draft = ("# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · Care relies on reports \\cite{wolff2018}.\n"
                 "- B2 · s2 · Few are trained \\citep{TOADD, nodate}.\n")
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(""), "v0.1")
            (task / "draft/evidence/bibex").mkdir(parents=True)
            (task / "draft/evidence/bibex/t01_note.bib").write_text(
                "@article{wolff2018,\n  author = {Wolff, J. and Roter, D. and Boyd, C.},\n  year = {2018}\n}\n"
                "@article{nodate,\n  author = {Lee, A.}\n}\n")
            html = _html(Path(tmp), task)
            text = " ".join(re.findall(r'(?s)<li data-s="[^"]*".*?</li>', html))
            text = re.sub(r'(?s)<[^>]*>', " ", text)
            self.assertIn("(Wolff et al. 2018)", text)
            self.assertNotIn("\\cite", text)
            self.assertEqual(html.count(">not in Bib<"), 2)                       # TOADD, and an entry with no year

class StandsTest(unittest.TestCase):
    def test_no_step_line_over_the_text(self):
        # deleted 261115: a state line with marks that had no record read worse than none (must-check M-D16)
        draft = "# Note · draft v0.2\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n"
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(_line("s1", 9), "Pass 1 · 261115 · on draft v0.2"), "v0.2")
            self.assertNotIn("sx-stands", _html(Path(tmp), task))


    def test_only_what_needs_the_person_shows(self):
        # M-D17 (JL 261115 "remove all unnecessary things"): no file row over the text, a star only under 8, one id,
        # history only inside an opened sentence
        draft = "# Note · draft v0.2\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n- B2 · s2 · Two.\n"
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(_line("s1", 9) + _line("s2", 6), "Pass 1 · 261115 · on draft v0.2"), "v0.2")
            html = _html(Path(tmp), task)
        self.assertNotIn("space-reads", html)
        self.assertIn("rv&&!fx&&lo>=8&&!so?'<span class=\"sx-ai pass\"", html)   # 8+: a small grey number, under 8 the star
        self.assertIn(".sx-row:not(.sx-open) .sx-marks .sx-clk{display:none}", html)
        self.assertNotIn("li[data-s]>.s-no{display:none}", html)       # both numbers show (JL 261115: "where is the sNN")
        self.assertIn("li[data-s]>.s-no{grid-column:2;grid-row:2", html)   # the sNN under the 1, 2, 3

    def test_the_review_card_shows_topics_and_points_and_marks_over_the_limit(self):
        # JL 261115: "one sentence one topic, usually one or two points, at most three points"
        draft = "# Note · draft v0.2\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n- B2 · s2 · Two.\n"
        rev = _revise("- s1 · logic 9/10 · read 9/10 · ai 9/10 · link: opens, carried · topics 1, points 2: loss; clear · Fix: none\n"
                      "- s2 · logic 9/10 · read 7/10 · ai 9/10 · link: continues, carried · topics 2, points 2: loss and judging; "
                      "two topics joined by and · Fix: none\n", "Pass 1 · 261115 · on draft v0.2")
        with tempfile.TemporaryDirectory() as tmp:
            html = _html(Path(tmp), _task(Path(tmp), draft, rev, "v0.2"))
        self.assertIn(">1 topic · 2 points</span>", html)
        self.assertIn('class="lg-tp over"', html)
        self.assertIn("Two topics joined by and.", html)              # the count leaves the problem's words

    def test_the_board_keeps_its_section_name_with_display_items(self):
        # JL 261115 "the check doesn't work": a DISPLAY item's targets once overwrote the board's data-task
        draft = "# Note · draft v0.2\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One (Fig. 1).\n"
        with tempfile.TemporaryDirectory() as tmp:
            task = _task(Path(tmp), draft, _revise(_line("s1", 9), "Pass 1 · 261115 · on draft v0.2"), "v0.2")
            (task / "draft" / f"{task.name}-evidence-items.md").write_text(
                "### E01-DISPLAY-fig1 · Figure 1\n- **Target**: C1.P1.B1\n", encoding="utf-8")
            html = _html(Path(tmp), task)
        board = re.search(r'class=rv-board data-task="([^"]+)"', html).group(1)
        self.assertTrue(board.endswith(task.name), board)

    def test_a_paragraph_heading_shows_its_flow_score(self):
        # JL 261115 "why no ... per paragraph eval?": the Flow line's score rides on the flow card for the heading
        draft = "# Note · draft v0.2\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · s1 · One.\n- B2 · s2 · Two.\n"
        rev = _revise(_line("s1", 9) + _line("s2", 9) + "Flow C1.P1: logic 7/10 · topic s1 · weakest join s1 to s2\n",
                      "Pass 1 · 261115 · on draft v0.2")
        with tempfile.TemporaryDirectory() as tmp:
            html = _html(Path(tmp), _task(Path(tmp), draft, rev, "v0.2"))
        self.assertIn('data-p="C1.P1" data-plow="7"', html)
        self.assertIn("sx-pscore", html)

if __name__ == "__main__":
    unittest.main()
