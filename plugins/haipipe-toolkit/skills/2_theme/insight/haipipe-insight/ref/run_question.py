"""run_question.py <task folder> <run> · run one Insight question on one dataset x partition.

The one runner of every Insight run ticket, `<Block>/jNN_<level>/tNN_<task>/runs/<run>.sh`
(ref/block-contract.md § The run). An Insight Block is a task Block (haipipe-task):
one Job per DIKW level, one Task per question, its spec in `question.md`, its code in
`scripts/`. The run's stem is `<dataset>_<partition>`: the dataset names an extract in
the Block's board.md `datasets:`, the partition a filter in `meta/partitions.md`; there
is no per-run config. It writes a receipt before the work, filters the partition,
checks power BEFORE any outcome contrast, runs the question's script, gates its output
against the spec, writes the tables to results/<run>/, draws their figures beside them
(ref/figures.py), and writes the generated report, the run's report, to
reports/<run>/report.md: per need its plain lead lines, its figures and its tables, rounded.

The receipt's `content_since` is when the spec's tables last changed: a rerun that writes
the same tables keeps it, so a page read and a CHECK made since stay current.

Exit 0 on ok or refused (a refusal is an answer), 1 on failed.
"""
import datetime
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figures  # noqa: E402  (bound before the Block's own src paths join sys.path)

OPS = {
    "eq": lambda s, v: s.eq(v), "ne": lambda s, v: s.ne(v),
    "lt": lambda s, v: s.lt(v), "lte": lambda s, v: s.le(v),
    "gt": lambda s, v: s.gt(v), "gte": lambda s, v: s.ge(v),
    "isin": lambda s, v: s.isin(v), "notin": lambda s, v: ~s.isin(v),
    "notna": lambda s, v: s.notna() if v else s.isna(),
}
META = "meta"                                                                    # partitions, thresholds, meta, status
LEVEL_DIR = {"D": "j01_data", "I": "j02_information", "K": "j03_knowledge", "W": "j04_wisdom"}   # one Job per level
QFOLDER = re.compile(r"^t(\d{2})_([a-z0-9]+(?:_[a-z0-9]+)*)$")                   # t01_extract_shape_and_quality
QFILE = "question.md"                                                            # the question's spec, beside its page
LOCK = "prototype.lock"                                                          # retired; skipped by sha256 if one lingers
Z = {0.80: 0.841621, 0.90: 1.281552}
REPORT_ROWS = 60                                                                 # a table longer than this is cut in the report


class Refused(Exception):
    """A script's probe shows the extract cannot answer; the cell becomes 🚫 <reason>."""


class GateError(Exception):
    pass


# ── reading the boards ───────────────────────────────────────────────────────
def front(path):
    """The YAML block at the top of a markdown file, and the text after it."""
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise GateError(f"{path}: no YAML block between --- lines at the top")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def space_root(start):
    p = Path(start).resolve()
    while p != p.parent and not (p / "env.sh").is_file():
        p = p.parent
    if not (p / "env.sh").is_file():
        raise GateError(f"no env.sh above {start}")
    return p


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256(*paths):
    """One hash over files and folders (names and bytes, __pycache__ and the lock left out)."""
    h = hashlib.sha256()
    for p in paths:
        p = Path(p)
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file() and "__pycache__" not in x.parts
                                               and x.name != LOCK)
        for f in files:
            h.update(f.name.encode())
            h.update(f.read_bytes())
    return h.hexdigest()


def tables_sha(out, q):
    """One digest over the spec's result files as they stand in `out` (None when one is missing)."""
    files = [out / f for f in sorted(expected_outputs(q))]
    return sha256(*files) if files and all(f.is_file() for f in files) else None


def question_folders(block):
    """Every question's task folder tNN_<name> (holding question.md) in its level's Job, climbing order."""
    for level_dir in LEVEL_DIR.values():
        for d in sorted((Path(block) / level_dir).glob("t[0-9][0-9]_*")):
            if d.is_dir() and QFOLDER.match(d.name) and (d / QFILE).is_file():
                yield d


def question_id(task):
    """D01 from a task folder: its Job's level letter and the tNN number (question.md's id must agree)."""
    task = Path(task)
    letter = next((k for k, v in LEVEL_DIR.items() if v == task.parent.name), None)
    m = QFOLDER.match(task.name)
    if not letter or not m:
        raise GateError(f"{task.parent.name}/{task.name} is not jNN_<level>/tNN_<name> of an Insight Block")
    return f"{letter}{m.group(1)}"


