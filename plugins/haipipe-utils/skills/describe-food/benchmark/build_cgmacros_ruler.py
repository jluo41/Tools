#!/usr/bin/env python3
"""
The one L1-grade nutrition ruler on this board, and the only one the TEXT door
can never reach.

WHY IT EXISTS
================================================================================
`2-corpus/README.md` ends on a measurement: five corpora of our own and not one
can grade the door on nutrition. Three name no food, Shanghai's macros were
written BY the door, and WellDoc shares an upstream vendor with its own bank.

CGMacros is the exception hiding inside that sentence. Its 1,437 gradeable meals
carry five macros from a STUDY KITCHEN -- weighed and computed by the people who
served the food, agreeing with each other under Atwater. That is the only
laboratory-grade nutrition truth anywhere near this project, and every other
ruler here is a third-party ESTIMATE.

It is unreachable because CGMacros writes the literal string 'Unknown' in
FoodName on all 1,644 rows and puts the meal in a PHOTO. Its `units.parquet`
reads 1 unit, 100% refused, and that reading is correct: the text door is right
to say nothing about a photo.

So this ruler is graded through STAGE 0. `imagename.read_images` turns the
photos into a name, the name enters the ordinary dialect -> retrieve -> aggregate
path, and what comes out is compared to the kitchen. The seam is the point: a
derived name is scored by the machinery that already exists.

    baseline    the text door on the same rows: 0 of them resolvable.
                `CGMacros/units.parquet` already records it. That is the number
                this ruler is measured against, and it is a real zero.

SCOPE, AND WHAT IS LEFT OUT AND WHY
================================================================================
Only rows with `AmountConsumed == 100`. The column is not a clean percentage --
it also holds 1.0, 200.0 and 300.0 -- so on the other rows it is not knowable
whether the macros describe the plate in the photo or some multiple of it.
Grading those would measure that column, not the food.

TWO PHOTOS PER MEAL IS NOT A MISTAKE. 1,177 of these meals ship a BEFORE and an
AFTER frame. Both go to the engine, which is what lets a model see what was left.

AUTH IS OAUTH, NEVER AN API KEY -- `imagename.claude_engine` shells out to the
`claude` CLI and strips the three key variables from the subprocess.

EVERY NAME IS BANKED. `_names_book.json` beside the ruler is a replay book, so
every later fix -- a different bank, a corrected filter, a calibration -- is free.
The model call is the expensive part and the least likely thing to need redoing.

    source .venv/bin/activate && source env.sh
    python build_cgmacros_ruler.py --n 120        # a priced slice first
    python build_cgmacros_ruler.py                # all of them
    python build_cgmacros_ruler.py --replay       # re-score, no model calls
"""
import argparse
import glob
import json
import os
import pathlib
import sys

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

ROOT = pathlib.Path("/home/jluo41/WellDoc-SPACE")
PHOTOS = ROOT / "_WorkSpace/0-RawDataStore/CGMacros/Source"
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"
FOLDER = INFO / "2-corpus/CGMacros"
BOOK = FOLDER / "_names_book.json"
RULER = "E4_CGMACROS"

NUTRIENTS = ("Calories", "Carbs", "Protein", "Fat", "Fiber")


def load():
    """The gradeable, unambiguous slice, with absolute image paths."""
    from taxonomy import classify_label
    f = sorted(glob.glob(str(ROOT / "_WorkSpace/1-SourceStore/CGMacros/@*/Diet.parquet")))[0]
    d = pd.read_parquet(f)
    d["PatientID"] = d.PatientID.astype(str)
    d["label"] = [classify_label(r) for _, r in d.iterrows()]
    d = d[(d.label == "gold_macros") & (d.AmountConsumed == 100)]

    # A DEGENERATE GOLD THAT PASSES THE ATWATER CHECK BY ACCIDENT.
    # `classify_label` calls a row gold_macros when kcal ~= 4C + 4P + 9F. A row
    # with P = F = 0 satisfies that whenever kcal ~= 4C, so a carb-only entry on
    # a carb-only food is admitted as five measured macros. 30 of CGMacros' 1,437
    # gradeable rows are like this, all small (mean 95 kcal), and one of them is
    # a photographed plate of chicken curry, rice, mashed potato and vegetables
    # logged at 80 kcal / 18 g carb / 0 protein / 0 fat. The photo is right and
    # the label is not. Found by eye on the first 30-meal slice, 260822.
    d = d[~((d.Protein == 0) & (d.Fat == 0))].reset_index(drop=True)

    paths = []
    for pid, ip in zip(d.PatientID, d.ImagePath.astype(str)):
        ps = [str(PHOTOS / pid / p.strip()) for p in ip.split(",") if p.strip()]
        paths.append([p for p in ps if os.path.exists(p)])
    d["paths"] = paths
    return d[d.paths.map(len) > 0].reset_index(drop=True)


