#!/usr/bin/env python3
"""Build `_InsInfo/`: what every cohort's insulin looks like, in and out.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-insulin/build_insinfo.py

WHY THIS NOUN HAS ITS OWN FOLDER
================================================================================
Until now describe-insulin had a skill, a server and a bench profile, and no
_XInfo at all -- it reported into `_MedInfo`, whose `_stats.json` carried
`noun='medication'` on all eleven rows and insulin on none. The rows that
resolve HERE and nowhere in describe-medication existed in a paragraph of
SKILL.md and in no artifact. A folder makes them countable -- and the first
count contradicted the paragraph: 5,445, not the 8,364 the skill claimed.

WHAT A SPLIT ACTUALLY COSTS, AND WHERE IT IS PAID
================================================================================
The seam. describe-medication resolves a logged row to a DrugKey and this skill
consumes that string; nobody measures a handoff that spans two folders by
accident. So README.md carries the SEAM TABLE -- per cohort, what the first half
resolved, what the second half resolved, and how many rows ONLY the second half
could reach. That table, not shared housing, is what holds the chain together.

THE ONE CIRCULARITY, NAMED RATHER THAN HIDDEN
================================================================================
`rows` here means INSULIN rows, and for the WellDoc cohorts the insulin slice is
decided by mednorm's own `IsInsulin` flag -- the thing being graded chooses its
own denominator, so an insulin it fails to recognise disappears from the
population instead of counting as a miss. Shanghai and OhioT1DM are clean: the
sheet column and the log's class word declare it independently. MEPS is clean
too (Multum's class hierarchy), which is why the identity gold lives there.
"""
import glob
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents if (a / "_WorkSpace").is_dir())
sys.path[:0] = [str(HERE), str(HERE.parent / "describe-medication")]

from insnorm import normalize as insnorm                          # noqa: E402
from insnorm.client import TRUSTED as INS_TRUSTED                 # noqa: E402
from mednorm import normalize as mednorm                          # noqa: E402

SRC = ROOT / "_WorkSpace/1-SourceStore"
DEST = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_InsInfo"

CONF_ORDER = ["GOOD", "OK", "ALIAS", "MISS"]

# How each cohort names the thing, and where in the payload it lives. The KIND
# is the dialect, and it is what decides whether the insulin slice was chosen
# independently of the resolver.
ORIGIN = {
    "WellDoc2025LLY":  ("id", "MedicationID",
                        "app MedAdministration: an integer id, insulin flagged by mednorm"),
    "WellDoc2022CGM":  ("id", "MedicationID",
                        "app MedAdministration: an integer id, insulin flagged by mednorm"),
    "WellDoc2025CVS":  ("id", "MedicationID",
                        "app MedAdministration: an integer id, insulin flagged by mednorm"),
    "WellDoc2025ALS":  ("id", "MedicationID",
                        "app MedAdministration: an integer id, insulin flagged by mednorm"),
    "WellDoc2026Libre": ("id", "MedicationID", "table present, no rows"),
    # Since 260822 the Shanghai SourceFn carries `DrugName` -- the cell's own
    # words when it has them, the COLUMN HEADER's product when the cell holds
    # only a pump rate. 2,247 of its 3,490 insulin rows were bare numbers.
    "Shanghai":        ("name_string", "DrugName",
                        "clinical sheet: the cell names the drug for injections, "
                        "the column header names it for the pump, and the column "
                        "also states the route"),
    # Since 260822 the Ohio SourceFn carries `insulin_type` from the study's own
    # patient tag, so the kind is `product` and not `class_word`. The class word
    # is still in the row and is now the DELIVERY question, not the identity one.
    "OhioT1DM":        ("product", "insulin_type",
                        "study log, pump: the patient tag names the product "
                        "(Humalog / Novalog / 'Humalog 200') and the event says "
                        "basal or bolus"),
    "CGMacros":        (None, None, "no medication table content"),
    "dubosson":        (None, None, "no medication table content"),
    "aireadi-noimage-v2": (None, None, "no medication table content"),
    "aireadi-v3":      (None, None, "no medication table content"),
}


