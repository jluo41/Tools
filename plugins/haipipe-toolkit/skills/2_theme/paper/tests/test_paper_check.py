"""haipipe-paper's checklist, ticked from a made-up paper Board's own files (JL 261031)."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "haipipe-paper" / "scripts"))
import paper_check  # noqa: E402


def test_a_new_board_shows_each_layer_and_what_waits():
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "Project-X"
        (project / "work" / "b11_x_did").mkdir(parents=True)
        board = project / "paper" / "Paper-X"
        board.mkdir(parents=True)
        (board / "board.md").write_text("# X\n\nspine: one question\nclose: sent\nstory-current: s02-story-x\n"
                                        "Runs: ../../work/b11_x_did/\n", encoding="utf-8")
        (board / "s02-story-x").mkdir()
        (board / "s02-story-x" / "s02-story-x.md").write_text("# story\n\n**G0:** ⬜ not chosen yet\n", encoding="utf-8")
        for j in ("j01_evidence_display", "j02_evidence_value", "j03_evidence_cite"):
            (board / j).mkdir()
        sec = board / "j11_writing_v1130_venue" / "t01_intro" / "draft"
        sec.mkdir(parents=True)
        (sec / "t01_intro-draft-v0.1.md").write_text("approved: ⬜\n\nA ⟦placeholder⟧ sentence.\n", encoding="utf-8")
        got = {i: (m, seen) for _, i, _, m, seen in paper_check.check(board)}
        assert got["P1"][0] == "✅" and got["P3"][0] == "✅" and got["P4"][0] == "🙋"
        assert got["E1"] == ("✅", "b11_x_did") and got["E2"][0] == "⬜"
        assert got["V1"][0] == "✅" and got["W1"][0] == "✅"
        assert got["W2"][0] == "🙋" and got["W3"][0] == "⬜" and got["D11"][0] == "🙋"


def test_layout_and_delivery_lines_and_the_checklist_topic():
    """⓪ Layout says what update fixes; ⑤ Delivery reads the build; --write ticks the sNN-paper-checklist topic."""
    import json
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / "Project-X" / "paper" / "Paper-X"
        (board / "j01_v1130_venue" / "t01_intro").mkdir(parents=True)
        (board / "board.md").write_text("# X\n\nspine: q\nclose: sent\nvenue: Venue\n", encoding="utf-8")
        (board / "venues" / "venue").mkdir(parents=True)
        (board / "venues" / "venue" / "call.md").write_text("| what | limit |\n|---|---|\n| words | up to 3000 | x |\n", encoding="utf-8")
        out = board / "delivery" / "j01_v1130_venue"
        (out / "latex").mkdir(parents=True)
        (out / "latex" / "p.pdf").write_text("x")
        (out / "build-manifest.json").write_text(json.dumps({"outputs": {"pdf": "latex/p.pdf", "docx": "word/p.docx"},
                                                             "build": {"main_text_words": 3400}, "status": "DRAFT",
                                                             "submission_readiness": {"status": "DRAFT", "blockers": ["b"]}}))
        got = {i: (m, seen) for _, i, _, m, seen in paper_check.check(board)}
        assert got["L3"][0] == "⬜" and "j01_v1130_venue" in got["L3"][1]
        assert got["L4"][0] == "⬜"
        assert got["D1"][0] == "⏳" and got["D4"][0] == "⏳" and "3400 words, limit 3000" in got["D4"][1]
        assert got["D7"][0] == "⏳" and got["D10"][0] == "🙋"
        assert got["D8"][0] == "⬜"                                             # no [portal]: no packet
        assert paper_check.write(board, paper_check.check(board)) is None          # no topic yet: nothing written
        t = board / "s05-paper-checklist"
        t.mkdir()
        (t / "s05-paper-checklist.md").write_text("s05 · Paper checklist\n\nabove stays\n", encoding="utf-8")
        f = paper_check.write(board, paper_check.check(board))
        text = f.read_text(encoding="utf-8")
        assert "above stays" in text and paper_check.GENERATED in text and "### ⑤ Delivery" in text
        paper_check.write(board, paper_check.check(board))                       # a rerun replaces, never stacks
        assert f.read_text(encoding="utf-8").count(paper_check.GENERATED) == 1


def test_update_dry_run_names_each_step_and_changes_nothing():
    import io
    import contextlib
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "haipipe-paper" / "scripts"))
    import paper_ladder
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / "Project-X" / "paper" / "Paper-X"
        (board / "j01_v1130_venue").mkdir(parents=True)
        (board / "j11_writing_v1201_venue").mkdir()
        (board / "board.md").write_text("# X\n\nj01_v1130_venue is the send\n", encoding="utf-8")
        before = sorted(p.name for p in board.iterdir())
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            paper_ladder.update(board, "", dry=True)
        said = buf.getvalue()
        assert "j01_v1130_venue -> j12_writing_v1130_venue" in said          # j11 is taken; a current one is left alone
        assert "j11_writing_v1201_venue ->" not in said
        assert "the checklist topic" in said and "the evidence Jobs" in said
        assert sorted(p.name for p in board.iterdir()) == before


def test_update_keeps_a_writing_number_and_sweeps_whole_names_only():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "haipipe-paper" / "scripts"))
    import paper_ladder
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / "Project-X" / "paper" / "Paper-X"
        (board / "j12_v0101_desk").mkdir(parents=True)
        (board / "j12_v0101_desk" / "j12_v0101_desk.md").write_text("# j12\n", encoding="utf-8")
        (board / "delivery" / "j12_v0101_desk").mkdir(parents=True)
        (board / "delivery" / "j12_v0101_desk" / "paper-build.toml").write_text('main = "../../j12_v0101_desk"\n', encoding="utf-8")
        (board / "board.md").write_text("# X\n\nj12_v0101_desk and j12_v0101_desk-letter\n", encoding="utf-8")
        paper_ladder.update(board, "", dry=False)
        assert (board / "j12_writing_v0101_desk" / "j12_writing_v0101_desk.md").is_file()     # number and face kept
        assert '"../../j12_writing_v0101_desk"' in (board / "delivery" / "j12_writing_v0101_desk" / "paper-build.toml").read_text()
        assert "j12_writing_v0101_desk and j12_v0101_desk-letter" in (board / "board.md").read_text()
        paper_ladder.rollback_update(board)
        assert (board / "j12_v0101_desk" / "j12_v0101_desk.md").is_file()
        assert "j12_v0101_desk and j12_v0101_desk-letter" in (board / "board.md").read_text()


def test_l6_each_job_says_its_use_and_update_writes_it():
    """L6 (b16 Job UI, JL 261108): every Job face carries the use-case: line the workbench shows and never guesses;
    update writes the matrix's word, under the H1, and its rollback takes it back out."""
    import io
    import contextlib
    import paper_ladder
    faces = {"j01_evidence_display": "layer: evidence\n", "j02_evidence_value": "layer: evidence\n",
             "j03_evidence_cite": "layer: evidence\n", "j11_writing_v1130_desk": "from: none (the first send)\n",
             "j12_writing_v0215_desk": "from: j11_writing_v1130_desk\n", "j13_writing_v0401_desk": "responds-to: reports/q01/q01.md\n",
             "j21_submission_v1130_desk": "layer: submission\n", "j51_insight_demo": "from: a meeting\n"}
    want = {"j01_evidence_display": "Figure and table preparation", "j02_evidence_value": "Printed-value verification",
            "j03_evidence_cite": "Citation verification", "j11_writing_v1130_desk": "Manuscript drafting",
            "j12_writing_v0215_desk": "Manuscript drafting", "j13_writing_v0401_desk": "Feedback revision",
            "j21_submission_v1130_desk": "Submission package preparation", "j51_insight_demo": ""}
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / "Project-X" / "paper" / "Paper-X"
        board.mkdir(parents=True)
        (board / "board.md").write_text("# X\n\nboard-kind: paper-board\n", encoding="utf-8")
        (board / "s05-paper-checklist").mkdir()
        for name, head in faces.items():
            (board / name).mkdir()
            (board / name / f"{name}.md").write_text(f"# {name} · a Job\n\n{head}\n## Tasks\n", encoding="utf-8")
        assert {j.name: w for j, w in paper_check.jobs_without_use_case(board)} == want
        rows = {i: m for _, i, _, m, _ in paper_check.layout(board, None)}
        assert rows["L6"] == "🙋"                                                # j51 is no version: a person says it
        with contextlib.redirect_stdout(io.StringIO()):
            paper_ladder.update(board, "", dry=True)
        assert paper_check.jobs_without_use_case(board)                       # the dry run wrote nothing
        with contextlib.redirect_stdout(io.StringIO()):
            paper_ladder.update(board, "", dry=False)
        assert (board / "j51_insight_demo" / "j51_insight_demo.md").read_text(encoding="utf-8").count("use-case") == 0
        (board / "j51_insight_demo" / "j51_insight_demo.md").write_text("# j51\n\nuse-case: Demo\n", encoding="utf-8")
        for name, word in want.items():
            if not word:
                continue
            text = (board / name / f"{name}.md").read_text(encoding="utf-8")
            assert text.startswith(f"# {name} · a Job\n\nuse-case: {word}\n")
        assert {i: m for _, i, _, m, _ in paper_check.layout(board, None)}["L6"] == "✅"
        with contextlib.redirect_stdout(io.StringIO()):
            paper_ladder.rollback_update(board)
        assert len(paper_check.jobs_without_use_case(board)) == len(want) - 1     # j51's own line, a person's, stays