def task_folder(block, qid):
    """The task folder of one question id in a Block, or None."""
    hits = [d for d in sorted((Path(block) / LEVEL_DIR.get(qid[:1], "_")).glob(f"t{qid[1:]}_*")) if d.is_dir()]
    return hits[0] if len(hits) == 1 else None


def block_meta(block):
    """The Block's board.md front matter; it must be an Insight task Block."""
    meta, _ = front(Path(block) / "board.md")
    if meta.get("board-kind") != "task-block" or meta.get("workbench") != "insight":
        raise GateError(f"{Path(block).name}/board.md is not board-kind: task-block with workbench: insight")
    if not isinstance(meta.get("datasets"), dict) or not meta["datasets"]:
        raise GateError(f"{Path(block).name}/board.md names no datasets: {{<name>: <extract .parquet>}}")
    return meta


def runs_of(block, partitions):
    """Every possible run stem of the Block: <dataset>_<partition>, datasets in board.md order."""
    return [f"{d}_{p['name']}" for d in block_meta(block)["datasets"] for p in partitions]


def split_run(run, datasets):
    """<dataset>_<partition> → (dataset, partition); the dataset is a board.md name (no underscore)."""
    ds, _, part = str(run).partition("_")
    if ds not in datasets or not part:
        raise GateError(f"{run} is not <dataset>_<partition> with a dataset of board.md ({', '.join(datasets)})")
    return ds, part


IMPORT = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_]\w*)", re.M)


def _imported(files, roots):
    """The shared modules (src/<name>.py or src/<name>/) these files import, and what those import."""
    found, todo = [], list(files)
    while todo:
        f = todo.pop()
        for name in IMPORT.findall(Path(f).read_text(encoding="utf-8")):
            for root in roots:
                for cand in (root / f"{name}.py", root / name):
                    if cand.exists() and cand not in found:
                        found.append(cand)
                        todo += [cand] if cand.is_file() else sorted(cand.rglob("*.py"))
    return sorted(found)


def shared_digest(block, level_dir, scripts, question=None):
    """The sha256 of what a run rests on besides its own files: partitions.md, the src/ modules its scripts
    import, and only the thresholds.yaml sections its code names (a quoted section name, or the top-level
    seed through ctx.seed), so a key added for another question leaves this run current."""
    block = Path(block)
    paths = shared_paths(block, level_dir, scripts)
    files = [f for f in paths if f.name != "thresholds.yaml"]
    text = "".join(Path(f).read_text(encoding="utf-8") for f in
                   sorted(Path(scripts).glob("*.py")) + [f for f in files if f.suffix == ".py"])
    tfile = block / META / "thresholds.yaml"
    th = (yaml.safe_load(tfile.read_text()) or {}) if tfile.is_file() else {}
    powered = isinstance(((question or {}).get("partitions") or {}).get("power"), dict)
    used = {k: v for k, v in th.items() if re.search(rf"[\"']{re.escape(str(k))}[\"']", text)
            or (k == "seed" and ".seed" in text) or (k == "power" and powered)}
    h = hashlib.sha256(sha256(*files).encode())
    h.update(yaml.safe_dump(used, sort_keys=True).encode())
    return h.hexdigest()


def shared_paths(block, level_dir=None, scripts=None):
    """What a script rests on besides its own files: the Block's partitions and thresholds, and the
    shared modules (its Job's src/, the Block's src/) its scripts import. Without `scripts`, every one."""
    block = Path(block)
    others = [block / d / "src" for d in LEVEL_DIR.values() if d != level_dir]       # a later level may reuse an earlier one's
    roots = [r for r in ([block / level_dir / "src"] if level_dir else []) + [block / "src"] + others if r.is_dir()]
    paths = [p for p in (block / META / "partitions.md", block / META / "thresholds.yaml") if p.exists()]
    if scripts is None:
        return paths + roots
    return paths + _imported(sorted(Path(scripts).glob("*.py")), roots)


def asked_partitions(q, partitions):
    """The partitions a question is asked on, in partitions.md order; a retired question, none."""
    if q.get("retired"):
        return []
    asked = (q.get("partitions") or {}).get("asked", "all")
    names = [p["name"] for p in partitions]
    if asked == "all":
        return [n for n in names if n != "cross"]
    if asked == "cross":
        return ["cross"]
    return [n for n in names if n in asked]


