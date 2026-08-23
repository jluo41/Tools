"""
The UNIT INVENTORY of describe-food, one folder per corpus.

WHY THIS FILE EXISTS
================================================================================
`gold_index.parquet` is a ROW index: 71,673 meals, one row each. It answers
"how often", never "how many DIFFERENT things are we asked to resolve". The
second question is the one a person can act on, and for food it needs a step
exercise and medication do not: A ROW IS NOT A THING. One Diet row is a whole
meal, and `split_meal()` is what turns it into the things.

    "Multi Grain Cheerios; 2% Fat Milk; banana"   ->  3 components
    64,317 WellDoc rows  ->  116,941 mentions  ->  21,065 distinct units

MEMBERSHIP IS 'THIS CORPUS HAS FOOD CONTENT', NOT 'THIS CORPUS HAS AN ANSWER'.
Three corpora here have a vocabulary of exactly one word, "Unknown", and they
are here anyway -- because a reader must be able to tell 'we looked and there
was nothing to resolve' from 'we never looked'. Corpora with no Diet content
at all are named in `_empty.md` for the same reason.

WHAT A UNIT IS DIFFERS BY CORPUS, AND THE TABLE SAYS SO
================================================================================
    item_string        a component of a ';' list, portion not stated
    item_grams         a component that states its own grams (Shanghai)
    class_word         a single word standing in for every meal ("Unknown")
    fndds_description  a nutrition coder's normalized phrase
    ingredient_name    a generic weighed component
    brand_product      a manufacturer's product name

WHY ONE CORPUS RESOLVES AGAINST A DIFFERENT BANK
================================================================================
Our USDA sqlite ships `survey_fndds_food`, one row per FNDDS code. Resolving
the FNDDS corpus against it is a SELF-JOIN: measured 260822 at carb MAE 0.31
with a median of exactly 0.00, against 8.21 / 2.71 once the table is removed.
So FNDDS declares `bank_config = usda_holdout` and every other corpus declares
`production`. The column is in the parquet, not only in this docstring.

CODE LIVES IN GIT, DATA DOES NOT. Everything written here lands under
_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/2-corpus/.

    source .venv/bin/activate && source env.sh
    python build_units.py                 # all corpora
    python build_units.py --only WellDoc  # one of them
"""
import argparse
import collections
import re
import json
import os
import pathlib
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))            # describe-food/

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
SOURCE = ROOT / "_WorkSpace/1-SourceStore"
EXT = ROOT / "_WorkSpace/ExternalStore"
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"
OUT = INFO / "2-corpus"
HOLDOUT_DB = INFO / "6-benchmark/bank_usda_holdout/usda_no_survey_fndds_food.sqlite"

MIN_GOLD_N = 30          # below this a per-unit macro median is not worth reading
RULER_MIN_N = 10         # the split ruler's floor; see build_split_ruler()
TRAIN_BANK = INFO / "6-benchmark/observed_train.parquet"
NUTRIENTS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")

WELLDOC = ["WellDoc2022CGM", "WellDoc2025ALS", "WellDoc2025CVS", "WellDoc2025LLY"]


# ── the corpora ──────────────────────────────────────────────────────────────
CORPORA = [
    dict(name="WellDoc", kind="ours", cohorts=WELLDOC, unit_is_a="item_string",
         ruler="I1_LOGGED", ruler_split=True),
    dict(name="Shanghai", kind="ours", cohorts=["Shanghai"], unit_is_a="item_grams",
         ruler=None),
    dict(name="CGMacros", kind="ours", cohorts=["CGMacros"], unit_is_a="class_word",
         ruler=None),
    dict(name="OhioT1DM", kind="ours", cohorts=["OhioT1DM"], unit_is_a="class_word",
         ruler=None),
    dict(name="dubosson", kind="ours", cohorts=["dubosson"], unit_is_a="class_word",
         ruler=None),
    dict(name="FNDDS-2021-2023", kind="fndds", unit_is_a="fndds_description",
         ruler="E1_FNDDS", bank="usda_holdout",
         env={"FOODNORM_DB": str(HOLDOUT_DB)}),
    dict(name="Nutrition5k", kind="n5k", unit_is_a="ingredient_name",
         ruler="E2_N5K"),
    dict(name="OpenFoodFacts-US", kind="off", unit_is_a="brand_product",
         ruler="E3_OFF"),
]

# Looked at, nothing there. The reason is recorded so nobody re-checks blind.
EMPTY = [
    ("aireadi-v3",         "Diet table present, 0 rows"),
    ("aireadi-noimage-v2", "Diet table present, 0 rows"),
    ("WellDoc2026Libre",   "Diet table present, 0 rows"),
    ("mcphases-v1",        "no Diet frame of any kind"),
    ("mimiciv-3.1",        "no Diet frame -- but see the note below"),
]


