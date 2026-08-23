"""
Stage 3: a compendium entry plus what the log actually stated becomes one
record, carrying the scale it is on.

MET IS A RATE. KCAL IS A DOSE. This file is the only place they meet, and it
refuses to cross the gap without both of the things that bridge it:

    kcal = MET x 3.5 mL O2/kg/min x body_mass_kg / 200 x minutes

Missing minutes, missing mass, or both -> no kcal, and ExerciseBasis says
per_minute so a reader knows a RATE is what they are holding. Inventing either
denominator is rule 4's exact prohibition, and it is the same defect that made
describe-food read a per-100g composition as a per-meal dose.
"""
from typing import Dict, Optional

from .constants import (FIELDS, KCAL_PER_L_O2, MAX_BOUT_MINUTES, PER_MINUTE,
                        PER_SESSION, POPULATION, TRUSTED, VO2_REST_ML_KG_MIN)


def kcal_from_met(met: float, minutes: float, weight_kg: float) -> float:
    """The compendium's own conversion. All three inputs are required; there is
    no default body mass, because a default body mass is a fabricated number
    wearing a plausible value."""
    kcal_per_min = met * VO2_REST_ML_KG_MIN * weight_kg / 1000.0 * KCAL_PER_L_O2
    return kcal_per_min * minutes


def empty(source: str, conf: str, resolved=None) -> Dict:
    """A MISS in the same shape as a hit. A caller never branches on whether a
    result came back; it branches on ExerciseConf."""
    d = {k: None for k in FIELDS}
    d["ExerciseSource"] = source
    d["ExerciseConf"] = conf
    d["ExerciseBasis"] = None
    d["ActivityResolved"] = resolved
    # The scale axis is stated even on a miss. `population` with no number is
    # the truth about a row that got no MET: nobody adjusted anything.
    d["METScale"] = POPULATION
    d["METScaleFactor"] = None
    return d


def build(act, row: Optional[Dict], conf: str, source: str,
          minutes: Optional[float] = None,
          weight_kg: Optional[float] = None,
          scale=None) -> Dict:
    """Assemble the 14 fields for one activity.

    `scale` is a (factor, tier, provenance) triple from scale.factor_for, or
    None for the floor. It adjusts the RATE and therefore the dose derived from
    it, and it NEVER touches which activity was resolved -- an adjustment on top
    of the wrong entry is still the wrong entry, only harder to spot."""
    d = empty(source, conf)
    # Rule 5. The NAME's provenance is its own pair, separate from the value's,
    # because 'a patient typed Walking' and 'Apple's enum says 52 is walking'
    # are different evidence for the same word, and a reader must be able to
    # tell them apart without going back to the source frame.
    d["TypeSource"] = f"{act.kind}|{act.via or 'none'}"
    d["TypeConf"] = ("CODEBOOK" if str(act.via).startswith("codebook:")
                     else "LOGGED" if act.via == "text" else None)

    if row is None:
        return d

    # The identity ALWAYS travels, even at WEAK, so a person can curate it.
    # describe-food computes fdc_id and then discards it; that is recorded as a
    # defect in _FoodInfo/README.md and is not repeated here.
    d["ActivityResolved"] = row["activity_description"]
    d["ActivityCode"] = row["activity_code"]
    d["MajorHeading"] = row["major_heading"]

    if conf not in TRUSTED:
        return d                      # candidate shown, value withheld

    # The reference ALWAYS travels unmodified. It is what ActivityCode points
    # at, so a reader can check the adjustment or undo it.
    d["METReference"] = row["met_value"]

    # A factor may only ride on a TRUSTED identity. Scaling a WEAK guess would
    # dress an unknown activity in a personal-looking number, which is rule 3's
    # exact prohibition read one layer up.
    factor, tier, prov = scale if scale else (1.0, POPULATION, None)
    d["METScale"] = tier
    d["METScaleFactor"] = round(float(factor), 4)
    met = row["met_value"] * float(factor)
    d["METValue"] = round(met, 2) if factor != 1.0 else row["met_value"]
    if prov:
        d["ExerciseSource"] += f"|{prov}"

    if minutes is not None and minutes > 0:
        d["ActiveMinutes"] = float(minutes)      # always the log's own claim

    dosable = (d["ActiveMinutes"] is not None
               and d["ActiveMinutes"] <= MAX_BOUT_MINUTES
               and weight_kg)
    if dosable:
        # The dose follows the RATE actually reported, never the reference. A
        # kcal computed off the unscaled MET while METValue says otherwise would
        # be two answers to one question.
        d["CaloriesBurnedEst"] = round(
            kcal_from_met(d["METValue"], d["ActiveMinutes"], float(weight_kg)), 1)
        d["ExerciseBasis"] = PER_SESSION
    else:
        d["ExerciseBasis"] = PER_MINUTE
        if d["ActiveMinutes"] is not None and d["ActiveMinutes"] > MAX_BOUT_MINUTES:
            # Say WHY the dose is missing. 'no duration was stated' and 'the
            # duration stated is not a bout' are different facts about the log
            # and must not share a silent NULL.
            d["ExerciseSource"] += f"|bout>{MAX_BOUT_MINUTES:g}min"
    return d