def entry_script(scripts_dir, qid):
    """The one script in scripts/ whose SPEC line names the question."""
    hits = [f for f in sorted(Path(scripts_dir).glob("*.py"))
            if re.search(rf'^SPEC\s*=\s*"{re.escape(qid)}"', f.read_text(encoding="utf-8"), re.M)]
    if len(hits) != 1:
        raise GateError(f"{scripts_dir}: expected one script with SPEC = \"{qid}\", found {len(hits)}")
    return hits[0]


def resolve(qfolder, run):
    """Task folder + run stem → everything the run needs, read from the names alone."""
    qfolder = Path(qfolder).resolve()
    qid, level_dir = question_id(qfolder), qfolder.parent.name
    block = qfolder.parents[1]
    meta = block_meta(block)
    dataset, partition = split_run(run, meta["datasets"])
    partitions = front(block / META / "partitions.md")[0]["partitions"]
    part = next((p for p in partitions if p["name"] == partition), None)
    if part is None:
        raise GateError(f"{partition} is not a partition in {block.name}/{META}/partitions.md")
    qfile = qfolder / QFILE
    q, _ = front(qfile)
    if q.get("id") != qid:
        raise GateError(f"{qfolder.name}/{QFILE}: id {q.get('id')!r} is not {qid} (its Job's letter and tNN)")
    if partition not in asked_partitions(q, partitions):
        raise GateError(f"{qid} is not asked on {partition}")
    scripts = qfolder / "scripts"
    return dict(qfolder=qfolder, block=block, extract=meta["datasets"][dataset], level_dir=level_dir,
                dataset=dataset, run=f"{dataset}_{partition}", partitions=partitions, part=part, qid=qid,
                pq_dir=qfolder, qfile=qfile, q=q, scripts=scripts, script=entry_script(scripts, qid))


# ── statistics the scripts share ─────────────────────────────────────────────
def apply_filter(df, part):
    before = len(df)
    for c in part.get("where") or []:
        col = c["column"]
        for op, val in c.items():
            if op != "column":
                df = df[OPS[op](df[col], val)]
    if len(df) == 0:
        raise Refused(f"partition {part['name']} selects no rows")
    return df, before


def wilson(k, n, z=1.959964):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def holm(pvals):
    """Holm-adjusted p values, in the input order."""
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    out, running = [0.0] * len(pvals), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(pvals) - rank) * pvals[i]))
        out[i] = running
    return out


class Ctx:
    def __init__(self, r, df, thresholds, partitions=None, extract=None):
        self.extract = extract
        self.question = r["q"]
        self.qid = r["qid"]
        self.partition = r["part"]["name"]
        self.partitions = partitions
        self.thresholds = thresholds
        self.seed = thresholds.get("seed", 0)
        self._df = df
        self.wilson = wilson
        self.holm = holm
        self.block = r["block"]
        self.dataset = r["dataset"]
        self.reads = {}                                  # result files of other questions this run read

    def result(self, qid, name, partition=None):
        """Another question's result table (csv → DataFrame, json → dict) in this Block, on the same
        dataset: how a Knowledge or Wisdom script reads the level below. Only a result its run wrote with
        status ok is read; the file is recorded in the receipt, so a change to it makes this run STALE."""
        part = partition or (self.partition if self.partition != "cross" else "full")
        task = task_folder(self.block, qid)
        if task is None:
            raise GateError(f"no single task folder for {qid} in {self.block.name}")
        out = task / "results" / f"{self.dataset}_{part}"
        path, rec = out / name, out / "runtime.yaml"
        if not path.is_file() or not rec.is_file() or (yaml.safe_load(rec.read_text()) or {}).get("status") != "ok":
            raise GateError(f"{qid} has no ok result {name} on {self.dataset}_{part}; run it first")
        self.reads[path.resolve().relative_to(space_root(path)).as_posix()] = file_sha(path)
        return pd.read_csv(path) if name.endswith(".csv") else json.loads(path.read_text())

    def constant(self, column, df=None):
        d = self._df if df is None else df
        return d[column].nunique(dropna=False) <= 1

    def refuse(self, reason):
        raise Refused(reason)

    def beside(self, name):
        """A file the extract's preparation wrote beside it (its manifest, its data dictionary)."""
        path = self.extract.parent / name
        if not path.is_file():
            raise GateError(f"no {name} beside the extract")
        return path


def _z(p):
    from statistics import NormalDist
    return NormalDist().inv_cdf(p)


