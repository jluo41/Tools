"""M05's one door to a raw extract: grouped counts and rates, never a row (M05 m3, step ①).

    python aggregate_query.py <dictionary.md> --columns
    python aggregate_query.py <dictionary.md> --out <run-reason-t00>/result/queries
                              --why "<what this asks>" [--by <key>[,<key>]] [--metrics <col>[,<col>]]
                              [--where <key>=<v>[|<v>]] [--where <key>!=<v>] [--budget 30]

The dictionary (Markdown: the extract's path in backticks, then a table name · group · dtype · null_pct · n_unique)
decides what may be asked, so no dataset needs its own list:

    never     a column of the `identity` group, an all-null column: refused as a key, a filter and a metric
    text      more than 1000 values (free text, names, codes): only as `<col>:length`, 10-character bins
    a time    only as `<col>:hour`, `<col>:weekday`, `<col>:date` or `<col>:month`
    a number  a key as itself with at most 50 values, else as `<col>:q5` (fifths); any number is a metric (its
              mean: a rate for a 0/1 flag)
    the rest  a key as itself

An answer groups by at most 3 keys (none: one group, all rows) and gives each group's n and its metrics' means. A
group under 11 is hidden and only counted; at most 60 groups show, the largest first. Each answer is written to
--out as q<NN>.yaml with its receipt (this tool's sha, the dictionary's, the extract's) and queries.md lists them all;
past --budget the tool refuses. An error prints its kind and the tool's own message, never a value from the data.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import sys
from pathlib import Path

import yaml

MIN_N = 11          # a group under this is hidden
MAX_GROUPS = 60     # groups shown per answer, the largest first
MAX_KEYS = 3
TEXT_LEVELS = 1000  # text with more values than this is free text: only its length
KEY_LEVELS = 50     # a number with more values than this is a key only in fifths
TIME_PARTS = ("hour", "weekday", "date", "month")


class Refuse(Exception):
    """The tool's own refusal: its message names columns and the asker's words only."""


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def space_root(start: Path) -> Path:
    for d in [start, *start.parents]:
        if (d / "env.sh").is_file():
            return d
    raise Refuse("no SPACE root (a folder holding env.sh) above the dictionary")


def read_dictionary(md: Path) -> tuple[Path, dict]:
    text = md.read_text(encoding="utf-8")
    m = re.search(r"`([^`]+\.(?:parquet|csv))`", text)
    if not m:
        raise Refuse(f"{md.name} names no extract (a `….parquet` or `….csv` path in backticks)")
    extract = Path(m.group(1))
    if not extract.is_absolute():
        extract = space_root(md.resolve().parent) / extract
    cols, head = {}, None
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if head is None:
            if "name" in cells and "dtype" in cells:
                head = cells
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        row = dict(zip(head, cells))
        cols[row["name"]] = {"group": row.get("group", ""), "dtype": row.get("dtype", ""),
                             "null_pct": float(row.get("null_pct") or 0), "n_unique": int(float(row.get("n_unique") or 0))}
    if not cols:
        raise Refuse(f"{md.name} has no column table (name · group · dtype · null_pct · n_unique)")
    return extract, cols


def kind(c: dict) -> str:
    if c["group"] == "identity" or c["null_pct"] >= 100:
        return "never"
    d = c["dtype"]
    if d.startswith("datetime"):
        return "time"
    if d.startswith(("int", "float", "uint")):
        return "number"
    if c["n_unique"] > TEXT_LEVELS:
        return "text"
    return "category"


def uses(c: dict) -> str:
    k = kind(c)
    return {"never": "refused",
            "time": "key as :hour · :weekday · :date · :month",
            "text": "key as :length only",
            "number": ("key as itself · metric" if c["n_unique"] <= KEY_LEVELS else "key as :q5 · metric"),
            "category": "key as itself"}[k]


def parse_key(key: str, cols: dict) -> tuple[str, str]:
    col, part = (key, "") if key in cols or ":" not in key else key.rpartition(":")[::2]   # a name may hold a colon
    if col not in cols:
        raise Refuse(f"{col} is not in the dictionary")
    c, k = cols[col], kind(cols[col])
    if k == "never":
        raise Refuse(f"{col} is refused (identity or empty)")
    if k == "time" and part not in TIME_PARTS:
        raise Refuse(f"{col} is a time: ask {col}:hour, :weekday, :date or :month")
    if k == "text" and part != "length":
        raise Refuse(f"{col} is free text: ask {col}:length")
    if k == "number" and not part and c["n_unique"] > KEY_LEVELS:
        raise Refuse(f"{col} has more than {KEY_LEVELS} values: ask {col}:q5")
    if k == "number" and part not in ("", "q5"):
        raise Refuse(f"{col} is a number: ask {col} or {col}:q5")
    if k == "category" and part:
        raise Refuse(f"{col} is a category: ask {col} as it is")
    return col, part


def derive(s, part: str):
    import pandas as pd
    if part == "hour":
        return s.dt.hour.astype("Int64")
    if part == "weekday":
        return s.dt.day_name()
    if part == "date":
        return s.dt.strftime("%Y-%m-%d")
    if part == "month":
        return s.dt.strftime("%Y-%m")
    if part == "length":
        lo = (s.astype("string").str.len() // 10 * 10).astype("Int64")
        return lo.map(lambda v: f"{v}-{v + 9}" if pd.notna(v) else None)
    if part == "q5":
        return pd.qcut(s, 5, duplicates="drop").astype("string")
    return s


def parse_where(text: str) -> tuple[str, str, list]:
    m = re.match(r"^([^!=]+)(!=|=)(.*)$", text)
    if not m:
        raise Refuse(f"a filter is <key>=<v>[|<v>] or <key>!=<v>: {text}")
    return m.group(1).strip(), m.group(2), [v.strip() for v in m.group(3).split("|")]


def mask_for(s, op: str, values: list):
    import pandas as pd
    if pd.api.types.is_numeric_dtype(s):
        try:
            hit = s.isin([float(v) for v in values])
        except ValueError:
            raise Refuse("a number filter takes numbers")
    else:
        hit = s.astype("string").isin(values)
    return ~hit if op == "!=" else hit


def plain(v):
    if hasattr(v, "item"):
        v = v.item()
    if isinstance(v, float):
        return round(v, 4)
    return v if isinstance(v, (int, str)) or v is None else str(v)


def answer(md: Path, by: list, metrics: list, where: list) -> tuple[list, int, int, Path]:
    import pandas as pd
    extract, cols = read_dictionary(md)
    if not extract.is_file():
        raise Refuse(f"the extract named in {md.name} is not on this machine")
    if len(by) > MAX_KEYS:
        raise Refuse(f"at most {MAX_KEYS} keys")
    keys = [parse_key(k, cols) for k in by]
    filters = [(parse_key(w, cols), op, vals) for w, op, vals in (parse_where(x) for x in where)]
    for m in metrics:
        if m not in cols or kind(cols[m]) != "number":
            raise Refuse(f"{m} is not a metric (a number, not identity)")
        if any(c == m and not p for c, p in keys):
            raise Refuse(f"{m} is a key here: ask it as a key or as a metric, not both")
    need = sorted({c for c, _ in keys} | {c for (c, _), _, _ in filters} | set(metrics))
    df = pd.read_parquet(extract, columns=need) if extract.suffix == ".parquet" else pd.read_csv(extract, usecols=need)
    keep = pd.Series(True, index=df.index)
    for (col, part), op, vals in filters:
        keep &= mask_for(derive(df[col], part), op, vals).fillna(False).astype(bool)
    df = df[keep]
    frame = pd.DataFrame({f"{c}:{p}" if p else c: derive(df[c], p) for c, p in keys}, index=df.index)
    for m in metrics:
        frame[m] = df[m]
    names = list(frame.columns[:len(keys)])
    if names:
        grouped = frame.groupby(names, dropna=False, observed=True)
        table = grouped.size().rename("n").to_frame()
        if metrics:
            table = table.join(grouped[metrics].mean())
        table = table.reset_index()
    else:
        table = pd.DataFrame([{"n": len(frame), **{m: frame[m].mean() for m in metrics}}])
    shown = table[table["n"] >= MIN_N].sort_values("n", ascending=False)
    hidden = int((table["n"] < MIN_N).sum())
    omitted = max(0, len(shown) - MAX_GROUPS)
    rows = [{k: plain(v) for k, v in r.items()} for r in shown.head(MAX_GROUPS).to_dict("records")]
    return rows, hidden, omitted, extract


def index(out: Path) -> None:
    lines = ["# Queries", "", "Each answer of `aggregate_query.py`: grouped counts and rates only; a group under "
             f"{MIN_N} is hidden.", "", "| query | why | by | where | groups | hidden |", "|---|---|---|---|---|---|"]
    for q in sorted(out.glob("q[0-9]*.yaml")):
        d = yaml.safe_load(q.read_text(encoding="utf-8")) or {}
        lines.append(f"| {d.get('query')} | {d.get('why', '')} | {', '.join(d.get('by') or ['all'])} | "
                     f"{'; '.join(d.get('where') or []) or '—'} | {len(d.get('rows') or [])} | {d.get('hidden', 0)} |")
    (out / "queries.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def ask(md: Path, out: Path, why: str, by: list, metrics: list, where: list, budget: int) -> Path:
    if not why.strip():
        raise Refuse("--why says what the query asks")
    out.mkdir(parents=True, exist_ok=True)
    done = sorted(out.glob("q[0-9]*.yaml"))
    if len(done) >= budget:
        raise Refuse(f"the budget of {budget} queries is spent")
    qid = f"q{max([int(p.stem[1:]) for p in done] or [0]) + 1:02d}"
    rows, hidden, omitted, extract = answer(md, by, metrics, where)
    root = space_root(md.resolve().parent)
    rel = lambda p: p.resolve().relative_to(root).as_posix() if p.resolve().is_relative_to(root) else p.name
    record = {"query": qid, "why": why.strip(), "by": by, "where": where, "metrics": metrics, "rows": rows,
              "hidden": hidden, "omitted": omitted,
              "receipt": {"tool": "aggregate_query.py", "tool_sha": sha(Path(__file__)),
                          "dictionary": rel(md), "dictionary_sha": sha(md.resolve()),
                          "extract": rel(extract), "extract_sha": sha(extract),
                          "min_n": MIN_N, "made_at": datetime.datetime.now().isoformat(timespec="seconds")}}
    path = out / f"{qid}.yaml"
    path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True), encoding="utf-8")
    index(out)
    return path


def show(path: Path) -> None:
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    print(f"{d['query']} · {d['why']}")
    rows = d["rows"]
    if rows:
        head = list(rows[0])
        print(" | ".join(head))
        for r in rows:
            print(" | ".join(str(r[h]) for h in head))
    print(f"shown {len(rows)} · hidden {d['hidden']} (under {MIN_N}) · omitted {d['omitted']} · {path.name}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dictionary", type=Path)
    ap.add_argument("--columns", action="store_true", help="list each column and how it may be asked")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--why", default="")
    ap.add_argument("--by", default="")
    ap.add_argument("--metrics", default="")
    ap.add_argument("--where", action="append", default=[])
    ap.add_argument("--budget", type=int, default=30)
    a = ap.parse_args(argv)
    split = lambda s: [x.strip() for x in s.split(",") if x.strip()]
    try:
        if a.columns:
            _, cols = read_dictionary(a.dictionary)
            for name, c in cols.items():
                print(f"{name:<40} {c['group']:<14} {uses(c)}")
            return 0
        if a.out is None:
            raise Refuse("--out names run-reason-t00's result/queries")
        show(ask(a.dictionary, a.out, a.why, split(a.by), split(a.metrics), a.where, a.budget))
        return 0
    except Refuse as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    except Exception as e:                       # never echo a data value
        print(f"refused: {type(e).__name__} while answering (no data shown)", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
