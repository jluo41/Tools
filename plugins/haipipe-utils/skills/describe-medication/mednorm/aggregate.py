"""
Stage 3: a resolved product plus what the log actually stated becomes one
record, carrying the scale its dose is on.

THE DOSE UNIT IS A PROPERTY OF THE DRUG, NOT OF THE LOG
================================================================================
`Dose` arrives as a bare float and there is no unit column anywhere in the
pipeline. Measured over 386,373 WellDoc administrations, the number means two
different things depending on what was taken:

    insulin rows      median 7     international units
    everything else   median 1     tablets or actuations TAKEN, not milligrams

So 39.0 is 39 units of insulin or 39 tablets, and nothing in the row says which.
This file decides the unit AFTER the drug is known, and writes it into a column
next to the number. Rule 4 of haipipe-norm: never report a quantity without the
scale it is on. It is the same defect as reading a per-100g nutrition
composition as a per-meal dose, in a different noun.

WHEN THE UNIT CANNOT BE DECIDED, THE VALUE STILL TRAVELS AND THE UNIT IS NULL.
A dose is not wrong just because we cannot name its unit -- but a consumer that
sums it across drugs is, and a null unit is what stops them.
"""
import re
from typing import Dict, Optional

from .constants import (COUNT, FIELDS, G, IU, MG, ML, PER_ADMIN, TRUSTED)

# An ingredient string that means insulin. Deliberately generous on brand names,
# because the ingredient field sometimes carries one.
# WORD BOUNDARIES MATTER HERE. Without \b, 'aspart' matches 'Amphetamine
# ASPARTate' and five rows of dextroamphetamine were typed as insulin and sent
# to a pharmacokinetics table. A substring is not an ingredient.
INSULIN_RE = re.compile(
    r"\b(insulin|lantus|levemir|tresiba|toujeo|basaglar|semglee|rezvoglar|"
    r"humalog|novolog|apidra|fiasp|lyumjev|admelog|humulin|novolin|afrezza|"
    r"degludec|glargine|lispro|aspart|detemir|glulisine)\b", re.I)

# Dosage forms that are counted rather than measured: 'Dose 1' is one tablet.
COUNTED_FORM_RE = re.compile(
    r"tablet|capsule|caplet|lozenge|suppository|patch|film|wafer|gum|"
    r"troche|pen\b|inhaler|actuation|spray", re.I)

# Forms measured by volume.
VOLUME_FORM_RE = re.compile(r"solution|suspension|syrup|elixir|liquid|drops|"
                            r"concentrate|emulsion", re.I)


def is_insulin(ingredient, brand=None, class_key=None) -> bool:
    for s in (class_key, ingredient, brand):
        if s and INSULIN_RE.search(str(s)):
            return True
    return False


def infer_unit(logged_unit, ingredient, dosage_form, insulin) -> Optional[str]:
    """The unit the number is in.

    A unit the LOG stated always wins -- Shanghai writes 'metformin 0.5 g' and
    that is a measurement, not an inference. Otherwise the drug decides, and
    when the drug cannot decide, the answer is None rather than a guess.
    """
    if logged_unit:
        return logged_unit
    if insulin:
        return IU
    form = str(dosage_form or "")
    if COUNTED_FORM_RE.search(form):
        return COUNT
    if VOLUME_FORM_RE.search(form):
        return ML
    if ingredient:
        # A resolved oral drug with an unrecognised form: the WellDoc app logs
        # 'how many did you take', so COUNT is the app's own semantics rather
        # than a pharmacological guess. Anything unresolved gets None.
        return COUNT
    return None


def empty(source: str, conf: str) -> Dict:
    d = {k: None for k in FIELDS}
    d["MedSource"] = source
    d["MedConf"] = conf
    d["IsInsulin"] = False
    return d


def build(item, hit: Optional[Dict], conf: str, source: str,
          ndc: Optional[str] = None) -> Dict:
    """Assemble the 12 fields for one logged medication."""
    d = empty(source, conf)
    d["NDC"] = ndc

    class_key = item.key if item.kind == "class_only" else None
    ingredient = (hit or {}).get("Ingredient")
    brand = (hit or {}).get("BrandName")
    # THE LOG'S OWN WORDS COUNT TOO, and this is not a nicety. Shanghai writes
    # 'insulin degludec, 12 IU' and 'Novolin R'; neither resolves in the FDA
    # Directory, so an IsInsulin computed only from the bank's answer said False
    # for 59% of Shanghai's insulin and would have routed those rows away from
    # describe-insulin -- the one member of the family that can serve them.
    # A bank miss is not evidence that a thing is not insulin.
    logged = item.key if item.kind in ("named", "class_only") else None
    d["IsInsulin"] = is_insulin(ingredient, brand, class_key or logged)

    # The seam. See constants.IDENTITY for why this is not Ingredient.
    d["DrugKey"] = ingredient or logged or None

    if hit is not None and conf in TRUSTED:
        d["Ingredient"] = ingredient
        d["BrandName"] = brand
        d["PharmClass"] = hit.get("PharmClass")
        d["DosageForm"] = hit.get("DosageForm")
        d["Route"] = hit.get("Route")
    elif class_key:
        # Not a product and never will be, but the class IS what the log said.
        # It travels so describe-insulin can use it; it is not an Ingredient.
        d["PharmClass"] = class_key

    if item.dose is not None:
        d["DoseValue"] = float(item.dose)
        d["DoseUnit"] = infer_unit(item.unit, d["Ingredient"],
                                   d["DosageForm"], d["IsInsulin"])
        d["DoseBasis"] = PER_ADMIN if d["DoseUnit"] else None
    return d