# ── loading ──────────────────────────────────────────────────────────────────
def _load_ours(c):
    """Every cohort of one corpus, stacked, classified on SHAPE and LABEL."""
    from taxonomy import classify_shape, classify_label
    frames = []
    for coh in c["cohorts"]:
        for f in sorted(SOURCE.glob(f"{coh}/@*/Diet.parquet")):
            d = pd.read_parquet(f)
            if not len(d):
                continue
            d = d.copy()
            d["cohort"] = coh
            d["PatientID"] = d.PatientID.astype(str)
            d["FoodName"] = d.FoodName.astype(str)
            img = d.ImagePath if "ImagePath" in d else pd.Series([None] * len(d))
            src = d.NutritionSource if "NutritionSource" in d else pd.Series([None] * len(d))
            d["shape"] = [classify_shape(n, p) for n, p in zip(d.FoodName, img)]
            d["label"] = [classify_label(r, s)
                          for (_, r), s in zip(d.iterrows(), src)]
            frames.append(d)
    return pd.concat(frames, ignore_index=True)


def _mentions_ours(d):
    """One row per COMPONENT MENTION. This is the step food needs and the
    other nouns do not: a Diet row is a meal, not a thing."""
    from foodnorm.dialect import split_meal
    cache, rows, empty = {}, [], 0
    for i, (fn, pid, coh, lab) in enumerate(
            zip(d.FoodName, d.PatientID, d.cohort, d.label)):
        comps = cache.get(fn)
        if comps is None:
            comps = cache[fn] = [(c.name, c.kind, c.amount_g) for c in split_meal(fn)]
        if not comps:
            empty += 1
            continue
        for name, kind, g in comps:
            rows.append((name, kind, g is not None, pid, coh, lab, i, len(comps)))
    m = pd.DataFrame(rows, columns=["unit", "kind", "stated", "PatientID",
                                    "cohort", "label", "row_i", "n_comp"])
    return m, empty


def _load_public(c):
    """A public reference table -> (units frame, corpus row count)."""
    if c["kind"] == "fndds":
        d = pd.read_parquet(EXT / "fndds_2021_2023/fndds_food.parquet")
        d["unit"] = d.description.astype(str).str.strip()
        g = d.groupby("unit", sort=False)
        u = pd.DataFrame({"unit": g.size().index, "row_weight": g.size().values,
                          "n_rows": g.size().values})
        for n in NUTRIENTS:
            u["gold_" + n] = g[n].median().values
        u["gold_n"] = u.row_weight
        return u, len(d), "per_100g", \
            "USDA FNDDS 2021-2023 Foods and Beverages, held out of the bank"

    if c["kind"] == "n5k":
        ing = pd.read_parquet(EXT / "nutrition5k/n5k_ingredient.parquet")
        it = pd.read_parquet(EXT / "nutrition5k/n5k_item.parquet")
        it["ingredient"] = it.ingredient.astype(str).str.strip()
        g = it.groupby("ingredient", sort=False)
        cnt = pd.DataFrame({"unit": g.size().index, "row_weight": g.size().values,
                            "n_rows": g.dish_id.nunique().values})
        ing["unit"] = ing.ingr.astype(str).str.strip()
        # per-GRAM in the file; a bank speaks per 100 g.
        ing["gold_Calories"] = ing["cal/g"] * 100
        ing["gold_Carbs"] = ing["carb(g)"] * 100
        ing["gold_Protein"] = ing["protein(g)"] * 100
        ing["gold_Fat"] = ing["fat(g)"] * 100
        ing["gold_Fiber"] = np.nan          # Nutrition5k publishes no fibre
        # ingredients_metadata ships 555 rows for 552 distinct names: three
        # names appear twice under different ids. Left-merging on the raw table
        # would duplicate those units and double-count their mentions.
        ing = (ing.groupby("unit", as_index=False)[["gold_" + n for n in NUTRIENTS]]
               .median())
        u = cnt.merge(ing, on="unit", how="left")
        u["gold_n"] = u.row_weight
        return u, len(it), "per_100g", \
            "Nutrition5k ingredients_metadata (USDA-derived per-gram macros)"

    d = pd.read_parquet(EXT / "openfoodfacts/off_product.parquet")
    d = d[d.countries_en.astype(str).str.contains("United States", na=False)]
    d["unit"] = d.product_name.astype(str).str.strip()
    d = d[d.unit.str.len() > 0]
    g = d.groupby("unit", sort=False)
    u = pd.DataFrame({"unit": g.size().index, "row_weight": g.size().values,
                      "n_rows": g.size().values})
    for n in NUTRIENTS:
        u["gold_" + n] = g[n].median().values
    u["gold_n"] = u.row_weight
    return u, len(d), "per_100g", \
        "Open Food Facts manufacturer label, US products, per 100 g"


# ── resolving ────────────────────────────────────────────────────────────────
def _resolve(texts):
    """Ask the door each DISTINCT thing once."""
    from foodnorm import normalize
    out, STEP = [], 5000
    for i in range(0, len(texts), STEP):
        out.extend(normalize(list(texts[i:i + STEP])))
        print(f"      resolved {min(i + STEP, len(texts)):,d}/{len(texts):,d}",
              flush=True)
    return pd.DataFrame(out)