def test_put_use_case_replaces_a_line_already_there():
    text = "# j11 · v1\n\nuse-case: Manuscript drafting\nsend: j11\n"
    assert paper_check.put_use_case(text, "Feedback revision") == "# j11 · v1\n\nuse-case: Feedback revision\nsend: j11\n"


def test_board_and_task_faces_say_their_use_too():
    """JL 261109 ("there are no page type and use case"): the Board and every Task face carry the line as well, from
    what they declare; a scaffold stamps a new face, a copied face too."""
    cases = [("board.md", "# X\n\nboard-kind: paper-board\n", "Manuscript development"),
             ("board.md", "# X\n\nboard-kind: grant-board\n", "Initial application"),
             ("j11_writing_v0101_x/t00_abstract/t00_abstract.md", "# t\n\nsection_kind: abstract\n", "Abstract or summary"),
             ("j11_writing_v0101_x/t02_methods/t02_methods.md", "# t\n\nsection_kind: methods\n", "Manuscript section"),
             ("j11_writing_v0101_x/t31_letter/t31_letter.md", "# t\n\nsection_kind: letter\n", "Cover letter drafting"),
             ("j12_writing_v0201_x/t32_response/t32_response.md", "# t\n\nsection_kind: letter\nresponds-to: q\n",
              "Reviewer response"),
             ("j01_evidence_display/t01_q00-overview/t01_q00-overview.md", "# t\n\ntype: table\n", "Table preparation"),
             ("j01_evidence_display/t02_q01/t02_q01.md", "# t\n\nlabel: fig:model\n", "Figure preparation"),
             ("j01_evidence_display/t03_q02/t03_q02.md", "# t\n\n", ""),                    # nothing declared: no guess
             ("j02_evidence_value/t99_paper_value_check/t99_paper_value_check.md", "# t\n", "Whole-paper value audit"),
             ("j02_evidence_value/t02_raw-value-tables/t02_raw-value-tables.md", "# t\n", "Source table inspection"),
             ("j03_evidence_cite/t01_cite/t01_cite.md", "# t\n", "Claim-group citation check"),
             ("j21_submission_v0101_x/t02_portal-walk/t02_portal-walk.md", "# t\n", "Portal field survey"),
             ("j51_insight_demo/t01_a/t01_a.md", "# t\n", ""),
             ("j11_writing_v0101_x/notes.md", "# n\n", None)]
    for rel, text, want in cases:
        assert paper_check.face_use(rel, text) == want, rel
    stamped = paper_check.stamp_use_case("j11_writing_v0101_x/t00_abstract/t00_abstract.md", "# t\n\nsection_kind: abstract\n")
    assert stamped == "# t\n\nuse-case: Abstract or summary\nsection_kind: abstract\n"
    kept = "# t\n\nuse-case: Mine\n"
    assert paper_check.stamp_use_case("board.md", kept) == kept


