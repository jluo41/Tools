"""
Constants for the food → nutrition normalizer.
Regex patterns, stopwords, placeholders, thresholds, DB path.
"""
import re
import pathlib

# The retrieval corpus. Overridable by FOODNORM_DB, which is how the two banks
# below get A/B measured instead of argued about.
#
# THE DEFAULT DELIBERATELY STAYS ON THE OLD FILE, and the reason is a result, not
# caution. `foodbank/foodbank.sqlite` (built 260821) holds the same usable foods,
# 13,602 against 13,601, WITHOUT the 87,614 laboratory-sample rows that carry
# NULL nutrition and are nonetheless full-text indexed. Measured on the frozen
# benchmark it is better in aggregate:
#
#     item_list|gold   MAE 14.52 -> 14.11   r 0.643 -> 0.659   (crosses r >= 0.65)
#     single_item|gold MAE 10.5  -> 10.1    r 0.822 -> 0.830
#
# and it BREAKS two things that must not break:
#
#     the Shanghai regression guard   G196/P97/M7 -> G182/P110/M8, so a meal that
#                                     resolved stops resolving
#     test_foodnorm L2                'scrambled egg with tomato' matches a food
#                                     with carbs 6.3 against a golden 1.5
#
# The mechanism is not obvious and is worth stating: FTS5 ranking uses CORPUS
# statistics, so deleting 87,614 documents changes the inverse document frequency
# of every term and reorders results. The sample rows could never be returned
# themselves, because every recall tier filters `calories IS NOT NULL`, but they
# were acting as BALLAST in the index. A cleaner corpus therefore needs
# `score_candidate` retuned against it; it is not a drop-in.
#
# Set FOODNORM_DB to evaluate the bank. Rebuild it with
# `code/scripts/haibuilder/0-external/e13_build_external_foodbank.py`.
import os

_LEGACY_DB = ("/home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/"
              "usda_fdc/usda_nutrition.sqlite")
_FOODBANK_DB = ("/home/jluo41/WellDoc-SPACE/_WorkSpace/ExternalStore/@v1215/"
                "foodbank/foodbank.sqlite")
USDA_DB = pathlib.Path(os.environ.get("FOODNORM_DB", _LEGACY_DB))

# App UI labels that occupy the FoodName field but name no food. Sending one of
# these to a food bank can only produce a wrong match -- there is nothing to match.
#
#   "unknown"     CGMacros / OhioT1DM / dubosson: the food was never named
#                 (CGMacros logged a photo instead)
#   "just carbs"  a WellDoc app entry MODE: the user typed a carb count and named
#                 no food. 12,964 rows across the four WellDoc cohorts, plus 2,018
#                 more where it is one component of a composite ("Just Carbs; White
#                 Rice") -- which is why this must be applied per COMPONENT, not
#                 per meal string.
#
# Their Carbs is a real user-reported number, but Calories/Protein/Fat/Fiber are
# 0 in 100% of rows against 8-19% for real foods: those zeros mean NOT MEASURED,
# not zero. Treat as NutritionSource="user_reported": trust Carbs, NULL the rest.
PLACEHOLDERS = {"unknown", "just carbs", "none", "nan", "n/a", ""}

# Status tracking file location
STATUS_DIR = pathlib.Path.home() / ".food-description"
STATUS_FILE = STATUS_DIR / "status.json"

# Regex for parsing food lines: "<food> <number> <unit>"
# Units: g, ml, IU (case-insensitive)
# Units are matched case-INSENSITIVELY. Without re.I, 'Milk 250 mL' did not
# parse and the portion was lost: the alternation listed `ml` and `iu` and `IU`
# and happened to omit `mL`, which is how a millilitre is normally written.
# Found 260821 by the parse lane.
LINE_RE = re.compile(r"^\s*(.+?)\s+(\d+(?:\.\d+)?)\s*(g|ml|IU)\s*$", re.I)

# Stopwords that muddy retrieval signal
# (cooking methods, adjectives that don't help identify the food)
STOPWORDS = {
    "boiled", "steamed", "fried", "raw", "cooked", "minced", "sliced",
    "shredded", "scrambled", "baked", "grilled", "stir", "stewed",
    "roasted", "braised", "poached", "cured", "dried", "fresh", "whole",
    "broiled", "sauteed"
}

# FTS5 retrieval scoring thresholds
MIN_COVERAGE = 0.8  # token coverage needed for GOOD classification
MIN_FTS_CANDIDATES = 3  # if FTS5 returns fewer, mark as MISS
