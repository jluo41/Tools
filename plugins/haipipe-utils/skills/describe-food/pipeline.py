#!/usr/bin/env python3
"""
CLI for the food → nutrition normalizer.

This is a thin wrapper. All the logic lives in the installed package:

    from foodnorm import enrich_food_to_nutrition

It used to be a 321-line orchestrator that re-implemented the stage sequence, and
it was dead on arrival: it did `from stages import stage_1_decompose`, but the
modules were named `1_decompose.py` -- a leading digit is not a Python identifier,
so every documented command raised ImportError. The stages now live in
`foodnorm` under importable names and the orchestration is
`enrich_food_to_nutrition()`, so there is nothing left for this file to do but
parse argv.

Usage:
    python pipeline.py <Diet.parquet> -o <out.parquet>
    python pipeline.py <Diet.parquet> -o <out.parquet> --stages 1-3   # + LLM rerank
    python pipeline.py --lexicon                                      # lexicon coverage
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

from foodnorm import enrich_food_to_nutrition, TRUSTED

LEXICON = Path("/home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/foodnorm/food_lexicon.parquet")


def show_lexicon():
    """Coverage of the pre-resolved lexicon that SourceFn joins against."""
    if not LEXICON.exists():
        print(f"No lexicon at {LEXICON}\n"
              f"Build it: python code/scripts/haibuilder/0-external/e12_build_external_foodnorm.py")
        return 1

    lex = pd.read_parquet(LEXICON)
    total = lex.n_mentions.sum()
    by_q = lex.groupby("quality").agg(components=("component", "size"),
                                      mentions=("n_mentions", "sum"))
    by_q["mention_%"] = (by_q.mentions / total * 100).round(1)

    print(f"FoodNorm lexicon: {len(lex):,} components, {total:,} mentions\n")
    print(by_q.sort_values("mentions", ascending=False).to_string())
    joinable = lex[lex.quality.isin(TRUSTED)].n_mentions.sum() / total * 100
    print(f"\njoinable (GOOD/OK/ALIAS): {joinable:.1f}% of mentions\n")

    for cohort in sorted({c for cs in lex.cohorts.dropna() for c in cs.split(",")}):
        sub = lex[lex.cohorts.str.contains(cohort, na=False)]
        cov = sub[sub.quality.isin(TRUSTED)].n_mentions.sum() / sub.n_mentions.sum() * 100
        print(f"  {cohort:<20} {len(sub):>6,} components   joinable {cov:5.1f}%")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", nargs="?", help="Diet.parquet with a FoodName column")
    ap.add_argument("-o", "--output", help="where to write the enriched parquet")
    ap.add_argument("--stages", default="1-2",
                    help="1-2 = decompose+retrieve+aggregate (free, default); "
                         "1-3 = + LLM rerank of WEAK/MISS (needs ANTHROPIC_API_KEY)")
    ap.add_argument("--food-col", default="FoodName")
    ap.add_argument("--lexicon", action="store_true",
                    help="show the pre-resolved lexicon's coverage and exit")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.lexicon:
        return show_lexicon()
    if not args.input:
        ap.error("give an input parquet, or --lexicon")

    df = pd.read_parquet(args.input)
    print(f"loaded {len(df):,} meals from {args.input}")

    out = enrich_food_to_nutrition(df, food_col=args.food_col,
                                   stages=args.stages, verbose=args.verbose)

    print(f"\nrows by confidence: {out.NutritionConf.value_counts().to_dict()}")
    print(out[["Calories", "Carbs", "Protein", "Fat", "Fiber"]]
          .describe().loc[["mean", "50%", "max"]].round(1).to_string())

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        out.to_parquet(args.output, index=False)
        print(f"\nwrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
