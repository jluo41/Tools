CHANGELOG — food-to-description
================================================================================


0.3.1 — 2026-07-24
--------------------------------------------------------------------------------

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 3.1.0; older entries below keep their original numbers).

3.1.0 — 2026-07-12
--------------------------------------------------------------------------------

Coverage 68.5% -> 77.4%; lexicon build 76 min -> 4 min. Two orthogonal fixes.

- `"just carbs"` added to PLACEHOLDERS. It was the lexicon's single biggest entry
  -- 16,573 mentions, 11% of everything -- and it is not a food: it is a WellDoc
  app entry MODE where the user types a carb count and names no food. We were
  looking up a UI label in a food bank, which can only ever match wrongly. It also
  appears as one component of composites ("Just Carbs; White Rice", 2,018 rows),
  so the filter is applied per COMPONENT, not per meal string.

  Its rows carry a true user-reported Carbs, with Calories/Protein/Fat/Fiber = 0
  in 100% of cases against 8-19% for real foods -- structurally false zeros that
  mean NOT MEASURED. Anyone averaging calories over WellDoc is being diluted by
  ~13,000 of them. A `NutritionSource="user_reported"` path is still to be wired.

  Effect: WellDoc2025ALS 68.3% -> 90.6%, 2022CGM 71.6% -> 85.8%,
  2025CVS 69.9% -> 85.4%, 2025LLY 70.5% -> 82.6%. Shanghai unchanged (it has none).

- sqlite index on `food.description`. The queries wrapped the column in `lower()`,
  which is unindexable, so every recall tier full-scanned 101k rows: 16.42 ms per
  query, 76 min for a 23k-component build. `idx_food_desc_nocase`
  (description COLLATE NOCASE) + the bare column: SCAN -> SEARCH USING INDEX,
  0.10 ms, 164x. Retrieval results are unchanged (r 0.705 -> 0.704, float noise).

  The subtlety: an index on `lower(description)` does NOT work either. SQLite's
  LIKE is already case-insensitive, so it only uses a COLLATE NOCASE index, and
  only when the LHS is a bare column.

  This was the prerequisite for USDA Branded Foods (2,007,636 rows, 20x this bank)
  -- unindexed, that import would make retrieval unusable.

- `e12_build_external_foodnorm.py`: `parents[3]` -> `find_repo()`. Moving the file
  from `_WorkSpace/code-dev/0-EXTERNAL/` to `code/scripts/haibuilder/0-external/`
  silently repointed REPO at `code/`, so SOURCE_STORE did not exist, the glob
  matched nothing, and the build printed "0 unique components" and exited 0 in
  0.3 s -- leaving the old lexicon in place and reporting success. A guard now
  raises when the harvest is empty. (Second time this session that counting
  parent directories produced a wrong path; the first was `parents[2]` in enrich.)


3.0.0 — 2026-07-12
--------------------------------------------------------------------------------

Moved the library into `haiutils`; the skill is now docs + CLI + tests.

STRUCTURAL

- The resolver moved OUT of this skill and INTO `code/haiutils/food_enrichment/`,
  an installed package (pyproject.toml lists it beside haipipe/hainn/haifn).
  The dependency was backwards: an installed package (`haiutils`) reached out
  through `sys.path.insert()` to import code living in a skill directory. Every
  peripheral bug traced back to that one inversion --

    * `stages/1_decompose.py` etc. began with a digit, so
      `from stages import stage_1_decompose` could never resolve. The entire
      documented CLI was dead on arrival (audit finding C1, filed 2026-07-05).
    * `enrich_food_to_nutrition` carried ~40 lines of
      `importlib.util.spec_from_file_location` to work around C1.
    * Callers wrote `from code.haiutils import ...`, which collides with the
      Python standard library's `code` module -- IPython imports the stdlib one at
      startup, so that form works under `python` and dies in any notebook.
    * A hand-counted `parents[2]` pointed at `code/Tools/...` and only ever worked
      via a cwd fallback.

  All four are gone, not fixed: with importable module names there is nothing to
  alias, no path to compute, and no prefix to collide.

  `stages/` + `utils/` deleted (content preserved in git history and in the new
  package). `pipeline.py` went from a 321-line orchestrator to a ~95-line argv
  parser over `enrich_food_to_nutrition()`.

