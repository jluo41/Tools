"""I01 · the outcome rate in each arm and the gap B - A, with intervals. Writes exactly the question file's output files."""
import pandas as pd

from example_stats import gap, gap_row, rate_row

SPEC = "I01"
COLUMNS = ["arm", "outcome"]


def run(df, ctx):
    rates = pd.DataFrame([rate_row(a, int((df["arm"] == a).sum()), int(df.loc[df["arm"] == a, "outcome"].sum()), ctx.wilson)
                          for a in ("A", "B")])
    g, se = gap(df)
    return {"rates_by_arm.csv": rates, "gap.csv": pd.DataFrame([gap_row("B - A", g, se, key="contrast")])}
