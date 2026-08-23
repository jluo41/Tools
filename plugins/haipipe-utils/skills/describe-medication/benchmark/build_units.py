#!/usr/bin/env python3
"""Freeze one UNIT INVENTORY per corpus into `_MedInfo/2-corpus/<Corpus>/`.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-medication/benchmark/build_units.py

WHY A CORPUS WITH NO GOLD STILL BELONGS HERE
================================================================================
The earlier rule was "a dataset earns a place in 2-corpus only if it brings an
answer". That rule cost us a real measurement. E2_LEXICON was built from the
`med_lexicon` table rather than from the ids the cohorts actually administer,
and nothing noticed until a per-corpus inventory existed:

    MedicationIDs the four WellDoc cohorts actually use      1,373
    MedicationIDs E2_LEXICON grades                            871
    in the data, absent from the gold                          892
    in the gold, never administered                            390

A gold cannot tell you it is aimed at the wrong population. Only an inventory
of what the corpus REALLY contains can. So membership is "this corpus has
medication content", and having an answer is a PROPERTY recorded per unit,
never the entry ticket.

WHAT A UNIT IS, PER CORPUS
================================================================================
The unit is what this corpus asks the resolver to resolve -- not a tidied
version of it, because a tidied string is not what production sees.

    WellDoc     an integer MedicationID              1,373 in data
    Shanghai    a name string with the dose inside     254 raw strings
                'Humulin R, 5 IU' · 'voglibose 0.2 mg'
                `unit_key` strips the dose so the 254 group into ~103 drugs
    OhioT1DM    a therapeutic class word                 2
                'Basal Insulin' · 'Bolus Insulin'
    MEPS        a pharmacy string, truncated to 12   1,447

Four kinds of thing, one schema, so the inventories concat and the whole
medication vocabulary can be read at once.

WELLDOC IS ONE CORPUS
================================================================================
Four cohort folders, one data source, one MedicationID namespace, one lexicon.
Splitting them would split a vocabulary that is not split, so `cohorts` is a
column and the folder is singular.
"""
import glob
import json
import pathlib
import re
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents if (a / "_WorkSpace").is_dir())
SKILLS = HERE.parent.parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(SKILLS / "describe-medication")]

from mednorm import normalize as mednorm                         # noqa: E402

SRC = ROOT / "_WorkSpace/1-SourceStore"
LEXICON = ROOT / "_WorkSpace/ExternalStore/medbank/med_lexicon.parquet"
MEPS = ROOT / "_WorkSpace/ExternalStore/meps/meps_h248a_rx.parquet"
DEST = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo/2-corpus"

# Shanghai writes the dose INSIDE the name, in two shapes:
#     'Humulin R, 5 IU'        comma, then dose
#     'voglibose 0.2 mg'       space, then dose
# `unit` keeps the whole string because that is what gets resolved; `unit_key`
# drops the dose so a person labelling drugs is not asked the same drug twice.
SH_DOSE = re.compile(r"\s*,?\s*[\d.]+\s*(IU|U|mg|g|mL|ml|ug|mcg)\b.*$", re.I)
MEPS_MISSING = re.compile(r"^\s*-\d+\s*$")

COLUMNS = ["corpus", "unit", "unit_key", "unit_kind", "unit_text",
           "row_weight", "n_patients", "cohorts", "dup_of",
           "pred_drugkey", "pred_conf", "resolved", "has_gold", "gold_set"]


def _blank(s) -> bool:
    s = str(s or "").strip()
    return (not s) or s.lower() in ("nan", "none") or bool(MEPS_MISSING.match(s))


def frames(*cohorts):
    """Medication.parquet lives at 1-SourceStore/<cohort>/<version>/."""
    for c in cohorts:
        for p in sorted(glob.glob(str(SRC / c / "*" / "Medication.parquet"))):
            d = pd.read_parquet(p)
            if len(d):
                yield c, d


def payload(d: pd.DataFrame) -> pd.Series:
    return d["medication"].dropna().map(json.loads)


