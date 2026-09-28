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


def test_evidence_markdown_groups_items_by_kind_and_keeps_every_block():
    from src.draft_migration import _item_blocks, group_evidence
    flat = ("# P · evidence items\nplan: v1\n\n### E01-VALUE-a · C1.P1.B1 · a\n- **Target**: C1.P1.B1\n\n"
            "### E02-CITE-b · C1.P1.B2 · b\n- **Target**: C1.P1.B2\n\n#### E03-CITE-c · retired\n- old\n\n"
            "## Retired or moved\n\n### E09-CITE-z · gone\n")
    grouped = group_evidence(flat)
    assert grouped.index("## Citations") < grouped.index("### E02") < grouped.index("#### E03")
    assert grouped.index("## Values") < grouped.index("### E01") < grouped.index("## Retired or moved")
    assert "## Displays" in grouped and grouped.startswith("# P · evidence items\nplan: v1\n")
    assert _item_blocks(grouped) == _item_blocks(flat)
    assert group_evidence(grouped) == grouped


def test_check_page_folder_reports_behind_then_latest(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder, pages_in
    page = tmp_path / "Board" / "Sample-Page"
    (page / "outline").mkdir(parents=True)
    (page / "Sample-Page.md").write_text("# Sample-Page\n", encoding="utf-8")
    (page / "outline" / "Sample-Page-outline-v1.1.md").write_text(DRAFT_FIRST, encoding="utf-8")
    (page / "runs").mkdir()
    (page / "runs" / "rp-para-01_P01.md").write_text("x\n", encoding="utf-8")
    (page / "runs" / "r01_task_run.sh").write_text("x\n", encoding="utf-8")
    before = check_page_folder(page)
    behind = {r["rule"] for r in before["rules"] if r["state"] == "BEHIND"}
    assert before["verdict"] == "behind" and "plan folder is draft/" in behind
    assert "runs/ sorted by Space" in behind and "plan in three sections" in behind
    draft_layout(page, sort_runs=True)
    after = check_page_folder(page)
    assert after["verdict"] == "latest", [r for r in after["rules"] if r["state"] == "BEHIND"]
    assert (page / "runs" / "r01_task_run.sh").is_file()  # a Task Run stays flat
    assert pages_in(tmp_path / "Board") == [page.resolve()]


def test_draft_layout_on_a_task_group_moves_every_page_and_the_paths_around_them(tmp_path: Path):
    from src.draft_migration import draft_layout_tree
    from src.layout_check import check_page_folder
    group = tmp_path / "tasks" / "b01_x" / "j01_y"
    task = group / "t01_first_task"
    (task / "outline" / "records").mkdir(parents=True)
    (task / "outline" / "records" / "t01_first_task-log.md").write_text("log\n", encoding="utf-8")
    (task / "t01_first_task.md").write_text(
        "# t01\n- `outline/records/t01_first_task-log.md`\n- see /_board/outline?path=x\n", encoding="utf-8")
    (task / "runs").mkdir()
    (task / "runs" / "r01_run.sh").write_text('PAGE_DIR=x; cat "$PAGE_DIR/outline/records/a.md"\n', encoding="utf-8")
    (tmp_path / "tasks" / "TASK-TABLE.md").write_text(
        "b01_x/j01_y/t01_first_task/outline/records/t01_first_task-log.md\noutline/ elsewhere\n", encoding="utf-8")
    report = draft_layout_tree(tmp_path / "tasks", sort_runs=True)
    assert report["pages"][0]["plan"] == "no plan yet" and (task / "draft" / "records").is_dir()
    face = (task / "t01_first_task.md").read_text()
    assert "`draft/records/t01_first_task-log.md`" in face and "/_board/outline?path=x" in face
    assert "$PAGE_DIR/draft/records/a.md" in (task / "runs" / "r01_run.sh").read_text()
    table = (tmp_path / "tasks" / "TASK-TABLE.md").read_text()
    assert "t01_first_task/draft/records/" in table and "outline/ elsewhere" in table
    assert check_page_folder(task)["verdict"] == "latest"


def test_board_migration_moves_records_and_links_between_pages(tmp_path: Path):
    from src.draft_migration import draft_layout_tree
    from src.layout_check import check_page_folder
    board = tmp_path / "Board" / "Ba-Main"
    for name in ("S-One", "S-Two"):
        page = board / name
        (page / "outline").mkdir(parents=True)
        (page / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
        (page / "outline" / f"{name}-outline-v1.1.md").write_text(DRAFT_FIRST, encoding="utf-8")
        (page / "outline" / f"{name}-log.md").write_text("log\n", encoding="utf-8")
    (board / "S-Two" / "S-Two.md").write_text(
        "# S-Two\nsee ../S-One/outline/S-One-log.md and outline/S-Two-log.md\n", encoding="utf-8")
    dry = draft_layout_tree(tmp_path / "Board", dry_run=True)
    assert dry["between_pages"]["outline_to_draft"] >= 1 and dry["pages"][0]["records_moved"] == 1
    assert (board / "S-One" / "outline").is_dir()  # a dry run moves nothing
    draft_layout_tree(tmp_path / "Board")
    face = (board / "S-Two" / "S-Two.md").read_text()
    assert "../S-One/draft/records/S-One-log.md" in face and "draft/records/S-Two-log.md" in face
    assert all(check_page_folder(board / n)["verdict"] == "latest" for n in ("S-One", "S-Two"))


def test_migration_keeps_sealed_results_and_skips_ambiguous_moves(tmp_path: Path):
    from src.draft_migration import draft_layout
    page = tmp_path / "Sample-Page"
    (page / "outline" / "history").mkdir(parents=True)
    (page / "Sample-Page.md").write_text("# Sample-Page\nplan: outline/Sample-Page-outline-v1.1.md\n",
                                         encoding="utf-8")
    approved = DRAFT_FIRST.replace("outline-version: v1.1\n", "outline-version: v1.1\napproved: ✅ JL 260906\n")
    (page / "outline" / "Sample-Page-outline-v1.1.md").write_text(approved, encoding="utf-8")
    (page / "outline" / "history" / "Sample-Page-outline-v1.1.md").write_text("older bytes\n", encoding="utf-8")
    sealed = "input: outline/Sample-Page-outline-v1.1.md\n"
    (page / "results" / "r01_x").mkdir(parents=True)
    (page / "results" / "r01_x" / "input.yaml").write_text(sealed, encoding="utf-8")
    draft_layout(page)
    assert (page / "results" / "r01_x" / "input.yaml").read_text() == sealed
    face = (page / "Sample-Page.md").read_text()
    assert "draft/Sample-Page-outline-v1.1.md" in face  # two files share the name: not guessed
    new = (page / "draft" / "Sample-Page-draft-v1.2.md").read_text()
    assert "approved: ✅ JL 260906 · carried from v1.1: same Bullets, three-section layout" in new


def test_archive_evidence_moves_retired_lanes_and_repoints_citations(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "t07_task"
    unit = page / "draft" / "evidence" / "display" / "Display1-x" / "assets"
    unit.mkdir(parents=True)
    (unit / "figure.pdf").write_bytes(b"%PDF")
    (page / "draft" / "evidence" / "bibex").mkdir()
    (page / "draft" / "t07_task-evidence.md").write_text("old ledger\n", encoding="utf-8")
    (page / "t07_task.md").write_text("# t07\nsee draft/t07_task-evidence.md\n", encoding="utf-8")
    (page / "delivery" / "latex").mkdir(parents=True)
    tex = "\\includegraphics{../../draft/evidence/display/Display1-x/assets/figure.pdf}\n"
    (page / "delivery" / "latex" / "t07_task.tex").write_text(tex, encoding="utf-8")
    (page / "results" / "r01").mkdir(parents=True)
    (page / "results" / "r01" / "input.yaml").write_text("a: draft/evidence/display/Display1-x\n", encoding="utf-8")
    (page / "results" / "re-display-01" / "payload" / "Display1-x").mkdir(parents=True)  # carried by a Result
    assert check_page_folder(page)["verdict"] == "behind"
    report = draft_layout(page, archive_evidence=True)["archived_evidence"]
    assert report["moved"] == ["evidence/display", "t07_task-evidence.md"] and not report["blocked"]
    moved = "draft/_archive/legacy-outline-evidence/evidence/display/Display1-x/assets/figure.pdf"
    assert (page / moved).is_file() and (page / "draft" / "evidence" / "bibex").is_dir()
    assert moved in (page / "delivery" / "latex" / "t07_task.tex").read_text()
    assert "draft/_archive/legacy-outline-evidence/t07_task-evidence.md" in (page / "t07_task.md").read_text()
    assert "a: draft/evidence/display/Display1-x" in (page / "results" / "r01" / "input.yaml").read_text()
    assert check_page_folder(page)["verdict"] == "latest"


def test_archive_evidence_keeps_display_units_without_a_result(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "S-Paper-Main-3-Results"
    (page / "draft" / "evidence" / "display" / "Display1-table").mkdir(parents=True)
    (page / "draft" / "evidence" / "supporting-runs").mkdir(parents=True)
    (page / "S-Paper-Main-3-Results.md").write_text("# Results\n", encoding="utf-8")
    report = draft_layout(page, archive_evidence=True)["archived_evidence"]
    assert report["moved"] == ["evidence/supporting-runs"]
    assert report["kept"] == ["evidence/display (1 unit(s) without a DISPLAY Result)"]
    assert (page / "draft" / "evidence" / "display" / "Display1-table").is_dir()
    rules = {r["rule"]: r for r in check_page_folder(page)["rules"]}
    assert rules["retired Outline evidence archived"]["state"] == "PASS"
    assert rules["display units are DISPLAY Results"]["state"] == "BEHIND"
    (page / "results" / "re-display-01" / "payload" / "Display1-table").mkdir(parents=True)
    assert draft_layout(page, archive_evidence=True)["archived_evidence"]["moved"] == ["evidence/display"]
    assert check_page_folder(page)["verdict"] == "latest"


def test_unknown_evidence_kind_skips_grouping_but_moves_the_page(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "t03_task"
    (page / "outline").mkdir(parents=True)
    (page / "t03_task.md").write_text("# t03\n", encoding="utf-8")
    items = "# Evidence Items\n\n### E01-CITE-a · C1.P1.B1 · a\n- **Need**: a\n\n### E02-SCHEMA-b · C1.P1.B2 · b\n- **Need**: b\n"
    (page / "outline" / "t03_task-evidence-items.md").write_text(items, encoding="utf-8")
    report = draft_layout(page)
    assert report["renamed"] == "outline/ → draft/" and report["evidence"].startswith("not grouped: unknown evidence kind 'SCHEMA'")
    assert (page / "draft" / "t03_task-evidence-items.md").read_text() == items
    rule = {r["rule"]: r for r in check_page_folder(page)["rules"]}["Evidence Markdown grouped by kind"]
    assert rule["state"] == "BEHIND" and rule["fix"].startswith("EVIDENCE: retype the item")


def test_archive_evidence_keeps_relative_links_on_their_targets(tmp_path: Path):
    from src.draft_migration import draft_layout
    seed = tmp_path / "Story00-ideation"
    seed.mkdir()
    (seed / "Story00-ideation.md").write_text("# seed\n", encoding="utf-8")
    page = tmp_path / "Story01-seed"
    pagex = page / "draft" / "evidence" / "pagex"
    pagex.mkdir(parents=True)
    (page / "Story01-seed.md").write_text("# Story01\n", encoding="utf-8")
    (pagex / "SD00-ideation.md").symlink_to("../../../../Story00-ideation/Story00-ideation.md")
    assert (pagex / "SD00-ideation.md").read_text() == "# seed\n"
    draft_layout(page, archive_evidence=True)
    moved = page / "draft" / "_archive" / "legacy-outline-evidence" / "evidence" / "pagex" / "SD00-ideation.md"
    assert moved.is_symlink() and moved.read_text() == "# seed\n"


LOOSE_PLAN = """# Loose-Page · outline v1
outline-version: v1
approved: ✅ JL 260901

## C1 · Opening

- A division note before any paragraph

### C1.P1 · First · S1 to S1
- B1 · S1 · [Claim] The first sentence.
  Point: First point
  Evidence: none · a definition
%% a note the three sections have no field for
- Note: P01 keeps its example

### Cut · detail that moves downstream
- the cut detail
"""


def test_three_sections_keep_every_line_that_is_not_a_bullet(tmp_path: Path):
    from src.draft_migration import _lost_lines, draft_layout
    page = tmp_path / "Loose-Page"
    (page / "outline").mkdir(parents=True)
    (page / "Loose-Page.md").write_text("# Loose\n", encoding="utf-8")
    (page / "outline" / "Loose-Page-outline-v1.md").write_text(LOOSE_PLAN, encoding="utf-8")
    report = draft_layout(page)
    assert report["plan"] == "Loose-Page-outline-v1.md → Loose-Page-draft-v0.2.md"  # legacy v1 is v0.1
    new = (page / "draft" / "Loose-Page-draft-v0.2.md").read_text()
    assert _lost_lines(LOOSE_PLAN, new) == []
    scratch = new.split("## 2 · Scratch")[1].split("## 3 · Draft")[0]
    assert "### C1 · Opening\n- A division note before any paragraph\n\n### Cut · detail" in scratch
    assert "### C1.P1 · First · S1 to S1\n%% a note the three sections have no field for\n- Note: P01" in scratch
    assert "approved: ✅ JL 260901 · carried from v1" in new


def test_a_plan_without_bullets_is_left_as_it_is(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "StoryA"
    (page / "outline").mkdir(parents=True)
    (page / "StoryA.md").write_text("# StoryA\n", encoding="utf-8")
    plan = "# StoryA · outline v0.1\noutline-version: v0.1\n\n## C1 · Idea\n\n- Working title and identity\n"
    (page / "outline" / "StoryA-outline-v0.1.md").write_text(plan, encoding="utf-8")
    assert "has no Bullets" in draft_layout(page)["plan"]
    assert (page / "draft" / "StoryA-outline-v0.1.md").read_text() == plan
    rule = {r["rule"]: r for r in check_page_folder(page)["rules"]}["plan in three sections"]
    assert rule["state"] == "BEHIND" and rule["fix"].startswith("OUTLINE: write the plan as Bullets")


def test_moved_tickets_and_relative_citations_follow(tmp_path: Path):
    from src.draft_migration import draft_layout
    page = tmp_path / "S-Page"
    (page / "runs").mkdir(parents=True)
    (page / "draft" / "evidence" / "display" / "U1").mkdir(parents=True)
    (page / "results" / "re-cite-01_x" / "payload" / "U1").mkdir(parents=True)
    (page / "S-Page.md").write_text("# S\n", encoding="utf-8")
    ticket = 'script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\npage_dir="$(cd "$script_dir/.." && pwd)"\n'
    (page / "runs" / "re-cite-01_x.sh").write_text(ticket, encoding="utf-8")
    (page / "draft" / "S-Page-evidence-items.md").write_text("see [run](../runs/re-cite-01_x.sh)\n", encoding="utf-8")
    deep = page / "draft" / "evidence" / "display" / "U1" / "README.md"
    deep.write_text("[t](../../../../runs/re-cite-01_x.sh) and ../Other/runs/re-cite-01_x.sh\n", encoding="utf-8")
    draft_layout(page, sort_runs=True)
    moved = (page / "runs" / "evidence-run" / "re-cite-01_x.sh").read_text()
    assert 'page_dir="$(cd "$script_dir/../.." && pwd)"' in moved
    assert "(../runs/evidence-run/re-cite-01_x.sh)" in (page / "draft" / "S-Page-evidence-items.md").read_text()
    text = deep.read_text()
    assert "(../../../../runs/evidence-run/re-cite-01_x.sh)" in text and "../Other/runs/re-cite-01_x.sh" in text


def test_sweep_keeps_prose_rewrites_python_joins_and_follows_the_archive(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "S-Two"
    (page / "outline" / "evidence" / "materials").mkdir(parents=True)
    (page / "outline" / "evidence" / "supporting-runs").mkdir(parents=True)
    (page / "outline" / "S-Two-evidence.md").write_text("old ledger\n", encoding="utf-8")
    (page / "outline" / "S-Two-files.md").write_text("- **Path**: `../../Sibling/Sibling.md`\n", encoding="utf-8")
    (tmp_path / "Sibling").mkdir()
    (tmp_path / "Sibling" / "Sibling.md").write_text("# Sib\n", encoding="utf-8")
    (page / "S-Two.md").write_text("# S\nThe outline/content split. See outline/S-Two-evidence.md\n", encoding="utf-8")
    (page / "scripts").mkdir()
    (page / "scripts" / "read.py").write_text('ledger = page_dir / "outline" / "x.md"\nkey = data["outline"]\n', encoding="utf-8")
    draft_layout(page, archive_evidence=True)
    face = (page / "S-Two.md").read_text()
    assert "The outline/content split" in face
    assert "draft/_archive/legacy-outline-evidence/S-Two-evidence.md" in face
    assert (page / "scripts" / "read.py").read_text() == 'ledger = page_dir / "draft" / "x.md"\nkey = data["outline"]\n'
    assert (page / "draft" / "evidence" / "materials").is_dir()  # the Page's imports stay live
    assert "`../../../Sibling/Sibling.md`" in (page / "draft" / "records" / "S-Two-files.md").read_text()
    assert check_page_folder(page)["verdict"] == "latest"


BARE_PLAN = """# Bare-Page · outline v3
outline-version: v3
approved: ✅ JL 260828

## C1 · Identity
- B1 · Working title and identity.   ✅ have it
- B2 · Unit of analysis.   🔢 value · S1

## C2 · Pitch
- B1 · Four moves in about 150 words.   ✅ have it

### Cut · moved downstream
- B2 · The long version.
"""


def test_bullets_straight_under_a_division_sit_in_paragraph_1(tmp_path: Path):
    from src.draft_migration import _lost_lines, draft_layout
    page = tmp_path / "Bare-Page"
    (page / "outline").mkdir(parents=True)
    (page / "Bare-Page.md").write_text("# Bare\n", encoding="utf-8")
    (page / "outline" / "Bare-Page-outline-v3.md").write_text(BARE_PLAN, encoding="utf-8")
    assert draft_layout(page)["plan"] == "Bare-Page-outline-v3.md → Bare-Page-draft-v0.4.md"
    new = (page / "draft" / "Bare-Page-draft-v0.4.md").read_text()
    assert rows(new) == rows(BARE_PLAN) and _lost_lines(BARE_PLAN, new) == []
    structure, scratch = new.split("## 2 · Scratch")[0], new.split("## 2 · Scratch")[1].split("## 3 · Draft")[0]
    assert "### C1.P1\n- B1 · Working title and identity.   ✅ have it" in structure
    assert "Working title" not in scratch and "### Cut · moved downstream\n- B2 · The long version." in scratch


REGISTRY_PLAN = """# Reg-Page · outline v0.3
outline-version: v0.3

## C1 · Abstract

### C1.P1 · One paragraph · S1 to S1
- B1 · S1 · [Premise] Scaling laws assume unlimited data.
  Draft: Scaling laws assume data is unlimited.

## Scratch

### rp-scratch-01_C1.P1 · paragraph · C1.P1
- Scope: paragraph
- Target: C1.P1
- Status: open
- Started: 2026-09-18T21:21:30+00:00
- Updated: 2026-09-21T01:18:25+00:00
- Run: rp-scratch-01_C1.P1
- Notes: |
  S1 - why scaling law

  For physiological signals this does not hold.
- Summary: |
  premise first

## Aims
- Keep the abstract under 150 words.
"""


def test_a_0117_scratch_registry_moves_into_section_2(tmp_path: Path):
    from src.draft_migration import draft_layout
    page = tmp_path / "Reg-Page"
    (page / "outline").mkdir(parents=True)
    (page / "Reg-Page.md").write_text("# Reg\n", encoding="utf-8")
    (page / "outline" / "Reg-Page-outline-v0.3.md").write_text(REGISTRY_PLAN, encoding="utf-8")
    assert draft_layout(page)["plan"] == "Reg-Page-outline-v0.3.md → Reg-Page-draft-v0.4.md"
    new = (page / "draft" / "Reg-Page-draft-v0.4.md").read_text()
    assert "\n## Scratch\n" not in new and "- Started:" not in new and "## Aims\n- Keep the abstract" in new
    notes = scratch_notes(new)
    assert [(n["run"], n["target"], n["status"], n["summary"]) for n in notes] == [
        ("rp-scratch-01_C1.P1", "C1.P1", "open", "premise first")]
    assert notes[0]["notes"] == "S1 - why scaling law\n\nFor physiological signals this does not hold."


def test_a_sentence_ending_in_outline_step_is_prose(tmp_path: Path):
    from src.draft_migration import is_prose_outline
    assert is_prose_outline("content.", tmp_path) and is_prose_outline("venue. Next", tmp_path)
    assert not is_prose_outline("content.md", tmp_path) and not is_prose_outline("evidence/bibex", tmp_path)


def test_archive_keeps_retired_evidence_a_script_still_reads(tmp_path: Path):
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    project = tmp_path / "Project-X"
    (project / ".git").mkdir(parents=True)
    page = project / "board" / "S-Results"
    (page / "draft" / "evidence" / "cite").mkdir(parents=True)
    (page / "draft" / "evidence" / "probe").mkdir(parents=True)
    (page / "S-Results.md").write_text("# S\n", encoding="utf-8")
    (page / "draft" / "S-Results-evidence.md").write_text("**Status**: specified\n", encoding="utf-8")
    (project / "build").mkdir()
    (project / "build" / "sections.py").write_text(
        'ledger = page / "draft" / f"{stem}-evidence.md"\nunits = page / "draft" / "evidence" / "cite"\n',
        encoding="utf-8")
    report = draft_layout(page, archive_evidence=True)["archived_evidence"]
    assert report["moved"] == ["evidence/probe"]
    assert report["kept"] == ["evidence/cite (read by build/sections.py)",
                              "S-Results-evidence.md (read by build/sections.py)"]
    assert (page / "draft" / "S-Results-evidence.md").is_file()
    rules = {r["rule"]: r for r in check_page_folder(page)["rules"]}
    assert rules["retired Outline evidence archived"]["state"] == "PASS"
    assert rules["no script reads retired evidence"]["state"] == "BEHIND"
    assert rules["no script reads retired evidence"]["fix"].startswith("EVIDENCE: point each script")


def test_root_pagex_is_archived_with_its_links_made_real(tmp_path: Path):
    from src.draft_migration import draft_layout_tree
    from src.layout_check import check_page_folder, pages_in
    board = tmp_path / "board"
    seed = board / "SD00-ideation"
    seed.mkdir(parents=True)
    (seed / "SD00-ideation.md").write_text("# seed\n", encoding="utf-8")
    page = board / "SD01-seed"
    (page / "pagex" / "SD00-ideation").mkdir(parents=True)
    (page / "SD01-seed.md").write_text("# SD01\nBound in pagex/SD00-ideation/SD00-ideation.md.\n",
                                       encoding="utf-8")
    (page / "pagex" / "SD00-ideation" / "SD00-ideation.md").symlink_to("../../../SD00-ideation/SD00-ideation.md")
    (page / "pagex" / "gone.tex").symlink_to("../../missing.tex")
    assert pages_in(board) == [seed, page]  # a linked Face inside pagex/ is not a Page
    report = draft_layout_tree(board, archive_evidence=True)
    archived = {p["page"]: p["archived_evidence"] for p in report["pages"]}["SD01-seed"]
    assert archived["moved"] == ["pagex/"] and archived["links_dropped"] == ["gone.tex"]
    copy = page / "draft" / "_archive" / "legacy-outline-evidence" / "pagex" / "SD00-ideation" / "SD00-ideation.md"
    assert not copy.is_symlink() and copy.read_text() == "# seed\n"
    assert "draft/_archive/legacy-outline-evidence/pagex/SD00-ideation/SD00-ideation.md" in (page / "SD01-seed.md").read_text()
    assert check_page_folder(page)["verdict"] == "latest"


def test_a_task_id_file_name_is_a_path_not_prose(tmp_path: Path):
    from src.draft_migration import draft_layout, is_prose_outline
    assert not is_prose_outline("t01_demo-files.md", tmp_path) and is_prose_outline("content", tmp_path)
    page = tmp_path / "t01_demo"
    (page / "outline").mkdir(parents=True)
    (page / "t01_demo.md").write_text("# t01\n", encoding="utf-8")
    (page / "outline" / "t01_demo-files.md").write_text("- files\n", encoding="utf-8")
    (page / "outline" / "t01_demo-log.md").write_text("- 260901 · wrote `outline/t01_demo-files.md`\n", encoding="utf-8")
    draft_layout(page)
    assert "`draft/records/t01_demo-files.md`" in (page / "draft" / "records" / "t01_demo-log.md").read_text() \
        or "`draft/t01_demo-files.md`" in (page / "draft" / "records" / "t01_demo-log.md").read_text()


def test_a_multi_line_supersedes_is_replaced_whole(tmp_path: Path):
    from src.draft_migration import draft_layout
    page = tmp_path / "QC1"
    (page / "outline").mkdir(parents=True)
    (page / "QC1.md").write_text("# QC1\n", encoding="utf-8")
    plan = ("# QC1 · outline v6\noutline-version: v6\nsupersedes: v5 (approved by JL, together with both\n"
            "  rulings v5 asked for)\ndate: 260821\n\n## C1 · One\n\n### C1.P1 · First · S1 to S1\n- B1 · S1 · A.\n")
    (page / "outline" / "QC1-outline-v6.md").write_text(plan, encoding="utf-8")
    draft_layout(page)
    head = (page / "draft" / "QC1-draft-v0.7.md").read_text().split("## 1 ·")[0]
    assert "supersedes: v6\ndate: 260821" in head and "rulings" not in head


def test_a_result_card_under_results_is_not_a_page(tmp_path: Path):
    from src.layout_check import pages_in
    page = tmp_path / "t01_task"
    (page / "results" / "r01_run").mkdir(parents=True)
    (page / "t01_task.md").write_text("# t01\n", encoding="utf-8")
    (page / "results" / "r01_run" / "r01_run.md").write_text("# card\n", encoding="utf-8")
    assert pages_in(tmp_path) == [page]


def test_design_run_tickets_stay_flat():
    assert folder_for("rd01_web") == "delivery-run" and folder_for("rd00_page-content") == "delivery-run"
    for run in ("rd01_commission_item01", "rd12_generate_sms", "rd13_verify_item02", "rd43_adopt_item05"):
        assert folder_for(run) is None


def test_an_old_receipt_hash_no_longer_seals_a_ticket(tmp_path: Path):
    """JL 260928: no content hashes. An old receipt's leftover `ticket_sha256` is
    ignored, so the sweep rewrites the ticket like every other file."""
    from src.draft_migration import draft_layout
    from src.layout_check import check_page_folder
    page = tmp_path / "Design-01-x"
    (page / "outline" / "feedback").mkdir(parents=True)
    (page / "runs").mkdir()
    (page / "Design-01-x.md").write_text("# D\n", encoding="utf-8")
    (page / "outline" / "feedback" / "rd02_generate_item01.md").write_text("fb\n", encoding="utf-8")
    ticket = page / "runs" / "rd02_generate_item01.yaml"
    ticket.write_text("inputs:\n- path: outline/feedback/rd02_generate_item01.md\n", encoding="utf-8")
    (page / "results" / "rd02_generate_item01").mkdir(parents=True)
    receipt = page / "results" / "rd02_generate_item01" / "runtime.yaml"
    receipt.write_text("ticket_sha256: " + "a" * 64 + "\n", encoding="utf-8")
    draft_layout(page, sort_runs=True, archive_evidence=True)
    assert "outline/" not in ticket.read_text(encoding="utf-8")
    assert receipt.read_text(encoding="utf-8") == "ticket_sha256: " + "a" * 64 + "\n"  # results/ keeps its words
    assert check_page_folder(page)["verdict"] == "latest"
