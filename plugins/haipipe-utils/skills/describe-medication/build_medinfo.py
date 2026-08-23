#!/usr/bin/env python3
"""
Build `_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo/`.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-medication/build_medinfo.py

Emits the xinfo-v1 shape shared by _FoodInfo and _ExerciseInfo, so a benchmark
that reads coverage, confidence or basis is written once for all four nouns.
This file owns only what is about MEDICATION; the folder's shape belongs to
`haipipe-norm/xinfo`.

Covers describe-medication ONLY since insulin moved to `_InsInfo`. The two are
still one chain -- the insulin skill's input is this skill's DrugKey -- and the
handoff is measured in `_InsInfo/README.md`, which counts per cohort the rows
only the second half can reach.
"""
import glob
import json
import os
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(HERE.parent / "describe-insulin"),
                str(HERE.parent / "haipipe-norm")]

from mednorm import normalize as mednorm                      # noqa: E402
from mednorm.constants import BANK, LEXICON                   # noqa: E402
from insnorm import normalize as insnorm                      # noqa: E402
from xinfo import CohortStats, copy_api_examples, link_reference, write  # noqa: E402

# The three _XInfo folders live together under 0-EventNorm/ -- they are
# one layer of one system, not three folders that happen to share a
# parent with every raw cohort dump.
DEST = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo"

# Where each cohort's medication rows came from. One line, no hedging.
ORIGIN = {
    "WellDoc2022CGM": "app MedAdministration: an integer id and a bare dose",
    "WellDoc2025ALS": "app MedAdministration: an integer id and a bare dose",
    "WellDoc2025CVS": "app MedAdministration: an integer id and a bare dose",
    "WellDoc2025LLY": "app MedAdministration: an integer id and a bare dose",
    "WellDoc2026Libre": "app MedAdministration: table present, no rows",
    "OhioT1DM": "study log: a therapeutic CLASS ('Basal Insulin'), never a product",
    "Shanghai": "clinical sheet, five insulin/oral columns, drug and dose in one string",
    "CGMacros": "no medication table content",
    "dubosson": "no medication table content",
    "aireadi-noimage-v2": "no medication table content",
    "aireadi-v3": "no medication table content",
}


def frames():
    for p in sorted(glob.glob(str(ROOT / "_WorkSpace/1-SourceStore/*/*/Medication.parquet"))):
        yield p.split("/")[-3], pd.read_parquet(p)


def patient_dia():
    """The one per-patient gold in this whole noun: a duration of insulin
    action the prescriber recorded for THIS person. 3 preset values, so it is
    a clinician's SETTING and not a PK study -- but it is per-patient, and
    nothing else here is."""
    fs = [f for f in glob.glob(str(ROOT / "_WorkSpace/0-RawDataStore/WellDoc*/Source/*MedPrescription.csv"))
          if "DaySchedule" not in f]
    if not fs:
        return pd.DataFrame()
    rx = pd.concat([pd.read_csv(f, low_memory=False) for f in fs], ignore_index=True)
    d = pd.to_numeric(rx.get("DIA"), errors="coerce")
    return rx[d > 0].assign(dia=d[d > 0])


def page(coh, df, res, ins, dia_n):
    """One cohort page: what goes in, and what comes out."""
    L = [f"# {coh} — medication", ""]
    if not len(df):
        L += ["The Medication table exists and is empty.", "",
              f"origin: {ORIGIN.get(coh, 'unknown')}", ""]
        return "\n".join(L)
    kinds = res.MedSource.str.split(":").str[0].value_counts()
    L += [f"origin: {ORIGIN.get(coh, 'unknown')}", "",
          "```text",
          f"  rows            {len(df):>9,}",
          f"  patients        {df.PatientID.nunique():>9,}",
          f"  span            {pd.to_datetime(df.AdministrationDate, errors='coerce', format='mixed').min()}"
          f"  ..  {pd.to_datetime(df.AdministrationDate, errors='coerce', format='mixed').max()}",
          "",
          "  OUT",
          f"  ingredient      {res.Ingredient.notna().sum():>9,}  {res.Ingredient.notna().mean():6.1%}",
          f"  dose has a unit {res.DoseUnit.notna().sum():>9,}  {res.DoseUnit.notna().mean():6.1%}",
          f"  is insulin      {res.IsInsulin.sum():>9,}  {res.IsInsulin.mean():6.1%}",
          f"  insulin -> PK   {int(ins):>9,}",
          f"  per-patient DIA {dia_n:>9,}   (the only gold this cohort offers)",
          "",
          "  MedSource, by kind"] + [
              f"  {k:<22} {v:>9,}" for k, v in kinds.items()] + [
          "",
          "  confidence"] + [
              f"  {k:<22} {v:>9,}" for k, v in res.MedConf.value_counts().items()] + [
          "```", "",
          "## Two real rows", "", "```text"]
    for _, r in df.head(2).iterrows():
        L.append("  " + json.dumps({k: (None if pd.isna(v) else str(v)[:60])
                                    for k, v in r.items()}, ensure_ascii=False)[:300])
    L += ["```", ""]
    return "\n".join(L)


