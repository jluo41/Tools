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
        assert got["W2"][0] == "🙋" and got["W3"][0] == "⬜" and got["D9"][0] == "🙋"


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
        assert got["D7"][0] == "⏳" and got["D8"][0] == "🙋"
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
