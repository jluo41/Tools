haipipe External: Asset Model
=============================

The one reference for how external data is described, versioned, served, and
attached. Other skills point here instead of restating it.

**Status (JL, 260923).** The model below is adopted. The framework code
(`code/haipipe/external_base/`) is not built yet. Until it is, SourceFns keep
the v4 attach helpers (`attach_external_fields`, `<field>_ids`,
`<field>_matched`, `external_release`) and legacy `@{tag}` releases stay
readable. Signatures in § Lookup interface are the target contract; the
returned column names are provisional until the reference implementation
(DrFirst `b51/j01_asset_zip3`) lands.

---

Contract vs data
================

Two things are versioned separately:

```
contract   what an asset IS: key, fields, family, time rules, providers.
           One asset.yaml per asset. The same for every provider.
data       which values, as of when. Depends on the provider:
           built folders (local), event_time snapshots (feature store),
           API versions (third party).
```

A SourceFn depends on the contract. Which provider answers is configuration.

---

ExternalStore layout (topic-wise)
=================================

```
_WorkSpace/ExternalStore/
  <asset>/                      one folder per topic, e.g. npi, zip3, npi_engagement
    asset.yaml                  the contract
    @raw/                       vendor or API landings for this asset (local only)
    <version>/                  one built version or one frozen snapshot
      df_<asset>_id.parquet     ID-mapped values
      column_to_<asset>_li.pkl  vocabulary (index 0 _unknown, 1 _mask)
      README.md
      version.yaml
  _locks/
    <LockName>.yaml             which version of each asset a SourceFn uses
  @<tag>/                       LEGACY release-wide folder (e.g. @260104R4); read-only
```

Version names say what the data is:

```
vendor release   NPPES202507, ACS2019_2023
data year        2025
snapshot date    S20260104        (engagement builds and frozen API/FS pulls)
```

```yaml
# <asset>/asset.yaml
asset: npi
contract_version: 1
family: dimension               # dimension | engagement
key: {name: NPI, kind: npi}     # kind: zip3 | zip5 | npi | ndc | ncpdp | patient_id
fields: [Specialty, Credential, Gender]
temporal: false                 # engagement: true
leak_policy: nearest_allowed    # engagement: strict
providers:
  train: local_external_store   # training ALWAYS reads frozen local versions
  serve: local_external_store   # or feature_store | third_party_api
serve:                          # only when providers.serve is live
  max_staleness: 14d            # newer data required at serving, else fallback
  log_responses: true           # keep what the live provider answered
```

```yaml
# a multi-step asset: the key the cohort has is not the key the provider uses
asset: patient_engagement
family: engagement
key: {name: patient_id, kind: patient_id}
chain:                          # hops run in order; each hop's output keys the next
  - {group: patient-id-fg,         in: patient_id,        out: global_patient_id}
  - {group: patient-engagement-fg, in: global_patient_id}
temporal: true
leak_policy: strict
providers: {train: local_external_store, serve: feature_store}
```

```yaml
# <asset>/<version>/version.yaml
asset: npi
version: NPPES202507
ValidFromDT: 2025-07-15         # when this data became available to us
ValidToDT: null
RefPeriod: "NPPES 2025-07"      # what period it describes (label only)
source: "@raw/NPPES_Data_Dissemination_July_2025"
builder: "b51/j03_asset_npi/t02_build_NPPES202507/runs/r01_build.sh"
sha256: {df_npi_demo_id.parquet: "..."}
```

```yaml
# _locks/OptTimeR1v1.yaml
lock: OptTimeR1v1
assets: {zip3: "2025", npi: NPPES202507, npi_engagement: S20260104}
```

A version folder is immutable and self-contained, so it zips cleanly for
transport (endpoint package, S3 share). Unzip before reading; parquet is not
read efficiently from inside a zip, and `sha256` verifies the result. An
endpoint packages only the versions its lock names, never `@raw/`.

---

Providers and environments
==========================

```
provider               contract pins            data versions           train                     serve
---------------------  -----------------------  ----------------------  ------------------------  ----------------
local_external_store   key, fields              built <version>/        the pinned version        pinned, packaged
feature_store          group + schema           event_time snapshots    frozen S<date> pull       online latest
third_party_api        vendor API version       whenever called         frozen S<date> pull       live call
local_service          as the one it mimics     as the one it mimics    tests only                tests only
```

`env` is `train` or `serve` and selects `providers.<env>` from asset.yaml.

**Record and replay.** Training never calls a live service. A feature-store or
API pull for training is frozen into `<asset>/S<date>/` first (`fn-freeze`),
and every rebuild replays it through `local_external_store`. Only `serve`
calls live providers. This is the rule `haipipe-data-source` states as "no
uncontrolled live API calls inside SourceFn".

**Parity.** An asset with a live serving provider carries a parity check: the
same keys through the frozen version and the live provider give the same
fields (`fn-parity`).