- CHANGELOG.md added; SKILL.md gains `summary:` + `changelog:` (audit finding E1).

CORRECTNESS — six bugs, each verified by execution

- `sqlite3.Row` has no `.get`, so `classify()` threw on EVERY food. The SourceFn
  caller wrapped it in `except Exception: print(warning); continue`, so the
  SourceSet was built anyway with Carbs/Calories/Protein/Fat/Fiber 100% NULL. It
  shipped that way and nobody noticed. `fts_topk()` now returns plain dicts, and
  the SourceFn no longer swallows the failure (`on_error='raise'` + an assertion
  that >50% of meals resolved).

- `classify()` measured coverage against `description.split(",")[0]` only. USDA's
  inverted naming puts the discriminating word AFTER the comma, so the query
  "chinese cabbage" scored 50% against its own correct match ("Cabbage, chinese
  (pak-choi), cooked") and was labelled WEAK. This one line produced most of the
  35% WEAK rate.

- Retrieval tiers were treated as rank order and used `ORDER BY length(description)`,
  which systematically prefers the generic entry over the specific one. Retrieval
  is now two-phase: tiers RECALL, `score_candidate()` RANKS.

- `enrich_food_to_nutrition` computed `decompose(food)` and then threw the result
  away, querying USDA with the entire multi-line meal string as if it were one
  food name.

- It never called stage 4, so per-100g bank values were written straight into
  `Carbs` as though they were the meal total. Nutrition is now
  `sum over components of (per100g x grams / 100)`.

- `_stem()` folded only a trailing "s", so USDA's "Tomatoes, raw" stemmed to
  "tomatoe" and never met the query "tomato" -- raw tomato could not enter scoring
  and the query landed on "Tomato, green, pickled".

SCORING — `score_candidate()`, five terms, each defending against a real error

    coverage        of the query by the FULL description (dominant)
    headword        "rice" must not match "Soup, rice"        28g carbs -> 7g
    cooking state   "Millet, raw" 72g vs "Millet, cooked" 23g       (3x)
    added fat       "Fish, cod, fried" = 11.7g carbs of batter
    concentrated    "Milk, dry" 52g vs fluid milk 4.8g

  Two of these were added after the term above it caused a regression: raising the
  dilution penalty sent "rice" to rice soup; adding milk to a raw-edible list sent
  it to milk powder. Neither raised an exception. Both would have shipped.

CONTRACT

- New columns `NutritionSource` (bank_usda | none) and `NutritionConf`
  (GOOD | PARTIAL | MISS). Only GOOD/OK/ALIAS may be written into nutrition
  columns; WEAK/MISS stay NULL. PARTIAL means a component of the meal did not
  resolve, so the totals understate it.

TESTS — `test_foodnorm.py`, new

    L1  contract    retrieve() returns dicts; absent food -> MISS; grams survive
    L2  golden set  23 foods, carbs within tolerance AND not regressed onto the
                    old wrong match (`must_not`)
    L3  benchmark   WellDoc's app-DB macros held out: coverage 62.7%,
                    carb-share MAE 12.6 pp, r = 0.705. Floors: >=55%, <=15pp, >=0.60.

  This is the first accuracy number the pipeline has ever had.

MEASURED

    Shanghai trusted coverage   62.9%  ->  92.0%     (no LLM, no cost)
    Shanghai WEAK               35.4%  ->   6.3%
    Lexicon, all cohorts        22,978 components, 68.5% joinable

OPEN

- `"just carbs"`: 16,573 mentions (11% of all) and not a food -- a WellDoc app
  entry mode. Belongs in PLACEHOLDERS on a `user_reported` path.
- The bank holds ZERO of USDA's 2,007,636 free branded foods. This is the whole
  reason WellDoc resolves at ~70% against Shanghai's 94%.
- No index on `food.description`; a full lexicon build takes ~76 min. Index BEFORE
  importing branded foods.


2.0.0 — 2026-06-02
--------------------------------------------------------------------------------

Initial 4-stage pipeline (decompose / retrieve / llm_rerank / aggregate).
Never produced a nutrition value: the CLI could not import its own stages, and the
library path threw on every row. See 3.0.0.
