#!/usr/bin/env python3
"""Execute a Python source and convert it, preserving every attempt separately.

This helper records an execution Step. It does not allocate a haipipe Run or
close a caller's Run. --run-id only links an identity supplied by that owner.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import uuid


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_receipt(path: Path, record: dict) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", type=Path)
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--python", default=sys.executable,
                        help="Verified Python interpreter for the script and converter")
    parser.add_argument("--run-id", help="Existing caller-owned Run ID, if one exists")
    args = parser.parse_args()
    script = args.script.expanduser().resolve()
    project = args.project_dir.expanduser().resolve()
    interpreter = shutil.which(args.python)
    if not script.is_file() or script.suffix != ".py":
        parser.error("script must name an existing .py file")
    if not project.is_dir():
        parser.error("--project-dir must name an existing directory")
    if interpreter is None:
        parser.error("--python must name an executable Python interpreter")
    interpreter = str(Path(interpreter).resolve())

    execution_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S")
    execution_id += "-" + uuid.uuid4().hex
    attempt = args.output_root.expanduser().resolve() / execution_id
    attempt.mkdir(parents=True, exist_ok=False)
    artifacts = attempt / "artifacts"
    artifacts.mkdir()
    notebook = attempt / (script.stem + ".ipynb")
    receipt = attempt / "execution.json"
    record = {
        "schema": "haipipe.notebook-execution/v1",
        "execution_id": execution_id,
        "run_id": args.run_id,
        "target": str(script),
        "action": "execute-and-convert",
        "project_dir": str(project),
        "python": interpreter,
        "started": stamp(),
        "ended": None,
        "status": "running",
        "exit_code": None,
        "artifacts": str(artifacts),
        "notebook": None,
        "steps": [],
    }
    write_receipt(receipt, record)
    environment = dict(os.environ, RUN_DIR=str(artifacts))
    converter = Path(__file__).resolve().with_name("convert_to_notebooks.py")
    child = None
    previous_handlers = {}
    interrupted = None

    def interrupt(signum, _frame):
        nonlocal interrupted
        interrupted = signum
        raise KeyboardInterrupt

    code = 1
    try:
        for signum in (signal.SIGINT, signal.SIGTERM):
            previous_handlers[signum] = signal.signal(signum, interrupt)
        for name, command in (
            ("execute", [interpreter, str(script)]),
            ("convert", [interpreter, str(converter), str(script), "-o", str(notebook)]),
        ):
            step = {"name": name, "status": "running", "exit_code": None,
                    "log": str(attempt / (name + ".log"))}
            record["steps"].append(step)
            write_receipt(receipt, record)
            with Path(step["log"]).open("w", encoding="utf-8") as log:
                child = subprocess.Popen(command, cwd=project, env=environment,
                                         stdout=log, stderr=subprocess.STDOUT)
                raw_code = child.wait()
                child = None
            code = raw_code if raw_code >= 0 else 128 - raw_code
            step.update(status="complete" if code == 0 else "failed", exit_code=code)
            write_receipt(receipt, record)
            if code:
                break
        record["status"] = "complete" if code == 0 else "failed"
        if code == 0:
            record["notebook"] = str(notebook)
    except KeyboardInterrupt:
        code = 128 + (interrupted or signal.SIGINT)
        record["status"] = "interrupted"
    except Exception as exc:
        code = 1
        record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    finally:
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)
        if child is not None and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
        for step in record["steps"]:
            if step["status"] == "running":
                step.update(status=record["status"], exit_code=code)
        record.update(ended=stamp(), exit_code=code)
        write_receipt(receipt, record)
    print(json.dumps({"status": record["status"], "receipt": str(receipt),
                      "notebook": record["notebook"]}))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