# ------------------------------------------------------------------ WellDoc --

def welldoc_admin_counts() -> dict:
    """{MedicationID: {n, pts, coh}} over the four cohorts' administrations.

    EXPORTED because build_gold.py must weight E2 by this and not by the
    lexicon's own `RawRows`. RawRows is a bookkeeping count from the lexicon
    build, not administration volume: it totals 7,910 against 386,373 real
    rows, and it RANKS DIFFERENTLY. MedicationID 612997 -- Lyumjev, the single
    most-administered product in the dataset at 110,654 rows -- carries
    RawRows=1, while a cephalexin nobody took carries 89. Weighting a
    'deployment' number by that measures a population that does not exist; it
    understated E2's row-weighted accuracy by 10 points.
    """
    seen = {}
    for coh, d in frames("WellDoc2025LLY", "WellDoc2022CGM",
                         "WellDoc2025CVS", "WellDoc2025ALS", "WellDoc2026Libre"):
        m = payload(d)
        ids = m.map(lambda j: j.get("MedicationID"))
        pt = d.loc[ids.index, "PatientID"]
        for i, p in zip(ids, pt):
            if i is None or i != i:
                continue
            k = str(int(float(i)))
            e = seen.setdefault(k, {"n": 0, "pts": set(), "coh": set()})
            e["n"] += 1
            e["pts"].add(p)
            e["coh"].add(coh)
    return seen


def units_welldoc() -> pd.DataFrame:
    """The four cohorts pooled, plus every id the lexicon knows.

    A unit is kept when it appears in EITHER place, and both facts are columns.
    An id in the data with no lexicon row is a hole in the bank; an id in the
    lexicon that nobody administered is dead weight in the gold. Dropping
    either one hides the mismatch that motivated this file.
    """
    seen = welldoc_admin_counts()
    lex = pd.read_parquet(LEXICON)
    lex["MedicationID"] = lex.MedicationID.astype(str)
    text = dict(zip(lex.MedicationID, lex.MedicationName))

    rows = []
    for k in sorted(set(seen) | set(text), key=lambda x: -seen.get(x, {}).get("n", 0)):
        e = seen.get(k, {"n": 0, "pts": set(), "coh": set()})
        rows.append({
            "corpus": "WellDoc", "unit": k, "unit_key": k, "unit_kind": "id",
            "unit_text": text.get(k),
            "row_weight": e["n"], "n_patients": len(e["pts"]),
            "cohorts": sorted(e["coh"]),
            "in_data": k in seen, "in_lexicon": k in text,
        })
    return mark_dupes(pd.DataFrame(rows))


def mark_dupes(df: pd.DataFrame) -> pd.DataFrame:
    """`dup_of`: another unit in this corpus with the BYTE-IDENTICAL name.

    Ten product names in the WellDoc lexicon carry two MedicationIDs -- one
    Tresiba, one Humalog, one Symbicort, a bare TESTOSTERONE -- so the id is
    not a clean primary key for a drug. Marked rather than merged: which id a
    row used is a fact about the source, and rule 2 says TYPE, DO NOT DELETE.
    The lowest-numbered id in each group is the canonical one.

    ONLY WHERE THE UNIT IS AN OPAQUE ID. A `name_string` unit IS its own name:
    two of them cannot share a name without being the same unit. Running this
    on Shanghai marked 247 of its 254 units as duplicates, because Shanghai's
    `unit_text` holds the SHEET COLUMN ('Insulin dose - s.c.') and nearly every
    row shares one. Only an id needs a separate name to say what it is, so only
    an id can have two ids meaning one thing.
    """
    df = df.copy()
    df["dup_of"] = None
    if not len(df) or "unit_kind" not in df or df.unit_kind.iloc[0] != "id":
        return df
    named = df[df.unit_text.notna() & df.unit_text.astype(str).str.len().gt(0)]
    for text, g in named.groupby("unit_text"):
        if len(g) < 2:
            continue
        canon = sorted(g.unit, key=lambda x: (len(x), x))[0]
        df.loc[df.unit.isin(set(g.unit) - {canon}), "dup_of"] = canon
    return df


