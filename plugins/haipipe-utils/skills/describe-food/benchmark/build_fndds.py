"""
Parse the USDA FNDDS 2021-2023 workbooks into a benchmark corpus.

WHY THIS ONE, AND WHY IT IS DIFFERENT FROM EVERY CELL WE HAVE
================================================================================
Every gradeable row in our own corpus is L2: the reference is FatSecret or the
app's own database, an estimator grading an estimator. And ten of eleven cohorts
state no portion, so absolute MAE has never been reportable -- the door answers
per_100g while the label is per meal, and comparing them measures portion size,
not food resolution.

FNDDS removes both problems at once:

    Foods and Beverages      food code -> a food DESCRIPTION, 7,000+ of them
    FNDDS Nutrient Values    food code -> 65 nutrients, PER 100 g
    Portions and Weights     food code -> 'l cup' -> the gram weight

    ▶ per 100 g on BOTH sides -> absolute MAE in grams, for the first time
    ▶ the reference is USDA's own analytical compilation, not a food app
    ▶ the portion table is a separate, independently gradeable task

WHAT IT IS NOT
================================================================================
Not our input distribution. 'Milk, NFS' is a trained coder's normalized
description; a patient types 'Just Carbs; dinner'. This grades the door's
CAPABILITY, not its DEPLOYMENT, and the two numbers must be reported apart.

    python build_fndds.py
"""
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[6]
D = ROOT / "_WorkSpace/ExternalStore/fndds_2021_2023"

CORE = {
    "Energy (kcal)": "Calories",
    "Carbohydrate (g)": "Carbs",
    "Protein (g)": "Protein",
    "Total Fat (g)": "Fat",
    "Fiber, total dietary (g)": "Fiber",
}


def main():
    if not (D / "Foods_and_Beverages.xlsx").exists():
        sys.exit(f"workbooks not found under {D}")

    foods = pd.read_excel(D / "Foods_and_Beverages.xlsx", sheet_name=0, header=1)
    nutr = pd.read_excel(D / "FNDDS_Nutrient_Values.xlsx", sheet_name=0, header=1)
    port = pd.read_excel(D / "Portions_and_Weights.xlsx", sheet_name=0, header=1)

    keep = ["Food code", "Main food description", "WWEIA Category description"]
    f = foods[keep + ["Additional food description"]].copy()
    n = nutr[["Food code"] + list(CORE)].rename(columns=CORE)
    food = f.merge(n, on="Food code", how="inner")
    food.columns = ["food_code", "description", "wweia_category", "extra_description",
                    *[CORE[k] for k in CORE]]
    for c in CORE.values():
        food[c] = pd.to_numeric(food[c], errors="coerce")

    p = port[["Food code", "Portion description", "Portion weight\n(g)"]].copy()
    p.columns = ["food_code", "portion_description", "grams"]
    p["grams"] = pd.to_numeric(p["grams"], errors="coerce")
    # 'Quantity not specified' carries no weight. It is the FNDDS equivalent of
    # our unstated portion, so it is kept and flagged rather than dropped.
    p["stated"] = p["grams"].notna()

    food.to_parquet(D / "fndds_food.parquet", index=False)
    p.to_parquet(D / "fndds_portion.parquet", index=False)

    (D / "PROVENANCE.md").write_text(
        "# FNDDS 2021-2023\n\n"
        "USDA Food and Nutrient Database for Dietary Studies, the database that\n"
        "converts What We Eat In America / NHANES 24-hour recalls into gram\n"
        "amounts and nutrient values.\n\n"
        "```text\n"
        f"  fndds_food.parquet     {len(food):,} food codes\n"
        "                         description + WWEIA category + 5 macros PER 100 g\n"
        f"  fndds_portion.parquet  {len(p):,} portion rows\n"
        "                         a natural-language portion phrase -> its gram weight\n"
        "```\n\n"
        "Downloaded 2026-08-22 from\n"
        "`https://www.ars.usda.gov/ARSUserFiles/80400530/apps/`\n"
        "(2021-2023 FNDDS At A Glance workbooks). Public domain, US Government work.\n\n"
        "WHAT IT IS: an analytical compilation maintained by USDA ARS, used for\n"
        "national dietary surveillance. WHAT IT IS NOT: our input distribution --\n"
        "these descriptions were written by trained coders, not typed by patients.\n",
        encoding="utf-8")

    print(f"foods   {len(food):>7,}  codes with all 5 macros: "
          f"{food[list(CORE.values())].notna().all(axis=1).sum():,}")
    print(f"portion {len(p):>7,}  with a stated gram weight: {p.stated.sum():,}")
    print(f"\n-> {D/'fndds_food.parquet'}")
    print(f"-> {D/'fndds_portion.parquet'}")
    print("\nsample:")
    print(food.head(5)[["food_code", "description", "Calories", "Carbs",
                        "Protein", "Fat", "Fiber"]].to_string(index=False))


if __name__ == "__main__":
    main()