def read_names(d, replay, model, batch):
    """Names from the book where they exist, from the engine where they do not."""
    from foodnorm.imagename import read_images

    book = json.loads(BOOK.read_text()) if BOOK.exists() else {}
    keys = ["\n".join(p) for p in d.paths]
    todo = [i for i, k in enumerate(keys) if k not in book]
    print(f"  {len(keys) - len(todo):,d} of {len(keys):,d} meals already in the book")

    if todo and not replay:
        reads = read_images([d.paths[i] for i in todo], engine="claude",
                            model=model, batch=batch, verbose=True)
        for i, r in zip(todo, reads):
            if r is not None:
                book[keys[i]] = dict(foods=r.food_name, conf=r.conf,
                                     engine=r.engine)
        BOOK.write_text(json.dumps(book, indent=1, ensure_ascii=False))
        print(f"  banked {len(book):,d} names in {BOOK.name}")
    elif todo:
        print(f"  --replay: {len(todo):,d} meals have no banked name, skipped")

    got = [book.get(k) for k in keys]
    d = d.assign(
        name=[g["foods"] if g else None for g in got],
        name_conf=[g["conf"] if g else np.nan for g in got],
        name_engine=[g["engine"] if g else None for g in got])
    return d[d.name.notna()].reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None, help="cap the meals read")
    ap.add_argument("--replay", action="store_true",
                    help="score banked names only; make no model call")
    ap.add_argument("--model", default=None)
    ap.add_argument("--batch", type=int, default=None)
    a = ap.parse_args()

    d = load()
    print(f"CGMacros: {len(d):,d} gradeable meals at AmountConsumed == 100")
    if a.n:
        d = d.head(a.n).copy()
        print(f"  capped to {len(d):,d}")

    d = read_names(d, a.replay, a.model, a.batch)
    if not len(d):
        sys.exit("no names available; drop --replay to buy them")
    print(f"  {len(d):,d} meals carry a derived name")

    from foodnorm import normalize
    res = pd.DataFrame(normalize(d.name.tolist()))

    u = pd.DataFrame({
        "unit": [pathlib.Path(p[0]).stem for p in d.paths],
        "unit_text": d.name.values,
        "kind": "photo",
        "row_weight": 1,
        "n_rows": 1,
        "n_patients": 1,
        "n_cohorts": 1,
        "grams_stated_n": 0,
        "n_frames": d.paths.map(len).values,
        "name_conf": d.name_conf.values,
        "name_engine": d.name_engine.values,
        "resolved_conf": res.NutritionConf.values,
        "resolved_source": res.NutritionSource.values,
        "resolved_basis": res.NutritionBasis.values,
        "resolved_name": res.FoodNameResolved.values,
    })
    for n in NUTRIENTS:
        u["resolved_" + n] = pd.to_numeric(res[n], errors="coerce").values
        u["gold_" + n] = pd.to_numeric(d[n], errors="coerce").values

    u["verdict"] = np.where(u.resolved_conf == "MEASURED", "measured",
                            np.where(u.resolved_conf == "ESTIMATED",
                                     "estimated", "gap"))
    u["gold_n"] = 1
    u["gold_basis"] = "per_meal"
    u["gold_tier"] = "G1"
    u["gold_source"] = ("CGMacros study kitchen -- weighed and computed by the "
                        "people who served the meal")
    u["gold_circular"] = False
    u["bank_config"] = "production"
    u["corpus"] = "CGMacros"
    u["unit_is_a"] = "photographed_meal"
    u.to_parquet(FOLDER / f"{RULER}.parquet", index=False)

    # ── the reading ──────────────────────────────────────────────────────────
    print(f"\n  {'nutrient':<10}{'n':>6}{'MAE':>9}{'median':>9}{'bias':>9}{'r':>7}")
    print("  " + "-" * 50)
    reading = {}
    for n in NUTRIENTS:
        p, g = u["resolved_" + n], u["gold_" + n]
        ok = p.notna() & g.notna()
        if ok.sum() < 5:
            continue
        e = (p[ok] - g[ok])
        r = float(np.corrcoef(p[ok], g[ok])[0, 1]) if ok.sum() > 2 else np.nan
        reading[n] = dict(n=int(ok.sum()), mae=round(float(e.abs().mean()), 2),
                          median=round(float(e.abs().median()), 2),
                          bias=round(float(e.mean()), 2), r=round(r, 3))
        print(f"  {n:<10}{ok.sum():>6,d}{reading[n]['mae']:>9.2f}"
              f"{reading[n]['median']:>9.2f}{reading[n]['bias']:>9.2f}"
              f"{reading[n]['r']:>7.2f}")

    shares = u.verdict.value_counts(normalize=True).round(4).to_dict()
    stat = json.loads((FOLDER / "_stat.json").read_text())
    stat["rulers"] = [RULER]
    stat["photo_ruler"] = dict(
        meals=int(len(u)), gold_tier="G1", scope="AmountConsumed == 100",
        engine=str(u.name_engine.iloc[0]), verdict_share=shares,
        baseline="text door on the same rows: 0 resolvable",
        reading=reading)
    (FOLDER / "_stat.json").write_text(json.dumps(stat, indent=1))

    rp = FOLDER / "README.md"
    t = rp.read_text().split("\n## ")[0].rstrip() + "\n"
    t = t.replace("  rulers          --", f"  rulers          {RULER}")
    rows = "\n".join(
        f"  {n:<10}{v['n']:>6,d}{v['mae']:>10.1f}{v['median']:>9.1f}"
        f"{v['bias']:>9.1f}{v['r']:>7.2f}" for n, v in reading.items())
    t += NOTE.format(ruler=RULER, meals=len(u), rows=rows,
                     engine=u.name_engine.iloc[0],
                     meas=shares.get("measured", 0), est=shares.get("estimated", 0),
                     gap=shares.get("gap", 0))
    rp.write_text(t)
    print(f"\n  wrote {FOLDER / (RULER + '.parquet')}")


