"""insight_ladder's Board data Jobs (ref/dataprep.md; JL 261120): a Board runs a signed prep version of its DataPrep
Block on its own dataset and adds the ready folder as its next data version, as it runs a signed question version on a
data version. `datasource` names the Board's raw export, cut and DataPrep Block; `datajob` opens
`jNN_prep-vK-<slug>_data-vM/`, one Task per step of the prep version (`tNN_<step>/`, the same names), one hard Run each
(`runs/r01_<dataset>/`), whose ticket calls ref/run_prep.py."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from insight_ladder_base import (
    DATAJOB, JOB, PREP, STEP, Plan, front, with_front, runs_readme, face, face_kind, project_of)
import insight_ladder_prep as PR

TICKET = """#!/bin/bash
# run.sh · one hard Run of a Board data Job: this step of the prep version on the Board's dataset (haipipe-insight
# ref/run_prep.py). The same lines in every ticket; the folder name is the Run (r01_<dataset>).
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="$R/.venv/bin/python"; [ -x "$PY" ] || PY=python3
exec "$PY" "$R/Tools/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight/ref/run_prep.py" \\
  "$(cd "$HERE/../.." && pwd)" "$(basename "$HERE")"
"""


def _find(home: Path, ref: str) -> Path | None:
    """A Project- or SPACE-relative path: the first folder above the Project that holds it."""
    return next(((b / ref).resolve() for b in [home, *home.parents] if ref and (b / ref).exists()), None)


def dataprep_of(board: Path) -> Path:
    fm = front(board / "board.md")[0]
    block = _find(project_of(board), str(fm.get("dataprep") or ""))
    if block is None or face_kind(block) != "dataprep":
        sys.exit(f"{board.name} names no DataPrep Block (board.md dataprep:; insight_ladder.py datasource)")
    return block


def datasource(board: Path, raw: str, dataprep: str, cut: str, plan: Plan, params: str = "") -> None:
    """Where a Board's one dataset comes from: its raw export (`raw:`), the cut a step applies (`cut:`), and the
    DataPrep Block whose prep versions it runs (`dataprep:`), and the settings its steps read (`params:`, such as the
    source function: ctx.params). Paths are Project- or SPACE-relative, never absolute."""
    if face_kind(board) != "board":
        sys.exit(f"{board.name} is not an insight Board (board.md board-kind: insight-board)")
    if not raw or not dataprep or raw.startswith("/") or dataprep.startswith("/"):
        sys.exit("a data source is: datasource <Board> --raw <SPACE-relative raw export> --dataprep <DataPrep Block>")
    home = project_of(board)
    if _find(home, raw) is None:
        sys.exit(f"--raw {raw}: not there; a dataset is read from its raw export only (ref/dataprep.md rule 3)")
    block = _find(home, dataprep)
    if block is None or face_kind(block) != "dataprep":
        sys.exit(f"--dataprep {dataprep}: not a DataPrep Block (insight/InsightDataPrep-<Set>/)")
    if block not in [b.resolve() for b in PR.serving(board)]:
        sys.exit(f"{block.name} does not name {board.name} in serves:; add it there first")
    fields, body = front(board / "board.md")
    fields.update({"raw": raw, "dataprep": dataprep})
    for key, given in (("cut", cut), ("params", params)):
        pairs = [kv.split("=", 1) for kv in given.split(",") if "=" in kv]
        if pairs:
            fields[key] = {**(fields.get(key) or {}), **{k.strip(): v.strip() for k, v in pairs}}
    plan.write(board / "board.md", with_front(fields, body), replace=True)


def datajobs(board: Path) -> list[Path]:
    return sorted((p for p in board.iterdir() if p.is_dir() and DATAJOB.match(p.name)),
                  key=lambda p: int(DATAJOB.match(p.name).group(1))) if board.is_dir() else []


def next_number(board: Path) -> int:
    """The next Job number on a Board: question Jobs and data Jobs share one count."""
    nums = [int(m.group(1)) for p in board.iterdir() if p.is_dir() for m in [JOB.match(p.name) or DATAJOB.match(p.name)]
            if m] if board.is_dir() else []
    return max(nums, default=0) + 1


def next_data(board: Path) -> int:
    """The next data version's number: after the Board's versions and any data Job still running toward one."""
    have = [int(re.sub(r"\D", "", str(v.get("version")))) for v in front(board / "board.md")[0].get("versions") or []
            if re.sub(r"\D", "", str(v.get("version")))]
    have += [int(DATAJOB.match(j.name).group(4).split("-v")[1]) for j in datajobs(board)]
    return max(have, default=0) + 1


def datajob(board: Path, pid: str, plan: Plan) -> Path:
    """The next data Job jNN_prep-vK-<slug>_data-vM/: prep-vK, signed, on the Board's dataset; one Task per step."""
    if face_kind(board) != "board":
        sys.exit(f"{board.name} is not an insight Board (board.md board-kind: insight-board)")
    fm = front(board / "board.md")[0]
    if not fm.get("raw"):
        sys.exit(f"{board.name} names no raw export (board.md raw:; insight_ladder.py datasource)")
    block = dataprep_of(board)
    ver = PR.prep_version(block, pid)
    if ver is None:
        sys.exit(f"{pid} is not a prep version of {block.name}")
    if not PR.signed(ver):
        sys.exit(f"{ver.name} is not signed: a person signs a prep version before a Board runs it")
    if str(face(ver).get("hash")) != PR.prep_hash(ver):
        sys.exit(f"{ver.name}'s code changed after its signature (audit hash): restore it, or open the next version")
    n, m = next_number(board), next_data(board)
    slug = PREP.match(ver.name).group(3)
    path = board / (f"j{n:02d}_{pid}" + (f"-{slug}" if slug else "") + f"_data-v{m}")
    dataset = str(fm.get("dataset") or "dataset")
    plan.write(path / f"{path.name}.md", with_front(
        {"prep": pid, "dataprep": fm["dataprep"], "prep-hash": face(ver).get("hash"), "data": f"data-v{m}",
         "raw": fm["raw"], "cut": dict(fm.get("cut") or {}), "params": dict(fm.get("params") or {}), "state": "open",
         "goal": f"{pid} on {dataset}'s raw export: the folder ready for insight that becomes data-v{m}"},
        f"\n# {path.name}\n\nRuns {pid} of `{block.name}` on `{fm['raw']}`, one step a Task, in order; the last step's\n"
        f"folder becomes data-v{m} on this Board once every step has finished (ref/run_prep.py).\n"))
    run = f"r01_{dataset.lower()}"
    for s in PR.steps(ver):
        task = path / s.name
        plan.write(task / f"{task.name}.md", with_front({"step": STEP.match(s.name).group(2),
                                                         "goal": str(face(s).get("goal") or "")}, f"\n# {task.name}\n"))
        plan.write(task / "runs" / run / "run.sh", TICKET)
        if not plan.dry and (task / "runs" / run / "run.sh").exists():
            (task / "runs" / run / "run.sh").chmod(0o755)
        plan.write(task / "runs" / run / "run.yaml", "".join(f"{k}: {v}\n" for k, v in (
            ("run", run), ("kind", "hard"), ("type", "prep"), ("target", task.name), ("prep", pid),
            ("data", f"data-v{m}"), ("status", "planned"))))
    runs_readme(path, "datajob", plan)
    return path


def check_prep(board: Path, pid: str) -> None:
    """A data version named by hand (`data … --prep prep-vK`) names a signed prep version of the Board's DataPrep Block."""
    ver = PR.prep_version(dataprep_of(board), pid)
    if ver is None or not PR.signed(ver):
        sys.exit(f"--prep {pid}: not a signed prep version of {dataprep_of(board).name}")
