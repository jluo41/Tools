"""
Tier 0 of the bank ladder: the food strings patients ACTUALLY logged, with the
macros the app ACTUALLY attached to them.

    T0  observed   this exact string was logged, with numbers   -> MEASURED
    T1  catalog    (reserved: FoodID -> catalog entry)          -> MEASURED
    T2  usda       fuzzy match against USDA FDC                 -> ESTIMATED
    T3  none                                                    -> MISS

WHY A TIER AND NOT A BETTER MATCHER
================================================================================
Calibrated 2026-08-22 on 10,068 logged food names, the USDA fuzzy match has a
median carb error of 2.0 g and a tail of 688 names (10.0%) wrong by more than
15 g. That tail is NOT PREDICTABLE FROM THE NAME. Six candidate signals were
measured against it -- a near-zero carb prediction, 'with'/'and' compounds,
sugar-free/diet modifiers, beverage words, a parenthesised size, low support --
and the best reached 2.4x lift on 72 names. Gating on three of them at once
discarded 25% of all answers to move the bad rate from 10.0% to 8.8%.

So this file does not try to tell a good match from a bad one. It removes the
need to match at all, for every string that was already measured:

    'Pepsi (12 oz)'   USDA -> 0.00 g carbs, labelled GOOD
                      logged 4 times -> 41 g carbs
    'Sprite (12 oz)'  USDA -> 0.00 g       observed -> 38 g
    'Chicken Alfredo' USDA -> 0.00 g       observed -> 55.8 g

For a CGM project a sugary drink read as zero carbs is the worst single error
available, because it is also the sharpest glucose excursion there is.

WHAT THESE NUMBERS ARE
================================================================================
NOT laboratory truth. FatSecret supplied 86.1% of them, Welldoc's own source
10.6%, Calorie Mama (a photo model) 2.0%, Nutritionix 1.3%. They are WHAT THE
APP TOLD THE PATIENT -- which for CGM modelling is arguably the better target,
since the patient dosed against this number and not against an assay. The
distinction is why the confidence word is MEASURED and not TRUE.

DENOMINATED PER SERVING
================================================================================
USDA is per 100 g. This bank is per one serving of the named food. They may
NEVER be summed together, which is why `NutritionBasis` gains `per_serving` and
why enrich.py resolves a meal at ONE tier rather than mixing tiers.
"""
import functools
import os
import re
from pathlib import Path
from typing import Dict, Optional

NUTRIENT_KEYS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")
# The nine the Diet frame has never carried. Banked here so a caller that wants
# them does not need a second lookup; describe-food does not return them yet.
EXTRA_KEYS = ("Sodium", "Sugar", "AddedSugars", "SaturatedFat", "TransFat",
              "PolyUnSaturatedFat", "MonoUnSaturatedFat", "Cholesterol",
              "Potassium")

_WS = re.compile(r"\s+")


def _find_bank() -> Path:
    """FOODNORM_OBSERVED_DB, then $LOCAL_EXTERNAL_STORE, then walk up to the
    repo root. Same order describe-exercise uses; a service must be startable
    from any directory."""
    explicit = os.environ.get("FOODNORM_OBSERVED_DB")
    if explicit:
        return Path(explicit)
    rel = Path("foodbank_observed") / "observed_food.parquet"
    roots = []
    store = os.environ.get("LOCAL_EXTERNAL_STORE")
    if store:
        roots.append(Path(store))
        roots += [anc / store for anc in Path(__file__).resolve().parents]
    roots += [anc / "_WorkSpace" / "ExternalStore"
              for anc in Path(__file__).resolve().parents]
    for r in roots:
        if (r / rel).exists():
            return (r / rel).resolve()
    return (Path("_WorkSpace/ExternalStore") / rel).resolve()


DEFAULT_BANK = _find_bank()


def norm_key(name: str) -> str:
    """Must match the builder's `norm_name` exactly, or the bank never hits.
    Case and surrounding whitespace are not information; the '(12 oz)' suffix
    is, because sizes differ and the log distinguishes them."""
    return _WS.sub(" ", str(name).strip().lower())


@functools.lru_cache(maxsize=4)
def load(path=None) -> Dict[str, Dict]:
    """key -> one dict per entry. Cached: a cook resolves tens of thousands of
    components against one load. Returns {} when the bank is absent, so a
    deployment without it degrades to T2 rather than failing."""
    import pandas as pd
    p = Path(path or DEFAULT_BANK)
    if not p.exists():
        return {}
    df = pd.read_parquet(p)
    out = {}
    for rec in df.to_dict("records"):
        out[rec["key"]] = rec
    return out


def lookup(name: str, path=None) -> Optional[Dict]:
    """One food name -> its logged nutrition, PER SERVING, or None.

    Exact key match only. No fuzz: the entire point of this tier is that it is
    not a match, it is a retrieval of something already recorded. A near-miss
    here belongs in T2, wearing T2's confidence.
    """
    rec = load(path).get(norm_key(name))
    if rec is None:
        return None
    vals = {}
    for k in NUTRIENT_KEYS:
        v = rec.get(k)
        vals[k] = float(v) if v is not None and v == v else 0.0
    return {
        "values": vals,
        "n": int(rec.get("n") or 0),
        "serving_type": rec.get("serving_type"),
        "food_id": rec.get("food_id"),
        "name_raw": rec.get("name_raw"),
    }


def size() -> int:
    return len(load())
