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


def test_draft_task_steps_warn_until_each_has_its_file(tmp_path):
    """JL 261102: a draft Task's seven steps, each by the file it leaves; a face without task-type: draft is skipped."""
    plain = folder_health(make(tmp_path / "a"))
    assert levels(plain, "steps") == []                       # not a draft Task: no steps check
    face = "# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1]
    report = folder_health(make(tmp_path / "b", face=face))
    msgs = [f["message"] for f in report["findings"] if f["check"] == "steps"]
    assert any("context.md" in m for m in msgs) and any("revise.md" in m for m in msgs)
    assert any("not signed" in m for m in msgs) and any("delivery lanes built: none" in m for m in msgs)
    assert set(levels(report, "steps")) == {WARN}


def test_final_gate_fails_what_may_wait_while_writing(tmp_path):
    """JL 261102: "I think /haipipe-draft should do this final checklist before saying it is finished"."""
    face = "# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1]
    folder = make(tmp_path, face=face)
    loose = folder_health(folder)
    final = folder_health(folder, final=True)
    assert loose["verdict"] == WARN and final["verdict"] == FAIL
    by = {(f["check"], f["level"]) for f in final["findings"]}
    assert ("printed", FAIL) in by                         # no built PDF to read back
    signs = [f for f in final["findings"] if "not signed" in f["message"]]
    assert signs and all(f["level"] == WARN for f in signs)   # the person's step is named, never failed


def test_draft_on_an_unsigned_plan_is_out_of_order(tmp_path):
    """JL 261111 (t01_introduction): § 3 written, rebound and revised on a plan never signed; the final gate fails it."""
    face = "# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1]
    plan = HEADER + BULLET + "\n## 3 · Draft\n\nThe first sentence is on the Page.\n"
    folder = make(tmp_path, face=face, plan=plan)
    assert levels(folder_health(folder), "order") == [WARN]
    # M-D15 (JL 261115): Content already holds adopted text, so health names the sign and stays a WARN at the gate
    held = [f for f in folder_health(folder, final=True)["findings"] if f["check"] == "order"]
    assert [f["level"] for f in held] == [WARN]
    assert held[0]["message"] == "Content holds text from an unsigned plan (v1.1); sign the plan"
    bare = make(tmp_path / "b", face=face.replace(" <!-- realizes: C1.P1.B1 -->", "").replace(" <!-- realizes: C1.P1.B2 -->", ""),
                plan=plan)
    assert levels(folder_health(bare, final=True), "order") == [FAIL]   # nothing adopted: the old order rule
    signed = make(tmp_path / "s", face=face, plan=plan.replace("approved: ⬜", "approved: ✅ JL 261111 · in chat: \"B\""))
    assert levels(folder_health(signed), "order") == []


