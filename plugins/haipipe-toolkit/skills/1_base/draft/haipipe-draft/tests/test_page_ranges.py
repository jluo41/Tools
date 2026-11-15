"""A paragraph's range is rebuilt from the sentences it holds, in its heading and its Structure Overview line, by
`page.py renumber`; a range that does not match fails the ids health check; an Abstract's title paragraph keeps s0
(ScalingGlucose 261115: Overview ranges left for hand fixes, "s21 to s26" shifted to s27, the title's s0 moved to s1).
Temp drafts only."""
from pathlib import Path

from src.folder_health import check_ids
from src.page_ranges import fix, wrong
from src.page_renumber import renumber

FACE = "# t01_note · Note\n\nfolder-kind: section\npage-type: section\n\n## Content\n\n<prose>\n"

ARROWS = """# t01_note · draft v0.2
draft-version: v0.2

## 1 · Structure · Bullet Point Table

### Structure Overview

C1.P1 Why the need matters → s1 to s3
C1.P2 How we ask → s4 to s9

## 3 · Draft

### C1.P1 · Why · s1 to s2
- B1 · s1 · The problem grows.
- B2 · s2 · It costs money.

### C1.P2 · How · s3 to s5
- B1 · s3 · We ask the payers.
- B2 · s4 · They answer.
- B3 · s5 · Nobody has, see Table S1.
"""

TITLE = """# t00_abstract · draft v1.0
draft-version: v1.0

## 3 · Draft

### C1.P0 · Title · s0
- B1 · s0 · A title.

### C1.P1 · Abstract · s1 to s3
- B1 · s1 · One.
- B2 · s2 · Two.
- B3 · s3 · Three.
"""


def _page(tmp_path: Path, name: str, draft: str) -> Path:
    folder = tmp_path / name
    (folder / "draft" / "records").mkdir(parents=True)
    (folder / f"{name}.md").write_text(FACE.replace("t01_note", name), encoding="utf-8")
    (folder / "draft" / f"{name}-draft-v0.2.md").write_text(draft, encoding="utf-8")
    return folder


def test_overview_arrows_and_headings_take_their_paragraphs_ranges():
    out = fix(ARROWS)
    assert "C1.P1 Why the need matters → s1 to s2" in out
    assert "C1.P2 How we ask → s3 to s5" in out
    assert "### C1.P2 · How · s3 to s5" in out and "Table S1" in out        # a right heading and the words stay
    assert [n for n, _, _ in wrong(ARROWS)] == [8, 9]


def test_renumber_fixes_ranges_even_when_the_ids_are_in_order(tmp_path):
    folder = _page(tmp_path, "t01_note", ARROWS)
    draft = folder / "draft" / "t01_note-draft-v0.2.md"
    found = []
    check_ids(draft, draft.read_text(), found)
    assert [(f.level, f.check) for f in found] == [("FAIL", "ids")]       # the health check fails a wrong range
    report = renumber(folder)
    assert report["mapping"] == {} and report["written"]
    assert "C1.P2 How we ask → s3 to s5" in draft.read_text()
    found = []
    check_ids(draft, draft.read_text(), found)
    assert found == []


def test_a_person_set_range_end_follows_its_paragraph_not_a_shift(tmp_path):
    shifted = ARROWS.replace("- B1 · s3 · We ask the payers.\n", "- B1 · s3 · We ask the payers.\n- B1b · s3b · New one.\n")
    folder = _page(tmp_path, "t01_note", shifted)
    renumber(folder)
    text = (folder / "draft" / "t01_note-draft-v0.2.md").read_text()
    assert "### C1.P2 · How · s3 to s6" in text and "→ s3 to s6" in text


def test_an_abstract_title_keeps_s0(tmp_path):
    folder = _page(tmp_path, "t00_abstract", TITLE)
    report = renumber(folder, dry_run=True)
    assert report["mapping"] == {}                                          # s0 is never moved to s1
