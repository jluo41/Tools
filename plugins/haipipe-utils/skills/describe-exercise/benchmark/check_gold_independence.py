#!/usr/bin/env python3
"""
Prove -- or refuse -- the one assumption the whole exercise benchmark rests on.

THE ASSUMPTION
================================================================================
The gold is a MET back-solved from the kcal a vendor's app logged. If a vendor
computed that kcal by looking the activity up in a MET table, the gold IS the
prediction wearing a different hat, and every number downstream is memorisation
-- the same trap describe-food fell into with its observed bank.

THE TEST
================================================================================
A table lookup is a constant. So within one (vendor, activity) pair, hold the
back-solved MET up to the light:

    coefficient of variation = 0  ->  TABLE, and the gold is worthless
    coefficient of variation > 0  ->  the figure moved with something the table
                                      does not know, i.e. sensors

    python check_gold_independence.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec import SPEC, SOURCE_STORE, _augment

ROOT = Path("/home/jluo41/WellDoc-SPACE")
OUT = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/6-benchmark"
TABLE_CV = 0.05      # anything under this is a lookup, not a measurement
MIN_N = 100


def main():
    rows = []
    for p in sorted(SOURCE_STORE.glob("*/@*/Exercise.parquet")):
        cohort = p.relative_to(SOURCE_STORE).parts[0]
        df = pd.read_parquet(p)
        if len(df) == 0 or "EntrySourceID" not in df.columns:
            continue
        df = _augment(df, cohort)
        rows.append(df[df.MET_device.notna()][
            ["EntrySourceID", "ExerciseType", "MET_device"]])
    e = pd.concat(rows, ignore_index=True)
    print(f"{len(e):,} rows carry a back-solved MET\n")

    g = e.groupby(["EntrySourceID", "ExerciseType"]).MET_device.agg(
        ["size", "median", "std"])
    g = g[g["size"] >= MIN_N].copy()
    g["cv"] = g["std"] / g["median"]

    print(f"{'vendor':>7} {'activity':>10} {'n':>7} {'MET med':>8} {'SD':>7} {'CV':>7}  verdict")
    print("-" * 72)
    for (ns, act), r in g.sort_values("size", ascending=False).head(20).iterrows():
        v = "TABLE -- gold is void" if r.cv < TABLE_CV else "sensor-derived"
        print(f"{ns:>7} {str(act):>10} {int(r['size']):>7,} {r['median']:>8.2f} "
              f"{r['std']:>7.2f} {r.cv:>7.2f}  {v}")

    per_vendor = g.groupby(level=0).cv.median().round(3)
    print(f"\nper-vendor median CV across activities with n >= {MIN_N}:")
    print(per_vendor.to_string())

    tabled = g[g.cv < TABLE_CV]
    verdict = "INDEPENDENT" if len(tabled) == 0 else "CONTAMINATED"
    print(f"\nVERDICT: {verdict}"
          f"   ({len(tabled)} of {len(g)} (vendor, activity) pairs look like a table)")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "gold_independence.json").write_text(json.dumps({
        "verdict": verdict,
        "rows_with_back_solved_met": int(len(e)),
        "pairs_tested": int(len(g)), "min_n_per_pair": MIN_N,
        "table_cv_threshold": TABLE_CV,
        "per_vendor_median_cv": {str(k): float(v) for k, v in per_vendor.items()},
        "pairs_that_look_like_a_table": [
            {"vendor": str(k[0]), "activity": str(k[1])} for k in tabled.index],
    }, indent=2))
    print(f"\nwrote {OUT/'gold_independence.json'}")
    return 0 if verdict == "INDEPENDENT" else 1


if __name__ == "__main__":
    sys.exit(main())
