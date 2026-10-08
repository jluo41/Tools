"""run_job.py <Board Task folder> <rNN_partition> · run one question of a plan-C Job on one partition.

Plan C (b11 s00 · s12 · s13, 261007): an insight Board's Job `jNN_pN_<d>vM/` pins one Prototype release
(board.md `prototype:` + the Job face's `release:`) and one data version (board.md `versions:` + `data:`).
Each of its Tasks `tNN_<L><NN>_<slug>/` is one question; its hard Runs are `runs/rNN_<partition>/`. This is
the one runner of their tickets (`runs/rNN_<partition>/run.sh`, written by open_job.py).

It reads the question and its script from the release (never a copy), the cut from the release's
partitions.md, the extract from the data version, and writes only its Run: `result/` (the tables, their
figures, `runtime.yaml`, the generated `report.md`) and the Run's card `run.yaml`. The statistics, the
power check before any contrast and the gate are run_question.py's, unchanged.

Exit 0 on ok or refused (a refusal is an answer), 1 on failed.
"""
import datetime
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures  # noqa: E402
import run_question as RQ  # noqa: E402

JOB = re.compile(r"^j\d+_(p\d+)_(.+?)(v\d+)$")
TASK = re.compile(r"^t\d+_([DIKW]\d+)_")
RUN = re.compile(r"^r\d{2}_(.+)$")


def _yaml(path):
    return (yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}) if Path(path).is_file() else {}


def version_extract(version: dict, root: Path) -> str:
    """A data version's data file, SPACE-relative: its `extract:`, else found in its `folder:` (the folder of
    the data, JL 261008): the manifest.json's `output_file`, else the one .parquet on top of the folder."""
    if version.get("extract"):
        return str(version["extract"])
    folder = str(version.get("folder") or "").rstrip("/")
    if not folder:
        raise RQ.GateError(f"data version {version.get('version')} names neither folder: nor extract:")
    here = Path(root) / folder
    try:
        named = json.loads((here / "manifest.json").read_text(encoding="utf-8")).get("output_file") or ""
    except (OSError, ValueError):
        named = ""
    found = [p.name for p in sorted(here.glob("*.parquet"))]
    pick = named if named in found else (found[0] if len(found) == 1 else "")
    if not pick:
        raise RQ.GateError(f"{folder}/ holds {len(found)} .parquet files and no manifest.json output_file names one")
    return f"{folder}/{pick}"


def resolve(task, stem):
    """Board Task + rNN_<partition> → everything the run needs, from the names and the faces."""
    task = Path(task).resolve()
    job, board = task.parent, task.parent.parent
    project = board.parent.parent
    jm = JOB.match(job.name)
    jface, _ = RQ.front(job / f"{job.name}.md")
    bface, _ = RQ.front(board / "board.md")
    tface, _ = RQ.front(task / f"{task.name}.md")
    qid = tface.get("question") or (TASK.match(task.name).group(1) if TASK.match(task.name) else "")
    rel = jface.get("release") or (jm.group(1) if jm else "")
    data = jface.get("data") or (jm.group(3) if jm else "")
    proto = project / str(bface.get("prototype", ""))
    rdir = next((p for p in sorted(proto.glob("j*_*")) if p.is_dir()          # jNN_pN or jNN_pN_<slug>
                 and re.match(rf"^j\d+_{rel}(_.+)?$", p.name)), None)
    if rdir is None:
        raise RQ.GateError(f"no release {rel} in {proto}")
    row = (_yaml(rdir / "release.yaml").get("questions") or {}).get(qid)
    if not row:
        raise RQ.GateError(f"{qid} is not in release {rel}")
    qfolder = (rdir / row["task"]).resolve()
    version = next((v for v in bface.get("versions") or [] if v.get("version") == data), None)
    if not version:
        raise RQ.GateError(f"no data version {data} in {board.name}/board.md versions:")
    m = RUN.match(stem)
    if not m:
        raise RQ.GateError(f"{stem} is not rNN_<partition>")
    partitions = RQ.front(rdir / "partitions.md")[0]["partitions"]
    part = next((p for p in partitions if p["name"] == m.group(1)), None)
    if part is None:
        raise RQ.GateError(f"{m.group(1)} is not a cut of release {rel}")
    q, _ = RQ.front(qfolder / RQ.QFILE)
    if q.get("id") != qid:
        raise RQ.GateError(f"{qfolder.name}/{RQ.QFILE}: id {q.get('id')!r} is not {qid}")
    if part["name"] not in RQ.asked_partitions(q, partitions):
        raise RQ.GateError(f"{qid} is not asked on {part['name']}")
    scripts = qfolder / "scripts"
    return dict(task=task, job=job, board=board, release=rel, rdir=rdir, data=data, dataset=f"{bface.get('dataset', '')}{data}",
                extract=version_extract(version, RQ.space_root(task)), qfolder=qfolder, qfile=qfolder / RQ.QFILE, q=q, qid=qid, scripts=scripts,
                script=RQ.entry_script(scripts, qid), partitions=partitions, part=part, run=stem, block=job)


