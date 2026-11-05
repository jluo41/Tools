"""Build a paper Board's Values tabs: raw rows from the value Runs' copies, arranged into tables. It filters and arranges;
it never averages, fits or transforms (JL 261104: "这个 value table 就是从我们 run 里面摘出来、整理出来的，但是我们没有对它进行 process").
A cell holding two source rows shows both, joined, never their mean. SKILL.md "The Values tabs" has the config's shape.

    python build_tables.py <jNN_evidence_value/tNN_x/scripts/tables.yaml>      (from the Run ticket; RESULT_DIR set)

Writes result/tables.json (what the workbench draws), result/<tab>__<table>.csv (a table the displays can read), headline.txt.
"""
from __future__ import annotations

import itertools
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd
import yaml

SIZE = {"m": 1e6, "b": 1e9}


def copy_path(job: Path, frm: str) -> Path:
    """`<value Task>/<key>/<file>`: that file in the newest of the Task's Runs that holds it."""
    task, rest = frm.split("/", 1)
    runs = sorted((job / task / "runs").glob("*/result"), reverse=True)
    found = next((r / rest for r in runs if (r / rest).is_file()), None)
    if found is None:
        raise SystemExit(f"{frm}: no Run of {task} holds {rest}")
    return found


def keep(d: pd.DataFrame, where: dict) -> pd.DataFrame:
    for k, want in (where or {}).items():
        want = want if isinstance(want, list) else [want]
        d = d[d[k].astype(str).isin([str(w) for w in want])]
    return d


def order(values) -> list:
    """Natural order: 1m before 10m before 1b; numbers as numbers."""
    def key(x):
        s = str(x)
        m = re.fullmatch(r"([\d.]+)([mb])", s)
        if m:
            return (0, float(m.group(1)) * SIZE[m.group(2)], s)
        try:
            return (0, float(s), s)
        except ValueError:
            return (1, 0.0, s)
    return sorted(set(values), key=key)


def raw(x) -> str:
    if pd.isna(x):
        return ""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)


def pivot_table(d: pd.DataFrame, p: dict, combo: dict, flag: dict | None) -> dict:
    value = p["value"].format(**combo) if "{" in p["value"] else p["value"]
    marked = set(d.query(flag["query"]).index) if flag else set()
    if "melt" in p:                              # one column per step of a wide file (step_rmse_01 ... 24)
        steps = sorted(c for c in d.columns if c.startswith(p["melt"]))
        cols = [f"{int(c.rsplit('_', 1)[1]) * 5} min" for c in steps]
        rows = []
        for r in order(d[p["rows"]]):
            sub = d[d[p["rows"]] == r]
            rows.append({"head": raw(r), "cells": [{"v": " / ".join(raw(x) for x in sub[c]), "at": f"{p['rows']} = {r}, {c}"} for c in steps]})
        return {"row_head": p["rows"], "col_head": "Steps ahead", "cell_head": p["value"], "cols": cols, "rows": rows}
    cols = order(d[p["cols"]])
    rows = []
    for r in order(d[p["rows"]]):
        cells = []
        for c in cols:
            sub = d[(d[p["rows"]] == r) & (d[p["cols"]] == c)]
            cell = {"v": " / ".join(raw(x) for x in sub[value]), "at": f"{p['rows']} = {r}, {p['cols']} = {raw(c)}, column {value}"}
            if len(sub) > 1:
                cell["n"] = len(sub)
            if marked & set(sub.index):
                cell["flag"] = flag["why"]
            cells.append(cell)
        rows.append({"head": raw(r), "cells": cells})
    labels = [raw(c) for c in cols]
    if p.get("also"):                            # the column's other name, from the same rows: 0.1 epochs is 51M tokens
        labels = [f"{raw(c)} ({' / '.join(raw(x) for x in order(d[d[p['cols']] == c][p['also']]))}{p.get('also_suffix', '')})" for c in cols]
    return {"row_head": p["rows"], "col_head": p["cols"] + (f" ({p.get('also_head', p.get('also'))})" if p.get("also") else ""), "cell_head": combo.get("metric") if p["value"] == "value" else value,
            "cols": labels, "rows": rows}


def list_table(d: pd.DataFrame, columns: list) -> dict:
    return {"cols": columns, "rows": [{"cells": [{"v": raw(row[c])} for c in columns]} for _, row in d.iterrows()]}


def main() -> None:
    config = Path(sys.argv[1]).resolve()
    job, res = config.parents[2], Path(os.environ["RESULT_DIR"])
    cfg = yaml.safe_load(config.read_text(encoding="utf-8"))
    methods = config.parent / "methods.yaml"
    how = (yaml.safe_load(methods.read_text(encoding="utf-8")) if methods.is_file() else None) or {}
    tabs, total = [], 0
    for tab in cfg["tabs"]:
        tables = []
        for spec in tab["tables"]:
            src = pd.read_csv(copy_path(job, spec["from"]), dtype=None)
            d0 = keep(src, spec.get("where"))
            dims = spec.get("for", {})
            names = list(dims)
            for combo_keys in itertools.product(*[list(dims[k]) for k in names]):
                combo = dict(zip(names, combo_keys))
                d = d0
                for k, v in combo.items():
                    if k in d.columns:           # "metric" on a wide file only names the value column
                        d = d[d[k].astype(str) == str(v)]
                if d.empty:
                    raise SystemExit(f"{tab['slug']}: no rows for {combo} in {spec['from']}")
                body = (pivot_table(d, spec["pivot"], combo, spec.get("flag")) if "pivot" in spec
                        else list_table(d, spec["list"]))
                total += sum(len(r["cells"]) for r in body["rows"])
                key = ([spec["name"]] if spec.get("name") else []) + [str(dims[k][combo[k]]) for k in names]
                stem = "__".join(re.sub(r"[^A-Za-z0-9]+", "-", x).strip("-").lower() for x in [tab["slug"]] + key)
                (d if "list" in spec else pd.DataFrame(
                    [[r.get("head", "")] + [c["v"] for c in r["cells"]] for r in body["rows"]],
                    columns=[body["row_head"]] + body["cols"])).to_csv(res / f"{stem}.csv", index=False)
                got = {**(spec.get("where") or {}), **{k: v for k, v in combo.items() if k in src.columns}}
                column = spec["pivot"]["value"].format(**combo) if "pivot" in spec and "melt" not in spec["pivot"] else ""
                tables.append({**body, "key": key, "from": spec["from"], "file": f"{stem}.csv",
                               "keeps": "; ".join(f"{k} = {' or '.join(map(str, v)) if isinstance(v, list) else v}" for k, v in got.items()),
                               "column": column})
        steps = [x for c in tab.get("chain", []) for x in how["chains"][c]] + how.get("tabs", {}).get(tab["slug"], [])
        tabs.append({k: tab.get(k) for k in ("slug", "title", "line", "story", "values")} | {"tables": tables, "method": steps})
    (res / "tables.json").write_text(json.dumps({"tabs": tabs, "words": cfg.get("words") or {}, "suffixes": cfg.get("suffixes") or {}},
                                                ensure_ascii=False), encoding="utf-8")
    (res / "headline.txt").write_text(f"{len(tabs)} tabs, {sum(len(t['tables']) for t in tabs)} tables, {total} raw cells\n")
    print((res / "headline.txt").read_text())


if __name__ == "__main__":
    main()
