"""I02 · the outcome rate on each day of the window and its drift per day. Writes exactly the question file's output
files. Every day of the window is listed; a day with no rows shows n = 0 and no rate. The slope's interval uses the t
quantile with (days with rows - 2) degrees of freedom."""
import math

import pandas as pd
from scipy.stats import t as t_dist

from example_stats import rate_row

SPEC = "I02"
COLUMNS = ["date", "outcome"]


def run(df, ctx):
    day = pd.to_datetime(df["date"]).dt.normalize()
    first, last = day.min(), day.max()
    df = df.assign(_day=(day - first).dt.days + 1)
    by = df.groupby("_day")["outcome"].agg(["size", "sum"])
    days = range(1, (last - first).days + 2)
    rates = pd.DataFrame([rate_row(d, int(by.loc[d, "size"]) if d in by.index else 0,
                                   int(by.loc[d, "sum"]) if d in by.index else 0, ctx.wilson) for d in days])
    seen = rates[rates["n"] > 0]
    x, y, w = seen["level"].astype(float), seen["rate_pct"], seen["n"].astype(float)
    xm, ym = (w * x).sum() / w.sum(), (w * y).sum() / w.sum()
    sxx = (w * (x - xm) ** 2).sum()
    slope = (w * (x - xm) * (y - ym)).sum() / sxx
    resid = y - (ym + slope * (x - xm))
    dof = max(len(x) - 2, 1)
    se = math.sqrt((w * resid ** 2).sum() / dof / sxx)
    q = float(t_dist.ppf(0.975, dof))
    trend = pd.DataFrame([{"term": "points per day", "slope_pp": slope, "slope_lo_pp": slope - q * se,
                           "slope_hi_pp": slope + q * se}])
    return {"rates_by_day.csv": rates, "trend.csv": trend}
