#!/usr/bin/env python3
"""
Regression + benchmark suite for the food -> nutrition normalizer.

    python test_foodnorm.py            # L1 + L2 (fast, no cohort data needed)
    python test_foodnorm.py --bench    # + L3 WellDoc held-out benchmark

WHY THIS EXISTS
================================================================================
score_candidate() is five hand-weighted heuristics. Tuning any one of them moves
every food at once, and the failures are silent -- a wrong match still returns a
plausible number. While building it, two regressions were introduced and caught
only by eyeballing output:

  raising the dilution penalty      -> "rice" matched "Soup, rice"  (28g -> 7g carbs)
  adding milk to RAW_EDIBLE_HEADS   -> "milk" matched "Milk, dry"   (4.8g -> 52g carbs)

Neither raised an exception. Both would have shipped. Every case below is a bug
that actually happened -- this file is the net under the next tuning pass.

LEVELS
------
  L1  contract    -- WEAK/MISS must never yield nutrition; retrieve returns dicts
  L2  golden set  -- known foods must land within tolerance of their true carbs
  L3  benchmark   -- WellDoc's 64k app-labelled meals, held out (needs --bench)
"""
import sys
import argparse
from pathlib import Path

from haiutils.food_enrichment import decompose, retrieve, classify, TRUSTED

# ============================================================================
# L2 GOLDEN SET -- carbs per 100 g, as eaten
# ============================================================================
# `must_not` names a description substring the matcher previously (wrongly)
# picked. It is the regression assertion: getting the carbs right by luck while
# still matching rice-soup is not a pass.
GOLDEN = [
    # food                   carbs  tol   must_not
    ("rice",                   28,   6,   "soup"),      # matched "Soup, rice" (7g)
    ("fried rice",             32,   8,   None),        # must KEEP the frying it asked for
    ("egg",                   1.1,   3,   "creamed"),   # matched "Egg, creamed" (5.5g)
    ("boiled egg",            1.1,   3,   "fried"),
    ("milk",                  4.8,   3,   "dry"),       # matched "Milk, dry" (52g)
    ("noodles",                25,   7,   None),
    ("bread",                  49,  12,   None),
    ("tofu",                    2,   4,   "fried"),     # matched "Tofu, fried" (8.9g)
    ("potato",                 17,   6,   None),
    ("apple",                  14,   5,   "baked"),     # matched "Apple, baked" (22.7g)
    ("banana",                 23,   7,   "baked"),     # matched "Banana, baked" (32.4g)
    ("cucumber",              3.6,   3,   None),
    ("lettuce",                 2,   3,   None),
    ("cabbage",                 6,   4,   None),
    ("chinese cabbage",       2.2,   3,   None),        # matched "Cabbage, raw" -- lost "chinese"
    ("millet porridge",        23,   7,   "raw"),       # matched "Millet, raw" (72g) -- 3x error
    ("bitter gourd",          4.3,   4,   "dishcloth"), # matched "Gourd, dishcloth"
    ("pork",                    0,   4,   None),
    ("chicken",                 0,   4,   None),
    ("shrimp",                  1,   4,   "fried"),     # matched "Shrimp, fried" (12.4g)
    ("beef",                    0,   4,   None),
    ("scrambled egg with tomato", 1.5, 4, "creamed"),
    ("rice in soup",          6.8,   5,   None),        # this one SHOULD be a soup
]


def run_l1_contract():
    """Structural guarantees the downstream join depends on."""
    print("\nL1  CONTRACT")
    print("-" * 78)
    fails = []

    # sqlite3.Row has no .get -- this crashed on EVERY food and the caller's
    # `except: continue` turned it into 100% NULL nutrition, silently shipped.
    cands = retrieve("rice", k=5)
    if not all(isinstance(c, dict) for c in cands):
        fails.append("retrieve() must return plain dicts (sqlite3.Row has no .get)")
    else:
        print("  ok   retrieve() returns plain dicts")

    # A WEAK match is a confidently wrong food. It must not contribute numbers.
    # hairtail (带鱼) is genuinely absent from USDA -- the resolver must say so
    # rather than hand back the nearest fish.
    verdict = classify("hairtail", (retrieve("hairtail", k=1) or [None])[0])
    if verdict in TRUSTED:
        fails.append(f"'hairtail' is absent from the bank but classified {verdict}")
    else:
        print(f"  ok   absent food -> {verdict} (not trusted)")

    # decompose must recover grams; without them there is no portion scaling.
    comps = decompose("Marinated egg 23 g\nRice 25 g")
    if comps != [("marinated egg", 23.0), ("rice", 25.0)]:
        fails.append(f"decompose lost the grams: {comps}")
    else:
        print("  ok   decompose() recovers (food, grams)")

    return fails


