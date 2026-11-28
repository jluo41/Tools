"""D6: a Task's draft-bibliography must be its own bibex (pp-LBP-JAMA 261104)."""
import importlib.util
import os
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "paper_check.py"
spec = importlib.util.spec_from_file_location("paper_check", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def _task(job, name, declared):
    task = job / name
    (task / "draft/evidence/bibex").mkdir(parents=True)
    (task / "draft/evidence/bibex" / f"{name}.bib").write_text("% own")
    (task / f"{name}.md").write_text(f"---\ndraft-bibliography: {declared}\n---\n" if declared else "---\n---\n")
    return task


def test_own_bibex_or_no_field_is_quiet(tmp_path):
    _task(tmp_path, "t01_intro", "draft/evidence/bibex/t01_intro.bib")
    _task(tmp_path, "t02_methods", "")
    assert check.other_bibs(tmp_path) == []


def test_a_frozen_older_copy_is_named(tmp_path):
    task = _task(tmp_path, "t01_intro", "../review-inputs/t01_intro.bib")
    old = tmp_path / "review-inputs/t01_intro.bib"
    old.parent.mkdir()
    old.write_text("% frozen")
    os.utime(old, (1000, 1000))
    assert check.other_bibs(tmp_path) == ["t01_intro reads t01_intro.bib, older than its bibex"]
    os.utime(old, None)
    os.utime(task / "draft/evidence/bibex/t01_intro.bib", (1000, 1000))
    assert check.other_bibs(tmp_path) == ["t01_intro reads t01_intro.bib, not its bibex"]
