---
name: describe-food
description: "Normalize free-text food descriptions (any cohort's dialect) to USDA nutrition. Use when a Diet ProcName's FoodName column needs Calories/Carbs/Protein/Fat/Fiber/Sugar, when a SourceFn must enrich diet data, or when the FoodNorm lexicon needs rebuilding. Trigger: describe food, food to nutrition, resolve diet to USDA, fill nutrition columns, foodnorm, 食物营养归一化."
metadata:
  version: "0.6.0"
  last_updated: "2026-09-30"
  changelog: CHANGELOG.md
  measured: "69.1% of 71,673 Diet rows MEASURED, 5.7% ESTIMATED, 25.2% MISS. ESTIMATED carries median 2.0 g carb error, p90 15.0 g, 10% over 15 g."
---

Skill: describe-food
================================================================================


THE BANK LADDER, AND WHY THE CONFIDENCE WORDS CHANGED
================================================================================

Until 260822 every name went to one place -- USDA FDC, fuzzy-matched -- and came
back labelled GOOD / OK / ALIAS / WEAK / PARTIAL. Those words had never been
checked against anything.

They were checked on 260822, against 10,068 food names that WellDoc patients
logged with macros attached. GOOD is genuinely informative: carb-share MAE 0.122
against a 0.258 mean-guess baseline, median carb error 2.0 g. It also has a tail
that its own name denies:

    p90  15.0 g of carbohydrate       688 names (10.0%), covering 7,151 records
    p99  48.7 g

    'Pepsi (12 oz)'    USDA -> 0.00 g carbs, labelled GOOD.   Logged: 41 g.
    'Sprite (12 oz)'   USDA -> 0.00 g                          Logged: 38 g.
    'Chicken Alfredo'  USDA -> 0.00 g                          Logged: 55.8 g.
    'Collagen Powder'  USDA -> 79.7 g (it is pure protein)     Logged: 0 g.
    'air'              USDA -> 77.5 g, labelled GOOD.

For a CGM project a sugary drink read as zero carbohydrate is the worst single
error available, because it is also the sharpest glucose excursion there is.

AND THE TAIL IS NOT DETECTABLE FROM THE NAME. Six candidate signals were
measured against it -- a near-zero carb prediction, `with`/`and` compounds,
sugar-free/diet modifiers, beverage words, a parenthesised size, low support.
The best reached 2.4x lift over base rate on 72 names. Gating on three at once
discarded 25% of all answers to move the bad rate from 10.0% to 8.8%.

So the answer is not a smarter matcher and not a cleverer gate. It is: DO NOT
MATCH WHAT HAS ALREADY BEEN MEASURED.

    T0  observed   the exact string was logged, with macros attached
                   28,408 entries, ExternalStore/foodbank_observed/  -> MEASURED
    T1  catalog    RESERVED: FoodID -> the app's own food catalog     -> MEASURED
    T2  usda       fuzzy match against USDA FDC                       -> ESTIMATED
    T_CN china     the component's CHINESE original, exact name or    -> ESTIMATED
                   alias, in the China Food Composition Tables 6th ed.
                   (ext_food_bank_cn); only when T2 found no trusted
                   match and the caller passed name_zh_col
    T3  branded    USDA's 1.8M packaged products (ext_food_bank_branded) -> ESTIMATED
                   only for a ONE-FOOD meal, when T0 missed AND T2 found no
                   trusted match;
                   every content word of the name must be in the
                   product's description or brand; the answer is the
                   median over the top 5 such products
        none                                                          -> MISS

T_CN and T3 are OFF unless a release pins their table, or FOODNORM_CN_DB /
FOODNORM_BRANDED_DB names the file for an A/B run (`off` forces them off). A
release that pins neither (EventNormV3) answers exactly as before: re-asking all
35,549 frozen requests with this code under EventNormV3 agreed on every field
(b51 j01 t04 r06_parity_EventNormV3). A label or a book that leaves a nutrient out
leaves it EMPTY, never 0, and a meal that sums such a component is empty for that
nutrient.

