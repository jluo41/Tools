"""
The dialect layer: one logged medication, however its cohort wrote it, becomes
a TYPED item.

THREE DIALECTS WEARING ONE SCHEMA
================================================================================
All six cohorts with medication data share the same 11-column Source table, and
the column contents are three unrelated languages. Measured 260822 over 397,133
rows:

  welldoc_id    386,373   MedicationID 612997, Dose 39.0. No name anywhere in
                          the row; the name lives in a pooled lexicon.
  ohio_type       5,026   MedicationID is EMPTY -- zero distinct values. The
                          drug is in the JSON as 'Basal Insulin' / 'Bolus
                          Insulin'. A CLASS, not a product: it can never resolve
                          in a product directory, and typing it as a bank miss
                          would be a lie about what is wrong.
  shanghai_text   5,805   MedicationID is a CATEGORY STRING, and the name is in
                          the JSON in one of four sub-forms, each determined by
                          that category:
                            bare number   2,176  '0.6'  -- the dose; the drug is
                                                 named by the category (Novolin R)
                            drug+dose     2,304  'metformin 0.5 g'
                              of which      736  are MULTI-DRUG in one string:
                                                 'liraglutide 1.2 mg, acarbose
                                                  50 mg, metformin 0.5 g'
                                                 -- the same shape as describe-
                                                 food's item_list
                            'drug, N IU'  1,214  'insulin degludec, 12 IU'
                          Units are mixed: mg 2,440 and g 798, so
                          'metformin 0.5 g' must normalise to 500 mg.

DOSE UNITS ARE NOT IN THE LOG
================================================================================
Except in Shanghai, where they are inside the string. WellDoc and Ohio state a
bare number, and the unit follows from the drug. That is why parse() reports
what it FOUND and never guesses: the unit is decided in aggregate.py, after the
drug is known.
"""
import json
import re
from collections import namedtuple
from typing import List, Optional

from .constants import (CLASS_ONLY, CODED, DOSE_SENTINELS, G, IU, MG, ML,
                        NAMED, PLACEHOLDER, SENTINEL)

# One logged medication, typed.
#   kind        constants.TYPES
#   key         the id (coded) or the drug string (named/class_only)
#   dose        the number the log stated, or None
#   unit        the unit the log stated, only when the log actually stated one
#   raw         exactly what came in
#   components  >1 only for a multi-drug Shanghai string
Item = namedtuple("Item", "kind key dose unit raw components")

PLACEHOLDER_TEXT = {"", "none", "nan", "null", "n/a", "na", "unknown", "other"}

# WellDoc ids that are obviously not products. 1,452 rows.
SENTINEL_IDS = {"0", "777777", "777778", "777779", "999999", "1999999"}

# OhioT1DM. A therapeutic class; describe-insulin takes these directly.
CLASS_TEXT = {
    "basal insulin": "basal insulin",
    "bolus insulin": "bolus insulin",
    "long acting insulin": "basal insulin",
    "rapid acting insulin": "bolus insulin",
}

# Shanghai's category strings -> the drug the category itself names.
SHANGHAI_CATEGORY = {
    "csii - basal insulin (novolin r, iu / h)": ("Novolin R", IU),
    "csii - bolus insulin (novolin r, iu)": ("Novolin R", IU),
    "insulin dose - s.c.": (None, IU),
    "insulin dose - i.v.": (None, IU),
    "non-insulin hypoglycemic agents": (None, None),
}

_CODE_RE = re.compile(r"^\d+$")
_BARE_NUM_RE = re.compile(r"^\s*[\d.]+\s*$")
# 'metformin 0.5 g' / 'acarbose 50 mg'
_DRUG_DOSE_RE = re.compile(r"([A-Za-z][A-Za-z\- ]*[A-Za-z])\s+([\d.]+)\s*(IU|mg|g|ml|mL|u)\b")
# 'insulin degludec, 12 IU' / 'Novolin R, 5 IU'
_DRUG_COMMA_RE = re.compile(r"^(.+?),\s*([\d.]+)\s*(IU|U|mg|g|ml)\b", re.I)

_UNIT_CANON = {"iu": IU, "u": IU, "mg": MG, "g": G, "ml": ML, "mL": ML}


def canon_unit(u: Optional[str]) -> Optional[str]:
    return _UNIT_CANON.get(str(u).lower()) if u else None


def to_mg(value: float, unit: Optional[str]):
    """g -> mg. 'metformin 0.5 g' and 'metformin 500 mg' are the same
    prescription and must not sort into two different buckets."""
    if unit == G and value is not None:
        return value * 1000.0, MG
    return value, unit


def _num(x):
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    return None if f != f else f


def parse(raw, dose=None, payload=None) -> Item:
    """Type one logged medication. Never raises, never drops, never guesses.

    raw      the MedicationID column: an integer id, a Shanghai category, or a
             drug name.
    dose     the Dose column, when the caller has it.
    payload  the `medication` JSON column, when the caller has it. Ohio's drug
             class and Shanghai's drug string live only in there.
    """
    original = raw
    text = "" if raw is None else str(raw).strip()
    d = _num(dose)
    if d in DOSE_SENTINELS:
        # 255 is uint8 overflow, not 255 units. Typed, and the number withheld.
        return Item(SENTINEL, text or None, None, None, original, [])

    inner = None
    if payload:
        try:
            js = json.loads(payload) if isinstance(payload, str) else dict(payload)
            inner = js.get("MedicationName") or js.get("MedicationType")
        except Exception:
            inner = None

    # --- OhioT1DM: a class, never a product -------------------------------
    if inner and str(inner).strip().lower() in CLASS_TEXT:
        return Item(CLASS_ONLY, CLASS_TEXT[str(inner).strip().lower()], d, IU,
                    original, [])

    # --- Shanghai: the category decides which sub-form the name takes ------
    cat = SHANGHAI_CATEGORY.get(text.lower())
    if cat is not None:
        drug_from_cat, cat_unit = cat
        s = str(inner or "").strip()
        if _BARE_NUM_RE.match(s):
            # the string IS the dose; the drug is whatever the category names
            return Item(NAMED if drug_from_cat else CLASS_ONLY,
                        drug_from_cat or "insulin", _num(s), cat_unit,
                        original, [])
        m = _DRUG_COMMA_RE.match(s)
        if m:
            v, u = to_mg(_num(m.group(2)), canon_unit(m.group(3)))
            return Item(NAMED, m.group(1).strip(), v, u, original, [])
        found = _DRUG_DOSE_RE.findall(s)
        if found:
            comps = []
            for name, val, unit in found:
                v, u = to_mg(_num(val), canon_unit(unit))
                comps.append((name.strip(), v, u))
            first = comps[0]
            return Item(NAMED, first[0], first[1], first[2], original, comps)
        if s and s.lower() not in PLACEHOLDER_TEXT:
            return Item(NAMED, s, d, cat_unit, original, [])
        return Item(PLACEHOLDER, None, d, None, original, [])

    # --- WellDoc: a bare integer id ---------------------------------------
    if _CODE_RE.match(text):
        if text in SENTINEL_IDS:
            return Item(SENTINEL, text, None, None, original, [])
        return Item(CODED, text, d, None, original, [])

    if not text or text.lower() in PLACEHOLDER_TEXT:
        return Item(PLACEHOLDER, None, d, None, original, [])

    return Item(NAMED, text, d, None, original, [])
