#!/usr/bin/env python3
"""Build or check QBt1 through the shipping haipipe-view implementation."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys


HERE = pathlib.Path(__file__).resolve().parent
UNIT = HERE.parent
PAGE = UNIT.parent.parent / f"{UNIT.name}.md"


def skill_script() -> pathlib.Path:
    for parent in HERE.parents:
        candidate = parent / "view" / "haipipe-view" / "scripts" / "view.py"
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("cannot locate haipipe-view/scripts/view.py")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--target", type=pathlib.Path)
    args = parser.parse_args()
    command = [sys.executable, str(skill_script()), "build", str(PAGE)]
    if args.check:
        command.append("--check")
    if args.target:
        command += ["--target", str(args.target)]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
