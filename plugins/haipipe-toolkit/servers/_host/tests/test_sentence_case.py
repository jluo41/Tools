"""A draft sentence id reads in either case (S8 is s8) and is written as s8: an old draft whose records all say S
shows the same Draft Lab as one written with s (every ✓ held, every ★, the evidence marks, the comments)."""
from __future__ import annotations

import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import task_draft  # noqa: E402
from live.sentence_id import SENT, label, sid  # noqa: E402


DRAFT = ("# Note · draft v0.1\n\n## 3 · Draft\n\n### C1.P1 · Why\n- B1 · {S}1 · The problem grows.\n"
         "- B2 · {S}2 · It costs money.\n- B3 · {S}3 · Nobody pays it.\n")
CHECKED = ("# t01_note · checked sentences\n\n- {S}1 · 2026-11-14 10:00 · The problem grows.\n"
           "- {S}3 · 2026-11-14 10:01 · Nobody pays it.\n")
REVISE = ("# t01_note · Revise cards\n\n## Pass 1 · 261114 · on draft v0.1\n\n"
          "### Edit · {S}2 · the cost\n\nWhy: your comment\nAnswers: Comment 1\nOriginal: It costs money.\n"
          "Expected: It costs $5 a year.\nState: proposed\n\n"
          "### Revise review report\nVerdict: one join is weak.\nSentences:\n"
          "- {S}1 · logic 9/10 · read 9/10 · link: opens the paragraph, carried · none · Fix: none\n"
          "- {S}2 · logic 6/10 · read 7/10 · link: cause, weak · the cost is vague · Fix: It costs $5 a year.\n"
          "- {S}3 · logic 8/10 · read 8/10 · link: contrast, carried · none · Fix: none\n")
COMMENTS = ("# t01_note · comments\n\n### Comment 1 · C1.P1.{S}2\nQuote: costs\nState: open\n"
            "- Note · 2026-11-14 10:02: how much?\n")
CARDS = ("evidence:\n- kind: value\n  source: ''\n  title: the cost\n  items:\n"
         "  - for: [{S}2]\n    anchor: [money]\n    need: the yearly cost\n")


def _task(root: Path, S: str) -> Path:
    task = root / "Project-X/work/b01_topic/j01_job/t01_note"
    rec = task / "draft" / "records"
    rec.mkdir(parents=True)
    (task / "evidence").mkdir()
    (task.parents[1] / "board.md").write_text("# Topic\n")
    (task / "t01_note.md").write_text("# t01_note · Note\n\nfolder-kind: task\ntask-type: draft\n")
    (task / "draft" / "t01_note-draft-v0.1.md").write_text(DRAFT.format(S=S))
    (rec / "t01_note-checked.md").write_text(CHECKED.format(S=S))
    (rec / "t01_note-revise.md").write_text(REVISE.format(S=S))
    (rec / "t01_note-comments.md").write_text(COMMENTS.format(S=S))
    (task / "evidence" / "cards.yaml").write_text(CARDS.format(S=S))
    return task


def _face(html: str) -> dict:
    """What the reader sees, without the record's own words: each sentence's ✓, the ★ scores, the cards' sentences,
    the evidence marks."""
    return {"li": re.findall(r'<li data-s="([^"]*)"( data-checked="[^"]*")?', html),
            "stars": re.findall(r"class=lg-q>★([\d.]+)", html),
            "cards": sorted(re.findall(r'class="rv-card[^"]*" data-(?:n="\d+" data-)?s="([^"]*)"', html)),
            "marks": len(re.findall(r"<mark", html)),
            "notes": re.findall(r'data-n="(\d+)" data-s="([^"]*)"', html)}


class SentenceCaseTest(unittest.TestCase):
    def test_sid_lowers_only_the_sentence_segment(self):
        self.assertEqual(sid("S8"), "s8")
        self.assertEqual(sid("s3b"), "s3b")
        self.assertEqual(sid("C1.P2.S8"), "C1.P2.s8")
        self.assertEqual(sid("C1.P2"), "C1.P2")
        self.assertEqual(sid("B3"), "B3")
        self.assertEqual(sid("S1 S2a"), "s1 s2a")
        self.assertEqual(sid(None), "")
        self.assertEqual(label(8), "s8")
        self.assertEqual(label("S4", "a"), "s4a")
        self.assertTrue(re.fullmatch(SENT, "S12b") and re.fullmatch(SENT, "s12b"))

    def test_an_S_draft_and_an_s_draft_show_the_same_draft_lab(self):
        faces = {}
        for S in ("S", "s"):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                task = _task(root, S)
                html = task_draft.draft_task_spaces(task, root, "5 · Revise")["Work Details"].html
                faces[S] = _face(html)
                # every ✓ holds (never the lapsed "stale"), each sentence its own row, written s
                self.assertIn(('s1', ' data-checked="1"'), faces[S]["li"], S)
                self.assertIn(('s3', ' data-checked="1"'), faces[S]["li"], S)
                self.assertNotIn('data-checked="stale"', html, S)
                # a ★ on every scored sentence the person has not checked: a checked one shows its ✓ only (M-D06)
                self.assertEqual(len(faces[S]["stars"]), 1, S)
                self.assertIn("s2", " ".join(faces[S]["cards"]), S)     # the Edit card on its sentence
                self.assertGreater(faces[S]["marks"], 0, S)             # the evidence anchor boxed
                self.assertEqual(faces[S]["notes"], [("1", "C1.P1.s2")], S)
                self.assertNotRegex(html, r'data-s="[^"]*S\d', S)
        self.assertEqual(faces["S"], faces["s"])

    def test_an_S_record_is_acted_on_from_an_s_page(self):
        # the page posts s ids; the record on disk says S: the card, the check and the comment are still found
        from live import draft_steps
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            task = _task(root, "S")
            rel = task.relative_to(root).as_posix()
            rec = task / "draft" / "records"
            code, res = draft_steps.card_act(root, {"task": rel, "pass": "Pass 1 · 261114 · on draft v0.1",
                                                    "card": "Edit · s2 · the cost", "state": "accepted",
                                                    "was": "proposed"})
            self.assertEqual(code, 200, res)
            self.assertIn("- B2 · S2 · It costs $5 a year.", (task / "draft" / "t01_note-draft-v0.1.md").read_text())
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "uncheck", "s": "C1.P1.s1"})[0], 200)
            self.assertNotIn("1 · 2026-11-14 10:00", (rec / "t01_note-checked.md").read_text())
            self.assertEqual(draft_steps.note_act(root, {"task": rel, "act": "check", "s": "C1.P1.s3"})[0], 200)
            checked = (rec / "t01_note-checked.md").read_text()
            self.assertEqual(checked.count("· Nobody pays it."), 1)                # the old S3 line replaced
            self.assertIn("- s3 · ", checked)
            code, res = draft_steps.card_act(root, {"task": rel, "act": "adopt", "s": "s3", "original": "Nobody pays it.",
                                                    "expected": "Nobody pays it yet."})
            self.assertEqual(code, 200, res)
            self.assertIn("### Edit · s3 · the reviewer's suggestion", (rec / "t01_note-revise.md").read_text())


if __name__ == "__main__":
    unittest.main()
