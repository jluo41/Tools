#!/usr/bin/env python3
"""
Seed or update a column dictionary for haipipe-task-for-description.

    python seed_dictionary.py --dictionary <dict.yaml> --table <file.parquet> [--table ...]
                              [--seed <contract.yaml> ...] [--groups-from <module.py>]

Run it from the SPACE root; every path is SPACE-relative.

What it does, and what it never does
    - Adds every column of every --table that the dictionary lacks, with
      meaning "?" so the Table Card shows it as undescribed.
    - Fills a "?" meaning from a --seed file: any YAML with a `columns:` list
      of {name, meaning} (a ProcName contract card, a vendor dictionary). The
      seed's top-level `procname` is added to the column's `feeds:`, and
      `source:` records which file the meaning came from.
    - Sets `group:` from --groups-from, a Python file with GROUPS =
      {group: [columns]} and optionally IDENTIFYING_GROUPS = {group, ...}.
    - Never overwrites a meaning, group, or note someone typed. Re-running is
      safe; it only fills gaps.
"""

import argparse
import importlib.util
import os
import sys
from pathlib import Path

import pyarrow.parquet as pq
import yaml

UNKNOWN = "?"


def load_groups(path):
    spec = importlib.util.spec_from_file_location("groups_module", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(path).parent))
    spec.loader.exec_module(module)
    by_column = {c: g for g, cols in getattr(module, "GROUPS", {}).items() for c in cols}
    return getattr(module, "GROUPS", {}), by_column, set(getattr(module, "IDENTIFYING_GROUPS", set()))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dictionary", required=True)
    ap.add_argument("--table", action="append", required=True)
    ap.add_argument("--seed", action="append", default=[])
    ap.add_argument("--groups-from")
    args = ap.parse_args()

    for p in [args.dictionary, *args.table, *args.seed] + ([args.groups_from] if args.groups_from else []):
        if os.path.isabs(p):
            sys.exit(f"use a SPACE-relative path, not {p}")

    dict_path = Path(args.dictionary)
    data = yaml.safe_load(dict_path.read_text()) if dict_path.is_file() else {}
    data = data or {}
    data.setdefault("table", {"name": UNKNOWN, "what": UNKNOWN, "row": UNKNOWN, "grain": [], "time": None,
                              "source": UNKNOWN, "notes": []})
    groups = data.setdefault("groups", {})
    columns = data.setdefault("columns", {})

    group_lists, group_of, identifying = ({}, {}, set())
    if args.groups_from:
        group_lists, group_of, identifying = load_groups(args.groups_from)
        for g in group_lists:
            groups.setdefault(g, {"title": g.replace("_", " ").capitalize(), "what": UNKNOWN,
                                  "identifying": g in identifying})

    seeds = {}
    for seed in args.seed:
        doc = yaml.safe_load(Path(seed).read_text()) or {}
        procname = doc.get("procname")
        for col in doc.get("columns") or []:
            name, meaning = col.get("name"), (col.get("meaning") or "").strip()
            if not name:
                continue
            slot = seeds.setdefault(name, {"meaning": None, "source": None, "feeds": []})
            if meaning and not slot["meaning"]:
                slot["meaning"], slot["source"] = meaning, seed
            if procname and procname not in slot["feeds"]:
                slot["feeds"].append(procname)

    added = filled = 0
    for table in args.table:
        for name in pq.ParquetFile(table).schema_arrow.names:
            e = columns.get(name)
            if e is None:
                e = columns[name] = {"group": group_of.get(name, "undescribed"), "meaning": UNKNOWN}
                added += 1
            if e.get("group") in (None, "undescribed") and name in group_of:
                e["group"] = group_of[name]
            s = seeds.get(name)
            if s and e.get("meaning") in (None, "", UNKNOWN) and s["meaning"]:
                e["meaning"], e["source"] = s["meaning"], s["source"]
                filled += 1
            if s and s["feeds"]:
                e["feeds"] = sorted(set(e.get("feeds") or []) | set(s["feeds"]))

    dict_path.parent.mkdir(parents=True, exist_ok=True)
    dict_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100))
    unknown = sum(1 for e in columns.values() if e.get("meaning") in (None, "", UNKNOWN))
    print(f"{dict_path}: {len(columns)} columns; added {added}, meanings filled from seeds {filled}, "
          f"still '?' {unknown}")


if __name__ == "__main__":
    main()
