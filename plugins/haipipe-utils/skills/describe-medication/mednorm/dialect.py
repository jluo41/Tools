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

DOSE UNITS ARE NOT IN EVERY LOG
================================================================================
Shanghai puts them inside its medication string, and a named catalogue string
can do the same. WellDoc and Ohio rows instead state a bare number, and the unit
follows from the drug. That is why parse() reports what it FOUND and never
guesses: an absent unit is decided in aggregate.py, after the drug is known.
"""
import json
import re
from collections import namedtuple
from typing import List, Optional

from .constants import (CLASS_ONLY, CODED, DOSE_SENTINELS, G, IU, MG, ML,
                        NAMED, PLACEHOLDER, SENTINEL, UNIT_PER_ML)

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
# Put the compound unit first: otherwise `100 unit/mL` would be read as a
# bare `unit` and leave the denominator behind.
_DOSE_UNIT_RE = r"unit\s*/\s*mL|units\s*/\s*mL|IU\s*/\s*mL|U\s*/\s*mL|IU|mg|g|ml|mL|u"
_NUMBER_RE = r"[\d]+(?:\.[\d]+)?"
# A Shanghai string (or typed words) names each drug, then its dose:
# 'metformin 0.5 g, acarbose 50 mg', 'insulin degludec, 12 IU', 'Humulin 70/30, 8 IU'.
# A dose ends its drug. A combination pill's two-part dose ('Janumet 50/1000 mg',
# 'sitagliptin/metformin 50 mg / 500 mg') is no one number. A ratio with no unit
# after it ('70/30') stays in the name.
_DOSE_AT_RE = re.compile(
    rf"(?<![\w/.])(?:(?P<two>{_NUMBER_RE}\s*(?:(?:{_DOSE_UNIT_RE})\s*)?/\s*{_NUMBER_RE}\s*(?:{_DOSE_UNIT_RE}))"
    rf"|(?P<dose>{_NUMBER_RE})\s*(?P<unit>{_DOSE_UNIT_RE}))\b", re.I)
_SEP_RE = re.compile(r"[,;，；、]")

# A catalogue/free-text medication can put its strength in the item itself,
# outside the Shanghai JSON payload path. This is intentionally anchored at the
# beginning and stops at the first number+unit pair, so the `U-100` in a brand
# qualifier is not mistaken for the stated concentration later in the string.
_EMBEDDED_DOSE_RE = re.compile(
    rf"^(?P<name>.+?)\s+(?P<dose>{_NUMBER_RE})\s*(?P<unit>{_DOSE_UNIT_RE})\b",
    re.I)

_UNIT_CANON = {
    "iu": IU, "u": IU, "mg": MG, "g": G, "ml": ML,
    "unit/ml": UNIT_PER_ML, "units/ml": UNIT_PER_ML,
    "iu/ml": UNIT_PER_ML, "u/ml": UNIT_PER_ML,
}


def canon_unit(u: Optional[str]) -> Optional[str]:
    return _UNIT_CANON.get(re.sub(r"\s+", "", str(u)).lower()) if u else None


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


def split_doses(s: str) -> List[tuple]:
    """A string naming one drug or several, each before its dose ->
    [(name, dose, unit)] in order; [] when it states no dose.

    Never drops a drug. Words between two separators with no dose of their
    own are a drug with no dose ('Janumet, metformin 500 mg'); so are words
    after the last dose when a separator sets them apart. A two-part dose
    keeps its drug and gives it no dose. Words after the last dose with no
    separator ('after dinner') are not a drug, nor are words between a dose
    and the next separator ('500 mg twice, ...')."""
    comps, at = [], 0
    for m in _DOSE_AT_RE.finditer(s):
        parts = _SEP_RE.split(s[at:m.start()])
        if at and len(parts) > 1:                  # words the last dose's own
            parts = parts[1:]
        pieces = [p.strip() for p in parts if p.strip()]
        comps += [(p, None, None) for p in pieces[:-1]]
        name = pieces[-1] if pieces else m.group(0).strip()
        if m.group("two"):
            comps.append((name, None, None))
        else:
            v, u = to_mg(_num(m.group("dose")), canon_unit(m.group("unit")))
            comps.append((name, v, u) if pieces else (name, None, None))
        at = m.end()
    rest = s[at:]
    if comps and _SEP_RE.search(rest):
        comps += [(p.strip(), None, None) for p in _SEP_RE.split(rest)[1:] if p.strip()]
    return comps


def two_part_doses(s: str) -> List[str]:
    """The two-part doses a string states ('50/1000 mg'), each read as no dose."""
    return [m.group("two") for m in _DOSE_AT_RE.finditer(str(s or "")) if m.group("two")]


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
        comps = split_doses(s)
        if comps:
            first = comps[0]
            return Item(NAMED, first[0], first[1], first[2], original,
                        comps if len(comps) > 1 else [])
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

    # Named catalogue strings can carry their own strength. Preserve the
    # explicit number and unit before the resolver strips product/device words.
    m = _EMBEDDED_DOSE_RE.match(text)
    if m:
        v, u = to_mg(_num(m.group("dose")), canon_unit(m.group("unit")))
        name = m.group("name").strip(" ,;-")
        return Item(NAMED, name, v, u, original, [])

    return Item(NAMED, text, d, None, original, [])