def run_l2_golden():
    """Known foods must land near their true carbs -- and not via the old wrong match."""
    print("\nL2  GOLDEN SET  (carbs per 100 g, as eaten)")
    print("-" * 78)
    print(f"  {'query':<26} {'match':<32} {'got':>6} {'want':>6}")
    fails = []

    for food, want, tol, must_not in GOLDEN:
        cands = retrieve(food, k=10)
        top = cands[0] if cands else None
        got = top["carbs"] if top and top["carbs"] is not None else None
        desc = top["description"] if top else "-"

        bad = []
        if got is None:
            bad.append("no match")
        elif abs(got - want) > tol:
            bad.append(f"carbs {got:.1f} outside {want}+/-{tol}")
        if must_not and top and must_not.lower() in desc.lower():
            bad.append(f"regressed onto '{must_not}'")

        mark = "FAIL" if bad else "ok  "
        got_s = f"{got:.1f}" if got is not None else "-"
        print(f"  {mark} {food:<26} {desc[:32]:<32} {got_s:>6} {want:>6}")
        if bad:
            fails.append(f"{food}: {'; '.join(bad)}")

    return fails


def run_l3_welldoc_benchmark():
    """Score the normalizer against WellDoc's app-DB macros -- the only ground truth.

    WellDoc's Diet rows carry FoodName AND all five macros, filled in by the
    WellDoc app's own food database. Hide the macros, feed only the name, and the
    normalizer can be graded. Shanghai can never be graded -- it has no labels --
    so a resolver only earns the right to run on Shanghai by passing here.

    Portion is unknown (WellDoc's macros are per serving, the bank is per 100 g),
    so the metric is the carb share of energy: dimensionless, portion-free.
    """
    import numpy as np
    import pandas as pd

    print("\nL3  WELLDOC HELD-OUT BENCHMARK")
    print("-" * 78)

    path = Path("/home/jluo41/WellDoc-SPACE/_WorkSpace/1-SourceStore/"
                "WellDoc2025CVS/@WellDocDataV251226/Diet.parquet")
    if not path.exists():
        print(f"  SKIP  {path} not found")
        return []

    df = pd.read_parquet(path)
    df = df[(df.Carbs > 0) & (df.Calories > 0)]
    # Multi-item rows join foods with ';' at unknown per-item portions -- not gradeable.
    single = df[~df.FoodName.str.contains(";", na=False)].drop_duplicates("FoodName")
    samp = single.sample(min(400, len(single)), random_state=0)

    rows = []
    for r in samp.itertuples():
        cands = retrieve(r.FoodName, k=10)
        top = cands[0] if cands else None
        rows.append(dict(
            q=classify(r.FoodName, top),
            true_carb=r.Carbs, true_kcal=r.Calories,
            pred_carb=(top["carbs"] if top and top["carbs"] is not None else np.nan),
            pred_kcal=(top["calories"] if top and top["calories"] is not None else np.nan),
        ))
    v = pd.DataFrame(rows)

    trusted_pct = v.q.isin(TRUSTED).mean() * 100

    e = v[v.q.isin(TRUSTED)].dropna(subset=["pred_carb", "pred_kcal"])
    e = e[(e.pred_kcal > 0) & (e.pred_carb > 0)]
    true_share = e.true_carb / e.true_kcal * 400      # % of energy from carbs
    pred_share = e.pred_carb / e.pred_kcal * 400
    mae = (true_share - pred_share).abs().mean()
    r = np.corrcoef(true_share, pred_share)[0, 1]

    print(f"  trusted coverage        {trusted_pct:5.1f}%   (n={len(v)})")
    print(f"  carb-share-of-energy    MAE {mae:5.1f} pp,  r = {r:.3f}   (n={len(e)})")

    # Baselines from 2026-07-12, the first run that produced any number at all.
    # These are floors to defend, not targets -- lower them only deliberately.
    fails = []
    if trusted_pct < 55:
        fails.append(f"trusted coverage {trusted_pct:.1f}% regressed below 55% floor")
    if mae > 15:
        fails.append(f"carb-share MAE {mae:.1f}pp regressed above 15pp ceiling")
    if r < 0.60:
        fails.append(f"carb-share r {r:.3f} regressed below 0.60 floor")
    if not fails:
        print("  ok   within baseline (coverage >=55%, MAE <=15pp, r >=0.60)")
    return fails


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", action="store_true",
                    help="also run L3 (needs 1-SourceStore, ~1 min)")
    args = ap.parse_args()

    fails = run_l1_contract() + run_l2_golden()
    if args.bench:
        fails += run_l3_welldoc_benchmark()

    print("\n" + "=" * 78)
    if fails:
        print(f"FAILED ({len(fails)})")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)
    print("PASSED")
