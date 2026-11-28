"""run_prep.py · run a whole signed prep version, in one Run, on a data version's raw export (ref/dataprep.md; JL 261120).

    python run_prep.py <Job>/t01_prep-vK_<slug> r01_<dataset>    (its ticket, run.sh, calls this)
    python run_prep.py <Job>                                     the same, found from the Job

A Board Job `jNN_data-vM_prep-vK_question-vN/` pins a data version (board.md `versions:`: its `raw:`, `cut:`, `params:`),
a prep version of the Board's DataPrep Block (the Job face's `prep:`, `prep-hash:`) and a question version. Its first
Task `t01_prep-vK_<slug>/` has one hard Run, and this runs every step of the prep version inside it, in order, each
step's `run(ctx)`:

    ctx.raw     the raw export folder            ctx.prev    the earlier step's output (None for the first)
    ctx.out     where this step writes           ctx.refs    {name: path}, the DataPrep Block's references:
    ctx.cut     the data version's cut (a dict)  ctx.params  its params (a dict, such as source_fn)
    ctx.result  this step's light place in the Result (one metrics.json)
    ctx.dataset  ctx.prep  ctx.refuse(reason)    stop here: the Run is refused, with its reason

Where a step writes: the first step `result/steps/<step>/` (the experiment card, rule 7); the last step the ready
folder `<store>/<dataset>_data-vM@prep-vK/` (the DataPrep Block's `store:`); a step between them its heavy folder
under `_WorkSpace/ProjectResult/…/<step>/` (the Result keeps `heavy.yaml`). The Run's Result holds `runtime.yaml` (a
line per step), `provenance/` (the exact scripts and their sha256), the card, each step's light `metrics.json`. When
the last step has finished, the Job face records `ready:`, which the question Runs read (ref/run_job.py).

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
from insight_ladder_base import JOB3, PREPTASK, front, with_front, face  # noqa: E402
import insight_ladder_prep as PR  # noqa: E402
from insight_ladder_prep_checks import DICT_SAMPLE  # noqa: E402

CARD = ("experiment_card.json", "experiment_card.md")
METRICS, METRICS_MAX = "metrics.json", 256 * 1024          # the one file a step may add to its light place (rule 4)


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
    """What one Job of three versions pins, resolved once."""

    def __init__(self, job: Path):
        self.path = job.resolve()
        if not JOB3.match(self.path.name):
            sys.exit(f"{self.path.name} is not a Board Job of three versions (jNN_data-vM_prep-vK_question-vN)")
        self.board = self.path.parent
        self.face = face(self.path)
        self.fm = front(self.board / "board.md")[0]
        self.root = space_root(self.board)
        home = self.board.parent.parent
        self.data = str(self.face.get("data"))
        self.row = next((v for v in self.fm.get("versions") or [] if str(v.get("version")) == self.data), {})
        self.block = _find(home, str(self.face.get("dataprep") or self.fm.get("dataprep") or ""))
        self.pid = str(self.face.get("prep"))
        self.ver = PR.prep_version(self.block, self.pid) if self.block else None
        self.raw = _find(home, str(self.row.get("raw") or ""))
        self.cut, self.params = dict(self.row.get("cut") or {}), dict(self.row.get("params") or {})
        self.dataset = str(self.fm.get("dataset") or "dataset")
        self.task = next((t for t in sorted(self.path.iterdir()) if t.is_dir() and PREPTASK.match(t.name)), None)
        self.run = next(iter(sorted(r for r in (self.task / "runs").glob("r[0-9][0-9]_*") if r.is_dir())), None) \
            if self.task else None
        bfm = front(self.block / "board.md")[0] if self.block else {}
        self.store = self.root / str(bfm.get("store") or "_WorkSpace/stage")
        self.ready = self.store / f"{self.dataset}_{self.data}@{self.pid}"
        self.refs = {str(r.get("name")): _find(self.block.parent.parent, str(r.get("path"))) or self.root / str(r.get("path"))
                     for r in bfm.get("references") or []} if self.block else {}

    def heavy(self, step: Path) -> Path:
        pr = Path(os.environ.get("LOCAL_PROJECT_RESULT") or (self.root / "_WorkSpace" / "ProjectResult"))
        pr = pr if pr.is_absolute() else self.root / pr
        return (pr / self.board.parent.parent.name / self.board.parent.name / self.board.name / self.path.name
                / self.task.name / self.run.name / step.name)


def _gate(job: Job) -> None:
    if job.ver is None:
        raise Refused(f"{job.pid} is not a prep version of the Board's DataPrep Block")
    if not PR.signed(job.ver):
        raise Refused(f"{job.ver.name} is not signed")
    if PR.prep_hash(job.ver) != str(job.face.get("prep-hash")):
        raise Refused(f"{job.ver.name}'s code is not what this Job pinned ({job.face.get('prep-hash')}): open a new Job")
    if not job.row:
        raise Refused(f"{job.data} is not a data version of the Board")
    if job.raw is None or not job.raw.exists():
        raise Refused(f"{job.data}'s raw export is not there ({job.row.get('raw')})")
    stray = PR.undeclared(job.ver, job.cut, job.params)
    if stray:
        raise Refused(f"no step of {job.pid} reads {', '.join(stray)}: a key nobody reads is refused, never ignored")
    mark = job.ready / "made-by.yaml"
    if job.ready.exists() and any(job.ready.iterdir()):
        if not mark.is_file() or (yaml.safe_load(mark.read_text()) or {}).get("job") != job.path.name:
            raise Refused(f"{_rel(job.ready, job.root)} holds another Job's folder")
        shutil.rmtree(job.ready)                                # this Job's own earlier attempt


def _provenance(job: Job, result: Path) -> dict:
    """The exact scripts of every step, and src/, with their sha256: {step: sha256 of its script}."""
    prov = result / "provenance"
    prov.mkdir(parents=True, exist_ok=True)
    files = [PR.script_of(s) for s in PR.steps(job.ver)] + \
        (sorted((job.ver / "src").rglob("*.py")) if (job.ver / "src").is_dir() else [])
    lines = []
    for f in files:
        dst = prov / f.relative_to(job.ver)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        lines.append(f"{_sha(f)}  {f.relative_to(job.ver).as_posix()}")
    (prov / "sha256.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {s.name: _sha(PR.script_of(s)) for s in PR.steps(job.ver)}


def _card_status(run: Path, status: str) -> None:
    card = run / "run.yaml"
    if card.is_file():
        card.write_text(re.sub(r"(?m)^status: .*$", f"status: {status}", card.read_text(encoding="utf-8"), count=1),
                        encoding="utf-8")


def _step(job: Job, i: int, step: Path, result: Path, outs: list) -> dict:
    """One step inside the Run: its out, its light place, its run(ctx), the checks the runner keeps."""
    steps = PR.steps(job.ver)
    light = result / "steps" / step.name
    light.mkdir(parents=True, exist_ok=True)
    out = light if i == 0 else job.ready if i == len(steps) - 1 else job.heavy(step)
    out.mkdir(parents=True, exist_ok=True)
    if i == len(steps) - 1:
        (out / "made-by.yaml").write_text(yaml.safe_dump({"job": job.path.name, "data": job.data, "prep": job.pid}),
                                          encoding="utf-8")
    outs.append(out)
    t0 = time.time()
    line = {"step": step.name, "status": "failed", "out": _rel(out, job.root)}
    try:
        script = PR.script_of(step)
        spec = importlib.util.spec_from_file_location(f"prep_{step.name.replace('-', '_')}", script)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.run(Ctx(raw=job.raw, out=out, prev=outs[i - 1] if i else None, cut=dict(job.cut), params=dict(job.params),
                    refs=job.refs, dataset=job.dataset, prep=job.pid, data=job.data, result=light))
        if i == 0 and not all((out / f).is_file() for f in CARD):
            raise RuntimeError("the first step wrote no experiment card (experiment_card.json and .md; rule 7)")
        if i > 0:
            extra = sorted(p.name for p in light.iterdir() if p.name != METRICS)
            if extra:
                raise RuntimeError(f"a step writes only ctx.out and one light {METRICS}; it also wrote {', '.join(extra)}")
        if (light / METRICS).is_file() and (light / METRICS).stat().st_size > METRICS_MAX:
            raise RuntimeError(f"{METRICS} is light (shapes, counts, checks): under {METRICS_MAX // 1024} KB (rule 4)")
        if i == len(steps) - 1:
            d = out / "data_dictionary.csv"
            if d.is_file() and {h.strip().lower() for h in d.read_text(encoding="utf-8").splitlines()[0].split(",")} & DICT_SAMPLE:
                raise RuntimeError("the ready folder's dictionary holds a sample column: no record value (rule 4)")
        line["status"] = "done"
    except Refused as why:
        line.update(status="refused", reason=str(why))
    except Exception as e:                                       # a script's own failure, kept as its last lines
        line.update(status="failed", reason=f"{type(e).__name__}: {e}", trace=traceback.format_exc().strip().splitlines()[-3:])
    line["seconds"] = round(time.time() - t0, 1)
    return line


def run(job: Job) -> str:
    """The whole prep version in the Job's prep Run: the gates, every step in order, the receipt; `ready:` on success."""
    if job.task is None or job.run is None:
        sys.exit(f"{job.path.name} has no prep Task (t01_prep-vK…) with a Run")
    result = job.run / "result"
    done = yaml.safe_load((result / "runtime.yaml").read_text()) if (result / "runtime.yaml").is_file() else {}
    if (done or {}).get("status") == "done":                    # its ready folder may be read already: never rerun
        print(f"{job.task.name}/{job.run.name}: done already" + (f" (reused {done.get('reused')})" if done.get("reused") else ""))
        return "done"
    if result.exists():
        shutil.rmtree(result)                                   # an earlier attempt that did not finish
    result.mkdir(parents=True)
    receipt = {"status": "failed", "data": job.data, "prep": job.pid, "prep_hash": job.face.get("prep-hash"),
               "raw": job.row.get("raw"), "cut": job.cut, "params": job.params,
               "started": dt.datetime.now().isoformat(timespec="seconds")}
    _card_status(job.run, "running")
    try:
        _gate(job)
        receipt["scripts_sha256"] = _provenance(job, result)
        lines, outs = [], []
        for i, step in enumerate(PR.steps(job.ver)):
            lines.append(_step(job, i, step, result, outs))
            if lines[-1]["status"] != "done":
                break
        receipt["steps"] = lines
        receipt["status"] = lines[-1]["status"] if lines else "failed"
        if lines and lines[-1].get("reason"):
            receipt["reason"] = f"{lines[-1]['step']}: {lines[-1]['reason']}"
        heavy = [o for k, o in enumerate(outs) if 0 < k < len(PR.steps(job.ver)) - 1]
        if heavy:
            (result / "heavy.yaml").write_text(yaml.safe_dump({"heavy": [
                {"dir": _rel(o, job.root), "files": [{"path": _rel(p, o), "bytes": p.stat().st_size}
                                                     for p in sorted(o.rglob("*")) if p.is_file()]} for o in heavy]},
                sort_keys=False), encoding="utf-8")
        if receipt["status"] == "done":
            for f in CARD:                                       # the card at the Result's top, and in the ready folder
                shutil.copy2(outs[0] / f, result / f)
                shutil.copy2(outs[0] / f, job.ready / f)
            receipt["ready"] = _rel(job.ready, job.root) + "/"
            jf, jbody = front(job.path / f"{job.path.name}.md")
            jf["ready"] = receipt["ready"]
            (job.path / f"{job.path.name}.md").write_text(with_front(jf, jbody), encoding="utf-8")
    except Refused as why:
        receipt.update(status="refused", reason=str(why))
    receipt["finished"] = dt.datetime.now().isoformat(timespec="seconds")
    (result / "runtime.yaml").write_text(yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _card_status(job.run, receipt["status"])
    print(f"{job.task.name}/{job.run.name}: {receipt['status']}" + (f" · {receipt.get('reason')}" if receipt.get("reason") else ""))
    return receipt["status"]


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        sys.exit(__doc__.split("\n\n")[1])
    folder = Path(argv[0]).resolve()
    job = Job(folder if JOB3.match(folder.name) else folder.parent)
    return 1 if run(job) == "failed" else 0


if __name__ == "__main__":
    sys.exit(main())
