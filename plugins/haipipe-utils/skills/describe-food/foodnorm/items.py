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
    item      the input item's own fields first (ITEM_KEYS: id, food, prep, cook, amount, dish, ...)
    match     the food the table holds, by the table's own name (FoodMatched), so a wrong match shows (261028)
    words     match.words: does the matched name hold every word of the food asked (fatsecret's word rule, 93.5%
              right when it does in t24 r04)? PASS every word, PARTIAL at least half, NONE fewer; `missing` names
              them ("chicken pilaf" -> "Chicken, chicken roll, roasted" misses "pilaf"). A MEASURED match that is not
              PASS is ESTIMATED. A Chinese table name is not checked (null). (JL 261101)
    a dish    is split in the INPUT, not here (split_dishes, which eventnorm runs before it shows the input; JL
              261029: "they should be separated"): a dish line ("Sliced pork with mushroom and carrot 120 g") whose
              whole name finds nothing, or whose match lacks one of its foods (pork asked, "Peas and carrots"
              found), becomes one input item per food: i1 pork, i2 mushroom, i3 carrot. Split on with, and, a
              comma, & or +; each item names its food ("pork"), how it was cut or cooked ("sliced", `prep`; the
              dish's Chinese name gives `cook`: 炒 stir-fried, 炖 stewed, ...), its amount (a stated amount shared
              evenly, marked a guess) and the line it came from (`dish`). Here every item is one answer.
    total     the six: the items' sum, over the items that have the number, or `answer` when the caller already
              holds the meal's answer (the photo API's); coverage is the share of items counted, conf the weakest
              of them. (Until 261022 the six came from normalize() of the whole meal as one string, which adds up
              only foods matched the same way: "Banana; Milk 250 ml" gave the milk's 12.07 g alone.) The eight:
              the items' sum, empty when any item has none; GL: the items' GL summed

Numbers are written as text with their unit ("28 g", "150 kcal"), rounded to two places, null when absent: the
event JSON's form (eventnorm/schema.py).
"""
import re
from typing import Dict, List, Optional, Tuple

FOOD_GROUPS = [("macros", [("calories", "Calories", "kcal"), ("carbs", "Carbs", "g"), ("protein", "Protein", "g"),
                           ("fat", "Fat", "g")]),
               ("carb_parts", [("fiber", "Fiber", "g"), ("sugar", "Sugar", "g"), ("added_sugars", "AddedSugars", "g")]),
               ("fat_parts", [("saturated", "SaturatedFat", "g"), ("mono", "MonoUnSaturatedFat", "g"),
                              ("poly", "PolyUnSaturatedFat", "g"), ("trans", "TransFat", "g"),
                              ("cholesterol", "Cholesterol", "mg")]),
               ("minerals", [("sodium", "Sodium", "mg"), ("potassium", "Potassium", "mg")])]   # FatSecret's 14
# What an output item repeats from its input item, first, so each item says which food it is (JL 261029: "for each
# item, where is the item name???"), in the input item's own order (eventnorm schema.py ITEM_KEYS), so an item reads
# the same in the input and in the output (261102).
ITEM_KEYS = ("id", "food", "prep", "cook", "amount", "amount_from", "food_zh", "dish", "dish_zh")
SIX = ("Calories", "Carbs", "Protein", "Fat", "Fiber", "Sugar")    # the ones normalize() returns today


def val(v, unit: str):
    """A number as the event JSON writes it: "28 g", rounded to two places; None when absent."""
    return None if v is None or v != v else f"{round(float(v), 2):g} {unit}"


def clean(v):
    """A word or number from an answer as JSON: NaN (a MISS's empty basis) is null, never a bare NaN token."""
    return None if isinstance(v, float) and v != v else v


SPLIT = re.compile(r"\s*(?:,|&|\+|\bwith\b|\band\b)\s*", re.I)
AMOUNT = re.compile(r"\s*([0-9]*\.?[0-9]+)\s*(g|ml)\s*$", re.I)


# How a food was cut or cooked, as a log writes it before the food: "Sliced pork", "steamed rice".
PREP = ("stir-fried", "stir fried", "deep-fried", "pan-fried", "fried", "steamed", "boiled", "braised", "stewed",
        "roasted", "grilled", "baked", "scrambled", "poached", "smoked", "sliced", "minced", "shredded", "diced",
        "chopped", "mashed", "ground", "raw", "cooked")
PREP_RE = re.compile(r"^\s*((?:(?:" + "|".join(re.escape(w) for w in PREP) + r")\s+)+)(.+)$", re.I)
# How a dish was cooked, from its Chinese name (the first word found, longest first).
COOK_ZH = (("红烧", "red-braised"), ("凉拌", "dressed cold"), ("清蒸", "steamed"), ("炒", "stir-fried"), ("炖", "stewed"),
           ("蒸", "steamed"), ("煮", "boiled"), ("烤", "roasted"), ("炸", "deep-fried"), ("煎", "pan-fried"),
           ("焖", "braised"), ("卤", "braised in soy"), ("拌", "dressed"))


def prep_of(part: str) -> Tuple[str, Optional[str]]:
    """'Sliced pork' -> ('pork', 'sliced'); 'carrot' -> ('carrot', None)."""
    m = PREP_RE.match(part)
    return (m.group(2).strip(), " ".join(m.group(1).lower().split())) if m else (part.strip(), None)


def cook_zh(name: Optional[str]) -> Optional[str]:
    return next((en for zh, en in COOK_ZH if zh in str(name or "")), None)


def dish_parts(food: str) -> List[str]:
    """'Minced pork with cauliflower and carrot' -> ['Minced pork', 'cauliflower', 'carrot']; [] for one food."""
    bare = re.sub(r"\s*\([^)]*\)", "", AMOUNT.sub("", str(food)))      # "(with Peel)", "(150g)" describe one food
    parts = [p for p in SPLIT.split(bare) if p.strip()]
    return parts if len(parts) > 1 else []


def lost_a_food(food: str, a: Dict) -> bool:
    """A dish to ask part by part: its whole name found nothing, or the match lacks one of its foods (the last word
    of each part: 'pork' of 'Sliced pork', 'mushroom'), as "Pork, potatoes, and vegetables ...; gravy" lacks the
    mushroom of 'Sliced pork with mushroom and carrot'."""
    parts = dish_parts(food)
    if not parts:
        return False
    if a.get("NutritionConf") == "MISS":
        return True
    got = str(a.get("FoodMatched") or "").lower()
    for p in parts:
        w = (re.findall(r"[a-z]+", p.lower()) or [""])[-1]
        if (w[:-1] if w.endswith("s") and len(w) > 3 else w) not in got:
            return True
    return False


def word_check(food: str, matched) -> Optional[Dict]:
    """Does the matched name hold every word of the food asked? {"check": PASS | PARTIAL | NONE, "missing": [...]};
    None when nothing matched or the name is the Chinese table's (no English words to compare)."""
    from .fatsecret import found, words
    if not matched or re.search(r"[\u4e00-\u9fff]", str(matched)):
        return None
    mine = words(food)
    if not mine:
        return None
    got = words(matched)
    missing = [w for w in mine if not found(w, got)]
    share = 1 - len(missing) / len(mine)
    return {"check": "PASS" if not missing else "PARTIAL" if share >= 0.5 else "NONE", "missing": missing}


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

    def entry(e, ask, a, amount=None, food_zh=None):
        """One answer -> its match, serving, the 14 in four groups and GI/GL, added to e; and its numbers."""
        rec = ob.load().get(ob.norm_key(ask)) if a.get("NutritionSource") == "bank_observed" else None
        num = {k: a.get(k) for k in SIX}
        for k in ob.EXTRA_KEYS:
            v = (rec or {}).get(k)
            num[k] = float(v) if v is not None and v == v and float(v) >= 0 else None
        a = {k: clean(v) for k, v in a.items()}
        wc = word_check(e.get("food") or ask, a.get("FoodMatched")) if a.get("NutritionConf") != "MISS" else None
        if wc and wc["check"] != "PASS" and a.get("NutritionConf") == "MEASURED":
            a["NutritionConf"] = "ESTIMATED"
        basis = a.get("NutritionBasis")
        n = (rec or {}).get("n")
        e.update({"match": {"food": a.get("FoodMatched"), "source": a.get("NutritionSource"),
                            "conf": a.get("NutritionConf"), "words": wc,
                            "times_logged": int(n) if n is not None and n == n else None},
                  "serving": {"basis": basis, "unit": {"per_serving": clean((rec or {}).get("serving_type")),
                                                       "per_meal": amount, "per_100g": "100 g"}.get(basis),
                              "grams": None}})
        e.update({g: {name: val(num.get(col), u) for name, col, u in fields} for g, fields in FOOD_GROUPS})
        gly = gm.glycemic(m, ask, num.get("Carbs"), num.get("Fiber"), food_zh)
        e["glycemic"] = {"gi": gly["gi"], "gl": gly["gl"], "from": gly["from"]}
        return e, num

    out, nums = [], []
    for it, ask, a in zip(items, asks, alone):
        e, num = entry({k: it[k] for k in ITEM_KEYS if k in it}, ask, a, it.get("amount"), it.get("food_zh"))
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


def split_dishes(items: List[Dict], asks: List[str]) -> Tuple[List[Dict], List[str], int]:
    """The input's items with each dish line split into one item per food -> (items, the text each is asked with,
    how many lines were split). A line splits when its whole name finds nothing or its match lacks one of its foods,
    and at least one of its foods is found alone; "Mac and cheese" (found whole) stays one item. Ids run i1, i2, ...
    again; each split item keeps the line it came from in `dish` and its Chinese line in `dish_zh`."""
    from . import normalize
    ks = [k for k, it in enumerate(items) if dish_parts(it["food"])]
    whole = dict(zip(ks, normalize([asks[k] for k in ks]))) if ks else {}
    parts = {}
    for k in ks:
        if lost_a_food(items[k]["food"], whole[k]):
            g = AMOUNT.search(asks[k])
            share = f"{float(g.group(1)) / len(dish_parts(items[k]['food'])):.4g} {g.group(2)}" if g else None
            parts[k] = [(p, share, f"{p} {share}" if share else p) for p in dish_parts(items[k]["food"])]
    flat = [x[2] for k in parts for x in parts[k]]
    got = iter(normalize(flat) if flat else [])
    ans = {k: [next(got) for _ in parts[k]] for k in parts}               # all read first: any() would stop early
    found = {k: any(a.get("NutritionConf") != "MISS" for a in ans[k]) for k in parts}
    new, new_asks, n = [], [], 0
    for k, (it, ask) in enumerate(zip(items, asks)):
        if not found.get(k):
            new.append({**it, "id": f"i{len(new) + 1}"})
            new_asks.append(ask)
            continue
        n += 1
        amount = it.get("amount")
        line = f"{it['food']} {amount}" if amount else it["food"]
        for p, share, pask in parts[k]:
            food, prep = prep_of(p)
            e = {"id": f"i{len(new) + 1}", "food": food, "prep": prep, "cook": cook_zh(it.get("food_zh")),
                 "amount": share if share else None,
                 "amount_from": f"an even share of {amount}, a guess" if share else
                                f"part of {amount}" if amount else None,
                 "dish": line}
            if it.get("food_zh"):
                e["dish_zh"] = it["food_zh"]
            new.append(e)
            new_asks.append(pask)
    return new, new_asks, n


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
