"""
Score the text door against PUBLIC datasets whose reference nobody in this
project produced.

    python eval_public.py fndds        --n 2000
    python eval_public.py fndds --joined          # the leaky run, for contrast
    python eval_public.py nutrition5k  --n 2000
    python eval_public.py openfoodfacts --n 5000
    python eval_public.py both

WHY THESE TWO AND WHY THEY ARE SCORED APART
================================================================================
    FNDDS         a USDA food DESCRIPTION -> 5 macros PER 100 g
                  both sides per 100 g, so absolute MAE needs no portion
                  ▶ answers: can the door find the right food?

    Nutrition5k   a plate replayed as 'name GRAMS g' lines -> the plate's totals
                  the grams were WEIGHED, the per-gram macros are USDA
                  ▶ answers: given a real portion, is the total right?

Merging them would average a per-100g question with a per-plate question. They
are different tasks that happen to share a unit.

THE BANK MUST NOT CONTAIN THE ANSWER SHEET
================================================================================
Our USDA bank ships `survey_fndds_food`, 5,432 rows -- one per FNDDS food code.
The first run of this file reported carbohydrate MAE 0.31 g with a MEDIAN
ABSOLUTE ERROR OF 0.00 and r = 0.99, which is not a model, it is a self-join.
So the fndds lane runs against a bank with that data_type REMOVED (see
build_holdout_db.py). `--joined` reproduces the leaky number on purpose,
because the contrast between the two is the actual finding.

Nutrition5k has a WEAKER version of the same issue and it is not removable: the
dataset's per-gram macros were themselves taken from USDA, so a USDA-backed
door and this reference agree on density by construction. What is independent
there is the MASS, weighed on a scale. That is what the lane really tests --
decomposition, gram handling, and summation over a real portion.

BASIS IS NOT A DETAIL
================================================================================
The door may answer on per_100g, per_meal or per_serving. A per_serving answer
cannot be compared with a per-100 g truth -- that comparison measures serving
size. Rows are therefore bucketed by NutritionBasis and a bucket that cannot be
compared is REPORTED AS SUCH, never folded into the headline.
"""
import argparse
import datetime
import json
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve()
SKILL = HERE.parent.parent
ROOT = SKILL.parents[4]
sys.path.insert(0, str(SKILL))

# NUTRIENTS is a constant; `normalize` is imported INSIDE main(), after
# FOODNORM_DB has been set. constants.py reads that env var at import time, so
# importing the package up here would pin the full bank and silently undo the
# holdout.
NUTRIENTS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")

EXT = ROOT / "_WorkSpace/ExternalStore"
RUNS = ROOT / ("_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/6-benchmark/runs")


def _stats(truth, pred):
    m = truth.notna() & pred.notna()
    if m.sum() < 3:
        return {"n": int(m.sum())}
    t, p = truth[m].astype(float), pred[m].astype(float)
    return {
        "n": int(m.sum()),
        "MAE": round(float(np.abs(t - p).mean()), 3),
        "median_AE": round(float(np.abs(t - p).median()), 3),
        "r": round(float(np.corrcoef(t, p)[0, 1]), 4) if t.std() and p.std() else None,
        "bias": round(float((p - t).mean()), 3),
    }


def _score(df, texts, label, nutrients=NUTRIENTS):
    from foodnorm import normalize
    out = pd.DataFrame(normalize(list(texts)))
    for c in nutrients:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    res = {
        "dataset": label,
        "n_rows": int(len(df)),
        "coverage": round(float(out["NutritionConf"].ne("MISS").mean()), 4),
        "conf": {k: int(v) for k, v in out["NutritionConf"].value_counts().items()},
        "basis": {str(k): int(v) for k, v in
                  out["NutritionBasis"].fillna("none").value_counts().items()},
        "graded_nutrients": list(nutrients),
        "source": {str(k): int(v) for k, v in
                   out["NutritionSource"].fillna("none").value_counts().items()},
        "by_basis": {},
        "by_source": {},
    }
    for basis, idx in out.groupby(out["NutritionBasis"].fillna("none")).groups.items():
        cell = {}
        for n in nutrients:
            cell[n] = _stats(df[n].reset_index(drop=True).loc[idx],
                             out[n].loc[idx])
        res["by_basis"][str(basis)] = cell
    # WHICH TIER answered matters most on branded food: T0 (the observed bank)
    # exists precisely because USDA reads a sugary drink as zero carbohydrate.
    for src, idx in out.groupby(out["NutritionSource"].fillna("none")).groups.items():
        res["by_source"][str(src)] = {n: _stats(
            df[n].reset_index(drop=True).loc[idx], out[n].loc[idx])
            for n in nutrients}
    return res, out


