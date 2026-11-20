"""run_prep.py · run a signed prep version's steps on a Board's dataset (ref/dataprep.md; JL 261120).

    python run_prep.py <data Task folder> <r01_<dataset>>   one step's Run (its ticket, run.sh, calls this)
    python run_prep.py <data Job folder>                    every step in order, stopping at the first that does not finish

A Board data Job `jNN_prep-vK-<slug>_data-vM/` pins one prep version (its face's `prep:` and `prep-hash:`) of the
Board's DataPrep Block (board.md `dataprep:`) and the Board's raw export (`raw:`, `cut:`). Each Task `tNN_<step>/` is that
version's step of the same name; its one Run calls the step's script, `run(ctx)`:

    ctx.raw    the raw export folder          ctx.prev     the earlier step's output folder (None for the first)
    ctx.out    where this step writes         ctx.refs     {name: path}, the DataPrep Block's references:
    ctx.cut    the Board's cut: (a dict)      ctx.params   the Board's params: (a dict, such as source_fn)
    ctx.dataset  ctx.prep  ctx.result (the Run's result/: a step may add one light metrics.json there)
    ctx.refuse(reason)   stop here: the Run is refused, with its reason

Where a step writes: the first its Run's `result/` (the experiment card, rule 7); the last the ready folder
`<store>/<dataset>@prep-vK` (the DataPrep Block's `store:`); one between them the Run's heavy folder under
`_WorkSpace/ProjectResult` (the Result keeps `heavy.yaml`). The runner writes the Run's `result/runtime.yaml`, its
`result/provenance/` (the exact scripts and their sha256) and the card's status. When the last step has finished, the
ready folder becomes the Board's next data version {version, folder, frozen, prep, made-by}, and the Job closes.

Exit 0 on done or refused (a refusal is an answer), 1 on failed.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import time
import traceback
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from insight_ladder_base import DATAJOB, STEP, front, with_front, face  # noqa: E402
import insight_ladder_prep as PR  # noqa: E402
from insight_ladder_prep_checks import DICT_SAMPLE  # noqa: E402

CARD = ("experiment_card.json", "experiment_card.md")
METRICS, METRICS_MAX = "metrics.json", 256 * 1024          # the one file a step may add to its Result (rule 4)
RUNNER_FILES = {"runtime.yaml", "provenance", "heavy.yaml"}  # what the runner writes there


class Refused(Exception):
    """A step's ctx.refuse(reason), or a gate the runner keeps."""


class Ctx:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def refuse(self, reason: str):
        raise Refused(str(reason))


def _find(home: Path, ref: str) -> Path | None:
    return next(((b / ref).resolve() for b in [home, *home.parents] if ref and (b / ref).exists()), None)


def space_root(board: Path) -> Path:
    """The SPACE: the first folder above the Board holding env.sh (else .server_config)."""
    for marker in ("env.sh", ".server_config"):
        hit = next((a for a in board.parents if (a / marker).exists()), None)
        if hit:
            return hit
    return board.parent.parent.parent


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


class Job:
    """What one data Job pins, resolved once."""

    def __init__(self, job: Path):
        self.path = job.resolve()
        if not DATAJOB.match(self.path.name):
            sys.exit(f"{self.path.name} is not a Board data Job (jNN_prep-vK-<slug>_data-vM)")
        self.board = self.path.parent
        self.face = face(self.path)
        self.fm = front(self.board / "board.md")[0]
        self.root = space_root(self.board)
        home = self.board.parent.parent
        self.block = _find(home, str(self.face.get("dataprep") or self.fm.get("dataprep") or ""))
        self.pid = str(self.face.get("prep"))
        self.ver = PR.prep_version(self.block, self.pid) if self.block else None
        self.raw = _find(home, str(self.face.get("raw") or self.fm.get("raw") or ""))
        self.dataset = str(self.fm.get("dataset") or "dataset")
        pinned = lambda k: (self.face.get(k) if k in self.face else self.fm.get(k)) or {}   # noqa: E731 · the Job's own
        self.cut, self.params = dict(pinned("cut")), dict(pinned("params"))                # values; an older Job: the Board's
        self.tasks = sorted((t for t in self.path.iterdir() if t.is_dir() and STEP.match(t.name)),
                            key=lambda t: int(STEP.match(t.name).group(1)))
        bfm = front(self.block / "board.md")[0] if self.block else {}
        self.store = self.root / str(bfm.get("store") or "_WorkSpace/stage")
        self.refs = {str(r.get("name")): _find(self.block.parent.parent, str(r.get("path"))) or self.root / str(r.get("path"))
                     for r in bfm.get("references") or []} if self.block else {}

    def run_of(self, task: Path) -> Path:
        return next(iter(sorted(r for r in (task / "runs").glob("r[0-9][0-9]_*") if r.is_dir())), task / "runs" / "r01")

    def out_of(self, i: int) -> Path:
        """Where step i writes: the first its result/, the last the ready folder, one between them its heavy folder."""
        task = self.tasks[i]
        run = self.run_of(task)
        if i == 0:
            return run / "result"
        if i == len(self.tasks) - 1:
            return self.store / f"{self.dataset}@{self.pid}"
        pr = Path(os.environ.get("LOCAL_PROJECT_RESULT") or (self.root / "_WorkSpace" / "ProjectResult"))
        if not pr.is_absolute():
            pr = self.root / pr
        return pr / self.board.parent.parent.name / self.board.parent.name / self.board.name / self.path.name / task.name / run.name

    def status(self, task: Path) -> str:
        rt = self.run_of(task) / "result" / "runtime.yaml"
        return str((yaml.safe_load(rt.read_text(encoding="utf-8")) or {}).get("status", "")) if rt.is_file() else ""


