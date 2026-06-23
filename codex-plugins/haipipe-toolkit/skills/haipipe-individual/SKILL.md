---
name: haipipe-individual
description: "Per-individual data contract skill. Builds and manages a single-individual slice of the pipeline at stages 0-2 (RawDataStore, SourceStore, RecStore) under _WorkSpace/A-User-Store/UserGroup-{dataset}/Subject-{id}. Use when the user asks to create, inspect, or clean per-individual folders, build individual samples from a dataset, or prepare data for endpoint inference. Trigger: individual, per-individual, single-individual, UserGroup, Subject-ID, A-User-Store, inference data, endpoint data, sample patient."
argument-hint: "[command] [args...]"
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Per-individual data contract skill."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-individual
======================

Per-individual data contract covering stages 0-2. One folder per individual, holding
just the data needed to serve them via a deployed endpoint. Stages 3-6 are for
model development and never appear per-individual — at inference time the individual
calls the endpoint directly.


Why stages 0-2 only
-------------------

  Stage           Role                              Per-individual?
  -----           ----                              ------------
  0-RawDataStore  original dataset files            YES  — individual's raw slice
  1-SourceStore   typed source frames               YES  — individual's rows
  2-RecStore      individual-centered records          YES  — individual's record(s)
  3-CaseStore     cohort cases                      NO   — training-time
  4-AIDataStore   model-ready tensors               NO   — training-time
  5-ModelInstance trained weights                   NO   — training artifact
  6-Endpoint      deployable                        NO   — shared by all individuals

A deployed endpoint reads the individual's 2-RecStore, runs inference, and returns
a prediction. It does NOT need 3-6.


Folder Layout  (FLAT — no dataset-name or partition wrappers nested inside)
-------------

  _WorkSpace/A-User-Store/
  ├── UserGroup-OhioT1DM/
  │   ├── Subject-540/
  │   ├── Subject-559/
  │   │   ├── 0-RawDataStore/               ← just the raw file names, flat
  │   │   │   ├── 559-ws-training.xml
  │   │   │   └── 559-ws-testing.xml
  │   │   ├── 1-SourceStore/                ← filtered source tables, flat
  │   │   │   ├── CGM.parquet
  │   │   │   ├── Diet.parquet
  │   │   │   ├── Exercise.parquet
  │   │   │   └── ...
  │   │   ├── 2-RecStore/                   ← filtered records, flat (no @iXnY)
  │   │   │   ├── Human-HmPtt/Human2RawNum.parquet
  │   │   │   ├── Record-HmPtt.CGM5Min/{RecAttr,RecIndex}.parquet
  │   │   │   ├── Record-HmPtt.Diet5Min/...
  │   │   │   └── ...
  │   │   └── manifest.yaml                 ← source_set, rec_set, partition, provenance
  │   └── ...
  ├── UserGroup-mimiciv-3.1/
  │   ├── Subject-10000032/                ← MIMIC partitions (@iXnY) are collapsed
  │   └── ...
  └── UserGroup-WellDoc2022CGM/
      ├── Subject-26/
      └── ...

