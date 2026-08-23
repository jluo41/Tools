#!/usr/bin/env python3
"""Freeze the two medication golds into `_MedInfo/2-corpus/`.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-medication/benchmark/build_gold.py

A corpus that moves when the code moves grades nothing, so this writes the
RULER and never a score. Grading is run_bench.py, and it writes next door into
6-benchmark/runs/.

THE UNIT OF EVALUATION IS THE DISTINCT STRING, AND THE SAMPLING IS ROW-UNIFORM
================================================================================
Both weightings are frozen with the gold, because they answer different
questions and disagree:

    row_weight   how many real fills / administrations carry this string.
                 Sampling rows uniformly gives probability-proportional-to-size
                 over strings for free, which is the principled design (Binette
                 et al. 2024) and also the DEPLOYMENT question: what patients
                 actually take.
    type weight  every distinct string once. The VOCABULARY question, where the
                 long tail dominates.

Freezing the weight, not the sample, means a later run may draw any n and still
estimate the same population.
"""
import json
import pathlib
import re
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
# Find the workspace by its marker, not by counting directories. A count is
# right until someone moves the skill one level, and then it silently reads a
# path that does not exist rather than failing where the mistake is.
ROOT = next(a for a in HERE.parents if (a / "_WorkSpace").is_dir())
sys.path[:0] = [str(HERE), str(HERE.parent)]

import build_units as U                                          # noqa: E402
import drugname as D                                             # noqa: E402

MEPS = ROOT / "_WorkSpace/ExternalStore/meps/meps_h248a_rx.parquet"
LEXICON = ROOT / "_WorkSpace/ExternalStore/medbank/med_lexicon.parquet"

# ONE FOLDER PER CORPUS, NAMED AFTER THE CORPUS. A reader who opens 2-corpus
# should see where each ruler came from without opening a parquet, and a
# corpus with no gold yet still gets a folder -- see build_units.py for why
# that is not an empty gesture. The file name inside is the evaluation set, so
# one source feeding three sets reads as three files under one name.
CORPUS = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo/2-corpus"
DEST = {"MEPS": CORPUS / "MEPS", "WellDoc": CORPUS / "WellDoc"}

# MEPS writes missing as a negative integer, never as a blank. Treating -15 as
# a drug name is how a sentinel becomes a measurement.
MEPS_MISSING = re.compile(r"^\s*-\d+\s*$")

# WellDoc writes a product name in TWO shapes, and assuming only the first one
# was a defect in this file, not in the resolver:
#
#     losartan (COZAAR) 50 mg oral tablet          brand in the middle
#     metFORMIN HCl 1000 MG Oral Tablet (Glucophage)   brand at the end
#
# Taking "everything before the parenthesis" gives `metFORMIN HCl 1000 MG Oral
# Tablet` for the second, and then a correct answer of `metformin
# hydrochloride` scores as WRONG. The generic is the text before whichever
# comes FIRST: the parenthesis, or the strength.
LEX_BRAND = re.compile(r"\(([^)]+)\)")
LEX_STRENGTH = re.compile(r"\d")


def _blank(s) -> bool:
    s = str(s or "").strip()
    return (not s) or s.lower() in ("nan", "none") or bool(MEPS_MISSING.match(s))


# ------------------------------------------------------------------ E1 MEPS --

def build_meps() -> pd.DataFrame:
    d = pd.read_parquet(MEPS)
    d = d[~d.RXNAME.map(_blank) & ~d.RXDRGNAM.map(_blank)].copy()
    d["ndc9"] = d.RXNDC.map(lambda x: "" if _blank(x) else D.ndc9(x))

    rows = []
    for name, g in d.groupby("RXNAME", sort=True):
        golds = g.RXDRGNAM.value_counts()
        ndcs = sorted({n for n in g.ndc9 if len(n) == 9})
        tc = g.TC1[~g.TC1.map(_blank)]
        rows.append({
            "unit": name,
            "row_weight": len(g),
            "gold_ingredient": golds.index[0],
            # A pharmacy string that maps to more than one Multum name is
            # AMBIGUOUS, not wrong. It is kept and flagged, never dropped:
            # 'VITAMIN D' really is two molecules in the wild.
            "gold_ingredient_alts": list(golds.index[1:]) if len(golds) > 1 else [],
            "gold_ambiguous": len(golds) > 1,
            "gold_ndc9": ndcs,
            "n_gold_ndc9": len(ndcs),
            "gold_class_tc1": int(tc.iloc[0]) if len(tc) else None,
            "name_equals_gold": D.same(name, golds.index[0]),
        })
    out = pd.DataFrame(rows).sort_values("row_weight", ascending=False)
    out["corpus"] = "MEPS"
    out["set"] = "E1_ALL"
    out["gold_tier"] = "G2"          # declared by an independent source
    out["gold_source"] = "MEPS HC-248A 2023 / Multum Lexicon"
    return out.reset_index(drop=True)


