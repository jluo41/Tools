"""insight_ladder's Board Jobs of three versions (ref/dataprep.md; JL 261120: "please recreate the j02 which has the data
version and dataprep version and the question version. I think it should be three versions").

A data version is the raw data: a raw export with its cut and params, a row of board.md `versions:`
(`data <Board> data-vM --raw … --cut … --param …`). A prep version is the DataPrep Block's code; a question version
the Question Book's. A Job `jNN_data-vM_prep-vK_question-vN/` pins all three. Its first Task `t01_prep-vK_<slug>/`
runs the whole prep version in one hard Run (ref/run_prep.py) and writes the ready folder
`<store>/<dataset>_data-vM@prep-vK/`; the question version's Tasks follow (`tNN+1_<L><NN>_<slug>/`, one place after
their number in the release) and read that folder. One version moves per Job. `datasource` names the DataPrep Block;
`drop-datajob` undoes a Job of the withdrawn shape (`jNN_prep-vK-<slug>_data-vM/`, a Task per step)."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from insight_ladder_base import (
    DATAJOB, JOB, JOB3, PREP, Plan, front, with_front, runs_readme, face, face_kind, project_of, today)
import insight_ladder_prep as PR
import open_job as OJ  # noqa: E402  (ref/, put on the path by insight_ladder_base)

TICKET = """#!/bin/bash
# run.sh · the prep Run of a Board Job: the whole prep version on the data version's raw export (haipipe-insight
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


def _pairs(given: str) -> dict:
    return {k.strip(): v.strip() for k, v in (kv.split("=", 1) for kv in given.split(",") if "=" in kv)}


def dataprep_of(board: Path) -> Path:
    fm = front(board / "board.md")[0]
    block = _find(project_of(board), str(fm.get("dataprep") or ""))
    if block is None or face_kind(block) != "dataprep":
        sys.exit(f"{board.name} names no DataPrep Block (board.md dataprep:; insight_ladder.py datasource)")
    return block


def datasource(board: Path, dataprep: str, plan: Plan, raw: str = "") -> None:
    """The DataPrep Block whose prep versions a Board runs (`dataprep:`); it must name the Board in `serves:`."""
    if face_kind(board) != "board":
        sys.exit(f"{board.name} is not an insight Board (board.md board-kind: insight-board)")
    if raw:
        sys.exit("a data version names its raw export: data <Board> data-v<M> --raw … [--cut …] [--param …]")
    if not dataprep or dataprep.startswith("/"):
        sys.exit("a DataPrep Block is: datasource <Board> --dataprep <Project- or SPACE-relative DataPrep Block>")
    block = _find(project_of(board), dataprep)
    if block is None or face_kind(block) != "dataprep":
        sys.exit(f"--dataprep {dataprep}: not a DataPrep Block (insight/InsightDataPrep-<Set>/)")
    if block not in [b.resolve() for b in PR.serving(board)]:
        sys.exit(f"{block.name} does not name {board.name} in serves:; add it there first")
    fields, body = front(board / "board.md")
    fields["dataprep"] = dataprep
    plan.write(board / "board.md", with_front(fields, body), replace=True)


def raw_version(board: Path, ver: str, raw: str, cut: str, params: str, label: str, new: str, plan: Plan) -> None:
    """A data version as raw data: {version, raw, cut, params, frozen}. A new one is the next number; an older row that
    names no raw export yet (a folder made by hand) gains its raw, cut and params once, and is frozen after."""
    if raw.startswith("/"):
        sys.exit("--raw is SPACE-relative (or through a variable), never absolute")
    if _find(project_of(board), raw) is None:
        sys.exit(f"--raw {raw}: not there; a data version is a raw export that exists")
    fields, body = front(board / "board.md")
    rows = fields.setdefault("versions", [])
    row = next((v for v in rows if str(v.get("version")) == ver), None)
    if row is not None and row.get("raw"):
        sys.exit(f"{ver} names its raw export already, and is frozen; new raw data is the next data version")
    if row is None:
        want = f"data-v{len(rows) + 1}"
        if ver != want:
            sys.exit(f"the next data version is {want}")
        row = {"version": ver, "frozen": today()}
        rows.append(row)
    row.update({"raw": raw, "cut": _pairs(cut), "params": _pairs(params)})
    if label:
        row["label"] = label
    row.setdefault("new", new or "<what is new>")
    plan.write(board / "board.md", with_front(fields, body), replace=True)


