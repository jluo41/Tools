"""
Food-to-Nutrition enricher — the orchestrator over decompose → retrieve → aggregate.

Resolves a free-text FoodName column into USDA nutrition, for any SourceFn whose
diet data is free text, in whatever dialect it was written:

    Shanghai   "Egg 50 g\\nRice 25 g"                 free text + grams
    WellDoc    "Toasted Bread; Decaf Coffee"          item list
    CGMacros   "Unknown"                              the food is a photo

All three parse as of 260819. The dialect layer (`dialect.split_meal`) splits
on ';' and newline, types every component, and keeps the app UI labels out of
the food bank by CLASSIFYING them rather than deleting them: 'Just Carbs' is a
carb declaration, 'dinner' is a meal slot, 'Unknown' is unnamed. QE1 D10 gate A
and gate B are both closed.

**Usage:**
    from foodnorm import enrich_food_to_nutrition

    df = enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2")
    # df now has: Calories, Carbs, Protein, Fat, Fiber,
    #             NutritionSource, NutritionConf, NutritionBasis

**Why at Source stage?**
- Source turns raw data into typed frames; nutrition is metadata about the food,
  like a clinical lab value.
- Record and AIData inherit it for free -- no Case function, no Record change.
"""
import pandas as pd
from typing import Optional

from .observed import lookup as observed_lookup