A meal never mixes per SERVING with per 100 g: T0 is denominated per serving and
T2, T_CN and T3 per 100 g, and adding one to the other yields a number that is
neither. The three per-100 g banks are ONE family and do add up: 'Hairtail 80 g
+ Rice 100 g' is the China table's hairtail plus USDA's rice, with
NutritionSource `bank_usda+bank_cn`. The family (T0, or per 100 g) is picked by,
in order:

    1. CAN IT HONOUR THE STATED PORTION?  A log that says '141 g' has given
       better information than any bank's idea of a serving, and only T2 can be
       scaled to it. So when grams are stated, T2 wins -- which is why Shanghai,
       the one cohort that consumes this resolver today and states grams on
       every component, still resolves 97.9% ESTIMATED and is unharmed.
    2. COVERAGE.  One banana at T0 against three dishes at T2 is better
       described by the three.
    3. TIER QUALITY, as the tie-break.

WHAT T0 IS NOT: laboratory truth. FatSecret supplied 86.1% of these numbers,
Welldoc's own source 10.6%, Calorie Mama (a photo model) 2.0%, Nutritionix 1.3%.
They are WHAT THE APP TOLD THE PATIENT -- arguably the better modelling target,
since the patient dosed insulin against this figure and not against an assay,
but never to be called measured-in-a-lab. That is why the word is MEASURED and
not TRUE.

WHAT T0 DOES NOT DO: it does not make estimation more accurate. The T2 residual
is exactly what it was. It reduces HOW MANY ROWS DEPEND ON ESTIMATION.

    over all 71,673 Diet rows            MEASURED  49,508   69.1%
                                         ESTIMATED  4,087    5.7%
                                         MISS      18,078   25.2%

    WellDoc2025CVS   89.3% MEASURED      Shanghai   97.9% ESTIMATED (states grams)
    WellDoc2022CGM   84.3%               CGMacros / OhioT1DM / dubosson
    WellDoc2025ALS   72.5%                          100% MISS (no food name at all)
    WellDoc2025LLY   70.4%

    basis   per_serving 69.1%   per_meal 5.3%   per_100g 0.4%

That last line is the point of the whole exercise. `per_100g` means "we can tell
you what this food IS but not how much of it there was", and it used to be the
majority answer. A serving is a DOSE.

CIRCULARITY, stated plainly: T0 is built from WellDoc's own food log, so
measuring T0's accuracy against WellDoc names would be circular and no such
number is published here. T0 is not a prediction; it is a JOIN that recovers
per-item values the SourceFn discarded. The non-circular claim is the coverage
table above.


THE CONFIDENCE VOCABULARY
================================================================================

    MEASURED    the exact string was logged with these macros (T0/T1)
    ESTIMATED   fuzzy-matched (T2). Median carb error 2.0 g, p90 15.0 g,
                10.0% over 15 g, and that tail is not predictable.
    MISS        nothing trustworthy. Values are NULL.

`PARTIAL` is retired. It meant "some component did not resolve", folding
completeness into the confidence word so that one column answered two questions.
Completeness is now `NutritionCoverage`, the fraction of a meal's food components
the reported totals actually cover. 92.7% of resolved meals are at 1.0. Rule 5:
provenance never folds.

REBUILD T0 with
    python code/scripts/haibuilder/0-external/e14_build_external_foodbank_observed.py


Normalize a `Diet.parquet` `FoodName` column into `Calories / Carbs / Protein /
Fat / Fiber`, whatever dialect it was written in.


WHERE THE CODE LIVES
--------------------------------------------------------------------------------

The library ships INSIDE this skill. Docs, CLI, tests and implementation are one
thing, in one folder, versioned together.

    Tools/plugins/haipipe-utils/skills/describe-food/
        SKILL.md            you are here
        foodnorm/           <- THE LIBRARY
            client.py       normalize()  <- THE DOOR, and what callers use
            dialect.py      "Egg 50 g\nRice 25 g" -> typed components
            retrieve.py     component -> USDA candidates, scored and ranked
            aggregate.py    per-100g x grams/100, summed over components
            usda_db.py      the bank + score_candidate()
            imagename.py    stage 0, optional: photo -> food name
            llm_rerank.py   stage 3, optional: only what stage 2 could not resolve
            enrich.py       enrich_food_to_nutrition(), the DataFrame-shaped form
        pipeline.py         CLI wrapper
        test_foodnorm.py    regression + benchmark suite

It used to live at `code/haiutils/food_enrichment/`, which split one thing across
two repositories: the docs said one thing and the code did another, and the
skill's own CHANGELOG records the drift that followed. A normalizer belongs with
the skill that documents it.


