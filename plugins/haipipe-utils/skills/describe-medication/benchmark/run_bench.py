#!/usr/bin/env python3
"""Grade describe-medication against the frozen golds.

    source .venv/bin/activate && source env.sh
    python .../benchmark/run_bench.py                 # both sets, everything
    python .../benchmark/run_bench.py --n 300         # a fast sample
    python .../benchmark/run_bench.py --set E1_ALL --tag after-the-fix

Writes `_MedInfo/6-benchmark/runs/<tag>-gold-medication.json` and `GOLD.md`.
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
sys.path[:0] = [str(HERE), str(HERE.parent), str(HERE.parents[1] / "haipipe-norm")]

import score as S                                                # noqa: E402
from mednorm import normalize                                    # noqa: E402
from mednorm.constants import TRUSTED                            # noqa: E402

INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_MedInfo"
CORPUS, DEST = INFO / "2-corpus", INFO / "6-benchmark"
CONF_ORDER = ["GOOD", "OK", "ALIAS", "WEAK", "MISS"]


def git_head():
    try:
        h = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        d = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "-uno"],
                           capture_output=True, text=True, timeout=20).stdout.strip()
        return h + ("-dirty" if d else "")
    except Exception:                                            # noqa: BLE001
        return "unknown"


def run_set(name: str, df: pd.DataFrame, n: int | None) -> dict:
    dropped = 0
    if name == "E2_LEXICON":
        before = len(df)
        # The unparseable 202 have no gold yet. They are REPORTED as a hole,
        # never silently excluded: a benchmark that drops its hard cases reads
        # as coverage it does not have.
        df = df[df.parseable].copy()
        dropped = before - len(df)
    if n:
        df = df.head(n).copy()

    units = df.unit.astype(str).tolist()
    preds = normalize(units)
    confs = [p.get("MedConf") or "MISS" for p in preds]
    graded = [
        S.grade_unit(p, r.gold_ingredient, getattr(r, "gold_ingredient_alts", []),
                     [] if r.gold_ndc9 is None else list(r.gold_ndc9))
        for p, r in zip(preds, df.itertuples())
    ]
    out = S.summarize(graded, confs, df.row_weight.astype(float).tolist(),
                      CONF_ORDER, list(TRUSTED),
                      drug_w=S.drug_weights(df.gold_ingredient.tolist()))
    out["n_distinct_gold_drugs"] = round(sum(
        S.drug_weights(df.gold_ingredient.tolist())))
    out["set"] = name
    out["units_graded"] = len(df)
    out["units_without_gold"] = dropped

    # CIRCULARITY. E2's gold NDC is `med_lexicon.NDC`, and the resolver's tier A
    # reads that same column to find the product. Grading one against the other
    # measures a join, and it measures it at 100.0%. The number is computed and
    # then SUPPRESSED rather than left out quietly, because a reader who does
    # not see the field cannot tell whether it was circular or just absent.
    out["product_circular"] = (name == "E2_LEXICON")
    out["product_circular_why"] = (
        "gold_ndc9 and the resolver's tier A read the same med_lexicon.NDC "
        "column; the comparison grades a join, not a resolution"
        if name == "E2_LEXICON" else None)

    # The worst rows, by row weight, so the error analysis comes before the
    # aggregate rather than after it.
    bad = [(float(r.row_weight), str(r.unit), str(r.gold_ingredient),
            preds[i].get("Ingredient"), preds[i].get("DrugKey"), confs[i])
           for i, r in enumerate(df.itertuples()) if not graded[i]["ingredient_exact"]]
    bad.sort(reverse=True)
    out["worst_misses"] = [
        {"row_weight": w, "input": u, "gold": g, "ours": o, "drugkey": k, "conf": c}
        for w, u, g, o, k, c in bad[:25]]
    return out


def bar(v, w=22):
    if v is None:
        return " " * w
    return ("█" * round(v * w)).ljust(w)


def render(runs, tag, at, head) -> str:
    L = ["# GOLD -- B2", "",
         "describe-medication against two independent answer keys. `CONTRACT.md`",
         "beside this file is the no-gold half of the scorecard; this is the half",
         "that needs one.", "",
         "GENERATED. Do not hand-edit. The producer is under git at",
         "`Tools/plugins/haipipe-utils/skills/describe-medication/benchmark/`.", "",
         "```bash", "source .venv/bin/activate && source env.sh",
         "python Tools/plugins/haipipe-utils/skills/describe-medication/"
         "benchmark/build_gold.py   # the ruler, once",
         "python Tools/plugins/haipipe-utils/skills/describe-medication/"
         "benchmark/run_bench.py    # the reading",
         "```", "",
         f"run `{tag}` · {at} · code at `{head}`", "",
         "", "## The two evaluation sets are not comparable, and that is the point", "",
         "```text",
         "  E1 MEPS      the dirty string is a PHARMACY's, truncated to 12 characters.",
         "               'LEVOTHYROXIN' · 'HYDROCHLOROT' · 'LANTUS SOLOS'",
         "               answer key: Multum Lexicon, a different organisation's",
         "               curation. Says whether the resolver is any good at all.",
         "",
         "  E2 LEXICON   the dirty string is a WellDoc MedicationID, an integer.",
         "               answer key: the generic inside WellDoc's own product name.",
         "               Says whether it handles the dialect it is pointed at.",
         "",
         "  MEPS holds no MedicationID. Our corpus holds no truncated pharmacy",
         "  string and no independent product key. Neither number replaces the other.",
         "```", ""]

    for r in runs:
        o = r["overall"]
        L += ["", f"## {r['set']}", "", "```text",
              f"  units graded          {r['units_graded']:,}"
              + (f"   ({r['units_without_gold']:,} have no gold yet and are NOT counted)"
                 if r["units_without_gold"] else ""),
              ""]
        L += [f"  distinct gold drugs   {r['n_distinct_gold_drugs']:,}"
              f"   (from {r['units_graded']:,} units -- one drug can carry many)", ""]
        for w in ("row", "type", "drug"):
            if w not in o:
                continue
            a = o[w]
            what = {"row": "every administration once -- DEPLOYMENT",
                    "type": "every distinct id/string once -- PRODUCT vocabulary",
                    "drug": "every distinct GOLD DRUG once -- DRUG vocabulary"}[w]
            L += [f"  {w:<5} weighted   {what}",
                  f"    coverage (Ingredient non-null)      {_p(a['coverage_ingredient'])}",
                  f"    coverage (DrugKey  non-null)        {_p(a['coverage_key'])}",
                  f"    ingredient exact, of ANSWERED       {_p(a['ingredient_exact_of_answered'])}",
                  f"    ingredient exact, of ALL            {_p(a['ingredient_exact_of_all'])}",
                  f"    ingredient F1,    of ANSWERED       {_p(a['ingredient_f1_of_answered'])}",
                  f"    DrugKey exact,    of ALL            {_p(a['drugkey_exact_of_all'])}",
                  ]
            if r.get("product_circular"):
                L += [f"    product NDC                         "
                      f"CIRCULAR, suppressed",
                      f"      why: {r['product_circular_why']}", ""]
            else:
                L += [f"    product NDC attempted, of gradeable {_p(a['product_coverage'])}"
                      f"   (n={a['n_product_gradeable']:,})",
                      f"    product NDC hit, of ATTEMPTED       {_p(a['product_hit_of_answered'])}", ""]
        L += ["```", "",
              "### risk-coverage, row-weighted", "",
              "Cumulative down the DECLARED confidence order. Accuracy must fall.", "",
              "```text",
              f"  {'through tier':<14}{'coverage':>10}{'ing exact':>11}  curve"]
        for p in r["curve"]["row"]:
            L.append(f"  {p['through_tier']:<14}{_p(p['coverage']):>10}"
                     f"{_p(p['ingredient_exact']):>11}  {bar(p['ingredient_exact'])}")
        mono = r.get("monotone", {}).get("row")
        L += ["```", "",
              ("✅ monotone: the ladder is ordered right, so MedConf is worth reading."
               if mono else
               "❌ NOT monotone: a lower tier beats a higher one. The ladder is "
               "mis-declared, and that is a one-line fix in constants.py, not a "
               "model problem."), ""]
        if r["worst_misses"]:
            L += ["### the misses that cost the most rows", "", "```text",
                  f"  {'rows':>7}  {'input':<26}{'gold':<28}{'ours':<24}conf"]
            for m in r["worst_misses"][:12]:
                L.append(f"  {int(m['row_weight']):>7}  {str(m['input'])[:25]:<26}"
                         f"{str(m['gold'])[:27]:<28}{str(m['ours'])[:23]:<24}{m['conf']}")
            L += ["```", ""]

    L += ["", "## What this cannot say", "",
          "```text",
          "  · Both keys are G2 -- DECLARED BY A SOURCE, not measured on a person.",
          "    Multum is a curated commercial database and WellDoc's product name",
          "    is a vendor export. Each is independent of the FDA Directory the",
          "    resolver reads, which is what makes them usable; neither is truth.",
          "  · 202 of 871 MedicationIDs have no gold in any tier. They are the",
          "    stratum a person must label, and they are excluded from E2 above.",
          "  · A formulation error scores as RIGHT at ingredient level by design.",
          "    Only the product row catches it. Read both.",
          "```", ""]
    return "\n".join(L) + "\n"


def _p(v):
    return "     -" if v is None else f"{v:6.1%}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", dest="only", choices=["E1_ALL", "E2_LEXICON"])
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--tag", default=None)
    a = ap.parse_args()

    at = datetime.datetime.now().isoformat(timespec="seconds")
    tag = a.tag or at[:10].replace("-", "")[2:]
    head = git_head()

    # <corpus>/<SET_ID>.parquet -- the folder says where the answer came from
    # and the file name says which evaluation set it is, so one source feeding
    # several sets needs no naming convention beyond the two.
    sets = {"E1_ALL": CORPUS / "MEPS" / "E1_ALL.parquet",
            "E2_LEXICON": CORPUS / "WellDoc" / "E2_LEXICON.parquet"}
    runs = []
    for name, path in sets.items():
        if a.only and name != a.only:
            continue
        print(f"  grading {name} ...", flush=True)
        runs.append(run_set(name, pd.read_parquet(path), a.n))

    (DEST / "runs").mkdir(parents=True, exist_ok=True)
    payload = {"bench": "B2_gold", "tag": tag, "at": at, "git_head": head,
               "noun": "medication", "sets": runs}
    (DEST / "runs" / f"{tag}-gold-medication.json").write_text(
        json.dumps(payload, indent=1, default=str) + "\n")
    (DEST / "_gold.json").write_text(json.dumps(
        {"bench": "B2_gold", "tag": tag, "at": at, "git_head": head,
         "sets": {r["set"]: {"units": r["units_graded"],
                             "drugs": r.get("n_distinct_gold_drugs"),
                             "row": r["overall"]["row"],
                             "drug": r["overall"].get("drug"),
                             "monotone": r.get("monotone")} for r in runs}},
        indent=1, default=str) + "\n")
    (DEST / "GOLD.md").write_text(render(runs, tag, at, head))

    for r in runs:
        o = r["overall"]["row"]
        print(f"\n  {r['set']}  units={r['units_graded']:,}")
        print(f"    coverage {_p(o['coverage_ingredient'])} · "
              f"ing exact(all) {_p(o['ingredient_exact_of_all'])} · "
              f"ing exact(answered) {_p(o['ingredient_exact_of_answered'])} · "
              + ("NDC circular · " if r.get("product_circular") else
                 f"NDC att {_p(o['product_coverage'])} hit {_p(o['product_hit_of_answered'])} · ")
              + f"monotone {r.get('monotone', {}).get('row')}")
    print(f"\n  wrote {DEST}")


if __name__ == "__main__":
    main()
