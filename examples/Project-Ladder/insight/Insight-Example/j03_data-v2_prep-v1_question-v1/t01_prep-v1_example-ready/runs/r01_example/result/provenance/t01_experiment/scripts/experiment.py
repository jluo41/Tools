"""experiment · one step of prep-v1 (hai-insight ref/dataprep.md): the experiment card, from ctx.raw only.
Aggregates only: arms and their counts, the date range, rows per day. The example has no documents, so nothing is
stated and nothing stated is checked."""
import json

import pandas as pd

COLUMNS = ["date", "arm", "group", "outcome", "score"]


def run(ctx):
    raw = ctx.raw / "example.parquet"
    if not raw.is_file():
        ctx.refuse(f"the raw export holds no example.parquet: {ctx.raw}")
    df = pd.read_parquet(raw)
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        ctx.refuse(f"the raw export lacks {', '.join(missing)}")
    days = pd.to_datetime(df["date"]).dt.normalize()
    per_day = days.value_counts()
    seen = sorted(days.unique())
    gaps = [f"{a.date()} to {b.date()}" for a, b in zip(seen, seen[1:]) if (b - a).days > 1]
    card = {"stated": "nothing stated",
            "settings": {"arms": {a: int(n) for a, n in df["arm"].value_counts().sort_index().items()},
                         "groups": sorted(df["group"].unique().tolist())},
            "time": {"first_day": str(days.min().date()), "last_day": str(days.max().date()),
                     "calendar_days": int((days.max() - days.min()).days) + 1, "active_days": int(days.nunique()),
                     "gaps": gaps, "rows_per_day": {"min": int(per_day.min()), "max": int(per_day.max())},
                     "utc_and_local_time": "not checkable: the export holds days, not times",
                     "send_hours": "not checkable: the export holds days, not times"},
            "checks": {"settings": "not checkable: nothing stated", "time": "not checkable: nothing stated"}}
    (ctx.out / "experiment_card.json").write_text(json.dumps(card, indent=2) + "\n")
    arms = ", ".join(f"{a} {n}" for a, n in card["settings"]["arms"].items())
    t = card["time"]
    (ctx.out / "experiment_card.md").write_text(
        "# Experiment card\n\nNothing stated: the example has no documents, so no setting is checked.\n\n"
        f"- arms: {arms}\n- groups: {', '.join(card['settings']['groups'])}\n"
        f"- days: {t['first_day']} to {t['last_day']}, {t['active_days']} active of {t['calendar_days']}\n"
        f"- gaps: {', '.join(t['gaps']) or 'none'}\n"
        f"- rows per day: {t['rows_per_day']['min']} to {t['rows_per_day']['max']}\n"
        "- UTC and local time, send hours: not checkable, the export holds days, not times\n")