def _verdict(kind, conf):
    """A MISS is not one thing.

    refused  the component names no food -- a meal slot, a carb declaration,
             the word 'Unknown'. There is nothing to resolve and saying so is
             the right answer.
    gap      a real food name that nothing matched. The only real hole.
    """
    if kind != "food":
        return "refused"
    if conf == "MEASURED":
        return "measured"
    if conf == "ESTIMATED":
        return "estimated"
    return "gap"


# ── one corpus ───────────────────────────────────────────────────────────────
def build_one(c):
    from taxonomy import GOLD_MACROS
    name = c["name"]
    print(f"  {name}")

    if c["kind"] == "ours":
        d = _load_ours(c)
        m, n_empty = _mentions_ours(d)
        g = m.groupby("unit", sort=False)
        u = pd.DataFrame({
            "unit": g.size().index,
            "kind": g.kind.first().values,
            "row_weight": g.size().values,
            "n_rows": g.row_i.nunique().values,
            "n_patients": g.PatientID.nunique().values,
            "n_cohorts": g.cohort.nunique().values,
            "grams_stated_n": g.stated.sum().values,
        })

        # GOLD: a meal that decomposes to exactly ONE food component IS that
        # component, so its logged macros are that unit's macros. Nothing else
        # on our own board gives a unit-level number at all.
        solo = m[(m.n_comp == 1) & (m.kind == "food") & (m.label == GOLD_MACROS)]
        if len(solo):
            rows = d.iloc[solo.row_i.values]
            gg = pd.DataFrame({"unit": solo.unit.values,
                               **{n: pd.to_numeric(rows[n], errors="coerce").values
                                  for n in NUTRIENTS}}).groupby("unit")
            gold = gg.median()
            gold.columns = ["gold_" + n for n in gold.columns]
            gold["gold_n"] = gg.size()
            u = u.merge(gold.reset_index(), on="unit", how="left")
        else:
            for n in NUTRIENTS:
                u["gold_" + n] = np.nan
            u["gold_n"] = 0
        u["gold_n"] = u.gold_n.fillna(0).astype(int)
        gold_basis = "per_meal"
        gold_src = ("logged by the app beside the meal -- FatSecret 86.1%, "
                    "Welldoc 10.6%, Calorie Mama 2.0%, Nutritionix 1.3%")
        n_rows_corpus, n_pat = len(d), int(d.PatientID.nunique())
        cohorts = " ".join(c["cohorts"])
        # Shanghai's macros ARE this resolver's own output. Circular by
        # construction, and the taxonomy already says so (label == derived).
        derived = float((d.label == "derived").mean())
    else:
        u, n_rows_corpus, gold_basis, gold_src = _load_public(c)
        u["kind"] = "food"
        u["n_patients"] = np.nan
        u["n_cohorts"] = 1
        u["grams_stated_n"] = 0
        n_empty, n_pat, cohorts, derived = 0, 0, c["name"], 0.0

    u["unit_text"] = u.unit
    res = _resolve(u.unit_text.tolist())
    u["resolved_conf"] = res.NutritionConf.values
    u["resolved_source"] = res.NutritionSource.values
    u["resolved_basis"] = res.NutritionBasis.values
    u["resolved_name"] = res.FoodNameResolved.values
    for n in NUTRIENTS:
        u["resolved_" + n] = pd.to_numeric(res[n], errors="coerce").values

    u["verdict"] = [_verdict(k, cf) for k, cf in zip(u.kind, u.resolved_conf)]

    # MIN_GOLD_N is a floor on an AGGREGATE. A published reference row is not
    # an aggregate -- one row of FNDDS is the whole of what USDA says -- so the
    # floor applies to our own corpora and nowhere else.
    min_n = MIN_GOLD_N if c["kind"] == "ours" else 1
    graded = (u.gold_n >= min_n) & u.gold_Carbs.notna()
    if derived > 0.5:
        # Not "no gold yet". No gold POSSIBLE: grading it returns our own answer.
        u["gold_tier"] = "CIRCULAR"
        u["gold_source"] = "produced by this resolver; grading it is circular"
        for n in NUTRIENTS:
            u["gold_" + n] = np.nan
        u["gold_n"] = 0
        graded = pd.Series(False, index=u.index)
    else:
        u["gold_tier"] = np.where(graded, "G2", "UNLABELLED")
        u["gold_source"] = np.where(graded, gold_src, "")
    u["gold_basis"] = np.where(graded, gold_basis, None)

    # The observed bank is harvested from OUR OWN logged rows, so on our own
    # corpora a unit answered from it has its gold and its answer coming out of
    # the same rows -- one number, two paths.
    #
    # ON A PUBLIC CORPUS THE SAME HIT IS NOT CIRCULAR AND MARKING IT SO WOULD BE
    # A LIE: Nutrition5k's gold is a USDA per-gram table and the bank is what
    # WellDoc patients logged. Two independent sources that happen to agree on
    # the string 'white rice' is exactly what we want to measure, not a leak.
    u["gold_circular"] = (graded & (u.resolved_source == "bank_observed")
                          if c["kind"] == "ours"
                          else pd.Series(False, index=u.index))

    u["bank_config"] = c.get("bank", "production")
    u["corpus"] = name
    u["unit_is_a"] = c["unit_is_a"]

    cols = ["unit", "unit_text", "kind", "row_weight", "n_rows", "n_patients",
            "n_cohorts", "grams_stated_n", "resolved_conf", "resolved_source",
            "resolved_basis", "resolved_name"] \
        + ["resolved_" + n for n in NUTRIENTS] + ["verdict"] \
        + ["gold_" + n for n in NUTRIENTS] \
        + ["gold_n", "gold_basis", "gold_tier", "gold_source", "gold_circular",
           "bank_config", "corpus", "unit_is_a"]
    u = u[cols].sort_values("row_weight", ascending=False).reset_index(drop=True)

    folder = OUT / name
    folder.mkdir(parents=True, exist_ok=True)
    u.to_parquet(folder / "units.parquet", index=False)

    answered = u.resolved_conf.isin(("MEASURED", "ESTIMATED"))
    w = int(u.row_weight.sum())
    share = {"m_" + v: float(u.row_weight[u.verdict == v].sum() / w)
             for v in ("measured", "estimated", "refused", "gap")}
    ngold = int((u.gold_tier == "G2").sum())
    ncirc = int(u.gold_circular.sum())

    rulers = []
    if c["ruler"] and ngold:
        r = u[(u.gold_tier == "G2") & (~u.gold_circular)]
        if len(r):
            r.to_parquet(folder / f"{c['ruler']}.parquet", index=False)
            rulers = [c["ruler"]]

    stat = dict(rows=n_rows_corpus, mentions=w, units=len(u),
                unit_is_a=c["unit_is_a"], patients=n_pat,
                rows_no_component=n_empty,
                units_answered=round(float(answered.mean()), 4),
                mentions_measured=round(share["m_measured"], 4),
                mentions_estimated=round(share["m_estimated"], 4),
                mentions_refused=round(share["m_refused"], 4),
                mentions_gap=round(share["m_gap"], 4),
                units_with_gold=ngold, units_gold_circular=ncirc,
                min_gold_n=min_n,
                gold_tier="G2" if ngold else ("CIRCULAR" if derived > 0.5 else None),
                bank_config=c.get("bank", "production"),
                rulers=rulers, cohorts=cohorts.split())
    (folder / "_stat.json").write_text(json.dumps(stat, indent=1))

    (folder / "README.md").write_text(CORPUS_README.format(
        name=name, blurb=BLURB[name].strip(), rows=n_rows_corpus, mentions=w,
        units=len(u), unit_is_a=c["unit_is_a"],
        pats=f"{n_pat:,d}" if n_pat else "--",
        cohorts=cohorts, answered=stat["units_answered"],
        m_meas=share["m_measured"], m_est=share["m_estimated"],
        m_ref=share["m_refused"], m_gap=share["m_gap"],
        ngold=ngold, ncirc=ncirc, minn=min_n,
        bank=c.get("bank", "production"),
        rulers=" ".join(rulers) or "--"))
    print(f"    units={len(u):,d} answered={stat['units_answered']:.1%} "
          f"gold={ngold} circular={ncirc} rulers={rulers}")
    return stat