def enrich_food_to_nutrition(
    df: pd.DataFrame,
    food_col: str = "FoodName",
    stages: str = "1-2",
    image_col: Optional[str] = None,
    image_engine=None,
    image_root=None,
    cache_results: bool = True,
    on_error: str = "raise",
    verbose: bool = False,
    use_observed: bool = True,
) -> pd.DataFrame:
    """
    Enrich a DataFrame with USDA nutrition data by resolving FoodName strings.

    Converts free-text food descriptions to standardized USDA nutrition columns.
    Works with any SourceFn that has food data.

    **Args:**
        df: Input DataFrame with food names
        food_col: Column name containing food names (default: "FoodName")
        stages: Which pipeline stages to run:
                "1-2" = decompose + retrieve + aggregate (fast, free)
                "1-3" = + LLM rerank of WEAK/MISS (needs ANTHROPIC_API_KEY)
                Default "1-2": fixing the retriever took trusted coverage from
                62.9% to 92%, so stage 3 is rarely worth its cost. See SKILL.md.
        image_col: Column of image paths, comma-separated, for cohorts that
                   photograph the meal instead of naming it. When set together
                   with an image_engine, STAGE 0 runs first and derives a food
                   name for every row that names no food. Default None: the
                   images are not read.
        image_engine: Name or callable from `imagename.ENGINES`. Default None
                   resolves through FOODNORM_IMAGE_ENGINE, itself defaulting to
                   "null" -- so nothing reads an image unless it was asked to.
        image_root: Directory, or a callable row -> directory, that relative
                   image paths are joined against. CGMacros stores
                   'photos/x.jpg' relative to its own subject folder, so where
                   the photos live is a property of the cohort, not of this
                   stage.
        cache_results: Cache resolved components across meals (default: True)
        use_observed: consult the T0 observed bank before USDA (default: True).
            Set False to measure the ladder against the USDA-only baseline; that
            is how the T0 numbers in SKILL.md were produced.
        on_error: "raise" (default) or "skip" (leave NaN on failure).
                  Defaults to raise: this enricher once threw on every single row
                  and a caller's `except: continue` shipped a SourceSet with 100%
                  NULL nutrition. Silence is the expensive failure mode.
        verbose: Print progress details (default: False)

    **Returns:**
        DataFrame with added columns:
            Calories, Carbs, Protein, Fat, Fiber   scale given by NutritionBasis
            NutritionSource                        bank_usda | bank_usda|img:<engine> | none
            NutritionConf                          GOOD | PARTIAL | MISS
            NutritionBasis                         per_meal | per_100g | None
            NameSource                             typed | <engine id>
            NameConf                               the engine's own 0-1, else None

        NameSource/NameConf accompany a name this library DERIVED rather than
        read. They are separate from NutritionConf on purpose: NutritionConf
        answers "did the bank recognise this food", NameConf answers "was it
        the right food to look up", and these fail independently. Collapsing
        two different failures into one column is the bug gate B was: a meal
        whose food did not resolve and a meal that stated no portion shared one
        `continue`, and every gram-free cohort read as 100% MISS while its
        foods matched at GOOD. NutritionSource carries the `|img:` tag so a
        downstream reading only that one column still cannot mistake a
        model-named meal for a reported one.

        NutritionBasis is NOT a diagnostic and must be read before the numbers
        are compared or pooled:
            per_meal   every component stated a portion; values are the meal
            per_100g   at least one component stated none; values are the sum
                       over components of their per-100g nutrition. A portion
                       is never invented, so this is what the log supports.
            None       accompanies MISS
        Of eleven cohorts only Shanghai states portions (99.2% of components);
        every other cohort resolves at per_100g. Pooling the two without this
        column compares a meal against a reference portion.

    **Example:**
        df = enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2")
    """
    from .dialect import split_meal, foods
    from .retrieve import retrieve, classify

    # Stage 3 needs ANTHROPIC_API_KEY and the anthropic SDK; both are optional.
    try:
        from .llm_rerank import rerank_via_claude
    except Exception:
        rerank_via_claude = None

    # Validate inputs
    if food_col not in df.columns:
        raise ValueError(f"Column '{food_col}' not found in DataFrame")

    # Initialize output columns.
    # NutritionSource/NutritionConf are part of the contract, not diagnostics:
    # a WEAK match is a confidently wrong number, and downstream must be able to
    # exclude it. Nutrition without provenance is indistinguishable from measured.
    df = df.copy()  # Don't modify original
    df["Calories"] = None
    df["Carbs"] = None
    df["Protein"] = None
    df["Fat"] = None
    df["Fiber"] = None
    df["NutritionSource"] = None   # bank_usda | none
    df["NutritionConf"] = None     # GOOD | PARTIAL | MISS
    df["NutritionBasis"] = None    # per_meal | per_100g | None
    df["NameSource"] = "typed"     # typed | <engine id>
    df["NameConf"] = None          # the engine's own 0-1 for a derived name

    # ── STAGE 0 · image -> food name ────────────────────────────────────────
    # Runs before anything else, because every stage after it takes a STRING.
    # It rewrites nothing the caller passed in: the derived name goes into its
    # own working series, and `food_col` still holds what the cohort wrote.
    work = df[food_col].astype(object).copy()

    if image_col and image_engine is not None:
        from .imagename import read_images

        if image_col not in df.columns:
            raise ValueError(f"Column '{image_col}' not found in DataFrame")

        # WHICH rows need stage 0 is the dialect layer's judgment, not a second
        # copy of its placeholder set. A row needs an image read when the string
        # it carries names no food -- 'Unknown', 'Just Carbs', 'dinner', ''.
        needs = [i for i, v in work.items() if not foods(split_meal("" if pd.isna(v) else str(v)))]

        # Path joining is the cohort's business: CGMacros writes
        # 'photos/x.jpg' relative to each subject's own folder.
        def _abspaths(i):
            raw = df.at[i, image_col]
            if raw is None or (isinstance(raw, float) and pd.isna(raw)):
                return []
            parts = [s.strip() for s in str(raw).split(",") if s.strip() not in ("", "nan", "None")]
            if image_root is None:
                return parts
            root = image_root(df.loc[i]) if callable(image_root) else image_root
            return [str(root) + "/" + s if not s.startswith("/") else s for s in parts]

        targets = [(i, _abspaths(i)) for i in needs]
        targets = [(i, paths) for i, paths in targets if paths]

        if verbose:
            print(f"Stage 0: {len(targets)} rows name no food and carry images")

        if targets:
            reads = read_images([paths for _, paths in targets], engine=image_engine)
            n_read = 0
            for (i, _paths), r in zip(targets, reads):
                if r is None or not r.food_name:
                    continue
                work.at[i] = r.food_name
                df.at[i, "NameSource"] = r.engine
                df.at[i, "NameConf"] = r.conf
                n_read += 1
            if verbose:
                print(f"Stage 0: {n_read}/{len(targets)} rows named")

    # The string actually looked up, derived or typed. Without it a derived
    # name would be unauditable: the caller's column still says 'Unknown' and
    # nothing else records what the bank was asked for.
    df["FoodNameResolved"] = work

    # Parse stages
    stages_list = [int(s) for s in stages.split("-")]
    min_stage, max_stage = min(stages_list), max(stages_list)

    # A meal string is resolved COMPONENT by component, never as one query.
    # "Egg 50 g\nRice 25 g\nVegetable 100 g" is not a food -- retrieving it as
    # a single string (the previous behaviour) asks USDA to name a meal.
    #
    # Caching is therefore at component level, where the reuse actually is:
    # Shanghai has 3,130 distinct meal strings but only ~2,000 distinct
    # components, and the common ones (rice, egg) recur in thousands of meals.
    comp_cache = {}

    NUTRIENT_KEYS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")
    _BANK_KEY = {"Calories": "calories", "Carbs": "carbs", "Protein": "protein",
                 "Fat": "fat", "Fiber": "fiber"}
    # Only these may be written into nutrition columns. A WEAK rank-1 is a
    # confidently wrong food; propagating its numbers is worse than a NULL.
    TRUSTED = ("GOOD", "OK", "ALIAS")

    # THE BANK LADDER. A component is resolved at the highest tier that has it,
    # and a meal is summed at ONE tier only -- T0 is per SERVING and T2 is per
    # 100 g, and adding one to the other yields a number that is neither.
    #
    #   T0 observed   this exact string was logged, with numbers   MEASURED
    #   T2 usda       fuzzy match against USDA FDC                 ESTIMATED
    #
    # T0 exists because the T2 error tail is real and undetectable: calibrated
    # 260822 over 10,068 logged names, T2's median carb error is 2.0 g but 688
    # names (10.0%) are wrong by more than 15 g, and six candidate signals for
    # spotting them topped out at 2.4x lift on 72 names. 'Pepsi (12 oz)' came
    # back from USDA at 0.00 g carbs labelled GOOD; it was logged with 41 g.
    T_OBS, T_USDA = "observed", "usda"
    TIER_RANK = {T_OBS: 0, T_USDA: 1}

    def resolve_t0(name):
        """name -> per-SERVING dict, or None. An exact retrieval, never a match."""
        if not use_observed:
            return None
        obs = observed_lookup(name)
        return obs["values"] if obs else None

    def resolve_t2(name):
        """name -> per-100 g dict or None, plus the legacy quality word.

        Computed ONLY when it can be used: when T0 missed, or when the log
        stated a gram amount. T0 cannot honour a stated portion -- its servings
        have no mass in the bank -- so a gram-bearing component needs T2 even if
        T0 has it. Skipping the query otherwise keeps a cook from paying ~12 ms
        of FTS5 per distinct component it will not use."""
        if name in comp_cache:
            return comp_cache[name]

        candidates = retrieve(name, k=10)
        top = candidates[0] if candidates else None
        quality = classify(name, top)

        if min_stage <= 3 <= max_stage and quality in ("WEAK", "MISS") and rerank_via_claude and candidates:
            rerank = rerank_via_claude(name, candidates)
            if rerank and rerank.get("fdc_id"):
                picked = next((c for c in candidates if c["fdc_id"] == rerank["fdc_id"]), None)
                if picked:
                    top, quality = picked, "OK"

        per100 = None
        if top and quality in TRUSTED:
            per100 = {k: (float(top[_BANK_KEY[k]]) if top.get(_BANK_KEY[k]) is not None else 0.0)
                      for k in NUTRIENT_KEYS}

        out = (per100, quality)
        if cache_results:
            comp_cache[name] = out
        return out

    # Keyed on the working series: a derived name must go through the same
    # dialect -> retrieve -> aggregate path as a typed one, and two rows whose
    # photos yielded the same name must still share one cache entry.
    unique_meals = work.dropna().unique()
    if verbose:
        print(f"Processing {len(unique_meals)} unique meal strings across {len(df)} rows")

    meal_cache = {}
    for idx, meal in enumerate(unique_meals):
        if verbose and idx % 200 == 0:
            print(f"  {idx}/{len(unique_meals)}  (components cached: {len(comp_cache)})")

        try:
            # Typed components, then the food subset. A carb declaration or a
            # meal slot is NOT a failure to resolve, so it must not sit in the
            # denominator: 'Just Carbs; Fried Egg' with the egg resolved is
            # GOOD, and counting the declaration would print PARTIAL for a
            # meal in which every food was found.
            components = split_meal(meal)
            food_components = foods(components)
            n_total = len(food_components)

            # Two DIFFERENT failures used to share one `continue`: the bank did
            # not recognise the food, and the log did not state a portion. Only
            # the first is unresolvable. Collapsing them made every gram-free
            # cohort MISS at 100% while its foods were matching at GOOD -- on
            # 150 single-component WellDoc rows, 90 components matched and 0
            # carried grams, so all 90 were discarded. See QE1 D10, gate B.
            resolved = []
            for c in food_components:
                t0 = resolve_t0(c.name)
                if t0 is not None:
                    resolved.append((c.amount_g, t0, T_OBS))
                # T2 is still worth having when the log stated grams, because
                # only T2 can be scaled to them.
                if t0 is None or c.amount_g is not None:
                    t2, _q = resolve_t2(c.name)
                    if t2 is not None:
                        resolved.append((c.amount_g, t2, T_USDA))

            if n_total == 0 or not resolved:
                nutrition = {k: None for k in NUTRIENT_KEYS}
                nutrition["NutritionSource"] = "none"
                nutrition["NutritionConf"] = "MISS"
                nutrition["NutritionBasis"] = None
                nutrition["NutritionCoverage"] = 0.0 if n_total else None
            else:
                # PICK ONE TIER FOR THE WHOLE MEAL, never a mixture: a
                # per-serving figure added to a per-100 g figure is neither.
                # The pick is ordered
                #
                #   1. CAN IT HONOUR THE STATED PORTION?
                #      A log that says '141 g' has given better information
                #      than any bank's idea of a serving, and only T2's
                #      per-100 g values can be scaled to it -- T0 is
                #      denominated in servings whose mass the bank does not
                #      know ('cup', 'large', 'medium (7" to 7-7/8" long)').
                #      So when grams are stated, T2 wins. Shanghai, the one
                #      cohort that consumes this resolver today, states grams
                #      on every component; ignoring them to use a serving
                #      default turned a correct 4.2 g cucumber into 0.15 g.
                #   2. COVERAGE. One banana at T0 against three dishes at T2 is
                #      better described by the three, and NutritionConf tells
                #      the reader which they got.
                #   3. TIER QUALITY, as the tie-break.
                by_tier = {}
                for amt, vals, tier in resolved:
                    by_tier.setdefault(tier, []).append((amt, vals))

                def _pick(t):
                    grams = all(a is not None for a, _ in by_tier[t])
                    return (1 if (grams and t == T_USDA) else 0,
                            len(by_tier[t]), -TIER_RANK[t])

                tier = max(by_tier, key=_pick)
                at_tier = by_tier[tier]
                n_resolved = len(at_tier)
                # Portion basis is a MEAL-level property, because summing a
                # gram-scaled component with an unscaled one yields a number
                # that is neither. A portion is never invented: if any resolved
                # component lacks grams the whole meal is reported per 100 g of
                # each component, and the basis column says so.
                if tier == T_OBS:
                    # T0 values are PER SERVING of the named food, and a
                    # serving's mass is not in the bank -- 'cup', 'large',
                    # 'medium (7" to 7-7/8" long)'. So a stated gram amount
                    # cannot scale them and is deliberately NOT applied; the
                    # basis column says per_serving and means it.
                    total = {k: 0.0 for k in NUTRIENT_KEYS}
                    for _amt, vals in at_tier:
                        for k in NUTRIENT_KEYS:
                            total[k] += vals[k]
                    nutrition = {k: round(v, 2) for k, v in total.items()}
                    nutrition["NutritionSource"] = "bank_observed"
                    nutrition["NutritionConf"] = "MEASURED"
                    nutrition["NutritionBasis"] = "per_serving"
                else:
                    stated = all(amt is not None for amt, _ in at_tier)
                    total = {k: 0.0 for k in NUTRIENT_KEYS}
                    for amount_g, per100 in at_tier:
                        scale = (amount_g / 100.0) if stated else 1.0
                        for k in NUTRIENT_KEYS:
                            total[k] += per100[k] * scale
                    nutrition = {k: round(v, 2) for k, v in total.items()}
                    nutrition["NutritionSource"] = "bank_usda"
                    nutrition["NutritionConf"] = "ESTIMATED"
                    nutrition["NutritionBasis"] = "per_meal" if stated else "per_100g"

                # Completeness is its OWN question and now its own column. It
                # used to be folded into the confidence word as `PARTIAL`,
                # which made one column answer two things: where the numbers
                # came from, and how much of the meal they cover. Rule 5.
                nutrition["NutritionCoverage"] = round(n_resolved / n_total, 3)

        except Exception as e:
            if on_error == "raise":
                raise
            if verbose:
                print(f"  ⚠️ Meal {meal!r}: {e}")
            nutrition = {k: None for k in NUTRIENT_KEYS}
            nutrition["NutritionSource"] = "none"
            nutrition["NutritionConf"] = "MISS"
            nutrition["NutritionBasis"] = None
            nutrition["NutritionCoverage"] = None

        meal_cache[meal] = nutrition

    for col in list(NUTRIENT_KEYS) + ["NutritionSource", "NutritionConf",
                                      "NutritionBasis", "NutritionCoverage"]:
        df[col] = work.map(lambda m: meal_cache.get(m, {}).get(col) if pd.notna(m) else None)

    # Tag the provenance into NutritionSource too. A downstream that reads only
    # this one column must still be unable to mistake a model-named meal for a
    # reported one -- the name is the same TYPE either way, which is what makes
    # stage 0 the easiest place in the library to launder a guess.
    # Tag EVERY resolved tier, not just bank_usda. Pinning this to one tier was
    # a rule-5 break introduced with the ladder: a photo-derived name that hit
    # the observed bank came back as plain `bank_observed`, so a model's guess
    # became indistinguishable from a patient's own report. Written against the
    # general condition so a future T1 is covered without this line changing.
    derived = (df["NameSource"].ne("typed")
               & df["NutritionSource"].notna()
               & df["NutritionSource"].ne("none"))
    if derived.any():
        df.loc[derived, "NutritionSource"] = (
            df.loc[derived, "NutritionSource"].astype(str)
            + "|img:" + df.loc[derived, "NameSource"].astype(str))

    if verbose:
        conf = df["NutritionConf"].value_counts(dropna=False).to_dict()
        print(f"✅ Rows by confidence: {conf}")
        print(f"   Unique components resolved: {len(comp_cache)}")

    return df
