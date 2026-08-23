#!/usr/bin/env python3
"""Freeze `_InsInfo/2-corpus/<Corpus>/` -- the insulin slice of every corpus.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-insulin/benchmark/build_units.py

SAME LAYOUT AS _MedInfo, DIFFERENT SLICE. One folder per corpus, named after
the corpus; `units.parquet` always; a `<SET_ID>.parquet` only where a ruler
exists. This is not a copy of medication's inventory: 1,550 MEPS strings become
38, and the 38 are almost all BRAND names, which is the hardest thing the FDA
NDC Directory cannot do and the reason the identity gold belongs here.

WHAT DECIDES THE SLICE, AND WHERE THAT IS CIRCULAR
================================================================================
    MEPS        Multum's class hierarchy, TC1S1_1 == 215     independent
    Shanghai    the sheet COLUMN says 'Insulin dose - s.c.'  independent
    OhioT1DM    the log's class word                         independent
    WellDoc     mednorm's own IsInsulin flag                 CIRCULAR

Only the independent three can carry a gold that means anything, and of those
only MEPS names a PRODUCT. That is the whole argument for I1 living on MEPS.
"""
import glob
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents if (a / "_WorkSpace").is_dir())
SKILLS = HERE.parent.parent
sys.path[:0] = [str(HERE.parent), str(SKILLS / "describe-medication")]

from insnorm import normalize as insnorm                          # noqa: E402
from mednorm import normalize as mednorm                          # noqa: E402

SRC = ROOT / "_WorkSpace/1-SourceStore"
RX = ROOT / "_WorkSpace/0-RawDataStore"
MEPS = ROOT / "_WorkSpace/ExternalStore/meps/meps_h248a_rx.parquet"
DEST = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_InsInfo/2-corpus"

MULTUM_INSULIN = 215        # TC1S1_1, Multum's insulin subclass under antidiabetics

COLUMNS = ["corpus", "unit", "unit_key", "unit_kind", "unit_text",
           "row_weight", "n_patients",
           "pred_drugkey", "pred_class", "pred_conf", "pred_basis", "resolved",
           "has_gold", "gold_set"]

NOTE = {
    "MEPS": (
        "The insulin slice of MEPS HC-248A 2023, drawn by MULTUM's class\n"
        "hierarchy (TC1S1_1 == 215) and not by anything of ours.\n\n"
        "38 distinct pharmacy strings, 3,507 fills, and 7 gold molecules. The\n"
        "strings are overwhelmingly BRANDS -- LANTUS, NOVOLOG, LEVEMIR,\n"
        "TRESIBA, HUMALOG, TOUJEO, BASAGLAR, ADMELOG, SEMGLEE, FIASP, LYUMJEV\n"
        "-- and the FDA NDC Directory has no brand-to-generic edge at all. This\n"
        "is the only corpus here that both names a product AND carries an\n"
        "outside answer for it, so it is where an identity gold can live.\n\n"
        "I1_IDENTITY.parquet is graded by benchmark/run_bench.py; the reading\n"
        "lands in 6-benchmark/GOLD.md."),
    "WellDoc": (
        "The insulin MedicationIDs of the four WellDoc cohorts pooled.\n\n"
        "CIRCULAR SLICE. Membership is mednorm's own `IsInsulin`, so an insulin\n"
        "it fails to recognise leaves the population rather than counting as a\n"
        "miss. Coverage measured here is an upper bound, and the identity gold\n"
        "deliberately lives on MEPS instead.\n\n"
        "I3a_DIA.parquet is the one ruler here and it is the only number in\n"
        "this noun measured on an actual person: a duration of insulin action\n"
        "the PRESCRIBER recorded, 1,831 prescriptions. Its unit is a\n"
        "PRESCRIPTION, not a drug, so it does not join to this inventory."),
    "Shanghai": (
        "Insulin rows drawn by the SHEET COLUMN -- 'Insulin dose - s.c.',\n"
        "'Insulin dose - i.v.', 'CSII - basal insulin', 'CSII - bolus insulin'\n"
        "-- and never by our own output. 'Non-insulin hypoglycemic agents' is\n"
        "the one column excluded.\n\n"
        "THIS IS THE BIGGEST UNMEASURED HOLE IN THE NOUN. The column declares\n"
        "3,490 insulin rows and only a third of them get a curve, because the\n"
        "products are Chinese-market ones the FDA Directory does not list. No\n"
        "gold exists, so we know the coverage and nothing about correctness."),
    "OhioT1DM": (
        "The study's own XML names the PRODUCT per subject, on the patient tag:\n"
        "`<patient id=\"591\" weight=\"99\" insulin_type=\"Novalog\">`. All 12\n"
        "subjects have one -- Humalog, Novalog, 'Humalog 200'.\n\n"
        "UNTIL 260822 THE INGEST DROPPED IT and this note said an identity gold\n"
        "was impossible here. It was not; the attribute was one field away. The\n"
        "SourceFn now carries `insulin_type` and `DeliveryMode`, and the unit of\n"
        "this corpus is the product.\n\n"
        "WHAT THAT FIXED. These subjects are on PUMPS -- the XML proves it with\n"
        "<temp_basal> spans and bolus-wizard types, no outside knowledge needed.\n"
        "In CSII there is ONE reservoir: the basal is the same rapid analogue as\n"
        "the bolus, delivered at a rate. Asking the chain with 'Basal Insulin'\n"
        "returned long-acting, 1440 min, for 679 rows whose drug is lispro.\n\n"
        "STILL MISSING: the concentration. 'Humalog 200' is U-200, and the record\n"
        "has nowhere to put that. It does not change this PK (U-200 lispro is\n"
        "bioequivalent) but it changes the volume delivered per unit."),
}