def build_split_ruler(c):
    """The probe that PROVED WellDoc can have no unit-level nutrition ruler.

    Under the production configuration every WellDoc unit with enough support
    is answered from the T0 observed bank, and that bank was harvested from the
    very rows the gold is computed over: 37 gold units, 37 of them circular,
    ruler empty. That is a true reading of production and a useless ruler.

    So the ruler is built under a SPLIT configuration, declared in its own
    columns and never mixed into units.parquet:

        answer   the T0 bank rebuilt from TRAIN patients only
        gold     single-component meals logged by TEST patients

    Different people, different rows. The question it asks is real: does what
    one patient logged for 'greek yogurt' predict what another patient logged
    for it. The floor drops from 30 to 10 rows because a 30% split leaves the
    30-row floor with seven units, which grades nothing.
    """
    from taxonomy import GOLD_MACROS
    gi = pd.read_parquet(OUT / "gold_index.parquet")
    g = gi[gi.cohort.str.startswith("WellDoc")].reset_index(drop=True)

    from foodnorm.dialect import split_meal
    cache, rows = {}, []
    for i, (fn, lab, sp) in enumerate(zip(g.FoodName.astype(str), g.label, g.split)):
        cs = cache.get(fn)
        if cs is None:
            cs = cache[fn] = [(x.name, x.kind) for x in split_meal(fn)]
        if len(cs) == 1 and cs[0][1] == "food":
            rows.append((cs[0][0], lab, sp, i))
    m = pd.DataFrame(rows, columns=["unit", "label", "split", "row_i"])
    solo = m[(m.label == GOLD_MACROS) & (m.split == "test")]

    src = g.iloc[solo.row_i.values]
    gg = pd.DataFrame({"unit": solo.unit.values,
                       **{n: pd.to_numeric(src[n], errors="coerce").values
                          for n in NUTRIENTS}}).groupby("unit")
    u = gg.median()
    u.columns = ["gold_" + n for n in u.columns]
    u["gold_n"] = gg.size()
    u = u.reset_index()
    u = u[u.gold_n >= RULER_MIN_N].reset_index(drop=True)

    prod = pd.read_parquet(OUT / c["name"] / "units.parquet")
    u = u.merge(prod[["unit", "kind", "row_weight", "n_rows", "n_patients",
                      "n_cohorts", "grams_stated_n"]], on="unit", how="left")

    u["unit_text"] = u.unit
    res = _resolve(u.unit_text.tolist())
    u["resolved_conf"] = res.NutritionConf.values
    u["resolved_source"] = res.NutritionSource.values
    u["resolved_basis"] = res.NutritionBasis.values
    u["resolved_name"] = res.FoodNameResolved.values
    for n in NUTRIENTS:
        u["resolved_" + n] = pd.to_numeric(res[n], errors="coerce").values
    u["verdict"] = [_verdict(k, cf) for k, cf in zip(u.kind, u.resolved_conf)]
    u["gold_basis"] = "per_meal"
    u["gold_tier"] = "CIRCULAR"
    u["gold_source"] = ("logged by TEST patients beside a single-component "
                        "meal; answered from a TRAIN-patients-only T0 bank -- "
                        "same upstream vendor on both sides")
    u["gold_circular"] = True
    u["bank_config"] = "bank_train"
    u["corpus"] = c["name"]
    u["unit_is_a"] = c["unit_is_a"]

    cols = ["unit", "unit_text", "kind", "row_weight", "n_rows", "n_patients",
            "n_cohorts", "grams_stated_n", "resolved_conf", "resolved_source",
            "resolved_basis", "resolved_name"] \
        + ["resolved_" + n for n in NUTRIENTS] + ["verdict"] \
        + ["gold_" + n for n in NUTRIENTS] \
        + ["gold_n", "gold_basis", "gold_tier", "gold_source", "gold_circular",
           "bank_config", "corpus", "unit_is_a"]
    u = u[cols].sort_values("gold_n", ascending=False).reset_index(drop=True)
    (OUT / c["name"] / f"{c['ruler']}.parquet").unlink(missing_ok=True)
    u.to_parquet(OUT / c["name"] / "_split_probe.parquet", index=False)

    err = (u.resolved_Carbs - u.gold_Carbs).abs()
    exact = int((err < 0.01).sum())

    f = OUT / c["name"] / "_stat.json"
    stat = json.loads(f.read_text())
    stat["rulers"] = []
    stat["split_probe"] = dict(
        bank="bank_train", gold_scope="test_patients", min_gold_n=RULER_MIN_N,
        units=len(u), carb_exact_to_0g01=exact,
        carb_mae=round(float(err.mean()), 3),
        carb_median_err=round(float(err.median()), 3),
        verdict="circular -- same upstream vendor supplies both sides")
    f.write_text(json.dumps(stat, indent=1))
    # build_one wrote this README before the ruler existed. Say so here rather
    # than re-rendering, so the production reading above stays untouched.
    rp = OUT / c["name"] / "README.md"
    t = rp.read_text().split("\n## ")[0].rstrip() + "\n"
    t = re.sub(r"  rulers {10}\S+", "  rulers          --", t)
    t += RULER_NOTE.format(n=len(u), exact=exact, minn=RULER_MIN_N,
                           prod_min=MIN_GOLD_N,
                           med=round(float(err.median()), 2))
    rp.write_text(t)
    print(f"    _split_probe: {len(u)} units, {exact} exact to 0.01 g "
          f"-> CIRCULAR, no ruler")
    return stat


