"""The example Board's data: two data versions of one made-up dataset, so every insight page has something to show.

Every row is synthetic (numpy, fixed seed); nothing comes from a real dataset, person or organization. One row is one
made-up contact: its day, the arm it got (A or B), its group (group_1, group_2, and a deliberately small group_3), a
0/1 outcome and a plain numeric score. Arm B is given a higher outcome rate than arm A, so the example has a gap to find.

    python make_example_data.py        writes data-v1/ (the first ten days) and data-v2/ (all sixteen days) beside this file

Each data version folder holds the data file (example.parquet), its manifest.json, data_dictionary.csv, cohort_summary.txt
and figures/rows-per-day.png: what a data version folder holds (haipipe-insight ref/insight-ladder.md rule 6). data-v2 holds
every data-v1 row plus the later days (accumulates: yes). Rerun it to rebuild both; the same seed writes the same rows.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SEED = 7
START = pd.Timestamp("2026-01-05")
DAYS_V1, DAYS_V2 = 10, 16
PER_DAY = 60
RATE = {"A": 0.30, "B": 0.48}                          # the made-up gap the example's questions find
GROUPS = (("group_1", 0.55), ("group_2", 0.38), ("group_3", 0.07))   # group_3 too small to answer on its own


def rows(days: int) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    n = days * PER_DAY
    day = np.repeat(np.arange(days), PER_DAY)
    arm = rng.choice(["A", "B"], size=n)
    group = rng.choice([g for g, _ in GROUPS], size=n, p=[p for _, p in GROUPS])
    late = day >= days // 2
    p = np.array([RATE[a] for a in arm]) + np.where(group == "group_2", 0.04, 0.0) - np.where(late, 0.02, 0.0)
    outcome = (rng.random(n) < p).astype(int)
    score = np.round(rng.normal(50, 10, size=n) + 6 * outcome, 1)
    return pd.DataFrame({"date": START + pd.to_timedelta(day, unit="D"), "arm": arm, "group": group,
                         "outcome": outcome, "score": score})


DICTIONARY = [("date", "time", "the day of the contact"), ("arm", "design", "the arm it got: A or B"),
              ("group", "design", "its group: group_1, group_2 or the small group_3"),
              ("outcome", "outcome", "1 when the made-up outcome happened, else 0"),
              ("score", "measure", "a plain numeric score, higher with the outcome")]


def freeze(name: str, days: int, label: str) -> None:
    # data-v2 accumulates: the first DAYS_V1 days are the same rows as data-v1 (same seed, rows drawn day by day in order)
    df = rows(DAYS_V2).loc[lambda d: d["date"] < START + pd.Timedelta(days=days)].reset_index(drop=True)
    out = HERE / name
    (out / "figures").mkdir(parents=True, exist_ok=True)
    df.to_parquet(out / "example.parquet", index=False)
    manifest = {"output_file": "example.parquet", "n_rows": int(len(df)), "n_cols": int(df.shape[1]),
                "start_date": str(df["date"].min().date()), "end_date": str(df["date"].max().date()),
                "source_set": "synthetic (make_example_data.py, seed 7)", "label": label,
                "groups": {"identity": []}}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    dd = pd.DataFrame([{"name": c, "group": g, "dtype": str(df[c].dtype),
                        "null_pct": round(100 * float(df[c].isna().mean()), 1), "n_unique": int(df[c].nunique()),
                        "notes": notes} for c, g, notes in DICTIONARY])
    dd.to_csv(out / "data_dictionary.csv", index=False)
    by_arm = df.groupby("arm")["outcome"].agg(["size", "mean"])
    by_group = df["group"].value_counts().sort_index()
    lines = [f"Example data version {name}: {label} (synthetic, made by make_example_data.py)",
             f"rows: {len(df)}  ·  days: {df['date'].nunique()}  ·  {manifest['start_date']} to {manifest['end_date']}",
             "rows per arm: " + ", ".join(f"{a} {int(r['size'])}" for a, r in by_arm.iterrows()),
             "rows per group: " + ", ".join(f"{g} {int(n)}" for g, n in by_group.items()),
             "outcome rate per arm: " + ", ".join(f"{a} {r['mean']:.2f}" for a, r in by_arm.iterrows())]
    (out / "cohort_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    per_day = df.groupby(["date", "arm"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    per_day.plot(kind="bar", stacked=True, ax=ax, color=["#3e5c84", "#adb5bd"], width=0.8)
    ax.set_xticklabels([d.strftime("%m-%d") for d in per_day.index], rotation=0, fontsize=7)
    ax.set_xlabel("")
    ax.set_ylabel("rows")
    ax.set_title(f"Rows per day, by arm · {name}", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "figures" / "rows-per-day.png", dpi=110)
    plt.close(fig)
    print(f"{name}: {len(df)} rows -> {out.relative_to(HERE)}/example.parquet")


def main() -> int:
    freeze("data-v1", DAYS_V1, "first ten days")
    freeze("data-v2", DAYS_V2, "all sixteen days")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
