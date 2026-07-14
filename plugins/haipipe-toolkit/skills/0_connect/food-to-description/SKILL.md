---
name: food-to-description
description: "Normalize free-text food descriptions (any cohort's dialect) to USDA nutrition. Use when a Diet ProcName's FoodName column needs Calories/Carbs/Protein/Fat/Fiber, when a SourceFn must enrich diet data, or when the FoodNorm lexicon needs rebuilding. Trigger: food to nutrition, resolve diet to USDA, fill nutrition columns, foodnorm, 食物营养归一化."
metadata:
  version: "3.1.0"
  last_updated: "2026-07-12"
  changelog: CHANGELOG.md
  summary: "Library = haiutils.food_enrichment (installed). This skill = docs + CLI + tests."
  measured: "77.4% joinable overall (Shanghai 93.7%, WellDoc 83-91%), no LLM"
---

Skill: food-to-description
================================================================================

Normalize a `Diet.parquet` `FoodName` column into `Calories / Carbs / Protein /
Fat / Fiber`, whatever dialect it was written in.


WHERE THE CODE LIVES
--------------------------------------------------------------------------------

The library is an installed package. This skill is its docs, CLI and tests.

    code/haiutils/food_enrichment/     <- THE LIBRARY (pyproject.toml, editable)
        decompose.py       "Egg 50 g\nRice 25 g" -> [("egg",50.0), ("rice",25.0)]
        retrieve.py        component -> USDA candidates, scored and ranked
        llm_rerank.py      optional; only for what stage 2 could not resolve
        aggregate.py       per-100g x grams/100, summed over components
        usda_db.py         the bank + score_candidate()
        enrich.py          enrich_food_to_nutrition()  <- the entry point

    Tools/.../food-to-description/     <- THIS SKILL
        SKILL.md           you are here
        pipeline.py        CLI wrapper
        test_foodnorm.py   regression + benchmark suite

`haiutils` sits in `pyproject.toml` beside `haipipe` / `hainn` / `haifn`, so it
imports anywhere with no path juggling:

    from haiutils.food_enrichment import enrich_food_to_nutrition

Do NOT write `from code.haiutils import ...`. The repo package is named `code`,
the Python standard library also has a `code` module, and IPython imports the
stdlib one at startup -- so that form works under plain `python` and dies in any
notebook.


THE PROBLEM
--------------------------------------------------------------------------------

Eleven cohorts share one Diet column contract. The columns are uniform; what is
inside `FoodName` is not:

    WellDoc    "Toasted Whole Wheat Bread; Decaf Coffee"   item list, full macros
    Shanghai   "Egg 50 g\nRice 25 g"                       free text + grams, NO macros
    CGMacros   "Unknown"                                   the food is a photo
    OhioT1DM   "Unknown"                                   carbs only
    dubosson   "Unknown"                                   calories only

Five incompatible ways to say what somebody ate. This skill maps them all onto
one nutrient vector.


USAGE
--------------------------------------------------------------------------------

Package (what SourceFn uses):

    from haiutils.food_enrichment import enrich_food_to_nutrition

    df = enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2")
    # -> Calories, Carbs, Protein, Fat, Fiber, NutritionSource, NutritionConf

CLI:

    python pipeline.py <Diet.parquet> -o <out.parquet>
    python pipeline.py --lexicon              # coverage of the pre-resolved lexicon

Lexicon (what SourceFn should JOIN against, rather than re-resolving):

    python code/scripts/haibuilder/0-external/e12_build_external_foodnorm.py
    -> _WorkSpace/ExternalStore/@v1215/foodnorm/food_lexicon.parquet

Resolution is slow and its alias table needs human review, so it is done once and
versioned in ExternalStore -- the same way NDC/NPI reference data works.


HOW RETRIEVAL WORKS
--------------------------------------------------------------------------------

Two phases. The SQL/FTS tiers only RECALL; `score_candidate()` scores each
candidate over its FULL description and re-sorts. **Tier order is not rank
order** -- the tiers fire in priority order and use `ORDER BY length(description)`,
which systematically prefers the generic entry ("Cabbage, raw") over the specific
one ("Cabbage, chinese (pak-choi)").

Five scoring terms. Each exists because of a specific nutrition error that
actually happened -- they are hand-weighted, so `test_foodnorm.py` pins all five:

    coverage        of the query by the full description (dominant term)
    headword        USDA's first segment is the food's head noun, so plain "rice"
                    must not match "Soup, rice"          28g carbs -> 7g
    cooking state   "Millet, raw" is 72g carbs, "Millet, cooked" is 23g    (3x)
    added fat       "Fish, cod, fried" carries 11.7g carbs from the batter
    concentrated    "Milk, dry" is 52g carbs, fluid milk is 4.8g


THE CONTRACT
--------------------------------------------------------------------------------

Only GOOD / OK / ALIAS may be written into nutrition columns. WEAK and MISS stay
NULL. **A confidently wrong food is worse than a missing one.**

    NutritionSource   bank_usda | none
    NutritionConf     GOOD | PARTIAL | MISS