RULER_NOTE = """

## why the biggest corpus on the board ships NO ruler

Under PRODUCTION every WellDoc unit with enough support is answered from the T0
observed bank -- and that bank was harvested from the very rows the gold is
computed over. {prod_min}-row floor, 37 gold units, 37 of them circular.

The obvious repair was tried and is recorded in `_split_probe.parquet`:

```text
  answer   T0 bank rebuilt from TRAIN patients only
  gold     single-component meals logged by TEST patients
  floor    >= {minn} rows, not {prod_min}: a 30% split leaves the 30-row floor
           with seven units
  ──────────────────────────────────────────────────────────────────────
  {n} units,  {exact} of them matching the gold to within 0.01 g of carbohydrate
              median error {med} g
```

IT DID NOT WORK, AND WHY IT DID NOT IS THE FINDING. Splitting PATIENTS does not
split SOURCES. The observed bank does not hold one patient's opinion of
'banana'; it holds FatSecret's number for the string 'banana' -- and FatSecret
supplied the test patient's label too. Same upstream on both sides. A self-join
in different clothing, and the same failure the `survey_fndds_food` table caused
on FNDDS.

The leading underscore on `_split_probe.parquet` is the point: it is the
receipt for this paragraph, not a set anything may be scored on.

So WellDoc has no unit-level nutrition ruler, and neither does any other corpus
of ours. All three rulers on this board are PUBLIC -- which is the whole
argument for having gone and got public references.
"""