def smallest_effect(pw, thresholds):
    """The smallest effect worth acting on, in percentage points: the board-wide one in
    thresholds.yaml, unless the question overrides it (power.effect, with power.effect_reason)."""
    if pw.get("effect") is not None:
        return float(pw["effect"])
    v = (thresholds.get("power") or {}).get("smallest_effect_pp")
    return None if v is None else float(v)


def power_rows(q, frames, thresholds):
    """partition_power.csv rows, from n and the base rate only: never an outcome contrast."""
    pw = (q.get("partitions") or {}).get("power") or "none"
    rows = []
    for name, df in frames.items():
        row = {"partition": name, "test": pw if isinstance(pw, str) else pw.get("test"), "n": len(df),
               "base_rate": None, "mde": None, "effect": None, "answerable": True}
        if isinstance(pw, dict) and pw.get("test") in ("rate_precision", "two_proportion"):
            effect = smallest_effect(pw, thresholds)
            if effect is None:
                raise GateError(f"no smallest effect: {META}/thresholds.yaml power.smallest_effect_pp is not declared "
                                f"and the question sets no power.effect")
            p = float(df[pw["outcome"]].astype(float).mean())
            za = 1.959964 if pw.get("alpha", 0.05) == 0.05 else abs(_z(pw["alpha"] / 2))
            if pw["test"] == "rate_precision":
                mde = za * math.sqrt(p * (1 - p) / len(df))
            else:
                counts = df[pw["groups"]].dropna().value_counts()
                n_small = int(counts.min()) if len(counts) >= 2 else 0
                zb = Z.get(pw.get("target_power", 0.80), 0.841621)
                mde = (za + zb) * math.sqrt(2 * p * (1 - p) / n_small) if n_small else float("inf")
            row.update(base_rate=p, mde=mde * 100, effect=effect, answerable=mde * 100 <= effect)
        rows.append(row)
    return rows


# ── the gate and the report ──────────────────────────────────────────────────
def live_needs(q):
    """The needs a run and a page answer today: every need not retired (none on a retired question)."""
    if q.get("retired"):
        return {}
    return {nid: n for nid, n in (q.get("needs") or {}).items() if not n.get("retired")}


def expected_outputs(q):
    """{file: its columns (csv, in order) or keys (json, dotted)} over the live compute needs.
    Two needs may write one json file, each naming its keys; a csv is named by one need."""
    out = {}
    for n in live_needs(q).values():
        if n.get("kind") == "compute":
            for f, cols in (n.get("output") or {}).items():
                if f.endswith(".json") and f in out:
                    out[f] = out[f] + [c for c in cols if c not in out[f]]
                else:
                    out[f] = list(cols)
    return out


def flat_keys(d, prefix=""):
    """A json result's keys, nested dicts written as dotted paths (shape.n_rows)."""
    keys = []
    for k, v in d.items():
        if isinstance(v, dict) and v:
            keys += flat_keys(v, f"{prefix}{k}.")
        else:
            keys.append(f"{prefix}{k}")
    return keys


def gate(tables, q, read_cols, frames):
    want = expected_outputs(q)
    problems = []
    if set(tables) != set(want):
        extra, missing = sorted(set(tables) - set(want)), sorted(set(want) - set(tables))
        if extra:
            problems.append(f"files the spec does not name: {', '.join(extra)}")
        if missing:
            problems.append(f"spec files not written: {', '.join(missing)}")
    n_rows = sum(len(d) for d in frames.values())
    keys = {c for d in frames.values() for c in read_cols if c in d and d[c].nunique() > 1000}
    for f, t in tables.items():
        if f not in want:
            continue
        if isinstance(t, pd.DataFrame):
            cols = list(t.columns)
            if cols != want[f]:
                problems.append(f"{f}: columns {cols} are not the spec's {want[f]}")
        elif sorted(flat_keys(t)) != sorted(want[f]):
            problems.append(f"{f}: keys {sorted(flat_keys(t))} are not the spec's {sorted(want[f])}")
        if isinstance(t, pd.DataFrame):
            if keys & set(t.columns):
                problems.append(f"{f}: carries row key column(s) {', '.join(sorted(keys & set(t.columns)))}")
            if n_rows > 50 and len(t) >= n_rows:
                problems.append(f"{f}: one row per input row; a result is aggregate")
    if problems:
        raise GateError("; ".join(problems))


