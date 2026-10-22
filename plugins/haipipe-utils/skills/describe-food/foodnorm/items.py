"""
A meal's food items, each enriched: the food each matched, the serving its numbers are for, FatSecret's 14 nutrients
in four groups, and its GI and GL; then the meal's total. The food noun's `enrich(items)` that the event API calls
(eventnorm/assemble.py), lifted from b51 s01's drawing builder (studio/_build/topic_frames.py `enriched`, s01-D21,
D25), where it ran first.

    from foodnorm.items import enrich_items
    items, total = enrich_items([{"id": "i1", "food": "White Rice", "amount": "1 cup, cooked"}],
                                asks=["White Rice"], meal="Just Carbs; White Rice")

WHERE EACH NUMBER COMES FROM
================================================================================
    six       Calories Carbs Protein Fat Fiber Sugar: normalize(), each item asked ALONE, the same door as ever
    eight     Sodium ... Potassium: the observed table's row for the item, when normalize() found it there
              (observed.EXTRA_KEYS: the answer does not carry them yet); a negative is the vendor's "not given",
              so empty, and a food matched in the USDA tables has them empty
    GI, GL    glycemic.py on ext_food_gi, by the item's name (its Chinese name first, when it has one)
    total     the six: the items' sum, over the items that have the number, or `answer` when the caller already
              holds the meal's answer (the photo API's); coverage is the share of items counted, conf the weakest
              of them. (Until 261022 the six came from normalize() of the whole meal as one string, which adds up
              only foods matched the same way: "Banana; Milk 250 ml" gave the milk's 12.07 g alone.) The eight:
              the items' sum, empty when any item has none; GL: the items' GL summed

Numbers are written as text with their unit ("28 g", "150 kcal"), rounded to two places, null when absent: the
event JSON's form (eventnorm/schema.py).
"""
from typing import Dict, List, Optional, Tuple

FOOD_GROUPS = [("macros", [("calories", "Calories", "kcal"), ("carbs", "Carbs", "g"), ("protein", "Protein", "g"),
                           ("fat", "Fat", "g")]),
               ("carb_parts", [("fiber", "Fiber", "g"), ("sugar", "Sugar", "g"), ("added_sugars", "AddedSugars", "g")]),
               ("fat_parts", [("saturated", "SaturatedFat", "g"), ("mono", "MonoUnSaturatedFat", "g"),
                              ("poly", "PolyUnSaturatedFat", "g"), ("trans", "TransFat", "g"),
                              ("cholesterol", "Cholesterol", "mg")]),
               ("minerals", [("sodium", "Sodium", "mg"), ("potassium", "Potassium", "mg")])]   # FatSecret's 14
SIX = ("Calories", "Carbs", "Protein", "Fat", "Fiber", "Sugar")    # the ones normalize() returns today


def val(v, unit: str):
    """A number as the event JSON writes it: "28 g", rounded to two places; None when absent."""
    return None if v is None or v != v else f"{round(float(v), 2):g} {unit}"


def clean(v):
    """A word or number from an answer as JSON: NaN (a MISS's empty basis) is null, never a bare NaN token."""
    return None if isinstance(v, float) and v != v else v


def enrich_items(items: List[Dict], asks: Optional[List[str]] = None, meal: Optional[str] = None,
                 answer: Optional[Dict] = None) -> Tuple[List[Dict], Dict]:
    """items (each {"id", "food", "amount"?, "food_zh"?}) -> (each enriched, the meal's total).

    asks    the text each item is asked with (default its food); Shanghai asks the line with its grams
    meal    kept for callers; the total no longer asks the meal as one string (261022)
    answer  the meal's answer already in hand (a photo API reply): its six are the total's, no second call
    """
    from . import normalize, observed as ob
    from . import glycemic as gm
    asks = list(asks) if asks is not None else [it["food"] for it in items]
    alone = normalize(asks) if asks else []
    m = gm.matcher()
    out, nums = [], []
    for it, ask, a in zip(items, asks, alone):
        rec = ob.load().get(ob.norm_key(ask)) if a.get("NutritionSource") == "bank_observed" else None
        num = {k: a.get(k) for k in SIX}
        for k in ob.EXTRA_KEYS:
            v = (rec or {}).get(k)
            num[k] = float(v) if v is not None and v == v and float(v) >= 0 else None
        a = {k: clean(v) for k, v in a.items()}
        basis = a.get("NutritionBasis")
        n = (rec or {}).get("n")
        e = {"id": it["id"],
             "match": {"food": a.get("FoodNameResolved"), "source": a.get("NutritionSource"),
                       "conf": a.get("NutritionConf"), "times_logged": int(n) if n is not None and n == n else None},
             "serving": {"basis": basis, "unit": {"per_serving": clean((rec or {}).get("serving_type")),
                                                  "per_meal": it.get("amount"), "per_100g": "100 g"}.get(basis),
                         "grams": None}}
        e.update({g: {name: val(num.get(col), u) for name, col, u in fields} for g, fields in FOOD_GROUPS})
        gly = gm.glycemic(m, ask, num.get("Carbs"), num.get("Fiber"), it.get("food_zh"))
        e["glycemic"] = {"gi": gly["gi"], "gl": gly["gl"], "from": gly["from"]}
        out.append(e)
        nums.append(num)
    tot = answer if answer is not None else summed(nums, [it["match"]["conf"] for it in out],
                                                   [it["serving"]["basis"] for it in out])
    total = {}
    for g, fields in FOOD_GROUPS:
        total[g] = {}
        for name, col, u in fields:
            vals = [x[col] for x in nums]
            total[g][name] = val((tot or {}).get(col), u) if col in SIX else \
                None if not vals or None in vals else val(sum(vals), u)
    gls = [it["glycemic"]["gl"] for it in out]
    total["glycemic"] = {"gl": None if not gls or None in gls else round(sum(gls), 1)}
    total.update({k: clean((tot or {}).get(c)) for k, c in
                  (("conf", "NutritionConf"), ("basis", "NutritionBasis"), ("coverage", "NutritionCoverage"))})
    return out, total


CONF_ORDER = ("MEASURED", "ESTIMATED")                      # weakest last; anything else (a MISS) counts as none


def summed(nums: List[Dict], confs: List[str], bases: List[str]) -> Dict:
    """The meal's six as the sum of its counted items: an item with none of the six (a MISS) is not counted, and a
    nutrient that any counted item lacks is empty, never a sum too small (as the eight). NutritionCoverage is the
    share of items counted, NutritionConf the weakest of them, NutritionBasis theirs when they share one, else
    "mixed"."""
    has = lambda v: v is not None and v == v
    got = [k for k, x in enumerate(nums) if any(has(x[c]) for c in SIX)]
    out = {c: sum(nums[k][c] for k in got) if got and all(has(nums[k][c]) for k in got) else None for c in SIX}
    ranks = [CONF_ORDER.index(confs[k]) if confs[k] in CONF_ORDER else len(CONF_ORDER) for k in got]
    basis = {bases[k] for k in got}
    out.update(NutritionCoverage=round(len(got) / len(nums), 3) if nums else None,
               NutritionConf=(CONF_ORDER + ("MISS",))[max(ranks)] if ranks else "MISS",
               NutritionBasis=(basis.pop() if len(basis) == 1 else "mixed") if got else None)
    return out