# ── prose ────────────────────────────────────────────────────────────────────
CORPUS_README = """\
# {name}

{blurb}

```text
  rows            {rows:>10,d}      a row is one meal / product
  mentions        {mentions:>10,d}      components, after split_meal()
  units           {units:>10,d}      a unit here is a {unit_is_a}
  patients        {pats:>10}
  cohorts         {cohorts}
  bank            {bank}

  answered        {answered:>9.1%}      of UNITS the door returns numbers for

  share of MENTIONS
    measured      {m_meas:>9.1%}      T0: the exact string was logged with macros
    estimated     {m_est:>9.1%}      T2: fuzzy-matched against USDA FDC
    refused       {m_ref:>9.1%}      names no food. Correct, not a failure.
    gap           {m_gap:>9.1%}      a real food name nothing matched

  units with gold {ngold:>10,d}      macros resting on >= {minn} row(s)
  of those, circular {ncirc:>7,d}      answered from the same source as the gold
  rulers          {rulers}
```

`units.parquet` is the inventory: one row per distinct thing this corpus asks
the door to resolve, with what it answers today. A `<SET_ID>.parquet` sits
beside it only where a NON-CIRCULAR gold exists.

GENERATED by `describe-food/benchmark/build_units.py`. Do not hand-edit.
"""

BLURB = {
    "WellDoc": """
Four WellDoc cohorts, stacked. The widest vocabulary on the board by a factor
of ten, because a WellDoc meal is a ';' list a person typed and every component
becomes its own unit. Portions are almost never stated, so nearly every answer
is per-100 g arithmetic over a name.

Its gold is the meals that decompose to exactly ONE component: that meal's
logged macros ARE that unit's macros. It is also the corpus the T0 observed
bank was harvested from, so a unit answered from that bank has its gold and its
answer coming out of the same rows. `gold_circular` marks them, every one of
them is marked, AND IT SHIPS NO RULER -- see the section below for the probe
that established that and for why the obvious repair does not work.
""",
    "Shanghai": """
The only cohort that states grams on nearly every component, and therefore the
only place the per-meal portion path can be exercised at all.

IT CAN NEVER BE GRADED ON NUTRITION. Its macro columns were written BY this
resolver -- the frame on disk carries `NutritionSource` -- so scoring against
them returns our own answer. `gold_tier` is CIRCULAR, not UNLABELLED: this is
not a gold we have yet to build, it is a gold that cannot exist. What it IS
good for is PARSE (the raw string is its own oracle), PORTION, and REGRESSION.
""",
    "CGMacros": """
ONE UNIT, THE WORD 'Unknown', ON EVERY ROW -- and the most valuable labels in
the house sitting right behind it.

1,437 of its meals carry five macros that agree with each other under Atwater,
supplied by a study kitchen rather than an app. That is the only L1-grade
nutrition truth anywhere on this board. The TEXT door cannot reach a single one
of them, because CGMacros names no food: it ships a PHOTO. This folder exists
to make that visible instead of letting the rows quietly vanish.
""",
    "OhioT1DM": """
ONE UNIT, THE WORD 'Unknown'. 2,164 of its rows carry a real, hand-entered
carbohydrate count and no food name at all.

A corpus with an ANSWER and no QUESTION. It grades nothing here, and it is here
so that a reader can see the shape of a diet log that records how many grams of
carbohydrate were eaten and nothing whatever about what was eaten.
""",
    "dubosson": """
ONE UNIT, THE WORD 'Unknown', over 74 rows carrying calories only. The smallest
corpus on the board, kept for the same reason as OhioT1DM: 'we looked, and the
food name is not there' is a finding, and deleting it would erase the finding.
""",
    "FNDDS-2021-2023": """
The USDA's own food-coding vocabulary: what a trained nutrition coder writes
down when a survey respondent describes a meal. 'Milk, NFS'. 'Chicken, NS as to
part'. Names normalized by a professional, which is a strictly easier problem
than a patient's typing and a strictly harder one than a generic ingredient.

RESOLVED AGAINST A HELD-OUT BANK, and it is the only corpus that is. Our USDA
sqlite ships `survey_fndds_food`, one row per FNDDS code; leaving it in makes
this a self-join that scores carb MAE 0.31 with a median of exactly 0.00.
Removing it -- and rebuilding the fts5 index, which an external-content table
needs or it keeps serving deleted rows -- moves the same corpus to 8.21 / 2.71.
""",
    "Nutrition5k": """
Google's weighed-plate dataset: every component of every dish physically placed
on a scale. Its vocabulary is generic ingredient words -- 'white rice',
'onions' -- which makes it the EASY end of the difficulty ladder and therefore
the control. The units here are the ingredients its dishes ACTUALLY use, which
is a subset of the ingredient table it ships.

WHAT IS MEASURED HERE IS THE MASS, NOT THE MACROS. The grams came off a scale;
the per-gram macros behind them are USDA lookups, so this is a third-party
estimate and not laboratory truth. It publishes no fibre column, so its fibre
gold is null rather than zero.
""",
    "OpenFoodFacts-US": """
Packaged retail products, named the way a manufacturer names them. The HARD end
of the ladder: a brand name carries the food word somewhere inside a phrase
built to sell, and the bank has never heard of the brand.

US products only. The dump is multilingual and both the door and USDA read
English; grading a French product name would measure language, not food.
""",
}

