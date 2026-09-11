#!/usr/bin/env python3
"""
Build `_InsInfo/0-inputs/`: one specimen of every SHAPE that can arrive.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-insulin/build_inputs_gallery.py

The engine is haipipe-norm/inputs_gallery.py, shared by all four nouns. This
file holds only the list of shapes, because the list is the part that differs:
insulin is not a table of its own. It hides inside Medication, and each cohort
buries it differently: OhioT1DM in a JSON record with the name inside, WellDoc in
a JSON record with only an id, Shanghai in a clinician's phrase. Only MEPS writes
a plain product name -- and MEPS is the only shape the corpus contains.

This noun counts DISTINCT STRINGS, not rows: its corpus is a weighted unit list,
so a share here is a share of the vocabulary a resolver must cover.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents
            if (a / "pyproject.toml").exists() and (a / "code").is_dir())
SKILLS = ROOT / "Tools/plugins/haipipe-utils/skills"
sys.path[:0] = [str(HERE), str(SKILLS / "haipipe-norm"), str(SKILLS / "describe-medication")]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_InsInfo"

import pandas as pd                                       # noqa: E402
from inputs_gallery import (Shape, build, ABSENT, CALL,
                            CONTRACT, DEPLOYMENT)     # noqa: E402
from insnorm import normalize                             # noqa: E402


def sample_meps(n=3):
    def take(c):
        d = c["meps"].nlargest(n, "row_weight")
        prov = ("Real units from MEPS/I1_IDENTITY. "
                + " · ".join(f"{r.unit!r} (weight {r.row_weight:,.0f})"
                             for r in d.itertuples()) + ".")
        return {"items": list(d.unit.astype(str))}, prov
    return take


def sample_literal(key, note):
    """A real row copied off 1-SourceStore, verbatim, plus what it unwraps to."""
    def take(c):
        return {"items": c[key]}, note + " Copied verbatim from 1-SourceStore."
    return take


def call(req):
    return normalize(req["items"])


def sources(c):
    """Insulin has no table of its own: every source buries it in Medication a
    different way, so `writings` means something different in each row."""
    m = c["meps"]
    rows = [
        ("MEPS/I1_IDENTITY", f"{int(m.row_weight.sum()):,}", f"{len(m):,}",
         f"{m.row_weight.sum()/len(m):.0f}x",
         "plain product names; the ONLY source in the graded corpus"),
        ("WellDoc Medication", f"{c['welldoc_rows']:,}", "871 ids", "-",
         "a JSON record carrying only a MedicationID"),
        ("Shanghai Medication", f"{c['shanghai_rows']:,}", "5 phrases", "-",
         "a clinician's phrase: `CSII - basal insulin (Novolin R, IU / H)`"),
        ("OhioT1DM Medication", f"{c['ohio_rows']:,}", "3 names", "-",
         "a JSON record with `insulin_type` inside, spelled `Novalog`"),
    ]
    note = ("Only the first row is in the graded corpus. The other three are 99.97% "
            "of the real records and none of them has been benchmarked, which is why "
            "insulin's 12/12 contract pass is a statement about 38 strings.")
    return rows, note


SHAPES = [
    Shape("01-plain-text", "a product name",
          "The shape MEPS is written in, and THE ONLY SHAPE THIS NOUN'S CORPUS "
          "CONTAINS. 38 units is the entire vocabulary describe-insulin has ever "
          "been graded on. Every shape below is one insulin actually arrives in "
          "and is not graded against.",
          {"items": ["LANTUS", "NOVOLOG", "LEVEMIR"]},
          lambda c: int(c["meps_units"]), sample=sample_meps(),
          see="5-api-examples/1-class"),
    Shape("02-json-with-name", "a JSON blob with the drug name inside",
          "OhioT1DM does not store a string, it stores a record. The name is a "
          "field in it, and it is MISSPELLED: 'Novalog' for Novolog, 1,881 rows "
          "of it. A caller handed this blob whole gets nothing.",
          {"items": ['{\"Dose\": 1.0, \"MedicationType\": \"Basal Insulin\", '
                     '\"insulin_type\": \"Novalog\", \"DeliveryMode\": \"pump_basal\"}',
                     "Novalog"]},
          lambda c: int(c["ohio_rows"]), sample=sample_literal("ohio_items", "Real OhioT1DM rows."), layer=DEPLOYMENT, unwraps_to=
          "`01-plain-text` by reading the `insulin_type` field out of the record. "
          "Handed the blob WHOLE, the door reads the words 'Basal Insulin' from a "
          "different field and answers long-acting, 1440 min, with PKConf OK -- "
          "for an insulin that is rapid and lasts 270. Unwrapping is not optional."),
    Shape("03-json-with-id", "a JSON blob with an internal id inside",
          "WellDoc's shape, and the largest of the four by two orders of "
          "magnitude. The name is not in the record at all: MedicationID points "
          "at a side table. Dose 255 is a sentinel, not a dose.",
          {"items": ['{\"MedicationID\": 612997.0, \"Dose\": 6.0, '
                     '\"MedSourceID\": 1.0}',
                     "612997",
                     "insulin lispro-aabc (LYUMJEV TEMPO PEN,U-100,INSULN) 100 unit/mL"]},
          lambda c: int(c["welldoc_rows"]), sample=sample_literal("wd_items", "Real WellDoc rows."), layer=DEPLOYMENT, unwraps_to=
          "`01-plain-text` via E2_LEXICON, which covers 87.4% of WellDoc rows. "
          "The three items below are the SAME prescription in three forms: the "
          "record, its bare id, and what the id unwraps to. Only the third one "
          "answers. (777777 with Dose 255, which an earlier draft used here, is "
          "a sentinel and is in no lexicon at all.)"),
    Shape("04-clinical-phrase", "a clinician's phrase, not a product",
          "Shanghai writes the route and the regimen, with the product in "
          "brackets. Five phrases cover the cohort. 'Insulin dose - s.c.' names "
          "no product at all.",
          {"items": ["CSII - basal insulin (Novolin R, IU / H)",
                     "CSII - bolus insulin (Novolin R, IU)",
                     "Insulin dose - s.c."]},
          lambda c: int(c["shanghai_rows"])),
    Shape("05-brand-with-generic", "brand name carrying its generic in brackets",
          "How MetaboNet's 13 source studies write insulin, and a convention "
          "this board has never seen. It carries real noise: 'Apidra (Glusine)' "
          "is Glulisine misspelled, and two names can share one field.",
          {"items": ["Humalog (Lispro)", "Apidra (Glusine)",
                     "Humalog (Lispro) or Novolog (Aspart)", "Regular insulin"]},
          ABSENT),
    Shape("06-text-with-dose", "a product and how many units",
          "Insulin's dose is units, not milligrams, and its basis is the "
          "injection rather than the day.",
          {"items": ["Lantus 20 units", "Humalog 6u"]}, ABSENT,
          see="5-api-examples/3-patient"),
    Shape("07-named-nothing", "a string that names no insulin",
          "Including a real drug that is not an insulin: saying so is the "
          "answer, and it is the chain's job to say it.",
          {"items": ["Unknown", "METFORMIN"]}, ABSENT,
          see="5-api-examples/2-chain/not-insulin"),
    Shape("08-batch", "several at once, mixed shapes",
          "A call shape rather than a row shape.",
          {"items": ["LANTUS", "Novalog", "553838", "Humalog (Lispro)"]}, CALL),
]

if __name__ == "__main__":
    # Counts come from 1-SourceStore, the real input, NOT from the benchmark
    # corpus. I3a_DIA's `unit` is MedPrescriptionID: it grades duration of
    # action, one prescription at a time, and is not a vocabulary at all.
    import glob, json
    meps = pd.read_parquet(INFO / "2-corpus/MEPS/I1_IDENTITY.parquet")
    src = ROOT / "_WorkSpace/1-SourceStore"
    ohio = 0
    for f in glob.glob(str(src / "OhioT1DM/@*/Medication.parquet")):
        for v in pd.read_parquet(f)["medication"].astype(str):
            try:
                ohio += 1 if json.loads(v).get("insulin_type") else 0
            except Exception:
                pass
    welldoc = sum(len(pd.read_parquet(f, columns=["medication"]))
                  for f in glob.glob(str(src / "WellDoc*/@*/Medication.parquet")))
    sh = 0
    for f in glob.glob(str(src / "Shanghai/@*/Medication.parquet")):
        s_ = pd.read_parquet(f)["MedicationID"].astype(str)
        sh += int(s_.str.contains("insulin", case=False, na=False).sum())
    # real specimens, taken verbatim off 1-SourceStore
    ohio_items = []
    for f in glob.glob(str(src / "OhioT1DM/@*/Medication.parquet")):
        vc = pd.read_parquet(f)["medication"].astype(str).value_counts()
        ohio_items = [str(vc.index[0])]
        try:
            ohio_items.append(str(json.loads(vc.index[0])["insulin_type"]))
        except Exception:
            pass
        break
    wd_items = []
    for f in glob.glob(str(src / "WellDoc2025LLY/@*/Medication.parquet")):
        d_ = pd.read_parquet(f, columns=["MedicationID", "medication"])
        top = int(d_.MedicationID.dropna().astype(int).value_counts().index[0])
        wd_items = [str(d_[d_.MedicationID == top]["medication"].iloc[0]), str(top)]
        lex = pd.read_parquet(INFO.parent / "_MedInfo/2-corpus/WellDoc/E2_LEXICON.parquet")
        hit = lex[lex.unit.astype(int) == top]
        if len(hit):
            wd_items.append(str(hit.unit_text.iloc[0]))
        break
    sh_items = []
    for f in glob.glob(str(src / "Shanghai/@*/Medication.parquet")):
        s_ = pd.read_parquet(f)["MedicationID"].astype(str)
        sh_items = list(s_[s_.str.contains("insulin", case=False, na=False)]
                        .value_counts().head(3).index)
        break
    c = {"meps_units": len(meps), "ohio_rows": ohio,
         "welldoc_rows": welldoc, "shanghai_rows": sh, "meps": meps,
         "ohio_items": ohio_items, "wd_items": wd_items, "sh_items": sh_items}
    out = build("insulin", INFO, SHAPES, call,
                # The real column names. InsulinConf/InsulinSource do not exist
                # on this door; asking for them printed nulls and hid the fact
                # that a blob came back with PKConf: OK.
                keep=["InsulinResolved", "InsulinClass", "OnsetMin", "PeakMin",
                      "DurationMin", "PKBasis", "PKSource", "PKConf"],
                corpus=c,
                # name the four counts; c also carries the frames the
                # samplers read, which are not summable
                total=(c["meps_units"] + c["ohio_rows"]
                       + c["welldoc_rows"] + c["shanghai_rows"]),
                sources=sources,
                verdict=lambda a: f"`{a.get('PKConf') or 'MISS'}`"
                + (f" {a['InsulinResolved']}" if a.get("InsulinResolved") else "")
                + (f" {a['DurationMin']}min" if a.get("DurationMin") else ""))
    print(f"wrote {out}")