**Multi-step lookups (`chain`).** When the provider keys differ from the
cohort's key (patient_id -> global_patient_id -> engagement), asset.yaml lists
the hops. The lookup runs them in order, applies `obs_dt` at every hop, and a
miss at any hop is a miss for the row (`_matched=False`). A frozen version
stores the final answer per original key, so training replays one table.

Feature-store history
---------------------

- `event_time` must mean when a snapshot was COMPUTED (its data cutoff), not
  when the underlying event happened. Otherwise a point-in-time pull picks
  the wrong snapshot.
- Offline-store history starts at the first ingestion. A cohort whose
  observation window is earlier has nothing valid to look up. Backfill first:
  re-run the feature query with past cutoffs (e.g. weekly) and ingest each with
  its past `event_time`, then freeze (`fn-freeze` § Backfill).
- Never train on a latest-per-key dedup of the offline store: it attaches
  values computed after the rows they serve.

Serving: staleness, fallback, logging
-------------------------------------

- `max_staleness`: at serving, a live answer whose snapshot is older than
  this falls back (defaults, `_matched=False`) instead of silently serving
  stale values; the endpoint reports the fallback rate.
- Fallback: an outage, a timeout, or a missing key returns defaults and
  `_matched=False`, so the model still scores. Training learned the same
  unmatched pattern.
- `log_responses`: the serving lookup keeps what the live provider answered
  (key hash, fields, snapshot time, provider) in a governed store, never in
  plain logs. A later training set can replay exactly what production saw
  instead of re-deriving it; such a log is frozen into `<asset>/S<date>/`
  like any other pull.

Serving: the endpoint bundle (local_external_store)
---------------------------------------------------

An endpoint that serves pinned local versions ships them in its package
(`external/`), and the same `ExternalLock` resolves them there. Full tables
make the container slow to start and heavy per worker (DrFirst OptTime: 17 s
for the first request, 4.0 GB per worker). Stage the bundle this way:

- **Only the lock.** Copy `_locks/<lock>.yaml`, and for each pinned asset its
  `asset.yaml` and `<version>/`. An asset the SourceFn never looked up is not
  shipped.
- **Only the fields training used.** The training SourceSet's
  `external-dependency.json` lists, per asset, its lock, pinned version and
  every lookup's fields. Keep the key plus the union of those fields. The
  shipped `asset.yaml` lists only them. The shipped `version.yaml` has the
  trimmed table's `sha256`, with the original `sha256` and the kept columns
  under `trimmed_from`, so the loader's checks run unchanged. Stop if the
  dependency's lock or version differs from the bundle's.
- **Pre-keyed.** For a number-like key (zip3, zip5, npi, ndc, ncpdp), store
  `__key__` = `haipipe.external_base.keys.normalize_keys(key, kind)` as int64,
  with invalid keys dropped and the first row per key kept (what the loader
  would compute), and write `key_normalized: int64` in `version.yaml`. The
  loader then indexes `__key__` directly instead of re-keying at start
  (DrFirst `ext_npi`: about 9 s down to about 1 s).
- **A record.** `external/_bundle.yaml` lists every asset: shipped or not
  (and why), columns before and after, and size before and after.

Loading at serving:

- **Once per process, never per request.** `lock.asset()` builds a new
  provider on every call, so the Input2SrcFn keeps one `ExternalAsset` per
  `(asset, env)` for the life of the process.
- **At container start.** The Input2SrcFn exports `Warmup(SPACE)`, which runs
  one lookup per shipped asset. `Endpoint_Set.warmup()` calls it, so the
  first request pays nothing.
- **Memory is per worker.** Each gunicorn worker loads its own copy. Size the
  instance as workers × peak per worker, and set `MODEL_SERVER_WORKERS` when
  the CPU count would oversubscribe memory (DrFirst: 2 workers at about
  1.3 GB each on 8 GB).

Reference implementation: DrFirst-SPACE
`examples-3-model/Project-ExpModel-OptTime/tasks/b03_C_optimal_timing_serving/j01_opttime_endpoint_package/t01_endpoint_package/scripts/stage_external_bundle.py`
(`--dependency` trims and pre-keys) and
`t02_input2src_ext/scripts/build_input2src_extv260924.py` (asset cache and
`Warmup`).

---

Time rule
=========