def frames(*cohorts):
    for c in cohorts:
        for p in sorted(glob.glob(str(SRC / c / "*" / "Medication.parquet"))):
            d = pd.read_parquet(p)
            if len(d):
                yield c, d


def payload(d):
    return d["medication"].dropna().map(json.loads)


def _agg(rows):
    """rows: (unit, unit_key, patient, text) -> one frame."""
    agg = {}
    for u, k, p, t in rows:
        e = agg.setdefault(u, {"k": k, "n": 0, "pts": set(), "t": t})
        e["n"] += 1
        e["pts"].add(p)
    return pd.DataFrame([
        {"unit": u, "unit_key": e["k"], "row_weight": e["n"],
         "n_patients": len(e["pts"]), "unit_text": e["t"]}
        for u, e in agg.items()]).sort_values("row_weight", ascending=False)


# --------------------------------------------------------------------- MEPS --

def units_meps():
    d = pd.read_parquet(MEPS)
    d = d[d.TC1S1_1 == MULTUM_INSULIN].copy()
    d["u"] = d.RXNAME.astype(str).str.strip()
    d["g"] = d.RXDRGNAM.astype(str).str.strip().str.upper()
    out = _agg([(r.u, r.u, r.DUPERSID, None) for r in d.itertuples()])
    out["corpus"] = "MEPS"
    out["unit_kind"] = "name_string"
    return out, d


def gold_meps(d) -> pd.DataFrame:
    """I1_IDENTITY: does the brand resolve to the right molecule?

    The gold is Multum's drug name, exactly the E1 rule, restricted to insulin.
    Frozen here rather than in _MedInfo because the QUESTION is different: E1
    asks 'which drug', I1 asks 'which insulin', and their misses are different
    misses -- a brand that collapses to the wrong analogue is a PK error, not a
    vocabulary error.
    """
    rows = []
    for name, g in d.groupby("u", sort=True):
        golds = g.g.value_counts()
        rows.append({
            "unit": name, "row_weight": len(g),
            "gold_ingredient": golds.index[0],
            "gold_ingredient_alts": list(golds.index[1:]) if len(golds) > 1 else [],
            "gold_ambiguous": len(golds) > 1,
            "name_equals_gold": name.upper() == golds.index[0],
        })
    out = pd.DataFrame(rows).sort_values("row_weight", ascending=False)
    out["corpus"] = "MEPS"
    out["set"] = "I1_IDENTITY"
    out["gold_tier"] = "G2"
    out["gold_source"] = "MEPS HC-248A 2023 / Multum Lexicon, TC1S1_1==215"
    return out.reset_index(drop=True)


