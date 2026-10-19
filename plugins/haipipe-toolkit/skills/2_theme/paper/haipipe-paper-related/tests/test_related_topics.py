"""haipipe-paper-related: the s10 map, the s11-s19 types, the check, and moving an older Board into the band."""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import related_topics as rt  # noqa: E402

TABLE = """# Paper-Demo · related work

| kind | date | item | link | feeds | group | bears on | key | venue | why here | read | source |
|---|---|---|---|---|---|---|---|---|---|---|---|
| paper | 2026 | Ada et al. 2026 · Chatbots name doctors | https://doi.org/10/a | s10 |  | Closest: chatbot audits | ★ | J1 | Asked chatbots for doctors. Many wrong. |  | https://doi.org/10/a |
| paper | 2025 | Bo 2025 · A doctor ranker | https://doi.org/10/b | s10 |  | Closest: doctor recommenders |  | J2 | Ranks doctors offline. |  | https://doi.org/10/b |
| paper | 2024 | Cy 2024 · Search engines | https://doi.org/10/c | s10 |  | Shared background: search |  | J3 | Background only. |  | https://doi.org/10/c |
"""


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = fn(*a, **k)
    return code, out.getvalue()


def board(root: Path) -> Path:
    b = root / "paper" / "Paper-Demo"
    (b / "related").mkdir(parents=True)
    (b / "board.md").write_text("# Paper-Demo\nboard-kind: paper-board\n", encoding="utf-8")
    (b / "related" / "related.md").write_text(TABLE, encoding="utf-8")
    return b


def topic(b: Path, name: str, body: str = "", tag: str = "Related work") -> Path:
    t = b / "studio" / name
    t.mkdir(parents=True)
    head = f"{name.split('-')[0]} · {name}"
    (t / f"{name}.md").write_text(f"{head}\n{'=' * len(head)}\n\n**Tags:** `{tag}`\n\n**Stage:** explore\n\n{body}",
                                  encoding="utf-8")
    (t / f"build_{name.split('-')[0]}_{name.split('-', 1)[1].replace('-', '_')}.py").write_text("print('drawn')\n")
    return t


