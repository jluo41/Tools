"""
describe-food's NounSpec. Three things xbench cannot know, and nothing else.

WHAT THIS NOUN IS GRADED ON, AND WHY IT IS NOT GRAMS
================================================================================
Ten of eleven cohorts state no portion, so the API answers per_100g while the
label is per meal. Their difference measures PORTION SIZE, not food resolution.

    carb share of energy   4 * Carbs / Calories, as a percent of energy.
                           DIMENSIONLESS, so a per_100g prediction may be
                           compared against a per_meal label.

Absolute MAE in g or kcal becomes available when portion estimation does, and
not before. `carb_only` cells -- 12,936 "Just Carbs" rows and their kin -- are
therefore scored on COVERAGE ONLY: the label is grams of carbohydrate in a meal
and there is no denominator to make it dimensionless with.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from taxonomy import (classify_shape, classify_label, GRADEABLE, GOLD_MACROS,
                      DERIVED)

from xbench import NounSpec
from xbench.score import mae_r

from foodnorm import enrich_food_to_nutrition


def _shape(row):
    return classify_shape(row.get("FoodName"), row.get("ImagePath"))


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    return enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2",
                                    on_error="raise")


def _metric(df: pd.DataFrame, label: str) -> dict:
    """Carb share of energy, on the rows where both sides state one."""
    if label != GOLD_MACROS:
        return {"mae": None, "r": None, "scored": 0,
                "note": "no dimensionless label on this cell; coverage only"}
    e = df[df.NutritionConf != "MISS"]
    e = e[(e.true_Calories > 0) & (e.true_Carbs > 0)
          & (e.Calories > 0) & (e.Carbs > 0)]
    mae, r, n = mae_r(e.true_Carbs / e.true_Calories * 400.0,
                      e.Carbs / e.Calories * 400.0)
    return {"mae": mae, "r": r, "scored": n, "unit": "percentage points of energy"}


SPEC = NounSpec(
    noun="food",
    frame="Diet",
    text_col="FoodName",
    id_cols=("PatientID", "CarbsEntryID"),
    label_cols=("Carbs", "Calories", "Protein", "Fat", "Fiber"),
    extra_cols=("ImagePath",),
    conf_col="NutritionConf",
    basis_col="NutritionBasis",
    derived_col="NutritionSource",
    classify_shape=_shape,
    classify_label=classify_label,
    gradeable=GRADEABLE,
    derived_label=DERIVED,
    circular_conf=("MEASURED",),
    # ^ T0 of foodnorm's ladder is `bank_observed`: a table harvested from the
    #   food strings patients logged on THIS BOARD, with the macros the app
    #   attached. It is the right answer to return in production -- a sugary
    #   drink USDA reads as 0 g carbs is the worst error a CGM project can make
    #   -- and it is the label itself when the row being graded is one of the
    #   rows it was harvested from. 2,310 of 8,167 test-split names are in it.
    normalize=_normalize,
    metric=_metric,
).check()