# ----------------------------------------------------------------- Shanghai --

def units_shanghai() -> pd.DataFrame:
    agg = {}
    for _, d in frames("Shanghai"):
        m = payload(d)
        pt = d.loc[m.index, "PatientID"]
        col = d.loc[m.index, "MedicationID"]        # the sheet column it came from
        for j, p, c in zip(m, pt, col):
            s = str(j.get("MedicationName") or "").strip()
            if not s:
                continue
            e = agg.setdefault(s, {"n": 0, "pts": set(), "cols": set()})
            e["n"] += 1
            e["pts"].add(p)
            e["cols"].add(str(c))
    rows = [{
        "corpus": "Shanghai", "unit": s, "unit_key": SH_DOSE.sub("", s).strip(" ,-"),
        "unit_kind": "name_string", "unit_text": " | ".join(sorted(e["cols"])),
        "row_weight": e["n"], "n_patients": len(e["pts"]), "cohorts": ["Shanghai"],
    } for s, e in agg.items()]
    return pd.DataFrame(rows).sort_values("row_weight", ascending=False)


# ----------------------------------------------------------------- OhioT1DM --

def units_ohio() -> pd.DataFrame:
    agg = {}
    for _, d in frames("OhioT1DM"):
        m = payload(d)
        pt = d.loc[m.index, "PatientID"]
        for j, p in zip(m, pt):
            s = str(j.get("MedicationType") or "").strip()
            if not s:
                continue
            e = agg.setdefault(s, {"n": 0, "pts": set()})
            e["n"] += 1
            e["pts"].add(p)
    rows = [{
        "corpus": "OhioT1DM", "unit": s, "unit_key": s, "unit_kind": "class_word",
        "unit_text": None, "row_weight": e["n"], "n_patients": len(e["pts"]),
        "cohorts": ["OhioT1DM"],
    } for s, e in agg.items()]
    return pd.DataFrame(rows).sort_values("row_weight", ascending=False)


# --------------------------------------------------------------------- MEPS --

def units_meps() -> pd.DataFrame:
    d = pd.read_parquet(MEPS)
    d = d[~d.RXNAME.map(_blank)].copy()
    d["u"] = d.RXNAME.astype(str).str.strip()
    g = d.groupby("u").agg(row_weight=("u", "size"),
                           n_patients=("DUPERSID", "nunique")).reset_index()
    g = g.rename(columns={"u": "unit"})
    g["corpus"] = "MEPS"
    g["unit_key"] = g.unit
    g["unit_kind"] = "name_string"
    g["unit_text"] = None
    g["cohorts"] = [["MEPS"]] * len(g)
    return g.sort_values("row_weight", ascending=False)


# ----------------------------------------------------------------- resolver --

def ask(df: pd.DataFrame) -> pd.DataFrame:
    """Record what the resolver answers TODAY for every unit.

    This is behaviour, not gold. It is here because the units a corpus cannot
    resolve ARE the annotation candidate pool, and a pool you have to recompute
    is a pool nobody samples from.
    """
    if not len(df):
        return df
    items = df.unit.tolist()
    r = pd.DataFrame(mednorm(items, doses=[1] * len(items)))
    df = df.copy()
    df["pred_drugkey"] = r.DrugKey.values
    df["pred_conf"] = r.MedConf.values
    # Rule 9 makes DrugKey echo the input on a bank miss, so a non-null DrugKey
    # is not evidence of a resolution. Trust the confidence word instead.
    df["resolved"] = ~r.MedConf.isin(["MISS"]).values
    return df


