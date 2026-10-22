"""page.py renumber, page.py bump, and adopt laying out a new Page's Content (t01_introduction, 261021).

What one Section needed by hand, every draft Task now gets as a command: the sentence ids renumbered in reading order
in every file that names them, the draft moved to its next version, and a Page whose Content is still the placeholder
laid out from its Draft so `adopt` and `export` can run.
"""
from pathlib import Path

from src.page_adopt import run as adopt_run
from src.page_bump import bump
from src.page_renumber import renumber

FACE = """# t01_note · Note

folder-kind: section
page-type: section

## Opening

Why it matters.

## Content

<the Section's prose, adopted from its Draft>

## Aims

- none
"""

DRAFT = """# t01_note · draft v0.4
draft-version: v0.4
supersedes: v0.3
date: 261020
approved: ⬜
status: working

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Note
- C1.P1 · Why

### C1.P1 · Why
- B1 · S1 · [Need] The need
- B2 · S3 · [Cost] The cost
- B3 · S2 · [Gap] The gap
- B4 · S22 · [New] A new point

## 3 · Draft · Reading and Revise

### C1.P1 · Why
- B1 · S1 · The problem grows.
- B2 · S3 · It costs money \\citep{Wang_2022}.
- B3 · S2 · No one has measured it.
- B4 · S22 · A new sentence.
"""


def _page(tmp_path: Path) -> Path:
    folder = tmp_path / "t01_note"
    (folder / "draft" / "records").mkdir(parents=True)
    (folder / "evidence").mkdir()
    (folder / "t01_note.md").write_text(FACE, encoding="utf-8")
    (folder / "draft" / "t01_note-draft-v0.4.md").write_text(DRAFT, encoding="utf-8")
    (folder / "evidence" / "cards.yaml").write_text(
        "evidence:\n- kind: cite\n  source: b01.j01.t01\n  items:\n  - run: r01\n    anchor:\n    - costs money\n"
        "    for:\n    - 3\n    cite: Wang_2022\n", encoding="utf-8")
    (folder / "draft" / "records" / "t01_note-comments.md").write_text(
        "# t01_note · comments\n\n### Comment 1 · S22\nState: answered\n- Note · 2026-10-21 10:00: S22 is odd\n"
        "- Reply · 2026-10-21 10:05: S22 stays after S2.\n", encoding="utf-8")
    (folder / "draft" / "records" / "t01_note-revise.md").write_text(
        "# t01_note · Revise cards\n\n## Pass 1 · 261021 · on draft v0.4\n\n### Edit · S3 · the cost\nWhy: S3 needs a number\n"
        "State: written\n", encoding="utf-8")
    return folder


def test_renumber_follows_the_text_in_every_file(tmp_path):
    folder = _page(tmp_path)
    report = renumber(folder)
    assert report["mapping"] == {"S3": "S2", "S2": "S3", "S22": "S4"}
    draft = (folder / "draft" / "t01_note-draft-v0.4.md").read_text()
    assert "- B2 · S2 · It costs money" in draft and "- B4 · S4 · A new sentence." in draft
    assert "- B2 · S2 · [Cost] The cost" in draft                          # §1 follows §3
    assert "    for:\n    - 2\n" in (folder / "evidence" / "cards.yaml").read_text()
    comments = (folder / "draft" / "records" / "t01_note-comments.md").read_text()
    assert "### Comment 1 · S4" in comments and "Reply · 2026-10-21 10:05: S4 stays after S3." in comments
    assert "Note · 2026-10-21 10:00: S22 is odd" in comments               # the person's note stays as written
    assert "### Edit · S2 · the cost\nWhy: S2 needs a number" in (folder / "draft" / "records" / "t01_note-revise.md").read_text()
    assert renumber(folder)["mapping"] == {}                                # once in order, nothing to do


def test_bump_moves_the_draft_to_its_next_version(tmp_path):
    folder = _page(tmp_path)
    report = bump(folder)
    assert (report["from"], report["to"], report["written"]) == ("v0.4", "v0.5", True)
    new = (folder / "draft" / "t01_note-draft-v0.5.md").read_text()
    assert new.startswith("# t01_note · draft v0.5\ndraft-version: v0.5\nsupersedes: v0.4\n")
    assert "approved: ⬜\nstatus: working" in new                          # the person's lines stay
    assert (folder / "draft" / "previous" / "t01_note-draft-v0.4.md").is_file()
    assert not (folder / "draft" / "t01_note-draft-v0.4.md").exists()
    assert bump(folder, to="v0.5")["refused"]                               # never over an existing version


def test_adopt_lays_out_a_new_pages_content_from_its_draft(tmp_path):
    folder = _page(tmp_path)
    report = adopt_run(folder)
    assert not report["refused"] and report["written"]
    face = (folder / "t01_note.md").read_text()
    assert "### Note\n\n#### C1.P1 · Why\n\nThe problem grows. <!-- realizes: C1.P1.B1 -->" in face
    assert "A new sentence. <!-- realizes: C1.P1.B4 -->" in face
    assert "<the Section's prose" not in face
    assert adopt_run(folder)["changes"] == []                               # a second run finds it equal
