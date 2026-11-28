"""The checks a DataPrep Block is held to (ref/dataprep.md): it holds code only, so what it can hold wrong is its code.
`audit` lists them against the Block; read-only. What a Run makes is checked where it runs, on a Board (ref/run_prep.py)."""

from __future__ import annotations

import re
from pathlib import Path

from insight_ladder_base import front, face, face_kind
from insight_ladder_prep import preps, steps, spec, script_of, prep_hash

# a line that would put a record's values in a Result or a page (the reviewer reads each one): rows taken by
# head/tail/sample, unless they are an aggregate's (value_counts, describe, agg, size, count, nunique); a sample value
# written into a dictionary; a table printed whole
ROWS = re.compile(r"\.(head|tail|sample)\(")
AGGREGATE = re.compile(r"value_counts\(|describe\(|\.agg\(|\.size\(\)|\.count\(\)|nunique\(")
RECORD = re.compile(r"""['"]sample_value['"]\s*:|print\(\s*(df|rows|data)\s*\)""")
# a dictionary column that holds record values (the workbench drops the same names as it reads: insight_plan_c SAMPLE_KEYS)
DICT_SAMPLE = {"sample_value", "sample", "samples", "example", "example_value", "examples", "first_value", "top_values"}


def records(ver: Path) -> list[tuple[str, str]]:
    """Each script line of a prep version that takes a record's value (rule 4). A pattern, not a verdict: the step
    review reads each one."""
    out = []
    files = [p for s in steps(ver) for p in sorted((s / "scripts").rglob("*.py"))] + \
        (sorted((ver / "src").rglob("*.py")) if (ver / "src").is_dir() else [])
    for f in files:
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            m = ROWS.search(line)
            taken = m and not AGGREGATE.search(line[:m.start()])
            if (taken or RECORD.search(line)) and not line.lstrip().startswith("#"):
                out.append((f"{f.relative_to(ver)}:{i}", "takes a record's value"))
    return out


def references_off(block: Path) -> list[str]:
    """Each reference table that names no version, or whose path is not there (SPACE-relative)."""
    home = block.parent.parent
    return [str(r.get("name")) for r in front(block / "board.md")[0].get("references") or []
            if not r.get("version") or not r.get("path")
            or not any((x / str(r["path"])).exists() for x in [home, *home.parents])]


def audit(block: Path, quiet: bool = False) -> list[tuple]:
    """What a DataPrep Block lacks against ref/dataprep.md, one row per check: (Block, check, count, the step that
    fixes it). `scripts`, `records` and `agreed` read the open prep version; `hash` every signed one."""
    block = block.resolve()
    home = block.parent.parent
    rows = []
    serves = front(block / "board.md")[0].get("serves") or []
    lost = [r for r in serves if not any(face_kind(x / str(r)) == "board" for x in [home, *home.parents])]
    rows.append((block, "serves", len(lost), "serves: names each Board that runs it, Project- or SPACE-relative"))
    rows.append((block, "references", len(references_off(block)), "each reference names its version, and its path is "
                                                                  "there (insight_ladder.py reference; rule 3)"))
    vers = preps(block)
    open_ = [v for v in vers if str(face(v).get("state")) != "closed"]
    unwritten = [s for v in open_ for s in steps(v) if not script_of(s).is_file()
                 or "def run(" not in script_of(s).read_text(encoding="utf-8")]
    rows.append((block, "scripts", len(unwritten), "each step's scripts/<script>.py exposes run(ctx), the name its "
                                                   "step.md gives"))
    found = [x for v in open_ for x in records(v)]
    rows.append((block, "records", len(found), "a Result and a page show shapes, counts and names, never a record "
                                               "value (rule 4); the step review reads each line"))
    unagreed = [s for v in open_ for s in steps(v) if not str(spec(s).get("agreed", "")).startswith("✅")]
    rows.append((block, "agreed", len(unagreed), "run-review-steps: another agent agrees each step; sign waits on it"))
    drift = [v for v in vers if str(face(v).get("state")) == "closed" and str(face(v).get("hash")) != prep_hash(v)]
    rows.append((block, "hash", len(drift), "a signed version's code changed after the signature: restore it, or open "
                                            "the next prep version"))
    if not quiet:
        for b, check, n, step_ in rows:
            print(f"{'✅' if n == 0 else '❗'} {b.name:<28} {check:<10} {n:>4}" + ("" if n == 0 else f"   ▶ {step_}"))
        for where, what in found:
            print(f"     records  {where} -> {what}")
    return rows
