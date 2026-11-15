"""Sentence ids written s8 (an older S8 reads the same), the sentence-case converter, and renumbering a Draft whose ids
restart in every paragraph. Temp files only."""
from pathlib import Path

from src.folder_health import check_ids
from src.page_renumber import renumber, repeated
from src.sentence_case import convert
from src.sentence_id import sid

FACE = "# t01_note · Note\n\nfolder-kind: section\npage-type: section\n\n## Content\n\n<prose>\n"

PER_PARAGRAPH = """# t01_note · draft v0.2
draft-version: v0.2

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Note
- C1.P1 · Why · S1 to S2
- C1.P2 · How · S1 to S2

### C1.P1 · Why · S1 to S2
- B1 · S1 · [Need] The need
- B2 · S2 · [Cost] The cost

### C1.P2 · How · S1 to S2
- B1 · S1 · [Way] The way
- B2 · S2 · [Gap] The gap

## 3 · Draft

### C1.P1 · Why · S1 to S2
- B1 · S1 · The problem grows.
- B2 · S2 · It costs money.

### C1.P2 · How · S1 to S2
- B1 · S1 · We ask the payers.
- B2 · S2 · Nobody has, see Table S1.
"""


def _page(tmp_path: Path, draft: str) -> Path:
    folder = tmp_path / "t01_note"
    (folder / "draft" / "records").mkdir(parents=True)
    (folder / "evidence").mkdir()
    (folder / "t01_note.md").write_text(FACE, encoding="utf-8")
    (folder / "draft" / "t01_note-draft-v0.2.md").write_text(draft, encoding="utf-8")
    return folder


def test_sid_reads_both_cases_as_one():
    assert sid("S8") == sid("s8") == "s8"
    assert sid("C1.P2.S8") == "C1.P2.s8"
    assert sid("C1.P2") == "C1.P2" and sid("B3") == "B3" and sid("s01-topic") == "s01-topic"


def test_sentence_case_rewrites_ids_only(tmp_path):
    folder = _page(tmp_path, PER_PARAGRAPH.replace("C1.P2 · How", "C1.P2 · How").replace(
        "### C1.P2 · How · S1 to S2\n- B1 · S1 · We", "### C1.P2 · How · S3 to S4\n- B1 · S3 · We").replace(
        "- B2 · S2 · Nobody", "- B2 · S4 · Nobody"))
    draft = folder / "draft" / "t01_note-draft-v0.2.md"
    rec = folder / "draft" / "records"
    (rec / "t01_note-revise.md").write_text("## Pass 1\n\n### Edit · S2 · C1.P1.B2 · the cost\nWhy: S2 is vague\n"
                                            "Original: It costs money.\n\n### Revise review report\nSentences:\n"
                                            "- S1 · logic 9/10 · read 9/10 · none · Fix: none\n", encoding="utf-8")
    (rec / "t01_note-checked.md").write_text("- S1 · 2026-11-14 10:00 · The problem grows.\n", encoding="utf-8")
    before = draft.read_text()
    dry = convert(draft, records=True, dry_run=True)
    assert [p.name for p, _, _ in dry] == ["t01_note-draft-v0.2.md", "t01_note-revise.md", "t01_note-checked.md"]
    assert draft.read_text() == before                                     # a dry run writes nothing
    convert(draft, records=True)
    text = draft.read_text()
    assert "- B1 · s1 · The problem grows." in text and "### C1.P2 · How · s3 to s4" in text
    assert "- C1.P1 · Why · s1 to s2" in text and "see Table S1." in text   # a sentence's own words stay
    revise = (rec / "t01_note-revise.md").read_text()
    assert "### Edit · s2 · C1.P1.B2 · the cost" in revise and "- s1 · logic" in revise
    assert "Why: S2 is vague" in revise                                    # prose in a card stays as written
    assert (rec / "t01_note-checked.md").read_text().startswith("- s1 · ")
    assert convert(draft, records=True) == []                              # a second run changes nothing


def test_a_draft_numbered_per_paragraph_renumbers_through_the_section(tmp_path):
    folder = _page(tmp_path, PER_PARAGRAPH)
    rec = folder / "draft" / "records"
    (rec / "t01_note-revise.md").write_text(
        "## Pass 1\n\n### Edit · S1 · C1.P2.B1 · the ask\nWhy: see C1.P2.S2\n\n### Edit · S2 · the cost\nWhy: x\n",
        encoding="utf-8")
    (rec / "t01_note-checked.md").write_text("- S2 · 2026-11-14 10:00 · Nobody has, see Table S1.\n", encoding="utf-8")
    (rec / "t01_note-comments.md").write_text("### Comment 1 · C1.P2.S1\nState: open\n- Note · 2026-11-14: why\n",
                                              encoding="utf-8")
    (folder / "evidence" / "cards.yaml").write_text("evidence:\n- kind: value\n  items:\n  - for:\n    - 2\n",
                                                   encoding="utf-8")
    text = (folder / "draft" / "t01_note-draft-v0.2.md").read_text()
    assert repeated(text) == ["s1", "s2"]
    found = []
    check_ids(folder / "draft" / "t01_note-draft-v0.2.md", text, found)
    assert [(f.level, f.check) for f in found] == [("FAIL", "ids")]
    dry = renumber(folder, dry_run=True)
    assert dry["mapping"] == {"C1.P2.s1": "s3", "C1.P2.s2": "s4"}           # never "already in reading order"
    assert (folder / "draft" / "t01_note-draft-v0.2.md").read_text() == text
    renumber(folder)
    draft = (folder / "draft" / "t01_note-draft-v0.2.md").read_text()
    assert "### C1.P2 · How · s3 to s4\n- B1 · s3 · [Way] The way\n- B2 · s4 · [Gap] The gap" in draft
    assert "- B1 · s3 · We ask the payers.\n- B2 · s4 · Nobody has, see Table S1." in draft
    assert "- B1 · s1 · The problem grows." in draft and "- C1.P2 · How · s3 to s4" in draft
    revise = (rec / "t01_note-revise.md").read_text()
    assert "### Edit · s3 · C1.P2.B1 · the ask\nWhy: see C1.P2.s4" in revise   # mapped by its paragraph
    assert "### Edit · S2 · the cost" in revise                                # a bare id with no paragraph stays
    assert (rec / "t01_note-checked.md").read_text().startswith("- s4 · ")    # by its words
    assert "### Comment 1 · C1.P2.s3" in (rec / "t01_note-comments.md").read_text()
    assert dry["ambiguous"] == ["t01_note-revise.md:6 S2", "evidence/cards.yaml:5 2"]   # listed for a person
    assert repeated((folder / "draft" / "t01_note-draft-v0.2.md").read_text()) == []