def finish(df: pd.DataFrame, corpus: str) -> pd.DataFrame:
    if "dup_of" not in df.columns:
        df = mark_dupes(df)
    """Mark has_gold from the FROZEN gold files, never from a rule.

    Restating build_gold's inclusion rule here is how the two drift: MEPS has
    1,550 distinct pharmacy strings but only 1,447 carry a Multum name, and an
    inventory that assumed otherwise reported 100% gold coverage on its first
    run. Read the ruler that actually exists.
    """
    df = df.copy()
    df["has_gold"] = False
    df["gold_set"] = None
    for g in sorted((DEST / corpus).glob("*.parquet")):
        if g.name == "units.parquet":
            continue
        gold = pd.read_parquet(g)
        if "unit" not in gold.columns:
            continue
        keep = gold[gold.gold_tier.ne("UNLABELLED")] if "gold_tier" in gold else gold
        hit = df.unit.astype(str).isin(set(keep.unit.astype(str)))
        df.loc[hit & ~df.has_gold, "gold_set"] = g.stem
        df.loc[hit, "has_gold"] = True
    extra = [c for c in df.columns if c not in COLUMNS]
    return df[COLUMNS + extra].reset_index(drop=True)


# ------------------------------------------------------------------ prose ---

NOTE = {
    "WellDoc": (
        "Four cohort folders, ONE corpus: WellDoc2025LLY, WellDoc2022CGM,\n"
        "WellDoc2025CVS, WellDoc2025ALS (and WellDoc2026Libre, table present,\n"
        "no rows). One data source, one MedicationID namespace, one lexicon --\n"
        "splitting them would split a vocabulary that is not split. Which\n"
        "cohorts used a unit is the `cohorts` column.\n\n"
        "THE UNIT IS AN INTEGER. Nothing about `612997` says what drug it is;\n"
        "the product name comes from `med_lexicon`, and `in_lexicon` records\n"
        "whether it has one.\n\n"
        "THE MISMATCH THIS FOLDER EXISTS TO SHOW\n"
        "```text\n"
        "  ids the cohorts actually administer      1,373\n"
        "  ids med_lexicon knows                       871\n"
        "  administered, absent from the lexicon       892   <- 65% of what is used\n"
        "  in the lexicon, never administered          390\n"
        "```\n"
        "E2_LEXICON grades the second row. It cannot see the third, and no\n"
        "score computed from it would have revealed the gap.\n\n"
        "TEN IDS ARE DUPLICATES AND ARE MARKED, NOT MERGED. Ten product names\n"
        "carry two MedicationIDs each -- one Tresiba (1,404 rows), one\n"
        "Symbicort (349), one Humalog, a bare TESTOSTERONE -- so the id is not\n"
        "a clean primary key for a drug. `dup_of` names the canonical id; which\n"
        "id a row actually used stays a fact about the source (rule 2).\n\n"
        "HOW HONEST IS row_weight? Every MedAdministrationID is unique, so\n"
        "nothing here is an export-level duplicate. But 13.1% of rows sit in a\n"
        "group sharing patient + timestamp + id + dose:\n"
        "```text\n"
        "  group of 1   335,808   86.9%   not duplicated at all\n"
        "  group of 2    36,912    9.6%   plausible: two units logged in one minute\n"
        "  group of 3-5  13,187    3.4%\n"
        "  group of 6+      440    0.1%   <- 81.6% of the 11+ rows land on a\n"
        "                                    ROUND HOUR against a 4.9% baseline,\n"
        "                                    so these are bulk back-entry, not\n"
        "                                    37 real injections at 5:00:00 AM\n"
        "```\n"
        "Deduplicating on patient+time+id+dose would remove 7.3% of rows;\n"
        "additionally requiring the same EntryDateTime removes 3.7%. NOTHING IS\n"
        "DEDUPLICATED HERE, because a minute-resolution timestamp cannot be told\n"
        "from a double-log, and the extreme groups are 0.1% of the mass. The\n"
        "sensitivity is recorded so a later reader can decide with the number in\n"
        "front of them."),
    "Shanghai": (
        "A clinical sheet: five insulin / oral columns, drug and dose in ONE\n"
        "string, English and Chinese mixed. `unit` keeps the whole string\n"
        "because that is what the resolver sees; `unit_key` drops the trailing\n"
        "dose so the 254 strings group into the ~103 distinct drugs a person\n"
        "would actually have to label.\n\n"
        "NO GOLD, AND IT IS THE CHEAPEST ONE LEFT. 103 drug identities is an\n"
        "afternoon of labelling, and it is the ONLY non-English dialect we\n"
        "have. Today we know how many rows resolve and nothing about whether\n"
        "they resolve correctly."),
    "OhioT1DM": (
        "A study log that records a therapeutic CLASS and never a product:\n"
        "5,026 rows carrying exactly two words, 'Basal Insulin' and 'Bolus\n"
        "Insulin'.\n\n"
        "A DRUG-IDENTITY GOLD IS NOT MERELY MISSING HERE, IT IS IMPOSSIBLE --\n"
        "the log never named a drug, so no labeller could recover one. What\n"
        "this corpus CAN grade is describe-insulin's class channel, where two\n"
        "words decide 5,026 rows and there is nowhere for an error to hide."),
    "MEPS": (
        "Medical Expenditure Panel Survey, Prescribed Medicines file HC-248A,\n"
        "2023. US federal PUBLIC USE FILE: no data use agreement, no\n"
        "registration, redistribution of derived files permitted.\n\n"
        "```text\n"
        "  https://meps.ahrq.gov/mepsweb/data_files/pufs/h248a/h248adta.zip\n"
        "  downloaded 260822 · raw archive kept at ExternalStore/meps/\n"
        "```\n"
        "WHY IT IS A GOLD AND NOT ANOTHER BANK: the answer key is Multum\n"
        "Lexicon, a different organisation's curation, and NOT the FDA NDC\n"
        "Directory this library resolves against. A gold produced by the thing\n"
        "it grades measures self-consistency.\n\n"
        "```text\n"
        "  RXNAME     the pharmacy's string, TRUNCATED TO 12 CHARACTERS\n"
        "             'LEVOTHYROXIN' · 'HYDROCHLOROT' · 'LANTUS SOLOS'\n"
        "             a real-world corruption our own cohorts do not have\n"
        "  RXDRGNAM   Multum's drug name         -> the ingredient gold\n"
        "  RXNDC      the NDC the pharmacy gave  -> the product gold\n"
        "  TC1..TC3   Multum's class hierarchy   -> the class gold\n"
        "```\n"
        "1,550 distinct strings are inventoried; 1,447 carry a Multum name and\n"
        "are gradeable. Negative integers are MEPS missing codes, not values."),
}

