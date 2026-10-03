"""run_question.py <Instance question folder> <partition> · run one question on one partition of an Instance.

The one runner of every Instance run ticket, `<question folder>/runs/<partition>.sh`
(ref/prototype-contract.md § The run). It resolves the question folder to its
Instance and Prototype, writes a receipt before the work, filters the partition,
checks power BEFORE any outcome contrast, runs the Instance's own copy of the
question's script, gates its output against the Prototype's spec, writes the
tables to results/<partition>/ and a generated report to reports/<partition>/.

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

OPS = {
    "eq": lambda s, v: s.eq(v), "ne": lambda s, v: s.ne(v),
    "lt": lambda s, v: s.lt(v), "lte": lambda s, v: s.le(v),
    "gt": lambda s, v: s.gt(v), "gte": lambda s, v: s.ge(v),
    "isin": lambda s, v: s.isin(v), "notin": lambda s, v: ~s.isin(v),
    "notna": lambda s, v: s.notna() if v else s.isna(),
}
META = "0-Meta"
RUNG_DIR = {"D": "1-Data", "I": "2-Information", "K": "3-Knowledge", "W": "4-Wisdom"}
QFOLDER = re.compile(r"^([DIKW])(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")           # D01-extract-shape
LOCK = "prototype.lock"
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


def question_folders(board):
    """Every question folder <L><NN>-<name> in its rung folder, in climbing order (Prototype or Instance)."""
    for rung in RUNG_DIR.values():
        for d in sorted((Path(board) / rung).glob("[DIKW][0-9][0-9]-*")):
            if d.is_dir() and QFOLDER.match(d.name):
                yield d


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


def shared_digest(prototype, rung, scripts, question=None):
    """The sha256 of what a run rests on besides its own files: partitions.md, the src/ modules its scripts
    import, and only the thresholds.yaml sections its code names (a quoted section name, or the top-level
    seed through ctx.seed), so a key added for another question leaves this run current."""
    prototype = Path(prototype)
    paths = shared_paths(prototype, rung, scripts)
    files = [f for f in paths if f.name != "thresholds.yaml"]
    text = "".join(Path(f).read_text(encoding="utf-8") for f in
                   sorted(Path(scripts).glob("*.py")) + [f for f in files if f.suffix == ".py"])
    tfile = prototype / META / "thresholds.yaml"
    th = (yaml.safe_load(tfile.read_text()) or {}) if tfile.is_file() else {}
    powered = isinstance(((question or {}).get("partitions") or {}).get("power"), dict)
    used = {k: v for k, v in th.items() if re.search(rf"[\"']{re.escape(str(k))}[\"']", text)
            or (k == "seed" and ".seed" in text) or (k == "power" and powered)}
    h = hashlib.sha256(sha256(*files).encode())
    h.update(yaml.safe_dump(used, sort_keys=True).encode())
    return h.hexdigest()


def shared_paths(prototype, rung=None, scripts=None):
    """What a script rests on besides its own files: the Prototype's partitions and thresholds, and
    the shared modules (rung src/, top src/) its scripts import. Without `scripts`, every shared module."""
    prototype = Path(prototype)
    others = [prototype / d / "src" for d in RUNG_DIR.values() if d != rung]       # a later rung may reuse an earlier one's
    roots = [r for r in ([prototype / rung / "src"] if rung else []) + [prototype / "src"] + others if r.is_dir()]
    paths = [p for p in (prototype / META / "partitions.md", prototype / META / "thresholds.yaml") if p.exists()]
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


def resolve(qfolder, partition):
    """Instance question folder + partition → everything the run needs, read from the names alone."""
    qfolder = Path(qfolder).resolve()
    m = QFOLDER.match(qfolder.name)
    if not m:
        raise GateError(f"{qfolder.name} is not a question folder <L><NN>-<name>")
    qid, rung = f"{m.group(1)}{m.group(2)}", qfolder.parent.name
    if rung != RUNG_DIR[m.group(1)]:
        raise GateError(f"{qfolder.name} sits in {rung}, not {RUNG_DIR[m.group(1)]}")
    instance = qfolder.parents[1]
    meta, _ = front(instance / "board.md")
    if meta.get("board-kind") != "insight-instance":
        raise GateError(f"{instance.name}/board.md is not board-kind: insight-instance")
    prototype = (instance / meta["prototype"]).resolve()
    partitions = front(prototype / META / "partitions.md")[0]["partitions"]
    part = next((p for p in partitions if p["name"] == partition), None)
    if part is None:
        raise GateError(f"{partition} is not a partition in {prototype.name}/{META}/partitions.md")
    pq_dir = prototype / rung / qfolder.name
    qfile = pq_dir / f"{qfolder.name}.md"
    if not qfile.is_file():
        raise GateError(f"{prototype.name} has no question {rung}/{qfolder.name}")
    q, _ = front(qfile)
    if q.get("id") != qid:
        raise GateError(f"{qfile.name}: id {q.get('id')!r} is not {qid}, the start of its folder name")
    if partition not in asked_partitions(q, partitions):
        raise GateError(f"{qid} is not asked on {partition}")
    scripts = qfolder / "scripts"
    return dict(qfolder=qfolder, instance=instance, prototype=prototype, extract=meta["extract"], rung=rung,
                partitions=partitions, part=part, qid=qid, pq_dir=pq_dir, qfile=qfile, q=q,
                scripts=scripts, script=entry_script(scripts, qid))


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
    return str(v).replace("|", "/").replace("\n", " ")


def md_table(df, limit=REPORT_ROWS):
    """A markdown table of a result, cut at `limit` rows with the cut said."""
    lines = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join(_cell(v) for v in r) + " |" for r in df.head(limit).itertuples(index=False)]
    if len(df) > limit:
        lines.append(f"\n({len(df)} rows; the first {limit} are shown, the full table is in results/)")
    return "\n".join(lines)


def write_report(r, receipt, out, rep):
    """reports/<partition>/report.md: generated from the run, never written by hand (AGENTS.md rule 0)."""
    q, part = r["q"], r["part"]
    status = receipt["status"] + (f" · {receipt.get('reason') or receipt.get('problem')}" if receipt["status"] != "ok" else "")
    lines = [f"# {r['qid']} · {part['name']} · run report", "",
             "Generated by haipipe-insight ref/run_question.py from this run's results; rerun the ticket to change it.", "",
             f"- **Question**: {q.get('name', '')} · {q.get('question', '')}".rstrip(" ·"),
             f"- **The ask**: {q.get('ask')}",
             f"- **Partition**: {part['name']} · {part.get('plain', '')}",
             f"- **Status**: {status}",
             f"- **Rows**: {receipt.get('rows_after', '')} of {receipt.get('rows_before', '')}",
             f"- **Ticket**: `{receipt['ticket']}` · ended {receipt.get('ended', '')}", ""]
    power = out / "partition_power.csv"
    if power.is_file():
        lines += ["## Power, before any contrast", "", md_table(pd.read_csv(power)), ""]
    if receipt["status"] == "ok":
        for nid, n in live_needs(q).items():
            if n.get("kind") != "compute":
                continue
            lines += [f"## {r['qid']}.{nid} · {n.get('what', '')}", "", f"**Pass**: {n.get('pass', '')}", ""]
            for f in n.get("output") or {}:
                lines += [f"### {f}", ""]
                if f.endswith(".csv"):
                    lines.append(md_table(pd.read_csv(out / f)))
                else:
                    data = json.loads((out / f).read_text())
                    flat = pd.json_normalize(data, sep=".").iloc[0].to_dict() if data else {}
                    lines.append(md_table(pd.DataFrame([{"key": k, "value": flat.get(k)} for k in n["output"][f]])))
                lines.append("")
    rep.mkdir(parents=True, exist_ok=True)
    (rep / "report.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _clear(folder):
    """A rerun replaces its result: nothing of an older run survives."""
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)


# ── one run ──────────────────────────────────────────────────────────────────
def run(qfolder, partition):
    t0 = time.time()
    root = space_root(qfolder)
    rel = lambda p: str(Path(p).resolve().relative_to(root))
    r = resolve(qfolder, partition)
    out, rep = r["qfolder"] / "results" / partition, r["qfolder"] / "reports" / partition
    _clear(out)
    _clear(rep)
    shared = shared_paths(r["prototype"], r["rung"], r["scripts"])
    proto_scripts = r["pq_dir"] / "scripts"
    receipt = {
        "status": "running", "question": r["qid"], "partition": partition,
        "ticket": rel(r["qfolder"] / "runs" / f"{partition}.sh"),
        "prototype": rel(r["prototype"]), "extract": r["extract"],
        "spec": rel(r["qfile"]), "spec_sha256": sha256(r["qfile"]),
        "scripts": rel(r["scripts"]), "scripts_sha256": sha256(r["scripts"]),
        "prototype_scripts_sha256": sha256(proto_scripts) if proto_scripts.is_dir() else None,
        "shared_sha256": shared_digest(r["prototype"], r["rung"], r["scripts"], r["q"]),
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
        tfile = r["prototype"] / META / "thresholds.yaml"
        thresholds = (yaml.safe_load(tfile.read_text()) or {}) if tfile.is_file() else {}
        others = [r["prototype"] / d / "src" for d in RUNG_DIR.values() if d != r["rung"]]
        for p in (*others, r["prototype"] / "src", r["prototype"] / r["rung"] / "src", r["scripts"]):
            if p.is_dir():                                   # the last inserted is searched first: scripts, own rung, top
                sys.path.insert(0, str(p))
        mod = {}
        exec(compile(r["script"].read_text(encoding="utf-8"), str(r["script"]), "exec"), mod)
        members = ([p for p in r["partitions"] if p["name"] in r["part"]["of"]] if partition == "cross" else [r["part"]])
        pw = (r["q"].get("partitions") or {}).get("power") or {}
        filt = {c["column"] for p in members for c in (p.get("where") or [])}
        extra = ({pw.get("outcome"), pw.get("groups")} - {None}) if isinstance(pw, dict) else set()
        want_cols = mod.get("COLUMNS") or []
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
        gate(tables, r["q"], read_cols, frames)
        for f, t in tables.items():
            if f.endswith(".csv"):
                t.to_csv(out / f, index=False)
            else:
                (out / f).write_text(json.dumps(t, indent=2, default=str))
        receipt.update(status="ok", outputs=sorted(tables) + ["partition_power.csv"])
    except Refused as e:
        receipt.update(status="refused", reason=str(e))
    except Exception as e:  # noqa: BLE001 · every failure is written into the receipt
        receipt.update(status="failed", problem=f"{type(e).__name__}: {e}")
    receipt.update(ended=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   duration_s=round(time.time() - t0, 1))
    write()
    write_report(r, receipt, out, rep)
    print(f"{r['qid']} · {partition}: {receipt['status']}"
          + (f" · {receipt.get('reason') or receipt.get('problem')}" if receipt["status"] != "ok" else ""))
    return receipt


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.exit(0 if run(sys.argv[1], sys.argv[2])["status"] in ("ok", "refused") else 1)
