fn-review: Schema, coverage, and staleness audit
=================================================

Read-only audit of one asset (or all assets in the active release if
no asset name given). Reports:

  schema:     mandatory files present, column contract satisfied
  coverage:   primary-key uniqueness, null rates, vocab sizes
  staleness:  for dimension assets, raw-vs-output mtimes
              for engagement assets, cohort-vs-output mtimes

---

Step 1: Resolve scope
----------------------

  - `review {asset}`         -> audit one asset
  - `review` (no arg)        -> audit every asset in EXTERNAL_VERSION

Use `ref/asset-catalog.md` to enumerate.

---

Step 2: Schema audit
---------------------

For each asset, verify:

  required:  df_{asset}_id.parquet
             column_to_{asset}_li.pkl
             README.md
  optional:  df_{asset}_raw.parquet (engagement only)

Read the parquet's columns and the pkl's keys. Verify:

  - `{PRIMARY_KEY}_original` column exists in the parquet
  - `{PRIMARY_KEY}` column exists (the integer ID)
  - Every non-key parquet column has a matching vocab entry
  - Every vocab entry contains `_unknown` at index 0 and `_mask`
    at index 1

Report any missing pieces.

---

Step 3: Coverage audit
-----------------------

```python
df = pd.read_parquet(parquet_path)
n            = len(df)
unique_keys  = df[f'{PRIMARY_KEY}_original'].dropna().nunique()
key_rate     = unique_keys / n
null_rates   = df.isna().mean().sort_values(ascending=False)
```

Surface:

```
rows:                    {n}
primary-key uniqueness:  {unique_keys}/{n}  ({key_rate:.1%})
top-5 null-rate columns:
  {col}:  {pct}%
  ...
vocab sizes per column:
  {col}:  {size}
  ...
```

A primary-key uniqueness rate < 100% means the asset has duplicate
keys -- flag as a warning unless the README explicitly documents
multi-row-per-key (e.g. an asset that emits one row per (NPI, year)
would have <100% uniqueness on NPI alone).

---

Step 4: Staleness audit
------------------------

```python
import os
asset_mtime = os.path.getmtime(parquet_path)
```

For dimension:

  - Read the builder file to find raw input paths (`*_PATH = ...`).
  - For each raw input that exists locally, compare mtime.
  - If raw_mtime > asset_mtime: STALE (raw newer than asset).

For engagement:

  - Read the builder to find the source cohort path (often a
    `combined_deidentified_*.parquet` or a SourceSet folder).
  - Compare mtime of the cohort's newest file vs asset_mtime.

Report:

```
{asset}  fresh                                 (asset newer than inputs)
{asset}  STALE  raw=2025-09-01  asset=2025-08-15  (raw 17d newer)
{asset}  unknown (raw missing locally; cannot determine staleness)
```

---

Step 5: Return tail
--------------------

```
status:        ok | warn | fail
asset(s):      [list reviewed]
issues:        [list of any schema / coverage / staleness flags]
stale assets:  [list]
next:          "/haipipe-data-external refresh {stale list}   (rebuild stale)"
```

---

MUST NOT
---------

- Do NOT mutate the asset or the builder during review.
- Do NOT pull raw inputs from remote -- review uses what is local.
- Do NOT auto-rebuild stale assets -- that is `refresh`.
