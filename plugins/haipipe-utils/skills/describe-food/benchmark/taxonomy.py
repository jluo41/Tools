"""
The corpus taxonomy: two ORTHOGONAL axes over every Diet row on the board.

Getting these confused is the reason no benchmark existed. "Just Carbs" is not
one category: it is a SHAPE (the string names no food) and separately a LABEL
CLASS (carbs are real, the other four macros are 0 meaning "not measured"). A
single list conflates "what does the input look like" with "what can we grade
against", and only the second decides whether a row belongs in a benchmark.

    SHAPE   a property of FoodName. What the normalizer must parse.
    LABEL   a property of the macro columns. What we may grade against.

Import, never copy:

    from taxonomy import classify_shape, classify_label, GRADEABLE

This file moved here from
`examples/ProjA-CGM-Raw2AIData/tasks/AY1_foodrec_v1/00_benchmark/shapes.py`
on 260822, unchanged apart from this paragraph. It lives beside the resolver
now because the taxonomy is a property of the NOUN, not of one project's task:
`_FoodInfo/6-benchmark/code` is a symlink to this directory, and the old path
is a shim that re-exports from here.
"""
import math

# ── SHAPE ────────────────────────────────────────────────────────────────────
SINGLE_ITEM   = "single_item"        # one component, a real food name
ITEM_LIST     = "item_list"          # ';' separated, 2+ real components
CARB_DECL     = "carb_declaration"   # the whole string is the app's carb-entry mode
MIXED_DECL    = "mixed_declaration"  # ';' list with a carb declaration inside it
NEWLINE_GRAMS = "newline_grams"      # '\n' separated, each line carries grams
SINGLE_GRAMS  = "single_grams"       # one line carrying grams
PHOTO_ONLY    = "photo_only"         # no food named, an image exists
UNNAMED       = "unnamed"            # no food named, nothing else either

# App UI labels that occupy FoodName and name no food. Kept local to the
# taxonomy rather than imported from the library: the library's PLACEHOLDERS is
# a RETRIEVAL filter (do not send this to a food bank), this is a CLASSIFIER
# (this row is of kind X). They agree today and need not agree forever.
_DECLARATIONS = {"just carbs"}
_NO_FOOD      = {"unknown", "none", "nan", "n/a", ""}


def classify_shape(food_name, image_path=None):
    """FoodName -> one SHAPE. Never raises; an unreadable value is UNNAMED."""
    s = "" if food_name is None else str(food_name)
    low = s.strip().lower()

    if low in _NO_FOOD:
        return PHOTO_ONLY if image_path and str(image_path).strip() not in ("", "nan", "None") else UNNAMED
    if low in _DECLARATIONS:
        return CARB_DECL
    if "\n" in s:
        return NEWLINE_GRAMS
    if ";" in s:
        parts = [p.strip().lower() for p in s.split(";")]
        return MIXED_DECL if any(p in _DECLARATIONS for p in parts) else ITEM_LIST
    # A single line. Shanghai's carry grams, WellDoc's do not, and the
    # difference is exactly what the portion gate turns on -- so it is a
    # distinct shape, not a formatting detail.
    import re
    return SINGLE_GRAMS if re.search(r"\d+(\.\d+)?\s*(g|ml)\s*$", low) else SINGLE_ITEM


# ── LABEL ────────────────────────────────────────────────────────────────────
GOLD_MACROS  = "gold_macros"    # 5 macros, internally consistent -> gradeable
CARB_ONLY    = "carb_only"      # carbs real, other four are 0 meaning NOT MEASURED
KCAL_ONLY    = "kcal_only"      # calories real, rest absent
PARTIAL      = "partial"        # filled but not self-consistent -> unusable
DERIVED      = "derived"        # 🔴 produced BY the normalizer. Grading it is circular.
NO_LABEL     = "no_label"

# Only these carry a label INDEPENDENT of the normalizer, so only these may be
# scored on nutrition QUALITY. Each says what it may be scored on.
GRADEABLE = {
    GOLD_MACROS: ("Carbs", "Calories", "Protein", "Fat", "Fiber"),
    CARB_ONLY:   ("Carbs",),
    KCAL_ONLY:   ("Calories",),
}

# DERIVED IS NOT WORTHLESS, IT IS DIFFERENTLY USEFUL.
#
# An earlier version of this file treated `derived` as "excluded" and stopped
# there, which threw away the only cohort that states portions. Its macros are
# the normalizer's own output, so scoring nutrition quality against them is
# circular. Three other things are not circular, and one of them cannot be
# measured anywhere else on the board:
#
#   PARSE       ground truth is the RAW STRING, read by a dumb oracle: count the
#               separators, count the `<number> g` occurrences. Disagreement
#               between that count and the parser's is a parse bug, and this is
#               how the missing-space defect was found. No label needed.
#
#   PORTION     Shanghai states grams on 99.2% of components and every other
#               cohort on effectively none. It is the ONLY place the per-meal
#               path can be exercised at all, so excluding it means absolute
#               nutrition is permanently untestable.
#
#   REGRESSION  the frame on disk is a FROZEN snapshot from an older library
#               version. Today's output against the stored column answers "did
#               behaviour change", which is not a quality claim and is still the
#               guard that caught 4 meals moving PARTIAL to GOOD.
#
# A fourth is available and unused: `nutrition.FoodName_zh` holds the Chinese
# original beside the English, which is a free bilingual name-resolution set.
LANES = {
    "quality":    tuple(GRADEABLE),          # needs an independent label
    "parse":      (DERIVED, GOLD_MACROS, CARB_ONLY, KCAL_ONLY),
    "regression": (DERIVED,),                # only a frozen frame can regress
}

ATWATER_TOL = 0.15   # kcal ~= 4C + 4P + 9F, within 15%


def _num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def classify_label(row, nutrition_source=None):
    """A row's macro columns -> one LABEL class.

    `nutrition_source` is the frame's NutritionSource value where it exists. Any
    non-null value means the normalizer wrote these numbers, so the row is
    DERIVED and must never enter a benchmark. Shanghai is the whole of this
    class: it is the one cohort the library is wired into, and therefore the one
    cohort that cannot grade it.
    """
    if nutrition_source is not None and str(nutrition_source) not in ("", "nan", "None"):
        return DERIVED

    c, k = _num(row.get("Carbs")), _num(row.get("Calories"))
    p, f = _num(row.get("Protein")), _num(row.get("Fat"))

    if k is not None and k > 0 and None not in (c, p, f):
        atwater = 4 * c + 4 * p + 9 * f
        if atwater > 0 and abs(k - atwater) <= ATWATER_TOL * k:
            return GOLD_MACROS
        return PARTIAL

    # All four non-carb macros exactly 0 is the app's "not measured", not zero.
    if c is not None and c > 0 and all(v == 0 for v in (k, p, f) if v is not None) \
            and (k == 0 or k is None):
        return CARB_ONLY
    if c is not None and c > 0 and k is None:
        return CARB_ONLY
    if k is not None and k > 0 and c is None:
        return KCAL_ONLY
    if any(v is not None and v > 0 for v in (c, k, p, f)):
        return PARTIAL
    return NO_LABEL
