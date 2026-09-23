haipipe Stage 0: External
==========================

Stage reference for the External pantry.
Externals are versioned reference assets that SourceFn may attach to cohort data.
They are NOT a layer in series with Source -> Record -> Case -> AIData -- they are a governed input to Source.

**Read first:** `ref/asset-model.md` (JL, 260923) is the authority for
contracts, per-asset versions, locks, providers, the obs_dt time rule, the
lookup interface, and the b51 build Block. Where this file disagrees, the
asset model wins; this file keeps the asset file format and legacy detail.

**Scope:** Framework patterns and the current implementation reality.
Does not catalog which specific assets exist (that lives in ref/asset-catalog.md, discovered at runtime from _WorkSpace/ExternalStore/).

---

Architecture Position
=====================

```
            Layer 6: Endpoint
                  ^
            Layer 5: ModelInstance
                  ^
            Layer 4: AIData
                  ^
            Layer 3: Case
                  ^
            Layer 2: Record
                  ^
            Layer 1: Source  <------- ExternalStore
                  ^                    - dimension assets
                  |                    - engagement snapshots
                Raw
```

External assets are loaded by SourceFn and attached by primary key (NPI, NDC, NCPDP, zip3, zip5, patient_id).
RecordFn aligns the attached values to entity and time, including point-in-time selection for engagement snapshots; CaseFn selects, windows, aggregates, and encodes them.
A cohort can be processed end-to-end with no externals at all -- they are an enrichment pantry, not a prerequisite.

---

Cooking Metaphor
================

```
Concept    Pipeline Term              Location
---------  -------------------------  ------------------------------------------
Pantry     ExternalStore              _WorkSpace/ExternalStore/<asset>/<version>/
Label      asset.yaml                 _WorkSpace/ExternalStore/<asset>/asset.yaml
Recipe     build script               b51 Block: j0N_asset_<asset>/t02_build_<Version>/scripts/
                                      (legacy: code-dev/0-EXTERNAL/e{N}_build_external_*.py)
Order      lock                       _WorkSpace/ExternalStore/_locks/<LockName>.yaml
Output     ExternalAsset triplet      df_{asset}_id.parquet +
                                      column_to_{asset}_li.pkl +
                                      README.md (+ version.yaml)
```

Builders are Task scripts in the b51 Block, one Task per version; there is no
generated `ExternalFn` class. A build writes one immutable version folder.
---

What Is an ExternalAsset
=========================

An ExternalAsset is the directory of files produced by one `e_build_external_<asset>.py` script:

```
_WorkSpace/ExternalStore/@{version}/{asset}/
    df_{asset}_id.parquet            <- ID-mapped values (primary output)
    column_to_{asset}_li.pkl         <- vocabulary for decoding IDs
    README.md                        <- auto-generated schema + usage
    df_{asset}_raw.parquet           <- (engagement only) pre-ID-mapped raw
    df_{asset}_<auxiliary>.parquet   <- optional: secondary outputs
                                        (e.g. df_npi_to_zip5info.parquet)
```

Mandatory contract for every asset:

```
OUTPUT_DIR_NAME       Asset slug used as the folder name (e.g. 'npi')
DISPLAY_NAME          Human label for headers / READMEs (e.g. 'NPI')
PRIMARY_KEY           The single column that joins cohort data to this
                      asset (e.g. 'NPI', 'ndc', 'zip5')
column_to_value_list  Vocabulary dict per column. Index 0 is always the
                      `_unknown` token; index 1 is always `_mask`.
```

The primary key is preserved twice in the output:

```
{PRIMARY_KEY}_original   the original string value (for joining)
{PRIMARY_KEY}            the integer ID (for embedding layers)
```

Downstream code joins on `_original`.
Embedding-based models read the integer column.

---

Two Asset Families
==================

Externals split into two semantically distinct families.
Treat them differently for staleness and rebuild triggers.

