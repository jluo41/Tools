"""A Task Block is a Board: Block -> Job group -> Task Page."""
import importlib.util
import subprocess
import sys
from pathlib import Path

from src.common import page_files
from src.parse import parse_dir


ENGINE = Path(__file__).resolve().parents[1]
TASK_CHECKER = ENGINE.parents[1] / "task" / "haipipe-task" / "ref" / "check_task_tree.py"


def _task_check(block):
    spec = importlib.util.spec_from_file_location("task_tree_checker", TASK_CHECKER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check(block)


def _page(title):
    return f"""# {title}
state: 🔴 OPEN
owner: CC
folder-kind: task
task-type: data
task: .

## Opening
This Task tests one bounded computation and keeps its readable interpretation beside the code that produced it.

## Content
### 1 · Result · Current finding
**Division map · evidence path**
```text
input -> computation -> finding
```
The current fixture has not run yet, so the result remains open.

### 2 · Conclusion · Current reading
**Division map · closing path**
```text
finding -> reading -> next run
```
<a id="reading-current"></a>
#### READING · current
| ID | Topic | Verdict Run | Ruling | Meaning |
|---|---|---|---|---|
| R01 | fixture | b03j01t01r01 | unread | establish the fixture result |

answers none
not answered the fixture question
next run b03j01t01r01

## Aims
### A1 · Result
- ⬜ A1.1 · Produce one readable result.
  **Done when:** the result is bound to its full Run address.
  **Now:** no accepted Result exists.
"""


def _board(tmp_path, pages_lines=""):
    block = tmp_path / "b03_result_interpretation"
    block.mkdir()
    (block / "board.md").write_text(
        "# Task Block Board\n"
        "board-kind: task-block\n"
        "spine: Keep executable Tasks readable as one Block.\n"
        "close: Every Task Folder is closed across both faces.\n\n"
        "## Topic\nA Block of two Jobs and their Task Pages.\n\n"
        "## Pipeline\nJobs are Board Groups; Tasks are Pages; Runs remain executions.\n\n"
        "## Pages\n"
        + pages_lines,
        encoding="utf-8",
    )
    for job, label in (("j01_first_job", "First task"), ("j02_second_job", "Second task")):
        task = block / job / "t01_measure_result"
        task.mkdir(parents=True)
        (task / "t01_measure_result.md").write_text(_page(label), encoding="utf-8")
        (task / "scripts").mkdir()
        (task / "runs").mkdir()
    return block


def test_task_block_discovers_tree_as_groups_and_pages(tmp_path):
    block = _board(
        tmp_path,
        "### j01 · First job\nThe first executable question.\n"
        "### j02 · Second job\nThe second executable question.\n",
    )

    meta, pages, warnings = parse_dir(block)

    assert meta["board_kind"] == "task-block"
    assert [page["id"] for page in pages] == ["b03j01t01", "b03j02t01"]
    assert [page["kind"] for page in pages] == ["task", "task"]
    assert [page["group"] for page in pages] == ["j01 · First job", "j02 · Second job"]
    assert [page["folder_kind"] for page in pages] == ["task", "task"]
    assert not [warning for warning in warnings if "not listed" in warning]


def test_task_block_registry_uses_relative_paths_when_basenames_repeat(tmp_path):
    block = _board(
        tmp_path,
        "### j02 · Second job\n"
        "j02_second_job/t01_measure_result/t01_measure_result.md\n"
        "### j01 · First job\n"
        "j01_first_job/t01_measure_result/t01_measure_result.md\n",
    )

    _meta, pages, warnings = parse_dir(block)

    assert [page["id"] for page in pages] == ["b03j02t01", "b03j01t01"]
    assert not warnings


def test_task_block_rejects_ambiguous_bare_task_filename_once(tmp_path):
    block = _board(tmp_path, "t01_measure_result.md\n")

    _meta, pages, warnings = parse_dir(block)

    assert [page["id"] for page in pages] == ["b03j01t01", "b03j02t01"]
    assert warnings == [
        "t01_measure_result.md is ambiguous in a Task Block Board; list its "
        "job/task/page relative path"
    ]


def test_generic_board_does_not_adopt_task_pages(tmp_path):
    block = _board(tmp_path)
    (block / "board.md").write_text(
        (block / "board.md").read_text(encoding="utf-8").replace(
            "board-kind: task-block\n", ""
        ),
        encoding="utf-8",
    )
    assert not list(page_files(block))


def test_task_block_build_emits_job_groups_and_addressed_task_pages(tmp_path):
    block = _board(tmp_path)
    result = subprocess.run(
        [sys.executable, str(ENGINE / "cli" / "build.py"), str(block)],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert (block / "board" / "j01.html").is_file()
    assert (block / "board" / "j01" / "b03j01t01-measure_result.html").is_file()
    index = (block / "board" / "index.html").read_text(encoding="utf-8")
    assert "ALL TASKS" in index
    assert "0/2 tasks closed" in index


def test_task_tree_checker_requires_explicit_task_block_board_head(tmp_path):
    block = _board(tmp_path)
    assert not [finding for finding in _task_check(block) if finding[0] == "S18"]

    (block / "board.md").unlink()
    findings = [finding for finding in _task_check(block) if finding[0] == "S18"]
    assert findings == [
        ("S18", block.name, "canonical Block has no board.md Task Block Board head")
    ]