# --------------------------------------------------------------- E2 LEXICON --

def build_lexicon() -> pd.DataFrame:
    # THE WEIGHT IS ADMINISTRATION VOLUME, NOT THE LEXICON'S OWN RawRows.
    # RawRows is a count from the lexicon build; it totals 7,910 against
    # 386,373 real administrations and it RANKS DIFFERENTLY. MedicationID
    # 612997 -- Lyumjev, the most-administered product in the dataset at
    # 110,654 rows -- carries RawRows=1, while a cephalexin nobody took carries
    # 89. A 'row-weighted' number computed on that describes no population.
    # Measured: it understated E2's row-weighted exact by 10.1 points
    # (87.1% -> 97.2%). RawRows is KEPT as its own column, because the old
    # number has to stay reproducible for anyone reading an earlier run.
    admin = U.welldoc_admin_counts()
    d = pd.read_parquet(LEXICON)
    rows = []
    for r in d.itertuples():
        nm = str(r.MedicationName or "")
        b = LEX_BRAND.search(nm)
        s = LEX_STRENGTH.search(nm)
        cut = min([x.start() for x in (b, s) if x] or [len(nm)])
        generic = nm[:cut].strip(" ,-")
        # A name is parseable when it HAS a brand or a strength to cut at and
        # something is left in front. `SANTYL OINTMENT` and `Keppra 500 MG` are
        # a brand with no generic; they get no gold and go to the human stratum.
        ok = bool(generic) and (b is not None or s is not None) and len(generic) > 2
        uid = str(r.MedicationID)
        rows.append({
            "unit": uid,
            "unit_text": nm,
            "row_weight": int(admin.get(uid, {}).get("n", 0)),
            "n_patients": len(admin.get(uid, {}).get("pts", ())),
            "lexicon_rawrows": int(r.RawRows or 0),
            "gold_ingredient": generic if ok else None,
            "gold_brand": b.group(1).strip() if b else None,
            "gold_ndc9": [D.ndc9(r.NDC)] if not _blank(r.NDC) else [],
            "parseable": ok,
        })
    out = pd.DataFrame(rows)
    out["corpus"] = "WellDoc"
    out["set"] = "E2_LEXICON"
    # The 202 unparseable names are NOT dropped -- rule 2, TYPE DO NOT DELETE.
    # They are the stratum a person must label, and hiding them would make the
    # corpus look like coverage it does not have.
    out["gold_tier"] = out.parseable.map({True: "G2", False: "UNLABELLED"})
    out["gold_source"] = "WellDoc MedicationID export, name parsed"
    return out.sort_values("row_weight", ascending=False).reset_index(drop=True)


def main():
    for d in DEST.values():
        d.mkdir(parents=True, exist_ok=True)
    e1, e2 = build_meps(), build_lexicon()

    e1.to_parquet(DEST["MEPS"] / "E1_ALL.parquet", index=False)
    e2.to_parquet(DEST["WellDoc"] / "E2_LEXICON.parquet", index=False)

    summary = {
        "E1_ALL": {
            "gold_tier": "G2 -- declared by an independent source (Multum)",
            "units": len(e1),
            "rows": int(e1.row_weight.sum()),
            "ambiguous_units": int(e1.gold_ambiguous.sum()),
            "units_where_string_already_equals_gold": int(e1.name_equals_gold.sum()),
            "units_needing_real_resolution": int((~e1.name_equals_gold).sum()),
            "rows_needing_real_resolution": int(e1.loc[~e1.name_equals_gold, "row_weight"].sum()),
            "units_with_a_gold_ndc": int((e1.n_gold_ndc9 > 0).sum()),
            "median_ndc_per_unit": float(e1.n_gold_ndc9.median()),
        },
        "E2_LEXICON": {
            "gold_tier": "G2 parseable / UNLABELLED otherwise",
            "units": len(e2),
            "rows": int(e2.row_weight.sum()),
            "parseable": int(e2.parseable.sum()),
            "unparseable_needing_human_labels": int((~e2.parseable).sum()),
            "rows_covered_by_parseable": float(
                e2.loc[e2.parseable, "row_weight"].sum() / max(e2.row_weight.sum(), 1)),
        },
    }
    (CORPUS / "_gold_summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))
    for d in DEST.values():
        print(f"wrote {d}")


if __name__ == "__main__":
    main()
