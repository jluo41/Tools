"""`page.py adopt`: the Draft's sentences reach the Page Content in Draft order."""
from pathlib import Path

from src.folder_health import folder_health
from src.page_adopt import run

PAGE = """# Q1-demo · demo
state: DRAFT

## Content
### §1 Results

#### P1. First
(Say the result.)

Alpha one. <!-- realizes: C1.P1.B1 -->
> Value: E01-VALUE-a · results/re-value-01/result.yaml
Beta two. <!-- realizes: C1.P1.B2 -->
Gamma three. <!-- realizes: C1.P1.B3 -->
> Citation: smith2020 · \\citep{smith2020}

#### P2. Second

Delta four. <!-- realizes: C1.P2.B1 -->

## Aims
- A1 · done when the Page prints the Draft
"""


def draft(structure: str, sentences: str) -> str:
    return f"""# Q1-demo · draft v1.0
draft-version: v1.0
approved: ⬜

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Results

{structure}
## 2 · Scratch · What to write here

## 3 · Draft · Reading and Revise

{sentences}"""


STRUCTURE = """### C1.P1 · First · S1 to S3
- B1 · S1 · [Claim] state alpha
- B2 · S2 · [Claim] state beta
- B3 · S3 · [Claim] state gamma

### C1.P2 · Second · S4
- B1 · S4 · [Claim] state delta
"""

SENTENCES = """### C1.P1 · First · S1 to S3
- B1 · S1 · Alpha one.
- B2 · S2 · Beta two.
- B3 · S3 · Gamma three.

### C1.P2 · Second · S4
- B1 · S4 · Delta four.
"""


def make(tmp_path: Path, page=PAGE, structure=STRUCTURE, sentences=SENTENCES) -> Path:
    folder = tmp_path / "Q1-demo"
    (folder / "draft").mkdir(parents=True)
    (folder / "Q1-demo.md").write_text(page, encoding="utf-8")
    (folder / "draft" / "Q1-demo-draft-v1.0.md").write_text(draft(structure, sentences), encoding="utf-8")
    return folder


def sync(folder: Path) -> list:
    return [f for f in folder_health(folder)["findings"] if f["check"] == "sync"]


def test_a_page_equal_to_its_draft_is_untouched(tmp_path):
    folder = make(tmp_path)
    report = run(folder, dry_run=True)
    assert report["refused"] == [] and report["changes"] == [] and report["diff"] == ""
    assert (folder / "Q1-demo.md").read_text(encoding="utf-8") == PAGE


def test_rewrite_reorder_add_and_cut_keep_apparatus_with_its_sentence(tmp_path):
    structure = STRUCTURE.replace("- B3 · S3 · [Claim] state gamma", "- B4 · S3 · [Claim] state epsilon")
    sentences = SENTENCES.replace("- B1 · S1 · Alpha one.\n- B2 · S2 · Beta two.\n- B3 · S3 · Gamma three.",
                                  "- B2 · S1 · Beta two, revised.\n- B1 · S2 · Alpha one.\n- B4 · S3 · Epsilon five.")
    folder = make(tmp_path, structure=structure, sentences=sentences)
    dry = run(folder, dry_run=True)
    assert (folder / "Q1-demo.md").read_text(encoding="utf-8") == PAGE          # a dry run writes nothing
    assert dry["changes"] == ["rewritten C1.P1.B2", "added C1.P1.B4", "removed C1.P1.B3"]
    assert dry["dropped"] == ["C1.P1.B3 · > Citation: smith2020 · \\citep{smith2020}"]
    report = run(folder)
    assert report["written"]
    text = (folder / "Q1-demo.md").read_text(encoding="utf-8")
    assert ("#### P1. First\n(Say the result.)\n\n"
            "Beta two, revised. <!-- realizes: C1.P1.B2 -->\n"
            "Alpha one. <!-- realizes: C1.P1.B1 -->\n"
            "> Value: E01-VALUE-a · results/re-value-01/result.yaml\n"
            "Epsilon five. <!-- realizes: C1.P1.B4 -->\n\n#### P2. Second") in text
    assert "Gamma" not in text and "smith2020" not in text
    assert text.endswith("## Aims\n- A1 · done when the Page prints the Draft\n")
    assert [f["level"] for f in sync(folder)] == ["OK"]