def write_contract(dest):
    """4-contract: what a record IS, as a schema plus real rows.

    Contributed by _FoodInfo. A schema without worked specimens is a wish; a
    specimen is a row that actually came out of the service."""
    import mednorm
    d = dest / "4-contract"
    d.mkdir(parents=True, exist_ok=True)
    from mednorm.constants import BASES, FIELDS, TYPES, UNITS
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "mednorm-v1.response",
        "title": "one describe-medication result",
        "description": ("The SAME 13 keys on a hit and on a miss, so a caller "
                        "never branches on shape -- only on MedConf."),
        "type": "object", "additionalProperties": False,
        "required": list(FIELDS),
        "properties": {
            "DoseValue": {"type": ["number", "null"]},
            "DoseUnit": {"enum": [u for u in UNITS]},
            "DoseBasis": {"enum": [b for b in BASES]},
            "DrugKey": {"type": ["string", "null"],
                        "description": "the seam to describe-insulin. The FDA "
                        "ingredient when the Directory listed the drug, the "
                        "log's own words when it did not. Non-null on 100% of "
                        "insulin rows; Ingredient is non-null on 58% of them."},
            "Ingredient": {"type": ["string", "null"]},
            "BrandName": {"type": ["string", "null"]},
            "PharmClass": {"type": ["string", "null"]},
            "DosageForm": {"type": ["string", "null"]},
            "Route": {"type": ["string", "null"]},
            "NDC": {"type": ["string", "null"]},
            "MedSource": {"type": "string",
                          "description": "one of five prefixes, one per kind of "
                          "not-knowing: not_resolvable:placeholder, "
                          "not_resolvable:sentinel, lexicon:no_such_id, "
                          "class_only:<class>, fda:no_match -- or a hit's tier."},
            "MedConf": {"enum": ["GOOD", "OK", "ALIAS", "WEAK", "MISS"]},
            "IsInsulin": {"type": "boolean"},
        },
    }
    (d / "mednorm-v1.response.schema.json").write_text(
        json.dumps(schema, indent=2) + "\n")

    specimens = [
        ("1-welldoc-id-insulin", {"item": "612997", "dose": 39}, None,
         "the commonest row in the corpus: an integer, a bare number, no name"),
        ("2-welldoc-id-tablet", {"item": "155744", "dose": 1}, None,
         "the same shape, and Dose 1 means one TABLET, not one milligram"),
        ("3-ohio-class-only", {"item": "x", "dose": 1.5}, {"MedicationType": "Basal Insulin"},
         "a therapeutic CLASS. Ingredient stays null on purpose"),
        ("4-shanghai-grams", {"item": "Non-insulin hypoglycemic agents"},
         {"MedicationName": "metformin 0.5 g"}, "the unit is in the string; 0.5 g -> 500 mg"),
        ("5-shanghai-csii-bare-number", {"item": "CSII - basal insulin (Novolin R, IU / H)", "dose": 0.6},
         {"MedicationName": "0.6"}, "the name field holds the DOSE; the category names the drug"),
        ("6-sentinel-dose", {"item": "612997", "dose": 255}, None,
         "255 is uint8 overflow; the value is withheld"),
        ("7-no-drug-no-unit", {"item": "999999999", "dose": 5}, None,
         "a real dose whose unit is unknowable: DoseUnit and DoseBasis both null"),
    ]
    for name, body, payload, why in specimens:
        out = mednorm.normalize([body["item"]], doses=body.get("dose"),
                                payloads=json.dumps(payload) if payload else None,
                                transport="local")[0]
        (d / f"{name}.json").write_text(json.dumps(
            {"why": why, "request": dict(body, **({"payload": payload} if payload else {})),
             "response": out}, indent=2, ensure_ascii=False) + "\n")
    (d / "README.md").write_text(
        "# 4-contract\n\nThe record's JSON Schema and worked specimens, every one a real\n"
        "response from the running service. Regenerated by `build_medinfo.py`.\n")
    return len(specimens)


def write_corpus(dest, dia):
    """NOTHING. THE DIA RULER MOVED TO describe-insulin ON 260822.

    This function used to build `I3a_DIA.parquet`. It should not: DIA is a
    duration of insulin action, nothing in describe-medication can be graded by
    it, and the version written here carried three columns that were OUR ANSWER
    rather than the answer key -- `table_duration_h`, `InsulinClass`,
    `abs_err_h`. A ruler that moves when the PK table moves cannot measure the
    PK table, and those columns went stale the first time an alias was added.

    The owner is now:

        describe-insulin/benchmark/build_units.py::gold_dia()
            -> _InsInfo/2-corpus/WellDoc/I3a_DIA.parquet   (gold + provenance)
        describe-insulin/benchmark/run_bench.py::run_dia()
            -> the error, computed at grading time

    Kept as a no-op rather than deleted so that a reader who greps for
    `I3a_DIA` in this file finds out where it went instead of finding nothing.
    """
    return 0


