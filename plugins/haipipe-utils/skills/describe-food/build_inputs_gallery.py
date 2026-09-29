#!/usr/bin/env python3
"""
Build `_FoodInfo/0-inputs/`: one specimen of every SHAPE that can arrive.

    source .venv/bin/activate && source env.sh
    python Tools/plugins/haipipe-utils/skills/describe-food/build_inputs_gallery.py

The engine is haipipe-norm/inputs_gallery.py, shared by all four nouns. This
file holds only the list of shapes, because the list is the part that differs:
food arrives as a photograph and exercise never does.
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
# resolve() unwinds a Tools symlink, so a SPACE that links Tools in is found from the cwd instead
ROOT = next(a for a in [*HERE.parents, pathlib.Path.cwd(), *pathlib.Path.cwd().parents]
            if (a / "pyproject.toml").exists() and (a / "code").is_dir())
SKILLS = ROOT / "Tools/plugins/haipipe-utils/skills"
sys.path[:0] = [str(HERE), str(SKILLS / "haipipe-norm")]
INFO = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"

from inputs_gallery import (Shape, build, ABSENT, CALL,
                            CONTRACT, DEPLOYMENT)   # noqa: E402
import pandas as pd                                      # noqa: E402
import numpy as np                                       # noqa: E402
from foodnorm import enrich_food_to_nutrition            # noqa: E402


def call(req):
    df = pd.DataFrame({"FoodName": req["FoodName"]})
    if "ImagePath" in req:
        df["ImagePath"] = req["ImagePath"]
    out = enrich_food_to_nutrition(df, food_col="FoodName", stages="1-2")
    return out.replace({np.nan: None}).to_dict("records")


def by_shape(*names):
    return lambda g: int(g["shape"].isin(names).sum())


def sample_shape(*names, n=1):
    """The specimen comes off the board, not out of my head. Take the most
    common real string of this shape, and say which cohorts wrote it."""
    def take(g):
        sub = g[g["shape"].isin(names)]
        top = sub.FoodName.dropna().astype(str).value_counts().head(n)
        picked = list(top.index)
        who = sub[sub.FoodName.isin(picked)].cohort.value_counts()
        prov = ("Real rows. "
                + " · ".join(f"{v!r} appears {int(top[v]):,} times" for v in picked)
                + ". Written by " + ", ".join(f"{c} ({int(k):,})" for c, k in who.items()) + ".")
        return {"FoodName": picked}, prov
    return take


def sample_macro():
    """The input of 05-macro-nutrition is the typed NUMBER; the name beside it
    is only a placeholder. One real row per kind of writer, biggest first:
    WellDoc's 'Just Carbs' with its carbs, OhioT1DM's 'Unknown' with its carbs,
    dubosson's 'Unknown' with its calories. Values go in as they arrive: a 0
    that WellDoc stores for a macro nobody typed stays 0, NaN becomes null."""
    def take(g):
        sub = g[g["shape"].isin(["carb_declaration", "unnamed"])].copy()
        sub["typed"] = np.where(sub["Carbs"].fillna(0) > 0, "Carbs",
                                np.where(sub["Calories"].fillna(0) > 0, "Calories", ""))
        sub = sub[sub["typed"] != ""].sort_values(["cohort", "PatientID", "CarbsEntryID"], kind="stable")
        sub["placeholder"] = sub["FoodName"].astype(str).str.strip().str.lower()   # 'just carbs' is 'Just Carbs'
        groups = sorted(sub.groupby(["placeholder", "typed"]), key=lambda kv: -len(kv[1]))
        req = {"FoodName": [], "Carbs": [], "Calories": []}
        prov = []
        for (_, typed), grp in groups:
            top = grp.cohort.value_counts()
            row = grp[grp.cohort == top.index[0]].iloc[0]
            name = grp["FoodName"].value_counts().index[0]            # its commonest writing
            req["FoodName"].append(name)
            for c in ("Carbs", "Calories"):
                req[c].append(None if pd.isna(row[c]) else float(row[c]))
            prov.append(f"{name!r} with {typed} typed, {len(grp):,} rows, mostly {top.index[0]}")
        return req, "Real rows. " + " · ".join(prov) + "."
    return take


def sample_photo(n=1):
    """Return a real CGMacros photo row, not the text placeholder ``Unknown``.

    The frozen gold index intentionally omits image paths, so the photo shape
    must join back to the source Diet frame. The first frame is written
    relative to the SPACE root, the way t17's frozen photo names are keyed, so
    no machine path lands on disk; stage 0 reads it from the SPACE root.
    """
    def take(g):
        rows = []
        source = ROOT / "_WorkSpace/1-SourceStore/CGMacros"
        for f in sorted(source.glob("@*/Diet.parquet")):
            d = pd.read_parquet(f)
            if not len(d) or "ImagePath" not in d.columns:
                continue
            d = d.copy()
            d["PatientID"] = d["PatientID"].astype(str)
            d["FoodName"] = d["FoodName"].astype(str)
            d = d[(d["FoodName"].str.strip().str.lower() == "unknown")
                   & d["ImagePath"].notna()]
            rows.append(d[["PatientID", "CarbsEntryID", "FoodName", "ImagePath"]])
        if not rows:
            raise FileNotFoundError("no CGMacros photo rows with ImagePath")

        d = pd.concat(rows, ignore_index=True)
        d = d.sort_values(["PatientID", "CarbsEntryID"], kind="stable")
        for _, row in d.iterrows():
            rel = next((p.strip() for p in str(row["ImagePath"]).split(",")
                        if p.strip()), "")
            path = ROOT / "_WorkSpace/0-RawDataStore/CGMacros/Source" \
                         / str(row["PatientID"]) / rel
            if path.is_file():
                return {
                    "FoodName": [row["FoodName"]],
                    "ImagePath": [str(path.relative_to(ROOT))],
                }, ("Real CGMacros row. `Unknown` appears 1,644 times; this "
                    f"specimen carries {path.name} from {row['PatientID']}.")
        raise FileNotFoundError("CGMacros photo rows exist but no JPG is readable")
    return take


def sources(g):
    """Who wrote the rows, and what kind of thing each cohort writes."""
    rows = []
    for c, sub in g.groupby("cohort"):
        w = sub.FoodName.dropna().astype(str)
        n, u = len(sub), max(w.nunique(), 1)
        top = sub["shape"].value_counts()
        rows.append((c, f"{n:,}", f"{u:,}", f"{n/u:.1f}x",
                     f"mostly `{top.index[0]}` ({top.iloc[0]/n:.0%})"))
    rows.sort(key=lambda r: -int(r[1].replace(",", "")))
    tot, totu = len(g), g.FoodName.nunique()
    rows.append(("ALL", f"**{tot:,}**", f"**{totu:,}**", f"**{tot/totu:.1f}x**",
                 f"{int((g.FoodName.value_counts() == 1).sum()):,} writings appear once"))
    note = ("Food is the only one of the four with real language variety: 31,075 of "
            "its 35,558 writings appear exactly once, and those singletons are 43.4% "
            "of all rows. No amount of memorising common phrases reaches them.")
    return rows, note


SHAPES = [
    Shape("01-plain-text", "one food, named",
          "The contract's default. Every other shape is a way a logged meal "
          "fails to be one clean name.",
          {"FoodName": ["White Rice"]}, by_shape("single_item"),
          "5-api-examples/01-text-single-item/1-fried-rice",
          sample=sample_shape("single_item")),
    Shape("02-decorated-text", "a name with something else stuck to it",
          "What a real free-text box produces. Not on this board, because "
          "WellDoc's composites use separators rather than prose.",
          {"FoodName": ["White Rice, homemade", "rice (steamed)"]}, ABSENT),
    Shape("03-several-in-one", "several foods in one string",
          "The largest shape here. A meal is not one item, and a resolver that "
          "reads the whole string as one name resolves none of them.",
          {"FoodName": ["Spinach; Original English Muffins; 100% Liquid Egg Whites"]},
          by_shape("item_list"), "5-api-examples/02-text-item-list/1-list-1",
          sample=sample_shape("item_list")),
    Shape("04-text-with-amount", "a food and how much of it",
          "The only shape that can be scored in grams. Ten of eleven cohorts "
          "never state a portion, which is why the rest are scored on coverage.",
          {"FoodName": ["White Rice, 100 g", "Boiled vegetable111 g"]},
          by_shape("newline_grams", "single_grams"),
          "5-api-examples/03-text-with-grams/1-grams-1",
          sample=sample_shape("newline_grams", "single_grams")),
    Shape("05-macro-nutrition", "typed macro numbers; the name is only a placeholder",
          "The input is the NUMBER, not the name. WellDoc's 'Just Carbs' entry "
          "mode and the public cohorts' 'Unknown' (OhioT1DM carbs, dubosson "
          "calories) both mean: a count was typed and no food was named. "
          "Nothing to resolve, so the door answers MISS on purpose and the "
          "row's own number is the meal's. A macro nobody typed is NOT "
          "MEASURED, not zero.",
          {"FoodName": ["Just Carbs"], "Carbs": [45]},
          by_shape("carb_declaration", "unnamed"),
          "5-api-examples/04-text-names-no-food/1-just-carbs",
          sample=sample_macro()),
    Shape("06-mixed-declaration", "a carb count AND a food, together",
          "'Just Carbs; White Rice' is both shapes at once, which is why typing "
          "must happen per COMPONENT and not per meal string.",
          {"FoodName": ["Just Carbs; White Rice"]}, by_shape("mixed_declaration"),
          "5-api-examples/04-text-names-no-food/3-dinner",
          sample=sample_shape("mixed_declaration")),
    Shape("07-image", "a photo in, macros out",
          "The input is the PHOTO; the output is the macros. The door reads it "
          "only when an image engine is set: stage 0 names the food from the "
          "photo, then the text lane finds its nutrition. CGMacros is the only "
          "cohort where a meal photo and five measured macros sit on the same "
          "row, so its measured macros are the right answer to check against.",
          {"ImagePath": ["<a CGMacros photo>"], "FoodName": ["Unknown"]},
          by_shape("photo_only"), "5-api-examples/06-image-upload",
          sample=sample_photo()),
    Shape("08-batch", "several meals at once",
          "A call shape rather than a row shape. Order is preserved and each "
          "meal keeps its own verdict.",
          {"FoodName": ["White Rice", "Just Carbs", "Unknown", "Banana"]},
          CALL, "5-api-examples/05-text-batch/1-batch-1"),
]

if __name__ == "__main__":
    g = pd.read_parquet(INFO / "2-corpus/gold_index.parquet")
    out = build("food", INFO, SHAPES, call,
                keep=["NutritionConf", "NutritionSource", "NutritionBasis",
                      "Carbs", "Calories"],
                corpus=g, total=len(g), sources=sources,
                verdict=lambda a: f"`{a.get('NutritionConf')}`"
                + (f" carbs {a['Carbs']:.0f}" if a.get("Carbs") else ""))
    print(f"wrote {out}")
