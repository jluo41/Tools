#!/usr/bin/env python3
"""
Build `_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo/`.

    source .venv/bin/activate && source env.sh
    Tools/plugins/haipipe-utils/skills/describe-food/run_server.sh   # another shell
    python Tools/plugins/haipipe-utils/skills/describe-food/build_foodinfo.py

MOVED HERE FROM A TASK FOLDER, and the move is the point. This file describes
what the SKILL currently is, so it must be rerun on every resolver change, and a
generator that lives next to the resolver gets rerun. The BENCHMARK that grades
the skill stays a task -- it has a question, a run and a reading, and its numbers
are supposed to move.

    skill/build_<noun>info.py   ->  _XInfo/       "what am I right now"
    task/<...>/00_benchmark/    ->  results/      "how good am I"

WHAT CHANGED BESIDES THE ADDRESS
--------------------------------------------------------------------------------
The old page said what the INPUT looked like -- shapes, labels, two real rows.
That half is kept, because the SHAPE x LABEL split is this noun's best idea and
the reason its corpus is honest: gradability is a property of the TARGET
columns, so Shanghai's 3,470 rows are excluded as `derived` even though they
parse beautifully, since their Carbs IS this library's own output.

The half it did not have is the OUTPUT, contributed by _ExerciseInfo. A folder
that never runs the resolver cannot report the two columns the family rests on:
the CONFIDENCE distribution (rule 3) and the BASIS distribution (rule 4). It
runs the resolver now. Measured cost: ~1 minute for all 71,673 rows.
"""
import glob
import json
import pathlib
import shutil
import sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(HERE.parent / "haipipe-norm")]

from foodnorm import normalize                                       # noqa: E402
from xinfo import CohortStats, copy_api_examples, link_reference, write  # noqa: E402

# The three _XInfo folders live together under 0-EventNorm/ -- they are
# one layer of one system, not three folders that happen to share a
# parent with every raw cohort dump.
DEST = ROOT / "_WorkSpace/0-RawDataStore/0-EventNorm/_FoodInfo"
EXTERNAL = ROOT / "_WorkSpace/ExternalStore"
BENCH = ROOT / "examples/Proj1-CGM-RawData/tasks/AY1_foodrec_v1/00_benchmark"

ORIGIN = {
    "CGMacros": "study protocol: meal photos + laboratory macros",
    "OhioT1DM": "patient self-report, carbs only",
    "Shanghai": "clinical dietary-intake sheet, Chinese, translated",
    "dubosson": "study log, calories only",
}
DEFAULT_ORIGIN = "app food database + user free text"


def page(cohort, df, res, gold_sub):
    L = [f"# {cohort} — food", "",
         f"origin: {ORIGIN.get(cohort, DEFAULT_ORIGIN)}", ""]
    if not len(df):
        return "\n".join(L + ["The Diet table exists and is empty.", ""])
    L += ["```text",
          f"  rows            {len(df):>9,}",
          f"  patients        {df.PatientID.nunique():>9,}",
          f"  distinct names  {df.FoodName.fillna('').nunique():>9,}",
          "",
          "  OUT",
          f"  value written   {res.Calories.notna().sum():>9,}"
          f"  {res.Calories.notna().mean():6.1%}",
          f"  has a basis     {res.NutritionBasis.notna().sum():>9,}"
          f"  {res.NutritionBasis.notna().mean():6.1%}",
          "",
          "  confidence"] + [
        f"  {k:<20} {v:>9,}" for k, v in res.NutritionConf.value_counts().items()] + [
        "", "  basis"] + [
        f"  {str(k):<20} {v:>9,}" for k, v in
        res.NutritionBasis.value_counts(dropna=False).items()]
    if gold_sub is not None and len(gold_sub):
        L += ["", "  shape x label (only LABEL decides gradability)"]
        for sh, n in gold_sub["shape"].value_counts().items():
            L.append(f"  {sh:<20} {n:>9,}")
    L += ["```", "", "## Two real rows", "", "```text"]
    for _, r in df.head(2).iterrows():
        L.append("  " + json.dumps({k: (None if pd.isna(v) else str(v)[:60])
                                    for k, v in r.items()}, ensure_ascii=False)[:320])
    L += ["```", ""]
    return "\n".join(L)