def run_fndds(n, joined):
    f = pd.read_parquet(EXT / "fndds_2021_2023/fndds_food.parquet")
    f = f.dropna(subset=list(NUTRIENTS))
    if n and n < len(f):
        f = f.sample(n, random_state=17).reset_index(drop=True)
    res, _ = _score(f, f["description"], "fndds_2021_2023")
    res["truth_basis"] = "per_100g"
    res["comparable_basis"] = "per_100g"
    res["bank"] = "FULL (survey_fndds_food INCLUDED -- self-join)" if joined \
        else "survey_fndds_food HELD OUT"
    res["note"] = ("descriptions written by trained coders, not typed by patients. "
                   "capability, not deployment.")
    return res


# Nutrition5k records calories, fat, carb, protein. It has NO fibre column, so
# fibre is not gradeable here and is not silently scored as zero.
N5K_NUTRIENTS = ("Calories", "Carbs", "Protein", "Fat")


def run_n5k(n):
    d = pd.read_parquet(EXT / "nutrition5k/n5k_dish.parquet")
    d = d.dropna(subset=list(N5K_NUTRIENTS))
    if n and n < len(d):
        d = d.sample(n, random_state=17).reset_index(drop=True)
    res, _ = _score(d, d["text"], "nutrition5k", N5K_NUTRIENTS)
    res["truth_basis"] = "per_dish (component masses WEIGHED)"
    res["comparable_basis"] = "per_meal"
    res["note"] = ("grams measured on a scale; per-gram macros are USDA. "
                   "portion is real, density is estimated. no fibre column.")
    return res


def run_off(n):
    """Branded packaged food. US subset only: the dump is multilingual and the
    door, like USDA, reads English. Scoring a French product name would measure
    language, not food resolution."""
    o = pd.read_parquet(EXT / "openfoodfacts/off_product.parquet")
    o = o[o["countries_en"].astype(str).str.contains("United States", na=False)]
    o = o.dropna(subset=list(NUTRIENTS)).reset_index(drop=True)
    if n and n < len(o):
        o = o.sample(n, random_state=17).reset_index(drop=True)
    res, _ = _score(o, o["product_name"], "openfoodfacts_us")
    res["truth_basis"] = "per_100g"
    res["comparable_basis"] = "per_100g"
    res["note"] = ("crowd-sourced label transcription -- what the PACKAGE says. "
                   "strong on brand identity, weak on absolute nutrient truth.")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["fndds", "nutrition5k",
                                      "openfoodfacts", "both", "all"])
    ap.add_argument("--n", type=int, default=2000)
    ap.add_argument("--tag", default="public")
    ap.add_argument("--joined", action="store_true",
                    help="fndds: use the FULL bank, reproducing the self-join")
    a = ap.parse_args()

    if not a.joined and a.which in ("fndds", "both"):
        sys.path.insert(0, str(HERE.parent))
        from build_holdout_db import build
        db = build("survey_fndds_food")
        import os
        os.environ["FOODNORM_DB"] = str(db)
        print(f"FOODNORM_DB -> {db.name}")

    todo = {"both": ["fndds", "nutrition5k"],
            "all": ["fndds", "nutrition5k", "openfoodfacts"]}.get(a.which, [a.which])
    runs = []
    for w in todo:
        r = {"fndds": lambda: run_fndds(a.n, a.joined),
             "nutrition5k": lambda: run_n5k(a.n),
             "openfoodfacts": lambda: run_off(a.n)}[w]()
        runs.append(r)
        print(f"\n=== {r['dataset']}   n={r['n_rows']:,}   "
              f"coverage {r['coverage']:.1%}")
        if r.get("bank"):
            print(f"    bank  {r['bank']}")
        print(f"    conf  {r['conf']}")
        print(f"    basis {r['basis']}")
        comp = r["comparable_basis"]
        cell = r["by_basis"].get(comp)
        if not cell:
            print(f"    !! no rows answered on {comp}; nothing comparable")
            continue
        print(f"    --- on {comp} (the only comparable basis) ---")
        for nut in r["graded_nutrients"]:
            s = cell[nut]
            if "MAE" not in s:
                print(f"      {nut:<9} n={s['n']}  too few")
                continue
            print(f"      {nut:<9} n={s['n']:>5}  MAE {s['MAE']:>8.2f}  "
                  f"med {s['median_AE']:>7.2f}  r {s['r']}  bias {s['bias']:>8.2f}")

    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.date.today().strftime("%y%m%d")
    out = RUNS / f"{stamp}-{a.tag}.json"
    out.write_text(json.dumps(
        {"metric": "CLOSE (public reference)",
         "ran_at": datetime.datetime.now().isoformat(timespec="seconds"),
         "runs": runs}, indent=2) + "\n")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