HOW A CALLER REACHES IT
--------------------------------------------------------------------------------

Through ONE function, deliberately shaped like a third-party API call:

    from foodnorm import normalize
    out = normalize(["fried rice; egg", "Cucumber 100g"])

The caller knows that signature and nothing else -- not the dialect layer, not
the bank, not the stage sequence, not which repository any of them ship from.
All of those can move or be rewritten without a pipeline file changing.

`foodnorm` imports as a bare top-level name because the WORKSPACE says where its
skills are. That is what `env.sh` is for: a space is the unit of work, and each
space puts the normalizer skill dirs it wants on `PYTHONPATH`:

    _HAIPIPE_UTILS="${_REPO_ROOT}/Tools/plugins/haipipe-utils/skills"
    export PYTHONPATH="${_HAIPIPE_UTILS}/describe-food:${PYTHONPATH}"

Never write a path-shaped import. The repo package is named `code`, the Python
standard library also has a `code` module, and IPython imports the stdlib one at
startup -- so `from code.… import …` works under plain `python` and dies in any
notebook.

TRANSPORT is the one thing that varies, from `FOODNORM_TRANSPORT`:

    local   the default. In process, no service, no network, ~12 ms per meal.
            A cook must not fail because a daemon was down.
    http    POST $FOODNORM_URL/normalize/batch -- the same contract over the wire.

The service is `Tools/plugins/haipipe-utils/servers/api-food/server.py`, mounted at
`/food` by the plugin's host, `servers/_host/serve.py` (so `FOODNORM_URL` defaults to
`http://127.0.0.1:8070/food`); its 24 recorded request/response cases and its service suite
sit beside it. `foodnorm/` stays here; the arrow points from servers to skills only.


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

The door (what a SourceFn uses) -- batch, order-preserving, duplicates resolved once:

    from foodnorm import normalize

    out = normalize(df["FoodName"].fillna("").astype(str).tolist())
    # -> one dict per input: Calories, Carbs, Protein, Fat, Fiber, Sugar,
    #    NutritionSource, NutritionConf, NutritionBasis, NutritionCoverage
    # Sugar (total sugars, g) is empty, never 0, where no table gave one.

The DataFrame-shaped form, for a caller that already holds one and wants the
columns joined on. It exposes the stage sequence, so prefer the door:

    from foodnorm import enrich_food_to_nutrition
    df = enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2")

    # Shanghai logs in Chinese and FoodName is a translation. Pass the original
    # (one component per line, same order) so the China table can be reached:
    df = enrich_food_to_nutrition(df, food_col="FoodName", name_zh_col="FoodName_zh")
    # A string typed in Chinese needs nothing extra: normalize(["带鱼100g"]) reaches
    # the China table by itself. USDA (T2) never answers a Chinese name.

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

    NutritionSource   bank_observed | bank_usda | bank_cn | bank_branded | none,
                      or several per-100 g banks joined by + (bank_usda+bank_cn)
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

1. Branded foods now have their own table, ext_food_bank_branded (T3), for
   ONE-FOOD meals only. Open Food Facts US: gap 45.6% -> 24.4% on 10,000
   products, carb median error 0.32 g per 100 g (b51 j01 t19 r01). Still open:
   brewed coffee and size-only names ('cold brew iced coffee (venti)'), and
   branded items inside meals of several foods, where a per-100 g figure without
   grams cannot be combined with T0's servings.

2. Chinese composite dishes (红烧肉, 百叶包, 烂糊肉丝) exist in no public food
   composition table -- every official table, including 中国食物成分表, lists
   ingredients only. Only consumer databases (e.g. boohee, commercial) carry
   prepared dishes. The ingredients USDA lacks (带鱼, 茼蒿, 鲳鱼) are now reached
   through ext_food_bank_cn (T_CN, name_zh_col); Shanghai rows fully answered
   70.3% -> 73.5% (b51 j01 t19 r03).

3. Six nutrients are answered; Sugar joined in 0.6.0. WellDoc rows carry eight
   more (AddedSugars, Sodium, four kinds of fat, cholesterol, potassium) and no
   tier returns them yet. The China table gives no sugar, so a meal with a
   China-table food has an empty Sugar. A glycemic-index table is proposed but
   waits on a licence check of its two candidate sources.


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