def _jobs(board: Path) -> list[Path]:
    """Every Board Job (a question Job, a Job of three versions, a withdrawn data Job), in number order."""
    found = [(int(m.group(1)), p) for p in board.iterdir() if p.is_dir()
             for m in [JOB.match(p.name) or JOB3.match(p.name) or DATAJOB.match(p.name)] if m] if board.is_dir() else []
    return [p for _, p in sorted(found)]


def next_number(board: Path) -> int:
    """The next Job number on a Board: every Job shares one count."""
    return max((int(re.match(r"^j(\d+)_", j.name).group(1)) for j in _jobs(board)), default=0) + 1


def ready_name(dataset: str, data: str, pid: str) -> str:
    """The ready folder a Job's prep Task writes, named by its data and prep versions: <dataset>_data-vM@prep-vK."""
    return f"{dataset}_{data}@{pid}"


def three_job(board: Path, data: str, pid: str, rel: str, rhash: str, plan: Plan) -> Path:
    """The next Job jNN_data-vM_prep-vK_question-vN/: t01_prep-vK_<slug> (the prep version, one Run) and the question
    version's Tasks, one place after their release number. One version moves from the Job before, never two. A ready
    folder another Job already made from the same data and prep version is reused, its prep Task done."""
    fm = front(board / "board.md")[0]
    row = next((v for v in fm.get("versions") or [] if str(v.get("version")) == data), None)
    if row is None or not row.get("raw"):
        sys.exit(f"{data} is not a data version with a raw export (data <Board> {data} --raw …)")
    block = dataprep_of(board)
    ver = PR.prep_version(block, pid)
    if ver is None:
        sys.exit(f"{pid} is not a prep version of {block.name}")
    if not PR.signed(ver):
        sys.exit(f"{ver.name} is not signed: a person signs a prep version before a Board runs it")
    if str(face(ver).get("hash")) != PR.prep_hash(ver):
        sys.exit(f"{ver.name}'s code changed after its signature (audit hash): restore it, or open the next version")
    stray = PR.undeclared(ver, row.get("cut") or {}, row.get("params") or {})
    if stray:
        sys.exit(f"no step of {pid} reads {data}'s {', '.join(stray)} (step.md cut: and params:): fix the data version, "
                 f"or declare the key in the step that reads it")
    jobs = [j for j in _jobs(board) if not DATAJOB.match(j.name)]
    if any(JOB3.match(j.name) and JOB3.match(j.name).group(2, 3, 4) == (data, pid, rel) for j in jobs):
        sys.exit(f"{board.name} already runs {rel} with {pid} on {data}: one Job per three versions")
    prev = jobs[-1] if jobs else None
    moved = "start"
    if prev:
        pf = face(prev)
        changed = [w for w, same in (("data", str(pf.get("data")) == data), ("prep", pf.get("prep") == pid),
                                     ("code", pf.get("release") == rel)) if not same]
        if len(changed) > 1:
            sys.exit(f"one version per Job: {prev.name} ran {pf.get('release')} with {pf.get('prep') or 'no prep'} on "
                     f"{pf.get('data')}; this Job moves {' and '.join(changed)}. Move one first, so each change has one cause")
        moved = changed[0] if changed else "start"
    dataset = str(fm.get("dataset") or "dataset")
    store = str(front(block / "board.md")[0].get("store") or "_WorkSpace/stage").rstrip("/")
    ready = f"{store}/{ready_name(dataset, data, pid)}/"
    reuse = next((j for j in jobs if JOB3.match(j.name) and JOB3.match(j.name).group(2, 3) == (data, pid)
                  and face(j).get("ready")), None)
    n = next_number(board)
    name = f"j{n:02d}_{data}_{pid}_{rel}"
    path = board / name
    if plan.dry:
        plan.made.append(path / f"{name}.md")
        return path
    _, made = OJ.open_job(board, rel, data, previous=prev.name if prev else "", moved=moved, number=n, name=name,
                          shift=1, extra={"prep": pid, "dataprep": fm["dataprep"], "prep-hash": face(ver).get("hash"),
                                          "hash": rhash, **({"ready": face(reuse)["ready"]} if reuse else {})})
    plan.made += made
    slug = PREP.match(ver.name).group(3)
    head = path / (f"t01_{pid}_{slug}" if slug else f"t01_{pid}")
    run = head / "runs" / f"r01_{dataset.lower()}"
    plan.write(head / f"{head.name}.md", with_front(
        {"prep": pid, "data": data, "goal": f"{pid} on {data}'s raw export: the ready folder the questions read"},
        f"\n# {head.name}\n\nEvery step of {pid}, in order, in one Run; it writes `{ready}`, which the question Tasks\n"
        "after it read.\n"))
    plan.write(run / "run.sh", TICKET)
    (run / "run.sh").chmod(0o755)
    card = {"run": run.name, "kind": "hard", "type": "prep", "target": head.name, "prep": pid, "data": data,
            "ready": ready, "status": "done" if reuse else "planned"}
    if reuse:
        card["reuses"] = f"the ready folder {reuse.name} made"
        plan.write(run / "result" / "runtime.yaml", f"status: done\nreused: {ready}\nmade-by: {reuse.name}\n")
    plan.write(run / "run.yaml", "".join(f"{k}: {v}\n" for k, v in card.items()))
    runs_readme(path, "job", plan)
    return path


