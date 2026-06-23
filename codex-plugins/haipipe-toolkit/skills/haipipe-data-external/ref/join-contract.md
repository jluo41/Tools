External Join Contract
=======================

Defines how an external asset is joined into a cohort layer (Source,
Record, Case, AIData). The `join` verb in this skill **previews** the
operation; the actual join happens in the consuming layer.

---

Mechanics
=========

A join takes two inputs:

  1. Cohort table -- a DataFrame from a SourceSet / RecordSet / CaseSet
                     containing a left-side join column (e.g. Rx.npi).
  2. External asset -- df_{asset}_id.parquet + column_to_*_li.pkl from
                     _WorkSpace/ExternalStore/@{version}/{asset}/.

The join key:

```
cohort_column   --merged on-->   {PRIMARY_KEY}_original
(string)                         (string, in the external)
```

The merge is a LEFT JOIN from the cohort side. Cohort rows whose key
has no match in the external get NaN for the new columns; integer ID
columns can optionally be filled with the asset's `_unknown` token's
ID (see `on_unmatched` below).

---

Match-Rate Calculation (used by `join` preview)
================================================

```
unique_cohort_keys   = cohort[cohort_column].dropna().astype(str).unique()
unique_external_keys = external[f'{PRIMARY_KEY}_original'].dropna().astype(str).unique()

matched     = unique_cohort_keys ∩ unique_external_keys
unmatched   = unique_cohort_keys − unique_external_keys

match_rate    = len(matched) / max(len(unique_cohort_keys), 1)
top_unmatched = sorted(unmatched by frequency in cohort, descending)[:20]
```

Always coerce both sides to string before set-comparing -- mixed-dtype
joins are the most common cause of false zero-match.

Report all four numbers in the preview output:

```
unique cohort keys:     1,234,567
unique external keys:   4,639,030
matched:                1,089,432  (88.2%)
unmatched (top 20):     [...]
```

A match rate below 70% should trigger a format-mismatch warning. The
preview should sample 5 matched + 5 unmatched keys side-by-side so
the user can eyeball length / leading-zero / case issues.

---

Recommended Config Snippet (output of `join`)
==============================================

The skill emits a YAML block to paste into the consuming layer's
config:

```yaml
externals:
  npi:
    version: "@260104R4"          # pin or omit to follow EXTERNAL_VERSION
    asset_path: ExternalStore/@260104R4/npi
    join:
      cohort_table:    Rx          # which table in the SourceSet/RecordSet
      cohort_column:   prescriber_npi
      external_key:    NPI_original
    columns:                       # optional; defaults to all non-key cols
      - Specialty
      - Credential
      - Openness_score
      - Conscientiousness_score
      - final_MIPS_score
    on_unmatched:    keep_null     # keep_null | use_unknown_token | drop_row
```

Field semantics:

  version          Pin to a specific release for reproducibility.
                   Omit to inherit EXTERNAL_VERSION from env.sh.
  asset_path       Relative to _WorkSpace/. Mirrors the resolved
                   release.
  cohort_table     Which ProcName in the cohort set the join applies
                   to. Required when the cohort is multi-table.
  cohort_column    The left-side join column name.
  external_key     Always {PRIMARY_KEY}_original for that asset.
  columns          Whitelist of external columns to add. Without this,
                   all non-key columns are joined.
  on_unmatched     What to do with rows whose key has no match.
                     keep_null         -- numeric NaN, string None
                     use_unknown_token -- integer ID columns get the
                                          asset's _unknown index
                     drop_row          -- exclude unmatched cohort rows

---

Primary-Key Cheat Sheet
========================

Per-asset key formats and common pitfalls:

```
asset       key column          format            common pitfall
----------- ------------------- ----------------- ------------------------------------
ndc         ndc                 11-digit string   cohort sometimes has 10-digit form
                                                  (missing leading zero) -- normalize
npi         NPI                 10-digit string   cohort sometimes int -- cast to str
ncpdp       ncpdp               7-digit string    leading zeros must be preserved
zip3        zip3                3-char string     derived from zip5[:3]
zip5        zip5                5-char string     9-digit ZIP+4 must be truncated
                                                  to 5 chars; preserve leading zeros
patient_id  patient_id_encoded  hash/UUID         cohort uses patient_id_encoded
                                                  (not raw patient_id) for joins
```

When a join's match rate is unexpectedly low, the first thing to check
is format normalization on either side.

---

What `join` Does NOT Do
========================

  - Does NOT mutate any file.
  - Does NOT write to _WorkSpace/.
  - Does NOT update RecordFn / CaseFn config files.
  - Does NOT cast or normalize keys silently -- it reports the match
    rate as-is and flags suspected format mismatches for the user to
    decide.

The only output is the textual preview (numbers + samples + YAML
snippet). The user copies the snippet into the appropriate cohort
layer's config and runs the actual cook there.
