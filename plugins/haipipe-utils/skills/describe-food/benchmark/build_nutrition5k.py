"""
Parse Nutrition5k dish metadata into a benchmark corpus for the TEXT door.

WHY A VISION DATASET IS THE BEST TEXT BENCHMARK WE HAVE
================================================================================
Nutrition5k was built for image models, but its ground truth was collected by
weighing every component of every plate on a scale. Each dish is therefore a
list of (ingredient name, MEASURED grams) -- which is exactly the shape of
Shanghai's `newline_grams` dialect, the one dialect our door already handles
end to end:

    'soy sauce 3.4 g; garlic 2.1 g; white rice 8.5 g; ...'

So the plate can be replayed as a STRING, and the answer compared against
numbers no food app produced.

HOW MUCH OF IT IS ACTUALLY MEASURED -- BE PRECISE
================================================================================
    the MASS of each component        weighed on a scale        MEASURED
    the macros per gram               USDA, via the dataset's   ESTIMATED
                                      ingredients_metadata.csv

That is not a full L1 label. But the portion is real, and portion is the exact
thing that has blocked absolute MAE on our own corpus, where ten of eleven
cohorts state no portion at all. A reference whose masses are weighed is a
strictly better instrument than one whose masses are guessed.

    python build_nutrition5k.py
"""
import csv
import pathlib
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve()
ROOT = HERE.parents[6]
D = ROOT / "_WorkSpace/ExternalStore/nutrition5k"

# dish_id, cal, mass, fat, carb, protein, then 7-tuples per ingredient.
HEAD = 6
STRIDE = 7


def main():
    files = sorted(D.glob("dish_metadata_cafe*.csv"))
    if not files:
        sys.exit(f"no dish_metadata_cafe*.csv under {D}")

    dishes, items = [], []
    for f in files:
        cafe = f.stem.replace("dish_metadata_", "")
        for row in csv.reader(open(f)):
            if len(row) < HEAD:
                continue
            did = row[0]
            try:
                cal, mass, fat, carb, prot = (float(x) for x in row[1:HEAD])
            except ValueError:
                continue
            rest = row[HEAD:]
            n = len(rest) // STRIDE
            comps = []
            for i in range(n):
                c = rest[i * STRIDE:(i + 1) * STRIDE]
                if len(c) < STRIDE:
                    break
                try:
                    g = float(c[2])
                except ValueError:
                    continue
                comps.append((c[1].strip(), g))
                items.append({"dish_id": did, "ingredient": c[1].strip(),
                              "grams": g})
            if not comps:
                continue
            dishes.append({
                "dish_id": did, "cafe": cafe, "n_components": len(comps),
                # The door's own newline_grams dialect, rebuilt from the plate.
                "text": "\n".join(f"{nm} {g:.1f} g" for nm, g in comps),
                "text_semicolon": "; ".join(f"{nm} {g:.1f} g" for nm, g in comps),
                "Calories": cal, "Carbs": carb, "Protein": prot, "Fat": fat,
                "total_mass_g": mass,
            })

    dd = pd.DataFrame(dishes)
    ii = pd.DataFrame(items)
    dd.to_parquet(D / "n5k_dish.parquet", index=False)
    ii.to_parquet(D / "n5k_item.parquet", index=False)

    ing = pd.read_csv(D / "ingredients_metadata.csv")
    ing.to_parquet(D / "n5k_ingredient.parquet", index=False)

    (D / "PROVENANCE.md").write_text(
        "# Nutrition5k\n\n"
        "Google Research, 2021. Real cafeteria plates, each component weighed\n"
        "individually on a scale as it was added.\n\n"
        "```text\n"
        f"  n5k_dish.parquet        {len(dd):,} dishes, replayed as a newline_grams string\n"
        f"  n5k_item.parquet        {len(ii):,} (dish, ingredient, MEASURED grams)\n"
        f"  n5k_ingredient.parquet  {len(ing):,} ingredient names -> macros PER GRAM\n"
        "```\n\n"
        "Downloaded 2026-08-22 from\n"
        "`https://storage.googleapis.com/nutrition5k_dataset/nutrition5k_dataset/metadata/`\n\n"
        "MASS is measured. The per-gram macros behind each component come from\n"
        "USDA via the dataset's own ingredient table, so a dish total is\n"
        "measured-portion x estimated-density. Say so wherever it is scored.\n",
        encoding="utf-8")

    print(f"dishes      {len(dd):>7,}   components {len(ii):>7,}   "
          f"ingredients {len(ing):>5,}")
    print(f"components per dish: median {dd.n_components.median():.0f}  "
          f"max {dd.n_components.max()}")
    print(f"\n-> {D/'n5k_dish.parquet'}")
    print("\nsample text the door will be handed:")
    print("   " + dd.iloc[1].text.replace("\n", "\n   "))
    print(f"   -> truth  {dd.iloc[1].Calories:.0f} kcal  "
          f"{dd.iloc[1].Carbs:.1f} C  {dd.iloc[1].Protein:.1f} P  {dd.iloc[1].Fat:.1f} F")


if __name__ == "__main__":
    main()