EMPTY = {"CGMacros": "no medication table content",
         "dubosson": "no medication table content",
         "aireadi-noimage-v2": "no medication table content",
         "aireadi-v3": "no medication table content",
         "WellDoc2026Libre": "folded into WellDoc; table present, no rows"}


def write_readmes(built):
    for name, df in built.items():
        golds = sorted(p.stem for p in (DEST / name).glob("*.parquet")
                       if p.name != "units.parquet")
        (DEST / name / "README.md").write_text(
            f"# {name}\n\n{NOTE[name]}\n\n"
            "```text\n"
            f"  units          {len(df):>9,}   distinct {df.unit_kind.iloc[0]}\n"
            f"  rows           {int(df.row_weight.sum()):>9,}\n"
            f"  patients       {int(df.n_patients.max()):>9,}   (max over units)\n"
            f"  resolved today {df.resolved.mean():>9.1%}   "
            f"{int((~df.resolved).sum()):,} units are the annotation pool\n"
            f"  has a gold     {df.has_gold.mean():>9.1%}\n"
            "```\n\n"
            "```text\n"
            f"  {'units.parquet':<22}the inventory, always\n"
            + "".join(f"  {g + '.parquet':<22}a frozen ruler\n" for g in golds)
            + "```\n\nGENERATED. Do not hand-edit. Producer under git at\n"
            "`Tools/plugins/haipipe-utils/skills/describe-medication/benchmark/`.\n")

    rows = []
    for name, df in sorted(built.items(), key=lambda kv: -kv[1].row_weight.sum()):
        golds = sorted(p.stem for p in (DEST / name).glob("*.parquet")
                       if p.name != "units.parquet")
        rows.append(f"{name:<12}{int(df.row_weight.sum()):>10,}{len(df):>9,}"
                    f"  {df.unit_kind.iloc[0]:<13}{df.resolved.mean():>9.1%}"
                    f"   {' '.join(golds) if golds else '-- none yet --'}")

    (DEST / "README.md").write_text(
        "# 2-corpus\n\n"
        "ONE FOLDER PER CORPUS, NAMED AFTER THE CORPUS. Open the folder and you\n"
        "know where the data came from without opening a parquet.\n\n"
        "MEMBERSHIP IS 'THIS CORPUS HAS MEDICATION CONTENT', NOT 'THIS CORPUS HAS\n"
        "AN ANSWER'. Having a gold is a property recorded per unit, never the\n"
        "entry ticket -- see build_units.py for the measurement that cost us.\n\n"
        "Every folder holds `units.parquet`, the inventory of distinct things\n"
        "this corpus asks the resolver to resolve, with what it answers today.\n"
        "A folder holds a `<SET_ID>.parquet` as well only where a gold exists.\n\n"
        "```text\n"
        f"{'corpus':<12}{'rows':>10}{'units':>9}  {'unit is a':<13}{'resolved':>9}"
        "   rulers\n"
        + "-" * 88 + "\n" + "\n".join(rows) + "\n```\n\n"
        "```text\n  DATA ONLY. The code that produces all of this lives in git at\n"
        "  Tools/plugins/haipipe-utils/skills/describe-medication/benchmark/\n\n"
        "  source .venv/bin/activate && source env.sh\n"
        "  python .../benchmark/build_gold.py     # the rulers\n"
        "  python .../benchmark/build_units.py    # the inventories\n"
        "  python .../benchmark/run_bench.py      # the readings -> 6-benchmark/\n"
        "```\n\nSee `_empty.md` for the corpora with no medication rows at all.\n")

    (DEST / "_empty.md").write_text(
        "# corpora with no medication content\n\n"
        "Listed, not omitted: a reader must be able to tell 'we looked and there\n"
        "was nothing' from 'we never looked'. Each has a Medication table that\n"
        "exists and holds zero rows. The moment one gains rows it gets a folder\n"
        "here with no change to any of this.\n\n"
        "```text\n"
        + "".join(f"  {k:<22}{v}\n" for k, v in EMPTY.items()) + "```\n")