def _cell(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return ""
    if isinstance(v, float):
        v = round(v, 1) if abs(v) >= 1 else round(v, 3)       # the report rounds; results/ keeps every digit
        if float(v).is_integer():
            v = int(v)
    return str(v).replace("|", "/").replace("\n", " ")


def md_table(df, limit=REPORT_ROWS):
    """A markdown table of a result, cut at `limit` rows with the cut said."""
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(_cell(v) for v in r) + " |" for r in df.head(limit).itertuples(index=False)]
    if len(df) > limit:
        lines.append(f"\n({len(df)} rows; the first {limit} are shown, the full table is in results/)")
    return "\n".join(lines)


def write_report(r, receipt, out, rep):
    """reports/<run>/report.md, the run's report: generated from the run, never written by hand
    (AGENTS.md rule 0). The point first (each need's lead lines), then its figures, then its tables."""
    lead = figures.lead
    q, part = r["q"], r["part"]
    status = receipt["status"] + (f" · {receipt.get('reason') or receipt.get('problem')}" if receipt["status"] != "ok" else "")
    figs = {}
    for f in receipt.get("figures") or []:
        if f.get("file"):
            figs.setdefault(f["need"], []).append(f)
    lines = [f"# {r['qid']} · {q.get('name', '')} · {r['run']}".replace(" ·  · ", " · "), "",
             f"**The ask**: {q.get('ask')}", "",
             f"**Run**: {status} · {receipt.get('rows_after', '')} of {receipt.get('rows_before', '')} rows"
             f" · dataset {r['dataset']} · partition {part['name']}" + (f" ({part['plain']})" if part.get("plain") else "")
             + f" · ended {receipt.get('ended', '')}", "",
             "Generated by haipipe-insight ref/run_question.py from this run's results; rerun the ticket "
             f"`{receipt['ticket']}` to change it.", ""]
    if receipt["status"] == "ok":
        for nid, n in live_needs(q).items():
            if n.get("kind") != "compute":
                continue
            lines += [f"## {r['qid']}.{nid} · {n.get('what', '')}", ""]
            said = []
            for f in n.get("output") or {}:
                if f.endswith(".csv") and (out / f).is_file():
                    said += [f"- {x} (`{f}`)" for x in lead(pd.read_csv(out / f))]
            lines += (said + [""]) if said else []
            for fig in figs.get(nid, []):
                lines += [f"![{fig['table']}](../../results/{r['run']}/{fig['file']})", ""]
            lines += [f"**Pass**: {n.get('pass', '')}", ""]
            for f in n.get("output") or {}:
                lines += [f"### {f}", ""]
                if f.endswith(".csv"):
                    lines.append(md_table(pd.read_csv(out / f)))
                else:
                    data = json.loads((out / f).read_text())
                    flat = pd.json_normalize(data, sep=".").iloc[0].to_dict() if data else {}
                    lines.append(md_table(pd.DataFrame([{"key": k, "value": flat.get(k)} for k in n["output"][f]])))
                lines.append("")
    power = out / "partition_power.csv"
    if power.is_file():
        lines += ["## Power, before any contrast", "", md_table(pd.read_csv(power)), ""]
    rep.mkdir(parents=True, exist_ok=True)
    (rep / "report.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _clear(folder):
    """A rerun replaces its result: nothing of an older run survives."""
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)