# ---------------------------------------------------------------- I3a  DIA --

def gold_dia() -> pd.DataFrame:
    """I3a_DIA: the duration a PRESCRIBER recorded for THIS person.

    OWNED HERE SINCE 260822, AND REBUILT AS A PURE RULER. The earlier version
    was written by describe-medication's builder and carried three columns that
    are OUR ANSWER, not the answer key -- `table_duration_h`, `InsulinClass`
    and `abs_err_h`. A ruler that moves when the PK table moves cannot measure
    the PK table; the error columns went stale the moment `novalog` was added.
    So this frame holds the gold and its provenance and nothing else, and
    run_bench computes the error at grading time.

    WHAT IT IS NOT: a pharmacokinetic study. DIA takes three preset values, so
    it is a clinician's SETTING for a pump or a calculator. It is still the only
    number in this noun measured on a person, which is why it is tier G1 and why
    it is the only ruler that can grade DurationMin at all.
    """
    fs = [f for f in glob.glob(str(RX / "WellDoc*/Source/*MedPrescription.csv"))
          if "DaySchedule" not in f]
    if not fs:
        print("  ⚠️ no MedPrescription.csv found; I3a_DIA not rebuilt")
        return pd.DataFrame()
    rx = pd.concat([pd.read_csv(f, low_memory=False) for f in fs], ignore_index=True)
    d = pd.to_numeric(rx.get("DIA"), errors="coerce")
    g = rx[d > 0].assign(dia_h=d[d > 0])

    keep = [c for c in ["PatientID", "MedPrescriptionID", "MedicationID"]
            if c in g.columns]
    out = g[keep + ["dia_h"]].copy()
    out["unit"] = out.MedPrescriptionID.astype(str)
    out["row_weight"] = 1.0            # one prescription, one observation
    out["corpus"] = "WellDoc"
    out["set"] = "I3a_DIA"
    out["gold_tier"] = "G1"            # measured on an actual person
    out["gold_source"] = "WellDoc MedPrescription, prescriber-recorded DIA"
    return out.reset_index(drop=True)


# ------------------------------------------------------------------ cohorts --

def units_welldoc():
    rows = []
    for coh, d in frames("WellDoc2025LLY", "WellDoc2022CGM",
                         "WellDoc2025CVS", "WellDoc2025ALS"):
        m = payload(d)
        pt = d.loc[m.index, "PatientID"]
        for j, p in zip(m, pt):
            i = j.get("MedicationID")
            if i is None or i != i:
                continue
            rows.append((str(int(float(i))), str(int(float(i))), p, None))
    out = _agg(rows)
    out["corpus"] = "WellDoc"
    out["unit_kind"] = "id"
    return out


def slice_welldoc(df):
    """WellDoc's insulin slice is mednorm's own IsInsulin, applied AFTER the
    chain has run. There is no independent declaration in this cohort -- an
    integer id says nothing -- so the circularity is structural, and the only
    honest response is to name it wherever the numbers appear.
    """
    return df[df.is_insulin.fillna(False)].copy()


def units_shanghai():
    """The unit is `DrugName`, which since 260822 is the drug and not the cell.

    2,247 of 3,490 insulin rows held ONLY A NUMBER: for a pump the sheet writes
    the product once in the column header and the rate in every row. The
    SourceFn now lifts the header's product into the row, so those rows have a
    drug instead of resolving to nothing. `unit_text` keeps the route, because
    an intravenous row gets no curve at all.
    """
    rows = []
    for _, d in frames("Shanghai"):
        m = payload(d)
        col = d.loc[m.index, "MedicationID"].astype(str)
        pt = d.loc[m.index, "PatientID"]
        for j, p, c in zip(m, pt, col):
            lc = c.lower()
            if "insulin" not in lc or "non-insulin" in lc:
                continue
            name = str(j.get("DrugName") or j.get("MedicationName") or "").strip()
            if not name:
                continue
            route = j.get("DeliveryMode")
            rows.append((f"{name}\t{route or ''}", name.split(",")[0].strip(), p,
                         f"{j.get('CellKind')} · {route or 'route not stated'}"))
    out = _agg(rows)
    # The unit carries the route because the ANSWER depends on it: the same
    # Novolin R is a 480-minute curve subcutaneously and no curve at all
    # intravenously. Splitting them keeps the inventory honest about which.
    out["route"] = [u.split("\t")[1] or None for u in out.unit]
    out["unit"] = [u.split("\t")[0] for u in out.unit]
    out["corpus"] = "Shanghai"
    out["unit_kind"] = "name_string"
    return out


