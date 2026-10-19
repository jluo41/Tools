"""Folder health: each check fires on the defect it names and stays quiet otherwise."""
from pathlib import Path

from src.folder_health import FAIL, OK, WARN, folder_health

PAGE = "Sample-Page"
HEADER = """# Sample-Page · outline v1.1
outline-version: v1.1
approved: ⬜
status: working
arc: problem → answer
"""
BULLET = """
## C1 · Answer

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · The first sentence is on the Page.
  Point: [Claim] First claim
  Evidence: E01-VALUE-first · the first value
- B2 · S2 · The second sentence is also on the Page.
  Point: [Claim] Second claim
  Evidence: none · a definition
"""
ITEMS = """# Sample-Page · evidence items

### E01-VALUE-first · C1.P1.B1 · the first value
- **Label**: First
"""
FACE = """# Sample-Page

## 📚 Content

The first sentence is on the Page. <!-- realizes: C1.P1.B1 -->
The second sentence is also on the Page. <!-- realizes: C1.P1.B2 -->
"""


def make(tmp_path: Path, plan: str = HEADER + BULLET, face: str = FACE,
         items: str = ITEMS) -> Path:
    folder = tmp_path / PAGE
    (folder / "outline" / "records").mkdir(parents=True)
    (folder / f"{PAGE}.md").write_text(face, encoding="utf-8")
    (folder / "outline" / f"{PAGE}-outline-v1.1.md").write_text(plan, encoding="utf-8")
    if items is not None:
        (folder / "outline" / f"{PAGE}-evidence-items.md").write_text(items, encoding="utf-8")
    return folder


def levels(report, check):
    return [f["level"] for f in report["findings"] if f["check"] == check]


def test_consistent_folder_passes(tmp_path):
    report = folder_health(make(tmp_path))
    assert report["verdict"] == OK
    assert levels(report, "sync") == [OK]


def test_unindented_draft_line_fails(tmp_path):
    broken = BULLET.replace("  Point: [Claim] First claim",
                            "A lost continuation line.\n  Point: [Claim] First claim")
    report = folder_health(make(tmp_path, plan=HEADER + broken))
    assert report["verdict"] == FAIL
    assert FAIL in levels(report, "bullets")


def test_draft_that_differs_from_page_warns(tmp_path):
    changed = BULLET.replace("The second sentence is also on the Page.", "A revised second sentence.")
    report = folder_health(make(tmp_path, plan=HEADER + changed))
    assert WARN in levels(report, "sync")


def test_page_address_missing_from_plan_fails(tmp_path):
    face = FACE + "An old sentence. <!-- realizes: C1.P1.B9 -->\n"
    report = folder_health(make(tmp_path, face=face))
    assert FAIL in levels(report, "sync")


def test_undeclared_evidence_item_fails(tmp_path):
    report = folder_health(make(tmp_path, items=ITEMS.replace("E01-VALUE-first", "E02-VALUE-other")))
    assert FAIL in levels(report, "evidence")


def test_missing_header_lines_and_pushed_arc_warn(tmp_path):
    # a long header is fine (run names grew, 260929); `arc:` below the first `## ` is not
    long = "# Sample-Page · outline v1.1\noutline-version: v1.1\nnote: " + "x" * 1600 + "\narc: late\n"
    report = folder_health(make(tmp_path, plan=long + BULLET))
    messages = " ".join(f["message"] for f in report["findings"] if f["check"] == "header")
    assert "approved:" in messages and "status:" in messages and "arc:" not in messages
    pushed = "# Sample-Page · outline v1.1\noutline-version: v1.1\n\n## Notes\narc: late\n"
    report = folder_health(make(tmp_path / "second", plan=pushed + BULLET))
    messages = " ".join(f["message"] for f in report["findings"] if f["check"] == "header")
    assert "missing" in messages


def test_stale_pending_header_warns_when_page_is_current(tmp_path):
    header = HEADER.replace("status: working", "status: working · Page Content adoption pending")
    report = folder_health(make(tmp_path, plan=header + BULLET))
    assert WARN in levels(report, "header")


def test_live_bibliography_lane_is_not_retired(tmp_path):
    folder = make(tmp_path)
    (folder / "outline" / "evidence" / "bibex").mkdir(parents=True)
    assert levels(folder_health(folder), "layout") == []
    (folder / "outline" / "evidence" / "display").mkdir()
    assert levels(folder_health(folder), "layout") == [WARN]


def test_second_current_plan_fails(tmp_path):
    folder = make(tmp_path)
    (folder / "outline" / f"{PAGE}-outline-v1.2.md").write_text(HEADER + BULLET, encoding="utf-8")
    assert FAIL in levels(folder_health(folder), "layout")


def test_bullet_realized_by_two_sentences_is_in_sync(tmp_path):
    plan = HEADER + BULLET.replace("- B2 · S2 · The second sentence is also on the Page.",
                                   "- B2 · S2 · The second sentence is also on the Page.\n  And a third one.")
    face = FACE + "And a third one. <!-- realizes: C1.P1.B2 -->\n"
    assert levels(folder_health(make(tmp_path, plan=plan, face=face)), "sync") == [OK]


def test_earlier_shape_on_page_is_warn_while_promotion_gate_is_open(tmp_path):
    face = FACE + "An old sentence. <!-- realizes: C1.P1.B9 -->\n"
    gated = HEADER.replace("status: working", "status: working\npromotion-gate: human review")
    report = folder_health(make(tmp_path, plan=gated + BULLET, face=face))
    assert FAIL not in levels(report, "sync") and WARN in levels(report, "sync")



def test_delivery_compares_reader_text_with_the_export_snapshot(tmp_path):
    folder = make(tmp_path)
    (folder / "delivery" / "latex").mkdir(parents=True)
    (folder / "delivery" / "web").mkdir()
    snapshot = folder / "delivery" / "web" / f"{PAGE}.md"
    snapshot.write_text("state: old\n" + FACE, encoding="utf-8")
    page = folder / f"{PAGE}.md"
    page.write_text("state: new\n" + FACE, encoding="utf-8")
    assert levels(folder_health(folder), "delivery") == []
    page.write_text("state: new\n" + FACE + "A new sentence.\n", encoding="utf-8")
    assert levels(folder_health(folder), "delivery") == [WARN]


def test_untagged_continuation_line_belongs_to_the_tagged_bullet(tmp_path):
    plan = HEADER + BULLET.replace("- B2 · S2 · The second sentence is also on the Page.",
                                   "- B2 · S2 · The second sentence is also on the Page.\n  Its continuation.")
    face = FACE.replace("<!-- realizes: C1.P1.B2 -->", "<!-- realizes: C1.P1.B2 -->\nIts continuation.")
    assert levels(folder_health(make(tmp_path, plan=plan, face=face)), "sync") == [OK]




def test_display_equation_after_a_blank_line_stays_with_its_bullet(tmp_path):
    plan = HEADER + BULLET.replace("- B2 · S2 · The second sentence is also on the Page.",
                                   "- B2 · S2 · The second sentence is also on the Page.\n\n  $$\n  y = x\n  $$")
    face = FACE.replace("<!-- realizes: C1.P1.B2 -->", "<!-- realizes: C1.P1.B2 -->\n\n$$\ny = x\n$$")
    assert levels(folder_health(make(tmp_path, plan=plan, face=face)), "sync") == [OK]