def main():
    dia = patient_dia()
    dia_ids = set(pd.to_numeric(dia.get("MedicationID"), errors="coerce").dropna().astype(int)) if len(dia) else set()

    stats, pages = [], {}
    for coh, df in frames():
        if not len(df):
            stats.append(CohortStats(noun="medication", cohort=coh, rows=0,
                                     origin=ORIGIN.get(coh)))
            pages[coh] = page(coh, df, None, 0, 0)
            continue
        res = pd.DataFrame(mednorm(df.MedicationID.tolist(),
                                   doses=df.Dose.tolist(),
                                   payloads=df["medication"].tolist()))
        kind = res.MedSource.str.split(":").str[0]
        # A sentinel, a placeholder and a bare CLASS can never resolve in a
        # PRODUCT directory. Counting them against the resolver measures the
        # log, not the resolver.
        never = kind.isin(["not_resolvable", "class_only"])
        excluded = kind[never].value_counts().to_dict()

        ins_keys = res.loc[res.IsInsulin, "DrugKey"].dropna()
        ins_pk = 0
        if len(ins_keys):
            k = pd.DataFrame(insnorm(ins_keys.tolist()))
            ins_pk = int(k.InsulinClass.notna().sum())

        mid = pd.to_numeric(df.MedicationID, errors="coerce")
        n_dia = int(mid.isin(dia_ids).sum()) if dia_ids else 0

        gradeable = {}
        if n_dia:
            gradeable["patient_dia_hours"] = n_dia
        # Two independent paths that overlap: a consistency check, NOT accuracy.
        both = int((res.MedSource.str.startswith("fda_ndc") & res.Ingredient.notna()).sum())
        if both:
            gradeable["ndc_vs_name_overlap"] = both

        stats.append(CohortStats(
            noun="medication", cohort=coh, rows=len(df),
            patients=int(df.PatientID.nunique()),
            kinds=kind.value_counts().to_dict(),
            denominator={"resolvable": int((~never).sum()), "excluded": excluded},
            coverage={"value_written": int(res.Ingredient.notna().sum())},
            confidence=res.MedConf.value_counts().to_dict(),
            # Most- to least-trusted. GOOD is reachable only through an NDC that
            # resolved in the FDA's own file; a name match, however exact, is OK.
            confidence_order=["GOOD", "OK", "ALIAS", "WEAK", "MISS"],
            trusted=["GOOD", "OK", "ALIAS"],
            basis={str(k): int(v) for k, v in
                   res.DoseUnit.value_counts(dropna=False).items()},
            gradeable=gradeable,
            origin=ORIGIN.get(coh),
        ))
        pages[coh] = page(coh, df, res, ins_pk, n_dia)
        print(f"  {coh:<20} {len(df):>8,} rows  "
              f"{res.Ingredient.notna().mean():6.1%} named  {ins_pk:>7,} PK")

    link_reference(DEST, "medbank", BANK.parent)
    n_ex = copy_api_examples(DEST, HERE / "examples" / "api")
    write_contract(DEST)
    n_gold = write_corpus(DEST, dia)

    rep = write(
        noun="medication", emoji="💊",
        tagline=("Every cohort's medication data, in and out, on one page each.\n"
                 "describe-medication ONLY. The second half of the chain moved to\n"
                 "`_InsInfo` and took its api-examples, its DIA ruler and its B1 run\n"
                 "with it; the seam between them is measured in _InsInfo/README.md."),
        producer="Tools/plugins/haipipe-utils/skills/describe-medication/build_medinfo.py",
        rerun=("source .venv/bin/activate && source env.sh\n"
               "Tools/plugins/haipipe-utils/skills/describe-medication/run_server.sh  # another shell\n"
               "Tools/plugins/haipipe-utils/skills/describe-insulin/run_server.sh     # another shell\n"
               "python Tools/plugins/haipipe-utils/skills/describe-medication/build_medinfo.py"),
        dest=DEST, stats=stats, pages=pages,
        sections=[
            "## What is NOT in here", "",
            "```text",
            "  MedPrescription             24,705 rows   DIA per patient",
            "  MedPrescriptionDaySchedule  24,021 rows   insulin-to-carb ratio,",
            "                                            correction factor, slot times",
            "```", "",
            "Both are now cooked into a `MedRegimen` frame, and no normalizer reads",
            "them yet. They carry the only per-patient pharmacology in the whole",
            "dataset: 1,831 prescriptions state a measured duration of insulin",
            "action, and comparing it against describe-insulin's label table puts",
            "the rapid analogues 0.5 h short and regular human insulin 1.0 h long.",
        ])
    print(f"\nwrote {rep['dest']}  ·  {rep['cohorts']} cohorts  ·  "
          f"{n_ex} api examples  ·  {n_gold:,} gold rows  ·  "
          f"conforming: {not rep['problems']}")


if __name__ == "__main__":
    sys.exit(main())
