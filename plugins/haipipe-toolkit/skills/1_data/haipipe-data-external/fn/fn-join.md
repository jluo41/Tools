fn-join: Preview joining an external asset into a cohort set
=============================================================

NEVER materializes a join. Always preview-only. Outputs match-rate
diagnostics + a config snippet to paste into the consuming layer.

---

Step 0: Read prerequisite refs
-------------------------------

  - `ref/concepts.md`
  - `ref/join-contract.md`     (mechanics + match-rate calc)
  - `ref/asset-catalog.md`     (asset's primary key + common cohort cols)
  - `../haipipe-data-source/ref/concepts.md`   (target SourceSet shape)

---

Step 1: Resolve inputs
-----------------------

Args:

```
<asset>            external asset slug (e.g. npi)
--to <set>         path to a SourceSet/RecordSet/CaseSet
                   (e.g. _WorkSpace/1-SourceStore/20250829_SMSR3Full/@SMSParquetV250211)
--table <name>     optional: which ProcName/table inside the set
--on <column>      optional: cohort column to join on
                   (defaults: see asset-catalog Common Cohort Columns)
--columns <list>   optional: subset of external columns to include
--version @{tag}   optional: pin external release
```

If `--table` is omitted, scan the set's parquets for one that contains
a column matching the asset's expected join key (per catalog table).
If multiple tables match, ask the user.

---

Step 2: Load both sides (in-memory only)
-----------------------------------------

```python
# Cohort side
cohort_df = pd.read_parquet(f'{set_path}/{table}.parquet')
left_col  = on or {default cohort column from catalog}

# External side
ext_dir   = f'{LOCAL_EXTERNAL_STORE}/{asset}'
ext_df    = pd.read_parquet(f'{ext_dir}/df_{asset}_id.parquet')
right_col = f'{PRIMARY_KEY}_original'
```

NEVER write the loaded data anywhere. Both DataFrames stay in-memory
for the duration of the preview.

---

Step 3: Compute match rate
---------------------------

Per `ref/join-contract.md`:

```python
left_keys  = cohort_df[left_col].dropna().astype(str).unique()
right_keys = ext_df[right_col].dropna().astype(str).unique()

matched   = set(left_keys) & set(right_keys)
unmatched = set(left_keys) - set(right_keys)

match_rate = len(matched) / max(len(left_keys), 1)

freq          = cohort_df[left_col].astype(str).value_counts()
top_unmatched = [k for k in freq.index if k in unmatched][:20]
```

If `match_rate < 0.70`: emit a format-mismatch warning and sample
5 matched + 5 unmatched keys side-by-side so the user can eyeball
length / leading-zero / dtype issues.

---

Step 4: Identify columns the join would add
--------------------------------------------

```python
ext_cols = [c for c in ext_df.columns
            if c not in (right_col, PRIMARY_KEY)]
join_cols = filter_by_columns_arg(ext_cols)   # honor --columns flag
```

If the README has logical column groups (e.g. NPI -> Demographics,
Geographic, Reviews/Personality), preserve them in the rendered
preview.

---

Step 5: Render the preview
---------------------------

```
Join preview: {asset} (release {version}) -> {set_path}/{table}.parquet

  cohort column:     {table}.{left_col}     ({len(left_keys):,} unique)
  external key:      {right_col}             ({len(right_keys):,} unique)
  matched:           {len(matched):,}        ({match_rate:.1%})
  unmatched (top 20 by frequency):
    {key} (n={freq})
    ...

  columns to add ({len(join_cols)}):
    {col} (vocab_size=N)
    ...

  [low match-rate warning, if applicable]
  Sample matched / unmatched keys side-by-side:
    matched:   ['1234567890', '0987654321', ...]
    unmatched: ['1234567890.0', '987654321',  ...]
    -> Possible cause: float vs str dtype, missing leading zero
```

Then emit the YAML config snippet from `ref/join-contract.md`,
filled with the resolved values.

---

Step 6: Return tail
--------------------

```
status:          ok | warn (low match rate)
asset:           {asset}
target:          {set_path}/{table}
match_rate:      {pct}%
columns_added:   {N}
config_snippet:  |
  externals:
    {asset}:
      ...
next:            "Paste the snippet into your RecordFn/CaseFn config and
                  run /haipipe-data-record cook (or the appropriate stage)."
```

---

MUST NOT
---------

- Do NOT write a merged DataFrame to disk.
- Do NOT modify the cohort set or the external asset.
- Do NOT cast or normalize the join key without flagging it -- a low
  match rate is data the user needs to see, not a problem to silently
  fix.
- Do NOT update RecordFn / CaseFn config files automatically -- the
  user pastes the snippet themselves.