# --------------------------------------------------------------------- main --

def main():
    built = {
        "WellDoc": finish(ask(units_welldoc()), "WellDoc"),
        "Shanghai": finish(ask(units_shanghai()), "Shanghai"),
        "OhioT1DM": finish(ask(units_ohio()), "OhioT1DM"),
        "MEPS": finish(ask(units_meps()), "MEPS"),
    }

    for name, df in built.items():
        d = DEST / name
        d.mkdir(parents=True, exist_ok=True)
        df.to_parquet(d / "units.parquet", index=False)
        print(f"{name:<12} units={len(df):>6}  rows={int(df.row_weight.sum()):>9,}  "
              f"resolved={df.resolved.mean():6.1%}  gold={df.has_gold.mean():6.1%}")

    write_readmes(built)
    (DEST / "_units_summary.json").write_text(json.dumps({
        n: {"units": len(d), "rows": int(d.row_weight.sum()),
            "resolved": float(d.resolved.mean()),
            "with_gold": int(d.has_gold.sum()),
            "unresolved_units": int((~d.resolved).sum()),
            "unresolved_rows": int(d.loc[~d.resolved, "row_weight"].sum())}
        for n, d in built.items()}, indent=1) + "\n")
    print(f"\nwrote {DEST}")


if __name__ == "__main__":
    main()
