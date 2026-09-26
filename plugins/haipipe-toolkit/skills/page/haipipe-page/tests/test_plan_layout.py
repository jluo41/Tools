"""Three-section Draft Markdown: readers see one plan, writers keep three sections."""
from pathlib import Path

from src.outline_version import latest_outline, plan_dir, retire_superseded
from src.plan_layout import (from_canonical, is_sectioned, scratch_notes, to_canonical,
                             to_sectioned, write_scratch)
from src.plan_shape import canonical_plan, draft_first_plan, iter_plan_bullets
from src.run_folders import folder_for, space_of, ticket_dir, ticket_rel

SECTIONED = """# Sample-Page · draft v1.1
draft-version: v1.1
approved: ⬜
arc: problem → answer

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · State the answer · S1 to S2

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · [Claim] First claim
  Note: a note
  Evidence: none · a definition
- B2 · S2 · [Claim] Second claim
  Evidence: none · a definition

## 2 · Scratch · What to write here

### C1.P1 · State the answer · S1 to S2

## 3 · Draft · Reading and Revise

The sentences themselves.

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · The first sentence is on the Page.
- B2 · S2 · The second sentence.
  $$
  y = x
  $$
"""
DRAFT_FIRST = """# Sample-Page · outline v1.1
outline-version: v1.1

## C1 · Answer

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · The first sentence is on the Page.
  Point: [Claim] First claim
  Note: a note
  Evidence: none · a definition
- B2 · S2 · The second sentence.
  $$
  y = x
  $$
  Point: [Claim] Second claim
  Evidence: none · a definition
"""


def rows(text):
    return [(b["address"], b["draft"], b["head"], tuple(b["continuation"])) for b in iter_plan_bullets(text)]


def test_readers_see_the_same_bullets_as_the_draft_first_plan():
    assert is_sectioned(SECTIONED) and not is_sectioned(DRAFT_FIRST)
    assert rows(SECTIONED) == rows(DRAFT_FIRST)
    assert "## C1 · Answer" in to_canonical(SECTIONED)


def test_both_canonical_shapes_write_back_byte_for_byte():
    assert from_canonical(SECTIONED, to_canonical(SECTIONED)) == SECTIONED
    assert from_canonical(SECTIONED, canonical_plan(SECTIONED)) == SECTIONED
    assert draft_first_plan(SECTIONED) == SECTIONED


def test_an_edited_draft_lands_in_section_3_and_keeps_overview_and_scratch():
    edited = to_canonical(SECTIONED).replace("The first sentence is on the Page.", "A revised first sentence.")
    out = from_canonical(SECTIONED, edited)
    assert "- B1 · S1 · A revised first sentence." in out.split("## 3 ·")[1]
    assert "### Structure Overview" in out and "## 2 · Scratch" in out
    assert out.count("[Claim] First claim") == 1


def test_migration_lays_a_draft_first_plan_out_in_three_sections():
    out = to_sectioned(DRAFT_FIRST)
    assert is_sectioned(out) and rows(out) == rows(DRAFT_FIRST)


def test_scratch_notes_are_written_under_their_paragraph_and_read_back():
    out = write_scratch(SECTIONED, "C1.P1", "Link the claim to the design.",
                        run="rp-scratch-01_C1.P1", scope="paragraph", status="open")
    notes = scratch_notes(out)
    assert notes == [{"run": "rp-scratch-01_C1.P1", "target": "C1.P1", "notes": "Link the claim to the design.",
                      "summary": "", "scope": "paragraph", "status": "open"}]
    again = write_scratch(out, "C1.P1", "Shorter.", run="rp-scratch-01_C1.P1", scope="paragraph",
                          status="closed", summary="One line.")
    assert scratch_notes(again)[0]["notes"] == "Shorter." and "> Summary: One line." in again
    assert rows(again) == rows(SECTIONED)


def test_hand_written_scratch_without_a_marker_is_still_read():
    text = SECTIONED.replace("## 2 · Scratch · What to write here\n\n### C1.P1 · State the answer · S1 to S2\n",
                             "## 2 · Scratch · What to write here\n\n### C1.P1 · State the answer · S1 to S2\nmy own note\n")
    assert scratch_notes(text)[0]["notes"] == "my own note" and scratch_notes(text)[0]["run"] == ""


