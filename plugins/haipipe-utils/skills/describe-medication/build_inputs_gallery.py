#!/usr/bin/env python3
"""
Build `_MedInfo/0-inputs/`: one specimen of every SHAPE that can arrive.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-medication/build_inputs_gallery.py

The engine is haipipe-norm/inputs_gallery.py, shared by all four nouns. This
file holds only the list of shapes, because the list is the part that differs:
medication arrives as a pharmacy catalogue string keyed by an internal id.

This noun counts DISTINCT STRINGS, not rows: its corpus is a weighted unit list,
so a share here is a share of the vocabulary a resolver must cover.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents
            if (a / "pyproject.toml").exists() and (a / "code").is_dir())
SKILLS = ROOT / "Tools/plugins/haipipe-utils/skills"
sys.path[:0] = [str(HERE), str(SKILLS / "haipipe-norm")]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo"

import pandas as pd                                       # noqa: E402
from inputs_gallery import (Shape, build, ABSENT, CALL,
                            CONTRACT, DEPLOYMENT)     # noqa: E402
from mednorm import normalize                             # noqa: E402


def sample_meps(n=2):
    """Real MEPS units, the ones patients actually reported, most-weighted first."""
    def take(c):
        d = c["meps"].nlargest(n, "row_weight")
        prov = ("Real rows from MEPS/E1_ALL. "
                + " · ".join(f"{r.unit!r} (weight {r.row_weight:,.0f}, gold "
                             f"{r.gold_ingredient!r})" for r in d.itertuples()) + ".")
        return {"items": list(d.unit.astype(str))}, prov
    return take


def sample_welldoc(n=2):
    """Real WellDoc MedicationIDs, most-prescribed first, with the text they map to."""
    def take(c):
        d = c["wd"].nlargest(n, "row_weight")
        prov = ("Real rows from WellDoc/E2_LEXICON. "
                + " · ".join(f"{r.unit!r} carries {r.n_patients:,.0f} patients and "
                             f"unwraps to {str(r.unit_text)[:56]!r}" for r in d.itertuples()) + ".")
        return {"items": list(d.unit.astype(str))}, prov
    return take


def sample_dose(n=2):
    """Real WellDoc catalogue strings that state a dose."""
    def take(c):
        d = c["wd"]
        hit = d[d.unit_text.astype(str).str.contains(r"\d+\s*(?:MG|mg|unit)", na=False)]
        hit = hit.nlargest(n, "row_weight")
        prov = ("Real strings from WellDoc/E2_LEXICON, chosen because they state a "
                "dose. " + " · ".join(f"{str(r.unit_text)[:60]!r}" for r in hit.itertuples()) + ".")
        return {"items": [str(x) for x in hit.unit_text]}, prov
    return take


def call(req):
    return normalize(req["items"])


def sources(c):
    """These corpora are already deduplicated: one row IS one writing, and the
    repeats live in row_weight. So `rows` here is the real record count that
    weight represents, and `writings` is the table length."""
    rows = []
    for name, d, what in [
            ("MEPS/E1_ALL", c["meps"], "survey answers, plain ingredient names"),
            ("WellDoc/E2_LEXICON", c["wd"], "pharmacy catalogue strings, keyed by an internal id")]:
        w = int(d.row_weight.sum()); u = len(d)
        top10 = d.row_weight.nlargest(10).sum() / d.row_weight.sum()
        rows.append((name, f"{w:,}", f"{u:,}", f"{w/u:.0f}x",
                     f"{what}; top 10 cover {top10:.0%}"))
    tw = int(c["meps"].row_weight.sum() + c["wd"].row_weight.sum())
    tu = len(c["meps"]) + len(c["wd"])
    rows.append(("ALL", f"**{tw:,}**", f"**{tu:,}**", f"**{tw/tu:.0f}x**",
                 "no writing appears twice: the corpus is already merged"))
    note = ("Medication's corpus is stored merged, so the repeat column comes from "
            "`row_weight` rather than from counting rows. WellDoc is the more skewed "
            "of the two: ten ids carry three quarters of its records, and all ten are "
            "insulin pens.")
    return rows, note


SHAPES = [
    Shape("01-plain-text", "an ingredient name",
          "The shape MEPS is written in, and the only one where the string "
          "itself names the drug. 1,447 of the corpus's units.",
          {"items": ["METFORMIN", "ATORVASTATIN"]},
          lambda c: int(c["meps_units"]), sample=sample_meps(),
          see="5-api-examples/3-ladder/generic-ok"),
    Shape("02-decorated-text", "a name with something else stuck to it",
          "What a real free-text box produces. Not on this board: every string "
          "here came from a catalogue or a survey, never from a patient typing.",
          {"items": ["metformin, taken at breakfast", "metformin (generic)"]},
          ABSENT),
    Shape("03-text-with-dose", "a drug and how much of it",
          "The shape the dose lane needs. C04 of the B1 contract is currently "
          "FAILING on this noun: the dose is stated and does not survive.",
          {"items": ["metformin 500 mg"]},
          lambda c: 0, sample=sample_dose(), see="5-api-examples/2-dose/tablet-count"),
    Shape("04-vendor-id", "an internal id, not a name",
          "WellDoc stores a MedicationID and keeps the text in a side table. "
          "The door resolves these today WITHOUT being told they are ids, which "
          "is why a resolved name and a looked-up id are indistinguishable in "
          "the output.",
          {"items": ["612997", "241223"]},
          lambda c: int(c["welldoc_units"]), sample=sample_welldoc(),
          see="5-api-examples/1-dialects/welldoc-id",
          layer=DEPLOYMENT,
          unwraps_to="`01-plain-text` via E2_LEXICON, which covers 337,565 of "
                     "386,373 WellDoc rows (87.4%). 612997 becomes "
                     "'insulin lispro-aabc (LYUMJEV TEMPO PEN,U-100,INSULN)'."),
    Shape("05-several-in-one", "several drugs in one string",
          "Shanghai writes a regimen as one field. One string, several drugs, "
          "each with its own dose.",
          {"items": ["二甲双胍 0.5g; 格列美脲 2mg"]}, ABSENT,
          see="5-api-examples/1-dialects/shanghai-multidrug"),
    Shape("06-named-nothing", "a string that names no drug",
          "Returning an ingredient for these would be inventing one.",
          {"items": ["Unknown", "99999999"]}, ABSENT),
    Shape("07-batch", "several at once, mixed shapes",
          "A call shape rather than a row shape.",
          {"items": ["METFORMIN", "612997", "Unknown", "metformin 500 mg"]},
          CALL),
]

if __name__ == "__main__":
    meps = pd.read_parquet(INFO / "2-corpus/MEPS/E1_ALL.parquet")
    wd = pd.read_parquet(INFO / "2-corpus/WellDoc/E2_LEXICON.parquet")
    c = {"meps_units": len(meps), "welldoc_units": len(wd), "meps": meps, "wd": wd}
    out = build("medication", INFO, SHAPES, call,
                keep=["MedConf", "MedSource", "Ingredient", "DrugKey",
                      "DoseValue", "DoseUnit", "DoseBasis", "NDC"],
                corpus=c, total=len(meps) + len(wd), sources=sources,
                verdict=lambda a: f"`{a.get('MedConf')}`"
                + (f" {a['Ingredient'][:18]}" if a.get("Ingredient") else ""))
    print(f"wrote {out}")
