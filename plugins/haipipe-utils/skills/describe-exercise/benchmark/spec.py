"""
describe-exercise's NounSpec.

WHERE THE GOLD COMES FROM
================================================================================
No public corpus of PATIENT-LOGGED exercise strings coded to the Compendium has
been found, so the VALUE gold has to come off this board. It does, and it is NOT
circular:

(Corrected 260822: an earlier version of this docstring said no Compendium-coded
corpus existed at all. CAPTURE-24 does -- 206 CPA codes, human-annotated at
Cohen's kappa > 0.8, CC-BY. Its text is wearable-camera descriptions rather than
a patient's own log entry, so it is not a drop-in for this gold, but it is a
real external resource for the IDENTITY question and the claim was too broad.)

    MET_device = CaloriesBurned * 200 / (3.5 * kg * minutes)

the standard back-solve of  kcal/min = MET * 3.5 * kg / 200. The kcal is what
the vendor's app logged; the mass comes from Weight.parquet.

The one thing that could have ruined it -- a vendor computing its kcal from a
MET table, which would make the gold the prediction in disguise -- was tested
and rejected. See taxonomy.py.

WHAT IS BEING GRADED, PRECISELY
================================================================================
Not "is the Compendium right". The Compendium's numbers ARE indirect
calorimetry; they are the reference standard by construction. What is graded is
whether THIS ROW was mapped to the right Compendium entry, and how far this
person's actual intensity sat from the population value that entry carries.

Those two failures are not separable with this gold, and the report says so.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from taxonomy import (classify_kind, classify_label, GRADEABLE, DEVICE_MET,
                      MIN_MET, MAX_MET)

from xbench import NounSpec
from xbench.score import mae_r

from exnorm import normalize

ROOT = Path("/home/jluo41/WellDoc-SPACE")
SOURCE_STORE = ROOT / "_WorkSpace/1-SourceStore"

LB_TO_KG = 0.45359237
MIN_KG, MAX_KG = 35.0, 250.0
MAX_MINUTES = 240.0          # same bound the resolver refuses a dose above


def _weights(cohort: str):
    """PatientID -> median body mass in kg. WellDoc stores Weight in POUNDS."""
    p = list(SOURCE_STORE.glob(f"{cohort}/@*/Weight.parquet"))
    if not p:
        return {}
    w = pd.read_parquet(p[0])[["PatientID", "Weight"]]
    w["Weight"] = pd.to_numeric(w.Weight, errors="coerce") * LB_TO_KG
    w = w[w.Weight.between(MIN_KG, MAX_KG)]
    return w.groupby("PatientID").Weight.median().to_dict()


def _augment(df: pd.DataFrame, cohort: str) -> pd.DataFrame:
    """Attach the back-solved device MET. Absent inputs leave it NaN, which
    taxonomy turns into a non-gradeable label rather than a wrong number."""
    df = df.copy()
    kg = df.PatientID.map(_weights(cohort))
    kcal = pd.to_numeric(df.get("CaloriesBurned"), errors="coerce")
    mins = pd.to_numeric(df.get("ExerciseDuration"), errors="coerce")
    ok = kg.notna() & kcal.gt(0) & mins.between(1, MAX_MINUTES)
    met = kcal * 200.0 / (3.5 * kg * mins)
    df["MET_device"] = met.where(ok & met.between(MIN_MET, MAX_MET))
    df["BodyMassKg"] = kg
    return df


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(normalize(
        list(df.ExerciseType.astype(str)),
        minutes=list(pd.to_numeric(df.ExerciseDuration, errors="coerce")),
        weight_kg=list(pd.to_numeric(df.BodyMassKg, errors="coerce")),
        source_ids=list(df.EntrySourceID),
    ))
    out.index = df.index
    return pd.concat([df, out], axis=1)


def _metric(df: pd.DataFrame, label: str) -> dict:
    if label != DEVICE_MET:
        return {"mae": None, "r": None, "scored": 0,
                "note": "no independent MET on this cell; coverage only"}
    e = df[df.METValue.notna() & df.true_MET_device.notna()].copy()
    e["METValue"] = pd.to_numeric(e.METValue, errors="coerce")
    e = e[e.METValue.notna()]
    mae, r, n = mae_r(e.true_MET_device, e.METValue)
    out = {"mae": mae, "r": r, "scored": n, "unit": "MET"}
    if n >= 10:
        d = (e.METValue - e.true_MET_device)
        out["bias"] = round(float(d.mean()), 2)
        for t in (1, 2, 3):
            out[f"within_{t}"] = round(float((d.abs() <= t).mean()), 4)
        # THE CEILING. Replace the Compendium with the best possible
        # activity-name-only predictor -- the median device MET of that very
        # activity, fitted on these same rows -- and see how far r can go at
        # all. Anything above this line is not reachable by naming the
        # activity; it is within-activity, within-person variation.
        n_groups = e.ExerciseType.nunique()
        if len(e) >= 3 * n_groups:
            med = e.groupby("ExerciseType").true_MET_device.transform("median")
            if med.std() > 0:
                out["ceiling_r"] = round(
                    float(np.corrcoef(e.true_MET_device, med)[0, 1]), 3)
        else:
            # With one row per activity the per-activity median IS the row and
            # the ceiling reads 1.000, which is arithmetic, not a finding. The
            # deduped weighting is degenerate for this noun anyway: the input
            # vocabulary is a 130-entry codebook, not free text.
            out["ceiling_r"] = None
            out["ceiling_note"] = "undefined: too few rows per activity"
    return out


SPEC = NounSpec(
    noun="exercise",
    frame="Exercise",
    text_col="ExerciseType",
    id_cols=("PatientID", "ExerciseEntryID"),
    label_cols=("MET_device",),
    extra_cols=("EntrySourceID", "ExerciseDuration", "CaloriesBurned",
                "ExerciseIntensity", "BodyMassKg"),
    conf_col="ExerciseConf",
    basis_col="ExerciseBasis",
    derived_col=None,
    classify_shape=classify_kind,
    classify_label=classify_label,
    gradeable=GRADEABLE,
    derived_label="derived",     # declared, never produced. See taxonomy.py.
    circular_conf=(),            # the Compendium never saw a WellDoc patient
    augment=_augment,
    normalize=_normalize,
    metric=_metric,
).check()