def units_ohio():
    """The unit is now the PRODUCT, not the class word.

    Since 260822 the Ohio SourceFn carries `insulin_type` from the study's own
    patient tag. Asking with 'Basal Insulin' returned a 24-hour glargine curve
    for 679 rows whose pump reservoir holds lispro; asking with 'Humalog' does
    not. `unit_text` keeps the class word, because basal-vs-bolus is still a
    real distinction -- it is a DELIVERY question, and the record has no field
    for it.
    """
    rows = []
    for _, d in frames("OhioT1DM"):
        m = payload(d)
        pt = d.loc[m.index, "PatientID"]
        for j, p in zip(m, pt):
            cw = str(j.get("MedicationType") or "").strip()
            if not cw or "insulin" not in cw.lower():
                continue
            prod = str(j.get("insulin_type") or "").strip()
            dm = str(j.get("DeliveryMode") or "").strip()
            unit = prod or cw
            rows.append((unit, unit, p, f"{cw} · {dm}" if dm else cw))
    out = _agg(rows)
    out["corpus"] = "OhioT1DM"
    out["unit_kind"] = "product" if any(rows) else "class_word"
    return out


# ----------------------------------------------------------------- resolver --

def ask(df):
    """What the CHAIN answers today: mednorm for the seam, insnorm for the curve.

    The ROUTE goes with the question when the corpus states one. Without it an
    intravenous row is answered with a subcutaneous curve, which is the defect
    `PKBasis` exists to stop.
    """
    items = df.unit.tolist()
    routes = df.route.tolist() if "route" in df.columns else None
    med = pd.DataFrame(mednorm(items, doses=[1] * len(items)))
    # The log's own string travels beside the seam; see the door's `raw` note.
    ins = pd.DataFrame(insnorm(med.DrugKey.tolist(), delivery=routes,
                               raw=items))
    df = df.copy()
    df["pred_drugkey"] = med.DrugKey.values
    df["is_insulin"] = med.IsInsulin.values
    df["pred_class"] = ins.InsulinClass.values
    df["pred_conf"] = ins.PKConf.values
    df["pred_basis"] = ins.PKBasis.values
    # A curve was written or it was not. PKConf is the word; DrugKey echoes the
    # input on a bank miss (rule 9) and proves nothing.
    df["resolved"] = ins.InsulinClass.notna().values
    return df


def finish(df, corpus):
    df = df.copy()
    df["has_gold"] = False
    df["gold_set"] = None
    for g in sorted((DEST / corpus).glob("*.parquet")):
        if g.name == "units.parquet":
            continue
        gold = pd.read_parquet(g)
        if "unit" not in gold.columns:
            continue
        hit = df.unit.astype(str).isin(set(gold.unit.astype(str)))
        df.loc[hit & ~df.has_gold, "gold_set"] = g.stem
        df.loc[hit, "has_gold"] = True
    extra = [c for c in df.columns if c not in COLUMNS]
    return df[COLUMNS + extra].reset_index(drop=True)


