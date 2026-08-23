"""
Parse the Open Food Facts dump into a BRANDED-food benchmark.

WHY BRANDED FOODS DESERVE THEIR OWN CELL
================================================================================
USDA is strongest on generic foods and weakest on brands, and the weakness is
not random -- it is the single worst error available to a CGM project:

    'Pepsi (12 oz)'    USDA fuzzy match -> 0.00 g carbohydrate, labelled GOOD
                       actually logged  -> 41 g

A sugary drink read as zero carbohydrate is also the sharpest glucose excursion
there is. Our observed bank exists because of exactly this failure, and it fixes
it only for names OUR patients happened to log. Open Food Facts is the public
reference that tests the same lane on 3 million products nobody here logged.

STREAMED, NEVER EXTRACTED
================================================================================
The dump is 1.2 GB gzipped and about 10 GB as CSV; the root filesystem has 206
GB free and is 88% full. So this reads the gzip in chunks, keeps eight columns,
drops every row without a name or a full macro set, and writes a parquet. The
CSV is never materialised.

    python build_openfoodfacts.py [--max-rows N]
"""
import argparse
import gzip
import pathlib

import pandas as pd

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[6]
D = ROOT / "_WorkSpace/ExternalStore/openfoodfacts"
SRC = D / "products.csv.gz"

COLS = ["code", "product_name", "brands", "countries_en",
        "energy-kcal_100g", "carbohydrates_100g", "proteins_100g",
        "fat_100g", "fiber_100g"]
REN = {"energy-kcal_100g": "Calories", "carbohydrates_100g": "Carbs",
       "proteins_100g": "Protein", "fat_100g": "Fat", "fiber_100g": "Fiber"}
MACROS = list(REN.values())

# A product whose macros do not reconstruct its own energy is a bad row, not
# evidence. Same Atwater rule the observed bank uses, same tolerance.
ATWATER_TOL = 0.25


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-rows", type=int, default=0)
    a = ap.parse_args()

    keep, seen = [], 0
    with gzip.open(SRC, "rt", encoding="utf-8", errors="replace") as fh:
        for chunk in pd.read_csv(fh, sep="\t", usecols=COLS, chunksize=200_000,
                                 low_memory=False, on_bad_lines="skip"):
            seen += len(chunk)
            c = chunk.rename(columns=REN)
            # A barcode is an IDENTIFIER, never arithmetic, and some are wider
            # than int64. Store it as text or the parquet write overflows.
            c["code"] = c["code"].astype(str)
            c = c[c["product_name"].notna()]
            c["product_name"] = c["product_name"].astype(str).str.strip()
            c = c[c["product_name"].str.len().between(2, 120)]
            for m in MACROS:
                c[m] = pd.to_numeric(c[m], errors="coerce")
            c = c.dropna(subset=MACROS)
            # Per 100 g, so nothing may exceed 100 g of a macro or 900 kcal.
            c = c[(c[["Carbs", "Protein", "Fat", "Fiber"]].ge(0).all(axis=1))
                  & (c[["Carbs", "Protein", "Fat", "Fiber"]].le(100).all(axis=1))
                  & c["Calories"].between(0, 900)]
            at = 4 * c["Carbs"] + 4 * c["Protein"] + 9 * c["Fat"]
            ok = c["Calories"].le(0) | ((at - c["Calories"]).abs()
                                        / c["Calories"].clip(lower=1) < ATWATER_TOL)
            keep.append(c[ok])
            if a.max_rows and sum(len(k) for k in keep) >= a.max_rows:
                break
            print(f"  read {seen:,}  kept {sum(len(k) for k in keep):,}", end="\r")

    off = pd.concat(keep, ignore_index=True).drop_duplicates(subset=["product_name"])
    off.to_parquet(D / "off_product.parquet", index=False)

    us = off[off["countries_en"].astype(str).str.contains("United States", na=False)]
    (D / "PROVENANCE.md").write_text(
        "# Open Food Facts\n\n"
        "Collaborative open database of packaged food products. ODbL v1.0.\n\n"
        "```text\n"
        f"  off_product.parquet   {len(off):,} products, one row per distinct name\n"
        "                        name + brand + 5 macros PER 100 g\n"
        f"                        of which United States: {len(us):,}\n"
        "```\n\n"
        "Downloaded 2026-08-22 from\n"
        "`https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz`\n\n"
        f"Filtered from {seen:,} raw rows: a usable name, all five macros present,\n"
        "within per-100 g bounds, and Atwater-consistent within 25%.\n\n"
        "WHAT IT IS: crowd-sourced label transcription -- what the PACKAGE says.\n"
        "WHAT IT IS NOT: an assay, and not a curated compilation the way FNDDS is.\n"
        "It is a strong reference for BRAND IDENTITY and a weak one for absolute\n"
        "nutrient truth. Score the branded lane with it; do not merge it with FNDDS.\n",
        encoding="utf-8")

    print(f"\nraw rows read {seen:,}")
    print(f"kept          {len(off):,} distinct products   (US: {len(us):,})")
    print(f"-> {D/'off_product.parquet'}")
    print(off.head(5)[["product_name", "brands", "Calories", "Carbs"]].to_string(index=False))


if __name__ == "__main__":
    main()
