"""
Build a USDA bank with one data_type REMOVED, so a public dataset can be
evaluated without the door retrieving the answer sheet.

WHY
================================================================================
The first FNDDS run reported MAE 0.31 g of carbohydrate with a MEDIAN ABSOLUTE
ERROR OF 0.00 and r = 0.99. That is not a good model, it is a JOIN: our USDA
bank ships `survey_fndds_food`, 5,432 rows, one per FNDDS food code. The door
was handed an FNDDS description and looked up the FNDDS row.

A median of exactly zero is the tell. Any benchmark whose reference is also in
the system's own reference bank measures retrieval and reports generalisation --
the failure `arXiv:2605.20537` names as identifier overlap.

    python build_holdout_db.py --exclude survey_fndds_food

The result keeps the other 95,783 foods, so the question becomes the real one:
given an FNDDS description, can the door find the right food among SR Legacy,
Foundation, Branded and the sample foods?
"""
import argparse
import pathlib
import shutil
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve()
SKILL = HERE.parent.parent
ROOT = SKILL.parents[4]
SRC = ROOT / ("_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/3-reference/"
              "usda_fdc/usda_nutrition.sqlite")
OUT_DIR = ROOT / ("_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/6-benchmark/"
                  "bank_usda_holdout")


def build(exclude: str) -> pathlib.Path:
    out = OUT_DIR / f"usda_no_{exclude}.sqlite"
    if out.exists():
        return out
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SRC, out)
    c = sqlite3.connect(out)
    before = c.execute("SELECT count(*) FROM food").fetchone()[0]
    n = c.execute("SELECT count(*) FROM food WHERE data_type = ?",
                  (exclude,)).fetchone()[0]
    if n == 0:
        sys.exit(f"data_type {exclude!r} not present; nothing to hold out")
    c.execute("DELETE FROM food WHERE data_type = ?", (exclude,))
    # food_fts is an EXTERNAL-CONTENT fts5 table over `food`. Deleting from the
    # content table leaves the index stale, so a held-out row would still be
    # findable by search and the holdout would be a fiction.
    c.execute("INSERT INTO food_fts(food_fts) VALUES('rebuild')")
    c.commit()
    after = c.execute("SELECT count(*) FROM food").fetchone()[0]
    hits = c.execute("SELECT count(*) FROM food_fts").fetchone()[0]
    c.execute("VACUUM")
    c.close()
    print(f"  {SRC.name}: {before:,} rows")
    print(f"  removed {n:,} of data_type {exclude!r}")
    print(f"  -> {after:,} rows, FTS rebuilt to {hits:,} documents")
    print(f"  -> {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--exclude", default="survey_fndds_food")
    build(ap.parse_args().exclude)
