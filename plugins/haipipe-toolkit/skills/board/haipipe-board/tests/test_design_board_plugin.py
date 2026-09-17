"""The Board-level Design plugin: the Brief's design tasks × folders × items, one grain up from the Page."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from live.design import brief_rows, design_snapshot
from live.designboard import (
    add_tasks,
    bundle_csv,
    bundle_rows,
    design_board_snapshot,
    design_boards,
    is_design_board,
    new_folder,
    render_design_board,
    resolve_board,
)
from tests.fixture_design_v2 import build_design_folder, build_insight_board, demo_specs

BRIEF = """# Design Brief
folder-kind: brief

## Opening

Three lines; the third has no folder yet.

### 8 · What to design

| line | audience | job | venue | designs | folder |
|---|---|---|---|---|---|
| R1 | full SMSR2 population, unconditioned | prescription review | sms | 2 | `Design-01-patient-confirm-sms` |
| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-refill-reminder-ui` |
| R3 | young male, age 35 or under | prescription review | sms | 1 | — |
"""


def board_fixture(root: Path) -> Path:
    build_insight_board(root / "DesignPlugin-Demo-260916-InsightBoard")
    board = root / "DesignPlugin-Demo-260916-DesignBoard"
    board.mkdir(parents=True)
    (board / "board.md").write_text(
        "# Design Plugin Playground\nboard-kind: design-board\nreads: DesignPlugin-Demo-260916-InsightBoard\n"
        "spine: See the entire design programme from signed input through adopted candidate.\n",
        encoding="utf-8")
    brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
    brief.parent.mkdir(parents=True)
    brief.write_text(BRIEF, encoding="utf-8")
    for stem, spec in demo_specs().items():
        build_design_folder(board / "2-Design" / stem, stem, spec["title"], spec["opening"], spec["specs"])
    return board


class BriefTest(unittest.TestCase):
    def test_brief_lines_are_matched_by_header_word(self):
        rows = brief_rows(BRIEF)
        self.assertEqual([r["id"] for r in rows], ["R1", "R2", "R3"])
        self.assertEqual(rows[0]["folder"], "Design-01-patient-confirm-sms")
        self.assertEqual(rows[0]["designs"], 2)
        self.assertEqual(rows[0]["insight"], "")            # no column: the board's reads: applies
        self.assertEqual(rows[2]["folder"], "")
        self.assertEqual(rows[2]["venue"], "sms")
        self.assertEqual(brief_rows("# Brief\n\nno table here\n"), [])
        with_insight = BRIEF.replace("| designs | folder |", "| designs | insight | folder |") \
            .replace("|---|---|---|---|---|---|", "|---|---|---|---|---|---|---|") \
            .replace("| 2 | `Design-01", "| 2 | `Other-InsightBoard` | `Design-01") \
            .replace("| 1 | `Design-02", "| 1 |  | `Design-02").replace("| 1 | — |", "| 1 |  | — |")
        rows = brief_rows(with_insight)
        self.assertEqual(rows[0]["insight"], "Other-InsightBoard")
        self.assertEqual(rows[1]["insight"], "")


class DesignBoardSnapshotTest(unittest.TestCase):
    def test_identity_and_resolution(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            self.assertTrue(is_design_board(board))
            self.assertFalse(is_design_board(board.parent / "DesignPlugin-Demo-260916-InsightBoard"))
            self.assertEqual(design_boards(Path(td)), [board])
            self.assertEqual(resolve_board(Path(td), "/DesignPlugin-Demo-260916-DesignBoard/board.md").resolve(),
                             board.resolve())
            self.assertEqual(resolve_board(Path(td), "DesignPlugin-Demo-260916-DesignBoard").resolve(), board.resolve())
            self.assertIsNone(resolve_board(Path(td), "/../etc/board.md"))
            # a bare link opens the only DesignBoard: the one under the root, or the root itself
            self.assertEqual(resolve_board(Path(td), "").resolve(), board.resolve())
            self.assertEqual(resolve_board(board, "").resolve(), board.resolve())

    def test_snapshot_stacks_folders_brief_lines_items_and_queue(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual([f["name"] for f in snap["folders"]],
                             ["Design-01-patient-confirm-sms", "Design-02-refill-reminder-ui"])
            self.assertEqual([(i["folder"], i["id"], i["state"]) for i in snap["items"]],
                             [("Design-01-patient-confirm-sms", "ITEM01", "adopted"),
                              ("Design-01-patient-confirm-sms", "ITEM02", "generate failed"),
                              ("Design-02-refill-reminder-ui", "ITEM01", "generated")])
            statuses = {r["id"]: r["status"] for r in snap["brief_rows"]}
            self.assertEqual(statuses["R1"], "1 adopted · 1 generate failed")
            self.assertEqual(statuses["R2"], "1 generated")
            self.assertEqual(statuses["R3"], "no folder yet")
            self.assertEqual(snap["totals"], {"lines": 3, "wanted": 4, "registered": 3, "adopted": 1})
            self.assertEqual(snap["unlisted"], [])
            self.assertEqual([(i["folder"], i["id"]) for i in snap["waiting"]],
                             [("Design-01-patient-confirm-sms", "ITEM02"), ("Design-02-refill-reminder-ui", "ITEM01")])
            self.assertEqual(len(snap["adopted"]), 1)
            self.assertEqual(snap["runs"][0]["id"], "rd04_adopt_item01")   # newest first
            self.assertEqual(snap["audit"], [])
            self.assertEqual(snap["insight"]["status"], "bound")
            self.assertEqual(snap["insight_names"], ["DesignPlugin-Demo-260916-InsightBoard"])
            pages = snap["insight_space"][0]["pages"]
            self.assertEqual(pages[0]["name"], "FW01-send-salience.md")
            self.assertEqual(pages[0]["used_by"], ["Design-01-patient-confirm-sms ITEM01",
                                                   "Design-01-patient-confirm-sms ITEM02"])
            self.assertTrue(pages[0]["finding"].startswith("Of thirteen arms"))
            self.assertEqual(snap["relative"], "DesignPlugin-Demo-260916-DesignBoard")

    def test_render_has_five_spaces_and_links_down_to_the_page_level(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rendered = render_design_board(snap)
            for label in ("Goal Space", "Design Space", "Insight Space", "Run Space", "Delivery Space",
                          "Design tasks · from the Brief", "3 design task(s) · 4 wanted · 3 registered · 1 adopted",
                          "R3", "no folder yet", "New Design Folder", "New design tasks", "(board default)",
                          # the href is HTML-escaped, so & is &amp; in the page
                          "/_board/design?path=%2FDesignPlugin-Demo-260916-DesignBoard%2Fboard.md&amp;file=2-Design%2FDesign-01-patient-confirm-sms%2FDesign-01-patient-confirm-sms.md&amp;space=design&amp;item=ITEM02",
                          "1 of 1 insights signed", "records check: PASS in every folder",
                          "<th>used by</th>", "Design-01-patient-confirm-sms ITEM01 · Design-01-patient-confirm-sms ITEM02"):
                self.assertIn(label, rendered)
            for jargon in ("roster", "Roster", "handoffs signed", "check_unit", "candidate", "DS01"):
                self.assertNotIn(jargon, rendered)
            self.assertIn("Waiting on", render_design_board(snap, "run"))
            self.assertIn("✅ adopted · JL", render_design_board(snap, "delivery"))
            static = render_design_board(design_board_snapshot(board, Path(td), static=True))
            self.assertNotIn("New Design Folder", static)
            self.assertNotIn("New design tasks", static)


class DesignBoardWritesTest(unittest.TestCase):
    def test_new_folder_opens_a_current_folder_and_names_it_on_the_brief(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = new_folder(board, "R3")
            self.assertEqual(out["folder"], "Design-03-young-male-prescription-review-sms")
            self.assertTrue(out["brief_updated"])
            page = board / "2-Design" / out["folder"] / f'{out["folder"]}.md'
            self.assertIn("folder-kind: design", page.read_text(encoding="utf-8"))
            self.assertIn("The Brief asks for 1 design.", page.read_text(encoding="utf-8"))
            self.assertTrue((page.parent / "outline" / f'{out["folder"]}-design-items.md').is_file())
            snap = design_board_snapshot(board, Path(td))
            r3 = next(r for r in snap["brief_rows"] if r["id"] == "R3")
            self.assertEqual(r3["folder"], out["folder"])
            self.assertEqual(r3["status"], "no Design Item yet")
            with self.assertRaises(ValueError):
                new_folder(board, "R3")          # already has a folder
            with self.assertRaises(ValueError):
                new_folder(board, "R9")          # not in the Brief

    def test_add_tasks_writes_lines_opens_folders_and_names_the_insight_board(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = add_tasks(board, ["young male, age 35 or under", "female, age 36 to 50", ""],
                            "prescription review", "sms", 10, "DesignPlugin-Demo-260916-InsightBoard")
            self.assertEqual(out["lines"], ["R4", "R5"])
            self.assertEqual(out["folders"], ["Design-03-young-male-prescription-review-sms",
                                              "Design-04-female-age-prescription-review-sms"])
            brief_text = (board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8")
            self.assertIn("| insight |", brief_text)               # the column was added to the table
            rows = brief_rows(brief_text)
            self.assertEqual([r["id"] for r in rows], ["R1", "R2", "R3", "R4", "R5"])
            self.assertEqual(rows[0]["folder"], "Design-01-patient-confirm-sms")   # old lines intact
            self.assertEqual((rows[3]["audience"], rows[3]["designs"], rows[3]["insight"], rows[3]["folder"]),
                             ("young male, age 35 or under", 10, "DesignPlugin-Demo-260916-InsightBoard",
                              "Design-03-young-male-prescription-review-sms"))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual(snap["totals"], {"lines": 5, "wanted": 24, "registered": 3, "adopted": 1})
            # the new folder's Page level reads its own line and Insight board
            page = board / "2-Design" / out["folders"][0] / f'{out["folders"][0]}.md'
            page_snap = design_snapshot(page, Path(td))
            self.assertEqual(page_snap["goal"]["sentence"],
                             "10 sms designs for young male, age 35 or under, prescription review")
            self.assertEqual(page_snap["goal"]["insight"], "DesignPlugin-Demo-260916-InsightBoard")
            self.assertEqual(page_snap["insight"]["status"], "bound")

    def test_add_tasks_refusals_write_nothing(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            before = (board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8")
            for args in (([""], "job", "sms", 10, ""), (["who"], "", "sms", 10, ""),
                         (["who"], "job", "", 10, ""), (["who"], "job", "sms", 0, ""),
                         (["who"], "job", "sms", 10, "No-Such-Board")):
                with self.assertRaises(ValueError):
                    add_tasks(board, *args)
            self.assertEqual((board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8"), before)
            self.assertEqual(sorted(p.name for p in (board / "2-Design").iterdir()),
                             ["Design-01-patient-confirm-sms", "Design-02-refill-reminder-ui"])

    def test_add_tasks_without_opening_folders_and_without_a_table(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
            brief.write_text("# Design Brief\nfolder-kind: brief\n\n## Opening\n\nNo list yet.\n", encoding="utf-8")
            out = add_tasks(board, ["patients over 65"], "refill review", "email", 3, "", open_folders=False)
            self.assertEqual(out["lines"], ["R1"])
            self.assertEqual(out["folders"], [])
            rows = brief_rows(brief.read_text(encoding="utf-8"))
            self.assertEqual((rows[0]["id"], rows[0]["venue"], rows[0]["designs"], rows[0]["folder"]),
                             ("R1", "email", 3, ""))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual(next(r["status"] for r in snap["brief_rows"] if r["id"] == "R1"), "no folder yet")
            self.assertEqual(len(snap["unlisted"]), 2)      # the two demo folders are no longer listed


if __name__ == "__main__":
    unittest.main()


class BundleTest(unittest.TestCase):
    def test_bundle_has_one_row_per_adopted_draft_with_its_brief_line(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rows = bundle_rows(snap)
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual((row["line"], row["venue"], row["folder"], row["item"], row["adopted_by"]),
                             ("R1", "sms", "Design-01-patient-confirm-sms", "ITEM01", "JL"))
            self.assertTrue(row["text"].startswith("Hi, it's Dr. {NAME}'s office."))
            self.assertEqual(len(row["sha256"]), 64)
            csv_text = bundle_csv(snap)
            self.assertTrue(csv_text.startswith("line,who,their_job,venue,folder,item,title,text,sha256"))
            self.assertEqual(csv_text.count("\n"), 2)                # header + one row
            self.assertIn("Download the bundle · 1 adopted message(s) · csv", render_design_board(snap, "delivery"))
            self.assertNotIn("Download the bundle", render_design_board(design_board_snapshot(board, Path(td), static=True), "delivery"))
            self.assertIn("rules it implies: DO send", render_design_board(snap, "insight"))
