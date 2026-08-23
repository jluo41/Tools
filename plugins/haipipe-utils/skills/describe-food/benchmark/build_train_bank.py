"""
Rebuild the observed bank from the TRAIN patients only.

WHY THIS FILE EXISTS
================================================================================
The observed bank was built FROM this corpus. Scoring an eval row whose name is
already in the bank measures a JOIN, not a prediction -- the number comes back
because the row itself put it there. Measured on the full bank, 97.1% of eval
names were already present.

The literature has a name for this. `arXiv:2605.20537` measures train/test
overlap at four levels -- token vocabulary, mention tokens, exact mention
strings, concept identifiers -- and its point is that high identifier overlap
means a benchmark scores memorisation while reporting generalisation. Our leak
is exactly its third level.

THE FIX IS NOT TO FORBID OVERLAP
================================================================================
In deployment the bank DOES contain names other patients logged. Forbidding
that would measure a system nobody runs. So this rebuilds the bank without the
EVAL PATIENTS' OWN ROWS, which is the honest deployment simulation, and the
scorer then reports two cells that must never be merged:

    seen     the eval name is in the train bank   -> retrieval
    unseen   it is not                            -> generalisation

Two raw cohorts contribute to the bank and appear in NO corpus row --
WellDoc2023CVSDeRx (55 patients) and WellDoc2023CVSTDC (924) -- so their names
are train by construction and leak nothing.

    python build_train_bank.py
"""
import glob
import hashlib
import json
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve()
SKILL = HERE.parent.parent
ROOT = SKILL.parents[4]
sys.path.insert(0, str(ROOT / "code/scripts/haibuilder/0-external"))

from e14_build_external_foodbank_observed import build_bank   # noqa: E402

XINFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"
GOLD = XINFO / "2-corpus/gold_index.parquet"
OUT = XINFO / "6-benchmark/bank_train"
RAW = str(ROOT / "_WorkSpace/0-RawDataStore/WellDoc*/Source/*ELogFoodItem.csv")

# Must match build_gold.py EXACTLY. A different hash here silently puts eval
# patients back into the bank, which is the defect this file exists to remove.
TEST_FRACTION = 0.30


def split_of(patient_id):
    h = hashlib.sha256(str(patient_id).encode()).hexdigest()
    return "test" if (int(h[:8], 16) % 1000) < TEST_FRACTION * 1000 else "train"


def main():
    gold = pd.read_parquet(GOLD)
    # cohort -> the cooked PatientID prefix. Verified 100% reconstructable for
    # every cohort that has both raw food items and corpus rows.
    prefix = {}
    for c, sub in gold.groupby("cohort"):
        pres = {str(i).rsplit("-", 1)[0] for i in sub.PatientID.dropna().astype(str)
                if "-" in str(i)}
        if len(pres) == 1:
            prefix[c] = pres.pop()

    files = sorted(glob.glob(RAW))
    frames, report = [], []
    for f in files:
        cohort = pathlib.Path(f).parts[-3]
        d = pd.read_csv(f, low_memory=False)
        if len(d) == 0:
            continue
        p = prefix.get(cohort)
        if p is None:
            # No corpus row can ever come from this cohort, so nothing it
            # contributes can leak. Keep all of it.
            d["_split"] = "train"
            note = "not in corpus -> all train"
        else:
            cooked = p + "-" + d["PatientID"].astype("Int64").astype(str)
            d["_split"] = cooked.map(split_of)
            note = f"{(d._split == 'train').mean():.1%} train"
        report.append((cohort, len(d), note))
        frames.append(d)

    fi = pd.concat(frames, ignore_index=True)
    print(f"{len(fi):,} raw items from {len(files)} files")
    for c, n, note in report:
        print(f"  {c:<20} {n:>8,}   {note}")

    train = fi[fi["_split"] == "train"].drop(columns=["_split"])
    print(f"\ntrain rows {len(train):,}  ({len(train)/len(fi):.1%})")

    bank = build_bank(train.copy())
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "observed_food.parquet"
    bank.to_parquet(path, index=False)

    full = pd.read_parquet(ROOT / "_WorkSpace/ExternalStore/foodbank_observed"
                                  "/observed_food.parquet")
    stats = {
        "entries_full_bank": int(len(full)),
        "entries_train_bank": int(len(bank)),
        "entries_dropped": int(len(full) - len(bank)),
        "records_covered": int(bank["n"].sum()),
        "test_fraction": TEST_FRACTION,
        "basis": "per_serving",
        "built_from": "train patients only; see module docstring",
    }
    (OUT / "_stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(f"\n-> {path}")
    print(f"   full bank  {len(full):>7,} entries")
    print(f"   train bank {len(bank):>7,} entries   "
          f"({len(bank)/len(full):.1%}, {len(full)-len(bank):,} withheld)")


if __name__ == "__main__":
    main()