def main():
    gold_path = BENCH / "results/gold_index.parquet"
    gold = pd.read_parquet(gold_path) if gold_path.exists() else None
    if gold is None:
        print(f"  ! no gold index at {gold_path}; gradeable will be empty")

    stats, pages = [], {}
    for p in sorted(glob.glob(str(ROOT / "_WorkSpace/1-SourceStore/*/*/Diet.parquet"))):
        coh = p.split("/")[-3]
        df = pd.read_parquet(p)
        if not len(df):
            stats.append(CohortStats(noun="food", cohort=coh, rows=0,
                                     origin=ORIGIN.get(coh, DEFAULT_ORIGIN)))
            pages[coh] = page(coh, df, None, None)
            continue
        res = pd.DataFrame(normalize(df.FoodName.fillna("").astype(str).tolist()))
        # The honest denominator. A row that named no food at all cannot be
        # resolved by any bank, and counting it as a miss measures the log.
        named = df.FoodName.fillna("").astype(str).str.strip().ne("") & \
            ~df.FoodName.fillna("").astype(str).str.lower().isin(
                {"unknown", "nan", "none", "n/a"})
        excluded = {"unnamed": int((~named).sum())} if (~named).any() else {}

        g = gold[gold.cohort == coh] if gold is not None else None
        gradeable = {}
        if g is not None and len(g) and "label" in g.columns:
            for k, n in g["label"].value_counts().items():
                # Only LABEL decides. 'derived' means the label IS this
                # library's own output and grading it would be circular.
                if k not in ("derived", "no_label"):
                    gradeable[str(k)] = int(n)

        stats.append(CohortStats(
            noun="food", cohort=coh, rows=len(df),
            patients=int(df.PatientID.nunique()),
            kinds=({"named": int(named.sum()), "unnamed": int((~named).sum())}),
            denominator={"resolvable": int(named.sum()), "excluded": excluded},
            coverage={"value_written": int(res.Calories.notna().sum())},
            confidence=res.NutritionConf.value_counts().to_dict(),
            # This noun ranks by WHERE THE NUMBER CAME FROM, not by how likely a
            # match is. A measured value beats a modelled one; both beat none.
            confidence_order=["MEASURED", "ESTIMATED", "WEAK", "MISS"],
            trusted=["MEASURED", "ESTIMATED"],
            basis={str(k): int(v) for k, v in
                   res.NutritionBasis.value_counts(dropna=False).items()},
            gradeable=gradeable,
            origin=ORIGIN.get(coh, DEFAULT_ORIGIN)))
        pages[coh] = page(coh, df, res, g)
        print(f"  {coh:<20} {len(df):>7,} rows  "
              f"{res.Calories.notna().mean():6.1%} valued")

    for name, target in (("foodnorm", EXTERNAL / "foodnorm"),
                         ("usda_fdc", EXTERNAL / "usda_fdc")):
        if target.exists():
            link_reference(DEST, name, target)
    (DEST / "2-corpus").mkdir(parents=True, exist_ok=True)
    for name in ("gold_index.parquet", "gold_summary.json", "bench_gate_b.json"):
        src = BENCH / "results" / name
        if src.exists():
            shutil.copy2(src, DEST / "2-corpus" / name)
    n_ex = copy_api_examples(DEST, HERE / "examples" / "api")

    rep = write(
        noun="food", emoji="🍎",
        tagline="Every cohort's food data, in and out, on one page each.",
        producer="Tools/plugins/haipipe-utils/skills/describe-food/build_foodinfo.py",
        rerun=("source .venv/bin/activate && source env.sh\n"
               "Tools/plugins/haipipe-utils/skills/describe-food/run_server.sh   # another shell\n"
               "python Tools/plugins/haipipe-utils/skills/describe-food/build_foodinfo.py"),
        dest=DEST, stats=stats, pages=pages,
        sections=[
            "## SHAPE is not LABEL", "",
            "Two orthogonal axes, and this noun's best idea. SHAPE is a property",
            "of `FoodName`: what a parser must handle. LABEL is a property of the",
            "macro columns: what may be graded against. **Only LABEL decides",
            "benchmark membership.**", "",
            "Shanghai's 3,470 rows are excluded as `derived` even though they parse",
            "cleanly, because their Carbs and Calories ARE this library's own output",
            "-- `NutritionSource='bank_usda'` proves it. Grading them is circular,",
            "and the irony is exact: the one cohort the library is wired into is the",
            "one cohort that cannot grade it.", "",
            "The frozen corpus and the current baseline are in `2-corpus/`; the",
            "benchmark that produces them stays a task, at",
            "`examples/Proj1-CGM-RawData/tasks/AY1_foodrec_v1/00_benchmark/`.",
        ])
    print(f"\nwrote {rep['dest']}  ·  {rep['cohorts']} cohorts  ·  "
          f"{n_ex} api examples  ·  conforming: {not rep['problems']}")


if __name__ == "__main__":
    sys.exit(main())
