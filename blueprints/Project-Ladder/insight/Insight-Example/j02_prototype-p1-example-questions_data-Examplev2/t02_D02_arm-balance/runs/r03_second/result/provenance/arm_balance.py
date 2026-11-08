"""D02 · rows and share of the cut in each arm and each group. Writes exactly the question file's output files.
Every arm the cut holds is listed (A and B always, at zero when empty); a missing value is its own level, so the
shares always add to 100."""
import pandas as pd

SPEC = "D02"
COLUMNS = ["arm", "group"]
MISSING = "(missing)"


def _share(df, col, always=()):
    values = df[col].astype("object").where(df[col].notna(), MISSING)
    counts = values.value_counts()
    levels = list(always) + sorted(v for v in counts.index if v not in always and v != MISSING)
    levels += [MISSING] if MISSING in counts.index else []
    out = pd.DataFrame([{"level": lv, "n": int(counts.get(lv, 0))} for lv in levels])
    out["share_pct"] = 100 * out["n"] / max(len(df), 1)
    return out


def run(df, ctx):
    return {"share_by_arm.csv": _share(df, "arm", ("A", "B")), "share_by_group.csv": _share(df, "group")}
