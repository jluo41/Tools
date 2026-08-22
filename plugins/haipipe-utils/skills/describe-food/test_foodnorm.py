#!/usr/bin/env python3
"""
Regression + benchmark suite for the food -> nutrition normalizer.

    python test_foodnorm.py            # L1 + L2. Fast, no cohort data needed.

L3 IS GONE. It lived here as a 400-row single-item sample of ONE cohort, called
`retrieve`/`classify` directly, and reported one weighting. Every one of those
was a limit worth removing:

  it never called `enrich_food_to_nutrition`, so it graded the retriever rather
    than the pipeline that ships, and a defect that made ten of eleven cohorts
    MISS was invisible to it for as long as it existed (QE1 D10 gate B)
  it dropped rows containing ';', which is 59.5% of WellDoc and the LARGEST
    gradeable class at 27,665 rows
  its r = 0.704 was the DEDUPED weighting presented as the number; the
    row-weighted figure on the same rows is 0.821

The replacement grades the API itself, over 11 SHAPE x LABEL cells, under both
weightings, with a PatientID-level split:

    examples/ProjA-CGM-Raw2AIData/tasks/AY1_foodrec_v1/00_benchmark/
      python build_gold.py                      # freeze the corpus
      python run_bench.py --n 400 --tag <name>  # grade it

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

Both run in seconds and need no cohort data. That is the point: this file is the
guard rail you run by reflex after touching `score_candidate`. Corpus-scale
grading is the benchmark's job, not this file's.
"""
import sys
import argparse
from pathlib import Path

from foodnorm import decompose, retrieve, classify, TRUSTED

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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", action="store_true",
                    help="retired; the benchmark moved, see the module docstring")
    args = ap.parse_args()

    if args.bench:
        print("--bench is retired. Corpus-scale grading now lives at\n"
              "  examples/ProjA-CGM-Raw2AIData/tasks/AY1_foodrec_v1/00_benchmark/\n"
              "and grades the API rather than the retriever. Running L1 + L2 only.\n")

    fails = run_l1_contract() + run_l2_golden()

    print("\n" + "=" * 78)
    if fails:
        print(f"FAILED ({len(fails)})")
        for f in fails:
            print(f"  - {f}")
        sys.exit(1)
    print("PASSED")