# The route each cohort states, and where it states it. Rule 9: this is the
# CALLER's fact, handed to the door, echoed back, and it survives a bank miss.
#
#   Shanghai   the sheet COLUMN is the route -- 's.c.' / 'i.v.' / 'CSII - basal'
#              / 'CSII - bolus'. 29 of its rows are INTRAVENOUS and were
#              receiving a subcutaneous 4.5-hour curve.
#   OhioT1DM   `DeliveryMode` in the payload since 260822: entirely pump.
#   WellDoc    an integer id says nothing about a pen versus a pump. None, and
#              the door answers on the declared reference scale.
def delivery_for(cohort, declared, dm_field):
    """Both cohorts that know their route now SAY so in the payload.

    This used to re-parse Shanghai's column header here, which put the same
    rule in two places; the SourceFn is where it belongs -- rule 10, a SourceFn
    reads raw files and loses nothing. WellDoc stays None: an integer id says
    nothing about a pen versus a pump, and the door answers on its declared
    reference scale.
    """
    return dm_field if cohort in ("OhioT1DM", "Shanghai") else None


def frames():
    for p in sorted(glob.glob(str(SRC / "*" / "*" / "Medication.parquet"))):
        yield p.split("/")[-3], pd.read_parquet(p)


def resolve(cohort: str, d: pd.DataFrame) -> pd.DataFrame:
    """Run the whole chain over one cohort, deduplicating first.

    Resolving 251,293 rows one at a time answers the same 315 questions 800
    times each. The unique item is the unit of work everywhere else in this
    benchmark and it is the unit of work here too.
    """
    kind, key, _ = ORIGIN[cohort]
    m = d["medication"].dropna().map(json.loads)
    if kind == "product":
        # PREFER THE PRODUCT, FALL BACK TO THE CLASS WORD. A pump's basal is the
        # rapid analogue in its reservoir; asking with 'Basal Insulin' returned a
        # 24-hour glargine curve for 679 rows whose drug is lispro. The fallback
        # stays because a future subject may have no insulin_type.
        ident = m.map(lambda j: (str(j.get(key) or "").strip()
                                 or str(j.get("MedicationType") or "").strip() or None))
    elif kind == "id":
        ident = m.map(lambda j: None if j.get("MedicationID") is None
                      or j.get("MedicationID") != j.get("MedicationID")
                      else str(int(float(j["MedicationID"]))))
    else:
        ident = m.map(lambda j: (str(j.get(key) or "").strip() or None))
    df = pd.DataFrame({"ident": ident, "PatientID": d.loc[m.index, "PatientID"],
                       # Shanghai's Medication.parquet keeps the SHEET COLUMN in
                       # MedicationID. It is the independent insulin declaration
                       # this cohort has, and using anything else would make the
                       # README's claim of independence false.
                       "declared": d.loc[m.index, "MedicationID"].astype(str),
                       # How it entered the body. Carried so a per-cohort page can
                       # say pump_basal vs pump_bolus vs (elsewhere) mdi / iv; the
                       # record itself still has no field for it.
                       "delivery": m.map(lambda j: j.get("DeliveryMode")).values,
                       "classword": m.map(lambda j: j.get("MedicationType")).values})
    df = df[df.ident.notna()]
    if not len(df):
        return df

    # THE ROUTE IS PART OF THE QUESTION, so the cache key is (ident, route).
    # Caching on the drug alone would answer an intravenous row with the
    # subcutaneous result it had just computed for a different row.
    df["route"] = [delivery_for(cohort, dec, dm)
                   for dec, dm in zip(df.declared, df.delivery)]
    pairs = sorted(set(zip(df.ident, df.route.fillna(""))))
    idents = [a for a, _ in pairs]
    routes = [b or None for _, b in pairs]
    med = pd.DataFrame(mednorm(idents, doses=[1] * len(idents)))
    # `raw=idents`: the log's own string, beside the seam. The upstream bank
    # strips a premix ratio -- 'insulin aspart 70/30' becomes the ingredient
    # 'insulin aspart' -- and 356 Shanghai rows read `rapid` when they are
    # `premix`. The door uses the raw string ONLY when it is strictly more
    # specific, so this cannot make a disagreement worse.
    ins = pd.DataFrame(insnorm(med.DrugKey.tolist(), delivery=routes,
                               raw=idents))
    look = pd.DataFrame({
        "ident": idents, "route": [b or "" for _, b in pairs],
        "DrugKey": med.DrugKey.values, "MedConf": med.MedConf.values,
        "IsInsulin": med.IsInsulin.values,
        "InsulinClass": ins.InsulinClass.values, "PKConf": ins.PKConf.values,
        "PKBasis": ins.PKBasis.values,
    })
    df["route"] = df.route.fillna("")
    return df.merge(look, on=["ident", "route"], how="left")


