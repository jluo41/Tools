"""
Freeze one noun's benchmark corpus.

Runs NO normalizer and touches NO reference bank, so the output is a fact about
the DATA, not about our code. A corpus that moves when the code moves grades
nothing -- that is the whole reason this is a separate step from grading.
"""
import json
from pathlib import Path

import pandas as pd

from .split import split_of, TEST_FRACTION


def freeze(spec, source_store, out_dir, test_fraction: float = TEST_FRACTION,
           verbose: bool = True) -> pd.DataFrame:
    """Walk every cohort's typed frame -> gold_index.parquet + gold_summary.json."""
    spec.check()
    source_store, out_dir = Path(source_store), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    keep = tuple(spec.id_cols) + (spec.text_col,) + tuple(spec.extra_cols) \
        + tuple(spec.label_cols)
    rows, empty = [], []

    for path in sorted(source_store.glob(f"*/@*/{spec.frame}.parquet")):
        cohort = path.relative_to(source_store).parts[0]
        df = pd.read_parquet(path)
        if len(df) == 0:
            # An empty typed frame is a FACT (the table exists, the cohort logs
            # nothing), not a cohort to omit. xinfo makes the same choice.
            empty.append(cohort)
            if verbose:
                print(f"  {cohort:<24} {0:>7} rows (empty typed frame)")
            continue

        if spec.augment is not None:
            df = spec.augment(df, cohort)
        have_derived = spec.derived_col in df.columns if spec.derived_col else False
        for c in keep:
            if c not in df.columns:
                df[c] = None
        for r in df.to_dict("records"):
            derived = r.get(spec.derived_col) if have_derived else None
            rec = {"cohort": cohort}
            rec.update({c: r.get(c) for c in keep})
            rec["shape"] = spec.classify_shape(r)
            rec["label"] = spec.classify_label(r, derived)
            rec["split"] = split_of(r.get(spec.id_cols[0]), test_fraction)
            rows.append(rec)
        if verbose:
            print(f"  {cohort:<24} {len(df):>7,} rows")

    g = pd.DataFrame(rows)
    for c in spec.label_cols:
        g[c] = pd.to_numeric(g[c], errors="coerce")
    # Identifiers are never arithmetic. WellDoc's are GUIDs and everyone else's
    # are small ints; let the parquet writer guess a common type and it fails.
    for c in tuple(spec.id_cols) + (spec.text_col,):
        g[c] = g[c].astype("string")

    x = pd.crosstab(g["shape"], g["label"])
    if verbose:
        print(f"\n{len(g):,} rows total\n")
        print("SHAPE x LABEL");  print("-" * 78);  print(x.to_string())
        print("\nGRADEABLE, held-out test split only");  print("-" * 78)
        t = g[(g.split == "test") & (g.label.isin(spec.gradeable))]
        for (sh, lb), n in t.groupby(["shape", "label"]).size() \
                            .sort_values(ascending=False).items():
            print(f"  {sh:<22} {lb:<16} {n:>7,}   score on: "
                  f"{', '.join(spec.gradeable[lb])}")
        print("\nEXCLUDED, and why");  print("-" * 78)
        d = g[g.label == spec.derived_label]
        print(f"  {spec.derived_label:<22} {len(d):>7,}   {sorted(d.cohort.unique())}")
        print(f"  {'':<22} {'':>7}   the normalizer WROTE these numbers. Circular.")
        for lb in sorted(set(g.label) - set(spec.gradeable) - {spec.derived_label}):
            print(f"  {lb:<22} {int((g.label == lb).sum()):>7,}")

    g.to_parquet(out_dir / "gold_index.parquet", index=False)
    summary = {
        "noun": spec.noun,
        "frame": spec.frame,
        "n_rows": int(len(g)),
        "test_fraction": test_fraction,
        "empty_frames": empty,
        "shape_x_label": {str(k): {str(kk): int(vv) for kk, vv in v.items()}
                          for k, v in x.to_dict().items()},
        "n_patients": {s: int(g[g.split == s][spec.id_cols[0]].nunique())
                       for s in ("train", "test")},
    }
    (out_dir / "gold_summary.json").write_text(json.dumps(summary, indent=2))
    if verbose:
        print(f"\nwrote {out_dir/'gold_index.parquet'}\n      {out_dir/'gold_summary.json'}")
    return g