Flattening rules (build script strips these wrapper segments):
  - dataset-name wrappers inside 1-SourceStore/ (e.g. `OhioT1DM/@OhioT1DMxmlv250302/`)
  - rec-set wrappers inside 2-RecStore/ (e.g. `OhioT1DM_v0RecSet/`)
  - partition wrappers `@iXnY/` (individual's data lives in only one partition anyway)
  - cohort nesting inside 0-RawDataStore/ (e.g. `Source/2018/train/` → flat)

Wrapper names preserved in manifest.yaml for provenance (source_set,
rec_set, rec_partitions_found_in), so you can always trace back to the
global store that seeded a individual.


Naming Convention
-----------------

  Parent:   UserGroup-{DatasetTag}
  Child:    Subject-{SubjectID}

  DatasetTag matches _WorkSpace/0-RawDataStore/ directory name (short form
  for long names):
    OhioT1DM                         → OhioT1DM
    mimiciv-3.1                      → mimiciv-3.1
    WellDoc2022CGM                   → WellDoc2022CGM

  SubjectID is the dataset's native identifier WITHOUT the dataset prefix
  (the prefix lives on the parent UserGroup-* folder):
    OhioT1DM     → 540, 544, 552, 559, 563, ...
    MIMIC-IV     → 10004235, 10009628, ...  (numeric individual_id)
    WellDoc      → 26, 48, ...              (study's individual number)

  Rationale: dataset-qualifying the PARENT folder instead of every individual
  folder name keeps individual paths short and makes cohort-level operations
  (list all MIMIC individuals, wipe one cohort) trivial.


Commands
--------

  /haipipe-individual                         → dashboard: list existing Subject-* folders
  /haipipe-individual dashboard               → same as above
  /haipipe-individual list [dataset]          → list individuals for one dataset
  /haipipe-individual inspect <Subject-*>     → show folder tree + manifest
  /haipipe-individual build <dataset> <id>    → build one individual folder
  /haipipe-individual build-samples           → build N samples per dataset (config-driven)
  /haipipe-individual clean <Subject-*>       → remove a individual folder (reversible via rebuild)
  /haipipe-individual spec                    → show full per-stage content spec


Build Logic (what `build` does)
--------------------------------

Given `{dataset, individual_id}` the build proceeds in 5 steps:

  Step 1  — mkdir
    Create Subject-{DatasetTag}-{id}/ under _WorkSpace/A-User-Store/UserGroup/.
    If folder exists and manifest is fresh → skip (idempotent).

  Step 2  — slice raw
    Copy or filter raw files from _WorkSpace/0-RawDataStore/{dataset}/
    scoped to individual_id. Format-specific:
      OhioT1DM     → copy {id}-ws-training.xml + {id}-ws-testing.xml
      MIMIC-IV     → filter each CSV on individual_id column, write slice
      WellDoc      → filter study CSV rows on individual_id
    Write into Subject-*/0-RawDataStore/.

  Step 3  — filtered source
    Run the existing fn_source.run() pipeline with a individual filter
    (Partition_Args['individual_id_filter'] = [individual_id]).
    Reads: Subject-*/0-RawDataStore/ (or global 0-RawDataStore/ + filter).
    Writes: Subject-*/1-SourceStore/{SourceSet}_v{ver}/.

  Step 4  — filtered record
    Run fn_record.run() against the filtered source from Step 3.
    Reads: Subject-*/1-SourceStore/.
    Writes: Subject-*/2-RecStore/{RecSet}/rec_{id}.parquet.

  Step 5  — manifest
    Write Subject-*/manifest.yaml with provenance:
      individual_id, dataset, source_raw_paths, source_set, rec_set,
      built_at, built_by (script version), build_args (filter config).


manifest.yaml schema
--------------------

```yaml
individual_id: "559"
dataset: "OhioT1DM"
dataset_tag: "OhioT1DM"
source_raw_paths:
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-training.xml"
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-testing.xml"
source_set: "OhioT1DM_v0"
rec_set: "OhioT1DM_v0RecSet"
built_at: "2026-04-20T14:30:00"
built_by: "build_sample_individuals.py v0.1"
build_args:
  individual_id_filter: ["559"]
```


Build Contract
--------------

The build MUST be deterministic and reproducible. A single script (planned:
`fn/build_sample_individuals.py`) owns this:

  1. Read sample config (which datasets, which individual IDs, N per dataset).
  2. For each (dataset, individual_id):
     a. Steps 1-5 from Build Logic.
     b. Idempotent: skip if manifest.built_at is fresh.
  3. Emit a build report (what was built, what was skipped, any errors).

Do NOT hand-edit per-individual folders. They are derived, not source of truth.
Source of truth = global _WorkSpace/0-RawDataStore/ + the build script.


Consumers
---------

  Deployed endpoints (stage 6) read:
    manifest.yaml       → dataset + rec_set identification
    2-RecStore/         → the record for inference
    (NEVER read 3-6 — those don't exist per-individual anyway.)

  Tutorials and demos read:
    0-RawDataStore/     → "here's what one individual's raw data looks like"
    manifest.yaml       → attribution and provenance

  Privacy / deletion:
    rm -rf Subject-{DatasetTag}-{id}/  → wipes ALL derived data for one individual.
    Global stores untouched; re-run build to regenerate.


Relationship to Project-Wide Stores
------------------------------------

  Global _WorkSpace/ stores = BATCH work (training, cohort analysis):
    0-RawDataStore/{dataset}/*   ← whole dataset
    1-SourceStore/{SourceSet}/*  ← all individuals combined
    2-RecStore/{RecSet}/*        ← all records

  Per-individual UserGroup/Subject-*/ = SINGLE-INDIVIDUAL serving:
    0-RawDataStore/             ← one individual's raw slice
    1-SourceStore/              ← one individual's source rows
    2-RecStore/                 ← one individual's record

  A per-individual folder is a VIEW of the global store, scoped to one ID,
  built by running the SAME pipeline with a individual filter.


Rules
-----

  - NEVER create stages 3-6 inside a Subject-*/ folder. Those are not per-individual.
  - ALWAYS dataset-qualify the folder name: Subject-{DatasetTag}-{id}.
  - ALWAYS write manifest.yaml — it's the provenance record.
  - If a dataset's raw format can't be cleanly sliced (e.g. proprietary binary),
    store a pointer manifest in 0-RawDataStore/ instead of copying.
  - The build script is the source of truth for how each dataset is sliced.
    Hand-curated individual folders drift and break — do not do it.
  - Individual folders are reproducible: `rm -rf` and re-run `build` must produce
    an equivalent folder (differences only in built_at timestamp).
