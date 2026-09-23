fn-freeze: Freeze a live pull into a local snapshot
===================================================

Turns a feature-store or third-party API answer into an immutable
`<asset>/S<date>/` version, so training can replay it
(`ref/asset-model.md` § Record and replay). Training never calls the live
provider; this is the only door from live data into training.

Runs as a b51 Task: `j0N_asset_<asset>/t02_freeze_S<yyyymmdd>/`.

---

Step 1: Check the contract
--------------------------

```bash
cat _WorkSpace/ExternalStore/<asset>/asset.yaml
```

- `providers.serve` must be `feature_store` or `third_party_api`.
- Key kind `patient_id` with `third_party_api`: STOP (PHI rule).
- No asset.yaml: write it first (`t01_contract`).

---

Step 2: Choose the key set and the time
---------------------------------------

- Keys: the union of keys the training cohorts need (from their SourceSets or
  the cohort's raw key columns). Never send patient keys to a third party.
- Time:
  - feature store offline: a point-in-time pull, one row per (key, snapshot)
    with `event_time` <= each snapshot date. NEVER a latest-per-key dedup
    for training: it attaches values computed after the rows it serves.
  - third-party API: answers are "as of now"; the snapshot date is the call
    date.
  - chained assets (`chain:` in asset.yaml): run every hop at the same
    snapshot time and store the final answer per original key.

---

Backfill (feature store, when history is short)
-----------------------------------------------

Check the offline store's earliest `event_time` against the earliest
observation time of every cohort the version will serve. If history starts
later:

1. Confirm `event_time` is the snapshot's computation cutoff, not the event
   date (ask the feature-group owner if the ingestion code does not say).
2. Re-run the feature query with past cutoffs at the ingestion cadence
   (e.g. weekly), each using only data before its cutoff.
3. Ingest each result with its past `event_time`.
4. Then pull point-in-time as in Step 2.

Without a backfill, rows before the first snapshot are unmatched under
`leak_policy: strict`; say so in the Task page rather than loosening the
policy.

---

Step 3: Pull and write the version
----------------------------------

Write `<asset>/S<yyyymmdd>/` with the asset triplet plus `version.yaml`:

```yaml
asset: <asset>
version: S20260923
ValidFromDT: 2026-09-23          # call date, or the event_time cutoff for FS pulls
RefPeriod: "<provider> as of 2026-09-23"
source: "feature_store:<group>@<event_time cutoff>"   # or "third_party_api:<vendor>/<api_version>"
builder: "b51/j0N_asset_<asset>/t02_freeze_S20260923/runs/r01_freeze.sh"
sha256: {...}
```

Row values are never printed; report shape, key coverage, and the written path.

---

Step 4: Hand off
----------------

- Run `t03_validate` on the new version.
- Run `fn-parity` if the asset serves live.
- Add the version to a lock (`fn-lock`) only after both pass.
