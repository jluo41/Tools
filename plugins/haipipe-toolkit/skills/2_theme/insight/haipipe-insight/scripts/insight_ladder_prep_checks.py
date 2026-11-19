"""The checks a DataPrep Block is held to (ref/dataprep.md rules 3, 4 and 7): what a Run may read, what it may write, what
its Result may show, and the audit that lists each against the Block. Read-only; `sign` refuses on `outputs`."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml

from insight_ladder_base import PREP, STEP, front, face, face_kind
from insight_ladder_prep import preps, steps, prep_hash

# a shared source stage: it copies the raw export into a store and saves a cache there, whatever else the config says
SHARED_SOURCE = {"raw_data_path": "copies the raw export into a shared raw store",
                 "source_config": "runs a shared source stage",
                 "save_cache": "saves a cache in a shared store", "use_cache": "reads a cache from a shared store"}
# a line that would put a record's values in a Result or a notebook (the reviewer reads each one): rows taken by
# head/tail/sample, unless they are an aggregate's (value_counts, describe, agg, size, count, nunique); a sample value
# written into a dictionary; a table printed whole
ROWS = re.compile(r"\.(head|tail|sample)\(")
AGGREGATE = re.compile(r"value_counts\(|describe\(|\.agg\(|\.size\(\)|\.count\(\)|nunique\(")
RECORD = re.compile(r"""['"]sample_value['"]\s*:|print\(\s*(df|rows|data)\s*\)""")
DICT_SAMPLE = {"sample_value", "sample", "example", "example_value", "first_value"}


def _configs(ver: Path, runs_only: bool = True) -> list[tuple[Path, Path, dict]]:
    pattern = "r[0-9][0-9]_*.yaml" if runs_only else "*.yaml"
    out = []
    for s in steps(ver):
        for cfg in sorted((s / "scripts" / "config").glob(pattern)):
            out.append((s, cfg, yaml.safe_load(cfg.read_text(encoding="utf-8")) or {}))
    return out


def _keys(node, path: str = "") -> list[tuple[str, object]]:
    """Every (dotted key, value) in a config, at any depth."""
    if isinstance(node, dict):
        return [kv for k, v in node.items() for kv in [(f"{path}{k}", v), *_keys(v, f"{path}{k}.")]]
    if isinstance(node, list):
        return [kv for v in node for kv in _keys(v, path)]
    return []


def _frozen(block: Path) -> set[str]:
    """The folders the served Boards' data versions name: frozen, never written."""
    home = block.parent.parent
    out = set()
    for ref in front(block / "board.md")[0].get("serves") or []:
        b = next((x / str(ref) for x in [home, *home.parents] if (x / str(ref) / "board.md").is_file()), None)
        for v in (front(b / "board.md")[0].get("versions") or []) if b else []:
            out.add(str(v.get("folder") or v.get("extract") or "").rstrip("/"))
    return out


def outputs(ver: Path) -> list[tuple[str, str]]:
    """Each Run config of a prep version that would write where it may not (rule 4): it names no output folder, or an
    output name (`output.prepare_dir`, and `env.OUT_NAME` when a carried worker names its folder from it) does not end
    in `@prep-vK`, or is a folder a served Board's data version names. [(step/rNN, the folder or why)]."""
    k = PREP.match(ver.name).group(2)
    frozen = _frozen(ver.parent)
    out = []
    for s, cfg, c in _configs(ver):
        prepare = str((c.get("output") or {}).get("prepare_dir") or "")
        if not prepare:
            out.append((f"{s.name}/{cfg.stem}", "names no output folder of its own"))
        names = [prepare] + ([str(c["env"]["OUT_NAME"])] if (c.get("env") or {}).get("OUT_NAME") else [])
        for n in names:
            if n and (not n.rstrip("/").endswith(f"@{k}") or n.rstrip("/") in frozen):
                out.append((f"{s.name}/{cfg.stem}", n))
    return out


def inputs(ver: Path) -> list[tuple[str, str]]:
    """Each config of a prep version that reads or writes a shared store through a source stage (rule 3): a source
    config with `raw_data_path` copies the raw export and overwrites the source cache whatever `use_cache` says, so any
    of these keys is named, in a Run config or a stage config beside it."""
    out = []
    for s, cfg, c in _configs(ver, runs_only=False):
        for key, value in _keys(c):
            leaf = key.rsplit(".", 1)[-1]
            if leaf in SHARED_SOURCE and value not in (False, None, "", "false"):
                out.append((f"{s.name}/{cfg.name}", f"{key}: {SHARED_SOURCE[leaf]}"))
    return out