ROOT_README = """\
# 2-corpus

ONE FOLDER PER CORPUS, NAMED AFTER THE CORPUS. Open the folder and you know
where the data came from without opening a parquet.

MEMBERSHIP IS 'THIS CORPUS HAS FOOD CONTENT', NOT 'THIS CORPUS HAS AN ANSWER'.
Having a gold is a property recorded per unit, never the entry ticket. {n_corpora}
corpora are here -- {n_ours} of our own and {n_pub} taken from public references -- and
{n_empty} more were looked at and are named in `_empty.md`.

A ROW IS NOT A THING. This is the one step food needs that the other nouns do
not: a Diet row is a MEAL, and `split_meal()` is what turns it into the units.

```text
  "Multi Grain Cheerios; 2% Fat Milk; banana"  ──▶  3 mentions, 3 units
```

Every folder holds `units.parquet`, the inventory of distinct things this
corpus asks the door to resolve, with what it answers today. A folder holds a
`<SET_ID>.parquet` as well only where a NON-CIRCULAR gold exists.

```text
corpus                 rows  mentions   units  unit is a          unit%  ── share of mentions ─────────────     gold  rulers
                                                                        measured estimated  refused     gap
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
{table}
```

`unit%` counts VOCABULARY: how much of what this corpus says the door returns
numbers for. The four shares count TRAFFIC, and they are split because a MISS
is not one thing:

```text
  measured   T0. The exact string was logged once, with macros attached.
  estimated  T2. Fuzzy-matched against USDA FDC -- answered, with a calibrated
             tail: median 2.0 g carb error, p90 15.0 g.
  refused    ON PURPOSE. 'Just Carbs', a meal slot, the word 'Unknown'. There
             is no food named, so there is nothing to resolve.
  gap        ⚠️ THE ONLY REAL HOLE: a real food name nothing matched.
```

Reading `refused` as failure would be the single easiest mistake to make here.
`gap` is the number to drive down.

## Three corpora whose whole vocabulary is the word 'Unknown'

Not a defect in this table -- a finding it exists to show. {n_unknown:,d} rows carry a
LABEL and no QUESTION, for three different reasons:

```text
  OhioT1DM   2,164 rows  a real hand-entered carb count, no food name
  dubosson      74 rows  calories only, no food name
  CGMacros   1,437 rows  five study-kitchen macros -- the only L1-grade
                         nutrition truth on the board -- behind a PHOTO the
                         TEXT door cannot see
```

## gold, and the three ways it goes circular

`gold` counts units carrying macros independent of the door. The support it
needs is not the same on both sides: OUR corpora aggregate logged rows and need
at least {minn} of them; a public reference row is not an aggregate -- one row
of FNDDS is the whole of what USDA says about that code -- so one is enough.

```text
  gold_circular   the door answered from the T0 observed bank, which was
                  harvested from the very rows the gold comes from. One number,
                  two paths. The ruler parquet excludes these.
  gold_tier CIRCULAR  Shanghai. Its macro columns were WRITTEN by this
                  resolver. Not a gold we have yet to build -- one that cannot
                  exist. Kept anyway: it is the only corpus that states grams.
  same upstream  WellDoc, and the one that took a probe to find. Splitting
                  PATIENTS does not split SOURCES: the T0 bank holds FatSecret's
                  number for 'banana', and FatSecret supplied the test patient's
                  label too. 35 of 44 units matched to within 0.01 g.
                  `WellDoc/_split_probe.parquet` is the receipt.
  bank_config     FNDDS resolves against `usda_holdout`, every other corpus
                  against `production`. Our USDA sqlite ships
                  `survey_fndds_food`; leaving it in scores 0.31 carb MAE with
                  a median of exactly 0.00, which measures nothing.
```

```text
  DATA ONLY. The code that produces all of this lives in git at
  Tools/plugins/haipipe-utils/skills/describe-food/benchmark/

  source .venv/bin/activate && source env.sh
  python .../benchmark/build_units.py       # the inventories, this folder
  python .../benchmark/build_train_bank.py  # the train-patients-only T0 bank
  python .../benchmark/check_gold_independence.py   # the gate, with its control
  python .../benchmark/build_cgmacros_ruler.py      # the photo ruler (E4)
  python .../benchmark/run.py --full        # the row readings
```

## four rulers, and not one of them is our own logged data

NO CORPUS OF OURS CONTRIBUTES A PER-UNIT NUTRITION RULER, and that is a
measurement rather than a gap. Three of the five name no food at all; Shanghai's
macros were written BY the door; WellDoc shares an upstream vendor with its own
bank. What is left came from outside:

```text
  E1_FNDDS      per unit   a nutrition coder's phrase   G2  published table
  E2_N5K        per unit   a generic ingredient word    G2  published table
  E3_OFF        per unit   a manufacturer's brand name  G2  manufacturer label
  E4_CGMACROS   per MEAL   a PHOTOGRAPHED PLATE         G1  study kitchen
```

E4 is the odd one and the most valuable. It is the only L1 gold anywhere on this
board -- weighed and computed by the people who served the food -- and the TEXT
door cannot reach one row of it: CGMacros names no food, so its `units.parquet`
correctly reads 1 unit and 100% refused, and the `gold` column above correctly
reads 0. It becomes gradeable only through STAGE 0, where `imagename` turns the
photo into a name and the name enters the ordinary path. Its ruler is per MEAL
because a photographed plate has no vocabulary to be a unit of.

`gold_independence.json` in `6-benchmark/` is the gate that keeps all four
honest. It tests three failure modes -- written by the door, same table, same
upstream vendor -- and carries a POSITIVE CONTROL that re-resolves FNDDS against
the bank still holding `survey_fndds_food` and REQUIRES that reading to fail. A
gate that has never fired is not a gate.

`gold_index.parquet` beside these folders is the ROW index, one row per meal,
and is what `run.py` grades. `gold_summary.json` is its SHAPE x LABEL crosstab
and `bench_gate_b.json` a 400-row baseline kept from 260819. The folders are
the UNIT view of the same data. Neither replaces the other.
"""

