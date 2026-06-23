haipipe Stage 0: External
==========================

Stage reference for the External pantry. Externals are reference assets
that any cohort-scoped Stage 1-4 chef can pull from. They are NOT a layer
in series with Source -> Record -> Case -> AIData -- they sit sideways.

**Scope:** Framework patterns and the current implementation reality.
Does not catalog which specific assets exist (that lives in
ref/asset-catalog.md, discovered at runtime from
_WorkSpace/ExternalStore/).

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
            Layer 3: Case  <----+
                  ^             |
            Layer 2: Record  <--+----  External (pantry)
                  ^             |        - dimension assets
            Layer 1: Source     |        - engagement assets
                  ^             |
                Raw  <----------+
```

Externals are loaded and joined inside Record / Case / AIData chefs by
primary key (NPI, NDC, NCPDP, zip3, zip5, patient_id). They are NOT
chained behind Source. A cohort can be processed end-to-end with no
externals at all -- they are an enrichment pantry, not a prerequisite.

---

Cooking Metaphor
================

```
Concept    Pipeline Term              Location
---------  -------------------------  ------------------------------------------
Pantry     ExternalStore              _WorkSpace/ExternalStore/@{version}/
Recipe     e_build_external_*.py      code-dev/0-EXTERNAL/
Pantry     ExternalFn                 (NOT YET A CLASS -- Phase 2 promotion)
  Chef                                Currently: top-level scripts that import
                                      from haipipe.base
Output     ExternalAsset triplet      df_{asset}_id.parquet +
                                      column_to_{asset}_li.pkl +
                                      README.md
```

In Phase 1, "Chef" is metaphorical -- there is no `ExternalFn` class.
Each `e{N}_build_external_<asset>.py` is a self-contained build script
that imports `setup_workspace` from haipipe.base, defines its inputs,
and writes the asset triplet. Phase 2 (deferred) would promote these to
generated `ExternalFn` modules under `code/haifn/fn_external/`.

---

What Is an ExternalAsset
=========================

An ExternalAsset is the directory of files produced by one
`e_build_external_<asset>.py` script:

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

Downstream code joins on `_original`. Embedding-based models read the
integer column.

---

Two Asset Families
==================

Externals split into two semantically distinct families. Treat them
differently for staleness and rebuild triggers.

**dimension** -- vendor-sourced lookup tables.

  Source:    @raw/ vendor data (NPPES, ZipInfo/{Zip3,Zip5}, drug DB,
             physician review CSVs)
  Refresh:   when the vendor releases new data (e.g. NPPES monthly,
             ADI yearly)
  Examples:  ndc, npi, ncpdp, zip3, zip5
  Stable:    yes -- safe to reuse across cohorts

**engagement** -- cohort-aggregated stats keyed by an external dimension.

  Source:    a cohort SourceSet (e.g. 20250218_SMSAll/...)
  Refresh:   when the source cohort changes
  Examples:  ndc_engagement, npi_engagement, ncpdp_engagement,
             zip3_engagement, zip5_engagement, patient_engagement
  Stable:    no -- bound to the cohort that produced it. Re-derive
             when adding a new cohort if cohort-specific aggregates
             are needed.

The boundary matters because dimension and engagement assets have
different correctness criteria. A stale dimension asset means "vendor
data is older than current"; a stale engagement asset means "cohort
state has drifted from the asset's snapshot". The skill's `review` and
`refresh` verbs check both kinds of staleness.

---

Versioning
==========

```
_WorkSpace/ExternalStore/
  @{version}/                e.g. @260104R4 (date-tagged release)
    {asset}/...
