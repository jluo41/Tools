"""K01 · is the gap B - A the same in the first and second groups: the pooling verdict, on cross. It reads I01's gap
for each group through ctx.result (never the rows again), so a change to I01 marks this run stale. Writes exactly the
question file's output files."""
import pandas as pd

from example_stats import Z, gap_row, z_test

SPEC = "K01"
COLUMNS = "none"


def _gap(ctx, part):
    try:
        row = ctx.result("I01", "gap.csv", partition=part).iloc[0]
    except Exception:                       # I01 refused or has not run this cut: nothing to pool, and that is the answer
        ctx.refuse(f"I01 has no gap on {part} (refused for power or not run), so the groups cannot be pooled")
    return float(row["gap_pp"]), (float(row["gap_hi_pp"]) - float(row["gap_lo_pp"])) / (2 * Z)


def run(df, ctx):
    smallest = float(ctx.thresholds["power"]["smallest_effect_pp"])
    (n1, _), (n2, _) = list(ctx.partitions.items())
    g1, se1 = _gap(ctx, n1)
    g2, se2 = _gap(ctx, n2)
    d, se, p = z_test(g1, se1, g2, se2)
    lo, hi = d - Z * se, d + Z * se
    if p < 0.05:
        word, rule = "SPLIT", "the groups' gaps differ (p < 0.05)"
    elif -smallest < lo and hi < smallest:
        word, rule = "POOL", f"the difference's 95% interval lies inside ±{smallest:g} points"
    else:
        word, rule = "UNDETERMINED", f"no difference shown, but its 95% interval reaches past ±{smallest:g} points"
    table = pd.DataFrame([gap_row(n1, g1, se1), gap_row(n2, g2, se2), gap_row(f"{n2} - {n1}", d, se)])
    return {"pooling.csv": table, "verdict.json": {"verdict": word, "test": "pooling: z test of two gaps",
                                                   "p_value": round(p, 4), "rule": rule}}
