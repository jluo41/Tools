"""The Board-level Design workbench: the Brief's design tasks × folders × items, one grain up from the Page."""

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
| R1 | all patients | prescription review | sms | 2 | `Design-01-all-patients-prescription-review-sms` |
| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-patients-refill-due-refill-review-ui-card` |
| R3 | young male, age 35 or under | prescription review | sms | 1 | — |
"""


def board_fixture(root: Path) -> Path:
    build_insight_board(root / "DesignWorkbench-Demo-260916-InsightBoard")
    board = root / "DesignWorkbench-Demo-260916-DesignBoard"
    board.mkdir(parents=True)
    (board / "board.md").write_text(
        "# Design Workbench Playground\nboard-kind: design-board\nreads: DesignWorkbench-Demo-260916-InsightBoard\n"
        "spine: See the entire design programme from signed input through ready candidate.\n",
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
        self.assertEqual(rows[0]["folder"], "Design-01-all-patients-prescription-review-sms")
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
            self.assertFalse(is_design_board(board.parent / "DesignWorkbench-Demo-260916-InsightBoard"))
            self.assertEqual(design_boards(Path(td)), [board])
            self.assertEqual(resolve_board(Path(td), "/DesignWorkbench-Demo-260916-DesignBoard/board.md").resolve(),
                             board.resolve())
            self.assertEqual(resolve_board(Path(td), "DesignWorkbench-Demo-260916-DesignBoard").resolve(), board.resolve())
            self.assertIsNone(resolve_board(Path(td), "/../etc/board.md"))
            # a bare link opens the only DesignBoard: the one under the root, or the root itself
            self.assertEqual(resolve_board(Path(td), "").resolve(), board.resolve())
            self.assertEqual(resolve_board(board, "").resolve(), board.resolve())

    def test_a_board_in_one_project_reads_an_insight_board_in_another(self):
        with TemporaryDirectory() as td:
            build_insight_board(Path(td) / "ProjB" / "applications" / "DesignWorkbench-Demo-260916-InsightBoard")
            project = Path(td) / "ProjA"
            board = project / "applications" / "UI-DesignBoard"
            board.mkdir(parents=True)
            (board / "board.md").write_text(
                "# UI DesignBoard\nboard-kind: design-board\n"
                "reads: ../../ProjB/applications/DesignWorkbench-Demo-260916-InsightBoard\n", encoding="utf-8")
            self.assertEqual(design_boards(project), [board])        # a Project folder served as the root
            snapshot = design_board_snapshot(board, project)
            self.assertEqual(snapshot["insight"]["status"], "bound")
            self.assertEqual(resolve_board(project, "").resolve(), board.resolve())

    def test_snapshot_stacks_folders_brief_lines_items_and_queue(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual([f["name"] for f in snap["folders"]],
                             ["Design-01-all-patients-prescription-review-sms", "Design-02-patients-refill-due-refill-review-ui-card"])
            self.assertEqual([(i["folder"], i["id"], i["state"]) for i in snap["items"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM01", "ready"),
                              ("Design-01-all-patients-prescription-review-sms", "ITEM02", "generate failed"),
                              ("Design-02-patients-refill-due-refill-review-ui-card", "ITEM01", "generated")])
            statuses = {r["id"]: r["status"] for r in snap["brief_rows"]}
            self.assertEqual(statuses["R1"], "1 ready · 1 generate failed")
            self.assertEqual(statuses["R2"], "1 generated")
            self.assertEqual(statuses["R3"], "no folder yet")
            self.assertEqual(snap["totals"], {"lines": 3, "wanted": 4, "registered": 3, "ready": 1})
            self.assertEqual(snap["unlisted"], [])
            self.assertEqual([(i["folder"], i["id"]) for i in snap["waiting"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM02"), ("Design-02-patients-refill-due-refill-review-ui-card", "ITEM01")])
            self.assertEqual(len(snap["ready"]), 1)
            self.assertEqual(snap["runs"][0]["id"], "rd04_adopt_item01")   # newest first
            self.assertEqual(snap["audit"], [])
            self.assertEqual(snap["insight"]["status"], "bound")
            self.assertEqual(snap["insight_names"], ["DesignWorkbench-Demo-260916-InsightBoard"])
            pages = snap["insight_space"][0]["pages"]
            self.assertEqual(pages[0]["name"], "FW01-send-salience.md")
            self.assertEqual([(name, item) for name, _rel, item in pages[0]["used_by"]],
                             [("Design-01-all-patients-prescription-review-sms", "ITEM01"),
                              ("Design-01-all-patients-prescription-review-sms", "ITEM02")])
            self.assertIn(">Design-01</a> <span class=mut>2 items</span>",
                          render_design_board(snap, "insight"))          # grouped per folder, linked
            self.assertTrue(pages[0]["finding"].startswith("Of thirteen arms"))
            self.assertEqual(snap["relative"], "DesignWorkbench-Demo-260916-DesignBoard")

    def test_render_has_five_spaces_and_links_down_to_the_page_level(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rendered = render_design_board(snap)
            for label in ("Goal Space", "Design Space", "Insight Space", "Run Space", "Delivery Space",
                          "Design tasks · from the Brief", "3 design tasks · 4 wanted · 3 registered · 1 ready",
                          "<th>design task</th>", "Prescription review SMS for young male, age 35 or under",
                          "no folder yet", "New Design Folder", "New design tasks", "(board default)",
                          # the href is HTML-escaped, so & is &amp; in the page
                          "/_board/design?path=%2FDesignWorkbench-Demo-260916-DesignBoard%2Fboard.md&amp;file=2-Design%2FDesign-01-all-patients-prescription-review-sms%2FDesign-01-all-patients-prescription-review-sms.md&amp;space=design&amp;item=ITEM02",
                          "1 of 1 insights currently eligible", "records check: PASS in every folder",
                          "<th>used by</th>", ">Design-01</a> <span class=mut>2 items</span>"):
                self.assertIn(label, rendered)
            for jargon in ("roster", "Roster", "handoffs signed", "check_unit", "candidate", "DS01",
                           "<b>R3</b>", "<th>line</th>"):  # a task shows by its full name, not its row id
                self.assertNotIn(jargon, rendered)
            self.assertIn("Waiting on", render_design_board(snap, "run"))
            delivery = render_design_board(snap, "delivery").split('data-space="delivery">', 1)[1].split("</section>", 1)[0]
            self.assertIn("<tr><th>item</th><th>design</th></tr>", delivery)
            self.assertNotIn("Refill review app card for patients with a refill due within 7 days", delivery)
            self.assertNotIn("adopted", delivery)
            static = render_design_board(design_board_snapshot(board, Path(td), static=True))
            self.assertNotIn("New Design Folder", static)
            self.assertNotIn("New design tasks", static)


class DesignBoardWritesTest(unittest.TestCase):
    def test_new_folder_opens_a_current_folder_and_names_it_on_the_brief(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = new_folder(board, "R3")
            self.assertEqual(out["folder"], "Design-03-young-male-age-prescription-review-sms")
            self.assertTrue(out["brief_updated"])
            page = board / "2-Design" / out["folder"] / f'{out["folder"]}.md'
            self.assertIn("folder-kind: design", page.read_text(encoding="utf-8"))
            text = page.read_text(encoding="utf-8")
            # the board checker's page contract holds from the first write (audit H8)
            self.assertIn("Which prescription review SMS design should we make for young male, age 35 or under?", text)
            self.assertRegex(text, r"(?m)^state: 🔴 OPEN · ")
            self.assertRegex(text, r"(?m)^owner: \S")
            self.assertTrue((page.parent / "outline" / f'{out["folder"]}-design-items.md').is_file())
            # Sparse native Boards still gain the promised presentation entry.
            board_text = (board / "board.md").read_text(encoding="utf-8")
            self.assertIn("## Pages\n" + page.relative_to(board).as_posix(), board_text)
            snap = design_board_snapshot(board, Path(td))
            r3 = next(r for r in snap["brief_rows"] if r["id"] == "R3")
            self.assertEqual(r3["folder"], out["folder"])
            self.assertEqual(r3["status"], "no Design Item yet")
            with self.assertRaises(ValueError):
                new_folder(board, "R3")          # already has a folder
            with self.assertRaises(ValueError):
                new_folder(board, "R9")          # not in the Brief

    def test_new_folder_registers_under_design_group_and_preserves_other_sections(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            board_md = board / "board.md"
            suffix = "\n## Pages\n### Brief\nExisting brief\n### Design\nExisting design\n\n## Links\nKeep these links.\n"
            board_md.write_text(board_md.read_text(encoding="utf-8") + suffix, encoding="utf-8")
            before = board_md.read_text(encoding="utf-8")
            out = new_folder(board, "R3")
            rel = f'2-Design/{out["folder"]}/{out["folder"]}.md'
            after = board_md.read_text(encoding="utf-8")
            self.assertEqual(after, before.replace("Existing design\n", f"Existing design\n{rel}\n"))
            with self.assertRaises(ValueError):
                new_folder(board, "R3")
            self.assertEqual(board_md.read_text(encoding="utf-8"), after)

    def test_new_folder_without_a_line_column_is_opened_once(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
            lines = []
            for line in brief.read_text(encoding="utf-8").splitlines():
                if line.startswith("|"):
                    line = "|" + "|".join(line.strip("|").split("|")[1:]) + "|"   # drop the line column
                lines.append(line)
            brief.write_text("\n".join(lines) + "\n", encoding="utf-8")
            snap = design_board_snapshot(board, Path(td))
            open_row = next(r for r in snap["brief_rows"] if not r["folder"])
            out = new_folder(board, open_row["id"])
            self.assertTrue(out["brief_updated"])
            with self.assertRaises(ValueError):
                new_folder(board, open_row["id"])            # a second click opens nothing (audit L9)
            self.assertEqual(len(list((board / "2-Design").glob("Design-*"))), 3)

    def test_add_tasks_writes_lines_opens_folders_and_names_the_insight_board(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            out = add_tasks(board, ["young male, age 35 or under", "female, age 36 to 50", ""],
                            "prescription review", "sms", 10, "DesignWorkbench-Demo-260916-InsightBoard")
            self.assertEqual(out["lines"], ["R4", "R5"])
            self.assertEqual(out["folders"], ["Design-03-young-male-age-prescription-review-sms",
                                              "Design-04-female-age-36-prescription-review-sms"])
            brief_text = (board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md").read_text(encoding="utf-8")
            self.assertIn("| insight |", brief_text)               # the column was added to the table
            rows = brief_rows(brief_text)
            self.assertEqual([r["id"] for r in rows], ["R1", "R2", "R3", "R4", "R5"])
            self.assertEqual(rows[0]["folder"], "Design-01-all-patients-prescription-review-sms")   # old lines intact
            self.assertEqual((rows[3]["audience"], rows[3]["designs"], rows[3]["insight"], rows[3]["folder"]),
                             ("young male, age 35 or under", 10, "DesignWorkbench-Demo-260916-InsightBoard",
                              "Design-03-young-male-age-prescription-review-sms"))
            snap = design_board_snapshot(board, Path(td))
            self.assertEqual(snap["totals"], {"lines": 5, "wanted": 24, "registered": 3, "ready": 1})
            # the new folder's Page level reads its own line and Insight board
            page = board / "2-Design" / out["folders"][0] / f'{out["folders"][0]}.md'
            page_snap = design_snapshot(page, Path(td))
            self.assertEqual(page_snap["goal"]["sentence"],
                             "10 prescription review SMS designs for young male, age 35 or under")
            self.assertEqual(page_snap["goal"]["insight"], "DesignWorkbench-Demo-260916-InsightBoard")
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
                             ["Design-01-all-patients-prescription-review-sms", "Design-02-patients-refill-due-refill-review-ui-card"])

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
    def test_bundle_has_one_row_per_design_with_its_brief_line(self):
        with TemporaryDirectory() as td:
            board = board_fixture(Path(td))
            snap = design_board_snapshot(board, Path(td))
            rows = bundle_rows(snap)
            self.assertEqual([(r["folder"][:9], r["item"]) for r in rows],
                             [("Design-01", "ITEM01")])   # only a passed Verify is deliverable
            row = rows[0]
            self.assertEqual((row["line"], row["venue"], row["item"]), ("R1", "sms", "ITEM01"))
            self.assertTrue(row["text"].startswith("Hi, it's Dr. {NAME}'s office."))
            self.assertEqual(len(row["sha256"]), 64)
            csv_text = bundle_csv(snap)
            self.assertTrue(csv_text.startswith("line,who,their_job,venue,folder,item,title,state,text,draft_run,sha256,render"))
            self.assertIn(",ready,", csv_text)
            self.assertIn("Download all designs · 1 · csv", render_design_board(snap, "delivery"))
            self.assertNotIn("Download all designs", render_design_board(design_board_snapshot(board, Path(td), static=True), "delivery"))
            self.assertIn("rules it implies: DO send", render_design_board(snap, "insight"))