`PARTIAL` means some component of that meal did not resolve -- its totals
UNDERSTATE the meal, and downstream must be able to exclude it. Nutrition without
provenance is indistinguishable from measured nutrition.


MEASURED
--------------------------------------------------------------------------------

Joinable coverage, per cohort (`python pipeline.py --lexicon`):

    Shanghai          93.7%     generic ingredients
    WellDoc2025ALS    90.6%
    WellDoc2022CGM    85.8%
    WellDoc2025CVS    85.4%     branded / restaurant food
    WellDoc2025LLY    82.6%
    ------------------------
    all cohorts       77.4%     22,977 components, 128,334 mentions

Accuracy, graded against WellDoc's app-DB macros (`test_foodnorm.py --bench`):
carb share of energy MAE 12.6 pp, r = 0.705.

WellDoc is the only ground truth we have -- its rows carry FoodName AND all five
macros, filled in by the WellDoc app's own food database. Hide the macros, feed
only the name, and the normalizer can be graded. Shanghai can never be graded: it
has no labels. **A resolver earns the right to run on Shanghai by passing on
WellDoc.**


STAGE 3 (LLM) IS USUALLY NOT THE ANSWER
--------------------------------------------------------------------------------

The old 35% WEAK rate was a scoring bug: `classify()` measured coverage against
`description.split(",")[0]` only, and USDA's inverted naming puts the
discriminating words AFTER the comma ("Cabbage, chinese (pak-choi)"). Paying an
LLM to rerank was paying it to clean up after a broken retriever.

Fixing retrieval took trusted coverage from 62.9% to 92% on Shanghai, at zero
cost. What is left is mostly a *vocabulary* gap -- USDA has no entry for hairtail
(带鱼), crown daisy (茼蒿), pomfret (鲳鱼) at all -- and no amount of reranking a
candidate list repairs a bank that lacks the food.


CLOSED GAPS (2026-07-12)
--------------------------------------------------------------------------------

- `"just carbs"` -- was the lexicon's single biggest entry at 16,573 mentions, 11%
  of everything, and NOT A FOOD: a WellDoc app entry mode where the user types a
  carb count and names no food. Now in `PLACEHOLDERS`. Filtering it lifted WellDoc
  from ~70% to 83-91%. Its rows carry a true user-reported `Carbs` with
  Calories/Protein/Fat/Fiber = 0 in 100% of cases (vs 8-19% for real foods) --
  those zeros mean NOT MEASURED. A `NutritionSource="user_reported"` path that
  trusts Carbs and NULLs the rest is still to be wired into the Diet contract.

- `food.description` had no usable index, so every LIKE was a full scan of 101k
  rows and a lexicon build took 76 min. `idx_food_desc_nocase` (COLLATE NOCASE)
  plus dropping the `lower()` wrapper from the queries: 16.42 ms -> 0.10 ms, 164x.
  Build is now ~4 min. NOTE: the index must be COLLATE NOCASE and the query must
  use the bare column -- `lower(description) LIKE ?` is unindexable, and an index
  on `lower(description)` is not used either, because SQLite's LIKE is already
  case-insensitive and needs a NOCASE index to match.


OPEN GAPS
--------------------------------------------------------------------------------

1. The bank holds ZERO branded foods. USDA publishes 2,007,636 of them, free. This
   is what the residual 22.6% is made of, essentially without exception:

       657  coffee (brewed from grounds)
       308  whole grain oatmeal bread (pepperidge farm)
       238  cold brew iced coffee (venti)
       144  multi grain cheerios
       143  honey (sue bee)
       141  steel cut oats quick 3-minute (quaker)

   The index above was the prerequisite -- at 20x the rows, unindexed retrieval
   would be unusable. Importing is now the highest-value move, and its payoff is
   falsifiable: rerun `test_foodnorm.py --bench` and see whether r moves off 0.705.

2. Chinese composite dishes (红烧肉, 百叶包) exist in no public food composition
   table -- every official table, including 中国食物成分表, lists ingredients only.
   Only consumer databases (e.g. boohee, commercial) carry prepared dishes.
   Chinese INGREDIENTS that USDA lacks entirely (hairtail 带鱼, crown daisy 茼蒿,
   pomfret 鲳鱼) would be covered by 中国食物成分表 (1,677 items, free).


TESTS
--------------------------------------------------------------------------------

    python test_foodnorm.py           # L1 contract + L2 golden set
    python test_foodnorm.py --bench   # + L3 WellDoc held-out benchmark

    L1  contract    retrieve() returns dicts; an absent food -> MISS, not a
                    nearest-neighbour guess; decompose() keeps the grams
    L2  golden set  23 known foods must land within tolerance of their true carbs
                    AND must not have regressed onto the old wrong match
    L3  benchmark   floors: coverage >=55%, MAE <=15pp, r >=0.60

Run L2 after touching ANY scoring weight. Two regressions were introduced while
building the scorer and caught only by eyeballing output -- a wrong match still
returns a plausible number, so the failures are silent.
