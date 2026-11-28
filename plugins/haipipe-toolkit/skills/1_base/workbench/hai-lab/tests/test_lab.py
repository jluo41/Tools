"""cli/lab.py: a theme Block opens as a lab of sessions; a plain Block is refused; nothing is written in the Block."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

LAB = Path(__file__).resolve().parents[1] / "cli" / "lab.py"


def make_space(tmp_path, theme="design", jobs=("j01_first", "j02_second")):
    root = tmp_path / "SPACE"
    (root / ".server_config").mkdir(parents=True)
    (root / ".server_config" / "settings.env").write_text("DOMAIN=space.example.test\n", encoding="utf-8")
    (root / "env.sh").write_text("", encoding="utf-8")
    project = root / "examples" / "Project-Demo"
    project.mkdir(parents=True)
    (project / "project.md").write_text("---\ntitle: Demo\n---\n# Demo\n", encoding="utf-8")
    kind = {"design": "design-board", "insight": "insight-board", "labeling": "task-block", "work": "task-block"}[theme]
    block = project / theme / "b01_demo"
    block.mkdir(parents=True)
    (block / "board.md").write_text(f"---\ntitle: Demo\nboard-kind: {kind}\n---\n# Demo\n", encoding="utf-8")
    for j in jobs:
        (block / j).mkdir()
        (block / j / f"{j}.md").write_text(f"---\ntitle: {j}\n---\n# {j}\n", encoding="utf-8")
    return root, block


def run(root, *args, labs):
    env = {**os.environ, "HAIPIPE_LABS_DIR": str(labs)}
    return subprocess.run([sys.executable, str(LAB), *args, "--root", str(root)], cwd=root, env=env,
                          capture_output=True, text=True)


def test_plan_lists_the_board_and_each_job_and_writes_nothing(tmp_path):
    root, block = make_space(tmp_path)
    before = sorted(p.name for p in block.rglob("*"))
    r = run(root, str(block), "--plan", labs=tmp_path / "labs")
    assert r.returncode == 0, r.stderr
    assert "design lab" in r.stdout
    assert "b01_demo-Board" in r.stdout and "b01_demo-j01" in r.stdout and "b01_demo-j02" in r.stdout
    assert not (tmp_path / "labs").exists()
    assert sorted(p.name for p in block.rglob("*")) == before


def test_no_open_writes_the_lab_outside_the_block_and_keeps_its_ids(tmp_path):
    root, block = make_space(tmp_path, theme="insight")
    labs = tmp_path / "labs"
    before = sorted(p.name for p in block.rglob("*"))
    assert run(root, str(block), "--no-open", labs=labs).returncode == 0
    out = labs / "Project-Demo--b01_demo"
    ws = json.loads((out / "b01_demo-Lab-A.code-workspace").read_text())
    terms = ws["settings"]["haipipeLab.terminals"]
    assert [t["name"] for t in terms] == ["Board", "j01", "j02"]
    assert terms[1]["url"] == ("http://space.example.test/_board/workbench?"
                               "path=examples/Project-Demo/insight/b01_demo/j01_first&layout=focus")
    assert "lab_launch.py" in terms[0]["command"]
    assert "/hai-insight" in (out / "prompts" / "j01.txt").read_text()
    first = json.loads((out / "sessions.json").read_text())
    assert run(root, str(block), "--no-open", labs=labs).returncode == 0
    assert json.loads((out / "sessions.json").read_text()) == first          # the same sessions next time
    assert sorted(p.name for p in block.rglob("*")) == before                 # the Block is never written


def test_max_keeps_the_newest_jobs_and_windows_hold_four(tmp_path):
    root, block = make_space(tmp_path, jobs=[f"j0{i}_x" for i in range(1, 9)])
    r = run(root, str(block), "--plan", "--max", "6", labs=tmp_path / "labs")
    assert r.returncode == 0, r.stderr
    assert "-j01 " not in r.stdout and "-j04" in r.stdout and "-j08" in r.stdout
    assert "Lab-B" in r.stdout and "Lab-C" not in r.stdout


def test_a_job_path_opens_its_blocks_lab(tmp_path):
    root, block = make_space(tmp_path, theme="labeling")
    r = run(root, str(block / "j01_first"), "--plan", labs=tmp_path / "labs")
    assert r.returncode == 0, r.stderr
    assert "labeling lab" in r.stdout


def test_a_work_block_is_refused_with_its_wb_link(tmp_path):
    root, block = make_space(tmp_path, theme="work")
    r = run(root, str(block), "--plan", labs=tmp_path / "labs")
    assert r.returncode != 0
    assert "/wb examples/Project-Demo/work/b01_demo" in r.stderr


def test_a_question_book_opens_as_an_insight_lab(tmp_path):
    """A Question Book (board-kind: prototype) sits in insight/ and opens on the work page; its lab is an insight lab."""
    root, block = make_space(tmp_path, theme="insight", jobs=("j01_question-v1_basic",))
    book = block.parent / "InsightQuestionBook-Demo"
    book.mkdir()
    (book / "board.md").write_text("---\nboard-kind: prototype\nserves: insight/b01_demo\n---\n# Demo\n", encoding="utf-8")
    (book / "j01_question-v1_basic").mkdir()
    (book / "j01_question-v1_basic" / "j01_question-v1_basic.md").write_text("---\nrelease: question-v1\n---\n# v1\n", encoding="utf-8")
    r = run(root, str(book), "--plan", labs=tmp_path / "labs")
    assert r.returncode == 0, r.stderr
    assert "insight lab" in r.stdout
    assert "InsightQuestionBook-Demo-Board" in r.stdout and "InsightQuestionBook-Demo-j01" in r.stdout