def check_prep(board: Path, pid: str) -> None:
    """A data version named by hand (`data … --prep prep-vK`) names a signed prep version of the Board's DataPrep Block."""
    ver = PR.prep_version(dataprep_of(board), pid)
    if ver is None or not PR.signed(ver):
        sys.exit(f"--prep {pid}: not a signed prep version of {dataprep_of(board).name}")


def drop_datajob(job: Path, plan: Plan) -> None:
    """Undo a Job of the withdrawn shape (jNN_prep-vK-<slug>_data-vM/): the data version it registered, unless another
    Job reads it; its ready folder, when its made-by.yaml names this Job; and the Job folder itself, when it is still
    there (its name is enough once the folder is gone). Prints what it removes; a dry run removes nothing."""
    job = job.absolute()
    board = job.parent
    if not DATAJOB.match(job.name) or face_kind(board) != "board":
        sys.exit(f"{job.name} is not a Board data Job of the withdrawn shape (jNN_prep-vK-<slug>_data-vM)")
    fields, body = front(board / "board.md")
    rows = [v for v in fields.get("versions") or [] if v.get("made-by") == job.name]
    readers = [j.name for j in _jobs(board) if j != job and str(face(j).get("data")) in [str(r["version"]) for r in rows]]
    if readers:
        sys.exit(f"{', '.join(readers)} read the data version {job.name} made; keep it, or drop those first")
    root = next((a for a in board.resolve().parents if (a / "env.sh").exists()), board.parent.parent.parent)
    gone = []
    for r in rows:
        folder = root / str(r.get("folder") or "").rstrip("/")
        mark = folder / "made-by.yaml"
        if mark.is_file() and job.name in mark.read_text(encoding="utf-8"):
            gone.append(folder)
    word = "would remove" if plan.dry else "removed"
    for r in rows:
        print(f"{word} the data version {r['version']} ({board.name}/board.md versions:)")
    for f in gone + ([job] if job.exists() else []):
        print(f"{word} {f}")
        if not plan.dry:
            shutil.rmtree(f)
    if rows and not plan.dry:
        fields["versions"] = [v for v in fields["versions"] if v not in rows]
        (board / "board.md").write_text(with_front(fields, body), encoding="utf-8")
    if not rows and not job.exists():
        print(f"nothing of {job.name} is left on {board.name}")
