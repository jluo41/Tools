"""
photo: a meal photo and its row (CGMacros: Timestamp, Meal Type, the meal's numbers, Image path).

    time       Timestamp, local, no zone named
    meal_type  "Meal Type" (Snack, Snacks and Snack 1 are all snack)
    total      the row's own numbers: Calories, Carbs, Protein, Fat, Fiber
    items      none from the row: the photo API names the foods (POST /food/normalize/image, its FoodNameResolved);
               send its names as input.items beside the raw and they are the items (s01-D16, D29)

The photo's path is read for nothing and goes nowhere: it names the subject's folder.
"""
from .common import clock, meal_word, stated_total

CGMACROS = {"time": "Timestamp", "meal_type": "Meal Type"}


def fits(rows) -> bool:
    return {"Timestamp", "Meal Type"} <= set(rows.columns)


def make(rows) -> dict:
    kind = meal_word(rows.iloc[0][CGMACROS["meal_type"]]) if CGMACROS["meal_type"] in rows.columns else None
    return {"input": {"start": clock(rows, CGMACROS["time"]), "end": None, "logged_at": None, "meal_type": kind,
                      "total": stated_total(rows), "items": None, "timeline": None},
            "asks": [], "meal": "",
            "step": "a photo row: the photo is not read here, so no items until the photo API's names come as "
                    "input.items"}
