"""
The WITHIN-PERSON TIME SPLIT: the fence the person scale tier cannot exist
without.

WHY A SECOND SPLIT
================================================================================
`2-corpus/gold_index.parquet` already carries a patient-hash split, and that
split answers a real question -- does this resolver hold up on a different set
of people. It cannot answer the other one. A test patient has ZERO training
rows by construction, so a factor personal to them could only ever be fit on the
very rows it is scored on. That is not a weak measurement; it is the same
circularity that once read as r 0.988 in describe-food, and haipipe-norm rule 11
exists to stop it.

    by patient   does it hold on people we have never seen?
    by time      after seeing THIS person N times, is it better?   <- this file

Both are needed and neither replaces the other.

THE FENCE IS ORDINAL, NOT A DATE
================================================================================
Each patient's gradeable bouts are ordered by their own clock and the FIRST
`CALIB_BOUTS` are the calibration set. Everything later is evaluation. A single
global cut-off date would have been simpler and wrong: patients enrol at
different times, so one date gives an early joiner years of history and a late
joiner none, and the resulting number would measure enrolment rather than
calibration.

A patient whose whole record is shorter than `CALIB_BOUTS + MIN_EVAL` gets
`short`. They are NOT dropped -- they are exactly the cold-start population the
device tier exists for, and counting them is how anyone can see what fraction of
the board a person tier could ever reach.

    source .venv/bin/activate && source env.sh
    python build_person_split.py
"""
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
SOURCE_STORE = ROOT / "_WorkSpace/1-SourceStore"
CORPUS = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_ExerciseInfo/2-corpus"

CALIB_BOUTS = 5     # how many of a person's own bouts the factor may see
MIN_EVAL = 5        # and how many must remain, or the person is cold-start


def _timestamps(cohorts):
    """gold_index does not carry the clock; the source frame does."""
    fr = []
    for c in cohorts:
        for f in sorted(SOURCE_STORE.glob(f"{c}/@*/Exercise.parquet")):
            d = pd.read_parquet(f)[["PatientID", "ExerciseEntryID",
                                    "ObservationDateTime"]]
            d["cohort"] = c
            fr.append(d)
    t = pd.concat(fr, ignore_index=True)
    t["PatientID"] = t.PatientID.astype(str)
    t["ExerciseEntryID"] = t.ExerciseEntryID.astype(str)
    return t


def main():
    g = pd.read_parquet(CORPUS / "gold_index.parquet")
    grad = g[(g["shape"] == "session") & (g["label"] == "device_met")].copy()
    grad["PatientID"] = grad.PatientID.astype(str)
    grad["ExerciseEntryID"] = grad.ExerciseEntryID.astype(str)

    t = _timestamps(sorted(grad.cohort.unique()))
    d = grad.merge(t, on=["cohort", "PatientID", "ExerciseEntryID"], how="left")
    d["ts"] = pd.to_datetime(d.ObservationDateTime, errors="coerce",
                             format="mixed")
    missing = int(d.ts.isna().sum())
    d = d[d.ts.notna()]

    # A person's own clock. Ties broken by entry id so the order is stable
    # across rebuilds -- a split that reshuffles is not a fence.
    d = d.sort_values(["cohort", "PatientID", "ts", "ExerciseEntryID"])
    d["bout_rank"] = d.groupby(["cohort", "PatientID"]).cumcount()
    d["n_bouts"] = d.groupby(["cohort", "PatientID"]).PatientID.transform("size")

    short = d.n_bouts < CALIB_BOUTS + MIN_EVAL
    d["person_split"] = "eval"
    d.loc[d.bout_rank < CALIB_BOUTS, "person_split"] = "calib"
    d.loc[short, "person_split"] = "short"

    # The moment a person's factor stops being allowed to look. Any row at or
    # before this is fit material; anything after is scoreable. Written per
    # patient so a reader can audit one person without rerunning anything.
    cut = (d[d.person_split == "calib"].groupby(["cohort", "PatientID"]).ts.max()
           .rename("calib_until").reset_index())
    d = d.merge(cut, on=["cohort", "PatientID"], how="left")

    out = d[["cohort", "PatientID", "ExerciseEntryID", "ts", "bout_rank",
             "n_bouts", "person_split", "calib_until", "split"]]
    out.to_parquet(CORPUS / "person_split.parquet", index=False)

    pats = d.groupby(["cohort", "PatientID"]).person_split.first()
    summary = {
        "calib_bouts": CALIB_BOUTS, "min_eval": MIN_EVAL,
        "gradeable_rows": int(len(grad)),
        "rows_without_a_clock": missing,
        "rows": {k: int(v) for k, v in d.person_split.value_counts().items()},
        "patients_total": int(d.groupby(['cohort', 'PatientID']).ngroups),
        "patients_cold_start": int((pats == "short").sum()),
        "eval_rows_by_patient_split":
            {k: int(v) for k, v in
             d[d.person_split == "eval"].split.value_counts().items()},
    }
    (CORPUS / "_person_split_summary.json").write_text(json.dumps(summary, indent=1))

    print(f"  gradeable rows           {len(grad):>8,d}")
    print(f"  no clock, dropped        {missing:>8,d}")
    for k in ("calib", "eval", "short"):
        n = int((d.person_split == k).sum())
        print(f"  {k:<24s} {n:>8,d}  ({n/len(d):.1%})")
    print(f"  patients                 {summary['patients_total']:>8,d}"
          f"   cold-start {summary['patients_cold_start']}")
    print(f"\n  wrote {CORPUS}/person_split.parquet")


if __name__ == "__main__":
    main()