EMPTY_MD = """\
# corpora with no food content

Listed, not omitted: a reader must be able to tell 'we looked and there was
nothing' from 'we never looked'. The moment one gains rows it gets a folder
next door with no change to any of this.

```text
{rows}
```

## mimiciv-3.1 deserves a sentence of its own

It has no Diet frame, but `IngredientEvent.parquet` holds 14,253,480 rows of
ICU nutrition delivery: dextrose, lipid emulsion, free water, tube feed, with
real volumes and rates.

It is not a corpus, because it asks the door nothing. Every row is an `ItemID`
against a closed dictionary -- there is no food name anywhere in it, and a
parenteral infusion is not a meal in any case. If it is ever wanted, it is a
REFERENCE for delivered energy, which is a use for `3-reference/`, not a folder
here.

## and one that is NOT here on purpose

`mcphases-v1` carries Apple Health workouts and no diet at all. It is the only
free-text corpus with a gradeable gold in `_ExerciseInfo`, and none of that
reaches food.
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--assemble", action="store_true",
                    help="re-render only the root README / summary / _empty")
    ap.add_argument("--_worker", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--_ruler", default=None, help=argparse.SUPPRESS)
    a = ap.parse_args()

    if a._worker:
        c = next(x for x in CORPORA if x["name"] == a._worker)
        build_one(c)
        return
    if a._ruler:
        c = next(x for x in CORPORA if x["name"] == a._ruler)
        build_split_ruler(c)
        return

    OUT.mkdir(parents=True, exist_ok=True)
    todo = [] if a.assemble else [c for c in CORPORA if a.only in (None, c["name"])]

    # Each corpus declares its own bank, and foodnorm resolves the path at
    # IMPORT time -- so a corpus that needs a different bank needs its own
    # process. One subprocess each, uniformly, rather than a special case.
    for c in todo:
        env = {**os.environ, **c.get("env", {})}
        r = subprocess.run([sys.executable, __file__, "--_worker", c["name"]],
                           env=env)
        if r.returncode:
            sys.exit(f"corpus {c['name']} failed")
        if c.get("ruler_split"):
            # Its own process again: the T0 bank path is resolved at import.
            r = subprocess.run(
                [sys.executable, __file__, "--_ruler", c["name"]],
                env={**env, "FOODNORM_OBSERVED_DB": str(TRAIN_BANK)})
            if r.returncode:
                sys.exit(f"ruler {c['name']} failed")

    stats = {c["name"]: json.loads((OUT / c["name"] / "_stat.json").read_text())
             for c in CORPORA if (OUT / c["name"] / "_stat.json").exists()}
    (OUT / "_units_summary.json").write_text(json.dumps(stats, indent=1))

    order = [c["name"] for c in CORPORA]
    tbl = "\n".join(
        f"{n:<18s}{s['rows']:>9,d}{s['mentions']:>10,d}{s['units']:>8,d}  "
        f"{s['unit_is_a']:<18s}{s['units_answered']:>6.1%}"
        f"{s['mentions_measured']:>9.1%}{s['mentions_estimated']:>10.1%}"
        f"{s['mentions_refused']:>9.1%}{s['mentions_gap']:>8.1%}"
        f"{s['units_with_gold']:>9,d}  {' '.join(s['rulers']) or '--'}"
        for n in order if (s := stats.get(n)))

    n_unknown = 2164 + 74 + 1437
    (OUT / "README.md").write_text(ROOT_README.format(
        table=tbl, minn=MIN_GOLD_N, n_corpora=len(stats),
        n_ours=sum(1 for c in CORPORA if c["kind"] == "ours"),
        n_pub=sum(1 for c in CORPORA if c["kind"] != "ours"),
        n_empty=len(EMPTY), n_unknown=n_unknown))
    (OUT / "_empty.md").write_text(EMPTY_MD.format(
        rows="\n".join(f"  {n:<20s}{why}" for n, why in EMPTY)))
    print(f"\n  wrote {OUT}")


if __name__ == "__main__":
    main()
