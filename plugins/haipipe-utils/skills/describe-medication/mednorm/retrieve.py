"""
Stage 2: a typed item becomes an FDA product, or honestly nothing.

THE LADDER, and what each rung is worth
================================================================================
    A  NDC -> FDA product                  GOOD   the drug's own code resolved
                                                  in the FDA's own file. There
                                                  is no better evidence.
    B  generic name -> NONPROPRIETARYNAME  OK     WellDoc writes
                                                  'generic (BRAND) strength
                                                  form', so the leading token is
                                                  usually the ingredient.
    C  brand name -> PROPRIETARYNAME       OK     'Jardiance 25 MG tablet' ->
                                                  Empagliflozin.
    B2 generic prefix, salt dropped        ALIAS  'ATORVASTATIN' ->
                                                  'Atorvastatin Calcium'. Only
                                                  when the prefix picks out one
                                                  ingredient and no combination.
    -  no match                            MISS

GOOD IS REACHABLE HERE, and that is a real difference from describe-exercise,
whose bank is a third-party mirror and whose confidence is capped at OK. This
bank is fetched from accessdata.fda.gov. An NDC that resolves in it is as good
as this kind of evidence gets.

A NAME MATCH IS NOT GOOD, however exact. Two products can share
NONPROPRIETARYNAME and differ in salt, strength, route and form, so tier B and C
return the ingredient and its class and stay at OK. That is enough for
'which drug is this' and not enough for 'which product'.

WHY CLASS_ONLY NEVER REACHES THE BANK
================================================================================
OhioT1DM's 'Basal Insulin' is a THERAPEUTIC CLASS. No product directory can
resolve it, and typing it as a bank miss would blame the bank for something the
log never said. It leaves here with its own source string and goes straight to
describe-insulin, which is the only member of the family that can use it.
"""
from typing import Dict, Optional, Tuple

from . import bank
from .constants import (ALIAS, CLASS_ONLY, CODED, GOOD, MISS, NAMED, OK,
                        PLACEHOLDER, SENTINEL)
from .dialect import Item


def resolve(item: Item) -> Tuple[Optional[Dict], str, str, Optional[str]]:
    """One typed item -> (FDA record or None, confidence, source, ndc).

    Every not-knowing gets its OWN source string, because they have different
    fixes: no drug was named, the number was a sentinel, the id is absent from
    our lexicon, the name is a class, or the FDA file does not list it.
    Rule 5 -- they may not share a column.
    """
    if item.kind == PLACEHOLDER:
        return None, MISS, "not_resolvable:placeholder", None
    if item.kind == SENTINEL:
        return None, MISS, "not_resolvable:sentinel", None
    if item.kind == CLASS_ONLY:
        # A class, on purpose. describe-insulin takes it from here.
        return None, MISS, f"class_only:{item.key}", None

    name, ndc = None, None
    if item.kind == CODED:
        entry = bank.lexicon_lookup(item.key)
        if entry is None:
            return None, MISS, "lexicon:no_such_id", None
        name, ndc = entry["MedicationName"], entry["NDC"]
    else:
        name = item.key

    # A -- the code
    if ndc:
        hit = bank.by_ndc(ndc)
        if hit:
            return hit, GOOD, "fda_ndc:" + str(ndc), ndc

    # B / C -- the name. WellDoc writes 'generic (BRAND) strength form'.
    lead = _lead(name)
    brand = _brand(name)
    for probe, tier in ((lead, "generic"), (brand, "brand")):
        if not probe:
            continue
        hit = bank.by_generic(probe)
        if hit:
            return hit, OK, f"fda_generic:{probe}", ndc
        hit = bank.by_brand(probe)
        if hit:
            return hit, OK, f"fda_brand:{probe}", ndc

    # B2 -- the ingredient without its salt
    for probe in (lead, brand):
        if not probe:
            continue
        hit = bank.by_generic_prefix(probe)
        if hit:
            return hit, ALIAS, f"fda_generic_prefix:{probe}", ndc

    return None, MISS, "fda:no_match", ndc


import re as _re

# Concentration and device words that are not part of the drug's name.
# 'insulin aspart U-100' failed every tier until U-100 was stripped -- the
# strength was written as a LETTER-led token, which the numeric rule below
# cannot see. That one id is 5,846 administrations.
_STRENGTH_RE = _re.compile(
    r"\b(u-?\d+|\d+/\d+|\d[\d./,-]*\s*(mg|mcg|g|ml|unit|units|%|iu)\b.*)", _re.I)
_DEVICE_RE = _re.compile(
    r"\b(insuln|insulin pen|pen|kwikpen|flexpen|solostar|tempo|sensor|"
    r"cartridge|vial|inj|injection|solution|soln|susp|suspension)\b", _re.I)


def _clean(s: str) -> str:
    s = _STRENGTH_RE.sub(" ", str(s or ""))
    s = _DEVICE_RE.sub(" ", s)
    return _re.sub(r"[\s,;-]+$", "", _re.sub(r"\s+", " ", s)).strip()


def _lead(name) -> str:
    """The text before the first parenthesis, with strength and device words
    stripped. 'insulin aspart U-100 (NOVOLOG FLEXPEN...)' -> 'insulin aspart'."""
    return _clean(str(name or "").split("(")[0])


def _brand(name) -> str:
    """The first token inside the first parenthesis, cleaned the same way.
    'metFORMIN (GLUCOPHAGE) 500 MG tablet' -> 'GLUCOPHAGE'."""
    m = _re.search(r"\(([^)]*)\)", str(name or ""))
    if not m:
        # No parenthesis: the whole string may itself be a brand.
        return _lead(name)
    return _clean(_re.split(r"[,;]", m.group(1))[0])
