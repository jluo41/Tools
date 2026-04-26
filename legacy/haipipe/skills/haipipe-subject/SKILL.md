---
name: haipipe-subject
description: "Per-subject data contract skill. Builds and manages a single-subject slice of the pipeline at stages 0-2 (RawDataStore, SourceStore, RecStore) under _WorkSpace/A-User-Store/UserGroup-{dataset}/Subject-{id}. Use when the user asks to create, inspect, or clean per-subject folders, build subject samples from a dataset, or prepare data for endpoint inference. Trigger: subject, per-subject, single-subject, UserGroup, Subject-ID, A-User-Store, inference data, endpoint data, sample patient."
argument-hint: [command] [args...]
---

Skill: haipipe-subject
======================

Per-subject data contract covering stages 0-2. One folder per subject, holding
just the data needed to serve them via a deployed endpoint. Stages 3-6 are for
model development and never appear per-subject — at inference time the subject
calls the endpoint directly.


Why stages 0-2 only
-------------------

  Stage           Role                              Per-subject?
  -----           ----                              ------------
  0-RawDataStore  original dataset files            YES  — subject's raw slice
  1-SourceStore   typed source frames               YES  — subject's rows
  2-RecStore      subject-centered records          YES  — subject's record(s)
  3-CaseStore     cohort cases                      NO   — training-time
  4-AIDataStore   model-ready tensors               NO   — training-time
  5-ModelInstance trained weights                   NO   — training artifact
  6-Endpoint      deployable                        NO   — shared by all subjects

A deployed endpoint reads the subject's 2-RecStore, runs inference, and returns
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
  - partition wrappers `@iXnY/` (subject's data lives in only one partition anyway)
  - cohort nesting inside 0-RawDataStore/ (e.g. `Source/2018/train/` → flat)

Wrapper names preserved in manifest.yaml for provenance (source_set,
rec_set, rec_partitions_found_in), so you can always trace back to the
global store that seeded a subject.


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
    MIMIC-IV     → 10004235, 10009628, ...  (numeric subject_id)
    WellDoc      → 26, 48, ...              (study's subject number)

  Rationale: dataset-qualifying the PARENT folder instead of every subject
  folder name keeps subject paths short and makes cohort-level operations
  (list all MIMIC subjects, wipe one cohort) trivial.


Commands
--------

  /haipipe-subject                         → dashboard: list existing Subject-* folders
  /haipipe-subject dashboard               → same as above
  /haipipe-subject list [dataset]          → list subjects for one dataset
  /haipipe-subject inspect <Subject-*>     → show folder tree + manifest
  /haipipe-subject build <dataset> <id>    → build one subject folder
  /haipipe-subject build-samples           → build N samples per dataset (config-driven)
  /haipipe-subject clean <Subject-*>       → remove a subject folder (reversible via rebuild)
  /haipipe-subject spec                    → show full per-stage content spec


Build Logic (what `build` does)
--------------------------------

Given `{dataset, subject_id}` the build proceeds in 5 steps:

  Step 1  — mkdir
    Create Subject-{DatasetTag}-{id}/ under _WorkSpace/A-User-Store/UserGroup/.
    If folder exists and manifest is fresh → skip (idempotent).

  Step 2  — slice raw
    Copy or filter raw files from _WorkSpace/0-RawDataStore/{dataset}/
    scoped to subject_id. Format-specific:
      OhioT1DM     → copy {id}-ws-training.xml + {id}-ws-testing.xml
      MIMIC-IV     → filter each CSV on subject_id column, write slice
      WellDoc      → filter study CSV rows on subject_id
    Write into Subject-*/0-RawDataStore/.

  Step 3  — filtered source
    Run the existing fn_source.run() pipeline with a subject filter
    (Partition_Args['subject_id_filter'] = [subject_id]).
    Reads: Subject-*/0-RawDataStore/ (or global 0-RawDataStore/ + filter).
    Writes: Subject-*/1-SourceStore/{SourceSet}_v{ver}/.

  Step 4  — filtered record
    Run fn_record.run() against the filtered source from Step 3.
    Reads: Subject-*/1-SourceStore/.
    Writes: Subject-*/2-RecStore/{RecSet}/rec_{id}.parquet.

  Step 5  — manifest
    Write Subject-*/manifest.yaml with provenance:
      subject_id, dataset, source_raw_paths, source_set, rec_set,
      built_at, built_by (script version), build_args (filter config).


manifest.yaml schema
--------------------

```yaml
subject_id: "559"
dataset: "OhioT1DM"
dataset_tag: "OhioT1DM"
source_raw_paths:
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-training.xml"
  - "_WorkSpace/0-RawDataStore/OhioT1DM/559-ws-testing.xml"
source_set: "OhioT1DM_v0"
rec_set: "OhioT1DM_v0RecSet"
built_at: "2026-04-20T14:30:00"
built_by: "build_sample_subjects.py v0.1"
build_args:
  subject_id_filter: ["559"]
```


Build Contract
--------------

The build MUST be deterministic and reproducible. A single script (planned:
`fn/build_sample_subjects.py`) owns this:

  1. Read sample config (which datasets, which subject IDs, N per dataset).
  2. For each (dataset, subject_id):
     a. Steps 1-5 from Build Logic.
     b. Idempotent: skip if manifest.built_at is fresh.
  3. Emit a build report (what was built, what was skipped, any errors).

Do NOT hand-edit per-subject folders. They are derived, not source of truth.
Source of truth = global _WorkSpace/0-RawDataStore/ + the build script.


Consumers
---------

  Deployed endpoints (stage 6) read:
    manifest.yaml       → dataset + rec_set identification
    2-RecStore/         → the record for inference
    (NEVER read 3-6 — those don't exist per-subject anyway.)

  Tutorials and demos read:
    0-RawDataStore/     → "here's what one subject's raw data looks like"
    manifest.yaml       → attribution and provenance

  Privacy / deletion:
    rm -rf Subject-{DatasetTag}-{id}/  → wipes ALL derived data for one subject.
    Global stores untouched; re-run build to regenerate.


Relationship to Project-Wide Stores
------------------------------------

  Global _WorkSpace/ stores = BATCH work (training, cohort analysis):
    0-RawDataStore/{dataset}/*   ← whole dataset
    1-SourceStore/{SourceSet}/*  ← all subjects combined
    2-RecStore/{RecSet}/*        ← all records

  Per-subject UserGroup/Subject-*/ = SINGLE-SUBJECT serving:
    0-RawDataStore/             ← one subject's raw slice
    1-SourceStore/              ← one subject's source rows
    2-RecStore/                 ← one subject's record

  A per-subject folder is a VIEW of the global store, scoped to one ID,
  built by running the SAME pipeline with a subject filter.


Rules
-----

  - NEVER create stages 3-6 inside a Subject-*/ folder. Those are not per-subject.
  - ALWAYS dataset-qualify the folder name: Subject-{DatasetTag}-{id}.
  - ALWAYS write manifest.yaml — it's the provenance record.
  - If a dataset's raw format can't be cleanly sliced (e.g. proprietary binary),
    store a pointer manifest in 0-RawDataStore/ instead of copying.
  - The build script is the source of truth for how each dataset is sliced.
    Hand-curated subject folders drift and break — do not do it.
  - Subject folders are reproducible: `rm -rf` and re-run `build` must produce
    an equivalent folder (differences only in built_at timestamp).