def test_a_paragraph_mismatch_is_refused_and_nothing_is_written(tmp_path):
    structure = STRUCTURE + "\n### C1.P3 · Third · S5\n- B1 · S5 · [Claim] state zeta\n"
    sentences = SENTENCES + "\n### C1.P3 · Third · S5\n- B1 · S5 · Zeta six.\n"
    folder = make(tmp_path, structure=structure, sentences=sentences)
    report = run(folder)
    assert report["refused"] == ["Draft paragraph(s) with no Page paragraph: C1.P3"]
    assert (folder / "Q1-demo.md").read_text(encoding="utf-8") == PAGE


def test_an_address_on_two_lines_is_one_sentence_and_a_marker_is_not_printed(tmp_path):
    page = PAGE.replace("Gamma three. <!-- realizes: C1.P1.B3 -->",
                        "Gamma three. <!-- realizes: C1.P1.B3 -->\n> ✎ a review mark\n"
                        "Gamma more. <!-- realizes: C1.P1.B3 -->")
    sentences = (SENTENCES.replace("- B3 · S3 · Gamma three.", "- B3 · S3-S4 · Gamma three.\n  Gamma, more.")
                 .replace("- B1 · S4 · Delta four.", "- B1 · S4 · [open · E05 · Q-2] Delta, once the rerun lands."))
    folder = make(tmp_path, page=page, sentences=sentences)
    report = run(folder)
    assert report["changes"] == ["rewritten C1.P1.B3"]
    assert report["notes"] == ["C1.P2.B1 Draft is still a marker ([open · E05 · Q-2]); left off the Page"]
    text = (folder / "Q1-demo.md").read_text(encoding="utf-8")
    assert ("Gamma three. <!-- realizes: C1.P1.B3 -->\nGamma, more.\n> ✎ a review mark\n"
            "> Citation: smith2020 · \\citep{smith2020}") in text
    assert "Delta four. <!-- realizes: C1.P2.B1 -->" in text                 # the Page keeps its sentence


def test_untagged_material_under_a_sentence_is_never_moved(tmp_path):
    page = PAGE.replace("Beta two. <!-- realizes: C1.P1.B2 -->",
                        "Beta two. <!-- realizes: C1.P1.B2 -->\n\n```text\nInput: reviews\n```")
    structure = STRUCTURE.replace("- B3 · S3 · [Claim] state gamma", "- B3 · S3 · [Claim] state gamma\n- B4 · S4 · [Claim] new")
    sentences = SENTENCES.replace("- B3 · S3 · Gamma three.", "- B3 · S3 · Gamma three.\n- B4 · S4 · Epsilon five.")
    folder = make(tmp_path, page=page, structure=structure, sentences=sentences)
    report = run(folder)
    assert len(report["refused"]) == 1 and report["refused"][0].startswith("C1.P1 holds 3 untagged line(s)")
    assert (folder / "Q1-demo.md").read_text(encoding="utf-8") == page
    # a rewrite in place is still allowed there
    folder2 = make(tmp_path / "b", page=page, sentences=SENTENCES.replace("Gamma three.", "Gamma, rewritten."))
    assert run(folder2)["changes"] == ["rewritten C1.P1.B3"]
    assert "```text\nInput: reviews\n```" in (folder2 / "Q1-demo.md").read_text(encoding="utf-8")