**dimension** -- vendor-sourced lookup tables.

  Source:    @raw/ vendor data (NPPES, ZipInfo/{Zip3,Zip5}, drug DB,
             physician review CSVs)
  Refresh:   when the vendor releases new data (e.g. NPPES monthly,
             ADI yearly)
  Examples:  ndc, npi, ncpdp, zip3, zip5
  Stable:    yes -- safe to reuse across cohorts

**engagement** -- cohort-aggregated stats keyed by an external dimension.

  Source:    a cohort SourceSet (e.g. reach-adhd/... or mimiciv-3.1/...)
  Refresh:   when the source cohort changes
  Examples:  ndc_engagement, npi_engagement, ncpdp_engagement,
             zip3_engagement, zip5_engagement, patient_engagement
  Stable:    no -- bound to the cohort that produced it. Re-derive
             when adding a new cohort if cohort-specific aggregates
             are needed.

The boundary matters because dimension and engagement assets have different correctness criteria.
A stale dimension asset means "vendor data is older than current"; a stale engagement asset means "cohort state has drifted from the asset's snapshot".
The skill's `review` and `refresh` verbs check both kinds of staleness.

---

Versioning
==========

Current model (`ref/asset-model.md`): each ASSET is versioned on its own.

```
_WorkSpace/ExternalStore/
  <asset>/<version>/         e.g. npi/NPPES202507, npi_engagement/S20260104
    version.yaml             ValidFromDT, ValidToDT, RefPeriod, source, builder, sha256
  _locks/<LockName>.yaml     asset -> version pins for one SourceFn
```

  - A version is immutable once published. Never overwrite one without
    explicit user confirmation.
  - A lock replaces the old "one release for everything" default.
  - Lookups choose the version valid at each row's `obs_dt`.

Legacy model: `@{version}/` folders (e.g. `@260104R4`) froze many assets
together and the `EXTERNAL_VERSION` env var named the active one. They stay
readable for SourceFns and CaseFns that still pin them; build nothing new on
them.
---

Concrete Code
=============

**Loading an existing asset:**

```python
import pandas as pd
import pickle
import os

EXTERNAL_DIR = os.path.join(SPACE['LOCAL_EXTERNAL_STORE'], 'npi')

df_npi    = pd.read_parquet(os.path.join(EXTERNAL_DIR, 'df_npi_demo_id.parquet'))
with open(os.path.join(EXTERNAL_DIR, 'column_to_demo_li.pkl'), 'rb') as f:
    vocabs = pickle.load(f)

# Decode an ID column back to its original value
gender_id = df_npi.iloc[0]['Gender']
gender    = vocabs['Gender'][gender_id]
```

`SPACE['LOCAL_EXTERNAL_STORE']` resolves to `_WorkSpace/ExternalStore/{EXTERNAL_VERSION}` (e.g. `_WorkSpace/ExternalStore/@260104R4`).
Pin a different release by exporting `EXTERNAL_VERSION` before sourcing env.sh.

**Cooking (rebuilding) an asset:**

```bash
source .venv/bin/activate && source env.sh
python code-dev/0-EXTERNAL/e2_build_external_npi.py
```

Each builder is self-contained: it reads its raw inputs, writes the asset triplet to `SPACE['LOCAL_EXTERNAL_STORE']/{OUTPUT_DIR_NAME}/`, and prints a verification block at the end.

---

How Externals Get Used Downstream
==================================

SourceFn is the attachment boundary. It looks up each asset explicitly and
assigns every field by name (`ref/asset-model.md` § SourceFn pattern):

```python
npi = lock.asset('npi', env='train').lookup(
    keys=df_rx['prescriber_npi'], obs_dt=df_rx['DT'], fields=['Specialty'])
df_rx['npi_specialty'] = npi['Specialty']
df_rx['npi_matched']   = npi['_matched']
```

- Fields are data representations (scalars, lists, fixed-order vectors), not
  the final model vector.
- RecordFn preserves them while aligning entity and time; it never re-joins.
- CaseFn applies windows, aggregation, and encoding; it never opens
  ExternalStore (`context.get_external_path` is legacy).
