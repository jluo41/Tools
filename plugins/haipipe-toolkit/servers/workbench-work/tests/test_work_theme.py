"""The work theme on the base frame (work_theme.py): what a work Task's Spaces list."""
import tempfile
from pathlib import Path

from live import frame


def test_code_lists_nested_files_but_not_build_leftovers():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        task = root / "Project" / "tasks" / "b01_topic" / "j01_job" / "t01_task"
        for d in ("scripts/config", "scripts/__pycache__", "workflow", "tests"):
            (task / d).mkdir(parents=True)
        (task / "t01_task.md").write_text("# t01 · Task\n")
        (task / "scripts" / "worker.py").write_text("print(1)\n")
        (task / "scripts" / "config" / "defaults.yaml").write_text("a: 1\n")
        (task / "scripts" / "__pycache__" / "worker.cpython-312.pyc").write_bytes(b"\0")
        (task / "workflow" / "plan.yaml").write_text("plan: x\n")
        (task / "tests" / "test_worker.py").write_text("def test(): pass\n")
        html = frame.render(frame.themes()["work"], root, task, "Work Details", "Code")
        for name in ("scripts/worker.py", "scripts/config/defaults.yaml", "workflow/plan.yaml", "tests/test_worker.py"):
            assert name in html
        assert "__pycache__" not in html and ".pyc" not in html