def _gate(job: Job, i: int) -> None:
    if job.ver is None:
        raise Refused(f"{job.pid} is not a prep version of the Board's DataPrep Block")
    if not PR.signed(job.ver):
        raise Refused(f"{job.ver.name} is not signed")
    if PR.prep_hash(job.ver) != str(job.face.get("prep-hash")):
        raise Refused(f"{job.ver.name}'s code is not what this Job pinned ({job.face.get('prep-hash')}): open a new data Job")
    stray = PR.undeclared(job.ver, job.cut, job.params)
    if stray:
        raise Refused(f"no step of {job.pid} reads {', '.join(stray)}: a key nobody reads is refused, never ignored")
    if job.raw is None or not job.raw.exists():
        raise Refused("the Board's raw export is not there (board.md raw:)")
    if i > 0 and job.status(job.tasks[i - 1]) != "done":
        raise Refused(f"the earlier step, {job.tasks[i - 1].name}, has not finished")
    if i == len(job.tasks) - 1:
        out = job.out_of(i)
        frozen = {str(v.get("folder") or "").rstrip("/") for v in job.fm.get("versions") or []}
        if _rel(out, job.root) in frozen:
            raise Refused(f"{_rel(out, job.root)} is a data version already, frozen")
        mark = out / "made-by.yaml"
        if out.exists() and any(out.iterdir()):
            if not mark.is_file() or (yaml.safe_load(mark.read_text()) or {}).get("job") != job.path.name:
                raise Refused(f"{_rel(out, job.root)} holds another Job's folder")
            shutil.rmtree(out)                                  # this Job's own earlier attempt, never registered


