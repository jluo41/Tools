"""
The dialect layer: one meal string, in whatever dialect it was written, becomes
a list of TYPED components.

WHY THIS FILE EXISTS
================================================================================
These rules used to live in `code/scripts/haibuilder/0-external/
e12_build_external_foodnorm.py`, a one-off build script. The library therefore
could not read the dialect that 33,059 WellDoc rows are written in, while the
lexicon that same script produced resolved those same cohorts at 82.6 to 90.6
percent. The rules were on the wrong side of the boundary. QE1 D10, gate A.

A PLACEHOLDER IS TYPED, NOT DROPPED
================================================================================
The build script's answer was to FILTER app UI labels out. That is right for
building a food lexicon, where "just carbs" was the single biggest entry at
16,573 mentions, and wrong for reading a meal, because the label carries
information:

    'Just Carbs'          the user typed a carb count and named no food.
                          Carbs is REAL. The other four macros are 0 meaning
                          NOT MEASURED. Dropping the component loses the fact
                          that a carb count was declared.
    'Just Carbs; dinner'  component 2 is a MEAL SLOT, not a food. Sent to a
                          food bank it matches something, and that something
                          is wrong. This row is why SLOT_LABEL exists.
    'Unknown'             the food was never named. CGMacros logged a photo
                          instead; OhioT1DM and dubosson logged nothing.

So this layer TYPES every component and lets the caller decide. `decompose`
keeps its old two-tuple shape and returns the FOOD components only, so the six
existing call sites need no change.

DIALECT IS NOT A COHORT PROPERTY
================================================================================
Measured 260819 over all 71,673 Diet rows: `newline_grams` has 10 non-Shanghai
rows, so WellDoc carries a few rows in Shanghai's dialect. A parser keyed only
on cohort meets the wrong dialect eventually, which is why 'auto' splits on
both separators and is the default.
"""
import re
from collections import namedtuple
from typing import List, Optional

from .constants import LINE_RE

# name       the component text, lowercased, portion removed
# amount_g   grams if the text stated them, else None. NEVER invented.
# kind       what this component IS. See below.
# raw        the component exactly as it appeared, for provenance
Component = namedtuple("Component", "name amount_g kind raw")

FOOD             = "food"              # a real food, send it to the bank
CARB_DECLARATION = "carb_declaration"  # a user-entered carb count, no food named
SLOT_LABEL       = "slot_label"        # a meal slot: breakfast, dinner, ...
UNNAMED          = "unnamed"           # the food was never named

# Typed, where `constants.PLACEHOLDERS` is a flat set. PLACEHOLDERS stays what
# it is: a RETRIEVAL filter, the answer to "may I send this to a food bank".
# These are a CLASSIFIER, the answer to "what is this component". The union of
# the three below covers PLACEHOLDERS, and `_check_covers_placeholders` at the
# bottom of this file fails the import if that ever stops being true.
_DECLARATIONS = {"just carbs", "carbs only", "just carb"}
_NO_FOOD      = {"unknown", "none", "nan", "n/a", "", "n a", "unspecified"}
_SLOTS = {
    "breakfast", "lunch", "dinner", "supper", "brunch", "snack", "meal",
    "morning snack", "afternoon snack", "evening snack", "bedtime snack",
    "late night snack", "am snack", "pm snack", "dessert",
}

# A meal string is split on EITHER separator, always. See the module docstring.
_SEPARATORS = re.compile(r"[;\n]")

# LINE_RE demands whitespace before the number. Shanghai's raw text does not
# always supply it: 'Boiled vegetable111 g' does not match, so the whole line
# including the digits becomes the food name and the portion is lost, 27 rows.
# This is a FALLBACK, tried only when LINE_RE has already failed, so no line
# that parses today changes how it parses.
#
# The name must END IN A LETTER for the fallback to fire. Without that guard it
# read 'kirkland egg whites 1s=46g' as the food 'kirkland egg whites 1s=', a
# product code cut in half. Requiring a letter means a missing SPACE gets the
# second chance while a missing WORD does not.
#
# TODO(portion units): neither pattern knows 'mg'. A product named
# 'Omega 3 500mg' will be read as 500 grams by the fallback. Adding mg means
# deciding the unit's scale factor, which is a nutrition question, not a
# parsing one, and it is not in gate A's scope.
_LINE_RE_TIGHT = re.compile(r"^\s*(.*[A-Za-z)\]])\s*(\d+(?:\.\d+)?)\s*(g|ml|IU)\s*$", re.I)