class Scaffold(unittest.TestCase):
    def test_map_then_one_topic_per_type_in_the_band(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            rt.draw_once = lambda builder: "drawn"                  # the drawing itself is excalidraw's to test
            quiet(rt.make_map, b)
            quiet(rt.make_group, b, "chatbot audits", "chatbot-audits", offline=True)
            quiet(rt.make_group, b, "doctor recommenders", "doctor-recommenders", offline=True)
            names = sorted(p.name for p in (b / "studio").iterdir() if p.is_dir())
            self.assertEqual(names, ["s10-related-work-map", "s11-related-work-chatbot-audits",
                                     "s12-related-work-doctor-recommenders"])
            face = (b / "studio/s11-related-work-chatbot-audits/s11-related-work-chatbot-audits.md").read_text()
            self.assertIn("item: Ada et al. 2026", face)
            self.assertNotIn("Bo 2025", face)                      # another type's paper stays in its own topic
            self.assertIn("Related work", (b / "studio/_groups.txt").read_text())
            self.assertTrue((b / "studio/s10-related-work-map/build_s10_related_work_map.py").is_file())

    def test_check_names_what_is_missing_then_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            rt.draw_once = lambda builder: "drawn"
            quiet(rt.make_map, b)
            code, out = quiet(rt.check, b)
            self.assertEqual(code, 1)
            self.assertIn("Ada et al. 2026: Closest (chatbot audits) but not placed on the s10 map", out)
            self.assertIn("in no s11-s19 topic", out)
            quiet(rt.make_group, b, "chatbot audits", "chatbot-audits", offline=True)
            quiet(rt.make_group, b, "doctor recommenders", "doctor-recommenders", offline=True)
            face = b / "studio/s10-related-work-map/s10-related-work-map.md"
            face.write_text(face.read_text().replace(
                "  placements: {}", '  placements:\n    "Ada et al. 2026": {at: TR, label: a}\n'
                                    '    "Bo 2025": {at: BL, label: b}'))
            code, out = quiet(rt.check, b)
            self.assertEqual(code, 0, out)
            self.assertIn("not read from its PDF yet", out)          # unread is a note, never a failure
            self.assertIn("s12-related-work-doctor-recommenders: no ★", out)


class Table(unittest.TestCase):
    def test_a_six_column_table_gets_the_paper_columns_and_group_fills_feeds(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            six = ("| kind | date | item | link | feeds | group |\n|---|---|---|---|---|---|\n"
                   "| meeting | 2026-09-08 | Intro meeting | `meeting/x.md` | t01_introduction |  |\n")
            (b / "related" / "related.md").write_text("# related\n\n" + six)
            self.assertEqual(rt.ensure_columns(b), ["bears on", "key", "venue", "why here", "read", "source"])
            lines = (b / "related" / "related.md").read_text().splitlines()
            self.assertEqual(lines[2].count("|"), 13)
            self.assertEqual(lines[3], "| " + " | ".join(["---"] * 12) + " |")
            self.assertIn("| t01_introduction |  |  |  |", lines[4])
            self.assertEqual(rt.ensure_columns(b), [])                # twice changes nothing
            (b / "related" / "related.md").write_text(TABLE)
            rt.draw_once = lambda builder: "drawn"
            quiet(rt.make_group, b, "chatbot audits", "chatbot-audits", offline=True)
            rows = {r["item"].split(" · ")[0]: r for r in rt.rm.related_rows(b)}
            self.assertEqual(rows["Ada et al. 2026"]["feeds"], "s10, s11")
            self.assertEqual(rows["Bo 2025"]["feeds"], "s10")          # another type's row is left alone
            face = (b / "studio/s11-related-work-chatbot-audits/s11-related-work-chatbot-audits.md").read_text()
            self.assertIn("      title: Chatbots name doctors", face)
            self.assertIn("      authors: ❓ the authors from the DOI record", face)
            with self.assertRaises(SystemExit):
                quiet(rt.make_group, b, "a, b", "a-b", offline=True)

    def test_the_first_sentence_is_not_cut_at_an_abbreviation(self):
        self.assertEqual(rt.first_sentence("Of 226,999 U.S. physicians, 4% were named. Then more."),
                         "Of 226,999 U.S. physicians, 4% were named.")
        self.assertEqual(rt.first_sentence("Flags overprescribers from reviews;"), "Flags overprescribers from reviews")
        self.assertEqual(rt.first_sentence("Smith J. Doe et al. found it. Next."), "Smith J. Doe et al. found it.")


class Band(unittest.TestCase):
    def test_an_older_board_moves_into_s10_s19_with_every_mention(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            rt.draw_once = lambda builder: "drawn"
            topic(b, "s01-ideation", "See s05 and studio/s06-related-work-a/ (https://x.org/s05). Read in s06-s10.\n",
                  tag="Ideation")
            m = topic(b, "s05-related-work-map", "```yaml\nmap:\n  title: x\n```\n\ns05-D01 · one map. s10 reads B.\n")
            (m / ".s05-related-work-map.seed.json").write_text("{}")
            topic(b, "s06-related-work-a", "**Feeds:** s05 (the map).\n")
            topic(b, "s10-related-work-b", "Read in s10; build_s10_related_work_b.py.\n")
            run = b / "runs" / "run-draw-s05"
            run.mkdir(parents=True)
            (run / "run.yaml").write_text("target: s05\n")
            (run / "run-draw-s05.md").write_text("# run-draw-s05\ntarget: s05\n")
            quiet(rt.band, b, apply=True)
            studio = b / "studio"
            self.assertEqual(sorted(p.name for p in studio.iterdir() if p.is_dir()),
                             ["s01-ideation", "s10-related-work-map", "s11-related-work-a", "s12-related-work-b"])
            ideation = (studio / "s01-ideation/s01-ideation.md").read_text()
            self.assertIn("See s10 and studio/s11-related-work-a/ (https://x.org/s05). Read in s11-s12.", ideation)
            mp = (studio / "s10-related-work-map/s10-related-work-map.md").read_text()
            self.assertIn("renamed-from: s05-related-work-map", mp.splitlines()[2])
            self.assertIn("s10-D01 · one map. s12 reads B.", mp)
            self.assertTrue((studio / "s10-related-work-map/.s10-related-work-map.seed.json").is_file())
            self.assertTrue((studio / "s12-related-work-b/build_s12_related_work_b.py").is_file())
            self.assertIn("build_s12_related_work_b.py", (studio / "s12-related-work-b/s12-related-work-b.md").read_text())
            self.assertEqual((b / "runs/run-draw-s10/run.yaml").read_text(), "target: s10\n")
            self.assertTrue((b / "runs/run-draw-s10/run-draw-s10.md").is_file())
            code, out = quiet(rt.band, b)
            self.assertIn("already in s10-s19", out)

    def test_a_dry_run_changes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            topic(b, "s05-related-work-map", "```yaml\nmap:\n  title: x\n```\n")
            code, out = quiet(rt.band, b)
            self.assertIn("s05-related-work-map  →  s10-related-work-map", out)
            self.assertTrue((b / "studio/s05-related-work-map").is_dir())

    def test_a_number_held_by_another_topic_stops_the_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = board(Path(tmp))
            topic(b, "s05-related-work-map", "```yaml\nmap:\n  title: x\n```\n")
            topic(b, "s10-figures", tag="Figures")
            with self.assertRaises(SystemExit):
                quiet(rt.band, b, apply=True)


if __name__ == "__main__":
    unittest.main()