def test_plan_dir_and_draft_named_versions(tmp_path: Path):
    page = tmp_path / "Sample-Page"
    (page / "outline").mkdir(parents=True)
    assert plan_dir(page) == page / "outline"
    (page / "draft").mkdir()
    for name in ("Sample-Page-outline-v1.0.md", "Sample-Page-draft-v1.1.md"):
        (page / "draft" / name).write_text("x", encoding="utf-8")
    assert plan_dir(page) == page / "draft"
    assert latest_outline(page / "draft", "Sample-Page").name == "Sample-Page-draft-v1.1.md"
    retire_superseded(page / "draft", "Sample-Page")
    assert (page / "draft" / "previous" / "Sample-Page-outline-v1.0.md").is_file()


def test_run_folders_by_space(tmp_path: Path):
    assert folder_for("rp-para-15_P02") == "draft-manual-run"
    assert folder_for("rp-embed-01_P02") == "draft-auto-run"
    assert folder_for("re-cite-02_cite-x") == "evidence-run"
    assert folder_for("rd01_latex") == "delivery-run"
    assert ticket_dir(tmp_path, "rp-para-15_P02") == tmp_path / "runs"
    (tmp_path / "runs" / "draft-manual-run").mkdir(parents=True)
    assert ticket_rel(tmp_path, "rp-para-15_P02") == "runs/draft-manual-run/rp-para-15_P02.md"
    assert space_of("runs/evidence-run/pj02t40r01_x.sh") == "evidence"
    assert space_of("runs/rd02_word.md") == "delivery"


def test_a_renamed_paragraph_keeps_one_name_in_every_section():
    text = write_scratch(SECTIONED, "C1.P1", "a note", run="rp-scratch-01_C1.P1", scope="paragraph", status="open")
    renamed = to_canonical(text).replace("### C1.P1 · State the answer", "### C1.P1 · Give the answer")
    out = from_canonical(text, renamed)
    assert out.count("C1.P1 · Give the answer") == 4 and "State the answer" not in out
    assert scratch_notes(out)[0]["notes"] == "a note"


def test_draft_layout_moves_a_draft_first_page_to_the_three_section_layout(tmp_path: Path):
    from src.draft_migration import draft_layout
    page = tmp_path / "Sample-Page"
    (page / "outline").mkdir(parents=True)
    (page / "Sample-Page.md").write_text("# Sample-Page\n", encoding="utf-8")
    (page / "outline" / "Sample-Page-outline-v1.1.md").write_text(DRAFT_FIRST, encoding="utf-8")
    (page / "runs").mkdir()
    (page / "runs" / "rp-para-01_P01.md").write_text("result: results/rp-para-01_P01\n", encoding="utf-8")
    (page / "runs" / "rd01_latex.md").write_text("see runs/rp-para-01_P01.md\n", encoding="utf-8")
    report = draft_layout(page, sort_runs=True)
    assert report["renamed"] == "outline/ → draft/" and not (page / "outline").exists()
    new = page / "draft" / "Sample-Page-draft-v1.2.md"
    assert new.is_file() and (page / "draft" / "previous" / "Sample-Page-outline-v1.1.md").is_file()
    assert is_sectioned(new.read_text()) and rows(new.read_text()) == rows(DRAFT_FIRST)
    assert (page / "runs" / "draft-manual-run" / "rp-para-01_P01.md").is_file()
    assert "runs/draft-manual-run/rp-para-01_P01.md" in (page / "runs" / "delivery-run" / "rd01_latex.md").read_text()
    assert draft_layout(page)["plan"].endswith("already three sections")


def test_generated_overview_gives_each_paragraph_a_title_line_and_a_span_line():
    out = to_sectioned(DRAFT_FIRST)
    overview = out.split("### Structure Overview")[1].split("## 2 ·")[0]
    assert "- C1 · Answer\n- C1.P1 · State the answer\n  → S1 to S2" in overview


def test_overview_entries_are_read_normalized_and_replaced():
    from src.plan_layout import normalize_overview, overview_lines, set_overview
    assert overview_lines(SECTIONED) == ["- C1 · Answer", "- C1.P1 · State the answer · S1 to S2"]
    entries = normalize_overview("C1 · Answer\nC1.P1 · State the answer\n→ S1 to S2 · the job\n→ C1.P2: next?")
    assert entries == ["- C1 · Answer", "- C1.P1 · State the answer", "  → S1 to S2 · the job", "  → C1.P2: next?"]
    out = set_overview(SECTIONED, entries)
    assert overview_lines(out) == entries and rows(out) == rows(SECTIONED)
