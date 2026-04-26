"""Refresh every task-folder inventory figure for a project.

Scans  <project>/tasks/*/build_inventory.py,  runs each builder, then renders
every  *.excalidraw  under  tasks/  to PNG via the shared excalidraw-diagram-skill.

Usage:
  python refresh_all.py                                   # auto-detect from cwd
  python refresh_all.py <project_path>                    # explicit

Example:
  cd examples/ProjC-Model-1-ScalingLaw
  python ../../Tools/plugins/haipipe/skills/haipipe-project/ref/inventory/refresh_all.py

Exits non-zero if any builder or render step fails.  Safe to run unattended.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
RENDER = HERE / "render.py"


def _detect_project(start: Path) -> Path | None:
    """Walk up from  start  looking for a  tasks/  directory."""
    cur = start.resolve()
    for _ in range(6):
        if (cur / "tasks").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", type=Path, nargs="?", default=None,
                    help="Project directory (contains tasks/). "
                         "Defaults to walking up from cwd.")
    args = ap.parse_args()

    project = args.project or _detect_project(Path.cwd())
    if project is None or not (project / "tasks").is_dir():
        print("ERROR: no tasks/ dir found.  "
              "Run from within a project or pass project path explicitly.",
              file=sys.stderr)
        sys.exit(2)

    # Skip symlinked task folders (e.g. backward-compat aliases during renames)
    # — they'd run the same builder twice and produce stale duplicate artefacts.
    tasks = sorted(
        b for b in (project / "tasks").glob("*/build_inventory.py")
        if not b.parent.is_symlink()
    )
    if not tasks:
        print(f"WARNING: no build_inventory.py found under {project}/tasks/*/",
              file=sys.stderr)
        sys.exit(0)

    print(f"Project: {project}")
    print(f"Found {len(tasks)} task-folder builders.\n")

    # ── 1. run each builder ──────────────────────────────────────────────────
    build_failures = 0
    t_build = time.time()
    for b in tasks:
        folder = b.parent.name
        print(f"── build {folder} ──────────────────────────")
        r = subprocess.run([sys.executable, str(b)])
        if r.returncode != 0:
            print(f"!! {folder}: builder exit {r.returncode}")
            build_failures += 1
        print()

    print(f"Build step: {len(tasks) - build_failures}/{len(tasks)} OK  "
          f"({time.time() - t_build:.1f}s)\n")

    # ── 2. render every .excalidraw under tasks/ ─────────────────────────────
    print("── render all ─────────────────────────────")
    t_render = time.time()
    r = subprocess.run(
        [sys.executable, str(RENDER), "--all", str(project / "tasks")],
    )
    render_failed = r.returncode != 0
    print(f"\nRender step: {'FAILED' if render_failed else 'OK'}  "
          f"({time.time() - t_render:.1f}s)")

    # ── exit code ────────────────────────────────────────────────────────────
    if build_failures or render_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
