"""project.py audit / update on a scratch SPACE holding every older layout the migration met (fn/update.md)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import project as M  # noqa: E402
import probe_tickets as PT  # noqa: E402

OLD_TICKET = '''#!/bin/bash
set -uo pipefail
fail_shape() { echo "==> BLOCKED: $1" >&2; exit 2; }
TICKET="$(realpath "$0" 2>/dev/null || echo "$0")"
RUNS_DIR="$(cd "$(dirname "$TICKET")" && pwd)"
[ "$(basename "$RUNS_DIR")" = "runs" ] || fail_shape "Ticket must live in a Task Folder's runs/ lane"
TASK_FOLDER="$(cd "$RUNS_DIR/.." && pwd)"
TASK_SEG="$(basename "$TASK_FOLDER")"
JOB_FOLDER="$(cd "$TASK_FOLDER/.." && pwd)"
BLOCK_FOLDER="$(cd "$JOB_FOLDER/.." && pwd)"
TASKS_DIR="$(cd "$BLOCK_FOLDER/.." && pwd)"
[ "$(basename "$TASKS_DIR")" = "tasks" ] || fail_shape "Block must be a direct child of tasks/"
RUN_NAME="$(basename "$TICKET" .sh)"
OUTPUT_ROOT="$JOB_FOLDER"
RESULTS_DIR="$OUTPUT_ROOT/results/$TASK_SEG/$RUN_NAME"
'''
PAPER_TICKET = '''#!/usr/bin/env bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULT_DIR="$TASK_DIR/results/r01_smith2020_demo"
'''
V081_TICKET = '''#!/bin/bash

# Canonical haipipe-task v0.8.1 execution context.
HAIPIPE_JOB_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
HAIPIPE_TASK_NAME="$(basename "$(dirname "$0")")"
HAIPIPE_TASK_DIR="${HAIPIPE_JOB_DIR}/scripts/${HAIPIPE_TASK_NAME}"
HAIPIPE_RUN_NAME="$(basename "$0" .sh)"
HAIPIPE_RESULT_DIR="${HAIPIPE_JOB_DIR}/results/${HAIPIPE_TASK_NAME}/${HAIPIPE_RUN_NAME}"
HAIPIPE_PROJECT_ROOT="$(cd "${HAIPIPE_JOB_DIR}/../../.." && pwd)"
HAIPIPE_WORKSPACE_ROOT="$(cd "${HAIPIPE_PROJECT_ROOT}/../.." && pwd)"

mkdir -p "${HAIPIPE_RESULT_DIR}"
export RESULT_DIR="${HAIPIPE_RESULT_DIR}"
'''


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def old_project(space: Path) -> Path:
    p = space / "examples-9-demo" / "Project-Demo"
    t = p / "tasks/b01_demo/j01_demo/t01_demo"
    write(t / "t01_demo.md", "# t01 · demo\n\nMetrics: [metrics](../results/t01_demo/r01_a/metrics.json)\n")
    write(t / "scripts/config/r01_a.yaml", "notebook: off\n")
    write(t / "runs/r01_a.sh", OLD_TICKET)
    write(p / "tasks/b01_demo/j01_demo/results/t01_demo/r01_a/runtime.yaml", "status: complete\nrun: r01_a\n")
    write(p / "tasks/b01_demo/j01_demo/results/t01_demo/r01_a/metrics.json", "{}\n")
    write(p / "tasks/b01_demo/j01_demo/diagram/01-overview.txt", "a drawing\n")
    write(p / "tasks/b01_demo/studio/01-overview.txt", "BLOCK\n\nPurpose\n  Show every older layout.\n\nContents\n")
    old = p / "tasks/b01_demo/j02_old"
    write(old / "scripts/t01_fit/01_fit.py", "print('fit')\n")
    write(old / "scripts/t01_fit/config/r01_fit.yaml", "a: 1\n")
    write(old / "runs/t01_fit/r01_fit.sh", V081_TICKET)
    (old / "results/t01_fit").mkdir(parents=True)
    d = p / "discoveries/b01_evidence/j01_reading/t01_landscape"
    write(d / "t01_landscape.md", "# t01 · landscape\n")
    write(d / "runs/r01_smith2020_demo.sh", PAPER_TICKET)
    write(d / "results/r01_smith2020_demo/runtime.yaml", "status: complete\n")
    return p


def tree(root: Path) -> list[str]:
    return sorted(str(x.relative_to(root)) for x in root.rglob("*"))


class MigrateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.space = Path(self.tmp.name).resolve()
        write(self.space / "env.sh", "")
        write(self.space / "AGENTS.md", "# demo SPACE\n")
        self.project = old_project(self.space)
        self.cwd = os.getcwd()
        os.chdir(self.space)

    def tearDown(self):
        os.chdir(self.cwd)
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "project.py"), *args], cwd=self.space,
                              capture_output=True, text=True)

    def test_audit_finds_every_step(self):
        steps = set(M.check(self.project).by_step())
        self.assertTrue({"root", "themes", "convert", "runs", "faces"} <= steps, steps)

    def test_update_dry_run_changes_nothing(self):
        before = tree(self.space)
        out = self.run_cli("update", str(self.project))
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(tree(self.space), before)
        for step in ("root", "themes", "convert", "runs", "faces"):
            self.assertIn(step, out.stdout)

    def test_update_apply_leaves_a_clean_project(self):
        out = self.run_cli("update", str(self.project), "--apply", "--state", str(self.space / "_state"))
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        rep = M.check(self.project)
        self.assertEqual([(f.step, f.where, f.what) for f in rep.findings], [])
        p = self.project
        for name in ("work", "discovery", "project.yaml", "README.md"):
            self.assertTrue((p / name).exists(), name)
        self.assertFalse((p / "tasks").exists())
        run = p / "work/b01_demo/j01_demo/t01_demo/runs/r01_a"
        self.assertTrue((run / "result/metrics.json").is_file())
        self.assertTrue((run / "run.yaml").is_file())
        self.assertIn("runs/r01_a/result/metrics.json",
                      (p / "work/b01_demo/j01_demo/t01_demo/t01_demo.md").read_text())
        self.assertTrue((p / "work/b01_demo/j02_old/t01_fit/runs/r01_fit/r01_fit.sh").is_file())
        self.assertTrue((p / "work/b01_demo/board.md").is_file())
        self.assertIn("Show every older layout.", (p / "work/b01_demo/board.md").read_text())
        self.assertTrue((p / "work/b01_demo/j01_demo/studio/01-overview.txt").is_file())
        counts = PT.probe_all(p, quiet=True)
        self.assertEqual(counts["unexpected"], 0, counts)
        self.assertGreaterEqual(counts["resolves"], 3, counts)
        self.assertIn("newly broken 0", out.stdout)

    def test_update_apply_refuses_when_tools_cannot_read_the_new_layout(self):
        real = M.TEMPLATE
        fake = self.space / "old-template.sh"
        fake.write_text("RESULTS_DIR=\"$OUTPUT_ROOT/$TASK_SEG/results/$RUN_NAME\"\n")
        M.TEMPLATE = fake
        try:
            self.assertTrue(M.tools_findings())
        finally:
            M.TEMPLATE = real


if __name__ == "__main__":
    unittest.main()