def test_l5_asks_for_the_story_arc_and_the_section_rows():
    """JL 261109: Story by Section opens with the Story arc and tells each Section's part; L5 asks for both, and a new
    Section adds its placeholder row to the version's ## Narrative."""
    import paper_ladder
    with tempfile.TemporaryDirectory() as tmp:
        board = Path(tmp) / "Paper-X"
        v = board / "j11_writing_v0101_x"
        v.mkdir(parents=True)
        face_text = "# v\n\n## Narrative\n\n" + paper_ladder.NARRATIVE_HEAD + "\n## Questions\n"
        (v / "j11_writing_v0101_x.md").write_text(face_text, encoding="utf-8")
        assert not paper_check.section_rows(board, "")
        filled = paper_ladder.narrative_row(face_text, "t01_introduction")
        assert "| t01_introduction | <what the reader asks here> |" in filled
        assert paper_ladder.narrative_row(filled, "t01_introduction") == filled          # one row per Section
        (v / "j11_writing_v0101_x.md").write_text(filled, encoding="utf-8")
        assert not paper_check.section_rows(board, "")                                    # placeholders tell nothing
        (v / "j11_writing_v0101_x.md").write_text(filled.replace("<what the reader asks here>", "Why ask?"), encoding="utf-8")
        assert paper_check.section_rows(board, "")