def insulin_slice(cohort: str, r: pd.DataFrame) -> pd.DataFrame:
    """Which rows of this cohort ARE insulin, decided as independently as the
    cohort allows. The three criteria are not interchangeable and the README
    says which cohort gets which:

        Shanghai   the SHEET COLUMN declares it        independent
        OhioT1DM   the LOG's class word declares it    independent
        WellDoc*   mednorm's own IsInsulin flag        CIRCULAR

    An earlier version used the resolver for all three, which quietly dropped
    the Shanghai insulin NEITHER half recognised -- exactly the rows the split
    exists to count.
    """
    if not len(r):
        return r
    if cohort == "Shanghai":
        col = r.declared.str.lower()
        return r[col.str.contains("insulin") & ~col.str.contains("non-insulin")]
    if cohort == "OhioT1DM":
        # Every row of this cohort is insulin: the log records nothing else. Read
        # the CLASS WORD rather than `ident`, which is now a product name and does
        # not contain the word 'insulin'.
        return r[r.classword.astype(str).str.lower().str.contains("insulin")]
    return r[r.IsInsulin.fillna(False) | r.InsulinClass.notna()]


def stats_for(cohort: str, r: pd.DataFrame) -> dict:
    kind, _, origin = ORIGIN[cohort]
    rec = {"noun": "insulin", "cohort": cohort, "rows": 0, "origin": origin}
    if not len(r):
        return rec

    ins = insulin_slice(cohort, r)
    if not len(ins):
        return rec

    conf = ins.PKConf.fillna("MISS")
    # Rows whose ROUTE the table cannot serve -- typed, not silently dropped.
    n_route_out = int(ins.PKBasis.isin(["intravenous", "suspension"]).sum()) \
        if "PKBasis" in ins.columns else 0
    rec.update({
        "rows": int(len(ins)),
        "patients": int(ins.PatientID.nunique()),
        "kinds": {kind: int(len(ins))},
        # THE HONEST DENOMINATOR, and it stopped being 'everything' on 260822.
        # This read `excluded: {}` with the argument that unlike exercise there
        # is no shape of insulin log that is unresolvable in principle. A route
        # the PK table was never measured on is exactly that shape: an
        # intravenous dose has no subcutaneous absorption phase and a suspend
        # delivers no insulin at all, so neither has a curve to get right.
        # Counting them as misses measures the log, not the resolver.
        "denominator": {
            "resolvable": int(len(ins) - n_route_out),
            "excluded": ({"route_unsupported": int(n_route_out)}
                         if n_route_out else {}),
        },
        "coverage": {"value_written": int(ins.InsulinClass.notna().sum())},
        "confidence": {k: int(v) for k, v in conf.value_counts().items()},
        "confidence_order": CONF_ORDER,
        "trusted": list(INS_TRUSTED),
        "origin": origin,
    })
    return rec


def seam_for(cohort: str, r: pd.DataFrame) -> dict:
    """The handoff, per cohort. The one number a split folder could lose."""
    if not len(r):
        return {"cohort": cohort, "insulin_rows": 0, "med_resolved": 0,
                "ins_resolved": 0, "ins_only": 0}
    ins = insulin_slice(cohort, r)
    med_ok = ins.MedConf.isin(["GOOD", "OK", "ALIAS"])
    ins_ok = ins.PKConf.isin(list(INS_TRUSTED))
    return {"cohort": cohort, "insulin_rows": int(len(ins)),
            "med_resolved": int(med_ok.sum()), "ins_resolved": int(ins_ok.sum()),
            "ins_only": int((ins_ok & ~med_ok).sum())}