def test_a_moved_governing_row_sends_the_section_back_to_plan(tmp_path):
    """JL 261111: the Narrative row changed (v0.3 to v0.4) after the sign; health says go back to Plan."""
    from src.page_sign import sign
    (tmp_path / "board.md").write_text("# Paper-X\nboard-kind: paper-board\n", encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    face = "# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1]
    folder = make(job, face=face)
    jf = job / "j11_writing_v1.md"
    jf.write_text("# j11\n\n## Narrative\n\n| Section | question |\n|---|---|\n| Sample-Page | What is it? |\n", encoding="utf-8")
    assert not sign(folder, "")["ok"]                               # the sign is the person's quoted word
    r = sign(folder, "go with B")
    assert r["ok"] and 'in chat: "go with B"' in r["approved"]
    kept = (folder / "outline" / "records" / "Sample-Page-sign.md").read_text()
    assert "| Sample-Page | What is it? |" in kept and "sha" not in kept    # the row as text, no hash
    assert levels(folder_health(folder), "row") == []
    jf.write_text(jf.read_text().replace("What is it?", "What changed?"), encoding="utf-8")
    assert levels(folder_health(folder), "row") == [WARN]
    assert levels(folder_health(folder, final=True), "row") == [FAIL]


def test_a_version_narrative_is_signed_before_its_sections(tmp_path):
    """JL 261111: the version's ## Narrative is signed (page.py sign-narrative); a changed Story § 8 makes it stale."""
    from src.page_sign import sign_narrative
    (tmp_path / "board.md").write_text("# Paper-X\nboard-kind: paper-board\nstory-current: s02-story\n", encoding="utf-8")
    (tmp_path / "s02-story").mkdir()
    story = tmp_path / "s02-story" / "s02-story.md"
    story.write_text("# s02\n\n## Content\n\n### 8 · Section Narrative\n\nC1 first.\n\n#### 8.1 · Claims\n\nC1.\n\n### 9 · Venue\n\nx\n",
                     encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    face = "# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1]
    folder = make(job, face=face)
    jf = job / "j11_writing_v1.md"
    jf.write_text("# j11\ngoal: the first send\n\n## Narrative\n\n| Section | question |\n|---|---|\n| Sample-Page | Q |\n",
                  encoding="utf-8")
    assert levels(folder_health(folder), "narrative") == [WARN]
    assert levels(folder_health(folder, final=True), "narrative") == [FAIL]
    r = sign_narrative(job, "this order")
    assert r["ok"] and (job / "records" / "narrative-sign.md").is_file()
    head = jf.read_text().split("## ")[0]
    assert "goal: the first send" in head and 'narrative-approved: ✅ JL' in head and "story-at-sign: s02-story § 8" in head
    assert levels(folder_health(folder), "narrative") == []
    story.write_text(story.read_text().replace("C1 first.", "C2 first."), encoding="utf-8")
    assert levels(folder_health(folder), "narrative") == [WARN]
    story.write_text(story.read_text().replace("C2 first.", "C1 first.").replace("\nx\n", "\ny\n"), encoding="utf-8")
    assert levels(folder_health(folder), "narrative") == []         # § 9 is not the Narrative


def test_a_paper_paragraph_holds_4_to_7_sentences(tmp_path):
    """JL 261112: "unless having good reason, we might make sure they are between 4~7 sentences"; the Abstract is
    exempt, a `reason:` line accepts the count, the final gate fails what is left."""
    from src.paragraph_length import off_range, paragraphs
    plan = (HEADER + "\n## 1 · Structure\n\n### C1.P0 · Title · S0\n\n### C1.P1 · Long · S1 to S10\n\n"
            "### C1.P2 · Fine · S11 to S15\n\n### C1.P3 · Short · S16 to S17\nreason: one claim, stated once\n\n"
            "### C1.P4 · Bullets\n- B1 · S18 · a\n- B2 · S19 · b\n")
    assert [(p, n) for p, n, _ in paragraphs(plan)] == [("C1.P1", 10), ("C1.P2", 5), ("C1.P3", 2), ("C1.P4", 2)]
    assert [p for p, _, why in off_range(plan, "results") if not why] == ["C1.P1", "C1.P4"]
    assert off_range(plan, "abstract") == []
    face = "# Sample-Page\ntask-type: draft\nsection_kind: results\n\n" + FACE.split("\n", 1)[1]
    folder = make(tmp_path, face=face, plan=plan)
    found = [f for f in folder_health(folder)["findings"] if f["check"] == "paragraph"]
    assert [f["level"] for f in found] == [WARN] and "C1.P1 has 10" in found[0]["message"] and "C1.P3" not in found[0]["message"]
    assert levels(folder_health(folder, final=True), "paragraph") == [FAIL]
    plain = make(tmp_path / "p", face="# Sample-Page\ntask-type: draft\n\n" + FACE.split("\n", 1)[1], plan=plan)
    assert levels(folder_health(plain), "paragraph") == []           # no section_kind: not a paper Section


def test_an_introduction_expect_with_no_evidence_and_a_title_placeholder_warn(tmp_path):
    """JL 261112: "do we really have evidence for this?" and "could you put the title here?"."""
    from src.paragraph_length import title_placeholder, unsupported_expectations
    plan = (HEADER + "\n## 1 · Structure\n\n### C1.P0 · Title · S0\n- B0 · S0 · [Title] The paper's title.\n\n"
            "### C1.P1 · Why · S1 to S4\n- B1 · S1 · [Expect] Large where past readings hold the answer.\n"
            "  Evidence: none · framing\n- B2 · S2 · [Expect] Cited.\n  Evidence: E01-CITE-x\n")
    assert unsupported_expectations(plan) == ["S1"] and title_placeholder(plan) == ["S0"]
    face = "# Sample-Page\ntask-type: draft\nsection_kind: introduction\n\n" + FACE.split("\n", 1)[1]
    folder = make(tmp_path, face=face, plan=plan)
    assert levels(folder_health(folder), "expect") == [WARN] and levels(folder_health(folder), "title") == [WARN]
    results = make(tmp_path / "r", face=face.replace("introduction", "results"), plan=plan)
    assert levels(folder_health(results), "expect") == []           # Results may state what was expected

