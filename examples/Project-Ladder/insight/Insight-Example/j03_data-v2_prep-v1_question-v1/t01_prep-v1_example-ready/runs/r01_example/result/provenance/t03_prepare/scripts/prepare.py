"""prepare · one step of prep-v1 (hai-insight ref/dataprep.md): the ready folder the questions read, the same shape
as a data version folder (example.parquet, manifest.json, data_dictionary.csv). The dictionary carries names, types and
counts, never a record value."""
import json

import pandas as pd

DICTIONARY = [("date", "time", "the day of the contact"), ("arm", "design", "the arm it got: A or B"),
              ("group", "design", "its group: group_1, group_2 or the small group_3"),
              ("outcome", "outcome", "1 when the made-up outcome happened, else 0"),
              ("score", "measure", "a plain numeric score, higher with the outcome")]
FIELDS = {"name", "group", "dtype", "null_pct", "n_unique", "notes"}     # names, types and counts only


def run(ctx):
    df = pd.read_parquet(ctx.prev / "rows.parquet")
    names = [c for c, _, _ in DICTIONARY]
    if sorted(df.columns) != sorted(names):
        ctx.refuse(f"the rows' columns {sorted(df.columns)} differ from the dictionary's {sorted(names)}")
    df = df.sort_values(["date", "arm", "group"], kind="stable").reset_index(drop=True)
    df.to_parquet(ctx.out / "example.parquet", index=False)
    (ctx.out / "manifest.json").write_text(json.dumps({
        "output_file": "example.parquet", "n_rows": int(len(df)), "n_cols": int(df.shape[1]),
        "start_date": str(df["date"].min().date()), "end_date": str(df["date"].max().date()),
        "source_set": f"{ctx.dataset} {ctx.data} made ready by {ctx.prep}", "groups": {"identity": []}}, indent=2) + "\n")
    dd = pd.DataFrame([{"name": c, "group": g, "dtype": str(df[c].dtype),
                   "null_pct": round(100 * float(df[c].isna().mean()), 1), "n_unique": int(df[c].nunique()),
                   "notes": notes} for c, g, notes in DICTIONARY])
    if set(dd.columns) != FIELDS:
        ctx.refuse(f"the dictionary holds a field beyond {sorted(FIELDS)}: no record value")
    dd.to_csv(ctx.out / "data_dictionary.csv", index=False)