- `Input2SrcFn` calls the same `enrich_<table>()` with `env='serve'` and
  `obs_dt='now'`.
- Vector fields declare stable ordering, dtype, missing behavior, and the
  version they came from.

Legacy (v4 contract, until external_base exists): SourceFns attach with
`attach_external_fields` from a contract dict and emit `<field>_ids`,
`<field>_matched`, and `external_release`. `ref/join-contract.md` documents
that form.
---

Discovering Available Assets
=============================

Always discover at runtime; the catalog can grow:

```bash
ls _WorkSpace/ExternalStore/                          # assets (topic folders) + legacy @{tag}
ls _WorkSpace/ExternalStore/<asset>/                  # asset.yaml + versions
cat _WorkSpace/ExternalStore/<asset>/asset.yaml
cat _WorkSpace/ExternalStore/<asset>/<version>/version.yaml
ls _WorkSpace/ExternalStore/_locks/
ls examples*/*/tasks/b51_*/j*_asset_*/                # asset build Jobs
```

For the canonical catalog (asset name, primary key, source, columns), see ref/asset-catalog.md.
---

Prerequisites
=============

```bash
source .venv/bin/activate && source env.sh
```

Both required for `cook`, `refresh`, and `load`.
The env vars `LOCAL_EXTERNAL_STORE` and `EXTERNAL_VERSION` come from env.sh; the builders fail without them.

`source .venv/bin/activate` does NOT persist across Bash tool calls.
Always chain: `source .venv/bin/activate && source env.sh && python <script>` Or call venv python directly: `.venv/bin/python script.py`

---

MUST DO
=======

1. **Activate .venv first**: `source .venv/bin/activate && source env.sh`
2. **Treat `@{version}/` as immutable** -- never overwrite a published
   release without explicit user confirmation
3. **Use `_original` columns for joins** -- the integer ID column is
   only meaningful with the matching vocabulary
4. **Distinguish dimension vs engagement** when reasoning about
   staleness -- they have different rebuild triggers
5. **Present plan to user and get approval** before any code changes
6. **Carry `obs_dt` on every lookup** and choose versions by `ValidFromDT`
7. **Freeze before training** on any feature-store or API data

---

MUST NOT
========

1. **NEVER edit** assets under `_WorkSpace/ExternalStore/@{version}/`
   directly -- they are builder outputs
2. **NEVER treat builders as generated Fns** -- they are b51 Task scripts;
   there is no `code/haifn/fn_external/` (if one appears, it is generated
   and read-only)
3. **NEVER materialize** a cohort join inside this skill -- the `join` verb is
   preview-only. Put the real attachment in a SourceFn builder.
4. **NEVER assume** an asset's primary key from its folder name --
   read the README or the builder script.
5. **NEVER mix** vocabularies across versions -- the integer IDs in
   df_{asset}_id.parquet are only valid against the column_to_*_li.pkl
   from the same version.
6. **NEVER call a live provider for training**, and never send a
   `patient_id` key to a third-party or local-service provider.

---

Key File Locations
==================

```
Asset model:          ref/asset-model.md                              <- authority
Builder scripts:      b51 Block, j0N_asset_<asset>/t02_build_<Version>/scripts/
                      (legacy: code-dev/0-EXTERNAL/e{N}_build_external_*.py)
Shared build helpers: b51 Block src/ (build_vocabulary, convert_to_ids, generate_readme)
Asset contract:       _WorkSpace/ExternalStore/<asset>/asset.yaml
Asset versions:       _WorkSpace/ExternalStore/<asset>/<version>/ (+ version.yaml)
Locks:                _WorkSpace/ExternalStore/_locks/<LockName>.yaml
Raw vendor inputs:    _WorkSpace/ExternalStore/<asset>/@raw/  (legacy: ExternalStore/@raw/)
Legacy releases:      _WorkSpace/ExternalStore/@{tag}/ ; env var EXTERNAL_VERSION
Inference samples:    _WorkSpace/ExternalStore/@inference/
```