Every lookup carries `obs_dt`: the row's observation time at training, `now`
at serving. It is required for every asset, so it can never be skipped by
accident. (Term: a point-in-time join; `obs_dt` follows haipipe's `ObsDT`.)

```
snapshot choice   newest version with ValidFromDT <= obs_dt
                  (searchsorted over the asset's versions; merge_asof for FS offline)
leak_policy
  strict            no valid version -> unmatched, never a later version   (engagement)
  nearest_allowed   no valid version -> oldest version, flagged            (slow reference data)
```

- "Static" reference data (zip3, NPI, NDC) also changes; it is versioned and
  chosen by date like everything else, with the looser policy.
- `ValidFromDT` is availability, not the period described: ACS "2023" 5-year
  data published in Dec 2024 is not valid for a Mar 2024 row.
- Engagement assets summarize a past cohort. Their `ValidFromDT` must follow
  the build's data cutoff, and a rebuild that includes the modeled period
  leaks the outcome.

---

Key rule (PHI)
==============

- `third_party_api` and `local_service` accept non-patient keys only: zip3,
  zip5, npi, ndc, ncpdp.
- Assets keyed by `patient_id` use internal providers only (feature store,
  local ExternalStore).
- The client refuses the combination; a config edit cannot enable it.
- A de-identified cohort key (`patient_id_encoded`) does not join a
  feature-store `patient_id`. That join happens upstream, where real ids live.

---

Lookup interface (target contract)
==================================

Words: the lookup returns external FIELDS (Source-stage values), not features.
Features are CaseFn outputs; the feature vector is the AIData model input.

```python
from haipipe.external_base import ExternalAsset, ExternalLock

npi  = ExternalAsset('npi', version='NPPES202507', env='train')
lock = ExternalLock('OptTimeR1v1')              # optional: versions from _locks/
npi  = lock.asset('npi', env='train')

f = npi.lookup(keys=df_rx['prescriber_npi'],    # normalized by key kind
               obs_dt=df_rx['DT'],              # per row; 'now' at serving
               fields=['Specialty', 'Credential'],
               encode='raw')                    # 'raw' values | 'ids' vocab ids

# f: same index and order as df_rx, one row per input row
# Specialty | Credential | _matched | _snapshot_dt | _ref_period | _release
```

The lookup guarantees:

- key normalization (NPI 10, NDC 11, NCPDP 7 digits); invalid keys unmatched
- snapshot choice by `obs_dt`, the leak policy, `chain` hops
- defaults plus `_matched=False` on a miss, outage, timeout, or stale answer
- unknown `fields` stop the run
- de-duplicated keys, batched calls (e.g. 100 ids per feature-store call),
  a per-run cache, bounded retries with timeouts, and the provider's rate limit
- every call recorded for `external-dependency.json`; serving answers logged
  when `log_responses` is on

The lookup does NOT join, rename, or choose tables. The SourceFn does.

---

SourceFn pattern
================

Explicit, one block per asset, every field assigned by name:

```python
def enrich_Rx(df_rx, lock, env):
    npi = lock.asset('npi', env=env).lookup(
        keys=df_rx['prescriber_npi'], obs_dt=df_rx['DT'],
        fields=['Specialty', 'Credential'])
    df_rx['npi_specialty']  = npi['Specialty']
    df_rx['npi_credential'] = npi['Credential']
    df_rx['npi_matched']    = npi['_matched']
    df_rx['npi_snapshot_dt'] = npi['_snapshot_dt']
    return df_rx
```

- Temporal assets attach only to tables with a row time (`invitation`, `Rx`,
  events). A one-row-per-patient table gets reference data looked up at the
  patient's first observation time.
- One plain `enrich_<table>()` per table is shared by the SourceFn (`train`)
  and `Input2SrcFn` (`serve`, `obs_dt='now'`), so the two cannot drift.
- Every new column is listed in `ProcName_to_columns`.
- The SourceFn writes `external-dependency.json` beside the SourceSet: lock,
  asset versions, provider, match rate, and leak-dropped count per asset.

---

Downstream boundaries
=====================

```
SourceFn     looks up and assigns external fields                (only place)
RecordFn     aligns them in entity/time; never re-joins
CaseFn       encodes them; never calls context.get_external_path
Input2SrcFn  same enrich_<table>() with env=serve
```

Legacy CaseFns that open `@{tag}` folders directly stay valid until their
SourceFn moves to this model; the move is proven by an identical AIDataSet.

---

Build Block (b51)
=================

External assets are built in an auxiliary Block (`b51`-`b59`, see
`haipipe-task/ref/hierarchy.md`). Same Job ranges as the data Blocks:

```
b51_<name>_externalstore/
  src/                          shared builders + config-defaults.yaml
  j01_asset_<asset>/ ...        topic Jobs j01-j48, one per asset
    t01_contract/               writes asset.yaml                          (every provider)
    t02_build_<Version>/        local: build from @raw                     (one Task per version)
    t02_freeze_<SDate>/         feature store / API: freeze a pull
    t03_validate/               schema, key coverage, ValidFromDT, leak dates
    t04_parity/                 frozen vs live, same keys                  (live providers only)
  j49_external_locks/           t01_lock_<LockName>: spans every asset
  j51_release_<tag>/            a legacy frozen release, audit only (dated frozen thing = j5N range)
```

Suggested topic numbering: dimensions `j01`-`j09`, engagement `j11`-`j19`,
feature-store assets `j21`-`j29`, third-party assets `j31`-`j39`.

---

Legacy releases
===============

`@{YYMMDD}R{N}` folders (e.g. `@260104R4`) are frozen, undocumented bundles of
many assets. Do not build new locks or `version.yaml` files on top of them.
Rebuild each asset from `@raw/` with a documented builder, compare against the
legacy asset once, and retire the legacy folder when no SourceFn or CaseFn
reads it.