class Ctx(RQ.Ctx):
    def result(self, qid, name, partition=None):
        """Another question's result in this Job, on the same partition (or full from a cross run)."""
        part = partition or (self.partition if self.partition != "cross" else "full")
        hits = [t for t in sorted(self.block.glob(f"t*_{qid}_*")) if t.is_dir()]
        runs = [r for t in hits for r in sorted((t / "runs").glob(f"r[0-9][0-9]_{part}"))]
        if len(runs) != 1:
            raise RQ.GateError(f"no single run of {qid} on {part} in {self.block.name}")
        out = runs[0] / "result"
        path, rec = out / name, out / "runtime.yaml"
        if not path.is_file() or _yaml(rec).get("status") != "ok":
            raise RQ.GateError(f"{qid} has no ok result {name} on {part}; run it first")
        self.reads[path.resolve().relative_to(RQ.space_root(path)).as_posix()] = RQ.file_sha(path)
        return pd.read_csv(path) if name.endswith(".csv") else json.loads(path.read_text())


def _imports(r):
    src = r["rdir"] / "src"
    return RQ._imported(sorted(r["scripts"].glob("*.py")), [src] if src.is_dir() else [])


def run(task, stem):
    t0 = time.time()
    root = RQ.space_root(task)
    rel = lambda p: str(Path(p).resolve().relative_to(root))
    r = resolve(task, stem)
    rundir = r["task"] / "runs" / stem
    out = rundir / "result"
    card = _yaml(rundir / "run.yaml")
    old = _yaml(out / "runtime.yaml")
    old_sha = old.get("tables_sha256") or RQ.tables_sha(out, r["q"])
    old_since = old.get("content_since") or old.get("ended") if old.get("status") == "ok" else None
    RQ._clear(out)
    shared = [r["rdir"] / "partitions.md", r["rdir"] / "thresholds.yaml"] + _imports(r)
    receipt = {
        "status": "running", "question": r["qid"], "run": stem, "partition": r["part"]["name"],
        "release": r["release"], "data": r["data"], "ticket": rel(rundir / "run.sh"),
        "job": rel(r["job"]), "prototype": rel(r["rdir"]), "extract": r["extract"],
        "spec": rel(r["qfile"]), "spec_sha256": RQ.sha256(r["qfile"]),
        "scripts": rel(r["scripts"]), "scripts_sha256": RQ.sha256(r["scripts"]),
        "shared_sha256": RQ.sha256(*[p for p in shared if p.exists()]),
        "git_sha": subprocess.run(["git", "-C", str(r["task"]), "rev-parse", "--short", "HEAD"],
                                  capture_output=True, text=True).stdout.strip() or "unknown",
        "started": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write = lambda: (out / "runtime.yaml").write_text(yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True))
    write()
    prov = out / "provenance"                          # the exact spec and scripts this run ran
    prov.mkdir()
    shutil.copy2(r["qfile"], prov / r["qfile"].name)
    for f in sorted(r["scripts"].glob("*.py")):
        shutil.copy2(f, prov / f.name)
    partition = r["part"]["name"]
    try:
        thresholds = _yaml(r["rdir"] / "thresholds.yaml")
        for p in (r["rdir"] / "src", r["scripts"]):
            if p.is_dir():
                sys.path.insert(0, str(p))
        mod = {}
        exec(compile(r["script"].read_text(encoding="utf-8"), str(r["script"]), "exec"), mod)
        members = [p for p in r["partitions"] if p["name"] in r["part"]["of"]] if partition == "cross" else [r["part"]]
        pw = (r["q"].get("partitions") or {}).get("power") or {}
        filt = {c["column"] for p in members for c in (p.get("where") or [])}
        extra = ({pw.get("outcome"), pw.get("groups")} - {None}) if isinstance(pw, dict) else set()
        want = mod.get("COLUMNS") or []
        if want == "none":
            full, read_cols = pd.DataFrame(), []
            frames = {p["name"]: full for p in members}
        else:
            read_cols = None if want == "all" else sorted(set(want) | filt | extra)
            full = pd.read_parquet(root / r["extract"], columns=read_cols)
            read_cols = list(full.columns)
            frames = {p["name"]: RQ.apply_filter(full, p)[0] for p in members}
        receipt.update(rows_before=len(full), rows_after=sum(len(v) for v in frames.values()))
        prow = RQ.power_rows(r["q"], frames, thresholds)
        pd.DataFrame(prow).to_csv(out / "partition_power.csv", index=False)
        receipt["power"] = "low" if any(not x["answerable"] for x in prow) else "ok"
        weak = [x for x in prow if not x["answerable"]]
        if weak:
            raise RQ.Refused("underpowered: " + "; ".join(f"{x['partition']} MDE {x['mde']:.2f} > {x['effect']}" for x in weak))
        df = frames[partition] if partition != "cross" else None
        ctx = Ctx(r, df, thresholds, partitions=frames if df is None else None, extract=root / r["extract"])
        ctx.full = full if df is None else None
        tables = mod["run"](df, ctx)
        if ctx.reads:
            receipt["reads"] = ctx.reads
        RQ.gate(tables, r["q"], read_cols, frames)
        for f, t in tables.items():
            if f.endswith(".csv"):
                t.to_csv(out / f, index=False)
            else:
                (out / f).write_text(json.dumps(t, indent=2, default=str))
        receipt.update(status="ok", outputs=sorted(tables) + ["partition_power.csv"])
        receipt["figures"] = figures.draw(out, RQ.live_needs(r["q"]))
        receipt["tables_sha256"] = RQ.tables_sha(out, r["q"])
    except RQ.Refused as e:
        receipt.update(status="refused", reason=str(e))
    except Exception as e:  # noqa: BLE001 · every failure is written into the receipt
        receipt.update(status="failed", problem=f"{type(e).__name__}: {e}")
    receipt.update(ended=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   duration_s=round(time.time() - t0, 1))
    same = receipt["status"] == "ok" and old_since and receipt.get("tables_sha256") == old_sha
    receipt["content_since"] = old_since if same else receipt["ended"]
    write()
    RQ.write_report(r, receipt, out, out)                    # the generated report, beside its results
    report = out / "report.md"
    report.write_text(report.read_text(encoding="utf-8").replace(f"../../results/{stem}/", "")
                      .replace("ref/run_question.py", "ref/run_job.py"), encoding="utf-8")
    card.update(run=stem, kind="hard", type="cross" if partition == "cross" else "partition", partition=partition,
                target=r["task"].name, question=r["qid"], release=r["release"], data=r["data"],
                script=receipt["scripts_sha256"][:12], n=receipt.get("rows_after", "—"), power=receipt.get("power", "—"),
                status=receipt["status"], passes=int(card.get("passes") or 0) + 1, ticket=receipt["ticket"])
    (rundir / "run.yaml").write_text(yaml.safe_dump(card, sort_keys=False, allow_unicode=True))
    print(f"{r['qid']} · {stem}: {receipt['status']}"
          + (f" · {receipt.get('reason') or receipt.get('problem')}" if receipt["status"] != "ok" else ""))
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(0 if run(sys.argv[1], sys.argv[2])["status"] in ("ok", "refused") else 1)