def write_readmes(built):
    for name, df in built.items():
        golds = sorted(p.stem for p in (DEST / name).glob("*.parquet")
                       if p.name != "units.parquet")
        (DEST / name / "README.md").write_text(
            f"# {name}\n\n{NOTE[name]}\n\n```text\n"
            f"  units          {len(df):>9,}   distinct {df.unit_kind.iloc[0]}\n"
            f"  rows           {int(df.row_weight.sum()):>9,}\n"
            f"  a curve today  {df.resolved.mean():>9.1%}   "
            f"{int((~df.resolved).sum()):,} units unresolved\n"
            f"  has a gold     {df.has_gold.mean():>9.1%}\n```\n\n```text\n"
            f"  {'units.parquet':<22}the inventory, always\n"
            + "".join(f"  {g + '.parquet':<22}a frozen ruler\n" for g in golds)
            + "```\n\nGENERATED. Do not hand-edit. Producer under git at\n"
            "`Tools/plugins/haipipe-utils/skills/describe-insulin/benchmark/`.\n")

    rows = []
    for name, df in sorted(built.items(), key=lambda kv: -kv[1].row_weight.sum()):
        golds = sorted(p.stem for p in (DEST / name).glob("*.parquet")
                       if p.name != "units.parquet")
        rows.append(f"{name:<12}{int(df.row_weight.sum()):>10,}{len(df):>9,}"
                    f"  {df.unit_kind.iloc[0]:<13}{df.resolved.mean():>9.1%}"
                    f"   {' '.join(golds) if golds else '-- none yet --'}")

    (DEST / "README.md").write_text(
        "# 2-corpus\n\n"
        "ONE FOLDER PER CORPUS, NAMED AFTER THE CORPUS -- the same layout as\n"
        "`_MedInfo/2-corpus`, holding the INSULIN slice of each.\n\n"
        "Membership is 'this corpus has insulin content', never 'this corpus has\n"
        "an answer'. `units.parquet` is the inventory of distinct things the\n"
        "chain is asked to give a curve, with what it answers today; a\n"
        "`<SET_ID>.parquet` appears only where a ruler exists.\n\n"
        "```text\n"
        f"{'corpus':<12}{'rows':>10}{'units':>9}  {'unit is a':<13}{'a curve':>9}"
        "   rulers\n" + "-" * 88 + "\n" + "\n".join(rows) + "\n```\n\n"
        "```text\n"
        "  WHAT DECIDES THE SLICE\n"
        "    MEPS        Multum TC1S1_1 == 215                    independent\n"
        "    Shanghai    the sheet COLUMN declares insulin        independent\n"
        "    OhioT1DM    the log's class word                     independent\n"
        "    WellDoc     mednorm's own IsInsulin flag             CIRCULAR\n"
        "```\n\n```text\n"
        "  DATA ONLY. The code lives in git at\n"
        "  Tools/plugins/haipipe-utils/skills/describe-insulin/benchmark/\n\n"
        "  source .venv/bin/activate && source env.sh\n"
        "  python .../describe-insulin/benchmark/build_units.py\n"
        "```\n")


def main():
    mu, mraw = units_meps()
    for n in ("MEPS", "WellDoc", "Shanghai", "OhioT1DM"):
        (DEST / n).mkdir(parents=True, exist_ok=True)
    gold_meps(mraw).to_parquet(DEST / "MEPS" / "I1_IDENTITY.parquet", index=False)
    dia = gold_dia()
    if len(dia):
        dia.to_parquet(DEST / "WellDoc" / "I3a_DIA.parquet", index=False)
        print(f"I3a_DIA      rows={len(dia):>6,}  "
              f"prescriptions with a DIA, values {sorted(dia.dia_h.unique())}")

    built = {
        "MEPS": finish(ask(mu), "MEPS"),
        "WellDoc": finish(slice_welldoc(ask(units_welldoc())), "WellDoc"),
        "Shanghai": finish(ask(units_shanghai()), "Shanghai"),
        "OhioT1DM": finish(ask(units_ohio()), "OhioT1DM"),
    }
    for name, df in built.items():
        df.to_parquet(DEST / name / "units.parquet", index=False)
        print(f"{name:<12} units={len(df):>6}  rows={int(df.row_weight.sum()):>9,}  "
              f"curve={df.resolved.mean():6.1%}  gold={df.has_gold.mean():6.1%}")

    write_readmes(built)
    print(f"\nwrote {DEST}")


if __name__ == "__main__":
    main()