# ── one run ──────────────────────────────────────────────────────────────────
def run(qfolder, run_stem):
    t0 = time.time()
    root = space_root(qfolder)
    rel = lambda p: str(Path(p).resolve().relative_to(root))
    r = resolve(qfolder, run_stem)
    partition = r["part"]["name"]
    out, rep = r["qfolder"] / "results" / r["run"], r["qfolder"] / "reports" / r["run"]
    old = (yaml.safe_load((out / "runtime.yaml").read_text()) or {}) if (out / "runtime.yaml").is_file() else {}
    old_sha = old.get("tables_sha256") or tables_sha(out, r["q"])
    old_since = old.get("content_since") or old.get("ended") if old.get("status") == "ok" else None
    _clear(out)
    _clear(rep)
    shared = shared_paths(r["block"], r["level_dir"], r["scripts"])
    receipt = {
        "status": "running", "question": r["qid"], "run": r["run"], "dataset": r["dataset"], "partition": partition,
        "ticket": rel(r["qfolder"] / "runs" / f"{r['run']}.sh"),
        "block": rel(r["block"]), "extract": r["extract"],
        "spec": rel(r["qfile"]), "spec_sha256": sha256(r["qfile"]),
        "scripts": rel(r["scripts"]), "scripts_sha256": sha256(r["scripts"]),
        "shared_sha256": shared_digest(r["block"], r["level_dir"], r["scripts"], r["q"]),
        "git_sha": subprocess.run(["git", "-C", str(r["qfolder"]), "rev-parse", "--short", "HEAD"],
                                  capture_output=True, text=True).stdout.strip() or "unknown",
        "started": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    write = lambda: (out / "runtime.yaml").write_text(yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True))
    write()
    prov = out / "provenance"                      # the exact spec and scripts this run ran, for any later diff
    prov.mkdir()
    shutil.copy2(r["qfile"], prov / r["qfile"].name)
    for f in sorted(r["scripts"].glob("*.py")):
        shutil.copy2(f, prov / f.name)
    try:
        tfile = r["block"] / META / "thresholds.yaml"
        thresholds = (yaml.safe_load(tfile.read_text()) or {}) if tfile.is_file() else {}
        others = [r["block"] / d / "src" for d in LEVEL_DIR.values() if d != r["level_dir"]]
        for p in (*others, r["block"] / "src", r["block"] / r["level_dir"] / "src", r["scripts"]):
            if p.is_dir():                                   # the last inserted is searched first: scripts, own level, top
                sys.path.insert(0, str(p))
        mod = {}
        exec(compile(r["script"].read_text(encoding="utf-8"), str(r["script"]), "exec"), mod)
        members = ([p for p in r["partitions"] if p["name"] in r["part"]["of"]] if partition == "cross" else [r["part"]])
        pw = (r["q"].get("partitions") or {}).get("power") or {}
        filt = {c["column"] for p in members for c in (p.get("where") or [])}
        extra = ({pw.get("outcome"), pw.get("groups")} - {None}) if isinstance(pw, dict) else set()
        want_cols = mod.get("COLUMNS") or []
        if want_cols == "none":                     # a script that reads only results (ctx.result): no extract
            full, read_cols = pd.DataFrame(), []
            frames = {p["name"]: full for p in members}
        else:
            read_cols = None if want_cols == "all" else sorted(set(want_cols) | filt | extra)
            full = pd.read_parquet(root / r["extract"], columns=read_cols)
            read_cols = list(full.columns)
            frames = {p["name"]: apply_filter(full, p)[0] for p in members}
        receipt.update(rows_before=len(full), rows_after=sum(len(v) for v in frames.values()))
        prow = power_rows(r["q"], frames, thresholds)
        pd.DataFrame(prow).to_csv(out / "partition_power.csv", index=False)
        weak = [x for x in prow if not x["answerable"]]
        if weak:
            raise Refused("underpowered: " + "; ".join(f"{x['partition']} MDE {x['mde']:.2f} > {x['effect']}" for x in weak))
        df = frames[partition] if partition != "cross" else None
        ctx = Ctx(r, df, thresholds, partitions=frames if df is None else None, extract=root / r["extract"])
        ctx.full = full if df is None else None          # a cross run also reads the whole extract (its reference)
        tables = mod["run"](df, ctx)
        if ctx.reads:
            receipt["reads"] = ctx.reads
        gate(tables, r["q"], read_cols, frames)
        for f, t in tables.items():
            if f.endswith(".csv"):
                t.to_csv(out / f, index=False)
            else:
                (out / f).write_text(json.dumps(t, indent=2, default=str))
        receipt.update(status="ok", outputs=sorted(tables) + ["partition_power.csv"])
        receipt["figures"] = figures.draw(out, live_needs(r["q"]))
        receipt["tables_sha256"] = tables_sha(out, r["q"])
    except Refused as e:
        receipt.update(status="refused", reason=str(e))
    except Exception as e:  # noqa: BLE001 · every failure is written into the receipt
        receipt.update(status="failed", problem=f"{type(e).__name__}: {e}")
    receipt.update(ended=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   duration_s=round(time.time() - t0, 1))
    same = receipt["status"] == "ok" and old_since and receipt.get("tables_sha256") == old_sha
    receipt["content_since"] = old_since if same else receipt["ended"]
    write()
    write_report(r, receipt, out, rep)
    print(f"{r['qid']} · {r['run']}: {receipt['status']}"
          + (f" · {receipt.get('reason') or receipt.get('problem')}" if receipt["status"] != "ok" else ""))
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(0 if run(sys.argv[1], sys.argv[2])["status"] in ("ok", "refused") else 1)
