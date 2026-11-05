"""A paper's views while a build runs (Paper-PhyAbsence 261103: the Writing view dropped the connection; 261104: its panel
vanished): the last built files stay, with a note. The Word step keeps a build's outputs (test_latex_room_to_docx.py)."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
for path in (HERE, HERE.parent / "workbench", HERE.parent / "_host"):
    sys.path.insert(0, str(path))

import board_results          # noqa: E402
import paper_version          # noqa: E402


def _version(tmp_path, outputs):
    vdir = tmp_path / "delivery" / "j11_writing"
    vdir.mkdir(parents=True)
    (vdir / "build-manifest.json").write_text(json.dumps({"outputs": outputs}), encoding="utf-8")
    return vdir


def _locked(vdir, pid):
    lock = Path(tempfile.gettempdir()) / f"haipipe-paper-build-{hashlib.sha1(str(vdir.resolve()).encode()).hexdigest()[:12]}.lock"
    lock.write_text(f"build pid {pid} started 2026-11-04 09:35:00\n", encoding="utf-8")
    return lock


def test_a_running_build_keeps_the_last_files_and_says_so(tmp_path):
    vdir = _version(tmp_path, {"pdf": "latex/P.pdf"})
    (vdir / "latex").mkdir()
    (vdir / "latex" / "P.pdf").write_bytes(b"%PDF")
    assert "A build is running" not in board_results._paper_files(vdir, tmp_path)
    lock = _locked(vdir, os.getpid())
    try:
        page = board_results._paper_files(vdir, tmp_path)
        assert "A build is running" in page and "P.pdf" in page
    finally:
        lock.unlink()


def test_a_dead_builds_lock_is_no_running_build(tmp_path):
    vdir = _version(tmp_path, {"pdf": "latex/P.pdf"})
    gone = subprocess.Popen([sys.executable, "-c", ""])
    gone.wait()
    lock = _locked(vdir, gone.pid)
    try:
        assert paper_version.build_running(vdir) is False
    finally:
        lock.unlink()
    assert paper_version.build_running(vdir) is False


def test_the_word_step_alone_shows_nothing_and_never_raises(tmp_path):
    vdir = _version(tmp_path, ["word/P.docx", "word/P-supplement.docx"])
    assert paper_version.built_outputs(vdir) is None
    assert paper_version.paper_rows(vdir, tmp_path) == ""
    assert board_results._paper_files(vdir, tmp_path) == ""


def test_a_finished_build_still_reads(tmp_path):
    vdir = _version(tmp_path, {"pdf": "latex/P.pdf"})
    assert paper_version.built_outputs(vdir) == {"pdf": "latex/P.pdf"}


def test_no_manifest_is_no_outputs(tmp_path):
    assert paper_version.built_outputs(tmp_path) is None


def test_a_word_row_shows_the_adopted_copy_until_the_next_build(tmp_path):
    """word_round.py adopt renames -draft to -v<n> (Paper-PhyAbsence 261104)."""
    vdir = _version(tmp_path, {"docx": "word/P-draft.docx", "docx_pdf": "word/P-draft.pdf"})
    (vdir / "word").mkdir()
    (vdir / "word" / "P-v1.docx").write_bytes(b"x")
    (vdir / "word" / "P-v1.pdf").write_bytes(b"%PDF")
    page = board_results._paper_files(vdir, tmp_path)
    assert "the copy adopted for the round" in page and "P-v1.pdf" in page
    assert "Earlier round" not in page
    (vdir / "word" / "P-draft.docx").write_bytes(b"x")
    (vdir / "word" / "P-draft.pdf").write_bytes(b"%PDF")
    page = board_results._paper_files(vdir, tmp_path)
    assert "the copy adopted for the round" not in page and "Earlier round" in page