# ------------------------------------------------------------------- pages --

def write_cohort_page(cohort: str, rec: dict, seam: dict, r: pd.DataFrame):
    kind, _, origin = ORIGIN[cohort]
    L = [f"# {cohort}", "", origin, ""]
    if not rec["rows"]:
        L += ["```text", "  no insulin rows", "```", ""]
    else:
        c = rec["confidence"]
        L += ["```text",
              f"  insulin rows   {rec['rows']:>9,}",
              f"  patients       {rec['patients']:>9,}",
              f"  the row names  {kind}",
              f"  class written  {rec['coverage']['value_written']:>9,}"
              f"   {rec['coverage']['value_written'] / rec['rows']:.1%}",
              "```", "",
              "## Confidence", "",
              "```text"]
        for k in CONF_ORDER:
            if c.get(k):
                L.append(f"  {k:<8}{c[k]:>9,}")
        L += ["```", ""]

        ins = insulin_slice(cohort, r)
        if len(ins) and "route" in ins.columns and ins.route.astype(str).ne("").any():
            L += ["## How it entered the body", "",
                  "Passed to the door as `delivery` since 260822 and echoed back",
                  "as DeliveryMode. `PKBasis` is the scale the numbers are on:",
                  "an intravenous row gets NO numbers, because there is no",
                  "subcutaneous depot and a 4.5-hour curve would be wrong by an",
                  "order of magnitude.", "",
                  "```text",
                  f"  {'route':<16}{'rows':>9}   PKBasis"]
            for (dm, b), n in (ins.groupby([ins.route.replace("", "not stated"),
                                            ins.PKBasis.fillna("-")])
                               .size().sort_values(ascending=False).items()):
                L.append(f"  {str(dm):<16}{n:>9,}   {b}")
            L += ["```", ""]

        L += ["## The seam", "",
              "```text",
              f"  describe-medication resolved   {seam['med_resolved']:>9,}",
              f"  describe-insulin    resolved   {seam['ins_resolved']:>9,}",
              f"  ONLY describe-insulin reached  {seam['ins_only']:>9,}",
              "```", ""]
        if rec["rows"] and len(r):
            ins = insulin_slice(cohort, r)
            top = (ins.groupby(["ident", "DrugKey", "InsulinClass"], dropna=False)
                   .size().sort_values(ascending=False).head(10))
            L += ["## What it actually contains", "", "```text",
                  f"  {'rows':>8}  {'logged as':<26}{'DrugKey':<26}class"]
            for (i, k, cl), n in top.items():
                L.append(f"  {n:>8,}  {str(i)[:24]:<26}{str(k)[:24]:<26}{cl}")
            L += ["```", ""]
    L += ["GENERATED. Do not hand-edit. Producer under git at",
          "`Tools/plugins/haipipe-utils/skills/describe-insulin/build_insinfo.py`.", ""]
    (DEST / "1-per-cohort" / f"{cohort}.md").write_text("\n".join(L))


