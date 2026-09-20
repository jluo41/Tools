"""Tests for the Board-level Insight plugin: one selected cell, five Spaces.

The fixture mirrors the real A00 board's shapes: an ASCII register grid with
one column per partition, a D page that names a run receipt, and a W page
with a signed handoff.  When the real A00 board is present it is read too,
because the parsers exist for that board's exact formatting.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from live.insightboard import (
    _append_question_row,
    _board_by_name,
    _cell_view,
    _parse_register,
    register_question,
    board_snapshot,
    groom_snapshot,
    handoff_records,
    insight_boards,
    is_insight_board,
    page_cells,
    render_insight_board,
    render_page_insight,
)

REAL = Path("/Users/jluo41/Desktop/DrFirst-SPACE")
REAL_BOARD = REAL / "examples-5-design/Project-Application-SMSDesign/applications/A00_InsightBoard-SMSR2v1-260821"


def page(folder: Path, stem: str, body: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stem}.md"
    path.write_text(body, encoding="utf-8")
    return path


def board_fixture(root: Path) -> Path:
    board = root / "Demo-InsightBoard"
    page(board / "0-MT-meta" / "MT00-meta", "MT00-meta",
         "# Meta\n\nstate: ✅ SETTLED\npage-type: meta\nowner: JL\n\n## Content\n"
         "extract  demo_dikw_input.parquet\n"
         "F      full          where: []  declared unfiltered      full.yaml   1-F-full/\n"
         "                     1,000 of 1,000 rows · 100.0000%\n"
         "B      young         age lt 40                          young.yaml  2-B-young/\n"
         "                       400 of 1,000 rows ·  40.0000%\n")
    page(board / "0-MT-meta" / "MT01-question-data", "MT01-question-data",
         "# Data questions\n\nstate: ✅ SETTLED · 1 question\npage-type: question\nquestion-rung: data\nowner: JL\n\n"
         "## Content\n\n```text\nid   question                 Gen-1   F·full   B·young\n"
         "QD1  what does the extract   Data/1  ✅ FD01  🚫 F-only\n     hold?\n```\n")
    page(board / "0-MT-meta" / "MT04-question-wisdom", "MT04-question-wisdom",
         "# Wisdom questions\n\nstate: ✅ SETTLED\npage-type: question\nquestion-rung: wisdom\nowner: JL\n\n"
         "## Content\n\n```text\nid    question           Gen-1     partition   QW1\n"
         "QW1   what to send?      Wisdom/1  F · full    ✅ FW01\n"
         "                                   B · young   🚫 F-only\n```\n")
    page(board / "1-F-full" / "FD01-extract-shape", "FD01-extract-shape",
         "# Extract shape\n\nstate: ✅ SETTLED · answers QD1\npage-type: data\nowner: JL\n\n## Opening\n\nWhat is in the extract?\n\n"
         "## Content\n\n```text\nrun receipt    results/full/runtime.yaml    status ok\n```\n\n```text\nD1   rows   1,000   counts.csv\n```\n"
         "\n### 📥 Input files\n- `../../_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/QA/1.md`\n\n## Log\n\n260901 · Created.\n")
    page(board / "1-F-full" / "FW01-what-to-send", "FW01-what-to-send",
         "# Send the one arm\n\nstate: ✅ SETTLED · answers QW1\npage-type: wisdom\nowner: JL\n\n## Opening\n\nSend `a`.\n\n"
         "## Content\n\n```text\nW1  ←  FD01 · D1   one row\n```\n\n```text\nW1   DO send `a`.        FD01 · D1\n```\n\n"
         "#### 4 · Forbidden Overreach\n\n```text\n❌ Do not say why.\n\nSERVES        QW1 · brief\n\nsigned: ✅ JL 260902\n```\n\n## Log\n\n260902 · Signed.\n")
    (board / "2-B-young").mkdir()          # registered partition, no page yet
    (board / "board.md").write_text(
        "# Demo Insight Board\n\nboard-kind: insight-board\nstore: _WorkSpace/Store/Demo-InsightBoard\n\n"
        "## Topic\n\nOne question, one extract.\n", encoding="utf-8")
    receipt = root / "_WorkSpace/Store/Demo-InsightBoard/T01_profile/01_shape/results/full/runtime.yaml"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("status: ok\ncall: full\ntask: T01_profile/01_shape\nstarted: 2026-09-01T10:00:00Z\n"
                       "duration_s: 3\ngit_sha: abc1234\n", encoding="utf-8")
    return board


class InsightBoardPluginTest(unittest.TestCase):
    def test_register_cells_and_partitions(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            self.assertTrue(is_insight_board(board))
            snap = board_snapshot(board, Path(td))
            self.assertEqual(snap["question_ids"], ["QD1", "QW1"])
            qd1 = snap["questions"][0]
            self.assertEqual(qd1["question"], "what does the extract hold?")
            self.assertEqual(qd1["cells"]["F"]["page"], "FD01")
            self.assertEqual(qd1["cells"]["B"]["raw"], "🚫 F-only")
            qw1 = snap["questions"][1]
            self.assertEqual(qw1["question"], "what to send?")
            self.assertEqual(qw1["cells"]["F"]["page"], "FW01")
            self.assertEqual(qw1["cells"]["B"]["mark"], "🚫")
            self.assertEqual([(p["id"], p["rows"]) for p in snap["partitions"]],
                             [("F", "1,000"), ("B", "400")])
            self.assertIn("demo_dikw_input.parquet", snap["context"])

    def test_receipt_ladder_gates_and_handoff(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            self.assertEqual([(r["task"], r["status"], r["git"]) for r in snap["runs"]],
                             [("T01_profile/01_shape", "ok", "abc1234")])
            view = _cell_view(snap, "QW1", "F")
            self.assertEqual([p["id"] for p in view["primary"]], ["FW01", "FD01"])
            self.assertEqual(view["receipt"]["status"], "ok")
            gates = {g["key"]: g["state"] for g in view["gates"]}
            self.assertEqual(gates["GI5"], "passed")
            self.assertEqual(gates["GI6"], "passed")
            handoffs = handoff_records(board, snap["pages"])
            self.assertEqual([(h["signed"], h["signature"]) for h in handoffs], [(True, "JL 260902")])
            refused = _cell_view(snap, "QW1", "B")
            self.assertIsNone(refused["page"])
            self.assertEqual(refused["cell"]["note"], "F-only")

    def test_render_every_space_and_short_link(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            apps = root / "examples-x" / "Project-Demo" / "applications"
            apps.mkdir(parents=True)
            board = board_fixture(apps)
            (apps / "_WorkSpace").mkdir(exist_ok=True)
            snap = board_snapshot(board, root)
            html = render_insight_board(snap, "insight", "QW1", "F")
            for space in ("scope", "run", "insight", "evidence", "check"):
                self.assertIn(f'data-space="{space}"', html)
            self.assertIn("DO send", html)                 # the answer's rows are shown
            self.assertIn("signed", html.lower())
            self.assertIn("Workflow map", html)            # Run Space: run types × Spaces (JL 260918)
            self.assertIn("I5 Wisdom", html)
            self.assertIn("Folder on this board", html)    # the map names the folder each run type lands in
            self.assertIn("Folder tree × Run type", html)  # the folder tree replaced the Folders table (260918)
            self.assertIn("0-MT-meta/MT00-meta/", html)
            self.assertNotIn('data-view="folders"', html)
            self.assertNotIn("Identity chain", html)
            self.assertEqual(insight_boards(root), [board])
            self.assertEqual(_board_by_name(root, "Demo-InsightBoard"), board)
            self.assertIsNone(_board_by_name(root, "%2Fexa"))
            groom = groom_snapshot(board, snap)
            self.assertTrue(groom["bindable_handoffs"])

    def test_register_question_appends_a_grid_row_and_a_log_line(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            qid, pids = register_question(board, "D", "how many rows per week?", "F,B",
                                          "curiosity-driven", "FD01 · D1")
            self.assertEqual((qid, pids), ("QD2", ["F", "B"]))
            snap = board_snapshot(board, Path(td))
            qd2 = next(q for q in snap["questions"] if q["id"] == "QD2")
            self.assertEqual(qd2["question"], "how many rows per week?")
            self.assertEqual(qd2["cells"]["F"]["raw"], "⬜ open")
            self.assertEqual(qd2["cells"]["B"]["raw"], "⬜ open")
            text = (board / "0-MT-meta/MT01-question-data/MT01-question-data.md").read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^\d{6} · Registered `QD2` on F, B from the Insight Board · origin: curiosity-driven · born from: FD01 · D1")
            self.assertIn("give Claude Code", render_insight_board(snap, "insight", "QD2", "B"))
            with self.assertRaises(ValueError):
                register_question(board, "W", "what to send next?", "B")   # MT04 is transposed
            with self.assertRaises(ValueError):
                register_question(board, "D", "no such column", "X")

    @unittest.skipUnless(REAL_BOARD.is_dir(), "real A00 board not present")
    def test_append_row_to_a_copy_of_the_real_mt02(self):
        with TemporaryDirectory() as td:
            src = REAL_BOARD / "0-MT-meta/MT02-question-information/MT02-question-information.md"
            copy = Path(td) / "MT02-question-information.md"
            copy.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            qid = _append_question_row(copy, "I", "does send hour change the salience lead in the young-female cut?", "C")
            self.assertEqual(qid, "QI19")
            page = {"text": copy.read_text(encoding="utf-8"), "id": "MT02", "rung": "information",
                    "page_type": "question", "path": copy}
            rows = _parse_register(page, ["F", "B", "C", "D", "E", "G", "X"])
            self.assertEqual(len(rows), 19)
            new = rows[-1]
            self.assertEqual(new["id"], "QI19")
            self.assertEqual(new["question"], "does send hour change the salience lead in the young-female cut?")
            self.assertEqual({k: v["raw"] for k, v in new["cells"].items()},
                             {"F": "·", "B": "·", "C": "⬜ open", "D": "·", "E": "·", "G": "·", "X": "·"})
            self.assertEqual(rows[-2]["id"], "QI18")                       # QI18 row untouched
            self.assertEqual(rows[-2]["cells"]["C"]["raw"], "🟡 CI16 final")

    def test_page_level_insight_surface(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = board_snapshot(board, Path(td))
            fw01 = snap["by_id"]["FW01"]
            self.assertEqual(page_cells(snap, fw01), [("QW1", "F")])
            html = render_page_insight(snap, fw01, "/Demo-InsightBoard/board.md")
            self.assertIn("QW1 × F", html)                 # the cell this page answers
            self.assertIn("DO send", html)                 # its own rows
            self.assertRegex(html, r">full-D01[ <]")       # what it cites: FD01 spelled full-D01 (JL 260918)
            self.assertIn('href="/Demo-InsightBoard/1-F-full/FW01-what-to-send/', html)  # links keep the code
            self.assertIn("<code>Demo-InsightBoard/1-F-full/FW01-what-to-send/", html)  # so do paths
            fd01 = snap["by_id"]["FD01"]
            html = render_page_insight(snap, fd01, "/Demo-InsightBoard/board.md")
            self.assertRegex(html, r">full-W01[ <]")       # cited by
            self.assertIn("open this page", render_insight_board(snap, "insight", "QW1", "F"))

    def test_ordinary_board_is_not_promoted(self):
        with TemporaryDirectory() as td:
            ordinary = Path(td) / "Demo-Board"
            ordinary.mkdir()
            (ordinary / "board.md").write_text("# Ordinary Board\n", encoding="utf-8")
            self.assertFalse(is_insight_board(ordinary))

    @unittest.skipUnless(REAL_BOARD.is_dir(), "real A00 board not present")
    def test_real_a00_board(self):
        snap = board_snapshot(REAL_BOARD, REAL)
        self.assertEqual(len(snap["question_ids"]), 40)
        q = {row["id"]: row for row in snap["questions"]}
        self.assertEqual(q["QI3"]["cells"]["B"]["raw"], "🟡 BI03 final")
        self.assertEqual(q["QI8"]["cells"]["B"]["raw"], "🚫 thin")
        self.assertEqual(q["QD4"]["cells"]["X"]["page"], "XD01")
        self.assertEqual(q["QI9"]["cells"]["E"]["raw"], "✅ EI08")
        self.assertEqual(q["QK1"]["cells"]["G"]["raw"], "🟡 GK01 final")
        self.assertEqual(q["QI14"]["cells"]["X"]["page"], "XI01")
        self.assertEqual(q["QW1"]["question"], "which messages should round 2 exploit?")
        self.assertEqual(q["QW1"]["cells"]["B"]["raw"], "✅ BW01 defers")
        self.assertEqual(q["QW2"]["cells"]["B"]["raw"], "🚫 F-only")
        self.assertTrue(all(r["found"] for r in snap["runs"]), [r["rel"] for r in snap["runs"]])
        view = _cell_view(snap, "QW1", "F")
        self.assertEqual(view["primary"][0]["id"], "FW01")
        self.assertEqual(view["primary"][-1]["level"], "data")
        self.assertEqual(view["ladder"][0]["rows"][0][0], "W1")


if __name__ == "__main__":
    unittest.main()