def _provenance(job: Job, step_dir: Path, script: Path, result: Path) -> str:
    prov = result / "provenance"
    prov.mkdir(parents=True, exist_ok=True)
    lines = []
    for f in [script] + (sorted((job.ver / "src").rglob("*.py")) if (job.ver / "src").is_dir() else []):
        dst = prov / f.relative_to(job.ver)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        lines.append(f"{_sha(f)}  {f.relative_to(job.ver).as_posix()}")
    (prov / "sha256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return _sha(script)


def _card_status(run: Path, status: str) -> None:
    card = run / "run.yaml"
    if card.is_file():
        card.write_text(re.sub(r"(?m)^status: .*$", f"status: {status}", card.read_text(encoding="utf-8"), count=1),
                        encoding="utf-8")


def _register(job: Job, out: Path) -> str:
    """The ready folder becomes the Board's next data version; the Job closes."""
    fields, body = front(job.board / "board.md")
    ver = str(job.face.get("data"))
    if ver in [str(v.get("version")) for v in fields.get("versions") or []]:
        raise Refused(f"{ver} is a data version of the Board already")
    fields.setdefault("versions", []).append({"version": ver, "folder": _rel(out, job.root) + "/",
                                              "frozen": dt.date.today().strftime("%y%m%d"), "prep": job.pid,
                                              "made-by": job.path.name, "new": f"made by {job.pid}"})
    (job.board / "board.md").write_text(with_front(fields, body), encoding="utf-8")
    jf, jbody = front(job.path / f"{job.path.name}.md")
    jf.update(state="closed", made=ver)
    (job.path / f"{job.path.name}.md").write_text(with_front(jf, jbody), encoding="utf-8")
    return ver


def run_step(job: Job, task: Path) -> str:
    """One step's Run: the gates, the step's run(ctx), the checks the runner keeps, the receipt."""
    i = job.tasks.index(task)
    run = job.run_of(task)
    result = run / "result"
    result.mkdir(parents=True, exist_ok=True)
    started, t0 = dt.datetime.now(), time.time()
    receipt = {"status": "failed", "step": task.name, "prep": job.pid, "prep_hash": job.face.get("prep-hash"),
               "dataset": job.dataset, "started": started.isoformat(timespec="seconds")}
    _card_status(run, "running")
    try:
        _gate(job, i)
        step_dir = job.ver / task.name
        if not step_dir.is_dir():
            raise Refused(f"{job.pid} has no step {task.name}")
        script = PR.script_of(step_dir)
        receipt.update(script=script.name, script_sha256=_provenance(job, step_dir, script, result))
        out = job.out_of(i)
        out.mkdir(parents=True, exist_ok=True)
        if i == len(job.tasks) - 1:
            (out / "made-by.yaml").write_text(yaml.safe_dump({"job": job.path.name, "prep": job.pid}), encoding="utf-8")
        receipt["out"] = _rel(out, job.root)
        spec = importlib.util.spec_from_file_location(f"prep_step_{task.name.replace('-', '_')}", script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        receipt["params"] = job.params
        mod.run(Ctx(raw=job.raw, out=out, prev=job.out_of(i - 1) if i else None, cut=dict(job.cut), params=dict(job.params),
                    refs=job.refs, dataset=job.dataset, prep=job.pid, result=result))
        if i > 0:                                                # result/ is the runner's, and one light metrics.json
            extra = sorted(p.name for p in result.iterdir() if p.name not in RUNNER_FILES | {METRICS})
            if extra:
                raise RuntimeError(f"a step writes only ctx.out and one light result/{METRICS}; it also wrote "
                                   f"{', '.join(extra)} (rule 4)")
        if (result / METRICS).is_file() and (result / METRICS).stat().st_size > METRICS_MAX:
            raise RuntimeError(f"result/{METRICS} is light (shapes, counts, checks): under {METRICS_MAX // 1024} KB (rule 4)")
        if i == 0 and not all((out / f).is_file() for f in CARD):
            raise RuntimeError("the first step wrote no experiment card (experiment_card.json and .md; rule 7)")
        if i == len(job.tasks) - 1:
            d = out / "data_dictionary.csv"
            if d.is_file() and {h.strip().lower() for h in d.read_text(encoding="utf-8").splitlines()[0].split(",")} & DICT_SAMPLE:
                raise RuntimeError("the ready folder's dictionary holds a sample column: no record value (rule 4)")
        if 0 < i < len(job.tasks) - 1:
            files = [p for p in sorted(out.rglob("*")) if p.is_file()]
            (result / "heavy.yaml").write_text(yaml.safe_dump(
                {"heavy_dir": _rel(out, job.root), "files": [{"path": _rel(p, out), "bytes": p.stat().st_size}
                                                             for p in files]}, sort_keys=False), encoding="utf-8")
        receipt["status"] = "done"
        if i == len(job.tasks) - 1:
            for f in CARD:                                       # the ready folder carries its experiment card
                if (job.out_of(0) / f).is_file():
                    shutil.copy2(job.out_of(0) / f, out / f)
            receipt["data_version"] = _register(job, out)
    except Refused as why:
        receipt.update(status="refused", reason=str(why))
    except Exception as e:                                       # a script's own failure, kept as its last line
        receipt.update(status="failed", reason=f"{type(e).__name__}: {e}",
                       trace=traceback.format_exc().strip().splitlines()[-3:])
    receipt.update(finished=dt.datetime.now().isoformat(timespec="seconds"), seconds=round(time.time() - t0, 1))
    (result / "runtime.yaml").write_text(yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _card_status(run, receipt["status"])
    print(f"{task.name}/{run.name}: {receipt['status']}" + (f" · {receipt.get('reason')}" if receipt.get("reason") else ""))
    return receipt["status"]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        sys.exit(__doc__.split("\n\n")[1])
    folder = Path(argv[0]).resolve()
    if DATAJOB.match(folder.name):                              # the whole chain, in order
        job = Job(folder)
        for task in job.tasks:
            if job.status(task) == "done":
                continue
            if run_step(job, task) != "done":
                return 0 if job.status(task) == "refused" else 1
        return 0
    job = Job(folder.parent)
    status = run_step(job, folder)
    return 1 if status == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
