"""source · one step of prep-v1 (hai-insight ref/dataprep.md): read the raw export, cut each date to its day,
check its keys, and hand the rows on. Writes the rows to ctx.out, its counts to ctx.result/metrics.json."""
import json

import pandas as pd

ARMS, GROUPS = {"A", "B"}, {"group_1", "group_2", "group_3"}


def run(ctx):
    df = pd.read_parquet(ctx.raw / "example.parquet")
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    bad = []
    if df[["date", "arm", "group", "outcome"]].isna().any().any():
        bad.append("a key column is empty")
    if not set(df["arm"]) <= ARMS:
        bad.append(f"an arm outside {sorted(ARMS)}")
    if not set(df["group"]) <= GROUPS:
        bad.append(f"a group outside {sorted(GROUPS)}")
    if not set(df["outcome"].unique()) <= {0, 1}:
        bad.append("an outcome that is not 0 or 1")
    if bad:
        ctx.refuse("; ".join(bad))
    df.to_parquet(ctx.out / "rows.parquet", index=False)
    (ctx.result / "metrics.json").write_text(json.dumps({
        "rows": int(len(df)), "columns": list(df.columns),
        "checks": {"keys not empty": "pass", "arms known": "pass", "groups known": "pass", "outcome 0 or 1": "pass"}},
        indent=2) + "\n")