NOTE = """

## `{ruler}.parquet` -- the ruler the TEXT door cannot reach

The block above is a true reading of the text door and it is a real zero: this
corpus names no food, so the door correctly says nothing about all of it.

The meal is in the PHOTO. Sending it through STAGE 0 first -- `imagename` turns
the frames into a name, the name enters the ordinary dialect -> retrieve ->
aggregate path -- makes these rows gradeable, and against the only L1 gold on
the board: a study kitchen weighed and computed them.

```text
  engine    {engine}
  scope     AmountConsumed == 100 only. The column also holds 1.0, 200.0 and
            300.0, and on those rows it is not knowable whether the macros
            describe the plate in the photo or a multiple of it.
            MINUS 30 rows with protein = 0 AND fat = 0: those satisfy the
            Atwater check whenever kcal ~= 4C, so a carb-only entry is admitted
            as five measured macros. One is a full curry plate logged at 80 kcal.
  meals     {meals:,d}
  baseline  the text door on these same rows: 0 resolvable

  after stage 0     measured {meas:.1%}   estimated {est:.1%}   gap {gap:.1%}

  nutrient       n       MAE   median     bias      r
  ────────────────────────────────────────────────────
{rows}
```

`bias` is signed on purpose. A model that names a plate it can see is not
symmetric about the truth, and which way it leans is the finding, not the MAE.

`_names_book.json` banks every name this cost. Re-score with `--replay` and the
model is never called again.
"""


if __name__ == "__main__":
    main()
