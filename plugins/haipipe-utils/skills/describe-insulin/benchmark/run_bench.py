#!/usr/bin/env python3
"""Grade describe-insulin against the frozen golds.

    source .venv/bin/activate && source env.sh
    python .../describe-insulin/benchmark/run_bench.py
    python .../describe-insulin/benchmark/run_bench.py --set I1_IDENTITY --tag after-fix

Writes `_InsInfo/6-benchmark/runs/<tag>-gold-insulin.json` and `GOLD.md`.
It never touches 2-corpus: the ruler is frozen elsewhere, on purpose.
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(a for a in HERE.parents if (a / "_WorkSpace").is_dir())
SKILLS = HERE.parent.parent
sys.path[:0] = [str(HERE), str(HERE.parent), str(SKILLS / "describe-medication")]

import insulinname as N                                          # noqa: E402
import score as S                                                # noqa: E402
from insnorm import normalize as insnorm                         # noqa: E402
from insnorm.client import TRUSTED as INS_TRUSTED                # noqa: E402
from mednorm import normalize as mednorm                         # noqa: E402
from mednorm.constants import TRUSTED as MED_TRUSTED             # noqa: E402

INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_InsInfo"
CORPUS, DEST = INFO / "2-corpus", INFO / "6-benchmark"
CONF_ORDER = ["GOOD", "OK", "ALIAS", "MISS"]

SETS = {"I1_IDENTITY": CORPUS / "MEPS" / "I1_IDENTITY.parquet",
        "I3a_DIA": CORPUS / "WellDoc" / "I3a_DIA.parquet"}


def git_head():
    try:
        h = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        d = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "-uno"],
                           capture_output=True, text=True, timeout=20).stdout.strip()
        return h + ("-dirty" if d else "")
    except Exception:                                            # noqa: BLE001
        return "unknown"


def run_set(name: str, df: pd.DataFrame, n) -> dict:
    if n:
        df = df.head(n).copy()
    units = df.unit.astype(str).tolist()

    # THE WHOLE CHAIN IS RUN, because the whole chain is what a caller uses.
    # Feeding the raw string straight to insnorm would grade a door nobody
    # knocks on: production always arrives through describe-medication.
    med = pd.DataFrame(mednorm(units, doses=[1] * len(units)))
    # `raw=units` -- the pharmacy string travels beside the seam, which is what
    # a real caller has. It is used only where it resolves to a strictly more
    # specific key, so it recovers TOUJEO's U-300 (the bank collapses it to the
    # ingredient) without touching anything the seam already got right.
    preds = insnorm(med.DrugKey.tolist(), raw=units)
    confs = [p.get("PKConf") or "MISS" for p in preds]

    graded = [
        S.grade_unit(p, mc, r.gold_ingredient,
                     getattr(r, "gold_ingredient_alts", []), list(MED_TRUSTED))
        for p, mc, r in zip(preds, med.MedConf.tolist(), df.itertuples())
    ]
    out = S.summarize(graded, confs, df.row_weight.astype(float).tolist(),
                      CONF_ORDER, list(INS_TRUSTED))
    out["set"] = name
    out["units_graded"] = len(df)

    bad = [(float(r.row_weight), str(r.unit), str(r.gold_ingredient),
            preds[i].get("InsulinResolved"), preds[i].get("InsulinClass"),
            graded[i]["gold_class"], confs[i])
           for i, r in enumerate(df.itertuples()) if not graded[i]["molecule_exact"]]
    bad.sort(reverse=True)
    out["worst_misses"] = [
        {"row_weight": w, "input": u, "gold": g, "ours": o,
         "our_class": c, "gold_class": gc, "conf": k}
        for w, u, g, o, c, gc, k in bad[:25]]

    out["more_specific"] = [
        {"input": str(r.unit), "gold": str(r.gold_ingredient),
         "ours": preds[i].get("InsulinResolved"), "variant": graded[i]["variant"],
         "row_weight": float(r.row_weight)}
        for i, r in enumerate(df.itertuples()) if graded[i]["more_specific"]]
    return out


def run_dia(name: str, df: pd.DataFrame, n) -> dict:
    """I3a: DurationMin against a DIA the prescriber recorded for that person.

    THE GOLD IS DELIBERATELY NOT PASSED IN. `normalize(dia_hours=...)` replaces
    DurationMin with the DIA and stamps GOOD; grading that would score a copy of
    the input. Everything here is the TABLE answering on its own.
    """
    if n:
        df = df.head(n).copy()
    ids = df.MedicationID.astype(str).tolist()
    med = pd.DataFrame(mednorm(ids, doses=[1] * len(ids)))
    # no dia_hours -- see above. `raw` is the MedicationID, an integer, which
    # resolves to nothing, so it is not passed: there is no log string here.
    preds = insnorm(med.DrugKey.tolist())

    graded = [S.grade_duration(p, g) for p, g in zip(preds, df.dia_h.tolist())]
    out = S.summarize_duration(graded)
    out["set"] = name
    out["units_graded"] = len(df)

    worst = sorted(
        ((g["abs_err_h"], str(r.MedicationID), med.DrugKey.iloc[i],
          g["pred_class"], g["ours_h"], g["gold_h"])
         for i, (g, r) in enumerate(zip(graded, df.itertuples()))
         if g["abs_err_h"] is not None), reverse=True)
    seen, rows = set(), []
    for e, mid, key, cls, ours, gold in worst:
        if key in seen:
            continue
        seen.add(key)
        rows.append({"abs_err_h": e, "MedicationID": mid, "drugkey": key,
                     "class": cls, "ours_h": ours, "gold_h": gold})
        if len(rows) >= 15:
            break
    out["worst_by_drug"] = rows
    return out


def render_dia(r) -> list:
    L = ["", f"## {r['set']}", "",
         "The only ruler in this noun measured on a PERSON: a duration of insulin",
         "action the prescriber recorded for that patient. Tier G1.", "",
         "```text",
         f"  prescriptions graded  {r['units_graded']:,}",
         f"  a duration answered   {_p(r['coverage'])}",
         f"  gradeable (an insulin){r['n_gradeable']:>9,}"
         f"   ({r['n_not_insulin']:,} resolve to no insulin and are NOT scored wrong)",
         "",
         f"  median |error|        {r['median_abs_err_h']:.2f} h"
         if r["median_abs_err_h"] is not None else "  median |error|        -",
         f"  mean   |error|        {r['mean_abs_err_h']:.2f} h"
         if r["mean_abs_err_h"] is not None else "  mean   |error|        -",
         f"  median SIGNED error   {r['median_signed_err_h']:+.2f} h"
         if r["median_signed_err_h"] is not None else "  median SIGNED error   -",
         f"  within +/-{r['tolerance_h']} h         {_p(r['within_tolerance'])}",
         "```", "",
         "The SIGNED error is the one to read. A table uniformly short and a table",
         "off at random share a MAE and need different fixes.", "",
         "### the gold's own grid", "",
         "Three preset values, not a continuous measurement. Read every error",
         "against that before reading it as physiology.", "",
         "```text"]
    for k, v in r["gold_grid"].items():
        L.append(f"  {k:>5} h {v:>9,} prescriptions")
    L += ["```", "", "### by the class we answered", "", "```text",
          f"  {'class':<13}{'n':>7}{'signed err':>13}   gold DIA -> ours (h)"]
    for cls, v in r["by_class"].items():
        g = ", ".join(f"{x:g}" for x in v["gold_dia_h"])
        o = ", ".join(f"{x:g}" for x in v["our_duration_h"])
        L.append(f"  {cls:<13}{v['n']:>7}{v['median_signed_err_h']:>+13.2f}   {g} -> {o}")
    L += ["```", "", "### worst drugs by absolute error", "", "```text",
          f"  {'|err| h':>8}  {'DrugKey':<28}{'class':<13}{'ours':>7}{'gold':>7}"]
    for w in r["worst_by_drug"]:
        L.append(f"  {w['abs_err_h']:>8.2f}  {str(w['drugkey'])[:26]:<28}"
                 f"{str(w['class']):<13}{w['ours_h']:>7.1f}{w['gold_h']:>7.1f}")
    L += ["```", ""]
    return L


def _p(v):
    return "     -" if v is None else f"{v:6.1%}"


def render(runs, tag, at, head) -> str:
    L = ["# GOLD -- B2", "",
         "describe-insulin against an outside answer key. `CONTRACT.md` beside",
         "this file is the no-gold half of the scorecard; this is the half that",
         "needs one.", "",
         "GENERATED. Do not hand-edit. The producer is under git at",
         "`Tools/plugins/haipipe-utils/skills/describe-insulin/benchmark/`.", "",
         "```bash", "source .venv/bin/activate && source env.sh",
         "python .../describe-insulin/benchmark/build_units.py   # the ruler, once",
         "python .../describe-insulin/benchmark/run_bench.py     # the reading",
         "```", "",
         f"run `{tag}` · {at} · code at `{head}`", "",
         "", "## What is graded, and why it is three things", "",
         "```text",
         "  SEAM        did describe-medication resolve at all? Everything below",
         "              is bounded by it, and rule 9's DrugKey echo means a",
         "              non-null seam proves nothing -- MedConf is the test.",
         "  MOLECULE    InsulinResolved vs Multum's drug name.",
         "  CLASS       InsulinClass vs the class this benchmark derives from the",
         "              GOLD molecule, by its own table, never insnorm's.",
         "",
         "  A wrong molecule inside the right class moves a curve by minutes.",
         "  A wrong class moves it by hours. One number could not tell them apart.",
         "```", "",
         "", "## The gold is coarser than we are, on purpose", "",
         "```text",
         "  MEPS names the parent molecule and we answer the variant:",
         "    SEMGLEE   gold INSULIN GLARGINE   ours insulin glargine-yfgn",
         "    LYUMJEV   gold INSULIN LISPRO     ours insulin lispro-aabc",
         "    TOUJEO    gold INSULIN GLARGINE   ours insulin glargine u300",
         "  These are MORE SPECIFIC, not wrong. The comparison folds the variant",
         "  and counts how often it did; scoring them as misses would push the",
         "  resolver toward a coarser table.",
         "```", ""]

    for r in runs:
        if r["set"] == "I3a_DIA":
            L += render_dia(r)
            continue
        o = r["overall"]
        L += ["", f"## {r['set']}", "", "```text",
              f"  units graded          {r['units_graded']:,}", ""]
        for w in ("row", "type"):
            a = o[w]
            what = ("every fill counts once -- DEPLOYMENT" if w == "row"
                    else "every distinct string once -- VOCABULARY")
            L += [f"  {w:<5} weighted   {what}",
                  f"    seam: medication resolved           {_p(a['seam_med_resolved'])}",
                  f"    coverage (a molecule)               {_p(a['coverage_molecule'])}",
                  f"    coverage (a class)                  {_p(a['coverage_class'])}",
                  f"    molecule exact, of ANSWERED         {_p(a['molecule_exact_of_answered'])}",
                  f"    molecule exact, of ALL              {_p(a['molecule_exact_of_all'])}",
                  f"    molecule F1,    of ANSWERED         {_p(a['molecule_f1_of_answered'])}",
                  f"    class exact,    of GRADEABLE        {_p(a['class_exact_of_gradeable'])}"
                  f"   (n={a['n_class_gradeable']:,})",
                  f"    answered MORE SPECIFICALLY than gold {a['n_more_specific']:>4} units", ""]
        L += ["```", "",
              "### risk-coverage, row-weighted", "",
              "Cumulative down the DECLARED confidence order. Accuracy must fall.", "",
              "```text",
              f"  {'through':<10}{'coverage':>10}{'molecule':>11}{'class':>9}"]
        for p in r["curve"]["row"]:
            L.append(f"  {p['through_tier']:<10}{p['coverage']:>10.1%}"
                     f"{_p(p['molecule_exact']):>11}{_p(p['class_exact']):>9}")
        mono = r["monotone"]["row"]
        L += ["```", "",
              f"monotone: {'YES' if mono else 'NO -- the ladder is mis-ordered'}", ""]

        if r.get("class_confusion"):
            L += ["### where the CLASS is wrong", "",
                  "By fills, worst first. This is the table a clinician reads.", "",
                  "```text"]
            for k, v in r["class_confusion"].items():
                L.append(f"  {v:>8,}  {k}")
            L += ["```", ""]

        if r.get("more_specific"):
            L += ["### answered more specifically than the gold", "", "```text"]
            for m in r["more_specific"]:
                L.append(f"  {m['row_weight']:>8,.0f}  {m['input']:<22}"
                         f"{m['gold']:<24}{m['ours']}   (+{m['variant']})")
            L += ["```", ""]

        L += ["### the most expensive misses", "", "```text",
              f"  {'rows':>8}  {'input':<22}{'gold':<34}{'ours':<26}conf"]
        for m in r["worst_misses"]:
            L.append(f"  {m['row_weight']:>8,.0f}  {m['input']:<22}{m['gold']:<34}"
                     f"{str(m['ours'])[:24]:<26}{m['conf']}")
        L += ["```", ""]

    L += ["", "## What this set cannot say", "",
          "```text",
          "  NOTHING ABOUT OUR OWN DIALECTS. MEPS holds no MedicationID and no",
          "  Chinese product name. Shanghai declares 3,490 insulin rows and only",
          "  a third get a curve, and no gold exists to say whether that third",
          "  is right.",
          "",
          "  NOTHING ABOUT THE NUMBERS. This grades the molecule and the class,",
          "  never onset / peak / duration. I3a_DIA grades duration alone on",
          "  1,831 real prescriptions; onset and peak have no ruler at all.",
          "",
          "  NOTHING ABOUT CONCENTRATION. TOUJEO SOLO answers 1800 min and TOUJEO",
          "  SOLOSTAR answers 1440 -- the same U-300 product, two durations,",
          "  decided by spelling. Both pass the molecule test and both pass the",
          "  class test. Only a duration ruler would catch it.",
          "```", ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", dest="only", choices=list(SETS))
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()

    at = datetime.datetime.now().replace(microsecond=0).isoformat()
    tag = a.tag or at[:10].replace("-", "")[2:]
    head = git_head()

    runs = []
    for name, path in SETS.items():
        if a.only and name != a.only:
            continue
        if not path.exists():
            print(f"  skipping {name}: no ruler at {path}")
            continue
        print(f"  grading {name} ...", flush=True)
        df = pd.read_parquet(path)
        runs.append(run_dia(name, df, a.n) if name == "I3a_DIA"
                    else run_set(name, df, a.n))

    (DEST / "runs").mkdir(parents=True, exist_ok=True)
    body = {"bench": "B2_gold", "tag": tag, "at": at, "git_head": head,
            "noun": "insulin", "sets": runs}
    (DEST / "runs" / f"{tag}-gold-insulin.json").write_text(
        json.dumps(body, indent=1) + "\n")
    (DEST / "_gold.json").write_text(json.dumps(
        {"bench": "B2_gold", "tag": tag, "at": at, "git_head": head,
         "sets": {r["set"]: ({"units": r["units_graded"],
                             "median_abs_err_h": r["median_abs_err_h"],
                             "median_signed_err_h": r["median_signed_err_h"],
                             "within_tolerance": r["within_tolerance"]}
                            if r["set"] == "I3a_DIA" else
                            {"units": r["units_graded"], "row": r["overall"]["row"],
                             "monotone": r["monotone"]}) for r in runs}},
        indent=1) + "\n")
    (DEST / "GOLD.md").write_text(render(runs, tag, at, head))

    for r in runs:
        if r["set"] == "I3a_DIA":
            print(f"\n  {r['set']}  prescriptions={r['units_graded']:,}")
            print(f"    coverage {_p(r['coverage'])} · gradeable {r['n_gradeable']:,}"
                  f" · not-insulin {r['n_not_insulin']:,}")
            print(f"    median |err| {r['median_abs_err_h']:.2f} h · "
                  f"signed {r['median_signed_err_h']:+.2f} h · "
                  f"within {r['tolerance_h']}h {_p(r['within_tolerance'])}")
            continue
        o = r["overall"]["row"]
        print(f"\n  {r['set']}  units={r['units_graded']:,}")
        print(f"    seam {_p(o['seam_med_resolved'])} · molecule cov "
              f"{_p(o['coverage_molecule'])} · exact(all) {_p(o['molecule_exact_of_all'])}"
              f" · exact(answered) {_p(o['molecule_exact_of_answered'])}")
        print(f"    class exact {_p(o['class_exact_of_gradeable'])} "
              f"(n={o['n_class_gradeable']}) · more-specific {o['n_more_specific']}"
              f" · monotone {r['monotone']['row']}")
    print(f"\n  wrote {DEST}")


if __name__ == "__main__":
    main()
