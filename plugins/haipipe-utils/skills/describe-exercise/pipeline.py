"""
CLI for describe-exercise, for looking at one activity without writing a script.

    python pipeline.py Walking --minutes 30 --weight 82
    python pipeline.py 20903 --source 20
    python pipeline.py --frame _WorkSpace/1-SourceStore/WellDoc2025ALS/@WellDocDataV251226/Exercise.parquet
"""
import argparse
import json
import sys

from exnorm import normalize
from exnorm.constants import DEFAULT_BANK


def main():
    ap = argparse.ArgumentParser(description="describe-exercise")
    ap.add_argument("activities", nargs="*", help="activity names or codes")
    ap.add_argument("--minutes", type=float)
    ap.add_argument("--weight", type=float, dest="weight_kg")
    ap.add_argument("--source", dest="source_ids", help="EntrySourceID")
    ap.add_argument("--transport", choices=["local", "http"])
    ap.add_argument("--frame", help="a parquet Exercise frame; prints a summary")
    a = ap.parse_args()

    if a.frame:
        import pandas as pd
        from exnorm.enrich import enrich_exercise
        df = pd.read_parquet(a.frame)
        out = enrich_exercise(df, weight_kg=a.weight_kg)
        print(f"bank  {DEFAULT_BANK}")
        print(f"rows  {len(out):,}\n")
        print("-- what each row IS --")
        print(out["TypeSource"].str.split(":").str[1].value_counts().to_string())
        print("\n-- confidence --")
        print(out["ExerciseConf"].value_counts().to_string())
        print("\n-- basis --")
        print(out["ExerciseBasis"].value_counts(dropna=False).to_string())
        got = out["METValue"].notna()
        print(f"\nMET written  {got.sum():,} / {len(out):,} = {got.mean():.1%}")
        return 0

    if not a.activities:
        ap.error("give an activity, or --frame")
    rows = normalize(a.activities, minutes=a.minutes, weight_kg=a.weight_kg,
                     source_ids=a.source_ids, transport=a.transport)
    print(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