def write_readme(stats, seams):
    live = [s for s in stats if s["rows"]]
    tot_rows = sum(s["rows"] for s in live)
    tot_w = sum(s["coverage"]["value_written"] for s in live)

    w = "{:<22}{:>9}{:>10}{:>10}{:>9}"
    tbl = [w.format("cohort", "ins rows", "patients", "class", "of rows"),
           "-" * 60]
    for s in sorted(live, key=lambda x: -x["rows"]):
        tbl.append(w.format(s["cohort"], f"{s['rows']:,}", f"{s['patients']:,}",
                            f"{s['coverage']['value_written']:,}",
                            f"{s['coverage']['value_written'] / s['rows']:.1%}"))
    tbl += ["-" * 60,
            w.format("TOTAL", f"{tot_rows:,}", "", f"{tot_w:,}",
                     f"{tot_w / max(tot_rows, 1):.1%}")]

    sw = "{:<22}{:>11}{:>11}{:>11}{:>13}"
    seam = [sw.format("cohort", "ins rows", "med res.", "ins res.", "ONLY ins"),
            "-" * 68]
    for s in sorted(seams, key=lambda x: -x["insulin_rows"]):
        if not s["insulin_rows"]:
            continue
        seam.append(sw.format(s["cohort"], f"{s['insulin_rows']:,}",
                              f"{s['med_resolved']:,}", f"{s['ins_resolved']:,}",
                              f"{s['ins_only']:,}"))
    only = sum(s["ins_only"] for s in seams)
    seam += ["-" * 68, sw.format("TOTAL", "", "", "", f"{only:,}")]

    empty = [s for s in stats if not s["rows"]]

    (DEST / "README.md").write_text("\n".join([
        "# 💉 _InsulinInfo", "",
        "Every cohort's INSULIN, in and out, on one page each. Sibling of",
        "`_MedInfo`, and the second half of a chain with it.", "",
        "GENERATED. Do not hand-edit. The producer is under git at",
        "`Tools/plugins/haipipe-utils/skills/describe-insulin/build_insinfo.py`.", "",
        "```bash",
        "source .venv/bin/activate && source env.sh",
        "python Tools/plugins/haipipe-utils/skills/describe-insulin/build_insinfo.py",
        "```", "",
        "", "## Read this table first", "",
        "`class` is how often a curve was actually written. Unlike medication",
        "there is no unresolvable shape of log here, so the denominator is the",
        "insulin population itself.", "",
        "```text", *tbl, "```", "",
        "", "## The seam", "",
        "This is the table a split folder could have lost, and the reason the",
        "two skills are two skills. `ONLY ins` counts rows describe-medication",
        "could not resolve at all and describe-insulin could.", "",
        "```text",
        "   raw row --> describe-medication --> DrugKey --> describe-insulin",
        "                                       'insulin lispro'",
        "                                       'Novolin R'",
        "                                       'basal insulin'",
        "```", "",
        "```text", *seam, "```", "",
        "", "## What decides an insulin row, and where that is circular", "",
        "```text",
        "  Shanghai     the SHEET COLUMN says 'Insulin dose - s.c.'    independent",
        "  OhioT1DM     the LOG says 'Basal Insulin'                   independent",
        "  MEPS         Multum's class hierarchy, TC1S1_1 == 215       independent",
        "  WellDoc*     mednorm's own IsInsulin flag                   CIRCULAR",
        "",
        "  On the WellDoc cohorts the thing being graded chooses its own",
        "  denominator: an insulin it fails to recognise leaves the population",
        "  instead of counting as a miss. That is why the identity gold lives on",
        "  MEPS, where an outside organisation drew the line.",
        "```", "",
        "", "## Layers", "",
        "```text",
        "  1-per-cohort     one page per cohort: what goes in, and what comes out",
        "  2-corpus         the gradeable subset, its gold, one folder per corpus",
        "  3-reference      where the PK table's numbers come from",
        "  4-contract       the record's JSON Schema and worked specimens",
        "  5-api-examples   real request/response pairs against the running service",
        "  6-benchmark      the readings: CONTRACT.md (B1), GOLD.md (B2)",
        "```", "",
        "", "## Cohorts with no insulin", "",
        "```text",
        *[f"  {s['cohort']:<22}{s['origin']}" for s in empty],
        "```", ""]))


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "1-per-cohort").mkdir(exist_ok=True)

    stats, seams = [], []
    for cohort, d in frames():
        if cohort not in ORIGIN:
            continue
        r = resolve(cohort, d) if len(d) else pd.DataFrame()
        rec, sm = stats_for(cohort, r), seam_for(cohort, r)
        stats.append(rec)
        seams.append(sm)
        write_cohort_page(cohort, rec, sm, r)
        print(f"  {cohort:<22} insulin rows {rec['rows']:>8,}  "
              f"class {rec.get('coverage', {}).get('value_written', 0):>8,}  "
              f"only-ins {sm['ins_only']:>6,}")

    (DEST / "_stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    (DEST / "_seam.json").write_text(json.dumps(seams, indent=1) + "\n")
    write_readme(stats, seams)
    print(f"\nwrote {DEST}  ·  {len([s for s in stats if s['rows']])} cohorts with insulin")


if __name__ == "__main__":
    main()
