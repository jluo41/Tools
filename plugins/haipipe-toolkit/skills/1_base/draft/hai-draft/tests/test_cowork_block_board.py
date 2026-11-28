"""A cowork Block (hai-cowork) checks clean: its Jobs are its tree, so ## Pages is optional, a Job face it lists is
not a ghost, and a name not on disk still is (a Project's b12, 261118)."""
import subprocess
import sys
from pathlib import Path

CHECK = Path(__file__).resolve().parents[1] / "cli" / "check.py"


def _run(board: Path) -> str:
    return subprocess.run([sys.executable, str(CHECK), str(board)], capture_output=True, text=True).stdout


def _board(tmp: Path, pages: str) -> Path:
    b = tmp / "b12_x"
    (b / "j00_people").mkdir(parents=True)
    (b / "j00_people" / "j00_people.md").write_text("# j00 · People\n")
    (b / "board.md").write_text("# b12 · X\nboard-kind: cowork-block\nspine: a\nclose: b\n\n## Topic\n\nt\n\n"
                                "## Pipeline\n\np\n" + pages)
    return b


def test_no_pages_section_is_clean(tmp_path):
    out = _run(_board(tmp_path, ""))
    assert "unknown-board-kind" not in out and "board-missing-section" not in out


def test_a_listed_job_face_is_not_a_ghost_but_a_missing_one_is(tmp_path):
    out = _run(_board(tmp_path, "\n## Pages\n\n- j00_people/j00_people.md\n- j09_gone/j09_gone.md\n"))
    assert "j00_people/j00_people.md" not in out and "j09_gone/j09_gone.md" in out