# A PARENTHESISED trailing portion, which is how WellDoc writes one:
#   'Nacho Cheese Tortilla Chips (28g)'
#   'Chicken Alfredo with Fettuccine & Broccoli (397g)'
# LINE_RE anchors on `$` and the closing bracket defeats it, so every one of
# these lost its grams. That matters more than the count suggests: this is the
# ONLY way WellDoc ever states a portion, so without this pattern the entire
# cohort is forced onto the per_100g basis. Found 260821 by the parse lane, a
# dumb oracle counting `<number> <unit>` occurrences in the raw string.
_LINE_RE_PAREN = re.compile(
    r"^\s*(.+?)\s*[\(\[]\s*(\d+(?:\.\d+)?)\s*(g|ml|IU)\s*[\)\]]\s*$", re.I)


def _parse_amount(part: str):
    """'Rice 200 g' -> ('rice', 200.0).  'coffee' -> ('coffee', None)."""
    s = part.strip()
    # Most specific first. The parenthesised form is unambiguous, LINE_RE is the
    # historical primary, and the tight fallback is the permissive last resort.
    for pattern in (_LINE_RE_PAREN, LINE_RE, _LINE_RE_TIGHT):
        m = pattern.match(s)
        if m:
            return m.group(1).strip().lower(), float(m.group(2))
    return s.lower(), None


def _classify(name: str) -> str:
    """A component's name -> its kind. Runs AFTER the portion is stripped."""
    n = name.strip().lower()
    if n in _NO_FOOD:
        return UNNAMED
    if n in _DECLARATIONS:
        return CARB_DECLARATION
    if n in _SLOTS:
        return SLOT_LABEL
    return FOOD


def split_meal(text, dialect: str = "auto") -> List[Component]:
    """One meal string -> typed components. Never raises.

    Args:
        text:    the FoodName value, any dialect, may be None.
        dialect: 'auto' splits on ';' and newline, and is what every caller
                 should use. 'semicolon_list' and 'newline_grams' restrict the
                 separator, for a caller that must reproduce one cohort's
                 historical parse exactly. 'single' does not split at all.

    Returns:
        A list of Component. An empty list means the string held nothing at
        all, which is different from holding a component of kind UNNAMED.
    """
    if text is None or not isinstance(text, str):
        return []

    if dialect == "auto":
        parts = _SEPARATORS.split(text)
    elif dialect == "semicolon_list":
        parts = text.split(";")
    elif dialect == "newline_grams":
        parts = text.split("\n")
    elif dialect == "single":
        parts = [text]
    else:
        raise ValueError(f"unknown dialect {dialect!r}")

    out = []
    for part in parts:
        if not part.strip():
            continue
        name, amount_g = _parse_amount(part)
        out.append(Component(name=name, amount_g=amount_g,
                             kind=_classify(name), raw=part.strip()))
    return out


def foods(components: List[Component]) -> List[Component]:
    """The subset a food bank may be asked about."""
    return [c for c in components if c.kind == FOOD]


def _check_covers_placeholders():
    """PLACEHOLDERS must stay a subset of what this module can type.

    If someone adds a label to PLACEHOLDERS and not here, the retrieval filter
    would refuse a component that this classifier still calls FOOD, and the two
    would silently disagree. Fail at import instead.
    """
    from .constants import PLACEHOLDERS
    typed = _DECLARATIONS | _NO_FOOD | _SLOTS
    missing = {p for p in PLACEHOLDERS if p.strip().lower() not in typed}
    if missing:
        raise ImportError(
            f"food_enrichment.dialect cannot type these PLACEHOLDERS: {sorted(missing)}. "
            f"Add each to _DECLARATIONS, _NO_FOOD or _SLOTS."
        )


_check_covers_placeholders()
