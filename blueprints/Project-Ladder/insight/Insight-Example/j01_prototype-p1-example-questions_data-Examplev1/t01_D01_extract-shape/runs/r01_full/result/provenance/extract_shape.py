"""D01 · the extract's size, window and missing share per column. Writes exactly the question file's output files."""
import pandas as pd

SPEC = "D01"
COLUMNS = "all"


def run(df, ctx):
    days = pd.to_datetime(df["date"])
    shape = {"n_rows": int(len(df)), "n_cols": int(df.shape[1]), "n_days": int(days.dt.date.nunique()),
             "first_day": str(days.min().date()), "last_day": str(days.max().date())}
    missing = pd.DataFrame({"column": list(df.columns), "null_pct": [100 * float(df[c].isna().mean()) for c in df.columns]})
    return {"shape.json": shape, "missing_by_column.csv": missing}
