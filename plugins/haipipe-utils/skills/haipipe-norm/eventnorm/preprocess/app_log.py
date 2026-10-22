"""
app_log: the WellDoc app's ELogFoodItem, a row per food, all the rows of one meal (one CarbEntryID).

    time       ObservationDateTime is UTC; TimezoneOffset (minutes) makes it local (Diet5Min does the same)
    logged_at  ObservationEntryDateTime, the latest row: when the meal was typed in (s01-D36)
    meal_type  ActivityTypeID, named by the SourceFn's own ID_to_Type (WellDocDataExtV260930B), Before/After dropped
    items      a row per food; a row the food split calls no food ('Just Carbs', a placeholder) is no item
    amount     ServingsConsumed x ServingSize ServingType ("0.25 serving", "1 slice (1 oz)")
    total      the rows' own numbers (common.stated_total: a typed carb count is the meal's carbs, once)
"""
from .common import clock, stated_total, step_text

# WellDocDataExtV260930B.ID_to_Type, its Before/After dropped (s01-D25)
MEAL_TYPES = {"1": "breakfast", "2": "breakfast", "3": "lunch", "4": "lunch", "5": "dinner", "6": "dinner",
              "7": "bedtime", "8": "exercise", "9": "exercise", "12": "snack", "14": "fasting"}
SERVING = ("ServingsConsumed", "ServingSize", "ServingType")


def fits(rows) -> bool:
    return {"FoodName", "ObservationDateTime"} <= set(rows.columns)


def make(rows) -> dict:
    from foodnorm.dialect import split_meal
    if "CarbEntryID" in rows.columns and rows["CarbEntryID"].nunique() > 1:
        raise ValueError(f"app_log rows hold {rows['CarbEntryID'].nunique()} meals (CarbEntryID); send one meal a call")
    num = lambda v: float(v) if str(v).strip() not in ("", "nan", "None") else 1.0
    items, asks, skipped = [], [], []
    for _, r in rows.iterrows():
        name = str(r["FoodName"]).strip()
        c = split_meal(name)
        if not c or c[0].kind != "food":
            skipped.append(name)
            continue
        it = {"id": f"i{len(items) + 1}", "food": name}
        if set(SERVING) <= set(rows.columns) and str(r["ServingType"]).strip() not in ("", "nan", "None"):
            it["amount"] = f"{num(r['ServingsConsumed']) * num(r['ServingSize']):g} {str(r['ServingType']).strip()}"
        items.append(it)
        asks.append(name)
    kind = None
    if "ActivityTypeID" in rows.columns:
        kind = MEAL_TYPES.get(str(rows.iloc[0]["ActivityTypeID"]).strip().removesuffix(".0"))
    t = dict(col="ObservationDateTime", offset="TimezoneOffset")
    return {"input": {"start": clock(rows, **t), "end": None,
                      "logged_at": clock(rows, "ObservationEntryDateTime", "TimezoneOffset", latest=True),
                      "meal_type": kind, "total": stated_total(rows, "FoodName", skipped),
                      "items": items or None, "timeline": None},
            "asks": asks, "meal": "; ".join(rows["FoodName"].astype(str).str.strip()),
            "step": step_text(len(rows), items, skipped)}
