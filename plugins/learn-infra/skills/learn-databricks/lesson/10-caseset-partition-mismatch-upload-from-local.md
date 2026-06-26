# Lesson 10: CaseSet Partition Mismatch — Upload Full Local Store

## The Problem

When Stage 3 (Case) runs on Databricks, it may produce a **non-partitioned CaseSet** — a single `@v0CaseSet-REACHADHDLabeledVisit/` folder. But Stage 4 (AIData) expects **partitioned** CaseSet folders in the `@i{idx}n{total}` format:

```
# What Stage 4 expects (partitioned, from local pipeline):
3-CaseStore/
└── hHmREACHPtt/
    ├── @i1n10-@v0CaseSet-REACHADHDLabeledVisit/
    ├── @i2n10-@v0CaseSet-REACHADHDLabeledVisit/
    ├── ...
    └── @i10n10-@v0CaseSet-REACHADHDLabeledVisit/

# What Stage 3 on Databricks produced (non-partitioned):
3-CaseStore/
└── hHmREACHPtt/
    └── @v0CaseSet-REACHADHDLabeledVisit/
```

Stage 4's `discover_caseset_partitions()` function looks for `@i{N}n{M}` prefixed folders. When it finds none, it returns an empty list, causing:

```
ValueError: Unable to concatenate an empty list of datasets.
```

## Why This Happens

The local pipeline's CaseSet builder uses a partitioned writer that splits patients across `n` shards (typically 10). This is for parallel processing and memory efficiency. On Databricks, the single-node execution may skip partitioning or use a different default.

## The Workaround

Upload the full CaseStore from your local machine to the Databricks Volume:

```bash
# Upload the 10-partition CaseStore from local to Volume
databricks fs cp -r \
  _WorkSpace/3-CaseStore/hHmREACHPtt/ \
  dbfs:/Volumes/cdhai_welldoc_space/haipipe/reach_space/_WorkSpace/3-CaseStore/hHmREACHPtt/ \
  --profile cdhai-new --overwrite
```

After upload, the Volume has the partitioned format and Stage 4 succeeds.

## Proper Fix (TODO)

The root cause is in the CaseSet builder's Databricks codepath — it should produce the same partitioned output format regardless of where it runs. The relevant code is:

- `discover_caseset_partitions()` in `haiutils/haistep/aidata_utils.py`
- CaseSet writer in `haipipe/case_base/builder/`

Until fixed, uploading the local CaseStore is a reliable workaround. The upload is ~100 MB and takes 2-3 minutes.

## When to Apply

- Any time Stage 4 (AIData) fails with "Unable to concatenate an empty list of datasets" on Databricks
- Check `3-CaseStore/<human>/` on the Volume — if you see `@v0CaseSet-*` without `@i{N}n{M}` prefix, partition mismatch is the cause
- Workaround is idempotent — re-uploading local CaseStore won't break anything