def records(ver: Path) -> list[tuple[str, str]]:
    """What may show a record's values (rule 4): a worker line that prints rows, and a Result dictionary with a sample
    column. A pattern, not a verdict: the step review reads each one."""
    out = []
    for s in steps(ver):
        for f in sorted((s / "scripts").rglob("*.py")) if (s / "scripts").is_dir() else []:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                m = ROWS.search(line)
                taken = m and not AGGREGATE.search(line[:m.start()])
                if (taken or RECORD.search(line)) and not line.lstrip().startswith("#"):
                    out.append((f"{f.relative_to(ver)}:{i}", "takes a record's value"))
        for d in sorted((s / "runs").glob("r[0-9][0-9]_*/result/**/data_dictionary.csv")):
            with d.open(encoding="utf-8", errors="replace") as fh:
                head = {h.strip().lower() for h in next(csv.reader(fh), [])}
            if head & DICT_SAMPLE:
                out.append((str(d.relative_to(ver)), f"a sample column ({', '.join(sorted(head & DICT_SAMPLE))})"))
    return out


def raw_gone(block: Path) -> list[str]:
    """Each dataset whose `raw:` folder is not there (SPACE-relative: found from any folder above the Block)."""
    home = block.parent.parent
    return [str(d.get("name")) for d in front(block / "board.md")[0].get("datasets") or []
            if d.get("raw") and not any((x / str(d["raw"])).exists() for x in [home, *home.parents])]


def audit(block: Path, quiet: bool = False) -> list[tuple]:
    """What a DataPrep Block lacks against ref/dataprep.md, one row per check: (Block, check, count, the step that
    fixes it). `outputs`, `inputs`, `records` and `agreed` read the open prep version; `hash` every signed one."""
    block = block.resolve()
    home = block.parent.parent
    rows = []
    serves = front(block / "board.md")[0].get("serves") or []
    lost = [r for r in serves if not any(face_kind(x / str(r)) == "board" for x in [home, *home.parents])]
    rows.append((block, "serves", len(lost), "serves: names each Board it feeds, Project- or SPACE-relative"))
    rows.append((block, "raw", len(raw_gone(block)), "each dataset's raw: folder is there; a dataset whose export is "
                                                      "gone is rebuilt from a new export, never from a cache"))
    vers = preps(block)
    open_ = [v for v in vers if str(face(v).get("state")) != "closed"]
    newest = vers[-1:] if vers else []
    workers = [s for v in newest for s in steps(v)
               if not (s / "scripts" / f"{face(s).get('worker') or STEP.match(s.name).group(2)}.py").is_file()]
    rows.append((block, "workers", len(workers), "each step's scripts/<worker>.py, the name on its face (worker:)"))
    configs = [r for v in newest for s in steps(v) for r in sorted((s / "runs").glob("r[0-9][0-9]_*"))
               if r.is_dir() and not (s / "scripts" / "config" / f"{r.name}.yaml").is_file()]
    rows.append((block, "configs", len(configs), "each Run's scripts/config/rNN_<dataset>.yaml (run <step> dataset)"))
    found = {name: [x for v in open_ for x in fn(v)] for name, fn in (("outputs", outputs), ("inputs", inputs),
                                                                     ("records", records))}
    rows.append((block, "outputs", len(found["outputs"]), "each Run names its own new folder ending @prep-vK, never one "
                                                          "made before or a Board's data version (rule 4)"))
    rows.append((block, "inputs", len(found["inputs"]), "a step reads only its raw: folder and earlier steps; it loads "
                                                        "the raw export itself, with no shared source stage (rule 3)"))
    rows.append((block, "records", len(found["records"]), "a Result and a notebook show shapes, counts and names, "
                                                          "never a record value (rule 4); the review reads each line"))
    unagreed = [s for v in open_ for s in steps(v) if not str(face(s).get("agreed", "")).startswith("✅")]
    rows.append((block, "agreed", len(unagreed), "run-review-steps: another agent agrees each step; sign waits on it"))
    drift = [v for v in vers if str(face(v).get("state")) == "closed" and str(face(v).get("hash")) != prep_hash(v)]
    rows.append((block, "hash", len(drift), "a signed version's tools changed after the signature: restore them, or "
                                            "open the next prep version"))
    if not quiet:
        for b, check, n, step_ in rows:
            print(f"{'✅' if n == 0 else '❗'} {b.name:<28} {check:<9} {n:>4}" + ("" if n == 0 else f"   ▶ {step_}"))
        for name, items in found.items():
            for where, what in items:
                print(f"     {name:<8} {where} -> {what}")
        for d in raw_gone(block):
            print(f"     raw      {d}")
    return rows
