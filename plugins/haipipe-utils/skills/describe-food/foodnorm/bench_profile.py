"""How describe-food declares itself to the shared B1 benchmark.

This member is the one that proves the engine is not secretly noun-specific:
its confidence vocabulary is MEASURED / ESTIMATED, not GOOD / OK / ALIAS, and
every check below reads the DECLARED order rather than a family default.
"""
import pathlib

from bench import Profile

from . import normalize
from .client import NUTRIENTS, PROVENANCE

ROOT = pathlib.Path(__file__).resolve().parents[6]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"


def _adapt(req):
    foods = req.get("foods", [req["food"]] if "food" in req else [])
    if isinstance(foods, str):
        # The service 422s on this and the local door would iterate the string
        # one character at a time. Reproduce the service's refusal rather than
        # letting the trap pass as a hit -- see C11.
        raise ValueError(f"foods={foods!r} is a string, not a list")
    return normalize(foods)


def _skip(fx):
    r = fx["request"]
    if "_multipart" in r:
        return "multipart upload: the door takes strings, the service takes files"
    if "meals" in r:
        return ("the image door is a model call. Its output is not "
                "deterministic, so C06 would be measuring the model")
    return None


PROFILE = Profile(
    noun="food", emoji="🍎", skill="describe-food",
    door=normalize,
    required=tuple(NUTRIENTS) + tuple(PROVENANCE),

    # All five macros are governed. Unlike exercise and medication, nothing in
    # this record comes from the log itself: the door is handed a NAME and
    # every number it returns is the bank's.
    governed=tuple(NUTRIENTS),

    # And all five are scaled, which is this noun's whole difficulty: ten of
    # eleven cohorts state no portion, so the answer is per_100g while the
    # question was about a meal.
    scaled=tuple(NUTRIENTS),

    conf_field="NutritionConf", source_field="NutritionSource",
    basis_field="NutritionBasis",
    conf_order=["MEASURED", "ESTIMATED", "WEAK", "MISS"],
    trusted=["MEASURED", "ESTIMATED"],

    port=8077, url_env="FOODNORM_URL",
    dest=INFO / "6-benchmark", examples=INFO / "5-api-examples",

    # A plain item, a semicolon list, a stated portion, a carb declaration
    # (rule 2), and a meal slot that is not a food at all.
    probe=["fried rice", "Toasted Bread; Decaf Coffee", "Cucumber 100g",
           "Just Carbs", "dinner"],
    adapt=_adapt,

    # Stage 0 tags a name it read from a photo with its own provenance pair,
    # per rule 5. Present only when the image stage ran.
    optional=("NameSource", "NameConf", "FoodNameResolved"),
    skip=_skip,
)