```

  - `@{version}/` is a **release**: a frozen set of assets cooked
    together at a point in time. Treat as immutable once published.
  - The `EXTERNAL_VERSION` env var (env.sh) names the active default
    release. The skill defaults to that release; pin a different one
    with `--version @{tag}`.
  - Old releases are kept for reproducibility (RecordFn / CaseFn configs
    can pin a specific release). Never overwrite an existing release
    folder without explicit user confirmation.
  - Naming convention observed in the repo: `@{YYMMDD}R{N}`
    (e.g. @260104R4 = 4th release on 2026-01-04). Not enforced.

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

`SPACE['LOCAL_EXTERNAL_STORE']` resolves to
`_WorkSpace/ExternalStore/{EXTERNAL_VERSION}` (e.g.
`_WorkSpace/ExternalStore/@260104R4`). Pin a different release by
exporting `EXTERNAL_VERSION` before sourcing env.sh.

**Cooking (rebuilding) an asset:**

```bash
source .venv/bin/activate && source env.sh
python code-dev/0-EXTERNAL/e2_build_external_npi.py
```

Each builder is self-contained: it reads its raw inputs, writes the
asset triplet to `SPACE['LOCAL_EXTERNAL_STORE']/{OUTPUT_DIR_NAME}/`,
and prints a verification block at the end.

---

How Externals Get Used Downstream
==================================

Externals are not consumed by Source. Source is cohort-scoped and
deidentified -- it produces the typed Ptt/invitation/Rx tables. The
join into externals happens in Record or Case.

A typical join (illustrative):

```
RecordFn / CaseFn config:
  externals:
    npi:
      version: '@260104R4'
      source:  ExternalStore/@260104R4/npi
      join_key: prescriber_npi -> NPI_original
      columns:  [Specialty, Credential, Big5*, MIPS_score]
```

  - `join_key` left side is the cohort column (`Rx.prescriber_npi`).
  - Right side is the external's `_original` column (the un-mapped
    string version of the primary key).
  - `columns` selects which external columns to add. Defaults to all
    if omitted.

The skill's `join` verb does NOT execute this -- it only previews:
match rate, top unmatched keys, columns that would be added, and the
config snippet to paste into the consuming layer.

---

Discovering Available Assets
=============================

Always discover at runtime; the catalog can grow:

```bash
ls _WorkSpace/ExternalStore/                          # available releases
ls _WorkSpace/ExternalStore/{EXTERNAL_VERSION}/       # assets in active release
ls code-dev/0-EXTERNAL/                               # registered builder scripts
cat _WorkSpace/ExternalStore/{EXTERNAL_VERSION}/{asset}/README.md
```

For the canonical catalog (asset name, primary key, source, columns),
see ref/asset-catalog.md.

---

Prerequisites
=============

```bash
source .venv/bin/activate && source env.sh
```

Both required for `cook`, `refresh`, and `load`. The env vars
`LOCAL_EXTERNAL_STORE` and `EXTERNAL_VERSION` come from env.sh; the
builders fail without them.

`source .venv/bin/activate` does NOT persist across Bash tool calls.
Always chain: `source .venv/bin/activate && source env.sh && python <script>`
Or call venv python directly: `.venv/bin/python script.py`

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

---

MUST NOT
========

1. **NEVER edit** assets under `_WorkSpace/ExternalStore/@{version}/`
   directly -- they are builder outputs
2. **NEVER edit** `code/haifn/fn_external/` (does not exist in Phase 1;
   if Phase 2 promotion happens, it becomes generated and read-only)
3. **NEVER materialize** a join inside this skill -- joins belong in
   RecordFn / CaseFn. The `join` verb is preview-only.
4. **NEVER assume** an asset's primary key from its folder name --
   read the README or the builder script.
5. **NEVER mix** vocabularies across releases -- the integer IDs in
   df_{asset}_id.parquet are only valid against the column_to_*_li.pkl
   from the same release.

---

Key File Locations
==================

```
Builder scripts:      code-dev/0-EXTERNAL/e{N}_build_external_*.py   <- discover with ls
Helpers (Phase 1):    duplicated inside each builder script
                      (build_vocabulary, convert_to_ids, generate_readme)
Asset outputs:        _WorkSpace/ExternalStore/@{version}/{asset}/
Active release:       env var EXTERNAL_VERSION (set in env.sh)
Raw vendor inputs:    _WorkSpace/ExternalStore/@raw/
Inference samples:    _WorkSpace/ExternalStore/@inference/
```