LEDGER = """# Q1-demo · evidence items

## Citations

### E02-CITE-source · C1.P1.B2 · the source
- **Supporting Runs**: Discovery · reuse · b01j01t04r01
- **Local Run**: Page · Evidence Item · reuse · re-cite-01_source → results/re-cite-01_source/result.yaml
- **Decide**: ☑ make

## Displays

## Values

### E01-VALUE-a · C1.P1.B1 · the a value
- **Supporting Runs**: Execution · reuse · b03j02t01r04; Execution · reuse · b03j02t05r04
- **Local Run**: Page · Evidence Item · reuse · re-value-01_a → results/re-value-01_a/result.yaml
- **Decide**: ☑ make

### E03-VALUE-later · C1.P1.B3 · a later value
- **Supporting Runs**: []
- **Local Run**: Page · Evidence Item · reuse · re-value-02_later → results/re-value-02_later/result.yaml
- **Decide**: ☑ defer
"""


def test_evidence_lines_are_written_from_the_draft_and_the_ledger(tmp_path):
    """JL 260928: `> Value:` / `> Citation:` / `> Display:` / `> Supporting Run:` lines are derived:
    the Bullet names its items, the ledger binds each to a Result and its Supporting Runs."""
    structure = STRUCTURE.replace(
        "- B1 · S1 · [Claim] state alpha", "- B1 · S1 · [Claim] state alpha\n  Evidence: E01-VALUE-a · the a value").replace(
        "- B2 · S2 · [Claim] state beta", "- B2 · S2 · [Claim] state beta\n  Evidence: E02-CITE-source · the source").replace(
        "- B3 · S3 · [Claim] state gamma", "- B3 · S3 · [Claim] state gamma\n  Evidence: E03-VALUE-later · deferred")
    page = PAGE.replace("Beta two. <!-- realizes: C1.P1.B2 -->",
                        "Beta two. <!-- realizes: C1.P1.B2 -->\n> Citation: smith2020 · \\citep{smith2020} · hand note\n"
                        "> Value: paper-owned definition · cutoff = 0.75").replace(
                        "Gamma three. <!-- realizes: C1.P1.B3 -->",
                        "Gamma three. <!-- realizes: C1.P1.B3 -->\n> Value: E03-VALUE-later · deferred for now")
    folder = make(tmp_path, page=page, structure=structure)
    (folder / "draft" / "Q1-demo-evidence-items.md").write_text(LEDGER, encoding="utf-8")
    cite = folder / "results" / "re-cite-01_source"
    cite.mkdir(parents=True)
    (cite / "result.yaml").write_text('{"item": "E02-CITE-source", "type": "CITE", '
                                      '"payload": {"sources": [{"cite": "@smith2020"}]}}', encoding="utf-8")
    report = run(folder)
    assert report["refused"] == []
    assert report["changes"] == ["evidence lines C1.P1.B1: +3 −1", "evidence lines C1.P1.B2: +2 −1",
                                 "evidence lines C1.P1.B3: +0 −1"]
    text = (folder / "Q1-demo.md").read_text(encoding="utf-8")
    assert ("Alpha one. <!-- realizes: C1.P1.B1 -->\n"
            "> Value: E01-VALUE-a · results/re-value-01/result.yaml\n") not in text     # the old hand path is replaced
    assert ("Alpha one. <!-- realizes: C1.P1.B1 -->\n"
            "> Value: E01-VALUE-a · results/re-value-01_a/result.yaml\n"
            "> Supporting Run: b03j02t01r04 · Execution · E01-VALUE-a\n"
            "> Supporting Run: b03j02t05r04 · Execution · E01-VALUE-a\n") in text
    assert ("Beta two. <!-- realizes: C1.P1.B2 -->\n"
            "> Citation: E02-CITE-source · results/re-cite-01_source/result.yaml · smith2020\n"
            "> Supporting Run: b01j01t04r01 · Discovery · E02-CITE-source\n"
            "> Value: paper-owned definition · cutoff = 0.75\n") in text          # a line naming no item stays
    assert "hand note" not in text and "deferred for now" not in text           # replaced, and a deferred item
    assert run(folder)["changes"] == []                                           # a second adopt changes nothing
